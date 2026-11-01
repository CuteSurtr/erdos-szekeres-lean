#!/usr/bin/env python3
"""Independent recount for a case P_a (not using C2P/orbits or tools/summary.py): the 560 second-layer subcases are read
from the names in C2P/cubes/P<a>_cubes.txt; the reflection pairs V with V' = {(a - i) mod 17 : i in V}; every resulting
orbit needs a member certified by both checkers in some record (pilot C2C34/logs/p8_units.tsv, or any C2P*/M*/ and
C2P*/LOCAL*/ out.jsonl), and the cover P<a>_cover must be certified. usage: check_case.py RESULTS_DIR a"""
import glob, json, sys
R, A = sys.argv[1], int(sys.argv[2])
subs = [l.split()[0] for l in open(f"{R}/C2P/cubes/P{A}_cubes.txt") if l.strip()]
assert len(subs) == len(set(subs)) == 560, len(subs)
def cls(name): return frozenset(int(x) for x in name.split("_")[1].split("-"))
def name(V): return f"P{A}_" + "-".join(map(str, sorted(V)))
byset = {cls(s): s for s in subs}
assert all(name(V) == s for V, s in byset.items())
cert = set()
for l in list(open(f"{R}/C2C34/logs/p8_units.tsv"))[1:]:
    f = l.rstrip("\n").split("\t")
    if f[9] == "c VERIFIED" and f[11] == "s VERIFIED UNSAT": cert.add(f[0])
for p in glob.glob(f"{R}/C2P*/M*/out.jsonl") + glob.glob(f"{R}/C2P*/LOCAL*/out.jsonl"):
    for l in open(p):
        if l.strip():
            r = json.loads(l)
            if r.get("certified") is True and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
                cert.add(r["unit"])
orbits, seen = [], set()
for V, s in byset.items():
    if V in seen: continue
    W = frozenset((A - i) % 17 for i in V)
    assert W in byset, (s, sorted(W))
    seen |= {V, W}; orbits.append((s, byset[W]))
fixed = sum(1 for a, b in orbits if a == b)
open_ = [(a, b) for a, b in orbits if a not in cert and b not in cert]
print(f"subcases 560, orbits {len(orbits)} ({fixed} fixed), cover certified: {f'P{A}_cover' in cert}, "
      f"orbits without a certified member: {len(open_)} {open_[:10]}")
