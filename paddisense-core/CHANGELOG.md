# PaddiSense Core — Changelog

All notable changes to PaddiSense Core (system gateway).

## 2026.6.315
- Fix application logging — all addon log output now visible (heartbeat, backup, selftest)
- Add Store, Weather, GIS to heartbeat addon health discovery
- Fix fallback port map for addon health polling
- Heartbeat confirmed working to Admin

## 2026.6.312
- Fix licence management page (G01.B) — JS errors prevented Core licence from displaying
- Null checks on GSM status elements, missing function stub added

## 2026.6.309
- Fix addon port map for licence activation (GIS, Store, Weather, Livestock, ASM, Sugar)
- Correct ports for all 10 addons in discovery and licence forwarding

## 2026.6.307
- GSM boundary exchange section moved into GIS module card on G01.B
- Only visible when GIS addon is licensed

## 2026.6.304
- Backups write to /config/backups/ on host filesystem (survives addon reinstall)
- All 8 addon databases backed up daily with 3-day rolling retention
- Download button on backup files for USB export

## 2026.6.300
- Core stripped to system gateway — all farming logic moved to GIS addon
- Heartbeat, licences, addon discovery, backup, selftest only
- Consistent PaddiSense naming across all 10 addons

## 2026.6.297
- Security hardening: login rate limiting, path validation
- Paddock delete FK safety (nullify dependent records first)

