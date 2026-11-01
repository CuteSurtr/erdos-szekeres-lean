# Centrally symmetric octagon-free sets: projective transfer, closing criterion, deep halves

Written proofs for `ES8SYM/README.md` §5. Each statement was re-derived in an independent review,
which found no error; the two steps it filled in are included below (Proposition 2, "only if"; Proposition 1(c)
count). Section 5 lists refuted statements, with counterexamples checked by exact computation on
`sets/c2_64points_k8.txt`.

**Setting.** S = -S is finite, in general position, 0 ∉ S, |S| = 2m. Let ℓ be a line through 0 containing no point of
S. After a rotation, ℓ is the x-axis. H = {p ∈ S : y(p) > 0}, so S = H ∪ (-H) and |H| = m.

**Fact 0.** The points of H have distinct directions from 0: if p, q ∈ H and 0, p, q were collinear, then p, q, -p
would be three collinear points of S. So H has a strict counter-clockwise (ccw) angular order θ_1 < ... < θ_m in
(0, π). For a, b, c ∈ H in ccw order, orient(a, b, c) > 0 iff b is strictly beyond the line ac as seen from 0
("outward"), and orient(a, b, c) < 0 iff b is on 0's side ("inward"). An outward (inward) j-chain is a ccw sequence
in H all of whose consecutive triples are outward (inward).

## 1. The projective map ψ and what it preserves

Let ψ(x, y) = (x/y, 1/y), the projective map [x : y : z] -> [x : z : y]. It sends ℓ to the line at infinity, the line at
infinity to the u-axis {w = 0}, and 0 to the vertical point at infinity. (Any linear map of positive determinant that
moves ℓ to the x-axis can replace the rotation; the illustration below uses the shear (x, y) -> (x, y - x/7919).)

**Proposition 1.**
(a) ψ(-p) = ρ(ψ(p)) with ρ(u, w) = (u, -w). So T = ψ(S) is mirror-symmetric about the u-axis, with ψ(H) above it.
(b) For P ⊆ H (or P ⊆ -H): P is in convex position iff ψ(P) is.
(c) For all a, b, c ∈ S: χ_T(ψa, ψb, ψc) = -χ_S(a, b, c)·sgn(y_a y_b y_c), where χ = sign of orient. So the
    chirotope of T is, up to a global sign, the chirotope of S reoriented on -H. Convex position of a set that meets
    both H and -H is not an invariant of this reorientation.
(d) The u-order of ψ(H) is the reverse ccw angular order of H. Outward chains of H correspond to cups of ψ(H), and
    inward chains to caps.
(e) *Symmetric polygons are swapped, never transported.* Let C = (p_1, ..., p_j) ⊆ H with j >= 3.
    - If C ∪ (-C) is in convex position in S, then C is an outward chain, ψ(C) is a cup above the axis, and
      ψ(C) ∪ ρψ(C) is not in convex position in T.
    - If ψ(C) ∪ ρψ(C) is in convex position in T, then ψ(C) is a cap, C is an inward chain, and C ∪ (-C) is not
      in convex position in S.

*Proof.* (a) ψ(-x, -y) = (x/y, -1/y). (b) ψ maps the open half-plane {y > 0} (resp. {y < 0}) onto {w > 0}
(resp. {w < 0}). Its singular line ℓ misses the half-plane, so on it ψ maps segments to segments and convex sets to
convex sets, and the same holds for the inverse. Hence conv(ψ(P)) = ψ(conv(P)), and extreme points correspond.
(c) In homogeneous coordinates (ψ(p), 1) = M(p, 1)/y_p, where M is the permutation matrix of [x:y:z] -> [x:z:y], with
det M = -1. So det[(ψa,1), (ψb,1), (ψc,1)] = -det[(a,1), (b,1), (c,1)]/(y_a y_b y_c).
(d) u = x/y = cot θ decreases with θ. A line αx + βy = 1 not through 0 becomes w = αu + β, and 0's side
{αx + βy < 1} becomes {w > αu + β} (multiply by w = 1/y > 0). So "inward" (middle point on 0's side of the chord)
becomes "above the chord", a cap, and "outward" becomes a cup.
(e) First claim: if C ∪ (-C) is convex, its hull is centrally symmetric, so 0 is interior and the vertices appear in
ccw angular order. The vertices with angle in (0, π) are exactly C, consecutive, and consecutive vertices turn left, so
C is outward. By (d), ψ(C) = (a_1, ..., a_j) in u-order is a cup above the axis. For 1 < i < j, a_i lies strictly below
the chord a_1 a_j and strictly above the axis, with abscissa between those of a_1 and a_j. So a_i lies in the interior
of the trapezoid a_1, a_j, ρa_j, ρa_1, and ψ(C) ∪ ρψ(C) is not in convex position.
Second claim: if D = ψ(C) and D ∪ ρD is convex, the boundary of the hull crosses the axis in two vertical edges
d–ρd, and its part above the axis is a concave chain whose vertices are exactly the points of D in u-order. So D is a
cap. By (d) C is inward, so by the first claim (contrapositive, j >= 3) C ∪ (-C) is not convex. ∎

So the mirror chain lemma (`proofs/mirror.md`), applied to T, produces only T-polygons whose preimages are not convex.
Only polygons inside one half survive the transfer. Illustration (exact, `tools/projective_check.py`,
`tools/enum_table.c`): for S = `sets/c2_64points_k8.txt` and ℓ the line y = x/7919, T = ψ(S) is a 64-point
mirror-symmetric set, (c) holds on all 249,984 ordered triples of distinct points, T has 25,739,849 convex octagons
and a largest convex subset of 14 points, and every convex polygon of T with 8 or more vertices crosses the axis.

## 2. The closing criterion

**Proposition 2.** Let p_1, ..., p_j (j >= 3) be an outward chain of H. Then the 2j points ±p_i are in convex position
iff the two closing turns are left turns: orient(p_{j-1}, p_j, -p_1) > 0 and orient(-p_j, p_1, p_2) > 0.
For j = 3, put A = p_1 × p_2, B = p_2 × p_3, C = p_1 × p_3 (all > 0). Then orient(p_1, p_2, p_3) = A + B - C,
orient(p_2, p_3, -p_1) = B + C - A and orient(-p_3, p_1, p_2) = A + C - B. So the centrally symmetric hexagon is convex
iff A, B, C satisfy the three strict triangle inequalities.

*Proof.* "If": the cyclic sequence p_1, ..., p_j, -p_1, ..., -p_j has strictly increasing angles, and every angular gap
is less than π (the gap from p_j to -p_1 is θ_1 + π - θ_j ∈ (0, π)). So the polygon is star-shaped from 0 and simple.
Since orient(-a, -b, -c) = orient(a, b, c), the turn at -p_i equals the turn at p_i. The turns at p_2..p_{j-1} are left
(the chain is outward) and the remaining two are the closing turns. A simple polygon whose turns are all left is
convex.
"Only if": suppose orient(p_{j-1}, p_j, -p_1) < 0. The direction of p_j lies in the open cone spanned by p_{j-1} and
-p_1, whose angle θ_1 + π - θ_{j-1} is below π because j >= 3; and p_j lies on 0's side of the line through p_{j-1}
and -p_1, since orient(p_{j-1}, -p_1, 0) = p_1 × p_{j-1} > 0. So p_j lies strictly inside the triangle
(0, p_{j-1}, -p_1) (not on its boundary, by general position). As 0 = (p_1 + (-p_1))/2, p_j is not an extreme point
of the 2j points. The same argument applies to p_1 and the triangle (0, -p_j, p_2). The j = 3 formulas follow by
expanding the cross products, e.g. orient(p_2, p_3, -p_1) = p_1 × p_3 + p_2 × p_3 - p_1 × p_2. ∎

Neither closing turn is implied by outwardness. Example: p_1 = (10, 1), p_2 = (0, 10), p_3 = (-1, 3). Then A = 100,
B = 10, C = 31: outward (A + B > C), but B + C < A. In the mirror case the closing turns are automatic (the closing
edges are perpendicular to the axis), which is why the mirror bound is elementary.

## 3. Deep halves: a mirror-type bound for a special class

**Lemma 3.** Let S = -S be in general position, 0 ∉ S, with no 8 points in convex position. Suppose that for some
line ℓ through 0 avoiding S, the side H has this property: for all a, b ∈ H, the origin and all points of -H lie
strictly on the same side of the line ab. Then |H| <= 28 and |S| <= 56. (For even k = 2j: |S| <= 2·C(3j-4, j-2).)

*Proof.* Let p_1..p_j be an outward chain of H. The origin is on the left of the directed line p_{j-1} -> p_j (ccw
order), so by hypothesis -p_1 is too: orient(p_{j-1}, p_j, -p_1) > 0. Likewise -p_j is on the left of p_1 -> p_2. By
Proposition 2 every outward chain closes. So H has no outward 4-chain (it would give 8 points in convex position), and
ψ(H) has no 4-cup. An 8-cap of ψ(H) would pull back by Proposition 1(b) to 8 points of H in convex position, so there
is none. ψ(H) has distinct u-coordinates (Fact 0) and no three collinear points (Proposition 1(c)). By the
Erdős–Szekeres cups–caps theorem, |H| <= C(4 + 8 - 4, 4 - 2) = 28. ∎

General position is needed: H = {(i, 1000) : i = 1..30} gives a symmetric 60-point set with a deep half and no
5 points in convex position. The class is not empty: `sets/deep42.txt` is a 42-point octagon-free set with a deep half
(checked exactly; `tools/deep_halves_check.py`). The bound 56 is not shown to be attained. The 64-point set has no
deep half (300 to 395 violating pairs in each of its 32 halves), as Lemma 3 requires.

## 4. Hull-anchored chains always close

**Proposition 4.** Let v be a vertex of conv(S) and let p_1, ..., p_j ∈ S have angles 0 < θ_1 < ... < θ_j < π,
measured counter-clockwise around 0 from the direction of v. If v, p_1, ..., p_j, -v turns left at every p_i, then the
2j + 2 points ±v, ±p_1, ..., ±p_j are in convex position.

*Proof.* The cyclic sequence v, p_1, ..., p_j, -v, -p_1, ..., -p_j has strictly increasing angles 0, θ_i, π, θ_i + π,
and every gap is in (0, π), so the polygon is star-shaped from 0 and simple. The turns at p_i are left by hypothesis,
and by central symmetry so are those at -p_i: the turn at -p_1 is orient(-v, -p_1, -p_2) = orient(v, p_1, p_2), and the
turn at -p_j is orient(-p_{j-1}, -p_j, v) = orient(p_{j-1}, p_j, -v). The turns at v and -v both equal
orient(-p_j, v, p_1). Suppose it were negative (it is nonzero by general position). The origin is on the left of
-p_j -> p_1 (orient(-p_j, p_1, 0) = p_1 × p_j > 0), and so would be v; the direction of v lies strictly inside the cone
spanned by -p_j and p_1. Hence v would lie in the triangle (0, -p_j, p_1), not on its boundary (that would make three
points of S collinear). But 0 = (p_1 + (-p_1))/2 lies in conv(S \ {v}), so v ∈ conv(S \ {v}), contradicting that v is
a vertex. A simple polygon with all turns left is convex. ∎

The angular order is needed: v = (-7, -23), p = (18, -3), (12, -1), (16, -10) turns left at every p_i, v is a hull
vertex of ±{v, p_i}, but only 6 of the 8 points are hull vertices. In an octagon-free S, Proposition 4 forbids only
those 3-cups of ψ(H) whose slopes lie between the directions ψ(v), ψ(-v); it gives no bound on |H|.

## 5. What a bound "below 66" would have to achieve, and refuted statements

A centrally symmetric octagon-free set of 64 points exists (`sets/c2_64points_k8.txt`), and sizes are even. So
"every centrally symmetric octagon-free set has fewer than 66 points" is equivalent to "the central maximum is 64",
the centrally symmetric case of ES(8) = 65. Any proof must be tight on the 64-point example. In particular:
- no argument can bound a half below 32 points. Arguments of the form "ψ(H) has no a-cup and no b-cap" need
  C(a + b - 4, a - 2) >= 32: (4, 8) [28] and (5, 5) [20] are impossible;
- in every centrally symmetric octagon-free S with at least 58 points, for every line ℓ through 0 avoiding S, H has
  an outward 4-chain: |H| >= 29 > C(8, 2) and ψ(H) has no 8-cap, so ψ(H) has a 4-cup. By Proposition 2 no such
  chain closes.

Refuted (counterexamples by exact computation, `tools/projective_check.py` on `sets/c2_64points_k8.txt`):
- *Central chain lemma* (an outward j-chain plus its antipodes is in convex position). False: the 3-chain of §2, and in
  the 64-point set each of the 32 halves contains 3,644 to 16,682 outward 4-chains, none of which closes. One of
  them: (100000, 36542), (999986000000, 999999266000), (1999995000000, 7999999917700),
  (4000000000000, 64000000000000), with orient(-p_4, p_1, p_2) < 0.
- *The mirror bound transfers* (|H| <= 28, |S| <= 58). False: |S| = 64.
- *ψ(S) is octagon-free.* False: 25,739,849 convex octagons, all crossing the axis.
- Data: in the 64-point set the longest outward chain in a half has 4 to 7 points, the longest inward chain 6 to 7,
  and the largest centrally symmetric convex polygon is a hexagon.
