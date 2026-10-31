#!/usr/bin/env python3
"""Small analogue (t classes, K) of the central formula: full clause evaluation on real sets.
- Generates base.cnf/base.json with the code under test: zcnf.py rot t K --m 2 --hull; hull cubes with hullcubes.py;
  second-layer cubes with l2cubes.py for every a (all three are generic in t).
- Numbers the convexity variables independently (same allocation order as described in zcnf.py: canonical 4-sets,
  then 5-sets, ..., (K-1)-sets in lexicographic order, after the triple variables) and checks the total.
- For designed and random real sets with a parallelogram hull, original and reflected, and every hull vertex as the
  first point: labels the set, evaluates EVERY clause of base.cnf (a failure is allowed only for a clause made of
  negated (K-1)-set convexity variables, and only when the set really has K points in convex position), the hull
  cubes (exactly one, the geometric one) and the second-layer cubes (exactly one, the geometric one), and checks the
  claimed relabellings (B): -> (P_a, {(a-i) mod t}) and (A): -> (P_{t-a}, ...).
usage: small_full.py t K n_designed n_random seed"""
import os
import itertools, os, random, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom import *

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")  # results
HERE = os.path.dirname(os.path.abspath(__file__))
t, K, nd, nr, seed = map(int, sys.argv[1:6])
W = os.path.join(HERE, "small", f"t{t}k{K}")
os.makedirs(W, exist_ok=True)
cnf, mapf = os.path.join(W, "base.cnf"), os.path.join(W, "base.json")
if not os.path.exists(mapf):
    subprocess.run(["python3", "-B", f"{R}/SYMZ/zcnf.py", "rot", str(t), str(K), "--m", "2", "--hull", "-o", cnf,
                    "--map", mapf], check=True, cwd=W, stdout=subprocess.DEVNULL)
    subprocess.run(["python3", "-B", f"{R}/C2C34/hullcubes.py", cnf, mapf, W], check=True, cwd=W,
                   stdout=subprocess.DEVNULL)
    for a in range(1, t):
        subprocess.run(["python3", "-B", f"{R}/C2C34/l2cubes.py", mapf, str(a), os.path.join(W, f"P{a}_cubes.txt")],
                       check=True, cwd=W)
    os.remove(os.path.join(W, "cover.cnf"))
mp = Map(mapf)
N, Z, nX, nv = mp.N, mp.Z, mp.nX, mp.info["vars"]
hull = load_cubes(os.path.join(W, "cubes.txt"))
l2 = {a: load_cubes(os.path.join(W, f"P{a}_cubes.txt")) for a in range(1, t)}
name = lambda a, V: f"P{a}_" + "-".join(map(str, sorted(V)))

# clauses, literals offset by nv for a flat truth table
clauses = []
with open(cnf) as f:
    for line in f:
        if line[0] in "cp":
            continue
        ls = [int(x) for x in line.split()[:-1]]
        clauses.append(tuple(l + nv for l in ls))
assert len(clauses) == mp.info["clauses"]

# independent numbering of convexity variables
def canon(S):
    T = tuple(sorted(i ^ 1 for i in S))
    return min(S, T)

conv_sets = []
for r in range(4, K):
    for S in itertools.combinations(range(N), r):
        if canon(S) == S:
            conv_sets.append(S)
assert nX + len(conv_sets) == nv, (nX, len(conv_sets), nv)
var_size = [0] * (nv + 1)
for k, S in enumerate(conv_sets):
    var_size[nX + 1 + k] = len(S)

cnt = dict(configs=0, labellings=0, kgon_sets=0, kfree_sets=0, allowed_kclause_fails=0, B_checked=0, A_checked=0,
           l2_none=0, fixedV=0)
fails = []
seen = set()


def evaluate(P, first, has_k):
    X = normal_form(P, first)
    val = mp.assign(X)
    tv = [False] * (2 * nv + 1)
    for v in range(1, nX + 1):
        tv[nv + v] = val[v] > 0
        tv[nv - v] = val[v] < 0
    for k, S in enumerate(conv_sets):
        c = in_convex_position([X[i] for i in S])
        v = nX + 1 + k
        tv[nv + v] = c
        tv[nv - v] = not c
    get = tv.__getitem__
    for cl in clauses:
        if not any(map(get, cl)):
            lits = [l - nv for l in cl]
            ok = has_k and all(l < 0 and -l > nX and var_size[-l] == K - 1 for l in lits)
            if not ok:
                raise AssertionError(f"clause {lits} false (has K-gon: {has_k})")
            cnt["allowed_kclause_fails"] += 1
    # cubes
    H, V2, Hp, H2p = geometry_case(X)
    assert len(H) == 2 and H[0] == 0, H
    a = H[1]
    sat_h = [n for n, c in hull.items() if cube_true(val, c)]
    if sat_h != [f"P{a}"]:
        raise AssertionError(f"hull cubes {sat_h} vs geometry P{a}")
    sat2 = [n for n, c in l2[a].items() if cube_true(val, c)]
    if len(H2p) in (4, 6):
        if sat2 != [name(a, V2)]:
            raise AssertionError(f"l2 cubes {sat2} vs geometry {name(a, V2)}")
        return a, tuple(V2)
    if sat2:
        raise AssertionError(f"second layer with {len(H2p)} vertices satisfies {sat2}")
    cnt["l2_none"] += 1
    return a, None


def run(P, p0):
    has_k = has_convex_k(P, K)
    cnt["kgon_sets" if has_k else "kfree_sets"] += 1
    res = evaluate(P, p0, has_k); cnt["labellings"] += 1
    ga, gV = res
    pa = normal_form(P, p0)[2 * ga]
    r = evaluate(P, neg(p0), has_k); cnt["labellings"] += 1
    if r != res:
        fails.append(f"-p0 {res} {r}")
    for f in (pa, neg(pa)):
        r = evaluate(P, f, has_k); cnt["labellings"] += 1; cnt["A_checked"] += 1
        exp = (t - ga, None if gV is None else tuple(sorted((i - ga) % t for i in gV)))
        if r != exp:
            fails.append(f"(A) rot {res} -> {r}, expected {exp}; P={P}")
    for kind in range(3):
        Q = reflect(P, kind)
        s = lambda p: reflect([p], kind)[0]
        for f in (s(pa), s(neg(pa))):
            r = evaluate(Q, f, has_k); cnt["labellings"] += 1; cnt["B_checked"] += 1
            exp = (ga, None if gV is None else tuple(sorted((ga - i) % t for i in gV)))
            if r != exp:
                fails.append(f"(B) {res} -> {r}, expected {exp}; P={P}")
            if gV is not None and exp == res:
                cnt["fixedV"] += 1
        for f in (s(p0), s(neg(p0))):
            r = evaluate(Q, f, has_k); cnt["labellings"] += 1
            exp = (t - ga, None if gV is None else tuple(sorted((-i) % t for i in gV)))
            if r != exp:
                fails.append(f"(A) refl {res} -> {r}, expected {exp}; P={P}")
    seen.add(res)


rng = random.Random(seed)
t0 = time.time()
inner_all = lambda a: [o for o in range(1, t) if o != a]
todo = []
# designed: cycle through every (a, V) first, then random ones
allAV = [(a, V) for a in range(1, t) for h in (2, 3) for V in itertools.combinations(inner_all(a), h)]
rng.shuffle(allAV)
for k in range(nd):
    todo.append(("d",) + allAV[k % len(allAV)])
todo += [("r", None, None)] * nr
for kind, a, V in todo:
    while True:
        if kind == "d":
            P, p0 = design(t, a, V, rng)
        else:
            P = random_set(t, rng)
            p0 = hull_ccw(P)[rng.randrange(4)] if len(hull_ccw(P)) == 4 else None
        if p0 is not None and general_position(P) and len(hull_ccw(P)) == 4:
            break
    cnt["configs"] += 1
    try:
        run(P, p0)
    except AssertionError as e:
        fails.append(f"{kind} a={a} V={V}: {e}; P={P}")
print(f"t={t} K={K} clauses={len(clauses)} vars={nv} conv={len(conv_sets)} time={time.time() - t0:.0f}s")
print("counts", cnt, "distinct (a,V) with a 4/6-vertex second layer reached", len({x for x in seen if x[1] is not None}), "of", len(allAV))
print("FAILURES", len(fails))
for x in fails[:20]:
    print("  ", x[:700])
