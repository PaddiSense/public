# PaddiSense Planner — What's New

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
