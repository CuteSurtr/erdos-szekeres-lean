#!/usr/bin/env python3
"""M9 hash binding (trust item E1) for ae33-lean.

For every pair index i < 203: run `ae33print cnf i` (the exe prints exactly the Lean string `cnfText i`), hash the
stream with SHA-256, and compare with the recorded CNF hashes of that pair:
  - hashes_203.tsv (worker record, its own hash pinned in that work dir's SHA256SUMS),
  - L18 e72/cert/certify.jsonl (the certification run: CNF hash -> LRAT hash -> verdict),
  - L18 e72/summary.jsonl (L18's encoder run).
Also: header `p cnf 961 <clauses>` vs the recorded clause count; the exe's pair name vs the table row; verdict lines
(exactly one line equal to `s VERIFIED UNSAT`) in L18's cert/<name>.cake.out and in the worker's fresh
cake/<name>.cake.out (which must have no other line); LRAT hash chain certify.jsonl = hashes_203.tsv.
Controls: `ae33print pts` hashes to ae33.txt's SHA-256; out-of-range / malformed indices are refused (rc 1, no
output); the exe hashes group the pairs exactly as the recorded hashes do (the record has 194 distinct CNFs for 203
pairs: 9 pairs of pairs share a CNF); the exe file hash is the same at start and end. (Version 1 of this script
required 203 distinct hashes, a wrong expectation; its summary is kept as m9_hash_binding.summary.v1.json.)
Resumable: rows already in the TSV are skipped. Stops (exit 3) if the YIELD file appears.
"""
import hashlib, json, os, subprocess, sys, time

D = '/home/jay/research/data/formalize-20261122/ae33-lean'
X = D + '/build/bin/ae33print'
L18 = '/home/jay/research/data/roadmap-20261115/pm1115/l1118/e72'
AE = '/home/jay/research/data/lower-20261121/ae33'
YIELD = '/home/jay/research/data/agents-20261121/YIELD'
OUT = D + '/logs/m9_hash_binding.tsv'
SUMMARY = D + '/logs/m9_hash_binding.summary.json'
AE33_TXT_SHA = 'cb6a5327b26b869ab39baadf0ade737882f8473dc1ccfbd377d06405a59eb54d'
HT_SHA = '90cbb85d506d390e8d6a226296cc7581eeecee10611dce20f2f896031dc2b010'
VERDICT = 's VERIFIED UNSAT'


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def run_exe(args):
    p = subprocess.Popen([X] + args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    h = hashlib.sha256()
    first, n = b'', 0
    for b in iter(lambda: p.stdout.read(1 << 20), b''):
        if n == 0:
            first = b.split(b'\n', 1)[0]
        h.update(b)
        n += len(b)
    return p.wait(), h.hexdigest(), first.decode('ascii', 'replace'), n


def verdict_lines(p):
    if not os.path.exists(p):
        return -1, -1
    lines = open(p, encoding='utf-8', errors='replace').read().splitlines()
    return sum(1 for l in lines if l == VERDICT), len(lines)


def main():
    exe_sha0 = sha_file(X)
    ht_rows = [l.rstrip('\n').split('\t') for l in open(AE + '/hashes_203.tsv') if not l.startswith('#')]
    assert len(ht_rows) == 203
    cert, summ = {}, {}
    for line in open(L18 + '/cert/certify.jsonl'):
        j = json.loads(line)
        cert.setdefault(os.path.basename(j['cnf'])[:-4], []).append(j)
    for line in open(L18 + '/summary.jsonl'):
        j = json.loads(line)
        summ.setdefault(j['name'], []).append(j)
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            if l and l[0].isdigit():
                done.add(int(l.split('\t')[0]))
    else:
        with open(OUT, 'w') as f:
            f.write('i\tname\tsha_exe\tbytes\theader\tsha_ht\tsha_certify\tsha_summary\tclauses_ht\tclauses_summary\t'
                    'cake_l18\tcake_fresh\tlrat_chain\twall_s\tMATCH\n')
    for i in range(203):
        if os.path.exists(YIELD):
            print('YIELD present; stopping at', i, flush=True)
            sys.exit(3)
        if i in done:
            continue
        r = ht_rows[i]
        nm = r[0]
        nmexe = subprocess.run([X, 'name', str(i)], capture_output=True, text=True).stdout.strip()
        t0 = time.time()
        rc, sha, hdr, nbytes = run_exe(['cnf', str(i)])
        wall = time.time() - t0
        c = cert.get(nm, [])
        s = summ.get(nm, [])
        sha_c = c[0]['cnf_sha256'] if len(c) == 1 else 'MISSING_OR_DUP'
        sha_s = s[0]['cnf_sha256'] if len(s) == 1 else 'MISSING_OR_DUP'
        cl_s = s[0]['stats']['clauses'] if len(s) == 1 else -1
        v18, _ = verdict_lines(f'{L18}/cert/{nm}.cake.out')
        vf, nf = verdict_lines(f'{AE}/cake/{nm}.cake.out')
        lrat_ok = len(c) == 1 and c[0]['lrat_sha256'] == r[6] and c[0]['verdict'] == VERDICT
        ok = (rc == 0 and nmexe == nm and sha == r[4] == sha_c == sha_s and hdr == f'p cnf 961 {r[5]}'
              and int(r[5]) == cl_s and v18 == 1 and vf == 1 and nf == 1 and lrat_ok)
        with open(OUT, 'a') as f:
            f.write(f'{i}\t{nm}\t{sha}\t{nbytes}\t{hdr}\t{r[4]}\t{sha_c}\t{sha_s}\t{r[5]}\t{cl_s}\t{v18}\t{vf}/{nf}\t'
                    f'{int(lrat_ok)}\t{wall:.1f}\t{"MATCH" if ok else "FAIL"}\n')
        print(i, nm, 'MATCH' if ok else 'FAIL', f'{wall:.1f}s', flush=True)
    # summary and controls
    rows = [l.rstrip('\n').split('\t') for l in open(OUT) if l and l[0].isdigit()]
    rows.sort(key=lambda r: int(r[0]))
    rc_pts, sha_pts, _, _ = run_exe(['pts'])
    ctl = {}
    for args in (['cnf', '203'], ['cnf', 'x'], ['cnf', '-1'], []):
        p = subprocess.run([X] + args, capture_output=True)
        ctl[' '.join(args) or '(no args)'] = {'rc': p.returncode, 'stdout_bytes': len(p.stdout)}
    shas = [r[2] for r in rows]
    # the record itself has duplicate CNFs (9 pairs of pairs, e.g. ae_d15_26 / ae_d15_27); compare the structure
    groups_exe, groups_rec = {}, {}
    for r in rows:
        groups_exe.setdefault(r[2], set()).add(r[1])
        groups_rec.setdefault(r[5], set()).add(r[1])
    same_groups = sorted(map(sorted, groups_exe.values())) == sorted(map(sorted, groups_rec.values()))
    dups = sorted(sorted(g) for g in groups_rec.values() if len(g) > 1)
    summary = {
        'time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'exe_sha256_start': exe_sha0, 'exe_sha256_end': sha_file(X),
        'hashes_203_tsv_sha256': sha_file(AE + '/hashes_203.tsv'), 'hashes_203_tsv_expected': HT_SHA,
        'rows': len(rows), 'match': sum(1 for r in rows if r[-1] == 'MATCH'),
        'fail': [r[1] for r in rows if r[-1] != 'MATCH'],
        'distinct_exe_hashes': len(set(shas)), 'distinct_recorded_hashes': len(groups_rec),
        'duplicate_groups_identical': same_groups, 'recorded_duplicate_groups': dups,
        'pts_rc': rc_pts, 'pts_sha256': sha_pts, 'pts_equals_ae33_txt': sha_pts == AE33_TXT_SHA,
        'refusal_controls': ctl,
        'total_wall_s': round(sum(float(r[13]) for r in rows), 1),
    }
    summary['PASS'] = (summary['rows'] == 203 and summary['match'] == 203 and same_groups
                       and summary['distinct_exe_hashes'] == summary['distinct_recorded_hashes']
                       and summary['pts_equals_ae33_txt'] and exe_sha0 == summary['exe_sha256_end']
                       and summary['hashes_203_tsv_sha256'] == HT_SHA
                       and all(v['rc'] == 1 and v['stdout_bytes'] == 0 for v in ctl.values()))
    json.dump(summary, open(SUMMARY, 'w'), indent=1)
    print(json.dumps(summary, indent=1))
    return 0 if summary['PASS'] else 2


if __name__ == '__main__':
    sys.exit(main())
