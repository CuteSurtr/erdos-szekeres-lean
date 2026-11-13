"""Shrink the state-dependent facts a core's refutation needs, then transport (discovery only).

Start from the tests used by one LRAT proof; drop each test (replace the clause by nothing) and keep the
drop when the CNF stays UNSAT.  The remaining tests define a template; enumerate its compatible maps."""
import json, os, subprocess, sys, time, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import coupled
from transport import used_tests, search

def unsat_without(S, keep_tests, workdir=os.path.join(HERE, 'shrink')):
    """CNF of S keeping only state-dependent clauses whose tag is in keep_tests."""
    os.makedirs(workdir, exist_ok=True)
    nv, nc, body = coupled._static(len(S))
    dyn = coupled.CNF(S, static=False)
    keep = set(keep_tests)
    cls = [c for c, t in zip(dyn.clauses, dyn.tags) if t in keep]
    p = os.path.join(workdir, f'{os.getpid()}.cnf')
    with open(p, 'w') as f:
        f.write(f'p cnf {nv} {nc + len(cls)}\n' + body + ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls))
    r = subprocess.run(['cadical', '-q', '-n', '-t', '60', p], capture_output=True)
    return r.returncode == 20

def shrink(S, tests):
    # try dropping whole groups first (all source, all domain, ...), then single tests
    tests = list(tests)
    for kind in ('source', 'domain', 'empty', 'positive'):
        trial = [t for t in tests if t[0] != kind]
        if len(trial) < len(tests) and unsat_without(S, trial):
            tests = trial
    i = 0
    while i < len(tests):
        trial = tests[:i] + tests[i + 1:]
        if unsat_without(S, trial):
            tests = trial
        else:
            i += 1
    return tests

def run(S, transport_seconds=120):
    t0 = time.time()
    tests, info = used_tests(S)
    if tests is None:
        return None
    small = shrink(S, tests)
    sups, sinfo = search(S, small, limit=transport_seconds)
    return {'core': S, 'tests_used': len(tests), 'tests_min': len(small), 'tests': small,
            'supports': sups, 'search': sinfo, 'seconds': round(time.time() - t0, 1)}

if __name__ == '__main__':
    S = json.loads(sys.argv[1])
    r = run(S)
    print(json.dumps({k: v for k, v in r.items() if k not in ('supports', 'tests')}))
    print(json.dumps(r['tests']))
