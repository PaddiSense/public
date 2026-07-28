# PaddiSense Core — What's New

> Plain-English release notes for growers. The full technical changelog lives in the
> source repo (`CHANGELOG.md`); this is the version that ships in the grower catalog.

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
