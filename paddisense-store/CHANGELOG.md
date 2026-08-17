# PaddiSense Store — What's New

## 2026.8.17

**New installs get a randomly generated admin password instead of a known default.** On a
brand-new install the add-on now creates its admin account with a random password, written to a
protected file inside the add-on (`/data/.admin_initial_pw`) for you to read once, sign in with,
and change. **Existing installs are unaffected** — your current login still works. If your admin
account is still on the old default password, you will see a warning at start-up asking you to
change it.

**Every page now tells you if the box is not connected to PaddiSense.** A small, dismissable
note. It never blocks you or locks any page — it is there so a box that has quietly dropped its
connection does not look perfectly normal.

**Security: the factory database password is gone from the last three places it remained**,
including the database restore path used when recovering a backup. The add-on now fails safely
rather than falling back to a known default. No action needed on your part.

## 2026.8.16

**Licence codes are now signature-checked, and an unsigned one is refused.** Every licence
PaddiSense has issued since 3 August is signed, so this affects nothing in normal use — it closes
the door on a hand-made or tampered licence code being accepted.

## 2026.8.15

**Faster start-up.** Removed duplicate code checks from add-on start — they already run in the build pipeline.

## 2026.8.14

**Security — how the add-on connects to its database.** This update changes Store
to use its own restricted database account instead of the shared administrator
one. Nothing changes in how you use the add-on.

**Internal improvements — no user-visible changes.** Repaired two start-up checks
that had stopped working, so problems are reported instead of being missed.

## 2026.8.13

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are with
a cryptographic token before they can change this add-on's licence or permissions. Previously,
being on the box's internal network was treated as sufficient proof.

## 2026.8.12

- A newly installed add-on now stays on its activation screen until you enter your licence.
  Nothing changes for an add-on you are already using: once it has been activated it keeps
  working, and a later licence change or renewal will not lock you out of your own data.
