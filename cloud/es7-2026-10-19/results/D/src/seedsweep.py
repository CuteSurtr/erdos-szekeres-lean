#!/usr/bin/env python3
"""Plateau statistics: sweep every heptagon-free deletion of every seed.

For each 33-point seed with exactly one convex 7-gon (checked with cgon), the
deletions of the 7 heptagon vertices are heptagon-free 32-point sets; each is
normalised (exact power-of-two scaling) and swept with satcount (m capped at
3).  Output: OUTDIR/seedsweep.jsonl, one line per deletion.

usage: seedsweep.py OUTDIR NPROC SEEDFILES...   (int:PATH for "x y" files)
"""
import os, sys, json, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dlib
import walk


def main():
    outdir, nproc = sys.argv[1], int(sys.argv[2])
    seeds = walk.load_seeds(sys.argv[3:])
    tmp = os.path.join(outdir, "tmp_seedsweep")
    os.makedirs(tmp, exist_ok=True)
    seedc = {}
    for lab, P in seeds:
        c = dlib.cgon_count(P, 8)
        seedc[lab] = c
    sig33 = dlib.canon([P for _, P in seeds])
    dels = walk.seed_deletions(seeds)
    sigs = dlib.canon([S for S, _ in dels])

    def job(i):
        S, lab = dels[i]
        p = os.path.join(tmp, f"d{i}.txt"); fp = p + ".faces"
        dlib.write_pts(p, S)
        st = dlib.satcount_sweep(p, 7, fp, 1, 3)
        F = dlib.read_faces(fp)
        m1 = [f for f in F if f["m"] == 1]
        blk = set(tuple(sorted(f["hex"])) for f in m1)
        areas = sorted(f["area"] for f in m1)
        os.unlink(p); os.unlink(fp)
        return {"label": lab, "canonm": walk.h(sigs[i][1]), "m0": st["m0"], "m1": st["m1"], "m2": st["m2"],
                "m3plus": st["m3plus"], "faces": st["faces_euler"], "complete": st["complete"],
                "m1_lattice_ok": sum(1 for f in m1 if f["ok"]), "m1_distinct_blocking_hexagons": len(blk),
                "m1_area_median": areas[len(areas) // 2] if areas else None, "cpu": st["cpu_seconds"]}
    t0 = time.time()
    with ThreadPoolExecutor(nproc) as ex:
        res = list(ex.map(job, range(len(dels))))
    with open(os.path.join(outdir, "seedsweep.jsonl"), "w") as f:
        for r in res:
            f.write(json.dumps(r) + "\n")
    summ = {"seeds": len(seeds), "seeds_with_exactly_one_heptagon": sum(1 for c in seedc.values() if c and c[7] == 1),
            "seed_c7_values": sorted(set((c or {}).get(7, -1) for c in seedc.values())),
            "seed_c8_values": sorted(set((c or {}).get(8, -1) for c in seedc.values())),
            "distinct_seed_order_types": len(set(s[1] for s in sig33)),
            "deletions": len(res), "distinct_deletion_order_types": len(set(r["canonm"] for r in res)),
            "m0_total": sum(r["m0"] for r in res), "all_complete": all(r["complete"] for r in res),
            "wall": round(time.time() - t0, 1), "sweep_cpu": round(sum(r["cpu"] for r in res), 1)}
    json.dump(summ, open(os.path.join(outdir, "seedsweep_summary.json"), "w"), indent=1)
    print(json.dumps(summ))


if __name__ == "__main__":
    main()
