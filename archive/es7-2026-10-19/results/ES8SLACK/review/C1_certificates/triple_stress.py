#!/usr/bin/env python3
"""Adversarial geometric stress test of the balanced six-order sign check (exact integers).

Builds random ordered configurations in general position with no 7-cup and no 7-cap (greedy random
insertion, several point distributions), computes the actual labels d_B(u,v) = (E_-(u,v)-1, E_+(u,v)-1),
incoming states (column-height profiles) and their catalog indices, and tests:
  (a) every profile is in the 252-state catalog, and states are pairwise distinct (Lemma 2.1);
  (b) for every ordered triple of distinct vertices (x,y,z) with CheckTriple(st[x],st[y],st[z]) true,
      orient(p_x,p_y,p_z) > 0  (the content of CycleSigns.checked_triple_positive).
A single violation would contradict the claimed geometric validity of the balanced cycle rows.
Usage: python3 -I triple_stress.py SEED NCONF
"""
import json, random, sys

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
cat = json.load(open(ROOT + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))['states']
index = {tuple(s): i for i, s in enumerate(cat)}
GRID = [(x, y) for x in range(1, 6) for y in range(1, 6)]


def contains(s, z):
    return z[1] <= s[z[0] - 1]


def box(a, b):
    d = [z for z in GRID if contains(cat[b], z) and not contains(cat[a], z)]
    if not d:
        return (False, 0, 0, 0, 0)
    return (True, min(z[0] for z in d), max(z[0] for z in d), min(z[1] for z in d), max(z[1] for z in d))


T = [[box(a, b) for b in range(252)] for a in range(252)]


def safe(ab, bc, ac, want):
    if not ab[0] or not bc[0] or not ac[0]:
        return True
    return bc[2] <= ab[1] if want else bc[4] <= ab[3]


def check_triple(a, b, c):
    return (safe(T[a][b], T[b][c], T[a][c], True) and safe(T[a][c], T[c][b], T[a][b], False) and
            safe(T[b][a], T[a][c], T[b][c], False) and safe(T[b][c], T[c][a], T[b][a], True) and
            safe(T[c][a], T[a][b], T[c][b], True) and safe(T[c][b], T[b][a], T[c][a], False))


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def ranks(P):
    n = len(P)
    Ep = [[0] * n for _ in range(n)]
    Em = [[0] * n for _ in range(n)]
    for v in range(n):
        for u in range(v):
            bp = bm = 2
            for t in range(u):
                o = orient(P[t], P[u], P[v])
                if o > 0 and Ep[t][u] + 1 > bp:
                    bp = Ep[t][u] + 1
                elif o < 0 and Em[t][u] + 1 > bm:
                    bm = Em[t][u] + 1
            Ep[u][v], Em[u][v] = bp, bm
    return Ep, Em


def general_position(P, q):
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            if orient(P[i], P[j], q) == 0:
                return False
    return True


def build(rng, target, mode):
    P = []
    tries = 0
    while len(P) < target and tries < 40 * target:
        tries += 1
        if mode == 0:
            q = (rng.randrange(10 ** 6), rng.randrange(10 ** 6))
        elif mode == 1:  # clustered
            cx, cy = rng.choice([(2e5, 2e5), (8e5, 3e5), (5e5, 9e5), (3e5, 7e5)])
            q = (int(cx + rng.gauss(0, 6e4)), int(cy + rng.gauss(0, 6e4)))
        elif mode == 2:  # wide x, small y spread: many long chains are rejected, mixed labels
            q = (rng.randrange(10 ** 7), rng.randrange(10 ** 4))
        else:  # perturbed grid
            q = (rng.randrange(40) * 25000 + rng.randrange(20000), rng.randrange(40) * 25000 + rng.randrange(20000))
        if any(p[0] == q[0] for p in P) or not general_position(P, q):
            continue
        Q = sorted(P + [q])
        Ep, Em = ranks(Q)
        n = len(Q)
        if max((Ep[u][v] for v in range(n) for u in range(v)), default=0) >= 7:
            continue
        if max((Em[u][v] for v in range(n) for u in range(v)), default=0) >= 7:
            continue
        P = Q
    return sorted(P)


def main():
    seed, nconf = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    stats = dict(configs=0, points=0, triples_checked=0, triples_passing=0, violations=0,
                 not_in_catalog=0, state_collisions=0, max_label=0, distinct_states_seen=set())
    viol = []
    for k in range(nconf):
        P = build(rng, rng.randrange(25, 56), k % 4)
        n = len(P)
        Ep, Em = ranks(P)
        st = []
        for v in range(n):
            prof = [0] * 5
            for u in range(v):
                d1, d2 = Em[u][v] - 1, Ep[u][v] - 1
                stats['max_label'] = max(stats['max_label'], d1, d2)
                for x in range(1, d1 + 1):
                    prof[x - 1] = max(prof[x - 1], d2)
            i = index.get(tuple(prof))
            if i is None:
                stats['not_in_catalog'] += 1
                i = -1
            st.append(i)
        if len(set(st)) != n:
            stats['state_collisions'] += 1
        stats['distinct_states_seen'] |= set(st)
        for x in range(n):
            for y in range(n):
                if y == x:
                    continue
                for z in range(n):
                    if z == x or z == y:
                        continue
                    stats['triples_checked'] += 1
                    if check_triple(st[x], st[y], st[z]):
                        stats['triples_passing'] += 1
                        if orient(P[x], P[y], P[z]) <= 0:
                            stats['violations'] += 1
                            if len(viol) < 5:
                                viol.append((k, x, y, z, st[x], st[y], st[z]))
        stats['configs'] += 1
        stats['points'] += n
    stats['distinct_states_seen'] = len(stats['distinct_states_seen'])
    stats['first_violations'] = viol
    print(json.dumps(stats))
    ok = stats['violations'] == 0 and stats['not_in_catalog'] == 0 and stats['state_collisions'] == 0
    print('NO VIOLATION' if ok else 'VIOLATION FOUND')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
