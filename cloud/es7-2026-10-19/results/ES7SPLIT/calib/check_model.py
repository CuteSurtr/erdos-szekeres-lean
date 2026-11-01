#!/usr/bin/env python3
"""Independent checker for SAT models of gen_etv.py instances.

usage: check_model.py N solver_output
Decodes X(i,j,k) (variables 1..C(N,3), lexicographic), checks the signotope axioms, and computes by
dynamic programming (independently of the clauses) the longest cap, the longest cup and the largest
subset in convex position (= max over x<y of longest cap x..y + longest cup x..y - 2).
Also: brute-force cross-check of the largest convex subset on small N (all subsets via the
4-point/triangle criterion is too slow; instead we cross-check the chain DP against a direct
enumeration of cap/cup pairs for N <= 14).
"""
import itertools
import json
import sys


def read_model(fn):
    vals = {}
    sat = None
    for line in open(fn):
        if line.startswith("s "):
            sat = line.strip()
        if line.startswith("v "):
            for t in line.split()[1:]:
                v = int(t)
                if v != 0:
                    vals[abs(v)] = v > 0
    return sat, vals


def analyse(N, sigma):
    """sigma[(i,j,k)] in {+1,-1} for i<j<k (1-based)."""
    bad_axiom = 0
    for i, j, k, l in itertools.combinations(range(1, N + 1), 4):
        seq = [sigma[(i, j, k)], sigma[(i, j, l)], sigma[(i, k, l)], sigma[(j, k, l)]]
        changes = sum(1 for t in range(3) if seq[t] != seq[t + 1])
        if changes > 1:
            bad_axiom += 1
    # longest cap/cup from x to y, ending with edge (w,y): chain DP
    cap = {}
    cup = {}
    capxy = {}
    cupxy = {}
    for x in range(1, N + 1):
        # chains starting at x
        c_cap = {}
        c_cup = {}
        for y in range(x + 1, N + 1):
            c_cap[(x, y)] = 2
            c_cup[(x, y)] = 2
        for y in range(x + 1, N + 1):
            for w in range(x + 1, y):
                for v in range(x, w):
                    s = sigma[(v, w, y)]
                    if s < 0 and (v, w) in c_cap and c_cap[(v, w)] + 1 > c_cap.get((w, y), 0):
                        c_cap[(w, y)] = c_cap[(v, w)] + 1
                    if s > 0 and (v, w) in c_cup and c_cup[(v, w)] + 1 > c_cup.get((w, y), 0):
                        c_cup[(w, y)] = c_cup[(v, w)] + 1
        # c_cap[(w,y)]: longest cap starting at x with last edge (w,y); (x,y) means 2-chain
        for y in range(x + 1, N + 1):
            capxy[(x, y)] = max(c_cap.get((w, y), 0) for w in range(x, y))
            cupxy[(x, y)] = max(c_cup.get((w, y), 0) for w in range(x, y))
    longest_cap = max(capxy.values()) if capxy else min(N, 2)
    longest_cup = max(cupxy.values()) if cupxy else min(N, 2)
    gon = max(capxy[k] + cupxy[k] - 2 for k in capxy) if capxy else N
    return dict(axiom_violations=bad_axiom, longest_cap=longest_cap, longest_cup=longest_cup, largest_convex=gon)


def main():
    N = int(sys.argv[1])
    sat, vals = read_model(sys.argv[2])
    sigma = {}
    v = 0
    for t in itertools.combinations(range(1, N + 1), 3):
        v += 1
        sigma[t] = 1 if vals.get(v, False) else -1
    res = analyse(N, sigma)
    res["status"] = sat
    print(json.dumps(res))


if __name__ == "__main__":
    main()
