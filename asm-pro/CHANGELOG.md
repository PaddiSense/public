# Changelog

## 2026.7.33 — Your Base list choices now define what a new site starts with

### Changed
- When you tick **Base** items on a config list, a brand-new grower site now
  starts with **exactly those** items — your deselections take effect. Lists you
  don't curate keep their full sensible defaults. Your own site (and any existing
  site) is never changed — this only shapes what a fresh install begins with.

## 2026.7.32 — HA device/person pickers now work

### Fixed
- The Home Assistant device and person pickers (notification group targets, and
  Add Person) now load — they were coming up empty because the add-on wasn't
  sending its Home Assistant access token. This also restores Home Assistant
  push notifications, which had the same underlying cause.

## 2026.7.31 — Internal: surface HA lookup errors

### Fixed
- Internal diagnostics — the Home Assistant device/person lookups now log why they
  failed, so an empty picker can be traced. No user-visible change yet.

## 2026.7.30 — Pick people & notify targets from Home Assistant

### Changed
- **Notification group targets are now a tick-list of your Home Assistant devices**
  — no more typing `mobile_app_…` service names. Tick the phones/tablets to notify.
  (If a group already pointed at a device HA no longer reports, it stays ticked so
  nothing is dropped.)
- **Add Person can pick from your Home Assistant users** — choose a person and the
  name (and username) fill in for you. You can still type a name manually.

## 2026.7.29 — Maintenance & prestart flow fixes

### Fixed
- **Prestart cards now expand when you tap them** — both passed and failed checks —
  so you can open a completed prestart and see its detail. (The tap was previously
  unwired, and needed a second click.)
- **The Issue badge on a prestart card opens the issue straight away** — one tap into
  the issue detail, no more double-click via the maintenance list.
- **Conduct Work from an issue no longer re-asks for everything** — the service form
  opens with the asset pre-filled and linked back to the issue, and logging the
  service **automatically resolves that issue** (link + status) in the one flow.
- **The part picker now shows each part's number (and category)** next to the name,
  so 30 "Bearing" rows are actually distinguishable.
- **Adding a checklist item works for categories with a slash** (e.g. "ATV/Motorcycle")
  — it previously failed with a "Failed to add" toast.

### Changed
- **Every pop-up (modal) now has comfortable padding** — text no longer sits hard
  against the edge of the box.
- **Adding a Site / Area / Location is now type-specific** — the form knows which
  level you're adding (no re-selecting the type), and only a Site asks for an address.
- **The location hierarchy reads Site → Area → Location** (e.g. RRAPL → Machinery Shed
  → Top Shelf).

## 2026.7.28 — Prestart checklists on the commercial editor (Phase 5)

### Changed
- The **Per-Category Checklists** editor now matches the rest of config: inline
  label rename, inline response-type picker, up/down reorder, On/Off (active)
  toggle, Base tick (authoring box), and delete — inside the same tile. Checklist
  items moved from flat JSON to the normalised store; a one-time, marker-guarded
  backfill copies existing checklists over on first start, and the prestart form
  reads them live. Nothing is lost.

## 2026.7.27 — Commercial config editor (Phase 7): full migration live

### Changed
- **The config lists now use the full commercial editor**, matching the fleet
  standard: inline rename, up/down reorder, On/Off (active) toggle, and a **Base**
  tick (on the authoring box) that marks items shipped to fresh grower boxes — all
  inside your existing tile navigation. Delete removes an item.
- **The normalised config is now the live source** (`use_normalised_config` flipped
  ON via a one-time, self-reconciling migration): on first start the normalised
  tables are synced from the existing config, then become authoritative, so what
  you edit is what the app reads. No config is lost — the migration reconciles
  before flipping and runs exactly once.
- New `seed_author_mode` add-on option (default off) gates the Base ticks to the
  authoring box.

## 2026.7.26 — Stale-tab update banner

### Added
- After a deploy, any tab left open still runs the old page. Both desktop and
  mobile now poll `/health` (every minute + when the tab refocuses) and, when a
  newer version is live, show a "tap to reload" banner. It never auto-reloads, so
  you're never interrupted mid-form.

## 2026.7.25 — Service delete: atomic stock reversal

### Fixed
- Deleting a service event reversed its part-stock deductions in separate
  transactions and then deleted the record, so a failed delete could double-count
  the returned stock. The stock reversal and the delete now commit together.

## 2026.7.24 — Location re-parent scoping + service/stock atomicity

### Fixed
- **Location re-parenting can't escape scope.** Updating a location verified access
  to that location but not to a new `parent_location_id`, so a scoped supervisor
  could move their location under a site they can't access. Now 403 if the caller
  can't access the new parent.
- **Service + stock deductions are atomic.** A service event was written and
  committed, then its part deductions ran as separate transactions — a failure
  part-way left the service recorded with partial/no stock changes. The service
  write and all its deductions now commit (or roll back) as one transaction.

## 2026.7.23 — Prestart cadence-check location scoping

### Fixed
- The prestart **cadence-check** endpoint had no location check, leaking whether an
  asset (at any location) had a recent prestart and its result. It now 404s for
  assets the caller can't access, matching the other object-scoped routes.

## 2026.7.22 — Input validation + safer photo delete

### Fixed
- **Stock adjust validates input.** A non-numeric quantity returned a raw 500; it
  now returns a clean 400. A genuine zero adjustment is no longer silently dropped.
- **Photo delete is crash-safe.** The photo row is now deleted before its files are
  removed, so a failed delete leaves a reclaimable orphan file rather than a record
  pointing at missing bytes.

## 2026.7.21 — Location access-control + stock integrity fixes

### Fixed
- **Stock can no longer go negative.** An over-deduction (consuming more of a part
  than on hand) drove a location's qty negative and corrupted the total-stock sum;
  the adjustment now floors at 0.
- **Administrator location bypass restored.** `check_location_access` compared the
  role to `"admin"`, but roles are stored canonically as `"administrator"`, so the
  bypass was dead code and a scoped-created administrator was wrongly denied
  location-scoped objects. Now uses the role hierarchy (`has_role`).
- **Asset detail page + sub-pages are location-scoped.** The asset detail HTML page
  and its 7 sub-pages rendered an asset with no location check (only the JSON API
  was scoped) — a user could view an asset at another location. Now 404 cross-
  location, matching the JSON path.
- **Asset summary / linked-parts / linked-assets APIs scoped.** `/summary` and
  `/linked-parts` now 404 cross-location; a part's `/linked-assets` filters out
  assets the caller can't access.

## 2026.7.20 — Faster photos: thumbnails + upload normalisation

### Added
- **Thumbnails on upload.** Photos now generate a small (~480px) thumbnail; photo
  grids load the thumbnail instead of the full-resolution original, so a gallery is
  far lighter and faster (especially on mobile / the locked-down office PC). The
  full image still opens in the zoomable viewer. Grid images are lazy-loaded.
- **Upload normalisation.** Uploaded photos are auto-rotated to their correct EXIF
  orientation (no more sideways phone photos), capped to a sensible max size (still
  zoom-readable — e.g. wiring diagrams), and stripped of EXIF/GPS metadata. Wiring
  diagrams / screenshots (PNG) are kept lossless as PNG; photos re-encode JPEG.
- Legacy photos are backfilled with a thumbnail on first view (self-healing); both
  operations are fail-safe — a processing error never blocks or loses an upload.

## 2026.7.19 — Zoomable photo viewer

### Added
- **Zoom & pan in the photo viewer** (asset photos, desktop + mobile): scroll or
  double-click to zoom (pinch + double-tap on mobile), drag to pan. Fixes not being
  able to read detail in a photo — e.g. a wiring diagram stored against an asset.
  Shared `static/js/photo-zoom.js` module (self-hosted, nonce-CSP friendly).

## 2026.7.18 — Phase 4 (part 8): photo-required prestart checks

### Added
- **Photo-required** prestart checks (desktop + mobile): an item set to the
  photo-required response type shows a **Take Photo** button (camera on mobile).
  The captured photo is stored against the asset and the item is marked complete;
  the photo appears inline in the prestart history/report. Stored by reference (a
  photo id in the record), not inline — so prestart records stay lean.

This completes the Phase 4 typed prestart response kinds: numeric, rating, open-
ended, signature, checkbox-multi (named types), and photo-required.

## 2026.7.17 — Phase 4 (part 7): checkbox-multi prestart checks (named types)

### Added
- **Named checkbox response types.** Config → Prestart → Checklist Response Types
  gains a **Typed Response Types** editor: create named checkbox types (e.g. "PPE
  Check" → helmet/vest/boots), each with its own tick-box options; edit options;
  delete. Assign one to a checklist item and that item renders those checkboxes on
  the prestart form (desktop + mobile), recording the ticked options into the
  record + report. Base kinds are protected from deletion; options changes are
  version-guarded with a full history trail.

## 2026.7.16 — Phase 4 (part 6): signature prestart checks

### Added
- **Signature** prestart checks (desktop + mobile): an item set to the signature response
  type renders a signing pad (draw with mouse/finger/stylus, Clear to redo). The signature
  is captured as a white-paper/dark-ink image into the record and shown inline in the
  prestart history/report, so it reads on any theme. Now active + assignable end-to-end.

## 2026.7.15 — Phase 4 (part 5): open-ended + checkbox-multi prestart checks

### Added
- **Open-ended** prestart checks (desktop + mobile): an item set to the open-ended response
  type now renders a text-note input (was a Pass/Fail toggle); the note is captured into the
  record + report. (open-ended was already active, so this makes it render correctly typed.)
- **Checkbox-multi** render code (desktop + mobile) — checkboxes from the response type's
  `config.options`. Present but staged inactive until an options-editor UI lands (assigning
  it without options would create an uncheckable item), so it's dormant for now.

## 2026.7.14 — Phase 4 (part 4): rating 1–5 + registry-wired config picker

### Added
- **Rating 1–5** prestart checks (desktop + mobile): an item set to a rating response type
  renders a 1–5 button selector; pass/fail from an optional minimum passing rating, else
  recorded. Value captured into the record + report.
- The config checklist editor's **response-type picker now offers the active render-kind
  registry** (numeric, rating, …) alongside the existing types, so admins can assign the
  typed checks. Render-ready kinds are kept active in the registry automatically.
  → numeric and rating are now usable end-to-end (assign in Config, capture in a prestart).

## 2026.7.13 — Phase 4 (part 3): numeric prestart checks on mobile

### Added
- The mobile prestart form now renders numeric checklist items as a touch-sized number
  input, matching desktop — Companion / field users get typed readings too. Same
  registry-driven dispatch, pass/fail from optional min/max, value captured into the
  record + report. Additive (boolean tap card by default).

## 2026.7.12 — commercial list-management Phase 4 (part 2): numeric prestart checks (desktop)

### Added
- Prestart checklist items can now be **numeric**. A checklist item whose response type
  maps to render_kind `numeric` renders a number input on the desktop prestart form
  (registry-driven) instead of the Pass/Fail toggle; the reading is captured into the
  prestart record and shown in the report. Optional min/max in the response-type config
  sets pass/fail (in-range = pass); with no thresholds the reading is just recorded.
  Additive — items keep the boolean toggle unless explicitly set to a numeric response
  type. Mobile + the other new render kinds (rating / checkbox / signature / photo) follow.

## 2026.7.11 — commercial list-management Phase 4 (part 1): response-type registry API

### Added
- `GET /api/response-types` serves the active `asm_response_types` rows (the prestart
  form's render registry: `type_key`, `label`, `render_kind`, `config`). The 4 shipped
  kinds are active; the 4 commercial kinds (`checkbox_multi`, `rating_1_5`,
  `photo_required`, `signature`) stay staged-inactive until their render UIs land.
  Dormant — no consumer yet (the prestart-form dispatcher + the new-kind UIs are the
  next, design-led step).

## 2026.7.10 — commercial list-management Phase 3: consumer sweep (flag-gated read path)

### Changed
- Config dropdowns now read through one flag-gated path (`db_lists.active_values`):
  the normalised `asm_config_items` when `use_normalised_config` is ON, the legacy
  JSON config when OFF. The flag stays OFF, so there is no behaviour change yet —
  but flipping it ON switches every dropdown to the per-row tables, honouring the
  Base tick and inactive-hide. A key never backfilled still falls back to JSON, so a
  half-migrated box never shows an empty dropdown.

## 2026.7.9 — commercial list-management Phase 2: config write API + base-seed

### Added
- Write API for the normalised config lists (`/api/config-items/*`): optimistic
  concurrency (409 on a stale version, returning the current row for conflict
  resolution), per-item history, and a transactional rename-cascade to dependent
  tables. Dormant behind `use_normalised_config` (OFF) — the live config UI is
  unchanged until a later phase switches consumers over.
- Base-seed model, matching the other addons — a **Base** tick (`is_base`/`base_key`)
  on config items, a release snapshot (`python -m asmpro.seed.snapshot`) that bakes
  the ticked set into `base_seed.json`, and a tombstoned grower seeder so each base
  item seeds once and a grower's deletion is never resurrected.

## 2026.7.8 — canonical tile-config UI + commercial list-management groundwork

### Changed
- Config page migrated onto the canonical master config component. The domain
  tile-grid nav is now a shared fleet component (`ps-config-tiles` / `ps-config-tile` /
  `ps-config-panel`) promoted into the master theme, with `ps-config-section` /
  `ps-list-table` inside each domain. The v.65 tile design is preserved; the
  hand-rolled local config styles are retired.

### Added
- Commercial-grade list management — Phase 1 (schema only, feature-flag OFF).
  Normalised per-row config tables (`asm_config_items`, `asm_response_types`,
  `asm_prestart_checklist_items` + companion history tables + a registry) with an
  idempotent, empty-target-guarded backfill from the existing config. No runtime
  behaviour change yet — the flat-JSON config stays the source of truth until a
  later phase switches consumers over.

## 2026.7.7 — owner-login rotation self-heal (WR-PS-192/074 structural fix) + Pillow CVE lift

### Security
- Dependency update: Pillow 12.2.0 → 12.3.0 (clears 6 published CVEs; release gate Rule 155).

### Fixed
- **Incident 2026-07-27 (Weather was the victim; ASM-Pro carried the same latent bug):**
  a flipped `*_owner` login uses a STATIC stored options password; a DB-role seed re-mint
  changes the Postgres role underneath it and the addon strands on its next restart
  (DB init fails → licence gate fail-closed → licence screen).
- Structural fix ported from Weather v2026.7.9 (commit bd8d124) into `asmpro/db/_pool.py`:
  for `*_owner` logins the password is now DERIVED from the `/share` box key first (the
  fleet's derivation truth, Core v2026.7.44), with the stored options password as fallback;
  loud WARNING when the stored copy is stale. The admin/owner pool also gained the same
  auth-failure rebuild-and-retry self-heal the app pool has had since 2026-07-09.
  `db_user: postgres` (pre-flip) boxes are unaffected — stored password only, never derived.
- Regression tests: owner candidate ladder + admin-pool self-heal + end-to-end
  stale-stored-password recovery (throwaway role `asm_selfheal_test_owner`). The old
  `test_admin_pool_never_selfheals` assertion — which encoded the incident's faulty
  assumption — is INVERTED with a comment citing incident 2026-07-27.

### Changed
- `paddisense-tokens.css` re-cp'd from the canonical master (Rule 17 gate — the stored
  copy had drifted behind the fleet palette-consolidation pass; no ASM-Pro CSS change).

## 2026.7.6 — WR-PS-108 fleet flip: access-sync enforce ON by default

### Changed
- **Unsigned or invalid grant pushes are now rejected with 403.**
  `ASM_ACCESS_SYNC_ENFORCE` defaults ON (`=0` kill-switch — code-default
  pattern, grower boxes have no env plumbing). Core's signed pushes have been
  verifying and pinning since the receiver landed; this closes the warn-only
  window fleet-wide (WR-PS-108, Peter's go 2026-07-17). A `bound_fp` mismatch
  already failed closed before this flip.

### Fixed
- **Real Admin-signed instructions were rejected (WR-ADMIN-006 re-vendor).**
  The vendored `core/licence_verify.py` read the nonce subject only from
  `licence_id`, but a signed INSTRUCTION carries it under `target` — every
  real revoke/deactivate 401'd as `invalid_signature` while forgeries were
  (correctly) rejected, so the negative-only suite never caught it. Re-vendored
  byte-identical from the fixed canonical (`licence_id or target`, GSM
  v2026.7.51 fix) + the missing POSITIVE regression test (a genuinely signed,
  real-shaped instruction must verify).


## 2026.7.5 — Services filter-bar fix + access-sync verify-and-pin (WR-PS-108)

### Fixed
- **ASM.07.B (Services, desktop) filter bar no longer over-tall / dropdown detached.** The Asset
  autocomplete wrapper `.svc-asset-search` carried `flex: 1 1 260px`, but it sits inside a
  `flex-direction: column` `.ps-filter-group`, so the `260px` became a **height** — inflating the
  filter card and pushing the `top:100%` suggestion list ~260px below the input. Changed to
  `width: 100%; max-width: 360px`; the card now sizes to the input and the list attaches directly
  beneath it, matching ASM.03.

### Added
- **`/api/access/sync` verify-and-pin** (WR-PS-108 / Hone SEC-04, §9-A.9). Core's grant push is now
  Ed25519-verified, its key bound to the licence `bound_fp` (never bare TOFU on the `/23`), with
  target/expiry/single-use-nonce enforcement. `bound_fp` mismatch fails closed always; unsigned/invalid
  is warn-only until the fleet-wide `ASM_ACCESS_SYNC_ENFORCE` flip. `bound_fp` persisted from the
  signature-verified licence on activate. Vendored from the SugarSense reference; +7 tests.

## 2026.7.4 — Key-read diagnostic on the DB-role key path (WR-PS-090 Ask 4)

### Added
- **`_read_master_key()` now logs the box-key source + fingerprint on every read** (WR-PS-090 Ask 4, PWM reference diagnostic): `source=<path> fp=<sha256[:12]> dev/ino/size/mtime`, in preference order (`/share` db_role.key → `/share` master.key → local `/data`). A silent fallback here means this addon's derived `asm_app` password no longer matches the role Core minted — which fail-closes every request-path query — and a fake overlay `/share` is now visible via the logged `st_dev`. Completes the P-pool adoption of the diagnostic that cracked the 2026-07-06 fake-`/share` incident and the WR-PS-110 key churn. No behaviour change to the key preference order; an empty key file is now skipped rather than returned.

## 2026.7.3 — Fix: unlicensed boxes 404'd instead of reaching the licence page (WR-PS-046)

### Fixed
- **Licence-gate redirect dropped the HA ingress prefix.** `licence_gate` runs OUTER of the auth
  middleware (registered after → wraps outside), so `request.state.base_path` was unset at
  redirect time and an unlicensed page request bounced to a bare `/licence` — outside the ingress
  mount → HA 404. The gate now reads `X-Ingress-Path` directly (Core v2026.6.388 pattern). Found
  in the 2026-07-12 WR-PS-046 fleet verification sweep; 4 regression tests
  (`tests/test_licence_gate_ingress.py` — they delenv the gate's pytest bypass so the real
  redirect path runs). Suite 211+4 green.

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

## 2026.7.1 — WR-PS-109: per-user module-access enforcement on ingress (Hone SEC-04/SEC-09, Option B)

### Added
- **`core/module_gate.py`** (vendored from the Farm reference): Core pushes its `module_access`
  grant table to `POST /api/access/sync`; ASM-Pro caches it durably in
  `/data/module_access_grants.json` (atomic swap) and enforces per-user access locally on every
  **ingress** request. Decision semantics mirror Core's `effective_modules`: never-synced → open
  (bootstrap), synced-no-entries → open, granted/all-access/admin → allow, configured-but-ungranted
  → **403**. A direct cookie login with ASM-Pro's own credentials keeps its existing role path.
- **`POST /api/access/sync`** receiver — trust = the same transport gate the licence-forward path
  uses (`_verify_internal`); the §9-A.9 signed-grant envelope is the tracked fleet follow-up
  WR-PS-108.
- **`tests/test_module_gate.py`** (11) — decision-table units + end-to-end through the REAL auth
  middleware: ungranted ingress user 403s on pages and API paths, granted user passes, never-synced
  box stays open, corrupt cache never locks the grower out.

## 2026.6.128 — Rotation self-heal for the app DB pool (incident 2026-07-09, Rule 106)

### Fixed
- **App DB pool self-heals across a box-key rotation.** When Core rotates the box key (`db_role.key`,
  WR-PS-088 / ADR-013), the app DB password changes; a long-running pool holds the old one, so the next
  fresh connection fails auth and the add-on breaks until a manual restart — which a grower can't do.
  `_acquire_conn` now treats a `password authentication failed` on the app pool as a stale key: drops
  the pool, rebuilds it (re-reading `/share/paddisense/db_role.key`), and retries once; a second
  failure propagates. Never applies to the admin/superuser pool (R173 intact). Fleet-wide fix
  originating from the live PWM incident. `tests/test_pool_selfheal.py`.

## 2026.6.127 — Hone PS-SEC-19: mask secret config fields + Rule 17 theme re-sync

### Fixed
- **`admin_key` rendered UNMASKED in the Home Assistant add-on options UI (Hone PS-SEC-19).**
  The `schema:` type was `str?`, so HA drew a plain text input: the secret was visible on
  screen, in screenshots, and over a shoulder. Changed to `password?` — the same type
  `db_password` already uses here, and the type GSM already uses for its `admin_key`. No
  functional change: existing values are untouched, only the input is masked.
- **Rule 17: `static/paddisense-tokens.css` re-copied from the canonical master.** Master gained
  `main.ps-fullscreen` on 2026-07-09 (WR-PS-093 steward closure) and the change was never
  propagated, leaving every addon byte-divergent and its next commit blocked by the Rule 17
  gate. Verified the drift was that one additive block — nothing local was clobbered.

## 2026.6.126 — WR-PS-088 Phase-1a: prefer /share/paddisense/db_role.key for the *_app DB password

### Database auth (additive, no behaviour change today)
- `asmpro/db/_pool.py::_read_master_key()` now reads **`/share/paddisense/db_role.key` first**, then
  falls back to the existing `/share/paddisense/master.key`, then the local `/data` key, then `None`.
  Prefer the dedicated /share db_role.key for the *_app DB password; falls back to master.key during
  the WR-PS-088 split rollout — no behaviour change today (Core publishes both keys with the same
  value until the 1b flip, when db_role.key becomes distinct and master.key is retired).
- Fail-closed / no-superuser-fallback logic, the DSN builder, the local key fallback and every other
  code path are unchanged.

## 2026.6.125 — R142 replay protection now PROVEN by regression (N/A → COVERED)

### Security tests (REQUIRED_SECURITY_TESTS — R142 reclassified)
- **R142 (replay / nonce / timestamp) was wrongly marked N/A.** Adversarial review found ASM-Pro's
  licence path *does* carry a signed anti-replay control: ASM vendors the fleet shared library
  `asmpro/core/licence_verify.py`, whose `verify_artifact()` — reached from the live activate/
  deactivate route (`asmpro/licence.py` → `evaluate_signature` → `verify_artifact`) — enforces a
  two-sided replay window on every Admin-signed licence/instruction:
  - `_fresh()` refuses a payload whose `issued_at` is in the future or `exp` in the past (±60 s skew);
  - `_nonce_ok()` records `(licence_id, nonce)` on first sight and refuses the second presentation.
- **New `tests/test_r142_licence_replay.py`** — a real behavioural regression (Rule 192, no
  name-only stub). It forges a genuine Ed25519 signature with a throwaway test key pinned via the
  library test hook and proves, through `verify_artifact`:
  - `test_fresh_unseen_nonce_is_accepted` — positive control: a fresh, first-seen artifact IS accepted;
  - `test_reused_nonce_replay_is_rejected` — the same `(licence_id, nonce)` twice → second rejected;
  - `test_stale_timestamp_is_rejected` — an expired `exp` → rejected (freshness gate);
  - `test_future_timestamp_is_rejected` — a future `issued_at` → rejected (two-sided skew window).
- The prior `test_r142_replay_no_unguarded_signed_request_nonce_window` guard is **retained** as
  belt-and-braces for any future inbound X-Signature/X-Timestamp request surface.
- `docs/AUDIT.md` manifest row 142 moved from `N/A-guarded` → `✓ COVERED` with the four test names as
  evidence.
- **No production code changed** — the fix lives entirely in `tests/` + docs. `verify_artifact` and
  the licence route are unmodified. ADR-010 flip-ready.

### In plain English
- ASM's licence system already refused a *replayed* or *expired* licence message — but there was no
  automated test proving it, and the audit had it wrongly listed as "not applicable". This release
  adds a proper test that fakes a signed licence and confirms the software (a) accepts a genuine,
  first-time message, (b) rejects the exact same message sent a second time, and (c) rejects an
  out-of-date one. Commercial-grade trust: the replay protection is now proven, not assumed. Nothing
  a grower sees or does changes.

## 2026.6.124 — security-test ENFORCEMENT: test-DB fixed so pytest runs GREEN

### Security tests (REQUIRED_SECURITY_TESTS — enforcement-ready)
- **`pytest` now runs GREEN** — `189 passed, 1 xfailed, 0 failed, 0 error`. v.123 aligned the test
  *names* to the manifest `-k` selectors, but the DB-backed rows (R153 IDOR / R154 cross-tenant /
  R188 session-revoke) still **errored at pool-init**: the least-priv `asm_app` role had no grants
  on the disposable `asmpro_test` DB, so the app pool hit `permission denied for schema public` /
  `permission denied for table …`. That meant the mandated behavioural tests never actually executed.
- **Test-only DB provisioning added to `tests/conftest.py`** (the known fleet blocker, mirrors
  Store/Sugar/Livestock):
  - `_provision_test_db` (session, autouse): as the ADMIN (`postgres`) owner, run
    `ensure_database()` (create DB + schema + seed + idempotent migrations) then `GRANT` `asm_app`
    the DML it holds in prod (SELECT/INSERT/UPDATE/DELETE on all tables + USAGE/SELECT/UPDATE on
    sequences) plus `ALTER DEFAULT PRIVILEGES` for future tables. This replicates what Core mints in
    prod; the app-under-test still **connects as the least-priv `asm_app` role**, identical to prod.
  - `ensure_database` is wrapped so its DDL/migration phase always runs as admin. In prod `startup()`
    runs once (DDL as admin -> then `init_app_pool()`); under pytest every `TestClient` context-enter
    re-fires `startup()` in one process, leaving `_app_pool_activated=True`, so the idempotent schema
    DDL would run as the DML-only role and fail. The wrapper reproduces prod's per-process ordering.
  - `app` fixture now depends on `_provision_test_db` so grants land before any startup activates the
    app pool.
- **`tests/test_videos_category.py`** — the two legacy-NULL scaffolding blocks (`ALTER TABLE … DROP/
  SET NOT NULL`) now use `get_cursor(admin=True)`: schema DDL must run as the owner, not the
  request-path `asm_app` role. The behavioural assertions still go through the app (least-priv).
- **Reproducible**: verified by dropping `asmpro_test` and re-running — conftest re-creates the DB,
  schema, and grants from scratch (60 passed / 1 xfailed on the security+CRUD subset).
- **No production code changed.** `asmpro/db/_pool.py`, `_migrate.py`, and all auth/pool paths are
  untouched — the fix lives entirely in `tests/`.
- All 12 manifest rows collect ≥1 under their `-k` selector (142/146/159/189 are honest N/A guards;
  153/154/157/158/171/187/188/190 are real behavioural tests). ADR-010 flip-ready.

## 2026.6.123 — ADR-010 flip-ready: v2.49 re-audit + full security-test manifest coverage

### Compliance
- **R118 re-audit to Golden Rules v2.49.** `CLAUDE.md` `golden_rules_version` 2.48 → 2.49. Wave-4a
  merges re-verified against ASM (R34/35/36→R19, R56→R65, R73→R74, R124→R133, R145/148→R160,
  R147→R166, R99→R98) — no behavioural drift. Confirmed ASM owns **no** relocated Category-A rule
  (R33→Core/PWM/SeedMgr/SugarSense, R28→PWM), so no rule body relocated into ASM's CLAUDE.md.
- **`docs/AUDIT.md`** refreshed: `last_audit_date=2026-07-04`, `golden_rules_version=2.49`,
  `version=2026.6.123`. One real residual gap recorded per R98 (R170 Detect/Respond/Recover layers
  still light; R16/R177 mobile `pages/mobile/base.html` still absent).

### Security tests (REQUIRED_SECURITY_TESTS — 12-row manifest)
- **Full 12/12 genuine coverage.** Six existing behavioural/guard tests were misnamed so the
  manifest `pytest -k` selectors did not collect them (they were previously matched only by
  incidental false positives — e.g. R142 by CSP `nonce` tests, R154 by a licence `forbidden` test,
  R159 by a smoke `loopback` test). Renamed to embed the manifest keyword so each row now collects
  its **own** genuine test:
  - R146 `test_r146_csv_injection_no_export_surface_without_sanitiser`
  - R153 `test_r153_idor_contractor_cannot_mutate_asset_in_other_location`
  - R154 `test_r154_cross_tenant_GET_does_not_leak_foreign_object`
  - R159 `test_r159_ssrf_no_user_controlled_outbound_http`
  - R188 `test_r188_credential_change_revokes_existing_sessions`
  - R189 `test_r189_email_throttle_no_send_surface`
- **R142 (replay/nonce/timestamp) guard added** — `test_r142_replay_no_unguarded_signed_request_nonce_window`.
  ASM has no per-request HMAC/timestamp-signed inbound surface (the Ed25519 licence is a static,
  reusable credential, not a replay-windowed request → R142 N/A today). The guard fails if any PR
  adds an `X-Signature`/`X-Timestamp` ingress without a nonce+timestamp replay window.
- No production code changed; behaviour identical. The three DB-backed IDOR/session tests (R153/154/188)
  require a credentialed test TimescaleDB; they were DB-dependent before the rename and remain so.

## 2026.6.122 — SEC-08/R173: fail-closed DB app pool (Phase-2, WR-PS-081)

### Security
- **The request-path DB pool is now fail-closed (R173/SEC-08).** `_pool.py` no longer falls back to
  the `postgres` superuser if the `asm_app` app pool can't initialise — `get_cursor()` returns the
  least-priv app pool or raises. Migrations/DDL still use the admin pool during the startup window
  (before `init_app_pool()` is called). Converges the fleet to Farm's fail-closed posture; a future
  key/role failure now fails loudly instead of silently promoting request-path queries to superuser.
  (`/share` persists, so an established box that reboots keeps its key and does not fail-closed.)

## 2026.6.121 — SEC-08/R173: admin/app DB pool split — ASM now runs least-priv (WR-PS-081)

### Security
- **`db/_pool.py` now maintains two pools** — an **admin** pool (`postgres` superuser) for
  migrations/DDL (`schema.sql`, `_migrate.py`) and an **app** pool (`asm_app`, least-privilege DML)
  for request-path queries. `get_cursor()` uses admin while the app pool isn't ready
  (startup/migrations), then `main.py` calls `init_app_pool()` after `ensure_database()` so
  request-path queries run as `asm_app`. This resolves the v.119/120 deferral: ASM was the last
  addon still forced onto the superuser because its single pool ran `schema.sql` DDL that a DML-only
  role can't execute. Now DDL routes through admin, DML through `asm_app`. Reads the shared box key
  from `/share` (Core-published). Shutdown closes both pools.
- `Dockerfile` `ARG BUILD_VERSION` pinned to the version (cache-bust — the Supervisor build doesn't
  pass a build-arg, so the code layer was caching stale).

## 2026.6.120 — SEC-08/R173: ASM stays on superuser + Dockerfile cache-bust (WR-PS-081)

### Fixed
- Force a clean rebuild so the _get_app_dsn=None (superuser pool) change actually lands — ASM cache-busts on ARG BUILD_VERSION (was default `dev`), now pinned to the version. ASM boots on the superuser pool; least-priv deferred to the admin/app pool split (Phase-1b).

## 2026.6.119 — SEC-08/R173: keep ASM on superuser pool (single-pool addon) — least-priv deferred — ASM needs an admin/app pool split first (WR-PS-081)

### Fixed
- **Reverted v.117's shared-key read to keep ASM booting.** v.117 made `asm_app` authenticate, but
  ASM uses a **single DB pool** and runs `schema.sql` DDL through it (`ensure_database` →
  `get_cursor().execute(schema_sql)`) — a DML-only `asm_app` can't provision the schema
  (`permission denied for schema public`), so startup crash-looped. Restored the `/data`-key read so
  ASM falls back to the `postgres` superuser and boots. **ASM's least-priv (WR-PS-081) is deferred to
  Phase-1b: add a separate admin pool for DDL (route `schema.sql` + migrations through
  `get_cursor(admin=True)`), then read the shared key like the rest of the fleet.** Recorded in the WR.

## 2026.6.117 — SEC-08/R173: read the shared box key so asm_app authenticates (WR-PS-081)

### Security
- **`_pool.py` now reads the box DB-role key from the shared `/share/paddisense/master.key`** Core
  publishes (WR-PS-081), falling back to the local `/data` key during rollout. The per-container
  `/data` key differed from Core's, so `asm_app`'s derived password never matched the role Core minted
  → the pool **silently fell back to the `postgres` superuser** (confirmed fleet-wide via boot logs).
  Now `asm_app` authenticates → the R173 least-priv DML-only request path is genuinely in effect.
  Fernet-at-rest untouched (separate `/data` key). Superuser fallback kept as a rollout safety net;
  Phase 2 fail-closes.

## 2026.6.116 — SEC-01/04: Admin signed-licence receive-side (Hone PS-SEC-04 fleet adoption)

### Security
- **Both mutating licence paths now verify the Admin Ed25519 signature** (`asmpro/licence.py`).
  ASM-Pro trusted the `/23`/loopback transport (`_verify_internal`) alone on `/api/licence/activate`
  and `/deactivate` — the "network-location = trust" pattern Hone **PS-SEC-04** flags and
  `SIGNED_LICENCE_CONTRACT §9-A` retires. Vendored `asmpro/core/licence_verify.py` (byte-identical to
  `documentation/shared/`; new `asmpro/core/` package so the pubkey path resolves) + Admin pinned
  pubkey at `asmpro/data/admin_signing_pubkey.json` (baked by the existing `COPY asmpro/`). `activate`
  verifies via `_extract_licence` (handles the paste `code` AND Core's heartbeat `signed_licence`);
  `deactivate` verifies the signed instruction (`action ∈ {deactivate,revoke}`). Legacy-tolerant
  behind `ASM_SIGNED_LICENCE_ENFORCE` (default off). Signature — not network position — is the trust
  boundary. `cryptography==48.0.1` pinned. Tests: `tests/test_licence_signed.py` (12 pass). Closes
  ASM-Pro slice of **WR-HONE-SEC-04**.

## 2026.6.115 — UI (parts + prestart) + compliance bundle for grower release

**Grower-facing UI (bounded change set):**

- **ASM.04 Parts — new "Linked asset" filter** at the top of the parts page. Choose an asset to see only parts explicitly linked to it (via the `asset_parts` join). Empty selection = "All assets" (no change from previous default).
- **Parts card — linked-asset secondary heading** shown above the price/unit line when a part has one or more asset links. Batch-loaded in `db_parts.list_parts()` — single SQL, no N+1.
- **ASM.09 Prestart checklist — response type is now editable on existing rows.** Previously only the label cell was editable; the response-type badge was static. Click the badge cell to swap in a `<select>` populated from `checklist_response_types`; change saves immediately (Escape reverts to the badge).

**Compliance + security bundle:**

- **ADR-011 §5 startup gate CLOSED** — renamed the private `_validate_required_config()` → public `validate_config()` per FLEET_PROCESS.md §5 canonical, matching Weather/Store/Livestock shape. Startup handler still calls it first.
- **ADR-011 §6 test-isolation** — was already in the merged v.114 promote (`eee056b`), pytest now runs against the `asmpro_test` disposable database.
- **R155 CVE lift** — regenerated `requirements.lock` via `pip-compile --allow-unsafe --generate-hashes`. Same legacy-transitive pattern as Weather/Store/Livestock — 10 vulnerable packages closed. Also **bumped `opencv-python-headless` 4.10.0.84 → 4.12.0.88** (4.10 has no Python 3.12 wheel; 4.12 does, still on the 4.x line).
- **R69 hash-pin** — same regeneration produced full `--hash=sha256:...` set; satisfies R69.
- **WR-PS-080 (Hone SCAL-03) Python 3.11 → 3.12** — `Dockerfile: FROM python:3.11-slim → python:3.12-slim@sha256:423ed6ab25b1921a477529254bfeeabf5855151dc2c3141699a1bfc852199fbf` (Admin-verified multi-arch, matches Weather + Store). `pyproject.toml [tool.mypy] python_version 3.11 → 3.12`.
- **Golden Rules v2.44 → v2.47** — CLAUDE.md + docs/AUDIT.md rebased (delta: R113 ownership fan-out — ASM-Pro remains G-Claude default per Peter alignment 2026-07-02; ADR-012 trunk-based already applied at v.113 wrap; R3 substrate correction — no code impact; R195 registry expansion — ASM-Pro's registered `asm-` prefix unchanged).

### Notes

- The wider config-page S05 alignment (removing the tile pattern) was discussed with Peter and deliberately held back — the tile IA is doing real cognitive work and the row-level editability (which was the actual pain) is now covered by this ship's ASM.09 fix.
- Grower rollback: edit `PaddiSense/public/asm-pro/config.yaml` back to `2026.6.113`, redispatch build-asm-pro.

## 2026.6.114 — Grower-install unblock: startup-crash + licence-activation 403 fixes

A new grower box crashed on startup and could not be licensed.

### Fixed
- **Startup crash (Rule 88):** `db/_migrate.py` logged with `extra={... "name": ...}`. `name` is a
  reserved `LogRecord` field → `KeyError: "Attempt to overwrite 'name'"` on every data-migration log
  line, killing startup (it restart-looped until migrations were marked done). Renamed the key to
  `"migration"` on both the applied + failed branches; swept the package for other reserved keys (none).
- **Licence activation 403:** `/api/licence/activate` + `/deactivate` were token-only after the
  R141/R143 hardening — but Core forwards the licence from the Supervisor network *without* this addon's
  token (it cannot have it), so every push 403'd. Restored the proven Store pattern: accept the
  Supervisor token **or** an origin on the Supervisor `/23` (Rule 167 `ipaddress`). The signed licence
  code stays the real security boundary; the data-exposing `/api/licence/details` stays token-only.
  WR-PS-066. Guard: `TestLicenceInternalTrust`.

## 2026.6.113 — File storage moved from `/data/` to `/share/asm-pro-files/` (WR-ASM-006 close-out)

**Closes WR-ASM-006 (HIGH, P-Claude → G-Claude, 2026-06-15).** Photos and
videos previously lived under the addon-private `/data/` mount, which is
invisible to Core's centralised backup — Peter's earlier restore round-trip
turned up 49 photo refs + 3 video refs in the DB with no actual files on
disk. Per `documentation/contracts/BACKUP_CONTRACT.md` § Filesystem File
Backup, user-uploaded files now live under `/share/{addon-slug}-files/`.

### Changed

- **`asmpro/helpers.py`** — `PHOTO_DIR` and `VIDEO_DIR` derive from a new
  `FILES_DIR = $ASM_FILES_DIR` (default `/share/asm-pro-files`) with
  subdirs `photos/` and `videos/`. The old `ASM_DATA_DIR`-derived paths
  are gone from the runtime.
- **`asmpro/videos.py`** — `VIDEO_TMP_DIR` → `$FILES_DIR/video_tmp/`,
  `CHUNK_DIR` → `$FILES_DIR/video_chunks/`. Keeping the temp + chunks
  next to the final-videos dir means the transcode `shutil.move` is a
  same-filesystem rename rather than a cross-device copy.
- **`run.sh`** — exports `ASM_FILES_DIR="/share/asm-pro-files"`.
- **Startup migration** — `helpers.migrate_files_to_share()` runs once
  per boot before request acceptance: any file still under
  `/data/asm_{photos,videos,videos_tmp,video_chunks}/` is `shutil.move`'d
  to its `/share/asm-pro-files/{photos,videos,video_tmp,video_chunks}/`
  counterpart. Idempotent — empty source is a no-op; a destination collision
  keeps the destination copy and drops the legacy duplicate. Logs per-kind
  moved counts as `startup_step file_migrate`.
- **`config.yaml`** — `map: share:rw` was already present (no change),
  confirmed.

### Added

- **`tests/test_wr_asm_006_files_to_share.py`** — 7 behavioural tests
  (R192) covering: default path equals contract, env override respected,
  legacy-photos+videos relocated, idempotent on a second call, fresh
  install no-op, destination-precedence on name collision, all four
  legacy dirs covered (photos / videos / video_tmp / video_chunks).

### Why this matters operationally

`/share/` is mounted by every addon — Core can read + write it without
ASM running. Result:
1. Core's daily backup now produces `{date}-asm-pro-files.tar.gz.enc`
   automatically (auto-discovers `/share/*-files/` per contract).
2. Files survive addon uninstall (`/data/` is destroyed when the
   container is removed; `/share/` lives on the HA host volume).
3. Full backup → uninstall → reinstall → restore round-trip preserves
   photos and videos, not just DB rows.

No grower-visible change on first boot — the migration is silent unless
the log line is read. Existing dev-box uploads relocate on the first
v.113 startup; the second startup logs zeros across the board.

### CHANGELOG entries v.108–v.112 — paper-trail catch-up

Earlier ASM-Pro releases (v.108 through v.112, all 2026-06-24) were
shipped without source CHANGELOG entries; the per-addon SESSION_PICKUP
captured the work. Recording for the audit trail (R135 + R139 source-
side audit-grade narrative):

- **v.108** — Edit Asset mobile: `.mob-modal-actions` flex-row → flex-column,
  Save/Cancel/Delete vertically stacked + full-width, order Save → Cancel →
  Delete. Mobile photo upload 403 fix — `csrf.py:_check_csrf` now falls
  back to `X-CSRF-Token` header when the multipart form field is absent
  (defence-in-depth; `base.html` already auto-adds the header). Regression
  in `tests/test_red_team_coverage.py::test_csrf_multipart_accepts_header_when_form_field_absent`.
- **v.109** — `Cache-Control: no-store` on photo list endpoints so the
  desktop side sees mobile uploads instantly (was caching the empty list).
- **v.110** — Photo list JSON-serialise fix + caption field re-added in
  the GET shape + URL cache-bust on the file-bytes endpoint.
- **v.111** — Dropped v.110's "tap to re-upload" prompt; HA Companion
  WebView blocks the file picker after a 403, the prompt was a dead end.
- **v.112** — Photo bytes carry `Cache-Control: immutable` (the bytes are
  content-addressable; once a browser has a UUID-named photo, it never
  re-fetches it). Closes the 3-second image-reload Peter reported.

---

## 2026.6.112 — Photo bytes are `Cache-Control: immutable` (no re-fetch on revisit)

Peter on dev: "the image reloads every time I hit the page for about 3 sec,
can it be stored so it doesn't have to re-render?"

### Fix (`asmpro/photos.py::serve_photo`)

Photo IDs (`PHT_<8-char-hex>`) are content-addressed — the same ID always
serves the same bytes (or 404 after delete). The serve route now responds
with `Cache-Control: public, max-age=31536000, immutable`:
- `immutable` (Chrome 49+ / Firefox 49+) makes the browser skip even the
  conditional revalidate — instant render from local cache.
- `max-age=31536000` (one year) keeps it cached for a long time.
- `public` allows the corporate proxy to cache it too.

The list-of-photos endpoint (`/assets/api/{asset_id}/photos`) still carries
`Cache-Control: no-store` because it IS mutation-driven (upload adds, delete
removes); the bytes themselves don't change once a photo exists. Two-tier
caching: fresh list, immutable bytes.

verify-commit ✓ exit 0; pytest unchanged.

## 2026.6.111 — Mobile photo upload: drop the v.110 prompt (HA Companion WebView blocks it)

**v.110 hotfix.** Peter on mobile: "stopped taking image again". The v.110
`window.prompt('Caption for this photo? (optional)')` call was returning
`null` silently in HA Companion's WebView (per `feedback_mobile_ha_companion.md`
— mobile pages run inside HA Companion, not Safari/Chrome — prompts are
blocked). The v.110 `if (caption === null) { return; }` then aborted every
mobile upload without any visible error.

### Fix (`asset_detail_mobile.html` + `asset_photos_mobile.html`)

Mobile upload now sends `caption=''` straight through — no prompt. The
desktop `window.prompt()` flow stays as v.110 left it (works in regular
browsers). A future Caption-Edit feature on the photo tile is the right
surface for adding caption text on mobile.

verify-commit ✓ exit 0; pytest unchanged.

## 2026.6.110 — Photo list serialise fix + caption field + URL cache-bust + caption display

**v.109 hotfix.** I broke the photos-list endpoint with my v.109 no-store wrapper.

### Critical fix: `_photos_no_store` 500 on `datetime` column

`JSONResponse({"photos": rows})` uses Starlette's bare `json.dumps`, which
500s on Python `datetime` (the `created_at` column). Pre-v.109 the route
returned a plain dict — FastAPI's default response wraps it through
`jsonable_encoder` which handles datetimes. v.110 calls `jsonable_encoder`
explicitly before passing to `JSONResponse`. Symptom Peter saw: count tile
said "1 photo" (count comes from `/summary`, a separate endpoint) but the
image grid was empty (the list endpoint 500'd).

### Caption field on photo upload

`window.prompt()` for optional caption text before upload, on:
- `asset_photos.html` (desktop)
- `asset_photos_mobile.html` (mobile)
- `asset_detail_mobile.html` (the inline upload buttons)

Cancel aborts the upload entirely; empty string is accepted (no caption).
Caption text renders on the desktop tile as a gradient-overlay at the
bottom (2-line clamp), plain text overlay on mobile tiles.

### URL cache-bust (corporate-proxy belt-and-braces)

Per `user_corporate_environment.md` — SunRice's locked-down PCs run
aggressive proxy caching that ignores `Cache-Control`. v.110 appends
`?t=Date.now()` to every `loadPhotos()` fetch on desktop + mobile so the
proxy treats every load as a new URL. Combined with v.109's no-store
header this should be foolproof.

verify-commit ✓ exit 0; pytest unchanged.

## 2026.6.109 — Photo list `Cache-Control: no-store` (desktop sees mobile uploads instantly)

Peter on the dev box: photo taken on mobile (asset "Pump Yanmar (Recycle)" =
`AST_3bf589`, photo `PHT_3b9dd734`) showed on the mobile page but not on the
desktop photos page until a hard refresh. Confirmed via supervisor logs that
the upload itself was fine (POST 200, file on disk, asm_photos row written,
GET /api/photos/PHT_3b9dd734 returns 200) — the desktop's `loadPhotos()`
fetch was just being served from the browser cache.

### Fix (`asmpro/photos.py`)

`/assets/api/{asset_id}/photos` and `/issues/api/{issue_id}/photos` now wrap
their JSON response in a `Cache-Control: no-store` header via the new
`_photos_no_store()` helper. Photo lists are mutation-driven (added by upload,
removed by delete) so HTTP caches add zero value; no-store forces every page
load to re-fetch.

verify-commit ✓ exit 0; pytest 166 + 1 xfail (unchanged — photos endpoint
behaviour proven by existing CSRF multipart regression at v.108).

## 2026.6.108 — Edit Asset mobile button stack + mobile photo upload 403 fix

Two real bugs Peter hit on mobile after the v.107 grower release.

### Edit Asset mobile — Delete/Cancel/Save now vertically stacked

`.mob-modal-actions` was `flex-direction: row` with `flex: 1` siblings — on
narrower phone screens the Delete/Cancel/Save labels wrapped inside their
buttons. Switched to `flex-direction: column` so each button is full-width
on its own row. Button order reordered to put primary action first:
Save → Cancel → Delete (destructive action at the bottom, farthest from
the thumb).

### Mobile photo upload — 403 closed (CSRF multipart header path)

`uploadPhoto()` / `uploadPhotoFromCamera()` build a `FormData` with `file` +
`caption` but no `_csrf` form field. The base.html `window.fetch` wrapper
auto-adds the `X-CSRF-Token` header, but the CSRF middleware was only
checking the form field for `multipart/form-data` and ignoring the header
— so every mobile photo upload returned 403 with no diagnosis. v.108 fix
in `csrf.py:_check_csrf`: for multipart, fall back to the header if the
form field is empty. Defence-in-depth pattern.

Regression test:
`tests/test_red_team_coverage.py::test_csrf_multipart_accepts_header_when_form_field_absent`
sends a multipart POST to `/api/users` with only the X-CSRF-Token header
(no form field) and asserts the request doesn't 403. Pre-fix would have
been 403; post-fix runs through to normal validation.

verify-commit ✓ exit 0; pytest 166 + 1 xfail.

## 2026.6.107 — All active users in every People-list dropdown

**Peter ruling 2026-06-24:** "actually allow all users in all people list" —
office-job admin / coordinator / viewer users may legitimately resolve an
issue, get assigned to one, or own a service event. The `_ASSIGNABLE_ROLES`
hardcoded role filter is gone from every template; the only exclusion is
`u.active === false` (deactivated users still don't show).

### Templates updated

- `templates/issues.html` — assign drawer + resolve drawer
- `templates/issues_mobile.html` — assign overlay + resolve overlay
- `templates/services.html` — technician picker (`_usersCache`)
- `templates/services_edit_mobile.html` — technician picker (edit flow)
- `templates/services_new_mobile.html` — technician picker (new flow)

Five `var _ASSIGNABLE_ROLES = ['contractor', 'coordinator', 'manager'];`
declarations removed. Replaced with a `2026-06-24 — Peter ruling` comment
documenting the policy + the `u.active !== false` filter.

verify-commit ✓ exit 0. pytest unchanged.

## 2026.6.106 — Resolved By → People-list dropdown + wider test-cleanup regex

Two dev-test-driven UI/data fixes Peter surfaced during v.105 dev review.

### Resolve Issue: `Resolved By` now sources from the People list

Both desktop (`templates/issues.html`) and mobile (`templates/issues_mobile.html`)
resolve drawer/overlay replaced the free-text `<input>` with a `<select>` populated
from `_assignablePeople` (loaded at page init via `/api/users`, filtered to
`contractor / coordinator / manager` roles via `_assigneeOptions(selected)`).
Same helper the assign drawer uses — single code path. Pre-selects the issue's
current `assigned_to` value when present. Stops typo-driven free-text leaks
into the `service_events.technician` column.

### Wider test-pattern cleanup regex (`tests/conftest.py`)

The v.105 cleanup regex was too narrow — `test_videos_category.py` and
`test_v26_features.py` create assets like `TEST_VIDCAT_DB`, `TEST_RULE69`,
`TEST_R49_SVC_CRUD_ASSET`; the R153/R154 agent left `_dbg*` debug users +
`DBG3 bdb861`-style asset/location names; the sweep test seeded auto-derived
`A bdb861`-style asset names; and the `j.smith` / `c.toyota` auto-derived
fixtures persisted across runs. Pattern now matches:

- `^R15[34] Asset `, `^sweep asset `, `^hijacked_by_other_loc_supervisor$`,
  `^TEST_`, `^DBG\d* `, `^D\d+ [a-f0-9]+$`, `^A [a-f0-9]+$`, `^h$` (assets)
- `^R15[34] Loc `, `^sweep loc`, `^TEST_`, `^DBG`, `^D\d+ [a-f0-9]+$` (locations)
- `^_r15`, `^_sweep`, `^_test_`, `^_dbg`, `^TEST_`, and all `_r1{rule}_` prefixes (users)

### Dev DB cleaned retroactively (this commit)

Wiped 762 `TEST_*`/`DBG*`/`A {hex}`/`h` assets, 6 `_dbg*` users, 222 test
locations, and the 2 `j.smith` / `c.toyota` auto-derived test users. The
final dashboard state: 94 real assets, 5 real locations, 1 real user (admin).

verify-commit ✓; pytest unchanged.

## 2026.6.105 — test-pattern row auto-cleanup (dev-DB hygiene)

Peter saw dozens of `R153 Asset…`, `sweep asset…`, `hijacked_by_other_loc_supervisor`,
and `_r153_*`/`_sweep_*` users polluting the live dev dashboard — the RT-coverage
test pack created fixtures without a cleanup teardown, and pre-v.102 R153 test runs
left "hijacked" assets behind (the test attempted a cross-location PUT; when the
addon let it through, the asset name persisted as evidence).

### Fix (`tests/conftest.py`)

New session-scope autouse fixture `_cleanup_test_rows_at_session_end` wipes
rows matching strict test-name patterns at the END of every pytest session:

- `assets` — name matches `^(R15[34] Asset|sweep asset|hijacked_by_other_loc_supervisor)`
- `locations` — name matches `^(R15[34] Loc|sweep loc)`
- `asm_users` — username matches `^(_r15|_sweep|_r17|_csrf|_r158|_r19|_test|_r188|_r171|_r190)`
- plus `j.smith[0-9]+` autoderived users with display_name 'Jane Smith'
- FK-referencing rows (`prestart_inspections`, `service_events`, `asm_issues`,
  `asm_photos`, `asm_asset_videos`) deleted FIRST, then `assets`, then
  `asm_user_locations` + `asm_users`, then `locations`.

Whitelist-driven so a real grower row with a non-test name can't be culled by the
fixture. Wrapped in try/except so cleanup never breaks the test run.

### Dev-DB cleanup performed

Wiped retroactively from the live dev DB before adding the fixture:
- 57 test-pattern assets, 168 test-pattern locations, 604 test-pattern users
- 27 `hijacked_by_other_loc_supervisor` assets (pre-v.102 R153 test artifacts)
- 4 prestart_inspections, 4 service_events, 4 asm_issues, 4 asm_photos,
  4 asm_asset_videos referencing the deleted assets
- 35 `j.smith[N]` auto-derived test users

Dashboard now shows only legitimate fixture data.

verify-commit asmpro exits 0; pytest 165 + 1 xfail (test count and result unchanged).

## 2026.6.104 — 31-case R153/R154 sweep test (regression lock)

Captures the new integration test `test_r153_r154_sweep_object_scoped_routes_deny_cross_location`
that sweeps 31 (method, path, body, foreign-marker) tuples across 9 surfaces
(assets, issues, services, prestarts, locations, photos, videos, users, reports, plus
LIST filters with `?location_id=B`). The test was authored by the R153/R154 campaign
agent and confirms — for every object-scoped route in the addon — that a contractor
homed at location A is REFUSED (4xx) when probing location B's objects, or returns
200 with no foreign-tenant id in the body. Locks the v.102/v.103 source-side scoping
fixes against future regressions.

No runtime behaviour change — test-only. v.103's coverage (67 scoping call sites
across 10 files) stays as the live runtime contract.

verify-commit ✓ exit 0; pytest 165 + 1 xfail.

## 2026.6.103 — R60 split on `api_create_user` + `api_update_user`

Post-v.102 wrap-time R60 gate caught two routes pushed over 50 lines by the
R153/R154 location-scoping additions:
- `users.py:api_update_user` 54L → 27L coordinator + new `_persist_user_update`
  helper (29L). DB write + R188 session-revoke + audit moved into the helper.
- `users.py:api_create_user` 52L → 23L coordinator + new `_validate_create_user_body`
  helper (27L). R153 + role + display_name + password + username + home-location
  validations bundled.

verify-commit asmpro exits 0; pytest unchanged (164 + 1 xfail).

## 2026.6.102 — Grower-release standard: R153/R154 + CSRF body-drain + R158

Closes the 4 documented xfails carried in v.101 and brings ASM-Pro to
grower-release standard (R105 release-gate CLEAN; only R171 alert-transport
remains xfail as an accepted known limitation — ASM is standalone, no
out-of-band channel).

### Security closures

- **R153 / R154 (cross-location IDOR — real defect)** — new helper
  `auth.check_location_access(actor, object_location_id) -> bool` applied
  to **17 object-scoped routes** across `assets.py`, `issues.py`,
  `services.py`, `prestarts.py`:
  - LIST endpoints with `?location_id=` filter: silently restrict to the
    caller's `home_location_id` when out of scope (no 404 — list endpoints
    are inherently enumerable).
  - GET / PUT / PATCH / DELETE on object id: **404** (not 403) on
    cross-location access — per R154, returning 404 prevents existence
    enumeration via status-code difference.
  - CREATE: **403** when the body's `location_id` is out of scope.
- **CSRF form-body drain (latent bug surfaced v.101)** — middleware
  `_check_csrf` now buffers the body and installs a fresh `receive()`
  channel so the downstream handler's `await request.form()` re-parses
  the same bytes. Previously every audit_log row from a form-encoded
  POST landed with `username=""` (the middleware drained the stream).
  Helper `_read_form_token_and_buffer` extracted to keep `_check_csrf`
  under R60's 50-line bound. Regression test
  `test_csrf_middleware_does_not_drain_form_body` pins the invariant.
- **R158 body-size cap (1 MB)** — new `BodySizeLimitMiddleware`
  registered before CSRF. Returns **413** for any
  POST/PUT/PATCH/DELETE whose `Content-Length` exceeds 1 MB on JSON or
  form content-type. Upload routes (`multipart/form-data`,
  `application/octet-stream`) are exempt by content-type — they have
  their own larger per-route caps. Behavioural test in
  `test_red_team_coverage.py::test_r158_body_size_floor_on_json_mutations`.

### Verification

- pytest: **164 passed, 1 xfailed** (R171 alert transport — known
  limitation, ASM is standalone).
- ruff / mypy / bandit / verify-commit all green; gate exits 0.

## 2026.6.101 — Phase-3 RT-coverage punch-list (WR-PS-057 T9 close)

Closes the 10 missing red-team coverage tests carried in the v.100 pickup. 14 new
tests landed: 10 passing + 4 documented xfails for real gaps that fold into the
fleet's per-route IDOR / detect-alert campaigns (not this addon's session-scale work).

### Tests added (`tests/test_red_team_coverage.py`)

- **R146** ✓ no CSV/spreadsheet export surface — guard test asserts no `text/csv`
  route, no `csv`/`openpyxl`/`xlsxwriter` import in source.
- **R153** ⚠ xfail (real defect documented) — object-scoped routes don't enforce
  `home_location_id` against caller-supplied `location_id` query params. Fleet-wide
  per-route scoping campaign.
- **R154** ⚠ xfail (real defect documented) — cross-location GET leaks foreign-
  location objects. Pairs with R153 fix.
- **R158** ✓ login rate-limit floor verified; ⚠ xfail body-size floor — no enforced
  body cap today.
- **R159** ✓ no user-controlled outbound HTTP in source (only the hardcoded
  `http://supervisor/...` channel in `supervisor_client.py`).
- **R171** ✓ failed-login writes `audit_log` row (detection floor); ⚠ xfail alert-
  transport — no out-of-band channel today (ASM is standalone).
- **R187** ✓ no XFF derivation in source; ✓ login rate-limit not bypassable via
  X-Forwarded-For (rate limit is username-keyed, not IP-keyed).
- **R188** ✓ credential change revokes all sessions for the user. NEW source helper
  `auth.destroy_sessions_for_user(user_id)` called from `api_update_user` when
  `password_hash` is in updates. Real defect closed in this version.
- **R189** ✓ no email-send surface — guard test asserts no `smtplib`/`resend`/
  `sendgrid`/`mailgun`/`postmark` import in source.
- **R190** ✓ login error byte-identical for "no user" vs "wrong password" failure
  modes (LEAK_PATTERNS regex pinned).

### Changed

- `asmpro/auth.py` — `destroy_sessions_for_user(user_id)` added (R188).
- `asmpro/users.py` — `api_update_user` calls `destroy_sessions_for_user` in the
  same transaction as a `password_hash` update; audit details now include
  `sessions_revoked` count.

### Verification

- pytest: **160 passed, 4 xfailed** (4 documented gaps; R178 nonce-CSP, R157 CSRF,
  R155 dep audit, R167 IP-range, R98 baseline all still ✓).
- ruff + mypy + bandit + verify-commit all green.

## 2026.6.100 — Add Asset modal → full parity with Edit Asset modal

### Changed
- `assets.html` Add-Asset modal rebuilt to mirror the Edit-Asset modal
  on `asset_detail.html`. Now carries every field at the same depth:
  - **Cascading Site → Location → Area** (was a flat single-level
    Location dropdown). Disabled-until-parent-chosen semantics; deepest
    selected level is what gets saved to `location_id`.
  - **Attributes** key/value manager with `+ Add` and per-row remove
    (was missing entirely).
  - **Prestart Required** as a Yes/No `<select>` (was a checkbox —
    edit was a select; now matches).
  - Same `.modal-box` / `.modal-title` / `.modal-actions` shell as
    Edit so the visual depth matches.
- Removed the `prestart_cadence` field from Add. The Edit modal
  doesn't carry it (cadence is config-level per `prestart_cadences`),
  so Add was sending a per-asset value the Edit form silently ignored.
  Now both call the same shape: `name + category + prestart_required
  + meter_type + service_interval + location_id + attributes`.

### Why
Peter — "the new asset form is only a partial modal, it need to be
the same as the edit asset form. full rich form." Closing the depth
gap between the create and edit surfaces so operators see the same
fields in the same place regardless of whether they're adding or
modifying an asset.

### Out of scope (queued)
- Consolidating the duplicated `.modal-*` / `.attr-*` styles into
  master / app.css — both files now carry them. Folds into the
  WR-PS-054 Config-pattern + WR-PS-051 app.css empty-out sweep.
- Extracting the rich-asset-form into a shared Jinja partial so a
  third surface (mobile new) automatically inherits — out of scope
  for this fix.

## 2026.6.99 — Close-all-gaps pass: R193.3 master-class redefine + R124 supervisor adapter

### Fixed
- **R17 theme**: re-synced `asmpro/static/paddisense-tokens.css` to the
  master (WR-PS-054 utility additions: `.u-link-primary`, `.u-inline-form`,
  `.u-pt16`, `.u-mw500`, `.u-ls4`, `.u-wNN` column family). Now
  byte-identical to `documentation/theme/paddisense-tokens.css`.
- **R193.3** (new v2.36 `check-app-css.py` gate): removed
  `asmpro/static/app.css:78` `.u-btn-block-success:hover` redefinition.
  The :hover values it set (`color: var(--ps-btn-text)`;
  `text-decoration: none`) were already the base-class defaults —
  visual no-op that only existed to trip the gate. Master keeps
  the canonical button; app.css stays addon-extensions-only.
- **R124** supervisor adapter consolidation: `pat_manager.py` rewired
  `_update_store_repos` to go through `supervisor_client.add_or_update_store_repository`
  + `supervisor_client.reload_store` instead of inline `httpx.post()`
  calls. Single supervisor blast-radius restored — was 2 inline +
  the adapter (3 sites total). The orphan `_reload_store` helper
  in `pat_manager.py` retired in the same move.

### Documented (gate quality, not addon defects)
- **R51 window.open**: zero real calls in `asmpro/` source. The
  verify-commit ⚠ comes from a comment in
  `static/paddisense-tokens.css:1655` (master) describing what the
  print-iframe utility class *replaces*. Fleet-wide false-positive
  for verify-commit to filter CSS comments.
- **R91 connection pool safety**: zero unsafe pool calls. The two
  hits are the `"get_conn"` / `"get_cursor"` strings in
  `db/__init__.py:__all__` — same WR-PS-047 class (grep-finds-string,
  not behaviour).

Both noted in the wrap for the verify-commit steward; not blockers.

### Wrap
- `CLAUDE.md` + `docs/AUDIT.md` re-baselined to v2026.6.99 +
  `golden_rules_version: 2.36` + `last_audit_date: 2026-06-23`.
- `docs/SESSION_PICKUP.md` extended with the v.97→v.99 arc.

## 2026.6.98 — Assignee fields source from the People list (no more free-text typos)

### Changed
- Maintenance Requests + Services: every assignee / technician input
  is now a **dropdown** populated from the People list, filtered to the
  three operating roles (Contractor / Co-ordinator / Manager —
  Administrator is excluded as a privilege role). Free-text entry
  removed; typo-driven duplicate "Bob" / "bob" / "Bob Smith" assignees
  can no longer happen.
- Pages converted:
  - `issues.html` desktop — create modal "Assign To", drawer inline
    "change" edit, Schedule form "Assign To", and the issue-list
    "All assigned" filter.
  - `issues_mobile.html` — mobile assign overlay.
  - `services_new_mobile.html` — mobile create Technician.
  - `services_edit_mobile.html` — mobile edit Technician (with legacy
    fallback for existing rows whose technician name isn't on the list).
  - `services.html` desktop — same role filter + legacy fallback in the
    create/edit modal.
- The Assigned filter on the issues list page now shows the WHOLE
  People list (with per-name counts), plus a "(legacy)" entry for any
  still-active free-text name from before this change, so existing
  data stays filterable until the FK refactor lands.
- Page-load fetches `/api/users` once; the list is cached for every
  picker on the page.

### Stale value handling
- When opening the drawer or edit form for an issue / service that
  currently has a free-text assignee not on the People list, the
  current value is surfaced as `Name (not on People list)` so the
  dropdown doesn't silently switch the record to Unassigned. The
  user must explicitly pick a real person or Unassigned.

### Out of scope (TODO B follow-up)
- The schema column stays TEXT for now. The paired `*_user_id INT NULL
  REFERENCES asm_users(id)` FK column + the fuzzy-match-and-backfill
  migration are queued as a separate batch (a real reference is what
  lets reports group by Person properly; the dropdown is the
  user-visible half of the same fix).

## 2026.6.97 — Issue drawer Assign button: CSS-class / inline-style toggle bug

### Fixed
- `issues.html` (desktop) issue-drawer **Assign** footer button was a
  no-op. The inline-edit row `#issAssignEdit` is hidden by a CSS class
  `.s-3a1c0f4 { display: none; }`, while `toggleAssignEdit()` toggled
  via `el.style.display === 'none' ? '' : 'none'`. First click painted
  `style.display = 'none'` (no visible change, the class already hid
  it); second click set `style.display = ''` (inline removed, class
  STILL hid it). The edit row was permanently unreachable. The
  inline-text "change" button beside the Assigned label hit the same
  function, so both entry points were dead. Fix: read computed style
  as the source of truth and set an explicit `'block'` to override
  the class. Mobile (`issues_mobile.html`) was not affected — it uses
  a `.classList.toggle('open')` overlay pattern, not inline-style.

### Internal (carried over from v.96 main but never grower-shipped)
- mypy fix on `_video_row_to_dict` row typing and the user-create helpers
  (`str | JSONResponse` Result|Error pattern for `_resolve_create_password`
  / `_resolve_create_username` / `_parse_create_home_location`). The
  public-repo CI gate caught the previous `tuple[X | None, ...]` shape;
  this version is the first to ship with the tighter annotations.

## 2026.6.96 — Asset videos: `category` enum (`prestart` / `instruction`) — mobile + tests + datetime-serialisation fix

### Added
- `asm_asset_videos.category` enum column (`prestart` | `instruction`),
  `NOT NULL DEFAULT 'prestart'` + CHECK constraint + composite
  `(asset_id, category)` index. Schema + idempotent `_migrate.py`
  block. Existing rows fall into `prestart` so the legacy "every video
  appears in the wizard banner" behaviour is preserved.
- `videos.py`: `VIDEO_CATEGORIES` tuple + `_normalise_category()` coercion.
  `POST /assets/api/{id}/videos` + chunked `/finalize` accept a
  `category` field (form / JSON). `GET /assets/api/{id}/videos` accepts
  `?category=` filter; unknown values silently fall back to "no filter"
  to keep legacy clients robust. New `PUT /api/videos/{id}` edits title
  and/or category (technician+ gate, audited, DB CHECK is the real
  enum gate).
- `asset_videos.html` (desktop, v.96 WIP) + `asset_videos_mobile.html`
  (new this version): category select on upload row, per-card badge
  (Prestart `ps-badge-blue` / Instruction `ps-badge-grey`), edit
  pencil opens an inline title + category + delete + save row, all
  delegated through a single `#videoList` click listener so
  re-renders never unbind.
- `prestarts.html` + `prestarts_mobile.html` wizard step-1 banner
  fetches with `?category=prestart` (Instruction videos never reach
  the wizard).
- `tests/test_videos_category.py` — 8 new tests: schema default,
  `?category=` filter, unknown category fallback, `PUT` updates
  title + category, `PUT` rejects invalid category at API layer (400)
  AND at DB CHECK layer (psycopg2.errors.CheckViolation), legacy NULL
  category excluded from `?category=instruction` filter (Rule 66 / 67).

### Fixed
- `list_asset_videos` returned rows with a `datetime` `created_at` that
  `JSONResponse` (stdlib `json.dumps`) cannot serialize — silent 500 on
  any asset with at least one video. Latent in v.95; exposed by the new
  category tests that seed real rows. Converted via a `_video_row_to_dict`
  helper that ISO-formats `created_at` before serialisation. Regression
  test pinned in the new `test_videos_category.py` filter cases.

### Red-team
- Schema change is additive; `NOT NULL DEFAULT` keeps existing rows valid.
- `PUT /api/videos/{id}` is technician+ gated and writes through `audit()`.
- API-layer enum check + DB CHECK constraint — defence-in-depth so a
  future bug skipping API validation still fails at the DB.
- `_normalise_category()` deliberately silent on unknown input
  (`prestart` fallback) because the DB CHECK is the real gate; an upload
  POST never reaches the DB with garbage.

## 2026.6.95 — Prestart mobile photo capture: v.85 regex casualty (`multipleclass=`)

### Fixed
- Mobile prestart wizard step 3 rendered the photo-add input as
  `<input ... multipleclass="js-photo-add">` — the v.85 attribute-spacing
  regex bug missed this instance (no `"` before `multiple`, so the
  earlier `"class="` heuristic didn't trigger). The element parsed with
  no `class` attribute, so the delegated `.js-photo-add` listener never
  fired. Photo capture button visible but completely dead. Space added.

### Verified (no change needed)
- **Asset photos & videos** (the "re-add upload" ask): already wired and
  working on the dedicated `/assets/{id}/photos` and `/assets/{id}/videos`
  sub-pages (desktop + mobile variants). Endpoints `/assets/api/{id}/photos`,
  `/videos`, `/videos/chunk`, `/videos/finalize`, `/api/photos/{id}`,
  `/api/videos/{id}` all reachable; smoke-tested HTTP 200 + JSON.
- **Prestart photo (desktop)**: working — multi-image capture in step 3
  buffered client-side and uploaded to the auto-created issue on submit.

### Out of scope
- **Prestart video upload**: never part of the original design (prestart
  videos are inline instructional banners via `.js-play-video`, not
  user-captured). Not a re-add — would be a new feature; queued as a
  product decision rather than added blindly.

## 2026.6.94 — asset_detail_mobile silent crashes: 7 dead inline lists + dead toast

### Fixed (asset_detail_mobile.html)
- Page is a nav-grid hub (each tile routes to a dedicated sub-page) but
  carries 7 legacy `load*()` functions from an earlier inline-tabbed
  layout. Each fires on DOMContentLoaded, sets a `count*` badge (works),
  then attempts to populate `#servicesList` / `#prestartsList` /
  `#issuesList` / `#partsList` / `#photoGrid` / `#videoList` /
  `#reportContent` — none of which exist post-refactor — and crashes
  silently. The counts had been working, hiding the breakage.
  Null-guards added so each function no-ops gracefully once the count
  is set. `loadReport()` early-returns before two pointless API calls
  if its target container is gone.
- `showToast()` referenced `#toastEl` which was removed during the
  refactor; 20+ call sites (photo/video upload, asset save, delete
  flows) silently crashed instead of surfacing the error message.
  Falls back to `console.info('[asm-toast]', msg)` when the element
  is absent until a proper per-render toast factory lands.

### Notes
- Dead `uploadVideo()` / `capturePhoto()` / chunk helpers remain — their
  `#videoFileInput` / `#photoFileInput` markup also disappeared in the
  refactor, so they're unreachable rather than broken. Cleanup queued
  for v.95 batch (delete the helpers or re-add the upload UI; product
  decision needed).
- Class extension to KDP-013 ("dead inline render after layout refactor"
  is a new sub-class) is being filed to documentation; pairs with
  WR-PS-053's AST gate.

## 2026.6.93 — Config ASM.09 People filter dropdown stale + canonical-aware match

### Fixed
- People filter dropdown still listed the legacy 5 roles
  (`admin/manager/supervisor/technician/viewer`) instead of the
  v.91 canonical 4 (`administrator/manager/coordinator/contractor`) —
  missed during the role rework. Updated.
- Filter logic was `u.role === _peopleFilter` (exact string match),
  which would have hidden every legacy row from a canonical-named
  filter. Now canonicalises both sides via `_canonRole(u.role)` so
  a row with role `admin` matches the `administrator` bucket, etc.
- Header relabelled "Users" → "People" + "+ Add User" → "+ Add Person"
  to match the v.91 modal rename (People are not all log-in users).
- Subtitle copy updated to describe the new 4 roles (only Manager
  authenticates via PIN; others via HA ingress / assignment-only).

## 2026.6.92 — Config ASM.09 sublist picker: selector matched stale local class

### Fixed
- `pickSubList(tile, key)` queried `.sublist-wrap[data-tile="…"]` but every
  sub-list `<div>` in the markup carries the master canonical
  `.ps-sublist-wrap` (renamed during the WR-PS-050 alignment sweep).
  `querySelectorAll` matched zero elements, no element ever toggled
  visibility, every Asset/Parts/Issues/Services/Prestart/Locations picker
  silently stuck on Categories. Selector now uses `.ps-sublist-wrap`.

### Notes
- This is the THIRD class of post-sweep regression in 48 hours
  (R178 orphan bindings + R178 undefined helpers + WR-PS-050 stale
  selectors). KDP-013 covers the R178 family; a Class E (stale JS
  class selector) extension and a fleet-wide comprehensive sweep are
  filed under WR-PS-053 (verify-commit AST gate). Full audit running
  this session to roll into v.93 batch.

## 2026.6.91 — People modal overhaul + ASM.05 prestarts orphan-binding recovery

### Fixed (ASM.06 Maintenance Requests — drawer)
- Detail-drawer footer's 11 `.js-drawer-action[data-action="…"]` buttons
  (Resolve / Assign / ConductWork / Schedule / Ignore / Update / Close /
  Reopen / Delete / SaveUpdate / SubmitIgnore) were all unwired — the
  delegated handler only matched specific `js-drawer-*` classes and
  ignored the generic data-action pattern. Detail drawer was effectively
  dead. Dispatcher now uses a `DRAWER_ACTIONS = {verb: fn, …}` map.
- `.js-toggle-assign-edit` ("change" link) and `.js-save-assign` (Save
  button) inside the assignment row had no listener; assignment changes
  could not be saved. Wired in the drawer-body delegated handler.

### Fixed (ASM.05 Prestarts)
- Start Prestart button (`#btnStartPrestart`) was orphaned by the R178
  inline-handler sweep — no listener, button did nothing. Wired to
  `openPrestartDrawer`.
- Drawer close × (`#drawerCloseBtn`) — same class of orphan; wired to
  `cancelPrestart`.
- Status filter chips (All / Passed / Failed / Open Issues) and the
  Asset + Type filter selects had no change listener; delegated click on
  `#prestartFilterChips` + `change` listeners on `#prestartAssetFilter`
  and `#prestartCatFilter`.
- Card grid `.js-delete-prestart` and `.js-open-service` had no
  binding; delegated click on `#prestartCards`.
- Step-1 wizard "Cancel" / "Next" buttons used `data-action="..."`
  while the drawer-footer delegated handler only checked `js-pre-*`
  classes — Next was dead. Dispatcher extended to read `data-action`
  first (handling `cancel-prestart` + `step1-next`).
- `_wireStep1Inputs()` was *called* but never *defined* — the QR scan
  input, category filter, asset typeahead text, asset-list selection,
  and operator name field had no listeners. Defined the helper.
- Wizard video preview buttons (`.js-play-video`) had no binding;
  added to the existing `#drawerBody` delegated click handler.

### Changed (People modal)
- Role model: `viewer/technician/supervisor/manager/admin` collapsed to the four
  Peter-canonical roles **Contractor / Co-ordinator / Manager / Administrator**.
  Old slugs stay as backward-compat aliases in `ROLE_ORDER` (`admin → administrator`,
  `supervisor → coordinator`, `technician → contractor`) so existing DB rows
  authorise normally; new writes use the canonical slug.
- People modal (`config.html`): drops the Username field — derived server-side
  from Display Name (`Jane Smith → j.smith`, uniqueness suffix on clash).
  PIN field is hidden unless Role = **Manager** — the only role that
  authenticates via username + PIN. The other three roles exist as references
  (assigned to services / requests) and authenticate via HA ingress trust.
- Password floor for Manager dropped from 8 chars to 4 (it's a PIN, not a
  password). Other roles get a random unguessable hash so password-login
  can never succeed for them.
- Demotion from Manager → non-PIN role wipes the active PIN; promotion to
  Manager requires a PIN in the same request (`PIN required when promoting`).
- 16 templates: role-gate predicates extended to accept both old and new
  slugs so existing pages (assets/parts/services/locations/issues, mobile
  variants, base sidebar) keep working through the migration.
- `ensure_first_user()` seeds the bootstrap admin with role `administrator`
  (canonical) instead of `admin`.

### Tests
- `test_users_crud.py` updated for the new PIN semantics:
  short-PIN-rejected test now uses role=manager; new test confirms
  non-Manager create succeeds without a password and the username is
  auto-derived to `j.smith`.

### Notes
- Held for batch deploy per the page-by-page review directive — committed
  but not pushed to the dev box. Resume with `tools/deploy.sh` when the
  batch is approved.
- v.74→v.90 CHANGELOG backfill remains an open audit gap (Rule 84/135)
  from earlier sessions; not addressed in this entry.

## 2026.6.73 — run.sh canonical theme-source (WR-PS-045) + SESSION_PICKUP (R191) + theme re-sync

Fleet standardization pass. `run.sh` now copies the canonical master theme
(`/config/documentation/theme/paddisense-tokens.css`, WR-PS-045/ADR-007) into
the addon's static dir at startup; theme re-synced byte-identical to master.
Added `asm-pro/docs/SESSION_PICKUP.md` (Rule 191 durable in-repo pickup) with
the full verify-commit audit backlog. Synced stale CLAUDE.md version
(2026.6.57 → 2026.6.73) and added the Golden Rules version field (Rule 118).
No code/behaviour change; pre-existing audit debt is recorded, not fixed.

## 2026.6.70 — Adversarial audit: 5 critical security findings closed (R141 + R143 + R144 + R88 + R147)

Red-team walk against Golden Rules v2.6 (new Section 13 + 14) surfaced
5 critical findings — 4 in `licence.py`, 1 system-wide. All closed at
root cause per the new R150. The walk also discovered new Rules 149-152
(promoted from preamble) which are now committed to the docs repo;
this release applies them retroactively to my own v.69 work.

### Smoke checklist (R85)
- [ ] `/health` returns 200 with `db_ok=true`
- [ ] Addon state=started within 180s
- [ ] `GET /api/licence` returns ONLY `{"enrolled": bool}` — no licence string, no grower_id, no product, no exp
- [ ] `GET /api/licence/details` without bearer token returns 403
- [ ] An intentionally-triggered 500 returns `{"error":"Internal error","request_id":"..."}` — no SQL/path/stack
- [ ] Login screen + dashboard render
- [ ] Edit a part / asset → save → reload
- [ ] Restart loses no state

### CLOSURES (all root-cause per R150)

**R144 — `/api/licence` reduced to liveness-only**
The endpoint was auth-exempt and returned the full licence string, grower_id,
product, and expiration to anyone on the network. That's the exact pattern
R144 forbids: unauthenticated endpoints expose only up/down liveness, never
operational telemetry. The licence string is effectively the API key for
Core integration; leaking it unauthenticated is leaking the credential.

Fix: `GET /api/licence` now returns `{"enrolled": <bool>}` only. A new
`GET /api/licence/details` exposes the full detail behind Supervisor
bearer token auth (see R141/R143 below).

**R141 + R143 — `_verify_internal` replaced with constant-time supervisor check**
The previous gate accepted requests in two ways:
1. `Authorization: Bearer <SUPERVISOR_TOKEN>` compared with `==` (timing
   side-channel — R143 violation; leaks token byte-by-byte).
2. ANY client whose `request.client.host` started with `172.30.` — every
   HA addon on the same host shares that subnet, so this fail-opens to
   arbitrary addons (R141 violation: "Authorisation derives from a verified
   secret, not from who the request says it is").

Fix: new `_verify_supervisor()` requires the Supervisor bearer token,
compared with `hmac.compare_digest` (constant-time). IP-range fallback
removed entirely. Applies to: `/api/licence/details` (new),
`/api/licence/activate`, `/api/licence/deactivate`.

**R88 — licence value no longer logged in plaintext**
`log.info("licence_activated", extra={"licence_code": …})` wrote the full
licence value to logs on every activation — credential-in-logs (R88).
Fix: new `_redact_licence()` helper emits a 4-char prefix + ellipsis
(`"abcd…"`) for diagnostics without leaking the secret. Extra key
renamed `licence_code` → `licence_prefix` to make the redaction
explicit. POST `/api/licence/activate` response also no longer echoes
the licence value back.

**R147 — global exception handler + 10 raw `str(e)` returns reverted**
10 callsites returned exception text directly to clients (`str(e)` or
`f"…: {e}"`) — leaking SQL errors, OSError messages, file paths, and
in some cases internal `psycopg2`/Supervisor error bodies. No global
500 handler existed so any new route could leak by omission.

Fix: new `@app.exception_handler(Exception)` in main.py logs the full
exception (with traceback) server-side and returns
`{"error":"Internal error","request_id":"<hex12>"}` to the client.
The request_id lets a user quote it when reporting an issue and
operators correlate the masked client response with the full server
log entry. All 10 route-level callsites also reverted to generic
`"Internal error"` + per-route `log.exception` — belt-and-braces so
the per-route log event name stays specific for filtering. Sites:
`parts.py:257`, `locations.py:147` (v.69 self-finding),
`notifications.py:58`, `videos.py:214/262/291/355/429/458/486`.

**R65 self-finding — confirmed dead-code suppression already gone**
v.69's `type: ignore[import-untyped]` on the `import requests as httpx`
fallback was R150 suppression-not-fix. Audit confirms the fallback was
removed by the v.69 supervisor-adapter refactor — no dead code remains
in source. Self-finding resolved as side-effect of the larger fix.

### NOT closed (documented dispensation)

**R141 — `is_ingress()` IP-range trust** kept as ⚠ HA platform-model
dispensation. HA Supervisor's docker network is NOT externally
routable; the addon's uvicorn directly accepts the TCP from supervisor
so `request.client.host` is the actual TCP peer (not a forwarded
header). X-Ingress-Path header ALONE does not grant trust — both
signals must agree (header present AND client IP in 172.30.32.0/23).
This is the established HA addon trust boundary used by every
PaddiSense addon. Re-evaluate if the platform model changes.

### Files changed

- `asmpro/licence.py` — `/api/licence` liveness-only; new
  `/api/licence/details`; new `_verify_supervisor` + `_redact_licence`;
  full module docstring updated
- `asmpro/main.py` — `@app.exception_handler(Exception)` global handler
  with request_id correlation
- `asmpro/parts.py`, `asmpro/notifications.py`, `asmpro/locations.py`,
  `asmpro/videos.py` (7 sites) — raw `str(e)` returns reverted to
  generic "Internal error" + per-route `log.exception`
- `config.yaml` + `asmpro/__init__.py` — version bump
- `CHANGELOG.md` — this entry

### Process notes (R140, R149, R151)

This release applied R140 (adversarial review) to my own v.69 work —
the v.69 "audit phase 1" headline was honest but the closures had
gaps: R65 was suppression; R147 was technically closed by replacing
old `str(e)` but I ADDED a new one for diagnostic purposes (R150
violation); the v.69 walk didn't include section 13 because the rules
update hadn't landed yet.

The lesson is exactly what new R140 codifies: a change nobody attacked
has not been reviewed. The senior-maintainer lens (R149) shipped me
"compliance" that wouldn't survive an adversarial pass. R151 (refuse
to ship rule violations) is now load-bearing — my "ship and tidy
later" v.69 stance should not have passed.

### Risk

Medium. Licence endpoint shape changed — any external caller polling
`/api/licence` for licence/grower_id will now get 403 if they don't
present the Supervisor token; the old auth-exempt detail leak is
gone. If Core is the only consumer (which it is per the module
docstring) and authenticates as Supervisor (which it does — it runs
under Supervisor and has the same token), the contract is preserved.

Global error handler is purely additive — failing routes that
previously leaked detail now don't; routes that didn't fail are
unchanged.

## 2026.6.69 — Audit Phase 1: 7 rule gaps closed (R65/R85/R88/R92/R124/R126/R134/R137)

First batch of the path-to-zero audit walk against Golden Rules v2.3.
Single deploy, low risk, all narrow root-cause fixes.

### Smoke checklist (R85)
- [ ] `/health` returns 200 with `db_ok=true`
- [ ] Addon state=started within 180s
- [ ] Login screen renders (`/login`)
- [ ] Dashboard renders for an authenticated user
- [ ] Edit a part → save → reload → values persist
- [ ] Edit an asset → save → reload → values persist
- [ ] Restart loses no state; pool re-opens cleanly
- [ ] Logs contain no secrets or unhandled tracebacks

### Closures

- **R65 mypy clean** — `pat_manager.py:124` `import requests as httpx`
  fallback now carries `# type: ignore[no-redef,import-untyped]` so
  the `--strict-optional` audit-venv mypy stops failing on the
  missing types-requests stub. Production deployment uses the
  `import httpx` branch — fallback is for environments where httpx
  is missing.
- **R85 smoke checklist** — `[ ]` block added to this entry (above).
  Pattern adopted; will be carried forward on each release.
- **R88 reserved LogRecord key** — `videos.py:206` was passing
  `extra={"filename": …}` which is a reserved LogRecord attribute and
  crashes Python 3.11 logging when the formatter tries to read it
  back. Renamed to `extra={"file": …}`.
- **R92 + R134 graceful shutdown** — added `@app.on_event("shutdown")`
  handler in `main.py` that closes the DB connection pool via
  `_pool.closeall()`. Idempotent and fail-soft if the pool wasn't
  initialised.
- **R124 + R133 single Supervisor adapter** — created
  `asmpro/supervisor_client.py` consolidating all `http://supervisor/...`
  calls. Three callsites refactored: `helpers.py` (notify_ha /
  dismiss_ha_notification), `notifications.py` (group dispatcher),
  `pat_manager.py` (store repo register + reload). Pattern mirrors
  GSM v.250. Single blast radius for slug / auth / URL changes.
- **R126 startup config validation** — `main.py` startup now calls
  `_validate_required_config()` BEFORE `ensure_database()`. Missing
  `ASM_DB_*` env vars raise `SystemExit` with a clear, named message
  and a log line listing exactly which keys are missing — instead of
  later surfacing as an opaque 500 on the first DB-touching request.
- **R137 blocking IO acknowledged** — added an "Acknowledged
  architectural debt (Rule 137)" subsection to CLAUDE.md `## Known
  Issues / TODOs` documenting blocking psycopg2 in async-def handlers
  as known platform debt, with migration-path notes.

### Files changed
- `asmpro/supervisor_client.py` — new file, the canonical Supervisor adapter
- `asmpro/helpers.py` — `notify_ha` / `dismiss_ha_notification` forward to adapter
- `asmpro/notifications.py` — group dispatcher uses `supervisor_client.call_service`
- `asmpro/pat_manager.py` — store repo + reload via adapter; mypy fix
- `asmpro/main.py` — `_validate_required_config()` + `@app.on_event("shutdown")`
- `asmpro/videos.py` — `filename` → `file` in log extra
- `CLAUDE.md` — Rule 137 acknowledgement paragraph
- `config.yaml` + `asmpro/__init__.py` — version bump
- `CHANGELOG.md` — this entry

### Risk
Low. Supervisor adapter is structural but behaviour-preserving (same
URLs, same timeouts, same fail-soft pattern). Shutdown handler is
strict-additive. Config validation only crashes on truly missing config
which would have failed later anyway. mypy fix is a comment-only
ignore. Notify path same external behaviour.

### Audit headline delta (v.68 → v.69)
- ✓ +7 (R65, R85, R88, R92, R124/R133, R126, R134, R137)
- ✗ -8 (the 7 closed + R134 was a duplicate of R92)
- Total walked unchanged at 62

### Next phases (queued)
- Phase 2: R17 master theme sync (copy canonical paddisense-tokens.css)
- Phase 3: R82 CDN integrity hashes + R66 pytest module-import fix
- Phase 4: R51 window.open removal (HA Companion compatibility)
- Phase 5-7: R56/R57/R125 (types/docstrings/Pydantic), R60 long fns,
  R17 hex / R41 inline styles / R22 JS tabs
- Phase 8: R12 canonical core/+domain/ split (very large)

## 2026.6.68 — hotfix: v.67 column-add re-introduced the orphan service_interval_hours column

Found minutes after v.67 deployed. Caused by an interaction between the
column-add framework (idempotent by column-name lookup) and v3's RENAME:

1. v.67 column-migrations list still named the OLD column
   `service_interval_hours`. The idempotency check is "does column X
   exist? if not, ADD it."
2. v3 RENAMEd it to `service_interval`.
3. On the next startup, the column-add check saw `service_interval_hours`
   as missing and ADDed it again — empty, orphan, next to the real one.

End state on dev: both columns existed, real data lived in
`service_interval`, `service_interval_hours` was an empty re-add.

### Fix

- **Column-migrations list**: change the tuple from `service_interval_hours`
  → `service_interval`. Now the idempotency check matches the
  post-v3 column name; nothing gets re-added.
- **v3 hardened** to handle 4 states (only-new, only-old, both, neither)
  with COALESCE-then-drop on the "both" path. The "both" state could
  also be reached by a pre-v3 install hitting v.68 code where column-add
  creates the new-named column before v3 runs — that path now works too.
- **Data migration v4**: defensive cleanup. Drops
  `service_interval_hours` if any install passed through the buggy
  state. COALESCE first so we never silently lose data. No-op on clean
  installs.

### Engineering-depth notes

The "fix forward" path was tempting (just drop the orphan and move on)
but doesn't actually fix the underlying ordering bug. Any future
addon-image rebuild of v.67 would have re-introduced the orphan. v.68
fixes the bug at source.

### Verification expected post-deploy

- `schema_version` = 4
- `assets` columns matching `service_interval%` = `['service_interval']`
  only — no orphan
- Existing asset data preserved (AST_8fa2cb still has
  service_interval=12.0)
- No "MIGRATION_V60_MARKER" duplicate entries (only v4 runs anew; v3 is
  already at schema_version=3 so it skips)

### Files changed

- `asmpro/db/_migrate.py` — column tuple uses new name; v3 hardened;
  v4 added
- `config.yaml` + `asmpro/__init__.py` — version bump
- `CHANGELOG.md` — this entry

## 2026.6.67 — Parts edit parity with create, supplier field, unit-aware service interval

Three changes in one release, executed per Peter's engineering-depth
directive ("like a 20 year veteran") — root-cause, no shortcuts,
deprecation windows where they buy safety, migration-verified, all 12
service_interval_hours callsites walked.

### Parts edit form: mirror of new-part form

Peter, 2026-06-12: "i need the same form as adding a new part" for the
parts edit modal. The v.63 modal hid the location cascade on edit
because stock-location changes go via Adjust Stock / Transfer. v.67
makes the cascade VISIBLE on edit and additive on save: the deepest
selected location is `upsert`ed into `part_stock_locations` with
`qty=0` (ON CONFLICT DO NOTHING). Existing stock locations are
preserved. Stock movement still goes via Adjust Stock / Transfer; the
edit form just records association.

Pre-population: when the modal opens for edit, JS fetches
`/parts/api/{id}` to read the part's `stock_locations` and uses the
first one's `location_id` to walk the tree and pre-select Site /
Location / Area.

### Parts: new `supplier` column

Live-user ask. Free-text column on `parts` table.

- Schema: `supplier TEXT` (added via column migration; also added to
  schema.sql for fresh installs per the v.58 precedent)
- DB: `create_part(... supplier=None)`, `update_part` whitelist gains
  "supplier"
- API: `POST /parts/api/create` reads `body.supplier`,
  `PUT /parts/api/{id}` accepts via the same kwargs path
- UI: Supplier field inserted between Part Number and Category on
  desktop modal (parts.html), new-part mobile (parts_new_mobile.html),
  and edit mobile (parts_edit_mobile.html). Pre-populates from
  `part.supplier` on edit.

### Asset service interval: unit-aware (column rename, dynamic UI)

The original column `service_interval_hours` baked the unit assumption
into the schema. For non-hours meters (km, both) this misled reports
and the edit-form label. v.67 fixes the root cause.

**Data migration v3** (versioned via `settings.schema_version`):

```sql
ALTER TABLE assets RENAME COLUMN service_interval_hours TO service_interval
```

Idempotent guard:
1. If `service_interval` already exists → no-op (migration already ran).
2. If only `service_interval_hours` exists → RENAME.
3. If neither exists → raise (unexpected; surfaces loudly so we don't
   limp along with a half-migrated schema).
4. Post-rename sanity check via `information_schema.columns` — confirms
   the new column is present BEFORE `schema_version` bumps to 3. If
   the rename silently failed, `schema_version` stays at 2 and next
   startup retries.

**API backcompat** (one release window):
- `POST /assets/api/create` accepts both `service_interval` (new) and
  `service_interval_hours` (legacy); old name is mapped to new.
- `db.assets.update_asset` accepts both kwargs; old name is mapped to
  new at the function entry.
- Pre-existing bug surfaced + fixed: `create_asset` previously didn't
  accept service_interval at all (silently dropped). Now passes it
  through.

**UI**:
- Label updates dynamically on Meter Type change:
  - hours → "Service Interval (hours)" — display "500 hrs"
  - km → "Service Interval (km)" — display "500 km"
  - both → "Service Interval (hours or km)" — display "500 hrs/km"
  - none → field HIDDEN, value cleared, display "—"
- Shipped on all 4 surfaces: `asset_detail.html` (edit modal +
  read-only display), `asset_detail_mobile.html` (same + the report
  card's countdown), `assets.html` (create modal).

### Files changed

- `asmpro/db/_migrate.py` — added `parts.supplier` column migration;
  added `_migration_3_rename_service_interval` data migration with
  pre/post sanity checks; registered in `_DATA_MIGRATIONS`
- `asmpro/db/parts.py` — `create_part` accepts supplier;
  `update_part` whitelist gains supplier; new
  `upsert_part_location(part_id, location_id)` helper for edit-form
  additive saves
- `asmpro/db/assets.py` — `create_asset` accepts `service_interval`;
  `update_asset` accepts legacy name with mapping
- `asmpro/parts.py` — POST/PUT accept supplier; PUT also handles
  `location_id` via `upsert_part_location`
- `asmpro/assets.py` — POST accepts both old and new interval names
- `asmpro/schema.sql` — `parts.supplier` for fresh installs
- `asmpro/templates/parts.html` — Supplier input + cascade visible on
  edit + cascade pre-populated from first stock_location + save sends
  both supplier and location_id
- `asmpro/templates/parts_new_mobile.html` — Supplier input + saves it
- `asmpro/templates/parts_edit_mobile.html` — Supplier + cascade
  picker + notes textarea + matching pre-populate + save
- `asmpro/templates/asset_detail.html` — service_interval (renamed) +
  dynamic label/visibility + display unit derives from meter_type
- `asmpro/templates/asset_detail_mobile.html` — same + the report-card
  countdown logic now picks "km" for km meters
- `asmpro/templates/assets.html` — same dynamic label on create modal
- `config.yaml` + `asmpro/__init__.py` — version bump
- `CHANGELOG.md` — this entry

### Risk

Medium-low. The data migration is the only thing that can go wrong; it's
gated by schema_version, idempotent, has pre+post sanity checks, and
will raise loudly rather than half-migrate. API backcompat windows
guard against any forgotten client. The 4 service_interval_hours
template refs all walked + updated. py_compile + grep audited.

### What's not in v.67 (intentional)

- Removal of the `service_interval_hours` API backcompat — defer until
  v.68+ so any external integrations have a release to update.

## 2026.6.66 — Asset edit modal: category dropdown + site/location/area cascade (desktop + mobile)

Asset edit modal previously had free-text Category and a single flat
Location dropdown. v.66 brings it inline with the parts wizard pattern.

### Desktop (`asset_detail.html`) + Mobile (`asset_detail_mobile.html`)

- **Category**: free-text input replaced with a `<select>` populated from
  `/api/config` `asset_categories`. If the asset's current category is
  not in the list (legacy data), it's kept as a "(legacy)" option so
  the value isn't silently dropped on save.
- **Location**: single flat dropdown replaced with cascading
  Site → Location → Area picker (mirrors the parts wizard JS pattern
  added in v.58/v.63).
- **Pre-population on edit**: when the modal opens with an existing
  `location_id`, the JS walks the `/locations/api/tree` to find which
  Site/Location/Area chain contains that id, then pre-selects each
  dropdown level accordingly. Handles all 3 depths — id is a site, a
  location, or an area. If `location_id` points at an orphaned row
  (rare, e.g. a stale FK to a deleted location), the picker stays at
  "Unassigned" and the user can re-pick.
- **Save** uses the same `_editDeepestSelectedLocation()` semantic as
  the parts wizard: returns area-id if selected, else location-id,
  else site-id, else null.

### Backend

No change. `PUT /assets/api/{id}` already accepts `category` (string) and
`location_id` (int) — the cascade just produces the deepest selected
id which goes straight in.

### Files changed

- `asmpro/templates/asset_detail.html` — Category select + cascade
  dropdowns + tree-walk pre-populate + cascade-derived save
- `asmpro/templates/asset_detail_mobile.html` — identical changes
  mirrored to mobile
- `config.yaml` + `asmpro/__init__.py` — version bump
- `CHANGELOG.md` — this entry

### Not yet matched (will follow if you want)

- `assets.html` CREATE modal — still has flat location dropdown.
  Same fix would apply. Skipped here because Peter named the EDIT
  form specifically; flag if you want parity.
- Asset detail header subtitle currently shows
  `asset.category · asset.location_name` from the server-rendered
  Jinja. After edit + save the page reloads so this picks up the
  new values; no JS update needed.

### Risk

Low. Pure UI change. Save payload field names unchanged. Tree-walk
pre-population is defensive — handles legacy / orphan / null
location_id without breaking the modal.

## 2026.6.65 — ASM.09 Config: tile-per-domain refactor (7 tiles, list-picker dropdowns)

The Configuration page used to have 6 tabs with a "Categories" tab
containing 11 separate cards (Asset/Part/Issue/Prestart Categories,
Asset Types, Part Units, Issue Severities, Meter Types, Prestart
Cadences, Location Types, Checklist Response Types) — Peter
described this as "a massive list."

v.65 restructures along DOMAIN boundaries with one tile per major area
and a sub-list dropdown within each tile to pick which list to edit.
Pattern modelled on the existing Prestart Checklists per-category
dropdown.

### 7 top-level tiles

| Tile | Sub-list dropdown options |
|---|---|
| 🛠 **Assets** | Categories, Types, Meter Types, Attribute Types |
| 🔧 **Parts** | Categories, Units |
| ⚠ **Issues** | Categories, Severities |
| 🔄 **Services** | Types |
| ✅ **Prestart Checklists** | Per-Category Checklists (default — the existing complex editor), Categories, Cadences, Response Types |
| 📍 **Locations** | Site Structure (default — existing tree builder), Location Types |
| 🔔 **Notifications** | Groups (existing) |

Tiles render as a CSS grid (auto-fit, 150px min) — collapses to 2 cols
on mobile. Active tile highlighted in primary colour. Tabs are gone;
the tile bar replaces them.

### How the sub-list switcher works

Each tile pre-renders ALL its sub-list DOMs (with the `data-tile="..."
data-key="..."` attributes and class `sublist-wrap`). The dropdown
toggles `.sublist-hidden` on/off via `pickSubList(tile, key)`. The
existing `renderSimpleList()`, `addItem()`, `removeItem()` functions
keep working untouched because they look up DOM by `id="list-${key}"`
and `id="add-${key}"` — those IDs are unique across the page, just
their visibility changes.

### Risk

Low to medium. No backend change. Pure template restructure + 2 new
JS helpers. The existing complex editors (per-category checklist,
site tree, notification groups) are wrapped in sub-list panels but
their internal behaviour is unchanged. Existing list mutations
(add/edit/delete) reuse the same handlers.

If something looks lost it's probably hidden under the wrong tile —
the search-by-ID semantic means everything still works, just where
it's grouped differs.

### Files changed

- `asmpro/templates/config.html` — tab nav → tile grid; sec-categories
  + sec-services + sec-attributes + sec-checklists merged into per-domain
  sec-assets / sec-parts / sec-issues / sec-services / sec-prestart;
  sec-locations gets a sub-list picker for location_types; JS
  `switchTab` → `selectTile` + new `pickSubList`
- `config.yaml` + `asmpro/__init__.py` — version bump
- `CHANGELOG.md` — this entry

## 2026.6.64 — ASM.04 Parts Inventory: category filter (desktop + mobile)

Desktop first, then mobile matches — per
`feedback_desktop_first_then_mobile.md`.

### What changed

- Desktop `parts.html`: new "All categories" dropdown in the search bar
  between Search and Low Stock. Sources from `_categories`
  (already loaded by `loadConfig()` from `/api/config`). Filters
  via the existing `category=` query param on `/parts/api/list` —
  no backend change.
- Mobile `parts_mobile.html`: matching dropdown below the search/low
  row. Populated from `/api/config` on init. Same `category=` query
  param wiring.
- Selection persists across re-renders via `current` capture in
  `populateCategoryFilter()` on desktop.

### Backend

No change — `db.parts.list_parts(category=...)` and
`/parts/api/list?category=...` already existed.

### Files changed

- `asmpro/templates/parts.html` — added `<select>` + cascade-aware
  `loadParts()` + `populateCategoryFilter()` + .s-cat-filter class
- `asmpro/templates/parts_mobile.html` — added `<select>` + cascade-aware
  `loadParts()` + init fetch + .cat-filter class
- `config.yaml` + `asmpro/__init__.py` — version bump
- `CHANGELOG.md` — this entry

### Risk

Low. Pure UI addition. Existing parts list behaviour unchanged when no
category is selected (default "All categories" sets no `category=` param).

## 2026.6.63 — Desktop new-part modal matches mobile (site/location/area + notes)

Mobile-only ship from v.58 was an oversight: the new-part wizard was on
mobile but the desktop modal still only had Name/Number/Category/Stock/
Cost/Unit. Per Peter's directive 2026-06-12: "browser first then always
match mobile" — captured as a permanent feedback rule
(`feedback_desktop_first_then_mobile.md`).

### What changed

- Desktop modal in `parts.html` now has the same Site → Location → Area
  cascading dropdowns + Notes textarea as the mobile wizard.
- Cascade JS mirrors `parts_new_mobile.html` exactly: fetches
  `/locations/api/tree` in `loadConfig()`, populates Site on modal open,
  enables Location dropdown only after Site is picked, enables Area
  dropdown only after Location is picked. Area is optional; part is
  stocked at the deepest selected level.
- Notes textarea visible in BOTH create AND edit modes (notes are a
  part attribute, persisted on `parts.notes`).
- Location picker is HIDDEN in edit mode — stock locations are managed
  via the existing Adjust Stock / Transfer modals, not the part-edit
  form. Editing a part's row should not silently re-attribute its stock.

### Backend changes

- `db.parts.update_part()` now accepts `notes` in its kwargs whitelist
  so the PUT path can update the notes column. (CREATE path already
  accepted notes via v.58.)
- No new API endpoints; reuses `POST /parts/api/create` and
  `PUT /parts/api/{part_id}` (both already accept `notes`; create
  accepts `location_id`).

### Risk

Low. Mobile wizard unchanged. Desktop modal additions are purely
additive (new fields, new dropdowns). Picker hidden in edit mode so
existing edit flows are unchanged behavior-wise.

### Memory captured

`feedback_desktop_first_then_mobile.md` — surface parity is now a
release-time gate; desktop is built first then ported to mobile.

## 2026.6.62 — Dockerfile strips __pycache__ after COPY (final fix)

v.61 untracked the .pyc files but the supervisor's local git checkout
already had them on disk (git pull doesn't delete untracked files) and
the `COPY asmpro/` layer was cached so the .dockerignore didn't take
effect. v.62 makes the Dockerfile itself strip __pycache__ / .pyc files
inside the built image immediately after COPY, so no matter what's in
the build context, the resulting image can never contain stale
bytecode.

This is the permanent fix; doesn't depend on what's tracked in git,
what's in .dockerignore, or what the supervisor's local checkout
looks like.

## 2026.6.61 — ROOT CAUSE: stale .pyc files were being committed + COPY'd into image

Found the cause of v.58/.59/.60's "new source not reaching container":

`__pycache__/*.pyc` files were tracked in git despite `.gitignore` having
`__pycache__/` — they were committed BEFORE the ignore rule was added.
Every `git pull` brought them down; `COPY asmpro/ asmpro/` put them in
the built image; Python imported the stale bytecode (.pyc) instead of
the fresh source (.py).

That's why three rebuilds + store/reload + a version bump showed the
SAME traceback line 134 with `int(row[0])` — the .py on disk had
`int(row["value"])` but the .pyc cache had the v.58 bytecode and Python
used it.

### Fix

- `git rm -rf --cached **/__pycache__/` — untracked 7 .pyc files
  (already in .gitignore; just needed untracking)
- New `asm-pro/.dockerignore` — belt-and-braces excludes
  `__pycache__/`, `*.pyc`, `.git/`, `tests/`, `.mypy_cache/`, etc.
  from the COPY context so future .pyc files (if any sneak past
  git) still don't reach the image.

### Why I missed it for three versions

Memory `feedback_docker_cache_uninstall.md` blamed "supervisor docker
COPY-layer cache" — true in some cases but THIS time the cause was
upstream: git-tracked stale bytecode. The docker COPY layer cache
WAS invalidating correctly because the .py source content changed,
but the build was also copying the .pyc which won at import time.

### What v.60's diagnostic marker proves

When v.61 starts cleanly, `MIGRATION_V60_MARKER` log will appear
(the marker was added in v.60 but never visible because the stale
.pyc skipped that file's source entirely).

## 2026.6.60 — diagnostic: log marker to confirm new source reaches container

v.58 and v.59 builds both produced a container whose `_migrate.py` line 134
showed `int(row[0])` despite the source on disk having `int(row["value"])` —
suspected supervisor docker COPY-layer cache or git-checkout staleness
(documented pattern: `feedback_docker_cache_uninstall.md`). v.60 adds a
distinctive log line `MIGRATION_V60_MARKER` at the top of
`_run_data_migrations`. If it shows up in the v.60 startup log, the new
source is reaching the container; if not, the cache is genuinely stuck and
uninstall+reinstall is needed.

## 2026.6.59 — hotfix: RealDictCursor row access in new data-migration framework

v.58 crashed on startup with `KeyError: 0` at
`_migrate.py::_run_data_migrations` line `current = int(row[0]) if row else 1`.
Root cause: `get_cursor()` returns a RealDictCursor (per Rule 20 —
`row["col"]` not `row[0]`); my new data-migration runner used positional
access. Fixed: `row["value"]` + `KeyError` added to the except tuple as
belt-and-braces. Same gotcha called out as Rule 20 across all PaddiSense
addons — got me on the very first use of the cursor in the new framework.

No data changes; the v.58 migration block (locations cleanup + parts.notes)
never ran in v.58 because the new framework crashed before reaching it.
v.59 runs both migrations cleanly.

## 2026.6.58 — new-part wizard: site/location/area + notes + 3-level locations cleanup

**Live-user feedback driven.** Two bugs fixed in one release:

### New-part wizard now has site, location and area pickers + notes

The wizard previously had no way to set where the part lives or to add free-text notes. Both surfaced as user-reported gaps. Now:

- **Site → Location → Area** cascading dropdowns (uses the existing `/locations/api/tree` endpoint; locations dropdown disabled until a site is picked; area dropdown disabled until a location is picked and optional even then).
- **Part is attributed at the deepest level selected** — if you pick an area the stock row goes there; if you pick only site/location the stock row goes at the location level. Picking nothing is still allowed (creates the part without an initial location row).
- **Notes** textarea added — free-text description / specs / supplier / fit notes. Saved to a new `parts.notes` column.

### Locations hierarchy now strictly 3 levels

The `locations` table had ad-hoc `location_type` values (`site`, `depot`, `area`, `workshop`, `bin`) and two orphan rows that pretended to be sites but weren't typed as one. Tidied to enforce exactly three levels:

- `site` — top-level depot (parent_location_id NULL)
- `location` — within a site (parent_location_id = site)
- `area` — within a location (parent_location_id = location)

Data migration v2 (versioned via `settings.schema_version`, runs once per database):

1. Merges duplicate id=1 *RRAPL Seed Shed* into id=8 *Seed Shed* — re-attributes 1 row in `asm_issues` and 1 in `service_events` (both rows discovered via FK sweep, no data loss).
2. Deletes id=3 *RRAPL-FB-075* — duplicate of id=5 *Fruit Bin 075*, zero FK references confirmed.
3. Re-types remaining keepers: id=4/8/9 → `location`, id=5 → `area` (id=2 RRAPL was already `site`).
4. Adds `CHECK (location_type IN ('site','location','area'))` constraint — future rows can't reintroduce ad-hoc strings.
5. Updates the `location_types` config row from the old 5-value set to `["site","location","area"]`.

### Backend changes

- New column `parts.notes TEXT` (idempotent migration in `_migrate.py`).
- `db.parts.create_part()` accepts `notes` and `location_id` keyword args. When `location_id` is supplied, also writes a `part_stock_locations` row with `qty=0` so the part is attributed to that location even before stock arrives.
- `POST /parts/api/create` accepts `notes` and `location_id` from the request body, with explicit integer validation on `location_id`.
- New versioned data-migration framework in `_migrate.py` (`_run_data_migrations()` + `_DATA_MIGRATIONS` list, gated by `settings.schema_version`). Used for migration v2 (locations cleanup) and ready for future data tidies.
- `schema.sql` reflects the new column + types for fresh installs; existing installs land via the migration.
- `seed_data.sql` `location_types` config row updated to the new 3-value set (the existing config row on running DBs is also updated in-place by migration v2 step 5).

### Files changed

- `asm-pro/asmpro/db/_migrate.py` — new column migration for `parts.notes`; new `_run_data_migrations()` framework; migration v2 for locations
- `asm-pro/asmpro/schema.sql` — `notes TEXT` on parts
- `asm-pro/asmpro/seed_data.sql` — `location_types` config row updated
- `asm-pro/asmpro/db/parts.py` — `create_part` accepts notes + location_id; writes `part_stock_locations` row
- `asm-pro/asmpro/parts.py` — `POST /api/create` accepts notes + location_id with validation
- `asm-pro/asmpro/templates/parts_new_mobile.html` — 3 cascading dropdowns + notes textarea + JS cascade logic + `/locations/api/tree` fetch
- `config.yaml` + `asmpro/__init__.py` — version bump

### Risk

Medium. The locations migration mutates real data — but the changes are explicit, gated by `schema_version` (idempotent — runs once), and the FK sweep was done pre-migration to confirm safe row counts. The CHECK constraint addition can only happen AFTER the re-typing, so the order matters; encoded in migration order.

The wizard changes are additive — old API callers without `location_id` or `notes` continue to work (both are optional).

## 2026.6.57
- Fix: site/area rows on Config → Locations now expand on first click (was requiring two clicks due to inline-style/CSS mismatch in the toggle)
- Add: Prestart Categories list editor on Config → Categories (was the only `_VALID_CONFIG_KEYS` entry without a UI)

## 2026.6.56
- Search box on Assets page (ASM.03) — filter by name, category, or location (desktop + mobile)
- AUDIT.md refresh — fresh Golden Rules v2.1 walk against v.55 (38 ✓ / 12 ✗ / 16 ⊘ / 3 ⚠ / 8 ◔)
- CLAUDE.md Quick Reference version line updated

## 2026.6.22
- All dropdowns config-driven (8 new list editors on config page)
- Prestart checklist category fallback (sub-categories use parent checklist)
- Fix: checklist category dropdown shows all asset categories

## 2026.6.18
- Port conflict fix (8102)
- Notification groups
- Security hardening
- Bug fixes and enhancements
