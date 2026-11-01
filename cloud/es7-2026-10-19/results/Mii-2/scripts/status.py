#!/usr/bin/env python3
"""Summarize a shard run: closed / open / SAT leaves and closed weight per root cube.

usage: status.py <resultdir> <cubes.icnf> [shard=2] [nshards=8]

Weight of a leaf = 2^-(len(cube) - len(root cube)) within its root (march_cu trees are binary).
A leaf is closed only if CaDiCaL said UNSAT and lrat-check printed VERIFIED.  Open = the
frontier implied by the shard roots and the recorded splits minus finished leaves.  The
script also checks that, under each root, closed + open leaves form a complete binary tree.
"""
import sys, os, json
from fractions import Fraction
rd, cubef = sys.argv[1], sys.argv[2]
shard = int(sys.argv[3]) if len(sys.argv) > 3 else 2; nsh = int(sys.argv[4]) if len(sys.argv) > 4 else 8
key = lambda c: ' '.join(map(str, c))
roots = [(i, [int(x) for x in l.split()[1:-1]]) for i, l in enumerate(open(cubef)) if l.startswith('a') and i % nsh == shard]
leaves, splits = {}, {}
if os.path.exists(os.path.join(rd, 'leaves.jsonl')):
    for l in open(os.path.join(rd, 'leaves.jsonl')): o = json.loads(l); leaves[key(o['cube'])] = o
if os.path.exists(os.path.join(rd, 'splits.jsonl')):
    for l in open(os.path.join(rd, 'splits.jsonl')):
        o = json.loads(l)
        if 'children' in o: splits[key(o['cube'])] = o
def frontier(c):
    k = key(c)
    if k in leaves: return [('leaf', c)]
    if k in splits: return [x for ch in splits[k]['children'] for x in frontier(ch)]
    return [('open', c)]
def complete(cubes, d):
    if any(len(c) == d for c in cubes): return len(cubes) == 1
    vs = set(abs(c[d]) for c in cubes)
    if len(vs) != 1: return False
    v = vs.pop(); pos = [c for c in cubes if c[d] == v]; neg = [c for c in cubes if c[d] == -v]
    return bool(pos) and bool(neg) and complete(pos, d + 1) and complete(neg, d + 1)
tot = {'roots': len(roots), 'closed_leaves': 0, 'closed_lrat_verified': 0, 'unsat_not_verified': 0,
       'sat_leaves': 0, 'open_leaves': 0, 'splits': len(splits), 'closed_weight': Fraction(0), 'roots_fully_closed': 0}
per = []
for i, r in roots:
    fr = frontier(r); w = Fraction(0); st = {'closed': 0, 'open': 0, 'sat': 0, 'unver': 0}
    for kind, c in fr:
        if kind == 'open': st['open'] += 1; continue
        o = leaves[key(c)]
        if o['status'] == 'SAT': st['sat'] += 1
        elif o['status'] == 'UNSAT' and o['lrat'] == 'VERIFIED': st['closed'] += 1; w += Fraction(1, 2 ** (len(c) - len(r)))
        else: st['unver'] += 1
    ok = complete([c[len(r):] for _, c in fr], 0) if fr != [('leaf', r)] and fr != [('open', r)] else True
    per.append({'root': i, 'closed': st['closed'], 'open': st['open'], 'sat': st['sat'], 'unsat_unverified': st['unver'],
                'closed_weight': str(w), 'closed_weight_f': float(w), 'tree_complete': ok, 'fully_closed': w == 1 and ok})
    tot['closed_leaves'] += st['closed']; tot['closed_lrat_verified'] += st['closed']; tot['sat_leaves'] += st['sat']
    tot['open_leaves'] += st['open']; tot['unsat_not_verified'] += st['unver']; tot['closed_weight'] += w / len(roots)
    tot['roots_fully_closed'] += (w == 1 and ok)
tot['closed_weight_of_shard'] = float(tot['closed_weight']); tot['closed_weight'] = str(tot['closed_weight'])
tot['shard_fully_closed'] = tot['roots_fully_closed'] == len(roots)
print(json.dumps({'total': tot, 'per_root': per}, indent=1))
