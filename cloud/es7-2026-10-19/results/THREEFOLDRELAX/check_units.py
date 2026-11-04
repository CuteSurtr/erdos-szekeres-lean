#!/usr/bin/env python3
"""check_units.py CNF UNITS : file-based check that CNF + the unit clauses in UNITS (the real base assignment of
orbit, Y and H variables) is satisfiable.  Clauses are evaluated under UNITS; what remains must be Horn in the
remaining (chain) variables; the least model is computed by graph reachability and every clause is re-checked."""
import sys
from collections import defaultdict
A = {}
for line in open(sys.argv[2]):
    l = int(line.split()[0]); A[abs(l)] = l > 0
rest, nsat, nfalse = [], 0, 0
with open(sys.argv[1]) as f:
    for line in f:
        if line[0] in 'pc': continue
        lits = [int(x) for x in line.split()[:-1]]
        r, sat = [], False
        for l in lits:
            v = abs(l)
            if v in A:
                if A[v] == (l > 0): sat = True; break
            else: r.append(l)
        if sat: nsat += 1; continue
        if not r: nfalse += 1; continue
        rest.append(r)
pos = [r for r in rest if sum(1 for l in r if l > 0) > 1]
assert not pos, 'non-Horn residual'
true, edges, todo = set(), defaultdict(list), []
for r in rest:
    p = [l for l in r if l > 0]; n = [-l for l in r if l < 0]
    if p and not n: todo.append(p[0])
    elif p and len(n) == 1: edges[n[0]].append(p[0])
    elif p: edges[tuple(sorted(n))].append(p[0])   # multi-body (not expected)
while todo:
    v = todo.pop()
    if v in true: continue
    true.add(v); todo.extend(edges.get(v, []))
multi = [k for k in edges if isinstance(k, tuple)]
viol = sum(1 for r in rest if not any((l > 0 and l in true) or (l < 0 and -l not in true) for l in r))
print({'base_vars': len(A), 'sat_by_base': nsat, 'falsified_by_base': nfalse, 'residual': len(rest),
       'multi_body': len(multi), 'chain_true': len(true), 'residual_violated': viol})
