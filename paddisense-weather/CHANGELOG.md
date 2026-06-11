# PaddiSense Weather — Changelog

All notable changes to PaddiSense Weather.

## 2026.6.39
- Per-station card: rain totals (Event / Today / Weekly / Monthly / Yearly) now grouped in a single column. Fix NaN on history chart x-axis.

## 2026.6.38
- API stations now show event / weekly / monthly / yearly rain totals (was only daily).

## 2026.6.37
- Fix NaN on API station wind direction charts.

## 2026.6.36
- Each station now shows when it last received data.

## 2026.6.35
- Fix Ecowitt API credentials wrongly showing "Not configured" after save.

## 2026.6.34
- Fix stations showing offline in steady weather.

## 2026.6.33
- Fix sensor cadence jitter: station-level liveness check covers all readers (temp / humidity / wind / pressure / rain) when any one entity is fresh.

## 2026.6.32
- Fix rain totals hidden between rain events.

## 2026.6.31
- Fix W04 Save / Remove buttons (slot-quoting bug).

## 2026.6.30
- Fix station lat / lon resetting on addon update.

## 2026.6.29
- Fix W03 slot 2 not clickable + slot fallback.

## 2026.6.28
- Fix unit-aware helpers honouring staleness check.

## 2026.6.27
- Fix offline detection: stale HA entities now return None.

## 2026.6.26
- Remove duplicate backup UI from W07 (Core handles backups).

## 2026.6.25
- Graceful shutdown handler. Duplicate backup loop removed.

## 2026.6.24
- Offline station badge on card header. Chart.js NaN axes fixed.

## 2026.6.23
- Full Golden Rules v2.1 compliance pass.

## 2026.6.22
- Fix W08 spray page crash. Station property paths normalised.

## 2026.6.21
- Fix windrose + wind chart canvas colours. Fix W04 radar styling.

## 2026.6.20
- New W08 Spray Conditions page — Delta-T, wind, inversion + 5-day outlook.

## 2026.6.19
- Semantic colour tokens — last Rule 14 gap closed.

## 2026.6.18
- New W06 Audit Log + W07 System Status admin pages. UI-configurable backup retention.

## 2026.6.17
- Fix spray banner showing °F as °C on rain-only gauges (unit conversion).

## 2026.6.16
- Migrate five TEXT-holding-JSON columns to JSONB.

## 2026.6.15
- Strict typing pass (mypy `disallow_untyped_defs`).

## 2026.6.14
- DRY pass — shared burn-rules JS extracted to `static/`.

## 2026.6.13
- 3-layer cache busting (path-versioned URLs, Cache-Control headers, server rewrite).

## 2026.6.12
- W03 map picker: satellite tiles for paddock-boundary visibility.

## 2026.6.11
- W03 map picker + typed station lat / lon + GSM-sync prep.

## 2026.6.10
- Tests for burn-rules CRUD + 3 regression tests.

## 2026.6.9
- CLAUDE.md rewrite. API envelope documented.

## 2026.6.8
- Audit gap closure pass.

## 2026.6.7
- Hotfix W02 stuck on "Loading…".

## 2026.6.6
- W02 burn forecast mobile redesign + per-site rules.

## 2026.6.5
- Hotfix v.4 dev-test crash.

## 2026.6.4
- Full 102-rule audit + W03 save fix.

## 2026.6.1
- Initial release — extracted from PaddiSense Core weather module
- Weather stations (local Ecowitt via HA + Ecowitt Cloud API)
- Open-Meteo 16-day forecast, Delta-T spray assessment, wind rose
- Burn forecast assessment (mixing height, ventilation index)
- Rain radar page with Windy embed (full resolution at any zoom)
- Paddock boundaries on radar via server-side proxy
- Settings page for station management and API credentials
- Background poller (5-minute cycle)
- Application logging fix for visible addon diagnostics
