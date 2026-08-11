# PaddiSense Safety — What's New

## 2026.8.16

**Security update — installs a safer database configuration.** This add-on no longer ships with
a factory database password; it now uses its own dedicated, locked-down database account that is
set up automatically. No action needed on your part. Also includes internal reliability fixes to
the add-on's startup checks.

## 2026.8.15

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are with
a cryptographic token before they can change this add-on's licence or permissions. Previously,
being on the box's internal network was treated as sufficient proof.

## 2026.8.14

- A newly installed add-on now stays on its activation screen until you enter your licence.
  Nothing changes for an add-on you are already using: once it has been activated it keeps
  working, and a later licence change or renewal will not lock you out of your own data.
