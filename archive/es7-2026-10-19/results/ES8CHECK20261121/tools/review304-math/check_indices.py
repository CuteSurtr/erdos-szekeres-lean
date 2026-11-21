import re, json, sys, itertools
E = sys.argv[1]
R = E + "/archive/es7-2026-10-19/results"
src = open(E + "/ErdosSzekeres/Omission/BalancedCatalogData.lean").read()
m = re.search(r"def catalog : List \(List Nat\) := (\[\[.*?\]\])", src, re.S)
cat = json.loads(m.group(1))
print("catalog len", len(cat), "distinct", len(set(map(tuple, cat))))
ok = all(len(f) == 5 and all(0 <= x <= 5 for x in f) and all(f[i] >= f[i+1] for i in range(4)) for f in cat)
print("all antitone in [0,5]^5:", ok)
allF = [f for f in itertools.product(range(6), repeat=5) if all(f[i] >= f[i+1] for i in range(4))]
print("number of antitone maps", len(allF), "catalog == all:", set(map(tuple, cat)) == set(allF))
Z = [i for i, f in enumerate(cat) if f[0] <= 4 and f[4] == 0]
Zs = [i for i, f in enumerate(cat) if f[0] == 5 and f[4] >= 1]
print("|Z|", len(Z), "|Z*|", len(Zs), "disjoint", not set(Z) & set(Zs))
def lean_list(path, name):
    s = open(path).read()
    mm = re.search(name + r" : List ℕ := \[(.*?)\]", s, re.S)
    return [int(x) for x in mm.group(1).replace("\n", " ").split(",")]
zI = lean_list(R + "/ES305N20261119/LemmaZ.lean", "zIndices")
zsI = lean_list(R + "/ES303N20261120/LemmaZStar.lean", "zsIndices")
print("Z == zIndices:", Z == zI, " Z* == zsIndices:", Zs == zsI)
zst = json.load(open(R + "/ES303N20261120/data/zstar.json"))
print("zstar.json == Z*:", zst["zstar"] == Zs, "rhs", zst["rhs"])
rows = json.load(open(R + "/ES303N20261120/data/zzs_rows.json"))
print("zzs_rows[0] support == Z:", rows[0]["support"] == Z, "rhs", rows[0]["rhs"])
print("zzs_rows[1] support == Z*:", rows[1]["support"] == Zs, "rhs", rows[1]["rhs"])
rows54 = json.load(open(R + "/ES303N20261120/data/zzs_rows_n54.json"))
print("n54 rows supports equal, rhs:", rows54[0]["support"] == Z, rows54[1]["support"] == Zs, rows54[0]["rhs"], rows54[1]["rhs"])
print("cat[0], cat[1]:", cat[0], cat[1], "; index of [0,0,0,0,0]:", [i for i,f in enumerate(cat) if f==[0,0,0,0,0]], "index of [1,0,0,0,0]:", [i for i,f in enumerate(cat) if f==[1,0,0,0,0]])
# transpose closure
def transpose(f):
    return tuple(sum(1 for i in range(5) if f[i] >= j+1) for j in range(5))
idx = {tuple(f): i for i, f in enumerate(cat)}
print("Z* transpose-closed:", all(idx[transpose(cat[i])] in Zs for i in Zs), " Z transpose-closed:", all(idx[transpose(cat[i])] in Z for i in Z))
