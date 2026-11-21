#!/usr/bin/env python3
"""Random exact controls for C2: random integer point sets, pruned (by deleting a vertex of a
found 6-cap / 8-cup) until they have no 6-cap and no 8-cup; then the c2check.analyse checks.
Several generators: uniform box, concave arcs with noise (cap-rich), mixed convex/concave arcs."""
import sys, os, random, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c2check import analyse, newstats, find_chain, orient


def general_position(P):
    n = len(P)
    xs = [p[0] for p in P]
    if len(set(xs)) != n:
        return False
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if orient(P[i], P[j], P[k]) == 0:
                    return False
    return True


def gen(rng):
    kind = rng.choice(['box', 'arcs', 'mixed', 'box'])
    n = rng.randint(10, 34)
    P = set()
    if kind == 'box':
        B = rng.choice([50, 1000, 10**6])
        while len(P) < n:
            P.add((rng.randint(0, B), rng.randint(0, B)))
    elif kind == 'arcs':
        k = rng.randint(1, 4)
        while len(P) < n:
            c = rng.randrange(k)
            x = rng.randint(0, 10**4)
            y = -((x - 3000 * c) ** 2) // (500 + 400 * c) + 7000 * c + rng.randint(-2000, 2000)
            P.add((x, y))
    else:
        while len(P) < n:
            s = rng.choice([1, -1])
            x = rng.randint(0, 10**4)
            y = s * ((x - rng.randint(0, 10**4)) ** 2) // 2000 + rng.randint(-5000, 5000)
            P.add((x, y))
    P = sorted(P)
    # enforce distinct x and general position by dropping offenders
    Q = []
    for p in P:
        if Q and Q[-1][0] == p[0]:
            continue
        Q.append(p)
    changed = True
    while changed:
        changed = False
        n = len(Q)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if orient(Q[i], Q[j], Q[k]) == 0:
                        del Q[rng.choice([i, j, k])]
                        changed = True
                        break
                if changed:
                    break
            if changed:
                break
    # prune 6-caps and 8-cups
    while True:
        c = find_chain(Q, 6, 'cap')
        if c is None:
            c = find_chain(Q, 8, 'cup')
        if c is None:
            break
        del Q[rng.choice(c)]
    return kind, Q


def main():
    seed = int(sys.argv[1])
    budget = float(sys.argv[2])
    rng = random.Random(seed)
    st = newstats()
    t0 = time.time()
    kinds = {}
    sizes = []
    while time.time() - t0 < budget:
        kind, Q = gen(rng)
        if len(Q) < 3:
            continue
        assert general_position(Q)
        r = analyse(Q, (seed, st['configs']), st)
        kinds[kind] = kinds.get(kind, 0) + 1
        sizes.append(len(Q))
    st['kinds'] = kinds
    st['size_min_max_mean'] = (min(sizes), max(sizes), sum(sizes) / len(sizes))
    print(json.dumps(st, default=str))


if __name__ == '__main__':
    main()
