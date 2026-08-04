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


## 2026.8.8 — WR-PS-210: accept an operator's own deactivate from this box's console

### Fixed
- Core's console "remove licence" button carries no Admin signature — it is not a remote revoke —
  so this addon refused it `unsigned_rejected` and the grower could not remove a licence from their
  own box. Now a caller presenting a valid **box-key internal-auth token** (WR-PS-204) is accepted
  as a local operator act: cryptographic proof of "Core, here", not `/23` position.
- **Admin's remote revoke is unchanged** and still requires the Ed25519 signature; only the local
  path is opened. Tests: `tests/test_local_operator_deactivate.py` (4) — no token is not local
  authorisation, a valid token is, the route actually consults the check, and signature
  verification is still on the route so the narrow path cannot become a general bypass.

## 2026.8.7 — Grower boxes trust ONLY the prod Admin signing key (per-lane keyring)

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

## 2026.8.6 — WR-PS-201 §9-A: a failed licence save hands back the reserved nonce

### Fixed
- `verify_artifact` RESERVES the signed artifact's one-time nonce the instant the signature checks
  out — *before* anything is persisted. When the save then failed (classically `sugar_app` missing its
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

## 2026.8.5 — WR-PS-152 F-D3: re-vendor the canonical log redactor (`enc:v2:` masking restored)

### Fixed
- The vendored log redactor had drifted to the **v1-only** `enc:` pattern, so an `enc:v2:` or bare
  `enc:` encrypted-secret token appearing in a log line or stored error string was **NOT masked**
  (Rules 88/164). Re-vendored byte-identical from canonical `documentation/shared/log_redactor.py`
  (`cmp -s` clean), restoring the optional-version-segment pattern from WR-PS-152 F-D3.
- The drift survived because `check-vendored-sync.py` could not resolve this addon's vendored path
  (the manifest carried no `dest_by_addon` row for this package name), so the ADR-020 gate skipped
  the file — and the addon's own test asserted `enc:v1:` only. Both closed: manifest row added, and
  `tests/test_log_redactor.py` gains `enc_token_v2` + `enc_token_bare` cases (Rule 106 regression —
  proven to FAIL against the drifted pattern before the fix).

## 2026.8.4 — WR-PS-603: licence activation self-heals the sugar_app grant IN-LINE (fresh-box fix)

### Fixed
- On a fresh box the least-priv `sugar_app` role can be missing its DML grants (Core's out-of-band
  provisioning never landed, or was lost on an owner-flip), so the licence save hits `permission
  denied` AFTER the signed one-time nonce is consumed — Core's retry then reads as a replay →
  `invalid_signature` → the misleading "signature verification failed" (Store grower incident
  2026-07-30; PROD Safety first-seed 500 2026-08-02).
- The startup grant self-heal only fixes the NEXT restart. The licence save path now **self-heals the
  grant IN-LINE and retries the save once** (never the verify — the nonce is already consumed) so a
  first-ever activation succeeds without a manual restart. Fan-out of the Store v2026.8.5 fix.
- Test: `test_licence_save_selfheals_grant_then_retries` (fail → grant → retry → saved).

## 2026.8.3 — WR-PS-152 §9-A receiver hardening (box-binding + no-bare-TOFU flag)

### Security (additive — no behaviour change on a legit own-box path)
- **F-A1 box-binding** (`_verify_instruction_signature`): a validly-signed deactivate/revoke whose
  subject (`licence_id`/`target`) != this box's stored identity (`licence`/`grower_id`) is rejected 400,
  closing cross-box replay of a real Admin-signed revoke minted for another grower. Enforced only when
  signed + subject-bearing + enrolled.
- **F-A2 no-bare-TOFU flag** (`core/module_gate.py::_no_bare_tofu`, env `SS_NO_BARE_TOFU`, default OFF):
  refuses a bare first-pin (`reject_hard`) once the fleet re-issues `bound_fp`; transitional TOFU kept OFF.
- Tests +3 (real-signed cross-grower→400, own→proceeds; flag on→reject_hard, off→TOFU-pins).

Fan-out of Farm's WR-PS-152 F-A1/F-A2 to the shared §9-A receiver.

## 2026.8.2 — ADR-020 convergence (canonical core/ingress.py + internal_auth)

### Changed
- Vendored `core/ingress.py` + `core/internal_auth.py` (canonical); `core/auth.py` imports the
  canonical `is_ingress` (cached, fail-closed) instead of a local copy, and gains the box
  internal-auth token path. Added `**Version:**` to `docs/AUDIT.md`. Green through both ADR-020
  gates. UI carries a tracked ADR-020 debt (lift to pages/{desktop,mobile} + api/, add mobile UI).
  No behaviour change to the ingress trust logic.



## 2026.8.1 — Pin ingress trust to the resolved proxy peer (Rule 167/172/187)

### Security
- Pinned `core/auth.py::is_ingress` to the **exact resolved IP** of an HA ingress
  proxy (`supervisor`/`homeassistant`/`hassio`) instead of trusting the broad
  `172.30.32.0/23` subnet. Under the subnet trust, any sibling addon on the hassio
  bridge could forge the `X-Ingress-Path` header and obtain this addon's admin
  ingress session. Matches the PWM/Farm reference fix; part of the fleet-wide sweep.
  This addon exposes no sibling-consumed proxy, so the change is a pure security
  tightening (no internal-token channel needed here).

## 2026.7.21 — Trust the DEV Admin signing key (dev-box enrolment)

### Changed
- Re-vendored `sugarsense/data/admin_signing_pubkey.json` from canonical `documentation/contracts/admin_signing_pubkey.json` — adds `admin-dev-2026a` beside prod `admin-2026a` so this DEV box verifies DEV-Admin-signed licences (verification is per-key_id, so additive; prod key unchanged). Fleet keyring propagation (Core did the same, v2026.7.58). ⚠ ships the dev key to PROD at the next grower release — per-lane keyring decision owed to Peter+A before a prod cut.

## 2026.7.20 — self-heals DB permissions + fixes empty supervisor token

### Fixed
- **Self-heals its own database permissions on startup (WR-PS-201).** Since the
  request path runs as a least-privilege `sugar_app` database role, it depends on a
  grant that Core provisions out-of-band. On a box where that grant never landed — or
  was lost when the database owner flipped — every page could fail with a
  `permission denied` error, and (worse) a licence activation would surface a
  misleading *"signature verification failed"* when the real cause was the missing
  grant. SugarSense now ensures its own `sugar_app` DML grants at startup
  (`core/db/_pool.py::grant_app_privileges` — `GRANT SELECT, INSERT, UPDATE, DELETE`
  on all tables + `USAGE, SELECT` on all sequences + `USAGE` on the schema, from the
  admin pool, idempotent and non-fatal), called from startup between
  `ensure_database()` and `init_app_pool()`. Self-heals on every restart.
- **Licence activation now returns a legible error instead of a crash.** The Admin
  signature's single-use nonce is consumed before the licence is written to the
  database, so a database write failure after that point left the box stuck. The save
  is now wrapped (`core/licence.py::activate_licence`): a database failure returns a
  clear **503 "verified but could not be stored — retry after restart"** rather than an
  unhandled 500 misread as a signature error.
- **HA notifications / features that need the Supervisor token now work (WR-PS-406).**
  `core/helpers.py::_read_supervisor_token()` read the s6 token file first, but that
  file is often empty in this addon image → the token came back blank and every Home
  Assistant call sent a bare `Bearer ` header that HA rejected (HA persistent
  notifications came up silent). It now prefers the `SUPERVISOR_TOKEN` environment
  variable HA always injects, falling back to the s6 file only if the env var is empty.

### Tests
- `test_supervisor_token.py` (3 — env wins, file fallback, None outside Supervisor)
- `test_pool_selfheal.py::test_grant_app_privileges_self_heals_after_revoke`
  (revoke → app role locked out → grant restores, idempotent)
- `test_licence_signed.py::TestActivateSaveFailure` (503-not-500 on a save failure)

Port of ASM v2026.7.36 / Store v2026.7.9 (WR-PS-201) + ASM v2026.7.32 (WR-PS-406).

## 2026.7.19 — fleet timezone fix (DB session pinned to local zone)

### Fixed
- **Dates now follow the box's LOCAL time, not UTC.** The shared TimescaleDB session ran
  in **UTC** while the farm/HA is Australia/Sydney (UTC+10/+11), so every SQL
  `CURRENT_DATE` / `date_trunc(...)` / `TIMESTAMPTZ::date` sliced the day on the UTC
  boundary (~10-11h early = mid-morning local). Any daily count keyed off the calendar day
  — e.g. an ASM-style prestart-compliance count (`WHERE timestamp::date = CURRENT_DATE`) —
  landed on the wrong Zulu date for that morning window.
- Fix in `core/db/_pool.py`: the Postgres **session timezone** is now pinned to the box's
  local zone via a libpq `options='-c timezone=<zone>'` fragment appended to BOTH DSN
  builders (`_admin_dsn_with` + `_get_app_dsn`), sourced by new `_session_tz()`
  (TZ env → `/etc/timezone` → `Australia/Sydney` fallback). `CURRENT_DATE` / `date_trunc`
  / `::date` now resolve on the LOCAL calendar; `NOW()` / `DEFAULT NOW()` render with the
  local offset.
- **TIMESTAMPTZ storage is unchanged** — each column still stores a UTC instant, so
  **existing records are unaffected** (no data migration); only the session's
  interpretation of "the date" becomes local.
- Tests: `test_session_timezone.py` (session tz is local not UTC; CURRENT_DATE == local
  date). Reference pattern is the ASM fleet timezone fix.

### Changed
- Theme tokens re-copied byte-identical from the canonical master (Rule 17 gate flagged
  drift — the fleet `ps-config-tiles` promotion had not been re-synced here; no
  SugarSense-side edits, straight `cp` of the steward's master).

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
