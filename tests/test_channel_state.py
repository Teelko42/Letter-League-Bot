"""Tests for ChannelStore and ChannelState (Phase A5).

Pure in-memory state management — no mocking needed.
"""

from __future__ import annotations

from src.bot.channel_state import ChannelState, ChannelStore


class TestChannelStore:
    def test_get_creates_default_state(self):
        store = ChannelStore()
        state = store.get(12345)
        assert state.difficulty == 100
        assert state.mode == "wild"

    def test_get_same_channel_returns_same_object(self):
        store = ChannelStore()
        s1 = store.get(123)
        s2 = store.get(123)
        assert s1 is s2

    def test_set_difficulty_updates_and_returns(self):
        store = ChannelStore()
        state = store.set_difficulty(123, 50)
        assert state.difficulty == 50
        assert store.get(123).difficulty == 50

    def test_set_mode_updates_and_returns(self):
        store = ChannelStore()
        state = store.set_mode(123, "classic")
        assert state.mode == "classic"
        assert store.get(123).mode == "classic"

    def test_separate_channels_isolated(self):
        store = ChannelStore()
        store.set_difficulty(1, 25)
        state2 = store.get(2)
        assert state2.difficulty == 100  # default, not channel 1's value
