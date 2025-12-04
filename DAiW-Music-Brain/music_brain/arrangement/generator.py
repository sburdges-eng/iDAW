"""
Main arrangement generator for iDAW Music Brain.

Orchestrates complete song generation combining templates, bass, and energy arcs.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
import json
from pathlib import Path

from .templates import (
    SectionType,
    SectionTemplate,
    ArrangementTemplate,
    get_genre_template,
    create_custom_arrangement,
    GENRE_TEMPLATES,
)
from .bass_generator import (
    BassLine,
    BassPattern,
    generate_bass_line,
    generate_bass_for_arrangement,
    select_pattern_for_genre,
)
from .energy_arc import (
    EnergyArc,
    EnergyPoint,
    ArcType,
    EmotionalJourney,
    generate_energy_arc,
    apply_energy_to_sections,
    suggest_arc_for_intent,
    describe_energy_arc,
)


@dataclass
class SectionGenerated:
    """A generated section with all musical elements."""
    name: str
    section_type: SectionType
    bars: int
    start_bar: int
    energy: float
    chords: List[Tuple[str, int]]  # (chord_name, duration_bars)
    instruments: List[str]
    bass_pattern: BassPattern
    velocity_range: Tuple[int, int]
    production_notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "section_type": self.section_type.value,
            "bars": self.bars,
            "start_bar": self.start_bar,
            "energy": self.energy,
            "chords": [[c, d] for c, d in self.chords],
            "instruments": self.instruments,
            "bass_pattern": self.bass_pattern.value,
            "velocity_range": list(self.velocity_range),
            "production_notes": self.production_notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SectionGenerated":
        return cls(
            name=data["name"],
            section_type=SectionType(data["section_type"]),
            bars=data["bars"],
            start_bar=data["start_bar"],
            energy=data["energy"],
            chords=[(c, d) for c, d in data["chords"]],
            instruments=data["instruments"],
            bass_pattern=BassPattern(data["bass_pattern"]),
            velocity_range=tuple(data["velocity_range"]),
            production_notes=data.get("production_notes", ""),
        )


@dataclass
class GeneratedArrangement:
    """Complete generated arrangement with all elements."""
    title: str
    genre: str
    key: str
    tempo: float
    time_signature: Tuple[int, int]  # (numerator, denominator)
    total_bars: int
    sections: List[SectionGenerated]
    energy_arc: EnergyArc
    bass_lines: Dict[str, BassLine]
    production_notes: str
    chord_progression: List[str]  # Full song chord progression
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "genre": self.genre,
            "key": self.key,
            "tempo": self.tempo,
            "time_signature": list(self.time_signature),
            "total_bars": self.total_bars,
            "sections": [s.to_dict() for s in self.sections],
            "energy_arc": self.energy_arc.to_dict(),
            "bass_lines": {k: v.to_dict() for k, v in self.bass_lines.items()},
            "production_notes": self.production_notes,
            "chord_progression": self.chord_progression,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GeneratedArrangement":
        return cls(
            title=data["title"],
            genre=data["genre"],
            key=data["key"],
            tempo=data["tempo"],
            time_signature=tuple(data["time_signature"]),
            total_bars=data["total_bars"],
            sections=[SectionGenerated.from_dict(s) for s in data["sections"]],
            energy_arc=EnergyArc.from_dict(data["energy_arc"]),
            bass_lines={k: BassLine.from_dict(v) for k, v in data["bass_lines"].items()},
            production_notes=data["production_notes"],
            chord_progression=data["chord_progression"],
            metadata=data.get("metadata", {}),
        )

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: str):
        """Save arrangement to JSON file."""
        Path(path).write_text(self.to_json())

    @classmethod
    def load(cls, path: str) -> "GeneratedArrangement":
        """Load arrangement from JSON file."""
        data = json.loads(Path(path).read_text())
        return cls.from_dict(data)

    def get_section_at_bar(self, bar: int) -> Optional[SectionGenerated]:
        """Get the section containing the given bar."""
        for section in self.sections:
            if section.start_bar <= bar < section.start_bar + section.bars:
                return section
        return None

    def describe(self) -> str:
        """Generate human-readable description."""
        lines = [
            f"# {self.title}",
            f"Genre: {self.genre} | Key: {self.key} | Tempo: {self.tempo} BPM",
            f"Duration: {self.total_bars} bars ({self.time_signature[0]}/{self.time_signature[1]})",
            "",
            "## Structure",
        ]

        for section in self.sections:
            lines.append(
                f"- {section.name} ({section.section_type.value}): "
                f"bars {section.start_bar}-{section.start_bar + section.bars - 1}, "
                f"energy {section.energy:.0%}"
            )

        lines.extend([
            "",
            "## Chord Progression",
            " | ".join(self.chord_progression),
            "",
            "## Production Notes",
            self.production_notes,
        ])

        return "\n".join(lines)


class ArrangementGenerator:
    """
    Main generator class for creating complete song arrangements.

    Combines templates, bass generation, and energy arcs to create
    cohesive musical arrangements from intent specifications.
    """

    def __init__(
        self,
        default_genre: str = "pop",
        default_key: str = "C",
        default_tempo: float = 120.0,
    ):
        self.default_genre = default_genre
        self.default_key = default_key
        self.default_tempo = default_tempo

    def generate(
        self,
        title: str = "Untitled",
        genre: str = None,
        key: str = None,
        tempo: float = None,
        chord_progression: Optional[List[str]] = None,
        structure: Optional[str] = None,
        mood: str = "neutral",
        vulnerability: float = 0.5,
        narrative_arc: str = "transformation",
        time_signature: Tuple[int, int] = (4, 4),
        custom_sections: Optional[List[Dict[str, Any]]] = None,
    ) -> GeneratedArrangement:
        """
        Generate a complete arrangement.

        Args:
            title: Song title
            genre: Genre (pop, rock, folk, lofi, edm, jazz, hiphop, rnb, indie)
            key: Musical key (C, Am, F#, etc.)
            tempo: Tempo in BPM
            chord_progression: List of chord symbols
            structure: Structure string like "VCVC" or "intro-verse-chorus-verse-chorus-bridge-chorus-outro"
            mood: Primary mood for energy arc
            vulnerability: Vulnerability scale (0.0-1.0)
            narrative_arc: Narrative type (transformation, cyclical, descent, ascent)
            time_signature: Time signature tuple
            custom_sections: Custom section definitions (overrides template)

        Returns:
            GeneratedArrangement object
        """
        # Apply defaults
        genre = genre or self.default_genre
        key = key or self.default_key
        tempo = tempo or self.default_tempo

        # Get arrangement template
        if custom_sections:
            template = create_custom_arrangement(
                sections=custom_sections,
                name=title,
                genre=genre,
            )
        else:
            template = get_genre_template(genre)

        # Generate energy arc
        arc_type, journey, climax = suggest_arc_for_intent(
            mood=mood,
            vulnerability=vulnerability,
            narrative_arc=narrative_arc,
        )

        section_boundaries = []
        current_bar = 0
        for s in template.sections:
            section_boundaries.append((current_bar, s.section_type.value))
            current_bar += s.bars

        energy_arc = generate_energy_arc(
            total_bars=template.total_bars,
            arc_type=arc_type,
            emotional_journey=journey,
            climax_position=climax,
            section_boundaries=section_boundaries,
        )

        # Apply energy to sections
        section_dicts = [
            {"name": f"{s.section_type.value}_{i}", "bars": s.bars, "type": s.section_type.value}
            for i, s in enumerate(template.sections)
        ]
        energized_sections = apply_energy_to_sections(section_dicts, energy_arc)

        # Generate chord assignments per section
        if not chord_progression:
            chord_progression = self._generate_default_progression(key, genre)

        section_chords = self._assign_chords_to_sections(
            chord_progression,
            energized_sections,
            key,
        )

        # Generate sections
        generated_sections = []
        current_bar = 0
        full_chord_sequence = []

        for i, (tmpl_section, energy_section) in enumerate(zip(template.sections, energized_sections)):
            section_name = f"{tmpl_section.section_type.value}_{i + 1}"
            chords = section_chords.get(section_name, [(key, tmpl_section.bars)])

            # Add to full progression
            for chord, _ in chords:
                if chord not in full_chord_sequence:
                    full_chord_sequence.append(chord)

            generated_sections.append(SectionGenerated(
                name=section_name,
                section_type=tmpl_section.section_type,
                bars=tmpl_section.bars,
                start_bar=current_bar,
                energy=energy_section["energy"],
                chords=chords,
                instruments=tmpl_section.instruments,
                bass_pattern=select_pattern_for_genre(genre, tmpl_section.section_type.value),
                velocity_range=energy_section.get("velocity_range", (60, 100)),
                production_notes=self._generate_section_notes(
                    tmpl_section.section_type,
                    energy_section["energy"],
                    genre,
                ),
            ))
            current_bar += tmpl_section.bars

        # Generate bass lines for all sections
        bass_lines = {}
        for section in generated_sections:
            bass_lines[section.name] = generate_bass_line(
                chords=section.chords,
                genre=genre,
                key=key,
                section_type=section.section_type.value,
                energy=section.energy,
            )

        # Generate overall production notes
        production_notes = self._generate_production_notes(
            genre=genre,
            mood=mood,
            energy_arc=energy_arc,
            sections=generated_sections,
        )

        return GeneratedArrangement(
            title=title,
            genre=genre,
            key=key,
            tempo=tempo,
            time_signature=time_signature,
            total_bars=template.total_bars,
            sections=generated_sections,
            energy_arc=energy_arc,
            bass_lines=bass_lines,
            production_notes=production_notes,
            chord_progression=full_chord_sequence,
            metadata={
                "mood": mood,
                "vulnerability": vulnerability,
                "narrative_arc": narrative_arc,
                "template_name": template.name,
            },
        )

    def _generate_default_progression(self, key: str, genre: str) -> List[str]:
        """Generate a default chord progression based on key and genre."""
        # Common progressions by genre
        progressions = {
            "pop": ["I", "V", "vi", "IV"],  # Classic pop
            "rock": ["I", "IV", "V", "I"],  # Rock standard
            "folk": ["I", "IV", "I", "V"],  # Folk/country
            "lofi": ["ii", "V", "I", "vi"],  # Jazz-influenced
            "jazz": ["ii", "V", "I", "vi"],  # ii-V-I-vi
            "edm": ["vi", "IV", "I", "V"],  # EDM progression
            "hiphop": ["i", "VI", "III", "VII"],  # Minor hip-hop
            "rnb": ["I", "vi", "IV", "V"],  # R&B standard
            "indie": ["I", "iii", "IV", "V"],  # Indie variation
        }

        # Scale degrees to chord conversion
        major_scale = {
            "I": "", "ii": "m", "iii": "m", "IV": "", "V": "", "vi": "m", "vii°": "dim",
            "i": "m", "II": "", "III": "", "iv": "m", "v": "m", "VI": "", "VII": "",
        }

        # Note mapping
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        # Find root note index
        root = key.replace("m", "").replace("#", "").replace("b", "")
        if "#" in key:
            root += "#"
        elif "b" in key:
            root = notes[(notes.index(root) - 1) % 12]

        try:
            root_idx = notes.index(root)
        except ValueError:
            root_idx = 0

        # Get progression template
        prog_template = progressions.get(genre.lower(), progressions["pop"])

        # Major scale intervals
        major_intervals = [0, 2, 4, 5, 7, 9, 11]
        minor_intervals = [0, 2, 3, 5, 7, 8, 10]

        is_minor = "m" in key and key[-1] == "m"
        intervals = minor_intervals if is_minor else major_intervals

        # Build chord progression
        chords = []
        for degree in prog_template:
            # Get scale degree number
            degree_map = {
                "I": 0, "i": 0,
                "II": 1, "ii": 1,
                "III": 2, "iii": 2,
                "IV": 3, "iv": 3,
                "V": 4, "v": 4,
                "VI": 5, "vi": 5,
                "VII": 6, "vii°": 6,
            }

            deg_num = degree_map.get(degree.replace("°", ""), 0)
            chord_root = notes[(root_idx + intervals[deg_num]) % 12]
            quality = major_scale.get(degree, "")

            chords.append(chord_root + quality)

        return chords

    def _assign_chords_to_sections(
        self,
        progression: List[str],
        sections: List[Dict[str, Any]],
        key: str,
    ) -> Dict[str, List[Tuple[str, int]]]:
        """Assign chords to each section based on section type and length."""
        section_chords = {}

        for section in sections:
            name = section.get("name", "section")
            bars = section.get("bars", 8)
            section_type = section.get("type", "verse")

            # Determine chord pattern based on section type
            if section_type in ["intro", "outro"]:
                # Simple: use first chord or tonic
                chords = [(progression[0] if progression else key, bars)]

            elif section_type in ["verse", "prechorus"]:
                # Use full progression, cycling if needed
                chords = []
                remaining_bars = bars
                prog_idx = 0

                while remaining_bars > 0:
                    chord = progression[prog_idx % len(progression)]
                    chord_bars = min(2, remaining_bars)  # 2 bars per chord
                    chords.append((chord, chord_bars))
                    remaining_bars -= chord_bars
                    prog_idx += 1

            elif section_type == "chorus":
                # Different progression order for contrast
                alt_progression = progression[2:] + progression[:2] if len(progression) >= 4 else progression
                chords = []
                remaining_bars = bars
                prog_idx = 0

                while remaining_bars > 0:
                    chord = alt_progression[prog_idx % len(alt_progression)]
                    chord_bars = min(2, remaining_bars)
                    chords.append((chord, chord_bars))
                    remaining_bars -= chord_bars
                    prog_idx += 1

            elif section_type == "bridge":
                # Use different chords (vi, IV, I, V or similar)
                bridge_prog = progression[1:] + [progression[0]]
                chords = []
                remaining_bars = bars
                prog_idx = 0

                while remaining_bars > 0:
                    chord = bridge_prog[prog_idx % len(bridge_prog)]
                    chord_bars = min(2, remaining_bars)
                    chords.append((chord, chord_bars))
                    remaining_bars -= chord_bars
                    prog_idx += 1

            elif section_type in ["breakdown", "buildup"]:
                # Simpler: pedal on one chord or oscillate between two
                if len(progression) >= 2:
                    chords = [
                        (progression[0], bars // 2),
                        (progression[1], bars - bars // 2),
                    ]
                else:
                    chords = [(progression[0] if progression else key, bars)]

            elif section_type == "drop":
                # High energy: quick chord changes
                chords = []
                remaining_bars = bars
                prog_idx = 0

                while remaining_bars > 0:
                    chord = progression[prog_idx % len(progression)]
                    chord_bars = min(1, remaining_bars)  # 1 bar per chord
                    chords.append((chord, chord_bars))
                    remaining_bars -= chord_bars
                    prog_idx += 1

            else:
                # Default: spread progression across section
                chords_per_bar = max(1, bars // len(progression))
                chords = [(c, chords_per_bar) for c in progression]

                # Adjust last chord to fill remaining bars
                total_assigned = sum(d for _, d in chords)
                if total_assigned < bars:
                    last_chord, last_dur = chords[-1]
                    chords[-1] = (last_chord, last_dur + (bars - total_assigned))

            section_chords[name] = chords

        return section_chords

    def _generate_section_notes(
        self,
        section_type: SectionType,
        energy: float,
        genre: str,
    ) -> str:
        """Generate production notes for a specific section."""
        notes = []

        # Energy-based notes
        if energy < 0.3:
            notes.append("Keep sparse, intimate feel")
            notes.append("Reduce drum presence or use brushes")
        elif energy < 0.5:
            notes.append("Moderate energy, room to grow")
            notes.append("Full arrangement but not overwhelming")
        elif energy < 0.7:
            notes.append("Building energy, add layers")
            notes.append("Increase rhythmic drive")
        elif energy < 0.9:
            notes.append("High energy section")
            notes.append("Full arrangement, all instruments active")
        else:
            notes.append("Maximum intensity - climax")
            notes.append("Everything at full power")

        # Section-specific notes
        section_notes = {
            SectionType.INTRO: "Establish mood and key, hook listener",
            SectionType.VERSE: "Carry the narrative, leave space for vocals",
            SectionType.PRECHORUS: "Build tension, anticipate the chorus",
            SectionType.CHORUS: "Emotional peak, memorable hook",
            SectionType.BRIDGE: "Provide contrast, new perspective",
            SectionType.OUTRO: "Resolution, leave lasting impression",
            SectionType.BREAKDOWN: "Strip back, create breathing room",
            SectionType.BUILDUP: "Increase tension progressively",
            SectionType.DROP: "Maximum impact, release built tension",
            SectionType.SOLO: "Showcase featured instrument",
        }

        if section_type in section_notes:
            notes.append(section_notes[section_type])

        return " | ".join(notes)

    def _generate_production_notes(
        self,
        genre: str,
        mood: str,
        energy_arc: EnergyArc,
        sections: List[SectionGenerated],
    ) -> str:
        """Generate overall production notes for the arrangement."""
        lines = [
            f"## Production Guide for {genre.title()} Track",
            "",
            f"### Emotional Journey: {energy_arc.emotional_journey.value}",
            describe_energy_arc(energy_arc),
            "",
            "### General Guidelines",
        ]

        # Genre-specific production notes
        genre_notes = {
            "pop": [
                "- Polished, radio-ready sound",
                "- Strong hook in chorus",
                "- Crisp drums with punchy kick",
                "- Vocals front and center",
            ],
            "rock": [
                "- Guitar-driven energy",
                "- Room for dynamics",
                "- Drums: solid backbeat",
                "- Don't over-compress",
            ],
            "folk": [
                "- Natural, organic sound",
                "- Acoustic instruments forward",
                "- Minimal processing",
                "- Room ambience preferred",
            ],
            "lofi": [
                "- Embrace imperfection",
                "- Vinyl noise, tape saturation",
                "- Buried vocals if present",
                "- Lo-fi drum samples",
                "- Narrow stereo field",
            ],
            "jazz": [
                "- Natural room sound",
                "- Dynamic playing, no compression",
                "- Space for improvisation",
                "- Warm, vintage tone",
            ],
            "edm": [
                "- Powerful sub-bass",
                "- Side-chain compression",
                "- Build tension before drops",
                "- Wide stereo in drops",
            ],
            "hiphop": [
                "- 808 bass presence",
                "- Punchy kick, snappy snare",
                "- Vocal processing: subtle",
                "- Sample-based or synth textures",
            ],
            "rnb": [
                "- Smooth, warm sound",
                "- Lush pads and keys",
                "- Vocals: emotion over power",
                "- Groove is everything",
            ],
        }

        lines.extend(genre_notes.get(genre.lower(), [
            "- Follow genre conventions",
            "- Maintain dynamic range",
            "- Balance all elements",
        ]))

        # Mood-specific notes
        lines.append("")
        lines.append(f"### Mood: {mood.title()}")

        mood_notes = {
            "grief": "Allow space for emotion. Don't rush resolutions. Reverb for distance.",
            "anger": "Aggressive compression. Forward presence. Distortion where appropriate.",
            "joy": "Bright EQ. Open sound. Lift the energy.",
            "nostalgia": "Vintage processing. Tape warmth. Slightly muffled highs.",
            "anxiety": "Tension in the mix. Unresolved elements. Restless energy.",
            "peace": "Gentle dynamics. Smooth transitions. Warm frequencies.",
        }

        lines.append(mood_notes.get(mood.lower(), "Match production to emotional intent."))

        # Section breakdown
        lines.append("")
        lines.append("### Section-by-Section")

        for section in sections:
            lines.append(f"\n**{section.name.replace('_', ' ').title()}** (bars {section.start_bar}-{section.start_bar + section.bars - 1})")
            lines.append(f"- Energy: {section.energy:.0%}")
            lines.append(f"- Instruments: {', '.join(section.instruments)}")
            lines.append(f"- Notes: {section.production_notes}")

        return "\n".join(lines)


# Convenience functions
def generate_arrangement(
    title: str = "Untitled",
    genre: str = "pop",
    key: str = "C",
    tempo: float = 120.0,
    chord_progression: Optional[List[str]] = None,
    mood: str = "neutral",
    **kwargs
) -> GeneratedArrangement:
    """
    Generate a complete song arrangement.

    This is a convenience wrapper around ArrangementGenerator.

    Args:
        title: Song title
        genre: Genre name
        key: Musical key
        tempo: Tempo in BPM
        chord_progression: Optional chord progression
        mood: Primary mood
        **kwargs: Additional arguments passed to generator

    Returns:
        GeneratedArrangement object
    """
    generator = ArrangementGenerator(
        default_genre=genre,
        default_key=key,
        default_tempo=tempo,
    )

    return generator.generate(
        title=title,
        genre=genre,
        key=key,
        tempo=tempo,
        chord_progression=chord_progression,
        mood=mood,
        **kwargs
    )


def generate_complete_song(
    intent: Dict[str, Any],
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a complete song package from intent.

    Args:
        intent: Song intent dictionary with keys:
            - title: str
            - genre: str
            - key: str
            - tempo: float
            - mood: str
            - chord_progression: List[str] (optional)
            - vulnerability: float (optional)
            - narrative_arc: str (optional)
        output_dir: Directory to save outputs (optional)

    Returns:
        Dictionary containing:
            - arrangement: GeneratedArrangement
            - bass_lines: Dict of BassLine objects
            - energy_arc: EnergyArc
            - production_notes: str

    Example:
        >>> intent = {
        ...     "title": "My Song",
        ...     "genre": "pop",
        ...     "key": "C",
        ...     "tempo": 120,
        ...     "mood": "joy",
        ...     "chord_progression": ["C", "G", "Am", "F"],
        ... }
        >>> result = generate_complete_song(intent)
    """
    # Extract intent fields
    title = intent.get("title", "Untitled")
    genre = intent.get("genre", "pop")
    key = intent.get("key", "C")
    tempo = intent.get("tempo", 120.0)
    mood = intent.get("mood", "neutral")
    chord_progression = intent.get("chord_progression")
    vulnerability = intent.get("vulnerability", 0.5)
    narrative_arc = intent.get("narrative_arc", "transformation")

    # Generate arrangement
    arrangement = generate_arrangement(
        title=title,
        genre=genre,
        key=key,
        tempo=tempo,
        chord_progression=chord_progression,
        mood=mood,
        vulnerability=vulnerability,
        narrative_arc=narrative_arc,
    )

    # Prepare output
    result = {
        "arrangement": arrangement,
        "bass_lines": arrangement.bass_lines,
        "energy_arc": arrangement.energy_arc,
        "production_notes": arrangement.production_notes,
        "sections": [s.to_dict() for s in arrangement.sections],
    }

    # Save outputs if directory provided
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save arrangement JSON
        arrangement.save(str(output_path / f"{title.lower().replace(' ', '_')}_arrangement.json"))

        # Save production notes as markdown
        notes_path = output_path / f"{title.lower().replace(' ', '_')}_production_notes.md"
        notes_path.write_text(arrangement.production_notes)

        # Save song description
        desc_path = output_path / f"{title.lower().replace(' ', '_')}_description.md"
        desc_path.write_text(arrangement.describe())

        result["output_files"] = {
            "arrangement": str(output_path / f"{title.lower().replace(' ', '_')}_arrangement.json"),
            "production_notes": str(notes_path),
            "description": str(desc_path),
        }

    return result
