"""
MIDI export functionality for iDAW Desktop.

Converts generated arrangements to MIDI files.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

# Try to import mido for MIDI operations
try:
    import mido
    from mido import MidiFile, MidiTrack, Message, MetaMessage
    MIDO_AVAILABLE = True
except ImportError:
    MIDO_AVAILABLE = False


# Note name to MIDI pitch mapping
NOTE_TO_MIDI: Dict[str, int] = {
    "C": 60, "C#": 61, "Db": 61, "D": 62, "D#": 63, "Eb": 63,
    "E": 64, "F": 65, "F#": 66, "Gb": 66, "G": 67, "G#": 68,
    "Ab": 68, "A": 69, "A#": 70, "Bb": 70, "B": 71,
}

# Chord quality to intervals
CHORD_INTERVALS: Dict[str, List[int]] = {
    "": [0, 4, 7],  # Major
    "m": [0, 3, 7],  # Minor
    "7": [0, 4, 7, 10],
    "maj7": [0, 4, 7, 11],
    "m7": [0, 3, 7, 10],
    "dim": [0, 3, 6],
    "aug": [0, 4, 8],
    "sus2": [0, 2, 7],
    "sus4": [0, 5, 7],
}


def check_mido():
    """Check if mido is available."""
    if not MIDO_AVAILABLE:
        raise ImportError(
            "mido is required for MIDI export. "
            "Install with: pip install mido"
        )


def parse_chord(chord: str) -> Tuple[int, List[int]]:
    """Parse chord symbol to root pitch and intervals."""
    chord = chord.strip()

    # Extract root
    if len(chord) >= 2 and chord[1] in "#b":
        root = chord[:2]
        quality = chord[2:]
    else:
        root = chord[0]
        quality = chord[1:]

    # Handle minor key notation (e.g., "Am" where m is the quality)
    if quality.startswith("m") and len(quality) > 1:
        quality = "m" + quality[1:]
    elif quality == "m":
        quality = "m"

    root_pitch = NOTE_TO_MIDI.get(root, 60)
    intervals = CHORD_INTERVALS.get(quality, CHORD_INTERVALS[""])

    return root_pitch, intervals


def chord_to_notes(chord: str, octave_offset: int = 0) -> List[int]:
    """Convert chord symbol to list of MIDI note numbers."""
    root_pitch, intervals = parse_chord(chord)
    base_pitch = root_pitch + (octave_offset * 12)
    return [base_pitch + interval for interval in intervals]


@dataclass
class MIDIExportConfig:
    """Configuration for MIDI export."""
    ticks_per_beat: int = 480
    default_velocity: int = 80
    chord_velocity: int = 70
    bass_velocity: int = 85
    drum_velocity: int = 90

    # Track channels
    chord_channel: int = 0
    bass_channel: int = 1
    drum_channel: int = 9  # Standard MIDI drum channel

    # Octave settings
    chord_octave: int = 0  # Middle C area
    bass_octave: int = -2  # Two octaves below


class MIDIExporter:
    """Exports arrangements to MIDI files."""

    def __init__(self, config: Optional[MIDIExportConfig] = None):
        check_mido()
        self.config = config or MIDIExportConfig()

    def export_arrangement(
        self,
        arrangement: Dict[str, Any],
        output_path: str,
        include_bass: bool = True,
        include_markers: bool = True,
    ) -> str:
        """
        Export a complete arrangement to MIDI.

        Args:
            arrangement: Arrangement dict with sections, bass_lines, etc.
            output_path: Path for output MIDI file
            include_bass: Include bass track
            include_markers: Include section markers

        Returns:
            Path to exported file
        """
        mid = MidiFile(ticks_per_beat=self.config.ticks_per_beat)

        # Tempo track
        tempo_track = MidiTrack()
        mid.tracks.append(tempo_track)

        tempo = arrangement.get("tempo", 120)
        tempo_track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))
        tempo_track.append(MetaMessage('time_signature', numerator=4, denominator=4))
        tempo_track.append(MetaMessage('track_name', name='Tempo'))

        # Add section markers
        if include_markers:
            self._add_markers(tempo_track, arrangement)

        # Chord track
        chord_track = MidiTrack()
        mid.tracks.append(chord_track)
        chord_track.append(MetaMessage('track_name', name='Chords'))
        self._add_chords(chord_track, arrangement)

        # Bass track
        if include_bass:
            bass_track = MidiTrack()
            mid.tracks.append(bass_track)
            bass_track.append(MetaMessage('track_name', name='Bass'))
            self._add_bass(bass_track, arrangement)

        # Save
        mid.save(output_path)
        return output_path

    def _add_markers(self, track: MidiTrack, arrangement: Dict[str, Any]):
        """Add section markers to track."""
        current_tick = 0
        ticks_per_bar = self.config.ticks_per_beat * 4

        for section in arrangement.get("sections", []):
            start_bar = section.get("start_bar", 0)
            start_tick = start_bar * ticks_per_bar

            # Calculate delta time
            delta = start_tick - current_tick
            if delta < 0:
                delta = 0

            track.append(MetaMessage(
                'marker',
                text=section.get("name", "Section"),
                time=delta
            ))
            current_tick = start_tick

    def _add_chords(self, track: MidiTrack, arrangement: Dict[str, Any]):
        """Add chord notes to track."""
        ticks_per_bar = self.config.ticks_per_beat * 4
        current_tick = 0

        for section in arrangement.get("sections", []):
            chords = section.get("chords", [])
            energy = section.get("energy", 0.5)

            # Velocity based on energy
            velocity = int(self.config.chord_velocity * (0.7 + energy * 0.4))
            velocity = min(127, max(30, velocity))

            for chord_name, duration_bars in chords:
                notes = chord_to_notes(chord_name, self.config.chord_octave)
                duration_ticks = duration_bars * ticks_per_bar

                # Note on events
                for i, note in enumerate(notes):
                    delta = 0 if i > 0 else (current_tick - sum(m.time for m in track))
                    if delta < 0:
                        delta = 0
                    track.append(Message(
                        'note_on',
                        channel=self.config.chord_channel,
                        note=note,
                        velocity=velocity,
                        time=delta if i == 0 else 0
                    ))

                # Note off events
                for i, note in enumerate(notes):
                    track.append(Message(
                        'note_off',
                        channel=self.config.chord_channel,
                        note=note,
                        velocity=0,
                        time=duration_ticks if i == 0 else 0
                    ))

                current_tick += duration_ticks

    def _add_bass(self, track: MidiTrack, arrangement: Dict[str, Any]):
        """Add bass notes to track."""
        bass_lines = arrangement.get("bass_lines", {})

        if not bass_lines:
            # Generate simple bass from chords
            self._add_simple_bass(track, arrangement)
            return

        # Use generated bass lines
        for section_name, bass_line in bass_lines.items():
            notes = bass_line.get("notes", [])

            for note_data in notes:
                pitch = note_data.get("pitch", 36)
                start_beat = note_data.get("start_beat", 0)
                duration = note_data.get("duration", 1)
                velocity = note_data.get("velocity", self.config.bass_velocity)

                start_tick = int(start_beat * self.config.ticks_per_beat)
                duration_ticks = int(duration * self.config.ticks_per_beat)

                # Note on
                track.append(Message(
                    'note_on',
                    channel=self.config.bass_channel,
                    note=pitch,
                    velocity=velocity,
                    time=start_tick
                ))

                # Note off
                track.append(Message(
                    'note_off',
                    channel=self.config.bass_channel,
                    note=pitch,
                    velocity=0,
                    time=duration_ticks
                ))

    def _add_simple_bass(self, track: MidiTrack, arrangement: Dict[str, Any]):
        """Add simple root-note bass from chords."""
        ticks_per_bar = self.config.ticks_per_beat * 4

        for section in arrangement.get("sections", []):
            chords = section.get("chords", [])
            energy = section.get("energy", 0.5)

            velocity = int(self.config.bass_velocity * (0.7 + energy * 0.3))
            velocity = min(127, max(40, velocity))

            for chord_name, duration_bars in chords:
                root_pitch, _ = parse_chord(chord_name)
                bass_pitch = root_pitch + (self.config.bass_octave * 12)

                duration_ticks = duration_bars * ticks_per_bar

                track.append(Message(
                    'note_on',
                    channel=self.config.bass_channel,
                    note=bass_pitch,
                    velocity=velocity,
                    time=0
                ))

                track.append(Message(
                    'note_off',
                    channel=self.config.bass_channel,
                    note=bass_pitch,
                    velocity=0,
                    time=duration_ticks
                ))

    def export_bass_line(
        self,
        bass_line: Dict[str, Any],
        output_path: str,
        tempo: float = 120.0
    ) -> str:
        """Export a bass line to MIDI."""
        mid = MidiFile(ticks_per_beat=self.config.ticks_per_beat)

        # Tempo track
        tempo_track = MidiTrack()
        mid.tracks.append(tempo_track)
        tempo_track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))

        # Bass track
        bass_track = MidiTrack()
        mid.tracks.append(bass_track)
        bass_track.append(MetaMessage('track_name', name='Bass'))

        current_tick = 0

        for note_data in bass_line.get("notes", []):
            pitch = note_data.get("pitch", 36)
            start_beat = note_data.get("start_beat", 0)
            duration = note_data.get("duration", 1)
            velocity = note_data.get("velocity", self.config.bass_velocity)

            start_tick = int(start_beat * self.config.ticks_per_beat)
            duration_ticks = int(duration * self.config.ticks_per_beat)

            # Delta from current position
            delta = start_tick - current_tick
            if delta < 0:
                delta = 0

            bass_track.append(Message(
                'note_on',
                channel=self.config.bass_channel,
                note=pitch,
                velocity=velocity,
                time=delta
            ))

            bass_track.append(Message(
                'note_off',
                channel=self.config.bass_channel,
                note=pitch,
                velocity=0,
                time=duration_ticks
            ))

            current_tick = start_tick + duration_ticks

        mid.save(output_path)
        return output_path


def export_arrangement_to_midi(
    arrangement: Dict[str, Any],
    output_path: str,
    **kwargs
) -> str:
    """
    Convenience function to export arrangement to MIDI.

    Args:
        arrangement: Arrangement dictionary
        output_path: Output file path
        **kwargs: Additional options for MIDIExporter.export_arrangement

    Returns:
        Path to exported file
    """
    exporter = MIDIExporter()
    return exporter.export_arrangement(arrangement, output_path, **kwargs)


def export_chords_to_midi(
    chords: List[Tuple[str, int]],
    output_path: str,
    tempo: float = 120.0
) -> str:
    """
    Export a simple chord progression to MIDI.

    Args:
        chords: List of (chord_name, duration_bars) tuples
        output_path: Output file path
        tempo: Tempo in BPM

    Returns:
        Path to exported file
    """
    check_mido()

    config = MIDIExportConfig()
    mid = MidiFile(ticks_per_beat=config.ticks_per_beat)

    # Tempo track
    tempo_track = MidiTrack()
    mid.tracks.append(tempo_track)
    tempo_track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))

    # Chord track
    chord_track = MidiTrack()
    mid.tracks.append(chord_track)

    ticks_per_bar = config.ticks_per_beat * 4

    for chord_name, duration_bars in chords:
        notes = chord_to_notes(chord_name, config.chord_octave)
        duration_ticks = duration_bars * ticks_per_bar

        # Note on
        for i, note in enumerate(notes):
            chord_track.append(Message(
                'note_on',
                channel=0,
                note=note,
                velocity=config.chord_velocity,
                time=0
            ))

        # Note off
        for i, note in enumerate(notes):
            chord_track.append(Message(
                'note_off',
                channel=0,
                note=note,
                velocity=0,
                time=duration_ticks if i == 0 else 0
            ))

    mid.save(output_path)
    return output_path
