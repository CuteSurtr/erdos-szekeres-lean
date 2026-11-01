#!/usr/bin/env python3
"""Independent re-check of the size-compatibility claim, written from scratch 2026-11-02.

Claim (arithmetic part): with m = k-1 and N = 2^(k-2) = 2^(m-1),
   N mod m in {0, 1}  <=>  m is a power of 2 (m even)  or  2^(m-1) = 1 mod m (m odd),
and for odd m the second case holds for every odd prime and for the base-2 Fermat pseudoprimes
341, 561, 645, 1105, ... ; in particular m = 341 = 11*31 (k = 342) qualifies.

Everything below is exact integer arithmetic. Three independent evaluations of 2^(m-1) mod m are compared:
  (1) my own right-to-left square-and-multiply,   (2) the exact big integer 2**(m-1) reduced mod m,
  (3) a CRT route: reduce mod each prime-power factor of m (own trial-division factoring) and recombine.
No code from the literature notes is used.
"""
import sys

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000          # check 1 <= m < LIMIT
EXT_LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else 200000    # cheaper extended scan (methods 1 and 3 only)


def modpow_own(base, exp, mod):
    """Right-to-left binary exponentiation, no use of pow()."""
    if mod == 1:
        return 0
    result, b, e = 1, base % mod, exp
    while e > 0:
        if e & 1:
            result = (result * b) % mod
        b = (b * b) % mod
        e >>= 1
    return result


def sieve(n):
    """Sieve of Eratosthenes: is_prime[i] for 0 <= i < n."""
    is_p = bytearray([1]) * n
    is_p[0:2] = b"\x00\x00"[: min(2, n)]
    i = 2
    while i * i < n:
        if is_p[i]:
            is_p[i * i :: i] = bytearray(len(range(i * i, n, i)))
        i += 1
    return is_p


def factor(n):
    """Trial division; returns list of (p, e)."""
    out, d = [], 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            out.append((d, e))
        d += 1 if d == 2 else 2
    if n > 1:
        out.append((n, 1))
    return out


def crt_pow2_minus1(m):
    """2^(m-1) mod m via CRT over the prime-power factors of m (independent route)."""
    if m == 1:
        return 0
    x, M = 0, 1
    for p, e in factor(m):
        q = p ** e
        r = modpow_own(2, m - 1, q)
        # combine x mod M with r mod q (M, q coprime)
        # find t with x + M*t = r (mod q)
        inv = None
        for t in range(q):                       # q < LIMIT, brute-force inverse is fine and independent of pow(-1)
            if (M * t) % q == 1 % q:
                inv = t
                break
        assert inv is not None
        t = ((r - x) * inv) % q
        x, M = x + M * t, M * q
    assert M == m
    return x % m


def is_power_of_two(n):
    if n < 1:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1


def main():
    is_p = sieve(max(LIMIT, EXT_LIMIT) + 1)
    lines = []
    say = lines.append

    # ---------- spot facts from the evidence ----------
    say("== spot facts ==")
    say(f"341 = 11*31: {11 * 31 == 341}; factor(341) = {factor(341)}")
    say(f"2^10 = {2 ** 10}; 2^10 mod 11 = {2 ** 10 % 11}; 2^10 mod 31 = {2 ** 10 % 31}; 2^10 - 1 = 1023 = 3*341: {1023 == 3 * 341}")
    say(f"2^340 mod 341: own={modpow_own(2, 340, 341)}  bigint={(2 ** 340) % 341}  via (2^10)^34: {((2 ** 10) % 341) ** 34 % 341}")
    t, r = divmod(2 ** 340, 341)
    say(f"2^340 = 341*t + r with r = {r}; t has {len(str(t))} digits")
    say(f"2^340 mod 11 = {modpow_own(2,340,11)}, mod 31 = {modpow_own(2,340,31)}")

    # ---------- full scan 1 <= m < LIMIT, three methods ----------
    say("")
    say(f"== scan 1 <= m < {LIMIT}: N = 2^(m-1), compatible iff N mod m in {{0,1}} ==")
    compat = []
    mismatches = 0
    for m in range(1, LIMIT):
        a = modpow_own(2, m - 1, m)
        b = (2 ** (m - 1)) % m
        c = crt_pow2_minus1(m)
        if not (a == b == c):
            mismatches += 1
            say(f"  MISMATCH m={m}: own={a} bigint={b} crt={c}")
        # note: for m = 1 every residue is 0 (and 0 == 1 mod 1)
        if b in (0, 1 % m):
            compat.append(m)
    say(f"method mismatches: {mismatches}")
    even = [m for m in compat if m % 2 == 0]
    odd = [m for m in compat if m % 2 == 1]
    pow2_in_range = [2 ** a for a in range(1, 64) if 2 ** a < LIMIT]
    say(f"even compatible m: {even}")
    say(f"powers of two 2..{LIMIT - 1}: {pow2_in_range}; equal: {even == pow2_in_range}")
    odd_primes = [m for m in range(3, LIMIT, 2) if is_p[m]]
    odd_compat_primes = [m for m in odd if m > 1 and is_p[m]]
    odd_compat_composites = [m for m in odd if m > 1 and not is_p[m]]
    say(f"number of odd primes < {LIMIT}: {len(odd_primes)}; all compatible: {odd_compat_primes == odd_primes}")
    say(f"odd compatible m that are neither 1 nor prime (base-2 pseudoprimes): {odd_compat_composites}")
    for n in odd_compat_composites:
        fs = factor(n)
        sqf = all(e == 1 for _, e in fs)
        # order of 2 mod p for each p | n
        orders = []
        for p, _ in fs:
            o, x = 1, 2 % p
            while x != 1:
                x = (x * 2) % p
                o += 1
            orders.append((p, o, (n - 1) % o == 0))
        carm = sqf and all((n - 1) % (p - 1) == 0 for p, _ in fs) and len(fs) >= 2
        say(f"  {n} = {' * '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in fs)}; squarefree={sqf}; "
            f"(p, ord_p(2), ord | n-1) = {orders}; Carmichael(Korselt)={carm}")
    claimed = [341, 561, 645, 1105, 1387, 1729, 1905, 2047, 2465, 2701, 2821]
    say(f"literature-notes list (NOTES.md): {claimed}; equal to computed: {odd_compat_composites == claimed}")
    say(f"claim's prefix (341, 561, 645, 1105) is the start of the computed list: {odd_compat_composites[:4] == [341, 561, 645, 1105]}")
    say(f"is m = 1 compatible (k = 2)? {1 in compat}  <- odd, neither prime nor pseudoprime")
    say(f"k values for even compatible m: {[m + 1 for m in even]}")

    # ---------- characterisation sanity: odd m > 1 can never give residue 0 ----------
    zero_odd = [m for m in range(3, LIMIT, 2) if modpow_own(2, m - 1, m) == 0]
    say(f"odd m > 1 with 2^(m-1) = 0 mod m: {zero_odd}")
    one_even = [m for m in range(2, LIMIT, 2) if modpow_own(2, m - 1, m) == 1]
    say(f"even m with 2^(m-1) = 1 mod m: {one_even}")

    # ---------- extended scan (own modpow + CRT), counts only ----------
    say("")
    say(f"== extended scan {LIMIT} <= m < {EXT_LIMIT} (own square-and-multiply; spot CRT on every pseudoprime) ==")
    ext_even_bad, ext_prime_bad, ext_psp = [], [], []
    for m in range(LIMIT, EXT_LIMIT):
        r = modpow_own(2, m - 1, m)
        ok = r in (0, 1)
        if m % 2 == 0:
            if ok != is_power_of_two(m):
                ext_even_bad.append(m)
        else:
            if is_p[m] and not ok:
                ext_prime_bad.append(m)
            if (not is_p[m]) and ok:
                ext_psp.append(m)
                assert crt_pow2_minus1(m) == r
    say(f"even m where (compatible) != (power of two): {ext_even_bad}")
    say(f"odd primes that fail: {ext_prime_bad}")
    say(f"number of odd composite compatible m in range: {len(ext_psp)}; first 10: {ext_psp[:10]}")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
