"""
Energy arc generator for iDAW Music Brain.

Models the emotional/energy journey of a song through tension and release curves.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple, Any
import math


class ArcType(Enum):
    """Types of energy arc shapes."""
    LINEAR_BUILD = "linear_build"  # Steady increase
    LINEAR_DECAY = "linear_decay"  # Steady decrease
    EXPONENTIAL_BUILD = "exponential_build"  # Slow start, fast finish
    EXPONENTIAL_DECAY = "exponential_decay"  # Fast start, slow finish
    WAVE = "wave"  # Oscillating energy
    PEAK = "peak"  # Build to single peak, then decay
    DOUBLE_PEAK = "double_peak"  # Two peaks with valley
    PLATEAU = "plateau"  # Build, sustain, decay
    FLAT = "flat"  # Constant energy
    SAWTOOTH = "sawtooth"  # Repeated build and drop
    INVERSE_PEAK = "inverse_peak"  # High start, dip, high end


class EmotionalJourney(Enum):
    """Emotional narrative types."""
    TRIUMPH = "triumph"  # Struggle to victory
    TRAGEDY = "tragedy"  # Hope to despair
    CATHARSIS = "catharsis"  # Build tension, release
    MEDITATION = "meditation"  # Sustained calm
    EUPHORIA = "euphoria"  # Building joy
    GRIEF = "grief"  # Waves of sorrow
    DEFIANCE = "defiance"  # Rising resistance
    NOSTALGIA = "nostalgia"  # Bittersweet memories
    TENSION = "tension"  # Unresolved buildup
    RESOLUTION = "resolution"  # Conflict to peace


@dataclass
class EnergyPoint:
    """A single point in the energy arc."""
    position: float  # 0.0 to 1.0 (normalized position in song)
    energy: float  # 0.0 to 1.0 (energy level)
    bar: int = 0  # Absolute bar number
    section_name: str = ""
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "position": self.position,
            "energy": self.energy,
            "bar": self.bar,
            "section_name": self.section_name,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnergyPoint":
        return cls(
            position=data["position"],
            energy=data["energy"],
            bar=data.get("bar", 0),
            section_name=data.get("section_name", ""),
            description=data.get("description", ""),
        )


@dataclass
class EnergyArc:
    """Complete energy arc for a song."""
    points: List[EnergyPoint] = field(default_factory=list)
    arc_type: ArcType = ArcType.PEAK
    emotional_journey: EmotionalJourney = EmotionalJourney.CATHARSIS
    total_bars: int = 0
    climax_position: float = 0.75  # Where the peak occurs (0.0-1.0)
    min_energy: float = 0.2
    max_energy: float = 0.95

    def to_dict(self) -> Dict[str, Any]:
        return {
            "points": [p.to_dict() for p in self.points],
            "arc_type": self.arc_type.value,
            "emotional_journey": self.emotional_journey.value,
            "total_bars": self.total_bars,
            "climax_position": self.climax_position,
            "min_energy": self.min_energy,
            "max_energy": self.max_energy,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnergyArc":
        return cls(
            points=[EnergyPoint.from_dict(p) for p in data["points"]],
            arc_type=ArcType(data["arc_type"]),
            emotional_journey=EmotionalJourney(data.get("emotional_journey", "catharsis")),
            total_bars=data.get("total_bars", 0),
            climax_position=data.get("climax_position", 0.75),
            min_energy=data.get("min_energy", 0.2),
            max_energy=data.get("max_energy", 0.95),
        )

    def get_energy_at_position(self, position: float) -> float:
        """
        Get interpolated energy at any position.

        Args:
            position: Normalized position (0.0-1.0)

        Returns:
            Energy level (0.0-1.0)
        """
        if not self.points:
            return 0.5

        # Find surrounding points
        prev_point = self.points[0]
        next_point = self.points[-1]

        for i, point in enumerate(self.points):
            if point.position >= position:
                next_point = point
                if i > 0:
                    prev_point = self.points[i - 1]
                break
            prev_point = point

        # Linear interpolation
        if next_point.position == prev_point.position:
            return next_point.energy

        t = (position - prev_point.position) / (next_point.position - prev_point.position)
        return prev_point.energy + t * (next_point.energy - prev_point.energy)

    def get_energy_at_bar(self, bar: int) -> float:
        """Get energy level at a specific bar."""
        if self.total_bars == 0:
            return 0.5
        position = bar / self.total_bars
        return self.get_energy_at_position(position)

    def get_climax_bar(self) -> int:
        """Get the bar number of the climax."""
        return int(self.climax_position * self.total_bars)

    def describe(self) -> str:
        """Get a human-readable description of the energy arc."""
        peak_bar = self.get_climax_bar()
        return (
            f"Energy arc: {self.arc_type.value}\n"
            f"Emotional journey: {self.emotional_journey.value}\n"
            f"Range: {self.min_energy:.0%} to {self.max_energy:.0%}\n"
            f"Climax at bar {peak_bar} ({self.climax_position:.0%} through song)"
        )


def _generate_arc_curve(
    arc_type: ArcType,
    num_points: int = 20,
    climax_position: float = 0.75,
    min_energy: float = 0.2,
    max_energy: float = 0.95,
) -> List[Tuple[float, float]]:
    """
    Generate the raw (position, energy) curve for an arc type.

    Returns:
        List of (position, energy) tuples
    """
    points = []
    energy_range = max_energy - min_energy

    for i in range(num_points + 1):
        pos = i / num_points

        if arc_type == ArcType.LINEAR_BUILD:
            energy = min_energy + energy_range * pos

        elif arc_type == ArcType.LINEAR_DECAY:
            energy = max_energy - energy_range * pos

        elif arc_type == ArcType.EXPONENTIAL_BUILD:
            energy = min_energy + energy_range * (pos ** 2)

        elif arc_type == ArcType.EXPONENTIAL_DECAY:
            energy = max_energy - energy_range * (pos ** 2)

        elif arc_type == ArcType.WAVE:
            # Two full waves
            wave = math.sin(pos * 4 * math.pi)
            energy = min_energy + (energy_range * 0.5) + (wave * energy_range * 0.3)

        elif arc_type == ArcType.PEAK:
            # Single peak at climax position
            if pos <= climax_position:
                t = pos / climax_position
                energy = min_energy + energy_range * (t ** 1.5)
            else:
                t = (pos - climax_position) / (1 - climax_position)
                energy = max_energy - energy_range * 0.7 * t

        elif arc_type == ArcType.DOUBLE_PEAK:
            # Two peaks with valley in middle
            if pos < 0.35:
                t = pos / 0.35
                energy = min_energy + energy_range * 0.7 * t
            elif pos < 0.5:
                t = (pos - 0.35) / 0.15
                energy = min_energy + energy_range * 0.7 - energy_range * 0.3 * t
            elif pos < 0.85:
                t = (pos - 0.5) / 0.35
                energy = min_energy + energy_range * 0.4 + energy_range * 0.6 * t
            else:
                t = (pos - 0.85) / 0.15
                energy = max_energy - energy_range * 0.4 * t

        elif arc_type == ArcType.PLATEAU:
            # Build, sustain, decay
            if pos < 0.25:
                t = pos / 0.25
                energy = min_energy + energy_range * 0.8 * t
            elif pos < 0.75:
                energy = min_energy + energy_range * 0.8
            else:
                t = (pos - 0.75) / 0.25
                energy = min_energy + energy_range * 0.8 - energy_range * 0.5 * t

        elif arc_type == ArcType.FLAT:
            energy = min_energy + energy_range * 0.5

        elif arc_type == ArcType.SAWTOOTH:
            # Four sawtooth waves
            cycle = (pos * 4) % 1.0
            energy = min_energy + energy_range * cycle

        elif arc_type == ArcType.INVERSE_PEAK:
            # High-low-high
            if pos <= 0.5:
                t = pos / 0.5
                energy = max_energy - energy_range * 0.6 * t
            else:
                t = (pos - 0.5) / 0.5
                energy = min_energy + energy_range * 0.4 + energy_range * 0.6 * t

        else:
            energy = 0.5

        # Clamp energy to valid range
        energy = max(min_energy, min(max_energy, energy))
        points.append((pos, energy))

    return points


def get_arc_for_journey(journey: EmotionalJourney) -> Tuple[ArcType, float]:
    """
    Get appropriate arc type and climax position for an emotional journey.

    Returns:
        Tuple of (ArcType, climax_position)
    """
    journey_arcs: Dict[EmotionalJourney, Tuple[ArcType, float]] = {
        EmotionalJourney.TRIUMPH: (ArcType.EXPONENTIAL_BUILD, 0.9),
        EmotionalJourney.TRAGEDY: (ArcType.EXPONENTIAL_DECAY, 0.2),
        EmotionalJourney.CATHARSIS: (ArcType.PEAK, 0.75),
        EmotionalJourney.MEDITATION: (ArcType.FLAT, 0.5),
        EmotionalJourney.EUPHORIA: (ArcType.LINEAR_BUILD, 0.95),
        EmotionalJourney.GRIEF: (ArcType.WAVE, 0.5),
        EmotionalJourney.DEFIANCE: (ArcType.DOUBLE_PEAK, 0.85),
        EmotionalJourney.NOSTALGIA: (ArcType.INVERSE_PEAK, 0.5),
        EmotionalJourney.TENSION: (ArcType.EXPONENTIAL_BUILD, 0.95),
        EmotionalJourney.RESOLUTION: (ArcType.PEAK, 0.6),
    }

    return journey_arcs.get(journey, (ArcType.PEAK, 0.75))


def generate_energy_arc(
    total_bars: int,
    arc_type: Optional[ArcType] = None,
    emotional_journey: EmotionalJourney = EmotionalJourney.CATHARSIS,
    climax_position: Optional[float] = None,
    min_energy: float = 0.2,
    max_energy: float = 0.95,
    section_boundaries: Optional[List[Tuple[int, str]]] = None,
) -> EnergyArc:
    """
    Generate an energy arc for a song.

    Args:
        total_bars: Total number of bars in the song
        arc_type: Type of arc (if None, derived from emotional_journey)
        emotional_journey: The emotional narrative type
        climax_position: Where the peak occurs (0.0-1.0)
        min_energy: Minimum energy level
        max_energy: Maximum energy level
        section_boundaries: List of (bar_number, section_name) tuples

    Returns:
        EnergyArc object

    Example:
        >>> arc = generate_energy_arc(
        ...     total_bars=64,
        ...     emotional_journey=EmotionalJourney.CATHARSIS,
        ...     section_boundaries=[(0, "intro"), (8, "verse"), (24, "chorus")]
        ... )
    """
    # Derive arc type from journey if not specified
    if arc_type is None:
        arc_type, default_climax = get_arc_for_journey(emotional_journey)
        if climax_position is None:
            climax_position = default_climax
    elif climax_position is None:
        climax_position = 0.75

    # Generate raw curve
    curve = _generate_arc_curve(
        arc_type=arc_type,
        num_points=max(20, total_bars // 2),
        climax_position=climax_position,
        min_energy=min_energy,
        max_energy=max_energy,
    )

    # Convert to EnergyPoints
    points = []
    for pos, energy in curve:
        bar = int(pos * total_bars)

        # Find section name if boundaries provided
        section_name = ""
        if section_boundaries:
            for b, name in reversed(section_boundaries):
                if bar >= b:
                    section_name = name
                    break

        points.append(EnergyPoint(
            position=pos,
            energy=energy,
            bar=bar,
            section_name=section_name,
        ))

    return EnergyArc(
        points=points,
        arc_type=arc_type,
        emotional_journey=emotional_journey,
        total_bars=total_bars,
        climax_position=climax_position,
        min_energy=min_energy,
        max_energy=max_energy,
    )


def apply_energy_to_sections(
    sections: List[Dict[str, Any]],
    energy_arc: EnergyArc,
) -> List[Dict[str, Any]]:
    """
    Apply energy arc values to section definitions.

    Args:
        sections: List of section dicts with 'bars' key
        energy_arc: EnergyArc to apply

    Returns:
        Updated sections with 'energy' and 'velocity_range' keys

    Example:
        >>> sections = [
        ...     {"name": "intro", "bars": 4},
        ...     {"name": "verse", "bars": 8},
        ...     {"name": "chorus", "bars": 8},
        ... ]
        >>> arc = generate_energy_arc(20, emotional_journey=EmotionalJourney.TRIUMPH)
        >>> updated = apply_energy_to_sections(sections, arc)
    """
    current_bar = 0
    updated_sections = []

    for section in sections:
        section_copy = section.copy()
        bars = section.get("bars", 8)

        # Get energy at section start and midpoint
        start_pos = current_bar / energy_arc.total_bars if energy_arc.total_bars > 0 else 0
        mid_pos = (current_bar + bars // 2) / energy_arc.total_bars if energy_arc.total_bars > 0 else 0

        start_energy = energy_arc.get_energy_at_position(start_pos)
        mid_energy = energy_arc.get_energy_at_position(mid_pos)

        # Use midpoint energy as section energy
        section_copy["energy"] = round(mid_energy, 2)

        # Calculate velocity range based on energy
        base_vel = 50
        energy_vel = int(mid_energy * 60)  # 0-60 based on energy
        section_copy["velocity_range"] = (
            max(30, base_vel + int(energy_vel * 0.5)),
            min(127, base_vel + energy_vel + 20)
        )

        # Add energy gradient (for sections that span energy changes)
        end_pos = (current_bar + bars) / energy_arc.total_bars if energy_arc.total_bars > 0 else 0
        end_energy = energy_arc.get_energy_at_position(end_pos)
        section_copy["energy_gradient"] = round(end_energy - start_energy, 2)

        updated_sections.append(section_copy)
        current_bar += bars

    return updated_sections


def describe_energy_arc(arc: EnergyArc) -> str:
    """
    Generate a human-readable description of an energy arc.

    Args:
        arc: EnergyArc to describe

    Returns:
        Multi-line description string
    """
    climax_bar = arc.get_climax_bar()

    descriptions: Dict[ArcType, str] = {
        ArcType.LINEAR_BUILD: "Steady building tension throughout",
        ArcType.LINEAR_DECAY: "Gradual release from opening intensity",
        ArcType.EXPONENTIAL_BUILD: "Slow burn building to explosive climax",
        ArcType.EXPONENTIAL_DECAY: "Powerful opening fading to intimate close",
        ArcType.WAVE: "Oscillating waves of intensity",
        ArcType.PEAK: "Classic rise and fall with clear emotional peak",
        ArcType.DOUBLE_PEAK: "Two emotional peaks with reflective valley",
        ArcType.PLATEAU: "Build to sustained intensity before resolution",
        ArcType.FLAT: "Consistent meditative energy throughout",
        ArcType.SAWTOOTH: "Repeated cycles of build and release",
        ArcType.INVERSE_PEAK: "Bookended by intensity with quiet middle",
    }

    journey_descriptions: Dict[EmotionalJourney, str] = {
        EmotionalJourney.TRIUMPH: "A journey from struggle to victory",
        EmotionalJourney.TRAGEDY: "Hope giving way to despair",
        EmotionalJourney.CATHARSIS: "Building tension released through climax",
        EmotionalJourney.MEDITATION: "Sustained contemplative space",
        EmotionalJourney.EUPHORIA: "Growing joy reaching ecstatic heights",
        EmotionalJourney.GRIEF: "Waves of sorrow and remembrance",
        EmotionalJourney.DEFIANCE: "Rising resistance against the inevitable",
        EmotionalJourney.NOSTALGIA: "Bittersweet journey through memory",
        EmotionalJourney.TENSION: "Unresolved buildup seeking release",
        EmotionalJourney.RESOLUTION: "Conflict finding peace",
    }

    arc_desc = descriptions.get(arc.arc_type, "Custom energy curve")
    journey_desc = journey_descriptions.get(arc.emotional_journey, "Emotional journey")

    return f"""Energy Arc: {arc.arc_type.value}
{arc_desc}

Emotional Journey: {arc.emotional_journey.value}
{journey_desc}

Technical Details:
- Energy range: {arc.min_energy:.0%} to {arc.max_energy:.0%}
- Climax: Bar {climax_bar} ({arc.climax_position:.0%} through song)
- Total duration: {arc.total_bars} bars"""


def suggest_arc_for_intent(
    mood: str,
    vulnerability: float = 0.5,
    narrative_arc: str = "transformation"
) -> Tuple[ArcType, EmotionalJourney, float]:
    """
    Suggest an energy arc based on song intent.

    Args:
        mood: Primary mood (grief, anger, joy, nostalgia, etc.)
        vulnerability: Vulnerability scale (0.0-1.0)
        narrative_arc: Narrative type (transformation, cyclical, descent, ascent)

    Returns:
        Tuple of (ArcType, EmotionalJourney, climax_position)
    """
    mood = mood.lower()

    # Map moods to journeys
    mood_journeys: Dict[str, EmotionalJourney] = {
        "grief": EmotionalJourney.GRIEF,
        "sadness": EmotionalJourney.GRIEF,
        "anger": EmotionalJourney.DEFIANCE,
        "rage": EmotionalJourney.DEFIANCE,
        "joy": EmotionalJourney.EUPHORIA,
        "happiness": EmotionalJourney.EUPHORIA,
        "nostalgia": EmotionalJourney.NOSTALGIA,
        "longing": EmotionalJourney.NOSTALGIA,
        "anxiety": EmotionalJourney.TENSION,
        "fear": EmotionalJourney.TENSION,
        "hope": EmotionalJourney.TRIUMPH,
        "determination": EmotionalJourney.TRIUMPH,
        "peace": EmotionalJourney.MEDITATION,
        "calm": EmotionalJourney.MEDITATION,
        "despair": EmotionalJourney.TRAGEDY,
        "loss": EmotionalJourney.TRAGEDY,
        "love": EmotionalJourney.CATHARSIS,
        "heartbreak": EmotionalJourney.GRIEF,
        "release": EmotionalJourney.CATHARSIS,
        "acceptance": EmotionalJourney.RESOLUTION,
    }

    journey = mood_journeys.get(mood, EmotionalJourney.CATHARSIS)

    # Adjust based on narrative arc
    narrative_adjustments: Dict[str, Tuple[Optional[ArcType], float]] = {
        "transformation": (None, 0.75),  # Use journey default
        "cyclical": (ArcType.WAVE, 0.5),
        "descent": (ArcType.EXPONENTIAL_DECAY, 0.15),
        "ascent": (ArcType.EXPONENTIAL_BUILD, 0.95),
        "static": (ArcType.FLAT, 0.5),
        "climactic": (ArcType.PEAK, 0.8),
    }

    arc_override, climax = narrative_adjustments.get(
        narrative_arc.lower(),
        (None, 0.75)
    )

    # Get arc type from journey if not overridden
    if arc_override is None:
        arc_type, default_climax = get_arc_for_journey(journey)
        climax = default_climax
    else:
        arc_type = arc_override

    # Adjust climax based on vulnerability (more vulnerable = earlier climax)
    if vulnerability > 0.7:
        climax = min(climax, 0.65)  # Earlier climax for high vulnerability
    elif vulnerability < 0.3:
        climax = max(climax, 0.8)  # Later climax for low vulnerability

    return arc_type, journey, climax
