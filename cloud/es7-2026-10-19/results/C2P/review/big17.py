#!/usr/bin/env python3
"""Real 34-point (t = 17) centrally symmetric sets with a parallelogram hull, designed to hit every (a, V).
For the original set and a reflected copy, and every hull vertex as the first point:
  - label it in the normal form from the coordinates (geom.normal_form; my own code),
  - check every triple-class of the map is consistent (the identities) and the zero pattern,
  - evaluate the 136 SB units and 10,880 hull-SB clauses taken from the tail of the real base.cnf,
  - evaluate all 136 hull cubes (C2C34/cubes.txt): exactly one may hold, and it must be the geometric P_a,
  - evaluate all 560 second-layer cubes of that case: exactly one may hold, the geometric (P_a, V).
Then the claimed relabellings are compared with what the geometry gives:
  (B) reflect, first point = image of +-p_a      -> (P_a, {(a - i) mod 17 : i in V})
  (A) no reflection, first point = +-p_a          -> (P_{17-a}, {(i - a) mod 17})
      reflect, first point = image of +-p_0       -> (P_{17-a}, {(-i) mod 17})
      first point = -p_0                          -> (P_a, V)
The 7-gon clauses are not evaluated (such sets have 7-gons); the encoder itself was reviewed earlier.
usage: big17.py MAP HULLCUBES L2DIR TAIL a_lo a_hi seed [reps_per_V]"""
import itertools, random, sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom import *

mp = Map(sys.argv[1])
hull = load_cubes(sys.argv[2])
L2DIR = sys.argv[3]
lines = [l.split() for l in open(sys.argv[4]) if l.strip()]
sbu = [int(l[0]) for l in lines[:136]]
hsb = [[int(x) for x in l[:-1]] for l in lines[136:]]
assert len(hsb) == 10880
a_lo, a_hi, seed = int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
reps = int(sys.argv[8]) if len(sys.argv) > 8 else 1
T = mp.t
rng = random.Random(seed)
l2 = {a: load_cubes(f"{L2DIR}/P{a}_cubes.txt") for a in range(1, T)}
name = lambda a, V: f"P{a}_" + "-".join(map(str, sorted(V)))

cnt = dict(configs=0, rejected_gp=0, offdesign=0, labellings=0, B_checked=0, A_checked=0, fixedV=0)
fails = []
seen = set()


def classify(P, first):
    X = normal_form(P, first)
    val = mp.assign(X)
    for l in sbu:
        if not lit_true(val, l):
            raise AssertionError("SB unit false")
    for cl in hsb:
        if not any(lit_true(val, l) for l in cl):
            raise AssertionError(f"hull-SB clause false {cl}")
    H, V2, Hp, H2p = geometry_case(X)
    sat_h = [n for n, c in hull.items() if cube_true(val, c)]
    if len(H) == 2:
        a = [c for c in H if c != 0]
        assert len(a) == 1
        a = a[0]
        if sat_h != [f"P{a}"]:
            raise AssertionError(f"hull cubes satisfied {sat_h}, geometry P{a}")
        if len(H2p) in (4, 6):
            sat2 = [n for n, c in l2[a].items() if cube_true(val, c)]
            if sat2 != [name(a, V2)]:
                raise AssertionError(f"l2 cubes satisfied {sat2}, geometry {name(a, V2)}")
            return a, tuple(V2)
        else:
            sat2 = [n for n, c in l2[a].items() if cube_true(val, c)]
            if sat2:
                raise AssertionError(f"second layer has {len(H2p)} vertices but {sat2} satisfied")
            return a, None
    raise AssertionError(f"hull has {len(H)} classes")


t0 = time.time()
for a in range(a_lo, a_hi + 1):
    inner = [o for o in range(1, T) if o != a]
    allV = [V for h in (2, 3) for V in itertools.combinations(inner, h)]
    for V in allV:
        for _ in range(reps):
            while True:
                P, p0 = design(T, a, V, rng)
                if general_position(P):
                    break
                cnt["rejected_gp"] += 1
            cnt["configs"] += 1
            try:
                res = classify(P, p0)
                cnt["labellings"] += 1
                if res != (a, tuple(V)):
                    cnt["offdesign"] += 1
                ga, gV = res
                if gV is None:
                    continue
                pa = normal_form(P, p0)[2 * ga]          # the point (a, 0) of the original labelling
                # first point -p0
                r = classify(P, neg(p0)); cnt["labellings"] += 1
                if r != res:
                    fails.append(f"-p0: {res} -> {r}")
                # (A) rotation: first point +-p_a
                for f in (pa, neg(pa)):
                    r = classify(P, f); cnt["labellings"] += 1; cnt["A_checked"] += 1
                    exp = (T - ga, tuple(sorted((i - ga) % T for i in gV)))
                    if r != exp:
                        fails.append(f"(A) rot {res} -> {r}, expected {exp}")
                kind = rng.randrange(3)
                Q = reflect(P, kind)
                s = lambda p: reflect([p], kind)[0]
                # (B) reflect, first point = image of +-p_a
                for f in (s(pa), s(neg(pa))):
                    r = classify(Q, f); cnt["labellings"] += 1; cnt["B_checked"] += 1
                    exp = (ga, tuple(sorted((ga - i) % T for i in gV)))
                    if r != exp:
                        fails.append(f"(B) {res} -> {r}, expected {exp}  P={P}")
                    if exp == res:
                        cnt["fixedV"] += 1
                # (A) via reflection: first point = image of +-p0
                for f in (s(p0), s(neg(p0))):
                    r = classify(Q, f); cnt["labellings"] += 1
                    exp = (T - ga, tuple(sorted((-i) % T for i in gV)))
                    if r != exp:
                        fails.append(f"(A) refl {res} -> {r}, expected {exp}")
                seen.add(res)
            except AssertionError as e:
                fails.append(f"config a={a} V={V}: {e}  P={P}")
    print(f"a={a} done, {time.time() - t0:.0f}s, fails so far {len(fails)}", flush=True)

print("counts", cnt, "distinct (a,V) reached", len(seen))
print("FAILURES", len(fails))
for x in fails[:20]:
    print("  ", x[:600])
