#!/usr/bin/env python3
"""Which sigma-cube-format threefold pieces is the project's cover unable to do without?

Population.  The 280 record files of results/C3FINAL/compose_files.txt.  A record is certified exactly when
compose.py counts it (certified truthy, lrat_check == 'c VERIFIED', cake_lpr == 's VERIFIED UNSAT').  A record
of results/C3PLAN/scripts/sigma_cubes.py has a "cube" field and its "node" is the PARENT node; its piece is
parent + '__' + the cube sorted by residue (exactly compose.py's reading).  A piece is "sigma-only" when it is
certified by sigma-cube-format records and by no plain-format record (so the C3SPOT sample, which excluded the
sigma-cube format, could not have drawn it).

Runs (every run is the repository's C3U2/tools/compose.py, unchanged, read-only, with --mirror-h6 --no-sha, on
the 280 files; the files that lose lines are replaced by filtered copies, every other byte is kept):
  full      : nothing dropped (must be covered)
  drop:<n>  : for each sigma-only piece n, its certified sigma-format records dropped   -> n necessary iff uncovered
  keep_nec  : certified sigma-format records of every sigma-only piece NOT found necessary dropped (sufficiency)
  keep_none : certified sigma-format records of every sigma-only piece dropped (control: must be uncovered)
Because compose.py's coverage is monotone in the set of records (a record can only add certified nodes, splits
and explored prefixes; no rule tests for the absence of a record), 'drop:n uncovered for every n in NEC' and
'keep_nec covered' together say: NEC is contained in every subset of sigma-only pieces that, with all
plain-format records, covers the class, and NEC itself is such a subset, i.e. NEC is the unique minimum.
Writes OUT/runs.jsonl (one line per run), OUT/summary.json, OUT/necessary.txt; and, for the independent A2
composer, full filtered trees OUT/trees/<variant>/ + files.txt for keep_nec and keep_none (--trees).
usage: python3 -I -B indispensable.py RESULTS_DIR BASE OUTDIR [--trees]"""
import json
import os
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
RD, BASE, OUT = sys.argv[1:4]
TREES = "--trees" in sys.argv
PYC = os.path.join(OUT, "pycache_prefix_unused")  # pyc lookups go here (never into the repository's __pycache__)
sys.pycache_prefix = PYC
sys.path.insert(0, os.path.join(RD, "C3a"))
sys.path.insert(0, os.path.join(RD, "C3U2", "tools"))
from hullcase import node_name, parse_node  # noqa: E402

os.makedirs(OUT, exist_ok=True)
COMPOSE = os.path.join(RD, "C3U2", "tools", "compose.py")
files = [l.strip() for l in open(os.path.join(RD, "C3FINAL", "compose_files.txt")) if l.strip()]
assert len(files) == 280, len(files)


def own_canon(node, cube):
    """independent canonicalisation (cross-check of hullcase.parse_node/node_name)."""
    if cube is not None:
        assert "__" not in node
        return node + "__" + "-".join(f"{r}s{v}" for r, v in sorted((int(a), int(b)) for a, b in cube.items()))
    if "__" not in node:
        return node
    lay, cub = node.split("__")
    pairs = sorted((int(t.split("s")[0]), int(t.split("s")[1])) for t in cub.split("-"))
    return lay + "__" + "-".join(f"{r}s{v}" for r, v in pairs)


cert_sig, cert_plain = {}, set()
nrec = canon_mismatch = 0
for f in files:
    for i, l in enumerate(open(os.path.join(RD, f))):
        if not l.strip():
            continue
        r = json.loads(l)
        nrec += 1
        if "node" not in r:
            continue
        if "cube" in r:
            lay, C0 = parse_node(r["node"])
            assert not C0
            name = node_name(lay, sorted((int(x), v) for x, v in r["cube"].items()))
        else:
            name = node_name(*parse_node(r["node"]))
        if name != own_canon(r["node"], r.get("cube")):
            canon_mismatch += 1
        if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
            if "cube" in r:
                cert_sig.setdefault(name, []).append((f, i))
            else:
                cert_plain.add(name)
sig_only = sorted(set(cert_sig) - cert_plain)
both = sorted(set(cert_sig) & cert_plain)
print(json.dumps({"records": nrec, "certified_sigma_format_pieces": len(cert_sig), "certified_plain_pieces": len(cert_plain),
                  "both_formats": len(both), "sigma_only": len(sig_only), "canon_mismatch": canon_mismatch}), flush=True)

TMP = os.path.join(OUT, "tmp")


def compose(drop):
    """drop: {file: set(line indices)} -> compose.py summary dict (+ exit, seconds)."""
    if os.path.exists(TMP):
        shutil.rmtree(TMP)
    os.makedirs(TMP)
    args = []
    for f in files:
        if f in drop:
            p = os.path.join(TMP, f.replace("/", "__"))
            with open(os.path.join(RD, f), "rb") as fi, open(p, "wb") as fo:
                for i, line in enumerate(fi):
                    if i not in drop[f]:
                        fo.write(line)
            args.append(p)
        else:
            args.append(os.path.join(RD, f))
    t = time.time()
    cp = subprocess.run([sys.executable, "-I", "-B", "-X", f"pycache_prefix={PYC}", COMPOSE, BASE] + args
                        + ["--mirror-h6", "--no-sha"], capture_output=True, text=True)
    res = {"exit": cp.returncode, "s": round(time.time() - t, 2)}
    try:
        o = json.loads(cp.stdout.strip().splitlines()[-1])
        for k in ("class_covered", "uncovered_frontier_nodes", "certified_nodes", "certified_records",
                  "certified_cube_nodes", "sigma_splits_used", "error"):
            if k in o:
                res[k] = o[k]
    except Exception:  # noqa: BLE001
        res["error"] = (cp.stdout[-400:] + cp.stderr[-400:])
    shutil.rmtree(TMP)
    return res


def drops_for(names):
    d = {}
    for n in names:
        for f, i in cert_sig[n]:
            d.setdefault(f, set()).add(i)
    return d


runs = open(os.path.join(OUT, "runs.jsonl"), "w")


def record(tag, names, res):
    line = {"run": tag, "dropped_pieces": len(names), "dropped_records": sum(len(cert_sig[n]) for n in names)}
    line.update(res)
    runs.write(json.dumps(line) + "\n")
    runs.flush()
    return line


t0 = time.time()
full = record("full", [], compose({}))
print(json.dumps(full), flush=True)
nec, unnec, bad = [], [], []
for j, n in enumerate(sig_only):
    res = record("drop:" + n, [n], compose(drops_for([n])))
    if res.get("exit") != 0 or not isinstance(res.get("class_covered"), bool):
        bad.append(n)
    elif res["class_covered"]:
        unnec.append(n)
    else:
        nec.append(n)
    if j % 25 == 0:
        print(f"{j + 1}/{len(sig_only)} necessary so far {len(nec)} ({time.time() - t0:.0f} s)", flush=True)
keep_nec = record("keep_nec", sorted(set(sig_only) - set(nec)), compose(drops_for(sorted(set(sig_only) - set(nec)))))
keep_none = record("keep_none", sig_only, compose(drops_for(sig_only)))
runs.close()

src = lambda n: sorted({f.split("/")[0] for f, _ in cert_sig[n]})
summary = {
    "compose": COMPOSE, "options": ["--mirror-h6", "--no-sha"], "files": len(files), "records": nrec,
    "certified_sigma_format_pieces": len(cert_sig), "certified_plain_pieces": len(cert_plain),
    "pieces_certified_in_both_formats": len(both), "sigma_only_pieces": len(sig_only),
    "canonicalisation_mismatches_vs_own": canon_mismatch,
    "full_covered": full.get("class_covered"),
    "necessary": len(nec), "unnecessary": len(unnec), "runs_with_errors": bad,
    "necessary_by_source": {s: sum(1 for n in nec if src(n) == [s]) for s in sorted({x for n in nec for x in src(n)})},
    "unnecessary_by_source": {s: sum(1 for n in unnec if src(n) == [s]) for s in sorted({x for n in unnec for x in src(n)})},
    "keep_nec_covered": keep_nec.get("class_covered"), "keep_none_covered": keep_none.get("class_covered"),
    "keep_nec": keep_nec, "keep_none": keep_none, "seconds": round(time.time() - t0, 1),
}
json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
open(os.path.join(OUT, "necessary.txt"), "w").write("".join(n + "\n" for n in sorted(nec)))
print(json.dumps({k: v for k, v in summary.items() if k not in ("keep_nec", "keep_none")}), flush=True)

if TREES:  # full filtered trees (relative paths kept) for the independent composer
    for tag, names in (("keep_nec", sorted(set(sig_only) - set(nec))), ("keep_none", sig_only)):
        d = drops_for(names)
        root = os.path.join(OUT, "trees", tag)
        for f in files:
            dst = os.path.join(root, f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(os.path.join(RD, f), "rb") as fi, open(dst, "wb") as fo:
                for i, line in enumerate(fi):
                    if i not in d.get(f, ()):
                        fo.write(line)
        open(os.path.join(root, "files.txt"), "w").write("".join(f + "\n" for f in files))
    print("trees written", flush=True)
