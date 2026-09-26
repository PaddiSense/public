#!/usr/bin/env python3
"""GHCR image retention for the private add-on image families (2026-09-26). Every release adds a
~35–50 MB version per arch and nothing was ever deleted, so the org hit its package storage limit.

Runs INSIDE GitHub Actions (PaddiSense/public) with the workflow's GITHUB_TOKEN (packages: write). It never
needs a credential on a box. DRY-RUN BY DEFAULT: it prints the plan; `--apply` deletes.

KEEP, per package (e.g. amd64-paddisense-safety):
  1. the version the catalog PINS (paddisense-public main, <addon>/config.yaml `version:`)
  2. the 2 versions immediately BEFORE it (rollback), and every version NEWER than it (cut but not yet
     rolled out — the Admin "Roll out to fleet" button has not been pressed)
  3. `latest`, and any tag that is not a version, `latest` or cosign (a deliberate push — never guessed at)
  4. every manifest a kept tag REFERENCES (its platform image + its attestation manifest)
  5. the cosign `sha256-<digest>.sig` / `.att` tags of every kept digest
Everything else is deleted.

Three traps, each a stored negative case in --selftest (measured on the public Core image, 2026-09-26):
  · A kept tag is an OCI INDEX whose platform image and provenance attestation are UNTAGGED versions.
    `delete-only-untagged-versions` would delete the children of every image we keep — the pinned one
    would stop pulling. (2026.9.10: index → amd64 image + attestation-manifest, both untagged.)
  · Tags sort as STRINGS wrong: '2026.9.5' > '2026.9.10'. "Newest N by name" keeps 9.3–9.5 and deletes
    what growers run. Versions compare numerically.
  · The pinned version need not be the newest (a cut awaiting roll-out is newer). "Keep newest N" can
    delete the pinned one if more than N cuts are pending.
FAIL-CLOSED: pinned tag absent from the package, a manifest that cannot be read, or a plan that would
delete a pinned/kept digest → abort, delete NOTHING, exit 2.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

VERSION = re.compile(r"^\d{4}\.\d{1,2}\.\d+$")
SIG = re.compile(r"^sha256-([0-9a-f]{64})\.(sig|att|sbom)$")
ORG = "PaddiSense"


def vkey(tag: str) -> tuple[int, ...]:
    return tuple(int(x) for x in tag.split("."))


class Abort(Exception):
    """A condition under which deleting anything is unsafe."""


def plan(versions: list[dict], pinned: str, children: dict[str, list[str]], before: int = 2) -> tuple[list[dict], list[dict]]:
    """Pure: (keep, delete). versions: [{"id", "digest", "tags": [...]}]; children: index digest -> child digests."""
    by_tag = {t: v for v in versions for t in v["tags"]}
    if pinned not in by_tag:
        raise Abort(f"pinned version {pinned} is not in the package — refusing to plan (would delete the catalog's image)")
    vtags = sorted((t for t in by_tag if VERSION.match(t)), key=vkey)
    i = vtags.index(pinned)
    keep_tags = set(vtags[max(0, i - before):]) | {"latest"}
    # any tag that is not a version, `latest` or a cosign tag is someone's deliberate push: keep it, never guess
    keep_tags |= {t for t in by_tag if not VERSION.match(t) and t != "latest" and not SIG.match(t)}
    keep_digests = {by_tag[t]["digest"] for t in keep_tags if t in by_tag}
    for d in list(keep_digests):
        keep_digests |= set(children.get(d, []))
    for v in versions:                      # cosign signatures/attestations of a kept digest
        for t in v["tags"]:
            m = SIG.match(t)
            if m and f"sha256:{m.group(1)}" in keep_digests:
                keep_digests.add(v["digest"])
    keep = [v for v in versions if v["digest"] in keep_digests or set(v["tags"]) & keep_tags]
    kept_ids = {v["id"] for v in keep}
    delete = [v for v in versions if v["id"] not in kept_ids]
    # invariant: the pinned image and everything it references survive
    must = {by_tag[pinned]["digest"], *children.get(by_tag[pinned]["digest"], [])}
    if must - {v["digest"] for v in keep}:
        raise Abort(f"plan would delete part of the pinned image {pinned}")
    return keep, delete


# ── I/O (GitHub Actions) ────────────────────────────────────────────────────────────────────────────

def _req(url: str, token: str, method: str = "GET", accept: str = "application/vnd.github+json"):
    r = urllib.request.Request(url, method=method, headers={"Authorization": f"Bearer {token}", "Accept": accept,
                                                            "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        body = resp.read()
        return json.loads(body) if body else None


def list_versions(pkg: str, token: str) -> list[dict]:
    out, page = [], 1
    while True:
        b = _req(f"https://api.github.com/orgs/{ORG}/packages/container/{pkg}/versions?per_page=100&page={page}", token)
        out += [{"id": v["id"], "digest": v["name"], "tags": v.get("metadata", {}).get("container", {}).get("tags", []),
                 "created": v.get("created_at", "")} for v in b]
        if len(b) < 100:
            return out
        page += 1


def manifest_children(pkg: str, digest: str, token: str) -> list[str]:
    reg = json.loads(urllib.request.urlopen(urllib.request.Request(
        f"https://ghcr.io/token?scope=repository:{ORG.lower()}/{pkg}:pull",
        headers={"Authorization": "Basic " + __import__("base64").b64encode(f"x:{token}".encode()).decode()}), timeout=60).read())["token"]
    m = _req(f"https://ghcr.io/v2/{ORG.lower()}/{pkg}/manifests/{digest}", reg, accept=", ".join([
        "application/vnd.oci.image.index.v1+json", "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.oci.image.manifest.v1+json", "application/vnd.docker.distribution.manifest.v2+json"]))
    return [c["digest"] for c in (m or {}).get("manifests", [])]


def pinned_version(catalog_dir: str) -> str:
    m = re.search(r'^version:\s*"?([0-9.]+)"?', Path(catalog_dir, "config.yaml").read_text(), re.M)
    if not m:
        raise Abort(f"no version: in {catalog_dir}/config.yaml")
    return m.group(1)


def run(pkg: str, catalog_dir: str, apply: bool, token: str) -> int:
    pinned = pinned_version(catalog_dir)
    versions = list_versions(pkg, token)
    tagged = [v for v in versions if any(not SIG.match(t) for t in v["tags"])]   # every kept-able tag, incl. unknown ones
    children = {v["digest"]: manifest_children(pkg, v["digest"], token) for v in tagged}
    keep, delete = plan(versions, pinned, children)
    print(f"{pkg}: pinned {pinned} · {len(versions)} versions · keep {len(keep)} · delete {len(delete)}"
          f" · kept tags {sorted({t for v in keep for t in v['tags'] if VERSION.match(t)}, key=vkey)}")
    if not apply:
        print(f"{pkg}: DRY RUN — nothing deleted (pass --apply)")
        return 0
    done = 0
    for v in delete:
        try:
            _req(f"https://api.github.com/orgs/{ORG}/packages/container/{pkg}/versions/{v['id']}", token, method="DELETE")
        except (urllib.error.URLError, OSError) as e:
            # "could not finish" must never read as "did nothing"
            print(f"{pkg}: STOPPED — deleted {done} of {len(delete)} before: {e}")
            return 3
        done += 1
    print(f"{pkg}: deleted {done} of {len(delete)}")
    return 0


# ── selftest: stored negative cases (never runtime-generated) ────────────────────────────────────────

def selftest(fixtures: Path) -> int:
    fails = 0
    for f in sorted(fixtures.glob("*.json")):
        case = json.loads(f.read_text())
        try:
            keep, delete = plan(case["versions"], case["pinned"], case.get("children", {}))
            got = {"keep": sorted(v["id"] for v in keep), "delete": sorted(v["id"] for v in delete)}
        except Abort as e:
            got = {"abort": str(e)[:40]}
        except Exception as e:  # a crash is not an abort: the guard must refuse deliberately, by name
            got = {"crash": f"{type(e).__name__}: {e}"[:60]}
        want = case["expect"]
        ok = ("abort" in want) == ("abort" in got) and all(got.get(k) == want[k] for k in ("keep", "delete") if k in want)
        fails += not ok
        print(f"  {'✓' if ok else '✗'} {f.stem}: {case['why']}" + ("" if ok else f"\n      want {want}\n      got  {got}"))
    fails += _selftest_partial_delete()
    print(f"selftest: {fails} failure(s) over {len(list(fixtures.glob('*.json')))} stored case(s) + the partial-delete report")
    return 1 if fails else 0


def _selftest_partial_delete() -> int:
    """A DELETE that fails on the 2nd of 3 must report 'deleted 1 of 3', rc 3 — never 'nothing deleted'."""
    import contextlib, io
    g = globals()
    saved = {k: g[k] for k in ("pinned_version", "list_versions", "manifest_children", "_req")}
    calls = {"n": 0}

    def fake_req(url, token, method="GET", accept=""):
        if method == "DELETE":
            calls["n"] += 1
            if calls["n"] == 2:
                raise urllib.error.HTTPError(url, 403, "Forbidden", None, None)
    vs = [{"id": i, "digest": f"sha256:{i:064x}", "tags": [f"2026.9.{i}"]} for i in range(1, 7)]
    g.update(pinned_version=lambda d: "2026.9.6", list_versions=lambda p, t: vs,
             manifest_children=lambda p, d, t: [], _req=fake_req)
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            rc = run("amd64-x", "x", True, "t")
    finally:
        g.update(saved)
    ok = rc == 3 and "deleted 1 of 3" in out.getvalue() and "nothing deleted" not in out.getvalue()
    print(f"  {'✓' if ok else '✗'} partial_delete_is_reported: a 403 on the 2nd of 3 deletes → 'deleted 1 of 3', rc 3"
          + ("" if ok else f"\n      got rc {rc}: {out.getvalue().strip()[-120:]}"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--package", help="e.g. amd64-paddisense-safety")
    ap.add_argument("--catalog", help="catalog dir holding config.yaml, e.g. paddisense-safety")
    ap.add_argument("--apply", action="store_true", help="delete (default: dry run)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest(Path(__file__).resolve().parent / "fixtures")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not (a.package and a.catalog and token):
        ap.error("--package, --catalog and GITHUB_TOKEN are required")
    try:
        return run(a.package, a.catalog, a.apply, token)
    except (Abort, urllib.error.URLError, KeyError, ValueError) as e:
        print(f"{a.package}: ABORT before any delete — nothing deleted: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
