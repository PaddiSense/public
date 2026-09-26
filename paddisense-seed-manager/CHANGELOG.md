# PaddiSense Seed Manager — What's New


## 2026.9.13

**New PaddiSense colours on every screen.** Seed Manager now uses the light grey PaddiSense look
everywhere — the office screens, the shed kiosk, and the login and licence pages — with dark text on
light cards and white writing on coloured buttons. Buttons you can't press yet now look greyed out.
The printed grading report still prints black on white.

## 2026.9.12

- **🔴 Security: updated a networking library that had two published vulnerabilities.** Most
  PaddiSense add-ons had already been updated; Seed Manager had been missed. No action is
  needed on your part.

## 2026.9.11

**Kiosk exit PIN.** If no exit PIN had ever been set, the settings page showed `1234` in the box — so
saving it would have made `1234` your real PIN. The box is now empty until you choose one, and the
page tells you kiosk mode cannot be exited until you do.

## 2026.9.10

**Easier to read, and printing works again.** Buttons and cards now use the new PaddiSense light theme properly, and a printed detail page is dark text on a light page again instead of solid black.

## 2026.9.9

**Delete works on the kiosk.** Whoever is signed in as the kiosk operator can now delete a docket or a bag weighed in
the last 24 hours — no PIN. The stock is put back and the delete is recorded under that operator. Older dockets are
still deleted from the office.

## 2026.9.8

**Behind-the-scenes code checks tightened.** Nothing changes in how you use Seed Manager.

## 2026.9.7

**The kiosk no longer pretends a delete worked.** Deleting a docket or a bag on the shed kiosk has needed the kiosk PIN
since April, but the kiosk never asked for it, so the delete was refused while the screen acted as if it had worked.
The kiosk now tells you the delete needs the PIN, and nothing disappears from the screen that is still saved.

**A bag that didn't save keeps its weight.** If saving a bag was refused, the weight used to reset to zero. It now stays
on screen with a message saying why, so you can fix it and save again.

**Racks, silos and bag lots tell you when a change didn't save**, instead of looking like it worked.

## 2026.9.6

**No visible change.** A tidy-up in the stock movement form so an automated release check can read its script.

## 2026.9.5

**Behind-the-scenes fixes — nothing changes in how you use Seed Manager.**

- The database export file is now named with today's local date (it could show yesterday's date early in the morning).
- Dates and times follow your box's time zone reliably.
- Security housekeeping: tighter handling of access keys and faster, safer log handling.

## 2026.9.4

**Behind-the-scenes security hardening — nothing changes in how you use Seed Manager.**

The protective browser settings Seed Manager already sends with its pages now also go out with its "please sign in"
and "request refused" responses.

## 2026.9.3

**Behind-the-scenes security hardening — nothing changes in how you use Seed Manager.**

Your licence details are now stored encrypted on your box, and your existing licence keeps working. Seed Manager also
refuses malformed settings that could have pointed its moisture-sensor reads or add-on store registration somewhere
they should not go.

## 2026.9.2

**Security fix: names and notes typed into Seed Manager can no longer run as code on someone else's screen.**

Text that people enter — truck notes, variety and generation names, seed sources, bin and silo codes, sensor names —
was placed onto some pages in a way that let a specially crafted entry act as a script when another person opened
that page. Every one of those places now shows the text exactly as typed and nothing more. Nothing you have entered
has changed.

## 2026.9.1

**The shed kiosk now records WHO did the work — and only a chosen operator can record it.**

The kiosk screen in the shed is meant to be walk-up: no login, just tap your name and enter your
PIN. That part has not changed. But until now the kiosk would accept work from anyone who could
reach the address, without a name attached — those entries were recorded as "kiosk" with nothing
in the audit trail. It was also possible to be recorded as someone else without ever knowing
their PIN.

From this version: reading the kiosk is still open to anyone at the tablet, recording work needs
an operator chosen on the screen, and every kiosk entry carries that operator's name in the audit
log. Repeated wrong PINs now pause briefly instead of allowing unlimited guesses. Signing out of
the kiosk properly ends the session.

Also fixed: restoring a backup treated the table names inside the uploaded file as instructions
rather than as names.

## 2026.8.27

**Fixes an error when creating a grading order.** The previous version could refuse valid long row
orders and then show "Failed to create grading order" instead of the reason. Creating orders works
normally again, and the long row weight check still refuses a source heavier than that long row
actually holds.

## 2026.8.26

**Long row grading orders no longer report grain from other long rows as loss.** When a bin holds
several long rows, a grading order for one of them now takes only that long row's bags. Previously it
took the bin's whole weight, so completing the order recorded everything else in the bin as lost —
even when all the grain was accounted for.

The weight shown for each source location is now that long row's share of that location, and an order
cannot draw more than the long row actually holds there.

## 2026.8.25

**The Operator name now fills in when you open Seed Manager from Home Assistant.** In the previous
version it only filled in for people who signed in with a Seed Manager account, so for most users the
field stayed empty. It now uses your Home Assistant name, and you can still type over it.

## 2026.8.24

**The Operator name is filled in for you.** When you create a grading order, the Operator field now
starts with your own name, and you can still type over it. If you are working through the Home
Assistant side panel rather than signing in with your own account, the field stays blank so a real
name gets recorded.

## 2026.8.23

**Long row grading orders now show weights in kilograms.** The grading order screen used to report
everything in tonnes, so a 13.35 kg bag lot appeared as 0.01t and a small loss as 0.00t. Long row
orders now show kilograms to two decimal places throughout that screen.

Ordinary grading orders are unchanged and still show tonnes.

## 2026.8.22

**Long row grading now accepts part-kilogram weights.** Long rows are bagged in small lots, so their
weights can now be entered and shown to two decimal places — 13.35 kg rather than 13 kg. On the shed
kiosk, the grading gross and tare buttons step in finer amounts (10, 1, 0.1 and 0.01 kg) when you are
working a long row order.

Ordinary grading orders are unchanged: they keep whole-kilogram entry and the larger kiosk buttons.

**Also fixed:** editing a graded output could quietly round its weight down to the nearest kilogram
when you saved another change on the same row. It now keeps the weight you recorded.

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
