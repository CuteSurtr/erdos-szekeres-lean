#!/usr/bin/env python3
"""receipt.py (26 Nov 2026): receipt of the deletions of CLEANUP20261126. Read-only. For each target: files, bytes,
and a digest = sha256 over the sorted lines "relpath<TAB>sha256(file)" (files only; symlinks listed by target).
Usage: receipt.py write|check. write -> receipt.json; check -> recompute and compare with receipt.json (exit 1 on any
difference), run right before deleting."""
import hashlib, json, os, sys
R = "/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results"
T = {
 "pkg-LEANLB20261111": (R + "/LEANLB20261111/.lake/packages", "duplicate Mathlib f897ebcf package copy; 60,103 of 60,177 files equal to the main repository's .lake/packages, the rest Lake .trace/.setup.json bookkeeping (20) and .git internals (42); restore: cp -a ~/research/lean/erdos-szekeres-lean/.lake/packages .lake/"),
 "pkg-ENCBLEAN-geo": (R + "/ENCBLEAN/geo/.lake/packages", "the same (geo's copy, from lake exe cache get on 7 Nov); restore as above, in ENCBLEAN/geo"),
 "pkg-LEANLB7_20261126": (R + "/LEANLB7_20261126/.lake/packages", "the copy restored from the main repository at 13:52:36 for the restore test (the original copy, digest in pkgs.json, was deleted at 13:52:35); restore as above"),
 "regen-fv302": ("/home/jay/research/data/cleanup-20261125/fv302-regen/export", "regenerated FV302 chunk sources of the 25 Nov regeneration test; verdict in git: FORMAL20261122/fv302/regen-test/compare.json (= work copy)"),
 "regen-s3520": ("/home/jay/research/data/cleanup-20261125/s3520-regen/out", "regenerated s35_20 chunk sources of the 25 Nov test; verdict in git: FORMAL20261122/res-slices-fv/regen-test/compare3520.{json,tsv}"),
 "regen-slices": ("/home/jay/research/data/cleanup-20261125/slices-regen/out", "regenerated slice chunk sources (3318-3519) of the 25 Nov test; verdict in git: res-slices-fv/regen-test/compare_slices.{json,tsv}"),
 "gh-c2-release-copy": ("/home/jay/research/data/gh-c2-20261125/release/P8_1-9.lrat.zst", "local copy of the C2 P8_1-9 proof; on GitHub as release c2-p8-1-9-2026-11-25 of the private archive repository (two parts); both halves of this file hash to that release's SHA256SUMS (fetched live, 26 Nov)"),
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
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "receipt.json"), "w"), indent=1)
    for k, v in out.items(): print(k, v["files"], v["bytes"], v["digest"][:16])
else:
    rc = json.load(open(os.path.join(os.path.dirname(__file__), "receipt.json"))); bad = 0
    for k, v in rc.items():
        s = summarize(v["path"]); ok = (s["files"], s["bytes"], s["digest"]) == (v["files"], v["bytes"], v["digest"])
        print(("OK  " if ok else "DIFF"), k, s["files"], s["bytes"]); bad += not ok
    sys.exit(1 if bad else 0)
