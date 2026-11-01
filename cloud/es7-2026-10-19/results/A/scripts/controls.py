#!/usr/bin/env python3
"""Positive and negative controls for ext_solve (run before trusting any extension answer).

usage: controls.py WORKDIR OUT.json [workers]
WORKDIR must contain: ext_solve, brute_kgon, n32k7.cnf, n33k7.cnf, pool.sig, extra/*.sig, tmp/.

C1 (positive, required): 30 pool sets (evenly spaced ids), one point q deleted (seeded random);
   the 31-point signotope is extended with the 32-point base CNF at p = 1..32. Position q must be
   SAT. Every SAT model is checked by brute force.
C2 (positive): every pool set and AE-derived 32-point set, all 4,960 triples fixed in the 32-point
   CNF, must be SAT (the encoding accepts the known heptagon-free signotopes).
C3 (negative, required): signotopes containing a convex 7-gon must be rejected:
   the 273 near-full 33-point sets and AlphaEvolve's 33-point set (all triples fixed, 33-point CNF)
   must be UNSAT and brute_kgon must find a convex 7-subset; 3 AE 32-point sets that keep the 7-gon
   must be UNSAT at all 33 extension positions; a pool set with one triple flipped so that it
   breaks the signotope axiom must be flagged by brute_kgon and be UNSAT with all triples fixed.
"""
import json
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigutil import delete_point, parse_outputs, check_model, brute, is_signotope, triples  # noqa
from run_ext import run_pool  # noqa


def load_sig(path):
    out = []
    for l in open(path):
        t = l.split()
        if t:
            out.append((t[0], int(t[-2]), t[-1]))
    return out


def results(outdir):
    R, W = {}, {}
    for rec in parse_outputs(outdir):
        if rec[0] == 'R':
            R[(rec[1], rec[2])] = rec[3:]
        else:
            W[(rec[1], rec[2])] = rec[3]
    return R, W


def main():
    wd, outjson = sys.argv[1], sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else os.cpu_count()
    ex = os.path.join(wd, 'ext_solve')
    bb = os.path.join(wd, 'brute_kgon')
    tmp = os.path.join(wd, 'tmp')
    cnf32, cnf33 = os.path.join(wd, 'n32k7.cnf'), os.path.join(wd, 'n33k7.cnf')
    pool = load_sig(os.path.join(wd, 'pool.sig'))
    rep = {}

    # C1
    rng = random.Random(20261019)
    pick = [pool[round(k * (len(pool) - 1) / 29)] for k in range(30)]
    c1sets = {}
    blocks = []
    for sid, n, sg in pick:
        q = rng.randint(1, 32)
        s31 = delete_point(32, sg, q)
        lab = f"c1_{sid}_q{q}"
        c1sets[lab] = (q, s31)
        blocks.append("".join([f"S {lab} 31 {s31}\n"] + [f"P {p}\n" for p in range(1, 33)]))
    run = run_pool(ex, cnf32, 32, 0, blocks, os.path.join(wd, 'ctl_c1'), workers)
    R, W = results(os.path.join(wd, 'ctl_c1'))
    own_sat = 0
    model_checks = Counter()
    per = {}
    for lab, (q, s31) in c1sets.items():
        st = Counter(R[(lab, f"p{p}")][0] for p in range(1, 33))
        per[lab] = dict(st)
        own_sat += R[(lab, f"p{q}")][0] == 'SAT'
    for (lab, tag), model in W.items():
        q, s31 = c1sets[lab]
        c = check_model(bb, 32, model, 31, s31, tag, tmp)
        ok = c["old_triples_agree"] and c["py_signotope"] and c["brute_violations"] == 0 and c["brute_convex"] == 0
        model_checks["ok" if ok else "FAIL"] += 1
    rep["C1"] = {"sets": 30, "own_position_SAT": own_sat, "solve_runs": run,
                 "status_counts": dict(Counter(v[0] for v in R.values())),
                 "sat_models_checked": dict(model_checks), "per_set": per,
                 "pass": own_sat == 30 and model_checks["FAIL"] == 0}

    # C2
    ae = load_sig(os.path.join(wd, 'extra', 'ae.sig'))
    blocks = [f"S {sid} 32 {sg}\nJ full@ " + " ".join(map(str, range(1, 33))) + "\n" for sid, n, sg in pool + ae]
    run = run_pool(ex, cnf32, 32, 0, blocks, os.path.join(wd, 'ctl_c2'), workers)
    R, W = results(os.path.join(wd, 'ctl_c2'))
    st = Counter(v[0] for v in R.values())
    rep["C2"] = {"sets": len(blocks), "status_counts": dict(st), "solve_runs": run,
                 "pass": st.get('SAT', 0) == len(blocks)}

    # C3
    nf = load_sig(os.path.join(wd, 'extra', 'nearfull.sig')) + load_sig(os.path.join(wd, 'extra', 'ae33.sig'))
    blocks = [f"S {sid} 33 {sg}\nJ full@ " + " ".join(map(str, range(1, 34))) + "\n" for sid, n, sg in nf]
    run = run_pool(ex, cnf33, 33, 0, blocks, os.path.join(wd, 'ctl_c3a'), workers)
    R, W = results(os.path.join(wd, 'ctl_c3a'))
    st = Counter(v[0] for v in R.values())
    br = [brute(bb, 33, 7, sg, tmp, sid)["convex"] for sid, n, sg in nf]
    rep["C3_full33"] = {"sets": len(nf), "status_counts": dict(st), "solve_runs": run,
                        "brute_min_convex7": min(br), "brute_max_convex7": max(br),
                        "pass": st.get('UNSAT', 0) == len(nf) and min(br) >= 1}
    bad = load_sig(os.path.join(wd, 'extra', 'ae_bad.sig'))
    blocks = ["".join([f"S {sid} 32 {sg}\n"] + [f"P {p}\n" for p in range(1, 34)]) for sid, n, sg in bad]
    run = run_pool(ex, cnf33, 33, 0, blocks, os.path.join(wd, 'ctl_c3b'), workers)
    R, W = results(os.path.join(wd, 'ctl_c3b'))
    st = Counter(v[0] for v in R.values())
    br = [brute(bb, 32, 7, sg, tmp, sid)["convex"] for sid, n, sg in bad]
    rep["C3_ext_with_7gon"] = {"sets": len(bad), "status_counts": dict(st), "brute_convex7": br,
                               "pass": st.get('UNSAT', 0) == 33 * len(bad) and min(br) >= 1}
    # flipped triple: find a flip in pool set 0 that breaks the signotope axiom
    sid, n, sg = pool[0]
    T = triples(32)
    for t in range(len(T)):
        s2 = sg[:t] + ('-' if sg[t] == '+' else '+') + sg[t + 1:]
        if not is_signotope(32, s2):
            break
    b = brute(bb, 32, 7, s2, tmp, 'flip')
    run = run_pool(ex, cnf32, 32, 0, [f"S flip_{sid}_{T[t][0]}-{T[t][1]}-{T[t][2]} 32 {s2}\nJ full@ " +
                                      " ".join(map(str, range(1, 33))) + "\n"],
                   os.path.join(wd, 'ctl_c3c'), 1)
    R, W = results(os.path.join(wd, 'ctl_c3c'))
    st = Counter(v[0] for v in R.values())
    rep["C3_flipped"] = {"set": sid, "flipped_triple": T[t], "brute_violations": b["violations"],
                         "status_counts": dict(st),
                         "pass": b["violations"] > 0 and st.get('UNSAT', 0) == 1}
    rep["all_pass"] = all(v["pass"] for k, v in rep.items() if isinstance(v, dict) and "pass" in v)
    json.dump(rep, open(outjson, 'w'), indent=1)
    print(json.dumps({k: (v["pass"] if isinstance(v, dict) and "pass" in v else v) for k, v in rep.items()}))


if __name__ == '__main__':
    main()
