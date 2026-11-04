#!/usr/bin/env python3
"""recert.py AUDIT.tsv OUTDIR [JOBS] [LIMIT] : exact re-certification of shared cuts that have no surviving witness.
For a cut C, write the sign pattern it forbids as a synthetic model (positive set = variables v with -v in C) and
restrict the certificate search to the records of C (sdp_ext.py here reads RECERT_VARS).  Try, in order, the
negative-definite certificate (sdp_ext.py, check_def.py) and the face certificate on each face seen in the run, most
frequent first (face_sparse_g.py, face_cert_g.py, check_cert_g.py).  A cut counts as re-certified when an exact
checker accepts a witness whose clause is a subset of C (a sub-clause implies C)."""
import collections, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
H = Path(__file__).resolve().parent; W = H.parent.parent
VPY = '<research-venv>/bin/python3'
ENV0 = dict(os.environ, ES_RESULTS='<review-results>', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
aud, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 4; LIMIT = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
cuts = [[int(x) for x in l.split()[:-1]] for l in (W / 'cuts.clauses').read_text().splitlines() if l.strip()]
todo = [int(r.split('\t')[0]) for r in aud.read_text().splitlines() if r.split('\t')[1] == 'none'][:LIMIT]
# faces seen in the run, most frequent first
fc = collections.Counter(); spec_of = {}
for p in list(W.glob('runs/**/face_witness.json')):
    try: sp = json.loads(p.read_text()).get('face_spec')
    except Exception: continue
    if sp:
        k = json.dumps({'groups': sp['groups'], 'zero': sp['zero']}, sort_keys=True); fc[k] += 1; spec_of[k] = sp
specs = [spec_of[k] for k, _ in fc.most_common(int(os.environ.get("RECERT_NFACES", "12")))]
for j, sp in enumerate(specs):
    (OUT / ('face%02d.json' % j)).write_text(json.dumps(sp))


def run(cmd, env, timeout=300):
    try:
        return subprocess.run(cmd, cwd=H, env=env, capture_output=True, text=True, timeout=timeout).returncode
    except subprocess.TimeoutExpired:
        return -9


def one(i):
    c = set(cuts[i]); d = OUT / ('c%05d' % i); d.mkdir(exist_ok=True)
    mp = d / 'model.json'; mp.write_text(json.dumps(sorted(-l for l in c if l < 0)))
    vf = d / 'vars.json'; vf.write_text(json.dumps(sorted(abs(l) for l in c)))
    env = dict(ENV0, RECERT_VARS=str(vf))
    sd = d / 'def'
    if run([VPY, '-I', '-B', 'sdp_ext.py', '--model', str(mp), '--out', str(sd), '--no-phase', '--no-radius'], env) == 0 \
            and (sd / 'witness.json').exists() and run(['python3', '-I', '-B', 'check_def.py', str(mp), str(sd / 'witness.json')], ENV0) == 0:
        w = json.loads((sd / 'witness.json').read_text())
        if {-r['variable'] * r['required_sign'] for r in w['records']} <= c:
            return i, 'def', str((sd / 'witness.json').relative_to(W))
    for j in range(len(specs)):
        spf = OUT / ('face%02d.json' % j); sp, fg = d / ('sp%02d' % j), d / ('fg%02d' % j)
        if run([VPY, '-I', '-B', 'face_sparse_g.py', str(mp), str(sp), '2', str(spf)], env) == 0 \
                and run([VPY, '-I', '-B', 'face_cert_g.py', str(sp), str(mp), '1e-8', str(fg), str(spf)], env) == 0 \
                and run(['python3', '-I', '-B', 'check_cert_g.py', str(mp), str(fg / 'face_witness.json')], ENV0) == 0:
            if set(json.loads((fg / 'face_witness.json').read_text())['candidate_clause']) <= c:
                return i, 'face%02d' % j, str((fg / 'face_witness.json').relative_to(W))
    return i, 'not re-certified', ''


with ThreadPoolExecutor(JOBS) as ex:
    res = list(ex.map(one, todo))
with open(OUT / 'recert.tsv', 'w') as f:
    for r in res: f.write('\t'.join(map(str, r)) + '\n')
cnt = collections.Counter(r[1] for r in res); print(json.dumps({'tried': len(res), 'by_method': dict(cnt)}))
