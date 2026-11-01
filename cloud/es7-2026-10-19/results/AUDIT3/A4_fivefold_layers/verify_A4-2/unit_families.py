#!/usr/bin/env python3
"""A4-2 check 1: classify the layer-form units of symcnf_layers.py (N=35, K=7, m=5) without building the big CNF.

Builds only the triple-variable map (cheap) and calls add_center_facts() and add_sb() into an in-memory sink.
Question answered: which of the three unit families of the layer form are *layer-lemma* facts and which are already
part of the base model (centre units emitted by symcnf.py for every orbit, in both the angle and the layer CNF)?
Also prints the exact list of layer sb clauses so that it can be compared with the tail of the solved CNF.
usage: python3 -B unit_families.py [N K m]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "enc"))
from symcnf_layers import LayerEncoding  # noqa: E402
from symcnf import SymEncoding  # noqa: E402

N, K, m = (int(x) for x in sys.argv[1:4]) if len(sys.argv) >= 4 else (35, 7, 5)

enc = LayerEncoding(N, K, m, body=None)       # body=None -> in-memory clause sink
enc.stats = {}
enc.add_center_facts()
n_centre = len(enc.clauses)
centre_units = {cl[0] for cl in enc.clauses.mem}
assert all(len(cl) == 1 for cl in enc.clauses.mem)
enc.add_sb()
sb = enc.clauses.mem[n_centre:]
assert all(len(cl) == 1 for cl in sb)
sb_lits = [cl[0] for cl in sb]
t, c = enc.t, enc.c
print(f"N={N} K={K} m={m} t={t} centre index={c}  centre units={len(centre_units)}  layer sb units={len(sb_lits)}")

# rebuild the families exactly as the encoder documents them
fam = {"sector": [], "polygon": [], "centre_inside": [], "nesting": []}
for o in range(1, t):
    fam["sector"].append(enc.lit(c, enc.pt(0, 0), enc.pt(o, 0)))
    fam["sector"].append(-enc.lit(c, enc.pt(0, 1), enc.pt(o, 0)))
for o in range(t):
    e0, e1 = enc.pt(o, 0), enc.pt(o, 1)
    for k in range(2, m):
        fam["polygon"].append(enc.lit(e0, e1, enc.pt(o, k)))
    fam["centre_inside"].append(enc.lit(e0, e1, c))
    for o2 in range(o + 1, t):
        for r in range(m):
            fam["nesting"].append(enc.lit(e0, e1, enc.pt(o2, r)))
rebuilt = fam["sector"] + [x for o in range(t) for x in
                           ([enc.lit(enc.pt(o, 0), enc.pt(o, 1), enc.pt(o, k)) for k in range(2, m)] +
                            [enc.lit(enc.pt(o, 0), enc.pt(o, 1), c)] +
                            [enc.lit(enc.pt(o, 0), enc.pt(o, 1), enc.pt(o2, r)) for o2 in range(o + 1, t)
                             for r in range(m)])]
print("rebuilt families equal the emitted sb list (same order):", rebuilt == sb_lits)
for name, lits in fam.items():
    dup = sum(1 for x in lits if x in centre_units)
    neg = sum(1 for x in lits if -x in centre_units)
    print(f"  {name:14s} {len(lits):4d} units; identical to a base centre unit: {dup}; contradicting one: {neg}")

# what does the angle form (symcnf.py) emit instead?  (orbit order units, not used by the layer form)
ang = SymEncoding(N, K, m, body=None)
ang.stats = {}
ang.add_center_facts()
assert {cl[0] for cl in ang.clauses.mem} == centre_units, "centre units differ between encodings"
k0 = len(ang.clauses)
ang.add_sb()
ang_sb = [cl[0] for cl in ang.clauses.mem[k0:]]
print(f"angle-form sb units: {len(ang_sb)}; shared with layer-form sb: {len(set(ang_sb) & set(sb_lits))}")
print(f"layer-form sb units not already among base centre units: "
      f"{sum(1 for x in sb_lits if x not in centre_units)}")
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"layer_sb_units_N{N}.txt"), "w") as f:
    for x in sb_lits:
        f.write(f"{x} 0\n")
