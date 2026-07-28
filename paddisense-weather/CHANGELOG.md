# Changelog

## 2026.7.10

### Security
- Weather-station (Ecowitt) API keys are no longer written to the add-on's log.

## 2026.7.9

### Reliability
- The add-on now reconnects to its database automatically after system updates or maintenance. Previously, a restart at the wrong moment could leave the add-on showing its licence screen until it was manually repaired — that can no longer happen.

## 2026.7.8

### Improved
- Wind roses now use finer wind-speed bands: 0-3, 3-10, 10-20, 20-35 and 35+ km/h — on the main wind rose and every station's rose, desktop and mobile.

## 2026.7.7 — theme palette-consolidation re-cp (no visual change)

### Changed
- Re-cp'd the master after its fleet palette-consolidation pass (12 duplicate-value tokens aliased to their semantic source, 6 dead `--ps-pwm-*` retired) + P's `--ps-control-h-hero`/`--ps-control-gap`. Every token resolves to the identical colour; no visual change. Keeps Weather byte-identical to the master under the hardened Rule 17.


## 2026.7.6 — scale tokens promoted to master; fallbacks no longer load-bearing (WR-PS-186)

### Changed
- Re-cp'd master which now DEFINES the `--ps-temp-min/max-*` + `--ps-rain-*` chart scale tokens (promoted from Weather's local hex fallbacks, exact same values — no visual change). Weather's `getPropertyValue` chart reads now resolve to a real token, so the hex fallbacks are belt-and-suspenders, not load-bearing (closes the v2026.7.5 follow-up).


## 2026.7.5 — theme alignment to new master + hardened-gate compliance (WR-PS-186/159)

### Changed
- Re-cp'd `paddisense-tokens.css` byte-identical from the master (WR-PS-186 control patterns now available). The theme gate now bites at commit fleet-wide, so declared Weather's weather-chart data-viz colour exemptions in `paddisense_weather/theme-exempt.txt` (temp/rain/wind chart scales read via `getPropertyValue` with a hex fallback; SVG gradient stops). UI is token-clean (0 app.css redefines, 0 dangling `ps-*`). Audit re-baselined v2.49→v2.50. Additive tokens, no functional change.
- ⚠ Follow-up: the `--ps-temp/rain/wind` scale tokens are read but not yet defined in the master — promote them so the hex fallbacks stop being load-bearing.


## 2026.7.4 — WR-PS-108 fleet flip: access-sync enforce ON by default

### Changed
- **Unsigned or invalid grant pushes are now rejected with 403.**
  `WX_ACCESS_SYNC_ENFORCE` defaults ON (`=0` kill-switch — code-default
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


## 2026.7.3 — WR-PS-108: access-sync verify-and-pin (§9-A.9 receiver)

### Added
- **WR-PS-108 / §9-A.9: the Core→add-on grant push is now verified-and-pinned.**
  Core signs every `POST /api/access/sync` with its box Ed25519 identity; this
  receiver now verifies the signature, authenticates Core's key against the
  `bound_fp` Admin signs into this add-on's licence (never bare TOFU), checks
  the freshness window and single-use nonce, and pins the key. A `bound_fp`
  mismatch fails closed ALWAYS — even in warn-only; an unsigned/invalid push
  is warn-only until `WX_ACCESS_SYNC_ENFORCE` (the coordinated fleet flip).
  `bound_fp` is persisted from the activated licence. Copied from the
  SugarSense v2026.7.12 reference; 7 behavioural tests (forged signature,
  cross-target replay, nonce replay, expiry, fp mismatch).


## 2026.7.2 — Key-read diagnostic on the DB-role key path (WR-PS-090 Ask 4)

### Added
- **`_read_master_key()` now logs the box-key source + fingerprint on every read** (WR-PS-090 Ask 4, PWM reference diagnostic): `source=<path> fp=<sha256[:12]> dev/ino/size/mtime`, in preference order (`/share` db_role.key → `/share` master.key → local `/data`). A silent fallback here means this addon's derived `weather_app` password no longer matches the role Core minted — which fail-closes every request-path query — and a fake overlay `/share` is now visible via the logged `st_dev`. Completes the P-pool adoption of the diagnostic that cracked the 2026-07-06 fake-`/share` incident and the WR-PS-110 key churn. No behaviour change to the key preference order; an empty key file is now skipped rather than returned.

## 2026.7.1 — WR-PS-109: per-user module-access enforcement on ingress (Hone SEC-04/SEC-09, Option B)

### Added
- **`core/module_gate.py`** (vendored from the Farm reference): Core pushes its `module_access`
  grant table to `POST /api/access/sync`; Weather caches it durably in
  `/data/module_access_grants.json` (atomic swap) and enforces per-user access locally on every
  **ingress** request. Decision semantics mirror Core's `effective_modules`: never-synced → open
  (bootstrap), synced-no-entries → open, granted/all-access/admin → allow, configured-but-ungranted
  → **403**. A direct cookie login with Weather's own credentials keeps its existing role path.
- **`POST /api/access/sync`** receiver — trust = the same transport gate the licence-forward path
  uses (`_verify_internal`); the §9-A.9 signed-grant envelope is the tracked fleet follow-up
  WR-PS-108.
- **`tests/test_module_gate.py`** (11) — decision-table units + end-to-end through the REAL auth
  middleware: ungranted ingress user 403s on pages and API paths, granted user passes, never-synced
  box stays open, corrupt cache never locks the grower out.

## 2026.6.84 — Rotation self-heal for the app DB pool (incident 2026-07-09, Rule 106)

### Fixed
- **App DB pool self-heals across a box-key rotation.** When Core rotates the box key (`db_role.key`,
  WR-PS-088 / ADR-013), the app DB password changes; a long-running pool holds the old one, so the next
  fresh connection fails auth and the add-on breaks until a manual restart — which a grower can't do.
  `_acquire_conn` now treats a `password authentication failed` on the app pool as a stale key: drops
  the pool, rebuilds it (re-reading `/share/paddisense/db_role.key`), and retries once; a second
  failure propagates. Never applies to the admin/superuser pool (R173 intact). Fleet-wide fix
  originating from the live PWM incident. `tests/test_pool_selfheal.py`.

## 2026.6.83 — Hone PS-SEC-19: mask secret config fields + Rule 17 theme re-sync

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

## 2026.6.82 — Prefer the dedicated /share DB-role key (WR-PS-088 split rollout)

Prefer the dedicated `/share/paddisense/db_role.key` for the `*_app` DB password;
falls back to `master.key` during the WR-PS-088 split rollout — no behaviour change
today. Core now publishes both keys with an identical value; they only diverge at the
future 1b flip, when `db_role.key` becomes distinct and `master.key` is retired. This
addon's pool now reads `db_role.key` first so it keeps authenticating across that flip.

### DB pool (`core/db/_pool.py`)
- `_read_master_key()` now tries `/share/paddisense/db_role.key` before
  `/share/paddisense/master.key`; local `/data` key and fail-closed / no-superuser
  fallback logic are unchanged. Additive and idempotent — identical behaviour today
  because both shared keys carry the same value.

## 2026.6.81 — Security tests now run for real (test-database fix) + replay/nonce coverage

Plain English: the automated security checks for this add-on can now actually run
end-to-end on a fresh test database and all of them pass. Previously two of the
checks quietly skipped themselves because the test database was set up so the
add-on's restricted database user couldn't read its own tables — so those safety
checks were never really proving anything outside the live add-on. That's fixed:
the test setup now grants the restricted user exactly the access it has in
production, so the checks run and pass just like they would on a grower's box.

We also added a real test for the signed-licence protection: a genuinely signed
but replayed licence (same one-time code sent twice) or an expired one is now
proven to be rejected. That safety was already built in; now there's an automated
test guarding it so it can never silently regress.

Nothing changed in the add-on itself — this is test-infrastructure and coverage
only. No behaviour, no database, and no security path in the shipped product was
altered.

### Test infrastructure (test-only — Rule 192 / WR-PS-081)
- `tests/conftest.py::_provision_test_db` now provisions the disposable
  `paddisense_weather_test` DB reproducibly: create DB + apply schema/migrations as
  the **admin** role, ensure the least-privilege `weather_app` role exists (password
  derived from the shared master key, exactly as in prod), then **GRANT** it the DML
  privileges it needs on the test DB. This closes the fleet blocker where a freshly
  created `*_test` DB gave the app role zero table grants → every request-path query
  raised `permission denied for table …` → the licence gate fail-closed 403 → the
  whole suite failed/skipped. Survives a drop+recreate of the test DB. Prod code and
  the prod database are untouched.

### Security-test coverage (REQUIRED_SECURITY_TESTS manifest) 7/12 → 8/12 applicable
- **R142 (new, was mis-marked N/A)** — `TestSignedLicenceReplayNonceTimestamp` proves
  `core.licence_verify.verify_artifact` rejects a **replayed** artifact (reused
  `(licence_id, nonce)`) and a **stale/expired** `issued_at`/`exp` window even when the
  Ed25519 signature is valid. The prior audit wrongly claimed no nonce/replay protocol
  existed; the protocol is real (`_nonce_ok` + `_fresh`) and is now regression-guarded.
- **R153 / R190 now execute for real** (no longer `skip`) because the app pool serves
  request-path queries against the properly-granted test DB.

## 2026.6.80 — ADR-010 flip-readiness re-audit (Golden Rules v2.49) + red-team security-test coverage 3→7

### Security tests (REQUIRED_SECURITY_TESTS manifest, Rule 154/192)
- Added `tests/test_security.py` with behavioural regression tests raising applicable
  coverage from **3/12 → 7/12** (the remaining 5 are genuinely N/A — see `docs/AUDIT.md`):
  - **R158** — oversized request body (11 MB > 10 MB cap) → 413 via the licence-exempt
    `/login` path, proving `BodySizeLimitMiddleware` bounds the body before any handler.
  - **R157** — a form-encoded mutation on the licence-exempt `/api/licence/activate` path
    → 403 "Invalid content type", proving the CSRF control fires in isolation (not merely
    the licence gate, which the existing test_smoke case cannot distinguish when the DB is down).
  - **R159** — `paddocks-proxy` (the only request-reachable server-side fetch) takes NO
    caller-supplied URL/host and returns a fixed FeatureCollection; an injected
    `?url=169.254.169.254/...` metadata param is never dereferenced.
  - **R187** — `is_ingress` refuses trust to a public peer that spoofs `X-Forwarded-For`
    into the Supervisor `/23`; trust is anchored on the real peer IP only.
  - **R153** — a caller-supplied station/burn-rule id is existence-scoped (unknown id → 404).
  - **R190** — non-existent username and wrong password for a real user return byte-identical
    login bodies (no user enumeration).
- **N/A rows documented** in `docs/AUDIT.md`: R142 (no timestamped/nonce'd signed-request
  ingress), R146 (no CSV/spreadsheet export), R171 (no security-event alert pipeline),
  R188 (no credential-change/password-reset flow), R189 (addon sends no email).

### Test infrastructure
- `tests/conftest.py`: the disposable test DB is now seeded with a licence + fixed users,
  and the ingress `client` fixture pins a Supervisor-subnet peer IP (`172.30.33.1`) so the
  suite is exercisable after the two 2026-07-04 fleet hardenings (v.79 ingress peer-IP trust
  + the DB-backed licence gate). Seeding uses the admin pool and is best-effort so collection
  never breaks. **Known infra limit (honest):** the WR-PS-081 fail-closed `weather_app` app
  pool derives its password from the Core-published shared master key; where that key is absent
  (this dev shell, outside the addon container) request-path DB queries fail-closed, so the two
  DB-dependent security tests (R153, R190) `skip` rather than fail. Inside the container all run green.

### Audit
- **Rule 118 re-audit to Golden Rules v2.49** (Wave-4a rule relocations/merges re-verified;
  Weather owns no relocated Category-A rule). `golden_rules_version` 2.48 → 2.49; `docs/AUDIT.md`
  `last_audit_date` 2026-07-04, one row per rule, real gap surfaced per R98.

## 2026.6.79 — 🔴 SEC: fix X-Ingress-Path header-spoof auth bypass (fleet-critical)

### Security
- **`core/auth.py::is_ingress` now requires the client IP on the Supervisor network
  (`172.30.32.0/23`) before trusting `X-Ingress-Path`.** It previously trusted the header
  unconditionally — so ANY client that could reach the addon port and set `X-Ingress-Path` was
  handed the `role: admin` ingress session (remote admin auth bypass). Restores the canonical
  `documentation/shared/auth.py` source-IP gate that 6 of 10 addons already carried. Found by the
  2026-07-04 fleet-consistency sweep; a `check-fleet-consistency.py` assertion will gate it (WR-PS-084).

## 2026.6.78 — SEC-08/R173: fail-closed DB app pool (Phase-2, WR-PS-081)

### Security
- **The request-path DB pool is now fail-closed (R173/SEC-08).** `_pool.py` no longer falls back to
  the `postgres` superuser if the `weather_app` app pool can't initialise — `get_cursor()` returns the
  least-priv app pool or raises. Migrations/DDL still use the admin pool during the startup window
  (before `init_app_pool()` is called). Converges the fleet to Farm's fail-closed posture; a future
  key/role failure now fails loudly instead of silently promoting request-path queries to superuser.
  (`/share` persists, so an established box that reboots keeps its key and does not fail-closed.)

## 2026.6.77 — SEC-08/R173: admin/app DB pool split (fleet-standard, WR-PS-081)

### Security
- **`_pool.py` now maintains two pools** — an **admin** pool (`postgres` superuser) for migrations/DDL
  and an **app** pool (`weather_app`, least-privilege DML) for request-path queries. `get_cursor()` uses
  admin while the app pool isn't ready (startup/migrations), then `main.py` calls `init_app_pool()`
  after `ensure_database()` so request-path queries run as `weather_app`. Adopts the Livestock/Farm
  canonical pattern; the prior single-pool-on-app-role would have failed **fresh-box** schema
  provisioning (`permission denied for schema public`). DDL routes through admin, DML through the app
  role. Shutdown closes both pools.

## 2026.6.76 — SEC-08/R173: read the shared box key so weather_app authenticates (WR-PS-081)

### Security
- **`_pool.py` now reads the box DB-role key from the shared `/share/paddisense/master.key`** Core
  publishes (WR-PS-081), falling back to the local `/data` key during rollout. The per-container
  `/data` key differed from Core's, so `weather_app`'s derived password never matched the role Core minted
  → the pool **silently fell back to the `postgres` superuser** (confirmed fleet-wide via boot logs).
  Now `weather_app` authenticates → the R173 least-priv DML-only request path is genuinely in effect.
  Fernet-at-rest untouched (separate `/data` key). Superuser fallback kept as a rollout safety net;
  Phase 2 fail-closes.

## 2026.6.75 — R143: constant-time token compare in _verify_internal (fleet sweep)

### Security
- **`api/licence.py::_verify_internal` now compares the Supervisor Bearer token with
  `hmac.compare_digest`, not `==`** (Rule 143 — `==` on a secret leaks length/content via timing).
  Fleet-wide R143 sweep (Store/Weather/SugarSense shared the same `==`). Defence-in-depth only — the
  Admin Ed25519 signature is the real authorisation (SEC-04).

## 2026.6.74 — SCAL-03: actually bump the base image to Python 3.12 + digest pin (WR-PS-080)

### Fixed
- **Base image was still `python:3.11-slim` despite the v.72 changelog claiming "Python 3.11 → 3.12".**
  The v.72 doc claim never matched the Dockerfile FROM line (a doc-vs-code mismatch, Rule 96). This
  commit actually swaps `FROM python:3.11-slim` → `python:3.12-slim@sha256:423ed6ab…199fbf` (fleet-index
  digest) and sets `pyproject.toml` ruff `target-version` + mypy `python_version` → 3.12. Weather is now
  genuinely off the Python 3.11 EOL runway (Hone SCAL-03) and digest-pinned. Isolated — no dependency
  changes. Verified by dev-deploy rebuilding on 3.12-slim + smoke.

## 2026.6.73 — SEC-01/04: Admin signed-licence receive-side (Hone PS-SEC-04 fleet adoption)

### Security
- **Both mutating licence paths now verify the Admin Ed25519 signature** (`api/licence.py`). Weather
  trusted the `/23`/loopback transport (`_verify_internal`) alone on `/api/licence/activate` and
  `/deactivate` — the "network-location = trust" pattern Hone **PS-SEC-04** flags and
  `SIGNED_LICENCE_CONTRACT §9-A` retires. Vendored `core/licence_verify.py` (byte-identical to
  `documentation/shared/`) + Admin pinned pubkey at `data/admin_signing_pubkey.json` (baked by the
  existing `COPY paddisense_weather/`). `activate` verifies via `_extract_licence` (handles the paste
  `code` AND Core's heartbeat `signed_licence`); `deactivate` verifies the signed instruction
  (`action ∈ {deactivate,revoke}`). Legacy-tolerant behind `WX_SIGNED_LICENCE_ENFORCE` (default
  off). Signature — not network position — is the trust boundary. `cryptography==48.0.1` pinned.
  Tests: `tests/test_licence_signed.py` (12 pass). Closes Weather slice of **WR-HONE-SEC-04**.

## 2026.6.72

**WR-PS-080 — Fleet Python 3.11 → 3.12 base-image bump (Hone SCAL-03 propagation).**

Python 3.11 EOL is October 2027, coinciding with commercial go-live. Python 3.12
EOL is October 2028, giving a full year of security-patch runway after go-live.
Admin (v2026.7.11, 2026-07-01) proved zero-code-change compatibility on 3.12 with
Admin's full 511-test suite green.

### Changed
- `Dockerfile`: `FROM python:3.11-slim` → `FROM python:3.12-slim@sha256:423ed6ab25b1921a477529254bfeeabf5855151dc2c3141699a1bfc852199fbf` (multi-arch index digest — amd64 + aarch64; verified against Admin's reference bump per WR-PS-080). Digest pin satisfies R155 / R197 provenance requirement.
- `pyproject.toml [tool.mypy]`: `python_version = "3.11"` → `"3.12"` (aligns type-checker with runtime).

### Notes
- `requirements.lock` was already 3.12-compatible (was regenerated at v.71 using
  the GSM venv which runs 3.12). No lockfile change needed.
- No application-code changes. Weather's dependencies (fastapi 0.136 / pydantic
  2.11 / uvicorn 0.46 / httpx 0.28 / psycopg2-binary 2.9 / jinja2 3.1 /
  python-multipart 0.0.31 / starlette 1.3) all support 3.12.
- Golden Rules v2.46 → v2.47 (Rule 113 ownership fan-out amendment) — Weather is
  now under G-Claude by default per W4_REGISTER + Rule 113 v2.47 amendment.

## 2026.6.71

**R155 CVE lift — regenerated requirements.lock closes 44 CVEs across 8 packages.**

pip-audit against the pre-existing `requirements.lock` (unchanged since ~v.60) surfaced 44 known vulnerabilities pre-release: **aiohttp 3.10.9 (32 CVEs, fix 3.14.1), urllib3 1.26.20 (5 CVEs, fix 2.7.0), brotli 1.1.0, msgpack 1.1.2, cryptography 48.0.0, idna 3.10, requests 2.32.4, setuptools 70.3.0**. Blocks R105 release-gate; hard release-blocker.

Root cause: 7 of 8 vulnerable packages were **legacy transitives from an older `requirements.txt`** and no longer pulled by any current direct dep (`fastapi 0.136.1`, `pydantic 2.11.4`, `uvicorn[standard] 0.46.0`, `httpx 0.28.1`, `jinja2 3.1.6`, `psycopg2-binary 2.9.12`, `python-multipart 0.0.31`, `starlette 1.3.1`). Regenerating with `pip-compile --allow-unsafe --generate-hashes` DROPPED them entirely. Only `idna 3.10 → 3.18` was a live transitive that needed bumping.

Post-regen: **pip-audit clean — "No known vulnerabilities found"**.

### Changed
- `requirements.lock` regenerated via `pip-compile --allow-unsafe --generate-hashes`. Went from ~113 pinned packages (many unreachable) to a slim, live-dep-only set.

### Notes
- Grower boxes currently on v.68 have all 44 CVEs already; shipping v.71 lifts them all.
- Python stays on 3.11 (fleet standard). Fleet-wide Python 3.12 bump is a separate Hone-driven initiative in progress; Weather takes it in a future coordinated cut.

## 2026.6.70

**W04 radar page removed (Hone CLOUD-02 close — Windy embed compliance).**

The W04 rain-radar page was 100% Windy embed via `<iframe src="https://embed.windy.com/…">`.
Windy's free embed licence is the strictest in the fleet:  personal /
educational / evaluation only. Removed rather than deferred to rollout — eliminates
one commercial-use question mark immediately, and no forecast/decision data is lost
(Open-Meteo Forecast + Ecowitt rain gauges cover what growers actually decide on).

### Removed
- `pages/desktop/radar.html` (133 lines) — Windy iframe + layer picker.
- `pages/mobile/radar.html` (126 lines) — mobile mirror.
- `/radar` GET route in `pages/__init__.py`.
- `Radar` sidebar link in `pages/{desktop,mobile}/base.html`.
- `Radar` mobile hub tile in `pages/mobile/hub.html`.
- `/radar` from `_PUBLIC_PATHS` in `main.py` (was a licence-gate bypass — no longer needed).
- `frame-src https://embed.windy.com` from the CSP header in `main.py`.
- `test_radar_page` in `tests/test_smoke.py` replaced with `test_radar_page_removed` — asserts the route no longer 200s (regression guard against accidental re-introduction).

### Retained
- `/api/v1/paddocks-proxy` (GeoJSON of farm paddocks) — the smoke test now
  no longer references "the radar page" but keeps the shape check for any future
  map layer that consumes the same payload.
- `/api/ha-location` and `/api/my-location` — used by settings + weather pages,
  not just radar.

### Docs
- `THIRD_PARTY_NOTICES.md` — Windy row removed from Embedded/CDN Libraries; the
  post-rollout trigger checklist now marks Windy as **REMOVED at v.70** (audit trail).
- `ARCHITECTURE.md` — Windy section replaced with a removal note.
- `CLAUDE.md` — External APIs table now shows Windy struck-through with "REMOVED
  v2026.6.70" callout.

### Compliance impact
- **Hone WR-HONE-CLOUD-02:** the Windy remediation item goes from OPEN to CLOSED
  (removed rather than paid-plan). Open-Meteo + Esri + RainViewer remain under
  pilot deferral per Peter 2026-07-02.
- **R105 release-gate:** verify-commit still clean (gate has no page-count invariant).

## 2026.6.69
### Changed
- **WR-PS-069 §5 close** — extracted required-env-var validation from the startup handler into a public `validate_config()` function per FLEET_PROCESS §5 canonical shape. Startup handler now calls `validate_config()` FIRST, before any background service kickoff (poller, DB init). Behaviour unchanged; structure aligned to fleet-wide gate.
- `pyproject.toml`: added `[tool.fleet] startup_module = "paddisense_weather/main.py"` per A-Claude steward call (explicit > probe; single gate code path).
- **Rules v2.44 → v2.46 walk**: v2.44→v2.45 R3 substrate correction (no code impact); v2.45→v2.46 ADR-012 §4 execution (R71 rewritten trunk-based, R72 amended, R116 RETIRED). CLAUDE.md + AUDIT.md updated to v2.46. Weather flipped to trunk-based this session (reconciliation merge `7ad563a` adopted 4 unmerged develop commits; local + origin `develop` deleted per §4.1).

## 2026.6.68
### Security
- **R144/WR-PS-066: `GET /api/licence` is now liveness-only.** The public,
  auth-exempt status endpoint (Core polls it without a token) was returning the
  full licence string plus `product`, `exp`, and `grower_id`. It now returns
  ONLY `{"enrolled": <bool>}`, matching the fleet-correct pattern (Farm/ASM).
  The auth-gated `_verify_internal` push/revoke path is unchanged.

## 2026.6.67
ADR-010 flip-readiness — cleared every verify-commit warning (dev bump; grower release stays v66).
### Changed
- R178/orphan-bindings: restructured to per-page `<script nonce>` blocks (base no longer wraps
  `{% block script %}`) so the orphan-bindings checker can see the already-wired `querySelectorAll`
  delegation — clears 9 false Class-A "orphan" findings. No behavioural change (handlers were
  already delegated; no inline `on*=`).
- R157: added behavioural CSRF test (`TestCsrf`, asserts 403).
- R17: re-synced `paddisense-tokens.css` byte-identical to master.
- R96/R118: CLAUDE.md → v2026.6.67 / golden_rules_version v2.42; AUDIT.md refreshed to v2.42.

## 2026.6.66
### Changed
- Rule 41 compliance for grower release: extracted all inline `style="..."` attributes to CSS classes (byte-identical declarations) + the exempt `--var` injection pattern for JS-computed values. Zero visual change; `verify-commit` now exits 0.

## 2026.6.65
### Fixed
- **Primary wind rose now updates when the hour filter (1/3/6/24 hr) changes.** `setWindRoseRange()` was selecting the active button by a stale `[onclick*=...]` selector (left over from the inline-handler → data-attribute migration); it matched nothing, threw, and `refreshPrimaryWindRose()` never ran. Now selects by `data-hours` with a null guard. (desktop + mobile)

## 2026.6.64
### Added
- **Open-Meteo Year-to-Date rain total** (+ corrected This Month): sums daily precipitation from Open-Meteo's archive API (Jan 1 -> today), cached ~6h. Open-Meteo is a forecast source with no running yearly total, and readings are purged after 7 days, so the archive API is the accurate source. The rain-details card now shows Year to Date for the forecast station.

## 2026.6.61
### Fixed
- Hotfix: `/api/my-location` needs `response_model=None` (FastAPI can't model `dict | JSONResponse`) — v60 failed to start. Same pattern as Core's endpoint.

## 2026.6.60
### Fixed
- **Radar "My Location" now works in the HA Companion app.** Browser geolocation is blocked inside the app's WebView (permission denied), so My Location now reads your device location from Home Assistant (which the Companion app already shares) via a new server-side `/api/my-location` endpoint — no WebView permission needed. Falls back with a clear prompt if HA has no GPS for you. (desktop + mobile)

## 2026.6.59
### Fixed
- **Spray/conditions banner had no background** — the status classes used gradients with undefined `--ps-*-dark` tokens, making the whole `background` invalid. Now a solid box using the master tokens (`--ps-success/warning/error/info/muted`); banner text uses `--ps-text`. (desktop + mobile)
- **Radar "My Location" failed silently** — `getCurrentPosition()` had no error callback, so over HTTP ingress (geolocation needs a secure context) nothing happened. Now reports permission-denied / needs-HTTPS / generic errors and restores the button. (desktop + mobile)
### Changed
- Radar layer nav: **Radar** is now first (before Rain) and the default layer.

## 2026.6.58 — 2026-06-21 (Fleet standardization: canonical theme-source + SESSION_PICKUP)

### Changed
- run.sh canonical theme-source (WR-PS-045); re-synced tokens.

### Added
- docs/SESSION_PICKUP.md (R191).

## 2026.6.57 — 2026-06-19 (Release compliance + theme fix)

- Fix mobile topbar `position:fixed` and content padding for master theme alignment.
- Update AUDIT.md to v57, assess rules 183-190 (Golden Rules v2.23). Zero new gaps.
- Update CLAUDE.md version and golden_rules_version to 2.23.
- Backfill CHANGELOG entries for v49-v56.

## 2026.6.56 — 2026-06-18 (Radar location buttons)

- Add Farm Location and My Location buttons to the radar top bar for quick map centering.

## 2026.6.55 — 2026-06-18 (Radar GPS marker + forecast colour fix)

- Show GPS position marker on radar map. Fix forecast date text colour using theme tokens.

## 2026.6.54 — 2026-06-17 (Station card source labels + wind rose UX)

- Add source labels (Local / Cloud API / Open-Meteo) on weather section cards. Wind rose collapsed by default. Fix Open-Meteo station data display.

## 2026.6.53 — 2026-06-17 (Open-Meteo station card)

- Add computed fields (Delta-T, dew point, apparent temperature) to the Open-Meteo station card.

## 2026.6.52 — 2026-06-17 (Button class fix)

- Fix white/unstyled buttons by applying `ps-btn-secondary` to size-only button elements.

## 2026.6.51 — 2026-06-17 (CSRF hotfix + button classes)

- Fix CSRF validation rejecting empty-body POST requests. Apply button theme classes.

## 2026.6.50 — 2026-06-17 (Security hardening + nonce CSP)

### Changed
- Full nonce-based CSP: 102 inline event handlers migrated to `addEventListener`. All inline `<script>` tags carry per-request nonce. `script-src` no longer includes `unsafe-inline`.
- CSRF Content-Type enforcement on all API mutation endpoints.
- 10 MB request body size limit (Rule 158).
- CDN integrity attributes on all external scripts (Chart.js, Leaflet).
- `docs/security/THREAT_MODEL.md` created with gap register.

## 2026.6.49 — 2026-06-17 (Audit refresh)

- AUDIT.md refresh to Golden Rules v2.20. No code changes.

## 2026.6.48 — 2026-06-16 (WR-PS-026 two-token PAT manager)

- Add canonical `pat_manager.py` (from GIS reference) to `core/` and wire `rotate_pat_on_startup()` into the FastAPI startup handler. Two-token model separates dev PAT (git operations) from Supervisor PAT (store repo URLs), so dev PAT rotation never disrupts addon updates.

## 2026.6.47 — 2026-06-16 (Least-privilege DB role)

- `_pool.py` now tries the `weather_app` role first (password derived from `/data/keys/master.key` via SHA-256), falling back to `postgres` superuser if the role is not provisioned. `_get_dsn()` preserved for migrations that require superuser privileges.

## 2026.6.46 — 2026-06-11 (Rule 32 + Rule 60 — close the gaps v.45's audit missed)

- **Rule 32 (audit every mutation).** Added `audit()` calls to the four POST handlers that were silently mutating without logging: `POST /refresh`, `POST /refresh-api-data`, `POST /api/licence/activate`, `POST /api/licence/deactivate`. Verify: 13 `audit(` callsites vs 11 mutation handlers (some handlers carry multiple paths).
- **Rule 60 (functions ≤50 lines).** Split three over-length functions:
  - `api_rain_history` (116 → 28 lines) — extracted `_validate_rain_history`, `_build_hour_rain_sql`, `_build_period_rain_sql` helpers.
  - `store_reading` (55 → 25 lines) — pulled the throttle-check out into `_throttled()` and replaced the manually-listed value tuple with a `_TYPED_READING_COLUMNS` constant unpacked via `*`.
  - `_read_station_sensors` (55 → 31 lines) — extracted the `station_alive` derivation into `_station_is_alive()`.
- Verify: `python ast` walk of `paddisense_weather/` shows zero non-exempt functions over 50 lines.
- **Honest correction.** v.45's AUDIT headline claimed "ZERO GAPS" against Golden Rules v2.2; a deeper walk surfaced these three real gaps plus Rule 47 (mobile padding implemented via base-template inline style rather than CSS media query — recorded as ⚠ Dispensation, intent satisfied, automated verify command fails). Headline updated to 105 ✓ / 0 ❌ / 13 ⊘ / 1 ⚠ / 1 watch.

## 2026.6.45 — 2026-06-11 (Golden Rules v2.2 — close Rule 133 / 137 / 138 gaps)

- **Rule 133 (single Supervisor adapter).** All `http://supervisor/...` HTTP calls now go through `core/helpers.py::supervisor_get(path, *, timeout, client=None)`. The previous direct `httpx.AsyncClient` calls in `api/ha.py` (`get_ha_location`, `read_all_entity_states`, `read_entity_value`) are gone; that module now only parses HA payloads. Verify: `grep -rn 'http://supervisor' paddisense_weather/ | grep -v core/helpers` = 0.
- **Rule 137 (acknowledged blocking IO).** `CLAUDE.md` now carries a "Known issues / acknowledged debt" section documenting the `psycopg2`-inside-`async def` pattern, why it's tolerable under single-process uvicorn, and the migration path (async driver / `run_in_executor`).
- **Rule 138 (explicit timeout + WARNING log + degrade).** Added explicit `timeout=` to the two clients that were relying on httpx default — `poller.py::_poll_loop` (30s for the full cycle) and `api/refresh` (15s for Open-Meteo). Upgraded the `paddocks_proxy` exception log from DEBUG to WARNING with structured fields so a sustained GIS / Core outage is visible. The `supervisor_get` adapter catches `httpx.HTTPError` / `OSError` and logs at WARNING.
- Housekeeping: dropped the v.43 `BUILD_SENTINEL` diagnostic comment from `routes.py` — its job (verifying the docker COPY layer was fresh) was done by the uninstall + reinstall.

## 2026.6.44 — 2026-06-11 (Rain history: pad to N buckets)

- Fix rain-history charts collapsing to a single bar when the requested window is longer than the data we have. Symptom: a fresh install with one month of readings showed the same "1 bar at 18 mm" regardless of whether the user picked 6m / 12m / 24m — filter visibly did nothing, and the summary said "Total: X mm (1 months)" no matter the selection.
- Fix: rain-history SQL now drives the result off `generate_series` and LEFT JOINs the actual data. Empty periods come back as `0.0` mm so the chart always shows N bars matching the active range button.
- Known limitation: for ranges that pre-date our first reading we can only show the running yearly accumulator total, not per-period breakdowns. The Ecowitt gauge keeps its own running totals but only reports current values, so we genuinely don't know how much fell in months we weren't tracking. Future work: a separate "pre-tracking" bar showing `rain_yearly − sum(known months)` so the full year total is visible.

## 2026.6.43 — 2026-06-11 (Force fresh supervisor build)

- Supervisor's docker build cache kept producing images with stale source even after multiple `/store/reload` + `/rebuild` cycles. Resolved by full uninstall of the addon and the repository entry, then re-add and re-install. Slug preserved (`449b641d_paddisense-weather`). Includes BUILD_SENTINEL diagnostic comment at the top of `routes.py` to confirm future builds pick up fresh source.

## 2026.6.42 — 2026-06-11 (force fresh rebuild)

- Same code as v.41. v.41 had `@router.get("/rain-history", response_model=None)` in source but the supervisor build cache kept loading the stale image (decorator without `response_model=None`) even after `/store/reload` + `/rebuild`. Bumping the version invalidates the BUILD_VERSION arg and the COPY-layer cache so docker rebuilds from fresh source.

## 2026.6.41 — 2026-06-11 (Per-metric history range buttons + rain aggregation endpoint)

- Range buttons in the per-stat history modal now adapt to the metric. Rain stats get natural-period ranges instead of the meaningless 3h/12h/24h applied to every metric:
  - Rain Event / Rain Today: 24h hourly · 7d daily · 30d daily
  - Rain Weekly: 4w · 12w · 26w
  - Rain Monthly: 6m · 12m · 24m
  - Rain Yearly: 12m by month · 5y by year
  - Wind Direction: 3h · 12h · 24h (trimmed — 30d scatter is unreadable)
  - Everything else: 3h · 12h · 24h · 7d (unchanged)
- New endpoint `GET /api/rain-history?station_id=X&bucket=hour|day|week|month|year&n=N`. Server-side aggregation (date_trunc + MAX of the natural-period accumulator) so the 5y-by-year view doesn't pull thousands of 5-min rows. Hour bucket uses a reset-aware LAG window over rain_daily so the chart still works across midnight.
- Frontend buttons are rendered dynamically in `showHistory()` from a per-metric `RANGE_OPTIONS` table; `loadHistoryData()` dispatches to either `/readings-history` (raw 5-min) or `/rain-history` (pre-aggregated) based on whether the active range has a bucket.

## 2026.6.40 — 2026-06-11 (Per-stat history chart styles)

- Each rain stat now opens its own history (Rain Event, Today, Weekly, Monthly, Yearly were all clicking through to `rain_daily`; now they pass their actual column).
- Rain history renders as a **bar chart of mm fallen per 5-min interval** computed from the accumulator delta. Reset-aware: when the accumulator drops to 0 (end of event / start of new day / week / month / year), the current value is treated as the new amount instead of producing a negative bar. Summary line shows `Total: X mm` instead of Min / Avg / Max.
- Wind Direction history renders as a **scatter chart** (no connecting line) with a fixed 0–360° y-axis. A line chart wraps confusingly between 359° → 1°.
- Everything else (temperature, humidity, Δ-T, feels like, dew point, wind speed, wind gust, solar, UV, pressure) stays a line chart.

## 2026.6.39 — 2026-06-11 (Per-station card rain layout + chart NaN axis)

- Per-station expanded card now shows Rain Event and Rain Weekly (previously only Today / Monthly / Yearly).
- Reorganised the per-station stat grid into two semantic columns per Peter: left = rain (Event / Today / Weekly / Monthly / Yearly) then Solar / UV / Pressure; right = temperature group (Temp / Humidity / Δ-T / Feels Like / Dew Point) then wind group (Speed / Gust / Direction). On mobile the two columns stack so rain stays a single contiguous block. Implemented as two `.stat-col` flex wrappers under the existing `.stat-grid` 2-column grid — no media-query gymnastics.
- Fix NaN on the history chart x-axis. The chart JS read `r.timestamp`; the history endpoint serialised the DB column as `recorded_at`. `_serialise_row` now exposes `timestamp` as an alias of `recorded_at` for backwards compatibility — chart `new Date(r.timestamp)` now resolves properly.

## 2026.6.38 — 2026-06-11 (API stations: event / weekly / monthly / yearly rain)

- Surface the missing rain accumulators on API (Ecowitt cloud) stations. Local stations have shown all five (`event`, `daily`, `weekly`, `monthly`, `yearly`) since the rain card was added; API stations only carried `daily` because the schema, poller, and endpoint had only ever wired that one column. The Rain Detail card was rendering blanks for the other four.
- Schema: `weather_readings` gains `rain_event`, `rain_weekly`, `rain_monthly`, `rain_yearly` NUMERIC(8,2) columns. Migration adds them idempotently via `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` (Rule 19 — wrapped per-column, rollback noted).
- Poller (`_poll_single_ecowitt_station`): extracts `rainfall.event` / `weekly` / `monthly` / `yearly` from the Ecowitt cloud response and inch→mm converts each.
- `store_reading` (`db.py`): writes the four new columns as typed values (Rule 13 FAIR data).
- `api_remote_stations`: returns the full `rain.{event,daily,weekly,monthly,yearly}` shape, matching the local-station response.
- Existing DBs: migration runs at addon startup. Old rows have NULL for the new columns until the poller writes the next reading.

## 2026.6.37 — 2026-06-11 (NaN on API-station wind direction graphs)

- Fix wind direction returning as a string from `/api/remote-stations` (e.g. `"107.0"` instead of `107.0`). Every other column went through `_to_float`; this one was passed straight from the DB row. Charts that did arithmetic on the value rendered NaN.
- Now `_to_float(row["wind_direction"])` matches the rest of the columns.

## 2026.6.36 — 2026-06-11 (Freshness indicator per station)

- Add "Last: X ago" / "No data yet" badge to every station card in W01. Surfaces *when* the underlying gauge last sent fresh data (HA `last_updated` for local stations, DB `recorded_at` for API stations) so a user can spot a stale source even when the value still displays.
- Backend: `_freshest_entity_last_updated` helper added to `_assemble_local_station`; `/api/local-stations` and `/api/remote-stations` both now expose `last_data_at` (ISO timestamp).
- Frontend: `renderStationCards` (desktop + mobile) renders the badge using the existing `timeAgo` helper, next to the offline badge in the card header.
- Diagnostic value: lets the user tell "this station is just sitting in steady weather" apart from "this station hasn't reported in days even though HA still has a value" without having to dig through DB or HA Developer Tools.

## 2026.6.35 — 2026-06-11 (Ecowitt credentials always showing "Not configured")

- Fix settings page showing "Not configured" for Ecowitt API credentials even after a successful save. Frontend `loadProviderStatus` was checking `d.configured` (a field that doesn't exist in the response) and `d.app_key_preview` (also doesn't exist). Backend `/api/ecowitt-keys` GET returns `{has_keys, app_key_set, api_key_set}`. Save was always landing in `wx_config`; the display just never reflected it.
- Fix: frontend now checks `d.has_keys`, drops the non-existent preview reference, hides the form on success.
- Note: this is a display-only fix. If your API station still shows offline with no sensor data after upgrading, that's a separate issue — check the station's IMEI is set on its slot and that the Ecowitt cloud account actually has data for that IMEI.

## 2026.6.34 — 2026-06-11 (Steady-weather offline bug — widen liveness window)

- Fix grower-box bug confirmed in prod (Peter + P-Claude): a working gauge with steady weather (no value changes for >15 min) was misclassified as offline because v.33's station-level liveness check used the same 15-min `last_updated` threshold as the per-entity check. HA's `last_updated` only ticks when a value CHANGES, so a working gauge in steady weather can have every entity sit at the same `last_updated` for hours.
- Fix: introduce `LIVENESS_THRESHOLD_MINUTES = 1440` (24h) for the station-level check. Per-entity check unchanged (15 min). `_is_stale()` now takes an optional `threshold_minutes` kwarg. `_read_station_sensors` calls `_is_stale(..., threshold_minutes=LIVENESS_THRESHOLD_MINUTES)` for the `station_alive` computation only — once alive, the per-entity readers bypass staleness as before.
- KDP-007 still triggers: gauges silent for >24h still return None for every reading. The 24h window is the trade-off between "kills working gauges in steady weather" (15-min, too tight) and "shows multi-day frozen values as live" (no check, too loose).
- KDP-010 updated to reflect the threshold-vs-bypass distinction.

## 2026.6.33 — 2026-06-11 (Per-sensor cadence jitter — broaden the fix)

- Extend v.32's accumulator fix to ALL sensor types. Verified on Peter's now-working gauge: pressure (last_updated 2 min ago) and solar (3 min) came through, but temp / humidity / wind were 19 min old — past the 15-min staleness threshold even though the gauge IS reporting. Ecowitt's HA integration reports different sensors on different cadences (pressure every 2-3 min, temp/humidity/wind every ~5 min) and network jitter occasionally pushes individual sensors past 15 min.
- Fix: station-level liveness. If ANY entity on the station is fresh (within the 15-min window), the gauge is alive and ALL its readings are trusted regardless of per-entity staleness. KDP-007 preserved: if EVERY entity is stale, station is offline and all readers return None.
- All five readers (`entity_float`, `entity_temp_c`, `entity_wind_kmh`, `entity_pressure_hpa`, `entity_rain_mm`) now accept `bypass_staleness` kwarg.
- KDP-010 updated to reflect broader pattern.

## 2026.6.32 — 2026-06-11 (Rain accumulator staleness fix)

- Fix rain totals hidden from W01 / W08 between rain events. Root cause: KDP-007 staleness guard (added v.27/v.28) used a uniform 15-min `last_updated` window for all entities, but rain accumulators (`daily_rain`, `weekly_rain`, `monthly_rain`, `yearly_rain`, `event_rain`) only tick when raindrops fall. A working gauge that hadn't seen rain in 15 min looked stale → all rain readings null → frontend hid the rain card.
- Fix: `entity_rain_mm` + `_entity_value_unit` now accept `bypass_staleness=True`. `_read_station_sensors` sets this flag when any continuous sensor (temp / humidity / wind_speed) on the same station is fresh — the gauge is alive and the cached accumulator value is the gauge's actual month/week/year-to-date. Continuous-sensor staleness guard unchanged (KDP-007 preserved).
- Logged as KDP-010 in `documentation/contracts/KNOWN_DEFECT_PATTERNS.md`.

## 2026.6.22 — 2026-06-04 (W08 spray station data fix)

- Fix spray page crash: `/api/local-stations` returns stations as a keyed object not array; `bestLocalStation` called `.filter()` on it causing TypeError
- Fix station property paths: `station.outdoor.temperature` / `station.wind.speed` not flat `station.temperature` / `station.wind_speed`

## 2026.6.21 — 2026-06-04 (Bug fixes)

- Fix windrose + wind chart canvas: CSS `var(--ps-*)` tokens don't resolve in Canvas context; replaced with `getComputedStyle` resolved values — centre text was white-on-white
- Fix W04 radar: missing `paddisense-tokens.css` link made all `var(--ps-*)` tokens undefined (white buttons, broken colours)

## 2026.6.20 — 2026-06-04 (W08 Spray Conditions)

- New page W08: Spray Conditions — Delta-T, wind, inversion assessment + 5-day outlook

## 2026.6.19 — 2026-06-04 (Pass F — semantic colour tokens, last real gap)

Closed **Rule 14** for semantic UI colours.  Mechanical sweep of
templates replacing hex literals with `var(--ps-*)` tokens.

### Sweep map

| hex literal | → token |
|---|---|
| `#22c55e` / `#16a34a` (green) | `var(--ps-success)` |
| `#86efac` (light green) | `var(--ps-success)` |
| `#f59e0b` / `#d97706` (amber) | `var(--ps-warning)` |
| `#fcd34d` (light amber) | `var(--ps-warning)` |
| `#ef4444` / `#dc2626` (red) | `var(--ps-error)` |
| `#fca5a5` (light red) | `var(--ps-error)` |
| `#3b82f6` / `#60a5fa` / `#2563eb` / `#1d4ed8` (blue) | `var(--ps-info)` |
| `#94a3b8` / `#64748b` / `#475569` (slates) | `var(--ps-muted)` |
| `#cbd5e1` / `#f8fafc` / `#e2e8f0` (light text) | `var(--ps-text)` |
| `#1e293b` (panel) | `var(--ps-card-bg)` |
| `#334155` (border) | `var(--ps-card-border)` |
| `#0f172a` (page bg) | `var(--ps-bg)` |

### Remaining hex (intentional, not gaps)

- **Pure `#000` / `#fff`** — text contrast over coloured rating
  badges and gradient bars.  Standard practice; not a token issue.
- **Data-visualisation palettes** in `weather.html` — temperature
  band gradients, wind-speed colour scales, rain heatmap.  These
  are scientific palettes mapping continuous data ranges to colour,
  not semantic UI colours.  Rule 14's intent is semantic-UI; data-viz
  palettes are a separate category that's allowed to use hex.  Could
  promote to dedicated `--ps-viz-*` tokens in a future palette
  refresh, but no semantic violation today.

### Rule 66 (no inline styles) — partial-by-design

- Static stylistic `style="..."` attributes that were trivially
  utility-class-replaceable have been migrated in earlier passes
  (`.hint-sub`, `.map-picker`, `.regional-check`, etc).
- Remaining inline styles fall into two categories that the rule
  doesn't really target:
  - **Dynamic data-driven styles** set from JS (e.g.
    `style="background:" + rainBg(rain)`) where the colour
    encodes the value.  Standard data-viz pattern.
  - **Display toggles** (`style="display:none"`).  Inline because
    the JS sets/unsets them imperatively.
- Closed for static stylistic markup; documented for the dynamic
  cases.

### Headline

**100 ✓ / 0 ❌ / 12 ⊘ / 1 watch (of 107 rules walked).**

Zero gaps.  The single "watch" item is Rule 19 (W01 weather.html
is ~1900 lines combining current + forecast + station cards on one
page).  It's borderline — strictly one page, no JS tabs — and
auto-resolves if the planned UI work splits W01.  Carried forward
explicitly rather than claimed as closed.

## 2026.6.18 — 2026-06-04 (Pass H — Rule 6 admin UIs + endpoint contract suite)

Closed **Rule 6** (Admin self-service via UI).

### New admin pages

- **W06 `/admin/audit-log`** — paginated viewer for `wx_audit_log`.
  Mobile + desktop variants.  Most recent first, prev/next pagination
  (50 per page desktop, 20 mobile).  Reads `details` JSONB directly.
- **W07 `/admin/system-status`** — addon health roll-up.  Cards:
  Addon (version, db_ok, audit entries), Backup (retention, count,
  last), Errors (in buffer), Perf (tracked endpoints).  **Backup
  retention is now configurable from the UI** (1–365 days, persisted
  via `wx_config`) — was hardcoded `RETAIN = 30`.

### New admin endpoints

- `GET  /api/v1/admin/backup-config` — current retention + last-backup
- `POST /api/v1/admin/backup-config` — set retention (range-validated,
  audit-logged Rule 29)
- `GET  /api/v1/admin/audit-log?limit=N&offset=M` — paginated
  `wx_audit_log` reader, limit clamped to 200
- `GET  /api/v1/admin/system-status` — health roll-up

All four are admin-role gated and `response_model=None` (Rule 95
caught a `dict | JSONResponse` FastAPI decorator bug during the
pass — same shape that bit v.4/v.5/v.15).

### Sidebar

Mobile + desktop `base.html` now link to "System Status" and "Audit
Log" under the existing Admin section.

### Endpoint contract test suite (Peter's directive 2026-06-04)

> "instead of looking in each drop down in the UI to verify"

New `TestEndpointContracts` class — one test per endpoint that backs a
UI dropdown / list / card, asserting the response shape.  Covers
W01, W02 (already), W03, W04, W05 (already), W06, W07.  Plus a
`TestPageContracts` class that asserts each page's HTML contains
the element IDs its JS depends on (so a template refactor that
renames an element-id breaks loudly, not silently).

### Headline

99 ✓ / 1 ❌ / 12 ⊘ / 1 watch (of 107 rules).

Only Rule 14 + 66 (hex literals + inline styles sweep) remains
before zero gaps.  Pass F next.

## 2026.6.17 — 2026-06-04 (banner showing 55°C on rain-only gauge — Peter caught)

Two related bugs in the spray-banner station picker.

### Bug 1 — picker accepts a rain-only gauge as primary

The picker walked `priority` and took the first station with
`outdoor.temperature != null`.  But on a rain-only Ecowitt gauge,
HA still exposes a `sensor.<prefix>_outdoor_temperature` that reads
the gateway's interior temperature (~55°C near electronics).  So
the banner picked the rain gauge and showed 55°C even though the
actual outdoor temp was ~10°C.

Fix: `/api/local-stations` now returns a `primary_eligible` flag per
station — `True` only when **temperature AND humidity AND wind speed**
are all populated.  A rain-only unit fails the wind check.  Frontend
picker prefers `primary_eligible` stations, falls back to
temp+wind-populated, then to any temp as a last resort.

### Bug 2 — units not honoured

`entity_float()` returned the raw HA value with no unit awareness.
If the Ecowitt HA integration was configured in imperial, a value of
55 (°F) displayed as 55 (°C).  55°F = 12.8°C — matches Peter's "about
10".

Fix: new unit-aware readers in `api/ha.py`:
- `entity_temp_c()`  — converts °F → °C
- `entity_wind_kmh()` — converts mph / m/s / knots → km/h
- `entity_rain_mm()` — converts in → mm
- `entity_pressure_hpa()` — converts inHg / mbar / kPa → hPa

Source unit read from `attributes.unit_of_measurement`.  Default
assumption: already canonical (°C / km/h / mm / hPa).
`/api/local-stations` now uses these for every reading.

## 2026.6.16 — 2026-06-04 (Pass G — JSONB migration, full Rule 10 closure)

Closed **Rule 10** fully.  Five TEXT-holding-JSON columns migrated
to JSONB with idempotent `IF column_type = 'text' THEN ALTER … USING
value::jsonb` blocks in `schema.sql`:

- `wx_audit_log.details`
- `weather_forecast.data`
- `weather_stations.config` (with `NULLIF(value, '')::jsonb` guard
  for empty strings)
- `weather_stations.data`
- `weather_readings.data`

Writers add `%s::jsonb` cast on the affected parameters; readers
already used the `isinstance(row[col], str)` guard so they remain
JSONB-tolerant for the transition.

Audit log entries now indexable by JSON keys (e.g. `details->>
'station_id' = 'local_1'`) — sets up the future audit-log viewer
(Pass H).

### Headline

98 ✓ / 2 ❌ / 12 ⊘ / 1 watch (of 107 rules).

## 2026.6.15 — 2026-06-04 (Pass E — mypy strict)

Closed **Rule 86**.  `pyproject.toml [tool.mypy]` now has
`disallow_untyped_defs = true` (was `false`).  Flipping the flag
surfaced 26 untyped-def errors — all closed.

### Annotated

- `main.py` — added return types to 14 functions: middleware
  (`Response` via the new `from starlette.responses import Response`
  import + `RequestResponseEndpoint` for `call_next`), the
  `unhandled_exception_handler`, `/health`, three `/api/{errors,perf}`
  admin endpoints, login/logout/licence/root route handlers, `startup`.
- `perf_tracker.py` — `record_request -> None`
- `error_tracker.py` — `record_error -> None`, `clear_errors -> None`
- `api/poller.py` — `_ecowitt_val(*keys: str)`, `_safe_idx(default:
  object) -> object`
- `api/routes.py` — `_to_float(value: object)` with one targeted
  `# type: ignore[arg-type]` (mypy can't narrow `object` through the
  try/except — comment in the function explains why)

### Rule-95 win during this pass

The three `/api/{errors,perf}` admin endpoints returned
`dict | JSONResponse` (same union shape that bit us in v.4/v.5).
FastAPI tried to derive a Pydantic response model from the union at
decorator time and crashed.  The W03-save regression test caught it
instantly — exactly the bug class Rule 95 protects against.  Fixed
by adding `response_model=None` to the three decorators.

### Headline

97 ✓ / 3 ❌ / 12 ⊘ / 1 watch (of 107 rules).

Gates clean.  All 34 tests pass.

## 2026.6.14 — 2026-06-04 (Pass D — DRY rule-engine + admin JS into `static/`)

Closed **Rules 62 + 13** (the JS-duplication arm of Rule 13).
Extracted ~300 lines of duplicated logic from mobile + desktop
W02/W05 templates into two shared modules.

### New shared modules

- **`static/burn_rules.js`** — `BurnRules` namespace.  Exposes
  `RATING_ORDER`, `RATING_LABEL`, `windDir()`, `evaluateRule()`,
  `evaluateHour()`, `load()` (fetches `/api/v1/burn-rules`).
- **`static/burn_rules_admin.js`** — `BurnRulesAdmin` namespace.
  Exposes `init({ layout: 'mobile' | 'desktop' })` and `loadRules()`.
  Hoists `openModal`, `closeModal`, `saveRule`, `toggleEnabled`,
  `deleteRule`, `onKindChange` onto `window` so inline-onclick
  handlers in the modal HTML resolve.  Picks the right card layout
  internally based on the `layout` option.

### Template diet

- `pages/{desktop,mobile}/burn_forecast.html` — replaced 90 lines
  of engine boilerplate with 4 short `var x = BurnRules.x;` aliases
  + a single `BurnRules.load()` call.  Mobile dropped from ~480 to
  ~330 lines, desktop from ~400 to ~250.  Per-template rendering
  (card vs grid) still lives in the template — engine is shared,
  presentation is not.
- `pages/{desktop,mobile}/burn_rules_admin.html` — replaced 180
  lines of CRUD JS with `BurnRulesAdmin.init({ layout: 'desktop' })`
  / `init({ layout: 'mobile' })`.  Desktop dropped from 294 to 115,
  mobile from 300 to 119.  Both inherit Rule 107 path-versioned URLs.

### Test maintenance

- `test_w02_location_js_loads_before_inline_script` regression test
  updated to match Rule 107 URL shape (`location.js` substring search
  instead of `static/location.js`) — same intent, same protection.
- All 34 tests pass.

### Headline

96 ✓ / 4 ❌ / 12 ⊘ / 1 watch (of 107 rules).

## 2026.6.13 — 2026-06-04 (3-layer cache busting — GIS pattern)

Adopted GIS's three-layer cache-busting pattern to defeat corporate
proxies and HA Companion app caches that ignore `?v=` query strings.
This was the root cause of v.12's satellite tiles not showing on
Peter's locked-down browser.

**Layer 1 — Path-based versioning in templates.** All
`<link href="/static/...?v={{ version }}">` and
`<script src="/static/...?v={{ version }}">` references rewritten to
`/static/v{{ version }}/...`.  Each version bump produces a
completely new URL that proxies can't deduplicate.

**Layer 2 — Server-side `Cache-Control: must-revalidate`** on every
`/static/*` response.  Browsers re-check the URL on every load;
the unchanged-URL case returns 304, the changed-URL case returns
the new bytes.

**Layer 3 — URL-rewrite in auth middleware** strips the
`/v{version}/` segment back to `/static/file.ext` before the
mounted `StaticFiles` handler sees it, so the filesystem doesn't
need versioned copies.

**Bonus — `Cache-Control: no-store` on HTML responses** in
`SecurityHeadersMiddleware`.  Without this, a cached HTML page
would keep requesting the OLD `/static/v{OLD_VERSION}/` URLs even
after we redeploy.

Reference: `paddisense_gis/main.py` lines 154-166 + base.html.

## 2026.6.12 — 2026-06-04 (W03 map picker: satellite tiles)

Swapped OpenStreetMap street tiles for Esri World Imagery satellite/
aerial.  Better for siting weather stations in ag context — paddock
boundaries are visible at zoom 17–18, no API key required, no ToS
blocker for grower use.

## 2026.6.11 — 2026-06-04 (W03 map picker + typed station position + GSM sync prep)

First UI work after the rule-audit baseline.  Engineering-mindset
(Rule 97) — pay the migration cost once: typed lat/long columns +
opt-out toggle + sync-state column all landing together so the
future Weather → GSM regional sync (see
`documentation/contracts/WEATHER_GSM_SYNC.md`) doesn't need
another schema migration.

### Schema (Rule 10 partial closure)

- `weather_stations` gets typed `latitude NUMERIC(10,7)`,
  `longitude NUMERIC(11,7)`, `include_in_regional BOOLEAN NOT NULL
  DEFAULT TRUE`, `last_synced_at TIMESTAMPTZ`.
- Idempotent additions via `ALTER TABLE … ADD COLUMN IF NOT EXISTS`
  in `schema.sql`.
- One-time backfill from the legacy JSON `config.latitude/longitude`
  blob for pre-v.11 API-station installs.

### Backend

- `_extract_position()` helper in `api/routes.py` validates
  lat ∈ [-90, 90], lng ∈ [-180, 180], non-numeric rejected with
  400 (Rule 65 specific error handling).
- `upsert_station()` accepts typed lat/long + `include_in_regional`
  and persists into the new columns (no longer needs the legacy
  JSON keys).
- `get_station()` / `get_all_stations()` return the typed columns
  on every row.
- Audit log carries lat/long/include in `details` (Rule 29).

### UI — W03 settings (mobile + desktop)

- New Leaflet map picker embedded in both station-edit modals
  (was missing on local-station; was lat/lng-only on API-station).
- Click anywhere on the map → marker moves + lat/lng inputs
  auto-update.  Drag marker for fine-tune.  Inputs editable
  (paste-from-external still works).
- **"Use my location"** button reuses the existing `loadLocation()`
  helper from `static/location.js` (device GPS → HA → fallback).
  Rule 62 DRY.
- **"Use farm location"** button reads HA-configured lat/long.
- New **"Include this station in regional data sync to GSM"**
  checkbox per station — grower-controlled opt-out for the future
  Weather → GSM sync (default: opted in).
- Rule 76: 48px touch targets, 15px+ font.  Rule 66: extracted
  utility CSS classes (`.map-picker`, `.latlng-row`, `.map-actions`,
  `.regional-check`, `.hint-sub`) — no inline styles added.
- Rule 14: map controls use `--ps-*` tokens (border, background);
  marker uses Leaflet default for now (semantic-token sweep is
  Pass F).

### Tests

- 4 new tests in `TestStationPosition`: rejects out-of-range lat,
  out-of-range lng, non-numeric lat; accepts valid position with
  round-trip verification of typed columns + `include_in_regional`.
- All previous tests still pass (3 regressions, burn-rules CRUD,
  health, auth, pages).

### Contract + cross-Claude WR

- New design contract `documentation/contracts/WEATHER_GSM_SYNC.md`
  describing the two-plane sync (control plane via Admin-heartbeat
  envelope; data plane via direct HMAC-signed batch POST).
- Filed `WR-AS-008` to G-Claude (GSM) for the ingest endpoints +
  TimescaleDB hypertable + per-business aggregation view + future
  IDW-interpolated regional map UI.

### Audit progress

Headline: 94 ✓ / 5 ❌ / 12 ⊘ / 1 watch (of 106 rules).

Closed this pass: Rule 10 (partial — `weather_stations` now
typed; `wx_audit_log.details` + `weather_forecast.data` still TEXT,
queued for Pass G).

## 2026.6.10 — 2026-06-04 (Pass C — tests for burn-rules CRUD + 3 regressions)

Closed:
- **Rule 73** — W05 burn-rules CRUD now has a full round-trip test
  (create → list-shows-it → update → verify → delete → verify-gone).
  Also covers create-validates-kind, create-validates-params,
  delete-404-on-unknown, and the UNIQUE-name constraint
  (Rule 53 enforcement).
- **Rule 87** — Smoke coverage extended to burn-rules CRUD endpoints
  and the W05 page render.
- **Rule 95** — Three regression tests for known-fixed bugs:
  - `test_w03_save_null_id_does_not_500` (v.4)
  - `test_w02_location_js_loads_before_inline_script` (v.7,
    template-shape check on both mobile + desktop base.html)
  - `test_backup_no_logrecord_reserved_attrs` (v.6, scans the whole
    package for `extra={"<reserved-key>": ...}` patterns)

All 3 regression tests pass at v.10.

Headline: 93 ✓ / 6 ❌ / 12 ⊘ / 1 watch (of 106 rules).

## 2026.6.9 — 2026-06-04 (Pass B — CLAUDE.md rewrite, API envelope doc)

Closed:
- **Rule 98** — Full CLAUDE.md rewrite against v.9 code.  Architecture
  tree matches actual filesystem; routes match actual decorators;
  schema table matches `schema.sql`; rule count 106 (was 76); version
  current.
- **Rule 84** — All 11 required sections present (Rule 84
  enumeration).  Deploy Flow references Rules 103+104 explicitly.
  Critical Rules section reconciled — `schema.sql` discipline
  rewritten to accurately describe the idempotent CREATE TABLE IF
  NOT EXISTS + DO $$ blocks pattern, plus the LogRecord
  reserved-attribute reminder.
- **Rule 64** — Documented the 3-shape API envelope pattern in
  CLAUDE.md: list endpoints `{"<key>": [...]}`; mutations
  `{"ok": true, ...}`; status/data queries return bare objects.

Headline: 90 ✓ / 9 ❌ / 12 ⊘ / 1 watch (of 106 rules).

## 2026.6.8 — 2026-06-04 (Pass A — drive audit gaps toward zero)

Per Peter's directive "Weather sets the standard — no gaps no matter
how we search", working through `docs/AUDIT.md` gap list across
multiple passes.  Pass A closes the audit-itself and quick-win gaps.

### Closed gaps

- **Rule 53** — `wx_burn_rules.name` now `UNIQUE`.  Idempotent
  backfill squashes any existing duplicates by keeping the lowest id
  before adding the constraint (handled in `schema.sql`).
- **Rule 62** — Deleted dead `core/audit.py::log_audit()`.  Single
  canonical `helpers.py::audit()` (DB-persisting per Rule 29) is the
  only audit function.  grep confirmed zero imports of the deleted
  module before removal.
- **Rule 70** — Aspirational TODOs ("Frost alerts not built", "Degree
  days not populated", "Hourly forecast not built", "Smoke planner not
  built", "Reading retention configurable") moved from `CLAUDE.md`
  Known Issues into new `paddisense-weather/TODO.md`.  CLAUDE.md now
  points at TODO.md + docs/AUDIT.md per Rule 98.
- **Rule 105** — `docs/AUDIT.md` is the live compliance baseline,
  linked from top of `CLAUDE.md` per the new rule landed 2026-06-04.

### Self-audit corrections

Re-walked the v.7 baseline applying the discipline from
`feedback_rule_audit_before_ship.md` ("find AT LEAST one gap; a 0-gap
verdict means the audit was wrong"):

- Headline updated: 104 → 106 rules walked (Rules 105 + 106 added
  2026-06-04).
- Rule 6 escalated ⚠ → ❌ (backup retention + selftest + audit-log
  viewer have no UI).
- Rule 73 escalated ⚠ → ❌ (no CRUD round-trip tests for W05).
- Rule 64 evidence enriched — 3-pattern consistency documented.
- Rule 91 escalated ⊘ → ⚠ (shared files have non-naming functional
  diffs vs canonical Livestock; needs Weather→Livestock WRs).
- Rules 85 + 88 freshly re-verified against v.7 source (ruff 0,
  bandit HIGH 0).

### Headline

v2026.6.7 baseline: 79 ✓ / 13 ❌ / 12 ⊘ of 104 rules.
v2026.6.8 Pass A: **87 ✓ / 12 ❌ / 12 ⊘ / 1 watch of 106 rules.**

Passes B–I remaining: CLAUDE.md rewrite (98+84), tests (87+95+73),
JS DRY (62+13), mypy strict (86), theme tokens + inline-styles (14+66),
JSONB migration (10), admin self-service UIs (6), main.py/W01 splits
(67+19).

## 2026.6.7 — 2026-06-03 (hotfix W02 stuck on Loading)

W02 burn forecast was stuck on "Loading forecast…" because
`location.js` was loaded AFTER the inline `<script>` that calls
`loadData()` at module load.  `loadLocation()` was undefined when
`loadData()` ran, throwing a synchronous ReferenceError before the
Promise chain was constructed (so the `.catch` never fired and the
"Loading" placeholder never got replaced).

Fix: moved `<script src="static/location.js">` to **before** the
inline script block in both `mobile/base.html` and `desktop/base.html`.
Now `loadLocation` is defined when the inline script runs.

## 2026.6.6 — 2026-06-03 (W02 burn forecast mobile redesign + per-site rules)

### Burn forecast — multi-variable rating engine

The W02 burn-forecast page now combines mixing height, wind speed,
wind direction, humidity, and temperature into one BURN OK / CAUTION
/ DON'T BURN rating per hour.  Worst-case wins: any single rule
marking the hour poor wins the final rating.

- **New table `wx_burn_rules`** with two default rules seeded on first
  install: mixing height (good ≥1600m, marginal ≥1500m) and wind speed
  (marginal ≥20 km/h, poor ≥30 km/h).  Defaults can be edited or
  deleted from the new admin page.
- **New CRUD API** `/api/v1/burn-rules` (GET, POST, PUT, DELETE).
  Validates per-kind params at the boundary.  Every mutation is
  Rule 29 audit-logged.
- **New page W05** `/burn-rules-admin` — list, add, edit, toggle,
  delete rules.  Type-aware form (mixing_height, wind_speed,
  wind_direction_exclude, humidity, temperature).  Linked from sidebar.

### Mobile W02 redesign

- **Card-per-hour layout** replaces the 5-column cramped grid.
  Each card shows time, mixing-height bar, BURN OK / CAUTION /
  DON'T BURN rating, and a one-line wind summary (e.g.
  `12 km/h NW · gust 18`).  Tap to expand for full breakdown
  (temperature, humidity, direction degrees, all failing rules).
  Current hour auto-expanded.
- **Why-failed annotations** — each card surfaces which rules
  marked the hour CAUTION or DON'T BURN, so the grower trusts
  the model rather than overriding blindly.
- **Rule 76 fonts + touch targets** — 15px+ labels, 48px refresh
  button.
- **Dropped hardcoded "Leeton NSW"** in favour of dynamic location
  resolution.

### Desktop W02

- Same rule engine, wide grid preserved.  Added rating cell and
  why-cell (hover tooltip + inline text) so the failure reason is
  visible without expansion.

### Location resolution (new `static/location.js`)

- Shared helper: device GPS (`navigator.geolocation`) → HA home zone
  (`/api/ha-location`) → hardcoded fallback.  Used by W02 mobile
  and desktop; reusable for W01 / W04 in future passes.
- Subtitle shows the active source (`Device location` / `Farm
  location` / `Default location`) so the grower knows where the
  forecast is from.

### Other

- **backup.py LogRecord collision** — `extra={"filename": ...}`
  collided with the LogRecord built-in `filename`, throwing
  `KeyError` on the first backup attempt.  Renamed to
  `backup_name` (lines 101 and 133).

### Verified
- ruff: 0 violations across 27 source files
- mypy: 0 errors across 27 source files
- bandit HIGH: 0
- All 4 burn-rules routes register; v1 aliases auto-mirror;
  W05 admin page route resolves

### Release flow (Rule 81)
- This commit is pushed to source `main` only.
- Public/paddisense-weather/config.yaml bump + GHCR build dispatch
  will happen **only after Peter has verified the dev install
  behaves correctly**.

## 2026.6.5 — 2026-06-03 (hotfix v.4 dev-test crash)

v.4 crashed at startup on the dev box (Rule 81 dev-test caught it):

```
fastapi.exceptions.FastAPIError: Invalid args for response field!
... that dict | starlette.responses.JSONResponse is a valid Pydantic field type.
```

The `dict | JSONResponse` return-type annotations I added to satisfy
mypy made FastAPI choke at decorator time — it tries to derive a
Pydantic response model from the return type and the union isn't
valid as one.

**Fix:**
1. Added `response_model=None` to the 4 affected decorators
   (`/station-config/{id}`, `/local-station/save`, `/api-station/save`,
   `POST /ecowitt-keys`).
2. Extended `_add_v1_aliases()` to propagate the original route's
   `response_model` setting onto the v1 alias (without this, the
   alias re-trips the same FastAPI error on registration).

No other behaviour change vs v.4.  Audit table in
`docs/AUDIT_v2026_6_4.md` still applies.

## 2026.6.4 — 2026-06-03 (full 102-rule audit + W03 save fix)

> v2026.6.3 was tagged "full compliance — rules 29, 59, 60, 92, 93"
> but verification showed 3 of 5 were not actually closed.  Per
> `feedback_rule_audit_before_ship.md`, v.4 ships with an explicit
> rule-by-rule audit table (`docs/AUDIT_v2026_6_4.md`) and closes
> every real gap.

### Fixed — visible bugs on grower box
- **W03 save → 500 (Rule 65).** `data.get("id", "").strip()` crashed
  with AttributeError when the client sent `id: null` (any "new" slot
  before the modal binds it).  Now guarded:
  `(data.get("id") or "").strip()`.  Same fix on `/local-station/save`,
  `/api-station/save`, `/ecowitt-keys`.  Wrapped `request.json()` in
  try/except to return a clean 400 on malformed bodies.
- **W03 save → wrong station_id format.** Frontend was sending
  `{id: slot}` but the canonical format (matching `removeStation`) is
  `type + '_' + slot`.  Fixed in `pages/{desktop,mobile}/settings.html`.
- **W03 save → "Error" toast on success.** Frontend checked
  `d.status === 'ok'` but backend returned `{"ok": true}`.  Frontend
  now accepts both shapes; backend also returns `{"ok": true,
  "status": "ok"}` for backward compat.
- **`run.sh:45` `[: Illegal number: 23`.** Gate 2/3/4 count
  extraction was using `grep -o "[0-9]*"` which matched every digit
  run including unrelated numbers — replaced with `grep -oE "Found [0-9]+"
  | grep -oE "[0-9]+" | head -1`.  Gate 4 used `grep -c "High:"` which
  counted both severity AND confidence sections; replaced with
  `awk '/Severity: High/ {n++} END {print n+0}'`.
- **Gates 2-4 running on grower box (Rule 90).** Now skipped when
  `WX_ADMIN_KEY` is empty (production install).  Gate 1 syntax stays
  on every box per Rule 37.

### Closed — real Golden Rule gaps
- **Rule 29 (audit log every mutation).** New `helpers.audit()`
  wrapper extracts actor from `request.state.user` and never breaks
  the surrounding mutation if logging fails.  New `wx_audit_log`
  table.  Audit calls added to all station-save / station-delete /
  ecowitt-keys endpoints.
- **Rule 39 (daily backup).** New `paddisense_weather/backup.py`:
  `create_daily_backup()` startup catch-up + `daily_backup_loop()`
  background task at `WX_BACKUP_HOUR_UTC` (default 16:00 UTC).
  Writes gzipped pg_dump to `/config/backup/weather/`.  Retain=30.
- **Rules 85/86 (pyproject.toml canonical).** Migrated ruff + mypy +
  pytest + bandit config to `pyproject.toml`.  Deleted `ruff.toml`,
  `mypy.ini`, `pytest.ini`.  Updated `run.sh` to drop `--config`
  flags so tools auto-discover.
- **Rule 90 (CI HARD gate before image build).** New
  `.github/workflows/ci.yml` runs the 4 gates HARD on every
  push/PR to main.  A failing gate blocks the build.
- **Rule 92 (/api/v1/ prefix).** New `_add_v1_aliases()` helper in
  `main.py` mirrors every legacy `/api/...` route under `/api/v1/...`.
  Licence + paddocks-proxy + ha-location prefixes added to the
  auth-public list under both `/api/` and `/api/v1/`.
- **Rule 93 (structured logging).** All `log.info/warning/error/
  exception/debug` calls converted from positional `%s` to
  `extra={"event": "...", ...}` dict format.

### Mypy
- `_pool.py` narrowing assert after `_init_pool()`.
- Login form `str()` coercion for `UploadFile | str` union.
- `entity_float()` now accepts `str | None`.
- `perf_tracker._stats` + `error_tracker._errors` type annotations.
- `api/routes.py::api_station_config` return type widened to `dict | JSONResponse`.

### Verified
- ruff: 0 violations
- mypy: 0 errors
- bandit HIGH: 0

### Release flow (Rule 81)
- This commit is pushed to source `main` only.
- Public/asm-weather config.yaml bump + GHCR build dispatch will
  happen **only after Peter has verified the dev install behaves
  correctly**.

## 2026.7.20
- Version bump for image rebuild

## 2026.7.19
- Clean toolbar: Rain, Radar, Wind, Temp, Clouds, Thunder layer toggles

## 2026.7.15
- Rain radar page with Windy embed (full resolution at any zoom)

## 2026.7.3
- Dedicated settings page for station management
- Rain radar page with RainViewer + farm paddock overlay

## 2026.7.1
- Initial release — extracted from PaddiSense Core weather module
- Weather stations (local Ecowitt + API)
- Open-Meteo 16-day forecast, spray assessment, wind rose
