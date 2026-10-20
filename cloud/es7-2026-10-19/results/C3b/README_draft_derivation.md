## Derivation of the encoding (proofs of the identities)

S: n = 3m points in general position, invariant under the rotation R by +120 degrees about
c = origin, c not in S, no two points of S on a line through c (generic symmetric
perturbation). l: a line through c avoiding S, taken as the y-axis. Then x != 0 on S.

phi(x, y) = (y/x, 1/x). In homogeneous coordinates (x, y, w) -> (y, w, x): a cyclic column
permutation, determinant +1. A point (x, y, 1) maps to (y, 1, x) = x * (y/x, 1/x, 1).

* **Labels.** X' = y/x is the slope of the line c p. Points have pairwise distinct slopes,
  so the labels 0..n-1 by increasing X' are well defined. They are the line directions
  theta in (-90, 90) degrees in increasing order.
* **R(i) = i - m mod n.** R moves a direction theta (mod 180) to theta + 120 = theta - 60
  (mod 180). This preserves the cyclic order and has order 3, so it shifts the cyclic
  order of the 3m directions by -m.
* **chi_S = chi' (-1)^(s_i+s_j+s_k).** Write det for the 3x3 determinant of the
  homogeneous rows. det(rows of S) = det(rows (y, 1, x)) = x_i x_j x_k det(rows of
  phi(S)), and sign(x_i x_j x_k) = (-1)^(s_i+s_j+s_k).
* **s_{Ri} = s_i XOR [i >= m].** For i < m the direction is in (-90, -30). Then the
  direction angle alpha of p is in (-90, -30), so alpha + 120 is in (30, 90) and x stays
  positive; or alpha is in (90, 150), so alpha + 120 is in (210, 270) and x stays
  negative. For i >= m the direction is in (-30, 90), and adding 120 always crosses
  x = 0.
* **chi'(Ri,Rj,Rk) = chi'(ijk) e_i e_j e_k.** R preserves chi_S because det R = 1.
  Combine this with the previous two identities.
* **x-order.** inv_ij = [Y'_i > Y'_j] = [1/x_i > 1/x_j].
  - If s_i = s_j, then 1/x_i > 1/x_j iff x_i < x_j.
  - If s_i = 0 and s_j = 1, then 1/x_i > 0 > 1/x_j, so inv = 1, and j precedes i.
  - If s_i = 1 and s_j = 0, then inv = 0, and i precedes j.
  - In all cases "i precedes j" = inv XOR s_i XOR s_j.
* **Prefix rule.** Take i < j < k in X' with chi' = + (j below the line ik).
  - Y'_i < Y'_k with Y'_j > Y'_k is impossible: then Y'_j < line(X'_j) < Y'_k.
  - Y'_k < Y'_i < Y'_j is impossible: then Y'_j < line(X'_j) < Y'_i.
  - That leaves the inversion sets {}, {ij}, {ij,ik}, {ij,ik,jk}, the prefixes of
    (ij, ik, jk). The case chi' = - is the mirror image.
* **s_0 = 0 WLOG.** The point reflection -I is the rotation by 180 degrees. It commutes
  with R, preserves the slopes (so the labels) and chi_S, and flips every s.
* **chi' is a signotope.** phi(S) is a point set with distinct X', labelled by X'.
* **chi_S acyclic.** S is a point set. In a uniform rank-3 oriented matroid every circuit
  has 4 elements, so acyclic = no totally cyclic 4-set. The signotope gives a
  pseudoline arrangement, hence an oriented matroid; chi_S is a reorientation of it, so
  chi_S is a uniform oriented matroid and the 4-set condition makes it acyclic.
* **No convex k-gon (KGON).** Let P be a convex k-gon in S, and p its leftmost vertex in
  the x-order of S.
  - All other vertices lie strictly to the right of p. Sorted by slope about p, they are
    q_1..q_{k-1} with chi_S(p, q_t, q_{t+1}) = + and left turns
    chi_S(q_t, q_{t+1}, q_{t+2}) = +.
  - So the chain variables C^l_p (least model) reach length k-1, which the final clause
    forbids.
  - Conversely, take points right of p with consecutive chi_S(p, ., .) = +. Slope order
    about p is linear on the right half-plane, so they are sorted by slope. With the
    middle left turns, p, q_1, .., q_{k-1} is a simple polygon with all left turns,
    i.e. convex.
  - So on a real set, the k-gon clauses are satisfiable iff there is no convex k-gon.
    This is checked on random sets by validate.py.
* **D3 (`--d3`).** Choose the gap of l so that the point on the mirror axis gets label
  (n-1)/2 (gap choice only cycles the labels; R(i) = i - m is unchanged).
  - Then the gap containing l is M-invariant, and since it contains no direction of S it
    contains the perpendicular to the axis. Moving l inside the gap changes no label and
    no s.
  - With l perpendicular to the axis, M is (x, y) -> (x, -y). So M(i) = n-1-i,
    s_{M i} = s_i, chi_S(M .) = -chi_S, and chi'(M .) = -chi'.
  - inv and o are left unconstrained: with l exactly perpendicular, mirror pairs share
    an x-coordinate.
