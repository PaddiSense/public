# PaddiSense PWM — What's New


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
