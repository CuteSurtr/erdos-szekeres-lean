#!/usr/bin/env python3
"""Reviewer's stress test: evaluate chord-rule clauses (and, as a convention sanity check, the base encoding's
order/angle/nesting clauses over variables <= 5746) on random and adversarial real configurations, computed with
mpmath at 80 significant digits.

usage: stress.py SEED NCONF OUTLOG
Configuration: r_0 = 1, theta_0 = 0, theta_i in (0,60) deg distinct; radii chosen so that L_{i+1} lies strictly inside
conv(L_i) (nesting), except in mode 'nonmono' (arbitrary radii).
Point (i,k) = r_i (cos, sin)(theta_i + 60 k).  Triple variable v true iff orient(TRIPLE_OF[v]) > 0;
Y(i,j) = [theta_i < theta_j].  An orientation is trusted only if |orient| > 1e-60 * max |det| term scale; untrusted
literals are 'undetermined' (counted, never reported as violations).
Mode 'nonmono' uses unsorted radii (tests the lemma's 'no radius assumption' claim); only chord clauses are
evaluated there (base clauses assume nesting)."""
import sys, json, random, time
import mpmath as mp
from indep_enc import TRIPLE_OF, YINV, NTRIP, Y as YVAR

mp.mp.dps = 80
D = '<six10-work-dir>'


def readcl(fn, maxvar=None, limit=None):
    out = []
    with open(fn) as f:
        for n, line in enumerate(f):
            if line[0] in 'cp':
                continue
            l = list(map(int, line.split()))[:-1]
            if maxvar is not None and any(abs(x) > maxvar for x in l):
                continue
            out.append(l)
            if limit and len(out) >= limit:
                break
    return out


CHORD = readcl(D + '/main/chord_rules.clauses')
# base: order (168) + angle + nest families are the first 7709 clauses (encA_6_8_10.cnf.json 'ranges')
BASE = readcl(D + '/cegar/base/encA_6_8_10.cnf', maxvar=5746, limit=7709)


def tiny(rng, lo=-12, hi=-9):
    return 10 ** rng.uniform(lo, hi)


def gen(rng, mode):
    # phases (degrees, mpf)
    th = [mp.mpf(0)]
    if mode in ('uniform', 'multiscale'):
        th += [mp.mpf(rng.uniform(0, 60)) for _ in range(9)]
    elif mode == 'phase_cluster':
        c = rng.choice([mp.mpf(rng.uniform(0, 60)), mp.mpf(tiny(rng, -9, -6)), 60 - mp.mpf(tiny(rng, -9, -6))])
        for _ in range(9):
            th.append(c + (mp.mpf(rng.random()) - mp.mpf(0.5)) * mp.mpf(10) ** -rng.uniform(9, 12) * 2)
    else:   # phase_edge, mixed, nonmono
        for i in range(1, 10):
            c = rng.random()
            if c < 0.2:
                th.append(mp.mpf(tiny(rng, -12, -9)))
            elif c < 0.4:
                th.append(60 - mp.mpf(tiny(rng, -12, -9)))
            elif c < 0.7 and i > 1:
                b = th[rng.randrange(1, i)]
                th.append(b + rng.choice([-1, 1]) * mp.mpf(tiny(rng, -12, -9)))
            else:
                th.append(mp.mpf(rng.uniform(0, 60)))
    for i in range(1, 10):
        if not (0 < th[i] < 60):
            th[i] = mp.mpf(rng.uniform(1, 59))
    # radii: built AFTER the phases so that nesting holds: L_{i+1} strictly inside conv(L_i) iff
    # r_{i+1} < r_i * cos30 / cos(d_i), d_i = angular distance of theta_{i+1} from the edge-normal directions
    # theta_i + 30 + 60k (in [0,30]).  Ratios are drawn relative to that maximal ratio (tight / tiny / moderate).
    rs = [mp.mpf(1)]
    for i in range(9):
        x = (th[i + 1] - th[i] - 30) % 60
        d = min(x, 60 - x)
        mx = mp.cos(mp.radians(30)) / mp.cos(mp.radians(d))
        c = rng.random()
        if mode == 'uniform':
            f = mp.mpf(rng.uniform(0.01, 0.999))
        elif c < 0.35:
            f = mp.mpf(10) ** (-rng.uniform(6, 12))
        elif c < 0.7:
            f = 1 - mp.mpf(10) ** (-rng.uniform(9, 14))
        else:
            f = mp.mpf(rng.uniform(0.05, 0.999))
        rs.append(rs[-1] * mx * f)
    if mode == 'nonmono':
        rs = [mp.mpf(10) ** rng.uniform(-12, 12) for _ in range(10)]
        if rng.random() < 0.5:
            rs = [mp.mpf(10) ** rng.choice([-12, 0, 12]) * (1 + mp.mpf(rng.random()) * mp.mpf(10) ** -9) for _ in range(10)]
    if len(set(th)) < 10:
        return gen(rng, mode)
    return rs, th


SQ3H = mp.sqrt(3) / 2
# exact-constant cos / sin of 60*m degrees (no rounding error in the constants)
C60 = [mp.mpf(1), mp.mpf(1) / 2, -mp.mpf(1) / 2, mp.mpf(-1), -mp.mpf(1) / 2, mp.mpf(1) / 2]
S60 = [mp.mpf(0), SQ3H, SQ3H, mp.mpf(0), -SQ3H, -SQ3H]


def evaluate(rs, th, clauses):
    """orient(a,b,c) = sum_cyc det(a,b), det((i,k),(j,l)) = r_i r_j sin(d + 60 m), d = theta_j - theta_i (mpf
    subtraction, then sin(d) / cos(d) computed with full relative accuracy), m = l - k; expanded as
    r_i r_j (sin d cos60m + cos d sin60m) with exact-constant cos60m, sin60m.  Each summand is thus computed with
    relative error ~1e-78, so the sign is trusted iff |orient| > 1e-60 * max |summand|."""
    sd = {}
    for i in range(10):
        for j in range(10):
            d = mp.radians(th[j] - th[i])
            sd[(i, j)] = (mp.sin(d), mp.cos(d))
    cache = {}

    def tval(v):
        if v in cache:
            return cache[v]
        pts = [divmod(x, 6) for x in TRIPLE_OF[v]]
        terms = []
        for (i, k), (j, l) in zip(pts, pts[1:] + pts[:1]):
            s, c = sd[(i, j)]
            m = (l - k) % 6
            rr = rs[i] * rs[j]
            if C60[m] != 0 and s != 0:
                terms.append(rr * s * C60[m])
            if S60[m] != 0:
                terms.append(rr * c * S60[m])
        o = mp.fsum(terms)
        sc = max([abs(x) for x in terms] + [mp.mpf(10) ** -100000])
        if abs(o) <= sc * mp.mpf(10) ** -60:
            r = None
        else:
            r = o > 0
        cache[v] = r
        return r

    def lval(l):
        v = abs(l)
        if v <= NTRIP:
            x = tval(v)
        else:
            i, j = YINV[v]
            x = th[i] < th[j]
        if x is None:
            return None
        return x if l > 0 else (not x)

    viol = []; und = 0
    for cl in clauses:
        vals = [lval(l) for l in cl]
        if any(x is True for x in vals):
            continue
        if any(x is None for x in vals):
            und += 1
            continue
        viol.append(cl)
    return viol, und


if __name__ == '__main__':
    seed, nconf, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    modes = ['uniform', 'multiscale', 'phase_edge', 'phase_cluster', 'mixed', 'nonmono']
    stats = {m: {'configs': 0, 'chord_viol': 0, 'base_viol': 0, 'chord_undet': 0, 'base_undet': 0} for m in modes}
    t0 = time.time()
    with open(out, 'w') as log:
        for n in range(nconf):
            mode = modes[n % len(modes)]
            rs, th = gen(rng, mode)
            cv, cu = evaluate(rs, th, CHORD)
            st = stats[mode]; st['configs'] += 1; st['chord_viol'] += len(cv); st['chord_undet'] += cu
            if mode != 'nonmono':
                bv, bu = evaluate(rs, th, BASE)
                st['base_viol'] += len(bv); st['base_undet'] += bu
            else:
                bv = []
            if cv or bv:
                log.write(json.dumps({'mode': mode, 'chord_violations': cv[:20], 'base_violations': bv[:20],
                                      'r': [mp.nstr(x, 30) for x in rs], 'theta': [mp.nstr(x, 30) for x in th]}) + '\n')
                log.flush()
        log.write(json.dumps({'seed': seed, 'nconf': nconf, 'seconds': round(time.time() - t0, 1), 'stats': stats}) + '\n')
    print(json.dumps({'seed': seed, 'nconf': nconf, 'seconds': round(time.time() - t0, 1), 'stats': stats}))
