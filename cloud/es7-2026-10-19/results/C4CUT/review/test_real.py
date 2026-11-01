"""Soundness tests of symcnf_layers.py (m=4) on exact real fourfold sets.
usage: test_real.py CNFDIR"""
import sys, time, random, itertools
from fractions import Fraction as F
sys.path.insert(0, __import__("os").path.dirname(__file__))
from geom import *
from evalcnf import CNF

CD = sys.argv[1]
cnfs = {}


def get(N):
    if N not in cnfs:
        cnfs[N] = CNF(f"{CD}/c4_n{N}L.cnf", f"{CD}/c4_n{N}L.json")
    return cnfs[N]


def transforms(P, c, rnd):
    """yield (name, P', c') : identity, mirror, rational rotation + translation, mirror of that"""
    yield "id", P, c
    yield "mirror", [(x, -y) for x, y in P], (c[0], -c[1])
    # rotation by a Pythagorean angle (3/5, 4/5) about origin, then translate by a rational vector
    a, b = F(3, 5), F(4, 5)
    tx, ty = F(rnd.randint(-50, 50), 7), F(rnd.randint(-50, 50), 3)
    rot = lambda p: (a * p[0] - b * p[1] + tx, b * p[0] + a * p[1] + ty)
    yield "rot+trans", [rot(p) for p in P], rot(c)
    yield "rot+trans+mirror", [(x, -y) for x, y in map(rot, P)], (rot(c)[0], -rot(c)[1])


def run_set(name, P, c, expect_free, rnd, verbose=True):
    N = len(P)
    cnf = get(N)
    n7 = len(convex_ksets(P, 7))
    if expect_free is not None:
        assert (n7 == 0) == expect_free
    out = []
    for tn, Q, cq in transforms(P, c, rnd):
        assert is_c4(Q, cq) and in_gp(Q)
        for first in range(4):
            lab = label_normal_form(Q, cq, first)
            r = cnf.evaluate(lab)
            ok = (r["symmetry_inconsistencies"] == 0 and r["violated_triple_only"] == 0
                  and r["violated_other"] == 0 and 4 * r["violated_Kset"] == n7)
            out.append(ok)
            if not ok or verbose:
                print(f"  {name} N={N} {tn} first={first}: convex7={n7} {r} {'OK' if ok else 'FAIL'}", flush=True)
    return all(out)


if __name__ == "__main__":
    rnd = random.Random(12345)
    P28 = [tuple(map(int, l.split()[:2])) for l in open(sys.argv[2]) if l.strip()]
    c0 = (0, 0)
    L = layers(P28)
    orbs = [orbit(V[0], c0) for V in L]
    allok = True
    t0 = time.time()
    # every subset of >= 2 orbits of the 28-point set (no convex 7-gon)
    for t in range(7, 1, -1):
        for keep in itertools.combinations(range(7), t):
            P = [p for o in keep for p in orbs[o]]
            ok = run_set(f"c4_28 orbits{keep}", P, c0, True, rnd, verbose=(t == 7))
            allok &= ok
        print(f"t={t} done, all ok so far: {allok}  ({time.time()-t0:.0f}s)", flush=True)
    print("ALL OK" if allok else "SOME FAILED")
