#!/usr/bin/env python3
"""One-point abstract extension: base signotope on N points (file .sig), new point inserted at
x-position p (1..N+1). Appends unit clauses fixing every triple of old points to the base CNF for
N+1 points (no symmetry breaking!).

usage: ext_cnf.py base.sig N p base_cnf_for_N+1 out.cnf
"""
import itertools
import sys


def main():
    sigf, N, p, cnf, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
    M = N + 1
    sig = {}
    for line in open(sigf):
        i, j, k, s = map(int, line.split())
        sig[(i, j, k)] = s
    assert len(sig) == N * (N - 1) * (N - 2) // 6
    idx = {}
    n = 0
    for t in itertools.combinations(range(1, M + 1), 3):
        n += 1
        idx[t] = n
    old = [i for i in range(1, M + 1) if i != p]  # old point a (1..N) -> old[a-1]
    units = []
    for (a, b, c), s in sig.items():
        t = (old[a - 1], old[b - 1], old[c - 1])
        units.append(idx[t] if s > 0 else -idx[t])
    lines = open(cnf).read().split("\n")
    out_lines = []
    for line in lines:
        if line.startswith("p cnf"):
            _, _, nv, nc = line.split()
            line = f"p cnf {nv} {int(nc) + len(units)}"
        out_lines.append(line)
    with open(out, "w") as f:
        f.write("\n".join(l for l in out_lines if l.strip() != "") + "\n")
        for u in units:
            f.write(f"{u} 0\n")


if __name__ == "__main__":
    main()
