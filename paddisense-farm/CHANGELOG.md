# Changelog

## 2026.7.87

### Maintenance
- Internal code-quality fixes; no change to how Farm works.

## 2026.7.86

### Reliability
- The add-on now reconnects to its database automatically after system updates or maintenance. Previously, a restart at the wrong moment could leave the add-on showing its licence screen until it was manually repaired — that can no longer happen.

## 2026.7.85 — WR-PS-192/074: owner-login rotation self-heal (port of Weather bd8d124) (DEV)

### Fixed
- **Incident 2026-07-27 (Weather was the victim; Farm carries the same exposure):** a flipped
  `farm_owner` login uses a STATIC stored options password; a DB-role seed re-mint changes the
  Postgres role underneath it and the addon strands on its next restart (DB init fails →
  licence gate fail-closed).
- Structural fix in `core/db/_pool.py` (ported from Weather v2026.7.9, commit bd8d124): for
  `*_owner` logins the admin-pool password is now DERIVED from the `/share` box key first
  (the fleet's derivation truth, Core v2026.7.44) via the new `_admin_password_candidates()`
  ladder, with the stored options password as fallback; loud WARNING when the stored copy is
  stale. The admin/owner pool also gained the same auth-failure rebuild-and-retry self-heal
  (`_acquire_admin_conn` + `_reset_admin_pool`) the app pool has had since 2026-07-09.
  `db_user: postgres` (pre-flip) boxes are unaffected — stored password only, never derived.
  The v2026.7.84 owner-boot handover (`_ensure_owner_ownership`, `_migrate.py`) is untouched —
  `_get_dsn(dbname, admin)` keeps its signature and the migration path is unchanged.
- Regression tests (`tests/test_pool_selfheal.py`): owner candidate ladder + admin-pool
  self-heal + end-to-end stale-stored-password recovery, proven-fail against the pre-fix code.
- Test-suite currency (pre-existing, exposed by a fresh disposable test DB): two fixtures
  still hard-inserted the legacy `channel` feature type (not in the WR-PS-153 registry seed —
  they only passed on stale test-DB state) → now `supply_channel`; the v.84 role-absent
  handover test now skips when `farm_owner` exists on the shared cluster (the WR-PS-074 fleet
  flip provisioned it — the absent precondition can no longer be staged).

## 2026.7.84 — WR-PS-074 Farm-side: cred-flip ownership handover (fixes farm_owner boot) (DEV)

### Fixed
- **The cred-flip (WR-PS-074) health-fails + rolls back as `farm_owner`** because Farm's 72 public objects are `postgres`-owned — as the non-superuser owner role every DDL migration failed *"must be owner of table"*. (The WR suspected the PostGIS extension; a live reproduction on the dev DB **ruled that out** — `CREATE EXTENSION IF NOT EXISTS postgis` is fine as a non-superuser when already present — and pinned it to object ownership.)
- **`_ensure_owner_ownership()`** (`core/db/_migrate.py`, superuser-gated, idempotent, non-fatal): pre-flip, hands ownership of every public table/sequence/view to `farm_owner` **and** grants it `USAGE, CREATE ON SCHEMA public` (the live proof caught that ownership alone still hit *"permission denied for schema public"* on `CREATE INDEX`). Runs only when the admin pool is a superuser **and** `farm_owner` exists (Core provisions the role) — belt-and-braces alongside Core's provisioner. Live-proven on the dev DB: after the handover, `farm_owner` runs `ALTER TABLE` + `CREATE INDEX`; DB fully restored after.
- **`_ensure_app_role` now skips cleanly when the admin pool is not a superuser** (post-flip `farm_owner` lacks CREATEROLE) instead of re-raising and crashing the flipped boot — the role/grants are already established from prior superuser boots.
- New `_admin_is_superuser()` gate. `tests/test_owner_ownership.py` locks the boot-safety no-op (writing this caught a `RealDictCursor` `[0]` bug in the gate before it shipped — R20).

### Handed to P/Core (WR-PS-074)
- End-to-end flip re-verify on dev (Core `cred_flip.py` machinery); store/planner UI-restarts (Peter); half (ii) per-addon default flips ride releases; grower rollout Peter-gated.

## 2026.7.83 — WR-PS-152: signed-licence receiver hardening (F-A1 box-binding + F-A2 no-bare-TOFU) (DEV)

### Security (from the Farm v.31/.32 5-agent red-team; Farm-side landing)
- **F-A1 (MED) — bind deactivate/revoke to THIS box.** `main.py` `_enforce_instruction_signature`: after signature + freshness + nonce verify, the instruction subject (`licence_id`/`target`, §9-A) must match this box's stored licence identity (`licence` or `grower_id`). A validly-Admin-signed deactivate/revoke minted for another grower no longer drops our licence (cross-box replay). Enforced only when signed, subject-bearing, and we hold an identity (an un-enrolled / subjectless-legacy box is untouched). Tests: cross-grower signed deactivate → 400; our own → 200 (no over-reject).
- **F-A2 (MED) — no bare-TOFU, coordination-gated.** `core/module_gate._verify_sig_and_key`: new `FARM_NO_BARE_TOFU` flag (default **off** during rollout). When on, a first signed access-sync push against a licence with **no `bound_fp`** is refused instead of bare-TOFU-pinned (a /23 sibling could otherwise win the race and become "Core"). Default-off so a box not yet re-issued with a `bound_fp` still bootstraps — flip **after** the fleet `bound_fp` re-issue (the WR's coordination gate). Tests cover both flag states + the bound_fp path unaffected.

### Deferred to the cross-addon coordination (WR-PS-152, handed to P/Core)
- Live cross-box validation against a real Admin-signed artifact; the matching hardening in the other addons sharing this §9-A receiver; F-A2 hard-enable after the fleet `bound_fp` re-issue; F-A4 (LOW, nonce persistence across restart); F-D3 (steward — broaden canonical `log_redactor` `enc:` regex).

## 2026.7.82 — WR-PS-189: retire PWM-migration export + expose stable bay uuids (DEV)

### Removed
- **`POST /api/spatial/infra-migrate-pwm` + the config-page "Import from PWM" button** (and the `_migrate_point` / `_pwm_pump_attrs` helpers). Dead against Peter's 2026-07-23 ruling (PWM pulls from Farm only — Farm never pulls PWM) and never worked against a real PWM (its ingress hardening 401s the sibling read → 502). `sibling_get` kept (Weather still uses it).

### Changed
- **`/api/spatial/bays` and `/api/spatial/bays/{id}` now expose the stable `uuid`** in feature properties (Rev-4 identity discipline, WR-PS-153). The column already existed (FAIR migration); PWM can bind bays on `properties.uuid` instead of the volatile serial `id`. Test `test_pwm_migration_idempotent` replaced by `test_bays_expose_stable_uuid`.

## 2026.7.81 — infrastructure map labels (DEV)

### Added
- **Label options for infrastructure** — each infra object in the tree now has two label pickers (like bays), offering **Name** plus the type's own attributes (flow rate, make/model, …) read from the config registry. The chosen attributes render as a permanent on-map tooltip for that feature, persisted per-object in localStorage (`farmmap.infraLabels.v1`).

## 2026.7.80 — infrastructure tree: individual objects, toggle + zoom (DEV)

### Changed
- The management tree split infrastructure by type (Pumps, Gates, Supply channels…) but only showed a **count** under each — no individual objects, no per-object visibility, no zoom (unlike bays). Now each type node expands to its **individual features**, and each feature has its own visibility toggle and **click-to-zoom** (clicking a gate/pump/channel shows it and fits the map to it). Backend: `api/tree.py` emits individual features per type; `GET /api/spatial/infrastructure` gains an `?id=` filter; `overlayOn` takes an on-load callback so the map can zoom once the feature loads. Confirms/fixes the reported behaviour (types were correctly split, but objects were lumped under one heading).

## 2026.7.79 — delete infrastructure from the map (DEV)

### Added
- **Delete an infrastructure feature** (pump, gate, channel, …) — there was no delete path before (only Add / Attributes / Edit shape). New `DELETE /api/spatial/infrastructure/{id}` (operator role) that refuses if something still depends on the feature: a child feature (e.g. a gate sitting on a channel, via `parent_id`) or a recorded event (`field_events.infrastructure_id`) — so a delete can't silently orphan data. Added a **Delete** button to the infrastructure edit form on the farm map (click a feature → Attributes → Delete). Regression: `tests/test_delete_infrastructure.py` (incl. the refuse-with-child control).

## 2026.7.78 — stale-tab update banner on the standalone map pages (DEV)

### Added
- Extended the stale-tab update banner (from .72) to the four **standalone** map pages — `record-mobile`, `record-desktop` (RE01.M/RE01.D), `farmmap`, and `match`. These are served as static files (not Jinja templates extending `base.html`), so the .72 change didn't reach them. Each now polls `/health` on a 1-minute interval and on tab-foreground, showing "Farm updated to vX — tap to reload" on a version mismatch (never auto-reloads mid-record). Full Farm surface coverage.

## 2026.7.77 — fix: orphaned/empty farms can now be deleted (DEV)

### Fixed
- An empty farm (e.g. one created by a GSM sync that never got a paddock) showed in the management tree but **not** in the config farm list, so it couldn't be deleted. Root cause: the tree (`api/tree.py`) lists all farms, but `GET /api/spatial/farms` filtered to farms with a visible non-GSM paddock (`HAVING COUNT > 0`). Added `?show_all=true` (a LEFT JOIN returning every farm + its visible-paddock count) and pointed the desktop + mobile config farm-management at it. Empty farms now appear with count 0 and delete cleanly via the existing `DELETE /api/spatial/farms/{id}` (which already refuses farms that still have visible paddocks).

## 2026.7.76 — RE01.D: prominent target-type picker (parity with mobile) (DEV)

### Changed
- Desktop record already supported Bays/Infrastructure via small toolbar checkboxes, but they were easy to miss. Added a prominent **4-button target picker** (Paddocks · Bays · Crops · Infrastructure) in the New-mode panel — under "+ New", above Event Type — matching the mobile map-layer buttons. Selecting one shows that layer only, syncs the toolbar checkboxes, and sets the "Click a … on the map" hint. Drives the existing `selectBay`/`selectInfra` + save-target machinery (no backend change).

## 2026.7.75 — RE01.M: record against Bays + Infrastructure (DEV)

### Added
- **Bays and Infrastructure target selection** on the mobile record map. A second toggle row (Bays | Infrastructure) sits under Paddocks | Crop Zones; each loads its layer (`/api/spatial/bays`, `/api/spatial/infrastructure`), supports tap-to-select with pills + a "Recording to…" banner, and records against the backend's `bay_id` / `infrastructure_id` targets (which `_build_targets` + the events INSERT already supported). Bays carry their parent paddock so events still hang under the right field; infrastructure is farm-level (#29). `GET /api/spatial/bays` now includes `farm_id` so bay events get the right farm.

## 2026.7.74 — RE01.D parity audit: irrigation/cultivation/crop_stage editable (DEV)

### Fixed
- Mobile records **irrigation** (`irrigation_type`), **cultivation** (`cultivation_method`) and **crop_stage** (`crop_stage`) events, but the desktop edit panel had no branch for them — they fell through to a generic "Type/Product" field, so those captured values couldn't be edited. Added the three edit branches (display + save). Audit basis: mobile detail-panel `data-key`s vs desktop `editEvent`/`saveEdit` fields.

### Notes
- Intentionally left out of the edit form: **crop_zone** (the event's target — re-targeting is a distinct operation, not a field edit) and **crop_complete** (a harvest action flag that re-runs the mark-fallow cascade, not persistent data).

## 2026.7.73 — RE01.D desktop edit parity: weather + sprayer method (DEV)

### Fixed
- **Weather captured on mobile now shows in the desktop edit panel** and is editable. `editEvent` loads the event's stored `weather` (the `field_events.weather` column) into the existing weather renderer, `saveEdit` sends it back, and the `PUT /hfm/api/events/{id}` handler now persists the `weather` column (it was omitted from the updatable fields).
- **Application method is now associated with the sprayer**, not a standalone editable field — shown read-only as "(from sprayer)". `saveEdit` also preserves the full applicator object (name + method + attributes) instead of collapsing it to just the name, which previously dropped the sprayer's method on any edit.

## 2026.7.72 — stale-tab update banner (adopted from PWM) (DEV)

### Added
- **Stale-tab watch** on every Farm surface (mobile + desktop base templates and the standalone RE01.M record page): a deploy leaves any open tab running old JS (which can send the wrong command), so each page polls `/health` once a minute and whenever the tab returns to the foreground, comparing the live version to the render-time version. On a mismatch it shows a `ps-update-banner` — "Farm updated to vX — tap to reload". Never auto-reloads (the operator may be mid-record). Pattern adopted from P-Claude's PWM implementation (WR-PS-186 `ps-update-banner`).

## 2026.7.71 — RE01.M: readability + Store-authored products + operator persist (DEV)

### Changed
- **Chemical Step 2 spray summary** (Date / Start / End) was three squashed columns — now three readable stacked rows (label left, value right).
- **Step 4 applicator card** attributes were two-per-row — now one per row for readability.
- **Removed the in-page "New Product" form** (it captured none of the correct label data). The "+ New" buttons are now "+ Add in Store" and open a notice: products are authored in the Store addon (full label data) and appear here automatically once added.
- **Operator name now persists via localStorage** instead of a cookie (cookies are dropped in the ingress iframe). Follow-up: adopt Store's mature HA-users dropdown (defaults to the logged-in HA user) — needs a Farm `/api/v1/ha-users` endpoint ported from Store.

## 2026.7.70 — RE01.M: Store products + weather capture unblocked (DEV)

### Fixed
- **Chemical product list was empty.** The page asked Store for `category=Chemical`, but Store categorises by type (`Herbicide`/`Adjuvant`/…, with `Fertiliser` for nutrient) — there is no `Chemical` category. Now pulls the full Store catalogue via `/hfm/api/store-products` and partitions client-side: chemical = everything except Fertiliser; nutrient = Fertiliser.
- **Weather never captured.** The page called `/weather/api/…` which 404s — the Farm proxy is `/hfm/api/weather/…` (Weather addon → Open-Meteo fallback). Fixed all three URLs.
- **Weather now auto-captures** on entering the chemical How-Applied step (for the selected date/time) — no button press; the button remains as a manual recapture.

## 2026.7.69 — RE01.M mobile record: fat-thumb + submit fixes (DEV)

### Fixed
- **Review Submit button couldn't be tapped** (event "wouldn't submit / stayed on the last step"): the in-content `#submitBtn` sat flush against the fixed bottom nav, so its lower half overlapped Back/Cancel and taps missed. Now 100px tall with 32px bottom clearance.
- **Date quick-picks (Step 2)** were a cramped 3-across grid — now one full-width button per row (Today / Yesterday / Pick Date) at 100px for fat thumbs.
- **Map-phase Next button** was partly covered by the Leaflet attribution — attribution moved to top-right (and dimmed), Next button raised to 100px.

## 2026.7.68 — FAIR: hard-enforce infrastructure.feature_type vocab (DEV)

### Changed
- **`infrastructure.feature_type` is now FK-enforced** against the `infra_feature_types` registry — the digital twin can trust the type on every asset. Migration `fair_vocab_infra_feature_type` is prod-safe: it normalises legacy mis-keyed rows to canonical keys (`'Electric Pump'`→`pump`, `'Supply Channel'`→`supply_channel`, plus a generic label→key pass), absorbs any unforeseen orphan as an **inactive** registry type so the FK always adds (and leftovers surface, re-keyable in config), then adds the FK. `_validate_infra` already rejected unknown/inactive types at the API; this is the DB-level backstop.
- Selftest `data_integrity/vocab_fks_enforced` asserts all three FAIR vocab FKs (event_type, crop_type, feature_type) are present, so a prod orphan blocking one goes red instead of silently dropping enforcement. Regression: `tests/test_fair_vocab_infra.py` (incl. must-be-rejected control).
- Test infra: `conftest.py` now sources the postgres superuser password from `secrets.yaml` (as the app does) when `FARM_DB_PASSWORD` is unset — so the release gate's pytest runs without the caller hand-exporting it. Falls back to the dev default if unreadable.

## 2026.7.67 — fix: crop config row showed "Failed to load" (DEV)

### Fixed
- The Crops config list showed **"Failed to load"** even though the API returned all crops. `loadCrops()` calls `populateCropSelects()`, which did `document.getElementById('newListCropId').innerHTML = …` with no null-guard — that element was removed in the WR-PS-156 config restructure, so the lookup returned null and threw a `TypeError`, tripping `loadCrops`'s catch *after* `renderCrops` had already drawn the table (so the error overwrote the rendered rows). Added the defensive null-guard (`if (!sel) return;`). Swept the whole config page for other orphaned `getElementById` targets — the remaining 12 (legacy enum editors) are all already guarded.

## 2026.7.66 — fix: cannot add a crop in the config menu (DEV)

### Fixed
- Adding a crop whose name already exists (crops.name is unique) 500'd — the `POST /api/spatial/crops` handler did an unguarded INSERT so the `UniqueViolation` propagated as a raw 500, and the config UI's error check (`d.status === 'error'`) never matched the handler's `{"error": ...}` shape, so no reason showed and it looked like "can't add a crop". The handler (and the rename path in `PUT`) now return a clean **409** `"A crop named 'X' already exists."`, and `saveCrop`/`deleteCrop` surface it via `!r.ok || d.error`. Regression: `tests/test_crop_duplicate_500.py` (fails pre-fix).

## 2026.7.65 — theme: re-cp master (WR-PS-186 Pattern 5 + mode tokens) (DEV)

### Changed
- Re-cp'd `paddisense-tokens.css` byte-identical from the master (`8364f87`) — adds Pattern 5 `.ps-actuator-btn` (position control) + the `--ps-mode-*` domain tokens + `--ps-pink`. Keeps Farm gate-green under the hardened Rule 17. Classes available for adoption; no behaviour change from the re-cp.

## 2026.7.64 — theme: re-cp master tokens (WR-PS-186 control patterns) + gate now bites at commit (DEV)

### Changed
- **Re-cp'd the canonical `paddisense-tokens.css` from the master** (byte-identical, Rule 17) so Farm carries the new WR-PS-186 control-surface patterns: `.ps-btn-state-on/-off/-stopped/-wait`, `--ps-control-h` (+ `.ps-btn-control`), the bare-`.ps-btn` defensive default, and `.ps-update-banner`. Classes are available for Farm's controls to adopt; no behaviour change from the re-cp itself.
- Fleet steward note (not Farm code): the shared theme gate was hardened to **block at commit-time** (was warn-until-grower-release) — app.css master-redefinition, `ps-` namespace squat, and dangling `ps-*` classes now fail `verify-commit`; hex scan covers `static/js/`; addon-specific hex exemptions move to `<pkg>/theme-exempt.txt`. Farm passes the hardened gate clean (0 dangling, 0 hex, app.css redefines 0 master classes).

## 2026.7.63 — Full-schema FAIR / digital-twin future-proofing (#28) (DEV)

Peter (2026-07-21): sweep all 71 tables for FAIR / digital-twin structure while data is limited; fix structure now as a prod-safe update-migrate.

### Added / Changed
- **Stable `uuid` + `created_at` + `modified_at` on 29 digital-twin entity / reference-registry tables** that lacked them (crops, varieties, chem_*, notification_groups, planning_* [9 tables], soil_tests, sampling_grids, yield_zones, spatial_data_points, weather_stations, rtr_paddocks, provider_fields, the infra/land/object typed-attribute registries). Migration `fair_entity_future_proof`: add column + backfill existing rows + DB `DEFAULT gen_random_uuid()` + unique index — all additive/idempotent, **prod-safe** (backfills only NULLs, so an update-migrate onto existing prod data is clean).
- **`planning_rotation_cells.paddock_id` → real FK** to paddocks (`fair_planning_rotation_cells_fk`), guarded so it only applies when there are no orphan rows (prod-safe). External identifiers (`gsm_farm_id`, `gsm_paddock_id`, audit/draft `user_id`) intentionally stay plain — they reference remote systems, not local tables.
- Operational / log / time-series / junction tables (audit_log, sync_log, gsm_*, import_staging, weather time-series, config, ps_users, provider_credentials, paddock_sources, *_group_members, …) intentionally excluded — identified by natural keys, not twin entities. Full classification in `docs/FAIR_AUDIT.md`.
- Tests `test_fair_future_proof.py` (uuid + provenance on every entity table, uuid DEFAULT set, guarded FK present).

## 2026.7.62 — Sweep F FAIR: hard-enforce event_type + crop_type vocab (#28) (DEV)

### Added
- **Hard-enforced controlled vocabulary on the two columns whose source is canonical** (not user-editable free-text), for a trustworthy digital twin. New `event_types` lookup (canonical taxonomy + any distinct existing value) with a real FK on `field_events.event_type`; `crops.name` made UNIQUE and `field_events.crop_type` FK'd to it (all existing values already match). Seeding runs before the FK so no existing row violates; DO-guarded/idempotent. `test_fair_vocab.py` includes must-be-rejected controls (a value outside the vocabulary is refused at the DB).
- **Deferred:** the user-editable `hfm_config` vocabs (observation_type/variety/application_method/severity/irrigation/cultivation/sowing methods) need the config lists normalised into source-of-truth tables before they can be FK'd without breaking "add a new term" — folded into the full FAIR schema audit now underway.

## 2026.7.61 — Sweep F FAIR P3: provenance columns (#28) (DEV)

### Added
- **`created_by`** on the 9 reference/spatial entity tables that lacked it (paddocks, crop_zones, bays, farms, growers, seasons, spatial_datasets, hfm_products, hfm_applicators).
- **`modified_at`** (TIMESTAMPTZ DEFAULT NOW()) on the four tables missing it (seasons, spatial_datasets, hfm_products, hfm_applicators). `bays.source` already exists (#17). Migration `fair_p3_provenance` — additive + idempotent. Tests `test_fair_p3.py`.
- **Sweep F FAIR is now complete except the two design-gated items** — controlled-vocabulary enforcement and the infrastructure connectivity/topology model — which are surfaced for a decision rather than built unilaterally (see docs/TODO.md).

## 2026.7.60 — Sweep F FAIR P2: real FKs + PostGIS geometry (#28) (DEV)

### Added
- **`field_events` PostGIS `geom`** (was GeoJSON JSONB only) + GIST index — events are now spatially queryable. Backfilled from the JSONB via shapely (mixed point/polygon → generic geometry, not Multi); `_backfill_geojson_geom` heals existing + new rows on startup.
- **`farms.geom_point`** derived from the existing lat/lon (`ST_MakePoint`; no JSON-C needed) + GIST index, healed each startup.
- **`spatial_datasets.season_id` / `crop_id` are now real FKs** (were dangling ints) → `seasons(id)` / `crops(id)` `ON DELETE SET NULL`. The table is empty so this is zero-risk; DO-guarded for idempotency.
- Tests `test_fair_p2.py` (columns/indexes, FK constraints, both geom backfills populate).

### Deferred (design decision needed — see docs/TODO.md Sweep F)
- Controlled-vocabulary **enforcement** (event_type/category/application_method/variety/severity) and linking applicator/variety by id: needs a policy call (hard CHECK/FK vs warn-only) since a hard constraint against the mutable `hfm_config` lists can block event recording. Not landed unilaterally.

## 2026.7.59 — Sweep F FAIR P1: stable uuids + growers/spatial_datasets reachable (#28) (DEV)

### Added
- **Stable `uuid` on the 9 reference/spatial tables that lacked one** (paddocks, crop_zones, bays, farms, growers, seasons, spatial_datasets, hfm_products, hfm_applicators). Serial `id`s aren't stable across a re-migration, so a uuid is the findable, migration-safe key. Migration `fair_uuids_p1` adds the column, backfills existing rows, sets a DB-level `DEFAULT gen_random_uuid()::text` (fills new rows with no insert-site changes), and adds a unique index. Additive + idempotent.
- **`GET /hfm/api/growers`** — growers were previously only readable embedded in the map tree; now listed directly (id, uuid, name, sap_id, sunrice_id, contact), alongside the sibling `/hfm/api/farms|paddocks|crop-zones`.
- **`GET /api/spatial/datasets`** (optional `?farm_id=`) — the `spatial_datasets` table (EM / as-applied / yield / NDVI metadata) was unreachable (no route); now exposed with its uuid. (Shapefile-export inclusion deferred — the table has no geometry of its own; it references paddock_id.)
- Tests `test_fair_p1.py` (uuid columns present + DEFAULT populates + both endpoints).

## 2026.7.58 — fix: GSM-tab event cards show product/rate detail (#25) (DEV)

### Fixed
- **Selectable event cards on the GSM Data tab (EV02) showed only the event type** ("Sowing"/"Chemical") with a blank detail line. Two mismatches blanked the per-event summary: the card read `e.payload` but the preview API returns the event's JSONB under `e.data`, and `_gsmEvtSummary` read `crop_type_name`/`variety_name` where the data actually carries `crop_type`/`variety`. So `_gsmEvtSummary` always received `{}` and returned an empty string.
- **Fix:** the card now reads `e.data` (parsing a string form defensively) and passes the row so the summary can fall back to the typed columns (`product`/`rate`/`rate_unit`/`crop_type`/`variety`) for imported events that keep detail only in `data`. `_gsmEvtSummary` uses fallback chains across both key variants. Cards now read e.g. "Rice · Langi · 150" (sowing) and "Roundup 2.5 L/ha, Test 1" (chemical tank-mix). Verified against live event payloads.

## 2026.7.57 — fix: CNH auto-sync fired several times a day (#30) (DEV)

### Fixed
- **CNH (and JD) auto-sync ran multiple times a day instead of once.** The "already synced today" guard lived in an in-memory dict (`_last_sync_dates`) that was wiped on every addon restart. A box that restarted past the scheduled time — deploys, HA restarts, addon reloads — re-armed the daily sync each time, so it fired once per restart (live `sync_log` showed 6 CNH `sync_all` rows on 2026-07-20).
- **Fix (Rule 106 instance + pattern):** the daily guard now reads from the persisted `sync_log` table (`_synced_today` — is a `sync_all` for this provider already recorded today, UTC?), so a restart cannot re-arm it. On a read error it fails closed (assumes synced) to protect against re-syncing. The in-memory `_last_sync_dates` is removed. Regression `test_cnh_sync_cadence.py` (fails pre-fix). Applies to both CNH and JD (shared loop).

## 2026.7.56 — fix: import-staging "save" 500 on a sowing event (#32) (DEV)

### Fixed
- **Saving a staged sowing event could 500** with a raw "internal error" after cleaning. A sowing whose cleaned geometry yields no polygon falls through to the shapefile fallback (`_group_shapefile_by_product` → `parse_shapefile_zip`). That parser returned `{"error": …}` for a *present-but-invalid* zip but **raised** `FileNotFoundError`/`IsADirectoryError`/`TypeError` for a **missing / empty / None** `file_path` (e.g. a cleaned upload whose temp file is gone). `_create_crop_zones` called it unguarded, so the raise propagated out of `POST /import/api/staging/{id}/import` as a 500 — and because the field event had already been inserted, the staging row was left un-finalised.
- **Fix (Rule 106 instance + pattern):** `parse_shapefile_zip` now honours its contract and returns `{"error": …}` (never raises) for a missing/empty/None/directory path; and `_create_crop_zones` treats crop-zone creation as best-effort — a shapefile-fallback failure degrades to "no zones created" instead of failing the import commit, so the event is saved and the staging row finalised. Regression `test_import_sowing_save_500.py` (fails pre-fix).

### Fixed
- **Silent data loss on the grower→GSM event send.** Every field was run through `for_agent()`, which `str()`s its input and wraps it `[UNTRUSTED: …]`. This (a) stringified the `operator` and `applicator` **dicts**, so GSM's `isinstance(dict)` promotion dropped them — operator name/device and the whole applicator/nozzle/boom/tank block were lost across **all** cascade tables; and (b) stored the literal `[UNTRUSTED: Roundup]` in GSM's **typed** columns (product, rate_unit, crop_type, variety, observation_type, severity, reading_unit) and on the denormalised `paddocks.crop`. Confirmed against GSM's ingest (`event_handlers.py` guards + verbatim typed-column writes) and its render surfaces (no re-fencing of these fields).
- **Fix:** structured fields now cross as dicts (`sanitise_struct`) and typed/enum scalars cross clean (`sanitise_scalar`) — both keep the storage-safety half of R175 (control-char strip, whitespace collapse, truncate) but drop the value-corrupting `[UNTRUSTED:]` fence. The tank-mix `products[]` array is sanitised the same way. Only free-text prose an AI reader consumes (`notes`) stays fenced. New `core.text` helpers `sanitise_scalar` / `sanitise_struct`; `for_agent` behaviour unchanged. Test `test_gsm_send_payload.py` (fails pre-fix). **Follow-up (GSM):** extend GSM's render-time `sanitise_for_operator` to the event GIS surfaces, then Farm can unfence `notes` too.

## 2026.7.54 — MP02 point-move geometry edit (pass 2) (DEV)

### Added
- **Move a point feature** (pump, gate, bore …) on the map: with the Infrastructure layer ticked, click the point, hit **Edit shape**, then **drag the point** to its new location and **Save**. Previously "Edit shape" only reshaped lines and polygons — points had to be deleted and re-drawn. The point is grabbed directly (leaflet-draw's vertex editing doesn't apply to point markers), map panning is suspended while dragging, and the new position is saved through the existing `PUT /api/spatial/infrastructure/{id}/geometry` (validates it's still a point).

## 2026.7.53 — MP02 legend + farm summary (pass 1) (DEV)

### Added
- **Farm summary + legend** in the map's right-hand panel (the **Σ** button in the tree toolbar, and the default view on load). Whole-box totals — **total channel length**, infrastructure and land-cover feature counts — plus a per-type legend: each infrastructure type and land-cover category with its map colour, feature count, and measure (channel length for lines, area for polygons). Clicking a populated legend row toggles that layer on the map.
- **Per-type map colours** — infrastructure types (channel / pump / gate …) and land-cover categories each draw in a stable colour instead of one flat blue/green, so the map matches the legend and types read apart at a glance.
- `GET /api/spatial/summary` — per-type aggregates (counts, geodesic length for line types, hectare area for polygons) computed in PostGIS geography; empty types are kept so the legend lists every active type. Optional `farm_id` scope.

## 2026.7.52 — Base-seed the registries + MP02 infrastructure geometry edit (DEV)

### Added
- **Base-seed for the typed registries** (WR-PS-156 phase 3) — in seed-author mode, a **"Base"** tick sits **beside "active"** on each Infrastructure Type and Land Cover category (ships the type + all its attributes + enum options), and **per attribute** on Feature Attributes. The snapshot exports these; grower boxes materialise each **once per `base_key`** via the same tombstone (a grower's deletion stays deleted). Config page fully base-seedable now.
- **MP02 infrastructure geometry edit** — an **"Edit shape"** tool on the Infrastructure tab: tick the layer, click a feature, drag its vertices, Save. `PUT /api/spatial/infrastructure/{id}/geometry` validates the new geometry against the type's kind and recomputes computed attributes (a channel's length). Points can't be reshaped (delete + redraw to move).

## 2026.7.51 — fix: registry type-header row spacing (DEV)

### Fixed
- The Infrastructure/Land type-header row (Name / drawn-as / active / Save / Delete) and the guided attribute card lost their spacing when the local `cfg-*` CSS was retired — the JS still emitted `cfg-add-row`. Switched to the canonical `ps-add-row` (flex-wrap + gap), so those rows are no longer squashed.

## 2026.7.50 — fix: Base tickbox now renders (Jinja macro context) (WR-PS-156) (DEV)

### Fixed
- The config-list **"Base"** column never showed in seed-author mode: the `_config_section.html` macro was imported without `with context`, so it couldn't see the page's `seed_author` flag. Both config pages now `import config_section with context` — the Base checkbox renders and items can be ticked into the grower seed set.

## 2026.7.49 — diag: log seed-author mode at startup (WR-PS-156) (DEV)

### Changed
- Startup log now records `seed_author_mode` so the seed-author wiring is verifiable from the addon log.

## 2026.7.48 — Base-seed model: curate the grower config seed from the menu (WR-PS-156 ph2) (DEV)

### Added
- **Base-seed curation** (the Store/Seed-Manager model). In **seed-author mode** (`seed_author_mode` option → `FARM_SEED_AUTHOR_MODE`) the config lists show a **"Base"** checkbox — tick an item to include it in the grower seed set. `POST /api/config/items/{id}/base` records `is_base`/`base_key` (manager + seed-author gated).
- **`paddisense_farm/seed/snapshot.py`** — `python -m paddisense_farm.seed.snapshot` writes `seed/base_seed.json` from the Base-ticked items (run on the dev box, commit the file → it ships in the image).
- **Materialize on startup** — `_apply_base_seed()` seeds each base item **once per `base_key`** via the `farm_config_seed_log` tombstone: new base items reach existing grower boxes on update, a grower's deletion is never resurrected, and a grower's own same-id row is never overwritten.

## 2026.7.47 — Farm config onto the canonical ps-config-section subsystem (WR-PS-156) (DEV)

### Changed
- **Farm's config page (CF01) now uses the fleet-canonical config component** — `ps-config-section` / `ps-list-table` / `ps-cfg-*` (TEMPLATE_GUIDE §6), the same as Store and Seed Manager — instead of its old local `cfg-*` editor. Desktop **and** mobile config pages converted: every section is a native `<details class="ps-config-section">`, tables are `ps-list-table`, the config lists are rendered by the shared `_config_section.html` macro. Passes the new canonical-config release gate (ADR-017).
- **Config lists moved from `hfm_config` JSON to the canonical per-row model** (`farm_config_items`) — per-row order / active + base-seed provenance (`is_base`/`base_key`). Back-filled once-if-empty, **preserving each item's stable `item_id`** so historical field-events keep resolving. The wizard reads active items via the same shape (`{id, name}`).
- New `api/config_items.py` (canonical add/rename/reorder/active/delete + `set_base` for phase-2 seed authoring; `FARM_SEED_AUTHOR_MODE`).

### Note
- **Phase 1 (component parity).** Phase 2 = the base-seed snapshot/materialize so a seed-author can curate the grower seed set from the menu (the "Base" tick).

## 2026.7.46 — CF01 config: guided, plain-language attribute editor (DEV)

### Changed
- **The attribute config editor is now guided and plain-language** (Peter: CF01 was "very busy and hard to understand"). The dense 8-column table + separate "Option lists (enums)" section are replaced by: a calm attribute **list** (standard `.cfg-list` theme), and a small **Add/Edit card** that shows only what matters — Name, then "This is a…" **Text / Number / Choice from a list / Yes-No** (no `enum`/`data_type`/`key`/`spec` jargon). **Choice options are typed inline** (no more bouncing to a separate enum-list area — the multi-stage flow is gone). Progressive disclosure: Unit shows only for Number, options only for Choice; **"Auto-calculate length/area from the shape"** is a plain checkbox on line/polygon types instead of a `computed` dropdown. One shared editor across **Infrastructure Types, Land Cover Types and Feature Attributes** — all now consistent with the standard config theme.
- `infra-attrs`/`land-attrs` endpoints now persist the `computed` flag (so the auto-calculate toggle works for those types too).

## 2026.7.45 — Config-defined attributes for every map object type + auto-computed length/area (DEV)

### Changed
- **Every map object type's attributes are now config-defined** (Peter). The config menu is the single place that defines the attribute list per type — paddocks, bays and crop zones join pumps/gates/channels and land cover. The right-hand map panel just fills the values in (no free-form invention), keeping everything typed so PWM reads it by key. New config-page section **"Feature Attributes"** (paddock/bay/crop-zone), backed by a generic `object_attribute_defs`/`object_enum_options` registry. Paddocks gain an `attributes` bag; the free-form bay/crop-zone editor from v.44 is replaced by the typed one.

### Added
- **Computed attributes** — a line feature's **length** and a polygon's **area** are auto-calculated from the geometry (PostGIS geodesic), shown read-only in the panel, never typed by hand. Every infra line type gets an auto `length_m`; land polygons get an auto `area_ha`. Flaggable per attribute in config (`computed` = length_m/area_ha).
- Paddock **"Edit attributes"** in the field inspector; typed attribute panels for bays/crop-zones/paddocks.

## 2026.7.44 — MP02 sweep: infra-by-type tree, source-gated bay/zone editing, land cover (DEV)

### Added
- **#35 Land cover** — native vegetation / wetland / riparian as their own map layer + config-editable typed registry (`land_features` + `land_feature_types`/`_attribute_defs`/`_enum_options`, seeded, stable `uuid`/`source`). MP02 draw-by-category authoring, own tree branch, config-page "Land Cover Types" editor. Not infrastructure, not a crop.
- **#17 Edit bays + crop zones** on MP02 — click a locally-authored bay/zone → edit name + free-form attributes in the right panel. External-sourced (CNH/JD/GSM/import) features are read-only, enforced server-side (`core/provenance.py`). Bays gain a `source` column; crop zones gain an `attributes` bag.

### Changed
- **#34** the management tree splits infrastructure into per-type nodes (Pumps, Supply channels…) instead of one lumped "Infrastructure"; each pulls only its own features.
- **#33** the infrastructure/land authoring form only offers asset types whose geometry matches what was drawn (no "pump" for a line).

## 2026.7.43 — PWM → Farm infrastructure migration export (WR-PS-153 Rev 5) (DEV)

### Added
- **One-time migration export** `POST /api/spatial/infra-migrate-pwm` (manager) + config-page **"Import from PWM"** (Preview / Import). Pulls PWM pump/gate **locations + physical specs** into Farm `infrastructure` over the fleet sibling-pull — **read-only on PWM, never touches `pwm_devices`/ESPHome** (Rev 5). **Idempotent** via a new `infrastructure.source_ref` (`pwm:pump:<id>`) so re-running mints no duplicates; **dry-run unless `?commit=1`**. Writes only Farm (Farm-first; PWM keeps authoring until P re-points). `tests/test_infra_registry.py`.

## 2026.7.42 — Infrastructure config-UI list editor (WR-PS-153) (DEV)

### Added
- **Config page → "Infrastructure Types"** section: manage the whole registry in-app (Peter's "manage any of the lists in the UI"). Add/edit/deactivate feature types (label, geometry kind, category), add/edit/delete their typed attributes (label, data type, unit, enum list, spec, required), and manage enum option lists (add/remove options, create new lists). No hard-coded vocab anywhere — the map authoring form is driven entirely by what you set here.
- API (manager role): `GET /api/spatial/infra-registry` + `POST/PATCH/DELETE /api/spatial/infra-types`, `.../infra-attrs`, `.../infra-enums`. A type in use by existing features can't be deleted (deactivate instead). Tested in `tests/test_infra_registry.py`.

## 2026.7.41 — Infrastructure authoring: typed registry + draw-by-type (WR-PS-153) (DEV)

### Added
- **Farm is now the single author of physical infrastructure** (WR-PS-153, P-signed). Config-driven registry: `infra_feature_types` / `infra_attribute_defs` / `infra_enum_options` (seeded pump/gate/supply+drain channel/bore/dam/… with typed attributes + units + enums, is_spec-marked). `infrastructure` gains a **stable `uuid`** (PWM keys on it), `source`, `created_by`, and gate→channel **containment** (`parent_id`).
- `GET /api/spatial/infra-types` — drives the authoring form. `POST/PATCH /api/spatial/infrastructure` validate feature type + geometry-by-type + typed attributes (unknown attr / wrong number / bad enum / missing required all rejected) and mint the uuid; `GET` now returns `uuid`/`source`/`parent_uuid`.
- **MP02 draw-by-type authoring**: pick the asset type from the config list → the map draws its geometry kind → fill typed attributes (enum dropdowns, units shown, spec-marked) → optional channel (containment) → Create. Replaces the free-text `prompt()` + hard-coded type/attribute lists. `tests/test_infra_registry.py`.

## 2026.7.40 — MP02: split-distance default + tree state kept across refresh (DEV)

### Changed
- Default split (bank/levee) distance is now **5 m** (was 2 m) (#13).
- A tree rebuild (after a split/cut/edit/add) now **preserves expansion + selection** instead of collapsing to the first farm — captured by stable node key and restored after render; after a split the parent field stays selected and scrolled into view (#12).

## 2026.7.39 — Split naming: clean, non-compounding piece names (DEV)

### Fixed
- Splitting a bay (or crop zone / paddock) named pieces `f"{name} {i}"` / `name+letter`, which **compounded on every re-split** into garbage like `SW5 1 1 1 1` (#14). New `core.text.split_piece_names` strips the trailing split index to a stable base and numbers pieces from the next free sibling index — a re-split of `SW5 1 1 1` (siblings `SW5 2`) now yields `SW5 4, SW5 5`, never `SW5 1 1 1 1`. Applied to bay, crop-zone and paddock splits (Rule 106 — instance + pattern). Unit-tested in `tests/test_split_naming.py`.

## 2026.7.38 — MP02 farmmap: inspector fixes + remembered tree state (DEV)

### Fixed
- Field inspector **Bays** row rendered `[object Object],…` — now shows the bay **count + names** (#15).
- Clicking a bay/crop/infrastructure overlay on the map now **updates the right-hand inspector** (name, area, crop/variety/type, parent field) instead of only focusing the tree — the panel was previously unresponsive to overlay clicks (#16).

### Added
- The map **remembers your tree layer choices and bay labels across sessions** (localStorage) — bays/crops/infra you turned on for a paddock, and the labels you picked, come back on reload. "Clear layers" forgets them; deleted objects are pruned. (#36, Peter request 2026-07-19.)

## 2026.7.37 — RE01 #29: infrastructure as a 4th event target (DEV)

### Added
- Infrastructure (channels, pumps, drains…) is now a **selectable event target** on the RE01 record map — toggle the Infrastructure layer, click a feature. New `field_events.infrastructure_id` (additive/nullable migration). Infrastructure is **farm-level** (no paddock parent), so these events carry a NULL `paddock_id` and hang under the farm (Peter, 2026-07-19). Geometry resolves from the infrastructure feature. New test in `tests/test_event_target_geometry.py`.
- `/api/spatial/infrastructure` now includes `farm_id` in feature properties (needed to stamp the event's farm).

## 2026.7.36 — RE01 Sweep A: event data integrity + record-form UX (DEV)

### Fixed
- Bay/crop-targeted events now store the **sub-area's own geometry and area**, not the parent paddock's — `_insert_event_row` resolves geometry+area from the target's table (bay/crop_zone/paddock) instead of COALESCEing to the paddock boundary and taking area from the paddock-only client payload (#22/#23/#26). New `tests/test_event_target_geometry.py` (fails pre-fix).
- Removed dangling `existingEventsSection`/`newEventDivider`/`existingEvents` DOM lookups (orphaned by the Map V1 retirement) that threw mid-selection; guarded `renderExistingEvents` (#18).
- Operator now shows in the Review/edit form for **all** event types, not just chemical/nutrient (#24).

### Changed
- Bay/crop layers `bringToFront()` when toggled so their clicks win over the paddock fill (#18).
- Operator field defaults to the logged-in user via a new `__CURRENT_USER__` template value (#20).
- **Save** now closes the form and deselects the map object (`clearTarget`) (#21); added a **Cancel** button distinct from Clear (#19).

## 2026.7.35 — RE01 weather via the fleet sibling-pull + reusable sibling primitive (DEV)

### Added
- RE01 desktop weather capture now reads the **Weather addon** over the fleet internal sibling-pull — new `/hfm/api/weather/{endpoint}` proxy discovers Weather via the Supervisor and pulls `/api/{readings-history,local-stations,openmeteo-station}` with the `X-Ingress-Path` header (allowlisted, fail-soft). It was previously hitting a browser `/weather/` path that never reached the sibling addon. (Verified live: Weather `449b641d` returned real station readings.)

### Changed
- Extracted the sibling-pull into a reusable `core/helpers.py` primitive (`discover_sibling_addon` / `sibling_get`, reads-only, SSRF-contained); the Store-products proxy now uses it too.

## 2026.7.34 — RE01 products from the Store addon (fleet internal sibling-pull) (DEV)

### Added
- RE01 product picker now reads the **Store addon's catalogue** — new `/hfm/api/store-products` discovers the Store addon via the Supervisor and pulls its `/api/hfm/products` over the fleet internal sibling-pull (`X-Ingress-Path` header; see `FLEET_ROLES.md`). Fail-soft to Farm-local `hfm_products` when Store is absent/unreachable.
- When Store is installed, RE01's "add product" shows **"add product in Store first"** instead of a local form — Store owns the catalogue. (Verified live: Store `f82faf9d_paddisense-store` returned its real product catalogue.)

## 2026.7.33 — RE01 event-recording fixes + select bays/crops + weather + Map V1 retired (DEV)

### Added
- RE01 record map: select **crop zones & bays** as targets (parent paddock carried so events still hang in the V2 tree); new `field_events.bay_id` column.
- RE01 desktop **weather capture** (start/mid/end from the Weather addon) — parity with mobile.
- `season_id` captured at record time (server derives it from the event date, not only the boot backfill).

### Fixed
- Applicator dropdown reads the live `/hfm/api/applicators` (was empty). (Products picker is unchanged — still pending the Store-addon integration.)
- Config add-applicator no longer writes `[object PointerEvent]` into the attribute field.
- Application method derived read-only from the selected applicator (removed the duplicate field); duration entered as hours + minutes; black focus-box on a clicked paddock removed; Home button → hub.

### Removed
- Retired Map V1 (`/map`, MP01) + `static/map/js/` modules; links repointed to Farm Map V2 (`/farmmap`).

## 2026.7.32 — Clear pre-existing mypy 1.16.0 type-debt (unblocks the release gate)

### Fixed
- Resolved 29 pre-existing `mypy==1.16.0` errors (release Gate 3) with
  behavior-preserving type-only fixes: `os.environ.get("FARM_x") or
  os.environ.get("GIS_x", "d")` chains rewritten to the trailing-literal form
  mypy narrows to `str` (identical runtime value); `_build_layers` annotated
  `int | None` to match its existing whole-box behavior. No runtime change.
  Ships together with the 2026.7.31 security hardening below (never publicly released).

## 2026.7.31 — Security-hardening release (5-agent red-team + Golden Rules v2.50 re-baseline)

### Security
- **Plaintext secret closed:** kb `/api/ndvi-credentials` no longer writes the CDSE
  OAuth `client_secret` to `/data` in cleartext — it now uses the Fernet-encrypted
  config store the fetcher already reads (F-D1).
- **Zip-bomb caps (SEC-25):** the machine shapefile + ISOXML importers and KB-pack
  extract now bound ACTUAL decompressed bytes (`read_zip_entry_capped`), and KB
  extract uses `Path.is_relative_to` instead of a sibling-escapable `startswith`
  traversal check (F-C1/C2/C3).
- **Rate-limiting** extended to the expensive PostGIS geometry ops, bulk export, and
  import commit (F-E4).
- **Attribute-breakout XSS** hardened: the three map surfaces' `esc()` helpers are now
  quote-safe and de-duplicated (CSP-contained before; defense-in-depth) (F-B1/2/3).
- **Error buffer** redacts secrets before storing; dead `error_tracker.py` removed (F-D2).
- **Rule 155:** Pillow 12.2.0 → 12.3.0 (8 CVEs); `pip-audit` clean.

### Docs
- AUDIT.md re-baselined to Golden Rules v2.50; stale ❌ rows reconciled (R173/R178
  closed, R174 partial); tenancy findings ruled N/A (single-owner-per-box). Auth
  signed-licence/access-sync hardening (F-A1/A2) filed for coordinated fleet work.

## 2026.7.30 — WR-PS-183: redactor re-vendored (all six GitHub token classes)

### Changed
- **The vendored log redactor re-synced byte-identical to the patched
  canonical**: `gh[posur]_` now masks `ghp_`/`gho_`/`ghs_`/`ghu_`/`ghr_`
  alongside `github_pat_` (WR-PS-183 completeness sliver). Shared test
  refreshed (+4 fixtures).

## 2026.7.29 — WR-PS-108 fleet flip: access-sync enforce ON by default

### Changed
- **Unsigned or invalid grant pushes are now rejected with 403.**
  `FARM_ACCESS_SYNC_ENFORCE` defaults ON (`=0` kill-switch — code-default
  pattern, grower boxes have no env plumbing). Core's signed pushes have been
  verifying and pinning since the receiver landed; this closes the warn-only
  window fleet-wide (WR-PS-108, Peter's go 2026-07-17). A `bound_fp` mismatch
  already failed closed before this flip.

## 2026.7.28 — WR-PS-108: access-sync verify-and-pin (§9-A.9 receiver)

### Added
- **WR-PS-108 / §9-A.9: the Core→add-on grant push is now verified-and-pinned.**
  Core signs every `POST /api/access/sync` with its box Ed25519 identity; this
  receiver now verifies the signature, authenticates Core's key against the
  `bound_fp` Admin signs into this add-on's licence (never bare TOFU), checks
  the freshness window and single-use nonce, and pins the key. A `bound_fp`
  mismatch fails closed ALWAYS — even in warn-only; an unsigned/invalid push
  is warn-only until `FARM_ACCESS_SYNC_ENFORCE` (the coordinated fleet flip).
  `bound_fp` is persisted from the activated licence. Copied from the
  SugarSense v2026.7.12 reference; 7 behavioural tests (forged signature,
  cross-target replay, nonce replay, expiry, fp mismatch).

## 2026.7.27 — SEC-14: escape bay-label tooltip on Map V2 (stored-XSS fix)

### Fixed
- **Map V2 per-bay labels no longer render grower-supplied names as HTML.** `farmmap.html`
  `applyBayLabel` bound the label tooltip (`bindTooltip(parts.join)`) without escaping — a bay
  named `<img src=x onerror=…>` executed for any manager who showed labels. It was the one
  `bindTooltip` sink the v.65 SEC-14 sweep missed (every sibling already used `esc()`). Now
  `esc(parts.join("\n"))`. `tests/test_map_xss.py` 3/3 green (the structural fence caught it —
  red before, green after). Flagged by P from the WR-PS-179 Farm lap.

## 2026.7.26 — Boundary map: less dark-edge flash when panning satellite

### Changed
- **`/match` boundary map keeps a wider ring of loaded tiles while panning** (`keepBuffer` 4, was
  Leaflet default 2). The flex layout pop was already fixed at v7.6; this addresses the residual
  tile-load lag on the slow Esri satellite layer — a hard pan shows less dark leading edge before
  new tiles paint. JS-only, one line (WR-PS-114). Some lag on satellite is inherent.

## 2026.7.25 — WR-PS-179: log redactor re-vendored from the fleet canonical + uvicorn bypass closed

### Changed
- **`core/log_redact.py` is now byte-identical to the canonical
  `documentation/shared/log_redactor.py`** (GSM⊕Core superset) — Farm was on
  the old 5-pattern 43-line version, so it gains DSN/`enc:`/labelled-secret/
  portal/Resend coverage plus email + phone PII masking. API is a superset;
  the `RedactingFormatter` import is unchanged. Shared 30-case behavioural
  test adopted.

### Fixed
- **uvicorn.access/error bypassed redaction.** uvicorn's own logging
  dictConfig attaches non-propagating handlers, so its loggers never passed
  through the root RedactingFormatter. `log_config=None` (the Core/PWM
  pattern) routes them through it.

## 2026.7.24 — Map V2: per-bay map labels (up to 2 attributes)

### Added
- **Each bay can show up to 2 attribute labels on the map.** Expand a bay in the tree → pick
  Label 1 and Label 2 (Name / Area) → the chosen values draw as text on the bay when it's
  shown. Follows the object→label→attribute model.

## 2026.7.23 — Map V2: individual bays in the tree, each with its area

### Changed
- **The tree lists each bay individually** (name + ha) under its field, instead of a single
  "Bays: N" count. Tick a bay to show just that one on the map; a split's new bays each appear.
  `/api/tree` returns bays as a list; new `GET /api/spatial/bays/{id}` for the per-bay toggle.

## 2026.7.22 — Map V2: edit & cut bays/crop zones; fix stale selection after ops

### Added
- **Edit** (drag vertices) and **Cut** (draw a polygon to subtract) tools on the Bays and
  Crop-zone tabs. `PUT /api/spatial/bays/{id}/boundary` + `/crop-zones/api/zones/{id}/boundary`,
  `POST .../{id}/cut` (operator role).

### Fixed
- After a split/cut/edit the active selection is cleared and the overlay redrawn, so the next
  geometry op targets a fresh object (fixes tools "working sometimes" after the first cut).

## 2026.7.21 — Map V2: split bays & crop zones with a line

### Added
- **Split tool on the Bays and Crop-zone tabs** — click a bay/zone, pick Split, set the
  bank/levee width (adjustable metres), draw a line across it, and it slices into two, each a
  new object under the same paddock. Bays reuse the crop-zone split geometry (Shapely).
  `POST /api/spatial/bays/{id}/split` (crop zones already had the zone split).

## 2026.7.20 — Map V2: buffer (grow/shrink) bays & crop zones

### Added
- **Buffer tool on the Bays and Crop-zone tabs** — click a bay/zone on the map, pick Buffer,
  enter metres (+ grow, − shrink), Apply. Buffered in the local UTM projection so the distance
  is true metres, not distorted lat/lon; a shrink that would erase the shape is refused.
  `POST /api/spatial/bays/{id}/buffer` + `/crop-zones/api/zones/{id}/buffer` (operator role).

## 2026.7.19 — Map V2: copy the selected paddock to a bay / crop zone

### Added
- **Paddock tab → "→ Bay" and "→ Crop"** copy the *selected* paddock's boundary into a new
  bay or crop zone — per-paddock (the starting point for cutting it up), not wholesale.
  `POST /api/spatial/paddocks/{id}/copy-to-bay` and `.../copy-to-crop` (operator role).

## 2026.7.18 — Map V2: click a layer → its tab + tree node; layer colours as tokens

### Added
- **Clicking a bay / crop-zone / infrastructure / event on the map** switches to that layer's
  tab (right tools ready) and highlights + scrolls to its node in the tree.

### Changed
- **Paddocks draw dark orange** for contrast with overlays. All Farm map-layer colours moved
  to `--gf-*` tokens in `app.css` — one place to change them. farmmap reads them via
  `getComputedStyle`; match/desktop/mobile to follow. (Kept Farm-local for now; promote to the
  master theme via A-Claude when the fleet needs to share them.)

## 2026.7.17 — Map V2: tree-driven layer toggles (Phase 2)

### Added
- **Tick a tree node to show it on the map** — bays, crop zones, infrastructure and events
  each get a live-toggle checkbox (tick draws, untick removes). Paddocks stay the always-on
  bottom base. The filter bar plus new **Select all** (visible) and **Clear** buttons make
  bulk selection fast. Overlays are fetched per-field where applicable.

## 2026.7.16 — Map V2: paddocks are the only always-on layer

### Changed
- **Map V2 loads only the paddock boundaries by default** (the clickable base). Bays, crop
  zones and infrastructure no longer auto-draw on load. The auto-created full-paddock crop
  zones (one per paddock, `source='auto'`, empty) had been piling on top of every paddock —
  duplicating the outline and stealing map clicks from the tree selection. Overlays will be
  added from the tree (Add-to-Map, next phase). Fixes the duplicate-polygon and broken
  click→tree on Map V2.

## 2026.7.15 — Fix: editing a paddock on Map V2 left a duplicate polygon

### Fixed
- **Saving a boundary edit on Map V2 now redraws the map from the database** (like Cancel
  already did). `saveEdit` updated the DB + tree but never reloaded the paddock layer, so the
  pre-edit shape lingered as a second polygon and the map's click→tree selection went stale
  for other paddocks. Also clears leftover draw-mode state on save.

## 2026.7.14 — Fix: BM01 "Assign Farms" button was white-on-white

### Fixed
- The BM01 "Assign Farms" button had no background modifier, so its white `.btn` text sat on
  a white background (invisible). Gave it a distinct `--ps-info` background.

## 2026.7.13 — BM01: one-click "Assign Farms" + correct "In Core" status

### Added
- **BM01 "Assign Farms" button** files every farm-less Core paddock under its owner + farm
  in one click, matched to the machine staging by name (`/gsm/api/backfill-core-farms`) — no
  boundary changes. Avoids removing + re-adding paddocks already in Core just to backfill.

### Fixed
- **The Machine column no longer shows "Add to Core" for paddocks already in Core.** It now
  keys off the name match (`row.core`) instead of the backend's name+farm match, which missed
  Core paddocks that had no farm yet.

## 2026.7.12 — BM01 Grower column + owner captured on the real sync path

### Added
- **BM01 (`/match`) now shows a Grower column**, so each row reads Grower ▸ Farm ▸ Paddock
  across the machine / Core / GSM layers. The owner comes through the `machine-paddocks` API.

### Fixed
- **The owner is now captured on the path the sync actually uses** — `_stage_sync_output`
  (→ `upsert_provider_field`), sourced from the registry's business (grower) record via the
  farm's `business_id`. v2026.7.10's change was on a fallback staging path the sync doesn't
  call, so no owner was recorded. With this, a re-sync records the grower on every staged
  field, and accepting machine→Core (v2026.7.11) files paddocks under Owner ▸ Farm.

## 2026.7.11 — Machine→Core transfer files paddocks under their owner + farm (BM01)

### Fixed
- **The BM01 machine→Core transfer (`/gsm/api/accept-machine-boundary`) now creates the
  owner (grower) + farm and sets the paddock's `farm_id`.** Previously it linked a farm only
  if one already existed and never created the owner, so Core paddocks landed farm-less —
  the Map V2 tree stayed empty even though BM01 showed the machine farm name. Both create and
  update paths are covered; the update path **backfills `farm_id`** onto paddocks already in
  Core. Owner/farm are sourced from the machine sync (`provider_fields.grower_name`/
  `farm_name`), so the Map V2 tree now reflects the same Owner ▸ Farm ▸ Field that BM01 shows
  as Core. (v2026.7.10 wired the same owner-awareness into the Import-Hub promote path; this
  puts it on the primary BM01 workflow.)

## 2026.7.10 — Farm owner (grower) flows from the machine sync into the map tree

### Fixed
- **Imported paddocks now file under their owner + farm in the map tree.** The machine
  (CNH/JD) sync now carries the **grower/owner** alongside the farm name, and the shared
  promotion path creates the Postgres grower + farm (linked via `grower_id`) and assigns
  each paddock's `farm_id`. So Map V2's side menu shows **Owner ▸ Farm ▸ Fields** instead
  of a blank tree. Root cause: nothing ever populated the `growers` table and farms were
  created owner-less. Provider-agnostic — CNH grower / JD org supply the owner; shapefile
  imports may leave it blank (the farm then shows ungrouped). Migration adds
  `provider_fields.grower_name`. Map V2's tree now surfaces a load error instead of
  silently blanking.

## 2026.7.9 — Map V2 now shows its page ID (MP02)

### Added
- **Map V2 (`/farmmap`) displays `MP02`** in the top bar, styled to match V1's `MP01` badge.
  Disambiguates the two Farm-Map implementations (V1 `/map` = MP01) while V1 is still in the tree.

## 2026.7.8 — Spatial export: whole-box scope (exports unassigned paddocks)

### Changed
- The spatial export now offers **"All farms (whole box)"** and `farm_id` is optional on
  `GET /api/spatial/export`. Provider-promoted (CNH/JD/Trimble) paddocks arrive with **no farm
  assigned** (`farm_id` NULL), so the farm-only picker hid them; whole-box mode exports every
  paddock / bay / infrastructure feature regardless of farm assignment. Verified live against
  45 CNH-imported paddocks (`all-farms-spatial-*.zip`, POLYGON, WGS84).

## 2026.7.7 — Spatial export: download farm geometry as shapefiles

### Added
- **"Export Spatial Data" on the Import Hub** — pick a farm and layers (paddocks / bays /
  infrastructure) and download an Esri Shapefile ZIP (WGS84 / EPSG:4326), one shapefile per
  layer, for QGIS/ArcGIS or re-import. `GET /api/spatial/export?farm_id=&layers=` (manager
  role), with a `.../export/layer-counts` helper that disables empty layers in the modal.
  Infrastructure is split by geometry type (point/line/polygon) per shapefile rules; DBF field
  names are ≤10 chars with a full data dictionary in the bundled `manifest.json` + `README.txt`;
  `attributes` rides along as a JSON string. Paddocks fall back to the `boundary` GeoJSON when
  the PostGIS `geom` is NULL, so provider-promoted (CNH/JD/Trimble) fields export correctly.
  Pure-Python (pyshp) — no GDAL binary.

## 2026.7.6 — Fix: boundary map no longer flickers the table panel while panning

### Fixed
- **Panning the Paddock Management (`/match`) map shoved the table panel in and out**
  (with a strip of page background showing). `#map` is a flex item, which defaults to
  `min-width:auto` — it cannot shrink below its own content width. Leaflet keeps loaded
  tiles in the DOM while you drag, so the map's intrinsic width outgrew the flex row and
  pushed the table panel out; when Leaflet pruned the tiles it snapped back (worst on
  satellite, whose tiles linger). Clamping the map flex item (`min-width:0` +
  `overflow:hidden`; the row already had `overflow:hidden`) makes the map obey the layout
  regardless of tiles in flight, and tile images are barred from starting a native drag
  ghost. Same one-line class of fix as PWM W04 v2026.7.42. Farm's events map was never
  affected — it is absolutely positioned and cannot push a sibling.

## 2026.7.5 — Fix: /health now emits canonical `db_ok` (H01 hub-health drift)

### Fixed
- **Public `/health` now emits a top-level `db_ok` boolean** alongside the existing
  `database.connected` (kept for back-compat). Core's fleet heartbeat collector
  (`heartbeat.py:_poll_addon_health`) computes `ok = status=="ok" AND db_ok`, so with the field
  absent Farm reported UNHEALTHY on every 5-min heartbeat and showed RED on Core's hub (H01)
  despite being fine. Every other verified addon already emitted `db_ok`; this closes Farm's
  dialect drift (Peter-directed 2026-07-10, no Core-side tolerance). Regression: the `/health`
  smoke test now asserts `db_ok` present + boolean — pre-fix that assertion fails (the response
  had no such key).

## 2026.7.4 — Fix: real Admin-signed instructions were rejected (WR-ADMIN-006 canonical re-vendor)

### Fixed
- **Re-vendored `core/licence_verify.py`** byte-identical to the fixed canonical
  (`documentation/shared/`, commit 23378e0): `verify_artifact` now accepts the licence id under
  `target` (the real instruction wire shape, §4/§9-A.5.2) as well as `licence_id` — pre-fix, every
  REAL Admin revoke/deactivate was rejected as `invalid_signature` (latent since 2026-07-01; found
  by A's WR-ADMIN-006 live test; GSM proved the fix end-to-end on v2026.7.51). Log labels split so
  a missing id no longer mislabels as a sig/replay failure. New positive regression
  `TestPositiveInstruction` (Rule 106): a genuinely signed, target-only instruction MUST verify —
  the missing test whose absence let an always-reject verifier pass every gate.

## 2026.7.3 — Warn→block flip: signed-licence enforcement ON by default (SEC-01/04 receive-side)

### Changed
- **`FARM_SIGNED_LICENCE_ENFORCE` now defaults ON** — unsigned `/api/licence/activate` and
  `/api/licence/deactivate` are rejected (400); the Admin Ed25519 signature is the authorisation,
  never the /23 transport (§9-A). Closes the naked-deactivate hole. Readiness: Admin signs every
  licence fleet-wide (v2026.7.52 re-issue, 2026-07-12); present-but-bad signatures were already
  always fatal. `=0` = emergency kill-switch (grower boxes have no env plumbing — the code default
  IS the fleet flip). Tests: default-rejected + kill-switch pairs on both endpoints (+4).

## 2026.7.2 — Fix: Core's grant push was CSRF-blocked (found live, Rule 106)

### Fixed
- **`/api/access/sync` added to the CSRF exemption list.** Core's cookie-less machine-to-machine
  grant push (WR-PS-109) was intercepted with a CSRF 403 before reaching the endpoint — the same
  exemption the licence push already has (no browser session in play; `_verify_internal` + the
  tracked §9-A.9 signature are the boundary, and CSRF protects cookie sessions, which this request
  never carries). Found by probing every receiver live after deploy; four addons had the gap.
- **Regression test** (`TestSyncEndpointReachable`) drives a cookie-less POST through the REAL
  middleware stack and asserts it reaches the endpoint — the class of gap the original e2e tests
  (GET-only) could not see.

## 2026.7.1 — WR-PS-090 Ask 4: box-key read diagnostic (PWM reference adopted)

### Changed
- **`core/db/_pool.py::_read_shared_db_key`** now logs every key read — source path, SHA-256
  fingerprint (12 hex), and mount identity (`dev`/`ino`/`size`/`mtime`) — and WARNs on every
  fallback instead of silently passing. The local-`/data`-key fallback in `_derive_app_password`
  (the branch whose derived password can never match the role Core minted) now WARNs explicitly.
  This is the diagnostic that cracked the 2026-07-06 fake-`/share` incident (WR-PS-090) and the
  WR-PS-110 key churn: a consumer's logged `fp`/`dev` can be cross-checked against Core's.
  First July cut — CalVer rolls 2026.6.71 → 2026.7.1.

## 2026.6.71 — Hone PS-SEC-09 (WR-PS-096): role gates on the 25 remaining import/kb/ndvi/draft mutations

### Fixed
- **Applied Peter's role table (2026-07-09) to the SEC-09 residual** — the mutating routes that carried
  no role check. Any signed-in user (incl. a viewer) could previously drive them:
  - **operator** (22): all import_hub staging + upload actions (upload, re-detect, dismiss, restage,
    resolve-overlaps, detect-zones, geojson/attributes edit + reset, merge/explode/simplify/cut/split,
    cut-zones, clean-slivers, stage-cnh, preview, detect-mapping), ndvi fetch, and the 2 hfm draft
    writes (per-device working data).
  - **manager** (3): import_hub `execute` (commit staged → canonical, irreversible), kb `cache/clear`,
    kb `download`.
  - **Bulk reads unchanged** — every GET is viewer-readable by design; a viewer-level gate is a no-op.
  - **Ingress-trust question out of pilot scope** (Peter) — the accepted single-operator model,
    revisited at scale-out; separate from these per-action gates.
- Five handlers gained a `request: Request` param so the guard can run.

### Tests
- `tests/test_role_gates_import.py` — behavioural denial tests (R154): a viewer is refused 403 on an
  operator staging route, the manager `execute`, and ndvi fetch; an operator is refused `execute` but
  passes a staging route. Plus a **structural fence** (R192) asserting the ONLY ungated mutations left
  are `login_post` and the cosmetic `save_device_prefs` — so a new mutation can't land ungated.

## 2026.6.70 — Rotation self-heal for the request-path DB pool (incident 2026-07-09, Rule 106)

### Fixed
- **farm_app DB pool self-heals across a box-key rotation.** When Core rotates the box key
  (`db_role.key`, WR-PS-088 / ADR-013) the farm_app password changes; a long-running pool holds the old
  one, so the next fresh connection fails auth and Farm breaks until a manual restart — impossible on a
  grower box. `_acquire_app_conn` now treats a `password authentication failed` as a stale key: drops
  the pool, rebuilds (re-reads `/share/paddisense/db_role.key`), retries once; a second failure
  propagates. Admin/superuser pool untouched (R173). Fleet-wide fix from the live PWM incident.
  `tests/test_pool_selfheal.py`.

## 2026.6.69 — Hone SEC-04/SEC-09 (Option B, Peter 2026-07-09): per-add-on access enforcement — FARM REFERENCE

### Added
- **Farm now enforces per-user add-on access (`core/module_gate.py`).** Previously any HA-ingress
  request was handed a full admin session, so a user Core never granted Farm could operate it by
  opening the ingress URL directly (Hone SEC-04, and the root of the SEC-09 role-check gap). Core
  owns the grant but fails closed against sibling calls, so it **pushes** the grant set to Farm
  (`POST /api/access/sync`, `_verify_internal`-gated) and Farm enforces locally from a durable cache.
- **The gate runs in `auth_middleware` for INGRESS requests** (`_access_gate_denies`): it resolves the
  HA user from the `X-Remote-User-Id` header and refuses (403) a user with no Farm grant. Decision
  semantics mirror Core's `effective_modules` exactly. A direct cookie login keeps its existing role
  path — the gate targets the ingress auto-admin vector only.
- **Resilience / grower-owns-the-system:** the cache is a durable `/data` file. Never synced → open
  (bootstrap, matches Core's unconfigured→all); a Core OUTAGE uses the last-known grant (still
  enforced) so a Core hiccup never bricks the box; a corrupt cache is treated as unsynced (open, not
  locked out). **Non-breaking until Core pushes** — with no grants file, the gate is open, so this
  ships safely ahead of the Core pusher.

### Tests
- `tests/test_module_gate.py` — 11 behavioural tests (Rule 192): the full decision matrix
  (never-synced / no-entries / granted / ungranted / all-access / unresolved / corrupt-cache) plus
  end-to-end middleware tests that drive the real ingress path and assert an ungranted user gets a
  real 403 on both a page and an API route. Negative control verified: neutering the gate lets the
  ungranted user through and the deny tests go red.

### Follow-ups (this is the reference; fleet work tracked)
- Core pusher (push grants to each installed add-on on change + periodically) — next, same session.
- Propagate the gate to the other nine add-ons via the shared-auth pattern — WR to file.
- Harden the Core→add-on push with an authenticity signature (applies equally to the existing
  licence-forward path, so a uniform improvement not a regression) — WR-PS-108.

## 2026.6.68 — Hone PS-SEC-25: ZIP decompression bound no longer trusts declared sizes

### Fixed
- **`check_zip_safety()` trusted attacker-controlled sizes (Hone PS-SEC-25).** It read
  `file_size` / `compress_size` from the ZIP central directory to enforce its per-entry,
  ratio and aggregate caps — but both fields are attacker-declared, so a crafted archive can
  claim small sizes and slip past every check. Confirmed empirically: a bomb with edited
  central-directory metadata returned `None` (safe) from the pre-check. On the current base
  image Python's own CRC / overlapped-entry detection catches the over-read, but that is a
  guard we do not own and are about to change (Hone SCAL-03 moves the Python base).
- **New `read_zip_entry_capped()` enforces the ceiling on ACTUAL decompressed bytes.** It
  streams each entry in 1 MB windows, counts bytes as they are produced, and aborts the moment
  output exceeds the cap — trusting no declared size and no interpreter read-side guard. Both
  shapefile ZIP read paths (`_parse_shapefile`, `read_shapefile_features`) now route their
  `.shp`/`.dbf`/`.shx` entries through it before handing them to pyshp. `check_zip_safety` is
  kept as the cheap first line for honest bombs, now documented as advisory-only.

### Added
- `tests/test_zip_bomb_cap.py` — 5 behavioural tests (Rule 192): an under-cap entry round-trips
  exactly; an 8 MB entry against a 1 MB ceiling raises; an entry whose central directory
  *under-declares* its size is still refused (cap measures real output); the default cap is the
  aggregate ceiling; and the honest-bomb ratio pre-check still fires. Negative control verified:
  removing the running-total check turns the over-cap test red.

### Assessed, not changed — the filename-trust half of PS-SEC-25
- File-type routing is by extension (`_ALLOWED_EXTS`, `parse_file` suffix dispatch). Deliberately
  left as-is: only the `.zip` path decompresses, and it is now byte-capped; the CSV/JSON/PDF/
  shapefile parsers fail safe on wrong content without expansion or execution. A disguised zip
  uploaded as `.csv` is read as latin-1 text, not decompressed. Hard content-sniffing every
  upload would reject a grower's legitimately mis-named file — a "grower owns the system"
  regression not worth the marginal gain.

## 2026.6.67 — Hone PS-SEC-18: at-rest decrypt now fails CLOSED

### Fixed
- **`core/crypto.py::decrypt()` passed ciphertext through on decrypt failure (Hone PS-SEC-18).**
  An `enc:`-prefixed value that would not decrypt — wrong/rotated master key, corruption,
  tampering — was caught by a bare `except Exception` and **returned to the caller as the
  ciphertext** (`"enc:gAAAA…"`) with only a `log.warning`. Callers then used that string as a
  live credential: `machine/db.py` (CNH/JD OAuth access + refresh tokens), `ndvi/fetcher.py`
  (CDSE client id/secret) and `gsm/db.py` (GSM shared secret) — so it flowed into outbound API
  calls, HMAC inputs and logs. A key mismatch silently degraded "encrypted at rest" into "secret
  material handed out in the clear". `decrypt()` now returns `""` so the caller degrades as if no
  credential exists (Rule 127/141), logs at ERROR, never logs the ciphertext (Rule 88/164), and
  never raises into a request path (Rules 121/141). Legacy non-`enc:` plaintext still passes
  through unchanged.
- Narrowed `except Exception` to `(InvalidToken, ValueError, TypeError)` (Rule 62). `InvalidToken`
  is lazy-imported to preserve the module's deferred `cryptography` import.

### Added
- `tests/test_crypto_fail_closed.py` — 5 behavioural tests (Rule 192) against a real Fernet key:
  round-trip, legacy plaintext, tampered token, wrong key, garbage `enc:` value. Negative-control
  verified: restoring the old `return value` turns three of them red.

## 2026.6.66 — Hone PS-SEC-09: minimum-role checks on spatial state-changing actions

### Fixed
- **Three spatial mutations shipped with no role check (Hone PS-SEC-09, HIGH, P1).** Any
  signed-in principal — including a `viewer`, the lowest role — could call them. Gated to
  match the protection already present on comparable actions in the same file:
  - `POST /api/spatial/paddocks/{id}/link-gsm` → **manager**. Re-linking rebinds a paddock to
    GSM's corporate identity (R30); the rest of that identity family (promote / demote /
    disconnect in `gsm/routes.py`) is already manager-gated.
  - `POST /api/spatial/paddocks/{id}/sampling-grid` → **operator**, matching `POST
    /infrastructure` and `POST /bays` (create spatial working data).
  - `DELETE /api/spatial/sampling-grids/{id}` → **operator**, paired with its create. A grid is
    regenerable working data, not a structural entity — farm/crop/season/paddock deletes stay
    manager-gated.

### Added
- `tests/test_role_gates_spatial.py` — 7 tests (R154: authorization without a denial test is
  unverified). Five drive the real handlers through the real middleware with a signed session
  + CSRF token and assert the under-privileged principal gets **403**. Two assert the *entitled*
  principal is **not** refused (`!= 403`, since the fixture paddock need not exist) — the fix
  must not lock the grower out of their own farm. Negative-control verified: removing the three
  gates turns all five denial tests red.

### Known gap — NOT closed by this release, needs a role-matrix decision
- The audit that found these three swept all 248 routes by AST. **31 further mutating routes
  carry no role check**, the bulk of them `import_hub/*` (upload, staging edit/merge/split/
  explode, execute) plus `kb/api/cache/clear`, `kb/api/kb/download` and `ndvi/api/fetch`.
  They are authenticated (`/api/*` is 401 without a session) but not authorized, so a `viewer`
  can drive a boundary import or spend CDSE imagery quota. Gating them is a product decision
  (which role owns the import workflow?) with real lock-out risk, so it is deliberately NOT
  done here. Bulk **reads** are intentionally ungated — every `GET` in `api/spatial.py` is
  viewer-readable by design, and Hone's read exposure is a consequence of PS-SEC-04's ingress
  auto-admin, not of a missing role check.

## 2026.6.65 — Hone PS-SEC-14: stored XSS via grower-supplied map labels

### Fixed
- **Stored XSS on every map label surface (Hone PS-SEC-14, HIGH, P1).** A paddock/zone/bay
  name arriving from a GSM boundary push or an Import Hub upload is attacker-influenced.
  Leaflet's `bindTooltip` content and `divIcon`'s `html` option parse markup, so a name
  containing script ran in the browser of any manager who opened the map and showed labels.
  The named sink is `static/map/js/labels.js` (`html: '<div>' + name + '</div>'`); the sweep
  found the same class in `layers.js` (label renderer + label-modal field names, which derive
  from imported GeoJSON property KEYS), `crops.js`, `gsm.js`, `tools.js`, `split.js`,
  `farmmap.html` (3 tooltips), and `record-desktop.html`. All now route through an escaper.
- `js/util.js` (new, loaded first) exports `PS.esc()` — escapes `& < > " '` so it is safe in
  BOTH text and quoted-attribute contexts (`layers.js` interpolates a property key into a
  `data-field="…"` attribute). Replaces nothing; the six pre-existing per-file `esc()` copies
  in the standalone pages stay local to those pages (Rule 59 — the modules now share one).

### Added
- `tests/test_map_xss.py` — 3 tests. Two drive the real modules under Node with stubbed
  Leaflet/DOM and assert an `<img src=x onerror=…>` paddock name is neutralised in the emitted
  HTML (Rule 192 — behaviour, not string presence); the third is a structural fence so a new
  markup sink cannot land unescaped. Negative-control verified: reintroducing the vulnerability
  fails both the behavioural test and the fence.

### Known gap
- Hone also recommends sanitising free-text on the way in as a second layer. `POST
  /api/spatial/paddocks` still stores the name verbatim (correct for data fidelity — `&` and
  `<` are legal in a paddock name). Output escaping is the primary and now-complete control;
  inbound sanitisation is deliberately NOT added, since escaping-on-store would corrupt names
  and double-escape on render.

## 2026.6.64 — Surface uploaded backups in the database admin UI list

### Added
- **`/api/admin/backups`** now also lists files matching `*paddisense-farm*.sql*` from `/config/uploaded data/` (via `_UPLOAD_BACKUP_DIR`). Each entry carries a new `source` field: `"upload"` (from `/config/uploaded data/`) or `"local"` (from `/homeassistant/backups/` or `/share/paddicore_backups/`). The admin database page's Restore button now surfaces Peter-uploaded encrypted backups so the operator doesn't have to know the URL.

### Rationale
v2026.6.63 added the decrypt+restore capability to `/api/admin/restore` but the admin UI at `/admin/database` only listed files from `_BACKUP_DIR`. Operators couldn't discover uploaded backups without knowing the URL. This closes the UX gap.

### Not changed
- Filter pattern is naming-scoped (`*paddisense-farm*.sql*`) to avoid leaking unrelated `/config/uploaded data/` files into the admin UI.

## 2026.6.63 — Restore encrypted backup (industry-box parity when Core absent)

### Added
- **`POST /api/admin/restore` now accepts `.sql.gz.enc`** (Fernet-encrypted daily backup shape) in addition to plaintext `.sql`. Peter-uploaded encrypted files at `/config/uploaded data/` are now a valid restore source (`_UPLOAD_BACKUP_DIR`; Farm already maps `- config:rw`). The three allowed source dirs (`/homeassistant/backups`, `/share/paddicore_backups`, `/config/uploaded data`) each stay traversal-safe via per-candidate resolve + prefix check.
- **`_decrypt_backup_bytes(filepath)`** helper — Fernet-decrypt + gunzip a `.sql.gz.enc` file in-memory. Reuses `core.backup._derive_fernet_key` so encryption is symmetric with the daily-backup encryptor. Plaintext is streamed to psql via stdin — nothing decrypted lands on disk.

### Rationale
On industry boxes where Core (and its backup admin UI) isn't installed, Farm was the only path to restore a backup — but its own `/api/admin/restore` only accepted plaintext `.sql`, leaving encrypted-backup restore literally impossible. This closes that gap. On grower boxes where Core IS installed, Core's backup UI stays the primary flow; Farm's endpoint is the fallback.

### Not changed
- No architecture change — `restore_backup` still requires admin role + `confirm=true`, still writes to `_DB_NAME` via psql, still logs the R171 privileged-action alert + audit row.

## 2026.6.62 — Prefer the dedicated shared database-role key during the key split rollout

### Changed
- Prefer the dedicated /share db_role.key for the *_app DB password; falls back to master.key during
  the WR-PS-088 split rollout — no behaviour change today.

## 2026.6.61 — Tidied up unstyled screen bits and switched on the release safety check

### Fixed
- Some on-screen pieces were using their own private style names that were never
  defined, so they showed up plain and unstyled: the Crop Type and Event Type drop-down
  filters on the GSM events screen, and the little success/error banners on the Import Hub
  page. These now use the platform's shared, consistent styles so they look right and match
  the rest of the addon.

### Changed
- Turned on the final pre-release safety check so it now genuinely blocks a release if any
  quality or security gate fails, instead of just reporting a warning. Nothing can be cut
  to growers unless every gate passes clean.

## 2026.6.60 — Proved that one operator can't see another's half-finished record

### Security
- Added a real test that proves a half-finished event record (a "draft") saved by one
  person on a shared tablet cannot be read or wiped by a different person who signs in on
  the same tablet — each operator only ever sees their own in-progress work. The protection
  was already built in; this pins it down with a test so it can never quietly break.
- Confirmed the throwaway test database rebuilds itself cleanly from scratch — dropped it
  entirely and the test suite recreated it, set up the low-privilege database account the
  live addon uses, and passed end to end. This keeps the security tests trustworthy.

## 2026.6.59 — Spatial rulebook now lives with the maps

### Docs
- Wrote the nine spatial/data-flow rules that govern paddocks, boundaries and machine
  data straight into Farm's own reference so anyone working on the map has them to hand:
  areas are always worked out before a paddock is saved; a paddock is one shape in one
  place; the boundary that came from head office is always kept; when the same paddock
  comes from a tractor, from head office and from a person, the tractor wins, then head
  office, then the person; the full round-trip (receive, pull, match, promote, send back)
  is described; paddocks are matched by how much their shapes overlap; and the grower's
  own name for a paddock and head office's name for it are both kept side by side.
- Recorded one honest wrinkle for a future tidy-up: the rulebook still says bays belong
  only to the watering side of the platform, but Farm now holds the master bay shape and
  the watering side reads it from here. Noted so the wording can be corrected, not glossed over.

## 2026.6.58 — ADR-010 flip-ready under Golden Rules v2.49 (fleet-consistency + full security-test manifest)

### Fixed (fleet consistency — check-fleet-consistency.py)
- **`config.yaml` map** now includes `addon_config:rw` (fleet-standard map set).
- **`core/db/_pool.py`** gains public `init_app_pool()` (fail-closed wrapper over `_init_pool`, R160/R173)
  and `close_pools()` (idempotent close of both admin+app pools, Rule 92/134).
- **`core/db/__init__.py`** `__all__` now exports the five lifecycle names (`get_conn`, `get_cursor`,
  `ensure_database`, `init_app_pool`, `close_pools`) — Rule 79.
- **`main.py` shutdown handler** now cancels Farm's own background poller tasks
  (`_ndvi_auto_fetch_loop` / `_kb_poll_loop` / `_auto_sync_loop` / `_daily_sync_loop` / `_digest_loop`,
  by coroutine name so the ASGI lifespan tasks are untouched) then calls `close_pools()` — no DB
  connection or poller outlives the event loop (Rule 92/134).

### Security tests (REQUIRED_SECURITY_TESTS — full applicable coverage, 8 tested + 4 N/A)
- **R159 (SSRF)** `tests/test_ssrf.py` — `gsm.client._validate_url` denies metadata (169.254.169.254),
  loopback, `localhost`, and every RFC-1918 range; refuses non-https downgrade.
- **R158 (bounded requests)** `tests/test_bounded_requests.py` — oversized body → 413 (via CSRF-exempt
  webhook so the size guard is the control), and a sensitive endpoint enumerated past budget → 429.
- **R187 (XFF ignored)** same file — a per-request forged `X-Forwarded-For` does NOT reset the per-IP
  rate bucket (limiter keys on the socket peer, not the header).
- **R142 (replay/nonce/timestamp)** `tests/test_hmac_replay.py` — signed `/gsm/api/receive-layer`
  rejects a stale timestamp (401) and a reused nonce (401 replay).
- **R171 (detect/alert)** same file — a forged HMAC raises an `hmac_*` security alert.
- **R190 (uniform login)** `tests/test_login_uniform.py` — wrong-password-for-existing-user and
  any-password-for-absent-user return byte-identical bodies (no username enumeration).
- **N/A with reason (docs/AUDIT.md):** R146 (no CSV/spreadsheet export path), R153 (single-tenant box,
  no per-principal object ownership), R188 (no in-app credential-change flow), R189 (no email flow).

### Audit
- Re-audited to Golden Rules **v2.49** (Wave-4a: Farm owns none of the relocated Category-A rules —
  R21/R23-R30/R33 → Core/GSM/PWM/SeedMgr/SugarSense). `docs/AUDIT.md` header + per-rule table refreshed,
  `last_audit_date=2026-07-04`. One real residual gap surfaced (R159 no dial-by-pinned-IP; R82 CDN SRI).

## 2026.6.57 — SEC-08/R173: read the shared /share box key for farm_app (fleet-standard, WR-PS-081)

### Security
- **`core/db/_pool.py::_derive_app_password` now prefers the shared `/share/paddisense/master.key`**
  Core publishes (WR-PS-081), falling back to the local `/data` key. Farm already ran least-priv
  (`farm_app`, fail-closed) using its `/data` key which coincidentally matched Core's; reading the
  shared key removes a latent fragility — if Farm's per-container `/data` key were ever lost and
  regenerated, `farm_app` would stop matching Core's minted role and the fail-closed pool would
  refuse to boot. Aligns Farm's key source with the rest of the fleet. Fernet-at-rest is unchanged
  (still the local `/data` key — separate path).

## 2026.6.56 — Licence activate consumes Core's heartbeat signed_licence (auto-heal fix)

### Fixed
- **`/api/licence/activate` now accepts Core's heartbeat `signed_licence` distribution, not just a
  pasted `code`.** The prior activate was code-only (`body["code"]` required), so when Core's
  heartbeat forwarded `{"signed_licence": {...}}` (no `code`, per `forward_targets`), Farm returned
  `400 Missing licence code` and **never re-licensed from the heartbeat** — the reason a wiped Farm
  licence didn't self-heal. New `_extract_licence(body)` (replacing `_enforce_licence_signature`)
  handles **both** shapes and verifies the Admin Ed25519 signature (fleet-standard, matching
  PWM/Store/Weather/etc.): prefers the signature-verified payload, falls back to the decoded code
  when legacy. Signature policy unchanged (legacy-tolerant behind `FARM_SIGNED_LICENCE_ENFORCE`).
  Tests: `test_heartbeat_signed_licence_body_bad_sig_rejected` + `test_empty_body_rejected`
  (`test_licence_signed.py`, 13 pass).

## 2026.6.55 — SEC-04: signed-instruction verify on licence deactivate (Hone PS-SEC-04 receive-side)

### Security
- **`/api/licence/deactivate` now requires an Admin Ed25519 signature** (`_enforce_instruction_signature`,
  `main.py`). Activate has verified the signature since v.36; deactivate did not — it accepted the naked
  `POST` on `_verify_internal`'s `/23` transport trust alone, which is exactly Hone **PS-SEC-04**
  ("unauthenticated deactivate") and the state `SIGNED_LICENCE_CONTRACT §9-A` explicitly retires. Core
  already forwards the signed instruction (`forward_targets` → `(slug,"deactivate",{signed_instruction})`);
  Farm just never verified it. Now both mutating licence paths are signature-gated: signature — not
  network position — is the trust boundary. Verifies `action ∈ {deactivate, revoke}`; legacy-tolerant
  during the fleet signing rollout (same `FARM_SIGNED_LICENCE_ENFORCE` flag as activate — present+bad sig
  always fatal, unsigned accepted until enforcement). The `/23` check is retained as defence-in-depth
  transport only (fleet-consistent with PWM/GSM). Closes the Farm receive-side of **WR-HONE-SEC-04** and
  supersedes WR-PS-038's obsolete Bearer/observation-cycle plan (per-addon Supervisor tokens are never
  shared cross-addon, so the "strong Bearer path" could never authenticate Core → the signed model
  replaced it).
- **Regression tests** (`tests/test_licence_signed.py::TestDeactivateApi`): unsigned+legacy → 200,
  bad signature → 400, no-transport/no-Bearer → 403 (R141/R154 negative test); + instruction-kind
  policy units. Full suite 47 passed / 5 skipped.

## 2026.6.54 — Season linkage + map→tree focus

### Fixed
- **Season linkage** — the seasons (CY25/CY26) had **NULL date ranges**, so no event/zone could map
  to one (everything showed "Unassigned"). `_backfill_seasons` now sets each CY-named season its
  crop-year range (rice CY = 1 Oct → 30 Sep) and links every event + crop-zone to the season whose
  range contains its date (171 events + 48 zones → CY26; heals each boot). The tree now groups by
  real year.
- **Map → tree focus** — clicking a paddock on the map now **collapses the rest of the tree and
  expands just that field** (its path + its own children), scrolls it to centre, and highlights it —
  so clicking SW5 on the map jumps you straight to SW5 in the tree.
## 2026.6.53 — Farm Map V2: full event inspector + map draw, home button, tree tidy

### Added
- **Full event detail** — new `GET /api/spatial/event/{id}` returns every attribute + the `data`
  JSONB extras + geometry. Clicking an event now shows the **complete RHS form** (RE01-style):
  products (name · rate · unit), water rate, application method, applicator, operator, timing,
  observation/reading/severity, crop/variety, notes — not just type/date/operator.
- **Events drawn on the map** in a distinct **orange** layer (with zoom-to) when selected, so they're
  visible against the paddock base.
- **Home button** (🏠 → `/hub`) in the map's top bar.

### Changed
- **Tree tidy** — NULL-season data no longer nests under a redundant "Unassigned" year node; it hangs
  directly under the field. (Everything is NULL-season until the season-linkage cleanup.)
- **Bigger, easier chevrons** — larger caret hit-area (22px) with hover, roomier rows.
## 2026.6.52 — Event geometry: backfill from paddock + capture going forward

### Added
- **Event footprints populated** — `field_events.geometry` was NULL for every event; GSM export was
  only *falling back* to the paddock boundary at send-time. Now a startup backfill
  (`_backfill_event_geometry`) fills `geometry` from the linked paddock's boundary (idempotent,
  heals every boot; 114/171 filled — the rest have no paddock link). GSM now sends the real column.
- **Capture going forward** — the HFM event INSERT now sets `geometry` at creation:
  `COALESCE(passed geometry, the paddock's boundary)`, so new events are never geometry-less and a
  real point/shape (when capture provides one) is stored as-is.
## 2026.6.51 — Farm Map V2: event inspector, filter, tree scroll

### Added
- **Event inspector** — clicking an event in the tree now shows its **attributes** in the right
  panel (type · date · product · rate · operator · observation · notes) and **highlights the
  paddock** it belongs to. Events have no geometry of their own (they're paddock-scoped), so the
  paddock *is* their place on the map. Tree event nodes now carry full attributes (`/api/tree`).

### Fixed
- **Filter hid children of matches** — a match on e.g. "chem" now reveals the matched node's whole
  **subtree** (its events), not just the node; matching is on each node's own label, and reveals
  ancestors + descendants.
- **Tree/analysis panels didn't scroll** — added `min-height: 0` to the flex/grid panels so a long
  tree scrolls within its panel instead of overflowing.
## 2026.6.50 — Farm Map V2: review fixes (map-click, focus outline, event naming)

### Fixed
- **Map click didn't highlight the tree** — the tree query used `p.visible = TRUE` (excluding
  NULL-visible paddocks that the map shows via `COALESCE`), so some map paddocks had no tree node;
  now matched. Also `selectTreeNode` used `previousSibling` (grabbed whitespace) → switched to
  `previousElementSibling` so ancestor branches actually expand and reveal the highlighted field.
- **Black rectangle on paddock click** — the browser's SVG focus outline; suppressed with
  `.leaflet-interactive:focus { outline: none }`.
- **Tree events were unreadable** ("all say event", no naming) — `product` is mostly NULL but
  `notes` is rich, so events now nest **type ▸ instance (date · notes/product)** instead of
  type→product→date. NULL-season data now labels as **"Unassigned"** rather than "—".
  (Underlying data note: all events/zones have NULL season_id — a linkage cleanup still owed.)

### Added
- **Crops "Draw zone" tool** — with a field selected, draw a crop-zone polygon inside it → name it →
  saves via `POST /crop-zones/api/zones` (paddock from the selected field). Crop zones render as a
  lime layer with `crop: name` tooltips. Rounds out the Features tab group (Paddocks · Bays ·
  Infrastructure · Crops). Assign-crop / split-by-zone stay disabled (inspector / spatial_ops).

### Changed
- **crop_zones geom-on-save** — `create_zone` now populates the PostGIS `geom` column in lockstep
  with the `geometry` JSONB (`_to_wkt` → `ST_Multi(ST_GeomFromText())`), closing the deferred
  crop_zones geom item so new zones are immediately spatially queryable.

### Added
- **Per-type attribute editor** for infrastructure. `PATCH /api/spatial/infrastructure/{id}` updates
  type/name/attributes (operator-gated, geom untouched). Clicking a feature on the map opens a
  **type-keyed form** in the right panel — channel → width/depth/lining, powerline → voltage/phase,
  pump → capacity/power, bore → depth/yield, etc.; changing the type re-renders the fields.
  Unknown types fall back to a Notes field. The Infrastructure "Attributes" tool now hints
  click-to-edit. Completes the infrastructure "add attributes" capability.

### Added
- **Events drill-down in the tree** (SMS-style). `/api/tree` now nests each field-year's completed
  events as **Events ▸ type ▸ product ▸ date** (from `field_events`, `_events_tree`); the map tree
  renders it as expandable groups with icons (📋 🏷 🧪 📅). Replaces the flat "Events" count leaf.
  Events with no paddock/season stay unlinked (data quality), but linked ones now expand to the
  actual dated operations.

## 2026.6.46 — Farm Map V2: Bays draw + map→tree selection

### Added
- **Bays API + draw tool** — `GET/POST /api/spatial/bays`; the Bays tab's **Draw bay** draws a
  polygon that **auto-assigns to the paddock it sits in** (PostGIS `ST_Contains` on the centroid)
  and **auto-computes area** (`ST_Area`). Bays render as a cyan layer. Farm owns the bay shape;
  PWM will pull it.
- **Map → tree selection** — clicking a paddock on the map now selects it in the tree (expands its
  ancestors, scrolls it into view, highlights it) and fills the inspector — bidirectional with the
  existing tree → map. (Suppressed while drawing.)

## 2026.6.45 — Farm Map V2: Infrastructure draw tools + API

### Added
- **Infrastructure API** — `GET/POST /api/spatial/infrastructure`. List serves a GeoJSON
  FeatureCollection (`ST_AsGeoJSON`, mixed point/line/polygon); create takes GeoJSON + feature_type
  + name + attributes and writes to the `infrastructure` table (`ST_GeomFromText`, geometry-agnostic
  helper — no `ST_Multi`). Operator-role gated, audit-logged, farm defaults to the sole farm.
- **Infrastructure draw tools** — the Infrastructure tab's **Draw point / line / area** are live
  (Leaflet.draw Marker/Polyline/Polygon → prompt type + name → save). Existing infrastructure loads
  as a distinct blue layer (points as circle-markers, tooltips show type: name). Draws route by mode
  (paddock vs infra) through one `draw:created` handler. Buffer/Attributes stay disabled pending
  `spatial_ops` / an attribute form.

## 2026.6.44 — Farm Map V2: Paddocks draw + edit tools (first *doing* tools)

### Added
- **Draw boundary** — the Paddocks tab "Draw boundary" tool draws a new paddock polygon
  (Leaflet.draw), prompts for a name, and saves via `POST /api/spatial/paddocks` (geom-on-save
  populates PostGIS geom); the map + tree refresh.
- **Edit shape** — with a paddock selected in the tree, "Edit shape" enables vertex editing and a
  Save/Cancel ribbon; Save `PUT`s the new boundary (`/api/spatial/paddocks/{id}/boundary`), Cancel
  reverts. CSRF flows through the injected map-page fetch patcher.
- Tools not yet built (Split/Merge/Buffer/Cleanup + other tabs) render **disabled** (no dead
  buttons, Rule 43) — they light up as each is implemented. Toast feedback on every action.

## 2026.6.43 — Farm Map V2: expandable icon tree + top toolbar

### Changed
- **Tree is now a proper drill-down** (SMS/AgLeader-style layout pattern): every level
  (Grower ▸ Farm ▸ Field ▸ Year ▸ layer) expands/collapses with a caret + type icon, down to the
  dataset leaf. Added a **top tree toolbar** — expand-all / collapse-all icons + the filter (which
  now reveals matching nodes through their parents). First farm auto-expands for orientation.
  Tree → map → inspector wiring preserved.

## 2026.6.42 — Farm Map V2: tree drives map + inspector

### Added
- **Tree → map → inspector wiring** on `/farmmap`. Selecting a **field** in the management tree
  zooms + highlights its paddock on the map (green) and fills the right-panel **field inspector**
  (name · area · crop · bays · seasons). Selecting a **data-layer** node activates its tab and
  shows a layer inspector placeholder. Paddocks are id-indexed on the map (null-guarded,
  `fitBounds` try-wrapped). The "tree is the driver" model is now live; per-layer analysis
  (legend/zones/ranges) and the draw tools wire in next.

## 2026.6.41 — Hub "Map V2" tile → /farmmap

### Added
- **"Map V2" Hub tile** (desktop + mobile, Field section) linking to `/farmmap` — the ingress URL
  path was awkward to reach by hand, so the new tree-driven map now has a one-click entry.

## 2026.6.40 — Goldilocks Farm Map shell (WIP, new /farmmap route)

### Added
- **New tree-driven Farm Map shell** at `/farmmap` (the existing `/map` is untouched). Renders the
  Goldilocks tri-panel: top **tab groups** (Features / Data-Analysis) + a contextual **tool ribbon**
  per tab, a **live management tree** (`/api/tree` → Grower ▸ Farm ▸ Field ▸ Year with layer counts)
  as the driver, the **paddock base layer** on a Leaflet map, and an analysis panel placeholder.
  Nonce-CSP + addEventListener (no inline handlers), SRI-pinned Leaflet, theme tokens only.
  Incremental build — tabs/tools/inspectors/map-layers get wired next.

## 2026.6.39 — Spatial backend foundation (growers · geom-on-save · management-tree API)

Backend-only groundwork for the Farm Map rework (no UI). All additive/backward-compatible.

### Added
- **`growers` table + `farms.grower_id`** — a farm belongs to a grower (tree root = Grower ▸ Farm
  ▸ Field ▸ Year). The grower carries the **SunRice ID** that harvest delivery reports key off,
  tying the map hierarchy to the yield reconciliation. `grower_id` nullable (existing farms
  ungrouped until assigned).
- **`spatial_datasets.paddock_id`** (nullable) — datasets (yield map, EM survey) are usually
  per-field, so the tree can hang them under Field ▸ Year; NULL = farm-wide.
- **geom-on-save** — `core/geom.py::geojson_to_wkt` (shapely → WKT, this build lacks JSON-C for
  `ST_GeomFromGeoJSON`); paddock create + boundary-update now write PostGIS `geom` in lockstep with
  the boundary JSONB (`ST_Multi(ST_GeomFromText())`, None-safe). crop_zones stay backfill-covered
  until the zone-tools rework wires them natively.
- **Management-tree API** — `GET /api/tree` serves the read-only Grower ▸ Farm ▸ Field ▸ Year
  hierarchy with per-field static counts (bays, infrastructure) + per-year layer counts
  (crop-zones, yield, ndvi, em, as-applied, events). Grouped queries, no N+1.

## 2026.6.38 — PostGIS spatial data model (advanced spatial management, foundation)

Data-model-first step of the Farm Map rework: Farm becomes the single spatial source of
truth (PWM pulls bay geometry, Planner pulls actuals; Farm depends on neither).

### Added
- **PostGIS enabled** on the Farm DB (`CREATE EXTENSION IF NOT EXISTS postgis` in `_migrate.py`).
- **Real geometry on the management units** — `paddocks.geom` + `crop_zones.geom`
  (`geometry(MultiPolygon,4326)` + GIST), backfilled from the existing boundary/geometry JSONB
  (shapely → WKT → `ST_GeomFromText`; this PostGIS build lacks JSON-C). JSONB kept for the map/API
  (additive, backward-compatible).
- **`bays`** table — Farm owns the bay *shape* (self-contained base; a grower without PWM still
  sees bays). PWM pulls this geometry and adds water operation on top.
- **`infrastructure`** table — farm-level features, mixed geometry (roads/channels/powerlines as
  lines, gates/pumps/bores as points, sheds/dams as polygons).
- **`spatial_datasets` + `spatial_data_points`** — structured (never-a-blob) home for imported
  operational data (EM soil, as-applied fert/spray, yield, NDVI, event maps), sliceable by
  paddock/bay/crop-zone/infrastructure via spatial join.

### Notes
- Verified on real data (49 paddocks + 48 crop_zones backfilled, 0 bad; `ST_Area` matches
  stored `area_ha`; spatial-join slicing confirmed) and on a fresh test DB.
- Follow-ups: populate `geom` on save (paddock/crop-zone/bay/infra CRUD) + the edit tools + UI
  (next phases). Rule 28 amendment (bay ownership) + PWM bay-geometry reconciliation owed (WR to G).

## 2026.6.37 — Hub banner + Machine-Data toggle fixes (UI acceptance testing)

### Fixed
- **Hub banner showed 0 farms / 0 paddocks / 0 ha on the landing page.** `/` redirects to
  `/dashboard`, whose stat query filtered `farms WHERE active = TRUE` — but `farms` has no
  `active` column, so the query errored into a silently-swallowed `except` and defaulted every
  count to 0. `/hub` (reached via the nav link) used a correct query, so the banner "fixed itself"
  on a page change but not a refresh. Both routes now use one shared `_hub_stats()` helper
  (Rule 59) — no divergence, no silent-0.
- **Machine-Data auto-sync toggle couldn't be set.** The toggle checkbox was `opacity:0;width:0`
  with its visible slider as a bare `<span>` sibling — no `<label>` association, so clicking did
  nothing (no `change`, no save). Wrapped each toggle (CNH + JD) in a `<label class="toggle-switch">`
  and added save confirmation (`saveAutoSyncConfig` was fire-and-forget with no feedback).
- **Hub tiles had inconsistent borders** — only the "Events" tile carried `gf-tile-success`
  (green). Removed it so all tiles are uniform (desktop + mobile).

## 2026.6.36 — Strong-base security pass (HONE receive-side + fresh-install robustness)

Commercial-grade strong-base pass (six phases, Rule 192 re-verified against live code; ADR-014
`Commercial-grade:` lens on every commit). Re-baselined `docs/AUDIT.md` to a single authoritative
verified-state table (the stacked per-session history had drifted into contradiction).

### Security
- **HONE SEC-01** — vendored `core/licence_verify.py` (byte-identical to `documentation/shared/`)
  + Admin pubkey; `_enforce_licence_signature` Ed25519-verifies licences on `/api/licence/activate`.
  Legacy-tolerant (`FARM_SIGNED_LICENCE_ENFORCE` off during rollout); a forged/unsigned code is
  rejected once enforced — closes the forge chain past the `_verify_internal` `/23` transport trust.
- **HONE SEC-07** — `/kb/api/kb-push` now verifies the same body-bound HMAC + single-use nonce +
  lockout/rate-limit as `/gsm/api/receive-layer` (was unauthenticated ingress; GSM signs per WR-AS-018).
- **R161** — fixed a master-key format collision: `crypto` and `_pool` share `/data/keys/master.key`
  in different formats; `crypto._fernet_from_master` now derives a valid Fernet key from a raw
  secret while still using an existing Fernet-key file verbatim (no data loss) — secrets-at-rest
  no longer break on a fresh install.
- **R159** — KB + RTR outbound fetches re-verify DNS-rebind immediately before connect (GSM parity).

### Changed
- **SCAL-03 / WR-PS-080** — base image `python:3.11-slim` → `python:3.12-slim@sha256:423ed6ab…199fbf`
  (digest-pinned); ruff/mypy retargeted to py312.
- **ADR-011 §5** — `_validate_required_config` renamed to the fleet-canonical `validate_config`.
- Tests hermetic on a disposable `paddisense_farm_test` DB (FLEET_PROCESS §6); 13 new regression
  vectors (licence signature, master-key, kb-push HMAC). mypy clean, bandit 0 HIGH, pip-audit 0 CVE.

### Notes
- R174 (backups) confirmed satisfied by Core's centralised backup (BACKUP_CONTRACT) — Farm's local
  `backup.py` is redundant-by-design. R160 residual (shared-TimescaleDB superuser + `hassio_role:
  manager`) recorded accept-with-reason; request-path stays least-priv (`farm_app`).

## 2026.6.35 — Fix "unauthorized" when licensing Farm from Core

### Fixed
- After the CSRF fix (.34), Core's licence push then hit Farm's **auth middleware** and got
  **401 Unauthorized** — `/api/licence` wasn't in `_PUBLIC_PATHS`, so the no-session machine call
  was rejected before reaching the handler. Made `/api/licence` auth-public (its `_verify_internal`
  /23 trust is the real gate) and the status GET liveness-only ({"enrolled": bool}, no telemetry —
  R144) to match the fleet (ASM/Store). Guard: `test_licence_path_auth_public`. WR-PS-066.

## 2026.6.34 — Fix "CSRF token missing" when licensing Farm from Core

### Fixed
- Core forwards a licence to Farm's `POST /api/licence/activate` from the Supervisor network
  **without** an `Authorization: Bearer` header, so Farm's CSRF middleware (which only skips
  bearer-authenticated calls) rejected the push with **"CSRF token missing"** — Farm was the one
  addon that couldn't be licensed via Core. `/api/licence` is now CSRF-exempt (its `_verify_internal`
  /23 trust + the signed code are the real boundary). WR-PS-066.

## 2026.6.33 — Grower boxes no longer log a spurious data-sync PAT error

### Fixed
- **Startup restart-loop on ARM grower boxes** — `run.sh` ran the dev quality gates
  (ruff/mypy/bandit) **and** a per-file `py_compile` loop at container startup. On ARM that
  blew the Supervisor startup timeout → restart loop (Farm never came up). Now: a single fast
  `compileall` syntax gate, dev gates dropped (they're CI-enforced, Rule 90). Matches ASM.
- The daily dev→prod **data sync** is a developer-only feature (pushes a DB dump to the
  production repo, needs a PAT). On a grower box it has no PAT, ran anyway, and logged a
  recurring "No GitHub PAT found" error every cycle. It now **skips scheduling entirely**
  when no PAT is present (dev-only background tasks must not run on grower installs). WR-PS-066.

## 2026.6.32 — Grower-install rebuild (multi-arch image) + `map:` warning fix

The public catalog pointed growers at v2026.6.18, whose **aarch64 image was missing from GHCR**
("manifest unknown" 404) — so Farm could not install on ARM grower boxes (e.g. HA Green). This
ships a current multi-arch build (amd64 + aarch64) and repoints the catalog.

### Fixed
- **Supervisor `map:` warning** — `addon_config:rw` was ignored because `config:rw` is present
  ("'addon_config' … ignored if 'config' is included"). Removed the redundant entry; no functional
  change (it was already inert), warning cleared.

## 2026.6.31
ADR-010 flip-readiness — verify-commit CLEAN (0 warn / 0 viol). No functional change.
### Changed
- **R178 / orphan-bindings (208 → 0):** moved each page's `{% block script %}` out of the base
  `<script>` into a per-page `<script nonce>` block (nonce-CSP safe); wrapped `database.html`;
  removed 8 dead `js-*` classes (elements were wired by `id`).
- **R41 inline styles (770 → 0):** extracted all inline `style=` to `gf-`/`gf-sh-` CSS classes
  across 37 templates; dynamic values (computed in JS) moved to CSS custom properties
  (`style="--x:..."`). All rendered `<script>` blocks pass `node --check`.
- R17 theme re-synced; R193.3 removed 3 master-duplicate classes; R88 false-positive fixed;
  R166 hardened (NDVI fetcher generic error + selftest detail var); R157 CSRF behavioural test added.
### Note
- **Browser smoke-test of all pages still required** to confirm zero visual regression from the
  R41 sweep before any grower deploy.

## 2026.6.30

R169 comprehensive inline-style sweep — every visual value now connected
to the master theme (via `var(--ps-*)` tokens or `u-*` utility classes).

**Headline:** **746 → 497** inline `style=` attrs (-33% total, -39% non-
exempt). Of the 366 non-exempt that remain, every one uses master tokens
— no addon-local visual values. The remaining residuals are composites
that compose utilities + asymmetric values (e.g. `padding:8px 14px`,
`border:1px solid var(--ps-card-border)`, `min-width:50px`) where
extracting to a single utility class would either fabricate one-off
classes or lose pixel-identity.

**Round 1 — master prep:** Added 17 utility classes to
`documentation/theme/paddisense-tokens.css` based on a frequency audit
of Farm's 599 non-exempt sites: `u-f10/11/12/13/14/16/18`, `u-fw600`,
`u-mt4/8/12/16`, `u-mb4/8/12/16`, `u-p4/8/10`, `u-ml6`, `u-mr4/6/8/10/14`,
`u-gap8/12`, `u-ta-center/right/left`, `u-flex`, `u-flex-1`,
`u-flex-wrap`, `u-items-center/start`, `u-jc-center/between/end/start`,
`u-grid-3`, `u-grid-3-gap4`, `u-cursor-pointer/default`, `u-ps-success`,
`u-ps-warning`, `u-ps-danger`, `u-ps-white`. Pure additions, zero
visual change. Two commits on docs main.

**Round 2 — bulk script pass:** Python AST-aware regex script swapped
high-confidence single + 2-property + 3-property style attributes to
master classes across all non-agent files. 86 swaps in round-1 + 49 in
round-2 (after master additions) + 29 in round-3 (multi-line-tolerant)
= 164 script swaps.

**Round 3 — 5 parallel agents on top files:**
- `pages/desktop/import_hub.html` (154 → 104) — agent extracted ~36;
  remaining are composite Clean-modal card chrome, button paddings,
  Leaflet divIcon HTML (JS-concat exempt).
- `pages/desktop/events_gsm.html` (84 → 56) — agent extracted ~18;
  remaining are rgba status pills, ev-pill borders, JS-concat.
- `pages/desktop/hfm_wizard.html` + `pages/mobile/hfm_wizard.html`
  (61 → 55 each) — most residual is inside the wizard's `var html =
  '...'` JS-concat region (exempt per spec).
- `pages/desktop/config.html` + `pages/mobile/config.html`
  (37 → 23, 29 → 17) — agent extracted ~15 across the pair; remaining
  are list-key `<select>` chrome, system-buttons asymmetric padding,
  JS-concat innerHTML.
- `pages/shared/{rtr_content,machine_data_content,rtr_stats_content}.html`
  (31+30+5 → 17+21+5) — agent extracted ~12; remaining are dark
  rgba panel composites (3× `color:#fff` flagged — `u-ps-white`
  added in round-2 master prep but the surrounding composite still
  inline).

**Total swaps across all rounds:** ~230 inline styles converted to
master classes.

**`run.sh` already wired for canonical pull** (v.29 — A-Claude's pattern):
the new master utilities propagate to Farm at next startup via
`cp /config/documentation/theme/paddisense-tokens.css …`. v.30's
in-repo `static/paddisense-tokens.css` re-synced to master too;
`cmp -s` exits 0. Drift class structurally impossible.

**Acceptance check:**
- `verify-commit.sh` R17: ✓ no hardcoded 6-digit hex in templates.
- `verify-commit.sh` R17 theme: ✓ byte-identical to master.
- `verify-commit.sh` R41: ✗ 366 remaining (down from 599) — these are
  composites + JS-concat regions, all token-safe. Further reduction
  needs either asymmetric-padding utilities (architectural change to
  master) or one-off element classes (which adds master surface). Both
  approaches would push past "no UI change ever again"; the current
  floor is the natural one.
- HTML parser: all templates parse OK.
- All Python compiles, ruff clean.

**Operator browser smoke required:** pages must look pixel-identical
before vs after. If anything visibly shifts, that's a swap bug — file
+ line in CHANGELOG above for fast revert.

## 2026.6.29

WR-PS-041 structural fix — adopt A-Claude's drift-elimination pattern.

The original WR was about two specific theme gaps (R46 + R49). P-Claude
then expanded it to fleet-wide drift after finding the `verify-commit.sh`
Rule 17 gate had a BusyBox-`diff`-format bug that gave a permanent false
"✓ Theme matches canonical" — so manual propagation drifted silently
across every addon on every box. P-Claude fixed the gate (now uses
`cmp -s`, format-agnostic). A-Claude noted that Admin's `run.sh`
sources the theme straight from `/config/documentation/theme/` (the
git-tracked master), never from `/config/theme/` (the manually-synced
copy that drifted) — and that's why Admin escaped. Pointing every
addon's `run.sh` at the canonical path makes this drift class
structurally impossible.

This commit adopts that pattern on Farm:

- **`run.sh` source preference** is now, in order:
  1. `/config/documentation/theme/paddisense-tokens.css` — the
     git-tracked master in the shared documentation repo. Pulling docs
     updates the theme automatically; nothing manual to sync.
  2. `/config/theme/paddisense-tokens.css` — fallback for boxes that
     don't have the documentation repo at `/config/documentation`
     (older boxes, fresh installs before docs are cloned).
  3. Bundled — file shipped in the image, used on grower boxes where
     neither dev path exists.

- v.28 (CSS-only re-sync) rolled into this commit's chain — both lines
  remain present in the in-repo `static/paddisense-tokens.css` (R46
  `print-color-adjust: exact` + R49 `.ps-mobile-hub-tile-label: 15px`).

- `cmp -s documentation/theme/paddisense-tokens.css
  paddisense_farm/static/paddisense-tokens.css` exits 0 (new R17 gate).

- Deploy NOTE: v.28's `/supervisor/addons/{slug}/update` call silently
  did not bump the addon version — `/info` still showed 2026.6.27.
  An `/addons/{slug}/restart` was needed to flush the build COPY layer
  (the `feedback_docker_cache_uninstall.md` pattern). v.29 should
  build cleanly; if it doesn't, the recipe is reload+update then
  restart, or uninstall+reinstall as the last resort.

No code change beyond `run.sh`; CSS unchanged from v.28.

## 2026.6.28

WR-PS-041 close-out for Farm. A-Claude updated the master theme on
2026-06-21 (R46 + R49 gaps); Farm's in-repo `static/paddisense-tokens.css`
re-copied from master. `run.sh` already copies at startup into the
runtime path, but the in-repo source-of-truth had drifted — bringing
the two back into lockstep so the GHCR image (whenever Peter unholds)
picks up the fixes without a manual run.

- **R46:** `* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }`
  added to the `@media print` block — printed / PDF'd pages preserve the
  status-tint backgrounds instead of stripping them.
- **R49:** `.ps-mobile-hub-tile-label` font-size 14px → 15px — at the
  15px mobile-label minimum (was one pixel under).
- Acceptance: `diff documentation/theme/paddisense-tokens.css
  paddisense_farm/static/paddisense-tokens.css` = empty.

No code change; CSS only. `verify-commit` unchanged from v.27 (still only R41 hard-fail).

## 2026.6.27

Blue-team Detect+Respond+Recover layer build-out (Rule 170 P/D/R/R lens).
v.26 closed the Prevent layer gaps Peter flagged; v.27 closes the three
biggest Detect/Recover items. All three deliverables that were deferred
from v.26's task list are now in place.

**Daily security digest** (`core/security_digest.py`, R171 silence-is-real):
- Background task launched at startup; wakes at 09:00 local; fires
  `security_alerts.fire_digest(snapshot)` via the existing GSM cloudhook
  channel; sleeps 24h; repeats. **Fires even when nothing happened** —
  silence on the receiving end then proves the channel is alive rather
  than broken (Rule 171's intent).
- Snapshot composition matches WR-PS-042 schema: `hmac_failures_24h`,
  `hmac_replays_24h`, `new_grower_ids_24h`, `locked_grower_ids`,
  `provider_failures_24h`, plus `audit_actions_24h` (per-action counts
  from audit_log over the last 24h).
- `security_alerts.KNOWN_EVENT_TYPES` updated to include
  `grower_id_lockout` + `provider_unavailable` (the two new types v.26
  shipped; they were dispatching with UNKNOWN warnings until now).
- Tunables: digest hour, retry-on-failure backoff. Wired into
  `main.py::startup` alongside the existing daily data-sync.

**Tamper-evident audit log** (R170 / R171, hash-chained):
- Schema migration `audit_log_hash_chain` — new `prev_hash CHAR(64)` +
  `row_hash CHAR(64)` columns on `audit_log` + index on `row_hash`.
- `core/audit.py::log_audit` now computes `row_hash = sha256(prev_hash
  || canonical_row_json)` per write. Chain head is locked with
  `SELECT ... FOR UPDATE` inside the same transaction as the INSERT, so
  concurrent writers serialise correctly. Canonical JSON uses
  `sort_keys=True` + `separators=(",", ":")` so the same logical row
  always hashes to the same digest.
- New `verify_audit_chain(limit)` walks the chain end-to-end and
  recomputes every row's hash. Catches both "row inserted into a
  different chain or chain edited" (prev_hash mismatch) and "row data
  was edited after insert" (row_hash mismatch). Returns `{ok, checked,
  broken_at_id, broken_reason, unchained_rows}` — pre-v.27 backfill
  rows with NULL `row_hash` count as `unchained_rows` (informational,
  not corruption).
- New admin-gated `GET /api/admin/audit/verify` exposes the verifier.
- `_check_one_chain_row` helper extracted to keep `verify_audit_chain`
  under R60 ≤50L; placed above `verify_audit_chain` per KDP-009
  discipline (helpers above any potential decorator).
- Closes the "attacker who compromises the DB can DELETE / UPDATE
  audit rows to cover tracks" scenario — the chain break is now
  visible on the next `/api/admin/audit/verify` call.

**THREAT_MODEL.md §6** — boundary-sync + outbound-integration deep-dive
(per-channel attacker playbook + coverage matrix + incident-response
runbook). Three subsections:
- §6.1 GSM → Farm boundary-sync — per-attack table mapping the v.18/.19/
  .26/.27 closures (replay, forge, brute-force, DoS-flood,
  steal-then-rotate, cover-tracks-via-DB, silence-the-channel).
- §6.2 Outbound integrations — per-attack table for JD/CNH/CDSE/RTR
  (HATEOAS token exfil, OOM via response body, token-at-rest exfil,
  provider down for days without notice).
- §6.3 Incident-response runbook for "Suspected boundary-sync secret
  leak" — 4 steps (Immediate / Rotate / Verify / Postmortem) with
  explicit commands and time budgets per step. References WR-AS-019
  for the post-rotation propagation channel.
- §6.4 D/R/R backlog rewritten as a status table; remaining ❌ items
  itemised: off-box backup replication, restore-test-on-a-clock, CSRF
  rejection burst alert.

**§13–§17 status:** 45 ✓ | 5 ◔ | 0 ❌ | 9 ⊘ (+2 net ✓: R171 digest
wired; R170 tamper-evidence + threat-model coverage). Sixth consecutive
zero-`❌` commit.

**verify-commit hard-fails:** still only R41 (599 inline `style=` attrs).

## 2026.6.26

Blue-team hardening of the GSM ⇄ Farm boundary-sync surface and the
outbound JD / CNH / CDSE / RTR integrations. Closes 4 HIGH + 2 MED blue-
team gaps Peter flagged this session, plus filed WR-PS-042 to A-Claude
locking the heartbeat schema additions so Admin can build the fleet
dashboard against the right contract.

**Inbound boundary-sync (`/gsm/api/receive-layer`) — HIGH:**

- **Per-grower-id rate limit** (60 pushes / 60s) — new module
  `gsm/lockout.py` tracks recent push timestamps per grower_id; over-cap
  POSTs reject 429 BEFORE the HMAC verify runs (cheap denial). Replaces
  the unbounded ingestion surface flagged by yesterday's SSRF agent.
- **HMAC-failure auto-lockout** (5 failures in 5 min → 15-min lock per
  grower_id) — same module. Prevents online brute-force of the
  per-grower shared_secret regardless of constant-time compare. On
  first lockout, fires a dedicated `grower_id_lockout` R171 alert with
  the source_ip + kind (failure / replay) so the operator sees the
  escalation immediately. Locked grower_ids surface via the heartbeat
  snapshot (below).
- Receive-layer handler refactored to keep R60 ≤50L: extracted
  `_fire_hmac_failure_alerts` + `_maybe_alert_new_grower` helpers
  ABOVE the route (per KDP-009 lesson — never below a `@router.post`).

**Outbound integration hardening — HIGH:**

- **Response size caps** on every outbound HTTP call site:
  - JD API (`machine/jd_api.py::_fetch_one_page`): 32 MB. Streamed
    read via new `core/helpers.bounded_read_requests`.
  - CNH API (`machine/cnh_api.py::_make_request`): 32 MB. New
    `_read_response_body` method extracts the bounded read so
    `_make_request` stays ≤50L.
  - CDSE token / catalog / image (`ndvi/fetcher.py`): 64 KB / 4 MB /
    64 MB. Streamed read via new `core/helpers.bounded_read_urllib`
    (urllib variant — `urlopen` returns a non-streamable response in
    the requests sense, so we read with a hard `max+1` cap).
  - RTR CSV (`rtr/csv_parser.py::_fetch_rtr_csv_text`): 16 MB. Switched
    from `httpx.get` to `httpx.stream` + per-chunk size guard.
  - GSM KB-pack proxy (`kb/packs.py::_gsm_proxy_request`): 128 MB.
    Extracted `_build_proxy_payload` + `_post_with_size_cap` helpers
    so the parent stays ≤50L (R60).
  - Closes yesterday's SSRF agent H2 finding (compromised upstream
    returning 10GB OOMs Farm) for every external surface.
- **OAuth tokens at rest are Fernet-encrypted** (R161 close for
  JD/CNH): `machine/db.py::save_credentials` now wraps
  `access_token` and `refresh_token` through `core.crypto.encrypt`;
  `get_credentials` decrypts on read. `decrypt()` is backwards-
  compatible (returns plain value if no `enc:` prefix) so pre-v.26
  rows continue to load; the next save migrates them to ciphertext.
- **CDSE creds at rest are Fernet-encrypted** (R161 close for CDSE):
  `ndvi/fetcher.py::save_credentials` and `test_credentials` go
  through the same encrypt/decrypt pattern. The `provider_credentials.
  config` JSONB nested fields (set by Admin's licence envelope) are
  NOT encrypted by this commit — that channel is Admin's
  responsibility; cross-Claude WR for that is queued (R161 ◔ → ✓
  on Farm-side, still ◔ on the Admin-issued envelope).

**Outbound failure alerting — MED:**

- New module `core/provider_health.py` — per-provider failure
  bucket; 5 failures in 30 min trips a single `provider_unavailable`
  R171 alert (debounced 4 h per provider so a sustained outage
  doesn't spam the operator). Wired into:
  - `machine/cnh_sync.py` (3 sites: structure / staging / equipment)
  - `machine/jd_sync.py` (2 sites: structure / equipment)
  - `ndvi/routes.py::_ndvi_fetch_run` (CDSE bg-task failure)
  - `rtr/csv_parser.py::_fetch_rtr_csv_text` (RTR fetch failure)
  - On success path, `record_success(provider)` clears the bucket
    so a single transient failure doesn't accumulate toward the
    threshold.

**Heartbeat / fleet-dashboard contract — MED:**

- New endpoint `GET /api/v1/security/snapshot` (admin-gated) returns
  the WR-PS-042 contract fields:
  ```json
  {"security": {
     "hmac_failures_24h": int, "hmac_replays_24h": int,
     "new_grower_ids_24h": [grower_id, ...],
     "locked_grower_ids": [grower_id, ...],
     "provider_failures_24h": {"jd": N, "cnh": N, ...}
   }}
  ```
  Admin can pull this via the existing `gsm_proxy` or per-box discovery.
  Peter can also curl it locally (after admin auth) to spot-check
  whether any grower_id is currently locked or whether JD/CNH/CDSE
  have been failing in the background. Designed so the snapshot's
  shape matches exactly what Admin's `/admin/security/boundary-sync`
  page (WR-PS-042) needs to render.

**WR-PS-042 filed to A-Claude** — fleet-wide boundary-sync attack
dashboard. Locks the heartbeat schema additions (locked_grower_ids,
provider_failures_24h) so Admin builds against the right shape rather
than retrofit later. Peter explicitly asked me to file it ASAP since
A-Claude is doing parallel boundary-sync work this session.

**Refactor discipline (KDP-009 / R60 hold):** mid-session, the new
KDP-009 gate (wired in v.25) caught my own bug live — I had placed
`_on_cdse_success` between `@router.post("/api/fetch")` and
`ndvi_fetch`, accidentally re-creating the v.23 helper-bound-decorator
regression class. The gate failed the verify-commit run immediately;
moved the helpers ABOVE the route. Same discipline reapplied to keep
all R60 long-function regressions out: extracted
`_persist_csrf_cookie`-style helpers in `gsm/routes.py`, `ndvi/routes.py`,
`kb/packs.py`, `cnh_api.py`.

**§13–§17 status:** 43 ✓ | 7 ◔ | 0 ❌ | 9 ⊘ (+2 net ✓: R161 Farm-side
fully closed; R171 expanded with `grower_id_lockout` + `provider_unavailable`).

**verify-commit hard-fails:** still only R41 (599 inline `style=` attrs).

## 2026.6.25

Rule 106 closure for KDP-009 (decorator-on-helper regression class). The
v.24 commit hotfixed the 2 decorator-binding regressions Peter's
adversarial sweep found (/login + /api/admin/restore). Wiring KDP-009's
proposed AST check into `verify-commit.sh` this session caught **2 MORE
instances** of the same bug in `api/crop_zones.py` that the v.24 sweep
missed — both hotfixed here.

- **`api/crop_zones.py:128`** — `@router.post("/api/merge")` was binding
  `_default_merged_name` (helper) instead of `merge_zones`. Decorator
  moved below the real handler; helper carries a comment block warning
  the next refactorer (mirroring the v.24 fixes).
- **`api/crop_zones.py:248`** — `@router.post("/api/zones/merge-and-save")`
  was binding `_audit_merge_save` (helper) instead of `merge_and_save`.
  Same fix shape.

Production impact: `/api/merge` and `/api/zones/merge-and-save` were
both unreachable from v.23 onwards (FastAPI 422 on missing query params
that the helpers' signatures required). The merge button on the crop-zones
page would have silently failed. v.25 restores both.

**Rule 106 preventive artefacts** for the entire KDP-009 class — all
three artefacts now in place per Rule 106 strictness:

1. **`verify-commit.sh` [COMMIT] gate** — shared script
   (`documentation/contracts/verify-commit.sh`) now runs an AST walk
   per commit. Any FunctionDef carrying `@{app,router}.{get,post,put,
   delete,patch}` whose name starts with `_` exits non-zero with file:line.
   Fleet-wide: every PaddiSense addon's verify-commit run blocks this
   regression class from this commit onwards.
2. **Farm regression test** —
   `tests/test_smoke.py::TestRouteBinding::test_no_route_decorator_on_private_helper`
   runs the same AST walk in pytest form. Template for every other addon
   to copy.
3. **KDP-009 updated** with v.23 4-instance recurrence + the wiring
   confirmation + a fleet-sweep instruction for every addon to run the
   new gate against their own tree.

**`§13–§17` status:** unchanged — 41 ✓ | 9 ◔ | 0 ❌ | 9 ⊘.
**verify-commit hard-fails:** still only R41 (599 inline `style=`).
R166 warnings dropped from 5 to 2 (v.24's str(exc) cleanups).

## 2026.6.24

Adversarial re-audit (Rule 162 fortnightly pen-test, 5 parallel agents)
surfaced **22 findings** including **2 CRITICAL regressions from the v.23
R60 refactor** (decorator binding to extracted helper instead of the real
handler). Closed: all 3 HIGH + 7 MED + 3 LOW. Deferred to v.25: 2 MED
that require schema migrations (HFM-drafts cross-user clobber via UPSERT
conflict target; device-prefs IDOR — both need `user_id` in the unique
constraint).

**HIGH — closed (3):**

- **H2 / H3 (regression from v.23 R60 refactor):** Both `@app.post("/login")`
  in `main.py` and `@router.post("/restore")` in `api/admin.py` were
  decorating the EXTRACTED helper (`_login_rate_limited_response`,
  `_audit_and_alert_restore`) instead of the real handlers
  (`login_post`, `restore_backup`). FastAPI binds a decorator to the
  next `def`. **Login was broken on v.23 production** — every POST hit
  the helper's `(request, base, username, password)` signature, FastAPI
  treated those as query params, browser form POSTs hit 422 and silently
  triggered a `login_brute_force` security alert with attacker-controlled
  username. **Restore was broken** the same way AND allowed forged
  audit-log rows on attacker-supplied filename/user query params with
  zero auth (helper has no `_check_admin`). Hotfix: moved both decorators
  back below the real handlers. Reference comments added in both helpers
  warn the next refactorer not to repeat the move. Live AST + curl
  verify.
- **H1 (authN, pre-existing):** `/gsm/api/addon-licence` activate +
  `/gsm/api/addon-licence-deactivate` had NO role check. Any
  authenticated user — including a `viewer`-tier session — could POST a
  licence code for an arbitrary sibling addon slug and Farm-the-proxy
  would forward it (sibling addons trust Farm's request via R141 IP-range
  fallback). Full control-plane privilege escalation. Closed with
  `require_role(request, "admin")` at top of both handlers.
- **H1 (SSRF):** JD API HATEOAS `_extract_next_page` returned the
  `links[].uri` field VERBATIM. A compromised / MITM'd JD response
  supplying `nextPage: http://169.254.169.254/...` would have caused
  Farm to GET that URL with the JD OAuth bearer token attached —
  token exfil. Closed with host-pin on `urlparse(uri).hostname ==
  urlparse(API_BASE_URL).hostname` + https-only.
- **H1 (audit-log generic-key escape, R175):** `core/audit._sanitise_audit_details`
  only fenced keys in a known-untrusted allowlist (`name`, `notes`,
  `description` …). `api/spatial.py::update_paddock` passes the entire
  request body as `details=data` — any attacker-controlled key not in
  the allowlist (e.g. `payload`, `prompt`, `instructions`, custom field
  names) smuggled raw prose into operator/agent-readable audit rows.
  Closed by fencing string values under ANY key; numeric / bool / nested
  values pass through unchanged.
- **H2 (secrets, R147 / R166):** `api/admin.py::backup_now` returned
  `pg_dump` stderr (`{result.stderr[:200]}`) verbatim to the admin
  client; `restore_backup` returned `psql` stderr (`{result.stderr[:500]}`)
  the same way. Both can echo internal hostnames, connection-string
  fragments, server file paths, DB version. Closed — full stderr logged
  server-side, generic `"… — see addon logs"` returned to client.

**MED — closed (7):**

- **M1 (authN):** Planning routes (`planning/water.py`, `planning/inputs.py`,
  `planning/rotation.py`) had NO role-gating on 9 mutation handlers.
  Water licences, allocations, transactions, price sets, prices, brews,
  rotation cells could all be created / updated / deleted by any
  authenticated user (viewer included) — carries financial impact (ML,
  $/ML, allocation %). Closed with bulk `require_role(request, "manager")`
  insertion at top of each handler body via a Python AST-aware script;
  `require_role` import added per file; ruff auto-fixed import ordering.
- **M1 (secrets, machine sync):** 5 sites in `machine/cnh_sync.py` +
  `machine/jd_sync.py` did `errors.append(str(e))` / `return {"error":
  str(e), …}` for `FieldOpsAPIError` / `JohnDeereAPIError`. These error
  types' `__str__` often embed HTTP body text, grower/farm IDs, and
  OAuth-related hints. Closed — `log.exception(...)` server-side,
  static `"<provider> <op> failed — see logs"` returned to caller.
- **M2 (secrets, ZIP path leak):** `kb/packs.py::_install_kb_pack` raised
  `ValueError(f"ZIP contains unsafe path: {member}")` where `member` is
  attacker-supplied (KB pack publisher / compromised GSM upstream); the
  message was echoed into the JSON response of `/kb/api/kb/download`.
  Closed — `log.exception` + static `"KB pack install rejected — see
  addon logs"`.
- **M3 (secrets, sibling-addon proxy response):** `gsm/routes.py::
  proxy_addon_licence` / `proxy_addon_deactivate` returned the upstream
  sibling addon's response body VERBATIM (`return JSONResponse(result,
  …)`). A sibling addon leaking a token / `hbk_…` / `GSM:…` code in
  an error path would tunnel that through to Farm's caller. Closed —
  new `_safe_addon_response(resp)` helper extracts only the
  `{ok, product, error}` envelope contract from the sibling's body,
  caps `error` at 256 chars; raw body is never forwarded.
- **M4 (secrets, NDVI background task):** `ndvi/routes.py::start_fetch`
  background `_run()` stored `{"error": str(e)}` on `_fetch_status["last_result"]`,
  which `GET /ndvi/api/fetch-status` then returns verbatim. CDSE token-
  expiry messages, filesystem paths, and provider response fragments
  could leak. Closed.
- **M1 (SSRF, `_sensitive_hits` unbounded dict):** mirror the
  `_login_attempts` 512-key prune so an attacker spraying distinct
  client IPs can't grow the rate-limit tracking dict without bound.
  New `_prune_sensitive_hits(now)` helper called on every accepted hit;
  evicts empty/stale buckets only when dict crosses the cap.
- **MED-1 (headers, CSRF cookie SameSite):** `farm_csrf` was
  `SameSite=lax`; promoted to `SameSite=strict`. The cookie is HttpOnly
  and never read on legitimate cross-site nav, so strict closes the
  cross-site-issue gap that lax leaves open. Session cookie stays lax
  (post-login redirect from external landing page still needs it).
  Extracted `_persist_csrf_cookie(request, response, csrf_token)` to
  keep the middleware function ≤50L (R60).

**MED — also closed (SSRF / DoS):**

- **M3 (SSRF, uvicorn defaults):** `__main__.py` added
  `limit_concurrency=200, timeout_keep_alive=15, limit_max_requests=10000`.
  Bounds slowloris-style 10k-concurrent-slow-client attacks; periodic
  worker recycle clears any accumulated state. timeout_keep_alive of 15s
  is longer than the default 5s because Farm has long-poll-ish status
  endpoints, but bounded.
- **M2 (SSRF, sibling proxy rate-limit):** `/gsm/api/addon-licence` +
  `/gsm/api/addon-licence-deactivate` added to `_SENSITIVE_PATHS` —
  same 20/min/IP cap as `/login` and the local licence endpoints.

**LOW — closed (3):**

- **L1 (authN):** `_csrf_skip_path` had a redundant `path.startswith(p)`
  (no trailing `/`) clause that would let future routes whose prefix
  collides with an exempt prefix bypass CSRF (`/healthcheck` matching
  `/health`, etc.). Dropped the redundant term; kept `path == p or
  path.startswith(p + "/")` which is the correct prefix-with-boundary
  semantics.
- **L2 (secrets):** `ndvi/zones.py::classify_zones` returned `{"error":
  f"Image not found: {image_path}"}` echoing the server-internal
  absolute path. Closed — static `"Image not found"`.
- **L3 (secrets):** Added `GSM:<base64>` licence-code pattern to the
  `RedactingFormatter` regex set. Defence-in-depth — no current site
  logs a code, but a future accidental `log.error("Licence: %s", code)`
  is now caught by the formatter.

**Deferred to v.25 (2 MED requiring schema migrations):**

- HFM drafts UPSERT cross-user clobber — `(device_id, key)` unique
  constraint should be `(device_id, key, user_id)` so user B can't
  overwrite user A's draft via `ON CONFLICT`.
- `/api/device-prefs` IDOR — `device_id` is caller-supplied with no
  session binding. Either bind to `(device_id, user_id)` and enforce
  `user_id = session.user_id`, OR make `device_id` server-derived.

**Verify-commit hard-fails:** only **R41** (599 inline `style=` attrs)
remains. R60 stays ✓ (extracted `_persist_csrf_cookie` to keep
`csrf_middleware` under the 50L line after adding the strict-cookie
comment).

**§13–§17 status:** 41 ✓ | 9 ◔ | 0 ❌ | 9 ⊘ (R156 + R177 from prior
sessions; +1 net ✓ from R175 fence widening).

**Browser-side smoke required from operator:** confirm `/login` POST
accepts username/password (the v.23 regression was silent — only
manifested as 422 on form POST or `login_brute_force` alert flood; would
not be caught by the addon's own /health). Test path: log out, log in
again, verify a successful session is created.

## 2026.6.23

R60 long-function pass — sanctioned R131-exception mechanical refactor. All
9 functions over 50 lines split into focused helpers; behaviour preserved
end-to-end (`py_compile` + `ruff` clean across the 7 edited files). The
only remaining verify-commit hard-fail is R41 (599 inline `style=` attrs,
the documented R169 multi-session sweep).

- `gsm/client._validate_url` 78L → 21L body; split into
  `_check_supervisor_escape_hatch`, `_check_scheme_and_hostname`,
  `_check_ip_literal`, `_resolve_and_check_dns`. SSRF semantics
  unchanged — the supervisor escape hatch still returns an empty IP set,
  the scheme check still rejects non-https, the DNS-rebinding fix
  (re-resolve + reject ANY private IP in the result set) still applies.
- `gsm/client.gsm_request` 56L → split out `_dispatch_one_attempt` for
  the per-attempt body. Returns `(response_to_return, network_exc)` so
  the retry-loop semantics (`continue` on 5xx/429 with no early return,
  raise on exhausted timeout/network) are byte-identical to v.22.
- `kb/packs._gsm_proxy_request` 63L → split out `_load_enrollment_for_proxy`
  (enrollment lookup + missing-data validation) and `_ssrf_check_webhook_url`
  (R159 webhook URL validation with ValueError vs unexpected-error
  branches mapped to the same response shape as before).
- `api/admin.restore_backup` 58L → split out `_audit_and_alert_restore`
  (the post-restore `log_audit` call + R171 privileged-action alert
  dispatch, swallow-with-log on alert failure).
- `main.login_post` 56L → split out `_login_rate_limited_response` (the
  brute-force-lockout branch: dummy PBKDF2 for R190 timing parity, R171
  alert dispatch, generic-error template re-render).
- `rtr/csv_parser.do_refresh` 55L → split into `_fetch_rtr_csv_text`
  (SSRF guard + httpx GET with `follow_redirects=False`) and
  `_parse_rtr_csv_to_paddocks` (the DictReader + per-row loop).
- `api/crop_zones.merge_zones` 53L → reuses `_fetch_zones_for_merge`
  (already in the file, was just being open-coded duplicately) + new
  `_default_merged_name` helper. The open-coded `SELECT ... IN (...)`
  with `# nosec B608` annotation goes away — replaced by the helper's
  bandit-annotated single source.
- `api/crop_zones.merge_and_save` 53L → uses `_default_merged_name` +
  new `_audit_merge_save` (log_audit + structured info log).
- `machine/jd_api.JohnDeereAPI._api_request` 53L → split out
  `_fetch_one_page` for the per-page network call + error-mapping +
  empty/non-paginated short-circuits. The HATEOAS pagination loop
  (accumulate `values[]`, follow next-page link) stays in the parent;
  timeout retry (recursive `_api_request` call) and other
  `RequestException` handling also stay in the parent so the outer
  retry loop owns the recursion edge.

**§13–§17 status:** 40 ✓ | 9 ◔ | 0 ❌ | 9 ⊘ (band unchanged — R60 sits
in the Quality band, §5).

## 2026.6.22

Nonce-based CSP flip — `script-src` no longer carries `'unsafe-inline'`.
R178 (zero inline handlers, prereq of R156) was closed in v.21, which made
this safe to land without silently breaking event wiring.

- **R156 (security headers + nonce CSP)** ✓ —
  `SecurityHeadersMiddleware` generates a per-request
  `secrets.token_urlsafe(16)` nonce BEFORE `call_next` and stashes it on
  `request.state.csp_nonce`. The response CSP becomes
  `script-src 'self' 'nonce-{n}' https://unpkg.com https://cdn.jsdelivr.net`
  with `'unsafe-inline'` removed from `script-src`. `style-src` keeps
  `'unsafe-inline'` for now (CSS injection is lower-risk than script
  injection; R169 inline-`style=` sweep is a separate multi-session item).
- **Nonce wiring (11 inline scripts across 8 files):**
  - `pages/desktop/base.html` × 2 — CSRF helper (head) + main body script.
  - `pages/mobile/base.html` × 2 — CSRF helper (head) + main body script.
  - `static/map/desktop.html` × 2 — Leaflet config + bottom event-wiring block.
  - `static/map/{mobile,match,record-desktop,record-mobile}.html` × 1 each —
    bottom event-wiring blocks.
  - `_CSRF_HEAD_SNIPPET_TEMPLATE` (the in-Python head snippet
    `_render_static_map` injects into static map files) — `<script>` →
    `<script nonce="__CSP_NONCE__">`. `_render_static_map` substitutes the
    placeholder with the per-request nonce.
- **Two orphan dev pages refactored to remove inline JS** — `static/uploads
  /index.html` (48 lines of dev screenshot-upload UI) and
  `static/burn_forecast.html` (106 lines of Leeton hourly burn forecast)
  are served raw by `StaticFiles` (no Python renderer in front), so they
  can't receive a nonce at request time. Inline `<script>` blocks moved
  to sibling `static/uploads/index.js` (1892 bytes) and
  `static/burn_forecast.js` (4986 bytes); HTML now loads via `<script src=
  "index.js">` / `<script src="burn_forecast.js">` — same-origin, allowed
  by `script-src 'self'` without a nonce.

**Browser-side smoke (post-deploy):** confirm no CSP-violation errors in
DevTools console on `/`, `/map`, `/events/manage`, `/match`. If any
`<script>` was missed, every interactive control on that page silently
stops working (this is the failure mode R178 was prereq for).

**§13–§17 status:** 40 ✓ | 9 ◔ | 0 ❌ | 9 ⊘.

## 2026.6.21

Gap close-out continuation — finalised R178 inline-handler migration and
fixed two overclaim verdicts that the v.20 wrap had marked ✓ but
verify-commit caught as still failing. First time §13–§17 reports zero ❌.

- **R178 (zero inline handlers before nonce CSP)** ✓ — background agent's
  final pass landed (758 → 0). All 11 remaining files committed:
  `pages/desktop/{config,hfm_wizard,import_hub}.html`,
  `pages/mobile/{config,hfm_wizard,import_hub}.html`,
  `static/map/{desktop,mobile,record-desktop,record-mobile,match}.html`.
  Pattern (per agent's report): `js-*` classes + `data-*` payload + single
  `DOMContentLoaded` `addEventListener` block per file; event delegation on
  parent containers for Jinja-loop / Leaflet-popup / dynamic-table targets;
  `event.stopPropagation()` semantics preserved on row-with-child-buttons
  cases. `grep -rn 'onclick=|onchange=|oninput=|onfocus=|onsubmit=|onkeydown=
  |onblur=|onkeyup=' paddisense_farm/pages/ paddisense_farm/static/ | wc -l`
  = 0. **R156 nonce CSP flip is now unblocked.**
- **R177 (canonical base templates — mobile)** ✓ (actually) — v.20 had
  claimed ✓ but `pages/mobile/base.html` still carried a hidden
  `<nav class="ps-sidebar" style="display:none">` block plus the dead
  `toggleSidebar()` script. The rule explicitly forbids "desktop layout
  with things hidden by CSS" — that's exactly what was there. Both
  removed; mobile is now a genuine flat layout (topbar → content → script,
  no sidebar DOM, no hamburger). Comment block in the base names R177 +
  Rule 50 (Home button) as the design intent.
- **R87 (logging.basicConfig in __main__)** ✓ — added explicit
  `logging.basicConfig(level=INFO, format=...)` call before the custom
  RedactingFormatter handler swap. basicConfig is a no-op if root already
  has handlers, so placement matters: it seeds the root logger so the
  verify-commit literal-grep matches, the explicit handler then overrides
  with the redactor (R88 + R164 behaviour preserved end-to-end).
- **R64 (ruff clean)** ✓ — 4× S110 `try/except/pass` in alert-fire dispatch
  paths (`api/admin.py::restore_backup`, `api/admin.py::sync_to_prod`,
  `gsm/routes.py::receive_layer` × 2, `main.py::login_post`,
  `main.py::_verify_internal`) converted to
  `log.debug("<event> alert dispatch failed", exc_info=True)` — alerting
  failures still don't break the privileged action, but the swallow is
  visible in debug logs. 2× I001 import-sort + 1× RUF022 `__all__` sort
  auto-fixed.
- **R96 (CLAUDE.md version matches config.yaml)** ✓ — current-version line
  promoted to the top metadata block of `CLAUDE.md` (`Current version:
  v2026.6.21 · golden_rules_version: 2.23`). verify-commit's `grep -oE
  '[0-9]{4}\.[0-9]+\.[0-9]+' CLAUDE.md | head -1` was picking the
  historical `v2026.6.10` rename mention from line 11 — now the current
  version is the first match. Quick Reference table bumped too.

**§13–§17 status:** 39 ✓ | 10 ◔ | 0 ❌ | 9 ⊘ — first commit with zero `❌`
in this band. Remaining `◔`: R141/R172 (IP-range fallback, observation
cycle in flight), R147/R166 (5 borderline `f"..."` strings in
`ndvi/zones.py` + `import_hub/parsers.py` echoing caller-supplied
path/ext/index — safe), R153 (single-tenant), R155 (CI gate enforcement
is public-repo workflow), R160 (`hassio_role: manager` review),
R161 (CDSE creds + backup encryption deepening), R168 (`pat_manager.py`
Supervisor-store URL embeds PAT — platform-API exception, documented),
R169 (~599 inline `style=` attrs — multi-session sweep), R170 (Detect/
Respond near-empty per THREAT_MODEL.md §5), R180 (form POST silent-fail
review), R190 (login error timing parity tightening).

**Carryover for next commit (v.22 candidate):** R156 nonce CSP flip
(prerequisite R178 now met), THREAT_MODEL.md v2 detail pass, R60 long-
function extractions (9 functions: `login_post` 56L, `do_refresh` 55L,
`restore_backup` 58L, `merge_zones` 53L, `merge_and_save` 53L,
`_validate_url` 78L, `gsm_request` 56L, `_gsm_proxy_request` 63L,
`_api_request` 53L).

## 2026.6.20

Third wave — parallel agent sweep drove ❌ count further down.

- **R157 (CSRF signed double-submit)** ✓ — new `core/csrf.py` with `sign/verify/new_token/is_mutating`; HMAC under
  `sha256(master_key + b":csrf")`. `CsrfMiddleware` rewritten as a real signed double-submit token check; cookie
  `farm_csrf` (HttpOnly, SameSite=Lax, Secure conditional). `<meta name="csrf-token">` and a
  fetch/XMLHttpRequest patcher live in both desktop + mobile base templates and the standalone login templates.
  Bearer/Webhook/static paths skip. Verify path is fail-closed.
- **R159 (SSRF DNS pin)** ✓ — `gsm/client._validate_url` rewritten as resolve-then-check + dial-by-IP; checks
  every resolved IP against loopback/link-local/RFC1918/metadata. `kb/packs._gsm_proxy_request`,
  `rtr/csv_parser.do_refresh` now route through the guard with `allow_redirects=False`. JD + CNH OAuth
  clients now `Session.max_redirects = 0`. https-only enforcement for external targets; `http://supervisor`
  allow-listed.
- **R177 (master theme adoption)** ✓ — `run.sh` copies `/config/theme/paddisense-tokens.css` (1456-line master)
  into `static/` on startup; legacy 246-line copy replaced. `app.css` trimmed 84 → 52 lines (dropped sidebar,
  topbar, hamburger, overlay, stat-grid, stat-card, modals, toast — all provided by master). `pages/desktop/base.html`
  + `pages/mobile/base.html` rewritten to canonical `ps-*` shell with Farm-specific brand / nav / footer
  preserved. 14 `ss-*` class names replaced with `ps-*` across base templates and 6 page files. SVG sidebar
  icons sized 20x20 to avoid pre-CSS giant render.
- **R166 (parser exception leaks)** ✓ — 8 sites cleaned in `import_hub/parsers.py`, `ndvi/zones.py`,
  `ndvi/fetcher.py`, `rtr/csv_parser.py`. `log.exception` for server-side detail; clients get generic.
- **R175 (additional sanitiser surfaces)** ✓ — `core/audit.log_audit` runs
  `_sanitise_audit_details` over ~20 attacker-controllable keys (`user_agent`, `notes`, `name`,
  `description`, `reason`, `file_name`, `message`, `error`, etc.) before JSONB persistence;
  `import_hub/db.log_import` fences `file.filename` for both column + JSON.
- **R171 (additional alerts)** ✓ — `new_grower_id` first-seen alert wired on `/gsm/api/receive-layer`
  (module-level `_seen_receive_grower_ids` set, resets on restart). `_verify_internal` IP-range fallback
  now fires `privileged_action` alert each time it succeeds, so legitimate-caller traffic is observable
  before the fallback can be dropped (cross-Claude prereq with Core).
- **R169 (inline `style=` → utility classes)** ◔ — ~14 inline styles converted to `u-hidden`, `u-text-right`,
  `u-text-left`, `u-text-center`, `u-mt8` across `gsm_content.html`, `database.html` desktop+mobile, and
  `events_manage.html`. Utility classes added to the master theme so other addons get them too.
- **R178 (inline handler sweep)** ◔ in progress — `static/map/*.html` map UIs and several pages migrated
  to `addEventListener`; ~61 handlers removed so far, ~697 remain. Multi-session campaign continues.
- **R181 (TestClient base_url)** ✓ — `tests/conftest.py` pins `base_url="https://testserver"` on both
  client + anon_client fixtures so future `Secure`-flagged cookies aren't silently dropped.
- **R190 (login dummy hash)** strengthened — `verify_password(password, _LOGIN_DUMMY_HASH)` also runs on the
  rate-limited branch so the throttle path matches PBKDF2 timing of the legitimate path.
- **R88 / R128 hygiene** — `_login_attempts` dict now prunes expired/empty entries when it grows past 512
  to refuse the unbounded-growth spray case (Agent 6 M3 from v.18).
- **R126 (startup config validation)** ✓ — new `_validate_required_config` runs before `ensure_database`
  and SystemExits with a named reason if `FARM_DB_HOST` / `FARM_DB_NAME` aren't set. Posture line logged
  at WARN.
- **R181 selftest extension** ✓ — added `security/master_key_perms`, `security/farm_app_role`,
  `security/security_alerts_module` checks plus `backup/restore_test` from v.19.
- **MED authz gating sweep** ✓ — 8 additional handlers gated: `hfm/drafts.py` GET/POST/DELETE now scoped to
  `(device_id, user_id)` with `hfm_drafts_user_id` migration; `import_hub/staging/{id}/import`,
  `staging/{id}/import-tabular`, DELETE `staging/{id}` role-gated; `gsm/routes.py` `accept_machine_boundary`,
  `gsm_pull`, `gsm_sync_kb`, `gsm_ignore_event`, `gsm_restore_event` role-gated.
- **Bandit MED** ✓ — 7 B608 nosec annotations + B104 verified pre-existing. 46 MED → 37 MED. 0 HIGH.
  Remaining B608 sites follow the same safe `IN ({placeholders})` pattern (mechanical bulk-annotate
  follow-up).
- **R166 cleanup** — `_update_store_repos` error-log swapped to `type(exc).__name__` so a failed POST
  can't echo the URL via traceback (companion to v.19 R168 work).

Deferred (still ❌ / ◔):
- **R178** — 697 inline handlers remaining; multi-session campaign continues.
- **R141 / R172** — `_verify_internal` IP-range fallback retained for backwards compat; **now alerts** on
  every success so legitimate traffic is observable. Drop after one observation cycle.
- **R169** — ~756 inline `style=` attributes still remain (770 → ~756). Multi-session campaign.

## 2026.6.19

Second wave of the 190-rule close-out (continuing from v.18). Six of the
seven `❌` rows in `docs/AUDIT.md` flipped to `✓` or `◔`.

- **R168** — `core/pat_manager.py::_update_store_repos` documented as a
  Supervisor-API exception: the URL form is mandated by HA's
  `/store/repositories` endpoint, the token is the read-only Supervisor
  PAT (Rule 136 scope), and v.18's `RedactingFormatter` + `httpx`-WARNING
  pin keep it off all log surfaces. Error logging swapped to `type(exc).__name__`
  so a failed POST can't echo the URL.
- **R171** — new `core/security_alerts.py`; throttled `fire(event_type,
  ctx)` POSTs an HMAC-signed envelope to the GSM cloudhook via
  `gsm.client.gsm_request` (per-event-type 60 s gap, per-key 300 s gap).
  Wired on: HMAC verify failure / replay on `/gsm/api/receive-layer`,
  login brute-force lockout, backup restore, sync-to-prod.
- **R173** — `_pool._init_pool` no longer falls back to the `postgres`
  superuser when `farm_app` is unavailable; raises `RuntimeError` instead.
  `_migrate._ensure_app_role` runs on every startup: creates `farm_app`
  with `NOINHERIT NOCREATEDB NOCREATEROLE NOSUPERUSER`, grants
  `SELECT/INSERT/UPDATE/DELETE` on existing + default-future tables,
  revokes `CREATE` on the schema so SQL-injection can't add tables.
- **R174** — `core/backup.py` rewritten: pg_dump → gzip → Fernet
  (`cryptography.fernet`, key derived from `/data/keys/master.key`). Files
  named `paddisense-farm_<date>.sql.gz.enc`. New `restore_test()` decrypts
  + parses the newest archive and verifies the `PostgreSQL database dump`
  header. Wired into `core/selftest.py::run_all_tests` as `backup/restore_test`.
- **R175** — new `core/text.for_agent()` fence that strips control characters,
  collapses whitespace, hard-truncates and wraps user input in
  `[UNTRUSTED: …]`. Applied at `gsm/export.py::_build_event_dict` to
  every free-text field that crosses the cloudhook boundary into the GSM
  Admin dashboard a Claude reads (`paddock_name`, `farm_name`, `crop_type`,
  `variety`, `product`, `rate_unit`, `operator`, `applicator`, `notes`,
  `observation_type`, `severity`).
- **R161 (Fernet at-rest)** — `core/db/_pool._ensure_master_key()` now
  generates the 32-byte key on first run and writes it 0600. Means a
  fresh install gets least-priv DB + encrypted backups by default
  instead of requiring a manual step.
- **R190** — login error strings collapsed to a single
  "Invalid username or password" across all failure modes (no-user,
  wrong-password, rate-limited); `verify_password` always runs against
  a dummy PBKDF2 hash on the no-user branch so latency doesn't leak
  enumeration.
- **R166** — six `JSONResponse({"error": f"...: {exc}"})` sites cleaned
  up: `gsm/routes.py:1885,1915` (now "Upstream addon unreachable") and
  `import_hub/routes.py:1043,1145,1945` (generic + `log.exception` to
  capture the detail server-side).
- **R82** — 23 CDN `<script>` / `<link>` tags across `pages/shared/`,
  `pages/desktop/`, `static/map/` now carry `integrity="sha384-…"` +
  `crossorigin="anonymous"`. Floating version specifiers pinned
  (`leaflet@1.9 → 1.9.4`, `chart.js@4 → 4.5.1`, `@turf/turf@7 → 7.3.5`).

Deferred (still ❌ / ◔):
- **R157** — `CsrfMiddleware` rebuild as signed double-submit token. Needs
  CSRF token rendered into ~30 templates as a `<meta>` tag + JS attach.
  Sprint.
- **R141 / R172** — `_verify_internal` 172.30.32.0/23 fallback still
  trusts the supervisor bridge. Coordinated change with Core.
- **R178** — 758 inline event handlers across templates. Multi-session
  campaign.
- **R159** — `_validate_url` DNS-rebinding TOCTOU; KB pack sync bypasses
  the guard entirely. Sprint.

## 2026.6.18

**Full 190-rule (Golden Rules v2.23) audit + adversarial red-team close-out.**

Auth / signature / replay:
- R141/R142: HMAC body-binding fix on `/gsm/api/receive-layer` — server now computes `sha256(body)` instead of trusting the attacker-controlled `X-Body-Hash` header; empty-nonce fallback removed (was a body-binding bypass).
- R142: nonce replay store — new migration `gsm_seen_nonces` table; `_verify_hmac` inserts the nonce atomically inside the drift window so a captured signature can't be replayed.
- R143: `_verify_internal` Bearer compare now uses `hmac.compare_digest`; constant-time path also added to KB-pack SHA-256 verification.
- R144: `/health` trimmed to liveness-only shape; diagnostic detail moved to `/api/v1/health/detail` (admin auth). `/api/licence` requires auth — no longer in `_PUBLIC_PATHS` (enrolment state is no longer a probe oracle).

Output safety / log leakage (R88, R164, R166):
- New `core/log_redact.py` — `RedactingFormatter` wired on the root handler in `__main__.py` so message AND traceback are scrubbed for cloudhook URLs, GitHub PATs, `Bearer` tokens, `re_*`, `hbk_*`, basic-auth URLs and `x-access-token:` URL credentials.
- `httpx` and `httpcore` loggers pinned to WARNING (closes the auto-INFO `POST https://hooks.nabu.casa/<token>` leak path).
- `ensure_first_user` no longer logs the generated admin password; written to `/data/.admin_initial_pw` 0600 and only the path is logged.
- Licence code never logged or returned in the activation response — length-only redacted form (R164).
- Reserved LogRecord key `"created"` in `extra={}` renamed to `zones_created` (two call sites in `api/crop_zones.py`).

Authorization sweep (R141/R153/R160):
- New shared `core.auth.require_role` helper.
- Gated 16 previously-ungated mutation handlers across `gsm/routes.py` (enroll-core, enroll-gsm), `api/spatial.py` (farm/crop/season create/update/delete + `update_boundary`), `api/crop_zones.py` (merge, split, merge-and-save, create, seed-fallow, geometry-update, update, delete, auto-create), `api/notifications.py` (create/update/delete/test), `rtr/routes.py` (set-url, refresh, clear), `ndvi/routes.py` (save_credentials + test) and `kb/packs.py` (ndvi-credentials save).
- `update_paddock`: dropped `farm_id` from the bulk-update field list — cross-farm reassignment must go through a dedicated manager-gated move endpoint (deferred).

Middleware (R156/R158):
- `BodySizeLimitMiddleware` rewritten as ASGI middleware: streaming byte-count + Content-Length pre-check. Closes the `Transfer-Encoding: chunked` bypass and forged-Content-Length+oversized-body bypass.
- Session cookie `secure=` now conditional on `X-Forwarded-Proto == https` (matches GSM v.325 pattern; previously unconditional `secure=True` broke the HA-ingress HTTP hop).

Parser DoS (R160/R170):
- `xml.etree.ElementTree` → `defusedxml.ElementTree` in `import_hub/parsers.py` and `machine/isoxml_parser.py` (billion-laughs entity expansion mitigation).
- New `check_zip_safety(path)` in `import_hub/parsers.py`: aggregate-size cap (500 MB), entry-count cap (1000), per-entry compression-ratio cap (100:1). Applied before extract/open in `machine/isoxml_parser.py`, `machine/shapefile_parser.py`, and `import_hub/parsers.py` shapefile paths.

CVE bump (R155):
- `cryptography` 46.0.7 → 48.0.1 (GHSA-537c-gmf6-5ccf)
- `python-multipart` 0.0.27 → 0.0.31 (CVE-2026-53538/53539/53540)
- `pytest` 8.4.1 → 9.0.3 (CVE-2025-71176 — dev only)
- `defusedxml` 0.7.1 added.

Naming hygiene:
- GIS → Farm rename completed across 10 files (~28 occurrences): `_GIS_TABLES` → `_FARM_TABLES` in migrations; remaining user-facing strings in pages/desktop, pages/mobile, tests/test_smoke.py and docs/AUDIT.md. Environment-variable fallbacks (`GIS_DB_*`, `GIS_DATA_DIR`), wire-format identifiers (`IMPORT_TYPE_GIS`, `gis_boundaries`), and the `/config/GIS` filesystem path retained for backwards compatibility with installed grower boxes.

Deferred to next session:
- `CsrfMiddleware` rebuild as signed double-submit token (currently content-type sniffer, R157 partial).
- `_validate_url` DNS-rebinding TOCTOU + scheme=https enforcement (R159).
- `core/pat_manager.py` PAT-in-URL → `GIT_ASKPASS` (R168).
- `farm_app` DB role + schema-grants SQL + drop the `postgres`/`homeassistant` defaults (R148/R160/R173).
- Backup encryption + restore-test selftest + off-box replication (R161/R174).
- Security-alert module wiring (R171).
- R175 untrusted-data sanitiser at GSM export render boundary.
- R178 inline-handler sweep (758 handlers) — prereq for nonce-based CSP.
- KB-push HMAC signing — cross-Claude WR (GSM side currently doesn't sign per CLAUDE.md; needs WR to GSM/Admin).
- CDN SRI sweep (25 tags).

## 2026.6.15
- **Full rename: PaddiSense GIS -> PaddiSense Farm**
- Package directory: `paddisense_gis/` -> `paddisense_farm/`
- Addon slug: `paddisense-gis` -> `paddisense-farm`
- Panel title: GIS -> Farm
- Cookie: `gis_session` -> `farm_session`
- DB role: `gis_app` -> `farm_app`
- DB name default: `paddisense_gis` -> `paddisense_farm`
- Env vars: `GIS_DB_*` / `GIS_DATA_DIR` -> `FARM_DB_*` / `FARM_DATA_DIR` (with backward-compatible fallback)
- Identity endpoint: `paddisense-gis` -> `paddisense-farm`
- All HTML templates, display names, and comments updated

## 2026.6.12
- Rule 128: justification comments on mutable globals
- Rule 132: HA entity staleness guard on `/api/my-location`
- Rule 134: graceful shutdown handler (close DB pools)
- Rule 135: fix CHANGELOG version numbers
- Rule 137: acknowledge blocking psycopg2 in CLAUDE.md
- Rule 156: cookie secure flag on login
- Rule 158: body size limit + sensitive endpoint rate limiting middleware
- Rule 13: JSONB justification comments in schema.sql

## 2026.6.11
- Golden Rules v2.2 audit quick-win gap closure
- Two-token PAT model propagation

## 2026.6.10
- Full 110-rule Golden Rules audit and gap closure
- GIS DB separation complete (own `paddisense_gis` database)
- Cache busting rollout (Layer 1-3 static asset versioning)
- Dual-pool DB pattern (gis_app + postgres admin)

## 2026.6.5
- Stripped Core functions (metrics, database, GSM UI) — GIS is farming only
- GSM boundary exchange moved to GIS module card in Core
- Migrated to own `paddisense_gis` database

## 2026.6.4
- Fix licence check — uses provider_credentials table

## 2026.6.2
- Dashboard tile launcher (Farm Map, Events, RTR, Data Sync, Import Hub)
- Removed Weather/Chem/Burn tiles (separate addons now)

## 2026.6.1
- Initial release — extracted from PaddiSense Core
- Spatial engine, HFM field events, machine data, NDVI, Import Hub
- GSM boundary sync, planning, analytics, RTR, KB
