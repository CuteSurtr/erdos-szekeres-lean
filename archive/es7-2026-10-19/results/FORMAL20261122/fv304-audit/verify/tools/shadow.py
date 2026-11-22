#!/usr/bin/env python3
"""rv4 own two-roots check: every relative .olean / .olean.server / .olean.private path must occur under at most one
root of a LEAN_PATH. Read only (directory walk, no hashing). Usage: shadow.py OUT.json"""
import json, os, sys

FV = "/home/jay/research/data/fv304-20261120/lean_path.txt"
AUDIT_ROOT = "/home/jay/research/data/formalize-20261122/fv304-audit/olean"
RES118_ROOT = "/home/jay/research/data/formalize-20261122/res118/olean"
EXTS = (".olean", ".olean.server", ".olean.private")


def files_under(root):
    out = set()
    for d, _, fs in os.walk(root, followlinks=True):
        for f in fs:
            if f.endswith(EXTS):
                out.add(os.path.relpath(os.path.join(d, f), root))
    return out


def dups(roots, per_root):
    seen = {}
    for r in roots:
        for rel in per_root[r]:
            seen.setdefault(rel, []).append(r)
    return {rel: rs for rel, rs in seen.items() if len(rs) > 1}


roots14 = open(FV).read().strip().split(":")
assert len(roots14) == 14 and len(set(roots14)) == 14, roots14
per_root = {r: files_under(r) for r in roots14 + [AUDIT_ROOT, RES118_ROOT]}
res = {
    "roots14": roots14,
    "files_per_root": {r: len(v) for r, v in per_root.items()},
    "dups_fv304_path": dups(roots14, per_root),
    "dups_with_audit_root": dups(roots14 + [AUDIT_ROOT], per_root),
    "negative_control_with_res118_root": sorted(dups(roots14 + [RES118_ROOT], per_root)),
}
res["ok"] = not res["dups_fv304_path"] and not res["dups_with_audit_root"] and bool(res["negative_control_with_res118_root"])
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps({k: res[k] for k in ("dups_fv304_path", "dups_with_audit_root", "negative_control_with_res118_root", "ok")}, indent=1))
