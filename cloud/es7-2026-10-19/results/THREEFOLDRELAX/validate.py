#!/usr/bin/env python3
"""Exact validation of the radius-ordered relaxation (gen_relax.py) for m = 3.

Points are lattice pairs (a, b) meaning z = a + b*w, w = exp(2 pi i/3).  All tests are exact integer arithmetic:
  orient sign      = sign of the lattice determinant (the map (a,b) -> z is linear with det > 0);
  |z|^2            = a^2 - a b + b^2;
  rotation by 2pi/3: (a,b) -> (-b, a-b);  rotation by pi/3: (a,b) -> (a-b, a);  reflection: (a,b) -> (a-b, -b).
The assignment is the real one (orbits in strictly decreasing radius, labels relative to a point of orbit 0), and
clauses are evaluated while being generated; chain variables get their least fixpoint (heads at level l+1 are
emitted before they are read), so a clause with no true literal and no fresh head is a real violation.

usage: validate.py FILE [--mirror] [--nest] [K]     (FILE: lines 'a b'; the centre 0 0 is dropped)
       validate.py random SEED NCONF               (adversarial random tests + brute force, K in {5,6,7})
"""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_relax as G

R3 = lambda p: (-p[1], p[0] - p[1])
R6 = lambda p: (p[0] - p[1], p[0])
MIR = lambda p: (p[0] - p[1], -p[1])
def cross(p, q): return p[0] * q[1] - p[1] * q[0]
def orient(p, q, r): return cross((q[0]-p[0], q[1]-p[1]), (r[0]-p[0], r[1]-p[1]))
def rad2(p): return p[0] * p[0] - p[0] * p[1] + p[1] * p[1]

def in_cone(p0, j, z):
    """angle(z) - angle(p0) in [j pi/3, (j+1) pi/3) ; exact"""
    a = p0
    for _ in range(j): a = R6(a)
    b = R6(a)
    return cross(a, z) >= 0 and cross(z, b) > 0

def sector(p0, z):
    hits = [j for j in range(6) if in_cone(p0, j, z)]
    assert len(hits) == 1, (p0, z, hits)
    return hits[0]

def label(points):
    """points: list of lattice pairs closed under R3, no centre. returns (pt[id], Y, H, info)"""
    pts = set(points)
    assert len(pts) == len(points), 'duplicate'
    orbits, seen = [], set()
    for p in points:
        if p in seen: continue
        o = [p, R3(p), R3(R3(p))]
        assert all(q in pts for q in o), 'not 3-fold invariant'
        seen.update(o); orbits.append(o)
    r = [rad2(o[0]) for o in orbits]
    assert len(set(r)) == len(r), 'two orbits share a radius'
    orbits = [o for _, o in sorted(zip(r, orbits), key=lambda x: -x[0])]
    p0 = orbits[0][0]
    pt, Jof = {}, {}
    for i, o in enumerate(orbits):
        for z in o:
            J = sector(p0, z)
            if i >= 1:
                a = p0
                for _ in range(J): a = R6(a)
                assert cross(a, z) != 0, 'non-generic phase (point collinear with O and a sector ray)'
            k = J // 2
            assert (i * 3 + k) not in pt
            pt[i * 3 + k] = z; Jof[i * 3 + k] = J
    t = len(orbits)
    H = {i: (Jof[i * 3] == 0) for i in range(1, t)}
    w = {}
    for i in range(t):
        z = pt[i * 3]
        for _ in range(5 * Jof[i * 3]): z = R6(z)   # rotate by -pi/3, J times
        assert sector(p0, z) == 0
        w[i] = z
    Y = {}
    for i in range(1, t):
        for j in range(i + 1, t):
            c = cross(w[i], w[j]); assert c != 0, 'equal psi'
            Y[(i, j)] = c > 0
    return pt, Y, H, t

class Val(G.Enc):
    def setup(self, pt, Y, H):
        self.val0 = {}
        for C, v in self.tvar.items():
            s = orient(*[pt[x] for x in C]); assert s != 0, 'collinear triple'
            self.val0[v] = s > 0
        for k, v in self.Y.items(): self.val0[v] = Y[k]
        for k, v in self.H.items(): self.val0[v] = H[k]
        self.truechain = set(); self.read = set(); self.fam = None; self.viol = {}
    def lv(self, l):
        v = abs(l)
        if v in self.val0: b = self.val0[v]
        else: b = v in self.truechain
        return b if l > 0 else not b
    def add(self, cl):
        self.ncls += 1
        if any(self.lv(l) for l in cl):
            for l in cl:
                if abs(l) not in self.val0 and l < 0: self.read.add(-l)
            return
        heads = [l for l in cl if l > 0 and l not in self.val0 and l not in self.read]
        if self.fam == 'chain' and len(heads) == 1:
            self.truechain.add(heads[0])
        else:
            self.viol[self.fam] = self.viol.get(self.fam, 0) + 1
        for l in cl:
            if abs(l) not in self.val0 and l < 0: self.read.add(-l)

def run(points, K, nest=False):
    pt, Y, H, t = label(points)
    E = Val(3, K, t); E.setup(pt, Y, H)
    for fam, f in (('order', E.fam_order), ('angle', E.fam_angle), ('nest', E.fam_nest if nest else None),
                   ('chain', E.fam_chain)):
        if f is None: continue
        E.fam = fam
        try:
            f()
        except RuntimeError as e:
            E.viol['nest-consistency'] = str(e)
    if os.environ.get('UNITS'):
        with open(os.environ['UNITS'], 'w') as f:
            for v, b in sorted(E.val0.items()): f.write('%d 0\n' % (v if b else -v))
    return t, E.ncls, E.viol

def convex_K(points, K):
    """brute force: is there a K-subset in convex position (general position assumed, exact)"""
    n = len(points)
    inside = set()
    for a, b, c in itertools.combinations(range(n), 3):
        s = orient(points[a], points[b], points[c])
        for d in range(n):
            if d in (a, b, c): continue
            P = points[d]
            s1, s2, s3 = orient(points[a], points[b], P), orient(points[b], points[c], P), orient(points[c], points[a], P)
            if (s1 > 0) == (s > 0) and (s2 > 0) == (s > 0) and (s3 > 0) == (s > 0):
                inside.add((frozenset((a, b, c)), d))
    for S in itertools.combinations(range(n), K):
        ok = True
        for d in S:
            for T in itertools.combinations([x for x in S if x != d], 3):
                if (frozenset(T), d) in inside: ok = False; break
            if not ok: break
        if ok: return True
    return False

def hull_layers(points):
    rest = list(points); layers = []
    while rest:
        h = [p for p in rest if not any(
            all(orient(T[i], T[(i+1) % 3], p) * orient(*T) > 0 for i in range(3))
            for T in itertools.combinations([q for q in rest if q != p], 3))] if len(rest) > 3 else rest[:]
        layers.append(h); rest = [p for p in rest if p not in h]
    return layers

def random_conf_band(rng, t):
    """t orbits, all radii in a narrow band [0.85, 1] * S, random phases: several orbits share the outer hull"""
    S = 10 ** 6; out = []
    import math
    for _ in range(t):
        r = S * rng.uniform(0.85, 1.0); th = rng.uniform(0, 2 * math.pi)
        x, y = r * math.cos(th), r * math.sin(th)
        p = (int(x + y / math.sqrt(3)), int(2 * y / math.sqrt(3)))   # lattice coords of (x, y)
        out += [p, R3(p), R3(R3(p))]
    return out

def random_conf(rng, t):
    """t orbits; orbit 1 is a near copy of orbit 0 rotated by about pi/3 (two orbits in one convex layer)"""
    S = 10 ** 6
    pts = []
    z = (rng.randint(S // 2, S), rng.randint(-S, S))
    pts.append(z)
    zz = R6(z); f = rng.uniform(0.80, 0.98)
    zz = (int(zz[0] * f) + rng.randint(-50, 50), int(zz[1] * f) + rng.randint(-50, 50))
    pts.append(zz)
    for _ in range(t - 2):
        f = rng.uniform(0.2, 0.99)
        a, b = rng.randint(-S, S), rng.randint(-S, S)
        pts.append((int(a * f), int(b * f)))
    out = []
    for p in pts: out += [p, R3(p), R3(R3(p))]
    return out

if __name__ == '__main__':
    if sys.argv[1] == 'random':
        rng = random.Random(int(sys.argv[2])); N = int(sys.argv[3]); band = '--band' in sys.argv
        stats = dict(conf=0, samelayer=0, nonchain_viol=0, agree=0, disagree=0, kgon=0, nest_viol=0, skipped=0)
        for it in range(N):
            t = rng.choice([3, 4, 5]); K = rng.choice([5, 6, 7, 8])
            P = (random_conf_band if band else random_conf)(rng, t)
            try:
                tt, ncl, viol = run(P, K)
            except AssertionError as e:
                stats['skipped'] += 1; continue
            stats['conf'] += 1
            L = hull_layers(P)
            orb = lambda p: frozenset([p, R3(p), R3(R3(p))])
            if any(len(set(orb(p) for p in lay)) >= 2 for lay in L): stats['samelayer'] += 1
            nc = sum(v for k, v in viol.items() if k != 'chain')
            stats['nonchain_viol'] += nc
            bf = convex_K(P, K); stats['kgon'] += bf
            if bf == (viol.get('chain', 0) > 0): stats['agree'] += 1
            else: stats['disagree'] += 1; print('DISAGREE', t, K, P, viol, bf)
            _, _, v2 = run(P, K, nest=True)
            if v2.get('nest', 0) or 'nest-consistency' in v2: stats['nest_viol'] += 1
        print(stats)
    else:
        fn = sys.argv[1]; K = 8
        for a in sys.argv[2:]:
            if a.isdigit(): K = int(a)
        P = []
        for line in open(fn):
            s = line.split()
            if len(s) >= 2:
                p = (int(s[0]), int(s[1]))
                if p != (0, 0): P.append(p)
        if '--mirror' in sys.argv: P = [MIR(p) for p in P]
        t, ncl, viol = run(P, K, nest='--nest' in sys.argv)
        L = hull_layers(P) if len(P) <= 30 else None
        print({'file': os.path.basename(fn), 'mirror': '--mirror' in sys.argv, 'nest': '--nest' in sys.argv,
               'K': K, 't': t, 'clauses': ncl, 'violations': viol})
