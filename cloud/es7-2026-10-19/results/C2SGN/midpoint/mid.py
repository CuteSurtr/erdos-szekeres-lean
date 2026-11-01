#!/usr/bin/env python3
"""Midpoint clauses for sgn.py --sym (experimental, 2026-10-30).

For a real set with p_{n+1-i} = -p_i (centre c at the origin): c is the midpoint of every pair {r, -r}, and p lies on
the line pq, so c and -p are on the same side of line pq. Hence if r and -r lie on the same side of line pq, so do c
and -p:   chi(p,q,r) = chi(p,q,-r) = s  ->  chi(p,q,-p) = s,
for non-antipodal p, q and a pair {r, -r} disjoint from {p, q, -p, -q}. (Equivalently: lines pq and (-p)(-q) are
parallel, so no point lies beyond both of them.)
usage: mid.py add BASE.cnf MAP.json OUT.cnf     base + midpoint clauses
       mid.py check [RESULTS]                   the clauses hold on random real symmetric sets and the known examples
                                                (RESULTS: the results directory, default ../..)
       mid.py viol MAP.json MODEL.out           number of midpoint clauses a CaDiCaL model violates"""
import itertools, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # sgn.py is one level up
from sgn import Enc


def mid_clauses(e):
    n = e.n; A = lambda x: n + 1 - x; out = set()
    for p, q in itertools.combinations(range(1, n + 1), 2):
        if q == A(p): continue
        m = e.chi(p, q, A(p))
        for r in range(1, n // 2 + 1):
            if r in (p, q, A(p), A(q)): continue
            a, b = e.chi(p, q, r), e.chi(p, q, A(r))
            out.add(tuple(sorted((-a, -b, m), key=abs))); out.add(tuple(sorted((a, b, -m), key=abs)))
    return sorted(out, key=lambda c: [abs(x) for x in c])


def enc_for(n, mapf=None):
    e = Enc(n, 3, True, False)
    if mapf:
        mp = json.load(open(mapf))
        assert mp["n"] == n and {tuple(t[:3]): t[3] for t in mp["triples"]} == e.ov, "map numbering differs"
    return e


def add(base, mapf, out):
    mp = json.load(open(mapf)); e = enc_for(mp["n"], mapf); cl = mid_clauses(e)
    with open(base) as f, open(out, "w") as g:
        for line in f:
            if line.startswith("p cnf"):
                _, _, nv, nc = line.split(); g.write(f"p cnf {nv} {int(nc) + len(cl)}\n")
            else:
                g.write(line)
        for c in cl: g.write(" ".join(map(str, c)) + " 0\n")
    print(json.dumps({"n": mp["n"], "mid_clauses": len(cl)}))


def assignment(P):
    """P sorted by x with P[n-1-i] = -P[i]; returns {canonical o variable: bool} for Enc(n, ..., sym=True)."""
    n = len(P); e = Enc(n, 3, True, False); val = {}
    det = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    for t, v in e.ov.items():
        i, j, k = t; d = det(P[i - 1], P[j - 1], P[k - 1]); assert d != 0
        val[v] = d > 0
    # the symmetry relation of the encoding must hold on the real set
    for i, j, k in itertools.combinations(range(1, n + 1), 3):
        l = e.o(i, j, k); d = det(P[i - 1], P[j - 1], P[k - 1]) > 0
        assert (val[abs(l)] if l > 0 else not val[abs(l)]) == d
    return e, val


def holds(cl, val):
    return all(any(val[abs(l)] if l > 0 else not val[abs(l)] for l in c) for c in cl)


def check(results=None):
    random.seed(20261030); bad = 0; tested = 0
    for trial in range(300):
        h = random.randint(4, 10); pts = set()
        while len(pts) < h:
            x, y = random.randint(-60, 60), random.randint(-60, 60)
            if x != 0 and (x, y) not in pts and (-x, -y) not in pts: pts.add((x, y))
        P = sorted(list(pts) + [(-x, -y) for x, y in pts])
        if len({p[0] for p in P}) < len(P): continue
        try:
            e, val = assignment(P)
        except AssertionError:
            continue                                    # collinear triple
        tested += 1; bad += not holds(mid_clauses(e), val)
    print(json.dumps({"random_sets": tested, "violations": bad}))
    R = results or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    for f in ["SYM2/sym7_32points.txt", "SYMMAX/c4_28points.txt"]:
        P = [tuple(map(int, l.split())) for l in open(os.path.join(R, f)) if l.strip()]
        P = sorted(((10**9 + 7) * x + y, y) for x, y in P)   # orientation-preserving linear map: distinct x, same symmetry
        e, val = assignment(P)
        print(json.dumps({"set": f, "n": len(P), "mid_clauses_hold": holds(mid_clauses(e), val)}))


def viol(mapf, model):
    mp = json.load(open(mapf)); e = enc_for(mp["n"], mapf); val = {}
    for line in open(model):
        if line.startswith("v "):
            for x in map(int, line.split()[1:]):
                if x: val[abs(x)] = x > 0
    cl = mid_clauses(e); v = sum(1 for c in cl if not any(val[abs(l)] if l > 0 else not val[abs(l)] for l in c))
    print(json.dumps({"mid_clauses": len(cl), "violated": v}))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "add": add(*sys.argv[2:5])
    elif cmd == "check": check(*sys.argv[2:3])
    elif cmd == "viol": viol(*sys.argv[2:4])
