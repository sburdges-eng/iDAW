"""
Shared pytest fixtures and configuration for iDAW Music Brain tests.

Provides mock objects, sample data, and common test utilities.
"""

import pytest
from unittest.mock import MagicMock, patch
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


# ==============================================================================
# MIDI and Music Fixtures
# ==============================================================================

@pytest.fixture
def sample_chord_symbols() -> List[str]:
    """Common chord progression for testing."""
    return ["Cm", "Fm", "Gm", "Cm"]


@pytest.fixture
def sample_major_chords() -> List[str]:
    """Major key chord progression."""
    return ["G", "C", "D", "G"]


@pytest.fixture
def sample_midi_notes() -> List[tuple]:
    """Sample MIDI note data as (pitch, velocity) tuples."""
    return [
        (60, 100),  # C4
        (64, 90),   # E4
        (67, 85),   # G4
        (72, 95),   # C5
    ]


@pytest.fixture
def sample_groove_data() -> Dict[str, Any]:
    """Sample groove analysis result."""
    return {
        "tempo": 120.0,
        "tempo_confidence": 0.95,
        "time_signature": "4/4",
        "swing": 0.0,
        "onset_count": 16,
    }


# ==============================================================================
# Mock Fixtures for Bridge Integration
# ==============================================================================

@pytest.fixture
def mock_logic_project():
    """Mock LogicProject for DAW integration tests."""
    with patch("music_brain.daw.logic.LogicProject") as MockProject:
        instance = MockProject.return_value
        instance.ppq = 480
        instance.tempo_bpm = 120
        instance.export_midi.return_value = "output.mid"
        instance.add_track = MagicMock()
        yield MockProject


@pytest.fixture
def mock_progression_parser():
    """Mock progression parser for chord analysis tests."""
    with patch("music_brain.structure.progression.parse_progression_string") as mock:
        # Create mock chord objects
        mock_chord = MagicMock()
        mock_chord.root_num = 0  # C
        mock_chord.quality = "min"
        mock.return_value = [mock_chord] * 4
        yield mock


@pytest.fixture
def mock_mido_available():
    """Mock MIDO availability flag."""
    with patch("music_brain.structure.comprehensive_engine.MIDO_AVAILABLE", True):
        yield


# ==============================================================================
# Harmony Plan Fixtures
# ==============================================================================

@pytest.fixture
def harmony_plan_minor(sample_chord_symbols):
    """HarmonyPlan fixture for minor key testing."""
    from music_brain.structure.comprehensive_engine import HarmonyPlan
    return HarmonyPlan(
        root_note="C",
        mode="minor",
        tempo_bpm=120,
        time_signature="4/4",
        length_bars=4,
        chord_symbols=sample_chord_symbols,
        harmonic_rhythm="1_chord_per_bar",
        mood_profile="grief",
        complexity=0.5,
        vulnerability=0.5,
    )


@pytest.fixture
def harmony_plan_major(sample_major_chords):
    """HarmonyPlan fixture for major key testing."""
    from music_brain.structure.comprehensive_engine import HarmonyPlan
    return HarmonyPlan(
        root_note="G",
        mode="ionian",
        tempo_bpm=100,
        time_signature="4/4",
        length_bars=8,
        chord_symbols=sample_major_chords,
        mood_profile="tenderness",
        complexity=0.3,
        vulnerability=0.7,
    )


# ==============================================================================
# Therapy Session Fixtures
# ==============================================================================

@pytest.fixture
def therapy_session():
    """Fresh TherapySession for testing."""
    from music_brain.structure.comprehensive_engine import TherapySession
    return TherapySession()


@pytest.fixture
def therapy_session_grief():
    """TherapySession pre-configured with grief context."""
    from music_brain.structure.comprehensive_engine import TherapySession
    session = TherapySession()
    session.process_core_input("I miss my grandmother who passed away")
    session.set_scales(motivation=7, chaos=0.3)
    return session


@pytest.fixture
def therapy_session_rage():
    """TherapySession pre-configured with rage context."""
    from music_brain.structure.comprehensive_engine import TherapySession
    session = TherapySession()
    session.process_core_input("I am furious and want revenge")
    session.set_scales(motivation=9, chaos=0.8)
    return session


# ==============================================================================
# Bridge and Integration Fixtures
# ==============================================================================

@pytest.fixture
def mock_penta_core_native():
    """Mock the native C++ penta_core module."""
    mock_native = MagicMock()

    # Mock harmony submodule
    mock_native.harmony.HarmonyConfig.return_value = MagicMock()
    mock_native.harmony.HarmonyEngine.return_value = MagicMock()
    mock_native.harmony.Note = MagicMock
    mock_native.harmony.Chord = MagicMock

    # Mock groove submodule
    mock_native.groove.GrooveConfig.return_value = MagicMock()
    mock_native.groove.GrooveEngine.return_value = MagicMock()

    # Mock diagnostics submodule
    mock_native.diagnostics.DiagnosticsConfig.return_value = MagicMock()
    mock_native.diagnostics.DiagnosticsEngine.return_value = MagicMock()

    # Mock OSC submodule
    mock_native.osc.OSCConfig.return_value = MagicMock()
    mock_native.osc.OSCHub.return_value = MagicMock()
    mock_native.osc.create_osc_message.return_value = MagicMock()

    with patch.dict("sys.modules", {"penta_core_native": mock_native}):
        yield mock_native


@pytest.fixture
def mock_bridge_api():
    """Mock the bridge API for integration tests."""
    with patch("music_brain.orchestrator.bridge_api") as mock:
        mock.process_prompt_sync.return_value = MagicMock(
            midi_events=[],
            ghost_hands_suggestions={},
        )
        yield mock


# ==============================================================================
# Knob State Fixtures (for Bridge API)
# ==============================================================================

@pytest.fixture
def default_knob_state():
    """Default knob state for bridge tests."""
    return {
        "grid": 16,
        "gate": 0.8,
        "swing": 0.0,
        "chaos": 0.1,
        "complexity": 0.5,
    }


@pytest.fixture
def aggressive_knob_state():
    """Aggressive/chaotic knob state."""
    return {
        "grid": 32,
        "gate": 0.5,
        "swing": 0.2,
        "chaos": 0.8,
        "complexity": 0.9,
    }


# ==============================================================================
# Intent Schema Fixtures
# ==============================================================================

@pytest.fixture
def sample_intent_phase0():
    """Phase 0 (Core Wound/Desire) intent data."""
    return {
        "core_event": "loss of connection",
        "core_resistance": "fear of vulnerability",
        "core_longing": "to be understood",
    }


@pytest.fixture
def sample_intent_phase1():
    """Phase 1 (Emotional Intent) intent data."""
    return {
        "mood_primary": "grief",
        "vulnerability_scale": 0.7,
        "narrative_arc": "descent_to_acceptance",
    }


@pytest.fixture
def sample_intent_phase2():
    """Phase 2 (Technical Constraints) intent data."""
    return {
        "technical_genre": "ambient",
        "technical_key": "C minor",
        "technical_rule_to_break": "HARMONY_AvoidTonicResolution",
    }


# ==============================================================================
# Pytest Markers Configuration
# ==============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "bridge: marks tests that test Python/C++ bridge"
    )
    config.addinivalue_line(
        "markers", "requires_audio: marks tests that require audio dependencies"
    )
    config.addinivalue_line(
        "markers", "requires_theory: marks tests that require music21"
    )


# ==============================================================================
# Skip Markers for Optional Dependencies
# ==============================================================================

@pytest.fixture(scope="session")
def has_librosa():
    """Check if librosa is available."""
    try:
        import librosa
        return True
    except ImportError:
        return False


@pytest.fixture(scope="session")
def has_music21():
    """Check if music21 is available."""
    try:
        import music21
        return True
    except ImportError:
        return False


@pytest.fixture(scope="session")
def has_mido():
    """Check if mido is available."""
    try:
        import mido
        return True
    except ImportError:
        return False


# Conditional skip decorators - use lazy checking
def _has_module(name: str) -> bool:
    """Check if a module is importable."""
    try:
        __import__(name)
        return True
    except ImportError:
        return False


requires_librosa = pytest.mark.skipif(
    not _has_module("librosa"),
    reason="librosa not installed"
)

requires_music21 = pytest.mark.skipif(
    not _has_module("music21"),
    reason="music21 not installed"
)


# ==============================================================================
# Audio Data Fixtures
# ==============================================================================

@pytest.fixture
def sample_audio_buffer():
    """Generate sample audio buffer for testing."""
    import numpy as np
    # Generate 1 second of 440Hz sine wave at 48kHz
    sample_rate = 48000
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return np.sin(2 * np.pi * 440 * t).astype(np.float32)


@pytest.fixture
def sample_stereo_audio():
    """Generate stereo audio buffer."""
    import numpy as np
    sample_rate = 48000
    duration = 0.5
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples, endpoint=False)
    left = np.sin(2 * np.pi * 440 * t)
    right = np.sin(2 * np.pi * 554.37 * t)  # C#5
    return np.stack([left, right], axis=1).astype(np.float32)


# ==============================================================================
# Cleanup and Session Management
# ==============================================================================

@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset any singleton instances between tests."""
    yield
    # Clean up after test
    pass
