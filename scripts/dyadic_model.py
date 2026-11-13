#!/usr/bin/env python3
"""Exact coefficients of the endpoint-only repeated-doubling model."""
import json
from fractions import Fraction
from math import sqrt


def coefficient_squared(t):
    if t < 1:
        raise ValueError("Require at least one doubling")
    return Fraction(4 * 4**t * t, (2**t - 1)**2)


if __name__ == "__main__":
    print(json.dumps({
        "scope": "endpoint-only dyadic model; not a lower bound on ES(n)",
        "minimum_squared": str(Fraction(128, 9)),
        "minimizer": 2,
        "all_t_proof": "ErdosSzekeres.DyadicModel.two_scales_optimal",
        "rows": [{"doublings": t, "squared_exact": str(coefficient_squared(t)),
                  "coefficient_approx": sqrt(coefficient_squared(t))}
                 for t in range(1, 13)],
    }, indent=2))
