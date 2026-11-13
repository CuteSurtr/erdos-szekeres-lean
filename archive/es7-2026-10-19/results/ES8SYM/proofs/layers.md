# Rotations of order m >= 4: layers, sizes, chains and zones (k = 8)

Written proofs for `ES8SYM/README.md` §3. They were read line by line in an independent review. Lemma 3 is given
here in its **corrected** form; the first version was false (see the end of Lemma 3).

**Notation.** S is a finite set in the plane in general position (no three points collinear), invariant under the
rotation R by 2π/m about the origin O, with no K points in convex position, K <= 2m. By the layer lemma
(`SYM5/README.md`, §2; it needs K <= 2m and is stated there without a centre point, but O is never a hull vertex, so it
applies to S \ {O}), S \ {O} is a family of nested regular m-gons L_1 (outermost), ..., L_t, every point of L_j (j > i)
strictly inside conv(L_i). Layer i has circumradius r_i and phase θ_i: L_i = { r_i e^{i(θ_i + 2πk/m)} : k = 0..m-1 },
listed counter-clockwise. O can belong to S only for odd m (for even m it is the midpoint of p and -p). "Beyond a
line" means strictly on the side away from O. **L(m, 8)** is the largest t for which such a set with K = 8 exists
(the centre is not counted as a layer).

## Lemma 1 (orientation in polar form)

For points p_k = (cos φ_k, sin φ_k)/u_k with u_k > 0 (k = 1, 2, 3),

    orient(p_1, p_2, p_3) = sign[ u_1 sin(φ_3 - φ_2) + u_2 sin(φ_1 - φ_3) + u_3 sin(φ_2 - φ_1) ].

*Proof.* orient = sign det [[x_k, y_k, 1]]_{k=1..3}. Multiplying row k by u_k > 0 does not change the sign and gives
det [[cos φ_k, sin φ_k, u_k]]_k. Expanding along the last column gives
u_1 sin(φ_3 - φ_2) - u_2 sin(φ_3 - φ_1) + u_3 sin(φ_2 - φ_1). ∎

*Consequence.* With u_i = 1/r_i, every orientation of three non-central points of nested regular m-gons is the sign of
a linear form in (u_1, ..., u_t) whose coefficients depend only on the phases; for fixed phases the order type is
constant on the cells of a central hyperplane arrangement in u-space. A triple containing O has orientation
sign sin(φ_q - φ_p), which depends on the phases only. Lean check: `lean/PolarOrient.lean` (`C7.orient_polar` is the
displayed formula; the other theorems there are the layered and scaled versions and the centre case).

## Lemma 2 (sizes for K = 8)

(a) If m >= 8, then S ⊆ {O}. (b) For m in {4, 5, 6, 7}: |S \ {O}| = m t, and O ∈ S only for odd m. Hence an m-fold
symmetric set in general position without 8 points in convex position has at least 65 points iff it has
t >= 17 (m = 4), t >= 13 (m = 5), t >= 11 (m = 6), t >= 10 (m = 7) layers.

*Proof.* (a) The R-orbit of a point p ≠ O is a regular m-gon: m >= 8 points on a circle, hence in convex position.
(b) Layer lemma and the remark on O. For m = 5: 5t + 1 >= 65 iff t >= 13 (5·12 + 1 = 61); for m = 7: 7t + 1 >= 65 iff
t >= 10 (7·9 + 1 = 64); for even m the centre is excluded. ∎

General position is needed in (b): without it, O together with (±k, 0), (0, ±k) for k <= 16 is a 65-point 4-fold set
with 16 layers and no 5 points in strictly convex position. Lean check of (a) and of the threshold arithmetic of (b):
`lean/C6check.lean` (`RefuteC6.part_a`, `thr_m4` ... `thr_m7`); the layer-lemma step of (b) is not formalised.

## Lemma 3 (rotation chains; corrected)

Let d >= 2 divide m, Q = R^{m/d} (rotation by 2π/d), L_i a layer (any R-orbit works) and a a vertex of L_i. Let P be
the closed part of conv(L_i) on the far side of the chord [a, Qa] from O (for d = 2, the chord is a diameter and P is
the closed half of conv(L_i) counter-clockwise from a to Qa = -a; the clockwise case is the mirror image). Let
c_1, ..., c_j be points of S in P \ {a, Qa} such that **a, c_1, ..., c_j, Qa are in convex position, in this
counter-clockwise cyclic order** (the chain and the chord bound a convex polygon). Then d (j + 1) <= K - 1.

For K = 8: j <= 2 when d = 2 (m = 4 or 6) and j <= 1 when d = 3 (m = 6). For odd prime m only d = m is available, and
then P \ {a, Qa} contains no point of S (j = 0).

*Proof.* Points of S in P are vertices of L_i or points of inner layers (outer layers lie outside conv(L_i)), and every
point of P \ {a, Qa} lies strictly beyond the line (a, Qa) (for d = 2: strictly on the chosen side), by general
position. Let C = (c_0, ..., c_j) with c_0 = a, put c_{j+1} = Qa, and let Π = C, QC, Q^2 C, ..., Q^{d-1} C (a closed
polygon; Qc_0 is the first vertex of QC). Its d(j + 1) vertices are points of S (S is Q-invariant) and are distinct
(the regions Q^s P meet only in the points Q^s a). We show that Π is convex; then d(j + 1) <= K - 1.

* *Angular order.* P lies in the closed angular sector from the ray Oa to the ray O(Qa) (counter-clockwise, angle
  2π/d <= π): for x ∈ P the segment [O, x] meets the line (a, Qa) inside conv(L_i), that is, inside [a, Qa]. No c_l
  lies on one of the two bounding rays (it would lie on [O, a] or [O, Qa], which meet P only in a and Qa; for d = 2 it
  would be collinear with a and -a). Let Γ be the convex polygon a, c_1, ..., c_j, Qa; [Qa, a] is one of its edges, and
  Γ lies on the side of the line (a, Qa) away from O (for d = 2: on the chosen side). A ray from O strictly inside the
  sector meets the chord [a, Qa] at an interior point of it (at O itself when d = 2), enters Γ there, and leaves Γ
  through exactly one point of the chain a, c_1, ..., c_j, Qa. So the c_l are in strictly increasing angular order
  around O, and so are the vertices of Π, with every angular gap below π. Hence Π is a simple polygon, star-shaped
  from O.
* *Turns inside one copy* are left turns, because Γ is convex and listed counter-clockwise; Q preserves orientation.
* *Junction turns.* By symmetry consider (c_j, v, Qc_1) with v = Qa (if j = 0 it is (a, v, Q^2 a), a turn of the
  regular d-gon). Let C_v be the interior cone of conv(L_i) at its vertex v; its angle (m - 2)π/m is < π. The lines
  (v, a) and (v, Q^2 a) through v split C_v into consecutive sub-cones C1 | C2 | C3, C2 containing the direction of
  O (for d = 2 the two lines coincide and C2 is the ray towards O). A point of P \ {a, v} lies in C1 (it is in C_v
  and strictly beyond the line (a, v)); likewise a point of QP \ {v, Q^2 a} lies in C3. For x in C1 and y in C3 the
  rotation from the ray vx to the ray vy passes through C2 and has angle in (0, π), so orient(x, v, y) has the same
  sign for all such x, y. For x = the vertex of L_i adjacent to v inside P and y = the vertex adjacent to v inside QP
  (three consecutive vertices of the counter-clockwise polygon L_i) the turn is left. So every junction turn is left.
* A simple closed polygon with all turns to the left is convex. ∎

*The first version was false.* It assumed only that every turn (c_{l-1}, c_l, c_{l+1}), 1 <= l <= j, is a left turn
(local convexity). That does not give the angular order: a closed pentagon (a, c_1, c_2, c_3, Qa) with all turns left
can wind twice. Counterexamples occur in the certified sets (1-based rows of the point files, d = 2, layer L_1):
`c6_54pts_9layers.pts`, rows a = 1, c_1 = 7, c_2 = 8, c_3 = 12, Qa = 4, and `c4_52pts_13layers.pts`, rows 1, 2, 9, 7, 3.
In both, all c_l lie in P \ {a, Qa} and all three turns are left (`tools/rotation_chain_cex.py`, exact and 100-digit
decimal), so j = 3 and d(j + 1) = 8 > 7, while both sets have no 8 points in convex position. A review counted,
for L_1, d = 2 and the counter-clockwise half, 2,574 such chains with j = 3 in the 6-fold set and 2,197 in the 4-fold
set, and 56 chains with d = 3, j = 3 for layer 2 of the 6-fold set. In both sets the longest chain satisfying the
corrected hypothesis has j = 2 for d = 2, and in the 6-fold set j = 1 for d = 3 (d = 3 does not divide 4).

## Lemma 4 (zones; K = m + 1 with m >= 7, in particular m = 7, K = 8)

Let K = m + 1 with m >= 7, and i < j.
(a) Every vertex v of L_i lies beyond at least two edge-lines of L_j.
(b) If w is the angular offset between v and the nearest vertex of L_j (|w| <= π/m), then
    r_j / r_i < cos(|w| + π/m) / cos(π/m).
(c) For a vertex b of L_j with neighbours b-, b+ (and next neighbours b--, b++), let DZ(b) be the set of points
beyond the edge-lines (b-, b) and (b, b+) and not beyond the edge-lines (b--, b-) and (b+, b++). There are no two
points x, y of S in DZ(b) such that (b-, x, y, b+) is a convex chain turning left at x and y.

*Proof.* (a) v lies outside conv(L_j), so it is beyond at least one edge-line (not on one, by general position). If it
were beyond exactly one, say that of the edge (b, b+), then conv(L_j ∪ {v}) has v as a vertex between b and b+ and
keeps every vertex of L_j (v is not beyond any other edge-line); so L_j ∪ {v} is m + 1 = K points in convex position.
(b) The edge-lines of L_j lie at distance h = r_j cos(π/m) from O with outward normals at angles
θ_j + (2k + 1)π/m. A point at radius r is beyond the edge-line with normal n iff r cos(angle(v, n)) > h, so the
edge-lines v is beyond are those whose normals are within angle arccos(h/r_i) of the direction of v. The two
normals nearest to v are at angular distances π/m - |w| and π/m + |w|; by (a) at least two normals are in the set,
so the second one is: r_i cos(π/m + |w|) > r_j cos(π/m), which is (b).
(c) For m >= 7, DZ(b) is the quadrilateral bounded by the extensions of the two edges at b and by the lines
(b--, b-), (b+, b++). Its vertices other than b are the apices of the zones of the edges (b-, b) and (b, b+) (in the
directions of their normals, at angles θ_b ∓ π/m from O) and the meeting point of (b--, b-) and (b+, b++) on the ray Ob
(these lines meet beyond b because 3π/m < π/2). So DZ(b) lies in the angular sector between b- and b+, and inside
the open wedge at b bounded by the extensions of the two edges at b, which is strictly beyond the chord (b-, b+).
Hence (b-, x, y, b+) has left turns at x and y by hypothesis and at b- and b+ because x, y are beyond the chord; four
left turns make it a convex counter-clockwise quadrilateral, so x precedes y in angular order around O. The polygon
(b+, b++, ..., b--, b-, x, y) turns left at every vertex: inside L_j by convexity; at b- because x is not beyond the
line (b--, b-); at b+ because y is not beyond (b+, b++); at x and y by hypothesis. Its vertices are in angular order
around O, so it is simple, hence convex. It has (m - 1) + 2 = K vertices. ∎

For m = 7, (b) with |w| = π/7 (outer vertex opposite an inner edge midpoint) gives
r_j / r_i < cos(2π/7)/cos(π/7) = 0.692021... For m <= 6 the set DZ(b) is unbounded and the sector argument above does
not apply as written.

## Lemma 5 (trivial upper bounds)

If every set of N points in general position contains a convex octagon, then |S| <= N - 1, so m t <= N - 1 (and
m t + 1 <= N - 1 if O ∈ S). With N = 311 (the project's ES(8) <= 311, Lean-checked in the repository, not re-run
here): L(4,8) <= 77, L(5,8) <= 62 (61 if O ∈ S), L(6,8) <= 51, L(7,8) <= 44. With the peer-reviewed N = 408
(Mojarrad–Vlachos, Discrete Comput. Geom. 56 (2016)): 101, 81, 67, 58. ∎
