"""Chirotope utilities: decoding symcnf.py models, .sig I/O, exact verification, canonical forms.

A chirotope on P points is stored as a dict {(a, b, c): s} over all a < b < c (0-based), s = +1
(counter-clockwise) or -1.  Exact checks use Python integers / Fractions only.
"""
import itertools
from fractions import Fraction


def parity_sort(t):
    a, b, c = int(t[0]), int(t[1]), int(t[2])   # int(): numpy bools would add as logical or
    inv = int(a > b) + int(a > c) + int(b > c)
    return tuple(sorted((a, b, c))), (-1 if inv & 1 else 1)


# ---------------------------------------------------------------- symcnf.py decoding
def sym_triple_map(P, m, has_center):
    """Replicates SymEncoding._triples of tools/symmetric/symcnf.py: returns {(a,b,c): (var, sign)}.
    Point index o*m + r is R^r applied to the representative of orbit o; the centre (if any) is the
    last index P-1 and is fixed by the rotation."""
    c = P - 1 if has_center else None
    norb = P - (1 if has_center else 0)

    def pi(i, k):
        if i == c:
            return i
        o, r = divmod(i, m)
        return o * m + (r + k) % m

    tv, nv = {}, 0
    for T in itertools.combinations(range(P), 3):
        if T in tv:
            continue
        nv += 1
        seen = {}
        for k in range(m):
            S, s = parity_sort((pi(T[0], k), pi(T[1], k), pi(T[2], k)))
            if S in seen:
                assert seen[S] == s
            else:
                seen[S] = s
        for S, s in seen.items():
            tv[S] = (nv, s)
    assert norb % m == 0
    return tv, nv


def decode_model(line, tv):
    lits = [int(x) for x in line.split()]
    vals = {abs(l): (l > 0) for l in lits}
    return {S: s * (1 if vals[v] else -1) for S, (v, s) in tv.items()}


def read_models(path, P, m, has_center):
    tv, nv = sym_triple_map(P, m, has_center)
    out = []
    for line in open(path):
        if line.strip():
            out.append(decode_model(line, tv))
    return out


def read_signotope_models(path, n):
    """Models of a signotope CNF in the tools/trackB/gen_cnf.py numbering: X(i,j,k), i<j<k (0-based
    here), is variable 1..C(n,3) in lexicographic order, true = counter-clockwise.  The file is
    either a SAT-solver output ("s SATISFIABLE" and "v" lines: one model) or one model per line
    (signed integers, optionally prefixed by "v").  Literals of other variables are ignored."""
    triples = list(itertools.combinations(range(n), 3))
    nx = len(triples)
    text = open(path).read()
    if any(l.startswith("s SATISFIABLE") for l in text.splitlines()):
        lits = []
        for l in text.splitlines():
            if l.startswith("v"):
                lits += [int(x) for x in l[1:].split()]
        blocks = [lits]
    else:
        blocks = []
        for l in text.splitlines():
            l = l.strip()
            if l.startswith("v"):
                l = l[1:]
            if l and not l.startswith(("c", "s")):
                blocks.append([int(x) for x in l.split()])
    out = []
    for lits in blocks:
        val = {abs(x): x > 0 for x in lits if 0 < abs(x) <= nx}
        if len(val) < nx:
            raise ValueError(f"model assigns only {len(val)} of the {nx} triple variables")
        out.append({t: (1 if val[v + 1] else -1) for v, t in enumerate(triples)})
    return out


def read_sig(path):
    chi = {}
    for line in open(path):
        p = line.split()
        if len(p) == 4:
            a, b, c, s = map(int, p)
            S, sg = parity_sort((a, b, c))
            chi[S] = sg * s
    return chi


def write_sig(chi, path):
    with open(path, "w") as f:
        for (a, b, c), s in sorted(chi.items()):
            f.write(f"{a} {b} {c} {s}\n")


def chi_get(chi, a, b, c):
    S, s = parity_sort((a, b, c))
    return s * chi[S]


# ---------------------------------------------------------------- exact geometry
def orient_exact(p, q, r):
    """sign-carrying exact determinant for integer or Fraction coordinates"""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def chirotope_of(points):
    """exact chirotope of a point list (ints/Fractions); raises if a triple is collinear"""
    n = len(points)
    chi = {}
    for a, b, c in itertools.combinations(range(n), 3):
        d = orient_exact(points[a], points[b], points[c])
        if d == 0:
            raise ValueError(f"collinear triple {a} {b} {c}")
        chi[(a, b, c)] = 1 if d > 0 else -1
    return chi


def verify_exact(points, chi):
    """Exact check that rational points realize chi: every listed triple has the required nonzero
    sign.  Returns (ok, n_mismatch, n_zero).  points: list of (Fraction|int, Fraction|int)."""
    pts = [(Fraction(x), Fraction(y)) for x, y in points]
    bad = zero = 0
    for (a, b, c), s in chi.items():
        d = orient_exact(pts[a], pts[b], pts[c])
        if d == 0:
            zero += 1
        elif (d > 0) != (s > 0):
            bad += 1
    n = len(pts)
    complete = len(chi) == n * (n - 1) * (n - 2) // 6
    return (bad == 0 and zero == 0 and complete), bad, zero


# ---------------------------------------------------------------- abstract structure
def hull_vertices(chi, n):
    """abstract extreme points: v is extreme iff i < j :<=> chi(v,i,j)=+1 is a strict total order
    (equivalently, every out-degree in that tournament is distinct).  Returns [(v, order)] where
    order lists the other points so that chi(v, order[p], order[q]) = +1 for p < q."""
    res = []
    for v in range(n):
        others = [i for i in range(n) if i != v]
        wins = {i: sum(1 for j in others if j != i and chi_get(chi, v, i, j) > 0) for i in others}
        if sorted(wins.values()) == list(range(n - 1)):
            order = sorted(others, key=lambda i: -wins[i])
            res.append((v, order))
    return res


def canonical_form(chi, n, mirror=True):
    """lexicographically least sign string over the labellings that start at an extreme point and
    list the others in angular order (for both orientations if mirror=True).  Two chirotopes get the
    same form iff they are isomorphic (relabelling, plus reflection if mirror)."""
    best = None
    for flip in ((1, -1) if mirror else (1,)):
        ch = chi if flip == 1 else {k: -s for k, s in chi.items()}
        for v, order in hull_vertices(ch, n):
            lab = [v] + order
            pos = {p: i for i, p in enumerate(lab)}
            s = []
            for a, b, c in itertools.combinations(range(n), 3):
                s.append('+' if chi_get(ch, lab[a], lab[b], lab[c]) > 0 else '-')
            s = "".join(s)
            if best is None or s < best:
                best = s
    return best


# ---------------------------------------------------------------- convex position (exact)
def largest_convex_subset(points):
    """Exact size of a largest subset in convex position (general position assumed).  Same DP as
    scripts/es_lower_bound_witness.py."""
    from functools import cmp_to_key
    best = min(len(points), 2)
    for p in points:
        above = [q for q in points if (q[1], q[0]) > (p[1], p[0])]
        q = sorted(above, key=cmp_to_key(lambda a, b: -1 if orient_exact(p, a, b) > 0 else 1))
        m = len(q)
        chain = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(i):
                value = 3
                for k in range(j):
                    if chain[k][j] and orient_exact(q[k], q[j], q[i]) > 0:
                        value = max(value, chain[k][j] + 1)
                chain[j][i] = value
                if orient_exact(q[j], q[i], p) > 0:
                    best = max(best, value)
    return best
