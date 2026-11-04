#!/usr/bin/env python3
"""audit.py OUTDIR [JOBS] : re-check every shared cut against a stored witness with the exact checkers.

For each clause of cuts.clauses, find the witness files under runs/ whose clause is the same set of literals and run
the matching exact checker on one of them:
  face_witness.json with face_spec -> gen/check_cert_g.py   (generalized face)
  face_witness.json without it     -> six_model0090/check_cert.py (fixed face)
  witness.json                     -> six_model0090/check_def.py  (negative definite)
If the model file the witness was made from is still on disk (same SHA-256), the original checker runs, including its
binding of the record signs to the model ('full'). Otherwise a copy of the checker with only the model-binding lines
removed runs ('sound'): it still checks the triple/variable binding, the weights, the face and the exact LDL, so the
clause is still certified; it only no longer re-checks that the clause excludes that model.
Writes OUTDIR/audit.tsv (cut index, status, witness) and OUTDIR/summary.json."""
import hashlib, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

W = Path('<run-dir>')
G = W / 'gen'; D = Path('<SIX10REFINE>')
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True); JOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 4
ENV = dict(os.environ, ES_RESULTS='<review-results>')

# model-free copies of the three checkers (mechanical edit of exactly three lines each)
CHK = {'g': G / 'check_cert_g.py', 'f': D / 'check_cert.py', 'd': D / 'check_def.py'}
NM = {}
for k, p in CHK.items():
    src = p.read_text()
    reps = [("raw = Path(model_path).read_bytes(); pos = set(json.loads(raw)); wit = json.loads(Path(wit_path).read_text())",
             "wit = json.loads(Path(wit_path).read_text())  # model-free copy"),
            ("assert hashlib.sha256(raw).hexdigest() == wit['model_sha256']\n", ""),
            ("assert r['required_sign'] == (1 if r['variable'] in pos else -1), 'sign binding to model'",
             "assert r['required_sign'] in (1, -1)  # model-free copy")]
    for a, b in reps:
        assert src.count(a) == 1, (p, a[:50]); src = src.replace(a, b)
    q = OUT / ('nm_' + p.name); q.write_text(src); NM[k] = q

models = {}
for mp in W.glob('runs/**/model*.json'):
    models.setdefault(hashlib.sha256(mp.read_bytes()).hexdigest(), mp)
wits = {}
for wp in list(W.glob('runs/**/face_witness.json')) + list(W.glob('runs/**/witness.json')):
    try:
        w = json.loads(wp.read_text())
    except Exception:
        continue
    if wp.name == 'witness.json':
        key = frozenset(-r['variable'] * r['required_sign'] for r in w['records']); kind = 'd'
    else:
        key = frozenset(w['candidate_clause']); kind = 'g' if 'face_spec' in w else 'f'
    wits.setdefault(key, []).append((wp, kind, w.get('model_sha256')))
cuts = [frozenset(int(x) for x in l.split()[:-1]) for l in (W / 'cuts.clauses').read_text().splitlines() if l.strip()]


def check(i):
    for wp, kind, msha in wits.get(cuts[i], []):
        cwd = G if kind == 'g' else D
        if msha in models:
            cmd, status = ['python3', '-I', '-B', str(CHK[kind]), str(models[msha]), str(wp)], 'full'
        else:
            cmd, status = ['python3', '-I', '-B', str(NM[kind]), '-', str(wp)], 'sound'
        r = subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True)
        if r.returncode == 0 and '"ok": true' in r.stdout:
            return i, status, str(wp.relative_to(W)), kind
    return i, 'none' if not wits.get(cuts[i]) else 'fail', '', ''


with ThreadPoolExecutor(JOBS) as ex:
    res = sorted(ex.map(check, range(len(cuts))))
with open(OUT / 'audit.tsv', 'w') as f:
    for row in res:
        f.write('\t'.join(map(str, row)) + '\n')
summ = {'cuts': len(cuts), 'distinct_cuts': len(set(cuts)), 'witness_files': sum(len(v) for v in wits.values()),
        'model_files': len(models), 'by_status': {}, 'by_kind': {}}
for _, st, _, k in res:
    summ['by_status'][st] = summ['by_status'].get(st, 0) + 1
    if k: summ['by_kind'][k] = summ['by_kind'].get(k, 0) + 1
(OUT / 'summary.json').write_text(json.dumps(summ, indent=1)); print(json.dumps(summ))
