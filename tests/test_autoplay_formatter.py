"""Unit tests for autoplay embed builders and state types.

Tests cover:
- build_turn_embed: title, description (word, score, direction, position), color
- build_swap_embed: title, description, color
- build_gameover_embed: title, description (turn count), color
- LoopState: default field values
- AutoPlayPhase: exactly 4 members with expected names
"""

from __future__ import annotations

import discord
import pytest

from src.bot.autoplay_state import AutoPlayPhase, LoopState
from src.bot.formatter import (
    INFO_COLOR,
    SUCCESS_COLOR,
    WARNING_COLOR,
    build_gameover_embed,
    build_swap_embed,
    build_turn_embed,
)
from src.engine.models import Move, ScoreBreakdown, TileUse


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_move(direction: str = "H") -> Move:
    """Construct a minimal Move with known values for assertion."""
    return Move(
        word="QUEST",
        start_row=5,
        start_col=3,
        direction=direction,
        tiles_used=[
            TileUse(row=5, col=3, letter="Q", is_blank=False, from_rack=True),
        ],
        score_breakdown=ScoreBreakdown(base_letter_sum=0, word_multiplier=1, total=42),
        score=42,
    )


# ---------------------------------------------------------------------------
# build_turn_embed
# ---------------------------------------------------------------------------

def test_turn_embed_horizontal() -> None:
    move = _make_move(direction="H")
    embed = build_turn_embed(move, turn_count=5)

    assert embed.title == "Turn 5"
    assert "QUEST" in embed.description
    assert "42 pts" in embed.description
    assert "across" in embed.description
    assert "(5,3)" in embed.description
    assert embed.color == SUCCESS_COLOR


def test_turn_embed_vertical() -> None:
    move = _make_move(direction="V")
    embed = build_turn_embed(move, turn_count=3)

    assert "down" in embed.description


# ---------------------------------------------------------------------------
# build_swap_embed
# ---------------------------------------------------------------------------

def test_swap_embed() -> None:
    embed = build_swap_embed(turn_count=8)

    assert embed.title == "Turn 8"
    assert "Swapped tiles" in embed.description
    assert embed.color == WARNING_COLOR


# ---------------------------------------------------------------------------
# build_gameover_embed
# ---------------------------------------------------------------------------

def test_gameover_embed() -> None:
    embed = build_gameover_embed(turn_count=12)

    assert embed.title == "Game Over"
    assert "12" in embed.description
    assert embed.color == INFO_COLOR


# ---------------------------------------------------------------------------
# LoopState defaults
# ---------------------------------------------------------------------------

def test_loop_state_defaults() -> None:
    state = LoopState()

    assert state.phase == AutoPlayPhase.IDLE
    assert state.turn_count == 0
    assert state.channel_id == 0
    assert state.channel_url == ""


# ---------------------------------------------------------------------------
# AutoPlayPhase members
# ---------------------------------------------------------------------------

def test_autoplay_phase_members() -> None:
    members = set(AutoPlayPhase)

    assert len(members) == 4
    assert AutoPlayPhase.IDLE in members
    assert AutoPlayPhase.STARTING in members
    assert AutoPlayPhase.RUNNING in members
    assert AutoPlayPhase.STOPPING in members
