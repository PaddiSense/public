# PaddiSense — New Grower Onboarding

This guide covers setting up a new PaddiSense server (grower hub) from scratch, including optional PWM relay board provisioning.

---

## Part 1 — Hub Setup

### 1. Provision the hardware

Use either:
- A new **HA Green** (recommended), or
- An old PC reformatted to run **Home Assistant OS**

Install Home Assistant OS using the [official installation guide](https://www.home-assistant.io/installation/).

### 2. Update to the latest environment

Once HA is running, update all components before installing PaddiSense:

- **Settings → System → Updates** — apply all pending HA OS, Core, and Supervisor updates
- Reboot if prompted

### 3. Create a Nabu Casa account

A Nabu Casa account is required for remote access and for PaddiSense to communicate with the management server.

1. Go to **Settings → Home Assistant Cloud**
2. Sign up for a Nabu Casa account (or log in if the grower already has one)
3. Subscribe to Home Assistant Cloud

### 4. Enable remote connection

In **Settings → Home Assistant Cloud → Remote Access**, enable the remote UI. Confirm the remote URL is active before proceeding — PaddiSense uses this relay to send heartbeats and field data.

---

## Part 2 — PaddiSense Installation

### 5. Create the grower in Admin

Before installing on the grower's hub, set up their record in the **PaddiSense Admin** addon:

1. Open Admin → **Growers → New Grower**
2. Enter the grower's details (name, business name, contact)
3. Under **Licences**, issue the appropriate licences for the modules required

> Admin generates the connection code — you will need this in Step 7.

### 6. Add the PaddiSense addon repository

On the grower's HA server:

1. Go to **Settings → Add-ons → Add-on Store**
2. Click the menu (⋮) → **Repositories**
3. Add: `https://github.com/PaddiSense/public`
4. The PaddiSense addon collection will appear in the store

### 7. Install PaddiSense Core

1. In the Add-on Store, find **PaddiSense Core** and install it
2. Start the addon and open the UI
3. On first launch, enter the **connection code** generated in Step 5
4. If the grower requires **GSM boundary management** (field event sync and knowledge packs), ensure the GSM licence has been issued in Admin — Core will activate this automatically from the connection code

### 8. Install additional modules

From the **App Install** section inside PaddiSense Core, install any additional modules the grower's licence covers:

| Module | Purpose |
|--------|---------|
| PWM | Precision Water Management — pumps, valves, irrigation |
| Safety | Worker Safety System (WSS) |
| Livestock | Stock and livestock tracking |
| ASM | Asset and Service Management |
| SugarSense | Sugar cane farm management variant |

---

## Part 3 — PWM Relay Board Provisioning

Complete this section if the grower's licence includes PWM and they have relay boards to configure.

### 1. Add device secrets

In the **ESPHome** addon on the grower's HA server, open `secrets.yaml` and add:

```yaml
wifi_ssid: "GrowerWiFiNetworkName"
wifi_password: "GrowerWiFiPassword"
# Add any device-specific secrets (API keys, OTA passwords) here
```

> The grower's exact WiFi SSID is required before flashing — the firmware is compiled with it embedded.

### 2. Create the device in PWM

1. Open **PaddiSense Core → PWM → Device Config**
2. Click **New Device** and fill in the device details (name, type, zone assignment)
3. Save — this generates the ESPHome YAML configuration

### 3. Flash firmware via ESPHome Connect

1. Open the **ESPHome** addon dashboard
2. Locate the newly generated device
3. Click **Install → Connect via USB** (first flash must be wired)
4. Wait for the compile and flash to complete

### 4. Update firmware via OTA

Once the device is online and connected to the grower's WiFi:

1. In ESPHome, click **Install → Wirelessly (OTA)**
2. Confirm the device responds to OTA updates before leaving site
3. Future firmware updates can be pushed remotely via OTA without physical access

---

## Checklist — Before Leaving Site

- [ ] HA updated to latest OS/Core/Supervisor
- [ ] Nabu Casa remote access active and URL confirmed
- [ ] Grower record and licences created in Admin
- [ ] PaddiSense/public repo added to HA addon store
- [ ] PaddiSense Core installed and connection code accepted
- [ ] Core heartbeat visible in Admin → Fleet (within 15 min of install)
- [ ] All required modules installed and accessible
- [ ] PWM relay boards flashed, online, and OTA-verified (if applicable)
