"""Cube split for the k = 5 question (used only if the single CNF is too hard).

Base CNF B (any of the k=5 CNFs written by rainbow.py).  V = a 3-set or 5-set (default X1 = {0,1,3}, mask 11);
its 5 edges e_1..e_5 pairwise lie in common 4-cycles.  For each bijection pi of {e_i} onto the 5 colours, cube_pi = B + units x(e_i, pi(e_i)).
Covering argument: in any model of B, give each edge its least true colour (clause (1)); the 5 edges of V then
carry 5 pairwise different colours (clauses (2)), i.e. a bijection pi, and the model satisfies cube_pi.
So: all 120 cube CNFs UNSAT => B UNSAT.
Usage: python cubes.py G.json base.cnf outdir [mask of the star vertex, default 11 = {0,1,3}]
"""
import sys, json, itertools, os

g = json.load(open(sys.argv[1])); base = open(sys.argv[2]).read().split("\n"); out = sys.argv[3]
k = 5
E = [tuple(e) for e in g["edges"]]; masks = g["masks"]
mask = int(sys.argv[4]) if len(sys.argv) > 4 else 11
x1 = masks.index(mask)
star = [i for i, (u, v) in enumerate(E) if x1 in (u, v)]
assert len(star) == 5
hdr = base[0].split(); assert hdr[:2] == ["p", "cnf"]
nv, nc = int(hdr[2]), int(hdr[3])
body = [l for l in base[1:] if l.strip()]
assert len(body) == nc
os.makedirs(out, exist_ok=True)
for n, pi in enumerate(itertools.permutations(range(k))):
    units = [f"{e * k + c + 1} 0" for e, c in zip(star, pi)]
    with open(f"{out}/cube{n:03d}.cnf", "w") as f:
        f.write(f"p cnf {nv} {nc + 5}\n" + "\n".join(body + units) + "\n")
print(f"wrote 120 cubes over the star of mask {mask} (edges {star})")
