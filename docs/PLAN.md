# Plan

**Drafted 2026-11-13. Proposed; nothing is built.** Tick items as they land.

## Phases at a glance

| Phase | Outcome | Depends on |
|---|---|---|
| A0 | Groundwork that needs no code | — |
| A1 | The TIM2 app lives here, restructured into modules | TIM2 app proven on phones |
| A2 | Sign in through the hub; choose an organisation | Hub H1 |
| A3 | Staff: door credential and my access | Hub H5 |
| A4 | Managers: who is on site, doors, alerts, approvals | Hub H4, TIM2 manager API |
| A5 | Managers: remote door actions | Hub H6 |
| A6 | IT: support and device help | Later |

## A0 — Groundwork (can start now)

- [ ] Decision D1: name, bundle identifier, icon. Nothing can be published without it.
- [ ] Apple and Google developer accounts under the business, not a personal account.
- [ ] Module map agreed: **Roster** (TIM2), **Access** (hub), **IT** (later). An organisation sees
  only what it has switched on. Drafted in [`MODULES.md`](MODULES.md); needs the owner's agreement
  and answers to M1 to M3 there.
- [ ] Decide what happens to the TIM2-only app for standalone installs: decision D2.
- [ ] List every TIM2 mobile API call the app uses and mark which move behind hub sign-in. Not
  started: the 2026-11-13 session could not read the TIM2 repo.
- [ ] Privacy text for location, camera and notifications. Location, notifications and Face ID
  drafted in [`PRIVACY-TEXT.md`](PRIVACY-TEXT.md); camera waits on the TIM2 repo; none reviewed.
- [ ] Access groundwork: what PAC has today and what the hub and PAC must build before A3 to A5.
  Written up in [`ACCESS-GROUNDWORK.md`](ACCESS-GROUNDWORK.md); decisions D6 to D9 follow from it.

## A1 — Import and restructure

- [ ] Bring `TimeIsMoney2/mobile/` across with its history (`git subtree split`, then merge here).
  Record the TIM2 commit it was taken from.
- [ ] From that point this repo is the only home of the app; remove `mobile/` from TIM2 in a
  matching pull request so there are never two copies.
- [ ] Folder structure by module: `modules/roster`, `modules/access`, `modules/it`, with shared
  `core` (auth, API client, offline queue, notifications, theme).
- [ ] The existing screens become the Roster module unchanged in behaviour.
- [ ] CI: type check, unit tests, lint on every pull request. EAS build profiles for development,
  preview and production.
- [ ] Demo workspace still works with no server.

## A2 — Hub sign-in

- [ ] Sign in with the hub (OIDC, authorisation code with PKCE); tokens in the secure store.
- [ ] Organisation switcher for people who belong to more than one.
- [ ] Module visibility from the hub's response, not hard-coded.
- [ ] Keep direct sign-in to a standalone TIM2 server, per decision D2.
- [ ] MFA prompts, session expiry and remote sign-out handled cleanly.
- [ ] Push notification registration moves to the hub, with a per-device record.

## A3 — Staff access

- [ ] Rotating QR door credential, following rule 7 in `CLAUDE.md`. Works with poor signal: the
  secret is held on the device, the code is generated locally.
- [ ] "My access": which sites and doors I can open, and when.
- [ ] Clear states: no access, suspended, credential revoked, clock out of sync.

## A4 — Manager view

- [ ] Who is on site now, per site and across sites.
- [ ] Door status and recent events; alerts as notifications.
- [ ] Approve timesheets and leave (TIM2's planned manager features).
- [ ] Add or end a person's access by access group; card enrolment stays on site.
- [ ] Role checks on the server; hiding a screen is not a permission.

## A5 — Remote door actions

- [ ] Timed unlock of one door and site lockdown only. No emergency unlock.
- [ ] Fresh biometric or MFA check per action, door and site named on the confirm screen, a reason
  captured.
- [ ] Show "requested" until the gateway confirms, then the result. Never show success on send.
- [ ] Does not ship before the hub and PAC sides have passed their security review.

## A6 — IT

- [ ] Start with a link to Pulsar support and a "report a problem" form. Nothing more until a
  client asks.

## Order

A0 → A1 → A2 → A3 → A4 → A5. A6 whenever it is wanted.
