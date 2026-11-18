#!/usr/bin/env python3
"""Witness discovery only. No solver status is a proof of exclusion.

API reference: https://github.com/google/or-tools/blob/stable/ortools/sat/docs/solver.md
"""
import argparse
import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import resource
import sys

sys.dont_write_bytecode = True
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  PYTHONDONTWRITEBYTECODE='1', NUMEXPR_NUM_THREADS='1')
os.sched_setaffinity(0, {11})
resource.setrlimit(resource.RLIMIT_AS, (1000*1024**2, 1000*1024**2))
resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
ap = argparse.ArgumentParser()
ap.add_argument('directory')
ap.add_argument('--seconds', type=int, default=600)
ap.add_argument('--name', default='cpsat-1')
ap.add_argument('--seed', type=int, default=308)
ap.add_argument('--slice', type=int, choices=(19, 20))
ap.add_argument('--hint')
ap.add_argument('--linearization', type=int, choices=(0, 1, 2), default=2)
ap.add_argument('--provisional', help='UNCERTIFIED size9 demand-one rows, discovery only')
a = ap.parse_args()
assert datetime.datetime.now().time() < datetime.time(10, 45)
cutoff = datetime.datetime.combine(datetime.date.today(), datetime.time(10, 51, 15))
a.seconds = min(a.seconds, int((cutoff-datetime.datetime.now()).total_seconds()))
assert a.seconds > 0
folder = Path(a.directory).resolve()
out = folder/a.name
out.mkdir(exist_ok=False)
# Keep all library/solver output in the authorized output directory.
log = os.open(out/'solver.log', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
os.dup2(log, 1)
os.dup2(log, 2)
os.close(log)
status = {'label': 'COMPUTED running; witness discovery only',
          'started': datetime.datetime.now().isoformat(), 'AS_MiB': 1000,
          'CPU': 11, 'workers': 1, 'seconds_limit': a.seconds, 'seed': a.seed,
          'slice': a.slice, 'hint': a.hint, 'linearization_level': a.linearization,
          'provisional_path': a.provisional}
(out/'status.json').write_text(json.dumps(status, indent=2)+'\n')
try:
    from ortools.sat.python import cp_model
    import ortools
    meta = json.loads((folder/'encoding.json').read_text())
    base_bytes, pool_bytes = Path(meta['base']).read_bytes(), Path(meta['pool']).read_bytes()
    assert hashlib.sha256(base_bytes).hexdigest() == meta['base_sha256']
    assert hashlib.sha256(pool_bytes).hexdigest() == meta['pool_sha256']
    base = json.loads(gzip.decompress(base_bytes))
    pool = json.loads(pool_bytes)
    F = [i for i, s in enumerate(base['states']) if s[0] >= 5]
    Lo = [i for i, s in enumerate(base['states']) if s[0] <= 4]
    assert len(F) == 84 and len(Lo) == 70 and len(pool) == meta['pool_rows']
    active_slice = a.slice or meta['slice']
    provisional = []
    if a.provisional:
        provisional_bytes = Path(a.provisional).read_bytes()
        provisional = json.loads(provisional_bytes)
        assert all(r['rhs'] == 1 and len(r['support']) == 9 for r in provisional)
        status['provisional_sha256'] = hashlib.sha256(provisional_bytes).hexdigest()
        status['provisional_rows'] = len(provisional)
        status['label'] = 'HEURISTIC running with uncertified rows; discovery only'
        (out/'status.json').write_text(json.dumps(status, indent=2)+'\n')
    model = cp_model.CpModel()
    h = [model.new_bool_var('h'+str(i)) for i in range(154)]
    model.add(h[0] == 0)
    for row in base['constraints'] + pool + provisional:
        S, d = row['support'], row['rhs']
        assert len(S) == len(set(S)) and all(type(i) is int and 0 <= i < 154 for i in S)
        assert type(d) is int and 1 <= d <= len(S)
        model.add(sum(h[i] for i in S) >= d)
    model.add(sum(h[i] for i in F) >= (active_slice or 19))
    model.add(sum(h[i] for i in Lo) >= (34-active_slice if active_slice else 14))
    model.add(sum(h) <= 34)
    if a.hint:
        hint = json.loads(Path(a.hint).read_text())
        assert len(hint) == 154 and all(type(v) is int and v in (0, 1) for v in hint)
        for variable, value in zip(h, hint):
            model.add_hint(variable, value)
    assert model.validate() == ''
    model.export_to_file(str(out/'model.pbtxt'))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.max_time_in_seconds = a.seconds
    solver.parameters.max_memory_in_mb = 700
    solver.parameters.random_seed = a.seed
    solver.parameters.linearization_level = a.linearization
    solver.parameters.log_search_progress = True
    if a.hint:
        solver.parameters.repair_hint = True
        solver.parameters.hint_conflict_limit = 10000
    result = solver.solve(model)
    status.update(label='COMPUTED '+solver.status_name(result)+'; no exclusion certificate',
                  finished=datetime.datetime.now().isoformat(),
                  solver_version=ortools.__version__, solver_statistics=solver.response_stats(),
                  peak_RSS_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if provisional:
        status['label'] = 'HEURISTIC '+solver.status_name(result)+' with uncertified rows; NO exclusion evidence'
    if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        holes = [int(solver.value(v)) for v in h]
        (out/'raw-holes.json').write_text(json.dumps(holes)+'\n')
        status['label'] = 'COMPUTED candidate SAT; independent check pending'
        status['hole_bits_index_0_first'] = ''.join(map(str, holes))
    (out/'status.json').write_text(json.dumps(status, indent=2)+'\n')
    if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sys.stdout.flush()
        sys.stderr.flush()
        # exec releases OR-Tools before the independent checking phase.
        os.execv(sys.executable, [sys.executable, str(Path(__file__).with_name('extend_assignment.py')),
                 str(folder), str(out/'raw-holes.json'), str(out)])
except BaseException as exc:
    status['exception'] = repr(exc)
    status['label'] = 'COMPUTED failed; no conclusion'
    (out/'status.json').write_text(json.dumps(status, indent=2)+'\n')
    raise
