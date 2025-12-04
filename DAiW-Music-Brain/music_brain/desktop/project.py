"""
Project management for iDAW Desktop.

Handles project creation, saving, loading, and state management.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid


@dataclass
class ProjectIntent:
    """Intent data for a project."""
    # Phase 0: Core
    core_event: str = ""
    core_resistance: str = ""
    core_longing: str = ""

    # Phase 1: Emotional
    mood_primary: str = ""
    mood_secondary: str = ""
    vulnerability: float = 0.5
    narrative_arc: str = "transformation"

    # Phase 2: Technical
    genre: str = "pop"
    key: str = "C"
    tempo: float = 120.0
    time_signature: tuple = (4, 4)
    chord_progression: List[str] = field(default_factory=list)
    rule_to_break: str = ""
    rule_justification: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["time_signature"] = list(self.time_signature)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectIntent":
        if "time_signature" in data:
            data["time_signature"] = tuple(data["time_signature"])
        return cls(**data)

    def is_complete(self) -> bool:
        """Check if all required fields are filled."""
        return bool(
            self.core_event and
            self.mood_primary and
            self.genre and
            self.key
        )


@dataclass
class ProjectArrangement:
    """Generated arrangement data."""
    sections: List[Dict[str, Any]] = field(default_factory=list)
    chord_progression: List[str] = field(default_factory=list)
    bass_lines: Dict[str, Any] = field(default_factory=dict)
    energy_arc: Dict[str, Any] = field(default_factory=dict)
    production_notes: str = ""
    total_bars: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectArrangement":
        return cls(**data)


@dataclass
class Project:
    """Complete iDAW project."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = "Untitled Project"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "1.0.0"

    intent: ProjectIntent = field(default_factory=ProjectIntent)
    arrangement: Optional[ProjectArrangement] = None

    # Project state
    current_phase: int = 0  # 0, 1, or 2
    is_generated: bool = False
    file_path: Optional[str] = None

    # Export history
    exports: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "version": self.version,
            "intent": self.intent.to_dict(),
            "arrangement": self.arrangement.to_dict() if self.arrangement else None,
            "current_phase": self.current_phase,
            "is_generated": self.is_generated,
            "exports": self.exports,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        intent = ProjectIntent.from_dict(data.get("intent", {}))
        arrangement = None
        if data.get("arrangement"):
            arrangement = ProjectArrangement.from_dict(data["arrangement"])

        return cls(
            id=data.get("id", str(uuid.uuid4())[:8]),
            title=data.get("title", "Untitled Project"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            modified_at=data.get("modified_at", datetime.now().isoformat()),
            version=data.get("version", "1.0.0"),
            intent=intent,
            arrangement=arrangement,
            current_phase=data.get("current_phase", 0),
            is_generated=data.get("is_generated", False),
            exports=data.get("exports", []),
        )

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: Optional[str] = None) -> str:
        """Save project to file."""
        if path:
            self.file_path = path
        elif not self.file_path:
            # Default to title-based filename
            safe_title = "".join(c if c.isalnum() or c in "._- " else "_" for c in self.title)
            self.file_path = f"{safe_title.lower().replace(' ', '_')}.idaw"

        self.modified_at = datetime.now().isoformat()

        Path(self.file_path).write_text(self.to_json())
        return self.file_path

    @classmethod
    def load(cls, path: str) -> "Project":
        """Load project from file."""
        data = json.loads(Path(path).read_text())
        project = cls.from_dict(data)
        project.file_path = path
        return project

    def update_intent(self, **kwargs):
        """Update intent fields."""
        for key, value in kwargs.items():
            if hasattr(self.intent, key):
                setattr(self.intent, key, value)
        self.modified_at = datetime.now().isoformat()

    def set_arrangement(self, arrangement_data: Dict[str, Any]):
        """Set generated arrangement."""
        self.arrangement = ProjectArrangement.from_dict(arrangement_data)
        self.is_generated = True
        self.modified_at = datetime.now().isoformat()

    def add_export(self, export_type: str, file_path: str):
        """Record an export."""
        self.exports.append({
            "type": export_type,
            "path": file_path,
            "timestamp": datetime.now().isoformat(),
        })


class ProjectManager:
    """Manages multiple projects and recent files."""

    def __init__(self, projects_dir: Optional[str] = None):
        self.projects_dir = Path(projects_dir or os.path.expanduser("~/.idaw/projects"))
        self.projects_dir.mkdir(parents=True, exist_ok=True)

        self.recent_file = self.projects_dir.parent / "recent_projects.json"
        self.recent_projects: List[Dict[str, str]] = []
        self._load_recent()

    def _load_recent(self):
        """Load recent projects list."""
        if self.recent_file.exists():
            try:
                self.recent_projects = json.loads(self.recent_file.read_text())
            except json.JSONDecodeError:
                self.recent_projects = []

    def _save_recent(self):
        """Save recent projects list."""
        self.recent_file.parent.mkdir(parents=True, exist_ok=True)
        self.recent_file.write_text(json.dumps(self.recent_projects, indent=2))

    def add_recent(self, project: Project):
        """Add project to recent list."""
        entry = {
            "id": project.id,
            "title": project.title,
            "path": project.file_path,
            "modified_at": project.modified_at,
        }

        # Remove if already exists
        self.recent_projects = [
            p for p in self.recent_projects if p.get("id") != project.id
        ]

        # Add to front
        self.recent_projects.insert(0, entry)

        # Keep only last 10
        self.recent_projects = self.recent_projects[:10]

        self._save_recent()

    def get_recent(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent projects."""
        return self.recent_projects[:limit]

    def create_project(self, title: str = "Untitled Project") -> Project:
        """Create a new project."""
        project = Project(title=title)
        return project

    def save_project(self, project: Project, path: Optional[str] = None) -> str:
        """Save project and update recent list."""
        if not path and not project.file_path:
            path = str(self.projects_dir / f"{project.id}.idaw")

        saved_path = project.save(path)
        self.add_recent(project)
        return saved_path

    def load_project(self, path: str) -> Project:
        """Load project and update recent list."""
        project = Project.load(path)
        self.add_recent(project)
        return project

    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects in projects directory."""
        projects = []
        for path in self.projects_dir.glob("*.idaw"):
            try:
                project = Project.load(str(path))
                projects.append({
                    "id": project.id,
                    "title": project.title,
                    "path": str(path),
                    "modified_at": project.modified_at,
                    "is_generated": project.is_generated,
                })
            except (json.JSONDecodeError, KeyError):
                continue

        # Sort by modified date
        projects.sort(key=lambda p: p["modified_at"], reverse=True)
        return projects


# Convenience functions
def create_project(title: str = "Untitled Project") -> Project:
    """Create a new project."""
    return Project(title=title)


def load_project(path: str) -> Project:
    """Load a project from file."""
    return Project.load(path)


def save_project(project: Project, path: Optional[str] = None) -> str:
    """Save a project to file."""
    return project.save(path)
