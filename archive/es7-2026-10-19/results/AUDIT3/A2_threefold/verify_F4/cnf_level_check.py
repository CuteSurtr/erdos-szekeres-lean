#!/usr/bin/env python3
"""F4 check 2: CNF-level test of the ACTUAL c3cnf.py chain CNF (the encoding behind the final
base CNF, gen_case.py 11 7 none imports C3a/c3cnf.py) on exact 3-fold symmetric point sets.

My own exact geometry in Q(sqrt3) (pairs of Fractions), my own normal form (frame, labels, sigma,
inv, B, chi', chi_S), my own Horn least-fixpoint evaluator over the clause list.  Only the
variable numbering is taken from the generator's --map output.

For each set: all non-gon clauses must hold under the true base assignment plus the least
fixpoint of the auxiliary variables; and the gon clauses must all hold  <=>  brute force finds
no convex k-subset.  The direction that UNSAT soundness needs is:
   no convex k-subset  =>  every gon clause holds (checked on every k-gon-free set below).
Usage: cnf_level_check.py CNF MAP SEED TRIALS SHAPES(comma list)
"""
import itertools
import json
import random
import sys
from fractions import Fraction as F


# ---- exact arithmetic in Q(sqrt 3): (a, b) = a + b sqrt3 ----
def add(x, y): return (x[0] + y[0], x[1] + y[1])
def sub(x, y): return (x[0] - y[0], x[1] - y[1])
def mul(x, y): return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
def inv(x):
    d = x[0] * x[0] - 3 * x[1] * x[1]
    assert d != 0
    return (x[0] / d, -x[1] / d)
def sgn(x):
    a, b = x
    sa = (a > 0) - (a < 0)
    sb = (b > 0) - (b < 0)
    if sb == 0: return sa
    if sa == 0: return sb
    if sa == sb: return sa
    t = a * a - 3 * b * b  # |a| vs sqrt3 |b|
    st = (t > 0) - (t < 0)
    return sa * st
def lt(x, y): return sgn(sub(y, x)) > 0
def Q(v): return (F(v), F(0))


def orient(p, q, r):
    return sgn(sub(mul(sub(q[0], p[0]), sub(r[1], p[1])), mul(sub(q[1], p[1]), sub(r[0], p[0]))))


H = F(1, 2)
def rot120(p):
    x, y = p
    # (-x/2 - (sqrt3/2) y,  (sqrt3/2) x - y/2)
    return (sub(mul((-H, F(0)), x), mul((F(0), H), y)), sub(mul((F(0), H), x), mul((H, F(0)), y)))


def base_points(rng, m, shape):
    pts = []
    for _ in range(m):
        if shape == "disk":
            while True:
                x, y = rng.randint(-1000, 1000), rng.randint(-1000, 1000)
                if 50 ** 2 < x * x + y * y <= 1000 ** 2: break
        elif shape == "ring":
            while True:
                x, y = rng.randint(-1000, 1000), rng.randint(-1000, 1000)
                if 800 ** 2 <= x * x + y * y <= 1000 ** 2: break
        elif shape == "cluster":
            x, y = 600 + rng.randint(-40, 40), 100 + rng.randint(-40, 40)
        elif shape == "strip":  # thin radial strip: few large convex subsets
            t = rng.randint(100, 1000)
            x, y = t + rng.randint(-15, 15), (t // 7) + rng.randint(-15, 15)
        else:
            raise ValueError(shape)
        pts.append((Q(x), Q(y)))
    return pts


def normal_form(S, m, u):
    """S: list of 3m exact points ordered as orbits (p, Rp, R^2p) so that index 3o+e has R-image
    3o+(e+1)%3.  u = integer direction of the y-axis l.  Returns None if a genericity check fails."""
    n = 3 * m
    u1, u2 = Q(u[0]), Q(u[1])
    fr = [(sub(mul(u2, p[0]), mul(u1, p[1])), add(mul(u1, p[0]), mul(u2, p[1]))) for p in S]
    if any(sgn(x) == 0 for x, _ in fr):
        return None
    Xp = [mul(y, inv(x)) for x, y in fr]
    Yp = [inv(x) for x, _ in fr]
    # distinct X' (no two points collinear with c) and distinct x (B is a total order)
    for i, j in itertools.combinations(range(n), 2):
        if sgn(sub(Xp[i], Xp[j])) == 0 or sgn(sub(fr[i][0], fr[j][0])) == 0:
            return None
    import functools
    order = sorted(range(n), key=functools.cmp_to_key(lambda i, j: sgn(sub(Xp[i], Xp[j]))))
    lab = {pt: L for L, pt in enumerate(order)}
    # identity 1: R(i) = i - m mod n on labels
    for o in range(m):
        for e in range(3):
            a, b = 3 * o + e, 3 * o + (e + 1) % 3
            assert lab[b] == (lab[a] - m) % n, "R(i) = i-m fails"
    P = [fr[pt] for pt in order]        # frame coordinates by label
    Sp = [(Xp[pt], Yp[pt]) for pt in order]
    sigma = [sgn(P[i][0]) < 0 for i in range(n)]
    return P, Sp, sigma


def true_assignment(P, Sp, sigma, mp):
    n = mp["n"]
    m = mp["m"]
    val = {}
    def put(lit, truth, what):
        v, t = abs(lit), (truth if lit > 0 else not truth)
        if v in val and val[v] != t:
            raise AssertionError("orbit-inconsistent " + what)
        val[v] = t
    chip = {}
    for i, j, k, lit in mp["C"]:
        s = orient(Sp[i], Sp[j], Sp[k]); assert s != 0
        put(lit, s > 0, "C")
    for r in range(m):
        assert sigma[r + m] == (not sigma[r]) and sigma[r + 2 * m] == sigma[r], "sigma orbit pattern"
        put(mp["s"][r], sigma[r], "s")
    for i, j, v in mp["inv"]:
        put(v, lt(Sp[j][1], Sp[i][1]), "inv")
    for i, j, v in mp["B"]:
        put(v, lt(P[i][0], P[j][0]), "B")
    for i, j, k, lit in mp["T"]:
        s = orient(P[i], P[j], P[k]); assert s != 0
        put(lit, s > 0, "T")
    return val


class CNF:
    def __init__(self, path, mp):
        self.cl = []
        with open(path) as f:
            for line in f:
                if line[0] in "pc":
                    continue
                xs = list(map(int, line.split()))
                assert xs[-1] == 0
                self.cl.append(xs[:-1])
        assert len(self.cl) == mp["clauses"]
        self.sec = []
        for name, st, cnt in mp["sections"]:
            self.sec += [name] * cnt
        assert len(self.sec) == len(self.cl)
        base = set()
        for key in ("C", "T"):
            for *_, lit in mp[key]: base.add(abs(lit))
        for v in mp["s"]: base.add(v)
        for key in ("inv", "B"):
            for *_, v in mp[key]: base.add(v)
        self.base = base
        # pre-split every clause into base literals and aux literals
        self.split = []
        for c in self.cl:
            b = [l for l in c if abs(l) in base]
            a = [l for l in c if abs(l) not in base]
            assert sum(1 for l in a if l > 0) <= 1, "non-Horn aux clause"
            self.split.append((b, a))

    def evaluate(self, val):
        isTrue = lambda l: val[abs(l)] == (l > 0)
        rules, goals, bad_base = [], [], []
        for idx, (b, a) in enumerate(self.split):
            if any(isTrue(l) for l in b):
                continue
            if not a:
                bad_base.append(idx)
                continue
            head = [l for l in a if l > 0]
            body = [-l for l in a if l < 0]
            if head:
                rules.append((body, head[0], idx))
            else:
                goals.append((body, idx))
        # least fixpoint (counter-based forward chaining)
        true = set()
        watch = {}
        cnt = []
        queue = []
        for r, (body, h, idx) in enumerate(rules):
            cnt.append(len(body))
            for v in body:
                watch.setdefault(v, []).append(r)
            if not body:
                queue.append(h)
        while queue:
            v = queue.pop()
            if v in true:
                continue
            true.add(v)
            for r in watch.get(v, ()):
                cnt[r] -= 1
                if cnt[r] == 0:
                    queue.append(rules[r][1])
        violated = [idx for body, idx in goals if all(v in true for v in body)]
        return bad_base, violated


def convex4_table(P):
    n = len(P)
    O = {}
    for t in itertools.permutations(range(n), 3):
        O[t] = orient(P[t[0]], P[t[1]], P[t[2]])
    def inside(d, a, b, c):
        return O[(a, b, d)] == O[(b, c, d)] == O[(c, a, d)]
    cv = {}
    for q in itertools.combinations(range(n), 4):
        cv[q] = not any(inside(q[i], *[q[j] for j in range(4) if j != i]) for i in range(4))
    return cv


def largest_convex_at_least(P, k):
    cv = convex4_table(P)
    for S in itertools.combinations(range(len(P)), k):
        if all(cv[q] for q in itertools.combinations(S, 4)):
            return True
    return False


def main():
    cnfpath, mappath, seed, trials, shapes = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5].split(",")
    mp = json.load(open(mappath))
    m, k, n = mp["m"], mp["k"], mp["n"]
    kcnf = k
    if len(sys.argv) > 6:  # mutation control: brute force with a different k than the CNF's
        k = int(sys.argv[6])
    assert mp["gon"] == "chain" and mp["sb"] and not mp["xsig"] and not mp["acy"]
    cnf = CNF(cnfpath, mp)
    rng = random.Random(seed)
    st = {"m": m, "k_cnf": kcnf, "k_bruteforce": k, "sets": 0, "kgon_free": 0, "with_kgon": 0, "negated_for_sb": 0,
          "fail_base": 0, "fail_sound": 0, "fail_complete": 0, "redraws": 0}
    while st["sets"] < trials:
        shape = rng.choice(shapes)
        bp = base_points(rng, m, shape)
        S = []
        for p in bp:
            S += [p, rot120(p), rot120(rot120(p))]
        if any(orient(*t) == 0 for t in itertools.combinations(S, 3)):
            st["redraws"] += 1; continue
        u = (rng.randint(-50, 50), rng.randint(-50, 50))
        if u == (0, 0):
            continue
        nf = normal_form(S, m, u)
        if nf is None:
            st["redraws"] += 1; continue
        P, Sp, sigma = nf
        if sigma[0]:  # C3a item 5: replace S by -S with the same l
            S = [((-p[0][0], -p[0][1]), (-p[1][0], -p[1][1])) for p in S]
            nf2 = normal_form(S, m, u)
            assert nf2 is not None
            P2, Sp2, sigma2 = nf2
            assert all(sgn(sub(Sp2[i][0], Sp[i][0])) == 0 for i in range(n)), "labels changed under -I"
            P, Sp, sigma = P2, Sp2, sigma2
            assert not sigma[0]
            st["negated_for_sb"] += 1
        val = true_assignment(P, Sp, sigma, mp)
        bad_base, violated = cnf.evaluate(val)
        real = largest_convex_at_least(P, k)
        st["sets"] += 1
        st["with_kgon" if real else "kgon_free"] += 1
        nongon_bad = [i for i in bad_base] + [i for i in violated if cnf.sec[i] != "gon"]
        if nongon_bad:
            st["fail_base"] += 1
            print("NON-GON CLAUSE FALSE", shape, [cnf.sec[i] for i in nongon_bad[:5]])
        gon_viol = [i for i in violated if cnf.sec[i] == "gon"]
        if gon_viol and not real:
            st["fail_sound"] += 1
            print("SOUNDNESS FAIL: gon clause false on a k-gon-free set", shape)
        if real and not gon_viol:
            st["fail_complete"] += 1
            print("COMPLETENESS FAIL: k-gon present but no gon clause false", shape)
    print(json.dumps(st))


if __name__ == "__main__":
    main()
