# PaddiSense Farm — What's New

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
