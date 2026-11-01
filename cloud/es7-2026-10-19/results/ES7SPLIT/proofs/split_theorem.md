# Split theorem for heptagon-free sets (written proof)

Paths in this file are relative to the `ES7SPLIT` directory (`data/`, `logs/`, `tools/`, `review/`), except those
beginning with `docs/` or `cloud/`, which are from the repository root.

Status: written proof, checked by an independent review on 1 November 2026 (no error found; see
`review/README.md`). It uses one published theorem as a black box:
Baek's theorem (Erdős–Tuza–Valtr case a = 4: any C(n−1,2)+2 points in the plane, no three on a line and no
two with the same x-coordinate, contain 4 points on a concave-downward curve or n points in convex position;
J. Baek, arXiv:2206.04260, Eur. J. Combin. 124 (2025) 104085, Lean formalization jcpaik/erdos-tuza-valtr,
ported in this repository per docs/THIRD_PARTY.md). For n = 7 it says: a set with no 4-cap and no 7 points in
convex position has at most 16 points. The Lean port states the theorem for abstract configurations; its
instantiation at n = 7 is Lean-checked in `review/equivalence/BaekSeven.lean`. The step from the abstract form to
real point sets is not Lean-checked for n = 7 (the repository's bridge covers the octagon case only), so for real point
sets this proof relies on the published paper.

Everything else is elementary. Randomized exact tests of Lemmas 2–3 and Corollary 4 are in §7.

## Summary

Write gon(X) for the largest number of points of X in convex position.

* **Theorem 5.** Let S be a set of at least 33 points in general position with gon(S) ≤ 6. If S = A ∪ B is a
  z-split (Definition 1; this generalises Baek–Balko's "deep below" to any point z outside conv(S), finite or at
  infinity) with |A| ≥ 2 and |B| ≥ 2, then one part has at most 6 points and is in convex position (a z-cap below
  or a z-cup above), and the other part has at least |S| − 6 ≥ 27 points and contains no z-5-cap (respectively
  no z-5-cup). In the normal-form frame of Lemma 0 that larger part is a set with no 5-cap (after reflection if
  needed) and no 7 points in convex position.
* **Corollary.** If the Erdős–Tuza–Valtr bound N(7,5,7) ≤ 26 holds, no set of ≥ 33 points without a convex
  7-gon has a z-split with both parts of size ≥ 2.
* **Theorem 6 (equivalence).** A 33-point set in general position without a convex 7-gon having such a split
  exists **iff** N(7,5,7) ≥ 27.
* **Corollary 7.** The same argument for general k: splits of k-gon-free sets with more than 2^(k−2) points are
  excluded by the ETV cases (k, a, k) with 5 ≤ a ≤ k − 2 (none open for k ≤ 6; only a = 5 for k = 7; a = 5, 6
  for k = 8).

## 1. Definitions

S is a finite set of points in the plane in general position (no three collinear).
orient(a,b,c) = det(b − a, c − a); it is positive iff a, b, c is a counter-clockwise triple.

**Points outside S.** A *point outside S* is either a point z ∈ R² \ conv(S) ("finite"), or a nonzero vector d,
read as the point at infinity reached by travelling in direction d ("direction"). For a line L and such a z not on
L (for a direction: d not parallel to L) let H_z(L) be the open half-plane of L that contains z (finite case), or
that contains p + t·d for all large t (direction case; independent of p). In formulas, for a line L = ab:

  q ∈ H_z(ab)  ⇔  sgn orient(a, b, q) = sgn orient_h(a, b, z) ≠ 0,

where orient_h(a,b,z) = orient(a,b,z) for finite z and orient_h(a,b,d) = det(b − a, d) for a direction
(indeed orient(a, b, p + t d) = orient(a,b,p) + t·det(b − a, d)).

**Definition 1 (z-split).** A partition S = A ∪ B into nonempty parts is a *z-split* (A the upper part, B the
lower part) if

* (S1) for all distinct a, a' ∈ A and all b ∈ B: b ∈ H_z(aa');
* (S2) for all distinct b, b' ∈ B and all a ∈ A: a lies in the open half-plane of bb' **not** containing z
  (i.e. a ∉ H_z(bb') and a ∉ bb').

(S1) and (S2) include that z lies on no line through two points of A (if B ≠ ∅) or of B (if A ≠ ∅).
For z the downward vertical direction (0, −1), (S1) says that B lies below every line spanned by A and (S2) that
A lies above every line spanned by B. Baek–Balko (SoCG 2025, §4) call this "B deep below A" when in addition every
point of B has smaller y-coordinate than every point of A; that extra condition is not used here.

**z-order.** For finite z outside conv(S) there is a line through z with S strictly on one side, so the directions
from z to the points of S lie in an open half-plane. Put p <_z q iff orient_h(p, q, z) < 0 (for finite z this is
orient(z, p, q) < 0: q is clockwise from p as seen from z; for the direction (0,−1) it is x(p) < x(q)).
If z lies on no line through two points of a subset X, then <_z is a strict total order on X.

**z-caps and z-cups.** A sequence q_1 <_z … <_z q_m (z on no line q_i q_k) is a *z-cup* if q_j ∈ H_z(q_i q_k)
for all i < j < k, and a *z-cap* if q_j is in the opposite open half-plane for all i < j < k. Sets of at most two
points are both. cap_z(X), cup_z(X) are the largest sizes of a z-cap, z-cup contained in X.
For z = (0, −1) these are the usual caps and cups (x-sorted; a cup is a lower convex chain).

**ETV numbers.** For a, b ≥ 2 let N(7, a, b) be the largest size of a set X in general position with distinct
x-coordinates, no a-cap, no b-cup and gon(X) ≤ 6. Facts used:

* (F1) N(7,2,7) = 1 (two points form a 2-cap). Symmetrically N(7,7,2) = 1.
* (F2) N(7,3,7) ≤ 6: with no 3-cap every triple is a cup triple, so X is a cup, hence in convex position
  (a cup of m points has the same labelled orientations as m points on a circular arc, all triples positive in
  x-order, and convex position is determined by the labelled orientations), so |X| ≤ 6. Symmetrically
  N(7,7,3) ≤ 6.
* (F3) N(7,4,7) ≤ 16 (Baek's theorem with n = 7: C(6,2) + 2 = 17). The reflection (x, y) ↦ (x, −y) keeps
  general position, distinct x-coordinates and convex position and swaps caps with cups, so N(7,7,4) ≤ 16 and
  N(7,7,5) = N(7,5,7).
* (F4) N(7,5,7) ≥ 26 (the Erdős–Tuza–Valtr construction; an explicit instance, by exact computation: the 26
  leftmost points of `data/classical32.txt` have no 5-cap and gon 6, `review/equivalence/gluing_check.txt`); the
  ETV conjecture says N(7,5,7) = 26. It is open.

## 2. Normal form

**Lemma 0.** Let X be a finite set in general position and z a point outside X (finite z ∉ conv(X), or a
direction). There is an injective map φ, defined on an open half-plane Ω ⊇ conv(X) (on R² for a direction), such
that for all points of X:

* (a) φ maps every segment in Ω onto a segment; hence a subset Y ⊆ X is in convex position iff φ(Y) is;
* (b) sgn orient(φp, φq, φr) = sgn orient(p, q, r);
* (c) p <_z q iff x(φp) < x(φq) (ties correspond to ties);
* (d) for p ≠ r in X and q ∉ pr, with z ∉ pr: q ∈ H_z(pr) iff φ(q) lies below the line φ(p)φ(r), which is
  not vertical.

Consequently z-caps / z-cups of Y ⊆ X are exactly the sets mapped to caps / cups, and (A, B) is a z-split of X
iff φ(B) lies below every line spanned by φ(A) and φ(A) lies above every line spanned by φ(B).

*Proof.* Direction case: let φ be the rotation taking d to a positive multiple of (0, −1). It preserves
orientation; det(d, q − p) = |d|·(x(φq) − x(φp)), and p <_z q iff orient_h(p,q,d) = det(q − p, d) < 0 iff
det(d, q − p) > 0, which gives (c); H_d(L) is the side of L into which d points, which after the rotation is the
lower side of the (non-vertical, since d ∦ L) line φ(L), giving (d).

Finite case. Since conv(X) is compact and convex and z ∉ conv(X) there is a vector n with n·x > n·z for all
x ∈ conv(X). Put w(p) = n·(p − z) (so w > 0 on conv(X); Ω = {w > 0}), u = (−n_y, n_x), and

  φ(p) = ( −u·(p − z) / w(p),  −1 / w(p) ).

In homogeneous coordinates (p, 1) ↦ M(p, 1) = (−u·(p − z), −1, w(p)) = w(p)·(φ(p), 1) with
M = [[−u_x, −u_y, u·z], [0, 0, −1], [n_x, n_y, −n·z]] and det M = −u_x n_y + u_y n_x = n_x² + n_y² > 0.
φ is a bijection from Ω onto {Y < 0} (given (X, Y) with Y < 0, w = −1/Y and u·(p − z) = −Xw, n·(p − z) = w
determine p).

(a) For p, q ∈ Ω and p_t = (1 − t)p + tq, both the numerator vector F(p) = (−u·(p − z), −1) and w are affine,
so φ(p_t) = [(1 − t)w(p)φ(p) + t w(q)φ(q)] / [(1 − t)w(p) + t w(q)] = (1 − s)φ(p) + sφ(q) with
s = t w(q)/((1 − t)w(p) + t w(q)), which increases from 0 to 1. So φ([p, q]) = [φp, φq]. Hence φ maps closed
triangles with vertices in Ω onto closed triangles (a triangle is the union of segments from a vertex to the
points of the opposite side), and the same holds for φ⁻¹ (it has the same form on {Y < 0}). A set in general
position is in convex position iff none of its points lies in a closed triangle of three others (Carathéodory),
so convex position is preserved in both directions.

(b) orient(φp, φq, φr) = det[(φp,1); (φq,1); (φr,1)] = det(V Mᵀ)/(w(p)w(q)w(r)) where V has rows (p,1), (q,1),
(r,1); this equals det M · orient(p,q,r)/(w(p)w(q)w(r)), a positive multiple of orient(p, q, r).

(c) Write p − z = α_p n + β_p u with α_p = w(p)/|n|² > 0 and β_p = u·(p − z)/|n|². Then x(φp) = −β_p/α_p
and orient(z, p, q) = det(p − z, q − z) = (α_p β_q − β_p α_q)·det(n, u) with det(n, u) = |n|² > 0. So
orient(z, p, q) < 0 iff β_q/α_q < β_p/α_p iff x(φp) < x(φq).

(d) Let L = pr with z ∉ L. Lines through z map into vertical lines (φ(z + tv) = (−u·v/n·v, −1/(t n·v)) for
t > 0, n·v > 0), and the preimage of a vertical line {X = c} is the line {(u + c n)·(p − z) = 0} through z; so
L' := the line containing φ(L ∩ Ω) is not vertical. L meets Ω (it contains p ∈ X), and φ maps Ω \ L
homeomorphically onto {Y < 0} \ L'; each side of L within Ω is convex, hence connected, and is mapped onto one of
the two (connected) sides of L' within {Y < 0}. The side H_z(L) ∩ Ω contains the points z + tv for small t > 0
(H_z(L) is an open set containing z), whose images have a fixed abscissa and ordinate −1/(t n·v) → −∞; these lie
below the non-vertical line L'. Hence H_z(L) ∩ Ω is mapped below L' and the other side above L'. Apply this to q.

The final sentence follows from (b)–(d) and the definitions. ∎

**Lemma 0′ (genericity).** If (A, B) is a z-split of S, there is a point z' outside S of the same kind
(finite outside conv(S), or a direction) on no line through two points of S such that (A, B) is a z'-split, the
z'-order restricted to A and to B equals the z-order, and z'-caps/z'-cups of subsets of A and of B are the same
as z-caps/z-cups.

*Proof.* (S1), (S2) and (for finite z) z ∉ conv(S) are finitely many strict inequalities in z (for a direction,
in d), so they hold on a neighbourhood of z; the lines through two points of S are finitely many, so some z' in the
neighbourhood avoids them all. The z-order and the z-side relations within A are given by the signs of
orient_h(a, a', z) for a, a' ∈ A, which are nonzero by (S1) and therefore unchanged near z; likewise within B by
(S2). ∎

## 3. Convex subsets of a split

By Lemmas 0 and 0′ we may, whenever convenient, assume z = (0, −1) and all x-coordinates distinct: then (S1) says
B is below every line through two points of A, (S2) says A is above every line through two points of B, the
z-order is the x-order and z-caps/cups are caps/cups. Call this the *standard frame*.

**Lemma 2.** Let (A, B) be a z-split of S and P ⊆ S in convex position with P ∩ A ≠ ∅ ≠ P ∩ B. Then P ∩ A is a
z-cap and P ∩ B is a z-cup.

*Proof.* Work in the standard frame. Suppose a_1 < a_2 < a_3 (x-order) are points of P ∩ A forming a cup, i.e.
a_2 lies below the segment a_1a_3, equivalently slope(a_1a_2) < slope(a_2a_3). Take b ∈ P ∩ B. By (S1), b lies
below both lines a_1a_2 and a_2a_3. For x > x(a_2) the lower of the two lines is a_1a_2, for x < x(a_2) it is
a_2a_3, so the open region below both lines is the convex wedge with apex a_2 bounded by the ray from a_2 in
direction a_2 − a_1 (along a_1a_2, to the right) and the ray in direction a_2 − a_3 (along a_2a_3, to the left):
it equals a_2 + {λ(a_2 − a_1) + μ(a_2 − a_3) : λ, μ > 0}. Hence b = a_2 + λ(a_2 − a_1) + μ(a_2 − a_3) with
λ, μ > 0, i.e. a_2 = (b + λa_1 + μa_3)/(1 + λ + μ) lies in the interior of the triangle a_1a_3b. This contradicts
convex position of P. So no three points of P ∩ A form a cup; as every triple is a cup or a cap, P ∩ A is a cap.

Symmetrically, suppose b_1 < b_2 < b_3 in P ∩ B form a cap: slope(b_1b_2) > slope(b_2b_3). Take a ∈ P ∩ A; by
(S2) a lies above both lines b_1b_2 and b_2b_3. The open region above both lines is the convex wedge
b_2 + {λ(b_2 − b_1) + μ(b_2 − b_3) : λ, μ > 0} (for x > x(b_2) the upper line is b_1b_2, for x < x(b_2) it is
b_2b_3). So b_2 = (a + λb_1 + μb_3)/(1 + λ + μ) is interior to the triangle b_1b_3a, a contradiction. ∎

**Lemma 3.** Let (A, B) be a z-split, C ⊆ A a z-cap and D ⊆ B a z-cup, both nonempty. Then C ∪ D is in convex
position.

*Proof.* Standard frame. Label C = {c_1 < … < c_s} and D = {d_1 < … < d_t} by x-order. Every triple of C ∪ D has a
determined orientation:
* c_i, c_j, c_k (i < j < k): negative (cap);  d_i, d_j, d_k (i < j < k): positive (cup);
* c_i, c_j, d (i < j): d lies below the line c_ic_j and x(c_i) < x(c_j), so orient(c_i, c_j, d) < 0;
* d_i, d_j, c (i < j): c lies above d_id_j, so orient(d_i, d_j, c) > 0.
(Orientations of the other orderings follow by antisymmetry; the relative x-order of points of C and D does not
enter.) Now take the model C* = {(cos θ_i, sin θ_i)} with π/2 + δ > θ_1 > … > θ_s > π/2 − δ and
D* = {(cos ψ_j, sin ψ_j)} with −π/2 − δ < ψ_1 < … < ψ_t < −π/2 + δ, for small δ > 0. Then C* is a cap and D* a cup
in x-order, every line through two points of C* is a nearly horizontal chord near height 1, so D* lies below it,
and every line through two points of D* lies near height −1, so C* lies above it. So C* ∪ D* has the same labelled
orientations as C ∪ D, and C* ∪ D* lies on a circle, hence is in convex position. Convex position of a set in
general position is determined by its labelled orientations (no point in a closed triangle of three others), so
C ∪ D is in convex position. ∎

**Corollary 4.** For a z-split S = A ∪ B: gon(S) = max{ gon(A), gon(B), cap_z(A) + cup_z(B) }.

*Proof.* "≥": subsets of A or of B, and (Lemma 3) a largest z-cap of A together with a largest z-cup of B.
"≤": a convex P ⊆ S lies in A, or in B, or meets both, and then |P| = |P ∩ A| + |P ∩ B| ≤ cap_z(A) + cup_z(B)
by Lemma 2. ∎

(Lemmas 2–3 are the classical mechanism behind the Erdős–Szekeres construction; they are written out here for the
projective, y-separation-free notion of split used below.)

**Lemma 4′ (splits are linear partitions; used only for the completeness of the computations).** If (A, B) is a
z-split with |A|, |B| ≥ 2, then conv(A) ∩ conv(B) = ∅; hence some line through two points of S, with those two
points assigned suitably, induces the partition (A, B).

*Proof.* Standard frame. Let R be the open region below every line through two points of A; it is convex and
contains B by (S1), hence contains conv(B). If x ∈ conv(A), let e = aa' be the edge of the lower boundary of conv(A)
lying over the abscissa of x (|A| ≥ 2; at a vertex abscissa take either adjacent edge; if conv(A) is a segment, e is
that segment): x lies on or above e, hence on or above the line aa', so x ∉ R. Thus conv(A) ∩ conv(B) = ∅, and the
two compact convex sets are strictly separated by a line ℓ. Translate ℓ towards A until it first meets a point
a₀ ∈ A (it moves away from B), then rotate it about a₀ until it first meets another point p ∈ S. No point crossed the line, so all points of
A other than a₀, p lie strictly on one side and all points of B other than p strictly on the other; (A, B) is the
partition induced by the line a₀p with a₀ put on A's side and p on its own side. ∎

So `tools/splits.py`, which enumerates the partitions induced by all lines through two points with all four
assignments of the two points and both roles (A above / B above), tests every candidate. On all example sets and on
all 216 walk sets, every partition that is not a split already fails the exact one-sidedness test (the LP was never
the reason for a rejection; `logs/split_exactness.txt`), so "no nontrivial split" is decided by exact integer tests
for those finite sets, and each split found was re-verified with an exact rational z.

## 4. Main theorem

**Theorem 5.** Let S be in general position with gon(S) ≤ 6 and |S| ≥ 33, and let (A, B) be a z-split of S with
|A| ≥ 2 and |B| ≥ 2. Put c = cap_z(A), d = cup_z(B). Then (c, d) ∈ {(4, 2), (2, 4)}, and

* if (c, d) = (4, 2): B is a z-cap, 2 ≤ |B| ≤ 6, |A| ≥ |S| − 6 ≥ 27, and A has no z-5-cap;
* if (c, d) = (2, 4): A is a z-cup, 2 ≤ |A| ≤ 6, |B| ≥ |S| − 6 ≥ 27, and B has no z-5-cup.

In particular min(|A|, |B|) ≤ 6 and the smaller part is in convex position. If N(7,5,7) ≤ 26, no such split
exists.

*Proof.* By Lemma 0′ assume z lies on no line through two points of S; let φ be the map of Lemma 0 for X = S, so
φ(S) has distinct x-coordinates and is in general position, and caps/cups/convex position correspond.
|A| ≥ 2 gives c ≥ 2 and |B| ≥ 2 gives d ≥ 2, and by Corollary 4, c + d ≤ gon(S) ≤ 6. Hence
(c, d) ∈ {(2,2), (2,3), (2,4), (3,2), (3,3), (4,2)}. φ(A) has no (c+1)-cap and gon(φ(A)) ≤ 6, so
|A| ≤ N(7, c+1, 7); φ(B) has no (d+1)-cup, so |B| ≤ N(7, 7, d+1). By (F2), (F3):

| (c, d) | bound on \|A\| + \|B\| |
|---|---|
| (2, 2) | 6 + 6 = 12 |
| (2, 3), (3, 2) | 6 + 16 = 22 |
| (3, 3) | 16 + 16 = 32 |

all smaller than 33. In case (4, 2), φ(B) has no 3-cup, so every triple of φ(B) is a cap triple, B is a z-cap and
hence in convex position (as in (F2)), so |B| ≤ 6 and
|A| = |S| − |B| ≥ |S| − 6; c = 4 means A has no z-5-cap. Case (2, 4) is symmetric. If N(7,5,7) ≤ 26, case (4,2)
would give a set φ(A) of ≥ 27 points with distinct x-coordinates, no 5-cap and gon ≤ 6, which is impossible; case
(2,4) gives the same after the reflection (x,y) ↦ (x,−y) (F3). ∎

**Remark (32 points).** For |S| = 32 the same table leaves exactly: (c, d) = (3, 3) with |A| = |B| = 16 (both parts
extremal for Baek's theorem), or (4, 2) / (2, 4) with the small part a convex chain of at most 6 points and the large
part of at least 26 points without z-5-caps (resp. z-5-cups). The classical 32-point set realizes all three types
(16+16, 26+6, 6+26; §7).

**Remark (relation to Tóth–Valtr).** For a hull vertex v of S and z just outside conv(S) near v, ({S∖v}, {v})
is a z-split with |B| = 1; then Corollary 4 gives gon(S) = max(gon(S∖v), cap_z(S∖v) + 1), which is exactly the
Tóth–Valtr reduction (ES(7) ≤ N(7,6,7) + 2). Theorem 5 is the analogue for splits with two nontrivial parts, where
Baek's theorem removes every case except (4,2)/(2,4).

**Theorem 6 (equivalence).** The following are equivalent:
1. some set of 33 points in general position with gon ≤ 6 has a z-split (A, B) with |A|, |B| ≥ 2;
2. N(7, 5, 7) ≥ 27.

*Proof.* (1 ⇒ 2) Theorem 5: in case (4,2), φ(A) contains 27 points with distinct x-coordinates, no 5-cap and
gon ≤ 6; in case (2,4) reflect φ(B).
(2 ⇒ 1) Let A₀ be 27 points in general position, distinct x-coordinates, no 5-cap, gon(A₀) ≤ 6. Let
B₀ = {(t_j, −M − ε t_j²) : j = 1..6} with distinct t_j ∈ [−1, 1], ε > 0 and M large. B₀ is a cap of 6 points
(on a downward parabola), so gon(B₀) = 6 and cup(B₀) = 2. A line through two points of B₀ is
y = −M − ε(t_i + t_j)x + εt_it_j; on the x-range of A₀ it stays below min y(A₀) once M is large, so A₀ is above
all lines of B₀ (S2). The lines through two points of A₀ are finitely many non-vertical lines, bounded below on
[−1, 1], so for M large B₀ is below all of them (S1). General position: three points of B₀ are never collinear;
a fixed pair of A₀ and a point of B₀, or a pair of B₀ and a point of A₀, is collinear for at most one value of M
(the B₀-line moves vertically with M), so all but finitely many large M work. Then (A₀, B₀) is a z-split for
z = (0, −1) and by Corollary 4 gon(A₀ ∪ B₀) = max(gon(A₀), 6, cap(A₀) + cup(B₀)) ≤ max(6, 6, 4 + 2) = 6, with
|A₀ ∪ B₀| = 33. ∎

(The direction 2 ⇒ 1 is the classical gluing of the Erdős–Tuza–Valtr equivalence; it is also recorded in the
project plan `cloud/es7-2026-10-19/plan/es7_structure.md`, lead L1. Direction 1 ⇒ 2 is the one for which no matching
statement was found in the sources inspected; see §5.)

**Corollary 7 (general k).** Let k ≥ 5, gon(S) ≤ k − 1, |S| > 2^(k−2), and (A, B) a z-split with |A|, |B| ≥ 2.
Then c = cap_z(A), d = cup_z(B) satisfy 2 ≤ c, d and c + d ≤ k − 1, |A| ≤ N(k, c+1, k), |B| ≤ N(k, k, d+1). If
the ETV values N(k, a, k) = Σ_{i=0}^{a−2} C(k−2, i) hold for all 5 ≤ a ≤ k − 2 (a = 3 is trivial and a = 4 is
Baek's theorem N(k,4,k) = C(k−1,2) + 1), then |A| + |B| ≤ Σ_{i=0}^{c−1} C(k−2,i) + Σ_{i=c}^{k−2} C(k−2,i) = 2^(k−2),
a contradiction; so no such split exists. For k = 7 the only open case is a = 5; for k = 8 they are a = 5, 6.
(Proof as for Theorem 5, using N(k,k,d+1) = N(k,d+1,k) ≤ Σ_{i=k−1−d}^{k−2} C(k−2,i) and k − 1 − d ≥ c.)

**Proposition 8 (hull vertices and hexagons; sharp threshold).** Let N* = N(7,5,7) (so 26 ≤ N* ≤ 56; the upper
bound is the cups–caps bound C(8,3) for no 5-cap and no 7-cup).
(a) Let S be in general position with gon(S) ≤ 6, v a vertex of conv(S), and T ⊆ S \ {v} with |T| ≥ N* + 1. Then
T ∪ {v} contains a convex hexagon having v as a vertex. In particular, if |S| ≥ N* + 2 every hull vertex of S is a
vertex of a convex hexagon of S.
(b) There is a set of N* + 1 points in general position with gon ≤ 6 having a hull vertex that is a vertex of no
convex hexagon.
So "every hull vertex of a 33-point counterexample lies on a convex hexagon" follows from N(7,5,7) ≤ 31, and the
same statement fails for some 27-point heptagon-free sets (the construction in (b) works with any A₀ of 26 points with
distinct x-coordinates, no 5-cap and gon ≤ 6, which exists by (F4); an explicit 27-point example, checked by exact
computation, is `data/prop8b_witness27.txt`).

*Proof.* (a) z = v is a point outside X = S \ {v} (v ∉ conv(X)) on no line through two points of X. For Y ⊆ X,
Y ∪ {v} is in convex position iff Y is a v-cap: if y_1 <_v y_2 <_v y_3 is a v-cup triple, the ray from v through y_2
meets the segment y_1y_3 at a point m and y_2 lies strictly between v and m, so y_2 is interior to the triangle
v y_1 y_3; conversely, if Y is a v-cap, Y is in convex position (by Lemma 0 it maps to a cap, which is in convex
position as in (F2)), no y_j lies in a triangle v y_i y_k (if it
is angularly between y_i and y_k it is beyond the segment y_iy_k as seen from v, otherwise it is outside the angle),
and v lies in no triangle of points of X because it is a hull vertex of S. So a convex hexagon through v is the same
as a v-5-cap. If T had none, φ(T) (Lemma 0) would have distinct x-coordinates, no 5-cap and gon ≤ 6, so |T| ≤ N*.
(b) Take a real set A₀ attaining N* (distinct x-coordinates, no 5-cap, gon ≤ 6) and add v = (x₀, −M) with x₀ generic
and M large, so that ({A₀}, {v}) is a z-split for z = (0, −1) and the set is in general position. By Corollary 4,
gon = max(gon(A₀), cap(A₀) + 1) ≤ 6; v is the lowest point, hence a hull vertex; by Lemma 2 every convex set
through v is v plus a cap of A₀, so it has at most 5 points. ∎

Sample check (computational evidence): in all 216 distinct heptagon-free 32-point order types of
logs/walks_analysis.jsonl every hull vertex v has a v-5-cap (and a v-6-cup) in S \ {v}.

## 5. Relation to known results

* Lemmas 2–3 / Corollary 4 are the classical cap/cup mechanism of the Erdős–Szekeres construction, here stated for
  an arbitrary point z outside the set (finite or at infinity) and without Baek–Balko's y-separation condition.
* Theorem 6's direction 2 ⇒ 1 is the classical Erdős–Tuza–Valtr gluing.
* Theorem 5 (single split with arbitrary, not necessarily decomposable, parts, closed by Baek's theorem except
  for the (4,2)/(2,4) case, which is exactly ETV(7,5,7)) and the equivalence 1 ⇔ 2: **no matching statement was
  found in the sources inspected**: Baek–Balko, SoCG 2025 (HTML; Theorem 8 for recursively decomposable sets, proof
  omitted there; no single-split lemma); Baek, arXiv:2206.04260 (abstract); this repository's
  docs/RELATED_WORK_2026-10-14.md, cloud/es7-2026-10-19/plan/es7_structure.md and
  cloud/es7-2026-10-19/results/LIT/RELATED.md. Not inspected: the Erdős–Tuza–Valtr 1996 paper and the JCTA 2026
  version of Baek–Balko (both unreachable here). The argument for 1 ⇒ 2 is a short combination of the classical
  cap–cup mechanism with Baek's theorem, so it may well be known. Priority is not claimed.

## 6. Value and limits

* The theorem converts "counterexamples with a nontrivial split" into "ETV(7,5,7) counterexamples" (27 points,
  no 5-cap), and conversely. The project estimated ETV(7,5,7)@27 by SAT at 10⁵ to 10⁶ core-hours
  (cloud/es7-2026-10-19/results/B3/README.md; the earlier probes of cloud/es7-2026-10-19/results/B2/README.md gave
  10⁴ to 10⁶ or more), so the conditional part is not cheap to discharge.
* Unconditionally it rules out every *balanced* split: the smaller side of any nontrivial split of a 33-point
  counterexample has at most 6 points and is a convex chain.
* Practical pruning power is small (computational evidence): in the sample of 216 distinct heptagon-free 32-point
  order types (random walks from the classical, mirror and central sets and three annealed random starts), only the
  classical set itself has nontrivial splits; the next emitted walk state (1,000 accepted moves later) and all later
  ones have none (logs/walks_analysis.jsonl, logs/split_exactness.txt), and a separate walk that moves one point per
  step (40 visited sets) has splits only at its start (review/split_theorem/log_k7_walk.txt).
  This suggests that generic extremal sets are split-free, so a counterexample would be expected to be split-free
  anyway.

## 7. Checks performed (computational evidence for the lemmas, not part of the proof)

The independent review ran its own exact tests as well; they are listed in `review/README.md`.

* `tools/test_lemma0.py`: the explicit map φ of Lemma 0 (finite z) on 293 random 7-point sets with random far
  points z, in exact rational arithmetic: 0 violations of (b) orientation signs, (c) z-order ↔ x-order and
  (d) z-side ↔ below (logs/test_lemma0.txt).

* `tools/test_split_lemma.py`: 599 random splits (A, B of 2–6 points; half of them pushed through a random exact
  projective map, which moves z to a finite point), brute force over all subsets: 0 violations of Lemma 2, 0 of
  Lemma 3, 0 mismatches of Corollary 4, and the split finder recovered every planted split
  (logs/test_split_lemma.txt).
* `tools/splits.py` on the example sets (exact one-sidedness tests, LP for z, exact rational re-verification of
  every z): classical 32-point set: 6 nontrivial splits, types (|A|, |B|, c, d) = (6, 26, 2, 4) ×2,
  (26, 6, 4, 2) ×2, (16, 16, 3, 3) ×2, all with c + d = 6; the part sizes 16 and 26 equal Baek's bound
  N(7,4,7) = 16 and the conjectured value N(7,5,7) = 26 (not a proven bound); the mirror 32, central
  32, 3-fold 31 and 30, 6-fold 30, 4-fold 28 and 3-fold 27 sets: no nontrivial split.
