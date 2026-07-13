# Changelog

## 2026.7.17
- Stronger licence security: connection codes and licence updates are now always verified
  before they are accepted. If an older connection code is refused during enrolment,
  generate a fresh code in your PaddiSense portal and enrol again.
- Licence deactivation is now managed from your PaddiSense provider rather than the
  per-add-on buttons in Core, so a licence can no longer be removed by mistake.
- Faster automatic recovery if the system's database connection is interrupted, and an
  on-screen alert if the box has not been able to report in for more than 15 minutes.
- More reliable backups: a failed backup can no longer overwrite a good one.

## 2026.7.10
- New: Core can now be locked behind a sign-in. Set the owner password and give your admin
  user their own password on the Access page — from then on, opening Core asks for a sign-in.
  Until you set those passwords, nothing changes.
- Sign in with your name as it appears in Home Assistant ("Peter McDonnell" works — exact
  spelling of the account name is not required)
- Opening Core now lands on the system dashboard, showing every add-on with its live version
  and health — this page previously showed add-ons as "not installed" by mistake
- Fixed sign-in not working when Home Assistant is accessed over a plain HTTP address
- A password recovery guide is included — an admin can always reset any password, and the
  owner login is always the way back in
- Reliability: per-user module access updates now reach every installed add-on
- Core sign-ins last 12 hours, so you sign in about once a day

## 2026.7.4
- More reliable database connections: add-ons now recover automatically after a password change instead of needing a restart
- Fixed an issue where reinstalling an add-on could break sign-in for other add-ons until keys were reset
- Uploaded backup restores now accept encrypted backup files only, protecting your data
- User access management: farm users are limited to the modules ticked for them
- Simpler user roles: operator, manager and admin
- Internal improvements to licensing and fleet health reporting

## 2026.6.404
- User management: add farm users and choose which modules each user can see
- Access management is limited to admin users

## 2026.6.382
- Maintenance + reliability improvements.

## 2026.6.378
- Fixed the Licences page: addon panels now expand so you can enter your connection code
- Internal improvements — no user-visible changes

## 2026.6.376
- Improved browser security protections
- Improved mobile interface readability and touch targets
- Better error messages on backup and restore operations
- Added system self-test and addon discovery endpoints
- File backup support for addon data directories
- Unified visual theme across all pages
- Internal improvements — no user-visible changes

## 2026.6.373
- Updated visual theme to match the PaddiSense standard look
- Improved sidebar navigation with icons
- Security dependency updates
- Improved startup logging and diagnostics

## 2026.6.370
- Backup now includes addon photos and files alongside database backups

## 2026.6.369
- Farm rename: all addon references updated from GIS to Farm

- Improved startup validation and error handling
- Internal security improvements
- Internal improvements — no user-visible changes

## 2026.6.363
- Boundary sync security: replay protection and payload integrity

## 2026.6.362
- Heartbeat security: signed heartbeats with replay protection
- Improved session security and cookie protection
- Rate limiting on sensitive operations
- Request size limits enforced
- Internal improvements — no user-visible changes

## 2026.6.356
- GHCR credential registration from connection codes
- Heartbeat aggregates all addon health
- Daily backup for all databases

## 2026.6.332
- Gateway cleanup and optimisation
- Weather release support
