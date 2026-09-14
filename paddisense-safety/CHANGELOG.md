# PaddiSense Safety — What's New

## 2026.9.3

**Security fixes for the Safety map and paddock sync.** A zone or paddock name could carry hidden code that ran
when you hovered over it on the map; names are now always shown as plain text. Safety also looked for your Farm
add-on too loosely and could have sent its access key to a look-alike add-on; it now only talks to the real Farm
and Core add-ons. Your licence details are now stored encrypted. Nothing changes in how you use Safety.

This release also includes 2026.9.2, below, which had not reached growers yet.

## 2026.9.2

**Maintenance roll-up since 2026.9.1. Nothing you use day to day moves unless a line above says so.**


## 2026.9.1

- **Security: saving device preferences now requires you to be signed in.** That page previously
  accepted the request without a session. Nothing changes for normal use.
- **Security: the browser-protection headers now also arrive on sign-in redirects and refused
  requests**, not only on pages you are signed into. No change for normal use.
- **Security: a worker's notification target can now only be a phone notification service.**
  Previously a Safety manager could type any Home Assistant service name (or a path) into that
  field, and the add-on would call it with its own credentials. Now only `notify.…` services are
  accepted and sent. If a worker's notifications stop after this update, re-select the phone
  from the list on their user record.
- Includes the 2026.8.19 fresh-install fix below, which had not yet reached the store.

## 2026.8.19

- Fixed: a brand-new installation could fail to start with a configuration error, even when
  correctly set up. Existing installations were unaffected.

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
