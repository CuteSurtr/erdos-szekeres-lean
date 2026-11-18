#!/usr/bin/env python
"""Exact test of the ONE-LEVEL THRESHOLD RULE on all signotopes with m points (pure existential SAT, with LRAT + cake_lpr).

Rule T(a, n): for a signotope S with no a-cap and no convex n-gon let
     L = {p : p starts an (a-1)-cap of S},  R = {p : p ends an (a-1)-cap of S},
     Delta_x = {p < x : p not in R}  u  {p >= x : p not in L}          (x = 0..m; positions 0..m-1).
Claim tested: for some x, Delta_x contains no (a-1)-cap and meets every convex (n-1)-gon of S.

CNF G(a,n,m): base(a,n,m) + exact definitions of s_p (p in L), e_p (p in R) + for EVERY x a clause
"Delta_x fails" over witness variables.  G satisfiable <=> some valid signotope on m points defeats every threshold.
usage: thr_exact.py a n m [--tl SEC] [--nocert] [--out DIR]
"""
import sys, os, json, time, subprocess, itertools, argparse
from eager_cert import Enc, sha, CADICAL, CAKE, CAKE_OPTS, limit_as
comb = itertools.combinations

def build(a, n, m):
    E = Enc(a, n, m, False)          # base + witness vars Y (b = a-1 caps), Q4, Z
    tri = E.tri; b = a - 1
    cl = list(E.base) + list(E.wit)
    nv = E.nv
    # exact cap indicators for b-subsets: X[K] <-> K is a b-cap
    X = {}
    if b == 3:
        for K in comb(range(m), 3): X[K] = -tri[K]
    else:
        for K in comb(range(m), b):
            nv += 1; X[K] = nv
            ts = [tri[K[i], K[i + 1], K[i + 2]] for i in range(b - 2)]
            for t in ts: cl.append([-nv, -t])
            cl.append([nv] + ts)
    # s_p <-> p starts a b-cap ; e_p <-> p ends a b-cap  (exact)
    s = {}; e = {}
    for p in range(m):
        nv += 1; s[p] = nv
        Ks = [K for K in comb(range(p, m), b) if K[0] == p]
        cl.append([-nv] + [X[K] for K in Ks])
        for K in Ks: cl.append([nv, -X[K]])
        nv += 1; e[p] = nv
        Ks = [K for K in comb(range(0, p + 1), b) if K[-1] == p]
        cl.append([-nv] + [X[K] for K in Ks])
        for K in Ks: cl.append([nv, -X[K]])
    def inlit(x, p):               # literal that is true iff p in Delta_x
        return -e[p] if p < x else -s[p]
    for x in range(m + 1):
        big = []
        for K in comb(range(m), b):
            if not (K[0] < x <= K[-1]): continue      # a b-cap inside Delta_x starts left of x and ends at/after x
            nv += 1; big.append(nv)
            cl.append([-nv, E.Y[K]])
            for p in K: cl.append([-nv, inlit(x, p)])
        for G in comb(range(m), n - 1):
            nv += 1; big.append(nv)
            cl.append([-nv, E.Z[G]])
            for p in G: cl.append([-nv, -inlit(x, p)])
        cl.append(big)
    return E, nv, cl, s, e

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('a', type=int); ap.add_argument('n', type=int); ap.add_argument('m', type=int)
    ap.add_argument('--tl', type=int, default=3600); ap.add_argument('--nocert', action='store_true'); ap.add_argument('--out', default='thr')
    A = ap.parse_args(); a, n, m = A.a, A.n, A.m
    os.makedirs(A.out, exist_ok=True); tag = 'thr_a%d_n%d_m%d' % (a, n, m)
    cnf = os.path.join(A.out, tag + '.cnf'); lrat = os.path.join(A.out, tag + '.lrat'); log = os.path.join(A.out, tag + '.cadical.out')
    t0 = time.time(); E, nv, cl, s, e = build(a, n, m)
    with open(cnf, 'w') as f:
        f.write('p cnf %d %d\n' % (nv, len(cl)))
        for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
    info = {'rule': 'threshold-1', 'a': a, 'n': n, 'm': m, 'vars': nv, 'clauses': len(cl), 'cnf_sha256': sha(cnf), 'build_s': round(time.time() - t0, 1)}
    t = time.time()
    cmd = [CADICAL, '-q', '-t', str(A.tl)] + ([] if A.nocert else ['--lrat=true', '--binary=false']) + [cnf] + ([] if A.nocert else [lrat])
    with open(log, 'w') as f: r = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, preexec_fn=limit_as)
    info['cadical_exit'] = r.returncode; info['cadical_s'] = round(time.time() - t, 1)
    if r.returncode == 20:
        info['status'] = 'UNSAT'
        if not A.nocert:
            info['lrat_bytes'] = os.path.getsize(lrat); info['lrat_sha256'] = sha(lrat); t = time.time()
            c = subprocess.run([CAKE] + CAKE_OPTS + [cnf, lrat], capture_output=True, text=True)
            info['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in c.stdout else ('FAILED: ' + (c.stdout + c.stderr)[-300:])
            info['cake_s'] = round(time.time() - t, 1)
    elif r.returncode == 10:
        info['status'] = 'SAT'
        lits = []
        for line in open(log):
            if line.startswith('v '): lits += [int(v) for v in line.split()[1:]]
        val = {abs(l): l > 0 for l in lits}
        info['model'] = ''.join('+' if val[E.tri[t]] else '-' for t in comb(range(m), 3))
    else: info['status'] = 'UNKNOWN'
    if os.path.exists(lrat): os.remove(lrat)
    if os.path.getsize(cnf) > 30e6: os.remove(cnf)
    info['total_s'] = round(time.time() - t0, 1)
    print(json.dumps(info), flush=True)
    with open(os.path.join(A.out, 'results.jsonl'), 'a') as f: f.write(json.dumps(info) + '\n')

if __name__ == '__main__':
    main()
