# C3-S: hull and convex-layer normalization — soundness argument

Class: S, 33 points (n = 3m, m = 11) in general position, invariant under the rotation R by
+120° about a centre c not in S, with no 7 points in convex position. As in C3a/C3b, a generic
symmetric perturbation keeps the order type, so no two points of S are collinear with c.

Normal form (C3a/C3b): pick a line l through c that avoids S and make it the y-axis with an
orientation-preserving similarity. Label the points 0..n−1 by increasing y/x, set
σ_i = [x_i < 0], and use R(i) = (i − m) mod n, σ_{r+m} = 1 − σ_r, σ_{r+2m} = σ_r. Both encoders
have one variable per R-orbit of chi_S (true = counter-clockwise).

## Lemma 1 (angular order). For labels i, j: the ccw angular order of the points about c,
starting at direction −90°, is the lexicographic order of the keys (σ_i, i).

Proof. A point with x > 0 (σ = 0) has polar angle θ ∈ (−90°, 90°) and tan θ = y/x is increasing
in θ there; a point with x < 0 (σ = 1) has θ ∈ (90°, 270°) and tan θ = y/x is again increasing.
Every σ = 0 point comes before every σ = 1 point. ∎

## Lemma 2 (WLOG label 0 on the hull, σ_0 = 0, and the top case).
Let H be the vertex set of conv(S).

(a) Any point p of S can be given label 0: the labels are the positions in the cyclic order of
the n distinct lines through c and the points, read from l; turning l to a direction just before
the line through p (still avoiding S) makes p label 0, and moving l to just before the line of the
point with old label t turns every old label i into (i − t) mod n.

(b) The point reflection p ↦ −p maps S to a set of the same class (rotations commute with it,
convex position is kept), keeps every y/x and so every label, keeps the hull vertices as hull
vertices (with the same labels), and flips every σ. So σ_0 = 0 may be assumed after (a). (C3a
item 5; this is the existing `sb` clause.)

(c) H is R-invariant, so it is a union of R-orbits, each of size 3 (c ∉ S). H is in convex
position, so |H| ≤ 6 (no convex 7-gon). Hence |H| ∈ {3, 6}. With label 0 in H: H = {0, m, 2m}
(case H3), or H = {0, m, 2m, a, a+m, a+2m} with 1 ≤ a ≤ m−1. Moving label 0 to the point with
label a (by (a)) changes the other orbit's residue to (m − a) mod m, so a ≤ ⌊m/2⌋ may be
assumed; m = 11 is odd, so a ∈ {1..5}. Then apply (b) (which keeps labels and H).
Finally split on s = σ_a ∈ {0, 1}. Cases: H3, H6(a, s) for a = 1..5, s = 0, 1 — 11 cases.

## Lemma 3 (layer clauses). Let P ⊆ S be R-invariant, and L the vertex set of conv(P)
with |L| ∈ {3, 6}. Then c is interior to conv(L) (L contains an orbit, an equilateral triangle
centred at c), so the boundary order of conv(L) is the ccw angular order about c, i.e. the order
of the keys (σ_i, i) (Lemma 1). For every ccw-consecutive pair (u, v) of L and every
w ∈ P \ {u, v}: chi_S(u, v, w) = + (w is strictly left of the directed hull edge; strict by
general position). These are the unit clauses `ccw(u, v, w)`.
For one orbit {r, r+m, r+2m} the cyclic order is r, r+2m, r+m whatever σ_r is (R(r) = r+2m is
the point 120° further ccw), so a one-orbit layer needs no σ.
For the top layer this gives exactly: H3: 0, 2m, m; H6(a, 0): 0, a, 2m, a+2m, m, a+m;
H6(a, 1): 0, a+m, 2m, a, m, a+2m.

Conversely (not needed for soundness, used only by the sanity check "other cases are violated"):
if a cyclic sequence of points has every other point strictly left of every edge, it is the hull
in that order.

## Lemma 4 (convex layers). Define P_1 = S, L_j = vertices of conv(P_j),
P_{j+1} = P_j \ L_j. By induction every P_j and L_j is R-invariant; |L_j| ∈ {3, 6} as in
Lemma 2(c). So every S in the class has a layer sequence (L_1, L_2, ...), each layer one orbit or
two orbits, and the layer clauses of Lemma 3 hold for each (P_j, L_j). `hullcase.layer2_options`
lists, for the residues not used by L_1..L_j, every one-orbit choice and every two-orbit choice
with both σ values of both residues; that is every possible L_{j+1}. So for every node of the
layer tree, the children cover the node. (L_1 is normalized by Lemma 2; residue 0 is in L_1, so it
never appears below, and σ of the residues of a two-orbit layer is fixed by the node.)

## Theorem (cover). If S is in the class, then for the canonical labelling of Lemma 2, the true
assignment of the C3a (or C3b) variables satisfies the base CNF (C3a/C3b soundness, validated in
those tasks) and the hull/layer units of exactly the nodes on S's own layer path. Hence:
if for some set of tree nodes N, every node of N has a UNSAT case CNF (base + its units), and
every root-to-leaf path of the layer tree passes through a node of N (a "cut"), then the class is
empty — up to the trusted parts: the base encoding, Lemmas 1–4 (paper proofs above, validated
below), and the proof checkers.

The cut condition is purely combinatorial: it is checked by `tools/check_cut.py` style
enumeration (every node in the plan is either in N or has all its children enumerated).

## What is validated mechanically (tools/validate_hull.py)
For random symmetric sets with exact coordinates: the hull is computed from the coordinates,
a line l is found by search (random integer directions, with an exact constructive fallback)
satisfying Lemma 2, then σ_0 is fixed by reflection; the case is read off and every clause of
that case's CNF is evaluated on the true assignment; the convex layers are peeled from the
coordinates and the layer units of every prefix are evaluated. Mutations of the hull order are
detected (`tools/mutation_hull.py`).
