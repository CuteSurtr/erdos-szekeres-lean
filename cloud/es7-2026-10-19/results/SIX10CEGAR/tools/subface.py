#!/usr/bin/env python3
"""subface.py MODEL OUTDIR : certificate search on layer subsets for a model the full pipeline could not exclude.
For each subset L (inner suffixes first, then complements of one or two layers): sdp_ext.py --layers L; if it
returns a negative-definite witness, check it (check_def.py); otherwise read a face from the restricted lift
(facegen_sub.py, layers outside L free) and run the exact face certificate on all records (face_sparse_g.py,
face_cert_g.py, check_cert_g.py).  Prints the first certified witness."""
import itertools, json, os, subprocess, sys
from pathlib import Path
G = Path(__file__).resolve().parent
D = '<SIX10REFINE>'
VPY = '<research-venv>/bin/python3'
ENV = dict(os.environ, ES_RESULTS='<review-results>', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
mp, out = sys.argv[1], Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)


def run(cmd, cwd=G, timeout=600):
    try:
        r = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout[-300:]
    except subprocess.TimeoutExpired:
        return -9, 'timeout'


subsets = [list(range(k, 10)) for k in range(1, 7)] + [list(range(0, k)) for k in range(9, 4, -1)]
subsets += [[i for i in range(10) if i not in d] for d in itertools.combinations(range(10), 2)]
if os.environ.get('SUBFACE_SMALL'):   # small subsets of layers 1..9 that contain layer 9, smallest first
    subsets = [list(c) + [9] for k in (2, 3, 4, 5) for c in itertools.combinations(range(1, 9), k)]
for L in subsets:
    tag = ''.join(map(str, L)); sd = out / ('sdp_' + tag); lay = ','.join(map(str, L))
    rc, _ = run([VPY, '-I', '-B', 'sdp_ext.py', '--model', mp, '--out', str(sd), '--layers', lay, '--no-phase', '--no-radius'], cwd=D)
    if rc != 0:
        continue
    res = json.load(open(sd / 'result.json'))
    if res.get('certificate') and (sd / 'witness.json').exists():
        rc, o = run(['python3', '-I', '-B', 'check_def.py', mp, str(sd / 'witness.json')], cwd=D)
        print(tag, 'def', 'CHECKED' if rc == 0 else 'check failed', flush=True)
        if rc == 0:
            json.dump({'witness': str(sd / 'witness.json'), 'kind': 'd', 'layers': L}, open(out / 'found.json', 'w')); break
        continue
    spec = out / ('spec_' + tag + '.json')
    rc, o = run([VPY, '-I', '-B', 'facegen_sub.py', mp, str(sd), str(spec), lay])
    if rc != 0:
        print(tag, 'margin %.2g' % res['margin_evidence_only'], 'no face', flush=True); continue
    spg, fg = out / ('spg_' + tag), out / ('faceg_' + tag)
    rc1, _ = run([VPY, '-I', '-B', 'face_sparse_g.py', mp, str(spg), '4', str(spec)])
    rc2, _ = run([VPY, '-I', '-B', 'face_cert_g.py', str(spg), mp, '1e-8', str(fg), str(spec)]) if rc1 == 0 else (1, '')
    rc3, o = run(['python3', '-I', '-B', 'check_cert_g.py', mp, str(fg / 'face_witness.json')]) if rc2 == 0 else (1, '')
    print(tag, 'margin %.2g' % res['margin_evidence_only'], 'face', json.load(open(spec))['groups'], json.load(open(spec))['zero'],
          'CHECKED' if rc3 == 0 else 'failed at step %d' % (1 if rc1 else 2 if rc2 else 3), flush=True)
    if rc3 == 0:
        print(o); json.dump({'witness': str(fg / 'face_witness.json'), 'kind': 'g', 'layers': L}, open(out / 'found.json', 'w')); break
