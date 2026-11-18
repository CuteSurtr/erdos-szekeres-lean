"""Cycle-row separation (Lemma 2.2) with bitmasks.  A list L of distinct states such that every
triple in list order is forced positive (table T) has at most 7 occupied: row (L, len(L)-7)."""
import random
from etv_common import N

def masks(T):
    M = [[0] * N for _ in range(N)]
    for a in range(N):
        for b in range(N):
            if a != b:
                m = 0
                for x in range(N):
                    if T[a, b, x]: m |= 1 << x
                M[a][b] = m
    return M

def find_lists(M, occ, k=8, limit=50, rng=None, per_start=3):
    occ = sorted(occ); occm = 0
    for x in occ: occm |= 1 << x
    res = []; seen = set()
    starts = occ[:]
    if rng: rng.shuffle(starts)
    def dfs(seq, cand, quota):
        if len(seq) == k:
            key = frozenset(seq)
            if key not in seen:
                seen.add(key); res.append(tuple(seq)); quota[0] -= 1
            return quota[0] <= 0 or len(res) >= limit
        c = cand
        while c:
            low = c & -c; x = low.bit_length() - 1; c ^= low
            nc = cand & ~low
            for y in seq[1:] if len(seq) > 1 else []:
                pass
            # new candidate set: all pairs (seq[i], x) must be followed by positive triples
            for s in seq:
                nc &= M[s][x]
            if len(seq) + 1 + bin(nc).count('1') < k:
                continue
            if dfs(seq + [x], nc, quota):
                return True
        return False
    for s in starts:
        quota = [per_start]
        cand = occm & ~((1 << (s + 1)) - 1)   # rotate so that s is the minimum element
        dfs([s], cand, quota)
        if len(res) >= limit: break
    return res

def valid_insert(T, lst, x, p):
    new = lst[:p] + [x] + lst[p:]
    k = len(new)
    for a in range(k):
        for b in range(a + 1, k):
            if p in (a, b): continue
            tri = sorted([a, b, p])
            if not T[new[tri[0]], new[tri[1]], new[tri[2]]]:
                return None
    return new

def extend(T, lst, rng):
    lst = list(lst); changed = True
    cand = list(range(N)); rng.shuffle(cand)
    while changed:
        changed = False
        for x in cand:
            if x in lst: continue
            for p in range(len(lst) + 1):
                new = valid_insert(T, lst, x, p)
                if new is not None:
                    lst = new; changed = True; break
    return lst
