# Changelog


## 2026.8.6 — Log redaction adopted (this addon had NONE) + prod-only Admin keyring

### Security
- **This addon shipped with no log redaction of any kind.** The canonical `RedactingFormatter`
  (SEC-17 / KEY-01 / DATA-01; Rules 88 / 164 / 166) that the rest of the fleet has carried since
  WR-PS-179 was never adopted here, so secrets (cloudhook URLs, PATs, bearer/DSN/`enc:` tokens,
  labelled secrets) and PII (email, phone) reached the log verbatim — including uvicorn's own
  access/error lines and any exception traceback. Vendored byte-identical from
  `documentation/shared/log_redactor.py` and **wired at the entry point**, with
  `log_config=None` so uvicorn's loggers propagate through the formatter instead of bypassing it.
  Vendoring without wiring would have been a control that never fires.
- **Prod-only Admin keyring.** The vendored `data/admin_signing_pubkey.json` carried
  `admin-dev-2026a` beside prod `admin-2026a` since 2026-08-01. Verification resolves the
  artifact's own `key_id`, not `active`, so shipping it would make the **development** Admin a
  trusted licence authority on grower boxes. Pruned and re-vendored (Peter ruled 2026-08-03); no
  released version ever carried it. Dev boxes re-add it via `PS_ADMIN_PUBKEY_FILE` →
  `/share/paddisense/admin_signing_pubkey.dev.json`, gated in `run.sh` on that file existing, so
  the export is inert on a grower box.

### Tests
- `tests/test_log_redactor.py` — the fleet-standard contract: every secret/PII class is masked in
  both the message and the traceback, redaction is idempotent, and operational signal (versions,
  ports, key fingerprints, `password_hash`) survives.

## 2026.8.5 — WR-PS-603: licence activation self-heals the store_app grant IN-LINE (fresh-box fix)

### Fixed (grower-blocking)
- Growers on v2026.7.8 (pre the v2026.7.9 startup self-heal) could not activate Store — "licence
  signature verification failed", which was really `permission denied for table store_config` on the
  first `_save_licence` (store_app missing DML grants) AFTER the signed nonce was consumed, so Core's
  retry read as `invalid_signature`. Root cause is the WR-201 grant class (NOT signing/pubkey — the
  pinned `admin-2026a` key was present and every envelope verified 7/7).
- The startup self-heal (v2026.7.9) only fixes the NEXT restart. `activate_licence` now **self-heals
  the grant in-line and retries the save once** on failure, so a first-ever activation succeeds
  without a manual restart — the fresh-box case behind both the Store grower incident and the PROD
  Safety first-seed 500. Test: `test_save_selfheals_grant_then_retry_succeeds` (fail→grant→retry→200).

Growers on <v2026.7.9 need this released to unblock activation.

## 2026.8.4 — WR-PS-152 §9-A receiver hardening (box-binding + no-bare-TOFU flag)

### Security (additive — no behaviour change on a legit own-box path)
- **F-A1 box-binding** (`_verify_instruction_signature`): a validly-signed deactivate/revoke whose
  subject (`licence_id`/`target`) != this box's stored identity (`licence`/`grower_id`) is rejected 400,
  closing cross-box replay of a real Admin-signed revoke minted for another grower. Enforced only when
  signed + subject-bearing + enrolled.
- **F-A2 no-bare-TOFU flag** (`core/module_gate.py::_no_bare_tofu`, env `STORE_NO_BARE_TOFU`, default OFF):
  refuses a bare first-pin (`reject_hard`) once the fleet re-issues `bound_fp`; transitional TOFU kept OFF.
- Tests +3 (real-signed cross-grower→400, own→proceeds; flag on→reject_hard, off→TOFU-pins).

Fan-out of Farm's WR-PS-152 F-A1/F-A2 to the shared §9-A receiver.

## 2026.8.3 — ADR-020: canonical `core/ingress.py` upgraded (cached, fail-closed)

### Changed
- Re-vendored `core/ingress.py` (canonical) — `is_ingress` now uses the fleet-standard
  cached, fail-closed infra-peer resolution (ADR-020 Option A, Core's model) instead of a
  per-request DNS lookup. No behaviour change beyond the perf fix + loopback trust.



## 2026.8.2 — ADR-020 convergence (canonical `core/ingress.py`)

### Changed
- Vendored `core/ingress.py` (canonical `is_ingress` + resolved-proxy pin + `INGRESS_SESSION`/
  `INTERNAL_SESSION`) from `documentation/contracts/ingress.py`; `core/auth.py` now imports it
  instead of holding a local copy. Added the `**Version:**` field to `docs/AUDIT.md`. Store is the
  ADR-020 reference exemplar; green through `check-fleet-structure` + `check-vendored-sync`.
  No behaviour change — the ingress logic is byte-identical, now canonical-sourced.


## 2026.8.1 — Box-key internal-auth token + resolved-proxy ingress pin (fleet root-cause fix)

### Security
- Pinned `core/auth.py::is_ingress` to the **exact resolved IP** of an HA ingress
  proxy (`supervisor`/`homeassistant`/`hassio`) instead of trusting the broad
  `172.30.32.0/23` subnet — under it any sibling addon on the hassio bridge could
  forge `X-Ingress-Path` and obtain this addon's admin ingress session (Rule 167/172/187).
- New `core/internal_auth.py` (vendored fleet-wide from
  `documentation/contracts/internal_auth.py`): a symmetric bearer token derived from
  the shared box master key via HMAC. `core/auth.py::require_auth` grants a read-only (`viewer`) session to a valid-token caller, so Farm's `GET /api/hfm/products` proxy keeps working after Store's own ingress pin; per-route role gates still block any mutation. Replaces the subnet trust the
  sibling proxy relied on with cryptographic box-key possession.

## 2026.7.10 — Trust the DEV Admin signing key (dev-box enrolment)

### Changed
- Re-vendored `paddisense_store/data/admin_signing_pubkey.json` from canonical `documentation/contracts/admin_signing_pubkey.json` — adds `admin-dev-2026a` beside prod `admin-2026a` so this DEV box verifies DEV-Admin-signed licences (verification is per-key_id, so additive; prod key unchanged). Fleet keyring propagation (Core did the same, v2026.7.58). ⚠ ships the dev key to PROD at the next grower release — per-lane keyring decision owed to Peter+A before a prod cut.

## 2026.7.9 — fix: licence activation failing with a false "signature verification" error

Two grower boxes could not activate a new licence — the box reported a licence **signature
verification** failure, while already-enrolled boxes kept running. The signature was never the
problem: the addon's least-privilege database role (`store_app`) was missing its table grants, so
the licence **save** crashed with `permission denied for table store_config` *after* the signed
one-time token had already been consumed. The retry then looked like a replay and was rejected as a
bad signature.

- **Permanent fix:** Store now ensures its own database grants at startup instead of relying solely
  on Core to provision them out-of-band. Self-healing on every restart, idempotent, non-fatal.
- The licence save now returns a clear, retryable error if the database ever refuses it, instead of
  an unhandled crash that masqueraded as a signature failure.

No data or configuration change is required — the box heals itself on update/restart.

## 2026.7.8 — pricing figures held to 2 decimal places (Peter)

Every dollar figure in the purchase-price calculator (total spend, price per unit, and the
saved cost-per-stored-unit) now displays to exactly 2 decimals, matching how costs are stored.

## 2026.7.7 — fix: pricing calculator now opens on the Receive page

The "Calc from invoice" modal opened but was invisible on Receive — the shared modal's
show/chrome styles lived only on the Store/History pages, not globally. Promoted the modal
styles to `app.css` so the calculator renders on every page that uses it (Receive, History,
product form). No behaviour change beyond the fix.

## 2026.7.6 — purchase-price calculator + application-units list + retroactive price fixes (Peter)

### Added
- **Application Units are now a managed list** (Settings) — no longer hard-wired. Add/rename/reorder
  your own like the other lists.
- **Units carry a conversion** (measure + factor) so the app can convert between how a product is
  bought and how it's stored — `tonne` is now included.
- **Products have a "Bought by" (purchase) unit** — how invoices are priced (e.g. Urea bought by the
  tonne, stored in kg). Shown on the product form, defaults to the stored unit.
- **Purchase-price calculator** on Receive and on the History edit screen ("Calc from invoice"):
  enter the invoice total + product amount and it works out the cost per stored unit for you — every
  figure shown at once so a mistake is easy to spot. Converts between units (e.g. $/tonne → $/kg).

### Fixed / changed
- **Correcting a purchase price now re-values stock retroactively** — the weighted-average cost is
  rebuilt as if the corrected price had always applied (exact even after some stock was used or voided),
  replacing the previous approximate adjustment.
- Every product/receive price field now spells out **which unit** the price is per — no guessing.

## 2026.7.5 — owner-login rotation self-heal (WR-PS-192/074 structural fix, port of Weather bd8d124)

### Fixed
- **Incident 2026-07-27 (Weather was the victim; Store carries the same class):** a flipped
  `*_owner` login uses a STATIC stored options password; a DB-role seed re-mint changes the
  Postgres role underneath it and the addon strands on its next restart (DB init failed →
  licence gate fail-closed → licence screen).
- Structural fix in `core/db/_pool.py` (verbatim port of Weather v2026.7.9 / bd8d124): for
  `*_owner` logins the password is now DERIVED from the `/share` box key first (the fleet's
  derivation truth, Core v2026.7.44), with the stored options password as fallback; loud
  WARNING when the stored copy is stale. The admin/owner pool also gained the same
  auth-failure rebuild-and-retry self-heal the app pool has had since 2026-07-09.
  `db_user: postgres` (pre-flip) boxes are unaffected — stored password only, never derived.
- Regression tests: owner candidate ladder + admin-pool self-heal + end-to-end
  stale-stored-password recovery (throwaway role `store_selfheal_test_owner`); the old
  `test_admin_pool_never_selfheals` assertion INVERTED — it encoded the incident's faulty
  assumption.

## 2026.7.4 — WR-PS-108 fleet flip: access-sync enforce ON by default

### Changed
- **Unsigned or invalid grant pushes are now rejected with 403.**
  `STORE_ACCESS_SYNC_ENFORCE` defaults ON (`=0` kill-switch — code-default
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
  is warn-only until `STORE_ACCESS_SYNC_ENFORCE` (the coordinated fleet flip).
  `bound_fp` is persisted from the activated licence. Copied from the
  SugarSense v2026.7.12 reference; 7 behavioural tests (forged signature,
  cross-target replay, nonce replay, expiry, fp mismatch).


## 2026.7.2 — Key-read diagnostic on the DB-role key path (WR-PS-090 Ask 4)

### Added
- **`_read_master_key()` now logs the box-key source + fingerprint on every read** (WR-PS-090 Ask 4, PWM reference diagnostic): `source=<path> fp=<sha256[:12]> dev/ino/size/mtime`, in preference order (`/share` db_role.key → `/share` master.key → local `/data`). A silent fallback here means this addon's derived `store_app` password no longer matches the role Core minted — which fail-closes every request-path query — and a fake overlay `/share` is now visible via the logged `st_dev`. Completes the P-pool adoption of the diagnostic that cracked the 2026-07-06 fake-`/share` incident and the WR-PS-110 key churn. No behaviour change to the key preference order; an empty key file is now skipped rather than returned.

## 2026.7.1 — WR-PS-109: per-user module-access enforcement on ingress (Hone SEC-04/SEC-09, Option B)

### Added
- **`core/module_gate.py`** (vendored from the Farm reference): Core pushes its `module_access`
  grant table to `POST /api/access/sync`; Store caches it durably in
  `/data/module_access_grants.json` (atomic swap) and enforces per-user access locally on every
  **ingress** request. Decision semantics mirror Core's `effective_modules`: never-synced → open
  (bootstrap), synced-no-entries → open, granted/all-access/admin → allow, configured-but-ungranted
  → **403**. A direct cookie login with Store's own credentials keeps its existing role path.
- **`POST /api/access/sync`** receiver — trust = the same transport gate the licence-forward path
  uses (`_verify_internal`); the §9-A.9 signed-grant envelope is the tracked fleet follow-up
  WR-PS-108.
- **`tests/test_module_gate.py`** (11) — decision-table units + end-to-end through the REAL auth
  middleware: ungranted ingress user 403s on pages and API paths, granted user passes, never-synced
  box stays open, corrupt cache never locks the grower out.

## 2026.6.68 — Rotation self-heal for the app DB pool (incident 2026-07-09, Rule 106)

### Fixed
- **App DB pool self-heals across a box-key rotation.** When Core rotates the box key (`db_role.key`,
  WR-PS-088 / ADR-013), the app DB password changes; a long-running pool holds the old one, so the next
  fresh connection fails auth and the add-on breaks until a manual restart — which a grower can't do.
  `_acquire_conn` now treats a `password authentication failed` on the app pool as a stale key: drops
  the pool, rebuilds it (re-reading `/share/paddisense/db_role.key`), and retries once; a second
  failure propagates. Never applies to the admin/superuser pool (R173 intact). Fleet-wide fix
  originating from the live PWM incident. `tests/test_pool_selfheal.py`.

## 2026.6.67 — Hone PS-SEC-19: mask secret config fields + Rule 17 theme re-sync

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

## 2026.6.66 — Prefer the dedicated /share db_role.key for the DB app password

### Grower-facing
- No change to how Store looks or works. This release prepares Store for a future central-management
  security upgrade with zero behaviour change today.

### Security
- Prefer the dedicated /share db_role.key for the *_app DB password; falls back to master.key during
  the WR-PS-088 split rollout — no behaviour change today. Core now publishes both
  `/share/paddisense/db_role.key` (canonical) and `/share/paddisense/master.key` (legacy), equal today;
  the pool reads `db_role.key` first so it keeps authenticating after the future 1b flip when the two
  keys diverge and master.key is retired. Additive and safe: the master.key read, the local /data
  fallback, and the fail-closed no-superuser-fallback logic are all unchanged.

## 2026.6.65 — R142 replay protection now proven by regression test

### Grower-facing
- No change to how Store looks or works. This release adds an automated test that proves a
  security protection already built into Store: a licence sent from central management can only
  be used once, and an out-of-date (expired) licence is refused. If that protection ever broke,
  the test would now fail and block the release.

### Security / testing
- **R142 (anti-replay) reclassified N/A → COVERED with a real regression test (test-only).** The
  adversarial review found Store's signed-licence receive-side (`api/licence.py` →
  `core/licence_verify.verify_artifact`) already enforces single-use nonces and timestamp
  freshness, but had no behavioural test — it was wrongly marked N/A. New
  `tests/test_r142_licence_replay.py` forges a real Ed25519-signed artifact with a throwaway test
  key and asserts: a fresh, first-seen artifact is accepted; a byte-identical replay
  (same `licence_id`+`nonce`) is rejected; an expired timestamp is rejected; a future-dated
  timestamp is rejected. Collects under `pytest -k "replay or nonce or timestamp"`.
- **`docs/AUDIT.md` R142 row updated** to COVERED with the test names as evidence; the stale
  `test_replay_na_licence_uses_ip_not_signatures` N/A stub (whose premise "no client-signed
  inbound surface" was false) was removed.
- No production code path was changed — verification, signing enforcement, and pools are untouched.

## 2026.6.64 — security test suite made real & enforceable (green + red-team coverage)

### Grower-facing
- No change to how Store looks or works. This release strengthens the automated safety net
  behind the scenes so security checks run green and can block a release if a protection ever
  regresses.

### Security / testing
- **Test database now provisions like production (test-only).** The behavioural test suite was
  unable to run because the least-privilege `store_app` database role — the exact role Store uses
  in production for day-to-day queries — had no permissions granted on the disposable test
  database. The test bootstrap (`tests/conftest.py`) now drops+recreates a pristine
  `paddisense_store_test` database each run, applies the schema/migrations as the admin owner, then
  grants `store_app` the same least-privilege permissions it holds in production. No production
  database, pool, or authentication path was changed. A hard guard refuses to run against any
  database whose name does not end in `_test`, so the live database can never be touched.
- **Ingress-trust and CSRF tests fixed to match the 2026-07-04 header-spoof fix.** Test clients now
  present a Supervisor-subnet peer address alongside the ingress header, exercising the real trust
  boundary (header + trusted network position) rather than the old header-only shortcut.
- **Every required red-team security test now collects and runs green.** All twelve rows of the
  fleet Required-Security-Test manifest (CSRF 403, IDOR/object-scoping, oversized-body + login
  rate-limit bounds, SSRF/no user-URL fetch, forged-internal-request refusal, forged
  X-Forwarded-For ignored, login-enumeration byte-identical responses, plus honest N/A markers for
  replay, CSV-injection, cross-tenant, credential-reset and email-throttle surfaces Store does not
  have) are present, named to the manifest selectors, and pass. This makes Store's row in the
  security-test enforcement manifest ready to block a release on regression.

## 2026.6.63 — hardening: no error internals in API responses + v2.49 rules re-audit

### Grower-facing
- When a stock or product action can't be completed, the app now shows a short, plain message
  instead of raw technical text. Nothing about how the system works internally is shown on screen.
- No change to how Store looks or works day to day.

### Security / hardening
- **Rule 166 — no exception internals to clients.** `POST /api/products` (create) no longer
  returns `str(exc)` in its 500 body; it returns a fixed `"Failed to create product"` message and
  logs the full exception server-side via `log.exception`. The two `InsufficientStock` 409 paths in
  `api/movements.py` (movement + transfer) now return the exception's explicit, authored
  `user_message` attribute rather than `str(e)` — the message is text we author (never a wrapped
  DB/internal error), so the behaviour (the same on-hand/withdrawal wording) is unchanged while the
  `str(e)` leak-pattern is removed. `InsufficientStock` gained a typed `user_message` contract.
- **Golden Rules v2.48 → v2.49 re-audit.** Walked every applicable rule against source under
  Wave-4a (R34/35/36→R19, R42→R60+R98, R56→R65, R73→R74, R99→R98, R124→R133, R145/148→R160,
  R147→R166). Store owns no relocated Category-A product rule. `docs/AUDIT.md` refreshed
  (last_audit_date 2026-07-04, one row per rule).

## 2026.6.62 — 🔴 SEC: fix X-Ingress-Path header-spoof auth bypass (fleet-critical)

### Security
- **`core/auth.py::is_ingress` now requires the client IP on the Supervisor network
  (`172.30.32.0/23`) before trusting `X-Ingress-Path`.** It previously trusted the header
  unconditionally — so ANY client that could reach the addon port and set `X-Ingress-Path` was
  handed the `role: admin` ingress session (remote admin auth bypass). Restores the canonical
  `documentation/shared/auth.py` source-IP gate that 6 of 10 addons already carried. Found by the
  2026-07-04 fleet-consistency sweep; a `check-fleet-consistency.py` assertion will gate it (WR-PS-084).

## 2026.6.61 — add fleet-standard BodySizeLimitMiddleware (10 MB DoS guard)

### Security
- **Added the global `BodySizeLimitMiddleware`** (10 MB cap, matches Core + the other 7 addons):
  rejects requests whose `Content-Length` exceeds the limit with **413**, and requires a declared
  length on chunked body-bearing methods (**411**). Closes a fleet-consistency gap — this addon was
  one of three lacking the global body-size guard (only endpoint-level caps existed). Fleet-alignment
  pass (Peter-directed 2026-07-04).

## 2026.6.60 — SEC-08/R173: fail-closed DB app pool (Phase-2, WR-PS-081)

### Security
- **The request-path DB pool is now fail-closed (R173/SEC-08).** `_pool.py` no longer falls back to
  the `postgres` superuser if the `store_app` app pool can't initialise — `get_cursor()` returns the
  least-priv app pool or raises. Migrations/DDL still use the admin pool during the startup window
  (before `init_app_pool()` is called). Converges the fleet to Farm's fail-closed posture; a future
  key/role failure now fails loudly instead of silently promoting request-path queries to superuser.
  (`/share` persists, so an established box that reboots keeps its key and does not fail-closed.)

## 2026.6.59 — SEC-08/R173: admin/app DB pool split (fleet-standard, WR-PS-081)

### Security
- **`core/db/_pool.py` now maintains two pools** — an **admin** pool (`postgres` superuser) for
  migrations/DDL and an **app** pool (`store_app`, least-privilege DML) for request-path queries.
  `get_cursor()` transparently uses admin while the app pool is not yet ready (startup/migrations),
  then `main.py` calls `init_app_pool()` after `ensure_database()` so all request-path queries run as
  `store_app`. This is the Livestock/Farm canonical pattern; v.58 (single pool on `store_app`) would
  have failed **fresh-box** schema provisioning (`permission denied for schema public`) — DDL now
  routes through admin, DML through the app role. Shutdown closes both pools.

## 2026.6.58 — SEC-08/R173: read the shared box key so store_app actually authenticates (WR-PS-081)

### Security
- **`core/db/_pool.py` now reads the box DB-role key from the shared `/share/paddisense/master.key`**
  Core publishes (WR-PS-081), falling back to the local `/data` key during rollout. Root cause: the
  per-container `/data` key differed from Core's, so `store_app`'s derived password never matched the
  role Core minted → the pool **silently fell back to the `postgres` superuser** (confirmed at runtime:
  boot log `role=postgres`). Now `store_app` authenticates → the R173 least-priv DML-only request path
  is genuinely in effect. Fernet-at-rest is untouched (separate local `/data` key). The superuser
  fallback remains as a rollout safety net; Phase 2 fail-closes it.

## 2026.6.57 — R143: constant-time token compare in _verify_internal (fleet sweep)

### Security
- **`api/licence.py::_verify_internal` now compares the Supervisor Bearer token with
  `hmac.compare_digest`, not `==`** (Rule 143 — `==` on a secret leaks length/content via timing).
  Fleet-wide R143 sweep (Store/Weather/SugarSense shared the same `==`). Defence-in-depth only — the
  Admin Ed25519 signature is the real authorisation (SEC-04).

## 2026.6.56 — Negative-stock guard (THREAT_MODEL G3)

### Fixed
- **An outward movement can no longer drive `store_stock.quantity` negative.** `_update_store_stock`
  now reads on-hand and raises `InsufficientStock` (→ **409**, clear "Insufficient stock: X on hand,
  cannot remove Y") when a withdrawal exceeds available stock — covering all three paths
  (`/api/movements` out, `/api/movements/transfer`, `/api/movements/batch`), atomically within the
  movement transaction. A negative cache previously desynced the ledger and made WAC divide by a
  negative quantity (only `total_value` was floored, not `quantity`). Surfaced as **G3** in
  `docs/security/THREAT_MODEL.md`. Tests: `tests/test_movements.py` (3 — over-withdraw rejected,
  within-stock allowed, transfer-over-source rejected).

## 2026.6.55 — SEC-01/04: Admin signed-licence receive-side (Hone PS-SEC-04 fleet adoption)

### Security
- **Both mutating licence paths now verify the Admin Ed25519 signature** (`api/licence.py`). Store
  trusted the `/23`/loopback transport (`_verify_internal`) alone on `/api/licence/activate` and
  `/deactivate` — the "network-location = trust" pattern Hone **PS-SEC-04** flags and
  `SIGNED_LICENCE_CONTRACT §9-A` retires. Vendored `core/licence_verify.py` (byte-identical to
  `documentation/shared/`) + Admin pinned pubkey at `data/admin_signing_pubkey.json` (baked by the
  existing `COPY paddisense_store/`). `activate` verifies via `_extract_licence` (handles the paste
  `code` AND Core's heartbeat `signed_licence`); `deactivate` verifies the signed instruction
  (`action ∈ {deactivate,revoke}`). Legacy-tolerant behind `STORE_SIGNED_LICENCE_ENFORCE` (default
  off). Signature — not network position — is the trust boundary. `cryptography==48.0.1` pinned.
  Tests: `tests/test_licence_signed.py` (12 pass). Closes Store slice of **WR-HONE-SEC-04**.

## 2026.6.54

**Compliance + security bundle for grower release.** Closes 4 gate ✗ + 48 CVEs + 2 fleet WRs in one arc.

### Fixed (P0 security)

- **ADR-011 §6 test-isolation P0** — `tests/conftest.py` was setting `STORE_DB_NAME=paddisense_store` (LIVE), meaning every pytest run mutated production data on the dev box. Fix per FLEET_PROCESS.md §6 canonical: force `os.environ["STORE_DB_NAME"] = os.environ.get("STORE_TEST_DB_NAME", "paddisense_store_test")` at module import time (not `setdefault`, so a parent-shell env var override doesn't defeat it). This is the exact P0 hole ADR-011 §6 was created to catch fleet-wide.
- **ADR-011 §5 startup gate** — extracted required-env-var validation from the startup handler into a public `validate_config()` function per FLEET_PROCESS.md §5 canonical. Startup handler now calls `validate_config()` FIRST, before any background service kickoff (§4.4 D gate). Behaviour unchanged; structure aligned to fleet-wide gate.

### Changed

- **R155 CVE lift** — `requirements.lock` regenerated via `pip-compile --allow-unsafe --generate-hashes`. Closes **48 known CVEs across 9 packages**: aiohttp (32), urllib3 (5), starlette (5), setuptools (1), brotli (1), cryptography (1), idna (1), msgpack (1), requests (1). Root cause identical to Weather's v.71 lift — 8 of 9 vulnerable packages were legacy transitives from a pre-httpx-only `requirements.txt`; pip-compile dropped them entirely on regen. Post-regen `pip-audit`: **No known vulnerabilities found**.
- **R69 hash-pinning** — same regen also generated `--hash=` lines for every package (735 hash lines from 0). Closes the "R69 deferred" item that was carried across three prior sessions.
- **WR-PS-080 (Hone SCAL-03) — Python 3.11 → 3.12.** `Dockerfile: FROM python:3.11-slim → python:3.12-slim@sha256:423ed6ab25b1921a477529254bfeeabf5855151dc2c3141699a1bfc852199fbf` (multi-arch index digest — amd64 + aarch64, verified against Admin's + Weather's reference bump). `pyproject.toml [tool.mypy] python_version: "3.11" → "3.12"`. Digest pin satisfies R155 / R197 provenance requirement.
- **WR-PS-076 (Rule 195 CSS prefix rehome) — `ss-` → `st-`.** Store's local CSS prefix was squatting on Seed Manager's reserved `ss-` namespace. Rule 195 registry (v2.47 Rule 113 amendment / A-Claude steward WR-PS-064 close) added `st-` for Store. Mechanical `\bss-` → `st-` rename across `static/app.css` + 12 templates (28 class definitions + 72 references). Zero residual `ss-` refs post-rename.
- **`run.sh` Gate 1 uses `compileall` (fast ARM startup).** Single-process `python -m compileall` on the tree replaces the per-file `py_compile` loop — matches ASM-Pro / Farm / Weather. Faster boot on ARM grower boxes. (Ported from Store's `origin/develop` branch — 4 legacy P-Claude commits absorbed and `develop` deleted as part of the ADR-012 trunk-based flip landing in this ship.)

### Notes

- Golden Rules v2.44 → v2.47 rebaseline: delta covers Rule 113 ownership fan-out (Store defaults to G-Claude per Peter alignment 2026-07-02), ADR-012 trunk-based (already applied at v.49), R3 substrate correction (no code impact), and the R195 registry expansion that unblocked WR-PS-076.
- Fleet ownership updated: Store flipped P → G per Peter alignment `98ab4f0` in `PaddiSense/documentation`.
- Grower boxes currently on v.49 have all 48 CVEs already; v.54 lifts them all in one shot. Same delivery model as Weather v.72.

## 2026.6.53
Grower base-seed refresh: 10 base products + 178 base config items, with enriched chemical data.
### Added/Fixed
- **Base product set captured** — snapshot of the products you flagged as Base (active constituents,
  concentrations, chemical group) → `seed/base_seed.json`, seeded onto fresh grower boxes.
- **Snapshot + seeder now round-trip `chemical_group`** (and apvma_number, container_size/unit,
  min_stock, notes) — previously the snapshot SELECT + `_seed_products` INSERT dropped them, so the
  enriched group/data never reached growers. Fixed both.

## 2026.6.52
Security: the public licence-status endpoint no longer leaks the licence string or telemetry.
### Security
- **`GET /api/licence` is now liveness-only** (Rule 144, WR-PS-066) — this endpoint has no auth
  (Core polls it), but it was returning the full `licence`, `product`, `exp` and `grower_id` fields,
  so anyone on the network could read the licence. It now returns only `{"enrolled": <bool>}`,
  matching the Farm/ASM fleet pattern. Auth-gated activate/deactivate are unchanged.
  Guard: `test_licence_status_no_secret_leak`.

## 2026.6.51
Fix: new products were invisible on the Store page until stock was received (they showed on Receive but not Store).
### Fixed
- **Zero-stock products hidden on the store page** — `/api/stock` required `quantity > 0`, so a
  brand-new product (no stock yet) had no card even though it existed. Changed the query to LEFT JOIN
  from `store_products`, so every active product shows with its stock level (including 0) and new
  products are visible immediately (receive against them). Guard: `test_zero_stock_product_appears`.

## 2026.6.50
Fix: on a fresh/grower box the product form's Sector dropdown was empty, so new products saved with no category and the store page filtered them out.
### Fixed
- **`product_sectors` not seeded on fresh boxes** — the Cropping/Livestock → category map lives in
  `store_config` and was only ever present on the dev box (created during development), never seeded.
  A grower box had an empty map → empty Sector dropdown → new products got a blank category → the
  store page's category filter dropped them ("don't render"). Added `_seed_product_sectors` migration
  (seeds the default when the row is absent OR empty; never overwrites a populated/customised map).
  Guard: `TestDataIntegrity.test_product_sectors_seeded`.

## 2026.6.49
Base-seed authoring (the Base ticks) is now hidden on grower boxes — it's a dev/curation-only tool.
### Added
- `seed_author_mode` addon option (bool). **Default: true in the dev/source config** (master box
  authors automatically), **false in the grower/public config**. When off: the Base ticks (config
  list + product form) and the `set-base` endpoint + product `is_base` writes are hidden/blocked.
  The seeder still runs on grower boxes (they *consume* the seed) — only authoring is gated.
  Toggle per box via the add-on config UI. Tests: `TestSeedAuthorGate`.

## 2026.6.48
Fix: on mobile Use, the + buttons were subtracting stock like the - buttons.
### Fixed
- Mobile Use (S03) **+** quantity buttons carried a positive `data-delta`, so `adjustDelta`
  added to the use amount exactly like the **-** buttons (both subtracted from stock). They now
  carry negative deltas (matching desktop) so **+** reduces the use / raises projected stock.
  Regression guard: `TestUsePageButtonDirection` asserts the +/- sign on both templates (KDP-001 variant).

## 2026.6.47
Security hardening — login timing-equalisation + full security-test manifest. No grower-visible change.
### Changed
- Login no longer leaks whether a username exists via response timing: the "no such user" branch now
  runs the same PBKDF2 hash as a real check (constant-time — Rule 190/143). The error message was
  already uniform.
### Added
- Security-test manifest coverage (Rule 163): `TestSecurityManifest` covers all 12 required rows —
  behavioural where Store has the surface (login uniformity + rate-limit, unknown-id 404, forged-internal
  reject, XFF-ignored), structural "safe-by-construction" where it doesn't (no export/email/self-reset/
  client-signing/cross-tenant surface). 58 tests pass.
### Deferred (honest)
- R69 hash-pinned requirements (`--require-hashes`): must be generated in the image's **Python 3.11** and
  dev-tested first; not done in the 3.12 toolbox to avoid transitive-version drift that could break the
  grower build (Rule 19 — minimal risk). Tracked follow-up; the `==` form of R69 is satisfied.

## 2026.6.46
Reverted the full-screen search overlay; restored the v2026.6.44 pin-to-top search on mobile Use.
### Changed
- Removed the full-screen search overlay (v2026.6.45). Mobile Use product search is back to the
  pin-to-top behaviour (search bar pins toward the top on focus so the iOS keyboard covers less
  of the list). Sector-tiles grid + Empty Container retained.

## 2026.6.45
Mobile Use: product search is now a full-screen overlay (iOS keyboard never covers the list).
### Changed
- Tapping the product search on mobile Use (S03) opens a full-screen search panel — search box
  pinned at the very top, results list filling the screen down to the keyboard. Tap a result to
  pick it (drops back into the form); ✕ to cancel. Replaces the unreliable position:fixed pin
  (iOS positions fixed elements against the layout viewport, so it never landed at the true top).
  Reuses the sector/category-aware product filter.

## 2026.6.44
Mobile Use: tapping the product search pins it to the top so the iOS keyboard doesn't hide the list.
### Changed
- On mobile Use (S03), focusing the product search bar pins it to the top of the screen
  (`position: fixed`) and expands its results dropdown (up to 60vh), so the iOS keyboard
  (bottom) no longer covers the list. Restores to normal position on select / tap-away.

## 2026.6.43
Mobile Use (S03): the 3 sector filter tiles now sit 3-per-row (were wrapping to 2 lines).
### Changed
- Sector filter pills on mobile Use are an equal-width 3-column grid matching the qty (+/-)
  buttons (rounded-rect, 56px), instead of a wrapping pill row.

## 2026.6.42
Product form: pick a Sector, and the Category list filters to it (Cropping → Herbicide…).
### Added
- **Sector → Category cascade on the product create/edit form** (S01, desktop + mobile): a new
  **Sector** dropdown (Cropping / Livestock, from the `product_sectors` config) drives the **Category**
  dropdown so it shows only that sector's categories. On edit the sector auto-fills from the product's
  category. Sources entirely from config; no schema change (product still stores its `category`).
### Fixed
- Mobile product modal previously had **hardcoded** category options (chemical/fertilizer/adjuvant/seed)
  and loaded no config — so real categories (Herbicide, Fungicide…) couldn't be selected. Now
  config-driven like desktop, with the sector cascade.

## 2026.6.41
"Empty container" — write off the dregs of a physically-empty drum.
### Added
- **Empty Container** on the Use page (S03, desktop + mobile): when a product + location with
  stock is selected, an **EMPTY CONTAINER** button writes off the remaining quantity as an
  `adjust` movement (note "Container emptied" — a reconciliation, not a dispense, so Use figures
  stay honest per Rule 33) and zeros quantity + `total_value`. Backend `POST /api/stock/{id}/empty`
  (reuses `_update_store_stock` + `_insert_movement_record`). Restores the legacy IPM
  "EMPTY LOCATION" feature. Tests: `TestEmptyContainer` (3).

## 2026.6.40
Grower base-seed: tick items "Base" and they're baked into each release + copied to new boxes.
### Added
- **Base tick on products** (S01 create/edit modal, desktop + mobile) — `is_base` + `base_key`
  on `store_products`, handled by `/api/hfm/products` POST/PUT/GET. Tick e.g. Urea as Base and it
  ships to growers exactly like a base config item.
- **Idempotent startup seeder** (`core/db/_migrate._apply_base_seed`) — reads the shipped
  `seed/base_seed.json` and inserts each base item **once per `base_key`** via the `store_seed_log`
  tombstone: a fresh box seeds everything, reboots are no-ops, grower deletions stay deleted, and
  grower edits are never overwritten (`ON CONFLICT` / existence check).
- **Release snapshot generator** (`python -m paddisense_store.seed.snapshot <version>`) — writes
  every `is_base=TRUE` row to `seed/base_seed.json`. Run at release so the ticked set is baked into
  the image. `base_key` uses the raw value (unique by construction — near-duplicate values can't collide).
### Notes
- Initial seed set: 178 base config items (all active constituents + all chemical groups + ticked
  categories). Products: tick as needed. Run the snapshot before each grower release (CI step once GHCR builds are wired).

## 2026.6.39
Settings (S05) rebuilt on the canonical SM config component + foundations for grower base-seed data.
### Added
- **Config lists promoted to a typed table** (`store_config_items` — Rule 13 FAIR) with per-row
  `sort_order`, **`active`**, and base-seed provenance (`is_base`, `base_key`). Migrations M004–M008
  (idempotent; backfill is one-shot-per-list so grower deletions are never resurrected). New
  `store_seed_log` (base-seed tombstone) and `is_base`/`base_key` on `store_products` + `store_locations`.
- **Settings page rebuilt to the canonical master config component** (`ps-config-section` collapsible +
  `ps-list-table` + `ps-cfg-*`, TEMPLATE_GUIDE §6) — **the same as Seed Manager**. Per row: inline rename
  (autosave + ✓ tick), reorder ▲▼, **active On/Off toggle**, **Base tick**, delete-with-confirm; `<details>`
  open-state persisted to `localStorage`. Shared macro `_config_section.html` + `static/store-config.js`
  across desktop + mobile. Server-rendered (Rule 15); actions via the existing CSRF fetch wrapper.
- **Config item API** (table-backed, id-based): `POST /api/config/{key}/items`, `PUT /api/config/items/{id}`,
  `POST …/move|active|base`, `DELETE …/{id}`. `GET /api/config` keeps the legacy flat shape (product dropdowns).
### Removed
- Local reinvented `cfg-*` config-editor classes from `app.css` and the `store-settings.js` builder
  (Rule 169/193 — config management is now the canonical master component).

## 2026.6.38
Master-theme alignment of the shell chrome, a negative-inventory-value bug fixed at
the source, mobile S01 tile fix, and dead-template removal. No grower release (dev/compliance).
### Fixed
- **Negative inventory Value (`-$23,917`) — root cause (KDP-014).** A movement recorded at
  `cost_per_unit = -1.00` wrote `total_value = qty × cost = -27,000` into `store_stock`, so
  `SUM(total_value)` went negative. New central `_validate_cost()` rejects negative / non-numeric
  cost (400) on **all four** paths — create, transfer, batch, and the PATCH cost-edit — before any
  DB write; `_recalc_wac_on_cost_change` now floors `total_value` at 0 (`GREATEST`). Tests:
  `TestMovementCostValidation` (5). *(The poisoned Urea dev row is corrected separately — needs DB consent.)*
- **Currency formatting:** negative values render `-$X` (was `$-X`) on the S01 Value chip
  (mobile + desktop) and the dashboard/hub stat line. New `fmtMoney()` helper.
- **Mobile S01 stat tiles** no longer overflow: `.stats-bar` is now a 2-column grid (was a
  4-up flex row that crushed "12 Locations" / "$…"); value text ellipsizes if still too long.
### Changed
- **Shell chrome migrated to the canonical master `ps-*` classes (Rule 17/177/193).** Both base
  templates (desktop sidebar/topbar/content, mobile topbar/content), the dashboard (S00) and mobile
  hub (H01.M) page-headers + hub-stats now use `ps-app-shell`/`ps-sidebar*`/`ps-topbar*`/
  `ps-main-content`/`ps-mobile-*`/`ps-page-header` (+ `<h1>`)/`ps-hub-stats`/`ps-toast` — replacing
  Store's reinvented, drifted `ss-*` chrome (fixes "doesn't match other addons / top spacing /
  overlapping dashboard numbers"). Dead chrome definitions pruned from `app.css`. App-specific
  classes (tiles, delta-val, page-id badge, utilities) and the `ps-msg` banner are flagged for
  prefix-registration in **WR-PS-064** (Rule 195 — Store squats on Seed Manager's `ss-`).
### Removed
- Orphaned `pages/{desktop,mobile}/movements.html` (no route rendered them — `/movements` only
  302-redirects to `/receive`; that redirect is kept for bookmarks).

## 2026.6.37
Operator field is now an HA-user pick-list, and a pile of dead code is gone.
### Added
- **Operator dropdown** on Use (S03) + Receive (S02), mobile + desktop: a `<select>` of
  HA `person.*` entities that auto-selects the logged-in HA user, matched on the stable
  `X-Remote-User-Id` ingress header (locked-in on a personal device, defaulted on a shared
  browser; still overridable). Degrades to a usable empty select if HA is unreachable.
- `GET /api/v1/ha-users` (+ `/api/ha-users` alias) → `{users:[{name,user_id}], current}`,
  backed by `core/ha_identity.py` (async, 60s cache, timeout + graceful fallback — Rules
  121/124/127/138). Store's first outbound HA Core API call. Shared loader
  `static/store-operators.js` (Rule 59). Tests: `TestOperatorUsers` (4).
### Removed
- **Dead "quick move" modal** from the product cards (`store.html`, mobile + desktop):
  the per-product Move button was removed earlier, leaving the modal + `openMoveModal`/
  `saveMove`/`onMoveActionChange`/`saveMoveBtn` orphaned (zero callers). Excised entirely.
- Mobile Use (S03) Paddock/Job Reference field (HFM/Farm captures it — double-handling).
- Dead hidden sidebar from the mobile base (Rule 177) + the temp ingress-header probe.
### Fixed
- `loadLocations()` in `store.html` no longer references the deleted `#moveLocation`
  (`null.innerHTML` would have thrown on the product page).

## 2026.6.36
Mobile UI tuning (S03 Use) + a temporary dev diagnostic. No grower release.
### Changed
- Mobile base (`pages/mobile/base.html`): removed the dead, hidden sidebar nav
  (`ss-sidebar ss-sidebar-mobile-hidden`) + the unreachable `toggleSidebar()` and the
  now-orphaned `.ss-sidebar-mobile-hidden` rule in `app.css`. Rule 177 — mobile is a
  purpose-built layout (topbar → content), not the desktop layout hidden by CSS.
- Mobile Use (S03): removed the **Paddock / Job Reference** free-text field — application
  context is captured by HFM/Farm, so recording it here is double-handling. The movement
  `reference` is now sent as `null` from this page (column unchanged; desktop untouched).
### Dev
- TEMP probe in the `/use` route (`pages/__init__.py::_probe_whoami`) logs which HA ingress
  identity headers (`X-Remote-User-*`, `X-Ingress-Path`) actually arrive on mobile vs
  browser — to confirm a locked-in operator source before building the operator dropdown.
  **Removed in the next version.** Logs header keys + the user's own display name only;
  never Authorization/Cookie.

## 2026.6.35
Full compliance pass — clears every `verify-commit` warning so the addon is ready
for the ADR-010 warn→block gate flips. `verify-commit` now passes with ZERO warnings;
mypy/ruff/bandit/pip-audit clean; 33 tests pass.
### Security
- Rule 157 (CSRF): added double-submit CSRF protection. `CsrfMiddleware` (fail-closed)
  requires `application/json` + a matching `X-CSRF-Token`/`store_csrf` (constant-time)
  on cookie-session `/api/` mutations; internal Core licence calls exempt. Login issues
  the `store_csrf` cookie; logout clears it. Base templates patch `window.fetch` to echo
  the token. Behavioural 403 regression tests added (`TestCsrf`).
- Rule 156 (CSP): nonce-based Content-Security-Policy. Per-request nonce set in
  `SecurityHeadersMiddleware`; `script-src 'self' 'nonce-…'` with NO `unsafe-inline`;
  every inline `<script>` stamped with the nonce.
- Rule 167 (security): `api/licence.py::_verify_internal` Supervisor-network trust now
  uses the `ipaddress` module against `172.30.32.0/23` (+ loopback) instead of
  `startswith("172.30.")` (which trusted the whole /16). Regression tests added.
- Rule 80: `X-Frame-Options: SAMEORIGIN` now set.
- Rule 69/155: bumped `python-multipart` 0.0.27→0.0.32 (3 CVEs) and `pytest`
  8.4.1→9.0.3 (dev CVE); pip-audit clean.
### Fixed
- Rule 178: migrated all 200 inline `on*=` handlers (14 page templates + the shared
  `store-filters.js`/`store-settings.js`) to `addEventListener`/event-delegation, a
  prerequisite for nonce CSP. Each page now ships its own `<script nonce>` block
  (base no longer wraps `{% block script %}`). Orphan-bindings gate clean.
- Rule 88: `api/products.py` log used reserved LogRecord key `name` in `extra={}`
  → `product_name`.
- Rule 65: cleared 13 mypy errors (login `UploadFile|str` `str()` wrap, untyped defs,
  container annotations, duplicate-var rename in movements).
### Changed
- Rule 41: extracted remaining inline `style=` (receive page) to CSS classes.
- Rule 17: re-synced `static/paddisense-tokens.css` byte-identical to the master theme.
- Refreshed `docs/AUDIT.md` to Golden Rules v2.42 (was v2.1~115); CLAUDE.md
  `golden_rules_version` → v2.42.
### Contracts (shared — flagged to GR steward)
- Fixed three `verify-commit.sh` gate false-positives that would block the warn→block
  flip fleet-wide: Rule 91 (`__all__` export line), Rule 51 (`window.open` in a master
  CSS comment), Rule 124 (`.pyc` in `__pycache__` double-counted). See WR-PS-058.

## 2026.6.34
- run.sh now syncs the canonical master theme on boot (WR-PS-045/ADR-007)
- Re-synced paddisense-tokens.css byte-identical to master
- Added docs/SESSION_PICKUP.md (Rule 191)

## 2026.7.14
- Location-aware product search (shows stock at selected location)
- Red minus buttons on both Receive and Use pages

## 2026.7.12
- Desktop dashboard with tile launcher
- Two-tier filter: Sector (Cropping/Livestock) then Category

## 2026.7.10
- Split movements into Receive (stock in) and Use (stock out) pages
- Each page has dedicated fields and workflow

## 2026.7.1
- Initial release — extracted from PaddiSense Core chemical store
- Product registry, storage locations, stock movements
- 13 product categories (crop + livestock)
