#!/usr/bin/env python3
"""V1-0: re-check leaves of hull_leaves.icnf (0-based line index i, i % MOD == RES)
with two LRAT checkers: cake_lpr (must print `s VERIFIED UNSAT`) and drat-trim
lrat-check with results/E2/tools/lrat-check-E2.patch (must print `c VERIFIED`).

cubeCnf is built as in results/H3/scripts/check_cubes.sh: header clause count + |c|,
the CNF body unchanged, then one unit clause per cube literal.

Usage: run_leaves.py CNF LEAVES OUT.jsonl [--mod 4] [--res 0] [--jobs 4]
Env: CADICAL, CAKE_LPR, LRAT_FIXED (binaries), TMPD (scratch dir).
Resumable: line indices already present in OUT.jsonl are skipped.
CNF and proof files are deleted after both checks; a SAT model is kept in OUT's dir.
"""
import json, os, resource, subprocess, sys, time, fcntl, argparse
from multiprocessing import Pool

ap = argparse.ArgumentParser()
ap.add_argument('cnf'); ap.add_argument('leaves'); ap.add_argument('out')
ap.add_argument('--mod', type=int, default=4); ap.add_argument('--res', type=int, default=0)
ap.add_argument('--jobs', type=int, default=4)
ap.add_argument('--only', type=str, default=None, help='comma-separated indices (re-solve)')
A = ap.parse_args()
CADICAL, CAKE, LRAT = os.environ['CADICAL'], os.environ['CAKE_LPR'], os.environ['LRAT_FIXED']
TMPD = os.environ.get('TMPD', '/tmp')
OUTDIR = os.path.dirname(os.path.abspath(A.out))

with open(A.cnf, 'rb') as f:
    hdr = f.readline().split()
    BODY_OFF = f.tell()
NV, NC = int(hdr[2]), int(hdr[3])


def cpu():
    r = resource.getrusage(resource.RUSAGE_CHILDREN)
    return r.ru_utime + r.ru_stime


def timed(cmd, **kw):
    c0, t0 = cpu(), time.time()
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw)
    return p, time.time() - t0, cpu() - c0


def work(item):
    i, lits = item
    f = os.path.join(TMPD, f'leaf{i}.cnf'); pf = os.path.join(TMPD, f'leaf{i}.lrat')
    with open(f, 'wb') as o, open(A.cnf, 'rb') as src:
        o.write(f'p cnf {NV} {NC + len(lits)}\n'.encode())
        src.seek(BODY_OFF)
        while True:
            b = src.read(1 << 20)
            if not b: break
            o.write(b)
        for l in lits: o.write(f'{l} 0\n'.encode())
    p, ts, cs = timed([CADICAL, '--elim=0', '--lrat', '--binary=false', f, pf])
    rec = {'i': i, 'cube': lits, 'solver_exit': p.returncode, 'solve_s': round(ts, 2),
           'solve_cpu_s': round(cs, 2)}
    if p.returncode == 20:
        rec['proof_bytes'] = os.path.getsize(pf)
        q, tc, cc = timed([CAKE, f, pf])
        out = q.stdout.decode(errors='replace').strip().splitlines()
        rec['cake_lpr'] = out[0] if out else ''
        rec['cake_exit'] = q.returncode; rec['cake_s'] = round(tc, 2); rec['cake_cpu_s'] = round(cc, 2)
        q, tl, cl = timed([LRAT, f, pf])
        out = q.stdout.decode(errors='replace').splitlines()
        v = [x for x in out if x.startswith('c VERIFIED') or x.startswith('c NOT VERIFIED')]
        rec['lrat_check'] = v[0] if v else 'no verdict'
        if not v or v[0] != 'c VERIFIED':
            rec['lrat_check_tail'] = [x for x in out if 'FAIL' in x or 'WARN' in x][:5]
        rec['lrat_exit'] = q.returncode; rec['lrat_s'] = round(tl, 2); rec['lrat_cpu_s'] = round(cl, 2)
    else:
        rec['proof_bytes'] = os.path.getsize(pf) if os.path.exists(pf) else 0
        rec['cake_lpr'] = rec['lrat_check'] = f'not run (solver exit {p.returncode})'
        if p.returncode == 10:
            with open(os.path.join(OUTDIR, f'SAT_leaf{i}.model'), 'wb') as m: m.write(p.stdout)
        else:
            rec['solver_tail'] = p.stdout.decode(errors='replace').splitlines()[-5:]
    rec['ok'] = rec['cake_lpr'] == 's VERIFIED UNSAT' and rec['lrat_check'] == 'c VERIFIED'
    for x in (f, pf):
        if os.path.exists(x): os.remove(x)
    with open(A.out, 'a') as o:
        fcntl.flock(o, fcntl.LOCK_EX); o.write(json.dumps(rec) + '\n'); o.flush()
    return rec


def main():
    done = set()
    if os.path.exists(A.out):
        for l in open(A.out):
            if l.strip(): done.add(json.loads(l)['i'])
    only = set(map(int, A.only.split(','))) if A.only else None
    items = []
    for i, line in enumerate(open(A.leaves)):
        if i % A.mod != A.res: continue
        if only is not None:
            if i not in only: continue
        elif i in done: continue
        t = line.split()
        if t and t[0] == 'a': t = t[1:]
        lits = []
        for x in t:
            if x == '0': break
            lits.append(int(x))
        items.append((i, lits))
    print(f'{len(items)} leaves to run, {len(done)} already done', flush=True)
    with Pool(A.jobs) as P:
        for r in P.imap_unordered(work, items):
            print(r['i'], r['solver_exit'], r['solve_s'], r['cake_lpr'], r['lrat_check'], flush=True)


main()
