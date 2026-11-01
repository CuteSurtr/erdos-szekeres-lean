#!/usr/bin/env python3
"""Auditor A5: for the CNF-level composition of (A) with the closed P_b statement UNSAT(base + H_b + P_b), check that
sigma_A maps the hull clauses of the new point (b,0) into base + H_a (expected: onto the base's own hull clauses H_0,
because new (b,0) is old (0,1) and H_(0,1) = H_(0,0) as literal sets under the half-turn identification).
Also checks H_(0,1) == H_(0,0) directly.  usage: A5_MAP=base.json hullimage.py"""
import sys
sys.path.insert(0, '.')
import symmaps_lib as L
H0 = {frozenset(c) for c in L.hull_clauses(0)}
H01 = {frozenset(c) for c in L.hull_clauses(1)}
print("H_(0,1) == H_(0,0) as clause sets:", H01 == H0, len(H0))
ok = True
for b in range(1, 9):
    a = 17 - b
    sg = L.sigma(L.pi_A(a), +1)
    Ha = {frozenset(c) for c in L.hull_clauses(2 * a)}
    img = {frozenset((sg[abs(l)] if l > 0 else -sg[abs(l)]) for l in c) for c in L.hull_clauses(2 * b)}
    inside = img <= (H0 | Ha)
    print(f"(A) b={b} a={a}: sigma_A(H_b) subset of base hull clauses: {img <= H0}; of H_0 + H_a: {inside}")
    ok &= inside
print("OK" if ok else "FAIL")
