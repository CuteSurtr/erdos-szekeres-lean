#!/usr/bin/env python3
"""Parallel continuation of replay.py (same checks, same results.tsv): LANES CaDiCaL lanes, at most CAKE concurrent
cake_lpr runs (memory), hardest cubes first (by recorded proof size). Skips every (enc, cube) already ACCEPTED.
Only cake_lpr's line 's VERIFIED UNSAT' counts. Accepted proofs are kept as .lrat.zst. When all cubes are done it
restores the budget-64 campaign to its full 28 workers (only if its cap is still the value set at launch)."""
import os, sys, time, threading, subprocess
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import replay as R

LANES = int(os.environ.get('LANES', '6')); CAKE = int(os.environ.get('CAKE', '2'))
CAMP_CAP = '/home/jay/research/data/es8-b64-pilot-20261105/campaign/max_running'
lock = threading.Lock(); cake_sem = threading.Semaphore(CAKE)

def log(m):
    with lock: R.log(m)

def sizes():
    """(enc, cube) -> recorded raw proof bytes, for hardest-first ordering"""
    out, sec = {}, None
    for l in open(R.T + '/SHA256SUMS.txt'):
        if l.startswith('#'):
            sec = 'A' if l.startswith('# LRAT proofs') else 'B' if l.startswith('# encoder-B LRAT') else None; continue
        f = l.split()
        if sec and len(f) >= 4 and f[3].isdigit(): out[(sec, f[0].replace('B/', ''))] = int(f[3])
    return out

def one(enc, n, arch):
    d = os.path.join(R.W, enc, 'cubes'); cnf, lrat = d + '/' + n + '.cnf', d + '/' + n + '.lrat'
    t0 = time.time()
    with open(d + '/' + n + '.cadical.out', 'w') as o:
        rc = subprocess.call([R.CAD, '-q', '--lrat', '--binary=false', cnf, lrat], stdout=o, stderr=subprocess.STDOUT)
    dt = time.time() - t0
    row = [enc, n, R.sha(cnf), str(rc), '%.1f' % dt]
    if rc != 20 or not os.path.exists(lrat):
        row += ['', '', '', 'NOT-UNSAT', '', '', time.strftime('%F %T')]
        with lock: open(R.TSV, 'a').write('\t'.join(row) + '\n')
        log('%s %s cadical rc %d -- NOT UNSAT' % (enc, n, rc)); return
    ph, pb = R.sha(lrat), os.path.getsize(lrat)
    with cake_sem:
        r = subprocess.run([R.CAKE, '--CML_HEAP_SIZE=8000', '--CML_STACK_SIZE=4000', cnf, lrat], capture_output=True, text=True)
    open(d + '/' + n + '.cake.log', 'w').write(r.stdout + r.stderr)
    line = next((l for l in (r.stdout + r.stderr).splitlines() if l.startswith('s ')), '')
    verdict = 'ACCEPTED' if line.strip() == 's VERIFIED UNSAT' else 'REJECTED'
    zh = ''
    if verdict == 'ACCEPTED':
        subprocess.run(['zstd', '-q', '-3', '-T1', '--rm', '-f', lrat, '-o', lrat + '.zst'])
        zh = R.sha(lrat + '.zst') if os.path.exists(lrat + '.zst') else ''
    row += [ph, str(pb), 'yes' if arch.get(n) == ph else 'no', verdict, line.strip(), zh, time.strftime('%F %T')]
    with lock: open(R.TSV, 'a').write('\t'.join(row) + '\n')
    log('%s %s UNSAT %.0fs proof %s %s' % (enc, n, dt, ph[:12], verdict))

def main():
    rec, prA, prB = R.recorded()
    log('parallel replay start pid %d, lanes %d, cake %d' % (os.getpid(), LANES, CAKE))
    done = R.done_rows(); sz = sizes(); jobs = []
    for enc, arch in (('A', prA), ('B', prB)):
        if not R.prepare(enc, rec): continue
        d = os.path.join(R.W, enc, 'cubes')
        for f in os.listdir(d):
            if f.endswith('.cnf') and f.startswith('c') and (enc, f[:-4]) not in done:
                jobs.append((sz.get((enc, f[:-4]), 0), enc, f[:-4], arch))
    jobs.sort(key=lambda j: -j[0])
    log('%d cubes to do' % len(jobs))
    with ThreadPoolExecutor(LANES) as ex:
        for fut in [ex.submit(one, e, n, a) for _, e, n, a in jobs]: fut.result()
    rows = [l.rstrip('\n').split('\t') for l in open(R.TSV)][1:]
    acc = {(f[0], f[1]) for f in rows if len(f) > 8 and f[8] == 'ACCEPTED'}
    log('replay finished: %d of 64 cube proofs ACCEPTED by cake_lpr (hash-bound)' % len(acc))
    open(R.W + '/SUMMARY.txt', 'w').write('%s: %d of 64 cube proofs accepted by cake_lpr, hash-bound (results.tsv)\n' % (time.strftime('%F %T'), len(acc)))
    try:
        if open(CAMP_CAP).read().split()[0] == os.environ.get('CAMP_FROM', '26'):
            open(CAMP_CAP, 'w').write('28\n'); log('campaign cap restored to 28')
    except Exception as e: log('campaign cap not changed: %s' % e)

if __name__ == '__main__':
    main()
