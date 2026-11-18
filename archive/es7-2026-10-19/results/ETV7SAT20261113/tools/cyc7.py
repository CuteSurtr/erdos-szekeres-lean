#!/usr/bin/env python3
"""cyc7.py -- cycle rows for the heptagon catalog (own implementation, 13 Nov 2026).

Lemma (cycle row; math.md Lemma 2.2 / ETV5N20261113 section 2, restated in README section 8).
Let L = (s_1,...,s_k) be distinct states such that for all i<j<l and for every chronological order
(x,y,z) of {s_i,s_j,s_l} that is feasible (D'(x->y), D'(y->z), D'(x->z) nonempty) the orientation of
the owners is forced to make det(p_{s_i}, p_{s_j}, p_{s_l}) > 0.  Then the owners of the occupied
states of L are in convex position, so at most G-1 states of L are occupied.
"Forced": for a chronological triple x<y<z a cup needs d2(y,z) > d2(x,y) and a cap needs
d1(y,z) > d1(x,y) (Growth); so the triple is forced to be a cup if
max d1 over D'(y->z) <= min d1 over D'(x->y), and forced to be a cap if the same holds for d2.

usage: cyc7.py CA CB G out.json [workers] [timelimit]
Lazy separation with CP-SAT (COMPUTED): minimise the number of holes subject to the rows found so
far, the block rows S1, S2 <= bound56, B1, B2 <= bound47 and the two fixed occupied states.
"""
import sys, json, time, random, itertools
sys.path.insert(0, '.')
import cat_common


def forced_table(CA, CB):
    states, cells, capH, cupH, D = cat_common.make(CA, CB)
    N = len(states)
    ne = [[bool(D[s][t]) for t in range(N)] for s in range(N)]
    mn = [[[min((z[c] for z in D[s][t]), default=0) for t in range(N)] for s in range(N)] for c in (0, 1)]
    mx = [[[max((z[c] for z in D[s][t]), default=0) for t in range(N)] for s in range(N)] for c in (0, 1)]

    def forced_pos(a, b, c):
        """list-order triple (a,b,c): positive orientation forced in every feasible chronological order"""
        tri = (a, b, c)
        for perm in itertools.permutations(range(3)):
            x, y, z = tri[perm[0]], tri[perm[1]], tri[perm[2]]
            if not (ne[x][y] and ne[y][z] and ne[x][z]):
                continue
            inv = sum(1 for i in range(3) for j in range(i + 1, 3) if perm[i] > perm[j])
            if inv % 2 == 0:
                # chronological orientation must be positive (cup): a cap must be impossible
                if not (mx[0][y][z] <= mn[0][x][y]):
                    return False
            else:
                # chronological orientation must be negative (cap): a cup must be impossible
                if not (mx[1][y][z] <= mn[1][x][y]):
                    return False
        return True
    T = [[[False] * N for _ in range(N)] for _ in range(N)]
    cnt = 0
    for a in range(N):
        for b in range(N):
            if b == a:
                continue
            for c in range(N):
                if c == a or c == b:
                    continue
                if forced_pos(a, b, c):
                    T[a][b][c] = True
                    cnt += 1
    return states, T, cnt


def list_ok(T, lst):
    return all(T[lst[i]][lst[j]][lst[l]] for i in range(len(lst)) for j in range(i + 1, len(lst))
               for l in range(j + 1, len(lst)))


def find_lists(T, N, occ, k, limit, rng):
    """lists of k occupied states with all triples forced positive (first element = minimum index)"""
    occ = sorted(occ)
    res = []
    seen = set()

    def dfs(seq, cand):
        if len(res) >= limit:
            return
        if len(seq) == k:
            key = frozenset(seq)
            if key not in seen:
                seen.add(key)
                res.append(tuple(seq))
            return
        for x in cand:
            if all(T[seq[i]][seq[j]][x] for i in range(len(seq)) for j in range(i + 1, len(seq))):
                nc = [y for y in cand if y != x and all(T[s][x][y] for s in seq)]
                if len(seq) + 1 + len(nc) >= k:
                    dfs(seq + [x], nc)
            if len(res) >= limit:
                return
    starts = occ[:]
    rng.shuffle(starts)
    for s in starts:
        cand = [x for x in occ if x > s]
        dfs([s], cand)
        if len(res) >= limit:
            break
    return res


def extend(T, N, lst, rng):
    lst = list(lst)
    cand = list(range(N))
    rng.shuffle(cand)
    changed = True
    while changed:
        changed = False
        for x in cand:
            if x in lst:
                continue
            for p in range(len(lst) + 1):
                new = lst[:p] + [x] + lst[p:]
                if list_ok(T, new):
                    lst = new
                    changed = True
                    break
    return lst


def main():
    from ortools.sat.python import cp_model
    CA, CB, G = map(int, sys.argv[1:4])
    out = sys.argv[4]
    W = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    TL = float(sys.argv[6]) if len(sys.argv) > 6 else 600
    t0 = time.time()
    states, T, cnt = forced_table(CA, CB)
    N = len(states)
    print('states', N, 'forced list-order triples', cnt, 'table time', round(time.time() - t0, 1), flush=True)
    rng = random.Random(7)
    rows = {}        # frozenset(list) -> (list in order, demand)
    blocks = []
    if (CA, CB, G) == (3, 5, 7):
        blocks = [('S1', [i for i, f in enumerate(states) if f[0] <= 4], 25),
                  ('S2', [i for i, f in enumerate(states) if f[2] >= 1], 25),
                  ('B1', [i for i, f in enumerate(states) if f[2] == 0], 16),
                  ('B2', [i for i, f in enumerate(states) if f[0] == 5], 16)]
    fixed = [states.index(tuple([0] * CA)), states.index(tuple([1] + [0] * (CA - 1)))]

    def solve():
        m = cp_model.CpModel()
        h = [m.NewBoolVar(f'h{i}') for i in range(N)]
        for i in fixed:
            m.Add(h[i] == 0)
        for key, (lst, d) in rows.items():
            m.Add(sum(h[i] for i in lst) >= d)
        for name, fam, K in blocks:
            m.Add(sum(h[i] for i in fam) >= len(fam) - K)
        m.Minimize(sum(h))
        so = cp_model.CpSolver()
        so.parameters.num_workers = W
        so.parameters.max_time_in_seconds = 300
        st = so.Solve(m)
        return so.StatusName(st), [i for i in range(N) if so.Value(h[i])], so.BestObjectiveBound()
    it = 0
    while True:
        it += 1
        st, H, bd = solve()
        occ = [i for i in range(N) if i not in set(H)]
        L = find_lists(T, N, occ, G, 80, rng)
        add = 0
        for l in L:
            E = extend(T, N, l, rng)
            key = frozenset(E)
            if key not in rows:
                rows[key] = (E, len(E) - (G - 1))
                add += 1
        print(f'it {it} rows {len(rows)} status {st} holes {len(H)} bound {bd} new {add} t={time.time()-t0:.1f}', flush=True)
        json.dump({'CA': CA, 'CB': CB, 'G': G, 'status': st, 'min_holes': len(H), 'holes': H, 'iter': it,
                   'closed': not L,
                   'rows': [[lst, d] for (lst, d) in rows.values()],
                   'blocks': [[n, f, K] for n, f, K in blocks]}, open(out, 'w'))
        if not L or time.time() - t0 > TL:
            break
    print('FINAL', st, 'min holes', len(H), 'capacity', N - len(H), 'closed (no violated 7-list found by full DFS):', not L)


if __name__ == '__main__':
    main()
