#!/usr/bin/env python3
"""LBS2 L5: 32-point subsets of the 33-point near-misses (1 to 3 convex 7-gons) of
results/LBS/L1, L2, L3: list the convex 7-gons with vfy7 -l, drop each point of a remaining
7-gon, keep the subsets with c7 = 0 by vfy7. Writes candidate JSONL for pipeline.py.
usage: nearmiss.py LBSDIR VFYBIN OUT.jsonl"""
import glob, json, os, subprocess, sys, tempfile

def sets_from(lbs):
    # L1: snap/s*.best.txt: "# c7 .." header then "x y" lines
    for f in sorted(glob.glob(f"{lbs}/L1/snap/*.best.txt")):
        pts = [tuple(map(int, l.split()[:2])) for l in open(f) if l.strip() and not l.startswith("#")]
        yield f"L1/{os.path.basename(f)}", pts
    # L3: *_near.txt / *_best.txt / *_bestsym.txt: blocks "# ..." + 33 lines "a b u v" (use u v)
    for f in sorted(glob.glob(f"{lbs}/L3/runs/*_near.txt") + glob.glob(f"{lbs}/L3/runs/*_best*.txt")):
        blk, k, hdr = [], 0, None
        for l in list(open(f)) + ["# end"]:
            if l.startswith("#"):
                if len(blk) == 33:
                    yield f"L3/{os.path.basename(f)}#{k}", blk
                    k += 1
                if not l.startswith("# columns"):
                    blk = []
                continue
            w = l.split()
            if len(w) >= 4:
                blk.append((int(w[2]), int(w[3])))
    # L2: best.txt and out/*.best.txt ("x y" lines), out/*.sets (one set per line "x,y" tokens)
    for f in [f"{lbs}/L2/best.txt"] + sorted(glob.glob(f"{lbs}/L2/out/*.best.txt")):
        pts = [tuple(map(int, l.split()[:2])) for l in open(f) if l.strip() and not l.startswith("#")]
        if len(pts) == 33:
            yield f"L2/{os.path.relpath(f, lbs + '/L2')}", pts
    for f in sorted(glob.glob(f"{lbs}/L2/out/*.sets")):
        for i, l in enumerate(open(f)):
            pts = [tuple(map(int, t.split(","))) for t in l.split() if "," in t]
            if len(pts) == 33:
                yield f"L2/{os.path.basename(f)}#{i}", pts

def vfy(vfyb, pts, lst=False):
    with tempfile.NamedTemporaryFile("w", suffix=".pts", delete=False) as t:
        t.write("".join(f"{x} {y}\n" for x, y in pts))
    r = subprocess.run([vfyb, t.name] + (["-l"] if lst else []), capture_output=True, text=True).stdout
    os.unlink(t.name)
    gons = [list(map(int, l.split()[1:])) for l in r.splitlines() if l.startswith("C7")]
    w = [l for l in r.splitlines() if l.startswith("gp")][0].split()
    return dict(zip(w[0::2], w[1::2])), gons

def main():
    lbs, vfyb, outp = sys.argv[1:4]
    seen_sets = set(); n33 = n32 = 0
    with open(outp, "w") as out:
        for src, pts in sets_from(lbs):
            key = tuple(sorted(pts))
            if key in seen_sets:
                continue
            seen_sets.add(key)
            d, gons = vfy(vfyb, pts, True)
            if d.get("gp") != "1" or not (1 <= int(d["c7"]) <= 3):
                continue
            n33 += 1
            cand = sorted(set(i for g in gons for i in g))
            for i in cand:
                if all(i in g for g in gons):  # dropping i kills every 7-gon
                    sub = pts[:i] + pts[i + 1:]
                    d2, _ = vfy(vfyb, sub)
                    if d2.get("gp") == "1" and d2["c7"] == "0":
                        out.write(json.dumps({"id": f"near:{src}:drop{i}", "gen": "nearmiss-drop", "seed": f"{src} c7={d['c7']} drop {i}", "pts": sub}) + "\n")
                        n32 += 1
    print(f"33-point near-misses with 1..3 convex 7-gons: {n33}; 32-point subsets with c7 = 0: {n32}")

if __name__ == "__main__":
    main()
