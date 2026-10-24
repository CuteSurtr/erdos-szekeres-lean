#!/usr/bin/env python3
"""LRAT-check and Baek-Balko cross-check of closed leaf cubes of the real instances.

No cube of the breadth-first runs closed, so the LRAT lane of cnc2.py was never triggered on
them. The Knuth probes do end in closed cubes; this re-solves each such leaf from scratch as
CNF + unit clauses with `cadical --lrat`, checks the proof with lrat-check, and re-solves the
same cube on the Baek-Balko CNF (+ the same lex-leader) without proof.
usage: lrat_leaves.py CACHE_DIR OUT.jsonl [max_per_instance]"""
import json, subprocess, sys, time
from pathlib import Path

C = Path(sys.argv[1]).resolve(); outp = Path(sys.argv[2]); mx = int(sys.argv[3]) if len(sys.argv) > 3 else 4
cad = str(C / "ext/cadical/build/cadical"); chk = str(C / "ext/drat-trim/lrat-check")
done = set()
if outp.exists():
    done = {(r["instance"], tuple(r["cube"])) for r in map(json.loads, open(outp))}


def with_units(cnf, cube, dst):
    with open(cnf) as f:
        h = f.readline().split(); body = f.read()
    with open(dst, "w") as g:
        g.write(f"p cnf {h[2]} {int(h[3]) + len(cube)}\n"); g.write(body)
        for l in cube:
            g.write(f"{l} 0\n")


log = open(outp, "a")
for tag in ("k7a5u6N26", "k7a5u7N27"):
    probes = [json.loads(l) for p in sorted((C / "knuth").glob(f"{tag}_s*.jsonl")) for l in open(p)]
    leaves = [p["cube"] for p in probes if p["end"] == "closed"][:mx]
    for cube in leaves:
        if (tag, tuple(cube)) in done:
            continue
        rec = {"instance": tag, "depth": len(cube), "cube": cube}
        tmp = C / "lratleaf.cnf"; prf = C / "lratleaf.lrat"
        with_units(C / "inst" / f"{tag}_lexx.cnf", cube, tmp)
        t = time.time(); r = subprocess.run([cad, "-q", "-n", "--lrat=true", "--binary=false", "-t", "3600", str(tmp), str(prf)])
        rec["solve_rc"] = r.returncode; rec["solve_wall_s"] = round(time.time() - t, 1)
        if r.returncode == 20:
            rec["proof_MB"] = round(prf.stat().st_size / 1e6, 1)
            t = time.time(); pc = subprocess.run([chk, str(tmp), str(prf)], capture_output=True, text=True)
            rec["check_wall_s"] = round(time.time() - t, 1)
            rec["lrat"] = "VERIFIED" if any(l.strip() == "c VERIFIED" for l in pc.stdout.splitlines()) else "FAILED"
        prf.unlink(missing_ok=True)
        with_units(C / "inst" / f"{tag}_bb_lexx.cnf", cube, tmp)
        t = time.time(); r = subprocess.run([cad, "-q", "-n", "-t", "3600", str(tmp)])
        rec["bb_rc"] = r.returncode; rec["bb_wall_s"] = round(time.time() - t, 1)
        tmp.unlink(missing_ok=True)
        log.write(json.dumps(rec) + "\n"); log.flush(); print(json.dumps(rec), flush=True)
