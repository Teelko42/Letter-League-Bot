"""Tests for LetterLeagueBot initialization (Phase C4).

GADDAG and Discord are mocked.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.bot.bot import LetterLeagueBot
from src.bot.channel_state import ChannelStore


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestLetterLeagueBotInit:
    def test_bot_init_stores_paths(self):
        bot = LetterLeagueBot(
            wordlist_path=Path("/tmp/words.txt"),
            cache_path=Path("/tmp/cache.pkl"),
        )
        assert bot._wordlist_path == Path("/tmp/words.txt")
        assert bot._cache_path == Path("/tmp/cache.pkl")

    def test_bot_creates_channel_store(self):
        bot = LetterLeagueBot(wordlist_path=Path("/tmp/words.txt"))
        assert isinstance(bot.channel_store, ChannelStore)

    def test_bot_gaddag_initially_none(self):
        bot = LetterLeagueBot(wordlist_path=Path("/tmp/words.txt"))
        assert bot.gaddag is None
        assert bot.difficulty_engine is None

    @pytest.mark.asyncio
    async def test_setup_hook_loads_gaddag(self):
        bot = LetterLeagueBot(
            wordlist_path=Path("/tmp/words.txt"),
            cache_path=Path("/tmp/cache.pkl"),
        )

        mock_gaddag = MagicMock()
        mock_difficulty = MagicMock()

        with (
            patch("src.bot.bot.asyncio.to_thread", new_callable=AsyncMock, return_value=mock_gaddag),
            patch("src.bot.bot.DifficultyEngine", return_value=mock_difficulty),
            patch.object(bot, "add_cog", new_callable=AsyncMock),
            patch.object(type(bot), "tree", new_callable=lambda: MagicMock(sync=AsyncMock(), copy_global_to=MagicMock())),
        ):
            await bot.setup_hook()

        assert bot.gaddag is mock_gaddag

    @pytest.mark.asyncio
    async def test_setup_hook_loads_difficulty_engine(self):
        bot = LetterLeagueBot(
            wordlist_path=Path("/tmp/words.txt"),
            cache_path=Path("/tmp/cache.pkl"),
        )

        mock_gaddag = MagicMock()
        mock_difficulty = MagicMock()

        with (
            patch("src.bot.bot.asyncio.to_thread", new_callable=AsyncMock, return_value=mock_gaddag),
            patch("src.bot.bot.DifficultyEngine", return_value=mock_difficulty),
            patch.object(bot, "add_cog", new_callable=AsyncMock),
            patch.object(type(bot), "tree", new_callable=lambda: MagicMock(sync=AsyncMock(), copy_global_to=MagicMock())),
        ):
            await bot.setup_hook()

        assert bot.difficulty_engine is mock_difficulty
