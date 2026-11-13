#!/usr/bin/env python3
"""Check that every leaf of the case trees is a leaf of the acceptance manifest for its case.

  crosscheck_trees.py RESULTS_DIR TREES_OUT MANIFEST.jsonl

TREES_OUT is the OUTDIR of gen_trees.py (status.json, leaves/<case>.icnf). The manifest stores
each leaf's literals sorted by (abs, sign) (v3_manifest.py), so a tree leaf (a literal sequence,
as recorded) is compared with the manifest's lits after the same sort; gen_trees.py already
checked that no tree has a repeated leaf. Cases with tree `leaf` have the single empty leaf: a
Mii-S direct case must be UNSAT_VERIFIED in cases.jsonl; a wave empty-cube case is compared with
the manifest's empty leaf if the manifest has one, otherwise with the wave records gen_trees.py
found (listed in status.json). Exit status 1 if some tree leaf is not in the manifest."""
import json, os, sys
res, tout, man = sys.argv[1:4]
st = json.load(open(os.path.join(tout, "status.json")))
cases = {c["case"]: c for c in (json.loads(l) for l in open(os.path.join(res, "Mii-S/cases.jsonl")) if l.strip())}
M = {}
for l in open(man):
    x = json.loads(l)
    M.setdefault(x["case"], set()).add(json.dumps(x["lits"]))
def key(c): return json.dumps(sorted(c, key=lambda z: (abs(z), z)))
tot_t = tot_m = extra_m = missing = 0
bad = []
print("k case tree tree_leaves manifest_leaves manifest_not_in_tree tree_not_in_manifest how")
for r in st["rows"]:
    n = r["case"]; m = M.get(n, set())
    if r["tree"] == "leaf":
        T = {key([])}
        if r["source"] == "Mii-S direct":
            ok = cases[n]["status"] == "UNSAT_VERIFIED"; how = "Mii-S UNSAT_VERIFIED"
        elif key([]) in m:
            ok = True; how = "manifest empty leaf"
        else:
            ok = bool(r.get("whole_dirs")); how = "wave empty-cube record " + ",".join(r.get("whole_dirs", []))
        nm = 0 if ok else 1
    elif r["tree"] == "node":
        T = [key(list(map(int, line.split()[1:-1]))) for line in open(os.path.join(tout, "leaves", n + ".icnf"))]
        assert len(T) == r["leaves"]
        T = set(T); assert len(T) == r["leaves"]
        nm = len(T - m); how = "manifest"
        if nm: bad.append((n, sorted(T - m)[:20]))
    else:
        print("OPEN CASE", n); missing += 1; continue
    em = len(m - T)
    tot_t += len(T); tot_m += len(m); extra_m += em; missing += nm
    print(r["k"], n, r["tree"], len(T), len(m), em, nm, how)
print(f"TOTAL tree_leaves {tot_t} manifest_leaves {tot_m} manifest_not_in_tree {extra_m} tree_not_in_manifest {missing}")
for b in bad: print("NOT IN MANIFEST", b)
sys.exit(1 if missing else 0)
