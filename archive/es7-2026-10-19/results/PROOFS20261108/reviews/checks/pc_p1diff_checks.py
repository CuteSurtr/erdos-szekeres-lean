"""pc polish-1 diff audit: small exact checks of the new claims (no heavy computation)."""
from itertools import product
import sympy as sp

# 1. word_dichotomy: premise holds for exactly 8 of the 64 words; conclusion holds for those 8;
#    PPAPPA violates the premise and is neither alternating nor has a cyclic PPP (M7 counterexample).
def alt(s):
    return all(s[(i + 1) % 6] == (not s[i]) for i in range(6))

def run(s):
    return any(s[i] and s[(i + 1) % 6] and s[(i + 2) % 6] for i in range(6))

def prem(s):
    return all(s[(i + 3) % 6] == (not s[i]) for i in range(6))

words = list(product([True, False], repeat=6))
good = [s for s in words if prem(s)]
assert len(words) == 64 and len(good) == 8
assert all((alt(s) or run(s)) and not (alt(s) and run(s)) for s in good)
P, A = True, False
w = (P, P, A, P, P, A)
assert not prem(w) and w[3] == w[0] and not alt(w) and not run(w)
print("word checks OK: 64 words, 8 satisfy the premise, PPAPPA is a counterexample to M7")

# 2. Remark pc:rem:reading: with a<b<d<a+2pi, a direction x and an antipode y+pi coincide mod 2pi
#    iff |x-y| = pi for x != y in {a,b,d} (never for x = y); exhaustive rational grid incl. boundary.
pi = sp.pi
bad = 0
cnt = 0
for j in range(1, 48):
    for k in range(j + 1, 48):
        a = sp.Integer(0)
        b = sp.Rational(j, 24) * pi
        d = sp.Rational(k, 24) * pi
        dirs = [a, b, d]
        g = [b - a, d - b, a + 2 * pi - d]
        any_gap_pi = any(sp.simplify(x - pi) == 0 for x in g)
        coincide = False
        for x in dirs:
            for y in dirs:
                t = sp.simplify((x - (y + pi)) / (2 * pi))
                if t.is_integer:
                    coincide = True
        cnt += 1
        if coincide != any_gap_pi:
            bad += 1
print("reading-remark grid:", cnt, "triples, mismatches:", bad)
