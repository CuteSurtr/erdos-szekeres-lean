#!/usr/bin/env python3
"""Two-level lookahead cube-and-conquer over a random sample of top-level cubes.

Top level: march_cu -d 14 on the whole CNF (cubes_d14.icnf). For each sampled top cube c
(seeded random order, so the processed set is a uniform random sample):
  1. sub-CNF = CNF + units(c)                       (subcnf.py)
  2. march_cu -d D on the sub-CNF                   (second-level cubes)
  3. iworker (incremental CaDiCaL, one instance) on all second-level cubes, per-cube limit T
Records one JSON line per top cube in OUT/top.jsonl:
  id, march_s, n_sub, solve_s (sum), max_sub_s, n_U, n_S, n_T, wall_s, status
status: UNSAT if every sub-cube is U (and march finished), SAT if any S, OPEN otherwise.
Note: a top cube refuted by march itself yields 0 sub-cubes -> UNSAT.

usage: twolevel.py ROOT OUT --slots K --depth D --tlim T [--first id,id,..] [--seed S]
"""
import argparse, json, os, random, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("root"); ap.add_argument("out")
ap.add_argument("--slots", type=int, default=3); ap.add_argument("--depth", type=int, default=10)
ap.add_argument("--tlim", type=int, default=600); ap.add_argument("--first", default="")
ap.add_argument("--seed", type=int, default=12345); ap.add_argument("--n", type=int, default=100000)
a = ap.parse_args()
R = Path(a.root).resolve(); O = Path(a.out).resolve(); O.mkdir(parents=True, exist_ok=True)
HERE = Path(__file__).resolve().parent
ntop = sum(1 for l in open(R / "cubes_d14.icnf") if l.startswith("a "))
first = [int(x) for x in a.first.split(",") if x]
rest = list(range(ntop)); random.Random(a.seed).shuffle(rest)
order = first + [i for i in rest if i not in set(first)]
done = set()
if (O / "top.jsonl").exists():
    done = {json.loads(l)["id"] for l in open(O / "top.jsonl")}
order = [i for i in order if i not in done][: a.n]


def job(cid):
    t0 = time.time()
    d = O / f"c{cid}"; d.mkdir(exist_ok=True)
    cnf = d / "sub.cnf"; cub = d / f"d{a.depth}.icnf"
    subprocess.run([sys.executable, str(HERE / "subcnf.py"), str(R / "cnf/bbx.cnf"), str(R / "cubes_d14.icnf"),
                    str(cid), str(cnf)], check=True, capture_output=True)
    tm = time.time()
    pre = R / "sub" / f"c{cid}.d{a.depth}.icnf"
    if pre.exists():  # second-level cubes already made by an earlier manual march_cu run
        import shutil; shutil.copy(pre, cub)
        log = (R / "sub" / f"c{cid}.march.log").read_text()
        march_s = float(log.split("c time = ")[1].split()[0])
        class P: stdout = log; returncode = 0
        p = P()
    else:
      p = subprocess.run([str(R / "CnC/march_cu/march_cu"), str(cnf), "-d", str(a.depth), "-o", str(cub)],
                       capture_output=True, text=True)
      march_s = time.time() - tm
    refuted_by_march = "UNSATISFIABLE" in p.stdout or p.returncode == 20
    n_sub = sum(1 for l in open(cub) if l.startswith("a ")) if cub.exists() else 0
    rec = {"id": cid, "march_s": round(march_s, 2), "n_sub": n_sub, "march_rc": p.returncode}
    if n_sub > 0:
        subprocess.run([str(R / "iworker"), str(cnf), str(cub), "0", "1", str(a.tlim), "2925", str(d), "7"],
                       capture_output=True)
        rows = [l.split() for l in open(d / "w0.log") if not l.startswith("#")]
        ts = [float(r[2]) for r in rows]
        rec.update(solve_s=round(sum(ts), 2), max_sub_s=round(max(ts), 2),
                   n_U=sum(r[1] == "U" for r in rows), n_S=sum(r[1] == "S" for r in rows),
                   n_T=sum(r[1] == "T" for r in rows))
        rec["status"] = "SAT" if rec["n_S"] else ("UNSAT" if rec["n_U"] == n_sub else "OPEN")
        (d / "times.txt").write_text(" ".join(f"{r[1]}{r[2]}" for r in rows) + "\n")
    else:
        rec.update(solve_s=0.0, max_sub_s=0.0, n_U=0, n_S=0, n_T=0,
                   status="UNSAT" if refuted_by_march else "NOCUBES?")
        rec["march_tail"] = p.stdout[-300:]
    rec["wall_s"] = round(time.time() - t0, 2); rec["end"] = time.time()
    cnf.unlink(missing_ok=True); cub.unlink(missing_ok=True)
    with open(O / "top.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps(rec), flush=True)
    return rec


with ThreadPoolExecutor(a.slots) as ex:
    list(ex.map(job, order))
