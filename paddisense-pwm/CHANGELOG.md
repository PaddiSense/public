# PaddiSense PWM — What's New


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
