#!/usr/bin/env python3
"""Encoder B (gen_b2.py, any m): random real layered configurations never violate a non-chain clause.
usage: test_random_b2.py CNF N SEED"""
import os, sys, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'C7UPPER', 'tests')); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'C7UPPER'))
from validate import random_layers
from validate_b2 import assignment, check
cnf = sys.argv[1]; mp = json.load(open(cnf + '.map.json')); N = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
n = geo = withchain = 0
for s in range(N):
    A, mind = assignment(mp, random_layers(mp['m'], mp['t'], rng, ['free', 'needle'][s % 2]))
    if mind < 1e-9: continue
    o, c = check(cnf, mp, A); n += 1; geo += (o > 0); withchain += (c > 0)
print(cnf, 'configs', n, 'with non-chain violations', geo, 'with chain violations (convex octagon)', withchain)
