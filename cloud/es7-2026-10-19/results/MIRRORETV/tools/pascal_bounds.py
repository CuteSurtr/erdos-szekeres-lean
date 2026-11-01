#!/usr/bin/env python3
"""Exact arithmetic for N_mirror(9) <= 226 and N_mirror(10) <= 316 (README.md section 6; PROOFS.md section 8)."""
from math import comb

def baek(n):            # Baek Thm 1.6 (upper bound used): N(n,4,n) <= C(n-1,2)+1
    return comb(n - 1, 2) + 1

def cc(a, b):           # cups-caps: N(n,a,b) <= C(a+b-4,a-2)
    return comb(a + b - 4, a - 2)

# identity C(n,2)-(n-2) == C(n-1,2)+1
for n in range(3, 60):
    assert comb(n, 2) - (n - 2) == baek(n)

# Pascal recursion bound U(n,a) for N(n,a,n), a>=4: U(n,4)=baek(n), U(n,a)=U(n,a-1)+cc(a,n-1)
def U(n, a):
    if a == 4:
        return baek(n)
    return U(n, a - 1) + cc(a, n - 1)

for n in range(5, 40):
    for a in range(4, n + 1):
        assert U(n, a) == comb(a + n - 4, a - 2) - (n - 2), (n, a)

r9 = U(9, 5); r10 = U(10, 5)
print("N(9,4,9) <=", baek(9), " N(9,5,8) <=", cc(5, 8), " => N(9,5,9) <=", r9)
print("N(10,4,10) <=", baek(10), " N(10,5,9) <=", cc(5, 9), " => N(10,5,10) <=", r10)
print("N_mirror(9) <= 2*N(9,5,9) =", 2 * r9)
print("N_mirror(10) <= 2*N(10,5,10)+2 =", 2 * r10 + 2)
print("cups-caps only: 2*C(10,3) =", 2 * cc(5, 9), " 2*C(11,3)+2 =", 2 * cc(5, 10) + 2)
print("general formulas j=5: C(3j-5,j-2)-(2j-3) =", comb(10, 3) - 7, " C(3j-4,j-2)-(2j-2) =", comb(11, 3) - 8)
print("lower bounds: 2^(k-2) for k=9:", 2 ** 7, "; 2^(2j-2)-C(2j-2,j-1)+2 for j=5:", 2 ** 8 - comb(8, 4) + 2)
print("ETV values E(9,5,9) =", sum(comb(7, i) for i in range(0, 4)), " E(10,5,10) =", sum(comb(8, i) for i in range(0, 4)))
# what the bound would be without Baek (cups-caps base N(n,4,n) <= C(n,2))
print("without Baek: N(9,5,9) <=", comb(9, 2) + cc(5, 8), " N(10,5,10) <=", comb(10, 2) + cc(5, 9))
