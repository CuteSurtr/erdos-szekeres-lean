import json, re, sys
E = sys.argv[1]
J = json.load(open(E + "/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json"))
print("keys", sorted(J.keys()))
src = open(E + "/ErdosSzekeres/Omission/BalancedCatalogData.lean").read()
cat = json.loads(re.search(r"def catalog : List \(List Nat\) := (\[\[.*?\]\])", src, re.S).group(1))
st = J["states"]
print("json states == Lean catalog (same order):", [list(s) for s in st] == cat)
Zj = [i for i, f in enumerate(st) if f[0] <= 4 and f[4] == 0]
Zsj = [i for i, f in enumerate(st) if f[0] == 5 and f[4] >= 1]
R = E + "/archive/es7-2026-10-19/results/ES303N20261120/data/zzs_rows.json"
rows = json.load(open(R))
print("json Z == zzs Z-row support:", Zj == rows[0]["support"], " json Z* == zzs Z*-row support:", Zsj == rows[1]["support"])
cons = J["constraints"]; print("constraints", len(cons), "first keys", sorted(cons[0].keys()))
cut = open(E + "/experiments/omission-cover-certificates-2026-10-10/BalancedCoverCutsV2.lean").read()
sup = {int(k): sorted(int(x) for x in v.split(',')) for k, v in re.findall(r'^def support(\d+) : Finset \(Fin 252\) := \{([0-9, ]*)\}', cut, re.M)}
dem = [int(x) for x in re.search(r'^def demand : Fin 446 → ℕ := !\[([0-9, ]*)\]', cut, re.M).group(1).split(',')]
print("cuts parsed", len(sup), len(dem))
bad = [k for k in range(446) if sorted(cons[2685 + k]["support"]) != sup[k] or cons[2685 + k]["rhs"] != dem[k]]
print("cut mismatches vs JSON rows 2685..3130:", len(bad), bad[:5])
dups = sum(1 for c in cons if len(set(c["support"])) != len(c["support"]))
print("constraints with duplicate support entries:", dups, "; states in range:", all(0 <= i < 252 for c in cons for i in c["support"]))
# does any catalog row contain state 0 or 1 (relevant to fixed-state trees)?
print("rows containing state 0:", sum(0 in c["support"] for c in cons), " rows containing state 1:", sum(1 in c["support"] for c in cons))
