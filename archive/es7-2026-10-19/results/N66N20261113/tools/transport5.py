"""Template transport of a coupled core (discovery tooling; adapted from RES33N transport.py/shrink_tests.py).
For a refuted support S: CaDiCaL LRAT proof, trace the original clauses it uses, keep the state-dependent ones
(positive / empty / domain), shrink them while the CNF stays UNSAT, then enumerate every injective map
sigma: owners -> states for which each kept clause is present in (or implied by) sigma's CNF:
  positive (i,j,k):   TT[s_i,s_j,s_k]                  (same unit clause)
  empty (u,v):        D'(s_u -> s_v) empty             (same unit clause)
  domain (u,v,a,b):   (a,b) not in D'(s_u -> s_v)      (same clause, or implied by the empty clause)
The same refutation (static clauses are identical for equal n) then refutes sigma's CNF: image(sigma) is a
demand-one row."""
import json, os, subprocess, sys, time, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
import coupled5
from coupled5 import TT, DIFF
from etv_common import N

def used_tests(S, workdir=os.path.join(HERE, 'lrat')):
    os.makedirs(workdir, exist_ok=True)
    nv, nc, body = coupled5._static(len(S))
    dyn = coupled5.CNF(S, static=False)
    tags = [None] * nc + list(dyn.tags)
    p = os.path.join(workdir, f'core_{os.getpid()}.cnf'); q = p[:-4] + '.lrat'
    with open(p, 'w') as f:
        f.write(f'p cnf {nv} {nc + len(dyn.clauses)}\n' + body + ''.join(' '.join(map(str, c)) + ' 0\n' for c in dyn.clauses))
    r = subprocess.run(['cadical', '-q', '--lrat=true', '--binary=false', p, q], capture_output=True, text=True)
    if r.returncode != 20:
        return None, None
    m = len(tags); hints = {}; empty = None
    with open(q) as f:
        for line in f:
            t = line.split()
            if len(t) > 1 and t[1] == 'd': continue
            cid = int(t[0]); z = t.index('0', 1)
            lits = t[1:z]; hints[cid] = [int(x) for x in t[z + 1:-1]]
            if not lits: empty = cid
    used = set(); stack = [empty]; seen = set()
    while stack:
        c = stack.pop()
        if c in seen: continue
        seen.add(c)
        if c <= m: used.add(c); continue
        stack.extend(abs(x) for x in hints.get(c, []))
    tests = sorted({tags[c - 1] for c in used if tags[c - 1] is not None})
    os.remove(q); os.remove(p)
    return tests, {'original_clauses': m, 'used_original': len(used), 'tests': len(tests)}

def good(test, sig):
    kind = test[0]
    if kind == 'positive':
        _, i, j, k = test; return bool(TT[sig[i], sig[j], sig[k]])
    if kind == 'empty':
        _, u, v = test; return not DIFF[sig[u]][sig[v]]
    if kind == 'domain':
        _, u, v, a, b = test; return (a, b) not in DIFF[sig[u]][sig[v]]
    raise ValueError(test)

def scope(test):
    return set(test[1:4]) if test[0] == 'positive' else set(test[1:3])

def unsat_without(S, keep_tests, workdir=os.path.join(HERE, 'shrink')):
    os.makedirs(workdir, exist_ok=True)
    keep = set(map(tuple, keep_tests))
    p = os.path.join(workdir, f'{os.getpid()}.cnf')
    with open(p, 'w') as f: f.write(coupled5.fast_dimacs(S, keep))
    r = subprocess.run(['cadical', '-q', '-n', '-t', '60', p], capture_output=True)
    return r.returncode == 20

def shrink(S, tests):
    tests = list(tests)
    for kind in ('domain', 'empty', 'positive'):
        trial = [t for t in tests if t[0] != kind]
        if len(trial) < len(tests) and unsat_without(S, trial): tests = trial
    i = 0
    while i < len(tests):
        trial = tests[:i] + tests[i + 1:]
        if unsat_without(S, trial): tests = trial
        else: i += 1
    return tests

def search(S, tests, limit=60.0, max_supports=200000):
    k = len(S); sc = [scope(t) for t in tests]
    checks = [[(t, s) for t, s in zip(tests, sc) if i in s] for i in range(k)]
    start = time.monotonic(); found = set(); st = {'nodes': 0, 'halted': None}
    sig = [None] * k
    def dfs(used, assigned):
        st['nodes'] += 1
        if time.monotonic() - start > limit: st['halted'] = 'time'; return
        if len(found) >= max_supports: st['halted'] = 'max'; return
        if len(assigned) == k:
            found.add(frozenset(sig)); return
        best = None
        for i in range(k):
            if i in assigned: continue
            ready = [t for t, s in checks[i] if s - {i} <= assigned]
            opts = []
            for v in range(N):
                if v in used: continue
                sig[i] = v
                if all(good(t, sig) for t in ready): opts.append(v)
            sig[i] = None
            score = (len(opts), -len(ready))
            if best is None or score < best[0]: best = (score, i, opts)
            if not opts: return
        _, i, opts = best
        for v in opts:
            sig[i] = v
            dfs(used | {v}, assigned | {i})
            if st['halted']: break
        sig[i] = None
    dfs(frozenset(), frozenset())
    return [sorted(s) for s in found], {'complete': st['halted'] is None, 'nodes': st['nodes'],
                                        'seconds': round(time.monotonic() - start, 1)}

def run(S, transport_seconds=60):
    t0 = time.time()
    tests, info = used_tests(S)
    if tests is None: return None
    small = shrink(S, tests)
    sups, sinfo = search(S, small, limit=transport_seconds)
    return {'core': S, 'tests_used': len(tests), 'tests_min': len(small), 'tests': small,
            'supports': sups, 'search': sinfo, 'seconds': round(time.time() - t0, 1)}
