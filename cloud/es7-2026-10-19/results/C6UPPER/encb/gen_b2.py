#!/usr/bin/env python3
"""Second implementation of the same mathematical encoding as gen.py (no shared code; see the scope note below):
  * point (i,k) = layer i (0 outermost), direction sector k; triples are enumerated layer-major (the helper `pid`
    below is unused);
  * triple-orbit canonical form: rotate so that the first point (in (layer,k) order) has k = 0, take the
    lexicographically smallest (layer,k)-sorted list (this selects the same representatives as gen.py);
  * angular configuration computed EXACTLY (integer circular order of points and antipodes), no float sampling:
    direction of (i,k) = (J, rank) with J = 2k + h_i (mod 2m), units of pi/m, h_i = 0 iff theta_i < pi/m, and the
    psi-rank inside the cell; antipode = (J + m, rank);
  * chains are built BACKWARDS (F_l(q,q') = chain of l points starting q, q');
  * only clauses whose orientation literal is forced false are dropped; true-forced literals are kept.
Scope (4 November 2026 review): the two encoders differ in the angular computation (exact integer circular order here,
sampled float patterns in gen.py), the chain recurrence direction and the variable allocation; they share the triple
canonical representatives, and parts of the validation code use gen.py.
Same-layer antipodal triples (even m): the centre lies on a segment of the triple, which is neither a triangle around the
centre nor in an open half-plane; such triples get no angular clause (a third, deliberately omitted case).
Odd m: as written for m = 7 (C7UPPER/gen_b.py; this file reproduces its output byte for byte).
Even m (added 3 November 2026): psi_i = theta_i mod 2pi/m, no Hb variables; direction of (i,k) = (k, rank) in units of
2pi/m, antipode = (k + m/2, rank), which is the direction of the orbit point (i, k + m/2).  A triple containing such an
antipodal pair of one layer has coinciding keys; it gets no angular clause (weaker, sound).
Variables: orbit vars; Y'(i,j) = [psi_i < psi_j] for 1 <= i < j; Hb(i) = [theta_i < pi/m] for i >= 1 (odd m only).
usage: gen_b.py m K t OUT.cnf   (writes OUT.cnf and OUT.cnf.map.json)
"""
import sys, itertools, json


def main():
    m, K, t = map(int, sys.argv[1:4]); out = sys.argv[4]
    odd = m % 2 == 1
    pid = lambda i, k: k * t + i
    nv = [0]
    def new():
        nv[0] += 1
        return nv[0]
    # ---- phase variables first (different numbering from gen.py)
    Yv = {}
    for i in range(1, t):
        for j in range(i + 1, t):
            Yv[(i, j)] = new()
    Hv = {i: new() for i in range(1, t)} if odd else {}
    # ---- orbit variables
    def canon(tri):              # tri: list of (i,k)
        best = None
        for (i0, k0) in tri:
            s = (-k0) % m
            rt = sorted((i, (k + s) % m) for (i, k) in tri)
            if best is None or rt < best:
                best = rt
        return tuple(best)
    orb = {}
    pts = [(i, k) for i in range(t) for k in range(m)]
    for tri in itertools.combinations(pts, 3):
        c = canon(list(tri))
        if c not in orb:
            orb[c] = new()
    def perm_sign(seq):
        s = 1; a = list(seq)
        for x in range(len(a)):
            for y in range(x + 1, len(a)):
                if a[x] > a[y]:
                    s = -s
        return s
    def olit(P, Q, R):          # literal for orient(P,Q,R) = +, P,Q,R as (i,k)
        tri = [P, Q, R]
        # rotate so that a chosen point gets k = 0 and sort; find the rotation used by canon
        c = canon(tri)
        for (i0, k0) in tri:
            s = (-k0) % m
            rt = [(i, (k + s) % m) for (i, k) in tri]
            if tuple(sorted(rt)) == c:
                # orientation of (P,Q,R) = orientation of rt (rotation) = sign(perm rt->sorted) * V
                order = sorted(range(3), key=lambda r: rt[r])
                sg = perm_sign(order)
                v = orb[c]
                return v if sg > 0 else -v
        raise RuntimeError
    cls = []
    # ---- psi order transitivity (forbid cyclic triangles)
    for i, j, k in itertools.combinations(range(1, t), 3):
        cls.append([-Yv[(i, j)], -Yv[(j, k)], Yv[(i, k)]])
        cls.append([Yv[(i, j)], Yv[(j, k)], -Yv[(i, k)]])
    # ---- exact angular configurations
    forced = {}
    nunit = 0; ncond = 0
    for c, v in orb.items():
        Ls = sorted(set(i for (i, k) in c))
        free = [L for L in Ls if L != 0]
        outs = []
        for ranks in itertools.permutations(range(len(free))):
            rk = {L: r + 1 for L, r in zip(free, ranks)}
            rk[0] = 0
            for hb in itertools.product([0, 1], repeat=len(free) if odd else 0):
                h = {L: b for L, b in zip(free, hb)}
                h[0] = 0
                # premise literals (true under this pattern)
                prem = []
                for a_, b_ in itertools.combinations(free, 2):
                    lit = Yv[(a_, b_)] if a_ < b_ else Yv[(b_, a_)]
                    truth = rk[a_] < rk[b_] if a_ < b_ else rk[b_] < rk[a_]
                    prem.append(lit if truth else -lit)
                for L in (free if odd else []):
                    prem.append(Hv[L] if h[L] == 0 else -Hv[L])
                # circular order of points and antipodes
                objs = []
                for idx, (i, k) in enumerate(c):
                    if odd:
                        J = (2 * k + h[i]) % (2 * m); Ja = (J + m) % (2 * m)
                    else:
                        J = k; Ja = (k + m // 2) % m
                    objs.append(((J, rk[i]), 'P', idx))
                    objs.append(((Ja, rk[i]), 'A', idx))
                keys = [o[0] for o in objs]
                if len(set(keys)) < 6:
                    assert not odd
                    outs.append((prem, None))
                    continue
                assert len(set(keys)) == 6
                objs.sort()
                kinds = ''.join(o[1] for o in objs)
                lit = None
                if kinds in ('PAPAPA', 'APAPAP'):
                    seq = [o[2] for o in objs if o[1] == 'P']          # ccw order of the 3 points
                    sg = perm_sign(seq)
                    lit = v if sg > 0 else -v                          # orient(c0,c1,c2) = sign of cyclic order
                else:
                    dbl = kinds + kinds
                    st = dbl.find('PPP')
                    assert st >= 0, kinds
                    seq = [objs[(st + r) % 6][2] for r in range(3)]
                    a, b, cc = (c[x] for x in seq)
                    if b[0] <= a[0] and b[0] <= cc[0]:
                        lit = olit(a, b, cc)
                outs.append((prem, lit))
        vals = set(l for _, l in outs)
        if len(vals) == 1 and None not in vals:
            l = vals.pop()
            cls.append([l]); forced[abs(l)] = l; nunit += 1
        else:
            for prem, l in outs:
                if l is not None:
                    cls.append([-x for x in prem] + [l]); ncond += 1
    # ---- nesting
    for i in range(t):
        for j in range(i + 1, t):
            for k in range(m):
                l = olit((i, 0), (i, 1), (j, k))
                cls.append([l])
                if forced.get(abs(l), l) != l:
                    raise RuntimeError('conflict')
                forced[abs(l)] = l
    def is_false(l):
        f = forced.get(abs(l))
        return f is not None and f == -l
    # ---- backward chains
    nchain = 0
    L = K - 1
    for i in range(t):
        p = (i, 0)
        Q = [(j, k) for j in range(i, t) for k in range(m) if (j, k) != p]
        F = {}
        def fv(l, a, b):
            key = (l, a, b)
            if key not in F:
                F[key] = new()
            return F[key]
        okpair = {}
        for a in Q:
            for b in Q:
                if a != b:
                    l = olit(p, a, b)
                    if not is_false(l):
                        okpair[(a, b)] = l
        # o(p,a,b) => F_2(a,b)
        for (a, b), l in okpair.items():
            cls.append([fv(2, a, b), -l]); nchain += 1
        for lev in range(2, L):
            # F_lev(b,c) & o(p,a,b) & o(a,b,c) => F_{lev+1}(a,b)
            for (b, c), _ in okpair.items():
                if (lev, b, c) not in F:
                    continue
                for a in Q:
                    if a == b or a == c or (a, b) not in okpair:
                        continue
                    lt = olit(a, b, c)
                    if is_false(lt):
                        continue
                    cl = [-F[(lev, b, c)], -okpair[(a, b)], -lt]
                    if lev + 1 < L:
                        cl.append(fv(lev + 1, a, b))
                    cls.append(cl); nchain += 1
    with open(out, 'w') as f:
        f.write('p cnf %d %d\n' % (nv[0], len(cls)))
        for cl in cls:
            f.write(' '.join(map(str, cl)) + ' 0\n')
    mp = {'m': m, 'K': K, 't': t, 'nv': nv[0], 'ncl': len(cls),
          'orb': [[list(map(list, c)), v] for c, v in orb.items()],
          'Y': [[i, j, v] for (i, j), v in Yv.items()], 'H': [[i, v] for i, v in Hv.items()],
          'counts': {'unit': nunit, 'cond': ncond, 'chain': nchain}}
    json.dump(mp, open(out + '.map.json', 'w'))
    print(json.dumps({k: mp[k] for k in ('m', 'K', 't', 'nv', 'ncl', 'counts')}))


main()
