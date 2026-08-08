# Grower Services Manager — What's New

> Plain-English release notes. The full technical changelog lives in the source repo
> (`CHANGELOG.md`); this is the version that ships in the catalog.

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
