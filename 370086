# app.py
"""
DAiW - Digital Audio intimate Workstation
Cutting-edge Streamlit UI with unique EMIDI features.

"The tool shouldn't finish art for people. It should make them braver."
"""
import os
import tempfile
import json
import math
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

import streamlit as st

# Core imports
from music_brain.structure.comprehensive_engine import (
    TherapySession,
    render_plan_to_midi,
)
from music_brain.harmony import HarmonyGenerator, HarmonyResult, generate_midi_from_harmony
from music_brain.session.intent_schema import (
    CompleteSongIntent,
    SongRoot,
    SongIntent,
    TechnicalConstraints,
    SystemDirective,
    suggest_rule_break,
    list_all_rules,
    validate_intent,
)
from music_brain.session.intent_processor import process_intent
from music_brain.structure import analyze_chords, detect_sections
from music_brain.groove import extract_groove, apply_groove
from music_brain.text.lyrical_mirror import generate_lyrical_fragments

# Guitar Effects Engine
try:
    from music_brain.effects import (
        GuitarFXEngine,
        EffectChain,
        EffectPreset,
        ModulationMatrix,
        ALL_EFFECTS,
        EFFECT_CATEGORIES,
        create_preset_from_emotion,
        get_effect_suggestions,
    )
    EFFECTS_AVAILABLE = True
except ImportError:
    EFFECTS_AVAILABLE = False


# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================

EMOTION_COLORS = {
    "grief": "#4a5568",
    "rage": "#e53e3e",
    "fear": "#9f7aea",
    "nostalgia": "#ed8936",
    "defiance": "#f56565",
    "tenderness": "#ed64a6",
    "dissociation": "#a0aec0",
    "awe": "#4fd1c5",
    "confusion": "#667eea",
    "hope": "#48bb78",
    "longing": "#9f7aea",
    "neutral": "#718096",
}

MODE_COLORS = {
    "ionian": "#48bb78",
    "dorian": "#ed8936",
    "phrygian": "#e53e3e",
    "lydian": "#4fd1c5",
    "mixolydian": "#f6ad55",
    "aeolian": "#4a5568",
    "locrian": "#9f7aea",
}

# =============================================================================
# CUSTOM CSS - CUTTING EDGE DESIGN
# =============================================================================

def inject_custom_css():
    """Inject custom CSS for cutting-edge design."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* =================================================================
       ROOT THEME - DARK MIDNIGHT WITH AURORA ACCENTS
       ================================================================= */
    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --bg-tertiary: #1a1a25;
        --bg-card: rgba(26, 26, 37, 0.7);
        --bg-glass: rgba(255, 255, 255, 0.03);
        --border-subtle: rgba(255, 255, 255, 0.06);
        --border-glow: rgba(99, 102, 241, 0.3);
        --text-primary: #f4f4f5;
        --text-secondary: #a1a1aa;
        --text-muted: #71717a;
        --accent-aurora: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        --accent-ember: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #f093fb 100%);
        --accent-ocean: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --accent-forest: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        --glow-purple: 0 0 40px rgba(102, 126, 234, 0.15);
        --glow-pink: 0 0 40px rgba(240, 147, 251, 0.15);
    }
    
    /* =================================================================
       GLOBAL STYLES
       ================================================================= */
    .stApp {
        background: var(--bg-primary);
        background-image: 
            radial-gradient(ellipse at 0% 0%, rgba(102, 126, 234, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 100% 100%, rgba(240, 147, 251, 0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(79, 172, 254, 0.03) 0%, transparent 70%);
        font-family: 'Space Grotesk', -apple-system, sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* =================================================================
       TYPOGRAPHY
       ================================================================= */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
        color: var(--text-primary) !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        background: var(--accent-aurora);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    p, span, div, label {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-secondary);
    }
    
    code, .stCode {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    /* =================================================================
       SIDEBAR - GLASSMORPHIC
       ================================================================= */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(18, 18, 26, 0.95) 0%, rgba(10, 10, 15, 0.98) 100%) !important;
        border-right: 1px solid var(--border-subtle);
        backdrop-filter: blur(20px);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: var(--text-primary) !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--text-secondary);
    }
    
    /* Sidebar nav items */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.25rem;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 0.75rem 1rem !important;
        margin: 0.25rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateX(4px);
    }
    
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: var(--glow-purple);
    }
    
    /* =================================================================
       CARDS & CONTAINERS
       ================================================================= */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-subtle);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: var(--glow-purple);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: var(--border-glow);
        box-shadow: 0 0 60px rgba(102, 126, 234, 0.2);
    }
    
    .feature-card {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 1.25rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--accent-aurora);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(102, 126, 234, 0.4);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), var(--glow-purple);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    /* =================================================================
       BUTTONS - AURORA STYLE
       ================================================================= */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background: var(--bg-glass) !important;
        border: 1px solid var(--border-subtle) !important;
        color: var(--text-primary) !important;
        box-shadow: none !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(102, 126, 234, 0.1) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
    }
    
    /* =================================================================
       INPUTS - MINIMAL DARK
       ================================================================= */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(102, 126, 234, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: var(--accent-aurora) !important;
    }
    
    .stSlider > div > div > div > div > div {
        background: white !important;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* =================================================================
       TABS - MODERN PILLS
       ================================================================= */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-tertiary);
        border-radius: 16px;
        padding: 0.5rem;
        gap: 0.5rem;
        border: 1px solid var(--border-subtle);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 12px !important;
        color: var(--text-secondary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
        padding: 0.75rem 1.25rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--bg-glass) !important;
        color: var(--text-primary) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
        color: var(--text-primary) !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    
    /* =================================================================
       METRICS - GLOWING
       ================================================================= */
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.75rem !important;
        background: var(--accent-aurora);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--text-muted) !important;
        font-weight: 500;
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.1em;
    }
    
    /* =================================================================
       EXPANDERS - SLEEK
       ================================================================= */
    .streamlit-expanderHeader {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderContent {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* =================================================================
       PROGRESS BARS - GRADIENT
       ================================================================= */
    .stProgress > div > div > div > div {
        background: var(--accent-aurora) !important;
        border-radius: 10px !important;
    }
    
    /* =================================================================
       ALERTS & INFO BOXES
       ================================================================= */
    .stAlert {
        background: var(--bg-card) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stAlertContainer"] > div {
        border-radius: 12px !important;
    }
    
    /* =================================================================
       CUSTOM COMPONENTS
       ================================================================= */
    .emotion-orb {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        animation: pulse 3s ease-in-out infinite;
        box-shadow: 0 0 60px currentColor;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px currentColor; }
        50% { box-shadow: 0 0 40px currentColor; }
    }
    
    .stat-box {
        background: var(--bg-tertiary);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        border-color: var(--border-glow);
        transform: translateY(-2px);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        background: var(--accent-aurora);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .stat-label {
        color: var(--text-muted);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.25rem;
    }
    
    .mode-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .chord-pill {
        display: inline-block;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        margin: 0.25rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .chord-pill:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
        transform: scale(1.05);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        line-height: 1.1;
        background: var(--accent-aurora);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-subtle), transparent);
        margin: 2rem 0;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-subtle);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(102, 126, 234, 0.5);
    }
    
    /* =================================================================
       ANIMATIONS FOR EMIDI
       ================================================================= */
    .emotion-wheel {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
    }
    
    .emotion-tag {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        background: var(--bg-glass);
        border: 1px solid var(--border-subtle);
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .emotion-tag:hover {
        transform: scale(1.05);
        border-color: currentColor;
        box-shadow: 0 0 20px currentColor;
    }
    
    .emotion-tag.active {
        background: currentColor;
        color: white;
    }
    
    /* Tension curve visualization */
    .tension-bar {
        height: 8px;
        border-radius: 4px;
        background: var(--bg-tertiary);
        overflow: hidden;
        position: relative;
    }
    
    .tension-fill {
        height: 100%;
        border-radius: 4px;
        background: var(--accent-aurora);
        transition: width 0.5s ease;
    }
    
    /* Phase indicators */
    .phase-indicator {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        background: var(--bg-tertiary);
        border-radius: 12px;
        border-left: 3px solid;
        margin-bottom: 1rem;
    }
    
    .phase-number {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    /* EMIDI Visualizer */
    .emidi-visualizer {
        background: var(--bg-tertiary);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid var(--border-subtle);
        position: relative;
        overflow: hidden;
    }
    
    .emidi-visualizer::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="DAiW — Digital Audio intimate Workstation",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()


# =============================================================================
# HELPER COMPONENTS
# =============================================================================

def render_emotion_orb(emotion: str, intensity: float = 0.7):
    """Render an animated emotion orb."""
    color = EMOTION_COLORS.get(emotion.lower(), "#667eea")
    emoji_map = {
        "grief": "💔", "rage": "🔥", "fear": "👁️", "nostalgia": "🌅",
        "defiance": "⚡", "tenderness": "🌸", "dissociation": "🌫️",
        "awe": "✨", "confusion": "🌀", "hope": "🌱", "longing": "🌙"
    }
    emoji = emoji_map.get(emotion.lower(), "💭")
    
    st.markdown(f"""
    <div style="display: flex; justify-content: center; margin: 1rem 0;">
        <div class="emotion-orb" style="
            background: radial-gradient(circle at 30% 30%, {color}88, {color}44);
            color: {color};
        ">
            {emoji}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_stat_box(value: str, label: str, icon: str = ""):
    """Render a stat box with value and label."""
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-value">{icon} {value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_chord_pills(chords: List[str]):
    """Render chord progression as interactive pills."""
    pills_html = "".join([f'<span class="chord-pill">{chord}</span>' for chord in chords])
    st.markdown(f'<div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">{pills_html}</div>', unsafe_allow_html=True)


def render_mode_badge(mode: str):
    """Render a colored mode badge."""
    color = MODE_COLORS.get(mode.lower(), "#667eea")
    st.markdown(f"""
    <span class="mode-badge" style="background: {color}22; color: {color}; border: 1px solid {color}44;">
        {mode.upper()}
    </span>
    """, unsafe_allow_html=True)


def render_tension_curve(sections: List[Dict], width: int = 100):
    """Render a visual tension curve."""
    st.markdown("#### Tension Curve")
    for section in sections:
        tension = section.get('tension', 0.5)
        name = section.get('name', 'Section')
        color = f"hsl({120 - tension * 120}, 70%, 50%)"  # Green to red
        st.markdown(f"""
        <div style="margin: 0.5rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span style="font-size: 0.8rem; color: var(--text-secondary);">{name}</span>
                <span style="font-size: 0.8rem; color: var(--text-muted);">{tension:.0%}</span>
            </div>
            <div class="tension-bar">
                <div class="tension-fill" style="width: {tension * 100}%; background: {color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_phase_indicator(phase: int, title: str, description: str, color: str = "#667eea"):
    """Render a phase indicator."""
    st.markdown(f"""
    <div class="phase-indicator" style="border-color: {color};">
        <div class="phase-number" style="background: {color}22; color: {color};">
            {phase}
        </div>
        <div>
            <div style="font-weight: 600; color: var(--text-primary);">{title}</div>
            <div style="font-size: 0.85rem; color: var(--text-muted);">{description}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_divider():
    """Render a subtle divider."""
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================

def render_sidebar():
    """Render sidebar with modern navigation."""
    with st.sidebar:
        # Logo/Brand
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌙</div>
            <div style="
                font-size: 1.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.02em;
            ">DAiW</div>
            <div style="
                font-size: 0.7rem;
                color: var(--text-muted);
                text-transform: uppercase;
                letter-spacing: 0.15em;
                margin-top: 0.25rem;
            ">Digital Audio intimate Workstation</div>
        </div>
        """, unsafe_allow_html=True)
        
        render_divider()
        
        # Navigation
        page = st.radio(
            "Navigate",
            [
                "🏠  Home",
                "💫  EMIDI Studio",
                "🎭  Wound & Healing",
                "📝  Intent Builder",
                "🎹  Harmony Lab",
                "🎸  Guitar FX Lab",
                "📊  Analysis",
                "🥁  Groove Engine",
                "📚  Rule Breaking",
            ],
            label_visibility="collapsed",
        )
        
        render_divider()
        
        # Philosophy quote
        st.markdown("""
        <div style="
            padding: 1rem;
            background: rgba(102, 126, 234, 0.05);
            border-radius: 12px;
            border: 1px solid rgba(102, 126, 234, 0.1);
        ">
            <div style="font-style: italic; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                "The tool shouldn't finish art for people. It should make them braver."
            </div>
            <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 0.5rem;">
                — DAiW Philosophy
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Version info
        st.markdown("""
        <div style="
            text-align: center;
            padding-top: 2rem;
            font-size: 0.7rem;
            color: var(--text-muted);
        ">
            v2.0.0 · Interrogate Before Generate
        </div>
        """, unsafe_allow_html=True)
        
        return page


# =============================================================================
# HOME PAGE
# =============================================================================

def render_home():
    """Render stunning home page."""
    # Hero section
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <div class="hero-title">Transform Emotion<br/>Into Music</div>
        <div class="hero-subtitle">
            EMIDI translates your emotional state into MIDI.<br/>
            Interrogate before you generate.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    render_divider()
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 2rem; margin-bottom: 0.75rem;">💫</div>
            <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-primary); margin-bottom: 0.5rem;">EMIDI Studio</div>
            <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5;">
                Express what hurts. Transform raw emotion into musical language that speaks what words cannot.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open EMIDI →", key="nav_emidi", use_container_width=True):
            st.session_state.page = "💫  EMIDI Studio"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 2rem; margin-bottom: 0.75rem;">🎭</div>
            <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-primary); margin-bottom: 0.5rem;">Wound & Healing</div>
            <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5;">
                Deep interrogation. What happened? What holds you back? What transformation do you seek?
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Begin Journey →", key="nav_wound", use_container_width=True):
            st.session_state.page = "🎭  Wound & Healing"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 2rem; margin-bottom: 0.75rem;">🎸</div>
            <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-primary); margin-bottom: 0.5rem;">Guitar FX Lab</div>
            <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5;">
                28+ effects. Full modulation matrix. Emotion-aware presets. The most customizable FX engine.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open FX Lab →", key="nav_fx", use_container_width=True):
            st.session_state.page = "🎸  Guitar FX Lab"
            st.rerun()
    
    render_divider()
    
    # Second row of features
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 2rem; margin-bottom: 0.75rem;">📚</div>
            <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-primary); margin-bottom: 0.5rem;">Rule Breaking</div>
            <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5;">
                Learn to break rules intentionally. Every deviation needs emotional justification.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Rules →", key="nav_rules", use_container_width=True):
            st.session_state.page = "📚  Rule Breaking"
            st.rerun()
    
    with col5:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 2rem; margin-bottom: 0.75rem;">🎹</div>
            <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-primary); margin-bottom: 0.5rem;">Harmony Lab</div>
            <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5;">
                Generate chord progressions with intentional rule-breaking for emotional impact.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Create Harmony →", key="nav_harmony", use_container_width=True):
            st.session_state.page = "🎹  Harmony Lab"
            st.rerun()
    
    with col6:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 2rem; margin-bottom: 0.75rem;">🥁</div>
            <div style="font-weight: 600; font-size: 1.1rem; color: var(--text-primary); margin-bottom: 0.5rem;">Groove Engine</div>
            <div style="font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5;">
                Extract groove DNA from any MIDI. Apply genre templates. Humanize your tracks.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Shape Groove →", key="nav_groove", use_container_width=True):
            st.session_state.page = "🥁  Groove Engine"
            st.rerun()
    
    render_divider()
    
    # Quick stats
    st.markdown("### 🎯 What Makes DAiW Different")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        render_stat_box("3", "Phase Intent", "🎭")
    with col2:
        render_stat_box("28+", "Guitar FX", "🎸")
    with col3:
        render_stat_box("24+", "Rule Breaks", "⚡")
    with col4:
        render_stat_box("7", "Modes", "🎵")
    with col5:
        render_stat_box("∞", "Emotions", "💭")
    
    render_divider()
    
    # Philosophy section
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(240, 147, 251, 0.08) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
    ">
        <div style="font-size: 1.5rem; font-weight: 600; color: var(--text-primary); margin-bottom: 1rem;">
            The Three-Phase Philosophy
        </div>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <div style="max-width: 200px;">
                <div style="color: #e53e3e; font-weight: 600; margin-bottom: 0.25rem;">Phase 0: The Wound</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">What happened? What needs to be said?</div>
            </div>
            <div style="max-width: 200px;">
                <div style="color: #ed8936; font-weight: 600; margin-bottom: 0.25rem;">Phase 1: The Emotion</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">What do you feel? What's at stake?</div>
            </div>
            <div style="max-width: 200px;">
                <div style="color: #48bb78; font-weight: 600; margin-bottom: 0.25rem;">Phase 2: The Sound</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">How will this manifest in music?</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# EMIDI STUDIO PAGE
# =============================================================================

def render_emidi_studio():
    """Render the cutting-edge EMIDI Studio interface."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">💫</div>
        <h1 style="margin-bottom: 0.5rem;">EMIDI Studio</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem;">
            Emotion-to-MIDI · Transform feelings into sound
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main input area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💭 Express Your Truth")
        st.markdown("""
        <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem;">
            Don't filter. Don't edit. Let the raw emotion flow.
        </div>
        """, unsafe_allow_html=True)
        
        user_text = st.text_area(
            "What needs to come out?",
            placeholder="I feel... \n\nWrite freely. The music will follow the emotion.",
            height=200,
            label_visibility="collapsed",
        )
        
        # Quick emotion tags
        st.markdown("#### Or start with an emotion:")
        
        emotions_row1 = ["grief", "rage", "fear", "nostalgia", "defiance"]
        emotions_row2 = ["tenderness", "dissociation", "awe", "confusion", "longing"]
        
        cols = st.columns(5)
        selected_emotion = None
        
        for i, emotion in enumerate(emotions_row1):
            with cols[i]:
                color = EMOTION_COLORS.get(emotion, "#667eea")
                if st.button(
                    emotion.capitalize(),
                    key=f"emotion_{emotion}",
                    use_container_width=True,
                ):
                    selected_emotion = emotion
                    user_text = f"I am feeling deep {emotion}."
        
        cols = st.columns(5)
        for i, emotion in enumerate(emotions_row2):
            with cols[i]:
                color = EMOTION_COLORS.get(emotion, "#667eea")
                if st.button(
                    emotion.capitalize(),
                    key=f"emotion_{emotion}",
                    use_container_width=True,
                ):
                    selected_emotion = emotion
    
    with col2:
        st.markdown("### ⚙️ Parameters")
        
        motivation = st.slider(
            "Motivation Level",
            min_value=1,
            max_value=10,
            value=7,
            help="1 = quick sketch, 10 = complete piece",
        )
        
        chaos = st.slider(
            "Chaos Tolerance",
            min_value=1,
            max_value=10,
            value=5,
            help="Higher = more instability, rhythmic displacement",
        )
        
        st.markdown("---")
        
        st.markdown("##### Output Settings")
        include_markers = st.checkbox("Include emotional markers", value=True)
        extended_form = st.checkbox("Extended form (32+ bars)", value=False)
    
    render_divider()
    
    # Generate button
    if st.button("🎵 Generate EMIDI", type="primary", use_container_width=True):
        if not user_text.strip():
            st.error("Please express something first. Even a single word can become music.")
            return
        
        # Processing animation
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        steps = [
            ("🔍 Analyzing emotional content...", 0.2),
            ("🎭 Detecting affect patterns...", 0.4),
            ("🎵 Mapping to musical parameters...", 0.6),
            ("🎹 Generating harmonic framework...", 0.8),
            ("✨ Rendering MIDI...", 1.0),
        ]
        
        for step_text, progress in steps:
            status_placeholder.markdown(f"<div style='text-align: center; color: var(--text-secondary);'>{step_text}</div>", unsafe_allow_html=True)
            progress_placeholder.progress(progress)
            time.sleep(0.3)
        
        progress_placeholder.empty()
        status_placeholder.empty()
        
        # Actual processing
        with st.spinner("Finalizing..."):
            session = TherapySession()
            affect = session.process_core_input(user_text)
            session.set_scales(motivation, chaos / 10.0)
            plan = session.generate_plan()
        
        st.success("✨ EMIDI generated successfully!")
        
        # Results display
        st.markdown("---")
        
        # Emotion visualization
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            render_emotion_orb(affect, session.state.affect_result.intensity if session.state.affect_result else 0.7)
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 600; color: var(--text-primary);">{affect.title()}</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">Primary Detected Emotion</div>
            </div>
            """, unsafe_allow_html=True)
        
        render_divider()
        
        # Musical parameters
        st.markdown("### 🎵 Generated Musical Parameters")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_stat_box(plan.root_note, "Root Note", "")
        with col2:
            render_stat_box(plan.mode.upper(), "Mode", "")
        with col3:
            render_stat_box(f"{plan.tempo_bpm}", "BPM", "")
        with col4:
            render_stat_box(f"{plan.length_bars}", "Bars", "")
        
        st.markdown("")
        
        # Chord progression
        st.markdown("#### 🎹 Chord Progression")
        render_chord_pills(plan.chord_symbols)
        
        # Mode explanation
        mode_explanations = {
            "ionian": ("Bright & Resolved", "The major scale — stability, happiness, resolution"),
            "dorian": ("Nostalgic & Bittersweet", "Minor with hope — jazz, funk, melancholic warmth"),
            "phrygian": ("Dark & Tense", "Spanish/Flamenco color — mystery, tension, exoticism"),
            "lydian": ("Dreamy & Floating", "Ethereal, otherworldly — the raised 4th creates suspension"),
            "mixolydian": ("Bluesy & Defiant", "Rock and blues backbone — earthy, grounded, rebellious"),
            "aeolian": ("Sad & Introspective", "Natural minor — melancholy, grief, reflection"),
            "locrian": ("Unstable & Disorienting", "Diminished quality — dissociation, anxiety, unease"),
        }
        
        mode_info = mode_explanations.get(plan.mode.lower(), ("Musical Mode", "A specific scale pattern"))
        
        st.markdown(f"""
        <div style="
            background: var(--bg-tertiary);
            border-left: 3px solid {MODE_COLORS.get(plan.mode.lower(), '#667eea')};
            padding: 1rem 1.25rem;
            border-radius: 0 12px 12px 0;
            margin: 1rem 0;
        ">
            <div style="font-weight: 600; color: var(--text-primary);">{mode_info[0]}</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.25rem;">{mode_info[1]}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed analysis expander
        with st.expander("📊 Detailed Emotional Analysis"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Affect Scores")
                if session.state.affect_result and session.state.affect_result.scores:
                    scores = session.state.affect_result.scores
                    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
                    
                    for emotion, score in sorted_scores:
                        if score > 0:
                            percentage = min(score / max(s for _, s in sorted_scores) * 100, 100)
                            color = EMOTION_COLORS.get(emotion, "#667eea")
                            st.markdown(f"""
                            <div style="margin: 0.5rem 0;">
                                <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
                                    <span style="color: {color};">{emotion.title()}</span>
                                    <span style="color: var(--text-muted);">{score:.1f}</span>
                                </div>
                                <div class="tension-bar">
                                    <div class="tension-fill" style="width: {percentage}%; background: {color};"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("##### Processing Path")
                st.markdown(f"""
                - **Input Length:** {len(user_text.split())} words
                - **Primary Affect:** {affect.title()}
                - **Secondary:** {session.state.affect_result.secondary.title() if session.state.affect_result and session.state.affect_result.secondary else 'None'}
                - **Intensity:** {session.state.affect_result.intensity:.2f if session.state.affect_result else 0}
                - **Complexity:** {plan.complexity:.2f}
                - **Mood Profile:** {plan.mood_profile}
                """)
        
        # Generate and offer download
        with st.spinner("Rendering MIDI file..."):
            tmpdir = tempfile.mkdtemp(prefix="daiw_")
            midi_path = os.path.join(tmpdir, "emidi_output.mid")
            midi_path = render_plan_to_midi(plan, midi_path)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with open(midi_path, "rb") as f:
                st.download_button(
                    label="📥 Download EMIDI File",
                    data=f.read(),
                    file_name=f"emidi_{affect}_{plan.tempo_bpm}bpm.mid",
                    mime="audio/midi",
                    type="primary",
                    use_container_width=True,
                )


# =============================================================================
# WOUND & HEALING PAGE (Deep Interrogation)
# =============================================================================

def render_wound_healing():
    """Render the deep interrogation interface."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎭</div>
        <h1 style="margin-bottom: 0.5rem;">Wound & Healing</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem;">
            Deep interrogation before generation · Three phases of emotional clarity
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress indicator
    if "wound_phase" not in st.session_state:
        st.session_state.wound_phase = 0
    
    phases = ["The Wound", "The Emotion", "The Sound"]
    phase_colors = ["#e53e3e", "#ed8936", "#48bb78"]
    
    # Phase tabs
    tab1, tab2, tab3 = st.tabs(["🩸 Phase 0: The Wound", "💭 Phase 1: The Emotion", "🎵 Phase 2: The Sound"])
    
    with tab1:
        render_phase_indicator(0, "The Wound", "What happened? What needs to be said?", "#e53e3e")
        
        st.markdown("##### What happened?")
        core_event = st.text_area(
            "The specific moment, memory, or realization...",
            placeholder="The night I realized... / When they said... / I finally understood that...",
            height=120,
            key="core_event",
            label_visibility="collapsed",
        )
        
        st.markdown("##### What holds you back from saying it?")
        core_resistance = st.text_area(
            "The resistance...",
            placeholder="I'm afraid of... / I don't want to admit... / It feels too...",
            height=100,
            key="core_resistance",
            label_visibility="collapsed",
        )
        
        st.markdown("##### What do you long for?")
        core_longing = st.text_area(
            "The longing...",
            placeholder="I wish I could feel... / I want to be... / I need...",
            height=100,
            key="core_longing",
            label_visibility="collapsed",
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### What's at stake?")
            core_stakes = st.selectbox(
                "Stakes",
                ["Personal Identity", "Relationship", "Existential", "Creative Expression", "Spiritual"],
                key="core_stakes",
                label_visibility="collapsed",
            )
        
        with col2:
            st.markdown("##### What transformation do you seek?")
            core_transformation = st.selectbox(
                "Transformation",
                ["Release", "Acceptance", "Understanding", "Catharsis", "Integration", "Defiance"],
                key="core_transformation",
                label_visibility="collapsed",
            )
    
    with tab2:
        render_phase_indicator(1, "The Emotion", "What do you feel? How intense?", "#ed8936")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Primary Emotion")
            mood_primary = st.selectbox(
                "Primary",
                ["grief", "rage", "fear", "nostalgia", "defiance", "tenderness", "dissociation", "awe", "confusion", "longing"],
                key="mood_primary",
                label_visibility="collapsed",
            )
            
            # Show emotion orb
            render_emotion_orb(mood_primary, 0.8)
            
            st.markdown("##### Secondary Tension")
            mood_secondary = st.slider(
                "How much internal conflict?",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                key="mood_secondary",
                help="0 = pure emotion, 1 = deeply conflicted",
            )
        
        with col2:
            st.markdown("##### Vulnerability Level")
            vulnerability = st.select_slider(
                "How exposed?",
                options=["Guarded", "Cautious", "Open", "Exposed", "Raw"],
                value="Open",
                key="vulnerability",
            )
            
            st.markdown("##### Narrative Arc")
            narrative_arc = st.selectbox(
                "Arc",
                [
                    "Climb-to-Climax (building intensity)",
                    "Slow Reveal (gradual unfolding)",
                    "Repetitive Despair (circular, trapped)",
                    "Cathartic Release (explosion → calm)",
                    "Circular Return (back where we started)",
                ],
                key="narrative_arc",
                label_visibility="collapsed",
            )
            
            st.markdown("##### Imagery/Texture")
            imagery = st.text_input(
                "Visual quality",
                placeholder="gritty, ethereal, underwater, fractured...",
                key="imagery",
                label_visibility="collapsed",
            )
    
    with tab3:
        render_phase_indicator(2, "The Sound", "Technical constraints informed by emotion", "#48bb78")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Key & Mode")
            key_col, mode_col = st.columns(2)
            with key_col:
                tech_key = st.selectbox(
                    "Key",
                    ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"],
                    key="tech_key",
                    label_visibility="collapsed",
                )
            with mode_col:
                tech_mode = st.selectbox(
                    "Mode",
                    ["major", "minor", "dorian", "phrygian", "lydian", "mixolydian", "locrian"],
                    key="tech_mode",
                    label_visibility="collapsed",
                )
            
            render_mode_badge(tech_mode)
            
            st.markdown("##### Tempo Range")
            tempo_range = st.slider(
                "BPM",
                min_value=40,
                max_value=200,
                value=(70, 100),
                key="tempo_range",
                label_visibility="collapsed",
            )
            
            st.markdown("##### Genre")
            tech_genre = st.text_input(
                "Genre",
                placeholder="bedroom emo, lo-fi, ambient, noise rock...",
                key="tech_genre",
                label_visibility="collapsed",
            )
        
        with col2:
            st.markdown("##### Rule to Break")
            
            # Show suggestions based on primary emotion
            if "mood_primary" in st.session_state:
                suggestions = suggest_rule_break(st.session_state.mood_primary)
                if suggestions:
                    st.markdown("*Suggested for your emotion:*")
                    for sug in suggestions[:2]:
                        st.markdown(f"""
                        <div style="
                            background: var(--bg-tertiary);
                            border-radius: 8px;
                            padding: 0.75rem;
                            margin: 0.5rem 0;
                            font-size: 0.85rem;
                        ">
                            <div style="color: var(--text-primary); font-weight: 500;">{sug['rule']}</div>
                            <div style="color: var(--text-muted); font-size: 0.8rem;">{sug['effect']}</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            rule_to_break = st.text_input(
                "Rule",
                placeholder="e.g., HARMONY_AvoidTonicResolution",
                key="rule_to_break",
                label_visibility="collapsed",
            )
            
            st.markdown("##### Why break this rule?")
            rule_justification = st.text_area(
                "Justification",
                placeholder="Because the emotion demands... / To capture the feeling of...",
                height=100,
                key="rule_justification",
                label_visibility="collapsed",
            )
    
    render_divider()
    
    # Generate button
    if st.button("🎵 Generate from Intent", type="primary", use_container_width=True):
        # Validate
        if not st.session_state.get("core_event"):
            st.error("Please fill in Phase 0: The Wound first.")
            return
        
        with st.spinner("Processing your intent..."):
            try:
                intent = CompleteSongIntent(
                    title="Generated from Wound & Healing",
                    song_root=SongRoot(
                        core_event=st.session_state.get("core_event", ""),
                        core_resistance=st.session_state.get("core_resistance", ""),
                        core_longing=st.session_state.get("core_longing", ""),
                        core_stakes=st.session_state.get("core_stakes", "Personal Identity"),
                        core_transformation=st.session_state.get("core_transformation", "Release"),
                    ),
                    song_intent=SongIntent(
                        mood_primary=st.session_state.get("mood_primary", "grief"),
                        mood_secondary_tension=st.session_state.get("mood_secondary", 0.5),
                        imagery_texture=st.session_state.get("imagery", ""),
                        vulnerability_scale=st.session_state.get("vulnerability", "Open"),
                        narrative_arc=st.session_state.get("narrative_arc", "").split(" (")[0],
                    ),
                    technical_constraints=TechnicalConstraints(
                        technical_genre=st.session_state.get("tech_genre", ""),
                        technical_tempo_range=st.session_state.get("tempo_range", (70, 100)),
                        technical_key=st.session_state.get("tech_key", "C"),
                        technical_mode=st.session_state.get("tech_mode", "minor"),
                        technical_groove_feel="Organic/Breathing",
                        technical_rule_to_break=st.session_state.get("rule_to_break", ""),
                        rule_breaking_justification=st.session_state.get("rule_justification", ""),
                    ),
                    system_directive=SystemDirective(),
                )
                
                # Validate
                issues = validate_intent(intent)
                if issues:
                    st.warning("⚠️ Validation notes:")
                    for issue in issues:
                        st.write(f"- {issue}")
                
                # Process
                result = process_intent(intent)
                
                st.success("✨ Generation complete!")
                
                # Display results
                st.markdown("### 🎵 Generated Elements")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### Harmony")
                    harmony = result['harmony']
                    render_chord_pills(harmony.chords)
                    st.caption(f"Roman numerals: {' - '.join(harmony.roman_numerals)}")
                    
                    if harmony.rule_broken:
                        st.info(f"**Rule Broken:** {harmony.rule_broken}\n\n*Effect:* {harmony.rule_effect}")
                
                with col2:
                    st.markdown("##### Groove")
                    groove = result['groove']
                    st.write(f"**Pattern:** {groove.pattern_name}")
                    st.write(f"**Tempo:** {groove.tempo_bpm} BPM")
                    
                    st.markdown("##### Arrangement")
                    arr = result['arrangement']
                    render_tension_curve(arr.sections)
                
                # Lyrical fragments
                with st.expander("📝 Lyrical Fragments"):
                    fragments = generate_lyrical_fragments(intent)
                    if fragments:
                        for fragment in fragments[:5]:
                            st.markdown(f"*{fragment}*")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.exception(e)


# =============================================================================
# INTENT BUILDER PAGE
# =============================================================================

def render_intent_builder():
    """Render a streamlined intent builder."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📝</div>
        <h1 style="margin-bottom: 0.5rem;">Intent Builder</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem;">
            Build, save, and load song intent files
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Create Intent", "Load Intent"])
    
    with tab1:
        st.markdown("### Quick Intent Creator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Song Title", placeholder="Untitled")
            emotion = st.selectbox("Primary Emotion", ["grief", "rage", "fear", "nostalgia", "defiance", "tenderness", "awe", "confusion"])
            key = st.selectbox("Key", ["C", "D", "E", "F", "G", "A", "B", "Eb", "Bb", "Ab"])
        
        with col2:
            mode = st.selectbox("Mode", ["minor", "major", "dorian", "phrygian", "lydian", "mixolydian"])
            tempo = st.number_input("Tempo (BPM)", min_value=40, max_value=200, value=82)
            genre = st.text_input("Genre", placeholder="bedroom emo, lo-fi...")
        
        core_event = st.text_area("Core Event (What happened?)", placeholder="The moment that sparked this song...", height=100)
        
        if st.button("Generate Intent JSON", type="primary"):
            intent_data = {
                "title": title or "Untitled",
                "song_root": {
                    "core_event": core_event,
                    "core_resistance": "",
                    "core_longing": "",
                    "core_stakes": "Personal",
                    "core_transformation": "",
                },
                "song_intent": {
                    "mood_primary": emotion,
                    "mood_secondary_tension": 0.5,
                    "imagery_texture": "",
                    "vulnerability_scale": "Medium",
                    "narrative_arc": "Climb-to-Climax",
                },
                "technical_constraints": {
                    "technical_genre": genre,
                    "technical_tempo_range": [tempo - 10, tempo + 10],
                    "technical_key": key,
                    "technical_mode": mode,
                    "technical_groove_feel": "Organic/Breathing",
                    "technical_rule_to_break": "",
                    "rule_breaking_justification": "",
                },
            }
            
            intent_json = json.dumps(intent_data, indent=2)
            
            st.code(intent_json, language="json")
            
            st.download_button(
                "📥 Download Intent JSON",
                data=intent_json,
                file_name=f"{title or 'untitled'}_intent.json",
                mime="application/json",
                use_container_width=True,
            )
    
    with tab2:
        st.markdown("### Load Existing Intent")
        
        uploaded = st.file_uploader("Upload Intent JSON", type=["json"])
        
        if uploaded:
            try:
                intent_data = json.load(uploaded)
                st.success("Intent loaded!")
                
                with st.expander("View Intent", expanded=True):
                    st.json(intent_data)
                
                if st.button("Process Intent", type="primary"):
                    with st.spinner("Processing..."):
                        intent = CompleteSongIntent.from_dict(intent_data)
                        result = process_intent(intent)
                        
                        st.success("Processed!")
                        
                        harmony = result['harmony']
                        st.markdown("#### Generated Harmony")
                        render_chord_pills(harmony.chords)
                        
            except Exception as e:
                st.error(f"Error loading intent: {e}")


# =============================================================================
# HARMONY LAB PAGE
# =============================================================================

def render_harmony_lab():
    """Render the harmony generator lab."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎹</div>
        <h1 style="margin-bottom: 0.5rem;">Harmony Lab</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem;">
            Generate chord progressions with intentional rule-breaking
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Build Your Progression")
        
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            key = st.selectbox("Key", ["F", "C", "G", "D", "A", "E", "B", "Bb", "Eb", "Ab"])
            pattern = st.text_input("Roman Numeral Pattern", value="I-V-vi-IV", help="e.g., I-V-vi-IV, ii-V-I, I-vi-ii-V")
        
        with row1_col2:
            mode = st.selectbox("Mode", ["major", "minor", "dorian", "phrygian", "lydian", "mixolydian"])
            tempo = st.number_input("Tempo (BPM)", min_value=40, max_value=200, value=82)
        
        render_mode_badge(mode)
        
        st.markdown("### Rule Breaking (Optional)")
        
        rule_col1, rule_col2 = st.columns(2)
        
        with rule_col1:
            rule_break = st.selectbox(
                "Rule to Break",
                [
                    "None",
                    "HARMONY_AvoidTonicResolution",
                    "HARMONY_ModalInterchange",
                    "HARMONY_ParallelMovement",
                    "RHYTHM_ConstantDisplacement",
                    "PRODUCTION_PitchImperfection",
                ],
            )
        
        with rule_col2:
            if rule_break != "None":
                justification = st.text_input("Why?", placeholder="Because the emotion demands...")
    
    with col2:
        st.markdown("### Preview")
        
        st.markdown("""
        <div style="
            background: var(--bg-tertiary);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid var(--border-subtle);
        ">
            <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em;">Current Selection</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Key", f"{key} {mode}")
        st.metric("Pattern", pattern)
        st.metric("Tempo", f"{tempo} BPM")
    
    render_divider()
    
    if st.button("🎹 Generate Harmony", type="primary", use_container_width=True):
        with st.spinner("Generating..."):
            try:
                generator = HarmonyGenerator()
                harmony = generator.generate_basic_progression(
                    key=key,
                    mode=mode,
                    pattern=pattern,
                )
                
                st.success("✨ Harmony generated!")
                
                st.markdown("### Result")
                render_chord_pills(harmony.chords)
                
                # Generate MIDI
                tmpdir = tempfile.mkdtemp(prefix="daiw_")
                midi_path = os.path.join(tmpdir, "harmony.mid")
                generate_midi_from_harmony(harmony, midi_path, tempo_bpm=tempo)
                
                with open(midi_path, "rb") as f:
                    st.download_button(
                        "📥 Download MIDI",
                        data=f.read(),
                        file_name=f"harmony_{key}_{mode}_{tempo}bpm.mid",
                        mime="audio/midi",
                        type="primary",
                        use_container_width=True,
                    )
                
            except Exception as e:
                st.error(f"Error: {e}")


# =============================================================================
# GUITAR FX LAB PAGE
# =============================================================================

def render_guitar_fx_lab():
    """Render the comprehensive guitar effects modulator."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎸</div>
        <h1 style="margin-bottom: 0.5rem;">Guitar FX Lab</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem;">
            The most customizable effects modulator · Every technique · Emotionally aware
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not EFFECTS_AVAILABLE:
        st.error("Effects module not available. Please check installation.")
        return
    
    # Initialize engine in session state
    if "fx_engine" not in st.session_state:
        st.session_state.fx_engine = GuitarFXEngine()
    
    engine = st.session_state.fx_engine
    
    # Top stats bar
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_stat_box(str(len(ALL_EFFECTS)), "Effects", "🎛️")
    with col2:
        render_stat_box(str(len(engine.chain.effects)), "Active", "✓")
    with col3:
        render_stat_box(str(len(engine.modulation.sources)), "Mod Sources", "〰️")
    with col4:
        current_emotion = engine.current_emotion or "None"
        render_stat_box(current_emotion.title()[:8], "Emotion", "💭")
    
    render_divider()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎛️ Effect Chain",
        "〰️ Modulation",
        "💭 Emotion FX",
        "📦 Presets",
        "📚 All Effects",
    ])
    
    # ==========================================================================
    # TAB 1: EFFECT CHAIN
    # ==========================================================================
    with tab1:
        st.markdown("### Build Your Signal Chain")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Add effect
            st.markdown("##### Add Effect")
            
            add_col1, add_col2 = st.columns([3, 1])
            
            with add_col1:
                # Group by category
                categories = engine.list_effects_by_category()
                all_effects_list = []
                for cat, effects in categories.items():
                    for eff in effects:
                        all_effects_list.append(f"{cat.upper()}: {eff}")
                
                selected_effect = st.selectbox(
                    "Select Effect",
                    all_effects_list,
                    label_visibility="collapsed",
                )
            
            with add_col2:
                if st.button("➕ Add", use_container_width=True):
                    effect_name = selected_effect.split(": ")[1]
                    try:
                        engine.add_effect(effect_name)
                        st.success(f"Added {effect_name}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            # Current chain
            st.markdown("##### Current Chain")
            
            if not engine.chain.order:
                st.info("No effects in chain. Add some above!")
            else:
                for i, effect_name in enumerate(engine.chain.order):
                    effect = engine.chain.get_effect(effect_name)
                    if not effect:
                        continue
                    
                    with st.expander(f"**{i+1}. {effect_name}**", expanded=False):
                        # Bypass toggle
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            effect.bypass = st.checkbox(
                                "Bypass",
                                value=effect.bypass,
                                key=f"bypass_{effect_name}_{i}",
                            )
                        with col_b:
                            if st.button("🗑️", key=f"remove_{effect_name}_{i}"):
                                engine.remove_effect(effect_name)
                                st.rerun()
                        
                        # Parameters
                        st.markdown("**Parameters:**")
                        
                        params = effect.parameters
                        param_cols = st.columns(2)
                        
                        for j, (param_name, param) in enumerate(params.items()):
                            with param_cols[j % 2]:
                                new_val = st.slider(
                                    param_name.replace("_", " ").title(),
                                    min_value=float(param.min_val),
                                    max_value=float(param.max_val),
                                    value=float(param.value),
                                    key=f"param_{effect_name}_{param_name}_{i}",
                                    help=param.description,
                                )
                                effect.set_param(param_name, new_val)
        
        with col2:
            st.markdown("##### Chain Settings")
            
            engine.chain.input_level = st.slider(
                "Input Level",
                0.0, 2.0, engine.chain.input_level,
                key="chain_input",
            )
            
            engine.chain.output_level = st.slider(
                "Output Level",
                0.0, 2.0, engine.chain.output_level,
                key="chain_output",
            )
            
            engine.chain.global_bypass = st.checkbox(
                "Global Bypass",
                value=engine.chain.global_bypass,
            )
            
            st.markdown("---")
            
            if st.button("🔀 Randomize All", use_container_width=True):
                for effect in engine.chain.effects.values():
                    effect.randomize(0.3)
                st.rerun()
            
            if st.button("🗑️ Clear Chain", use_container_width=True):
                engine.chain.effects.clear()
                engine.chain.order.clear()
                st.rerun()
    
    # ==========================================================================
    # TAB 2: MODULATION
    # ==========================================================================
    with tab2:
        st.markdown("### Modulation Matrix")
        st.caption("Any source can modulate any parameter")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Modulation Sources")
            
            for source_name, source in engine.modulation.sources.items():
                source_type = type(source).__name__
                
                with st.expander(f"**{source_name}** ({source_type})", expanded=False):
                    st.write(f"Current output: **{source.output:.3f}**")
                    
                    # LFO specific controls
                    if "LFO" in source_name:
                        source.rate = st.slider(
                            "Rate (Hz)",
                            0.01, 20.0, float(source.rate),
                            key=f"lfo_rate_{source_name}",
                        )
                        source.depth = st.slider(
                            "Depth",
                            0.0, 1.0, float(source.depth),
                            key=f"lfo_depth_{source_name}",
                        )
                    
                    # Step sequencer
                    elif "StepSeq" in source_name:
                        st.write("Steps:")
                        for step_i in range(min(8, source.num_steps)):
                            source.steps[step_i] = st.slider(
                                f"Step {step_i+1}",
                                -1.0, 1.0, float(source.steps[step_i]),
                                key=f"step_{source_name}_{step_i}",
                            )
        
        with col2:
            st.markdown("##### Add Modulation Route")
            
            # Source selection
            source_options = list(engine.modulation.sources.keys())
            selected_source = st.selectbox("Source", source_options, key="mod_source")
            
            # Target effect
            effect_options = list(engine.chain.effects.keys())
            if effect_options:
                selected_target_effect = st.selectbox("Target Effect", effect_options, key="mod_target_effect")
                
                # Target parameter
                if selected_target_effect:
                    effect = engine.chain.get_effect(selected_target_effect)
                    if effect:
                        param_options = list(effect.parameters.keys())
                        selected_param = st.selectbox("Target Parameter", param_options, key="mod_target_param")
                        
                        mod_amount = st.slider("Amount", -1.0, 1.0, 0.5, key="mod_amount")
                        
                        if st.button("Add Route", type="primary"):
                            engine.add_modulation(selected_source, selected_target_effect, selected_param, mod_amount)
                            st.success(f"Added modulation: {selected_source} → {selected_target_effect}.{selected_param}")
            else:
                st.info("Add effects to the chain first")
            
            # Active routes
            st.markdown("##### Active Routes")
            
            if not engine.modulation.routes:
                st.caption("No modulation routes")
            else:
                for route in engine.modulation.routes:
                    st.markdown(f"""
                    <div style="
                        background: var(--bg-tertiary);
                        border-radius: 8px;
                        padding: 0.5rem 0.75rem;
                        margin: 0.25rem 0;
                        font-size: 0.85rem;
                    ">
                        <span style="color: #667eea;">{route.source_name}</span> → 
                        <span style="color: var(--text-primary);">{route.target_effect}.{route.target_param}</span>
                        <span style="color: var(--text-muted);"> ({route.amount:+.2f})</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ==========================================================================
    # TAB 3: EMOTION FX
    # ==========================================================================
    with tab3:
        st.markdown("### Emotion-Driven Effects")
        st.caption("Let your emotional state shape your sound — the DAiW way")
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(240, 147, 251, 0.1) 100%);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        ">
            <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">
                🎭 How It Works
            </div>
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                Select an emotion, and DAiW will suggest and configure effects that complement 
                that emotional state. Each emotion maps to specific effect parameters that have 
                been designed to evoke that feeling sonically.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Select Emotion")
            
            emotions = ["grief", "rage", "fear", "nostalgia", "defiance", "tenderness", "dissociation", "awe", "confusion", "longing"]
            
            selected_emotion = st.selectbox(
                "Emotion",
                emotions,
                format_func=lambda x: x.title(),
                key="emotion_select",
                label_visibility="collapsed",
            )
            
            intensity = st.slider("Intensity", 0.0, 1.0, 1.0, key="emotion_intensity")
            
            # Show emotion orb
            render_emotion_orb(selected_emotion, intensity)
            
            if st.button("🎭 Apply Emotion Effects", type="primary", use_container_width=True):
                engine.set_emotion(selected_emotion, intensity)
                engine.apply_emotion_preset(selected_emotion, intensity)
                st.success(f"Applied {selected_emotion} effects at {intensity:.0%} intensity")
                st.rerun()
        
        with col2:
            st.markdown("##### Effect Suggestions")
            
            suggestions = get_effect_suggestions(selected_emotion)
            
            if suggestions:
                for sug in suggestions:
                    effect_type = sug["effect"].replace("_", " ").title()
                    params = sug["params"]
                    
                    st.markdown(f"""
                    <div style="
                        background: var(--bg-tertiary);
                        border-radius: 12px;
                        padding: 1rem;
                        margin: 0.5rem 0;
                        border-left: 3px solid {EMOTION_COLORS.get(selected_emotion, '#667eea')};
                    ">
                        <div style="font-weight: 600; color: var(--text-primary);">{effect_type}</div>
                        <div style="color: var(--text-muted); font-size: 0.8rem; margin-top: 0.25rem;">
                            {', '.join([f'{k}={v}' for k, v in list(params.items())[:3]])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("No specific suggestions for this emotion")
        
        # Emotion description
        emotion_descriptions = {
            "grief": "Heavy reverb, filtered highs, slow modulation — the weight of loss",
            "rage": "High gain distortion, aggressive compression — raw power unleashed",
            "fear": "Fast tremolo, swirling phaser, dark ambience — anxiety in sound",
            "nostalgia": "Warm chorus, tape delay, spring reverb — memories in motion",
            "defiance": "Crunchy overdrive, bold presence — standing your ground",
            "tenderness": "Gentle chorus, soft compression — vulnerability exposed",
            "dissociation": "Shimmer reverb, granular textures — floating away",
            "awe": "Lush reverb, ethereal shimmer — transcendent moments",
            "confusion": "Chaotic modulation, ping-pong delays — disorientation",
            "longing": "Long reverb, distant delays — reaching for what's gone",
        }
        
        st.markdown(f"""
        <div style="
            background: var(--bg-tertiary);
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
            text-align: center;
        ">
            <div style="font-style: italic; color: var(--text-secondary);">
                "{emotion_descriptions.get(selected_emotion, 'Express your truth through sound.')}"
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # ==========================================================================
    # TAB 4: PRESETS
    # ==========================================================================
    with tab4:
        st.markdown("### Preset Manager")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Save Current Settings")
            
            preset_name = st.text_input("Preset Name", placeholder="My Awesome Sound")
            preset_desc = st.text_area("Description", placeholder="What makes this sound special?", height=80)
            
            if st.button("💾 Save Preset", use_container_width=True):
                if preset_name:
                    try:
                        tmpdir = tempfile.mkdtemp(prefix="daiw_fx_")
                        preset_path = os.path.join(tmpdir, f"{preset_name.replace(' ', '_')}.json")
                        preset = engine.save_preset(preset_name, preset_path, preset_desc)
                        
                        with open(preset_path, "r") as f:
                            preset_data = f.read()
                        
                        st.download_button(
                            "📥 Download Preset",
                            data=preset_data,
                            file_name=f"{preset_name.replace(' ', '_')}.json",
                            mime="application/json",
                            use_container_width=True,
                        )
                        
                        st.success("Preset saved!")
                    except Exception as e:
                        st.error(f"Error saving preset: {e}")
                else:
                    st.warning("Please enter a preset name")
        
        with col2:
            st.markdown("##### Load Preset")
            
            uploaded = st.file_uploader("Upload Preset JSON", type=["json"], key="preset_upload")
            
            if uploaded:
                try:
                    tmpdir = tempfile.mkdtemp(prefix="daiw_fx_")
                    preset_path = os.path.join(tmpdir, uploaded.name)
                    
                    with open(preset_path, "wb") as f:
                        f.write(uploaded.getbuffer())
                    
                    preset = engine.load_preset(preset_path)
                    st.success(f"Loaded preset: {preset.name}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error loading preset: {e}")
            
            st.markdown("---")
            
            st.markdown("##### Quick Presets")
            
            quick_presets = [
                ("Clean & Sparkly", ["Compressor", "Chorus", "Reverb"]),
                ("Dirty Blues", ["Overdrive", "Delay", "Reverb"]),
                ("Heavy Metal", ["Noise Gate", "Distortion", "EQ", "Reverb"]),
                ("Ambient Dream", ["Shimmer", "Delay", "Reverb"]),
                ("Lo-Fi Vibes", ["Bitcrusher", "Chorus", "Delay"]),
            ]
            
            for preset_name, effects in quick_presets:
                if st.button(preset_name, key=f"quick_{preset_name}", use_container_width=True):
                    engine.chain.effects.clear()
                    engine.chain.order.clear()
                    for eff in effects:
                        try:
                            engine.add_effect(eff)
                        except:
                            pass
                    st.success(f"Loaded: {preset_name}")
                    st.rerun()
    
    # ==========================================================================
    # TAB 5: ALL EFFECTS REFERENCE
    # ==========================================================================
    with tab5:
        st.markdown("### Complete Effects Reference")
        st.caption(f"**{len(ALL_EFFECTS)} effects** across **8 categories**")
        
        categories = engine.list_effects_by_category()
        
        category_icons = {
            "distortion": "🔥",
            "modulation": "〰️",
            "time": "⏱️",
            "dynamics": "📊",
            "filter": "🎚️",
            "pitch": "🎵",
            "amp": "🔊",
            "special": "✨",
        }
        
        category_descriptions = {
            "distortion": "Overdrive, fuzz, and harmonic saturation",
            "modulation": "Chorus, flanger, phaser, tremolo, and more",
            "time": "Delay and reverb algorithms",
            "dynamics": "Compressor, gate, and dynamics processing",
            "filter": "EQ, wah, and filter effects",
            "pitch": "Pitch shifting, harmonizing, and octave effects",
            "amp": "Amplifier and cabinet simulation",
            "special": "Unique effects: granular, shimmer, freeze, slicer",
        }
        
        for cat, effects in categories.items():
            icon = category_icons.get(cat, "🎛️")
            desc = category_descriptions.get(cat, "")
            
            with st.expander(f"{icon} **{cat.upper()}** — {len(effects)} effects", expanded=False):
                st.caption(desc)
                
                effect_cols = st.columns(3)
                for i, effect in enumerate(effects):
                    with effect_cols[i % 3]:
                        st.markdown(f"""
                        <div style="
                            background: var(--bg-tertiary);
                            border-radius: 8px;
                            padding: 0.75rem;
                            margin: 0.25rem 0;
                            text-align: center;
                        ">
                            <div style="font-weight: 500; color: var(--text-primary);">{effect}</div>
                        </div>
                        """, unsafe_allow_html=True)


# =============================================================================
# ANALYSIS PAGE
# =============================================================================

def render_analysis():
    """Render MIDI analysis page."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
        <h1 style="margin-bottom: 0.5rem;">Analysis</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem;">
            Upload MIDI files to analyze structure, harmony, and groove
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded = st.file_uploader("Upload MIDI File", type=["mid", "midi"])
    
    if uploaded:
        tmpdir = tempfile.mkdtemp(prefix="daiw_")
        midi_path = os.path.join(tmpdir, uploaded.name)
        
        with open(midi_path, "wb") as f:
            f.write(uploaded.getbuffer())
        
        st.success(f"Uploaded: {uploaded.name}")
        
        tab1, tab2, tab3 = st.tabs(["Chord Analysis", "Section Detection", "Groove Extraction"])
        
        with tab1:
            if st.button("Analyze Chords", key="analyze_chords"):
                with st.spinner("Analyzing..."):
                    try:
                        progression = analyze_chords(midi_path)
                        
                        st.markdown("### Detected Progression")
                        render_chord_pills(progression.chords)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Key", progression.key)
                        with col2:
                            st.metric("Roman Numerals", " - ".join(progression.roman_numerals))
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        with tab2:
            if st.button("Detect Sections", key="detect_sections"):
                with st.spinner("Detecting..."):
                    try:
                        sections = detect_sections(midi_path)
                        
                        st.markdown("### Detected Sections")
                        
                        for section in sections:
                            st.markdown(f"""
                            <div style="
                                background: var(--bg-tertiary);
                                border-radius: 12px;
                                padding: 1rem;
                                margin: 0.5rem 0;
                                border-left: 3px solid hsl({120 - section.energy * 120}, 70%, 50%);
                            ">
                                <div style="font-weight: 600; color: var(--text-primary);">{section.name}</div>
                                <div style="font-size: 0.85rem; color: var(--text-muted);">
                                    Bars {section.start_bar}-{section.end_bar} · Energy: {section.energy:.0%}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        with tab3:
            if st.button("Extract Groove", key="extract_groove"):
                with st.spinner("Extracting..."):
                    try:
                        groove = extract_groove(midi_path)
                        
                        st.markdown("### Groove DNA")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            render_stat_box(f"{groove.timing_stats['mean_deviation_ms']:.1f}ms", "Timing Dev", "")
                        with col2:
                            render_stat_box(f"{groove.swing_factor:.2f}", "Swing", "")
                        with col3:
                            render_stat_box(f"{groove.velocity_stats['std']:.1f}", "Vel. Variance", "")
                        
                        # Download groove JSON
                        groove_json = json.dumps(groove.to_dict(), indent=2)
                        st.download_button(
                            "📥 Download Groove DNA",
                            data=groove_json,
                            file_name="groove_dna.json",
                            mime="application/json",
                            use_container_width=True,
                        )
                        
                    except Exception as e:
                        st.error(f"Error: {e}")


# =============================================================================
# GROOVE ENGINE PAGE
# =============================================================================

def render_groove_engine():
    """Render groove tools page."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🥁</div>
        <h1 style="margin-bottom: 0.5rem;">Groove Engine</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem;">
            Extract and apply groove patterns · Humanize your MIDI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Apply Groove", "Extract Groove"])
    
    with tab1:
        st.markdown("### Apply Genre Groove")
        
        uploaded = st.file_uploader("Upload MIDI to groove", type=["mid", "midi"], key="groove_apply")
        
        if uploaded:
            col1, col2 = st.columns(2)
            
            with col1:
                genre = st.selectbox(
                    "Genre Template",
                    ["funk", "jazz", "rock", "hiphop", "edm", "latin", "neosoul"],
                )
            
            with col2:
                intensity = st.slider("Intensity", 0.0, 1.0, 0.5)
            
            # Genre descriptions
            genre_desc = {
                "funk": "Tight pocket, syncopated, emphasis on the one",
                "jazz": "Swing feel, laid-back, behind the beat",
                "rock": "Driving, on the beat, powerful",
                "hiphop": "Swung 16ths, lazy feel, boom bap",
                "edm": "Quantized, precise, four-on-the-floor",
                "latin": "Clave-based, polyrhythmic, energetic",
                "neosoul": "Drunk feel, elastic time, intimate",
            }
            
            st.info(f"**{genre.title()}:** {genre_desc.get(genre, '')}")
            
            if st.button("Apply Groove", type="primary"):
                with st.spinner(f"Applying {genre} groove..."):
                    try:
                        tmpdir = tempfile.mkdtemp(prefix="daiw_")
                        input_path = os.path.join(tmpdir, uploaded.name)
                        
                        with open(input_path, "wb") as f:
                            f.write(uploaded.getbuffer())
                        
                        output_path = os.path.join(tmpdir, f"{Path(uploaded.name).stem}_grooved.mid")
                        apply_groove(input_path, genre=genre, output=output_path, intensity=intensity)
                        
                        st.success("✨ Groove applied!")
                        
                        with open(output_path, "rb") as f:
                            st.download_button(
                                "📥 Download Grooved MIDI",
                                data=f.read(),
                                file_name=f"{Path(uploaded.name).stem}_{genre}.mid",
                                mime="audio/midi",
                                type="primary",
                                use_container_width=True,
                            )
                        
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    with tab2:
        st.markdown("### Extract Groove DNA")
        
        uploaded = st.file_uploader("Upload reference MIDI", type=["mid", "midi"], key="groove_extract")
        
        if uploaded:
            if st.button("Extract Groove", type="primary"):
                with st.spinner("Extracting groove DNA..."):
                    try:
                        tmpdir = tempfile.mkdtemp(prefix="daiw_")
                        input_path = os.path.join(tmpdir, uploaded.name)
                        
                        with open(input_path, "wb") as f:
                            f.write(uploaded.getbuffer())
                        
                        groove = extract_groove(input_path)
                        
                        st.success("✨ Groove extracted!")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            render_stat_box(f"{groove.timing_stats['mean_deviation_ms']:.1f}", "Timing (ms)", "")
                        with col2:
                            render_stat_box(f"{groove.swing_factor:.2f}", "Swing", "")
                        with col3:
                            render_stat_box(f"{groove.velocity_stats['std']:.1f}", "Dynamics", "")
                        
                        groove_json = json.dumps(groove.to_dict(), indent=2)
                        st.download_button(
                            "📥 Save Groove DNA",
                            data=groove_json,
                            file_name="groove_dna.json",
                            mime="application/json",
                            use_container_width=True,
                        )
                        
                    except Exception as e:
                        st.error(f"Error: {e}")


# =============================================================================
# RULE BREAKING PAGE
# =============================================================================

def render_rule_breaking():
    """Render rule breaking catalog and education."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📚</div>
        <h1 style="margin-bottom: 0.5rem;">Rule Breaking</h1>
        <p style="color: var(--text-secondary); font-size: 1.1rem;">
            Learn to break rules intentionally · Every deviation needs justification
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(229, 62, 62, 0.1) 0%, rgba(237, 137, 54, 0.1) 100%);
        border: 1px solid rgba(229, 62, 62, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    ">
        <div style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">
            ⚠️ The Cardinal Rule
        </div>
        <div style="color: var(--text-secondary);">
            Every rule break must have an <strong>emotional justification</strong>. 
            Breaking rules without intention is just sloppiness. 
            Breaking rules <em>with</em> intention is art.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Rule categories
    categories = {
        "🎹 Harmony": [
            ("HARMONY_AvoidTonicResolution", "Never resolve to the tonic", "Creates perpetual yearning, unfinished feeling", "grief, longing"),
            ("HARMONY_ModalInterchange", "Borrow chords from parallel modes", "Bittersweet color, emotional complexity", "nostalgia, tenderness"),
            ("HARMONY_ParallelMovement", "Move all voices in parallel", "Medieval/haunting quality, loss of independence", "dissociation, awe"),
            ("HARMONY_UnresolvedSeventh", "Leave seventh chords unresolved", "Sophisticated tension, jazz ambiguity", "confusion, longing"),
        ],
        "🥁 Rhythm": [
            ("RHYTHM_ConstantDisplacement", "Shift beats off the grid", "Anxiety, unease, intoxication", "fear, confusion"),
            ("RHYTHM_TempoFluctuation", "Allow tempo to breathe", "Organic, human, intimate", "tenderness, grief"),
            ("RHYTHM_PolymetricConflict", "Layer conflicting time signatures", "Disorientation, complexity", "confusion, rage"),
        ],
        "🎚️ Production": [
            ("PRODUCTION_PitchImperfection", "Allow pitch drift and wobble", "Emotional honesty, vulnerability", "grief, tenderness"),
            ("PRODUCTION_ExcessiveMud", "Don't clean the low end", "Claustrophobia, weight, heaviness", "grief, dissociation"),
            ("PRODUCTION_BuriedVocals", "Push vocals behind instruments", "Dissociation, distance, overwhelm", "dissociation, fear"),
        ],
        "🎼 Arrangement": [
            ("ARRANGEMENT_SparseToPoint", "Leave uncomfortable space", "Vulnerability, isolation, exposure", "grief, fear"),
            ("ARRANGEMENT_ExtremeContrast", "Jarring dynamic shifts", "Emotional whiplash, surprise", "rage, awe"),
            ("ARRANGEMENT_NoResolution", "End without closure", "Unfinished, life continues", "grief, confusion"),
        ],
    }
    
    for category, rules in categories.items():
        with st.expander(category, expanded=False):
            for rule_id, name, effect, emotions in rules:
                st.markdown(f"""
                <div style="
                    background: var(--bg-tertiary);
                    border-radius: 12px;
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-left: 3px solid #667eea;
                ">
                    <div style="font-weight: 600; color: var(--text-primary); font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;">
                        {rule_id}
                    </div>
                    <div style="color: var(--text-primary); margin: 0.5rem 0;">
                        {name}
                    </div>
                    <div style="color: var(--text-secondary); font-size: 0.9rem;">
                        <strong>Effect:</strong> {effect}
                    </div>
                    <div style="color: var(--text-muted); font-size: 0.8rem; margin-top: 0.25rem;">
                        Best for: {emotions}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    render_divider()
    
    # Suggestion tool
    st.markdown("### 💡 Get Suggestions")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        emotion_input = st.text_input(
            "What emotion are you working with?",
            placeholder="grief, rage, nostalgia, fear...",
        )
    
    with col2:
        if st.button("Get Suggestions", type="primary"):
            if emotion_input:
                suggestions = suggest_rule_break(emotion_input)
                
                if suggestions:
                    st.markdown("#### Suggested Rules to Break")
                    for sug in suggestions[:4]:
                        st.markdown(f"""
                        <div style="
                            background: var(--bg-tertiary);
                            border-radius: 12px;
                            padding: 1rem;
                            margin: 0.5rem 0;
                        ">
                            <div style="font-weight: 600; color: #667eea;">{sug['rule']}</div>
                            <div style="color: var(--text-secondary); margin-top: 0.25rem;">{sug['effect']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No specific suggestions for that emotion. Try: grief, rage, fear, nostalgia, defiance")


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "🏠  Home"
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Route to appropriate page
    if selected_page == "🏠  Home":
        render_home()
    elif selected_page == "💫  EMIDI Studio":
        render_emidi_studio()
    elif selected_page == "🎭  Wound & Healing":
        render_wound_healing()
    elif selected_page == "📝  Intent Builder":
        render_intent_builder()
    elif selected_page == "🎹  Harmony Lab":
        render_harmony_lab()
    elif selected_page == "🎸  Guitar FX Lab":
        render_guitar_fx_lab()
    elif selected_page == "📊  Analysis":
        render_analysis()
    elif selected_page == "🥁  Groove Engine":
        render_groove_engine()
    elif selected_page == "📚  Rule Breaking":
        render_rule_breaking()


if __name__ == "__main__":
    main()
