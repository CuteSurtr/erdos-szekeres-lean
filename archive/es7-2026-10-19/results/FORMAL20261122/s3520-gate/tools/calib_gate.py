#!/usr/bin/env python3
"""s3520-gate (22 Nov 2026): per-leaf cost of the gate's finished chunk compiles (HEURISTIC calibration; read-only).

  calib_gate.py EXPORT TAG UNIT [UNIT ...]

Per module with an olean: leaves (manifest), wall and user+sys seconds and max RSS (/usr/bin/time in its log), anon +
shmem peak (its .mem file, sampled every 0.5 s), source and olean bytes. Prints one JSON line per unit and one for all."""
import json
import re
import sys
from pathlib import Path

G = Path("/home/jay/research/data/formalize-20261122/s3520-gate")


def secs(w):
    s = 0.0
    for x in w.split(":"):
        s = s * 60 + float(x)
    return s


def main():
    ex, tag, units = Path(sys.argv[1]), sys.argv[2], [int(u) for u in sys.argv[3:]]
    allt = dict(modules=0, leaves=0, wall=0.0, cpu=0.0, src=0, olean=0, anon=0, rss=0, missing=0)
    for u in units:
        man = json.loads((ex / "ctx" / f"ctx-{u:04d}.json").read_text())
        t = dict(modules=0, leaves=0, wall=0.0, cpu=0.0, src=0, olean=0, anon=0, rss=0, missing=0)
        per = []
        for m in man["modules"]:
            stem = m["module"].split(".")[-1]
            ol, lg, mem = G / f"olean/RS{tag}/{stem}.olean", G / f"logs/RS{tag}_{stem}.log", G / f"logs/RS{tag}_{stem}.mem"
            if not ol.exists():
                t["missing"] += 1
                continue
            log = lg.read_text(errors="replace")
            cpu = float(re.search(r"User time \(seconds\): ([\d.]+)", log).group(1)) + \
                float(re.search(r"System time \(seconds\): ([\d.]+)", log).group(1))
            wall = secs(re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([\d:.]+)", log).group(1))
            rss = int(re.search(r"Maximum resident set size \(kbytes\): (\d+)", log).group(1)) // 1024
            anon = int(re.search(r"anon_shmem_max_mb=(\d+)", mem.read_text()).group(1))
            t["modules"] += 1
            t["leaves"] += m["leaves"]
            t["wall"] += wall
            t["cpu"] += cpu
            t["src"] += (ex / m["file"]).stat().st_size
            t["olean"] += ol.stat().st_size
            t["anon"] = max(t["anon"], anon)
            t["rss"] = max(t["rss"], rss)
            per.append(cpu / m["leaves"])
        L = max(t["leaves"], 1)
        print(json.dumps({"unit": u, **{k: round(v, 1) if isinstance(v, float) else v for k, v in t.items()},
                          "cpu_s_per_leaf": round(t["cpu"] / L, 5), "wall_s_per_leaf": round(t["wall"] / L, 5),
                          "src_B_per_leaf": round(t["src"] / L), "olean_B_per_leaf": round(t["olean"] / L),
                          "per_module_cpu_s_per_leaf_range": [round(min(per), 5), round(max(per), 5)] if per else None}))
        for k in allt:
            allt[k] = max(allt[k], t[k]) if k in ("anon", "rss") else allt[k] + t[k]
    L = max(allt["leaves"], 1)
    print(json.dumps({"all": units, **{k: round(v, 1) if isinstance(v, float) else v for k, v in allt.items()},
                      "cpu_s_per_leaf": round(allt["cpu"] / L, 5), "wall_s_per_leaf": round(allt["wall"] / L, 5),
                      "src_B_per_leaf": round(allt["src"] / L), "olean_B_per_leaf": round(allt["olean"] / L)}))


if __name__ == "__main__":
    main()
