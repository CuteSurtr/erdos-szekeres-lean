#!/usr/bin/env python3
"""Table of all CaDiCaL runs: instance sizes (from cnf/*.json or *.json.info) and outcomes (runs/summary.txt)."""
import glob, json, os, re
sizes = {}
for p in glob.glob("cnf/*.json") + glob.glob("cnf/*.json.info"):
    try: d = json.load(open(p))
    except Exception: continue
    tag = os.path.basename(p).replace(".json.info", "").replace(".json", "")
    sizes[tag] = d
rows = []
for line in open("runs/summary.txt"):
    m = re.match(r"(\S+) exit=(\d+) s (\w+) wall=(\d+)s real ([\d.]+) user ([\d.]+)\s+args=\[(.*)\]", line.strip())
    if not m: continue
    out, ec, st, wall, real, user, args = m.groups()
    inst = re.sub(r"_(sat|seed\d)$", "", out)
    d = sizes.get(inst, {})
    rows.append((out, d.get("N"), d.get("K"), d.get("m"), d.get("center"), d.get("X_vars"), d.get("vars"), d.get("clauses"), st, float(real), args))
print(f"{'run':20s} {'N':>3} {'K':>2} {'m':>2} {'centre':6s} {'X-vars':>6} {'vars':>7} {'clauses':>9}  {'result':13s} {'sec':>8}  args")
for r in rows:
    print(f"{r[0]:20s} {r[1]:3} {r[2]:2} {r[3]:2} {str(r[4]):6s} {r[5]:6} {r[6]:7} {r[7]:9}  {r[8]:13s} {r[9]:8.2f}  {r[10]}")
