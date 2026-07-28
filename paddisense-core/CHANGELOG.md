# Changelog

## 2026.7.47 — self-diagnosing refusals + realistic-semantics happy-path test (A-Claude rulings)

### Improved
- Rollout refusals now CARRY the observed values — `catalog_head_mismatch (head=… target=…)`,
  `installed_version_mismatch (installed=… from=…)` — in the log line and the heartbeat attest.
  A bare reason cost three rounds of guessing on the first PROD canary; two numbers settle it.
- New named regression: installed BEHIND catalog with head == target MUST reach install — the
  matrix proved every refusal but never the install with realistic Supervisor field values,
  which is how a rail that could never install passed its tests. 23 directive tests green.

## 2026.7.46 — canary head check reads `version_latest` (A-Claude's find, first PROD canary)

### Fixed
- The catalog-head binding read the store entry's `version` field — which on a box where
  installed ≠ catalog tracks the INSTALLED build, so the check refused `catalog_head_mismatch`
  forever even with a current catalog and the v.45 poll. Now reads `version_latest` (the
  catalog head on every Supervisor variant), falling back to `version`. Test stubs updated to
  model the real field semantics so this class is regression-locked.

## 2026.7.45 — WR-PS-116 amendment: catalog-head poll + refusal/deferral heartbeat attestation

### Fixed (first live canary findings, 2026-07-27)
- **Catalog-head reload race:** `/store/reload` is async on the Supervisor (and rapid repeats
  are throttled), so `_bindings_reason`'s immediate read served the pre-reload cache — the
  first real canary (Weather → RRAPL) refused `catalog_head_mismatch` on every heartbeat
  against a current catalog. The head check now polls (5 tries / ~16 s) before ruling; a
  genuinely stale catalog still refuses.
- **Fleet-visible outcomes (A-Claude's idea, Peter-approved):** refusals and quiet-window
  deferrals now stamp the `addon_update_attest` heartbeat block (`refused:<reason>` /
  `deferred:<busy>`, last-state-wins, `since` preserved while the outcome is unchanged) so
  Admin's fleet view shows WHY a rollout isn't landing — no per-box log digging. Reasons are
  closed enums; no secrets ride out. Admin panel half is A-Claude's (WR-PS-116 amendment).
- 22 directive tests green (7 assertions updated to the new attested-outcome behaviour + 4 new).

### Fixed (third find of the night — async health path had NO self-heal)
- `async_cursor` (the `/health` DB probe) called `pool.getconn()` directly, bypassing
  `_acquire_conn`'s auth-failure rebuild-retry — after a key event the request path healed
  but `/health` reported degraded FOREVER (Admin's fleet view trusts /health; on a grower
  box this is a false "addon down"). Async acquire now routes through the same self-heal;
  health warnings now name the exception. Found via the suite's durable `db_ok` failure;
  406/406 green after the fix.

### Fixed (SECOND live WR-PS-192 incident, same night)
- **Test-suite cluster repave:** `create_addon_roles` skipped the WR-192 divergence guard for
  `*_test` DBs on an "isolated test cluster" assumption that is FALSE on a dev box — the test
  DB shares the production Postgres and roles are cluster-wide, so a suite run from a shell
  with a drifted `/data` key repaved all 22 fleet role passwords from the stale key (Core
  down until a manual repave; this was also the mechanism behind the evening incident).
  Test-context provisioning now derives from the PUBLISHED `/share` key whenever one exists
  (repave becomes convergent — a no-op on a healthy cluster); the local key remains only for
  genuinely `/share`-less environments (CI's disposable cluster). 2 regression tests.

## 2026.7.44 — WR-PS-192 root cause (create-only provisioning) + startup /share app-pool self-heal

> Supersedes v2026.7.43 (never ran healthy on dev — the create-only change exposed the
> gap below before the same-version rebuild could pick up the fix; relabelled to v.44 so
> the version matches the shipped code).

### Fixed
- **Boot provisioning no longer ALTERs existing role passwords** (`_ensure_role` is
  create-only at boot). The every-boot repave silently fought the explicit credential
  rails: on 2026-07-27, Core's local `db_role.key` seed vanished, boot fell back to the
  master key and repaved all 22 role passwords — while every WR-074-flipped addon still
  held old-key credentials. Any addon that restarted crashed on DB auth (PWM did).
  Password changes now belong ONLY to the signed `rotate_secret` rail
  (`create_addon_roles(..., repave=True)`) and cred-flip. The isolated `*_test` cluster
  still repaves (same carve-out + predicate as the WR-192 divergence guard).
- **`publish_box_db_key_to_share` refuses to pave over a conflicting `/share` key.** The
  unconditional every-boot publish ran BEFORE the WR-192 divergence guard, so a drifted
  local key overwrote `/share` first and the guard always compared equal — neutered by
  its own boot ordering. A differing `/share` key now stays put: CRITICAL log + HA
  persistent notification. `force=True` reserved for the signed rotation rail.
- **Startup app-pool `/share` self-heal.** With provisioning create-only, Core no longer
  force-matches the roles to its own key each boot, so a Core whose local key diverged
  from the seed the roles were minted with must converge on the `/share` seed at startup —
  exactly like its sibling addons — instead of crashing. The WR-PS-175 second-tier
  fallback existed only on the request path (`_acquire_conn_from_share`); `init_app_pool`
  now has it too (never the superuser pool; both-seeds mismatch still fails closed, R173).
  `verify_owner_roles` also tries the `/share` seed so boot readiness isn't a misleading
  0/11.
- 8 regression tests (`tests/test_role_provisioning_create_only.py`).

### Operational note (dev box, 2026-07-27 evening)
- Incident recovery: all 10 flipped addons re-converged on the current derivation via the
  cred-flip semantics (Peter-run, one at a time, health-verified 11/11 `db_ok`). The
  distinct rotation seed is GONE — the fleet now derives from the master key (Phase-1a
  fallback). Re-establishing a distinct seed = run the signed `rotate_secret` rail.

## 2026.7.43 — (folded into v2026.7.44 — never shipped healthy)

## 2026.7.42 — Hone PLAT-08: dependencies hash-locked, image installs --require-hashes

### Fixed
- **Boot provisioning no longer ALTERs existing role passwords** (`_ensure_role` is
  create-only at boot). The every-boot repave silently fought the explicit credential
  rails: on 2026-07-27, Core's local `db_role.key` seed vanished, boot fell back to the
  master key and repaved all 22 role passwords — while every WR-074-flipped addon still
  held old-key credentials in its stored options. Any addon that restarted crashed on DB
  auth (PWM did). Password changes now belong ONLY to the signed `rotate_secret` rail
  (`create_addon_roles(..., repave=True)`) and cred-flip. The isolated `*_test` cluster
  still repaves (same carve-out + predicate as the WR-192 divergence guard).
- **`publish_box_db_key_to_share` refuses to pave over a conflicting `/share` key.** The
  unconditional every-boot publish ran BEFORE the WR-192 divergence guard, so a drifted
  local key overwrote `/share` first and the guard always compared equal — neutered by
  its own boot ordering. A differing `/share` key now stays put: CRITICAL log + HA
  persistent notification, remedy is deliberate (reconcile local↔/share or rotate).
  `force=True` is reserved for the signed rotation rail.
- 8 regression tests (`tests/test_role_provisioning_create_only.py`) pin all three
  behaviours: no boot ALTER, refuse-publish-on-conflict (+ evidence preserved), rotation
  as the one forced/repave caller.

### Operational note (dev box, 2026-07-27 evening)
- Incident recovery: all 10 flipped addons re-converged on the current derivation via the
  cred-flip semantics (Peter-run, one at a time, health-verified 11/11 `db_ok`). The
  distinct rotation seed is GONE — the fleet now derives from the master key (Phase-1a
  fallback). Re-establishing a distinct seed = run the signed `rotate_secret` rail.

## 2026.7.42 — Hone PLAT-08: dependencies hash-locked, image installs --require-hashes

### Security
- **`requirements.lock` regenerated with `pip-compile --generate-hashes --allow-unsafe`**
  (55 packages, 1275 sha256 hashes, 0 unhashed — pip/setuptools pinned too). The old
  lock carried zero `--hash` lines, so the image build would accept any archive a
  compromised index/mirror served for a pinned version.
- **Dockerfile installs ONLY from the lock with `--require-hashes`** — a package whose
  archive doesn't match its recorded hash, or any dep missing from the lock, aborts the
  build. No unverified fallback path (GSM v2026.7.33 donor pattern, fail-closed).
- **`.github/dependabot.yml` added** (pip + docker + github-actions, weekly) — the
  SRV-PLAT-05 outdated-dependency tracking half; PRs update `requirements.txt` and the
  hash lock is regenerated alongside the merge (command pinned in the file header).
- Proven both ways before ship: clean lock resolves + hash-checks (exit 0); one flipped
  hash byte → pip refuses with "THESE PACKAGES DO NOT MATCH THE HASHES".

## 2026.7.41 — WR-PS-192 hardening: role re-mint refuses on key divergence + restart-addon uses `self`

### Fixed
- **`create_addon_roles` now refuses to re-provision when Core's local db-role key
  has drifted from `/share/paddisense/db_role.key`** (the copy the addons derive
  from). Every boot it ALTERs role passwords to the local-derived value; if a
  rapid-redeploy race churns local `/data` away from `/share` (the 2026-07-27
  incident), an un-guarded re-mint would set every role to a password the addons
  don't have and break fleet DB auth at once. The guard is fleet-only (skipped on
  the `*_test` cluster) and logs CRITICAL, leaving roles intact — the fix is to
  reconcile local↔`/share` (a clean restart's `publish_box_db_key_to_share` does
  this, which recovered it live). Note: the earlier "stale in-memory cache" framing
  was wrong — `get_db_role_key_bytes()` reads the file each call; the real fault is
  local↔`/share` file drift, which this guards.
- **`/admin/restart-addon` now targets `/addons/self/restart`** instead of an
  env/hostname-derived slug that Supervisor 404'd on (found driving the WR-192
  recovery — the restart endpoint returned 500 "HTTP 404"). `self` is Supervisor's
  canonical self-reference, same idiom `heartbeat.py` already uses.
- 6 tests: divergence detection (differs/matches/no-share), guard refuses-before-
  write, proceeds-when-aligned, and skips on the test cluster.

## 2026.7.40 — cred-flip: verify the LIVE admin-pool role, not just db_ok (weak-signal gap)

### Fixed
- **A flip is "done" only when the admin pool actually connects as the owner
  role** (`pg_stat_activity` check), not when `/health db_ok` is true. `db_ok`
  reflects the runtime-derived `*_app` pool, which works regardless of the
  flip — so an addon whose build predates the `db_user`→admin-pool mapping (or
  that never restarted into it) reported success/"already flipped" while its
  admin pool stayed on the `postgres` superuser (found live 2026-07-27 on
  store/planner/farm). Now: "already flipped" requires the owner role live;
  success requires `db_ok` AND owner-live, else roll back with an honest error
  naming the likely cause (stale build). +2 tests.

## 2026.7.39 — WR-PS-116 Core half: the §9-A.12 addon_update executor (fleet rollout rail)

### Added
- **Core now receives and executes Admin's signed `addon_update` directives**
  (`core/update_directive.py`) — the box-side half of the "Roll out to fleet"
  gate (Admin half live in v2026.7.77/.78). Built against the FROZEN
  `SIGNED_LICENCE_CONTRACT.md §9-A.12`, riding the existing
  `signed_instructions[]` heartbeat array beside owner_reset/rotate_secret.
- **Verify → bind → quiet-window → execute:** pinned-key Ed25519 + payload-
  carried 15-min TTL + nonce + durable HWM; then the three bindings that make
  a captured directive inert — `target` == this box's server_id, installed ==
  `from_version`, catalog head == `target_version` (store-reloaded first) —
  plus a fleet-slug allowlist (admin/gsm excluded). Wrong box / wrong version /
  catalog mismatch ⇒ refuse loudly, never install.
- **Quiet window (Amendment 5 by construction — no box-side queue):** a
  deferred delivery is simply declined and re-served by Admin next heartbeat,
  so whatever installs was verified seconds earlier and a Halt stops the flow
  within one beat. `normal` defers on any `busy_reason`; `critical` installs
  through pump/flush but still waits for `valve_moving`. Health `busy_reason`
  is the v1 interface (PWM grows the field at bench time; absent = clear).
- **Attestation** `extra.addon_update` on every heartbeat (old→new + result)
  for Admin's convergence view — written before dispatch so Core-updating-Core
  survives its own container restart. `auto_update`-ON is flagged loudly (it
  would bypass the gate). Supervisor prior-image watchdog = recorded follow-up
  (§9-A.12 amendment 2). 12 tests across the full frozen matrix.

## 2026.7.38 — cred-flip: non-canary failures are independent (farm mid-deploy stranded store/planner)

### Fixed
- **flip_all no longer aborts the whole pass on a non-canary failure.** Live
  lesson: farm bounced twice (mid-deploy on another Claude's session) and its
  abort stranded store + planner on the superuser. A failed CANARY still
  aborts (systemic doubt); after a good canary each attempt is independent —
  it rolled itself back, the rest get their turn, failures are collected and
  reported. Farm now runs second-to-last, PWM last. +1 test, order test
  extended.

## 2026.7.37 — 🔴 restore misroute fixed: date-stamped backups restored into the WRONG database

### Security / Fixed
- **Caught live by the WR-074 step-4 restore drill:** `_detect_target_db` could
  not match date-stamped filenames (`2026.07.27-paddisense-safety.sql.gz.enc` —
  the `startswith` never fired past the date), and the fallthrough DEFAULTED to
  `paddicore` — Safety's dump restored into Core's database. Every dated addon
  backup restored via DB01 has been misrouting this way. Fix: the date/time
  stamp is stripped before matching, and BOTH detection paths (on-box +
  upload) now **fail closed** — an unrecognisable filename is refused with a
  400, never guessed. 10 regression tests incl. the exact incident filename
  (proven-fail pre-fix).
- **Cleanup migration `drop_misrouted_restore_leak`** removes the leaked
  foreign tables (`wss_*`) from paddicore — idempotent, heals any box that
  ever hit the same misroute (notification_* already covered by the legacy
  drop). Damage audit on dev: Core's own tables and users untouched (the
  colliding `ps_users` COPY appended nothing); leak was 6 foreign tables.

## 2026.7.36 — WR-PS-074 Phase-2 half (i): THE credential flip (existing boxes off the shared superuser)

### Security
- **Every domain addon's saved options flip off `db_user: postgres` /
  `db_password: homeassistant` onto its per-DB owner role** (`pwm_owner`,
  `farm_owner`, … — DDL inside its own database, nothing else), with the
  box-derived password. A leaked addon credential no longer opens every
  database on the box. Core itself is deliberately NOT flipped (gateway:
  creates DBs/roles, takes the fleet backup — its superuser rotation is the
  ADR-013/SEC-08 lane). The `*_app` DML pools are untouched.
- **Fail-closed verify harness (Peter-ratified order):** box gate =
  owner-roles verify 11/11 `flip_ready`; per addon: a REAL owner-role login
  BEFORE options are touched → Supervisor options write → restart → poll
  `/health db_ok` → on failure the previous credentials are restored, the
  addon restarted again, and a persistent notification raised (R171).
  Sequential with canary ordering: safety first, PWM last, abort on first
  failure. Idempotent (already-flipped addons skip).
- **Unattended execution for grower boxes:** startup task, default ON
  (code-default — grower boxes have no env plumbing; `PS_CRED_FLIP_AUTO=0`
  kill-switch), plus `/admin/cred-flip {slug}` + `/admin/cred-flip-all`
  for manual canary/re-run. 8 tests (pre-verify gates the flip, rollback
  proven, canary order pinned, kill-switch honoured).

## 2026.7.35 — SSRF guard runs at send time (Hone SEC-10 rebind TOCTOU)

### Security
- **The heartbeat sender re-runs the SSRF guard immediately before every
  POST.** The URL was validated at save, but a DNS record re-pointed at an
  internal target afterwards sailed through the 5-minute send (save→fetch
  rebind TOCTOU, the documented SEC-10 residual). The send-time re-check
  shrinks the window from days to the check→connect gap of one request; a
  rebound-internal URL is refused with a SECURITY log and the heartbeat
  marked failed. Full resolve-and-pin considered + rejected: IP-pinning
  breaks TLS hostname verification on the fleet's lifeline for a
  defence-in-depth residual. Tests prove refuse-internal and still-sends-
  external (and caught that py3.12 correctly treats TEST-NET as private).

## 2026.7.34 — Executable migration rollbacks (Hone SCAL-04)

### Added
- **`MIGRATION_ROLLBACKS` ledger + `rollback_migration(name)` + CLI**
  (`python3 -m paddicore.core.db._migrate --rollback <name>` / `--list-rollbacks`).
  Every migration now carries a tested, executable down() — or an explicit
  `None` marking it IRREVERSIBLE, where the tool refuses and points at the
  daily backups instead of pretending a data-drop can be undone. Rollbacks are
  audited; the idempotent forward pass re-applies cleanly after a rollback
  (round-trip pinned by test). A completeness test fails the suite if a future
  migration lands without a rollback decision — the comment-only gap SCAL-04
  flagged can't silently return. (Note: the register's cited GSM donor
  `tools/rollback-migration.py` does not exist — flagged for the provenance
  gate; this is a fresh build.)

## 2026.7.33 — Dependency CVE refresh (release gate catch, Rule 155)

### Security
- **pip-audit blocked the v2026.7.32 grower cut on fresh PYSEC-2026 advisories**
  (published since the 2026-07-17 cut) — the stricter WR-PS-157 release gate
  working as signed. Bumped: Pillow 12.2.0→12.3.0 (runtime pin), and in the
  audit lock: urllib3 1.26.20→2.7.0, requests→2.33.1, starlette→1.3.1 (now
  matching requirements.txt), python-multipart→0.0.31, setuptools→83.0.0,
  soupsieve→2.8.4, cryptography→48.0.1, idna→3.15, msgpack→1.2.1,
  aiohttp→3.14.1, brotli→1.2.0. `requirements.lock` regenerated;
  pip-audit: **no known vulnerabilities**. Full suite 342 green on the
  upgraded tree (urllib3 2.x major included); ruff/mypy clean.

## 2026.7.32 — "Trust this device" on login (kills the third-password wall for growers)

### Added
- **Trust this device — stay signed in** tick box on /login (desktop + mobile).
  Core sessions are 12 h AND in-memory, so every timeout and every addon
  restart/update demanded the console password again — a third wall behind the
  device lock and the HA login. A trusted device now carries a DB-backed token
  (SHA-256 at rest, `ps_trusted_devices`, sliding 90-day window — each visit
  extends it) that silently re-mints the session, surviving restarts and
  updates. Unticked = exactly today's 12 h behaviour.
- **Revocation is total on credential change:** any password change/reset
  revokes ALL the user's trusted devices — wired inside the R188 session
  revocation so every present and future path (admin reset, self-change,
  starter re-issue, owner_reset recovery) is covered. Sign-out un-trusts that
  device; deactivated users can't redeem; a must-change (starter/reset)
  password can never redeem, and a tick made through a must-change login is
  only honoured once the password is personalised.
- 12 new tests (token custody, restart survival via the real middleware,
  sliding window, every revocation path, deferred trust, session-fixture
  isolation for the simulated restarts).

## 2026.7.31 — Mobile hub: User Access tile (was unreachable on mobile)

### Fixed
- **User management now has a door on mobile.** Desktop reaches UA01 via the
  sidebar; mobile has no sidebar and the hub had no tile — so the Access page
  (which fully exists on mobile) was unreachable from a phone. Added the
  User Access tile to the mobile hub (H01.M), admin-only to match the
  `/access` route guard. Peter-directed, pre-grower-cut.

## 2026.7.30 — Access gate Rev 2: the lock arms on the FARM OWNER, never on commissioning (Peter-directed)

### Changed
- **The console lock now arms on exactly one event: the designated Farm Owner
  account being personalised** (the farmer signs in with the starter password
  and sets their own). The fleet administrator's commissioning work — DB
  password, the `owner` administration password, their own admin console
  account — never latches the box. The Rev 1 predicate (owner + any linked
  admin personalised) latched a grower box during commissioning and locked the
  farmer out before they existed in the system; that exact state is now the
  proven-fail regression test (`test_commissioning_never_locks`).
- **Farm Owner is a designation, not a username** — held by exactly one console
  account per box (schema-enforced partial unique index), assigned and MOVED in
  user management by admin authority, so an existing account on an already-armed
  box can be flipped to Farm Owner. Moving or removing it never releases the
  latch. The seeded `owner` break-glass can never hold it.
- **The seeded `owner` account now displays as "Administrator"** (login name
  unchanged — recovery ladder untouched); UA01 card, banners, and dashboard
  gate notes rewritten around the new arming step.
- After the lock, both the administrator and the farm owner can add/edit users
  (both are admin authority — pinned by test).

### Added
- Migration `ps_users_farm_owner_designation` (additive, rollback comment):
  `is_farm_owner` + one-per-box partial unique index + Administrator display
  rename. `farm_owner` flag on the access-entry API; designation service
  `users.sync_farm_owner` (audited assign/move/remove, fail-closed guards).
- Tests: 9 new/rewritten gate cases (commissioning-never-locks proven live to
  fail under Rev 1 — locked=True on the old predicate, False on Rev 2);
  conftest now runs migrations up-front so DB-direct tests are order-independent.

## 2026.7.29 — fix: recovery password-change audits `via_recovery: true` (drill-verify find)

### Fixed
- **The password-change audit row now records its recovery provenance
  correctly.** The kept session's `via_recovery` flag is cleared during the
  change (same dict), so the post-change audit read logged `false` for a
  genuine recovery — flag now captured before the change. Behavioural skip
  logic was always correct; audit-accuracy only. Pinned in the flow test.

## 2026.7.28 — Grower-simple owner recovery flow (Peter's UX spec from the live drill)

### Added
- **`/recovery` — one box, type the code, done.** No username (there is exactly
  one break-glass account); the code is normalised (spaces stripped, upcased) so
  a grower on the phone can type it spaced or lowercase. The door only EXISTS
  while an Admin-issued recovery is pending — no standing code-entry surface —
  and the login page grows a "Have a recovery code?" link at the same moment,
  which doubles as the "it's arrived" cue on a support call. Rate-limited
  (sensitive-path middleware + the login attempt lockout), audited on every
  failure, timing-uniform verify.

### Changed
- **The recovery code is never re-asked.** A `via_recovery` session (minted at
  code entry) skips the current-password field on the change screen — the code
  WAS the credential, seconds earlier. Ordinary sessions still require it
  (test-pinned).
- **No third login.** Changing your own password keeps YOUR session (lands on
  the hub signed in); every OTHER cookie for the user still dies — Rule 188's
  stolen-cookie intent preserved, the ceremony removed.
- **New-password fields are visible by default** (two fields + confirm, with a
  "Hide what I type" toggle) — a blind typo re-locks a just-recovered grower.

6-case behavioural flow test (door gating, link appearance, wrong/right code,
skip-reask + session survival + other-cookie death, no-skip for normal sessions).

## 2026.7.27 — Sign-out button + honest UA01 recovery-state wording (drill UX finds)

### Added
- **A visible Sign out** — desktop sidebar footer + a slim mobile bar — shown
  only for real cookie sessions (`user_id > 0`); ingress-trusted callers have
  no session to end, so they never see a no-op button. (Found during the
  WR-184 recovery drill: `/logout` existed but nothing surfaced it.)

### Changed
- **UA01 no longer calls a recovery code "the default password".**
  `list_users` marks the owner row `recovery_pending` when its hash is the
  bcrypt/argon2 `$…` form an Admin-signed owner_reset installs (boolean only —
  the hash never leaves the service); the banner now says "Recovery code set —
  sign in as owner with the code" for that state.

## 2026.7.26 — fix: upload-restore path also fail-closed (pinned-mypy catch)

### Fixed
- **`_restore_file` (the upload-restore path) now handles the fail-closed owner
  refusal** — the second `_run_psql_restore` call site missed the v2026.7.24
  `None` contract; the release gate's pinned mypy caught it before the grower
  build dispatched. Refusal → audit row + explicit error, same as the named
  restore path.

## 2026.7.25 — WR-PS-183: redactor re-vendored (all six GitHub token classes)

### Changed
- **`core/_log_redactor.py` re-synced byte-identical to the patched canonical**:
  the single `gh[posur]_` class now masks `ghp_`/`gho_`/`ghs_`/`ghu_`/`ghr_`
  (classic PAT, OAuth, server-to-server, user-to-server, refresh) alongside
  `github_pat_` — closing the WR-PS-183 completeness sliver A found during the
  Admin fan-out. Shared test refreshed (4 new fixtures).

## 2026.7.24 — WR-PS-074 Phase 2: per-DB owner roles + owner-role restore (provision-verify half)

### Added
- **Per-database OWNER roles** (`<prefix>_owner` beside each `<prefix>_app`):
  minted at startup, NOSUPERUSER/NOCREATEDB/NOCREATEROLE, password derived from
  the box DB-role key (same family as the app roles, so seed rotation re-mints
  both). Each addon database, its public schema and every object hand over to
  its owner; default privileges are re-declared FOR the owner so future tables
  (restores, migrations) stay DML-visible to the app role.
- **`verify_owner_roles`** — the Peter-ratified pre-flip gate: a REAL login per
  owner + database/schema ownership checks, run on every startup and exposed at
  `GET /admin/owner-roles-verify` (`flip_ready: true` == this box may flip its
  config defaults off `db_user: postgres`, WR-PS-100).

### Fixed
- **Restore no longer runs as the cluster superuser (Hone PS-SEC-11 step 2/3).**
  `_run_psql_restore` connects as the target DB's owner role; a crafted `.sql`
  `COPY … FROM PROGRAM` now executes with one-database blast radius instead of
  superuser over every grower table. FAIL-CLOSED: owner role unknown or not
  authenticating → restore REFUSED (503 + audit row) — no superuser fallback,
  ever. Dumps were already `--no-owner --no-acl`, so restores-as-owner are clean.

### NOT in this release (deliberately — ratified order)
- The addon config-default flip off `db_user: postgres`/`db_password:
  homeassistant` (ex-WR-100) ships only after `owner-roles-verify` reads
  `flip_ready` on every box — provision + VERIFY first, then flip.

## 2026.7.23 — WR-PS-148: §9-A.11 owner_reset box-side executor

### Added
- **The absolute recovery rung is live on the box side.** `core/owner_reset.py`
  consumes an Admin-signed `owner_reset` instruction from the heartbeat
  response (same `signed_instructions[]` array as `rotate_secret`): pinned-key
  Ed25519 verify → §6 freshness + single-use nonce + durable issued_at HWM →
  custody machine-check (`code_hash` must be bcrypt/argon2-shaped; ANY
  plaintext credential field → `owner_reset_policy_violation`) → sets the
  seeded `owner` account's hash + `must_change_password=TRUE`. Loud on apply:
  audit row + WARNING (heartbeat carries the audit tail) + HA persistent
  notification. Attests `extra.secrets["owner_reset"] = {applied, at}` — never
  a hash or code. 15-case test matrix per the frozen contract.
- **`verify_password` now dispatches on hash form** — bcrypt (`$2…`) and
  argon2 (`$argon2…`) verify alongside the local PBKDF2 form, so the recovery
  code Admin hashes actually logs in; `must_change_password` immediately
  replaces it with a local hash. Deps: `bcrypt==5.0.0`, `argon2-cffi==25.1.0`.

## 2026.7.22 — Revert AppArmor profile (broke addon start under real enforcement)

### Fixed
- **Removed `apparmor.txt`** — v2026.7.21's profile was accepted by Supervisor (`apparmor: profile`)
  but the addon went to `state: error` under real enforcement: a denial in the profile blocks the
  container from starting. Reverted to the Supervisor default so Core starts. PLAT-09/11 stays open;
  the profile needs proper bench debugging with AppArmor audit logs (which denial breaks start)
  before it can ship — dev-box enforcement caught it, exactly what the isolated bump was for.

## 2026.7.21 — Ship AppArmor MAC profile (Hone PS-PLAT-09 / PS-PLAT-11)

### Added
- **`apparmor.txt`** — a mandatory-access-control profile (Peter ruling 2026-07-13, "ship it").
  Keeps normal operation permissive (files/network/capabilities the python+bash runtime uses) and
  DENIES the container-escape / host-tamper primitives an addon never needs: mount/umount/remount/
  pivotroot, ptrace, raw kernel memory (`/dev/mem`, `@{PROC}/pid/mem`), kernel sysctls, firmware.
  ⚠ Enforcement validation is owed on the real HA Green target before a grower cut — AppArmor is a
  host-kernel feature and the dev box may not apply it; this dev-deploy only confirms the addon
  still starts healthy with the profile present.

## 2026.7.20 — Enforce default-password change + adopt fleet-canonical redactor (Hone SEC-03 · WR-PS-179)

### Changed
- **SEC-03: a legacy admin account still on the literal default password `admin` is now ENFORCED,
  not just warned** — `ensure_first_user` sets `must_change_password`, so the existing middleware
  gate redirects that account straight to `/change-password` before it can reach anything. No
  lockout (they still log in with `admin`, then must change). Fresh boxes were never on `admin`
  (random per-box secret); this closes the legacy path.
- **Adopted the fleet-canonical `documentation/shared/log_redactor.py`** (WR-PS-179, G steward) —
  `core/_log_redactor.py` re-vendored byte-identical (`cmp -s`). A superset of Core's prior
  redactor: gains portal reset/activate/session tokens, Resend/`hbk_` shapes, URL-userinfo + SQL
  `PASSWORD '…'` masking, and the `extra={}`-walking formatter. `RedactingFormatter`/`redact()`
  call sites unchanged. Canonical behavioural test adopted (23 secret/PII cases + 6 keep + idempotence).

## 2026.7.19 — Log redaction extended to DB creds, keys & PII (Hone SEC-17 / KEY-01 / DATA-01)

### Fixed
- **`core/_log_redactor.py` now redacts the secret classes it was missing** — Postgres DSN
  passwords + `PGPASSWORD`, labelled `password`/`secret`/`api_key`/`admin_key`/`passphrase`/
  `shared_secret`/`client_secret`/`*_token` values, and Fernet `enc:` at-rest tokens — plus
  **PII**: email addresses and AU/international phone numbers. Previously only cloudhook
  URLs / PATs / Bearer tokens were stripped (Hone PS-SEC-17), and no PII pattern existed
  (PS-DATA-01). Conservative by design: patterns target labelled secret contexts + clearly
  shaped PII, so operational data (versions, epochs, ports, key fingerprints, paddock names)
  survives — proven by `test_log_redactor.py` (19: secrets gone, PII gone, ops-lines unchanged).

## 2026.7.18 — Fix: a failed restore-upload poisoned the restore-test into false alarms

### Fixed
- **`/admin/restore-upload` left FAILED uploads in the live `/config/backups/`** — the leftover
  became the newest `.enc` by mtime, so every later R174 restore-test picked it and fired a false
  "RESTORE-TEST FAILED" alert while real backups were healthy. Found live during release-prep: the
  test suite's own `not-a-real-token` upload fixture kept resurrecting a 16-byte stub via the REAL
  endpoint (root cause of the recurring 2026.07.09 stub, incl. its "reappearance" after the 07-12
  cleanup — every pytest run re-created it). A failed upload-restore is now unlinked (a successful
  restore keeps its artifact); the test module isolates `_BACKUP_DIR` to tmp_path so suites never
  write production paths; regression `test_failed_upload_leaves_no_stub_behind` (R106/R174).

## 2026.7.17 — Fix: real Admin-signed instructions were rejected — verifier + HWM (WR-ADMIN-006)

### Fixed
- **Re-vendored `core/licence_verify.py`** byte-identical to the fixed canonical (23378e0):
  `verify_artifact` accepts the licence id under `target` (real instruction shape, §4/§9-A.5.2) —
  pre-fix every REAL Admin revoke/deactivate/rotate-adjacent instruction was rejected as
  `invalid_signature` (latent since 2026-07-01; found by A's WR-ADMIN-006 live test). Core's copy
  is now byte-identical to shared/ again (the local `reload_pubkeys` removal is reverted — one
  canonical version fleet-wide, per A's reconciliation ask).
- **Second site fixed: `licence_state._accept_issued_at`** read `licence_id` only, so even a
  VERIFIED revoke died on the durable replay HWM (fail-closed) and never applied — now
  `licence_id or target` (same id space, so a revoke advances the same per-licence HWM and an
  older captured licence cannot undo a newer revoke). Regression
  `test_verified_revoke_applies_real_shape_target_only` uses the REAL wire shape (target only,
  no licence_id) — proven to FAIL pre-fix with A's exact failure signature; the old fixture
  carried BOTH keys, which is how the dead path passed every gate (Rule 106).

## 2026.7.16 — Planner added to the SEC-04 licence-forward map

### Fixed
- **`PRODUCT_SLUG` was missing `planner`** — Core silently never forwarded Admin-signed planner
  licence artifacts (the WR-PS-109 Planner catch-up added the access gate but not the forward
  entry). Planner shipped its verify stack at v2026.7.1 (enforcement ON), so the forward now has a
  verifying receiver. Admin still needs to ISSUE planner licences (WR filed) — until then the
  heartbeat carries no planner row and the entry is inert.

## 2026.7.15 — Warn→block flip: licence-signature + node-lock enforcement ON by default (SEC-01/04 · §9-A.10)

### Changed
- **`PS_LICENCE_ENFORCE_SIG` now defaults ON** — an unsigned connection code is rejected at
  `/gsm/api/enroll-core`. Readiness evidence: Admin signs every licence fleet-wide (v2026.7.52
  re-issue landed 2026-07-12, live-verified on-box: signed artifacts in the heartbeat `licences[]`,
  HWM advancing, state `active`). A present-but-bad signature was already always fatal; this flip
  closes the absent-signature legacy path. `PS_LICENCE_ENFORCE_SIG=0` = emergency kill-switch.
- **`PS_LICENCE_NODELOCK_ENFORCE` now defaults ON** (§9-A.10) — a verified licence bound to a
  different box degrades to unlicensed-tier (banner + updates stop, NEVER operation). Inert on the
  live fleet today: the 07-12 re-issue delivered `bound_fp` EMPTY (verified on-box in the heartbeat
  artifacts + SugarSense's persisted licence — pushed back to A), and empty/absent = unbound = no
  check. Arms automatically when genuinely bound licences arrive. `PS_LICENCE_NODELOCK_ENFORCE=0`
  = kill-switch. Rationale for default-flip over env-flip: grower boxes have NO options plumbing to
  set an env var — a code default is the only mechanism that actually reaches the fleet.
- Tests: `test_licence_sig_enforce.py` (6 — default-on, kill-switch, unsigned-rejected,
  forgery-fatal-even-killswitched) + `test_licence_nodelock.py` default-enforced case (+1).

## 2026.7.14 — Access-sync push is now Ed25519-signed (WR-PS-108 / §9-A.9 rev-3, sender)

### Added
- **Core signs each `/api/access/sync` push with its box identity** (SEC-04, on-box). `access_push.build_signed_body(target)` wraps the grant set in the §9-A.9 freshness envelope (`kind`/`target`/`issued_at`/`exp`/`nonce`) and attaches an **additive** `_sig` (`{ed25519, box_pubkey, box_fp}`) over `canonical(payload)`. **Per-target** — the signed `target` binds the grant set to one add-on so a compromised sibling on the `/23` can't replay it elsewhere. Signed per §9-A.9 rev-3: the payload is signed **exactly as it already flows** (bool/list[str] leaves — A's ruling, "authenticate first, normalise later"), so zero receiver-shape change.
- **`signed_push.canonical()`** — the ONE §9-A.2 canonicalisation both the signer and every receiver use (rev-3 condition 1); `sign_canonical()` signs it directly (freshness lives in the payload). The heartbeat leg's `canonical_base` now shares it. `tests/test_signed_push.py` + `tests/test_access_push.py` (+6).

**Inert until the receivers verify:** `_sig` is additive — a receiver that doesn't yet verify ignores it (backward-compatible). Next: the `bound_fp`-authenticated verify-and-pin receiver (SugarSense reference → fan-out, warn-only), then the coordinated enforce flip after A's fleet licence re-issue (WR-PS-112 item 0, done).

## 2026.7.13 — Shared Ed25519 signed-push helper (WR-PS-108 / §9-A.9, step 1)

### Added
- **`core/signed_push.py` — the single signed-push mechanism** the §9-A.9 rev-2 scheme (settled A+P+G)
  mandates be implemented ONCE across the three Core-family legs (box→GSM heartbeat, Core→add-on
  access-sync, Farm boundary). `canonical_base()` builds the `<ts>.<nonce>.<sha256(canonical)>` base
  (payload minus `_sig`, §9-A.2 canonicalisation); `ed25519_over()` returns the `{ed25519, box_pubkey,
  box_fp}` block signed with `box_identity` (private key in `/data`, never on `/share`); `build_sig()`
  returns the full `_sig` block. Fail-soft: no box key → None → caller pushes unsigned (warn-only only).
  `tests/test_signed_push.py` (5).

### Changed
- **`heartbeat._sign_envelope` now builds on the shared helper** (behaviour-preserving) — proving the
  mechanism on the live Admin-heartbeat leg before the GSM-sender + access-sync fan-out. The heartbeat
  still carries both the transitional HMAC and the additive Ed25519 block over the identical base;
  `tests/test_heartbeat_box_identity.py` unchanged and green.

**Not yet wired (next steps, still warn-only/inert):** the box→GSM heartbeat SENDER (needs the Core→GSM
path decision — Core currently reaches GSM only for boundary, not a heartbeat; flagged to G on WR-PS-172/108),
then the access-sync `_sig` + the `bound_fp`-authenticated receiver, then the coordinated enforce flip
(after A's fleet licence re-issue, WR-PS-112 item 0).

## 2026.7.12 — Fail-closed backup writer (WR-PS-175 sibling defect)

### Fixed
- **The daily backup writer now fails closed on an empty/truncated pg_dump instead of encrypting a
  stub.** `_run_pg_dump` checked only pg_dump's exit code — but pg_dump can exit 0 and hand back an
  empty/truncated stream (seen during the 2026-07-x restart churn), which was then gzipped, encrypted
  and written as a 16-byte `.enc` that overwrote nothing useful and later fooled the restore-test into
  a misleading "backup key mismatch" alarm. New `_dump_is_valid()` gate (header + 512-byte floor, the
  same "real dump" definition R174 checks) runs BEFORE the write; an invalid dump is refused, logged as
  `invalid_dump`, and the previous good backup is left intact. `tests/test_backup_failclosed.py` (6).
- **Restore-test alert text corrected (R106/R174).** A sub-`MIN_DUMP_BYTES` `.enc` is now reported as a
  truncated STUB ("not a key mismatch"), not as a decryption/key failure — the old text sent the reader
  hunting a non-existent key problem. The corrupt 2026-07-09 16-byte stub was removed from
  `/config/backups` + `/share/paddicore_backups` (the `.corrupt-16bytes` quarantine copy is retained).

## 2026.7.11 — Resilience after the 2026-07-10 /share key divergence (WR-PS-175)

### Fixed
- **Second-tier DB self-heal: converge on the `/share` key when the local-first key can't authenticate.**
  Core derives its `paddicore_app` password local-first, but the roles are minted from whatever seed is
  on `/share`. On 2026-07-10 an out-of-band writer put a different key on `/share` and re-minted the
  roles from it; every `/share`-reading sibling converged and stayed green, while Core — re-reading the
  same local key on each self-heal — could never converge and went **dark to Admin for two days**. The
  app-pool self-heal now has a bounded second tier: after a local rebuild still fails auth, it re-derives
  the password from the `/share`-published key ONCE and retries (`crypto.get_db_role_key_bytes_from_share`,
  `_pool._acquire_conn_from_share`). Fail-closed preserved — if `/share` has no key, or the shared-derived
  password also fails, the original auth error propagates (R173). Loudly logged so the divergence is one
  line, not a silent 2-day outage. `tests/test_pool_selfheal.py` (+3: converge-from-share, no-shared-key,
  both-fail-restore-local).

### Added
- **On-box operator alert when the box stops reporting to Admin** (WR-PS-175 Q2). A degraded-but-not-down
  box (licence read fails → no `heartbeat_url` → every heartbeat silently skipped) previously went dark
  with no on-box surface. The heartbeat loop now counts consecutive non-deliveries; at 3 (~15 min) it
  raises an HA persistent notification naming the likely cause (no-licence/DB-key vs Admin-unreachable),
  and clears it on the next successful delivery. New Supervisor-adapter helpers `create_/dismiss_
  persistent_notification` (Rule 133). `tests/test_heartbeat_alert.py` (3).

## 2026.7.10 — Hub tells the truth; root lands on the hub

### Fixed
- **Hub grid showed the whole fleet as "not installed" (Peter, live):** the grid probed
  `http://localhost:<port>/health` from the BROWSER — only ever worked with a browser running
  on the HA box; every remote/ingress viewer saw a dead fleet. Its hardcoded addon list was
  also stale (wrong ports, missing Weather/Store/Farm/Planner). New `GET /api/fleet-health`
  (session-auth) polls server-side via the heartbeat collector (off-thread, R121); both hub
  templates consume it; non-PaddiSense addons filtered; Core listed first (serving the
  response is its liveness proof). Tests: 401 anon + shape/filter behaviour.
- **"Two licence pages":** root `/` rendered the licence page (v353 gateway posture) while the
  post-login flow landed on the hub — the HA sidebar and the login flow disagreed about home.
  Root now renders the hub; an unlicensed box still lands on `/licence` via the licence gate.

## 2026.7.9 — Login accepts the name as the user knows it + two live-found activation bugs

### Fixed
- **Session cookie dropped on plain-HTTP HA (the "not authenticated" loop):** the cookie
  carried an unconditional `Secure` flag, so on LAN `http://<ip>:8123` the browser silently
  discarded it — login 302'd but no session survived, and `/api/change-password` refused the
  ambient ingress identity (`user_id 0`). Secure now follows `X-Forwarded-Proto` (Farm's
  heuristic, R181's production twin). Same fix on the logout delete.
- **Self-set passwords skip must-change:** forcing a user to re-choose a password they typed
  seconds ago is friction with no security gain. When the granting admin's HA identity IS the
  entry being granted, the password counts as personalised immediately — meaning the box can
  lock straight from the UA01 save, no sign-in-once step for the self-grant flow. Setting
  someone ELSE's password stays a must-change starter (granter never knows a live password).
- **Peter's login failures 2026-07-10 root-caused:** he typed his display name; the console
  username is a derived slug nobody is told to memorise. `/login` now normalises the typed
  username with the SAME transform that derives console usernames (`users.normalise_username`:
  lowercase, spaces→hyphens, alnum+hyphen) after an exact-match attempt (legacy names keep
  working). NOT display-name authentication — display names aren't unique; normalisation is
  deterministic onto the unique, pre-normalised username column, so the lookup is never
  ambiguous. Both lookups always run + the R190 dummy-verify stays (uniform work, no
  enumeration oracle). Test: form login as "Gatetest Login" reaches change-password.

## 2026.7.8 — UA01 gate banner is progressive (names the actual next step)

### Fixed
- **Stale banner guidance (Peter, 2026-07-10):** after setting the owner password AND an admin
  console password, the Access-page banner still recited the full "set the owner password and
  give your admin a console password" checklist. `GET /api/access` now returns `gate_progress`
  (`owner_personalised` · `admins_ready` · `admins_pending` usernames from
  `access_gate.progress()`), and both UA01 templates render the ONE remaining step:
  owner → console password → **"Almost locked — sign in once as \"<username>\" … sign in here"**
  (link). Banner also re-evaluates after an owner-password set (was only on entry saves).

## 2026.7.7 — Access gate activation flow: local sign-in outranks ingress; console username surfaced

### Fixed
- **Activation was impossible on an unlocked box (found by Peter's first use, 2026-07-10):**
  `require_auth` preferred ambient ingress identity over a freshly-minted /login cookie, so
  the must-change step never fired, the starter console password could never be personalised,
  and the lock could never arm. A deliberate local sign-in now ALWAYS outranks ingress trust
  (also makes the owner break-glass usable *through* ingress, which it previously wasn't).
  A stolen low-privilege cookie can only downgrade what an ingress user sees, never escalate;
  logout restores ingress trust. New test: cookie session (must-change) wins over ingress.
- **Console username was undiscoverable:** UA01 never showed the generated login name.
  Entries now display `console: <username>`; the save toast names the account and says
  "sign in once to activate the lock"; the console hint + the hub/access unlocked banners
  link straight to the sign-in page.

## 2026.7.6 — Console access gate: whole-addon password lock (DESIGN_CORE_ACCESS_GATE.md)

### Added
- **`core/access_gate.py`** — the lock predicate + write-once latch (`config.access_gate`).
  Locked ⇔ owner personalised AND ≥1 active, HA-linked, personalised admin console account
  (legacy unlinked `admin` row deliberately excluded). Latch never auto-releases; flip is
  audited + WARNING-logged (R32/R171). Fail-open on DB error (gate never takes the box down).
- **Ingress narrowing** (`auth.require_auth`): once locked, ingress no longer authenticates —
  the session cookie is the only credential. Closes T1 (HA-admin resets another HA user's HA
  password → inherits their PaddiSense role; every HA user must be an HA-admin per the
  side-panel constraint, so HA identity is spoofable between users). While UNLOCKED (setup),
  behaviour is byte-identical to v2026.7.5.
- **Grant-time console accounts** (§6): granting manager/admin on UA01 now creates (or syncs)
  a `ps_users` account linked via new `ha_user_id` column — starter password set by the
  granting admin, must-change on first login (owner-bootstrap pattern). Downgrade/delete of
  the entry deactivates the account + revokes sessions (R188). New UA01 password field
  (desktop + mobile); required-vs-keep-current driven by `console_linked` from `GET /api/access`.
- **Setup banner** on hub + Access pages while unlocked ("Core console is UNLOCKED — …").
  Base-template shell untouched (R177) — banner rides page content blocks.
- **`docs/RECOVERY.md`** — operator-facing 4-rung recovery ladder (admin→owner→signed
  owner-reset (WR-PS-148)→DB reseed). Previously this ladder existed only in code.
- `tests/test_access_gate.py` — 14 tests: predicate matrix (incl. legacy-admin exclusion +
  manager-doesn't-lock), latch persistence after losing the last admin, T1 e2e through the
  real middleware (locked ingress → 302 login / API 401; cookie session unaffected; setup
  mode unchanged), console-account service (required starter pw, sync, deactivate, collision).

### Changed
- **Core console sessions: 7 days → 12 hours** (`SESSION_MAX_AGE`) — the console re-locks
  daily-ish; domain addons are unaffected.
- Migration `ps_users_ha_user_id` (additive column + partial unique index; rollback noted).

### Migration behaviour (existing boxes)
No flag day: an updated box has no passworded console admins yet → stays UNLOCKED with the
banner until the grower's console password is set, then latches LOCKED. Deploying this
version changes nothing visible except the banner until that moment.

## 2026.7.5 — Planner missing from addon port map: grant pushes + health polls silently failed

### Fixed
- **Incident (found live 2026-07-10):** heartbeat.py carried private `_SLUG_PORTS` /
  `_PADDISENSE_SLUGS` copies that had drifted from the licence router's
  `_DEFAULT_ADDON_PORTS` — both missing `paddisense-planner`. The Supervisor `/addons`
  list returns no hostname/ingress_port, so Core fell back to port 8099 for Planner:
  every SEC-04/09 module-access grant push AND every fleet health poll to Planner
  failed silently (best-effort paths, debug-level logs; `access_push` counted
  "9 addon(s)" with nothing to compare against). Surfaced while verifying the Planner
  v2026.6.57 module_gate: Core could never deliver the grants it enforces.
- Fix at the source (R59): ONE canonical `ADDON_DEFAULT_PORTS` in `core/constants.py`;
  heartbeat's `_SLUG_PORTS`/`_PADDISENSE_SLUGS` and licence's `_DEFAULT_ADDON_PORTS`
  are now views of it. Adding a future addon means one entry, one file.

**Install/upgrade:** standard. **Rollback:** v2026.7.4. **Known risk:** Planner now
appears in fleet health polling + receives grant pushes — intended, previously broken.

## 2026.7.4 — release-gate lint sweep (pinned ruff 0.15.14)

### Fixed
- R64 pre-release gate: removed unused `is_sql` local in `api/admin.py::restore_upload`
  (dead since the v.416 SEC-11 `.enc`-only upload change — the sql fall-through path no
  longer branches on it; `_is_sql_backup` itself remains in use by the on-box restore path).
- UP037 dequoted three annotations made redundant by `from __future__ import annotations`:
  `box_identity._priv`, `box_identity._load_or_create`, `db/_pool._acquire_conn`.

No behavioural change. Release vehicle for the grower cut of v2026.6.405→v2026.7.3 work
(master-key durability WR-PS-110, self-heal pools, access enforcement, rotate_secret pilot).

**Install/upgrade:** standard (`ha store reload` → update). **Rollback:** previous grower
image v2026.6.404. **Known risk:** none new — code delta vs the dev-proven v2026.7.3 is
lint-only.

## 2026.7.3 — WR-PS-074 Phase-1 pilot: ADR-013 §9-A.8 rotate_secret box-side executor + attestation

### Added
- **`core/secret_rotation.py`** — the box-side executor for Admin-signed `rotate_secret`
  instructions (delivered on the heartbeat response's `signed_instructions[]`, §9-A.8). Pipeline:
  pinned-key Ed25519 verify (composing the frozen `licence_verify` primitives — the §9-A.8 payload
  keys its nonce on `target`, which `verify_artifact` cannot express; the frozen file is untouched)
  → §6 freshness → single-use nonce → **custody enforcement** (a box-local root arriving with a
  `value` is rejected `rotate_secret_policy_violation` — the ADR-013 D3 machine-check that stops a
  compromised Admin becoming a fleet skeleton key) → durable per-(target, kind) `issued_at`
  high-water mark (config table, survives restart) → per-kind execution + audit.
- **Phase-1 execution: `db_pw_<addon>_app`** rotates the shared DB-role seed — fresh 32-byte
  CSPRNG `db_role.key` (which also lands the WR-PS-088 1b split: the Fernet `master.key` stays
  local and no at-rest secret re-keys) → publish to `/share` → re-mint all `*_app` roles; the
  fleet's self-heal pools (deployed 2026-07-09) converge every addon without a restart. Per-kind
  granularity arrives with Phase-2 per-addon stored passwords (documented deviation in the module
  docstring). `db_pw_superuser`/`master_key`/`backup_key`/`box_pubkey_reset` verify + custody-check
  then log unimplemented — no attestation bump, so Admin's "presumed failed" flag stays honest.
- **Attestation (`extra.secrets`, HEARTBEAT_ENVELOPE §Secret attestation):** per-kind
  `{rotated, version, at}` persisted in the config table and emitted on every heartbeat — never a
  value (Admin ingestion 400s `attestation_leaks_value`); genesis kinds report
  `rotated: false, version: 1` so the secret-hygiene tile sees honest pre-rotation state.
- **`tests/test_secret_rotation.py`** (16) — real Ed25519 through the real entry point: valid
  apply; bad-sig/unknown-key/wrong-kind/expired/nonce-replay/tampered-payload all rejected; value
  on a box-local root rejected (both policies); unknown addon + unknown kind rejected; Phase-3 kind
  verified-not-executed; durable HWM rejects a captured older instruction after a newer applied;
  attestation bumps on apply, never carries a value, genesis reports unrotated.

## 2026.7.2 — WR-PS-095 / §9-A.10: licence node-locking verifier (Hone PS-LIC-04)

### Added
- **`bound_fp` consumer in the licence state driver** (`core/licence_state.py`). After the existing
  sig → freshness → nonce → issued_at-HWM checks, a licence carrying `bound_fp` must match this
  box's own Ed25519 fingerprint (`box_identity.box_fp()` — the PS-LIC-02 identity, private key
  never leaves the box). Mismatch → new `NODE_LOCKED` state: banner ("bound to different hardware —
  re-issue to re-bind") + updates stop — **never operation** (SEC-06 semantics); audited as
  `licence_node_lock_mismatch`. Null `bound_fp` = unbound, unchecked (ADR-003 internal licences).
- **Warn→enforce rollout per §9-A.7 discipline:** while `PS_LICENCE_NODELOCK_ENFORCE` is off
  (default), a mismatch logs a WOULD-BLOCK warning + audit row and the licence still applies —
  flip once Admin has re-issued bound licences fleet-wide. Enrol path logs the same check
  informationally; the heartbeat driver is the single enforcement point.
- **`tests/test_licence_nodelock.py`** (6) — unbound/matching activate; warn-mode mismatch applies
  with the would-block logged; enforced mismatch degrades to NODE_LOCKED with banner + updates off;
  identity-less box degrades (never crashes); a tampered `bound_fp` still fails the Ed25519 verify
  (node-lock sits behind the signature, not instead of it).

## 2026.7.1 — WR-PS-090 Ask 4: publisher-side box-key fingerprint log

### Changed
- **`core/crypto.py::get_db_role_key_bytes`** now logs the loaded key's source path, SHA-256
  fingerprint (12 hex), and mount identity (`dev`/`ino`/`size`/`mtime`) — once per process per
  value (`_log_key_fp`, no per-call spam: the key is read on every Fernet op). This is the
  publisher half of the PWM reference diagnostic (WR-PS-090 Ask 4): a consumer addon's logged
  `fp` can now be cross-checked against what Core actually publishes, the check that cracked the
  2026-07-06 fake-`/share` incident and the WR-PS-110 key churn. Key handling itself unchanged.
  First July cut — CalVer rolls 2026.6.420 → 2026.7.1.

## 2026.6.420 — 🔴 WR-PS-110 (P0): box master key survives a /data reset — no re-mint, no churn, no secret loss

### Fixed
- **`get_master_key_bytes` re-minted the box master key whenever `/data/keys/master.key` was absent at
  startup** (an addon `/data` volume reset — slug change on reinstall, or a volume remap on update). That
  single key both derives every `*_app` DB password AND is the Fernet at-rest key, so a fresh key
  simultaneously (a) broke every addon's DB auth (the live 2026-07-09 incident — surfaced as "PWM not
  licensed") and (b) made every Fernet-encrypted secret written under the previous key undecryptable
  (GSM shared secret, OAuth tokens). Confirmed live: a `provider_credentials` value encrypted 2026-06-01
  no longer decrypts, and `/share` (which IS this key — no distinct `db_role.key` is ever created) was
  rewritten across a plain Core restart, proving `/data` did not persist it.
- **Now the key is DURABLE:** before minting, Core recovers it from the `/share` copy it published
  (`/share` survives an addon `/data` reset). It generates a fresh key ONLY when the key is absent
  everywhere (genuine first boot). This stops the churn permanently — a `/data` reset recovers the same
  key, so DB passwords stay valid and at-rest secrets stay decryptable. Does not widen SEC-08 (the key
  is already on `/share` by design, Phase-1a); the Fernet-key-leaves-`/share` hardening remains the
  separate WR-PS-088 1b step.

### Added
- `tests/test_master_key_durable.py` — 4 tests (R192): a `/data` reset recovers the SAME key (not
  re-minted); local `/data` wins when present; a genuine first boot (nothing anywhere) mints; the key is
  stable across repeated resets. Negative control: the old mint-on-absent behaviour fails the recovery
  tests.

### Companion mitigation (already shipped this session)
- The self-healing DB pool (all 11 addon pools) recovers an addon's DB auth on a key change without a
  restart — the safety net while boxes update to this durable-key fix.

## 2026.6.419 — Rotation self-heal for the app DB pool (incident 2026-07-09, Rule 106)

### Fixed
- **App DB pool self-heals across a box-key rotation.** When Core rotates the box key (`db_role.key`,
  WR-PS-088 / ADR-013), the app DB password changes; a long-running pool holds the old one, so the next
  fresh connection fails auth and the add-on breaks until a manual restart — which a grower can't do.
  `_acquire_conn` now treats a `password authentication failed` on the app pool as a stale key: drops
  the pool, rebuilds it (re-reading `/share/paddisense/db_role.key`), and retries once; a second
  failure propagates. Never applies to the admin/superuser pool (R173 intact). Fleet-wide fix
  originating from the live PWM incident. `tests/test_pool_selfheal.py`.

## 2026.6.418 — Hone SEC-04/SEC-09 (Option B): Core pushes module-access grants to add-ons

### Added
- **`core/access_push.py` — Core propagates the module-access grant set to add-ons.** Core owns
  `module_access` but fails closed against sibling calls, so add-ons can't pull; Core PUSHES the grant
  (`build_grant_payload` → each started add-on's `POST /api/access/sync`) and the add-on enforces
  locally (Farm reference: `paddisense_farm/core/module_gate.py`, v2026.6.69). Best-effort: a down
  add-on is skipped and self-heals on the next push, never blocking the caller (Rule 127).
- **Pushed on change + periodically.** `api/access.py` calls `push_all_safe()` after every grant
  upsert/delete so enforcement updates immediately; the heartbeat loop re-pushes each cycle so a
  newly-installed or briefly-unreachable add-on converges to the current grant.

### Tests
- `tests/test_access_push.py` — 3 tests (R192): the payload shape the add-on gate consumes (malformed
  rows dropped), the push targets every started add-on's sync endpoint, and a down add-on is skipped
  without raising.

### End-to-end status (SEC-04/SEC-09 Option B)
- Core (push) + Farm (receive + enforce) now close the loop for Farm: a user Core never granted Farm
  is refused when they open Farm's ingress URL. **Owed:** propagate the `module_gate` to the other
  nine add-ons (shared-auth pattern) — WR to file; push-authenticity signature — WR-PS-108.

## 2026.6.417 — Hone PS-LIC-02 (Core sender side): asymmetric box-identity heartbeat signature

### Added
- **`core/box_identity.py` — per-box Ed25519 keypair (PS-LIC-02, the one open Critical).** The fleet
  heartbeat was authenticated only by a per-`server_id` SYMMETRIC HMAC the box holds, so a compromised
  box could sign a false self-report (the report demonstrated a falsified version accepted live). Each
  box now has its own Ed25519 private key (`/data/keys/box_identity.key`, 0600, generated once, stable
  across restarts); its identity IS its public key (no `/etc/machine-id`, which is absent in the addon
  container). Fail-soft: a key-load/sign failure returns None, never raises into the heartbeat path.
- **`core/heartbeat.py::_sign_envelope` now ADDS an Ed25519 signature over the same signed base**, plus
  the box public key + fingerprint, alongside the existing HMAC. Transition-tolerant: the HMAC stays so
  the GSM receiver keeps verifying today; the receiver adds Ed25519 verification (pinning the box key at
  first sight under the still-valid HMAC), then the fleet flips and the box-held symmetric secret is
  retired.
- Tests: `tests/test_box_identity.py` (5) + `tests/test_heartbeat_box_identity.py` (3) — real keypair,
  sign/verify, stability across restart, 0600 perms, fail-soft, tampered-body rejection, HMAC still valid.

### Honest scope (PS-LIC-02 is multi-Claude — this is the Core SENDER half only)
- Asymmetric signing alone does NOT meet the full acceptance ("a key extracted from a box cannot assert
  a false version") — the box legitimately holds its own key. The other half is **server-side: GSM must
  verify the self-reported version against what was actually deployed** (today `ps_version` is stored
  verbatim, no cross-check). Receiver + version-verify = G-Claude (GSM); the signed-heartbeat-request
  envelope + per-box public-key enrolment = A-Claude (contract). Design + coordination: WR-PS-105 (G) +
  WR-PS-106 (A). This commit is safe and non-breaking on its own.

## 2026.6.416 — Hone PS-SEC-11 Step 1 (Peter-approved): restore upload accepts only authenticated backups

### Fixed
- **`POST /admin/restore-upload` accepted plaintext `.sql` / `.sql.gz` / `.tar.gz` (Hone PS-SEC-11).**
  An uploaded backup is fed to `psql`/`tar` under the `postgres` superuser, so a crafted plaintext
  backup can carry `COPY … FROM PROGRAM` (RCE on the box hosting every grower DB) or hostile tar
  paths. The upload surface now accepts ONLY `.sql.gz.enc` and `-files.tar.gz.enc` — Fernet
  (AES + HMAC) artifacts that `backup_decrypt` verifies before a byte reaches psql/tar. New
  `_is_authenticated_backup()` gate; a plaintext upload returns 400 pointing the operator at the
  on-box path. **Plaintext restore stays available** via `/admin/restore` for a file an operator has
  deliberately placed in `/config/backups/` (not an upload) — disaster recovery is unaffected.
  Peter-approved 2026-07-09 ("yes, lock down the DB"). This is Step 1; the least-privilege half
  (restore under a per-DB owner role instead of the superuser) folds into ADR-013 — WR-PS-097.

### Added
- `tests/test_restore_upload_authenticated.py` — 8 behavioural tests (Rule 192): every plaintext
  format (incl. a hand-crafted `evil.sql`) is rejected 400; both `.enc` formats pass the guard; the
  `_is_authenticated_backup` predicate is pinned.

## 2026.6.415 — Hone PS-SEC-28: prove the durable replay guard survives a restart

### Added (test-only — no production code changed)
- `tests/test_licence_state.py::TestReplayAcrossRestart` — 2 behavioural tests (Rule 192) for the
  SEC-28 scenario the `_accept_issued_at` high-water mark was built for but had never been exercised
  end to end: apply a newer verified revoke (advancing the durable per-`licence_id` `issued_at`
  mark in the `config` table) → model a process **restart** (clear the in-memory nonce set + cached
  state, keep the DB) → replay an OLDER captured signed-ACTIVE licence. The cleared in-memory nonce
  store would accept the replay and flip REVOKED→ACTIVE; the durable mark must reject it. A positive
  control proves a genuinely newer artifact still reactivates (the guard is monotonic, not a blanket
  post-restart block). Negative control verified: neutering `_accept_issued_at` flips the site back
  to ACTIVE and the test goes red.

### Context — SEC-28 status
- `licence_verify`'s nonce store is process-memory only (resets on restart); the durable defence is
  the config-table `issued_at` high-water mark (`_accept_issued_at`, added earlier), now proven here.
- The shared `licence_verify.py` nonce store is DB-free by design and contract-frozen
  (SIGNED_LICENCE_CONTRACT §9-A) — making it durable is a steward change, filed low-priority. The
  Farm HMAC receive paths already use a durable DB nonce (`gsm_seen_nonces`, 1 h retention over a
  5 min window), so they are unaffected.

## 2026.6.414 — Hone PS-SEC-18: at-rest decrypt now fails CLOSED

### Fixed
- **`core/crypto.py::decrypt()` passed ciphertext through on decrypt failure (Hone PS-SEC-18).**
  An `enc:`-prefixed value that would not decrypt — wrong/rotated master key, corruption,
  tampering — was caught by a bare `except Exception` and **returned to the caller as the
  ciphertext** (`"enc:gAAAA…"`) with only a `log.warning`. Callers in `licence/db.py` then used
  that string as the GSM shared secret / licence secret: it flows into HMAC inputs and logs. A
  key mismatch silently degraded "encrypted at rest" into "secret material handed out in the
  clear". `decrypt()` now returns `""` so the caller degrades as if no credential exists
  (Rule 127/141), logs at ERROR, never logs the ciphertext (Rule 88/164), and never raises into
  a request path (Rules 121/141). Legacy non-`enc:` plaintext still passes through unchanged.
- Narrowed `except Exception` to `(InvalidToken, ValueError, TypeError)` (Rule 62). `InvalidToken`
  is lazy-imported to preserve the module's deferred `cryptography` import.

### Added
- `tests/test_crypto_fail_closed.py` — 6 behavioural tests (Rule 192) against a real Fernet key:
  round-trip, legacy plaintext, tampered token, wrong key, garbage `enc:` value, and a pin that
  `backup_decrypt()` stays fail-closed (raises `InvalidToken`). Negative-control verified: the
  old `return value` turns three of them red.
- Test fixture redirects **both** `_KEY_FILE` and `_BACKUP_KEY_FILE` to `tmp_path`. Patching
  `_KEY_DIR` alone is not enough — `_BACKUP_KEY_FILE` is an absolute path resolved at import, so
  `backup_encrypt()` in a test generated a real `/data/keys/backup.key` on the box running the
  suite. Caught during this change.


## 2026.6.413

Changed (WR-PS-088/089 — reconcile Core rotation against G's proven GSM version; Rule 101)
- Replaced the first-cut db_fleet_rotation.py (which wrongly matched self/GSM/Admin via a
  "paddisense" substring) with a thin adapter over the CANONICAL SHARED ENGINE vendored at
  core/_fleet_rotation_engine.py (byte-identical to documentation/shared/db_fleet_rotation.py). The
  engine is G's live-validated GSM logic generalised: churn-safe suffix->slug resolution, TimescaleDB
  init_commands persistence, wait-started polling, full-body option writes, never-log-password. Self
  excluded by construction (Core not in the sibling suffix list) — fixes the self-restart bug.
- Core-specific: supervisor httpx get/post + option reads + Core's OWN self-rotate
  (_rotate_self_last): after siblings rotate, Core sets its own db_password + restarts LAST;
  idempotent/no-loop (hook runs before Core's pool is used; skips when already NEW).
- 8 tests (engine branches + self-rotate idempotency). Still gated/dormant. GSM to vendor the same
  shared engine (WR-PS-088); A-steward curates documentation/shared.


## 2026.6.412

Added (WR-PS-088/089 — grower-box DB rotation field, Peter 2026-07-06)
- core/db_fleet_rotation.py: a gated fleet DB-superuser rotation, the grower-box mirror of GSM's
  db_fleet_rotation.py (Rule 101, identical state machine). New Core option
  postgres_superuser_password (+ _old trigger) = the single field to rotate the shared TimescaleDB
  postgres password across every managed addon: PATCH each addon's db_password option + restart.
  State machine: cluster-on-new -> propagate / cluster-on-old + old-set -> rotate then propagate /
  both-fail -> CRITICAL (never crashes Core). Wired into startup, safe-hook wrapped, no-op unless
  the field is set. Never logs password bytes. 6 state-machine unit tests.
- BUILT + gated but NOT triggered live: reconcile the shared shape with GSM's copy (promote one to
  documentation/shared/) before a coordinated fleet rotation. Handles the postgres SUPERUSER only;
  per-addon *_app stored passwords are WR-PS-088 Phase-2.


## 2026.6.411

Fixed (WR-PS-088 incident 2026-07-06)
- publish_box_db_key_to_share() is now PURELY ADDITIVE — it writes both /share db_role.key and the
  legacy master.key and NEVER auto-removes master.key. The v410 logic removed master.key whenever a
  db_role.key existed on Core, which stranded not-yet-updated addon pools (they lost the shared key
  on reconnect). Retiring master.key from /share is now a deliberate 1b-only step. Added a startup
  diagnostic logging whether a distinct db_role.key is in play.


## 2026.6.410

Security (WR-PS-088 Phase-1a — /share master-key split; Core red-team HIGH)
- Split the DB-role-derivation key from the Fernet at-rest key: new crypto.get_db_role_key_bytes()
  reads a dedicated /data/keys/db_role.key, falling back to the master key while none exists
  (ADDITIVE — derived passwords unchanged, no addon lockout). _roles.py derives *_app passwords from it.
- publish_box_db_key_to_share() publishes /share/paddisense/db_role.key (canonical) alongside the
  legacy master.key during rollout; once a DISTINCT db_role.key exists (the 1b flip) the master.key
  copy is removed so the Fernet at-rest key never sits on /share.
- Regression: tests/test_ps088_db_role_key.py (fallback invariant + distinct-key use).
- Remaining (WR-PS-088): addon _pool.py propagation (prefer db_role.key) + the coordinated 1b flip.


## 2026.6.409

Security (red-team audit 2026-07-05 — Core-local findings; the substrate licence authority)
- Session cookie scoped to the addon ingress base path (was path="/") — stops cross-addon cookie leak under HA ingress (MEDIUM).
- Login: constant-time dummy-hash on the no-user branch — closes the username-enumeration timing oracle (R190).
- Ingress trust fails CLOSED when infra DNS is unresolved — dropped the /23 legacy fallback that let a co-hosted sibling forge ingress identity during a DNS blip.
- /api/my-location no longer falls back to person.admin (cross-principal location disclosure).
- /api/device-prefs is owner-scoped (owner_user_id) — closes the IDOR.
- Connection-code: removed the forgeable self-signed HMAC (keyed on the code's own secret); Ed25519 verify-when-present active, hard-enforce behind PS_LICENCE_ENFORCE_SIG pending the Admin-signing cutover (R141).
- Licence replay: durable per-licence_id issued_at high-water mark defeats a captured signed-ACTIVE licence flipping REVOKED->ACTIVE across restart.
- _validate_url SSRF guard rewritten: http/https only, resolves the host + blocks internal targets (loopback/metadata/RFC1918/ULA) except the Supervisor /23, bounded DNS timeout, fail-closed.
- Backup: run_restore_test() (R174) + backup-key escrow (inert until PS_BACKUP_KEY_PASSPHRASE set) + docs/DATA_RETENTION.md (R196).
- Deferred to the fleet data-tier plan: restore-as-non-superuser role (LOW) and the /share master-key split (HIGH, fleet-wide).


## 2026.6.408 — Security-test enforcement: real SSRF protection test

### Security
- Added a genuine behavioural test for the built-in SSRF guard that protects the licence
  connection-code URLs (the heartbeat / webhook / install addresses supplied when you connect
  Core to the licence server). The test proves Core refuses to call cloud-metadata, loopback
  and private-network addresses while still allowing your real licence host — so a tampered
  connection code cannot make Core reach into internal services.
- Verified the automated test database rebuilds cleanly from scratch (drop and recreate), so
  the full safety-check suite (179 checks) stays green and can block a bad release.

No functional change to Core itself — this release strengthens the automated safety net only.


### Compliance / process
- **Re-audited against Golden Rules v2.49** (was v2.48). `golden_rules_version` bumped in
  CLAUDE.md + docs/AUDIT.md; `last_audit_date` 2026-07-04, cadence 14 days.
- **Category-A rule landing (WR-PS-085 / Wave-4a):** Core now carries the body + Verify line
  for R21, R23–R29 in its own CLAUDE.md "Critical Rules" section (they were relocated out of
  GOLDEN_RULES.md to the owning addon). Each is re-verified against Core's *current* code:
  R28 is genuinely met (no `bay` concept); R21/R23/R24/R25/R26/R27/R29 are **N/A** in Core —
  the spatial layer (paddocks/boundary/source-hierarchy/matching/CNH-JD sync) was extracted to
  the GIS addon in v353, so Core has no `paddocks` table, `boundary`/`gsm_boundary` columns,
  `SOURCE_PRIORITY`, or `SPATIAL_MATCH_THRESHOLD`.
- **Real gap found (audit honesty):** the prior audit's rows marking R23/R24 "✓ paddocks has
  boundary JSONB" were **stale** — carried across the v353 extraction. Corrected to N/A with
  grep evidence.

### Fleet consistency (ADR-011 / R79 / R134)
- Renamed the pool-close entrypoint to the fleet-canonical `close_pools()` (a backward-compat
  `close_pool` alias is retained); the shutdown handler now calls `close_pools()`.
- `db/__init__.py` `__all__` now exports `init_app_pool` and `close_pools`.

### Security tests (REQUIRED_SECURITY_TESTS manifest → full applicable coverage)
- New `tests/test_security_regression.py` adds behavioural tests for the rules Core is the
  applicable receiver/owner for: **R187** (X-Forwarded-For never trusted for client identity),
  **R188** (a credential change revokes every live session), **R153/R154** (a non-admin is
  refused 403 on another principal's caller-supplied user object), **R190** (unknown user and
  wrong password return the same error — no enumeration). R146 (CSV export) and R189 (user
  email throttle) are documented N/A — Core has neither surface.

### Grower-facing (plain English)
- This is an internal quality and safety hardening release for the PaddiSense Core system
  service that runs on your box. Nothing changes in what you see or do. Under the hood we
  tightened the automated safety checks, added more security tests, and refreshed the internal
  compliance record. Your licence, backups, and box health monitoring keep working exactly as
  before.

## 2026.6.406 — SEC-08/R173: fail-closed DB app pool (Phase-2, WR-PS-081)

### Security
- **The request-path DB pool is now fail-closed (R173/SEC-08).** `_pool.py` no longer falls back to
  the `postgres` superuser if the `paddicore_app` app pool can't initialise — `get_cursor()` returns the
  least-priv app pool or raises. Migrations/DDL still use the admin pool during the startup window
  (before `init_app_pool()` is called). Converges the fleet to Farm's fail-closed posture; a future
  key/role failure now fails loudly instead of silently promoting request-path queries to superuser.
  (`/share` persists, so an established box that reboots keeps its key and does not fail-closed.)

## 2026.6.405 — SEC-08/R173: publish the box DB-role key to /share (WR-PS-081)

### Security
- **Core now publishes its box master key to `/share/paddisense/master.key`** at startup
  (`crypto.publish_box_db_key_to_share()`), so every addon derives the **same** `*_app` DB-role
  password Core mints its roles with. Root cause (WR-PS-081): the per-addon-container
  `/data/keys/master.key` differs from Core's, so each addon's `*_app` login failed and the pool
  **silently fell back to the `postgres` superuser** — the R173/SEC-08 least-priv split was a facade
  for every addon except Farm. Runtime boot logs confirmed PWM/Store running `role=postgres`.
  Fernet-at-rest is untouched (keeps the local `/data` key — a separate path), so no encrypted data
  is re-keyed. Addons read the shared key next; Phase 2 fail-closes the pool once all on their app role.

## 2026.6.404 — RBAC: 3 roles + access management is admin-only

Two grower-driven RBAC changes (Peter, 2026-07-02):

### Access management is now admin-only
`/api/access`, `/api/users`, and the `/access` (UA01) page are **admin-only** (were manager+). This
closes a real gap: a **manager could re-grant module access, including to themselves** — e.g. an admin
removing Planner from a manager didn't stick, because the manager could add it back. Now only an admin
assigns modules/roles/users. New `tests/test_access_admin_only.py` proves a manager is blocked from
viewing and re-granting access; admin still allowed.

### Role ladder reduced 5 → 3
Removed the unused `viewer` and `supervisor` tiers. The model is now **operator < manager < admin**:
- **operator** — base; sees its assigned modules.
- **manager** — + operational/system (backups, metrics, addon updates via `/api/admin`); **no** access
  management, **no** restore.
- **admin** — everything: access management (UA01), restore, licence.

Migration `role_3tier_remap` remaps any existing rows (`viewer`→`operator`, `supervisor`→`manager`) in
`ps_users` and `module_access`; UA01 role dropdown, schema/table defaults, and docstrings updated to match.

## 2026.6.403 — UA01: show owner break-glass password status

The Owner card now states clearly whether a custom owner (break-glass) password has been set:
- 🟢 "✓ A custom owner password has been set." once changed off the default.
- 🟠 "Still on the default password — set a custom one below." while unchanged.
(Model A retained — owner seeds from the box `db_password`; the grower sets a custom one on install.)

## 2026.6.402 — UA01 layout: collapsible sections + entries-first

UX polish on the User Access page (desktop + mobile), per grower review:
- **Current access entries** moved **above** the add form — the list is the focus.
- **Assign module access** is now a **collapsible section, collapsed by default** (clicking Edit on an
  entry re-opens it and scrolls to it).
- **Owner card** auto-collapses once a non-seeded owner password is set (`must_change_password` false);
  stays open while the seeded password still needs changing.
- Reuses the shared `toggleSection` collapsible convention (chevron + `ps-hidden`).

## 2026.6.401 — Pre-release security re-audit: close all findings + SEC-07 rate-limit + dead-code sweep

Full 4-agent adversarial re-audit at v400/401 (Rule 105) ahead of a grower release. All findings closed;
Hone review confirms **0 release-blocking Hone actions owed for Core**. Golden Rules re-baselined v2.46→v2.47.

### Security — findings closed
- **Owner/session auth:** `must_change_password` is now **enforced in middleware** (a seeded/weak account
  can reach only the change-password flow until it's changed), and any password change/reset **invalidates
  that user's live sessions** (Rule 188) — a stolen cookie can't outlive the credential. Session store now
  reaped/bounded.
- **RT-10:** `/gsm/api/status` no longer returns `heartbeat_url` (a cloudhook token was reachable by any
  authenticated user, incl. viewer).
- **Rule 133 / SSRF:** the Core→addon licence proxy now validates the caller-supplied `slug` against
  `KNOWN_ADDONS` + charset before it reaches the Supervisor API.
- **module_access:** outrank guard on `upsert`/`delete` (a manager can't tamper with an admin's entry);
  a **SETUP MODE banner** now warns while the empty-admin bootstrap window is open (UA01 desktop+mobile).
- **SEC-07 inbound:** the per-source rate-limit (`lockout.check_rate_limit`/`record_request`, built under
  WR-PS-043 but previously unwired) is now **wired into the connection-code enrolment path** — completes
  Core's inbound hardening alongside the Ed25519 nonce replay-guard.
- **Hardening:** bounded the login/sensitive rate-limit dicts (RT-9); require a declared length so a chunked
  body can't bypass `MAX_BODY_SIZE` (RT-6); uvicorn loggers now pass through the secret redactor (F6);
  enforce `0600` on pre-existing key files.

### Removed — dead-code sweep (~270 LOC, v353 GIS/Farm/GSM extraction remnants)
- Orphan modules `core/error_tracker.py`, `core/perf_tracker.py`, `core/text.py`.
- Dead functions/constants: `helpers.get_ha_state`, `auth._INGRESS_SESSION`, `audit.get_recent_errors`,
  `licence_verify.reload_pubkeys`, `users.get_user`, `provider_health._KNOWN_PROVIDERS`,
  `constants.MODE_COOKIE_MAX_AGE`, `backup.RETENTION_DAYS`, the GSM-webhook HMAC vestiges
  (`_verify_hmac`/`_sign_request` + `HMAC_ALGORITHM`/`TIMESTAMP_DRIFT_SECONDS` + dead `import time`).
- Stale docs: dropped the `seasons_unique_name` "known issue" (migration no longer exists); fixed CLAUDE.md
  rules version.
- **Kept deliberately:** `crypto.rotate_key`/`is_encrypted` (wanted for ADR-013 rotation).

### Tests
- New: `test_licence_hardening`, `test_module_access_hardening`, `test_lockout_rate_limit`,
  owner/session-invalidation + must-change-gate cases. ruff + mypy clean (39 files, down from 42); vulture clean.

## 2026.6.400 — Backups: prune orphan DB dumps + group the DB01 list by addon

Confirmed all 11 addon DBs are backed up daily; these fix the DB01 UI clutter (stale + legacy files
showing as duplicates / making per-addon backups hard to see).

### Fixed
- **Orphan backup pruning** (`core/backup.py`): the daily prune now removes DB dumps that no longer
  belong to a current addon — stale renames (`paddisense-gis`, pre GIS→Farm), non-standard legacy dumps
  (`paddisense_asmpro_*`), and pre-Postgres `.db` exports (`*_for_prod.db`, `paddisense_daily_*.db`). The
  previous prune (2-per-DB) left these forever because their names don't map to a current DB. **Safe:** a
  current-format backup always resolves to a valid group, so live addon backups are never touched — proven
  by `tests/test_backup_orphan_prune.py` (asserts every current backup + old mapped dumps survive). File
  archives (`.tar.gz.enc`) are left to the retention prune.

### Changed
- **DB01 backup list grouped by addon** (desktop + mobile): each addon gets a header with its backups
  beneath (legacy/other sorted last), so it's obvious every addon has a current backup.

### Notes
- The existing stale/legacy files are swept on the **next daily backup run** (per Peter — no manual delete).

## 2026.6.399 — Fix Seed Manager addon key (`paddisense-seed-manager`)

Seed Manager showed as "not installed" and its signed-licence distribution was misrouted because Core
used the wrong key `rrapl-seed-manager`; the installed addon slug is `paddisense-seed-manager`.

### Fixed
- Corrected the key in all 6 references: `KNOWN_ADDONS` + default-port map (`licence/routes.py`),
  `licence_state.PRODUCT_SLUG` (SEC-04 signed distribution), heartbeat addon list + ports
  (`heartbeat.py`), and the admin metrics addon list (`admin.py`). `slug.endswith(key)` now matches the
  installed `…_paddisense-seed-manager` → shows installed, and signed artifacts route correctly.
- Migration `module_access_seed_manager_key_rename`: rewrites the old key inside any existing
  `module_access` grants so assignments keep pointing at the addon.
- 3 tests (`test_addon_keys.py`); suite green, ruff + mypy clean.

## 2026.6.398 — RBAC Part 2: HA-ingress authority from the access table, not blanket admin (WR-PS-068, SEC-04/05)

The lockdown that makes the whole RBAC meaningful: opening Core via the HA sidebar no longer auto-grants
admin. **Network is no longer identity** (Hone SEC-04/SEC-05 applied to Core's own admin surface).

### Changed
- `require_auth()`: an HA-ingress user's **authority** now comes from their `module_access` entry
  (`ingress_session`/`ingress_role`): **no admin configured yet → admin (setup mode)** so an admin can
  always be established; a granted user gets **their entry role** (admin if all-access); everyone else is
  a **viewer** (reaches Core, but `/access`, `/api/access`, `/api/users`, DB/metrics are manager+ gated →
  bounced/403). Replaces the old static admin `_INGRESS_SESSION` grant.
- **Safety net:** the seeded local `owner` login always keeps its real role (break-glass) — a cookie
  session, unaffected by this — so the box can't be locked out. Last **admin-authority** `module_access`
  entry is now guarded against delete/demote (can't drop to zero admins via the UI).

### Notes
- 10 new tests (`test_ingress_authority.py`) — role derivation, last-admin guard, `require_auth` over a real
  ingress request. **144 pass**, ruff + mypy clean. Trusted-IP check unchanged (Rule 172); non-ingress
  cookie sessions unchanged.

## 2026.6.397 — RBAC: Owner card on the User Access page (WR-PS-068)

### Added
- **Owner card** pinned at the top of UA01 (desktop + mobile): shows the seeded `owner` login (the
  break-glass admin you sign in with to manage HA-user access), warns while it's still on the seeded
  password, and lets an admin set a new owner password inline (`POST /api/users/{id}/reset-password`).
  On a fresh box it's the only thing on the page — sign in as owner, then add HA users below.
- `core/users.py`: `must_change_password` added to the users API projection so the card can show the
  "still using the seeded password" nudge (hash still never leaves the API).

### Notes
- No model change — HA-user `module_access` (who sees which modules) is unchanged; the Owner card is the
  login/fallback layer on top. 1 new test; **134 pass**, ruff + mypy clean, orphan-bindings green.

## 2026.6.396 — RBAC: seeded break-glass owner + self-service password change (WR-PS-068)

Owner bootstrap (Peter's design, Option A): guarantees there is always a known way into a production
box that does not depend on HA ingress or the access table — the safety net that lets the ingress
authority be locked down (Q2, next).

### Added
- `ensure_owner()` (startup, seed-once) — a local `owner` account (role admin) seeded with the **box DB
  password**, flagged `must_change_password`. Deterministic per-box recovery credential; never overwrites
  a password the owner later changes.
- **Self-service password change** — `/change-password` page (CP01, desktop + mobile) + `POST
  /api/change-password` (verifies the current password, clears the must-change flag). `core/users.py
  change_own_password()`. Login **redirects to `/change-password`** when the account still carries the
  seeded secret. Licence-gate-exempt so the owner can change it before enrolment.
- Migration `ps_users.must_change_password`; the flag rides in the session.

### Security note
- The seeded owner is **break-glass**: the DB password defaults to the well-known `homeassistant` and is
  grower-readable until rotated (ADR-013), hence the forced change-prompt. Admin-reset (`reset_password`)
  also clears the flag. 7 new tests; **133 pass**, ruff + mypy clean.

## 2026.6.395 — RBAC UI: grey module checkboxes for admin/all-access entries (UX)

### Changed
- User-access page (UA01, desktop + mobile): the module checkboxes now **grey out + clear** when the
  selected **role is `admin`** — not just when "All modules" is ticked — because an admin entry sees every
  module regardless (`effective_modules` short-circuits admin → all). Shared `_uaSyncModules()` helper wired
  into role-change, all-access toggle, edit, and reset; adds a hint line ("Admin / all-access entries see
  every module — individual modules do not apply"). Stops the confusing admin-role + specific-modules
  contradiction at the source (surfaced testing v394: an admin entry with 7 modules ticked still saw all).
- No behavioural/API change — verify-commit green (orphan-bindings resolves the new `onRoleChange`), 126 pass.

## 2026.6.394 — RBAC: user-access admin page (UA01, WR-PS-068 UI)

### Added
- `/access` page (**UA01**, manager+; non-managers redirect to the hub) — desktop + mobile templates
  (`pages/desktop/access.html`, `pages/mobile/access.html`). Pick a Home Assistant user (or enter an id),
  set role, toggle **All modules (owner/admin)**, and tick the modules they may see; table of existing
  entries with edit/delete. Consumes the v392/v393 APIs (`/api/ha-users`, `/api/modules`, `/api/access`).
- Sidebar nav entry "User Access" under **System** (role-gated to admin/manager).
- Built to the Template Guide: nonce-CSP scripts, delegated `data-act` dispatcher (zero inline handlers,
  orphan-bindings gate green), `var(--ps-*)` tokens only (no hex, no inline styles), desktop/mobile split.

### Notes
- 2 page tests (render for admin; redirect for viewer); **126 tests pass**, ruff + mypy clean, verify-commit
  green. ⚠ **Needs a browser smoke at the box** before grower release (v377 CSP history) — deployed to dev for that.

## 2026.6.393 — RBAC role→feature: per-HA-user module access (WR-PS-068)

Owner-directed model (Peter, 2026-07-02): **Owner/Admin see all modules; other HA users get only the
modules assigned to them.** Identity = HA ingress user; authorisation = an explicit per-user grant.

### Added
- Vendored `core/ha_identity.py` (canonical `shared/ha_identity.py`, WR-PS-063) — resolves the current
  HA user from ingress headers + lists HA persons.
- `core/module_access.py` — the authz model over a new `module_access` table (`ha_user_id → {role,
  modules[], all_access}`). `effective_modules()` returns all-access for owner/admin/all_access **and for
  an unconfigured box** (no lockout before setup); a granted HA user is restricted to their modules —
  **even though Core hands ingress an admin session** (the entry governs, which is what makes the filter
  bite). Guards: no privilege escalation, admin-only `all_access` grant, module keys validated.
- `api/access.py` — `/api/ha-users`, `/api/modules`, `/api/access` (list) + `/api/access/{ha_user_id}`
  (PUT/DELETE), all manager+ gated + audited. Pydantic `AccessEntryRequest`.
- Migration `module_access_table`.

### Changed
- `/gsm/api/addon-discovery` now filters the addon list to the caller's permitted modules (owner/admin =
  all). Side benefit: narrows red-team **RT-4** (a viewer can no longer enumerate every addon).

### Notes
- 16 new tests (`test_module_access.py`); **124 tests pass**, ruff + mypy clean. Backend + filtering only;
  the assignment **UI is deferred to a box session** (browser smoke). Complements the v392 local-account RBAC.

## 2026.6.392 — RBAC: farm user-management backend (WR-PS-068 folded feature)

### Added
- `core/users.py` — user-management service over `ps_users` with the guards a naive CRUD misses:
  **no privilege escalation** (an actor can't grant a role above their own, nor edit a user who
  outranks them), **no self-lockout** (can't deactivate/demote yourself), **no last-admin lockout**
  (the final active admin can't be deactivated or demoted). Password policy + unique-username checks.
- `api/users.py` — `/api/users` (+ `/api/v1/users`) endpoints: list / create / update (role+display) /
  activate-deactivate / reset-password. **Manager+ gated**, thin ingress delegating to the service,
  every mutation audited. Pydantic request models (Rule 125). No password hash ever leaves the API.
- `tests/test_users_rbac.py` — 18 tests: service guards (escalation, self/last-admin lockout,
  outranking, dup, password policy) + API happy-path + manager-role gating (viewer → 403).
- **108 tests pass** (was 90), ruff + mypy clean. Backend only — UI + role→feature filtering follow.

## 2026.6.391 — SEC-08: least-priv read metrics (Rule 148) + document DB-privilege posture (Hone PS-SEC-08)

### Changed
- `api/admin.py` `_collect_db_metrics()`: read-only counts (`information_schema`, `pg_stat_activity`,
  `ps_users`) now run on the **least-privilege `paddicore_app` pool**, not the `postgres` superuser pool
  (Rule 148 ⚠ → ✓). Verified on the live dev DB — the request role can read all three. Reserves the
  superuser pool for DDL/backup only.

### Notes (Hone PS-SEC-08 — Core position, no code change)
- **Request path is already least-priv** (`paddicore_app` DML-only, R173) — done.
- **Core's admin/DDL pool legitimately needs elevated privileges**: Core is the fleet DB bootstrapper —
  `CREATE DATABASE` (every addon's DB), `CREATE ROLE` (all 11 addon roles), and `pg_dump` of *all* DBs.
  GSM's "drop to a non-superuser owner" pattern does not transfer to the bootstrapper.
- **The closeable residual — rotating the `postgres` superuser password off the `homeassistant` default —
  is FLEET-BLOCKED** (WR-PS-037): the superuser is shared by every addon, so rotation is a coordinated
  Peter/A flip once each addon carries its own credential, not a Core-solo change.
- 90 tests pass, ruff + mypy clean.

## 2026.6.390 — PLAT-06: remove leftover code + document /api/v1 versioning stance (Hone PS-PLAT-06)

### Removed
- `paddicore/PENDING_NAV_ITEMS.md` — dead pre-split scaffold referencing planning/analytics/kb
  routers extracted to the GIS addon in v353 (referenced nowhere).
- Unused `APIRouter(prefix="/api")` aggregation in `api/__init__.py` — a dead duplicate of main.py's
  direct router mounting (Rule 59/101). `api/` is now a namespace marker only.

### Changed
- `paddicore/__init__.py` docstring: "spatial farm management, machine data, HFM, weather" (stale
  since the v353 gateway refactor) → the actual gateway responsibilities.
- **Documented the `/api/v1` interface-versioning stance** (Hone PS-PLAT-06 "same term means different
  things"): `/api/v1/*` is a STABLE ALIAS of the current `/api/*` interface (same handlers), not an
  independent version; `/api/v2/*` is reserved for a genuine breaking change with a deprecation window
  (single-prefix convention, fleet-aligned with GSM's INTERFACE_VERSIONING.md). Documented in
  `main.py` + CLAUDE.md; the stale "v1 API router empty" Known-Issue corrected.
- No behavioural change: 90 tests pass, all 16 `/api/v1` aliases still resolve, ruff + mypy clean.

## 2026.6.389 — PLAT-04: harden the raw-JSON entry point + behavioural input-validation tests (Hone PS-PLAT-04)

### Fixed
- `api/admin.py` `/admin/restore` (the only raw-`request.json()` reader — all other JSON
  endpoints use Pydantic models): guard that the parsed body is a `dict` before
  `_validate_restore_request` calls `.get()` on it. A non-dict body (`[]`, `"x"`, `42`) previously
  raised `AttributeError` → **500**; now returns a clean **400**. Acting on unchecked input shape
  is exactly the "thin validation" Hone PS-PLAT-04 flags.

### Added
- `tests/test_input_validation.py` (13 tests) — behavioural assertions that malformed input is
  *rejected*, never silently accepted or 500'd: Pydantic endpoints (`device-prefs`, `bugreport`,
  `enroll-core`, `addon-licence`) return a sanitised **422** on missing/empty/over-length fields
  (+ the Rule 147 envelope shape); `/admin/restore` returns **400** on non-dict / missing-confirm.
- **90 tests pass** (was 77), ruff + mypy clean. Documents Core's entry-point validation coverage
  for PS-PLAT-04 (Core = gateway; no irrigation/safety control paths).

## 2026.6.388 — PLAT-07 / WR-PS-046: licence-gate redirect carries the ingress prefix

### Fixed
- `main.py` `licence_gate`: the unlicensed-redirect built its `/licence` target from
  `request.state.base_path`, but `licence_gate` is the **outer** middleware layer and runs
  **before** `auth_middleware` sets `base_path` — so the prefix was empty and the redirect
  went to a bare `/licence`. Under HA ingress that resolves outside the addon mount → **HA 404**,
  leaving an unlicensed box unable to reach the licence-entry page. Now derives the prefix from
  the `X-Ingress-Path` header directly (mirroring `auth_middleware`). Closes Hone **PS-PLAT-07**
  (2nd fault) + **WR-PS-046**; same root cause + fix as Safety v2026.6.25.
- Regression test `tests/test_licence_gate_ingress.py` (4 tests): asserts the ingress-prefixed
  redirect, trailing-slash normalisation, the off-ingress bare-`/licence` fallback, and that
  `/api/` paths still 403 (no HTML to a JSON client). **77 tests pass** (was 73).

## 2026.6.387 — SCAL-03: pin base image to digest-pinned Python 3.12 (Hone PS-SCAL-03)

### Changed
- `Dockerfile`: `FROM python:3.11-slim` → **`python:3.12-slim@sha256:423ed6ab…199fbf`** (digest-pinned
  multi-arch index; same index digest as the fleet, Admin v2026.7.11). Closes Hone **PS-SCAL-03**
  (HIGH/P1): Python 3.11 reaches end-of-support ~Oct 2027 (coincident with go-live) — 3.12 runs to
  Oct 2028, a full year of security-patch runway. The digest pin also removes the silent-rebuild drift
  Hone flagged (an unpinned tag can pull a different base on rebuild).
- `pyproject.toml`: `[tool.mypy] python_version` and `[tool.ruff] target-version` → **3.12 / py312**.
- No application code change — full suite green on 3.12 (73 tests pass, ruff + mypy clean), matching
  Admin's clean 3.12 migration. Trunk-based: first Core commit landed directly on `main` (ADR-012 pilot).

## 2026.6.386 — Onboard Core to the ADR-011 §5 startup-order gate (validate_config)

### Changed
- `main.py`: renamed `_validate_config()` → **`validate_config()`** (public, fleet-canonical name
  per FLEET_PROCESS.md §5 / ADR-011 §4.4). The new `check-startup-order.py` gate requires the public
  name; Core is the cited §5 reference impl, so it must carry it. Startup order unchanged
  (`validate_config` → `ensure_database` → `ensure_first_user` → PAT rotation → services).
- Onboards Core to both §4.4 gates: **§5 startup-order ✓** (`validate_config` defined + called from
  the startup handler) and **§6 test-isolation ✓** (conftest already forces `paddicore_test`, v384).
- Docs synced (Rule 96): CLAUDE.md + `docs/AUDIT.md` Rule-126 row use the new name.

## 2026.6.385 — Remove dead GSM boundary-sync UI (WR-PS-062 Core↔Farm split follow-through)

### Removed
- `pages/shared/gsm_content.html`: the "Pull Boundaries" button + "Select Paddocks to Push" panel
  and their JS (`pullBoundaries`, `syncBack`, `confirmSyncBack`, `syncSelectAll`, `closeSyncPanel`,
  `renderSyncResults`) + `.sync-*` CSS. All three backends they called (`/api/pull`,
  `/api/sync-back/paddocks`, `/api/sync-back`) were removed in the v353 spatial extraction, leaving
  reachable dead buttons (Rule 43) that 404'd. Boundary sync lives in the Farm/GIS addon now.
  Template 700 → 525 lines; 0 orphan bindings (verify-commit orphan-bindings check green).
- GSM **connect/disconnect** + licence enrolment + addon discovery are unchanged and intact.

### Fixed
- `schema.sql` + `core/db/_migrate.py` comments referenced a non-existent `drop_dead_farm_tables`
  migration; corrected to the actual name `drop_dead_legacy_tables` (Rule 96 — docs accurate).

## 2026.6.384 — Boundary-sync security snapshot for Admin fleet reporting (WR-PS-043)

### Added
- `core/lockout.py` + `core/provider_health.py` — per-source HMAC-failure lockout and
  per-provider outbound-failure tracking (adapted from Farm v.26, WR-PS-043).
- `extra.security` in the 5-min heartbeat envelope: `hmac_failures_24h`, `hmac_replays_24h`,
  `new_grower_ids_24h`, `locked_grower_ids`, `provider_failures_24h` — the WR-PS-042 contract
  Admin's boundary-sync dashboard aggregates. Without it Core boxes rendered blank.
- `GET /api/v1/security/snapshot` (admin-gated) returning the same contract — Admin renders
  Core alongside Farm.
- Heartbeat send now records provider health on `admin`; connection-code HMAC failures feed the
  lockout (keyed by grower_id; locked sources rejected 429).
- `tests/test_security_snapshot.py` — 11 DB-free module tests + endpoint auth/contract tests.

## 2026.6.383 — Security: public /api/licence liveness-only (R144)

### Fixed
- R144/WR-PS-066: public `GET /api/licence` no longer leaks the licence string or
  product on this unauthenticated, cross-addon-polled endpoint. It now returns
  liveness-only `{"enrolled": <bool>}`, matching the fleet convention (Farm/ASM).
  Licence detail remains available via the auth-gated `/gsm/api/status` route.
  No consumer reads the stripped fields from this endpoint (discovery, metrics,
  and detail views read `.enrolled` or query the DB directly).

## 2026.6.382 — Unblock grower release: pinned-mypy type errors

### Fixed
- CI release audit failed under the pinned **mypy 1.16.0** (local tools run 2.1.0 — version drift):
  2 unused `# type: ignore[no-redef]` + 3 missing-stub imports. Fixed with the portable
  `# type: ignore[no-redef, unused-ignore]` idiom (clean on both versions) and `types-requests` +
  `types-PyYAML` added to requirements. No runtime change.

## 2026.6.381
ADR-010 flip-readiness — cleared every verify-commit warning (dev bump; grower release stays v378).
### Changed
- R193.3/R195: removed 4 app.css classes that shadowed the master theme
  (`ps-text-info/success/warning/muted`) — templates resolve to the canonical master copies.
- R157: CSRF rejection aligned 415→403 (fleet convention; reject path only). Added behavioural
  CSRF test (`TestCsrf`, asserts 403).
- R17: re-synced `paddisense-tokens.css` byte-identical to master.
- R96/R118: CLAUDE.md → v2026.6.381 / golden_rules_version v2.42; AUDIT.md refreshed to v2.42.
### Notes
- Follow-ups (not flip-blockers): ~61 net-new `ps-*` utility classes in app.css → future `dash-*`
  migration / steward promotion (R195 textual); consider double-submit CSRF token for the bootstrap
  addon (R157 hardening). See `docs/AUDIT.md`.

## 2026.6.380
### Changed
- `run.sh` now sources the canonical master theme (`documentation/theme`) at startup (WR-PS-045/ADR-007 — completes Core's part of the grower-addon run.sh sweep; prod falls back to the bundled image copy).

## 2026.6.379
### Changed
- Re-synced theme tokens to the current master (R169 round-2 utility additions landed after the v378 sync). Additive, no visual change. `verify-commit` Rule 17 passes. Grower release remains v378 (this is a dev theme-alignment bump).

## 2026.6.378
### Changed
- Re-synced theme tokens to the master (Rule 17 / WR-PS-041) — Core's `paddisense-tokens.css` is now byte-identical to `documentation/theme`. `verify-commit` Rule 17 passes. Additive only, no visual regression.

## 2026.6.377
### Fixed
- **Licence page unusable — could not expand modules or enter connection codes.** The nonce CSP (`script-src 'self' 'nonce-…'`, no `unsafe-inline`, Rule 156) blocked every inline `onclick=`, so the `toggleSection`/`toggleAddon` expanders and all enroll/activate buttons in `gsm_content.html` were dead. Converted all 17 inline handlers to a single delegated `addEventListener` dispatcher via `data-act`/`data-arg` (Rule 178). Also fixed the sidebar hamburger + overlay in `desktop/base.html` (same CSP cause). Blocked new-box enrollment.

## 2026.6.376
### Security
- Rule 156: Nonce-based CSP — `script-src` no longer uses `unsafe-inline`. Per-request nonce generated in middleware, applied to all `<script>` tags
- Rule 147/166: Removed all `str(exc)` leaks from client responses — generic messages + server-side logging
- Rule 133: Consolidated all Supervisor API calls through single adapter (`core/helpers.py`)

### Fixed
- Rule 49: Mobile font sizes raised to 15px+ minimum, touch targets to 48px
- Rule 57: Added missing docstrings on 6 public functions
- Rule 58: Magic numbers extracted to named constants (port dict, sort sentinel, slice lengths)
- Rule 59: DRY — extracted `_elapsed_ms()` helper in selftest.py
- Rule 61: API envelope normalized to `{"ok": true}` / `{"error": "..."}` consistently
- Rule 32: Added `log_audit()` to restore_upload archive failure path
- Rule 46: Added `print-color-adjust: exact` to @media print
- Rule 100: Added mypy gate to CI workflow
- Rule 102: Mounted `/api/identity` router (was dead code)
- Rule 176: Created `docs/security/THREAT_MODEL.md` (attacker's playbook + coverage matrix)

## 2026.6.375
### Fixed
- Fix smoke tests for Starlette 1.3.x: Secure cookie requires HTTPS base_url in TestClient
- Fix mobile seeded-data test to assert version in hub HTML (display_name not rendered on hub page)

### Changed
- Full adversarial AUDIT.md rewrite: 176 rules at v2.17, 6-agent red-team sweep. 15 gaps identified, 4 acknowledged debt.

## 2026.6.374
### Security
- Rule 172: Ingress trust pinned to resolved Supervisor/HA IPs — no longer trusts broad /23 subnet. Sibling addon IP forgery now rejected. DNS-failure fallback preserves operator access.

## 2026.6.373
### Security
- WR-PS-033: CVE bump — starlette 1.3.1, python-multipart 0.0.31, cryptography 48.0.1, pytest 9.0.3 (0 vulns)
- WR-PS-033: Structural log-redaction — RedactingFormatter strips secrets from all log output incl. tracebacks
- WR-PS-033: Startup security posture logging
- Rule 167: SSRF guard uses ipaddress module (was string prefix)

### Changed
- WR-PS-032: Adopt master theme (1,413 lines) — SM standard. All pages migrated to ps-* classes
- All ss-* legacy classes removed from templates + app.css
- Canonical desktop/mobile base templates from /config/theme/
- Hub tiles: gw-* → ps-hub-* master classes
- Bugreport: custom form → ps-field + ps-btn from master
- Database/metrics: shared status-dot, spinner, page-nav, addon-row, status-card moved to app.css
- gsm_content: empty-state → ps-empty-msg, removed duplicate spinner/dots
- Rule 60: extracted _get_db_credentials() and _handle_db_restore()
- WR-PS-025 Issue B: deleted trigger-build.yml (Rule 103)
- WR-PS-031: CLAUDE.md golden_rules_version=2.17

## 2026.6.370
### Added
- WR-PS-024: Filesystem file backup — daily backup now includes /share/*-files/ alongside SQL dumps
- Encrypted tar.gz archives for addon file directories

## 2026.6.369
### Changed
- GIS → Farm rename: all Core references updated (backup, roles, heartbeat, licence, UI)

## 2026.6.368
### Changed
- Documentation update: CLAUDE.md, CHANGELOG.md, docs/AUDIT.md all current at v368

## 2026.6.367
### Changed
- Rule 125 complete: all 6 JSON POST endpoints use Pydantic models
- enroll_core + enroll_gsm converted to ConnectionCodeRequest

## 2026.6.366
### Changed
- Rule 125 partial: 4 endpoints converted to Pydantic models
- Global 422 validation error handler (Rule 147)
- New: paddicore/api/models.py

## 2026.6.365
### Fixed
- Rule 41: Remove all 14 inline `style="display:none"` from templates — use `.ps-hidden` CSS class instead
- Rule 41: Replace all JS `style.display` toggles with `classList.add/remove('ps-hidden')`
- Rule 41: Dynamic addon logo colour uses CSS custom property `--ps-addon-colour` instead of inline `background:`
- Rule 126: Add `_validate_config()` at startup — logs clear fatal message if required env vars missing

## 2026.6.363
### Security (adversarial audit — 19 findings closed)
- WR-PS-028: HMAC heartbeat signing with body-embedded signature (replay protection)
- Connection code HMAC verification (staged — accepts legacy unsigned)
- CSRF protection via content-type enforcement on API mutations
- Content-Security-Policy header added
- Request body size limit (10MB)
- Session cookie secure flag
- Admin role required on licence management endpoints
- SSRF guard on heartbeat/webhook URLs (blocks localhost/RFC1918/metadata)
- Rate limiting on sensitive endpoints (enroll, backup, restore)
- Error detail no longer leaked to clients (generic messages)
- Backup download path traversal guard strengthened
- tar.gz member type validation (skip symlinks/devices)
- Dead public path removed, licence-exempt prefix tightened
- Admin password masked in logs
- SQL injection pattern hardened (whitelist + dollar-quoting)
- PAT removed from git command-line args (uses GIT_ASKPASS)
- X-Frame-Options SAMEORIGIN added
- Boundary sync HMAC upgraded with nonce + body hash (Rule 142)

### Changed
- Heartbeat function split for Rule 60 compliance

## 2026.6.356
### Changed
- Route handlers migrated to `async_cursor()` — DB calls no longer block the event loop (Rule 121)
- All 24 migrations annotated with `# rollback:` + `# backward-compat:` notes (Rule 19)
- Added missing `error_tracker.py` + `perf_tracker.py` from canonical shared files (Rule 101)

## 2026.6.355
### Added
- Graceful shutdown handler (Rule 134) — cancels heartbeat/sync tasks, closes DB pool
- Mobile smoke tests (Rule 67) — 6 tests with mobile UA + seeded data assertions
- `close_pool()` and `stop_heartbeat()`/`stop_daily_sync()` public functions

### Changed
- Consolidated `_supervisor_headers()` to single `core/helpers.py` adapter (Rule 133)
- All 61 mypy errors fixed — zero errors with `--disallow-untyped-defs` (Rule 65)
- Module-level mutables annotated with justifying comments (Rule 128)
- Full Golden Rules v2.2 audit — zero ❌ gaps

### Fixed
- `ghcr.py` except-pass replaced with explicit return (Rule 62/64)

## 2026.6.354
### Added
- WR-PS-027: GHCR private registry credential registration — reads `ghcr_pull_token` from connection code, registers with Supervisor `/docker/registries` on startup
- Heartbeat reports `ghcr_creds_registered` flag for Admin fleet readiness tracking

### Changed
- Gateway cleanup: removed all spatial/machine/sync dead code (-12K lines); Core is now system gateway only
- WR-PS-026: two-token PAT model in `pat_manager.py` (separate dev + Supervisor tokens)
- Licence routes: removed unused PROVIDER_GSM import
- `gsm/` directory renamed to `licence/` to reflect gateway role

### Fixed
- CLAUDE.md updated to v353 architecture (was documenting pre-gateway structure)

## 2026.6.309
- Fix addon port map — add GIS/Store/Weather ports, correct existing ports
- This fixes licence activation for new addons on grower boxes

## 2026.6.308
- Fix addon module list crash (boundary slot DOM protection)

## 2026.6.307
- GSM boundary exchange moved into GIS module card (only shows when GIS licensed)

## 2026.6.304
- Backups write to /config/backups/ (host filesystem, survives crashes)
- Backup all 8 addon databases with 3-day rolling retention
- Download button on backup files

## 2026.6.300
- Deep clean: remove all farming references from metrics, selftest, heartbeat
- Core is now system gateway only (heartbeat, licences, addon discovery)

## 2026.6.267
- Weather station management improvements
- GSM paddock display fix for new growers
- Record Event page with Review/New modes
- Full mobile wizard for field recording
- Security fixes and code quality sweep
- NDVI reference layer on record page

## 2026.6.243
- CVE fixes (cryptography, Pillow)
- Pre-deploy audit automation
- Import Hub shapefile support
