#!/usr/bin/env python3
"""Plug a decoded C3a model (chi' on sorted triples, sigma per point, inv) into the C3b CNF and
evaluate it with cnfeval (aux least model).  The model satisfies the C3b CNF iff the output is
"0 0 ...".  usage: eval_foreign.py c3a_model.json c3b.cnf c3b.json"""
import json, subprocess, sys
d = json.load(open(sys.argv[1])); mp = json.load(open(sys.argv[3]))
n, m = mp["n"], mp["m"]
chip = {(a, b, c): s for a, b, c, s in d["chi_prime"]}
sg = d["sigma"]; inv = {(i, j): v for i, j, v in d["inv"]}
assert len(sg) == n and len(chip) == n * (n - 1) * (n - 2) // 6
val, bad = {}, 0
def setv(v, b):
    global bad
    if v in val and val[v] != b: bad += 1
    val[v] = b
for a, b, c, v, s in mp["X"]: setv(v, chip[a, b, c] * s > 0)
for a, b, c, v, s in mp["Y"]: setv(v, chip[a, b, c] * (-1) ** (sg[a] + sg[b] + sg[c]) * s > 0)
for r, v in enumerate(mp["s"]): setv(v, sg[r] == 1)
for i in range(n):
    if sg[i] != sg[i % m] ^ (1 if i // m == 1 else 0): bad += 1
for i, j, v in mp["I"]: setv(v, inv[i, j] == 1)
for i, j, v in mp["O"]: setv(v, (inv[i, j] ^ sg[i] ^ sg[j]) == 1)
p = subprocess.run(["/tmp/claude-0/build/cnfeval", sys.argv[2], str(mp["primary_vars"]), str(mp["nonkgon_clauses"])],
                   input=" ".join(str(v if b else -v) for v, b in sorted(val.items())) + "\n", capture_output=True, text=True)
f1, f2, aux = map(int, p.stdout.split())
print(json.dumps({"model": sys.argv[1].split("/")[-1], "orbit_conflicts": bad, "nonkgon_falsified": f1, "kgon_falsified": f2,
                  "satisfies_c3b": bad == 0 and f1 == 0 and f2 == 0}))
