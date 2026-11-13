#!/usr/bin/env python3
"""EXACT checker (integer arithmetic only, stdlib) for a candidate realization of a hard-core sign pattern.
Input JSON: {"cube": ..., "layers": [...], "seeds": {"<layer>": [a, b], ...}}  with integers a, b: seed z_i = a + b*w,
w = exp(i pi/3).  Rotation by 60 deg is (a,b) -> (-b, a+b).  For points p=(pa,pb), q, r in oblique coordinates
(2/sqrt3) * orient(p,q,r) = sum over cyclic pairs (p_a q_b - p_b q_a)  (an integer).
Checks: (1) every point distinct, no zero orientation among ALL triples of the given layers (general position);
(2) every non-free canonical orbit triple inside the layers has the core's required sign;
(3) convention: radii strictly decreasing in layer index (exact |z|^2 = a^2 + ab + b^2), theta_0 = 0 (b_0 = 0, a_0 > 0),
    theta_i in (0, 60deg) for i >= 1 (a_i > 0, b_i > 0)  [reported, not required for (1),(2)];
optionally writes an orientation table (n, then n^3 signs) for cvx2.c / cvxcheck.c.
Usage: exact_check.py CAND.json [OTAB_PREFIX]"""
import sys, json, itertools, os, importlib.util
RES = os.environ.get('ES_RESULTS', '<results-dir>')
s = importlib.util.spec_from_file_location('enc', RES + '/C7UPPER/gen.py'); G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
E = G.Enc(6, 8, 10)


def rot(p, k):
    for _ in range(k % 6): p = (-p[1], p[0] + p[1])
    return p


def orient2(P, Q, R):
    v = 0
    for (pa, pb), (qa, qb) in ((P, Q), (Q, R), (R, P)): v += pa * qb - pb * qa
    return v


def main():
    cand = json.load(open(sys.argv[1])); layers = sorted(int(l) for l in cand['layers'])
    seeds = {int(k): (int(v[0]), int(v[1])) for k, v in cand['seeds'].items()}
    hm = json.load(open(RES + '/SIX10CEGAR/hard_models/cluster_%s.json' % cand['cube']))
    pos = set(hm['representative_true_vars']); free = set(hm['free_triple_vars'])
    pts = {6 * i + k: rot(seeds[i], k) for i in layers for k in range(6)}
    ids = sorted(pts)
    assert len(set(pts.values())) == len(ids), 'coincident points'
    zero = 0; bad = []; checked = 0; freeseen = {}
    for t in itertools.combinations(ids, 3):
        o = orient2(pts[t[0]], pts[t[1]], pts[t[2]])
        if o == 0: zero += 1; continue
        v = E.tvar.get(t)
        if v is None: continue          # non-canonical representative of an orbit: covered by its canonical triple
        if v in free: freeseen[v] = 1 if o > 0 else -1; continue
        checked += 1
        want = 1 if v in pos else -1
        if (1 if o > 0 else -1) != want: bad.append(v)
    r2 = {i: seeds[i][0] ** 2 + seeds[i][0] * seeds[i][1] + seeds[i][1] ** 2 for i in layers}
    conv = {'radii_decreasing': all(r2[a] > r2[b] for a, b in zip(layers, layers[1:])),
            'theta0_zero': (0 not in layers) or (seeds[0][1] == 0 and seeds[0][0] > 0),
            'theta_in_0_60': all(seeds[i][0] > 0 and seeds[i][1] > 0 for i in layers if i != 0)}
    out = {'cube': cand['cube'], 'layers': layers, 'points': len(ids), 'zero_orientations': zero,
           'canonical_records_checked': checked, 'wrong_records': len(bad), 'wrong_vars': bad[:50],
           'free_record_signs': freeseen, 'convention': conv,
           'PASS_pattern': zero == 0 and not bad}
    print(json.dumps(out, indent=1))
    if len(sys.argv) > 2:
        n = len(ids); idx = {x: j for j, x in enumerate(ids)}
        with open(sys.argv[2] + '.otab.txt', 'w') as f:
            f.write('%d\n' % n)
            for a in ids:
                row = []
                for b in ids:
                    for c in ids:
                        if a == b or b == c or a == c: row.append('0')
                        else:
                            o = orient2(pts[a], pts[b], pts[c]); row.append('1' if o > 0 else ('-1' if o < 0 else '0'))
                    f.write(' '.join(row) + '\n'); row = []
    return 0 if out['PASS_pattern'] else 1


if __name__ == '__main__': sys.exit(main())
