"""
iDAWi Music Brain
Minimal Python interface for emotion-driven music production

This is a lightweight version of the DAiW-Music-Brain package,
extracted for use in the iDAWi standalone application.
"""

__version__ = "0.1.0"
__author__ = "Sean Burdges"

from pathlib import Path

# Package root directory
PACKAGE_ROOT = Path(__file__).parent

# Re-export main functions from bridge for direct import
import sys
sys.path.insert(0, str(PACKAGE_ROOT.parent))

try:
    from bridge import (
        suggest_rule_break,
        process_intent,
        get_emotions,
        RULE_BREAKING_EFFECTS,
        EMOTION_RULE_MAPPING,
        EMOTIONS_DATABASE,
    )
except ImportError:
    # Fallback if bridge not available
    def suggest_rule_break(emotion: str):
        return []

    def process_intent(intent_data: dict):
        return {"harmony": ["I", "IV", "V", "I"], "tempo": 120, "key": "C major", "mixer_params": {}}

    def get_emotions():
        return []

    RULE_BREAKING_EFFECTS = {}
    EMOTION_RULE_MAPPING = {}
    EMOTIONS_DATABASE = []

__all__ = [
    "suggest_rule_break",
    "process_intent",
    "get_emotions",
    "RULE_BREAKING_EFFECTS",
    "EMOTION_RULE_MAPPING",
    "EMOTIONS_DATABASE",
]
