# CLAUDE.md — Pulsar app

One Expo (React Native, TypeScript) app for iOS, Android and web. Staff see their roster, clock in and carry
their door credential; managers see who is on site and approve timesheets and leave. It signs in through Pulsar
Hub and shows only the modules the organisation has switched on.

**Read first:** `README.md`, then `docs/PLAN.md`. Current phase: A0 (planning only). Don't scaffold an Expo
project here before phase A1's history-preserving import; an empty scaffold would collide with it.

## Rule 0: this repository is public

Everything committed here, including history, PR text and release notes, can be read by anyone. Never add
hostnames, IP addresses, client or partner names, private repository names, internal tool names, security
designs or gaps, endpoint details or unreleased commercial plans. Planning that needs them lives in the private
repositories, linked by name only where the name is already public. When unsure, leave it out and ask Adam.
Enforced today by review only; a secret scan in CI is a follow-up.

## Rules that do not bend

1. **Don't rewrite what the existing staff app already does.** Phase A1 imports it with history and
   restructures it; its offline-safe clocking and its tests come across intact.
2. **The app never talks to a site's door controller directly.** Everything about doors goes through the hub.
3. **No secrets in the bundle.** No API keys, signing keys or service tokens in the repo or the build. Tokens
   live in the platform secure store, never in plain storage. Signing files are git-ignored and deny-listed in
   `.claude/settings.json`.
4. **Money is never shown to staff accounts.** Pay and charge rates do not reach the app.
5. **Location is captured only at clock-in and clock-out**, never tracked in between, and the permission screen
   says so (`docs/PRIVACY-TEXT.md`).
6. **Clocking works offline** and syncs with an idempotency key, so a retry never double-records.
7. **A door credential must not survive a screenshot:** short-lived, shown only after device unlock, hidden
   when the app is backgrounded.
8. **Remote door actions need a fresh biometric or MFA check every time** and name the door and site before
   confirming.
9. **Unknown response fields are ignored; removed fields need a new API version.**
10. **Staff only.** No member-facing features. Which modules apply at which kind of site: `docs/MODULES.md`.
11. **The bundle identifier and app name are permanent once published.** Don't submit to a store until
    decision D1 is made. `eas submit` and `gh release` ask first.

Each rule gets a named enforcer (a test or CI step) in phase A1; until then, check them in review.

## Commands

None yet. Phase A1 adds them from the imported app (install, type check, tests, web export, lint).

## How to work here

- Australian English in UI copy and docs.
- Tick boxes in `docs/PLAN.md` as items land; record decisions in `docs/DECISIONS.md`.
- `.claude/hooks/` are vendored guard hooks (hash-checked by `.claude/pulsar-kit.lock`); don't edit them here.
