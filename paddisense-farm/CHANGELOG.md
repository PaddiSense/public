# PaddiSense Farm — What's New

## 2026.8.26

**Licence codes are now signature-checked everywhere.** The GSM enrolment card verifies
Admin's signature on a pasted licence code, same as the licence page — a tampered or
hand-made code is refused.

**Map: bays now follow the layer tree exactly.** Bays are drawn only by their layer
checkboxes; a newly drawn bay ticks itself and zooms into view, and unticking "Bays"
always clears them from the map.

## 2026.8.25

**The map tree stays where you left it.** Drawing a bay used to unfold the "Bays" branch of
*every* paddock in the tree, not just the one you were working in. Now only the branches you had
open stay open.

## 2026.8.24

**Quality assurance improvements — no user-visible changes.** The full automated test suite now
runs green, and additional security checks (personal-data log masking, map-label safety,
per-operator logins, signed licence authority) are verified on every release.

## 2026.8.23

**Internal consistency fix — no user-visible changes.** The signing helper used for Knowledge
Bank requests now shares the one canonical implementation, so all requests to your Grower
Services Manager are signed the same way.

## 2026.8.22

- **Recording a sowing event now offers the variety list on every device.** Varieties are
  filtered to the crop you pick, and the same list appears in the map recorder and the wizard,
  on desktop and mobile alike.
- Weather capture in the event wizard now reads from the on-box Weather addon correctly (it
  silently captured nothing before).

## 2026.8.21

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are
with a cryptographic token before they can change this add-on's licence or permissions.
Previously, being on the box's internal network was treated as sufficient proof.

## 2026.8.20

- When you push boundaries to your Grower Services Manager, Farm now checks that everything you
  sent actually arrived. If any are missing you'll be told how many and asked to send again,
  instead of the push simply looking successful.

## 2026.8.19

- Pushing boundaries to your Grower Services Manager now reports what actually happened. It
  previously said "0 created, 0 updated" even when the push had worked, which made a successful
  send look like it had done nothing. You now see how many boundaries were applied and how many are
  waiting to be accepted — and if the reply can't be read, it says so plainly instead of showing
  zeros.

## 2026.8.18

- Fixed the connection to your Grower Services Manager. Some requests were being rejected even
  though your connection code was correct.
