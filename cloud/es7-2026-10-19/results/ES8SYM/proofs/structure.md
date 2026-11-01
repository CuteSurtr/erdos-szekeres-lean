# Line-modules and blow-ups: why the needle-type 7-fold sets are not known constructions

Written argument for `ES8SYM/README.md` §6. It was checked line by line in an independent review,
which added the restriction to bases with at least two points and the remark on coordinates below.

**Line-modules.** A set C ⊆ S is a *line-module* of S if no line through two points of S \ C separates two points of
C. Modules with |C| <= 1 or |C| >= |S| - 1 are trivial. Whether C is a line-module depends only on the orientation
signs, so the multiset of module sizes is an order-type invariant (also under reflection).

**Lemma D.** (a) Let P be an (X, Y)-blow-up of a base with N >= 2 points in the sense of Baek and Balko (SoCG 2025,
Definition 13). Every cluster of P is a line-module of P.
(b) Let P be obtained from a base B in general position by replacing each b ∈ B by a sufficiently small copy C_b of a
set in general position, where no segment of any C_b is parallel to a line through two points of B. Every C_b is a
line-module of P.

*Proof.* (a) Let C be a cluster and q, q' points outside C. If q, q' lie in two different clusters, then for every
c ∈ C the triple (q, q', c) has the orientation of the corresponding base triple (the triple condition of
Definition 13), so the line qq' does not separate C. If q, q' lie in one cluster C', the almost-vertical condition of
C' puts all of C on one side of the line qq'.
(b) A line through points of two different clusters is close to a line through two base points, which misses the
base point of C_b by general position. A line through two points of one cluster C_{b'} passes close to b' with the
direction of a segment of C_{b'}; by the parallelism condition it misses a neighbourhood of b. For small enough copies
neither kind of line meets the convex hull of C_b. ∎

**Consequences** (orientation tables and module enumeration by `structure/orient.py` and `structure/modules.c`;
output in `logs/run_all.log`, §5):
- `c7_64pts_small.pts` and `c7_64pts_9layers_centre.pts` have 14 nontrivial line-modules each, of sizes 61 (7) and 62
  (7): the complements of three or two consecutive hull vertices. `c7_64pts_9layers_centre_own.pts` has 22, of sizes
  57, 60, 61 and 62. So none of these three sets is order-type equivalent to a blow-up as in (a) or (b) that has a
  cluster with 2 to 56 points (2 to 60 for the first two).
- The classical Erdős–Szekeres 64-point set (`structure/es_64points.txt`) has line-modules of sizes 6, 15 and 20,
  among 187 nontrivial ones; Valtr's construction for k = 8 in the form of Baek–Balko §6.1 has clusters of sizes
  C(6, i) for i = 0..6; the sets of Baek–Balko Theorem 19 for k = 8 have clusters of 7 or 22 points. Hence none of the
  three sets above is equivalent to any of these constructions.
- `rule_p7_64pts.pts` and `p7_compound_64.pts` do have 9-point line-modules (7 each): their 7 clusters.

**The given coordinates.** By the almost-vertical condition, a point q of another cluster is *deep* with respect to a
cluster C: the vectors c' - c (c, c' ∈ C) with orient(c, c', q) < 0 lie in an open half-plane. A point strictly inside
conv(C) is never deep. For the first two sets, no hull vertex is deep with respect to the 57 inner points
(`structure/deep_check.py`, three-vector certificates in exact Z[ζ_7] arithmetic). With N >= 2 (every cluster is
nonempty), the module sizes leave only singletons and one big cluster C of 61 to 63 points, and every singleton would
have to be deep with respect to C. A singleton that is an inner point lies strictly inside conv(C), so it is not deep.
A singleton that is a hull vertex q is not deep either: C then contains all 57 inner points (C is the complement of
two or three consecutive hull vertices, or of q), and the certificate for q uses only inner points. So these two
point sets, with these coordinates, are not (X, Y)-blow-ups of any base with 2 to 63 points. Deepness depends on the
coordinates, not only on the order type, so this last statement says nothing more about equivalent sets than the
module statement above. (With N = 1, Definition 13 allows any 64-point set with no 8 points in convex position as
the single cluster.)
