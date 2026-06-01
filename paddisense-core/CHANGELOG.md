# Changelog

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
