"""
Desktop application module for iDAW Music Brain.

Provides a Streamlit-based GUI for:
- Intent-driven song creation
- Arrangement visualization
- Project management
- MIDI export
"""

from .project import (
    Project,
    ProjectManager,
    ProjectIntent,
    create_project,
    load_project,
    save_project,
)

from .timeline import (
    TimelineRenderer,
    render_arrangement_timeline,
    render_energy_curve,
    SECTION_COLORS,
)

# MIDI export (optional - requires mido)
try:
    from .midi_export import (
        MIDIExporter,
        MIDIExportConfig,
        export_arrangement_to_midi,
        export_chords_to_midi,
    )
    MIDI_EXPORT_AVAILABLE = True
except ImportError:
    MIDI_EXPORT_AVAILABLE = False

__all__ = [
    # Project
    "Project",
    "ProjectManager",
    "ProjectIntent",
    "create_project",
    "load_project",
    "save_project",
    # Timeline
    "TimelineRenderer",
    "render_arrangement_timeline",
    "render_energy_curve",
    "SECTION_COLORS",
    # MIDI (conditional)
    "MIDI_EXPORT_AVAILABLE",
]

if MIDI_EXPORT_AVAILABLE:
    __all__.extend([
        "MIDIExporter",
        "MIDIExportConfig",
        "export_arrangement_to_midi",
        "export_chords_to_midi",
    ])
