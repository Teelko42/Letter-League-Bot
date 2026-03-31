---
phase: 8
slug: autonomous-game-loop
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-31
---

# Phase 8 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x + pytest-asyncio |
| **Config file** | none — pytest runs with defaults |
| **Quick run command** | `py -3 -m pytest tests/test_autoplay_cog.py -x -q` |
| **Full suite command** | `py -3 -m pytest tests/ -q` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `py -3 -m pytest tests/test_autoplay_cog.py -x -q`
- **After every plan wave:** Run `py -3 -m pytest tests/ -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 8-01-01 | 01 | 1 | LOOP-01 | unit | `py -3 -m pytest tests/test_autoplay_cog.py::test_loop_runs_as_task -x` | ❌ W0 | ⬜ pending |
| 8-01-02 | 01 | 1 | LOOP-02 | unit | `py -3 -m pytest tests/test_autoplay_cog.py::test_start_guard -x` | ❌ W0 | ⬜ pending |
| 8-01-03 | 01 | 1 | LOOP-02 | unit | `py -3 -m pytest tests/test_autoplay_cog.py::test_status_idle -x` | ❌ W0 | ⬜ pending |
| 8-01-04 | 01 | 1 | LOOP-03 | unit (existing) | `py -3 -m pytest tests/test_tile_placer.py -x` | ✅ verify | ⬜ pending |
| 8-01-05 | 01 | 1 | LOOP-04 | unit | `py -3 -m pytest tests/test_autoplay_cog.py::test_swap_on_no_moves -x` | ❌ W0 | ⬜ pending |
| 8-01-06 | 01 | 1 | LOOP-05 | unit | `py -3 -m pytest tests/test_autoplay_formatter.py -x` | ❌ W0 | ⬜ pending |
| 8-01-07 | 01 | 1 | BROW-03 | unit | `py -3 -m pytest tests/test_autoplay_cog.py::test_reconnect_backoff -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_autoplay_cog.py` — stubs for LOOP-01, LOOP-02, LOOP-04, BROW-03
- [ ] `tests/test_autoplay_formatter.py` — stubs for LOOP-05 embed builders
- [ ] `py -3 -m pip install pytest-asyncio` — needed for async test coroutines

*Existing infrastructure covers LOOP-03 via Phase 7 tests.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Browser reconnects after Activity disconnect | BROW-03 | Requires live Discord Activity session | 1. Start autoplay, 2. Kill Activity iframe in DevTools, 3. Verify bot reconnects within 3 retries |
| Human-like timing feels natural in live game | LOOP-03 | Subjective assessment of delay randomization | Watch autoplay run for 5+ turns, verify actions don't fire at machine speed |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
