#!/usr/bin/env python3
"""Check brute_a7 (C) against an independent Python count (Andrew hull) of convex k-subsets on random sets."""
import os, random, struct, subprocess, sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a7lib as L

rng = random.Random(777)
fails = 0
for t in range(30):
    fmt = ["Z2", "EIS", "Z5"][t % 3]
    n = rng.randint(9, 14)
    while True:
        if fmt == "Z5":
            pts = [tuple(rng.randint(-8, 8) for _ in range(4)) for _ in range(n)]
        else:
            pts = [(rng.randint(-200, 200), rng.randint(-200, 200)) for _ in range(n)]
        if len(set(pts)) == n and all(L.orient_A(a, b, c, fmt) for a, b, c in combinations(pts, 3)):
            break
    O = L.orient_table(pts, fmt)
    binp = os.path.join(HERE, "tmp_test.orient.bin")
    with open(binp, "wb") as f:
        f.write(struct.pack("<i", n))
        f.write(bytes((O[i][j][k] & 0xFF) for i in range(n) for j in range(n) for k in range(n)))
    k = rng.randint(5, 7)
    out = subprocess.run([os.path.join(HERE, "brute_a7"), binp, str(k)], capture_output=True, text=True).stdout
    cmpf = L.lex_key_cmp(fmt)
    cross = lambda o, a, b: L.orient_A(o, a, b, fmt)
    cnt = {kk: sum(1 for c in combinations(pts, kk) if L.hull_is_convex_position(list(c), cmpf, cross)) for kk in (k, k - 1)}
    got = {}
    for line in out.splitlines()[1:]:
        d = dict(kv.split("=") for kv in line.split() if "=" in kv)
        if "k" in d:
            got[int(d["k"])] = (int(d["convex_TRI"]), int(d["convex_WRAP"]))
    ok = all(got[kk] == (cnt[kk], cnt[kk]) for kk in (k, k - 1))
    if not ok:
        fails += 1
    print(fmt, n, k, "python", cnt, "C", got, "OK" if ok else "MISMATCH")
os.remove(binp)
print("fails=%d" % fails)
