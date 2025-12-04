"""
DAiW CLI - Command line interface for Music Brain toolkit

Usage:
    daiw extract <midi_file>                    Extract groove from MIDI
    daiw apply --genre <genre> <midi_file>      Apply groove template
    daiw analyze --chords <midi_file>           Analyze chord progression
    daiw diagnose <progression>                 Diagnose harmonic issues
    daiw reharm <progression> [--style <style>] Generate reharmonizations
    daiw teach <topic>                          Interactive teaching mode

    daiw intent new [--title <title>]           Create new intent template
    daiw intent process <file>                  Generate elements from intent
    daiw intent suggest <emotion>               Suggest rules to break
    daiw intent list                            List all rule-breaking options
    daiw intent validate <file>                 Validate intent file

    daiw arrange --genre <genre> [--key <key>]  Generate complete arrangement
    daiw bass <chords> --genre <genre>          Generate bass line
    daiw energy --mood <mood>                   Generate energy arc

    daiw app                                    Launch desktop GUI (requires streamlit)
    daiw server                                 Start DAW integration server
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional

# Lazy imports to speed up CLI startup
def get_groove_module():
    from music_brain.groove import extract_groove, apply_groove
    return extract_groove, apply_groove

def get_structure_module():
    from music_brain.structure import analyze_chords, detect_sections
    return analyze_chords, detect_sections

def get_session_module():
    from music_brain.session import RuleBreakingTeacher
    return RuleBreakingTeacher


def get_intent_module():
    from music_brain.session.intent_schema import (
        CompleteSongIntent, SongRoot, SongIntent, TechnicalConstraints,
        SystemDirective, suggest_rule_break, validate_intent, list_all_rules
    )
    from music_brain.session.intent_processor import IntentProcessor, process_intent
    return (CompleteSongIntent, SongRoot, SongIntent, TechnicalConstraints,
            SystemDirective, suggest_rule_break, validate_intent, list_all_rules,
            IntentProcessor, process_intent)


def get_arrangement_module():
    from music_brain.arrangement import (
        generate_arrangement,
        generate_complete_song,
        ArrangementGenerator,
        GeneratedArrangement,
        get_genre_template,
        GENRE_TEMPLATES,
    )
    return (generate_arrangement, generate_complete_song, ArrangementGenerator,
            GeneratedArrangement, get_genre_template, GENRE_TEMPLATES)


def get_bass_module():
    from music_brain.arrangement.bass_generator import (
        generate_bass_line,
        BassLine,
        BassPattern,
    )
    return generate_bass_line, BassLine, BassPattern


def get_energy_module():
    from music_brain.arrangement.energy_arc import (
        generate_energy_arc,
        EnergyArc,
        EmotionalJourney,
        describe_energy_arc,
        suggest_arc_for_intent,
    )
    return generate_energy_arc, EnergyArc, EmotionalJourney, describe_energy_arc, suggest_arc_for_intent


def cmd_extract(args):
    """Extract groove from MIDI file."""
    extract_groove, _ = get_groove_module()
    
    midi_path = Path(args.midi_file)
    if not midi_path.exists():
        print(f"Error: File not found: {midi_path}")
        return 1
    
    print(f"Extracting groove from: {midi_path}")
    groove = extract_groove(str(midi_path))
    
    output_path = midi_path.stem + "_groove.json"
    if args.output:
        output_path = args.output
    
    with open(output_path, 'w') as f:
        json.dump(groove.to_dict(), f, indent=2)
    
    print(f"Groove saved to: {output_path}")
    print(f"  Timing deviation: {groove.timing_stats['mean_deviation_ms']:.1f}ms avg")
    print(f"  Velocity range: {groove.velocity_stats['min']}-{groove.velocity_stats['max']}")
    print(f"  Swing factor: {groove.swing_factor:.2f}")
    return 0


def cmd_apply(args):
    """Apply groove template to MIDI file."""
    _, apply_groove = get_groove_module()
    
    midi_path = Path(args.midi_file)
    if not midi_path.exists():
        print(f"Error: File not found: {midi_path}")
        return 1
    
    print(f"Applying {args.genre} groove to: {midi_path}")
    
    output_path = args.output or f"{midi_path.stem}_grooved.mid"
    apply_groove(str(midi_path), genre=args.genre, output=output_path, intensity=args.intensity)
    
    print(f"Output saved to: {output_path}")
    return 0


def cmd_analyze(args):
    """Analyze chord progression in MIDI file."""
    analyze_chords, detect_sections = get_structure_module()
    
    midi_path = Path(args.midi_file)
    if not midi_path.exists():
        print(f"Error: File not found: {midi_path}")
        return 1
    
    if args.chords:
        print(f"Analyzing chords in: {midi_path}")
        progression = analyze_chords(str(midi_path))
        
        print("\n=== Chord Analysis ===")
        print(f"Key: {progression.key}")
        print(f"Progression: {' - '.join(progression.chords)}")
        print(f"Roman numerals: {' - '.join(progression.roman_numerals)}")
        
        if progression.borrowed_chords:
            print(f"\nBorrowed chords detected:")
            for chord, source in progression.borrowed_chords.items():
                print(f"  {chord} ← borrowed from {source}")
    
    if args.sections:
        print(f"\nDetecting sections in: {midi_path}")
        sections = detect_sections(str(midi_path))
        
        print("\n=== Section Analysis ===")
        for section in sections:
            print(f"  {section.name}: bars {section.start_bar}-{section.end_bar} (energy: {section.energy:.2f})")
    
    return 0


def cmd_diagnose(args):
    """Diagnose issues in a chord progression string."""
    from music_brain.structure.progression import diagnose_progression
    
    progression = args.progression
    print(f"Diagnosing: {progression}")
    
    diagnosis = diagnose_progression(progression)
    
    print("\n=== Harmonic Diagnosis ===")
    print(f"Key estimate: {diagnosis['key']}")
    print(f"Mode: {diagnosis['mode']}")
    
    if diagnosis['issues']:
        print("\nPotential issues:")
        for issue in diagnosis['issues']:
            print(f"  ⚠ {issue}")
    else:
        print("\n✓ No obvious issues detected")
    
    if diagnosis['suggestions']:
        print("\nSuggestions:")
        for suggestion in diagnosis['suggestions']:
            print(f"  → {suggestion}")
    
    return 0


def cmd_reharm(args):
    """Generate reharmonization suggestions."""
    from music_brain.structure.progression import generate_reharmonizations
    
    progression = args.progression
    style = args.style or "jazz"
    
    print(f"Reharmonizing: {progression}")
    print(f"Style: {style}")
    
    suggestions = generate_reharmonizations(progression, style=style, count=args.count)
    
    print("\n=== Reharmonization Suggestions ===")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {' - '.join(suggestion['chords'])}")
        print(f"   Technique: {suggestion['technique']}")
        print(f"   Mood shift: {suggestion['mood']}")
    
    return 0


def cmd_teach(args):
    """Interactive teaching mode."""
    RuleBreakingTeacher = get_session_module()
    
    topic = args.topic.lower().replace("-", "_").replace(" ", "_")
    
    valid_topics = [
        "rulebreaking", "rule_breaking", "borrowed", "borrowed_chords",
        "modal_mixture", "substitutions", "rhythm", "production"
    ]
    
    if topic not in valid_topics:
        print(f"Unknown topic: {args.topic}")
        print(f"Available topics: {', '.join(valid_topics)}")
        return 1
    
    teacher = RuleBreakingTeacher()
    
    if args.quick:
        # Quick single lesson
        teacher.quick_lesson(topic)
    else:
        # Interactive mode
        teacher.interactive_session(topic)
    
    return 0


def cmd_intent(args):
    """Handle intent-based song generation."""
    (CompleteSongIntent, SongRoot, SongIntent, TechnicalConstraints,
     SystemDirective, suggest_rule_break, validate_intent, list_all_rules,
     IntentProcessor, process_intent) = get_intent_module()
    
    if args.subcommand == 'new':
        # Create new intent from template
        print("Creating new song intent...")
        
        intent = CompleteSongIntent(
            title=args.title or "Untitled Song",
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
        
        output = args.output or "song_intent.json"
        intent.save(output)
        print(f"Template saved to: {output}")
        print("\nEdit the file to fill in your intent, then run:")
        print(f"  daiw intent process {output}")
    
    elif args.subcommand == 'process':
        # Process intent to generate elements
        if not args.file:
            print("Error: Please specify an intent file")
            return 1
        
        intent_path = Path(args.file)
        if not intent_path.exists():
            print(f"Error: File not found: {intent_path}")
            return 1
        
        print(f"Processing intent: {intent_path}")
        intent = CompleteSongIntent.load(str(intent_path))
        
        # Validate first
        issues = validate_intent(intent)
        if issues and not args.force:
            print("\n⚠️  Intent validation issues:")
            for issue in issues:
                print(f"  - {issue}")
            print("\nFix issues or use --force to proceed anyway")
            return 1
        
        # Process
        result = process_intent(intent)
        
        # Display results
        print("\n" + "=" * 60)
        print("🎵 GENERATED ELEMENTS")
        print("=" * 60)
        
        # Harmony
        harmony = result['harmony']
        print(f"\n📌 HARMONY ({harmony.rule_broken})")
        print(f"   Progression: {' - '.join(harmony.chords)}")
        print(f"   Roman: {' - '.join(harmony.roman_numerals)}")
        print(f"   Effect: {harmony.rule_effect}")
        
        # Groove
        groove = result['groove']
        print(f"\n📌 GROOVE ({groove.rule_broken})")
        print(f"   Pattern: {groove.pattern_name}")
        print(f"   Tempo: {groove.tempo_bpm} BPM")
        print(f"   Effect: {groove.rule_effect}")
        
        # Arrangement
        arr = result['arrangement']
        print(f"\n📌 ARRANGEMENT ({arr.rule_broken})")
        for section in arr.sections:
            print(f"   {section['name']}: {section['bars']} bars @ {section['energy']:.0%} energy")
        
        # Production
        prod = result['production']
        print(f"\n📌 PRODUCTION ({prod.rule_broken})")
        print(f"   Vocal: {prod.vocal_treatment}")
        for note in prod.eq_notes[:2]:
            print(f"   EQ: {note}")
        
        print("\n" + "=" * 60)
        
        # Save output if requested
        if args.output:
            import json
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
            with open(args.output, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"\nOutput saved to: {args.output}")
    
    elif args.subcommand == 'suggest':
        # Suggest rules to break based on emotion
        emotion = args.emotion
        suggestions = suggest_rule_break(emotion)
        
        print(f"\n🎯 Suggested rules to break for '{emotion}':\n")
        
        if not suggestions:
            print(f"  No specific suggestions for '{emotion}'")
            print("  Try: grief, anger, nostalgia, defiance, dissociation")
        else:
            for i, sug in enumerate(suggestions, 1):
                print(f"{i}. {sug['rule']}")
                print(f"   What: {sug['description']}")
                print(f"   Effect: {sug['effect']}")
                print(f"   Use when: {sug['use_when']}")
                print()
    
    elif args.subcommand == 'list':
        # List all available rules
        rules = list_all_rules()
        
        print("\n📋 Available Rule-Breaking Options:\n")
        for category, rule_list in rules.items():
            print(f"  {category}:")
            for rule in rule_list:
                print(f"    - {rule}")
            print()
    
    elif args.subcommand == 'validate':
        # Validate an intent file
        if not args.file:
            print("Error: Please specify an intent file")
            return 1
        
        intent_path = Path(args.file)
        if not intent_path.exists():
            print(f"Error: File not found: {intent_path}")
            return 1
        
        intent = CompleteSongIntent.load(str(intent_path))
        issues = validate_intent(intent)
        
        if issues:
            print("\n⚠️  Validation issues found:")
            for issue in issues:
                print(f"  - {issue}")
            return 1
        else:
            print("✅ Intent is valid!")
            return 0
    
    return 0


def cmd_arrange(args):
    """Generate complete arrangement."""
    (generate_arrangement, generate_complete_song, ArrangementGenerator,
     GeneratedArrangement, get_genre_template, GENRE_TEMPLATES) = get_arrangement_module()

    print(f"Generating {args.genre} arrangement...")
    print(f"Key: {args.key} | Tempo: {args.tempo} BPM | Mood: {args.mood}")

    # Parse chord progression if provided
    chord_progression = None
    if args.chords:
        chord_progression = [c.strip() for c in args.chords.split('-')]

    arrangement = generate_arrangement(
        title=args.title,
        genre=args.genre,
        key=args.key,
        tempo=args.tempo,
        chord_progression=chord_progression,
        mood=args.mood,
        vulnerability=args.vulnerability,
        narrative_arc=args.narrative,
    )

    print("\n" + "=" * 60)
    print("🎵 GENERATED ARRANGEMENT")
    print("=" * 60)
    print(f"\nTitle: {arrangement.title}")
    print(f"Genre: {arrangement.genre} | Key: {arrangement.key} | Tempo: {arrangement.tempo} BPM")
    print(f"Total: {arrangement.total_bars} bars")

    print("\n📋 STRUCTURE:")
    for section in arrangement.sections:
        chords_str = " → ".join([c for c, _ in section.chords[:4]])
        if len(section.chords) > 4:
            chords_str += " ..."
        print(f"  {section.name}: {section.bars} bars @ {section.energy:.0%} energy")
        print(f"    Chords: {chords_str}")
        print(f"    Instruments: {', '.join(section.instruments[:3])}")

    print("\n🎸 CHORD PROGRESSION:")
    print(f"  {' - '.join(arrangement.chord_progression)}")

    print("\n📈 ENERGY ARC:")
    print(f"  Journey: {arrangement.energy_arc.emotional_journey.value}")
    print(f"  Climax at bar {arrangement.energy_arc.get_climax_bar()}")

    # Save outputs
    if args.output:
        arrangement.save(args.output)
        print(f"\n✅ Arrangement saved to: {args.output}")

    if args.notes:
        with open(args.notes, 'w') as f:
            f.write(arrangement.production_notes)
        print(f"✅ Production notes saved to: {args.notes}")

    return 0


def cmd_bass(args):
    """Generate bass line from chord progression."""
    generate_bass_line, BassLine, BassPattern = get_bass_module()

    # Parse chord progression
    chords_str = args.chords
    chord_list = []

    for chord_part in chords_str.split('-'):
        chord_part = chord_part.strip()
        # Check for duration (e.g., "C:2" means C for 2 bars)
        if ':' in chord_part:
            chord, duration = chord_part.split(':')
            chord_list.append((chord.strip(), int(duration)))
        else:
            chord_list.append((chord_part, args.bars_per_chord))

    print(f"Generating {args.genre} bass line...")
    print(f"Chords: {chords_str}")

    bass_line = generate_bass_line(
        chords=chord_list,
        genre=args.genre,
        key=args.key,
        section_type=args.section,
        energy=args.energy,
    )

    print("\n" + "=" * 60)
    print("🎸 GENERATED BASS LINE")
    print("=" * 60)
    print(f"\nPattern: {bass_line.pattern.value}")
    print(f"Total bars: {bass_line.total_bars}")
    print(f"Total notes: {len(bass_line.notes)}")

    print("\n📋 NOTES (first 16):")
    for note in bass_line.notes[:16]:
        print(f"  Beat {note.start_beat:.1f}: MIDI {note.pitch} (vel: {note.velocity}, dur: {note.duration})")

    if len(bass_line.notes) > 16:
        print(f"  ... and {len(bass_line.notes) - 16} more notes")

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(bass_line.to_dict(), f, indent=2)
        print(f"\n✅ Bass line saved to: {args.output}")

    return 0


def cmd_energy(args):
    """Generate energy arc."""
    (generate_energy_arc, EnergyArc, EmotionalJourney,
     describe_energy_arc, suggest_arc_for_intent) = get_energy_module()

    print(f"Generating energy arc for mood: {args.mood}")

    # Suggest arc parameters from mood
    arc_type, journey, climax = suggest_arc_for_intent(
        mood=args.mood,
        vulnerability=args.vulnerability,
        narrative_arc=args.narrative,
    )

    arc = generate_energy_arc(
        total_bars=args.bars,
        arc_type=arc_type,
        emotional_journey=journey,
        climax_position=climax,
        min_energy=args.min_energy,
        max_energy=args.max_energy,
    )

    print("\n" + "=" * 60)
    print("📈 GENERATED ENERGY ARC")
    print("=" * 60)
    print(f"\n{describe_energy_arc(arc)}")

    print("\n📋 ENERGY CURVE (sampled):")
    sample_points = [0, 0.25, 0.5, 0.75, 1.0]
    for pos in sample_points:
        bar = int(pos * arc.total_bars)
        energy = arc.get_energy_at_position(pos)
        bar_graph = "█" * int(energy * 20) + "░" * (20 - int(energy * 20))
        print(f"  Bar {bar:3d} ({pos:.0%}): {bar_graph} {energy:.0%}")

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(arc.to_dict(), f, indent=2)
        print(f"\n✅ Energy arc saved to: {args.output}")

    return 0


def cmd_genres(args):
    """List available genres."""
    (_, _, _, _, get_genre_template, GENRE_TEMPLATES) = get_arrangement_module()

    print("\n📋 AVAILABLE GENRES:\n")
    for genre, template in GENRE_TEMPLATES.items():
        print(f"  {genre}:")
        print(f"    Name: {template.name}")
        print(f"    Tempo: {template.tempo_range[0]}-{template.tempo_range[1]} BPM")
        print(f"    Sections: {len(template.sections)} ({template.total_bars} bars)")
        print(f"    Description: {template.description}")
        print()

    return 0


def cmd_app(args):
    """Launch desktop GUI application."""
    try:
        import streamlit.web.cli as stcli
    except ImportError:
        print("Error: Streamlit is not installed.")
        print("Install with: pip install streamlit")
        print("Or install iDAW with: pip install -e '.[desktop]'")
        return 1

    # Find the app.py path
    from pathlib import Path
    app_path = Path(__file__).parent / "desktop" / "app.py"

    if not app_path.exists():
        print(f"Error: Desktop app not found at {app_path}")
        return 1

    print("Launching iDAW Desktop App...")
    print(f"App path: {app_path}")

    # Build streamlit arguments
    sys_argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.port", str(args.port),
        "--server.headless", "true" if args.headless else "false",
    ]

    if args.browser:
        sys_argv.extend(["--server.browser.serverAddress", "localhost"])

    # Run streamlit
    import sys
    sys.argv = sys_argv
    stcli.main()

    return 0


def cmd_server(args):
    """Start DAW integration server."""
    try:
        from music_brain.daw_server import DAWServer, start_server
    except ImportError as e:
        print(f"Error: Could not import DAW server: {e}")
        return 1

    print("=" * 60)
    print("iDAW Server - DAW Integration")
    print("=" * 60)
    print(f"\nHost: {args.host}")
    print(f"Port: {args.port}")
    print(f"Workers: {args.workers}")
    print()

    try:
        server = DAWServer(
            host=args.host,
            port=args.port,
            max_workers=args.workers,
        )
        server.start(blocking=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(
        prog='daiw',
        description='DAiW - Digital Audio intelligent Workstation CLI'
    )
    parser.add_argument('--version', action='version', version='%(prog)s 0.3.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract groove from MIDI')
    extract_parser.add_argument('midi_file', help='MIDI file to extract from')
    extract_parser.add_argument('-o', '--output', help='Output JSON file')
    
    # Apply command
    apply_parser = subparsers.add_parser('apply', help='Apply groove template')
    apply_parser.add_argument('midi_file', help='MIDI file to process')
    apply_parser.add_argument('-g', '--genre', default='funk', 
                              choices=['funk', 'jazz', 'rock', 'hiphop', 'edm', 'latin'],
                              help='Genre groove template')
    apply_parser.add_argument('-o', '--output', help='Output MIDI file')
    apply_parser.add_argument('-i', '--intensity', type=float, default=0.5,
                              help='Groove intensity 0.0-1.0')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze MIDI file')
    analyze_parser.add_argument('midi_file', help='MIDI file to analyze')
    analyze_parser.add_argument('-c', '--chords', action='store_true', help='Analyze chords')
    analyze_parser.add_argument('-s', '--sections', action='store_true', help='Detect sections')
    
    # Diagnose command
    diagnose_parser = subparsers.add_parser('diagnose', help='Diagnose chord progression')
    diagnose_parser.add_argument('progression', help='Chord progression (e.g., "F-C-Am-Dm")')
    
    # Reharm command
    reharm_parser = subparsers.add_parser('reharm', help='Generate reharmonizations')
    reharm_parser.add_argument('progression', help='Chord progression to reharmonize')
    reharm_parser.add_argument('-s', '--style', default='jazz',
                               choices=['jazz', 'pop', 'rnb', 'classical', 'experimental'],
                               help='Reharmonization style')
    reharm_parser.add_argument('-n', '--count', type=int, default=3,
                               help='Number of suggestions')
    
    # Teach command
    teach_parser = subparsers.add_parser('teach', help='Interactive teaching mode')
    teach_parser.add_argument('topic', help='Topic to learn (rulebreaking, borrowed, etc.)')
    teach_parser.add_argument('-q', '--quick', action='store_true', help='Quick single lesson')
    
    # Intent command with subcommands
    intent_parser = subparsers.add_parser('intent', help='Intent-based song generation')
    intent_subparsers = intent_parser.add_subparsers(dest='subcommand', help='Intent commands')
    
    # intent new
    intent_new = intent_subparsers.add_parser('new', help='Create new intent template')
    intent_new.add_argument('-t', '--title', help='Song title')
    intent_new.add_argument('-o', '--output', help='Output file (default: song_intent.json)')
    
    # intent process
    intent_process = intent_subparsers.add_parser('process', help='Process intent to generate elements')
    intent_process.add_argument('file', help='Intent JSON file')
    intent_process.add_argument('-o', '--output', help='Save output to JSON')
    intent_process.add_argument('-f', '--force', action='store_true', help='Proceed despite validation issues')
    
    # intent suggest
    intent_suggest = intent_subparsers.add_parser('suggest', help='Suggest rules to break')
    intent_suggest.add_argument('emotion', help='Target emotion (grief, anger, nostalgia, etc.)')
    
    # intent list
    intent_subparsers.add_parser('list', help='List all rule-breaking options')
    
    # intent validate
    intent_validate = intent_subparsers.add_parser('validate', help='Validate intent file')
    intent_validate.add_argument('file', help='Intent JSON file')

    # Arrange command
    arrange_parser = subparsers.add_parser('arrange', help='Generate complete arrangement')
    arrange_parser.add_argument('-t', '--title', default='Untitled', help='Song title')
    arrange_parser.add_argument('-g', '--genre', default='pop',
                                choices=['pop', 'rock', 'folk', 'lofi', 'edm', 'jazz', 'hiphop', 'rnb', 'indie'],
                                help='Genre template')
    arrange_parser.add_argument('-k', '--key', default='C', help='Musical key (e.g., C, Am, F#)')
    arrange_parser.add_argument('--tempo', type=float, default=120.0, help='Tempo in BPM')
    arrange_parser.add_argument('-c', '--chords', help='Chord progression (e.g., "C-G-Am-F")')
    arrange_parser.add_argument('-m', '--mood', default='neutral', help='Primary mood')
    arrange_parser.add_argument('-v', '--vulnerability', type=float, default=0.5,
                                help='Vulnerability scale 0.0-1.0')
    arrange_parser.add_argument('-n', '--narrative', default='transformation',
                                choices=['transformation', 'cyclical', 'descent', 'ascent', 'static', 'climactic'],
                                help='Narrative arc type')
    arrange_parser.add_argument('-o', '--output', help='Save arrangement JSON')
    arrange_parser.add_argument('--notes', help='Save production notes markdown')

    # Bass command
    bass_parser = subparsers.add_parser('bass', help='Generate bass line from chords')
    bass_parser.add_argument('chords', help='Chord progression (e.g., "C-G-Am-F" or "C:2-G:2-Am:2-F:2")')
    bass_parser.add_argument('-g', '--genre', default='pop',
                             choices=['pop', 'rock', 'folk', 'lofi', 'jazz', 'funk', 'hiphop', 'rnb', 'reggae'],
                             help='Genre for bass pattern')
    bass_parser.add_argument('-k', '--key', default='C', help='Musical key')
    bass_parser.add_argument('-s', '--section', default='verse',
                             choices=['intro', 'verse', 'chorus', 'bridge', 'outro', 'breakdown', 'buildup', 'drop'],
                             help='Section type')
    bass_parser.add_argument('-e', '--energy', type=float, default=0.5, help='Energy level 0.0-1.0')
    bass_parser.add_argument('-b', '--bars-per-chord', type=int, default=2, help='Default bars per chord')
    bass_parser.add_argument('-o', '--output', help='Save bass line JSON')

    # Energy command
    energy_parser = subparsers.add_parser('energy', help='Generate energy arc')
    energy_parser.add_argument('-m', '--mood', default='neutral', help='Primary mood')
    energy_parser.add_argument('-b', '--bars', type=int, default=64, help='Total bars')
    energy_parser.add_argument('-v', '--vulnerability', type=float, default=0.5,
                               help='Vulnerability scale 0.0-1.0')
    energy_parser.add_argument('-n', '--narrative', default='transformation',
                               choices=['transformation', 'cyclical', 'descent', 'ascent', 'static', 'climactic'],
                               help='Narrative arc type')
    energy_parser.add_argument('--min-energy', type=float, default=0.2, help='Minimum energy 0.0-1.0')
    energy_parser.add_argument('--max-energy', type=float, default=0.95, help='Maximum energy 0.0-1.0')
    energy_parser.add_argument('-o', '--output', help='Save energy arc JSON')

    # Genres command
    subparsers.add_parser('genres', help='List available genre templates')

    # App command (desktop GUI)
    app_parser = subparsers.add_parser('app', help='Launch desktop GUI application')
    app_parser.add_argument('-p', '--port', type=int, default=8501, help='Port for Streamlit server')
    app_parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    app_parser.add_argument('--browser', action='store_true', default=True, help='Open browser automatically')

    # Server command (DAW integration)
    server_parser = subparsers.add_parser('server', help='Start DAW integration server')
    server_parser.add_argument('--host', default='127.0.0.1', help='Host address (default: 127.0.0.1)')
    server_parser.add_argument('-p', '--port', type=int, default=8765, help='Port number (default: 8765)')
    server_parser.add_argument('-w', '--workers', type=int, default=2, help='Number of worker threads (default: 2)')

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    commands = {
        'extract': cmd_extract,
        'apply': cmd_apply,
        'analyze': cmd_analyze,
        'diagnose': cmd_diagnose,
        'reharm': cmd_reharm,
        'teach': cmd_teach,
        'intent': cmd_intent,
        'arrange': cmd_arrange,
        'bass': cmd_bass,
        'energy': cmd_energy,
        'genres': cmd_genres,
        'app': cmd_app,
        'server': cmd_server,
    }

    return commands[args.command](args)


if __name__ == '__main__':
    sys.exit(main())
