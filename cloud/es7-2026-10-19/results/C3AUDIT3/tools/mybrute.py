"""brute-force cover check independent of any composer and of split records: every maximal path of the
layer tree (mycompose.layer_children) and every sigma vector in {0,1}^{1..m-1} consistent with it must be
matched by a certified leaf L__C (L a prefix of the path, sigma agrees with C; plain L = empty C).
usage: mybrute.py m k RECORDS.jsonl [...]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mycompose as Y
m, k = int(sys.argv[1]), int(sys.argv[2])
leaves = {}
for f in sys.argv[3:]:
    for l in open(f):
        r = json.loads(l)
        if r.get("certified") is True and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
            L, C = Y.parse(r["node"])
            if "cube" in r: C = tuple(sorted((int(a), b) for a, b in r["cube"].items()))
            leaves.setdefault(Y.key(L, ())[0], []).append(dict(C))
holes, walked = [], [0]
def dfs(P, U):
    if P:
        U = [s for s in U if not any(all(s[r] == v for r, v in C.items()) for C in leaves.get(P, []))]
    if not U: return
    ch = Y.layer_children(m, k, P)
    if not ch: holes.append((Y.kname((P, ())), len(U))); return
    for c in ch:
        walked[0] += 1
        dfs(Y.key(c, ())[0], [s for s in U if all(sg is None or r == 0 or s[r] == sg for r, sg in c[-1])])
import itertools
ALL = [(0,) + v for v in itertools.product((0, 1), repeat=m - 1)]
dfs((), ALL)
print(json.dumps({"leaves": sum(map(len, leaves.values())), "edges_walked": walked[0], "holes": len(holes), "sample": holes[:3]}))
