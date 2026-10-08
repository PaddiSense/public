# PaddiSense Planner — What's New


## 2026.10.3

**MAIN button.** The Planner home screen has a MAIN button at the top left that takes you to your PaddiSense start
page. Project Assumptions and Actuals now have their own tiles on your phone, and the tiles are bigger.

## 2026.10.2

On an iPad or an Android tablet you now get the full desktop pages instead of the phone layout. Phones are unchanged.

## 2026.10.1

- **New look.** Planner now uses the same light grey PaddiSense theme as your other add-ons, replacing the old dark theme. Nothing
  about your plans, prices or water records changes.
- This update also brings you the two fixes below (2026.9.7 and 2026.9.8), which had not reached your box yet.

## 2026.9.8

- **🔴 Security: updated a networking library that had two published vulnerabilities.** The
  other PaddiSense add-ons had already been updated; Planner had been missed. No action is
  needed on your part.

## 2026.9.7

- **🔴 Fixed: a crop plan could use the wrong commodity price.** The price lookup matched on a
  partial name, so a price set containing both "Wheat" and "Durum Wheat" could answer "Wheat"
  with either price, and a blank crop name could pick any price at all. The lookup now matches
  the commodity exactly, and where a name genuinely is ambiguous it reports no price instead of
  guessing — so the paddock shows zero income rather than a confident wrong margin.

## 2026.9.6

**Easier to read, and tabs fit a narrow window.** Buttons, tabs and cards now use the new PaddiSense light theme properly, and rows of tabs and buttons wrap instead of squashing when the window is narrow.

## 2026.9.5

**Security housekeeping.** The part of Planner that hides passwords and keys from its logs has been updated to the
latest fleet version. Nothing changes in how you use Planner.

## 2026.9.4

**Behind-the-scenes security hardening — nothing changes in how you use Planner.**

The protective browser settings Planner already sends with its pages now also go out with its "please sign in" and
"not allowed" responses.

## 2026.9.3

**Your licence details are now stored encrypted.**

The licence Planner keeps on your box, and the private address it uses to check in, are now encrypted where
they are stored, with a key that stays on your box. Your existing licence keeps working — there is nothing
to re-enter.

## 2026.9.2

**Behind-the-scenes security hardening — nothing changes in how you use Planner.**

Planner's automatic add-on store registration now refuses a malformed access token instead of passing it
on, so a tampered setting can no longer send your box to fetch add-ons from somewhere else. We also added
checks that prove each person's password is stored separately and securely, and that every database
upgrade can be safely undone. Your plans, prices and water licences are untouched.

## 2026.9.1

**Only managers can change your plans, prices and water licences now.**

Anyone signed in to Planner — at any permission level — could add, change or delete your budget
figures, input prices, crop rotations and water licences. Viewing and changing were never separated,
so an account meant only to look at the numbers could rewrite them. Other PaddiSense add-ons that
read Planner over the box's internal link could do the same, even though that link is meant to be
read-only.

Planner now checks your **role** before every change: manager or above to make one, everyone else
can still read. Nothing you have entered has changed, and activating a licence on a new box works
exactly as before.

## 2026.8.21

**A brand-new box could not start Planner. Fixed.**

Installing Planner on a **new** box left it unable to start — it was waiting to be given a database
password that it is supposed to work out for itself. Existing boxes were never affected: yours has
been running normally, and nothing about your plans, water licences or prices changes.


## 2026.8.20

**Security: reading your paddocks and product list is now strictly read-only.** Planner pulls
paddock information from Farm and product information from Store. It was doing that through an
account that was technically able to change those records, even though it only ever read them —
the safeguard was "we don't write" rather than "we can't write". Those reads now use a dedicated
account with no ability to modify anything. Nothing changes in how Planner works; this removes a
way a future bug could have altered your Farm or Store records.

## 2026.8.17

**Faster start-up.** Removed duplicate code checks from add-on start — they already run in the build pipeline.

## 2026.8.16

**Security update — recommended for all growers.** The add-on now connects to its database with
its own restricted account instead of the shared administrator account, with no stored password
(it proves itself using your box's own key). Also removes a leftover hidden menu from mobile
pages and makes the add-on's start-up checks more reliable.

## 2026.8.15

**Security hardening — no user-visible changes.** Permission updates sent to this add-on are now
cryptographically verified as coming from PaddiSense Core. Previously a valid-looking update from
elsewhere on your box could have changed who is allowed to use it.

## 2026.8.14

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are
with a cryptographic token before they can change this add-on's licence or permissions.
Previously, being on the box's internal network was treated as sufficient proof.

## 2026.8.13

- A newly installed add-on now stays on its activation screen until you enter your licence.
  Nothing changes for an add-on you are already using: once it has been activated it keeps
  working, and a later licence change or renewal will not lock you out of your own data.
