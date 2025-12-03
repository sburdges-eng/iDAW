"""
Voice Processing - Text-to-speech synthesis and voice modulation.

Features:
- Local TTS voice synthesis using pyttsx3
- Guide vocal generation from lyrics and melody
- Voice profile presets for different emotional tones
- Cross-platform support (macOS, Windows, Linux)
"""

from music_brain.voice.synth import (
    VoiceSynthesizer,
    SynthConfig,
    get_voice_profile,
    VoiceProfile,
    LocalVoiceSynth,
)

__all__ = [
    "VoiceSynthesizer",
    "SynthConfig",
    "get_voice_profile",
    "VoiceProfile",
    "LocalVoiceSynth",
]
