#!/usr/bin/env python3
"""Planning only (no solving): from the record files of the repo, find for each needed root of the
3-fold class (m = 11, k = 7) the open frontier, using the split records and certified flags as
close_tree.py / compose.py read them (certified flags trusted, CNF hashes NOT re-derived: the
final composition does that).  Collapse rule: an uncovered six-bit cube whose layer subtree has
more than MAXLEAF open leaves becomes one unit (re-solved at a higher cap); otherwise its open
leaves are the units.
usage: plan_w6.py RESULTS_DIR OPEN_ROOTS_TSV FILES_TXT OUTDIR"""
import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "C3U2", "tools") if os.path.exists(os.path.join(HERE, "..", "..", "C3U2", "tools", "hullcase.py")) else HERE)
from hullcase import cube_layer_children, free_residues, node_name, parse_node, sigma_children  # noqa: E402

M, KC, MAXLEAF = 11, 7, 4
res, roots_tsv, files_txt, outdir = sys.argv[1:5]
sys.setrecursionlimit(100000)

files = [l.strip() for l in open(files_txt) if l.strip() and not l.startswith("#")]
extra = sorted(set(os.path.relpath(p, res) for pat in ("C3W4/*/out.jsonl", "C3W4/*/recheck*.jsonl",
                                                          "C3W5/*/out.jsonl", "C3COMP1/cap/out_lane*.jsonl")
                   for p in glob.glob(os.path.join(res, pat))))
files = list(dict.fromkeys(files + extra))
cert, sigcube_cert, splits = set(), set(), {}
nrec = 0
for f in files:
    p = os.path.join(res, f)
    if not os.path.exists(p):
        print("missing", f, file=sys.stderr)
        continue
    for l in open(p):
        l = l.strip()
        if not l:
            continue
        try:
            r = json.loads(l)
        except json.JSONDecodeError:
            print("bad line in", f, file=sys.stderr)
            continue
        nrec += 1
        if r.get("status") == "SATISFIABLE":
            print("SAT RECORD", f, r.get("node"), file=sys.stderr)
        if "cube" in r:
            if r.get("certified"):
                n = node_name(parse_node(r["node"])[0], sorted((int(x), v) for x, v in r["cube"].items()))
                cert.add(n)
                sigcube_cert.add(n)
            continue
        if r.get("certified"):
            cert.add(r["node"])
        if r.get("split"):
            splits.setdefault(r["node"], []).append(r)


def kids(n, rec):
    L, C = parse_node(n)
    if "sigma_bits" in rec:
        bits, ch = sigma_children(M, L, C, len(rec["sigma_bits"]))
        if bits != rec["sigma_bits"]:
            return []
        return [node_name(*c) for c in ch]
    return [node_name(*c) for c in cube_layer_children(M, KC, L, C)]


memo = {}


def covered(n):
    if n in memo:
        return memo[n]
    memo[n] = False
    ok = n in cert
    if not ok:
        for rec in splits.get(n, []):
            ks = kids(n, rec)
            if ks and all(covered(k) for k in ks):
                ok = True
                break
    if not ok:
        L, C = parse_node(n)
        if len(L) >= 2:
            fr = free_residues(M, L, C)
            for K in range(1, len(fr) + 1):
                if all(node_name(*c) in sigcube_cert for c in sigma_children(M, L, C, K)[1]):
                    ok = True
                    break
    memo[n] = ok
    return ok


def first_split(n):
    for rec in sorted(splits.get(n, []), key=lambda r: "sigma_bits" not in r):
        ks = kids(n, rec)
        if ks:
            return rec, ks
    return None, None


def leaves(n):
    if covered(n):
        return []
    rec, ks = first_split(n)
    if ks is None:
        return [n]
    return [x for k in ks for x in leaves(k)]


def units(n):
    """(node, kind) work units below n; kind: root (no split yet), six (six-bit cube re-solve),
    leaf (open leaf below a six-bit cube or of a two-orbit subtree)."""
    if covered(n):
        return []
    L, C = parse_node(n)
    rec, ks = first_split(n)
    if len(C) == 6:
        lv = leaves(n)
        if rec is None or len(lv) > MAXLEAF:
            return [(n, "six")]
        return [(x, "leaf") for x in lv]
    if ks is None:
        return [(n, "root" if not C and len(L) == 2 else "leaf")]
    return [u for k in ks for u in units(k)]



solved_unknown = set()
for f in files:
    p = os.path.join(res, f)
    if not os.path.exists(p):
        continue
    for l in open(p):
        l = l.strip()
        if l:
            r = json.loads(l)
            if "cube" not in r and r.get("status") == "UNKNOWN":
                solved_unknown.add(r["node"])

EXCLUDE = sys.argv[5].split(",") if len(sys.argv) > 5 else ["H3/one"]
rows = [l.rstrip("\n").split("\t") for l in open(roots_tsv)][1:]
os.makedirs(outdir, exist_ok=True)
pre, work, two, skipped = [], [], [], collections.Counter()
tag = "C3W6 planning: sigma split written without a solve (results/C3W6/TASK.md)"


def presplit(n, stratum, root, stop):
    """sigma-split n (a root or a 3-bit cube) down to cubes of `stop` bits, as close_tree.py would name them"""
    L, C = parse_node(n)
    bits, ch = sigma_children(M, L, C, 3)
    pre.append({"node": n, "split": True, "sigma_bits": bits, "children": len(ch), "planned": tag})
    for c in ch:
        cn = node_name(*c)
        if len(c[1]) == stop:
            if not covered(cn):
                work.append((cn, root, stratum, "presplit"))
        else:
            presplit(cn, stratum, root, stop)


for row in rows:
    root, stratum = row[0], row[1]
    if covered(root):
        continue
    if stratum in EXCLUDE:
        skipped[stratum] += 1
        continue
    for n, k in units(root):
        L, C = parse_node(n)
        if k == "six":
            work.append((n, root, stratum, "timeout300" if n in solved_unknown else "never_ran"))
        elif (k == "root" and not C) or (k == "leaf" and len(C) == 3):
            # H3 and one-orbit roots go straight to six-bit cubes (as C3W4 did with caps 1,1); a two-orbit
            # root is split one level only (its 3-bit cubes often close directly, results/C3W5)
            presplit(n, stratum, root, 3 if stratum.startswith("H6") and stratum.endswith("/two") and not C else 6)
        elif k == "leaf" and len(C) == 6 and len(L) > 2:
            # an open layer child of a six-bit cube whose layer subtree is almost done (at most MAXLEAF open)
            work.append((n, root, stratum, "layer_leaf"))
        else:
            raise SystemExit(f"unexpected unit {n} {k}")
assert len({w[0] for w in work}) == len(work)
with open(os.path.join(outdir, "W6.tsv"), "w") as f:
    f.write("row\tnode\troot\tstratum\tprior\n")
    for i, w in enumerate(sorted(work, key=lambda w: (w[2], w[1], w[0]))):
        f.write(f"{i}\t" + "\t".join(w) + "\n")
with open(os.path.join(outdir, "files.txt"), "w") as f:
    f.write("# record files read (paths under cloud/es7-2026-10-19/results/)\n" + "".join(x + "\n" for x in files))
with open(os.path.join(outdir, "presplit.jsonl"), "w") as f:
    for r in pre:
        f.write(json.dumps(r) + "\n")
print(f"files {len(files)}, records {nrec}; units {len(work)}, presplit records {len(pre)}, excluded roots {dict(skipped)}")
print(collections.Counter((w[2].split("/")[-1] if w[2].startswith("H6") else w[2], w[3]) for w in work))
