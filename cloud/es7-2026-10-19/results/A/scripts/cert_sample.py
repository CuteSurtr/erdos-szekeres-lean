#!/usr/bin/env python3
"""Independent re-check of a random sample of one-point-extension answers.

usage: cert_sample.py WORKDIR TOOLS_TRACKB OUT.jsonl K SEED [workers]

For K random (set, position) pairs of the main run (all of whose answers were UNSAT), the
non-incremental CNF is rebuilt with the repository's own tools/trackB/ext_cnf.py (an index map
written independently of ext_solve.cpp), solved by the stand-alone CaDiCaL binary with a DRAT
proof, and the proof is checked with drat-trim. As a positive counterpart, 5 SAT answers of
control C1 (31 -> 32 points, the deleted point's own position) are rebuilt the same way and must
come back SAT. "VERIFIED" here is a statement about that CNF only.
"""
import json
import os
import random
import subprocess
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigutil import write_sigfile, delete_point  # noqa: E402

WD = TB = None


def _init(wd, tb):
    global WD, TB
    WD, TB = wd, tb


def one(job):
    sid, n, signs, p, base, expect = job
    tag = f"{sid}_p{p}_{os.getpid()}"
    sigf = os.path.join(WD, 'tmp', f"{tag}.sig")
    cnf = os.path.join(WD, 'tmp', f"{tag}.cnf")
    prf = os.path.join(WD, 'tmp', f"{tag}.drat")
    write_sigfile(sigf, n, signs)
    subprocess.run([sys.executable, os.path.join(TB, 'ext_cnf.py'), sigf, str(n), str(p), os.path.join(WD, base), cnf],
                   check=True)
    r = subprocess.run([os.path.join(WD, '..', 'cadical', 'build', 'cadical'), '-q', cnf, prf],
                       capture_output=True, text=True)
    rec = {"set": sid, "n_old": n, "p": p, "base": base, "expect": expect, "cadical_exit": r.returncode}
    if r.returncode == 20:
        d = subprocess.run([os.path.join(WD, 'drat-trim'), cnf, prf], capture_output=True, text=True)
        rec["drat_trim"] = "VERIFIED" if "s VERIFIED" in d.stdout else d.stdout.strip().splitlines()[-1:]
    for f in (sigf, cnf, prf):
        if os.path.exists(f):
            os.remove(f)
    return rec


def main():
    wd, tb, out, K, seed = sys.argv[1:6]
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 8
    rng = random.Random(int(seed))
    sets = [l.split() for l in open(os.path.join(wd, 'main.sig')) if l.strip()]
    jobs = []
    for t in rng.sample(sets, int(K)):
        jobs.append((t[0], 32, t[-1], rng.randint(1, 33), 'n33k7.cnf', 'UNSAT'))
    pool_sig = {l.split()[0]: l.split()[-1] for l in open(os.path.join(wd, 'pool.sig'))}
    c1 = json.load(open(os.path.join(wd, 'controls.json')))["C1"]["per_set"]
    for lab in list(c1)[:5]:
        _, sid, q = lab.split('_')
        q = int(q[1:])
        jobs.append((f"c1_{sid}_q{q}", 31, delete_point(32, pool_sig[sid], q), q, 'n32k7.cnf', 'SAT'))
    res = []
    with Pool(workers, initializer=_init, initargs=(os.path.abspath(wd), os.path.abspath(tb))) as pool:
        for r in pool.imap_unordered(one, jobs):
            res.append(r)
    with open(out, 'w') as f:
        for r in res:
            f.write(json.dumps(r) + "\n")
    unsat_ok = sum(1 for r in res if r["expect"] == 'UNSAT' and r["cadical_exit"] == 20 and r.get("drat_trim") == "VERIFIED")
    sat_ok = sum(1 for r in res if r["expect"] == 'SAT' and r["cadical_exit"] == 10)
    print(json.dumps({"unsat_sample": int(K), "unsat_drat_verified": unsat_ok, "sat_controls": 5, "sat_ok": sat_ok}))


if __name__ == '__main__':
    main()
