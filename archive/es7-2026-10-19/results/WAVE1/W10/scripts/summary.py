#!/usr/bin/env python3
"""Shard summary and cover check for W10.

  summary.py DIR SHARD NSHARDS
Reads DIR/top.icnf, DIR/leaves.jsonl, DIR/leaves.icnf, DIR/open.icnf.  Writes DIR/cover_input.icnf
= (top cubes of the other shards) + leaves.icnf + optional extra, and runs Mii-S covercheck.py on
it: `s COVERED` means the cake_lpr-verified leaves cover this shard's part of the case.  Also checks
top.icnf alone, and leaves.icnf + open.icnf + other shards (must always cover).
"""
import json, os, subprocess, sys
d, s, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
CC = os.path.join(os.path.dirname(__file__), "../../../Mii-S/scripts/covercheck.py")
top = [l for l in open(os.path.join(d, "top.icnf")) if l.startswith("a")]
other = [l for i, l in enumerate(top) if i % k != s]
def cc(lines, name):
    p = os.path.join("/home/user/work", name); open(p, "w").writelines(lines)
    return subprocess.run(["python3", CC, p], capture_output=True, text=True).stdout.strip()
leaves = [l for l in open(os.path.join(d, "leaves.icnf"))]
opn = [l for l in open(os.path.join(d, "open.icnf"))]
recs = [json.loads(l) for l in open(os.path.join(d, "leaves.jsonl"))]
st = {}
for r in recs:
    if "cube" in r: st[r["status"]] = st.get(r["status"], 0) + 1
ver = sum(1 for r in recs if r.get("cake_lpr") == "s VERIFIED UNSAT")
cpu = sum(r.get("solve_s", 0) + r.get("check_s", 0) + r.get("split_s", 0) for r in recs)
out = {"records": st, "verified_leaves": ver, "leaves_icnf": len(leaves), "open": len(opn),
       "cpu_core_h": round(cpu / 3600, 2),
       "top_alone": cc(top, "cc_top.icnf"),
       "shard_by_verified_leaves": cc(other + leaves, "cc_shard.icnf"),
       "shard_by_leaves_plus_open": cc(other + leaves + opn, "cc_all.icnf")}
print(json.dumps(out, indent=1))
