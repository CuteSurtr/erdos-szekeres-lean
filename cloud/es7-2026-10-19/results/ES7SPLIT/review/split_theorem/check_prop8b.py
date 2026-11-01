import os
import sys
from itertools import combinations
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from igeom import orient, in_convex_position, general_position
from splits_ind import load
S = load(sys.argv[1])
n = len(S)
# hull vertices: p is a hull vertex iff not inside any triangle of others (general position)
from igeom import in_triangle
hull = [p for p in S if not any(in_triangle(p, a, b, c) for a, b, c in combinations([q for q in S if q != p], 3))]
print('n', n, 'general position', general_position(S), 'hull vertices', len(hull))
for v in hull:
    rest = [q for q in S if q != v]
    best = 0
    has6 = False
    for T in combinations(rest, 5):
        if in_convex_position(list(T) + [v]):
            has6 = True
            break
    print('hull vertex', v, 'on a convex hexagon:', has6)
