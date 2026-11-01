#!/usr/bin/env python3
"""Independent recomputation of the variable classes of a zcnf.py mirror map from the README's identities only
(group: chi(sigma T) = -chi(T) on point triples, +chi(T) on Z-triples; pair identity: chi(Z,p,q) = chi(R,L,q) for
p in pair {L,R}, q a point outside the pair).  Signed BFS (not a union-find), conflict detection, then comparison
with the map: same partition, consistent relative signs, class count equal to the closed formula
  (C(N,3) - t*axis)/2 + t*axis - C(t,2) + [axis == 2],
and variable numbers assigned in order of first appearance (lexicographic order of triples).
usage: myuf.py MAP.json t axis"""
import itertools, json, sys
from math import comb
from collections import defaultdict, deque


def perm_sign(t):
    a, b, c = t
    return -1 if ((a > b) + (a > c) + (b > c)) % 2 else 1


def srt(t):
    return tuple(sorted(t)), perm_sign(t)


def main():
    mp, t, axis = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    NP = 2 * t; N = NP + axis; Z = N
    sig = lambda i: i if i >= NP else i ^ 1
    zero = {tuple(sorted((Z, 2 * o, 2 * o + 1))) for o in range(t)}
    trip = [T for T in itertools.combinations(range(N + 1), 3) if T not in zero]
    adj = defaultdict(list)          # edge (T, U, s): chi(T) = s chi(U)

    def edge(T, U, s):
        adj[T].append((U, s)); adj[U].append((T, s))

    for T in trip:
        img = tuple(sig(x) for x in T)
        U, ps = srt(img)                       # chi(img) = ps chi(U)
        eps = 1 if Z in T else -1              # chi(img) = eps chi(T)
        edge(U, T, ps * eps)
    for o in range(t):
        L, Rr = 2 * o, 2 * o + 1
        for p in (L, Rr):
            for q in range(N):
                if q in (L, Rr):
                    continue
                A, sa = srt((Z, p, q))         # chi(Z,p,q) = sa chi(A)
                B, sb = srt((Rr, L, q))        # chi(R,L,q) = sb chi(B)
                edge(A, B, sa * sb)
    cls, sgn = {}, {}
    ncls = 0
    conflicts = 0
    for T in trip:                             # lexicographic order
        if T in cls:
            continue
        ncls += 1
        cls[T] = ncls; sgn[T] = 1
        dq = deque([T])
        while dq:
            X = dq.popleft()
            for Y, s in adj[X]:
                if Y not in cls:
                    cls[Y] = ncls; sgn[Y] = s * sgn[X]; dq.append(Y)
                elif sgn[Y] != s * sgn[X]:
                    conflicts += 1
    formula = (comb(N, 3) - t * axis) // 2 + t * axis - comb(t, 2) + (1 if axis == 2 else 0)
    info = json.load(open(mp))
    m = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
    assert set(m) == set(trip), "map triple set differs from nonzero triples"
    # partition and sign comparison
    rel = {}
    bad_part = bad_sign = 0
    for T in trip:
        v, s = m[T]
        key = cls[T]
        if key in rel:
            if rel[key][0] != v:
                bad_part += 1
            elif rel[key][1] != s * sgn[T]:
                bad_sign += 1
        else:
            rel[key] = (v, s * sgn[T])
    inj = len({v for v, _ in rel.values()}) == len(rel)
    numbering_ok = all(rel[k][0] == k for k in rel)
    print(json.dumps({"map": mp.split("/")[-1], "t": t, "axis": axis, "triples": len(trip), "my_classes": ncls,
                      "formula": formula, "map_classes": info["X_vars"], "bfs_conflicts": conflicts,
                      "partition_mismatch": bad_part, "sign_mismatch": bad_sign, "class_map_injective": inj,
                      "numbering_first_appearance": numbering_ok}))


if __name__ == "__main__":
    main()
