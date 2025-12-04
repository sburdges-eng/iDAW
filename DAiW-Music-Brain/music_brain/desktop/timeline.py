"""
Timeline visualization for iDAW Desktop.

Renders arrangement timelines and energy curves for display.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
import json


# Section type colors (for both text and visual rendering)
SECTION_COLORS: Dict[str, str] = {
    "intro": "#4A90D9",      # Blue
    "verse": "#50C878",      # Green
    "prechorus": "#FFD700",  # Gold
    "chorus": "#FF6B6B",     # Red/Pink
    "bridge": "#9B59B6",     # Purple
    "outro": "#4A90D9",      # Blue
    "breakdown": "#95A5A6",  # Gray
    "buildup": "#F39C12",    # Orange
    "drop": "#E74C3C",       # Red
    "solo": "#1ABC9C",       # Teal
    "interlude": "#BDC3C7",  # Light gray
    "hook": "#FF6B6B",       # Red/Pink
}


@dataclass
class TimelineSection:
    """A section in the timeline."""
    name: str
    section_type: str
    start_bar: int
    bars: int
    energy: float
    color: str
    chords: List[str]
    instruments: List[str]

    @property
    def end_bar(self) -> int:
        return self.start_bar + self.bars

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "section_type": self.section_type,
            "start_bar": self.start_bar,
            "bars": self.bars,
            "energy": self.energy,
            "color": self.color,
            "chords": self.chords,
            "instruments": self.instruments,
        }


class TimelineRenderer:
    """
    Renders arrangement timelines for display.

    Supports multiple output formats:
    - ASCII art for terminal
    - HTML for web
    - SVG for graphics
    - Data structure for Streamlit components
    """

    def __init__(self, total_bars: int, beats_per_bar: int = 4):
        self.total_bars = total_bars
        self.beats_per_bar = beats_per_bar
        self.sections: List[TimelineSection] = []

    def add_section(
        self,
        name: str,
        section_type: str,
        start_bar: int,
        bars: int,
        energy: float = 0.5,
        chords: Optional[List[str]] = None,
        instruments: Optional[List[str]] = None,
    ):
        """Add a section to the timeline."""
        color = SECTION_COLORS.get(section_type.lower(), "#95A5A6")

        self.sections.append(TimelineSection(
            name=name,
            section_type=section_type,
            start_bar=start_bar,
            bars=bars,
            energy=energy,
            color=color,
            chords=chords or [],
            instruments=instruments or [],
        ))

    def from_arrangement(self, arrangement: Dict[str, Any]):
        """Load sections from a generated arrangement."""
        self.total_bars = arrangement.get("total_bars", 64)
        self.sections = []

        for section in arrangement.get("sections", []):
            self.add_section(
                name=section.get("name", ""),
                section_type=section.get("section_type", "verse"),
                start_bar=section.get("start_bar", 0),
                bars=section.get("bars", 8),
                energy=section.get("energy", 0.5),
                chords=[c for c, _ in section.get("chords", [])],
                instruments=section.get("instruments", []),
            )

    def render_ascii(self, width: int = 80) -> str:
        """Render timeline as ASCII art."""
        if not self.sections:
            return "No sections to display"

        lines = []

        # Header
        lines.append("=" * width)
        lines.append(f"ARRANGEMENT TIMELINE ({self.total_bars} bars)")
        lines.append("=" * width)

        # Calculate scale
        bar_width = (width - 10) / self.total_bars

        # Render ruler
        ruler = "Bar:  "
        for bar in range(0, self.total_bars + 1, max(1, self.total_bars // 8)):
            pos = int(bar * bar_width)
            ruler = ruler[:6 + pos] + f"{bar}" + ruler[6 + pos + len(str(bar)):]
        lines.append(ruler[:width])

        # Render sections bar
        section_bar = "      "
        for section in self.sections:
            start_pos = int(section.start_bar * bar_width)
            end_pos = int(section.end_bar * bar_width)
            section_width = max(1, end_pos - start_pos)

            # Create section block
            label = section.section_type[:section_width].center(section_width)
            section_bar = section_bar[:6 + start_pos] + label + section_bar[6 + end_pos:]

        lines.append(section_bar[:width])

        # Energy bar
        energy_bar = "Ener: "
        for section in self.sections:
            start_pos = int(section.start_bar * bar_width)
            end_pos = int(section.end_bar * bar_width)
            section_width = max(1, end_pos - start_pos)

            # Energy visualization
            energy_chars = int(section.energy * 10)
            energy_str = ("█" * energy_chars + "░" * (10 - energy_chars))[:section_width]
            energy_bar = energy_bar[:6 + start_pos] + energy_str + energy_bar[6 + end_pos:]

        lines.append(energy_bar[:width])

        lines.append("=" * width)

        # Section details
        lines.append("\nSECTION DETAILS:")
        for section in self.sections:
            lines.append(
                f"  {section.name} ({section.section_type}): "
                f"bars {section.start_bar}-{section.end_bar - 1}, "
                f"energy {section.energy:.0%}"
            )
            if section.chords:
                lines.append(f"    Chords: {' → '.join(section.chords[:4])}")

        return "\n".join(lines)

    def render_html(self) -> str:
        """Render timeline as HTML."""
        html_parts = [
            '<div class="timeline-container" style="font-family: sans-serif; padding: 20px;">',
            f'<h3>Arrangement Timeline ({self.total_bars} bars)</h3>',
            '<div class="timeline" style="display: flex; height: 60px; border: 1px solid #ccc; border-radius: 4px; overflow: hidden;">',
        ]

        for section in self.sections:
            width_pct = (section.bars / self.total_bars) * 100
            html_parts.append(
                f'<div class="section" style="'
                f'width: {width_pct}%; '
                f'background: {section.color}; '
                f'display: flex; align-items: center; justify-content: center; '
                f'color: white; font-size: 12px; text-shadow: 1px 1px 1px rgba(0,0,0,0.5); '
                f'border-right: 1px solid rgba(255,255,255,0.3);" '
                f'title="{section.name}: {section.bars} bars, {section.energy:.0%} energy">'
                f'{section.section_type}'
                f'</div>'
            )

        html_parts.append('</div>')

        # Energy curve
        html_parts.append('<div class="energy-curve" style="margin-top: 10px; height: 40px; display: flex; align-items: flex-end;">')
        for section in self.sections:
            width_pct = (section.bars / self.total_bars) * 100
            height_pct = section.energy * 100
            html_parts.append(
                f'<div style="width: {width_pct}%; height: {height_pct}%; '
                f'background: linear-gradient(to top, {section.color}, {section.color}80); '
                f'border-right: 1px solid #fff;"></div>'
            )
        html_parts.append('</div>')

        html_parts.append('</div>')

        return "\n".join(html_parts)

    def render_svg(self, width: int = 800, height: int = 200) -> str:
        """Render timeline as SVG."""
        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            '<style>',
            '  .section-label { font-family: sans-serif; font-size: 12px; fill: white; }',
            '  .bar-label { font-family: sans-serif; font-size: 10px; fill: #666; }',
            '</style>',
        ]

        # Timeline area
        timeline_y = 40
        timeline_height = 60
        energy_y = 120
        energy_height = 50

        # Render sections
        for section in self.sections:
            x = (section.start_bar / self.total_bars) * width
            w = (section.bars / self.total_bars) * width

            # Section rectangle
            svg_parts.append(
                f'<rect x="{x}" y="{timeline_y}" width="{w}" height="{timeline_height}" '
                f'fill="{section.color}" stroke="white" stroke-width="1"/>'
            )

            # Section label
            label_x = x + w / 2
            svg_parts.append(
                f'<text x="{label_x}" y="{timeline_y + timeline_height / 2 + 4}" '
                f'class="section-label" text-anchor="middle">{section.section_type}</text>'
            )

            # Energy bar
            energy_h = section.energy * energy_height
            energy_bar_y = energy_y + energy_height - energy_h
            svg_parts.append(
                f'<rect x="{x}" y="{energy_bar_y}" width="{w}" height="{energy_h}" '
                f'fill="{section.color}" opacity="0.7"/>'
            )

        # Bar markers
        for bar in range(0, self.total_bars + 1, max(1, self.total_bars // 8)):
            x = (bar / self.total_bars) * width
            svg_parts.append(
                f'<line x1="{x}" y1="{timeline_y - 5}" x2="{x}" y2="{timeline_y}" stroke="#666"/>'
            )
            svg_parts.append(
                f'<text x="{x}" y="{timeline_y - 10}" class="bar-label" text-anchor="middle">{bar}</text>'
            )

        # Labels
        svg_parts.append(f'<text x="10" y="20" class="bar-label">Sections</text>')
        svg_parts.append(f'<text x="10" y="{energy_y - 5}" class="bar-label">Energy</text>')

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def to_streamlit_data(self) -> Dict[str, Any]:
        """
        Return data structure for Streamlit visualization.

        Can be used with st.plotly_chart or custom components.
        """
        return {
            "total_bars": self.total_bars,
            "sections": [s.to_dict() for s in self.sections],
            "colors": SECTION_COLORS,
        }


def render_arrangement_timeline(arrangement: Dict[str, Any], format: str = "ascii") -> str:
    """
    Render an arrangement as a timeline.

    Args:
        arrangement: Arrangement dictionary with sections
        format: Output format - "ascii", "html", or "svg"

    Returns:
        Rendered timeline string
    """
    renderer = TimelineRenderer(arrangement.get("total_bars", 64))
    renderer.from_arrangement(arrangement)

    if format == "html":
        return renderer.render_html()
    elif format == "svg":
        return renderer.render_svg()
    else:
        return renderer.render_ascii()


def render_energy_curve(
    energy_arc: Dict[str, Any],
    width: int = 60,
    height: int = 10
) -> str:
    """
    Render an energy arc as ASCII visualization.

    Args:
        energy_arc: Energy arc dictionary with points
        width: Character width
        height: Character height

    Returns:
        ASCII art energy curve
    """
    points = energy_arc.get("points", [])
    if not points:
        return "No energy data"

    lines = []

    # Create grid
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # Plot points
    for point in points:
        x = int(point["position"] * (width - 1))
        y = height - 1 - int(point["energy"] * (height - 1))

        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = "█"

    # Fill below the curve
    for x in range(width):
        found_point = False
        for y in range(height):
            if grid[y][x] == "█":
                found_point = True
            elif found_point:
                grid[y][x] = "░"

    # Convert to string
    lines.append("Energy Arc:")
    lines.append("┌" + "─" * width + "┐")
    for row in grid:
        lines.append("│" + "".join(row) + "│")
    lines.append("└" + "─" * width + "┘")
    lines.append(f" 0%{' ' * (width - 6)}100%")

    return "\n".join(lines)


def create_plotly_timeline(arrangement: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create Plotly figure data for timeline visualization.

    Returns a dict that can be passed to plotly.graph_objects.Figure()
    or st.plotly_chart().
    """
    sections = arrangement.get("sections", [])
    total_bars = arrangement.get("total_bars", 64)

    # Create Gantt-style data
    data = []
    for section in sections:
        section_type = section.get("section_type", "verse")
        color = SECTION_COLORS.get(section_type, "#95A5A6")

        data.append({
            "type": "bar",
            "x": [section.get("bars", 8)],
            "y": ["Timeline"],
            "orientation": "h",
            "base": section.get("start_bar", 0),
            "marker": {"color": color},
            "name": section.get("name", section_type),
            "hovertemplate": (
                f"<b>{section.get('name', section_type)}</b><br>"
                f"Bars: {section.get('start_bar', 0)}-{section.get('start_bar', 0) + section.get('bars', 8)}<br>"
                f"Energy: {section.get('energy', 0.5):.0%}<br>"
                "<extra></extra>"
            ),
        })

    layout = {
        "title": "Arrangement Timeline",
        "xaxis": {"title": "Bars", "range": [0, total_bars]},
        "yaxis": {"visible": False},
        "barmode": "stack",
        "showlegend": True,
        "height": 150,
        "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
    }

    return {"data": data, "layout": layout}
