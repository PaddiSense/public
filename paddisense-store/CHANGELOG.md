# PaddiSense Store — Changelog

All notable changes to PaddiSense Store.

## 2026.6.51
- Fix: new products now appear on the Store page right away (previously only visible once stock was received).

## 2026.6.50
- Fix: the new-product form now has its Cropping/Livestock sectors on a fresh install, so new products save and display correctly.

## 2026.6.49
- Tidied the Settings screen — removed a developer-only "Base" option that isn't relevant on your add-on.

## 2026.6.48
- Fix — on the Use page (phone), the **+** buttons were subtracting stock like the **−** buttons; **+** now correctly raises the projected stock.
- Internal security hardening — no user-visible change.

## 2026.6.46
- New look — now matches the rest of your PaddiSense add-ons.
- Settings rebuilt — manage your categories, units, chemical groups and active ingredients in a cleaner list (enable/disable, reorder, rename inline).
- Starter data — common chemical groups and active ingredients are pre-loaded on a new install.
- "Empty container" — on the Use page, write off the last bit of a finished drum in one tap.
- Products — choose a sector (Cropping/Livestock) and the category list narrows to match.
- Fix — inventory value now displays correctly.

## 2026.6.1
- Initial release — extracted from PaddiSense Core chemical store
- Product registry with 13 categories (crop + livestock sectors)
- Storage locations, stock levels via materialized cache
- Separate Receive (stock in) and Use (stock out) pages
- Movement audit trail with void mechanism
- Desktop dashboard with tile launcher
- Two-tier filter: Sector (Cropping/Livestock) then Category
- Application logging fix for visible addon diagnostics

