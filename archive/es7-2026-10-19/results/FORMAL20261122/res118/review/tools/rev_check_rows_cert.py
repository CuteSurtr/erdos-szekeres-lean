#!/usr/bin/env python3
"""Reviewer's own check that every unit row of the four Lean blocks has a CERTIFIED record (read-only).

For each per-job table (lrat-results.tsv of the T4-type rechecks), a row counts as certified only if some job with
its exact support has status ACCEPTED, sha_ok True, recorded == actual CNF/LRAT sha256, and the job's raw cake_lpr
stdout (cake/<job>.out next to the table) contains the exact line "s VERIFIED UNSAT". Writes a JSON report (argv[1]).
"""
import json, re, sys, hashlib
from pathlib import Path

LEAN = Path('/home/jay/research/data/formalize-20261122/res118/lean/Res118/Rows.lean')
TABLES = {
    'v169': Path('/home/jay/research/data/roadmap-20261115/pm1115/p307v/lrat-b35s20-v169'),
    'b35s19v16': Path('/home/jay/research/data/roadmap-20261115/pm1115/p307v/lrat-b35s19-v16'),
    'verify308': Path('/home/jay/research/data/verify308-20261114/out/lrat'),
}
REC = {  # record copies of the summaries
    'v169': Path('/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ES307N20261118/data/lrat_recheck_v169_summary.json'),
    'b35s19v16': Path('/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113/budget34/VERIFY307/data/lrat-b35s19-v16/lrat-summary.json'),
}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

text = LEAN.read_text()
defs = {}
for m in re.finditer(r'def (\w+) : List \(List Nat\) := \[(.*?)\n\]', text, re.S):
    defs[m.group(1)] = [tuple(int(x) for x in re.findall(r'\d+', r)) for r in re.findall(r'\[([^\[\]]*)\]', m.group(2))]
blocks = {}
for b in ['rowsP', 'rowsQ', 'rowsU', 'rowsA']:
    m = re.search(rf'def {b} : List \(List Nat\) := ([\w ]+(?:\+\+[\w ]+)*)\n', text)
    blocks[b] = [r for q in m.group(1).split('++') for r in defs[q.strip()]]

rep = {'tables': {}, 'blocks': {}}
cert = {}  # table -> set of supports certified
for name, d in TABLES.items():
    t = d / 'lrat-results.tsv'
    lines = t.read_text().splitlines()
    hdr = lines[0].split('\t')
    ok, jobs, bad = set(), 0, []
    for ln in lines[1:]:
        r = dict(zip(hdr, ln.split('\t')))
        jobs += 1
        key = tuple(int(x) for x in r['support'].split(','))
        out = d / 'cake' / (r['job'] + '.out')
        has_line = out.is_file() and 's VERIFIED UNSAT' in out.read_text(errors='replace').splitlines()
        good = (r['status'] == 'ACCEPTED' and r['sha_ok'] == 'True' and r['verified_line'] == 'True'
                and r['cnf_sha_recorded'] == r['cnf_sha_actual'] and r['lrat_sha_recorded'] == r['lrat_sha_actual']
                and has_line)
        if good:
            ok.add(key)
        else:
            bad.append((r['job'], r['status'], has_line))
    cert[name] = ok
    rep['tables'][name] = {'table': str(t), 'table_sha256': sha(t), 'jobs': jobs, 'certified_supports': len(ok),
                           'bad_jobs': bad[:20], 'n_bad': len(bad)}
    if name in REC:
        s = d / 'lrat-summary.json'
        rep['tables'][name]['summary_sha256_workdir'] = sha(s)
        rep['tables'][name]['summary_sha256_record'] = sha(REC[name])
        rep['tables'][name]['summary_equal_record'] = sha(s) == sha(REC[name])

for b, rows in blocks.items():
    rep['blocks'][b] = {t: sum(1 for r in rows if r in cert[t]) for t in cert}
    rep['blocks'][b]['rows'] = len(rows)
    rep['blocks'][b]['uncertified_everywhere'] = sum(1 for r in rows if not any(r in cert[t] for t in cert))
U, A = set(blocks['rowsU']), set(blocks['rowsA'])
rep['U_not_in_A'] = len(U - A)
rep['U_not_in_A_certified_by_b35s19v16'] = sum(1 for r in U - A if r in cert['b35s19v16'])
print(json.dumps(rep, indent=1))
Path(sys.argv[1]).write_text(json.dumps(rep, indent=1) + '\n')
