#!/usr/bin/env python3
"""summarize.py OUTDIR TOP.icnf: write OUTDIR/leaves.icnf (cake_lpr-verified leaves),
OUTDIR/open.icnf (cubes of this shard not closed: queued, timed out at the deadline or with an
unverified proof) and OUTDIR/summary.json (counts, CPU seconds, per-top-cube cover check with the
logic of results/Mii-S/scripts/covercheck.py applied to the leaves below each top cube)."""
import json, sys
sys.setrecursionlimit(100000)
out, topf = sys.argv[1], sys.argv[2]
R = [json.loads(l) for l in open(f"{out}/leaves.jsonl")]
T = R[0] if R and R[0].get("top") else next(r for r in R if r.get("top"))
top = [tuple(map(int, l.split()[1:-1])) for l in open(topf) if l.startswith("a")]
mine = [c for i, c in enumerate(top) if i % T["nshards"] == T["shard"]]
ok = lambda r: r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"
leaves = [tuple(r["cube"]) for r in R if "cube" in r and ok(r)]
final = set(leaves) | {tuple(r["cube"]) for r in R if r.get("status") in ("SPLIT", "SAT")}
want = list(mine) + [tuple(r["cube"]) + tuple(s) for r in R if r.get("status") == "SPLIT" for s in r["subs"]]
openc = sorted({c for c in want if c not in final}, key=lambda c: (len(c), c))
with open(f"{out}/leaves.icnf", "w") as f:
    for c in sorted(set(leaves), key=lambda c: (len(c), c)): f.write("a " + " ".join(map(str, c)) + " 0\n")
with open(f"{out}/open.icnf", "w") as f:
    for c in openc: f.write("a " + " ".join(map(str, c)) + " 0\n")
def restrict(z, cubes): return [[l for l in c if l != z] for c in cubes if -z not in c]
def cover(cubes):
    if any(len(c) == 0 for c in cubes): return True
    if not cubes: return False
    z = cubes[0][0]
    return z != 0 and cover(restrict(z, cubes)) and cover(restrict(-z, cubes))
closed_top = 0
for t in mine:
    below = [list(c[len(t):]) for c in leaves if c[:len(t)] == t]
    closed_top += cover(below)
cpu = sum(r.get(k, 0) for r in R for k in ("solve_s", "check_s", "split_s"))
S = {"ncubes_top": T["ncubes"], "top_sha256": T["top_sha256"], "shard": T["shard"], "nshards": T["nshards"],
     "nmine": len(mine), "top_cubes_covered": closed_top, "verified_leaves": len(set(leaves)),
     "splits": sum(r.get("status") == "SPLIT" for r in R), "open": len(openc),
     "unverified_unsat": sum(r.get("status") == "UNSAT" and not ok(r) for r in R),
     "sat": sum(r.get("status") == "SAT" for r in R), "cpu_s": round(cpu, 1),
     "shard_closed": closed_top == len(mine) and not openc}
json.dump(S, open(f"{out}/summary.json", "w"), indent=1); print(json.dumps(S))
