# Decisions

Open decisions first. Move an entry to "Made" with its date when it is settled.

## Open

| # | Decision | Recommendation | Blocks |
|---|---|---|---|
| D1 | App name and bundle identifier | Decide with the hub and rostering product names (hub decision D1). TIM2's plan notes the current placeholders are "TimeIsMoney" and `com.example.timeismoney`; a bundle id is permanent once published | Any store submission |
| D2 | One app or two | One app. Standalone TIM2 installs sign in to their own server from the same app; do not keep a second TIM2-only app alive | A1, A2 |
| D3 | When to extract from TIM2 | After the TIM2 pilot has run on real phones for a few weeks, so fixes land once and not in two repos | A1 |
| D4 | Native tap-to-enter (NFC or Bluetooth) | Not now. The rotating QR covers it without native modules or reader changes; revisit on client demand | Beyond A3 |
| D5 | Web build | Keep it. It gives staff without the app a way in and makes testing cheap | A1 |
| D6 | PAC guardrail on mobile apps | PAC's `CLAUDE.md` parks a member-facing app. This is a staff and manager app, a different audience, but it needs the same explicit sign-off through the PAC overseer before door features ship | A3 |

## Made

| Date | Decision |
|---|---|
| 2026-11-13 | The app is seeded from the TIM2 mobile app once that is done, in its own repo. |

## Assumed by this draft, not yet confirmed

| Assumption | Where it matters |
|---|---|
| The app never talks to a gateway directly; door features go through the hub | A3 to A5 |
| Sign-in moves to the hub once it exists | A2 |
