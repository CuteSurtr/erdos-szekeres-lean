#!/usr/bin/env python3
"""Independent brute-force validator: counts k-subsets in convex position by the
'no point inside a triangle of three others' criterion (general position), using
exact Python integers. Compares against `cgon count` and the repository's
largest_convex_subset DP."""
import itertools, random, subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, "..", "..", "..", "scripts"))
# Directory holding the compiled cgon binary (common.sh sets it; default: the ignored .cache/ build directory).
build = os.environ.get("BUILD_DIR") or os.path.join(
    here, "..", "..", "..", ".cache", "es8-lower-bound-search-2026-10-11", "anneal")
from es_lower_bound_witness import largest_convex_subset, orient

def general_position(pts):
    return len(set(pts)) == len(pts) and all(orient(a, b, c) != 0 for a, b, c in itertools.combinations(pts, 3))

def inside(p, a, b, c):
    s1, s2, s3 = orient(a, b, p), orient(b, c, p), orient(c, a, p)
    return (s1 > 0 and s2 > 0 and s3 > 0) or (s1 < 0 and s2 < 0 and s3 < 0)

def brute_counts(pts):
    n = len(pts)
    # emptiness[i] = set of triangles containing point i
    containing = {}
    for t in itertools.combinations(range(n), 3):
        containing[t] = [i for i in range(n) if i not in t and inside(pts[i], *(pts[j] for j in t))]
    res = {}
    for k in range(3, n + 1):
        cnt = 0
        for S in itertools.combinations(range(n), k):
            s = set(S)
            ok = True
            for t in itertools.combinations(S, 3):
                if any(i in s for i in containing[t]):
                    ok = False; break
            if ok: cnt += 1
        res[k] = cnt
        if cnt == 0: break
    return res

def cgon_counts(pts, K):
    inp = "".join(f"{x} {y}\n" for x, y in pts)
    out = subprocess.run([os.path.join(build, "cgon"), "count", str(K)], input=inp, capture_output=True, text=True, check=True).stdout
    d = {}
    for tok in out.split():
        if tok.startswith("c"): k, v = tok[1:].split("="); d[int(k)] = int(v)
        if tok.startswith("maxconvex="): d["max"] = int(tok.split("=")[1])
    return d

def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    ok = 0
    for t in range(trials):
        n = rng.randint(4, 11)
        R = rng.choice([8, 30, 1000, 10**6, 2**29])
        while True:
            pts = [(rng.randrange(-R, R), rng.randrange(-R, R)) for _ in range(n)]
            if general_position(pts): break
        b = brute_counts(pts)
        c = cgon_counts(pts, n)
        for k in range(3, n + 1):
            assert b.get(k, 0) == c.get(k, 0), (pts, k, b, c)
        bm = max([2] + [k for k, v in b.items() if v])
        assert bm == c["max"] == largest_convex_subset(pts), (pts, bm, c)
        ok += 1
    print(f"brute-force agreement on {ok} random sets (n=4..11, all k)")

if __name__ == "__main__":
    main()
