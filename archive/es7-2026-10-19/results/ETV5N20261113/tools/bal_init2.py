"""Exact cycle-row optimum by lazy separation with CaDiCaL level tests (PB CNF at budget L: SAT -> vector,
UNSAT -> L+1).  COMPUTED (CaDiCaL verdicts).  Writes rows_cycle.json, cyc_opt.json."""
import json, time, random, subprocess, os
import etv_common as ec
from etv_common import N
from cyclists import masks, find_lists, extend
from pbcnf5 import build
M = masks(ec.TT); rng = random.Random(5); rows = {}
def level_test(rows, L):
    top, cls = build([(list(s), d) for s, d in rows.items()], L, N, ec.FIXED_OCC)
    p = f'lvl_{os.getpid()}.cnf'
    with open(p, 'w') as f:
        f.write(f'p cnf {top} {len(cls)}\n')
        for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')
    r = subprocess.run(['cadical', '-q', p], capture_output=True, text=True); os.remove(p)
    if r.returncode == 20: return None
    vals = set(int(x) for line in r.stdout.splitlines() if line.startswith('v') for x in line.split()[1:])
    return [i for i in range(N) if (i + 1) in vals]
t0 = time.time(); L = 0; it = 0
while True:
    it += 1
    H = level_test(rows, L)
    if H is None:
        L += 1; print(json.dumps({'it': it, 'level_up': L, 'rows': len(rows), 't': round(time.time() - t0, 1)}), flush=True); continue
    occ = [i for i in range(N) if i not in H]
    Ls = find_lists(M, occ, 8, limit=80, rng=rng)
    for l in Ls:
        E = extend(ec.TT, l, rng); rows[tuple(sorted(E))] = len(E) - 7
    print(json.dumps({'it': it, 'rows': len(rows), 'level': L, 'holes': len(H), 'new': len(Ls), 't': round(time.time() - t0, 1)}), flush=True)
    if not Ls: break
json.dump([[list(k), v] for k, v in rows.items()], open('rows_cycle.json', 'w'))
json.dump({'min_holes': len(H), 'holes': H}, open('cyc_opt.json', 'w'))
print('FINAL', len(H), 'capacity', N - len(H))
