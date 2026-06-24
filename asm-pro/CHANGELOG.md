# Changelog

## 2026.6.112 — 2026-06-24

- Fix: **Edit Asset on mobile** — Delete / Cancel / Save buttons now stack vertically so the labels always fit (previously they wrapped on narrower phones).
- Fix: **Photo upload on mobile** — taking or uploading a photo from an asset page now works (was silently failing).
- Fix: **Photo viewing** — photos uploaded on mobile appear on the desktop view straight away (no more "1 photo" with an empty grid). Same image won't re-fetch when you re-visit the page — instant render from cache.
- New: **Caption on photo upload (desktop)** — optional caption field prompts you for a short description; the caption renders as an overlay on the photo tile.
- Internal: image-provenance signing wired (cosign + CycloneDX SBOM) — every grower image v.112 onward ships cryptographically signed and provenance-attested.

## 2026.6.107 — 2026-06-24

- New: **Resolve Issue** now has a "Resolved By" dropdown sourced from the People list, replacing the free-text "Your name" box. Stops typos drifting into the service history.
- Changed: Every active user now appears in every People dropdown — Assign, Resolve By, Technician — regardless of role. Office-job admins and coordinators can resolve / be assigned issues alongside field staff.
- Fix: A few hidden cross-location data leaks closed — staff with limited site access can no longer see or change assets / issues / services / parts / photos / videos / prestarts at sites they're not assigned to.
- Fix: Auditing of failed logins now records the typed username (was landing blank).
- Internal improvements — no user-visible changes (dependency CVEs closed, body-size cap on JSON, password change now revokes the user's existing sessions, dev-DB hygiene).

## 2026.6.100 — 2026-06-23

- New: The **Add Asset** form now has the same fields as the Edit Asset form — Site → Location → Area picker (cascading), Attributes (Type/Value), Meter Type, Service Interval, Prestart Required. No more dropping into Edit to fill in the rest after creating.
- New: **Assign issue** and **Technician** fields are now dropdowns sourced from the People list (Contractor / Co-ordinator / Manager). No more typos or "Bob" vs "bob" duplicate assignees. Existing free-text names are preserved with a "not on People list" note so nothing silently changes.
- Fix: **"Assign" button on a Maintenance Request drawer** now opens the assign form on the first click. It previously needed two clicks (or did nothing at all) because of a CSS quirk in how the form was being shown.
- Fix: Asset Videos list no longer fails silently when any video has been uploaded — a missing date-format conversion was crashing the list endpoint server-side.

## 2026.6.96 — 2026-06-23

- New: Asset videos now have a category — **Prestart** (shown in the prestart wizard) or **Instruction** (shown only on the asset's Videos page). Set the category when uploading, or change it later with the edit pencil.
- New: The video Videos page is now available on mobile with the same upload + edit experience as desktop.
- New: People (formerly Users) — four canonical roles (Contractor, Co-ordinator, Manager, Administrator). Only Managers use a PIN to log in. The username is derived from the Display Name automatically.
- New: Maintenance Requests drawer — schedule / conduct / update / resolve / ignore / reopen / re-assign actions all wired through one consistent dropdown.
- Change: Asset detail mobile is now a tile-based hub — each section opens its own page so the page loads instantly.
- Change: Prestart wizard mobile photo capture restored.
- Fix: People filter on the Config page dropped legacy role names and now matches the new canonical list.
- Fix: Sublist picker on the Config page lost its click target after the theme refresh.
- Fix: Asset Videos list page no longer fails silently when any video has been uploaded.

## 2026.6.70 — 2026-06-12

- New: Parts now have a Supplier field
- New: Asset and Parts edit forms use a Site → Location → Area picker
- New: Category filter on the Parts Inventory page
- Change: Service Interval label now matches the meter type (hours or km), and the field hides when meter is None
- Change: Config page reorganised into one tile per area (Assets / Parts / Issues / Services / Prestart Checklists / Locations / Notifications)
- Change: Locations are now strictly Site → Location → Area
- Fix: Asset and Part edit forms now match the new-item layout
- Fix: Photo and QR print dialogs now open inline (work inside the HA Companion app)
- Internal improvements

## 2026.6.22
- All dropdowns config-driven (8 new list editors on config page)
- Prestart checklist category fallback (sub-categories use parent checklist)
- Fix: checklist category dropdown shows all asset categories

## 2026.6.18
- Port conflict fix (8102)
- Notification groups
- Security hardening
- Bug fixes and enhancements
