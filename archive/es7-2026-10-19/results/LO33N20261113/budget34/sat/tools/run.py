#!/usr/bin/env python3
"""One CPU; 80 MiB parent + 1000 MiB child, leaving 120 MiB for preparation."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

MIB = 1024*1024
resource.setrlimit(resource.RLIMIT_AS, (80*MIB, 1200*MIB))
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  PYTHONDONTWRITEBYTECODE='1')
os.sched_setaffinity(0, {11})
ap = argparse.ArgumentParser()
ap.add_argument('directory')
ap.add_argument('--seconds', type=int, default=1200)
ap.add_argument('--name', default='cadical-default')
ap.add_argument('--sat', action='store_true')
ap.add_argument('--binary-proof', action='store_true')
args = ap.parse_args()
folder = Path(args.directory).resolve()
job = folder/args.name
job.mkdir(exist_ok=False)
cnf = folder/'system.cnf'
proof = job/'system.lrat'
status = {'label': 'COMPUTED running', 'started': datetime.datetime.now().isoformat(),
          'parent_AS_MiB': 80, 'child_AS_MiB': 1000, 'preparation_AS_MiB': 120, 'CPU_affinity': [11],
          'cake_heap_MiB': 700, 'retain_raw_and_compressed': True, 'steps': []}
child = None


def record():
    (job/'status.json').write_text(json.dumps(status, indent=2)+'\n')


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(MIB), b''):
            h.update(block)
    return h.hexdigest()


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (1000*MIB, 1000*MIB))
    resource.setrlimit(resource.RLIMIT_FSIZE, (3*1024**3, 3*1024**3))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def run(command, logfile, seconds):
    global child
    t = time.monotonic()
    step = {'command': command, 'log': str(logfile), 'started': datetime.datetime.now().isoformat()}
    status['steps'].append(step)
    record()
    with open(logfile, 'w') as output:
        child = subprocess.Popen(command, stdout=output, stderr=subprocess.STDOUT, preexec_fn=limits)
        try:
            rc = child.wait(timeout=seconds)
        except subprocess.TimeoutExpired:
            child.terminate()
            try:
                rc = child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                child.kill()
                rc = child.wait()
            step['timed_out'] = True
    child = None
    step.update(returncode=rc, seconds=round(time.monotonic()-t, 3))
    record()
    return rc


def stopped(signum, frame):
    status['label'] = 'COMPUTED interrupted; no certificate accepted'
    status['signal'] = signum
    if child is not None:
        child.terminate()
    record()
    raise SystemExit(128+signum)


signal.signal(signal.SIGTERM, stopped)
signal.signal(signal.SIGINT, stopped)
record()
try:
    assert datetime.datetime.now().time() < datetime.time(10, 45), 'no new long run after 10:45 KST'
    assert 0 < args.seconds <= 1600
    command = ['/usr/bin/cadical', '--lrat=true', '--binary='+str(args.binary_proof).lower(), '-t', str(args.seconds),
               '-w', str(job/'solution.txt')]
    if args.sat:
        command.append('--sat')
    command += [str(cnf), str(proof)]
    rc = run(command, job/'cadical.log', args.seconds+20)
    status['cadical_returncode'] = rc
    status['cnf_sha256'] = digest(cnf)
    if rc == 10:
        status['label'] = 'COMPUTED SAT; independent witness check pending'
        meta = json.loads((folder/'encoding.json').read_text())
        command = [sys.executable, str(Path(__file__).with_name('check_independent.py')),
                   'model', '--base', meta['base'], '--pool', meta['pool'],
                   '--solution', str(job/'solution.txt'), '--cnf', str(cnf),
                   '--out', str(job/'witness.json')]
        if meta['slice']:
            command += ['--slice', str(meta['slice'])]
        result = run(command, job/'witness-check.log', 45)
        if result == 0:
            status['label'] = 'COMPUTED SAT; all rows and CNF clauses independently verified'
    elif rc == 20:
        status['label'] = 'COMPUTED UNSAT; not certified'
        if proof.stat().st_size <= 128*MIB and datetime.datetime.now().time() < datetime.time(10, 45):
            run(['/home/jay/.local/bin/cake_lpr', '--CML_HEAP_SIZE=700', '--CML_STACK_SIZE=64', str(cnf), str(proof)],
                job/'cake.out', 420)
            accepted = any(line.rstrip('\r\n') == 's VERIFIED UNSAT'
                           for line in (job/'cake.out').open())
            status['cake_exact_line_accepted'] = accepted
            if accepted:
                status['label'] = 'CERTIFIED finite-row CNF UNSAT'
        else:
            status['cake_pending_reason'] = 'proof exceeds 128 MiB or new long-run cutoff; parent coordination needed'
    else:
        status['label'] = 'COMPUTED UNKNOWN; no conclusion'
    if proof.exists():
        status['lrat_bytes'] = proof.stat().st_size
        status['lrat_sha256'] = digest(proof)
        run(['/usr/bin/zstd', '-q', '-1', '-T1', str(proof), '-o', str(proof)+'.zst'],
            job/'compress.log', 90)
        if Path(str(proof)+'.zst').exists():
            status['lrat_zst_sha256'] = digest(str(proof)+'.zst')
    status['finished'] = datetime.datetime.now().isoformat()
    status['children_peak_RSS_KiB'] = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    record()
except BaseException as exc:
    status['exception'] = repr(exc)
    record()
    raise
