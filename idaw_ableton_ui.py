"""
iDAW - intelligent Digital Audio Workspace
===========================================
Ableton-Style Interface

Version: 1.0.02

Integrates with:
- Logic Pro X
- MeldaProduction  
- Vital
- User Sample Library (Google Drive)

Run with: streamlit run idaw_ableton_ui.py

Requirements:
    pip install streamlit music21 mido numpy
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional
import json

# Version
VERSION = "1.0.02"

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Try to import library integration
try:
    from idaw_library_integration import (
        iDAWLibraryIntegration,
        LibraryScanner,
        InstrumentSelector,
        EMOTION_TO_INSTRUMENTS,
    )
    LIBRARY_INTEGRATION_AVAILABLE = True
except ImportError:
    LIBRARY_INTEGRATION_AVAILABLE = False

try:
    from idaw_complete_pipeline import (
        InterrogationEngine, 
        get_parameters_for_state,
        StructureGenerator,
        HarmonyEngine,
        MelodyEngine,
        GrooveEngine,
        MIDIBuilder,
        PostProcessor,
        EMOTIONAL_PRESETS,
        EmotionalState,
        MusicalParameters,
        TimingFeel,
        RuleBreakCode,
        Mode,
        SongSection,
    )
    PIPELINE_AVAILABLE = True
except ImportError:
    PIPELINE_AVAILABLE = False

# ============================================================================
# PAGE CONFIG - Dark Theme Like Ableton
# ============================================================================
st.set_page_config(
    page_title=f"iDAW v{VERSION}", 
    page_icon="🎹", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ABLETON-STYLE CSS
# ============================================================================
st.markdown("""
<style>
    /* Dark theme base */
    .stApp {
        background-color: #1e1e1e;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Top toolbar */
    .toolbar {
        background: linear-gradient(180deg, #3d3d3d 0%, #2d2d2d 100%);
        border-bottom: 1px solid #1a1a1a;
        padding: 8px 15px;
        display: flex;
        align-items: center;
        gap: 20px;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        height: 45px;
    }
    
    .toolbar-logo {
        font-size: 18px;
        font-weight: bold;
        color: #ff9500;
        letter-spacing: 2px;
    }
    
    .toolbar-version {
        font-size: 10px;
        color: #888;
    }
    
    /* Transport controls */
    .transport {
        display: flex;
        gap: 5px;
        align-items: center;
    }
    
    .transport-btn {
        background: #4a4a4a;
        border: none;
        border-radius: 3px;
        color: #ccc;
        padding: 5px 12px;
        cursor: pointer;
        font-size: 14px;
    }
    
    .transport-btn:hover {
        background: #5a5a5a;
    }
    
    .transport-btn.active {
        background: #ff9500;
        color: #000;
    }
    
    /* BPM/Key display */
    .tempo-display {
        background: #2a2a2a;
        border: 1px solid #3a3a3a;
        border-radius: 3px;
        padding: 4px 10px;
        color: #ff9500;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        font-weight: bold;
    }
    
    /* Track headers (left sidebar) */
    .track-header {
        background: linear-gradient(90deg, #2d2d2d 0%, #252525 100%);
        border-bottom: 1px solid #1a1a1a;
        padding: 8px 10px;
        display: flex;
        align-items: center;
        gap: 8px;
        height: 60px;
    }
    
    .track-color {
        width: 4px;
        height: 40px;
        border-radius: 2px;
    }
    
    .track-name {
        color: #ffffff;
        font-size: 13px;
        font-weight: 600;
    }
    
    .track-arm {
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: #3a3a3a;
        border: 1px solid #4a4a4a;
    }
    
    .track-arm.armed {
        background: #ff3b30;
        border-color: #ff3b30;
    }
    
    /* Clip grid / Arrangement view */
    .arrangement {
        background: #1a1a1a;
        min-height: 400px;
        position: relative;
        overflow-x: auto;
    }
    
    /* HIGH CONTRAST TEXT FIXES */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .stMarkdown h3 {
        color: #ff9500 !important;
        font-weight: bold !important;
    }
    
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #e0e0e0 !important;
    }
    
    label, .stSelectbox label, .stSlider label, .stTextInput label, .stTextArea label {
        color: #cccccc !important;
    }
    
    /* Section headers */
    .stMarkdown h3::before {
        color: #ff9500;
    }
    
    .clip {
        background: linear-gradient(180deg, #5a7a5a 0%, #4a6a4a 100%);
        border-radius: 3px;
        padding: 4px 8px;
        margin: 2px;
        color: #fff;
        font-size: 11px;
        display: inline-block;
        cursor: pointer;
        border-left: 3px solid #7a9a7a;
    }
    
    .clip.drums {
        background: linear-gradient(180deg, #7a5a5a 0%, #6a4a4a 100%);
        border-left-color: #9a7a7a;
    }
    
    .clip.bass {
        background: linear-gradient(180deg, #5a5a7a 0%, #4a4a6a 100%);
        border-left-color: #7a7a9a;
    }
    
    .clip.melody {
        background: linear-gradient(180deg, #7a7a5a 0%, #6a6a4a 100%);
        border-left-color: #9a9a7a;
    }
    
    .clip.pad {
        background: linear-gradient(180deg, #5a7a7a 0%, #4a6a6a 100%);
        border-left-color: #7a9a9a;
    }
    
    /* Timeline ruler */
    .timeline {
        background: #252525;
        height: 25px;
        border-bottom: 1px solid #1a1a1a;
        display: flex;
        align-items: center;
        padding-left: 200px;
    }
    
    .bar-marker {
        color: #aaaaaa;
        font-size: 11px;
        width: 80px;
        text-align: center;
    }
    
    /* Browser panel (right side) */
    .browser {
        background: #252525;
        border-left: 1px solid #1a1a1a;
        padding: 10px;
        height: 100%;
    }
    
    .browser-header {
        color: #ff9500 !important;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    
    .browser-item {
        color: #e0e0e0;
        font-size: 12px;
        padding: 5px 8px;
        cursor: pointer;
        border-radius: 3px;
    }
    
    .browser-item:hover {
        background: #3a3a3a;
    }
    
    .browser-item.selected {
        background: #ff9500;
        color: #000;
    }
    
    /* Device chain / Detail view (bottom) */
    .device-chain {
        background: linear-gradient(180deg, #2d2d2d 0%, #252525 100%);
        border-top: 1px solid #3a3a3a;
        padding: 15px;
        min-height: 200px;
    }
    
    .device {
        background: #1e1e1e;
        border: 1px solid #3a3a3a;
        border-radius: 5px;
        padding: 10px;
        display: inline-block;
        margin-right: 10px;
        min-width: 150px;
    }
    
    .device-title {
        color: #ff9500;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    
    .knob-row {
        display: flex;
        gap: 15px;
        flex-wrap: wrap;
    }
    
    .knob {
        text-align: center;
    }
    
    .knob-dial {
        width: 40px;
        height: 40px;
        background: radial-gradient(circle, #4a4a4a 0%, #2a2a2a 100%);
        border-radius: 50%;
        border: 2px solid #5a5a5a;
        margin: 0 auto 5px;
        position: relative;
    }
    
    .knob-dial::after {
        content: '';
        position: absolute;
        width: 2px;
        height: 12px;
        background: #ff9500;
        top: 5px;
        left: 50%;
        transform: translateX(-50%);
        border-radius: 1px;
    }
    
    .knob-label {
        color: #bbbbbb;
        font-size: 10px;
        text-transform: uppercase;
    }
    
    .knob-value {
        color: #ffffff;
        font-size: 11px;
        font-family: 'Courier New', monospace;
    }
    
    /* Meter */
    .meter {
        width: 8px;
        height: 100px;
        background: #1a1a1a;
        border-radius: 2px;
        position: relative;
        overflow: hidden;
    }
    
    .meter-fill {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(180deg, #ff3b30 0%, #ff9500 20%, #30d158 50%);
        border-radius: 2px;
    }
    
    /* Emotional state display */
    .emotion-display {
        background: #1e1e1e;
        border: 1px solid #3a3a3a;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .emotion-primary {
        color: #ff9500;
        font-size: 24px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .emotion-secondary {
        color: #bbbbbb;
        font-size: 13px;
        margin-top: 5px;
    }
    
    /* Section markers */
    .section-marker {
        background: #ff9500;
        color: #000;
        font-size: 10px;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 2px;
        display: inline-block;
        margin-right: 5px;
    }
    
    /* Custom button styles */
    .stButton > button {
        background: #4a4a4a !important;
        color: #ccc !important;
        border: 1px solid #5a5a5a !important;
        border-radius: 3px !important;
    }
    
    .stButton > button:hover {
        background: #5a5a5a !important;
        border-color: #6a6a6a !important;
    }
    
    /* Primary action button */
    .generate-btn > button {
        background: #ff9500 !important;
        color: #000 !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: #ff9500 !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: #2a2a2a !important;
        color: #ccc !important;
        border: 1px solid #3a3a3a !important;
    }
    
    /* Metric styling */
    .stMetric {
        background: #2a2a2a;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #3a3a3a;
    }
    
    .stMetric label {
        color: #888 !important;
    }
    
    .stMetric > div {
        color: #ff9500 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'playing' not in st.session_state:
    st.session_state.playing = False
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'bpm' not in st.session_state:
    st.session_state.bpm = 82
if 'key' not in st.session_state:
    st.session_state.key = "F"
if 'tracks' not in st.session_state:
    st.session_state.tracks = []
if 'emotion' not in st.session_state:
    st.session_state.emotion = "neutral"
if 'generated' not in st.session_state:
    st.session_state.generated = False

# ============================================================================
# TOOLBAR
# ============================================================================
st.markdown(f"""
<div class="toolbar">
    <span class="toolbar-logo">iDAW</span>
    <span class="toolbar-version">v{VERSION}</span>
    <div style="flex-grow: 1;"></div>
    <div class="tempo-display">{st.session_state.bpm} BPM</div>
    <div class="tempo-display">{st.session_state.key}</div>
    <div style="flex-grow: 1;"></div>
</div>
<div style="height: 60px;"></div>
""", unsafe_allow_html=True)

# ============================================================================
# MAIN LAYOUT - Three columns like Ableton
# ============================================================================
col_browser, col_main, col_detail = st.columns([1, 4, 1.5])

# ============================================================================
# LEFT - BROWSER / PRESETS
# ============================================================================
with col_browser:
    st.markdown('<div class="browser-header">EMOTIONAL PRESETS</div>', unsafe_allow_html=True)
    
    preset_options = ["(interrogate)", "grief", "anxiety", "nostalgia", "anger", "calm", "hope", "intimacy", "defiance"]
    selected_preset = st.radio(
        "Preset",
        preset_options,
        label_visibility="collapsed",
        key="preset_select"
    )
    
    if selected_preset != "(interrogate)":
        st.session_state.emotion = selected_preset
    
    st.markdown('<div class="browser-header" style="margin-top:20px;">RULE BREAKS</div>', unsafe_allow_html=True)
    
    rule_breaks = {
        "Non-Resolution": st.checkbox("Non-Resolution", value=True, help="End unresolved (grief)"),
        "Modal Interchange": st.checkbox("Modal Interchange", help="Bittersweet"),
        "Parallel Motion": st.checkbox("Parallel Motion", help="Power/defiance"),
        "Tempo Drift": st.checkbox("Tempo Drift", help="Intimacy/rubato"),
    }
    
    st.markdown('<div class="browser-header" style="margin-top:20px;">GROOVE STYLE</div>', unsafe_allow_html=True)
    
    groove_style = st.selectbox(
        "Pattern",
        ["sparse", "basic", "boom_bap", "four_on_floor"],
        label_visibility="collapsed"
    )
    
    # ============================================================================
    # INSTRUMENT LIBRARIES
    # ============================================================================
    st.markdown('<div class="browser-header" style="margin-top:20px;">🎹 INSTRUMENTS</div>', unsafe_allow_html=True)
    
    if LIBRARY_INTEGRATION_AVAILABLE:
        # Show scan button instead of auto-scanning
        if 'libraries_scanned' not in st.session_state:
            st.session_state.libraries_scanned = False
            st.session_state.library_status = {}
        
        if not st.session_state.libraries_scanned:
            if st.button("🔍 Scan Libraries", key="scan_libs"):
                try:
                    integration = iDAWLibraryIntegration()
                    st.session_state.library_status = integration.get_available_libraries()
                    st.session_state.libraries_scanned = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Scan failed: {e}")
        else:
            # Show library status
            lib_status = st.session_state.library_status
            
            for lib_name, available in lib_status.items():
                icon = "✓" if available else "✗"
                color = "#30d158" if available else "#666"
                display_name = {
                    "logic_pro": "Logic Pro X",
                    "melda": "MeldaProduction",
                    "vital": "Vital",
                    "user_samples": "Your Samples"
                }.get(lib_name, lib_name)
                st.markdown(f'<span style="color:{color}">{icon}</span> {display_name}', unsafe_allow_html=True)
            
            # Rescan button
            if st.button("🔄 Rescan", key="rescan_libs"):
                st.session_state.libraries_scanned = False
                st.rerun()
        
        # Instrument source preference
        st.markdown('<div class="browser-header" style="margin-top:15px;">SOURCE</div>', unsafe_allow_html=True)
        instrument_source = st.selectbox(
            "Prefer",
            ["Auto", "Logic Pro", "Vital", "MeldaProduction", "User Samples"],
            label_visibility="collapsed",
            key="instrument_source"
        )
    else:
        st.markdown('<span style="color:#666">Library integration not loaded</span>', unsafe_allow_html=True)
        instrument_source = "Auto"

# ============================================================================
# CENTER - ARRANGEMENT VIEW
# ============================================================================
with col_main:
    # Transport bar
    transport_col1, transport_col2, transport_col3, transport_col4 = st.columns([1, 1, 1, 3])
    
    with transport_col1:
        if st.button("⏮️ REW"):
            pass
    with transport_col2:
        play_label = "⏹️ STOP" if st.session_state.playing else "▶️ PLAY"
        if st.button(play_label):
            st.session_state.playing = not st.session_state.playing
    with transport_col3:
        rec_label = "🔴 REC" if not st.session_state.recording else "⏺️ STOP"
        if st.button(rec_label):
            st.session_state.recording = not st.session_state.recording
    with transport_col4:
        st.session_state.bpm = st.number_input("BPM", 40, 200, st.session_state.bpm, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Timeline
    st.markdown("""
    <div class="timeline">
        <span class="bar-marker">1</span>
        <span class="bar-marker">5</span>
        <span class="bar-marker">9</span>
        <span class="bar-marker">13</span>
        <span class="bar-marker">17</span>
        <span class="bar-marker">21</span>
        <span class="bar-marker">25</span>
        <span class="bar-marker">29</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Track lanes
    st.markdown("### 🎹 Arrangement View")
    
    # If generated, show tracks
    if st.session_state.generated and st.session_state.tracks:
        for track in st.session_state.tracks:
            track_col1, track_col2 = st.columns([1, 5])
            
            with track_col1:
                color_map = {
                    "drums": "#9a7a7a",
                    "bass": "#7a7a9a",
                    "melody": "#9a9a7a",
                    "pad": "#7a9a9a",
                    "chords": "#7a9a7a"
                }
                color = color_map.get(track['name'].lower(), "#5a7a5a")
                st.markdown(f"""
                <div class="track-header">
                    <div class="track-color" style="background: {color};"></div>
                    <span class="track-name">{track['name'].upper()}</span>
                    <div class="track-arm"></div>
                </div>
                """, unsafe_allow_html=True)
            
            with track_col2:
                # Show clips for each section
                clips_html = ""
                for section in track.get('sections', []):
                    clip_class = track['name'].lower()
                    clips_html += f'<span class="clip {clip_class}">{section["name"]} ({section["bars"]} bars)</span>'
                
                st.markdown(f'<div style="padding: 10px; background: #1a1a1a; min-height: 50px;">{clips_html}</div>', unsafe_allow_html=True)
    else:
        # Empty state
        st.markdown("""
        <div style="background: #1a1a1a; min-height: 200px; display: flex; align-items: center; justify-content: center; color: #aaaaaa; border-radius: 5px;">
            <div style="text-align: center;">
                <div style="font-size: 48px; margin-bottom: 10px;">🎵</div>
                <div style="font-size: 14px;">Interrogate your emotion to generate tracks</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================================================
    # INTERROGATION SECTION
    # ============================================================================
    st.markdown("### 🎤 Interrogation Engine")
    
    interrog_col1, interrog_col2 = st.columns(2)
    
    with interrog_col1:
        st.markdown("**Phase 0: Core Wound**")
        core_wound = st.text_area(
            "What happened?",
            placeholder="The raw event - be specific",
            height=80,
            key="core_wound"
        )
        
        core_longing = st.text_input(
            "What do you wish you could feel?",
            placeholder="The transformation you seek",
            key="core_longing"
        )
    
    with interrog_col2:
        st.markdown("**Phase 1: Emotional Intent**")
        vernacular_input = st.text_area(
            "Describe the sound (vernacular):",
            placeholder="e.g., 'slow, fat, laid back, lo-fi bedroom feel'",
            height=80,
            key="vernacular"
        )
        
        vulnerability = st.slider("Vulnerability", 1, 10, 7, key="vuln_slider")
    
    # Generate button
    st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
    if st.button("🎵 GENERATE", use_container_width=True, type="primary"):
        if PIPELINE_AVAILABLE:
            with st.spinner("Interrogating emotional state..."):
                # Build input
                full_input = vernacular_input or ""
                if selected_preset != "(interrogate)":
                    full_input = f"{selected_preset} {full_input}"
                if core_wound:
                    full_input += f" about {core_wound}"
                
                # Interrogate
                engine = InterrogationEngine()
                state = engine.quick_interrogate(full_input)
                state.vulnerability = vulnerability / 10.0
                
                # Get parameters
                params = get_parameters_for_state(state)
                params.tempo_suggested = st.session_state.bpm
                params.key_signature = st.session_state.key
                
                # Apply rule breaks
                if rule_breaks.get("Non-Resolution"):
                    params.rule_breaks.append(RuleBreakCode.STRUCTURE_NonResolution)
                if rule_breaks.get("Modal Interchange"):
                    params.rule_breaks.append(RuleBreakCode.HARMONY_ModalInterchange)
                
                # Generate structure
                struct_gen = StructureGenerator()
                structure = struct_gen.generate(params, state)
                total_bars = sum(s.bars for s in structure)
                
                # Generate music
                harmony = HarmonyEngine(params)
                progression = harmony.generate_progression(total_bars, state.primary_emotion)
                
                melody_engine = MelodyEngine(params, harmony)
                melody = melody_engine.generate(progression, total_bars)
                
                groove = GrooveEngine(params)
                drums = groove.generate_drums(total_bars, groove_style)
                
                # Build MIDI
                builder = MIDIBuilder(bpm=params.tempo_suggested)
                builder.add_track("melody", melody)
                builder.add_track("drums", drums)
                
                # Save
                output_dir = Path.home() / "Music" / "iDAW_Output"
                output_dir.mkdir(parents=True, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                midi_path = output_dir / f"iDAW_{timestamp}_{state.primary_emotion}.mid"
                builder.save(midi_path)
                
                # ============================================
                # INSTRUMENT LIBRARY INTEGRATION
                # ============================================
                instrument_selections = {}
                if LIBRARY_INTEGRATION_AVAILABLE:
                    try:
                        integration = iDAWLibraryIntegration()
                        integration.scan_libraries()
                        
                        # Select instruments based on emotion
                        instrument_selections = integration.select_instruments(
                            state.primary_emotion, 
                            track_type="full"
                        )
                        
                        # Export Logic Pro project files
                        export_files = integration.export_for_logic(
                            midi_path,
                            instrument_selections,
                            state.primary_emotion,
                            params.tempo_suggested
                        )
                        
                        st.session_state.export_files = export_files
                        st.session_state.instrument_selections = {
                            k: {
                                "category": v.category.value,
                                "source": v.source,
                                "preset": v.preset_path,
                                "samples": v.sample_paths[:5]
                            }
                            for k, v in instrument_selections.items()
                        }
                    except Exception as e:
                        st.warning(f"Library integration: {e}")
                
                # Update session state
                st.session_state.emotion = state.primary_emotion
                st.session_state.generated = True
                st.session_state.midi_path = str(midi_path)
                st.session_state.tracks = [
                    {
                        "name": "Melody",
                        "notes": len(melody),
                        "sections": [{"name": s.name, "bars": s.bars} for s in structure],
                        "instrument": instrument_selections.get("lead", {})
                    },
                    {
                        "name": "Drums", 
                        "notes": len(drums),
                        "sections": [{"name": s.name, "bars": s.bars} for s in structure],
                        "instrument": instrument_selections.get("drums", {})
                    },
                    {
                        "name": "Pad",
                        "notes": 0,
                        "sections": [{"name": s.name, "bars": s.bars} for s in structure],
                        "instrument": instrument_selections.get("pad", {})
                    },
                    {
                        "name": "Bass",
                        "notes": 0,
                        "sections": [{"name": s.name, "bars": s.bars} for s in structure],
                        "instrument": instrument_selections.get("bass", {})
                    }
                ]
                st.session_state.structure = structure
                st.session_state.params = params
                
                st.success(f"✓ Generated: {midi_path.name}")
                st.rerun()
        else:
            st.error("Pipeline not available. Check imports.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# RIGHT - DETAIL / DEVICE VIEW
# ============================================================================
with col_detail:
    st.markdown('<div class="browser-header">EMOTIONAL STATE</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="emotion-display">
        <div class="emotion-primary">{st.session_state.emotion.upper()}</div>
        <div class="emotion-secondary">Vulnerability: {vulnerability}/10</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="browser-header">PARAMETERS</div>', unsafe_allow_html=True)
    
    # Key selector
    st.session_state.key = st.selectbox(
        "Key",
        ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"],
        index=5,
        key="key_select"
    )
    
    # Knob-style parameters
    humanize = st.slider("Humanize", 0.0, 0.5, 0.2, key="humanize")
    dissonance = st.slider("Dissonance", 0.0, 1.0, 0.3, key="dissonance")
    lofi = st.slider("Lo-Fi", 0.0, 0.6, 0.3, key="lofi")
    
    timing_feel = st.select_slider(
        "Pocket",
        ["ahead", "on", "behind"],
        value="behind",
        key="pocket"
    )
    
    st.markdown('<div class="browser-header" style="margin-top:20px;">OUTPUT</div>', unsafe_allow_html=True)
    
    if st.session_state.generated and hasattr(st.session_state, 'midi_path'):
        midi_path = Path(st.session_state.midi_path)
        if midi_path.exists():
            with open(midi_path, "rb") as f:
                st.download_button(
                    "📥 Download MIDI",
                    f,
                    file_name=midi_path.name,
                    mime="audio/midi",
                    use_container_width=True
                )
            st.caption(f"Saved: {midi_path.name}")
    
    # Structure display
    if st.session_state.generated and hasattr(st.session_state, 'structure'):
        st.markdown('<div class="browser-header" style="margin-top:20px;">STRUCTURE</div>', unsafe_allow_html=True)
        for section in st.session_state.structure:
            st.markdown(f'<span class="section-marker">{section.name.upper()}</span> {section.bars} bars', unsafe_allow_html=True)
    
    # ============================================================================
    # INSTRUMENT ASSIGNMENTS
    # ============================================================================
    if st.session_state.generated and hasattr(st.session_state, 'instrument_selections'):
        st.markdown('<div class="browser-header" style="margin-top:20px;">🎹 INSTRUMENTS</div>', unsafe_allow_html=True)
        
        for track_name, info in st.session_state.instrument_selections.items():
            source_icons = {
                "logic_pro": "🍎",
                "vital": "💎", 
                "melda": "🔷",
                "user_samples": "📁"
            }
            icon = source_icons.get(info.get("source", ""), "🎵")
            
            st.markdown(f"**{icon} {track_name.title()}**")
            st.markdown(f"<small style='color:#888'>{info.get('category', 'unknown')}</small>", unsafe_allow_html=True)
            
            if info.get("preset"):
                preset_name = Path(info["preset"]).stem[:20]
                st.markdown(f"<small style='color:#ff9500'>→ {preset_name}</small>", unsafe_allow_html=True)
            
            if info.get("samples"):
                st.markdown(f"<small style='color:#666'>{len(info['samples'])} samples</small>", unsafe_allow_html=True)
    
    # Export files for Logic Pro
    if st.session_state.generated and hasattr(st.session_state, 'export_files'):
        st.markdown('<div class="browser-header" style="margin-top:20px;">📦 LOGIC PRO</div>', unsafe_allow_html=True)
        
        export_files = st.session_state.export_files
        
        if "project" in export_files:
            project_path = export_files["project"]
            if project_path.exists():
                with open(project_path, "rb") as f:
                    st.download_button(
                        "📄 Project JSON",
                        f,
                        file_name=project_path.name,
                        mime="application/json",
                        use_container_width=True
                    )
        
        if "readme" in export_files:
            readme_path = export_files["readme"]
            if readme_path.exists():
                with open(readme_path, "rb") as f:
                    st.download_button(
                        "📝 Import Guide",
                        f,
                        file_name=readme_path.name,
                        mime="text/markdown",
                        use_container_width=True
                    )

# ============================================================================
# BOTTOM - DEVICE CHAIN
# ============================================================================
st.markdown("---")
st.markdown("### 🎛️ Device Chain")

device_cols = st.columns(5)

with device_cols[0]:
    st.markdown("""
    <div class="device">
        <div class="device-title">Interrogator</div>
        <div class="knob-row">
            <div class="knob">
                <div class="knob-dial"></div>
                <div class="knob-label">Depth</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with device_cols[1]:
    st.markdown("""
    <div class="device">
        <div class="device-title">Harmony</div>
        <div class="knob-row">
            <div class="knob">
                <div class="knob-dial"></div>
                <div class="knob-label">Dissonance</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with device_cols[2]:
    st.markdown("""
    <div class="device">
        <div class="device-title">Groove</div>
        <div class="knob-row">
            <div class="knob">
                <div class="knob-dial"></div>
                <div class="knob-label">Swing</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with device_cols[3]:
    st.markdown("""
    <div class="device">
        <div class="device-title">Humanizer</div>
        <div class="knob-row">
            <div class="knob">
                <div class="knob-dial"></div>
                <div class="knob-label">Feel</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with device_cols[4]:
    st.markdown("""
    <div class="device">
        <div class="device-title">Lo-Fi</div>
        <div class="knob-row">
            <div class="knob">
                <div class="knob-dial"></div>
                <div class="knob-label">Degrade</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #555; font-size: 11px;">
    iDAW v{VERSION} — intelligent Digital Audio Workspace<br>
    <em>"Interrogate Before Generate"</em>
</div>
""", unsafe_allow_html=True)
