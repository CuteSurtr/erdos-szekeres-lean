#!/usr/bin/env python3
"""Projection of the full compact ES(8) <= 311 run from the scaling trial (6 November 2026).

  project_es311.py --fit logs/es311/trial-fit.json --full build/es311/full \
      --root-s 120 --final-s 300 [--jobs 16 28]

For every module of the full manifests the wall time is predicted by the trial's per-side fit
wall = a + b * leaves (block limit 64). The modules are then scheduled longest first onto P
workers (greedy LPT), and the Roots and Final are added one after the other (the driver runs
them alone). Per-process wall times are taken as measured in the trial, i.e. on a machine
already loaded to about 35 runnable threads on 32 hardware threads; on an idle machine at 16
processes each would likely run faster, so the 16-process figure is an upper bound.
Disk: .olean bytes per leaf from the trial fit's slope, plus the exported sources.
"""
import argparse
import heapq
import json
from pathlib import Path


def lpt(times, p):
    heap = [0.0] * p
    for t in sorted(times, reverse=True):
        x = heapq.heappop(heap)
        heapq.heappush(heap, x + t)
    return max(heap)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fit", type=Path, required=True)
    ap.add_argument("--full", type=Path, required=True)
    ap.add_argument("--root-s", type=float, required=True, help="estimated seconds per Root module")
    ap.add_argument("--final-s", type=float, required=True, help="estimated seconds for E311.Final")
    ap.add_argument("--jobs", type=int, nargs="+", default=[16, 28])
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    fit = json.loads(args.fit.read_text())
    res = {"sides": {}, "parallel": {}}
    times, src_bytes, olean_bytes = [], 0, 0
    for prefix, side in (("E311B", "balanced"), ("E311R", "residual")):
        man = json.loads((args.full / f"manifest-{prefix}.json").read_text())
        f = fit[side]
        t = [f["wall_s"]["a"] + f["wall_s"]["b"] * m["leaves"] for m in man["modules"]]
        u = [f["user_s"]["a"] + f["user_s"]["b"] * m["leaves"] for m in man["modules"]]
        ob = sum(f["olean_bytes"]["a"] + f["olean_bytes"]["b"] * m["leaves"] for m in man["modules"])
        sb = sum(m["source_bytes"] for m in man["modules"])
        times += t
        src_bytes += sb
        olean_bytes += ob
        res["sides"][side] = {
            "modules": len(man["modules"]), "leaves": man["total_leaves"],
            "chunk_leaves": man["chunk_leaves"], "block_leaves": man["block_leaves"],
            "wall_cpu_hours": round(sum(t) / 3600, 2), "user_cpu_hours": round(sum(u) / 3600, 2),
            "largest_module_s": round(max(t), 1), "olean_gb": round(ob / 1e9, 2),
            "source_gb": round(sb / 1e9, 3),
            "peak_rss_gb_fit_at_largest": round(f["peak_rss_gb"]["a"] + f["peak_rss_gb"]["b"]
                                                * max(m["leaves"] for m in man["modules"]), 2)}
    tail = 2 * args.root_s + args.final_s
    res["chunks_cpu_hours"] = round(sum(times) / 3600, 2)
    res["roots_and_final_s"] = tail
    for p in args.jobs:
        w = lpt(times, p)
        res["parallel"][str(p)] = {"chunk_phase_hours": round(w / 3600, 2),
                                   "total_wall_hours": round((w + tail) / 3600, 2)}
    res["disk_gb"] = {"sources": round(src_bytes / 1e9, 2), "oleans": round(olean_bytes / 1e9, 2)}
    out = json.dumps(res, indent=1)
    if args.out:
        args.out.write_text(out + "\n")
    print(out)


if __name__ == "__main__":
    main()
