#!/usr/bin/env python3
"""Bin-order clauses (trivially sound): [psi_j < psi_i] and [psi_i < b U/B] => [psi_j < b U/B], with
Y(i,j) = [psi_i < psi_j] of gen.py Enc(m, K, t) and Z(i, b) = NV0 + (i-1)(B-1) + b as in cell_rules.py.
usage: binorder.py m t B NV0 OUT.clauses"""
import sys, os, importlib.util
m, t, B, NV0 = map(int, sys.argv[1:5])
s = importlib.util.spec_from_file_location('gen', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen.py'))
G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
E = G.Enc(m, 9, t)
def lt(a, b): return E.Y[(a, b)] if a < b else -E.Y[(b, a)]
def Z(i, b): return NV0 + (i - 1) * (B - 1) + b
with open(sys.argv[5], 'w') as f:
    for i in range(1, t):
        for j in range(1, t):
            if i != j:
                for b in range(1, B):
                    f.write('%d %d %d 0\n' % (-lt(j, i), -Z(i, b), Z(j, b)))
