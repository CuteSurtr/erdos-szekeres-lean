#!/usr/bin/env python3
"""M9 hash binding (trust items E1, E2) for the four Res118 row blocks. Read-only on every input.

For every row I of every block B in P, Q, U, A (the Lean lists, read through `rowprint list B`):
  1. printed = sha256sum of `rowprint row B I` (the exact string `RowEnc.rowText rows[I]`);
  2. the certified jobs of that support in the two T4 re-checks (ES307 v169: 1,994 jobs; VERIFY307 b35s19-v16:
     1,057 jobs; both summaries are hash-equal to the record copies): every such job must be ACCEPTED, with
     recorded = actual CNF hash, a fresh sha256sum of the CNF file on disk (zstd -dc for .zst) equal to it, and the
     exact line `s VERIFIED UNSAT` in its cake_lpr stdout;
  3. the original certification records agree: pool rows -> audit/pool_inventory.json cnf_sha256; cut rows -> the
     cut directory's receipt.json (generation.cnf_sha256, verdict) and its cake.log (exact line);
  4. printed == every recorded and fresh hash of step 2-3.
A row is BOUND only if all checks pass and it has at least one job. Writes logs/m9_binding.tsv and
logs/m9_binding.summary.json. Controls: out-of-range index and unknown block refused (rc 1, empty stdout); a
support with one entry changed prints a different hash.
usage: hash_binding.py [limit_per_block]
"""
import csv, hashlib, json, os, subprocess, sys, time

D = '/home/jay/research/data/formalize-20261122/res118-rowblocks'
EXE = D + '/build/bin/rowprint'
P307 = '/home/jay/research/data/roadmap-20261115/pm1115/p307v'
TSVS = [P307 + '/lrat-b35s20-v169/lrat-results.tsv', P307 + '/lrat-b35s19-v16/lrat-results.tsv']
SUMS = {P307 + '/lrat-b35s20-v169/lrat-summary.json': 'f80a720e3216b8b035fef6ee8713d0cfb0255772fb32ce5da78f1aa4bf3c1ec4',
        P307 + '/lrat-b35s19-v16/lrat-summary.json': '7b8d9eca5dad3cb7b679954bd9fcc20069fd1bce23b421878317e108795aa8ab'}
REC = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results'
POOLINV = REC + '/LO33N20261113/budget34/audit/pool_inventory.json'
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else None


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    assert r.returncode == 0, (cmd, r.stderr)
    return r.stdout


def sha_file(p):
    if p.endswith('.zst'):
        out = sh(f"zstd -dc -q '{p}' | sha256sum")
    else:
        out = sh(f"sha256sum '{p}'")
    return out.split()[0]


def exact_line(path):
    try:
        return 's VERIFIED UNSAT' in open(path).read().splitlines()
    except OSError:
        return False


t0 = time.time()
summary = {'exe_sha256': sha_file(EXE), 'inputs': {}}
for p, h in SUMS.items():
    summary['inputs'][p] = {'sha256': sha_file(p), 'expected': h}
    assert summary['inputs'][p]['sha256'] == h, p
for p in TSVS + [POOLINV]:
    summary['inputs'][p] = {'sha256': sha_file(p)}

jobs = {}
for tsv in TSVS:
    for r in csv.DictReader(open(tsv), delimiter='\t'):
        key = tuple(int(x) for x in r['support'].split(','))
        r['_cake'] = os.path.join(os.path.dirname(tsv), 'cake', r['job'] + '.out')
        r['_tsv'] = tsv
        jobs.setdefault(key, []).append(r)
pool = {tuple(r['support']): r for r in json.load(open(POOLINV))['rows']}

fresh_cache = {}
rows_out = []
counts = {}
for B in 'PQUA':
    lines = [l for l in sh(f'{EXE} list {B}').splitlines() if l]
    if LIMIT:
        lines = lines[:LIMIT]
    for line in lines:
        i, supp = line.split(' ')
        key = tuple(int(x) for x in supp.split(','))
        printed = sh(f'{EXE} row {B} {i} | sha256sum').split()[0]
        probs = []
        js = jobs.get(key, [])
        if not js:
            probs.append('no job')
        recs = []
        for j in js:
            if j['status'] != 'ACCEPTED' or j['sha_ok'] != 'True' or j['verified_line'] != 'True':
                probs.append(f"job {j['job']} status {j['status']}")
            if j['cnf_sha_recorded'] != j['cnf_sha_actual']:
                probs.append(f"job {j['job']} recorded != actual")
            if not exact_line(j['_cake']):
                probs.append(f"job {j['job']} no exact line in {j['_cake']}")
            f = j['cnf']
            if f not in fresh_cache:
                fresh_cache[f] = sha_file(f) if os.path.exists(f) else 'MISSING'
            recs += [j['cnf_sha_recorded'], j['cnf_sha_actual'], fresh_cache[f]]
            if j['source'] == 'pool':
                pr = pool.get(key)
                if pr is None:
                    probs.append('pool row missing in inventory')
                else:
                    recs.append(pr['cnf_sha256'])
            else:
                dd = os.path.dirname(f)
                try:
                    rc = json.load(open(os.path.join(dd, 'receipt.json')))
                    recs.append(rc['generation']['cnf_sha256'])
                    if rc.get('verdict') != 's VERIFIED UNSAT':
                        probs.append(f'receipt verdict {rc.get("verdict")}')
                    if tuple(rc['support']) != key:
                        probs.append('receipt support differs')
                except (OSError, KeyError) as e:
                    probs.append(f'receipt {dd}: {e}')
                if not exact_line(os.path.join(dd, 'cake.log')):
                    probs.append(f'no exact line in {dd}/cake.log')
        bad = sorted(set(h for h in recs if h != printed))
        if bad:
            probs.append('hash mismatch ' + ','.join(x[:16] for x in bad))
        status = 'BOUND' if not probs else 'FAIL'
        counts[status] = counts.get(status, 0) + 1
        rows_out.append([B, i, supp, len(key), printed, len(js), ';'.join(sorted(set(j['source'] for j in js))),
                         status, ' | '.join(probs)])
        if len(rows_out) % 100 == 0:
            print(len(rows_out), counts, round(time.time() - t0), flush=True)

with open(D + '/logs/m9_binding.tsv', 'w') as f:
    f.write('block\tindex\tsupport\tn\tprinted_sha256\tjobs\tsources\tstatus\tproblems\n')
    for r in rows_out:
        f.write('\t'.join(map(str, r)) + '\n')

# controls
ctl = {}
r = subprocess.run([EXE, 'row', 'P', '812'], capture_output=True)
ctl['out_of_range_refused'] = r.returncode == 1 and r.stdout == b''
r = subprocess.run([EXE, 'row', 'X', '0'], capture_output=True)
ctl['unknown_block_refused'] = r.returncode == 1 and r.stdout == b''
first = rows_out[0]
mut = [int(x) for x in first[2].split(',')]
mut[-1] += 1
ctl['mutated_support'] = ','.join(map(str, mut))
ctl['mutated_hash_differs'] = sh(f"{EXE} sup {' '.join(map(str, mut))} | sha256sum").split()[0] != first[4]
summary.update({'rows': len(rows_out), 'counts': counts,
                'distinct_supports': len(set(r[2] for r in rows_out)),
                'fresh_files_hashed': len(fresh_cache), 'controls': ctl,
                'seconds': round(time.time() - t0, 1), 'limit_per_block': LIMIT})
json.dump(summary, open(D + '/logs/m9_binding.summary.json', 'w'), indent=1)
print(json.dumps(summary, indent=1))
sys.exit(0 if counts.get('FAIL', 0) == 0 and all(v for k, v in ctl.items() if k != 'mutated_support') else 1)
