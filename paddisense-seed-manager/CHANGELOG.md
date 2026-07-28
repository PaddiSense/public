# Changelog

## 2026.7.9

### Reliability
- The add-on now reconnects to its database automatically after system updates or maintenance. Previously, a restart at the wrong moment could leave the add-on showing its licence screen until it was manually repaired — that can no longer happen.

## 2026.7.8 — WR-PS-183: redactor re-vendored (all six GitHub token classes)

### Changed
- **The vendored log redactor re-synced byte-identical to the patched
  canonical**: `gh[posur]_` now masks `ghp_`/`gho_`/`ghs_`/`ghu_`/`ghr_`
  alongside `github_pat_` (WR-PS-183 completeness sliver). Shared test
  refreshed (+4 fixtures).

All notable changes to the Seed Manager addon.
Format: [CalVer](https://calver.org/) — YYYY.M.PATCH

---

## 2026.7.7 — WR-PS-108 fleet flip: access-sync enforce ON by default

### Changed
- **Unsigned or invalid grant pushes are now rejected with 403.**
  `SM_ACCESS_SYNC_ENFORCE` defaults ON (`=0` kill-switch — code-default
  pattern, grower boxes have no env plumbing). Core's signed pushes have been
  verifying and pinning since the receiver landed; this closes the warn-only
  window fleet-wide (WR-PS-108, Peter's go 2026-07-17). A `bound_fp` mismatch
  already failed closed before this flip.

## 2026.7.6 — WR-PS-108: access-sync verify-and-pin (§9-A.9 receiver)

### Added
- **WR-PS-108 / §9-A.9: the Core→add-on grant push is now verified-and-pinned.**
  Core signs every `POST /api/access/sync` with its box Ed25519 identity; this
  receiver now verifies the signature, authenticates Core's key against the
  `bound_fp` Admin signs into this add-on's licence (never bare TOFU), checks
  the freshness window and single-use nonce, and pins the key. A `bound_fp`
  mismatch fails closed ALWAYS — even in warn-only; an unsigned/invalid push
  is warn-only until `SM_ACCESS_SYNC_ENFORCE` (the coordinated fleet flip).
  `bound_fp` is persisted from the activated licence. Copied from the
  SugarSense v2026.7.12 reference; 7 behavioural tests (forged signature,
  cross-target replay, nonce replay, expiry, fp mismatch).

## 2026.7.5 — WR-PS-179: canonical log redactor vendored + wired

### Added
- **Structural log redaction at the entry point.** Seed Manager previously
  shipped no log redactor. `core/_log_redactor.py` is now a byte-identical
  vendor of the fleet canonical `documentation/shared/log_redactor.py`
  (GSM⊕Core superset: cloudhook URLs, PATs, bearer/DSN/`enc:` tokens, labelled
  secrets, portal/Resend keys, email + phone PII), wired as the root
  `RedactingFormatter` with uvicorn `log_config=None` so uvicorn.access/error
  pass through it too. Shared 30-case behavioural test adopted. Closes Seed
  Manager's SEC-17/KEY-01/DATA-01 cell.

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
- **`SM_SIGNED_LICENCE_ENFORCE` now defaults ON** — unsigned `/api/licence/activate` and
  `/api/licence/deactivate` (and unsigned pasted codes) are rejected (400); the Admin Ed25519
  signature is the authorisation, never the transport (§9-A). Closes the naked-deactivate hole.
  Readiness: Admin signs every licence fleet-wide (v2026.7.52 re-issue, 2026-07-12);
  present-but-bad signatures were already always fatal. `=0` = emergency kill-switch (grower boxes
  have no env plumbing — the code default IS the fleet flip). NOTE for standalone RRAPL: SM there
  runs licence-free (no Core, no activate traffic) — the flip only affects the licence endpoints.
  Tests: default-rejected + kill-switch pairs (+3).

## 2026.7.2 — WR-PS-090 Ask 4: box-key read diagnostic (PWM reference adopted)

### Changed
- **`db/_pool.py::_read_box_key`** now logs every key read — source path, SHA-256 fingerprint
  (12 hex), and mount identity (`dev`/`ino`/`size`/`mtime`) — and WARNs on every fallback instead
  of silently passing. On a grower/industry box the logged `fp`/`dev` cross-checks against the
  publisher's key (the diagnostic that cracked the 2026-07-06 fake-`/share` incident); on the
  standalone RRAPL box the two `/share` WARNs per pool build are expected — they document that the
  local `/data` key is legitimately in use. Read order and return values unchanged.

## 2026.7.1 — WR-PS-109: per-user module-access enforcement on ingress (Hone SEC-04/SEC-09, Option B)

### Added
- **`core/module_gate.py`** (vendored from the Farm reference, `MODULE_KEY="paddisense-seed-manager"`):
  Core pushes its `module_access` grant table to `POST /api/access/sync`; SM caches it durably in
  `/data/module_access_grants.json` (atomic swap) and enforces per-user access locally on the
  **ingress** branch of `auth_middleware`. Decision semantics mirror Core's `effective_modules`:
  never-synced → open (bootstrap — including a standalone RRAPL box with no Core at all),
  synced-no-entries → open, granted/all-access/admin → allow, configured-but-ungranted → **403**.
  Direct cookie logins and the public `/kiosk` floor surface are untouched.
- **`POST /api/access/sync`** receiver — trust = the same transport gate the licence push uses
  (`_verify_internal`); the §9-A.9 signed-grant envelope is the tracked fleet follow-up WR-PS-108.
- **`tests/test_module_gate.py`** (11) — decision-table units + end-to-end through the REAL auth
  middleware: ungranted ingress user 403s on pages and `/storage/api/locations`, granted user
  passes, never-synced box stays open, corrupt cache never locks the operator out.

---
## 2026.6.225 — Rotation self-heal for the app DB pool (incident 2026-07-09, Rule 106)

### Fixed
- **App DB pool self-heals across a box-key rotation.** When Core rotates the box key (`db_role.key`,
  WR-PS-088 / ADR-013), the app DB password changes; a long-running pool holds the old one, so the next
  fresh connection fails auth and the add-on breaks until a manual restart — which a grower can't do.
  `_acquire_conn` now treats a `password authentication failed` on the app pool as a stale key: drops
  the pool, rebuilds it (re-reading `/share/paddisense/db_role.key`), and retries once; a second
  failure propagates. Never applies to the admin/superuser pool (R173 intact). Fleet-wide fix
  originating from the live PWM incident. `tests/test_pool_selfheal.py`.

## 2026.6.224 — Hone PS-SEC-19: mask secret config fields + Rule 17 theme re-sync

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

## 2026.6.223

### Fixed — 422 int_parsing when the kiosk PIN modal state got out of sync

**Symptom (Peter 2026-07-08, after kiosk PIN input):**
```
{"detail":[{"type":"int_parsing","loc":["path","user_id"],
"msg":"Input should be a valid integer, unable to parse string as an integer",
"input":"null"}]}
```

**Root cause.** The v.219 native-form-submit rewrite exposed a state-sync gap: `_pinUserId` initialises to JavaScript `null` and only becomes a valid integer once `openPin(userId, name)` runs. Two paths could reach `submitPin()` with `_pinUserId` still `null`:

1. The `pin_error=1&uid=X` auto-reopen block calls `openPin(uid, OP_NAMES[uid])` — but if `OP_NAMES[uid]` is undefined (e.g. the user was deactivated between the failed submit and the reload, or the query param arrived with `uid=` empty), `openPin` never fires. If the modal was already visible from a prior state (browser back-forward cache, etc.), the visible `✓` button still calls `submitPin`.
2. Any other path that opens the modal without going through `openPin` — none deliberate today but the defence is cheap.

In both, `_pinUserId` is `null`, `submitForm(null, pin)` builds `form.action = '/kiosk/select-operator/' + null` (JS coerces `null` → `"null"` via string concat), and FastAPI's path validator 422s the request with an ugly JSON body.

**Fix.** `submitPin()` and `submitForm()` both check `Number.isFinite(userId)` before touching the form. On failure, show `"Tap your name first"` in the modal error slot and close the modal cleanly. No POST fires with a bad path parameter.

### Not changed
- v.219 native form submit + `303 See Other` + `secure=True` removal — unchanged.
- v.220 `NO_CACHE_HEADERS` on entry pages — unchanged.
- v.221 licence-gate ingress prefix — unchanged.
- v.222 standalone-install self-bootstrap + role provisioning — unchanged.

---

## 2026.6.222

### Fixed — Phase-2 fail-closed crash on standalone SM installs (no Core, no GSM)

**Symptom (Peter 2026-07-08, RRAPL PROD box after v.221 update):**

```
File "/app/seedmgr/db/_pool.py", line 89, in _derive_app_password
    raise FileNotFoundError(f"box key missing ({_SHARED_DB_KEY_PATH} / {_MASTER_KEY_PATH})")
FileNotFoundError: box key missing (/share/paddisense/master.key / /data/keys/master.key)
ERROR:    Application startup failed. Exiting.
```

**Root cause — WR-PS-081 scope-gap on standalone deployments.** Phase-2 fail-closed pool (`_derive_app_password`) requires either `/share/paddisense/{db_role,master}.key` (published by Core on grower boxes, or by GSM on industry boxes per WR-AS-014 §2) OR `/data/keys/master.key` (local SM key that some external actor was supposed to seed). On boxes that run SM standalone — no Core, no GSM — NEITHER path exists, so SM refused to start after the Phase-2 landing in v.214. The RRAPL PROD seed shed is the first standalone box to update past v.213; it hit the wall on v.221.

**Fix — SM self-bootstraps its own key + provisions its own role.**

- `_pool.py::_bootstrap_local_master_key()` — new. When `_read_box_key()` returns None (neither shared nor local key present), generate 32 CSPRNG bytes via `os.urandom`, write to `/data/keys/master.key` with `0o600`. Idempotent: `_read_box_key` always tries the file first, so this bootstrap fires exactly once per addon-container-lifetime. Called from `_derive_app_password` when the read returns None.
- `_migrate.py::_ensure_seed_app_role()` — new. Called from `ensure_database()` after schema/migrations and BEFORE `init_app_pool()`. Uses the admin (postgres) DSN to `CREATE ROLE seed_app` on missing OR `ALTER ROLE ... PASSWORD` to realign an existing role's password to what SM derives. Also GRANTs CONNECT + minimal DML (`SELECT/INSERT/UPDATE/DELETE` on `public` tables + `USAGE, SELECT` on sequences) plus `ALTER DEFAULT PRIVILEGES` so future tables created by superuser inherit the same DML grant. Best-effort — failure to CREATE/ALTER is a WARNING not a crash (some cluster configs run admin as a locked-down role; SM should still start).

**Not touched on boxes where Core (or GSM) IS present.** `_read_box_key` still tries the shared paths FIRST. On grower boxes with Core running, `/share/paddisense/db_role.key` exists → self-bootstrap is skipped → Core-minted `seed_app` role auth works as before. On industry boxes with GSM publishing (v2026.7.6+) the same — shared key is preferred. Standalone installs get the fallback path.

### Cross-Claude coordination note

Filed as follow-up under WR-PS-081 in `documentation/contracts/PS_WORK_REQUESTS.md` (v.222 wrap). The self-bootstrap + role provisioning pattern here mirrors what Farm has always done (Farm self-bootstraps its own master.key + is the reference impl for standalone deployment). SM should also mirror Farm's more recent additive `db_role.key` mirror in a follow-up (v.223+) but that's a P-Claude coordination item, not a crash fix.

### Not changed
- v.219 kiosk PIN loop + keypad UX + `secure=True` removal — unchanged.
- v.220 `NO_CACHE_HEADERS` on kiosk entry pages — unchanged.
- v.221 licence-gate ingress-prefix fix — unchanged.

---

## 2026.6.221

### Fixed — licence-gate redirect lost the ingress prefix → 404 in side panel

**Symptom (Peter 2026-07-08, industry-box dev):** on a box with no SM licence installed, opening the SM side panel showed a 404 instead of the `/licence` activation page. Peter reported it as "no licence option in the side panel — just a 404".

**Root cause.** `licence_gate` middleware in `main.py:541` read `request.state.base_path` to build the redirect Location. But — and this was the trap — `request.state.base_path` is populated by `auth_middleware.` `_init_request_state` (`main.py:482`), and Starlette registers middleware bottom-up: because `licence_gate` was registered AFTER `auth_middleware` at module scope, `licence_gate` is OUTERMOST and runs FIRST — before `auth_middleware` populates the state. So `getattr(request.state, "base_path", "")` always saw empty, and the redirect Location was just `/licence` — no `/api/hassio_ingress/<token>` prefix. The browser (inside the HA ingress iframe) treated that as absolute against the HA frontend origin, HA returned 404 for the missing route, and the user saw "no licence option".

**Fix.** `licence_gate` now reads `X-Ingress-Path` DIRECTLY from `request.headers` — same source `_init_request_state` reads it from — so it doesn't depend on state-population order. One-line functional change; the rest is docstring capturing the ordering trap so a future refactor doesn't reintroduce it.

### Regression test

`tests/test_licence_gate_ingress_redirect.py` — AST-level assertion that `licence_gate`'s executable body (docstring stripped) uses `request.headers.get('X-Ingress-Path'...)` and does NOT read `request.state.base_path`. Locks the fix against a "cleanup — use request.state consistently" future rewrite.

### Not changed

- v.219 kiosk PIN loop fix + native form submit + `secure=True` removal + `303 See Other` — unchanged.
- v.220 `NO_CACHE_HEADERS` on kiosk entry pages — unchanged.
- Keypad ✓ / ✕ UX — unchanged.
- `_LICENCE_EXEMPT_PREFIXES` — unchanged; `/licence` is still exempt from the gate.

---

## 2026.6.220

### Fixed — kiosk entry pages served without cache-busting headers

`kiosk/home.py::kiosk_home` (route `/kiosk/`) and `kiosk/operator.py::kiosk_select_operator` (route `/kiosk/select-operator`) rendered their templates **without `NO_CACHE_HEADERS`**. Every other kiosk page in the surface (`bin_weigh`, `bins`, `grading`, `internal`, `movement_detail`, etc.) already applied them. The two entry-point pages were the only ones missing.

Symptom (Peter 2026-07-08, follow-up to v.219 ship): after v.219 dev-deployed + grower-released, the seed-shed iPad in HA Companion still displayed **v2026.6.211** in the kiosk header. iOS WKWebView had cached the rendered HTML from an older visit and had no cache-control instruction to refetch. Force-quitting the Companion app clears it, but users shouldn't need to do that after every release.

Fix: both routes now `return templates.TemplateResponse(..., headers=NO_CACHE_HEADERS)`. Two-line change. New kiosk fetches will always get the current version — no `Cache-Control` gymnastics on the client side needed.

### Not changed
- v2026.6.219 loop fix (native form submit + `secure=True` removal + `303 See Other`) — unchanged.
- Keypad ✓ / ✕ UX — unchanged.
- Regression test `tests/test_kiosk_cookie_flags.py` — unchanged; still passes.

---

## 2026.6.219

### Fixed — iPad HA Companion kiosk PIN loop

**Symptom (Peter 2026-07-08):** on the seed-shed iPad running HA Companion in kiosk mode, entering the operator PIN + submitting looped back to the PIN screen after every attempt. The exact same code path works fine on the office PC in kiosk mode. iPad-only.

**Root cause.** `kiosk/operator.py::kiosk_set_operator` returned a `302 Redirect` with `Set-Cookie: sm_kiosk_operator=...; Secure; HttpOnly; SameSite=Lax`, and the client-side JS submitted with `fetch(POST, credentials: 'same-origin', redirect: 'manual')`. Two problems compound on iOS WKWebView (which HA Companion uses):
1. **`Secure` cookies dropped over HTTP** — HA ingress is HTTP internally. Any addon page served via ingress runs over HTTP behind HA's HTTPS frontend, so `Secure`-flagged cookies are silently dropped by the browser. `secure=True` was added in v2026.6.207 as part of an adversarial-audit hardening pass and immediately broke this flow — but only surfaced on iPad because the office PC connects via a path (Nabu Casa cloud proxy or local HA HTTPS on desktop) where the browser considers the connection Secure end-to-end.
2. **`fetch(..., redirect: 'manual')` drops Set-Cookie on WKWebView** — WebKit's manual-redirect handling is quirky here; the cookie doesn't land even when the addon is served over HTTPS. Chrome and Firefox apply it; WKWebView doesn't.

**Fix (belt-and-braces).** `kiosk_set_operator` now:
- Uses `303 See Other` (proper POST → GET redirect) with `Set-Cookie` — native browser flow, works identically in Safari/WKWebView/Chrome.
- Cookie no longer carries `secure=True` (fleet invariant: HA ingress is HTTP internally; `Secure` cookies never land).
- Wrong PIN → `303` back to `/kiosk/select-operator?pin_error=1&uid=X` — client JS re-opens the PIN modal for that user with an error message (no page-navigation dead-end).
- Same-shape fix applied to `sm_session` in `dashboard.py` — same latent bug, would have bit the moment staff started using iPad Companion.

Client JS in `kiosk_operator.html` replaced the `fetch(POST, redirect: 'manual')` acrobatics with a native `<form id="pinForm" method="POST">.submit()` — one code path, one browser mechanic, works everywhere.

### Fixed — PIN keypad "no OK button" confusion

**Symptom (Peter 2026-07-08):** the PIN keypad shows an `✕` (cancel) in the bottom-left, no explicit OK/submit button. Users see the `✕` and don't know how to submit their PIN.

**Fix.** Bottom-left key on the keypad is now `✓` (submit, styled with the success/primary colour so the affordance is obvious). Cancel moved to a small `✕` in the modal's top-right corner. Auto-submit-on-4th-digit is preserved (fast-path for common case), but the visible `✓` gives users an explicit "how do I submit" answer.

New layout:
```
1 2 3
4 5 6
7 8 9
✓ 0 ⌫
```
plus a `✕` cancel in the modal's top-right corner.

### Regression test

`tests/test_kiosk_cookie_flags.py` — AST-level check that fails if any `set_cookie(..., secure=True, ...)` reappears anywhere in `seedmgr/`. Locks the fleet invariant against future well-intentioned hardening passes reintroducing the same bug.

---

## 2026.6.218

### Database auth
- Prefer the dedicated `/share/paddisense/db_role.key` for the `*_app` DB password; falls back to
  `master.key` during the WR-PS-088 split rollout — no behaviour change today (both keys carry the
  same value until the 1b flip). The app-role pool keeps authenticating after Core retires
  `master.key` in favour of the distinct `db_role.key`.

---

## 2026.6.217

### Security / Testing
- **The signed-licence path now has a proper anti-replay test — nobody can reuse an old approval.**
  When Head Office signs a licence approval and sends it to this addon, the addon already refuses
  a second copy of the same approval, and refuses one whose date has passed. That protection was
  in the code but had never been proven by an automatic test — a review flagged it as an untested
  gap. There is now a real regression test (`tests/test_r142_licence_replay.py`) that forges a
  genuinely-signed approval and confirms: a fresh one is accepted, a repeated one is rejected, an
  expired one is rejected, and a future-dated one is rejected. No change to any live/production
  code — this only adds the missing test and corrects the audit record from "not applicable" to
  "covered" (Rule 142).
- Result: 52/52 security + smoke tests green; the replay/nonce/timestamp protection is now
  guaranteed by the release gate.

---

## 2026.6.216

### Security / Testing
- **Security test-bench now sets itself up automatically and runs like the real server.**
  The behavioural security suite used to need a database that had been prepared by hand on
  this box — if that database was ever deleted, the tests could not run. The suite now builds
  its own throwaway `seedmgr_test` database from scratch every time (tables, reference data and
  a licence record), so it works on a fresh machine and after a wipe with no manual steps.
- **Tests now run under the same restricted database login the live addon uses.** Previously the
  test run quietly connected as the all-powerful database superuser, so it never actually checked
  that the addon's day-to-day, limited-permission login (`seed_app`) has exactly the access it
  needs. The tests now connect as that restricted login — proving the security boundary holds the
  way it does in production — while the one-time setup still runs as the admin login. No change to
  any live/production code path; this is test-harness only.
- Result: 47/47 security + smoke tests green, reproducibly, and every applicable required-security
  test is present and collected — the release gate can now enforce them.

---

## 2026.6.215

### Security
- **Red-team security-test coverage brought to full applicable (REQUIRED_SECURITY_TESTS, Rule 154/192).**
  Added three real behavioural regression tests: **R187** — a forged `X-Forwarded-For`/`X-Real-IP`
  from an off-network socket does not grant ingress admin (trust keys off the real socket peer in
  `172.30.32.0/23`, positive control from an in-range socket succeeds); **R171** — a spoofed
  `X-Ingress-Path` from an untrusted socket raises an `ingress_spoof_attempt` WARNING alert
  (`caplog`); **R190** — an unknown username and a wrong password for an existing user return
  byte-identical login responses (no account enumeration). Coverage now 9 tested + 3 N/A
  (142 no nonce/timestamp signed-request protocol, 146 CSV export is client-side, 189 no email flow).
- **R190 hardening — constant-time login.** `dashboard.login_submit` now verifies against a fixed
  `auth.DUMMY_PASSWORD_HASH` when the username does not exist, so the PBKDF2 cost (and hence response
  latency) is identical whether or not the account exists — closes the timing side-channel.

### Fixed
- **R79: `db/__init__.py` now re-exports `init_app_pool`** alongside `close_pools`/`get_conn`/
  `get_cursor` — the app-pool activation lifecycle function was importable only from the private
  `_pool` module, tripping the fleet-consistency db-exports check.

### Changed
- **v2.49 rebase-audit.** `golden_rules_version` 2.48 → 2.49; `docs/AUDIT.md` refreshed against the
  Wave-4a rule set (Category-B mergers R34/35/36→R19, R56→R65, R124→R133, R145/148→R160, R147→R166).
  **Rule 33 (moisture-corrected weight)** relocated into this addon's CLAUDE.md as an owned product
  invariant (Wave-4a Category A — Seed Manager is the canonical formula owner). CLAUDE.md Python
  version note corrected 3.11 → 3.12.

## 2026.6.214

### Security
- **SEC-08/R173: the request-path DB pool is now fail-closed (Phase-2, WR-PS-081).** `db/_pool.py` no
  longer falls back to the `postgres` superuser if the `seed_app` app pool can't initialise —
  `get_cursor()` returns the least-priv app pool or raises. Migrations/DDL still use the admin pool
  during the startup window (before `init_app_pool()`). Converges to the fleet fail-closed posture;
  a future key/role failure now fails loudly instead of silently promoting request-path queries to
  superuser. (`/share` persists, so an established box that reboots keeps its key and does not
  fail-closed.) Also removed the old `_read_box_key() is None` no-key admin gate for fleet uniformity.

## 2026.6.213
### Changed
- **SCAL-03 (Hone / WR-PS-080): base image `python:3.11-slim` → `python:3.12-slim@sha256:423ed6ab…199fbf`**
  (fleet-index digest). `pyproject.toml` ruff `target-version` + mypy `python_version` → 3.12. Off the
  Python 3.11 EOL runway, digest-pinned for reproducible builds. Isolated bump — no dependency changes.
  Tests run on the pinned 3.12 toolchain; dev-deploy rebuilds on 3.12-slim + smoke.

## 2026.6.212
### Security
- **SEC-01/04 (Hone PS-SEC-04): both mutating licence paths now verify the Admin Ed25519 signature**
  (`licence.py`). Previously `/api/licence/activate` and `/deactivate` were gated only by
  `_authorised` (admin session OR the `/23` transport) — the "network-location = trust" pattern
  `SIGNED_LICENCE_CONTRACT §9-A` retires. Vendored `seedmgr/core/licence_verify.py` (byte-identical to
  `documentation/shared/`; new `seedmgr/core/` package so the pubkey path resolves) + Admin pinned
  pubkey at `seedmgr/data/admin_signing_pubkey.json` (baked by the existing `COPY seedmgr/`).
  `activate` verifies via `_extract_licence` (handles the paste `code` AND Core's heartbeat
  `signed_licence`); `deactivate` verifies the signed instruction (`action ∈ {deactivate,revoke}`).
  Legacy-tolerant behind `SM_SIGNED_LICENCE_ENFORCE` (default off). Signature — not network position —
  is the trust boundary. `cryptography==48.0.1` pinned. Tests: `tests/test_licence_signed.py` (7 unit
  tests — signature policy + `_extract_licence` both paths; DB-backed API tests deferred to the
  WR-PS-069 test-harness follow-up, since SeedMgr's harness needs a pre-provisioned `seedmgr_test`).
  Closes SeedMgr slice of **WR-HONE-SEC-04**.

## 2026.6.211
### Security
- R144/WR-PS-066: the public `GET /api/licence` (Core polls it without auth) no longer
  leaks the licence string, product, grower_id or expiry. It now returns liveness-only
  `{"enrolled": <bool>}`, matching the fleet (Farm/ASM). The signed licence detail remains
  reachable only via the authenticated activate/deactivate path. Regression-covered.

## 2026.6.210
### Added
- F5/Rule 154: behavioural IDOR denial test (`TestGradingIdor`) — a grading child id from one
  order cannot be deleted via another order (the security fix from v207, now regression-covered
  before the grower release).

## 2026.6.209
Dead-code sweep (pre-grower-release). No functional change from v208.
### Removed
- 21 dead legacy `*_mobile.html` templates (superseded by `mobile/*.html`; `pick_template`
  always serves the `mobile/` version, so these were never rendered) + the `rack_assign_mobile.html`
  duplicate. ~40% of the template dir was dead duplicates.
- 14 unused imports (`starlette.responses.Response` ×12, `datetime.timezone` ×2).

## 2026.6.208
Dev-testing UX fixes (storage + drying racks).
### Changed
- Storage cards: removed the moisture reading (M: %) from silo + bin cards (desktop + mobile);
  the high-moisture attention border is kept as the visual alert.
- Storage card edit form: **Seed Source is now a dropdown from the defined `seed_sources` list**
  (was free text). reference-data endpoint now returns `seed_sources`.
- **Drying Racks (mobile P04.R) redesign:** single-column, uniform, readable bin numbers (the
  number was light-on-white = invisible on dark theme; now an accent circle with white text);
  tapping a bin now **expands the assignment form inline directly beneath it (accordion)** and
  collapses on re-tap — instead of a separate form below the fold that looked unresponsive.
- Removed the dead duplicate `rack_assign_mobile.html` (legacy `_mobile.html` never rendered —
  `pick_template` always serves `mobile/rack_assign.html`).

## 2026.6.207
Grower-release blockers F4–F10 (2026-06-23 adversarial re-audit) ALL CLOSED. Dev only — main
held at v204; the v205+ stream promotes to main only on Peter's call + a Rule 186 browser smoke test.
### Fixed
- F4 (Rule 33): SAP-unrecorded report + 4 sibling long-row queries now `IN('active','complete')`
  so fully-weighed (`complete`) deliveries appear for SAP recording / stock counts. SAP workflow
  confirmed with Peter.
- F5 (Rule 153): grading source/output/sample edit+delete scoped `AND order_id = %s` (DB funcs
  take `order_id`; routes pass the path id) — cross-entity IDOR closed (output edit/delete reverses
  sloc_stock, so a mismatched child id could have corrupted another order's stock).
- F6 (Rule 37): `_json_safe()` (Decimal→float, datetime→ISO) on `rack_configs`/`sensor_history`/
  `fan_daily` before `| tojson` — kiosk racks + silo automation pages no longer crash once those
  tables have rows.
- F7 (Rule 157): `_validate_csrf` now fail-closed on all mutating methods incl. JSON-body (via
  `X-CSRF-Token` header); `/kiosk/` exempt (public, no session). Authenticated JSON fetches send
  the token. Regression test `TestCsrfJsonBody`.
- F8 (Rule 156/181): `secure=True` on `_csrf` + `sm_kiosk_operator` cookies.
- F9 (Rule 32): audit log on whole-DB restore + licence activate/deactivate.
- F10 (Rule 138/19): PAT store-POST failures DEBUG→WARNING; `sm_config` DDL moved from the
  request path to `schema.sql`.

## 2026.6.206
ADR-010 flip-readiness — cleared remaining verify-commit warnings (dev bump; the v205 security
deploy stays parked pending the F4-F10 audit gaps, Rule 105).
### Fixed
- R166: kiosk redistribution put the raw `ValueError` message into the redirect URL with no
  server-side log. Now logs server-side (`kiosk_redistribute_rejected`) and surfaces the
  (deliberate, user-safe) validation reason via a local var — no `str(exc)` on the response path.
### Changed
- R96/R118: CLAUDE.md golden_rules_version → v2.42; AUDIT.md refreshed to v2.42.

## 2026.6.205
### Fixed (security — 2026-06-23 adversarial re-audit findings F1–F3)
- **F1 / Rule 156 — public-kiosk stored XSS.** `kiosk_bins/silos/racks/grading` emitted DB-derived JSON into inline `<script>` via `{{ … | safe }}` on `json.dumps` (which does NOT escape `</script>`), letting an operator-named variety/silo/bin break out of the script tag on the **unauthenticated** kiosk. Now: backends pass the object (not a `json.dumps` string) and templates use `| tojson` (escapes `<`/`>`/`'`); innerHTML sinks wrapped in an `esc()` helper; `kiosk_grading` JS-literal switched to `| tojson`.
- **F2 / Rule 158 — unbounded request body DoS.** Added `BodySizeLimitMiddleware` (outermost): rejects bodies over the **1 MB** floor with 413, **counts streamed bytes** so a chunked/no-Content-Length body can't bypass it; DB-restore keeps a 50 MB override. Previously only `/api/restore-db` had a (bypassable) per-handler check; the public kiosk JSON endpoints were unbounded.
- **F3 / Rule 188 — no session revocation on credential change.** Added `auth.delete_sessions_for_user()`, wired into the user update route (password reset, role change, deactivation) and delete. A token issued before the change no longer outlives it; a role downgrade now takes effect immediately instead of at session expiry.
### Added
- `tests/test_security.py` — 5 behavioural regressions (Rule 192) named to the `REQUIRED_SECURITY_TESTS` `-k` patterns; red-team coverage 1/12 → **3/12** (157 CSRF, 158 body-size, 188 session-revoke). Suite 24 → 29 green.

## 2026.6.204
### Changed
- **Theme adoption — SM is now the reference adopter of the master Config List Manager (WR-PS-054, Golden Rules v2.36).** Re-synced `static/paddisense-tokens.css` byte-identical to the updated master and aligned all templates to the canonical component, removing local theme drift.
- **Migrated 8 utility name-overlaps to the master canonical names** (steward map): `u-w100`(100%)→`u-w-full`, `u-w100px`(100px)→`u-w100`, `u-muted`→`u-ps-text-muted`, `u-bold`→`u-fw700`, `u-center`→`u-ta-center`, `u-right`→`u-ta-right`, `u-flex1`→`u-flex-1`, `u-nowrap`→`u-text-no-wrap`, `btn-sm`→`ps-btn-sm`, `u-f13-muted`→`u-f13 u-ps-text-muted` across ~20 templates.
- **De-duplicated `app.css` (Rule 193.3 / WR-PS-051):** removed 180 rules that redefined master classes — `check-app-css.py` now reports **0 redefinitions** (app.css holds only SM-specific extensions). `app.css` 3618→3226 lines. Config tables/badges/buttons now render from the single master source.
### Fixed
- **Autosave-tick indicator was colourless** — config list rows used a local `.row-saved` whose `.ok`/`.error` referenced undefined `--success`/`--danger` tokens. Migrated to the master canonical `.ps-row-saved` (`--ps-success`/`--ps-error`), so the ✓/✗ save indicator now shows green/red.
- **Two pre-existing dangling theme classes** — `u-f85`→`u-f085` (Edit buttons), `u-grid-full`→`u-grid-span-full` (tare form). Rule 193 dangling sweep: 0.

## 2026.6.203
### Changed
- **Release-hardening pass — Stage-0 `[COMMIT]` hygiene cleared (R60 / R41 / R17); verify-commit now ALL CHECKS PASSED.**
- **Rule 60 (functions ≤50 lines)** — split the 6 remaining long functions by extracting cohesive helpers, no behaviour change:
  `grading.grading_new` + `grading_submit` now share `_render_grading_form()` plus `_serialize_slocs_with_stock()` / `_variety_screen_defaults()` (also closes a 4-way form-render duplication, Rule 59);
  `db/grading.add_grading_output` → `_resolve_output_classification()`;
  `db/redistribution.execute_redistribution` (89→~30 lines) → `_clean_redistribution_inputs` / `_load_and_check_sources` / `_create_redistribution_order` / `_pool_sources` / `_variance_to_waste` (the whole pool→allocate→waste→finalise sequence still runs in one `get_cursor()` transaction);
  `movement/gross.gross_submit` → `_assemble_gross_data()`;
  `movement/wizard.movement_submit` → `_parse_wizard_extra_fields()` + `_inbound_classification_missing()`.
- **Rule 41 (no inline styles)** — converted all 20 gate-flagged inline `style=` to canonical master utility classes (`u-flex`/`u-gap*`/`u-flex-1`/`u-mb12`/`u-f13`/`u-fw800`/`u-ps-white`) + SM-kiosk state classes in `app.css` (`sm-tint-*` moisture tints, `rack-legend-hidden`) + a `--ka-fill` custom property on the silo fill bar. No new master classes — reused A-Claude's WR-PS-050 utility consolidation.
- **Rule 17 (theme)** — re-synced `static/paddisense-tokens.css` byte-identical to the canonical master (`cmp` clean).
### Added
- **Rule 157 / 192** — behavioural CSRF test (`TestCSRF`): a token-less form POST returns 403 (+ a positive control proving a valid token is accepted). Suite 22→24, green.

## 2026.6.202
### Fixed
- **Rule 178 / KDP-013 (WR-PS-053) — removed all 19 residual inline `on*=` handlers** (silent no-ops under nonce-CSP) from `storage_table_mobile`, `storage_map_mobile`, `stock_report_mobile`: converted to `js-*` classes / ids + `addEventListener` (sort headers, storage tabs/filters, stocked pill, SLOC modal close/backdrop, season auto-submit). Reworded a stale `_bins.html` comment that tripped the gate. `check-orphan-bindings.py` now clean.

## 2026.6.201
### Changed
- **Bin-stock edit now enforces non-blank classification.** `POST /storage/api/sloc-stock/{id}/update` rejects (400) a bin **with stock** (weight > 0) that's missing variety, material type or generation — server-side guard plus a client pre-check on the storage-map edit modal (desktop + mobile). Emptying a bin (weight 0) may still clear the class. Closes the last intake-enforcement gap from the v200 audit.

## 2026.6.200
### Fixed
- **pytest harness now runs green (WR-PS-048)** — 22/22 pass. Root causes: (1) the app lifespan re-ran `ensure_database()` (full schema DDL) through the least-privilege app pool → `permission denied for schema public`; tests now set `SM_SKIP_SCHEMA_INIT=1` and use the existing addon-maintained schema via the admin pool. (2) `TestClient` used host `testclient`, which the ingress-trust check rejects → fixtures now use a trusted source IP `172.30.32.1` (in `172.30.32.0/23`) + `https://testserver` base URL. (3) the ecowitt poller is skipped in test mode (it broke lifespan teardown). (4) corrected a stale test path (`/moisture/api/readings` → `/moisture/api/history/{id}`). Production startup is unchanged (flag unset).

## 2026.6.199
### Fixed
- **Bin-stock edit (storage map → edit classification) was broken** — `POST /storage/api/sloc-stock/{id}/update` called `db.update_bin_stock`, which existed in `db/storage.py` but was never re-exported from `db/__init__.py`, so the live edit form (desktop + mobile) 500'd with `AttributeError`. Added the export (mypy now clean).
- **Rule 193** — defined the one dangling theme class `.ps-card-header` (used in `moisture_history.html`) in `app.css`.
### Changed
- Release-prep housekeeping: CLAUDE.md version → 2026.6.199, golden_rules_version → 2.33.

## 2026.6.198
### Changed
- **Data integrity — variety, material type and generation can never be blank on intake.** All inbound entry screens now require all three: **client-side** `required` on variety/material/generation (movement wizard step 2, bin weigh, weighbridge gross — desktop, mobile, kiosk), and **server-side** validation rejecting a blank classification on the create path (`movement/wizard.py`, `movement/gross.py`, `kiosk/bin_weigh.py`). Internal/outbound/redistribution inherit a valid (already non-blank) classification from existing stock, so they're unaffected.

## 2026.6.197
### Changed
- Redistribution destination dropdown now offers **empty bins + the bins picked as sources** (they'll be empty once pooled), added/removed live as you select — so you can re-bin into the same bins you're condensing.

## 2026.6.196
### Changed
- Redistribution step 2 destination list shows **empty bins only**.

## 2026.6.195
### Added
- **Variety filter** on the Redistribution / Condense source-bin grid (desktop, mobile, kiosk) — narrows the grid to one variety so you can find the bins to pool; the grid still smart-locks to the full variety+generation+material on first pick.

## 2026.6.194
### Added
- **Redistribution / Condense (kiosk)** — touch-friendly floor version at `/kiosk/redistribute` with a tile on the kiosk home, mirroring the desktop flow (tap source bins → holding, add destination bins + re-weighed kg, variance → WASTE). Reuses the same `execute_redistribution` engine.

## 2026.6.193
### Added
- **Redistribution / Condense (desktop)** — a new mode on Internal Transfer for re-binning a known weight of one seed type across bins (e.g. condense 5 bins → 4). Reuses the grading holding engine: pool same-class source bins into a virtual holding (releases them), allocate to destination bins at re-weighed actual kg, and any shortfall (holding − allocated) goes to a designated **WASTE** location as a recorded movement (auto-emptied). Single atomic transaction; enforces same variety+generation+material across sources; live holding/allocated/variance. New `db/redistribution.py` (`execute_redistribution`, `list_redistributions`), `order_type` discriminator on `grading_orders` (redistributions excluded from the grading list), and the seeded `WASTE` location. Mobile screen included; kiosk to follow.

## 2026.6.192
### Added
- **Outbound 1t Bins (P02.OB) — variety / material type / generation filters** at the top of the bin grid (desktop + mobile). Filters are populated only with the values actually present in stocked bins; selecting them shows/hides bin cards client-side (CSP-safe `addEventListener`, no inline handlers) with a live "N shown" count. Each card carries `data-variety`/`data-material`/`data-generation`; the handler passes distinct option lists.

## 2026.6.191
### Fixed
- **Internal Transfer tile (P02.1 → /movements/internal) returned a 500** (`{"error":"Internal server error"}`) in desktop/office mode. The desktop template `movement_internal.html` did not exist — only `mobile/movement_internal.html` and a stale orphan `movement_internal_mobile.html` — so `pick_template` resolved to a missing file and raised `TemplateNotFound`. Added the desktop `movement_internal.html`. Mobile was unaffected.

## 2026.6.190

### Changed
- `run.sh` now sources the canonical master theme at `/config/documentation/theme/paddisense-tokens.css` (WR-PS-045 / ADR-007), replacing the drift-prone `/config/theme/` path.
- Re-synced `seedmgr/static/paddisense-tokens.css` from the canonical master — now byte-identical (`cmp -s` clean).

### Added
- `docs/SESSION_PICKUP.md` (Rule 191) — durable in-repo pickup with live state, architecture brief, and audit backlog.

---

## 2026.6.189

### Changed
- P04.A drying rack section redesigned — racks shown as unit cards (like silos) with automation management, not individual bin position grids
- Each rack card links to new rack detail page (P04.R.D) with fan mode, thresholds, and bin summary
- Bin assignment removed from P04.A — stays on dedicated P04.R page

### Added
- Rack automation detail page (P04.R.D) — fan mode selector (Manual/Drying/Maintenance), temperature and humidity threshold controls
- `fan_mode`, `temp_min`, `temp_max`, `humidity_min`, `humidity_max` columns on rack_config (migration R35)
- Routes: `GET /storage/automation/rack/{id}`, `POST /storage/automation/rack/{id}/update`

## 2026.6.174–188

### Changed
- Mobile pages restructured to canonical PaddiSense base-mobile template (topbar, home button, page ID)
- 414 inline event handlers migrated to addEventListener for nonce CSP compliance
- Nonce-based CSP enabled (script-src with per-request nonce)
- CSRF middleware added with Content-Type enforcement
- Body size limit (1MB) on all requests
- Grading outputs inherit variety/generation/seed_source from source bins
- Storage map: full edit form for bin stock (variety, generation, material type, weight, moisture)
- Movement detail: grading output movements show warning banner and hide Edit button
- Grading SLOC dropdown shows `B-025 (Reiziq 500kg)` format
- Mobile rack assign: single column bins, stacked filters
- sloc_stock constraint changed from PK to UNIQUE NULLS NOT DISTINCT (migration R34)

### Fixed
- Grading output crash when generation_id had NOT NULL constraint
- Storage map modal always visible (app.css display:flex override)
- Async renderSlocDetail not awaited from .then() chain
- CSRF cookie secure=True blocking ingress (HA uses HTTP internally)
- Mobile storage map "Loading" black square (async render fix)
- Season validation error toast on grading order creation

## 2026.6.149

### Changed
- Full PaddiSense shared theme migration — all pages use consistent ps-* component classes
- Dedicated top bar on all pages (Home button + page code badge)
- Sidebar navigation with icons matching all other PaddiSense addons
- Grading detail: outputs section uses proper data table (matches sources table)
- Config page: all sections aligned with consistent accordion styling
- Dashboard: moisture tile links to browser page (was kiosk)
- Stock report: proper tab navigation, filter bar, button styling
- Alerts, badges, forms, tables all using shared theme classes
- Addon renamed from rrapl-seed-manager to paddisense-seed-manager

### Added
- "Add another like this" button on movement detail — repeat bin weigh with same metadata
- Season selector on bin weigh form
- Source and seed source: inline "Add new" option

### Fixed
- Storage: silo tab visibility fix
- Movement save fix (sloc_stock constraint)

### Security
- Entity staleness guard on Ecowitt poller
- Kiosk edit scoped to recent inbound movements only

---

## 2026.6.136

### Changed
- Unified PaddiSense dark theme — canonical hub tiles, dashboard
- Kiosk hub tiles updated

### Security
- Login rate limiting, session cookie hardening
- Browser cache busting (3-layer)

---

## 2026.6.120

### Security (adversarial audit — 8 findings fixed)
- R141/R144: `/api/errors`, `/api/perf`, `/api/backups`, `/api/docs`, `/openapi.json` moved out of public prefixes — require admin auth; `/health` stripped to liveness-only (`status`, `version`, `db_ok`)
- R93/R158: login rate-limiting (5 attempts/5 min per IP); restore endpoint body-size guard (50 MB)
- R143: `verify_password` + kiosk PIN switched to `hmac.compare_digest` (timing-safe)
- R156: `Secure` flag added to session + CSRF cookies
- R82: CDN Chart.js pinned to `@4.4.8` with SRI integrity hashes
- R146: formula-injection guard on all 3 CSV exports (`_csvSafe` helper)

### Added
- `docs/AUDIT.md` — 169-rule adversarial audit (6 parallel agents: 4 rule-sweep + 2 red-team), 12 remaining gaps documented

### Changed
- R92/R134: `lifespan` context manager replaces deprecated `on_event`; shutdown cancels background tasks + closes DB pools via `close_pools()`

---

## 2026.6.119

### Changed
- Version bump for production deploy (no code changes — promotes v118 security work to live)

---

## 2026.6.118

### Security (R80, R156, R166, R167)
- `SecurityHeadersMiddleware` added: CSP, `X-Frame-Options SAMEORIGIN`, `nosniff`, `Referrer-Policy`, `no-store` on HTML responses
- Ingress IP validation switched to `ipaddress` module (replaces fragile `startswith("172.30.32.")`)
- Reserved logging key `"filename"` renamed to `"backup_file"` (Rule 88)
- `str(exc)` in SAP bins response replaced with generic error message (Rule 166)

### Changed
- R60: 17 functions refactored to ≤50 lines — `auth_middleware` (4 helpers), `ecowitt_poller` (sensor parsing + gateway helpers), `storage.py` (context builders), `db/backup.py` `restore_data` (5 helpers), `db/sap_bins.py`, `db/movements.py` `create_movement`, `movement/gross.py`, `wizard.py`, `long_rows.py`, `config_admin/home.py`, `db/stock.py`
- `paddisense-tokens.css` synced to shared canonical theme library
- Burn forecast static HTML removed; dashboard comment cleaned

---

## 2026.6.117

### Changed
- WR-PS-026: replaced simplified single-token `pat_manager.py` with the canonical two-token implementation (matches GIS/Farm pattern)
- Dev PAT no longer embedded in git remote URLs (Rule 80 fix); remotes use clean `https://github.com/PaddiSense/<repo>.git`
- Supervisor PAT (read-only, fine-grained) now used only for store URL registration; dev PAT used via credential helper at push time

---

## 2026.6.116

### Changed
- Least-privilege DB role `seed_app` activated after schema init (Rule 138); falls back to admin role if role is missing (`init_app_pool`)

---

## 2026.6.115

### Fixed
- Removed `-> Response` return type annotation from `response_class=HTMLResponse` routes — caused FastAPI response-model conflict crash on startup

---

## 2026.6.114

### Changed
- Dockerfile `ARG BUILD_VERSION` cache bust moved before `COPY seedmgr/` to force code-layer invalidation on every build

---

## 2026.6.113

### Added
- `ARCHITECTURE.md` and `SECURITY.md` created at repo root (stack overview, module map, auth layers, known gaps)

### Changed
- R93: structured logging — all `log.info/warning` calls in `db/` and support modules now include `extra={}` fields (`action` key + context); ~40 lines across 11 files
- 15 ruff violations fixed (import ordering, unused imports)

---

## 2026.6.112

### Changed
- Version bump to force Docker image rebuild (no code changes — Dockerfile layer invalidation)

---

## 2026.6.111

### Fixed
- `HTMLResponse | RedirectResponse` union return types on router functions caused FastAPI crash; replaced with plain `Response`

---

## 2026.6.110

### Fixed
- `| object` return type syntax on several routes caused FastAPI startup crash; corrected to plain `Response`

---

## 2026.6.109

### Fixed
- `response_model=None` applied to all 130 routes — FastAPI was crashing on startup because HTML routes lacked an explicit response model

---

## 2026.6.108

### Changed
- R29: `pyproject.toml` migration — single config file (replaces `setup.cfg` / `setup.py`); `ruff.toml` E402 per-file handling
- R59: `requirements.lock` added — all transitive dependencies pinned
- R60: full compliance — all functions now ≤50 lines (initial batch across `_csrf.py`, `auth.py`, `config_admin/`, `movement/`, `db/`)
- R92: CSRF middleware token comparison hardened
- R93: `run.sh` gates 2–4 (ruff, mypy, bandit, pytest) dev-only; skipped in production container

### Fixed
- 181 bare `except: pass` patterns replaced with `log.debug(...)` (removes `S110` ruff suppression)
- Last 2 import-sorting violations fixed

---

## 2026.6.107

### Added
- Full quality stack: smoke tests (`tests/`), `mypy.ini`, `pytest.ini`, 4-gate `run.sh` (ruff → mypy → bandit → pytest)
- `ruff.toml` with auto-fix for import sorting, type annotations, unused imports; unsafe-fixes applied
- `bandit==1.9.4` pinned (1.9.0 does not exist on PyPI)

### Changed
- Dockerfile updated to copy `tests/`, `mypy.ini`, `pytest.ini` into image
- `.gitignore` updated for `.mypy_cache/`, `.pytest_cache/`, `*.egg-info/`

---

## 2026.6.106

### Changed
- `panel_title` changed from `PaddiSense SM` to `Seed Manager` (config.yaml)
- Application logging fixed — `logging.basicConfig()` added to `__main__.py` so addon logs are visible (Rule 88)

### Fixed
- Open redirect in `set_mode` — `next` parameter now validated against allowed paths; off-site redirects blocked
- `samesite="lax"` added to kiosk operator cookie
- Grading `generation_id` `NameError` — `None` fallback instead of undefined variable
- 6 security findings from mock pen test: random admin password on first run, ingress IP validation, path traversal in restore-db, export/restore auth (role check replaces header-only), SQL injection guard in restore (table allowlist), licence endpoint auth

---

## 2026.6.105

### Fixed
- SAP backfill: silo SAP location now set to silo number only (`S-01` → `1`); previous backfill was setting wrong value
- Editable SAP bins config page added; burn forecast page removed

### Added
- SAP bin allocations: reference table, lookup function, backfill migration (v102–v105 incremental)
- Licence API (`/api/licence`) for central management queries from Core heartbeat
- Licence enforcement cache — `_licence_cache` with TTL; enforcement gate middleware

### Changed
- DB password default changed to `homeassistant` for out-of-box setup
- PAT auto-rotation on startup — reads from `/config/secrets.yaml`
- `pat_manager.py` f-string syntax fix + bare excepts cleaned (fortnightly audit)
