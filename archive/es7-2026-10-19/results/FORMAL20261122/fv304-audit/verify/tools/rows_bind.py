#!/usr/bin/env python3
"""rv4 own binding check of the Res118 hypotheses' literal data against the six slice row files.
Sources: Res118/Rows.lean and Res118/LemmaA.lean (the audit's copies, = res118 README §7), and optionally the rows
and index lists decoded from the kernel terms by src/RV.lean (lines RV-ROW / RV-NATLIST of logs/rv.log).
Usage: rows_bind.py OUT.json [rv.log]"""
import hashlib, json, re, sys

A = "/home/jay/research/data/formalize-20261122/fv304-audit/src/Res118"
REPO = "/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results"
IN = "/home/jay/research/data/es308-20261114/inputs"
SLICES = [  # (name, file, sha256 prefix from res118 README §4, B, T, blocks)
    ("b33s18", f"{REPO}/LO33N20261113/data/cert_66_55_leanrows/extra_66_55_leanrows.json", "1d6141afc91e3a4a", 33, 18, []),
    ("s18-v13", f"{IN}/s18-v13/extra.json", "1b72eb934e00c7f5", 34, 18, ["P", "Q"]),
    ("s19", f"{IN}/s19/extra.json", "770d276db7b51d36", 34, 19, ["P"]),
    ("b35s18-v13", f"{IN}/b35s18-v13/extra.json", "c9c922c0a113c78e", 35, 18, ["P", "Q"]),
    ("b35s19-v16", f"{IN}/b35s19-v16/extra.json", "1257c4a15a52d894", 35, 19, ["P", "Q", "U"]),
    ("b35s20-v169", f"{IN}/b35s20-v169/extra.json", "de4bcceba6d0c80c", 35, 20, ["P", "Q", "A"]),
]


def lean_defs(text):
    """name -> right-hand side text of every top-level `def name : T := rhs`."""
    out = {}
    text = re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", text, flags=re.S))  # drop Lean comments
    for m in re.finditer(r"^def (\w+) : [^\n]*?:=(.*?)(?=^def |^theorem |^end |\Z)", text, re.S | re.M):
        out[m.group(1)] = m.group(2).strip()
    return out


def lit(rhs):
    return json.loads(re.sub(r"--[^\n]*", "", rhs))


rows_src = open(f"{A}/Rows.lean").read()
defs = lean_defs(rows_src)
blocks = {}
for b in "PQUA":
    parts = [p.strip() for p in defs[f"rows{b}"].split("++")]
    assert all(re.fullmatch(rf"rows{b}_\d\d", p) for p in parts), parts
    blocks[b] = [r for p in parts for r in lit(defs[p])]
la = lean_defs(open(f"{A}/LemmaA.lean").read())
F, LO = lit(la["fIndices"]), lit(la["loIndices"])

problems = []
def need(cond, msg):
    if not cond:
        problems.append(msg)

need((len(blocks["P"]), len(blocks["Q"]), len(blocks["U"]), len(blocks["A"])) == (812, 208, 35, 970), "block sizes")
need(len(F) == 84 and len(LO) == 70 and sorted(F + LO) == list(range(154)), "F/Lo do not partition the 154 states")
for b, rs in blocks.items():
    for i, r in enumerate(rs):
        need(len(r) > 0, f"{b}[{i}] empty")
        need(all(0 <= x < 154 for x in r), f"{b}[{i}] state out of range")
        need(len(set(r)) == len(r), f"{b}[{i}] repeated state")
        need(not set(r) <= {0, 1}, f"{b}[{i}] only states 0/1 (always occupied for n >= 2)")
slices = {}
for name, path, pre, B, T, bl in SLICES:
    raw = open(path, "rb").read()
    h = hashlib.sha256(raw).hexdigest()
    d = json.loads(raw)
    exp = [r for b in bl for r in blocks[b]]
    ok_hash = h.startswith(pre)
    ok_cap = d[0] == {"support": sorted(F), "rhs": T} and d[1] == {"support": sorted(LO), "rhs": B - T}
    ok_rows = [x["support"] for x in d[2:]] == exp and all(x["rhs"] == 1 for x in d[2:])
    ok_sets = [sorted(x["support"]) for x in d[2:]] == [sorted(r) for r in exp]
    slices[name] = {"sha256": h, "hash_ok": ok_hash, "capacity_ok": ok_cap, "unit_rows": len(d) - 2,
                    "rows_equal_in_order": ok_rows, "rows_equal_as_sets": ok_sets, "B": B, "T": T, "blocks": bl}
    need(ok_hash and ok_cap and ok_rows, f"slice {name} binding")
# self-test: the in-order comparison must reject a one-entry mutation, a dropped row and a swap
d19 = json.load(open(SLICES[2][1]))
got = [x["support"] for x in d19[2:]]
assert got == blocks["P"]
assert got != [blocks["P"][0] + [153]] + blocks["P"][1:]
assert got != blocks["P"][1:]
assert got != [blocks["P"][1], blocks["P"][0]] + blocks["P"][2:]
distinct = {tuple(sorted(r)) for b in "PQUA" for r in blocks[b]}
res = {"blocks": {b: len(v) for b, v in blocks.items()}, "distinct_rows": len(distinct),
       "U_and_A_common": len({tuple(sorted(r)) for r in blocks["U"]} & {tuple(sorted(r)) for r in blocks["A"]}),
       "slices": slices}
if len(sys.argv) > 2:  # kernel-decoded data from the RV compile
    kern = {b: [] for b in "PQUA"}
    nat = {}
    for line in open(sys.argv[2], errors="replace"):
        m = re.match(r"RV-ROW Res118\.rows([PQUA]) (\[.*\])\s*$", line)
        if m:
            kern[m.group(1)].append(json.loads(m.group(2)))
        m = re.match(r"RV-NATLIST Res118\.(\w+) (\d+) (\[.*\])\s*$", line)
        if m:
            nat[m.group(1)] = json.loads(m.group(3))
    res["kernel"] = {b: {"rows": len(kern[b]), "equal_source": kern[b] == blocks[b]} for b in "PQUA"}
    res["kernel"]["fIndices_equal"] = nat.get("fIndices") == F
    res["kernel"]["loIndices_equal"] = nat.get("loIndices") == LO
    need(all(res["kernel"][b]["equal_source"] for b in "PQUA"), "kernel rows differ from Rows.lean")
    need(res["kernel"]["fIndices_equal"] and res["kernel"]["loIndices_equal"], "kernel F/Lo lists differ")
res["problems"] = problems
res["ok"] = not problems
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "slices"}, indent=1))
for k, v in slices.items():
    print(k, {x: v[x] for x in ("hash_ok", "capacity_ok", "rows_equal_in_order", "unit_rows")})
