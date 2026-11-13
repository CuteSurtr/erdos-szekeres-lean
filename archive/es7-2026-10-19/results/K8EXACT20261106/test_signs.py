#!/usr/bin/env python3
"""Self-tests of the sign routines of k8exact.py.

1. Exact identities in Z[zeta] (k8exact.identities).
2. sign_im / sign_re against double precision on random small vectors where |value| > 1e-6 (evidence only).
3. sign_im / sign_re against PRIMEFOLD/check64/z7exact.py on random vectors with 1..200-bit entries, including
   near-cancelling ones built from a rational approximation of c (both exact; separately written code).
4. Exact zero: sign 0 exactly for a = 0 and for real/imaginary elements.
5. Refinement path: q c - p and q c^2 - p for the continued-fraction convergents p/q of c and of c^2 (denominators
   up to about 2^1000, so |value| < 2^-1000 and the precision must be doubled several times).  The known sign
   (-1)^n of x - p_n/q_n for the n-th convergent of an irrational x is the reference (exact).
usage: python3 -I test_signs.py
"""
import importlib.util
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('k8exact', HERE / 'k8exact.py')
K = importlib.util.module_from_spec(spec); spec.loader.exec_module(K)
spec = importlib.util.spec_from_file_location('pf_z7exact', HERE.parent / 'PRIMEFOLD/check64/z7exact.py')
Z = importlib.util.module_from_spec(spec); spec.loader.exec_module(Z)
rng = random.Random(20261106)
out = {'identities': K.identities()}

# 2. floats
fl = 0; skipped = 0
for _ in range(20000):
    a = tuple(rng.randint(-50, 50) for _ in range(7))
    im = sum(x * math.sin(2 * math.pi * j / 7) for j, x in enumerate(a))
    re = sum(x * math.cos(2 * math.pi * j / 7) for j, x in enumerate(a))
    for v, s in ((im, K.sign_im(a)), (re, K.sign_re(a))):
        if abs(v) < 1e-6:
            skipped += 1
            continue
        assert (v > 0) == (s > 0) and s != 0, (a, v, s)
        fl += 1
out['float_agreements'] = fl; out['float_skipped_small'] = skipped

# 3. z7exact, including near-cancellation q0 + q1 c + q2 c^2 ~ 0
T, ONE = Z.T, Z.ONE
agree = 0; skipped_uncertified = 0
for n in range(20000):
    bits = rng.randint(1, 200)
    if n % 2:
        q2 = rng.randint(-2 ** bits, 2 ** bits); q1 = rng.randint(-2 ** bits, 2 ** bits)
        q0 = -((q1 * T * ONE + q2 * T * T) // (ONE * ONE)) + rng.randint(-2, 2)   # q0 ~ -(q1 c + q2 c^2)
        try:
            zs = Z.sign_poly(q0, q1, q2)
        except ArithmeticError:
            skipped_uncertified += 1
            continue
        assert K.sign_at_c(q0, q1, q2) == zs, (q0, q1, q2)
    else:
        a = tuple(rng.randint(-2 ** bits, 2 ** bits) for _ in range(7))
        assert K.sign_im(a) == Z.sign_im_diff(a, (0,) * 7), a
        assert K.sign_re(a) == Z.sign_re_diff(a, (0,) * 7), a
    agree += 1
out['z7exact_agreements'] = agree; out['z7exact_uncertified_skipped'] = skipped_uncertified

# 4. exact zeros
assert K.sign_im(K.ZERO) == 0 and K.sign_re(K.ZERO) == 0
for _ in range(1000):
    a = tuple(rng.randint(-10 ** 30, 10 ** 30) for _ in range(7))
    r = K.mul(a, K.conj(a))                       # real
    assert K.sign_im(r) == 0 and K.sign_re(r) >= 0
    i = K.sub(a, K.conj(a))                       # purely imaginary
    assert K.sign_re(i) == 0
out['exact_zero_checks'] = 'pass'


def cf_prefix(lo_num, hi_num, den):
    """continued-fraction terms shared by lo_num/den and hi_num/den (last shared term dropped)"""
    def cf(n, d):
        t = []
        while d and len(t) < 4000:
            q, r = divmod(n, d); t.append(q); n, d = d, r
        return t
    a, b = cf(lo_num, den), cf(hi_num, den)
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]:
        k += 1
    return a[:max(k - 1, 0)]


def convergents(terms):
    p0, q0, p1, q1 = 1, 0, terms[0], 1
    yield p1, q1
    for a in terms[1:]:
        p0, q0, p1, q1 = p1, q1, a * p1 + p0, a * q1 + q0
        yield p1, q1


N = 4096; L = K.bracket(N); S = 1 << N
tests = {'c': (cf_prefix(L, L + 1, S), lambda p, q: (-p, q, 0)),
         'c^2': (cf_prefix(L * L, (L + 1) ** 2, S * S), lambda p, q: (-p, 0, q))}
before = K.STATS['refinements']; ncf = 0; maxq = 0
for name, (terms, mk) in tests.items():
    for n, (p, q) in enumerate(convergents(terms)):
        if q.bit_length() > 1000:
            break
        assert K.sign_at_c(*mk(p, q)) == (1 if n % 2 == 0 else -1), (name, n)
        ncf += 1; maxq = max(maxq, q.bit_length())
out['convergent_sign_checks'] = ncf; out['convergent_max_denominator_bits'] = maxq
out['convergent_refinements'] = K.STATS['refinements'] - before
assert out['convergent_refinements'] > 0
out['refinements_used'] = K.STATS['refinements']; out['max_bits'] = K.STATS['max_bits']
out['status'] = 'PASS'
print(json.dumps(out))
