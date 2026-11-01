#!/usr/bin/env python3
"""Line-modules of an S1 Z[zeta_7] point file with my own code.  Usage: run_modules.py PTS TABLE.otv"""
import sys, collections
sys.path.insert(0, sys.path[0])
import z7, modmine

rows = z7.read_pts(sys.argv[1])
b = open(sys.argv[2], 'rb').read(); i = b.index(b'\n'); n = int(b[:i].split()[1]); T = b[i + 1:]
assert n == len(rows)


def O(a, c, d):
    v = T[(a * n + c) * n + d]
    return v - 256 if v > 127 else v


def upper(q, s):
    d = z7.sub(rows[s], rows[q])
    si = z7.sign_im(d)
    if si:
        return si > 0
    sr = z7.sign_re(d)
    assert sr != 0
    return sr > 0


L = modmine.left_masks(n, O)
ALL = (1 << n) - 1
# hull: directed edges p->r with every other point strictly left
edges = [(p, r) for p in range(n) for r in range(n) if p != r and L[p][r] == ALL & ~(1 << p) & ~(1 << r)]
succ = dict(edges)
assert len(succ) == len(edges)
start = edges[0][0]; cyc = [start]
while succ[cyc[-1]] != start:
    cyc.append(succ[cyc[-1]])
assert len(cyc) == len(edges)
hull = cyc
inner = [s for s in range(n) if s not in hull]
print('hull vertices (ccw):', hull, ' #inner =', len(inner))

mods, ncand, _ = modmine.enumerate_modules(n, O, upper, L)
print('distinct candidates tested:', ncand)
hist = collections.Counter(bin(C).count('1') for C in mods)
print('nontrivial line-modules (2..n-2):', len(mods), ' size histogram:', dict(sorted(hist.items())))
h = len(hull)
for C in mods:
    out = [s for s in range(n) if not (C >> s) & 1]
    # is the complement a set of consecutive hull vertices?
    desc = 'other'
    if all(s in hull for s in out):
        idx = sorted(hull.index(s) for s in out)
        for rot in range(h):
            if sorted((rot + t) % h for t in range(len(out))) == idx:
                desc = 'complement of %d consecutive hull vertices' % len(out)
                break
    print('  size %d, outside = %s : %s ; contains all inner points: %s' % (bin(C).count('1'), out, desc,
          all((C >> s) & 1 for s in inner)))
small = [C for C in mods if bin(C).count('1') <= 60]
print('modules of size 2..60:', len(small))
# n-1 complements are trivially modules (no line through two outside points): confirm with the test
print('all complements of one point pass the test:', all(modmine.is_module(n, ALL & ~(1 << s), L) for s in range(n)))
