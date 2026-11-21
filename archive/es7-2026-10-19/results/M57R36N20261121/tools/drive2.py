#!/usr/bin/env python3
"""drive2.py -- second-stage cube driver for rung N = 36 (owner model (3,5,7,36), --nosig), 21 Nov 2026.

Takes over the queued jobs of drive.py (cubes/, case A) and drive_b.py (cubes_b/, case B) without
stopping them: those drivers keep only their running jobs (cubes/LANES = 0 and NOSTART files; drive_b.py
passed its own start cutoff).  Jobs arrive through cubes2/inbox.json (written by handoff.py); a job id is
ingested once.  Same cube semantics as drive.py: base CNF + unit clauses on occ[s] = var 32759 + s; a cube
that times out is replaced by its two children on the next state of its case's split order.
Changes from drive.py (from the 21 Nov audit):
  - every job mutation and every save happens under one lock (no dict-size race in json.dump);
  - only exit 0 with a 'c UNKNOWN' line counts as a time-out (split); other exit codes -> 'error', no split;
  - a failed cake_lpr output is kept as <id>.cake.<k>; heap max(6000, 2000 + 0.8 * LRAT MB);
  - cases listed in cubes2/SKIP_CASES are not started (for example B once its monolithic run is certified);
  - start cutoff from the file cubes2/STOP_AT (epoch seconds) or env STOP_START; lanes from cubes2/LANES,
    capped so that all CaDiCaL processes on the machine stay at or below CAP (cubes2/CAP, default 13).
"""
import os, json, time, subprocess, hashlib, threading, copy

D = os.path.dirname(os.path.abspath(__file__))
CAD, CAKE = D + '/bin/cadical', D + '/bin/cake_lpr'
CU = D + '/cubes2'
STATE, RES = CU + '/state.json', CU + '/results.tsv'
OCC0 = 32759
BASE = {'A': D + '/run/c36_rle13.cnf', 'B': D + '/run/c36_tle22.cnf'}
ORDER = {'A': [44, 39, 26, 21, 15, 33, 27, 37, 32, 48, 38, 43, 46, 42, 47, 51, 50, 52, 53, 54, 55],
         'B': [34, 31, 16, 28, 22, 36, 29, 25, 23, 40, 49, 45, 41, 35, 30, 24, 20, 19, 18, 17]}
TL = int(os.environ.get('TL', '1500'))
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


def readint(path, default):
    try:
        return int(float(open(path).read().strip()))
    except (FileNotFoundError, ValueError):
        return default


def mem_used():
    out = subprocess.run(['vm_stat'], capture_output=True, text=True).stdout
    v = {}
    for line in out.splitlines():
        if ':' in line:
            k, x = line.split(':', 1)
            try:
                v[k.strip()] = int(x.strip().rstrip('.'))
            except ValueError:
                pass
    return 16384 * (v.get('Pages active', 0) + v.get('Pages wired down', 0) + v.get('Pages occupied by compressor', 0))


def cadical_count():
    out = subprocess.run(['ps', '-Ao', 'command', '-ww'], capture_output=True, text=True).stdout
    return sum(1 for l in out.splitlines() if '/bin/cadical' in l and 'awk' not in l)


def cid(case, units):
    return case + '_' + ''.join(('o' if u > 0 else 'h') + str(abs(u) - OCC0) for u in units)


def save(st):
    with lock:
        s = json.dumps(st, indent=0)
    tmp = STATE + '.tmp'
    open(tmp, 'w').write(s)
    os.replace(tmp, STATE)


def write_cube(job):
    base = BASE[job['case']]
    out = CU + '/' + job['id'] + '.cnf'
    with open(base) as f, open(out, 'w') as g:
        for line in f:
            if line.startswith('p cnf'):
                _, _, nv, nc = line.split()
                g.write('p cnf %s %d\n' % (nv, int(nc) + len(job['units'])))
                break
            g.write(line)
        while True:
            b = f.read(1 << 22)
            if not b:
                break
            g.write(b)
        for u in job['units']:
            g.write('%d 0\n' % u)
    return out


def result_row(job):
    keys = ['id', 'case', 'units', 'status', 'wall', 'conflicts', 'cnf_sha', 'lrat_bytes', 'lrat_sha', 'cake', 'cake_wall', 'heap']
    with lock:
        row = '\t'.join(' '.join(map(str, job['units'])) if k == 'units' else str(job.get(k, '')) for k in keys)
    with open(RES, 'a') as f:
        f.write(row + '\n')


def ingest(st):
    p = CU + '/inbox.json'
    if not os.path.exists(p):
        return
    try:
        new = json.load(open(p))
    except ValueError:
        return
    with lock:
        have = {j['id'] for j in st['jobs']}
        n = 0
        for j in new:
            if j['id'] in have:
                continue
            st['jobs'].append({'id': j['id'], 'case': j['case'], 'units': list(j['units']), 'status': 'queued',
                               'depth': j.get('depth', len(j['units'])), 'from': j.get('from', '')})
            have.add(j['id'])
            n += 1
    os.replace(p, CU + '/inbox.%d.done' % int(time.time()))
    save(st)
    log('ingested', n, 'jobs')


def verifier(st):
    while True:
        with lock:
            todo = [j for j in st['jobs'] if j['status'] == 'unsat']
            job = todo[0] if todo else None
            if job:
                job['status'] = 'verifying'
        if job is None:
            time.sleep(5)
            continue
        save(st)
        cnf, lrat = CU + '/' + job['id'] + '.cnf', CU + '/' + job['id'] + '.lrat'
        nb = os.path.getsize(lrat)
        heap = int(min(12000, max(6000, 2000 + 0.8 * nb / 1e6)))
        lsha, csha = sha(lrat), sha(cnf)
        cake = CU + '/' + job['id'] + '.cake'
        k = 1
        while os.path.exists(cake):
            os.replace(cake, cake + '.%d' % k) if not os.path.exists(cake + '.%d' % k) else None
            k += 1
        t = time.time()
        p = subprocess.run(['nice', '-n', '10', CAKE, '--CML_HEAP_SIZE=%d' % heap, '--CML_STACK_SIZE=200', cnf, lrat],
                           capture_output=True, text=True)
        open(cake, 'w').write(p.stdout + p.stderr)
        ok = any(l.strip() == 's VERIFIED UNSAT' for l in p.stdout.splitlines())
        with lock:
            job.update({'lrat_bytes': nb, 'lrat_sha': lsha, 'cnf_sha': csha, 'heap': heap,
                        'cake_wall': round(time.time() - t, 1), 'cake': 'VERIFIED' if ok else 'REJECTED rc=%d' % p.returncode,
                        'status': 'verified' if ok else 'cake_failed'})
        save(st)
        result_row(job)
        log('cake', job['id'], job['cake'], job['cake_wall'], 's heap', heap)
        if ok:
            z = lrat + '.zst'
            subprocess.run(['nice', '-n', '10', 'zstd', '-q', '-T2', '-3', '-f', lrat, '-o', z])
            d = subprocess.run('zstd -dc "%s" | shasum -a 256' % z, shell=True, capture_output=True, text=True).stdout.split()[0]
            if d == lsha:
                os.remove(lrat)
                os.remove(cnf)
                log('archived', job['id'], 'zst ok')
            else:
                log('ZSTD MISMATCH', job['id'])


def main():
    os.makedirs(CU, exist_ok=True)
    st = json.load(open(STATE)) if os.path.exists(STATE) else {'jobs': []}
    for j in st['jobs']:
        if j['status'] == 'running':
            j['status'] = 'queued'
        elif j['status'] == 'verifying':
            j['status'] = 'unsat'
    save(st)
    threading.Thread(target=verifier, args=(st,), daemon=True).start()
    running = {}
    while True:
        if os.path.exists(CU + '/STOP'):
            for p, j in running.values():
                p.terminate()
            log('STOP file: terminated', len(running))
            break
        ingest(st)
        for jid in list(running):
            p, job = running[jid]
            rc = p.poll()
            if rc is None:
                continue
            del running[jid]
            txt = open(CU + '/' + jid + '.log').read()
            conf = [l.split()[2] for l in txt.splitlines() if l.startswith('c conflicts:')]
            unknown = any(l.strip() in ('c UNKNOWN', 's UNKNOWN') for l in txt.splitlines())
            with lock:
                job['conflicts'] = conf[-1] if conf else ''
                job['wall'] = round(time.time() - job['t0'], 1)
                job['rc'] = rc
                if rc == 20:
                    job['status'] = 'unsat'
                elif rc == 10:
                    job['status'] = 'SAT'
                elif rc == 0 and unknown:
                    job['status'] = 'timeout'
                else:
                    job['status'] = 'error'
                if job['status'] in ('timeout', 'error'):
                    for ext in ('.lrat', '.cnf'):
                        try:
                            os.remove(CU + '/' + jid + ext)
                        except FileNotFoundError:
                            pass
                if job['status'] == 'timeout':
                    used = {abs(u) for u in job['units']}
                    nxt = [s for s in ORDER[job['case']] if OCC0 + s not in used]
                    if nxt:
                        s = nxt[0]
                        kids = [{'id': cid(job['case'], job['units'] + [sg * (OCC0 + s)]), 'case': job['case'],
                                 'units': job['units'] + [sg * (OCC0 + s)], 'status': 'queued',
                                 'depth': job['depth'] + 1, 'parent': jid} for sg in (1, -1)]
                        idx = st['jobs'].index(job)
                        st['jobs'][idx + 1:idx + 1] = kids
                        job['status'] = 'split'
            save(st)
            if job['status'] != 'unsat':
                result_row(job)
            log('done', jid, job['status'], job['wall'], 's', job['conflicts'], 'rc', rc)
        try:
            skip = set(open(CU + '/SKIP_CASES').read().split())
        except FileNotFoundError:
            skip = set()
        with lock:
            q = [j for j in st['jobs'] if j['status'] == 'queued' and j['case'] not in skip]
        lanes = readint(CU + '/LANES', 13)
        cap = readint(CU + '/CAP', 13)
        stop_at = readint(CU + '/STOP_AT', int(os.environ.get('STOP_START', '0') or 0))
        nostart = os.path.exists(CU + '/NOSTART') or (stop_at and time.time() >= stop_at)
        if q and not nostart and len(running) < lanes and cadical_count() < cap and mem_used() < MEM_LIMIT:
            job = q[0]
            cnf = write_cube(job)
            with lock:
                job['t0'] = time.time()
                job['status'] = 'running'
            p = subprocess.Popen(['nice', '-n', '10', CAD, '-t', str(TL), '--lrat', '--binary=false', cnf,
                                  CU + '/' + job['id'] + '.lrat'], stdout=open(CU + '/' + job['id'] + '.log', 'w'),
                                 stderr=subprocess.STDOUT)
            running[job['id']] = (p, job)
            save(st)
            log('start', job['id'], 'lanes', len(running))
            continue
        time.sleep(3)


if __name__ == '__main__':
    main()
