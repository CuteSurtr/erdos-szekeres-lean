#!/usr/bin/env python3
"""reverify.py -- re-run cake_lpr with a larger heap on cubes whose first check ran out of CakeML heap.

The running driver (drive.py) checks each UNSAT leaf with heap max(2000, 1200 + 0.9 * LRAT MB); some
proofs need more ("CakeML heap space exhausted").  This loop finds results.tsv rows with status
cake_failed whose .cake output reports heap exhaustion, re-runs cake_lpr on the same CNF and LRAT
(hashes recomputed and compared with the row), and on the exact line 's VERIFIED UNSAT' appends a
'verified' row (same columns) and archives the proof like the driver (zstd, round trip by hash).
"""
import hashlib, os, subprocess, sys, time
D = os.path.dirname(os.path.abspath(__file__)); CU = D + '/cubes'; CAKE = D + '/bin/cake_lpr'
HEAP = int(os.environ.get('HEAP', '6000'))

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()

def log(*a):
    with open(CU + '/reverify.log', 'a') as f: print(time.strftime('%H:%M:%S'), *a, file=f, flush=True)

done = set()
while not os.path.exists(CU + '/STOP_REVERIFY'):
    rows = [l.rstrip('\n').split('\t') for l in open(CU + '/results.tsv')] if os.path.exists(CU + '/results.tsv') else []
    ver = {r[0] for r in rows if len(r) > 3 and r[3] == 'verified'}
    todo = [r for r in rows if len(r) > 9 and r[3] == 'cake_failed' and r[0] not in ver and r[0] not in done]
    if not todo:
        time.sleep(20); continue
    r = todo[0]; jid = r[0]; done.add(jid)
    cnf, lrat, cake = CU + '/' + jid + '.cnf', CU + '/' + jid + '.lrat', CU + '/' + jid + '.cake'
    if 'heap space exhausted' not in open(cake, errors='replace').read():
        log('skip (not a heap failure)', jid); continue
    if sha(cnf) != r[6] or sha(lrat) != r[8]:
        log('HASH MISMATCH, not re-checked', jid); continue
    t = time.time()
    p = subprocess.run(['nice', '-n', '5', CAKE, '--CML_HEAP_SIZE=%d' % HEAP, '--CML_STACK_SIZE=200', cnf, lrat],
                       capture_output=True, text=True)
    open(cake, 'w').write(p.stdout + p.stderr)
    ok = any(l.strip() == 's VERIFIED UNSAT' for l in p.stdout.splitlines())
    wall = round(time.time() - t, 1)
    log('cake', jid, 'VERIFIED' if ok else 'REJECTED rc=%d' % p.returncode, wall, 's heap', HEAP)
    if not ok: continue
    r2 = list(r); r2[3] = 'verified'; r2[9] = 'VERIFIED'; r2[10] = str(wall)
    while len(r2) < 12: r2.append('')
    r2[11] = str(HEAP)
    with open(CU + '/results.tsv', 'a') as f: f.write('\t'.join(r2) + '\n')
    z = lrat + '.zst'
    subprocess.run(['nice', '-n', '10', 'zstd', '-q', '-T2', '-3', '-f', lrat, '-o', z])
    d = subprocess.run('zstd -dc "%s" | shasum -a 256' % z, shell=True, capture_output=True, text=True).stdout.split()[0]
    if d == r[8]:
        os.remove(lrat); os.remove(cnf); log('archived', jid, 'zst ok')
    else:
        log('ZSTD MISMATCH', jid)
