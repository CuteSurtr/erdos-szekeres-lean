#!/usr/bin/env python3
"""needed_roots.tsv from mycompose --dump outputs (off and --h6m) on the same records.
usage: needed_roots.py MANIFEST OFF.d2 ON.d2 > needed_roots.tsv"""
import csv, sys, collections
M = 11
def toks(lay):
    return sorted((int(t.split("s")[0]), int(t.split("s")[1]) if "s" in t else -1) for t in lay.split("-"))
def name(t):
    return "-".join(f"{r}" if s < 0 else f"{r}s{s}" for r, s in t)
off = {l.split("\t")[0]: l.split() for l in open(sys.argv[2])}
on = {l.split("\t")[0] for l in open(sys.argv[3])}
rows = [r["node"] for r in csv.DictReader(open(sys.argv[1]), delimiter="\t") if r["depth"] == "2"]
assert set(rows) == set(off) and on <= set(off) and len(rows) == 1630 and len(on) == 910
print("node\tstratum\tin_reduced_cut\tmirror_partner\tstatus")
cnt = collections.Counter()
for n in rows:
    top, l2 = n.split("_")
    T, L = toks(top), toks(l2)
    kind = "one" if len(L) == 1 else "two"
    if len(T) == 1:
        st = f"H3/{kind}"; partner = top + "_" + name(sorted(((M - r) % M, (1 - s) if s >= 0 else -1) for r, s in L))
    else:
        a, s = T[1]
        st = f"H6({a},{s})/{kind}"
        partner = top + "_" + name(sorted(((a - r) % M, -1 if g < 0 else g ^ (r < a) ^ (s == 0)) for r, g in L))
        assert partner in off
    status = "closed" if off[n][1] == "1" else ("partial" if off[n][2] == "1" else "untouched")
    inc = "yes" if n in on else "no"
    print(f"{n}\t{st}\t{inc}\t{partner if len(T) == 2 else '-'}\t{status}")
    cnt[(st.split("/")[0][:2] + "/" + kind, inc, status)] += 1
    cnt[(st, inc, status)] += 1
for k in sorted(cnt):
    print("#", *k, cnt[k], sep="\t", file=sys.stderr)
