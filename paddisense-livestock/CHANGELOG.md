# PaddiSense Livestock — What's New

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
