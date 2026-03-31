"""Autoplay session state types for the autonomous game loop.

``AutoPlayPhase`` tracks which lifecycle stage the loop is in.
``LoopState`` is the mutable session record — one instance per channel.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum


class AutoPlayPhase(Enum):
    """Lifecycle stages of an autonomous play session."""

    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"


@dataclass
class LoopState:
    """Mutable state for a single autoplay session.

    Attributes:
        phase:       Current lifecycle phase of the session.
        turn_count:  Number of turns completed so far.
        start_time:  Monotonic timestamp when the session started.
        channel_id:  Discord channel ID where the game is running.
        channel_url: URL of the Discord channel (used for navigation).
    """

    phase: AutoPlayPhase = AutoPlayPhase.IDLE
    turn_count: int = 0
    start_time: float = field(default_factory=time.monotonic)
    channel_id: int = 0
    channel_url: str = ""
