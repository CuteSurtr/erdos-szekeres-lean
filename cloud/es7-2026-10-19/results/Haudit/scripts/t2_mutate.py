#!/usr/bin/env python3
"""Mutation tests of covercheck.py (Mii-S) and of the own checker mycover.py on a real march cube tree.
usage: t2_mutate.py TOP.icnf SEED"""
import sys, random, subprocess, os
CC = '/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/Mii-S/scripts/covercheck.py'
top = [list(map(int, l.split()[1:-1])) for l in open(sys.argv[1]) if l.startswith('a')]
R = random.Random(int(sys.argv[2]))
D = max(len(c) for c in top)
refuted = [i for i, c in enumerate(top) if len(c) < D]
# a 2-level tree: split 3 random cubes by 3 fresh variables each (like close_march's children c+s)
used = {abs(l) for c in top for l in c}; fresh = [v for v in range(1, 5457) if v not in used]
tree = list(top)
for i in R.sample(range(len(top)), 3):
    c = tree[i]; vs = R.sample(fresh, 3); tree[i] = None
    for s in range(8): tree.append(c + [v if (s >> b) & 1 else -v for b, v in enumerate(vs)])
tree = [c for c in tree if c is not None]
def wr(cubes, p):
    with open(p, 'w') as f:
        for c in cubes: f.write("a " + " ".join(map(str, c)) + " 0\n")
def check(cubes, tag):
    p = f'/opt/work/mut/{tag}.icnf'; wr(cubes, p)
    a = subprocess.run(['python3', CC, p], capture_output=True, text=True).stdout.strip()
    b = subprocess.run(['python3', '/opt/audit/mycover.py', p, '/opt/work/mut/w'], capture_output=True, text=True).stdout.strip()
    print(f"{tag:28s} covercheck.py: {a:22s} mycover.py: {b}")
    return a.startswith("s COVERED"), b.startswith("s COVERED")
print("top cubes", len(top), "depth", D, "shorter (march-refuted) cubes", len(refuted), "tree leaves", len(tree))
res = {}
res['top'] = check(top, 'top')
res['tree'] = check(tree, 'tree')
for t in range(3):
    i = R.randrange(len(tree)); res[f'remove{t}'] = check(tree[:i] + tree[i+1:], f'remove_leaf_{t}')
for t in range(3):
    i = R.randrange(len(tree)); c = list(tree[i]); j = R.randrange(len(c)); c[j] = -c[j]
    res[f'flip{t}'] = check(tree[:i] + [c] + tree[i+1:], f'flip_literal_{t}')
for t, i in enumerate(R.sample(refuted, min(3, len(refuted)))):
    res[f'dropref{t}'] = check([c for c in top if c != top[i]], f'drop_refuted_{t}_len{len(top[i])}')
# a deeper leaf replaced by its parent prefix would be a superset: must still be covered (sanity)
i = R.randrange(len(tree)); res['shorten'] = check(tree[:i] + [tree[i][:-1]] + tree[i+1:], 'shorten_leaf(superset)')
# duplicate leaf: still covered
res['dup'] = check(tree + [tree[0]], 'duplicate_leaf')
exp = {k: (k in ('top', 'tree', 'shorten', 'dup')) for k in res}
ok = all(res[k] == (exp[k], exp[k]) for k in res)
print("ALL MUTATION TESTS AS EXPECTED" if ok else "UNEXPECTED RESULT", {k: v for k, v in res.items() if v != (exp[k], exp[k])})
