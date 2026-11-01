#!/usr/bin/env python3
"""Check Mx CNFs against the realizable mirror-symmetric sets saved by task C (results/C/sets).
For each set: exact mirror check about x=0, x-sort, brute-force largest convex subset (bfgon),
and Mx CNF (mode none) evaluated by Horn least model: no-gon clauses hold iff L < k."""
import sys, os, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate
from fractions import Fraction
from math import lcm
def toint(P):
    P = [(Fraction(x), Fraction(y)) for x, y in P]; d = 1
    for x, y in P: d = lcm(d, x.denominator, y.denominator)
    P = [(int(x * d), int(y * d)) for x, y in P]
    if sorted(P) != sorted((-x, y) for x, y in P) and sorted(P) == sorted((x, -y) for x, y in P):
        P = [(y, x) for x, y in P]          # horizontal axis -> vertical
    return P
def parse(line):
    lab, P = parse0(line); return lab, toint(P)
def parse0(line):
    t = line.split()
    for i, tok in enumerate(t):
        try: n = int(tok)
        except ValueError: continue
        if 3 <= n <= 64 and len(t) - i - 1 >= 2 * n:
            v = t[i + 1:i + 1 + 2 * n]; return t[0], [(v[2*j], v[2*j+1]) for j in range(n)]
    v = t; return 'nolabel', [(v[2*j], v[2*j+1]) for j in range(len(v) // 2)]
out = []
for path, k, maxl in [(a.split(':')[0], int(a.split(':')[1]), int(a.split(':')[2])) for a in sys.argv[1:]]:
    for ln, line in enumerate(open(path)):
        if ln >= maxl or not line.strip(): break
        lab, P = parse(line); P = sorted(P); n = len(P); pert = False
        if len(set(x for x, _ in P)) < n and sorted(P) == sorted((-x, y) for x, y in P):
            # repeated x: mirror-symmetric perturbation x -> x*M + i (and its mirror); keeps symmetry
            # and all strict orientation signs (M large), see README "Distinct x"
            M = 10 ** 6; right = sorted(p for p in P if p[0] > 0); pert = True
            Q = [(x * M + i + 1, y * M) for i, (x, y) in enumerate(right)]
            P = sorted(Q + [(-x, y) for x, y in Q] + [(0, y * M) for x, y in P if x == 0])
            assert validate.gp_ok(P)
        sym = sorted(P) == sorted((-x, y) for x, y in P)
        L = int(subprocess.run([validate.BF], input='%d %s\n' % (n, ' '.join('%d %d' % p for p in P)),
                               capture_output=True, text=True).stdout)
        r = validate.check_group(((n, k), [dict(id=ln, fam=os.path.basename(path), P=P, L=L)]))[0] if (sym and n % 2 == 1) else None
        if sym and n % 2 == 0:
            # even n: no axis point; reuse the encoder directly (mode none), least model
            import mxgen
            enc = mxgen.build(n, k, True, 'none'); ch = validate.chi_of(P); val = [None] * (enc['nvars'] + 1); ok = True
            for t_, v in ch.items():
                rr = enc['rep'][t_]
                if val[rr] is None: val[rr] = v
                elif val[rr] != v: ok = False
            no = enc['norient']
            for v in range(no + 1, enc['nvars'] + 1): val[v] = False
            sat = lambda c: any((val[abs(x)] if x > 0 else not val[abs(x)]) for x in c)
            sigok = all(sat(c) for t_, c in enc['clauses'] if t_ == 'sig')
            for t_, c in enc['clauses']:
                if t_ == 'aux' and not val[c[-1]] and all((not val[abs(x)]) if x > 0 else val[abs(x)] for x in c[:-1]): val[c[-1]] = True
            nogon = all(sat(c) for t_, c in enc['clauses'] if t_ == 'gon')
            r = dict(n=n, k=k, L=L, nogon=nogon, err=([] if ok and sigok and nogon == (L < k) else ['mismatch']))
        d = dict(file=os.path.relpath(path), line=ln, label=lab, n=n, k=k, mirror_exact=sym, perturbed=pert, L=L,
                 mx_nogon=r and r['nogon'], err=r and r['err'], axis=r and r.get('axis'))
        out.append(d); print(json.dumps(d), flush=True)
