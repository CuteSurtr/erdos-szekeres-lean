#!/usr/bin/env python3
"""P8 pilot work list. The 560 second-layer subcases of P8 (l2/P8_cubes.txt) fall into orbits of the relabelling
i -> (8 - i) mod 17 (reflect the configuration, then restart the angular normal form at the other hull class); this maps
a real configuration in subcase (P8, V) to one in subcase (P8, V'). units.txt lists P8_cover (the certified cover of the
560-way split) first, then one representative per orbit (quadrilateral and hexagonal second layers interleaved, shuffled
with a fixed seed), then the other members. orbits.tsv: subcase, representative. cover.cnf: base + P8 hull cube units +
one clause per subcase forbidding its second-layer literals.
usage: mkunits.py C"""
import random, sys
C = sys.argv[1]
A, T = 8, 17
cubes = {}
for l in open(f"{C}/l2/P8_cubes.txt"):
    name, *lits = l.split(); cubes[name] = [int(x) for x in lits]
hull = [int(x) for x in next(l for l in open(f"{C}/hc34/cubes.txt") if l.split()[0] == f"P{A}").split()[1:]]
hs = set(hull)
assert all(hs <= set(c) for c in cubes.values())
def img(name):
    V = [int(x) for x in name.split("_")[1].split("-")]
    return f"P{A}_" + "-".join(map(str, sorted((A - i) % T for i in V)))
rep = {}
for n in cubes:
    m = img(n); assert m in cubes and img(m) == n
    key = lambda s: tuple(int(x) for x in s.split("_")[1].split("-"))
    rep[n] = min(n, m, key=key)
reps = sorted(set(rep.values())); others = sorted(n for n in cubes if rep[n] != n)
def interleave(names, seed):
    rnd = random.Random(seed)
    q = [n for n in names if n.count("-") == 1]; h = [n for n in names if n.count("-") == 2]
    rnd.shuffle(q); rnd.shuffle(h)
    out, k = [], 0
    while q or h:
        if q and (not h or k % 5 == 0): out.append(q.pop())
        else: out.append(h.pop())
        k += 1
    return out
order = ["P8_cover"] + interleave(reps, 1) + interleave(others, 2)
open(f"{C}/p8/units.txt", "w").write("\n".join(order) + "\n")
open(f"{C}/p8/orbits.tsv", "w").write("subcase\trepresentative\n" + "".join(f"{n}\t{rep[n]}\n" for n in sorted(cubes)))
nq = sum(r.count("-") == 1 for r in reps); print(f"subcases {len(cubes)}, orbits {len(reps)} ({nq} quadrilateral, {len(reps) - nq} hexagonal), others {len(others)}")
# cover CNF
base = f"{C}/c34h_final.cnf"
with open(base) as f, open(f"{C}/p8/cover.cnf", "w") as g:
    for line in f:
        if line.startswith("p cnf"):
            _, _, nv, nc = line.split()
            g.write(f"p cnf {nv} {int(nc) + len(hull) + len(cubes)}\n")
        else:
            g.write(line)
    for l in hull: g.write(f"{l} 0\n")
    for n in sorted(cubes):
        g.write(" ".join(str(-l) for l in cubes[n] if l not in hs) + " 0\n")
print("cover clauses:", len(hull), "hull units +", len(cubes), "subcase clauses")
