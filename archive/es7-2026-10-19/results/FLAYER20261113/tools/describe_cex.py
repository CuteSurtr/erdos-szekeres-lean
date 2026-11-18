"""Describe an abstract FL(5,5) configuration: states (3x3 box), levels, hole pattern."""
import sys, json, itertools
d = json.load(open(sys.argv[1])); n, sig = d['n'], d['sig']
T = list(itertools.combinations(range(n), 3)); sg = {t: (1 if c == '+' else -1) for t, c in zip(T, sig)}
Em = {}; Ep = {}; st = []
for v in range(n):
    f = [0, 0, 0]
    for u in range(v):
        em = ep = 2
        for t in range(u):
            if sg[t, u, v] < 0: em = max(em, Em[t, u] + 1)
            else: ep = max(ep, Ep[t, u] + 1)
        Em[u, v] = em; Ep[u, v] = ep
        for c in range(em - 1): f[c] = max(f[c], ep - 1)
    st.append(tuple(f))
print('in-states by point:', ' '.join(''.join(map(str, f)) for f in st))
E = [v for v in range(n) if st[v][0] == 3]; A = [v for v in range(n) if st[v][2] >= 1]
print('|E| =', len(E), '|A| =', len(A), '|X| =', len(set(E) & set(A)), '|E u A| =', len(set(E) | set(A)))
allst = [f for f in itertools.product(range(4), repeat=3) if f[0] >= f[1] >= f[2]]
print('holes:', ' '.join(''.join(map(str, f)) for f in allst if f not in st))
