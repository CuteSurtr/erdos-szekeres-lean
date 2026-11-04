#!/usr/bin/env python3
"""worker.py NAME 'assumption literals' DEADLINE_EPOCH : incremental CEGAR on one cube of the GP-refined m6K8t10.
Loads current.cnf once (CaDiCaL 3.0 via PySAT), adds the shared cuts, solves under the cube assumptions; on SAT runs the
exact certificate pipeline (face-reduced semidefinite, else negative-definite), appends the verified cut to the shared
cuts file under a lock, and repeats; on UNSAT records the cube as closed. The cuts are sound for every configuration
with the prescribed sixfold rotation (written proof + exact check per cut)."""
import sys, os, time, json, subprocess, hashlib, fcntl
from pysat.solvers import Solver
W = '<run-dir>'
D = '<SIX10REFINE>'
BASE = '<proof-archives>/es8-rot-refine-2026-11-04/m6/current.cnf'
VPY = '<research-venv>/bin/python3'
ENV = dict(os.environ, ES_RESULTS='<review-results>', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
name, assum, deadline = sys.argv[1], [int(x) for x in sys.argv[2].split()], float(sys.argv[3])
R = os.path.join(W, 'runs', name, 'g%d' % os.getpid()); os.makedirs(R, exist_ok=True)   # one directory per worker generation
def log(s):
    with open(os.path.join(W, 'logs', name + '.log'), 'a') as f: f.write(time.strftime('%H:%M:%S ') + s + '\n')
def event(s):
    with open(os.path.join(W, 'events.txt'), 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX); f.write(time.strftime('%H:%M:%S ') + name + ' ' + s + '\n')
t0 = time.time(); s = Solver(name='cadical300'); n = 0
with open(BASE) as f:
    for line in f:
        if line[0] in 'pc': continue
        s.add_clause([int(x) for x in line.split()[:-1]]); n += 1
log('loaded %d clauses in %.0fs' % (n, time.time() - t0))
off = 0; boff = 0
def sync_cuts():
    # certified cuts (cuts.clauses) and, separately, blocked hard models (blocked.clauses: an ASSUMPTION, not a cut;
    # any UNSAT reached after a block is conditional on the blocked models being non-realizable)
    global off, boff
    with open(os.path.join(W, 'cuts.clauses')) as f:
        f.seek(off); new = f.read(); off = f.tell()
    with open(os.path.join(W, 'blocked.clauses')) as f:
        f.seek(boff); newb = f.read(); boff = f.tell()
    k = 0
    for line in new.splitlines() + newb.splitlines():
        if line.strip():
            s.add_clause([int(x) for x in line.split()[:-1]]); k += 1
    return k
def run(cmd, cwd=D, timeout=900):
    try:
        return subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout).returncode
    except subprocess.TimeoutExpired:
        return -9
log('synced %d cuts' % sync_cuts()); rnd = 0
while time.time() < deadline:
    sync_cuts()   # include every cut shared so far (including this worker's own last cut) before solving
    s.conf_budget(1000000)
    r = s.solve_limited(assumptions=assum)
    full = s.get_model() if r is True else None   # read the model BEFORE adding clauses (CaDiCaL forbids it after)
    k = sync_cuts()
    if r is None:
        log('budget exhausted (added %d new cuts)' % k); continue
    if r is False:
        nb = sum(1 for l in open(os.path.join(W, 'blocked.clauses')) if l.strip())
        event('UNSAT round %d%s' % (rnd, ' CONDITIONAL on %d blocked models' % nb if nb else '')); log('UNSAT'); break
    rnd += 1
    model = sorted(l for l in full if l > 0)
    mp = os.path.join(R, 'model%d.json' % rnd); data = json.dumps(model).encode(); open(mp, 'wb').write(data)
    msha = hashlib.sha256(data).hexdigest()[:16]
    clause = None; method = None; wpath = None
    fd = os.path.join(R, 'face%d' % rnd); sp = os.path.join(R, 'sp%d' % rnd)
    if run([VPY, '-I', '-B', 'face_sparse.py', mp, sp, '4']) == 0 and run([VPY, '-I', '-B', 'face_cert.py', sp, mp, '1e-8', fd]) == 0 \
            and run(['python3', '-I', '-B', 'check_cert.py', mp, os.path.join(fd, 'face_witness.json')]) == 0:
        clause = json.load(open(os.path.join(fd, 'face_witness.json')))['candidate_clause']; method = 'face'; wpath = os.path.join(fd, 'face_witness.json')
    else:
        sd = os.path.join(R, 'sdp%d' % rnd)
        if run([VPY, '-I', '-B', 'sdp_ext.py', '--model', mp, '--out', sd, '--no-phase', '--no-radius']) == 0 \
                and os.path.exists(os.path.join(sd, 'witness.json')) \
                and run(['python3', '-I', '-B', 'check_def.py', mp, os.path.join(sd, 'witness.json')]) == 0:
            v = json.load(open(os.path.join(sd, 'witness.json')))
            clause = sorted([-x['variable'] * x['required_sign'] for x in v['records'] if x.get('kind', 'triple') == 'triple'], key=abs)
            method = 'def'; wpath = os.path.join(sd, 'witness.json')
    if clause is None and os.path.exists(os.path.join(R, 'sdp%d' % rnd, 'lift.npy')):
        # generalized face: read the degenerate face from the SDP lift, then the exact face certificate on that face
        G = os.path.join(W, 'gen'); sd = os.path.join(R, 'sdp%d' % rnd); spec = os.path.join(R, 'spec%d.json' % rnd)
        fg = os.path.join(R, 'faceg%d' % rnd); spg = os.path.join(R, 'spg%d' % rnd)
        if run([VPY, '-I', '-B', 'facegen.py', mp, sd, spec], cwd=G) == 0 \
                and run([VPY, '-I', '-B', 'face_sparse_g.py', mp, spg, '4', spec], cwd=G) == 0 \
                and run([VPY, '-I', '-B', 'face_cert_g.py', spg, mp, '1e-8', fg, spec], cwd=G) == 0 \
                and run(['python3', '-I', '-B', 'check_cert_g.py', mp, os.path.join(fg, 'face_witness.json')], cwd=G) == 0:
            clause = json.load(open(os.path.join(fg, 'face_witness.json')))['candidate_clause']; method = 'faceg'; wpath = os.path.join(fg, 'face_witness.json')
    if clause is None:
        # layer subsets: a realization restricts to every subset of layers, so a face read from the lift of a subset
        # (layers outside it free) gives a certificate on all records; exact checks inside subface.py
        G = os.path.join(W, 'gen'); sub = os.path.join(R, 'sub%d' % rnd)
        run(['python3', '-I', '-B', 'subface.py', mp, sub], cwd=G, timeout=1500)
        if os.path.exists(os.path.join(sub, 'found.json')):
            fnd = json.load(open(os.path.join(sub, 'found.json'))); wv = json.load(open(fnd['witness']))
            chk = ['python3', '-I', '-B', 'check_cert_g.py', mp, fnd['witness']] if fnd['kind'] == 'g' else ['python3', '-I', '-B', 'check_def.py', mp, fnd['witness']]
            if run(chk, cwd=G if fnd['kind'] == 'g' else D) == 0:
                clause = sorted([-x['variable'] * x['required_sign'] for x in wv['records']], key=abs)
                if fnd['kind'] == 'g': assert clause == wv['candidate_clause']
                method = ('subfaceg' if fnd['kind'] == 'g' else 'subdef') + ''.join(map(str, fnd['layers'])); wpath = fnd['witness']
    if clause is None:
        # fallback: negative-definite certificates on layer subsets (a realization restricts to every subset)
        import itertools
        for drop in [(d,) for d in range(10)] + list(itertools.combinations(range(10), 2)):
            lay = ','.join(str(i) for i in range(10) if i not in drop)
            sd = os.path.join(R, 'sdp%d_%s' % (rnd, '_'.join(map(str, drop))))
            if run([VPY, '-I', '-B', 'sdp_ext.py', '--model', mp, '--out', sd, '--layers', lay, '--no-phase', '--no-radius'], timeout=300) == 0 \
                    and os.path.exists(os.path.join(sd, 'witness.json')) \
                    and run(['python3', '-I', '-B', 'check_def.py', mp, os.path.join(sd, 'witness.json')]) == 0:
                v = json.load(open(os.path.join(sd, 'witness.json')))
                clause = sorted([-x['variable'] * x['required_sign'] for x in v['records'] if x.get('kind', 'triple') == 'triple'], key=abs)
                method = 'def-drop' + '_'.join(map(str, drop)); wpath = os.path.join(sd, 'witness.json'); break
    if method in ('face', 'faceg'):
        # strengthen: greedy exact row removal, re-checked by the independent checker
        G = os.path.join(W, 'gen'); md = os.path.join(R, 'min%d' % rnd)
        sp_dir = os.path.join(R, ('sp%d' if method == 'face' else 'spg%d') % rnd)
        spec = os.path.join(G, 'spec_trueW.json') if method == 'face' else os.path.join(R, 'spec%d.json' % rnd)
        if run([VPY, '-I', '-B', 'minimize.py', sp_dir, mp, '1e-8', md, spec], cwd=G, timeout=300) == 0 \
                and run(['python3', '-I', '-B', 'check_cert_g.py', mp, os.path.join(md, 'face_witness.json')], cwd=G) == 0:
            c2 = json.load(open(os.path.join(md, 'face_witness.json')))['candidate_clause']
            if len(c2) < len(clause):
                clause = c2; method += '+min'; wpath = os.path.join(md, 'face_witness.json')
    if clause is None:
        # block this one model (its triple signs) as an explicit assumption and continue
        blk = [-l for l in full if 0 < abs(l) <= 5710]
        with open(os.path.join(W, 'blocked.clauses'), 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX); f.write(' '.join(map(str, blk)) + ' 0\n'); f.flush()
        event('UNRESOLVED model %s round %d (no certificate found; BLOCKED as assumption, file %s)' % (msha, rnd, os.path.relpath(mp, W)))
        log('no certificate; model blocked as an assumption'); continue
    # the cut must falsify the current model (sanity) before it is shared
    ms = set(full)
    if any(l in ms for l in clause):
        event('BAD cut for model %s (not excluded); stopping' % msha); break
    with open(os.path.join(W, 'cuts.clauses'), 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX); f.write(' '.join(map(str, clause)) + ' 0\n'); f.flush()
    with open(os.path.join(W, 'cuts_provenance.txt'), 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX); f.write('%s round %d model %s method %s len %d witness %s modelfile %s\n' % (name, rnd, msha, method, len(clause), os.path.relpath(wpath, W), os.path.relpath(mp, W)))
    log('round %d SAT model %s excluded by %s (%d terms)' % (rnd, msha, method, len(clause)))
log('worker exit')
