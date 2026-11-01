#!/usr/bin/env python3
"""Claim 1 (signotope axioms) and the `mono` clause pattern, checked independently.
(a) The clause pattern produced for a length-4 sequence (forbid +-+ and -+- on every 3 of 4 positions) excludes
    exactly the sign vectors with >= 2 sign changes (all 16 vectors).
(b) For random point sets sorted by random generic directions (exact integers), every 4-subset's orientation sequence
    o(ijk), o(ijl), o(ikl), o(jkl) has <= 1 sign change, with o computed in the ORIGINAL frame; also the same with the
    sequence computed in the rotated frame (sanity: rotation invariance), and a negative control (sorted by a
    different direction than the labels) to make sure the test can fail.
(c) Symbolic: o(n+1-k, n+1-j, n+1-i) = -o(i,j,k) for symmetric sets."""
import itertools, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv import det, dot, neg, general_position

# (a)
def mono_clauses(seq):
    cl = []
    for a, b, c in itertools.combinations(range(len(seq)), 3):
        cl.append([-seq[a], seq[b], -seq[c]]); cl.append([seq[a], -seq[b], seq[c]])
    return cl

ok_a = 0
for bits in itertools.product([False, True], repeat=4):
    seq = [1, 2, 3, 4]
    val = {i + 1: bits[i] for i in range(4)}
    sat = all(any(val[l] if l > 0 else not val[-l] for l in c) for c in mono_clauses(seq))
    changes = sum(1 for i in range(3) if bits[i] != bits[i + 1])
    assert sat == (changes <= 1), (bits, sat)
    ok_a += 1
print("(a) mono pattern exact on all", ok_a, "sign vectors")

# (b)
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
tests = viol = ctrl_viol = 0
for trial in range(400):
    n = rng.randint(5, 9)
    span = rng.choice([3, 10, 1000])
    P = list({(rng.randint(-span, span), rng.randint(-span, span)) for _ in range(n)})
    if len(P) < 5 or not general_position(P):
        continue
    while True:
        d = (rng.randint(-50, 50), rng.randint(-50, 50))
        if d != (0, 0) and len({dot(d, p) for p in P}) == len(P):
            break
    S = sorted(P, key=lambda p: dot(d, p))
    o = lambda i, j, k: det(S[i], S[j], S[k]) > 0
    # rotated frame (x' = d.p, y' = d_perp.p) -- proper rotation-scaling
    dp = (-d[1], d[0])
    T = [(dot(d, p), dot(dp, p)) for p in S]
    o2 = lambda i, j, k: det(T[i], T[j], T[k]) > 0
    for i, j, k, l in itertools.combinations(range(len(S)), 4):
        seq = [o(i, j, k), o(i, j, l), o(i, k, l), o(j, k, l)]
        seq2 = [o2(i, j, k), o2(i, j, l), o2(i, k, l), o2(j, k, l)]
        assert seq == seq2
        tests += 1
        if sum(1 for x in range(3) if seq[x] != seq[x + 1]) > 1:
            viol += 1
    # negative control: random labelling (not sorted) should violate sometimes
    R = S[:]; rng.shuffle(R)
    for i, j, k, l in itertools.combinations(range(len(R)), 4):
        seq = [det(R[i], R[j], R[k]) > 0, det(R[i], R[j], R[l]) > 0, det(R[i], R[k], R[l]) > 0, det(R[j], R[k], R[l]) > 0]
        if sum(1 for x in range(3) if seq[x] != seq[x + 1]) > 1:
            ctrl_viol += 1
print(f"(b) 4-subsets tested {tests}, violations {viol}; negative control violations (shuffled labels) {ctrl_viol}")

# (c)
cnt = 0
for trial in range(200):
    m = rng.randint(3, 8)
    P = []
    for _ in range(m):
        p = (rng.randint(-99, 99), rng.randint(-99, 99)); P += [p, neg(p)]
    if len(set(P)) != len(P) or (0, 0) in P or not general_position(P):
        continue
    d = (1000003, 1)
    S = sorted(P, key=lambda p: dot(d, p)); n = len(S)
    assert all(S[n - 1 - i] == neg(S[i]) for i in range(n))
    for i, j, k in itertools.combinations(range(1, n + 1), 3):
        a = det(S[i - 1], S[j - 1], S[k - 1]) > 0
        b = det(S[n - k], S[n - j], S[n - i]) > 0
        assert a != b
        cnt += 1
print("(c) o(n+1-k,n+1-j,n+1-i) = -o(i,j,k) on", cnt, "triples")
