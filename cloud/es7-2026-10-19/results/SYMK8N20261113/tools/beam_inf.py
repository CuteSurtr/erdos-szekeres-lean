#!/usr/bin/env python3
"""Beam search over *infinitesimal extensions* of an m-fold base set (m = 3, 4), exact limit order types.

State: list of orbit representatives (polynomial points in a symbolic eps), plus the centre flag.
Moves: double any orbit (twin with displacement eps^(1+maxexp) d, d one direction per open critical arc),
       new orbit at an outer (eps^-4) or inner (eps^+4) scale level (one direction per open critical arc).
A state is kept only if it has no convex K-gon (exact).  Ranking for the beam: fewest convex (K-1)-gons.
usage: beam_inf.py M FILE [--remove i,j,..] [--beam B] [--depth D] [--no-levels] [--K 8] [--add-centre]
"""
import sys, os, time, random, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ctypes
import double_exact as DE
DE.LIB = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libpolyeval2.so'))
DE.LIB.poly_eval.restype = ctypes.c_int
DE.LIB.poly_eval.argtypes = [ctypes.c_int] + [ctypes.c_void_p] * 5 + [ctypes.c_int, ctypes.c_void_p]
from double_exact import peval, read_set, orbits_of
from twostep import config, double_moves, level_moves, apply

m = int(sys.argv[1]); fn = sys.argv[2]
K = int(sys.argv[sys.argv.index('--K') + 1]) if '--K' in sys.argv else 8
B = int(sys.argv[sys.argv.index('--beam') + 1]) if '--beam' in sys.argv else 20
D = int(sys.argv[sys.argv.index('--depth') + 1]) if '--depth' in sys.argv else 6
levels = '--no-levels' not in sys.argv
if fn == 'NEEDLE':
    from needle_test import es_set
    E0 = sorted((x + 1, y) for (x, y) in es_set(4, 5))
    orbs = None; centre = False
else:
    P = read_set(fn, m)
    orbs, centre = orbits_of(P, m)
if orbs is not None and '--remove' in sys.argv:
    rem = set(int(x) for x in sys.argv[sys.argv.index('--remove') + 1].split(','))
    orbs = [o for i, o in enumerate(orbs) if i not in rem]
if '--add-centre' in sys.argv:
    centre = True
if orbs is None:
    reps = [[(0, r, 0), (1, 0, y)] for (r, y) in E0]
else:
    reps = [[(0, o[0][0], o[0][1])] for o in orbs]
ml, cnt, nz = peval(config(m, reps, centre), K)
tag = os.path.basename(fn) + ' ' + ' '.join(a for a in sys.argv[3:])
print('%s: base orbits=%d centre=%s n%d=%d n%d=%d' % (tag, len(reps), centre, K, cnt[K], K - 1, cnt[K - 1]), flush=True)
assert cnt[K] == 0
t0 = time.time()
beam = [(cnt[K - 1], reps)]
best_t = len(reps)
for depth in range(1, D + 1):
    cand = {}
    nev = 0
    for (_, st) in beam:
        moves = []
        for l in range(len(st)):
            moves += double_moves(m, st, centre, l)
        if levels:
            es = [e for r in st for (e, x, y) in r]
            moves += level_moves(m, st, centre, min(es) - 4) + level_moves(m, st, centre, max(es) + 4)
        for mv in moves:
            ns = apply(m, st, mv)
            ml, c, nz = peval(config(m, ns, centre), K)
            nev += 1
            if nz or c[K]:
                continue
            key = hashlib.sha1(repr(sorted(c)).encode() + repr(c).encode()).hexdigest()  # coarse dedupe by counts
            if key not in cand or c[K - 1] < cand[key][0]:
                cand[key] = (c[K - 1], ns)
    if not cand:
        print('depth %d: no octagon-free extension (evaluated %d, %.0fs)' % (depth, nev, time.time() - t0), flush=True)
        break
    beam = sorted(cand.values(), key=lambda x: x[0])[:B]
    best_t = len(beam[0][1])
    print('depth %d: %d distinct octagon-free states (count-signature), evaluated %d; keep %d; orbits now %d; '
          'min n%d=%d (%.0fs)' % (depth, len(cand), nev, len(beam), best_t, K - 1, beam[0][0], time.time() - t0),
          flush=True)
    if best_t * m + (1 if centre else 0) >= (56 if m == 4 else 63):
        print('TARGET SIZE REACHED:', beam[0][1], flush=True)
        import json
        json.dump({'m': m, 'points': config(m, beam[0][1], centre), 'reps': beam[0][1], 'centre': centre}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sets', 'found_beam_%d.json' % os.getpid()), 'w'))
print('DONE %s best orbits=%d points=%d (%.0fs)' % (tag, best_t, best_t * m + (1 if centre else 0), time.time() - t0),
      flush=True)
for (c7, st) in beam[:3]:
    print('  state n%d=%d reps=%s' % (K - 1, c7, st), flush=True)
