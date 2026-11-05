#!/usr/bin/env python3
"""Hash-bound cake_lpr replay of all 64 C6UPPER cube proofs (32 per encoder), one core, restart-safe.

For each encoder: regenerate the base CNF and require its recorded SHA-256 (C6UPPER/SHA256SUMS.txt); build the 32 cubes
with C6UPPER/tools/mkcubes.py; run C6UPPER/tools/verify_cover.py; require every cube CNF's recorded SHA-256.
Then, one cube at a time: CaDiCaL (system build, text LRAT) -> SHA-256 of the proof -> cake_lpr; only the line
's VERIFIED UNSAT' counts (cake_lpr exits 0 even when it rejects). Each row of results.tsv binds encoder, cube, CNF hash,
proof hash and verdict. Accepted proofs are kept, compressed with zstd (never deleted). A cube with an ACCEPTED row is
skipped on restart. Any hash mismatch stops that encoder before solving.
"""
import os, sys, subprocess, hashlib, time, re
W = os.path.dirname(os.path.abspath(__file__))
R = '/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results'
T = R + '/C6UPPER'
CAKE = '/home/jay/research/sat/tools/cake_lpr/cake_lpr'
CAD = '/usr/bin/cadical'
TSV = W + '/results.tsv'
LOG = W + '/replay.log'

def log(m):
    with open(LOG, 'a') as f: f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + m + '\n')

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()

def recorded():
    """name -> sha256 for the CNF lines, and cube -> raw proof sha for the two LRAT sections"""
    cnf, prA, prB, sec = {}, {}, {}, None
    for l in open(T + '/SHA256SUMS.txt'):
        if l.startswith('#'):
            sec = 'prA' if l.startswith('# LRAT proofs') else 'prB' if l.startswith('# encoder-B LRAT') else 'other'
            continue
        f = l.split()
        if not f: continue
        if sec in ('prA', 'prB') and len(f) >= 2: (prA if sec == 'prA' else prB)[f[0].replace('B/', '')] = f[1]
        elif len(f) == 2 and f[1].endswith('.cnf'): cnf[f[1]] = f[0]
    return cnf, prA, prB

def run(cmd, **kw):
    log('$ ' + ' '.join(cmd)); return subprocess.run(cmd, **kw)

def prepare(enc, rec):
    d = os.path.join(W, enc); os.makedirs(d, exist_ok=True)
    if enc == 'A':
        base, meta, key, pre = d + '/m6K8t11.cnf', d + '/m6K8t11.cnf.json', 'm6K8t11.cnf', ''
        gen = ['python3', R + '/C7UPPER/gen.py', '6', '8', '11', base]
    else:
        base, meta, key, pre = d + '/B_m6K8t11.cnf', T + '/encb/B_m6K8t11.meta.json', 'B_m6K8t11.cnf', 'B/'
        gen = ['python3', T + '/encb/gen_b2.py', '6', '8', '11', base]
    ok_flag = d + '/PREPARED'
    if os.path.exists(ok_flag): return True
    if not os.path.exists(base) or sha(base) != rec[key]:
        run(gen, cwd=d, stdout=open(d + '/gen.log', 'w'), stderr=subprocess.STDOUT)
    h = sha(base)
    if h != rec[key]:
        log('%s BASE HASH MISMATCH %s (recorded %s); encoder stopped' % (enc, h, rec[key])); return False
    log('%s base CNF hash OK %s' % (enc, h))
    os.makedirs(d + '/cubes', exist_ok=True)
    run(['python3', T + '/tools/mkcubes.py', base, meta, d + '/cubes'], stdout=open(d + '/mkcubes.log', 'w'), stderr=subprocess.STDOUT)
    r = run(['python3', T + '/tools/verify_cover.py', base, meta, d + '/cubes'], capture_output=True, text=True)
    open(d + '/verify_cover.log', 'w').write(r.stdout + r.stderr)
    if r.returncode != 0 or 'cover complete' not in r.stdout:
        log('%s verify_cover FAILED: %s' % (enc, (r.stdout + r.stderr).strip()[-300:])); return False
    log('%s verify_cover: %s' % (enc, r.stdout.strip().splitlines()[-1]))
    bad = 0
    for f in sorted(os.listdir(d + '/cubes')):
        if not f.endswith('.cnf'): continue
        want = rec.get(pre + f)
        got = sha(d + '/cubes/' + f)
        if want != got: bad += 1; log('%s cube %s HASH MISMATCH %s (recorded %s)' % (enc, f, got, want))
    if bad: log('%s %d cube hash mismatches; encoder stopped' % (enc, bad)); return False
    log('%s all cube CNF hashes match the record' % enc)
    open(ok_flag, 'w').write(time.strftime('%Y-%m-%d %H:%M:%S\n'))
    return True

def done_rows():
    out = set()
    if os.path.exists(TSV):
        for l in open(TSV):
            f = l.rstrip('\n').split('\t')
            if len(f) > 8 and f[8] == 'ACCEPTED': out.add((f[0], f[1]))
    return out

def main():
    if not os.path.exists(TSV):
        open(TSV, 'w').write('enc\tcube\tcnf_sha256\tcadical_rc\tsolve_s\tproof_sha256\tproof_bytes\tsame_as_archived\tverdict\tcake_line\tzst_sha256\tdate\n')
    rec, prA, prB = recorded()
    v = subprocess.run([CAD, '--version'], capture_output=True, text=True).stdout.strip()
    log('replay start pid %d; cadical %s; cake_lpr %s' % (os.getpid(), v, CAKE))
    done = done_rows()
    for enc in ('A', 'B'):
        if not prepare(enc, rec): continue
        d = os.path.join(W, enc, 'cubes')
        arch = prA if enc == 'A' else prB
        for f in sorted(x for x in os.listdir(d) if x.endswith('.cnf') and x.startswith('c')):
            n = f[:-4]
            if (enc, n) in done: continue
            cnf, lrat = d + '/' + f, d + '/' + n + '.lrat'
            t0 = time.time()
            with open(d + '/' + n + '.cadical.out', 'w') as o:
                rc = subprocess.call([CAD, '-q', '--lrat', '--binary=false', cnf, lrat], stdout=o, stderr=subprocess.STDOUT)
            dt = time.time() - t0
            row = [enc, n, sha(cnf), str(rc), '%.1f' % dt]
            if rc != 20 or not os.path.exists(lrat):
                row += ['', '', '', 'NOT-UNSAT', '', '', time.strftime('%F %T')]
                open(TSV, 'a').write('\t'.join(row) + '\n'); log('%s %s cadical rc %d -- NOT UNSAT' % (enc, n, rc)); continue
            ph, pb = sha(lrat), os.path.getsize(lrat)
            r = subprocess.run([CAKE, '--CML_HEAP_SIZE=8000', '--CML_STACK_SIZE=4000', cnf, lrat], capture_output=True, text=True)
            open(d + '/' + n + '.cake.log', 'w').write(r.stdout + r.stderr)
            line = next((l for l in (r.stdout + r.stderr).splitlines() if l.startswith('s ')), '')
            verdict = 'ACCEPTED' if line.strip() == 's VERIFIED UNSAT' else 'REJECTED'
            zh = ''
            if verdict == 'ACCEPTED':
                subprocess.run(['zstd', '-q', '-3', '-T1', '--rm', '-f', lrat, '-o', lrat + '.zst'])
                zh = sha(lrat + '.zst') if os.path.exists(lrat + '.zst') else ''
            row += [ph, str(pb), 'yes' if arch.get(n) == ph else 'no', verdict, line.strip(), zh, time.strftime('%F %T')]
            open(TSV, 'a').write('\t'.join(row) + '\n')
            log('%s %s UNSAT %.0fs proof %s %s' % (enc, n, dt, ph[:12], verdict))
    rows = [l.split('\t') for l in open(TSV)][1:]
    acc = sum(1 for f in rows if len(f) > 8 and f[8] == 'ACCEPTED')
    log('replay finished: %d of 64 cube proofs ACCEPTED by cake_lpr (hash-bound)' % acc)
    open(W + '/SUMMARY.txt', 'w').write('%s: %d of 64 cube proofs accepted by cake_lpr, hash-bound (results.tsv)\n' % (time.strftime('%F %T'), acc))

if __name__ == '__main__':
    main()
