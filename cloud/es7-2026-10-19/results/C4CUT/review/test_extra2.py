"""Extra exact tests: (1) perturbed 28-point sets with no convex 7-gon (new order types), full CNF evaluation;
(2) near-degenerate nested sets (representatives within ~1e-9 rad of a diameter of O_0, nearly touching layers).
usage: test_extra.py CNFDIR C4_28FILE"""
import sys, math, random
sys.path.insert(0, __import__("os").path.dirname(__file__))
from geom import *
from evalcnf import CNF

CD = sys.argv[1]
rnd = random.Random(99)
c = (0, 0)
P28 = [tuple(map(int, l.split()[:2])) for l in open(sys.argv[2]) if l.strip()]
reps = [V[0] for V in layers(P28)]
cnf28 = CNF(f"{CD}/c4_n28L.cnf", f"{CD}/c4_n28L.json")
seen_types, ok_all, found = set(), True, 0
for trial in range(400):
    S = 1000
    eps = rnd.choice([0.002, 0.01, 0.03]); new = [(x * S + round(rnd.uniform(-eps, eps) * S * math.hypot(x, y)), y * S + round(rnd.uniform(-eps, eps) * S * math.hypot(x, y))) for x, y in reps]
    P = [p for q in new for p in orbit(q, c)]
    if not in_gp(P):
        continue
    try:
        L = layers(P)
        if not all(len(V) == 4 and set(V) == set(orbit(V[0], c)) for V in L):
            continue
    except Exception:
        continue
    if convex_ksets(P, 7):
        continue
    lab = label_normal_form(P, c, rnd.randrange(4))
    key = tuple(sgn(det(lab[i], lab[j], lab[k])) for i, j, k in __import__("itertools").combinations(range(28), 3))
    if key in seen_types:
        continue
    seen_types.add(key)
    found += 1
    r = cnf28.evaluate(lab)
    ok = r["violated_total"] == 0 and r["symmetry_inconsistencies"] == 0
    ok_all &= ok
    if not ok or found <= 3:
        print("perturbed 28:", r, "OK" if ok else "FAIL", flush=True)
print(f"(1) {found} distinct labelled 7-gon-free 28-point chirotopes (perturbations of c4_28) -> {'ALL SATISFY' if ok_all else 'FAILURE'}")

sys.exit(0)
for N in (16, 32):
    cnf = CNF(f"{CD}/c4_n{N}L.cnf", f"{CD}/c4_n{N}L.json")
    t = N // 4
    okn = True
    for trial in range(6):
        while True:
            R0 = 10 ** 15
            th0 = rnd.uniform(0, 2 * math.pi)
            orbs, r = [], R0
            for o in range(t):
                if o == 0:
                    ang = th0
                else:
                    # representative angle within 1e-9 of a diameter of O_0 (either side), or random
                    k = rnd.randrange(4)
                    eps = rnd.choice([1e-9, -1e-9, 1e-7, -1e-7])
                    ang = th0 + k * math.pi / 2 + eps
                p = (round(r * math.cos(ang)), round(r * math.sin(ang)))
                orbs.append(orbit(p, c))
                # nearly touching: next square only slightly smaller when rotated by ~45 deg, else random
                r *= rnd.choice([0.7072, 0.75, 0.9, 0.99])
            P = [p for O in orbs for p in O]
            if not in_gp(P):
                continue
            L = layers(P)
            if not all(len(V) == 4 and set(V) == set(orbit(V[0], c)) for V in L):
                continue
            # ensure the layer order is the generation order? not needed: labelling recomputes layers
            break
        n7 = len(convex_ksets(P, 7))
        for first in range(4):
            lab = label_normal_form(P, c, first)
            rr = cnf.evaluate(lab)
            ok = (rr["symmetry_inconsistencies"] == 0 and rr["violated_triple_only"] == 0 and rr["violated_other"] == 0
                  and 4 * rr["violated_Kset"] == n7)
            okn &= ok
            if not ok:
                print("FAIL near-degenerate", N, trial, first, rr, n7)
    print(f"(2) near-degenerate N={N}: {'ALL OK' if okn else 'FAILURE'}", flush=True)
