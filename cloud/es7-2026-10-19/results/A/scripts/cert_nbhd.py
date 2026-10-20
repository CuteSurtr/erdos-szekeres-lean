#!/usr/bin/env python3
"""DRAT re-check of a random sample of neighbourhood answers.

usage: cert_nbhd.py WORKDIR NBDIR K SEED OUT.jsonl [workers]

Picks K random (S, J) jobs from NBDIR/w*.jobs. For each, the map is recomputed from the label
(deleted set D) and the tag (extra gap e) and compared with the J line; then a stand-alone CNF is
written (33-point base CNF plus one unit clause per kept triple, in Python, independent of
ext_solve.cpp), solved by the CaDiCaL binary with a DRAT proof, and checked with drat-trim.
The answer must agree with the one ext_solve reported.
"""
import itertools
import json
import os
import random
import subprocess
import sys
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigutil import parse_outputs  # noqa: E402

WD = None


def _init(wd):
    global WD
    WD = wd


def one(job):
    lab, n, signs, tag, mp, reported = job
    M = 33
    # recompute the map from the label and the tag
    D = [int(v) for v in lab.rsplit('_', 1)[1].split('-')]
    e = int(tag[1:].split('@')[0])
    keep = [a for a in range(1, 33) if a not in D]
    gaps = [sum(1 for a in keep if a < d) for d in D] + [e]
    mp2 = [a + sum(1 for x in gaps if x <= a - 1) for a in range(1, len(keep) + 1)]
    idx = {t: i + 1 for i, t in enumerate(itertools.combinations(range(1, M + 1), 3))}
    units = []
    for (a, b, c), s in zip(itertools.combinations(range(1, n + 1), 3), signs):
        v = idx[(mp[a - 1], mp[b - 1], mp[c - 1])]
        units.append(v if s == '+' else -v)
    base = os.path.join(WD, 'n33k7.cnf')
    stem = os.path.join(WD, 'tmp', f"cn_{os.getpid()}_{random.random():.9f}")
    cnf, prf = stem + '.cnf', stem + '.drat'
    with open(base) as fi, open(cnf, 'w') as fo:
        for line in fi:
            if line.startswith('p cnf'):
                _, _, nv, nc = line.split()
                line = f"p cnf {nv} {int(nc) + len(units)}\n"
            fo.write(line)
        for u in units:
            fo.write(f"{u} 0\n")
    r = subprocess.run([os.path.join(WD, '..', 'cadical', 'build', 'cadical'), '-q', cnf, prf], capture_output=True)
    rec = {"label": lab, "tag": tag, "map_matches": mp == mp2, "reported": reported, "cadical_exit": r.returncode}
    if r.returncode == 20:
        d = subprocess.run([os.path.join(WD, 'drat-trim'), cnf, prf], capture_output=True, text=True)
        rec["drat_trim"] = "VERIFIED" if "s VERIFIED" in d.stdout else (d.stdout.strip().splitlines() or ['?'])[-1]
    for f in (cnf, prf):
        if os.path.exists(f):
            os.remove(f)
    return rec


def main():
    wd, nbdir, K, seed, out = sys.argv[1:6]
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else 4
    rep = {}
    for rec in parse_outputs(nbdir):
        if rec[0] == 'R':
            rep[(rec[1], rec[2])] = rec[3]
    jobs = []
    for fn in sorted(os.listdir(nbdir)):
        if not fn.endswith('.jobs'):
            continue
        cur = None
        for line in open(os.path.join(nbdir, fn)):
            t = line.split()
            if t[0] == 'S':
                cur = (t[1], int(t[2]), t[3])
            elif t[0] == 'J':
                jobs.append((cur[0], cur[1], cur[2], t[1], [int(v) for v in t[2:]], rep.get((cur[0], t[1]))))
    rng = random.Random(int(seed))
    pick = rng.sample(jobs, int(K))
    res = []
    with Pool(workers, initializer=_init, initargs=(os.path.abspath(wd),)) as pool:
        for r in pool.imap_unordered(one, pick):
            res.append(r)
    with open(out, 'w') as f:
        for r in res:
            f.write(json.dumps(r) + "\n")
    ok = sum(1 for r in res if r["map_matches"] and r["reported"] == 'UNSAT' and r["cadical_exit"] == 20
             and r.get("drat_trim") == "VERIFIED")
    print(json.dumps({"nbdir": nbdir, "sample": int(K), "unsat_drat_verified_and_map_ok": ok,
                      "maps_ok": sum(r["map_matches"] for r in res)}))


if __name__ == '__main__':
    main()
