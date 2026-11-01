#!/usr/bin/env python3
"""Run chordcheck on every distinct order type (dedup by the canonm field) of the walk files in data/walks/."""
import subprocess, sys, re
chk = sys.argv[1]; every = sys.argv[2]; files = sys.argv[3:]
seen = set(); agg = dict(sets=0, hept=0, notgp=0, lemma=0, dp=0, cor=0, nest=0, hole=0, hexes=0, holes=0, hexhull=0, ears_all_nested=True)
hulls = {}
for fn in files:
    for line in open(fn):
        f = line.split()
        if len(f) < 6: continue
        canonm, n = f[3], int(f[4]); c = list(map(int, f[5:]))
        assert len(c) == 2 * n
        if canonm in seen: continue
        seen.add(canonm)
        inp = str(n) + " " + " ".join(map(str, c)) + "\n"
        out = subprocess.run([chk, "--every", every], input=inp, capture_output=True, text=True, check=True).stdout
        agg["sets"] += 1
        if "NOT IN GENERAL POSITION" in out: agg["notgp"] += 1; continue
        agg["hept"] += int(re.search(r"heptagons=(\d+)", out).group(1))
        v = re.search(r"lemma\(c!=m\)=(\d+) dp-vs-brute=(\d+)\S* corollary-region=(\d+) nesting=(\d+) hole-visibility=(\d+)", out)
        for k, g in zip(["lemma", "dp", "cor", "nest", "hole"], v.groups()): agg[k] += int(g)
        agg["hexes"] += int(re.search(r"convex hexagons=(\d+)", out).group(1))
        agg["holes"] += int(re.search(r"6-holes=(\d+)", out).group(1))
        hs = int(re.search(r"hull size (\d+)", out).group(1)); hulls[hs] = hulls.get(hs, 0) + 1
        if hs == 6:
            agg["hexhull"] += 1
            ears = re.findall(r"\((\d+),(\d)\)", out.split("hull ears")[1])
            if any(x[1] != "1" for x in ears): agg["ears_all_nested"] = False
            print("hexagonal hull set ears:", [int(x[0]) for x in ears])
print(agg); print("hull sizes:", hulls)
