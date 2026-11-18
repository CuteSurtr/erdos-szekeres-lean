"""4x4 state geometry, adapted from the prior independent rows66.py.
No original N66 encoder/checker imports. Paths are explicit for this follow-up.
"""
import functools
import itertools as it
import pathlib

D = pathlib.Path('/home/jay/research/data/n66-20261113/p2/b13g/it1')
OLD = pathlib.Path('/home/jay/research/data/n66-20261113/p2/b12/it1')
HERE = pathlib.Path(__file__).resolve().parents[1]
WORK = pathlib.Path('/home/jay/research/data/verify309-codex-20261113/followup56')
S = sorted((p for p in it.product(range(5), repeat=4)
            if list(p) == sorted(p, reverse=True)), key=lambda p: (sum(p), p))
C = [{(a+1, b) for a, h in enumerate(p) for b in range(1, h+1)} for p in S]
assert len(S) == 70
tau = [C.index({(b, a) for a, b in c}) for c in C]
plain = [[C[t]-C[s] for t in range(70)] for s in range(70)]
ref = [[{(a,b) for a,b in plain[s][t]
         if a <= sum(h > 0 for h in S[s])+1 and b <= S[s][0]+1}
        for t in range(70)] for s in range(70)]

@functools.lru_cache(None)
def positive(a, b, c):
    for p in it.permutations(range(3)):
        x, y, z = [(a,b,c)[k] for k in p]
        if not plain[x][y] or not plain[y][z] or not plain[x][z]:
            continue
        axis = sum(p[i] > p[j] for i in range(3) for j in range(i+1,3)) % 2
        if max(v[axis] for v in plain[y][z]) > min(v[axis] for v in plain[x][y]):
            return False
    return True

def valid(test, support):
    typ, *v = test
    count = 3 if typ == 'positive' else 2
    assert len(v) == {'positive': 3, 'empty': 2, 'domain': 4}[typ]
    assert len(set(v[:count])) == count
    assert all(type(i) is int and 0 <= i < len(support) for i in v[:count])
    if typ == 'positive':
        return positive(*(support[i] for i in v))
    if typ == 'empty':
        return not ref[support[v[0]]][support[v[1]]]
    assert all(1 <= i <= 4 for i in v[2:])
    return tuple(v[2:]) not in ref[support[v[0]]][support[v[1]]]
