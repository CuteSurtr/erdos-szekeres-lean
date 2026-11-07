#!/usr/bin/env python3
"""Solve and certify the other half of the C6UPPER encoder-B split: base + NOT Y(1,2) + the 32 sign patterns of
Y(1,3),Y(1,4),Y(2,3),Y(2,4),Y(3,4) (6 November 2026). Together with the 32 cubes base + Y(1,2) + pattern that
cake_lpr accepted in the hash-bound replay (/path/to/data/c6upper-replay-20261106, results.tsv, enc B),
the 64 cubes cover every assignment of the six variables, so the encoder-B base formula itself is UNSAT and the
reflection lemma (Y(1,2) without loss of generality) is no longer needed for the sixfold upper bound.

Checks, in order (any failure stops before solving):
  * SHA-256 of /usr/bin/cadical and of cake_lpr equal the replay's recorded tool hashes;
  * the base CNF (the replay's regenerated B_m6K8t11.cnf) has the recorded SHA-256 479e31a9...;
  * the 32 new cubes are written as header(nv, nc+6) + exact base body + units [-Y(1,2)] + pattern
    (the layout of C6UPPER/tools/mkcubes.py with the first unit negated), and verify_cover64.py checks them
    together with the 32 replayed Y(1,2) cubes (whose hashes must equal the ACCEPTED rows of the replay).
Then per cube: CaDiCaL 2.1.3 (text LRAT) -> SHA-256 of the proof -> cake_lpr; only the exact line
's VERIFIED UNSAT' counts (cake_lpr exits 0 even when it rejects). Accepted proofs are kept as .lrat.zst.
Restart-safe: a cube with an ACCEPTED row is skipped. Env: LANES (CaDiCaL lanes, default 4), CAKE (concurrent
cake_lpr runs, default 1).
"""
import os, sys, json, time, hashlib, itertools, threading, subprocess
from concurrent.futures import ThreadPoolExecutor

W = os.path.dirname(os.path.abspath(__file__))
R = '/path/to/repo/cloud/es7-2026-10-19/results'
REPLAY = '/path/to/data/c6upper-replay-20261106'
BASE = REPLAY + '/B/B_m6K8t11.cnf'
META = R + '/C6UPPER/encb/B_m6K8t11.meta.json'
BASE_SHA = '479e31a9e8d58d752c86b9abf02fb799c10615a7e61a88f132c49734674f37fc'
CAD, CAD_SHA = '/usr/bin/cadical', '4acf586001aa286dff6e1a390a273023c3160f0175aba2693e3e6a0065089e70'
CAKE_BIN = '/path/to/tools/cake_lpr/cake_lpr'
CAKE_SHA = 'c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54'
CUBES = W + '/cubes'
TSV, LOG = W + '/results.tsv', W + '/run.log'
LANES = int(os.environ.get('LANES', '4')); NCAKE = int(os.environ.get('CAKE', '1'))
lock = threading.Lock(); cake_sem = threading.Semaphore(NCAKE)
HEAD = 'cube\tunits\tcnf_sha256\tcadical_rc\tsolve_s\tproof_sha256\tproof_bytes\tverdict\tcake_line\tcake_s\tzst_sha256\tdate\n'


def log(m):
    with lock:
        with open(LOG, 'a') as f: f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + m + '\n')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()


def consistent(bits):
    """True if NOT Y(1,2) plus this pattern is a total order on {1,2,3,4} (Y(i,j) true means i before j)."""
    want = {(1, 2): False}
    want.update({p: b == 1 for p, b in zip(((1, 3), (1, 4), (2, 3), (2, 4), (3, 4)), bits)})
    for perm in itertools.permutations((1, 2, 3, 4)):
        pos = {v: i for i, v in enumerate(perm)}
        if all((pos[i] < pos[j]) == v for (i, j), v in want.items()): return True
    return False


def prepare():
    for p, want in ((CAD, CAD_SHA), (CAKE_BIN, CAKE_SHA)):
        got = sha(p)
        if got != want: log('TOOL HASH MISMATCH %s %s (want %s); stopped' % (p, got, want)); return None
    log('tool hashes OK: cadical %s, cake_lpr %s' % (CAD_SHA[:12], CAKE_SHA[:12]))
    got = sha(BASE)
    if got != BASE_SHA: log('BASE HASH MISMATCH %s; stopped' % got); return None
    log('base CNF hash OK %s' % got)
    Y = json.load(open(META))['Y']
    y12 = Y['1,2']; cv = [Y[k] for k in ('1,3', '1,4', '2,3', '2,4', '3,4')]
    raw = open(BASE, 'rb').read()
    hdr, body = raw.split(b'\n', 1)
    p, c, nv, nc = hdr.split()
    if (p, c) != (b'p', b'cnf'): log('bad base header; stopped'); return None
    os.makedirs(CUBES, exist_ok=True)
    jobs = []
    for bits in itertools.product((1, 0), repeat=5):
        units = [-y12] + [v if b else -v for v, b in zip(cv, bits)]
        name = 'n' + ''.join(map(str, bits))
        fn = CUBES + '/' + name + '.cnf'
        data = b'p cnf %s %d\n' % (nv, int(nc) + len(units)) + body
        if not body.endswith(b'\n'): data += b'\n'
        data += b''.join(b'%d 0\n' % u for u in units)
        if not os.path.exists(fn) or open(fn, 'rb').read() != data:
            with open(fn + '.tmp', 'wb') as g: g.write(data)
            os.replace(fn + '.tmp', fn)
        jobs.append((name, ' '.join(map(str, units)), consistent(bits)))
    r = subprocess.run([sys.executable, W + '/verify_cover64.py', BASE, META, CUBES, REPLAY + '/B/cubes',
                        REPLAY + '/results.tsv'], capture_output=True, text=True)
    open(W + '/verify_cover64.log', 'w').write(r.stdout + r.stderr)
    if r.returncode != 0 or 'cover complete' not in r.stdout:
        log('verify_cover64 FAILED: %s' % (r.stdout + r.stderr).strip()[-400:]); return None
    log('verify_cover64: ' + r.stdout.strip().splitlines()[-1])
    with open(W + '/cubes.sha256', 'w') as g:
        for name, _, _ in jobs: g.write('%s  cubes/%s.cnf\n' % (sha(CUBES + '/' + name + '.cnf'), name))
    log('%d cube CNFs written; %d are consistent phase orders' % (len(jobs), sum(j[2] for j in jobs)))
    return jobs


def done():
    out = set()
    if os.path.exists(TSV):
        for l in open(TSV):
            f = l.rstrip('\n').split('\t')
            if len(f) > 7 and f[7] == 'ACCEPTED': out.add(f[0])
    return out


def one(name, units):
    cnf, lrat = CUBES + '/' + name + '.cnf', CUBES + '/' + name + '.lrat'
    cnf_sha = sha(cnf)
    t0 = time.time()
    with open(CUBES + '/' + name + '.cadical.out', 'w') as o:
        rc = subprocess.call([CAD, '-q', '--lrat', '--binary=false', cnf, lrat], stdout=o, stderr=subprocess.STDOUT)
    dt = time.time() - t0
    row = [name, units, cnf_sha, str(rc), '%.1f' % dt]
    if rc != 20 or not os.path.exists(lrat):
        row += ['', '', 'NOT-UNSAT', '', '', '', time.strftime('%F %T')]
        with lock: open(TSV, 'a').write('\t'.join(row) + '\n')
        log('%s cadical rc %d -- NOT UNSAT' % (name, rc)); return
    ph, pb = sha(lrat), os.path.getsize(lrat)
    with cake_sem:
        t1 = time.time()
        r = subprocess.run([CAKE_BIN, '--CML_HEAP_SIZE=8000', '--CML_STACK_SIZE=4000', cnf, lrat],
                           capture_output=True, text=True)
        ct = time.time() - t1
    open(CUBES + '/' + name + '.cake.log', 'w').write(r.stdout + r.stderr)
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith('s ')]
    line = lines[0].strip() if lines else ''
    verdict = 'ACCEPTED' if lines and all(l.strip() == 's VERIFIED UNSAT' for l in lines) else 'REJECTED'
    zh = ''
    if verdict == 'ACCEPTED':
        subprocess.run(['zstd', '-q', '-3', '-T1', '--rm', '-f', lrat, '-o', lrat + '.zst'])
        zh = sha(lrat + '.zst') if os.path.exists(lrat + '.zst') else ''
    row += [ph, str(pb), verdict, line, '%.1f' % ct, zh, time.strftime('%F %T')]
    with lock: open(TSV, 'a').write('\t'.join(row) + '\n')
    log('%s UNSAT %.0fs proof %s (%d bytes) cake %.0fs %s' % (name, dt, ph[:12], pb, ct, verdict))


def main():
    if not os.path.exists(TSV): open(TSV, 'w').write(HEAD)
    log('start pid %d, lanes %d, cake %d' % (os.getpid(), LANES, NCAKE))
    jobs = prepare()
    if jobs is None: sys.exit(1)
    d = done()
    todo = sorted((j for j in jobs if j[0] not in d), key=lambda j: (not j[2], j[0]))
    log('%d cubes to do (%d already accepted)' % (len(todo), len(d)))
    with ThreadPoolExecutor(LANES) as ex:
        for fut in [ex.submit(one, n, u) for n, u, _ in todo]: fut.result()
    acc = done()
    msg = '%s: %d of 32 NOT-Y(1,2) cube proofs accepted by cake_lpr, hash-bound (results.tsv)' % (time.strftime('%F %T'), len(acc))
    log(msg); open(W + '/SUMMARY.txt', 'w').write(msg + '\n')


if __name__ == '__main__':
    main()
