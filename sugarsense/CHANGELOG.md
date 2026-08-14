# PaddiSense Sugar — What's New

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
