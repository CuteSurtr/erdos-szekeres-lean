#!/usr/bin/env python3
"""Receipts of a re-checked proof set (24 Nov 2026; generic form of receipts_c6.py): jobs_<SET>.jsonl and
ledger_<SET>.jsonl of recheck_set.py (fresh cake_lpr). A job without "orig" had no earlier cake_lpr run: its
campaign_cake_line is "none" and check does not ask for one (the re-check is then the first cake_lpr acceptance). Per proof: the .zst size and SHA-256 now; the SHA-256 of the decompressed proof
now, which must equal the recorded LRAT hash that the re-check also required; the CNF (kept) and its SHA-256, which
the re-check required of the CNF it built; the campaign's cake_lpr line (orig log); the fresh re-check's line, cake_lpr
and tool hashes. check = OK only if all of that holds. Read-only. Usage: python3 -I receipts_set.py SET OUT.tsv [--jobs N]
"""
import hashlib, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

V = '/home/jay/research/data/verify-20261124'


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()


def sha_zst(p):
    h = hashlib.sha256(); q = subprocess.Popen(['zstd', '-dcq', p], stdout=subprocess.PIPE)
    assert q.stdout is not None
    for b in iter(lambda: q.stdout.read(1 << 22), b''): h.update(b)
    if q.wait() != 0: raise RuntimeError('zstd failed: ' + p)
    return h.hexdigest()


def orig_line(p):
    if not p or not os.path.isfile(p): return ''
    ls = [l.strip() for l in open(p, errors='replace') if l.startswith('s ')]
    return ls[-1] if ls else ''


def one(pair):
    job, led = pair
    p = job['lrat']
    zb, zs, now = os.path.getsize(p), sha_file(p), sha_zst(p)
    cnf = job['cnf'].get('file') or ('base=%s units=%s' % (job['cnf']['base'], job['cnf']['units']))
    ol = orig_line(job.get('orig')) if job.get('orig') else 'none'
    fresh = 'cake_lpr %s %s heap %s MB: %s' % (led['cake_sha256'][:16], led['t'], led['heap'], ' / '.join(led['cake_lines']))
    ok = (led['status'] == 'OK' and led['cake_lines'] == ['s VERIFIED UNSAT'] and now == job['lrat_sha256']
          and led['lrat_sha256'] == job['lrat_sha256'] and led['cnf_sha256'] == job['cnf_sha256']
          and ol == ('s VERIFIED UNSAT' if job.get('orig') else 'none'))
    return [job['set'], job['id'], p, str(zb), zs, now, job['lrat_sha256'], cnf, job['cnf_sha256'], ol, fresh,
            led['tool_sha256'], 'OK' if ok else 'FAIL']


def main():
    name, out = sys.argv[1], sys.argv[2]
    n = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 4
    jobs = {j['id']: j for j in map(json.loads, open(V + '/jobs_%s.jsonl' % name))}
    led = {}
    for r in map(json.loads, open(V + '/ledger_%s.jsonl' % name)):
        led[r['id']] = r                       # the last line per id counts (a retry appends)
    assert set(jobs) == set(led), 'jobs and ledger differ'
    with ThreadPoolExecutor(n) as ex:
        rows = list(ex.map(one, [(jobs[k], led[k]) for k in sorted(jobs)]))
    head = ['set', 'id', 'proof_file', 'zst_bytes', 'zst_sha256', 'lrat_sha256_now', 'lrat_sha256_recorded', 'cnf_kept',
            'cnf_sha256', 'campaign_cake_line', 'independent_recheck', 'recheck_tool_sha256', 'check']
    with open(out + '.tmp', 'w') as f:
        f.write('\t'.join(head) + '\n')
        for r in rows: f.write('\t'.join(r) + '\n')
    os.replace(out + '.tmp', out)
    bad = [r[1] for r in rows if r[-1] != 'OK']
    print(json.dumps({'rows': len(rows), 'ok': len(rows) - len(bad), 'bad': bad[:10],
                      'zst_bytes': sum(int(r[3]) for r in rows), 'tsv_sha256': sha_file(out)}))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
