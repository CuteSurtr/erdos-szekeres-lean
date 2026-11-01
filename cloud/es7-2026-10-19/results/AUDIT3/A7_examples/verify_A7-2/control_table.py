# Positive control for no_convex.c: 8 points on the parabola y = x^2 (all in convex position) plus 2 interior points.
import sys
pts = [(i, i * i) for i in range(8)] + [(3, 20), (4, 30)]
def o(p, q, r):
    v = (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0]); return (v > 0) - (v < 0)
N = len(pts); print(N)
for a in range(N):
    for b in range(N):
        print(" ".join(str(o(pts[a], pts[b], pts[c]) if len({a,b,c}) == 3 else 0) for c in range(N)))
