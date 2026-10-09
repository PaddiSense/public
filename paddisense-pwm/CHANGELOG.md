# PaddiSense PWM — What's New

## 2026.10.52

Door buttons are clearer: both drain doors say "Drain", and the first bay's doors say "B-01 Supply". On a laptop the Paddocks page now scrolls as a whole page, so the map no longer squeezes the buttons into a small box. Safety: a pump will not start (or keep running) while its depth sensor loop is dead — use "Override Low Supply protection" on the pump card to run it anyway. Pump boards need a reflash for this. Includes everything in 2026.10.51.

## 2026.10.51

A depth sensor set below field level (for example in the furrow) now reads below zero again, so you see water coming before it covers the bay. Boards need re-flashing to pick this up. The +/- buttons are the same wide row on every page and phone. Includes everything in 2026.10.50.

## 2026.10.50

If you have more than one farm with a paddock of the same name (say "Blk 2" on two farms), PWM now keeps them as separate paddocks and shows the farm in front of the name everywhere ("7829 · Blk 2"). A paddock that may have been mixed up before asks you on Paddock Setup which farm it belongs to; its bays and gates stay as they are. Single-farm growers see no change. Includes everything in 2026.10.49.

## 2026.10.49

The paddock map no longer shows a working sensor board as "offline": it checks the right board, and shows "--" when it cannot tell instead of guessing. A dry bay's steady 0 cm reading stays live. After you re-zero a depth sensor, the device card now says the board needs flashing, and your new zero is kept when you next save the board. Pop-up forms (like editing a gate) now fit small laptop screens and scroll. Includes everything in 2026.10.48.

## 2026.10.48

Security: each person now gets the PWM rights set for them on the Core Access page, for every action, not only for which buttons they see.

## 2026.10.47

Security: licence checks are stricter about which signing keys they trust. Includes everything in 2026.10.46.

## 2026.10.46

Paddock setup is built in one place: the gate cards. Each gate says which bays it serves, where its water comes from (now including "Not automated" for a channel PWM does not run) and which bay its sensor reads. The bay card simply shows what the gates set up — its order, where its water comes from and goes, and which board reads its depth. If an older setting on a bay disagreed with its gate, the bay card says so and lets you settle it.

Depth sensors: an empty bay no longer shows LOOP FAULT. A sensor is only flagged when its signal is truly dead, and a depth below zero now reads 0 cm instead of a negative number. Reflash each board in ESPHome to get this.

## 2026.10.45

Each actuator now has a Forward / Reverse direction in Device Setup. If an actuator runs backwards (Open closes it), set it to Reverse, save, and flash the board — no re-wiring. Then run one full Close and check Open and Close with the Test buttons. Also: a door commanded fully open now stops at its set travel time, so a travel set short of the full stroke is never over-run (the manual switches can still go further when you are fault-finding).

## 2026.10.44

Far fewer alerts: a sensor that drops out sends one alert (and one "back online"), not one an hour, and only while that bay is running. Alerts go only to the people in your notification groups — nobody else in Home Assistant — and every kind of alert can be chosen per group. Groups now list people, not phones: all of a person's phones get it, and tapping an alert opens the right PWM page. New System ON/OFF switch on the Notifications page turns off every alert and all automation in one go. PWM will not arm Flush, Pond, gate Auto or Auto Demand while a sensor it needs is not working.

## 2026.10.43

Every +/− adjuster is one tidy line. In Device Setup each sensor has its own card with its settings and its live offset together, and a board with one sensor shows one adjustment.

## 2026.10.42

Safety: a pump timer now only says a pump stopped when the board confirms it (and warns loudly when it did not); a scheduled start that was missed while the system was offline is reported, not started hours late; overflow protection is always on once set up; every door, gate and switch command reports whether it actually worked.

## 2026.10.41

Everything looks and works the same way on every page: one door button, one pump button (grey when off), AUTO / MANUAL,
"Save" or "Save to board", one button size. The Home bar stays at the top while you scroll. The Paddocks page shows All plus
your enabled paddocks. Sensor and water-balance alerts only come when something is running — overflow protection still alerts
in every mode.

## 2026.10.40

Device Setup shows one tile per thing on the board — Board, Actuators, Sensors, Relays, Pump — with everything for it in one place. Each board card is green when online and up to date, orange when offline, red when it needs flashing. Every +/− button is the same size.

## 2026.10.39

A bay drained only through its second door now shows its drain button.

## 2026.10.38

Phone and computer now show the same thing on every setup page. Each bay lists its own gates (a gate shared by two bays shows
in both). The drain button is back on the last bay. Auto Demand is one tap-to-toggle button everywhere. On the phone you can
open, stop or close a channel gate from the map, rename a channel and refresh from ESPHome; on the computer you can keep
channel notes and see a pump's Live Status.

## 2026.10.37

Pump Setup → Live Settings looks the same on phone and computer, and the ±5 buttons now add up (press +5 three times for 15 cm). The dry-run minimum is set there; Device Setup shows it.

## 2026.10.36

Capture dry zero works on phones and tablets again — it stopped on "Settling…".

## 2026.10.35

Sensor calibration shows a live countdown and tells you when the board is not answering, instead of sitting on "Settling…".

## 2026.10.34

Housekeeping only — no change you will see.

## 2026.10.33

What each person can do in PWM now follows their access in PaddiSense Core — an Operator no longer sees delete and setup
buttons meant for the farm owner. A channel gate's overflow level is set in one place, Channel Setup (the Channels page shows
it). The Notifications page is now W12.

## 2026.10.32

A bay's second door can have its own part-open position — hold its button on the paddock map, as for the first door.

## 2026.10.31

Logs now hide one more kind of secret (GSM connection codes).

## 2026.10.30

Notifications, Trace and Licence are one page on phone and desktop — the notification list shows who each group alerts again;
moving a map badge tells you if it did not save; a relay whose state is unknown can't be pressed.

## 2026.10.29

Adding a gate, a channel or a service item now works on phones and tablets; buttons are one size and colour everywhere;
buttons that can't work on a board are no longer shown; the channel page keeps your gate order on the phone too.

## 2026.10.28

Tidier and more consistent on phone and desktop: the same controls behave the same everywhere, buttons only appear where
they can work, a failed sensor shows LOOP FAULT on the channel page too, and you can add a channel from your phone.

## 2026.10.27

Safer and clearer: the pump's low-supply check before a start works again; a bay whose sensor has failed now shows SUSPECT or
LOOP FAULT instead of a number; the map, the automation page and the automation all agree on each bay's state and band; fewer
repeated alerts and log lines; the Beep button only appears on boards that have a beeper.

## 2026.10.26

The PWM home screen on your phone has a MAIN button at the top that takes you straight back to the PaddiSense start page.

## 2026.10.25

Buttons and tiles are a consistent, easier-to-tap size on phones.

## 2026.10.24

Safer pump stops, and every page now shows the same state for each board, door and pump. The Wi-Fi-loss setting is one
setting per board, changed on the gate or pump it controls. Map icons show their colour straight away, buttons are a
consistent size, and two-door rows are square on a phone.

## 2026.10.23

Setup tiles are all the same size, and a board's capacity (relays and inputs used and free) is now a clear table.

## 2026.10.22

Device Setup: tap a board and every job is one tile away — sensor calibration, raw data, outputs test, board info,
settings backup and more. Dry zero capture now shows clearly that it is working.

## 2026.10.21

A bay with a second door board can now show that board's water level on the map — turn it on per bay in the map's
Sensor Config (off by default). The bay's own level still comes from its drain board. A newly flashed board that has
not been added in Home Assistant now says so ("flashed — add in HA") instead of "not flashed".

## 2026.10.20

Device Setup is now one page on phone and desktop: tap a board to see its live readings and its six setup tiles, then
one job per tile. Gate calibration on the phone now has the typed travel time too. Diagnostics & Logs now sits below Notifications on the home page.

## 2026.10.19

Buttons and filters fit phones better.

## 2026.10.18

**Tidy-up**: removed two old pump settings that had no screen, and depth offsets are now only set on the board.

## 2026.10.17

**Sensor problems alert, they don't stop watering**: if a depth sensor stops reporting you get an alert, and PWM leaves
the doors and pumps as they are.
Buttons are bigger on phones and tablets so they are easier to press.

## 2026.10.16

**Safer sensor reading**: a reading PWM cannot date is now treated as out of date, never as fine.

## 2026.10.15

Behind the scenes: groundwork so every screen shows a door's position the same way the automation reads it.

## 2026.10.14

**Safer sensor watching**: if the depth reading from a bay's drain board stops, you now get a Sensor Offline alert and
the supply is closed while the bay is filling — before, this went unnoticed on the standard setup. A door that is part
open now counts as open when PWM checks where the water is going, so you won't get a false BLOW OUT RISK.

## 2026.10.13

**Shorter, clearer alerts**: ABOVE MAX, BACK BELOW MAX, BAY STARVED, FIRST FILL STALLED, BLOW OUT RISK and NO FLOW
DETECTED — the title says what happened, the message says which bay. **Close supply** now closes only the paddock's
own supply, not the doors between bays. In Pond a bay's second door stays shut. Two actuators on one gate move together.

## 2026.10.12

**Clearing a door by hand**: when you move a bay door yourself (on the map, the device page or the switch on the board),
the automation leaves that door and its partner door alone for 10 minutes, then puts them back where they should be.
**Map rows line up**: the Flush / Pond / Off button is the same width on every row of a paddock.

## 2026.10.11

**Pond response times per bay**: on the map's settings panel, **Sensor Config** (was Sensor Calibration) now lets you
set for each bay how long the water must stay below min before the supply opens, how long above min before it closes,
and the starvation time. Raise them if waves or a water bulge cause false triggers. **Two-door bays** show the door
number above the button name.

## 2026.10.10

**Second doors on the map**: a bay with a second supply or drain door now shows a second button beside the first
(marked ②), so you can open and close it by hand. On a phone, when a bay row also has its Flush / Pond / Off button,
the mode shows as F / P / OFF to leave room for the names.

## 2026.10.9

**Water Chain**: a gate or bay you set up while the Water Chain page is open now appears in its "+ place…" list
as soon as you press Edit — no page reload needed.

## 2026.10.8

**Ganged gates on the map**: tapping a door on a board whose two actuators are ganged now moves both of them, not just
the first.

## 2026.10.7

**Support logs**: when PWM finds a stored setting it does not recognise, the log now names exactly which one, so support
can find it quickly. Nothing on your farm changes.

## 2026.10.6

**Bays with two doors**: a bay's second supply or drain door now moves with its first door in Flush, and closes with it
in Pond. A door that joins two bays is driven by the bay it supplies, so "zig-zag" layouts work without the doors
fighting.

**Water from another paddock**: a paddock's first bay can be fed from another paddock's drain. That drain only opens
while the bay it feeds is taking water.

**Easier setup**:
- "Water comes from" says why a bay cannot be chosen, and shows the bay you wired.
- A channel can be described before its boards are fitted.
- A water chain card can have as many arrows as fit.

**Pump auto-stop**: turn it on and off on the Pumps page. Pump Setup chooses what it watches, and the mobile Demand
Control section has its own Save.

**Fixes**:
- An offline channel gate can no longer be tapped.
- The phone's dry-zero capture is tidy and shows when it is busy.
- Pages no longer turn dark with black text on phones in dark mode.
- Tablets get the full desktop pages.


## 2026.10.5

**Only your live bays are watered** — a bay you have hidden or merged away in Farm is no longer picked up by PWM.

## 2026.10.4

**Switching off is immediate and final** — any gate command that was already on its way when you pressed Off is dropped.

**A bay above its maximum gets no more water** — its supply gate closes while the drain opens.

**Pond timing is cleaner**: a bay is either above or below its minimum, and only the time it stays there counts.

**Faster safety response** — overflow protection acts on every channel at once.

**Easier to read and use**: Pond has its own teal colour; gate buttons show an estimated % while moving; "When switched
Off" is in each paddock's settings; on the Devices page, Test & calibrate is inside each board, the list lines up, and
the phone can capture a sensor's dry zero.

## 2026.10.3

**Pond fills from the bottom up.** When Pond starts, water runs to the bottom bay; each bay, once it has held above its
minimum for 15 minutes, closes its own supply so the bay above fills next. When every bay is covered, normal Pond takes
over.

**Steadier Pond.** A bay must hold above minimum for 15 minutes to count as filled, below minimum for 30 minutes before
it calls for water, and above maximum for 2 minutes before the drain opens (a level more than 5 cm over maximum opens
it straight away).

**Switching Pond or Flush off stops everything** — gates still moving stop where they are, and the automation sends
no further commands.

**New alerts** for a bay that drops fast with its gates shut (possible breach or leak), rises with its gates shut, or
rises without the bay above it falling.

**Flush and Pond timers count down live** in the paddock settings panel. On the Devices page you can type an actuator's
travel time directly.

## 2026.10.2

**Diagnostics & Logs is in the side menu.** It shows every command PWM sent and every automation change, with the
reason. Gate positions shown there now always match the gate itself, within a minute.

## 2026.10.1

**Pond fills the paddock from the bottom first.** When Pond is switched on, the bottom drain closes and the gates
between bays open, so water runs through to the bottom bay and fills upward. Once every bay has reached its minimum,
normal Pond takes over and the 12-hour check starts. A bay at its maximum always drains. If the first fill has not
finished after 12 hours you get one alert naming the bays still short.

**Switching Pond off stops it straight away** — no further gate moves.

**A gate stopped part-way is no longer treated as open**, so Pond will finish opening it.

## 2026.9.173

**Pond: a bay whose level cannot be read no longer upsets the rest of the paddock.** Only the gates touching that bay
are left as they are; every other gate is decided as normal.

## 2026.9.172

From the bench walk:
- **Gates are only reported as moved once the gate's board confirms it.** A gate on a board that has lost power or WiFi
  now shows "not confirmed" straight away instead of "closing". Its button reads **OFFLINE** while the board is
  disconnected, and **HOLD** when a gate stops part-way.
- **Automation Failure** alert when a paddock's inlet board does not respond during a flush.
- **Pond:** the paddock inlet closes when the supply channel is below the top bay (no backflow); a bay that is below
  its minimum when Pond starts opens its supply straight away after the arm window.
- The Flush / Pond arm window is now **1 minute** (was 2).
- Turning off a paddock's individual bay control makes every bay follow the paddock's mode.
- A **Diagnostics** tile on the home page: every command PWM sent and every automation change, with the reason.
- Closed gates are shown in a clear red.

## 2026.9.171

Overflow alerts are short: **OVERFLOW — MC-01 Above Safe Level**, then **MC-01 Above Safe Level > 10 mins** (every
10 minutes while it stays high) and **MC-01 Back Below Safe Level**.

## 2026.9.170

**Overflow keeps telling you while it is still high.** If a channel stays above its emergency level, PWM now sends a
reminder every 10 minutes saying the relief is not bringing it down, and one message when it drops back below.

## 2026.9.169

A pump in an unknown state shows the amber "check it" colour instead of the running colour.

## 2026.9.168

After a stop the pump board did not confirm, the pump stays **UNKNOWN — STOP** (press it again to retry) until the
board itself reports in, instead of going back to showing RUNNING from an old reading.

## 2026.9.167

**The pump card says when PWM cannot be sure.** After a start or stop the pump board did not confirm, the card reads
**UNKNOWN STATE — CONFIRM DEVICE** until the board reports again. An idle pump on a connected board is no longer
treated as unknown just because it has been quiet.

## 2026.9.166

**Safety fix — a pump stop the board did not confirm is no longer shown as sent.** The button now reads
**Not stopped — No response from Pump 1 — it may still be running**.

## 2026.9.165

Behind the scenes: unused code removed.

## 2026.9.164

A pump that does not answer a start now says so in plain words on its button: **Not started — No response from Pump 1**.

## 2026.9.163

**A pump start that was refused now reads clearly on its button.** The reason wraps inside the button in normal text
instead of running off the card. A start you stop within 30 seconds no longer gets checked as if it had failed.

## 2026.9.162

**Safety fix — a pump start or stop is only reported once the pump board confirms it.** If a board has just lost power
or WiFi, Home Assistant can take a couple of minutes to notice, and until now a start in that window said "Command sent"
while nothing happened. PWM now waits a few seconds for the board itself to report the pump on (or off); if it does not,
you are told straight away that nothing started — and a stop the board did not confirm is flagged as "may still be
running" instead of being shown as stopped.

## 2026.9.161

**Diagnostics now shows what PWM did and why.** W11 Diagnostics lists every command PWM sent to a board (and whether the
board accepted it) and every change in what the automation is doing, newest first, with the reason.

## 2026.9.160

Behind the scenes: error messages shown on screen are now only the ones written for you; anything unexpected is logged
for support instead of being shown.

## 2026.9.159

Behind the scenes: PWM now keeps a record of every change in automatic pump demand and every valve movement a board
reports, so "why did that happen?" has an answer with the time and the reason.

## 2026.9.158

**Safety fix — Pond on a whole paddock.** Switching a whole paddock to Pond now gives the same 2-minute window to change
your mind as switching one bay, and a paddock going back into Pond starts its timers fresh instead of acting straight away
on old readings from its last run.

## 2026.9.157

**One overflow alert, not one every 30 seconds.** While a channel stays above its emergency level, PWM keeps its relief gate
open and its actions in force, but now sends the overflow alert once when it happens instead of repeating it.

## 2026.9.156

**Pump start that did not happen now says so straight away.** If a pump's board does not accept a start (for example it is
offline), PWM now tells you immediately that nothing was started, instead of reporting success and alerting you 30 seconds
later. PWM also keeps track of a pump started or stopped at its own switch.

## 2026.9.155

**Flush tells the truth about the inlet.** If the paddock inlet does not open (the board is offline or refuses), Flush now
waits and tries again instead of announcing "Flush started". If the supply channel level cannot be read, the waiting
message now says so instead of saying the water is not high enough yet.

## 2026.9.154

Behind the scenes: every setting PWM saves is now checked before it is stored, and a setting that is not valid is refused
with the name of the field that is wrong, instead of being saved and causing trouble later.

## 2026.9.153

**Safety fix — overflow protection.** If you chose a channel gate's emergency depth sensor on the **Channels** page, overflow
protection could not see that sensor and would not have opened the gate. PWM now repairs that setting by itself within a
few minutes of updating, and a gate whose overflow sensor cannot be read is now shown as a fault instead of looking fine.
Also fixed: choosing a gate's depth sensor on the Channels page could erase that gate's automation settings.

## 2026.9.152

**The automation now runs on its own.** Water control no longer shares its time with the screens you open, so a slow page
can never delay a pump or gate decision.

## 2026.9.151

**Every command is written down.** PWM now keeps a permanent record of every instruction it sends to a pump, gate or valve —
who or what asked, why, what the water levels were, and whether the board accepted it — so "why did my pump stop?" always
has an answer.

## 2026.9.150

Behind the scenes: PWM now tells PaddiSense support whether its automation is actually running and whether your gates and
pumps accepted their last command, so a stalled farm is noticed in minutes rather than when someone looks.

## 2026.9.149

**Syncing from Farm is now up to you.** PWM no longer pulls changes from Farm on its own — press **Sync now** on Paddock
Setup, which tells you how many Farm changes are waiting. If Farm removes a paddock you have switched on (or a bay in it),
PWM keeps it running and lists it for you to **Confirm remove** — and won't remove it while it is flushing or ponding.

## 2026.9.148

**Automation on a phone:** tapping a gate opens its settings again (it had stopped showing anything). Gate position and
overflow protection are set there; a board's actuators are set on the Devices page.

## 2026.9.147

**Devices page:** a board's gate controls now find their valves through Home Assistant's own device list, the same way the
depth readings already do, so a renamed board no longer shows controls that cannot reach it.

## 2026.9.146

**Updates wait for the water.** An update will no longer restart PWM while a gate is moving, a pump is running or a flush is
in progress — it installs once that finishes. Ponding does not hold an update back, and neither does a board that is offline.

## 2026.9.145

**Channel Setup on a phone** now works like Pump Setup: pick a channel, pick a gate, then one tile per setting — and a phone can
now set what happens when a channel overflows (stop a pump, close a gate, send an alert) and see the board's No-WiFi behaviour.
**Pump card:** water can be taken off the season total as well as added. **Paddock Setup:** gates are listed in the order the
water reaches them. The home page shows the version number.

## 2026.9.144

**Pump protection:** the Low-Supply check now uses exactly the setting on the Pump Setup page — 0 really is off, and the
board's Override is respected. The pump card says ON, OFF or OVERRIDDEN in words.
**Pump card:** add water to the season total directly, see the live pit level while adjusting the sensor offset, and the
shutdown and schedule settings are two separate cards. Pump cards on phones no longer sit inside each other.
**Gates:** renaming a gate no longer shows a false "not saved" error, and gates that share a position show #1 / #2.
**Map:** pumps and gates are one clear circle with the depth inside (blue on, grey off); depth numbers are easier to read;
the supply channel badge matches the bay badges and stays with its paddock.
**Setup pages:** open straight onto their tiles; bays come only from Farm; the channel gate settings say where each depth
comes from and warn when emergency opening is off. The Diagnostics page works again. Pop-up windows no longer let the page behind them scroll.

## 2026.9.143

**The "Sync from Farm" button on the Paddock Setup page works again** — it had stopped responding on desktop.

## 2026.9.142

**Automations page:** every Flush and Pond setting is here now, including each bay's minimum, maximum and flush hold.
**Paddock map:** the supply board's channel depth can be moved, renamed and tapped for its last 6 hours.
**Behind the scenes:** a bay can no longer be marked as flushing while it is in Pond or Off, and the water balance no longer
raises false "no flow" alarms on a channel that is draining through an open gate.

## 2026.9.141

**Pond:** Pond now opens and closes the bay doors as designed. Before this it set its clocks and then did nothing.
**Turning a bay Off** no longer moves any door; they stay where they are. Each paddock can choose otherwise under
Automations → the paddock panel → *When switched Off*.
**Flush:** a bay that has finished goes Off by itself while the next bay carries on, and its timer shows 0 and DONE.
Stopping a flush by turning the bays Off means the next flush starts from the beginning.
**Automations page:** each paddock now has its flush settings, a live countdown of what it is waiting for, and a Stop
& reset button.
**Paddock map:** a small countdown circle under each flushing bay, and the supply board's channel depth.
**Pumps:** the last stop says why. On a phone, the pump card is tidier and Auto Demand is one button.
**Channels page:** remembers which channel you had open.

## 2026.9.140

**Flush:** if you stop a flush part-way by turning the bays Off, the next flush starts from the beginning. Before this,
it could carry on from where the old one stopped, and the paddock inlet might not open.

## 2026.9.139

**Flush:** each bay now holds water for its full flush time. Before this, the hold finished early (a 30-minute hold
drained after about 8 minutes).
**Paddock map:** bay gate buttons now show OPENING / CLOSING and then OPEN or CLOSED, instead of staying on the old state.

## 2026.9.138

**Pump Setup:** saving no longer hides the other tiles until you reload, and it no longer asks you to confirm a safety setting
you did not change.

## 2026.9.137

**Pump Setup:** no more false "Settings changed — flash required" on pumps built in Device Setup. Saving a pump no longer loses
settings the page did not show.

## 2026.9.136

**Water Chain:** when a box already has an arrow coming in at the top, the next arrow comes in at a side, whichever is shortest.

## 2026.9.135

**Water Chain:** pumps are green, channels and water are blue, bays are pink and gates are yellow, so two of a kind side by
side are easy to spot. A bay reads its depth from its drain board; you do not pick a sensor for it.

## 2026.9.134

**Water Chain:** you can rename the water boxes you add. The page also warns when two boxes measure the same water.

## 2026.9.133

**Easier setup pages.**
- **Paddock Setup:** open a paddock to see its gates, each once, saying what it does ("Water in to B-01",
  "Drains B-01 into B-02") and whether its board is there. Tap a gate to choose its board. A bay now has
  "Depth read by", so you can see which board measures it.
- **Paddock Control:** the paddock names are solid buttons, and the one you are on is dark.
- **Channels:** each gate sits in its own box, with Auto/Manual and Open/Close on one row and the depth
  in a clear box.

## 2026.9.132

Behind-the-scenes update to the test bench. Nothing changes on a farm's screens.

## 2026.9.131

**Water Chain arrows now run between the boxes, never across them.** Also:
- The bay list only shows paddocks that are switched on.
- A pump drawn with its own pit box now reads that pit.
- Closing a bay's own inlet gate stops water reaching that bay, even when the gate is not drawn.
- The page is better at spotting where your chain differs from how your automation is set up.

## 2026.9.130

**On the Water Chain, a depth sensor can stand for a channel, a bay or a pit.** Pick the sensor, then
say what it measures. Each channel or bay box shows which sensor reads it, and you can change it. If
your pick differs from the one your automation uses, the page tells you and changes nothing.

## 2026.9.129

**The Water Chain is now yours to draw, and it and the Automation page are open to everyone.**

- **Water Chain** is a grid five boxes wide. Put each pump, gate, channel, bay or pit in the box where
  you want it drawn, then say where each one's water goes. The arrows follow what you say. Nothing
  is guessed.
- **Import from current setup** fills an empty grid from what your gates and pumps already say.
  Then you move boxes wherever they sit on your farm.
- The chain **only watches**. It never moves a gate or starts a pump. If it disagrees with how your
  automation is set up, it tells you and changes nothing.
- **Automation** (the rules overview) is now available on every box.
- **An iPad now gets the full desktop pages**, including in the Home Assistant app.

## 2026.9.128

**Behind-the-scenes update: shared styling brought up to date, and a board-checking tool now says so when it has no boards to check.** Nothing changes on your screens.

## 2026.9.127

**Boards can be named per box, and two broken pages are fixed.**

- **New `box_prefix` setting** on the add-on's Configuration page. Set it to something short
  like `sw7` and new boards are created as `sw7-rb-01` instead of `rb-01`. That stops boards on
  different servers sharing a network name. **Leave it blank and nothing changes** — existing
  boards are never renamed, and never need re-flashing because of this.
- **Channel Operating page** was stuck on "Loading…" and never showed your channels. Fixed.
- **Device Setup on a phone** showed "FETCH ERROR" and no devices. Fixed — and it was never a
  fetch problem; the page was failing while drawing the list.
- **Pump Setup** no longer shows the Bench Testing and Notes panels.
- On the water chain, gates that sit side by side now branch in parallel instead of being drawn
  one after another, and a gate can point at the pump it drains into.
## 2026.9.126

**Gates now point at the pump they drain into, and the Water Chain page owns its own gaps.**

- On Paddock Setup, a single gate's **"water goes to" / "water comes from"** list no longer
  offers "Drainage Channel". Instead it offers **your pumps**. A gate that empties into a
  recycle pit names the pump that lifts water out of it — the pit's depth is already shown on
  that pump's card, because the pump's own sensor is sitting in it.
- On Channel Setup, **"This Gate Feeds"** can now name a **pump** as well as gates and bays.
- The **"Not connected yet"** panel has moved off Paddock Setup and onto the **Water Chain**
  page, next to the picture it completes. On a phone it stays where it was.

If you had a gate set to "Drainage Channel", it will ask you to pick the pump instead.
## 2026.9.125

**Fixes to the new Water Chain, from first use.**

- **The chart's panel now grows to fit the whole chart** instead of being a fixed-height box
  you had to scroll inside.
- **Your drainage channel appears again**, and the bay drain that empties into it now shows its
  arrow. Both were being hidden by a filter that asked which control board each item was on —
  a question a channel of water cannot answer.
- **Channel gates are no longer hidden** on the Bench Simulation page just because their board
  is not part of the rig. Both pages now show the same pumps and channels; only the bays
  differ, and the bench page shows just the paddock the rig is bound to.
- **A duplicated arrow is no longer drawn as a recycle loop.** Only a genuine loop — a lift
  pump returning water upstream — is drawn as one, dotted.
- **A pump is no longer shown being fed by the channel it fills.**
## 2026.9.124

**The Water Chain now reads top to bottom, and it shows what was missing.**

The chart has been reworked so water flows **down** the page, with side branches stepping out
sideways — instead of being laid out by what kind of thing each card was.

What you will see that you could not before:

- **Bay gates have their own cards.** A bay's supply and drain gates were never on this chart;
  now they are. A shared gate between two bays appears once, as the one structure it is.
- **Your pumps are connected.** A pump's delivery and its source were already configured, but
  the chart was looking at the wrong field, so pumps sat on their own with no arrows.
- **Channels and bays are now the arrows**, labelled with their name, rather than cards of
  their own. The chart's cards are now only the things you can actually open, close or start.
- **Where several flows meet** — drains emptying into a drainage channel, two gates feeding one
  spur — you get a labelled bar rather than a misleading single arrow.
- **A recycle loop is drawn as a loop**, dotted, up the side of the chart.
- **A bay's water level now sits on its drain gate's card**, named, and says so when that bay's
  automation is switched off.
## 2026.9.123

**The pump draw and delivery boxes added in the previous build have been removed.**

Where a pump takes water from and where it sends it will be defined through Channel Setup
instead, so those boxes have been taken off Pump Setup rather than leaving two places that
could disagree. Nothing you had configured elsewhere is affected.
## 2026.9.121

**A pump now says "I can't read the sensor" instead of "the sensor is fine".**

Your pump watches a water level and stops itself when the channel is full enough. The board
it runs on can also report that a depth probe has failed — a broken 4-20 mA loop still sends
a believable-looking number, so that report is the only way to know the reading is junk.

If that report couldn't be found — most often because the sensor had been renamed in Home
Assistant — PWM treated the silence as good news and carried on using the number. The pump's
level protection looked armed while it was reading a dead probe.

It now looks the sensor up properly instead of guessing its name, and when it genuinely
cannot tell, it says so in the log and flags the level as unreadable.

**Nothing stops your pump because of this.** It is a warning, not a shutdown — the pump is
never halted on a guess.
## 2026.9.120

**You can now record where a single gate's water comes from, or goes to.**

On the paddock setup map, opening a single gate now offers one extra choice. A supply gate asks
**where the water comes from**; a drain gate asks **where the water goes to**, and offers a
**Drainage Channel** option as well as your channel sections.

Dual gates are unchanged — they already describe both sides. Recording this does not change how
anything is controlled today; it is the setup the water flow diagram will read.

## 2026.9.119

**The gate settings popup has its background back.**

On the paddock setup map, clicking **Edit** on a gate in the right-hand list opened a settings box
with no panel behind it — the fields sat directly on the dimmed screen, which made them hard to
read and easy to mis-tap. The panel is back. Phone was unaffected.

## 2026.9.118

**A sensor reading PWM cannot date is no longer assumed to be current.**

PWM ignores readings that have gone quiet, so a dead sensor cannot be mistaken for a live one. Two
gaps in that check are now closed: it now asks when the device last *reported* (rather than when its
value last *changed*, which stands still while a reading holds steady), and a reading with a corrupt
timestamp is now treated as out of date instead of current.

## 2026.9.117

**Pump daily totals now roll over at local midnight, not at 10 am.**

PWM works out "today" from the box's local time. The add-on image was missing the timezone
database, so that lookup quietly fell back to UTC instead of failing — which in eastern Australia
means the pump day changed over at about 10 am, and the morning's pumping was counted against
yesterday.

The timezone database is now installed, and a test keeps it that way.

## 2026.9.116

**Renaming a board can no longer switch off a pump safety without telling you.**

Pump-watch and overflow rules remember which depth sensor they watch. They remembered it by the
sensor's Home Assistant name — so renaming the board left the rule pointing at nothing. It did not
show an error; it simply stopped acting, quietly.

Those rules now remember the board and channel instead, and re-find the sensor whenever it moves.
If the sensor genuinely cannot be found, the rule keeps what it had and logs it, rather than
quietly treating the gate as having no sensor.

## 2026.9.115

**A board used as a bay's water-level sensor no longer shows as "unassigned".**

A board does one job. If a board was set up as a bay's level sensor and nothing else, the device
picker still listed it as free — so it could be handed to a second job by mistake. It now correctly
shows as assigned.

## 2026.9.114

**Depth readings that showed "not reporting" on boards that were reporting fine.**

Your device cards look up each depth channel by asking Home Assistant which sensor belongs to that
board. PWM was asking with an internal short name instead of the sensor's real name, so the lookup
found nothing — and a channel it could not look up was drawn as **not reporting**, even while the
board was sending readings normally.

Checked against this system's own boards: **all 9 depth channels** were affected, and all 9 now
resolve and show their live value. This applies on phone and desktop alike.

## 2026.9.113

**A self-check that could not see one of your boards now says so, instead of reporting all clear.**

PWM has a built-in audit that walks every board and checks that each gate, sensor and relay it
declares is the one it is actually talking to. Run on this system today it found **no
mis-matches** on any board it could reach.

But it could not reach one board — a leftover from a device set up on 14 September that was never
flashed — and it was still finishing with an "all clear". A board the system cannot identify is the
one most likely to be wrong, so that is now reported as **not checked** rather than passing.

Nothing about your gates, pumps or sensors changed.

## 2026.9.112

**A pump reading that has gone quiet is no longer treated as a reading.**

If a pump board stops reporting, the system used to keep trusting the last thing it said — on this
box, two pump boards were being read as "stopped" from a reading **33 hours old**, and every safety
that depends on knowing whether a pump is running trusted it.

Now a reading that is older than the board's reporting window counts as "cannot tell", and the
safeties treat that as *possibly running* and act, with a loud note in the trace. Stopping a pump
that is already stopped costs nothing; not stopping one that is running is what this prevents.

## 2026.9.111

On the test bench, the water-balance checker now reads the same simulated levels the
controllers act on. It was reading the real boards instead, so it could disagree with the
irrigation logic about where the water was. No change on a farm.

## 2026.9.110

**"No flow" now always tells you why.**

Two cases where the simulator moved no water and said nothing: a gate on a board's *second*
ram that it could not identify, and a valve reading `unavailable` — which looked exactly
like a gate you had closed.

Both still stop the water, which is the safe choice. Both now name the valve and the
reason, and clear themselves as soon as the valve reads properly again. An ordinary closed
gate is still not reported — that is just a farm at rest.

## 2026.9.109

**The bench simulator now follows your farm.**

It used to keep its own fixed idea of the farm — one pump, two channels, exactly two bays
— and simulate that no matter what you had actually set up. Boards it had no slot for
moved no water at all, and a paddock with one bay, or five, was refused outright.

Now it reads your declared farm: every pump, channel, gate and bay, however many there
are, and each gate on whichever ram it is wired to.

A few things it will now tell you instead of sitting still:

* **"No water can move"** — if the chain between your bays has not been declared yet, it
  says so and names what needs declaring, rather than running and moving nothing.
* **Assumed sizes** are labelled. A bay is sized from its surveyed area in Farm; channels
  and pumps from length, width and depth you can enter. Anything falling back to a default
  is marked, because the size sets how fast a level moves.
* **Overflowing** vessels are reported.

## 2026.9.108

Groundwork so the bench simulator follows your farm instead of keeping its own copy of it.
Nothing changes in how the system behaves yet — the switchover is the next update.

## 2026.9.107

**The water chain now agrees with your gates.**

Two faults are fixed, both of which could make the system look like nothing was
happening when it was — or the reverse.

* **Gates on a board's second ram are now read correctly.** Where one board drives two
  gates, the second gate's flow was being judged by looking at the first gate's valve.
  That gate would report "no flow expected" for ever, and a genuine blockage on it could
  never raise an alert.
* **The chain diagram no longer shows water moving through a closed gate.** The arrows
  animated whenever the channel or bay above held water, without checking whether the gate
  between them was open. Flow now needs water above *and* an open gate.

If a gate's position cannot be read at all, its line is now drawn in a distinct style
rather than looking the same as a closed gate — "I can't see this valve" and "this valve
is shut" are different things, and only one of them needs you.

## 2026.9.106

- **Fixed: renaming a board no longer silently breaks its depth threshold.** PWM used to
  remember a sensor by its Home Assistant name, so renaming the board left the gate watching
  nothing — without any error. It now remembers the board and channel, and re-checks itself,
  so a rename repairs automatically.
- **Improved: the sensor list now shows your PaddiSense boards by default**, with a
  "Show other HA sensors" tick box if you need something else. Your existing settings were
  migrated for you — nothing to re-pick.

## 2026.9.105

- **🔴 Fixed: a pump's demand level could be judged against the wrong depth.** If a channel
  gate's stored depth offset was unreadable, PWM quietly ignored it and carried on as though
  the level was fine. It now reports "Check Sensor" instead — the pump is never stopped on a
  guess, but you are told the level cannot be trusted.
- **Fixed: the board identity report now says WHY it could not read a board** — no setup
  header, an unreadable file, or a damaged header — instead of calling all three
  "undeclared".

## 2026.9.104

- **Internal: removed an old way of finding a board's sensors** that could not survive the
  board being renamed. Nothing had used it for months; removing it stops it coming back.
- **Bench simulation now says when it identified a board by name** rather than by its
  registered hardware, so a mismatch is visible instead of silently driving the wrong board.

## 2026.9.103

- **Fixed: the Paddock Control map on a phone now shows its page label (W01.M).** Every other
  page showed one; this page did not, which made it the hardest page to report a problem on.

## 2026.9.102

- **Added: a bay now tells you which turn it is on during a flush.** A bay waiting for the
  one above it to finish says "WAITING FOR MY TURN", and changes to "MY TURN TO FILL UP" the
  moment it is its turn. Previously a waiting bay looked the same as a bay doing nothing.

## 2026.9.101

- **Improved: "where does this bay's water come from" now offers the bay above it.** The
  first bay in a paddock is fed from a channel, so it only lists channel gates; any later bay
  can also be fed by another bay in the same paddock. Choosing one sets up the shared gate
  between them for you — one gate that drains the bay above and supplies this one.
- If that bay has no drain gate yet, PWM now tells you instead of appearing to save.

## 2026.9.100

- **Fixed: the Channel Setup page on a phone ran to the screen edges** — it had no margins,
  so text sat hard against the sides.
- **Fixed: confirmation messages on the bench simulation page** appeared in the middle of the
  page instead of floating at the bottom, and never disappeared.
- **Fixed: form labels on the phone's automation page** ran into their input boxes.
- **Fixed: a long bay name overflowed its box** on the Water Chain diagram.

## 2026.9.99

- **Added: the last setup jobs that were desktop-only now work on a phone.** You can force a
  re-sync of the bays drawn in Farm, release a bay Farm no longer has, tell the water chain
  what feeds a channel or pump it cannot trace, and set the water-balance alarm.
- Every setup action available on a computer is now available on a phone.

## 2026.9.98

- **Fixed: the Remove button on a bay's device asked twice.** It was wired up twice, so every
  removal ran two confirmations and two removals. It now runs once, on the device and slot you
  actually chose.

## 2026.9.97

- **🔴 Fixed: removing a board from a bay on your phone removed it from EVERY bay it served.**
  The message said "remove from this bay", but the board was cleared from every bay it was
  assigned to, and its map position was lost. Where one gate serves two bays — a drain for one
  and the supply for the next — taking it off one bay silently disconnected the other. Removal
  now affects only the bay you are looking at, and says so.

## 2026.9.96

- **Added: you can place a new gate from your phone.** The bay screen's Gates section now has
  an "Add gate" button. The gate is placed at the centre of the bay and opens straight into its
  setup so you can choose the board and actuator while you are standing at it; you can move the
  pin on the map page later.

## 2026.9.95

- **Added: you can now edit a gate from your phone.** The bay screen lists the gates on that
  bay, and tapping one lets you change its name, which board and actuator drives it, and which
  bays it connects — or remove it. Previously a gate set up in the field could not be changed
  or removed from a phone at all.
- **Fixed: the gate editor is now sized for use outdoors** — larger buttons and inputs, and no
  more zooming when you tap a field.

## 2026.9.94

- **Fixed: a board you have set up but not yet flashed now says "not flashed"** instead of
  "offline". Previously a board awaiting its first flash looked exactly like one that had
  failed in the field, which sent people out to check hardware that was never written.
- **Fixed: the board identity report now states which boards it checked.** It could report
  "no problems" while a board it had been unable to examine at all sat in the same report.

## 2026.9.93

- **Fixed: the add-on log filled with internal network chatter**, which pushed out the startup
  information support needs when something goes wrong. The log now keeps far more history.
- **Added: PWM reports how many of your boards it has matched to their hardware ID** when it
  starts, so a board still being identified by name is visible rather than assumed.

## 2026.9.92

- **Fixed: the bench simulator could move water through the wrong gate.** On a board driving two
  gates it always read the first one, so a bay could appear to fill before its turn.
- **Fixed: the flow diagram showed the wrong depth and the wrong gate position** on boards with two
  depth channels or two gates — it always showed the first of each.
- **New on phones: the flush close delay and trigger bay.** You can now set which bay's completion
  starts the clock, and how long after that the paddock inlet closes.
- **Fixed: the add-on log filled with a repeating bench message**, which pushed out the startup
  information you need when something goes wrong.

## 2026.9.91

- **Fixed: the +/- buttons on a phone were tall, narrow slivers**, and the row could run off the
  side of the screen. They are now square and wrap properly.
- **Fixed: Channel Setup on a phone hid your channels behind the tab bar** when you scrolled.
- **Fixed: on a phone you could not choose which gate a two-gate board drives** — so a gate set up
  from a phone quietly used the wrong one. You can now pick it, on both channel gates and bay gates.
- **Fixed: calibrating from a phone accepted a disconnected sensor.** A desktop already refused it.
  The phone now refuses it too, and says so.
- **Fixed: a board with three or more depth channels showed and adjusted the WRONG channel.**
- **Fixed: re-saving a board's setup could reset its calibration to factory values**, and could
  change what the board does when it loses WiFi.
- **New on phones:** restore a board's settings after replacing it, read back what a board is
  actually running, set what it does when WiFi drops, and set a gate's emergency open depth.

## 2026.9.90

- **Fixed: your pump's dry-run protection was not actually checking anything.** It looked for the
  depth sensor by an old internal name that no current board uses, found nothing, and allowed the
  start. It now reads the depth channels your board actually declares — and if it cannot read them,
  it says so instead of staying quiet.
- **Fixed: a pump PWM could not read was treated as "stopped", so the automatic stops never fired.**
  If PWM cannot tell whether a pump is running, the safety stops now act anyway. Stopping a pump
  that is already stopped does nothing; failing to stop one that is running does not.
- **Fixed: a gate PWM could not read reported itself as CLOSED.** That let sequences that require a
  closed gate carry on. An unreadable gate is now reported as unknown.
- **Fixed: the pump cleaning cycle could record that it ran when it had not.** If the cleaning relay
  cannot be found, the cycle is skipped and nothing is written to the log.

## 2026.9.89

- **Fixed: a gate watching a board with two depth channels could not say which one it was
  watching.** It now follows the channel you picked, by position on the board rather than by the
  sensor's name — so renaming a board or a channel can no longer point a gate at the wrong water.

## 2026.9.88

- **Fixed: an actuator PWM cannot find on the board is now an obviously dead button**, labelled
  "cannot resolve on the board", instead of a button that looked normal and could act on the wrong
  ram. If you see one, the board needs checking or re-flashing.
- **Fixed: the calibration list in Device Setup matched your actuators by name**, so renaming one
  before flashing could line it up against the wrong ram. It now follows the actuator's position on
  the board, so a rename is safe at any time.

## 2026.9.87

- **Fixed: depth sensors showed "not reporting" on the calibration screen while the board was
  working perfectly.** PWM was looking up each depth channel by its name, and that only worked when
  the channel's name happened to start with the board's name. Channels named anything else could
  not be found, so they looked dead when they were not — and could not be calibrated. PWM now asks
  Home Assistant directly which sensor belongs to which channel, so the name no longer matters. If
  PWM genuinely cannot find a channel it now says **"cannot resolve"**, which is different from a
  sensor that is simply not reading.
- **Fixed: the mobile depth calibration screen always offered two sensors**, even on a board with
  one, and labelled them "1m" and "5m" whatever their real range. It now shows exactly the channels
  your board is set up with, under the names you gave them, with their real range.

## 2026.9.86

- **Fixed: the mobile Channel Setup page did nothing at all.** It showed its header and tabs but no
  channels, and its buttons did not respond — saving a channel or a gate from that page silently had
  no effect. The page now works.
- **Fixed: the mobile Paddock Setup page showed a second back button and title** under the menu bar,
  duplicating the ones already there. They now appear only inside a bay, where Back returns you to
  the paddock list.
- **Fixed: every device offered "Relay 3" and "Relay 4" test buttons, even where those relays
  already drive a gate.** Those buttons could never work. A relay that is spare is still offered,
  and a relay you have named now appears under its own name.


## 2026.9.85

- **Fixed: calibrating a gate's travel time could show the OLD value and still say "Calibration
  complete".** The board had accepted the new time correctly — the page was reading it back before
  the board had published it, so the screen showed the previous number until you reloaded. The
  wizard now waits for the board to report, and if the travel time does not change it says so
  plainly instead of reporting success.

## 2026.9.84

- **Fixed: on a board with two independent gates, the second gate's card could briefly show the
  first gate's valve** when its own valve could not be found by name. It now only ever shows its own.

## 2026.9.83

- **The board's switch type now decides how its gates appear everywhere.** A board with two
  actuators set to *Ganged* (one switch pair) is one gate — one Open/Stop/Close button that moves
  both rams together. Set to *Independent* (a switch pair each) it is two gates, each with its own
  named buttons. Device Setup, the Devices page, the gate editor and the water diagram all follow
  that one setting. "None" is no longer offered — every actuator has its manual switches.
- **A bay gate can now be the second actuator on a board.** When a board drives two independent
  gates, the gate form asks which actuator this gate is, by the actuator's own name.
- **Fixed: automation rules set up for a board's second gate were saved but never ran.** They do now.
- **Fixed: two gates could be pointed at the same actuator by editing one of them.** That is now
  refused, with the name of the gate already using it.
- **Sensor offsets are now one setting, kept on the board, adjusted where you operate it.** Bay:
  the bay's settings. Channel: the gate's cog. Pump: a new ⚙ *Sensor offset* in the pump card's
  More Details. It is the same control in all three, changes apply instantly with no reflash, and
  the board keeps the value through a power cut. Default 0 cm, limit ±100 cm. Offsets you had set
  before are moved onto the board automatically so your readings do not change.
- **Fixed: pressing ± on an offset could replace the board's offset with a tiny number.** The
  page sometimes showed 0.0 when it had simply not read the board's value, and adjusted from that.
  It now shows "—" and refuses until the real value is read.


## 2026.9.82

- **Fixed: a board with two actuators could only be tested and calibrated on the first one.**
  Device Setup now shows a full set of controls — Open, Stop, Close and the calibration jogs —
  for *each* actuator the board is set up for, each labelled with that actuator's own name.
- **Fixed: a depth sensor with a broken loop disappeared from the calibration list.** The sensor
  you most need to recalibrate is usually the one that has stopped reading, and it was the one you
  could not pick. Every depth channel the board is configured for is now listed, and one that is
  not reporting says so instead of quietly vanishing.
- **Fixed: on a phone, a pump with two depth sensors only showed one offset control.** The phone
  now matches the desktop — one offset row per depth channel, labelled with that sensor's name and
  range.
- **Fixed: adjusting a depth offset on the desktop reported "Error" even though it worked.** The
  offset was saved correctly, but the page showed a failure and the numbers did not move until you
  reloaded.

## 2026.9.81

- **Fixed: a board with two depth sensors only showed one offset control.** The offset rows now
  come from the board's own configuration — one row per depth channel it is set up for, each
  labelled with that sensor's name and range, so you can tune each sensor separately.
- Adjusting an offset now targets the sensor by its channel rather than by a "1m"/"5m" label, which
  on a board with a real 1 m and a real 5 m sensor could adjust the wrong one.

**<plain-English note for growers — replace>**

## 2026.9.80

- **Fixed: a gate with two ganged actuators only moved one of them.** If a board is set up with a
  single (ganged) manual switch, its two actuators are linked — opening or closing the gate from
  PWM now drives both, matching what the physical switch already did, and the gate shows a single
  state. Boards set up with two independent switches are unchanged: each gate drives its own.

**<plain-English note for growers — replace>**

## 2026.9.79

- **New depth sensors now smooth over 9 readings instead of 15**, with a reading every 60
  seconds — so a change in water level shows up in about 5 minutes instead of 8. Boards already
  set up keep their current setting until you regenerate and re-flash them.

**<plain-English note for growers — replace>**

## 2026.9.78

- **Editing a board on the Devices page no longer throws you back to the top of the list.** Saving
  keeps the board open so you can carry on editing it, and when you do close, you land back on
  that board's row rather than at the top.

**<plain-English note for growers — replace>**

## 2026.9.77

- **PWM now mirrors Farm exactly.** Any paddock or bay that Farm does not have is removed from
  PWM on the next sync, including its bays and their device settings. Deleting a paddock in Farm
  now fully removes it here instead of leaving records behind.
- Every bay removed this way is written to the log with the board it was connected to, so you can
  see exactly what was removed.
- Nothing is deleted if Farm cannot be reached, or if Farm returns an empty or unexpectedly short
  list.

**<plain-English note for growers — replace>**

## 2026.9.76

- **Paddocks deleted in Farm are now removed from PWM automatically.** Previously they stayed
  behind and could appear twice on the Paddock Control page. The sync only removes a paddock that
  has no bays left in it — one that still holds bays is reported for you to look at, never deleted,
  because removing it would take its bays, boards and automation with it.
- If Farm cannot be reached, or returns an unexpectedly short list, nothing is deleted.

**<plain-English note for growers — replace>**

## 2026.9.75

- **Fixed: panels that should be hidden were showing on several pages** — most visibly a "Sensor
  depths" box stuck at the top of the map page. The rule that hides them was missing on those pages
  and is now defined once for the whole add-on.

**<plain-English note for growers — replace>**

## 2026.9.74

- **Fixed: a stray block of settings (including a Level Sensor picker) appeared at the top of pages.**
  Pop-up dialogs were only being made invisible rather than actually removed from the page, so their
  contents could show through. They are now properly hidden until you open them.
- Fixed a gate-edit dialog on the Paddocks page that appeared as a loose list of fields instead of a
  pop-up.

**<plain-English note for growers — replace>**

## 2026.9.73

- **Fixed: opening or closing one gate moved BOTH actuators on a two-actuator board.** The
  controls sent the command to every actuator on the board instead of the one the gate is assigned
  to. Each gate now moves only its own actuator, and each gate card shows only its own valve.
- If you have a board whose two actuators should always move together, set it up as two gates.

**<plain-English note for growers — replace>**

## 2026.9.72

- **Fixed: opening one gate could move the other gate on the same board.** A gate assigned to a
  board's second actuator was reading its own valve but commanding the first one. Both gates on a
  two-actuator board now command the actuator they are assigned to.

**<plain-English note for growers — replace>**

## 2026.9.71

- **Fixed: the second gate on a board could not be saved.** It was being treated as though it had
  the board's depth sensor, so the system kept asking for overflow protection it did not need.
- **A refused save now tells you.** If a gate cannot be saved because overflow protection is
  missing, you get a clear "NOT SAVED" message and are taken straight to that setting — instead of
  the save quietly doing nothing.

**<plain-English note for growers — replace>**

## 2026.9.70

- **Fixed: two gates on the same board could end up driving the same actuator.** Commanding one
  gate would move the other. If your board has two actuators, the actuator picker now appears
  correctly on the Channels page and your choice is saved.
- If a gate was set up before its board gained a second actuator, saving it now picks up the
  board's real actuator count. On an affected board, save the second gate first.

**<plain-English note for growers — replace>**

## 2026.9.69

- **Bench only:** channel overflow protection now reads the bench simulator's water level, so the
  channel-emergency sequence can be rehearsed on the test rig where no depth transmitter is fitted.
  On a farm nothing changes — the gate reads its real sensor exactly as before.

**<plain-English note for growers — replace>**

## 2026.9.68

- **Fixed: a pump could refuse to start in Manual.** If the channel was above the pump's demand
  level, Start was refused with an "Emergency level" message even though the demand level only
  applies in Auto. The demand level now affects starting and stopping the same way — in Auto only.
- The pump card says **"At Demand Level"** instead of "EMERGENCY", and only when the pump is in
  Auto. The channel's own emergency level is a different setting and still applies in every mode.
- **Channels page:** overflow actions are now one compact row each, and you can choose the gate you
  are editing as the target, not just other gates.

**<plain-English note for growers — replace>**

## 2026.9.67

- **Channel overflow protection now works in Manual too.** If a channel reaches its
  emergency depth it opens the gate and runs its actions — stopping a pump, closing a
  feeding gate — even if the channel or the pump is switched to Manual. A channel about
  to spill is not an operating preference.
- Everything else still needs Auto: auto demand, and the rules that open and close gates
  for offtake, pump watch and downstream.
- **The action picker now sits inside Overflow protection** on the Channels page, with
  the sensor and trip depth, instead of in a section of its own.
- **Fixed:** editing a gate on a phone could silently erase overflow actions set up on a
  computer.

**<plain-English note for growers — replace>**

## 2026.9.66

- **Auto Demand's depth level now only applies in Auto.** It is the level at which the channel is
  full enough to stop pumping — part of Auto Demand, not a separate safety. The page wording changed
  from "emergency" to "demand" to match.
- **Channel overflow protection can now act on what is filling the channel.** As well as opening the
  gate to relieve water, it can stop a pump, close another gate, or send an extra alert. Choose them
  on the Channels page under Overflow actions.
- **The Channels gate setup page is now tiles** — pick one thing to set up at a time instead of one
  long form.
- **Fixed:** a pump could be stopped for "zero demand" when the system could not actually read its
  watched gates (for example after a gate was deleted, or while its board was offline). It now leaves
  the pump alone and records why.

**<plain-English note for growers — replace>**

## 2026.9.65

**A pump whose level sensor cannot be read now says so.**

If a depth sensor's wiring is broken, the board detects it — but PWM was still reporting the
pump as protected, because a broken 4-20 mA loop publishes a number rather than nothing.
That is now treated as a fault, so the pump never appears protected when it is not.

Pit Demand now only appears on pumps a channel gate is actually watching, and it no longer
changes appearance when Auto Demand is switched on — the two are independent.

## 2026.9.64

**Bench only — flush clocks on the water-flow diagram.**

The rig's Live Water Flow page now shows each bay's flush timer on the bay itself, plus the
paddock's phase, arming window and close-delay countdown. Clicking a bay or gate opens its
controls beside it instead of in the corner of the screen.

## 2026.9.63

**Fixes the device list disappearing on the Devices page.**

A formatting mistake in the previous version stopped the Devices page loading its list of
boards. Corrected.

## 2026.9.62

**Depth sensor calibration now actually works.**

Calibrating a depth sensor was saving nothing while reporting success, so a board would
read exactly the same after being re-flashed. It now writes the calibration correctly, to
the right sensor channel, and refuses with a clear message if it cannot. The sensor picker
lists only the channels your board really has, by name. "Apply range" no longer overwrites
a measured zero point.

## 2026.9.61

**Internal test fixes found before release.**

The release checks caught a box on the map page whose text colour was unset, which could
have made it unreadable. Fixed, along with several checks that had gone out of date with
the new colour scheme.

## 2026.9.60

**The Home button reads properly again, and so does everything like it.**

The Home button had ended up with black writing on a blue background. It is white on blue
again. Eleven other buttons and badges had the same kind of problem and are fixed with it —
coloured backgrounds take white writing, grey ones take black.

## 2026.9.59

**Pumps & Channels now works on a phone.**

The depth list for pumps and channel gates was only ever on the desktop layout — on a
phone there was no way to see those readings at all. It is now a tab on the map page, with
the same six-hour history when you tap a reading.

## 2026.9.58

**Tap a depth reading to see the last six hours.**

On Pumps & Channels, the depth boxes are now clickable and show a six-hour chart with the
lowest, highest and current reading. Channel gates that measure depth now appear in that
list — some were being measured but not shown. Boards are named by their friendly name
instead of their ESPHome name, and the paddock labels have been removed from the main map.

## 2026.9.57

**Setting up a board is now five clear steps instead of one long form.**

Opening a device gives you five tiles — Details, Actuators, Sensors, Relays and Actions —
and each one opens as its own full-width page with room to work, the same way Pump Setup
already works. Nothing about what a board stores has changed; it is only easier to find.

## 2026.9.56

**Every Save button looks the same now — blue.**

Save buttons had drifted into six different styles, so the same action looked different
depending on which page you were on. They are all the one blue button now, and changing it
in future is a single change rather than eleven.

## 2026.9.55

**The last of the hard-to-read buttons.**

Eighteen more buttons and badges had dark writing on a strong colour — including the
paddock mode button, the open-gate marker on the map and the pump ON button. Every
coloured control in the app has now been checked and reads clearly.

## 2026.9.54

**Coloured buttons are readable again, and boards can be flashed.**

Around a hundred buttons and badges across the app had black writing on a strong blue,
red, amber or green background, which is hard to read on a screen in daylight. They now
use white writing. Grey buttons keep their black writing, which was already clear. The
paddock, bay and board names on the Paddock Setup map were blurry and are now sharp.

Also fixed: no board could be re-flashed. A firmware setting added recently had no default
value, so every board already set up stopped building with an error about "dp_window".
Existing boards kept running, which is why they still showed as online.

## 2026.9.53

**One button for Auto/Manual, and a bigger depth reading.**

A channel gate's Auto and Manual buttons are now a single button that shows which mode
you are in — green for Auto, grey for Manual — and swaps when you tap it, the same way
the paddock mode button works. The current depth figure on the map is larger on desktop,
matching the size already used on phones.

## 2026.9.52

**Buttons that were hard to read, or unreadable, are fixed.**

The plus/minus buttons for water depth now match the ones for hours — solid red and green
everywhere instead of washed out on some pages. The auto-demand OFF button was showing
black writing on a black box and could not be read at all; it is grey now. The low-supply
override button is green while protection is on and red while it is overridden, instead of
two shades of brown. "Check Supply Sensor" is now a bright yellow warning badge so it can
no longer be mistaken for a settings button. Small grey labels inside the pump card are
black.

## 2026.9.51

**Gate colours now read as how much water is flowing.**

Shut is deep red, holding is a light blue, fully open is a strong blue — so a partly-open
gate looks like partial flow rather than a warning. The three are distinct in brightness as
well as colour, so they read in bright sun.

## 2026.9.50

**Pump page buttons are readable, and the relay shows the right colour.**

Start, stop, timer and refuel buttons had dark text on strong colours and were hard to
read. The +/- buttons were so pale they looked blank. The relay button showed ON in grey
and OFF in red — it is now grey for off and green for on. Pump shows red when off, blue
when running.

## 2026.9.49

**You can now see when a gate is part-way.**

A gate holding between open and shut used to look the same as fully open. It now has its own
amber colour, distinct from the blue of open and the red of shut — and the three tell apart
in bright sun, not just by colour. Text across the screens is also sharper.

## 2026.9.48

**Gates you can read at a glance, and consistent text everywhere.**

Open gates are light blue, shut gates are dark red — they now differ in brightness as well
as colour, so you can tell them apart in bright sun or at a distance. Menu and map headings
use one consistent style. No change to how anything operates.

## 2026.9.47

**Pop-up message text is readable again.**

Notification pop-ups briefly had pale text on a pale background. Now black on grey.

## 2026.9.46

**Readability fixes across the screens.**

The side menu text was pale on a pale background and is now black. Paddock names on the map
had a dark glow that made them look smudged — they now have a clean white outline. Menu tabs
match the rest of the text. Type renders sharper. No change to how anything operates.

## 2026.9.45

**A new, higher-contrast look — built to be read outdoors.**

Light grey screens with black text, so the display stays legible in sunlight. Colour now
means one thing each: blue is water moving, green is good (online, automation on), red is a
problem, grey is off. Nothing about how your pumps, gates or schedules behave has changed.

## 2026.9.44

**A security update to a component PaddiSense uses internally.**

No change to how the system behaves in the paddock — your pumps, gates, channels and
schedules all work exactly as before. This release updates a networking library to a
version that closes three published security advisories. Nothing you do changes; it is
worth installing.

## 2026.9.43

**Housekeeping.** Removed 41 leftover styles that no part of the app used any more. No visible
change — this makes future appearance changes reach everywhere they should.

## 2026.9.42

**Every paddock and bay from Farm now shows on the map**, whether or not its automation is
switched on. Enabling a paddock arms its automation — it was also deciding what you could
see, so a paddock could list four bays and draw none.

**Check mirror now works.** The button did nothing at all.

**Buttons are readable.** Start, Pause and several others were white text on a colour too
light to carry it.

## 2026.9.41

**A deeper background, and page titles you can read.** The page background is a darker
blue, so white cards stand off it more clearly. Some page headings were dark text sitting
straight on that blue — they are white now.

## 2026.9.40

**The Inputs list reads properly.** Sensor names no longer repeat the board's name
("Pump 1 Pump 1 Pit Depth"), readings are rounded to the precision the board actually
publishes instead of fourteen decimal places, and analogue and digital inputs are in their
own cards.

## 2026.9.39

**Panels inside a card are now clearly separated.** Sections nested inside a card were
almost the same white as the card itself, so everything ran together. They now sit on a
visibly deeper background with a stronger edge, across every page.

## 2026.9.38

**Sensors & Calibration is readable again.** The sensor list showed Home Assistant's
internal names, which ran over the readings beside them — it now shows the sensor's own
name. The section is also split into three cards (live readings, the sensor's channel and
range, and two-point calibration) instead of one long white panel.

## 2026.9.37

**Check mirror.** A new button on Paddock Setup compares what PaddiSense holds against what
Farm actually has, and tells you plainly whether they match. It lists anything Farm has that
PaddiSense never received, anything PaddiSense is holding that Farm has dropped, and any
records with no link to Farm at all. It only reads — nothing is changed or deleted.

## 2026.9.36

**Groundwork so colours stay consistent.** Every colour in the app now comes from one
place, so a change to the theme reaches every page, button and label instead of leaving
patches behind. Also fixes the map, where a channel's outline and its fill could show
different colours for the same mode.

## 2026.9.35

**The new look, finished properly.** Text that was the wrong colour for its background —
in places the same colour, so it simply was not there — has been corrected across every
page: pump and channel cards, the countdown timer, gate depth, map labels and popups, the
setup tiles, and every button. Several buttons had been rendering with no background at
all. Start and Stop on a pump are now full contrast.

## 2026.9.34

**Paddock Setup now shows what PaddiSense actually holds.** Paddocks mirrored from Farm
were listed as "Unlinked" even though they were linked, and a paddock whose name differed
between Farm and PaddiSense could be added a second time by accident. The list is now in
three clear groups, and enabling a paddock says plainly that it starts its automation.

## 2026.9.33

**Completes the new look.** 2026.9.32 changed the colours but left some text the wrong
colour for its background — a few panels showed white text on white. Every panel now sets
the right text colour for what it sits on.

**Depth calibration: set the sensor's range, or type a voltage.** Pick 1 m or 5 m and press
Apply range, and you no longer need ESPHome. You can also type a known voltage instead of
waiting two minutes for a sample.

## 2026.9.32

**A new look, built to be read outdoors.** Pages are now blue with white cards instead of
dark grey on near-black. The old scheme was almost invisible in sunlight.

**Depth sensors: tell PaddiSense the sensor's range.** A 1 m and a 5 m sensor are wired
identically, so PaddiSense could not tell them apart and assumed 1 m — a 5 m sensor read a
fifth of the real depth. Set the range when you set up the board.

**Depth readings update as often as you ask.** The interval now means what it says: set
30 seconds and you get a new number every 30 seconds. You can also set how much smoothing
is applied, and the page tells you how quickly a real change will show.

**Fixed: a board showing nothing.** Some boards showed no firmware version, no WiFi signal,
an empty sensor list and "offline" while working perfectly. They now report correctly, and
2-point calibration can be started again.

## 2026.9.31

**Fixes the update that splits a dual-actuator board into two gates.** In 2026.9.30 that step could
not run, so boards with two actuators were left as they were. Update to this version and the split
happens as described below.

## 2026.9.30

**A board with two actuators now gives you two gates.** When you pick a board for a gate you also
pick which actuator it drives — named after the actuator itself, like "Main Channel" or "Spur" — and
that gate then configures only that actuator. The other actuator can be its own gate on a different
channel, which is what a spur usually is.

**Existing dual-actuator boards are split for you** on update: the second actuator becomes its own
gate, with its rules, on the same channel. **Move it to the channel it really belongs to** — PWM
cannot know that, so it does not guess.

**New "Pumps & Channels" tab on the map page** showing the current depth for every sensor on a pump
or channel gate, in one list.

## 2026.9.29

**Bays now follow Farm automatically.** If you move a bay to another paddock in Farm — or Farm
re-homes it after you redraw a boundary — PWM moves it too on the next sync. You no longer get a
list of bays "kept under" the old paddock asking you to move them by hand, and bays will stop
appearing to be missing from a paddock they belong to.

The bay keeps everything PWM owns: its board, gates, sensors, levels and automation all travel with
it. If its new paddock is not enabled, its automation simply does not run until you enable that
paddock.

## 2026.9.28

**Fixed: the + and − buttons said "no depth-1 entity on this device".** On boards whose sensor is
named (for example "Supply Depth") the adjust buttons could not find the sensor they were showing.

**Fixed: Current Depth showed "—" on the Pumps page** for the same boards, while Pump Setup showed
the reading correctly. Both now look the sensor up the same way.

## 2026.9.27

**The big number between − and + is now the actual depth**, with your offset already applied — the
pit level you are trying to match. Before, it showed the offset amount, which told you nothing about
the water. The offset itself, and the sensor voltage or any fault, sit on a small line underneath.
Pressing − or + moves the depth straight away.

Each sensor also gets its own heading, so nothing wraps onto two lines on a phone.

## 2026.9.26

**Pumps with one depth sensor now show one offset.** A second set of offset controls was showing on
boards that only have one sensor.

**The +/- buttons on a phone are bigger and further apart** — they were too small to press just one.

**You can now enter a run you did by hand.** If a pump was run in manual, add the hours and the
water pumped and both totals catch up. It is added as an extra entry rather than overwriting the
figures, so nothing you already recorded is lost.

## 2026.9.25

**The Sensor Offsets rows line up properly now** — sensor 1 and sensor 2 on neat rows, nothing
wrapping or squashed, with the offset and the resulting depth side by side.

**The Depth Calibration section has been removed.** It had no tile and was showing on the settings
screen all the time. Where calibration is done is explained under Sensor Offsets instead.

## 2026.9.24

**Pump Setup on your phone now uses tiles as well.** Instead of scrolling through every section, you
get Live Status, Pump Details, Live Settings, Demand Control, Service Items, Notes and Bench Tests
as tiles, and you tap the one you want.

## 2026.9.23

**The sensor offset row now says what each number is.** The value between − and + is the **offset**
you are applying (now shown in cm), and beside it **"reads"** is the depth with that offset applied.
There is a short note under the card explaining it.

**The Depth Calibration tile has been removed** — it only ever said "calibration is done on Device
Setup". That sentence now sits under Sensor Offsets, where you would be looking when you need it.

## 2026.9.22

**Pump Setup pages are laid out properly now.** The map on Pump Details drew as a white box with a
small map in one corner — it is measured correctly when you open the tile. And settings like the
sensor offset no longer stretch a single number across the whole screen; boxes are sized to what
goes in them.

## 2026.9.21

**Pump Setup tiles now open a proper full-width page.** Tapping a tile used to reveal the section
squeezed into half the screen with an empty column beside it. Each section now opens as its own
card across the full width, with the forms laid out to suit it.

## 2026.9.20

**The Pump Setup tiles now actually work.** They appeared, but every form was still shown beneath
them. Tapping a tile now opens just that one section.

**The pump card no longer contradicts itself.** With a broken sensor the top of the card said "LOOP
FAULT" while the Device section still listed a depth of -10.0 cm for the same sensor. Both now say
the sensor is faulty.

## 2026.9.19

**Pump Setup is much simpler to find your way around.** Instead of every setting on one long page,
you now get tiles — Pump Details, Live Settings, Depth Calibration, Auto-Stop Monitoring, Service
Items, Notes — and you tap the one you want. "← All settings" takes you back. Nothing has been
removed; it is just one thing at a time now.

**The pump card tells you which sensor needs attention.** It used to say just "Check Sensor", which
meant the downstream demand sensor even when the problem was the pump's own supply sensor. It now
says **Check Supply Sensor** or **Check Demand Sensor**.

## 2026.9.18

**The pump card now shows Current Depth.** One line on each pump — the live supply depth with your
offset applied — so you can check it without opening Setup. On a phone it sits just above Auto
Demand. If a pump has two depth sensors it shows the lower one, because that is the reading the
Low-Supply protection uses. If the sensor's wiring is broken it says so instead of showing a depth.

## 2026.9.17

**Depth sensors: you can now see whether the sensor is actually working.** Pump Setup shows the raw
sensor voltage beside the offset controls, and if the sensor is unplugged or its wiring is broken
the page says **"LOOP FAULT — check sensor wiring"** instead of showing a misleading depth. A
disconnected sensor used to read −10 cm, which looked like very shallow water and could not be
corrected with any offset.

**Boards with a hyphen in their name now show their readings.** Pumps on boards named like
`pmp-01` showed an offset of 0 and a live depth of "—" for every sensor; that is fixed.

**The pump card shows the current depth again**, and Pump Setup now says the depth is measured from
your own zero, with the offset applied.

🔧 **Your boards need re-flashing** to publish the new sensor-fault signal. Until a board is
updated, PWM says so rather than pretending the sensor is fine.

## 2026.9.16

**You can see at a glance which pumps are running.** A running pump's card is now green all over,
and a pump whose board is offline is red — instead of a thin coloured stripe down one edge that was
hard to spot. Pumps that are simply off keep the plain grey card.

## 2026.9.15

**The Home button is back on the Pumps page on your phone.** A styling fault from the Channels split
was swallowing the top bar on that one page.

**Delete a bay in Farm and it now goes from PWM too** — PWM mirrors Farm. Redrawing a bay is still
safe: PWM recognises the replacement and keeps that bay's board, gates and automation.
**Safety net:** if Farm ever reports no bays at all, or a large share of your bays vanish at once,
PWM refuses to delete them and lists them for you instead — it will not wipe your setup on the
strength of one odd answer from Farm.

## 2026.9.14

**Fixed a false warning on Paddock Setup.** Bays sitting under a paddock you have not enabled were
being listed under "Pointing at something that is gone". They were never gone — they simply are not
drawn on the water chain until the paddock is enabled. Only genuinely missing links are listed now.

**Pump and Channel cards are easier to tell apart** — a lighter card surface and a clearer edge, so
they no longer read as black on black.

## 2026.9.13

**One Sync brings everything across from Farm.** Paddocks and bays you draw in Farm now arrive in
PWM by themselves — no more importing them one at a time. Redraw a bay in Farm and PWM follows it,
keeping that bay's board, gates, sensors and automation. Get something wrong? Fix it in Farm and
sync; PWM mirrors what Farm has.

**Paddocks arrive switched OFF, and you turn them on.** Enabling a paddock is what puts its bays
under automation, so new paddocks appear on the map but are not running anything until you enable
them. **Enabled paddocks are now outlined in blue**, so you can see at a glance which ground PWM is
actually working.

**Sync from Farm has moved to the top of the Paddock Setup panel**, instead of being below the
whole paddock list.

## 2026.9.12

**Redrawing a bay in Farm no longer costs you its setup.** If you delete a bay in Farm and draw it
again, PWM now offers to **re-bind** the existing bay to the new shape — its board, gates, sensors,
levels and automation all stay exactly as they were. Previously the import just said "already
exists" and the only way through was deleting the bay and setting it all up again.

**Bays that Farm moved to another paddock now say so.** Farm re-homes a bay to the paddock its
ground actually sits in. PWM deliberately does not move it for you, so Paddock Setup now lists those
bays and tells you where Farm has them — instead of leaving you with a bay under what looks like the
wrong paddock and no explanation.

## 2026.9.11

**Buttons at the bottom of pop-up windows now fit a narrow browser too.** Cancel / Place on Map /
Save used to be squeezed onto one line; they now flow onto a second line when there is not room.
The rest of the pages were checked at the same time and needed no change.

## 2026.9.10

**Channel Setup now fits a half-width browser window.** The row of buttons along the top (+ Channel,
+ Gate, Map and the rest) used to be crushed onto one line when the window was not full size, with
labels breaking mid-word. They now keep their proper size and flow onto a second line. The Bench Sim,
Devices and Water Chain pages got the same treatment.

## 2026.9.9

**The Paddocks page now tells you when a link points at something you deleted.** If a gate or bay was
ticked as feeding something, and that something was later removed, the link quietly did nothing. The
"Not connected yet" panel now also lists these under *Pointing at something that is gone*, so you can
re-tick the right one instead of wondering why the Water Chain has a piece missing.

## 2026.9.8

**"This gate feeds" now already knows about your bays.** When you set a bay's supply gate on the Paddocks page, that
gate's "This gate feeds" list shows the bay ticked and greyed, marked *from this bay's supply gate* — you do not answer
it twice. Tick a box yourself only for something extra the gate feeds.

**Fixed: a bay you ticked there never appeared on the Water Chain.** Bays ticked under "This gate feeds" were stored in
a form the chain could not match, so the line was never drawn and the bay kept showing as unconnected. Those ticks now
draw properly — nothing to re-enter.

## 2026.9.7

**The Pumps page was blank — fixed.** A change in 2026.9.4 (moving Channels onto its own page) broke the Pumps page's
styling so the page rendered empty. Pumps are back, with their Auto/Manual and Low-Supply buttons styled as before.

## 2026.9.6

**The tick boxes in Upstream Offtake look right again** — small tick boxes sitting neatly beside the gate name and its
Open/Closed/Any choice, instead of big pale squares.

## 2026.9.5

**You can now say where a bay's water comes from.** Open a bay on the paddock setup page and pick its supply gate from
the new "Water comes from" list. That is what draws the water chain — pump, channel, gate, bay.

**A board with two actuators shows both.** If the second actuator had no name, its rules were hidden and it could not be
picked as the channel's own offtake. It now appears either way.

**The Upstream Offtake list is easier to read** — the Open/Closed/Any choices line up in one column.

**The map page is called Paddocks in the menu**, matching the home screen.

## 2026.9.4

**Channels now has its own button and page.** The home screen has three buttons — Paddocks, Pumps and Channels. Channel
gates used to be hidden at the bottom of the Pumps page. Nothing about how they work has changed; they have their own
page now. Channel setup stays where it was.

**Pump board settings that don't reach the board now say so.** If a setting could not be sent to a pump board, the
screen used to say it had synced. It now tells you which settings did not arrive.

## 2026.9.3

**Pump schedules set weeks ahead start at the right time.** A pump start scheduled for a date after the daylight-saving
change (for example set in September for a start in December) was armed an hour off. It now uses the clock that will
be in force on the day.

**Security fix.** A background logging component was hardened so an unusual web request cannot slow PWM down.

## 2026.9.2

**Housekeeping and hardening — nothing changes on your screens.**

Database upgrades can now be reversed cleanly where that is possible, and the ones that genuinely
cannot be undone are written down as such, so a future upgrade problem is easier to back out of.
Separately, the link PWM uses to fetch paddock boundaries from Farm is now checked more strictly
before it is used, so it cannot be pointed anywhere it should not go.

## 2026.9.1

**Security: the browser protections now apply to every response, including "please log in".**
The pages you use already carried the standard browser security headers; the short "not logged in"
and "redirect to login" replies did not. They now do. Nothing changes in how you use PWM.

## 2026.8.75

- **Security: the factory database password is gone from the shipped defaults.** PWM now starts
  with a blank database credential and fails safely if one has not been set, rather than falling
  back to a known default. The start-up warning that tells you a box is still on the factory
  credential is unaffected and still works. No action needed on your part.

## 2026.8.74

- **Gate names on the Upstream Offtake card were squashed to one letter per line.** That card is
  the only list that shows an Open/Closed/Any picker next to each gate, so it was the only place
  the name got crowded out — it now keeps its width and reads normally. Display only; no
  automation behaviour has changed.

## 2026.8.71

- **Your phone was describing an automation rule that no longer applies.** The Upstream Offtake card
  in the mobile app still explained the old behaviour ("close the gate when the offtakes above are
  open"). Since an earlier update the rule also *opens* the gate when your chosen pattern is matched.
  The card now describes what the gate actually does. Nothing about your gates changed — only what
  the app told you about them.
- **If a gate's offtake settings were saved before that change, the log now says so**, because those
  older settings behave differently under the new rule and it is worth re-checking that gate.
- **A valve that reports an unreadable position is now recorded** instead of being quietly treated as
  fully open.

## 2026.8.70

- **Editing gate rules on your phone could wipe the ones you set on the desktop.** There were three
  separate rule editors — desktop, mobile Channel Setup and mobile Automation — and each saved only
  the boxes it could see, so a change made in one place silently removed selections made in another.
  They now share a single editor. **If you have edited gate rules from more than one device, it is
  worth checking them once after this update.**

## 2026.8.69

- **The automation page now shows every step, including the ones that did not run.** Previously it
  stopped listing steps after the rule that acted, so a rule that never got its turn simply did not
  appear — and a missing line looks like a line that was fine.
- **You can now see the countdowns.** When a gate is waiting out a reaction delay or a settle period,
  the page shows how many seconds are left, so "why hasn't the gate moved yet?" has an answer.

## 2026.8.68

- **Downstream Demand is edited in one place only.** The pump page's gate settings used to edit the
  same rule as Channel Setup, and it armed it differently — so changing it in one place could switch
  on a rule you had switched off in the other.
- **"What this gate feeds" is now its own setting**, separate from the Downstream Demand rule. It
  describes your water chain whether or not any automation is switched on, so it no longer disappears
  when you turn that rule off.

## 2026.8.67

- **Setting the pit level no longer moves your gates.** Choosing High, Low or Off now only tells the
  system what to aim for. To open or close a gate yourself, use the channel card on the pump page.
- **Upstream Gate Control has been removed from the pump configuration page.** It was a second copy of
  the Pump Watch settings already on Channel Setup, and whichever page you saved last won.
- **The "Demand Level Changed" notification is gone** — you are standing at the button you just pressed.

## 2026.8.66

- **Upstream Offtake now opens the gate as well as closing it.** When every offtake above is open it
  closes, holding water back for upstream. When the pattern you choose is matched it opens, letting the
  surplus through. Previously it could only ever close, so once closed nothing reopened it.
- **The Full/Any threshold is replaced by a per-offtake pattern** (Open, Closed or Any) that you set
  yourself. ⚠ **If you previously used the "Any" setting, please re-check that gate** — your settings
  are kept, but that option no longer exists and the gate will behave differently.
- **My Demand Level is now part of the same section** rather than a separate box with its own list.

## 2026.8.65

- **A pump could stop telling you it needed water.** The "demand required" alert was meant to fire once
  and then reset when conditions changed. In several cases the reset was skipped, so once the alert had
  fired it stayed silent from then on. It now resets properly. This is the opposite of the notification
  flooding and it is the more serious of the two — a warning you never receive again.

## 2026.8.64

- **The direct pump relay controls on the device page are now bench-only.** On a farm box, a pump can
  only be started through the pump page, where the safety checks live — minimum depth, anti-short-cycle,
  the emergency level refusal and start confirmation. The direct control skipped all of them.

## 2026.8.63

- **The demand tag and emergency reading on the pump card were frozen at page load.** A card could show
  EMERGENCY over a pump that had been running normally for ten minutes. Both now update with the rest of
  the live page.
- **Several indicators were invisible** because of a colour that did not exist — the armed indicator, the
  Auto Demand button and the running-pump icon on the map all now show.

## 2026.8.62

- **New Diagnostics page.** It shows where an automation got to and why it stopped, in plain language, so
  you can say "it breaks when it hits this point". The existing trace page was only available on test
  boxes and was written for engineers.

## 2026.8.61

- **🔴 Important: pumps were not stopping when they should have.** The system could not tell whether a
  pump was actually running, so every automatic stop that depends on knowing that — including the stop
  when there is no demand — never fired. On the test rig, two pumps ran for seven minutes at 78 cm
  against a 50 cm emergency level and nothing stopped them. The system now identifies each pump's
  running state correctly. **If you have had pumps run longer than expected, or received repeated
  notifications, this is the likely cause.**

## 2026.8.60

- **Six indicators that should have been green or grey were showing as blank white boxes.** Fixed.

## 2026.8.59

- **Pit Demand is simpler and does what it says.** It reads your pump's own supply sensor and holds the
  pit between High and Low, or is Off and does not control the gate at all. The automatic calculation
  that sat behind it has been removed.

## 2026.8.58

- **The pump configuration page now shows at a glance what is armed** — a green or grey box, and beside
  it the gates, level and sensor actually configured, instead of four lines of explanation.
- **The "demand required" notice is sent once** rather than repeatedly, and re-arms when things change.
- **The collapsed pump card shows the demand state**, so you can see No Demand or Demand Required
  without expanding it.

## 2026.8.57

- **The emergency level now stops the pump whether or not Auto Demand is on.** Previously it only applied
  in Auto, so a pump running in manual had no level protection at all. It is a safety, it reports as a
  fault, and it clears as soon as the level drops.
- **Auto Demand and Pit Demand are separate automations** with separate settings — one manages where the
  water goes, the other keeps the pit supplied. Changing one no longer affects the other.
- **A level sensor that cannot be read now shows "Check Sensor"** rather than appearing healthy, and a
  pump with no sensor set shows "No Sensor".

## 2026.8.56

**Internal improvements — no user-visible changes.** Restored a set of internal safety checks that
had stopped running after the previous update.

## 2026.8.55

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are
with a cryptographic token before they can change this add-on's licence or permissions.
Previously, being on the box's internal network was treated as sufficient proof.

## 2026.8.54

**Internal improvements — no user-visible changes.** Removed start-up code-quality checks that could
report "passed" when they had in fact found problems. These checks belong in our build system, which
already runs them properly before your update is published.


## 2026.8.53

- **Pond now tops a bay up when it drops 2 cm below its minimum** — Peter's number, replacing the
  placeholder that shipped in the previous version.


## 2026.8.52

- **The system no longer repeats a command it has already given.** Opening a gate that is already
  open, or telling a pump to do what it is already doing, is noise — every action now checks the
  equipment's actual state first. Stop commands are never suppressed.


## 2026.8.51

- **Pond mode now works the way a paddock actually ponds.** A bay that drops below its minimum draws
  from the bay above it, so demand travels *up* the chain while water travels *down*. It is the
  opposite direction to Flush, and it is now modelled that way rather than each bay acting alone.
- **A gate shared between two bays is decided once per pass**, taking both bays into account, so it
  can no longer be opened by one rule and closed by another in the same minute.


## 2026.8.50

- **Fixed: a flush could sit waiting for water that was already there.** The top bay's supply gate
  reads the channel, and on the bench rig nothing was writing that reading — so the cascade waited
  indefinitely with the channel charged. Found by walking a real flush on the rig; twenty-two
  passing tests had not shown it.


## 2026.8.49

- **The gate rules are now editable on desktop, not just on a phone.** Downstream Demand, Upstream
  Offtake, Pump Watch and My Demand Level could only be set from the mobile pages, even though the
  desktop run sheets described all five.


## 2026.8.48

- **Fixed: the Automation page would not scroll.** Longer run sheets ran off the bottom of the screen
  with no way to reach them.


## 2026.8.47

- **Flush is now a paddock-wide cascade instead of a set of independent bays.** Water enters at the
  top and moves down the chain, which is how a paddock actually flushes. The supply is deliberately
  *not* closed when the first bay reaches its minimum — the inflow is the only path to the bays
  below it — and the inlet closes on a timer after the bay you nominate finishes, because a bay
  finishing is a clear event where a depth reading on a filling bay is not.
- **Flush ends with the drains left open.**


## 2026.8.46

- **Fixed: the flush hold timer paused when the add-on did.** The hold is how long water has sat on a
  bay — a physical fact that keeps running through a reboot or an update. It was counted down in
  software instead, so a restart mid-flush left water on the bay for the length of the outage *on
  top of* its timer. It is now measured against the clock.


## 2026.8.45

- **Run sheets now show each step's actions on their own lines, in the order they happen** — the
  trigger first, then what the system does. Previously a step that did three things read as one
  sentence and the order was not visible.


## 2026.8.44

- **Fixed: bay water depths had stopped being recorded.** Depth history is what shows how much water
  each bay uses and loses, so this is now logging again for every bay with a depth sensor.
- **The Water Chain page now leads with a live picture of your water** — pump to channel to gate to
  bay, filling as it actually is.
- Connecting a bay to its water source has moved to Paddock Setup, where you lay the bays out.


## 2026.8.43

- **A failed depth sensor now shows ERROR on the map**, right where its reading would be, instead of
  a dash that looked the same as a bay with no sensor fitted. You can see it at a glance and it no
  longer needs to send you an alert.
- **Fixed: the map was showing the wrong reading for a bay** — it used the supply gate's board
  instead of the one standing in the bay.
- **Fewer pointless alerts.** A bay switched Off is no longer monitored, and the system no longer
  warns that a bay isn't filling when the pump was never running.
- **The automations page no longer hides behind the menu.**


## 2026.8.42

- **The paddock setup page no longer covers the main menu.** It was painting over the navigation and
  only letting it show through while the map was zooming.
- **A pump board now shows "running" or "stopped"** instead of "unknown" — it has no valve, so it was
  being asked the wrong question.
- **On Device Setup, a folded section opens from anywhere on the card**, not just its title.


## 2026.8.41

- **The Wi-Fi drop policy is now on both gate edit forms** on the paddock page, not just the one
  reached from the map pin.
- **The Test & calibrate button on Device Setup is now a proper button** — it was too small to find.


## 2026.8.40

- **Fixed: the Test panel on Device Setup would not open** after the previous update.


## 2026.8.39

- **The Sensors page and the Bench page have been retired.** Everything you did on the Bench —
  identify a board, test its outputs, calibrate its depth sensors, back up and restore its settings —
  is now on **Device Setup**: open a board and press **Test**. Sections fold away so the page stays
  short.
- **You can now set what a gate does if it loses Wi-Fi** where you place the gate: open it on the
  paddock map, choose the board, and pick Hold, Close or Open. It is written straight to the board,
  so no reflash is needed.
- **The paddock map's side panel no longer fades in and out** — it stays on, with the map beside it.
- **The channel page shows its No-WiFi values again** instead of dashes, and no longer reports a
  healthy board as "not reporting".
- **Save on the channel page has moved to the top**, with Delete beside it, and the page now warns
  you if you leave with unsaved edits.
- Sensor names no longer repeat the board name ("MC-01 MC-01 Depth").
- You can **rename a channel**.


## 2026.8.38

- **Fixed: a gate set to Manual could switch itself back to Auto when the add-on restarted.**
  Introduced by the previous update; your Auto/Manual choice now survives restarts and updates.


## 2026.8.37

- **The Auto/Manual switch now means the same thing on every page.** Setting a gate to
  Manual on one screen and Auto on another could previously leave the two disagreeing.
- **You can set the order gates appear in** on the pump page — open a gate's settings and
  enter a display order. Existing channels are numbered from their gate names to start.
- **You can rename a channel** from the channel setup page.


## 2026.8.36

- **The bench simulator now runs on one of your real paddocks** instead of a separate test paddock of
  its own. Pick the paddock and it uses its bays and their boards exactly as you set them up.
- **The PDEV Bench test paddock has been removed** — it duplicated bays on the same boards as your
  real paddock.
- **The map now names every bay.** The first bay in a paddock used to be labelled "Supply" instead of
  its own name.


## 2026.8.35

- **Putting a gate or a channel in Manual now actually stops its automation.** The Auto/Manual
  buttons were being saved and displayed correctly but the automation ignored them, so a gate you
  had switched to Manual could still open and close on its own. Existing gates keep running exactly
  as they are — the switch simply works now.


## 2026.8.34

- **The bench simulator now works on a rig with no depth sensors fitted.** It measures what each
  board reads with no water when you arm it, then drives the difference, so a simulated bay reports
  the depth you asked for and the automations react as they would in a real paddock. Previously a
  full bay only moved the reading by a fraction of a centimetre and nothing ever triggered.
- **A board that cannot be simulated now says so** instead of sitting at a fixed reading that looks
  like the automation is stuck.

## 2026.8.33

- **A bay now reads its water depth from the board on its drain gate automatically.** That board is
  the one physically standing in the bay; the board on the supply gate is measuring the channel or
  the bay above it, so it is never used. You no longer have to set the sensor separately, though you
  still can if the probe is on a different board.


## 2026.8.32

- **You can now delete a channel** from the channel setup page. The confirmation tells you how many
  gates go with it.


## 2026.8.31

- **A bay's supply or drain position can now only be used by one gate.** Positions already taken show
  as "in use" and are refused if sent anyway, so two gates cannot claim the same one and the water
  path cannot be made to loop back on itself.
- **Setting up a dual gate now asks which bay it drains FROM and which it supplies INTO**, instead of
  leaving you to pick the roles. A dual gate is always one of each.
- Paddocks you have disabled no longer appear when choosing a bay for a gate.


## 2026.8.30

- **Fixed: the Sync now button disappeared once you had imported every bay** — which is exactly when
  you go and draw more in Farm. It is always available now.


## 2026.8.29

- **Paddocks you have disabled no longer appear in the Water Chain**, so the list of things still to
  connect only shows paddocks you are actually irrigating.


## 2026.8.28

- **Fixed: the Water Chain page did not show gates set up with the new gate tools**, so a paddock you
  had wired up correctly still appeared as separate bays.


## 2026.8.27

- **The paddock panel on the Paddocks page now sits above the map** as a proper floating panel, and
  no longer disappears when you zoom out. The map fills the screen behind it.


## 2026.8.26

- **Deleting a gate now frees its board**, so it can be assigned to another gate straight away.
- A board attached to a gate you have placed but not yet set up is also treated as in use, so it
  cannot be given to two gates by mistake.


## 2026.8.25

- **The map now stays where you put it.** Moving a gate, saving one or importing a bay no longer
  zooms back out to the whole farm.


## 2026.8.24

- **Further fix for the paddock panel disappearing**, which was still happening when zooming out.


## 2026.8.23

- **Fixed: the paddock panel on the Paddocks page could disappear**, showing itself only while you
  zoomed or dragged the map.


## 2026.8.22

- **Bay lists now show the paddock as well as the bay**, so several bays called B-01 in different
  paddocks can be told apart when you are setting up a gate.


## 2026.8.21

- **Adding a gate is now two clicks**: say whether it is single or dual, then click where it goes.
  You can place every gate on the farm this way and come back later to say which bays each one serves
  and which board runs it.
- **Click any gate on the map to set it up or change it**, and drag it to move it.
- Gates are colour-coded: blue square for supply, red circle for drain, blue circle for a gate that
  drains one bay into the next, and pink for one you have not set up yet.
- **Note:** placing a bay's level sensor has temporarily lost its button while the gate tools were
  rebuilt. Sensors already placed are unaffected.


## 2026.8.20

- **Gates can now be put on the map before you know anything else about them.** Say whether the gate
  is single or dual, drop it on the map, and move on — you can walk the whole farm placing gates and
  come back later to say which bays each one serves and which board runs it.
- A gate you have not set up yet shows as its own colour on the map, so it is obvious what still
  needs doing. Once set up: blue square for supply, red circle for drain, blue circle for a gate that
  drains one bay into the next.
- **A gate's type is fixed when you place it.** A single gate does not become a dual one — if the
  structure really changed, that is a new gate.
- **PWM now works out the bay order itself.** When you tell it a gate drains one bay into the next,
  that already says which bay comes first, so you no longer keep a separate running order. The last
  bay is worked out the same way: a bay whose drain does not feed another bay is the last one.


## 2026.8.19

- **Fixed: clicking a bay did not open it properly**, which left the Add Gate button doing nothing.
  Introduced in the previous version when the bay shape controls were removed.


## 2026.8.18

- **Placing a gate now works anywhere on the map**, including on top of a bay. Previously the click
  only registered if you found a spot outside the bays.
- **Bays are set up in Farm, not here.** The bay name, redraw and split controls have been removed
  from the Paddocks page — draw and name your bays on the Farm map and they come through. On this
  screen you place and move gates and assign their devices.
- **A board that is already in use is no longer offered** when you pick a device, so the same board
  cannot end up running two gates by accident. The gate you are editing still shows its own board.


## 2026.8.17

- **A gate between two bays is now added once, as one gate.** Tell PWM it is shared, name the two
  bays and which position it holds on each side — for example the drain of one bay and the supply of
  the next — and it is created on both. The position numbers do not have to match.
- **One board, assigned once.** Assign or change the device from either bay and the other side
  follows, because it is the same physical gate. Removing it removes it from both bays.
- **PWM now uses the positions you state, instead of working them out.** If you say a gate is drain
  #2, it stays drain #2. Previously it could be moved into the first position on its own, which meant
  automation could end up running a different gate from the one you set up.
- Because of that, deleting a bay's first gate no longer moves the second one up into its place. The
  bay will show that it has no gate in the first position, so you can put the one you want there.
- You can now give a gate its name and its device while you place it on the map.


## 2026.8.16

- **Adding a gate now works straight from a bay.** Previously you had to click the paddock first, which
  became fiddly once its bays were drawn in and covered it.
- **A bay's name now comes from Farm and can't be edited here.** Renaming it in PWM used to appear to
  work and then revert on the next sync. Rename the bay in Farm and it comes through.


## 2026.8.15

- **Bays you draw in Farm now stay up to date in PWM.** Previously a bay was copied across once
  at import and never updated, so a bay you reshaped in Farm kept its old outline here. PWM now
  re-checks with Farm every 30 minutes, and there is a **Sync now** button on the Paddocks page
  if you have just finished drawing.
- Only the bay's **outline and name** come across. Your pump, gate, sensor and automation
  settings are yours and are never changed by a sync, and enabling a paddock stays your decision.
- **Bays are still imported by you, one at a time.** Nothing appears in PWM on its own.
- If a bay is deleted or re-split in Farm, PWM tells you instead of quietly dropping it — the bay
  keeps working, and you can **Unbind** it to take over its outline here (which also lets you
  redraw it) or remove it yourself.
- The Paddocks page no longer waits on Farm to draw — it uses PWM's own stored copy and tells you
  when it was last synced.


## 2026.8.14

- A newly installed add-on now stays on its activation screen until you enter your licence.
  Nothing changes for an add-on you are already using: once it has been activated it keeps
  working, and a later licence change or renewal will not lock you out of your own data.
