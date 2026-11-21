#!/usr/bin/env python3
"""drive.py -- cube-and-conquer driver for rung N = 35 of the owner model (3,5,7,35), --nosig.

Four cases (rows of F = S1<=25 S2<=25 B1<=16 B2<=16 ALL<=35; each case lowers two of them;
coverage: cover35.py, "COVER OK"):
  A = run/c35_rle12_qle12.cnf (B2<=12, B1<=12)   97a256f8...
  B = run/c35_rle12_ule22.cnf (B2<=12, S2<=22)   daa27510...
  C = run/c35_tle22_qle12.cnf (S1<=22, B1<=12)   908bbd94...
  D = run/c35_tle22_ule22.cnf (S1<=22, S2<=22)   e89efe20...
Run it in its own directory (bin/, run/, a fresh cubes/), never in the r36 directory: main() resumes
from an existing cubes/state.json.
A cube = base CNF + unit clauses on occupancy variables occ[s] (var 32759 + s).  The leaves of each
case always cover every sign pattern of the case's top split: a timed-out cube is replaced by its two
children (cube + occ[s], cube + -occ[s]) for the next state s of the case's split order.
Each UNSAT leaf: CaDiCaL 3.0.1 --lrat --binary=false, then cake_lpr (one at a time); VERIFIED only on
the exact line 's VERIFIED UNSAT'.  State in cubes/state.json, results in cubes/results.tsv.
"""
import os, sys, json, time, subprocess, hashlib, threading
D = os.path.dirname(os.path.abspath(__file__))
CAD, CAKE = D + '/bin/cadical', D + '/bin/cake_lpr'
CU = D + '/cubes'
STATE, RES = CU + '/state.json', CU + '/results.tsv'
OCC0 = 32759
BASE = {'A': D + '/run/c35_rle12_qle12.cnf', 'B': D + '/run/c35_rle12_ule22.cnf',
        'C': D + '/run/c35_tle22_qle12.cnf', 'D': D + '/run/c35_tle22_ule22.cnf'}
ORDER = {'A': [44, 31, 39, 26, 21, 33, 27, 15, 25, 37, 32, 48, 18, 38, 43, 20, 46, 42, 47, 51, 50, 52, 53, 54, 55],
         'B': [44, 34, 39, 26, 21, 33, 27, 15, 28, 22, 16, 36, 29, 37, 23, 32, 49, 40, 19, 45, 41, 48, 35, 30, 38,
               24, 43, 46, 42, 17, 47, 51, 50, 52, 53, 54, 55],
         'C': [44, 34, 31, 39, 21, 33, 27, 15, 28, 22, 16, 36, 29, 25, 23, 49, 40, 19, 45, 41, 18, 35, 30, 24, 20, 17],
         'D': [34, 31, 26, 28, 22, 16, 36, 29, 25, 37, 23, 32, 49, 40, 19, 45, 41, 48, 18, 35, 30, 38, 24, 43, 20,
               46, 42, 17, 51, 47, 50, 52, 53, 54, 55]}
TOP = {'A': 6, 'B': 6, 'C': 5, 'D': 5}
LANES = int(os.environ.get('LANES', '11'))
TL = int(os.environ.get('TL', '1500'))
STOP_START = float(os.environ.get('STOP_START', '0'))   # epoch after which no new solve starts
MEM_LIMIT = float(os.environ.get('MEM_GB', '40')) * 1e9
lock = threading.Lock()

def log(*a):
    with open(CU + '/driver.log', 'a') as f:
        print(time.strftime('%H:%M:%S'), *a, file=f, flush=True)

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()

def mem_used():
    out = subprocess.run(['vm_stat'], capture_output=True, text=True).stdout
    v = {}
    for line in out.splitlines():
        if ':' in line:
            k, x = line.split(':', 1)
            try: v[k.strip()] = int(x.strip().rstrip('.'))
            except ValueError: pass
    pg = 16384
    return pg * (v.get('Pages active', 0) + v.get('Pages wired down', 0) + v.get('Pages occupied by compressor', 0))

def cid(case, units):
    return case + '_' + ''.join(('o' if u > 0 else 'h') + str(abs(u) - OCC0) for u in units)

def new_state():
    jobs = []
    for case in sorted(BASE):
        k = TOP[case]
        for m in range(1 << k):
            units = [(OCC0 + s) if (m >> i) & 1 else -(OCC0 + s) for i, s in enumerate(ORDER[case][:k])]
            jobs.append({'id': cid(case, units), 'case': case, 'units': units, 'status': 'queued', 'depth': k})
    return {'jobs': jobs}

def save(st):
    tmp = STATE + '.tmp'
    json.dump(st, open(tmp, 'w'), indent=0)
    os.replace(tmp, STATE)

def write_cube(job):
    base = BASE[job['case']]; out = CU + '/' + job['id'] + '.cnf'
    with open(base) as f, open(out, 'w') as g:
        for line in f:
            if line.startswith('p cnf'):
                _, _, nv, nc = line.split()
                g.write('p cnf %s %d\n' % (nv, int(nc) + len(job['units'])))
                break
            g.write(line)
        while True:
            b = f.read(1 << 22)
            if not b: break
            g.write(b)
        for u in job['units']:
            g.write('%d 0\n' % u)
    return out

def result_row(job):
    keys = ['id', 'case', 'units', 'status', 'wall', 'conflicts', 'cnf_sha', 'lrat_bytes', 'lrat_sha', 'cake', 'cake_wall', 'heap']
    with open(RES, 'a') as f:
        f.write('\t'.join(str(job.get(k, '')) if k != 'units' else ' '.join(map(str, job['units'])) for k in keys) + '\n')

def verifier(st):
    while True:
        with lock:
            todo = [j for j in st['jobs'] if j['status'] == 'unsat']
            job = todo[0] if todo else None
            if job: job['status'] = 'verifying'; save(st)
        if job is None:
            if os.path.exists(CU + '/DONE'): return
            time.sleep(5); continue
        cnf = CU + '/' + job['id'] + '.cnf'; lrat = CU + '/' + job['id'] + '.lrat'
        nb = os.path.getsize(lrat)
        heap = int(min(12000, max(6000, 2000 + 0.8 * nb / 1e6)))
        job['lrat_bytes'] = nb; job['lrat_sha'] = sha(lrat); job['cnf_sha'] = sha(cnf); job['heap'] = heap
        t = time.time()
        p = subprocess.run(['nice', '-n', '5', CAKE, '--CML_HEAP_SIZE=%d' % heap, '--CML_STACK_SIZE=200', cnf, lrat],
                           capture_output=True, text=True)
        open(CU + '/' + job['id'] + '.cake', 'w').write(p.stdout + p.stderr)
        ok = any(l.strip() == 's VERIFIED UNSAT' for l in p.stdout.splitlines())
        job['cake_wall'] = round(time.time() - t, 1)
        job['cake'] = 'VERIFIED' if ok else 'REJECTED rc=%d' % p.returncode
        with lock:
            job['status'] = 'verified' if ok else 'cake_failed'
            save(st)
        result_row(job); log('cake', job['id'], job['cake'], job['cake_wall'], 's', 'heap', heap)
        if ok:
            # archive copy: zstd, round trip checked by hashing the decompressed stream
            z = lrat + '.zst'
            subprocess.run(['nice', '-n', '10', 'zstd', '-q', '-T2', '-3', '-f', lrat, '-o', z])
            d = subprocess.run('zstd -dc "%s" | shasum -a 256' % z, shell=True, capture_output=True, text=True).stdout.split()[0]
            if d == job['lrat_sha']:
                os.remove(lrat); os.remove(cnf)
                log('archived', job['id'], 'zst ok')
            else:
                log('ZSTD MISMATCH', job['id'])

def main():
    os.makedirs(CU, exist_ok=True)
    st = json.load(open(STATE)) if os.path.exists(STATE) else new_state()
    for j in st['jobs']:
        if j['status'] in ('running', 'verifying'): j['status'] = 'queued' if j['status'] == 'running' else 'unsat'
    save(st)
    threading.Thread(target=verifier, args=(st,), daemon=True).start()
    running = {}
    while True:
        if os.path.exists(CU + '/STOP'):
            for p, j in running.values(): p.terminate()
            log('STOP file: terminated', len(running)); break
        # reap
        for jid in list(running):
            p, job = running[jid]
            rc = p.poll()
            if rc is None: continue
            del running[jid]
            logf = CU + '/' + jid + '.log'
            txt = open(logf).read()
            conf = [l.split()[2] for l in txt.splitlines() if l.startswith('c conflicts:')]
            job['conflicts'] = conf[-1] if conf else ''
            job['wall'] = round(time.time() - job['t0'], 1)
            with lock:
                if rc == 20:
                    job['status'] = 'unsat'
                elif rc == 10:
                    job['status'] = 'SAT'; log('SAT !!!', jid)
                else:
                    job['status'] = 'timeout'
                    try: os.remove(CU + '/' + jid + '.lrat')
                    except FileNotFoundError: pass
                    nxt = [s for s in ORDER[job['case']] if OCC0 + s not in map(abs, job['units'])]
                    if nxt:
                        s = nxt[0]
                        kids = [{'id': cid(job['case'], job['units'] + [sg * (OCC0 + s)]), 'case': job['case'],
                                 'units': job['units'] + [sg * (OCC0 + s)], 'status': 'queued',
                                 'depth': job['depth'] + 1, 'parent': jid} for sg in (1, -1)]
                        idx = st['jobs'].index(job)
                        st['jobs'][idx + 1:idx + 1] = kids
                        job['status'] = 'split'
                        try: os.remove(CU + '/' + jid + '.cnf')
                        except FileNotFoundError: pass
                save(st)
            if job['status'] != 'unsat': result_row(job)
            log('done', jid, job['status'], job['wall'], 's', job['conflicts'])
        # start
        q = [j for j in st['jobs'] if j['status'] == 'queued']
        if not q and not running:
            if not any(j['status'] in ('unsat', 'verifying') for j in st['jobs']):
                open(CU + '/DONE', 'w').write('done\n'); log('all done'); break
        lanes = LANES
        if os.path.exists(CU + '/LANES'):
            try: lanes = int(open(CU + '/LANES').read().strip())
            except ValueError: pass
        nostart = os.path.exists(CU + '/NOSTART') or (STOP_START and time.time() >= STOP_START)
        if q and len(running) < lanes and not nostart and mem_used() < MEM_LIMIT:
            job = q[0]
            cnf = write_cube(job)
            job['t0'] = time.time(); job['status'] = 'running'
            p = subprocess.Popen(['nice', '-n', '5', CAD, '-t', str(TL), '--lrat', '--binary=false', cnf,
                                  CU + '/' + job['id'] + '.lrat'], stdout=open(CU + '/' + job['id'] + '.log', 'w'),
                                 stderr=subprocess.STDOUT)
            running[job['id']] = (p, job)
            with lock: save(st)
            log('start', job['id'], 'lanes', len(running))
            continue
        time.sleep(3)

if __name__ == '__main__':
    main()
