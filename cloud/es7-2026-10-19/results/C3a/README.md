# Task C3a: compact CNF for 3-fold symmetric 33-point sets without a convex 7-gon

Nothing here is a theorem. "UNSAT" means UNSAT of one specific CNF; the encodings are
tested, not formally verified. A SAT model is an abstract signotope until it is realized
with exact coordinates and re-checked.

RESULTS_PLACEHOLDER

## The encoding (`c3cnf.py`)

Setup: S has 3m points in general position, is invariant under the rotation R by +120° about
c = 0, and c is not in S. A generic symmetric perturbation keeps the order type, so we may assume
no two points are collinear with c. Pick a line l through c that avoids S, make it the y-axis,
and map S by phi(x, y) = (y/x, 1/x) to S'. Label the points 0..3m-1 by increasing X' = y/x.

Identities used (re-checked exactly, see "Validation"):
1. R acts on labels as R(i) = (i - m) mod 3m.
2. chi_S(i,j,k) = chi'(i,j,k) · (-1)^(σi+σj+σk), where chi' is the orientation of S' (x-sorted, so
   a signotope on the labels) and σi = [x_i < 0].
3. chi'(Ri,Rj,Rk) = chi'(i,j,k) εi εj εk with εi = +1 iff i < m; and σ_{Ri} = σi xor [i ≥ m], so
   σ on the orbit (r, r+m, r+2m) is (s, ¬s, s), one free bit s per orbit.
4. For i < j let inv_ij = [Y'_i > Y'_j]. Then i is left of j in S iff inv_ij xor σi xor σj. The
   inversions of a triple form a prefix of (ij, ik, jk) if chi'(ijk) = + and of (jk, ik, ij) if −;
   σi = 0, σj = 1 forces inv_ij = 1, and σi = 1, σj = 0 forces inv_ij = 0.
5. The point reflection p ↦ −p keeps the labels (X' is unchanged) and the class, and maps
   (chi', σ, inv) to (−chi', ¬σ, ¬inv). So σ0 = 0 may be assumed. This is the only symmetry
   breaking.

Variables: chi' per R-orbit of triples (1,826 for m = 11: (5456 − 11)/3 + 11, the 11 orbit
triangles being fixed by R), 11 σ bits, 528 inv bits, 528 order bits B_ij, and chi_S per orbit
(T, 1,826), tied to chi' and σ by parity clauses.

Core clauses: the signotope axiom on chi' for every 4-set (3-term monotonicity; the 327,360
clauses collapse to 109,120 distinct ones under the orbit substitution), σ0 = 0, the prefix and
forced inversion clauses, and the parity definitions of B and T.

No convex k-gon, two variants (both one-directional, so only "a real convex k-gon forces a
contradiction" is needed for soundness):

- `--gon chain` (default; the encoding the task asked for). A convex k-gon has a leftmost vertex x
  (in the x-order of S, given by the literals B). The other k−1 vertices lie in the open
  half-plane right of x, sorted by angle about x; consecutive ones are counter-clockwise about x
  and every interior turn is a left turn. Conversely, such a chain of k−1 points right of x is
  angularly increasing inside a half-plane (span < 180°) with left turns everywhere, so with x it
  is a convex k-gon. Encoding: Y[x,b,c] ← B(x,c) ∧ ccw_S(x,b,c); W2[x,a,b] ← B(x,a) ∧ Y[x,a,b];
  W(r+1)[x,b,c] ← W r[x,a,b] ∧ Y[x,b,c] ∧ ccw_S(a,b,c); W(k−2) ∧ Y ∧ left turn → false. This is
  the Szekeres–Peters angular chain about the leftmost point, with "x is left of p" as literals.
  It is frame-dependent (tied to l), so it cannot be reduced by the rotation.
- `--gon conv` (variant). A set is in convex position iff all its 4-subsets are. conv4(Q) ← one
  of the 6 convex chi_S patterns of Q; conv_r(S) ← AND over x of conv_{r−1}(S − x); for every k-set
  OR over x of ¬conv_{k−1}(S − x). One variable per R-orbit of subsets, one clause per R-orbit of
  k-sets (chi_S is R-invariant). This is the gon layer of `symcnf.py`, placed on the compact
  signotope core instead of symcnf's CC-system axioms; it does not need the x-order at all.

Sizes for m = 11, k = 7:

| CNF | variables | clauses | sha256 |
|---|---|---|---|
| `c3cnf.py 11 7` (chain) | 168,399 | 4,154,921 | `bf0e502e…` |
| `c3cnf.py 11 7 --gon conv` | 466,697 | 2,115,323 | `023f8228…` |
| `symcnf.py 33 7 3` (results/E, E2) | about 464k | about 9.5M | `4c214b4c…` |
