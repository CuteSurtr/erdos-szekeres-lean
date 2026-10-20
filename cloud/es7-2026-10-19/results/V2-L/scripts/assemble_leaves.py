#!/usr/bin/env python3
"""Assemble the leaf lists `leaves (U, L)` of `V2L.CaseCertificates` from the WAVE1 runs, and
report which of the 450 cases are closed.

  assemble_leaves.py RESULTS_DIR OUT_DIR

* A case that Mii-S closed directly (cases.jsonl status UNSAT_VERIFIED, method direct; cake_lpr
  on the case CNF itself) gets the single empty leaf `[]`: `coverCheck [[]] = true` and
  `cubeCnf (cubeCnf F c) [] = cubeCnf F c ++ []`.
* Otherwise the leaves are the union, over every WAVE1/<vm>/<dir> whose name starts with the
  case name (shards included), of the records of leaves.jsonl with status UNSAT and cake_lpr
  "s VERIFIED UNSAT". A record with "direct": true (the case CNF itself refuted, its
  case_sha256 equal to the case's) gives the empty leaf. Every top record of such a dir must carry the case's cnf_sha256.
* A case is closed when its leaves pass a Python port of `Mir.coverCheck` (pre-check only; the
  Lean statement needs `coverCheck` proved in the kernel).
Writes OUT_DIR/status.json and OUT_DIR/leaves/<case>.icnf (cubes in record order)."""
import json, os, re, sys
sys.setrecursionlimit(1000000)
res, out = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(out, "leaves"), exist_ok=True)
cases = [json.loads(l) for l in open(os.path.join(res, "Mii-S/cases.jsonl"))]
w1 = os.path.join(res, "WAVE1")
NAME = re.compile(r"^(U[0-9-]*_L[0-9-]*)(?:[._-].*)?$")
dirs = {}
for vm in sorted(os.listdir(w1)):
    p = os.path.join(w1, vm)
    if not os.path.isdir(p): continue
    for d in sorted(os.listdir(p)):
        m = NAME.match(d)
        if m and os.path.isdir(os.path.join(p, d)):
            dirs.setdefault(m.group(1), []).append(os.path.join(vm, d))

def restrict(z, cubes):
    return [[l for l in c if l != z] for c in cubes if -z not in c]
def cover(cubes):
    while True:
        if any(len(c) == 0 for c in cubes): return True
        if not cubes: return False
        z = cubes[0][0]
        if z == 0 or not cover(restrict(z, cubes)): return False
        cubes = restrict(-z, cubes)

rows = []
for r in cases:
    name, row = r["case"], {"case": r["case"], "U": r["U"], "L": r["L"]}
    if r["status"] == "UNSAT_VERIFIED":
        row.update(source="Mii-S direct", leaves=1, closed=True); leaves = [[]]
    else:
        leaves, bad, other, seen = [], [], {}, set()
        for d in dirs.get(name, []):
            f = os.path.join(w1, d, "leaves.jsonl")
            if not os.path.exists(f): continue
            for line in open(f):
                try: x = json.loads(line)
                except ValueError: other["unparsable"] = other.get("unparsable", 0) + 1; continue
                if x.get("top"):
                    if x.get("case_sha256") != r["cnf_sha256"]: bad.append(d)
                elif x.get("status") == "UNSAT" and x.get("cake_lpr") == "s VERIFIED UNSAT":
                    if x.get("direct"):
                        # the case CNF itself was refuted: the empty leaf
                        if x.get("case_sha256") != r["cnf_sha256"]: bad.append(d); continue
                        x["cube"] = []
                    if "cube" not in x:
                        other["UNSAT without cube"] = other.get("UNSAT without cube", 0) + 1; continue
                    t = tuple(x["cube"])
                    if t not in seen: seen.add(t); leaves.append(x["cube"])
                else:
                    k = str(x.get("status")); other[k] = other.get(k, 0) + 1
        row.update(source=dirs.get(name, []), leaves=len(leaves), other_records=other,
                   sha_mismatch=bad, closed=(not bad) and len(leaves) > 0 and cover(leaves))
    with open(os.path.join(out, "leaves", name + ".icnf"), "w") as f:
        f.writelines("a " + " ".join(map(str, c) ) + (" 0\n" if c else "0\n") for c in leaves)
    rows.append(row)
summary = {"cases": len(rows), "closed": sum(r["closed"] for r in rows),
           "closed_direct": sum(r["source"] == "Mii-S direct" for r in rows),
           "leaves_total": sum(r["leaves"] for r in rows),
           "open": [r["case"] for r in rows if not r["closed"]]}
json.dump({"summary": summary, "rows": rows}, open(os.path.join(out, "status.json"), "w"), indent=1)
print(json.dumps({k: (v if k != "open" else len(v)) for k, v in summary.items()}))
