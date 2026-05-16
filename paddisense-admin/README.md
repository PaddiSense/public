# PaddiSense Admin (public manifest)

Public HA addon manifest pointing at the GHCR-built image.
Source code lives in the private [`PaddiSense/Admin`](https://github.com/PaddiSense/Admin) repo.
Build pipeline: `.github/workflows/build-admin.yml` (in this repo) builds the multi-arch image and pushes to `ghcr.io/paddisense/{amd64,aarch64}-paddisense-admin`.

## Install on a production HA box

1. Settings → Add-ons → Add-on Store → ⋮ → Repositories
2. Add this URL: `https://github.com/PaddiSense/public`
3. Find **PaddiSense Admin** in the list, click Install
4. Configure DB connection in the addon's Configuration tab
5. Start. Panel appears in HA sidebar as **Admin**.

No source code is downloaded; the addon pulls the pre-built image from GHCR.
