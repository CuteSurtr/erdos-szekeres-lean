#!/usr/bin/env python3
"""Convert a decoded C3a model (decode.py JSON) to the realizer's .sig convention:
point 3*o + r = R^r q_o (R = +120 degrees), centre last (index n).  Label r < m is q_r,
R(label) = label - m mod n.  chi(c, i, j) = (-1)^(sigma_i + sigma_j) for labels i < j.
usage: to_sig.py MODEL.json OUT.sig"""
import itertools, json, sys
d = json.load(open(sys.argv[1]))
n = d["report"]["n"]; m = n // 3
sigma = d["sigma"]
chiS = {}
for a, b, c, s in d["chi_prime"]:
    chiS[(a, b, c)] = s * (-1) ** (sigma[a] + sigma[b] + sigma[c])
for i, j in itertools.combinations(range(n), 2):
    chiS[(i, j, n)] = (-1) ** (sigma[i] + sigma[j])  # chi(i, j, c) = chi(c, i, j)
lab2idx = {}
for o in range(m):
    lab = o
    for r in range(3):
        lab2idx[lab] = 3 * o + r
        lab = (lab - m) % n
lab2idx[n] = n
def par(t):
    a, b, c = t
    return -1 if ((a > b) + (a > c) + (b > c)) & 1 else 1
with open(sys.argv[2], "w") as f:
    out = {}
    for t, s in chiS.items():
        u = tuple(lab2idx[x] for x in t)
        out[tuple(sorted(u))] = s * par(u)
    for t in sorted(out):
        f.write(f"{t[0]} {t[1]} {t[2]} {out[t]}\n")
print("chi(0,1,2) =", out[(0, 1, 2)], " (+1 = counter-clockwise R)")
