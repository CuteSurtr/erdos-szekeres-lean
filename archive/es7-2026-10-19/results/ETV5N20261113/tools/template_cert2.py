"""Justify every row of a subset (rows.json) for the final bound.
  cycle rows  : a list order passing the six-order test (demand = len - 7)
  block rows  : Baek family check (demand = len - 22)
  coupled rows: either a cake_lpr-certified core CNF (full CNF of the support), or a transported row:
                an explicit injective map sigma (core index -> state) with image = the row, compatible with a
                template's kept tests, where the template CNF (static(n) + kept clauses of the core) is itself
                cake_lpr-certified UNSAT.  Then sigma's CNF contains (or implies, for domain tests) every clause
                of the refuted template CNF, so it is UNSAT and the row is valid (README §2, Transport).
usage: template_cert.py <rows.json> <outdir> [procs]
Writes outdir/justification.json and outdir/template_certs.jsonl, outdir/core_certs.jsonl."""
import json, os, sys, hashlib, subprocess, itertools, time
from multiprocessing import Pool
import etv_common as ec
from etv_common import N
import coupled5, transport5
from cycle_order import order, check_list
CAKE = os.path.expanduser('~/.local/bin/cake_lpr')
rowsfile, od = sys.argv[1], sys.argv[2]; procs = int(sys.argv[3]) if len(sys.argv) > 3 else 1
os.makedirs(od, exist_ok=True)
rows = [(tuple(sorted(s)), d) for s, d in json.load(open(rowsfile))]
cores = set(tuple(sorted(json.loads(l)['support'])) for l in open('cores.jsonl'))
tr = {}
for l in open('trows.jsonl'):
    r = json.loads(l); tr.setdefault(tuple(sorted(r['support'])), tuple(r['core']))
tmpls = {}
for l in open('templates.jsonl'):
    r = json.loads(l)
    if r.get('tests') is None: continue
    tmpls.setdefault(tuple(r['core']), [])
    t = [tuple(x) for x in r['tests']]
    if t not in tmpls[tuple(r['core'])]: tmpls[tuple(r['core'])].append(t)

def block_ok(S):
    for K in itertools.combinations(range(1, ec.A + 1), 2):
        if all(z[0] in K for s, t in itertools.permutations(S, 2) for z in ec.DREF[s][t]): return True
    return False

def find_sigma(core, tests, image):
    """MRV backtracking for an injective sigma: index -> image state with all tests good; None if none."""
    k = len(core); img = sorted(image)
    sc = [transport5.scope(t) for t in tests]
    checks = [[(t, s) for t, s in zip(tests, sc) if i in s] for i in range(k)]
    sig = [None] * k
    def dfs(assigned, used):
        if len(assigned) == k: return True
        best = None
        for i in range(k):
            if i in assigned: continue
            ready = [t for t, s in checks[i] if s - {i} <= assigned]
            opts = []
            for v in img:
                if v in used: continue
                sig[i] = v
                if all(transport5.good(t, sig) for t in ready): opts.append(v)
            sig[i] = None
            if not opts: return False
            if best is None or (len(opts), -len(ready)) < best[0]: best = ((len(opts), -len(ready)), i, opts)
        _, i, opts = best
        for v in opts:
            sig[i] = v
            if dfs(assigned | {i}, used | {v}): return True
        sig[i] = None
        return False
    return list(sig) if dfs(frozenset(), frozenset()) else None

def template_cnf(core, tests):
    nv, nc, body = coupled5._static(len(core))
    dyn = coupled5.CNF(list(core), static=False)
    keep = set(tests)
    cls = [c for c, t in zip(dyn.clauses, dyn.tags) if t in keep]
    missing = keep - set(t for t in dyn.tags if t is not None)
    assert not missing, ('test not present in core CNF', list(missing)[:3])
    return f'p cnf {nv} {nc + len(cls)}\n' + body + ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls)

def lrat_check(txt, tag):
    h = hashlib.sha256(txt.encode()).hexdigest()
    p = os.path.join(od, f'{tag}_{h[:16]}.cnf'); q = p[:-4] + '.lrat'
    open(p, 'w').write(txt)
    r = subprocess.run(['cadical', '-q', '--lrat=true', '--binary=false', p, q], capture_output=True, text=True)
    if r.returncode != 20:
        os.remove(p); 
        if os.path.exists(q): os.remove(q)
        return {'cnf_sha256': h, 'verdict': f'cadical exit {r.returncode}'}
    lh = hashlib.sha256(open(q, 'rb').read()).hexdigest()
    c = subprocess.run([CAKE, p, q], capture_output=True, text=True)
    ok = 's VERIFIED UNSAT' in c.stdout
    os.remove(p); os.remove(q)
    return {'cnf_sha256': h, 'lrat_sha256': lh, 'verdict': 's VERIFIED UNSAT' if ok else (c.stdout + c.stderr)[-200:]}

def cert_template(job):
    core, tests = job
    return {'core': list(core), 'tests': [list(t) for t in tests], **lrat_check(template_cnf(core, tests), 'tmpl')}
def cert_core(core):
    return {'support': list(core), **lrat_check(coupled5.CNF(list(core)).dimacs(), 'core')}

def classify(item):
    S, d = item
    if d == len(S) - 7 and (lambda L: L is not None and check_list(L))(order(list(S))):
        return {'support': list(S), 'demand': d, 'kind': 'cycle', 'order': order(list(S))}, None
    if len(S) >= 23 and d == len(S) - 22 and block_ok(S):
        return {'support': list(S), 'demand': d, 'kind': 'block'}, None
    if d != 1: return None, (S, d, 'demand')
    if S in cores: return {'support': list(S), 'demand': 1, 'kind': 'core'}, None
    core = tr.get(S)
    if core is not None:
        for tests in tmpls.get(tuple(core), []):
            sig = find_sigma(core, tests, S)
            if sig is not None and sorted(sig) == list(S):
                tid = hashlib.sha256(json.dumps([list(core), [list(t) for t in tests]]).encode()).hexdigest()[:16]
                return {'support': list(S), 'demand': 1, 'kind': 'transported', 'template': tid, 'sigma': sig, '_tpl': [list(core), [list(t) for t in tests]]}, None
    return {'support': list(S), 'demand': 1, 'kind': 'core'}, None

if __name__ == '__main__' and os.environ.get('PAR_SIGMA'):
    t0 = time.time(); just = []; need_t = {}; need_c = set(); bad = []
    with Pool(procs) as P:
        for j, b in P.imap(classify, rows, chunksize=256):
            if b is not None: bad.append(b); continue
            if j['kind'] == 'transported':
                core, tests = j.pop('_tpl'); need_t[j['template']] = (tuple(core), tuple(tuple(t) for t in tests))
            elif j['kind'] == 'core': need_c.add(tuple(j['support']))
            just.append(j)
    rows_done = True
elif __name__ == '__main__':
    rows_done = False

if __name__ == '__main__' and not rows_done:
    t0 = time.time(); just = []; need_t = {}; need_c = set(); bad = []
    for S, d in rows:
        if d == len(S) - 7 and (lambda L: L is not None and check_list(L))(order(list(S))):
            just.append({'support': list(S), 'demand': d, 'kind': 'cycle', 'order': order(list(S))}); continue
        if len(S) >= 23 and d == len(S) - 22 and block_ok(S):
            just.append({'support': list(S), 'demand': d, 'kind': 'block'}); continue
        if d != 1: bad.append((S, d, 'demand')); continue
        if S in cores:
            need_c.add(S); just.append({'support': list(S), 'demand': 1, 'kind': 'core'}); continue
        core = tr.get(S)
        ok = False
        if core is not None:
            for tests in tmpls.get(tuple(core), []):
                sig = find_sigma(core, tests, S)
                if sig is not None and sorted(sig) == list(S):
                    tid = hashlib.sha256(json.dumps([list(core), [list(t) for t in tests]]).encode()).hexdigest()[:16]
                    need_t[tid] = (tuple(core), tuple(tests))
                    just.append({'support': list(S), 'demand': 1, 'kind': 'transported', 'template': tid, 'sigma': sig}); ok = True; break
        if not ok:
            need_c.add(S); just.append({'support': list(S), 'demand': 1, 'kind': 'core'})   # fall back: certify directly

if __name__ == '__main__':
    print(json.dumps({'rows': len(rows), 'templates': len(need_t), 'direct': len(need_c), 'bad': len(bad), 'secs': round(time.time() - t0, 1)}), flush=True)
    with Pool(procs) as P:
        tc = P.map(cert_template, list(need_t.values()))
        cc = P.map(cert_core, sorted(need_c))
    tid_ok = {}
    with open(os.path.join(od, 'template_certs.jsonl'), 'w') as f:
        for tid, r in zip(need_t.keys(), tc):
            r['id'] = tid; f.write(json.dumps(r) + '\n'); tid_ok[tid] = r['verdict'] == 's VERIFIED UNSAT'
    core_ok = {}
    with open(os.path.join(od, 'core_certs.jsonl'), 'w') as f:
        for S, r in zip(sorted(need_c), cc):
            f.write(json.dumps(r) + '\n'); core_ok[S] = r['verdict'] == 's VERIFIED UNSAT'
    unj = 0
    for j in just:
        if j['kind'] == 'transported' and not tid_ok[j['template']]: unj += 1
        if j['kind'] == 'core' and not core_ok[tuple(j['support'])]: unj += 1
    json.dump({'rows_file': rowsfile, 'rows_sha256': hashlib.sha256(open(rowsfile, 'rb').read()).hexdigest(), 'justifications': just}, open(os.path.join(od, 'justification.json'), 'w'))
    print(json.dumps({'templates_verified': sum(tid_ok.values()), 'templates': len(tid_ok), 'cores_verified': sum(core_ok.values()), 'cores': len(core_ok),
                      'unjustified': unj + len(bad), 'kinds': {k: sum(1 for j in just if j['kind'] == k) for k in ('cycle', 'block', 'core', 'transported')},
                      'secs': round(time.time() - t0, 1)}), flush=True)
