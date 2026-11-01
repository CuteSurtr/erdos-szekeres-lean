#!/usr/bin/env python3
"""Fix the base variables of a C3a CNF (chi', sigma bits, inv) to the values of a decoded C3b
model and ask CaDiCaL whether the rest extends (C3a's T/B/chain variables are functions of
these).  usage: c3b_model_in_c3a.py c3b_decoded.json c3a.cnf c3a_map.json"""
import json, subprocess, sys
d = json.load(open(sys.argv[1])); mp = json.load(open(sys.argv[3]))
chiP = {tuple(map(int, k.split(","))): v for k, v in d["chiP"].items()}
inv = {tuple(map(int, k.split(","))): v for k, v in d["inv"].items()}
s = d["s"]; m = d["m"]
units = set()
for a, b, c, l in mp["C"]:
    units.add(l if chiP[a, b, c] > 0 else -l)
for r, v in enumerate(mp["s"]):
    units.add(v if s[r] else -v)
for a, b, v in mp["inv"]:
    units.add(v if inv[a, b] else -v)
assert not any(-u in units for u in units)
lines = open(sys.argv[2]).read().split("\n")
h = [i for i, l in enumerate(lines) if l.startswith("p cnf")][0]
nv, nc = map(int, lines[h].split()[2:4])
lines[h] = f"p cnf {nv} {nc + len(units)}"
txt = "\n".join(lines).rstrip("\n") + "\n" + "".join(f"{u} 0\n" for u in sorted(units))
r = subprocess.run(["/tmp/claude-0/build/cadical/build/cadical", "-q"], input=txt, capture_output=True, text=True)
st = [l for l in r.stdout.splitlines() if l.startswith("s ")]
print(json.dumps({"model": sys.argv[1].split("/")[-1], "units": len(units), "c3a_status": st[0][2:] if st else "?"}))
