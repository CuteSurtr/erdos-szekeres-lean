#!/usr/bin/env python3
"""CPU-time calibration of the worker: on a shared, oversubscribed machine wall seconds per job
overstate core time, so measure user+sys CPU seconds of one cncw process for a fixed list of
jobs (root cube and the first split cubes of the real runs, budget 10000 conflicts each).
usage: calib.py CACHE_DIR OUT.json"""
import json, resource, subprocess, sys, time
from pathlib import Path

C = Path(sys.argv[1]).resolve()
rows = []
for tag, nx in (("k7a5u6N26", 2600), ("k7a5u7N27", 2925)):
    ev = [json.loads(l) for l in open(C / "runs" / tag / "events.jsonl")][:3]
    jobs = "".join(f"{i} 10000 {' '.join(map(str, e['cube']))} 0\n" for i, e in enumerate(ev))
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN); t0 = time.time()
    p = subprocess.run([str(C / "cncw"), str(C / "inst" / f"{tag}_lexx.cnf"), str(nx), str(C / "wtest")],
                       input=jobs, capture_output=True, text=True)
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)
    rows.append({"instance": tag, "jobs": len(ev), "budget_conflicts": 10000, "cpu_s": round(cpu, 1),
                 "wall_s": round(time.time() - t0, 1), "replies": p.stdout.split("\n")[1:-1]})
    print(json.dumps(rows[-1]), flush=True)
Path(sys.argv[2]).write_text(json.dumps(rows, indent=1))
