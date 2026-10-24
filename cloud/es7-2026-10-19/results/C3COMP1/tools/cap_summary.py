#!/usr/bin/env python3
"""C3COMP1 cap experiment: one row per cube of cap_cubes.tsv from the lane records (out_lane*.jsonl).
usage: cap_summary.py cap_cubes.tsv open_roots.tsv OUT.tsv out_lane*.jsonl"""
import json, sys
cubes = [l.rstrip("\n").split("\t") for l in open(sys.argv[1])][1:]
strat = {l.split("\t")[0]: l.split("\t")[1] for l in open(sys.argv[2])}
rec = {}
for f in sys.argv[4:]:
    for l in open(f):
        r = json.loads(l)
        if "status" in r:
            rec[r["node"]] = r
rows = []
for i, lane, c, R, d in cubes:
    r = rec.get(c)
    st = "not run" if r is None else ("certified" if r.get("certified") else r["status"])
    rows.append((i, lane, c, R, strat.get(R, "?"), d, st, r and r["solve_s"], r and r.get("check_s"), r and r.get("proof_bytes"),
                 r and r.get("lrat_check"), r and r.get("cake_lpr")))
with open(sys.argv[3], "w") as f:
    f.write("i\tlane\tcube\troot\tstratum\tC3W4_dir\tstatus\tsolve_s\tcheck_s\tproof_bytes\tlrat_check\tcake_lpr\n")
    f.writelines("\t".join("" if x is None else str(x) for x in row) + "\n" for row in rows)
for grp, sel in (("H3/one", lambda s: s == "H3/one"), ("other", lambda s: s != "H3/one")):
    o = [x for x in rows if sel(x[4]) and x[6] != "not run"]
    ce = [x for x in o if x[6] == "certified"]
    print(f"{grp}: run {len(o)}, certified {len(ce)}, timed out {sum(1 for x in o if x[6] == 'UNKNOWN')}; "
          f"certified solve_s {sorted(x[7] for x in ce)}; check_s {sorted(x[8] for x in ce)}")
print(f"roots: {len({x[3] for x in rows if x[6] != 'not run'})}; not run: {sum(1 for x in rows if x[6] == 'not run')}")
