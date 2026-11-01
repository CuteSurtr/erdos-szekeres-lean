# Proofs for single-orbit rotated blow-ups (written 1-2 November 2026)

**Read this first: corrections after the independent checks (2 November 2026).** The text below the line is the
proof file as written during the session; only this header was added. The corrections take precedence over it.
Status labels are those of `../README.md` §9.

1. *Lemma 1* holds as stated below, with its genericity hypothesis (no segment direction of a cluster is parallel to a
   line through two base points). Without that hypothesis the formula is false: B = {(0,0),(1,0)},
   C_1 = {(0,0),(1,0)}, C_2 = {(0,1)} gives sets S_e in general position with mc(S_e) = 3 while (1) gives 2. In the
   (>=) direction the case |B'| = 2 with a one-point chain {w} needs one more line: orient(z_k, w, z_1) =
   e cross(b - b', c_k - c_1) + O(e^2) > 0.
2. *Theorem A* is proved only for generic flattening directions: x not an integer, x != m/2 when O is in the base,
   beta normalised to (-pi/2, pi/2) (the triple (delta, c, d) describes the same cluster as (delta + pi, d, c)), and
   eta small compared with the distance of delta from every chord direction. As written it is **refuted**:
   (i) x = m/2 with O: one orbit of radially flat ES(5,4) clusters for m = 11 plus O (111 points,
   `thmA/m11_beta0_ES54.pts`) satisfies (a)-(c) but has 12 points in convex position;
   (ii) integer x: one orbit of chord-aligned flat 9-point clusters plus O for m = 7 (64 points,
   `../sets/k8/m7_x2_G9s_centre.pts`) has no convex octagon, although 9 > M(7) = 6.
   Condition (c) follows from (b) when c, d >= 2. The remark "M(m)/phi^m decreases" is false (it increases at
   m = 3->4, 7->8, 10->11, ...). M(m) <= phi^(m-1) and 1 + m M(m) < 2^(m-1) for m >= 7 hold (exact check for
   7 <= m <= 3000, written argument for the tail). Tightness for m = 4, 5, 7 (8, 16, 43 points) is confirmed.
3. *Theorem B* needs the hypothesis that every cluster is flat relative to its own orbit: all its segment directions
   lie, mod pi, strictly between two consecutive chord directions of that orbit. With it the proof holds; as written
   it is **refuted** by example (ii), which uses one orbit. The remark after Theorem B ("no symmetric analogue of the
   one-level Valtr construction exists for m >= 7") is withdrawn.
4. *Proposition C*: the "sufficient condition for (ii)" holds only together with (i). The reduction is one-way: a
   cluster of the right size satisfying (i)-(iii) suffices for the conjecture at that m, but is not necessary.
5. *Lemma D*: read "any base with at least 2 and fewer than 64 points". "Any Valtr construction" is covered only for
   Valtr sets realised as (X,Y)-blow-ups or with generic cluster directions. The deep-vertex test depends on the
   realisation, not only on the order type, so the case "one cluster of 61-63 points plus 1-3 single points" is not
   settled by it for all realisations; the module computation (no line-module of size 2..60) is unaffected.
6. *Theorem E* covers generic clusters only (no segment exactly parallel to a chord of the m-gon). Its UNSAT results
   are certificates accepted by lrat-check only (cake_lpr was not run). All four lower bounds rest on exactly checked
   point sets: N(4) >= 2, N(5) >= 3 and N(7) >= 9 on the sets named below, and N(6) >= 5 (stated below as a
   floating-point evaluation) on a 5-point cluster found by the independent check, whose 30-point 6-fold set has
   largest convex subset 6 (`check/m6_cluster5.py`, `check/m6_cluster5_exact.log`). N(8) <= 14 is an upper bound only.
7. *Lemma 0*, aside: the radius ratios quoted for the first 64-point set are inaccurate (layer 2 / layer 1 = 0.381,
   r8/r7 = 0.933). Nothing depends on them.

Paths in the text refer to the working directory of the session: `tools/clsat*.py` are `./clsat*.py`,
`out/sat/` is `./sat/`, `out/rb/` files are in `../sets/` and `./thmA/`, and "the S1 64-point set(s)" are
`../sets/k8/c7_64pts_small.pts` and `../sets/k8/c7_64pts_9layers_centre.pts`. `tools/rbeval.c`, `tools/clrec.c`,
`tools/deep_check.py`, `out/modules64.txt` and the session README are not copied.

---

# Proofs (as written)

Notation. A set is in general position if no three points are collinear. mc(X) is the size of a largest subset of X
in convex position. "Direction" means a unit vector, written as an angle mod 2 pi. For an open arc I of directions,
a ccw I-chain of a finite set C is a sequence z_1, ..., z_k of points of C (k >= 1) whose edge directions
dir(z_i z_{i+1}) all lie in I and increase strictly (counter-clockwise) along the chain (for arcs of length <= pi
this is the same as: all turns are left turns). f_C(I) is the largest k for which a ccw I-chain exists (f_C(I) >= 1
when C is non-empty). R is the rotation by 2 pi/m about the origin O.

-------------------------------------------------------------------------------------------------------------------

## Lemma 0 (sizes; the numerology of the task)

An m-fold rotationally symmetric finite set S (m >= 2) is a union of free R-orbits of size m plus possibly O; for
even m, O is not in S if S is in general position and has at least 2 points (O is the midpoint of p and -p).
Hence |S| = 2^(m-1) is possible only if
* m odd and 2^(m-1) = 1 (mod m): m is an odd prime (Fermat) or a base-2 Fermat pseudoprime (341 = 11*31, 561,
  645, ...), and then O is in S and S \ {O} has (2^(m-1) - 1)/m orbits;
* m even and m | 2^(m-1): m is a power of two (write m = 2^j q, q odd; q | 2^(m-1) forces q = 1).
So k = m + 1 is in {3, 4, 5, 6, 8, 9, 12, 14, 17, 18, 20, ...} (m prime or m = 2^j), plus k = 342, 562, ... .

Combinatorial aside (no geometry). For p an odd prime, Z_p acts freely by translation on the 2^(p-1) - 1 non-empty
even-size subsets of Z_p (a non-empty proper subset fixed by a translation of prime order would be a union of
cosets of Z_p). So (2^(p-1) - 1)/p is the number of orbits, and the orbits of size-2j subsets number C(p, 2j)/p.
For p = 7: 3 + 5 + 1 orbits of sizes 2, 4, 6. The certified S1 64-point set has its 9 layers grouped by radius as
1 (outer) + 3 + 5 (consecutive radius ratios inside the groups 0.95-0.99, between them 0.81). This match is an
observation only; nothing below depends on it.

## Lemma 1 (blow-up formula for tiny clusters)

Let B be a finite set in general position, and for each b in B let C_b be a finite set in general position. Let D
be the (finite) set of directions of segments of the sets C_b, and assume that no direction in D is parallel to a
line through two points of B. For e > 0 put S_e = union over b of (b + e C_b). For a subset B' of B in convex
position with |B'| >= 2 and b in B' let b-, b+ be the neighbours of b in the ccw cyclic order of B' (for |B'| = 2
both are the other point) and let I_b(B') be the open arc of directions from dir(b- b) counter-clockwise to
dir(b b+) (a half-circle if |B'| = 2). Then for all sufficiently small e > 0, S_e is in general position and

    mc(S_e) = max( max_b mc(C_b),  max over convex B' (|B'| >= 2) of  sum_{b in B'} f_{C_b}(I_b(B')) ).      (1)

Proof. All statements below involve finitely many strict inequalities, so one e_0 works for all of them.
General position: a triple inside one cluster is non-degenerate; a triple from three clusters is close to a
non-degenerate base triple; for two points of b + e C_b and one point near b' != b, the line through the two points
has a direction d in D and passes within O(e) of b, while the line through b with direction d misses b' (d is not
parallel to b b').
(>=) Take B' and ccw I_b(B')-chains Z_b of maximal length. Traverse the clusters in the ccw order of B' and each
b + e Z_b in its chain order. Edges inside a cluster have directions in I_b(B') (independent of e), edges between
consecutive clusters have directions within O(e) of dir(b b+). Since the chain directions lie strictly inside the
open arcs, for small e every turn is a left turn and the directions increase once around the circle, so the
closed polygon is convex and has sum |Z_b| vertices. A largest convex subset of one cluster gives the other term.
(<=) Let Q in S_e be in convex position and B' the set of b whose cluster meets Q. If |B'| = 1, |Q| <= mc(C_b).
Otherwise B' is in convex position (a base point strictly inside a triangle of three others would make the nearby
point of Q lie inside the triangle of the nearby points of Q). Every b in B' is a vertex of conv(B'), so a line
separates b from the other points of B' with a margin, hence (small e) the cluster of b from the other clusters; the
boundary of conv(Q) crosses this line at most twice, so the points of Q in each cluster are consecutive along the
boundary. The neighbouring clusters of b along Q are b- and b+, and the points of Q in cluster b form a ccw chain
whose edge directions lie in D and strictly between the directions of the two adjacent inter-cluster edges, which
tend to dir(b- b) and dir(b b+). As D is finite and avoids these limits, for small e all edge directions of the
chain lie in I_b(B'), so the chain has at most f_{C_b}(I_b(B')) points. Sum over b. QED

Flat clusters. If C_b is the image of a set G with largest cup c_b and largest cap d_b under a linear map that sends
the x-axis to direction delta_b and squeezes the other direction enough that every segment direction of C_b is
within eta of delta_b or delta_b + pi, then (eta small compared with the distance of delta_b and delta_b + pi from
the finitely many arc end-points) f_{C_b}(I) = c_b if delta_b is in I, d_b if delta_b + pi is in I, and 1
otherwise; and |G| <= C(c_b + d_b - 2, c_b - 1) (Erdos-Szekeres cup-cap theorem), with equality for the
Erdos-Szekeres sets G(c_b + 1, d_b + 1). This is the case used by Valtr / Baek-Balko (all delta_b equal); the
"rotated" case below has delta_{Rb} = delta_b + 2 pi/m.

## Theorem A (single orbit of flat clusters: exact characterization)

Let m >= 3, let L = {R^j v_0} be a regular m-gon centred at O, and let S be the blow-up (Lemma 1) of the base L, or
of L u {O} (O with a one-point cluster), where the cluster at R^j v_0 is R^j(C) for a flat cluster C at v_0 with
direction delta = theta_0 + beta (theta_0 = angle of v_0), largest cup c and largest cap d (|C| >= 2). Put
x = (m/pi)(beta + pi/2) and y = m - x, assume (genericity) x is not an integer. If mc(S) <= m then:
(a) 1 < x < m - 1 (the flattening direction is at least pi/m away from the tangent);
(b) c <= floor(y) + 1,  d <= floor(x) + 1,  c + d <= floor(max(x, y)) + 2;
(c) if O is in the base: d <= (m-1)/2 when x < m/2, and c <= (m-1)/2 when x > m/2 (m odd).
Consequently |C| <= M(m) := max over 2 <= a <= floor(m/2) + 1 of C(m - a, min(a - 1, floor((m - a)/2))), and
|S| <= 1 + m M(m) (O allowed only for odd m). Values: M(3) = 1, M(4) = 2, M(5) = 3, M(7) = 6, M(8) = 10, M(11) = 35,
M(13) = 84; M(m) <= phi^(m-1) for all m (phi the golden ratio; numerically M(m)/phi^m decreases). So 1 + m M(m) equals 2^(m-1) for m = 3, 5 and
m M(m) = 2^(m-1) for m = 4, while 1 + m M(m) < 2^(m-1) for every m >= 7 (and m M(m) < 2^(m-1) for even m >= 6).

Proof. Apply (1). For a base polygon B' contained in L, a vertex v with gaps a (before) and b (after) along L
(measured in steps of 2 pi/m) has turning arc I_v = (theta_v + pi/2 - a pi/m, theta_v + pi/2 + b pi/m). Hence v
gets weight c iff delta_v is in I_v iff beta in (pi/2 - a pi/m, pi/2 + b pi/m), and weight d iff
beta + pi is in I_v. (a) For B' = L all gaps are 1; if |beta -+ pi/2| < pi/m every vertex has weight c (or d) >= 2,
so the polygon has >= 2m > m points. So beta is in (-pi/2 + pi/m, pi/2 - pi/m), i.e. 1 < x < m-1. Then a vertex
gets the cup weight c iff its preceding gap exceeds y, and the cap weight d iff its following gap exceeds x.
(b) Take B' = s+1 consecutive vertices (s = 1, ..., m-1; preceding gap of the first vertex and following gap of the
last vertex both m - s, all other gaps 1). The first vertex has weight c iff s < x, the last has weight d iff
s < y, the others weight 1. So s + c <= m for all s < x, giving c <= m + 1 - ceil(x) = floor(y) + 1; likewise
d <= floor(x) + 1; and for s < min(x, y) both weights occur: s - 1 + c + d <= m, so
c + d <= m + 2 - ceil(min(x,y)) = floor(max(x,y)) + 2.
(c) Let m be odd, O in the base, x < m/2 (beta < 0). For B' = {O, v_0, ..., v_s} with s = (m-1)/2 consecutive steps
(O is a vertex since the arc spans less than pi), the arc at v_s is (theta_s + pi/2 - pi/m, theta_s + pi), which
contains delta + pi = theta_s + beta + pi because beta is in (-pi/2 - pi/m, 0). So 1 + (s+1) - 1 + d <= m, i.e.
d <= (m-1)/2. The case x > m/2 is symmetric (the first vertex then gets weight c).
Bound: by symmetry (x <-> y swaps c and d) assume x < m/2 and let a = ceil(x), 2 <= a <= floor(m/2) + 1. Then
floor(x) = a - 1, floor(y) = m - a, max(x,y) = y, so n := c + d - 2 <= m - a and k := d - 1 <= a - 1 (and
<= (m-3)/2 by (c), which is implied below). |C| <= C(n, k) <= C(m - a, min(a - 1, floor((m-a)/2))) since C(n, k)
increases in n and, for k <= n/2, in k. Comparison with 2^(m-1): for a <= (m+2)/3 the term is C(m - a, a - 1) and
the sum of these over a is the Fibonacci number F_m <= phi^(m-1); for a > (m+2)/3 the term is at most
2^(m-a) < 2^((2m-2)/3). So M(m) <= max(phi^(m-1), 2^((2m-2)/3)) and 1 + m M(m) < 2^(m-1) for m >= 30; for
7 <= m <= 400 the inequality was checked by exact integer computation (and M(m)/phi^m decreases, consistent with
Theta(phi^m/sqrt m)). QED

Converse. Conditions (a)-(c) (with c + d - 2 <= m, which follows from (b)) are also sufficient for mc(S) <= m.
Proof: a vertex with gaps (a, b) gets the cup weight iff a > y and the cap weight iff b > x (never both: for r >= 3
the two gaps are different parts, for r = 2 they sum to m). For an O-free polygon with gaps g_1..g_r (sum m), charge
each vertex's extra weight to its preceding gap (cup) or following gap (cap). A gap g > y receives c - 1 <= floor(y)
<= g - 1, a gap g > x receives d - 1 <= g - 1, a gap g > max(x,y) may receive both, c + d - 2 <= floor(max) <= g - 1;
so every gap g carries at most g (its vertex 1 plus charges), and the total is at most m. For a polygon
{O, v_1..v_r} with x < m/2 (gaps h_i, 2 sum h_i < m <= 2y, so no cup weights): v_r gets d, v_i (i < r) gets d iff
h_i > x (then h_i >= d); the total is at most 1 + d + sum h_i <= 1 + d + (m-1)/2 <= m by (c). {O, v}: 1 + d <= m.
One cluster: c + d - 2 <= m. (x > m/2 is symmetric.) QED
Cross-check: for 3024 random (m, beta, c, d) with m in {4,5,6,7,8,9,11}, c, d <= 7, the evaluator `tools/rbeval.c`
(full formula (1) over all convex base polygons) agrees with "(a)-(c)" in every case (`tools/check_thmA.py`).

Tightness (certified point sets, `out/rb/`): m = 5, beta = -36 deg, C = 3-cup (c, d) = (3, 2): 16 points, mc = 5
(`m36_cup.pts`); m = 7, beta = -25.7 deg, C = G(4,4), (c, d) = (3, 3): 43 points, mc = 7 (`p7_33.pts`); m = 4,
2-point clusters, beta = -18.4 deg: 8 points, mc = 4 (`c4_8_k5.txt`). The predicted failures were also observed
exactly: m = 5 with (2, 3) at beta = -36 deg gives mc = 7; m = 7 with (4, 3) gives 8 and (3, 4) gives 9.

## Theorem B (every flat cluster of a symmetric blow-up is small)

Let S be the blow-up (Lemma 1) of an m-fold symmetric base B in general position by flat clusters with
C_{Rb} = R(C_b). If mc(S) <= m, every cluster has at most M(m) points. Hence, if |S| = 2^(m-1), the base has at
least (2^(m-1) - 1)/(m M(m)) orbits: at least 2 for m = 7, at least 3 for m = 11, and at least
(2^(m-1) - 1)/(m phi^(m-1)) for m >= 30, i.e. exponentially many.

Proof. For an orbit L of B, the base polygons used in the proof of Theorem A(a), (b) are contained in L, hence are
convex sub-polygons of B; by (1) the same inequalities hold for the cluster type of L, and the size bound of
Theorem A follows (condition (c) was not needed for the formula of M(m)). QED

Remark. Theorem B does not exclude symmetric blow-ups with several orbits; in fact one exists for m = 7 (below).
What it shows is that no symmetric analogue of the one-level Valtr construction (a base of about m points with
large clusters) exists for m >= 7.

## Proposition C (single orbit plus centre, arbitrary tiny cluster): an exact reduction

Let m >= 3, v_0 on the unit circle, C a finite set (written in the radial frame of v_0: x radial outward,
y counter-clockwise tangent), generic in the sense of Lemma 1, and S = [O] u union_j R^j(v_0 + eC) (O only for odd
m), e small. Measure directions of C from the ccw tangent direction in units of pi/m, and put for integers x >= 1

    g(x) = f_C((0, x)),   h(x) = f_C((-x, 0)),   F(a, b) = f_C((-a, b)).

Then mc(S) <= m if and only if
 (i)   g(x) + h(x) <= x + 1 for x = 1, ..., m-1;
 (ii)  (only if O is in S) 1 + F_O(h_1) + sum_{i=2}^{r-1} F(h_{i-1}, h_i) + F^O(h_{r-1}) <= m for all r >= 2 and
       positive integers h_1..h_{r-1} with 2 sum h_i < m, and 1 + f_C((-m/2, m/2)) <= m, where
       F_O(b) = f_C((-m/2, b)), F^O(a) = f_C((-a, m/2));
 (iii) mc(C) <= m.
A sufficient condition for (ii) is  g(m/2) + h(m/2) <= (m+1)/2  (with g(m/2) = f_C((0, m/2)), h(m/2) = f_C((-m/2, 0))).

Proof. By (1) we must bound sums over convex sub-polygons of L (or of L u {O}). A vertex with gaps (a, b) has arc
(-a, b) in its own frame (rotation invariance of the cluster), so an O-free polygon with gaps g_1..g_r (r >= 2,
sum m) has total sum_i F(g_i, g_{i+1}) (indices mod r). The full orbit (all gaps 1) gives m F(1,1) <= m, so
F(1,1) = 1: no edge of C has direction in (-1, 1). Hence F(u, 1) = h(u) and F(1, u) = g(u), and the polygon of
s+1 consecutive vertices (gaps m-s, 1, ..., 1) gives h(u) + g(u) + (s - 1) <= m with u = m - s: this is (i), which is
therefore necessary. Conversely, a chain with directions in (-a, b) splits at the direction 0 (no edge has
direction exactly 0) into a chain in (-a, 0) and a chain in (0, b) sharing one point, so F(a, b) <= h(a) + g(b) - 1
and sum_i F(g_i, g_{i+1}) <= sum_i (h(g_i) + g(g_i) - 1) <= sum_i g_i = m. Polygons through O: the vertex after O
has arc (-m/2, h_1) (the edge from O is radial), the vertex before O has arc (-h_{r-1}, m/2), which gives (ii);
two-point polygons {O, v} give the last term. With F(a, b) <= h(a) + g(b) - 1 the left side of (ii) is at most
g(m/2) + h(m/2) + sum h_i <= g(m/2) + h(m/2) + (m-1)/2, which gives the sufficient condition. Polygons inside one
cluster give (iii). QED

Consequence. For m with size compatibility, a cluster C_m with |C_m| = (2^(m-1) - 1)/m (odd m) or 2^(m-1)/m
(m = 2^j) satisfying (i)-(iii) gives an m-fold symmetric set of 2^(m-1) points in general position with no convex
(m+1)-gon. Clusters exist for m = 3 (1 point), m = 4 (2 points), m = 5 (3-cup), m = 7 (9 points: G(4,4) flat at
-36.84 deg and G(4,3) flat at -34.45 deg, the second placed at offset direction 129.7 deg at a much larger scale than
the flat pieces; profile g = 1,2,3,3,3,3 and h = 1,1,1,1,3,4, so (i) holds with equality for x != 4). The m = 7
cluster gives a certified 64-point 7-fold octagon-free set (`out/rb/p7_compound_64.pts`, also realized with the two
pieces on separate orbits, `p7_two_orbit_64.pts`, same order type). Whether C_8 (16 points) and C_11 (93 points)
exist is open; searches (README) found none.

By the ES cup-cap theorem applied in the radial frame, (i) at x = m-1 gives c + d <= m for the largest cup/cap, so
|C| <= C(m-2, floor((m-2)/2)); this is >= (2^(m-1) - 1)/m for all m >= 5, so Proposition C alone does not rule
out any m. (If ES(m+1) = 2^(m-1) + 1, then |C| <= (2^(m-1) - 1)/m for every admissible C.)

## Lemma D (clusters of Baek-Balko blow-ups are line-modules)

Call C a line-module of S if no line through two points of S \ C separates two points of C. Every cluster of an
(X, Y)-blow-up b_{X,Y,k}(S0) in the sense of Baek-Balko (SoCG 2025, Definition 13) is a line-module: for two points
q, q' of two different other clusters, orient(q, q', c) equals the orientation of the corresponding base triple for
every c in C (the triple condition of Definition 13); for q, q' in one other cluster, all of C lies on one side of
the line q q' (the "almost vertical" condition). Moreover, by the almost-vertical condition, if a cluster C and a
point q of another cluster are given, all lines through two points of C have q on the same side "as the vertical
line through the base point of C"; in particular q is "deep" with respect to C: the vectors c' - c with
orient(c, c', q) < 0 (c, c' in C) lie in an open half-plane. A point strictly inside conv(C) is never deep (two edges
of a triangle of C containing it, oriented upwards, have it on opposite sides).

Application (computed exactly, `out/modules64.txt`, `tools/deep_check.py`): the certified S1 7-fold 64-point sets
have no line-module of size 2..60; their only nontrivial line-modules are the 7 complements of two consecutive hull
vertices and the 7 complements of three consecutive hull vertices; every such module and every complement of one hull
vertex contains all 57 inner points, and no hull vertex is deep with respect to the inner points (exact three-vector
certificates). Complements of one inner point contain that point in their hull. Hence neither set is an
(X, Y)-blow-up of any base with fewer than 64 points, in particular not order-type equivalent to the Erdos-Szekeres
construction, to any Valtr construction (clusters of sizes 6, 15, 20 for k = 8) or to the sets of Baek-Balko
Theorem 19.

## Theorem E (single orbit, arbitrary tiny cluster: exact maxima for m <= 8; computer-assisted)

Let N(m) be the largest size of a generic cluster C satisfying Proposition C (i) (the centre conditions are ignored,
so N(m) bounds both the with-centre and the centre-free single-orbit families). Then

    N(4) = 2,  N(5) = 3,  N(6) = 5,  N(7) = 9,  N(8) <= 14

(the upper bounds are certified; the lower bounds for m = 4, 5, 7 by certified point sets, for m = 6 by a
floating-point evaluation of formula (1) with comfortable margins).

Hence one orbit of tiny clusters (plus the centre for odd m) gives at most 8, 16, 30, 64, 112 points for
m = 4, 5, 6, 7, 8. For m = 7 this is the ES(8) = 65 bound inside the family, attained by the certified 64-point set.
**For m = 8 (k = 9) the family cannot reach 2^7 = 128 points.** The values for m = 4, 5, 7 are attained by certified
point sets; for m = 6 a 5-point cluster exists by the blow-up formula (`tools/clrec.c`, angles in `README`); for
m = 8 the relaxation below is satisfiable with 14 points (realizability not checked).

Proof (relaxation + SAT). Write C in the frame whose x-axis is the inward radial direction. By Prop. C, F(1,1) = 1,
so no segment of C is within pi/m of the tangent, i.e. of the vertical: sort C by x. For i < j let t_ij in (1, m-1)
be the direction of p_i p_j measured counter-clockwise from the ccw tangent (which points down in this frame), in
units of pi/m; it is an increasing function of the slope, and generically not an integer; b_ij = floor(t_ij). Then:
(a) for i < j < k the turn at p_j is left iff t_ij < t_jk; (b) t_ik lies strictly between t_ij and t_jk; (d) a cup
(left turns at consecutive triples) has increasing t, a cap decreasing t; Prop. C's g(x) is the longest cup with all
t < x (= last t < x) and h(x) the longest cap with all t > m - x (= last t > m - x), because a ccw chain with
directions in (-x, 0) is, read backwards, a cap with directions shifted by pi; (e) g(x) + h(x) <= x + 1. Encoding
(`tools/clsat2.py`, sig = 0): order-encoded bins, turn variables, clauses for (a) and (b), auxiliary variables
"a cup/cap with >= l points ends with edge (i,j)" with the forcing implications, profile variables for g, h with
the forcing clauses of (d) and the bounds (e). Assigning to every variable its true value for a real cluster
satisfies every clause, so UNSAT means no cluster of that size exists (and none larger: (i) is inherited by subsets).
CaDiCaL 3.0.1 reports UNSAT for (m, n) = (4,3), (5,4), (6,6), (7,10), (8,15) and the LRAT proofs were accepted by
lrat-check (`out/sat/small_cases.log`): for (7,10) and (8,15) both for this encoding and for the larger
chain-by-chain encoding `tools/clsat.py`; for (4,3), (5,4), (6,6) for `tools/clsat.py`, which encodes the same facts
chain by chain and adds (c) the signotope axiom (for p_i, p_j, p_k, p_l sorted by x the turn signs of ijk, ijl,
ikl, jkl change sign at most once; a known property of point sets, also checked on 20,000 random quadruples). (A tampered proof is rejected by
lrat-check, sanity test in the session.) The encoder was also tested for soundness: the real m = 7 cluster satisfies
all 7,894 clauses of its instance, and random real clusters satisfy all structural clauses
(`tools/clsat_sound.py`). Satisfiable: (5,3), (6,5), (7,9), (8,14). QED

Further (not certified as maxima): the relaxation is satisfiable for m = 9 with n = 28 and for m = 10 with n = 46;
m = 9, n = 30 was undecided after 600 s. For m = 11 (target n = 93) see README sec. 6.
