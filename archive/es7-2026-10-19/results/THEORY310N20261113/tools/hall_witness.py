"""Fix the in-vector to a known balanced witness; search an out-vector g (all rows,
same population, state 0 occupied) with a perfect matching between occupied in- and
out-states in the compatibility graph (exact Hall condition)."""
import json, sys
import numpy as np, highspy
sys.argv_saved = sys.argv; sys.argv = [sys.argv[0]]
from hall import S, C, n, comp
R = '/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/'
w72 = set(json.load(open(R + 'ES8SLACK/witnesses.json'))['balanced_v2_72_hole_witness'])
w71 = set(json.loads(open(R + 'ES8UPPER20261105/pilot/witness_solutions.jsonl').read().splitlines()[1])['set'])
def test(holes, tl=300):
    occ = [i for i in range(n) if i not in holes]
    edges = [(i, j) for i in occ for j in range(n) if comp[i, j]]
    h = highspy.Highs(); h.silent(); h.setOptionValue('threads', 1); h.setOptionValue('time_limit', float(tl))
    inf = highspy.kHighsInf
    for j in range(n):                       # g_j out-holes
        h.addVar(0.0, 0.0 if j == 0 else 1.0); h.changeColIntegrality(j, highspy.HighsVarType.kInteger)
    for e in edges:
        h.addVar(0.0, 1.0); h.changeColIntegrality(n + edges.index(e) if False else h.getNumCol() - 1, highspy.HighsVarType.kInteger)
    for r in C:
        sup = np.array(r['support'], dtype=np.int32); h.addRow(float(r['rhs']), inf, len(sup), sup, np.ones(len(sup)))
    h.addRow(float(len(holes)), float(len(holes)), n, np.arange(n, dtype=np.int32), np.ones(n))
    by_i = {}; by_j = {}
    for k, (i, j) in enumerate(edges):
        by_i.setdefault(i, []).append(n + k); by_j.setdefault(j, []).append(n + k)
    for i in occ:                            # each occupied in-state matched once
        idx = np.array(by_i.get(i, []), dtype=np.int32); h.addRow(1.0, 1.0, len(idx), idx, np.ones(len(idx)))
    for j in range(n):                       # sum_i x_ij = 1 - g_j
        idx = np.array(by_j.get(j, []) + [j], dtype=np.int32)
        h.addRow(1.0, 1.0, len(idx), idx, np.ones(len(idx)))
    h.run()
    return str(h.getModelStatus()), len(edges)
for name, W in (('w72', w72), ('w71', w71)):
    print(name, len(W), test(W), flush=True)
