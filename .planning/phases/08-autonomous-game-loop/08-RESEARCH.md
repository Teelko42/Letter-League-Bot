# Phase 8: Autonomous Game Loop - Research

**Researched:** 2026-03-31
**Domain:** discord.py slash command groups, asyncio task lifecycle, reconnection resilience, game loop orchestration
**Confidence:** HIGH

## Summary

Phase 8 is a pure orchestration layer. All the complex subsystems — browser session, navigation, canvas capture, turn detection, board vision, move generation, tile placement — are already built and tested in Phases 5-7. This phase wires them together into a self-sustaining loop controlled via Discord slash commands.

The two primary technical questions are: (1) how to expose `/autoplay start|stop|status` as a discord.py slash command group, and (2) how to run the game loop as an asyncio task that coexists with discord.py's event loop without blocking. Both have direct, well-established answers in the discord.py ecosystem. The reconnection strategy and state machine design are the only areas requiring careful design.

The game loop itself follows a linear sequence already described in CONTEXT.md — `poll_turn() → capture_canvas() → extract_board_state() → find_all_moves() → select_move() → place_move() → post embed → repeat`. All called functions already exist in `src/browser/` and `src/engine/`. Phase 8 only needs: a new cog, a state dataclass, the loop coroutine, and embed builders for turn summaries.

**Primary recommendation:** Implement `AutoPlayCog` as a new cog with an `app_commands.Group` class attribute for the three subcommands. Run the game loop via `asyncio.create_task()` stored on the cog instance. Use `asyncio.Event` for graceful stop signalling. Register the cog in `setup_hook()` alongside `AdvisorCog`.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Slash command design**
- Single `/autoplay` command with subcommands: `start`, `stop`, `status`
- `/autoplay start` takes no arguments — channel URL from config (.env), difficulty/mode from existing `/setdifficulty` and `/setmode` commands
- No permission restrictions — anyone in the server can start/stop/check status
- Single session only — `/autoplay start` fails with a message if already running (one browser context, one Discord account)

**Status reporting**
- Rich embed format for per-turn Discord messages (consistent with existing `/analyze` embeds)
- Post in the same text channel where `/autoplay start` was invoked
- Each turn update shows: word played, score, and turn number (e.g., "Played QUEST across row 5 for 42 pts — turn 7")
- Tile swap turns also get a message: "Swapped tiles (no valid moves) — turn 8"

**Reconnection and resilience**
- Activity disconnect: 3 retries with increasing backoff (5s, 15s, 30s), then give up
- On reconnection failure: stop the loop and post a Discord message in the autoplay channel explaining what happened
- Vision pipeline errors (Claude API failures): retry once, then skip the turn cycle and wait for the next poll
- Full browser crash: relaunch BrowserSession, re-navigate to Activity, resume the loop (uses persistent session data)

**Game lifecycle**
- `/autoplay start` is fully automatic: launches browser, navigates to channel, opens Activity, starts polling — one command does everything
- Supports joining mid-game — reads current board state and starts playing from wherever the game is
- Game-over detection (from Phase 6's `classify_frame()`): post a final summary embed (game-over notice, total turns played), then cleanly stop the loop and close the browser
- `/autoplay stop`: finishes the current turn if mid-placement (avoid leaving tiles half-placed), then stops gracefully

### Claude's Discretion
- Internal state management approach (dataclass, enum, etc.)
- How /autoplay status displays current state (running/stopped, turn count, uptime)
- Exact embed styling (colors, fields, footer)
- Cog structure (new AutoPlayCog vs extending AdvisorCog)
- Cancellation token pattern for graceful shutdown
- Logging verbosity and format

### Deferred Ideas (OUT OF SCOPE)
- Post final game score to Discord when game ends — partially covered (summary embed on game-over), but extracting actual score from the game-over screen would be a v2 enhancement
- Detect opponent disconnection as a distinct state — handle via existing error recovery
- Multi-game support / auto-queue for next game — would need separate phase
- Adaptive ML-based turn detection — deferred to AUTX-02
- Tile swap strategy integration with difficulty engine — deferred to AUTX-03
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| LOOP-01 | Async game loop runs concurrent with discord.py event loop without blocking | `asyncio.create_task()` on discord.py's own event loop; `asyncio.to_thread()` for CPU-bound `find_all_moves()`; no `asyncio.run()` inside the cog |
| LOOP-02 | User can run `/autoplay start`, `/autoplay stop`, and `/autoplay status` slash commands | `app_commands.Group` class attribute in cog; `@group.command()` decorator for each subcommand |
| LOOP-03 | Bot uses human-like timing jitter (random delays between actions) | Already handled inside `TilePlacer.place_tiles()` (1-3s inter-tile); outer loop needs no additional delay — Phase 7 satisfies intra-turn pacing |
| LOOP-04 | Bot falls back to tile swap when no valid moves exist | `TilePlacer.place_move()` already returns `False` + performs swap when `moves` list is empty or all attempts fail; outer loop detects empty `moves` list and calls `place_move([], rack)` |
| LOOP-05 | Bot posts Discord status updates showing what word was played and the score | `channel.send(embed=...)` after each `place_move()` call; requires storing `channel` object from the interaction at `/autoplay start` time |
| BROW-03 | Bot reconnects gracefully when the browser session or Activity disconnects mid-game | Catch `Exception` around `capture_canvas()` / `navigate_to_activity()` in the loop; retry with backoff (5s, 15s, 30s); relaunch `BrowserSession` on crash |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| discord.py | 2.x (already installed) | Slash commands, embed posting, interaction responses | Project's existing bot framework |
| discord.app_commands | bundled with discord.py 2.x | `Group` and `@group.command()` for subcommand routing | Official discord.py 2.0+ pattern for `/cmd sub` syntax |
| asyncio | stdlib | `create_task()`, `Event`, `CancelledError` | Python standard library; same event loop discord.py uses |
| loguru | already installed | Structured logging | Project standard (used in all existing modules) |
| dataclasses | stdlib | `LoopState` dataclass for session state | Consistent with `ChannelState` pattern in `channel_state.py` |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| datetime / time.monotonic | stdlib | Track uptime and turn timestamps for `/autoplay status` | Already used in `cog.py` for timing |
| random | stdlib | Human-like jitter in inter-turn delays (if any added at loop level) | LOOP-03 satisfaction at outer loop level if desired |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `asyncio.create_task()` manual task | `discord.ext.tasks.loop` | `ext.tasks` works for fixed-interval polling but doesn't model "run until game_over or stop signal" well; manual task gives full control over loop exit conditions |
| `asyncio.Event` for stop signal | `asyncio.Task.cancel()` direct | Direct cancel raises `CancelledError` immediately even mid-placement; `Event` lets the loop check at safe checkpoints (between turns) for graceful stop |
| New `AutoPlayCog` | Extend `AdvisorCog` | Extending `AdvisorCog` mixes unrelated concerns; separate cog is cleaner and matches project's existing single-responsibility cog structure |

**Installation:** No new packages needed. All required libraries are already installed.

## Architecture Patterns

### Recommended Project Structure
```
src/
├── bot/
│   ├── bot.py               # Add AutoPlayCog registration in setup_hook()
│   ├── cog.py               # AdvisorCog — unchanged
│   ├── autoplay_cog.py      # NEW: AutoPlayCog with /autoplay group
│   ├── formatter.py         # Add build_turn_embed(), build_swap_embed(), build_gameover_embed()
│   └── channel_state.py     # Unchanged
```

### Pattern 1: app_commands.Group as Cog Class Attribute

**What:** Declare a `Group` as a class-level attribute; decorate subcommands with `@group.command()`. discord.py auto-discovers it when the cog is added.

**When to use:** Any time you need `/cmd sub1`, `/cmd sub2`, `/cmd sub3` as a single slash command family.

**Example:**
```python
# Source: discord.py documentation + fallendeity.github.io/discord.py-masterclass
import discord
from discord import app_commands
from discord.ext import commands

class AutoPlayCog(commands.Cog):
    autoplay_group = app_commands.Group(
        name="autoplay",
        description="Autonomous game loop controls",
    )

    def __init__(self, bot: "LetterLeagueBot") -> None:
        self.bot = bot
        self._loop_task: asyncio.Task | None = None
        self._stop_event: asyncio.Event = asyncio.Event()
        self._state: LoopState | None = None

    @autoplay_group.command(name="start", description="Start the autonomous game loop")
    async def autoplay_start(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=False)
        # ... implementation

    @autoplay_group.command(name="stop", description="Stop the autonomous game loop")
    async def autoplay_stop(self, interaction: discord.Interaction) -> None:
        # ...

    @autoplay_group.command(name="status", description="Show current autoplay status")
    async def autoplay_status(self, interaction: discord.Interaction) -> None:
        # ...
```

### Pattern 2: asyncio.create_task for the Game Loop

**What:** Create a background coroutine as an asyncio Task. The task lives on discord.py's event loop. Store a reference on the cog to enable cancellation.

**When to use:** Long-running background work that must run concurrently with Discord event processing.

**Example:**
```python
# Source: Python asyncio docs + project established pattern (cog.py asyncio.to_thread usage)
async def autoplay_start(self, interaction: discord.Interaction) -> None:
    if self._loop_task and not self._loop_task.done():
        await interaction.followup.send(
            embed=build_error_embed_generic("Autoplay is already running."),
        )
        return

    self._stop_event.clear()
    channel = interaction.channel
    self._loop_task = asyncio.create_task(
        self._run_game_loop(channel),
        name="autoplay-game-loop",
    )
    await interaction.followup.send(embed=build_info_embed("Autoplay Started", "..."))
```

### Pattern 3: asyncio.Event for Graceful Stop

**What:** Use `asyncio.Event` as a cooperative stop signal. The loop checks `_stop_event.is_set()` at safe checkpoints (between turns, not mid-placement). `/autoplay stop` calls `_stop_event.set()`.

**When to use:** When you need graceful shutdown that finishes the current unit of work first ("finishes the current turn if mid-placement").

**Example:**
```python
# Source: Python asyncio docs, graceful shutdown patterns
async def _run_game_loop(self, channel: discord.TextChannel) -> None:
    turn_count = 0
    try:
        # startup: launch browser, navigate
        ...
        while not self._stop_event.is_set():
            turn_state = await poll_turn(page)
            if turn_state == "game_over":
                await channel.send(embed=build_gameover_embed(turn_count))
                break
            # ... execute turn ...
            turn_count += 1
            # Check stop after completing the full turn (not mid-placement)
            if self._stop_event.is_set():
                break
    except asyncio.CancelledError:
        # Hard cancel from cog_unload — log and re-raise
        logger.info("Game loop task cancelled")
        raise
    finally:
        await self._cleanup_browser()
```

### Pattern 4: Reconnection with Increasing Backoff

**What:** Wrap the inner loop body in a try/except. On Activity disconnect errors, retry `navigate_to_activity()` with delays of 5s, 15s, 30s (decision from CONTEXT.md). On full browser crash, relaunch `BrowserSession`.

**When to use:** BROW-03 requirement — the loop must survive transient disconnects.

**Example:**
```python
# Source: project pattern from navigate_to_activity() (navigator.py already does retry with backoff)
RECONNECT_DELAYS = [5, 15, 30]  # seconds

async def _attempt_reconnect(self, page) -> Any:
    """Attempt to re-navigate to the Activity. Returns new frame or raises."""
    for delay in RECONNECT_DELAYS:
        try:
            frame = await navigate_to_activity(page, self._channel_url)
            logger.info("Reconnected to Activity successfully")
            return frame
        except Exception as exc:
            logger.warning("Reconnect attempt failed: {} — waiting {}s", exc, delay)
            await asyncio.sleep(delay)
    raise RuntimeError("Activity reconnection failed after all retries")
```

### Pattern 5: LoopState Dataclass

**What:** A simple `@dataclass` to hold session state — start time, turn count, channel reference, and current phase (idle/running/stopping). Consistent with existing `ChannelState` pattern.

**Recommended design:**
```python
from dataclasses import dataclass, field
from enum import Enum
import time

class AutoPlayPhase(Enum):
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"

@dataclass
class LoopState:
    phase: AutoPlayPhase = AutoPlayPhase.IDLE
    turn_count: int = 0
    start_time: float = field(default_factory=time.monotonic)
    channel_id: int = 0
    channel_url: str = ""
```

### Anti-Patterns to Avoid

- **`asyncio.run()` inside the cog:** Creates a new event loop, crashes immediately with "This event loop is already running" because discord.py already owns it. Use `asyncio.create_task()` instead.
- **Blocking calls inside the loop:** `find_all_moves()` is CPU-bound — must use `asyncio.to_thread()` exactly as `cog.py` already does. Never call it directly in the async loop.
- **Task reference leak:** If `_loop_task` is not stored and checked, a second `/autoplay start` creates a second parallel loop. Always check `_loop_task.done()` before creating a new task.
- **Hard-cancelling mid-placement:** Calling `_loop_task.cancel()` directly during tile placement will interrupt drag operations, leaving tiles in a broken state. The `asyncio.Event` pattern lets the loop finish the current turn first.
- **Not re-raising CancelledError:** `except asyncio.CancelledError: pass` suppresses cancellation and prevents the task from terminating. Always re-raise it after cleanup.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Subcommand routing | Manual string parsing in one command | `app_commands.Group` + `@group.command()` | Discord enforces slash command structure; manual parsing is unreliable |
| Browser reconnection | Custom retry infrastructure | Wrap existing `navigate_to_activity()` which already has max_retries + backoff | navigator.py already implements retry-with-backoff; just add outer backoff delays |
| Turn completion detection | Custom post-placement wait logic | Reuse `classify_frame()` from turn_detector.py | Phase 7's `_wait_for_acceptance()` already does this; `place_move()` returns `True/False` |
| Tile swap detection | Inspect move list before calling placer | `TilePlacer.place_move([], rack)` with empty moves list triggers swap directly | `place_move()` already handles the empty-moves case (falls through to `_tile_swap()`) |
| Discord message channel resolution | Store raw channel_id and fetch on every post | Store `discord.TextChannel` object from interaction at start time | `interaction.channel` gives the live channel object; no need to fetch repeatedly |

**Key insight:** Nearly all the hard work is already done. Phase 8's loop body is approximately 15-20 lines of async orchestration code calling into already-tested modules.

## Common Pitfalls

### Pitfall 1: Double Session Start
**What goes wrong:** Two users (or one user pressing start twice) call `/autoplay start` before the task is fully initialised. Two game loop tasks run concurrently, both controlling the same browser.
**Why it happens:** There is a window between `create_task()` and the task's first `await` where `_loop_task.done()` would be False but the second start also passes the guard.
**How to avoid:** Set `_state.phase = AutoPlayPhase.STARTING` synchronously before creating the task. Guard on `phase != IDLE` not just `task.done()`.
**Warning signs:** Discord getting two simultaneous status messages; tile placement fighting with itself.

### Pitfall 2: asyncio.CancelledError Swallowed
**What goes wrong:** A broad `except Exception` in the loop body catches `CancelledError` (which inherits from `BaseException` in Python 3.8+, NOT from `Exception`, so this is actually safe — but easy to get wrong in Python 3.7-era code).
**Why it happens:** Copy-pasting old error-handling code from Python 3.7 where `CancelledError` was a subclass of `Exception`.
**How to avoid:** In Python 3.8+, `except Exception` will NOT catch `CancelledError`. Explicit `except asyncio.CancelledError: raise` at the outermost level is still good practice for clarity.
**Warning signs:** `/autoplay stop` appears to respond but the loop keeps running.

### Pitfall 3: Missing cog_unload Cleanup
**What goes wrong:** Bot shuts down or cog is reloaded; the game loop task keeps running orphaned. Browser session stays open.
**Why it happens:** Forgetting to cancel the task in `cog_unload()`.
**How to avoid:** Always implement `cog_unload()` with `if self._loop_task: self._loop_task.cancel()`.

### Pitfall 4: Interaction Token Expiry on Deferred Response
**What goes wrong:** `/autoplay start` defers, but the bot takes more than 15 minutes before calling `followup.send()`. Discord rejects the followup.
**Why it happens:** `interaction.followup` tokens expire after 15 minutes. The startup sequence (browser launch + navigation) can take 30-60 seconds — well within the window — but if something stalls, the followup will fail.
**How to avoid:** Send the initial followup ("Starting autoplay...") immediately after startup completes (before entering the polling loop). Subsequent turn updates use `channel.send()`, not the interaction followup.
**Warning signs:** `discord.errors.NotFound: 404 Unknown Webhook` in logs.

### Pitfall 5: Vision Retry Causing Turn Skip
**What goes wrong:** Vision pipeline (Claude API) fails. The retry logic retries once, then the code path is unclear — does it attempt tile placement with stale data? Does it skip the turn entirely?
**Why it happens:** Not explicitly handling the "retry failed, skip cycle" path.
**How to avoid:** After vision retry failure, `continue` to the top of the while loop (which re-enters `poll_turn()`). Do NOT call `place_move()` with stale/None board state.
**Warning signs:** `AttributeError` or `None`-related exceptions during move generation.

### Pitfall 6: find_all_moves Blocking the Event Loop
**What goes wrong:** `find_all_moves()` is CPU-bound and takes 100ms-2s. Calling it directly in the async loop blocks all other coroutines including Discord heartbeats, potentially causing gateway disconnection.
**Why it happens:** Forgetting that async functions can still block if they call synchronous CPU-intensive code.
**How to avoid:** Use `asyncio.to_thread(find_all_moves, board, rack, self.bot.gaddag, state.mode)` — exactly as `AdvisorCog.analyze()` already does.
**Warning signs:** Discord bot showing "offline" or command responses becoming sluggish during move generation.

## Code Examples

### Game Loop Skeleton
```python
# Source: project pattern from cog.py + turn_detector.py + tile_placer.py
async def _run_game_loop(
    self,
    channel: discord.TextChannel,
    channel_url: str,
) -> None:
    """Main game loop. Runs until game_over detected or stop signal set."""
    turn_count = 0
    session = BrowserSession()
    page = None

    try:
        # --- Startup ---
        page = await session.start()
        _frame = await navigate_to_activity(page, channel_url)
        await preflight_check(page)

        placer = TilePlacer(page)
        ch_state = self.bot.channel_store.get(channel.id)

        while not self._stop_event.is_set():
            # Step 1: Wait for our turn (or game over)
            turn_state = await poll_turn(page)
            if turn_state == "game_over":
                await channel.send(embed=build_gameover_embed(turn_count))
                break

            # Step 2: Capture and parse board
            try:
                img_bytes = await capture_canvas(page)
                board, rack = await extract_board_state(img_bytes, mode=ch_state.mode)
            except Exception as exc:
                logger.warning("Vision pipeline error (attempt 1): {}", exc)
                try:
                    img_bytes = await capture_canvas(page)
                    board, rack = await extract_board_state(img_bytes, mode=ch_state.mode)
                except Exception as exc2:
                    logger.error("Vision pipeline retry failed, skipping cycle: {}", exc2)
                    continue  # re-enter poll_turn

            # Step 3: Generate and select move
            moves = await asyncio.to_thread(
                find_all_moves, board, rack, self.bot.gaddag, ch_state.mode
            )
            if moves:
                selected = await asyncio.to_thread(
                    self.bot.difficulty_engine.select_move, moves, ch_state.difficulty
                )
                candidates = [selected] + [m for m in moves if m is not selected]
            else:
                candidates = []

            # Step 4: Place move (or swap)
            turn_count += 1
            word_played = await placer.place_move(candidates, rack)

            # Step 5: Post status update
            if word_played and candidates:
                played_move = candidates[0]  # place_move returns True when first accepted
                await channel.send(
                    embed=build_turn_embed(played_move, turn_count)
                )
            else:
                await channel.send(embed=build_swap_embed(turn_count))

    except asyncio.CancelledError:
        logger.info("Game loop cancelled by /autoplay stop or cog unload")
        raise
    except Exception as exc:
        logger.exception("Game loop terminated with unexpected error: {}", exc)
        await channel.send(
            embed=build_error_embed_generic(f"Autoplay stopped due to error: {exc}")
        )
    finally:
        self._state = None
        self._stop_event.clear()
        if page:
            await session.close()
        logger.info("Game loop cleanup complete")
```

### /autoplay start Guard Pattern
```python
# Source: project pattern (cog.py single-session guard)
@autoplay_group.command(name="start")
async def autoplay_start(self, interaction: discord.Interaction) -> None:
    await interaction.response.defer(ephemeral=False)

    # Guard: single session only
    if self._state is not None and self._state.phase != AutoPlayPhase.IDLE:
        await interaction.followup.send(
            embed=build_error_embed_generic(
                "Autoplay is already running. Use `/autoplay stop` first."
            )
        )
        return

    channel_url = os.environ.get("VOICE_CHANNEL_URL", "")
    if not channel_url:
        await interaction.followup.send(
            embed=build_error_embed_generic("VOICE_CHANNEL_URL not set in .env")
        )
        return

    self._state = LoopState(
        phase=AutoPlayPhase.STARTING,
        channel_id=interaction.channel_id,
        channel_url=channel_url,
    )
    self._stop_event.clear()
    self._loop_task = asyncio.create_task(
        self._run_game_loop(interaction.channel, channel_url),
        name="autoplay-game-loop",
    )
    await interaction.followup.send(
        embed=build_info_embed("Autoplay Started", "Launching browser and connecting...")
    )
```

### /autoplay stop Pattern
```python
# Source: asyncio graceful shutdown pattern
@autoplay_group.command(name="stop")
async def autoplay_stop(self, interaction: discord.Interaction) -> None:
    if self._state is None or self._state.phase == AutoPlayPhase.IDLE:
        await interaction.response.send_message(
            embed=build_info_embed("Not Running", "Autoplay is not currently active."),
            ephemeral=True,
        )
        return

    self._stop_event.set()  # Signal the loop to stop after current turn
    self._state.phase = AutoPlayPhase.STOPPING
    await interaction.response.send_message(
        embed=build_info_embed(
            "Stopping",
            "Finishing current turn, then stopping..."
        ),
        ephemeral=True,
    )
```

### cog_unload Cleanup
```python
# Source: discord.py cog lifecycle docs
def cog_unload(self) -> None:
    """Cancel the game loop task when the cog is unloaded."""
    if self._loop_task and not self._loop_task.done():
        self._loop_task.cancel()
```

### Reconnection Wrapper
```python
# Source: navigate_to_activity() retry pattern in navigator.py
RECONNECT_DELAYS = [5, 15, 30]

async def _reconnect_activity(self, page) -> Any:
    """Re-navigate to Activity with increasing backoff. Raises on total failure."""
    for i, delay in enumerate(RECONNECT_DELAYS, start=1):
        try:
            frame = await navigate_to_activity(page, self._state.channel_url)
            logger.info("Reconnected to Activity (attempt {})", i)
            return frame
        except Exception as exc:
            logger.warning(
                "Reconnect attempt {}/{} failed: {} — waiting {}s",
                i, len(RECONNECT_DELAYS), exc, delay
            )
            if i < len(RECONNECT_DELAYS):
                await asyncio.sleep(delay)
    raise RuntimeError("Activity reconnect failed after all retries")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `discord.ext.tasks.loop` for background work | `asyncio.create_task()` for event-driven loops | discord.py 2.0 | `ext.tasks` is interval-based; game loop is event-driven (poll_turn blocks until state changes) — raw task is the right tool |
| `@commands.group()` prefix commands | `app_commands.Group` slash command groups | discord.py 2.0 | Slash commands are now the standard; prefix commands are legacy |
| Sync Playwright API | patchright async API | Project decision Phase 5 | Never use sync patchright in async context — it blocks the event loop |

**Deprecated/outdated:**
- `discord.ext.tasks` for this use case: Works for fixed-interval polling, but `poll_turn()` already implements its own adaptive polling loop. Wrapping it in a fixed-interval task would create double-polling complexity.
- `asyncio.run()` inside an already-running loop: Universally forbidden in this project since discord.py owns the event loop.

## Open Questions

1. **`place_move()` return value vs played move identification**
   - What we know: `place_move()` returns `True` if a word was accepted, `False` for tile swap. It does not return which specific move was accepted.
   - What's unclear: When `place_move()` returns True, we need to know the word and score for the status embed. We passed a `candidates` list — the first accepted move is the one played, but `place_move()` internally tries each in order and returns True on first success.
   - Recommendation: Pass a single-item list (just the selected move) to `place_move()` at the outer loop level, or change the signature to return `Move | None` instead of `bool`. The planner should pick one approach and document it. The simplest fix: pass `[selected_move]` alone so the caller always knows what was played.

2. **Browser crash detection vs Activity disconnect**
   - What we know: CONTEXT.md distinguishes "Activity disconnect" (3 retries with reconnect) from "full browser crash" (relaunch BrowserSession).
   - What's unclear: How do we programmatically distinguish a patchright exception caused by "iframe disappeared" vs "browser process died"? Different exception types or messages would be needed.
   - Recommendation: Treat any `Error: Execution context was destroyed` or `TargetClosedError` from patchright as a crash signal; treat `TimeoutError` from iframe selectors as an Activity disconnect. Log exception class names during testing to calibrate.

3. **`/autoplay start` response visibility**
   - What we know: CONTEXT.md says "post in the same text channel where `/autoplay start` was invoked". The per-turn embeds should be public (not ephemeral) so the server can watch the game.
   - What's unclear: Should the `/autoplay start` confirmation itself be ephemeral or public?
   - Recommendation: Make start/stop/status responses ephemeral (visible only to invoker); make per-turn game updates public via `channel.send()`. This is Claude's discretion per CONTEXT.md.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest (installed at `C:\Users\Ninja\AppData\Local\Programs\Python\Python313\`) |
| Config file | none detected — pytest runs with defaults |
| Quick run command | `py -3 -m pytest tests/test_autoplay_cog.py -x -q` |
| Full suite command | `py -3 -m pytest tests/ -q` |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| LOOP-01 | Game loop task created with `create_task`, does not block event loop | unit | `py -3 -m pytest tests/test_autoplay_cog.py::test_loop_runs_as_task -x` | Wave 0 |
| LOOP-02 | `/autoplay start` fails if already running; `/autoplay stop` sets stop event | unit | `py -3 -m pytest tests/test_autoplay_cog.py::test_start_guard -x` | Wave 0 |
| LOOP-02 | `/autoplay status` returns idle/running state | unit | `py -3 -m pytest tests/test_autoplay_cog.py::test_status_idle -x` | Wave 0 |
| LOOP-03 | Human-like delays already covered by TilePlacer (Phase 7) | unit (existing) | `py -3 -m pytest tests/test_tile_placer.py -x` | verify |
| LOOP-04 | Empty moves list causes tile swap (place_move returns False) | unit | `py -3 -m pytest tests/test_autoplay_cog.py::test_swap_on_no_moves -x` | Wave 0 |
| LOOP-05 | turn embed built with correct word, score, turn number | unit | `py -3 -m pytest tests/test_autoplay_formatter.py -x` | Wave 0 |
| BROW-03 | Reconnect attempted 3 times with 5/15/30s delays on Activity error | unit | `py -3 -m pytest tests/test_autoplay_cog.py::test_reconnect_backoff -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `py -3 -m pytest tests/test_autoplay_cog.py -x -q`
- **Per wave merge:** `py -3 -m pytest tests/ -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_autoplay_cog.py` — covers LOOP-01, LOOP-02, LOOP-04, BROW-03 with mocked browser/engine
- [ ] `tests/test_autoplay_formatter.py` — covers LOOP-05 embed builders (pure function tests, no mocking needed)
- [ ] Framework install: `py -3 -m pip install pytest pytest-asyncio` — pytest-asyncio needed for `async def test_*` coroutines

## Sources

### Primary (HIGH confidence)
- discord.py official docs (discordpy.readthedocs.io) — `app_commands.Group`, slash command sync, cog patterns
- discord.py masterclass (fallendeity.github.io) — verified `app_commands.Group` class attribute pattern in Cog
- Python stdlib asyncio docs — `create_task`, `Event`, `CancelledError` behaviour
- Project source code (`src/browser/`, `src/bot/`) — direct inspection of established patterns, function signatures

### Secondary (MEDIUM confidence)
- Discord developer docs (discord.com/developers) — slash command group nesting limits (25 per group, 2 levels deep)
- asyncio graceful shutdown examples (roguelynn.com, github.com/wbenny) — `CancelledError` handling patterns

### Tertiary (LOW confidence)
- None — all critical claims are directly verified by official sources or project source inspection.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all libraries already installed and used in the project
- Architecture: HIGH — `app_commands.Group`, `create_task`, and `Event` are directly verified against official discord.py docs and existing project patterns
- Pitfalls: HIGH for LOOP-01/02/03/05 (direct code review), MEDIUM for BROW-03 (browser crash classification depends on patchright exception types not fully documented)

**Research date:** 2026-03-31
**Valid until:** 2026-07-01 (discord.py 2.x API is stable; patchright exception types could shift sooner)
