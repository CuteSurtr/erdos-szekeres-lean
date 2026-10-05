#!/usr/bin/env python3
"""Search the proved HMPT path formula, with exact integer density checks.

The symbolic theorem is Lean-checked. Numerical instances produced by this
Python program are not separate kernel certificates or a published improvement.
"""
import argparse
import json
from math import comb


def support_product_bound(n, r):
    if n < 4 or r < 1:
        raise ValueError("Require n >= 4 and r >= 1")
    budget = 2 * (n - 1) + r
    vertical = (r + 1) * (n - 1) + 2 * r
    return (1 << vertical) * comb(budget + r * (n - 2), budget)


def product_exponent(n, r):
    length = 2 * (r + 3)
    clog_bound = (support_product_bound(n, r) - 1).bit_length()
    return max(4 * (r + 3), (2 * length * length + length + 1 + clog_bound) // r + 1)


def check_density(n, r, exponent):
    """Independently check the exact hypothesis of HMPT.finite_product_bound."""
    size = 1 << exponent
    length = 2 * (r + 3)
    threshold = size ** (r + 3) * (size ** 3 * support_product_bound(n, r))
    return (4 ** length <= size and
            2 * threshold * comb(4 ** length, length) < comb(size, length))


def search(n, max_regions):
    if max_regions < 1:
        raise ValueError("max_regions must be positive")
    exponent, regions = min((product_exponent(n, r), r)
                            for r in range(1, max_regions + 1))
    verified = check_density(n, regions, exponent)
    if not verified:
        raise ArithmeticError("Computed exponent failed the independent density check")
    return {"n": n, "best_regions_in_search": regions,
            "exponent": exponent, "exact_density_check": verified}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, nargs="+", default=[64, 128, 256, 512, 1024, 2048])
    parser.add_argument("--max-regions", type=int, default=128)
    args = parser.parse_args()
    result = {
        "formal_theorem": "ErdosSzekeres.HMPT.integer_product_bound",
        "numeric_instances_kernel_checked": False,
        "arithmetic": "exact Python integers; independently checked binomial density inequality",
        "scope": "bounded parameter search; no claim of global parameter optimality or improvement over HMPT 2020",
        "region_search": [1, args.max_regions],
        "results": [search(n, args.max_regions) for n in args.n],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
