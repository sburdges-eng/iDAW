"""
Music Brain - Intelligent Music Analysis Toolkit

A Python package for music production analysis:
- Groove extraction and application
- Chord progression analysis
- Section detection
- Feel/timing analysis
- Arrangement generation
- Bass line generation
- Energy arc modeling
- DAW integration
"""

__version__ = "0.3.0"
__author__ = "Sean Burdges"

from music_brain.groove import extract_groove, apply_groove, GrooveTemplate
from music_brain.structure import analyze_chords, detect_sections, ChordProgression
from music_brain.audio import analyze_feel, AudioFeatures
from music_brain.arrangement import (
    generate_arrangement,
    generate_complete_song,
    ArrangementGenerator,
    GeneratedArrangement,
    SectionType,
    get_genre_template,
    generate_bass_line,
    BassLine,
    BassPattern,
    generate_energy_arc,
    EnergyArc,
    ArcType,
    EmotionalJourney,
)

__all__ = [
    # Groove
    "extract_groove",
    "apply_groove",
    "GrooveTemplate",
    # Structure
    "analyze_chords",
    "detect_sections",
    "ChordProgression",
    # Audio
    "analyze_feel",
    "AudioFeatures",
    # Arrangement
    "generate_arrangement",
    "generate_complete_song",
    "ArrangementGenerator",
    "GeneratedArrangement",
    "SectionType",
    "get_genre_template",
    # Bass
    "generate_bass_line",
    "BassLine",
    "BassPattern",
    # Energy
    "generate_energy_arc",
    "EnergyArc",
    "ArcType",
    "EmotionalJourney",
]
