"""Config flow for PaddiSense bootstrap installer."""
from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import tempfile

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

DOMAIN = "paddisense"

PADDISENSE_MODULES_DIR = "PaddiSense"
INTEGRATION_DIR = "custom_components/paddisense"
REPO_URL = "https://github.com/PaddiSense/PaddiSense.git"
REPO_BRANCH = "main"
REPO_SUBFOLDER = "PaddiSense"


def _is_paddisense_installed(hass: HomeAssistant) -> bool:
    """Return True if PaddiSense is actively installed with a config entry.

    Files alone are not sufficient — if the config entry was deleted but the
    PaddiSense/ directory was left behind (e.g. HACS uninstall without deleting
    the integration from Settings), we should allow re-bootstrap.
    """
    version_file = hass.config.path(PADDISENSE_MODULES_DIR, "VERSION")
    if not os.path.exists(version_file):
        return False
    return bool(hass.config_entries.async_entries(DOMAIN))


def _extract_token(license_key: str) -> str | None:
    """Extract the GitHub PAT from a PaddiSense license key."""
    PREFIX = "PADDISENSE."
    if not license_key.startswith(PREFIX):
        return None
    parts = license_key[len(PREFIX):].split(".")
    if len(parts) != 2:
        return None
    try:
        payload = json.loads(base64.urlsafe_b64decode(parts[0] + "=="))
        return payload.get("github_token") or None
    except Exception:
        return None


def _get_hacs_token(config_dir: str) -> str | None:
    """Read GitHub token from HACS .storage as fallback."""
    try:
        hacs_file = os.path.join(config_dir, ".storage", "hacs")
        if os.path.exists(hacs_file):
            data = json.loads(open(hacs_file, encoding="utf-8").read())
            return data.get("data", {}).get("token") or None
    except Exception:
        pass
    return None


def _run_bootstrap(config_path: str, token: str) -> tuple[bool, str]:
    """Clone the private repo and copy files. Runs in an executor thread."""
    modules_dst = os.path.join(config_path, PADDISENSE_MODULES_DIR)
    integration_dst = os.path.join(config_path, INTEGRATION_DIR)
    auth_url = REPO_URL.replace("https://", f"https://{token}@")

    tmp_dir = tempfile.mkdtemp()
    try:
        tmp_repo = os.path.join(tmp_dir, "repo")

        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"
        env["GIT_ASKPASS"] = "echo"

        result = subprocess.run(
            [
                "git", "clone", "--branch", REPO_BRANCH, "--single-branch",
                "--depth", "1", "--quiet", auth_url, tmp_repo,
            ],
            capture_output=True, text=True, timeout=180, env=env,
        )
        if result.returncode != 0 or not os.path.isdir(tmp_repo):
            return False, "Clone failed — check your license key is valid."

        # Determine source dirs
        modules_src = os.path.join(tmp_repo, REPO_SUBFOLDER)
        if not os.path.isdir(modules_src):
            modules_src = tmp_repo

        integration_src = os.path.join(tmp_repo, INTEGRATION_DIR)

        # Copy modules (preserve packages/)
        packages_backup = None
        packages_dir = os.path.join(modules_dst, "packages")
        if os.path.isdir(packages_dir):
            packages_backup = os.path.join(tmp_dir, "packages_backup")
            shutil.copytree(packages_dir, packages_backup)

        if os.path.isdir(modules_dst):
            shutil.rmtree(modules_dst)
        shutil.copytree(modules_src, modules_dst)

        if packages_backup and os.path.isdir(packages_backup):
            packages_dst = os.path.join(modules_dst, "packages")
            if os.path.isdir(packages_dst):
                shutil.rmtree(packages_dst)
            shutil.copytree(packages_backup, packages_dst)
            _cleanup_packages(packages_dst)
        else:
            os.makedirs(os.path.join(modules_dst, "packages"), exist_ok=True)

        # Copy integration files (.py, .json, .pem, .yaml, .js, .png)
        if os.path.isdir(integration_src) and os.path.isdir(integration_dst):
            for root, dirs, files in os.walk(integration_src):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                rel_root = os.path.relpath(root, integration_src)
                for fname in files:
                    if fname.endswith((".py", ".json", ".pem", ".yaml", ".js", ".png")):
                        src_file = os.path.join(root, fname)
                        dst_file = os.path.join(integration_dst, rel_root, fname)
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                        shutil.copy2(src_file, dst_file)

        # Sync www files from registry module to integration (for frontend cards)
        registry_www = os.path.join(modules_dst, "registry", "www")
        integration_www = os.path.join(integration_dst, "www")
        if os.path.isdir(registry_www):
            os.makedirs(integration_www, exist_ok=True)
            for fname in os.listdir(registry_www):
                if fname.endswith(".js"):
                    shutil.copy2(
                        os.path.join(registry_www, fname),
                        os.path.join(integration_www, fname),
                    )

        return True, ""

    except subprocess.TimeoutExpired:
        return False, "Clone timed out. Check your internet connection and try again."
    except Exception as e:
        return False, str(e)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _cleanup_packages(packages_dir: str) -> None:
    """Remove admin-only symlinks (e.g. license_generator.yaml) from packages/."""
    for entry in os.scandir(packages_dir):
        if entry.is_symlink():
            try:
                target = os.readlink(entry.path)
                if "rrapl" in target or "/admin/" in target:
                    os.unlink(entry.path)
            except OSError:
                pass


class PaddiSenseConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """PaddiSense bootstrap installer config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if _is_paddisense_installed(self.hass):
            return self.async_abort(reason="already_installed")

        errors = {}

        if user_input is not None:
            license_key = user_input.get("license_key", "").strip()
            token = _extract_token(license_key)

            # Fallback: try HACS token if no license key or extraction fails
            if not token:
                if not license_key:
                    token = _get_hacs_token(self.hass.config.config_dir)
                if not token:
                    errors["license_key"] = "invalid_key"

            if token and not errors:
                config_path = self.hass.config.config_dir
                ok, msg = await self.hass.async_add_executor_job(
                    _run_bootstrap, config_path, token
                )
                if ok:
                    # Notify grower to restart HA
                    try:
                        from homeassistant.components.persistent_notification import (
                            async_create as _pn_create,
                        )
                        _pn_create(
                            self.hass,
                            "PaddiSense has been installed successfully.\n\n"
                            "**Please restart Home Assistant** to load the PaddiSense "
                            "modules and management dashboard.",
                            title="PaddiSense — Restart Required",
                            notification_id="paddisense_restart_required",
                        )
                    except Exception:
                        pass
                    return self.async_create_entry(title="PaddiSense", data={})
                else:
                    errors["base"] = "bootstrap_failed"
                    errors["_bootstrap_msg"] = msg

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("license_key"): str,
            }),
            errors=errors,
            description_placeholders={
                "error_detail": errors.get("_bootstrap_msg", ""),
            },
        )
