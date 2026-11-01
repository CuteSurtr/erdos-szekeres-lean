#!/usr/bin/env python3
"""Falsification test of Lemma 3 (blow-up lemma): random clustered configurations with random cluster contents
(any sets meeting the cup/cap bounds of (H5), random sizes), random centrally symmetric middle cluster, random
relative scales. Keep those satisfying (H0)-(H5) exactly; for them the lemma predicts no convex k-gon.
Also records configurations violating only (H4), to see that (H4) is what matters.
Usage: python3 random_lemma_test.py K TRIALS SEED"""
import random
import sys
from fractions import Fraction
from geom_check import orient, longest_cup_cap, largest_convex_angular, general_position_violations


def sgn(v):
    return (v > 0) - (v < 0)


def rand_cluster(rng, alpha, beta, size, box):
    for _ in range(2000):
        xs = rng.sample(range(-box, box + 1), size)
        P = [(x, rng.randint(-box, box)) for x in xs]
        if general_position_violations(P):
            continue
        cu, ca = longest_cup_cap(P)
        if cu <= alpha and ca <= beta:
            return P
    return None


def hypotheses(clusters, xs, k):
    n = k - 2
    h = n // 2
    S = [p for B in clusters for p in B]
    if len({p[0] for p in S}) != len(S):
        return "H0"
    for j in range(n):
        if max(p[0] for p in clusters[j]) >= min(p[0] for p in clusters[j + 1]):
            return "H1"
    intra_max = None
    inter_min = None
    lab = [j for j, B in enumerate(clusters) for _ in B]
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            s = Fraction(S[j][1] - S[i][1], S[j][0] - S[i][0])
            if lab[i] == lab[j]:
                intra_max = s if intra_max is None or s > intra_max else intra_max
            else:
                inter_min = s if inter_min is None or s < inter_min else inter_min
    if intra_max is not None and not intra_max < inter_min:
        return "H2"
    h4fail = False
    for a in range(n + 1):
        for b in range(a + 1, n + 1):
            for c in range(b + 1, n + 1):
                ssum = xs[a] + xs[b] + xs[c]
                for p in clusters[a]:
                    for q in clusters[b]:
                        for r in clusters[c]:
                            o = sgn(orient(p, q, r))
                            if ssum != 0:
                                if o != sgn(ssum):
                                    return "H3"
                            elif p[0] + r[0] != 0 and o != -sgn(p[0] + r[0]):
                                h4fail = True
    for j in range(n + 1):
        cu, ca = longest_cup_cap(clusters[j])
        if cu > j + 1 or ca > k - j - 1:
            return "H5"
    return "H4" if h4fail else "OK"


def main():
    k, trials, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    n, m = k - 2, k // 2
    xs = [2 * j - n + 1 for j in range(n // 2)] + [0] + [2 * j - n - 1 for j in range(n // 2 + 1, n + 1)]
    stats = {}
    max_ok = 0
    max_h4 = 0
    counterexamples = 0
    for t in range(trials):
        clusters = []
        okc = True
        outer = {}
        for j in range(n // 2):
            alpha, beta = j + 1, k - j - 1
            size = 1 if alpha == 1 else rng.randint(1, min(beta + 2, 7))
            B = rand_cluster(rng, alpha, beta, size, rng.choice([6, 20, 100]))
            if B is None:
                okc = False
                break
            outer[j] = B
        if not okc:
            stats["gen_fail"] = stats.get("gen_fail", 0) + 1
            continue
        Y = rand_cluster(rng, m - 1, m, rng.randint(1, 5), rng.choice([6, 20, 100]))
        if Y is None:
            stats["gen_fail"] = stats.get("gen_fail", 0) + 1
            continue
        # middle cluster: Y flattened and pushed to the left half, plus its negative; random scale
        cy = rng.choice([200, 1000, 5000])
        shift = (rng.randint(2, 6) * 10 ** 4, rng.randint(1, 3) * 10 ** 3)
        Yp = [(cy * p[0] - shift[0], p[1] - shift[1]) for p in Y]
        if any(abs(p[0]) <= 0 for p in Yp) or max(p[0] for p in Yp) >= 0:
            stats["gen_fail"] = stats.get("gen_fail", 0) + 1
            continue
        M = Yp + [(-x, -y) for x, y in Yp]
        Fm = rng.choice([1, 1, 1, 3, 10, 30, 100, 1000])
        M = [(Fm * x, Fm * y) for x, y in M]
        c = rng.choice([10 ** 6, 10 ** 7, 10 ** 8])
        Lam = rng.choice([10 ** 14, 10 ** 16])
        for j in range(n + 1):
            if j < n // 2:
                B = [(Lam * xs[j] + c * p[0], Lam * xs[j] ** 3 + p[1]) for p in outer[j]]
            elif j == n // 2:
                B = M
            else:
                B = [(-x, -y) for x, y in clusters[n - j]]
            clusters.append(B)
        S = [p for B in clusters for p in B]
        if len(set(S)) != len(S) or general_position_violations(S):
            stats["not_gp"] = stats.get("not_gp", 0) + 1
            continue
        hyp = hypotheses(clusters, xs, k)
        stats[hyp] = stats.get(hyp, 0) + 1
        best = largest_convex_angular(S)[0]
        if hyp == "OK":
            max_ok = max(max_ok, best)
            if best >= k:
                counterexamples += 1
                print("COUNTEREXAMPLE to Lemma 3:", S)
        elif hyp == "H4":
            max_h4 = max(max_h4, best)
            stats["H4_fail_with_kgon"] = stats.get("H4_fail_with_kgon", 0) + (best >= k)
    print("k=%d trials=%d seed=%d outcome counts=%s" % (k, trials, seed, stats))
    print("  max convex subset among configurations satisfying (H0)-(H5): %d (k-1=%d); counterexamples: %d"
          % (max_ok, k - 1, counterexamples))
    print("  max convex subset among configurations failing only (H4): %d" % max_h4)
    return 1 if counterexamples else 0


if __name__ == "__main__":
    sys.exit(main())
