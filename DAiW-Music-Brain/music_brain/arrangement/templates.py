"""
Section and arrangement templates for song generation.

Provides genre-specific templates for building complete song structures.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any


class SectionType(Enum):
    """Types of song sections."""
    INTRO = "intro"
    VERSE = "verse"
    PRECHORUS = "prechorus"
    CHORUS = "chorus"
    BRIDGE = "bridge"
    OUTRO = "outro"
    BREAKDOWN = "breakdown"
    BUILDUP = "buildup"
    DROP = "drop"
    SOLO = "solo"
    INTERLUDE = "interlude"
    HOOK = "hook"


@dataclass
class SectionTemplate:
    """Template for a song section."""
    section_type: SectionType
    bars: int = 8
    energy: float = 0.5  # 0.0 to 1.0
    instruments: List[str] = field(default_factory=list)
    description: str = ""
    suggested_chords: Optional[str] = None
    velocity_range: tuple = (60, 100)
    density: float = 0.5  # Note density 0.0 to 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_type": self.section_type.value,
            "bars": self.bars,
            "energy": self.energy,
            "instruments": self.instruments,
            "description": self.description,
            "suggested_chords": self.suggested_chords,
            "velocity_range": list(self.velocity_range),
            "density": self.density,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SectionTemplate":
        return cls(
            section_type=SectionType(data["section_type"]),
            bars=data.get("bars", 8),
            energy=data.get("energy", 0.5),
            instruments=data.get("instruments", []),
            description=data.get("description", ""),
            suggested_chords=data.get("suggested_chords"),
            velocity_range=tuple(data.get("velocity_range", [60, 100])),
            density=data.get("density", 0.5),
        )


@dataclass
class ArrangementTemplate:
    """Complete song arrangement template."""
    name: str
    genre: str
    sections: List[SectionTemplate]
    tempo_range: tuple = (90, 130)
    default_key: str = "C"
    description: str = ""
    total_bars: int = field(init=False)

    def __post_init__(self):
        self.total_bars = sum(s.bars for s in self.sections)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "genre": self.genre,
            "sections": [s.to_dict() for s in self.sections],
            "tempo_range": list(self.tempo_range),
            "default_key": self.default_key,
            "description": self.description,
            "total_bars": self.total_bars,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArrangementTemplate":
        sections = [SectionTemplate.from_dict(s) for s in data["sections"]]
        return cls(
            name=data["name"],
            genre=data["genre"],
            sections=sections,
            tempo_range=tuple(data.get("tempo_range", [90, 130])),
            default_key=data.get("default_key", "C"),
            description=data.get("description", ""),
        )

    def get_section_at_bar(self, bar: int) -> Optional[SectionTemplate]:
        """Get the section that contains the given bar number."""
        current_bar = 0
        for section in self.sections:
            if current_bar <= bar < current_bar + section.bars:
                return section
            current_bar += section.bars
        return None

    def get_energy_at_bar(self, bar: int) -> float:
        """Get energy level at a specific bar."""
        section = self.get_section_at_bar(bar)
        return section.energy if section else 0.5


# Section factory functions
def create_intro(
    bars: int = 4,
    energy: float = 0.3,
    instruments: Optional[List[str]] = None
) -> SectionTemplate:
    """Create an intro section template."""
    return SectionTemplate(
        section_type=SectionType.INTRO,
        bars=bars,
        energy=energy,
        instruments=instruments or ["guitar", "ambient"],
        description="Opening, sets mood and key",
        density=0.3,
        velocity_range=(40, 70),
    )


def create_verse(
    bars: int = 8,
    energy: float = 0.5,
    instruments: Optional[List[str]] = None,
    verse_number: int = 1
) -> SectionTemplate:
    """Create a verse section template."""
    return SectionTemplate(
        section_type=SectionType.VERSE,
        bars=bars,
        energy=energy,
        instruments=instruments or ["guitar", "bass", "drums_light"],
        description=f"Verse {verse_number} - storytelling, builds narrative",
        density=0.5,
        velocity_range=(50, 80),
    )


def create_prechorus(
    bars: int = 4,
    energy: float = 0.65,
    instruments: Optional[List[str]] = None
) -> SectionTemplate:
    """Create a pre-chorus section template."""
    return SectionTemplate(
        section_type=SectionType.PRECHORUS,
        bars=bars,
        energy=energy,
        instruments=instruments or ["guitar", "bass", "drums", "synth_pad"],
        description="Builds tension before chorus",
        density=0.6,
        velocity_range=(60, 90),
    )


def create_chorus(
    bars: int = 8,
    energy: float = 0.85,
    instruments: Optional[List[str]] = None
) -> SectionTemplate:
    """Create a chorus section template."""
    return SectionTemplate(
        section_type=SectionType.CHORUS,
        bars=bars,
        energy=energy,
        instruments=instruments or ["guitar", "bass", "drums", "vocals", "synth"],
        description="Emotional peak, hook, memorable",
        density=0.8,
        velocity_range=(70, 110),
    )


def create_bridge(
    bars: int = 8,
    energy: float = 0.6,
    instruments: Optional[List[str]] = None
) -> SectionTemplate:
    """Create a bridge section template."""
    return SectionTemplate(
        section_type=SectionType.BRIDGE,
        bars=bars,
        energy=energy,
        instruments=instruments or ["piano", "strings", "vocals"],
        description="Contrast, new perspective, harmonic departure",
        density=0.5,
        velocity_range=(55, 85),
    )


def create_outro(
    bars: int = 4,
    energy: float = 0.25,
    instruments: Optional[List[str]] = None
) -> SectionTemplate:
    """Create an outro section template."""
    return SectionTemplate(
        section_type=SectionType.OUTRO,
        bars=bars,
        energy=energy,
        instruments=instruments or ["guitar", "ambient"],
        description="Closing, resolution or fade",
        density=0.2,
        velocity_range=(30, 60),
    )


def create_breakdown(
    bars: int = 4,
    energy: float = 0.35,
    instruments: Optional[List[str]] = None
) -> SectionTemplate:
    """Create a breakdown section template."""
    return SectionTemplate(
        section_type=SectionType.BREAKDOWN,
        bars=bars,
        energy=energy,
        instruments=instruments or ["drums_minimal", "bass"],
        description="Stripped down, breath before buildup",
        density=0.3,
        velocity_range=(40, 65),
    )


def create_buildup(
    bars: int = 4,
    energy: float = 0.7,
    instruments: Optional[List[str]] = None
) -> SectionTemplate:
    """Create a buildup section template."""
    return SectionTemplate(
        section_type=SectionType.BUILDUP,
        bars=bars,
        energy=energy,
        instruments=instruments or ["drums", "synth_riser", "fx"],
        description="Increasing tension toward drop/chorus",
        density=0.7,
        velocity_range=(60, 100),
    )


def create_drop(
    bars: int = 8,
    energy: float = 0.95,
    instruments: Optional[List[str]] = None
) -> SectionTemplate:
    """Create a drop section template (EDM)."""
    return SectionTemplate(
        section_type=SectionType.DROP,
        bars=bars,
        energy=energy,
        instruments=instruments or ["bass_heavy", "drums_full", "synth_lead"],
        description="Maximum energy release",
        density=0.9,
        velocity_range=(80, 127),
    )


def create_solo(
    bars: int = 8,
    energy: float = 0.75,
    instruments: Optional[List[str]] = None
) -> SectionTemplate:
    """Create a solo section template."""
    return SectionTemplate(
        section_type=SectionType.SOLO,
        bars=bars,
        energy=energy,
        instruments=instruments or ["lead_guitar", "bass", "drums"],
        description="Instrumental showcase",
        density=0.7,
        velocity_range=(65, 105),
    )


# Genre-specific arrangement templates
GENRE_TEMPLATES: Dict[str, ArrangementTemplate] = {
    "pop": ArrangementTemplate(
        name="Standard Pop",
        genre="pop",
        sections=[
            create_intro(bars=4, energy=0.3),
            create_verse(bars=8, energy=0.5, verse_number=1),
            create_prechorus(bars=4, energy=0.65),
            create_chorus(bars=8, energy=0.85),
            create_verse(bars=8, energy=0.55, verse_number=2),
            create_prechorus(bars=4, energy=0.7),
            create_chorus(bars=8, energy=0.9),
            create_bridge(bars=8, energy=0.6),
            create_chorus(bars=8, energy=0.95),
            create_outro(bars=4, energy=0.3),
        ],
        tempo_range=(100, 130),
        description="Classic verse-chorus pop structure",
    ),

    "rock": ArrangementTemplate(
        name="Rock Anthem",
        genre="rock",
        sections=[
            create_intro(bars=4, energy=0.5, instruments=["guitar_distorted", "drums"]),
            create_verse(bars=8, energy=0.6, instruments=["guitar", "bass", "drums"]),
            create_chorus(bars=8, energy=0.9, instruments=["guitar_full", "bass", "drums", "vocals"]),
            create_verse(bars=8, energy=0.65),
            create_chorus(bars=8, energy=0.9),
            create_solo(bars=8, energy=0.8, instruments=["lead_guitar", "bass", "drums"]),
            create_chorus(bars=8, energy=0.95),
            create_outro(bars=8, energy=0.4, instruments=["guitar_feedback"]),
        ],
        tempo_range=(110, 140),
        description="Guitar-driven rock structure with solo",
    ),

    "folk": ArrangementTemplate(
        name="Folk Ballad",
        genre="folk",
        sections=[
            create_intro(bars=4, energy=0.2, instruments=["acoustic_guitar"]),
            create_verse(bars=8, energy=0.4, instruments=["acoustic_guitar", "vocals"]),
            create_verse(bars=8, energy=0.5, instruments=["acoustic_guitar", "vocals", "bass"]),
            create_chorus(bars=8, energy=0.7, instruments=["acoustic_guitar", "vocals", "bass", "drums_brushes"]),
            create_verse(bars=8, energy=0.5),
            create_chorus(bars=8, energy=0.75),
            create_bridge(bars=8, energy=0.5, instruments=["piano", "vocals"]),
            create_chorus(bars=8, energy=0.8),
            create_outro(bars=8, energy=0.2, instruments=["acoustic_guitar"]),
        ],
        tempo_range=(70, 100),
        description="Intimate folk/acoustic structure",
    ),

    "lofi": ArrangementTemplate(
        name="Lo-Fi Bedroom",
        genre="lofi",
        sections=[
            create_intro(bars=4, energy=0.25, instruments=["guitar_lofi", "vinyl_noise"]),
            create_verse(bars=8, energy=0.4, instruments=["guitar_lofi", "bass_muted", "drums_lofi"]),
            create_verse(bars=8, energy=0.45, instruments=["guitar_lofi", "bass", "drums_lofi", "keys"]),
            create_chorus(bars=8, energy=0.6, instruments=["guitar_lofi", "bass", "drums_lofi", "vocals_buried"]),
            create_verse(bars=8, energy=0.4),
            create_chorus(bars=8, energy=0.65),
            create_outro(bars=8, energy=0.2, instruments=["guitar_lofi", "vinyl_noise"]),
        ],
        tempo_range=(70, 95),
        description="Intimate lo-fi with buried vocals aesthetic",
    ),

    "edm": ArrangementTemplate(
        name="EDM Drop",
        genre="edm",
        sections=[
            create_intro(bars=8, energy=0.3, instruments=["synth_pad", "fx"]),
            create_buildup(bars=8, energy=0.5),
            create_breakdown(bars=4, energy=0.3),
            create_buildup(bars=8, energy=0.75),
            create_drop(bars=16, energy=0.95),
            create_breakdown(bars=8, energy=0.35),
            create_buildup(bars=8, energy=0.8),
            create_drop(bars=16, energy=1.0),
            create_outro(bars=8, energy=0.3),
        ],
        tempo_range=(120, 150),
        description="Build-drop EDM structure",
    ),

    "jazz": ArrangementTemplate(
        name="Jazz Standard",
        genre="jazz",
        sections=[
            create_intro(bars=4, energy=0.4, instruments=["piano", "bass", "drums_brushes"]),
            create_verse(bars=8, energy=0.5, instruments=["piano", "bass", "drums"]),  # Head A
            create_verse(bars=8, energy=0.55),  # Head A'
            create_bridge(bars=8, energy=0.5, instruments=["piano", "bass", "drums"]),  # B section
            create_verse(bars=8, energy=0.5),  # Head A''
            create_solo(bars=16, energy=0.65, instruments=["piano_solo", "bass", "drums"]),
            create_solo(bars=16, energy=0.7, instruments=["sax_solo", "piano", "bass", "drums"]),
            create_verse(bars=8, energy=0.5),  # Head out
            create_outro(bars=4, energy=0.35),
        ],
        tempo_range=(100, 180),
        description="AABA jazz standard with solos",
    ),

    "hiphop": ArrangementTemplate(
        name="Hip-Hop Beat",
        genre="hiphop",
        sections=[
            create_intro(bars=4, energy=0.4, instruments=["sample", "drums_808"]),
            create_verse(bars=16, energy=0.6, instruments=["sample", "bass_808", "drums_808", "vocals_rap"]),
            create_chorus(bars=8, energy=0.75, instruments=["sample", "bass_808", "drums_808", "vocals_hook"]),
            create_verse(bars=16, energy=0.65),
            create_chorus(bars=8, energy=0.8),
            create_bridge(bars=8, energy=0.5, instruments=["sample_alt", "bass_808"]),
            create_chorus(bars=8, energy=0.85),
            create_outro(bars=4, energy=0.4),
        ],
        tempo_range=(80, 100),
        description="Hip-hop verse-hook structure",
    ),

    "rnb": ArrangementTemplate(
        name="R&B Slow Jam",
        genre="rnb",
        sections=[
            create_intro(bars=4, energy=0.3, instruments=["keys_rhodes", "strings_pad"]),
            create_verse(bars=8, energy=0.45, instruments=["keys", "bass", "drums_light", "vocals"]),
            create_prechorus(bars=4, energy=0.55),
            create_chorus(bars=8, energy=0.7, instruments=["keys", "bass", "drums", "vocals", "strings"]),
            create_verse(bars=8, energy=0.5),
            create_prechorus(bars=4, energy=0.6),
            create_chorus(bars=8, energy=0.75),
            create_bridge(bars=8, energy=0.55, instruments=["keys_solo", "strings"]),
            create_chorus(bars=8, energy=0.8),
            create_outro(bars=8, energy=0.3, instruments=["keys_rhodes", "vocals_ad_lib"]),
        ],
        tempo_range=(65, 90),
        description="Smooth R&B with pre-chorus",
    ),

    "indie": ArrangementTemplate(
        name="Indie Rock",
        genre="indie",
        sections=[
            create_intro(bars=8, energy=0.35, instruments=["guitar_clean", "synth_ambient"]),
            create_verse(bars=8, energy=0.5, instruments=["guitar", "bass", "drums"]),
            create_verse(bars=8, energy=0.55),
            create_chorus(bars=8, energy=0.75, instruments=["guitar_full", "bass", "drums", "synth"]),
            create_verse(bars=8, energy=0.5),
            create_chorus(bars=8, energy=0.8),
            create_bridge(bars=8, energy=0.6, instruments=["synth_lead", "drums"]),
            create_chorus(bars=8, energy=0.85),
            create_chorus(bars=8, energy=0.7),  # Repeated, fading
            create_outro(bars=8, energy=0.25),
        ],
        tempo_range=(100, 130),
        description="Indie rock with atmospheric elements",
    ),
}


def get_genre_template(genre: str) -> ArrangementTemplate:
    """
    Get arrangement template for a specific genre.

    Args:
        genre: Genre name (pop, rock, folk, lofi, edm, jazz, hiphop, rnb, indie)

    Returns:
        ArrangementTemplate for the genre

    Raises:
        ValueError: If genre is not found
    """
    genre_lower = genre.lower().replace("-", "").replace("_", "").replace(" ", "")

    # Handle aliases
    aliases = {
        "bedroom": "lofi",
        "lofibeats": "lofi",
        "electronic": "edm",
        "dance": "edm",
        "alternative": "indie",
        "acoustic": "folk",
        "country": "folk",
        "soul": "rnb",
        "trap": "hiphop",
        "rap": "hiphop",
    }

    genre_key = aliases.get(genre_lower, genre_lower)

    if genre_key not in GENRE_TEMPLATES:
        available = ", ".join(GENRE_TEMPLATES.keys())
        raise ValueError(f"Unknown genre '{genre}'. Available: {available}")

    return GENRE_TEMPLATES[genre_key]


def create_custom_arrangement(
    sections: List[Dict[str, Any]],
    name: str = "Custom",
    genre: str = "custom",
    tempo_range: tuple = (90, 130)
) -> ArrangementTemplate:
    """
    Create a custom arrangement template from section definitions.

    Args:
        sections: List of section dicts with keys: type, bars, energy, instruments
        name: Template name
        genre: Genre name
        tempo_range: (min_bpm, max_bpm)

    Returns:
        ArrangementTemplate

    Example:
        >>> sections = [
        ...     {"type": "intro", "bars": 4, "energy": 0.3},
        ...     {"type": "verse", "bars": 8, "energy": 0.5},
        ...     {"type": "chorus", "bars": 8, "energy": 0.8},
        ... ]
        >>> template = create_custom_arrangement(sections, name="My Song")
    """
    section_creators = {
        "intro": create_intro,
        "verse": create_verse,
        "prechorus": create_prechorus,
        "chorus": create_chorus,
        "bridge": create_bridge,
        "outro": create_outro,
        "breakdown": create_breakdown,
        "buildup": create_buildup,
        "drop": create_drop,
        "solo": create_solo,
    }

    section_templates = []
    for s in sections:
        section_type = s.get("type", "verse").lower()
        creator = section_creators.get(section_type, create_verse)

        template = creator(
            bars=s.get("bars", 8),
            energy=s.get("energy", 0.5),
            instruments=s.get("instruments"),
        )
        section_templates.append(template)

    return ArrangementTemplate(
        name=name,
        genre=genre,
        sections=section_templates,
        tempo_range=tempo_range,
    )
