# Changelog

## 2026.7.9 — owner-login rotation self-heal (WR-PS-192/074 structural fix, port of Weather bd8d124)

### Fixed
- **Incident 2026-07-27 (Weather was the victim; Safety carries the same class):** a flipped
  `*_owner` login uses a STATIC stored options password; a DB-role seed re-mint changes the
  Postgres role underneath it and the addon strands on its next restart (DB init failed →
  licence gate fail-closed → licence screen).
- Structural fix in `core/db/_pool.py`: for `*_owner` logins the password is now DERIVED
  from the `/share` box key first (the fleet's derivation truth, Core v2026.7.44), with the
  stored options password as fallback; loud WARNING when the stored copy is stale. The
  admin/owner pool also gained the same auth-failure rebuild-and-retry self-heal the app
  pool has had since 2026-07-09. `db_user: postgres` (pre-flip) boxes are unaffected —
  stored password only, never derived.
- Regression tests: owner candidate ladder + admin-pool self-heal + end-to-end
  stale-stored-password recovery, proven-fail against the pre-fix code.

### Changed
- Theme tokens re-synced to steward canonical (Rule 17 gate-mandated re-cp,
  palette consolidation — same re-cp Weather took at its v2026.7.7; no
  addon-specific CSS lives in the tokens copy).

## 2026.7.8 — WR-PS-183: redactor re-vendored (all six GitHub token classes)

### Changed
- **The vendored log redactor re-synced byte-identical to the patched
  canonical**: `gh[posur]_` now masks `ghp_`/`gho_`/`ghs_`/`ghu_`/`ghr_`
  alongside `github_pat_` (WR-PS-183 completeness sliver). Shared test
  refreshed (+4 fixtures).

## 2026.7.7 — WR-PS-108 fleet flip: access-sync enforce ON by default

### Changed
- **Unsigned or invalid grant pushes are now rejected with 403.**
  `SAFETY_ACCESS_SYNC_ENFORCE` defaults ON (`=0` kill-switch — code-default
  pattern, grower boxes have no env plumbing). Core's signed pushes have been
  verifying and pinning since the receiver landed; this closes the warn-only
  window fleet-wide (WR-PS-108, Peter's go 2026-07-17). A `bound_fp` mismatch
  already failed closed before this flip.

## 2026.7.6 — WR-PS-179: canonical log redactor vendored + wired

### Added
- **Structural log redaction at the entry point.** Safety previously shipped no
  log redactor at all. `core/_log_redactor.py` is now a byte-identical vendor of
  the fleet canonical `documentation/shared/log_redactor.py` (GSM⊕Core superset:
  cloudhook URLs, PATs, bearer/DSN/`enc:` tokens, labelled secrets, portal/Resend
  keys, email + phone PII), wired as the root `RedactingFormatter` with uvicorn
  `log_config=None` so uvicorn.access/error pass through it too. Shared 30-case
  behavioural test adopted. Closes Safety's SEC-17/KEY-01/DATA-01 cell.

## 2026.7.5 — Office-TV kiosk display + access-sync verify-and-pin (WR-PS-108)

### Added
- **Office-TV kiosk display over a LAN port.** The addon now also exposes an optional LAN port
  (`config.yaml` `ports:` on 8097 (unmapped by default — grower maps a free host port)) so the read-only `/kiosk` monitor is reachable off ingress. A new
  `kiosk_gate` middleware **token-gates the kiosk surface** — `/kiosk` and the two read endpoints it
  polls (`/wss/api/live-status`, `/wss/api/zones`) — whenever it's reached off ingress: a valid
  `kiosk_key` marks the request read-only (pseudo-user, skips login); no/!wrong key → 403
  (fail-closed, so with `kiosk_key` unset the off-ingress kiosk is simply off). A valid key does NOT
  unlock anything else — every non-kiosk path stays behind the addon's normal login on that port,
  exactly as over ingress (verified by test). On the TV, a Chrome/Android-TV kiosk browser loads
  `http://<ha-ip>:<mapped-port>/kiosk?key=<key>`; a short-lived `ps_kiosk` cookie then authenticates the page's
  polls. Note: true kiosk-*only* isolation of the port would need a separate kiosk listener (the Host
  header isn't a trustworthy signal of which port was used) — tracked as a follow-up. 8 new tests.
- **`/api/access/sync` now authenticates Core's grant push** (WR-PS-108). Core signs every push with
  its box_identity (Ed25519 over `canonical(payload)`, per-target); this receiver verifies the
  signature, binds the key to the `bound_fp` Admin signed into this add-on's licence (§9-A.10 — never
  bare TOFU on the untrusted `/23`), and enforces target-match + expiry + single-use nonce. A
  `bound_fp` mismatch **fails closed always**; an unsigned/invalid push is warn-only until the
  fleet-wide `SAFETY_ACCESS_SYNC_ENFORCE` flip. Vendored from the SugarSense reference. +7 tests.
- **`bound_fp` persisted from the activated licence** on `/api/licence/activate`.

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

## 2026.7.3 — Warn→block flip: signed-licence enforcement ON by default (SEC-04 receive-side)

### Changed
- **`SAFETY_SIGNED_LICENCE_ENFORCE` now defaults ON** — unsigned `/api/licence/activate` and
  `/api/licence/deactivate` are rejected (400); the Admin Ed25519 signature is the authorisation,
  never the /23 transport (§9-A). Closes the naked-deactivate hole. Readiness: Admin signs every
  licence fleet-wide (v2026.7.52 re-issue, 2026-07-12); present-but-bad signatures were already
  always fatal. `=0` = emergency kill-switch (grower boxes have no env plumbing — the code default
  IS the fleet flip). Core's manual UI deactivate forward (unsigned) now surfaces 400; deactivation
  is Admin-driven. Tests: default-rejected + kill-switch pairs on both paths (+4).

## 2026.7.2 — WR-PS-090 Ask 4: box-key read diagnostic (PWM reference adopted)

### Changed
- **`core/db/_pool.py::_read_master_key`** now logs every key read — source path, SHA-256
  fingerprint (12 hex), and mount identity (`dev`/`ino`/`size`/`mtime`) — and WARNs on every
  fallback instead of silently passing. A consumer's logged `fp`/`dev` can now be cross-checked
  against Core's published key (the diagnostic that cracked the 2026-07-06 fake-`/share`
  incident and the WR-PS-110 key churn). Read order and return values unchanged.

## 2026.7.1 — WR-PS-109: per-user module-access enforcement on ingress (Hone SEC-04/SEC-09, Option B)

### Added
- **`core/module_gate.py`** (vendored from the Farm reference, `MODULE_KEY="paddisense-safety"`):
  Core pushes its `module_access` grant table to `POST /api/access/sync`; Safety caches it durably
  in `/data/module_access_grants.json` (atomic swap) and enforces per-user access locally on every
  **ingress** request. Decision semantics mirror Core's `effective_modules`: never-synced → open
  (bootstrap), synced-no-entries → open, granted/all-access/admin → allow, configured-but-ungranted
  → **403**. A direct cookie login with Safety's own credentials keeps its existing role path; the
  public `/kiosk` surface is untouched (ingress-only gate, kiosk stays in `_PUBLIC_PATHS`).
- **`POST /api/access/sync`** receiver — trust = the same transport gate the licence-forward path
  uses (`_verify_internal`); the §9-A.9 signed-grant envelope is the tracked fleet follow-up
  WR-PS-108.
- **`tests/test_module_gate.py`** (11) — decision-table units + end-to-end through the REAL auth
  middleware: ungranted ingress user 403s on pages and `/api/*`, granted user passes, never-synced
  box stays open, corrupt cache never locks the grower out.

## 2026.6.49 — Rotation self-heal for the app DB pool (incident 2026-07-09, Rule 106)

### Fixed
- **App DB pool self-heals across a box-key rotation.** When Core rotates the box key (`db_role.key`,
  WR-PS-088 / ADR-013), the app DB password changes; a long-running pool holds the old one, so the next
  fresh connection fails auth and the add-on breaks until a manual restart — which a grower can't do.
  `_acquire_conn` now treats a `password authentication failed` on the app pool as a stale key: drops
  the pool, rebuilds it (re-reading `/share/paddisense/db_role.key`), and retries once; a second
  failure propagates. Never applies to the admin/superuser pool (R173 intact). Fleet-wide fix
  originating from the live PWM incident. `tests/test_pool_selfheal.py`.

## 2026.6.48 — Hone PS-SEC-19: mask secret config fields + Rule 17 theme re-sync

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

## 2026.6.47

Changed
- Prefer the dedicated `/share/paddisense/db_role.key` for the `safety_app` DB password; falls back
  to `master.key` during the WR-PS-088 split rollout — no behaviour change today (both keys carry
  the same value until the 1b flip).


## 2026.6.46

Fixed
- Dockerfile no longer COPYs `ruff.toml`/`mypy.ini` (removed in v2026.6.43 when the ruff/mypy
  config moved to `pyproject.toml`). Those stale `COPY` lines made the image build fail with
  "unknown error while trying to build the image" on every box. Lint config is dev/CI-only and
  isn't needed in the runtime image. No app behaviour change.


## 2026.6.45 — ADR-010 release gate CLEARED + flipped to BLOCKING

### Theme alignment (Rule 193 — release gate)
- **Removed the dangling `.ps-form-control` deviation** from the desktop config
  and WSS-settings templates. Per the theme steward (2026-06-23), `.ps-form-control`
  is a non-existent reference to REMOVE, not add to the master; the canonical
  form pattern is `.ps-field` (descendant-selector). The affected inputs already
  carry their own sizing classes (`ss-input-150/180`, `wss-mgr-num`,
  `wss-mgr-pin-input`) so removal is visually inert — the class rendered nothing.
- **Renamed the users table `.ps-table` → the canonical `.ps-data-table`**
  (config.html). Now Rule 193 reports 0 dangling theme classes.
- Note: a browser smoke of the config + WSS-settings pages is owed before a
  grower cut (low risk — the removed class was already unstyled).

### CI
- `.github/workflows/ci.yml` `release-gate` job flipped from rollout
  (`continue-on-error`) to **BLOCKING** — the ADR-010 pre-release gate now
  fails CI on a regression. mypy and pip-audit were already clean.

## 2026.6.44 — R142 signed-licence replay protection now proven (test-only)

### Security-test correction (Rule 192 / red-team)
- **R142 replay/nonce/timestamp was WRONGLY marked N/A.** The vendored
  `core/licence_verify.py::verify_artifact` — reached from the licence
  activate/deactivate path (`api/licence.py::evaluate_signature`) — already
  enforces a single-use `(licence_id, nonce)` ledger (`_nonce_ok`) AND an
  `issued_at`/`exp` freshness window (`_fresh`, ±60 s skew). A signed request
  with a stale timestamp or a replayed nonce is refused even when the Ed25519
  signature is perfectly valid. That IS the Rule 142 control; it simply had no
  regression test.
- **New `tests/test_r142_licence_replay.py`** forges a REAL Ed25519 signature
  with a throwaway pinned test key and proves: a fresh unseen nonce is accepted
  (positive control), a reused nonce is rejected, and a stale/future-dated
  timestamp is rejected. Not a name-only stub — the accept case makes the two
  rejects meaningful. Full suite green (45 passed).
- **`docs/AUDIT.md`** R142 reclassified N/A → **COVERED** with the test name as
  evidence. R188 (session-revoke) re-confirmed **N/A** honestly: the only
  change-password surface is a stub that toasts "Password management not yet
  implemented" and posts to no backend route — there is no credential-change
  event to revoke sessions on.
- **No production code changed** — this is test + docs only; no prod path
  weakened.

_Plain-English (grower-facing):_ We added an automated safety check that proves
the Worker Safety System refuses a "replayed" licence message — one that was
captured and re-sent, or one with an out-of-date timestamp. This protection was
already built in; this release just adds the test that guards it so it can never
silently regress. Nothing changes in how the app behaves for you.

## 2026.6.43 — ADR-010 flip-ready under Golden Rules v2.49

### Lifecycle / reliability
- **Shutdown handler added (R92/134).** `main.py` now registers `@app.on_event("shutdown")`
  which cancels both background tasks (`stop_wss_monitor()` + `stop_ha_entity_publisher()`)
  and calls `close_pools()`. New `stop_*` functions exported from `api/__init__.py` and
  `api/ha_entities.py`. Previously the monitor loops and DB pools were never torn down.

### Tooling / config
- **Ruff + mypy config consolidated into `pyproject.toml`** (`[tool.ruff]` / `[tool.mypy]`),
  replacing the standalone `ruff.toml` / `mypy.ini` (R64/65, fleet consistency). Lint/type
  behaviour unchanged (ruff + mypy re-run clean).

### UI
- **R41 to zero.** The 9 remaining inline `style=` attributes (the admin user-list table in
  `config.html`) extracted to `wss-user-*` classes in `app.css`.

### Security tests (REQUIRED_SECURITY_TESTS manifest → full applicable coverage)
- New `tests/test_security_manifest.py`: **R158** oversized body → 413 + admin-PIN endpoint
  → 429 (bounded enumeration); **R187** forged `X-Forwarded-For`/`X-Real-IP` ignored (ingress
  trust keys off the real socket peer); **R190** unknown-user and wrong-password login responses
  are byte-identical (no username-enumeration oracle). R157 (CSRF 403) already covered by
  `test_csrf_and_mobile.py`. Remaining manifest rows (142/146/153/154/159/171/188/189) marked
  N/A in `docs/AUDIT.md` with concrete reasons.
- **Test harness now provisions the disposable test DB like Core provisions a real box** —
  `conftest.py` grants the least-priv `safety_app` role its DML privileges and seeds a licence
  row. Without this the fail-closed app pool (WR-PS-081) hit `permission denied` on every
  request-path query and the licence gate fail-closed to 403 (22 → 41 tests now pass).

### Docs
- Re-audited to Golden Rules **v2.49** (R118); `docs/AUDIT.md` refreshed; CLAUDE.md
  `golden_rules_version` = 2.49.

## 2026.6.42 — SEC-08/R173: fail-closed DB app pool (Phase-2, WR-PS-081)

### Security
- **The request-path DB pool is now fail-closed (R173/SEC-08).** `_pool.py` no longer falls back to
  the `postgres` superuser if the `safety_app` app pool can't initialise — `get_cursor()` returns the
  least-priv app pool or raises. Migrations/DDL still use the admin pool during the startup window
  (before `init_app_pool()` is called). Converges the fleet to Farm's fail-closed posture; a future
  key/role failure now fails loudly instead of silently promoting request-path queries to superuser.
  (`/share` persists, so an established box that reboots keeps its key and does not fail-closed.)

## 2026.6.41 — SEC-08/R173: admin/app DB pool split (fleet-standard, WR-PS-081)

### Security
- **`_pool.py` now maintains two pools** — an **admin** pool (`postgres` superuser) for migrations/DDL
  and an **app** pool (`safety_app`, least-privilege DML) for request-path queries. `get_cursor()` uses
  admin while the app pool isn't ready (startup/migrations), then `main.py` calls `init_app_pool()`
  after `ensure_database()` so request-path queries run as `safety_app`. Adopts the Livestock/Farm
  canonical pattern; the prior single-pool-on-app-role would have failed **fresh-box** schema
  provisioning (`permission denied for schema public`). DDL routes through admin, DML through the app
  role. Shutdown closes both pools.

## 2026.6.40 — SEC-08/R173: read the shared box key so safety_app authenticates (WR-PS-081)

### Security
- **`_pool.py` now reads the box DB-role key from the shared `/share/paddisense/master.key`** Core
  publishes (WR-PS-081), falling back to the local `/data` key during rollout. The per-container
  `/data` key differed from Core's, so `safety_app`'s derived password never matched the role Core minted
  → the pool **silently fell back to the `postgres` superuser** (confirmed fleet-wide via boot logs).
  Now `safety_app` authenticates → the R173 least-priv DML-only request path is genuinely in effect.
  Fernet-at-rest untouched (separate `/data` key). Superuser fallback kept as a rollout safety net;
  Phase 2 fail-closes.

## 2026.6.39 — SCAL-03: Python 3.11 → 3.12 base-image bump + digest pin (Hone SCAL-03 / WR-PS-080)

### Changed
- **Base image `python:3.11-slim` → `python:3.12-slim@sha256:423ed6ab…199fbf`** (fleet-index digest).
  `ruff.toml target-version` + `mypy.ini python_version` → 3.12. Off the Python 3.11 EOL runway (Hone
  SCAL-03), digest-pinned for reproducible builds. Isolated bump — no dependency changes
  (WR-PS-080 non-goal). Tests run on the pinned 3.12 toolchain; dev-deploy rebuilds on 3.12-slim.

## 2026.6.38 — SEC-01/04: Admin signed-licence receive-side (Hone PS-SEC-04 fleet adoption)

### Security
- **Both mutating licence paths now verify the Admin Ed25519 signature** (`api/licence.py`). Safety
  previously trusted the `/23` transport (`_verify_internal`) alone on `/api/licence/activate` and
  `/api/licence/deactivate` — the "network-location = trust" pattern Hone **PS-SEC-04** flags and
  `SIGNED_LICENCE_CONTRACT §9-A` retires. Now:
  - Vendored `core/licence_verify.py` (byte-identical to `documentation/shared/`) + Admin pinned
    pubkey at `data/admin_signing_pubkey.json` (baked by the existing `COPY paddisense_safety/`).
  - `activate` verifies the licence signature via `_extract_licence` — handles **both** the paste
    `code` path and Core's heartbeat `signed_licence` distribution.
  - `deactivate` verifies the Admin signed instruction (`_verify_instruction_signature`,
    `action ∈ {deactivate,revoke}`).
  - Legacy-tolerant during the fleet signing rollout (`SAFETY_SIGNED_LICENCE_ENFORCE`, default off;
    present+bad sig always fatal, unsigned accepted until enforce). Signature — not network position
    — is the trust boundary; the `/23` check stays as defence-in-depth. `cryptography==48.0.1` pinned.
  - Tests: `tests/test_licence_signed.py` (11 pass — policy, `_extract_licence` both paths, API
    activate/deactivate signature gate). Closes the Safety slice of **WR-HONE-SEC-04**.

## 2026.6.37
### Fixed
- **Mobile INCIDENT modal was rendering as an always-visible inline card, not a fullscreen overlay.** Root cause: used `class="wss-modal"` on the wrapper — that class is a plain card style (background/radius/padding only, no positioning). The correct pattern in this codebase is `class="modal-overlay"` (defined in `static/app.css` as `display:none` + `.show { display:flex }` overlay with backdrop) — the same wrapper pause-modal / pin-modal / device-modal all use. Swapped the incident-modal wrapper to `.modal-overlay`; the step-1 / step-2 content inside remains unchanged. (Peter feedback 2026-07-02: "below that i have a big square that says Send Incident Alert? with more text then cancel button and send alert button".)

## 2026.6.36
### Changed
- **Mobile INCIDENT confirm now has a true two-step flow** (Peter feedback 2026-07-02: "there was no second step, after i hit send alert i want a second confirmation"). Modal split into `#incident-step-1` ("Send incident alert?" → Cancel / Send alert) and `#incident-step-2` ("⚠ Are you sure? This alert will be sent immediately and cannot be recalled." → Go back / Yes, send now). Only the Step-2 confirm fires `POST /trigger-incident`. Modal resets to Step 1 on close so a subsequent open starts fresh.

## 2026.6.35
### Changed
- **Mobile S02.M layout redesign** (Peter feedback 2026-07-02).
  * **Row 1:** INCIDENT — I NEED HELP button moved to the TOP of the worker panel, full width. Confirm modal (two-step) unchanged.
  * **Row 2:** External Tracking + Pause side-by-side (equal width). Replaces the previous full-width tracking banner.
  * On-page explanatory text stripped — details live inside the confirm modal only.
- **Tap worker icon on map → info + Clear alert button.** Map popup now shows username + status + a `Clear alert` button when `escalation_stage > 0`. Delegated click handler wires to the existing `POST /api/users/{uid}/clear-alert`. (Peter feedback 2026-07-02: "when I click on the user ICON that I can clear an alert trigger".)
- **Push-notification deep link → open the alerted worker's popup.** `POST /wss/api/users/{uid}/trigger-incident` notifications now carry `url=/wss/?user=<uid>` (primary, secondary, and every incident-event group). Mobile WSS reads the `user` query param on first load, zooms to that worker, and opens their popup — one-tap navigation from the alert push to the Clear-alert action. (Peter feedback 2026-07-02: "when the notification appears in the home screen then make the navigation to the user button so the alert can be cleared".)

## 2026.6.34
### Removed
- **Desktop INCIDENT button retired** (v.32 → gone). Deleted button HTML, confirm modal, JS handlers, and `.wss-incident-*` CSS from `desktop/templates/wss.html`. Peter feedback 2026-07-02: "actually delete the incident alert from the browser page" — mobile is the only target (workers in the field). Backend `POST /wss/api/users/{uid}/trigger-incident` endpoint kept; mobile UI still uses it.

## 2026.6.33
### Added
- **INCIDENT — I NEED HELP button on mobile too.** Bigger red button (22px pad, 1.15rem type) under the pause control on `mobile/templates/wss.html`; same confirm modal + backend endpoint as desktop (`POST /wss/api/users/{uid}/trigger-incident`). This is the primary target — workers in the field use mobile. (Peter feedback 2026-07-02: "we don't need the incident alert on the browser so much but we need it on the mobile page".)
- **.M / .B page-ID suffixes (fleet consistency with Weather).** WSS/config/notifications page badges now show `S02.B` on desktop and `S02.M` on mobile (etc.), matching Weather's convention (H01.M / W01.B). Determined by `request.state.mode` in `main.py` route handlers. (Peter feedback 2026-07-02.)

## 2026.6.32
### Added
- **INCIDENT — I NEED HELP button on the worker dashboard.** Big red button under the pause/tracking controls. Two-tap confirm modal to prevent accidental press. `POST /wss/api/users/{uid}/trigger-incident` sets `escalation_stage=3`, logs to `wss_escalation_log`, and fires the incident event chain: `notify_manager` + `notify_secondary` + `send_event_notification("incident", ..., critical=True)` so every group configured for the "incident" event type is paged immediately. (Peter feedback 2026-07-02.)

### Fixed
- **Sidebar status banner always showed "System OFF".** `base.html` read `d.wss_enabled` but the API returns `system_enabled` — key mismatch. Fixed the key + exposed the fetch as `window.refreshWssStatusBanner()` so `_wssToggleEnabled` refreshes the banner immediately after the toggle saves (was previously stale until page reload). (Peter feedback 2026-07-02: "even after saving with new PIN the system shows status = OFF on the main menu bar".)

### Verified
- **External tracking toggle behaviour** — `renderMap`'s filter (`atWork || u.track_external` after the `awayNorms` early-out) implements the intended contract: track_external ON + off-site → shown; at-home or track_external OFF → hidden. No code change needed. (Peter feedback 2026-07-02.)

## 2026.6.31
### Fixed
- **System-enabled toggle now saves (root cause of "nothing works").** `set_system_enabled` returns 403 when the admin PIN is still the factory default ("1234"). The frontend `_wssToggleEnabled` swallowed the error, so the checkbox appeared to toggle but never persisted — every downstream feature (notifications, escalations, worker discovery) was blocked because `system_enabled` stayed false. Client now checks `response.ok`, rewinds the checkbox on failure, and surfaces the server error. `_wssSaveSettings` got the same fix (all three PUTs checked). Also `_wssSavePin` surfaces the server error text (was hiding "PIN too simple" as generic "Error saving PIN"), and its min-length now matches the server (6 digits, was 4). (Peter feedback 2026-07-02.)
- **PIN-modal warns when default is in use.** `verify-pin` returns `pin_change_required: is_default`; on entry with the factory PIN, WSS now shows `⚠ Default PIN in use — change it below to unlock admin actions` so the operator knows why enable/save silently blocks. (Peter feedback 2026-07-02.)
- **Pause fires a notification.** `pause_user` (POST `/api/users/{uid}/pause`) updated the DB but never called `notify_manager`, so the manager never learned a worker had paused monitoring. Now sends a `"Worker paused"` notification with reason + duration after the DB update. `notify_manager` tolerates a missing primary_id and no-ops if the primary contact isn't configured. (Peter feedback 2026-07-02: "when I click on a user in the dashboard and paused tracking, I didn't get a notification, but the test notification for this works".)

## 2026.6.30
### Added
- **Config page — admin user list.** `GET /wss/api/config/ps-users` returns the `ps_users` addon-login roster; `config.html` `loadUsers()` renders a real table (username / display name / role / active) instead of the "User management via database" placeholder. (Peter feedback 2026-07-02.)
- **Sidebar Manager Mode entry point.** `desktop/templates/base.html` sidebar button now fires the PIN modal directly on WSS S02, or navigates to `/wss/#manager` from other pages (which auto-fires the modal on load). Previously the button existed but had no handler wired. Role gate removed — Manager Mode IS the elevation entry, so it's visible to everyone.

### Changed
- **`cfg-role-secondary` — never empty.** When no notification groups are defined, the select falls through to the notify-services device list so the operator always has something to pick. Groups take precedence when they exist; the `<optgroup>` labels make the mode clear.
- **`discoverWorkers()` — real error surfacing.** Client now checks `response.ok` and shows the backend's error message (previously showed "Discovering..." toast regardless of outcome, hiding 403/500 errors). Also awaits `loadAll()` and re-renders the worker list on success.
- **WSS map — auto-fit to home zone for all users.** `renderZonesOnMap()` computed the home-zone target inside the admin-only branch, so non-admin users never got the zoom. Split so bounds math runs for everyone; circle overlays remain admin-only. Mobile got the same fix via `fitToHomeZone()` called from `loadAll()`.

### Compliance
- **WR-PS-069 §5 close.** `validate_config()` extracted from the startup handler into a public function per FLEET_PROCESS §5 canonical; called FIRST before `start_wss_monitor` / `start_ha_entity_publisher` (§4.4 D gate). Safety has no `pyproject.toml` (uses standalone `ruff.toml`/`mypy.ini`), so `check-startup-order.py` finds the startup module via the fallback probe.
- **Rules v2.44 → v2.46 walk.** v2.44→v2.45 R3 substrate correction (no code impact). v2.45→v2.46 ADR-012 §4 execution (R71 rewritten trunk-based, R72 amended, R116 RETIRED).
- **ADR-012 GSM-shape pilot.** Reconciliation merge landed the CRITICAL §6 conftest fix + 3 develop-side commits on `main`; local + origin `develop` deleted per §4.1.

## 2026.6.29
### Security
- **Rule 144 — licence liveness-only.** The public `GET /api/licence` (Core polls it without auth) leaked the licence string, product, expiry, and grower_id in its response body. It now returns ONLY `{"enrolled": <bool>}`, matching the fleet-correct Farm/ASM shape. Licence/grower data stays on token-only endpoints (activate/deactivate untouched). (WR-PS-066.)

## 2026.6.28
ADR-010 flip-readiness — cleared every verify-commit warning so Safety's rules can flip warn→block.
### Fixed
- **Rule 173 (bootstrap bug):** `ensure_database()` applied `schema.sql` (CREATE TABLE DDL)
  through the request-path pool (`safety_app`, no CREATE) instead of the `postgres` owner role,
  so first-boot schema creation failed `permission denied for schema public` once the
  least-privilege role was provisioned. Schema + migrations now run on a dedicated `postgres`
  DDL connection; the request path keeps using `safety_app` for DML. Surfaced by the smoke
  suite (22 tests) once this box provisioned `safety_app` + the box master key.
- R88: 4 logs used reserved LogRecord key `name` in `extra={}` (`notification_groups.py` ×2 →
  `group_name`; `_migrate.py` ×2 → `migration_name`) — would clobber/raise at log time.
- R178/orphan-bindings: restructured to per-page `<script nonce>` blocks (base no longer wraps
  `{% block script %}`; mobile base `<script>` given a nonce) so the orphan checker sees the
  `dataset.action` dispatcher — clears 7 false Class-B `data-action` findings. No behavioural change.
- R41: WSS map marker (`wss.html` desktop+mobile) inline styles → `.wss-marker` class +
  `--marker-bg` CSS-variable injection (the exempt dynamic pattern); white via `var(--ps-btn-text)`.
### Changed
- R17: re-synced `paddisense-tokens.css` byte-identical to master.
- R96/R118: CLAUDE.md → v2026.6.28 / golden_rules_version v2.42; AUDIT.md refreshed to v2.42.
### Contracts (shared — flagged to GR steward)
- check-orphan-bindings.py Class-C false-positive: the `bind*/init*/wire*(` regex matched library
  METHOD calls (`m.bindPopup()`, `m.bindTooltip()` — Leaflet). Added a `(?<![.\w])` lookbehind to
  exclude method calls. See WR-PS-059.

## 2026.6.27
### Security
- **Rule 157 — real CSRF protection.** Replaced the content-type-only check (which allowed a `multipart/form-data` CSRF bypass) with a double-submit token: `application/json` required + `X-CSRF-Token` header must match the `safety_csrf` cookie (constant-time) when a session cookie is present. Token issued at login, echoed by a base-template `fetch` wrapper, cleared on logout. Internal Core→addon licence calls exempt; ingress callers (no session cookie) are not cookie-CSRF-able. (Ported from PWM's canonical pattern; closes WR-SAF-001.)
- **Rule 158 — streaming body-size cap.** Body limit now counts actual bytes streamed (chunked-safe), not just the `Content-Length` header which a chunked body bypasses.
### Fixed
- **`/api/v1/status` returned 500** — zones were serialised with raw `dict()` (datetime not JSON-serialisable); now use `_serialize_row()`. Caught by the repaired smoke suite.
- **Type-safety bug** — `notifications._parse_targets` could return a non-list; now always returns a list (mypy clean).
### Testing / tooling
- Repaired the smoke suite: `conftest` now simulates the Supervisor ingress IP (`172.30.32.1`) + https base_url (Rule 181), and stale `/api/*` test paths corrected to the real `/api/v1/*` routes. **22 tests pass** (was 6 failing / never run locally).
- Added CSRF regression tests + a Rule 67 mobile data test (seed worker → assert `/live-status` returns it).
- Validated with real tools (not grep): ruff, mypy, bandit (0 HIGH), pip-audit (0 CVEs), pytest. CSRF fix confirmed by a live 403-without-token probe.
### Docs
- CLAUDE.md: corrected the false "public no-auth endpoints" note (all `/api/*` require auth; kiosk uses ingress-admin), documented the real CSRF model.

## 2026.6.26
### Changed
- **Compliance gap-closure pass — verify-commit.sh now exits clean.**
  - **Rule 167 (security):** `core/auth.py::is_ingress` ingress trust now uses the `ipaddress` module against `172.30.32.0/23` instead of a `startswith("172.30.32.")` string prefix (the prefix only matched the /24 and was a weaker check).
  - **Rule 60:** split 16 over-length functions (incl. the 266-line `_check_stationary_workers`) across `api/monitor.py`, `users.py`, `ha_entities.py`, `discovery.py`, `notifications.py`, `notification_groups.py`, `paddock_detect.py`, `zones.py` into named private helpers. Behaviour preserved — escalation chain, DB writes, HA calls and logging unchanged.
  - **Rule 17:** removed all 9 hardcoded hex colours from templates — kiosk inline tokens moved to `static/kiosk.css`; `wss.html` (desktop + mobile) marker/zone/paddock colours now read from `--ps-*` tokens via a `cssVar()` getComputedStyle helper.
  - **Rule 41:** inline `style=` attributes reduced 106 → 2 (the 2 remaining are runtime-dynamic Leaflet marker colours); extracted classes live in `static/app.css`.
  - Added `golden_rules_version` field to CLAUDE.md.

## 2026.6.25
### Fixed
- **Unlicensed landing page 404 under HA ingress.** The licence gate redirected to a prefix-less `/licence`, which the browser resolved outside the addon's ingress mount → HA 404, so an unlicensed box had no way to enter a licence code. The gate now derives the ingress prefix from the `X-Ingress-Path` header directly (it runs before the auth middleware that normally sets `base_path`), so the redirect carries the ingress prefix and the licence page loads. Regression test `tests/test_licence_gate_ingress.py`.

## 2026.6.24
### Changed
- `run.sh` sources the canonical master theme (`documentation/theme`, not the drift-prone `/config/theme`) — drift-proof at dev runtime (WR-PS-045 / ADR-007); re-synced tokens to master.
### Added
- `docs/SESSION_PICKUP.md` — durable in-repo session pickup (Rule 191).

## 2026.6.19

**Rule 41 inline handler migration + documentation.**

- **Rule 41 (no inline handlers):** migrated all 56 `onclick=`, `onchange=`, `oninput=` attributes across 10 templates to `addEventListener` with event delegation for dynamically-generated content. Zero inline handlers remain.
- **Rule 105 (AUDIT.md):** created `docs/AUDIT.md` -- Golden Rules v2.20 compliance audit (0 gaps, 1 acknowledged debt: 127 inline styles).
- **Rule 153 (THREAT_MODEL.md):** created `docs/security/THREAT_MODEL.md` -- 10 assets, 6 trust boundaries, 10-threat attacker's playbook, P/D/R/R matrix, 3-item gap register.
- Templates converted: desktop/mobile `wss.html` (28+16 handlers), `base.html` (2), `config.html` (1), `notifications.html` (6+6 each), `licence.html` (1+1).
- Event delegation pattern used for JS-generated innerHTML: tile grid, device picker, pause modal, zone list, day toggles, worker enable/disable, notification group actions.
- Version bump: `2026.6.18` -> `2026.6.19`.

## 2026.6.18

**Security hardening and quality improvements.**

- Minor security and quality fixes.

## 2026.6.17

**Maintenance release.**

- Bug fixes and stability improvements.

## 2026.6.16

**Full 100-rule compliance pass — gaps 84, 90, 92, 93 closed.**

- **Rule 84 (CLAUDE.md complete brief):** added missing `Background Tasks` and `Critical Rules` sections; refreshed `Quick Reference` to v2026.6.16; removed stale "7 bare exception blocks" note (P-Claude already rewrote 181 of them in v2026.6.15).
- **Rule 90 (CI hard gate):** `.github/workflows/ci.yml` rewritten as a strict 4-gate workflow (syntax → ruff → mypy → bandit, all HARD), runs on push/PR to `main` AND `develop`. `.github/workflows/trigger-build.yml` switched from `push: branches: [main]` to `workflow_run` — image dispatch ONLY fires after CI succeeds. A failing gate = no GHCR image.
- **Rule 92 (/api/v1/ prefix):** added `_add_v1_aliases()` helper in `main.py` that programmatically mirrors every legacy `/api/...` and `/wss/api/...` route under `/api/v1/...`. 36 v1 aliases registered alongside 41 legacy paths. Zero handler changes — legacy callers (Core polling `/api/licence`, web UI calling `/wss/api/*`) keep working.
- **Rule 93 (structured logging):** all 79 `log.info/warning/error/exception/debug` calls across 13 files converted from positional `%s` interpolation to `extra={"event": "...", ...}` dict format. Logs are now machine-parseable for fleet monitoring.
- **Mypy:** re-applied 6 fixes (`_pool.py` narrowing assert, `monitor.py` `int(val_raw)` type-ignore, `main.py` login form `str()` coercion) — P-Claude's v.15 lost these in the rebase. Now 0 mypy errors.
- **Quality gates verified locally:** ruff 0, mypy 0, bandit HIGH 0.

## 2026.6.12
- Multi-zone detection fix
- Security improvements
- Bug fixes and enhancements
