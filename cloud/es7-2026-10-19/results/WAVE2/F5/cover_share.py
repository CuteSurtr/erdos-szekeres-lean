import json, subprocess, sys, os
D = sys.argv[1]
def cubes(p):
    out = []
    for l in open(p):
        assert l.startswith("a ") and l.endswith(" 0\n"), l
        out.append(tuple(map(int, l.split()[1:-1])))
    return out
share = cubes(D + "/share.icnf"); leaves = cubes(D + "/leaves.icnf")
drop = [tuple(json.loads(l)["cube"]) for l in open(D + "/dropped.jsonl")]
recs = [json.loads(l) for l in open(D + "/leaves.jsonl")]
ver = {tuple(r["cube"]) for r in recs if r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT"}
assert set(leaves) == ver and len(leaves) == len(set(leaves))
print("records", len(recs), "statuses", {s: sum(r.get("status") == s for r in recs) for s in ("UNSAT","SPLIT","SAT","UNSAT_UNCHECKED","TIMEOUT")})
bad = 0; pool = leaves + drop
for S in share:
    cl = [[l] for l in S] + [[-l for l in L] for L in pool if all(x in set(L) for x in S) or all(x in set(S) for x in L)]
    nv = max(abs(l) for c in cl for l in c)
    txt = f"p cnf {nv} {len(cl)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in cl)
    rc = subprocess.run(["/opt/work/bin/cadical", "-q"], input=txt, text=True, capture_output=True).returncode
    if rc != 20: bad += 1; print("NOT COVERED", S)
print("share", len(share), "leaves", len(leaves), "dropped", len(drop), "uncovered", bad)
