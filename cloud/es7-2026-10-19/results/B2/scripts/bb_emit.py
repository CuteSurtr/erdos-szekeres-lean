#!/usr/bin/env python3
"""Write Baek-Balko's etv_signotope CNF (https://github.com/jcpaik/erdos-szekeres-sat, lib/erdos.py)
without solving it.

usage: bb_emit.py BB_REPO_DIR k a u N out.cnf

Baek-Balko's etv(n, a, b, m): n = gon size, a = cap bound (cap triple = -v), b = cup bound
(cup triple = v), m = number of points. Their first C(m,3) variables are v(i,j,k) for
0 <= i < j < k < m in itertools.combinations order, which is the same numbering and the same
polarity (true = cup = counterclockwise) as gen_etv.py's X(i+1,j+1,k+1). So models and cubes
on the orientation variables are interchangeable between the two encoders.
"""
import json
import sys

repo, k, a, u, N, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
sys.path.insert(0, repo)
from lib.erdos import etv_signotope  # noqa: E402

inst = etv_signotope(k, a, u, N)
inst.write(out)
nX = N * (N - 1) * (N - 2) // 6
# sanity: the orientation variables must be 1..C(N,3) in combinations order
import itertools  # noqa: E402
for idx, t in enumerate(itertools.combinations(range(N), 3)):
    c = inst.v[t]._cnf
    assert c == [[idx + 1]], (t, c)
print(json.dumps({"enc": "bb", "k": k, "a": a, "u": u, "N": N, "vars": inst._num_vars,
                  "X": nX, "clauses": len(inst._clauses)}))
