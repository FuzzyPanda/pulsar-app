# Pulsar app — project context

Read `README.md` and `docs/PLAN.md` first. This file holds the rules and the starting point.

## What this is

One Expo (React Native, TypeScript) app for iOS, Android and web. Staff see their roster, clock in,
and carry their door credential. Managers see who is on site, door status and alerts, and approve
timesheets and leave. It signs in through Pulsar Hub and shows only the modules the organisation
has switched on.

## Rules that do not bend

1. **Do not rewrite what the TIM2 app already does.** Phase A1 imports it with history and
   restructures it. Its offline-safe clocking and its tests come across intact.
2. **The app never talks to a PAC gateway.** Everything about doors goes through the hub.
3. **No secrets in the bundle.** No API keys, signing keys or service tokens in the repo or the
   build. Tokens live in the platform secure store, never in plain storage.
4. **Money is never shown to staff accounts.** Pay and charge rates do not reach the app.
5. **Location is captured only at clock-in and clock-out**, never tracked in between. The app says
   so on the screen that asks for permission.
6. **Clocking works offline** and syncs with an idempotency key, so a retry never double-records.
7. **A door credential must not survive a screenshot.** The rotating code is short-lived, shown
   only after device unlock, and hidden when the app is backgrounded.
8. **Remote door actions need a fresh biometric or MFA check every time**, show the door and site
   by name before confirming, and never include emergency unlock.
9. **Unknown response fields are ignored; removed fields need a new API version.** The app must
   keep working against an older server during a rollout.
10. **No member-facing features.** No memberships, class bookings or member check-in. Staff only.
    At a PerfectGym site the Access module is off: PerfectGym handles access there, and staff get
    the Roster module only.
11. **The bundle identifier and app name are permanent once published.** Do not submit to a store
    until decision D1 is made.

## Where to start

- **Before the TIM2 app exists in `TimeIsMoney2/mobile/`:** only phase A0. Do not scaffold a new
  Expo project here; an empty scaffold would collide with the import in A1.
- **Once it exists and has run on phones:** phase A1, starting with the history-preserving import.
- Tick boxes in `docs/PLAN.md` as items land.

## Commands

To be filled in by the A1 session after the import (`npm install`, `npx expo start`,
`npm test`, `npx tsc --noEmit`, EAS build profiles).
