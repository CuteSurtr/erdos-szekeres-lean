#!/usr/bin/env python3
"""Re-check leaves of verify/hull_leaves.icnf (0-based line index i, i % MOD == RES) with
CaDiCaL LRAT proofs checked by cake_lpr and by the E2-patched lrat-check.
cubeCnf as in results/H3/scripts/check_cubes.sh: header count + |c|, unit clauses appended.
Usage: run_leaves.py CNF ICNF OUT.jsonl  (env CADICAL CAKE_LPR LRAT_CHECK TMPD JOBS MOD RES SATDIR)
Resumable: line indices already in OUT are skipped. CNF/proof files are deleted."""
import json, os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
CNF, ICNF, OUT = sys.argv[1:4]
E = os.environ
CAD, CAKE, LC = E['CADICAL'], E['CAKE_LPR'], E['LRAT_CHECK']
TMPD = E.get('TMPD', '/tmp'); JOBS = int(E.get('JOBS', 4))
MOD, RES = int(E.get('MOD', 4)), int(E.get('RES', 1)); SATDIR = E['SATDIR']
with open(CNF) as f:
    hdr = f.readline().split(); body = f.read()
NV, NC = int(hdr[2]), int(hdr[3])
lock = threading.Lock()

def run(cmd, out=subprocess.DEVNULL):
    t0 = time.time(); p = subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT)
    _, st, ru = os.wait4(p.pid, 0); p.returncode = os.waitstatus_to_exitcode(st)
    return p.returncode, time.time() - t0, ru.ru_utime + ru.ru_stime

def attempt(i, lits):
    f, p, so = (f'{TMPD}/leaf{i}.{x}' for x in ('cnf', 'lrat', 'out'))
    with open(f, 'w') as fh:
        fh.write(f'p cnf {NV} {NC + len(lits)}\n'); fh.write(body)
        fh.writelines(f'{l} 0\n' for l in lits)
    with open(so, 'w') as oh:
        st, ws, cs = run([CAD, '-q', '--elim=0', '--lrat', '--binary=false', f, p], oh)
    r = dict(solver_exit=st, solve_s=round(ws, 2), solve_cpu_s=round(cs, 2), proof_bytes=0,
             cake_lpr='', lrat_check='', cake_s=0, lrat_s=0, check_cpu_s=0)
    if st == 10:
        os.makedirs(SATDIR, exist_ok=True); os.replace(so, f'{SATDIR}/leaf{i}.model')
    elif st == 20:
        r['proof_bytes'] = os.path.getsize(p)
        with open(so, 'w') as oh: _, a, ca = run([CAKE, f, p], oh)
        cake = open(so).read()
        with open(so, 'w') as oh: lcx, b, cb = run([LC, f, p], oh)
        lco = open(so).read()
        r.update(cake_s=round(a, 2), lrat_s=round(b, 2), check_cpu_s=round(ca + cb, 2),
                 cake_lpr='VERIFIED UNSAT' if re.search(r'^s VERIFIED UNSAT$', cake, re.M) else 'REJECT: ' + cake.strip()[-300:],
                 lrat_check='VERIFIED' if lcx == 0 and re.search(r'^c VERIFIED$', lco, re.M) else f'REJECT exit {lcx}: ' + lco.strip()[-300:])
    for x in (f, p, so):
        if os.path.exists(x): os.remove(x)
    return r

def leaf(i, lits):
    r = attempt(i, lits); tries = 1
    if r['solver_exit'] == 20 and not (r['cake_lpr'] == 'VERIFIED UNSAT' and r['lrat_check'] == 'VERIFIED'):
        first = r; r = attempt(i, lits); tries = 2; r['first_attempt'] = first
    rec = dict(line=i, cube=lits, attempts=tries, **r)
    with lock:
        with open(OUT, 'a') as oh: oh.write(json.dumps(rec) + '\n')
    print(json.dumps({k: rec[k] for k in ('line', 'solver_exit', 'solve_s', 'proof_bytes', 'cake_lpr', 'lrat_check')}), flush=True)

done = set()
if os.path.exists(OUT):
    done = {json.loads(l)['line'] for l in open(OUT) if l.strip()}
todo = []
for i, line in enumerate(open(ICNF)):
    if i % MOD != RES or i in done: continue
    t = line.split(); assert t[0] == 'a' and t[-1] == '0'
    todo.append((i, [int(x) for x in t[1:-1]]))
print(f'{len(todo)} leaves to do, {len(done)} done', flush=True)
with ThreadPoolExecutor(JOBS) as ex:
    for fu in [ex.submit(leaf, i, c) for i, c in todo]: fu.result()
