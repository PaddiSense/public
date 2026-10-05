# PaddiSense Livestock — What's New

## 2026.10.6

**MAIN button.** The Livestock home screen has a MAIN button at the top left that takes you to your PaddiSense start
page. CSV Import now has its own tile on your phone, and the tiles are bigger.

## 2026.10.5

**Logging an event on a mob now saves properly.** Joining, shearing, pregnancy scanning and weighing entered through
Mobs → Log event are now recorded against the mob. Before this fix a preg scan or a weighing was not saved at all, and a
joining or shearing was saved without its mob. If a save is refused, the page now tells you why.

## 2026.10.4

On an iPad or an Android tablet you now get the full desktop pages instead of the phone layout. Phones are unchanged.

## 2026.10.3

**Farm paddocks now appear in Livestock on every box** — Livestock finds the Farm add-on wherever it is installed.

**Security update:** a network library (urllib3) updated to fix newly published vulnerabilities. No change to how Livestock works.

## 2026.10.2

- Changing a breeding group's untagged head count now changes its paddock's count too, when the group is in one paddock. If it is in several, you are told to record the change from the paddock it happened in.

## 2026.10.1

- You can record a **Death** or a **Cull** from a group's Event button on the Mobs page — the head comes off the group and the paddock it is in.

## 2026.9.9

**Behind-the-scenes update.** Nothing changes in how you use Livestock. This update also brings you the improvements listed below since your last update.

## 2026.9.8

**Security update.** A third-party networking library bundled with Livestock was updated to close
two published vulnerabilities. Nothing you do changes; the update is inside the add-on.

## 2026.9.7

**Easier to read.** Buttons, tabs and cards now use the new PaddiSense light theme properly — white text on coloured buttons, dark text on every card.

## 2026.9.6
**Behind-the-scenes code checks tightened.** Nothing changes in how you use Livestock.

## 2026.9.5
**New breeding groups tell you if their animals weren't added.** If the group was created but its tagged animals
could not be added to it, the page used to say "Created" anyway. It now tells you, so you can add them from the group.

## 2026.9.4

**Mistyped entries are rejected with a clear message.** If a head count or similar number was sent in a form
Livestock could not read, it could show a generic error instead of saying what was wrong. It now tells you which
field needs a whole number, and nothing is saved until it is fixed.

## 2026.9.3

**Your licence details are now stored encrypted.** The web address Livestock uses to check in, and the
licence itself, used to sit in the database as readable text. They are now encrypted, and a licence saved
before this update keeps working. This release also tightens a paddock-sync setting so it can only point at
your other PaddiSense add-ons, and adds checks that let a database update be safely undone. Nothing changes
in how you use Livestock.

This release also includes 2026.9.2 and 2026.9.1, below, which had not reached growers yet.

## 2026.9.2

**Livestock is harder to overload.** A security review found a few places where a flood of junk
requests could make the add-on slowly use more and more memory until it was restarted. Those are now
capped, very large uploads are turned away before any work is done on them, and list pages refuse
nonsensical sizes. Nothing changes in how you use Livestock.

This release also includes 2026.9.1, below, which had not reached growers yet.

## 2026.9.1

**Security: the browser protections now apply to every response, including "please log in".**
The pages you use already carried the standard browser security headers; the short "not logged in"
and "redirect to login" replies did not. They now do. Nothing changes in how you use Livestock.

## 2026.8.19

**When the add-on cannot reach your paddock data, it now says so instead of reporting an empty
farm.** If Farm (or Core) could not be reached at all — the add-on stopped, or the box off the
network — your paddock list said **"No paddocks found"**. That reads as *your farm has no
paddocks*, when what actually happened is that nothing could be asked. It now tells you it cannot
reach Farm (or Core), so you are pointed at the real problem. A source that genuinely has no
paddocks still says "No paddocks found", exactly as before. **No paddock data was ever lost or
overwritten by this** — your paddock list is only updated when one is actually received.

## 2026.8.18

**Fixes a brand-new install that would not start.** On a freshly installed add-on — not an
existing one — start-up refused to continue because it could not see a database password, even
though it was able to work one out for itself from this box's own key. The check now asks whether
the password can be derived before insisting on being handed one. **Existing installs were never
affected**; if yours is already running, nothing changes for you.

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

**Maintenance release — no user-visible changes.** Internal build checks now report
honestly when they find problems (previously a counting bug could hide them), a
security test was brought in line with the hardening shipped in 2026.8.14, and the
shared look-and-feel files were refreshed. This update also delivers the database
credential improvements to every box via the catalog.

## 2026.8.14

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are with
a cryptographic token before they can change this add-on's licence or permissions. Previously,
being on the box's internal network was treated as sufficient proof.

## 2026.8.13

- A newly installed add-on now stays on its activation screen until you enter your licence.
  Nothing changes for an add-on you are already using: once it has been activated it keeps
  working, and a later licence change or renewal will not lock you out of your own data.
