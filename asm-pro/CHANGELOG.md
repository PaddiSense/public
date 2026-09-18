# PaddiSense Assets — What's New

## 2026.9.7

**Behind-the-scenes code checks tightened.** Nothing changes in how you use Assets.

## 2026.9.6

**Fault photos on a prestart tell you if they didn't attach.** If a photo could not be added to the fault a prestart
raised, it used to disappear without a word. You are now told how many photos did not attach.

**Deleting, assigning, ignoring or scheduling tells you when it didn't save**, instead of saying it worked.

## 2026.9.5

- **Ignored issues now show who ignored them, why and when.** Previously that information was not being saved.

## 2026.9.4

- **Dates fixed.** A new service record now defaults to today's date even early in the morning, and "ignored" issues show the correct time.

## 2026.9.3

**Your licence details are now stored encrypted, and new installs set up the prestart template library correctly on
the first start.** Previously a brand-new install needed a restart before template changes could be saved. Nothing
changes in how you use Assets.

## 2026.9.2

- **Security: notification-group targets are now checked.** Only Home Assistant phone
  notification services can be saved as a group target; anything else is refused when saved and
  ignored when sending. Existing groups keep working; a target that is not a notification service
  is skipped and shown as refused in the test-notification result.
- **Security: very large sign-in or form submissions are now refused before they are read.**
  No change for normal use.
- Includes everything under 2026.9.1 below.

## 2026.9.1

- **Security: uploading an oversized photo or QR image is now refused as it arrives, instead of
  after the whole file has been received.** Previously the size limit was only checked once the
  upload was complete, so a very large file could occupy the add-on's memory before being rejected.
  The limit and the error message you see are unchanged.
- **The "decode QR" upload now checks your role the same way every other upload does.** No change
  for normal use.
- **Security: the browser-protection headers now also arrive on sign-in redirects and refused
  requests**, not only on pages you are signed into. No change for normal use.
- Includes everything listed under 2026.8.16 to 2026.8.18 below, which had not yet reached the
  store.

## 2026.8.18

- Fixed: a brand-new installation could fail to start with a configuration error, even when
  correctly set up. Existing installations were unaffected.

## 2026.8.17

- **Security: your first-boot admin password is no longer written into the log.** Assets already
  generated a random admin password on a new install, but it was printed in clear text in the
  start-up log, where anyone able to read logs could see it. It is now written to a protected file
  inside the add-on (`/data/.admin_initial_pw`) instead — read it once, sign in, change it.
  **If you set up this add-on previously, change your admin password**, since the original may
  still be sitting in old logs.

- **Every page now tells you if the box is not connected to PaddiSense.** A small, dismissable
  note. It never blocks you or locks any page.

- **Security: the factory database password is gone from the add-on's start-up defaults.** No
  action needed on your part.

## 2026.8.16

- **Reliability fix: notifications could stop working silently.** The add-on had two different
  ways of reading its Home Assistant access credential, and the older one could hand back an
  empty value without falling back — leaving notifications failing quietly with nothing obvious
  in the log. There is now a single way of reading it. If you have had Assets notifications go
  missing without explanation, this is the likely cause.

## 2026.8.15

- **Location dropdowns now match your Site Structure.** The Site / Area / Location pickers on the
  Add and Edit forms for parts and assets now show exactly the same structure you set up on the
  Configuration page — anything you add there appears in the pickers straight away. Existing
  records are untouched; the hierarchy is simply displayed consistently everywhere
  (Site → Area → Location).
- Reliability: internal database settings hardened. No visible change on a healthy box.

## 2026.8.13

**Security hardening — no user-visible changes.** Add-ons on your box now prove who they are with
a cryptographic token before they can change this add-on's licence or permissions. Previously,
being on the box's internal network was treated as sufficient proof.

## 2026.8.12

- A newly installed add-on now stays on its activation screen until you enter your licence.
  Nothing changes for an add-on you are already using: once it has been activated it keeps
  working, and a later licence change or renewal will not lock you out of your own data.
