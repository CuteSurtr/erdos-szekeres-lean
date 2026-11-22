#!/usr/bin/env python3
"""Reviewer's own hash binding for res118-rowblocks (slot lrv3). Read-only on every input; writes only under review/.
None of the worker's scripts is used; hashes are computed with Python's hashlib.

For every row I of every block B in P, Q, U, A, read from the exe (`rowprint list B`):
  * the exe is frozen: its sha256 is eabe3791... (the M9 summary and the manifest) before the first and after the last run;
  * printed = sha256 of the stdout bytes of `rowprint row B I` (rc 0, nonempty);
  * the T4 re-check tables (the hash of each table and summary is asserted; the b35s19-v16 pair also equals its record
    copy, the v169 summary equals the record copy ES307N20261118/data/lrat_recheck_v169_summary.json):
    a job of that support is GOOD iff status ACCEPTED, sha_ok True, verified_line True, cnf_sha_recorded ==
    cnf_sha_actual, lrat_sha_recorded == lrat_sha_actual, and the raw cake/<job>.out has the exact line
    `s VERIFIED UNSAT`. `cnf_sha_actual` is the hash the T4 runner computed of the very file it then gave to cake_lpr.
  * BOUND iff at least one GOOD job has cnf_sha_actual == printed, and no job of that support is bad or has another
    CNF hash.
Also: row counts 812/208/35/970, supports strictly increasing in range; a stride sample of fresh on-disk CNF hashes
(retention only); CaDiCaL controls (COMPUTED): a tiny support (expect SAT, rc 10) and block row U 0 (expect UNSAT,
rc 20). Writes data/lrv_bind.tsv, data/lrv_bind.json, data/exe_lists.txt.
"""
import csv, hashlib, json, os, subprocess, sys, time

V = '/home/jay/research/data/formalize-20261122/res118-rowblocks/review'
EXE = '/home/jay/research/data/formalize-20261122/res118-rowblocks/build/bin/rowprint'
EXE_SHA = 'eabe37912b332a844e8731d21f3bf4612a6ad2348a54a8d576c90c13476bd496'
P307 = '/home/jay/research/data/roadmap-20261115/pm1115/p307v'
REC = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results'
TABLES = {  # tsv -> (tsv sha, summary path, summary sha, record copies that must be equal)
    P307 + '/lrat-b35s20-v169/lrat-results.tsv':
        ('a80cbba552f288f66da7e096dbea5ccd8d2eab59bb7abdb506d8d3ef85a6e0d2',
         P307 + '/lrat-b35s20-v169/lrat-summary.json',
         'f80a720e3216b8b035fef6ee8713d0cfb0255772fb32ce5da78f1aa4bf3c1ec4',
         [REC + '/ES307N20261118/data/lrat_recheck_v169_summary.json']),
    P307 + '/lrat-b35s19-v16/lrat-results.tsv':
        ('3b3155e99587f80ee3f8b530caa188f6287d42e17140a02a44c6c3d8e45855d7',
         P307 + '/lrat-b35s19-v16/lrat-summary.json',
         '7b8d9eca5dad3cb7b679954bd9fcc20069fd1bce23b421878317e108795aa8ab',
         [REC + '/LO33N20261113/budget34/VERIFY307/data/lrat-b35s19-v16/lrat-results.tsv',
          REC + '/LO33N20261113/budget34/VERIFY307/data/lrat-b35s19-v16/lrat-summary.json']),
}
SIZES = {'P': 812, 'Q': 208, 'U': 35, 'A': 970}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_path(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def exact_line(p):
    try:
        with open(p, 'rb') as f:
            return any(l.rstrip(b'\r\n') == b's VERIFIED UNSAT' for l in f)
    except OSError:
        return False


t0 = time.time()
rep = {'exe': EXE, 'exe_sha_start': sha_path(EXE), 'tables': {}, 'problems': []}
assert rep['exe_sha_start'] == EXE_SHA, 'exe changed'
jobs = {}
for tsv, (tsha, summ, ssha, copies) in TABLES.items():
    t = {'sha': sha_path(tsv), 'summary_sha': sha_path(summ)}
    t['sha_ok'] = t['sha'] == tsha and t['summary_sha'] == ssha
    t['record_copies'] = {c: sha_path(c) for c in copies}
    t['record_copies_equal'] = all(h in (tsha, ssha) for h in t['record_copies'].values())
    n = 0
    with open(tsv, newline='') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            key = tuple(int(x) for x in r['support'].split(','))
            r['_out'] = os.path.join(os.path.dirname(tsv), 'cake', r['job'] + '.out')
            r['_table'] = os.path.basename(os.path.dirname(tsv))
            jobs.setdefault(key, []).append(r)
            n += 1
    t['jobs'] = n
    rep['tables'][tsv] = t
    if not (t['sha_ok'] and t['record_copies_equal']):
        rep['problems'].append(f'table hash {tsv}')

rows, lists_txt = [], []
for B in 'PQUA':
    out = subprocess.run([EXE, 'list', B], capture_output=True)
    assert out.returncode == 0
    lines = out.stdout.decode('ascii').splitlines()
    lists_txt += [f'{B} {l}' for l in lines]
    if len(lines) != SIZES[B]:
        rep['problems'].append(f'block {B}: {len(lines)} rows, expected {SIZES[B]}')
    for k, l in enumerate(lines):
        i, supp = l.split(' ')
        assert int(i) == k
        s = tuple(int(x) for x in supp.split(','))
        if not (all(a < b for a, b in zip(s, s[1:])) and all(0 <= x < 154 for x in s) and 1 <= len(s) <= 16):
            rep['problems'].append(f'{B} {k}: support not well formed')
        rows.append((B, k, s))
open(V + '/data/exe_lists.txt', 'w').write('\n'.join(lists_txt) + '\n')

res, counts, sample = [], {}, {}
LIMIT = int(os.environ.get('LRV_LIMIT', '0'))  # smoke test only: first LIMIT rows of each block
todo = [r for r in rows if not LIMIT or r[1] < LIMIT]
for n, (B, k, s) in enumerate(todo):
    p = subprocess.run([EXE, 'row', B, str(k)], capture_output=True)
    printed = sha_bytes(p.stdout) if p.returncode == 0 and p.stdout else 'NONE'
    js = jobs.get(s, [])
    good, bad, other_hash = [], [], []
    for j in js:
        ok = (j['status'] == 'ACCEPTED' and j['sha_ok'] == 'True' and j['verified_line'] == 'True'
              and j['cnf_sha_recorded'] == j['cnf_sha_actual'] and j['lrat_sha_recorded'] == j['lrat_sha_actual']
              and exact_line(j['_out']))
        (good if ok else bad).append(j['job'])
        if j['cnf_sha_actual'] != printed:
            other_hash.append(j['job'])
    bound = bool(good) and not bad and not other_hash and printed != 'NONE'
    st = 'BOUND' if bound else 'FAIL'
    counts[st] = counts.get(st, 0) + 1
    tabs = sorted(set(j['_table'] for j in js))
    res.append([B, k, ','.join(map(str, s)), len(p.stdout), printed, len(good), len(bad), len(other_hash),
                ';'.join(tabs), st])
    if n % 25 == 0 and js:  # retention sample: fresh hash of the file on disk (decompressed for .zst)
        f = js[0]['cnf']
        if os.path.exists(f):
            fresh = (sha_bytes(subprocess.run(['zstd', '-dc', '-q', f], capture_output=True, check=True).stdout)
                     if f.endswith('.zst') else sha_path(f))
        else:
            fresh = 'MISSING'
        sample[f'{B} {k}'] = {'file': f, 'fresh': fresh, 'equal_printed': fresh == printed}
    if (n + 1) % 200 == 0:
        print(n + 1, counts, round(time.time() - t0), flush=True)

SUF = '_smoke' if LIMIT else ''
with open(V + f'/data/lrv_bind{SUF}.tsv', 'w') as f:
    f.write('block\tindex\tsupport\tbytes\tprinted_sha256\tgood_jobs\tbad_jobs\tother_hash_jobs\ttables\tstatus\n')
    for r in res:
        f.write('\t'.join(map(str, r)) + '\n')

# CaDiCaL controls (COMPUTED, not certification)
ctl = {}
u0 = [str(x) for x in rows[[r[0] for r in rows].index('U')][2]]
for name, args, expect in [('tiny_0_1_2', ['sup', '0', '1', '2'], 10), ('row_U_0', ['row', 'U', '0'], 20),
                           ('U0_minus_last_info', ['sup'] + u0[:-1], None)]:
    cnf = V + f'/data/ctl_{name}.cnf'
    with open(cnf, 'wb') as fo:
        subprocess.run([EXE] + args, stdout=fo, check=True)
    c = subprocess.run(['/usr/bin/cadical', '-q', '-n', cnf], capture_output=True, timeout=600)
    ctl[name] = {'rc': c.returncode, 'expected': expect, 'ok': expect is None or c.returncode == expect,
                 'cnf_sha': sha_path(cnf), 'args': ' '.join(args)}
    os.remove(cnf)

rep['exe_sha_end'] = sha_path(EXE)
rep.update({'rows': len(res), 'counts': counts, 'by_block': {B: sum(1 for r in res if r[0] == B and r[9] == 'BOUND')
                                                            for B in 'PQUA'},
            'distinct_supports': len(set(r[2] for r in res)), 'distinct_printed': len(set(r[4] for r in res)),
            'fresh_sample': sample, 'fresh_sample_all_equal': all(v['equal_printed'] for v in sample.values()),
            'cadical_controls': ctl, 'seconds': round(time.time() - t0, 1)})
rep['ok'] = (rep['exe_sha_end'] == EXE_SHA and not rep['problems'] and counts.get('FAIL', 0) == 0
             and len(res) == 2025 and not LIMIT and rep['fresh_sample_all_equal'] and all(v['ok'] for v in ctl.values()))
json.dump(rep, open(V + f'/data/lrv_bind{SUF}.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in rep.items() if k not in ('fresh_sample',)}, indent=1))
sys.exit(0 if rep['ok'] else 1)
