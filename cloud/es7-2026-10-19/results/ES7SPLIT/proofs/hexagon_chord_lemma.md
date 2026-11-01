# Hexagon chord lemma (written proof)

Paths in this file are relative to the `ES7SPLIT` directory.

Status: written proof, checked by an independent review on 1 November 2026 (no error found; see
`review/README.md`). It is elementary and of folklore type (the same gluing is used throughout Erdős–Szekeres case
analyses, e.g. Bonnice's layer arguments and Strunk's conditions on points in consecutive-vertex triangles); no
novelty is claimed. It is recorded because it gives exact, local, SAT-ready constraints around every convex
hexagon of a heptagon-free set, in particular around the convex hull when the hull is a hexagon and around every
empty hexagon (which a 33-point counterexample must contain, by Heule–Scheucher's theorem that 24 points contain a
6-hole or a convex 7-gon).

## Statement

Let S be a finite set in general position with no 7 points in convex position, and let H = (h_0, …, h_5) be the
vertices of a convex hexagon with vertices in S, in counter-clockwise order (indices mod 6). Fix i and
m ∈ {1, 2, 3}; put a = h_i, b = h_{i+m+1}; the *dropped* vertices are h_{i+1}, …, h_{i+m} and the *kept* vertices
are the other 6 − m ≥ 3 (including a and b). Define the open region

  R(i, m) = { p : p is strictly on the dropped side of the line ab,
                  strictly left of the directed line h_{i−1} → h_i,
                  strictly left of the directed line h_{i+m+1} → h_{i+m+2} }.

(The last two lines are the edge lines of H at a and b on the kept side; "left" is the inner side since H is
counter-clockwise.)

**Lemma (chord lemma).** There are no m + 1 points q_1, …, q_{m+1} ∈ S ∩ R(i, m) such that
{a, b, q_1, …, q_{m+1}} is in convex position.

**Corollary (extended ears, m = 1).** For every vertex h_j of H, any two points p ≠ q of S ∩ R(j − 1, 1) are
nested with respect to the chord h_{j−1}h_{j+1}: one of them lies in the interior of the triangle formed by
h_{j−1}, h_{j+1} and the other. The region contains h_j itself, so S ∩ R(j − 1, 1) is a chain totally ordered by
nesting that passes through h_j; it consists of the points of S inside the ear triangle h_{j−1}h_jh_{j+1} and the
points outside H that see exactly the two edges of H at h_j (and are on the inner side of the two neighbouring
edge lines).

**Special cases.**
* If conv(S) is a hexagon H, then S ∩ R(j − 1, 1) = {h_j} ∪ (S ∩ int triangle h_{j−1}h_jh_{j+1}): the points in
  each ear triangle of the hull are totally ordered by nesting.
* If H is an empty hexagon (6-hole) of S, the other points of S lie outside H, each sees at least two consecutive
  edges of H (seeing exactly one edge e would make H ∪ {p} a convex 7-gon), and those seeing exactly the two edges
  at h_j form, together with h_j, a nested chain.

## Proof

Suppose q_1, …, q_{m+1} ∈ S ∩ R(i, m) and Q = {a, b, q_1, …, q_{m+1}} is in convex position. All q's lie
strictly on one side of the line ab, so Q′ = conv(Q) is a convex polygon with m + 3 vertices having ab as an edge;
traversed counter-clockwise it reads a, q_{σ(1)}, …, q_{σ(m+1)}, b (the q's in boundary order; the orientation is
the same as that of a, h_{i+1}, …, h_{i+m}, b, which lies on the same side of ab). Let K′ be the convex polygon
spanned by the kept vertices; it has ab as an edge and lies in the closed half-plane of ab not containing the
dropped vertices. Q′ and K′ lie on opposite sides of ab and share exactly the edge ab, so U = Q′ ∪ K′ is a simple
polygon with (m + 3) + (6 − m) − 2 = 7 vertices: a, b, the m + 1 points q, and the 4 − m kept vertices other than
a, b. Its interior angle at every vertex other than a and b is an angle of Q′ or of K′, hence less than π. At a,
the boundary of U (counter-clockwise) passes h_{i−1} → a → q_{σ(1)}; the turn is a left turn iff
orient(h_{i−1}, a, q_{σ(1)}) > 0, i.e. iff q_{σ(1)} is strictly left of the directed line h_{i−1} → h_i, which holds
because q_{σ(1)} ∈ R(i, m). At b the boundary passes q_{σ(m+1)} → b → h_{i+m+2}; the turn is left iff
orient(b, h_{i+m+2}, q_{σ(m+1)}) > 0, i.e. iff q_{σ(m+1)} is strictly left of the directed line
h_{i+m+1} → h_{i+m+2}, which again holds by the definition of R(i, m). A simple polygon all of whose interior angles
are less than π is convex and its vertices are in convex position. So S contains 7 points in convex position, a
contradiction. ∎

*Proof of the corollary.* With m = 1 and i = j − 1 the lemma forbids two points p, q of the region with
{h_{j−1}, h_{j+1}, p, q} in convex position. For four points in general position with p, q strictly on the same side
of the line h_{j−1}h_{j+1}, neither h_{j−1} nor h_{j+1} can lie in the triangle of the other three (that triangle
meets the line only in one of them), so the four are in convex position unless p lies inside the triangle
h_{j−1}h_{j+1}q or q lies inside h_{j−1}h_{j+1}p. That is the nesting alternative. h_j lies in R(j−1, 1) by
convexity of H (it is beyond the chord and strictly inside the neighbouring edge lines). The description of the
region: let p be beyond the chord and strictly inside the edge lines of h_{j−2}h_{j−1} and h_{j+1}h_{j+2}. If p is
inside the edge lines of h_{j−1}h_j and h_jh_{j+1} too, it lies in the open triangle h_{j−1}h_jh_{j+1} (beyond the
chord, inside the two edge lines at h_j), i.e. in the ear. Otherwise p is outside H, and the edges of H whose lines
separate p from H form a nonempty contiguous chain (a standard fact for a point outside a convex polygon). The chain
avoids h_{j−2}h_{j−1} and h_{j+1}h_{j+2}, so it lies inside {h_{j−1}h_j, h_jh_{j+1}} or inside the two remaining edges
{h_{j+2}h_{j+3}, h_{j+3}h_{j−2}}; the latter is impossible, because then p would be inside both edge lines at h_j
and hence in the ear, inside H. So p sees one or both edges at h_j, and not exactly one, since a point that sees
exactly one edge e of H forms a convex 7-gon with H. Conversely, a point seeing exactly the two edges at h_j lies in
the open wedge h_j + {λ(h_j − h_{j−1}) + μ(h_j − h_{j+1}) : λ, μ > 0}, which is beyond the chord (moving from h_j
along h_j − h_{j−1} or h_j − h_{j+1} increases the distance from the chord line on h_j's side), and it is inside the
other edge lines; so it belongs to R(j − 1, 1). ∎

## Checks (computational evidence, not part of the proof)

`tools/test_chord_lemma.py` (exact arithmetic): for 150 random convex hexagons of each of the classical, mirror
and central 32-point sets and all i, m, the largest chain over the chord inside R(i, m) has exactly m points (the
bound is attained, never exceeded), with regions of up to 29 points. Control: on a random 24-point set containing
11 points in convex position the same statistic reaches m + 2, which is the cap of the search loop (r ≤ m + 2), so
the test does detect violations. (logs/test_chord_lemma.txt)

`tools/hullstats.py`, `logs/walks_analysis.jsonl`: in the 4 hexagonal-hull sets of the walk sample (among them the
classical and mirror sets) all hull ears are nested chains; the independent review found the same for the 3-fold
31- and 30-point and 6-fold 30-point sets (`review/chord_lemma/exhaustive_other.txt`). The ear triangles of the
classical set contain 4, 4, 4, 9, 9, 4 points, so the corollary gives no small bound on ear sizes.
