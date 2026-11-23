#!/usr/bin/env python3
"""Verify-only re-check of kept LRAT proofs (24 Nov 2026; owner: "verify every one of these ... then delete").
Own code: it imports no campaign tool. For each job of a JSONL job file:
  1. build the CNF (a kept file, or BASE + cube units as the campaign's solve.sh did) while hashing it, and require the
     recorded CNF SHA-256;
  2. decompress the kept proof (zstd, or plain) while hashing it, and require the recorded LRAT SHA-256;
  3. run a FRESH cake_lpr on exactly those bytes; accept only the exact line "s VERIFIED UNSAT" with exit 0;
  4. append one fsync'd ledger line (OK or ALERT) with hashes, line, exit code, heap, seconds, peak RSS and the
     SHA-256 of this tool and of cake_lpr.
It never deletes anything. Usage:
  python3 -I recheck_set.py JOBS.jsonl LEDGER.jsonl [--jobs N] [--tmp DIR] [--limit N]
Job fields: id, set, cnf {"file": PATH} | {"base": PATH, "units": PATH}, cnf_sha256, lrat (PATH, .zst or plain),
lrat_sha256, heap (MB), heap_retry (MB, optional: one retry on heap exhaustion), orig (path of the campaign's cake output, for the receipts; optional).
"""
import hashlib, json, os, resource, subprocess, sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed

CAKE = os.path.expanduser('~/.local/bin/cake_lpr')


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


TOOL_SHA, CAKE_SHA = sha_file(os.path.abspath(__file__)), sha_file(CAKE)


def build_cnf(spec, out):
    """Write the CNF to out, return its SHA-256 (as hashed while writing)."""
    h = hashlib.sha256()
    with open(out, 'wb') as w:
        def put(b):
            h.update(b); w.write(b)
        if 'file' in spec:
            with open(spec['file'], 'rb') as f:
                for b in iter(lambda: f.read(1 << 20), b''): put(b)
        else:   # BASE + units, as satopen k9 tools/solve.sh: "p cnf nv (ncl+nu)", the base without its header, the units
            units = open(spec['units'], 'rb').read()
            nu = units.count(b'\n')
            with open(spec['base'], 'rb') as f:
                head = f.readline().split()
                assert head[:2] == [b'p', b'cnf'], head
                put(b'p cnf %d %d\n' % (int(head[2]), int(head[3]) + nu))
                for b in iter(lambda: f.read(1 << 20), b''): put(b)
            put(units)
    return h.hexdigest()


def unpack(lrat, out):
    h = hashlib.sha256()
    if lrat.endswith('.zst'):
        p = subprocess.Popen(['zstd', '-dcq', lrat], stdout=subprocess.PIPE)
        src = p.stdout
    else:
        p, src = None, open(lrat, 'rb')
    with open(out, 'wb') as w:
        for b in iter(lambda: src.read(1 << 20), b''):
            h.update(b); w.write(b)
    if p is not None and p.wait() != 0: raise RuntimeError('zstd failed on %s' % lrat)
    if p is None: src.close()
    return h.hexdigest()


def run(job, tmp):
    rec = dict(id=job['id'], set=job['set'], lrat=job['lrat'], cnf_sha256=job['cnf_sha256'], lrat_sha256=job['lrat_sha256'],
               heap=job['heap'], orig=job.get('orig'), tool_sha256=TOOL_SHA, cake_sha256=CAKE_SHA)
    c, l = os.path.join(tmp, job['id'].replace('/', '_') + '.cnf'), os.path.join(tmp, job['id'].replace('/', '_') + '.lrat')
    t0 = time.time()
    try:
        got = build_cnf(job['cnf'], c)
        if got != job['cnf_sha256']:
            return dict(rec, status='ALERT', why='cnf sha256 %s != recorded' % got)
        got = unpack(job['lrat'], l)
        if got != job['lrat_sha256']:
            return dict(rec, status='ALERT', why='lrat sha256 %s != recorded' % got)
        def cake(heap):
            return subprocess.run(['/usr/bin/time', '-f', '%M', CAKE, '--CML_HEAP_SIZE=%d' % heap, '--CML_STACK_SIZE=1000', c, l],
                                  capture_output=True, text=True)
        r = cake(job['heap'])
        if 'heap space exhausted' in (r.stdout + r.stderr) and job.get('heap_retry'):
            rec['heap_first_exhausted'] = job['heap']; rec['heap'] = job['heap_retry']; r = cake(job['heap_retry'])
        lines = [x.strip() for x in r.stdout.splitlines() if x.startswith('s ')]
        rss = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ''
        rec.update(cake_rc=r.returncode, cake_lines=lines, cake_maxrss_kb=rss, seconds=round(time.time() - t0, 1),
                   heap_exhausted='heap space exhausted' in (r.stdout + r.stderr))
        ok = r.returncode == 0 and lines == ['s VERIFIED UNSAT']
        return dict(rec, status='OK' if ok else 'ALERT', why='' if ok else 'cake_lpr did not print exactly the line')
    except Exception as e:
        return dict(rec, status='ALERT', why='exception: %r' % e)
    finally:
        for p in (c, l):
            if os.path.exists(p): os.remove(p)


def main():
    jobs_f, led = sys.argv[1], sys.argv[2]
    n = int(sys.argv[sys.argv.index('--jobs') + 1]) if '--jobs' in sys.argv else 1
    tmp = sys.argv[sys.argv.index('--tmp') + 1] if '--tmp' in sys.argv else os.path.join(os.path.dirname(os.path.abspath(led)), 'tmp')
    lim = int(sys.argv[sys.argv.index('--limit') + 1]) if '--limit' in sys.argv else None
    os.makedirs(tmp, exist_ok=True)
    done = set()
    if os.path.exists(led):
        for line in open(led):
            try:
                e = json.loads(line)
                if e.get('status') == 'OK': done.add(e['id'])
            except ValueError: pass
    jobs = [j for j in map(json.loads, open(jobs_f)) if j['id'] not in done][:lim]
    print('%d jobs to run (%d already OK), %d parallel' % (len(jobs), len(done), n), flush=True)
    with ProcessPoolExecutor(n) as ex:
        futs = [ex.submit(run, j, tmp) for j in jobs]
        for f in as_completed(futs):
            rec = f.result(); rec['t'] = time.strftime('%F %T')
            with open(led, 'a') as w:
                w.write(json.dumps(rec) + '\n'); w.flush(); os.fsync(w.fileno())
            print(rec['status'], rec['id'], rec.get('seconds'), rec.get('why', ''), flush=True)


if __name__ == '__main__':
    main()
