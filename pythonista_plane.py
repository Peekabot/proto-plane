# Pythonista. Same proto as iSH.
# 1) iSH: tar + python3 -m http.server 8000 --bind 127.0.0.1
# 2) Run pull_tar() once.
# 3) run_goal(...)

import json
import os
import sys
import tarfile
import urllib.request

ROOT = os.path.expanduser("~/Documents/proto-plane")
TAR_URL = "http://127.0.0.1:8000/plane.tar"


def pull_tar(url=TAR_URL, dest=ROOT):
    os.makedirs(dest, exist_ok=True)
    tar_path = os.path.join(dest, "_plane.tar")
    print("GET", url)
    urllib.request.urlretrieve(url, tar_path)
    with tarfile.open(tar_path, "r") as tf:
        for m in tf.getmembers():
            name = m.name.lstrip("./")
            if not name or name.startswith(".git"):
                continue
            tf.extract(m, dest)
    print("extracted", dest)
    return dest


def _load():
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    import proto
    proto._load_doors()
    return proto


def run_goal(name="left-pad", door="tools.npm.doc.get", mid="n1"):
    proto = _load()
    msg = {
        "id": mid,
        "goal": "describe " + name,
        "allow": [door],
        "context": {"name": name},
    }
    rep = proto.run(msg)
    print(json.dumps(rep, indent=2))
    return rep


if __name__ == "__main__":
    # First drop after iSH server is up:
    # pull_tar()
    run_goal("left-pad", "tools.npm.doc.get")
    # run_goal("requests", "tools.pypi.doc.get", mid="p1")
