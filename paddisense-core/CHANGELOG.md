# PaddiSense Core — What's New

> Plain-English release notes for growers. The full technical changelog lives in the
> source repo (`CHANGELOG.md`); this is the version that ships in the grower catalog.

## 2026.8.35

**Setting up a new box now completes on its own.** On a brand-new box the other PaddiSense add-ons
would install but then refuse to start — usually showing only *"An unknown error occurred"*, or
stopping seconds after launch. Each add-on needs its own database and its own database login, and on
a fresh box neither existed yet, so every add-on sat waiting for something that nothing was creating.
Core now creates each add-on's database, hands it the login it needs, and starts it.

**You can now run your own farm from the moment you install it.** Activating your licence and adding
users had come to require a *PaddiSense* administrator rather than the farm's own owner — so on a new
box the owner could not license the box and could not add anybody, including themselves. The Farm
Owner is the administrator of their own farm again, and can do both.

The separate `admin` account stays reserved as PaddiSense's way to help you back in if you are ever
locked out. It cannot be deleted or taken over — that is the one thing a Farm Owner cannot do, and it
exists so you always have a way back in.

**What you need to do:** on a NEW box, nothing beyond activating your licence — the other add-ons
should come up by themselves within a couple of minutes. On a box already running, nothing at all.

## 2026.8.34

**Setting up a brand-new box now works.** On a box that had never been set up, there was no way to
sign in: Core sent every page to the licence screen, activating a licence needed an administrator
account, and no administrator password was ever shown to you. There was no way through it.

A new box now opens straight onto a **"Claim this box"** screen where you choose the `admin`
password yourself. Once you set it, that screen closes permanently and you sign in normally to
activate your licence.

⚠ **This also unblocked installing the other PaddiSense add-ons.** They are pulled using
credentials that arrive with your Core licence, so on a box where Core could not be licensed, the
other add-ons would not install either — usually showing only *"An unknown error occurred"*.

**Security note, because it is a fair question:** the claim screen is reachable only from inside
Home Assistant on your own box — Core has no separate network port — so anyone who could open it
must already be able to sign in to your Home Assistant. The box also **notifies you the moment it
is claimed**, so if someone else does it you will know immediately. Once claimed, the screen never
reopens: not when a licence is removed or expires, and not if user accounts are deleted.

**What you need to do:** on a NEW box, set the admin password when the claim screen appears. On a
box that is already running, **nothing** — it stays exactly as it is and the claim screen is
already closed.

## 2026.8.33

**Not released on its own — included in 2026.8.34.** This version introduced the "Claim this box"
setup screen, but would also have re-opened that screen on boxes already up and running. That was
caught and corrected in 2026.8.34 before either version reached you, so the two ship together.

**What you need to do: nothing.** It is listed only so the jump from 2026.8.30 to 2026.8.34 has no
unexplained gaps.

## 2026.8.32

**Fix — disconnecting your GSM connection now reports honestly.** Disconnecting told you it had
worked even when the change had not reached the other add-on. Core now keeps re-sending the current
state until it is confirmed, so it corrects itself instead of leaving you with a screen that
disagrees with your farm.

**What you need to do: nothing.**

## 2026.8.31

**Fix — the licence page could show "Licensed" for a product that had been revoked.** Where a box
held both a licence and a later revoke for the same product, the page could show the wrong one.
Revocations now take precedence, so what you read matches your actual licence state.

**What you need to do: nothing.** Your machine control, your data and your pages are unaffected by
a revoke — as always, a revoke only stops updates and syncing with PaddiSense.

## 2026.8.30

**Housekeeping — the security update in 2026.8.28 now always records what it did.** When Core moves
your stored service credentials onto its new private encryption key, it writes a line to the add-on
log every time it checks, including when there is nothing left to move. Previously it only wrote a
line when it changed something, which made "everything is already done" look the same as "it never
ran".

**What you need to do: nothing.** No change to how anything works — this only makes the update
easier to confirm from the log.

## 2026.8.29

**Internal fix — a database password change could have disrupted your add-ons.** The routine that
updates the database password across PaddiSense add-ons was writing the wrong password to add-ons
that use their own dedicated login. It now only updates the add-ons that actually need it, and says
clearly in the log which ones it skipped and why.

**What you need to do: nothing.** No add-on is affected on a running system.

## 2026.8.28

**Security fix — the key protecting your stored service credentials is now private to Core.**
Core encrypts the credentials it holds for connected services (your GSM connection, software
updates, machine-data providers). The key used for that encryption could previously be worked out
by other PaddiSense add-ons running on the same box. It is now held privately by Core and shared
with nothing.

**What you need to do: nothing.** Existing credentials are moved across automatically the first time
Core starts, and your connections keep working. Nothing about how you sign in or use the system
changes.

## 2026.8.27

**The built-in emergency "owner" account now gets a random password instead of a standard one.**
Every new box used to create this backup account with the same well-known password until you changed
your database credential. It now gets a unique, randomly generated password on each box.

**What you need to do:** nothing on an existing box — your accounts are untouched. On a *new* box,
the emergency account's password is printed once in the Core add-on log at first start. If you ever
need it, that is where it lives. Your normal administrator account is unaffected and remains the way
you sign in.

## 2026.8.26

**Turning off a user account now signs them out straight away.** Previously, deactivating someone —
or lowering their access level — updated their account but left them signed in on any device they
were already using, for up to 12 hours. They are now signed out immediately, and a reduced access
level takes effect at once. Turning an account back on, or just editing someone's display name,
does not sign anyone out.

## 2026.8.25

**Clearer support diagnostics — no change to your box.** When PaddiSense support asks this box to
rotate a security credential it isn't able to change, the box now reports back that it declined and
why, instead of staying silent. Nothing about how your box runs is affected.

## 2026.8.24

**Signing in now uses your Home Assistant username.** If someone was added to your farm and then
could not sign in to the Core console, this is why: the console account was named after the person's
*display* name — "Jae Moore-Lambert" — while they were typing the username they actually log in to
Home Assistant with, "jaeml". The login page just said *"Invalid username or password"*, which
sounds like a password problem and isn't.

From this version your console username **is** your Home Assistant username. Existing accounts are
renamed automatically when the add-on starts, so anyone already affected can simply sign in with the
name they already know. Nobody's password changes.

**Capital letters no longer matter.** If an account was created as "Jae", typing "jae" used to be
refused. Either now works.

You do not need to do anything. If you had someone locked out, ask them to try their Home Assistant
username after this update.

## 2026.8.22

**A revoked Core licence now shows on your licence page.** If your Core licence was withdrawn, the
page kept saying *"Licensed"* — the box knew, but never told you. It does now, with the date.

Nothing about how your box runs has changed: this is a display fix. Your add-ons keep working
exactly as before, and a licence change can never lock you out of your own farm.

## 2026.8.21

**Internal improvements — no user-visible changes.** Corrected a fault in the previous update's
internal permission-sync code and cleared three code-quality issues flagged by our release checks.

## 2026.8.20

**Internal improvements — no user-visible changes.** Hardened how this add-on proves its
identity to the others on your box: permission updates are now sent with a cryptographic
token rather than being trusted because of where they came from on the internal network.

## 2026.8.19

**Internal improvements — no user-visible changes.** Your box reported a security-scan result that
was written when the software was built rather than by an actual scan, so it always read "0 issues"
whether or not anything had been checked. It no longer reports a figure it cannot stand behind — an
unscanned box now shows as unscanned rather than as clean.

## 2026.8.18

**Internal improvements — no user-visible changes.** Removed start-up code-quality checks that could
report "passed" when they had in fact found problems. These checks belong in our build system, which
already runs them properly before your update is published.

## 2026.8.17

**Internal improvements — no user-visible changes.** A rotation request this box cannot perform is
now refused cleanly and recorded, instead of being silently accepted and ignored.

## 2026.8.16

- **A revoked licence now says so.** The licence card shows **"Licence Revoked"** with the date and
  what it means: your system keeps working, but boundary sync and updates stop until you enter a new
  code. Previously a revoked add-on still read "Licensed" and there was no way to learn it from your
  own box.

## 2026.8.15

**Internal improvements — no user-visible changes.**

## 2026.8.14

- **Security update.** Refreshed the cryptography library behind licence verification (three
  published vulnerabilities) and locked every dependency to a verified checksum at build time.

## 2026.8.13

- **Fixed: connecting to Grower Services said it worked when it hadn't.** The connection was saved on
  the wrong add-on, so boundary and knowledge-base sync silently went nowhere while the screen
  reported success. Core now passes the enrolment to the add-on that actually syncs, and only reports
  success if that add-on accepts it.

## 2026.8.12

- **Connection-code errors now tell you which code you pasted.** There are two kinds of `GSM:` code
  and they look identical; the old message named the field that was missing, which read as
  "malformed code" and sent you hunting a fault that wasn't there.

## 2026.8.11

- **The revoke-lockout fix now protects boxes that were already licensed.** The previous release
  shipped the fix but only applied it to boxes licensed after upgrading — every box already in the
  field would still have been locked out by the first revoke.

## 2026.8.10

- **⭐ An unlicensed box is no longer a locked box.** A licence problem — a revoke, an expiry, or
  simply a database hiccup — used to deny every page and every API on the add-on. **A commercial
  decision could stop a farm's irrigation and its worker-safety monitoring.** The licence screen now
  appears only on a box that has never been set up, which is the one case where it is genuinely
  first-run onboarding.

## 2026.8.9

**Internal improvements — no user-visible changes.**

## 2026.8.8

- **Fixed: four buttons did nothing.** Disconnect Core, Disconnect GSM, and Backup Now (on both
  desktop and mobile) were rejected by the system's own security check. Found when an accidental
  revoke meant a licence had to be replaced and the recovery button was dead exactly when it was
  needed.

## 2026.8.7

- **Fixed: the "remove licence" button on your own box works again.** Removing a licence from the
  console is something you do at your own machine; it was being refused as though it were a remote
  instruction from head office.

## 2026.8.6

**Security — internal.** Grower boxes now trust only the production licence-signing key.

## 2026.8.5

- **🔴 Fixed a fault that could stop the whole box starting.** A superuser password rotation wrote a
  startup command into the database add-on that runs before the database itself, so the container
  shut down on every boot — taking TimescaleDB and seven add-ons with it. It took this development
  box down on 3 August. The faulty step is removed. **If your box has ever run a superuser rotation,
  ask for its database `init_commands` to be checked.**

## 2026.8.4

- **Fixed: a failed-login warning appeared in the logs on every restart** on a healthy box, which
  reads like a break-in attempt and isn't one.

## 2026.8.3

- **Fixed: "permission denied" errors on a working system.** After a database ownership change, some
  add-ons lost the permissions they needed and every request failed — including a licence activation,
  which then reported itself as a signature problem rather than the database fault it was. Core now
  checks and repairs those permissions at startup.

## 2026.8.2

**Internal improvements — no user-visible changes.**

## 2026.8.1

- **Fixed: encrypted settings could not be read after a factory-style reset**, which stopped licence
  enrolment from completing.

## 2026.7.59

**Internal improvements — no user-visible changes.**

## 2026.7.58

**Internal improvements — no user-visible changes.**

## 2026.7.57

**Internal improvements — no user-visible changes.**

## 2026.7.56

- **Signing in from the Home Assistant sidebar now reflects your real role** on a box that has not
  been locked.

## 2026.7.55

- **You choose when to lock the box.** It never locks itself. A Farm Owner or PaddiSense
  Administrator clicks "Lock this box" when ready, and the system refuses if locking would leave
  nobody with access.

## 2026.7.54

- **Fixed: the Admin card and the User Access and Database tiles had disappeared** after the role
  rename.

## 2026.7.53

- **Fixed: the System menu (User Access, Database, Metrics) had disappeared** from the desktop
  sidebar after the role rename.

## 2026.7.52

- **⭐ Three plain-language roles: Operator, Farm Owner, and PaddiSense Administrator.** Access is
  granted per module, so you give someone exactly the parts of the system they need. Farm Owner is a
  proper role that can lock the box, and more than one person can hold it. Existing accounts carry
  over.

## 2026.7.51

**Internal improvements — no user-visible changes.**

## 2026.7.50

**Internal improvements — no user-visible changes.**

## 2026.7.49

**Internal improvements — no user-visible changes.**

## 2026.7.48

**Reliability update — no action needed on your part.** Behind-the-scenes improvements to how system updates are applied and confirmed.

## 2026.7.44

**Reliability & security update — no action needed on your part.**

- **More robust internal database security.** Improved how the box manages the internal
  credentials its apps use to talk to their database, so a software update or a restart
  can't leave an app unable to start. If the box's internal security keys ever get out of
  step, it now recovers on its own instead of needing attention.
- **Safer software updates.** Every piece of third-party software the box installs is now
  verified against a locked, tamper-checked list — a stronger guarantee that what's
  installed is exactly what we shipped.
- **Ongoing security hardening.** A batch of behind-the-scenes improvements from our latest
  independent security review.

Your farm keeps running normally throughout — this update does not change how you use the
system, and irrigation is never interrupted by a Core update.
