import sys, itertools
sys.path.insert(0, "../decomp")
from mirror import mirror_construction
M = mirror_construction(7)
# rotate by -90 deg: (x,y) -> (y,-x); mirror y->-y becomes x'->-x'
P = sorted([(y, -x) for x, y in M])
N = len(P)
assert len(set(p[0] for p in P)) == N
def o(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
X = {}
for i, j, k in itertools.combinations(range(N), 3):
    v = o(P[i], P[j], P[k]); assert v != 0
    X[(i+1, j+1, k+1)] = v > 0
bad = sum(1 for (i, j, k), v in X.items() if X[(N+1-k, N+1-j, N+1-i)] != v)
print("N", N, "mirror-identity violations:", bad)
with open("m32k7_assume.txt", "w") as f:
    idx = {t: n+1 for n, t in enumerate(itertools.combinations(range(1, N+1), 3))}
    f.write(" ".join(str(idx[t] if v else -idx[t]) for t, v in X.items()))
