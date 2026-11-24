#!/usr/bin/env python3
"""Roadmap map (24 Nov 2026): one row per track of roadmap-20261115 (pm1115/<x> and the other top-level entries):
bytes (all / proofs by class A, H, N / other), files, the records that cite the track (git grep on main, counted per
record folder), live bindings (23 Nov bind list, formalize-20261122 text), and the plan. Read-only; writes
ROADMAP_MAP.md and roadmap_map.json in this folder."""
import collections, json, os, subprocess

ROOT = '/home/jay/research/data/roadmap-20261115'
REPO = '/home/jay/research/lean/erdos-szekeres-lean'
OUT = os.path.dirname(os.path.abspath(__file__))
KEEP = {  # track -> reason (live evidence of current results, per records and memory)
    'pm1115/p307v': 'T4 cake_lpr outputs = trust item E2 of the Res118 row blocks (302 chain)',
    'pm1115/vb1118': 'VB re-check of N66 and lo33 (N66N, LO33N: evidence of the 302 chain)',
    'pm1115/vb': 'VB re-check (N66N, LO33N, DELTA3N)',
    'pm1115/vb1116': 'VB re-check of N66 rows (N66N, LO33N)',
    'pm1115/l1118': 'bound by FORMAL20261122 (Lean work)',
    'n66cubes': 'N66 cube inputs (sb_clauses.cnf was loaded by the L15 driver; N66N)',
}
summ = json.load(open(os.path.join(OUT, 'roadmap_jobs_summary.json')))
cls_of = {}
for k in 'AHN':
    for p, b, why in summ[k]['items']:
        cls_of[p] = (k, b)


def track(rel):
    parts = rel.split('/')
    return '/'.join(parts[:2]) if parts[0] == 'pm1115' and len(parts) > 2 else parts[0]


rows = collections.defaultdict(lambda: dict(bytes=0, files=0, A=0, H=0, N=0, small_proofs=0, other=0))
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        p = os.path.join(dp, f)
        try: st = os.lstat(p)
        except OSError: continue
        rel = os.path.relpath(p, ROOT)
        t = track(rel) if '/' in rel else rel
        r = rows[t]; r['bytes'] += st.st_size; r['files'] += 1
        if p in cls_of: r[cls_of[p][0]] += st.st_size
        elif '.lrat' in f or '.drat' in f: r['small_proofs'] += st.st_size
        else: r['other'] += st.st_size
bind = open('/home/jay/research/data/cleanup-20261123/bind/bound_paths.tsv').read()
for t, r in rows.items():
    pat = t + '/' if not t.endswith(('.txt', '.jsonl', '.log', '.cksum')) else t
    g = subprocess.run(['git', '-C', REPO, 'grep', '-l', '-I', '-F', pat, 'main', '--', 'archive'], capture_output=True, text=True).stdout
    recs = collections.Counter(l.split(':', 1)[1].split('/')[3] for l in g.splitlines() if l.count('/') >= 4)
    r['cited_by'] = ', '.join('%s (%d)' % (k, v) for k, v in recs.most_common(4))
    r['bind23'] = bind.count('roadmap-20261115/' + t)
    if t in KEEP: r['plan'] = 'KEEP: ' + KEEP[t]
    elif r['A']: r['plan'] = 're-check class A proofs; delete them after receipts are pushed (CNFs kept)'
    elif r['H']: r['plan'] = 're-check (first cake_lpr acceptance); keep'
    else: r['plan'] = 'keep (small, or not re-checkable here)'
    if r['H'] and t not in KEEP and r['A']: r['plan'] += '; class H proofs: re-check, keep'
order = sorted(rows.items(), key=lambda x: -x[1]['bytes'])
G = lambda b: '%.2f' % (b / 1e9)
lines = ['# roadmap-20261115: map of 24 Nov 2026 (main session, read-only)', '',
         'Folder of the 15-18 Nov research programme (record ROADMAP20261115; the Δ-reduction work is DELTA3N20261113',
         '`attack20261115/`). Classes of proofs >= 10 MB (build_roadmap_jobs.py): A = campaign `s VERIFIED UNSAT` with',
         'CNF and hashes on record; H = the campaign\'s cake_lpr ran out of heap (never accepted); N = no certify record',
         'found or not re-checkable here. "cited by" = record folders whose text names the track path (git grep, main).', '',
         '| track | GB | files | A GB | H GB | N GB | small proofs GB | other GB | cited by | bind 23 Nov | plan |',
         '|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|']
for t, r in order:
    lines.append('| %s | %s | %d | %s | %s | %s | %s | %s | %s | %d | %s |' % (t, G(r['bytes']), r['files'], G(r['A']), G(r['H']), G(r['N']),
                 G(r['small_proofs']), G(r['other']), r['cited_by'] or '-', r['bind23'], r['plan']))
tot = {k: sum(r[k] for r in rows.values()) for k in ('bytes', 'A', 'H', 'N', 'small_proofs', 'other')}
lines += ['', 'Totals (GB): all %s; A %s; H %s; N %s; small proofs %s; other %s.' % tuple(G(tot[k]) for k in ('bytes', 'A', 'H', 'N', 'small_proofs', 'other'))]
open(os.path.join(OUT, 'ROADMAP_MAP.md'), 'w').write('\n'.join(lines) + '\n')
json.dump({t: r for t, r in order}, open(os.path.join(OUT, 'roadmap_map.json'), 'w'), indent=1)
print('\n'.join(lines[:12 + 25]))
print(lines[-1])
