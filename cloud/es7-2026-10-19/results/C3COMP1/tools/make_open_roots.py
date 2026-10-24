#!/usr/bin/env python3
"""C3COMP1 copy of C3U2/tests/make_open_roots.py, changed only so that a frontier-size difference is allowed and both sizes are written
(frontier_size = mycompose, compose_frontier = C3U2 compose.py, which also lists a sigma-split cube node whose sigma split is open and that has
no layer split, next to the frontier of its cubes: see README).  Status must still agree.
Write open_roots.tsv from frontier_cmp.py's ROOTS.tsv of the official --mirror-h6 composition:
every depth-2 root of the reduced cut with its stratum (C3PLAN/scripts/stats.py: top = H3 or
H6(a,s) from layer 1, l2type = one or two orbits in layer 2), status (closed / open, from C3U2
compose.py, which must agree with mycompose) and, for open roots, its frontier size.
usage: make_open_roots.py ROOTS.tsv OUT.tsv [W4LIST.tsv ...]   (W4 lists: cross-check of the stratum)"""
import collections, os, sys
sys.path.insert(0, "/opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools")
from hullcase import parse_node  # noqa: E402


def stratum(name):
    L = parse_node(name)[0]
    top = "H3" if len(L[0]) == 1 else f"H6({L[0][1][0]},{L[0][1][1]})"
    return top + ("/one" if len(L[1]) == 1 else "/two")


rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1])][1:]
out, cnt = [], collections.Counter()
for r, s1, f1, s2, f2 in rows:
    if s1 != s2:
        sys.exit(f"compose and mycompose disagree on {r}")
    st = stratum(r)
    cnt[(st, s1)] += 1
    out.append((r, st, s1, f2 if s1 == "open" else "", f1 if s1 == "open" else ""))
with open(sys.argv[2], "w") as f:
    f.write("root\tstratum\tstatus\tfrontier_size\tcompose_frontier\n")
    f.writelines("\t".join(x) + "\n" for x in out)
bad = 0
for w in sys.argv[3:]:
    for l in list(open(w))[1:]:
        x = l.rstrip("\n").split("\t")
        if stratum(x[1]) != x[4]:
            bad += 1
print(f"roots {len(out)}, open {sum(1 for x in out if x[2] == 'open')}, frontier {sum(int(x[3]) for x in out if x[3])}; "
      f"stratum mismatches against the W4 lists: {bad}")
print("stratum\troots\topen\tclosed\topen_frontier(mycompose)\topen_frontier(compose)")
for st in sorted({x[1] for x in out}, key=lambda s: (s[:2] != "H3", s)):
    o = [x for x in out if x[1] == st]
    print(f"{st}\t{len(o)}\t{sum(1 for x in o if x[2] == 'open')}\t{sum(1 for x in o if x[2] == 'closed')}\t"
          f"{sum(int(x[3]) for x in o if x[3])}\t{sum(int(x[4]) for x in o if x[4])}")
