# PaddiSense Assets — What's New

## 2026.10.20

**Tidier Config.** The unused "Prestart Categories" list is gone from the Prestart settings. Nothing read it; Templates is the one place
prestart checklists are set up. Pages now always use the lists you set in Config and never fall back to a built-in copy.

## 2026.10.19

**Hours and km agree everywhere.** The asset page, the reports and Hours Tracking all show the same latest reading, the newest one from a
prestart or a service. A corrected reading now replaces a mistyped high one in the reports, and machines that only have prestarts now show
up in Hours Tracking.

**Prestart history on the phone matches the desktop.** You can filter by asset, passed, failed or open issues. Each record shows engine hours,
km, notes and photos, with a link to its issue or the service that fixed it.

## 2026.10.18

Assets now publishes a small status summary that the PaddiSense support observer can read (no personal data, no passwords).

## 2026.10.17

The same improvements as 2026.10.16 (a small technical correction so it could be released).

## 2026.10.16

**More fixes from the full check.** Monthly prestarts are asked for once a month. Closing a maintenance request clears its
phone alert either way you do it. Locations are edited in one place, with a code and a move option. The prestart Next button
no longer stops you over optional items. Only people who can delete see a Delete button.

## 2026.10.15

**Fixes from a full check of the app.** Parts used on a service are now taken off stock. Supervisors and technicians see the
full lists in every form. Editing a service or part no longer loses its km, type or category. Issue categories are kept. Every
phone screen now uses the same forms as a computer.

## 2026.10.14

**Your prestart templates are now used.** The checklists you build in Config → Prestart Checklists are what the prestart
shows, on the phone and on a computer. If you picked a template for a particular machine, that machine now uses it. There is
one prestart editor in Config.

## 2026.10.13

**Locations are set up in one place.** Sites, areas and storage bins are now added and edited in Config → Locations.
Supervisors get a Locations tile on the home screen that opens it directly.

## 2026.10.12

**Cleaner phone menus.** Config and System now open like every other screen, with the Home button at the top and no
slide-out side menu. Home screen and Config tiles are all the same, bigger size.

## 2026.10.11

**MAIN is instant.** Tapping MAIN now goes straight to your start page, without Home Assistant reloading.

## 2026.10.10

**MAIN button.** The Assets home screen now has a MAIN button at the top left, where other screens have Home. It takes
you to your PaddiSense start page to open your other apps. (It replaces the tile added in 2026.10.9.)

## 2026.10.9

**A PaddiSense button to get to your other apps.** The Assets home screen has a new PaddiSense tile that takes you
back to your PaddiSense start page, so you can open Water, Farm or any other app without the Home Assistant menu.

## 2026.10.8

**One page for phone and desktop — the lists.** Assets, Locations, Services, Parts, Maintenance and Reports are now the same
on your phone as on a computer, with thumb-sized buttons and filters that fit the screen. The Assets list gains a
Location filter. In a maintenance request, the Update button's label is now visible.

## 2026.10.7

**One page for phone and desktop — assets first.** An asset's page and its Services, Prestarts, Maintenance, Parts, Photos,
Videos and Report pages are now the same on your phone as on a computer, with thumb-sized buttons. You can now delete a
photo from the photo viewer, and photo uploads from the phone work again. The dashboard has quick-action tiles everywhere.

## 2026.10.6

**Bigger buttons on phones and tablets.** Every button is now thumb-sized on a touch screen, and button labels no longer wrap onto two lines.

## 2026.10.5

**Trial switch.** On an asset page, tap **Try the new single page** to see the trial layout, and **Back to the current page** to return.

## 2026.10.4

**Trial: one asset page for phone and desktop.** For testing only — open an asset with `?layout=single` added to the
address to see the new single page. Nothing changes unless you add it.

## 2026.10.3

**Prestart checks can be Required or Optional.** In each prestart template you can now tick which checks must be
answered. An optional check left blank is recorded as N/A and never fails the prestart.

**Engine hours and km are part of the checklist.** The separate hours box on the first prestart screen is gone — the
Engine Hours / Odometer checks in the list are used instead, and the asset's page now shows the latest hours and km
(from a prestart or a service, whichever is newer).

## 2026.10.2

On an iPad or an Android tablet you now get the full desktop pages instead of the phone layout. Phones are unchanged.

## 2026.10.1

**Location privacy fix:** a user who can only see one location no longer sees other locations' costs in the summary
report's "cost by location" table.

## 2026.9.12

**Behind-the-scenes update.** Nothing changes in how you use ASM Pro.

## 2026.9.11

**Behind-the-scenes update.** Nothing changes in how you use ASM Pro. This update also brings you the improvements listed below since your last update.

## 2026.9.10

**Security update.** A third-party networking library bundled with ASM-Pro was updated to close
three published vulnerabilities. An internal packaging fix also restores a test tool that had been
missing from the build since July. Nothing you do changes.

## 2026.9.9

**Activating a licence works.** On some browsers the Activate Licence button did nothing when pressed. It now works.

## 2026.9.8

**Easier to read, and button rows fit a narrow window.** Buttons, highlights and cards now use the new PaddiSense light theme properly, and rows of buttons wrap instead of squashing when the window is narrow.

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
