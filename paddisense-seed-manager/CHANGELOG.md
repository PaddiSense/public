# PaddiSense Seed Manager — What's New

## 2026.8.21

**Fixes a brand-new install that would not start.** On a freshly installed add-on — not an existing
one — start-up stopped because it could not see a database password, even though it was able to
work one out for itself from this box's own key. It now checks whether the password can be derived
before insisting on being handed one. **Existing installs were never affected**; if yours is
already running, nothing changes.

## 2026.8.20

**Security: the factory database password is gone from the last place it remained** — the
database restore path used when recovering from a backup. Every other place was cleared
previously; this was the one site the earlier sweep missed. The add-on now fails safely rather
than falling back to a known default. No action needed on your part.

## 2026.8.19

**Every page now tells you if the box is not connected to PaddiSense.** A small, dismissable
note. It never blocks you or locks any page — it is there so a box that has quietly dropped its
connection does not look perfectly normal.

**Security: the factory database password is gone from the add-on's start-up and connection
settings.** No action needed on your part.

## 2026.8.18

**Faster start-up.** Removed duplicate code checks from add-on start — they already run in the build pipeline.

## 2026.8.17

**Delete a grading order.** Admins can now delete an order that was set up wrong (for
example, before Long-Row lots were selectable) and reissue it correctly. Deleting returns
all withdrawn stock to its source locations and removes the order's records completely.
Completed orders cannot be deleted.

## 2026.8.15

**Grade Long Rows separately.** When a variety has Long-Row bags in storage, creating a
grading order now offers a Long Row step — pick the row you are cleaning (e.g. LR5) and the
order only draws from that row's bags, never another row's. The row number stays with the
graded seed through to the storage views, and the kiosk shows it on the order and stepper
screens so it's always clear which row is being cleaned. Varieties without Long-Row bags see
no change.

## 2026.8.14

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are
with a cryptographic token before they can change this add-on's licence or permissions.
Previously, being on the box's internal network was treated as sufficient proof.

## 2026.8.13

- A newly installed add-on now stays on its activation screen until you enter your licence.
  Nothing changes for an add-on you are already using: once it has been activated it keeps
  working, and a later licence change or renewal will not lock you out of your own data.
