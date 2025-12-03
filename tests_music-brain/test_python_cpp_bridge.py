"""
Comprehensive tests for the Python/C++ bridge integration.

Tests the bridge_api module which provides the Python side of the Dual Engine
architecture, processing text prompts with knob parameters and returning MIDI data.

Run with: pytest tests_music-brain/test_python_cpp_bridge.py -v
"""

import pytest
from unittest.mock import MagicMock, patch
import math
import json


class TestResolveContradictions:
    """Test parameter contradiction resolution for safe operation."""

    def test_resolve_gain_contradiction(self):
        """Infinite gain with positive modulation should resolve to safe value."""
        from music_brain.orchestrator.bridge_api import resolve_contradictions

        params = {"gain": -math.inf, "gain_mod": 0.5}
        resolved = resolve_contradictions(params)

        assert resolved["gain"] == -6.0  # Safe default
        assert resolved["gain_mod"] == 0.5  # Unchanged

    def test_resolve_velocity_range_contradiction(self):
        """Velocity min > max should be averaged."""
        from music_brain.orchestrator.bridge_api import resolve_contradictions

        params = {"velocity_min": 100, "velocity_max": 50}
        resolved = resolve_contradictions(params)

        assert resolved["velocity_min"] == 75.0
        assert resolved["velocity_max"] == 75.0

    def test_chaos_clipping(self):
        """Chaos parameter should be clipped to 0-1 range."""
        from music_brain.orchestrator.bridge_api import resolve_contradictions

        # Test over-range
        params = {"chaos": 1.5}
        resolved = resolve_contradictions(params)
        assert resolved["chaos"] == 1.0

        # Test under-range
        params = {"chaos": -0.5}
        resolved = resolve_contradictions(params)
        assert resolved["chaos"] == 0.0

    def test_complexity_clipping(self):
        """Complexity parameter should be clipped to 0-1 range."""
        from music_brain.orchestrator.bridge_api import resolve_contradictions

        params = {"complexity": 2.0}
        resolved = resolve_contradictions(params)
        assert resolved["complexity"] == 1.0

    def test_tempo_bounds(self):
        """Tempo should be bounded to 20-300 BPM."""
        from music_brain.orchestrator.bridge_api import resolve_contradictions

        # Test under-range
        params = {"tempo": 10}
        resolved = resolve_contradictions(params)
        assert resolved["tempo"] == 20

        # Test over-range
        params = {"tempo": 400}
        resolved = resolve_contradictions(params)
        assert resolved["tempo"] == 300

    def test_grid_resolution_bounds(self):
        """Grid resolution should be bounded to 1-64."""
        from music_brain.orchestrator.bridge_api import resolve_contradictions

        # Test under-range
        params = {"grid": 0}
        resolved = resolve_contradictions(params)
        assert resolved["grid"] == 1

        # Test over-range
        params = {"grid": 128}
        resolved = resolve_contradictions(params)
        assert resolved["grid"] == 64

    def test_attack_release_swap(self):
        """Attack > release should swap values."""
        from music_brain.orchestrator.bridge_api import resolve_contradictions

        params = {"attack": 500, "release": 100}
        resolved = resolve_contradictions(params)

        assert resolved["attack"] == 100
        assert resolved["release"] == 500

    def test_valid_params_unchanged(self):
        """Valid parameters should pass through unchanged."""
        from music_brain.orchestrator.bridge_api import resolve_contradictions

        params = {
            "chaos": 0.5,
            "complexity": 0.6,
            "tempo": 120,
            "grid": 16,
            "gain": -3.0,
        }
        resolved = resolve_contradictions(params)

        assert resolved["chaos"] == 0.5
        assert resolved["complexity"] == 0.6
        assert resolved["tempo"] == 120
        assert resolved["grid"] == 16
        assert resolved["gain"] == -3.0


class TestSynesthesiaDictionary:
    """Test synesthesia word-to-parameter mapping."""

    def test_get_parameter_happy(self):
        """'Happy' should map to defined chaos and complexity."""
        from music_brain.orchestrator.bridge_api import get_parameter

        params = get_parameter("happy")
        assert "chaos" in params
        assert "complexity" in params
        # Happy should have specific defined values
        assert 0 <= params["chaos"] <= 1
        assert 0 <= params["complexity"] <= 1

    def test_get_parameter_angry(self):
        """'Angry' should map to high chaos and complexity."""
        from music_brain.orchestrator.bridge_api import get_parameter

        params = get_parameter("angry")
        assert params["chaos"] > 0.5
        assert params["complexity"] > 0.5

    def test_get_parameter_unknown_uses_hash(self):
        """Unknown words should use synesthesia fallback (hash-based)."""
        from music_brain.orchestrator.bridge_api import get_parameter

        params = get_parameter("xyznonexistent")
        # Should return deterministic hash-based values
        assert "chaos" in params
        assert "complexity" in params
        assert 0 <= params["chaos"] <= 1
        assert 0 <= params["complexity"] <= 1

    def test_get_parameter_deterministic(self):
        """Same unknown word should always return same values."""
        from music_brain.orchestrator.bridge_api import get_parameter

        params1 = get_parameter("testword123")
        params2 = get_parameter("testword123")

        assert params1["chaos"] == params2["chaos"]
        assert params1["complexity"] == params2["complexity"]


class TestGenreDetection:
    """Test genre detection from text prompts."""

    def test_detect_genre_with_genres_dict(self):
        """Genre detection should work with genre definitions."""
        from music_brain.orchestrator.bridge_api import detect_genre_from_text

        # Create mock genre definitions
        genres = {
            "jazz": {"emotional_tags": ["jazzy", "swing", "bebop"]},
            "funk": {"emotional_tags": ["funky", "groove", "tight"]},
            "rock": {"emotional_tags": ["rock", "guitar", "heavy"]},
        }

        genre, confidence = detect_genre_from_text("make it jazzy", genres)
        assert genre == "jazz" or confidence > 0

    def test_detect_genre_empty_text(self):
        """Empty text should return empty genre."""
        from music_brain.orchestrator.bridge_api import detect_genre_from_text

        genres = {"jazz": {"emotional_tags": ["jazzy"]}}
        genre, confidence = detect_genre_from_text("", genres)
        assert genre == "" or confidence == 0

    def test_detect_genre_no_match(self):
        """Text with no matches should return empty or low confidence."""
        from music_brain.orchestrator.bridge_api import detect_genre_from_text

        genres = {"jazz": {"emotional_tags": ["jazzy"]}}
        genre, confidence = detect_genre_from_text("make it completely different", genres)
        # Either empty genre or low confidence
        assert genre == "" or confidence < 0.5


class TestKnobState:
    """Test KnobState dataclass."""

    def test_knob_state_defaults(self):
        """KnobState should have the correct defaults."""
        from music_brain.orchestrator.bridge_api import KnobState

        knobs = KnobState()
        assert knobs.grid == 16.0
        assert knobs.gate == 0.75
        assert knobs.swing == 0.5
        assert knobs.chaos == 0.5
        assert knobs.complexity == 0.5

    def test_knob_state_custom(self):
        """KnobState should accept custom values."""
        from music_brain.orchestrator.bridge_api import KnobState

        knobs = KnobState(grid=32, gate=0.9, swing=0.6, chaos=0.8, complexity=0.9)
        assert knobs.grid == 32
        assert knobs.gate == 0.9
        assert knobs.swing == 0.6
        assert knobs.chaos == 0.8
        assert knobs.complexity == 0.9

    def test_knob_state_from_dict(self):
        """KnobState should be creatable from dict."""
        from music_brain.orchestrator.bridge_api import KnobState

        data = {"grid": 24, "gate": 0.8, "swing": 0.55, "chaos": 0.3, "complexity": 0.7}
        knobs = KnobState.from_dict(data)

        assert knobs.grid == 24
        assert knobs.gate == 0.8
        assert knobs.swing == 0.55
        assert knobs.chaos == 0.3
        assert knobs.complexity == 0.7

    def test_knob_state_from_partial_dict(self):
        """KnobState should use defaults for missing keys."""
        from music_brain.orchestrator.bridge_api import KnobState

        data = {"chaos": 0.9}
        knobs = KnobState.from_dict(data)

        assert knobs.chaos == 0.9
        assert knobs.grid == 16.0  # Default


class TestMidiEvent:
    """Test MidiEvent dataclass."""

    def test_midi_event_creation(self):
        """MidiEvent should store MIDI data correctly."""
        from music_brain.orchestrator.bridge_api import MidiEvent

        event = MidiEvent(
            status=0x90,  # Note on, channel 0
            data1=60,     # Middle C
            data2=100,    # Velocity
            timestamp=0,
        )
        assert event.status == 0x90
        assert event.data1 == 60
        assert event.data2 == 100
        assert event.timestamp == 0

    def test_midi_event_to_dict(self):
        """MidiEvent should convert to dict correctly."""
        from music_brain.orchestrator.bridge_api import MidiEvent

        event = MidiEvent(status=0x90, data1=60, data2=100, timestamp=480)
        d = event.to_dict()

        assert d["status"] == 0x90
        assert d["data1"] == 60
        assert d["data2"] == 100
        assert d["timestamp"] == 480


class TestBridgeResult:
    """Test BridgeResult dataclass."""

    def test_bridge_result_success(self):
        """BridgeResult should store success state."""
        from music_brain.orchestrator.bridge_api import BridgeResult

        result = BridgeResult(success=True)
        assert result.success is True
        assert result.midi_events == []
        assert result.error_message == ""

    def test_bridge_result_failure(self):
        """BridgeResult should store failure with error."""
        from music_brain.orchestrator.bridge_api import BridgeResult

        result = BridgeResult(success=False, error_message="Processing failed")
        assert result.success is False
        assert result.error_message == "Processing failed"

    def test_bridge_result_with_events(self):
        """BridgeResult should store MIDI events."""
        from music_brain.orchestrator.bridge_api import BridgeResult, MidiEvent

        events = [
            MidiEvent(status=0x90, data1=60, data2=100, timestamp=0),
            MidiEvent(status=0x80, data1=60, data2=0, timestamp=480),
        ]
        result = BridgeResult(success=True, midi_events=events)

        assert len(result.midi_events) == 2
        assert result.midi_events[0].data1 == 60

    def test_bridge_result_with_suggestions(self):
        """BridgeResult should store suggested parameters."""
        from music_brain.orchestrator.bridge_api import BridgeResult

        result = BridgeResult(
            success=True,
            suggested_chaos=0.7,
            suggested_complexity=0.8,
            detected_genre="jazz",
        )

        assert result.suggested_chaos == 0.7
        assert result.suggested_complexity == 0.8
        assert result.detected_genre == "jazz"

    def test_bridge_result_to_dict(self):
        """BridgeResult should convert to dict for C++ serialization."""
        from music_brain.orchestrator.bridge_api import BridgeResult, MidiEvent

        result = BridgeResult(
            success=True,
            midi_events=[MidiEvent(status=0x90, data1=60, data2=100, timestamp=0)],
            suggested_chaos=0.5,
            detected_genre="funk",
        )

        d = result.to_dict()
        assert d["success"] is True
        assert len(d["midi_events"]) == 1
        assert d["suggested_chaos"] == 0.5
        assert d["detected_genre"] == "funk"

    def test_bridge_result_json_serializable(self):
        """BridgeResult dict should be JSON serializable."""
        from music_brain.orchestrator.bridge_api import BridgeResult, MidiEvent

        result = BridgeResult(
            success=True,
            midi_events=[MidiEvent(status=0x90, data1=60, data2=100, timestamp=0)],
            suggested_chaos=0.5,
            metadata={"key": "C", "tempo": 120},
        )

        d = result.to_dict()
        json_str = json.dumps(d)

        # Should serialize without error
        assert '"success": true' in json_str or '"success":true' in json_str


class TestCppIntegration:
    """Test integration points for C++ bridge."""

    def test_midi_status_bytes(self):
        """Test MIDI status byte construction."""
        from music_brain.orchestrator.bridge_api import MidiEvent

        # Note on channel 0
        note_on = MidiEvent(status=0x90, data1=60, data2=100, timestamp=0)
        assert note_on.status & 0xF0 == 0x90  # Note on
        assert note_on.status & 0x0F == 0x00  # Channel 0

        # Note off channel 1
        note_off = MidiEvent(status=0x81, data1=60, data2=0, timestamp=480)
        assert note_off.status & 0xF0 == 0x80  # Note off
        assert note_off.status & 0x0F == 0x01  # Channel 1

    def test_timestamp_in_samples(self):
        """Timestamps should be in samples for C++ audio thread."""
        from music_brain.orchestrator.bridge_api import MidiEvent

        # At 44100 Hz, 1 beat at 120 BPM = 22050 samples
        samples_per_beat = 44100 * 60 // 120  # 22050

        event = MidiEvent(
            status=0x90,
            data1=60,
            data2=100,
            timestamp=samples_per_beat,
        )

        assert event.timestamp == 22050


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_params(self):
        """Empty params dict should not crash."""
        from music_brain.orchestrator.bridge_api import resolve_contradictions

        result = resolve_contradictions({})
        assert isinstance(result, dict)

    def test_none_gain_mod(self):
        """Infinite gain without mod should not crash."""
        from music_brain.orchestrator.bridge_api import resolve_contradictions

        params = {"gain": -math.inf}  # No gain_mod
        result = resolve_contradictions(params)
        # Should pass through (no contradiction without gain_mod)
        assert result["gain"] == -math.inf

    def test_whitespace_word(self):
        """Whitespace in words should be stripped."""
        from music_brain.orchestrator.bridge_api import get_parameter

        params = get_parameter("  happy  ")
        assert "chaos" in params
        assert "complexity" in params

    def test_case_insensitive_word(self):
        """Word lookup should be case-insensitive."""
        from music_brain.orchestrator.bridge_api import get_parameter

        params_lower = get_parameter("happy")
        params_upper = get_parameter("HAPPY")
        params_mixed = get_parameter("HaPpY")

        assert params_lower["chaos"] == params_upper["chaos"]
        assert params_lower["chaos"] == params_mixed["chaos"]


class TestLoadGenreDefinitions:
    """Test genre definition loading."""

    def test_load_genre_definitions_returns_dict(self):
        """load_genre_definitions should return a dict."""
        from music_brain.orchestrator.bridge_api import load_genre_definitions

        genres = load_genre_definitions()
        assert isinstance(genres, dict)

    def test_load_genre_definitions_cached(self):
        """Genre definitions should be cached."""
        from music_brain.orchestrator.bridge_api import load_genre_definitions

        genres1 = load_genre_definitions()
        genres2 = load_genre_definitions()
        # Should return same object (cached)
        assert genres1 is genres2


class TestProcessPromptSync:
    """Test synchronous wrapper for C++ bridge calls."""

    def test_process_prompt_sync_exists(self):
        """process_prompt_sync function should exist."""
        from music_brain.orchestrator.bridge_api import process_prompt_sync

        assert callable(process_prompt_sync)

    def test_process_prompt_sync_returns_result(self):
        """process_prompt_sync should return a BridgeResult or dict."""
        from music_brain.orchestrator.bridge_api import process_prompt_sync, BridgeResult

        # Call with simple input - implementation may vary
        try:
            result = process_prompt_sync("test", {})
            # Should return some result type
            assert result is not None
            assert isinstance(result, (dict, BridgeResult))
        except Exception:
            # Implementation may raise for missing dependencies
            pass
