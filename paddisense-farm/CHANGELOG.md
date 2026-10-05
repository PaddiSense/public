# PaddiSense Farm — What's New

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
