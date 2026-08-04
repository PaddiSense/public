# Changelog


## 2026.8.13 — the commissioning marker fails CLOSED with no evidence

### Changed
- **An add-on must be activated before it opens.** The commissioning marker previously failed
  OPEN on a read error, which gave the first-activation gate away on a box that had never held
  a licence. It now fails CLOSED when there is no evidence of commissioning (Peter,
  2026-08-04): activate to open, and once open a revoke never takes it away.
- A running, already-commissioned box is unaffected — `_box_commissioned_cached` returns the
  cached True before ever reading the database — so the WR-PS-421 protection is intact.
- Failing closed costs nothing real: with an unreadable database the add-on cannot serve
  anything anyway, because every page needs it.

### Tests
- `test_an_unreadable_marker_fails_OPEN` **inverted** to `..._fails_CLOSED` rather than
  deleted, so the old behaviour cannot creep back unnoticed.


## 2026.8.12 — Security: cryptography CVEs + PLAT-08 hash-pinned build

### Security
- **`cryptography` 48.0.1 → 50.0.0** — CVE-2026-69247 / 69248 / 69249. On every addon this is
  the Ed25519 implementation behind `core/licence_verify.py`, i.e. the licence trust plane.
  **49.0.0 does not clear it** — it fixes 69248 and 69249 and leaves 69247 (WR-PS-426).
- **PLAT-08 — the image now installs `requirements.lock` with `--require-hashes`.** It fails
  closed: a package whose archive does not match its recorded hash, or any dependency missing
  from the lock, aborts the build. The Hone register carried PLAT-08 as a closed HIGH while
  only 3 of 11 addons actually satisfied it.
- Pinning revealed an **existing** exposure rather than creating one: the unpinned build was
  already resolving vulnerable transitive packages, and the release gate could not see them
  because it audits `requirements.txt` while these are transitive.

### Changed
- `requirements.lock` regenerated hash-pinned. Where transitives were flagged, upgraded with
  targeted `--upgrade-package` rather than a blanket refresh, so the package-set diff stays
  contained to the security fix — same package count, only the flagged packages moved.

### Evidence
- `pip-audit -r requirements.lock` → exit 0 (the file the image installs).
- Full suite green against the **installed** upgraded packages, not the versions replaced —
  `urllib3` 1.x → 2.x is a major bump and a clean audit proves nothing about behaviour.


## 2026.8.11 — WR-PS-421 follow-up: write the commissioning marker at startup

### Fixed
- **An add-on nobody opened in a browser would still lock out on the first licence removal.**
  `licence_gate` records the marker on the licensed path, but it exempts `/api/licence`, `/health`,
  `/static` and `/login` — the paths Core's heartbeat and the Supervisor health probe use. So the
  marker was never written on a quiet add-on, and the WR-PS-421 protection did not apply to it.
- The marker is now recorded at startup, which is deterministic: every add-on restarts on upgrade.
- Placed **after** the app pool is live. `_is_licensed()` reads the database and fails closed, so
  calling it earlier would silently write nothing — the same class of bug in a different place.

### Added
- `tests/test_revoke_never_locks_the_box.py` +1, asserting both that startup records the marker and
  that it runs after the database is up. Proven failing against the real pre-change module.


## 2026.8.10 — WR-PS-216: re-vendor the log redactor (it was leaking secrets in clear)

### Fixed
- **The vendored `log_redactor.py` had drifted BEHIND canonical (WR-PS-616), in both directions.**
  - **Under-redaction (the security half):** every **owner-prefixed** secret label —
    `ps_api_key:`, `gsm_shared_secret:`, `<addon>_admin_key:` — was written to the log **in clear**.
    The pattern's leading `(?<![A-Za-z0-9_])` boundary refuses to match `api_key` inside
    `ps_api_key`, because the preceding character is `_`. It was never one key; it was every
    prefixed form, and this fleet names secrets that way as a matter of course.
  - **Over-redaction (the diagnostic half):** token prefixes matched inside ordinary identifiers, so
    `_ensure_sentinel_grower_basic` logged as `_ensure_<redacted>`. In practice the more damaging
    one — it silently mangles the tracebacks people read during an outage.
- Re-vendored `cmp -s`-identical with canonical.

### Added
- `tests/test_log_redactor.py` +3 — both failure directions plus a byte-identity assertion against
  canonical. All three proven failing against the real drifted file. The existing 5 tests covered
  **neither** direction, which is precisely why a green suite hid a leaking redactor (Rule 192).

### Note
- Fleet-wide condition, not a per-addon slip: **10 of 11 add-ons** carried the same stale copy
  (WR-PS-216). Released versions predate the canonical fix, so growers were exposed too.


## 2026.8.9 — WR-PS-421: an unlicensed box is not a LOCKED box

### Changed
- **`licence_gate` now fires only for a box that has never been commissioned.** Peter's ruling
  (2026-08-03): *"the only thing that stops is comms with GSM and ADMIN. machine data etc all keep
  working."* Core v2026.8.9 removed the fan-out that *sent* a revoke as a deactivate; this removes
  the receiving half, so the lockout cannot happen by any route.
- Previously ANY absence of a licence denied every page and API. "Absence" covered far more than a
  revoke: expiry, an operator removing the licence to rotate it, or a plain database hiccup —
  `_is_licensed()` fails closed. Demonstrated live 2026-08-03, every add-on showing the lock
  screen over a working farm. A commercial decision could stop irrigation and safety monitoring.
- The licence page remains correct **first-run onboarding** for a box that has never been
  licensed, so the commercial gate at first use is unchanged.

### Added
- `_note_commissioned()` — records a durable write-once marker in the addon's config table while
  the box is licensed. Marking from the HEALTHY state is what makes this retroactive: every box in
  the field is licensed right now and carries no marker.
- `_box_commissioned_cached()` — reads it, and deliberately fails **OPEN**, the opposite of
  `_is_licensed()`: a database wobble must never be the reason a grower loses their own box.
- `tests/test_revoke_never_locks_the_box.py` (6) — asserts the gate actually calls both helpers, so
  a helper the gate never invokes cannot pass for a fix. Five proven failing against the real
  pre-fix module.


## 2026.8.8 — Fix: Planner could not verify ANY signed licence (missing `cryptography`)

### Fixed
- Activating a licence returned **HTTP 500** with `ModuleNotFoundError: No module named
  'cryptography'`. `core/licence_verify.py` has imported `cryptography` for Ed25519 verification
  since v2026.7.1, but the dependency was **never added to `requirements.txt`** — every sibling
  addon pins `cryptography==48.0.1`; Planner was the only one missing it.
- Latent until now because Planner is pre-first-release and had never verified a signed licence in
  anger. It surfaced the moment a real Admin-signed code was pasted in. Pinned to the identical
  version the rest of the fleet uses.
- **Caught before Planner's first grower release** — it was queued in the release train and would
  have shipped with a licence path that 500s on every activation (WR-PS-203).

## 2026.8.7 — WR-PS-210: accept an operator's own deactivate from this box's console

### Fixed
- Core's console "remove licence" button carries no Admin signature — it is not a remote revoke —
  so this addon refused it `unsigned_rejected` and the grower could not remove a licence from their
  own box. Now a caller presenting a valid **box-key internal-auth token** (WR-PS-204) is accepted
  as a local operator act: cryptographic proof of "Core, here", not `/23` position.
- **Admin's remote revoke is unchanged** and still requires the Ed25519 signature; only the local
  path is opened. Tests: `tests/test_local_operator_deactivate.py` (4) — no token is not local
  authorisation, a valid token is, the route actually consults the check, and signature
  verification is still on the route so the narrow path cannot become a general bypass.

## 2026.8.6 — Grower boxes trust ONLY the prod Admin signing key (per-lane keyring)

### Security
- The vendored Admin keyring carried **two** keys since 2026-08-01: `admin-2026a` (prod) and
  `admin-dev-2026a` (the DEV Admin instance). Signature verification resolves the licence's own
  `key_id`, not `active` — so shipping both would make the **development** Admin a trusted licence
  authority on every grower box. Peter ruled it out (2026-08-03) before the first release that
  would have carried it; no released version has ever contained the dev key.
- `data/admin_signing_pubkey.json` is now the **prod-only** keyring, re-vendored byte-identical
  from canonical. Dev boxes re-add the dev key out-of-band via `PS_ADMIN_PUBKEY_FILE` (a mechanism
  `licence_verify` already supports) pointing at `/share/paddisense/admin_signing_pubkey.dev.json`
  — a file growers never have, so `run.sh`'s conditional export is a no-op on a grower box.

## 2026.8.5 — WR-PS-201 §9-A: a failed licence save hands back the reserved nonce

### Fixed
- `verify_artifact` RESERVES the signed artifact's one-time nonce the instant the signature checks
  out — *before* anything is persisted. When the save then failed (classically `planner_app` missing its
  DML grant on a fresh or owner-flipped box), the reservation stood, so Core's retry of the
  IDENTICAL artifact was judged a **replay** and the grower was shown
  **"Licence signature verification failed"** for what was a database fault. That false diagnosis is
  what sent two grower boxes down the wrong path on 2026-07-30.
- Re-vendored the canonical `core/licence_verify.py` (byte-identical, `cmp -s` clean) to pick up
  `release_nonce()`, and wired it at the licence-save site: on a save that is genuinely dead —
  *after* the in-line grant self-heal and retry — the nonce is released so the retry is judged on
  its merits. On SUCCESS the reservation stands, preserving the single-use guarantee.

### Tests
- `tests/test_licence_nonce_release.py` — release frees a reserved nonce; the instruction-shaped
  `target` subject key works as well as `licence_id`; and an unsigned/partial payload is a safe
  no-op that must NOT over-release.

## 2026.8.4 — Fleet-hardening parity for first grower release (WR-193/203)

Planner was skipped by the WR-201/152/603 fan-outs; brought to fleet parity before its first grower cut.

### Security / reliability
- **WR-201 grant self-heal** — new `core/db/_pool.py::grant_app_privileges()` ensures the `planner_app`
  DML grants from the admin pool at startup (called in `ensure_database` before `init_app_pool`),
  idempotent + non-fatal. Without it a fresh box strands on `permission denied`.
- **WR-603 activate self-heal+retry** — `api/licence.py` `_persist_licence()` self-heals the grant
  IN-LINE and retries the save once on `permission denied`, so a first-ever activation can't 500/
  false-fail as "signature verification failed" (the Store grower incident + PROD Safety first-seed class).
- **WR-152 F-A1 box-binding** — `_verify_instruction_signature` rejects 400 a validly-signed
  deactivate/revoke whose subject (`licence_id`/`target`) != this box's `licence`/`grower_id`
  (cross-box replay closed). (F-A2 no-bare-TOFU N/A — Planner's access-sync is the simple grant-cache,
  not the §9-A.9 verify-and-pin; that WR-108 gap is flagged separately.)
- **ADR-020 vendored-sync** — re-vendored `core/_log_redactor.py` byte-identical to canonical (it had
  drifted, missing the newer masking) + registered its per-addon dest in `vendored_manifest.json`.
- Tests +3 (F-A1 cross-grower→400/own→ok; `_persist` fail→grant→retry→ok; grant revoke→restore).

## 2026.8.3 — ADR-020: canonical `core/ingress.py` upgraded (cached, fail-closed)

### Changed
- Re-vendored `core/ingress.py` (canonical) — `is_ingress` now uses the fleet-standard
  cached, fail-closed infra-peer resolution (ADR-020 Option A, Core's model) instead of a
  per-request DNS lookup. No behaviour change beyond the perf fix + loopback trust.



## 2026.8.2 — ADR-020 convergence (canonical `core/ingress.py`)

### Changed
- Vendored `core/ingress.py` (canonical `is_ingress` resolved-proxy pin + `INGRESS_SESSION`/
  `INTERNAL_SESSION`) from `documentation/contracts/ingress.py`; `core/auth.py` imports it instead
  of a local copy. Green through `check-fleet-structure` + `check-vendored-sync`. No behaviour
  change — the ingress logic is byte-identical, now canonical-sourced. Vendored `core/internal_auth.py`.


## 2026.8.1 — Pin ingress trust to the resolved proxy peer (Rule 167/172/187)

### Security
- Pinned `core/auth.py::is_ingress` to the **exact resolved IP** of an HA ingress
  proxy (`supervisor`/`homeassistant`/`hassio`) instead of trusting the broad
  `172.30.32.0/23` subnet. Under the subnet trust, any sibling addon on the hassio
  bridge could forge the `X-Ingress-Path` header and obtain this addon's admin
  ingress session. Matches the PWM/Farm reference fix; part of the fleet-wide sweep.
  This addon exposes no sibling-consumed proxy, so the change is a pure security
  tightening (no internal-token channel needed here).

## 2026.7.7 — Trust the DEV Admin signing key (dev-box enrolment)

### Changed
- Re-vendored `paddisense_planner/data/admin_signing_pubkey.json` from the canonical
  `documentation/contracts/admin_signing_pubkey.json` — adds `admin-dev-2026a` beside prod
  `admin-2026a` so this DEV box verifies DEV-Admin-signed licences (per-key_id, additive; prod key
  unchanged). Fleet keyring alignment (Core v2026.7.58 + the other 9 addons). Planner also entered the
  fleet release manifest (`_release-manifest.sh`) for dev-deploy; its public catalog + `build-planner`
  GHCR workflow are owed (WR → G, first-release onboarding). ⚠ dev key rides to PROD at the first
  grower cut — per-lane keyring decision owed to Peter+A.

## 2026.7.6 — owner-login rotation self-heal (WR-PS-192/074 structural fix, port of Weather bd8d124)

### Fixed
- **Incident 2026-07-27 (Weather was the victim; Planner shares the vulnerable pattern):**
  a flipped `*_owner` login uses a STATIC stored options password; a DB-role seed re-mint
  changes the Postgres role underneath it and the addon strands on its next restart
  (DB init fails → licence gate fail-closed → licence screen).
- Structural fix in `core/db/_pool.py`: for `*_owner` logins (e.g. `planner_owner`) the
  password is now DERIVED from the `/share` box key first (the fleet's derivation truth,
  Core v2026.7.44), with the stored options password as fallback; loud WARNING when the
  stored copy is stale. `db_user: postgres` (pre-flip) boxes are unaffected — stored
  password only, never derived.
- **Both pools gained the auth-failure rebuild-and-retry self-heal** (`_acquire_conn` +
  `_reset_app_pool`/`_reset_admin_pool`): Planner had never received the 2026-07-09
  app-pool self-heal layer, so this port lands the app-pool self-heal AND the new
  admin/owner-pool self-heal together. Fail-closed pool selection (R173) untouched.
- Regression tests (`tests/test_pool_selfheal.py`, +7): app + admin pool self-heal,
  non-auth errors still propagate, owner candidate ladder, and end-to-end
  stale-stored-password recovery on the real test cluster (proven-fail against the
  pre-fix code in the donor).

## 2026.7.5 — WR-PS-183: redactor re-vendored (all six GitHub token classes)

### Changed
- **The vendored log redactor re-synced byte-identical to the patched
  canonical**: `gh[posur]_` now masks `ghp_`/`gho_`/`ghs_`/`ghu_`/`ghr_`
  alongside `github_pat_` (WR-PS-183 completeness sliver). Shared test
  refreshed (+4 fixtures).

## 2026.7.4 — WR-PS-080: base-image digest pin (last of 13)

### Changed
- **`FROM python:3.12-slim` is now digest-pinned** to the fleet-standard sha256
  (matches PWM/SeedMgr/SugarSense et al.) — Planner was already on 3.12 but was
  the one addon still floating on the tag. Closes the WR-PS-080 fleet row
  (Hone SCAL-03 propagation, 13/13).

## 2026.7.3 — WR-PS-179: canonical log redactor vendored + wired

### Added
- **Structural log redaction at the entry point.** Planner previously shipped
  no log redactor. `core/_log_redactor.py` is now a byte-identical vendor of
  the fleet canonical `documentation/shared/log_redactor.py` (GSM⊕Core
  superset: cloudhook URLs, PATs, bearer/DSN/`enc:` tokens, labelled secrets,
  portal/Resend keys, email + phone PII), wired as the root
  `RedactingFormatter` with uvicorn `log_config=None` so uvicorn.access/error
  pass through it too. Shared 30-case behavioural test adopted. Closes the
  Planner SEC-17/KEY-01/DATA-01 cell.

## 2026.7.2 — Fix: real Admin-signed instructions were rejected (WR-ADMIN-006 canonical re-vendor)

### Fixed
- **Re-vendored `core/licence_verify.py`** byte-identical to the fixed canonical
  (`documentation/shared/`, commit 23378e0): `verify_artifact` now accepts the licence id under
  `target` (the real instruction wire shape, §4/§9-A.5.2) as well as `licence_id` — pre-fix, every
  REAL Admin revoke/deactivate was rejected as `invalid_signature` (latent since 2026-07-01; found
  by A's WR-ADMIN-006 live test; GSM proved the fix end-to-end on v2026.7.51). Log labels split so
  a missing id no longer mislabels as a sig/replay failure. New positive regression
  `TestPositiveInstruction` (Rule 106): a genuinely signed, target-only instruction MUST verify —
  the missing test whose absence let an always-reject verifier pass every gate.

## 2026.7.1 — SEC-01/04 signed-licence receive-side built, enforcement ON from day one

### Added
- **Admin Ed25519 signature verification on both mutating licence paths** — Planner was the last
  P-pool addon with NO signature verify (the 07-13 warn→block sweep found it: plaintext-code
  activate, naked deactivate). Vendored `core/licence_verify.py` (byte-identical to
  `documentation/shared/`) + pinned `data/admin_signing_pubkey.json`; `/api/licence/activate`
  handles both the pasted-`code` and Core-heartbeat `signed_licence` shapes;
  `/api/licence/deactivate` requires an Admin-signed instruction. Lands directly in the fleet's
  post-flip posture: `PLANNER_SIGNED_LICENCE_ENFORCE` defaults ON (`=0` kill-switch; forgeries
  fatal even kill-switched). `bound_fp` persisted from the licence for the coming WR-PS-108
  access-sync receiver. Companion Core change (v2026.7.16) adds planner to the SEC-04 forward map.
  First July cut — CalVer rolls 2026.6.57 → 2026.7.1. Tests: `test_licence_signed.py` (12).

## 2026.6.57 — Module-access gate (WR-PS-109 catch-up; SEC-04/SEC-09 Option B)

### For growers (plain English)
- Planner now respects the per-user module access set in PaddiSense Core: a farm user who
  has not been given Planner can no longer open it. Users with Planner ticked (or admins)
  see no change.

### Detail (Claude-facing)
- **Found live by Peter 2026-07-10:** `testoperator` reached Planner with full access
  despite no Planner grant in Core UA01. Planner was never in the WR-PS-109 propagation
  lists (dev-only addon, no build workflow) so it had no `module_gate` receiver — Core's
  grant pushes 404'd — and its HA-ingress default is a full admin session.
- Vendored `core/module_gate.py` from the Farm reference (Option B semantics: never-synced
  → open; configured box → ungranted user DENIED; admin/all_access → allowed; corrupt cache
  → open, never brick the box). `MODULE_KEY = "paddisense-planner"`.
- New `POST /api/access/sync` receiver (main.py, `_verify_internal` trust boundary — same
  as the licence-forward path; push-signature hardening rides WR-PS-108 fleet-wide).
  Added to `_PUBLIC_PATHS` (cookie-less M2M POST does its own caller check).
- Auth middleware now applies `_access_gate_denies()` on ingress requests for both API and
  page branches (mirrors Farm/PWM/Safety wiring exactly).
- `tests/test_module_gate.py`: gate-decision matrix + end-to-end 403 through the real
  middleware + KDP-017 reachability regression (cookie-less push not intercepted by
  CSRF/auth) + a real-push-then-enforce e2e.
- NOT changed: Planner's local 5-role ladder and cookie-login path (fleet parity — the
  add-on-level grant IS the authorization, per Peter's ratified Option B model).

## 2026.6.56 — Prefer dedicated /share DB-role key (WR-PS-088 split rollout)

### For growers (plain English)
- No change to any screen or number you see. Behind the scenes, Planner now reads its
  database password from a dedicated key file that Core publishes, falling back to the
  existing key during the rollout. Identical behaviour today.

### Maintenance / audit
- **DB auth:** `core/db/_pool.py` `_read_box_key()` now prefers the dedicated
  `/share/paddisense/db_role.key` for the `planner_app` DB password; falls back to
  `master.key` during the WR-PS-088 split rollout — no behaviour change today (both
  keys carry the same value until the 1b flip). Fail-closed / no-superuser-fallback
  logic unchanged.

## 2026.6.55 — Release-gate housekeeping: clean type checks, patched dependencies

### For growers (plain English)
- No change to any screen or number you see. This release is a maintenance tick that
  tightens the safety net around Planner:
  - We updated two behind-the-scenes software libraries to their latest secure versions,
    closing off publicly known security weaknesses (in the file-upload handler and the
    test tool). Nothing you do in the app changes.
  - We tidied the code so our automated type-checker passes cleanly, which helps us catch
    mistakes before they ever reach you.
  - The "budget setup" and "staff" pop-up windows now use the shared PaddiSense pop-up
    styling instead of a private copy, so they look and behave consistently with the rest
    of the platform.

### Maintenance / audit
- **Security patches:** `python-multipart` 0.0.27 → 0.0.31 (CVE-2026-53538/53539/53540) and
  `pytest` 8.4.1 → 9.0.3 (CVE-2025-71176). pip-audit now reports 0 known vulnerabilities.
- **mypy clean:** annotated the middleware `dispatch` methods, widened P&L handler return
  types to `dict | JSONResponse`, typed the budget staff-allocation cursor helpers with the
  real `RealDictCursor`, made `log_audit` accept a structured dict (stored as JSON), coerced
  water-ledger form values through `str()` before `float()/int()`, and guarded a None paddock
  id in the crop rotation engine. No `# type: ignore` shortcuts added.
- **Theme (Rule 193):** the reinvented `.ps-modal-overlay` class (which rendered unstyled)
  was replaced by the canonical master `.ps-modal-backdrop` across the four budget pop-ups;
  mobile keeps its bottom-sheet layout via a small override.
- **CI:** the ADR-010 pre-release gate is now BLOCKING (was rollout/informational).

## 2026.6.54 — Security-test enforcement re-confirmed (ADR-010 manifest)

### For growers (plain English)
- No behaviour change. This is a safety-audit tick: we re-checked that every automated
  security test that must exist for Planner does exist and passes, and that the test
  database rebuilds cleanly from scratch. Your data and screens are unchanged.

### Security / audit
- **ADR-010 required-security-test manifest re-confirmed enforceable.** All 5 applicable rows
  (R157 CSRF→403, R158 oversized-body→413, R171 forged-ingress alert, R187 forged-XFF ignored,
  R190 login non-enumeration) each collect ≥1 behavioural test under their `-k` selector; the 7
  N/A rows (142/146/153/154/159/188/189) were re-verified against the real code, not trusted.
- **Test-DB reproducibility proven:** dropped `paddisense_planner_test` and re-ran the suite —
  `conftest` recreates the DB + full schema + all migrations as the admin role idempotently
  (19 passed, 0 failed). Request-path stays on the admin pool for tests via `PLANNER_SKIP_APP_POOL`
  because the least-priv `planner_app` role is not granted on the disposable test DB (documented
  partial — DDL bootstrap must run as admin, so forcing least-priv in tests would need a prod-code
  change, which this audit did not make).
- **AUDIT.md accuracy fix (R159):** corrected the SSRF N/A rationale — the sibling "farm_sync" is a
  direct DB-to-DB `psycopg2` connection to fixed sibling databases on a fixed host, NOT an HTTP fetch
  of any URL; there is no server-side URL fetch surface at all, user-controlled or otherwise.

## 2026.6.53 — 🔴 SEC: fail-CLOSED DB pools + fleet catch-up (v2.49 rebase-audit)

### Security
- **DB pools are now fail-CLOSED (WR-PS-081 / R160 / R173):** `_init_app_pool` no longer
  swallows an app-role auth failure and silently reuse the postgres **superuser** pool for
  request-path queries. Once the least-priv `planner_app` pool is activated it is used or the
  query **raises** — a mis-provisioned app role is a loud failure, never a silent privilege
  escalation of every request.
- **Shared box key (WR-PS-081):** `_pool` reads `/share/paddisense/master.key` (the key Core
  publishes) before the local `/data/keys/master.key`, so `planner_app`'s derived password
  matches the role Core minted.
- **Forged-ingress alert (R171/R187):** an `X-Ingress-Path` from an off-Supervisor-network
  socket now raises a `WARNING event=ingress_spoof_attempt` — the forged header is ignored,
  the attempt is logged.
- **+4 red-team regression tests:** R158 oversized-body→413, R187 forged-XFF-ignored,
  R171 spoof-alert, R190 login non-enumeration (byte-identical unknown-user / wrong-password).

### Changed
- **Shutdown (R92/R134):** shutdown handler now calls `close_pools()` (was a broken import of a
  non-existent `_pool` symbol that raised on every shutdown); both pools closed cleanly.
- **db/__init__ (R79):** `__all__` now exports `init_app_pool` and `close_pools`.
- **ADR-011 §5:** startup config validation extracted into a public `validate_config()` invoked
  first in the startup handler.
- **ADR-011 §6:** `tests/conftest.py` forces a disposable `paddisense_planner_test` DB (was
  pointed at the LIVE DB — WR-PS-069) and keeps request-path on the admin pool for tests.
- **CI (fleet standard):** added `.github/workflows/ci.yml` — compileall + ruff + bandit blocking,
  mypy + pip-audit informational, Python 3.12.
- **SCAL-03:** Dockerfile base `python:3.11-slim` → `python:3.12-slim`; ruff/mypy target 3.12.
- Golden Rules audit rebased v2.44 → **v2.49**.

### Known (pre-existing, not introduced here)
- App pool activates in production but the request-path still uses the admin pool on the
  disposable `*_test` DB (the `planner_app` role is not granted there) — test-only, guarded by
  `PLANNER_SKIP_APP_POOL`.

## 2026.6.52 — 🔴 SEC: fix X-Ingress-Path header-spoof bypass + Bearer == compare (fleet sweep)

### Security
- **is_ingress now requires the client IP on the Supervisor /23** before trusting X-Ingress-Path
  (was unconditional → any client setting the header got role:admin — remote-admin bypass).
- **licence _verify_internal uses hmac.compare_digest** for the Bearer token, not `==` (Rule 143).
- Found by the 2026-07-04 fleet-consistency gate (check-fleet-consistency.py). Planner still owes the
  full catch-up (fail-closed admin/app pool, /share key, ci.yml, py3.12, main-branch flip).

All notable changes to PaddiSense Planner are documented here.

## 2026.6.51
Security: public `GET /api/licence` is now liveness-only (Golden Rule 144, WR-PS-066).
### Fixed
- **R144 licence leak:** the unauthenticated `GET /api/licence` poll (Core calls it
  without auth) returned the full licence string plus `product`, `exp`, and `grower_id`.
  It now returns `{"enrolled": <bool>}` only — fleet-correct (Farm/ASM) liveness shape.
  No detail leaves the addon over the public endpoint. `activate`/`deactivate` unchanged.

## 2026.6.50
ADR-010 flip-readiness — verify-commit CLEAN (0 warn / 0 viol). No functional change.
### Changed
- **R178 (206 inline handlers → 0):** every inline `on*=` handler (click/change/input/blur/
  focus/mousedown/toggle, incl. JS-built strings) converted to `js-*` class + `data-*` attrs +
  delegated `addEventListener` (capture for non-bubbling blur/focus/toggle). Per-page
  `<script>` restructure (block moved out of base's `<script>`) so the orphan-checker sees the JS.
- **R41 (134 inline styles → 0):** extracted to `pl-` CSS classes; dynamic/conditional values →
  CSS custom properties / class toggles.
- R17 theme re-sync; R193.3 (`ps-section`/`ps-btn-outline` → `pl-` to stop redefining master);
  R157 CSRF reject 415→403 + behavioural test. Docs: CLAUDE/AUDIT golden_rules → 2.42.
### Note
- Planner is pre-maturity (pages still being finished/tested) — a full click-test pass is the
  natural verification as each page is completed.
### Known (pre-existing, not introduced here)
- `permission denied for schema public` on the test DB (least-priv role not fully provisioned/
  granted) — same class as the SugarSense finding; separate follow-up.

## v2026.6.49 (2026-06-21)

- run.sh: source canonical master theme on startup (WR-PS-045/ADR-007)
- Re-sync `static/paddisense-tokens.css` byte-identical to canonical master
- Add `docs/SESSION_PICKUP.md` durable in-repo pickup (Rule 191) with audit backlog
- Sync CLAUDE.md Golden Rules reference (v2.14 → v2.24)

## v2026.6.2 (2026-06-04)

- Decompose oversized water_page and rotation_page into helper functions (Rule 60)
- Replace 5 hardcoded hex colours with CSS variables (Rule 17)
- Add shutdown handler to close DB pool (Rule 92)
- Add startup environment variable validation (Rule 126)
- Document all module-level mutable globals (Rule 128)
- Add two-token PAT manager (WR-PS-026)
- Create develop branch (Rule 71)
- Add CHANGELOG.md (Rule 84)
- Update CLAUDE.md version and rules reference (Rule 98)

## v2026.6.1 (2026-06-04)

- Initial standalone Planner addon extracted from GIS
- Water Ledger: licences, allocations, transactions, available water calculation
- Rotation Grid: paddock x season x crop assignment with autosave
- Inputs: price sets (Hi/Avg/Low) and chemical brew recipes
- Licence gate middleware, auth with 5-role model, login/logout
- Desktop and mobile responsive layouts
- Health endpoint, error tracker, perf tracker
- Smoke tests with real DB integration
