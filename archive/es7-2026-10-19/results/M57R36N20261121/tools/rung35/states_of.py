#!/usr/bin/env python3
"""states_of.py PTS.json|COL.json -- states I(v) of every point (exact integers) and the counts
r=#{f1=5} (B2), t=#{f1<=4} (S1), q=#{f3=0} (B1), u=#{f3>=1} (S2). Point sets: list of [x,y] integer pairs."""
import sys, json
d = json.load(open(sys.argv[1]))
if isinstance(d, dict) and 'states_in_order' in d:
    st = [tuple(s) for s in d['states_in_order']]
else:
    P = sorted(tuple(map(int, p)) for p in d)
    n = len(P)
    assert len({p[0] for p in P}) == n
    def det(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    Ecap = {}; Ecup = {}
    for v in range(n):
        for u in range(v):
            bc = 2; bu = 2
            for t in range(u):
                s = det(P[t], P[u], P[v]); assert s != 0
                if s < 0: bc = max(bc, Ecap[(t, u)] + 1)
                else: bu = max(bu, Ecup[(t, u)] + 1)
            Ecap[(u, v)] = bc; Ecup[(u, v)] = bu
    CA, CB = 3, 5
    st = []
    for v in range(n):
        labs = [(Ecap[(u, v)] - 1, Ecup[(u, v)] - 1) for u in range(v)]
        assert all(1 <= a <= CA and 1 <= b <= CB for a, b in labs), 'cap/cup bound violated'
        f = tuple(max([b for a, b in labs if a >= col] + [0]) for col in range(1, CA + 1))
        st.append(f)
    assert len(set(st)) == n
r = sum(f[0] == 5 for f in st); q = sum(f[2] == 0 for f in st)
print(sys.argv[1].split('/')[-1], 'n', len(st), 'r(B2)', r, 't(S1)', len(st) - r, 'q(B1)', q, 'u(S2)', len(st) - q,
      'x(B2&B1)', sum(f[0] == 5 and f[2] == 0 for f in st))
