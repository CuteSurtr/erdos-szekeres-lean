"""Sample abstract FL(6,6) signotopes on n points with CaDiCaL seeds; verify by independent DP; record states.
usage: sample_fl.py <n> <seeds comma list> <out.jsonl> [what K]   (optional cardinality requirement as in fls.py)"""
import sys, os, json, itertools, subprocess, time
os.environ['ETV_A'] = '4'; os.environ['ETV_B'] = '4'
import etv_common as ec
import fls
n = int(sys.argv[1]); seeds = [int(x) for x in sys.argv[2].split(',')]; out = sys.argv[3]
what = sys.argv[4] if len(sys.argv) > 4 else 'none'; K = int(sys.argv[5]) if len(sys.argv) > 5 else 0
HERE = os.path.dirname(os.path.abspath(__file__))
w = fls.FL(6, 6, n)
if what != 'none': w.require(what, K)
cnf = os.path.join(HERE, 'tmp', f'sample_{n}_{what}{K}.cnf'); open(cnf, 'w').write(w.dimacs())
T = list(itertools.combinations(range(n), 3))
def states_from(sg):
    Em = {}; Ep = {}; st = []
    for v in range(n):
        f = [0] * 4
        for u in range(v):
            em = ep = 2
            for t in range(u):
                if sg[t, u, v] < 0: em = max(em, Em[t, u] + 1)
                else: ep = max(ep, Ep[t, u] + 1)
            Em[u, v] = em; Ep[u, v] = ep
            for c in range(em - 1): f[c] = max(f[c], ep - 1)
        st.append(ec.SINDEX[tuple(f)])
    return st
for seed in seeds:
    t0 = time.time()
    r = subprocess.run(['/usr/bin/cadical', '-q', f'--seed={seed}', '--phase=%d' % (seed % 2), cnf], capture_output=True, text=True)
    if r.returncode != 10: print('seed', seed, 'exit', r.returncode, flush=True); continue
    model = set()
    for line in r.stdout.splitlines():
        if line.startswith('v '):
            for tok in line.split()[1:]:
                x = int(tok)
                if x > 0: model.add(x)
    info = fls.check_model(6, 6, n, w.o, model)     # asserts signotope axioms; returns (mc, mu, gon, E, A, EuA, EnA)
    assert info[0] <= 5 and info[1] <= 5 and not info[2]
    sg = {t: (1 if w.o[t] in model else -1) for t in T}
    st = states_from(sg)
    # out-states = in-states of the x-reversed signotope (same signs on reversed index triples)
    sgr = {(n - 1 - k, n - 1 - j, n - 1 - i): sg[i, j, k] for (i, j, k) in T}
    str_ = states_from(sgr)
    assert len(set(st)) == n and len(set(str_)) == n
    sig = ''.join('+' if sg[t] > 0 else '-' for t in T)
    with open(out, 'a') as f:
        f.write(json.dumps({'n': n, 'seed': seed, 'what': what, 'K': K, 'info': info, 'in_states': st, 'out_states': str_[::-1], 'sig': sig}) + '\n')
    print('seed', seed, 'n', n, 'info', info, 'holes(in)', sorted(''.join(map(str, ec.STATES[i])) for i in range(70) if i not in set(st)), '%.0fs' % (time.time() - t0), flush=True)
os.remove(cnf)
