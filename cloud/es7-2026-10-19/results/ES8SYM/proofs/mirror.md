# Mirror-symmetric octagon-free sets have at most 46 points

Written proofs for `ES8SYM/README.md` §4. The reduction (§1) and encoding B (§4) were re-derived in an independent
review, which found no error. Encoding A (§3) and its proof were written without access to encoding B. The bound
|S| <= 46 itself is also Lean-checked in the repository (§2).

**Claim.** Let S be a finite set in general position, invariant under a reflection, with no 8 points in convex
position. Then |S| <= 2 r + 2, where r is the largest size of a set with distinct x-coordinates, in general position,
with no 4-cap and no 8 points in convex position. By Baek's theorem r = 22 (§2), so |S| <= 46.

## 0. Conventions

orient(a, b, c) = (b - a) × (c - a). For points sorted by x, chi(a, b, c) = sign orient(a, b, c); `+` (left turn)
means b lies strictly below the line ac. A k-cup (k-cap) is a sequence of k points with increasing x whose consecutive
triples are all `+` (all `-`). For x_a < x_b < x_c, with s_ab the slope of ab,

    orient(a, b, c) = (x_b - x_a)(x_c - x_b)(s_bc - s_ab),                                                   (0.1)

and chi(a, b, c) = sign(s_bc - s_ab) = sign(s_ac - s_ab) = sign(s_bc - s_ac). A cap is the graph of a strictly
concave piecewise-linear function: every point of a cap lies on or below the line through any edge of the cap, and
every interior point lies strictly above the chord of its end points (symmetrically for cups).

**Lemma 0 (supporting-edge criterion).** Let q_1, ..., q_m (m >= 3) be distinct points, indices mod m, and
s ∈ {+1, -1}. If s·orient(q_i, q_{i+1}, q_k) > 0 for every i and every k ∉ {i, i+1}, then the q_i are in convex
position.

*Proof.* Fix i, put u = q_i - q_{i-1}, v = q_{i+1} - q_i and f(z) = s·[u × (z - q_i) + v × (z - q_i)], an affine
function with f(q_i) = 0. The hypothesis for the edges (i-1, i) and (i, i+1) gives, for every q_k ≠ q_i, one strictly
positive and one non-negative term, so f > 0 on all q_k, k ≠ i, hence on their convex hull. So q_i is not in the
convex hull of the others. ∎

## 1. The reduction |S| <= 2r + 2

Choose coordinates with the mirror on the x-axis, μ(x, y) = (x, -y). Put R = S ∩ {y > 0} and A = S ∩ {y = 0}. Then
|S| = 2|R| + |A|, and:
- (a) |A| <= 2, since three points of the axis are collinear.
- (b) R has distinct x-coordinates: if p ≠ q in R had the same x, then p, q, μ(p) would be three points on a vertical
  line.
- (c) R is in general position and has no 8 points in convex position (it is a subset of S).
- (d) **Mirror lemma.** If p_1, ..., p_j (j >= 2) in R form a cap, then the 2j points p_1..p_j, μ(p_1)..μ(p_j) are in
  convex position. *Proof.* Apply Lemma 0 with s = -1 to Q = (p_1, ..., p_j, μp_j, ..., μp_1). Edge p_i -> p_{i+1}:
  the other p_k lie strictly below its line (cap), and every μ(p_k) has height -y_k < 0 < y_k <= L(x_k). Edge
  p_j -> μp_j: orient(p_j, μp_j, z) = 2y_j(z_x - x_j) < 0 for all other z. Edge μp_{i+1} -> μp_i: orient(μa, μb, μz) =
  -orient(a, b, z), which reduces to the first case. Edge μp_1 -> p_1: symmetric to the second. ∎
  So R has no 4-cap.

Hence |R| <= r and |S| <= 2r + 2. The properties defining r are inherited by subsets, so r <= 22 follows from the
non-existence of a 23-point example.

*Remark.* `SYMMAX/README.md` proves (d) by checking that all turns have the same sign. That alone does not give
convex position for a closed polygon (a pentagram has constant turn sign); the polygon is also simple because it is
x-monotone above and below. Lemma 0 avoids the issue. The cups–caps theorem (no 4-cap, no 8-cup) gives only
r <= C(8, 2) = 28 and |S| <= 58, the bound recorded in `SYMMAX/README.md`.

## 2. Baek's theorem gives r = 22

J. Baek, *On the Erdős–Tuza–Valtr conjecture*, Eur. J. Combin. 124 (2025) 104085 (arXiv:2206.04260), proves that
every set of C(n-1, 2) + 2 points in general position with distinct x-coordinates contains a 4-cap or n points in
convex position: the case a = 4 of the Erdős–Tuza–Valtr conjecture, N(n, 4, n) = C(n-1, 2) + 1 in Baek's notation.
For n = 8 this is r <= 22. Baek formalised the theorem in Lean 4; this repository has a port, with the geometric
n = 8 statement `ErdosSzekeres.Omission.BaekGeometry.geometric_capacity22` (recorded in `docs/THIRD_PARTY.md` at the
repository root as building and passing the axiom audit). `SYMLEAN/mirror/ReductionThreeClasses.lean` formalises §1
on top of it:
`MirrorOdd.mirror_eight_line` proves |S| <= 46 for every finite set in general position that is symmetric in a line
and has no 8 points in convex position (axioms `propext`, `Classical.choice`, `Quot.sound`; see
`SYMLEAN/mirror/README.md`; not re-run here). Earlier, Balko and Valtr (Electron. Notes Discrete Math. 49 (2015))
reported N(4, 8, 8) = 22 (their notation: no 4-cap, no 8-cup, no convex octagon) from a SAT computation in the
pseudolinear model. The lower bound r >= 22 is the Erdős–Tuza–Valtr construction, and also follows from the explicit
22-point halves of the 46-point sets.

The two encodings below give two further certificates of r <= 22, independent of Baek's proof and of each other.

## 3. Encoding A (`mirror/encode.py`) and its soundness

**Lemma 2.** A set P (|P| >= 3) in general position with distinct x is in convex position iff P = U ∪ L, where U is a
cap and L a cup, both from the leftmost point a to the rightmost point b, with U ∩ L = {a, b}.
*Proof.* (<=) Lemma 0 with s = -1 on U followed by L reversed. (=>) Put U = {a, b} ∪ {p : chi(a, p, b) = -} and
L = {a, b} ∪ {p : chi(a, p, b) = +}. If u, v, w were consecutive in U with chi(u, v, w) = +, then v would lie in
conv{a, b, u, w}. So U is a cap; symmetrically L is a cup. ∎

**Corollary.** If P has no 4-cap, then P contains 8 points in convex position iff it contains an 8-cup, or a 7-cup
c_1..c_7 and a point p with x(c_1) < x(p) < x(c_7) and chi(c_1, p, c_7) = - (then U = (c_1, p, c_7)).

`encode.py n 8 out.cnf full`: points 0..n-1 in x-order; variables O(a,b,c) = [chi(a,b,c) = +] and E(k,a,c,d) =
"there is a k-cup with first point a and last two points c, d" (3 <= k <= 7). Clauses:
- (SIG) for a < b < c < d with t_1..t_4 = O(abc), O(abd), O(acd), O(bcd), and every 3-subset i < j < l of {1,2,3,4}:
  (-t_i ∨ t_j ∨ -t_l) and (t_i ∨ -t_j ∨ t_l);
- (CAP4) O(a,b,c) ∨ O(b,c,d);
- (E3) -O(a,b,c) ∨ E(3,a,b,c); (EK) -E(k-1,a,b,c) ∨ -O(b,c,d) ∨ E(k,a,c,d) for 4 <= k <= 7;
- (CUP8) -E(7,a,b,c) ∨ -O(b,c,d);
- (OCT) -E(7,a,c,d) ∨ O(a,p,d) for every a < p < d.

*Soundness.* Let p_0..p_{n-1} be a real x-sorted set in general position with no 4-cap and no 8 points in convex
position, and give every variable its intended meaning. (SIG): for each choice of three of the four triples there is a
common point and three slopes compared pairwise by the three signs (0.1); if the first and third sign equal e, the
three slopes are strictly monotone and the middle sign is e too. (CAP4) is "no 4-cap". (E3), (EK): a (k-1)-cup
ending in b, c, extended by d with a left turn, is a k-cup. (CUP8): an 8-cup is in convex position. (OCT): if
chi(a, p, d) = - for some a < p < d, then p is not on the 7-cup from a to d and the cup plus p is in convex position by
Lemma 2. So every clause holds, and UNSAT for n = 23 means r <= 22. ∎

## 4. Encoding B (`mirror/enc_rmax.py`) and its soundness

Written separately from encoding A, with variables t(i,j,k) = [orient(p_i, p_j, p_k) > 0] for i < j < k in x-order
and w(i,k,l,L) = "some L-cup starts at p_i and ends with p_k, p_l". Clauses: (S) the signotope axioms on every
4-tuple (forbid +,-,+ and -,+,- on every 3 of the 4 triples, which hold for every x-sorted point set in general
position); (C) t(ijk) ∨ t(jkl) (no 4-cap); (W) t(i,k,l) -> w(i,k,l,3) and w(i,j,k,L) ∧ t(j,k,l) -> w(i,k,l,L+1);
(8) -w(i,k,l,8); (7) w(i,k,l,7) -> t(i,x,l) for all i < x < l, x ≠ k.

*Soundness.* As in §3: a real set with no 4-cap and no convex octagon, with t set to its orientations and w to its
intended meaning, satisfies (S), (C), (W) and (8); (7) holds because a point x strictly above the chord of a 7-cup
completes a convex octagon (lower chain the cup, upper chain p_i, x, p_l). Only forcing implications are used for w.
So UNSAT for n = 23 means r <= 22. ∎

The two encodings produce different CNFs (8,521 variables and 124,939 clauses against 12,102 and 144,991), and a
review rebuilt encoding B's clause multiset from the mathematical description with a separate script.

## 5. Lower bound

`sets/mirror_46points_k8.txt` (22 mirror pairs and 2 points on the axis x = 0) and `sets/mirror46_A_S.txt` (22 pairs
and 2 points on y = 0; the half R consists of blocks of sizes 1, 2, 3, 4, 5, 7 on a convex chain, point j of block i
being (60i + j, 720i + 100i² + j²)) are mirror-symmetric, in general position, with largest convex subset 7
(`tools/run_all.sh`). Equality in |S| <= 2r + 2 is not automatic: for the second set's half R, an exact check during
the derivation of encoding A found that one axis point left of R and one right of R create a convex octagon, while
two axis points to the right of R do not.
