#!/usr/bin/env python3
"""Independent adversarial checker for zcnf.py (rot, m=2, --no-sb) + zlayers.py layer units.
Pure Python (no numpy). Only zlayers.layer_units / zlayers.profiles are imported from the code under test."""
import sys, os, json, random, itertools, functools

C = os.environ.get('C2C', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(C, '..', 'SYMZ'))
sys.path.insert(0, C)
import zlayers  # code under test

O = (0, 0)


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def sgn(x):
    return (x > 0) - (x < 0)


def neg(q):
    return (-q[0], -q[1])


def general_position(P):
    return all(cross(a, b, c) != 0 for a, b, c in itertools.combinations(P, 3))


def hull_ccw(P):
    pts = sorted(set(P))
    if len(pts) <= 2:
        return pts
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def layers_of(P):
    rest, L = list(P), []
    while rest:
        V = list(rest) if len(rest) <= 2 else hull_ccw(rest)
        L.append(V)
        s = set(V)
        rest = [q for q in rest if q not in s]
    return L


def normal_form(P, p00):
    """my own labelling: layers outermost first, p00 = (0,0), reps strictly left of O->p00, sorted by angle."""
    L = layers_of(P)
    assert p00 in L[0]
    order = []
    for V in L:
        reps = [q for q in V if q != p00 and cross(O, p00, q) > 0]
        reps.sort(key=functools.cmp_to_key(lambda a, b: -1 if cross(O, a, b) > 0 else (1 if cross(O, a, b) < 0 else 0)))
        if p00 in V:
            reps = [p00] + reps
        assert 2 * len(reps) == len(V), (len(reps), len(V))
        order.append(reps)
    prof = tuple(len(r) for r in order)
    X = []
    for reps in order:
        for q in reps:
            X.append(q)
            X.append(neg(q))
    X.append(O)
    return prof, X, L, order


def check_ccw_claim(L, order):
    """claim: layer with h >= 2 pairs has CCW vertex order r_1..r_h, -r_1..-r_h (cyclically)."""
    bad = []
    for li, (V, reps) in enumerate(zip(L, order)):
        if len(reps) < 2:
            continue
        seq = reps + [neg(r) for r in reps]
        H = hull_ccw(V)
        k = H.index(seq[0])
        rot = H[k:] + H[:k]
        if rot != seq:
            bad.append(li)
    return bad


def convex_set(pts):
    return len(pts) <= 3 or len(hull_ccw(pts)) == len(pts)


# ---------------------------------------------------------------- CNF model
class Model:
    def __init__(self, cnf, mapf):
        self.cnf, self.mapf = cnf, mapf
        info = json.load(open(mapf))
        assert info['kind'] == 'rot' and info['m'] == 2 and info['axis'] == 0
        self.info = info
        self.t, self.N, self.K, self.Z = info['t'], info['N'], info['K'], info['Z']
        assert self.N == 2 * self.t and self.Z == self.N
        self.X_vars = info['X_vars']
        self.triples = info['triples']
        self.tv = {(a, b, c): (v, s) for a, b, c, v, s in self.triples}
        with open(cnf, 'rb') as f:
            l1 = f.readline()
            l2 = f.readline() if l1.startswith(b'c') else l1
        _, _, nv, nc = l2.split()
        self.nv, self.nc = int(nv), int(nc)
        # independent reconstruction of the conv variable numbering
        N, K = self.N, self.K

        def canon(S):
            T = tuple(sorted(x ^ 1 for x in S))
            return min(S, T)
        self.canon = canon
        v = self.X_vars
        self.csets = {}
        self.vrange = {}
        for r in range(4, K):
            lst = []
            lo = v + 1
            for S in itertools.combinations(range(N), r):
                if canon(S) == S:
                    lst.append(S)
            v += len(lst)
            self.csets[r] = lst
            self.vrange[r] = (lo, v)
        assert v == self.nv, ("conv numbering mismatch", v, self.nv)
        assert len(self.triples) == (N + 1) * N * (N - 1) // 6 - self.t

    def truth(self, X):
        """X: coordinates indexed by label (X[Z] = O). Returns (set of true literal byte-strings, val dict for triple
        vars, conv values) with conv = actual convex position."""
        val = {}
        for a, b, c, v, s in self.triples:
            r = sgn(cross(X[a], X[b], X[c]))
            if r == 0:
                raise AssertionError(f"zero chirotope value on nonzero triple {(a, b, c)}")
            x = s * r
            if v in val:
                if val[v] != x:
                    raise AssertionError(f"identity violated by real set at var {v}, triple {(a, b, c)}")
            else:
                val[v] = x
        assert len(val) == self.X_vars
        # zero triples really zero
        for o in range(self.t):
            assert cross(X[self.Z], X[2 * o], X[2 * o + 1]) == 0
        N = self.N
        conv4 = {}
        for S in itertools.combinations(range(N), 4):
            conv4[S] = convex_set([X[i] for i in S])
        prev = conv4
        cval = {}
        lo, hi = self.vrange[4]
        for i, S in enumerate(self.csets[4]):
            cval[lo + i] = conv4[S]
        for r in range(5, self.K):
            # all r-sets (for next level) and canonical ones get variables
            cur = {}
            need_all = r + 1 < self.K
            it = itertools.combinations(range(N), r) if need_all else self.csets[r]
            for S in it:
                cur[S] = all(prev[S[:j] + S[j + 1:]] for j in range(r))
            lo, hi = self.vrange[r]
            for i, S in enumerate(self.csets[r]):
                cval[lo + i] = cur[S]
            prev = cur
        T = set()
        for v, x in val.items():
            T.add(str(v if x > 0 else -v).encode())
        for v, x in cval.items():
            T.add(str(v if x else -v).encode())
        assert len(T) == self.nv
        return T, val, cval

    def lit_true(self, T, l):
        return str(l).encode() in T

    def kshape(self, toks):
        lo, hi = self.vrange[self.K - 1]
        for tkn in toks:
            l = int(tkn)
            if l == 0:
                continue
            if l > 0 or not (lo <= -l <= hi):
                return False
        return True

    def eval_stream(self, Ts, keep=30):
        """stream the CNF once; for each truth set report #violated K-shaped, list of other violated clauses."""
        res = [{'k_viol': 0, 'other_viol': 0, 'other': [], 'k_clauses': []} for _ in Ts]
        n = 0
        with open(self.cnf, 'rb') as f:
            for line in f:
                if line[:1] in (b'c', b'p'):
                    continue
                toks = line.split()
                n += 1
                for i, T in enumerate(Ts):
                    if T.isdisjoint(toks):
                        if self.kshape(toks):
                            res[i]['k_viol'] += 1
                            if len(res[i]['k_clauses']) < 5000:
                                res[i]['k_clauses'].append([int(x) for x in toks[:-1]])
                        else:
                            res[i]['other_viol'] += 1
                            if len(res[i]['other']) < keep:
                                res[i]['other'].append(line.decode().strip())
        assert n == self.nc, ("clause count mismatch", n, self.nc)
        return res


def var_of_set(model):
    r = model.K - 1
    lo, _ = model.vrange[r]
    return {S: lo + i for i, S in enumerate(model.csets[r])}


def identify_kset(model, clause, vos=None):
    """find K-sets S (canonical) whose K-clause equals the given clause; returns list."""
    r = model.K - 1
    lo, hi = model.vrange[r]
    sets = [model.csets[r][-l - lo] for l in clause]
    want = sorted(clause, key=abs)
    out = []
    A = sets[0]
    for base in (A, tuple(sorted(x ^ 1 for x in A))):
        for y in range(model.N):
            if y in base:
                continue
            S = tuple(sorted(base + (y,)))
            if model.canon(S) != S:
                continue
            cl = sorted({-vos[model.canon(S[:j] + S[j + 1:])] for j in range(model.K)}, key=abs)
            if cl == want and S not in out:
                out.append(S)
    return out


# ---------------------------------------------------------------- layer units
def my_units_from_geometry(model, X, L):
    """units I expect from the docstring, built from the REAL hull order of the labelled set (not from labels)."""
    t, Z = model.t, model.Z
    lab = {X[i]: i for i in range(2 * t)}
    tv = model.tv

    def lit(a, b, c):
        S, s = zlayers.parity_sort((a, b, c))
        v, sg = tv[S]
        return s * sg * v
    u = set()
    # half-plane
    for o in range(1, t):
        u.add(lit(Z, 0, 2 * o))
    # within-layer angular order: reps of a layer = labels with even index in that layer
    for V in L:
        reps = sorted(lab[q] for q in V if lab[q] % 2 == 0)
        for i, j in itertools.combinations(reps, 2):
            u.add(lit(Z, i, j))
    # edges: from the real CCW hull
    for li, V in enumerate(L):
        if len(V) < 4:
            continue
        H = hull_ccw(V)
        deeper = [q for V2 in L[li + 1:] for q in V2]
        for k in range(len(H)):
            a, b = H[k], H[(k + 1) % len(H)]
            for x in H + deeper:
                if x not in (a, b):
                    u.add(lit(lab[a], lab[b], lab[x]))
    return u


def check_units(model, T, X, L, prof):
    us = zlayers.layer_units(model.tv, model.Z, model.t, prof, allow_any=True)
    false = [l for l in us if str(l).encode() not in T]
    mine = my_units_from_geometry(model, X, L)
    return us, false, set(us) == mine, len(set(us) ^ mine)


# ---------------------------------------------------------------- convex k-gon counting
def count_convex(P, k):
    total = 0
    for a in P:
        up = [p for p in P if (p[1], p[0]) > (a[1], a[0])]
        up.sort(key=functools.cmp_to_key(lambda p, q: -1 if cross(a, p, q) > 0 else 1))
        m = len(up)
        D = {}
        for j in range(m):
            for i in range(j):
                cnt = [0] * (k + 1)
                cnt[3] = 1
                for h in range(i):
                    prev = D.get((h, i))
                    if prev is not None and cross(up[h], up[i], up[j]) > 0:
                        for Lq in range(3, k):
                            if prev[Lq]:
                                cnt[Lq + 1] += prev[Lq]
                D[(i, j)] = cnt
        for (i, j), cnt in D.items():
            if cnt[k] and cross(up[i], up[j], a) > 0:
                total += cnt[k]
    return total


def max_convex(P, cap=12):
    best = min(len(P), 3)
    for k in range(4, min(len(P), cap) + 1):
        if count_convex(P, k):
            best = k
        else:
            break
    return best


# ---------------------------------------------------------------- generators
def gen_random(t, rng, box=60):
    while True:
        S, P = set(), []
        for _ in range(t):
            while True:
                q = (rng.randint(-box, box), rng.randint(-box, box))
                if q != O and q not in S:
                    break
            S.update([q, neg(q)])
            P += [q, neg(q)]
        if general_position(P):
            return P


def gen_nested(profile, rng, scale=10 ** 6, near=False, tries=4000):
    """layers = centrally symmetric polygons inscribed in random ellipses (points chosen by polar angle), nested;
    a last layer with 1 pair is a single antipodal pair. near=True: the outer layer has a vertex at polar angle phi0
    and every deeper layer has a vertex at polar angle phi0 + eps or phi0 + pi + eps with tiny eps of random sign."""
    import math
    for _ in range(tries):
        P = []
        s = scale
        ok = True
        phi0 = rng.uniform(0, 2 * math.pi)
        for li, h in enumerate(profile):
            a = s * rng.uniform(0.5, 1.0)
            b = s * rng.uniform(0.5, 1.0)
            rho = rng.uniform(0, math.pi)
            angs = [rng.uniform(0, math.pi) for _ in range(h)]
            if near:
                if li == 0:
                    angs[0] = phi0
                else:
                    eps = rng.choice([1e-3, 1e-4, 2e-5]) * rng.choice([1, -1])
                    angs[rng.randrange(h)] = phi0 + eps + (math.pi if rng.random() < 0.5 else 0.0)
            for th in angs:
                al = th - rho
                r = 1.0 / math.sqrt(math.cos(al) ** 2 / a ** 2 + math.sin(al) ** 2 / b ** 2)
                q = (int(round(r * math.cos(th))), int(round(r * math.sin(th))))
                if q == O:
                    ok = False
                P += [q, neg(q)]
            s = s * rng.uniform(0.12, 0.5)
            if s < 30:
                ok = False
        if not ok or len(set(P)) != len(P) or not general_position(P):
            continue
        L = layers_of(P)
        if tuple(len(V) // 2 for V in L) != tuple(profile):
            continue
        return P
    return None
