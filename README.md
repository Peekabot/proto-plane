# proto-plane

Stdlib only. iSH + Pythonista.

Message `allow` is a list of dotted paths. Nothing else runs.

```sh
python3 proto.py '{"id":"n1","goal":"describe left-pad","allow":["tools.npm.doc.get"],"context":{"name":"left-pad"}}'
python3 proto.py '{"id":"p1","goal":"describe requests","allow":["tools.pypi.doc.get"],"context":{"name":"requests"}}'
```

## iSH -> Pythonista

```sh
cd
git clone https://github.com/Peekabot/proto-plane.git
cd proto-plane
tar --exclude='.git' -cf /tmp/plane.tar .
python3 -m http.server 8000 --bind 127.0.0.1
```

Pythonista: get `http://127.0.0.1:8000/plane.tar`, extract, skip `.git`.

Later: `git pull` then retar.
