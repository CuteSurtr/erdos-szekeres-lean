#!/usr/bin/env python3
"""fv304-audit: independent re-check of data/closure_{audit,combined}.tsv, written separately from tools/fv4a.py.
For every row: the file is <root>/<module path>.olean, and no other root of that LEAN_PATH has the same relative path
(a direct existence test per root, not a directory walk). The coreutils sha256sum of the file equals the row's
sha256. Library rows equal library.json and chain311 rows equal build.tsv's last ok row (fresh parses). The E304Z rows
of the audit closure equal {Root, Final} plus the import lines of the Root and S3 sources (parsed from export/src,
not from the context manifests). Prints one JSON line; exit 1 on any mismatch.  Run: python3 -I -B tools/recheck.py"""
import collections, json, os, subprocess, sys
from pathlib import Path

W = Path("/home/jay/research/data/formalize-20261122/fv304-audit")
FV = Path("/home/jay/research/data/fv304-20261120")
REPO = Path("/home/jay/research/lean/erdos-szekeres-lean")
CHAIN = REPO / "experiments/omission-compact-checker-2026-11-05/build/chain311"
fv_roots = (FV / "lean_path.txt").read_text().strip().split(":")
lib = json.loads((CHAIN / "library.json").read_text())
lroots = [r.replace("<repo>", str(REPO)).replace("<home>", str(Path.home())) for r in lib["roots"]]
libpin = {m: (lroots[i], h) for m, (i, h) in lib["modules"].items()}
blines = (CHAIN / "build.tsv").read_text().splitlines()
hdr, chain = blines[0].split("\t"), {}
for line in blines[1:]:
    d = dict(zip(hdr, line.split("\t")))
    chain[d["module"]] = d["olean_sha256"] if d["verdict"] == "ok" else None
bad, out, tables = [], {}, {}
for job, roots in (("audit", fv_roots), ("combined", fv_roots + [str(W / "olean")])):
    rows = [l.split("\t") for l in (W / f"data/closure_{job}.tsv").read_text().splitlines()[1:]]
    tables[job] = (roots, rows)
files = sorted({os.path.join(r[1], r[0].replace(".", "/") + ".olean") for _, rows in tables.values() for r in rows})
sums = {}
for i in range(0, len(files), 400):
    res = subprocess.run(["sha256sum", "--", *files[i:i + 400]], capture_output=True, text=True, check=True)
    for line in res.stdout.splitlines():
        h, f = line.split("  ", 1)
        sums[f] = h
for job, (roots, rows) in tables.items():
    for m, root, real, h, pin, st in rows:
        rel = m.replace(".", "/") + ".olean"
        hits = [r for r in roots if os.path.exists(os.path.join(r, rel))]
        f = os.path.join(root, rel)
        if hits != [root]:
            bad.append(f"{job} {m}: provided by {hits}, row says {root}")
        if sums.get(f) != h:
            bad.append(f"{job} {m}: sha256sum {sums.get(f)} != row {h}")
        if os.path.realpath(f) != real:
            bad.append(f"{job} {m}: resolves to {os.path.realpath(f)}, row says {real}")
        if root in lroots and libpin.get(m) != (root, h):
            bad.append(f"{job} {m}: library.json pin {libpin.get(m)}")
        if root == str(CHAIN / "olean") and chain.get(m) != h:
            bad.append(f"{job} {m}: chain311 build.tsv pin {chain.get(m)}")
        if st != "ok":
            bad.append(f"{job} {m}: status {st}")
    out[job] = {"rows": len(rows), "pins": dict(collections.Counter(r[4] for r in rows))}
src = FV / "export/src/E304Z"
imps = set()
for f in [src / "Root.lean"] + sorted(src.glob("S3_*.lean")):
    imps |= {l.split()[1] for l in f.read_text().splitlines() if l.startswith("import E304Z.")}
want = imps | {"E304Z.Root", "E304Z.Final"}
got = {r[0] for r in tables["audit"][1] if r[0].startswith("E304Z.")}
if want != got:
    bad.append(f"E304Z set: from the S3/Root imports {len(want)}, in the audit closure {len(got)}; "
               f"missing {sorted(want - got)[:5]}, extra {sorted(got - want)[:5]}")
out.update(files_hashed=len(files), e304z_from_imports=len(want), problems=bad[:20], n_problems=len(bad))
print(json.dumps(out))
sys.exit(1 if bad else 0)
