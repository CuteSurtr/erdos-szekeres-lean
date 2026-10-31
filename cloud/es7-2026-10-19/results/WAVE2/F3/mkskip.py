#!/usr/bin/env python3
"""F1 step b: write the skip file (cubes of SHARE already closed elsewhere).
  mkskip.py CASE_SHA SHARE.icnf OUT_skip.icnf SRC_leaves.jsonl...
A cube X counts as closed if (1) some source records X, or a subset of X, as UNSAT with
cake_lpr == 's VERIFIED UNSAT', or (2) some source records X as SPLIT with subs and every
child X+s is closed (recursively). Sources whose case_sha256 differs from CASE_SHA are refused.
SKIP records are never used. Lines of SHARE must be well-formed ('a ... 0')."""
import json, sys, os
VER = "s VERIFIED UNSAT"
sha, share, out, srcs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
ver, split = set(), {}
for s in srcs:
    if not os.path.exists(s): continue
    shas = set()
    rs = []
    for l in open(s):
        if not l.endswith("\n"): break  # partial last line
        try: rs.append(json.loads(l))
        except Exception: continue
    for r in rs:
        if "case_sha256" in r: shas.add(r["case_sha256"])
    if shas != {sha}: print("REFUSED (case sha)", s, shas, file=sys.stderr); continue
    nv = 0
    for r in rs:
        if "cube" not in r: continue
        c = tuple(r["cube"])
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == VER: ver.add(frozenset(c)); nv += 1
        elif r.get("status") == "SPLIT" and r.get("subs") is not None and r.get("nsub", len(r["subs"])) == len(r["subs"]):
            split[c] = [c + tuple(x) for x in r["subs"]]
    print(f"{s}: {nv} verified", file=sys.stderr)
verl = list(ver); memo = {}
def closed(c, depth=0):
    if c in memo: return memo[c]
    fc = frozenset(c); res = fc in ver or any(v <= fc for v in verl)
    if not res and c in split and depth < 50:
        subs = split[c]
        res = len(subs) > 0 and all(tuple(x) != c and closed(tuple(x), depth + 1) for x in subs)
    memo[c] = res; return res
cubes = []
for l in open(share):
    if not l.startswith("a "): continue
    assert l.endswith(" 0\n"), l
    cubes.append(tuple(map(int, l.split()[1:-1])))
sk = [c for c in cubes if closed(c)]
tmp = out + ".tmp"
with open(tmp, "w") as f:
    for c in sk: f.write("a " + " ".join(map(str, c)) + " 0\n")
os.replace(tmp, out)
print(f"share {len(cubes)} skip {len(sk)}", file=sys.stderr)
