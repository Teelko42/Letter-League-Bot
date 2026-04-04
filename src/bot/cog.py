"""AdvisorCog — slash command handlers for the Letter League Discord bot.

Slash commands
--------------
/analyze      Analyze a game screenshot and return top-3 move recommendations.
/setdifficulty Set play strength for the current channel (0-100).
/setmode      Set scoring mode (classic or wild) for the current channel.
"""

from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from src.bot.formatter import (
    build_error_embed,
    build_error_embed_generic,
    build_info_embed,
    build_no_moves_embed,
    build_success_embed,
)
from src.engine.moves import find_all_moves
from src.vision import extract_board_state
from src.vision.errors import VisNError

if TYPE_CHECKING:
    from src.bot.bot import LetterLeagueBot


# ---------------------------------------------------------------------------
# Validation constants
# ---------------------------------------------------------------------------

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp"}
MAX_ATTACHMENT_BYTES = 10_000_000  # 10 MB


class AdvisorCog(commands.Cog):
    """Cog that wires vision + engine + difficulty into Discord slash commands.

    All responses are ephemeral (visible only to the invoking user).
    Heavy engine calls run in a thread pool via asyncio.to_thread to avoid
    blocking the asyncio event loop.
    """

    def __init__(self, bot: "LetterLeagueBot") -> None:
        self.bot = bot

    # ------------------------------------------------------------------
    # /analyze
    # ------------------------------------------------------------------

    @app_commands.command(name="analyze", description="Analyze a Letter League screenshot")
    @app_commands.describe(screenshot="A screenshot of your Letter League game board")
    async def analyze(
        self,
        interaction: discord.Interaction,
        screenshot: discord.Attachment,
    ) -> None:
        """Analyze a game screenshot and return top-3 move recommendations."""

        # Step 1: Defer FIRST — vision API can take 4-15s, must defer immediately.
        await interaction.response.defer(ephemeral=True)

        logger.info("/analyze invoked — channel_id={}", interaction.channel_id)

        # Step 2: Get channel state
        state = self.bot.channel_store.get(interaction.channel_id)

        # Step 3: Validate attachment (before reading bytes)
        content_type = screenshot.content_type or ""
        # Discord may append "; charset=utf-8" — use startswith for each allowed type
        content_type_ok = any(
            content_type.startswith(allowed) for allowed in ALLOWED_CONTENT_TYPES
        )
        if not content_type_ok or screenshot.size > MAX_ATTACHMENT_BYTES:
            await interaction.followup.send(
                embed=build_error_embed_generic(
                    "Please attach a PNG, JPEG, or WebP screenshot (max 10 MB)."
                ),
                ephemeral=True,
            )
            return

        try:
            # Step 4: Read attachment bytes
            img_bytes = await screenshot.read()

            # Step 5: Run vision pipeline (already async, no thread wrapper needed)
            vision_start = time.monotonic()
            board, rack = await extract_board_state(img_bytes, mode=state.mode)
            logger.info("Vision pipeline completed in {:.2f}s", time.monotonic() - vision_start)

            # Step 6: Run engine (CPU-bound sync — must use asyncio.to_thread)
            engine_start = time.monotonic()
            moves = await asyncio.to_thread(
                find_all_moves, board, rack, self.bot.gaddag, state.mode
            )
            logger.info(
                "Engine found {} move(s) in {:.2f}s",
                len(moves),
                time.monotonic() - engine_start,
            )

            # Step 7: Handle no-moves case
            if not moves:
                await interaction.followup.send(
                    embed=build_no_moves_embed(board, rack),
                    ephemeral=True,
                )
                return

            # Step 8: Apply difficulty selection
            if state.difficulty < 100:
                difficulty_start = time.monotonic()
                selected = await asyncio.to_thread(
                    self.bot.difficulty_engine.select_move, moves, state.difficulty
                )
                logger.info(
                    "Difficulty={} selected move '{}' in {:.2f}s",
                    state.difficulty,
                    selected.word if selected else None,
                    time.monotonic() - difficulty_start,
                )
                # Put selected move first, then 2 more with distinct words
                seen_words = {selected.word}
                alternates: list = []
                for m in moves:
                    if m is not selected and m.word not in seen_words:
                        seen_words.add(m.word)
                        alternates.append(m)
                        if len(alternates) == 2:
                            break
                top_moves = [selected] + alternates
            else:
                # Difficulty 100 = optimal — pick top 3 with distinct words
                seen_words: set[str] = set()
                top_moves: list = []
                for m in moves:
                    if m.word not in seen_words:
                        seen_words.add(m.word)
                        top_moves.append(m)
                        if len(top_moves) == 3:
                            break

            # Step 9: Build and send success embed
            embed = build_success_embed(top_moves, board)
            await interaction.followup.send(embed=embed, ephemeral=True)

        except VisNError as e:
            logger.warning("/analyze VisNError: code={} message={}", e.code, e.message)
            await interaction.followup.send(
                embed=build_error_embed(e),
                ephemeral=True,
            )
        except Exception:
            logger.exception("/analyze unexpected error for channel_id={}", interaction.channel_id)
            await interaction.followup.send(
                embed=build_error_embed_generic(),
                ephemeral=True,
            )

    # ------------------------------------------------------------------
    # /setdifficulty
    # ------------------------------------------------------------------

    @app_commands.command(
        name="setdifficulty",
        description="Set bot play strength (0=easy, 100=optimal)",
    )
    @app_commands.describe(strength="Play strength as a percentage (0-100)")
    async def setdifficulty(
        self,
        interaction: discord.Interaction,
        strength: app_commands.Range[int, 0, 100],
    ) -> None:
        """Update the difficulty setting for this channel."""
        self.bot.channel_store.set_difficulty(interaction.channel_id, strength)
        logger.info(
            "/setdifficulty — channel_id={} strength={}",
            interaction.channel_id,
            strength,
        )
        await interaction.response.send_message(
            embed=build_info_embed(
                "Difficulty Updated",
                f"Play strength set to **{strength}%** for this channel.",
            ),
            ephemeral=True,
        )

    # ------------------------------------------------------------------
    # /setmode
    # ------------------------------------------------------------------

    @app_commands.command(
        name="setmode",
        description="Set scoring mode for this channel",
    )
    @app_commands.describe(
        mode="Classic: multipliers apply once. Wild: multipliers bond to tiles permanently."
    )
    @app_commands.choices(
        mode=[
            app_commands.Choice(name="Classic", value="classic"),
            app_commands.Choice(name="Wild", value="wild"),
        ]
    )
    async def setmode(
        self,
        interaction: discord.Interaction,
        mode: app_commands.Choice[str],
    ) -> None:
        """Update the scoring mode for this channel."""
        self.bot.channel_store.set_mode(interaction.channel_id, mode.value)
        logger.info(
            "/setmode — channel_id={} mode={}",
            interaction.channel_id,
            mode.value,
        )
        await interaction.response.send_message(
            embed=build_info_embed(
                "Scoring Mode Updated",
                f"Mode set to **{mode.name}** for this channel.",
            ),
            ephemeral=True,
        )
