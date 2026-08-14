# PaddiSense Seed Manager — What's New

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
