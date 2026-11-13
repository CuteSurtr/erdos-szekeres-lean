"""Random exact nested fourfold sets (integer coords, centre 0): every non-K-gon clause of the CNF must hold under the
true chirotope in the layer normal form, and the falsified K-set clauses must be exactly the orbits of convex 7-sets.
Also negative controls with deliberately wrong labellings.  usage: test_random.py CNFDIR N TRIALS SEED"""
import sys, math, random, time
sys.path.insert(0, __import__("os").path.dirname(__file__))
from geom import *
from evalcnf import CNF

CD, N, TR, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
t = N // 4
rnd = random.Random(SEED)
c = (0, 0)


def nested(P_orbs):
    for o in range(len(P_orbs) - 1):
        A, B = P_orbs[o], P_orbs[o + 1]
        for j in range(4):
            for q in B:
                if det(A[j], A[(j + 1) % 4], q) <= 0:
                    return False
    return True


def gen():
    while True:
        R0 = 10 ** 6
        r = R0
        orbs = []
        for o in range(t):
            ang = rnd.uniform(0, 2 * math.pi)
            p = (round(r * math.cos(ang)), round(r * math.sin(ang)))
            orbs.append(orbit(p, c))
            r *= rnd.uniform(0.70, 0.97)
        if not nested(orbs):
            continue
        P = [p for O in orbs for p in O]
        if in_gp(P):
            return P


t0 = time.time()
cnf = CNF(f"{CD}/c4_n{N}L.cnf", f"{CD}/c4_n{N}L.json")
print(f"loaded N={N} in {time.time()-t0:.0f}s", flush=True)
allok = True
for tr in range(TR):
    P = gen()
    n7 = len(convex_ksets(P, 7))
    L = layers(P)
    assert all(set(V) == set(orbit(V[0], c)) for V in L), "layers are not orbits"
    for variant in ("id", "mirror"):
        Q = P if variant == "id" else [(x, -y) for x, y in P]
        first = rnd.randrange(4)
        lab = label_normal_form(Q, c, first)
        r = cnf.evaluate(lab)
        ok = (r["symmetry_inconsistencies"] == 0 and r["violated_triple_only"] == 0 and r["violated_other"] == 0
              and 4 * r["violated_Kset"] == n7)
        allok &= ok
        print(f"trial {tr} {variant} first={first}: convex7={n7} {r} {'OK' if ok else 'FAIL'}", flush=True)
    if tr == 0:
        # negative controls on the first set: each must falsify some triple-only clause
        lab = label_normal_form(P, c, 0)
        ctr = {}
        # (a) swap two layers
        L2 = lab[:4] + lab[8:12] + lab[4:8] + lab[12:]
        ctr["swap layers 1,2"] = L2
        # (b) representative of layer 1 in the wrong sector (rotate it by one step)
        L3 = list(lab); L3[4:8] = lab[5:8] + lab[4:5]
        ctr["layer-1 rep in next sector"] = L3
        # (c) clockwise labelling of all orbits
        L4 = []
        for o in range(t):
            L4 += [lab[4 * o + ((-r) % 4)] for r in range(4)]
        ctr["clockwise order"] = L4
        # (d) only orbit 0 rotated by one step ((0,0) := old (0,1)), others kept: sector units should break
        L5 = list(lab); L5[0:4] = lab[1:4] + lab[0:1]
        ctr["(0,0) moved, reps not updated"] = L5
        for k, Lx in ctr.items():
            r = cnf.evaluate(Lx)
            print(f"  control [{k}]: {r} -> {'rejected (good)' if r['violated_triple_only'] or r['symmetry_inconsistencies'] else 'NOT REJECTED'}",
                  flush=True)
print("ALL OK" if allok else "SOME FAILED", f"{time.time()-t0:.0f}s")
