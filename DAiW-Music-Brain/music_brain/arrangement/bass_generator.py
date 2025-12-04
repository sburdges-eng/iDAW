"""
Bass line generator for iDAW Music Brain.

Generates bass lines from chord progressions with genre-appropriate patterns.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any
import random


class BassPattern(Enum):
    """Types of bass patterns."""
    ROOT = "root"  # Play root notes only
    ROOT_FIFTH = "root_fifth"  # Root and fifth alternation
    WALKING = "walking"  # Jazz walking bass
    OCTAVE = "octave"  # Root and octave
    ARPEGGIATED = "arpeggiated"  # Arpeggiate chord tones
    SYNCOPATED = "syncopated"  # Off-beat accents
    PEDAL = "pedal"  # Sustained pedal tone
    DRIVING = "driving"  # Eighth note driving pattern
    FUNK = "funk"  # Syncopated funk pattern
    REGGAE = "reggae"  # Off-beat reggae pattern


@dataclass
class BassNote:
    """Represents a single bass note."""
    pitch: int  # MIDI pitch (0-127)
    start_beat: float  # Beat position (e.g., 1.0, 1.5, 2.0)
    duration: float  # Duration in beats
    velocity: int = 80  # MIDI velocity (0-127)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pitch": self.pitch,
            "start_beat": self.start_beat,
            "duration": self.duration,
            "velocity": self.velocity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BassNote":
        return cls(
            pitch=data["pitch"],
            start_beat=data["start_beat"],
            duration=data["duration"],
            velocity=data.get("velocity", 80),
        )


@dataclass
class BassPedal:
    """Represents a pedal tone (sustained bass note)."""
    pitch: int
    start_bar: int
    duration_bars: int
    velocity: int = 70

    def to_notes(self, beats_per_bar: int = 4) -> List[BassNote]:
        """Convert pedal to individual tied notes."""
        notes = []
        total_beats = self.duration_bars * beats_per_bar
        start_beat = self.start_bar * beats_per_bar

        # Create tied notes for each bar
        for bar in range(self.duration_bars):
            bar_start = start_beat + (bar * beats_per_bar)
            notes.append(BassNote(
                pitch=self.pitch,
                start_beat=bar_start,
                duration=float(beats_per_bar),
                velocity=self.velocity,
            ))

        return notes


@dataclass
class BassLine:
    """Complete bass line for a song section or entire song."""
    notes: List[BassNote] = field(default_factory=list)
    pattern: BassPattern = BassPattern.ROOT
    key: str = "C"
    total_bars: int = 0
    beats_per_bar: int = 4

    def to_dict(self) -> Dict[str, Any]:
        return {
            "notes": [n.to_dict() for n in self.notes],
            "pattern": self.pattern.value,
            "key": self.key,
            "total_bars": self.total_bars,
            "beats_per_bar": self.beats_per_bar,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BassLine":
        return cls(
            notes=[BassNote.from_dict(n) for n in data["notes"]],
            pattern=BassPattern(data["pattern"]),
            key=data.get("key", "C"),
            total_bars=data.get("total_bars", 0),
            beats_per_bar=data.get("beats_per_bar", 4),
        )

    def add_note(self, pitch: int, start_beat: float, duration: float, velocity: int = 80):
        """Add a note to the bass line."""
        self.notes.append(BassNote(pitch, start_beat, duration, velocity))

    def get_notes_in_bar(self, bar: int) -> List[BassNote]:
        """Get all notes in a specific bar."""
        bar_start = bar * self.beats_per_bar
        bar_end = bar_start + self.beats_per_bar
        return [n for n in self.notes if bar_start <= n.start_beat < bar_end]


# Note name to MIDI pitch mapping (bass range, octave 2-3)
NOTE_TO_MIDI: Dict[str, int] = {
    "C": 36, "C#": 37, "Db": 37, "D": 38, "D#": 39, "Eb": 39,
    "E": 40, "F": 41, "F#": 42, "Gb": 42, "G": 43, "G#": 44,
    "Ab": 44, "A": 45, "A#": 46, "Bb": 46, "B": 47,
}

# Chord quality to intervals mapping
CHORD_INTERVALS: Dict[str, List[int]] = {
    "": [0, 4, 7],  # Major
    "m": [0, 3, 7],  # Minor
    "7": [0, 4, 7, 10],  # Dominant 7
    "maj7": [0, 4, 7, 11],  # Major 7
    "m7": [0, 3, 7, 10],  # Minor 7
    "dim": [0, 3, 6],  # Diminished
    "dim7": [0, 3, 6, 9],  # Diminished 7
    "aug": [0, 4, 8],  # Augmented
    "sus2": [0, 2, 7],  # Suspended 2
    "sus4": [0, 5, 7],  # Suspended 4
    "add9": [0, 4, 7, 14],  # Add 9
    "6": [0, 4, 7, 9],  # Major 6
    "m6": [0, 3, 7, 9],  # Minor 6
}


def parse_chord(chord: str) -> Tuple[int, List[int]]:
    """
    Parse a chord symbol into root pitch and intervals.

    Args:
        chord: Chord symbol (e.g., "C", "Am", "F#m7")

    Returns:
        Tuple of (root_midi_pitch, intervals)
    """
    chord = chord.strip()

    # Extract root note
    if len(chord) >= 2 and chord[1] in "#b":
        root = chord[:2]
        quality = chord[2:]
    else:
        root = chord[0]
        quality = chord[1:]

    # Get root pitch
    root_pitch = NOTE_TO_MIDI.get(root, 36)  # Default to C

    # Get intervals for quality
    intervals = CHORD_INTERVALS.get(quality, CHORD_INTERVALS[""])

    return root_pitch, intervals


def generate_bass_pattern(
    chord: str,
    pattern: BassPattern,
    bar_start: int,
    bars: int = 1,
    beats_per_bar: int = 4,
    velocity: int = 80,
    energy: float = 0.5
) -> List[BassNote]:
    """
    Generate bass notes for a chord using a specific pattern.

    Args:
        chord: Chord symbol
        pattern: Bass pattern type
        bar_start: Starting bar number
        bars: Number of bars
        beats_per_bar: Beats per bar (time signature)
        velocity: Base MIDI velocity
        energy: Energy level (0.0-1.0) affects velocity variation

    Returns:
        List of BassNote objects
    """
    root_pitch, intervals = parse_chord(chord)
    notes = []

    # Adjust velocity based on energy
    vel_min = int(velocity * (0.7 + energy * 0.3))
    vel_max = min(127, int(velocity * (0.9 + energy * 0.2)))

    for bar in range(bars):
        bar_offset = (bar_start + bar) * beats_per_bar

        if pattern == BassPattern.ROOT:
            # Whole note on root
            notes.append(BassNote(
                pitch=root_pitch,
                start_beat=bar_offset,
                duration=float(beats_per_bar),
                velocity=random.randint(vel_min, vel_max),
            ))

        elif pattern == BassPattern.ROOT_FIFTH:
            # Root on beat 1, fifth on beat 3
            notes.append(BassNote(
                pitch=root_pitch,
                start_beat=bar_offset,
                duration=2.0,
                velocity=random.randint(vel_min, vel_max),
            ))
            fifth = root_pitch + 7  # Perfect fifth
            notes.append(BassNote(
                pitch=fifth,
                start_beat=bar_offset + 2,
                duration=2.0,
                velocity=random.randint(vel_min - 5, vel_max - 5),
            ))

        elif pattern == BassPattern.OCTAVE:
            # Root, then octave above
            notes.append(BassNote(
                pitch=root_pitch,
                start_beat=bar_offset,
                duration=2.0,
                velocity=random.randint(vel_min, vel_max),
            ))
            notes.append(BassNote(
                pitch=root_pitch + 12,
                start_beat=bar_offset + 2,
                duration=2.0,
                velocity=random.randint(vel_min - 5, vel_max - 5),
            ))

        elif pattern == BassPattern.WALKING:
            # Jazz walking bass: chromatic/scalar approach
            scale_notes = [root_pitch, root_pitch + 2, root_pitch + 4, root_pitch + 5]
            approach = random.choice([-1, 1])  # Chromatic approach

            for beat in range(beats_per_bar):
                if beat < 3:
                    pitch = scale_notes[beat % len(scale_notes)]
                else:
                    # Approach note to next chord
                    pitch = root_pitch + 7 + approach

                notes.append(BassNote(
                    pitch=pitch,
                    start_beat=bar_offset + beat,
                    duration=1.0,
                    velocity=random.randint(vel_min, vel_max),
                ))

        elif pattern == BassPattern.ARPEGGIATED:
            # Arpeggiate chord tones
            chord_tones = [root_pitch + i for i in intervals[:4]]

            for beat, pitch in enumerate(chord_tones[:beats_per_bar]):
                notes.append(BassNote(
                    pitch=pitch,
                    start_beat=bar_offset + beat,
                    duration=1.0,
                    velocity=random.randint(vel_min, vel_max),
                ))

        elif pattern == BassPattern.SYNCOPATED:
            # Off-beat syncopation
            positions = [0, 1.5, 2.5, 3.5]  # Syncopated positions
            for pos in positions:
                notes.append(BassNote(
                    pitch=root_pitch if pos == 0 else root_pitch + 7,
                    start_beat=bar_offset + pos,
                    duration=0.5,
                    velocity=random.randint(vel_min, vel_max),
                ))

        elif pattern == BassPattern.PEDAL:
            # Sustained pedal tone
            notes.append(BassNote(
                pitch=root_pitch,
                start_beat=bar_offset,
                duration=float(beats_per_bar),
                velocity=random.randint(vel_min - 10, vel_max - 10),
            ))

        elif pattern == BassPattern.DRIVING:
            # Driving eighth notes
            for eighth in range(beats_per_bar * 2):
                pitch = root_pitch if eighth % 2 == 0 else root_pitch + 7
                accent = 10 if eighth % 2 == 0 else 0
                notes.append(BassNote(
                    pitch=pitch,
                    start_beat=bar_offset + (eighth * 0.5),
                    duration=0.5,
                    velocity=min(127, random.randint(vel_min, vel_max) + accent),
                ))

        elif pattern == BassPattern.FUNK:
            # Syncopated funk pattern
            funk_hits = [0, 0.75, 1.5, 2.25, 3.0, 3.5]
            for hit in funk_hits:
                ghost = random.random() < 0.3  # 30% ghost notes
                notes.append(BassNote(
                    pitch=root_pitch,
                    start_beat=bar_offset + hit,
                    duration=0.25,
                    velocity=random.randint(vel_min - 20, vel_max - 20) if ghost else random.randint(vel_min, vel_max),
                ))

        elif pattern == BassPattern.REGGAE:
            # Off-beat reggae
            for beat in range(beats_per_bar):
                notes.append(BassNote(
                    pitch=root_pitch,
                    start_beat=bar_offset + beat + 0.5,  # Off-beat
                    duration=0.5,
                    velocity=random.randint(vel_min, vel_max),
                ))

    return notes


def select_pattern_for_genre(genre: str, section_type: str = "verse") -> BassPattern:
    """
    Select appropriate bass pattern based on genre and section.

    Args:
        genre: Genre name
        section_type: Section type (intro, verse, chorus, etc.)

    Returns:
        Appropriate BassPattern
    """
    genre = genre.lower()

    # Genre-specific patterns
    genre_patterns: Dict[str, Dict[str, BassPattern]] = {
        "pop": {
            "intro": BassPattern.ROOT,
            "verse": BassPattern.ROOT_FIFTH,
            "chorus": BassPattern.OCTAVE,
            "bridge": BassPattern.ROOT,
            "outro": BassPattern.ROOT,
        },
        "rock": {
            "intro": BassPattern.DRIVING,
            "verse": BassPattern.ROOT_FIFTH,
            "chorus": BassPattern.DRIVING,
            "bridge": BassPattern.ROOT,
            "solo": BassPattern.DRIVING,
            "outro": BassPattern.ROOT,
        },
        "folk": {
            "intro": BassPattern.PEDAL,
            "verse": BassPattern.ROOT,
            "chorus": BassPattern.ROOT_FIFTH,
            "bridge": BassPattern.PEDAL,
            "outro": BassPattern.PEDAL,
        },
        "lofi": {
            "intro": BassPattern.PEDAL,
            "verse": BassPattern.ROOT,
            "chorus": BassPattern.ROOT_FIFTH,
            "outro": BassPattern.PEDAL,
        },
        "jazz": {
            "intro": BassPattern.WALKING,
            "verse": BassPattern.WALKING,
            "chorus": BassPattern.WALKING,
            "bridge": BassPattern.WALKING,
            "solo": BassPattern.WALKING,
            "outro": BassPattern.PEDAL,
        },
        "edm": {
            "intro": BassPattern.PEDAL,
            "buildup": BassPattern.SYNCOPATED,
            "drop": BassPattern.DRIVING,
            "breakdown": BassPattern.PEDAL,
            "outro": BassPattern.PEDAL,
        },
        "funk": {
            "intro": BassPattern.FUNK,
            "verse": BassPattern.FUNK,
            "chorus": BassPattern.FUNK,
            "bridge": BassPattern.SYNCOPATED,
            "outro": BassPattern.FUNK,
        },
        "hiphop": {
            "intro": BassPattern.ROOT,
            "verse": BassPattern.SYNCOPATED,
            "chorus": BassPattern.OCTAVE,
            "bridge": BassPattern.PEDAL,
            "outro": BassPattern.ROOT,
        },
        "rnb": {
            "intro": BassPattern.PEDAL,
            "verse": BassPattern.ROOT_FIFTH,
            "chorus": BassPattern.ARPEGGIATED,
            "bridge": BassPattern.PEDAL,
            "outro": BassPattern.PEDAL,
        },
        "reggae": {
            "intro": BassPattern.REGGAE,
            "verse": BassPattern.REGGAE,
            "chorus": BassPattern.REGGAE,
            "bridge": BassPattern.PEDAL,
            "outro": BassPattern.REGGAE,
        },
    }

    section_type = section_type.lower().replace("_", "").replace("-", "")

    if genre in genre_patterns:
        patterns = genre_patterns[genre]
        return patterns.get(section_type, BassPattern.ROOT_FIFTH)

    # Default patterns
    default_patterns = {
        "intro": BassPattern.ROOT,
        "verse": BassPattern.ROOT_FIFTH,
        "prechorus": BassPattern.ROOT_FIFTH,
        "chorus": BassPattern.OCTAVE,
        "bridge": BassPattern.ROOT,
        "breakdown": BassPattern.PEDAL,
        "buildup": BassPattern.SYNCOPATED,
        "drop": BassPattern.DRIVING,
        "solo": BassPattern.ROOT_FIFTH,
        "outro": BassPattern.PEDAL,
    }

    return default_patterns.get(section_type, BassPattern.ROOT)


def generate_bass_line(
    chords: List[Tuple[str, int]],  # (chord_name, duration_in_bars)
    genre: str = "pop",
    key: str = "C",
    tempo: float = 120.0,
    beats_per_bar: int = 4,
    section_type: str = "verse",
    energy: float = 0.5,
    velocity: int = 80,
) -> BassLine:
    """
    Generate a complete bass line from a chord progression.

    Args:
        chords: List of (chord_name, duration_in_bars) tuples
        genre: Genre for pattern selection
        key: Key of the song (for reference)
        tempo: Tempo in BPM
        beats_per_bar: Time signature numerator
        section_type: Type of section (verse, chorus, etc.)
        energy: Energy level (0.0-1.0)
        velocity: Base MIDI velocity

    Returns:
        Complete BassLine object

    Example:
        >>> chords = [("C", 2), ("Am", 2), ("F", 2), ("G", 2)]
        >>> bass = generate_bass_line(chords, genre="pop", section_type="verse")
    """
    bass_line = BassLine(
        pattern=select_pattern_for_genre(genre, section_type),
        key=key,
        beats_per_bar=beats_per_bar,
    )

    current_bar = 0
    for chord, duration_bars in chords:
        notes = generate_bass_pattern(
            chord=chord,
            pattern=bass_line.pattern,
            bar_start=current_bar,
            bars=duration_bars,
            beats_per_bar=beats_per_bar,
            velocity=velocity,
            energy=energy,
        )
        bass_line.notes.extend(notes)
        current_bar += duration_bars

    bass_line.total_bars = current_bar
    return bass_line


def generate_bass_for_arrangement(
    sections: List[Dict[str, Any]],
    chords_per_section: Dict[str, List[Tuple[str, int]]],
    genre: str = "pop",
    key: str = "C",
) -> Dict[str, BassLine]:
    """
    Generate bass lines for an entire arrangement.

    Args:
        sections: List of section dicts with 'name', 'type', 'energy', 'bars'
        chords_per_section: Dict mapping section names to chord progressions
        genre: Genre for pattern selection
        key: Key of the song

    Returns:
        Dict mapping section names to BassLine objects

    Example:
        >>> sections = [
        ...     {"name": "verse1", "type": "verse", "energy": 0.5, "bars": 8},
        ...     {"name": "chorus1", "type": "chorus", "energy": 0.8, "bars": 8},
        ... ]
        >>> chords = {
        ...     "verse1": [("C", 2), ("Am", 2), ("F", 2), ("G", 2)],
        ...     "chorus1": [("F", 2), ("G", 2), ("Am", 2), ("C", 2)],
        ... }
        >>> bass_lines = generate_bass_for_arrangement(sections, chords, genre="pop")
    """
    bass_lines = {}

    for section in sections:
        name = section.get("name", "section")
        section_type = section.get("type", "verse")
        energy = section.get("energy", 0.5)

        chords = chords_per_section.get(name, [("C", section.get("bars", 8))])

        bass_lines[name] = generate_bass_line(
            chords=chords,
            genre=genre,
            key=key,
            section_type=section_type,
            energy=energy,
        )

    return bass_lines
