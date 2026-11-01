"""Shows that the statement needs the standing general-position hypothesis of split_theorem.md section 1:
two parallel rows of 5 points (k = 5): 10 > 2^3 points, no 5 points in strictly convex position,
and (top row, bottom row) satisfies Definition 1 for z = direction (0,-1)."""
import itertools
import lemma_test as LT
A = [(x, 1) for x in range(5)]
B = [(x, 0) for x in range(5)]
z = LT.Z('dir', (0, -1))
S = A + B
strict5 = [P for P in itertools.combinations(S, 5) if LT.hull_size(P) == 5]
print("|S| =", len(S), "> 2^(5-2) = 8;  z-split (Definition 1):", LT.is_split(z, A, B),
      "; 5-subsets in strictly convex position:", len(strict5), "; general position:", LT.general_position(S))
