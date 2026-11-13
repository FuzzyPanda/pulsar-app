# Decisions

Open decisions first. Move an entry to "Made" with its date when it is settled.

## Open

| # | Decision | Recommendation | Blocks |
|---|---|---|---|
| D1 | App name and bundle identifier | Decide with the hub and rostering product names (hub decision D1). The phone app's placeholders today are "Pulsar Roster" and `com.example.pulsarroster`; a bundle id is permanent once published, and an Android phone treats a changed one as a different app | Any store submission |
| D2 | One app or two | One app. Standalone Pulsar Roster installs sign in to their own server from the same app; do not keep a second Pulsar Roster-only app alive | A1, A2 |
| D3 | When to extract from Pulsar Roster | After the Pulsar Roster pilot has run on real phones for a few weeks, so fixes land once and not in two repos | A1 |
| D4 | Native tap-to-enter (NFC or Bluetooth) | Not now. The rotating QR needs no native modules or reader changes, but it does need gateway changes: see D7. Revisit on client demand | Beyond A3 |
| D5 | Web build | Keep it. It gives staff without the app a way in and makes testing cheap | A1 |
| D6 | PAC guardrail on mobile apps | PAC's `CLAUDE.md` parks a member-facing app. This is a staff and manager app, a different audience, but it needs the same explicit sign-off through the PAC overseer before door features ship. PAC has no un-park procedure; the precedent is Pulsar Field: an owner decision recorded in PAC's backlog and its `CLAUDE.md` section 14 | A3 |
| D7 | How the gateway checks a rotating QR | Shared secret per phone, checked on the gateway, because the plan needs it to work with poor signal. PAC matches only static codes today and its own backlog leaves mobile credentials undecided. See `ACCESS-GROUNDWORK.md` | A3 |
| D8 | How the hub reaches a gateway | Raise it in PAC now. PAC has no design for an outside service calling in, and ranks remote write actions as Wave 3, not started, gated on a stable pilot site | A3, A4, A5 |
| D9 | Operator timed unlock in PAC | PAC needs a new operator action. Only the installer test pulse exists. The hub must also never pass on PAC's `emergency_unlock` lockdown action | A5 |
| D10 | Is a separate app repo still needed? | Decide before A1. The phone app in `pulsar-rostering/apps/mobile/` already describes itself as one app for every kind of user, with modules per organisation and an organisation switcher. That is most of A1 and A2. Either extract it here as planned, or keep it there and retire this repo | A1 |

## Made

| Date | Decision |
|---|---|
| 2026-11-13 | The app is seeded from the Pulsar Roster mobile app once that is done, in its own repo. |
| 2026-11-13 | `TimeIsMoney2` is no longer used. Rostering lives in `FuzzyPanda/pulsar-rostering`; the phone app is `apps/mobile/` there, named "Pulsar Roster". |

## Assumed by this draft, not yet confirmed

| Assumption | Where it matters |
|---|---|
| The app never talks to a gateway directly; door features go through the hub | A3 to A5 |
| Sign-in moves to the hub once it exists | A2 |
| The roster app and the access control app both merge into this app. The owner said "probably" on 2026-11-13. Pulsar Field, the installer app, does not | A1, A3 |
| "Access is off at a PerfectGym site" is a per-organisation setting in the hub. PAC has no such switch | A2, A3 |
| "The hub" means `FuzzyPanda/pulsar-hub`. `pulsar-rostering` also calls itself "Platform (hub)" and separately links to Pulsar Hub, so the word covers two things. This draft has not read `pulsar-hub` | A2 |
| Standalone installs with their own server (decision D2) still exist. `pulsar-rostering` describes one hosted service; if that is the only deployment, D2 is moot | A1, A2 |
