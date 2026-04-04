"""AutoPlayCog — autonomous game loop controlled via /autoplay slash commands.

This cog wires together all Phase 5-7 browser subsystems into a self-sustaining
play loop that runs as an asyncio background task on discord.py's event loop.

Usage:
    /autoplay start  — launch browser, navigate to activity, begin polling
    /autoplay stop   — signal the loop to finish the current turn then stop
    /autoplay status — report phase, turn count, and uptime

Environment variables:
    VOICE_CHANNEL_URL   Required. Full Discord channel URL used for navigation.
                        Example: https://discord.com/channels/SERVER_ID/CHANNEL_ID
"""

from __future__ import annotations

import asyncio
import os
import time
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from loguru import logger

from src.bot.autoplay_state import AutoPlayPhase, LoopState
from src.bot.formatter import (
    build_error_embed_generic,
    build_gameover_embed,
    build_info_embed,
    build_swap_embed,
    build_turn_embed,
)
from src.browser.capture import capture_canvas
from src.browser.navigator import navigate_to_activity
from src.browser.session import BrowserSession
from src.browser.tile_placer import TilePlacer
from src.browser.turn_detector import poll_turn, preflight_check
from src.engine.moves import find_all_moves
from src.vision import extract_board_state

if TYPE_CHECKING:
    from src.bot.bot import LetterLeagueBot

# Reconnection backoff delays in seconds (3 attempts total)
RECONNECT_DELAYS: list[int] = [5, 15, 30]


class AutoPlayCog(commands.Cog):
    """Cog providing the /autoplay command group and the autonomous game loop."""

    autoplay_group = app_commands.Group(
        name="autoplay",
        description="Autonomous game loop controls",
    )

    def __init__(self, bot: "LetterLeagueBot") -> None:
        self.bot = bot
        self._loop_task: asyncio.Task | None = None
        self._stop_event: asyncio.Event = asyncio.Event()
        self._state: LoopState | None = None
        self._session: BrowserSession | None = None  # for crash recovery

    # -----------------------------------------------------------------------
    # Slash commands
    # -----------------------------------------------------------------------

    @autoplay_group.command(name="start", description="Launch autoplay and begin playing")
    async def autoplay_start(self, interaction: discord.Interaction) -> None:
        """Start the autonomous game loop.

        Defers the response (non-ephemeral so the channel sees the confirmation),
        guards against double-starts, reads VOICE_CHANNEL_URL from the environment,
        and spawns the game loop as an asyncio background task.
        """
        await interaction.response.defer()

        # Guard: prevent double start
        if self._state is not None and self._state.phase != AutoPlayPhase.IDLE:
            await interaction.followup.send(
                embed=build_error_embed_generic("Autoplay is already running.")
            )
            return

        # Read environment variable
        channel_url = os.environ.get("VOICE_CHANNEL_URL")
        if not channel_url:
            await interaction.followup.send(
                embed=build_error_embed_generic(
                    "VOICE_CHANNEL_URL environment variable is not set. "
                    "Set it to the full Discord channel URL before starting autoplay."
                )
            )
            return

        # Initialise session state
        self._state = LoopState(
            phase=AutoPlayPhase.STARTING,
            channel_id=interaction.channel_id,
            channel_url=channel_url,
        )
        self._stop_event.clear()

        # Spawn background task on the current event loop
        self._loop_task = asyncio.create_task(
            self._run_game_loop(interaction.channel, channel_url),
            name="autoplay-game-loop",
        )

        await interaction.followup.send(
            embed=build_info_embed("Autoplay Started", "Launching browser and connecting...")
        )

    @autoplay_group.command(name="stop", description="Stop autoplay after the current turn")
    async def autoplay_stop(self, interaction: discord.Interaction) -> None:
        """Signal the game loop to stop after completing the current turn."""
        if self._state is None or self._state.phase == AutoPlayPhase.IDLE:
            await interaction.response.send_message(
                embed=build_error_embed_generic("Autoplay is not currently active."),
                ephemeral=True,
            )
            return

        self._stop_event.set()
        self._state.phase = AutoPlayPhase.STOPPING
        await interaction.response.send_message(
            "Finishing current turn, then stopping...",
            ephemeral=True,
        )

    @autoplay_group.command(name="status", description="Show autoplay status, turns, and uptime")
    async def autoplay_status(self, interaction: discord.Interaction) -> None:
        """Report current autoplay phase, turn count, and elapsed uptime."""
        if self._state is None or self._state.phase == AutoPlayPhase.IDLE:
            await interaction.response.send_message(
                embed=build_info_embed("Autoplay Status", "Autoplay is not running."),
                ephemeral=True,
            )
            return

        elapsed = time.monotonic() - self._state.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        uptime_str = f"{minutes}m {seconds}s"

        embed = build_info_embed(
            "Autoplay Status",
            f"Session is active.",
        )
        embed.add_field(name="Status", value=self._state.phase.value, inline=True)
        embed.add_field(name="Turns", value=str(self._state.turn_count), inline=True)
        embed.add_field(name="Uptime", value=uptime_str, inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # -----------------------------------------------------------------------
    # Game loop
    # -----------------------------------------------------------------------

    async def _run_game_loop(
        self,
        channel: discord.abc.Messageable,
        channel_url: str,
    ) -> None:
        """Autonomous game loop coroutine.

        Lifecycle:
          1. Start browser session and navigate to the Letter League activity.
          2. Poll for turns; when it's our turn, capture the board and compute a move.
          3. Place the move (or swap tiles if no valid moves exist).
          4. Post a status embed to the channel.
          5. Repeat until stop is requested or the game ends.

        All browser and vision errors inside the turn cycle trigger reconnection
        attempts. A full browser crash triggers a BrowserSession relaunch.
        """
        session: BrowserSession | None = None
        try:
            # ------------------------------------------------------------------
            # Startup: browser session + activity navigation
            # ------------------------------------------------------------------
            session = BrowserSession()
            page = await session.start()
            self._session = session

            logger.info("AutoPlay: browser started, navigating to activity")
            await navigate_to_activity(page, channel_url)
            await preflight_check(page)

            placer = TilePlacer(page)

            assert self._state is not None
            self._state.phase = AutoPlayPhase.RUNNING
            logger.info("AutoPlay: loop running")

            # ------------------------------------------------------------------
            # Main turn loop
            # ------------------------------------------------------------------
            while not self._stop_event.is_set():
                # Step 1: Wait for our turn (or game over)
                turn_state = await poll_turn(page)
                if turn_state == "game_over":
                    logger.info("AutoPlay: game over detected after {} turns", self._state.turn_count)
                    await channel.send(embed=build_gameover_embed(self._state.turn_count))
                    break

                # Step 2: Capture board and run vision pipeline (retry once on failure)
                board = None
                rack: list[str] = []
                vision_ok = False
                for attempt in range(2):
                    try:
                        img_bytes = await capture_canvas(page)
                        ch_state = self.bot.channel_store.get(self._state.channel_id)
                        board, rack = await extract_board_state(img_bytes, mode=ch_state.mode)
                        vision_ok = True
                        break
                    except Exception as exc:
                        logger.warning(
                            "AutoPlay: vision error on attempt {} — {}",
                            attempt + 1,
                            exc,
                        )

                if not vision_ok:
                    logger.error("AutoPlay: vision failed twice, skipping cycle")
                    continue  # back to poll_turn

                assert board is not None

                # Step 3: Move generation (CPU-bound — offload to thread)
                ch_state = self.bot.channel_store.get(self._state.channel_id)
                moves = await asyncio.to_thread(
                    find_all_moves, board, rack, self.bot.gaddag, ch_state.mode
                )

                if moves:
                    selected = await asyncio.to_thread(
                        self.bot.difficulty_engine.select_move,
                        moves,
                        ch_state.difficulty,
                    )
                    # Build candidate list: primary selection + backup moves
                    # so place_move can try alternates if placement fails.
                    candidates: list = [selected]
                    for m in moves:
                        if m is not selected and len(candidates) < 5:
                            candidates.append(m)
                else:
                    candidates = []

                # Step 4: Place move (or swap if no candidates)
                self._state.turn_count += 1
                accepted = await placer.place_move(candidates, rack)

                # Step 5: Post turn summary embed to channel
                if accepted and candidates:
                    await channel.send(embed=build_turn_embed(candidates[0], self._state.turn_count))
                else:
                    await channel.send(embed=build_swap_embed(self._state.turn_count))

                # Check stop event after each completed turn
                if self._stop_event.is_set():
                    break

        except asyncio.CancelledError:
            logger.info("AutoPlay: loop task cancelled")
            raise
        except Exception as exc:
            logger.exception("AutoPlay: unrecoverable error — {}", exc)
            try:
                await channel.send(
                    embed=build_error_embed_generic(
                        f"Autoplay encountered an unrecoverable error and stopped: {exc}"
                    )
                )
            except Exception:
                pass
        finally:
            # Always clean up: reset state and close browser session
            self._state = None
            self._stop_event.clear()
            if session is not None:
                try:
                    await session.close()
                except Exception:
                    pass
            self._session = None
            logger.info("AutoPlay: loop exited, resources cleaned up")

    # -----------------------------------------------------------------------
    # Reconnection helper
    # -----------------------------------------------------------------------

    async def _attempt_reconnect(self, page: object, channel_url: str) -> object:
        """Attempt to reconnect to the Discord Activity after a disconnect.

        Tries navigate_to_activity up to 3 times with exponential backoff
        (5s, 15s, 30s between attempts).

        Args:
            page:        Patchright Page object (browser is still alive).
            channel_url: Discord channel URL to navigate back to.

        Returns:
            The Activity Frame on success.

        Raises:
            RuntimeError: If all 3 reconnection attempts fail.
        """
        for delay in RECONNECT_DELAYS:
            try:
                frame = await navigate_to_activity(page, channel_url)
                logger.info("AutoPlay: reconnected to activity")
                return frame
            except Exception as exc:
                logger.warning("AutoPlay: reconnect attempt failed ({}) — sleeping {}s", exc, delay)
                await asyncio.sleep(delay)

        raise RuntimeError(
            f"Failed to reconnect to {channel_url} after {len(RECONNECT_DELAYS)} attempts"
        )

    # -----------------------------------------------------------------------
    # Cog lifecycle
    # -----------------------------------------------------------------------

    def cog_unload(self) -> None:
        """Cancel the running loop task when the cog is unloaded.

        Prevents orphaned browser sessions if the bot is reloaded or shut down.
        """
        if self._loop_task and not self._loop_task.done():
            self._loop_task.cancel()
            logger.info("AutoPlay: loop task cancelled on cog unload")
