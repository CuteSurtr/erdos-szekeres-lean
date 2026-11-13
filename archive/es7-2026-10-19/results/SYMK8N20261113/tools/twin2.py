#!/usr/bin/env python3
"""Complement to twostep.py (4-fold): delete one layer, add an octagon-free infinitesimal orbit a (twin or level),
then add a TWIN OF a (hierarchical cluster: twin of a twin, or a new level square plus its own twin), scanning one
direction per open critical arc of the second twin on B + a (complete for generic directions).
usage: twin2.py LISTFILE SECONDS"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ctypes
import double_exact as DE
DE.LIB = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libpolyeval2.so'))
DE.LIB.poly_eval.restype = ctypes.c_int
DE.LIB.poly_eval.argtypes = [ctypes.c_int] + [ctypes.c_void_p] * 5 + [ctypes.c_int, ctypes.c_void_p]
from double_exact import peval, read_set, orbits_of
from twostep import config, double_moves, level_moves, apply

files = [l.strip() for l in open(sys.argv[1]) if l.strip()]
T = float(sys.argv[2])
m = 4
t0 = time.time()
tot_bases = 0; tot_first = 0; tot_second = 0; found = 0; best = None
for fn in files:
    P = read_set(fn, m)
    orbs, centre = orbits_of(P, m)
    for r in range(len(orbs)):
        if time.time() - t0 > T:
            break
        reps = [[(0, o[0][0], o[0][1])] for i, o in enumerate(orbs) if i != r]
        moves = []
        for l in range(len(reps)):
            moves += double_moves(m, reps, centre, l)
        moves += level_moves(m, reps, centre, -4) + level_moves(m, reps, centre, 4)
        firsts = []
        for mv in moves:
            ml, cnt, nz = peval(config(m, apply(m, reps, mv), centre), 8)
            if not nz and cnt[8] == 0:
                firsts.append(mv)
        tot_bases += 1; tot_first += len(firsts)
        bb = None
        for a in firsts:
            ra = apply(m, reps, a)
            k = len(ra) - 1
            for mv2 in double_moves(m, ra, centre, k):
                rr = apply(m, ra, mv2)
                ml, cnt, nz = peval(config(m, rr, centre), 8)
                tot_second += 1
                if nz:
                    continue
                if bb is None or cnt[8] < bb:
                    bb = cnt[8]
                if cnt[8] == 0:
                    found += 1
                    print('FOUND', fn, r, a, mv2, flush=True)
        if bb is not None and (best is None or bb < best):
            best = bb
        print('%s remove=%d: first moves %d, twins of them %s best %s (%.0fs)' % (os.path.basename(fn), r, len(firsts),
              tot_second, bb, time.time() - t0), flush=True)
print('DONE bases=%d first=%d second=%d found=%d best=%s (%.0fs)' % (tot_bases, tot_first, tot_second, found, best,
      time.time() - t0), flush=True)
