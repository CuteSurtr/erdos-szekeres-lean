#!/usr/bin/env python3
"""Sampling check of arc completeness for level moves (4-fold outer level over the ES8SYM set) and for 3-fold twins
(c3_61pts_centre, orbit 5): random directions never give fewer octagons than the minimum over arc representatives."""
import sys, os, random, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from double_exact import peval, read_set, orbits_of
from twostep import config, double_moves, level_moves, apply
random.seed(11)
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sets')
P = read_set(os.path.join(W, 'lib4', 'es8sym_52.pts'), 4); orbs, c = orbits_of(P, 4)
reps = [[(0, o[0][0], o[0][1])] for o in orbs]
arcmin = min(peval(config(4, apply(4, reps, mv), c), 8)[1][8] for mv in level_moves(4, reps, c, -4))
mn = None
for _ in range(2000):
    a = random.uniform(0, 2 * math.pi); v = (int(1e12 * math.cos(a)), int(1e12 * math.sin(a)))
    ml, cnt, nz = peval(config(4, reps + [[(-4, v[0], v[1])]], c), 8)
    if not nz:
        mn = cnt[8] if mn is None else min(mn, cnt[8])
print('4-fold outer level over ES8SYM: arc minimum %d, 2000 random directions minimum %s' % (arcmin, mn), flush=True)
P = read_set(os.path.join(W, 'lib3', 'c3_61pts_centre.txt'), 3); orbs, c = orbits_of(P, 3)
reps = [[(0, o[0][0], o[0][1])] for o in orbs]
arcmin = min(peval(config(3, apply(3, reps, mv), c), 8)[1][8] for mv in double_moves(3, reps, c, 5))
mn = None
for _ in range(2000):
    a = random.uniform(0, 2 * math.pi); d = (int(1e15 * math.cos(a)), int(1e15 * math.sin(a)))
    ml, cnt, nz = peval(config(3, reps + [reps[5] + [(1, d[0], d[1])]], c), 8)
    if not nz:
        mn = cnt[8] if mn is None else min(mn, cnt[8])
print('3-fold twin of orbit 5 of c3_61pts_centre: arc minimum %d, 2000 random directions minimum %s' % (arcmin, mn), flush=True)
