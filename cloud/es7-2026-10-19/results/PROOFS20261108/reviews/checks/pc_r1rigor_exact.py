"""Exact randomized tests of the written statements of section pc (angles in units of pi, pi := 1),
negative controls for the Fourier-Motzkin checker, the word table, and float tests of the
orientation rules exactly as transcribed in the written statements."""
import itertools, math, random, sys
from fractions import Fraction as F

sys.path.insert(0, '.')
import importlib.util
spec = importlib.util.spec_from_file_location('fmmod', 'pc_r1rigor_fm.py')

ok_all = True


def report(name, cond):
    global ok_all
    print(("OK   " if cond else "FAIL ") + name)
    if not cond:
        ok_all = False


# ------------------------------------------------ exact arc predicates (pi = 1, so 2 pi = 2)
def floor_div(x):
    return math.floor(x)


def inArc(s, g, th):
    # exists integer k with s < th + 2k < s + g
    k0 = math.floor((s - th) / 2) + 1          # smallest k with th + 2k > s
    return th + 2 * k0 < s + g


def hasA(al, be, de, s, g):
    return inArc(s, g, al + 1) or inArc(s, g, be + 1) or inArc(s, g, de + 1)


def H(al, be, de):
    return (hasA(al, be, de, al, be - al), hasA(al, be, de, be, de - be), hasA(al, be, de, de, al + 2 - de))


def Alt(al, be, de):
    h1, h2, h3 = H(al, be, de); return h1 and h2 and h3


def RB(al, be, de):
    h1, h2, h3 = H(al, be, de); return (not h1) and (not h2)


def RD(al, be, de):
    h1, h2, h3 = H(al, be, de); return (not h2) and (not h3)


def RA(al, be, de):
    h1, h2, h3 = H(al, be, de); return (not h3) and (not h1)


random.seed(7)


def rq(lo, hi, den):
    return F(random.randint(lo * den, hi * den), den)


# sanity of inArc against brute force over k
okb = True
for _ in range(4000):
    s, g, th = rq(-6, 6, 4), rq(-1, 3, 4), rq(-6, 6, 4)
    brute = any(s < th + 2 * k < s + g for k in range(-20, 21))
    if brute != inArc(s, g, th):
        okb = False
report("exact inArc agrees with brute force over k", okb)

# Lemma shift (a),(b)
oks = True
for _ in range(3000):
    s, g, th, n = rq(-5, 5, 6), rq(-1, 3, 6), rq(-5, 5, 6), random.randint(-3, 3)
    if inArc(s, g, th + 2 * n) != inArc(s, g, th) or inArc(s + 2 * n, g, th) != inArc(s, g, th):
        oks = False
report("Lemma shift (a),(b) on 3000 exact samples", oks)
# Lemma shift (c),(d): RunMidD(a,b,d) <=> RunMidB(b,d,a+2); RunMidA(a,b,d) <=> RunMidB(d,a+2,b+2), all reals
oks = True
for _ in range(3000):
    al, be, de = rq(-4, 4, 6), rq(-4, 4, 6), rq(-4, 4, 6)
    if RD(al, be, de) != RB(be, de, al + 2) or RA(al, be, de) != RB(de, al + 2, be + 2):
        oks = False
report("Lemma shift (c),(d) for arbitrary (unordered) triples, 3000 samples", oks)


def sorted_triples(N=6000, den=6):
    out = []
    while len(out) < N:
        al = rq(-3, 3, den)
        be = al + rq(0, 2, den)
        de = al + rq(0, 2, den)
        if al < be < de < al + 2:
            out.append((al, be, de))
    return out


T = sorted_triples()
nb = sum(1 for (al, be, de) in T if 1 in (be - al, de - be, al + 2 - de))
print("   (sorted samples:", len(T), "with some gap = pi:", nb, ")")

# Lemma empty (a)-(f)
okE = True
for (al, be, de) in T:
    h1, h2, h3 = H(al, be, de)
    if de - al <= 1 and (h1 or h2): okE = False
    if al + 2 - be <= 1 and (h2 or h3): okE = False
    if be + 2 - de <= 1 and (h3 or h1): okE = False
report("Lemma empty on sorted samples", okE)
# Lemma arc12
report("Lemma arc12 on sorted samples", all((H(*t)[0] or H(*t)[1]) for t in T if t[2] - t[0] > 1))
# Theorem alternating iff gaps < pi
report("Thm alternating iff all gaps < pi (incl. gap = pi cases)",
       all(Alt(*t) == (t[1] - t[0] < 1 and t[2] - t[1] < 1 and t[0] + 2 - t[2] < 1) for t in T))
# Remark alt-boundary: a gap = pi makes alternation fail
report("Remark alt-boundary: gap = pi => not Alternating", all(not Alt(*t) for t in T if 1 in (t[1] - t[0], t[2] - t[1], t[0] + 2 - t[2])))
# Prop exactly-one
oke = True
for (al, be, de) in T:
    if Alt(al, be, de):
        c1 = inArc(al, be - al, de + 1) and not inArc(al, be - al, al + 1) and not inArc(al, be - al, be + 1)
        c2 = inArc(be, de - be, al + 1) and not inArc(be, de - be, be + 1) and not inArc(be, de - be, de + 1)
        c3 = inArc(de, al + 2 - de, be + 1) and not inArc(de, al + 2 - de, al + 1) and not inArc(de, al + 2 - de, de + 1)
        if not (c1 and c2 and c3): oke = False
report("Prop exactly-one on sorted samples", oke)
# Theorem runB (with gap hypothesis) and failure without it
report("Thm runB: RunMidB iff d-a<pi when a+2pi-d != pi",
       all(RB(*t) == (t[2] - t[0] < 1) for t in T if t[0] + 2 - t[2] != 1))
ex = (F(0), F(1, 2), F(1))
report("Remark runB-example (0,pi/2,pi): RunMidB true, d-a<pi false", RB(*ex) and not (ex[2] - ex[0] < 1))
report("  ... and every sorted sample with d-a = pi has RunMidB", all(RB(*t) for t in T if t[2] - t[0] == 1))
# gap classification and its counterexample
def disj(t):
    al, be, de = t
    return ((be - al < 1 and de - be < 1 and al + 2 - de < 1), de - al < 1, al + 2 - be < 1, be + 2 - de < 1)
gen = [t for t in T if 1 not in (t[1] - t[0], t[2] - t[1], t[0] + 2 - t[2])]
report("Prop gaps: some disjunct (generic samples)", all(any(disj(t)) for t in gen))
report("Remark gaps (2): exactly one disjunct (all sorted samples where some holds)", all(sum(disj(t)) <= 1 for t in T))
cx = (F(0), F(1), F(3, 2))
report("Remark gaps (1): (0,pi,3pi/2) has all four disjuncts false", not any(disj(cx)))
# Theorem trichotomy and Remark runs
report("Thm trichotomy (i) on generic samples", all(Alt(*t) or RA(*t) or RB(*t) or RD(*t) for t in gen))
report("Thm trichotomy (ii) on all sorted samples", all((not Alt(*t)) or not (RA(*t) or RB(*t) or RD(*t)) for t in T))
report("Remark runs: H1 or H2 or H3 for every sorted sample (incl. gap = pi)", all(any(H(*t)) for t in T))
report("Remark runs: exactly one pattern on generic samples", all(sum([Alt(*t), RA(*t), RB(*t), RD(*t)]) == 1 for t in gen))

# ------------------------------------------------ negative controls for the FM checker
import pc_r1rigor_fm as fm  # runs its checks once more (prints), then we use its functions
from sympy import Integer
a, b, d = fm.a, fm.b, fm.d
P = Integer(1)
order = fm.order
report("FM negative control: order does not imply b-a<pi", not fm.implies(order, fm.lt(b - a, P)))
report("FM negative control: d-a<=pi does not imply d-a<pi", not fm.implies(order + [fm.le(d - a, P)], fm.lt(d - a, P)))
report("FM negative control: wrong m=1 for alpha+pi in empty (a) is rejected",
       not fm.not_in_arc_ok([fm.lt(a, b), fm.lt(b, d), fm.le(d - a, P)], a, b - a, a + P, 1))
report("FM negative control: arc12 case 1 with k=1 rejected",
       not fm.in_arc_ok(order + [fm.lt(P, d - a), fm.lt(b - a, P)], b, d - b, a + P, 1))

# ------------------------------------------------ word dichotomy
words = list(itertools.product([True, False], repeat=6))
prem = lambda s: all(s[(i + 3) % 6] == (not s[i]) for i in range(6))
altw = lambda s: all(s[(i + 1) % 6] == (not s[i]) for i in range(6))
runw = lambda s: any(s[i] and s[(i + 1) % 6] and s[(i + 2) % 6] for i in range(6))
good = [s for s in words if prem(s)]
report("word: 64 functions, 8 satisfy the premise", len(words) == 64 and len(good) == 8)
report("word: (i) and (ii) for all premise words", all((altw(s) or runw(s)) and not (altw(s) and runw(s)) for s in good))
tab = {('P', 'P', 'P'): ('PPPAAA', 0), ('P', 'P', 'A'): ('PPAAAP', 5), ('P', 'A', 'P'): ('PAPAPA', None),
       ('P', 'A', 'A'): ('PAAAPP', 4), ('A', 'P', 'P'): ('APPPAA', 1), ('A', 'P', 'A'): ('APAPAP', None),
       ('A', 'A', 'P'): ('AAPPPA', 2), ('A', 'A', 'A'): ('AAAPPP', 3)}
okt = True
for (x_, y_, z_), (w, i0) in tab.items():
    s = [c == 'P' for c in w]
    if [c == 'P' for c in (x_, y_, z_)] != s[:3] or not prem(s): okt = False
    if i0 is None:
        if not altw(s): okt = False
    else:
        if not (s[i0] and s[(i0 + 1) % 6] and s[(i0 + 2) % 6]): okt = False
report("word: the 8-row table (words, run positions, alternating rows)", okt)
s = [c == 'P' for c in 'PPAPPA']
report("word: PPAPPA violates premise, neither alternating nor run", (not prem(s)) and not altw(s) and not runw(s))

# ------------------------------------------------ float tests of the orientation rules as transcribed
def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def polar(c, r, t):
    return (c[0] + r * math.cos(t), c[1] + r * math.sin(t))


PI = math.pi
random.seed(11)
cnt = {'B': 0, 'D': 0, 'A': 0, 'alt': 0, 'phase': 0, 'sign+': 0, 'sign-': 0}
okr = True


def runs_f(al, be, de):
    # use exact predicates on angles rounded to rationals in units of pi
    return None


for _ in range(20000):
    c = (random.uniform(-3, 3), random.uniform(-3, 3))
    # rationals in units of pi so the exact pattern predicates apply
    al = F(random.randint(-24, 24), 12)
    be = al + F(random.randint(1, 23), 12)
    de = al + F(random.randint(1, 23), 12)
    if not (al < be < de < al + 2):
        continue
    ra_, rb_, rd_ = (random.uniform(0.05, 3) for _ in range(3))
    A_ = polar(c, ra_, float(al) * PI); B_ = polar(c, rb_, float(be) * PI); D_ = polar(c, rd_, float(de) * PI)
    o = orient(A_, B_, D_)
    g1, g2, g3 = be - al, de - be, al + 2 - de
    if Alt(al, be, de):
        cnt['alt'] += 1
        if not o > 0: okr = False
    if g3 != 1 and RB(al, be, de) and ra_ <= rb_ and rd_ <= rb_:
        cnt['B'] += 1
        if not o > 0: okr = False
    if g1 != 1 and RD(al, be, de) and rb_ <= rd_ and ra_ <= rd_:
        cnt['D'] += 1
        if not o > 0: okr = False
    if g2 != 1 and RA(al, be, de) and rb_ <= ra_ and rd_ <= ra_:
        cnt['A'] += 1
        if not o > 0: okr = False
    if 1 not in (g1, g2, g3):
        cA = (not RA(al, be, de)) or (rb_ <= ra_ and rd_ <= ra_)
        cB = (not RB(al, be, de)) or (ra_ <= rb_ and rd_ <= rb_)
        cD = (not RD(al, be, de)) or (rb_ <= rd_ and ra_ <= rd_)
        if cA and cB and cD:
            cnt['phase'] += 1
            if not o > 0: okr = False
report("rules A, B, D, A and phase (as transcribed) on random samples " + str(cnt), okr)

# sign theorem (ii) as transcribed: arbitrary beta, delta, reduced into [alpha, alpha+2pi)
oks2 = True
for _ in range(20000):
    c = (random.uniform(-3, 3), random.uniform(-3, 3))
    al = F(random.randint(-24, 24), 12)
    be0 = F(random.randint(-60, 60), 12); de0 = F(random.randint(-60, 60), 12)
    red = lambda t: t - 2 * math.floor((t - al) / 2)
    bp, dp = red(be0), red(de0)
    assert al <= bp < al + 2 and al <= dp < al + 2
    if bp == al or dp == al:
        continue
    ra_, rb_, rd_ = (random.uniform(0.05, 3) for _ in range(3))
    o = orient(polar(c, ra_, float(al) * PI), polar(c, rb_, float(be0) * PI), polar(c, rd_, float(de0) * PI))
    if bp < dp and bp - al != 1 and dp - bp != 1 and al + 2 - dp != 1:
        ok_ = ((not RA(al, bp, dp)) or (rb_ <= ra_ and rd_ <= ra_)) and ((not RB(al, bp, dp)) or (ra_ <= rb_ and rd_ <= rb_)) and ((not RD(al, bp, dp)) or (rb_ <= rd_ and ra_ <= rd_))
        if ok_:
            cnt['sign+'] += 1
            if not o > 0: oks2 = False
    if dp < bp and dp - al != 1 and bp - dp != 1 and al + 2 - bp != 1:
        ok_ = ((not RA(al, dp, bp)) or (rd_ <= ra_ and rb_ <= ra_)) and ((not RB(al, dp, bp)) or (ra_ <= rd_ and rb_ <= rd_)) and ((not RD(al, dp, bp)) or (rd_ <= rb_ and ra_ <= rb_))
        if ok_:
            cnt['sign-'] += 1
            if not o < 0: oks2 = False
report("Thm sign (i),(ii) as transcribed on random samples " + str({k: cnt[k] for k in ('sign+', 'sign-')}), oks2)

print("\nALL OK" if ok_all else "\nSOME CHECK FAILED")
