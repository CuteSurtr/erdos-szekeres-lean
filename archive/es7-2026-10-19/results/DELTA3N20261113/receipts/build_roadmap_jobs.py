#!/usr/bin/env python3
"""Roadmap cleanup (24 Nov 2026): match every proof file >= MINB bytes under roadmap-20261115 to its certify record
(certify*.jsonl / cake.jsonl: cnf, cnf_sha256, lrat_sha256, verdict) and write recheck_set.py jobs. Read-only.
Classes: A = campaign verdict "s VERIFIED UNSAT" (a fresh re-check gives the second acceptance; then deletable after
receipts); H = campaign rejected or incomplete (cake heap exhausted: a re-check with a large heap may certify it for the
first time; the proof stays); N = no record or CNF missing (not re-checkable here; stays).
Usage: python3 -I build_roadmap_jobs.py OUTDIR [MINB]"""
import json, os, sys

ROOT = '/home/jay/research/data/roadmap-20261115'
out = sys.argv[1]
MINB = int(sys.argv[2]) if len(sys.argv) > 2 else 10_000_000
recs = {}                                   # abs proof path -> (record, certify file, cnf abs path)
for f in open(os.path.join(out, 'roadmap_certify_files.txt')):
    f = os.path.join(ROOT, f.strip())
    for line in open(f):
        try: r = json.loads(line)
        except Exception: continue
        if 'proof' not in r or 'cnf' not in r: continue
        d = os.path.dirname(f)
        for base in (d, os.path.dirname(d), os.path.dirname(os.path.dirname(d))):
            pp, cp = os.path.normpath(os.path.join(base, r['proof'])), os.path.normpath(os.path.join(base, r['cnf']))
            if os.path.isfile(pp):
                recs.setdefault(pp, []).append((r, f, cp))
                break
jobs, cls = [], {'A': [], 'H': [], 'N': []}
for line in open(os.path.join(out, 'roadmap_proofs.txt')):
    size, rel = line.split(' ', 1)
    p = os.path.normpath(os.path.join(ROOT, rel.strip()))
    if int(size) < MINB: continue
    rs = recs.get(p, [])
    if not rs:
        cls['N'].append((p, int(size), 'no certify record')); continue
    r, f, cp = rs[-1]                       # the last record of this proof counts
    if not os.path.isfile(cp):
        cls['N'].append((p, int(size), 'CNF missing: ' + cp)); continue
    if not r.get('cnf_sha256') or not r.get('lrat_sha256'):
        cls['N'].append((p, int(size), 'record without hashes')); continue
    ok = r.get('verdict') == 's VERIFIED UNSAT'
    stem = p[:-len('.lrat.zst')] if p.endswith('.lrat.zst') else p
    orig = stem + '.cake.out' if os.path.isfile(stem + '.cake.out') else None
    k = 'A' if ok else 'H'
    big = int(size) > 1_000_000_000
    job = dict(id='rm/' + os.path.relpath(p, ROOT), set='roadmap-' + k, cnf={'file': cp}, cnf_sha256=r['cnf_sha256'],
               lrat=p, lrat_sha256=r['lrat_sha256'], heap=11000 if big or k == 'H' else 8000,
               heap_retry=20000, orig=orig if ok else None, certify=f, campaign_verdict=r.get('verdict'))
    cls[k].append((p, int(size), r.get('verdict')))
    jobs.append(job)
for k in 'AH':
    with open(os.path.join(out, 'jobs_roadmap%s.jsonl' % k), 'w') as fo:
        for j in jobs:
            if j['set'] == 'roadmap-' + k: fo.write(json.dumps(j) + '\n')
with open(os.path.join(out, 'roadmap_jobs_summary.json'), 'w') as fo:
    json.dump({k: {'n': len(v), 'bytes': sum(x[1] for x in v), 'items': [[a, b, c] for a, b, c in v]} for k, v in cls.items()}, fo, indent=1)
for k, v in cls.items():
    print(k, len(v), round(sum(x[1] for x in v) / 1e9, 2), 'GB')
for p, s, why in cls['N'][:30]: print('  N', round(s / 1e9, 3), why[:90], p[len(ROOT) + 1:])
for p, s, why in cls['H']: print('  H', round(s / 1e9, 3), why[:60], p[len(ROOT) + 1:])
