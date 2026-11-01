"""Independent exact check of the arithmetic in Corollary 7 (general k) of split_theorem.md.

E(k, a) := sum_{i=0}^{a-2} C(k-2, i)   (conjectured ETV value N(k, a, k)).
Claim: for k >= 5, all c, d >= 2 with c + d <= k - 1:
    E(k, c+1) + E(k, d+1) <= 2^(k-2),  with equality iff c + d = k - 1.
Also: which a are needed (a = c+1 or d+1), E(k,3) = k-1 (trivial cup bound),
E(k,4) = C(k-1,2)+1 (Baek), and the open cases are a in [5, k-2].
Pure integer arithmetic.
"""
from math import comb


def E(k, a):
    return sum(comb(k - 2, i) for i in range(0, a - 1))


bad = []
needed_by_k = {}
for k in range(3, 121):
    needed = set()
    for c in range(2, k):
        for d in range(2, k):
            if c + d > k - 1:
                continue
            needed.add(c + 1)
            needed.add(d + 1)
            tot = E(k, c + 1) + E(k, d + 1)
            # also the reflected form used in the file: N(k,k,d+1) = sum_{i=k-1-d}^{k-2} C(k-2,i)
            refl = sum(comb(k - 2, i) for i in range(k - 1 - d, k - 1))
            if refl != E(k, d + 1):
                bad.append(("reflection identity", k, c, d))
            if tot > 2 ** (k - 2):
                bad.append(("bound", k, c, d, tot, 2 ** (k - 2)))
            if (tot == 2 ** (k - 2)) != (c + d == k - 1):
                bad.append(("equality case", k, c, d, tot))
    needed_by_k[k] = sorted(needed)
    if k >= 3:
        if E(k, 3) != k - 1:
            bad.append(("E3", k))
        if E(k, 4) != comb(k - 1, 2) + 1:
            bad.append(("E4", k))
        if E(k, k) != 2 ** (k - 2):
            bad.append(("Ek", k))

print("violations:", bad[:20], "count", len(bad))
for k in range(3, 13):
    nd = needed_by_k[k]
    open_ = [a for a in nd if a >= 5]
    exp = list(range(3, k - 1)) if k >= 5 else []
    print(f"k={k}: needed a = {nd}  (expected [3..k-2] = {exp}: {nd == exp});  beyond Baek (a>=5): {open_}")

# The k=7 table of Theorem 5 (with N(7,5,7)=26 assumed for the (4,2)/(2,4) rows)
k = 7
print("k=7 table:")
for c in range(2, 5):
    for d in range(2, 5):
        if c + d <= 6:
            print(f"  (c,d)=({c},{d}): |A|<=E(7,{c+1})={E(7,c+1)}, |B|<=E(7,{d+1})={E(7,d+1)}, sum={E(7,c+1)+E(7,d+1)}")
print("k=8 table:")
k = 8
for c in range(2, 6):
    for d in range(2, 6):
        if c + d <= 7:
            print(f"  (c,d)=({c},{d}): sum={E(8,c+1)}+{E(8,d+1)}={E(8,c+1)+E(8,d+1)} vs 2^6=64")
