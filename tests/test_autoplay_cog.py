"""Unit tests for AutoPlayCog — guard logic, loop task, reconnection, and swap fallback.

All browser, vision, and engine subsystems are mocked so these tests run without
a real browser or network connection.

Tests:
  - test_start_guard: double-start returns error, no second task
  - test_start_creates_task: idle start creates task and sets STARTING state
  - test_stop_sets_event: stop sets the stop event and transitions to STOPPING
  - test_stop_when_idle: stop when idle returns "not active" message
  - test_status_idle: status when idle reports "not running"
  - test_status_running: status when running shows turn count and phase
  - test_swap_on_no_moves: empty move list calls place_move([], rack) and posts swap embed
  - test_reconnect_backoff: _attempt_reconnect retries 3 times then raises
  - test_game_over_stops_loop: game_over from poll_turn posts gameover embed and exits loop
  - test_vision_retry_then_skip: two extract_board_state failures skip cycle
  - test_cog_unload_cancels_task: cog_unload cancels the running task
"""

from __future__ import annotations

import asyncio
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from src.bot.autoplay_cog import AutoPlayCog
from src.bot.autoplay_state import AutoPlayPhase, LoopState
from src.bot.formatter import WARNING_COLOR, INFO_COLOR, SUCCESS_COLOR


# ---------------------------------------------------------------------------
# Helpers and fixtures
# ---------------------------------------------------------------------------

def _make_mock_bot() -> MagicMock:
    """Return a mock LetterLeagueBot with required attributes."""
    bot = MagicMock()
    bot.gaddag = MagicMock()
    bot.difficulty_engine = MagicMock()

    # channel_store.get returns a ChannelState-like mock
    ch_state = MagicMock()
    ch_state.mode = "wild"
    ch_state.difficulty = 100
    bot.channel_store = MagicMock()
    bot.channel_store.get.return_value = ch_state

    return bot


def _make_mock_interaction(channel_id: int = 42) -> MagicMock:
    """Return a mock discord.Interaction."""
    interaction = MagicMock()
    interaction.response = AsyncMock()
    interaction.response.defer = AsyncMock()
    interaction.response.send_message = AsyncMock()
    interaction.followup = AsyncMock()
    interaction.followup.send = AsyncMock()
    interaction.channel_id = channel_id
    interaction.channel = AsyncMock()
    interaction.channel.send = AsyncMock()
    return interaction


def _make_move_mock() -> MagicMock:
    """Return a mock Move object."""
    move = MagicMock()
    move.word = "TEST"
    move.score = 10
    move.direction = "H"
    move.start_row = 5
    move.start_col = 3
    return move


# ---------------------------------------------------------------------------
# Test 1: Double-start guard
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_start_guard() -> None:
    """Starting when already running returns error embed, no second task created."""
    cog = AutoPlayCog(_make_mock_bot())
    # Simulate already-running state
    cog._state = LoopState(phase=AutoPlayPhase.RUNNING)

    interaction = _make_mock_interaction()

    with patch.dict(os.environ, {"VOICE_CHANNEL_URL": "https://discord.com/channels/1/2"}):
        await cog.autoplay_start.callback(cog, interaction)

    interaction.followup.send.assert_awaited_once()
    call_kwargs = interaction.followup.send.call_args
    embed = call_kwargs.kwargs.get("embed") or (call_kwargs.args[0] if call_kwargs.args else None)
    assert embed is not None
    assert "already running" in (embed.description or "").lower()
    # No loop task should have been created
    assert cog._loop_task is None


# ---------------------------------------------------------------------------
# Test 2: Start creates task
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_start_creates_task() -> None:
    """Starting when idle creates an asyncio task and sets state to STARTING."""
    cog = AutoPlayCog(_make_mock_bot())
    assert cog._state is None

    interaction = _make_mock_interaction()

    with patch.dict(os.environ, {"VOICE_CHANNEL_URL": "https://discord.com/channels/1/2"}):
        # Patch _run_game_loop so the task doesn't do real work
        with patch.object(cog, "_run_game_loop", new_callable=AsyncMock) as mock_loop:
            # Make the mock coroutine block until cancelled
            loop_event = asyncio.Event()

            async def _blocking_loop(*args, **kwargs):
                await loop_event.wait()

            mock_loop.side_effect = _blocking_loop

            await cog.autoplay_start.callback(cog, interaction)

            assert cog._loop_task is not None
            assert cog._state is not None
            assert cog._state.phase == AutoPlayPhase.STARTING

            # Clean up
            cog._loop_task.cancel()
            loop_event.set()
            try:
                await asyncio.wait_for(cog._loop_task, timeout=1.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass


# ---------------------------------------------------------------------------
# Test 3: Stop sets event and transitions to STOPPING
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_stop_sets_event() -> None:
    """Stopping a running session sets the stop event and changes phase to STOPPING."""
    cog = AutoPlayCog(_make_mock_bot())
    cog._state = LoopState(phase=AutoPlayPhase.RUNNING)
    # Provide a mock "done" task so the stop path doesn't fail
    mock_task = MagicMock()
    mock_task.done.return_value = False
    cog._loop_task = mock_task

    interaction = _make_mock_interaction()
    await cog.autoplay_stop.callback(cog, interaction)

    assert cog._stop_event.is_set()
    assert cog._state.phase == AutoPlayPhase.STOPPING
    interaction.response.send_message.assert_awaited_once()


# ---------------------------------------------------------------------------
# Test 4: Stop when idle returns "not active"
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_stop_when_idle() -> None:
    """Stopping when no session is active sends an ephemeral error."""
    cog = AutoPlayCog(_make_mock_bot())
    assert cog._state is None

    interaction = _make_mock_interaction()
    await cog.autoplay_stop.callback(cog, interaction)

    interaction.response.send_message.assert_awaited_once()
    call_args = interaction.response.send_message.call_args
    embed = call_args.kwargs.get("embed")
    assert embed is not None
    assert "not" in (embed.description or "").lower()


# ---------------------------------------------------------------------------
# Test 5: Status when idle
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_status_idle() -> None:
    """Status when not running reports 'not running' or similar."""
    cog = AutoPlayCog(_make_mock_bot())
    assert cog._state is None

    interaction = _make_mock_interaction()
    await cog.autoplay_status.callback(cog, interaction)

    interaction.response.send_message.assert_awaited_once()
    call_args = interaction.response.send_message.call_args
    embed = call_args.kwargs.get("embed")
    assert embed is not None
    assert "not" in (embed.description or embed.title or "").lower()


# ---------------------------------------------------------------------------
# Test 6: Status when running shows turn count and phase
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_status_running() -> None:
    """Status embed includes turn count and running phase."""
    cog = AutoPlayCog(_make_mock_bot())
    cog._state = LoopState(phase=AutoPlayPhase.RUNNING, turn_count=5)

    interaction = _make_mock_interaction()
    await cog.autoplay_status.callback(cog, interaction)

    interaction.response.send_message.assert_awaited_once()
    call_args = interaction.response.send_message.call_args
    embed = call_args.kwargs.get("embed")
    assert embed is not None

    # Check fields contain phase and turn count
    field_values = [f.value for f in embed.fields]
    field_names = [f.name for f in embed.fields]
    all_text = " ".join(field_values + field_names)

    assert "5" in all_text  # turn count
    assert "running" in all_text.lower()  # phase value


# ---------------------------------------------------------------------------
# Test 7: Swap on no moves
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_swap_on_no_moves() -> None:
    """When find_all_moves returns [], place_move([], rack) is called and swap embed posted."""
    cog = AutoPlayCog(_make_mock_bot())
    channel = AsyncMock()
    channel.send = AsyncMock()

    mock_rack = ["A", "B", "C"]

    with patch("src.bot.autoplay_cog.BrowserSession") as MockSession, \
         patch("src.bot.autoplay_cog.navigate_to_activity", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.preflight_check", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.wait_for_game_ready", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.click_start_game", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.poll_turn", new_callable=AsyncMock) as mock_poll, \
         patch("src.bot.autoplay_cog.capture_canvas", new_callable=AsyncMock) as mock_capture, \
         patch("src.bot.autoplay_cog.extract_board_state", new_callable=AsyncMock) as mock_vision, \
         patch("src.bot.autoplay_cog.find_all_moves", return_value=[]) as mock_find, \
         patch.dict(os.environ, {"VOICE_CHANNEL_URL": "https://discord.com/channels/1/2"}):

        # Set up session mock
        mock_page = MagicMock()
        mock_session = AsyncMock()
        mock_session.start = AsyncMock(return_value=mock_page)
        mock_session.close = AsyncMock()
        MockSession.return_value = mock_session

        # Set state so the loop assertion passes (normally set by autoplay_start)
        cog._state = LoopState(phase=AutoPlayPhase.STARTING, channel_id=42)

        # First poll returns my_turn; second returns game_over (exits loop)
        mock_poll.side_effect = ["my_turn", "game_over"]
        mock_capture.return_value = b"fake_png"

        mock_board = MagicMock()
        mock_vision.return_value = (mock_board, mock_rack)

        # Mock TilePlacer
        mock_placer = AsyncMock()
        mock_placer.place_move = AsyncMock(return_value=False)  # False = swapped

        with patch("src.bot.autoplay_cog.TilePlacer", return_value=mock_placer):
            await cog._run_game_loop(channel, "https://discord.com/channels/1/2")

    # Verify place_move was called with empty candidates list
    mock_placer.place_move.assert_awaited()
    call_args = mock_placer.place_move.call_args
    candidates_arg = call_args.args[0] if call_args.args else call_args.kwargs.get("moves", call_args.args[0])
    assert candidates_arg == []

    # Verify swap embed was posted (gold/WARNING color)
    channel.send.assert_awaited()
    # Check at least one embed posted is a swap embed (gold color)
    sent_embeds = [call.kwargs.get("embed") for call in channel.send.call_args_list if call.kwargs.get("embed")]
    swap_embeds = [e for e in sent_embeds if e is not None and e.color == WARNING_COLOR]
    assert len(swap_embeds) >= 1, f"Expected swap embed (WARNING_COLOR), got: {[e.color for e in sent_embeds if e]}"


# ---------------------------------------------------------------------------
# Test 8: Reconnect backoff — 3 attempts then raises
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_reconnect_backoff() -> None:
    """_attempt_reconnect retries 3 times with navigate_to_activity, raises on all failures."""
    cog = AutoPlayCog(_make_mock_bot())

    mock_page = MagicMock()

    with patch("src.bot.autoplay_cog.navigate_to_activity", new_callable=AsyncMock) as mock_nav, \
         patch("asyncio.sleep", new_callable=AsyncMock):  # speed up backoff
        mock_nav.side_effect = RuntimeError("connection refused")

        with pytest.raises(RuntimeError, match="Failed to reconnect"):
            await cog._attempt_reconnect(mock_page, "https://discord.com/channels/1/2")

    assert mock_nav.call_count == 3


# ---------------------------------------------------------------------------
# Test 9: Game over stops loop and posts gameover embed
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_game_over_stops_loop() -> None:
    """When poll_turn returns 'game_over' immediately, loop posts gameover embed and exits."""
    cog = AutoPlayCog(_make_mock_bot())
    channel = AsyncMock()
    channel.send = AsyncMock()

    with patch("src.bot.autoplay_cog.BrowserSession") as MockSession, \
         patch("src.bot.autoplay_cog.navigate_to_activity", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.preflight_check", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.wait_for_game_ready", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.click_start_game", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.poll_turn", new_callable=AsyncMock) as mock_poll, \
         patch.dict(os.environ, {"VOICE_CHANNEL_URL": "https://discord.com/channels/1/2"}):

        mock_page = MagicMock()
        mock_session = AsyncMock()
        mock_session.start = AsyncMock(return_value=mock_page)
        mock_session.close = AsyncMock()
        MockSession.return_value = mock_session

        # Set state so the loop assertion passes
        cog._state = LoopState(phase=AutoPlayPhase.STARTING, channel_id=42)

        # Immediately game over
        mock_poll.return_value = "game_over"

        mock_placer = AsyncMock()
        with patch("src.bot.autoplay_cog.TilePlacer", return_value=mock_placer):
            await cog._run_game_loop(channel, "https://discord.com/channels/1/2")

    # Verify gameover embed posted
    channel.send.assert_awaited_once()
    call_args = channel.send.call_args
    embed = call_args.kwargs.get("embed")
    assert embed is not None
    assert embed.title == "Game Over"

    # place_move should never have been called
    mock_placer.place_move.assert_not_awaited()

    # State should be reset after loop exit
    assert cog._state is None


# ---------------------------------------------------------------------------
# Test 10: Vision failure twice → skip cycle (no place_move for that turn)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_vision_retry_then_skip() -> None:
    """When extract_board_state fails twice, place_move is NOT called; loop handles game_over next cycle."""
    cog = AutoPlayCog(_make_mock_bot())
    channel = AsyncMock()
    channel.send = AsyncMock()

    with patch("src.bot.autoplay_cog.BrowserSession") as MockSession, \
         patch("src.bot.autoplay_cog.navigate_to_activity", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.preflight_check", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.wait_for_game_ready", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.click_start_game", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.poll_turn", new_callable=AsyncMock) as mock_poll, \
         patch("src.bot.autoplay_cog.capture_canvas", new_callable=AsyncMock) as mock_capture, \
         patch("src.bot.autoplay_cog.extract_board_state", new_callable=AsyncMock) as mock_vision, \
         patch.dict(os.environ, {"VOICE_CHANNEL_URL": "https://discord.com/channels/1/2"}):

        mock_page = MagicMock()
        mock_session = AsyncMock()
        mock_session.start = AsyncMock(return_value=mock_page)
        mock_session.close = AsyncMock()
        MockSession.return_value = mock_session

        # Set state so the loop assertion passes
        cog._state = LoopState(phase=AutoPlayPhase.STARTING, channel_id=42)

        # First poll: my_turn (vision fails); second poll: game_over (exits loop)
        mock_poll.side_effect = ["my_turn", "game_over"]
        mock_capture.return_value = b"fake_png"

        # Vision always fails
        mock_vision.side_effect = Exception("Vision API unavailable")

        mock_placer = AsyncMock()
        mock_placer.place_move = AsyncMock(return_value=True)

        with patch("src.bot.autoplay_cog.TilePlacer", return_value=mock_placer):
            await cog._run_game_loop(channel, "https://discord.com/channels/1/2")

    # place_move should NOT have been called (vision failed, cycle was skipped)
    mock_placer.place_move.assert_not_awaited()

    # extract_board_state should have been called exactly twice (two attempts on the failed cycle)
    assert mock_vision.call_count == 2

    # Gameover embed should have been posted after the second poll_turn cycle
    channel.send.assert_awaited()
    final_embed = channel.send.call_args.kwargs.get("embed")
    assert final_embed is not None
    assert final_embed.title == "Game Over"


# ---------------------------------------------------------------------------
# Test 11: cog_unload cancels the running task
# ---------------------------------------------------------------------------

def test_cog_unload_cancels_task() -> None:
    """cog_unload() cancels the loop task if it is still running."""
    cog = AutoPlayCog(_make_mock_bot())

    mock_task = MagicMock()
    mock_task.done.return_value = False
    cog._loop_task = mock_task

    cog.cog_unload()

    mock_task.cancel.assert_called_once()


# ---------------------------------------------------------------------------
# Test 12: Stop during poll_turn exits loop without further turn processing
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_stop_during_poll_turn_exits_cleanly() -> None:
    """When poll_turn returns 'stop_requested', loop exits without placing a move."""
    cog = AutoPlayCog(_make_mock_bot())
    channel = AsyncMock()
    channel.send = AsyncMock()

    with patch("src.bot.autoplay_cog.BrowserSession") as MockSession, \
         patch("src.bot.autoplay_cog.navigate_to_activity", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.preflight_check", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.wait_for_game_ready", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.click_start_game", new_callable=AsyncMock), \
         patch("src.bot.autoplay_cog.poll_turn", new_callable=AsyncMock) as mock_poll, \
         patch.dict(os.environ, {"VOICE_CHANNEL_URL": "https://discord.com/channels/1/2"}):

        mock_page = MagicMock()
        mock_session = AsyncMock()
        mock_session.start = AsyncMock(return_value=mock_page)
        mock_session.close = AsyncMock()
        MockSession.return_value = mock_session

        cog._state = LoopState(phase=AutoPlayPhase.STARTING, channel_id=42)

        # poll_turn immediately signals stop (as if stop_event fired during polling)
        mock_poll.return_value = "stop_requested"

        mock_placer = AsyncMock()
        mock_placer.place_move = AsyncMock(return_value=True)

        with patch("src.bot.autoplay_cog.TilePlacer", return_value=mock_placer):
            await cog._run_game_loop(channel, "https://discord.com/channels/1/2")

    # No move should have been placed
    mock_placer.place_move.assert_not_awaited()

    # No channel message should have been sent (no embed for a clean stop)
    channel.send.assert_not_awaited()

    # State should be reset after loop exit
    assert cog._state is None
