"""The strong / weak Delta-reduction of ETVTHY20261113 section 3 at (a, n) = (5, 6), tested by brute force on the
real 14-point FL(5,5) sets without a Pascal split (pure Python, integers only).
  weak   : S = D + R,  D has no 4-cap,                         R has no convex pentagon
  strong : S = D + R,  D has no 4-cap and no convex pentagon,  R has no convex pentagon
In a set with no 5-cap and no 5-cup a convex pentagon is a (3-cap,4-cup)-gon or a (4-cap,3-cup)-gon
(a 4-cap-free set can only contain the first kind)."""
import sys, json, itertools
def check(P):
    P = sorted(tuple(p) for p in P); n = len(P)
    det = lambda i, j, k: (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])
    sg = {t: (1 if det(*t) > 0 else -1) for t in itertools.combinations(range(n), 3)}
    def chains(L, s): return [idx for idx in itertools.combinations(range(n), L) if all(sg[idx[q], idx[q+1], idx[q+2]] == s for q in range(L - 2))]
    assert not chains(5, -1) and not chains(5, 1)
    caps4 = chains(4, -1); cups4 = chains(4, 1); caps3 = chains(3, -1); cups3 = chains(3, 1)
    m = lambda s: sum(1 << p for p in s)
    def gons(caps, cups):
        by = {}
        for c in cups: by.setdefault((c[0], c[-1]), []).append(c)
        return [m(set(c) | set(u)) for c in caps for u in by.get((c[0], c[-1]), [])]
    cap4 = sorted(set(m(c) for c in caps4))
    pent = sorted(set(gons(caps3, cups4)) | set(gons(caps4, cups3)))     # all convex pentagons of S (as point sets)
    # cross-check of the pentagon list: 5 points in convex position <=> no point inside a triangle of three others
    def convex5(idx):
        for p in idx:
            others = [q for q in idx if q != p]
            for tri in itertools.combinations(others, 3):
                a_, b_, c_ = tri
                d1 = det(*sorted((a_, b_, p))) * (1 if sorted((a_, b_, p)) == [a_, b_, p] else 1)
                # orientation test with explicit points
                def o(x, y, z): return (P[y][0]-P[x][0])*(P[z][1]-P[x][1]) - (P[y][1]-P[x][1])*(P[z][0]-P[x][0])
                s1, s2, s3 = o(a_, b_, p) > 0, o(b_, c_, p) > 0, o(c_, a_, p) > 0
                if s1 == s2 == s3: return False
        return True
    pent2 = sorted(m(idx) for idx in itertools.combinations(range(n), 5) if convex5(idx))
    assert pent == pent2, 'pentagon lists differ'
    full = (1 << n) - 1; inside = lambda S, L: any(x & S == x for x in L)
    weak = strong = 0
    for D in range(1 << n):
        R = full ^ D
        if inside(D, cap4) or inside(R, pent): continue
        weak += 1
        if not inside(D, pent): strong += 1
    return len(pent), weak, strong
for line in open(sys.argv[1]):
    d = json.loads(line); npent, weak, strong = check(d['P'])
    print(f'record {d.get("record")}: {npent} convex pentagons; Delta-reductions at (a,n) = (5,6): weak {weak}, strong {strong}', flush=True)
