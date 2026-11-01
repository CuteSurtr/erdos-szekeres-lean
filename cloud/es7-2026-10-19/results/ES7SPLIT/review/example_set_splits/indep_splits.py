#!/usr/bin/env python3
"""Independent re-check of the z-split claims (written from scratch; does not import tools/ of this result).

Definition (split_theorem.md, Def. 1): a partition S = A u B (both nonempty) is a z-split, z a finite point
outside conv(S) or a direction d (point at infinity), if
  (S1) for all distinct a, a' in A and b in B:  b lies strictly on z's side of line aa';
  (S2) for all distinct b, b' in B and a in A:  a lies strictly on the side of bb' NOT containing z.
Nontrivial: |A|, |B| >= 2.

Method (complete, does NOT use Lemma 4' or any linear-separability argument):
  necessary condition ("one-sidedness"): for each pair in A, all of B strictly on one side of its line; for each
  pair in B, all of A strictly on one side.  These are 3- and 4-literal clauses over v_p (p in A).  All models with
  |A|, |B| >= 2 are enumerated with CaDiCaL plus blocking clauses.  For each model a witness z is sought and then
  verified with exact integer/rational arithmetic; z-cap/cup sizes are computed by brute force over subsets.
"""
import sys, os, subprocess, itertools, json
from fractions import Fraction

CADICAL = os.environ.get("CADICAL", "cadical")  # CaDiCaL binary (3.0.1 was used)


def read_points(fn):
    P = []
    with open(fn) as f:
        for line in f:
            t = line.split()
            if len(t) >= 2:
                P.append((int(t[0]), int(t[1])))
    return P


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sgn(x):
    return (x > 0) - (x < 0)


def det3(r0, r1, r2):
    return (r0[0] * (r1[1] * r2[2] - r1[2] * r2[1])
            - r0[1] * (r1[0] * r2[2] - r1[2] * r2[0])
            + r0[2] * (r1[0] * r2[1] - r1[1] * r2[0]))


def orient_h(a, b, z):
    """det[[ax,ay,1],[bx,by,1],[z1,z2,z3]] : = orient(a,b,z) if z3 = 1; = det(b-a, d) if z = (d, 0)."""
    return det3((a[0], a[1], 1), (b[0], b[1], 1), z)


def general_position(P):
    if len(set(P)) != len(P):
        return False
    return all(orient(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))


# ---------------------------------------------------------------- SAT enumeration of one-sided partitions
def build_clauses(P):
    n = len(P)
    cl = []
    for p, q in itertools.combinations(range(n), 2):
        pos, neg, zero = [], [], []
        for r in range(n):
            if r in (p, q):
                continue
            s = sgn(orient(P[p], P[q], P[r]))
            (pos if s > 0 else neg if s < 0 else zero).append(r)
        vp, vq = p + 1, q + 1
        for r in zero:  # collinear point: forbidden on the other side in both (S1) and (S2)
            cl.append([-vp, -vq, r + 1])
            cl.append([vp, vq, -(r + 1)])
        for r in pos:
            for s in neg:
                cl.append([-vp, -vq, r + 1, s + 1])      # (S1) one-sidedness
                cl.append([vp, vq, -(r + 1), -(s + 1)])  # (S2) one-sidedness
    for p in range(n):
        cl.append([q + 1 for q in range(n) if q != p])    # |A| >= 2
        cl.append([-(q + 1) for q in range(n) if q != p]) # |B| >= 2
    return cl


def enumerate_models(P, workdir, tag, limit=100000):
    n = len(P)
    base = build_clauses(P)
    blocks = []
    models = []
    while True:
        fn = os.path.join(workdir, f"{tag}.cnf")
        with open(fn, "w") as f:
            f.write(f"p cnf {n} {len(base) + len(blocks)}\n")
            for c in base:
                f.write(" ".join(map(str, c)) + " 0\n")
            for c in blocks:
                f.write(" ".join(map(str, c)) + " 0\n")
        out = subprocess.run([CADICAL, "-q", fn], capture_output=True, text=True)
        status = None
        vals = {}
        for line in out.stdout.splitlines():
            if line.startswith("s "):
                status = line[2:].strip()
            elif line.startswith("v "):
                for t in line[2:].split():
                    k = int(t)
                    if k != 0:
                        vals[abs(k)] = k > 0
        if status == "UNSATISFIABLE":
            break
        assert status == "SATISFIABLE", (status, out.stdout[-500:], out.stderr[-500:])
        A = frozenset(i for i in range(n) if vals.get(i + 1, False))
        B = frozenset(range(n)) - A
        models.append((A, B))
        blocks.append([-(i + 1) if (i in A) else (i + 1) for i in range(n)])
        if len(models) >= limit:
            break
    os.remove(os.path.join(workdir, f"{tag}.cnf"))
    return models, len(base)


# ---------------------------------------------------------------- independent pure-python one-sided check
def one_sided(P, A, B):
    for X, Y in ((A, B), (B, A)):
        for p, q in itertools.combinations(sorted(X), 2):
            ss = {sgn(orient(P[p], P[q], P[r])) for r in Y}
            if len(ss) != 1 or 0 in ss:
                return False
    return True


# ---------------------------------------------------------------- exact verification of a witness z
def in_closed_hull(P, z):
    """z = (x, y) Fractions; True iff z lies in conv(P) (closed), via Caratheodory over triangles/segments."""
    zx, zy = z
    def o(a, b):
        return (b[0] - a[0]) * (zy - a[1]) - (b[1] - a[1]) * (zx - a[0])
    for a, b, c in itertools.combinations(P, 3):
        s = sgn(orient(a, b, c))
        if s == 0:
            continue
        if sgn(o(a, b)) * s >= 0 and sgn(o(b, c)) * s >= 0 and sgn(o(c, a)) * s >= 0:
            return True
    return False


def verify_split(P, A, B, z):
    """z = (z1, z2, z3) with z3 in {0, 1} (Fractions allowed).  Exact check of (S1), (S2), z outside S."""
    z = tuple(Fraction(v) for v in z)
    if z[2] == 0:
        if z[0] == 0 and z[1] == 0:
            return False, "zero direction"
    else:
        assert z[2] == 1
        if in_closed_hull(P, (z[0], z[1])):
            return False, "z in conv(S)"
    for a, a2 in itertools.combinations(sorted(A), 2):
        sz = sgn(orient_h(P[a], P[a2], z))
        if sz == 0:
            return False, "z on an A-line"
        for b in B:
            if sgn(orient(P[a], P[a2], P[b])) != sz:
                return False, f"S1 fails at {a},{a2},{b}"
    for b, b2 in itertools.combinations(sorted(B), 2):
        sz = sgn(orient_h(P[b], P[b2], z))
        if sz == 0:
            return False, "z on a B-line"
        for a in A:
            if sgn(orient(P[b], P[b2], P[a])) != -sz:
                return False, f"S2 fails at {b},{b2},{a}"
    return True, "ok"


def lp_witness(P, A, B):
    """Float LP for z (any feasible), then rationalised; returns list of candidate exact z's."""
    import numpy as np
    from scipy.optimize import linprog
    rows = []
    for a, a2 in itertools.combinations(sorted(A), 2):
        s = sgn(orient(P[a], P[a2], P[next(iter(B))]))
        pa, pb = P[a], P[a2]
        # orient_h(pa, pb, z) = z1 (ay - by) + z2 (bx - ax) + z3 (ax by - ay bx)
        coef = (pa[1] - pb[1], pb[0] - pa[0], pa[0] * pb[1] - pa[1] * pb[0])
        rows.append(tuple(s * c for c in coef))
    for b, b2 in itertools.combinations(sorted(B), 2):
        s = sgn(orient(P[b], P[b2], P[next(iter(A))]))
        pa, pb = P[b], P[b2]
        coef = (pa[1] - pb[1], pb[0] - pa[0], pa[0] * pb[1] - pa[1] * pb[0])
        rows.append(tuple(-s * c for c in coef))
    # sanity of my coefficient formula against orient_h
    for r_test in [(3, -7, 1), (2, 5, 0)]:
        pa, pb = P[0], P[1]
        coef = (pa[1] - pb[1], pb[0] - pa[0], pa[0] * pb[1] - pa[1] * pb[0])
        assert sum(c * t for c, t in zip(coef, r_test)) == orient_h(pa, pb, r_test)
    cands = []
    # directions: z3 = 0 ; maximise margin t subject to r . (d1, d2, 0) >= t, |d_i| <= 1
    M = np.array(rows, dtype=float)
    nrm = np.linalg.norm(M, axis=1)
    Mn = M / nrm[:, None]
    for fixz3 in (0.0, 1.0):
        # variables d1, d2, t  (z3 fixed); maximise t s.t. Mn[:, :2] d + Mn[:, 2] z3 >= t
        c = [0, 0, -1]
        Aub = np.hstack([-Mn[:, :2], np.ones((len(rows), 1))])
        bub = Mn[:, 2] * fixz3
        bnd = [(-1, 1), (-1, 1), (None, None)] if fixz3 == 0 else [(-1e7, 1e7), (-1e7, 1e7), (None, None)]
        res = linprog(c, A_ub=Aub, b_ub=bub, bounds=bnd, method="highs")
        if res.status == 0 and res.x[2] > 0:
            for scale in (10 ** 3, 10 ** 6, 10 ** 9, 10 ** 12):
                cands.append((Fraction(round(res.x[0] * scale), scale), Fraction(round(res.x[1] * scale), scale),
                              Fraction(int(fixz3))))
    return cands


# ---------------------------------------------------------------- brute-force z-caps / z-cups
def z_sort(P, idx, z):
    import functools
    def cmp(i, j):
        v = orient_h(P[i], P[j], z)
        assert v != 0
        return -1 if v < 0 else 1
    return sorted(idx, key=functools.cmp_to_key(cmp))


def is_zchain(P, seq, z, kind):
    """seq z-sorted. kind 'cup': middle on z's side of chord; 'cap': middle on the other side (all triples)."""
    for i, j, k in itertools.combinations(range(len(seq)), 3):
        sz = sgn(orient_h(P[seq[i]], P[seq[k]], z))
        sq = sgn(orient(P[seq[i]], P[seq[k]], P[seq[j]]))
        assert sz != 0 and sq != 0
        if kind == "cup" and sq != sz:
            return False
        if kind == "cap" and sq != -sz:
            return False
    return True


def check_transitive_order(P, idx, z):
    s = z_sort(P, idx, z)
    for i, j in itertools.combinations(range(len(s)), 2):
        if not orient_h(P[s[i]], P[s[j]], z) < 0:
            return False
    return True


def brute_longest(P, idx, z, kind):
    idx = sorted(idx)
    assert check_transitive_order(P, idx, z)
    best = min(2, len(idx))
    m = 3
    while m <= len(idx):
        found = False
        for sub in itertools.combinations(idx, m):
            if is_zchain(P, z_sort(P, list(sub), z), z, kind):
                found = True
                break
        if not found:
            break   # no m-chain => no larger chain (subsets of chains are chains)
        best = m
        m += 1
    return best


def zfree_longest(P, X, Y, role, kind):
    """z-free definition: in a split, sgn orient_h(x, x', z) = sgn orient(x, x', y) for any y in Y if X = A
    (role 'upper'), and = -sgn orient(x, x', y) if X = B (role 'lower').  Brute force using that sign."""
    y0 = next(iter(Y))
    f = 1 if role == "upper" else -1
    import functools
    def zs(i, j):
        return f * sgn(orient(P[i], P[j], P[y0]))
    def cmp(i, j):
        return -1 if zs(i, j) < 0 else 1
    idx = sorted(X)
    best = min(2, len(idx))
    m = 3
    while m <= len(idx):
        found = False
        for sub in itertools.combinations(idx, m):
            seq = sorted(sub, key=functools.cmp_to_key(cmp))
            ok = True
            for i, j, k in itertools.combinations(range(m), 3):
                s_side = zs(seq[i], seq[k])
                s_mid = sgn(orient(P[seq[i]], P[seq[k]], P[seq[j]]))
                if (kind == "cup" and s_mid != s_side) or (kind == "cap" and s_mid != -s_side):
                    ok = False
                    break
            if ok:
                found = True
                break
        if not found:
            break
        best = m
        m += 1
    return best


def hull_size(P):
    # extreme points: p is extreme iff p is in no closed triangle of three other points
    cnt = 0
    for i, p in enumerate(P):
        others = [q for j, q in enumerate(P) if j != i]
        inside = False
        for a, b, c in itertools.combinations(others, 3):
            s = sgn(orient(a, b, c))
            if sgn(orient(a, b, p)) * s >= 0 and sgn(orient(b, c, p)) * s >= 0 and sgn(orient(c, a, p)) * s >= 0:
                inside = True
                break
        if not inside:
            cnt += 1
    return cnt


def main():
    workdir = os.path.dirname(os.path.abspath(__file__))
    results = {}
    for fn in sys.argv[1:]:
        tag = os.path.basename(fn).replace(".txt", "")
        P = read_points(fn)
        n = len(P)
        gp = general_position(P)
        h = hull_size(P)
        models, ncl = enumerate_models(P, workdir, tag)
        rec = dict(n=n, general_position=gp, hull=h, clauses=ncl, one_sided_models=len(models), splits=[])
        for A, B in models:
            assert one_sided(P, A, B)
            # candidate witnesses: the two vertical directions, then LP-derived ones
            cands = [(0, -1, 0), (0, 1, 0)] + lp_witness(P, A, B)
            wit = None
            for z in cands:
                ok, why = verify_split(P, A, B, z)
                if ok:
                    wit = z
                    break
            entry = dict(A=sorted(A), B=sorted(B), sizes=(len(A), len(B)))
            if wit is None:
                entry["witness"] = None
            else:
                wz = tuple(str(Fraction(v)) for v in wit)
                capA = brute_longest(P, A, wit, "cap")
                cupB = brute_longest(P, B, wit, "cup")
                cupA = brute_longest(P, A, wit, "cup")
                capB = brute_longest(P, B, wit, "cap")
                capA2 = zfree_longest(P, A, B, "upper", "cap")
                cupB2 = zfree_longest(P, B, A, "lower", "cup")
                # also try every other verified candidate to confirm z-independence of the type
                others = []
                for z in cands:
                    if z == wit:
                        continue
                    if verify_split(P, A, B, z)[0]:
                        others.append((tuple(str(Fraction(v)) for v in z),
                                       brute_longest(P, A, z, "cap"), brute_longest(P, B, z, "cup")))
                        if len(others) >= 2:
                            break
                entry.update(witness=wz, capA=capA, cupB=cupB, cupA=cupA, capB=capB,
                             capA_zfree=capA2, cupB_zfree=cupB2, other_witnesses=others)
            rec["splits"].append(entry)
        results[tag] = rec
        print(tag, json.dumps({k: v for k, v in rec.items() if k != "splits"}), flush=True)
        for e in rec["splits"]:
            print("   ", json.dumps(e), flush=True)
    with open(os.path.join(workdir, "indep_results.json"), "w") as f:
        json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()
