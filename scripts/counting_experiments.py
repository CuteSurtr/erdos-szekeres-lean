#!/usr/bin/env python3
"""Explore arithmetic relaxations of HMPT. Output is NOT a certified ES bound.

Binomial coefficients and relaxed profiles use exact integers. Logarithms and
the selection of numerical minima use floating point, so results are exploratory.
"""
import json
from math import comb, log2, sqrt


def horizontal_factor(n, c):
    if n < 3 or c < 1:
        raise ValueError("Require n >= 3 and c >= 1")
    return comb(n + c - 3, c - 1)


def balanced_horizontal_product(n, k):
    """Candidate maximum under the two parity budgets; tested independently by DP."""
    if k < 4 or k % 2 or k >= n:
        raise ValueError("Require even k with 4 <= k < n")
    half = k // 2
    q, r = divmod(n - 1, half)
    return (horizontal_factor(n, q) ** (half - r)
            * horizontal_factor(n, q + 1) ** r) ** 2


def horizontal_max_dp(n, parts):
    """Exact maximization with positive c values and sum(c) <= n-1."""
    best = {0: 1}
    for _ in range(parts):
        nxt = {}
        for used, value in best.items():
            for c in range(1, n - used):
                total = used + c
                nxt[total] = max(nxt.get(total, 0), value * horizontal_factor(n, c))
        best = nxt
    return max(best.values(), default=0)


def compressed_factor(n, k):
    if k < 4 or k % 2 or k >= n:
        raise ValueError("Require even k with 4 <= k < n")
    budget = 2 * (n - 1) - k
    return comb(budget + k * (n - 2), budget)


def relaxed_profile(n, k):
    """A feasible numerical profile; NOT a realizable geometric configuration."""
    if k < 4 or k % 2 or k >= n:
        raise ValueError("Require even k with 4 <= k < n")
    a = b = (n - 1) // 2
    c = (n - 1) // (k // 2)
    d = n - 1
    horizontal = horizontal_factor(n, c) ** k
    vertical = comb(a + b - 2, a - 1) ** k
    return {
        "n": n, "k": k, "a": a, "b": b, "c": c, "d": d,
        "adjacent_budget_valid": a + b < n,
        "parity_budget_valid": (k // 2) * c < n,
        "outer_budget_valid": d < n,
        "horizontal_log2": log2(horizontal),
        "horizontal_over_n_log2_k": log2(horizontal) / (n * log2(k)),
        "vertical_log2_per_part": log2(vertical) / k,
        "geometric_realizability": "not established",
    }


def comparison(n):
    candidates = range(4, n, 2)
    # beta=8 is the elementary extraction loss in the published framework.
    # beta=4 omits a nonzero lower-order bootstrap term: a leading-order model only.
    def summarize(beta):
        coarse = min((beta * k + 2 * n * log2(n) / k, k) for k in candidates)
        compressed = min((beta * k - 3 + log2(compressed_factor(n, k)) / k, k)
                         for k in candidates)
        balanced = min((beta * k - 3 + log2(balanced_horizontal_product(n, k)) / k, k)
                       for k in candidates)
        scale = sqrt(n * log2(n))
        return {
            "extraction_coefficient": beta,
            "status": ("conditional on geometric budget interface" if beta == 8
                       else "leading-order model; omitted bootstrap error; not a finite bound"),
            "coarse": {"k": coarse[1], "exponent_error": coarse[0], "normalized": coarse[0]/scale},
            "compressed": {"k": compressed[1], "exponent_error": compressed[0], "normalized": compressed[0]/scale},
            "balanced": {"k": balanced[1], "exponent_error": balanced[0], "normalized": balanced[0]/scale},
        }
    return {"n": n, "models": [summarize(8), summarize(4)]}


if __name__ == "__main__":
    print(json.dumps({
        "status": "arithmetic exploration, not a new geometric theorem",
        "literature_check": "single-scale models do not beat HMPT v3's two-scale coefficient",
        "published_asymptotic_coefficient": 8 * sqrt(2) / 3,
        "arithmetic": "exact integer binomials; approximate logarithms and optimization",
        "comparisons": [comparison(n) for n in (32, 128, 512, 2048)],
        "relaxed_profiles": [relaxed_profile(n, k) for n, k in
                             ((128, 16), (512, 32), (2048, 64), (8192, 128))],
    }, indent=2))
