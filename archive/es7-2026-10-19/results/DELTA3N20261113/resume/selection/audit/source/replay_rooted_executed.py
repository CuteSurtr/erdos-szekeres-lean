#!/usr/bin/env python3
"""One independently bounded cake replay, using the explicitly granted AS800.

Never imports the AS400 control wrapper; this allocation is for cake only.
Each invocation must also be wrapped in an external 20-second timeout.
"""
import os
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
import resource
resource.setrlimit(resource.RLIMIT_AS, (800 << 20, 800 << 20))
resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

HERE = Path(__file__).resolve().parent
PARENT = Path('/home/jay/research/data/delta3-codex-20261113/selection/rooted')
CAKE = Path('/home/jay/.local/bin/cake_lpr')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('m', type=int)
    args = ap.parse_args()
    n, m = args.n, args.m
    require((n == 7 and 9 <= m <= 13) or (n == 8 and 10 <= m <= 14), 'not one of the ten accepted cases')
    case = PARENT / f'sweep{n}/m{m}'
    out = HERE / f'results/replays/n{n}m{m}'
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    parent = json.loads((case / 'solve/result.json').read_text())
    cnf, proof = case / 'rooted.cnf', case / 'solve/proof.lrat'
    result = dict(label='COMPUTED', status='RUNNING', n=n, m=m,
                  cnf=str(cnf), proof=str(proof), wrapper_sha256=sha(__file__),
                  limits=dict(as_mib=800, heap_mib=600, stack_mib=32,
                              cpu_seconds=18, checker_timeout_seconds=18,
                              external_seconds=20, affinity=list(os.sched_getaffinity(0))),
                  authorization='User reserved AS800 MiB for independent cake replay only.')
    record = out / 'result.json'
    def save():
        record.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    save()
    try:
        require(parent['status'] == 'UNSAT_CERTIFIED', 'parent not accepted')
        before = dict(cnf=sha(cnf), lrat=sha(proof), cake=sha(CAKE))
        require(before['cnf'] == parent['hashes']['input.cnf'], 'CNF hash mismatch')
        require(before['lrat'] == parent['hashes']['proof.lrat'], 'LRAT hash mismatch')
        require(before['cake'] == parent['hashes']['cake_lpr'], 'cake executable differs')
        verified_record = json.loads((HERE / f'results/sweep{n}.json').read_text())
        prior = next(c for c in verified_record['cases'] if c['m'] == m)
        require(prior['independently_reconstructed_child'] and
                before['cnf'] == prior['checked_hashes']['input.cnf'], 'CNF not independently reconstructed')
        command = [str(CAKE), '--CML_HEAP_SIZE=600', '--CML_STACK_SIZE=32', str(cnf), str(proof)]
        result.update(command=command, input_hashes=before)
        save()
        checker_start = time.monotonic()
        with (out / 'cake.stdout').open('wb') as stdout, (out / 'cake.stderr').open('wb') as stderr:
            try:
                p = subprocess.run(command, stdout=stdout, stderr=stderr, timeout=18)
                result['exit_code'] = p.returncode
            except subprocess.TimeoutExpired:
                result['status'] = 'TIMEOUT_NO_CERTIFICATE'
                result['exit_code'] = None
        result['checker_seconds'] = time.monotonic()-checker_start
        line_present = b's VERIFIED UNSAT' in (out / 'cake.stdout').read_bytes().splitlines()
        result['exact_success_line_present'] = line_present
        result['stdout_sha256'] = sha(out / 'cake.stdout')
        result['stderr_sha256'] = sha(out / 'cake.stderr')
        after = dict(cnf=sha(cnf), lrat=sha(proof), cake=sha(CAKE))
        require(after == before, 'input or checker changed during replay')
        result['hashes_stable_after_replay'] = True
        if result['status'] != 'TIMEOUT_NO_CERTIFICATE':
            if result['exit_code'] == 0 and line_present:
                result['status'] = 'INDEPENDENTLY_VERIFIED_UNSAT'
                result['label'] = 'CERTIFIED'
            else:
                result['status'] = 'REJECTED_OR_INCOMPLETE'
    except Exception as exc:
        result.update(status='AUDIT_ERROR', error=type(exc).__name__+': '+str(exc))
    result.update(elapsed_seconds=time.monotonic()-started,
                  child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  wrapper_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    save()
    print(json.dumps({k: result.get(k) for k in ('n', 'm', 'label', 'status',
                      'exact_success_line_present', 'checker_seconds', 'elapsed_seconds',
                      'child_peak_rss_kib')}, sort_keys=True))
    if result['status'] != 'INDEPENDENTLY_VERIFIED_UNSAT':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
