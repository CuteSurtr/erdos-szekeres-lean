#!/usr/bin/env python3
"""Exact search for infinitesimal extensions of an m-fold set by one or two new orbits (m = 3, 4).

Moves (all exact limit order types, polyeval.c):
  D(l, d):  double orbit l: twin orbit with representative P_l + eps^(1 + maxexp(P_l)) d
  A(E, v):  new orbit {eps^E g^k v} at a new scale level E (E = -4 outer, +4 inner; base at level 0)
For each move family the direction d (or v) ranges over one representative of every open arc between consecutive
critical directions (complete for that family; see double_exact.py / addon_exact.py for the critical sets).
Pairs: only pairs of moves that are individually octagon-free (a convex octagon of B + m1 stays in B + m1 + m2).
usage: twostep.py M FILE [--remove i] [--add-centre] [--no-centre] [--pairs] [--maxpairs N]
"""
import sys, os, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from double_exact import peval, read_set, rot, cross, prim, angcmp, orbits_of, critical_arcs


def orbit_points(m, rep):
    """rep: list of terms (e, x, y); returns m polynomial points (rotate every term)"""
    pts = [rep]
    cur = rep
    for _ in range(m - 1):
        cur = [(e,) + rot(m, (x, y)) for (e, x, y) in cur]
        pts.append(cur)
    return pts


def lead(poly_terms):
    """leading (lowest exponent) nonzero vector of a polynomial point given as dict e -> (x, y)"""
    for e in sorted(poly_terms):
        v = poly_terms[e]
        if v != (0, 0):
            return v
    return (0, 0)


def diff(p, q):
    d = {}
    for (e, x, y) in p:
        a = d.get(e, (0, 0)); d[e] = (a[0] + x, a[1] + y)
    for (e, x, y) in q:
        a = d.get(e, (0, 0)); d[e] = (a[0] - x, a[1] - y)
    return d


def config(m, reps, centre):
    pts = []
    for r in reps:
        pts.extend(orbit_points(m, r))
    if centre:
        pts.append([(0, 0, 0)])
    return pts


def double_moves(m, reps, centre, l):
    allpts = config(m, reps, centre)
    p0 = reps[l]
    dirs = []
    for q in allpts:
        if q == p0:
            continue
        v = lead(diff(q, p0))
        if v != (0, 0):
            dirs.append(v); dirs.append((-v[0], -v[1]))
    emax = max(e for (e, x, y) in p0)
    E = emax + 1
    return [('D', l, E, d) for d in critical_arcs(dirs)]


def level_moves(m, reps, centre, E):
    """new orbit at level E: critical directions: points and differences (leading terms), and the edge factors"""
    allpts = config(m, reps, centre)
    dirs = []
    leads = [lead(diff(q, [(0, 0, 0)])) for q in allpts]
    for v in leads:
        if v != (0, 0):
            dirs.append(v)
    if E > 0:  # inner: differences among points do not matter except antipodes; edges of V vs points
        pass
    else:      # outer: v vs differences of base points
        for i in range(len(allpts)):
            for j in range(i + 1, len(allpts)):
                v = lead(diff(allpts[i], allpts[j]))
                if v != (0, 0):
                    dirs.append(v)
    facs = [lambda p: p]
    if m == 4:
        facs += [lambda p: (p[0] - p[1], p[0] + p[1]), lambda p: (p[0] + p[1], p[1] - p[0])]
    else:
        facs += [lambda p: (2 * p[0] - p[1], p[0] + p[1]), lambda p: (p[0] + p[1], 2 * p[1] - p[0]),
                 lambda p: (p[0] - 2 * p[1], 2 * p[0] - p[1])]
    D2 = []
    for v in dirs:
        for f in facs:
            w = f(v)
            D2.append(w); D2.append((-w[0], -w[1]))
    # reduce by rotation symmetry is unnecessary: arcs over the full circle are a superset
    return [('A', None, E, v) for v in critical_arcs(D2)]


def arcs_with_bounds(dirs):
    from functools import cmp_to_key
    ds = sorted(set(prim(d) for d in dirs if d != (0, 0)), key=cmp_to_key(angcmp))
    C = []
    for d in ds:
        if C and angcmp(C[-1], d) == 0:
            continue
        C.append(d)
    out = []
    for i in range(len(C)):
        a = C[i]; b = C[(i + 1) % len(C)]
        if cross(a, b) > 0:
            out.append(((a[0] + b[0], a[1] + b[1]), a, b))
    return out


def double_moves_b(m, reps, centre, l):
    allpts = config(m, reps, centre)
    p0 = reps[l]
    dirs = []
    for q in allpts:
        if q == p0:
            continue
        v = lead(diff(q, p0))
        if v != (0, 0):
            dirs.append(v); dirs.append((-v[0], -v[1]))
    E = max(e for (e, x, y) in p0) + 1
    return [(('D', l, E, d), lo, hi) for (d, lo, hi) in arcs_with_bounds(dirs)]


def level_moves_b(m, reps, centre, E):
    mv = level_moves(m, reps, centre, E)
    allpts = config(m, reps, centre)
    dirs = []
    for q in allpts:
        v = lead(diff(q, [(0, 0, 0)]))
        if v != (0, 0):
            dirs.append(v)
    if E < 0:
        for i in range(len(allpts)):
            for j in range(i + 1, len(allpts)):
                v = lead(diff(allpts[i], allpts[j]))
                if v != (0, 0):
                    dirs.append(v)
    facs = [lambda p: p]
    if m == 4:
        facs += [lambda p: (p[0] - p[1], p[0] + p[1]), lambda p: (p[0] + p[1], p[1] - p[0])]
    else:
        facs += [lambda p: (2 * p[0] - p[1], p[0] + p[1]), lambda p: (p[0] + p[1], 2 * p[1] - p[0]),
                 lambda p: (p[0] - 2 * p[1], 2 * p[0] - p[1])]
    D2 = []
    for v in dirs:
        for f in facs:
            w = f(v)
            D2.append(w); D2.append((-w[0], -w[1]))
    return [(('A', None, E, d), lo, hi) for (d, lo, hi) in arcs_with_bounds(D2)]


def apply(m, reps, mv):
    kind, l, E, d = mv
    if kind == 'D':
        return reps + [reps[l] + [(E, d[0], d[1])]]
    return reps + [[(E, d[0], d[1])]]


def save_found(m, reps, centre, tag):
    import json, hashlib
    pts = config(m, reps, centre)
    h = hashlib.sha1(repr(pts).encode()).hexdigest()[:12]
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sets', 'found_%s_%s.json' % (tag, h))
    json.dump({'m': m, 'points': pts, 'reps': reps, 'centre': centre}, open(fn, 'w'))
    print('  saved', fn, flush=True)


def n8_of(m, reps, centre):
    ml, cnt, nz = peval(config(m, reps, centre))
    return (cnt[8] if not nz else None), ml


def main():
    m = int(sys.argv[1]); fn = sys.argv[2]
    P = read_set(fn, m)
    orbs, centre = orbits_of(P, m)
    if '--remove' in sys.argv:
        rem = set(int(x) for x in sys.argv[sys.argv.index('--remove') + 1].split(','))
        orbs = [o for i, o in enumerate(orbs) if i not in rem]
    if '--add-centre' in sys.argv:
        centre = True
    if '--no-centre' in sys.argv:
        centre = False
    levels = '--no-levels' not in sys.argv
    maxpairs = int(sys.argv[sys.argv.index('--maxpairs') + 1]) if '--maxpairs' in sys.argv else 10 ** 9
    reps = [[(0, o[0][0], o[0][1])] for o in orbs]
    n0, ml0 = n8_of(m, reps, centre)
    tag = os.path.basename(fn) + (' remove=' + sys.argv[sys.argv.index('--remove') + 1] if '--remove' in sys.argv else '')
    print('%s m=%d orbits=%d centre=%s base n8=%s maxlen=%s' % (tag, m, len(reps), centre, n0, ml0), flush=True)
    t0 = time.time()
    moves = []
    for l in range(len(reps)):
        moves += double_moves(m, reps, centre, l)
    if levels:
        moves += level_moves(m, reps, centre, -4) + level_moves(m, reps, centre, 4)
    free = []; best = None
    for mv in moves:
        n8, ml = n8_of(m, apply(m, reps, mv), centre)
        if n8 is None:
            continue
        if best is None or n8 < best[0]:
            best = (n8, mv[0], mv[1], mv[2])
        if n8 == 0:
            free.append(mv)
            if '--save-singles' in sys.argv:
                save_found(m, apply(m, reps, mv), centre, 'single')
    print('  single moves=%d free=%d best=%s (%.0fs)' % (len(moves), len(free), best, time.time() - t0), flush=True)
    for mv in free[:5]:
        print('   free single', mv, flush=True)
    if '--pairs' not in sys.argv or len(free) < 2:
        print('DONE', tag, flush=True)
        return
    # complete pair search: for every free first move a, recompute the critical arcs on B + a and evaluate every
    # second move whose direction lies in an arc that was free for B alone (other arcs contain octagons already)
    def arcs_of(family_moves):
        return [mv[3] for mv in family_moves]
    def in_free_arc(fam, d):
        # free base arcs of this family: list of (lo, hi) critical neighbours; d inside one of them
        for (lo, hi) in freearcs.get(fam, []):
            if cross(lo, d) > 0 and cross(d, hi) > 0:
                return True
        return False
    # rebuild free arcs with their bounding critical directions
    freearcs = {}
    def fam_moves(reps_, fam):
        if fam[0] == 'D':
            return double_moves_b(m, reps_, centre, fam[1])
        return level_moves_b(m, reps_, centre, fam[1])
    fams = [('D', l) for l in range(len(reps))] + ([('A', -4), ('A', 4)] if levels else [])
    for fam in fams:
        for (mv, lo, hi) in fam_moves(reps, fam):
            if mv in free:
                freearcs.setdefault(fam, []).append((lo, hi))
    npairs = 0; bestp = None; found = 0
    for a in free:
        ra = apply(m, reps, a)
        fa = ('D', a[1]) if a[0] == 'D' else ('A', a[2])
        for fam in fams:
            if fam == fa or fam not in freearcs:
                continue
            for (mv, lo, hi) in fam_moves(ra, fam):
                if not in_free_arc(fam, mv[3]):
                    continue
                npairs += 1
                n8, ml = n8_of(m, apply(m, ra, mv), centre)
                if n8 is None:
                    continue
                if bestp is None or n8 < bestp[0]:
                    bestp = (n8, a, mv)
                if n8 == 0:
                    found += 1
                    print('  FOUND PAIR', a, mv, flush=True)
                    save_found(m, apply(m, ra, mv), centre, 'pair')
            if npairs > maxpairs:
                break
        if npairs > maxpairs:
            break
    print('  pairs=%d found=%d best=%s (%.0fs)' % (npairs, found, bestp, time.time() - t0), flush=True)
    print('DONE', tag, flush=True)


if __name__ == '__main__':
    main()
