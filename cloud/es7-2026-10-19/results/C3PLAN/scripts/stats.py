#!/usr/bin/env python3
"""Per-root statistics of the C3 waves.
Reads every results/C3WAVE1/*/out.jsonl and results/C3WAVE2/*/out.jsonl and the depth-2 roots of
results/C3-S/manifest_depth2.tsv; writes one row per root to stats.tsv (stdout if no argument).
Columns: split_by_depth counts all split nodes (pre-split one-orbit nodes and nodes split after a
timeout); timeout_then_split_by_depth the latter; timeout_open_by_depth nodes that timed out and were
not yet split; unattempted_by_depth children of split nodes never solved.  solve_s and check_s sum
all records of the root's subtree (per-node times, not wall clock).
A root is closed if every leaf of its tree is certified: a node is closed if some record certifies
it, or if it has a split record and all its children (hullcase.tree_children, mirror reduction on)
are closed.  usage: stats.py [OUT.tsv]   (run from cloud/es7-2026-10-19)"""
import collections
import glob
import json
import sys

sys.path.insert(0, "results/C3-S/tools")
from hullcase import layers_name, parse_layers, tree_children  # noqa: E402

cert, split, att = set(), set(), collections.Counter()
solve, check = collections.Counter(), collections.Counter()
src = {}
nrec = 0
for f in sorted(glob.glob("results/C3WAVE1/*/out.jsonl") + glob.glob("results/C3WAVE2/*/out.jsonl")):
    wave = f.split("/")[1][-1]
    for l in open(f):
        try:
            r = json.loads(l)
        except ValueError:
            continue
        nrec += 1
        n = r["node"]
        src.setdefault(n.split("_")[0] + "_" + n.split("_")[1] if n.count("_") else n, set()).add(wave)
        if r.get("split"):
            split.add(n)
            continue
        if r.get("status") == "SATISFIABLE":
            print("SAT RECORD", n, file=sys.stderr)
        att[n] += 1
        solve[n] += r.get("solve_s", 0)
        check[n] += r.get("check_s", 0) or 0
        if r.get("certified"):
            cert.add(n)

roots = [l.split("\t")[1] for l in open("results/C3-S/manifest_depth2.tsv") if l.startswith("2\t")]


def walk(n, d, acc):
    """returns True if closed; fills acc with per-depth counts"""
    if n in cert:
        acc["cert", d] += 1
        return True
    if n in split:
        acc["split", d] += 1
        if att[n]:
            acc["tosplit", d] += 1
        ok = True
        for c in tree_children(11, 7, parse_layers(n)):
            ok &= walk(layers_name(c), d + 1, acc)
        return ok
    if att[n]:
        acc["timeout", d] += 1
    else:
        acc["unatt", d] += 1
    return False


def fmt(acc, kind):
    return ",".join(f"d{d}:{v}" for (k, d), v in sorted(acc.items()) if k == kind) or "-"


def top(L1):
    if len(L1) == 1:
        return "H3"
    a, s = L1[1]
    return f"H6({a},{s})"


cols = ["root", "top", "l2type", "l2", "l2sigma", "waves", "status", "cert_by_depth", "split_by_depth", "timeout_then_split_by_depth",
        "timeout_open_by_depth", "unattempted_by_depth", "n_cert", "n_open", "max_depth", "solve_s", "check_s"]
out = open(sys.argv[1], "w") if len(sys.argv) > 1 else sys.stdout
out.write("\t".join(cols) + "\n")
for r in roots:
    L = parse_layers(r)
    acc = collections.Counter()
    sub = [n for n in att if n == r or n.startswith(r + "_")]
    touched = bool(sub) or r in split
    closed = walk(r, 2, acc)
    st = "closed" if closed else ("partial" if touched else "untouched")
    if not touched:
        acc = collections.Counter()
    l2 = L[1]
    row = [r, top(L[0]), "one" if len(l2) == 1 else "two", "-".join(str(x[0]) for x in l2),
           "".join("-" if x[1] is None else str(x[1]) for x in l2), "".join(sorted(src.get(r, []))) or "-", st,
           fmt(acc, "cert"), fmt(acc, "split"), fmt(acc, "tosplit"), fmt(acc, "timeout"), fmt(acc, "unatt"),
           sum(v for (k, d), v in acc.items() if k == "cert"),
           sum(v for (k, d), v in acc.items() if k in ("timeout", "unatt")),
           max([d for (k, d) in acc] or [0]),
           round(sum(solve[n] for n in sub), 1), round(sum(check[n] for n in sub), 1)]
    out.write("\t".join(map(str, row)) + "\n")
print(f"records {nrec}, roots {len(roots)}", file=sys.stderr)
