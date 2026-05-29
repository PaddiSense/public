# PaddiSense — New Grower Onboarding

This guide covers setting up a new PaddiSense server (grower hub) from scratch, including optional PWM relay board provisioning.

---

## Part 1 — Hub Setup

### 1. Provision the hardware

Use either:
- A new **HA Green** (recommended) — see [Appendix C](#appendix-c--new-ha-server-first-time-setup) for first-time setup steps, or
- An old PC reformatted to run **Home Assistant OS** — see [Appendix B](#appendix-b--installing-ha-on-an-old-pc) for full procedure

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
> For Owner site devices, use `RRAPL_IOT` — see [Appendix A](#appendix-a--owner-site-network-rrapl) for network details.

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

---

---

## Appendix A — Owner Site Network (RRAPL)

Reference for anyone deploying hardware or troubleshooting connectivity at the Owner (RRAPL) site. IoT devices and PaddiSense relay boards connect to **RRAPL_IOT**.

### VLANs

| Network | SSID / Name | Gateway | DHCP Range | Usable IPs | VLAN | Type | Lease |
|---------|------------|---------|-----------|-----------|------|------|-------|
| Management | RRAPL_Management | 10.75.10.1 | 10.75.10.50 – 10.75.10.254 | 204 | 10 | Standard | 86400 s |
| Resident | RRAPL_Resident | 10.75.20.1 | 10.75.20.10 – 10.75.20.254 | 244 | 20 | Standard | 86400 s |
| Guest | RRAPL_Guest | 10.75.30.1 | 10.75.30.6 – 10.75.30.254 | 249 | 30 | Guest | 3660 s |
| SunRice | RRAPL_SunRice | 10.75.40.1 | 10.75.40.10 – 10.75.40.254 | 245 | 40 | Standard | 86400 s |
| IoT | RRAPL_IOT | 10.75.99.1 | 10.75.99.10 – 10.75.99.254 | 245 | 99 | Standard | 86400 s |

### Wi-Fi Networks

| Setting | RRAPL_Resident | RRAPL_SunRice | RRAPL_Guest | RRAPL_IOT |
|---------|---------------|--------------|------------|----------|
| AP Access | ALL | Server Room, Meeting Room, Lounge, Workshop | ALL | ALL |
| Client Isolation | Off | Off | Yes | Yes |
| BSS Transition | On | On | On | Off |
| Fast Roaming | On | On | On | Off |
| Security | WPA2 | WPA2 | Open | — |
| PMF | Required | Required | Disabled | Disabled |
| Band Steering | Off | Off | Off | Yes |

### Firewall Profile Groups

**RFC1918 Group** (all internal IP space):
- `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`

**Trusted VLANs:**
- Management `10.75.10.0`, Resident `10.75.20.0`, SunRice `10.75.40.0`

**Trusted VLAN Gateways:**
- Management `10.75.10.1`, Resident `10.75.20.1`, SunRice `10.75.40.1`

**Untrusted VLANs:**
- Guest `10.75.30.0`, IoT `10.75.99.0`

**Untrusted VLAN Gateways:**
- Guest `10.75.30.1`, IoT `10.75.99.1`

**Home Assistant Server:**
- IP `192.168.0.167`, Port 80

### Firewall Rules

> Rules are evaluated top-to-bottom. **Allow rules must be above Block rules.**

| # | Type | Description | Action | Source | Destination |
|---|------|-------------|--------|--------|-------------|
| 1 | LAN IN | Drop All Inter-VLAN Routing | **Drop** | RFC1918 Group | RFC1918 Group |
| 2 | LAN IN | Allow Trusted VLAN Routing | **Accept** | Trusted VLANs | Trusted VLANs |
| 3 | LAN IN | Block Trusted to Untrusted | **Drop** | Trusted VLANs | Untrusted VLANs |
| 4 | LAN IN | Allow IoT to Home Assistant | **Allow** | RRAPL_IOT (any port) | HA IP 192.168.0.167 : 80 |
| 5 | LAN IN | Allow Home Assistant to IoT | **Allow** | HA IP 192.168.0.167 : 80 | RRAPL_IOT (any port) |

### Security Features

**Country Restrictions** — Block both directions:
- North Korea, Russia, China, Iraq, Iran

**Threat Management:** Medium — Detect & Block  
Enable under DNS & User Agents:
- Dark Web Blocker: **On**
- Malicious Website: **On**

---

## Appendix B — Installing HA on an Old PC

These steps are for a **Hewlett-Packard EliteDesk**. Other systems are similar — search the web for model-specific BIOS instructions if required.

### 1. BIOS setup

1. Power on the PC
2. Press **ESC** during startup to enter the boot menu
3. Navigate to the **Security** tab → set **Secure Boot** to **Disabled** → **F10** to accept
4. Navigate to the **Advanced** tab → **Power On Options** → set **After Power Loss** to **ON**
5. Navigate to the **Storage** tab → confirm **Legacy Boot** is **Disabled** and **UEFI Boot** is **Enabled**
6. **F10** → Save and Exit

### 2. Prepare the install USB (on your working PC)

Download the following to your personal (working) PC:

- **Balena Etcher** (Windows x86/x64 installer): [balena.io/etcher](https://www.balena.io/etcher)
- **Ubuntu Desktop ISO**: [ubuntu.com/download/desktop](https://ubuntu.com/download/desktop)

Flash the USB drive (must be > 12 GB):

1. Insert a blank USB drive into your working PC
2. Open Balena Etcher
3. **Flash from file** → select the Ubuntu ISO
4. **Select target** → choose the USB drive
5. **Flash** and wait for completion

### 3. Install Home Assistant

1. Connect an ethernet cable to the old PC (or have the Wi-Fi password ready)
2. Insert the flashed USB drive into the old PC and restart
3. Press **F9** (or **ESC**) to open the boot menu → select the USB drive
4. At the Ubuntu menu, select **Try / Install**
5. When Ubuntu desktop loads, select **Try** (not Install)
6. Open the **Disks** app and format the drive — ensure there is only one partition
7. Open Firefox → search **"install home assistant x86-64 generic"**
8. Follow the official HA instructions to write the HA image to the internal drive
9. Shut down the PC, remove the USB, and reboot
10. HA will begin booting — the first boot takes several minutes

---

## Appendix C — New HA Server First-Time Setup

Applies to both HA Green and old PC installs once HA OS is running.

### 1. Connect and find the IP address

- Connect the server to the network via ethernet
- Connect a monitor to the HDMI port and power on — the IP address assigned by DHCP will appear on screen
- For Owner site servers: add this IP to the **HA-Servers** profile group in the firewall before continuing

### 2. Run the HA onboarding wizard

From a computer on the same network, open:

```
http://<HA-IP-address>:8123/onboarding.html
```

- Create the **owner** account with a strong, saved password
- Follow the wizard — do **not** add new devices at this stage
- Run all available Core updates before proceeding

### 3. Create a dedicated email account

A dedicated email is required for Nabu Casa and cloud backups.

- Create a new Outlook account: [outlook.live.com](https://outlook.live.com)
- If the grower is paying the Nabu Casa subscription, use their own email address instead
- Naming convention for Owner-managed servers:
  - Email: `haserver_XX@outlook.com` (increment XX for each new server)
  - Password format: `HAXX@<site>CY<YY>HAXX` (update XX to match server number, YY to current year)
- This account is used for Nabu Casa and OneDrive backup

### 4. Set up Nabu Casa

1. Create a new Nabu Casa account at [account.nabucasa.com](https://account.nabucasa.com) using the email above
2. On the HA server, go to **Settings → Home Assistant Cloud**
3. Log in with the new Nabu Casa credentials
4. Confirm the cloud connection is active and **Remote Access** is enabled

> Once remote access is confirmed active, the server is ready for PaddiSense installation — return to [Part 2](#part-2--paddisense-installation).
