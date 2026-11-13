# Access groundwork

**Written 2026-11-13 from a read of `Pulsar-Access-Control` at commit `416eef1`.** Nothing here was
run; it is what the code and docs say. The hub repo and the TIM2 repo were not read.

This file answers one question: what does the Access module (A3 to A5) need that the gateway does
not have yet? The app never calls a gateway, so every gap below is work for the hub, PAC or both
before the app can ship the matching phase.

## Summary

| Phase | App feature | PAC today | Verdict |
|---|---|---|---|
| A3 | Rotating QR door pass | QR codes are static strings matched by keyed hash | **Blocked.** A rotating code is denied as an unknown credential |
| A3 | My access | People, access levels, schedules exist; no "what can this person open" answer | Needs a computed view |
| A4 | Who is on site | Zone head-counts and a muster list; no list of named people over the API | Needs an endpoint |
| A4 | Door status and events | Both exist and are read-only for every role | Ready for the hub to relay |
| A4 | Alerts as notifications | Email, SMS, webhook and browser push; no phone push | Hub sends the phone push |
| A4 | Add or end access by group | Exists: write a person's access levels | Ready for the hub to relay |
| A5 | Timed unlock of one door | Only the installer test pulse | **Blocked.** No operator timed unlock |
| A5 | Site lockdown | Exists on site | Needs a hub-to-gateway channel |
| All | Hub reaches the gateway | No design for an outside service calling in | **Blocked.** PAC ranks this Wave 3, not started |

## A3: the rotating QR pass

Decision D4 here says the rotating QR works "without native modules or reader changes". The reader
half is true. The gateway half is not.

- A scanned QR becomes `code:<payload>`, is hashed with the gateway's key, and is looked up in the
  credentials table (`packages/schemas/credential.go`, `ScanID`). A code that changes every few
  seconds never matches a row.
- Nothing in PAC's Go or Python code checks a time-based, signed or one-time code. Visitor passes
  are a fixed random token with a start and end time.
- PAC already denies a scan older than 5 seconds and rejects reader clocks more than 5 minutes
  out, so a short-lived code fits the existing timing rules.
- PAC's own backlog lists "QR code / mobile credential delivery" as undecided, with the question
  "Does this need server-side generation (keys, expiry, one-time use)?" still open.

Two ways to close it, both gateway work:

| Option | How it works | Trade-off |
|---|---|---|
| Shared secret per phone | Phone and gateway derive the same code from a secret and the time | Works offline at both ends, which the plan requires. The gateway must store the secret readably, unlike every other credential, which is a one-way hash |
| Hub-signed short token | Hub signs a token; the gateway checks the signature | No secret on the gateway. The phone needs signal to fetch tokens, which breaks "works with poor signal" unless tokens are fetched ahead |

This is decision D7.

Rule 7 in `CLAUDE.md` says the pass must not survive a screenshot. Android can block screenshots
of a screen. iOS cannot; an app can only notice one was taken and hide the screen in the app
switcher. On iPhone the short life of the code is the whole defence, so the code lifetime and the
gateway's replay check carry rule 7 between them.

## A3: my access

- PAC models people, access levels, door-to-level links, schedules and holiday calendars, each
  with an endpoint.
- No endpoint answers "which doors can this person open, and when". The rules are evaluated only
  inside the Go decision engine.
- A PAC person can link to a login, but that link is used only for lone-worker check-in. Mapping a
  hub user to a PAC person is new.

If the hub rebuilds the answer from raw levels and schedules, it will drift from what the door
actually does. The answer should come from the gateway.

## A4: the manager view

| Need | PAC today |
|---|---|
| Door status | `GET /api/door-states/`, written only by the door controller, with the mode actually applied |
| Recent events | `GET /api/policy-events/`, filterable, with person names |
| Alarms and system events | `/api/alarm-areas/`, `/api/system-events/` with acknowledge |
| Who is on site, by name | Not available. Occupancy gives counts per zone. The muster list has names but only on a web page, not the API |
| Phone notifications | PAC's phone push is switched off; it has email, SMS, webhook and browser push. The hub would take PAC's webhook and send the phone push itself |
| Add or end access | Write `access_levels` on a person; operator and administrator roles |

## A5: remote door actions

Rule 8 allows two actions: timed unlock of one door, and site lockdown.

- **Timed unlock does not exist for operators.** The only pulse is the installer test pulse
  (installer and administrator roles, 0.1 to 5 seconds, for commissioning). Operators can only set
  latching modes: normal, lockdown, emergency unlock, disabled.
- **Lockdown exists** at `POST /api/lockdown/`, by door group, alarm area, zone or site.
- **The same endpoint also accepts `emergency_unlock`.** The hub must never pass that action
  through. Rule 8 here is stricter than PAC, whose fleet rules list "remote unlock" without
  excluding it.
- **"Requested until confirmed" is already how PAC works.** The web console shows "Requested —
  waiting for the door controller" until the controller reports the applied mode. The app's A5
  rule matches; the hub needs to relay the applied state, not the request.
- **PAC says a lockdown is never cleared by a timeout**, only by a person or an authenticated
  action. The app must not offer a lockdown that ends by itself.

PAC's rules for any remote write action (its `fleet-control-plane` skill):

1. Mutual TLS on every call, with certificates that can be revoked at once.
2. Every action logged at both ends, each log readable without the other.
3. A short, fixed list of allowed actions per role.
4. The action is a request recorded on the gateway; the door controller carries it out.
5. Egress is never blocked remotely.
6. A confirm step naming the site and the consequence.

PAC has no rule for a fresh biometric or MFA check per action. That part is this app's and the
hub's to supply.

## The channel from hub to gateway

This is the largest gap and it sits under everything above.

- PAC is built to run with no cloud. Remote access today is a mesh VPN used by the operator of the
  system, described as "MSP-operated, not customer cloud".
- Cross-site write actions are Wave 3 in PAC's plan, **not started**, and gated on at least one
  stable pilot site.
- Per-site device certificates exist but are off by default.
- PAC's docs never mention Pulsar Hub, TIM2 or a staff app.

So A3 to A5 depend on a PAC decision that has not been raised there yet. This is decisions D6
and D8.

## PerfectGym

Rule 10 says the Access module is off at a PerfectGym site. PAC has no such switch: PerfectGym is
one membership provider among several, and PAC still runs the doors at those sites. PAC's
PerfectGym work was paused by the owner on 2026-10-06. "Access is off" is therefore a setting the
hub holds per organisation, not something the gateway reports.

## Names that do not line up

`README.md` names `FuzzyPanda/pulsar-hub`. No repo of that name was visible on 2026-11-13; a
`FuzzyPanda/pulsar-core` was. Confirm which repo holds the hub and fix the table in the README.
