# Changelog

## 2026.7.199

### Maintenance
- Internal code-quality fix; no change to how PWM works.

## 2026.7.198

### Reliability
- The add-on now reconnects to its database automatically after system updates or maintenance. Previously, a restart at the wrong moment could leave the add-on showing its licence screen until it was manually repaired — that can no longer happen.

## 2026.7.197 — Hone PLAT-08: dependencies hash-locked, image installs --require-hashes

### Security
- **`requirements.lock` regenerated with `pip-compile --generate-hashes --allow-unsafe`**
  (45 packages, 982 sha256 hashes, 0 unhashed — pip/setuptools pinned too). The old lock
  carried zero `--hash` lines.
- **Dockerfile installs ONLY from the lock with `--require-hashes`** — an archive that
  doesn't match its recorded hash, or a dep missing from the lock, aborts the build; no
  unverified fallback (GSM v2026.7.33 donor pattern, matches Core v2026.7.42).
- **`.github/dependabot.yml` added** (pip + docker + github-actions, weekly) — the
  SRV-PLAT-05 tracking half; regenerate the hash lock alongside any dependency merge.
- Proven both ways before ship: clean lock resolves + hash-checks; one flipped hash byte
  → pip refuses with "THESE PACKAGES DO NOT MATCH THE HASHES".

## 2026.7.196 — Water-balance checker: gate depth sensors were NEVER read (permanent STALE-SENSOR)

### Fixed
- **Every sensored gate flagged STALE-SENSOR forever** — a hydro-graph gate node's `sensor_device`
  is the gate's stored `depth_sensor` (an entity id), but the balance checker's `_node_level()`
  treated every `sensor_device` as a DEVICE NAME and fed it to the resolver, which anchors nothing
  for an entity id → level None on every sample → stale flag on every evaluation. Found live during
  the HZ-03 bench run (MC-01/MC-02 flags that never cleared). `_node_level` now reads entity-id
  sensor_devices directly from HA state (unit-normalised); device names keep the resolver path.
  3 tests. Also repaired live data: MC-01's stored depth sensor pointed at MC-02's dead pre-rename
  entity id (cross-wired) and MC-02 had none — both re-pointed to their own boards' live sensors.

## 2026.7.195 — W03 rebuilt as the Automations viewer (Peter-directed design session)

### Changed
- **Desktop W03 is now the read-only Automations viewer** — pick an automation (Flush · Pond ·
  Demand Pumping · Demand Level · Channel Management · Water Balance backstop) and see the
  canonical **trigger → response contract**, rendered faithfully from the controller source (cited
  per automation, monolith-parity verified), plus every live instance with its parameters and last
  decision trace. Two OPEN RULINGS are flagged inline in the Flush contract (timer-end release
  behaviour; paddock-wide gate close on flush start) — surfaced, not buried.
- **The HZ-03 balance policy gets its first UI**: OFF / ALARM / HOLD buttons on the Water Balance
  view (manager-gated POST, server-confirmed paint); `GET /api/hydro/balance` now returns the
  current `policy`. The old broken editor page is retired on desktop (gate/pump rule EDITING lives
  on W05/W06 since v.83); mobile keeps the legacy editor unchanged. Editor structural gates
  re-scoped to mobile; 5 new viewer gates added.
- Phase 2 (design agreed, not built): the HA-authoring round-trip — build rule-shaped automations
  in HA's automation UI on dev, PWM imports/validates/executes with its guard chain, exports back
  for editing. Dev-only, beside Bench Sim.

## 2026.7.194 — Bench (W09) is grower-facing: calibration belongs to the field

### Changed
- **W09 Bench graduated out of the Development section** (Peter 2026-07-24): actuator/depth
  calibration lives there and growers calibrate in the field. Sidebar entry now sits directly
  below Notifications in the setup group; route un-gated. Its entire command surface rides the
  operator-gated device endpoint — the same control class W01/W02 already give a grower.
  **W09S Bench Sim (water engine / depth inject) stays dev-only** — route 404s and nav hidden on
  grower installs; the bench-fixture APIs (test paddock / test mode) stay dev-only too. Gate tests
  updated to pin the new split.

## 2026.7.193 — base.yaml 2.3.0 hardening (v192 hotfix: duplicate sensor key): SNTP time fallback + OTA failure visibility (fleet OTA test cut)

### Added
- **SNTP fallback clock** — time came ONLY from HA, so an HA outage left boards clockless
  (timestamped logs, schedules, time-anchored logic drift). SNTP now keeps the clock honest
  independently; HA remains primary.
- **`OTA Failures` diagnostic sensor** — failed OTAs were invisible (silent dashboard retry).
  A reboot-surviving counter increments on every `on_error` and surfaces in HA, so a board that
  repeatedly aborts updates is visible instead of silently stuck on old firmware.
- **`api: reboot_timeout: 0s` documented as deliberate** — a timeout here would reboot every board
  on the farm periodically whenever HA is down, and a reboot blips the pump relay on the GPIO15
  strapping pin (Hone FW-08). WiFi-level recovery has its own reboot path.

This cut flags every board with an update by design: the fleet-wide OTA run IS the OTA bench test,
with one board interrupted at ~50% for the Hone FW-10 dual-partition rollback proof.

## 2026.7.191 — WiFi saga closed: root cause was a secrets SSID/password mismatch; IDF pin corrected to 5.4.4

### Fixed
- **The real root cause of the fleet-wide flash failures (2026-07-24):** dev's `secrets.yaml` had
  carried `RRAPL_HomeAssistant` + the **IOT network's password** since 2026-07-07 — harmless while
  builds resolved the (correct) shadow secrets, fatal once v167 retired the shadow: every fresh
  build since compiled the wrong password for its SSID → "4-Way Handshake Timeout" on every AP,
  every board, while old firmware (built from the shadow pair) stayed connected. Peter set the
  right password in the ESPHome Secrets UI → dev-rb-02 online first try. Model of record:
  **dev boards → RRAPL_HomeAssistant, prod boards → RRAPL_IOT, one Secrets-UI source per box.**
- **v190's esp-idf pin corrected 5.5.1 → 5.4.4**: the esphome-libs mirror only serves the latest
  patch per minor, so 5.5.1 404'd at build time. 5.4.4 is bench-proven (dev-rb-02). The pin stays
  as hygiene (framework was NOT the culprit) — an unpinned framework let builder updates silently
  swap the radio stack; bumps are now deliberate + canary-first.

## 2026.7.190 — PIN esp-idf 5.5.1 (ESPHome 2026.7.2 builder broke ESP32 WiFi auth)

### Fixed
- **Every board flashed from the ESPHome 2026.7.2 builder failed to join WiFi** ("4-Way Handshake
  Timeout" / "Auth Expired") while previously-flashed boards stayed connected — the phone-connects,
  secrets-verified, AP-unchanged triangulation left one variable: the builder's bundled esp-idf.
  Known upstream class (esphome/esphome#13443: esp-idf 5.5.2 breaks ESP32 WiFi auth; 5.5.1 good).
  `base.yaml` now **pins `framework: esp-idf version: "5.5.1"`** — an unpinned framework meant every
  builder update silently swapped our radio stack under the fleet. Future bumps are deliberate,
  canary-first per docs/FIRMWARE_ROLLOUT.md.

## 2026.7.189 — Dev boxes mint dev-* device names (dev/prod share one LAN)

### Fixed
- **Dev and prod boxes minted identical device names** (`pmp-NN`/`ch-NN`/`rb-NN`) on the same
  physical network — two boards with the same mDNS hostname = identity fights, wrong-board API
  connections, "invalid encryption key" chaos (Peter root-spotted it live: prod picked up dev's
  ch-02). A dev box (admin_key convention) now mints **`dev-pmp-NN` / `dev-ch-NN` /
  `dev-rb-NN`** — a namespace structurally collision-free with grower boxes.
  Prod-style names never feed the dev counter (numbering starts fresh). Test pinned.

## 2026.7.187 — Board-stranding class KILLED: creds harvest from the flashed YAML, never re-mint

### Fixed
- **Root cause of three stranded boards found and closed** (pdev-mc-01 2026-07-20, pmp-01 + rb_01
  2026-07-23; audit-trail proven). The kill chain: discover's prune deletes a registry row →
  re-creates it BARE (no `yaml_vars`) → the next regenerate MINTED fresh per-device creds → the
  board still runs what it was flashed with → OTA + native API both dead, serial flash the only
  recovery. On a 50-farm fleet this is a truck roll.
  Fix, two layers: `get_or_create_device_secrets` now **harvests the creds from the device's own
  YAML file** (the record of what the board was actually flashed with) before ever minting —
  minting is reserved for genuinely new devices with no YAML; and discover's row creation harvests
  at insert so re-created rows are never bare. Self-healing: a bare row + existing YAML now
  recovers silently (logged loudly as `creds_harvested`). 3 tests pin the precedence
  (registry → YAML → mint).

## 2026.7.186 — Pump runtime/water/service accrual FIXED + ESPHome "modified" churn FIXED

### Fixed
- **Pump run sessions never opened since the port** — `track_pump_state()` (which writes
  `pwm_pump_run_log`, the source for runtime totals, water use = hours x flow, and service-hour
  accrual) had ZERO callers: the monolith called it from the live poll and the port lost the call
  site. Found on PROD: main pump ran for hours, all three meters frozen. New supervised
  `pump_run_tracker` loop samples every pump each minute (UI-independent — the monolith only
  tracked while a page was open). Offline board = session closes (board meters own the dark gap);
  unresolvable entities = skip, never a false stop. 3 tests.
- **Every board flipped to "modified" in ESPHome after every PWM update/restart** — `run.sh`
  blind-copied all firmware includes on every startup (added 2026-07-19 to fix the sync's missing
  module files, but it bypassed the content compare), bumping every include's mtime; the ESPHome
  dashboard compares include mtimes against each board's last compile. Now copies only when
  content differs — byte-identical includes are left untouched.

## 2026.7.185 — Ganged actuator pairs are ONE control in the demand workflow

### Added
- **Ganged gates (two actuators, one water — `gang_switches` on the board) now appear as a single
  "(both actuators)" entry** in the W05 upstream picker AND the auto-stop watch list (Peter
  2026-07-23). Linking one writes the identical Pump Watch rule into BOTH actuator blocks
  (`suffix: "both"` on the pump-watch endpoint), so the pair regulates in unison through the
  ordinary per-actuator machinery — one card, one set of Low/High Demand boxes. Independent
  2-actuator gates keep their two per-actuator entries. Tests pin the both-blocks write.

## 2026.7.184 — W05 upstream card redesign (Peter walk, 2026-07-23)

### Changed
- **"1. Watch" → "Watch Sensor"**; "+ Link" button gone (both picks create the link; both pickers
  now RESET after linking — the retained Watch value turned the next actuator pick into a surprise
  duplicate link).
- **Sensor list shows names only** — the live reading in the option text cluttered the picker.
- **The in-card sensor select is gone** — it duplicated the Watch picker and read as a confusing
  extra option. The watched sensor shows as text in the card header ("Pit sensor → controls MC-01");
  unlink (×) and re-pick to change it.
- **Low/High clearly separated:** each link card now carries two bordered boxes — **"Low Demand
  setting"** and **"High Demand setting"** — each with labelled fields: *Min depth (cm) — gate opens
  below* and *Max depth (cm) — gate closes above*. Same stored truth (per-gate Pump Watch), just no
  longer crammed into two cryptic inline rows.

## 2026.7.183 — W05 walk fixes: depths appear on link, phone sensors out of the depth list

### Fixed
- **Upstream link depths were hidden behind a third click** — the LOW/HIGH min/max inputs live on
  the link card, which only appeared after "+ Link". Now picking BOTH "Watch" + "Control with"
  creates the card (and its depth inputs) immediately; + Link stays for parity (Peter walk
  2026-07-23: "I can set the watch and the gate but not depths").
- **Companion-app phone "distance" sensors excluded from the canonical water-depth list** — the HA
  phone app publishes a `device_class: distance` sensor per phone, which passed the filter and
  polluted every depth picker. phone/ipad/tablet name hints now reject (test pinned).

## 2026.7.182 — Demand: AUTO arm on the pump card + manual takeover + OFF opens (Peter-directed)

### Added
- **W02 pump card AUTO button** (desktop + mobile), next to OFF/LOW/HIGH: one arm for BOTH demand
  autos — auto-stop (all watched gates closed = zero demand, or flood max → pump stops) and level
  auto-compute (the demand level follows the watched gates). `POST /api/pumps/{id}/demand/auto`;
  refuses to arm with nothing watched. The demand panel now also shows when only auto-stop
  monitoring is configured (it used to hide unless upstream level control was enabled).

### Changed
- **Manual takeover sticks (trap closed):** tapping OFF/LOW/HIGH drops AUTO server-side. Before
  this, the level auto-compute ran whenever demand was configured and silently overwrote a manual
  pick within one controller cycle — the missing "button to select auto" in its truest form.
- **Demand OFF opens the gates (Peter ruled 2026-07-23: "off — just keep the gate open"):** the
  OFF transition now drives the controlled gate(s) OPEN (was: closed), and the gate's Pump Watch
  stops regulating at level none (was: silently kept regulating on the LOW band). Explicit
  `action: close` level configs still close.
- W05 saves carry runtime state through: the mobile save no longer resets the live demand level to
  OFF on every config save, and both bases preserve the new AUTO flag instead of dropping it
  (whole-object channel_control replace). Mobile's dead `close_at_cm` inputs removed (nothing has
  consumed them since 2026-07-14 — the real thresholds are per-gate Pump Watch LOW/HIGH min/max,
  now labelled as min/max on the desktop upstream cards).

### Tests
- `tests/test_demand_auto.py` (8): manual takeover drops AUTO · OFF opens (not closes) · arm/disarm
  round-trip · arm refused with nothing watched · auto-compute + zero-demand stop both skipped when
  manual · pump_watch skips at level none.

## 2026.7.181 — release-audit tidy (mypy)

### Fixed
- One `var-annotated` mypy error in the v179 dangling-pump guard (`pumps/control.py`) — caught by
  the pre-release audit, no behaviour change. This is the grower release of the v179–180 Farm
  infrastructure work.

## 2026.7.180 — W04: import Farm-drawn bays

### Added
- **W04 "Farm Bays (drawn in Farm)" section** (Peter-directed 2026-07-23): unbound Farm bays list in
  the paddock sidebar with an Import button each — creates the PWM bay pre-bound (shape mirrored from
  Farm, one-door). Shows which enabled paddock the bay lands in, or that its paddock isn't enabled in
  PWM yet (the server refuses with the same message). Stale-sync note when Farm is unreachable.
- **Bay editor honours the one-door up front**: a Farm-bound bay's "Redraw Boundary" button is
  disabled and reads "Shape is Farm-owned — edit in Farm" (the server already 409s the write; the UI
  now says so before the draw instead of after).

## 2026.7.179 — Farm infrastructure consumer (WR-PS-154): bays, pumps, gates, channels

### Added
- **Farm is the single author of physical infrastructure** (Peter 2026-07-23): bays, pumps, gates and
  channels are DRAWN on the Farm map; PWM pulls them read-only over the fleet sibling-pull
  (`/api/spatial/infrastructure` + `/api/spatial/bays`, 5-min cache, degrades to last-known when Farm
  is unreachable). Direction is strictly one-way — Farm never pulls from PWM (the Farm-side migration
  export is dead); PWM's ingress hardening is untouched.
- **Bind**: each PWM pump/channel/gate/bay links to its Farm feature by the stable Farm `uuid`
  (migration 010, `farm_uuid` on all four tables; bays bind on Farm's bay id until Farm mints bay
  uuids). Assignment is its own act — a Link picker on W05 (pump) and W06 (channel + gate), backed by
  `POST /api/farm-infra/bind` (type-checked, one Farm feature ↔ one PWM row).
- **Import**: a Farm-drawn feature with no PWM record becomes one, pre-bound (`POST
  /api/farm-infra/import`) — W06's new Farm panel lists them. Gates land under their channel via
  Farm's `parent_uuid` containment; bays map their paddock via `gis_paddock_id`. PWM adds only the
  control shell; every physical fact stays Farm's.
- **One-door geometry (per-asset)**: once bound, PWM refuses to author that asset's position/shape —
  pump/gate lat-lon, channel `data.path` and bay `geometry` edits 409 with "Farm-owned"; unchanged
  full-form echoes pass. Farm's geometry is mirrored into the legacy columns on every pull so the
  map/hydro graph/automation read exactly what they always read.
- **Dangling fail-closed**: a bound Farm ref missing from a SUCCESSFUL pull pauses that asset's
  automation (irrigation skips the bay, gate automation skips the gate, pump starts refuse 409) until
  re-bound or unbound. Farm-down is NOT dangling — the cache degrades stale, automation untouched.
- Supervised 5-min background sync (`farm_infra_sync`); `GET /api/farm-infra` +
  `POST /api/farm-infra/refresh` for the UI. 25 new tests (pull/degrade, bind, import, one-door,
  dangling incl. the pump-start refusal).

### Fixed
- 4 stale bench-sim tests updated to the v178 recycle-loop vessel model (pit/mcs1-3/bays, ML/day
  rates) — they still asserted the retired channel/pit model.

## 2026.7.178 — W09S bench: volume/ML-per-day water engine + sim-speed

### Changed
- **Engine rebuilt to Peter's real-world volume model.** Flows are now **ML/day** (Pump 1 = 30, Pump 2
  = 20, gate/valve = 60 x open%, bay loss = 5/bay); each vessel holds a fixed **ML capacity** (pit 15,
  MCS1/2/3 = 5/20/2, bays 2/3); **depth = volume/capacity x full-depth**, so the same flow spikes a
  small section (MCS3 = 2 ML) ~10x faster than a big one (MCS2 = 20 ML) — the real unbalanced holding.
  Bays lose water (seepage/crop); the pit depletes accordingly (no auto top-up — inject/reset). New
  **sim-speed** control (1x / 10x / 60x) fast-forwards time so a multi-hour automation proves in minutes.
  Depth stays in cm (UI + thresholds unchanged); only the depth delta per flow is capacity-scaled.
  Engine controls form is ML/day + speed. Physics pinned by 5 volume tests (conservation + capacity
  scaling). Bench-only.

## 2026.7.177 — W09S bench: workbench mirrors live mode/auto state

### Fixed
- **The workbench now reflects state changed anywhere** (real page OR workbench), not just pump
  running. Bay nodes show their live **mode** (Flush/Pond/Off); channel-gate nodes show **AUTO/MANUAL**;
  the gate control panel shows the current Auto/Manual state and highlights the active one. The
  5-second poll (`/api/bays` + `/api/channels`) drives it, and every panel action re-reads state so
  the panel updates immediately. Bench-only.

## 2026.7.176 — W09S bench: gate + pump control panels (full grower-toggle mock-up)

### Added
- **Gate + pump node controls** on the W09S diagram (bench-only), completing the full set. Pump nodes →
  Start/Stop; gate/valve nodes (MC-01/MC-02, RB-01/02/03) → Open/Hold/Close; the channel gates
  (MC-01/MC-02) also get **Auto/Manual**. Pump/valve commands use the board's own device command
  (by device name — the Rule-10 bench exception); gate Auto/Manual calls the real
  `/api/gates/{id}/auto-toggle`. With the bay panels (v175) the workbench now toggles everything a
  grower can — bay mode/depths/flush + gate auto/manual/open/close + pump on/off — all on the real
  production endpoints, so any scenario (Bay 1 Flush + Bay 2 Pond, MC-01 → Manual emergency release)
  is the real automation.

## 2026.7.175 — W09S bench: node control panels (real bay controls)

### Added
- **Click a diagram node → its control panel** (bench-only). Bay nodes open a panel with the REAL
  grower controls, each wired to the production endpoint: mode Flush/Pond/Off (`/api/bays/{id}/mode`),
  min/max depth +/− (`/depth-threshold/adjust`), flush hold +/− minutes (`/flush-timer/adjust`), and
  set-actual-depth (inject — the rig has no sensors). Channel vessels get set-depth; gate/pump manual
  controls are the next increment. Every control edits the same rows the paddock/config pages do — one
  source of truth, so a bench scenario (Bay 1 Flush + Bay 2 Pond) drives the real automation.

## 2026.7.174 — W09S bench: L-shape flow diagram (whiteboard layout)

### Changed
- **W09S diagram rebuilt to the whiteboard L-shape** (`flow.jpeg`): the main channel across the top
  (Recycle Pit → PMP1 → MCS1 → MC-01 → MCS2 → MC-02 → MCS3 → PMP2), the vertical bay cascade dropping
  from MCS2 (RB-01 → Bay 1 → RB-02 → Bay 2 → RB-03), and the two return lines (RB-03 → pit, PMP2 → pit)
  drawn as SVG connectors. Vessels fill to live depth + click-to-inject; gates/pumps show live state.
  Node divs positioned via JS (zero inline style). Bench-only. Reused real grower controls per node next.

## 2026.7.173 — W09S bench: serial bay cascade + locked model/scope

### Changed
- **Bay topology relaxed to the serial cascade** (Peter's real-world model): only Bay 1 draws from
  MCS2; each bay drains into the next (RB-02 = Bay 1 → Bay 2), the last bay drains to the Recycle Pit
  (RB-03). `set_topology` no longer requires a supply on Bay 2; the W09S bind form updated (Bay 1
  supply RB-01 + drain RB-02; Bay 2 drain RB-03). Model + full-control workbench scope locked in
  `docs/W09S_WORKBENCH.md` (recycle loop, reuse the real grower controls, inject-for-depth). Bench-only.

## 2026.7.172 — W09S bench: fixed recycle-loop diagram

### Added
- **Loop diagram** on W09S, drawn from the bench topology (not `/api/hydro/graph`, which can't
  express the loop or the drains). The recycle chain renders as live vessels — Recycle Pit → MCS1 →
  MCS2 → MCS3, plus Bay 1/2 — that fill to the engine's live depth and are click-to-inject, with the
  actuators between them (PMP1, MC-01, MC-02, PMP2, bay supply + B1/B2 drains) showing live pump/valve
  state from `/api/devices`. Shows the true flow including the drain cascade (B1→B2→pit) and the
  Pump-2 return, matching the v171 physics. Replaces the graph-driven flow visual on the bench page.
  Bench-only, no grower surface.

## 2026.7.171 — W09S bench: rebuilt to the real-world recycle-loop water model

### Changed
- **`sim_water` engine rebuilt to the real recycle loop** (Peter's model; was a linear chain):
  recycle pit → PMP1 → MCS1 → MC-01 → MCS2 → bay supply; MCS2 → MC-02 → MCS3 → PMP2 → pit; B1 drains
  into B2, B2 into the pit. Water now MOVES between vessels (mass-conserving `_move` helper) instead
  of appearing/vanishing, so every automation sees the exact threshold crossings the real closed
  chain does. Vessel↔board mapping corrected: pit=PMP1 sensor · MCS1=MC-01 · MCS2=MC-02 · MCS3=PMP2 ·
  bay_i=supply_i. Level keys, inject-mapping, offset writeback and the W09S level chips (Recycle pit /
  MCS1 / MCS2 / MCS3 / Bay 1 / Bay 2) updated to match. Physics pinned by 6 tests incl. full-loop
  conservation. Bench-only, no grower surface.

## 2026.7.170 — fix: W09S full-width page clears the sidebar

### Fixed
- **W09S full-screen shell slid under the fixed sidebar.** `main.ps-fullscreen` zeroes the
  `.ps-main-content` sidebar offset (`margin:0`, WR-PS-113), so a full-width fullscreen page reaches
  `left:0` behind the sidebar. Re-applied the `--ps-sidebar-width` left offset on the W09S container
  (desktop only; ≤768px the sidebar is a slide-out). Content now locks to the right of the menu.

## 2026.7.169 — W09S bench: full-width workbench shell

### Changed
- **W09S is now a full-screen workbench** (bench-only, no grower surface): the route opts into
  `fullscreen`, and the container fills the viewport as a flex column with the live flow visual as
  the hero (flex-fill); the rig-topology + engine controls sit compact in the fold beneath.
  Realises the W09S "full-width workbench, not a column" spec.

## 2026.7.168 — W09S bench: 5-node water chain (Pump1 → MC-01 → bays → MC-02 → Pump2)

### Added
- **Bench-sim rig extended to the full W09S chain** (bench-only, no grower surface). `set_topology`
  now binds `gate2_device` (MC-02, the downstream channel) + `pump2_device` (Pump 2, demand), both
  optional so a partial rig (e.g. Pump-2 unpowered) still binds. The water engine (`sim_water.py`)
  models the 5-node chain: bay drains feed the downstream channel (`channel2`), MC-02's gate releases
  it into Pump-2's sump (`pit2`), and Pump-2 running draws `pit2` down — the demand trigger. Inject +
  the flow-visual live-device set cover the two new nodes; the W09S bind form gained MC-02 + Pump-2
  pickers. Physics pinned by `tests/test_bench_sim_chain.py` (3/3). Foundation for the W09S workbench
  and the HZ-03/HZ-04 bench close-out.

## 2026.7.167 — fix: farm WiFi resolves from the MAIN esphome secrets (the ESPHome UI editor)

### Fixed
- **Changing WiFi in the ESPHome "Secrets" UI didn't reach the boards.** PWM kept a SECOND
  `secrets.yaml` in `/config/esphome/Includes/` that shadowed the main `/config/esphome/secrets.yaml`.
  Because `base.yaml` (`ssid: !secret wifi_ssid`) lives in `Includes/`, ESPHome resolved WiFi from
  the Includes copy — so a grower who changed WiFi in the ESPHome Secrets editor (which edits the
  MAIN file) still flashed the OLD SSID (prod, 2026-07-22: edited main → IoT, board flashed the
  stale HomeAssistant SSID). `ensure_farm_secrets()` now maintains ONLY the main file and **retires
  the `Includes/` shadow** (renamed to `secrets.yaml.retired`, with any keys the main file was
  missing carried over first). ESPHome's `!secret` then falls back to the main file, making the
  ESPHome Secrets UI the single source of truth for farm WiFi (Peter ruling, 2026-07-22).
- Per-device OTA/API creds are unaffected — they're set per-device in each device YAML's own
  `substitutions` (from `pwm_devices.yaml_vars`) and override the `base.yaml` `!secret` defaults,
  so the `ota_password`/`encryption_key` in `secrets.yaml` were only vestigial defaults.

## 2026.7.166 — fix: W08 desktop "Discover" button was dead (undefined function)

### Fixed
- **The desktop Devices page (W08) Discover button did nothing.** `pages/desktop/devices.html` wired the
  button to call `discover()` but **never defined the function** (mobile had it; the desktop copy had
  regressed — the same `discover()` ReferenceError class fixed once before in v2026.7.21). Clicking threw
  `ReferenceError: discover is not defined` → no request, no toast, so the ESPHome folder was never synced
  into the registry. That's why existing/renamed device YAMLs — and the 30 pre-existing prod boards —
  never appeared no matter how long the list was watched. Added the `discover()` function (POST
  `/api/devices/discover`, toast the found/created counts, reload), mirroring the mobile implementation.
- Reminder of the design: the device list (`GET /api/devices`) reads the **DB registry**; only **Discover**
  scans `/config/esphome/` and syncs files → DB. A newly-created or renamed YAML appears **after** you
  click Discover, never from the auto-refresh alone. (A device built via "+ Add device" registers its own
  row, which is why `rb-36` showed up without Discover.)

## 2026.7.165 — force prod to re-apply the fixed catalog mount (version-bump only)

### Fixed
- **The prod map fix now actually lands on grower boxes.** The real prod bug was never in the source
  repo: `PaddiSense/public`'s catalog `config.yaml` still declared `map: [addon_config:rw]`. Supervisor
  reads `map:` from the **catalog**, not the image, and `release.sh` Step 7 only bumps the catalog
  `version:` line — so the v162/v164 source-repo map fixes never reached growers (dev builds from source,
  so only dev was ever fixed). The catalog map was corrected out-of-band (`PaddiSense/public` `843e638`
  → `homeassistant_config` / `path: /config`).
- Supervisor only re-applies a changed `map:` on an **update** — a plain restart keeps the installed
  mount (confirmed on prod). This version bump is the clean trigger: `ha store reload` → `update pwm`
  recreates the container with the correct mount, so the firmware `Includes/` and the 30 existing ESPHome
  device YAMLs become visible to Discover again. No code change. Root-cause pipeline gap filed as WR-PS-115.

## 2026.7.164 — fix: deterministic HA `/config` bind on every Supervisor (prod device setup)

### Fixed
- **Prod ESPHome device setup was blocked** — v162 dropped `addon_config` so the container's
  `/config` would resolve to HA's real `/config`, which fixed dev, but prod (HA Green, a
  different Supervisor version) still routed the **deprecated short `config:rw`** form to a
  PRIVATE `/addon_configs/<slug>/`. At v163 that meant `firmware_sync` wrote the shared
  `Includes/` into the private dir and **Discover** scanned the private `/config/esphome`, so
  neither the includes nor the 30 real device YAMLs were visible.
- Replaced `config:rw` with the explicit long-form map:
  `type: homeassistant_config` / `read_only: false` / `path: /config`, which binds HA's real
  config directory to the container's `/config` on **every** Supervisor version. No behaviour
  change on dev (already resolving to the real `/config`).
- Note: `check-fleet-consistency` warns `[std-maps] missing addon_config:rw` for this opt-out —
  tracked under WR-PS-187 (A to allowlist). Warn-only; does not block the build.

## 2026.7.163 — re-cp master theme + finish the burn-down (last local tokens → master)

### Changed
- **Re-cp'd the canonical `paddisense-tokens.css`** (G updated it — WR-186 landings). Rule 17
  byte-identical restored so the release gate passes.
- **Burn-down complete — no PWM-local design tokens left.** G landed `--ps-control-h-hero` /
  `--ps-control-gap` in master (WR-186 follow-up), so the last two local tokens migrated:
  `--pwm-btn-h-hero`/`--pwm-btn-gap` → `--ps-control-h-hero`/`--ps-control-gap`, and the local
  `:root` token blocks (control + mode) are removed from both base templates. Every token now
  comes from the master theme.

(Includes the v2026.7.162 `/config`-mount fix.)

## 2026.7.162 — fix: addon read/write HA's real /config (not a private addon_config dir)

### Fixed
- **Removed `addon_config` from the `map:`.** It claims the `/config` mount inside the
  container, so on some supervisors (prod, a HA Green) it won over `config` and the addon
  read/wrote its **own private `/addon_configs/<slug>/`** instead of HA's real `/config`.
  Effect on prod: the firmware `Includes/` were copied there (invisible to HA's ESPHome) and
  `POST /api/devices/discover` scanned the private (empty) `/config/esphome`, so **existing
  ESPHome devices never appeared and W08 rebuilds couldn't compile**. Dev happened to resolve
  `/config` to HA's config, hiding the bug. PWM's own data lives in `/data`, so nothing of
  ours was in `addon_config`. Now the includes deploy to HA's `/config/esphome/Includes/` and
  discovery scans HA's `/config/esphome/` on every supervisor.

## 2026.7.161 — one shared offset stepper + tighter sensor filter + 1-dp readings

### Changed
- **Offset +/- adjustment is now ONE shared component** — `pages/shared/_offset_stepper.html`
  (`PwmStepper.card`, the bay's `.cfg-vstep` card lifted to a single source). The mobile bay
  offset **and** both channel-gate cogs (mobile + desktop) render from it; the cog stops being a
  divergent lookalike and *is* the bay card. `.cfg-vstep*` CSS moved out of mobile map into the
  partial. (Desktop bay keeps its own horizontal `.config-field` layout — noted follow-up.)
- **Sensor readings in the depth-sensor list now show 1 decimal**, not the raw 10-dp float.

### Fixed
- **The water-level filter no longer leaks half of HA.** The bare `"water"` name hint matched the
  addon's own name (*"Precision Water Management …"*) so every board diagnostic passed, and bare
  `"level"` matched Battery/Fuel Level. Tightened to specific depth phrases (`depth` / `water level`
  / `water depth`); unit (cm/m/mm) + device_class `distance` remain the reliable signals.

## 2026.7.160 — one canonical water-depth sensor list across the addon

### Fixed
- **The canonical water-level filter (`/api/ha-sensors`) now excludes batteries/diagnostics.**
  Every device's **"Battery Level"** sensor matched the `"level"` name hint and leaked into the
  list; `_is_level_sensor` now rejects battery / signal / wifi / rssi / uptime / cpu / memory /
  voltage names + those device classes (Peter: water-depth sensors only). This one fix cleans
  every picker backed by the list (gate cog, W06 automation, pump config).
- **W03 gate-automation depth-sensor pickers (mobile + desktop) now use `/api/ha-sensors`**
  instead of convention-built synthetic entity ids (which could list non-existent sensors and
  miss real ones). Any already-saved sensor stays visible if it's not currently in HA.

### Note
- `sensors.html` (W07 bay sensor bindings) is a general multi-type binding form (depth/soil/
  temp/battery) with a free-text entity box — not a water-depth picker. Converting its depth-type
  entry to the canonical select is a UX follow-up, not a battery-pollution fix.

## 2026.7.159 — channel-gate cog = sensor calibration (select + bay-style offset stepper)

### Changed
- The channel-gate gear cog (mobile + desktop) is now the gate's **depth-sensor
  calibration**, aligned to the model (Peter 2026-07-21):
  - **Depth sensor** is a **select** off the canonical water-level list (`/api/ha-sensors`,
    `_is_level_sensor`-filtered — no batteries/CPU), so a gate can watch a *non-own* sensor
    (e.g. the last supply gate watching the pump pit). This is the one list every depth-sensor
    picker in the addon converges on.
  - **Depth offset** is a live **+/- stepper** (±0.1 / ±1) like the bay level-offset, backed by
    the new `POST /api/channels/{cid}/gates/{gid}/offset/adjust`. No Save button — both auto-save.
- **Open/close trigger depths stay on W06** (one-time setup); they were never on the cog's live path.

## 2026.7.158 — strip redundant fields from the channel-gate gear cog

### Removed
- The W02 gear cog (mobile + desktop pumps) dropped four **dead/redundant** fields:
  **Open above / Close below** (`depth_open_cm`/`depth_close_cm` — superseded by the `data`
  automation model that the gate controller actually reads; nothing reads the flat columns)
  and **Open time / Close time** (`actuator_open_seconds`/`_close_seconds` — ESPHome owns
  travel time via the board's Travel Time entity). The cog now shows only the two fields the
  automation reads: **Depth sensor + Depth offset** (quick sensor-binding + calibration).
- Backend `_GATE_NUMERIC_COLS` tightened to `depth_offset_cm` only — the gate-update endpoint
  no longer accepts the legacy columns from a request (board-bind still populates board-derived
  columns). Tests updated to pin the tightened allowlist.

## 2026.7.157 — theme burn-down pt2: one shared actuator source (all 4 pages)

### Changed
- **Every gate/bay-door button now drives ONE source** — `pages/shared/_actuator_control.html`
  (`window.PwmActuator`: the Open/Hold/Close phase machine — cycle/seed/reconcile/paint).
  Mobile + desktop, map (bays + drains) and pumps (channel gates) all include it and delegate;
  the four local copies of the phase logic are gone. Styling stays canonical `.ps-actuator-btn`
  + `.is-*` (master theme). The two can no longer drift.

### Fixed
- **Desktop channel-gate button had INVERTED colours** (closed = green, open = amber, held = red)
  and used next-action labels — a real drift bug. Dropping its local `.gate-cycle-btn` CSS +
  driving `PwmActuator` gives it the ratified position scheme (light-blue open/opening, red
  closing/closed, dark-blue held) and current-state labels, matching mobile + the bay standard.
- `PwmActuator.paint` toggles only the state classes, so render-time width/flex classes survive.

## 2026.7.156 — clear the release gate: burn-down test + pre-existing type debt

### Fixed
- **`test_unknown_gate_state_labels_open[mobile]`** updated for the WR-186 actuator
  button — the mobile phase-machine paints unknown as a neutral `--` and the first tap
  *arms* (never fires), which is safer than the old simple-cycle; desktop assertion
  unchanged.
- **Cleared 9 pre-existing mypy errors** (7 files) that the newly-blocking release audit
  (WR-PS-159/157) surfaced — return-type annotations (`stream._gen`, `timers._start_with_cooldown_retry`),
  None-guards (`live` valve id, `channels` data_merge, `stats` fuel row, `commands` value cast),
  and a fault-narrowing guard in `sensor_integrity`. No behavioural change.

## 2026.7.155 — theme burn-down: adopt master WR-186 classes, delete app.css (part 1)

### Changed
- **`static/app.css` deleted.** Its contents are now canonical in the master theme
  (WR-PS-186): `--pwm-btn-h*` → `--ps-control-h`, `--pwm-mode-*` → `--ps-mode-*`. The
  `@media print` rule + `.pwm-hub-rows` moved into the base template. Only `--pwm-btn-h-hero`
  / `--pwm-btn-gap` remain PWM-local (no master equivalent yet — WR-186 follow-up to G).
- **Actuator button is now the canonical master component.** Mobile `map.html` (bay door)
  and `pumps.html` (channel gate) drop their local `.gate-cycle-btn` + `.state-*` CSS and
  use master `.ps-actuator-btn` + `.is-open`/`.is-closed`/`.is-held`/`.is-unknown`. One
  definition, in the master theme — the bay and channel buttons can no longer drift. Channel
  button colours corrected to the ratified bay-door scheme (opening = light blue, closing =
  red, held = dark blue) in the process.
- **Stale-tab update banner** → canonical `.ps-update-banner` (both base templates).
- Re-cp'd the master `paddisense-tokens.css` byte-identical (WR-PS-159 gate).

### Deferred (part 2, next commit)
- Desktop `map.html`/`pumps.html` actuator button still on local `.gate-cycle-btn`.
- On/off controls (pump toggle, relays, demand, Auto/Manual) → `.ps-btn-state-*`.
- Extract the Open/Hold/Close phase-machine JS into a shared partial.

## 2026.7.154 — revert the magenta theme-propagation test

### Reverted
- Removed the temporary `:root { --ps-bg: #ff00ff }` override from `app.css`. The
  test confirmed **every PWM page background is driven by the master `--ps-bg`
  token** (all pages went magenta, zero hardcoded) — the drift audit ahead of the
  WR-PS-186 master-theme promotion. Backgrounds back to normal.

## 2026.7.153 — TEMP: theme-propagation test (magenta --ps-bg override)

### Testing
- **Temporary** `:root { --ps-bg: #ff00ff }` override in `app.css` to visually prove
  every PWM page's background is driven by the master `--ps-bg` token (drift audit
  ahead of the WR-PS-186 master-theme promotion). **Reverted in the next release.**
- Also reconciles the CLAUDE.md version (staged with the bump this time).

## 2026.7.152 — channel-gate control: bay-parity Open/Hold/Close + card no longer collapses

### Fixed
- **Channel-gate button now uses the map bay-door's exact Open/Hold/Close phase machine**
  (`bayCycle`/`updateBayButtons` ported verbatim). Six phases advance one per tap, HOLD is a
  real resting phase (mid-travel stop / partial), and the tap paints the button optimistically
  with a 3 s lock so the live poll can't stomp it — so the button **visibly responds to every
  tap** (previously it could stick at `--` when live gate state hadn't resolved). Actions sent
  lowercase (`open`/`close`/`stop`) to `POST /api/command` `target: gate` as before.
- **Tapping Auto/Manual no longer collapses the open channel card.** `setGateAuto` updated the
  gate then called `loadConfig()`, which rebuilt all channel cards and dropped the `.open`
  class + any open gear panel. It now flips the button state in place and patches `configData`.
- **Channels and their gates now sort numeric-aware by name** (MC-01 < MC-02 < MC-10), not in
  raw DB return order.
- The gate's **big live depth** (offset-adjusted) now updates from live state instead of
  staying `--`.

## 2026.7.151 — channel-gate button: match the map bay-actuator (100px fat-thumb standard)

### Fixed
- The v150 channel-gate button used the desktop `.ps-btn` (52px), not the mobile standard.
  It now uses the **exact same `.gate-cycle-btn` as the map/irrigation bay actuator** —
  `height: var(--pwm-btn-h)` = **100px on touch** (the fleet fat-thumb standard), full-width,
  blue = open · red = closed · grey = hold. Consistent with the paddock irrigation control.

## 2026.7.150 — channel-gate control: single master button (bay-actuator style)

### Changed
- Reworked the W02.B channel-gate control from three buttons to a **single button that
  cycles open → hold → close, like a bay actuator** (Peter 2026-07-21), built on the
  **master `.ps-btn`** (the fleet-standard button used across the mobile pages) coloured
  by live state: **blue = open · red = closed · grey = hold**, amber while travelling.
  Tap cycles: closed→open, open→hold (stop), stopped→close. Rows stay: Auto/Manual · the
  gate button · big offset-adjusted depth.

## 2026.7.149 — channel-gate control redesign (mobile): Auto/Manual · Open/Hold/Close · big depth

### Changed
- **The W02.B channel-gate control is rebuilt to match bay gates** (Peter 2026-07-21).
  Three clear rows replace the ambiguous single "cycle" button: an **Auto / Manual**
  toggle (Auto = the logic drives it, Manual = you do; the board's physical switch works
  in both), an explicit **Open / Hold / Close** control that drives *all* the gate's
  actuators together (Hold = stop at position), and a **big offset-adjusted depth**
  reading. The live gate state highlights the active Open/Hold/Close button. Desktop
  replication + the gear-modal trim (drop the dead travel-time + sensor-name fields)
  follow next.

## 2026.7.148 — device builder: clear manual-switch mode (None / Ganged / Independent)

### Changed
- **The actuator manual-switch UI was unclear** — a per-actuator "switches" tickbox
  plus a gang checkbox that only appeared once *both* were ticked read as "just two
  tickboxes", with no obvious way to gang (Peter 2026-07-21). Replaced with one
  **Manual switches** selector: a 2-actuator board → **None / Ganged (1 switch pair,
  2 inputs) / Independent (2 pairs, all 4 inputs)**; a 1-actuator board → None / 1 switch.
  The pin-cost trade-off is shown inline, and the "switch on one gate only" ambiguity is
  gone. Maps to the same `actuators[].switches` + `gang_switches` spec (backend unchanged).

## 2026.7.147 — channel gate: multi-valve state read + one control drives all actuators

### Fixed
- **A two-actuator channel gate (MC-02) read blank and never updated the UI** — the
  live-state builder resolved by actuator index, which returns None for a board with
  two labelled valves it can't disambiguate. It now resolves each actuator from the
  gate's `entity_prefix` (`gate_1`/`gate_2`) and reports one combined state (open if any
  actuator is open; closed only when all are shut; position = most-open). MC-01 (single
  valve) unchanged. Bench 2026-07-21.

### Changed
- **The manual gate command drives all of a gate's actuators together** — Open / Close /
  **Hold (stop)** now applies to `gate_1`+`gate_2` for a multi-actuator gate, not just the
  first. Backend for the W02 channel-gate control redesign (Auto/Manual + Open/Hold/Close
  UI, matching bay gates, follows).

## 2026.7.146 — pump aux relay resolves via the board's own label when unnamed

### Fixed
- **A pump's Camera/Light aux relay 404'd "entity not found" when the pump row had no
  grower-set relay name** (pmp_01, bench 2026-07-21). The relay-toggle only tried the
  grower name + `relay_N`, but the board names its aux-relay switch by its builder
  LABEL (Camera → `…_camera`). It now falls back to the board's K3/K4 label from
  `board_meta` (ESPHome is the source of truth), the same fallback the device-command
  path already used. Pump 2 (relay names set) was unaffected.

## 2026.7.145 — resolver: a UniFi device_tracker could mis-anchor a board onto another

### Fixed
- **A board could resolve to a *different* board's entities.** `_anchor_entities`
  matched any entity whose object_id embedded the board's marker — including UniFi
  `device_tracker.*` entities, whose hostname-derived names can embed another board's
  marker. On the bench rig `device_tracker.…_pdev_b01_pmp_02_recycle` anchored `pmp_02`
  (Pump 2) onto `pdev_b01`'s device, so Pump 2 drove a bay board (2026-07-21).
  Device-trackers are never ESPHome control entities — they're now excluded from every
  anchor pass and the marker-scan union, so a board with no direct-slug entity falls
  through to its friendly-name slug correctly. All 7 rig boards now resolve to their own
  entity sets, no collisions.

## 2026.7.144 — firmware-gen: pump status pin token stripped → "Cannot resolve pin name D1"

### Fixed
- **A generated pump board YAML failed to compile** — `Cannot resolve pin name 'D1'`
  (pmp-01, 2026-07-21). The substitutions block rendered every value through
  `_yaml_scalar`, which strips `$ { }` (a Rule 175 secret-leak guard), so the pump's
  `pump_status_pin: "${D1}"` was gutted to bare `"D1"` — and ESPHome can't resolve a
  bare `D1` (it's a hw-core substitution key, not a board pin). Now the substitutions
  block renders through `_pkg_var`, which preserves whitelisted pin tokens (`${A1}`,
  `${D1}`…) while every non-pin value still falls through to `_yaml_scalar`, so
  `${device_api_key}` and other secrets stay stripped (exact-match whitelist). The two
  already-generated pump YAMLs were corrected on disk; test locks the contract.

## 2026.7.143 — W08.B: pump start/stop pulse times in the device builder

### Fixed
- **The device builder had no field for a pump's momentary relay pulse times** — a new
  pulse pump silently took the 4s default with no way to change it (Peter 2026-07-21).
  Added **Start pulse (s)** + **Stop pulse (s)** inputs to the pump section, shown only
  when Start mode = **Pulse** (a constant pump just holds the relay energised, so they're
  hidden). The backend already round-tripped `on_trigger_s`/`off_trigger_s` end-to-end;
  this wires the UI to it (hydrate on edit + include in the submit body). Test locks the
  UI→YAML contract (`pump_turn_on/off_trigger_time_s`).

## 2026.7.142 — sensor integrity monitor (catch a lying level sensor)

### Added
- **Sensor integrity monitor** (`automation/sensor_integrity.py`, spec
  `docs/SENSOR_INTEGRITY.md`) — catches the three real field failures a value check
  can't, by judging the water's behaviour against what the valves/gates were doing:
  - **#1 floating** — sensor bobbing on the surface: large oscillation while the
    bay is quiescent (gate closed).
  - **#2 mud / venting** — buried sensor that can't release pressure: slow (diurnal)
    drift while quiescent.
  - **#3 no-response** — broken gate or stuck sensor: level flat while a gate is open.
  Runs per bay every 5 min off the depth poller, over the history already in
  `pwm_depth_log` + the valve activity in `pwm_gate_log`. Thresholds are
  Peter-confirmed (2026-07-21).
- **`sensor_fault` notification event type** — a confirmed fault raises a deduped
  grower alarm (per-bay `tag`) routed to any subscribed group; a group whose targets
  include a `mobile_app_*` service delivers it straight to the **HA Companion app**.
  Falls back to a persistent notification when no group is configured.
- **`sensor_health.py`** back end — debounce (a fault must persist 2 windows before
  it fires), one-shot alarm + re-arm, and an opt-in `lost_level_action`
  (`off`/`alarm`/`hold`, default `alarm`) policy.

### Changed
- **The irrigation controller now holds a bay whose sensor is flagged** (or has gone
  silent) instead of acting on it; under the opt-in `hold` policy it fail-safe closes
  the supply if the bay is still filling (only ever closes, never the drain — idempotent
  via the v2026.7.141 valve-command guard). `hold` is bench-only until ratified.

## 2026.7.141 — bay valve commands are conditional on live state (fix drain beeper)

### Fixed
- **Idle bay no longer beeps the board every control loop.** The irrigation controller
  re-issued `send_valve_command(drain, "close")` every 60s loop unconditionally; the rb
  firmware beeps as safety feedback on *every* close it receives, so a bay left armed in
  Flush beeped its drain board once a minute (bay 2 drain, 2026-07-21 — the sim engine was
  disarmed but the bay stayed in Flush, since engine-off ≠ teardown).

### Changed
- **`send_valve_command` reads the valve's live HA state and skips a no-op command**
  (new `_valve_at_target`): if the valve is already closed/closing (or open/opening) the
  command is not sent — no Supervisor call, no beep, no spurious `pwm_gate_log` row.
  Genuine drift still re-asserts immediately; `stop` is never suppressed. A chokepoint fix,
  so all bay-valve callers (flush/pond/demand/gate) are covered; the channel-gate path
  (`_gate_auto_send`) already debounced. Every command that DOES reach a board still writes
  its `pwm_gate_log` row, so a board action is always traceable.

## 2026.7.140 — housekeeping: theme re-cp (WR-185 sidebar-collapse) + AUDIT currency

### Changed
- **Theme re-cp to canonical** — `static/paddisense-tokens.css` re-synced byte-identical to the
  master (Rule 17) after G's WR-PS-185 additions landed (the `.ps-sidebar-section-*` /
  `.ps-sidebar-chevron` collapsible-section family + `.ps-qr` + `u-mh600`). PWM doesn't use
  these classes yet; this is the standard re-cp-on-next-touch so byte-identity holds.
- **AUDIT.md currency** bumped to v.140 — records the v.137–.140 surface (bench-sim flow visual;
  `/api/bench/sim/{inject,layout}` bench+manager-gated; `/api/hydro/balance/policy` manager-gated,
  `hold` additionally bench-gated). All gated + tested; no verdict changes.

## 2026.7.139 — HZ-03 over-fill backstop groundwork (water-balance action layer)

### Added
- **Over-fill backstop (HZ-03), opt-in** — the water-balance checker already detects the
  cross-sensor over-fill signal (`contradicted`) + lost level (`stale-sensor`); it can now
  act on a **confirmed** one (persists `CONFIRM_TICKS` windows, fires once, re-arms on clear):
  - `pwm_config['water_balance_action']` = `off` (default, detect-only, unchanged) /
    `alarm` (notify — over-fill→`overflow`, lost level→`depth_warning`) / `hold`
    (alarm **plus** a fail-safe close of the implicated bay inlet).
  - `POST /api/hydro/balance/policy` sets it (manager). **`hold` is bench-only** until Peter
    ratifies the fleet default — a grower box refuses it, so control never acts on the
    still-being-proven signal (grower owns the system).
  - `/api/hydro/balance` payload now carries `action_policy` + per-edge `confirmed`/`action`.

### Notes
- Default `off` = **no behaviour change for growers**. This is the software groundwork for
  increment C; the bench (W09S flow visual) is where `alarm`→`hold` gets proven, then W10
  reveals the read-only lens and HZ-03 closes. Firmware/implausible-value half of HZ-04
  (irrigation `_eval_*` silent-on-None) is a separate surgical change, still owed.

## 2026.7.138 — flow visual: rig-scoped bench + manual depth-inject + drag layout

### Added
- **Manual depth-inject** (`POST /api/bench/sim/inject`) — drive any vessel node's
  simulated depth directly from the flow visual (type a cm, hit set). Writes the same
  board offset the engine would (channel→gate board, pit→pump, bay→supply) so the real
  automations see the threshold cross identically — and works with the engine OFF, for
  precise boundary probing (drive B-01 to 4.9 → no fire → 5.1 → fires). Bench-gated
  (server AND UI).
- **Drag-position layout** (`POST /api/bench/sim/layout`) — reposition flow nodes on the
  bench; the layout persists (bench-sim state, not farm topology). Desktop only.

### Changed
- **W09S flow visual is now scoped to the rig** — the bench shows only its bound boards +
  the TEST paddock's bays + the connecting channel, not the whole farm. Growers still get
  the full farm on W10 (Peter 2026-07-20). Bench nodes read depth from the engine's sim
  levels; grower mode reads real sensors.
- `PwmFlow` gained `onInject`/`onMove` callbacks + per-node depth/position overrides
  (`nodeInfo`, `positions`) — same shared renderer, driving affordances only in bench mode.

## 2026.7.137 — bench-sim reshape: live water-flow visual (W09S) + scenario retire

### Added
- **Live water-flow visual (`pages/shared/_flow_visual.html`, `PwmFlow`)** — one shared
  renderer of the farm's hydraulic chain: tanks fill to each board's live depth, gates
  animate with their open %, edges show flow, and each node carries a **trigger badge off
  the automation trace** (which rule fired and why). Fed by `/api/hydro/graph` +
  `/api/devices` + `/api/gate-automation/status` + `/api/bay-automation/status` — no new
  backend. Mounted in **bench mode** on W09S (desktop + mobile); the same partial becomes
  the read-only grower Water Chain (W10) in a later cut (design `docs/BENCH_SIM_FLOW_VISUAL.md`).

### Changed
- **W09S reshaped** — the scenario/evidence machinery is retired (the sim tests automation
  *logic*, not buttons; RB-01 already proved the buttons on real hardware, Peter 2026-07-20).
  Topology binding + water engine move into a collapsible section; the flow visual is the hero.

### Removed
- **Scenario/evidence endpoints** `/api/bench/sim/scenario`, `/scenario/step`, `/scenario/finish`
  and the `SCENARIOS`/`runs` state. HONE closure is Peter's live judgment + code verification,
  not a recorded-scenario log. Engine + topology + reset-water + teardown are untouched.

## 2026.7.136 — single-actuator gang pin fix + Development surface gated for growers

### Fixed
- **🔴 Composed YAML: single-actuator boards emitted `allow_other_uses: true`**
  on their switch pins → ESPHome refused ("Pin 36 incorrectly sets
  allow_other_uses: true", pdev-mc-01 regenerate). Ganging shares one pin pair
  across actuators, so `allow_other_uses` is only valid with 2+ switched
  actuators; a lone switched actuator owns its pins. Gang now takes effect
  only at switched-count ≥ 2 (allocator + budget check). Regenerate affected
  single-actuator boards once on W08.

### Changed (grower-release prep)
- **Development surface gated behind `bench_enabled`** — Water Chain (W10,
  unproven balance checker) and Automation (W03, dev surface) are dev-only per
  Peter (2026-07-19/20). The desktop sidebar "Development" section is hidden
  and the `/water/`, `/automation/`, `/automation/trace/*` routes 404 for
  growers, matching how Bench/Bench-Sim already behave. No change on dev boxes
  (admin_key set).

## 2026.7.135 — one firmware door + minted device names + `${D1}` generator regression

### Fixed
- **🔴 Composed YAML pin regression (.85)**: the secret-exfil hardening
  stripped `${}` from every rendered field, gutting the allocator's
  `${D1}`/`${A1}` pin tokens to bare `D1` — ESPHome: "Cannot resolve pin name
  'D1' for board esp32dev" (pdev-mc-01, live). Exact-token whitelist restores
  pins; `${device_api_key}` still dies. Regenerate any board composed on
  .85–.134 (one W08 edit → Confirm & write).
- **W02.B: config actions no longer slam cards shut** — Auto/Manual/save
  re-renders now preserve open cards and open gate-config panels.
- **W02.B: an unbound gate says so** ("No board bound — bind one on Channel
  Setup") instead of a silent `--` with missing actions.

### Changed
- **W08 is the ONE firmware door (Peter re-ruled).** W06's legacy combined
  save+write-YAML is stripped (endpoint dies with the monoliths at T9) and the
  seven structure fields (actuator count/labels/gang/depth-fitted/travel) left
  W06 entirely: **binding a board copies its structure + entity_prefix from
  the board's YAML spec into the gate row server-side**, and a W08 regenerate
  re-syncs every bound gate row. Legacy boards without a spec are untouched.
- **Device names are minted, not typed (Peter-ruled)**: the W08 builder
  assigns `pmp-NN` / `ch-NN` / `rb-NN` (mDNS-safe hyphens) server-side at
  write time; numbers are max+1 over the registry, snapshot history and the
  ESPHome dir — a retired number never comes back. Name field is read-only in
  create AND edit (identity is never edited).
- **W08 "Hold position" carries no timer** — hold means do nothing ever; the
  time field only appears for policies that act (bay preset's stray
  hold+300min corrected to hold+0).

## 2026.7.134 — scheduled starts survive the cooldown + W02.B walk batch 2

### Fixed
- **A scheduled start refused by anti-short-cycle now waits out the cooldown
  and retries** (up to 3 attempts) instead of dropping the schedule — live:
  the pump stopped 46s before its scheduled time and "Wait 14s" killed a
  start the grower armed hours earlier. The refusal carries a machine-read
  `retry_after` (no string matching); dry-supply/offline refusals still
  drop-and-notify, retrying those could move water when nobody expects it.
  Verified live same day: arm → fire on the scheduled second → 60s run →
  auto-stop → board backstop resynced.
- **W02.B: Schedule Start showed only the calendar icon** — inline JS painted
  the label muted-on-grey (invisible; emoji ignore CSS colour) and panel-open
  painted it blue. All inline colour writes on the shutdown/schedule buttons
  removed — the class owns colour ("Shutdown Active" black too).
- **W02.B: Schedule Start drops back to grey once it fires** — desktop kept
  the green armed class forever (mobile removed it); green means "a future
  start is armed", the running state is already told by the toggle + clock.
- **W02.B: relay ON buttons finally go green** — `.pwm-relay-state-btn`'s grey
  base is defined after `.btn-start`, so the cascade ate the state colour;
  compound rules give the state class precedence (matches mobile).
- **W02.B text sizes**: fuel label matches service text (14px secondary);
  stat values (Water Pumped / hours) 18→20px.

## 2026.7.133 — no automation compares raw sensor values + W05 sensor-first flow + browser-walk fixes

### Changed
- **Calibration ruling (Peter 2026-07-20): every automation compares CALIBRATED
  depth, never raw.** Gate rules (overflow, pump-watch, downstream) now read
  through one calibrated reader — unit-normalised by the entity's real unit
  (card-display convention) + the sensor's registered `depth_offset_cm`,
  offset map rebuilt every controller cycle. Bay irrigation/depth-poller and
  the pump dry-run guard were already calibrated (bay offset / board-side
  offset) — unchanged.
- **W05 Upstream Gate Control is sensor-first**: "1. Watch [sensor] →
  2. Control with [actuator] → + Link". The sensor is the subject (any board —
  pump or gate), the gate actuator is the instrument; cards read "→ controls
  …" with a labelled watching-sensor select. Same stored truth
  (`gate.automation.pump_watch`) as the W06 gate modal.

### Fixed
- **Demand channel-depth safety stop never fired for metre sensors** — it
  compared the raw HA state with no unit conversion (0.35 m vs 30 cm), so an
  over-full channel could not stop the pump. Now calibrated like everything
  else (+ pin).
- **W05: ticking "Enable Upstream Gate Control" on the checkbox itself did
  nothing** — desktop was missing the `change` listener mobile always had; the
  gate list never opened.
- **W05: adding a link discarded unsaved edits** in existing threshold cards.
- **W02.B browser-walk items (Peter)**: Set Shutdown/Schedule Start black text
  on grey (was blue-on-grey); Camera/Light relay buttons black text (was
  literally grey-on-same-grey) + standard `--pwm-btn-h` height; Service Reset
  on the standard height token; service time text 11→14px brighter.
- **Hub: Automation tile removed on desktop** (dev-only surface; sidebar keeps
  the route — parity with mobile).

## 2026.7.132 — stale-tab reload banner + start refusals shown on the button

### Added
- **Stale-tab watch (every page, both form factors)**: a deploy used to leave any
  open tab running the old JS silently — the .131 afternoon proved it twice
  (desktop tab: START sent stop; phone tab: STOP sent start, "it won't stop").
  Both base templates now compare their render-time version against `/health`
  once a minute and whenever the tab returns to the foreground, and show a
  fixed "PWM updated to vX — tap to reload" banner on mismatch. Reload is the
  operator's tap, never automatic (a mid-form auto-reload would eat input).
- **Start refusals own the toggle button (W02.B + W02.M)**: a refused start
  (anti-short-cycle, dry-run, offline) only flashed a toast, then the button
  repainted "OFF — START" — indistinguishable from silent failure.
  Anti-short-cycle now counts down in place ("ANTI-SHORT-CYCLE — WAIT 47s",
  amber); other refusals hold their reason on the button, then hand back to
  the poll. `sendCommand` returns the response so the toggle can tell a
  refusal from success.

## 2026.7.131 — pump toggle regression fixed (state read from live data, not a colour class)

### Fixed
- The b123 state-colour flip inverted `pumpToggle`'s class-derived running check
  (`contains('btn-stop')`) — a running pump sent 'start', a stopped one sent 'stop';
  control dead both ways on both form factors. The handler now reads
  `liveData.pumps[id].running` — state never derives from styling again.

## 2026.7.130 — browser (W02.B) parity sweep + device-adaptive sizing token

### Changed
- **The sizing token is now device-adaptive, one mechanism everywhere**: `--pwm-btn-h`
  = 56 px for fine pointers (mouse), 100 px under `@media (pointer: coarse)` (touch =
  the fleet fat-thumb standard). Declared in app.css + inline in both bases; every
  template shares the same classes and the device picks the size.
- **W02.B behaviour parity with the validated mobile page**: Set Shutdown/Schedule grey
  idle → solid green armed (outline styles gone); Start greys while counting; Constant
  default + duration folded; ARMED schedules follow the controls (live re-arm, debounced,
  toasted) with reload hydration from the armed truth; Fill + / Set Total absolute fuel
  correction; Water Pumped always shown with all-time Total; Low-Supply Override
  full-width with unmistakable text.

## 2026.7.129 — stopwatch chip removed (diagnosis complete)

### Changed
- The dev-only client stopwatch/probe comes out — depth confirmed fast (~0.5s, was 6-10s).
  The root-cause chain it found, for the record: first live paint raced selectPaddock's
  badge re-render → visible depth waited a full poll cycle; settle repaints fixed it.

## 2026.7.128 — depth paints inside ~1s (paint raced the paddock re-render)

### Fixed
- Chip diagnosis (cfg 0.3s / live 0.2s / depth 10.3s, probe d:0.1 on:true): the first
  live paint landed on DOM that selectPaddock's re-render then replaced — depth waited a
  full 10 s poll cycle. Both maps now repaint after the builders settle (immediate +
  700 ms + 2 s idempotent passes), so first depth lands within ~1 s.

## 2026.7.127 — stopwatch chip probes B-01's raw payload values

### Changed
- Chip now appends the first device-bearing bay's raw `{water_depth_cm, device_online}`
  as the client sees them — cfg 0.3s/live 0.2s/depth 10.3s (exactly one poll cycle)
  means the first successful payload is being DISCARDED by the paint gate; this names
  which field blocks it.

## 2026.7.126 — on-device stopwatch chip for W01.M (dev boxes only)

### Added
- Tiny fixed chip (bottom-left, bench-enabled boxes only) reporting the phone's own
  measurements: cache hit/miss, config-fetch seconds, live-fetch seconds, and
  time-to-first-depth-paint — server is proven <1 s, so the 6 s lives client-side and
  this names it.

## 2026.7.125 — warm resolver caches (15 min TTL) + /api/live timing instrumentation

### Changed
- Device entity-set cache TTL 60 s → 15 min (sets change only on flash/rename;
  `bust_device_entity_cache()` fires on discover). On a quiet farm the 60 s expiry made
  the first `/api/live` after page-open pay a full multi-second cold re-warm — the
  prime suspect for the persistent ~6 s first depth.
- `/api/live` logs a warning with the build time whenever it exceeds 1 s — no more
  theorising about where the seconds go.

## 2026.7.124 — depth values paint the moment they arrive (was gated on the GIS fetch)

### Fixed
- Map init awaited Promise.all(config+boundaries, live) before ANY paint — the ~6 s
  first depth on K09 B-01 was the GIS boundary proxy round-trip holding the live values
  hostage. Both maps now paint incrementally: cached live as soon as the UI exists,
  fresh live the moment its own fetch returns, boundaries whenever they land.

## 2026.7.123 — the fleet state-colour law (Peter 2026-07-20)

### Changed
- **Pump**: GREEN running ("RUNNING — STOP") / RED stopped ("OFF — START") — state
  colour, action named after the dash. Both form factors.
- **Arm toggles** (Set Shutdown, Schedule Start): GREY when idle (was red), solid GREEN
  when armed — matching the relay pattern.
- **Auto toggles** (gate auto / manual): GREY when off (was warning-yellow), GREEN when
  auto — paddock mode rotator Off already grey via the mode tokens.
- **Relays**: green energised / grey off (already compliant). **Flush pink / Pond blue**
  via the mode tokens (already compliant). The law rides in the templates and goes
  verbatim into the master-theme WR.

## 2026.7.122 — mixed-prefix boards: multi-anchor resolution + union fallback (fuel blank root cause)

### Fixed
- **Recycle Pump fuel showed `-- / 1000 L`** while the entity read 200 L live: the
  test-pump board is mixed-prefix (old `pdev_test_pump_*` entities + new
  `precision_water_management_pdev_test_pump_*` after a rename — fuel among the new).
  The resolver's first anchor pass returned the old subset, and when the single
  `device_entities` template call failed (orphaned anchor), it silently fell back to
  that subset — pump status worked, fuel vanished. Now: up to 3 anchors are tried, and
  the fallback is the UNION of all marker scans (device-name + friendly-slug, sibling-
  excluded), with a loud warning when the template path is unresolvable. Pinning test.

## 2026.7.121 — standard top banner on every mobile page + badge doubling fixed

### Fixed
- **Paddock Setup (W04.M) had no top banner** — the template set `active_page='hub'`
  (the base's banner-suppress condition). Removed; every mobile page now carries the
  base banner. The map keeps its own tab-bar home (the reference size Peter chose).
- **Badge doubling** (`W02.M.M`/`W04.M.M`): templates hard-set `page_id='W0x.M'` on top
  of the base's `.M` suffix. Normalised to bare ids.
- Standard banner's Home button sized to the map's reference (52 px target).

## 2026.7.120 — B-01's calibration row restored (div imbalance)

### Fixed
- The stacked .116/.117 edits left one extra `</div>` per Sensor Calibration row — the
  first row's stray close terminated the collapsible container, trapping B-01 in the
  broken wrapper while later bays escaped outside it (K09: "nothing for B-01").
  Balanced; net-div audit across all three heavy templates now 0/0/0.

## 2026.7.119 — instant first paint from last-known values (W01.M + W02.M)

### Changed
- Live snapshots cache to localStorage on every successful poll; page open paints the
  last-known values immediately, stream/poll overwrites with fresh truth — no more
  zeros/blank gauges "taking some time to populate" (fuel gauge + K09 sensor values).
  Fuel meter itself verified correct against history: burn only while running at the
  calibrated 10.2 L/hr; refuel and Set Total land exactly.

## 2026.7.118 — white text on the +/- adjusters

### Changed
- Adjuster buttons keep their red/green fills but the +/- text is theme white on all four
  templates (was error/success-coloured text on same-family tinted backgrounds — blended).

## 2026.7.117 — flush timers vertical; LIVE DEPTH readout

### Changed
- Flush timers re-oriented to the vertical stepper: +1m/+10m above the countdown,
  -1m/-10m below (state label rides beside the bay name).
- Sensor Calibration's depth readout renamed **Live Depth** and enlarged (28 px, info
  colour) — walk-confirmed working.

## 2026.7.116 — W01.M config overlay: vertical steppers, contained scroll, no iOS text-selection

### Changed
- **Vertical steppers** (Peter's design): + row above, big value centre, - row below —
  full-width glove buttons, no more tall-and-narrow towers. Water Depth Min|Max as
  side-by-side columns; Sensor Calibration offset gets +0.1/+1 over the value, -0.1/-1
  below.
- **Overlay owns its scrolling**: `overscroll-behavior:contain` + body locked while the
  overlay is open — reaching the panel edge no longer hands the scroll to the page
  behind (the "screen moves, not the cards" trap).
- **iOS long-press text selection/callout disabled app-wide on mobile** (controls are
  not a document); real inputs keep selection.

## 2026.7.115 — flush +/- double-fire fixed; steps are ±1/±10 min

### Fixed
- The .114 flush-adjust binding was inserted twice on W01.M — every tap fired two
  adjustments (-1 acted as -2, +5 as +10). De-duplicated to one listener.

### Changed
- Flush hold adjusters are now -10m / -1m / +1m / +10m on both form factors
  (Peter's steps; was ±5m on the outer buttons).

## 2026.7.114 — mode-colour tokens (declared once) + mobile flush-display fix

### Changed
- **Flush/Pond/Drain/Off colours are now semantic tokens** (`--pwm-mode-*`), declared
  once — every rotator button and both maps' Leaflet polygons resolve from them (the JS
  colour maps read the computed tokens at runtime since SVG attributes can't take
  var()). Changing a mode's colour is one line, answering Peter's "does it apply across
  all of them" — it does now; it was 8 scattered declarations before.

### Fixed
- **W01.M flush +/- buttons were DEAD** — built in the overlay but never bound to a
  handler (and `flushTimerAdjust` didn't exist on mobile at all); the earlier "toast but
  no change" was the water-depth toast beside them. Bound + implemented; the toast now
  states the new hold time in minutes.
- **W01.M flush timer looked frozen** — same bug as W01.B v2026.7.90, mobile copy: the
  card showed stale `remaining` while +/- correctly adjusted the duration. Idle now
  shows the configured HOLD TIME (live-updating on tap), running shows the countdown.
  Note: a bay created before migration 009 shows its stored value (e.g. 1 h) until
  adjusted — stored values are deliberately untouched.

## 2026.7.113 — the live stream reaches mobile

### Changed
- **PwmLive (SSE client) added to the mobile base** — it only existed in the desktop
  shell, so W01.M door positions were still on the 10 s poll (jumpy 5%+ steps).
  W01.M now patches per-1% valve deltas in place (entity-matched, throttled repaint,
  post-tap locks released by truth); W02.M refresh is stream-kicked (800 ms coalesce).
- W01.M: door-button text wraps inside the fixed 100 px (was clipping "HOLD 69%");
  first bay labels by its real name (B-01) instead of "Supply".

## 2026.7.112 — PWM-wide fat-thumb pass (the fleet-standard test case)

### Changed
- **Every mobile template adopts the validated standard**: `height:var(--pwm-btn-h, 100px)`
  on all button rules — W01.M map (door controls included), W04.M paddocks, W06.M
  channels, W07.M sensors, W08.M devices, bench sim (22 rules converted; W02.M already
  on it). W02.M inter-button spacing normalised to `--pwm-btn-gap`.
- **Shared W01 desktop template**: fat-thumb keyed to touch — `@media (pointer: coarse)`
  applies the height token to door/gate/mode controls on any touch device; mouse desktops
  keep tight controls.
- **Page badge standardised**: `W02.M` / `W02.B`; the build number shows on dev boxes
  only (bench_enabled) — it stays as the stale-render tripwire without grower noise.
- TEST buttons removed (diagnostic served: WebKit min-height quirk found, 100 px + token
  mechanism validated on-device).
- Flagged for walk, not auto-grown: W03.M mini config-toggles, NT01.M filter chips.

## 2026.7.111 — the validated standard applied: height:var(--pwm-btn-h, 100px) on all 27 W02.M controls

### Changed
- Peter validated 100 px on-device (TEST B) and the token mechanism (TEST C ≡ B). All 27
  W02.M controls convert from `min-height` (ignored by WebKit on flex buttons — the root
  cause of the height churn) to `height: var(--pwm-btn-h, 100px)`; tokens set to 100 px.
  TEST buttons stay one build for the internals-match check, then come out.

## 2026.7.110 — diagnosis landed: WebKit ignores min-height on flex buttons

### Changed
- TEST B at Peter's requested 100 px; TEST C added (`height: var(--pwm-btn-h, 100px)`) to
  validate the token mechanism. A/B result on-device + clean CSS parse identified the root
  cause of the height churn: WebKit does not honour `min-height` on `display:flex`
  buttons — the fleet standard will be built on explicit `height`.

## 2026.7.109 — TEST buttons on W02.M (diagnostic build)

### Added
- Two TEST buttons above the pump cards (Peter's isolation experiment): A = the standard
  template class chain, B = fixed 112 px with no variables. One look separates card
  rendering vs sizing CSS vs renderer quirks. Temporary — removed once the fleet button
  standard is validated.

## 2026.7.108 — ?view=mobile|desktop template override (validation tooling)

### Added
- `?view=mobile` (or `desktop`) on any page overrides the UA template pick — render the
  mobile template in a desktop browser for measurement/validation (deep-diving the
  W02.M button-height report).

## 2026.7.107 — build number on the mobile page badge + hub restructure

### Changed
- **Mobile page badge shows the build** ("W02.M · b107") — a stale webview render is
  now visible at a glance; ends the churn where CSS fixes chased a cached page.
- **Mobile hub** (Peter's order): one tile per row — Paddocks (was Irrigation),
  Pumps & Channels (was Pump Control); Automation removed from the grower hub;
  Setup section follows, also one per row. Layout rule inlined (cache-proof).

## 2026.7.106 — literal fallbacks on every sizing var (renderer-proof glove scale)

### Fixed
- Every `var(--pwm-btn-h…)` now carries its literal fallback (`, 112px` / `, 10px`) —
  a renderer that loses the :root custom properties (companion-app webview) still gets
  glove-scale buttons. The template variable still governs wherever vars resolve.

## 2026.7.105 — sizing template inlined into the page (webview cache immunity)

### Fixed
- The glove-scale variables (`--pwm-btn-h` etc.) lived only in app.css; a cached
  stylesheet in the companion-app webview left most W02.M buttons at their fallback
  size while the page HTML was fresh (Peter's retest). The template is now ALSO
  inlined in the mobile base `<style>`, so sizing survives any stylesheet caching.
  Leftover hard caps removed: 40 px adjusters at ≤400 px, 44 px relay minimum.

## 2026.7.104 — W02.M batch 2: glove-scale template + walk-found fixes

### Changed
- **Control sizing is now a TEMPLATE**: `--pwm-btn-h` (112 px, glove-operable) +
  `--pwm-btn-gap` (10 px) defined once in app.css; 23 W02.M controls read it. Doubling
  came from Peter hitting two 56 px buttons at once with gloves; future sizing is a
  one-line change. Remaining pages adopt the same variable in the consolidation pass.
- **Black text on every solid-colour button** (17 fills — the theme's pale `--ps-text`
  read blue on green/red).
- Constant/Duration each a full-width row (Constant first); date/time input clamped
  inside the card (intrinsic picker width overflowed) and at template height.
- Timer Start goes grey + inert while the countdown runs.

### Fixed
- **Armed green survived the fold**: when a shutdown/schedule fired, the panel closed
  but the button stayed green — the transition branch now strips the armed state (both
  buttons) as it folds.
- **Constant schedule fired a phantom shutdown countdown** (walk-caught): the fire wrote
  state='running' + stale duration for display with no countdown engine behind it — it
  counted to zero and stopped nothing. A constant fire now leaves the shutdown timer
  idle; two tests pin constant→idle and duration→real countdown. Confirmed workflow:
  manual pump start never auto-arms the shutdown; only an explicit Start or a Duration
  schedule counts down.

## 2026.7.103 — W02.M batch (Peter's mobile walk, 2026-07-20)

### Changed (fat thumbs + honest controls)
- **Heights**: START/STOP toggle 2x (112 px); every other control uniform 56 px (timer
  row, adjusters, shutdown/schedule, demand, mode, Fill, Save, gate-auto, service Reset).
- **Relays**: Camera/Light are full-width one-per-row buttons, name inside ("Camera — ON").
- **Armed colour language**: Set Shutdown / Schedule Start are solid red when off, solid
  green when armed (shutdown active AND scheduled) — no more transparent blue/yellow.
- **Timer "Reset" renamed "Turn Off"** (mobile + desktop) — it disarms the timer, never
  the pump (behaviour walk-confirmed).
- **Schedule**: Constant is the default and listed first; duration panel folded until
  Duration picked; active mode solid green. **An ARMED schedule follows the controls** —
  changing mode/duration re-arms it live (same start, new settings, debounced, toasted);
  walk-confirmed that post-arm changes were silently ignored before. Reload hydrates the
  controls from what is actually armed.
- **Fuel**: gauge text 2x, bar 1.3x; litres input full-width; below it Fill + / Set Total
  50/50 at 56 px. **New Set Total** writes the ABSOLUTE tank volume (dipstick correction,
  down or up) — board-first via set_fuel_level, DB mirror, audited as fuel_correction
  distinct from refuel; capacity-capped (`POST /api/pumps/{id}/set-fuel`).
- **Water Pumped** panel always renders below Running Hours and gains an all-time Total
  (stats payload total = total hours x flow).
- **Low-Supply Override**: its own box above Device info; full-width 56 px button with
  unmistakable text ("Override Low-Supply Protection" / "OVERRIDE ACTIVE — protection
  off, tap to restore").

## 2026.7.102 — mobile pages show their page number

### Fixed
- The mobile top bar's page-id badge (`W02.M` etc.) only rendered when a template defined
  its `page_id` block — only Bench Sim did. The base now falls back to the `page_id`
  context variable every page already receives, so every mobile page carries its number
  (prerequisite for Peter's batched mobile UI walk, 2026-07-20).

## 2026.7.101 — every desktop surface goes live off the stream

### Changed
- **W01 map streams valve positions**: bay door/drain buttons and gate markers patch from
  `/api/stream` deltas (matched by exact entity id — the live payload now carries
  `door_entity`/`drain_entity`/gate `entity`), repainted through the existing lightweight
  painters, throttled 150 ms. The board publishes every 1% — now so does the map (was 5%+
  jumps on the 3 s poll, freezes on the 10 s idle cadence).
- **Post-tap lag fixed**: a stream delta is the board's truth, so it releases the 3 s
  tap-lock — the door button shows OPENING the moment the relay engages instead of 3–13 s
  later (was making partial-position setting nearly impossible).
- **`PwmLive.kick`**: universal wiring for the remaining surfaces — any watched board
  reporting kicks the page's existing refresh immediately (throttled, bursts coalesce).
  Wired: W02 Pump Control (0.8 s), W03 Automation, W05 Pump Setup, W07 Sensors, W09 Bench,
  W09S Bench Sim, W10 Water Chain. Polls everywhere remain as reconciliation/fallback.

## 2026.7.100 — live position stream (SSE): positions update the moment the board reports

### Added
- **`GET /api/stream`** — Server-Sent Events fan-out of live entity deltas. One supervised
  upstream websocket to HA (`state_changed`), filtered to **registered PWM devices'
  entities only** (the stream can never leak the rest of the HA state machine), payload a
  strict whitelist: `{eid, state, position, operation}` — never an attribute dump. Session
  auth (viewer+), 15 s heartbeat, 8-client cap, slow clients dropped (EventSource
  reconnects natively — a phone waking at the gate just resumes). GZip exempted so
  buffering can't hold events.
- **`PwmLive` client** (desktop base): pages subscribe and patch elements in place. First
  consumer: W08 desktop — valve badges tick live during travel with zero re-render;
  the 60 s poll stays as reconciliation. Registry actuator entries now carry their full
  `entity_id` for exact delta matching (two boards can both have a `bay_gate`).

## 2026.7.99 — calibration moves into the expanded device card (aligned design)

### Changed
- **Actuator calibration now lives inside the device form's Actuators section**, directly
  under "+ Add actuator" — one line per actuator ("Bay Gate · travel 39.2s · count —
  [Calibrate]"), the three-step wizard expanding in place inside the expanded card (Peter's
  aligned spec 2026-07-19: single card per device, cal within it, nothing outside).
  Live actuators only — a just-added draft actuator shows "not on the board yet — Save &
  flash first" instead of a button. A 3 s live poll ticks the counted seconds while a
  calibration is active.
- The W08 desktop directory rows are back to clean single lines (the .96–.98 header
  chips and below-row wizard are removed — that placement was wrong; this partial is
  shared, so mobile's edit form gains the same section).

## 2026.7.98 — desktop W08: Calibrate lives in the device header row

### Changed
- One card, one line: the travel time and Calibrate/Cancel button sit in the device
  header row next to the valve badge; nothing renders below the header until a
  calibration is active, and then only the step text + its 2–3 buttons expand inside
  the card (Peter 2026-07-19, third iteration of this layout — this one's his spec).

## 2026.7.97 — desktop W08: calibration lives INSIDE the device card

### Fixed
- The actuator calibration section rendered as what looked like separate sibling cards
  under each device (own background/border/margins). Now plain divider rows inside the
  one device card — label · travel · count · Calibrate, wizard steps expanding in place
  (Peter 2026-07-19: one card per device).

## 2026.7.96 — calibration wizard on desktop W08 too

### Added
- **The actuator calibration wizard now renders on the desktop W08 directory** — same
  three-step flow, same guards, per actuator under each device card (the card header still
  opens the edit form). Peter's ask: cal is not mobile-only.

### Fixed
- Desktop W08 `loadDevices` no longer blanks the list with debug scaffolding on every 5 s
  poll (leftover "Fetching…/Response…/Got N devices" states wiped the DOM each refresh),
  and returns its promise so the wizard can chain a fresh read after calibrating.

## 2026.7.95 — W08 actuator calibration wizard (Peter's manual-switch procedure)

### Added
- **Guided per-actuator calibration on the W08 mobile card** — replaces the raw
  "Set Open/Close Position" buttons (whose unguarded press wrote the 4.3 s travel onto
  rb-01). Three steps, human on the ends, board holds the stopwatch:
  1. Seat the gate CLOSED (drive + operator confirm → close-cal zeroes the reference).
  2. HOLD the OPEN manual switch to physical full open — the board counts the drive
     (live readout from the 1.1.0 counted-seconds sensor); operator confirms → open-cal
     stores it (firmware refuses <5 s).
  3. Verify with a full auto stroke; stopped short → extend with the switch and
     recalibrate. Wild change vs the old value (>2× either way) warns and offers
     one-tap Revert; Done snapshots the board (FW-06 mirror) so a replacement
     board restores the cal.
- **Per-actuator command routes** (`act_cal_open/act_cal_close/act_open/act_close/
  act_stop/act_set_travel` + `actuator` slug): dual-actuator boards are addressable
  per gate; resolution stays device-scoped; the revert path enforces the same 5–600 s
  bounds as the board — PWM can never be the loophole around the firmware guard.
  Four pinning tests.

## 2026.7.94 — grower-shaped nav, mod-actuator 1.1.0 (cal guard + counted-seconds), registry friendly-slug fix

### Changed
- **Desktop nav restructured as a grower menu** (Peter 2026-07-19): Operations (Irrigation,
  Pump Control) on top, Setup in the middle, Development at the bottom. Automation (W03) and
  Water Chain (W10) move to Development — W10 until the HZ-03/04 bench runs prove the balance
  checker and its flags get a grower-facing route; Bench + Bench Sim stay dev-gated within it.
- **W01 door buttons show the position % at fully OPEN/CLOSED** (was only during travel).

### Firmware (mod-actuator 1.0.5 → 1.1.0 — flash canary-first via ESPHome dashboard)
- **Open Calibration is guarded**: a counted travel under 5 s is refused with a loud log +
  beep (2026-07-18: the button silently accepted a 4.3 s count on rb-01, capping every stroke
  at ~10% travel and compromising the No-WiFi dark-close — found live 2026-07-19, recovered
  by Peter's manual-switch cal: 39.2 s).
- **New per-actuator sensor `… Travel Position Seconds`** — the board's internal tfrom_s
  count exposed live; the W08 cal wizard's stopwatch readout, and travel numbers stop being
  invisible.

### Fixed
- **run.sh now ships EVERY firmware include** (hand-list missed all Rev 2 module files —
  grower boxes never received unified firmware updates).
- **Registry device-state map falls back to the friendly-name slug** — W08 cards and W09S
  device chips were entirely blank for boards whose friendly name doesn't carry the device
  name (pdev-b01/b02/b02-drain).
- **`/api/devices` now carries a per-actuator list** (slug, position, stored travel time,
  counted seconds, cal availability) — the W08 calibration wizard's data source.

## 2026.7.93 — channel gates commandable from the map (operations, not setup)

### Added
- **Gate markers on W01 are now an operations control**: clicking a channel-gate marker opens
  a themed popup with OPEN / STOP / CLOSE, dispatched through the existing guarded gate
  command endpoint (operator role, board-offline 409/502, gate_log + audit on real dispatch).
  Until now the only manual channel-gate path was the Test button on the setup pages
  (Peter's ruling 2026-07-19: gates are commanded from operations, not setup).

## 2026.7.92 — label-aware valve + depth resolution everywhere (unified boards)

### Fixed
- **Every valve read/command and depth read now resolves unified boards' label-named
  entities.** Unified (Rev 2) boards name entities after their LABEL (`Bay Gate` →
  `…_bay_gate`, `Supply Channel` → `…_supply_channel_depth`); a dozen call sites still
  matched only the legacy `actuator_1` / `1m_water_depth` / `depth_1` suffixes. Live on the
  bench 2026-07-19: W01 door buttons errored "valve not found" (rb-01 AND the bay boards),
  door state stuck grey/holding, and no depths anywhere (map badges, W09S, the depth chart —
  and, silently, the irrigation controller's own close-at-max read).
- New shared resolvers in `core/helpers.py`:
  `match_device_valve`/`resolve_device_valve`/`sync_resolve_valve` — exact `actuator_n`
  suffix first, else the device's ONLY valve; two labelled valves return None loudly rather
  than command the wrong actuator. `sync_resolve_depth_ent` — canonical suffixes then the
  labelled sensor, excluding raw/offset/secondary (mirrors devices/registry.py).
- Applied at: `/api/live` (bay supply/drain/gate valves + bay depth), `/api/command`
  (supply/drain door commands), `core/helpers.send_valve_command` (the irrigation
  controller's door), `get_bay_depth` (controller decisions + trace + poller),
  `automation/status`, `automation/demand`, `automation/gate_automation` (×2),
  `automation/irrigation._check_supply_depth` (now also unit-aware), `depth_poller`
  (now delegates to `get_bay_depth` — one depth convention), and the bench-sim engine's
  valve reader. Five new resolver tests pin the matrix.

## 2026.7.91 — bench-sim engine + water-balance readers go through the resolver

### Fixed
- **The sim engine couldn't see the open bay valve** — `_valve_open_frac`/`_pump_running`
  matched entities by device-name substring, and a board whose friendly name doesn't carry
  its device name (`pdev-b01` → `pdev_bay_1_*` ids) has no matchable substring at all: the
  irrigation controller opened bay 1's valve (post-.89 resolver fix) but the physics saw it
  closed, so no water ever moved. All three sim readers (`_valve_open_frac`, `_pump_running`,
  `water_balance._node_level`) now consult the warmed resolver cache first, keeping the raw
  scan as the cold-cache fallback; both `_tick` loops warm their device sets up front — the
  same warm-then-sync-resolve pattern live/demand/gate-automation/depth-poller already use.
  This also un-blinds the HZ-03/HZ-04 balance checker for those boards (its edge-activity
  and level sampling import these readers). Test pins all three via a warmed cache.

## 2026.7.90 — W01 live gate/pump markers (status colours + depth + drag) and honest flush-timer card

### Added
- **Channel-gate map markers show live status** (Peter's bench ruling 2026-07-19): green =
  open, red = closed, grey = board offline, with the gate's depth reading as text beside the
  icon. The `/api/live` gate payload now carries an `online` flag (board `binary_sensor.online`,
  defaults False), test-pinned.
- **Pump markers get the same colour language**: green = running, red = stopped, grey =
  offline (was: yellow running / grey otherwise, offline indistinguishable from stopped). The
  depth badge stays an independent reading — shown whenever the pump has a level, regardless
  of relay/online state.
- **Gate and pump markers are draggable** — drag-to-position persists via the existing
  partial-update PUTs (`/api/channels/{cid}/gates/{gid}`, `/api/pumps/{id}`), with save/fail
  toasts, same pattern as bay badges.

### Fixed
- **Flush-timer +/- looked dead while idle.** The card displayed `flush_timer_remaining`,
  which the controller only writes while a hold is running; the adjust endpoint (correctly)
  changes the configured duration — so on an idle bay every tap worked server-side and the
  number never moved. The card now shows the configured duration while idle (labelled HOLD
  TIME) and the live countdown while running (FLUSHING).

## 2026.7.89 — hassio_role back to manager (GET /addons 403 live-proven) + friendly-name entity anchoring

### Fixed
- **`hassio_role: manager` restored** — the one live check owed from v.86 came back negative:
  `GET /addons` returns **403 Forbidden** at `default` (Supervisor log evidence, 2026-07-19),
  which silently killed GIS/Core slug discovery → the paddock-boundary proxy degraded to an
  empty FeatureCollection → W01/W04 lost every paddock shape. Reverted per the pre-ruled
  recovery. Least-privilege follow-up stays open: Core pushes peer addon URLs over the
  existing access-sync channel, then PWM re-flips to `default`. The v.87 store-reg removal
  stands.
- **Entity resolver: third anchoring pass by declared friendly-name slug.** A board whose
  YAML friendly name never contained its device name (`pdev-b01` → "PDEV Bay 1" →
  `pdev_bay_1_*` entity ids) had NO entity carrying the device name, so resolution returned
  nothing — the bench-sim engine logged `no depth-offset entity on pdev_b01` every tick and
  `/api/live` was blind to all three bay boards. The resolver now falls back to the slug of
  the friendly name **read from the ESPHome directory** (flash-time truth, never HA-derived
  identity), with the same longer-sibling exclusion ("PDEV Bay 2" can never anchor onto
  "PDEV Bay 2 Drain"'s entities). Three pinning tests.

## 2026.7.88 — hub page lost the Bench nav on dev boxes

### Fixed
- **`/hub` dropped the Bench / Bench Sim nav links even with `admin_key` set** — the hub route
  in `main.py` builds its template context by hand and never passed `bench_enabled` through, so
  the sidebar's `{% if bench_enabled %}` saw undefined → falsy on the landing page (every other
  page goes through `pages._ctx()`, which includes it). Found live 2026-07-19 when the dev box's
  bench day started at the hub. Two pinning tests added (`test_bench_gate.py`): hub shows the
  links with the key set, still hides them without it.

## 2026.7.87 — remove store-repo registration from PWM (completes the least-privilege flip)

### Changed
- **`pat_manager` no longer registers the fleet's private Supervisor store repos** (Peter-ruled
  2026-07-19). A single addon should not register the whole fleet's private store, and the
  `POST /store/*` calls needed the `manager` role PWM dropped in v.86 (→ 403 at `default`).
  Store-repo registration is a one-time dev-box / Core setup concern, not PWM's runtime. Removed
  `_update_store_repos`/`_reload_store`/`_get_supervisor_pat`; `rotate_pat_on_startup` now only
  keeps git remotes clean (Rule 80) + configures the dev credential helper (both no-ops on a
  grower box). No more `/store` 403s at startup. **Completes the v.86 `hassio_role: default` flip.**

## 2026.7.86 — least-privilege: hassio_role manager → default

### Changed
- **`hassio_role: manager` → `default`** (Rule 160). Audit of every Supervisor call showed
  PWM's request path uses only `/core/api/*` (`homeassistant_api`) plus one `GET /addons` for
  GIS/Core slug discovery (`hassio_api` read); it never starts/stops/installs/updates addons.
  `manager` would let a PWM compromise control every addon on the box — dropped to the minimum
  that works. The dev-only `/store` registration (`pat_manager`) runs on dev boxes with a dev
  PAT and is not part of the grower runtime. Deploy-verified at `default`: v.86 healthy, `db_ok`,
  pages render; `POST /store/*` now correctly 403 (dev-only, grower unaffected). **Pending live
  confirm:** the grower `GET /addons` slug-discovery read is lazy (runs on a paddocks-page load) —
  confirm on the next map load; if it 403s at `default`, the paddock proxy degrades gracefully and
  the flip reverts in one line. **Dev caveat:** a fresh dev box can no longer self-register the
  private store via PWM at `default` (existing boxes already registered).

### Red-team
- Commercial-grade: security — reduced blast radius; a compromised PWM can no longer reach the
  Supervisor addon-control surface. Closes the last flagged item from the v.85 deep red-team.

## 2026.7.85 — deep pre-cut red-team: bench-sim hardware-reach + YAML secret-exfil closed

Deep pre-grower-cut adversarial pass (5 focused red-team agents over the software surface;
firmware boundary deferred to bench). Findings hand-verified, fixed, and regression-tested.
Suite 495 green.

### Fixed — security
- **HIGH — bench-sim API reached real hardware on a grower box.** The 8 `/api/bench/sim/*`
  endpoints checked role but NOT `bench_enabled()` (the gate `bench.py` + the `/bench/sim/`
  page already enforce). Via ingress (admin), a user could bind real pump/gate/bay boards
  into the sim paddock and arm the engine, which writes depth offsets to those boards —
  tripping the real irrigation/demand controllers into opening a valve / starting a pump.
  All 8 handlers now `bench_enabled()`-gated (404 off-bench); the water engine also checks
  `bench_enabled()` before any board write (defence in depth). `TestBenchSimGating` pins it.
- **MEDIUM — `${…}` substitution-reference secret exfil (Rule 175).** `_yaml_scalar` stripped
  quotes/backslash/control but not `$`/`{`/`}`, so a grower value like `${device_api_key}`
  survived and ESPHome resolved it into the board's friendly-name / notification text —
  leaking the per-device credential the key-name scrubbers can't catch once it's a resolved
  value. All four YAML generators now strip `$`/`{`/`}`. `TestYamlScalarSanitiser` extended.
- **MEDIUM — channel gate `write-yaml` still minted a phantom board.**
  `get_or_create_device_secrets` ran BEFORE `unknown_device_guard`, INSERTing the very
  registry row the guard checks for → an unknown device name minted `/config/esphome/<x>.yaml`
  (Peter's 2026-07-14 phantom-board class, still reachable via the endpoint). Secrets now mint
  only AFTER the guard passes. New end-to-end `TestChannelWriteYamlNoPhantom` (the prior test
  only exercised the guard in isolation and missed the bypass).
- **LOW — deactivate licence replay across restart.** The SEC-28 durable issued_at HWM
  guarded activate only; a captured signed deactivate could replay after a restart (in-memory
  nonce ledger cleared) and re-delete the licence, locking the grower out. Deactivate now
  anchors the same HWM. `TestSec28DeactivateReplay` pins it.
- **LOW — unredacted exception text buffered** (`record_error`) now runs through `redact_all`
  (latent: the buffer is one getter away from a diagnostics endpoint).

### Fixed — hygiene
- `requirements.lock` drift corrected (cryptography 48.0.0→48.0.1, python-multipart
  0.0.30→0.0.31 — the image builds from requirements.txt, so the lock was a stale SBOM).

### Red-team notes (flagged, not fixed here)
- `hassio_role: manager` is over-provisioned for the grower runtime (only dev PAT machinery
  needs it) — a PWM compromise inherits box-wide addon control. Recommend `default` for the
  grower image + dev-gating the PAT store ops. Needs a deploy-flow check (flagged, not flipped).
- Login rate-limit is per-username not per-IP; no in-app password change; `/health` exposes
  version + pool stats. All low; tracked.
- Confirmed strong: Leaflet CDN tags carry SRI + crossorigin, base image digest-pinned,
  pip-audit 0 CVEs, CSP nonce (no unsafe-inline in script-src), SQL fully parameterised,
  two-pool least-priv DB split (no request-path DDL), every scrub surface holds.

### Prior-batch ruling records (Peter 2026-07-19)
- R69 hash-pinning **waiver ratified**; R90 `SECRET_INVENTORY.md` added (unknown-and-fill-in);
  R196 mechanism = grower Data-Management UI (TODO, non-blocking); R198 Farm↔PWM ownership
  **ruled** (Farm owns bay geometry + infrastructure structure, PWM consumes + binds + operates;
  Farm-first, nothing removed from PWM until Farm's replacement is live).

## 2026.7.84 — fortnightly re-baseline: security leak closed + compliance gaps fixed

Fortnightly R103/R162 audit re-baseline (due 2026-07-19). Four read-only audit
agents (2 adversarial pen-test finders, 2 per-rule verdict re-verifiers) over the
whole tree; findings hand-verified and fixed. Red-team: security — a viewer-reachable
board-credential leak, closed + regression-tested. Commercial-grade: operability —
event-loop-blocking and shutdown-leak paths removed so an operator's box degrades
and restarts cleanly.

### Fixed — security (HIGH)
- **`/api/devices` + `/api/devices/{id}` leaked per-board OTA password + API key**
  (Rule 88/164) — both endpoints returned the raw `pwm_devices.yaml_vars` column,
  into which `esphome_secrets` persists `device_ota_password` / `device_api_key`,
  to ANY authenticated session incl. viewer (OTA-push + native-API control of the
  board). The .82 sweep scrubbed the parallel pump surface (`/api/pumps`,
  `/api/config-data`) but missed the device registry. New `redact_yaml_vars()`
  (shares the canonical `_SECRET_SUB_RE`) scrubs both reads; regression tests
  `TestDeviceRegistrySecretScrub` pin list + detail.

### Fixed — compliance / operability
- **Rule 121** — `api/paddocks.py` did blocking `httpx.get` inside async routes
  (`/api/paddocks/available`, `/api/paddocks-proxy`); both now run off the event
  loop via `asyncio.to_thread`. Last standing ❌ from the prior baseline.
- **Rule 134** — the shutdown handler claimed to cancel background tasks but only
  closed the pool; added `task_supervisor.shutdown_all()` (cancel + drain) and
  called it before `close_pools()`.
- **Rule 65** — mypy is clean (was ⊘ "not in sandbox"): fixed 4 `union-attr`
  None-narrowing errors (`api/live.py`, `automation/status.py`, `core/helpers.py`)
  + 1 missing cursor annotation (`pumps/tracking.py`).
- **Rule 32** — `/api/access/sync` (a grant-push mutation) now writes `log_audit`.
- **Rule 61** — response-envelope convention documented in `api/__init__.py`.
- **Rule 17** — removed raw hex reintroduced by the July sweeps: `#7c3aed` →
  `var(--ps-accent)` (mobile channels, incl. dead `var(…, #hex)` fallbacks),
  `#fff` → `var(--ps-btn-text)` (licence button).

### Docs
- **Rule 96** — CLAUDE.md route + schema tables re-synced to code (~40 missing
  routes added; table count 14 → 19).
- **Rule 196** — added `docs/DATA_RETENTION.md` (per-class retention policy).
  The purge *mechanism* for operational time-series (depth/gate/pump logs) is
  flagged pending Peter's retention ruling — deleting grower analysis data is a
  product decision, not a default.
- AUDIT.md re-baselined: fresh per-rule verdicts (R60 ⚠→✓, R41 941→125, R169/R177
  ⚠→✓, R65 ⊘→✓), added rows for R192–R198. Open gaps flagged for Peter/steward:
  **R69** (dependency artifact-hash pinning — fleet-wide), **R90** (no
  `SECRET_INVENTORY.md` — fleet-wide), **R196** (purge mechanism), **R198**
  (bay-ownership Farm↔PWM contradiction — needs P/G/Peter settlement).

## 2026.7.83 — Peter's rulings on the .82 flags

### Changed
- **Gate `depth_offset_cm` now applies to the reading** (Peter-ruled) — the W02
  gate card's live depth is sensor value + offset, same convention as bay
  `offset_val`. It is the column's only live consumer (the rule engine reads
  the `data.automation` sensors, not the gate's own `depth_sensor` column).
- **Default flush hold = 30 minutes (1800 s) everywhere** (Peter-ruled) —
  code paths, schema default, and migration 009 (`ALTER COLUMN … SET DEFAULT`)
  all agree; stored values, including a deliberate 0, are untouched.
- Irrigation controller's own `water_level_min/max` reads now honour a stored 0
  (same zero-swallow class as .82, missed in the controller itself).

## 2026.7.82 — all-pages UI/UX sweep: ~60 verified fixes in one batch (4-agent sweep, hand-verified)

### Fixed — silent safety disarms
- **W02 gate config Save / Auto-Manual toggle were server-side no-ops** — the gate
  PUT allowlist dropped `auto_mode` and every depth/actuator field; the toast said
  saved, the DB never changed, and auto mode could not be disarmed from W02.
- **Desktop W06 gate save wiped automation config** — full-replace of the `data`
  JSONB destroyed `pump_watch`, downstream/offtake automation, `automation_2` and
  `overflow_declined` on any rename/travel tweak. Now merges (`data_merge`).
- **W03 gate form disarmed overflow/pump-watch on every save** — it hydrated from a
  status payload missing half the fields, then wrote the whole object back. Now
  hydrates from the stored `data.automation` and round-trips.
- **W05 Save pushed `depth_1/2_offset: 0` to the live board** (desktop + mobile) —
  tuned sensor offsets zeroed on every save. The .81 min-depth null-guard is also
  ported to mobile.
- **Travel times in `data`/`data_merge` bypassed the FW-09 admin confirm** — the
  guard watched only the legacy columns. SCAL-05 overflow guard got the same
  `data_merge` blind-spot fix.
- **Dry-run/anti-short/emergency zero-swallows** — a deliberate 0 ("disabled")
  rendered as the default and was silently re-armed on save (W03, mobile W06,
  irrigation controller flush hold-time, status payloads).
- **W08 mobile bench controls were live on grower installs** — all bench UI now
  Jinja-gated on `bench_enabled`; `devCmdAsync` rejects on failure; the dry-run
  sequence restores min-depth in a `finally` and screams if the restore fails.

### Fixed — phantom success / wrong action
- **Gate commands** now 409 on an offline board and 502 when no entity accepted
  the command — no more "Command sent" + a gate_log row for a command that went
  nowhere. Gate button in unknown state labelled OPEN (it always sent 'open').
- **Demand level buttons hit an unregistered endpoint** (missing decorator) —
  demand level was never changeable from the UI; "(act 2)" demand gates also
  actuated the wrong valve (`:2` suffix now resolved, both demand paths).
- **~40 blind success toasts** across W01/W02/W05/W06/NT01 now check `r.ok`.
- **Past scheduled starts are refused server-side** (400) — a stale tab or skewed
  phone clock could start the pump immediately; unparseable schedule = 400 not 500.

### Fixed — security
- **`/api/pumps` and `/api/config-data` shipped per-board OTA passwords + API
  keys** to every logged-in browser (viewer included). Secrets scrubbed
  server-side; non-secret firmware fields still flow to the config forms.

### Fixed — broken features
- Pump START/STOP no longer latches disabled after an offline poll; desktop hero
  styling survives polls. W01 gate map markers read the right live dict; the
  depth-history chart draws (tz-offset parse). W07 add-sensor binds the bay's
  `level_sensor` (device derived from entity id). W04 Edit-Gate Save saves
  in place (MouseEvent-as-`replace` bug) and mobile W04 scrolls again
  (fullscreen opt-out). W03 collapses to one usable column on phones; trace
  pages get a real topbar + error state. NT01 Test now tests THE group,
  duplicate names 400 cleanly, fetch failure shows an error not the empty state.
  Stats "today/week/month" + water-order today run on box-local time, not UTC.
  Service items created via API render their names. Pump depth sensors read cm
  on both templates (server normalises by unit). `/api/paddocks/available`
  un-shadowed from the `{pid}` route. Sensor pickers on W05/W06 source from
  `/api/ha-sensors` instead of convention-built entity ids (renamed/unified
  boards no longer silently disarm rules); mobile W06 dropdowns no longer null
  desktop-configured sensors on save.
- **Mobile W05 rebuilt select-only** (one-door): write-yaml call, free device
  select and firmware fields removed; board assignment via the typed picker +
  assignment endpoint, matching desktop; structural test now covers mobile.
- Mobile W02 gains the Low-Supply section (min depth, override, last stop
  reason) — phone operators can finally see why a start was refused.
- W08 mobile: no more debug-text flashes or half-typed-input wipes on the 2 s
  reload; phantom Friendly-Name/Policy "saves" are read-only rows; cal 0 cm
  displays as 0; abandoned cal panels no longer pin fast polling.

### Notes
- 487 tests green (+80 new pinning tests across 7 new/extended files).
- Flagged for ruling: gate `depth_offset_cm` is read by nothing (left unapplied);
  flush hold-time default unified on 1200 s in code while the schema default says
  3600 (discrepancy documented, not silently changed).

## 2026.7.81 — bench close-out: refusal tracing + adjust re-arms backstop + box-close polish

### Fixed
- **Timer/schedule boxes close only on a real transition** (running/paused →
  idle, scheduled → fired). .80's unconditional close slammed the box shut
  while the operator was still setting a duration (adjust re-renders).
  Mobile's original transition mechanism restored.
- **Adjusting a RUNNING timer re-arms the board backstop** at the new
  remaining — adding time used to leave the board counting the old value,
  which would have `timer_expired` the pump hours early.
- **Refused starts now leave a trace**: log warning + audit row with source
  and reason ("Wait Ns" appeared on the phone; the log said nothing).
- mod-pump: `%u`/`uint32_t` format warnings silenced ((unsigned) casts).

### Added
- **W05 Low Supply card shows the guard's live comparison depth** (lowest
  sensor, offset applied) — stand in the field and tune the offset until the
  number matches the water.
- **Bench + Bench Sim are dev-only.** Grower installs (no `admin_key`) get no
  bench nav, 404 on both pages, and a refusing bench API — pinned by
  tests/test_bench_gate.py.

### Mobile (phone sweep)
- Relay 3/4 are standard square ON/OFF/N-A buttons (the switch-with-knob
  read as "a square with a circle in it").
- Refuel row no longer pushes the Fill button off-screen (number input
  gets `min-width:0`).
- /api/live relay resolution tries stored name AND board label AND canonical
  suffix — a stale DB name can no longer blank the buttons to grey '--'.

### Bench evidence (2026-07-18, pdev-test-pump, full validation)
- Start/stop pulses, aux relays by label, 10-min schedule → exactly one K2,
  backstop margin + clear, meters exact (10.2 L/hr to the decimal, runtime
  1:1, water from flow), dry-run refusal, anti-short-cycle refusal + recovery,
  No-WiFi cascade: beeper at 50%, dark stop at 100% offline,
  `wifi_disconnect` recorded, autonomous rejoin.

## 2026.7.80 — hotfix: W02 dead on load (duplicate const) + JS-syntax suite gate

### Fixed
- **W02 stuck on "Loading…":** .79's water-volumes render redeclared `waterEl`
  inside `loadPumpStats` — one SyntaxError kills the page's whole script while
  the server still returns 200. Renamed; every page I ship now passes
  `node --check`.

### Added
- **tests/test_js_syntax.py** — every template `<script>` block must parse
  (node --check); the dead-page-on-200 bug class is now pinned.

## 2026.7.79 — bench day 3: single-stop timers (mod-pump 2.0.1) + schedule/timer UX + water volumes

### Fixed
- **Double shutdown killed (both sides).** The board backstop is now armed
  with a 2-minute margin over PWM's primary countdown (it only ever fires if
  PWM is dead), and **mod-pump 2.0.1** makes the stop script idempotent — a
  second stop can no longer pulse the stop relay again (bench 2026-07-18:
  timer expiry fired K2 twice).
- **mod-pump 2.0.1: countdown at 5 s resolution.** The 60 s decrement on a
  phase-random tick could eat a whole minute instantly — a 60 s bench timer
  fired with 25 s on the clock. Worst case is now 5 s early.
- **Timer expiry resets, closes, and disarms.** Server: expiry resets the
  timer, flips `enabled` off and clears the board's leftover backstop count
  (a stale count would have `timer_expired` the NEXT run mid-stream). UI
  (desktop + mobile): the expired card actually closes (the old branch
  restyled the button but never hid the panel).
- **Schedule can no longer run a pump forever by accident:** adjusting the
  schedule runtime force-selects Duration mode (a stale Constant toggle
  silently discarded the runtime); runtime minimum lowered 600 s → 60 s to
  match the server. A fired schedule closes its box — one-shot (Peter's
  ruling, 2026-07-18).
- **W05 Save no longer reverts the board's Min Water Depth.** The +/- buttons
  write the board directly; Save then pushed the stale DB copy back — every
  save silently changed the safety threshold. Min depth is now only pushed
  when the form actually collected it (board offline/unassigned).
- **Relay 3/4 live states resolve by board label** in /api/live (same bug as
  the .78 command fix) — composed boards' aux buttons sat grey '--' forever.

### Added
- **Water volumes on the pump card** (today/week/month/YTD, run hours × flow
  rate) — the API always computed them; the card never rendered them.

## 2026.7.78 — bench day 2: labelled aux relays + W09 calibration staging + narrow-width fixes

### Fixed
- **Relay 3/4 commands work on unified boards.** The command resolver hunted
  for a literal `relay_3`/`relay_4` entity, but the builder names aux relays
  by their label (Camera, Light, …) — so every toggle 404'd on a composed
  board. The resolver now asks the board's own YAML for the aux label
  (aux 1 = K3, aux 2 = K4) and matches that, falling back to the canonical
  name for legacy monoliths. W09 buttons show the board's labels.
- **W09 narrow-width overflow:** card/detail text (unbroken device names)
  spilled outside the cards just above the sidebar-collapse breakpoint —
  cards and value cells now shrink and wrap (`min-width:0` +
  `overflow-wrap:anywhere`); the two-point cal boxes stack instead of
  squeezing.

### Added
- **W09 calibration staging display:** each Sample now shows the exact
  values Save will write to the YAML (volts + METRES — the cm→m conversion
  was invisible), and a staged-for-YAML line tracks both points and the
  selected slot live.

### Changed
- **W05 Config layout (follow-up):** Fuel Tank Capacity joins Flow Rate +
  Burn Rate in the left column so the Board card fills the full column
  height.

## 2026.7.77 — bench day: instant manual switch (mod-actuator 1.0.5) + W05 board-picker fixes

### Fixed
- **mod-actuator 1.0.5 — the manual switch responds instantly.** The 3 s
  reversal dead-time applied to EVERY start, including from standstill, so a
  hold-to-run press shorter than ~3.1 s never energised the relay — every
  manual press ever logged on rb-01 was under it. Dead-time is now
  reversal-only: energising opposite to motion that ran within the last 3 s
  waits out the remainder (anchored to when the opposing relay cut); cold
  starts and same-direction jogs drive on the next 100 ms tick. Slam
  protection for true reversals is unchanged. Bench-validated on rb-01
  (2026-07-18): cold jog instant, quick reversal waits, UI + 300 s
  close-hold regression clean.
- **W05: Save no longer silently discards a changed board picker.** Picking
  "— no board —" (or a different board) then hitting Save now applies the
  change through the dedicated assignment endpoint — still never a YAML
  write (structural test added).

### Changed
- **W05 Config layout:** Burn Rate (L/hr) moved under Flow Rate in a left
  column so the Board card gets the full stacked height (was squashed into
  one grid cell).

## 2026.7.76 — WR-PS-183: redactor re-vendored (all six GitHub token classes)

### Changed
- **The vendored log redactor re-synced byte-identical to the patched
  canonical**: `gh[posur]_` now masks `ghp_`/`gho_`/`ghs_`/`ghu_`/`ghr_`
  alongside `github_pat_` (WR-PS-183 completeness sliver). Shared test
  refreshed (+4 fixtures).

## 2026.7.75 — WR-PS-108 fleet flip: access-sync enforce ON by default

### Changed
- **Unsigned or invalid grant pushes are now rejected with 403.**
  `PWM_ACCESS_SYNC_ENFORCE` defaults ON (`=0` kill-switch — code-default
  pattern, grower boxes have no env plumbing). Core's signed pushes have been
  verifying and pinning since the receiver landed; this closes the warn-only
  window fleet-wide (WR-PS-108, Peter's go 2026-07-17). A `bound_fp` mismatch
  already failed closed before this flip.

## 2026.7.74 — WR-PS-108: access-sync verify-and-pin (§9-A.9 receiver)

### Added
- **WR-PS-108 / §9-A.9: the Core→add-on grant push is now verified-and-pinned.**
  Core signs every `POST /api/access/sync` with its box Ed25519 identity; this
  receiver now verifies the signature, authenticates Core's key against the
  `bound_fp` Admin signs into this add-on's licence (never bare TOFU), checks
  the freshness window and single-use nonce, and pins the key. A `bound_fp`
  mismatch fails closed ALWAYS — even in warn-only; an unsigned/invalid push
  is warn-only until `PWM_ACCESS_SYNC_ENFORCE` (the coordinated fleet flip).
  `bound_fp` is persisted from the activated licence. Copied from the
  SugarSense v2026.7.12 reference; 7 behavioural tests (forged signature,
  cross-target replay, nonce replay, expiry, fp mismatch).

## 2026.7.73 — WR-PS-179: re-vendored the log redactor from the fleet canonical

### Changed
- **`core/_log_redactor.py` is now byte-identical to the canonical
  `documentation/shared/log_redactor.py`** (G's GSM⊕Core superset) instead of
  the older Core-extended copy — PWM gains the portal/Resend/PII-key coverage
  GSM had, plus two upstream fixes (idempotent unquoted-label masking; named
  pattern wins over the generic label). API is a superset (`redact()` alias
  kept) so the entry-point wiring is unchanged. Shared 30-case behavioural
  test adopted in place of the older 19-case local one.

## 2026.7.72 — W04 mobile: Disable is no longer one-way

### Fixed
- **Disabling a paddock on the phone made it vanish with no way back.** It
  left the Enabled list, and the Available list excludes any known PWM record
  — re-enable existed only on desktop. The mobile page now has a Disabled
  section with an Enable button (`PUT /api/paddocks/{id}/enable`).

## 2026.7.71 — W08: an offline board is not actionable

### Fixed
- **Commands to an offline board claimed success.** HA answers 200 for a
  service call on an unavailable entity, so valve/cal/pump/relay commands on
  a dead board toasted "valve open" with nothing moving.
  `POST /api/devices/{id}/command` now refuses with 409 when the board's
  online sensor is not `on` (`ping` stays exempt — its purpose is asking),
  and the mobile card's board-touching controls go inert while offline
  (Edit device, notes and cal-save stay usable — they never touch the board).

## 2026.7.70 — W04: one door for gate writes — the map popup joins the row model

### Fixed
- **Map popup assignments silently reverted; popup-removed gates resurrected.**
  The popup Save/Remove and the paddock-header "+ Add Gate" still wrote the
  legacy slot columns, but slots are only a projection rewritten from the
  gate ROWS on every row edit — so a popup assignment vanished at the next
  edit, and a popup-removed gate came back. All three flows now go through
  the row API; the level sensor (a bay field, not a gate row) keeps its own
  door.
- **Markers now render from the rows.** Manual gates, `other`-role gates and
  3rd+ supply/drain rows — which the four slots can never carry — now show
  on the map instead of the gate list claiming "on map" over a blank spot.
  The bays payload carries the rows; popup connections resolve against them,
  and the Add Gate modal's "in use" flags count rows too.

### Removed
- **`POST /api/bays/{id}/gate-device`** — the slot-write side door, no callers
  left. The slot forms of `POST`/`DELETE /api/bays/{id}/gate` now accept only
  `level_sensor` and answer 400 with a pointer to the row API for actuator
  slots. Route-table and template tests pin the doors shut, the same way the
  no-in-app-OTA tests keep the flash endpoint from growing back.

## 2026.7.69 — W03/W04: the UI stops lying — live selection re-point + honest command results

### Fixed
- **The selected gate/pump panel froze at click-time under a green live dot.**
  Each poll replaced `gateData` but the selection still referenced the
  previous poll's object, so valve state, trace steps, "Current: X cm",
  faults and recent actions were redrawn every 5s from stale data (the same
  selection-race family as the W02 fix). The selection is now re-pointed at
  the fresh poll's object by id before re-render, and pump rules re-render
  on poll at all (they never did).

- **Eleven mutation flows toasted success without reading the response.**
  Gate test/toggle/delete, pump save/delete, gate full-config and rule-config
  saves (W03, both variants), and the map popup assign/remove + gate-row
  delete (W04): a 403 from a viewer role — or any 4xx/5xx — read as
  "Saved"/"Deleted"/"open sent". Every site now checks `r.ok` and surfaces
  the server's error text. This same pattern is what hid the v2026.7.64
  CSRF-DELETE bug for weeks.
- **A device-less gate's Test buttons claimed success forever.**
  `send_gate_command` returned silently on its four skip paths (no device,
  no supervisor token, board offline, dispatch failure) and the endpoint
  answered `{"ok": true}` regardless. It now reports whether the command was
  actually dispatched; the test endpoint answers 400 for a gate with no
  device and 502 for an undispatched command (behavioural tests pin all
  three outcomes).

## 2026.7.68 — W08 sweep: mobile type filter, frozen dot, offline badges

### Fixed
- **Mobile type-filter chips did nothing.** `render()` computed the filtered
  list and then rendered the unfiltered one — tapping "Pump" re-showed every
  device (or claimed "No devices of this type" while devices existed).
- **Mobile online-dot froze while a card was open.** The dot was rendered
  without an id, so the live poll could never update it, and the full refresh
  is suppressed while a card is open — a board dropping offline kept its green
  dot indefinitely. The dot now carries the same id convention as desktop and
  the poll updates it.
- **Offline boards kept live-looking valve badges.** The mobile live poll
  computed the stale flag and then didn't apply it; first paint on both
  desktop and mobile omitted it entirely. `pwm-stale` is now applied on paint
  and on every poll (offline = last-synced, explicitly flagged — Rule 0).

## 2026.7.67 — W07 sweep: silent depth TypeError, poll destroying open cards

### Fixed
- **A nonzero level-sensor offset silently killed the live depth badge.**
  `_resolve_live_depth` added `float + Decimal` (NUMERIC column) — TypeError,
  swallowed to `None`, healthy sensor rendered as offline `--`. Exactly the
  site the v2026.7.62 cast sweep missed; now cast like its fixed twin in
  `core/helpers.py`.
- **The 15s diagnostics poll repainted the whole page over the user.** Open
  bay cards snapped shut within 15s and a half-typed add-sensor entity ID was
  destroyed mid-typing. The rebuild now skips while a field is focused or an
  add-form is open, and expanded cards are carried across the repaint.

## 2026.7.66 — W04 sweep: mobile Place Device, remove-resurrection, un-cancelable placement

### Fixed
- **Mobile "Place Device" could never succeed.** It POSTed a route that does
  not exist (only DELETE `/api/devices/{id}/place` exists) and mangled TEXT
  bay ids through `parseInt()` → every Save toasted "Failed to place device".
  Save now goes through the real doors: supply/drain placements upsert the
  bay's gate ROW (the ratified write model — a direct slot write is silently
  reverted by the next projection), and the level sensor updates the bay field.
- **Removing a device's placement resurrected it.** The DELETE endpoint
  cleared the slot columns but not the gate rows they are projected FROM —
  the next row edit put the device straight back. The endpoint now clears the
  row assignment and re-projects (regression test added).
- **Cancel didn't cancel gate placement.** The banner's Cancel reset drawing
  state but left placement mode armed with a pending map-click handler — the
  next innocent map click silently placed or moved the gate. Cancel now
  disarms the handler, the mode flag, and the crosshair cursor.

## 2026.7.65 — W03 sweep: dead desktop live feed, unclickable channels and pumps

### Fixed
- **Desktop W03 never refreshed after first paint.** The 5s poll wrote to a
  `#live-dot` element that only exists in the mobile template — TypeError on
  every successful response, before any render ran (the catch threw on the
  same missing element). Desktop now has the dot, pinned to the topbar beside
  the page badge, and the live feed actually updates valve badges/rules/faults.
- **Channels couldn't expand; pumps couldn't be selected (both variants).**
  The card HTML emitted a duplicate `class` attribute
  (`class="lp-card" class="js-channel-card"`); browsers discard the second,
  so the click wire-ups matched zero elements. Attributes merged; a template
  hygiene test now greps every template for the duplicate-attribute pattern
  so this bug class cannot return.

## 2026.7.64 — every bodyless DELETE in the UI was CSRF-403'd; success toasts hid it

### Fixed
- **All UI delete flows silently failed with 403.** The CSRF layer required
  `application/json` on every /api/ mutation, but `fetch()` sends no
  Content-Type on a bodyless DELETE — so gate/bay/pump/notification-group
  deletes were rejected by the middleware while their success toasts (fired
  without checking `r.ok`) claimed they worked. One call site had already
  been hand-patched with the header, confirming this bites live.
  An HTML form cannot send DELETE at all, so the form-CSRF vector layer 1
  blocks does not exist for bodyless DELETE: it is now exempt from the
  content-type check ONLY — the double-submit token (layer 2) still applies
  to cookie sessions, and a DELETE that carries a body stays fully gated.
  Tests pin all three properties.
  *(The toast-without-`r.ok` pattern itself is batch 2 of the sweep.)*

## 2026.7.63 — W02 sweep batch 1: schedule timezone, phantom hours, expired-timer UX, refuel→board

### Fixed
- **Scheduled start armed in the wrong timezone (DANGEROUS).** The date picker
  sends naive local time; the server armed it as UTC — on this AEST box a
  schedule fired 10 h late, or IMMEDIATELY when the picked local time was
  still in the past as UTC. Clients now send explicit UTC
  (`toISOString()`, desktop + mobile) and reject past times; the server stamps
  any naive value with the box zone as a safety net. The scheduled banner
  also re-displays correctly after reload (TIMESTAMPTZ round-trip).
- **Hour meters counted while the pump was off.** `started_at` is TIMESTAMPTZ
  (psycopg2 returns datetime) but the stop path called `fromisoformat()` on it
  — TypeError on every stop since the port, so run sessions never closed and
  stats counted them to now() forever (12 dangling rows found and closed,
  March→July). Stop now closes ALL open sessions; a dangling session found at
  the next start is closed with zero duration, not phantom months.
- **Expired shutdown timer stuck at 00:00:00** — the only way to clear it was
  Reset (which also touches the pump/board timer). The panel now folds away on
  the running→idle transition and the button returns to "Set Shutdown".
- **Refuel never showed up.** The UI displays the board's `fuel_remaining`
  sensor, but refuel only wrote the DB copy. Refuel now pushes to the board
  (set `refuel_amount`, press its `refuel` button — ESPHome owns the live fuel
  counter); the DB row stays as the business record, and the toast says when
  the board couldn't be reached.
- **Pump START/STOP button shrank after the first live poll** — className
  rewrites dropped the sizing class (same class-clobber family as W01).

### Changed (mobile W02)
- Relay 3/4 toggles now reflect live board state, and show **N/A** when the
  board has no such relay entity (the Recycle Pump's test board has none —
  re-point it to the real pump board) instead of a dead-looking grey toggle.
- ⏲ Set Shutdown / 📅 Schedule Start buttons no longer look disabled.

## 2026.7.62 — W01.M: Home button + pinned tabs, fat-thumb buttons; Decimal sweep

### Fixed
- **Nonzero offsets would have broken every depth read.** The v2026.7.61 fix
  made setting an offset possible — but `water_level_offset` (Decimal) was
  added to float depths in api/live, the depth poller and core/helpers:
  TypeError the moment an offset became nonzero. All three now cast. Verified
  end-to-end with new tests: adjust API → DB (real Decimal) → live depth math.
- **Same latent Decimal bug killed elsewhere:** custom bay-sensor `offset_val`
  (a nonzero offset made the sensor read "unknown"), pump refuel (second
  refuel would 500 once `fuel_level` was nonzero), and pump service stats
  (any service-log row broke the stats endpoint).

### Changed (mobile W01)
- The tiny back arrow beside "All" is now a proper blue **← Home** button
  (theme `ps-mobile-home`, same as pump control).
- The tab bar (Home / All / paddocks) is **sticky** — it no longer scrolls
  away with the page.
- Settings +/- buttons are taller (68px) for field thumbs.

## 2026.7.61 — W01 settings +/- never worked: Decimal + float TypeError

### Fixed
- **Water Depth min/max and sensor-offset +/- buttons did nothing — ever.**
  `pwm_bays.water_level_min/max/offset` are NUMERIC, so psycopg2 returns
  `Decimal`; both adjust handlers added a float delta to it and 500'd on every
  tap (the client swallows non-ok responses, so the buttons were a silent
  no-op on desktop AND mobile since the endpoints were built — zero
  `adjust_depth_threshold` rows in audit_log confirmed it). Values are now
  cast to float before arithmetic.
- **A stored 0 was swallowed by the default.** `bay.get(col) or 5` turned a
  grower-set min of 0 into 5 before adjusting; explicit `is not None` check.
- 7 new regression tests exercise both endpoints against the real schema
  (positive/negative/fractional deltas, stored-zero, clamp-at-zero,
  persistence). Suite 384 green.

## 2026.7.60 — W01.M scroll actually works: opt out of ps-fullscreen

### Fixed
- **v2026.7.59's mobile scroll didn't scroll.** The W01 route sets
  `fullscreen=True`, and the theme master's `main.ps-fullscreen` pins `<main>`
  to `height:100vh; overflow:hidden` — so the control sheet (and the Settings
  button below the bays) was trapped under the fold. The mobile template now
  opts out (`{% raw %}{% set fullscreen = False %}{% endraw %}`, same
  context-override mechanism the template already uses); the map block sizes
  itself in vh so it never needed the fullscreen height chain. Theme master
  untouched. Desktop W01 keeps ps-fullscreen for map fit.

## 2026.7.59 — W01 batch 1: full-width buttons, settings cards, disabled-paddock badges, mobile scroll

### Fixed
- **Control buttons collapsed after the first live update.** The live-state
  pollers rewrote `className` on the mode rotator, supply/drain and bay-gate
  buttons, stripping the `pwm-flex1` width helper — buttons shrank to their
  min-width instead of spanning the card. `flex:1` now lives on the base
  classes (`.mode-rotator`, `.gate-cycle-btn`, `.bay-mode-rotator`) so no
  className rewrite can shrink them. Desktop + mobile.
- **All tab showed sensor badges for disabled paddocks** (e.g. SW7). Bay
  badges/polygons now render only for enabled PWM paddocks — a disabled
  paddock keeps its boundary polygon and nothing else.

### Changed
- **Settings panel: separate-card look per bay** — each bay row is a bordered
  card with a divider under the bay name (the +/- adjusters are unchanged).
- **Mobile W01 page now scrolls.** The map is a fixed-height block (38vh while
  the control sheet is open) and the sheet flows below it, so the buttons get
  real room instead of a 40vh internal-scroll strip.

## 2026.7.58 — Channel map leaf lands on the REAL W06 page

### Fixed
- **v2026.7.57's map leaf went to a dead template.** The desktop W06 route
  serves `config_channels.html` (the two-column page); `channels.html` was
  unreachable on desktop and has been deleted so edits can never land there
  invisibly again. The map leaf is now on the page you actually see: a **Map**
  button in the toolbar — draw the channel line (undo/clear/save), place each
  gate by clicking its spot (the editor's lat/lon fields update live), Esri
  imagery + GIS paddock boundaries underneath. Switching channels re-scopes an
  open map. Structural tests now assert against the live template.

## 2026.7.57 — Channel map leaf: draw the channel, place its gates (Peter-ratified)

### Added
- **W06 channel map** (per-channel, the W05-map-window pattern): every channel
  card has a Map button — draw the channel line point-by-point (undo/clear/
  save), place each gate by clicking its spot, Esri imagery + GIS paddock
  boundaries as backdrop (proxied, never authored — Rule 28). The line lives
  in the channel row (`data.path`, merged so the hydraulic `data.upstream`
  link survives); gate placement writes the existing latitude/longitude
  columns. Cards show "path drawn · n/m placed".
- **W06 creates channels outright** ("+ Add Channel") — the "set paddock type
  to Channel in the Registry" hop is gone.
- API: `PUT /api/channels/{id}` accepts `path` ([[lat,lng],…], validated,
  merged into data); `/api/config-data` and `/api/status` expose it.

### Fixed
- **W04: gate connections no longer depend on paddock selection** — clicking a
  gate before selecting a paddock said "no assignments" because the lookup only
  searched the selected paddock's bays; it now searches every paddock
  (coordinates are the identity). Peter diagnosed it on the bench.
- W05 pump form: the board picker overlapped the board name inside the narrow
  BOARD box — the picker now takes its own line.

## 2026.7.56 — Setup Map gate picker: typed bay boards only, and an honest empty state

### Fixed
- **The map's gate device picker uses the typed registry view** filtered to bay
  boards (`/api/esp-devices?board_type=riceboard`) — it was offering the raw
  ESPHome list PLUS every stale "referenced, no YAML" name, so long-deleted
  phantom devices haunted the dropdown (Peter, bench walk 2026-07-15). A stored
  assignment that no longer exists still shows, flagged "not found", so a bad
  record is visible rather than silently dropped.
- **No more silent black box**: a gate with no bay connections at its point now
  says so explicitly and suggests the fix (re-place the gate / check the bay's
  supply-drain slots) instead of rendering an empty panel.

## 2026.7.55 — Device Setup is ONE form: click a device, get the same wizard as + Add

### Changed
- **W08 desktop is one form** (Peter, bench walk 2026-07-15): the device list
  is now a directory — click a device and the SAME wizard form used by
  "+ Add device" opens on it. The old expandable card (stats, controls,
  calibration, test buttons, a second Settings form) is gone from this page;
  **testing and live operation are conducted on the Bench (W09)**, which
  already owns those tools. The list rows keep the live position badge and
  online dot (motion-adaptive, offline-flagged).
- **No more rival copies**: the card's old "Save Settings" wrote friendly name
  and disconnect policy into the registry — both are YAML-owned and now edited
  only through the builder. Registry **Notes** moved into the edit form
  (marked registry-only, saved with the same click, never a re-flash).
- Deep links (?open=) from Pump/Channel Setup now land directly in the edit
  form. Side panel + hub tiles renamed "Bay Device Setup" → "Device Setup".
- Mobile W08 keeps its operational card for now — it is the only mobile home
  of the bench tests; it gets the same one-form cut once mobile bench work
  has a home (Peter to rule).

## 2026.7.54 — Device cards: smooth position tracking, one truth per card, offline flagged

### Fixed
- **The card-header badge is live** — it was baked at render time with no
  element id, so a card could say "open 13%" at the top while the slider
  correctly showed 0% (bench, 2026-07-15). One card, one position.
- **Position tracking is motion-adaptive** (Peter's ask): ~1 s polls while any
  gate is moving (a 42 s travel steps ~2.4%/s — the old 3 s poll read as 10%
  jumps when aiming for a position), ~2.5 s while a card is open, 10 s at
  rest. Net fewer HA calls than the old steady 3 s, smooth when it matters.
- **Offline boards look offline**: position/state/depth values grey out with
  "OFFLINE — LAST SYNCED" instead of presenting stale numbers as live truth
  (the device-model rule: last-synced values are flagged, never current).
- Live updates no longer shrink the device list to the active filter chip.

## 2026.7.53 — Pump and channel pages only SELECT boards; building lives on the Devices page

### Changed
- **W05 (pumps) and W06 (channels) are select-only** (Peter-ratified, bench
  2026-07-15): the embedded board builder is gone from both. The pump form's
  Board row is now a typed picker + "Use this board" (the dedicated assignment
  endpoint — never a YAML write) + "Manage device →", which deep-links to the
  Devices page with that board open. W06's "+ Channel board" button is gone;
  the gate modal's board button now links to the Devices page too.
- This structurally kills the "pump edit form dies when its device was deleted"
  failure: a picker always renders; an embedded config form can't.
- Enforced by tests, not convention: the structural suite now asserts neither
  page mounts the builder, alongside the existing no-write-yaml guarantees.
- Legacy monolith write-yaml paths remain, labelled, until T9 retires them.

## 2026.7.52 — Building a board starts with "what will it do?" (type-first wizard)

### Changed
- **The device builder is now a wizard** (Peter-ratified, bench 2026-07-15).
  Step 1 asks what the board will do — pump / channel gate / bay — and that
  answer becomes the capability preset AND the YAML's `ps-board-type` header,
  so the type still lives in ESPHome and the role pages' typed pickers gate
  assignment off it. Step 2 is name + capabilities with the live budget cop;
  step 3 is a review of exactly what will be written — for new boards too, not
  just edits (previously only edits got the was→will-be confirmation).
- **W08 is now THE device page**: it lists every board type — bay, channel,
  pump, untyped — with filter chips and a type badge per card. Previously it
  showed bay boards only, so a pump board built here vanished from view.
- The builder's role is chosen at runtime, not baked per page: W05/W06 still
  open it pre-typed for now (their mounts retire next release when the role
  pages become select-only).

## 2026.7.51 — Mirror restore: the snapshot you picked stays picked

### Fixed
- **Snapshot dropdown selection survives the bench page's 5 s refresh** (bench,
  2026-07-15): the periodic entity refresh rebuilt the snapshot list and reset
  the selection to the newest snapshot, silently stealing the operator's pick
  before Restore could be pressed — with a corrupted newest snapshot, that made
  restoring an older good one a race against a 5-second timer. The selection is
  now preserved across rebuilds while the chosen snapshot still exists.

## 2026.7.50 — Mirror restore: every setting lands on its own entity (bench-caught)

### Fixed
- **Restore cross-write** (Hone FW-06 bench, 2026-07-15): the rename-proof entity
  matching accepted a single-word tail as identity, so the snapshot's No-WiFi
  Response Time (5.0) matched *"…time"* against Bay Gate Travel Time and silently
  overwrote the just-restored 42.2 — a mis-calibrated gate on what looked like a
  successful restore. The matcher now scores every candidate, exact id wins
  outright, the longest word-boundary tail wins otherwise (minimum two words),
  and an **ambiguous match fails loudly into the report instead of guessing** —
  a reported failure beats a silent wrong write.
- Regression tests: the exact bench cross-write, the ambiguity guard, and a
  twin-actuator board where each gate's travel time must land on its own gate.

## 2026.7.49 — Firmware: the gate's close-hold now actually releases (bench-caught)

### Fixed
- **mod-actuator 1.0.4** — the 300 s close-hold (positive end calibration, v1.0.3) never
  expired: on reaching the stop the hold cleared its move target to keep the relay
  energised, and the very next control tick treated that as a *manual jog* ("no target →
  never auto-stop") and returned before the expiry check — so the relay stayed on
  indefinitely, no recalibration, no release. The open-end hold was dead the same way.
  One-line fix: an ARMED hold (`hold_start_ms` set) now falls through the jog guard to
  the expiry check. Manual jog is untouched — every jog/stop path clears `hold_start_ms`.
- Caught live on the bench (2026-07-15, rb-01): first close-cycle run held the relay
  10+ min past expiry. Re-run on 1.0.4: hold expired at exactly +300.0 s, position
  recalibrated to closed, relay released. Hone FW-11 + HZ-02 bench evidence.

## 2026.7.48 — The board mirror: replace a dead board without losing its calibration

### Added
- **PWM now keeps a one-way backup of every board's live settings** (Hone FW-06). The
  board owns its calibration and policy in NVS — which is right, it keeps working when
  PWM is down — but that meant a dead board took its calibration with it. A slow
  background pass (every 30 min) reads each board's settings and stores a timestamped
  snapshot; **board → PWM only**, PWM never becomes a second writer.
- **Restore path**: replace the board, flash it with the same YAML, then
  **Bench → 5 · Settings Mirror → Restore** — offsets, travel time, No-WiFi action and
  response time, dry-run minimum all come back as they were. The restore matches
  entities by their **tail**, so it still lands when HA has slugged the replacement's
  entity ids differently.
- What's mirrored is every `number` and `select` entity a board exposes — exactly the
  firmware's operator-settable `restore_value` config, across all board types, with no
  per-module list to maintain. Readings (`sensor`) and momentary switches are not.
- Endpoints: `GET /api/devices/{id}/snapshots`, `POST /api/devices/{id}/snapshot`,
  `POST /api/devices/{id}/restore` (`snapshot_id` / `from_device`).

### Safety invariants (tested)
- An **offline board can never erase its own backup**: an empty read is never stored.
- An **unchanged board doesn't churn the history**: identical snapshots are skipped, so
  the history is a record of real edits, not a timer's heartbeat.
- A setting that can't be found on the replacement is **reported as failed**, never
  silently dropped.

## 2026.7.47 — The board owns its own metadata (no more rival copy in the pump row)

### Changed
- **`pwm_pumps` no longer holds the authoritative copy of board data.** It stored its own
  relay 3/4 names, depth-sensor names, start mode, pulse times, status pin and power
  source — a second writer alongside the YAML, and therefore guaranteed drift (the same
  disease that produced duplicate device rows). Those fields are now **derived from the
  board's YAML at read time** and overlaid on every pump read (`/api/pumps`,
  `/api/pumps/{id}`, `/api/status`), so what the UI shows is what the board actually has.
- Both firmware generations are understood: the unified `# ps-compose-spec` header
  (capability labels + pump block) and a legacy monolith's `substitutions:`.
- **Nothing is destroyed**: the DB columns remain and still answer for a pump with no
  board assigned, so an unconfigured pump still shows what it was last set to. The board
  simply wins whenever there is one.
- Each pump read now carries a `board_meta` block (`source: unified|legacy`, depths,
  relays, pump settings) for the UI to render from.

## 2026.7.46 — W05 rebuilt: the pump form can no longer touch a board

### Changed — three tiers, one owner each (Peter, 2026-07-14)
- **The BOARD's YAML is owned solely by the device builder.** W05's right-hand "Board
  Setup" column — a second, weaker editor for the same fields, and the thing that minted
  a phantom board from a half-typed name — is **gone**. The board is reached from a
  read-only summary row beside Flow Rate: device name, type, firmware, online state, and
  one button into the builder.
- **Assignment is its own act**: `POST /api/pumps/{id}/board` writes `pwm_pumps.device`
  and *nothing else* — it never touches a YAML, refuses an unknown board, and refuses a
  board of the wrong type. Inside the builder, choosing a different board **re-hydrates
  the whole form from that board**, so board A's settings can never be written into
  board B's file.
- **The pump save is pure business config** — name, type, flow, fuel/kW, service items,
  demand, notes. It carries no device, no relay/sensor names, no firmware fields, and it
  **no longer calls write-yaml at all** (it used to, unconditionally, on every save).
  Enforced by a test that greps the page for the call.
- **Diff before write**: saving a board in the builder first shows *was → will be*
  ("Depth sensors: Pit Depth → Pit Depth, Channel Depth · Spare relays: none → Camera")
  and requires a confirming click. Editing anything invalidates the pending diff.
- **Layout compacted**: left = the pump (details, service, notes, bench); right = live
  board settings + what this pump watches (Live Settings, Upstream Gate Control,
  Auto-Stop, Depth Calibration).

## 2026.7.45 — Saving a form can no longer invent hardware

### Fixed
- **Saving the pump form regenerated its board's YAML — and when the pump still pointed
  at a board that no longer existed, that WROTE THE GHOST BACK into `/config/esphome`**,
  resurrecting it as a real file and re-creating the duplicate on the next Discover
  (Peter, bench: "yes it updated it in ESPHome when I saved the form"). The pump and
  channel-gate write-yaml paths now refuse (409) to MINT a YAML for a board that has
  neither an ESPHome file nor a registry row: *"'x' is not a known board — pick the
  board this belongs to, or build it with the device builder."* Regenerating a KNOWN
  board is unaffected.
- **W05's ESP Device control is a real dropdown.** It was a free-text input with a
  `<datalist>`, which only whispers suggestions as you type — so with a stale value it
  showed no list at all ("no select list"). Boards are created with the device builder
  now, so this control only ever needs to *choose* one.

## 2026.7.44 — Device identity comes from ESPHome only (the duplicate-rows root cause)

### Fixed
- **Every renamed board minted a SECOND registry row** — 11 rows for 7 boards on the
  bench, and two cards per device. Discover derived device names from two sources: the
  ESPHome YAMLs *and* HA entity ids. HA builds entity ids from a device's **friendly
  name**, so "PDEV Bay 2" became a phantom row `pdev_bay_2` even though the board's
  device name is `pdev_b02`. Identity now comes from ESPHome **only** (HA remains the
  source of live state, never of identity) — phantoms cannot be minted at all.
- **Existing phantoms are merged, matched by friendly-name slug** (the old containment
  test missed them entirely — `pdev_bay_2` doesn't contain `pdev_b02`). References are
  re-pointed to the real board, then the phantom row is deleted.
- **Most-specific match wins**: "PDEV Bay 2" slugs to `pdev_bay_2`, which is also a
  prefix of `pdev_bay_2_drain` — a greedy match would have re-pointed the DRAIN board's
  references at the SUPPLY board. Caught by dry-running the bench's real rows before
  release; regression-tested.

## 2026.7.43 — ESPHome is the source of truth for the device table

### Changed
- **A board that isn't in ESPHome is deleted from the device table** (Peter's ruling,
  2026-07-14). Discover previously KEPT a vanished board if some pump/gate/bay still
  referenced it — which is how a renamed-away board (`peter_test_pump`) kept haunting
  the pickers. The dangling reference is now REPORTED instead ("this pump points at a
  board that no longer exists"), which is honest; a ghost that impersonates a working
  board is not.
- **Rename-phantoms are merged, not duplicated.** HA slugs entity ids from a device's
  friendly name, so one board also appeared as `precision_water_management_<name>` —
  two cards for one physical board. Discover now folds the phantom into the real
  device, re-pointing every pump / gate / bay / bay-gate reference first, then deletes
  it. A name that merely *differs* is never auto-merged — it could be another board.

### Fixed
- **W05's Discover didn't refresh the device picker** (desktop and mobile): it reloaded
  the registry but not the list the dropdown reads, so a board Discover had just found
  could not be selected until a full page reload — Peter's "only peter_test_pump is
  available after discover".
- **W05 now shows stale references** in a banner after Discover, naming the pump and the
  board that no longer exists.

## 2026.7.42 — W04: the sidebar no longer flickers while panning the map

### Fixed
- **Panning W04's map made the sidebar pop in and out** (and showed a strip of page
  background). `#map` is a flex item, and a flex item defaults to `min-width:auto` —
  it cannot shrink below its own content width. Leaflet keeps loaded tiles in the DOM
  while you drag, so the map's intrinsic width outgrew the row and shoved the sidebar
  out; when Leaflet pruned the tiles it snapped back. Clamping the flex item
  (`min-width:0`, plus `overflow:hidden` on the row) makes the map obey the layout
  regardless of how many tiles are in flight. Tile images are also barred from
  starting a native drag ghost.
  *(Seen worst on satellite — those tiles are slow and linger — but it happens on any
  layer. Maps that are absolutely positioned, like W01 and Farm's events map, were
  never affected: they cannot push a sibling. Farm's boundary map has the same flex
  pattern and needs the same one-line fix.)*

## 2026.7.41 — Bay gates are ROWS: unlimited per bay, and editable

### Added
- **`pwm_bay_gates` table** (migration 007 + backfill): a bay's gates are now rows —
  any number, each with a role (supply / drain / other), device, map position and an
  **automated** flag. The old model had exactly four fixed slots, so a 5th gate had
  nowhere to live, a plain grower-operated gate with a device had no home, and a gate
  could not be **edited** — only cleared and re-added (Peter, 2026-07-14).
- **Edit a gate in place** on W04: pencil icon on every gate row opens an editor
  (name, role, order, device, automation on/off) with "Re-place on map"; "+ Add Gate"
  inside the bay editor adds directly to that bay.
- **Non-automated gates**: switch automation off and the gate still gets a device and
  a map pin — the grower drives it by hand and the controllers ignore it entirely.

### Changed
- **The four slot columns remain the automation's read path** and are rewritten from
  the rows on every change (primary supply/drain → `supply_1`/`drain_1`, second →
  `_2`). Irrigation, demand, gate automation, live, status and hydro_graph keep working
  untouched — verified by tests asserting the projection, including that a
  non-automated gate NEVER projects into a controller-read slot.

## 2026.7.40 — Bench UI walk-through, round 1 (W04 + the device builder)

### Fixed
- **W04: "Redraw Boundary" showed no vertices — a bay's shape could not be edited at
  all.** `L.geoJSON()` returns a layer GROUP; `.editing` lives on the polygon inside it,
  so `editing.enable()` was a silent no-op. It now resolves the child polygon.
- **W04: the bay-editor header wrapped** ("K09B01 test" collided with the buttons). The
  Back / Add Gate actions now sit on their own row with the paddock › bay name below.

### Changed
- **W04: not-enabled paddocks read like Farm's boundaries** — bold solid orange outline,
  transparent fill (they're what you come here to enrol, so they should be the easiest
  thing to see); enabled paddocks recede so their bays carry the colour.
- **Device builder: every relay and analog input is now named.** Actuator rows show
  their relay pair (K1/K2, K3/K4), depth rows show A1/A2, soil shows its analog pin,
  and the spare-relay button names the exact relay it will assign ("+ Add relay K3") —
  no more guessing which physical terminal a row maps to.
- **Wording:** "If it loses the controller" → **"Action when WiFi drops"**;
  "…after (minutes, 0 = never)" → **"Time before action (minutes)"** with an explicit
  note that 0 = never act and that "Hold" does nothing either way.

## 2026.7.39 — One device table, one sync (Peter's consolidation)

### Changed
- **`pwm_devices` is now THE device table and Discover THE sync.** `/api/esp-devices`
  is a thin typed view over the registry (it used to assemble its own three-source
  union — why pages disagreed about which boards exist); `/api/devices` gains a
  `?board_type=` filter. Both carry `device_name` AND `friendly_name`.
- **Discover fixed four ways:** new rows no longer default to `riceboard` (a raw pump
  was mislabelled a bay and invisible in every pump picker); renamed boards no longer
  mint phantom rows (`precision_water_management_pdev_test_pump`); raw boards are
  detected via the real `wifi_signal_db` suffix (the old `_wifi_signal` matched
  nothing); vanished-but-referenced devices are now REPORTED as `stale_refs` instead
  of silently kept (how peter_test_pump haunted the pickers).
- **Dead "Generate" button removed from W06** — it POSTed `/api/generate`, an endpoint
  that doesn't exist in standalone PWM (Server-era remnant; all automation runs inside
  PWM's controllers, nothing is copied to HA).

## 2026.7.38 — Bench fixes: commands on renamed/unified boards, instant offsets, 3 s reversal

### Fixed
- **Every PWM command on rb-01 failed "entity not found"** — two stacked causes:
  the entity resolver anchored by `startswith(device_name)` (HA had friendly-prefixed
  every entity: `precision_water_management_pdev_rb_01_*`), and the command table used
  legacy suffixes (`actuator_1`) while unified boards name entities from their labels
  (`bay_gate`). The resolver now falls back to embedded-marker anchoring with a
  sibling guard (pdev_b02 can never anchor onto pdev_b02_drain's entities and drive
  the wrong board — test-asserted), and valve/calibration commands carry unified
  fallback suffixes.
- **Depth offset appeared to do nothing**: it was applied BEFORE a 15-sample median at
  a 60 s interval, so a change was outvoted for 8–15 minutes. mod-depth 1.3.0 applies
  the offset AFTER smoothing in a template sensor that republishes the instant the
  offset changes. (OTA re-flash to apply.)
- **Valve % on PWM cards now glides** between the 3 s polls instead of stepping ~7 %.

### Changed (firmware — OTA re-flash to apply)
- **mod-actuator 1.0.3: reversal dead-time 500 ms → 3 s** (bench-felt on the real
  actuator; 500 ms still slammed the mechanism).

## 2026.7.37 — W05 bottom-half redesign: honest per-gate demand config + compact Live Settings

### Changed
- **Live Settings compacted**: Low Supply and Anti Short-Cycle sit side-by-side as
  mini-cards; sensor offsets are two tight single-line rows with the live reading inline.
  The prose paragraphs moved into the `?` help-tips.
- **Upstream Gate Control rebuilt**: an "add a gate…" dropdown replaces the checkbox
  tiles (which double-fired their toggle handler — the highlight and the actual checkbox
  went out of sync, Peter's "can't select gates properly"). Each added gate is a small
  contained card with **its own** sensor + LOW/HIGH open/close thresholds — a
  pump-centric window onto the gate's Pump Watch config, the settings the gate
  automation actually evaluates. New `POST /api/channels/{cid}/gates/{gid}/pump-watch`
  merges only that block so W05 can never clobber the rest of a gate's automation.
- **Dead config deleted**: the pump-level "Low/High Demand Close At" globals were stored
  and displayed but consumed by NOTHING — a decoy next to the real per-gate model.
- **Auto-Stop Monitoring**: same add-from-dropdown pattern with removable chips;
  flood max + sensor on one compact row.

## 2026.7.36 — Water-balance checker: stage 2 (cross-sensor corroboration, HZ-03)

### Added
- **Balance checker** (`automation/water_balance.py`, supervised, 1-min tick): walks
  every hydro-graph edge with a 15-minute ring of each node's level + control state.
  The contradiction rule is deliberately conservative — only a FULL window of open-inlet
  samples with demonstrable upstream water can flag: *"inlet open all window, upstream
  has water, level moved +0.0 cm — possible stuck sensor or no flow"* — the HZ-03
  over-fill signal, from sensor corroboration, never time-as-sensor (Peter-ratified).
  Also flags sensors that never report in a window (stale-sensor, the HZ-04 case).
- **Inform + trace only**: verdicts persist to `pwm_config` and log a WARNING; nothing
  is actuated and nothing notifies in v1 (grower owns the system).
- **W10 shows it live**: a "Balance flags" card at the top and a per-edge status chip
  (ok / inactive / indeterminate / contradicted / stale-sensor) on every chain row.
  `GET /api/hydro/balance` serves the latest evaluation.
- Bench validation path: run a Flush on the rig with the water engine armed, then stop
  the engine's writes to one bay (freeze its "sensor") — that edge must flag within a
  window. This is the HZ-03/HZ-04 register evidence.

## 2026.7.35 — Water Chain (W10): the hydraulic graph — stage 1 of the water balance

### Added
- **`/water/` page (W10, new sidebar entry under Operations)**: the farm's water chain
  drawn per pump — pump → channel → gates → bays — assembled from what the rows already
  declare (pump demand config, gate automation downstream lists, bay↔gate links), every
  edge tagged with where it came from. Nodes not yet reachable from a pump are shown as
  their own island; "Upstream gaps" lists every node with no known water source, with an
  inline picker to set the link.
- **`GET /api/hydro/graph`** — nodes (with their sensor/control devices), derivation-
  tagged edges, and gaps. **`POST /api/hydro/upstream`** — set/clear an explicit
  `data.upstream` link on any pump/channel/gate/bay; explicit links fill gaps and never
  overwrite what the demand/automation configs already derive.
- This is stage 1 of the HZ-03 direction Peter ratified (cross-sensor flow corroboration,
  not time guards): stage 2 walks these edges against `pwm_depth_log` slopes; the bench
  rig's chain is the validation bed.

## 2026.7.34 — Firmware: positive close calibration + per-board Wi-Fi drop test

### Changed (firmware — OTA re-flash to apply)
- **mod-actuator 1.0.2 — close-end hold is now 300 s and its expiry is a positive end
  calibration** (Peter's design intent, ratified 2026-07-14): a close command drives the
  actuator into its own internal limit switch (motor current already cut there — only the
  relay coil draws during the hold); when the 5-minute timer fires the actuator is by
  definition hard against the closed stop, so the position re-zeroes — the gate
  recalibrates itself to closed on every full-close cycle. Open-end hold keeps the short
  one-travel release (no calibration value in holding open).
- **mod-disconnect 1.0.1 — "TEST Drop WiFi (policy test)" button** (diagnostic entity):
  drops that ONE board's radio so the No-WiFi fail-safe (HZ-01) can be bench-proven
  per-board without killing the AP (which would blind HA and every other board). The
  radio re-enables itself after Response Time + 3 min — a stray field press can never
  strand a board.

## 2026.7.33 — Live state for unified boards + full builder on mobile + actuator dead-time

### Fixed
- **Device cards were blind to unified boards' live state** (no valve %, depth, offsets,
  soil, manual switches): the enrichment string-built entity ids from
  `<device>_<legacy-suffix>`, but HA slugs ids from the device's CURRENT friendly name
  (rb-01 landed under `precision_water_management_pdev_rb_01_*`) and unified entities are
  label-named (`bay_gate`, `bay_depth`). Enrichment is now prefix-agnostic and matches
  unified names, with sibling-name guards (pdev_b02 never swallows pdev_b02_drain).
- **W09 Bench §1 showed no firmware / Wi-Fi** for renamed or unified boards — same prefix
  assumption in the `/entities` suffix map, plus `hw_core_version` was missing from the
  firmware-version candidates.
- **Firmware: actuator reversal dead-time 80 ms → 500 ms** (mod-actuator 1.0.1). A
  direction change slammed the motor from open to close with no perceptible pause; both
  relays now stay off for half a second before the opposite direction energises.
  Boards need an OTA re-flash to pick this up.

### Added / Changed
- **"Configure Board (actuators / sensors / YAML)"** is now the FIRST section on every
  bay-device card — desktop and mobile — opening the full builder (it was a small button
  buried under Settings; Peter couldn't find the full edit form).
- **Mobile Bay Devices gets the full builder** (shared partial): add and edit bay boards
  from the phone, same edit-from-YAML hydration as desktop.

## 2026.7.32 — Device identity comes from the FILE, not the filename

### Fixed
- **A YAML file whose name doesn't match its `device_name` no longer hides the board.**
  `mainchannel-01.yaml` carried `device_name: "pdev-mc-01"`, so every picker listed a
  phantom "mainchannel_01" and the real pdev-mc-01 was invisible. The ESPHome directory
  scan now reads the device's real name from the file's `device_name` substitution
  (filename is only the fallback), and the compose-spec / yaml-subs read paths resolve
  hand-copied files by content. The stray bench file was also renamed to the canonical
  `pdev-mc-01.yaml`.

## 2026.7.31 — W06: fresh device pickers + unified-board structure hydration

### Fixed
- **Gate/pump modals now refresh the device list from ESPHome every time they open**
  (registry + ESPHome dir + HA) — a board built seconds earlier appeared only after a
  full page reload, so PDEV MC-01 was invisible in the MC-01 gate picker.
- **Selecting a unified (Rev 2) board in the gate modal loads that board's structure**
  from its compose spec — actuator count, labels, travel times, ganging, depth sensor —
  so the gate config that drives automations matches what the board really is (same
  behaviour the pump page already had). Hardware changes still go through
  "Edit board YAML".

## 2026.7.30 — W09.S Bench Simulation: the permanent 5-board rig harness

### Added
- **Bench Sim page** (`/bench/sim/`, desktop + mobile, sidebar entry): binds the 5-board
  rig (pump, channel gate, 2 bay supplies + optional drains) to a permanent, explicitly
  flagged test paddock "PDEV Bench". The page is the scenario driver and evidence
  recorder — **operator actions happen on the real PWM pages** (Irrigation, Pump Control,
  Pump/Channel Setup), so every scenario certifies the production buttons a grower will
  actually press, on desktop and phone.
- **Water engine**: a supervised background loop that simulates water on the dry bench by
  walking each board's depth-offset entity from the boards' REAL state — pump running
  fills the channel, an open bay supply moves channel water into the bay, drains and the
  channel gate empty. Writes go via HA `number.set_value` (ESPHome stays the source of
  truth); configurable flow rates; only ever touches rig devices, only while armed.
- **Scenario scripts with an evidence trail**: Flush fill, Demand pumping, Overflow
  protection, No-WiFi failsafe. Each step names the real page to work, records pass/fail
  with a timestamped water-level snapshot; finished runs are filed (last 20) — this is
  the T10 bench-acceptance record, rerunnable before any future release.
- Test paddocks are badged **⚠TEST** on the Irrigation page (`is_test` via
  `/api/status`); notifications stay live for test entities on purpose — the
  notification path is part of what the bench proves.

### Fixed
- **Mobile pages lost all their JavaScript** (devices, channels, automation, licence):
  they declared a `scripts` block the mobile base never rendered. Found building W09.S —
  exactly the class of defect the bench's mobile-UI testing exists to catch.
- Mobile Bay Devices page title corrected (was still "ESP Devices").

## 2026.7.29 — Pump/channel board builders + YAML-file truth everywhere (bench prep)

### Added
- **The unified device builder is now a SHARED partial** (`pages/shared/_compose_builder.html`)
  mounted role-locked on three pages: W08 Bay Devices (bay), W05 Pump Setup ("+ Pump board
  (KC868-A4)"), W06 Channel Setup ("+ Channel board") — so all five T10 bench YAMLs
  (1 pump / 1 channel / 3 bays) can be generated and edited from the new Rev 2 generator.
- **`GET /api/devices/{id}/yaml-subs`**: parses the device YAML file's substitutions block
  (per-device credentials redacted server-side, FW-03). The W06 gate modal and both pump
  forms now overlay these FILE values over the row copy on open/device-select — the form
  shows what the board was actually built with, never a stale row or a UI default.
- The legacy fallback in `GET compose-spec` now hydrates from the file's substitutions too
  (labels, travel times, gang, depth cal, disconnect policy) instead of role presets.
- Gate modal + pump hardware section gain an "Edit board YAML" hand-off into the builder;
  unified boards get an explicit "edit with the builder" notice.

### Fixed
- **Legacy write-yaml can no longer clobber a unified board**: the pump, channel-gate and
  rb write-yaml endpoints refuse (409) when the target file carries the Rev 2
  `# ps-compose-spec` header — unified boards are edited through the builder.
- **Firmware: ESPHome 2026.7 breakage pre-empted** — `id(no_wifi_action).state` (deprecated
  Select accessor, removal announced for 2026.7.0) replaced with `.current_option()` in
  `mod-actuator.yaml`, `rb-hardware.yaml` and `channel-hardware.yaml` (4 sites). Today's
  builds compiled with warnings; next ESPHome would have failed.

## 2026.7.28 — W08.B: bay-only device page + edit-from-YAML (bench prep)

### Changed
- **W08 is now the Bay Devices page** (matching its "Bay Device Setup" nav label): the device
  list shows only bay boards (`riceboard`, plus untyped boards tagged "unknown board type" so
  they aren't stranded); pump and channel boards live on their own pages. The pump-only card
  sections (pump control, fuel, dry-run safety, pump bench sequences — all owned by W09 Bench)
  are gone from this page.
- **The builder is bay-locked**: role picker and pump section removed from the W08 compose form.

### Added
- **Edit Device (YAML)** on every bay card: opens the SAME full builder form, hydrated from the
  spec recorded in the device's YAML file — never from UI defaults (Peter, 2026-07-13). Save is
  a full deterministic regenerate through `/api/devices/compose`; the toast says whether the
  YAML actually changed (re-flash needed) or not.
- Generated YAML now carries a one-line `# ps-compose-spec:` header (the builder body, JSON) so
  the FILE is the hydration source of truth; `GET /api/devices/{id}/compose-spec` reads it, falls
  back to the registry copy, and maps legacy monolith boards to a reviewed-before-save preset
  with an explicit re-flash / relay-wiring warning (open=K1 / close=K2).
- Fields the form doesn't show (per-sensor calibration, travel seeds, update intervals) round-trip
  through edits via a base-spec merge — a save can never silently reset bench calibration.

## 2026.7.27 — Validate pump_status_pin before flashing device YAML (Hone PS-APP-09)

### Fixed
- **`pump_status_pin` (a free-text form field) was interpolated straight into flashed device YAML**
  (`pump_status_pin: "<value>"` → ESPHome `number: ${pump_status_pin}`), so a value carrying a
  quote / newline / colon could inject arbitrary device config at flash time. Now allowlisted to a
  safe ESPHome pin token (`${...}` substitution ref or `GPIO<n>`): the write-yaml endpoint 400s a
  bad new value (operator sees what to fix), and `_build_pump_subs` sanitises any value (incl. a
  legacy one already in the DB) to the `${D1}` default so nothing unsafe reaches the YAML.
  `tests/test_app09_pin_validation.py` (18).

## 2026.7.26 — Core-parity hardening: rate-limit, body-size, durable replay (Hone SEC-23/24/28)

### Fixed
- **SEC-24 body-size guard hardened** — a non-numeric `Content-Length` no longer raises
  ValueError → 500 (`.isdigit()` guard), and a chunked body (no Content-Length) on a mutating
  method is refused 411 so the 10 MB cap is always enforceable. Was Content-Length-only.
- **SEC-23 sensitive-endpoint rate limiter added** — per-IP sliding window (12/min) on
  `/api/licence/{activate,deactivate}`; PWM previously had NO limiter on its /23-reachable POST
  surface (only the per-username login window). Ported from Core.
- **SEC-28 durable replay guard added** — a per-`licence_id` `issued_at` high-water mark persisted
  in `pwm_config` refuses a signed licence that isn't strictly newer, so a captured artifact can't
  replay across a PWM restart (the in-memory nonce LRU resets then). Unsigned/legacy payloads under
  the enforce kill-switch are unaffected (nothing to anchor); fail-closed on a DB error.
  `tests/test_pwm_parity_hardening.py` (6, behavioural).

## 2026.7.25 — Log redaction added (Hone SEC-17 / KEY-01 / DATA-01 — PWM had none)

### Fixed
- **PWM now ships a log redactor** (`core/_log_redactor.py`, byte-identical to Core) wired at the
  entry point — PWM previously had NO redaction at all, so any secret or personal datum reaching a
  log line was emitted in clear (Hone PS-SEC-17 / PS-KEY-01 / PS-DATA-01). Strips DB passwords/DSN,
  keys, Fernet `enc:` tokens, PATs, cloudhook URLs, Bearer tokens, and PII (email + phone) from both
  the message and the exception traceback; `uvicorn` loggers routed through it (`log_config=None`).
  `test_log_redactor.py` (19). Brings PWM to Core parity.

## 2026.7.24 — Fix: real Admin-signed instructions were rejected (WR-ADMIN-006 canonical re-vendor)

### Fixed
- **Re-vendored `core/licence_verify.py`** byte-identical to the fixed canonical
  (`documentation/shared/`, commit 23378e0): `verify_artifact` now accepts the licence id under
  `target` (the real instruction wire shape, §4/§9-A.5.2) as well as `licence_id` — pre-fix, every
  REAL Admin revoke/deactivate was rejected as `invalid_signature` (latent since 2026-07-01; found
  by A's WR-ADMIN-006 live test; GSM proved the fix end-to-end on v2026.7.51). Log labels split so
  a missing id no longer mislabels as a sig/replay failure. New positive regression
  `TestPositiveInstruction` (Rule 106): a genuinely signed, target-only instruction MUST verify —
  the missing test whose absence let an always-reject verifier pass every gate.

## 2026.7.23 — Warn→block flip: signed-licence enforcement ON by default (SEC-04 receive-side)

### Changed
- **`PWM_SIGNED_LICENCE_ENFORCE` now defaults ON** — an unsigned `/api/licence/activate` or
  `/api/licence/deactivate` is rejected (400). The Admin Ed25519 signature is the authorisation;
  the /23 transport never was (§9-A). Closes the naked-deactivate hole (any sibling addon could
  wipe PWM's licence). Readiness: Admin signs every licence fleet-wide (v2026.7.52 re-issue,
  2026-07-12). Present-but-bad signatures were already always fatal — this closes the
  absent-signature legacy path. `PWM_SIGNED_LICENCE_ENFORCE=0` = emergency kill-switch (grower
  boxes have no env plumbing, so the code default IS the fleet flip). Known consequence: Core's
  manual UI deactivate forward is unsigned → now surfaces a 400 to the operator; deactivation is
  Admin-driven (signed instruction via heartbeat). Tests: default-rejected + kill-switch pairs on
  both endpoints (test_licence_signed.py 13→17).

### Fixed
- **Paddock name rendered unescaped into the Leaflet map label (stored/DOM XSS).** The desktop and
  mobile maps set the paddock divIcon `html:` to the raw grower/GIS-derived `feat.properties.name`,
  which Leaflet renders via `innerHTML` — so a paddock named with markup executed in every viewer's
  browser. The sibling pump/gate/badge sinks already ran through `esc()`; only the paddock label was
  missed. Both maps now `esc(feat.properties.name)`. Regression: `tests/test_security.py::
  TestSec14PaddockLabelXss` (asserts the raw sink is gone and the label is escaped, on both variants).
  Closes Hone PS-SEC-14 on the Core/PWM column (GSM had closed all five of its equivalents).

## 2026.7.21 — T8: W08 unified device builder (capability toggles over the Rev 2 generator)

### Added
- **`devices/compose.py`** — `POST /api/devices/compose` (spec → budget cop → pin allocator →
  render → `/config/esphome/<name>.yaml` + registry row; the spec persists in
  `yaml_vars.compose_spec` so regeneration is deterministic) and
  `POST /api/devices/compose/validate` (dry-run: allocation + per-bank budget + module set +
  config hash, or the budget cop's grower-readable refusal as a 400).
- **W08 "+ Add device" builder (desktop)** replaces the bay-only add form: role presets
  (bay/channel/pump) + capability toggles (actuators ×0–2 with per-actuator manual switches +
  gang, depth ×0–2, soil, low-supply, spare relays ×0–2, offline policy). Every change dry-runs
  against the backend budget — over-budget add buttons grey out and the refusal message shows
  verbatim; Create is disabled while invalid. Device creation stays desktop-only (as before).
- Generated YAML now carries a `# ps-board-type:` header; `esphome_dir.infer_board_type` reads it
  first, so unified compositions discover with the right board type (legacy include inference kept).

### Fixed
- W08 `discover()` referenced the fetch response outside its closure — a failed discover threw a
  ReferenceError instead of showing the error toast (desktop + mobile).

### Notes
- `rb/write-yaml` (legacy bay path) is no longer UI-wired but stays serving already-flashed
  rb-hardware boards until the bench (T10) proves the new firmware; monoliths retire at T9.
- 10 new endpoint tests (`tests/test_compose.py`); suite 215 green.

## 2026.7.20 — Rev 2 unified KC868-A4 firmware carve: chassis + capability modules + generator

### Added
- **`firmware/includes/hw-core.yaml`** — the Layer-1 chassis every board shares (MODULAR_FIRMWARE_
  DESIGN.md Rev 2, T1): one pin map, relay_k1–k4 outputs + beeper (hw-core owns ALL outputs,
  invariant 1), boot-safe-off, and a **unified Last Stop Reason** enum/text-sensor covering pump
  and actuator vocabularies (commanded / travel_complete / safety_policy / boot / manual /
  external / low_supply / wifi_disconnect / timer_expired). Config Hash sensor moves here.
- **Capability modules (T2–T6):** `mod-actuator` (+ separate `mod-actuator-switches`; templated
  ×1–2 via ESPHome package vars, every id `${n}`-suffixed), `mod-pump`, `mod-depth` (×0–2),
  `mod-soil`, `mod-low-supply`, `mod-relay-aux` (×0–2), `mod-disconnect` (the two runtime policy
  entities). Logic ported from pump-hardware v1.2.1 / channel-hardware v1.1.2 / rb-hardware v2.3.1
  — **the rb tfrom_s position model is the one actuator travel model** (T2 decision, bench to
  ratify); ganged manual switches = shared D-pins via `allow_other_uses`, freeing D3/D4.
- **`devices/unified_yaml.py` (T7)** — the one generator: capability spec → budget cop (refuses
  relays>4 / analog>3+battery / digital-overflow at generate-time with grower-readable messages)
  → pin allocator (physical reality in exactly one place) → config hash over values + module set
  → packages-with-vars render. Route-free this release: the legacy per-board generators stay live
  until the T8 UI rewire. 36 new tests (`test_unified_yaml.py`) incl. the 5-board bench matrix and
  an invariant-3 id scan of the shipped modules. Suite 205 green.
- `firmware_sync` ships the 9 new includes to `/config/esphome/Includes/` (legacy monoliths still
  synced until T9 retirement).

### Notes
- **Nothing is flashed by this release** — flashing stays manual/canary via ESPHome
  (FIRMWARE_ROLLOUT.md). Bench-check items before first flash: physical pin map + the relay-pair
  standardisation (legacy rb boards wired open=K2/close=K1; unified standard open=K1/close=K2).

## 2026.7.19 — W08 stops refreshing constantly

### Changed
- **W08 polled too hard.** Live values (valve position, depth, raw volts) were fetched every **1s**
  with a cache-bust, and the whole card list was rebuilt every **15s** — the visible "page keeps
  refreshing" (Peter, 2026-07-11). Live values now update in place every **3s** (still smooth for a
  valve move, 3× lighter on HA), and the full rebuild — which only exists for membership + online
  status, both rare — drops to **60s** and pauses while a card or the add-bay form is open. Discover
  / add / delete still reload immediately, so nothing goes stale in practice.

## 2026.7.18 — device assignment: single source of truth

### Fixed
- **A board's assignment now derives only from what references it.** `pwm_devices.assignment_type`
  was a second, redundant flag alongside the real ownership (`pwm_pumps.device`,
  `pwm_channel_gates.device`, `pwm_bays` valve/sensor slots). Clearing it on the device page did not
  clear the pump/gate/bay that owned the board, so the W09 Bench stayed locked with no way out
  (Peter, 2026-07-10). The Bench `isAssigned()` now reads only the derived `assignment_display`, and
  the registry PUT no longer writes `assignment_type`/`id`/`slot`. To free a board, clear it on the
  page that owns it — which the Bench warning already names.

### Tests
- `tests/test_device_assignment.py` (+2) — the registry PUT does not write the assignment columns;
  Bench `isAssigned` is defined in terms of the derived label, not `assignment_type`.

## 2026.7.17 — W08 can create a bay device (RiceBoard) from inside PWM

### Added
- **W08 "+ Add bay device"** — names a new RiceBoard, sets its disconnect policy (close / hold /
  open) and timeout, and writes `/config/esphome/<name>.yaml`, adopting it into the registry as
  `board_type=riceboard` with per-device credentials. Same deterministic-from-config pattern as the
  pump (W05) and channel-gate (W06) builders; calibration follows on the W09 Bench. This closes the
  last gap in "create every board type from PWM" — previously a bay board could only be discovered,
  never created, and no RiceBoard YAML generator existed.
- **`devices/rb_yaml.py`** + **`POST /api/devices/rb/write-yaml`** — the generator. The rb-hardware
  include references 14 substitutions raw (cal_1m/cal_5m/soil × 4, plus disconnect policy/timeout),
  none with in-place defaults, so all are seeded here — a missing one fails the ESPHome build.

### Tests
- `tests/test_rb_yaml.py` (6) — asserts the generator supplies every raw substitution the
  rb-hardware include references, renders base + rb-hardware packages, policy/timeout come through,
  an invalid policy falls back to `close`, and no capitalised Python bools/None leak.

## 2026.7.16 — depth-sensor defaults: offset 0 (not min), device_class distance

### Fixed (firmware includes — reflash to apply)
- **Depth offset defaulted to its own minimum, so a fresh board read implausibly low.** The offset
  template numbers omitted `initial_value`, and ESPHome uses `min_value` when it's absent — so a
  newly-flashed board booted with offset −100 (pump) / −200 (channel) instead of 0, and the depth
  sensor read the clamped −10 cm floor. On a pumpboard this fed the low-supply gate and **blocked
  pump start** (the relay-1 investigation, 2026-07-10); on a channel board it feeds the overflow
  rule. Confirmed live on PDEV-MC-01 (`depth_offset −200`, `depth −10`). Now `initial_value: 0` in
  `pump-depth-1`, `pump-depth-2` and `channel-hardware`. (Existing boards keep their stored value —
  set it to 0 in HA, or it corrects on the next factory-clear.)
- **Depth sensors reported `device_class: voltage`.** They are `platform: adc`, which defaults the
  class to voltage, but they publish cm — so HA treated a depth as a voltage. Now `device_class:
  distance` on all three. Include versions bumped: pump-depth 1.1.0→1.1.1, channel-hardware
  1.1.1→1.1.2.

### Security (Hone)
- **PS-FW-04 verified CLOSED on a live board.** Probed PDEV-MC-01 (10.75.99.123): port 80 refused
  (no web control UI); only 6053 (Noise-encrypted HA API) and 3232 (password-protected ESPHome OTA)
  listen. The `ota: - platform: web_server` line in the resolved config is inert without a
  `web_server:` component. Firmware verdicts are now probed against a running board, not inferred
  from source or resolved config.

## 2026.7.15 — W06 gate form: sensor picker, one Save button, refresh-from-ESPHome

### Fixed
- **Overflow "upstream sensor" was free text** — a typo or a since-deleted entity saved fine, and
  the overflow rule reads it by exact id (`gate_automation.py`), so it silently never fired. Now a
  select sourced from **`GET /api/ha-sensors`** (HA sensors that plausibly report a water level — by
  unit cm/m/mm, `device_class: distance`, or a depth/level/water/section name, and a numeric state).
  A saved sensor no longer present in HA is still shown, flagged "— not in HA", so a dangling rule is
  visible rather than hidden.

### Changed
- **Save and "Generate & write YAML" are one button.** Save persists the gate, then — if a board is
  assigned — regenerates its YAML from the saved config (deterministic from the DB) and reports
  whether the firmware recipe actually changed, so you're told to flash only when it matters. The
  flash stays manual in ESPHome. `write-yaml` now returns `changed` (content-compared before
  overwrite).
- **"Automation enabled" relabelled to make its job clear** — it arms the gate's overflow protection
  (upstream sensor + trip depth); off means the controller leaves the gate alone. Grouped under an
  "Overflow protection" heading with a one-line explanation.
- **W06 gains "↻ Refresh from ESPHome"** — re-scans `/config/esphome` (discover) and rebuilds the
  device list + live entities, so a board renamed or added from the ESPHome dashboard shows up
  without an addon restart.

### Tests
- `tests/test_gate_overflow_sensor.py` (7) — `_is_level_sensor` includes cm/distance/name-hint
  sensors and rejects non-numeric, unrelated, and non-sensor entities; `write-yaml` reports `changed`.

## 2026.7.14 — main fills the space beside the sidebar; forms get every pixel

### Fixed
- **The v2026.7.13 layout fix was half a fix.** Keeping `max-width` while pushing content right of
  the sidebar shrank the usable width — at a 1440px window the form had 1160px instead of the 1280px
  it used to (incorrectly) claim, and text boxes clipped their contents. `bench`, `channels`,
  `config_pumps` and `config_channels` now do what `sensors`/`devices`/`trace` already did: **no
  margin override and no width cap.** The theme's `margin-left: var(--ps-sidebar-width)` anchors
  main to the sidebar and `flex:1` fills everything to its right. A 1920px window now gives 1640px
  of form, up from a 1240px cap.
- **The two-column editors collapsed too late.** `config_pumps` collapsed at a 900px *viewport*, but
  the fixed 240px sidebar comes out before the columns get a share — so between 1000px and 1100px
  each field was left 150–200px wide. Both setup pages now collapse to one column at 1100px, and
  `config_channels` stacks its 170px label above the input below 900px.

## 2026.7.13 — pages no longer slide under the sidebar; the Save button stays put

### Fixed
- **Cards rendered underneath the fixed sidebar whenever the window was not maximised.** Four pages
  overrode the theme with `.ps-main-content{margin:0 auto}`, wiping the theme's
  `margin-left: var(--ps-sidebar-width)`. The master theme and `app.css` are unchanged
  (Rule 17 / ADR-007, Rule 193.3). Superseded by the cleaner fix in 2026.7.14.

### Changed
- **W06: the Save button is a sticky bar.** It sat at the foot of the *left* column while
  "Generate & write YAML" sat at the foot of the *right* one; with `align-items:start` the columns
  end at different heights, so where Save appeared depended on how much you had configured. It now
  follows you down the editor, with the flash action deliberately left in the ⚠ column — a safe
  action and a board-changing one must not sit side by side.
- **W05: the "Save All Changes" bar is sticky**, for the same reason — the pump form is long enough
  that the primary action scrolled out of reach.

## 2026.7.12 — channel YAML compiles; device pickers know what a board is

### Fixed — channel-gate YAML generation (found in Peter's `pdev-mc-01` compile, 2026-07-10)
- **The generated channel YAML did not compile.** `_channel_subs` did `str(data.get(...))` on flags
  the UI stores as JSON **booleans**, so `has_depth_sensor` rendered as `"True"`. The generator's own
  `== "true"` check then failed, the `cal_1m_*` substitutions were never written, and ESPHome died on
  `'cal_1m_d0' is undefined` in the depth-sensor lambda.
- **Actuator 2 had no manual switch control.** The firmware tests `strcmp("${gang_manual_switches}",
  "true")`, which `"True"` never matches — so the ganged branch never fired. Actuator 2's independent
  switches are guarded by `strcmp(gang, "false")`, which `"True"` also never matches. Both paths were
  dead: the R2 manual switches did nothing.
- **`has_pump_status` could silently re-enable itself.** `str(body.get(x) or data.get(x) or "true")` —
  a real `False` is falsy, so a deliberately-disabled pump-status input fell through to `"true"`.
- New `core/helpers.yaml_bool()` normalises all three, and `default` now applies only to absent
  values, never to an explicit `False`.
- **W06: writing a gate's YAML did not rebind the gate to that board.** The YAML and the device
  registry moved to the new device while `pwm_channel_gates.device` kept pointing at the old one.
- **W06 registered channel boards as `board_type='channelboard'`** while `esphome_dir` infers
  `'channel'` from the same YAML — one board, two type names depending on where you read it.

### Fixed
- **A pumpboard could be assigned as a channel gate.** `/api/esp-devices` returned bare device
  names with no board type, and all eight pickers (`paddocks`, `channels`, `automation`,
  `config_pumps` × desktop/mobile) consumed it unfiltered. It now returns
  `{devices: [{name, board_type, source}], missing: [...]}`; pump pickers accept only
  `pumpboard`, gate and bay pickers exclude it. Boards of undetermined type stay selectable but
  are labelled — refusing them would hide a freshly-discovered board from the picker used to
  configure it.
- **Deleted and mistyped board names haunted every picker.** `_collect_referenced_devices` unioned
  every device string ever stored on a pump, gate or bay row, so a name with no registry row, no
  YAML and no HA presence reappeared forever — and selecting it wrote the bad name straight back.
  Those now come back under `missing`, shown as a flagged "referenced, no YAML yet" group in the
  gate pickers (they are precisely the boards you go there to configure) and never as ordinary
  peers. `pwm_bays.level_sensor` is no longer folded in at all: it holds an entity id, not a
  device name.
- **Raw, unflashed boards were invisible.** Discovery matched `sensor.<dev>_wifi_signal`; the
  firmware publishes `wifi_signal_db` (`base.yaml`). The suffix never matched.
- **`GET /api/devices/{id}/entities` dropped every entity of a renamed board.** It filtered by
  string prefix `<device>_`, but HA rebuilds entity ids from the device's *current* name, so a
  renamed board splits across prefixes. It now resolves through HA's device registry
  (`get_device_entity_ids_cached`) — the same fix `helpers.py` already carried. This is why W09
  could not see this board's depth sensors, aux relays or low-supply override.
- **W06: writing a gate's YAML did not rebind the gate to that board.** The YAML and the device
  registry moved to the new device while `pwm_channel_gates.device` kept pointing at the old one.
- **W06 registered channel boards as `board_type='channelboard'`** while `esphome_dir` infers
  `'channel'` from the same YAML — one board, two type names depending on where you read it.

### Added
- **W09 §3 "Inputs"** — enumerates the board's real analogue channels (calibrated value, raw
  voltage, offset) and digital inputs, from the device's actual entity set. On a pumpboard the
  digital group explains *why* it is empty: the only GPIO input is the pump-status feedback, which
  is `internal: true` and disabled unless `has_pump_status` is set. Relay-state sensors are
  excluded — they publish the board's commanded state, not a pin reading.
- **W06 Device field** now offers a datalist of channel-capable boards plus referenced-but-
  unconfigured ones, while staying free-text so a new board can be named before its YAML exists.

### Tests
- `tests/test_esp_device_picker.py` (4) — pumpboard detected from its control switch; a bare
  actuator never guesses a type (riceboard and channel both expose `valve.<dev>_actuator_1`); a raw
  board is found via `wifi_signal_db`; a YAML-derived type beats an unknown HA guess.

## 2026.7.11 — W09 Bench: relays 3/4 and depth offsets work on grower-renamed boards

### Fixed
- **W09 Bench "Relay 3/4 ON/OFF" did nothing, and reported success.** Two bugs stacked. The commands
  resolved the switch by object-id *suffix* (`relay_3`), but HA rebuilds an entity id from its display
  name — a relay named "Relay 3 On/Off" becomes `..._relay_3_on_off`, which no longer ends with
  `relay_3`. `dev_service` correctly returned `False` and logged "command NOT sent", and the relay
  branch **ignored the return value** and returned `{"ok": true}`. Same class as the 2026-07-07 gate
  bug; the bench path never got that fix.
- **`set_depth_offset` had the identical fault** — a grower-named depth sensor ("Sensor 1 Test")
  yields `..._sensor_1_test_offset`, matching neither canonical suffix.
- **`debug_on`/`debug_off` swallowed a missing entity.** All bench commands now surface a 404 when the
  entity is absent, and a 502 when the service call fails.

### Added
- **`core/helpers.match_device_entity_fragment()`** — object-id *contains* match, used only as a
  fallback after the exact-suffix match and only against a **single device's** entity list. Widening
  it to an unscoped list would recreate the 2026-07-07 cross-device incident, and it says so.

### Tests
- `tests/test_device_assignment.py` (+5) — exact suffix misses a renamed relay, the fragment finds it,
  the exact suffix still wins on an unrenamed board, the fragment respects the domain, and the bench
  relay path surfaces failures rather than swallowing them.

## 2026.7.10 — W09 Bench: a device card now names what owns the board

### Fixed
- **A board wired as a bay supply/drain valve or level sensor reported as UNASSIGNED.**
  `list_devices` never selected `supply_1`, `drain_1` or `level_sensor` from `pwm_bays`, so
  `_build_assignment_display` had nothing to match on. The Bench disables output tests on assigned
  boards — meaning it would have driven a live bay valve. Pump and gate assignments were unaffected
  (they matched via their own re-queries).
- **`/api/devices` re-queried `pwm_pumps` and `pwm_channel_gates` once per pump/gate, per device.**
  Both rows now carry `device` from the initial fetch.

### Changed
- **Assignments name their kind:** `Pump: Main Creek Pump`, `Gate: MC-02`, `Bay: W17 B-01 supply`.
  A bare name left the operator hunting across three pages for where to clear it.
- **W09 Bench** shows the owner on the device card ("Assigned to Pump: …" / "Unassigned — free for
  bench testing") and the locked-outputs warning now names the owner *and* the page that owns it.
  When the registry row is flagged assigned but nothing references the board, the warning says so
  rather than pointing nowhere.

### Tests
- `tests/test_device_assignment.py` (7) — each assignment kind renders its label, an unassigned board
  renders empty, and `list_devices` selects the columns the display matches on.

## 2026.7.9 — pump-start safety unified · in-app OTA removed · SEC-16 credential leak closed

### Security
- **SEC-16 — `POST /api/pumps/{id}/write-yaml` no longer returns the board's credentials.** The
  response carried `subs`, the substitution map, which `_build_pump_subs` merges the per-device OTA
  password and API encryption key into (FW-03). Any `operator` calling write-yaml received both in
  cleartext. The response is now `{ok, path, device}`, matching the channel-gate endpoint, which
  never leaked. No caller read `subs`.

### Fixed — pump automation (all found by source review, 2026-07-10)
- **Every automated start now runs the same guard chain as the manual button.** New
  `pumps/control.py` owns `start_pump()`/`stop_pump()`: board-online + strict control-entity
  resolution + ping, dry-run protection, anti-short-cycle, and the 30s start-verification alarm.
  Previously only `/api/command` checked any of it — the scheduled start (`pumps/timers.py`) and the
  demand controller (`automation/demand.py`) issued a raw `switch.turn_on`, so a scheduled start
  would run a pump into a dry channel that the manual button refused a minute later. A refused
  scheduled start no longer arms a countdown, clears the schedule, and notifies.
- **A scheduled start now fires without an addon restart.** `_start_scheduled_task` was only ever
  reached from `resume_pump_timers()` at startup, so a schedule set from the UI persisted to the DB
  and did nothing — unless PWM happened to restart before the scheduled time, in which case it fired.
- **Timer expiry records `last_stop_at`.** It didn't, so anti-short-cycle was silently skipped after
  the stop most likely to be followed by an immediate restart.
- **"Timer expired during restart — stopping pump" now stops the pump.** The branch logged exactly
  that, reset the timer row, and sent no command; a pump ran on indefinitely if PWM was down when its
  shutdown timer would have expired. It also re-arms the board backstop on resume — the board's
  `shutdown_timer` is `restore_value: no`, so nothing else ever put it back after a reboot.
- **Pause holds the board's remaining seconds instead of disarming it** (Peter, 2026-07-10). Pause
  and reset both wrote `0` to the board's `shutdown_timer` (= disabled) while leaving the pump
  running — removing the independent backstop that exists precisely for when PWM is dead. Reset
  re-arms at the full duration.
- **Stop/reset cancel a pending scheduled start**, which lived under a separate `{pump_id}_sched`
  task key and survived both. `_start_timer_task` now cancels before replacing, so an orphaned
  countdown can no longer turn a pump off out of nowhere.

### Removed
- **In-app OTA flash.** `POST /api/pumps/{id}/flash-ota` and `GET /api/pumps/{id}/flash-status`, the
  mobile "UPDATE DEVICE — OTA" button, and the orphaned desktop handler are gone. The device firmware
  lifecycle is ESPHome-managed and a board is flashed from the ESPHome dashboard, canary-first, by a
  person (`docs/FIRMWARE_ROLLOUT.md`, Peter-ratified 2026-07-08) — the code had never caught up with
  the decision. Drift detection (`/firmware-check`) and its `_device_online` helper are kept.

### Tests
- `tests/test_no_inapp_ota.py` (11) — asserts on the route table so the flash endpoints cannot grow
  back, and that `firmware-check` survives; plus the SEC-16 response-shape guard.
- `tests/test_pump_start_guards.py` (12) — every start path goes through `pumps/control.py`; stop
  paths record `last_stop_at`; pause holds the board backstop. Its call-site sweep found a fifth raw
  start path in `devices/commands.py` (device-scoped bench command), now a named, documented
  exception pending a ruling.
- Suite: 118 passed.

## 2026.7.8 — WR-PS-109: per-user module-access enforcement on ingress (Hone SEC-04/SEC-09, Option B)

### Added
- **`core/module_gate.py`** (vendored from the Farm reference, `MODULE_KEY="paddisense-pwm"`): Core
  pushes its `module_access` grant table to `POST /api/access/sync`; PWM caches it durably in
  `/data/module_access_grants.json` (atomic swap) and enforces per-user access locally on every
  **ingress** request. Decision semantics mirror Core's `effective_modules`: never-synced → open
  (bootstrap), synced-no-entries → open, granted/all-access/admin → allow, configured-but-ungranted
  → **403**. A direct cookie login with PWM's own credentials keeps its existing role path.
- **`POST /api/access/sync`** receiver — trust = the same transport gate the licence-forward path
  uses (`_authorised_caller`); push-signature hardening is the tracked fleet follow-up WR-PS-108.
- **`tests/test_module_gate.py`** (11) — decision-table units + end-to-end through the REAL auth
  middleware: ungranted ingress user 403s on pages and `/api/*`, granted user passes, never-synced
  box stays open, corrupt cache never locks the grower out.

## 2026.7.7 — WR-PS-093 close-out: interim `.ps-fullscreen` removed from app.css

### Changed
- **Removed the addon-local `main.ps-fullscreen` interim copy from `static/app.css`.** The rule was
  restored to the master theme (`documentation/theme/paddisense-tokens.css` §3, steward close of
  WR-PS-093, 2026-07-09) and PWM's tokens copy is byte-identical to the master (`cmp -s` clean), so
  the map-page height chain (W01/W03/W04) now resolves from the canonical tokens file. Property-for-
  property identical definition — no visual change; removing the duplicate closes the Rule 169/193.3
  "app.css must not duplicate master classes" exposure.

## 2026.7.6 — Rotation self-heal for the app DB pool (incident 2026-07-09, Rule 106)

### Fixed
- **App DB pool now self-heals across a box-key rotation.** Live incident 2026-07-09: Core rotated the
  box key (`db_role.key`, WR-PS-088), changing the `pwm_app` DB password; the running PWM held the OLD
  password in its pool, so the next fresh connection failed auth and PWM showed "not licensed / won't
  accept code" until a manual restart. On a grower box no one can restart it — a routine rotation would
  strand the add-on. `_acquire_conn` now treats a `password authentication failed` on the **app** pool
  as a stale key: it drops the pool, rebuilds it (re-reading `/share/paddisense/db_role.key`), and
  retries **once**. A second failure propagates (genuine mismatch, not a rotation). Never applies to the
  admin/superuser pool — least-privilege (R173) untouched.

### Added
- `tests/test_pool_selfheal.py` — 4 tests (R192): recovers from a stale password (exactly one retry, no
  storm); a genuine second auth failure propagates; a non-auth error (server down) is not retried; the
  admin pool never self-heals.

## 2026.7.5 — WR-PS-101: fix the lying test, not the app (licence-gate ingress redirect)

### Fixed
- **`tests/test_licence_gate_ingress.py::test_unlicensed_redirect_without_ingress_header_is_bare`
  was red on `main` and could never have passed.** It used the `client` fixture, which sets
  `X-Ingress-Path` as a **default header on every request** (`conftest.py`), then asserted the
  redirect carried *no* ingress prefix. httpx merges client-default headers into each request, so
  the test sent the header it claimed to omit. `licence_gate` returned the correct answer for the
  request it actually received. The test now uses `anon_client` (no headers) and additionally
  asserts that no ingress header is being sent, so a future fixture change cannot silently make it
  vacuous again.
- **No production bug existed.** `paddisense_pwm/main.py::licence_gate` reads `X-Ingress-Path` from
  the request on every call and holds no state. WR-PS-101 originally alleged a module-level
  `base_path` leaking across requests (Rule 128) with a concurrency hazard; that diagnosis is
  **retracted** — the test failed *in isolation*, where no previous request exists to leak from.

### Changed
- `tests/conftest.py::client` docstring now warns that `X-Ingress-Path` is a default header on
  every request and cannot be unset by omitting it from a call. Tests meaning "no ingress" or
  "unauthenticated" must use `anon_client`.

### Verified
- Not vacuous (Rule 192): injected a real cross-request `base_path` leak into `licence_gate` — the
  exact bug originally alleged — and the repaired test goes red; the real code turns it green.
- Swept the same class: AST-checked every PWM test taking `client` and asserting 401/403. Three
  hits, all legitimate (licence-403, or explicitly testing ingress-trusted admin). The genuine
  no-auth tests in `test_smoke.py` already use `anon_client`.

## 2026.7.4 — Hone PS-SEC-19: mask secret config fields + Rule 17 theme re-sync

### Fixed
- **`admin_key` + `github_pat` rendered UNMASKED in the Home Assistant add-on options UI (Hone PS-SEC-19).**
  The `schema:` type was `str?`, so HA drew a plain text input: the secret was visible on
  screen, in screenshots, and over a shoulder. Changed to `password?` — the same type
  `db_password` already uses here, and the type GSM already uses for its `admin_key`. No
  functional change: existing values are untouched, only the input is masked.
  `github_pat` is a GitHub Personal Access Token — a credential leaving a PAT unmasked in the
  options UI is the most severe instance of this class in the fleet.
- **Rule 17: `static/paddisense-tokens.css` re-copied from the canonical master.** Master gained
  `main.ps-fullscreen` on 2026-07-09 (WR-PS-093 steward closure) and the change was never
  propagated, leaving every addon byte-divergent and its next commit blocked by the Rule 17
  gate. Verified the drift was that one additive block — nothing local was clobbered.

## 2026.7.3 — ROOT CAUSE: `.ps-fullscreen` lost from the theme — map height chain restored

### Fixed (closes the W04 zoom/offset saga — git-history-proven)
- v2026.6.121 added `.ps-fullscreen` (the Leaflet height chain for W01/W03/W04) to the LIVE
  master theme file uncommitted; the steward theme rebuild obliterated it and the v2026.6.148
  Rule-17 re-sync propagated the loss — since then every map fit computed against a
  junk-height container: farm "just offscreen" on open, click-zoom landing elsewhere.
  The class is restored in PWM's own app.css (NOT the synced tokens copy — Rule 17 clean);
  WR-PS-093 asks the steward to land it in the master theme, then the local copy goes.
- v2026.7.1/7.2's fit-timing + ResizeObserver hardening stays — correct regardless.

## 2026.7.2 — W04 map: ResizeObserver kills the stale-container offset

### Fixed (Peter live-repro: click-zoom landing north of the clicked paddock — "like an offset")
- Leaflet caches the map container size at init; W04's layout changes after load and when
  panels open/close, offsetting EVERY centre/fit by the size delta (the load fit landing the
  farm just off-screen AND the click-zoom offset are the same bug). A ResizeObserver now
  re-measures on every container resize, and the click-fit invalidates before fitting.

## 2026.7.1 — W04 map fit lands on the farm (container-size race) · July versioning begins

### Fixed (Peter live-repro: farm "just offscreen" on page open)
- **W04's fitBounds raced the page layout** — Leaflet computes the fit against the container
  size at call time; the layout settles a moment after init, landing the farm just out of
  frame. The map now invalidates its size and re-fits once after layout settles.
- Version series moves to 2026.7.x (July) per Peter.

## 2026.6.209 — W05 include-file viewer removed + the no-Claude editing runbook

### Changed (Peter-agreed: includes are shipped firmware, never edited on-box)
- The Firmware Include viewer on W05 (desktop + mobile) is removed — on-box include edits
  are a trap (startup sync overwrites them; stripping the version header silently freezes a
  file out of all future fixes). Firmware source lives in the PWM repo.
- **FIRMWARE_ROLLOUT.md gains the bus-factor runbook**: how Peter edits and ships includes
  WITHOUT Claude (repo edit → version bumps → commit/push → store reload → reflash), plus
  the true-emergency on-box path with its trade-offs spelled out.

## 2026.6.208 — W05 depth calibration retired → W09 Bench (Peter-ruled: cal lives on the commissioning station)

### Changed
- The Depth Calibration section on W05 (desktop + mobile) now points to the W09 Bench page;
  the duplicated sampler/save code is removed. One calibration implementation, one home —
  built on the resolved entity feed.

## 2026.6.207 — Single save path on W05: standalone "Write YAML" button removed (Peter-directed)

### Changed
- The Board & Firmware "Write YAML & Save" button (desktop) and "Write YAML" (mobile) are
  gone — they generated the YAML from the SAVED DB row without saving the form first, so
  unsaved changes never reached the file (a stale-YAML trap, Peter live-repro). **Save All
  Changes** is the one path: saves the row (through the admin-confirm guard) → writes the
  YAML → syncs live settings. Hint text now points there.

## 2026.6.206 — Beeper on every board type + W05 bench section retired (Peter-directed)

### Firmware (pump v1.2.1 · rb v2.3.1 · channel v1.1.1 — reflash to take effect)
- **Pump boards now expose `switch.<device>_beeper`** (the only board type missing it —
  bench-found: W09 beep-to-identify silently did nothing on the pump). Matches the
  RiceBoard/channel pattern.
- **All beeper switches are `ALWAYS_OFF`** (were RESTORE_DEFAULT_OFF — a reboot mid-beep
  restored a screaming board; a reboot must never resume a beep).

### Changed
- **Beep reports honestly** — 404 "no beeper switch on this device — reflash" instead of a
  success toast over a resolver miss.
- **W05 pump setup: Bench Testing section retired** → links to the W09 Bench page (desktop +
  mobile); the bench test-suite JS removed with its dispatcher case.

## 2026.6.205 — W09 Bench page (desktop): commissioning station, slice 2

### Added (per docs/W09_BENCH_DESIGN.md — commissioning-only, Peter-ruled)
- **New W09 Bench page + sidebar entry.** Device picker (registry cards: online dot · board
  type · commissioned / not-commissioned / assigned / bench badges · Discover-Sync button),
  then per-device sections: **Identity & Comms** (ping, beep-to-identify, firmware versions,
  Wi-Fi); **Outputs Test** (board-type-adapted buttons — pump start/stop confirm-gated +
  relays 3/4; actuator open/stop/close + cal jogs for gate boards; DISABLED with an
  explanatory note when the board is assigned to live infrastructure); **Sensors &
  Calibration** — live raw-voltage feed (Debug auto-toggle button + automatic during
  sampling), and the two-point tube calibration rebuilt on the RESOLVED entity feed (pick
  the raw source entity + target slot → sample A/B with 30 s settle + 90 s average →
  save to cal_1m/cal_5m, provenance-audited). Desktop first; mobile after browser sign-off.
- Commissioning checklist UI + guided safety checks = slice 3 (wants the bench boards live).

## 2026.6.204 — W09 Bench slice 1: commissioning record + discover fix (Peter-designed)

### Added (W09 design: docs/W09_BENCH_DESIGN.md — commissioning-only, cal moves to W09, record kept)
- **`PUT /api/devices/{id}/commissioning`** — persists the per-board commissioning checklist
  (pass/fail items, firmware versions at test, note) server-stamped with the acting HA user
  and time, in the device registry. The commissioned flag will WARN on assignment elsewhere,
  never block. Audited.

### Fixed (Peter live-repro: "Found undefined" toast)
- **Discover 500d after a successful sync** — the stats dict passed as logging `extra`
  contains `created`, a reserved Python LogRecord attribute; logging raised AFTER the DB
  work committed. Keys now prefixed. (Gate gap noted: Rule 88s check misses dict-built
  extras.)
- **All four discover toasts check the response** — errors surface honestly instead of
  "Found undefined, undefined new".

## 2026.6.203 — W04 map render is exception-proof per feature

### Changed
- Each Farm boundary feature renders inside its own try/catch — one bad feature can no
  longer kill the render loop, leave the map at the default view, or hide the bays
  (the 2026-07-07 failure mode, now structurally impossible). Failures log to the browser
  console with the feature's properties for diagnosis. fitBounds runs regardless.

## 2026.6.202 — Strict entity-resolver sweep: bays, gates, automation controllers (fleet-wide)

### Changed (extends v200's safety fix from pumps to every device class — lands BEFORE bay/channel hardware)
- **All actuator command paths resolve entities per device, never string-built:** gate
  dispatch (switch + valve types), bay supply/drain valves, manual gate commands, pump
  control in the demand controller + timers, W08 device commands (cal buttons, relays,
  debug, offsets, numbers), refuel + settings sync. A missing entity is a LOUD error/404 —
  never a silent HA 200 no-op ("the gate didn't move").
- **All device-scoped reads go through the resolver too:** bay online/depth/valve state,
  gate valve state, dry-run depth check, demand pump status, depth poller, automation
  status — via a warmed 60 s per-device cache (`warm_device_entities` at each controller
  cycle + live build) with `sync_resolve_state` for tight sync loops. Legacy doubled-prefix
  variants (`{device}_{device}_online`) eliminated.
- **`ping_device` resolves its sensor** — a renamed device is no longer wrongly reported
  unreachable (which blocked pump starts fail-safe but needlessly).
- Intentional residuals: device DISCOVERY stays prefix-scanning (that is how unadopted
  boards are found); bay sensor bindings store explicit user-picked entity ids (safe by
  design).

## 2026.6.201 — Fix: pump delete silently failed (missing confirm param, unchecked response)

### Fixed (Peter live-repro on recycle pump)
- `deletePump` (desktop + mobile) never sent the `?confirm=true` the API requires — the server
  returned 400 and the UI showed "Pump deleted" anyway because it never checked the response.
  Now sends the confirm (the human already confirmed in the dialog) and surfaces failures
  honestly instead of lying with a success toast.

## 2026.6.200 — SAFETY: pump cards strictly scoped to their own device (bench-found) + relay state buttons

### Fixed (Peter live-repro: every pump card mirrored — and could reach — the one bench board)
- **The any-device suffix fallback in entity lookup is GONE.** `find_device_entity` is strict
  prefix-only; pump live state and pump start/stop resolve entities exclusively from THIS
  device's HA-resolved entity set (`device_entities`, 60 s TTL cache). A pump whose device
  lacks a control switch now errors instead of silently commanding another board — on a real
  multi-pump farm the old fallback could have started the wrong pump.

### Added (Peter-requested)
- **Relay 3/4 are now state buttons like the start button** — green = ON, red = OFF, `--`
  when unknown/offline — driven by per-device resolved relay states (custom relay names
  resolve by slug).

## 2026.6.199 — Pump card Low-Supply visibility + override · entity resolution fixes (bench-found)

### Fixed (Peter live-repro on the bench board)
- **Relay 3/4 toggles were silent no-ops after a relay rename** — the handler string-built
  `switch.{device}_relay_N`, but HA derives entity ids from the grower-set name AND the
  device's current HA name (one board found split across two prefixes). New resolver asks HA
  for the device's entities (`device_entities` template) and matches by name-slug/suffix.
- **Custom-named depth sensors now resolve** in pump live state (name-slug fallback), and the
  card's depth display shows cm (was mislabelled m).

### Added (Peter-requested)
- **Pump card Low-Supply Protection section (W02.B):** depth readings + minimum depth + the
  board's **Low-Supply Override** toggle (confirm dialog; stays ON until cleared; audited
  server-side with the acting HA user) + last-stop reason. The pre-start block now shows the
  operator WHY a start was refused and gives them the deliberate choice — the grower owns
  the system.
- New `pump_override` command target; `get_device_entity_ids`/`match_device_entity`/
  `ha_name_slug` helpers (fixed-prefix entity derivation is deprecated — resolver refactor
  of remaining call sites tracked in the device-sync build).

## 2026.6.198 — Live device-entity feed (state truth, slice 1)

### Added
- **`GET /api/devices/{id}/entities`** — one device's live entity states straight from HA
  (never cached in PWM; ESPHome is the source of truth): runtime settings (No-WiFi response/
  action, travel times), state-truth sensors (last stop reason / safety event), version
  sensors, online flag.
- **W06 reads live values through it** — per-gate device feed replaces the /api/live shape
  guesswork; online dots + the left-column live panel now populate the moment a board is
  adopted and online. Bench-verified target: peter_test_pump (v2.2.0-1.2.0, OTA-flashed
  with per-device credentials today).

## 2026.6.197 — Firmware sync compares content, not the header comment

### Fixed
- **v196's depth-module changes never reached `/config/esphome`** — the include sync only
  overwrote when the `# Version:` header comment differed, and the headers matched. Sync now
  compares file content (the grower-customised protection — no version header — is kept).
  Depth-module headers also stamped 2026.6.196.

## 2026.6.196 — Raw-voltage publishing gated on Debug Logging (Peter-agreed)

### Firmware (pump-depth-1/2 v1.1.0 — reflash to take effect)
- **Raw Voltage sensors publish only while Debug Logging is on.** The 5 s raw stream exists
  for the two-point calibration sampler; 24/7 it spams the device log + HA recorder. ADC keeps
  measuring; publishes are filtered.

### Changed
- **The calibration sampler flips Debug Logging automatically** (on at sample start, off at
  the end — desktop + mobile), so calibration works exactly as before with zero extra clicks.

### Bench evidence recorded (peter_test_pump wired-flashed to base v2.2.0 + pump v1.2.0)
- Per-device OTA password + Noise API key LIVE on hardware (FW-03/SEC-02) · safe_mode present
  and armed (10 attempts/300 s — FW-05 residual CLOSED) · port-80 probe REFUSED while 3232/6053
  open (FW-04 field evidence) · No-WiFi Response Time entity live · credential-change flashes
  confirmed wired-only (documented in FIRMWARE_ROLLOUT.md).

## 2026.6.195 — Secrets files are independent contexts: never merge (FW-03 fix) + wired-flash doc

### Fixed
- **`ensure_farm_secrets` no longer merges the two esphome secrets files.** They are separate
  `!secret` resolution contexts (per-directory) and legitimately hold different values on a
  real farm — found live: different `ota_password` AND `wifi_ssid`; the Includes copy is what
  flashed boards trust. A merge-triggering rewrite would have clobbered the boards' Wi-Fi
  credentials. Each file now only ever gains its own missing keys; existing values untouched.
- **FIRMWARE_ROLLOUT.md: credential-change flashes are wired, one-time per board** — ESPHome
  auths OTA with the new config's password; no old-password path exists (bench-proven on
  peter_test_pump). Farm-wide `ota_password` stays as compile fallback + recovery credential.

## 2026.6.194 — Fix: W06 gate cards failed to render (live-state shape + unparsed gate data)

### Fixed
- `/api/live` returns a structured object, not an entity array — the card renderer's entity
  lookup threw and aborted before drawing any gates. Lookups now tolerate any shape (offline/—
  is the truthful display until the state-truth endpoint lands with the bench boards).
- Gate `data` arrives as a JSON string from the list endpoint — now parsed defensively, so
  overflow badges and the editor populate correctly. Peter live-repro.

## 2026.6.193 — Fix: W06 channel setup fetched outside the ingress prefix (empty page)

### Fixed
- The new W06 page built its API base from a nonexistent `window.PWM_BASE` instead of the
  base template's `BASE` (`{{ base_path }}`), so every fetch escaped the HA ingress prefix
  and returned nothing — no channels rendered. Peter live-repro.

## 2026.6.192 — Fix: W06 channel setup 500 (template name missing .html)

### Fixed
- New W06 page 500d with TemplateNotFound — the route passed `desktop/config_channels`
  without the `.html` suffix that `pick_template` normally appends. Peter live-repro.

## 2026.6.191 — W06 Channel Setup: new two-column full page (desktop, pump-pattern copy)

### Added (Peter-approved layout; desktop first for browser review, mobile follows — W05.B sequence)
- **New `config_channels` page replaces the modal-based W06 on desktop.** Gate cards (online
  dot · adoption state · overflow set/declined/unset badges) → two-column editor. LEFT
  Operating Settings: name/position, No-WiFi behaviour + travel time + last-stop-reason shown
  LIVE from the board's entities (ESPHome is the source of truth; placeholders until adopted),
  automation incl. the overflow required-or-decline flow inline. RIGHT ⚠ Board & Firmware:
  device assignment, actuator/gang/depth config, travel seeds, **Generate & write YAML**
  (v190 endpoint — registry adoption + FW-03 credentials), firmware-version status line.
  15 s live refresh. Mobile keeps the existing page until desktop is signed off.

## 2026.6.190 — Channel-gate device YAML generation + registry adoption (UI build slice 1)

### Added
- **`POST /api/channels/{cid}/gates/{gid}/write-yaml`** — generates the ESPHome device YAML
  for a channel-gate board from the gate's DB config (the master: actuator count/labels,
  ganged switches, depth sensor + two-point cal, travel-time seeds) composing base v2.2.0 +
  channel-hardware v1.1.0, adopts the board into the device registry (`board_type:
  channelboard`) and mints its per-device OTA/API credentials (FW-03) on first write.
  Regeneration is deterministic — calibration and config survive reflash/rollback
  (FW-06 master, FIRMWARE_ROLLOUT.md). Writes audited with the acting HA user.

## 2026.6.189 — Every actuator command audited with the acting HA user (SEC-02 close-out)

### Security
- **`POST /api/command` writes one uniform `actuator_command` audit row at the entry point**
  (actor + target + params) covering all sub-handlers — paddock mode, bay door/drain, pump,
  gate, relay. Previously only some paths audited, none with actor identity.
- **`POST /api/devices/{id}/command` rows now carry the actor** as well. Together with the
  encrypted per-device ESPHome API (base v2.2.0) this closes PWM's SEC-02 slice: authenticated
  channel + per-device credentials + actor-attributed audit trail for every actuator move.

## 2026.6.188 — Calibration provenance: bench cal saves audited with the acting HA user (FW-06/FW-09)

### Changed
- The W08 two-point calibration save (`/api/devices/{id}/calibrate` — the test-tube two-depth
  sensor-average flow) now writes an `admin_config_change` audit row with the acting HA user
  and the saved cal pairs. This is the calibration master's who/when record: bench-calibrated
  once at construction, preserved by YAML regeneration for the life of the board. No extra
  confirm — the sample-sample-save flow is already deliberate.

## 2026.6.187 — DB pool pressure telemetry + graceful retry (SCAL-06)

### Changed (Peter-agreed: measure before resizing the Rule 91 ARM pool)
- **Momentary pool exhaustion no longer 5xxs the grower** — `get_conn` retries once after a
  0.3 s backoff; only sustained saturation propagates.
- **`/health` now carries `db_pool` counters** (`exhausted_total`, `retry_recovered`) so the
  Admin fleet view sees real pool pressure via the heartbeat poll; resizing decisions happen
  on evidence, not guesswork.

## 2026.6.186 — Overflow protection: required-or-decline on sensored gates (SCAL-05)

### Changed (Peter-agreed 2026-07-06: default ON where physically possible, explicit audited opt-out)
- **A gate with a depth sensor can no longer be saved with overflow protection silently
  unset.** Gate create/update now returns 422 unless the gate has an upstream sensor +
  emergency depth configured OR the operator explicitly declines; W06 (desktop + mobile)
  offers exactly that choice — configure now, or decline. A fresh decline writes an
  `overflow_protection_declined` audit row with the acting HA user. Hone's literal
  "fire on every gate" is physically impossible without a sensor — closure is
  on-by-requirement wherever a sensor exists (all 7 Main Channel gates get sensors at
  deployment per Peter).

## 2026.6.185 — Admin-setting confirm + change log with the acting HA user (FW-09)

### Security / UX (Hone FW-09 — Peter-designed: informs, never denies; the grower owns the system)
- **Safety-critical settings now require a deliberate confirm.** New `core/config_guard.py`:
  changes to the agreed administrative list (relay mode/pulse timings, status pin, module
  enables, depth calibration, battery divider, Low-Supply enable + minimum depth, gate
  actuator travel times) return 428 with a change list; both base templates show a simple
  confirm modal ("old → new") and resend with `_confirm_admin` — one generic hook covers
  every current and future admin endpoint. Cancelling leaves everything unchanged.
- **Every confirmed admin change is audit-logged with the acting HA user** —
  `admin_config_change` rows carry actor (`ha:<user>` from the ingress identity headers,
  falling back to the PWM session user) + a compact field: old→new summary. Wired on
  `PUT /api/pumps/{id}` and `PUT /api/channels/{cid}/gates/{gid}`.

## 2026.6.184 — Per-device credentials + generated farm secrets (FW-03) · Low-Supply ON by default (FW-08)

### Security (FW-03 — Peter-approved 2026-07-06; base include v2.2.0, reflash to take effect)
- **Per-device OTA password + API encryption key.** The YAML generator now mints a random
  OTA password and Noise API key per device (persisted in `pwm_devices.yaml_vars`, stable
  across regenerations so HA adoption survives) and emits them as `device_ota_password` /
  `device_api_key` substitutions. base.yaml v2.2.0 consumes them via `${...}` with the
  farm-wide `!secret` values as fallback — not-yet-regenerated device YAML keeps working.
  A board pulled from a paddock now leaks only its own credentials — no lateral movement.
- **Farm secrets generated by construction.** New `core/esphome_secrets.py` +
  `ensure_farm_secrets()` at startup: missing esphome secrets (ota, encryption key, fallback
  AP, api password) are generated randomly per farm; existing values are never touched;
  wifi_* placeholders only on fresh installs. Answers Hone's cross-farm-reuse question
  permanently: unique per farm because they are never copied.

### Changed (FW-08 — Peter-ruled)
- **Low-Supply protection is ON by default for every new pump** — `_insert_pump_row` seeds
  `data.low_supply_enabled: true`; disabling is an explicit per-pump operator action (the
  setup UI toggle already defaulted on; the backend now matches for pumps created without
  touching the toggles).

## 2026.6.183 — Licence-gate redirect carries the ingress prefix (WR-PS-046 / Hone PLAT-07)

### Fixed
- **Unlicensed page redirect 404d through HA ingress.** `licence_gate` runs before
  `auth_middleware` (LIFO), so `request.state.base_path` was unset and the redirect went to
  bare `/licence`. The gate now reads `X-Ingress-Path` directly — same root cause + fix as
  Core v2026.6.388 and Safety v2026.6.25. Regression suite `test_licence_gate_ingress.py`
  (4 tests: prefix carried · bare path without ingress · API 403 not redirect · exemption).
  Hone PLAT-07 fault #1 (startup crash) is guarded by the ADR-011 §5 `validate_config()`
  startup gate, verified at every commit.

## 2026.6.182 — RiceBoard v2.3.0 + pump v1.2.0: per-device No-WiFi response, countdown beeper (Peter-designed)

### Firmware (reflash required; bench-first — no field boards are live on this box)
- **RiceBoard v2.3.0.** Same reboot-defeat bug as pumps FIXED: the 15-min default wifi reboot
  reset the 30-min disconnect-policy countdown halfway, so close-under-safety could never fire
  at default timing — `wifi.reboot_timeout: 0s` (position survives reboots; boot forces relays
  off). Flash-time policy/timeout substitutions replaced by runtime entities: No-WiFi Action
  (close/hold/open, seed from `${disconnect_policy}`) + No-WiFi Response Time (min, 0 = never,
  seed 30) — per-device, UI-set via HA, board-executed. Manual-move exemption KEPT (a
  hand-positioned gate is never overridden by the policy). New `Safety Event` text sensor
  (safety_close / safety_open / policy_skipped_manual / policy_hold / boot) syncs on reconnect
  for the "closed under safety" badge + gate log.
- **Pump v1.2.0.** Fixed 30/60-min cascade → per-device No-WiFi Response Time (default 300 min
  / 5 h, 0 = never). At 50% offline: countdown beeper — one alert cycle EVERY MINUTE (only
  while the pump is actually running) so anyone on site knows a safety shutdown is counting
  down; at 100%: pump shuts down (stop reason wifi_disconnect) + final beep. The old device-side
  30-min `homeassistant.event` warning could never deliver while offline — removed; remote
  alerting + the operator countdown belong to the PWM addon (state-truth build, owed).

## 2026.6.181 — Channel firmware v1.1.0: hold on Wi-Fi loss + the finish guarantee (Peter-designed)

### Firmware (channel-hardware v1.0.0 → v1.1.0 — pre-deployment; no channel board is flashed yet)
- **Board-local timed travel (the finish guarantee).** A received open/close ALWAYS completes:
  the board stops the move itself after the per-device travel time + 3 s margin (deliberate
  slight overrun into the actuator's internal end stop, then the relay releases). Previously
  the stop came only from the addon over Wi-Fi — a drop mid-move left the relay energised
  indefinitely. Wi-Fi is now irrelevant once a command reaches the board.
- **Hold on Wi-Fi loss, enforced + per-device configurable.** Channel fail-safe is HOLD, no
  movement (Peter 2026-07-06 — supersedes Hone's close-on-loss prescription). New runtime
  entities on every board: No-WiFi Response Time (min, 0 = never/indefinite — the default) and
  No-WiFi Action (hold/close/open), plus per-actuator Travel Time — all UI-settable via HA,
  no reflash, board executes locally. Each device can be different.
- **`wifi.reboot_timeout: 0s`** — a reboot is a movement-state hazard; boards reboot only on
  crash/power (boot forces relays off, so a reboot never resumes a drive).
- **State truth for the UI:** Last Stop Reason (commanded / travel_complete / safety_policy /
  boot / manual) + Last Move Source (manual/remote) text sensors — sync on reconnect so PWM
  can show "closed under safety" vs operator action. Manual hold-to-run switches stay live
  offline (the local override).

## 2026.6.180 — Pump firmware v1.1.0: Wi-Fi loss never reboots a pump board (FW-05, Peter-agreed)

### Firmware (pump-hardware v1.0.1 → v1.1.0 — requires reflash to take effect; bench-first)
- **`wifi.reboot_timeout: 0s` on pump boards.** ESPHome's default (15 min) rebooted the board a
  quarter of the way into the deliberate Wi-Fi-loss safety cascade (30 min warn → 60 min pump
  shutdown), resetting the counters every cycle — the 60-minute shutdown could never fire, and
  each cycle blipped the relays. Pump boards now reboot only on crash or power event; any reboot
  leaves the pump OFF until an operator reviews (the existing on_boot reconciliation). Agreed
  with Peter 2026-07-06 (WR-HONE-FW-05 — remainder of the finding closes as design-intent:
  crash recovery is native, API-idle reboot deliberately off).
## 2026.6.179 — W04 paddock config: fix "failed to disable" + fit map to enrolled paddocks

Two live bugs Peter hit on the paddock setup page.

### Fixed
- **Enable/disable paddock returned "failed" (CSRF 403).** The toggle sends a bodyless PUT, so
  the browser sent no Content-Type and the CSRF middleware (Rule 157, fail-closed) rejected it.
  Both base-template fetch wrappers now default `Content-Type: application/json` on any mutation
  that doesn't set its own — fixes every bodyless mutation (desktop + mobile), not just this one.
- **W04 map opened zoomed to the whole property; bays + gate markers effectively invisible.**
  Since the GIS extraction the boundary proxy serves every farm paddock (47+), and the initial
  fit spanned them all. The map now fits to the PWM-enrolled paddocks (falls back to all
  boundaries when none are enrolled). Bays and gate markers were rendering all along — just
  sub-pixel at farm scale.

## 2026.6.178 — Box-key diagnostics: add stat identity (dev/ino/size/mtime)

### Fixed
- Box-key INFO line now includes `dev/ino/size/mtime` so a divergent mount source is
  identifiable from the boot log (live incident 2026-07-06: container reads different
  key bytes than the host at the same path).

## 2026.6.177 — Log the box-key source + fingerprint (WR-PS-088 diagnostics)

The `_read_master_key()` fallback chain was silent — an unreadable or empty `/share` key
dropped derivation to the stale local `/data` key with no trace in the logs, fail-closing the
`pwm_app` app pool with nothing to debug from. Live incident 2026-07-06: `pwm_app` auth
failed in-container after the 10:56 box-key republish while the identical derivation
succeeded outside the container.

### Fixed
- **Box-key reads are now logged.** Each candidate path logs a WARN when unreadable or empty;
  the chosen source logs an INFO with the key's SHA-256 fingerprint (first 12 hex chars — never
  the key or the derived password). No derivation or pool behaviour change.

## 2026.6.176 — Prefer the dedicated /share db_role.key for the DB password

Prefer the dedicated /share db_role.key for the *_app DB password; falls back to master.key during
the WR-PS-088 split rollout — no behaviour change today.

### Security
- **DB-role key preference (WR-PS-088 Phase-1a).** `_read_master_key()` now reads
  `/share/paddisense/db_role.key` first, then falls back to the legacy `/share/paddisense/master.key`,
  then the local `/data` key. Both shared keys carry the same value until the future 1b flip, so this
  is additive and behaviour is identical today. The fail-closed app-pool logic, the no-superuser
  fallback, the local key path and the DSN builder are unchanged.

## 2026.6.175 — Release-quality tidy-up: login and notification forms now use the standard theme styling

This release fixes some form boxes on the sign-in and notification-group screens that were quietly
using an old style name the shared PaddiSense theme no longer recognises, so they were showing
unstyled. They now use the standard theme field styling like the rest of the app, so the username,
password, group-name and description boxes look consistent and properly framed. We also tightened
the code-quality checks behind the scenes (stricter type checking) and switched the automated
release check from "advisory" to "must pass" so a build can no longer ship if these standards slip.
No features changed and no data is affected.

### Theme
- **Login and notification forms restyled to the canonical field pattern.** The desktop and mobile
  sign-in pages and the notification-group editor referenced `ps-form-group` / `ps-form-control`,
  which are not defined in the shared theme (master tokens or the addon stylesheet) and so rendered
  unstyled (Rule 193 dangling). They now use the theme's canonical `.ps-field` pattern, where inputs
  are styled by the `.ps-field input` rule — no reinvented classes.

### Quality
- **mypy now clean.** Added a missing cursor type annotation in `devices/bench.py` and replaced a
  type-inference-blocking lambda with a typed nested function in `devices/commands.py` so static
  type checking passes with no errors.
- **CI release-gate is now blocking.** The ADR-010 pre-release audit job in CI dropped its rollout
  `continue-on-error` flag, so the RELEASE gate now fails the build if a release-only standard
  regresses (dangling theme classes, mypy, CVEs).

## 2026.6.174 — Security-test correction: signed-licence replay/nonce now has a real regression test

We found that a required security test was wrongly recorded as "not applicable". PWM does check
that a digitally-signed licence can't be replayed or reused, but that protection had no test
proving it. This release adds a real test that forges a properly-signed licence and confirms the
app refuses a replayed one, an expired one, and a future-dated one — while still accepting a genuine
fresh one. No behaviour changed; this only closes a testing gap so the protection can never silently
break in future.

### Security (test coverage — REQUIRED_SECURITY_TESTS row 142 corrected N/A → covered)
- **Rule 142 signed-request replay was wrongly marked N/A.** The vendored `core/licence_verify.py`
  — reached from the activate/deactivate route in `api/licence.py` via `_verify_licence_signature`
  → `evaluate_signature` → `verify_artifact` — already enforces two anti-replay controls on every
  Admin-signed licence/instruction: a single-use `(licence_id, nonce)` ledger (`_nonce_ok`) and an
  `issued_at`/`exp` freshness window (`_fresh`, ±60 s skew). New `tests/test_r142_licence_replay.py`
  signs with a throwaway pinned Ed25519 key and proves the receive-side rejects (a) a reused nonce
  (replay), (b) an expired/stale timestamp, and (c) a future-dated timestamp, with a positive
  control that a fresh first-seen artifact IS accepted, plus an end-to-end case that a replay driven
  through the addon's own `_verify_licence_signature` route helper returns 400. Applicable
  security-test coverage is now **8/8** (remaining N/A: R146/153/159/189).
- **No production code changed** — test-only; the test-DB provisioning stays in `conftest`. Full
  `pytest` suite is GREEN (85 passed, 0 failed, 0 error).

## 2026.6.173 — security-test manifest now enforceable: test-DB grant fix (least-priv parity)

### Tests / infra
- **Test-DB made runnable as the least-privilege app role (WR-PS-081 gap closed test-side).**
  The disposable `paddisense_pwm_test` DB had tables owned by `postgres` but no grants for the
  request-path `pwm_app` role, so every DB-touching endpoint test failed-closed with
  `permission denied for table ...`. New session-scoped `conftest._provision_test_db` fixture
  provisions the test DB exactly like prod: create DB + apply schema/migrations **as admin
  (postgres)**, ensure the `pwm_app` login role exists (master-key-derived password, created only
  if absent — never re-passworded, so a shared prod role is untouched), then `GRANT` it the DML it
  needs (SELECT/INSERT/UPDATE/DELETE on tables, USAGE/SELECT on sequences, schema USAGE) plus
  matching DEFAULT PRIVILEGES. The app-under-test still connects as `pwm_app` (prod parity — no
  superuser shortcut). Idempotent; survives a drop+recreate of the test DB. **No production
  pool/auth/security path changed.**
- With the DB fixed the whole suite is **GREEN** (80 passed, 0 failed, 0 error), so the
  `REQUIRED_SECURITY_TESTS` manifest can be flipped to blocking for PWM (a green suite can no longer
  hide a never-written test). Determinism: a session-scoped `conftest._no_background_tasks` fixture
  no-ops the startup automation loops (depth poller / irrigation / demand / gate / pump timers) for
  the test process only — they use blocking psycopg2 in `async` (Rule 137 debt), so at teardown
  `TestClient.__exit__` could otherwise intermittently hang on task cancellation and stop pytest
  from printing its summary. No test asserts anything about those loops; production startup is
  unchanged. Verified reproducible: dropping and recreating the test DB, the suite rebuilds it from
  scratch and passes.
- Fixed pre-existing broken tests unrelated to security: `test_config_hash` updated to the current
  10-argument `_compute_config_hash` signature (relay/depth entity names now part of the hash);
  5 `TestMobilePages` assertions updated from removed page-id badges / inline `padding-bottom:80px`
  (dropped in the R41/R178 UI refactor) to the durable `ps-mobile-content` template discriminator
  (still proves the mobile — not desktop — template is served).

### Security-test manifest coverage (dispositions re-confirmed)
- Applicable + covered: R154/157/158/171/187/188/190. N/A with reason: R142/146/153/159/189
  (no signed-request replay channel · no CSV export · single-tenant/no owner column · no
  server-side dynamic-URL fetch · no email/resend flow). See `docs/AUDIT.md`.

## 2026.6.172 — ADR-010 flip-ready re-audit to Golden Rules v2.49 + security-test manifest

### Security / Tests
- **Security-test manifest brought to full applicable coverage** (`REQUIRED_SECURITY_TESTS`, Rule
  154/157/158/171/187/188/190). New behavioural regression tests in `tests/test_security.py`:
  CSRF token-less/non-JSON mutation → 403 (R157); role-based authorization denial via `has_role`
  (R154); oversized `Content-Length` → 413 + login rate-limit bound (R158); forged `X-Forwarded-For`
  ignored by ingress-trust (R187); forged ingress header from an untrusted peer refused **and**
  logged as a security event (R171); session revocation/expiry drops authentication (R188);
  non-existent-user vs wrong-password login responses are byte-identical — no enumeration oracle
  (R190). Rules 142/146/153/159/189 marked **N/A** with concrete reasons in `docs/AUDIT.md`.
- Tests assert each control at the layer that rejects **before** the DB is touched
  (middleware / pure auth primitives), so they pass despite the pre-existing test-DB `pwm_app`
  grant gap (WR-PS-081 rollout has not reached the disposable test DB) — no green is faked.

### Audit
- Re-audited against **Golden Rules v2.49** (Wave-4a). `golden_rules_version` 2.48 → 2.49 in
  CLAUDE.md and `docs/AUDIT.md`; last_audit_date 2026-07-04, cadence 14 days.
- **Rule 28 (Category-A relocation) now carried in this addon's CLAUDE.md** — Core = paddocks +
  crop zones, PWM = bays — with a Verify line. PWM owns no paddock boundary authority.
- Re-verified every applicable rule (not a version bump); one real gap re-registered per R98
  (Rule 121 blocking `httpx.get` in `api/paddocks.py`).

## 2026.6.171 — SEC-08/R173: fail-closed DB app pool (Phase-2, WR-PS-081)

### Security
- **The request-path DB pool is now fail-closed (R173/SEC-08).** `_pool.py` no longer falls back to
  the `postgres` superuser if the `pwm_app` app pool can't initialise — `get_cursor()` returns the
  least-priv app pool or raises. Migrations/DDL still use the admin pool during the startup window
  (before `init_app_pool()` is called). Converges the fleet to Farm's fail-closed posture; a future
  key/role failure now fails loudly instead of silently promoting request-path queries to superuser.
  (`/share` persists, so an established box that reboots keeps its key and does not fail-closed.)

## 2026.6.170 — SEC-08/R173: admin/app DB pool split (fleet-standard, WR-PS-081)

### Security
- **`_pool.py` now maintains two pools** — an **admin** pool (`postgres` superuser) for migrations/DDL
  and an **app** pool (`pwm_app`, least-privilege DML) for request-path queries. `get_cursor()` uses
  admin while the app pool isn't ready (startup/migrations), then `main.py` calls `init_app_pool()`
  after `ensure_database()` so request-path queries run as `pwm_app`. Adopts the Livestock/Farm
  canonical pattern; the prior single-pool-on-app-role would have failed **fresh-box** schema
  provisioning (`permission denied for schema public`). DDL routes through admin, DML through the app
  role. Shutdown closes both pools.

## 2026.6.169 — SEC-08/R173: read the shared box key so pwm_app authenticates (WR-PS-081)

### Security
- **`_pool.py` now reads the box DB-role key from the shared `/share/paddisense/master.key`** Core
  publishes (WR-PS-081), falling back to the local `/data` key during rollout. The per-container
  `/data` key differed from Core's, so `pwm_app`'s derived password never matched the role Core minted
  → the pool **silently fell back to the `postgres` superuser** (confirmed fleet-wide via boot logs).
  Now `pwm_app` authenticates → the R173 least-priv DML-only request path is genuinely in effect.
  Fernet-at-rest untouched (separate `/data` key). Superuser fallback kept as a rollout safety net;
  Phase 2 fail-closes.

## 2026.6.168 — SCAL-03: Python 3.11 → 3.12 base-image bump + digest pin (Hone SCAL-03 / WR-PS-080)

### Changed
- **Base image `python:3.11-slim` → `python:3.12-slim@sha256:423ed6ab…199fbf`** (same fleet-index
  digest as Core/Farm/Livestock/Store/ASM/Weather). `pyproject.toml` ruff `target-version` + mypy
  `python_version` → 3.12. Off the Python 3.11 EOL runway (Hone SCAL-03) and digest-pinned for
  reproducible builds (Rule 69 posture). Isolated bump — no dependency changes piggybacked
  (WR-PS-080 non-goal). Test suite already runs on the pinned 3.12 toolchain; dev-deploy rebuilds
  on 3.12-slim and smoke-verifies.

## 2026.6.167 — SEC-04: verify Admin signature on licence deactivate (finish the receive-side)

### Security
- **`/api/licence/deactivate` now verifies the Admin Ed25519 signed instruction**
  (`_verify_instruction_signature`, `api/licence.py`; `action ∈ {deactivate,revoke}`). Activate has
  verified the signature since v165; deactivate still accepted the naked call on transport trust
  (`_authorised_caller` /23) alone — the "unauthenticated deactivate" `SIGNED_LICENCE_CONTRACT §9-A`
  retires. Core already forwards the signed instruction (`forward_targets` deactivate →
  `{signed_instruction}`). Both mutating licence paths are now signature-gated — signature, not
  network position, is the trust boundary. Legacy-tolerant during the fleet signing rollout (same
  `PWM_SIGNED_LICENCE_ENFORCE` flag; present+bad sig always fatal, unsigned accepted until enforce).
  Closes the PWM slice of **WR-HONE-SEC-04**.
- Tests: `TestDeactivateApi` (403 unauth, 200 unsigned-legacy, 400 bad-sig) + instruction policy units
  (`test_licence_signed.py`, 13 pass).
- Type hygiene: `assert src is not None` after the `_extract_licence` guard in activate (narrows the
  pre-existing `dict|None` union — `api/licence.py` now mypy-clean).

## 2026.6.166 — Fix: add `cryptography` dep for the licence signature verifier (v165 500 fix)

### Fixed
- Entering a **signed** licence returned **500 Internal Server Error**: `core/licence_verify.py` imports
  `cryptography` lazily (Ed25519), so PWM started fine but `verify_artifact` hit an `ImportError` on the
  first signed licence because `cryptography` was not in `requirements.txt`. Added `cryptography==48.0.1`
  (pinned, matches Core). Signed-licence activation now works; unsigned still legacy-tolerated.

## 2026.6.165 — Licence activate: fleet /23 transport trust + Admin signature verify (SEC-04); §5 onboarding

### Fixed
- **Core→PWM licence forwarding returned 403 "Unauthorized."** PWM had narrowed its "internal" trust to
  loopback + HA-infra IPs only, excluding the sibling-addon subnet — so Core's tokenless forward from the
  Supervisor `/23` was rejected (every other addon still trusts the `/23`). `activate`/`deactivate` now
  accept the **Supervisor `/23`** as transport (matching Store/Weather/Livestock).

### Added
- **SEC-04 receive-side (first in the fleet):** PWM now **verifies the Admin Ed25519 signature** on the
  licence as the real authorisation — vendored `core/licence_verify.py` + pinned `data/admin_signing_pubkey.json`,
  `evaluate_signature` policy behind `PWM_SIGNED_LICENCE_ENFORCE` (default off during rollout: present+valid →
  authentic, present+BAD → always reject, absent → legacy-tolerated). Accepts a raw `code` or a `signed_licence`
  body (heartbeat distribution). 8 tests (`test_licence_signed.py`).
- **ADR-011 §5 onboarding:** public `validate_config()` called first in the startup handler.

### Docs
- Re-baselined audit v2.44 → **v2.46** (Rule 118); CLAUDE.md/AUDIT synced. Trunk-based on `main` (ADR-012).

## 2026.6.164
ADR-010 flip-readiness — verify-commit CLEAN (0 warn / 0 viol). No functional change.
### Changed
- **R41 inline styles (944 → 0):** extracted to `pwm-` CSS classes across 24 templates;
  dynamic (JS-computed) values → CSS custom properties (`style="--x:..."`); ~900 were inside
  JS-built HTML strings. All rendered `<script>` blocks pass `node --check`.
- **R178 / orphan-bindings (15 → 0):** per-page `<script nonce>` restructure (moved each page's
  `{% block script %}` out of the base `<script>`).
- R17: 5 JS status-colour hex → `var(--ps-*)` tokens / `getComputedStyle` (Leaflet); theme re-sync.
- R60: split `write_pump_yaml` + `create_test_paddock` to ≤50 lines.
- R106: removed the dead `@router.post(".../demand/set-level")` decorator on the `_actuate_demand_gates`
  helper (no callers; it's an internal helper).
- R88 ×2: var-extracted `existing["name"]` so the reserved-key grep no longer false-positives.
- R157: added CSRF behavioural 403 test. Docs: CLAUDE/AUDIT golden_rules 2.25→2.42.
### Note
- Browser smoke-test of all pages still required (visual-regression check after the R41 sweep).

## 2026.6.162
### Changed
- **Mobile Setup page restructured to match desktop.** Sections are now fixed (no accordion) and grouped under two clear headings — **Operating Settings** (no flash) and **⚠ Board & Firmware** (needs a flash) — the mobile equivalent of the desktop two columns. The Hardware section gets the same **+ Add / Remove** controls for Relay 3/4, Depth Sensor 1/2 and Low-Supply, writing the `*_enabled` flags; "Dry Run" → "Low Supply".
### Verified
- **Deep-dive on the save→YAML chain (desktop + mobile).** Exercised the real generator (`_build_pump_subs` + `_render_pump_yaml`) across selections: full board emits all 9 packages + cal_1m/cal_5m; a 1-sensor electric/constant board emits only base+hardware+depth_1 and cal_1m (no fuel/pulse/relays/depth_2/cal_5m); a relay3+depth2+low-supply mix emits exactly those + cal_5m only. `config_hash` changes with the module set. Confirmed flags flow form → `body.data` → PUT → write-yaml (reads DB data, composes, preserves flags), so the device YAML tracks the UI selection.

## 2026.6.161
### Changed
- **Two-column Setup page (W05.B desktop).** The pump detail page is now a fixed two-column layout (no accordion): **LEFT = Operating Settings** (no flash — Pump Details, Live Settings, Upstream/Auto-Stop, Service, Bench, Notes); **RIGHT = ⚠ Board & Firmware** (needs an ESPHome flash — Board Setup, Depth Calibration), with clear column headings. Sections are always open.
- **+ Add / Remove module controls.** "What's wired to the board" now has explicit **+ Add / Remove** for Relay 3, Relay 4, Depth Sensor 1, Depth Sensor 2 and Low-Supply Protection — each toggles the per-pump `*_enabled` flag the generator composes from (load/unload the include). Unsaved names are preserved across toggles. No more "blank name = off".
- **"Dry Run" → "Low Supply"** in the UI; Low-Supply threshold sits under Live Settings (live), enable sits under Board & Firmware (flash).
- **OTA button removed** from the drift banner — it now says "Settings changed — flash required: open `<device>` in ESPHome → Install → Wirelessly" (PWM can't trigger ESPHome OTA without the Device Builder integration; drift detection stays).
- Mobile `config_pumps.html` two-column restructure still pending (desktop only this release).

## 2026.6.160
### Changed
- **Modular carve — depth sensors + Low-Supply (W05.B).** Depth sensor 1 & 2 (each with its calibration, raw-voltage diagnostic and live offset) extracted to `pump-depth-1.yaml` / `pump-depth-2.yaml`; Low-Supply protection inputs (threshold number + override switch) to `pump-low-supply.yaml`. The pump-start dry-run safety logic in pump-hardware is **decoupled via core globals** (`depth_1_cm`/`depth_2_cm`/`dry_run_min_cm`/`dry_run_override`): depth modules publish their cm one-way, the Low-Supply module sets threshold + override, and core's **pre-start block + 60s runtime cut-out** check `min(depth_1, depth_2) < threshold` (uses **both** sensors; override bypasses; safe defaults never trip with no sensor). "Dry run" → **"Low Supply"** in messaging.
- **Generator composes by explicit enable flags** (`data.depth_1_enabled` etc.) — a 1-sensor pump emits no `depth_2`/`cal_5m`, an unused relay no `aux_relay`, etc. `config_hash` now folds in the **module set** so adding/removing a module flags "OTA required". Migration `006` backfills the flags for existing pumps (depth 1+2 + low-supply on; relays on iff named) so nothing vanishes on upgrade. (UI Add/Remove controls land with the two-column layout next.)
- Requires a reflash. Override switch stays on until turned off (maintenance / faulty sensor).

## 2026.6.159
### Changed
- **Modular carve — aux relays (W05.B).** Relays 3 & 4 extracted from `pump-hardware.yaml` into per-relay includes `pump-aux-relay-3.yaml` / `pump-aux-relay-4.yaml` (each carries its own GPIO output, switch, state sensor, boot-safe-off and 5s state-publish interval; references the `${K3}`/`${K4}` pin map from pump-hardware, one-way). The generator composes a relay's package **only when that relay is named** in the pump form, and emits its name substitution only then — so a pump that doesn't use relay 3/4 exposes no relay-3/4 switch or state sensor in HA. Name a relay → it appears on next flash; clear the name → it's gone. `firmware_sync._FILE_MAP` ships both. Requires a reflash.

## 2026.6.158
### Fixed
- **Pump status sensor / status pin (+ power source, calibration) reverted to defaults on every reopen.** `/api/config-data` (which populates the pump config page) trimmed each pump's `data` to a hardcoded 4-key allowlist (`channel_control, relay_mode, pulse_on_s, pulse_off_s`), silently dropping `has_pump_status`, `pump_status_pin`, `pump_power_source`, the `cal_*` points and `yaml_subs`. The form never received them and fell back to hardcoded defaults (Yes / D1) — even though the values saved correctly to the DB. `_prepare_config_pumps` now returns the full pump `data`. (Also removed the temporary v157 FWDBG diagnostic.)

## 2026.6.156
### Fixed
- **Pump detail showed a connected board as "offline".** `GET /api/devices/{id}` returned the raw DB row without live enrichment, so `online` (and depth/pump live fields) were never set — the pump page read it as offline even when the board was connected. It now enriches with live HA state (`_enrich_connectivity`/depth/pump/relay) exactly like the list endpoint.

## 2026.6.155
### Fixed
- **OTA error is now honest about the real blocker.** When a board is online + flashed but has no firmware `update` entity, the OTA path no longer says "flash over USB" — it says the **ESPHome Device Builder integration isn't linked** (Settings → Devices & Services), which is the actual reason PWM has nothing to `update.install`. `_update_entity_id` now also matches `update.<device>_firmware` (not just `update.<device>`), so PWM finds the entity whichever name ESPHome uses once the integration is linked.

## 2026.6.154
### Changed
- **Modular firmware carve — module 1 of N: `pump-pulse` (W05.B).** First step of the modular ESPHome composition (see `docs/MODULAR_FIRMWARE_DESIGN.md`). The diagnostic "Turn On/Off Trigger Time" sensors moved out of `pump-hardware.yaml` into a new `pump-pulse.yaml` include, composed by the generator **only when start mode = pulse**. Constant-mode (typically electric) boards no longer expose those sensors in HA. The pulse/constant control logic stays in `pump-hardware` (branches on `${pump_mode}`); only the diagnostic entities are gated. `firmware_sync._FILE_MAP` ships the new include. Requires a reflash to take effect. (Remaining modules — depth-1/2, dry-run, aux-relay-3/4 — follow one per deploy so each is flash-validated.)

## 2026.6.153
### Changed
- **Entity-name parity + single-source firmware fields (W05.B).** The generator now bakes the grower-entered names into the device YAML so Home Assistant shows exactly what was entered: relay 3/4 names and depth sensor 1/2 names are emitted as substitutions (`_build_pump_subs`/`_render_pump_yaml`), sourced via a single `_pump_entity_names()` helper. `config_hash` now covers those names (and power source consistently), so a name change correctly flags "OTA required". `write_pump_yaml` records the firmware fields top-level (`relay_mode`/`has_pump_status`/`pump_status_pin`/`pump_power_source`/`pulse_on_s`/`pulse_off_s`) so `firmware_check` and the form read exactly what was flashed — fixes settings appearing to "reset" after a YAML-only save (the top-level vs `yaml_subs` drift).
- **Pump page restructure (desktop) — tiers + one firmware banner.** Section headers now state the flash boundary: **Pump Details · no flash**, **Live Settings · no flash**, **⚠ Board & Firmware · changes need a flash**. The firmware status + **UPDATE DEVICE — OTA** button now render together **inside the danger zone** (alongside the top banner) so message and action are in one place; removed the dead "Flash Required / Firmware up to date" elements and the stale "flash via ESPHome Dashboard" wording; the drift banner now also tells the operator to run HA → device → ⋮ → **Update entity names** after a name-changing flash. Mobile page restructure to follow.

## 2026.6.152
### Changed
- **Firmware foundation (W05.B) — fuel split + entity-name parity + base security.** Restructured the ESPHome includes so a board flashed from PWM matches the form and the pump type:
  - **Fuel is now a diesel-only package.** Extracted all fuel logic from `.pump-hardware.yaml` into a new `.pump-fuel.yaml` (capacity/burn-rate numbers, remaining/level sensors, refuel button, and its own on-device 60s decrement interval that reads pump-running state one-way from the common include). The generator (`_render_pump_yaml`) composes `packages:` by power source — diesel adds `fuel: !include Includes/.pump-fuel.yaml`, electric omits it — so electric pumps no longer get empty fuel entities in HA. Offline fuel countdown is preserved (runs on-device, `restore_value`). `firmware_sync._FILE_MAP` ships the new include.
  - **Entity names parametrised** in `.pump-hardware.yaml`: relay 3/4 and depth 1/2 sensor names are now `${…}` substitutions with defaults equal to the current names (no behaviour change until the generator emits them next).
  - **`.base.yaml` security hardening:** removed the unauthenticated `web_server` on :80 (control is via the encrypted HA API); the fallback AP now uses the dedicated `esphome_fallback_wifi_password` secret instead of the main WiFi password. `base_version` → 2.1.0.
  - Requires an OTA/USB reflash of affected boards to take effect (includes sync from the repo on PWM startup). Electric `peter_test_pump` is the test case → should come back with zero fuel entities.

## 2026.6.151
### Fixed
- **Device-id canonicalisation (W05.B board management).** Pump `device` ids are now stored in the canonical underscore form (`peter_test_pump`), matching the `pwm_devices` registry and every Home Assistant entity id. Previously `create_pump`/`update_pump`/`write_pump_yaml` stored the form value verbatim, so a hyphenated ESPHome node name (`peter-test-pump`) was persisted — and every HA entity-id lookup built from it (`ping_device`, `firmware_check`, `_device_online`, `_update_entity_id`, `switch.{device}_control`, ~80 sites) missed the real underscore entities. Symptoms fixed: "Ping not detected" on pump start, pump control on/off via PWM, OTA drift detection / 3-state banner, and online status. New `canonical_device_id()` helper (`core/helpers.py`) normalises on write; the hyphenated ESPHome filename is rederived at YAML-write (`device.replace("_","-")`) so there is no YAML churn / no reflash. Migration `005_pump_device_underscore` repairs existing rows (idempotent, data-only). Root-cause fix (task #1); OTA *install* additionally needs the ESPHome Device Builder integration linked.

## 2026.6.150
### Changed
- Re-synced theme tokens to the master after its self-documenting update (usage legend, alias-deduped duplicate tokens, 6 new documented PWM/map tokens — `--ps-pwm-opening/flush/pond/off`, `--ps-map-selected/inactive`). Additive only — no visual change. These let PWM's hardcoded map colours map to named master tokens in a later wave (ADR-006 captures the deep restructure).

## 2026.6.149
### Changed
- `run.sh` now sources the theme straight from the canonical master `documentation/theme/paddisense-tokens.css` (not the drift-prone `/config/theme/`) — drift-proof at dev runtime; falls back to the bundled image copy on grower/Green boxes. Adopts A-Claude's structural fix (WR-PS-041); pairs with the `cmp` Rule 17 gate so theme drift is now structurally impossible.

## 2026.6.148
### Changed
- Re-synced `static/paddisense-tokens.css` to the master theme (was 41 lines stale) — now byte-identical to `documentation/theme/paddisense-tokens.css`. A change to the master now propagates to PWM. Fixes the Rule 17 drift (root cause: the verify-commit theme gate was blind to BusyBox diff output — fixed platform-wide this session).

## 2026.6.147
### Security
- **Rule 157 (CSRF):** API mutations now require `application/json` (no multipart — no endpoint uses it) AND a double-submit token — a cookie-session request must echo the `pwm_csrf` cookie in an `X-CSRF-Token` header (constant-time compare); a base-template fetch wrapper attaches it automatically. Ingress/internal callers (no session cookie) are exempt. Closes audit F4.
- **Rule 144:** unauthenticated `GET /api/licence` no longer returns `grower_id`/`exp`/`licence` — only `{enrolled, product}`; identity fields require an internal peer or auth. Closes audit F6.
- `docs/AUDIT.md` now **0 ❌ gaps** (F1/F2/F3 v146, F4/F6 v147; F5 mitigated → WR-PS-041). Rule 177 false-positive (comment) cleared.

## 2026.6.146
### Security
- **CRITICAL (Rule 167/172/187):** `is_ingress()` trusted any client IP starting `172.30.32.` — a sibling addon on the hassio bridge could forge the ingress header and obtain the admin session. Now pins to the exact resolved IPs of the HA ingress proxies (supervisor/homeassistant/hassio) via the `ipaddress` module.
- **HIGH (Rule 175):** grower-set values (`friendly_name` etc.) were f-string'd into ESPHome YAML unescaped — a quote/newline could inject ESPHome config. All substitution values are now sanitised for double-quoted YAML scalars.
- **HIGH (Rule 175):** calibration values were interpolated into a regex replacement (YAML quote-break + backref injection); now float-validated and substituted via a function.
- First baseline `docs/AUDIT.md` for PWM (red-team, refute-tested) — supersedes the stale 2026-06-17 audit that wrongly claimed "0 gaps".

## 2026.6.145
### Added
- Pump page (W05.B Phase 3): 3-state firmware banner at the top of the pump detail — **NEEDS FLASHING IN ESPHOME** (new/raw board), **UPDATE DEVICE — OTA** (board online but running older settings), or quiet when up to date. Offline boards show a distinct "board offline" note.
- **OTA firmware flash from PWM**: `POST /api/pumps/{id}/flash-ota` triggers HA `update.install` on the board's `update.<device>` entity (guards: device assigned, board online, pump not running); `GET /api/pumps/{id}/flash-status` reports progress. After a board's first USB flash, all updates can be sent over the air from the pump page.
### Changed
- `firmware-check` now also reports `online` so the banner can distinguish a never-flashed board from an offline one.

## 2026.6.144
### Fixed
- Discover / Generate / Delete buttons on the pump page were silently CSRF-rejected (403) because their `fetch()` calls sent no `Content-Type` — discover never ran, so ESPHome-directory boards never appeared. All state-changing requests on the pump page now send `Content-Type: application/json` (the CSRF protection). Discover now scans `/config/esphome` as intended.

## 2026.6.143
### Fixed
- Writing a pump's ESPHome YAML failed with "read-only file system" — the addon now maps `/config` read-write (`config:rw`, matching Core) so it can write `/config/esphome/<device>.yaml`. Unblocks generating a board YAML for the initial flash.

## 2026.6.142
### Added
- Pump setup (W05.B): "New Pump" opens the full setup form directly — same form for create and edit, no modal (row created on first Save).
- ESPHome devices defined in `/config/esphome` are now discovered and classified (pumpboard/riceboard/channel) even when offline or not yet flashed — new `devices/esphome_dir.py` adapter; discover merges HA states + the ESPHome directory.
- Saving a pump with a device registers the board in `pwm_devices` and writes its ESPHome YAML — covers assigning a new/replacement board to an existing pump.
### Changed
- Unified the ESPHome config-hash into one helper used by `firmware_check` and the written YAML; removed the divergent 3-field `_update_esphome_pump_yaml`.
### Fixed
- Pump form surfaces the real server error message instead of a generic "Error".

## 2026.6.109
### Security
- CRITICAL: 24 API endpoints now require role-based auth (operator/manager) — viewer could previously control pumps, gates, automation
- CRITICAL: verify_password timing side-channel fixed (hmac.compare_digest)
- CRITICAL: CSP header added (Content-Security-Policy on all responses)
- CRITICAL: 10 MB body size limit (was unlimited)
- CRITICAL: CVE fix — python-multipart 0.0.31, pytest 9.0.3
- HIGH: licence.py IP trust narrowed to resolved DNS IPs (was 172.30.0.0/16)
- HIGH: CSRF Content-Type enforcement on API mutations
- HIGH: Session cookie secure=True
- Default admin password no longer logged in full (only first 2 chars)
- Dormant /api/selftest licence exemption removed

### Changed
- run.sh: master theme copy added (Rule 179)

## 2026.6.108
### Changed
- Least-privilege DB role setup

## 2026.6.107
### Changed
- Rule 17: all hardcoded hex colours replaced with CSS token variables across 28 templates
- Rule 22: automation.html JS tabs removed — dead Paddocks+Devices tabs stripped (-59%)
- Rule 56: disallow_untyped_defs=true enforced — all functions fully typed
- Rule 60: all functions refactored to 50 lines max (40→0 violations)
- Rule 124/133: all 51 Supervisor calls consolidated into core/helpers.py adapter
- Rule 66/67: TestMobilePages added — 6 mobile smoke tests
- Rule 13: JSONB justification comments on all columns
- verify-commit.sh: ALL CHECKS PASSED — zero-gap release

## 2026.6.104
### Changed
- Golden Rules v2.3 re-audit at v103 — close quick-fix gaps (Rules 32, 35, 49, 128)
- CLAUDE.md, AUDIT.md, CHANGELOG updated to current version

## 2026.6.81-103
### Added
- W04 gate infrastructure placement on Setup Map (v6.81-99)
- Add Gate modal with dual bay connections and smart slot filtering (v6.92-98)
- Gate markers with slot type labels on map (v6.99)
- HA entity staleness guard on all entity reads (v6.80)

### Changed
- W04 sidebar rebuilt — two clean states: paddock list + bay editor (v6.90)
- Gates decoupled from devices — gates permanent, devices swappable (v6.87)
- Hub restructured: Setup tiles + Operations tiles, sidebar nav removed (v6.102)
- Infrastructure tab bar reduced to Pumps + Channels (v6.102)
- Cache busting propagated to all 22 standalone templates (v6.82)
- Canonical theme synced from documentation repo (v6.103)
- Page IDs use .B (desktop) / .M (mobile) suffix (v6.102)
- verify-commit.sh: Rule 17 theme sync check added

### Fixed
- Bay ID type TEXT not integer — was causing 500 on gate save (v6.86)
- JS crash from undefined sublabel variable in gate tooltip (v6.100)
- Disable/re-enable paddock preserves bays (v6.96)

## 2026.6.80
### Changed
- Golden Rules v2.3 full audit — 18 gaps closed, `docs/AUDIT.md` created (Rule 98/105)
- API response envelope standardised to `{"ok": true}` (Rule 61)
- Three-layer cache busting: path-versioned URLs, `must-revalidate` on static, `no-store` on HTML (Rule 53)
- HA entity staleness guard — stale values (>30 min) rejected (Rule 132)
- Graceful shutdown handler — cancels tasks, closes DB pool (Rule 92/134)
- Two-token PAT manager adopted (Rule 89/90, WR-PS-026)
- CDN integrity hashes on all external scripts (Rule 82)
- Mobile dashboard extends `mobile/base.html` (Rule 16)
- Mobile bottom padding 80px (Rule 47)
- Print colour preservation (Rule 46)
- Migration rollback comments (Rule 19)
- Session cookie uses named constant `SESSION_MAX_AGE` (Rule 58)
- Leaflet pinned to @1.9.4 with SRI hashes in automation templates

### Removed
- `.github/workflows/trigger-build.yml` — Rule 73 violation (WR-PS-025)

### Fixed
- 16 mypy errors resolved (Rule 65)
- Missing docstring on `get_recent_errors` (Rule 57)

## 2026.6.79
### Changed
- CLAUDE.md updated: version, slug, dynamic GIS discovery, known issues

## 2026.6.78
### Fixed
- Bay detail shows parent paddock name, fix `is_last_bay` after split

## 2026.6.77
### Fixed
- Refresh bay name on map/list after rename, fix bay detail navigation

## 2026.6.76
### Fixed
- Bay-split naming collision: use max existing bay number, not count

## 2026.6.75
### Changed
- Separate Setup Map (infrastructure) from Control page (devices/automation)

## 2026.6.74
### Fixed
- Split logic: paddock split only when no bays, bay split for subdivision

## 2026.6.73
### Added
- Mobile bay detail view with full device assignment

## 2026.6.72
### Fixed
- Zoom reset after split, add bay-level splitting
- Split-with-lines: auto-complete in-progress polyline on Apply Split

## 2026.6.71
### Added
- Bay detail panel — click bay on map to configure

## 2026.6.70
### Added
- "Use Entire Paddock as 1 Bay" option + buffer input replaces slider

## 2026.6.69
### Fixed
- Store GIS boundary on enable + split reads from DB

## 2026.6.68
### Fixed
- LogRecord reserved key `name` crash (Rule 88)

## 2026.6.67
### Changed
- Rename Config tile to Paddock Setup, link directly to setup map

## 2026.6.66
### Added
- Split paddock into bays — draw lines + buffer

## 2026.6.65
### Added
- W04 rebuild — Setup Map with paddock enable + bay drawing

## 2026.6.64
### Fixed
- Map zoom — match GIS features to PWM paddocks by name

## 2026.6.63
### Fixed
- Addon hostname — underscores to hyphens for Docker DNS

## 2026.6.62
### Fixed
- Paddock proxy — dynamic GIS slug discovery + available endpoint

## 2026.6.61
### Added
- ESPHome firmware sync — managed includes from PWM repo

## 2026.6.60
### Changed
- Full compliance pass — Rules 29, 59, 60, 92, 93

## 2026.6.59
### Added
- Full quality stack — smoke tests, mypy, bandit, 4-gate run.sh
- Ruff zero violations

## 2026.6.58
### Changed
- CLAUDE.md Rule 84 sections added
- Panel title set to PWM

## 2026.6.57
### Changed
- Bright orange paddock boundaries on satellite map

## 2026.6.56
### Fixed
- Map — show all GIS paddocks, use `properties.id` not `paddock_id`

## 2026.6.55
### Added
- Proxy logging for paddock fetch debugging

## 2026.6.54
### Fixed
- Paddock proxy route — `/api/paddocks-proxy`

## 2026.6.53
### Added
- GIS paddock proxy — map shows Core/GIS paddock boundaries

## 2026.6.49
### Changed
- Security improvements
- Bug fixes and enhancements
