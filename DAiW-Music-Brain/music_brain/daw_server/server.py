"""
HTTP/REST server for DAW integration.

Provides endpoints for DAW plugins to request music generation.
"""

import json
import time
import uuid
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import queue

from .protocol import (
    MessageType,
    DAWMessage,
    GenerationParams,
    GenerationResult,
    MIDITrack,
    MIDINote,
    create_generation_response,
    create_progress_response,
    create_error_response,
)


@dataclass
class GenerationRequest:
    """A queued generation request."""
    id: str
    params: GenerationParams
    status: str = "pending"  # pending, processing, complete, error
    progress: float = 0.0
    result: Optional[GenerationResult] = None
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None


@dataclass
class GenerationResponse:
    """Response to a generation request."""
    request_id: str
    success: bool
    message: str
    arrangement: Optional[Dict[str, Any]] = None
    midi_data: Optional[Dict[str, Any]] = None
    production_notes: str = ""


class RequestQueue:
    """Thread-safe queue for generation requests."""

    def __init__(self, max_size: int = 100):
        self.queue: queue.Queue = queue.Queue(maxsize=max_size)
        self.requests: Dict[str, GenerationRequest] = {}
        self.lock = threading.Lock()

    def add(self, request: GenerationRequest) -> bool:
        """Add a request to the queue."""
        try:
            with self.lock:
                self.requests[request.id] = request
            self.queue.put(request.id, block=False)
            return True
        except queue.Full:
            return False

    def get_next(self, timeout: float = 1.0) -> Optional[GenerationRequest]:
        """Get the next request from the queue."""
        try:
            request_id = self.queue.get(timeout=timeout)
            with self.lock:
                return self.requests.get(request_id)
        except queue.Empty:
            return None

    def get_status(self, request_id: str) -> Optional[GenerationRequest]:
        """Get status of a specific request."""
        with self.lock:
            return self.requests.get(request_id)

    def update_status(self, request_id: str, status: str, progress: float = 0.0):
        """Update request status."""
        with self.lock:
            if request_id in self.requests:
                self.requests[request_id].status = status
                self.requests[request_id].progress = progress

    def set_result(self, request_id: str, result: GenerationResult):
        """Set the result for a completed request."""
        with self.lock:
            if request_id in self.requests:
                self.requests[request_id].result = result
                self.requests[request_id].status = "complete" if result.success else "error"
                self.requests[request_id].completed_at = time.time()

    def cleanup_old(self, max_age_seconds: float = 3600):
        """Remove old completed requests."""
        cutoff = time.time() - max_age_seconds
        with self.lock:
            to_remove = [
                rid for rid, req in self.requests.items()
                if req.completed_at and req.completed_at < cutoff
            ]
            for rid in to_remove:
                del self.requests[rid]


class DAWServer:
    """
    HTTP server for DAW integration.

    Provides REST API for:
    - Submitting generation requests
    - Checking request status
    - Retrieving results
    - Server status
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8765,
        max_workers: int = 2,
    ):
        self.host = host
        self.port = port
        self.max_workers = max_workers

        self.request_queue = RequestQueue()
        self.is_running = False
        self.server: Optional[HTTPServer] = None
        self.worker_threads: List[threading.Thread] = []

        # Stats
        self.stats = {
            "requests_received": 0,
            "requests_completed": 0,
            "requests_failed": 0,
            "start_time": None,
        }

    def _create_handler(self):
        """Create HTTP request handler class with server reference."""
        server_ref = self

        class DAWRequestHandler(BaseHTTPRequestHandler):
            server_instance = server_ref

            def log_message(self, format, *args):
                pass  # Suppress logging

            def _send_json(self, data: Dict[str, Any], status: int = 200):
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())

            def do_OPTIONS(self):
                """Handle CORS preflight."""
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

            def do_GET(self):
                """Handle GET requests."""
                parsed = urlparse(self.path)
                path = parsed.path
                query = parse_qs(parsed.query)

                if path == "/status":
                    self._handle_status()
                elif path == "/request/status":
                    request_id = query.get("id", [None])[0]
                    self._handle_request_status(request_id)
                elif path == "/health":
                    self._send_json({"status": "ok"})
                else:
                    self._send_json({"error": "Not found"}, 404)

            def do_POST(self):
                """Handle POST requests."""
                parsed = urlparse(self.path)
                path = parsed.path

                # Read body
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode()

                try:
                    data = json.loads(body) if body else {}
                except json.JSONDecodeError:
                    self._send_json({"error": "Invalid JSON"}, 400)
                    return

                if path == "/generate":
                    self._handle_generate(data)
                elif path == "/cancel":
                    self._handle_cancel(data)
                else:
                    self._send_json({"error": "Not found"}, 404)

            def _handle_status(self):
                """Return server status."""
                stats = self.server_instance.stats.copy()
                stats["is_running"] = self.server_instance.is_running
                stats["queue_size"] = len(self.server_instance.request_queue.requests)
                stats["uptime_seconds"] = (
                    time.time() - stats["start_time"]
                    if stats["start_time"] else 0
                )
                self._send_json(stats)

            def _handle_request_status(self, request_id: Optional[str]):
                """Return status of a specific request."""
                if not request_id:
                    self._send_json({"error": "Missing request ID"}, 400)
                    return

                request = self.server_instance.request_queue.get_status(request_id)
                if not request:
                    self._send_json({"error": "Request not found"}, 404)
                    return

                response = {
                    "id": request.id,
                    "status": request.status,
                    "progress": request.progress,
                    "created_at": request.created_at,
                }

                if request.result:
                    response["result"] = request.result.to_dict()

                self._send_json(response)

            def _handle_generate(self, data: Dict[str, Any]):
                """Handle generation request."""
                self.server_instance.stats["requests_received"] += 1

                # Parse parameters
                params = GenerationParams.from_dict(data)

                # Create request
                request_id = str(uuid.uuid4())[:8]
                request = GenerationRequest(id=request_id, params=params)

                # Add to queue
                if self.server_instance.request_queue.add(request):
                    self._send_json({
                        "success": True,
                        "request_id": request_id,
                        "message": "Generation request queued",
                    })
                else:
                    self._send_json({
                        "success": False,
                        "error": "Queue full",
                    }, 503)

            def _handle_cancel(self, data: Dict[str, Any]):
                """Handle cancel request."""
                request_id = data.get("request_id")
                if not request_id:
                    self._send_json({"error": "Missing request ID"}, 400)
                    return

                request = self.server_instance.request_queue.get_status(request_id)
                if request and request.status == "pending":
                    self.server_instance.request_queue.update_status(
                        request_id, "cancelled"
                    )
                    self._send_json({"success": True, "message": "Request cancelled"})
                else:
                    self._send_json({
                        "success": False,
                        "error": "Request not found or already processing"
                    }, 400)

        return DAWRequestHandler

    def _worker_loop(self):
        """Worker thread loop for processing requests."""
        while self.is_running:
            request = self.request_queue.get_next(timeout=1.0)
            if request and request.status == "pending":
                self._process_request(request)

    def _process_request(self, request: GenerationRequest):
        """Process a single generation request."""
        self.request_queue.update_status(request.id, "processing", 0.1)

        start_time = time.time()

        try:
            # Import arrangement module
            from music_brain.arrangement import generate_arrangement

            self.request_queue.update_status(request.id, "processing", 0.3)

            # Generate arrangement
            arrangement = generate_arrangement(
                title=request.params.title,
                genre=request.params.genre,
                key=request.params.key,
                tempo=request.params.tempo,
                chord_progression=request.params.chord_progression,
                mood=request.params.mood,
                vulnerability=request.params.vulnerability,
                narrative_arc=request.params.narrative_arc,
            )

            self.request_queue.update_status(request.id, "processing", 0.8)

            # Convert to MIDI tracks
            midi_tracks = self._arrangement_to_midi_tracks(arrangement)

            self.request_queue.update_status(request.id, "processing", 0.95)

            # Create result
            result = GenerationResult(
                success=True,
                message="Generation complete",
                arrangement=arrangement.to_dict(),
                midi_tracks=midi_tracks,
                production_notes=arrangement.production_notes,
                generation_time_ms=(time.time() - start_time) * 1000,
            )

            self.request_queue.set_result(request.id, result)
            self.stats["requests_completed"] += 1

        except Exception as e:
            result = GenerationResult(
                success=False,
                message=f"Generation failed: {str(e)}",
                generation_time_ms=(time.time() - start_time) * 1000,
            )
            self.request_queue.set_result(request.id, result)
            self.stats["requests_failed"] += 1

    def _arrangement_to_midi_tracks(self, arrangement) -> List[MIDITrack]:
        """Convert arrangement to MIDI track data."""
        tracks = []

        # Chord track
        chord_track = MIDITrack(name="Chords", channel=0)
        current_beat = 0

        for section in arrangement.sections:
            for chord_name, duration_bars in section.chords:
                # Simple root note for now
                root_pitch = 60  # Middle C
                note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

                chord_root = chord_name.replace("m", "").replace("7", "")[:2]
                if chord_root in note_names:
                    root_pitch = 60 + note_names.index(chord_root)

                chord_track.notes.append(MIDINote(
                    pitch=root_pitch,
                    start_beat=current_beat,
                    duration=duration_bars * 4,
                    velocity=70,
                    channel=0,
                ))

                current_beat += duration_bars * 4

        tracks.append(chord_track)

        # Bass track from bass_lines
        bass_track = MIDITrack(name="Bass", channel=1)
        for section_name, bass_line in arrangement.bass_lines.items():
            for note_data in bass_line.notes:
                bass_track.notes.append(MIDINote(
                    pitch=note_data.pitch,
                    start_beat=note_data.start_beat,
                    duration=note_data.duration,
                    velocity=note_data.velocity,
                    channel=1,
                ))

        tracks.append(bass_track)

        return tracks

    def start(self, blocking: bool = True):
        """
        Start the server.

        Args:
            blocking: If True, blocks until server is stopped.
                     If False, runs in background thread.
        """
        self.is_running = True
        self.stats["start_time"] = time.time()

        # Create server
        handler_class = self._create_handler()
        self.server = HTTPServer((self.host, self.port), handler_class)

        # Start worker threads
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self.worker_threads.append(worker)

        print(f"iDAW Server starting on http://{self.host}:{self.port}")
        print("Endpoints:")
        print("  GET  /status         - Server status")
        print("  GET  /health         - Health check")
        print("  GET  /request/status - Request status (id=<id>)")
        print("  POST /generate       - Submit generation request")
        print("  POST /cancel         - Cancel pending request")

        if blocking:
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                self.stop()
        else:
            server_thread = threading.Thread(
                target=self.server.serve_forever,
                daemon=True
            )
            server_thread.start()

    def stop(self):
        """Stop the server."""
        print("\nShutting down server...")
        self.is_running = False

        if self.server:
            self.server.shutdown()

        for worker in self.worker_threads:
            worker.join(timeout=2.0)

        print("Server stopped.")


def start_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    blocking: bool = True
) -> DAWServer:
    """
    Start the DAW integration server.

    Args:
        host: Host address
        port: Port number
        blocking: If True, blocks until server is stopped

    Returns:
        DAWServer instance
    """
    server = DAWServer(host=host, port=port)
    server.start(blocking=blocking)
    return server


# CLI entry point
def main():
    """CLI entry point for the server."""
    import argparse

    parser = argparse.ArgumentParser(description="iDAW Server for DAW Integration")
    parser.add_argument("--host", default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, default=8765, help="Port number")

    args = parser.parse_args()

    server = DAWServer(host=args.host, port=args.port)
    server.start(blocking=True)


if __name__ == "__main__":
    main()
