"""Cores of any size from the large-support engine (dp66), put into certifiable form.
Template format for a core S (sorted states, n = |S|):
   CNF(S; octs, tests) = every clause of coupled5.CNF(S, octagon=False) with tag None   (all static families except
                         the complete no-octagon family; state independent, depends only on n)
                       + the no-octagon clause of each 8-subset in `octs`               (members of the complete family)
                       + the state-dependent clauses whose tag is in `tests`.
It is a sub-CNF of coupled5.CNF(S); for an injective sigma that passes the tests, sigma's full CNF contains or implies
every clause of it (README, Transport).  So if CNF(S; octs, tests) is UNSAT, image(sigma) is a demand-one row.
Discovery here; the certificate is CaDiCaL 2.1.3 LRAT + cake_lpr on exactly this CNF (bigcert66.py)."""
import itertools, os, subprocess, hashlib, json, time
from pysat.solvers import Solver
import etv_common as ec, coupled5, lazy66, transport66
HERE = os.path.dirname(os.path.abspath(__file__))
_SN = {}
def static_noct(n):
    """(nv, nc, body) of the static clauses of coupled5.CNF without the no-octagon family; cached on disk."""
    if n in _SN: return _SN[n]
    p = os.path.join(HERE, 'static', f'staticnoct_A{ec.A}_B{ec.B}_{n}.txt')
    if os.path.exists(p):
        with open(p) as f:
            nv, nc = map(int, f.readline().split()); body = f.read()
    else:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        cnf = coupled5.CNF(list(range(n)), static=True, octagon=False)
        cls = [c for c, t in zip(cnf.clauses, cnf.tags) if t is None]
        nv, nc = cnf.nv, len(cls)
        body = ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls)
        tmp = p + f'.{os.getpid()}'
        with open(tmp, 'w') as f: f.write(f'{nv} {nc}\n' + body)
        os.replace(tmp, p)
    if n <= 20: _SN[n] = (nv, nc, body)
    return (nv, nc, body)

def oct_clause(dyn, eight):
    return sorted((-dyn.convex(q) for q in itertools.combinations(sorted(eight), 4)), key=abs)

def template_parts(S, octs, keep=None):
    """Returns nv, static body text, list of (clause, tag) for octagon clauses (tag ('oct', i)) and kept tests."""
    nv, nc, body = static_noct(len(S))
    dyn = coupled5.CNF(list(S), static=False)
    assert dyn.nv == nv
    extra = [(oct_clause(dyn, e), ('oct', i)) for i, e in enumerate(octs)]
    kp = None if keep is None else set(map(tuple, keep))
    extra += [(c, t) for c, t in zip(dyn.clauses, dyn.tags) if kp is None or t in kp]
    return nv, nc, body, extra

def template_text(S, octs, keep=None):
    nv, nc, body, extra = template_parts(S, octs, keep)
    return f'p cnf {nv} {nc + len(extra)}\n' + body + ''.join(' '.join(map(str, c)) + ' 0\n' for c, t in extra)

def find_octs(S):
    """Octagon 8-sets (index tuples) that make the lazily built standard CNF of S unsatisfiable, or None."""
    L = lazy66.Lazy(list(S)); r, core = L.solve(range(len(S))); octs = sorted(L.octs); L.close()
    return octs if r == 'unsat' else None

def trace(S, octs, workdir=os.path.join(HERE, 'lrat')):
    """CaDiCaL 2.1.3 LRAT on CNF(S; octs, all tests); returns (used tests, used oct indices, used static clause lines)."""
    os.makedirs(workdir, exist_ok=True)
    nv, nc, body, extra = template_parts(S, octs)
    p = os.path.join(workdir, f'big_{os.getpid()}.cnf'); q = p[:-4] + '.lrat'
    with open(p, 'w') as f:
        f.write(f'p cnf {nv} {nc + len(extra)}\n' + body + ''.join(' '.join(map(str, c)) + ' 0\n' for c, t in extra))
    r = subprocess.run(['cadical', '-q', '--lrat=true', '--binary=false', p, q], capture_output=True, text=True)
    if r.returncode != 20:
        for x in (p, q):
            if os.path.exists(x): os.remove(x)
        return None
    m = nc + len(extra); hints = {}; empty = None
    with open(q) as f:
        for line in f:
            t = line.split()
            if len(t) > 1 and t[1] == 'd': continue
            cid = int(t[0]); z = t.index('0', 1)
            hints[cid] = [int(x) for x in t[z + 1:-1]]
            if z == 1: empty = cid
    used = set(); stack = [empty]; seen = set()
    while stack:
        c = stack.pop()
        if c in seen: continue
        seen.add(c)
        if c <= m: used.add(c); continue
        stack.extend(abs(x) for x in hints.get(c, []))
    os.remove(q); os.remove(p)
    tags = [extra[c - nc - 1][1] for c in used if c > nc]
    tests = sorted(t for t in tags if t[0] != 'oct')
    uoct = sorted(t[1] for t in tags if t[0] == 'oct')
    lines = body.split('\n')
    ustatic = [list(map(int, lines[c - 1].split()[:-1])) for c in used if c <= nc]
    return tests, uoct, ustatic

def shrink(S, octs, tests, ustatic):
    """Minimal subset of the tests such that (used static + used octagon clauses + kept tests) stays UNSAT."""
    dyn = coupled5.CNF(list(S), static=False)
    tests = [tuple(t) for t in tests]
    tsel = {t: dyn.nv + 1 + k for k, t in enumerate(tests)}
    s = Solver(name='cadical195')
    for c in ustatic: s.add_clause(c)
    for e in octs: s.add_clause(oct_clause(dyn, e))
    for c, t in zip(dyn.clauses, dyn.tags):
        if t in tsel: s.add_clause(c + [-tsel[t]])
    cur = list(tests)
    if s.solve(assumptions=[tsel[t] for t in cur]):
        s.delete(); return None
    core = set(s.get_core() or []); cur = [t for t in cur if tsel[t] in core]
    i = 0
    while i < len(cur):
        trial = cur[:i] + cur[i + 1:]
        if not s.solve(assumptions=[tsel[t] for t in trial]):
            core = set(s.get_core() or []); cur = [t for t in trial if tsel[t] in core]
        else: i += 1
    s.delete()
    return [list(t) for t in cur]

def transport_big(S, tlimit=20):
    """Core S (sorted states) -> template (octs, minimal tests) and all transported supports found in tlimit seconds."""
    S = sorted(S); t0 = time.time()
    octs = find_octs(S)
    if octs is None: return {'core': S, 'error': 'lazy standard CNF is SAT'}
    tr = trace(S, octs)
    if tr is None: return {'core': S, 'error': 'cadical did not refute the template CNF'}
    tests, uoct, ustatic = tr
    octs2 = [list(octs[i]) for i in uoct]
    small = shrink(S, octs2, tests, ustatic)
    if small is None: return {'core': S, 'error': 'shrink start SAT'}
    sups, sinfo = transport66.search(S, [tuple(t) for t in small], limit=tlimit)
    if S not in sups: sups.append(S)
    return {'core': S, 'octs': octs2, 'tests_used': len(tests), 'tests_min': len(small), 'tests': small, 'supports': sups,
            'search': sinfo, 'seconds': round(time.time() - t0, 1)}

if __name__ == '__main__':
    import sys
    for line in open(sys.argv[1]):
        c = json.loads(line)['support']
        r = transport_big(c)
        print(json.dumps({k: (v if k not in ('supports', 'octs', 'tests') else len(v)) for k, v in r.items() if k != 'core'} | {'n': len(c)}), flush=True)
        if 'tests' in r:
            # check: the template CNF with the minimal tests is UNSAT for CaDiCaL 2.1.3
            txt = template_text(r['core'], r['octs'], [tuple(t) for t in r['tests']])
            p = os.path.join(HERE, 'lrat', f'chk_{os.getpid()}.cnf'); open(p, 'w').write(txt)
            rc = subprocess.run(['cadical', '-q', '-n', p], capture_output=True).returncode; os.remove(p)
            print('   template CNF cadical exit', rc, 'bytes', len(txt), flush=True)
