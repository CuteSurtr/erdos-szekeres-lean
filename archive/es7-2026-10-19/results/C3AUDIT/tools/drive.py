import sys, random, json, subprocess, os, collections
sys.path.insert(0, "/opt/audit/ind")
from indep import *
import indep as _I; truth = _I.truth
m, nsets, seed, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]   # mode: geo | sat | satnogon
k = 7
KENC = int(mode.split(":")[1]) if mode.startswith("satk") else 7
rng = random.Random(seed)
E = C3Enc(m, KENC)
basefile = None
if mode in ("sat", "satnogon") or mode.startswith("satk"):
    E.build()
    cls = E.clauses
    if mode == "satnogon":
        g = [s for s in E.sections if s[0] == "gon"][0]
        assert g[1] + g[2] == len(cls)
        cls = cls[:g[1]]
    basefile = f"/opt/audit/ind/base_{m}_{mode.replace(':','')}.body"
    with open(basefile, "w") as f:
        for c in cls: f.write(" ".join(map(str, c)) + " 0\n")
    NC = len(cls)
stats = collections.Counter(); fails = []
scales = [3, 10, 30, 100, 300, 1000, 3000, 10000]
tried = 0
while stats["sets"] < nsets and tried < 200000:
    tried += 1
    S = gen(m, rng, rng.sample(scales, rng.randint(2, 6)))
    if not general(S): continue
    Ls = layers(S)
    if any(len(L) > 6 for L in Ls): stats["bighull_skip"] += 1; continue
    inclass = None
    if mode == "sat":
        if has_kgon(S, k): stats["kgon_skip"] += 1; continue
        inclass = True
    if mode.startswith("satk"):
        if maxconv(S) >= KENC: stats["kgon_skip"] += 1; continue
        inclass = True
    stats["sets"] += 1
    found_tree = []
    for which, T in (("S", S), ("M", [Mref(p) for p in S])):
        for d in frames(T):
            name, lab, sig, order = node_of(T, d, m)
            if name is None: continue
            assert name != "BIG"
            stats["valid_frames"] += 1
            ok, bad = in_tree(m, k, name, None)
            if not ok:
                # only allowed reason: H3 and layer 2 not mirror-kept
                if not (name.split("_")[0] == "0s0" and bad.count("_") == 1):
                    fails.append(("not in tree", which, name, bad))
                stats["pruned_frames"] += 1
                continue
            val = truth(E, lab, sig, order, m)
            us = [c[0] for c in HC.layer_clauses(m, HC.parse_layers(name), E.ccw, E.sig)]
            if not all(lit_true(val, u) for u in us): fails.append(("unit false", which, name))
            if not lit_true(val, -E.sig(0)): fails.append(("sb false", which, name))
            found_tree.append((which, name, val, us))
    if not found_tree: fails.append(("UNCOVERED", S)); continue
    if not any(w == "S" for w, *_ in found_tree): stats["covered_only_via_mirror"] += 1
    stats["covered"] += 1
    stats["top_" + found_tree[0][1].split("_")[0]] += 1
    stats["depth_%d" % (found_tree[0][1].count("_") + 1)] += 1
    if basefile:
        which, name, val, us = found_tree[rng.randrange(len(found_tree))]
        fix = [v if b else -v for v, b in val.items()]
        cnf = f"/opt/audit/ind/t_{m}_{seed}.cnf"
        with open(cnf, "w") as f:
            f.write(f"p cnf {E.nv} {NC + len(us) + len(fix)}\n")
            f.write(open(basefile).read())
            for u in us + fix: f.write(f"{u} 0\n")
        o = subprocess.run(["/opt/build/cadical/build/cadical", "-q", "-n", cnf], capture_output=True, text=True).stdout
        st = next((l[2:] for l in o.splitlines() if l.startswith("s ")), "UNKNOWN")
        stats["sat_" + st] += 1
        if st != "SATISFIABLE": fails.append(("CNF not satisfied by true config", which, name, st))
        os.remove(cnf)
print(json.dumps({"m": m, "mode": mode, "seed": seed, "tried": tried, "stats": stats, "fails": fails[:20], "nfails": len(fails)}))
