"""Template transport of a coupled core (discovery only).

For a refuted support S: solve with CaDiCaL LRAT, trace the original clauses the proof uses, keep the
state-dependent ones (positive / empty / domain / source tests), and enumerate every injective map
sigma: owners -> states for which each such clause is present or implied in sigma's CNF.  The same
refutation then refutes sigma's CNF, so image(sigma) is a valid demand-one row:
  positive (i,j,k): TT[s_i,s_j,s_k]                       (same clause)
  empty (u,v):      D(s_u -> s_v) empty                     (same clause)
  domain (u,v,a,b): (a,b) not in D(s_u -> s_v)             (same clause, or implied by empty(u,v))
  source (u,v):     height(s_u) <= height(S_u)              (implied by sigma's source clause + monotone)
"""
import json, os, subprocess, sys, time, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import STATES, N
import coupled
from coupled import TT, DIFF

def used_tests(S, workdir=os.path.join(HERE, 'lrat')):
    os.makedirs(workdir, exist_ok=True)
    cnf = coupled.CNF(S)
    h = hashlib.sha256(json.dumps(S).encode()).hexdigest()[:12]
    p = os.path.join(workdir, f'core_{h}.cnf'); q = p[:-4] + '.lrat'
    open(p, 'w').write(cnf.dimacs())
    r = subprocess.run(['cadical', '-q', '--lrat=true', '--binary=false', p, q], capture_output=True, text=True)
    if r.returncode != 20:
        return None, None
    m = len(cnf.clauses)
    hints = {}
    empty = None
    with open(q) as f:
        for line in f:
            t = line.split()
            if len(t) > 1 and t[1] == 'd':
                continue
            cid = int(t[0]); z = t.index('0', 1)
            lits = t[1:z]; hs = [int(x) for x in t[z + 1:-1]]
            hints[cid] = hs
            if not lits:
                empty = cid
    used = set(); stack = [empty]; seen = set()
    while stack:
        c = stack.pop()
        if c in seen: continue
        seen.add(c)
        if c <= m:
            used.add(c); continue
        stack.extend(abs(x) for x in hints.get(c, []))
    tests = sorted({cnf.tags[c - 1] for c in used if cnf.tags[c - 1] is not None})
    os.remove(q)
    return tests, {'cnf': p, 'original_clauses': m, 'used_original': len(used), 'tests': len(tests)}

def good(test, sig, S):
    kind = test[0]
    if kind == 'positive':
        _, i, j, k = test; return bool(TT[sig[i], sig[j], sig[k]])
    if kind == 'empty':
        _, u, v = test; return not DIFF[sig[u]][sig[v]]
    if kind == 'domain':
        _, u, v, a, b = test; return (a, b) not in DIFF[sig[u]][sig[v]]
    if kind == 'source':
        _, u, v = test; return STATES[sig[u]][0] <= STATES[S[u]][0]
    raise ValueError(test)

def scope(test):
    if test[0] == 'positive': return set(test[1:4])
    if test[0] == 'source': return {test[1]}
    return set(test[1:3])

def search(S, tests, limit=60.0, max_supports=100000):
    k = len(S)
    sc = [scope(t) for t in tests]
    checks = [[(t, s) for t, s in zip(tests, sc) if i in s] for i in range(k)]
    start = time.monotonic(); found = set(); st = {'nodes': 0, 'halted': None}
    sig = [None] * k
    def dfs(used, assigned):
        st['nodes'] += 1
        if time.monotonic() - start > limit:
            st['halted'] = 'time'; return
        if len(found) >= max_supports:
            st['halted'] = 'max'; return
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
                if all(good(t, sig, S) for t in ready): opts.append(v)
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
    dfs(set(), set())
    return [sorted(s) for s in found], {'complete': st['halted'] is None, 'nodes': st['nodes'],
                                        'seconds': round(time.monotonic() - start, 1)}

if __name__ == '__main__':
    S = json.loads(sys.argv[1])
    tests, info = used_tests(S)
    print(info, flush=True)
    sups, sinfo = search(S, tests, limit=float(sys.argv[2]) if len(sys.argv) > 2 else 60)
    print(len(sups), sinfo)
