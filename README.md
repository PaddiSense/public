# PaddiSense

Precision agriculture management for Home Assistant — paddock records, irrigation, spray programs, and more.

## Installation via HACS

> **Requires a PaddiSense license key.** Contact [PaddiSense](https://auth.paddisense.com) to get one.

### Step 1 — Add this repository to HACS

1. Open HACS in your Home Assistant sidebar
2. Go to **Integrations**
3. Click the three-dot menu (⋮) → **Custom repositories**
4. Add `https://github.com/PaddiSense/public` with category **Integration**
5. Close the dialog

### Step 2 — Install PaddiSense

1. Search for **PaddiSense** in HACS Integrations
2. Click **Download**
3. Restart Home Assistant when prompted

### Step 3 — Enter your license key

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **PaddiSense**
3. Enter your license key — this will download and install the full software
4. Restart Home Assistant again when prompted

### Step 4 — Done

PaddiSense is now installed. Future updates are managed in-app via **PSM Settings → Update**.

---

> Once installed, you can remove PaddiSense from HACS — it won't affect the running installation and in-app updates will handle future versions.
