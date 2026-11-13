#!/usr/bin/env python3
"""CP-SAT hunt for a balanced exclusion witness: a 0/1 hole vector x over the 252 balanced states with
  sum_{i in S} x_i >= d  for all 3,131 rows (S, d)   and   sum x_i <= B.
A feasible vector with B = 64 would show h_B^min <= 64 (budget 64 cannot be excluded over these rows);
with B = 71 it would beat the known 72-hole vector.

Rows are read exactly as the certificate code reads them: scripts/omission_row_probe.read_rows on
experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json (SHA-256 checked). Every
solution CP-SAT reports is re-checked with omission_row_probe.valid_holes (exact integers) and
appended to OUT/solutions.jsonl at once, so a long run that is killed keeps what it found.

usage: witness_hunt.py --budget B --seconds S [--threads T] [--seed K] [--minimize] [--cap C]
                       [--hint72] [--out DIR] [--tag NAME]
  --cap C    : impose sum x <= C instead of <= B (C >= B). With --minimize --hint72 --cap 72 the
               72-hole hint is feasible, so large-neighbourhood search starts from it at once; any
               solution with at most B holes is still what counts as a witness.
  --minimize : also minimise sum x (gives a dual bound in the log; keeps improving below B)
  --hint72   : use the recorded 72-hole vector (ES8SLACK/witnesses.json) as a solution hint
Result: OUT/<tag>.result.json (status FEASIBLE/OPTIMAL = witness found, INFEASIBLE = proved none,
UNKNOWN = time out) and OUT/<tag>.log (CP-SAT progress log). Exit 3 if an exactly valid witness was found.
"""
import argparse, hashlib, json, os, sys, time
from pathlib import Path

REPO = Path(os.environ.get('ES_REPO', '<repo>'))
BAL = REPO / 'experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
BAL_SHA = 'acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72'
W72 = REPO / 'cloud/es7-2026-10-19/results/ES8SLACK/witnesses.json'
sys.path.insert(0, str(REPO / 'scripts'))
from omission_row_probe import read_rows, valid_holes  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--budget', type=int, required=True)
    ap.add_argument('--seconds', type=float, required=True)
    ap.add_argument('--threads', type=int, default=1)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--minimize', action='store_true')
    ap.add_argument('--cap', type=int, default=None)
    ap.add_argument('--hint72', action='store_true')
    ap.add_argument('--out', default=str(Path(__file__).resolve().parent / 'witness'))
    ap.add_argument('--tag', default=None)
    a = ap.parse_args()
    tag = a.tag or f'b{a.budget}-t{a.threads}-s{a.seed}' + ('-min' if a.minimize else '')
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    raw = BAL.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == BAL_SHA, 'catalog hash mismatch'
    n, rows = read_rows(json.loads(raw))
    assert n == 252 and len(rows) == 3131

    from ortools.sat.python import cp_model
    import ortools
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(n)]
    for support, demand in rows:
        if demand > 0:
            m.Add(sum(x[i] for i in support) >= demand)
    cap = a.budget if a.cap is None else a.cap
    assert cap >= a.budget
    m.Add(sum(x) <= cap)
    if a.minimize:
        m.Minimize(sum(x))
    if a.hint72:
        H = set(json.load(open(W72))['balanced_v2_72_hole_witness'])
        assert len(H) == 72 and valid_holes(n, rows, 72, sorted(H))
        for i in range(n):
            m.AddHint(x[i], 1 if i in H else 0)
    sv = cp_model.CpSolver()
    p = sv.parameters
    p.num_workers = a.threads
    p.max_time_in_seconds = a.seconds
    p.random_seed = a.seed
    p.log_search_progress = True
    p.log_to_stdout = False
    logf = open(out / f'{tag}.log', 'a', buffering=1)
    sv.log_callback = lambda s: logf.write(s + '\n')
    solf = out / 'solutions.jsonl'
    t0 = time.time()
    found = []

    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(self):
            holes = [i for i in range(n) if self.Value(x[i])]
            rows_ok = valid_holes(n, rows, n, holes)          # all rows, exact integers
            ok = rows_ok and len(holes) <= a.budget
            rec = {'tag': tag, 'budget': a.budget, 't': round(time.time() - t0, 1), 'holes': len(holes),
                   'rows_valid': rows_ok, 'exact_valid': ok, 'set': holes, 'time': time.strftime('%F %T')}
            found.append(rec)
            with open(solf, 'a') as f:
                f.write(json.dumps(rec) + '\n')

    logf.write(f'# {tag} start {time.strftime("%F %T")} ortools {ortools.__version__}\n')
    st = sv.Solve(m, CB())
    res = {'tag': tag, 'budget': a.budget, 'threads': a.threads, 'seed': a.seed, 'minimize': a.minimize, 'cap': cap,
           'hint72': a.hint72, 'seconds_limit': a.seconds, 'wall_s': round(time.time() - t0, 1),
           'status': sv.StatusName(st), 'solutions': len(found),
           'best_holes': min((r['holes'] for r in found), default=None),
           'any_exact_valid': any(r['exact_valid'] for r in found),
           'objective_bound': sv.BestObjectiveBound() if a.minimize else None,
           'branches': sv.NumBranches(), 'conflicts': sv.NumConflicts(),
           'ortools': ortools.__version__, 'catalog_sha256': BAL_SHA, 'finished': time.strftime('%F %T')}
    (out / f'{tag}.result.json').write_text(json.dumps(res, indent=1))
    print(json.dumps(res), flush=True)
    sys.exit(3 if res['any_exact_valid'] else 0)


if __name__ == '__main__':
    main()
