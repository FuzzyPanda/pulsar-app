# Pulsar app

**Status: planning. No code yet.** Working name; the product name is an open decision.

One mobile app for a client's staff and managers across Pulsar products: rosters and clock-in from
Pulsar Roster, door access from Pulsar Access Control, signed in once through Pulsar Hub.

## Where the code comes from

This repo is **seeded from the Pulsar Roster phone app**, not written from scratch. That app is an
Expo (React Native) app for iOS, Android and web in `pulsar-rostering/apps/mobile/`, built against
the contract in `pulsar-rostering/openapi/schema.yaml`.

The old `TimeIsMoney2` repo is no longer used (owner, 2026-11-13). Rostering moved to
`FuzzyPanda/pulsar-rostering`, read here at commit `91a7041`. Its own handover says the phone app
passes its tests and a scripted run of the web test build, and that **nothing has been built for
or run on a real phone**. It has no Android build and no releases.

The extraction happens when that app has run on real phones in the Pulsar Roster pilot. Until then, work
here is limited to phase A0 in the plan. Whether the extraction should still happen at all is
decision D10.

## Read next

- [`docs/PLAN.md`](docs/PLAN.md) — phases and checklists
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — open decisions that block work
- [`docs/MODULES.md`](docs/MODULES.md) — what merges in, and the module map (draft)
- [`docs/ACCESS-GROUNDWORK.md`](docs/ACCESS-GROUNDWORK.md) — what PAC has and lacks for the Access module
- [`docs/PRIVACY-TEXT.md`](docs/PRIVACY-TEXT.md) — permission wording (draft)
- [`CLAUDE.md`](CLAUDE.md) — rules and where a coding session should start

## Related repos

| Repo | Role |
|---|---|
| `FuzzyPanda/pulsar-hub` | Sign-in, organisations, people, sites, door access. Contract: `docs/CONTRACTS.md` there |
| `FuzzyPanda/pulsar-rostering` | Rostering and attendance; source of the app's first screens |
| `FuzzyPanda/Pulsar-Access-Control` | The on-site gateway. The app never talks to a gateway directly. Its installer app, Pulsar Field, is separate and stays separate |
