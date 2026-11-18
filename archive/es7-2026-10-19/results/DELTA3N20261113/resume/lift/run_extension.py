#!/usr/bin/env python3
"""Bounded sequential extension search; parent alone schedules long runs.

Defaults fit a short probe. No units, installs, deletions or certification.
Every case has a fresh output directory; UNKNOWN traces and LRATs are kept.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/resume/lift')
SOURCE = HERE / '../../coordinator/data/cup15/realized.json'


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--n', type=int, required=True, choices=range(5,9))
    p.add_argument('--add', type=int, required=True, choices=range(6))
    p.add_argument('--mode', choices=['cup','weak'], default='cup')
    p.add_argument('--source', type=Path, default=SOURCE)
    p.add_argument('--binary', type=Path, default=SCRATCH/'extension_cnf')
    p.add_argument('--simplifier', type=Path, default=SCRATCH/'unit_simplify')
    p.add_argument('--simplify', action='store_true')
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--fixed-positions')
    p.add_argument('--pin-source', action='store_true', help='requires --add 0')
    p.add_argument('--base-only', action='store_true')
    p.add_argument('--embedding-only', action='store_true')
    p.add_argument('--generate-only', action='store_true')
    p.add_argument('--solve-seconds', type=int, default=5)
    p.add_argument('--wall-seconds', type=int, default=25)
    p.add_argument('--as-mib', type=int, default=360)
    args = p.parse_args()
    target = args.out.resolve()
    if not target.is_relative_to(SCRATCH):
        raise ValueError('experiment output must be below assigned scratch/lift')
    if args.base_only and args.embedding_only:
        raise ValueError('choose only one partial mode')
    if min(args.solve_seconds,args.wall_seconds,args.as_mib) <= 0:
        raise ValueError('budgets must be positive')
    target.mkdir(parents=True, exist_ok=False)
    resource.setrlimit(resource.RLIMIT_AS, (args.as_mib << 20, args.as_mib << 20))
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
                      PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(SCRATCH))
    # The exact source determinant audit is independent of the encoder.
    from audit_extension import load_source
    old_points, signs, margin = load_source(args.source)
    old_file = target/'old.signs'
    old_file.write_text(signs+'\n')
    result = {'label': 'COMPUTED', 'status': 'STARTED',
              'parameters': {k: str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},
              'source_minimum_abs_determinant': margin, 'runs': {}, 'hashes': {}}
    deadline = time.monotonic()+args.wall_seconds

    def save():
        (target/'result.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')

    def run(tag, command, cap):
        left = min(float(cap), deadline-time.monotonic())
        if left <= 0:
            result['runs'][tag] = {'command': command, 'exit': 'NO_TIME'}
            save()
            return False
        result['runs'][tag] = {'command': command, 'exit': 'RUNNING'}
        save()
        before = time.monotonic()
        with (target/(tag+'.log')).open('w') as log:
            proc = subprocess.Popen(['/usr/bin/time','-v','-o',str(target/(tag+'.time'))]+command,
                                    stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                rc = proc.wait(timeout=left)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
                rc = 'TIMEOUT'
        result['runs'][tag].update(exit=rc, wall_seconds=round(time.monotonic()-before,3))
        save()
        return rc == 0

    save()
    try:
        result['hashes'].update({
            'source': digest(args.source), 'binary': digest(args.binary),
            'extension_cnf.cpp': digest(HERE/'extension_cnf.cpp'),
            'universal_delta_cnf.cpp': digest(HERE/'../../encoder/delta_cnf.cpp'),
            'audit_extension.py': digest(HERE/'audit_extension.py')})
        command = [str(args.binary), '--n',str(args.n),'--add',str(args.add),
                   '--old-size',str(len(old_points)), '--mode',args.mode,
                   '--old-signs',str(old_file),'--out',str(target/'case.cnf')]
        if args.fixed_positions:
            command += ['--fixed-positions',args.fixed_positions]
        if args.base_only:
            command += ['--base-only']
        if args.embedding_only:
            command += ['--embedding-only']
        if args.pin_source:
            if args.add != 0:
                raise ValueError('--pin-source requires add=0')
            command += ['--pin-signs',str(old_file)]
        if not run('encode',command,args.wall_seconds):
            result['status'] = 'ENCODER_INCOMPLETE'
            return
        meta = json.loads((target/'encode.log').read_text())
        result['encoding'] = meta
        (target/'meta.json').write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n')
        result['hashes']['case.cnf'] = digest(target/'case.cnf')
        solve_cnf = target/'case.cnf'
        if args.simplify:
            result['hashes']['simplifier'] = digest(args.simplifier)
            result['hashes']['unit_simplify.cpp'] = digest(HERE/'unit_simplify.cpp')
            solve_cnf = target/'solve.cnf'
            if not run('simplify',[str(args.simplifier),str(target/'case.cnf'),str(solve_cnf)],args.wall_seconds):
                result['status'] = 'SIMPLIFICATION_INCOMPLETE'
                return
            result['simplified'] = json.loads((target/'simplify.log').read_text())
        result['proof_cnf'] = str(solve_cnf)
        if args.generate_only:
            result['status'] = 'GENERATED'
            return
        result['status'] = 'SOLVING'
        solver = ['/usr/bin/cadical','-q','-t',str(args.solve_seconds),'--lrat=true','--binary=false',
                  str(solve_cnf),str(target/'case.lrat')]
        run('solver',solver,args.solve_seconds+2)
        lines = (target/'solver.log').read_text(errors='replace').splitlines() if (target/'solver.log').exists() else []
        if 's SATISFIABLE' in lines and 's UNSATISFIABLE' not in lines:
            result['status'] = 'SAT_AUDIT_PENDING'
            checked = run('audit',[sys.executable,'-B',str(HERE/'audit_extension.py'),
                          '--source',str(args.source),'--meta',str(target/'meta.json'),
                          '--cnf',str(target/'case.cnf'),'--model',str(target/'solver.log'),
                          '--out',str(target/'audit.json')],args.wall_seconds)
            result['status'] = 'SAT_CHECKED_ABSTRACT' if checked else 'SAT_AUDIT_INCOMPLETE'
        elif 's UNSATISFIABLE' in lines and 's SATISFIABLE' not in lines:
            result['status'] = 'UNSAT_UNCERTIFIED'
        else:
            result['status'] = 'UNKNOWN'
    except Exception as exc:
        result['status'] = 'ERROR'
        result['error'] = repr(exc)
        raise
    finally:
        # These may include a partial LRAT: none is discarded or called certified.
        for file in sorted(target.iterdir()):
            if file.is_file() and file.name != 'result.json':
                result['hashes'][file.name] = digest(file)
        save()
        print(json.dumps({'out':str(target),'label':result['label'],'status':result['status']}))


if __name__ == '__main__':
    main()
