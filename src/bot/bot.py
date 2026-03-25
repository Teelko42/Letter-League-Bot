"""LetterLeagueBot — discord.py Commands.Bot subclass and main entry point.

Run the bot:
    python -m src.bot.bot

Environment variables (load via .env):
    DISCORD_TOKEN           Required. Bot token from Discord Developer Portal.
    WORDLIST_PATH           Optional. Path to wordlist file (default: data/wordlist.txt).
    GADDAG_CACHE_PATH       Optional. Path to GADDAG pickle cache (default: cache/gaddag.pkl).
    DISCORD_TEST_GUILD_ID   Optional. Guild ID for instant command sync during development.
                            When set, commands sync to the test guild immediately rather
                            than waiting up to 1 hour for global propagation.
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv
from loguru import logger

from src.bot.channel_state import ChannelStore
from src.difficulty.engine import DifficultyEngine
from src.engine.gaddag import GADDAG


class LetterLeagueBot(commands.Bot):
    """Discord bot that loads the GADDAG and DifficultyEngine on startup.

    The bot holds all heavy shared resources as instance attributes so that
    command cogs (added in Plan 04-02) can access them directly via
    ``interaction.client.gaddag`` etc.

    Resources are loaded in ``setup_hook`` (called before READY) so that the
    bot refuses to start at all if the GADDAG file is missing or corrupt — a
    bot that starts without its core resource is misleading.

    Slash-command cogs are NOT registered here; that happens in Plan 04-02.
    """

    def __init__(
        self,
        wordlist_path: Path,
        cache_path: Path | None = None,
    ) -> None:
        """Initialise the bot with resource paths.

        Args:
            wordlist_path:  Path to the plain-text word list (one word per line).
            cache_path:     Optional path for the GADDAG pickle cache. When provided,
                            GADDAG.from_wordlist() will read/write a cache to speed
                            up subsequent startups.
        """
        intents = discord.Intents.default()  # No privileged intents for slash-only bot
        super().__init__(command_prefix="!", intents=intents)

        self._wordlist_path = wordlist_path
        self._cache_path = cache_path

        # Populated in setup_hook — None until the bot has started
        self.gaddag: GADDAG | None = None
        self.difficulty_engine: DifficultyEngine | None = None

        # Per-channel settings store (in-memory, reset on restart)
        self.channel_store = ChannelStore()

    async def setup_hook(self) -> None:
        """Load heavy resources and sync commands before the READY event.

        Runs once after login, before the bot begins processing events.
        Exceptions propagate and prevent the bot from connecting — fail loudly.
        """
        logger.info("Loading GADDAG from {}", self._wordlist_path)
        # GADDAG.from_wordlist is CPU-bound — run in a thread to avoid blocking
        # the asyncio event loop (important if other async tasks are waiting).
        self.gaddag = await asyncio.to_thread(
            GADDAG.from_wordlist,
            self._wordlist_path,
            self._cache_path,
        )
        logger.info("GADDAG loaded successfully")

        self.difficulty_engine = DifficultyEngine()
        logger.info("DifficultyEngine initialised")

        # Register the AdvisorCog after all resources are loaded so that command
        # handlers can safely access self.gaddag and self.difficulty_engine.
        from src.bot.cog import AdvisorCog  # local import avoids circular dependency
        await self.add_cog(AdvisorCog(self))
        logger.info("AdvisorCog registered")

        # For dev: sync to test guild instantly. Set DISCORD_TEST_GUILD_ID in .env
        # for fast iteration. Without it, global sync can take up to 1 hour.
        guild_id = os.environ.get("DISCORD_TEST_GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info("Commands synced to test guild {}", guild_id)
        else:
            await self.tree.sync()
            logger.info("Commands synced globally (may take up to 1 hour)")

    async def on_ready(self) -> None:
        """Emitted when the bot has connected to the Discord gateway."""
        assert self.user is not None
        logger.info("Logged in as {} ({})", self.user.name, self.user.id)


async def main() -> None:
    """Async entry point: load env, build bot, connect to Discord."""
    load_dotenv()

    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        logger.error(
            "DISCORD_TOKEN not set in environment. "
            "Add it to .env or set it as an environment variable."
        )
        return

    wordlist_path = Path(os.environ.get("WORDLIST_PATH", "data/wordlist.txt"))
    cache_path = Path(os.environ.get("GADDAG_CACHE_PATH", "cache/gaddag.pkl"))

    bot = LetterLeagueBot(wordlist_path=wordlist_path, cache_path=cache_path)

    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
