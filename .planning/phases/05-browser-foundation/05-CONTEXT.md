# Phase 5: Browser Foundation - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Launch a persistent patchright browser session with a saved Discord login, navigate to a target voice channel, open the Letter League Activity iframe, and capture a canvas screenshot that passes through the existing vision pipeline. Session management, navigation, and screenshot capture are in scope. Turn detection, tile placement, and game loop are separate phases.

</domain>

<decisions>
## Implementation Decisions

### Operator login flow
- Manual browser login on first run — bot opens a visible Chromium window, operator logs into Discord manually
- First-run only trigger — bot detects no saved profile and opens the login window automatically
- Browser profile (cookies/session) stored in a project subdirectory (e.g., `./browser_data/`)
- Login completion auto-detected by waiting for a Discord page element (sidebar, friends list) to appear
- After login detected, keep the same browser session open and proceed to navigation (no relaunch)

### Failure behavior
- Expired session at startup: log a clear warning message explaining the issue and how to re-login, then exit cleanly
- All failure messages go to console/log only (Python logging) — no Discord DMs
- Navigation failures (voice channel, Activity): retry 2-3 times with short waits, then log error and exit
- Startup validates the captured screenshot through the full `extract_board_state()` vision pipeline, not just a non-blank check

### Browser visibility
- Headless by default during normal operation (after login is saved)
- No headed/debug toggle — keep it simple, edit code if debugging needed
- First-run login keeps the visible browser open and transitions to work (no close + relaunch)
- Fixed viewport size set at browser launch for consistent canvas screenshot dimensions

### Channel targeting
- Target voice channel specified via config file (e.g., `.env` or `config.json`)
- Config value is the full Discord URL (e.g., `https://discord.com/channels/SERVER_ID/CHANNEL_ID`) — operator copy-pastes from browser
- Navigation via direct URL — navigate straight to the channel URL, don't click through Discord UI
- Activity launch method at Claude's discretion (research best approach — Activity shelf click vs direct URL)

### Claude's Discretion
- Activity launch mechanism (click shelf vs direct URL — research what's most reliable)
- Fixed viewport dimensions (research what size works best for the game canvas)
- Exact Discord element to detect for login completion
- Retry timing and backoff strategy for navigation failures
- Pixel-variance threshold for non-blank screenshot check (used before full pipeline validation)

</decisions>

<specifics>
## Specific Ideas

- Uses patchright (Playwright fork) as the browser automation library
- The existing `extract_board_state()` function from Phase 3 must work unmodified on the captured screenshot
- Browser profile directory should be gitignored

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 05-browser-foundation*
*Context gathered: 2026-03-25*
