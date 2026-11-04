#!/usr/bin/env python3
"""RADIUS-ORDERED RELAXATION (threefold_relax): with --nonest, fam_nest is omitted and index i means the i-th
orbit in strictly decreasing radius (not a convex layer).  Everything else is byte-identical to C7UPPER/gen.py.

Compact CNF for: t nested regular m-gons (no centre), general position, no K points in convex position.

Points: (i, k), i = 0..t-1 layer (0 = outermost, radius r_0 > r_1 > ...), k = 0..m-1; angle theta_i + 2 pi k/m,
theta_0 = 0, theta_i in (0, 2pi/m) for i >= 1 (labelling convention: point (i,k) is the vertex of layer i whose angle
lies in [2 pi k/m, 2 pi (k+1)/m)).  id = i*m + k.  Rotation R: (i,k) -> (i,k+1).

Variables
  * one variable per rotation orbit of triples: V(C) = [orient(C) = +] for the canonical sorted triple C;
  * phase-order variables: psi_i = theta_i mod (pi/m) for odd m (theta_i mod 2pi/m for even m);
    Y(i,j) = [psi_i < psi_j] (i < j); psi_0 = 0 is the minimum; transitivity clauses;
  * odd m only: H(i) = [theta_i < pi/m]; H(0) = true;
  * chain variables for the "no convex K-gon" part (see below).

Sound clause families (each holds for every real configuration of nested regular m-gons in general position with
generic phases, plus the chain family which holds when there is no convex K-gon):
  (A) angular rules: for a triple of points the circular order of their directions and antipodes is a function of
      (psi-order, H) of the (at most 3) layers involved.  If O lies inside the triangle, orient = sign of the cyclic
      angular order.  If the triple lies in an open half-plane through O with angular order (a, b, c) and
      layer(b) <= layer(a), layer(c) (b is outermost), then orient(a, b, c) = + (b lies beyond the chord ac:
      polar formula + concavity of sin).
  (B) nesting: orient((i,k), (i,k+1), x) = + for every x in a layer j > i.
  (C) chains: for each layer i, pivot p = (i,0); Q = points of layers >= i except p (all strictly inside the
      tangent half-plane at p).  R_l(q,q') = there is a chain q_1..q_l = q' (q_{l-1} = q) with consecutive
      orient(p, q_s, q_{s+1}) = + and left turns at q_2..q_{l-1}.  A chain of K-1 points is a convex K-gon with p.
  (D) Grassmann-Pluecker 3-term relations: added lazily (gp clauses file; not used by the final certificate).

SOUNDNESS (written proof, not refereed).  Claim: if S is a set of t nested regular m-gons about O (no centre) in
general position with no K points in convex position, the CNF written by this program is satisfiable.
 0. Normalisation.  Nesting, general position and K-gon-freeness are strict inequalities in the parameters
    (r_i, theta_i), so they survive a small perturbation of the phases; hence WLOG the phases are generic:
    psi_i pairwise distinct, psi_i != 0 for i >= 1 (theta_i not in {0, pi/m}), so no point of S is collinear with O
    and another point (for odd m).  Rotate so that theta_0 = 0 and label (i,k) as in the header.  Radii strictly
    decrease with the layer index (L_j lies strictly inside conv(L_i) for j > i).
 1. Assignment.  Orbit variable := real orientation of its canonical triple (rotation preserves orientation, so
    one variable per orbit is consistent; the literal for an arbitrary ordered triple carries the permutation sign).
    Y, H := their real truth values; Y-transitivity holds.  Chain variables := least fixpoint of the implications.
 2. (A) Every direction of a point or antipode is psi_i + J pi/m with integer J determined by (k, H_i); the circular
    order of such directions is determined by J and the psi-order.  The angular configuration of a triple
    ('O strictly inside' vs 'open half-plane' + angular order) depends only on the circular order of its 3 points
    and 3 antipodes, hence only on the pattern of its layers; the program evaluates it at one representative
    phase vector per pattern.  O inside triangle abc => orient = cyclic angular order.  Half-plane with angular
    order a<b<c (angles alpha<beta<gamma, gamma-alpha<pi), u = 1/r: orient(a,b,c) = sign(u_a sin(gamma-beta)
    - u_b sin(gamma-alpha) + u_c sin(beta-alpha)) (polar formula, ES8SYM Lemma 1); if u_b <= u_a, u_c this is
    >= u_b (sin x + sin y - sin(x+y)) > 0 for x, y > 0, x+y < pi.  So every clause of (A) is true.
 3. (B) inner points lie strictly inside conv(L_i), i.e. strictly left of each ccw edge.
 4. (C) Q lies in the open half-plane bounded by the tangent at p to the circle of radius r_i (layer-i points
    other than p lie on that circle, inner points strictly inside conv(L_i)).  So orientation around p restricted to Q
    is the (strict, transitive) angular order of directions in an open half-plane.  If the least fixpoint violated a
    clause of (C), there would be q_1..q_{K-1} in Q with orient(p,q_s,q_{s+1}) = + and left turns at q_2..q_{K-2};
    the directions from p then increase monotonically within an arc < pi, all K turns of (p,q_1,..,q_{K-1}) are left
    turns (at q_1, q_{K-1} and p from the angular order) and the polygon is angularly monotone around its vertex p,
    hence simple, hence convex: K points of S in convex position, contradiction.
 5. Literal simplification uses only unit clauses that are themselves in the CNF.
 Completeness of (C) as an encoding of "no convex K-gon" (not needed for soundness): a convex K-gon P with
 outermost layer i has a vertex in L_i; a rotation maps it to p and P to a K-gon with vertices in layers >= i, whose
 other vertices in ccw order form a chain as above.
"""
import itertools, math, sys, json


class Enc:
    def __init__(self, m, K, t, rules=True):
        self.m, self.K, self.t = m, K, t
        self.n = m * t
        self.nv = 0
        self.cls = []
        self.rules = rules
        self.odd = (m % 2 == 1)
        # --- triple orbits
        self.canon = {}
        self.tvar = {}
        n = self.n
        for T in itertools.combinations(range(n), 3):
            best = None
            for s in range(m):
                rt = [self.rot(x, s) for x in T]
                srt, par = self.sortpar(rt)
                if best is None or srt < best[0]:
                    best = (srt, par)
            C = best[0]
            if C not in self.tvar:
                self.nv += 1
                self.tvar[C] = self.nv
            self.canon[T] = (C, best[1])
        self.ntriplevars = self.nv
        # --- phase vars
        self.Y = {}
        for i in range(1, t):
            for j in range(i + 1, t):
                self.nv += 1
                self.Y[(i, j)] = self.nv
        self.H = {}
        if self.odd:
            for i in range(1, t):
                self.nv += 1
                self.H[i] = self.nv
        self.forced = {}   # canonical var -> forced literal (unconditional)
        self.body = None
        self.ncls = 0

    # ---------------------------------------------------------------- basics
    def rot(self, x, s):
        i, k = divmod(x, self.m)
        return i * self.m + (k + s) % self.m

    @staticmethod
    def sortpar(lst):
        a = list(lst)
        par = 1
        for i in range(len(a)):
            for j in range(len(a) - 1 - i):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    par = -par
        return tuple(a), par

    def o(self, a, b, c):
        """literal for orient(a,b,c) = +"""
        T, s1 = self.sortpar((a, b, c))
        C, s2 = self.canon[T]
        v = self.tvar[C]
        return v if s1 * s2 > 0 else -v

    def ylit(self, i, j):
        """literal for psi_i < psi_j; returns True/False constants for layer 0"""
        if i == j:
            raise ValueError
        if i == 0:
            return True
        if j == 0:
            return False
        if i < j:
            return self.Y[(i, j)]
        return -self.Y[(j, i)]

    def hlit(self, i):
        if i == 0:
            return True
        return self.H[i]

    def add(self, cl):
        if self.body is not None:
            self.body.write(' '.join(map(str, cl)) + ' 0\n')
            self.ncls += 1
        else:
            self.cls.append(cl)
            self.ncls += 1

    # ---------------------------------------------------------------- families
    def fam_order(self):
        t = self.t
        for i, j, k in itertools.combinations(range(1, t), 3):
            a, b, c = self.Y[(i, j)], self.Y[(j, k)], self.Y[(i, k)]
            self.add([-a, -b, c])
            self.add([a, b, -c])

    def angle_config(self, pts, theta):
        """pts: 3 point ids.  returns ('in', sign) if O inside triangle with orient sign of (p0,p1,p2),
        ('half', (a,b,c)) angular order inside an open half-plane, or ('degenerate', None)."""
        m = self.m
        ang = []
        for x in pts:
            i, k = divmod(x, m)
            ang.append((theta[i] + 2 * math.pi * k / m) % (2 * math.pi))
        order = sorted(range(3), key=lambda r: ang[r])
        A = [ang[r] for r in order]
        gaps = [A[1] - A[0], A[2] - A[1], 2 * math.pi - (A[2] - A[0])]
        eps = 1e-9
        if any(abs(g - math.pi) < eps or g < eps for g in gaps):
            return ('degenerate', None)
        if max(gaps) < math.pi:
            # O inside; ccw order is order[0], order[1], order[2]
            perm = order
            # sign of permutation mapping (0,1,2) -> order
            _, par = self.sortpar(perm)
            return ('in', par)
        g = max(range(3), key=lambda r: gaps[r])
        # start after the largest gap
        start = (g + 1) % 3
        seq = [order[(start + r) % 3] for r in range(3)]
        return ('half', tuple(pts[r] for r in seq))

    def patterns(self, layers):
        """yield (literals, theta) for every psi-order / H pattern of the distinct layers"""
        m = self.m
        Ls = sorted(set(layers))
        unit = math.pi / m if self.odd else 2 * math.pi / m
        for perm in itertools.permutations(Ls):
            if 0 in Ls and perm[0] != 0:
                continue
            lits = []
            ok = True
            for a, b in zip(perm, perm[1:]):
                l = self.ylit(a, b)
                if l is False:
                    ok = False
                    break
                if l is not True:
                    lits.append(l)
            if not ok:
                continue
            nl = len(perm)
            psi = {}
            for r, L in enumerate(perm):
                if L == 0:
                    psi[L] = 0.0
                else:
                    psi[L] = unit * (r + (0 if 0 in Ls else 1)) / (nl + 1)
            if self.odd:
                hs = [L for L in Ls if L != 0]
                for bits in itertools.product([True, False], repeat=len(hs)):
                    th = {}
                    hl = []
                    for L, bt in zip(hs, bits):
                        th[L] = psi[L] + (0.0 if bt else math.pi / m)
                        hl.append(self.H[L] if bt else -self.H[L])
                    if 0 in Ls:
                        th[0] = 0.0
                    yield lits + hl, th
            else:
                th = dict(psi)
                yield lits, th

    def fam_angle(self):
        cnt = {'unit': 0, 'cond': 0}
        for C, v in self.tvar.items():
            layers = [x // self.m for x in C]
            outs = []
            for lits, th in self.patterns(layers):
                cfg = self.angle_config(C, th)
                lit = None
                if cfg[0] == 'in':
                    lit = v if cfg[1] > 0 else -v
                elif cfg[0] == 'half' and self.rules:
                    a, b, c = cfg[1]
                    la, lb, lc = a // self.m, b // self.m, c // self.m
                    if lb <= la and lb <= lc:
                        lit = self.o(a, b, c)
                outs.append((lits, lit))
            vals = set(l for _, l in outs)
            if len(vals) == 1 and None not in vals:
                lit = vals.pop()
                self.add([lit])
                self.forced[v] = lit
                cnt['unit'] += 1
            else:
                for lits, lit in outs:
                    if lit is not None:
                        self.add([-x for x in lits] + [lit])
                        cnt['cond'] += 1
        return cnt

    def fam_nest(self):
        m = self.m
        for i in range(self.t):
            for j in range(i + 1, self.t):
                for k in range(m):
                    lit = self.o(i * m + 0, i * m + 1, j * m + k)
                    self.add([lit])
                    if self.forced.get(abs(lit), lit) != lit:
                        raise RuntimeError('nesting contradicts angular rule')
                    self.forced[abs(lit)] = lit

    def val(self, lit):
        """constant value of a literal if forced, else None"""
        f = self.forced.get(abs(lit))
        if f is None:
            return None
        return (f == lit)

    def fam_chain(self):
        m, K, t = self.m, self.K, self.t
        L = K - 1          # chain length q_1..q_L
        stats = []
        for i in range(t):
            p = i * m
            Q = [x for x in range(i * m, t * m) if x != p]
            R = {}
            def rv(l, q, q2):
                key = (l, q, q2)
                if key not in R:
                    self.nv += 1
                    R[key] = self.nv
                return R[key]
            ncl = 0
            # possible ordered pairs
            pairs = []
            for q in Q:
                for q2 in Q:
                    if q == q2:
                        continue
                    lit = self.o(p, q, q2)
                    vv = self.val(lit)
                    if vv is False:
                        continue
                    pairs.append((q, q2, lit, vv))
            succ = {}
            for q, q2, lit, vv in pairs:
                succ.setdefault(q, []).append((q2, lit, vv))
            # level 2
            for q, q2, lit, vv in pairs:
                cl = [rv(2, q, q2)] + ([] if vv else [-lit])
                self.add(cl)
                ncl += 1
            for l in range(2, L):
                for q, q2, _, _ in pairs:
                    key = (l, q, q2)
                    if key not in R:
                        continue
                    for q3, lit2, vv2 in succ.get(q2, []):
                        if q3 == q:
                            continue
                        lt = self.o(q, q2, q3)
                        vt = self.val(lt)
                        if vt is False:
                            continue
                        cl = [-R[key]]
                        if not vv2:
                            cl.append(-lit2)
                        if not vt:
                            cl.append(-lt)
                        if l + 1 == L:
                            pass          # chain of L points: forbidden
                        else:
                            cl.append(rv(l + 1, q2, q3))
                        self.add(cl)
                        ncl += 1
            stats.append((i, len(Q), ncl))
        return stats

    def write(self, fn, extra=()):
        with open(fn, 'w') as f:
            f.write('p cnf %d %d\n' % (self.nv, len(self.cls) + len(extra)))
            for cl in self.cls:
                f.write(' '.join(map(str, cl)) + ' 0\n')
            for cl in extra:
                f.write(' '.join(map(str, cl)) + ' 0\n')


def build(m, K, t, rules=True, chain=True, body=None, nest=True):
    E = Enc(m, K, t, rules=rules)
    E.body = body
    E.ranges = {}
    a = E.ncls; E.fam_order(); E.ranges['order'] = (a, E.ncls)
    a = E.ncls; cnt = E.fam_angle(); E.ranges['angle'] = (a, E.ncls)
    a = E.ncls
    if nest:
        E.fam_nest()
    E.ranges['nest'] = (a, E.ncls)
    a = E.ncls; st = E.fam_chain() if chain else []; E.ranges['chain'] = (a, E.ncls)
    return E, cnt, st


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    nest = '--nonest' not in sys.argv
    m, K, t = int(args[0]), int(args[1]), int(args[2])
    out = args[3]
    import os
    body = open(out + '.body', 'w')
    E, cnt, st = build(m, K, t, body=body, nest=nest)
    body.close()
    with open(out, 'w') as f:
        f.write('p cnf %d %d\n' % (E.nv, E.ncls))
        with open(out + '.body') as g:
            while True:
                buf = g.read(1 << 24)
                if not buf:
                    break
                f.write(buf)
    os.remove(out + '.body')
    meta = {'m': m, 'K': K, 't': t, 'nv': E.nv, 'ncl': E.ncls, 'ntriple': E.ntriplevars,
            'Y': {'%d,%d' % k: v for k, v in E.Y.items()}, 'H': E.H, 'angle': cnt, 'chain': st,
            'ranges': E.ranges, 'nest': nest}
    json.dump(meta, open(out + '.json', 'w'))
    print(json.dumps({k: meta[k] for k in ('m', 'K', 't', 'nv', 'ncl', 'ntriple', 'angle', 'chain')}))
