# PaddiSense Safety — What's New

## 2026.8.18

**New installs: your first admin password is now recoverable.** On a brand-new install the add-on
creates an admin account with a randomly generated password. Previously that password was not
retrievable by anyone — a genuinely fresh install could not be signed into. It is now written to a
protected file inside the add-on (`/data/.admin_initial_pw`) for you to read once, sign in with,
and change. **Existing installs are unaffected** — your current login still works.

**Every page now tells you if the box is not connected to PaddiSense.** A small, dismissable
note. It never blocks you or locks any page — it is there so a box that has quietly dropped its
connection does not look perfectly normal.

**Security: the factory database password is gone from the last two places it remained.** The
add-on now refuses to start with a blank credential rather than falling back to a known default.
No action needed on your part.

## 2026.8.17

**Faster start-up.** Removed duplicate code checks from add-on start — they already run in the build pipeline.

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
