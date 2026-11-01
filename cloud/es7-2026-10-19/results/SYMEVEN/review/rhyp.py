"""Referee's own exact checker for the hypotheses (H0)-(H5) of Lemma 3 and general position.

clusters: list of n+1 lists of integer points (index = cluster index j).
xs: base abscissae x_0..x_n (used only through the sign of x_a+x_b+x_c in (H3)).
Counts are returned so one can see that every relevant triple was examined.
"""
from fractions import Fraction
from rg import orient, sgn, longest_cup_cap, collinear_triples


def check(clusters, k, xs, gp=True, stop_early=False):
    n = k - 2
    mid = n // 2
    rep = {}
    allp = [p for B in clusters for p in B]
    N = len(allp)
    rep['N'] = N
    # (H0)
    rep['H0'] = len(set(p[0] for p in allp)) == N
    # (H1)
    ne = [B for B in clusters if B]
    rep['H1'] = all(max(p[0] for p in ne[i]) < min(p[0] for p in ne[i + 1]) for i in range(len(ne) - 1))
    # (H2): max inside slope < min between slope
    ins = None
    for B in clusters:
        for i in range(len(B)):
            for j in range(i + 1, len(B)):
                dx = B[j][0] - B[i][0]
                s = Fraction(B[j][1] - B[i][1], dx) if dx else None
                if s is None:
                    ins = Fraction(10 ** 30)
                elif ins is None or s > ins:
                    ins = s
    btw = None
    for a in range(n + 1):
        for b in range(a + 1, n + 1):
            for p in clusters[a]:
                for q in clusters[b]:
                    if q[0] == p[0]:
                        s = Fraction(-10 ** 30)
                    else:
                        s = Fraction(q[1] - p[1], q[0] - p[0])
                    if btw is None or s < btw:
                        btw = s
    rep['H2'] = (ins is None or btw is None or ins < btw)
    rep['H2_detail'] = (str(ins), str(btw))
    # (H3)
    h3_ok = True; h3_cnt = 0; h3_bad = None
    for a in range(n + 1):
        for b in range(a + 1, n + 1):
            for c in range(b + 1, n + 1):
                tot = xs[a] + xs[b] + xs[c]
                if tot == 0:
                    continue
                st = sgn(tot)
                for p in clusters[a]:
                    for q in clusters[b]:
                        for r in clusters[c]:
                            h3_cnt += 1
                            if sgn(orient(p, q, r)) != st:
                                h3_ok = False
                                if h3_bad is None:
                                    h3_bad = (a, b, c, p, q, r)
    rep['H3'] = h3_ok; rep['H3_count'] = h3_cnt; rep['H3_bad'] = h3_bad
    # (H4)
    h4_ok = True; h4_cnt = 0; h4_bad = None; h4_zero = 0
    for j in range(mid):
        for p in clusters[j]:
            for r in clusters[n - j]:
                sx = p[0] + r[0]
                for q in clusters[mid]:
                    if sx == 0:
                        h4_zero += 1
                        continue
                    h4_cnt += 1
                    if sgn(orient(p, q, r)) != -sgn(sx):
                        h4_ok = False
                        if h4_bad is None:
                            h4_bad = (j, p, q, r)
    rep['H4'] = h4_ok; rep['H4_count'] = h4_cnt; rep['H4_zero_sum_skipped'] = h4_zero; rep['H4_bad'] = h4_bad
    # (H5)
    h5 = True; h5d = []
    for j in range(n + 1):
        if not clusters[j]:
            h5d.append((j, 0, 0)); continue
        lc, lk = longest_cup_cap(clusters[j])
        h5d.append((j, lc, lk))
        if not (lc <= j + 1 and lk <= k - j - 1):
            h5 = False
    rep['H5'] = h5; rep['H5_detail'] = h5d
    if gp:
        bad = collinear_triples(allp)
        rep['GP'] = not bad
    rep['ALL'] = all(rep[key] for key in ['H0', 'H1', 'H2', 'H3', 'H4', 'H5']) and rep.get('GP', True)
    return rep
