# PaddiSense Safety — What's New

## 2026.10.20

**A network hiccup inside the box can no longer lock you out.** If the box briefly could not look up Home Assistant's address, the add-on
stopped trusting it and sent everyone to the login page until the lookup worked again. It now keeps the last address that worked.

## 2026.10.19

**The worker board works without the internet.** The board used to fetch its map tool from an outside website every time it opened;
if that site could not be reached — the farm's internet down, a phone on Wi-Fi with no data — the board stayed on "Loading…" and
showed no workers. Now the workers and their states always load first, and PaddiSense carries the map tool itself. If the map
cannot start, its box says "Map unavailable" and everything else works. (The map's background imagery still needs the internet.)

## 2026.10.18

**The worker board now shows "Connection Lost".** If a worker's phone stops reporting for more than 15 minutes, their tile on the
board and on the kiosk now says **Connection Lost — Last seen 20m ago**. Until now the desktop board and the kiosk never showed it
(the alert to your phone was working; the board was not). The phone board shows it too, for the first time.

**A worker PaddiSense cannot locate is never shown as OK.** A checked-in worker whose phone has sent no readable location reads
**Signal Unknown**; a worker between zones with no position reads **Unknown — Not at known location**.

**Time on site and "minutes left" on a pause** show again on the board and kiosk.

**Notification group buttons** (Edit · Test · Delete) fill their row on a phone instead of standing tall and narrow.

## 2026.10.17

**A security fix in how logs are cleaned.** One specially shaped request could make the add-on stall while it tidied a log line. The
shared log-cleaning code is now bounded, so it cannot. Nothing changes in how you use the add-on.

## 2026.10.16

**Safety now uses the fleet's one theme.** Buttons, popups and notes look and size the same as in every other PaddiSense add-on. On
a phone the buttons are the standard 105 px with readable 16 px text (some were tall with tiny 12 px text), and a popup holds the
page behind it still. The worker status tiles and the I NEED HELP, tracking and pause controls are unchanged.

## 2026.10.15

**Told when a worker's phone goes quiet.** If a worker on shift has tracking turned on and their phone stops sending its location for
15 minutes, even though Safety asked for it, the primary contact gets one alert: "No location from <worker>". Before, Safety paused
that worker's safety check without telling anyone.

**Manager Mode follows your access.** The Manager Mode button now appears only for people Core gives Manager or Admin access. The PIN
is still asked for on a shared phone.

## 2026.10.14

**Alerts follow the person, not the phone.** In Notifications and in Config you can now pick a person from Home Assistant. Safety
alerts reach every phone that person has, as Home Assistant names it at the time. Renaming a phone or getting a new one no longer
stops safety alerts. Phones you picked before are moved to their owner automatically, a few minutes after the add-on starts.

**No more failing retries.** An alert is no longer sent again and again to a phone Home Assistant has removed.

## 2026.10.13

**Opens reliably from Home Assistant.** A brief network hiccup on the box could stop this add-on opening from the Home Assistant
sidebar for up to five minutes. It now recovers within seconds.

**Security updates.** The system software underneath this add-on is refreshed with three months of security fixes.

## 2026.10.12

Workers’ phones are no longer pinged for their location overnight or when they are not checked in. Safety alerts are unchanged.

## 2026.10.11

**Access follows Core.** What a person can change here now matches the role you gave them on Core's access page. An Operator can no longer use manager-only actions. A box with no access set up keeps full rights.

## 2026.10.10

**Security.** On your farm, PaddiSense trusts only the licence key it was built with. Another add-on on the same box can no longer add one.

## 2026.10.9

**The phone top bar matches the other PaddiSense apps.** MAIN (or Home) and the page title stay at the top while you scroll, and the
page number now sits in the bar.

## 2026.10.8

**Pages always show the latest version.** After an update, your browser could keep showing the old Safety screens until you cleared its
cache. Safety now tells the browser to fetch each page fresh.

## 2026.10.7

Logs now hide one more kind of secret (GSM connection codes).

## 2026.10.6

If a phone stops receiving Safety alerts, Home Assistant now shows a notice saying which phone and why, so it can be fixed.

## 2026.10.5

On your phone, Worker Safety has a MAIN button that takes you back to the PaddiSense start page, and the Notifications and Config pages have a Home button.

## 2026.10.4

Buttons and tiles are a consistent, easier-to-tap size on phones.

## 2026.10.3

Buttons and filters fit phones better.

## 2026.10.2

Buttons are bigger on phones and tablets so they are easier to press.

## 2026.10.1

On an iPad or an Android tablet you now get the full desktop pages instead of the phone layout. Phones are unchanged.

## 2026.9.10

**New PaddiSense colours, and easier to read at a glance.** Safety now uses the new light grey
PaddiSense look on every screen. Worker tiles and map pins show white writing on their red, orange,
green and blue, and workers who are off site or away now show as a light grey tile instead of black.
The wall display (kiosk) shows its status colours correctly again.

## 2026.9.9

**Security update.** A third-party networking library bundled with Safety was updated to close two
published vulnerabilities. Nothing you do changes; the update is inside the add-on.

## 2026.9.8

**Easier to use in a small window.** Rows of buttons and fields — the admin PIN, working hours,
worker settings and the group actions — now flow onto a second line instead of being squashed when
the browser window is made narrow.

## 2026.9.7

**Easier to read.** Buttons, the workday selector and cards now use the new PaddiSense light theme properly — white text on coloured buttons, dark text on every card.

## 2026.9.6

**Behind-the-scenes code checks tightened.** Nothing changes in how you use Safety.

## 2026.9.5

**Check-in, check-out and pause always tell you if they didn't work.** If a worker's check-in, check-out, pause or
resume was refused (for example an expired sign-in), the screen used to say it was done anyway. It now says the change
was not saved and why, and shows the worker's real status.

## 2026.9.4

**Settings are checked before they are saved.** A badly formed settings change could previously be saved and stop
the Safety status page from loading. Safety now rejects it with a clear message and keeps your existing settings.
Nothing changes in how you use Safety.

## 2026.9.3

**Security fixes for the Safety map and paddock sync.** A zone or paddock name could carry hidden code that ran
when you hovered over it on the map; names are now always shown as plain text. Safety also looked for your Farm
add-on too loosely and could have sent its access key to a look-alike add-on; it now only talks to the real Farm
and Core add-ons. Your licence details are now stored encrypted. Nothing changes in how you use Safety.

This release also includes 2026.9.2, below, which had not reached growers yet.

## 2026.9.2

**Maintenance roll-up since 2026.9.1. Nothing you use day to day moves unless a line above says so.**


## 2026.9.1

- **Security: saving device preferences now requires you to be signed in.** That page previously
  accepted the request without a session. Nothing changes for normal use.
- **Security: the browser-protection headers now also arrive on sign-in redirects and refused
  requests**, not only on pages you are signed into. No change for normal use.
- **Security: a worker's notification target can now only be a phone notification service.**
  Previously a Safety manager could type any Home Assistant service name (or a path) into that
  field, and the add-on would call it with its own credentials. Now only `notify.…` services are
  accepted and sent. If a worker's notifications stop after this update, re-select the phone
  from the list on their user record.
- Includes the 2026.8.19 fresh-install fix below, which had not yet reached the store.

## 2026.8.19

- Fixed: a brand-new installation could fail to start with a configuration error, even when
  correctly set up. Existing installations were unaffected.

## 2026.8.18

**New installs: your first admin password is now recoverable.** On a brand-new install the add-on
creates an admin account with a randomly generated password. Previously that password was not
retrievable by anyone — a genuinely fresh install could not be signed into. It is now written to a
protected file inside the add-on (`/data/.admin_initial_pw`) for you to read once, sign in with,
and change. **Existing installs are unaffected** — your current login still works.

**Every page now tells you if the box is not connected to PaddiSense.** A small, dismissable
note. It never blocks you or locks any page — it is there so a box that has quietly dropped its
connection does not look perfectly normal.

**Security: the factory database password is gone from the last two places it remained.** The
add-on now refuses to start with a blank credential rather than falling back to a known default.
No action needed on your part.

## 2026.8.17

**Faster start-up.** Removed duplicate code checks from add-on start — they already run in the build pipeline.

## 2026.8.16

**Security update — installs a safer database configuration.** This add-on no longer ships with
a factory database password; it now uses its own dedicated, locked-down database account that is
set up automatically. No action needed on your part. Also includes internal reliability fixes to
the add-on's startup checks.

## 2026.8.15

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are with
a cryptographic token before they can change this add-on's licence or permissions. Previously,
being on the box's internal network was treated as sufficient proof.

## 2026.8.14

- A newly installed add-on now stays on its activation screen until you enter your licence.
  Nothing changes for an add-on you are already using: once it has been activated it keeps
  working, and a later licence change or renewal will not lock you out of your own data.
