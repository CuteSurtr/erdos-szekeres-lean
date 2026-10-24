#!/usr/bin/env python3
"""3e: decode a c3cnf model and check it by brute force, independently of the clauses.
Checks: chi' (all triples) satisfies the signotope axiom on every 4-set; chi'(Ri,Rj,Rk) =
chi'(ijk) eps eps eps; sigma has the (s, not s, s) orbit pattern and sigma_0 = 0; the inversion
bits give a total order consistent with the prefix rule; chi_S = chi' (-1)^sigma is
R-invariant; convk finds no convex k-set in chi_S.  Writes the decoded model as JSON.
usage: decode.py MAP.json SOLVER_OUTPUT OUT.json"""
import itertools
import json
import subprocess
import sys

CONVK = "/opt/s/convk"


def parity_sort(t):
    a, b, c = t
    inv = (a > b) + (a > c) + (b > c)
    return tuple(sorted(t)), (-1 if inv & 1 else 1)


def main():
    mp = json.load(open(sys.argv[1]))
    val = {}
    for line in open(sys.argv[2]):
        if line.startswith("v "):
            for x in line.split()[1:]:
                x = int(x)
                if x:
                    val[abs(x)] = x > 0
    n, m, k = mp["n"], mp["m"], mp["k"]
    lit = lambda l: val[abs(l)] if l > 0 else not val[abs(l)]
    chip = {(a, b, c): (1 if lit(l) else -1) for a, b, c, l in mp["C"]}
    s = [val[v] for v in mp["s"]]
    sigma = [int(s[i % m]) ^ (1 if i // m == 1 else 0) for i in range(n)]
    inv = {(a, b): int(val[v]) for a, b, v in mp["inv"]}
    chiT = {(a, b, c): (1 if lit(l) else -1) for a, b, c, l in mp["T"]}
    rep = {"m": m, "k": k, "n": n}
    # signotope axiom
    bad4 = 0
    for q in itertools.combinations(range(n), 4):
        seq = [chip[t] for t in itertools.combinations(q, 3)]
        changes = sum(seq[i] != seq[i + 1] for i in range(3))
        bad4 += changes > 1
    rep["signotope_violations"] = bad4
    R = [(i - m) % n for i in range(n)]
    eps = [1 if i < m else -1 for i in range(n)]
    o = lambda tab, t: (lambda st: st[1] * tab[st[0]])(parity_sort(t))
    rep["symmetry_violations"] = sum(o(chip, tuple(R[i] for i in t)) != chip[t] * eps[t[0]] * eps[t[1]] * eps[t[2]] for t in chip)
    chiS = {t: c * (-1) ** (sigma[t[0]] + sigma[t[1]] + sigma[t[2]]) for t, c in chip.items()}
    rep["chiS_vs_T_mismatch"] = sum(chiS[t] != chiT[t] for t in chiS)
    rep["chiS_rotation_violations"] = sum(o(chiS, tuple(R[i] for i in t)) != chiS[t] for t in chiS)
    rep["sigma0"] = sigma[0]
    # inversion bits: transitive, prefix rule, forced bits
    badinv = 0
    for i, j, l in itertools.combinations(range(n), 3):
        pat = (inv[(i, j)], inv[(i, l)], inv[(j, l)])
        ok = {(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)} if chip[(i, j, l)] > 0 else {(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1)}
        badinv += pat not in ok
    for i, j in itertools.combinations(range(n), 2):
        if sigma[i] != sigma[j]:
            badinv += inv[(i, j)] != (1 if sigma[i] == 0 else 0)
    rep["inv_violations"] = badinv
    # S x-order from the model: before(i,j) = inv ^ sigma_i ^ sigma_j; check it is a total order
    bef = {}
    for (i, j), b in inv.items():
        bef[(i, j)] = b ^ sigma[i] ^ sigma[j]
        bef[(j, i)] = 1 - bef[(i, j)]
    order = sorted(range(n), key=lambda i: sum(bef[(j, i)] for j in range(n) if j != i))
    rep["xorder_total"] = all(bef[(order[a], order[b])] for a in range(n) for b in range(a + 1, n))
    # brute force convex k-set in chi_S
    inp = f"{n} {k}\n" + " ".join(str(chiS[t]) for t in itertools.combinations(range(n), 3))
    out = subprocess.run([CONVK], input=inp, capture_output=True, text=True, check=True).stdout.split()
    rep["convex_k_set"] = out[0] == "gon"
    largest = 3
    for kk in range(4, n + 1):
        inp = f"{n} {kk}\n" + " ".join(str(chiS[t]) for t in itertools.combinations(range(n), 3))
        if subprocess.run([CONVK], input=inp, capture_output=True, text=True, check=True).stdout.split()[0] != "gon":
            break
        largest = kk
    rep["largest_convex"] = largest
    rep["ok"] = (bad4 == 0 and rep["symmetry_violations"] == 0 and rep["chiS_vs_T_mismatch"] == 0
                 and rep["chiS_rotation_violations"] == 0 and sigma[0] == 0 and badinv == 0
                 and rep["xorder_total"] and not rep["convex_k_set"])
    json.dump({"report": rep, "chi_prime": [[*t, c] for t, c in sorted(chip.items())], "sigma": sigma,
               "inv": [[*p, b] for p, b in sorted(inv.items())], "xorder": order}, open(sys.argv[3], "w"))
    print(json.dumps(rep))


if __name__ == "__main__":
    main()
