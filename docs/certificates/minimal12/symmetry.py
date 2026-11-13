#!/usr/bin/env python3
"""Compute the permutation image of the twelve-point signed symmetry group.

Contraction at an anchor reduces the complete search to 12 * 11 * 2
projective cyclic-order maps. All remaining equations are solved over F_2.
"""
from collections import Counter
from functools import cmp_to_key
from pathlib import Path
import argparse
import itertools
import json
import math

from verify import require, verify


def symmetries(data):
    proof = verify(data)
    labels = tuple(data['labels'])
    index = {v: i for i, v in enumerate(labels)}
    signs = {tuple(row[:3]): row[3] for row in proof['derived_chirotope']}
    triples = list(itertools.combinations(labels, 3))

    def chi(t):
        inversions = sum(t[i] > t[j] for i in range(3) for j in range(i + 1, 3))
        return signs[tuple(sorted(t))] * (-1 if inversions % 2 else 1)

    def projective_cycle(anchor):
        rest = [v for v in labels if v != anchor]
        base = rest[0]
        flips = {v: chi((anchor, base, v)) for v in rest[1:]}
        order = sorted(rest[1:], key=cmp_to_key(
            lambda p, q: -flips[p] * flips[q] * chi((anchor, p, q))))
        require(all(flips[p] * flips[q] * chi((anchor, p, q)) == 1
                    for i, p in enumerate(order) for q in order[i + 1:]),
                'The contraction rays are not in the asserted cyclic order.')
        return [base] + order

    cycles = {v: projective_cycle(v) for v in labels}
    anchor = labels[0]
    # Bit 0 is the global sign; bit 1+index[v] is the reorientation of v.
    masks = [1 | sum(1 << (1 + index[v]) for v in t) for t in triples]

    def solve(rhs):
        basis = {}
        equations = list(zip(masks, rhs)) + [(1 << (1 + index[anchor]), 0)]
        for mask, value in equations:
            while mask:
                pivot = mask.bit_length() - 1
                if pivot not in basis:
                    basis[pivot] = (mask, value)
                    break
                mask ^= basis[pivot][0]
                value ^= basis[pivot][1]
            if not mask and value:
                return None
        solution = 0
        for pivot in sorted(basis):
            mask, value = basis[pivot]
            if value ^ ((mask & solution).bit_count() % 2):
                solution |= 1 << pivot
        return solution, len(basis)

    def permutation_order(p):
        seen, lengths = set(), []
        for v in labels:
            if v in seen:
                continue
            w, length = v, 0
            while w not in seen:
                seen.add(w)
                length += 1
                w = p[w]
            lengths.append(length)
        return math.lcm(*lengths)

    accepted, candidates = [], set()
    for target in labels:
        for shift in range(11):
            for direction in (-1, 1):
                p = {anchor: target}
                p.update({v: cycles[target][(shift + direction * j) % 11]
                          for j, v in enumerate(cycles[anchor])})
                key = tuple(p[v] for v in labels)
                require(key not in candidates, 'Duplicate candidate permutation.')
                candidates.add(key)
                rhs = [int(chi(tuple(p[v] for v in t)) != chi(t)) for t in triples]
                solution = solve(rhs)
                if solution is None:
                    continue
                bits, rank = solution
                require(rank == 13, 'The gauged sign solution is not unique.')
                gamma = (-1) ** (bits & 1)
                epsilon = {v: (-1) ** ((bits >> (1 + index[v])) & 1) for v in labels}
                require(all(chi(tuple(p[v] for v in t)) ==
                            gamma * math.prod(epsilon[v] for v in t) * chi(t)
                            for t in triples), 'A signed symmetry equation fails.')
                mutated = rhs.copy()
                mutated[0] ^= 1
                require(solve(mutated) is None, 'A changed equation was accepted.')
                accepted.append({'images': list(key), 'global_sign': gamma,
                                 'element_signs': [epsilon[v] for v in labels],
                                 'order': permutation_order(p)})
    keys = {tuple(item['images']) for item in accepted}
    require(all(tuple(p[index[q[i]]] for i in range(12)) in keys
                for p in keys for q in keys), 'Accepted permutations are not closed.')
    orders = dict(Counter(item['order'] for item in accepted))
    require(len(candidates) == 264 and orders == {1: 1, 2: 3, 3: 2},
            'The claimed group invariant differs from the computation.')
    require(all(item['element_signs'] == [1] * 12 for item in accepted),
            'A nontrivial element reorientation was needed.')
    return {'verified': True, 'candidates': len(candidates),
            'permutation_group': 'S3', 'group_order': len(accepted),
            'permutation_order_distribution': orders,
            'derived_sign_table_sha256': proof['derived_sign_table_sha256'],
            'symmetries': accepted}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path, nargs='?',
                        default=Path(__file__).with_name('certificate.json'))
    args = parser.parse_args()
    print(json.dumps(symmetries(json.loads(args.certificate.read_text())), indent=2))


if __name__ == '__main__':
    main()
