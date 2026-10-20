#!/usr/bin/env python3
"""Mx controls and comparison with the results/C encoding (tools/etv/gen_etv.py, run as a
black box) on small cases.  Every UNSAT of an Mx CNF here gets a CaDiCaL LRAT proof checked
by lrat-check.  SAT models of Mx CNFs are decoded to x-sorted signotopes, re-checked by brute
force at the signotope level (axioms, mirror, cup/cap enumeration for convex k-gons) and fed
to the gen_etv --mirror CNF as orientation units; and vice versa."""
import sys, os, json, itertools, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mxgen, sigcheck
CAD = '/tmp/claude-0/sw/cadical/build/cadical'; LC = '/tmp/claude-0/sw/drat-trim/lrat-check'
ETV = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../tools/etv/gen_etv.py')
T = '/tmp/claude-0/mx/ctl'; os.makedirs(T, exist_ok=True)

def solve(path, lrat=False, seed=0, timeout=1800, units=()):
    if units:
        p2 = path + '.u.cnf'
        lines = open(path).read().split('\n')
        hdr = [i for i, l in enumerate(lines) if l.startswith('p cnf')][0]
        v, c = lines[hdr].split()[2:4]
        lines[hdr] = 'p cnf %s %d' % (v, int(c) + len(units))
        open(p2, 'w').write('\n'.join(l for l in lines if l) + '\n' + ''.join('%d 0\n' % u for u in units))
        path = p2
    cmd = [CAD, '-q', '--seed=%d' % seed, '-t', str(timeout)]
    if lrat: cmd += ['--lrat', '--binary=false', path, path + '.lrat']
    else: cmd += [path]
    t = time.time(); r = subprocess.run(cmd, capture_output=True, text=True); dt = time.time() - t
    st = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, 'UNKNOWN')
    model = []
    if st == 'SAT':
        for l in r.stdout.split('\n'):
            if l.startswith('v'): model += [int(x) for x in l.split()[1:] if x != '0']
    res = dict(status=st, sec=round(dt, 2))
    if lrat and st == 'UNSAT':
        o = subprocess.run([LC, path, path + '.lrat'], capture_output=True, text=True).stdout
        res['lrat'] = 'VERIFIED' if 'c VERIFIED' in o else 'NOT VERIFIED'
    if lrat and os.path.exists(path + '.lrat'): os.remove(path + '.lrat')
    if units: os.remove(path)
    return res, set(model)

def mx(n, k, mode, mirror=True):
    p = os.path.join(T, 'mx_%d_%d_%s%s.cnf' % (n, k, mode, '' if mirror else '_nm'))
    enc = mxgen.build(n, k, mirror, mode); mxgen.write(enc, p); return p, enc

def etv(n, k, hull):
    p = os.path.join(T, 'etv_%d_%d_%s.cnf' % (n, k, 'hm' if hull else 'm'))
    subprocess.run([sys.executable, ETV] + (['--hull'] if hull else []) + ['--mirror', '-o', p, str(n), str(k), str(k), str(k)],
                   capture_output=True, check=True)
    return p

def lexidx(n):
    return {t: i + 1 for i, t in enumerate(itertools.combinations(range(n), 3))}

def decode_mx(enc, model):
    return {t: (r in model) for t, r in enc['rep'].items() if len(t) == 3}

if __name__ == '__main__':
    out = []
    log = open(sys.argv[1], 'w')
    def rec(d):
        out.append(d); log.write(json.dumps(d) + '\n'); log.flush(); print(json.dumps(d), flush=True)
    # 1. required UNSAT controls, all modes, LRAT-checked
    for n, k in [(9, 5), (17, 6), (19, 6)]:
        for mode in ['none', 'all', 'top', 'interior']:
            p, enc = mx(n, k, mode); r, _ = solve(p, lrat=True)
            rec(dict(kind='control-unsat', n=n, k=k, mode=mode, vars=enc['nvars'], clauses=len(enc['clauses']), **r))
    # 2. non-mirror Erdos-Szekeres controls
    for n, k, exp in [(8, 5, 'SAT'), (9, 5, 'UNSAT'), (16, 6, 'SAT'), (17, 6, 'UNSAT')]:
        p, enc = mx(n, k, 'none', mirror=False); r, m = solve(p, lrat=(exp == 'UNSAT'), timeout=3000)
        d = dict(kind='control-nomirror', n=n, k=k, expected=exp, **r)
        if r['status'] == 'SAT':
            chi = decode_mx(enc, m); d['sigcheck'] = sigcheck.check(n, chi, k, mirror=False)
        rec(d)
    # 3. small-case agreement with results/C encodings + model cross-acceptance
    grid = [(5, 4), (7, 4), (7, 5), (9, 5), (9, 6), (11, 6), (13, 6), (15, 6), (13, 7), (15, 7), (17, 7),
            (19, 7), (21, 7), (23, 7), (25, 7)]
    for n, k in grid:
        row = dict(kind='compare', n=n, k=k)
        for mode in ['none', 'top', 'interior']:
            p, enc = mx(n, k, mode); r, m = solve(p, lrat=True, timeout=900)
            row['mx_' + mode] = r['status']; row['mx_%s_sec' % mode] = r['sec']
            if 'lrat' in r: row['mx_%s_lrat' % mode] = r['lrat']
            if mode == 'none':
                encN, pN = enc, p
        for hull in [False, True]:
            q = etv(n, k, hull); r, m = solve(q, timeout=900)
            row['C_' + ('hm' if hull else 'm')] = r['status']; row['C_%s_sec' % ('hm' if hull else 'm')] = r['sec']
        # cross acceptance (same frame: Mx 'none' vs C 'm'), up to 5 models each way
        if row['mx_none'] == 'SAT':
            L = lexidx(n); acc = []; chk = []
            for seed in range(5):
                r, m = solve(pN, seed=seed); chi = decode_mx(encN, m)
                chk.append(sigcheck.check(n, chi, k, mirror=True)['ok'])
                r2, _ = solve(q.replace('_hm', '_m'), units=[(L[t] if v else -L[t]) for t, v in chi.items()])
                acc.append(r2['status'])
            row['mx_models_sigcheck_ok'] = chk; row['mx_models_in_C_m'] = acc
            acc = []
            for seed in range(5):
                r, m = solve(q.replace('_hm', '_m'), seed=seed)
                units = [(r_ if (L[t] in m) else -r_) for t, r_ in encN['rep'].items() if len(t) == 3]
                chi = {t: (L[t] in m) for t in L}
                ok = sigcheck.check(n, chi, k, mirror=True)['ok']
                r2, _ = solve(pN, units=sorted(set(units)))
                acc.append((ok, r2['status']))
            row['C_models_sigcheck_ok_and_in_mx'] = acc
        rec(row)
    log.close()
