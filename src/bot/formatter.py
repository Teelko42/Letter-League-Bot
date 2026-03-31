"""Embed builders and text-art board renderer for the Letter League Discord bot.

This is a pure-function module: it receives data objects and returns discord.Embed
instances. It holds no state and has no references to Bot or Interaction objects.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import discord

from src.vision.errors import (
    EXTRACTION_FAILED,
    INVALID_SCREENSHOT,
    VALIDATION_FAILED,
    VisNError,
)

if TYPE_CHECKING:
    from src.engine.board import Board
    from src.engine.models import Move


# ---------------------------------------------------------------------------
# Color constants (per user decision — color-coded embeds)
# ---------------------------------------------------------------------------

SUCCESS_COLOR: discord.Color = discord.Color.brand_green()  # green for success
WARNING_COLOR: discord.Color = discord.Color.gold()          # yellow for warnings
ERROR_COLOR: discord.Color = discord.Color.red()             # red for errors
INFO_COLOR: discord.Color = discord.Color.blurple()          # blue for /set* confirmations


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

MAX_WINDOW_COLS = 15  # Caps board window width to avoid Discord line-wrap


def _clamp(val: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, val))


def render_text_board(board: "Board", move: "Move", padding: int = 2) -> str:
    """Render a windowed text-art view of the board centred around *move*.

    The window is bounded by the move's tile positions +/- *padding* cells,
    clamped to board edges and capped at MAX_WINDOW_COLS columns wide.

    Character legend
    ----------------
    ``[X]``  — newly placed tile from the player's rack
    `` X ``  — existing tile already on the board
    `` . ``  — empty cell

    Row and column index labels are added for orientation.

    Args:
        board:    Board instance (used to inspect cells outside the move).
        move:     Move whose tiles define the rendering window.
        padding:  Number of empty cells to show beyond the move's bounding box.

    Returns:
        Multi-line string suitable for wrapping in a Discord monospace code block.
    """
    # Build a fast lookup: (row, col) -> "placed" or "existing" for move tiles
    placed: dict[tuple[int, int], str] = {}
    for tile in move.tiles_used:
        placed[(tile.row, tile.col)] = tile.letter

    new_tiles: set[tuple[int, int]] = {
        (t.row, t.col) for t in move.tiles_used if t.from_rack
    }

    # Bounding box of the move tiles
    rows_in_move = [t.row for t in move.tiles_used]
    cols_in_move = [t.col for t in move.tiles_used]
    min_r = _clamp(min(rows_in_move) - padding, 0, board.rows - 1)
    max_r = _clamp(max(rows_in_move) + padding, 0, board.rows - 1)
    min_c = _clamp(min(cols_in_move) - padding, 0, board.cols - 1)
    max_c = _clamp(max(cols_in_move) + padding, 0, board.cols - 1)

    # Cap width to MAX_WINDOW_COLS
    if (max_c - min_c + 1) > MAX_WINDOW_COLS:
        centre_c = (min(cols_in_move) + max(cols_in_move)) // 2
        half = MAX_WINDOW_COLS // 2
        min_c = _clamp(centre_c - half, 0, board.cols - 1)
        max_c = _clamp(min_c + MAX_WINDOW_COLS - 1, 0, board.cols - 1)

    col_range = range(min_c, max_c + 1)
    row_range = range(min_r, max_r + 1)

    # Header row: column indices (mod 10 for compactness)
    header = "    " + "".join(f"{c % 10:^3}" for c in col_range)
    separator = "    " + "---" * len(col_range)

    lines: list[str] = [header, separator]

    for r in row_range:
        row_label = f"{r:>2} |"
        cells: list[str] = []
        for c in col_range:
            pos = (r, c)
            if pos in new_tiles:
                cells.append(f"[{placed[pos]}]")
            elif pos in placed:
                cells.append(f" {placed[pos]} ")
            else:
                cell = board.grid[r][c]
                if cell.letter is not None:
                    cells.append(f" {cell.letter} ")
                else:
                    cells.append(" . ")
        lines.append(row_label + "".join(cells))

    return "\n".join(lines)


def _format_move_detail(move: "Move") -> str:
    """Return a concise position/tile summary for a single move.

    Format: ``"Across from (row,col) | Tiles: A B C"``
    """
    direction = "Across" if move.direction == "H" else "Down"
    consumed = move.rack_tiles_consumed()
    tiles_str = " ".join(t.letter for t in consumed) if consumed else "—"
    return f"{direction} from ({move.start_row},{move.start_col}) | Tiles: {tiles_str}"


# ---------------------------------------------------------------------------
# Public embed builders
# ---------------------------------------------------------------------------


def build_success_embed(moves: list["Move"], board: "Board") -> discord.Embed:
    """Build a green success embed showing up to 3 top moves.

    The top move's board position is rendered as a text-art code block in the
    embed description. Each move gets a field with word, score, direction, and
    rack tiles consumed.

    Args:
        moves:  Moves sorted by score descending (caller's responsibility). Must
                contain at least one move.
        board:  Board instance used to render the text-art window.

    Returns:
        discord.Embed with green color and up to 3 move fields.
    """
    embed = discord.Embed(
        title="Letter League Analysis",
        color=SUCCESS_COLOR,
    )

    # Text-art board for the top move
    board_art = render_text_board(board, moves[0])
    embed.description = f"```\n{board_art}\n```"

    # Move fields
    for idx, move in enumerate(moves[:3], start=1):
        inline = idx > 1  # move 1 is full-width; 2 and 3 are side-by-side
        embed.add_field(
            name=f"{idx}. {move.word} — {move.score} pts",
            value=_format_move_detail(move),
            inline=inline,
        )

    return embed


def build_error_embed(error: VisNError) -> discord.Embed:
    """Build a red error embed mapped from a VisNError code.

    Each error code maps to a user-facing title and actionable description.

    Args:
        error:  VisNError raised by the vision pipeline.

    Returns:
        discord.Embed with red color and code-specific messaging.
    """
    messages: dict[str, tuple[str, str]] = {
        INVALID_SCREENSHOT: (
            "Couldn't detect a board",
            "Make sure the full game board is visible in your screenshot and try again.",
        ),
        EXTRACTION_FAILED: (
            "Vision API unavailable",
            "The analysis service is temporarily unavailable. Please try again in a moment.",
        ),
        VALIDATION_FAILED: (
            "Board reading failed",
            "The screenshot was unclear or the board couldn't be parsed. "
            "Try a clearer screenshot with good lighting.",
        ),
    }

    title, description = messages.get(
        error.code,
        ("Analysis failed", f"An unexpected error occurred ({error.code}). Please try again."),
    )

    return discord.Embed(title=title, description=description, color=ERROR_COLOR)


def build_error_embed_generic(
    message: str = "Something went wrong. Please try again.",
) -> discord.Embed:
    """Build a red error embed for unexpected (non-VisNError) exceptions.

    Args:
        message:  User-facing error description.

    Returns:
        discord.Embed with red color and generic messaging.
    """
    return discord.Embed(title="Unexpected error", description=message, color=ERROR_COLOR)


def build_no_moves_embed(board: "Board", rack: list[str]) -> discord.Embed:
    """Build a yellow warning embed for the no-valid-placements case.

    Rather than a blank response, surfaces the rack and guides the user toward
    swapping tiles or reconsidering their position.

    Args:
        board:  Current Board (not rendered; used for context if needed later).
        rack:   Player's current rack tiles.

    Returns:
        discord.Embed with gold color and swap-tile guidance.
    """
    rack_display = " ".join(rack) if rack else "(empty)"
    description = (
        f"No valid word placements were found for your rack: **{rack_display}**\n\n"
        "You may want to:\n"
        "- **Swap tiles** to get a more playable set\n"
        "- **Pass** and wait for a better opportunity\n"
        "- Double-check that the screenshot captured the full board"
    )
    return discord.Embed(
        title="No valid placements found",
        description=description,
        color=WARNING_COLOR,
    )


def build_info_embed(title: str, description: str) -> discord.Embed:
    """Build a blurple info embed for /setdifficulty and /setmode confirmations.

    Args:
        title:        Short confirmation title.
        description:  Full confirmation message.

    Returns:
        discord.Embed with blurple color.
    """
    return discord.Embed(title=title, description=description, color=INFO_COLOR)


# ---------------------------------------------------------------------------
# Autoplay embed builders
# ---------------------------------------------------------------------------


def build_turn_embed(move: "Move", turn_count: int) -> discord.Embed:
    """Build a green embed announcing a word played during autoplay.

    Args:
        move:        The Move that was just played.
        turn_count:  Current turn number (1-based).

    Returns:
        discord.Embed with green color, turn number title, and play details.
    """
    direction_word = "across" if move.direction == "H" else "down"
    description = (
        f"Played **{move.word}** {direction_word} "
        f"from ({move.start_row},{move.start_col}) "
        f"for **{move.score} pts**"
    )
    return discord.Embed(
        title=f"Turn {turn_count}",
        description=description,
        color=SUCCESS_COLOR,
    )


def build_swap_embed(turn_count: int) -> discord.Embed:
    """Build a gold warning embed for a tile swap (no valid moves).

    Args:
        turn_count:  Current turn number (1-based).

    Returns:
        discord.Embed with gold color indicating a swap occurred.
    """
    return discord.Embed(
        title=f"Turn {turn_count}",
        description="Swapped tiles (no valid moves)",
        color=WARNING_COLOR,
    )


def build_gameover_embed(turn_count: int) -> discord.Embed:
    """Build a blurple embed announcing the end of an autoplay session.

    Args:
        turn_count:  Total turns played during the session.

    Returns:
        discord.Embed with blurple color and session summary.
    """
    return discord.Embed(
        title="Game Over",
        description=f"The game has ended after **{turn_count}** turns. Autoplay stopped.",
        color=INFO_COLOR,
    )
