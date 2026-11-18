"""Witness pre-killer for a pair (c, c2): CP-SAT over 2,650 rows + certified rows + h(F) >= 84-c +
h(Lo) >= 70-c2 + h0 = 0 + sum h <= 33.  Each vector found is killed (certify violated pooled rows with
cake_lpr; if none is violated, probe for new coupled cores, certify and transport them), exactly as
res33's capfinder.py.  INFEASIBLE from CP-SAT is only COMPUTED.
Usage: lofinder.py c c2 deadline_epoch workers [round_seconds]"""
import json, os, random, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from lo_common import *
import certify, coupled, shrink_tests
from probe_vec import candidates, minimize
from ortools.sat.python import cp_model
c, c2 = int(sys.argv[1]), int(sys.argv[2]); DL = float(sys.argv[3]); W = int(sys.argv[4])
RS = float(sys.argv[5]) if len(sys.argv) > 5 else 600
BUD = int(os.environ.get('LO_BUDGET', '33'))
LOG = open(os.path.join(HERE, 'lofinder.log'), 'a')
def log(**kw):
    kw['t'] = time.strftime('%H:%M:%S'); kw['pair'] = [c, c2]; kw['budget'] = BUD; LOG.write(json.dumps(kw) + '\n'); LOG.flush(); print(json.dumps(kw), flush=True)
def cert(S):
    r = certify.certify(sorted(S))
    with open(os.path.join(HERE, 'certified.jsonl'), 'a') as f: f.write(json.dumps(r) + '\n')
    return r['verdict'] == 's VERIFIED UNSAT'
pool_rows = pooled()
while time.time() < DL - 60:
    cs = certified_supports()
    m = cp_model.CpModel(); h = [m.NewBoolVar(f'h{i}') for i in range(N)]
    m.Add(h[0] == 0)
    for s, d in ROWS: m.Add(sum(h[i] for i in s) >= d)
    for s in cs: m.AddBoolOr([h[i] for i in s])
    m.Add(sum(h[i] for i in F) >= 84 - c); m.Add(sum(h[i] for i in LO) >= 70 - c2); m.Add(sum(h) <= BUD)
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = max(10, min(RS, DL - time.time() - 30))
    sol.parameters.num_workers = W; sol.parameters.random_seed = random.randrange(10**6)
    t0 = time.time(); st = sol.Solve(m); name = sol.StatusName(st)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        log(event='round', status=name, certified=len(cs), seconds=round(time.time() - t0, 1))
        if name == 'INFEASIBLE': break
        continue
    H = [i for i in range(N) if sol.Value(h[i])]
    assert len(H) <= BUD and 0 not in H and not check(H, ROWS + [(tuple(s), 1) for s in cs])
    occ = set(range(N)) - set(H)
    viol = [S for S in pool_rows if set(S) <= occ]
    random.shuffle(viol)
    got = sum(cert(S) for S in viol[:10])
    how = 'pooled'
    if not got:
        how = 'probe'
        cands, nf = candidates(H, [(tuple(s), d) for s, d in ROWS], random.Random(sum(H)), limit=2500)
        found = []
        for S in cands:
            if coupled.fast_solve(S, 30) == 'unsat':
                found.append(S)
                if len(found) >= 3: break
        new = []
        for core in {tuple(sorted(minimize(S))) for S in found}:
            got += cert(list(core))
            tr = shrink_tests.run(list(core), transport_seconds=60)
            if tr:
                new += [sorted(s) for s in tr['supports']]
        if new:
            pool_rows += new
            lp = os.path.join(HERE, 'lonewrows.json')
            old = json.load(open(lp)) if os.path.exists(lp) else []
            old += [{'support': s, 'kind': 'transport', 'from_pair': [c, c2]} for s in new]
            json.dump(old, open(lp + f'.{os.getpid()}', 'w'), separators=(',', ':')); os.replace(lp + f'.{os.getpid()}', lp)
    log(event='vector', holes=H, F_occupied=len(set(F) - set(H)), Lo_occupied=len(set(LO) - set(H)), killed_by=how,
        new_certified=got, pooled_violations=len(viol), seconds=round(time.time() - t0, 1))
    if not got:
        log(event='STUCK', holes=H); break
