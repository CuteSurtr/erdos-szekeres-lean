#!/usr/bin/env python3
"""Arm B: alternating SAT / geometry (realizability feedback).
  M_0 = a random-phase SAT model of the (7,5,7)@26 CNF.
  Loop: Q = penalty descent (realize.py, mode free) on the chirotope of M_t, warm-started at Q_{t-1};
        D = triples where the float chirotope of Q disagrees with M_t;
        T = points left after greedily deleting the point in most disagreements until none remain;
        M_{t+1} = CaDiCaL model with assumptions chi_Q restricted to triples inside T (= M_t there)
                  and initial phases chi_Q on every orientation variable (plus a blocking clause on
                  M_t so the model changes).
  A model is reported realized only after integer rounding and exact re-check of all C(26,3)
  orientations (chiro.verify_exact).  Output: JSON lines (one per iteration) and model lines."""
import sys, os, json, argparse, itertools, time, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../F/realizer"))
import numpy as np
import chiro, realize as R
from pysat.formula import CNF
from pysat.solvers import Solver
ap = argparse.ArgumentParser()
ap.add_argument("cnf"); ap.add_argument("--n", type=int, default=26)
ap.add_argument("--seed", type=int, default=1); ap.add_argument("--time", type=float, default=600)
ap.add_argument("--iters", type=int, default=40); ap.add_argument("--pd", type=float, default=2.0)
ap.add_argument("-o", required=True)
a = ap.parse_args()
n = a.n; TR = list(itertools.combinations(range(n), 3)); nx = len(TR); VID = {t: i + 1 for i, t in enumerate(TR)}
rng = random.Random(a.seed); nrng = np.random.default_rng(a.seed)
cnf = CNF(from_file=a.cnf)
out = open(a.o, "a"); mod_out = open(a.o + ".models", "a")
def solve(asm, phases, block):
    s = Solver(name="cadical195", bootstrap_with=cnf.clauses)
    for b in block: s.add_clause(b)
    s.set_phases(phases)
    ok = s.solve(assumptions=asm); m = s.get_model()[:nx] if ok else None
    s.delete(); return m
t_start = R._clock(); w0 = time.time(); run = 0
while time.time() - w0 < a.time:
    run += 1
    m = solve([], [v if rng.random() < 0.5 else -v for v in range(1, nx + 1)], [])
    Q = None; blocks = []; hist = []
    for it in range(a.iters):
        chi = {t: (1 if m[i] > 0 else -1) for i, t in enumerate(TR)}
        mod_out.write("".join("+" if x > 0 else "-" for x in m) + "\n"); mod_out.flush()
        prob = R.Prob(chi, n)
        pts, bv, bxy = R.penalty_descent(prob, nrng, R._clock() + a.pd, mode="free", R=24, steps=500,
                                         init=Q, max_rounds=None)
        rec = {"run": run, "seed": a.seed, "iter": it, "viol": bv}
        if pts is not None:
            ok, bad, zero = chiro.verify_exact(pts, chi)
            rec.update(realized=bool(ok), points=[list(p) for p in pts], model="".join("+" if x > 0 else "-" for x in m))
            out.write(json.dumps(rec) + "\n"); out.flush()
            print("REALIZED", run, it, ok, flush=True)
            break
        Q = bxy; x, y = Q
        A_, B_, C_ = prob.A, prob.B, prob.C
        D = (x[B_] - x[A_]) * (y[C_] - y[A_]) - (y[B_] - y[A_]) * (x[C_] - x[A_])
        sq = np.where(D > 0, 1, -1)
        dis = np.nonzero(sq != prob.S)[0]
        alive = set(range(n)); dl = [TR[i] for i in dis]
        while True:
            cnt = [0] * n
            for t in dl:
                if all(p in alive for p in t):
                    for p in t: cnt[p] += 1
            if max(cnt) == 0: break
            alive.discard(int(np.argmax(cnt)))
        phases = [VID[t] if sq[i] > 0 else -VID[t] for i, t in enumerate(TR)]
        asm = [phases[i] for i, t in enumerate(TR) if all(p in alive for p in t)]
        blocks.append([-x_ for x_ in m])
        m2 = solve(asm, phases, blocks)
        rec.update(disagree=int(len(dis)), T=len(alive), sat=m2 is not None)
        out.write(json.dumps(rec) + "\n"); out.flush()
        if m2 is None: break
        m = m2
