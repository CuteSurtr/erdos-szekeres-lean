#!/usr/bin/env python3
"""F7: write the --skip file: cubes of U_L8 closed elsewhere.
A cube C counts as closed if a verified leaf L (cake_lpr "s VERIFIED UNSAT") of W30 or another
WAVE2 helper satisfies set(L) <= set(C), or C was split by them and every child is closed.
  mkskip.py QUEUE.icnf OUT.icnf  (QUEUE: candidate cubes; children of own splits are added)"""
import glob, json, os, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # results/
dirs = [os.path.join(R, "WAVE1/W30/U_L8")] + [d for d in glob.glob(os.path.join(R, "WAVE2/*/U_L8")) if "/F7/" not in d]
leaves, split = set(), {}
for d in dirs:
    p = os.path.join(d, "leaves.jsonl")
    if not os.path.exists(p): continue
    for l in open(p):
        try: r = json.loads(l)
        except ValueError: continue   # partial last line
        if "cube" not in r: continue
        c = tuple(r["cube"])
        if r.get("status") == "UNSAT" and r.get("cake_lpr") == "s VERIFIED UNSAT": leaves.add(frozenset(c))
        elif r.get("status") == "SPLIT" and "subs" in r: split.setdefault(c, r["subs"])
bylit = {}
for L in leaves:
    for x in L: bylit.setdefault(x, []).append(L)
memo = {}
def closed(c):
    if c in memo: return memo[c]
    s = frozenset(c); ok = frozenset() in leaves or any(L <= s for x in c for L in bylit.get(x, ()))
    if not ok and c in split: ok = all(closed(c + tuple(t)) for t in split[c])
    memo[c] = ok; return ok
q = [tuple(map(int, l.split()[1:-1])) for l in open(sys.argv[1]) if l.startswith("a ") and l.endswith(" 0\n")]
own = os.path.join(R, "WAVE2/F7/U_L8/leaves.jsonl")   # also test children of our own splits
if os.path.exists(own):
    for l in open(own):
        try: r = json.loads(l)
        except ValueError: continue
        if r.get("status") == "SPLIT" and "subs" in r: q += [tuple(r["cube"]) + tuple(t) for t in r["subs"]]
out = sorted(set(c for c in q if closed(c)))
tmp = sys.argv[2] + ".tmp"
with open(tmp, "w") as f:
    for c in out: f.write("a " + " ".join(map(str, c)) + " 0\n")
os.replace(tmp, sys.argv[2])
print(len(leaves), "leaves from", len(dirs), "dirs;", len(out), "of", len(q), "queued cubes closed elsewhere")
