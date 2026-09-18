# PaddiSense Sugar — What's New


## 2026.9.6
**Harvest order changes tell you when they didn't save.** Moving a block up or down the harvest order now tells you
if the change was refused, instead of the row quietly jumping back.

## 2026.9.5

- **Behind-the-scenes quality work — nothing changes in how you use Sugar.** Stricter code checking and faster, safer log handling.

## 2026.9.4

**Security fix, plus behind-the-scenes hardening — nothing changes in how you use SugarSense.**

A block's class label could be set in a way that ran as code when someone else opened the harvest plan, Moddus or
irrigation pages; it now always shows as plain text. Your licence details are also now stored encrypted on your box,
and your existing licence keeps working.

## 2026.9.3

**Fixed: only a supervisor can rebuild your harvest schedule.**

Recalculating the harvest plan replaces every row of your schedule. Until this release, any
signed-in account could trigger that — including view-only accounts. Now it takes a supervisor,
the same as changing the harvest order or the group economics. Nothing you have already planned
is affected.

## 2026.9.2

**Security: the browser protections now apply to every response, including "please log in".**
The pages you use already carried the standard browser security headers; the short "not logged in"
and "redirect to login" replies did not. They now do. Nothing changes in how you use SugarSense.

## 2026.9.1

**Assets, parts, pre-starts, issues, chemical products and weather stations can now only be created or
changed by a supervisor, and deleted by an admin.** Before this, any signed-in account could change them.
Viewing is unchanged.

## 2026.8.18

**Brand-new installs start correctly.** On a freshly installed box the add-on could stop straight
after installing, with nothing to show you why. It now works out its own database password the way
it was always meant to, so a new install starts first time. Existing installs were never affected
and are unchanged.

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

**Security: the factory database password is gone from the last two places it remained.** The
add-on now refuses to start with a blank credential rather than falling back to a known default.
No action needed on your part.

## 2026.8.16

**Faster start-up.** Removed duplicate code checks from add-on start — they already run in the build pipeline.

## 2026.8.15

**Security update — no visible changes.** New installs no longer use a shared factory
database password; each box now gets its own locked-down database account. Existing
installs are updated automatically and nothing changes in how you use the add-on.

## 2026.8.14

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are with
a cryptographic token before they can change this add-on's licence or permissions. Previously,
being on the box's internal network was treated as sufficient proof.

## 2026.8.13

- A newly installed add-on now stays on its activation screen until you enter your licence.
  Nothing changes for an add-on you are already using: once it has been activated it keeps
  working, and a later licence change or renewal will not lock you out of your own data.
