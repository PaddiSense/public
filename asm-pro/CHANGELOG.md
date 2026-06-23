# Changelog

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
