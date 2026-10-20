#!/usr/bin/env python3
"""From realized 26-point sets to new heptagon-free 32-point sets.
For each S (integer points):
  1. exact checks: general position, largest convex subset <= 6 (chiro.largest_convex_subset);
  2. direction scan: for every combinatorially distinct sweep direction (between consecutive critical
     angles of the C(26,2) pair directions) an exact integer similarity (x,y) -> (c x - s y, s x + c y),
     c, s small integers, puts that direction up; the max cap in that frame is computed exactly;
  3. for each direction with max cap <= 4, build32.build adds a 6-cap deep below (the Lemma gives
     lcs <= max(6, 2 + cap) = 6; the result is re-checked anyway by check32.py);
  4. dedupe the 32-point sets by their x-sorted signotope; write them as OUT/<name>_d<k>.pts.
If a 32-point set has |coordinate| >= 2^27 (sat.c's bound), the realizer is run on its exact
chirotope to find a smaller realization of the same labelled order type, accepted only after an exact
re-check; it is written as <name>_d<k>_small.pts.
usage: process26.py OUTDIR S1.pts [S2.pts ...]  (JSON lines)"""
import hashlib, itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "realizer"))
sys.path.insert(0, HERE)
from chiro import largest_convex_subset, chirotope_of, verify_exact  # noqa
from build32 import build, orient  # noqa

def max_cap(pts):
    """exact max cap of points sorted by x (distinct x); cap = clockwise consecutive triples"""
    P = sorted(pts); n = len(P); L = {}; best = min(n, 2)
    for j in range(n):
        for k in range(j + 1, n):
            v = 2
            for i in range(j):
                if orient(P[i], P[j], P[k]) < 0: v = max(v, L[(i, j)] + 1)
            L[(j, k)] = v; best = max(best, v)
    return best

def sig_hash(pts):
    P = sorted(pts)
    return hashlib.sha1("".join("+" if orient(P[i], P[j], P[k]) > 0 else "-" for i, j, k in
                                itertools.combinations(range(len(P)), 3)).encode()).hexdigest()[:16]

def directions(S):
    """small integer (c, s) for one angle inside every arc between critical angles"""
    crit = set()
    for p, q in itertools.combinations(S, 2):
        a = math.atan2(q[1] - p[1], q[0] - p[0])  # x-order changes when the 'up' angle is perpendicular
        for t in (a, a + math.pi):
            crit.add(t % (2 * math.pi))
    crit = sorted(crit); out = []
    for i, a in enumerate(crit):
        b = crit[(i + 1) % len(crit)] + (2 * math.pi if i + 1 == len(crit) else 0)
        mid = (a + b) / 2; width = b - a
        for e in range(2, 40):
            sc = 1 << e
            c, s = round(sc * math.cos(mid)), round(sc * math.sin(mid))
            if abs(math.atan2(s, c) % (2 * math.pi) - mid % (2 * math.pi)) < width / 4: break
        out.append((c, s))
    return out

def main():
    outdir = sys.argv[1]; os.makedirs(outdir, exist_ok=True)
    for path in sys.argv[2:]:
        name = os.path.splitext(os.path.basename(path))[0]
        S = [tuple(map(int, l.split())) for l in open(path) if l.strip()]
        rec = {"set": name, "n": len(S)}
        try:
            chirotope_of(S); rec["general_position"] = True
        except ValueError:
            rec["general_position"] = False; print(json.dumps(rec), flush=True); continue
        rec["lcs"] = largest_convex_subset(S)
        if rec["lcs"] > 6: print(json.dumps(rec), flush=True); continue
        seen = {}; dirs = directions(S); good = 0
        for c, s in dirs:
            R = [(c * x - s * y, s * x + c * y) for x, y in S]
            if len(set(p[0] for p in R)) < len(R): continue
            if max_cap(R) > 4: continue
            good += 1
            T, M = build(R)
            P = R + T
            h = sig_hash(P)
            if h in seen: continue
            k = len(seen); seen[h] = k
            fn = os.path.join(outdir, f"{name}_d{k}.pts")
            with open(fn, "w") as f:
                for x, y in P: f.write(f"{x} {y}\n")
            mx = max(max(abs(x), abs(y)) for x, y in P)
            if mx >= 2 ** 27:
                from realize import realize
                chi = chirotope_of(P)
                for seed in range(3):
                    res = realize(chi, len(P), budget=60, seed=seed)
                    if res["realized"]:
                        Q = [tuple(p) for p in res["points"]]
                        if verify_exact(Q, chi)[0] and max(max(abs(x), abs(y)) for x, y in Q) < 2 ** 27:
                            with open(fn.replace(".pts", "_small.pts"), "w") as f:
                                for x, y in Q: f.write(f"{x} {y}\n")
                            break
        rec.update(directions=len(dirs), cap4_directions=good, new32=len(seen))
        print(json.dumps(rec), flush=True)

if __name__ == "__main__":
    main()
