"""Independent cut check (own tree definition) over certified records; compares with hullcase.tree_children.
C3H6M: copy of results/C3AUDIT/tools/mycompose.py with the H6M reduction added (own code, not C3T's):
  --h6m        children of each H6(a, s) node "0s0-<a>s<s>" reduced to the layer-2 options O with
               key(O) <= key(phi(O)), phi(r, sg) = ((a - r) mod 11, sg ^ [r < a] ^ [s = 0]).
  --dump P     write P.frontier (uncovered frontier nodes) and P.d2 (depth-2 roots: name, covered,
               has_certified_at_or_below).
usage: mycompose.py [--h6m] [--dump P] RESULTS.jsonl [...]"""
import json, sys, glob, itertools, functools
H6M = "--h6m" in sys.argv
DUMP = sys.argv[sys.argv.index("--dump") + 1] if "--dump" in sys.argv else None
FILES = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] != "--dump"]
sys.path.insert(0, "/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3-S/tools")
M = 11
def opts(unused):
    o = [f"{r}" for r in unused]
    for b, c in itertools.combinations(sorted(unused), 2):
        for sb in (0, 1):
            for sc in (0, 1): o.append(f"{b}s{sb}-{c}s{sc}")
    return o
def toks(lay):
    return sorted((int(t.split("s")[0]), int(t.split("s")[1]) if "s" in t else -1) for t in lay.split("-"))
def mirror(lay):
    return sorted(((M - r) % M, (1 - s) if s >= 0 else -1) for r, s in toks(lay))
def phi6(a, s, lay):
    return sorted(((a - r) % M, -1 if g < 0 else g ^ (r < a) ^ (s == 0)) for r, g in toks(lay))
def children(name):
    if name == "":
        return ["0s0"] + [f"0s0-{a}s{s}" for a in range(1, 6) for s in (0, 1)]
    lays = name.split("_")
    used = {r for l in lays for r, _ in toks(l)}
    o = opts([r for r in range(M) if r not in used])
    if name == "0s0": o = [x for x in o if toks(x) <= mirror(x)]
    if H6M and len(lays) == 1 and name != "0s0":
        (_, _), (a, s) = toks(lays[0])
        o = [x for x in o if toks(x) <= phi6(a, s, x)]
    return [name + "_" + x for x in o]
def norm(name):  # canonical order of residues inside a layer
    out = []
    for l in name.split("_"):
        t = toks(l); out.append("-".join(f"{r}" if s < 0 else f"{r}s{s}" for r, s in t))
    return "_".join(out)
cert = set(); nrec = 0; dup = 0
for f in FILES:
    for l in open(f):
        r = json.loads(l)
        if r.get("certified") and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
            nrec += 1; n = norm(r["node"]); dup += n in cert; cert.add(n)
prefixes = {"_".join(c.split("_")[:j]) for c in cert for j in range(1, c.count("_") + 1)}
missing = []
@functools.lru_cache(None)
def cov(name):
    if name in cert: return True
    if name and name not in prefixes: missing.append(name); return False
    return all([cov(c) for c in children(name)])
ok = cov("")
# compare own tree with hullcase on every prefix node
import hullcase as HC
mism = 0
for p in ([] if H6M else sorted(prefixes | {""})):
    a = sorted(children(p))
    b = sorted(HC.layers_name(c) for c in HC.tree_children(11, 7, HC.parse_layers(p) if p else [], mirror=True))
    mism += a != b
d2 = [c for t in children("") for c in children(t)]
_m = len(missing)
d2open = [c for c in d2 if not cov(c)]
del missing[_m:]
if DUMP:
    open(DUMP + ".frontier", "w").write("".join(x + "\n" for x in sorted(missing)))
    open(DUMP + ".d2", "w").write("".join(f"{c}\t{int(cov(c))}\t{int(c in cert or c in prefixes)}\n" for c in d2))
print(json.dumps({"h6m": H6M, "depth2_roots": len(d2), "depth2_open": len(d2open), "records": nrec, "distinct_certified": len(cert), "duplicates": dup, "class_covered": ok,
                  "uncovered_frontier": len(missing), "prefix_nodes_compared": len(prefixes) + 1, "children_mismatch": mism,
                  "not_in_tree": sum(1 for c in cert if c.rsplit("_",1)[-1] and c not in set(children(c.rsplit("_",1)[0] if "_" in c else "")))}))
