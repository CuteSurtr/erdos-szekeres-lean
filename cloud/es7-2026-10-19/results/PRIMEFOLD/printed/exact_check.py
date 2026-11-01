"""Independent re-check (written from scratch) of claim C-printed-(k-1)-fold.

Run:  python3 -I exact_check.py [OUTFILE.out]      (the log is written only when run as a script)

Everything that decides a sign is exact:
  * rational point sets use fractions.Fraction;
  * the SMQH 5-fold set lives in the field F = Q(sqrt5)(s), s = sqrt(10 + 2 sqrt5) > 0, where
    cos(2pi/5) = (sqrt5 - 1)/4 and sin(2pi/5) = s/4.  Elements are u + v*s with u, v in Q(sqrt5), and
    elements of Q(sqrt5) are a + b*sqrt5 with a, b rational.  Signs are decided by exact squaring.
  * as a second, independent method for the SMQH set, every orientation is also enclosed by
    rational interval arithmetic whose only non-exact steps are integer-sqrt bounds (outward rounding).
Convex position of a k-subset (general position assumed and checked) is decided in two different ways
from the exact sign table: (A) counting hull edges; (B) Caratheodory: no point inside a triangle of others.
"""
import itertools, math, sys
from fractions import Fraction as Fr

OUT = []
def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s); OUT.append(s)

# ----------------------------------------------------------------------------------------------
# generic orientation / convexity machinery
def sgn(x):
    return (x > 0) - (x < 0)

def build_sign_table(n, orient_sign):
    """orient_sign(i,j,k) for i<j<k -> -1/0/+1. Returns dict on sorted triples."""
    return {t: orient_sign(*t) for t in itertools.combinations(range(n), 3)}

def make_sg(table):
    def sg(a, b, c):
        # sign of (a,b,c) from the table of sorted triples, with permutation parity
        p = [a, b, c]; par = 1
        for i in range(3):
            for j in range(2 - i):
                if p[j] > p[j + 1]:
                    p[j], p[j + 1] = p[j + 1], p[j]; par = -par
        return par * table[tuple(p)]
    return sg

def convex_A(sub, sg):
    k = len(sub); edges = 0
    for i, j in itertools.combinations(sub, 2):
        side = None; ok = True
        for m in sub:
            if m == i or m == j:
                continue
            s = sg(i, j, m)
            if side is None:
                side = s
            elif s != side:
                ok = False; break
        edges += ok
    return edges == k

def convex_B(sub, sg):
    for m in sub:
        rest = [q for q in sub if q != m]
        for a, b, c in itertools.combinations(rest, 3):
            if sg(a, b, m) == sg(b, c, m) == sg(c, a, m):
                return False
    return True

def count_convex(n, sg, ks):
    res = {}
    for k in ks:
        ca = cb = 0
        for sub in itertools.combinations(range(n), k):
            a = convex_A(sub, sg); b = convex_B(sub, sg)
            if a != b:
                raise SystemExit(f'METHOD DISAGREEMENT on {sub}')
            ca += a
        res[k] = ca
    return res

def rat_orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def analyse_rational(name, P, ks):
    n = len(P)
    assert len(set(P)) == n, 'repeated point'
    vals = {t: rat_orient(P[t[0]], P[t[1]], P[t[2]]) for t in itertools.combinations(range(n), 3)}
    zeros = [t for t, v in vals.items() if v == 0]
    table = {t: sgn(v) for t, v in vals.items()}
    say(f'[{name}] n={n}; collinear triples: {len(zeros)}; min |orient| = {min(abs(v) for v in vals.values())}')
    if zeros:
        say(f'   collinear: {zeros[:10]}')
        return table, None
    cnt = count_convex(n, make_sg(table), ks)
    say(f'   convex k-subsets (methods A and B agree): {cnt}')
    return table, cnt

# ----------------------------------------------------------------------------------------------
# Part A: the k = 5 eight-point set (Wikipedia / Commons File:8-points-no-pentagon.svg)
say('=== Part A: k = 5, Eppstein 8-point figure ===')
svg_drawn = [(18, 18), (342, 18), (18, 342), (126, 99), (261, 126), (234, 261), (Fr('342.002'), 342), (99, 234)]
svg_drawn = [(Fr(x), Fr(y)) for x, y in svg_drawn]
svg_sym = [(Fr(342) if x == Fr('342.002') else x, y) for x, y in svg_drawn]

# exact 4-fold symmetry about (180,180): R(x,y) = (180-(y-180), 180+(x-180)) = (360-y, x)
R = lambda p: (360 - p[1], p[0])
S_sym = set(svg_sym)
say('symmetrized set closed under 90-degree rotation about (180,180):', all(R(p) in S_sym for p in svg_sym))
say('as-drawn set closed under the same rotation:', all(R(p) in set(svg_drawn) for p in svg_drawn))
# Hausdorff mismatch of the as-drawn set under R (exact)
def dist2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
hm = max(min(dist2(R(p), q) for q in svg_drawn) for p in svg_drawn)
diam2 = max(dist2(p, q) for p in svg_drawn for q in svg_drawn)
say(f'as-drawn: max over points of distance from R(p) to the set = sqrt({hm}) = {math.sqrt(hm):.6g};'
    f' relative to diameter {math.sqrt(diam2):.6g}: {math.sqrt(hm)/math.sqrt(diam2):.3g}')
# two nested squares
outer = [(Fr(18), Fr(18)), (Fr(342), Fr(18)), (Fr(342), Fr(342)), (Fr(18), Fr(342))]
inner = [(Fr(126), Fr(99)), (Fr(261), Fr(126)), (Fr(234), Fr(261)), (Fr(99), Fr(234))]
def is_square(Q):
    e = [(Q[(i + 1) % 4][0] - Q[i][0], Q[(i + 1) % 4][1] - Q[i][1]) for i in range(4)]
    # each edge vector is the previous one turned by +90 degrees: (dx,dy) -> (-dy,dx)
    return all(e[(i + 1) % 4] == (-e[i][1], e[i][0]) for i in range(4)) and e[0] != (0, 0)
say('outer quadruple is a square:', is_square(outer), '| inner quadruple is a square:', is_square(inner),
    '| union = symmetrized set:', set(outer) | set(inner) == S_sym)
# inner square strictly inside outer
say('inner square strictly inside outer square:', all(18 < x < 342 and 18 < y < 342 for x, y in inner))
tA1, cA1 = analyse_rational('SVG symmetrized (342.002 -> 342)', svg_sym, (3, 4, 5))
tA2, cA2 = analyse_rational('SVG as drawn (342.002)', svg_drawn, (3, 4, 5))
say('   symmetrized and as-drawn have identical orientation tables:', tA1 == tA2)

# Book figure (Eppstein 2018, Fig. 1.2): circle centres parsed from the page-3 content stream of the
# Cambridge excerpt PDF (tools/pdf_circles.py -> work/bookpdf/circles_p3.txt), in stream units.
book_parsed = [(Fr(53813, 20), Fr(1103, 2)), (Fr(34373, 20), Fr(1103, 2)), (Fr(34373, 20), Fr(3047, 2)),
               (Fr(53813, 20), Fr(3047, 2)), (Fr(47333, 20), Fr(1589, 2)), (Fr(784657, 400), Fr(1751, 2)),
               (Fr(817059, 400), Fr(2561, 2)), (Fr(48953, 20), Fr(2399, 2))]
# centres recomputed as (path start point x + radius 27), which avoids the 6-significant-digit rounding
# of the right-most Bezier end points (1961.64 / 2042.65 / 1988.64 / 2069.64 in the stream)
book_fixed = list(book_parsed)
book_fixed[5] = (Fr('1934.65') + 27, Fr(1751, 2))
book_fixed[6] = (Fr('2015.65') + 27, Fr(2561, 2))
for nm, B in (('book Fig 1.2 (parsed centres)', book_parsed), ('book Fig 1.2 (start-point centres)', book_fixed)):
    cx = sum(p[0] for p in B) / 8; cy = sum(p[1] for p in B) / 8
    RB = lambda p: (cx - (p[1] - cy), cy + (p[0] - cx))
    closed = all(RB(p) in set(B) for p in B)
    mis = max(min(math.sqrt(dist2(RB(p), q)) for q in B) for p in B)
    say(f'[{nm}] centroid ({float(cx)}, {float(cy)}); exactly 4-fold about centroid: {closed}; max mismatch {mis:.4g}'
        f' stream units (side 972)')
    analyse_rational(nm, B, (4, 5))
# similarity between the SVG set and the book set: book - c_book = diag(-3, 3) (svg - (180,180)) ?
cb = (sum(p[0] for p in book_fixed) / 8, sum(p[1] for p in book_fixed) / 8)
mapped = {(cb[0] - 3 * (x - 180), cb[1] + 3 * (y - 180)) for x, y in svg_sym}
say('book (start-point centres) == image of symmetrized SVG set under (x,y) -> (c - 3(x-180), c\' + 3(y-180)):',
    mapped == set(book_fixed))

# ----------------------------------------------------------------------------------------------
# Part B: the k = 6 SMQH 5-fold set, exact field arithmetic
say('')
say('=== Part B: k = 6, SMQH App. C Table 2 (5-fold, centre point) ===')

class Q5:
    """a + b*sqrt5, a, b rational"""
    __slots__ = ('a', 'b')
    def __init__(self, a, b=0):
        self.a = Fr(a); self.b = Fr(b)
    def __add__(s, o): return Q5(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return Q5(s.a - o.a, s.b - o.b)
    def __neg__(s): return Q5(-s.a, -s.b)
    def __mul__(s, o): return Q5(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def sign(s):
        sa, sb = sgn(s.a), sgn(s.b)
        if sb == 0: return sa
        if sa == 0: return sb
        if sa == sb: return sa
        d = s.a * s.a - 5 * s.b * s.b      # nonzero because sqrt5 is irrational
        assert d != 0
        return sa if d > 0 else sb
    def approx(s):
        return float(s.a) + float(s.b) * math.sqrt(5)

T = Q5(10, 2)                               # s^2 = 10 + 2 sqrt5

class Fe:
    """u + v*s, u, v in Q5, s = sqrt(10 + 2 sqrt5) > 0"""
    __slots__ = ('u', 'v')
    def __init__(self, u, v=None):
        self.u = u if isinstance(u, Q5) else Q5(u)
        self.v = v if v is not None else Q5(0)
    def __add__(s, o): return Fe(s.u + o.u, s.v + o.v)
    def __sub__(s, o): return Fe(s.u - o.u, s.v - o.v)
    def __neg__(s): return Fe(-s.u, -s.v)
    def __mul__(s, o): return Fe(s.u * o.u + s.v * o.v * T, s.u * o.v + s.v * o.u)
    def __eq__(s, o): return s.u == o.u and s.v == o.v
    def __hash__(s): return hash((s.u, s.v))
    def sign(s):
        su, sv = s.u.sign(), s.v.sign()
        if sv == 0: return su
        if su == 0: return sv
        if su == sv: return su
        d = (s.u * s.u - s.v * s.v * T).sign()   # nonzero because s is not in Q(sqrt5)
        assert d != 0
        return su if d > 0 else sv
    def approx(s):
        return s.u.approx() + s.v.approx() * math.sqrt(10 + 2 * math.sqrt(5))

C = Fe(Q5(Fr(-1, 4), Fr(1, 4)))             # cos(2pi/5) = (sqrt5 - 1)/4
Sn = Fe(Q5(0), Q5(Fr(1, 4)))                # sin(2pi/5) = s/4
ONE = Fe(1)
say('exact identity cos^2 + sin^2 = 1:', C * C + Sn * Sn == ONE)
say('sanity: cos(2pi/5) > 0, sin(2pi/5) > 0, cos(2pi/5) < 1/2:', C.sign() > 0, Sn.sign() > 0,
    (Fe(Fr(1, 2)) - C).sign() > 0, '| approx', C.approx(), Sn.approx())

def rho(p):
    x, y = p
    return (x * C - y * Sn, x * Sn + y * C)

gens = [(-12, -17), (-15, 2), (-13, 0)]
P = []; label = []
for gi, g in enumerate(gens):
    p = (Fe(g[0]), Fe(g[1]))
    orbit = []
    for j in range(5):
        orbit.append(p); p = rho(p)
    assert p == orbit[0], 'rho^5 != id on generator'
    # SMQH Table 2 numbering: points 1..5 = rho^(4), rho^(0), rho^(1), rho^(2), rho^(3) of (-12,-17);
    # 6..10 = rho^(0..4)(-15,2); 11..15 = rho^(0..4)(-13,0); 16 = (0,0)
    order = [4, 0, 1, 2, 3] if gi == 0 else [0, 1, 2, 3, 4]
    for j in order:
        P.append(orbit[j]); label.append(f'rho^{j}{g}')
P.append((Fe(0), Fe(0))); label.append('(0,0)')
n = len(P)
say('rho^5 = id on all generators (exact): True;  n =', n, '; distinct:', len(set(P)) == n)
say('set closed under rho (exact 5-fold symmetry about the origin):', all(rho(p) in set(P) for p in P))
say('centre point (0,0) included:', (Fe(0), Fe(0)) in set(P))

def fe_orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

detv = {t: fe_orient(P[t[0]], P[t[1]], P[t[2]]) for t in itertools.combinations(range(n), 3)}
tableB = {t: v.sign() for t, v in detv.items()}
nz = sum(1 for v in tableB.values() if v == 0)
say(f'exact signs: {len(tableB)} triples, zero orientations: {nz}')
absmin_t = min(detv, key=lambda t: abs(detv[t].approx()))
say(f'smallest |det| (float evaluation of the exact value): {abs(detv[absmin_t].approx()):.6f} at '
    f'{[label[i] for i in absmin_t]}')
bound = Fe(Fr(143, 100))
cert = all(((v if tableB[t] > 0 else -v) - bound).sign() > 0 for t, v in detv.items())
say('exact certificate |det| > 1.43 for all 560 triples:', cert)
bound2 = Fe(Fr(1434, 1000))
say('exact certificate |det| > 1.434 for all 560 triples:',
    all(((v if tableB[t] > 0 else -v) - bound2).sign() > 0 for t, v in detv.items()))

# --- second, independent method: rational interval enclosures with integer-sqrt bounds ---
N = 10 ** 50
G = 10 ** 70          # outward rounding grid
def out_lo(x): return Fr(math.floor(x * G), G)
def out_hi(x): return Fr(math.ceil(x * G), G)
class Iv:
    __slots__ = ('lo', 'hi')
    def __init__(s, lo, hi=None):
        s.lo = Fr(lo); s.hi = Fr(hi) if hi is not None else Fr(lo)
        assert s.lo <= s.hi
    def __add__(s, o): return Iv(s.lo + o.lo, s.hi + o.hi)
    def __sub__(s, o): return Iv(s.lo - o.hi, s.hi - o.lo)
    def __mul__(s, o):
        ps = [s.lo * o.lo, s.lo * o.hi, s.hi * o.lo, s.hi * o.hi]
        return Iv(out_lo(min(ps)), out_hi(max(ps)))
r5lo = Fr(math.isqrt(5 * N * N), N); r5hi = r5lo + Fr(1, N)
assert r5lo * r5lo <= 5 <= r5hi * r5hi
Tlo, Thi = 10 + 2 * r5lo, 10 + 2 * r5hi
slo = Fr(math.isqrt(math.floor(Tlo * N * N)), N)
shi = Fr(math.isqrt(math.ceil(Thi * N * N)) + 1, N)
assert slo * slo <= Tlo and shi * shi >= Thi and slo > 0
Ci = Iv((r5lo - 1) / 4, (r5hi - 1) / 4)
Si = Iv(slo / 4, shi / 4)
def rho_i(p):
    x, y = p
    return (x * Ci - y * Si, x * Si + y * Ci)
Pi = []
for gi, g in enumerate(gens):
    p = (Iv(g[0]), Iv(g[1])); orbit = []
    for j in range(5):
        orbit.append(p); p = rho_i(p)
    order = [4, 0, 1, 2, 3] if gi == 0 else [0, 1, 2, 3, 4]
    Pi += [orbit[j] for j in order]
Pi.append((Iv(0), Iv(0)))
agree = True; worst_width = Fr(0); minlo = None
for t in itertools.combinations(range(n), 3):
    a, b, c = (Pi[i] for i in t)
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if v.lo <= 0 <= v.hi:
        agree = False; say('interval contains 0 at', t); continue
    s = 1 if v.lo > 0 else -1
    if s != tableB[t]:
        agree = False; say('SIGN MISMATCH interval vs exact at', t)
    m = v.lo if s > 0 else -v.hi
    minlo = m if minlo is None or m < minlo else minlo
    worst_width = max(worst_width, v.hi - v.lo)
say(f'rational-interval method: all 560 intervals exclude 0 and agree with exact signs: {agree}; '
    f'min |det| lower bound {float(minlo):.6f}; widest interval {float(worst_width):.2e}')

sgB = make_sg(tableB)
cntB = count_convex(n, sgB, (4, 5, 6))
say(f'[SMQH Table 2 exact] convex k-subsets (methods A and B agree): {cntB}')

# --- Mackey Fig. 3.33 as printed (6 decimals), exact rational arithmetic ---
mackey = """-19.876200 6.159400
-12.000000 -17.000000
12.459800 -16.666000
19.700600 6.699900
-0.284100 20.806700
-15.000000 2.000000
-6.537400 -13.647800
10.959700 -10.434800
13.310800 7.198700
-2.733100 14.883900
-13.000000 0.000000
-4.017200 -12.363700
10.517200 -7.641200
10.517200 7.641200
-4.017200 12.363700
0.000000 0.000000"""
M = [tuple(Fr(t) for t in line.split()) for line in mackey.strip().splitlines()]
dev = max(max(abs(float(M[i][0]) - P[i][0].approx()), abs(float(M[i][1]) - P[i][1].approx())) for i in range(n))
say(f'Mackey Fig 3.33 point i vs SMQH Table 2 point i: max coordinate deviation {dev:.3g} (6-decimal rounding)')
tM, cM = analyse_rational('Mackey Fig 3.33 as printed', M, (4, 5, 6))
say('   Mackey printed set has the same orientation table as the exact SMQH set (index-matched):', tM == tableB)
# rotation mismatch of Mackey printed set
c72, s72 = math.cos(2 * math.pi / 5), math.sin(2 * math.pi / 5)
Mf = [(float(x), float(y)) for x, y in M]
mm = max(min(math.hypot(x * c72 - y * s72 - u, x * s72 + y * c72 - w) for u, w in Mf) for x, y in Mf)
say(f'   Mackey printed set: max |rho(p) - nearest point| = {mm:.3g} (diameter ~ {max(math.hypot(a[0]-b[0], a[1]-b[1]) for a in Mf for b in Mf):.4g})')

# ----------------------------------------------------------------------------------------------
# Part C: is Wikipedia's other figure (File:16nohexagon.svg, 2022) rotationally symmetric? (context only)
say('')
say('=== Part C (context): Wikipedia File:16nohexagon.svg ===')
w16 = [(19.0, 195.0), (254.0, 21.0), (490.0, 196.0), (401.0, 475.0), (110.0, 478.0), (250.91, 273.5),
       (117.02, 351.74), (405.12, 378.42), (272.43, 140.14), (91.92, 243.27), (413.49, 319.73), (228.64, 214.02),
       (256.28, 93.63), (116.17, 283.71), (245.37, 234.68), (407.52, 336.4)]
W = [(Fr(str(x)), Fr(str(y))) for x, y in w16]
analyse_rational('Wikipedia 16nohexagon.svg', W, (6,))
# best rotation-symmetry mismatch for orders 2..8 (centre = centroid, then a small local search)
def rot_mismatch(pts, order, c):
    th = 2 * math.pi / order; co, si = math.cos(th), math.sin(th)
    return max(min(math.hypot(c[0] + (x - c[0]) * co - (y - c[1]) * si - u, c[1] + (x - c[0]) * si + (y - c[1]) * co - w)
                   for u, w in pts) for x, y in pts)
cen = (sum(p[0] for p in w16) / 16, sum(p[1] for p in w16) / 16)
diam = max(math.hypot(a[0] - b[0], a[1] - b[1]) for a in w16 for b in w16)
res = {}
for order in range(2, 9):
    best = rot_mismatch(w16, order, cen)
    for dx in range(-40, 41, 2):
        for dy in range(-40, 41, 2):
            best = min(best, rot_mismatch(w16, order, (cen[0] + dx, cen[1] + dy)))
    res[order] = round(best / diam, 3)
say('   best relative rotation mismatch by order (0 = symmetric):', res)

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1].endswith('.out'):
    open(sys.argv[1], 'w').write('\n'.join(OUT) + '\n')
