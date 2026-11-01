"""Check the author's integer instances with the referee's own code only (the files are data)."""
import sys
from rg import read_points, max_convex_cupcap, max_convex_angular, convex_position_bf, count_convex_cupcap, \
    count_convex_bf, collinear_triples
from rhyp import check
from rconstruct import base_abscissae

for path, k in [(sys.argv[1], 6), (sys.argv[2], 8)]:
    rows = read_points(path)
    n = k - 2
    cl = [[] for _ in range(n + 1)]
    for (x, y, j) in rows:
        cl[j].append((x, y))
    pts = [(x, y) for (x, y, j) in rows]
    S = set(pts)
    sym = all((-x, -y) in S for (x, y) in pts)
    sizes = [len(B) for B in cl]
    # cluster-level symmetry B_{n-j} = -B_j
    csym = all(set((-x, -y) for (x, y) in cl[j]) == set(cl[n - j]) for j in range(n + 1))
    rep = check(cl, k, base_abscissae(k))
    m1, w1 = max_convex_cupcap(pts)
    m2 = max_convex_angular(pts)
    print("%s k=%d N=%d distinct=%s sym=%s clustersym=%s sizes=%s 0notin=%s" %
          (path.split('/')[-1], k, len(pts), len(S) == len(pts), sym, csym, sizes, (0, 0) not in S))
    print("   hyp:", {h: rep[h] for h in ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'GP', 'ALL']},
          "H3cnt", rep['H3_count'], "H4cnt", rep['H4_count'], "H5", rep['H5_detail'])
    print("   max convex: cupcap=%d angular=%d witness convex=%s" % (m1, m2, convex_position_bf(w1)))
    print("   counts (cup x cap DP):", count_convex_cupcap(pts))
    if k == 6:
        print("   counts (full brute force over all subsets):", count_convex_bf(pts))
    sys.stdout.flush()
