#!/usr/bin/env python3
"""make_ref.py [OUT.tsv]: run C6UPPER/encb/gen_b2.py on a grid of small (m, K, t) and record the SHA-256 of each CNF.

Grid: every m in 3..8, K in 4..2m, t in 1..4 (192 instances), plus cheap extras (edge cases K <= 3, t = 0,
m in {1, 2, 9, 10}, and t = 5..8 at K = 8). Each CNF is written to a temporary directory, hashed and deleted
together with its .map.json. An instance on which gen_b2.py raises is recorded with status FAIL:<exception>
(the Lean emitter must then refuse it too). gen_b2.py's own SHA-256 is checked first.
Columns: m K t status sha256 bytes nv ncl unit cond chain seconds.
Run at nice 10 inside one memory-capped scope (see ../README.md).
"""
import hashlib, json, os, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.normpath(os.path.join(HERE, '..', '..', 'C6UPPER', 'encb', 'gen_b2.py'))
GEN_SHA = '3d47459a9723b5f7344205f3f2d7463e0be00b41c5070155e5da8dbf78fd40ba'


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def grid():
    seen = []
    def add(m, K, t):
        if (m, K, t) not in seen:
            seen.append((m, K, t))
    for m in range(3, 9):
        for K in range(4, 2 * m + 1):
            for t in range(1, 5):
                add(m, K, t)
    # extras: edge cases and a few larger layer counts at K = 8
    for (m, K, t) in [(3, 3, 3), (4, 3, 3), (5, 2, 3), (6, 3, 4), (7, 1, 2), (6, 0, 2),
                      (3, 4, 0), (6, 8, 0), (7, 8, 0),
                      (2, 4, 1), (2, 4, 3), (2, 5, 4), (1, 4, 2),
                      (9, 4, 2), (9, 8, 3), (10, 4, 2), (10, 8, 3)]:
        add(m, K, t)
    for m in range(3, 9):
        for t in (5, 6):
            add(m, 8, t)
    for m in (6, 7):
        for t in (7, 8):
            add(m, 8, t)
    return seen


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'hashes.tsv')
    got = sha_file(GEN)
    if got != GEN_SHA:
        sys.exit('gen_b2.py sha256 %s != recorded %s' % (got, GEN_SHA))
    rows = ['# gen_b2.py %s  (%s)' % (got, os.path.relpath(GEN, os.path.dirname(out))),
            '# m\tK\tt\tstatus\tsha256\tbytes\tnv\tncl\tunit\tcond\tchain\tseconds']
    with tempfile.TemporaryDirectory(prefix='encb_ref_') as td:
        for (m, K, t) in grid():
            cnf = os.path.join(td, 'x.cnf')
            t0 = time.time()
            r = subprocess.run([sys.executable, GEN, str(m), str(K), str(t), cnf], capture_output=True, text=True)
            dt = time.time() - t0
            if r.returncode == 0:
                s = json.loads(r.stdout.strip().splitlines()[-1])
                c = s['counts']
                rows.append('\t'.join(map(str, [m, K, t, 'OK', sha_file(cnf), os.path.getsize(cnf), s['nv'],
                                                 s['ncl'], c['unit'], c['cond'], c['chain'], '%.2f' % dt])))
            else:
                last = (r.stderr.strip().splitlines() or ['?'])[-1]
                exc = last.split(':')[0].split()[-1] if last else '?'
                rows.append('\t'.join(map(str, [m, K, t, 'FAIL:' + exc] + ['-'] * 7 + ['%.2f' % dt])))
            for p in (cnf, cnf + '.map.json'):
                if os.path.exists(p):
                    os.remove(p)
            print(rows[-1], flush=True)
    with open(out, 'w') as f:
        f.write('\n'.join(rows) + '\n')


main()
