#!/usr/bin/env python3
"""decode_check.py NAME [CA CB G] -- decode a satisfying assignment of an owner-model CNF
(run/NAME.cnf + .names.pkl, model in run/NAME.model) into a 2-colouring of the triples of the
owners in chronological order, and check it INDEPENDENTLY of the CNF (position-indexed, pure
Python): longest cap / cup path (consecutive triples), weak polygons (a-cap path and b-cup path on
common endpoints, a + b = G + 2), signotope violations.  Writes run/NAME.coloring.json."""
import sys, pickle, json, itertools, functools
sys.path.insert(0, '.')
import cat_common


def decode(name):
    meta = pickle.load(open(f'run/{name}.cnf.names.pkl', 'rb'))
    names = meta['names']
    states = cat_common.make(meta['CA'], meta['CB'])[0]
    val = {}
    for line in open(f'run/{name}.model'):
        for t in line.split()[1:]:
            l = int(t)
            if l:
                val[abs(l)] = l > 0
    NS = len(states)
    occ = [s for s in range(NS) if val[names[('occ', s)]]]

    def before(a, b):
        v = names.get(('P', a, b))
        return v is not None and val[v]
    order = sorted(occ, key=functools.cmp_to_key(lambda a, b: -1 if before(a, b) else 1))
    n = len(order)
    assert all(before(order[i], order[j]) for i in range(n) for j in range(i + 1, n)), 'order not total'
    col = {}
    for i, j, k in itertools.combinations(range(n), 3):
        x, y, z = order[i], order[j], order[k]
        t = tuple(sorted((x, y, z)))
        inv = (x > y) + (x > z) + (y > z)
        v = val[names[('ori',) + t]]
        col[(i, j, k)] = 1 if (v if inv % 2 == 0 else not v) else -1
    return meta, states, order, col


def check(n, col, G):
    """independent position-indexed check; returns dict"""
    res = {}
    best = {1: {}, -1: {}}
    longest = {}
    for sgn in (1, -1):
        mx = 2
        for s in range(n):
            L = {(s, j): 2 for j in range(s + 1, n)}      # longest path from s ending with pair (.,.)
            for k in range(s + 2, n):
                for j in range(s + 1, k):
                    b = 0
                    if col[(s, j, k)] == sgn:
                        b = 3
                    for i in range(s + 1, j):
                        if col[(i, j, k)] == sgn and L.get((i, j), 0) >= 3:
                            b = max(b, L[(i, j)] + 1)
                    L[(j, k)] = b
                    if b:
                        mx = max(mx, b)
                        if b > best[sgn].get((s, k), 2):
                            best[sgn][(s, k)] = b
        longest[sgn] = mx
    res['longest_cap_path'] = longest[-1]
    res['longest_cup_path'] = longest[1]
    worst = 0
    wit = None
    for s in range(n):
        for t in range(s + 1, n):
            a = best[-1].get((s, t), 2)
            b = best[1].get((s, t), 2)
            if a >= 3 and b >= 3 and a + b - 2 > worst:
                worst = a + b - 2
                wit = (s, t, a, b)
    res['largest_weak_polygon'] = worst
    res['largest_weak_polygon_witness'] = wit
    res['has_weak_G_gon'] = bool(worst >= G or longest[1] >= G or longest[-1] >= G)
    bad = 0
    for i, j, k, l in itertools.combinations(range(n), 4):
        q = [col[(i, j, k)], col[(i, j, l)], col[(i, k, l)], col[(j, k, l)]]
        ch = sum(1 for a in range(3) if q[a] != q[a + 1])
        if ch > 1:
            bad += 1
    res['signotope_violations'] = bad
    res['four_tuples'] = n * (n - 1) * (n - 2) * (n - 3) // 24
    return res


if __name__ == '__main__':
    name = sys.argv[1]
    meta, states, order, col = decode(name)
    n = len(order)
    res = check(n, col, meta['G'])
    res['n'] = n
    res['states_in_order'] = [list(states[s]) for s in order]
    print(json.dumps(res))
    json.dump({'n': n, 'G': meta['G'], 'states_in_order': res['states_in_order'],
               'triples_positive': [list(t) for t, v in sorted(col.items()) if v > 0], 'check': res},
              open(f'run/{name}.coloring.json', 'w'))
