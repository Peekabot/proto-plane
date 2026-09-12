#!/usr/bin/env python3
"""Dotted-name proto. Message allow-list is the firewall."""
from __future__ import annotations

import json
import sys

REGISTRY = {}


def bind(name):
    def wrap(fn):
        REGISTRY[name] = fn
        return fn
    return wrap


def deny(name, msg, why):
    return {
        "id": msg.get("id"),
        "from": name,
        "action": "proto.deny",
        "ok": False,
        "result": {"why": why},
        "leftover": [],
    }


def call(name, msg):
    allow = msg.get("allow") or []
    if name not in allow:
        return deny(name, msg, "not in allow")
    fn = REGISTRY.get(name)
    if fn is None:
        return deny(name, msg, "proto.missing")
    out = fn(msg) or {}
    out.setdefault("id", msg.get("id"))
    out.setdefault("from", name)
    out.setdefault("action", name)
    out.setdefault("ok", True)
    out.setdefault("leftover", [])
    return out


def run(msg):
    allow = msg.get("allow") or []
    for name in allow:
        if name.startswith("skills.") or name.startswith("tools."):
            rep = call(name, msg)
            if rep.get("ok"):
                return rep
    for name in allow:
        if name.startswith("tiers."):
            return call(name, msg)
    return deny("human.ask", msg, "nothing in allow ran")


def _load_doors():
    import doors  # noqa: F401
    # python3 proto.py => this file is __main__, doors binds onto module proto
    proto = sys.modules.get("proto")
    if proto is not None and proto is not sys.modules[__name__]:
        REGISTRY.update(getattr(proto, "REGISTRY", {}))


def main():
    _load_doors()
    if len(sys.argv) < 2:
        print("usage: proto.py '{json msg}'", file=sys.stderr)
        sys.exit(2)
    raw = sys.argv[1]
    if raw == "-":
        raw = sys.stdin.read()
    msg = json.loads(raw)
    print(json.dumps(run(msg), indent=2))


if __name__ == "__main__":
    main()
