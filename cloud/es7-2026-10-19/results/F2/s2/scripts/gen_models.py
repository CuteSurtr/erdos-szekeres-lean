#!/usr/bin/env python3
"""Generate distinct models of the (7,5,7)@26 ETV CNF (tools/etv/gen_etv.py 26 5 7 7: no 5-cap,
no 7-cup, no convex 7-gon) with CaDiCaL (pysat), diversified by random initial phases on the
orientation variables, random unit assumptions on a few orientation variables, and blocking
clauses on all orientation variables.  Output: one line per model, C(n,3) chars '+'/'-' (X(i,j,k)
lexicographic, '+' = ccw = cup triple)."""
import sys, random, argparse, time
from pysat.formula import CNF
from pysat.solvers import Solver
ap = argparse.ArgumentParser()
ap.add_argument("cnf"); ap.add_argument("--n", type=int, default=26)
ap.add_argument("--count", type=int, default=1000); ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--assume", type=int, default=6, help="random unit assumptions per solve")
ap.add_argument("--rebuild", type=int, default=50, help="fresh solver (new random phases) every R models")
ap.add_argument("--time", type=float, default=1e9)
ap.add_argument("-o", required=True)
a = ap.parse_args()
nx = a.n * (a.n - 1) * (a.n - 2) // 6
rng = random.Random(a.seed)
cnf = CNF(from_file=a.cnf)
seen = set(); blocks = []
out = open(a.o, "w"); t0 = time.time(); s = None; made = 0; tries = 0
while made < a.count and time.time() - t0 < a.time:
    if s is None or made % a.rebuild == 0 and made:
        if s: s.delete()
        s = Solver(name="cadical195", bootstrap_with=cnf.clauses)
        for b in blocks: s.add_clause(b)
        s.set_phases([v if rng.random() < 0.5 else -v for v in range(1, nx + 1)])
    tries += 1
    asm = [v if rng.random() < 0.5 else -v for v in rng.sample(range(1, nx + 1), a.assume)]
    if not s.solve(assumptions=asm):
        continue
    m = s.get_model()[:nx]
    key = "".join("+" if x > 0 else "-" for x in m)
    if key in seen: continue
    seen.add(key)
    bl = [-x for x in m]; blocks.append(bl); s.add_clause(bl)
    out.write(key + "\n"); out.flush(); made += 1
print(f"models {made} tries {tries} seconds {time.time()-t0:.1f}", file=sys.stderr)
