#!/usr/bin/env python3
"""LRAT-check every closed cube of a cnc2.py run that its LRAT lane did not reach.
Each cube is re-solved from scratch as CNF + unit clauses with `cadical --lrat`, the proof is
checked with lrat-check, and the same cube is re-solved on the cross-check CNF (no proof).
Results are appended to RUN/lrat.jsonl in the cnc2.py format.
usage: lrat_rest.py RUN_DIR CNF XCHECK_CNF CADICAL LRATCHECK [max]"""
import json, subprocess, sys, time
from pathlib import Path

run, cnf, xcnf, cad, chk = Path(sys.argv[1]), *sys.argv[2:6]
mx = int(sys.argv[6]) if len(sys.argv) > 6 else 10**9
done = {tuple(json.loads(l)["cube"]) for l in open(run / "lrat.jsonl")}
closed = [json.loads(l) for l in open(run / "events.jsonl")]
closed = [e for e in closed if e["r"] == "U" and tuple(e["cube"]) not in done][:mx]


def units(src, cube, dst):
    with open(src) as f:
        h = f.readline().split(); body = f.read()
    with open(dst, "w") as g:
        g.write(f"p cnf {h[2]} {int(h[3]) + len(cube)}\n"); g.write(body)
        for l in cube:
            g.write(f"{l} 0\n")


log = open(run / "lrat.jsonl", "a")
for e in closed:
    cube = e["cube"]; rec = {"id": e["id"], "d": len(cube), "cube": cube, "lane": "lrat_rest"}
    tmp, prf = run / "rest.cnf", run / "rest.lrat"
    units(cnf, cube, tmp)
    t = time.time(); r = subprocess.run([cad, "-q", "-n", "--lrat=true", "--binary=false", "-t", "1800", str(tmp), str(prf)])
    rec["solve_rc"] = r.returncode; rec["solve_s"] = round(time.time() - t, 2)
    if r.returncode == 20:
        rec["proof_bytes"] = prf.stat().st_size
        t = time.time(); pc = subprocess.run([chk, str(tmp), str(prf)], capture_output=True, text=True)
        rec["check_s"] = round(time.time() - t, 2)
        rec["lrat"] = "VERIFIED" if any(l.strip() == "c VERIFIED" for l in pc.stdout.splitlines()) else "FAILED"
    else:
        rec["lrat"] = f"rc{r.returncode}"
    prf.unlink(missing_ok=True)
    units(xcnf, cube, tmp)
    t = time.time(); r = subprocess.run([cad, "-q", "-n", "-t", "1800", str(tmp)])
    rec["xcheck_rc"] = r.returncode; rec["xcheck_s"] = round(time.time() - t, 2)
    tmp.unlink(missing_ok=True)
    log.write(json.dumps(rec) + "\n"); log.flush(); print(json.dumps(rec), flush=True)
