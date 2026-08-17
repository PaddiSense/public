# PaddiSense Weather — What's New

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
