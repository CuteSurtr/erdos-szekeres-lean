#!/usr/bin/env python3
"""Exact check of the 7-fold 64-point octagon-free sets against encoder B's 9-layer formula (gen_b2.py 7 8 9).

usage: python3 -I k8exact.py [--dump DIR] CNF SET.pts [SET.pts ...]      (CNF.map.json must sit next to CNF)
Writes one JSON object per line to stdout.  Python standard library only.  With --dump, the full assignment of
each case is written to DIR/<set>.<case>.assign (one literal per variable, DIMACS style) for satcheck.py.

Arithmetic (exact computation).
  A point is w = (w_0, ..., w_6), meaning sum_j w_j zeta^j with zeta = exp(2 pi i/7) (the format of the set files).
  Sums, products and complex conjugation are done in Z[zeta] (integer vectors, multiplication mod x^7 - 1;
  equality after subtracting w_6 * (1, ..., 1), since 1 + zeta + ... + zeta^6 = 0).
  Every sign that is needed is the sign of Im(a) or Re(a) for some a in Z[zeta]:
    a - conj(a)     = (zeta - zeta^-1) * (d1 + d2 c + d3 (c^2 - 1)),   d_j = a_j - a_{7-j},
    2 Re(a)         = 2 a_0 - 2 s2 + s3 + (s1 - s3) c + (s2 - s3) c^2,  s_j = a_j + a_{7-j},
  with c = zeta + zeta^-1 = 2 cos(2 pi/7) and zeta - zeta^-1 = 2i sin(2 pi/7), sin(2 pi/7) > 0.  These identities
  hold in Z[zeta] and are re-verified exactly at start-up (`identities`).  So sign(Im a) = sign(P(c)) and
  sign(Re a) = sign(Q(c)) for integer polynomials P, Q of degree <= 2.
  c is the unique root in [1, 2] of f(x) = x^3 + x^2 - 2x - 1: f(c) = 0 (verified in Z[zeta]); 0 < 2 pi/7 < pi/3
  gives 1 < c < 2; f' = 3x^2 + 2x - 2 > 0 on [1, 2].  An isolating interval [L, L+1]/2^N is found by integer
  bisection with exact checks f(L/2^N) < 0 < f((L+1)/2^N).  The sign of q0 + q1 c + q2 c^2 is read off an exact
  integer interval enclosure over that interval (each term is monotone in c > 0); if the enclosure contains 0,
  N is doubled.  This terminates: f is irreducible over Q (no rational root), so 1, c, c^2 are linearly independent
  and q0 + q1 c + q2 c^2 = 0 only for q = 0, which is reported as sign 0 (a degenerate configuration).
Encoder conventions (C6UPPER/encb/gen_b2.py, odd m): layer 0 is outermost; point (i, k) has angle theta_i + 2 pi k/7
  with theta_0 = 0 and theta_i in [0, 2 pi/7); psi_i = theta_i mod pi/7; H(i) = [theta_i < pi/7];
  Y(i, j) = [psi_i < psi_j]; an orbit variable is true iff orient(c0, c1, c2) > 0 for its canonical triple c.
  e^{i pi/7} = -zeta^4 lies in Z[zeta], so every phase comparison is an exact sign of an Im.
Chain variables are given their least model under the fixed geometric assignment (the chain clauses are Horn in
them); the full assignment is then evaluated clause by clause.
Cross-checks: rotation invariance of all orientations (exact); phases independent of the choice of the layer-0
point (exact); all 41,664 orientation signs of the 64-point set against PRIMEFOLD/check64/z7exact.py (separately
written code for the same identities); a 200-digit Decimal recomputation of orientations, H and Y (evidence only).
"""
import collections
import decimal
import hashlib
import importlib.util
import itertools
import json
import math
import random
import resource
import sys
import time
from functools import cmp_to_key
from pathlib import Path

M = 7
HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent
START = time.monotonic()
STATS = collections.Counter()

# ---------------------------------------------------------------- Z[zeta_7]
ZERO = (0,) * 7


def norm(w):
    return tuple(x - w[6] for x in w)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, b):
    c = [0] * 7
    for j, aj in enumerate(a):
        if aj:
            for k, bk in enumerate(b):
                if bk:
                    c[(j + k) % 7] += aj * bk
    return tuple(c)


def conj(a):
    return tuple(a[(-j) % 7] for j in range(7))


def zpow(k):
    v = [0] * 7
    v[k % 7] = 1
    return tuple(v)


def rot(a, k):
    """multiplication by zeta^k"""
    return tuple(a[(j - k) % 7] for j in range(7))


def const(n):
    return (n, 0, 0, 0, 0, 0, 0)


ZETA = zpow(1)
OMEGA = tuple(-x for x in zpow(4))          # e^{i pi/7} = -zeta^4
OMEGA_BAR = conj(OMEGA)                      # -zeta^3
CC = norm(tuple(x + y for x, y in zip(zpow(1), zpow(6))))   # c = 2 cos(2 pi/7)


def identities():
    """Exact identities in Z[zeta] behind the sign reductions."""
    c, c2 = CC, mul(CC, CC)
    c3 = mul(c2, c)
    add = lambda *xs: tuple(sum(t) for t in zip(*xs))
    neg = lambda a: tuple(-x for x in a)
    checks = {
        'f(c)=c^3+c^2-2c-1=0': add(c3, c2, neg(add(c, c)), const(-1)),
        'zeta^2-zeta^-2=(zeta-zeta^-1)c': sub(sub(zpow(2), zpow(5)), mul(sub(zpow(1), zpow(6)), c)),
        'zeta^3-zeta^-3=(zeta-zeta^-1)(c^2-1)': sub(sub(zpow(3), zpow(4)), mul(sub(zpow(1), zpow(6)), add(c2, const(-1)))),
        'zeta^2+zeta^-2=c^2-2': sub(add(zpow(2), zpow(5)), add(c2, const(-2))),
        'zeta^3+zeta^-3=-c^2-c+1': sub(add(zpow(3), zpow(4)), add(neg(c2), neg(c), const(1))),
        'e^{i pi/7}=-zeta^4: omega^7=-1': add(mul(mul(mul(OMEGA, OMEGA), mul(OMEGA, OMEGA)), mul(mul(OMEGA, OMEGA), OMEGA)), const(1)),
        'omega^2=zeta': sub(mul(OMEGA, OMEGA), ZETA),
    }
    bad = [k for k, v in checks.items() if norm(v) != ZERO]
    assert not bad, bad
    # omega^2 = zeta, so omega = +-e^{i pi/7}; Re(omega) > 0 and Im(omega) > 0 select e^{i pi/7}.  (Both signs
    # follow from the identities above and sin(2 pi/7) > 0, which is elementary since 0 < 2 pi/7 < pi.)
    assert sign_re(OMEGA) > 0 and sign_im(OMEGA) > 0
    checks['Re(omega)>0, Im(omega)>0'] = ZERO
    # Consistency check only, not evidence: Im(zeta) = sin(2 pi/7) > 0 is the premise of sign_im itself.
    assert sign_im(ZETA) > 0
    # f has no rational root (+-1 are the only candidates), so it is irreducible over Q
    assert all(r ** 3 + r ** 2 - 2 * r - 1 != 0 for r in (1, -1))
    return sorted(checks)


_BRACKET = {}


def bracket(N):
    """L with f(L/2^N) < 0 < f((L+1)/2^N), 2^N <= L < 2^(N+1)."""
    if N not in _BRACKET:
        S = 1 << N
        g = lambda L: L ** 3 + L * L * S - 2 * L * S * S - S ** 3      # 2^(3N) f(L/2^N)
        lo, hi = S, 2 * S
        assert g(lo) < 0 < g(hi)
        while hi - lo > 1:
            mid = (lo + hi) // 2
            gm = g(mid)
            assert gm != 0
            if gm < 0:
                lo = mid
            else:
                hi = mid
        assert g(lo) < 0 < g(lo + 1) and S <= lo < 2 * S
        _BRACKET[N] = lo
    return _BRACKET[N]


def sign_at_c(q0, q1, q2):
    """certified sign of q0 + q1 c + q2 c^2 at c = 2 cos(2 pi/7)"""
    if q0 == 0 and q1 == 0 and q2 == 0:
        STATS['exact_zero'] += 1
        return 0
    N, bits = 64, max(abs(q0).bit_length(), abs(q1).bit_length(), abs(q2).bit_length())
    while N < bits + 32:                                           # powers of two: small bracket cache
        N *= 2
    while True:
        L = bracket(N)
        S = 1 << N
        a, b = L, L + 1                                            # c in (a/S, b/S), a > 0
        lo = hi = q0 * S * S
        t = (q1 * a * S, q1 * b * S)
        lo += min(t); hi += max(t)
        t = (q2 * a * a, q2 * b * b)
        lo += min(t); hi += max(t)
        if lo > 0:
            STATS['max_bits'] = max(STATS['max_bits'], N)
            return 1
        if hi < 0:
            STATS['max_bits'] = max(STATS['max_bits'], N)
            return -1
        STATS['refinements'] += 1
        N *= 2


def sign_im(a):
    d1, d2, d3 = a[1] - a[6], a[2] - a[5], a[3] - a[4]
    return sign_at_c(d1 - d3, d2, d3)


def sign_re(a):
    s1, s2, s3 = a[1] + a[6], a[2] + a[5], a[3] + a[4]
    return sign_at_c(2 * a[0] - 2 * s2 + s3, s1 - s3, s2 - s3)


def cross_sign(a, b):
    """sign of the cross product a x b = Im(conj(a) b)"""
    return sign_im(mul(conj(a), b))


# ---------------------------------------------------------------- 200-digit Decimal (evidence only)
decimal.setcontext(decimal.Context(prec=220))
D0 = decimal.Decimal(0)
EPS = decimal.Decimal(10) ** -225


def dec_pi():
    def atan_inv(x):
        x = decimal.Decimal(x); x2 = x * x; term = 1 / x; s = term; k = 1
        while True:
            term = -term / x2; k += 2; d = term / k
            if abs(d) < EPS:
                return s
            s += d
    return 4 * (4 * atan_inv(5) - atan_inv(239))


def dec_cos_sin(x):
    c = s = D0; term = decimal.Decimal(1); k = 0
    while True:
        if k % 4 == 0: c += term
        elif k % 4 == 1: s += term
        elif k % 4 == 2: c -= term
        else: s -= term
        k += 1
        term = term * x / k
        if abs(term) < EPS and k > 10:
            return c, s


PI = dec_pi()
TRIG = [dec_cos_sin(2 * j * PI / 7) for j in range(7)]
HALF = dec_cos_sin(PI / 7)                   # e^{i pi/7}


def dec_point(w):
    return (sum((x * TRIG[j][0] for j, x in enumerate(w)), D0), sum((x * TRIG[j][1] for j, x in enumerate(w)), D0))


def dec_cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def dec_rotate(p, cs, inverse=False):
    c, s = cs
    if inverse:
        s = -s
    return (c * p[0] - s * p[1], s * p[0] + c * p[1])


# ---------------------------------------------------------------- configurations
def read_set(path):
    raw = Path(path).read_bytes()
    rows = [tuple(map(int, line.split())) for line in raw.decode().splitlines() if line.strip() and not line.startswith('#')]
    assert len(rows) == 64 and all(len(r) == 7 for r in rows), path
    return raw, rows


def configuration(rows, mirror, p0_choice=0):
    """Exact normalisation: returns dict with labelled points P[i*7+k], H, Y, psi order, layer data."""
    pts = [norm(conj(r) if mirror else r) for r in rows]
    assert len(set(pts)) == 64, 'repeated point'
    centre = [n for n, p in enumerate(pts) if p == ZERO]
    assert len(centre) == 1, 'centre count %d' % len(centre)
    rest = [p for p in pts if p != ZERO]
    pset = set(rest)
    orbits, seen = [], set()
    for p in rest:
        if p in seen:
            continue
        orb = [norm(rot(p, k)) for k in range(7)]
        assert len(set(orb)) == 7 and all(q in pset for q in orb), 'not a full rotation orbit'
        seen.update(orb); orbits.append(orb)
    assert len(orbits) == 9 and len(seen) == 63
    # layer order: decreasing exact squared radius |p|^2 = p conj(p) (real)
    r2 = {id(o): mul(o[0], conj(o[0])) for o in orbits}
    assert all(sign_im(v) == 0 for v in r2.values())

    def cmp(o1, o2):
        s = sign_re(sub(r2[id(o2)], r2[id(o1)]))
        assert s != 0, 'two layers with equal radius'
        return s
    orbits.sort(key=cmp_to_key(cmp))
    p0 = orbits[0][p0_choice]
    reps, z = [], []
    for i, orb in enumerate(orbits):
        cand = []
        for q in orb:
            zq = mul(q, conj(p0))
            if sign_im(zq) >= 0 and sign_im(mul(zq, conj(ZETA))) < 0:      # arg in [0, 2 pi/7)
                cand.append((q, zq))
        assert len(cand) == 1, ('sector representative', i, len(cand))
        reps.append(cand[0][0]); z.append(cand[0][1])
    assert reps[0] == p0
    H, u = {}, [z[0]]
    for i in range(1, 9):
        s = sign_im(mul(z[i], OMEGA_BAR))                                    # sign sin(theta_i - pi/7)
        assert s != 0, 'theta_i = pi/7'
        H[i] = s < 0
        ui = z[i] if H[i] else mul(z[i], OMEGA_BAR)
        assert sign_im(ui) > 0 and sign_im(mul(ui, OMEGA_BAR)) < 0, 'psi_i not in (0, pi/7)'
        u.append(ui)
    Y = {}
    for i, j in itertools.combinations(range(1, 9), 2):
        s = cross_sign(u[i], u[j])
        assert s != 0, 'equal phases'
        Y[(i, j)] = s > 0
    lt = lambda i, j: True if i == 0 else (False if j == 0 else (Y[(i, j)] if i < j else not Y[(j, i)]))
    order = sorted(range(9), key=cmp_to_key(lambda i, j: -1 if lt(i, j) else 1))
    for a, b in zip(order, order[1:]):
        assert lt(a, b)
    P = [rot(reps[i], k) for i in range(9) for k in range(7)]
    rowidx = {p: n for n, p in enumerate(pts)}
    return {'P': P, 'H': H, 'Y': Y, 'order': order, 'reps': reps, 'p0': p0, 'centre_row': centre[0],
            'row_of': [rowidx[norm(p)] for p in P], 'pts': pts}


def orientations(P):
    """exact sign of orient(P_a, P_b, P_c) for a < b < c, plus orient(O, P_a, P_b) for a < b"""
    sg = {}
    for a, b, c in itertools.combinations(range(len(P)), 3):
        s = cross_sign(sub(P[b], P[a]), sub(P[c], P[a]))
        assert s != 0, ('collinear', a, b, c)
        sg[(a, b, c)] = s
    sc = {}
    for a, b in itertools.combinations(range(len(P)), 2):
        s = cross_sign(P[a], P[b])
        assert s != 0, ('collinear with centre', a, b)
        sc[(a, b)] = s
    return sg, sc


def perm_parity(t):
    s = 1
    for x in range(3):
        for y in range(x + 1, 3):
            if t[x] > t[y]:
                s = -s
    return s


def orient(sg, a, b, c):
    t = (a, b, c)
    return sg[tuple(sorted(t))] * perm_parity(t)


def rotation_check(sg):
    nxt = lambda n: (n // 7) * 7 + (n % 7 + 1) % 7
    bad = sum(1 for (a, b, c), s in sg.items() if orient(sg, nxt(a), nxt(b), nxt(c)) != s)
    return bad


_Z7 = []


def z7exact_check(cfg, sg, sc):
    if not _Z7:
        spec = importlib.util.spec_from_file_location('pf_z7exact', RESULTS / 'PRIMEFOLD/check64/z7exact.py')
        Z = importlib.util.module_from_spec(spec); spec.loader.exec_module(Z); _Z7.append(Z)
    O = _Z7[0].orient_table(cfg['pts'])
    R = cfg['row_of']; c0 = cfg['centre_row']
    bad = sum(1 for (a, b, c), s in sg.items() if O[R[a]][R[b]][R[c]] != s)
    bad += sum(1 for (a, b), s in sc.items() if O[c0][R[a]][R[b]] != s)
    return len(sg) + len(sc), bad


def decimal_check(cfg, sg, sc):
    """evidence only: 200-digit recomputation of orientations, H and Y"""
    D = [dec_point(p) for p in cfg['P']]
    scale = max(max(abs(x), abs(y)) for x, y in D)
    tol = scale * scale * decimal.Decimal(10) ** -180
    undecided = disagree = 0; minabs = None
    for (a, b, c), s in sg.items():
        pa = D[a]
        v = dec_cross((D[b][0] - pa[0], D[b][1] - pa[1]), (D[c][0] - pa[0], D[c][1] - pa[1]))
        minabs = abs(v) if minabs is None else min(minabs, abs(v))
        if abs(v) <= tol:
            undecided += 1
        elif (v > 0) != (s > 0):
            disagree += 1
    for (a, b), s in sc.items():
        v = dec_cross(D[a], D[b])
        if abs(v) <= tol:
            undecided += 1
        elif (v > 0) != (s > 0):
            disagree += 1
    # phases: representative k = 0 of each layer, measured from P[0]
    p0 = D[0]; hb = 0; yb = 0; ups = [p0]
    for i in range(1, 9):
        q = D[7 * i]
        assert dec_cross(p0, q) > tol and dec_cross(dec_rotate(p0, TRIG[1]), q) < -tol
        v = dec_cross(dec_rotate(p0, HALF), q)
        hb += (v < 0) != cfg['H'][i]
        ups.append(q if v < 0 else dec_rotate(q, HALF, inverse=True))
    for (i, j), y in cfg['Y'].items():
        yb += (dec_cross(ups[i], ups[j]) > 0) != y
    return {'orientation_signs': len(sg) + len(sc), 'undecided': undecided, 'disagreements': disagree,
            'H_disagreements': hb, 'Y_disagreements': yb, 'min_abs_orientation': '%.4e' % minabs,
            'max_abs_coordinate': '%.4e' % scale}


# ---------------------------------------------------------------- CNF
def read_cnf(path):
    raw = Path(path).read_bytes()
    lines = raw.decode().splitlines()
    head = lines[0].split()
    assert head[:2] == ['p', 'cnf']
    nv, ncl = int(head[2]), int(head[3])
    cls = []
    for line in lines[1:]:
        lits = list(map(int, line.split()))
        assert lits and lits[-1] == 0 and 0 not in lits[:-1]
        cls.append(lits[:-1])
    assert len(cls) == ncl
    assert all(abs(l) <= nv for cl in cls for l in cl)
    return hashlib.sha256(raw).hexdigest(), nv, cls


def families(mp, cls):
    t, m = mp['t'], mp['m']
    ntrans = 2 * math.comb(t - 1, 3)
    nang = mp['counts']['unit'] + mp['counts']['cond']
    nnest = math.comb(t, 2) * m
    nchain = mp['counts']['chain']
    assert ntrans + nang + nnest + nchain == len(cls)
    fam = ['transitivity'] * ntrans + ['angular'] * nang + ['nesting'] * nnest + ['chain'] * nchain
    return fam


def assignment(mp, cfg, sg):
    val = [None] * (mp['nv'] + 1)
    for c, v in mp['orb']:
        idx = [i * 7 + k for i, k in c]
        val[v] = orient(sg, *idx) > 0
    for i, j, v in mp['Y']:
        val[v] = cfg['Y'][(i, j)]
    for i, v in mp['H']:
        val[v] = cfg['H'][i]
    return val


def least_chain_model(cls, val):
    """least model of the clauses that remain once the geometric variables are fixed (Horn in the chain vars)"""
    head, need, uses, queue = [], [], collections.defaultdict(list), collections.deque()
    for cl in cls:
        pos, neg, sat = [], [], False
        for l in cl:
            x = val[abs(l)]
            if x is None:
                (pos if l > 0 else neg).append(abs(l))
            elif x == (l > 0):
                sat = True
                break
        if sat or (not pos and not neg):
            continue
        assert len(pos) <= 1, 'non-Horn clause'
        idx = len(head); head.append(pos[0] if pos else 0); need.append(len(neg))
        for v in neg:
            uses[v].append(idx)
        if not neg:
            queue.append(idx)
    true = set()
    while queue:
        idx = queue.popleft(); h = head[idx]
        if not h or h in true:
            continue
        true.add(h)
        for nx in uses[h]:
            need[nx] -= 1
            if not need[nx]:
                queue.append(nx)
    return true


def evaluate(cls, fam, val):
    """extend val by the least chain model (others false) and count unsatisfied clauses per family"""
    true = least_chain_model(cls, val)
    full = [x if x is not None else (v in true) for v, x in enumerate(val)]
    viol = collections.Counter({f: 0 for f in set(fam)})
    for cl, f in zip(cls, fam):
        if not any(full[abs(l)] == (l > 0) for l in cl):
            viol[f] += 1
    return dict(sorted(viol.items())), len(true), full


def main():
    args = sys.argv[1:]
    dump = None
    if args[0] == '--dump':
        dump = Path(args[1]); args = args[2:]
        dump.mkdir(parents=True, exist_ok=True)
    cnf = args[0]; sets = args[1:]
    print(json.dumps({'rigor': 'exact computation (Decimal cross-check: evidence only)', 'identities_checked': identities(),
                      'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'python': sys.version.split()[0]}), flush=True)
    sha, nv, cls = read_cnf(cnf)
    mp = json.loads(Path(cnf + '.map.json').read_text())
    assert (mp['m'], mp['K'], mp['t'], mp['nv'], mp['ncl']) == (7, 8, 9, nv, len(cls))
    assert len(mp['orb']) == math.comb(63, 3) // 7 and len(mp['Y']) == 28 and len(mp['H']) == 8
    fam = families(mp, cls)
    maxgeo = max(v for _, v in mp['orb'])
    assert maxgeo == len(mp['orb']) + 28 + 8                     # Y, H, orbit vars are 1..maxgeo
    for cl, f in zip(cls, fam):                                  # chain clauses are exactly those with chain vars
        geo = all(abs(l) <= maxgeo for l in cl)
        assert geo == (f != 'chain'), f
    print(json.dumps({'cnf': Path(cnf).name, 'sha256': sha, 'variables': nv, 'clauses': len(cls),
                      'families': dict(collections.Counter(fam)), 'orbit_vars': len(mp['orb'])}), flush=True)
    total_viol = 0; flips_ok = True
    for path in sets:
        raw, rows = read_set(path)
        name = Path(path).stem
        res = {}
        for mirror in (False, True):
            STATS.clear()
            t0 = time.monotonic()
            cfg = configuration(rows, mirror)
            # phases do not depend on which layer-0 point is put at angle 0
            p0_invariant = all((c['H'], c['Y']) == (cfg['H'], cfg['Y'])
                               for c in (configuration(rows, mirror, k) for k in range(1, 7)))
            sg, sc = orientations(cfg['P'])
            rot_bad = rotation_check(sg)
            nz, zbad = z7exact_check(cfg, sg, sc)
            dec = decimal_check(cfg, sg, sc)
            val = assignment(mp, cfg, sg)
            viol, ntrue, full = evaluate(cls, fam, val)
            nviol = sum(viol.values()); total_viol += nviol
            out = {'set': name, 'sha256': hashlib.sha256(raw).hexdigest(), 'case': 'mirror' if mirror else 'original',
                   'centre_row': cfg['centre_row'], 'p0_row': cfg['row_of'][0],
                   'triples_nonzero': len(sg) + len(sc), 'rotation_invariance_failures': rot_bad,
                   'phase_independent_of_p0': p0_invariant, 'z7exact_agreement': '%d/%d' % (nz - zbad, nz),
                   'decimal200_evidence': dec,
                   'H': ''.join('1' if cfg['H'][i] else '0' for i in range(1, 9)),
                   'H1': cfg['H'][1], 'Y12': cfg['Y'][(1, 2)], 'psi_order': cfg['order'],
                   'clauses': len(cls), 'violations': viol, 'violations_total': nviol, 'chain_vars_true': ntrue,
                   'sign_stats': dict(STATS), 'seconds': round(time.monotonic() - t0, 2)}
            assert rot_bad == 0 and p0_invariant and zbad == 0
            if not mirror:
                # negative controls: one wrong geometric value at a time.  The angular-unit flip only breaks its own
                # unit clause (a check of the bookkeeping); the H, Y and random orbit-variable flips test whether the
                # clause evaluation responds to the geometry.  The random orbit variables (fixed seed, the same
                # five for every set) are not guaranteed to break a clause, so only the unit flip is asserted.
                mut = {}
                unit = next(cl[0] for cl, f in zip(cls, fam) if f == 'angular' and len(cl) == 1)
                Hv = dict((i, v) for i, v in mp['H'])
                ctl = [('flip_first_angular_unit_var', abs(unit)), ('flip_H1', Hv[1]), ('flip_H8', Hv[8]),
                       ('flip_Y12', next(v for i, j, v in mp['Y'] if (i, j) == (1, 2)))]
                orbvars = sorted(v for _, v in mp['orb'])
                ctl += [('flip_orbit_var_%d' % v, v) for v in random.Random(20261106).sample(orbvars, 5)]
                for label, var in ctl:
                    v2 = list(val); v2[var] = not v2[var]
                    mv, _, _ = evaluate(cls, fam, v2)
                    mut[label] = sum(mv.values())
                out['negative_controls_violations'] = mut
                assert mut['flip_first_angular_unit_var'] > 0, mut
            if dump:
                text = ' '.join(str(v if full[v] else -v) for v in range(1, len(full))) + ' 0\n'
                fn = dump / ('%s.%s.assign' % (name, out['case']))
                fn.write_text(text)
                out['assignment_sha256'] = hashlib.sha256(text.encode()).hexdigest()
            res[mirror] = cfg
            print(json.dumps(out), flush=True)
        o, mr = res[False], res[True]
        flip = {'set': name, 'H1_original': o['H'][1], 'H1_mirror': mr['H'][1],
                'H1_flips': o['H'][1] != mr['H'][1],
                'all_H_flip': all(o['H'][i] != mr['H'][i] for i in range(1, 9)),
                'all_Y_reverse': all(o['Y'][k] != mr['Y'][k] for k in o['Y']),
                'mirror_psi_order_is_reverse_on_layers_1_to_8': mr['order'][1:] == o['order'][1:][::-1]}
        flips_ok &= flip['H1_flips']
        print(json.dumps(flip), flush=True)
    status = 'PASS' if total_viol == 0 and flips_ok else 'FAIL'
    print(json.dumps({'status': status, 'sets': len(sets),
                      'cases': 2 * len(sets), 'violations_total': total_viol, 'H1_flips_in_all': flips_ok,
                      'elapsed_seconds': round(time.monotonic() - START, 1),
                      'max_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024}), flush=True)
    sys.exit(0 if status == 'PASS' else 1)          # a violation or a missing H(1) flip gives exit status 1


if __name__ == '__main__':
    main()
