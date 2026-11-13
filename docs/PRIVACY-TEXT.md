# Privacy and permission text

**Drafted 2026-11-13. Draft wording; not reviewed by the owner or a lawyer.** This is the A0 item
"Privacy text for location, camera and notifications". The words here are what the phone shows
when it asks, plus the screen the app shows first.

## How the app asks

1. The app explains on its own screen before the phone's prompt appears. The phone's prompt can
   only be shown once on iOS, so it is never the first thing a person sees.
2. Each permission is asked for at the moment it is needed, not at first launch.
3. Saying no never locks a person out of the app. Each section says what still works.

## Location

Asked the first time a person clocks in. Rule 5 in `CLAUDE.md` requires the app to say on this
screen that location is not tracked between clock-in and clock-out.

**App screen, before the prompt**

> **Location at clock-in and clock-out only**
> When you clock in or out, the app records where you are, once, so your employer can confirm you
> were on site. It does not track you during your shift, on breaks, or after you clock out.
>
> [Continue] [Not now]

**Phone prompt (iOS `NSLocationWhenInUseUsageDescription`)**

> Your location is recorded once when you clock in and once when you clock out. It is not tracked
> in between.

**If the answer is no**

> You can still clock in. Your employer will see that no location was recorded for this shift.

Whether a clock-in without location is accepted is the employer's setting in Pulsar Roster, not the app's
decision. Confirm the wording above against that setting before it ships.

**This draft does not match the phone app as built.** The phone app's own prompt says: "Your
position is read while the Today screen is open, to show whether you are at your site, and is
attached to clock-ins and clock-outs so your employer can confirm attendance. It is never tracked
in the background." Reading position while a screen is open is more than "once at clock-in and
once at clock-out", which is what this draft and rule 5 in `CLAUDE.md` say. Either the app changes
or the rule and this wording do. Until that is settled, the phone app's wording is the accurate
one.

**Build settings that keep the promise**

| Platform | Setting |
|---|---|
| iOS | "When in use" only. No `NSLocationAlwaysAndWhenInUseUsageDescription`, no location background mode |
| Android | `ACCESS_FINE_LOCATION` only. `ACCESS_BACKGROUND_LOCATION` is never declared |
| Both | One reading per clock event. No watch or subscription is ever started |

## Notifications

Asked after first sign-in, once the person has seen their roster.

**App screen, before the prompt**

> **Stay up to date**
> Get a notification when your roster changes or a shift is about to start. Managers also get
> approvals and site alerts. You can change this at any time in Settings.
>
> [Turn on] [Not now]

**If the answer is no**

> Everything still works. Open the app to check for changes.

Android 13 and later needs `POST_NOTIFICATIONS`. iOS has no usage string for notifications; the
app screen above is the only explanation a person gets.

Notification text shown on a locked phone carries no door names, site names or people's names
beyond the person's own shift. A door alert on the lock screen reads "Site alert. Open the app to
view."

## Face ID and fingerprint

Not in the A0 list, but iOS will not allow Face ID without a usage string, and rules 7 and 8 in
`CLAUDE.md` depend on it. Needed from A3.

**Phone prompt (iOS `NSFaceIDUsageDescription`)**

> Face ID confirms it is you before the app shows your door pass or sends a door command.

**If the phone has no biometrics or the person declines**

> Use your phone passcode instead.

## Camera

The phone app already carries this wording (`pulsar-rostering/apps/mobile/app.json`):

> The camera is used to add photos to incident reports you write.

> Photos you choose are attached to incident reports you write.

Incident reports are switched off in the phone app today because the server has no API for them.
If they stay off at first release, leave the camera permission out of the build; both stores
question a permission the app never uses.

The rotating door pass in A3 is shown by the phone and read by the door reader, so the Access
module does not need the camera for it.

## Store listings

Both stores ask what data the app collects. Fill these in from the same facts as the text above:

| Data | Collected | Linked to the person | Used for tracking |
|---|---|---|---|
| Precise location | At clock-in and clock-out only | Yes | No |
| Name, work email | Yes, from sign-in | Yes | No |
| Device identifier for notifications | Yes | Yes | No |
| Photos or video | Depends on the camera decision above | — | No |
