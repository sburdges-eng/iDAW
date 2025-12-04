"""
DAW Server module for iDAW Music Brain.

Provides HTTP and OSC servers for DAW plugin integration.
"""

from .server import (
    DAWServer,
    start_server,
    GenerationRequest,
    GenerationResponse,
)

from .protocol import (
    MessageType,
    DAWMessage,
    create_generation_request,
    parse_response,
)

__all__ = [
    "DAWServer",
    "start_server",
    "GenerationRequest",
    "GenerationResponse",
    "MessageType",
    "DAWMessage",
    "create_generation_request",
    "parse_response",
]
