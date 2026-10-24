#!/usr/bin/env python3
"""Geometric face sweep for 32-point sets whose coordinates exceed sat.c's 2^27 bound: re-realize the
exact chirotope with the validated realizer (results/F; seeds 6600000+k), accept only an exact
re-check (chiro.verify_exact) with |coord| < 2^27, then run tools/trackA/sat.c on that realization
(same labelled order type, so the same saturation answer).  Sets already below 2^27 go straight to sat.c.
usage: geom_fill.py SATC OUT.jsonl budget seeds a.pts|sets32.jsonl ...   (jsonl: uses points_exact)"""
import sys, os, json, subprocess, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../F/realizer"))
import chiro, realize as R
satc, outp, budget, seeds = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
def items():
    for f in sys.argv[5:]:
        if f.endswith(".jsonl"):
            for l in open(f):
                r = json.loads(l); yield f"{os.path.basename(f)}:{r['id']}", [tuple(p) for p in (r["points_exact"] if "points_exact" in r else r["points"])]
        else:
            yield os.path.basename(f), [tuple(map(int, l.split())) for l in open(f) if l.strip()]
out = open(outp, "a")
for name, P in items():
    chi = chiro.chirotope_of(P); res = {"set": name, "N": len(P)}
    Q = P if max(max(abs(x), abs(y)) for x, y in P) < 2 ** 27 else None
    if Q is None:
        for k in range(seeds):
            rr = R.realize(chi, len(P), budget=budget, seed=6600000 + k)
            if rr["realized"]:
                C = [tuple(p) for p in rr["points"]]
                if chiro.verify_exact(C, chi)[0] and max(max(abs(x), abs(y)) for x, y in C) < 2 ** 27:
                    Q = C; res["recompressed_seed"] = 6600000 + k; break
    if Q is None:
        res["geom"] = "not run: no exact realization below 2^27 found"
    else:
        res["points_used"] = [list(p) for p in Q]
        with tempfile.TemporaryDirectory() as td:
            pf = os.path.join(td, "p.txt"); bf = os.path.join(td, "bad.txt")
            open(pf, "w").write("".join(f"{x} {y}\n" for x, y in Q))
            r = subprocess.run([satc, "sat", pf, "7", bf], capture_output=True, text=True)
            js = [l for l in r.stdout.splitlines() if l.startswith("{")]
            g = json.loads(js[-1]) if js else {"error": (r.stdout + r.stderr)[-300:]}
            res["geom"] = g
            if js:
                res["geom_saturated"] = g["bad_candidates"] == 0 and g["faces_euler"] == g["faces_hit_by_valid_candidates"]
                if g["bad_candidates"]: res["bad_head"] = open(bf).read()[:3000]
    out.write(json.dumps(res) + "\n"); out.flush()
    print(json.dumps({k: v for k, v in res.items() if k != "points_used"}), flush=True)
