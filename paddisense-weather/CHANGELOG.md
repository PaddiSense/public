# PaddiSense Weather — What's New

## 2026.9.7

**Internal type-checking fixes only. This is the version that brings you the 2026.9.2 → 2026.9.6 security hardening below; nothing you use day to day moves.**

## 2026.9.6

**Security hardening, rolled up from 2026.9.2 → 2026.9.6. Nothing you use day to day moves.**

- Login is protected against password-guessing from a single source, not just against one
  username at a time.
- Changing a burn-safety rule, your station settings or your Ecowitt cloud keys now requires a
  user with the right level of access. Viewing is unchanged.
- The settings page no longer sends your Ecowitt cloud keys or licence details to the browser.
- If Home Assistant restarts while Weather is asking it for your farm's location, Weather now
  waits instead of recording a wrong location and wrong forecasts.
- Every response from Weather, including the login redirect, now carries the browser security
  headers that protect against framing and content-sniffing.

## 2026.8.25

**Internal test corrections only — nothing on your box changes.**

The previous update changed how the add-on reports a failure to reach your paddock
boundaries, and three of our own tests were still checking for the old behaviour. We
corrected the tests. There is no change to Weather itself in this version.


## 2026.8.24

**Paddock outlines were missing from the radar map, and the page did not tell you
anything was wrong.**

The radar asks another add-on on your box for your paddock boundaries. That request had
been failing — but the page could not tell the difference between *"this farm has no
paddocks"* and *"nobody answered"*, so it simply drew an empty map and said nothing.

Two things are fixed. Weather now finds the other add-on reliably, instead of relying on
an internal address that changes whenever an add-on is re-installed. And when it genuinely
cannot reach it, the page now reports that as an error rather than showing you a blank map.

If your paddock outlines have been missing from the radar, this is why, and this update
should bring them back.


## 2026.8.23

**Weather could reveal a person's live location to someone who had not signed in.
Please update.**

The radar has a "My Location" button, and the address behind it was deliberately reachable
without signing in — it has to be, so the button works inside the Home Assistant app, where
the browser will not share your position.

The mistake was in what it did when nobody was signed in. Instead of refusing, it looked
through every person and device your Home Assistant knows about, picked the first one with
a position, and returned that person's live GPS coordinates **along with their name**. On a
farm that could be a worker or a family member.

It now refuses that request unless you are signed in. If you are signed in, nothing changes
— you still get your own position exactly as before.

**How exposed were you?** This was reachable from your own box and local network, not from
the open internet by default. We are telling you plainly because it involved a named
person's location, which we treat as your private information regardless of how narrow the
opening was.

**What you should do:** update Weather to this version or later.


## 2026.8.22

**A brand-new box could not start Weather. Fixed.**

If you installed Weather on a **new** box, it would not start — it was waiting for a database
password that the add-on is supposed to work out for itself. Existing boxes were never affected:
yours has been running normally throughout, and nothing about your data or settings changes.

This only mattered on a first install, which is exactly what makes it worth fixing now.


## 2026.8.21

**The Seasonal Outlook has been removed.**

We told you in the last update that it was working. It wasn't. The section
appeared, but every temperature and rainfall figure in it showed as "--" —
the part that fetched the outlook and the part that displayed it never
agreed on how to label the numbers, so nothing real ever reached the screen.

Rather than leave a section that looks like information but isn't, we have
taken it out. The 7-day and extended forecasts are unchanged, and so is
everything on My Stations.

Nothing else about the page has changed.

## 2026.8.17

**The Weather page is now two pages.** It had grown crowded, with your own
sensors and the forecast competing for the same screen.

- **Forecast** — the 7-day and extended outlook, the Home / Follow Me buttons and
  the town search, and now a **Seasonal Outlook** covering the months ahead.
- **My Stations** — everything coming from your own weather stations: live
  readings, rainfall, wind rose and daily ET0.

On a phone these are two tiles on the home screen; on a computer they are two
entries in the menu.

**Seasonal Outlook is now working.** The section existed but had never had any
data behind it, so it never appeared. It now shows a week-by-week temperature and
rainfall outlook for the months ahead.

**Text on the forecast tiles is now white**, so the dates and temperatures read clearly against their coloured backgrounds.

**If you have no weather station**, the My Stations page is simply not shown, and
your forecast page continues to use Open-Meteo for current conditions and rain —
including the daily ET0 figure, which stays available either way.

## 2026.8.14

**Choose the location your forecast comes from.** On the Weather page, just under the
7-Day Forecast heading, there are now two buttons — **Home** and **Follow Me** — and a
search box. Home uses your farm's coordinates, Follow Me uses your device's location,
and the search box lets you type a place ("Indianapolis USA") and pin it. The 7-day
tiles, the extended days and the conditions banner all follow your choice.

Your farm's own data never moves. Station readings, rainfall history and the daily ET0
figures are always your farm's, whatever the forecast is set to, and the station cards
and rain panel below always report your own weather stations.

The choice is remembered on that device only — setting your phone to another town does
not change what anyone else sees on the farm.

**Burn Forecast and Spray** also gained a Home / Follow Me choice, so you can see which
location a rating was built from.

**Fixed: "Today's Burn Window" could show the wrong day.** Before about 10–11 am the burn
window was calculated against the previous day's hours. Times on the Burn Forecast and
Spray pages are now always correct for the location shown — including when you are away
from the farm, where the hours could previously be out by several hours or a whole day.

**Weather page banner** now shows Temperature, Humidity, Wind and **Wind Direction**.
Delta-T has moved to the Spray page, where the full spray assessment already lives.

## 2026.8.13

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are
with a cryptographic token before they can change this add-on's licence or permissions.
Previously being on the box's internal network was treated as sufficient proof.

## 2026.8.12

- A newly installed add-on now stays on its activation screen until you enter your licence.
  Nothing changes for an add-on you are already using: once it has been activated it keeps
  working, and a later licence change or renewal will not lock you out of your own data.
