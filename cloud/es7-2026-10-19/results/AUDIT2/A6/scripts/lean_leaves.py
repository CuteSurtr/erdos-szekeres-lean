"""Decode V2-L/V2L/Trees/*.lean (Table + T<k>) into per-case leaf lists, as CTree.leaves orders them.
usage: lean_leaves.py V2L_DIR CASES_JSONL OUT_JSON"""
import json, re, sys, os
V, CJ, OUT = sys.argv[1:4]
cases = [json.loads(l) for l in open(CJ) if l.strip()]
ul2case = {(tuple(c["U"]), tuple(c["L"])): c["case"] for c in cases}
tab = open(os.path.join(V, "Trees", "Table.lean")).read()
body = tab[tab.index("def treeTable"):]
ents = re.findall(r"\(\(\[([0-9, ]*)\], \[([0-9, ]*)\]\), (Trees\.tree(\d{3})|\.leaf|\.node \[\])\)", body)
assert len(ents) == 450, len(ents)
def nl(s): return tuple(int(x) for x in s.split(",") if x.strip())
def dec(d): return d // 2 if d % 2 == 0 else -(d // 2)
def unpack(k, n):
    out = []
    for _ in range(k): out.append(dec(n % (1 << 20))); n >>= 20
    assert n == 0, "extra digits"
    return out[::-1]
res, seen = {}, set()
for u, l, t, k in ents:
    case = ul2case[(nl(u), nl(l))]
    assert case not in seen; seen.add(case)
    if t == ".leaf": res[case] = {"tree": "leaf", "leaves": [[]]}; continue
    assert t != ".node []", case
    src = open(os.path.join(V, "Trees", "T%s.lean" % k)).read()
    hdr = re.search(r"Cube tree of case (\S+) \(U = \[([0-9, ]*)\], L = \[([0-9, ]*)\]\)", src)
    assert hdr.group(1) == case and nl(hdr.group(2)) == nl(u) and nl(hdr.group(3)) == nl(l), (case, hdr.groups())
    assert ("def tree%s : CTree := .node n%s_0" % (k, k)) in src
    defs = {}
    for m in re.finditer(r"def n%s_(\d+) : List \(List Int × CTree\) := \[(.*)\]\n" % k, src):
        items = re.findall(r"(lf|nd) (\d+) (0x[0-9a-f]+|0)(?: n%s_(\d+))?" % k, m.group(2))
        defs[int(m.group(1))] = [(a, unpack(int(b), int(c, 16)), int(d) if d else None) for a, b, c, d in items]
        # sanity: number of items equals number of commas+1 at top level
        assert len(items) == m.group(2).count("lf ") + m.group(2).count("nd "), case
    def leaves(j):
        out = []
        for kind, cube, sub in defs[j]:
            if kind == "lf": assert sub is None; out.append(cube)
            else: out += [cube + x for x in leaves(sub)]
        return out
    lv = leaves(0)
    res[case] = {"tree": "node", "k": k, "leaves": lv, "nlists": len(defs)}
json.dump(res, open(OUT, "w"))
print("cases", len(res), "node", sum(r["tree"] == "node" for r in res.values()), "leaves", sum(len(r["leaves"]) for r in res.values()))
