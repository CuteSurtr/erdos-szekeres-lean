#!/usr/bin/env python3
"""Check that satcount's enumerated convex (K-1)-gons equal cgon's count c_{K-1}
on random swept walk states and seed deletions.   usage: check_hexcount.py RUNSDIR OUTJSON N"""
import os, sys, json, glob, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dlib, walk

runs, outp, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
rng = random.Random(5)
sets = []
for f in glob.glob(os.path.join(runs, "walk", "states_w*.txt")):
    for line in open(f):
        sets.append(dlib.parse_line_pts(line.split(), 4))
rng.shuffle(sets)
sets = sets[:n]
tmp = os.path.join(runs, "tmp_hex"); os.makedirs(tmp, exist_ok=True)
ok = 0; bad = []
for i, P in enumerate(sets):
    p = os.path.join(tmp, f"h{i}.txt")
    dlib.write_pts(p, P)
    st = dlib.satcount_sweep(p, 7, "-", 1, 3)
    c = dlib.cgon_count(P, 7)
    if st["polys_K-1"] == c[6] and c[7] == 0:
        ok += 1
    else:
        bad.append(i)
    os.unlink(p)
res = {"checked": len(sets), "hexagon_count_equal_and_heptagon_free": ok, "bad": bad}
json.dump(res, open(outp, "w"))
print(res)
