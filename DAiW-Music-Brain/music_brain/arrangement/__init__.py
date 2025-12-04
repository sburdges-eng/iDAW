"""
Arrangement module for iDAW Music Brain.

Provides complete song arrangement generation including:
- Section templates (verse, chorus, bridge, etc.)
- Bass line generation
- Energy arc modeling
- Instrumentation planning
- Multi-track MIDI generation
"""

from .templates import (
    SectionType,
    SectionTemplate,
    ArrangementTemplate,
    create_intro,
    create_verse,
    create_chorus,
    create_bridge,
    create_outro,
    create_breakdown,
    create_buildup,
    get_genre_template,
    GENRE_TEMPLATES,
)

from .bass_generator import (
    BassNote,
    BassPattern,
    BassLine,
    generate_bass_line,
    generate_bass_pattern,
)

from .energy_arc import (
    EnergyPoint,
    EnergyArc,
    ArcType,
    EmotionalJourney,
    generate_energy_arc,
    apply_energy_to_sections,
    suggest_arc_for_intent,
)

from .generator import (
    ArrangementGenerator,
    GeneratedArrangement,
    generate_arrangement,
    generate_complete_song,
)

__all__ = [
    # Templates
    "SectionType",
    "SectionTemplate",
    "ArrangementTemplate",
    "create_intro",
    "create_verse",
    "create_chorus",
    "create_bridge",
    "create_outro",
    "create_breakdown",
    "create_buildup",
    "get_genre_template",
    "GENRE_TEMPLATES",
    # Bass
    "BassNote",
    "BassPattern",
    "BassLine",
    "generate_bass_line",
    "generate_bass_pattern",
    # Energy
    "EnergyPoint",
    "EnergyArc",
    "ArcType",
    "EmotionalJourney",
    "generate_energy_arc",
    "apply_energy_to_sections",
    "suggest_arc_for_intent",
    # Generator
    "ArrangementGenerator",
    "GeneratedArrangement",
    "generate_arrangement",
    "generate_complete_song",
]
