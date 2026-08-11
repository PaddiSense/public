# PaddiSense Store — What's New

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
