#!/usr/bin/env python3
"""Exhaustive validation of the CNF on small N.

Enumerate ALL signotopes on N points (DFS over triples in lexicographic order, checking every
quadruple as soon as its 4 triples are fixed). For each signotope, decide whether the actual CNF
file (aux variables free) is satisfiable with these X values -- the aux part is Horn, so unit
propagation decides it exactly -- and compare with the independent 4-point brute force
(count of convex K-subsets == 0).

usage: exhaustive_validate.py N K cnf_file [--hull]
"""
import itertools
import sys
from sigcheck import count_convex_4pt


def load_cnf(path):
    clauses = []
    nv = 0
    with open(path) as f:
        for line in f:
            if line.startswith("c"):
                continue
            if line.startswith("p"):
                nv = int(line.split()[2])
                continue
            lits = list(map(int, line.split()))
            assert lits[-1] == 0
            clauses.append(lits[:-1])
    return nv, clauses


def cnf_sat_given_X(nv, clauses, occ, xassign):
    """xassign: dict var->bool for X vars. Unit propagation; Horn in aux vars => exact."""
    val = [None] * (nv + 1)
    for v, b in xassign.items():
        val[v] = b
    # simple propagation loop
    queue = list(range(len(clauses)))
    inq = [True] * len(clauses)
    while queue:
        ci = queue.pop()
        inq[ci] = False
        c = clauses[ci]
        unassigned = None
        nun = 0
        satisfied = False
        for l in c:
            v = val[abs(l)]
            if v is None:
                nun += 1
                unassigned = l
                if nun > 1:
                    break
            elif v == (l > 0):
                satisfied = True
                break
        if satisfied:
            continue
        if nun == 0:
            return False
        if nun == 1:
            var = abs(unassigned)
            val[var] = unassigned > 0
            for cj in occ[var]:
                if not inq[cj]:
                    inq[cj] = True
                    queue.append(cj)
    # completion: unassigned -> False; must satisfy all clauses
    for c in clauses:
        if not any((val[abs(l)] if val[abs(l)] is not None else False) == (l > 0) for l in c):
            return None  # would indicate non-Horn behaviour
    return True


def enumerate_signotopes(N):
    triples = list(itertools.combinations(range(1, N + 1), 3))
    # for each triple position, the quadruples completed when it is assigned
    order = {t: n for n, t in enumerate(triples)}
    complete_at = [[] for _ in triples]
    for q in itertools.combinations(range(1, N + 1), 4):
        i, j, k, l = q
        ts = [(i, j, k), (i, j, l), (i, k, l), (j, k, l)]
        last = max(order[t] for t in ts)
        complete_at[last].append(ts)
    sig = {}

    def ok(pos):
        for ts in complete_at[pos]:
            seq = [sig[t] for t in ts]
            if sum(1 for a in range(3) if seq[a] != seq[a + 1]) > 1:
                return False
        return True

    def dfs(pos):
        if pos == len(triples):
            yield dict(sig)
            return
        t = triples[pos]
        for s in (1, -1):
            sig[t] = s
            if ok(pos):
                yield from dfs(pos + 1)
        del sig[t]

    yield from dfs(0)


def main():
    N, K, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    hull = "--hull" in sys.argv
    mirror = "--mirror" in sys.argv
    nv, clauses = load_cnf(path)
    occ = [[] for _ in range(nv + 1)]
    for ci, c in enumerate(clauses):
        for l in c:
            occ[abs(l)].append(ci)
    triples = list(itertools.combinations(range(1, N + 1), 3))
    total = 0
    nogon = 0
    nogon_hull = 0
    mismatch = 0
    cnf_sat = 0
    for sig in enumerate_signotopes(N):
        total += 1
        brute_free = count_convex_4pt(sig, N, K, stop_at=1) == 0
        is_hull = all(sig[(1, i, j)] > 0 for i, j in itertools.combinations(range(2, N + 1), 2))
        if brute_free:
            nogon += 1
            if is_hull:
                nogon_hull += 1
        xa = {n + 1: sig[t] > 0 for n, t in enumerate(triples)}
        r = cnf_sat_given_X(nv, clauses, occ, xa)
        assert r is not None, "non-Horn completion failure"
        if r:
            cnf_sat += 1
        expected = brute_free and (is_hull or not hull)
        if mirror and N >= 7:
            expected = expected and (sig[(2, 3, 4)] < 0 or sig[(N - 2, N - 1, N)] > 0)
        if hull:
            pass
        if r != expected:
            mismatch += 1
            if mismatch <= 5:
                print("MISMATCH", r, brute_free, is_hull, sig)
    print(f"N={N} K={K} cnf={path} hull_mode={hull} mirror_mode={mirror}: signotopes={total} "
          f"no-convex-{K}-gon(4pt brute)={nogon} of which X(1,i,j)=+ : {nogon_hull}; "
          f"CNF-satisfiable={cnf_sat}; mismatches={mismatch}")


if __name__ == "__main__":
    main()
