"""
iDAW Collaboration Module.

Real-time multi-user session sharing for collaborative music production.
"""

from .websocket_server import (
    CollaborationServer,
    Session,
    Participant,
    MessageType,
)

__all__ = [
    "CollaborationServer",
    "Session",
    "Participant",
    "MessageType",
]
