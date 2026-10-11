#!/usr/bin/env python3
"""Generate a family of 64-point stacking sets certified (by the bound recursion)
to have no convex octagon, realize them with exact integer coordinates, verify
them, and deduplicate by order type.

Trees are strings: leaf 'o', internal 'U(A,B)' / 'D(A,B)'.
  U(A,B): B translated right, then far up   (stack(+1, A, B) in the repo script)
  D(A,B): B translated right, then far down (stack(-1, A, B))
"""
import hashlib, json, os, random, sys, time
from collections import defaultdict
from functools import lru_cache
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, HERE)
import es_lower_bound_witness as W  # noqa: E402
from dp import build, combine  # noqa: E402

import numpy as np  # noqa: E402

BOUND = 1 << 27  # sat.c / verify.c load-time coordinate bound (strict)

# ---------------------------------------------------------------- trees

def parse(s):
    """Parse a tree string into nested tuples."""
    pos = 0

    def rec():
        nonlocal pos
        if s[pos] == 'o':
            pos += 1
            return 'o'
        d = s[pos]
        assert d in 'UD' and s[pos + 1] == '('
        pos += 2
        a = rec()
        assert s[pos] == ','
        pos += 1
        b = rec()
        assert s[pos] == ')'
        pos += 1
        return (d, a, b)
    t = rec()
    assert pos == len(s)
    return t


def tstr(t):
    return 'o' if t == 'o' else f'{t[0]}({tstr(t[1])},{tstr(t[2])})'


def bounds(t):
    """Bound recursion (n, cup, cap, convex) of a tree."""
    if t == 'o':
        return (1, 1, 1, 1)
    return combine(bounds(t[1]), bounds(t[2]), t[0])


def canon_block(p, q):
    """Repo construction S(k,l) = Up(S(k-1,l), S(k,l-1)) with k=p+1, l=q+1."""
    if p == 1 or q == 1:
        return 'o'
    return f'U({canon_block(p - 1, q)},{canon_block(p, q - 1)})'


def random_block(p, q, rng):
    """Cup/cap block with cup bound p, cap bound q, size C(p+q-2,p-1); each node Up or Down."""
    if p == 1 or q == 1:
        return 'o'
    if rng.random() < 0.5:
        return f'U({random_block(p - 1, q, rng)},{random_block(p, q - 1, rng)})'
    return f'D({random_block(p, q - 1, rng)},{random_block(p - 1, q, rng)})'


def witness_tree(n=8):
    """The exact tree of W.witness(n): left-associated Down chain of S(n-j, j+2)."""
    t = canon_block(n - 1, 1)
    for j in range(1, n - 1):
        t = f'D({t},{canon_block(n - j - 1, j + 1)})'
    return t


def chain_bracketings(blocks):
    """All binary bracketings (Down at every node) of a sequence of block trees."""
    @lru_cache(None)
    def rec(i, j):
        if i == j:
            return [blocks[i]]
        out = []
        for k in range(i, j):
            for a in rec(i, k):
                for b in rec(k + 1, j):
                    out.append(f'D({a},{b})')
        return out
    return rec(0, len(blocks) - 1)

# ---------------------------------------------------------------- DP state graph

COUNT, BY_N = build()
IDX = defaultdict(list)
for _s in COUNT:
    IDX[_s[0]].append(_s)
TOP = (64, 7, 7, 7)
_DEC = {}


def decomps(s):
    if s not in _DEC:
        out = []
        n = s[0]
        for na in range(1, n):
            for sa in IDX[na]:
                for sb in IDX[n - na]:
                    for d in 'UD':
                        if combine(sa, sb, d) == s:
                            out.append((d, sa, sb))
        _DEC[s] = out
    return _DEC[s]


def is_block(s):
    n, p, q, c = s
    return n == comb(p + q - 2, p - 1) and (n == 1 or c == p + q - 2)


def all_skeletons(s, leaf):
    """All trees above maximal blocks; `leaf(state)` gives the block tree."""
    memo = {}

    def rec(s):
        if s in memo:
            return memo[s]
        if is_block(s):
            r = [leaf(s)]
        else:
            r = []
            for d, a, b in decomps(s):
                for x in rec(a):
                    for y in rec(b):
                        r.append(f'{d}({x},{y})')
        memo[s] = r
        return r
    return rec(s)


def sample_tree(s, rng, mode):
    """mode 'tree': uniform over all certified trees; 'dec': uniform decomposition per node."""
    if s == (1, 1, 1, 1):
        return 'o'
    ds = decomps(s)
    if mode == 'tree':
        w = [COUNT[a] * COUNT[b] for _, a, b in ds]
        r = rng.randrange(sum(w))
        for (d, a, b), wi in zip(ds, w):
            if r < wi:
                break
            r -= wi
    else:
        d, a, b = rng.choice(ds)
    return f'{d}({sample_tree(a, rng, mode)},{sample_tree(b, rng, mode)})'

# ---------------------------------------------------------------- realization

def stack_int(sign, left, right):
    """Integer-only version of W.stack (identical output; floor via //)."""
    t = max(p[0] for p in left) - min(p[0] for p in right) + 1
    moved = [(x + t, y) for x, y in right]
    L = sorted(left)
    M = sorted(moved)
    best = 0
    for i in range(len(L)):
        ax, ay = L[i]
        for j in range(i + 1, len(L)):
            bx, by = L[j]
            dx, dy = bx - ax, by - ay
            assert dx > 0
            v = max((-sign * (dx * (cy - ay) - dy * (cx - ax))) // dx for cx, cy in M)
            if v > best:
                best = v
    for i in range(len(M)):
        bx, by = M[i]
        for j in range(i + 1, len(M)):
            b2x, b2y = M[j]
            dx, dy = b2x - bx, b2y - by
            assert dx > 0
            v = max((sign * ((bx - ax) * (b2y - ay) - (by - ay) * (b2x - ax))) // dx for ax, ay in L)
            if v > best:
                best = v
    m = best + 1
    return left + [(x, y + sign * m) for x, y in moved]


_REAL = {}


def realize(t):
    key = tstr(t) if not isinstance(t, str) else t
    if key in _REAL:
        return _REAL[key]
    tt = parse(key) if isinstance(t, str) else t
    if tt == 'o':
        r = [(0, 0)]
    else:
        r = stack_int(+1 if tt[0] == 'U' else -1, realize(tstr(tt[1])), realize(tstr(tt[2])))
    _REAL[key] = r
    return r

# ---------------------------------------------------------------- order types

_TRI = None


def orient_table(P):
    big = max(max(abs(x), abs(y)) for x, y in P) >= (1 << 30)
    dt = object if big else np.int64  # exact Python ints when int64 could overflow
    X = np.array([p[0] for p in P], dtype=dt)
    Y = np.array([p[1] for p in P], dtype=dt)
    if big:
        dx = X[None, :] - X[:, None]
        dy = Y[None, :] - Y[:, None]
        O = dx[:, :, None] * dy[:, None, :] - dy[:, :, None] * dx[:, None, :]
        return np.vectorize(lambda v: (v > 0) - (v < 0), otypes=[np.int8])(O)
    dx = X[None, :] - X[:, None]  # dx[a,b] = Xb - Xa
    dy = Y[None, :] - Y[:, None]
    # O[a,b,c] = dx[a,b]*dy[a,c] - dy[a,b]*dx[a,c]
    O = dx[:, :, None] * dy[:, None, :] - dy[:, :, None] * dx[:, None, :]
    return np.sign(O).astype(np.int8)


def tri_index(n):
    global _TRI
    if _TRI is None or _TRI[0] != n:
        i, j, k = [], [], []
        for a in range(n):
            for b in range(a + 1, n):
                for c in range(b + 1, n):
                    i.append(a); j.append(b); k.append(c)
        _TRI = (n, np.array(i), np.array(j), np.array(k))
    return _TRI[1:]


def xorder_key(P, O=None):
    """Sign vector in x-order, canonical under x->-x and y->-y (min of 4)."""
    n = len(P)
    order = sorted(range(n), key=lambda i: P[i][0])
    O = orient_table(P) if O is None else O
    I, J, K = tri_index(n)
    o = np.array(order)
    base = O[o[I], o[J], o[K]]
    rev = o[::-1]
    # x-mirror: orient'(a,b,c) = orient(rev a, rev b, rev c) (two sign flips cancel)
    xm = O[rev[I], rev[J], rev[K]]
    cands = [base, -base, xm, -xm]
    return min(hashlib.sha256((c + 1).astype(np.uint8).tobytes()).hexdigest() + '' for c in [cands[0]]) if False else \
        min(bytes((c + 1).astype(np.uint8)) for c in cands)


def order_type_key(P, O=None):
    """Canonical order type (up to relabeling and reflection): min over hull
    vertices h and orientation s of the sign vector in the labeling
    [h] + angular order around h."""
    n = len(P)
    O = orient_table(P) if O is None else O
    # hull vertices: h such that all others lie in an open half-plane through h,
    # i.e. some other point a has all remaining points on one side of line h-a
    hull = []
    for h in range(n):
        for a in range(n):
            if a == h:
                continue
            row = O[h, a]
            s = row[[x for x in range(n) if x not in (h, a)]]
            if np.all(s > 0) or np.all(s < 0):
                hull.append(h)
                break
    I, J, K = tri_index(n)
    best = None
    from functools import cmp_to_key
    for h in hull:
        others = [x for x in range(n) if x != h]
        for s in (1, -1):
            lab = [h] + sorted(others, key=cmp_to_key(lambda a, b: -1 if s * O[h, a, b] > 0 else 1))
            lab = np.array(lab)
            v = (s * O[lab[I], lab[J], lab[K]]).astype(np.int8)
            bts = bytes((v + 1).astype(np.uint8))
            if best is None or bts < best:
                best = bts
    return hashlib.sha256(best).hexdigest(), len(hull)

# ---------------------------------------------------------------- verification

def verify_set(P, run_dp=True):
    n = len(P)
    info = {'n': n}
    info['distinct_points'] = len(set(P)) == n
    info['distinct_x'] = len({x for x, _ in P}) == n
    info['max_abs_coord'] = max(max(abs(x), abs(y)) for x, y in P)
    info['within_2^27'] = info['max_abs_coord'] < BOUND
    O = orient_table(P)
    I, J, K = tri_index(n)
    info['general_position'] = bool(np.all(O[I, J, K] != 0))
    if run_dp:
        t0 = time.time()
        info['largest_convex_subset'] = W.largest_convex_subset(P)
        info['dp_seconds'] = round(time.time() - t0, 2)
    return info, O


if __name__ == '__main__':
    # self-test: witness_tree realizes exactly W.witness(8)
    t0 = time.time()
    P = realize(witness_tree(8))
    assert P == W.witness(8), 'witness_tree mismatch'
    print('witness_tree reproduces witness(8):', time.time() - t0, 's')
    print('bounds', bounds(parse(witness_tree(8))))
    info, O = verify_set(P)
    print(info)
    t0 = time.time()
    print('order type', order_type_key(P, O), time.time() - t0)
    t0 = time.time()
    print('xorder key len', len(xorder_key(P, O)), time.time() - t0)
