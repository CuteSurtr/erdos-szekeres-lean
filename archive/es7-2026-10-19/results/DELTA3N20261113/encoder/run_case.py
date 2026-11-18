#!/usr/bin/env python3
"""One sequential, bounded case. Parent schedules it; never starts a unit.
Keeps all artifacts and hashes. No certification inferred from an exit code.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PYTHON = '/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python'
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/encoder')


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--mode', choices=['cup', 'weak', 'cap'], default='cup')
    ap.add_argument('--pool', choices=['lattice', 'flat'], default='lattice')
    ap.add_argument('--sym', choices=['none', 'mirror'], default='none')
    ap.add_argument('--cube', default='')
    ap.add_argument('--fix-signs', type=Path)
    ap.add_argument('--as-mib', type=int, default=900)
    ap.add_argument('--cake-heap', type=int, default=650)
    ap.add_argument('--cake-stack', type=int, default=32)
    ap.add_argument('--seconds', type=int, default=600)
    ap.add_argument('--cake-seconds', type=int, default=300)
    ap.add_argument('--defer-cake', action='store_true')
    ap.add_argument('--generate-only', action='store_true')
    ap.add_argument('--binary', type=Path, default=SCRATCH / 'delta_cnf')
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    target = args.out.resolve()
    if not target.is_relative_to(SCRATCH) and not target.is_relative_to(HERE):
        raise ValueError('output must be under assigned encoder/ directories')
    target.mkdir(parents=True, exist_ok=False)  # Never overwrite prior proofs.
    resource.setrlimit(resource.RLIMIT_AS, (args.as_mib << 20, args.as_mib << 20))
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
                      PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(SCRATCH))
    result = {'label': 'COMPUTED', 'status': 'STARTED', 'parameters': vars(args).copy(),
              'commands': [], 'hashes': {}, 'runs': {}}
    result['parameters'] = {k: str(v) if isinstance(v, Path) else v for k,v in result['parameters'].items()}

    def save():
        (target / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')

    def run(tag, command, seconds):
        result['commands'].append(command)
        save()
        before = time.monotonic()
        try:
            with (target / (tag+'.log')).open('w') as log:
                p = subprocess.run(['/usr/bin/time', '-v', '-o', str(target/(tag+'.time'))] + command,
                                   stdout=log, stderr=subprocess.STDOUT, timeout=seconds)
            rc = p.returncode
        except subprocess.TimeoutExpired:
            # The outer timeout command terminates its entire child process group first.
            rc = 'DRIVER_TIMEOUT'
        result['runs'][tag] = {'exit': rc, 'wall_seconds': round(time.monotonic()-before,3)}
        save()
        return (target/(tag+'.log')).read_text(errors='replace')

    def bounded(command, seconds):
        return ['/usr/bin/timeout', '--kill-after=2', str(seconds)] + command

    cnf, proof = target/'case.cnf', target/'case.lrat'
    enc = [str(args.binary), '--n', str(args.n), '--m', str(args.m), '--mode', args.mode,
           '--pool', args.pool, '--sym', args.sym, '--out', str(cnf)]
    if args.cube:
        enc += ['--cube', args.cube]
    if args.fix_signs:
        enc += ['--fix-signs', str(args.fix_signs)]
    generated = run('encode', bounded(enc, 18), 22)
    if result['runs']['encode']['exit'] != 0:
        result['status'] = 'ENCODER_FAILED'; save(); return
    result['encoding'] = json.loads(generated)
    result['hashes']['case.cnf'] = digest(cnf)
    result['hashes']['delta_cnf.cpp'] = digest(HERE/'delta_cnf.cpp')
    result['hashes']['encoder_binary'] = digest(args.binary)
    save()
    if args.generate_only:
        result['status'] = 'GENERATED'; save(); return
    solver = ['/usr/bin/cadical', '-q', '-t', str(args.seconds), '--lrat=true', '--binary=false', str(cnf), str(proof)]
    log = run('cadical', bounded(solver, args.seconds+2), args.seconds+6)
    lines = log.splitlines()
    if proof.exists():
        result['hashes']['case.lrat'] = digest(proof)
        result['proof_bytes'] = proof.stat().st_size
    if 's SATISFIABLE' in lines and 's UNSATISFIABLE' not in lines:
        check = [PYTHON, '-B', str(HERE/'check_model.py'), '--m', str(args.m), '--n', str(args.n),
                 '--mode', args.mode, '--model', str(target/'cadical.log')]
        checked = run('model', bounded(check, 18), 22)
        result['status'] = 'SAT_RECHECK_FAILED'
        if result['runs']['model']['exit'] == 0:
            result['model'] = json.loads(checked)
            result['status'] = 'SAT_CHECKED'
    elif 's UNSATISFIABLE' in lines and 's SATISFIABLE' not in lines:
        result['status'] = 'UNSAT_UNCERTIFIED'
        if not args.defer_cake:
            cake = [str(Path.home()/'.local/bin/cake_lpr'), '--CML_HEAP_SIZE='+str(args.cake_heap),
                    '--CML_STACK_SIZE='+str(args.cake_stack), str(cnf), str(proof)]
            checked = run('cake', bounded(cake, args.cake_seconds), args.cake_seconds+4)
            if 's VERIFIED UNSAT' in checked.splitlines():
                result['status'] = 'UNSAT_CERTIFIED'; result['label'] = 'CERTIFIED'
    else:
        result['status'] = 'UNKNOWN'
    for p in sorted(target.iterdir()):
        if p.name != 'result.json' and p.is_file():
            result['hashes'][p.name] = digest(p)
    save()
    print(json.dumps({'out': str(target), 'label': result['label'], 'status': result['status']}))


if __name__ == '__main__':
    main()
