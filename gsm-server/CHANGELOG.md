# Grower Services Manager — What's New

> Plain-English release notes. The full technical changelog lives in the source repo
> (`CHANGELOG.md`); this is the version that ships in the catalog.

## 2026.9.42

**Farm reference repair.** The repair can now merge a farm that appears under two SAP numbers of the same grower, keeping both as owners. Carries everything in 2026.9.41.

## 2026.9.41

**Farm references with leading zeros.** A farm entered as `34319` and the same farm imported as `0034319` were two farms — one owned by you with no paddocks, one parked with all the boundaries. References are now always stored as 7 digits, a repair merges the existing twins, and the start-up check reports any that remain. **Sync ledger.** The paddock sync ledger on the business page now names every farm and paddock that was sent, when (local time), in which direction, and which farms of the business have no boundaries to send — and says plainly when two paddocks with the same name were both sent.

## 2026.9.40

**Self-check fix.** The new start-up check that a box's two business records agree no longer flags a box whose licence has simply been revoked. Carries everything from 2026.9.39.

## 2026.9.39

**Farm and paddock sync is now one set of rules for a grower with more than one business.** Which business a box belongs to is answered the same way whether the box is pulling boundaries or pushing them, and a box that is bound to two businesses is stopped with a message rather than guessed. The farms a box may sync are the farms its owner actively owns — a farm you co-own now syncs — and a licence with no farm list means that one business only. A pushed farm is matched by its id, and by name only when the name is unambiguous; a paddock name that appears on several farms is no longer matched to one at random. Every push is now recorded on the business page beside the pull record, so "which paddocks did the box send, and which were not placed" has an answer. Carries everything from 2026.9.38.

## 2026.9.38

**Farm records now use SunRice's own field names on every screen.** Wherever you add or edit a farm — the CRM, the map's edit panel, the boundary import — the fields are Farm Number, Farm Ref (7 digits, the farm's identity) and Farm Vendor (6 digits), and each is checked before it is saved. Previously two of these fields were labelled the wrong way round and could silently overwrite a farm's identity. A business without a SAP number must now be declared as such when it is created; a paddock edit or an import can no longer create a business by mistake.

## 2026.9.37

**Start-up no longer fails when two farm records share a Farm Ref.** A database holding duplicate farm records (left by an old import) stopped the app from starting at all. It now starts, the self-check shows how many duplicates there are, and a repair tool merges them. Carries everything from 2026.9.36.

## 2026.9.36

**Build fix only.** A test could not run on the build server; no change to the app. Carries everything from 2026.9.33 to 2026.9.35.

## 2026.9.35

**Startup self-check updated** for the renamed farm fields. No visible change.

## 2026.9.34

**Internal naming tidy-up.** The farm lists sent to Admin now name the owner's SAP number unambiguously. No visible change.

## 2026.9.33

**Farm records now use SunRice's own terms.** Each farm is identified by its Farm Ref (the number that never changes), shows its short Farm Number and Farm Vendor, and if a farm changes hands the previous owner is kept in its history instead of being overwritten. The SAP import shows any change of owner before you commit it.

## 2026.9.32
**Every farm in a business now syncs.** A business whose name was spelt two ways in the source could end up split in two, with some farms left out of the sync. Farms are now matched on the business number, and the affected farms are moved back where they belong.

## 2026.9.31

- Product rows on the tablet event screen now wrap onto a second line instead of squashing when the window is narrow.

## 2026.9.30

- Security update to a networking library used by the server. No change to how anything works.

## 2026.9.29

- Every action that changes data is now recorded in the audit log, including Real Time Rice imports and bug reports, which were previously missed. Primary (blue) buttons have white text again after the shared theme update.

## 2026.9.28

- Internal code-quality milestone: every function in the server now carries type annotations, and the checker enforces it. No visible change.

## 2026.9.27

- Internal code-quality work across the server. No visible change.

## 2026.9.26

- Internal code-quality work on the admin pages and database helpers. No visible change.

## 2026.9.25

- Internal code-quality work across the server modules. No visible change.

## 2026.9.24

- Internal code-quality work on the admin, portal, map and analysis modules. No visible change.

## 2026.9.23

- Internal code-quality work on the self-test module. No visible change.

## 2026.9.22

- **Shared button styles.** Buttons across the app now come from one shared definition. No visible change on its own.

## 2026.9.21

- **Theme dial.** The shared theme now derives every colour from fourteen base values, so a change to the greys, the text inks or what blue, green, red, pink and amber mean flows through every page. No visible change on its own.

## 2026.9.20

- **Map layers, charts and pop-ups now follow the shared theme too.** Paddock outlines, event markers, crop and campaign colours, and the water and RTR charts take their colours from the one theme file at display time.

## 2026.9.19

- **Theme refinements:** delete and danger buttons are red with white text again, map labels are readable over imagery, and pop-up messages use dark text on their grey background. All colours still come from the one shared theme.

## 2026.9.18

- **Every page colour now follows the shared theme.** Sign-in hints, status pills, event dots and banners, and the import page's cancel button all take their colours from the one theme file, so a theme change reaches all of them.

## 2026.9.17

- **New PaddiSense palette: light grey pages, black text, blue highlights.** Every page follows it, and every surface/text pairing is now checked for readability automatically. Selected tabs and buttons show as white with a blue edge; buttons are grey; warnings and errors keep their colours as text and borders.

## 2026.9.16

- **Readability fixes across the map, hub, events and near-me pages.** Page text on the dark background is now white everywhere it should be, and every card states its own text colour, so nothing renders white-on-white or dark-on-dark after a theme change.

## 2026.9.15

- **Map page (GIS) colours now follow the shared PaddiSense theme.** Toolbars, menus, banners and buttons on the map page take their colours from one place, so a theme change reaches them. No behaviour changes.

## 2026.9.14

- **Security: the map's "Print" export now requires you to be signed in to the map.** Previously the PDF generator could be called without a session. Nothing else changes for users.

## 2026.9.13

- **Fixed: the "Link grower" row on a business page now fits a narrow browser window.** Its two drop-downs and the Link button flow onto a second line instead of being squeezed together when the window is not full width.

## 2026.9.12

- **Scheduled jobs now run on the box's local time.** The nightly backup, security scan and data cleanup are timed by the box's local clock instead of UTC, so they fire at the intended local hour year-round — previously they drifted an hour over daylight saving, and the "3 am" cleanup actually ran at 1 pm. Backups are also named for the local date.

## 2026.9.11

- **Fixed: map paddock and campaign actions no longer look successful when they fail.** Creating a sampling campaign, saving a new paddock, or deleting a paddock now shows an error if the server rejects it, instead of silently appearing to have worked.

## 2026.9.10

- **Fixed: forms no longer default to yesterday's date first thing in the morning.** Creating a map event, marking a sample collected, or logging a paddock event before about 10 am pre-filled the previous day's date. The default now follows the box's local calendar.

## 2026.9.9

- **Housekeeping, no visible change.** When the add-on stops or restarts, its background jobs (nightly backup, security scan, status reports) now finish cleanly before the database connection closes.

## 2026.9.8

- **Housekeeping, no visible change.** On development boxes the add-on now registers its update sources with the read-only access key only, never the full-access one, so rotating the full-access key can't break add-on updates.

## 2026.9.7

- **Housekeeping, no visible change.** Tidier error message when a webhook URL is rejected, and a documented list of the credentials this add-on holds so staff know what needs rotating.

## 2026.9.6

- **Paddock sync ledger on each business.** CRM → a business → Growers now lists that grower box's recent boundary syncs: how many paddocks were sent, which were held back and why (no boundary drawn, farm not on the licence, farm belongs to another business), and which paddocks arrived or disappeared since the previous sync.

## 2026.9.5

- **New Audit log screen (admins).** Admin → Audit log shows every request GSM received — who sent it, what it was, and whether it was accepted or refused, with the reason for a refusal. Filter by sender, path, status or date. Useful for checking whether a grower's sync arrived.

## 2026.9.4

- **Map: adding a farm now needs its business.** If a farm is created on the map without choosing the business it belongs to, you now get a clear "missing field" message instead of an error. Farms are still normally created in CRM.
- Behind the scenes: log masking now also hides longer secret names, and the build is checked against the same tool versions the release uses.

## 2026.9.3
- **Regional permits now apply to every map action.** Staff whose login is limited to particular
  regions could previously open, edit, accept or reject some records outside those regions by
  addressing them directly. Every map endpoint now checks the region first; out-of-region
  requests are refused. Staff with unrestricted access are unaffected.

## 2026.9.2
- **Event photos are now kept somewhere an uninstall cannot delete.** Photos attached to events
  were stored inside the add-on's private data area, which is wiped if the add-on is ever
  removed and is not part of any backup. They now live in the Home Assistant config area, which
  survives reinstalls and is included in Home Assistant backups. Any photos already uploaded are
  moved across automatically the first time the add-on starts, and the built-in self-test now
  checks every photo is still where its record says it is.

## 2026.8.110
- **Fixed a health check that had been reporting a false failure.** The add-on's built-in
  self-test checks that every knowledge-base pack still has its file on disk. That check had a
  fault and could never run, so the self-test showed one failure on every start-up regardless of
  whether anything was actually wrong. The check now works, and if a pack ever does go missing it
  names which one.

## 2026.8.109
- Internal improvements — no user-visible changes.

## 2026.8.108
- Internal improvements — no user-visible changes.

## 2026.8.107

**A maintenance script bundled with the add-on no longer falls back to a well-known default
database password. No action needed.**
`pii-sweep.sh` is a diagnostic script that ships inside the add-on and is run by hand. If no
database password was configured, it used to quietly fall back to the factory default — a value
that is public knowledge — and connect with full administrator rights. It now stops with a clear
message naming the missing setting instead of connecting at all. Normal day-to-day use of GSM is
unaffected; this hardens a maintenance tool, not the running service.

## 2026.8.106

**Sending paddock boundaries to GSM now works from every connected box. No action needed.**
Boxes could receive boundaries from GSM but not send their own back — the attempt was
refused with a permissions error that looked like a connection problem. Sending was
governed by a per-licence setting that was fixed to "receive only" when the licence was
issued and could not be changed. That setting has been retired: any connected box may now
both send and receive. Re-connecting or re-issuing a licence is not required.

## 2026.8.93

**Licence Remove and Paste on the Deploy page work again. No action needed.**
Removing or pasting an add-on licence from GSM's Deploy page had started returning
"Forbidden" against up-to-date add-ons — a side effect of this month's security
hardening that removed network-position trust. The Deploy page now authenticates
those actions properly, so both buttons work as before.

## 2026.8.92

**The business list now shows every business. No action needed.**
Admin's grower pages were cutting the business picker off partway through the
alphabet once the South American dataset arrived — the list stopped around the
letter S. The server now returns the full list (all 566 and room to grow).
Also quietened a false "provisioning" alert that could email repeatedly on
boxes where PaddiSense Core manages the database roles — those boxes were
healthy; the alert now recognises that setup and stays silent.

## 2026.8.91

**Map labels that follow your search. No action needed.**
Three new switches at the top of the map's Explorer tree — Farm, Paddock and
Area (ha) — put names and sizes right on the map. They follow whatever you've
narrowed to: search down to a single farm and only that farm shows its
labels, instead of the whole map lighting up.

## 2026.8.90

**Boundary export page rebuilt. No action needed.**
The boundary export picker now matches the rest of the app (side navigation
included) and is much faster to use: a one-click **Select all**, ticking a
business ticks all its farms, a running "farms · paddocks selected" count, a
search box to filter big lists, and each farm row shows its farm number,
region, paddock count and hectares. Exactly the farms you tick are what
downloads. Every page also now spots when the addon has updated underneath an
open tab and offers a reload.

## 2026.8.89

**Map tree zoom at every level. No action needed.**
Clicking a business or a farm in the map tree now zooms straight to its
land, the same way clicking a paddock always has.

## 2026.8.88

**Imported boundaries protected from MapRice refreshes. No action needed.**
Boundaries loaded through the import wizard are now explicitly protected, so a
MapRice re-import can never overwrite them. Also silences the repeated
self-test alert email this gap was triggering.

## 2026.8.87

**Import safety fix + tidier map. Recommended update.**

- When a boundary file contained several farms with same-named paddocks
  (like "1" or "3"), one farm's boundaries could overwrite another's during
  a single import. Boundary matching now stays inside each paddock's own
  farm, so this can no longer happen.
- The map's browse tree now lists only farms that actually have mapped
  boundaries — farms that exist only as records (no geometry yet) no longer
  flood the tree. They remain visible in the CRM pages as before.

## 2026.8.86

**Boundary import: farm number decides where boundaries go. No action needed.**
When an imported boundary file names a farm number that GSM already knows,
the boundaries now attach to that farm and its real owner — even if the
file's owner column says something else (common in bulk exports where
everything is labelled with a head-office owner). The preview shows when
this happened, and anything ambiguous still asks instead of guessing.

## 2026.8.85

**Boundary import pages get the standard GSM look. No action needed.**
The boundary import wizard now uses the normal GSM navigation and layout
(the pages previously rendered bare, with overlapping text on some screens).
The match step shows only the fields for the mode you've chosen, and the
dry-run preview lists every value that will be imported for each paddock.

## 2026.8.84

**Boundary imports now read the file's own business & farm columns — and the SAP
Excel import keeps every column. No action needed.**

- When a boundary file (Shapefile/KML/GeoJSON) carries business and farm details,
  the import wizard now maps those columns (auto-detected, adjustable) and files
  each paddock under its OWN business and farm — matching by farm number, the same
  key the SAP spreadsheet uses, so spreadsheet-then-boundaries imports link up.
  Unknown businesses/farms are created; nothing is ever guessed between
  same-named entries; everything is previewed before commit as before.
- The SAP Excel import previously discarded the Farm Vendor column after preview
  and had no home for Farm Reg — both are now saved with the farm.
- Behind the scenes: fresh installs now set up the second (least-privilege)
  database role automatically.

## 2026.8.83

**File imports fixed — uploading boundaries and SAP spreadsheets works again. No action needed.**

- The boundary import (Shapefile/KML/GeoJSON) and the SAP Excel import both rejected every
  file chosen in the browser with "choose a file" even though you had chosen one. Uploads now
  go through and stage for preview as designed. (Exports were unaffected.)
- On some tablets and the Home Assistant app, the file picker refused to let you select a
  file at all; the pickers now accept the proper file types everywhere.
- Behind the scenes: automated tests now exercise the real upload path end-to-end so this
  class of fault can't ship silently again, and internal housekeeping (shared library and
  theme re-sync) rode along.

## 2026.8.81

**Sign-in page tidied, and password reset now emails you — plus a batch of behind-the-scenes fixes. No action needed for most sites.**

- The GSM sign-in page had misaligned username and password boxes; they now line up cleanly (and the same fix carries across the reset and change-password pages).
- "Forgot password?" now sends the reset code by email, and if email hasn't been set up on your box the page tells you so plainly instead of silently doing nothing. The Resend email key and alert recipients can now be set on the add-on Configuration page, so you can prepare them before you ever need a reset.
- Internal reliability: the operator-alert checks no longer raise a false alarm on the box's own start-up self-checks, the start-up self-test is now self-contained, and the "do you have a recent backup?" check no longer mistakes a small (but real) backup of a light database for a missing one.

## 2026.8.57

**Security fix — revoking access now takes effect everywhere, immediately. No action needed.**
When a licence was revoked, GSM correctly stopped the revoked site on one of its two sign-in
routes but not the other, so a site that still held its original credentials could re-register
itself and resume sending data. Revocation is now checked on every route — registration,
event and boundary — so a revoked site stays shut out until it is deliberately re-licensed.
Legitimate first-time registration is unaffected.

Also included: an internal safeguard that proves GSM's start-up self-test leaves no test data
behind on a live database.

## 2026.8.55

**Faster diagnosis when the database isn't set up right — no action needed.** GSM now raises
a clear alert the moment it can't manage the other add-ons' database access (for example, if
the database superuser password is blank or wrong), instead of letting an add-on quietly fail
to start. If a sibling add-on ever won't come up, the alert now tells you why in one line. GSM
also refuses to connect on a factory-default database password rather than doing so silently.

## 2026.8.53

**Security hardening — no action needed.** Two internal access paths were tightened: the
cloudhook receiver can no longer be tricked into reaching an internal page it should not, and the
Real Time Rice data routes now accept requests only through Home Assistant, not from other add-ons
on the box. Nothing changes in day-to-day use.

**Also new since your last update:** the GIS map's Explorer panel (search farms and paddocks, and
narrow the map by sub-region) and per-paddock NDVI imagery now render from the cached snapshots.

## 2026.8.35

**A farm can now confirm every paddock it sent actually arrived.**

When a farm box sends its paddock boundaries, GSM's reply now states how many it received. Until
now the reply listed only what changed, so a farm had no way to tell "47 sent, 45 arrived" from
"47 sent, 47 arrived, 45 unchanged" — and a partial sync could look like a quiet success.

> **Correction to the 2026.8.34 note.** That release told you to reload the GSM Proxy integration
> from its ⋮ menu. That does not work — Home Assistant keeps running the previous copy of the
> integration's code until it is **restarted**. The correct step, after any update that mentions
> the GSM Proxy: **update the add-on first, then restart Home Assistant.** Restarting before the
> update just loads the old copy again.

## 2026.8.34

**Boundary syncs from farm boxes work again**, and reviewing them no longer drags in the
whole farm.

> **One step after updating: restart Home Assistant.** Part of the fix below lives in the GSM
> Proxy integration, and Home Assistant keeps running the previous copy of it until it is
> restarted. **Update the add-on first, then restart** — restarting before the update just
> loads the old copy again. Reloading the integration from its ⋮ menu is *not* enough: that
> reloads its settings, not its code.

### Paddock boundaries sent from a farm now arrive
Boundary pushes from a farm box were being refused. GSM's own proxy was reformatting the
data on its way through, which broke the security signature that proves the data came from
that farm — so GSM correctly rejected it, and nothing said why. The data is now passed
through untouched and lands in the review queue as expected.

### Accepting a few changes stays a few changes
Accepting 5 changed paddocks on a 97-paddock farm used to queue the other 92 for review as
well. A sync is now judged by how much of the farm it covers rather than how many paddocks
it names, so a small change stays small. A genuine whole-farm sync still asks about any
paddocks that were left out of it.

### A refused sync now says what happened
A rejected push previously left nothing behind but a failure code. The activity log now
records the reason and what GSM actually received, so a problem can be traced to the system
that caused it instead of guessed at.

## 2026.8.25

**A large update — the first since 2026.7.60.** It adds two new ways to get data in and
out of GSM, a new way to explore your regions on the map, and a consistent look across
every page. No action is needed on your part beyond the usual update.

### Import SAP farm and grower data

A new **Data Management → Import SAP Data** wizard takes the SAP farm/grower spreadsheet
straight from Excel:

- Upload the file — the column layout is detected for you and can be corrected.
- **Preview before anything is saved.** Every row shows what would happen: create a new
  business, create or update a farm, or flag it for review. Nothing is written at this step.
- Commit the import in one go, then **undo the whole batch with one click** if it isn't right.
- **Import history** lists every run by date with its counts, so you can see what was
  brought in and when.
- **Saved mappings** — save a column layout once and load it next time the same report comes
  through.
- A new **Region mapping** page lets you maintain how SAP regions and localities translate
  to GSM regions, instead of that list being fixed in the software. Anything unrecognised is
  flagged for you rather than guessed at.

Rows missing a farm or SAP number are skipped rather than guessed, and a backup is taken
before a commit is applied.

### Paddock boundaries in and out

- **Export** — pick businesses or farms and download their paddock boundaries as a
  Shapefile, with the full attribute set.
- **Import** — a wizard accepts a zipped Shapefile, KML or GeoJSON: preview what's in the
  file, choose the target business and farm, then see exactly which paddocks would be added,
  replaced or created before committing. The previous boundary is kept so an import can be
  undone.
- Anything ambiguous, and any boundary currently maintained from a grower's own box, is
  **skipped unless you explicitly choose to apply it** — the grower box stays authoritative
  by default.
- Import and export now live together under **Data Management**; the boundary tools have
  been taken off the map, which is for paddock matching.

### Explore your regions on the map

The GIS map gains an **Explorer** panel down the left: filter by region and sub-region, see
live totals across owners, farms, paddocks, area and events, search owners, and expand a
Business → Farm → Paddock → Events tree. Clicking any item flies the map to it.

### Everyday improvements

- **Times are shown in local time** (AEST/AEDT) everywhere, instead of UTC.
- **A consistent look** across all pages, matching the rest of the PaddiSense range, plus a
  notice when the page you're looking at is behind a newer version.
- **Alerts** — the email delivery key can now be set on the Alerts page instead of needing a
  technician, a history of alerts that fired and cleared is shown, and alert emails say which
  box they came from.
- **Farm detail** — the "Owners" tab is now **Business Owners**, and its column reads
  **Business**, so it isn't confused with the owner's contact person on the People tab.
- **A grower boundary you've accepted is now protected.** Previously a routine bulk re-import
  could quietly overwrite a boundary staff had reviewed and accepted, with no error and no
  record. It no longer can.
- **Settings and setup** — the add-on configuration page is now grouped and labelled with
  guidance on each field, and connecting a box to PaddiSense Admin takes a single pasted
  connection code instead of six separate values. If a connection is refused you now get the
  reason immediately rather than silent failure.

### Reliability and security

- **Security update.** Third-party cryptography libraries updated to close three published
  vulnerabilities, and a round of fixes from an independent security review — including
  tighter checks that a user restricted to certain regions cannot reach data outside them.
- **A fault that could stop a box restarting has been removed**, along with a check that
  detects and reports it on any box already affected.
- **Daily backups and security scanning** now run inside the add-on, so they survive a
  restart and report honestly when they haven't run.
- Assorted fixes to status reporting so that "nothing found" and "nothing checked" can no
  longer look the same.

## 2026.7.60

**"Trust this device" login, and backups that survive a restart.**

- The staff and GIS logins gain a **Trust this device** option — tick it and you stay signed
  in on that device across restarts and browser closes instead of signing in every fortnight.
  Leave it unticked and the session ends when the browser closes.
- **Daily backups now run inside the add-on**, so they restart with the box. Backups are
  encrypted; an operator must set a backup passphrase for them to run.
