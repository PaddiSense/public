# Changelog

## 2026.7.18 — owner-login rotation self-heal (WR-PS-192/074 structural fix, port of Weather bd8d124)

### Fixed
- **Incident 2026-07-27 (Weather was the victim; SugarSense carried the same latent
  defect):** a flipped `sugar_owner` login holds a STATIC stored options password; a
  DB-role seed re-mint changes the Postgres role underneath it and the addon strands on
  its next restart (DB init fails → licence gate fail-closed → licence screen).
- Structural fix in `core/db/_pool.py`: for `*_owner` logins the password is now DERIVED
  from the `/share` box key first (the fleet's derivation truth, Core v2026.7.44), with the
  stored options password as fallback; loud WARNING when the stored copy is stale. The
  admin/owner pool also gained the same auth-failure rebuild-and-retry self-heal the app
  pool has had since 2026-07-09. `db_user: postgres` (pre-flip) boxes are unaffected —
  stored password only, never derived.
- Regression tests: owner candidate ladder + admin-pool self-heal + end-to-end
  stale-stored-password recovery (`sugar_selfheal_test_owner` throwaway role),
  proven-fail against the pre-fix code.
- Test bootstrap hardened (same incident class, found live): the shared test cluster's
  `sugar_app` role had been rotated underneath the suite and `conftest.py` only
  created-if-absent — the whole suite failed auth on a clean checkout. Bootstrap now
  re-aligns the TEST role to the derived password when it can no longer authenticate
  (test-only; production role passwords are minted by Core, never here).

### Changed
- Theme tokens re-copied byte-identical from the canonical master (Rule 17 gate flagged
  drift — the fleet palette-consolidation had not been re-synced here; no SugarSense-side
  edits, straight `cp` of the steward's master).

## 2026.7.17 — WR-PS-183: redactor re-vendored (all six GitHub token classes)

### Changed
- **The vendored log redactor re-synced byte-identical to the patched
  canonical**: `gh[posur]_` now masks `ghp_`/`gho_`/`ghs_`/`ghu_`/`ghr_`
  alongside `github_pat_` (WR-PS-183 completeness sliver). Shared test
  refreshed (+4 fixtures).

## 2026.7.16 — WR-PS-108 fleet flip: access-sync enforce ON by default

### Changed
- **Unsigned or invalid grant pushes are now rejected with 403.**
  `SS_ACCESS_SYNC_ENFORCE` defaults ON (`=0` kill-switch — code-default
  pattern, grower boxes have no env plumbing). Core's signed pushes have been
  verifying and pinning since the receiver landed; this closes the warn-only
  window fleet-wide (WR-PS-108, Peter's go 2026-07-17). A `bound_fp` mismatch
  already failed closed before this flip.

## 2026.7.15 — WR-PS-179: canonical log redactor vendored + wired

### Added
- **Structural log redaction at the entry point.** SugarSense previously shipped
  no log redactor. `core/_log_redactor.py` is now a byte-identical vendor of the
  fleet canonical `documentation/shared/log_redactor.py` (GSM⊕Core superset:
  cloudhook URLs, PATs, bearer/DSN/`enc:` tokens, labelled secrets, portal/Resend
  keys, email + phone PII), wired as the root `RedactingFormatter` with uvicorn
  `log_config=None` so uvicorn.access/error pass through it too. Shared 30-case
  behavioural test adopted. Closes SugarSense's SEC-17/KEY-01/DATA-01 cell.

## 2026.7.14 — Fix: real Admin-signed instructions were rejected (WR-ADMIN-006 canonical re-vendor)

### Fixed
- **Re-vendored `core/licence_verify.py`** byte-identical to the fixed canonical
  (`documentation/shared/`, commit 23378e0): `verify_artifact` now accepts the licence id under
  `target` (the real instruction wire shape, §4/§9-A.5.2) as well as `licence_id` — pre-fix, every
  REAL Admin revoke/deactivate was rejected as `invalid_signature` (latent since 2026-07-01; found
  by A's WR-ADMIN-006 live test; GSM proved the fix end-to-end on v2026.7.51). Log labels split so
  a missing id no longer mislabels as a sig/replay failure. New positive regression
  `TestPositiveInstruction` (Rule 106): a genuinely signed, target-only instruction MUST verify —
  the missing test whose absence let an always-reject verifier pass every gate.

## 2026.7.13 — Warn→block flip: signed-licence enforcement ON by default (SEC-04 receive-side)

### Changed
- **`SS_SIGNED_LICENCE_ENFORCE` now defaults ON** — unsigned `/api/licence/activate` and
  `/api/licence/deactivate` are rejected (400); the Admin Ed25519 signature is the authorisation,
  never the /23 transport (§9-A). Closes the naked-deactivate hole. Readiness: Admin signs every
  licence fleet-wide (v2026.7.52 re-issue, 2026-07-12); present-but-bad signatures were already
  always fatal. `=0` = emergency kill-switch (grower boxes have no env plumbing — the code default
  IS the fleet flip). Tests: default-rejected + kill-switch pairs on both paths (+5).

## 2026.7.12 — Access-sync push verify-and-pin (WR-PS-108 / §9-A.9, reference receiver)

### Added
- **`/api/access/sync` now authenticates the push came from Core**, not just any `/23` sibling (SEC-04). `module_gate.verify_access_push` verifies Core's Ed25519 `_sig` over `canonical(payload)` (reusing the vendored `licence_verify.canonical`, the one §9-A.2 encoder — payload minus `_sig`), then **authenticates the box key against `bound_fp`**: `fp(box_pubkey)` must equal the fingerprint Admin signed into this add-on's licence (§9-A.10) — **a mismatch fails closed ALWAYS, even in warn-only** (never bare TOFU, which the untrusted `/23` would let a sibling poison). Freshness (§6 exp window) + nonce single-use per target. Pins the key on first authenticated use. **Warn-only** until `SS_ACCESS_SYNC_ENFORCE` (default off) — an unsigned/legacy push is logged and accepted during rollout; `bound_fp` mismatch is the sole warn-only exception. `bound_fp` now persisted from the activated licence. This is the fleet **reference receiver** (SugarSense `core/` is the shared base). `tests/test_module_gate.py` (+7). No behaviour change until Core signs (it does, v2026.7.14) and the fleet flips enforce.

## 2026.7.11 — Fix: unlicensed boxes 404'd instead of reaching the licence page (WR-PS-046)

### Fixed
- **Licence-gate redirect dropped the HA ingress prefix.** `licence_gate` runs OUTER of
  `auth_middleware` (registered after → Starlette wraps it outside), so `request.state.base_path`
  was unset at redirect time and an unlicensed page request bounced to a bare `/licence` — which
  resolves outside the addon's ingress mount → HA 404, leaving an unlicensed box unable to reach
  the licence-entry page. The gate now reads `X-Ingress-Path` directly (the Core v2026.6.388 /
  Safety v2026.6.25 / PWM pattern). Found in the 2026-07-12 WR-PS-046 fleet verification sweep;
  4 regression tests added (`tests/test_licence_gate_ingress.py`). Suite 62 green.

## 2026.7.10 — Fix: Core's grant push was CSRF-blocked (found live, Rule 106)

### Fixed
- **`/api/access/sync` added to the CSRF exemption list.** Core's cookie-less machine-to-machine
  grant push (WR-PS-109) was intercepted with a CSRF 403 before reaching the endpoint — the same
  exemption the licence push already has (no browser session in play; `_verify_internal` + the
  tracked §9-A.9 signature are the boundary, and CSRF protects cookie sessions, which this request
  never carries). Found by probing every receiver live after deploy; four addons had the gap.
- **Regression test** (`TestSyncEndpointReachable`) drives a cookie-less POST through the REAL
  middleware stack and asserts it reaches the endpoint — the class of gap the original e2e tests
  (GET-only) could not see.

## 2026.7.9 — WR-PS-090 Ask 4: box-key read diagnostic (PWM reference adopted)

### Changed
- **`core/db/_pool.py::_read_master_key`** now logs every key read — source path, SHA-256
  fingerprint (12 hex), and mount identity (`dev`/`ino`/`size`/`mtime`) — and WARNs on every
  fallback instead of silently passing. A consumer's logged `fp`/`dev` can now be cross-checked
  against Core's published key (the diagnostic that cracked the 2026-07-06 fake-`/share`
  incident and the WR-PS-110 key churn). Read order and return values unchanged.

## 2026.7.8 — WR-PS-109: per-user module-access enforcement on ingress (Hone SEC-04/SEC-09, Option B)

### Added
- **`core/module_gate.py`** (vendored from the Farm reference, `MODULE_KEY="sugarsense"`): Core
  pushes its `module_access` grant table to `POST /api/access/sync`; SugarSense caches it durably in
  `/data/module_access_grants.json` (atomic swap) and enforces per-user access locally on every
  **ingress** request. Decision semantics mirror Core's `effective_modules`: never-synced → open
  (bootstrap), synced-no-entries → open, granted/all-access/admin → allow, configured-but-ungranted
  → **403**. A direct cookie login with SugarSense's own credentials keeps its existing role path.
- **`POST /api/access/sync`** receiver — trust = the same transport gate the licence-forward path
  uses (`_verify_internal`); the §9-A.9 signed-grant envelope is the tracked fleet follow-up
  WR-PS-108.
- **`tests/test_module_gate.py`** (11) — decision-table units + end-to-end through the REAL auth
  middleware: ungranted ingress user 403s on pages and page-scoped API routes, granted user passes,
  never-synced box stays open, corrupt cache never locks the grower out.

## 2026.7.7 — Rotation self-heal for the app DB pool (incident 2026-07-09, Rule 106)

### Fixed
- **App DB pool self-heals across a box-key rotation.** When Core rotates the box key (`db_role.key`,
  WR-PS-088 / ADR-013), the app DB password changes; a long-running pool holds the old one, so the next
  fresh connection fails auth and the add-on breaks until a manual restart — which a grower can't do.
  `_acquire_conn` now treats a `password authentication failed` on the app pool as a stale key: drops
  the pool, rebuilds it (re-reading `/share/paddisense/db_role.key`), and retries once; a second
  failure propagates. Never applies to the admin/superuser pool (R173 intact). Fleet-wide fix
  originating from the live PWM incident. `tests/test_pool_selfheal.py`.

## 2026.7.6 — Hone PS-SEC-19: mask secret config fields + Rule 17 theme re-sync

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

## 2026.7.5 — DB password now reads a dedicated key

### Changed
- **Prefer the dedicated `/share` db_role.key for the *_app DB password; falls back to master.key
  during the WR-PS-088 split rollout — no behaviour change today.** Both keys currently carry the
  same value, so authentication is identical; this simply lets the addon keep working after the
  future split, when the DB-role key becomes distinct and the legacy master.key is retired.

## 2026.7.4 — form fields now render correctly + a security patch for file uploads

### Fixed
- **Text boxes and dropdowns on several pages now show the proper PaddiSense styling.** On the
  login, farms, blocks, varieties, chemical, weather and harvest-plan pages a handful of input
  fields and dropdowns were using a style name the theme no longer defined, so they rendered as
  plain, unstyled boxes. They now use the standard PaddiSense field styling and look consistent
  with the rest of the app.

### Security
- **Updated the file-upload handling library to a patched version.** The component that reads
  submitted forms (python-multipart) has been moved to a newer release that closes several known
  security advisories. No behaviour changes for you — it is a maintenance/hardening update.

### Changed
- **Internal code-quality only:** the type-checker now runs completely clean and the developer
  test tooling (pytest) was moved to a patched version. No harvest-planning, scheduling or licence
  behaviour changed in this release.

## 2026.7.3 — licence replay-protection is now proven by an automated test (R142)

### Security
- **We now automatically prove that a licence can't be replayed or reused.** SugarSense already
  refused a captured-and-replayed licence — every Admin-signed licence carries a one-time code and a
  time window, and the app rejects a licence whose code has been seen before or whose time window has
  passed. What was missing was an automated test proving it. A red-team review found this protection
  was wrongly recorded as "not applicable"; that is now corrected. A new behavioural test forges a
  genuinely-signed licence and shows the app accepts a fresh one, then rejects the same one presented
  twice (replay), rejects an expired one (stale), and rejects a future-dated one (clock-skew abuse).

### Changed
- `docs/AUDIT.md`: R142 (replay / nonce / timestamp) reclassified from **N/A** to **covered**, with
  `tests/test_r142_licence_replay.py` as evidence. Applicable required-security-test coverage is now
  **7/7** (142, 154, 157, 158, 171, 187, 190); 5 rows remain genuinely not-applicable. Full suite
  **44 passed, 0 failed, 0 error** on the least-privilege `sugar_app` pool.
- **No production code changed** — this release adds a regression test and documentation only; harvest
  planning and the licence path itself are byte-for-byte unchanged.

## 2026.7.2 — security tests now run under the real least-privilege database (ADR-010 enforceable)

### Security
- **The security test suite now runs against the same locked-down database account the live app
  uses.** Previously the automated safety checks ran as the database super-user because the
  disposable test database was missing the day-to-day permissions; that gap is now closed —
  the test harness builds the test database as the owner and grants the ordinary app account
  exactly the read/write it needs, so every test exercises the true production posture. This makes
  the required security tests enforceable: a release can be blocked if a safety test is missing.
- **Forged-login attempts now raise an alert (Rule 171).** When something presents a Home Assistant
  "ingress" header from outside the trusted Supervisor network — a spoofing attempt — SugarSense now
  denies it *and* logs a structured security event so the attempt is visible, instead of silently
  refusing. A new behavioural test proves the alert fires on a forged attempt and stays quiet for a
  genuine one.

### Fixed
- **Full test suite is green end-to-end (40 tests).** The database-permission error that was
  blocking the smoke and licence tests is resolved, and an unauthenticated-access test was corrected
  to check the real behaviour (an unauthenticated caller is redirected to the login page with no data
  returned) rather than a status code the app never emits for that route.

### Changed
- Re-audited `docs/AUDIT.md`: 6 of 6 applicable required-security-test rows are now covered
  (154, 157, 158, 171, 187, 190); the remaining 6 rows are documented as genuinely not-applicable
  with concrete reasons (no signed-request replay channel, no CSV export, no per-owner objects, no
  server-side URL fetch, no self-service credential change, no email). Version bump only — no
  behavioural change to harvest planning.

## 2026.7.1 — ADR-010 flip-ready: v2.49 re-audit, close_pools lifecycle, security-test suite

### Security
- **New `tests/test_security.py` — behavioural red-team regression suite** covering the applicable
  rows of `REQUIRED_SECURITY_TESTS`: R157 CSRF (token-less mutating POST → 403; valid double-submit
  token clears), R158 (oversized body → 413; login endpoint rate-limit bounds enumeration),
  R154 (viewer session refused a supervisor-only mutation → 403), R187 (forged `X-Forwarded-For`
  ignored — `is_ingress` trusts the real socket peer only), R190 (non-existent user and wrong
  password return **byte-identical** login bodies — no enumeration oracle). All pass on the admin
  pool; the least-priv `sugar_app` grants on the disposable test DB remain a pre-existing infra gap
  (WR-PS-081). N/A rows (142/146/153/159/171/188/189) documented in `docs/AUDIT.md`.

### Fixed
- **DB pool lifecycle (Rule 92/134):** added `close_pools()` to `core/db/_pool.py`, exported it from
  `core/db/__init__.py` (Rule 79), and wired an `@app.on_event("shutdown")` handler that calls it —
  connections are now released on restart instead of leaking (closes the two
  `check-fleet-consistency.py` warnings).

### Changed
- **Re-audited against Golden Rules v2.49** (was v2.48). Relocated Category-A **R33**
  (moisture/CCS-corrected weight — SeedMgr carries the canonical formula) folded into `CLAUDE.md`
  Critical Rules as an owned invariant. `docs/AUDIT.md` refreshed: one row per applicable rule,
  14-day cadence, real gaps recorded (test-DB least-priv provisioning; in-memory sessions
  not revoked on a future credential-change flow). Corrected the stale ingress port in `CLAUDE.md`
  (8097 → 8101).

## 2026.6.27 — 🔴 SEC: fix X-Ingress-Path header-spoof auth bypass (fleet-critical)

### Security
- **`core/auth.py::is_ingress` now requires the client IP on the Supervisor network
  (`172.30.32.0/23`) before trusting `X-Ingress-Path`.** It previously trusted the header
  unconditionally — so ANY client that could reach the addon port and set `X-Ingress-Path` was
  handed the `role: admin` ingress session (remote admin auth bypass). Restores the canonical
  `documentation/shared/auth.py` source-IP gate that 6 of 10 addons already carried. Found by the
  2026-07-04 fleet-consistency sweep; a `check-fleet-consistency.py` assertion will gate it (WR-PS-084).

## 2026.6.26 — add fleet-standard BodySizeLimitMiddleware (10 MB DoS guard)

### Security
- **Added the global `BodySizeLimitMiddleware`** (10 MB cap, matches Core + the other 7 addons):
  rejects requests whose `Content-Length` exceeds the limit with **413**, and requires a declared
  length on chunked body-bearing methods (**411**). Closes a fleet-consistency gap — this addon was
  one of three lacking the global body-size guard (only endpoint-level caps existed). Fleet-alignment
  pass (Peter-directed 2026-07-04).

## 2026.6.25 — align run.sh to fleet compileall gate (ADR-012 develop-branch alignment)

### Changed
- **`run.sh` Gate 1 now uses `python -m compileall` (single process)** instead of the per-file
  `py_compile` loop (one process per file, slow on ARM grower boxes) — same Rule 37 syntax coverage,
  faster boot. Matches the fleet standard (Store/Farm/ASM) and brings in the one genuine improvement
  that lived only on the stale pre-flip `develop` branch, so `develop` can be retired with no loss
  (ADR-012). Deep-dive confirmed every other `develop` diff was already superseded in main
  (Dockerfile 3.11→3.12, old fail-open pool → fail-closed, old-version docs).

## 2026.6.24 — SEC-08/R173: add `share:rw` map — SugarSense was silently on the superuser (WR-PS-081)

### Security
- **`config.yaml` now maps `share:rw`.** SugarSense was the ONE addon that never mapped the `/share`
  mount, so `_pool._read_master_key()` could not read the box key Core publishes to
  `/share/paddisense/master.key` — its `sugar_app` password never matched Core's role, the app pool
  init failed, and the (then fail-open) pool silently fell back to the `postgres` **superuser**. The
  v.23 fail-closed conversion exposed this by crash-looping (`RuntimeError: Master key not found`)
  instead of masking it. Mapping `/share` lets SugarSense read the shared key → `sugar_app`
  authenticates → the R173 least-priv request path is genuinely in effect (fail-closed). This is the
  value of fail-closed: a broken least-priv path now fails loudly instead of running as superuser.

## 2026.6.23 — SEC-08/R173: fail-closed DB app pool (Phase-2, WR-PS-081)

### Security
- **The request-path DB pool is now fail-closed (R173/SEC-08).** `_pool.py` no longer falls back to
  the `postgres` superuser if the `sugar_app` app pool can't initialise — `get_cursor()` returns the
  least-priv app pool or raises. Migrations/DDL still use the admin pool during the startup window
  (before `init_app_pool()` is called). Converges the fleet to Farm's fail-closed posture; a future
  key/role failure now fails loudly instead of silently promoting request-path queries to superuser.
  (`/share` persists, so an established box that reboots keeps its key and does not fail-closed.)

## 2026.6.22 — SEC-08/R173: read the shared box key so sugar_app authenticates (WR-PS-081)

### Security
- **`_pool.py` now reads the box DB-role key from the shared `/share/paddisense/master.key`** Core
  publishes (WR-PS-081), falling back to the local `/data` key during rollout. The per-container
  `/data` key differed from Core's, so `sugar_app`'s derived password never matched the role Core minted
  → the pool **silently fell back to the `postgres` superuser** (confirmed fleet-wide via boot logs).
  Now `sugar_app` authenticates → the R173 least-priv DML-only request path is genuinely in effect.
  Fernet-at-rest untouched (separate `/data` key). Superuser fallback kept as a rollout safety net;
  Phase 2 fail-closes.

## 2026.6.21 — R143: constant-time token compare in _verify_internal (fleet sweep)

### Security
- **`core/licence.py::_verify_internal` now compares the Supervisor Bearer token with
  `hmac.compare_digest`, not `==`** (Rule 143 — a plain `==` on secret material leaks length/content
  via timing). Fleet-wide R143 sweep (Store/Weather/SugarSense had the same `==`). Defence-in-depth
  only — the Admin Ed25519 signature is the real authorisation (SEC-04).

## 2026.6.20 — SEC-04/R172: tighten licence transport trust /16 → /23 (THREAT_MODEL G1)

### Security
- **`core/licence.py::_verify_internal` narrowed from `172.30.0.0/16` to `172.30.32.0/23`** (the
  Supervisor add-on bridge, fleet-standard) + loopback. The `/16` trusted the whole Supervisor
  supernet — far broader than the exact expected peer range (Rule 172). Surfaced as **G1** in the new
  `docs/security/THREAT_MODEL.md`. Defence-in-depth only — the Admin Ed25519 signature is the real
  authorisation (SEC-04); this just shrinks the transport-trust blast radius. Licence tests (12) green.

## 2026.6.19 — SCAL-03: Python 3.11 → 3.12 base-image bump + digest pin (Hone SCAL-03 / WR-PS-080)

### Changed
- **Base image `python:3.11-slim` → `python:3.12-slim@sha256:423ed6ab…199fbf`** (fleet-index digest).
  `pyproject.toml` ruff `target-version` + mypy `python_version` → 3.12. Off the Python 3.11 EOL
  runway (Hone SCAL-03), digest-pinned for reproducible builds. Isolated bump — no dependency changes
  (WR-PS-080 non-goal). Tests run on the pinned 3.12 toolchain; dev-deploy rebuilds on 3.12-slim.

## 2026.6.18 — SEC-01/04: Admin signed-licence receive-side (Hone PS-SEC-04 fleet adoption)

### Security
- **Both mutating licence paths now verify the Admin Ed25519 signature** (`core/licence.py`).
  SugarSense trusted the Supervisor subnet (`_verify_internal`) alone on `/api/licence/activate`
  and `/deactivate` — the "network-location = trust" pattern Hone **PS-SEC-04** flags and
  `SIGNED_LICENCE_CONTRACT §9-A` retires. Vendored `core/licence_verify.py` (byte-identical to
  `documentation/shared/`) + Admin pinned pubkey at `data/admin_signing_pubkey.json` (baked by the
  existing `COPY sugarsense/`). `activate` verifies via `_extract_licence` (handles the paste `code`
  AND Core's heartbeat `signed_licence`); `deactivate` verifies the signed instruction
  (`action ∈ {deactivate,revoke}`). Legacy-tolerant behind `SS_SIGNED_LICENCE_ENFORCE` (default
  off). Signature — not network position — is the trust boundary. `cryptography==48.0.1` pinned.

### Fixed
- **Test-DB isolation (FLEET_PROCESS §6, WR-PS-069)** — `tests/conftest.py` pointed at the LIVE
  `sugarsense` DB; now forces `SS_DB_NAME → sugarsense_test`. A test run no longer applies
  schema/migrations to production.
- Tests: `tests/test_licence_signed.py` (12 pass). Closes SugarSense slice of **WR-HONE-SEC-04**.

## 2026.6.17
Security: stop leaking licence details from the public licence endpoint (R144, WR-PS-066).
### Fixed
- **R144 licence liveness-only:** `GET /api/licence` is unauthenticated (Core polls it),
  but previously returned the full `licence` string plus `product`, `exp`, and `grower_id`.
  It now returns liveness only — `{"enrolled": <bool>}` — matching the fleet-correct
  Farm/ASM shape. `activate`/`deactivate` (internal-auth) endpoints are unchanged.

## 2026.6.16
ADR-010 flip-readiness — verify-commit CLEAN. No functional change to existing features.
### Added
- **CSP header (R156):** `Content-Security-Policy` added to `SecurityHeadersMiddleware`
  (default-src 'self', object-src 'none', frame-ancestors/base-uri/form-action 'self';
  script/style allow 'unsafe-inline' — inline-handler→nonce conversion is a follow-up).
- **CSRF protection (R157):** double-submit `CsrfMiddleware` (fail-closed 403 on mutating
  requests without a matching `sugar_csrf` token) + a base-template fetch wrapper that echoes
  the token on every mutating fetch; behavioural 403 test added.
### Changed
- R60: split `calculate_schedule` (fetch/compute/persist helpers) and `api_dashboard`
  (`_season_class_stats` helper) to ≤50 lines.
- R88: renamed 10 reserved `name` LogRecord `extra=` keys → `obj_name`.
- R167: Supervisor-network check uses the `ipaddress` module, not string prefix.
- R17 theme re-sync; CLAUDE.md golden_rules 2.24→2.42.
### Known (pre-existing, not introduced here)
- The least-privilege `sugar_app` DB role is referenced in `_pool.py` but never provisioned
  or GRANTed — schema DDL/DML through it fails ("permission denied for schema public") on a
  box where the role exists (5 tests error on it). Separate fix needed (role provisioning +
  grants, or route DDL through the admin pool); same class as the Safety Rule 173 fix.

## 2026.6.15
- run.sh: source canonical master theme (WR-PS-045/ADR-007)
- Theme re-synced byte-identical to canonical master
- Added docs/SESSION_PICKUP.md (Rule 191)
- CLAUDE.md version + golden_rules_version sync

## 2026.6.10
- Dependency updates
- Bug fixes and enhancements
