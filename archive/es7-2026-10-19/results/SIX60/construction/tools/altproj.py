#!/usr/bin/env python3
"""Alternating projections between REAL configurations and SAT models (evidence only; exact follow-up by
exact_check.py / verify_set.py).
  real R --(orientation signs as solver PHASES, R's phase order of layers 1-4 as the cube)--> SAT model M of the
  CEGAR formula (encoder A + verified cuts + shared GP/cut/inbox clauses; NO blocked-model assumptions), i.e. an
  octagon-free sign pattern found by a CDCL search that starts from R's signs
  --(scale-free fit started at R)--> real R' ; repeat.
If R' realizes M (0 wrong signs) R' is a candidate 60-point set.  Logged per iteration: Hamming distance d(M, R),
wrong(M, R'), float convex-8-gon counts of R and R'.
Usage: altproj.py INITS.json OUTPREFIX STOP_EPOCH [CONFLICTS]
INITS.json: list of {"name":..., "lr": [10], "th": [10]} (any phases/order; normalised and mirrored as needed)."""
import sys, os, json, time, glob, numpy as np, warnings
warnings.filterwarnings('ignore'); np.seterr(all='ignore')
import common as cm, opt, search, cvx, subprocess, hashlib, importlib.util
_s = importlib.util.spec_from_file_location('gpmod', '<six10-work-dir>/cegar/tools/gp.py'); gpmod = importlib.util.module_from_spec(_s); _s.loader.exec_module(gpmod)
GPT = gpmod.GP('<six10-work-dir>/cegar/base/gp_table.npy')
CT = '<six10-work-dir>/cegar/tools'
VPY = '<six10-work-dir>/venv/bin/python3'
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
from pysat.solvers import Solver
from scipy.optimize import minimize
CEG = '<six10-work-dir>/cegar'
inits = json.load(open(sys.argv[1])); outp = sys.argv[2]; stop = float(sys.argv[3]); conf = int(sys.argv[4]) if len(sys.argv) > 4 else 1000000
log = open(outp + '.log', 'a')
def P(*a):
    s = time.strftime('%H:%M:%S') + ' ' + ' '.join(str(x) for x in a); print(s, flush=True); log.write(s + '\n'); log.flush()

S = None; offsets = {}; nload = 0


def load(path, skip_header=False):
    global nload
    off = offsets.get(path, 0)
    with open(path, 'rb') as f:
        f.seek(off); data = f.read()
    end = data.rfind(b'\n') + 1; data = data[:end]; offsets[path] = off + end
    for line in data.split(b'\n'):
        if not line or line[:1] in (b'c', b'p'): continue
        lits = [int(x) for x in line.split()]
        if not lits or lits[-1] != 0 or 0 in lits[:-1]: continue
        S.add_clause(lits[:-1]); nload += 1


def sync():
    for p in [f'{CEG}/shared/gp.clauses', f'{CEG}/shared/cuts.clauses']:
        if os.path.exists(p): load(p)
    for p in sorted(glob.glob(f'{CEG}/inbox/*.clauses')):
        b = p[:-len('.clauses')]
        if any(os.path.exists(b + s) for s in ('.log', '.checker.log', '.check.log', '.clauses.log')): load(p)


def fresh():
    global S, offsets, nload
    if S is not None: S.delete()
    S = Solver(name='cadical300'); offsets = {}; nload = 0; t0 = time.time()
    load(f'{CEG}/base/encA_6_8_10.cnf'); load(f'{CEG}/base/cuts_verified.clauses'); load(f'{CEG}/base/cut_model0090_sparse.clauses'); sync()
    P('loaded', nload, 'clauses in', round(time.time() - t0), 's')
import anneal8
ELITE = outp + '_elite.jsonl'
YV = [5711, 5712, 5713, 5719, 5720, 5726]


def normalise(lr, th):
    z = np.exp(np.array(lr) + 1j * np.array(th)); z = cm.normalize_seeds(z)
    if np.angle(z[1]) % (np.pi / 3) > np.angle(z[2]) % (np.pi / 3):
        z = cm.normalize_seeds(np.conj(z))
    return z


def signs(z):
    o = cm.orient_z(z); th = np.angle(z) % (np.pi / 3); th[0] = 0
    lits = [(v + 1) if o[v] > 0 else -(v + 1) for v in range(cm.NT)]
    for (i, j), v in cm.E.Y.items(): lits.append(v if th[i] < th[j] else -v)
    return lits, np.where(o > 0, 1, -1)


def z_to_x(z):
    z = z / z[0] * abs(z[0]) / abs(z[0])
    rho = np.log(np.abs(z)); th = np.angle(z)
    return np.concatenate([rho[1:] - rho[0], th[1:] - th[0]])


def octs(z):
    c, _ = cvx.count6(np.log(np.abs(z)), np.angle(z)); return int(c[8]), int(c[7])


MAXCERT = int(os.environ.get('MAXCERT', '25')); FRESH = os.environ.get('FRESH', '1') == '1'
WD = outp + '_work'; os.makedirs(WD, exist_ok=True); NCUT = [0]
cutf = open(outp + '_cuts.clauses', 'a'); provf = open(outp + '_cuts.provenance.tsv', 'a')


def certify(pos):
    """lane certificates lin2 / lin (cegar/tools, read-only use) + their exact checkers; returns the clause or None"""
    data = json.dumps(sorted(pos)).encode(); h = hashlib.sha256(data).hexdigest()[:16]
    d = os.path.join(WD, h); os.makedirs(d, exist_ok=True); mp = os.path.join(d, 'model.json'); open(mp, 'wb').write(data)
    def run(cmd, timeout=180):
        try: return subprocess.run(cmd, cwd=CT, env=ENV, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired: return None
    r1 = run([VPY, '-I', '-B', 'lin2_cert.py', mp, os.path.join(d, 'lin2'), '3'])
    if r1 is not None and r1.returncode == 0 and os.path.exists(os.path.join(d, 'lin2', 'witness.json')):
        c = run(['python3', '-I', '-B', 'facial_snap/checker/check_facial.py', mp, os.path.join(d, 'lin2', 'witness.json')], 600)
        if c is not None and c.returncode == 0:
            open(os.path.join(d, 'lin2', 'check.out'), 'w').write(c.stdout[-5000:])
            cl = sorted(json.load(open(os.path.join(d, 'lin2', 'witness.json')))['clause'], key=abs)
            if not any(((abs(l) in pos) == (l > 0)) for l in cl):
                cutf.write(' '.join(map(str, cl)) + ' 0\n'); cutf.flush(); provf.write('%s\tlin2\t%s\t%d\n' % (h, os.path.join(d, 'lin2', 'witness.json'), len(cl))); provf.flush()
                NCUT[0] += 1; return cl
    r2 = run([VPY, '-I', '-B', 'lin_cert.py', mp, os.path.join(d, 'lin'), '60'])
    if r2 is not None and r2.returncode == 0 and os.path.exists(os.path.join(d, 'lin', 'lin_witness.json')):
        c = run(['python3', '-I', '-B', 'check_lin.py', mp, os.path.join(d, 'lin', 'lin_witness.json')], 600)
        if c is not None and c.returncode == 0:
            open(os.path.join(d, 'lin', 'check.out'), 'w').write(c.stdout[-5000:])
            cl = json.load(open(os.path.join(d, 'lin', 'lin_witness.json')))['candidate_clause']
            if not any(((abs(l) in pos) == (l > 0)) for l in cl):
                cutf.write(' '.join(map(str, cl)) + ' 0\n'); cutf.flush(); provf.write('%s\tlin\t%s\t%d\n' % (h, os.path.join(d, 'lin', 'lin_witness.json'), len(cl))); provf.flush()
                NCUT[0] += 1; return cl
    return None


results = []
for it0, ini in enumerate(inits):
    if time.time() > stop - 120: break
    if FRESH or S is None: fresh()
    z = normalise(ini['lr'], ini['th']); hist = []; seen = set()
    for rnd in range(8):
        if time.time() > stop - 120: break
        sync()
        lits, sR = signs(z)
        assum = [l for l in lits if abs(l) in YV]
        if 5711 not in assum: P(ini.get('name'), 'Y(1,2) false after mirror?'); break
        ncert = 0; ngp = 0; r = None
        for inner in range(MAXCERT):
            S.set_phases(lits)
            S.conf_budget(conf); r = S.solve_limited(assumptions=assum)
            if r is not True: break
            m = S.get_model(); pos = set(l for l in m[:5746] if l > 0)
            viol = GPT.violated(pos)
            if len(viol):
                for k in viol[:4000]:
                    for c in GPT.clauses(int(k)): S.add_clause([int(x) for x in c])
                ngp += 1; continue
            cl = certify(pos)
            if cl is None: break
            S.add_clause(cl); ncert += 1
        if r is not True: P(ini.get('name'), 'rnd', rnd, 'solver', r, 'certs', ncert); break
        if cl is not None: P(ini.get('name'), 'rnd', rnd, 'still certified after', ncert, 'certs; fitting the last model anyway')
        wantM = np.array([1 if (v + 1) in pos else -1 for v in range(cm.NT)])
        h = hash(wantM.tobytes())
        d = int((wantM != sR).sum())
        o8, o7 = octs(z)
        # fit M starting from z
        pr = opt.Problem(wantM, np.ones(cm.NT, bool)); x = z_to_x(z)
        best = (pr.nwrong(x), x)
        for rep in range(3):
            x1 = search.lbfgs(pr, best[1] if rep == 0 else best[1] + np.random.default_rng(rep).normal(size=18) * 0.02, taus=(0.03, 0.01, 0.003, 0.001))
            for j in range(1, 10):
                x2, w2 = search.grid_layer(pr, x1, j, np.random.default_rng(rep * 10 + j), n=24)
                if w2 is not None and w2 < pr.nwrong(x1): x1 = x2
            w = pr.nwrong(x1)
            if w < best[0]: best = (w, x1)
        w, x = best
        z2 = np.exp(np.concatenate([[0], x[:9]]) + 1j * np.concatenate([[0], x[9:]]))
        o8b, o7b = octs(z2)
        P(ini.get('name'), 'rnd', rnd, 'cube', ''.join('1' if l > 0 else '0' for l in assum[1:]), 'gpR', ngp, 'certs', ncert, 'uncertified' if cl is None else 'CERTIFIED', 'd(M,R)=', d, 'wrong(M,fit)=', w, 'N8(R)=', o8, 'N8(fit)=', o8b)
        mh = hashlib.sha256(json.dumps(sorted(pos)).encode()).hexdigest()[:16]
        hist.append({'rnd': rnd, 'd_MR': d, 'wrong_fit': w, 'N8_R': o8, 'N8_fit': o8b, 'model_hash': mh, 'R_lr': np.log(np.abs(z)).tolist(), 'R_th': np.angle(z).tolist(), 'fit_lr': np.log(np.abs(z2)).tolist(), 'fit_th': np.angle(z2).tolist(), 'wrong_vars': [int(pr.idx[i] + 1) for i in np.nonzero(pr.values(x) <= 0)[0]]})
        json.dump({'model_true_vars': sorted(pos)}, open(os.path.join(WD, mh + '_model.json'), 'w'))
        if w == 0:
            json.dump({'name': ini.get('name'), 'model_true_vars': sorted(pos), 'fit_z': [[float(c.real), float(c.imag)] for c in z2]}, open(f'{outp}_CANDIDATE_{it0}_{rnd}.json', 'w'))
            P('CANDIDATE realization found', ini.get('name'), rnd); break
        if h in seen: break
        seen.add(h); z = z2
    if hist:
        hb = min(hist, key=lambda h: (h['N8_fit'], h['wrong_fit']))
        n8, n7, lr2, th2 = anneal8.anneal(hb['fit_lr'], hb['fit_th'], iters=int(os.environ.get('ANNEAL', '30000')), seed=it0)
        P(ini.get('name'), 'anneal from N8', hb['N8_fit'], '->', n8, 'N7', n7)
        with open(ELITE, 'a') as f:
            f.write(json.dumps({'init': ini.get('name'), 'N8_fit': hb['N8_fit'], 'wrong_fit': hb['wrong_fit'], 'model_hash': hb['model_hash'], 'fit_lr': hb['fit_lr'], 'fit_th': hb['fit_th'],
                                'anneal_N8': int(n8), 'anneal_N7': int(n7), 'anneal_lr': lr2.tolist(), 'anneal_th': th2.tolist()}) + '\n')
        if n8 == 0:
            json.dump({'init': ini.get('name'), 'lr': lr2.tolist(), 'th': th2.tolist()}, open(f'{outp}_N8ZERO_{it0}.json', 'w')); P('N8 = 0 CONFIGURATION (float) found', ini.get('name'))
    results.append({'init': ini.get('name'), 'hist': hist})
    json.dump(results, open(outp + '.json', 'w'), indent=1)
P('ALTPROJ DONE')
