#!/usr/bin/env python3
"""Work list of the C2P wave: the second-layer subcases of the parallelogram cases P1..P8 of the central 34-point
formula (results/C2C34).

- cubes/P<a>_cubes.txt is the output of `results/C2C34/l2cubes.py MAP.json a` (560 subcases per case; P8 is identical
  to results/C2C34/p8/P8_cubes.txt).
- Orbits: the relabelling i -> (a - i) mod 17 (reflect the configuration, then restart the angular normal form at the
  other hull class) maps subcase (P_a, V) to (P_a, V'). It is the argument of results/C2C34 §6 for P8, applied to
  every P_a; orbits/P<a>.tsv lists subcase and representative (the lexicographically least member).
- The list: for a = 8, 7, ..., 1, the cover P<a>_cover (except P8, certified in results/C2C34), then the orbit
  representatives, quadrilateral second layers interleaved with hexagonal ones (shuffled with a fixed seed). For P8 it
  leaves out the 64 representatives certified in results/C2C34 and the 3 that need a deeper split there.
- Caps: cover 3600 s, quadrilateral second layer (Q) 2400 s, hexagonal (H) 1800 s.
usage: mklist.py C2P_DIR results/C2C34/logs/p8_units.tsv"""
import json, random, sys
D, p8res = sys.argv[1], sys.argv[2]
T = 17
done8 = set()
for l in open(p8res):                                    # results/C2C34/logs/p8_units.tsv (or the raw .jsonl)
    if not l.strip() or l.startswith("unit\t"): continue
    done8.add(json.loads(l)["unit"] if l.startswith("{") else l.split("\t")[0])   # 65 certified (incl. the cover), 3 timeouts
key = lambda s: tuple(int(x) for x in s.split("_")[1].split("-"))
rows = []
for a in range(8, 0, -1):
    names = [l.split()[0] for l in open(f"{D}/cubes/P{a}_cubes.txt") if l.strip()]
    S = set(names); assert len(S) == 560
    def img(n):
        V = [int(x) for x in n.split("_")[1].split("-")]
        return f"P{a}_" + "-".join(map(str, sorted((a - i) % T for i in V)))
    rep = {}
    for n in names:
        m = img(n); assert m in S and img(m) == n
        rep[n] = min(n, m, key=key)
    with open(f"{D}/orbits/P{a}.tsv", "w") as f:
        f.write("subcase\trepresentative\n" + "".join(f"{n}\t{rep[n]}\n" for n in sorted(names, key=key)))
    reps = sorted(set(rep.values()), key=key)
    rnd = random.Random(a)
    q = [n for n in reps if n.count("-") == 1]; h = [n for n in reps if n.count("-") == 2]
    rnd.shuffle(q); rnd.shuffle(h)
    order, k = [], 0
    while q or h:
        if q and (not h or k % 5 == 0): order.append(q.pop())
        else: order.append(h.pop())
        k += 1
    if a != 8:
        rows.append((f"P{a}_cover", f"P{a}", "cover", 3600))
    for n in order:
        if n in done8: continue
        kind = "Q" if n.count("-") == 1 else "H"
        rows.append((n, f"P{a}", kind, 2400 if kind == "Q" else 1800))
    fixed = sum(1 for n in names if rep[n] == n and img(n) == n)
    print(f"P{a}: subcases 560, orbits {len(reps)} ({sum(1 for n in reps if n.count('-') == 1)} Q), fixed {fixed}")
with open(f"{D}/lists/C2P.tsv", "w") as f:
    f.write("idx\tunit\tcase\tkind\tcap_s\n")
    for i, r in enumerate(rows): f.write(f"{i}\t" + "\t".join(map(str, r)) + "\n")
print("units", len(rows), {k: sum(1 for r in rows if r[2] == k) for k in ("cover", "Q", "H")})
