#!/usr/bin/env python3
"""Claim 8: do the l2sgn.py / l3sgn.py cube literals mean what their docstrings say, on real configurations?
And claim 7 at cube level: is the literal set of mirror(c) exactly -c, with the stated name mapping?

Steps: run l2sgn.py on the n=34 base formula (my work dir), then for real labelled configurations (my normal form,
generic nu) compute the nested inner hull layers myself and check:
  * exactly one second-layer cube is satisfied by the real orientations, and it is the one named by my layer
    computation (none if the inner hull has >= 8 vertices);
  * l3sgn.py children of that cube: exactly one satisfied and it matches my next layer;
  * structural: for every cube c, mirror(c) is present with literal set -c (Q3.x <-> Q3.(n+1-x),
    H3.a.b <-> H3.(n+1-b).(n+1-a); general Qi/Hi likewise).
usage: t5_cubes.py SEED TRIALS"""
import itertools, json, math, os, random, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv import *
from cnfeval import build, WORK
from t4_mirror import layer_names, mirror_name, nu_ties

HERE = os.path.dirname(os.path.abspath(__file__))
L2 = os.path.join(HERE, "..", "sgn", "l2sgn.py"); L3 = os.path.join(HERE, "..", "sgn", "l3sgn.py")
N = 34


def inside_strict(poly, q):
    h = len(poly)
    return all(det(poly[e], poly[(e + 1) % h], q) > 0 for e in range(h))


def layered(rng, layer_sizes, R=10 ** 6):
    """uv-coordinates: outer square +-R (parallelogram after the linear map), then nested symmetric convex layers with
    the given numbers of vertex pairs; remaining inner pairs (to reach 15) random inside the innermost layer."""
    while True:
        A = (rng.randint(-9, 9), rng.randint(-9, 9)); B = (rng.randint(-9, 9), rng.randint(-9, 9))
        if cross(A, B) > 0:
            break
    Lm = lambda p: (p[0] * A[0] + p[1] * B[0], p[0] * A[1] + p[1] * B[1])
    for attempt in range(200):
        outer = [(R, R), (-R, R), (-R, -R), (R, -R)]
        prev = outer; pairs = []; ok = True
        r = 0.95 * R
        for h in layer_sizes:
            for _ in range(200):
                angs = sorted(rng.uniform(0, math.pi) for _ in range(h))
                rad = [r * rng.uniform(0.7, 1.0) for _ in range(h)]
                V = [(int(rd * math.cos(a)), int(rd * math.sin(a))) for a, rd in zip(angs, rad)]
                poly = V + [neg(v) for v in V]
                if len(set(poly)) == 2 * h and all(inside_strict(prev, q) for q in poly) and len(hull_ccw(poly)) == 2 * h:
                    break
            else:
                ok = False; break
            pairs += V; prev = hull_ccw(poly); r *= 0.6
        if not ok:
            continue
        need = 15 - len(pairs)
        tries = 0
        while need > 0 and tries < 20000:
            tries += 1
            q = (rng.randint(-int(r), int(r)), rng.randint(-int(r), int(r)))
            if q != (0, 0) and inside_strict(prev, q):
                pairs.append(q); need -= 1
        if need > 0:
            continue
        P = [Lm(p) for p in outer] + [Lm(x) for p in pairs for x in (p, neg(p))]
        if len(set(P)) == len(P) and general_position(P) and len(hull_ccw(P)) == 4:
            return P
    return None


def main():
    seed, T = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed); t0 = time.time()
    F = build(N, 7, par=True, centre=True, rs=True)
    mapf = F.path + ".json"; cubef = os.path.join(WORK, "l2_34.cubes"); cover = os.path.join(WORK, "l2_34_cover.cnf")
    if not os.path.exists(cubef):
        r = subprocess.run([sys.executable, L2, F.path, mapf, str(N), cubef, cover], capture_output=True, text=True, check=True)
        print("l2sgn:", r.stdout.strip())
        os.remove(cover)   # not needed here; large
    cubes = {}
    for line in open(cubef):
        w = line.split(); cubes[w[0]] = [int(x) for x in w[1:]]
    # structural mirror check
    A = lambda x: N + 1 - x
    def mname(nm):
        v = list(map(int, nm[1:].split(".")))
        return f"Q{v[0]}.{A(v[1])}" if nm[0] == "Q" else f"H{v[0]}.{A(v[2])}.{A(v[1])}"
    s_ok = s_bad = s_missing = 0
    for nm, lits in cubes.items():
        mn = mname(nm)
        if mn not in cubes:
            s_missing += 1; continue
        if set(cubes[mn]) == {-l for l in lits}:
            s_ok += 1
        else:
            s_bad += 1
    print(json.dumps({"cubes": len(cubes), "Q3": sum(1 for c in cubes if c.startswith("Q3.")),
                      "H3": sum(1 for c in cubes if c.startswith("H3.")),
                      "mirror_pairs_literal_negation_ok": s_ok, "bad": s_bad, "mirror_missing": s_missing}))
    st = dict(configs=0, l2_ok=0, l2_bad=0, l2_none_ok=0, l3_ok=0, l3_bad=0, l3_skipped=0)
    ex = []
    for tr in range(T):
        sizes = [rng.choice([2, 3]) for _ in range(rng.randint(1, 6))]
        while sum(sizes) > 15:
            sizes.pop()
        P = layered(rng, sizes) if rng.random() < 0.85 else rand_par_set(rng, 15)
        if P is None or len(hull_ccw(P)) != 4:
            continue
        S, info = par_normal_form(P, rs=True, choice=rng.randrange(2))
        if nu_ties(S, info):
            continue
        st["configs"] += 1
        o = orient_table(S)
        val = {}
        for t, v in F.ov.items():
            val[v] = o[t]
        holds = lambda lits: all(val[l] if l > 0 else not val[-l] for l in lits)
        names = layer_names(S)
        sat = [nm for nm, lits in cubes.items() if holds(lits)]
        exp = [names[0]] if names and names[0][0] in "QH" else []
        if sat == exp:
            st["l2_ok" if exp else "l2_none_ok"] += 1
        else:
            st["l2_bad"] += 1; ex.append(("l2", names, sat))
            continue
        if not exp or len(names) < 2 or names[1][0] not in "QH":
            st["l3_skipped"] += 1; continue
        r = subprocess.run([sys.executable, L3, mapf, str(N), cubef, names[0]], capture_output=True, text=True, check=True)
        kids = {}
        for line in r.stdout.splitlines():
            w = line.split(); kids[w[0]] = [int(x) for x in w[1:]]
        ksat = [nm for nm, lits in kids.items() if holds(lits)]
        if ksat == [names[0] + "/" + names[1]]:
            st["l3_ok"] += 1
        else:
            st["l3_bad"] += 1; ex.append(("l3", names, ksat))
    print(json.dumps(st))
    for e in ex[:3]:
        print("EXAMPLE", e)
    print("time", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
