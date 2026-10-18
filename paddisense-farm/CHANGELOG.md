# PaddiSense Farm — What's New

## 2026.10.111

- **Varieties:** the list you keep under Settings → Varieties is now the one every screen offers. Your existing varieties are copied in once.

## 2026.10.110

- **Security:** an old built-in login with a well-known password is replaced automatically with a private one.

## 2026.10.109

- **Safer restore:** only encrypted PaddiSense backups can be restored; a plain database file is refused.

## 2026.10.108

- **Clearer access message:** someone without access to Farm now sees a proper page saying so, instead of a line of code.

## 2026.10.107

- **Security updates:** shared security components refreshed (who counts as Home Assistant's own proxy; log redaction).

## 2026.10.106

- **No surprise sign-outs:** removed an old setting meant to restart the add-on every 10,000 requests (which would have signed everyone out). It never actually triggered, so nothing changes day to day.

## 2026.10.105

- **Steadier and safer:** a stuck database query can no longer tie up the app, sign-in attempts are limited per device as well as per
  user, and viewers no longer trigger outside connections (machine data, GSM test) — those need an operator.

## 2026.10.104

- **Restore checks:** a valid backup that was wrongly refused now restores, and two more ways to slip a command past the check are closed.

## 2026.10.103

- **Safer connection codes:** a connection code that was altered after your PaddiSense administrator issued it is now refused.

## 2026.10.102

- **Security hardening:** several small fixes to how names and settings are displayed and stored.

## 2026.10.101

- **"Back up now" backups are now encrypted and kept** in Home Assistant's backups folder, so they survive add-on updates.
- **Security hardening:** stored satellite-data credentials are encrypted, and a few admin-only actions are tightened.

## 2026.10.100

- **Security updates.** The add-on now picks up the latest operating-system security fixes when it is built.

## 2026.10.99

- **Safer restores.** The check that inspects a backup before it is restored closes two more ways a tampered backup could slip a command through.

## 2026.10.98

- **Import hub fixes.** Opening a staged file on a paddock that already has crop zones now shows those zones instead of failing, and a
  sowing import over an existing zone no longer reports an error after it has actually worked.

## 2026.10.97

- **Easier to read on the phone.** When recording an event on the phone, the chosen date now shows white on solid green, **Cancel**
  is a solid red button, and a chosen event type is white on its colour — no more pale colour on pale colour.

## 2026.10.96

- **All bays / All crops on the farm.** In the map's tree, each farm now has **All bays** and **All crops** ticks: one tick shows every
  paddock's bays (or crop zones) on the map — with their labels, if Labels → Bays / Crop zones is on. Untick to hide them all again.

## 2026.10.95

- **Resize bays can now turn the split.** Besides the middle ◆ (slide), there is a ◆ at each end of the line: drag one to swing that end
  while the other stays put. The gap between the bays stays the same width all the way along. Save or Cancel as before.

## 2026.10.94

- **Fixed: Resize bays showed no handle** after you clicked the second bay, and Split did not become ready when you clicked a bay. Both
  now work from the bay you click.

## 2026.10.93

- **Resize bays.** Drew a split in the wrong place? On the map (Bays), click one of the two bays, press **Resize bays**, then click the
  bay beside it. Drag the ◆ handle: the shared side slides, the neighbouring bay's edge follows, and the gap between them stays the
  same — you see both new shapes and their areas as you drag. **Save** to keep it, **Cancel** to leave the bays as they were. The bays
  keep their names and history, and PWM follows on its next sync.

## 2026.10.92

- **"→ Bay" (a bay from the whole paddock) is now one time per paddock.** Once a paddock has a bay, the button is gone and Farm will not make
  another copy — so a double tap can no longer make duplicate bays. To start again, delete the paddock's bays first.
- **Split tells you what to click.** If you press Split with nothing selected, Draw split line waits and says "Click the bay to split first";
  click the bay on the map and it is ready.

## 2026.10.91

Housekeeping only — nothing you will see changes.

## 2026.10.90

**Staying signed in:** a brief network hiccup on the box could send you to the login page when opening Farm from Home Assistant. Farm now rides through it.

## 2026.10.89

**Home screen:** the Farm home screen's tiles are now the same size and layout as every other PaddiSense add-on — one tile per row on a phone.

## 2026.10.88

**Reliability:** an unusual web request can no longer make Farm pause while it writes its log.

## 2026.10.87

**Safer database restore.** A backup file is checked before it is restored, and a file that has been tampered with is refused with a clear message.

## 2026.10.86

**Safer handling of typed-in text.** Names and readings you or your team enter are now always shown as plain text on the event, record and Real Time Rice pages.

**Trial planner gives a clear message** when the run range is too wide to work out, instead of an error.

## 2026.10.85

**Import Hub lists your newest jobs first.** Staged machine jobs are now in date order, with the most recent job at the top.

**Buttons and fields on your phone follow the new PaddiSense look** — larger, easier to tap.

## 2026.10.84

**Real Time Rice keeps up with the season.** Predictions now refresh by themselves every morning at 6:30, show the crops sown this season (and keep showing them after New Year), and a refresh can no longer blank your cards if the file has nothing new. The season bar and region tabs now appear.

## 2026.10.83

**Satellite imagery that keeps up with the crop.** Farm now checks for a new satellite pass every day, keeps the last two months of clear pictures for each cropped paddock, and skips cloudy ones. On your phone, tap a paddock, choose Imagery, and tap a date to see that capture on the map. If there is no imagery, the screen now tells you why.

## 2026.10.82

**Varieties now belong to a crop.** In Config → Varieties, type the variety and pick its crop from your crop list. It then shows under that crop when you record a sowing or build a crop plan. Any variety you added before is listed as "no crop yet" — pick its crop once and it moves across.

## 2026.10.81

**Imports land on the right paddock.** When you import soil tests or events, a row is now attached to a paddock only if its name matches exactly, or matches just one paddock. If it could mean more than one (for example "SW1" when you have SW10 and SW11), it is saved without a paddock and the import report tells you, instead of guessing.

## 2026.10.80

**Housekeeping inside.** Unused code removed. No change on screen.

## 2026.10.79

**Buttons match your access.** Someone signed in as an Operator no longer sees buttons only a manager or the farm owner can use (they used to appear and then refuse). Nothing changes for the farm owner.

## 2026.10.78

**Housekeeping inside.** Unused code removed. No change on screen.

## 2026.10.77

**Housekeeping inside.** A safety check on how paddocks follow changes made in GSM. No change on screen.

## 2026.10.76

**Drawing a paddock over one you already have is stopped.** Farm now tells you which paddock already holds that ground, so you edit it instead of ending up with two.

## 2026.10.75

**Housekeeping inside.** A safety check on how paddocks are linked to GSM records. No change on screen.

## 2026.10.74

**Housekeeping inside.** No change on screen.

## 2026.10.73

**Security update underneath.** The system software this add-on is built on is refreshed with current security fixes. Nothing changes on screen.

## 2026.10.72

**Import Hub tidy-up.**
- Tiny slivers of machine data outside every paddock (under 0.1 ha) are set aside automatically. You can see them under Status → Dismissed and restore any you want.
- Two machine jobs in the same paddock that are really one job can be merged, and unmerged.
- The job card now asks the same things as the event recorder: fertiliser no longer asks for water rate, and products are picked from your product list with their unit.
- The card sits beside the map on a wide screen, with several boxes per row.
- Dismissed items can be restored. An item already imported cannot be imported twice by mistake.

## 2026.10.71

**A "Check" row on the paddock matching page can now be decided.** Press Check to see the machine field and the paddock it overlaps on the map, then choose Make a paddock or Dismiss. A dismissed field is listed under the table, where you can restore it.

## 2026.10.70

**The "ready to send to GSM" list now shows only confirmed events.** Events you dismissed, and machine records still waiting for you to confirm, no longer appear there or count as waiting.

## 2026.10.69

**Your crop plan can now feed Planner.** Nothing changes on screen in Farm. With this version, PaddiSense Planner (2026.10.6 or later) can read the crop plans you make here and fill its paddock plan from them.

## 2026.10.68

**Crop plan: make a planned crop the real crop zone.** Click a planned area and press "Make crop 1 the crop zone": Farm creates this season's crop zone with the same shape, crop and variety, so nothing is drawn twice. When the second crop goes in, press "Make crop 2 the crop zone" — it takes over the ground from crop 1. The plan keeps its record of what was planned and when each crop was made, so planned and actual can be compared. Only the plan for the season can be made into crop zones, not a scenario.

## 2026.10.67

**Crop plan.** A new Crop plan tab on the map lets you plan what each piece of ground will grow in a season. Click a bay, crop zone or paddock and press → Plan (or draw an area), then choose crop 1 and how many months it runs, and — if you grow two crops in the year — crop 2 and its months. Crop 1 starts in May; crop 2 starts when crop 1 finishes; either can be Fallow; anything left to the end of April is fallow. Varieties come from your variety list. Planned areas show on the map in one colour per crop, labelled with their months (for example "Rice (May-Jan) → Wheat (Feb-Apr)"), and in the tree under each paddock's Crop plan group.

You can keep more than one plan for a season (for example "Plan A" and "Dry year"), choose which one is the plan, and copy a plan to next season as a starting point. Planned areas have the same tools as bays and crop zones: edit shape, split, cut, buffer, merge and delete.

## 2026.10.66

**Trial plans in the tree.** A paddock's saved trial plans now appear in the tree under that paddock, in a new "Crop plan" group. Tick a plan to show its block on the map without opening it — several can be shown together and printed. Click a plan to open it in the Trial planner. The planner has a Paddock picker so you choose which paddock a plan belongs to; a new plan starts on the paddock you have selected. Closing the planner leaves a saved plan's block on the map, ticked in the tree.

## 2026.10.65

**Trial planner: choose fewer passes for a lot.** After "Work out run length", each lot's passes are now a box you can change. If a lot's last pass would leave almost no seed spare, turn it down by one to be safe: the seed left, the totals and the block on the map all update. You cannot go above what the seed allows. Clear the box to go back to the full number. Your choices are saved with the plan.

## 2026.10.64

**Trial planner: move the block and line it up.** Drag the block on the map to move it. "Match a line": click two points along a line (an AB line, a bank, last season's rows) and the block takes that heading. "Match an edge": click a paddock or bay boundary and the block lines up with it. You can also type the AB heading in degrees, and tick "Fill passes to the left" if the planter works the other way across the block. Press Save to keep where it sits.

**Measure and Trial planner are on the tool bar.** Both are now worded buttons at the right-hand end of the map's tool bar (the row with Split, Merge and the other tools). Press Measure to show Line, Path, Radius, Area and Clear.

## 2026.10.63

**Trial planner.** Press ▦ on the map to plan where trial seed lots will be sown. Enter the planter's application width and swath width, the sowing rate, and each seed lot's ID, variety and kilograms — or paste the rows straight from Excel. Press "Work out run length" and Farm lists the run lengths that leave the least seed over across all lots, with the passes each lot gets and what is left. Pick one (or type your own length), then "Place on map": click the start corner and a second point along the first run. Each bag lot is drawn as its own labelled strip. Save the plan to open it again later.

## 2026.10.62

**Measure on the map.** Press 📏 on the map (under the zoom buttons) and pick a tool: **Line** (click the start and the end), **Path** (click each corner — click the last point again to finish), **Radius** (click the centre, then the edge) or **Area** (click each corner — click the first point again to close it). The distance or area shows as you move, and stays on the map when you finish. Click a measurement to remove it, or press Clear to remove them all. Measurements are not saved.

## 2026.10.61

**Print maps.** Press 🖨 on the map: choose A4 or A3, portrait or landscape, give it a title, and drag the dashed frame over the area you want. The print shows the layers you have turned on, your labels where you placed them, a legend, a scale bar, the scale (1:N) and a north arrow. Use Print / Save as PDF to print it or keep it as a PDF.

## 2026.10.60

**Move, turn and hide map labels.** In 🏷 Labels, press "Move / rotate labels": drag any label to where you want it, or click it to rotate it, change its size, hide it, or put it back. Your changes are kept for the farm and will be used when maps are printed.

## 2026.10.59

**Labels for every map layer.** The new 🏷 Labels button lists every layer — paddocks, bays, crop zones, events, each infrastructure type and each land-cover type — and lets you choose up to two things to show on each (name, area, crop, date, product…) and the size. Your choice is saved for the farm, not just this browser.

## 2026.10.58

**Sowing makes its own crop zone.** When a sowing comes with the area actually sown (from the machine, or drawn), Farm now creates a crop zone for just that ground and trims the paddock's other zones to match — it no longer marks the whole paddock as sown.

**Edit or delete events on the map.** Click an event: the right panel now has Edit attributes, Edit boundary, Delete and Close. The event's area clears from the map when you close it or pick something else.

**Import Hub:** the map and tools now open right under the file you click, instead of at the bottom of the page.

## 2026.10.57

**Bays and crop zones on the phone map.** Turn on Bays (or Crops) and tap a bay: the panel shows that bay's size, its farm and paddock, and only the events recorded on that bay. Crop zones work the same way.

## 2026.10.56

**Access follows Core.** What a person can change here now matches the role you gave them on Core's access page. An Operator can no longer use manager-only actions. A box with no access set up keeps full rights.

## 2026.10.55

**Security.** On your farm, PaddiSense trusts only the licence key it was built with. Another add-on on the same box can no longer add one.

## 2026.10.54

**Editing a bay, crop zone or paddock works again.** On the map, Edit now shows the corner points so you can drag them, then Save.
A bay made of two separate pieces says so, instead of doing nothing.

## 2026.10.53

- Import Hub: the map preview no longer errors when it can't show existing crop zones; it simply shows none.

## 2026.10.52

- Behind the scenes: Farm writes a short, read-only health summary that PaddiSense's monitoring can read (no farm data leaves the box).

## 2026.10.51

- Removed leftover references to SugarSense, which is no longer part of PaddiSense.

## 2026.10.50

- Behind the scenes: Farm no longer copies database dumps to an off-site repository each night. That job has been retired.

## 2026.10.49

- On a phone, Farm's home screen has the same top bar as every other page. Its MAIN button takes you straight back to the PaddiSense start page, with no reload.
- Home screen tiles are taller and line up in even rows.

## 2026.10.48

- The event form on the map fits a phone screen: every event type is readable, with bigger buttons and fields.
- Behind the scenes, the phone Record Event wizard is now shared with GSM's field app; it works exactly as before.

## 2026.10.47

- Events sent to GSM now carry an id that is unique across every farm, so one farm's event can never be mistaken for another's.

## 2026.10.46

- A CNH machine job now opens in the same event form you use to record an event — the same fields for each type (for a cultivation, the method such as Disc; for a chemical, every product with its rate, water rate and applicator), filled in from the machine where it can. Chemicals and nutrients you record on the map now keep their product and rate on the event itself.

## 2026.10.45

- Each CNH job's paddock now shows only the days the machine worked that paddock.

## 2026.10.44

- Staged CNH jobs now show the days they were worked and the machine. An imported machine job is an ordinary Farm event you can edit — the machine's own data stays untouched.

## 2026.10.43

- Reviewed CNH machine jobs can now be imported. Each becomes a normal Farm event on its paddock — in the right season in the tree, with its worked area, your product and rate, and it goes to GSM like any event you record. If you cleaned the shape first, the cleaned shape is what is saved.

## 2026.10.42

- CNH jobs are joined back together (Case splits them into 30-minute files) and cut along your paddock boundaries: the review list shows one item per machine, task and paddock. Work outside every paddock is its own item to discard or attach. Files where the implement was never down are set aside as "no work recorded". Importing machine jobs comes with the next update.

## 2026.10.41

- Bays sent from GSM are now saved in Farm — they were being skipped.

## 2026.10.40

- Fetch + stage CNH data also records CNH's own operation list, so split jobs can be joined back together correctly.

## 2026.10.39

- Staged CNH jobs now show where the machine actually worked (its working track and width), not a guessed paddock outline.

## 2026.10.38

- Farm now keeps a permanent record of every CNH file and job it has fetched. Pressing **Fetch + stage CNH data** again never brings back a job you have already staged, imported or dismissed.

## 2026.10.37

- Import hub: **Fetch + stage CNH data** downloads your CNH machine job files since the start of the current season and puts each job in the review queue. Nothing reaches your paddocks until you import it.

## 2026.10.36

- Check job data now works when your CNH login has not had a company picked — it uses your login's company, the same as the field sync.

## 2026.10.35

- Machine data → CNH has a **Check job data** button: it asks CNH which machine jobs and files it holds for your login over the last 12 months, by machine and file type, and reads one sample file. Nothing is saved.

## 2026.10.34

- Opening the machine paddocks page (BM01) no longer freezes the rest of Farm while it works out the matches.

## 2026.10.33

- Drawing a crop zone over one of your own zones replaces it, whatever your role; zones from Case or John Deere are still protected.

## 2026.10.32

- Drawing a crop zone over a zone from Case or John Deere is refused instead of deleting it; removing a whole zone by drawing over it needs a manager.

## 2026.10.31

- An event you dismiss, or one still waiting for your confirmation, is no longer sent to GSM; the "not yet sent" count now matches what will be sent.

## 2026.10.30

- Removing a field in John Deere no longer risks removing a different paddock whose number matches the field's name.

## 2026.10.29

- Recording an event: the Operator is now filled in with the person who is logged in.

## 2026.10.28

- Crop zones never overlap: "Bays → Crop" now splits the crop zone that is there into one zone per bay, and drawing a zone takes its ground from the zone underneath.
- A split with a 0 m bank now cuts exactly along the line.
- New crop zones go into the active season, and events you record go into their date's season, so they show under that year in the tree.
- The selected paddock, bay or crop zone is highlighted in yellow, and crop zones in one paddock have different colours.
- The chemical list shows only chemicals and the nutrient list only nutrients.

## 2026.10.27

- Map: the panel on the right now matches GSM — tabs for each event type with this season's events, and buttons for Edit boundary, Edit farm, Record event, Edit attributes and Delete. Bays and crop zones use the same panel.
- Map: clicking a bay or crop zone now selects its paddock in the tree and zooms to it; clicking a farm in the tree zooms to that farm.
- Seasons: choose which seasons show in the map tree; a crop zone can be moved to another season; new crop zones made from a paddock or its bays go into the current season.

## 2026.10.26

- Farm and owner names now come from your machine data (CNH / John Deere) by the provider's own farm and grower, and are updated on every sync. Paddocks are no longer put on a farm just because it is nearby.
- Names that come from CNH / John Deere are changed there, not in Farm — Farm says "Edit in CNH". If the provider is disconnected you can edit them; after you reconnect and sync, the Match page lists every name that differs, with a button to take the machine's name.
- A machine sync that cannot reach CNH / John Deere now says so and changes nothing (it used to report "complete").
- The map's farm tree refreshes when you come back to it after a sync.

## 2026.10.25

- Health check: the public status reply now carries only what the fleet reads.

## 2026.10.24

- Paddock matching: every screen that links machine fields to paddocks now makes the same decision in the same place. Nothing changes in what you see; a sync, Accept, Accept all and Merge all record where each paddock is up to.

## 2026.10.23

- Map: click a paddock, bay or crop zone and press **Record event** — the full event form opens on the left (all eight event types, crop stage included); click more paddocks, bays or zones on the map to add them. Save brings the tree back.
- Events list: "view on map" now opens the paddock and the event.

## 2026.10.22

- Sending events to GSM: the bay or crop zone an event was on now goes with it, and so do the crop stage and the method fields that were left behind.

## 2026.10.21

- Map: labels are white on a dark outline and a bit bigger — easy to read on the satellite image.
- Map: label all paddocks at once (name, or name + hectares) from the tree bar; crop zones can carry labels like bays.
- Map: **Bays → Crops** makes a crop zone for every bay of a paddock — no re-splitting.
- Map tree: opening a paddock's bays, crops or events now uses the whole panel, with a breadcrumb to step back.

## 2026.10.20

- Matching page: a paddock GSM doesn't have is only sent when you press **Add to GSM** — nothing is sent without your say-so.
- Your farm takes the name your machine data gives it (e.g. "Old Coree - 7829") after the next machine sync.

## 2026.10.19

On an Android tablet you now get the full desktop pages instead of the phone layout. iPads and phones are unchanged.

## 2026.10.18

- Matching page, GSM column: **Matched ✓** when GSM holds exactly what Farm holds. Otherwise choose **Replace GSM** (send yours, in one batch
  with Push to GSM) or **Replace Core** (take GSM's version).

## 2026.10.17

- Sending to GSM when GSM is busy no longer fails with an authentication error — Farm retries properly.

## 2026.10.16

- Consolidate: the Confirm button and the Retire list are always on screen; the list is in name order.

## 2026.10.15

- Case sync is about twice as fast: it no longer downloads your whole Case account twice.

## 2026.10.14

- **Consolidate** never removes a paddock unless you tick it: paddocks your machine data doesn't cover are listed for you to Keep or Retire.
- A paddock whose machine field has moved to different ground is no longer updated automatically — it waits for you on the Matching page.

## 2026.10.13

- Matching page: **Consolidate** makes Farm's paddocks match your machine data exactly — one paddock per machine field. You see the whole
  change first (which paddocks are kept, merged or retired, and where their records move) and confirm once.

## 2026.10.12

- Events → GSM: **Test Connection** now really asks GSM, and tells you plainly if GSM did not answer or refused (and why).

## 2026.10.11

- One set of bays per paddock: where you have drawn your own bays, bays pulled from GSM are kept but hidden.
- A paddock that GSM has turned into a bay of a bigger paddock now joins that paddock in Farm (its records move with it).

## 2026.10.10

- Matching page: **Accept all** applies every Case / John Deere update at once — a name swap (e.g. K12 ↔ K13) lands in one go. After that,
  each Case sync keeps your paddocks up to date automatically.
- Each row fits on one line again.
- Merging paddocks is paused until bays are handled (coming next).

## 2026.10.9

- Matching page: a banner shows whether your paddocks and GSM match 100 % after GSM accepts — and, if not, which paddock differs and why.
- New paddocks join the farm they sit on, and Case's grower name fills in the farm owner when it was blank.

## 2026.10.8

- Matching page: when one Case field covers several of your paddocks, **Merges** combines them into one paddock with the Case shape and name;
  the old ones are kept in history. A field that is a new piece of a split paddock shows **Add (split from …)**.

## 2026.10.7

- The matching page lines up your Case / John Deere fields with your paddocks by where they are on the ground, not by name. Each row is one
  paddock, showing Update, In Core, Add to Core, Merges (several paddocks) or Check (needs you).
- Updating a paddock from Case takes Case's shape and name and keeps its history.
- Sync Now shows progress and finishes cleanly instead of looking stuck.

## 2026.10.6

- Merging paddocks now keeps the merged paddock linked to GSM, so GSM updates its record instead of adding a new one.
- The matching page no longer shows a Delete button on matched paddocks.

## 2026.10.5

- Map: the **Merge** button works. Pick paddocks, name the result and choose which one to keep. The others are hidden, not deleted.
- Matching page: each matched paddock asks one question, **Send to GSM** or **Keep GSM's**. Push all skips paddocks set to Keep GSM's.

## 2026.10.4

- Security: a library Farm uses for web requests updated to fix three published vulnerabilities. No visible change.

## 2026.10.3

- Internal: Farm's security alerts are now delivered to the PaddiSense operator. No visible change.

## 2026.10.2

- Internal: if PaddiSense cannot accept a security alert from Farm, Farm now records that it was refused. No visible change.

## 2026.10.1

- Internal: Farm's daily security summary and security alerts are now handed off correctly — before, some were silently never sent. No visible change.

## 2026.9.49

- A Farm Owner or PaddiSense Administrator can always open Farm, exactly as PaddiSense Core allows — even if "all modules" was not ticked for them.
- A malformed access update from Core is ignored and your current access settings stay in place.

## 2026.9.48

- Knowledge Bank packs are only installed when their checksum matches, and nothing outside the box can push content to it.

## 2026.9.47

- Internal: Farm and GSM now use the same version of the library that checks boundaries. No visible change.

## 2026.9.46

- If you re-link a paddock to GSM after Farm has suggested retiring it, that out-of-date suggestion is removed and can no longer hide the paddock.
- Farm checks every boundary it receives from, or sends to, GSM against one shared format. A malformed answer from GSM changes nothing, and a paddock whose shape can't be sent is named on the Boundary Manager.
- Farm refuses boundaries from a different GSM than the one your paddocks are linked to, so your links can't be scrambled.
- GSM can no longer change your paddocks without you pressing Pull GSM.
- After Pull Boundaries on the GSM settings page, the connection status now refreshes.

## 2026.9.45

- Pulling from GSM no longer hides a paddock by itself. If GSM stops holding one of your paddocks, the Boundary Manager lists it and you choose Retire or Keep.

## 2026.9.44

**Your paddocks stay matched to GSM when GSM tidies its records.** If GSM merges or removes a paddock you are linked to, Farm now follows it to the right record on your next pull instead of losing the match. If a paddock moves to another owner in GSM, Farm hides it but keeps all its history, and brings the same paddock back if it returns. Farm also flags any paddock whose shape no longer matches its GSM record so it can be checked. On the Match page, Remove now takes a paddock out of Core without deleting it, and Pull GSM tells you why it failed. Crop zones can now be split into several crops within a paddock, with or without a bank between them, and each zone shows in the map tree under its paddock; while drawing, the map shows the line length and area as you go; each group in the tree has an "all on / off" tick. On the map, drag the edge between the tree and the map to make the tree wider or narrower, and event names now show first in the tree.

## 2026.9.43

**Your bays now go to GSM and come back, exactly as drawn.** When you push to GSM, each paddock's bays go with it, and bays GSM holds for your paddocks come back into Farm on the next pull. Each bay is matched by its own identity, never by its name.

## 2026.9.42

**The map tree now starts with the season.** Pick a season under your business and see its farms and paddocks, with that season's crop zones, yield, NDVI and events underneath. The tree is also larger and easier to read, with bigger arrows and a coloured square beside each layer that matches its colour on the map.

## 2026.9.41

**Your paddocks now stay matched to GSM by where they are, not what they are called.** When you pull from GSM, each GSM
paddock is matched to yours by its boundary, even when GSM uses different business, farm or paddock names, and the match is
remembered so it holds on the next sync. A paddock GSM holds twice now lines up once, with the extra GSM name shown beside
yours. Renaming a field in Case, merging or splitting paddocks, or removing a paddock from Core no longer breaks or moves the
match, and a sync never re-creates a paddock you have removed. GSM records that are only a part of one of your paddocks (such as SunRice's bay-level records) are listed under that paddock instead of as new paddocks, and any staged GSM row that should not be there can now be deleted from Machine Boundaries.

## 2026.9.40

**GSM paddocks now line up with your own paddocks by where they are on the ground.** When GSM calls your business or farms by different names than you use in Case, Machine Boundaries used to list the GSM paddocks as new. It now matches them to your existing paddocks by their boundaries, and will not create a second copy of a paddock you already have.

## 2026.9.39

**Farm now says clearly when its map database is incomplete.** If the database is missing the map extension Farm needs, the self-test shows it in red and says how to fix it, instead of pages failing with a server error.

## 2026.9.38

**The event wizard now offers the same products as your Store.** Adding products to an event on a
computer showed a different, much shorter list than the one on your phone — it was reading a local
list left over from setup rather than your Store catalogue. Both now read Store, so a product you
add in Store appears everywhere, with its application rate unit (L/ha, kg/ha).

If you create a product from inside the wizard it is still saved to this box only, and now says so
— add it in Store for it to appear for everyone.

## 2026.9.37

**Spray weather now follows the spray.** Recording a spray captured three weather readings that
were often the same one, taken at the wrong time of day — and on a spray you entered the next day
or later, always the same one. The box now looks up the weather for the actual start, middle and
end of your spray, from a station that measures temperature, wind and humidity, preferring your
own local station.

If no reading was taken near a part of the spray, that part is left blank and says why, instead of
filling in the nearest reading it could find — your record only shows conditions that were really
measured. A chemical event now asks how long the spray took, since the weather is captured across
it. Wind direction is shown as a compass point on the event summary card, and if a station has got
stuck reporting the same number, the capture says so.

## 2026.9.36

**A paddock is no longer filed against a guessed farm.** When a paddock had no farm yet, the box
matched it by name alone — and paddock names repeat across farms, so it could be attached to the
wrong one. It now only matches when the name points at a single farm, and otherwise leaves the
paddock for you to place.

## 2026.9.35

**Paddocks you send to GSM land on the right farm.** The box used to send only the farm's name, and
names repeat across farms, so a paddock could be filed against the wrong one. It now sends the
farm's GSM identifier as well.

## 2026.9.34

**Connecting a second GSM code no longer takes your box away from its grower.** Pasting a
connection code that belongs to a different grower used to replace your existing connection
silently. It is now refused, and the message names both, so you can disconnect deliberately if that
is what you meant. Re-connecting the same grower with a new code still works as before.

## 2026.9.33

**Each farm keeps its own region.** A sync with GSM used to put a single region on every farm that
did not have one yet, so farms in another district could be labelled wrongly. Each farm now takes
the region that came with it, and a region you have already set is never changed.

## 2026.9.32

**Your own farms are no longer removed by a GSM sync.** If you created a farm yourself and had not
drawn its paddocks yet, a sync with GSM could delete it. Only farms that came from GSM are tidied up
now; anything you made stays.

## 2026.9.31

**RTR history is filed under the right day.** Refreshing the RTR data recorded its history entry
using UTC rather than your own date, so a refresh done early in the morning was filed under
yesterday — and on New Year's Day, under last year. It now uses the same date as the paddock rows
in the same refresh.

## 2026.9.30

**Your saved screen preferences are now private to you.** Map layers, panel choices and similar
settings were stored against the device only, so another signed-in person using the same device id
could see or replace yours. They are now kept per person.

## 2026.9.29

- Internal cleanup: removed an unused leftover helper. No visible change.

## 2026.9.28

- Security update to a bundled library (no visible change).

## 2026.9.27

- On the Farm Map, tap an event in a paddock's carousel to see its full record — the same detail as the event you submitted.

## 2026.9.26

- Fixed: on the phone Farm Map, tapping a paddock now opens its detail sheet (it was closing itself instantly).
- The Farm Map top bar now toggles what you see: Paddocks, Bays, Crops and Imagery.

## 2026.9.25

- **Farm Map on your phone.** Tap a paddock and swipe through what happened there: every recorded event and every satellite image, newest first. Tap an image to see it full screen.

## 2026.9.24

- **Event review on your phone is now built for the phone.** One card per event, tap for details and weather, confirm or dismiss with a thumb. Bulk actions and GSM review stay on the iPad and desktop.
- **iPad gets the full desktop pages.**
- The Import Hub moves to iPad and desktop. Your phone home screen now shows Farm Map, Events, Real Time Rice and Config.

## 2026.9.23

- **Machine import dates match your day.** A task that a machine file stamps in UTC is now recorded on the day it happened here, not the day it was in Greenwich.
- The developer screenshot box has been removed from the home page.

## 2026.9.22

- **Buttons stay readable in a narrow browser window.** Action bars and dialog buttons now flow onto a second line instead of being squeezed.

## 2026.9.21

- **Blue primary buttons with white text.** Save and confirm buttons follow the shared theme's new primary colour, with readable white text everywhere.

## 2026.9.20

- **Shared button styles.** No visible change on its own.

## 2026.9.19

- **Theme dial.** Every colour now derives from fourteen base values in the shared theme. No visible change on its own.

## 2026.9.18

- **Delete and danger buttons are red with white text again, and pop-up messages use dark text on grey.** No behaviour changes.

## 2026.9.17

- **New PaddiSense palette: light grey pages, black text, blue highlights — and every surface is checked for readability.** Selected tabs and buttons show as white with a blue edge, buttons are grey, warnings and errors keep their colours as text and borders. Every card states its own text colour. No behaviour changes.

## 2026.9.16

**No change on grower boxes.** The developer-only daily copy job on the PaddiSense dev box now reports a failure when it has nothing it can send, instead of reporting success. Nothing on a grower's box runs this job.

## 2026.9.15

**No change on grower boxes.** A developer-only background job on the PaddiSense dev box (a daily copy of the dev databases) had stopped working after a security clean-up in August; it works again. Nothing on a grower's box runs this job.

## 2026.9.14

**Farm now keeps a history of paddock, bay and crop-zone boundary changes.** Nothing changes on screen yet; this release starts recording so that later versions can show a paddock as it was on any date.

## 2026.9.13

**The same blue Home button on every page.** The map, the Boundary Manager, the event wizard and the mobile recorder now use the same Home button as the rest of Farm.

## 2026.9.12

**Deleting a farm now shows you what is in it first.** Config → Farms → Delete lists every paddock on the farm, including hidden
ones that do not appear in the map tree, with their bays and events. To remove the farm and all of it, type the farm's name to
confirm. A farm with nothing in it deletes as before.

## 2026.9.11

**Map field panel tidied.** The Farm selector under "Edit attributes" now has its own space and label.

## 2026.9.10

**Bays now follow the ground when a paddock moves.** If a paddock's boundary changes (a rename or correction in
your machine system, a boundary update or import), the bays inside it now go with the paddock that actually
covers them, and a bay named after its paddock is renamed to match. Before, the map moved the paddock but the
bays stayed under the old name, and "→ Bay" drew the new bay in the old place. Any paddocks already affected are
fixed automatically the first time this version starts.
**Boundary Manager buttons no longer fail with "Staged field not found" after a sync.**

## 2026.9.9
**Typing on a phone no longer zooms the screen.** A few fields in the event recording wizard and Import Hub were slightly too
small, so phones zoomed in when you tapped them. They are now full size.
**Housekeeping.** A small internal security log that only ever grew is now tidied automatically.

## 2026.9.8

**When something doesn't save, Farm now tells you.** Around forty buttons — recording events, creating products and
applicators, deleting or confirming events, GSM sharing, imports, disconnecting providers, the settings Update and
Restart buttons — used to show "saved", "deleted" or "done" even when the save had been refused. They now show the
reason instead.

**Imports can no longer apply the wrong shape.** When importing a file with several products, a failed save could make
the next import use the previous product's field shape. The import now stops and tells you.

**Tidy-up on the farm map.** An unused menu button on phones that never did anything has been removed.

## 2026.9.7

**Times now show your local time.** Weather readings captured with a spray or event, and event start and end times, were
being saved in UTC (so a 1:40 pm spray showed as 3:40). They are now saved on your own clock. The daily machine-data sync,
the knowledge-pack refresh, backup file names and export file names also follow your local time now.

**Security fix.** A background logging component was hardened so an unusual web request cannot slow the add-on down.

## 2026.9.6

**Security fix.** A setting page used for troubleshooting knowledge packs could be made to read Farm's own
configuration files. It is now limited to administrators and can only read knowledge pack content.

**Safer updates.** Every database change Farm makes can now be undone or is clearly marked as one-way, and
this is tested. Nothing changes in how you use Farm.

## 2026.9.5

**See everything that has happened on a paddock.** On the Farm Map, tap a paddock and choose **View
events**. Every event on that paddock shows as a card, newest first, with a search box at the top. Tap a
card to see the full record: products and rates, the sprayer and its setup, the weather at the start,
middle and end of a spray, who recorded it, and any notes. Events recorded on a bay, a crop zone, or just
drawn on the map over the paddock are included too.

**Delete items from any Config list.** Products, Applicators, Crops and Seasons now have a Delete button
on each row, like Farms. If something is still in use (for example a season with events), Farm tells you
what is using it instead of deleting it.

## 2026.9.4

**Weather is captured on your spray and field records again.** Recording an event could save it with no
weather readings, without telling you. Farm now connects to the Weather add-on properly, so the readings
are filled in as before.

**Config lists: the Edit buttons work, and you can delete a farm.** On the Config page the Edit buttons on
the Farms, Crops, Seasons, Products and Applicators lists did nothing. They now open the item. Each farm
also has a Delete button. A farm that still has paddocks, events, bays or infrastructure will not be
deleted, and Farm tells you what is still attached to it.

**Record Events map (desktop): the street map loads again.** The street background on the desktop
Record Events page could show "403 Access blocked" squares instead of a map, because it came from a
free public map service that can refuse requests. It now uses the same map provider as the Farm Map,
which was not affected. Nothing to do on your side.

## 2026.9.3

**Security: the browser protections now apply to every response, including "please log in".**
The pages you use already carried the standard browser security headers; the short "not logged in"
and "redirect to login" replies did not. They now do. Nothing changes in how you use Farm.

## 2026.9.2

**Your business name and each farm's identity now come through the PaddiSense sync.** Paddocks synced
from PaddiSense used to arrive with no grower shown ("Grower: –") and farms were told apart by name
only, so two farms with the same name could be treated as one. Each synced farm now carries your
business as its grower and is identified by its PaddiSense farm record, not just its name — and your
existing farms pick that up on the next sync, nothing to redo. A paddock name is unique within a farm
only; the same name on two farms is two paddocks, as it should be.

## 2026.8.36

**Files you import are now included in your backups, and survive reinstalling the add-on.**
Boundary files, machine and task data, and soil tests you had imported were being kept somewhere
your box's backup could not reach. Nothing deleted them, so they were there day to day — but a
backup did not contain them, a restore could not bring them back, and removing and reinstalling
Farm wiped every file you had ever imported. They are now stored alongside your other backed-up
data, where all three of those work properly.

**Your existing files move themselves.** The first time Farm starts on this version it relocates
anything already imported, and it will not overwrite a newer copy. **You do not need to re-import
anything**, and there is nothing to set up.

## 2026.8.35

**Paddocks with the same name now sync to the right farm.** If you run more than one farm and
each has a paddock called (say) "4", a boundary sync from PaddiSense could attach the wrong
farm's paddock — or quietly create a duplicate — and still report the sync as successful. Each
paddock now matches only within its own farm, and a paddock the system cannot confidently place
is left alone and reported rather than guessed at. **If you have synced before, please check any
paddocks whose names repeat across farms** — existing links made by the old behaviour are not
changed automatically, because only you can say which one is correct.

**Sync problems now tell you what actually went wrong.** A refused connection used to always
suggest fetching a fresh connection code. That is the fix for some problems and useless for
others — if your business is not linked yet, a new code changes nothing. The message now names
the real cause and only sends you for a new code when a new code is the answer.

**Every page tells you if the box is not connected to PaddiSense.** A small, dismissable note,
so a box that has quietly dropped its connection no longer looks perfectly normal.

## 2026.8.27

**Internal tidy-up.** No visible changes.

## 2026.8.26

**Licence codes are now signature-checked everywhere.** The GSM enrolment card verifies
Admin's signature on a pasted licence code, same as the licence page — a tampered or
hand-made code is refused.

**Map: bays now follow the layer tree exactly.** Bays are drawn only by their layer
checkboxes; a newly drawn bay ticks itself and zooms into view, and unticking "Bays"
always clears them from the map.

## 2026.8.25

**The map tree stays where you left it.** Drawing a bay used to unfold the "Bays" branch of
*every* paddock in the tree, not just the one you were working in. Now only the branches you had
open stay open.

## 2026.8.24

**Quality assurance improvements — no user-visible changes.** The full automated test suite now
runs green, and additional security checks (personal-data log masking, map-label safety,
per-operator logins, signed licence authority) are verified on every release.

## 2026.8.23

**Internal consistency fix — no user-visible changes.** The signing helper used for Knowledge
Bank requests now shares the one canonical implementation, so all requests to your Grower
Services Manager are signed the same way.

## 2026.8.22

- **Recording a sowing event now offers the variety list on every device.** Varieties are
  filtered to the crop you pick, and the same list appears in the map recorder and the wizard,
  on desktop and mobile alike.
- Weather capture in the event wizard now reads from the on-box Weather addon correctly (it
  silently captured nothing before).

## 2026.8.21

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are
with a cryptographic token before they can change this add-on's licence or permissions.
Previously, being on the box's internal network was treated as sufficient proof.

## 2026.8.20

- When you push boundaries to your Grower Services Manager, Farm now checks that everything you
  sent actually arrived. If any are missing you'll be told how many and asked to send again,
  instead of the push simply looking successful.

## 2026.8.19

- Pushing boundaries to your Grower Services Manager now reports what actually happened. It
  previously said "0 created, 0 updated" even when the push had worked, which made a successful
  send look like it had done nothing. You now see how many boundaries were applied and how many are
  waiting to be accepted — and if the reply can't be read, it says so plainly instead of showing
  zeros.

## 2026.8.18

- Fixed the connection to your Grower Services Manager. Some requests were being rejected even
  though your connection code was correct.
