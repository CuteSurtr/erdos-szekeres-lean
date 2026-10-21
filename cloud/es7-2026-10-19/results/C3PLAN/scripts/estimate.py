#!/usr/bin/env python3
"""Extrapolated cost of the whole C3 class with the current method, per stratum (top case x
layer-2 type).  Inputs: results/C3PLAN/stats.tsv (stats.py), the wave out.jsonl records, and the
root counts of results/C3-S/manifest_depth2.tsv.  Costs are solve + check core-seconds per node,
summed (not wall clock).
Per-node cost model, from all wave records: bucket b = (s = sigma_a of the top case, layer-2 type,
depth, orbits in the last layer); c_b = mean solve_s over attempted nodes (timeouts count their
cap) + mean check_s over certified nodes.  A partial root costs what it has spent plus, for each
open node (timed out and unsplit, or never attempted), c_b of its bucket ("mid").  "low" uses
0.5 c_b, "high" 3 c_b for the open nodes (the open nodes of a partial root are the harder half of
its tree, and a d3 single-after-single node always timed out at 300 s and was split).
A stratum's per-root cost is the mean over its closed and (extrapolated) partial roots; a stratum
with no data takes the per-root costs of the measured strata with the same (s, layer-2 type); the
spread over its measured roots gives low/high (10th / 90th percentile scaled by the root count is
not used: low = mean of the measured "low", high = mean of the measured "high").
H3 (no wave data) takes the C3-S Knuth-walk numbers (results/C3-S/README.md, "Measurements" 6):
mid = median 446 solve core-hours, low 218, high 6.8e5 (the heaviest walk), times 1.27 for checking
(check is about 0.27 x solve, C3-S README "Measurements" 7).
usage: estimate.py  (run from cloud/es7-2026-10-19; prints a table)"""
import collections
import csv
import glob
import json
import sys

sys.path.insert(0, "results/C3-S/tools")
from hullcase import parse_layers, tree_children, layers_name  # noqa: E402


def key(node):
    L = parse_layers(node)
    s = "H3" if len(L[0]) == 1 else f"s{L[0][1][1]}"
    return (s, "one" if len(L[1]) == 1 else "two", len(L), len(L[-1]))


A = collections.defaultdict(lambda: [0, 0, 0.0, 0.0])
cert, split, att = set(), set(), set()
for f in glob.glob("results/C3WAVE1/*/out.jsonl") + glob.glob("results/C3WAVE2/*/out.jsonl"):
    for l in open(f):
        try:
            r = json.loads(l)
        except ValueError:
            continue
        if r.get("split"):
            split.add(r["node"])
            continue
        a = A[key(r["node"])]
        a[0] += 1
        a[2] += r["solve_s"]
        att.add(r["node"])
        if r.get("certified"):
            cert.add(r["node"])
            a[1] += 1
            a[3] += r.get("check_s", 0)
cb = {k: a[2] / a[0] + (a[3] / a[1] if a[1] else 0) for k, a in A.items()}


def cbk(k):
    if k in cb:
        return cb[k]
    s, t, d, o = k  # deepest measured bucket of the same kind
    ks = [x for x in cb if x[:2] == (s, t) and x[3] == o and x[2] <= d] or [x for x in cb if x[:2] == (s, t)]
    return cb[max(ks, key=lambda x: x[2])]


def open_nodes(n):
    if n in cert:
        return []
    if n in split:
        return [x for c in tree_children(11, 7, parse_layers(n)) for x in open_nodes(layers_name(c))]
    return [n]


rows = list(csv.DictReader(open("results/C3PLAN/stats.tsv"), delimiter="\t"))
per = collections.defaultdict(list)  # (top, l2type) -> [(low, mid, high, status)]
for r in rows:
    if r["status"] == "untouched":
        continue
    spent = float(r["solve_s"]) + float(r["check_s"])
    ext = sum(cbk(key(n)) for n in open_nodes(r["root"]))
    per[(r["top"], r["l2type"])].append((spent + 0.5 * ext, spent + ext, spent + 3 * ext, r["status"]))
count = collections.Counter((r["top"], r["l2type"]) for r in rows)


def s_of(top):
    return "H3" if top == "H3" else "s" + top[-2]


tot = [0.0, 0.0, 0.0]
totm = [0.0, 0.0, 0.0]  # with the H6 mirror reduction of PLAN.md (kept: 5 of 9 one-orbit, 76 of 144 two-orbit roots)
print("stratum\troots\tmeasured(closed/partial)\tper_root_core_h(low/mid/high)\tstratum_core_h(low/mid/high)\tsource")
for st in sorted(count):
    n = count[st]
    if st[0] == "H3":
        lo, mid, hi = (x * 1.27 * 3600 / 100 for x in (218, 446, 6.8e5))
        src = "C3-S Knuth walks (H3 stratum, 100 roots)"
        meas = "0/0"
    else:
        v = per.get(st)
        src = "own roots"
        if not v:
            v = [x for k, xs in per.items() if k[0] != "H3" and s_of(k[0]) == s_of(st[0]) and k[1] == st[1] for x in xs]
            src = f"borrowed: all measured {s_of(st[0])}/{st[1]} roots"
        meas = f"{sum(x[3] == 'closed' for x in per.get(st, []))}/{sum(x[3] == 'partial' for x in per.get(st, []))}"
        lo, mid, hi = (sum(x[i] for x in v) / len(v) for i in range(3))
    tot = [tot[0] + n * lo, tot[1] + n * mid, tot[2] + n * hi]
    f = 1 if st[0] == "H3" else (5 / 9 if st[1] == "one" else 76 / 144)
    totm = [totm[0] + f * n * lo, totm[1] + f * n * mid, totm[2] + f * n * hi]
    print(f"{st[0]}/{st[1]}\t{n}\t{meas}\t{lo/3600:.2f}/{mid/3600:.2f}/{hi/3600:.2f}\t"
          f"{n*lo/3600:.0f}/{n*mid/3600:.0f}/{n*hi/3600:.0f}\t{src}")
print("TOTAL core-hours low/mid/high:", "/".join(f"{x/3600:.0f}" for x in tot))
print("TOTAL with H6 mirror reduction, core-hours low/mid/high:", "/".join(f"{x/3600:.0f}" for x in totm))
H3 = [x * 1.27 for x in (218, 446, 1681)]
print("H3 high from the second-heaviest walk (1,681 solve core-h) instead of 6.8e5:",
      "no mirror", f"{(tot[2] - 1.27 * 6.8e5 * 3600) / 3600 + H3[2]:.0f}", "with H6 mirror", f"{(totm[2] - 1.27 * 6.8e5 * 3600) / 3600 + H3[2]:.0f}")
print("bucket costs c_b (s):", json.dumps({"/".join(map(str, k)): round(v, 1) for k, v in sorted(cb.items())}))
