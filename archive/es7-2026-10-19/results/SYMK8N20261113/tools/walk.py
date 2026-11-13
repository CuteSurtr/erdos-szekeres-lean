#!/usr/bin/env python3
"""Random walk in the space of 13-layer octagon-free 4-fold *limit* configurations (HEURISTIC).
State: 13 orbits (polynomial points).  Each step: (1) scan every single infinitesimal move (twin of any orbit, new
outer/inner level) of the state; an octagon-free one would be a 14-layer configuration (saved and reported);
(2) otherwise delete a random orbit and replace it by a random octagon-free infinitesimal move of the 12-orbit base.
usage: walk.py FILE.pts SEED SECONDS"""
import sys, os, random, time, json, ctypes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import double_exact as DE
DE.LIB = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libpolyeval2.so'))
DE.LIB.poly_eval.restype = ctypes.c_int
DE.LIB.poly_eval.argtypes = [ctypes.c_int] + [ctypes.c_void_p] * 5 + [ctypes.c_int, ctypes.c_void_p]
from double_exact import peval, read_set, orbits_of
from twostep import config, double_moves, level_moves, apply

fn, seed, T = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
random.seed(seed)
m = 4
P = read_set(fn, m)
orbs, centre = orbits_of(P, m)
state = [[(0, o[0][0], o[0][1])] for o in orbs]
t0 = time.time()


def moves_of(st):
    mv = []
    for l in range(len(st)):
        mv += double_moves(m, st, centre, l)
    es = [e for r in st for (e, x, y) in r]
    mv += level_moves(m, st, centre, min(es) - 4) + level_moves(m, st, centre, max(es) + 4)
    return mv


def n8(st):
    try:
        ml, cnt, nz = peval(config(m, st, centre), 8)
    except AssertionError:   # coordinate bound 2^60 exceeded: skip this move
        return None
    return None if nz else cnt[8]


step = 0; best14 = None
while time.time() - t0 < T:
    step += 1
    mv = moves_of(state)
    best = None
    for x in mv:
        v = n8(apply(m, state, x))
        if v is None:
            continue
        if best is None or v < best:
            best = v
        if v == 0:
            out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sets', 'walk_found_%d_%d.json' % (seed, step))
            json.dump({'m': m, 'reps': apply(m, state, x), 'points': config(m, apply(m, state, x), centre)}, open(out, 'w'))
            print('FOUND 14-layer octagon-free limit configuration, saved', out, flush=True)
            sys.exit(0)
    if best14 is None or best < best14:
        best14 = best
    # move to a random neighbour
    for attempt in range(20):
        r = random.randrange(len(state))
        base = state[:r] + state[r + 1:]
        cand = moves_of(base)
        random.shuffle(cand)
        nxt = None
        for x in cand[:400]:
            ns = apply(m, base, x)
            if ns == state:
                continue
            if n8(ns) == 0:
                nxt = ns
                break
        if nxt is not None:
            state = nxt
            break
    print('step %d: best 14-layer octagon count %s (overall min %s), exps %s (%.0fs)' % (
        step, best, best14, sorted(set(e for rr in state for (e, x, y) in rr)), time.time() - t0), flush=True)
print('DONE steps=%d overall min octagons for a 14th orbit = %s' % (step, best14), flush=True)
