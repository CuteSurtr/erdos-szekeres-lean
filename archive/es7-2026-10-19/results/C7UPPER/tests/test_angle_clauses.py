#!/usr/bin/env python3
"""Targeted soundness test of the angular-rule clauses (family 'angle') of a gen.py CNF.

For every angle-family clause with a non-empty premise (Y/H literals), draw random real configurations whose
phases satisfy the premise (rejection sampling on the phases of the layers involved, other layers random) and random
radii (only the radii of the layers in the triple matter for the conclusion, but a full nested configuration is
built), and check that the conclusion (an orientation literal) holds.  Unit clauses are tested on random
configurations as well.  Independent of gen.py's sampler: phases are drawn uniformly, orientations computed from
coordinates.
usage: test_angle_clauses.py CNF samples_per_clause seed
"""
import sys, json, math, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import gen
from validate import orient_f


def main():
    cnf = sys.argv[1]; per = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
    meta = json.load(open(cnf + '.json'))
    m, K, t = meta['m'], meta['K'], meta['t']
    E = gen.Enc(m, K, t)
    inv = {v: C for C, v in E.tvar.items()}
    Yinv = {v: k for k, v in E.Y.items()}
    Hinv = {v: k for k, v in E.H.items()}
    a, b = meta['ranges']['angle']
    clauses = []
    with open(cnf) as f:
        f.readline()
        for idx, line in enumerate(f):
            if idx < a:
                continue
            if idx >= b:
                break
            clauses.append(list(map(int, line.split()))[:-1])
    unit = math.pi / m if m % 2 else 2 * math.pi / m
    sector = 2 * math.pi / m
    tested = 0; fails = 0; skipped = 0
    for cl in clauses:
        olits = [l for l in cl if abs(l) in inv]
        assert len(olits) == 1, cl
        ol = olits[0]
        C = inv[abs(ol)]
        prem = [-l for l in cl if abs(l) not in inv]     # premise literals must be true
        layers_needed = sorted(set(x // m for x in C))
        for s in range(per):
            # rejection sampling of phases for involved layers
            for attempt in range(2000):
                th = {0: 0.0}
                for L in layers_needed:
                    if L != 0:
                        th[L] = rng.uniform(0, sector)
                ok = True
                for l in prem:
                    v = abs(l)
                    if v in Yinv:
                        i, j = Yinv[v]
                        if i not in th or j not in th:
                            raise RuntimeError('premise on uninvolved layer')
                        val = (th[i] % unit) < (th[j] % unit)
                    else:
                        i = Hinv[v]
                        val = th[i] < math.pi / m
                    if val != (l > 0):
                        ok = False
                        break
                if ok:
                    break
            else:
                skipped += 1
                continue
            # radii: decreasing with layer index (only relative order matters for the rule; use random)
            rs = sorted([rng.uniform(0.05, 1.0) for _ in range(t)], reverse=True)
            pts = {}
            for x in C:
                i, k = divmod(x, m)
                ang = th[i] + 2 * math.pi * k / m
                pts[x] = (rs[i] * math.cos(ang), rs[i] * math.sin(ang))
            d = orient_f(pts[C[0]], pts[C[1]], pts[C[2]])
            if abs(d) < 1e-12:
                skipped += 1
                continue
            tested += 1
            if (d > 0) != (ol > 0):
                fails += 1
                if fails < 10:
                    print('FAIL', cl, C, th, rs)
    print(cnf, 'angle clauses', len(clauses), 'tests', tested, 'fails', fails, 'skipped', skipped)


main()
