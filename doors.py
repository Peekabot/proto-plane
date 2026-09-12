#!/usr/bin/env python3
"""REST catalog doors. Read-only. No install."""
from __future__ import annotations

import json
import urllib.request

from proto import bind


def _get_json(url, accept=None):
    headers = {}
    if accept:
        headers["Accept"] = accept
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def pypi_doc(name):
    return _get_json(f"https://pypi.org/pypi/{name}/json")


def npm_doc(name, version=None):
    path = name.replace("/", "%2f")
    url = f"https://registry.npmjs.org/{path}"
    if version:
        url += f"/{version}"
    return _get_json(url, accept="application/vnd.npm.install-v1+json")


@bind("tools.pypi.doc.get")
def pypi_get(msg):
    name = (msg.get("context") or {}).get("name")
    if not name:
        return {"ok": False, "result": {"why": "context.name missing"}}
    doc = pypi_doc(name)
    info = doc.get("info") or {}
    return {
        "ok": True,
        "result": {
            "name": info.get("name"),
            "version": info.get("version"),
            "requires": info.get("requires_dist") or [],
        },
    }


@bind("tools.npm.doc.get")
def npm_get(msg):
    ctx = msg.get("context") or {}
    name = ctx.get("name")
    if not name:
        return {"ok": False, "result": {"why": "context.name missing"}}
    doc = npm_doc(name, ctx.get("version"))
    latest = (doc.get("dist-tags") or {}).get("latest")
    ver = (doc.get("versions") or {}).get(latest) or {}
    deps = ver.get("dependencies") or {}
    return {
        "ok": True,
        "result": {
            "name": doc.get("name"),
            "version": latest,
            "requires": list(deps),
        },
    }
