"""PaddiSense Installer — single-page addon that validates a licence connection
code, then installs paddisense-server from the same public repo and auto-enrols
with GSM."""

import asyncio
import json
import base64
import logging
import os
from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

log = logging.getLogger("installer")

app = FastAPI(title="PaddiSense Installer")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

SUPERVISOR = "http://supervisor"
SUPERVISOR_TOKEN = os.environ.get("SUPERVISOR_TOKEN", "")


def _supervisor_headers() -> dict:
    return {"Authorization": f"Bearer {SUPERVISOR_TOKEN}"}


def _resolve_paddisense_slug() -> str | None:
    """Find the paddisense-server addon slug in the store.

    The slug is a hash of the repo URL + addon name. Rather than hardcode it,
    we search the store by addon name.
    """
    try:
        import requests
        resp = requests.get(
            f"{SUPERVISOR}/store/addons",
            headers=_supervisor_headers(),
            timeout=10,
        )
        if resp.status_code == 200:
            for addon in resp.json().get("data", {}).get("addons", []):
                if addon.get("name") == "PaddiSense Server":
                    return addon["slug"]
    except Exception as e:
        log.warning("Could not resolve PaddiSense slug: %s", e)
    return None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    ingress_path = request.headers.get("X-Ingress-Path", "")
    return templates.TemplateResponse(
        "install.html",
        {"request": request, "base_path": ingress_path},
    )


@app.post("/install")
async def install(request: Request):
    """Accept licence code, validate format, install addon, auto-enrol."""
    ingress_path = request.headers.get("X-Ingress-Path", "")
    body = await request.json()
    licence_code = (body.get("licence_code") or "").strip()

    if not licence_code:
        return JSONResponse({"ok": False, "error": "No licence code provided."}, 400)

    if not licence_code.startswith("GSM:"):
        return JSONResponse(
            {"ok": False, "error": "Invalid licence code format. Must start with GSM:"},
            400,
        )

    # --- Step 1: Validate connection code format ---
    try:
        b64 = licence_code[4:]
        # Handle URL-safe base64
        b64_standard = b64.replace("-", "+").replace("_", "/")
        decoded = json.loads(base64.b64decode(b64_standard))
    except Exception as e:
        log.error("Failed to decode licence code: %s", e)
        return JSONResponse(
            {"ok": False, "error": "Invalid licence code — could not decode."},
            400,
        )

    if not decoded.get("licence") or not decoded.get("secret"):
        return JSONResponse(
            {"ok": False, "error": "Licence code is missing required fields."},
            400,
        )

    if not decoded.get("webhook_url") and not decoded.get("url"):
        return JSONResponse(
            {"ok": False, "error": "Licence code has no GSM endpoint."},
            400,
        )

    log.info("Valid licence code: %s", decoded.get("licence", "")[:20])

    # --- Step 2: Reload store and find paddisense-server ---
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            # Reload to pick up latest
            reload_resp = await client.post(
                f"{SUPERVISOR}/store/reload",
                headers=_supervisor_headers(),
            )
            reload_resp.raise_for_status()
            log.info("Store reloaded")

    except httpx.RequestError as exc:
        log.error("Store reload failed: %s", exc)
        return JSONResponse(
            {"ok": False, "error": "Could not communicate with Supervisor."},
            500,
        )

    # Resolve the addon slug dynamically
    ps_slug = _resolve_paddisense_slug()
    if not ps_slug:
        return JSONResponse(
            {"ok": False, "error": "PaddiSense Server addon not found in store. Ensure the PaddiSense/public repository is added."},
            404,
        )
    log.info("Resolved PaddiSense slug: %s", ps_slug)

    # --- Step 3: Install paddisense-server ---
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            install_resp = await client.post(
                f"{SUPERVISOR}/addons/{ps_slug}/install",
                headers=_supervisor_headers(),
            )
            if install_resp.status_code not in (200, 201):
                log.error("Install failed: %s %s", install_resp.status_code, install_resp.text)
                return JSONResponse(
                    {"ok": False, "error": "Addon install failed. Try installing manually from the Add-on Store."},
                    500,
                )
            log.info("PaddiSense addon installed")

    except httpx.RequestError as exc:
        log.error("Install request failed: %s", exc)
        return JSONResponse(
            {"ok": False, "error": "Addon install timed out. Check the Add-on Store."},
            500,
        )

    # --- Step 4: Start addon, wait for healthy, auto-enroll ---
    ps_internal = f"http://{ps_slug.replace('_', '-')}:8100"

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            start_resp = await client.post(
                f"{SUPERVISOR}/addons/{ps_slug}/start",
                headers=_supervisor_headers(),
            )
            if start_resp.status_code not in (200, 201):
                log.warning("Start failed: %s", start_resp.text[:100])
    except httpx.RequestError as exc:
        log.warning("Could not start addon: %s", exc)

    # Wait for PaddiSense to become healthy (up to 90s)
    enrolled = False
    async with httpx.AsyncClient(timeout=10) as client:
        for attempt in range(18):
            await asyncio.sleep(5)
            try:
                health = await client.get(f"{ps_internal}/health")
                if health.status_code == 200:
                    log.info("PaddiSense healthy after %ds", (attempt + 1) * 5)
                    # Auto-enroll with the connection code
                    try:
                        enroll_resp = await client.post(
                            f"{ps_internal}/gsm/api/enroll",
                            json={"code": licence_code},
                            timeout=30,
                        )
                        if enroll_resp.status_code == 200:
                            log.info("Auto-enrollment successful")
                            enrolled = True
                        else:
                            log.warning("Auto-enroll returned %s: %s",
                                        enroll_resp.status_code, enroll_resp.text[:100])
                    except httpx.RequestError as exc:
                        log.warning("Auto-enroll request failed: %s", exc)
                    break
            except httpx.RequestError:
                log.debug("PaddiSense not ready yet (attempt %d/18)", attempt + 1)

    msg = "PaddiSense installed and enrolled!" if enrolled else \
          "PaddiSense installed! Open it from the sidebar to complete setup."

    return JSONResponse({
        "ok": True,
        "message": msg,
        "enrolled": enrolled,
    })
