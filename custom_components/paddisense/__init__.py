"""PaddiSense — bootstrap and auto-recovery stub.

This file is managed by HACS (PaddiSense/public). The full integration is
installed from the private repo via the config flow or auto-recovery.

If HACS updates this integration, this stub auto-detects that const.py is
missing (wiped by HACS) and re-syncs from the private repo without user
intervention.
"""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
import tempfile

_LOGGER = logging.getLogger(__name__)

DOMAIN = "paddisense"
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_URL = "https://github.com/PaddiSense/PaddiSense.git"


async def async_setup(hass, config):
    return True


async def async_setup_entry(hass, entry):
    """Bootstrap entry setup — auto-recovers full integration if HACS wiped files."""
    const_py = os.path.join(_HERE, "const.py")

    if os.path.exists(const_py):
        # Full integration files are present but we loaded as stub — return True.
        # HA will use the real __init__.py on next restart (after auto-recovery).
        return True

    # const.py missing — HACS update wiped the real files. Auto-recover.
    _LOGGER.warning(
        "PaddiSense: integration files missing (HACS update detected), "
        "attempting auto-recovery from private repository"
    )

    token = _get_hacs_token(hass)
    if token:
        hass.async_create_task(_auto_recover(hass, token))
        from homeassistant.exceptions import ConfigEntryNotReady
        raise ConfigEntryNotReady(
            "PaddiSense is recovering from HACS update — will restart when ready"
        )

    _LOGGER.error(
        "PaddiSense: no GitHub token found for auto-recovery. "
        "Delete the integration in HA Settings and reinstall via HACS."
    )
    from homeassistant.exceptions import ConfigEntryNotReady
    raise ConfigEntryNotReady(
        "PaddiSense needs reinstall — delete integration and re-add via HACS"
    )


async def async_unload_entry(hass, entry):
    return True


def _get_hacs_token(hass) -> str | None:
    """Read GitHub token from HACS .storage file, or git-credentials fallback."""
    try:
        import json
        hacs_file = os.path.join(hass.config.config_dir, ".storage", "hacs")
        if os.path.exists(hacs_file):
            data = json.loads(open(hacs_file, encoding="utf-8").read())
            token = data.get("data", {}).get("token") or None
            if token:
                return token
    except Exception:
        pass
    return _get_git_credentials_token(hass.config.config_dir)


def _get_git_credentials_token(config_dir: str) -> str | None:
    """Read GitHub PAT from git-credentials file as last-resort fallback."""
    import re
    from pathlib import Path
    for cred_path in (Path.home() / ".git-credentials", Path(config_dir) / ".git-credentials"):
        try:
            if cred_path.exists():
                text = cred_path.read_text(encoding="utf-8")
                m = re.search(r"https://x-access-token:([^@\s]+)@github\.com", text)
                if m:
                    return m.group(1)
        except Exception:
            pass
    return None


async def _auto_recover(hass, token: str) -> None:
    """Clone private repo and restore full integration files, then restart HA."""
    config_path = hass.config.config_dir
    ok = await hass.async_add_executor_job(_run_recovery, config_path, token)
    if ok:
        _LOGGER.info("PaddiSense: auto-recovery complete — restarting Home Assistant")
        await hass.services.async_call("homeassistant", "restart")
    else:
        _LOGGER.error(
            "PaddiSense: auto-recovery failed — delete integration and reinstall via HACS"
        )


def _run_recovery(config_path: str, token: str) -> bool:
    """Clone PaddiSense private repo and sync all integration + module files."""
    auth_url = _REPO_URL.replace("https://", f"https://x-access-token:{token}@")
    integration_dst = os.path.join(config_path, "custom_components", "paddisense")
    modules_dst = os.path.join(config_path, "PaddiSense")

    tmp_dir = tempfile.mkdtemp()
    try:
        tmp_repo = os.path.join(tmp_dir, "repo")
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"
        env["GIT_ASKPASS"] = "echo"

        result = subprocess.run(
            [
                "git", "clone", "--branch", "main", "--single-branch",
                "--depth", "1", "--quiet", auth_url, tmp_repo,
            ],
            capture_output=True, text=True, timeout=180, env=env,
        )
        if result.returncode != 0:
            _LOGGER.error("PaddiSense recovery: clone failed: %s", result.stderr[:300])
            return False

        # 1. Sync integration files (all types)
        integration_src = os.path.join(tmp_repo, "custom_components", "paddisense")
        if os.path.isdir(integration_src):
            _LOGGER.info("PaddiSense recovery: syncing integration files")
            for root, dirs, files in os.walk(integration_src):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                rel = os.path.relpath(root, integration_src)
                for fname in files:
                    if fname.endswith((".py", ".json", ".pem", ".yaml", ".js", ".png")):
                        src = os.path.join(root, fname)
                        dst = os.path.join(integration_dst, rel, fname)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copy2(src, dst)

        # 2. Sync PaddiSense modules (preserve packages/)
        modules_src = os.path.join(tmp_repo, "PaddiSense")
        if os.path.isdir(modules_src) and os.path.isdir(modules_dst):
            packages_dir = os.path.join(modules_dst, "packages")
            packages_bak = None
            if os.path.isdir(packages_dir):
                packages_bak = os.path.join(tmp_dir, "packages_bak")
                shutil.copytree(packages_dir, packages_bak)

            for item in os.listdir(modules_src):
                if item == "packages":
                    continue
                src_item = os.path.join(modules_src, item)
                dst_item = os.path.join(modules_dst, item)
                if os.path.isdir(src_item):
                    if os.path.exists(dst_item):
                        shutil.rmtree(dst_item)
                    shutil.copytree(src_item, dst_item)
                else:
                    shutil.copy2(src_item, dst_item)

            if packages_bak:
                if os.path.exists(packages_dir):
                    shutil.rmtree(packages_dir)
                shutil.copytree(packages_bak, packages_dir)
                _cleanup_packages(packages_dir)
            elif not os.path.exists(packages_dir):
                os.makedirs(packages_dir)

        return True

    except subprocess.TimeoutExpired:
        _LOGGER.error("PaddiSense recovery: clone timed out")
        return False
    except Exception as exc:
        _LOGGER.error("PaddiSense recovery: unexpected error: %s", exc)
        return False
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
                    _LOGGER.warning(
                        "Removed admin-only file from packages: %s", entry.name
                    )
            except OSError:
                pass
