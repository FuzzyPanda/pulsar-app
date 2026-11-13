# Module map

**Drafted 2026-11-13. Proposed; not yet agreed.** This is the A0 item "Module map agreed". When it
is agreed, tick the box in `PLAN.md` and change this line.

## What merges into this app

| App | Where it lives today | What happens |
|---|---|---|
| Roster app (TIM2 employee app) | Planned in `TimeIsMoney2/mobile/` | Imported with history in A1; becomes the Roster module |
| Access control app (staff and manager) | Not built. PAC parks the member-facing app and has no staff app | Built here as the Access module, A3 to A5 |
| Pulsar Field (installer app) | `Pulsar-Access-Control/apps/android-field/` | Stays separate. Never merges |

The owner's direction on 2026-11-13 is that the roster app and the access control app will
"probably" merge into this one. It is recorded as probable, not final, in `DECISIONS.md`.

## Modules

| Module | Server behind it | Staff see | Managers see | Phase |
|---|---|---|---|---|
| **Roster** | TIM2 | My roster, clock in and out | Approve timesheets and leave | A1, A4 |
| **Access** | Pulsar Hub only, never a gateway | Door credential, my access | Who is on site, door status and events, alerts, add or end access by group, remote door actions | A3, A4, A5 |
| **IT** | Pulsar support | Support link, report a problem | Same | A6 |

Shared **core**, used by every module and owned by none: sign-in and session, API client, offline
queue, notifications, theme.

## Rules for the map

1. **A module is on or off per organisation**, decided by the hub's response at sign-in. Nothing
   is hard-coded in the app (A2).
2. **A hidden module is not a permission.** The server refuses the call as well (A4).
3. **A module that is off leaves no trace**: no tab, no empty screen, no notification category.
4. **Modules do not import from each other.** Anything two modules need lives in core.
5. **PerfectGym sites get Roster only.** Access is off there (rule 10 in `CLAUDE.md`).
6. **Standalone TIM2 installs get Roster only**, signed in to their own server (decision D2).
7. **Money never reaches a staff account** in any module (rule 4 in `CLAUDE.md`).

## Folder shape after A1

```
modules/
  roster/     the imported TIM2 screens, behaviour unchanged
  access/     empty until A3
  it/         empty until A6
core/
  auth/  api/  offline/  notifications/  theme/
```

## Questions the map raises

| # | Question | Why it matters |
|---|---|---|
| M1 | Is "who is on site" an Access screen, a Roster screen, or both? | Door events say who badged in. Clock-ins say who is on shift. At a PerfectGym or standalone TIM2 site only clock-ins exist, so an Access-only screen would be blank there |
| M2 | Are alerts one inbox in core or one list per module? | A manager with both modules gets door alerts and roster alerts. One inbox is simpler to use; per-module lists are simpler to switch off |
| M3 | Does a person who is a manager at one site and staff at another see both views at once? | Decides whether role is per organisation or per site in the hub's response (A2) |
