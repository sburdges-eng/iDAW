"""
Voice Processing - Auto-tune, modulation, and voice synthesis.

This module provides voice processing capabilities including:
- AutoTuneProcessor: Pitch correction for vocals
- VoiceModulator: Voice character modification
- VoiceSynthesizer: Text-to-speech and guide vocal generation
"""

from music_brain.voice.auto_tune import (
    AutoTuneProcessor,
    AutoTuneSettings,
    get_auto_tune_preset,
)
from music_brain.voice.modulator import (
    VoiceModulator,
    ModulationSettings,
    get_modulation_preset,
)
from music_brain.voice.synthesizer import (
    VoiceSynthesizer,
    SynthConfig,
    get_voice_profile,
)

__all__ = [
    # Auto-tune
    "AutoTuneProcessor",
    "AutoTuneSettings",
    "get_auto_tune_preset",
    # Modulation
    "VoiceModulator",
    "ModulationSettings",
    "get_modulation_preset",
    # Synthesis
    "VoiceSynthesizer",
    "SynthConfig",
    "get_voice_profile",
]
