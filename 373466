# app.py
"""
DAiW Streamlit UI - Desktop-facing product interface.

Multi-page interface exposing the full music_brain API:
- Therapy Session (emotion → MIDI)
- Harmony Generator (intent-based and basic)
- Groove Tools (extract/apply)
- Chord Analysis (MIDI analysis, progression diagnosis)
- Intent-Based Generation (full intent schema)
- Humanization (drum humanization)
"""
import os
import tempfile
import json
from pathlib import Path
from typing import Optional

import streamlit as st

# Core imports
from music_brain.structure.comprehensive_engine import (
    TherapySession,
    render_plan_to_midi,
)
from music_brain.harmony import (
    HarmonyGenerator,
    HarmonyResult,
    generate_midi_from_harmony,
)
from music_brain.groove import extract_groove, apply_groove
from music_brain.structure import analyze_chords, detect_sections
from music_brain.structure.progression import diagnose_progression, generate_reharmonizations
from music_brain.session.intent_schema import (
    CompleteSongIntent,
    SongRoot,
    SongIntent,
    TechnicalConstraints,
    SystemDirective,
    suggest_rule_break,
    validate_intent,
    list_all_rules,
)
from music_brain.session.intent_processor import process_intent
from music_brain.groove import (
    humanize_midi_file,
    GrooveSettings,
    settings_from_preset,
    list_presets,
    get_preset,
)
from music_brain.chatbot.agent import ChatAgent, AgentConfig


def save_midi_download(midi_path: str, filename: str) -> None:
    """Helper to create download button for MIDI file."""
    try:
        with open(midi_path, "rb") as f:
            st.download_button(
                label=f"Download {filename}",
                data=f.read(),
                file_name=filename,
                mime="audio/midi",
            )
    except OSError:
        st.error(f"MIDI file could not be read: {midi_path}")


def page_therapy_session() -> None:
    """Therapy Session: Emotion → MIDI generation."""
    st.header("🎭 Therapy Session")
    st.caption("Tell me what hurts, and I'll translate it into music.")

    st.markdown("### 1. Tell me what hurts")

    default_text = "I feel dead inside because I chose safety over freedom."
    user_text = st.text_area(
        "What is hurting you right now?",
        value=default_text,
        height=140,
    )

    st.markdown("### 2. Set your state")

    col1, col2 = st.columns(2)

    with col1:
        motivation = st.slider(
            "Motivation (1 = sketch, 10 = full piece)",
            min_value=1,
            max_value=10,
            value=7,
        )

    with col2:
        chaos_1_10 = st.slider(
            "Chaos tolerance (1-10)",
            min_value=1,
            max_value=10,
            value=5,
            help="Higher = more unstable tempo and structure.",
        )

    st.markdown("### 3. Generate session")

    if st.button("Generate MIDI session", type="primary"):
        if not user_text.strip():
            st.error("I need at least one sentence to work with.")
            return

        with st.spinner("Processing your emotions..."):
            session = TherapySession()
            affect = session.process_core_input(user_text)
            session.set_scales(motivation, chaos_1_10 / 10.0)
            plan = session.generate_plan()

        st.subheader("Analysis")
        if session.state.affect_result:
            st.write(f"**Primary affect:** `{affect}`")
            if session.state.affect_result.secondary:
                st.write(
                    f"**Secondary undertone:** "
                    f"`{session.state.affect_result.secondary}`"
                )
            st.write(
                f"**Affect intensity:** "
                f"`{session.state.affect_result.intensity:.2f}`"
            )

        st.subheader("Generation directive")
        st.write(f"- Mode: **{plan.root_note} {plan.mode}**")
        st.write(f"- Tempo: **{plan.tempo_bpm} BPM**")
        st.write(f"- Length: **{plan.length_bars} bars**")
        st.write(f"- Progression: `{' - '.join(plan.chord_symbols)}`")
        st.write(f"- Complexity (chaos): `{plan.complexity:.2f}`")

        with st.spinner("Rendering MIDI..."):
            tmpdir = tempfile.mkdtemp(prefix="daiw_")
            midi_path = os.path.join(tmpdir, "daiw_therapy_session.mid")
            midi_path = render_plan_to_midi(plan, midi_path)

        st.success("MIDI generated.")
        save_midi_download(midi_path, "daiw_therapy_session.mid")


def page_harmony_generator() -> None:
    """Harmony Generator: Intent-based and basic progression generation."""
    st.header("🎹 Harmony Generator")
    st.caption("Generate chord progressions from intent or basic parameters.")

    tab1, tab2 = st.tabs(["From Intent", "Basic Progression"])

    with tab1:
        st.subheader("Generate from Intent File")
        intent_file = st.file_uploader(
            "Upload intent JSON file",
            type=["json"],
            help="Create an intent file using: daiw intent new"
        )

        if intent_file:
            try:
                intent_data = json.load(intent_file)
                intent = CompleteSongIntent.from_dict(intent_data)
                
                st.json(intent_data)
                
                if st.button("Generate Harmony from Intent", type="primary"):
                    with st.spinner("Generating harmony..."):
                        generator = HarmonyGenerator()
                        harmony = generator.generate_from_intent(intent)
                    
                    display_harmony_result(harmony)
                    
                    if st.button("Generate MIDI"):
                        with st.spinner("Rendering MIDI..."):
                            tmpdir = tempfile.mkdtemp(prefix="daiw_")
                            midi_path = os.path.join(tmpdir, "harmony_from_intent.mid")
                            tempo = getattr(intent.technical_constraints, 'technical_tempo_range', (82, 120))[0]
                            generate_midi_from_harmony(harmony, midi_path, tempo_bpm=tempo)
                            save_midi_download(midi_path, "harmony_from_intent.mid")
            except Exception as e:
                st.error(f"Error loading intent: {e}")

    with tab2:
        st.subheader("Basic Progression Generator")
        
        col1, col2 = st.columns(2)
        with col1:
            key = st.selectbox("Key", ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"], index=5)
            mode = st.selectbox("Mode", ["major", "minor", "dorian", "phrygian", "lydian", "mixolydian"], index=0)
        
        with col2:
            pattern = st.text_input(
                "Roman numeral pattern",
                value="I-V-vi-IV",
                help="e.g., I-V-vi-IV, I-vi-IV-V, ii-V-I"
            )
            tempo = st.number_input("Tempo (BPM)", min_value=60, max_value=200, value=82)
        
        if st.button("Generate Progression", type="primary"):
            with st.spinner("Generating harmony..."):
                generator = HarmonyGenerator()
                harmony = generator.generate_basic_progression(
                    key=key,
                    mode=mode,
                    pattern=pattern
                )
            
            display_harmony_result(harmony)
            
            if st.button("Generate MIDI"):
                with st.spinner("Rendering MIDI..."):
                    tmpdir = tempfile.mkdtemp(prefix="daiw_")
                    midi_path = os.path.join(tmpdir, "basic_progression.mid")
                    generate_midi_from_harmony(harmony, midi_path, tempo_bpm=tempo)
                    save_midi_download(midi_path, "basic_progression.mid")


def display_harmony_result(harmony: HarmonyResult) -> None:
    """Display harmony result in a formatted way."""
    st.subheader("Generated Harmony")
    st.write(f"**Key:** {harmony.key} {harmony.mode}")
    st.write(f"**Progression:** {' - '.join(harmony.chords)}")
    
    if harmony.rule_break_applied:
        st.write(f"**Rule break:** {harmony.rule_break_applied}")
        st.write(f"**Justification:** {harmony.emotional_justification}")
    
    with st.expander("View Voicings"):
        for i, voicing in enumerate(harmony.voicings):
            st.write(f"**{voicing.root}** (Roman: {voicing.roman_numeral})")
            st.write(f"  Notes: {voicing.notes}")
            st.write(f"  Duration: {voicing.duration_beats} beats")
            if voicing.emotional_function:
                st.write(f"  Function: {voicing.emotional_function}")


def page_groove_tools() -> None:
    """Groove Tools: Extract and apply groove patterns."""
    st.header("🥁 Groove Tools")
    st.caption("Extract groove from MIDI or apply genre templates.")

    tab1, tab2 = st.tabs(["Extract Groove", "Apply Groove"])

    with tab1:
        st.subheader("Extract Groove from MIDI")
        midi_file = st.file_uploader(
            "Upload MIDI file",
            type=["mid", "midi"],
            help="Extract timing and velocity patterns from a MIDI file"
        )

        if midi_file:
            if st.button("Extract Groove", type="primary"):
                with st.spinner("Analyzing groove..."):
                    # Save uploaded file temporarily
                    tmpdir = tempfile.mkdtemp(prefix="daiw_")
                    input_path = os.path.join(tmpdir, midi_file.name)
                    with open(input_path, "wb") as f:
                        f.write(midi_file.getbuffer())
                    
                    groove = extract_groove(input_path)
                    
                    st.subheader("Groove Analysis")
                    st.write(f"**Timing deviation:** {groove.timing_stats['mean_deviation_ms']:.1f}ms avg")
                    st.write(f"**Velocity range:** {groove.velocity_stats['min']}-{groove.velocity_stats['max']}")
                    st.write(f"**Swing factor:** {groove.swing_factor:.2f}")
                    
                    # Save groove as JSON
                    groove_json = json.dumps(groove.to_dict(), indent=2)
                    st.download_button(
                        label="Download Groove JSON",
                        data=groove_json,
                        file_name="extracted_groove.json",
                        mime="application/json",
                    )

    with tab2:
        st.subheader("Apply Groove Template")
        midi_file = st.file_uploader(
            "Upload MIDI file to process",
            type=["mid", "midi"],
            key="apply_groove_upload"
        )
        
        genre = st.selectbox(
            "Genre template",
            ["funk", "jazz", "rock", "hiphop", "edm", "latin"],
            index=0
        )
        
        intensity = st.slider(
            "Groove intensity",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1
        )

        if midi_file and st.button("Apply Groove", type="primary"):
            with st.spinner("Applying groove..."):
                tmpdir = tempfile.mkdtemp(prefix="daiw_")
                input_path = os.path.join(tmpdir, midi_file.name)
                output_path = os.path.join(tmpdir, f"{Path(midi_file.name).stem}_grooved.mid")
                
                with open(input_path, "wb") as f:
                    f.write(midi_file.getbuffer())
                
                apply_groove(input_path, genre=genre, output=output_path, intensity=intensity)
                save_midi_download(output_path, f"{Path(midi_file.name).stem}_grooved.mid")


def page_chord_analysis() -> None:
    """Chord Analysis: Analyze MIDI files and diagnose progressions."""
    st.header("🎼 Chord Analysis")
    st.caption("Analyze chord progressions in MIDI files or diagnose text progressions.")

    tab1, tab2 = st.tabs(["MIDI Analysis", "Progression Diagnosis"])

    with tab1:
        st.subheader("Analyze MIDI File")
        midi_file = st.file_uploader(
            "Upload MIDI file",
            type=["mid", "midi"],
            help="Analyze chord progression and sections in a MIDI file"
        )

        if midi_file:
            analyze_chords_option = st.checkbox("Analyze chords", value=True)
            analyze_sections_option = st.checkbox("Detect sections", value=False)

            if st.button("Analyze", type="primary"):
                with st.spinner("Analyzing..."):
                    tmpdir = tempfile.mkdtemp(prefix="daiw_")
                    input_path = os.path.join(tmpdir, midi_file.name)
                    with open(input_path, "wb") as f:
                        f.write(midi_file.getbuffer())
                    
                    if analyze_chords_option:
                        progression = analyze_chords(input_path)
                        st.subheader("Chord Analysis")
                        st.write(f"**Key:** {progression.key}")
                        st.write(f"**Progression:** {' - '.join(progression.chords)}")
                        st.write(f"**Roman numerals:** {' - '.join(progression.roman_numerals)}")
                        
                        if progression.borrowed_chords:
                            st.write("**Borrowed chords:**")
                            for chord, source in progression.borrowed_chords.items():
                                st.write(f"  - {chord} ← borrowed from {source}")
                    
                    if analyze_sections_option:
                        sections = detect_sections(input_path)
                        st.subheader("Section Analysis")
                        for section in sections:
                            st.write(f"**{section.name}:** bars {section.start_bar}-{section.end_bar} (energy: {section.energy:.2f})")

    with tab2:
        st.subheader("Diagnose Chord Progression")
        progression_text = st.text_input(
            "Chord progression",
            value="F-C-Am-Dm",
            help="Enter chords separated by hyphens, e.g., F-C-Am-Dm"
        )
        
        if st.button("Diagnose", type="primary"):
            with st.spinner("Analyzing progression..."):
                diagnosis = diagnose_progression(progression_text)
                
                st.subheader("Diagnosis")
                st.write(f"**Key estimate:** {diagnosis['key']}")
                st.write(f"**Mode:** {diagnosis['mode']}")
                
                if diagnosis['issues']:
                    st.warning("Potential issues:")
                    for issue in diagnosis['issues']:
                        st.write(f"  ⚠ {issue}")
                else:
                    st.success("✓ No obvious issues detected")
                
                if diagnosis['suggestions']:
                    st.info("Suggestions:")
                    for suggestion in diagnosis['suggestions']:
                        st.write(f"  → {suggestion}")
        
        st.divider()
        st.subheader("Reharmonization Suggestions")
        style = st.selectbox(
            "Style",
            ["jazz", "pop", "rnb", "classical", "experimental"],
            index=0
        )
        count = st.number_input("Number of suggestions", min_value=1, max_value=10, value=3)
        
        if st.button("Generate Reharmonizations", type="primary"):
            with st.spinner("Generating suggestions..."):
                suggestions = generate_reharmonizations(progression_text, style=style, count=count)
                
                st.subheader("Reharmonization Suggestions")
                for i, suggestion in enumerate(suggestions, 1):
                    st.write(f"**{i}. {' - '.join(suggestion['chords'])}**")
                    st.write(f"   Technique: {suggestion['technique']}")
                    st.write(f"   Mood shift: {suggestion['mood']}")


def page_intent_generation() -> None:
    """Intent-Based Generation: Full intent schema support."""
    st.header("🎯 Intent-Based Generation")
    st.caption("Generate complete musical elements from emotional intent.")

    tab1, tab2, tab3 = st.tabs(["Create Intent", "Process Intent", "Rule Suggestions"])

    with tab1:
        st.subheader("Create New Intent Template")
        title = st.text_input("Song title", value="Untitled Song")
        
        if st.button("Generate Template", type="primary"):
            intent = CompleteSongIntent(
                title=title,
                song_root=SongRoot(
                    core_event="[What happened?]",
                    core_resistance="[What holds you back?]",
                    core_longing="[What do you want to feel?]",
                    core_stakes="Personal",
                    core_transformation="[How should you feel at the end?]",
                ),
                song_intent=SongIntent(
                    mood_primary="[Primary emotion]",
                    mood_secondary_tension=0.5,
                    imagery_texture="[Visual/tactile quality]",
                    vulnerability_scale="Medium",
                    narrative_arc="Climb-to-Climax",
                ),
                technical_constraints=TechnicalConstraints(
                    technical_genre="[Genre]",
                    technical_tempo_range=(80, 120),
                    technical_key="F",
                    technical_mode="major",
                    technical_groove_feel="Organic/Breathing",
                    technical_rule_to_break="",
                    rule_breaking_justification="",
                ),
                system_directive=SystemDirective(
                    output_target="Chord progression",
                    output_feedback_loop="Harmony",
                ),
            )
            
            intent_json = json.dumps(intent.to_dict(), indent=2)
            st.text_area("Intent JSON", value=intent_json, height=400)
            st.download_button(
                label="Download Intent Template",
                data=intent_json,
                file_name="song_intent.json",
                mime="application/json",
            )

    with tab2:
        st.subheader("Process Intent File")
        intent_file = st.file_uploader(
            "Upload intent JSON file",
            type=["json"],
            key="process_intent_upload"
        )

        if intent_file:
            try:
                intent_data = json.load(intent_file)
                intent = CompleteSongIntent.from_dict(intent_data)
                
                # Validate
                issues = validate_intent(intent)
                if issues:
                    st.warning("Validation issues found:")
                    for issue in issues:
                        st.write(f"  - {issue}")
                else:
                    st.success("✓ Intent is valid!")
                
                if st.button("Process Intent", type="primary"):
                    with st.spinner("Processing intent and generating elements..."):
                        result = process_intent(intent)
                    
                    st.subheader("Generated Elements")
                    
                    # Harmony
                    harmony = result['harmony']
                    st.write(f"**Harmony** ({harmony.rule_broken})")
                    st.write(f"  Progression: {' - '.join(harmony.chords)}")
                    st.write(f"  Roman: {' - '.join(harmony.roman_numerals)}")
                    st.write(f"  Effect: {harmony.rule_effect}")
                    
                    # Groove
                    groove = result['groove']
                    st.write(f"**Groove** ({groove.rule_broken})")
                    st.write(f"  Pattern: {groove.pattern_name}")
                    st.write(f"  Tempo: {groove.tempo_bpm} BPM")
                    st.write(f"  Effect: {groove.rule_effect}")
                    
                    # Arrangement
                    arr = result['arrangement']
                    st.write(f"**Arrangement** ({arr.rule_broken})")
                    for section in arr.sections:
                        st.write(f"  {section['name']}: {section['bars']} bars @ {section['energy']:.0%} energy")
                    
                    # Production
                    prod = result['production']
                    st.write(f"**Production** ({prod.rule_broken})")
                    st.write(f"  Vocal: {prod.vocal_treatment}")
                    for note in prod.eq_notes[:2]:
                        st.write(f"  EQ: {note}")
                    
                    # Save output
                    output_data = {
                        "intent_summary": result['intent_summary'],
                        "harmony": {
                            "chords": harmony.chords,
                            "roman_numerals": harmony.roman_numerals,
                            "rule_broken": harmony.rule_broken,
                            "effect": harmony.rule_effect,
                        },
                        "groove": {
                            "pattern": groove.pattern_name,
                            "tempo": groove.tempo_bpm,
                            "swing": groove.swing_factor,
                        },
                        "arrangement": {
                            "sections": arr.sections,
                            "dynamic_arc": arr.dynamic_arc,
                        },
                        "production": {
                            "vocal_treatment": prod.vocal_treatment,
                            "eq_notes": prod.eq_notes,
                            "dynamics_notes": prod.dynamics_notes,
                        },
                    }
                    output_json = json.dumps(output_data, indent=2)
                    st.download_button(
                        label="Download Generated Elements",
                        data=output_json,
                        file_name="generated_elements.json",
                        mime="application/json",
                    )
            except Exception as e:
                st.error(f"Error processing intent: {e}")

    with tab3:
        st.subheader("Rule-Breaking Suggestions")
        emotion = st.text_input(
            "Target emotion",
            value="grief",
            help="e.g., grief, anger, nostalgia, defiance, dissociation"
        )
        
        if st.button("Get Suggestions", type="primary"):
            suggestions = suggest_rule_break(emotion)
            
            if not suggestions:
                st.info(f"No specific suggestions for '{emotion}'. Try: grief, anger, nostalgia, defiance, dissociation")
            else:
                st.subheader(f"Suggested rules to break for '{emotion}'")
                for i, sug in enumerate(suggestions, 1):
                    st.write(f"**{i}. {sug['rule']}**")
                    st.write(f"   What: {sug['description']}")
                    st.write(f"   Effect: {sug['effect']}")
                    st.write(f"   Use when: {sug['use_when']}")
                    st.divider()
        
        if st.button("List All Rules"):
            rules = list_all_rules()
            st.subheader("All Available Rule-Breaking Options")
            for category, rule_list in rules.items():
                st.write(f"**{category}:**")
                for rule in rule_list:
                    st.write(f"  - {rule}")


def page_humanization() -> None:
    """Humanization: Drum humanization tools."""
    st.header("🥁 Drum Humanization")
    st.caption("Apply human feel to drum MIDI tracks (Drunken Drummer).")

    midi_file = st.file_uploader(
        "Upload drum MIDI file",
        type=["mid", "midi"],
        help="MIDI file with drum track (typically channel 9/10)"
    )

    if midi_file:
        method = st.radio(
            "Humanization method",
            ["Preset", "Style", "Manual"],
            index=1
        )

        if method == "Preset":
            presets = list_presets()
            preset_name = st.selectbox("Emotional preset", sorted(presets))
            if preset_name:
                preset_data = get_preset(preset_name)
                st.caption(preset_data.get("description", ""))
                settings = settings_from_preset(preset_name)
                complexity = settings.complexity
                vulnerability = settings.vulnerability

        elif method == "Style":
            style = st.selectbox(
                "Style",
                ["tight", "natural", "loose", "drunk"],
                index=1
            )
            style_map = {
                "tight": (0.1, 0.2),
                "natural": (0.4, 0.5),
                "loose": (0.6, 0.6),
                "drunk": (0.9, 0.8),
            }
            complexity, vulnerability = style_map[style]
            settings = GrooveSettings(complexity=complexity, vulnerability=vulnerability)

        else:  # Manual
            complexity = st.slider(
                "Complexity (timing chaos)",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.1
            )
            vulnerability = st.slider(
                "Vulnerability (dynamic fragility)",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.1
            )
            settings = GrooveSettings(complexity=complexity, vulnerability=vulnerability)

        enable_ghost_notes = st.checkbox("Enable ghost notes", value=True)
        settings.enable_ghost_notes = enable_ghost_notes

        channel = st.number_input(
            "Drum channel (MIDI channel 10 = 9)",
            min_value=0,
            max_value=15,
            value=9
        )

        if st.button("Humanize Drums", type="primary"):
            with st.spinner("Applying humanization..."):
                tmpdir = tempfile.mkdtemp(prefix="daiw_")
                input_path = os.path.join(tmpdir, midi_file.name)
                output_path = os.path.join(tmpdir, f"{Path(midi_file.name).stem}_humanized.mid")
                
                with open(input_path, "wb") as f:
                    f.write(midi_file.getbuffer())
                
                result_path = humanize_midi_file(
                    input_path=input_path,
                    output_path=output_path,
                    complexity=complexity,
                    vulnerability=vulnerability,
                    drum_channel=channel,
                    settings=settings,
                )
                
                st.success("Humanization applied!")
                st.write(f"**Complexity:** {complexity:.2f} (timing chaos)")
                st.write(f"**Vulnerability:** {vulnerability:.2f} (dynamic fragility)")
                st.write(f"**Ghost notes:** {'enabled' if settings.enable_ghost_notes else 'disabled'}")
                
                save_midi_download(result_path, f"{Path(midi_file.name).stem}_humanized.mid")


def page_chatbot() -> None:
    """Offline chatbot integration."""
    st.header("💬 Offline Chatbot")
    st.caption("Talk to DAiW without an internet connection. Provide your local LLM model path.")

    if "chat_agent" not in st.session_state:
        st.session_state.chat_agent = None
    if "chat_model_path" not in st.session_state:
        st.session_state.chat_model_path = str(Path("~/Models/local-llm.gguf").expanduser())
    if "chat_persona" not in st.session_state:
        st.session_state.chat_persona = "You are DAiW's offline companion. Give musical advice based on intent."

    model_path = st.text_input(
        "Local model path (.gguf/.ggml)",
        value=st.session_state.chat_model_path,
    )
    persona = st.text_area(
        "Persona / system prompt",
        value=st.session_state.chat_persona,
        height=100,
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Initialize Agent"):
            st.session_state.chat_model_path = model_path
            st.session_state.chat_persona = persona
            config = AgentConfig(
                model_path=Path(model_path).expanduser(),
                system_prompt=persona,
            )
            st.session_state.chat_agent = ChatAgent(config)
            st.success("Chat agent initialized.")
    with col2:
        st.info("Note: LLM runner is currently a placeholder. Plug in llama.cpp / GPT4All to enable real responses.")

    agent: Optional[ChatAgent] = st.session_state.chat_agent
    if not agent:
        st.warning("Initialize the agent to start chatting.")
        return

    st.divider()
    st.subheader("Conversation")

    for msg in agent.history[1:]:
        role = msg.get("role", "assistant")
        with st.chat_message("user" if role == "user" else "assistant"):
            st.write(msg.get("content", ""))

    user_prompt = st.chat_input("Ask DAiW something...")
    if user_prompt:
        with st.chat_message("user"):
            st.write(user_prompt)
        reply = agent.chat(user_prompt)
        with st.chat_message("assistant"):
            st.write(reply)


def main() -> None:
    st.set_page_config(
        page_title="DAiW - Digital Audio Intimate Workstation",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.title("DAiW")
    st.sidebar.caption("Digital Audio Intimate Workstation")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Creative companion, not a factory.**")

    page = st.sidebar.radio(
        "Navigation",
        [
            "🎭 Therapy Session",
            "🎹 Harmony Generator",
            "🥁 Groove Tools",
            "🎼 Chord Analysis",
            "🎯 Intent Generation",
            "🥁 Humanization",
            "💬 Chatbot",
        ],
    )

    st.title(page.split(" ", 1)[1] if " " in page else page)

    if page == "🎭 Therapy Session":
        page_therapy_session()
    elif page == "🎹 Harmony Generator":
        page_harmony_generator()
    elif page == "🥁 Groove Tools":
        page_groove_tools()
    elif page == "🎼 Chord Analysis":
        page_chord_analysis()
    elif page == "🎯 Intent Generation":
        page_intent_generation()
    elif page == "🥁 Humanization":
        page_humanization()
    elif page == "💬 Chatbot":
        page_chatbot()


if __name__ == "__main__":
    main()
