"""
iDAW Desktop Application - Streamlit-based GUI.

Run with: streamlit run music_brain/desktop/app.py
Or: python -m music_brain.desktop.app
"""

import sys
import json
from pathlib import Path
from typing import Optional

# Check for streamlit
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

from .project import Project, ProjectManager, ProjectIntent
from .timeline import TimelineRenderer, render_arrangement_timeline, SECTION_COLORS


def check_dependencies():
    """Check if required dependencies are available."""
    if not STREAMLIT_AVAILABLE:
        print("Error: Streamlit is required for the desktop app.")
        print("Install with: pip install streamlit")
        sys.exit(1)


# Intent wizard phase configurations
PHASE_CONFIG = {
    0: {
        "title": "Phase 0: Core Wound/Desire",
        "description": "What emotional truth is at the heart of this song?",
        "fields": ["core_event", "core_resistance", "core_longing"],
    },
    1: {
        "title": "Phase 1: Emotional Intent",
        "description": "How should this song feel?",
        "fields": ["mood_primary", "mood_secondary", "vulnerability", "narrative_arc"],
    },
    2: {
        "title": "Phase 2: Technical Constraints",
        "description": "What are the musical parameters?",
        "fields": ["genre", "key", "tempo", "chord_progression", "rule_to_break"],
    },
}

MOODS = [
    "grief", "anger", "joy", "nostalgia", "longing", "anxiety",
    "hope", "peace", "despair", "love", "heartbreak", "defiance",
    "melancholy", "euphoria", "tension", "release", "acceptance"
]

GENRES = ["pop", "rock", "folk", "lofi", "edm", "jazz", "hiphop", "rnb", "indie"]

KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
        "Am", "A#m", "Bm", "Cm", "C#m", "Dm", "D#m", "Em", "Fm", "F#m", "Gm", "G#m"]

NARRATIVE_ARCS = [
    ("transformation", "Journey of change"),
    ("cyclical", "Repeating patterns"),
    ("descent", "Falling into darkness"),
    ("ascent", "Rising to triumph"),
    ("static", "Sustained contemplation"),
    ("climactic", "Building to peak"),
]

RULES_TO_BREAK = [
    ("", "None"),
    ("HARMONY_ModalInterchange", "Modal Interchange - Borrow from parallel modes"),
    ("HARMONY_AvoidTonicResolution", "Avoid Resolution - Never fully resolve"),
    ("HARMONY_ParallelMotion", "Parallel Motion - Break voice leading rules"),
    ("RHYTHM_ConstantDisplacement", "Constant Displacement - Off-beat emphasis"),
    ("PRODUCTION_PitchImperfection", "Pitch Imperfection - Leave vocal imperfections"),
    ("PRODUCTION_LoFiAesthetic", "Lo-Fi Aesthetic - Embrace degradation"),
    ("ARRANGEMENT_BuriedVocals", "Buried Vocals - Mix vocals low"),
    ("TEXTURE_FrequencyMasking", "Frequency Masking - Intentional mud"),
]


def init_session_state():
    """Initialize Streamlit session state."""
    if "project" not in st.session_state:
        st.session_state.project = Project(title="New Song")

    if "project_manager" not in st.session_state:
        st.session_state.project_manager = ProjectManager()

    if "current_view" not in st.session_state:
        st.session_state.current_view = "intent"  # intent, arrangement, export

    if "generation_result" not in st.session_state:
        st.session_state.generation_result = None


def render_sidebar():
    """Render the sidebar with project management."""
    st.sidebar.title("iDAW")
    st.sidebar.caption("Intelligent Digital Audio Workstation")

    # Project section
    st.sidebar.header("Project")

    # Title
    new_title = st.sidebar.text_input(
        "Title",
        value=st.session_state.project.title,
        key="project_title"
    )
    if new_title != st.session_state.project.title:
        st.session_state.project.title = new_title

    # Project actions
    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("New", use_container_width=True):
            st.session_state.project = Project(title="New Song")
            st.session_state.generation_result = None
            st.rerun()

    with col2:
        if st.button("Save", use_container_width=True):
            path = st.session_state.project_manager.save_project(st.session_state.project)
            st.sidebar.success(f"Saved to {path}")

    # Load project
    st.sidebar.subheader("Recent Projects")
    recent = st.session_state.project_manager.get_recent(5)

    if recent:
        for proj in recent:
            if st.sidebar.button(f"📄 {proj['title']}", key=f"load_{proj['id']}"):
                try:
                    st.session_state.project = st.session_state.project_manager.load_project(proj['path'])
                    st.session_state.generation_result = None
                    st.rerun()
                except Exception as e:
                    st.sidebar.error(f"Error loading: {e}")
    else:
        st.sidebar.caption("No recent projects")

    # Navigation
    st.sidebar.header("Navigation")
    view = st.sidebar.radio(
        "View",
        ["Intent Wizard", "Arrangement", "Export"],
        key="nav_view"
    )

    view_map = {"Intent Wizard": "intent", "Arrangement": "arrangement", "Export": "export"}
    st.session_state.current_view = view_map[view]

    # Status
    st.sidebar.header("Status")
    project = st.session_state.project

    if project.intent.is_complete():
        st.sidebar.success("✓ Intent complete")
    else:
        st.sidebar.warning("○ Intent incomplete")

    if project.is_generated:
        st.sidebar.success("✓ Arrangement generated")
    else:
        st.sidebar.info("○ Not generated yet")


def render_phase_0():
    """Render Phase 0: Core Wound/Desire."""
    st.header("Phase 0: Core Wound/Desire")
    st.caption("What emotional truth is at the heart of this song?")

    project = st.session_state.project

    project.intent.core_event = st.text_area(
        "Core Event",
        value=project.intent.core_event,
        placeholder="What happened? What's the trigger for this song?",
        help="The specific event or realization that sparked this song",
        height=100,
    )

    project.intent.core_resistance = st.text_area(
        "Core Resistance",
        value=project.intent.core_resistance,
        placeholder="What holds you back? What are you fighting against?",
        help="The internal or external force creating conflict",
        height=100,
    )

    project.intent.core_longing = st.text_area(
        "Core Longing",
        value=project.intent.core_longing,
        placeholder="What do you really want to feel by the end?",
        help="The desired emotional resolution or transformation",
        height=100,
    )


def render_phase_1():
    """Render Phase 1: Emotional Intent."""
    st.header("Phase 1: Emotional Intent")
    st.caption("How should this song feel?")

    project = st.session_state.project

    col1, col2 = st.columns(2)

    with col1:
        project.intent.mood_primary = st.selectbox(
            "Primary Mood",
            options=[""] + MOODS,
            index=MOODS.index(project.intent.mood_primary) + 1 if project.intent.mood_primary in MOODS else 0,
            help="The dominant emotional tone",
        )

        project.intent.mood_secondary = st.selectbox(
            "Secondary Mood (Optional)",
            options=[""] + MOODS,
            index=MOODS.index(project.intent.mood_secondary) + 1 if project.intent.mood_secondary in MOODS else 0,
            help="A contrasting or supporting emotion",
        )

    with col2:
        project.intent.vulnerability = st.slider(
            "Vulnerability Scale",
            min_value=0.0,
            max_value=1.0,
            value=project.intent.vulnerability,
            step=0.1,
            help="0 = Guarded, 1 = Completely exposed",
        )

        narrative_options = [label for _, label in NARRATIVE_ARCS]
        narrative_values = [value for value, _ in NARRATIVE_ARCS]

        current_idx = narrative_values.index(project.intent.narrative_arc) if project.intent.narrative_arc in narrative_values else 0

        selected_label = st.selectbox(
            "Narrative Arc",
            options=narrative_options,
            index=current_idx,
            help="The emotional journey structure",
        )
        project.intent.narrative_arc = narrative_values[narrative_options.index(selected_label)]


def render_phase_2():
    """Render Phase 2: Technical Constraints."""
    st.header("Phase 2: Technical Constraints")
    st.caption("What are the musical parameters?")

    project = st.session_state.project

    col1, col2, col3 = st.columns(3)

    with col1:
        project.intent.genre = st.selectbox(
            "Genre",
            options=GENRES,
            index=GENRES.index(project.intent.genre) if project.intent.genre in GENRES else 0,
        )

    with col2:
        project.intent.key = st.selectbox(
            "Key",
            options=KEYS,
            index=KEYS.index(project.intent.key) if project.intent.key in KEYS else 0,
        )

    with col3:
        project.intent.tempo = st.number_input(
            "Tempo (BPM)",
            min_value=40,
            max_value=200,
            value=int(project.intent.tempo),
            step=5,
        )

    # Chord progression
    chord_str = "-".join(project.intent.chord_progression) if project.intent.chord_progression else ""
    chord_input = st.text_input(
        "Chord Progression (Optional)",
        value=chord_str,
        placeholder="e.g., C-G-Am-F",
        help="Separate chords with dashes. Leave empty for auto-generation.",
    )

    if chord_input:
        project.intent.chord_progression = [c.strip() for c in chord_input.split("-") if c.strip()]
    else:
        project.intent.chord_progression = []

    # Rule breaking
    st.subheader("Rule Breaking (Optional)")

    rule_options = [label for _, label in RULES_TO_BREAK]
    rule_values = [value for value, _ in RULES_TO_BREAK]

    current_rule_idx = rule_values.index(project.intent.rule_to_break) if project.intent.rule_to_break in rule_values else 0

    selected_rule = st.selectbox(
        "Rule to Break",
        options=rule_options,
        index=current_rule_idx,
        help="Intentionally break a music theory 'rule' for emotional effect",
    )
    project.intent.rule_to_break = rule_values[rule_options.index(selected_rule)]

    if project.intent.rule_to_break:
        project.intent.rule_justification = st.text_area(
            "Why break this rule?",
            value=project.intent.rule_justification,
            placeholder="How does breaking this rule serve the emotional intent?",
            height=80,
        )


def render_intent_wizard():
    """Render the three-phase intent wizard."""
    project = st.session_state.project

    # Phase tabs
    tab0, tab1, tab2 = st.tabs(["Phase 0: Core", "Phase 1: Emotion", "Phase 2: Technical"])

    with tab0:
        render_phase_0()

    with tab1:
        render_phase_1()

    with tab2:
        render_phase_2()

    # Progress indicator
    st.divider()

    # Check completeness
    phase_complete = [
        bool(project.intent.core_event),
        bool(project.intent.mood_primary),
        bool(project.intent.genre and project.intent.key),
    ]

    cols = st.columns(4)
    for i, (complete, label) in enumerate(zip(phase_complete, ["Phase 0", "Phase 1", "Phase 2"])):
        with cols[i]:
            if complete:
                st.success(f"✓ {label}")
            else:
                st.warning(f"○ {label}")

    # Generate button
    with cols[3]:
        can_generate = all(phase_complete)

        if st.button(
            "Generate Arrangement",
            type="primary",
            disabled=not can_generate,
            use_container_width=True
        ):
            generate_arrangement()


def generate_arrangement():
    """Generate arrangement from current intent."""
    project = st.session_state.project

    with st.spinner("Generating arrangement..."):
        try:
            # Import arrangement module
            from music_brain.arrangement import generate_arrangement as gen_arr

            # Generate
            arrangement = gen_arr(
                title=project.title,
                genre=project.intent.genre,
                key=project.intent.key,
                tempo=project.intent.tempo,
                chord_progression=project.intent.chord_progression or None,
                mood=project.intent.mood_primary,
                vulnerability=project.intent.vulnerability,
                narrative_arc=project.intent.narrative_arc,
            )

            # Store result
            st.session_state.generation_result = arrangement

            # Update project
            project.set_arrangement({
                "sections": [s.to_dict() for s in arrangement.sections],
                "chord_progression": arrangement.chord_progression,
                "bass_lines": {k: v.to_dict() for k, v in arrangement.bass_lines.items()},
                "energy_arc": arrangement.energy_arc.to_dict(),
                "production_notes": arrangement.production_notes,
                "total_bars": arrangement.total_bars,
            })

            st.success("Arrangement generated!")
            st.session_state.current_view = "arrangement"
            st.rerun()

        except Exception as e:
            st.error(f"Generation failed: {e}")


def render_arrangement_view():
    """Render the arrangement visualization."""
    st.header("Generated Arrangement")

    project = st.session_state.project
    result = st.session_state.generation_result

    if not result and not project.arrangement:
        st.info("No arrangement generated yet. Complete the Intent Wizard first.")
        return

    # Use stored arrangement if no live result
    if result:
        arrangement = result
    else:
        # Reconstruct from project data
        st.warning("Showing saved arrangement data")
        arrangement = None

    if arrangement:
        # Header info
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Genre", arrangement.genre.title())
        with col2:
            st.metric("Key", arrangement.key)
        with col3:
            st.metric("Tempo", f"{arrangement.tempo} BPM")
        with col4:
            st.metric("Bars", arrangement.total_bars)

        # Timeline visualization
        st.subheader("Timeline")

        # Create visual timeline
        timeline_html = ""
        for section in arrangement.sections:
            width_pct = (section.bars / arrangement.total_bars) * 100
            color = SECTION_COLORS.get(section.section_type.value, "#95A5A6")
            timeline_html += (
                f'<div style="display: inline-block; width: {width_pct}%; height: 50px; '
                f'background: {color}; text-align: center; color: white; '
                f'line-height: 50px; font-size: 11px; overflow: hidden;" '
                f'title="{section.name}: {section.bars} bars">'
                f'{section.section_type.value}'
                f'</div>'
            )

        st.markdown(
            f'<div style="border: 1px solid #ccc; border-radius: 4px; overflow: hidden;">{timeline_html}</div>',
            unsafe_allow_html=True
        )

        # Energy curve
        st.subheader("Energy Curve")
        energy_html = ""
        for section in arrangement.sections:
            width_pct = (section.bars / arrangement.total_bars) * 100
            height_pct = section.energy * 100
            color = SECTION_COLORS.get(section.section_type.value, "#95A5A6")
            energy_html += (
                f'<div style="display: inline-block; width: {width_pct}%; height: {height_pct}px; '
                f'background: {color}; vertical-align: bottom;"></div>'
            )

        st.markdown(
            f'<div style="border: 1px solid #ccc; border-radius: 4px; height: 100px; '
            f'display: flex; align-items: flex-end;">{energy_html}</div>',
            unsafe_allow_html=True
        )

        # Sections detail
        st.subheader("Sections")

        for section in arrangement.sections:
            with st.expander(f"{section.name} ({section.section_type.value}) - {section.bars} bars"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Start Bar:** {section.start_bar}")
                    st.write(f"**Energy:** {section.energy:.0%}")
                    st.write(f"**Bass Pattern:** {section.bass_pattern.value}")

                with col2:
                    chords = [c for c, _ in section.chords]
                    st.write(f"**Chords:** {' → '.join(chords)}")
                    st.write(f"**Instruments:** {', '.join(section.instruments[:4])}")

        # Chord progression
        st.subheader("Chord Progression")
        st.code(" - ".join(arrangement.chord_progression))

        # Production notes
        st.subheader("Production Notes")
        with st.expander("View Production Notes"):
            st.markdown(arrangement.production_notes)


def render_export_view():
    """Render the export options."""
    st.header("Export")

    project = st.session_state.project
    result = st.session_state.generation_result

    if not result and not project.arrangement:
        st.info("Generate an arrangement first before exporting.")
        return

    arrangement = result

    st.subheader("Export Options")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Arrangement JSON**")
        if st.button("Download Arrangement JSON"):
            json_data = arrangement.to_json()
            st.download_button(
                label="Download",
                data=json_data,
                file_name=f"{project.title.lower().replace(' ', '_')}_arrangement.json",
                mime="application/json"
            )

        st.write("**Production Notes**")
        if st.button("Download Production Notes"):
            st.download_button(
                label="Download",
                data=arrangement.production_notes,
                file_name=f"{project.title.lower().replace(' ', '_')}_production_notes.md",
                mime="text/markdown"
            )

    with col2:
        st.write("**Project File**")
        if st.button("Download Project (.idaw)"):
            project_json = project.to_json()
            st.download_button(
                label="Download",
                data=project_json,
                file_name=f"{project.title.lower().replace(' ', '_')}.idaw",
                mime="application/json"
            )

        st.write("**Summary**")
        if st.button("Download Summary"):
            summary = arrangement.describe()
            st.download_button(
                label="Download",
                data=summary,
                file_name=f"{project.title.lower().replace(' ', '_')}_summary.md",
                mime="text/markdown"
            )

    # Export history
    if project.exports:
        st.subheader("Export History")
        for export in project.exports[-5:]:
            st.text(f"{export['type']}: {export['path']} ({export['timestamp'][:10]})")


def main():
    """Main application entry point."""
    check_dependencies()

    # Page config
    st.set_page_config(
        page_title="iDAW - Intelligent Digital Audio Workstation",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS
    st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a2e;
        color: #eee;
    }
    .stSidebar {
        background-color: #16213e;
    }
    .stButton button {
        border-radius: 4px;
    }
    .stExpander {
        background-color: #0f3460;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize state
    init_session_state()

    # Render sidebar
    render_sidebar()

    # Main content
    st.title(f"🎵 {st.session_state.project.title}")

    # Route to current view
    if st.session_state.current_view == "intent":
        render_intent_wizard()
    elif st.session_state.current_view == "arrangement":
        render_arrangement_view()
    elif st.session_state.current_view == "export":
        render_export_view()


if __name__ == "__main__":
    main()
