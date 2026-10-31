# Extract sub-case (i) leaf cubes (original decision order) and verify they form a complete binary partition.
import json, sys, hashlib
D = sys.argv[1]
leaves = {}
def is_unsat(o):
    return str(o.get("status", "")).upper() in ("UNSAT", "UNSATISFIABLE")
for t in ["Mi-0", "Mi-1", "Mi-2", "Mi-3"]:
    n = 0
    for line in open(f"{D}/{t}.leaves.jsonl"):
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if "cube" not in o or not is_unsat(o) or o.get("kind") in ("residual", "gap"):
            continue
        if "VERIFIED" not in str(o.get("lrat", o.get("lrat_check", ""))):
            sys.exit(f"{t}: unverified UNSAT leaf")
        cube = tuple(o["cube"])
        leaves.setdefault(frozenset(cube), cube); n += 1
    print(f"{t}: {n} UNSAT leaf records", flush=True)
cubes = list(leaves.values())
print("distinct leaves:", len(cubes), "| depths:", {d: sum(1 for c in cubes if len(c) == d) for d in sorted({len(c) for c in cubes})}, flush=True)

# trie check: every internal node must have exactly two children, x and -x; leaves terminal
root = {}
for c in cubes:
    node = root
    for lit in c:
        node = node.setdefault(lit, {})
    if node:
        sys.exit(f"leaf {c} is a prefix of another leaf")
    node["#leaf"] = True
bad = []
def check(node, path):
    if node.get("#leaf"):
        if len(node) != 1:
            bad.append(("leaf with children", path))
        return 1
    keys = [k for k in node if k != "#leaf"]
    if len(keys) != 2 or keys[0] != -keys[1]:
        bad.append(("incomplete split", path, keys[:4]))
        return 0
    return sum(check(node[k], path + (k,)) for k in keys)
import sys as _s
_s.setrecursionlimit(10000)
nleaf = check(root, ())
print("trie leaves:", nleaf, "| problems:", len(bad), bad[:3], flush=True)
# weight check: sum of 2^-depth must be exactly 1 for a complete partition
from fractions import Fraction
w = sum(Fraction(1, 2 ** len(c)) for c in cubes)
print("sum of 2^-depth over leaves:", w, flush=True)
order = sorted(cubes, key=lambda c: (len(c), c))
out = "".join("a " + " ".join(map(str, c)) + " 0\n" for c in order)
open(f"{D}/hull_leaves.icnf", "w").write(out)
print("hull_leaves.icnf sha256:", hashlib.sha256(out.encode()).hexdigest(), "lines:", out.count("\n"), flush=True)
