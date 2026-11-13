# Pulsar app

**Status: planning. No code yet.** Working name; the product name is an open decision.

One mobile app for a client's staff and managers across Pulsar products: rosters and clock-in from
Time Is Money 2, door access from Pulsar Access Control, signed in once through Pulsar Hub.

## Where the code comes from

This repo is **seeded from the Time Is Money 2 employee app**, not written from scratch. That app is
planned in the TIM2 product branch as an Expo (React Native) app for iOS, Android and web in
`mobile/`, against the contract in `TimeIsMoney2/docs/api/mobile-v1.md`. As of 2026-11-13 the
`mobile/` folder was not yet on the TIM2 product branch.

The extraction happens when that app has run on real phones in the TIM2 pilot. Until then, work
here is limited to phase A0 in the plan.

## Read next

- [`docs/PLAN.md`](docs/PLAN.md) — phases and checklists
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — open decisions that block work
- [`CLAUDE.md`](CLAUDE.md) — rules and where a coding session should start

## Related repos

| Repo | Role |
|---|---|
| `FuzzyPanda/pulsar-hub` | Sign-in, organisations, people, sites, door access. Contract: `docs/CONTRACTS.md` there |
| `FuzzyPanda/TimeIsMoney2` | Rostering and attendance; source of the app's first screens |
| `FuzzyPanda/Pulsar-Access-Control` | The on-site gateway. The app never talks to a gateway directly. Its installer app, Pulsar Field, is separate and stays separate |
