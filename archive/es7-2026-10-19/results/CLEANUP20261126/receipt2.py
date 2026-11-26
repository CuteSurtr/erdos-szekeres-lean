#!/usr/bin/env python3
"""receipt.py (26 Nov 2026): receipt of the second deletion set of CLEANUP20261126 (owner-approved 26 Nov wrap-up). Read-only. For each target: files, bytes,
and a digest = sha256 over the sorted lines "relpath<TAB>sha256(file)" (files only; symlinks listed by target).
Usage: receipt.py write|check. write -> receipt2.json; check -> recompute and compare with receipt2.json (exit 1 on any
difference), run right before deleting."""
import hashlib, json, os, sys
R = "/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results"
T = {
 "pkg-e810-hall-reduction": ("/home/jay/research/tools/e810-lean/research/hall-reduction/.lake/packages", "duplicate Mathlib f897ebcf package copy of the #810 project; 60,075 of 60,176 files equal to the repository's .lake/packages, the rest Lake .trace/.setup.json bookkeeping (20) and .git internals (54), none missing (pkgs.json); restore: cp -a ~/research/lean/erdos-szekeres-lean/.lake/packages .lake/"),
 "b70zs54-occ": ("/home/jay/research/data/bal186-20261119/zrow/b70zs54/occ", "resumable state of the stopped exploratory budget-70 finder (98 of 16,384 contexts closed, no witness, no result claimed; stopped by memguard 26 Nov 07:46); its PLAN.md, steps.log and occ.out stay; owner 26 Nov: do not restart the 301 search"),
}
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""): h.update(b)
    return h.hexdigest()
def summarize(path):
    if os.path.isfile(path):
        return {"files": 1, "bytes": os.path.getsize(path), "digest": sha(path)}
    n = b = 0; lines = []
    for root, dirs, files in os.walk(path):
        dirs.sort()
        for fn in sorted(files):
            p = os.path.join(root, fn); rel = os.path.relpath(p, path)
            if os.path.islink(p): lines.append(f"{rel}\t->{os.readlink(p)}"); continue
            n += 1; b += os.path.getsize(p); lines.append(f"{rel}\t{sha(p)}")
    return {"files": n, "bytes": b, "digest": hashlib.sha256("\n".join(lines).encode()).hexdigest()}
mode = sys.argv[1]
if mode == "write":
    out = {k: dict(path=v[0], why=v[1], **summarize(v[0])) for k, v in T.items()}
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "receipt2.json"), "w"), indent=1)
    for k, v in out.items(): print(k, v["files"], v["bytes"], v["digest"][:16])
else:
    rc = json.load(open(os.path.join(os.path.dirname(__file__), "receipt2.json"))); bad = 0
    for k, v in rc.items():
        s = summarize(v["path"]); ok = (s["files"], s["bytes"], s["digest"]) == (v["files"], v["bytes"], v["digest"])
        print(("OK  " if ok else "DIFF"), k, s["files"], s["bytes"]); bad += not ok
    sys.exit(1 if bad else 0)
