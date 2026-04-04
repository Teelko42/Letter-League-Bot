"""Tests for AdvisorCog (Phase B3).

All discord.py interactions, vision pipeline, and engine are mocked.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.bot.cog import AdvisorCog, MAX_ATTACHMENT_BYTES
from src.engine.models import Move, ScoreBreakdown, TileUse
from src.vision.errors import EXTRACTION_FAILED, VisNError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_bot() -> MagicMock:
    bot = MagicMock()
    bot.gaddag = MagicMock()
    bot.difficulty_engine = MagicMock()

    ch_state = MagicMock()
    ch_state.mode = "wild"
    ch_state.difficulty = 100
    bot.channel_store = MagicMock()
    bot.channel_store.get.return_value = ch_state

    return bot


def _make_interaction(channel_id: int = 42) -> MagicMock:
    interaction = MagicMock()
    interaction.channel_id = channel_id
    interaction.response = AsyncMock()
    interaction.response.defer = AsyncMock()
    interaction.response.send_message = AsyncMock()
    interaction.followup = AsyncMock()
    interaction.followup.send = AsyncMock()
    return interaction


def _make_attachment(
    content_type: str = "image/png",
    size: int = 50_000,
) -> MagicMock:
    att = MagicMock()
    att.content_type = content_type
    att.size = size
    att.read = AsyncMock(return_value=b"\x89PNG fake image bytes")
    return att


def _make_move(word: str = "TEST", score: int = 20) -> Move:
    return Move(
        word=word,
        start_row=0,
        start_col=0,
        direction="H",
        tiles_used=[
            TileUse(row=0, col=i, letter=ch, is_blank=False, from_rack=True)
            for i, ch in enumerate(word)
        ],
        score_breakdown=ScoreBreakdown(base_letter_sum=score, word_multiplier=1, total=score),
        score=score,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestAnalyze:
    @pytest.mark.asyncio
    async def test_rejects_oversized_attachment(self):
        bot = _make_bot()
        cog = AdvisorCog(bot)
        interaction = _make_interaction()
        att = _make_attachment(size=MAX_ATTACHMENT_BYTES + 1)

        await cog.analyze.callback(cog, interaction, att)

        interaction.followup.send.assert_called_once()
        call_kwargs = interaction.followup.send.call_args
        assert call_kwargs.kwargs.get("ephemeral") is True

    @pytest.mark.asyncio
    async def test_rejects_wrong_content_type(self):
        bot = _make_bot()
        cog = AdvisorCog(bot)
        interaction = _make_interaction()
        att = _make_attachment(content_type="text/plain")

        await cog.analyze.callback(cog, interaction, att)

        interaction.followup.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_success_returns_top_3(self):
        bot = _make_bot()
        cog = AdvisorCog(bot)
        interaction = _make_interaction()
        att = _make_attachment()

        moves = [_make_move(w, s) for w, s in [("ABCDE", 50), ("BCDEF", 40), ("CDEFG", 30), ("DEFGH", 20), ("EFGHI", 10)]]
        mock_board = MagicMock()

        with (
            patch("src.bot.cog.extract_board_state", new_callable=AsyncMock, return_value=(mock_board, ["A", "B"])),
            patch("src.bot.cog.find_all_moves", return_value=moves),
            patch("src.bot.cog.build_success_embed") as mock_embed,
        ):
            await cog.analyze.callback(cog, interaction, att)

        # Top 3 distinct words
        called_moves = mock_embed.call_args[0][0]
        assert len(called_moves) == 3

    @pytest.mark.asyncio
    async def test_no_moves_returns_no_moves_embed(self):
        bot = _make_bot()
        cog = AdvisorCog(bot)
        interaction = _make_interaction()
        att = _make_attachment()

        mock_board = MagicMock()

        with (
            patch("src.bot.cog.extract_board_state", new_callable=AsyncMock, return_value=(mock_board, ["A"])),
            patch("src.bot.cog.find_all_moves", return_value=[]),
            patch("src.bot.cog.build_no_moves_embed") as mock_no_moves,
        ):
            await cog.analyze.callback(cog, interaction, att)

        mock_no_moves.assert_called_once()

    @pytest.mark.asyncio
    async def test_vision_error_returns_error_embed(self):
        bot = _make_bot()
        cog = AdvisorCog(bot)
        interaction = _make_interaction()
        att = _make_attachment()

        with (
            patch("src.bot.cog.extract_board_state", new_callable=AsyncMock, side_effect=VisNError(EXTRACTION_FAILED, "bad")),
            patch("src.bot.cog.build_error_embed") as mock_err,
        ):
            await cog.analyze.callback(cog, interaction, att)

        mock_err.assert_called_once()

    @pytest.mark.asyncio
    async def test_unexpected_error_returns_generic_error(self):
        bot = _make_bot()
        cog = AdvisorCog(bot)
        interaction = _make_interaction()
        att = _make_attachment()

        with (
            patch("src.bot.cog.extract_board_state", new_callable=AsyncMock, side_effect=RuntimeError("boom")),
            patch("src.bot.cog.build_error_embed_generic") as mock_generic,
        ):
            await cog.analyze.callback(cog, interaction, att)

        mock_generic.assert_called_once()

    @pytest.mark.asyncio
    async def test_with_difficulty_below_100(self):
        bot = _make_bot()
        bot.channel_store.get.return_value.difficulty = 50
        bot.difficulty_engine.select_move.return_value = _make_move("PICK", 30)
        cog = AdvisorCog(bot)
        interaction = _make_interaction()
        att = _make_attachment()

        moves = [_make_move("ABCDE", 50), _make_move("BCDEF", 40)]
        mock_board = MagicMock()

        with (
            patch("src.bot.cog.extract_board_state", new_callable=AsyncMock, return_value=(mock_board, ["A"])),
            patch("src.bot.cog.find_all_moves", return_value=moves),
            patch("src.bot.cog.build_success_embed"),
            patch("src.bot.cog.asyncio.to_thread", new_callable=AsyncMock) as mock_thread,
        ):
            # to_thread is called twice: once for find_all_moves, once for select_move
            mock_thread.side_effect = [moves, _make_move("PICK", 30)]
            await cog.analyze.callback(cog, interaction, att)

        # difficulty_engine.select_move was called via to_thread
        assert mock_thread.call_count == 2

    @pytest.mark.asyncio
    async def test_defers_response(self):
        bot = _make_bot()
        cog = AdvisorCog(bot)
        interaction = _make_interaction()
        att = _make_attachment()

        with (
            patch("src.bot.cog.extract_board_state", new_callable=AsyncMock, return_value=(MagicMock(), ["A"])),
            patch("src.bot.cog.find_all_moves", return_value=[_make_move()]),
            patch("src.bot.cog.build_success_embed"),
        ):
            await cog.analyze.callback(cog, interaction, att)

        interaction.response.defer.assert_called_once_with(ephemeral=True)


class TestSetDifficulty:
    @pytest.mark.asyncio
    async def test_updates_channel_state(self):
        bot = _make_bot()
        cog = AdvisorCog(bot)
        interaction = _make_interaction(channel_id=99)

        await cog.setdifficulty.callback(cog, interaction, 75)

        bot.channel_store.set_difficulty.assert_called_once_with(99, 75)


class TestSetMode:
    @pytest.mark.asyncio
    async def test_updates_channel_state(self):
        bot = _make_bot()
        cog = AdvisorCog(bot)
        interaction = _make_interaction(channel_id=99)

        mode_choice = MagicMock()
        mode_choice.value = "classic"
        mode_choice.name = "Classic"

        await cog.setmode.callback(cog, interaction, mode_choice)

        bot.channel_store.set_mode.assert_called_once_with(99, "classic")
