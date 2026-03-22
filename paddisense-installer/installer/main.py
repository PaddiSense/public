"""PaddiSense Installer — single-page addon that validates a licence connection
code via a Cloudflare Worker, then adds the private PaddiSense repo and
installs paddisense-server through the HA Supervisor API."""

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
WORKER_URL = "https://paddisense-api.paddisense.workers.dev/validate"

# The slug the private repo will register the addon under
PADDISENSE_SLUG = "d425496f_paddisense-server"


def _supervisor_headers() -> dict:
    return {"Authorization": f"Bearer {SUPERVISOR_TOKEN}"}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    ingress_path = request.headers.get("X-Ingress-Path", "")
    return templates.TemplateResponse(
        "install.html",
        {"request": request, "base_path": ingress_path},
    )


@app.post("/install")
async def install(request: Request):
    """Accept licence code, validate via Cloudflare Worker, add repo, install addon."""
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

    # --- Step 1: Validate with Cloudflare Worker ---
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(WORKER_URL, json={"licence_code": licence_code})
    except httpx.RequestError as exc:
        log.error("Worker request failed: %s", exc)
        return JSONResponse(
            {"ok": False, "error": "Could not reach validation service. Try again later."},
            502,
        )

    if resp.status_code != 200:
        log.warning("Worker returned %s: %s", resp.status_code, resp.text)
        return JSONResponse(
            {"ok": False, "error": "Validation service error. Check your licence code."},
            502,
        )

    worker_data = resp.json()
    if not worker_data.get("valid"):
        return JSONResponse(
            {"ok": False, "error": worker_data.get("reason", "Invalid licence code.")},
            403,
        )

    repo_url = worker_data.get("repo_url")
    if not repo_url:
        return JSONResponse(
            {"ok": False, "error": "Validation succeeded but no repo URL returned."},
            502,
        )

    # --- Step 2: Add private repo to Supervisor ---
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Get current repos
            store_resp = await client.get(
                f"{SUPERVISOR}/store",
                headers=_supervisor_headers(),
            )
            store_resp.raise_for_status()
            current_repos = store_resp.json().get("data", {}).get("repositories", [])

            # Check if already added (compare by base URL, ignoring auth tokens)
            repo_base = "github.com/PaddiSense/PaddiSense"
            already_added = any(repo_base in r for r in current_repos)

            if not already_added:
                add_resp = await client.post(
                    f"{SUPERVISOR}/store/repositories",
                    headers=_supervisor_headers(),
                    json={"repository": repo_url},
                )
                if add_resp.status_code not in (200, 201):
                    resp_text = add_resp.text
                    if add_resp.status_code == 400 and "already in the store" in resp_text:
                        log.info("Private repo already in store (confirmed by Supervisor)")
                    else:
                        log.error("Failed to add repo: %s %s", add_resp.status_code, resp_text)
                        return JSONResponse(
                            {"ok": False, "error": "Failed to add addon repository."},
                            500,
                        )
                else:
                    log.info("Added private repo to store")
            else:
                log.info("Private repo already in store (matched by URL)")

    except httpx.RequestError as exc:
        log.error("Supervisor store request failed: %s", exc)
        return JSONResponse(
            {"ok": False, "error": "Could not communicate with Supervisor."},
            500,
        )

    # --- Step 3: Reload store and install paddisense-server ---
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            # Reload addon store
            reload_resp = await client.post(
                f"{SUPERVISOR}/store/reload",
                headers=_supervisor_headers(),
            )
            reload_resp.raise_for_status()
            log.info("Store reloaded")

            # Install the addon
            install_resp = await client.post(
                f"{SUPERVISOR}/addons/{PADDISENSE_SLUG}/install",
                headers=_supervisor_headers(),
            )
            if install_resp.status_code not in (200, 201):
                log.error("Install failed: %s %s", install_resp.status_code, install_resp.text)
                return JSONResponse(
                    {"ok": False, "error": "Repository added but addon install failed. Try installing manually from the Add-on Store."},
                    500,
                )
            log.info("PaddiSense addon installed")

    except httpx.RequestError as exc:
        log.error("Supervisor install request failed: %s", exc)
        return JSONResponse(
            {"ok": False, "error": "Repository added but addon install timed out. Check the Add-on Store."},
            500,
        )

    return JSONResponse({
        "ok": True,
        "message": "PaddiSense installed successfully!",
        "addon_path": f"{ingress_path}/../{PADDISENSE_SLUG}",
    })
