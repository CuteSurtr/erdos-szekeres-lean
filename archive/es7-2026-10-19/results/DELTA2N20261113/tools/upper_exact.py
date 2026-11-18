#!/usr/bin/env python
"""Exact test of the UPPER-CHAIN statement U(a, n, m):
   every signotope on m points with no a-cap and no convex n-gon has a subset Delta with no (a-1)-cap that meets the
   CAP PART (upper chain, including its two end points) of every convex (n-1)-gon.
[With --lower: the cup part instead.  With --strong: Delta also contains no convex (n-1)-gon.]
This is stronger than D(a, n, m; weak): Delta must hit every gon at a vertex of its own upper chain.

CNF: base(a,n,m) + witnesses  Y_K -> K is an (a-1)-cap;   z_{U,B} -> U = (u, A, v) is a cap chain and (u, B, v) is a cup
chain (so U u B is a convex (n-1)-gon with upper chain U);   g_U -> OR_B z_{U,B};
and for EVERY subset Delta the clause   OR{Y_K : K inside Delta}  v  OR{g_U : U disjoint from Delta}.
Soundness as Lemma S: a valid signotope without such a Delta satisfies the CNF with all witnesses at their true values.
SAT answers are re-checked by enumeration.   usage: upper_exact.py a n m [--lower] [--strong] [--tl SEC] [--out DIR]"""
import sys, os, json, time, subprocess, itertools, argparse
from eager_cert import Enc, sha, CADICAL, CAKE, CAKE_OPTS, exact_sets, limit_as
comb = itertools.combinations

def build(a, n, m, lower, strong, endsonly=False):
    E = Enc(a, n, m, strong)
    tri = E.tri; cl = list(E.base) + list(E.wit); nv = E.nv
    chains = {}                       # the chain that Delta has to meet -> variable
    for u, v in comb(range(m), 2):
        inner = list(range(u + 1, v))
        for r in range(0, a - 2):                 # |A| = r, cap part has r + 2 <= a - 1 points
            k = n - 3 - r                         # |B|
            if k < 0 or r + k > len(inner): continue
            for A in comb(inner, r):
                rest = [x for x in inner if x not in A]
                U = (u,) + A + (v,)
                for B in comb(rest, k):
                    D = (u,) + B + (v,)
                    nv += 1; z = nv
                    for i in range(len(U) - 2): cl.append([-z, -tri[U[i], U[i + 1], U[i + 2]]])
                    for i in range(len(D) - 2): cl.append([-z, tri[D[i], D[i + 1], D[i + 2]]])
                    key = (u, v) if endsonly else (D if lower else U)
                    chains.setdefault(key, []).append(z)
    G = {}
    for key, zs in chains.items():
        nv += 1; G[key] = nv; cl.append([-nv] + zs)
    keys = list(G)
    for d in range(m + 1):
        for Dl in comb(range(m), d):
            Ds = set(Dl)
            c = [E.Y[K] for K in comb(Dl, E.b)] + [G[key] for key in keys if Ds.isdisjoint(key)]
            if strong: c += [E.Z[H] for H in comb(Dl, n - 1)]
            cl.append(c)
    return E, nv, cl

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('a', type=int); ap.add_argument('n', type=int); ap.add_argument('m', type=int)
    ap.add_argument('--lower', action='store_true'); ap.add_argument('--strong', action='store_true'); ap.add_argument('--ends', action='store_true')
    ap.add_argument('--tl', type=int, default=600); ap.add_argument('--out', default='upper')
    A = ap.parse_args(); a, n, m = A.a, A.n, A.m
    os.makedirs(A.out, exist_ok=True)
    tag = '%s_a%d_n%d_m%d%s' % ('endpair' if A.ends else ('lower' if A.lower else 'upper'), a, n, m, '_strong' if A.strong else '')
    cnf = os.path.join(A.out, tag + '.cnf'); lrat = os.path.join(A.out, tag + '.lrat'); log = os.path.join(A.out, tag + '.cadical.out')
    t0 = time.time(); E, nv, cl = build(a, n, m, A.lower, A.strong, A.ends)
    with open(cnf, 'w') as f:
        f.write('p cnf %d %d\n' % (nv, len(cl)))
        for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
    info = {'rule': 'end-pair' if A.ends else ('lower-chain' if A.lower else 'upper-chain'), 'a': a, 'n': n, 'm': m, 'form': 'strong' if A.strong else 'weak', 'vars': nv, 'clauses': len(cl),
            'cnf_sha256': sha(cnf), 'build_s': round(time.time() - t0, 1)}
    t = time.time(); keep_lrat = False
    with open(log, 'w') as f: r = subprocess.run([CADICAL, '-q', '-t', str(A.tl), '--lrat=true', '--binary=false', cnf, lrat], stdout=f, stderr=subprocess.STDOUT, preexec_fn=limit_as)
    info['cadical_exit'] = r.returncode; info['cadical_s'] = round(time.time() - t, 1)
    if r.returncode == 20:
        info['status'] = 'UNSAT'; info['lrat_bytes'] = os.path.getsize(lrat); info['lrat_sha256'] = sha(lrat); t = time.time()
        if info['lrat_bytes'] > 1500e6:
            info['cake_lpr'] = 'DEFERRED'; keep_lrat = True
        else:
            c = subprocess.run([CAKE] + CAKE_OPTS + [cnf, lrat], capture_output=True, text=True)
            info['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in c.stdout else ('FAILED: ' + (c.stdout + c.stderr)[-300:])
            info['cake_s'] = round(time.time() - t, 1)
    elif r.returncode == 10:
        info['status'] = 'SAT'
        lits = []
        for line in open(log):
            if line.startswith('v '): lits += [int(x) for x in line.split()[1:]]
        val = {abs(l): l > 0 for l in lits}
        o = {t_: val[v] for t_, v in E.tri.items()}
        info['model'] = ''.join('+' if o[t_] else '-' for t_ in comb(range(m), 3))
        caps, gons = exact_sets(E, o)
        parts = []
        for H in gons:
            u, v = H[0], H[-1]
            up = [u] + [x for x in H[1:-1] if not o[u, x, v]] + [v]; lo = [u] + [x for x in H[1:-1] if o[u, x, v]] + [v]
            parts.append([u, v] if A.ends else (lo if A.lower else up))
        from pysat.solvers import Glucose4
        with Glucose4() as s2:
            for K in caps: s2.add_clause([-(i + 1) for i in K])
            for P_ in parts: s2.add_clause([i + 1 for i in P_])
            if A.strong:
                for H in gons: s2.add_clause([-(i + 1) for i in H])
            ok = s2.solve()
        info['verdict'] = 'model has NO such Delta (exact re-check)' if not ok else 'ENCODING ERROR: such a Delta exists'
    else: info['status'] = 'UNKNOWN'
    if os.path.exists(lrat) and not keep_lrat: os.remove(lrat)
    if not keep_lrat and os.path.getsize(cnf) > 30e6: os.remove(cnf)
    info['total_s'] = round(time.time() - t0, 1)
    print(json.dumps(info), flush=True)
    with open(os.path.join(A.out, 'results.jsonl'), 'a') as f: f.write(json.dumps(info) + '\n')
if __name__ == '__main__':
    main()
