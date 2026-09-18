# PaddiSense Store — What's New

## 2026.9.4
**Security housekeeping.** The part of Store that hides passwords and keys from its logs has been updated to
the latest fleet version. Nothing changes in how you use Store.

## 2026.9.3

**Mistyped entries are rejected with a clear message.** If a quantity or similar value in a delivery or stock
movement could not be read, Store could show a generic failure. It now says which value needs fixing, and nothing
is recorded until it is.

## 2026.9.2

**Security: your licence details are now stored encrypted.** The add-on keeps a copy of your PaddiSense
licence, including a private connection address, in its database. Both are now encrypted on disk with a key
unique to your box. Your existing licence keeps working with nothing to re-enter, and nothing changes in how
you use Store.

## 2026.9.1

**Security: the browser protections now apply to every response, including "please log in".**
The pages you use already carried the standard browser security headers; the short "not logged in"
and "redirect to login" replies did not. They now do. Nothing changes in how you use Store.

## 2026.8.18

**Fixes a brand-new install that would not start.** On a freshly installed add-on — not an existing
one — start-up stopped because it could not see a database password, even though it could work one
out from this box's own key. It now checks whether the password can be derived before insisting on
being handed one. **Existing installs were never affected.**

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
