"""Per-channel state management for the Letter League Discord bot.

Each Discord channel gets isolated settings (difficulty, mode) stored in-memory.
Settings reset on bot restart — no persistence layer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ChannelState:
    """Settings scoped to a single Discord channel.

    Attributes:
        difficulty: Strength percentage 0-100. 100 = optimal play (strongest),
            0 = weakest possible move. Default: 100.
        mode:       Game mode — "classic" or "wild". Default: "classic".
    """
    difficulty: int = 100
    mode: str = "classic"


class ChannelStore:
    """In-memory store of per-channel settings keyed by Discord channel ID.

    Thread-safety: the bot runs a single-threaded asyncio event loop, so a plain
    dict is sufficient here (no locking required).
    """

    def __init__(self) -> None:
        self._store: dict[int, ChannelState] = {}

    def get(self, channel_id: int) -> ChannelState:
        """Return the ChannelState for *channel_id*, creating defaults on first access."""
        if channel_id not in self._store:
            self._store[channel_id] = ChannelState()
        return self._store[channel_id]

    def set_difficulty(self, channel_id: int, difficulty: int) -> ChannelState:
        """Update difficulty for *channel_id* and return the updated state.

        Args:
            channel_id:  Discord channel snowflake ID.
            difficulty:  New difficulty percentage (0-100).

        Returns:
            Updated ChannelState.
        """
        state = self.get(channel_id)
        state.difficulty = difficulty
        return state

    def set_mode(self, channel_id: int, mode: str) -> ChannelState:
        """Update game mode for *channel_id* and return the updated state.

        Args:
            channel_id:  Discord channel snowflake ID.
            mode:        "classic" or "wild".

        Returns:
            Updated ChannelState.
        """
        state = self.get(channel_id)
        state.mode = mode
        return state
