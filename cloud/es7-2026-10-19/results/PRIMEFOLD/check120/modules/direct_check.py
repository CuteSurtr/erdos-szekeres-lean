# Direct (definition-level) checks on my exact table, independent of modclose:
#  * convex hull vertices and their cyclic order;
#  * every run of r = 2..6 cyclically consecutive hull vertices T: is S \ T a line-module?  (all pairs of T tested
#    against all points of S \ T); for non-modules print a witness (t, u, c1, c2) with the line tu separating c1, c2;
#  * number of points of S in the open cap cut off by the chord v_i v_{i+r-1}.
import sys


def load(path):
    b = open(path, 'rb').read(); nl = b.index(b'\n'); n = int(b[:nl].split()[-1]); t = b[nl + 1:]
    assert len(t) == n ** 3
    return n, t


n, tab = load(sys.argv[1])


def O(i, j, k):
    v = tab[(i * n + j) * n + k]
    return v - 256 if v > 127 else v


hull = [i for i in range(n) if any(all(O(i, j, k) > 0 for k in range(n) if k != i and k != j) for j in range(n) if j != i)]
succ = {}
for i in hull:
    for j in range(n):
        if j != i and all(O(i, j, k) > 0 for k in range(n) if k != i and k != j):
            succ[i] = j
cyc = [hull[0]]
while succ[cyc[-1]] != cyc[0]:
    cyc.append(succ[cyc[-1]])
print('n=%d hull=%s ccw cyclic order=%s' % (n, sorted(hull), cyc))
h = len(cyc)


def module_witness(T):
    C = [c for c in range(n) if c not in T]
    for a in range(len(T)):
        for b in range(a + 1, len(T)):
            t, u = T[a], T[b]
            s0 = O(t, u, C[0])
            for c in C[1:]:
                if O(t, u, c) != s0:
                    return (t, u, C[0], c)
    return None


for r in range(2, 7):
    res = []
    for i in range(h):
        T = [cyc[(i + s) % h] for s in range(r)]
        w = module_witness(T)
        # cap: points strictly on the side of chord T[0]T[-1] that contains T[1]
        side = O(T[0], T[-1], T[1])
        cap = [k for k in range(n) if k not in (T[0], T[-1]) and O(T[0], T[-1], k) == side]
        res.append((T, w is None, len(cap), w))
    nm = sum(1 for x in res if x[1])
    print('runs of %d consecutive hull vertices: %d of %d complements are modules (size n-%d=%d); cap sizes %s'
          % (r, nm, h, r, n - r, sorted(set(x[2] for x in res))))
    for T, ok, capn, w in res[:2]:
        print('   T=%s module=%s cap_points=%d witness=%s' % (T, ok, capn, w))
