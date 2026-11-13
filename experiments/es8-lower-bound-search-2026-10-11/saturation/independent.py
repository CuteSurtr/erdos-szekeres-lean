#!/usr/bin/env python3
"""Independent cross-check of `sat sat` on small instances.

Different face enumeration: every face has an edge of the arrangement on its
boundary, so we take the midpoint m of every edge (and a point beyond each
end of every line) and the symbolic points m +- eps * normal.  Faces are
deduplicated by exact sign vectors (Fractions only) and counted; the count
is compared with Euler's relation computed from exact vertex multiplicities.
For each face, existence of a convex K-gon through p is decided by brute
force over (K-1)-subsets of S with the criterion "no point inside a triangle
of three others".

usage: independent.py pointsfile K [badfile_from_sat]
prints JSON; exit code 1 on any disagreement with the C program's bad file.
"""
import json, sys
from fractions import Fraction
from itertools import combinations


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sgn(x):
    return (x > 0) - (x < 0)


def main():
    S = [tuple(map(int, l.split())) for l in open(sys.argv[1]) if l.strip()]
    K = int(sys.argv[2])
    N = len(S)
    lines = [(a, b) for a in range(N) for b in range(a + 1, N)]
    L = len(lines)
    lidx = {ab: i for i, ab in enumerate(lines)}
    assert all(orient(S[a], S[b], S[c]) != 0 for a, b, c in combinations(range(N), 3))

    def intersect(l1, l2):
        (a, b), (c, d) = lines[l1], lines[l2]
        A, B, C, Dp = S[a], S[b], S[c], S[d]
        u = (B[0] - A[0], B[1] - A[1]); w = (Dp[0] - C[0], Dp[1] - C[1])
        den = u[0] * w[1] - u[1] * w[0]
        if den == 0:
            return None
        t = Fraction((C[0] - A[0]) * w[1] - (C[1] - A[1]) * w[0], den)
        return t, (A[0] + t * u[0], A[1] + t * u[1])

    # Euler count from exact vertices
    vert = {}
    for l1 in range(L):
        for l2 in range(l1 + 1, L):
            r = intersect(l1, l2)
            if r is None:
                continue
            vert.setdefault(r[1], set()).update((l1, l2))
    F_euler = 1 + L + sum(len(s) - 1 for s in vert.values())

    faces = {}
    for l in range(L):
        a, b = lines[l]
        A, B = S[a], S[b]
        ts = sorted({r[0] for l2 in range(L) if l2 != l for r in [intersect(l, l2)] if r is not None})
        samples = [ts[0] - 1, ts[-1] + 1] + [(ts[i] + ts[i + 1]) / 2 for i in range(len(ts) - 1)]
        nv = (-(B[1] - A[1]), B[0] - A[0])
        for t in samples:
            m = (A[0] + t * (B[0] - A[0]), A[1] + t * (B[1] - A[1]))
            base = []
            for l2, (c, d) in enumerate(lines):
                o = orient(S[c], S[d], m)
                if l2 != l:
                    assert o != 0, "edge midpoint on a second line"
                else:
                    assert o == 0
                base.append(sgn(o))
            for s in (1, -1):
                vec = list(base)
                c, d = lines[l]
                e = (S[d][0] - S[c][0]) * s * nv[1] - (S[d][1] - S[c][1]) * s * nv[0]
                assert e != 0
                vec[l] = sgn(e)
                faces.setdefault(tuple(vec), None)

    def has_kgon(vec):
        def O(i, j, k):  # orientation with index -1 = p
            if -1 not in (i, j, k):
                return sgn(orient(S[i], S[j], S[k]))
            while k != -1:  # rotate cyclically so that p is last
                i, j, k = j, k, i
            return vec[lidx[(i, j)]] if i < j else -vec[lidx[(j, i)]]

        def inside(x, a, b, c):
            s1, s2, s3 = O(a, b, x), O(b, c, x), O(c, a, x)
            return s1 == s2 == s3

        for sub in combinations(range(N), K - 1):
            pts = list(sub) + [-1]
            ok = True
            for x in pts:
                others = [y for y in pts if y != x]
                if any(inside(x, a, b, c) for a, b, c in combinations(others, 3)):
                    ok = False
                    break
            if ok:
                return True
        return False

    bad = set()
    for vec in faces:
        if not has_kgon(vec):
            bad.add("".join("+" if s > 0 else "-" for s in vec))
    res = {"N": N, "K": K, "lines": L, "faces_euler": F_euler, "faces_enumerated": len(faces),
           "bad_faces": len(bad)}
    status = 0
    if len(faces) != F_euler:
        status = 1
    if len(sys.argv) > 3:
        cbad = set()
        for line in open(sys.argv[3]):
            parts = line.split()
            if parts:
                cbad.add(parts[-1])
        res["c_bad_faces"] = len(cbad)
        res["bad_sets_equal"] = (cbad == bad)
        if cbad != bad:
            status = 1
    print(json.dumps(res))
    return status


if __name__ == "__main__":
    sys.exit(main())
