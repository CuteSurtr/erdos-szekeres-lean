#!/usr/bin/env python3
"""DRAT re-check of a random sample of nbhd2.py answers (independent of ext_solve.cpp).

usage: cert2.py WORKDIR BASES.jsonl RUNDIR K SEED OUT.jsonl [workers]
For each sampled job: the kept signotope is rebuilt from BASES.jsonl and the deleted set in the
label (not from the S line), the map is rebuilt from the new indices in the tag and compared with
the J line, a stand-alone CNF (33-point base CNF + one unit clause per kept triple) is solved by the
CaDiCaL binary with a DRAT proof, and drat-trim checks the proof.
"""
import itertools
import json
import os
import random
import subprocess
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'A', 'scripts'))
from sigutil import parse_outputs  # noqa: E402

WD = BASES = None


def _init(wd, bf):
    global WD, BASES
    WD = wd
    BASES = {}
    for l in open(bf):
        b = json.loads(l)
        BASES[b["id"]] = b["signs"]


def one(job):
    lab, tag, mp, reported = job
    M = 33
    bid, kind, D = lab.split(':')
    D = [int(v) for v in D.split('-')]
    keep = [a for a in range(1, 33) if a not in D]
    T32 = list(itertools.combinations(range(1, 33), 3))
    old = [c for t, c in zip(T32, BASES[bid]) if all(x in keep for x in t)]
    new = [int(v) for v in tag.split('@')[1].split('.')]
    mp2 = [t for t in range(1, M + 1) if t not in new]
    idx = {t: i + 1 for i, t in enumerate(itertools.combinations(range(1, M + 1), 3))}
    units = []
    for (a, b, c), s in zip(itertools.combinations(range(1, len(keep) + 1), 3), old):
        v = idx[(mp2[a - 1], mp2[b - 1], mp2[c - 1])]
        units.append(v if s == '+' else -v)
    stem = os.path.join(WD, 'tmp', f"c2_{os.getpid()}_{random.random():.9f}")
    cnf, prf = stem + '.cnf', stem + '.drat'
    with open(os.path.join(WD, 'n33k7.cnf')) as fi, open(cnf, 'w') as fo:
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
        d = subprocess.run([os.path.join(WD, '..', 'drat-trim', 'drat-trim'), cnf, prf, '-t', '20000'],
                           capture_output=True, text=True)
        rec["drat_trim"] = "VERIFIED" if "s VERIFIED" in d.stdout else (d.stdout.strip().splitlines() or ['?'])[-1]
    for f in (cnf, prf):
        if os.path.exists(f):
            os.remove(f)
    return rec


def main():
    wd, bf, rd, K, seed, out = sys.argv[1:7]
    workers = int(sys.argv[7]) if len(sys.argv) > 7 else 1
    rep = {(r[1], r[2]): r[3] for r in parse_outputs(rd) if r[0] == 'R'}
    jobs = []
    for fn in sorted(os.listdir(rd)):
        if fn.endswith('.jobs'):
            cur = None
            for line in open(os.path.join(rd, fn)):
                t = line.split()
                if t[0] == 'S':
                    cur = t[1]
                elif t[0] == 'J':
                    jobs.append((cur, t[1], [int(v) for v in t[2:]], rep.get((cur, t[1]))))
    pick = random.Random(int(seed)).sample(jobs, int(K))
    with Pool(workers, initializer=_init, initargs=(os.path.abspath(wd), bf)) as pool:
        res = list(pool.imap_unordered(one, pick))
    with open(out, 'w') as f:
        for r in res:
            f.write(json.dumps(r) + "\n")
    ok = sum(1 for r in res if r["map_matches"] and r["reported"] == 'UNSAT' and r["cadical_exit"] == 20
             and r.get("drat_trim") == "VERIFIED")
    print(json.dumps({"rundir": rd, "sample": int(K), "unsat_drat_verified_and_map_ok": ok,
                      "maps_ok": sum(r["map_matches"] for r in res)}))


if __name__ == '__main__':
    main()
