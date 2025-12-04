"""
Communication protocol for DAW integration.

Defines message formats and serialization for DAW <-> Server communication.
"""

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime


class MessageType(Enum):
    """Types of messages in the DAW protocol."""
    # Requests
    GENERATE_REQUEST = "generate_request"
    STATUS_REQUEST = "status_request"
    CANCEL_REQUEST = "cancel_request"
    HEARTBEAT = "heartbeat"

    # Responses
    GENERATION_COMPLETE = "generation_complete"
    GENERATION_PROGRESS = "generation_progress"
    GENERATION_ERROR = "generation_error"
    STATUS_RESPONSE = "status_response"
    HEARTBEAT_ACK = "heartbeat_ack"

    # Data transfer
    MIDI_DATA = "midi_data"
    ARRANGEMENT_DATA = "arrangement_data"


@dataclass
class DAWMessage:
    """Base message class for DAW communication."""
    type: MessageType
    id: str  # Unique message ID
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "id": self.id,
            "timestamp": self.timestamp,
            "payload": self.payload,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DAWMessage":
        return cls(
            type=MessageType(data["type"]),
            id=data["id"],
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            payload=data.get("payload", {}),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "DAWMessage":
        return cls.from_dict(json.loads(json_str))


@dataclass
class GenerationParams:
    """Parameters for music generation."""
    title: str = "Untitled"
    genre: str = "pop"
    key: str = "C"
    tempo: float = 120.0
    mood: str = "neutral"
    vulnerability: float = 0.5
    narrative_arc: str = "transformation"
    chord_progression: Optional[List[str]] = None
    rule_to_break: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GenerationParams":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class MIDINote:
    """Representation of a MIDI note."""
    pitch: int
    start_beat: float
    duration: float
    velocity: int = 80
    channel: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MIDITrack:
    """Representation of a MIDI track."""
    name: str
    channel: int
    notes: List[MIDINote] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "channel": self.channel,
            "notes": [n.to_dict() for n in self.notes],
        }


@dataclass
class GenerationResult:
    """Result of a generation request."""
    success: bool
    message: str = ""
    arrangement: Optional[Dict[str, Any]] = None
    midi_tracks: List[MIDITrack] = field(default_factory=list)
    production_notes: str = ""
    generation_time_ms: float = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "arrangement": self.arrangement,
            "midi_tracks": [t.to_dict() for t in self.midi_tracks],
            "production_notes": self.production_notes,
            "generation_time_ms": self.generation_time_ms,
        }


# Message factory functions

def create_generation_request(
    request_id: str,
    params: GenerationParams
) -> DAWMessage:
    """Create a generation request message."""
    return DAWMessage(
        type=MessageType.GENERATE_REQUEST,
        id=request_id,
        payload=params.to_dict(),
    )


def create_status_request(request_id: str) -> DAWMessage:
    """Create a status request message."""
    return DAWMessage(
        type=MessageType.STATUS_REQUEST,
        id=request_id,
    )


def create_cancel_request(request_id: str, target_id: str) -> DAWMessage:
    """Create a cancel request message."""
    return DAWMessage(
        type=MessageType.CANCEL_REQUEST,
        id=request_id,
        payload={"target_id": target_id},
    )


def create_heartbeat(request_id: str) -> DAWMessage:
    """Create a heartbeat message."""
    return DAWMessage(
        type=MessageType.HEARTBEAT,
        id=request_id,
    )


def create_generation_response(
    request_id: str,
    result: GenerationResult
) -> DAWMessage:
    """Create a generation complete response."""
    return DAWMessage(
        type=MessageType.GENERATION_COMPLETE,
        id=request_id,
        payload=result.to_dict(),
    )


def create_progress_response(
    request_id: str,
    progress: float,
    status: str
) -> DAWMessage:
    """Create a progress update response."""
    return DAWMessage(
        type=MessageType.GENERATION_PROGRESS,
        id=request_id,
        payload={
            "progress": progress,
            "status": status,
        },
    )


def create_error_response(
    request_id: str,
    error: str,
    details: Optional[str] = None
) -> DAWMessage:
    """Create an error response."""
    return DAWMessage(
        type=MessageType.GENERATION_ERROR,
        id=request_id,
        payload={
            "error": error,
            "details": details or "",
        },
    )


def parse_response(message: DAWMessage) -> Dict[str, Any]:
    """
    Parse a response message and return structured data.

    Returns a dict with 'success', 'data', and 'error' keys.
    """
    if message.type == MessageType.GENERATION_COMPLETE:
        return {
            "success": message.payload.get("success", False),
            "data": message.payload,
            "error": None,
        }

    elif message.type == MessageType.GENERATION_ERROR:
        return {
            "success": False,
            "data": None,
            "error": message.payload.get("error", "Unknown error"),
        }

    elif message.type == MessageType.GENERATION_PROGRESS:
        return {
            "success": True,
            "data": {
                "progress": message.payload.get("progress", 0),
                "status": message.payload.get("status", ""),
            },
            "error": None,
        }

    elif message.type == MessageType.STATUS_RESPONSE:
        return {
            "success": True,
            "data": message.payload,
            "error": None,
        }

    elif message.type == MessageType.HEARTBEAT_ACK:
        return {
            "success": True,
            "data": {"alive": True},
            "error": None,
        }

    return {
        "success": False,
        "data": None,
        "error": f"Unknown message type: {message.type}",
    }


# OSC address patterns
OSC_ADDRESSES = {
    "generate": "/idaw/generate",
    "status": "/idaw/status",
    "cancel": "/idaw/cancel",
    "heartbeat": "/idaw/heartbeat",
    "response": "/idaw/response",
    "progress": "/idaw/progress",
    "error": "/idaw/error",
    "midi": "/idaw/midi",
}


def format_osc_message(address: str, *args) -> tuple:
    """Format an OSC message tuple."""
    return (address, args)


def create_osc_generation_request(params: GenerationParams) -> tuple:
    """Create OSC message for generation request."""
    return format_osc_message(
        OSC_ADDRESSES["generate"],
        params.genre,
        params.key,
        params.tempo,
        params.mood,
        params.title,
    )
