#!/usr/bin/env python3
"""Decode a SAT model of hm33k7.sub.cnf (orbit-substituted, hull frame) into all X(i,j,k),
check hull units X(1,i,j)=true, mirror identity X(i,j,k)=X(35-k,35-j,35-i) for i>=2, the CNF
itself under the full model, then run sigverify (signotope axioms + convex 7-gon count).
usage: decode.py <SAT.json> <cnf> <out_prefix>"""
import sys, json, itertools, subprocess
N = 33; lo = 2; m = N + lo
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
rep = {}
for (i, j, k), v in idx.items():
    rep[v] = v if i < lo else min(v, idx[tuple(sorted((m - k, m - j, m - i)))])
def decode(model):
    val = {abs(l): l > 0 for l in model}
    return {t: val[rep[v]] for t, v in idx.items()}
if __name__ == "__main__":
    d = json.load(open(sys.argv[1])); model = d["model"] + [l for l in d["cube"]]
    val = {abs(l): l > 0 for l in d["model"]}
    bad_cnf = 0
    for line in open(sys.argv[2]):
        if line[0] in "pc": continue
        c = list(map(int, line.split()[:-1]))
        if not any(val.get(abs(l), False) == (l > 0) for l in c): bad_cnf += 1
    cube_ok = all(val.get(abs(l)) == (l > 0) for l in d["cube"])
    X = decode(d["model"])
    hull_bad = sum(1 for (i, j, k), x in X.items() if i == 1 and not x)
    mir_bad = sum(1 for (i, j, k), x in X.items() if i >= 2 and X[tuple(sorted((m-k, m-j, m-i)))] != x)
    s = f"{N} " + " ".join("1" if X[t] else "0" for t in itertools.combinations(range(1, N + 1), 3))
    open(sys.argv[3] + ".X.txt", "w").write(s + "\n")
    sv = subprocess.run(["/opt/es7/bin/sigverify", "7"], input=s, capture_output=True, text=True).stdout
    rep_ = {"cnf_clauses_violated": bad_cnf, "cube_satisfied": cube_ok, "hull_unit_violations": hull_bad,
            "mirror_violations": mir_bad, "sigverify": sv.strip()}
    print(json.dumps(rep_)); json.dump(rep_, open(sys.argv[3] + ".verify.json", "w"), indent=1)
