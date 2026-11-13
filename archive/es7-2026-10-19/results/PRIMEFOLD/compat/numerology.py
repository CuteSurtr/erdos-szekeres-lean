#!/usr/bin/env python3
"""Independent re-check of the numerology in Lemma 0 (claim L0), written from scratch.

Model (proved by hand in the report): a finite set S invariant under the rotation R by 2*pi/m (m >= 2)
about O is a disjoint union of t orbits of size exactly m plus eps in {0,1} copies of O, so |S| = m*t + eps.
Conversely every pair (t >= 0, eps) is realised by some finite R-invariant set (take t generic orbits);
general position for odd m is also achievable, so the only extra constraint from general position is
"eps = 0 for even m" (rotation by pi maps p to -p, and O, p, -p are collinear).

We check, for every m in [2, N]:
  feasible_any(m)  := exists eps in {0,1}, t >= 0 with m t + eps = 2^(m-1)          (no general position)
  feasible_gp(m)   := same, but eps = 0 forced when m is even                         (general position)
  predicted(m)     := m odd prime, or m odd composite with 2^(m-1) = 1 mod m (base-2 Fermat pseudoprime),
                      or m a power of two
and that feasible_any == feasible_gp == predicted, plus: odd feasible m force eps = 1 (centre in S),
even feasible m force eps = 0.
Exact integer arithmetic only. For m <= BIG we use the full big integer 2^(m-1); above, pow(2, m-1, m).
"""
import sys, time

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
BIG = 6000

t0 = time.time()
# sieve of Eratosthenes (bytearray), independent primality reference
sieve = bytearray([1]) * (N + 1)
sieve[0] = sieve[1] = 0
i = 2
while i * i <= N:
    if sieve[i]:
        sieve[i * i::i] = bytearray(len(range(i * i, N + 1, i)))
    i += 1

def is_pow2(m):
    return m >= 1 and (m & (m - 1)) == 0

def residue(m):
    """2^(m-1) mod m, exact."""
    if m <= BIG:
        return (1 << (m - 1)) % m
    return pow(2, m - 1, m)

# cross-check the two residue methods on a range where both are cheap
for m in range(2, BIG + 1):
    assert (1 << (m - 1)) % m == pow(2, m - 1, m)

bad = []
psp = []           # odd composite m with 2^(m-1) = 1 mod m
feasible_list = []
centre_forced_ok = True
for m in range(2, N + 1):
    r = residue(m)                     # 2^(m-1) mod m
    total = None                       # 2^(m-1) itself is never needed beyond its residue mod m
    # eps = 0 feasible iff m | 2^(m-1); eps = 1 feasible iff 2^(m-1) = 1 (mod m) (t = (2^(m-1)-1)/m >= 0 automatically)
    f0 = (r == 0)
    f1 = (r == 1 % m)
    feas_any = f0 or f1
    feas_gp = f0 or (f1 and m % 2 == 1)
    odd_comp_psp = (m % 2 == 1) and not sieve[m] and r == 1
    if odd_comp_psp:
        psp.append(m)
    pred = (m % 2 == 1 and sieve[m]) or odd_comp_psp or is_pow2(m)
    if not (feas_any == feas_gp == pred):
        bad.append((m, feas_any, feas_gp, pred))
    if feas_any:
        feasible_list.append(m)
        # which eps values are possible?
        if m % 2 == 1:
            if f0 or not f1:           # odd m: must have eps = 1 only
                centre_forced_ok = False
        else:
            if f1 or not f0:           # even m: must have eps = 0 only (even without general position)
                centre_forced_ok = False

print(f"range m = 2..{N}; time {time.time()-t0:.1f}s")
print("mismatches feasible/predicted:", len(bad), bad[:10])
print("odd m force centre in S, even m force centre not in S (no GP needed):", centre_forced_ok)
print("first odd base-2 Fermat pseudoprimes:", psp[:22])
for e in range(3, len(str(N)) + 1):
    lim = 10 ** e
    if lim <= N + 1:
        print(f"  # odd base-2 psp < 10^{e}: {sum(1 for p in psp if p < lim)}")
print("feasible m <= 40:", [m for m in feasible_list if m <= 40])
print("k = m+1 for feasible m <= 20:", [m + 1 for m in feasible_list if m <= 20])
print("k = m+1 for first three pseudoprime m:", [p + 1 for p in psp[:3]])
print("341 = 11*31:", 11 * 31 == 341, "; 561 =", [d for d in range(2, 561) if 561 % d == 0 and sieve[d]],
      "; 645 =", [d for d in range(2, 645) if 645 % d == 0 and sieve[d]])
# even m: the only feasible ones are powers of two (and all powers of two are feasible)
ev = [m for m in feasible_list if m % 2 == 0]
print("even feasible m are exactly the powers of two <= N:",
      ev == [1 << j for j in range(1, N.bit_length()) if (1 << j) <= N])
# orbit counts in the extremal-size situation, small m
for m in [2, 3, 4, 5, 7, 8, 11, 13, 16, 17]:
    n = 1 << (m - 1)
    if m % 2:
        print(f"m={m}: |S|={n} = {m}*{(n-1)//m} + 1 (centre in S)")
    else:
        print(f"m={m}: |S|={n} = {m}*{n//m} (centre not in S)")
