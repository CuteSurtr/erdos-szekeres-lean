# MIRRORETV: written proofs

Complete written proofs for the statements of `README.md`, which also gives the status of each item and the checks.
The text collects the working notes of 1 November 2026, with the corrections asked for by the reviews (README §9).

Contents: definitions (§1); basic lemmas (§2); the mirror lemma (§3); Theorem A, the upper bounds (§4); Theorem B,
the matching lower bounds (§5); Theorem C, the Erdős–Szekeres/ETV block sets (§6); main consequences (§7); upper bounds
for k ≥ 9 (§8); a second construction by symmetric blocks (§9); what is open (§10).

## 1. Definitions and conventions

Points p = (x_p, y_p). orient(p,q,r) = (x_q - x_p)(y_r - y_p) - (y_q - y_p)(x_r - x_p) (twice the signed area).
A finite set is in *general position* if no three of its points are collinear. It is *x-distinct* if its points have
distinct x-coordinates. A set P is in *convex position* if no point of P lies in the convex hull of the others. A
*convex k-gon in X* is a k-subset of X in convex position; subsets of a set in convex position are in convex position.

A sequence p_1, ..., p_m with x_{p_1} < ... < x_{p_m} is an *m-cap* if orient(p_{i-1}, p_i, p_{i+1}) < 0 for all 1 < i < m,
and an *m-cup* if > 0. Sequences with m <= 2 count as both. An x-distinct set is called a cap (cup) if it is one in
increasing x-order. cap(X) and cup(X) are the largest cap and cup sizes, maxconv(X) the largest convex subset.

mu(x,y) = (x,-y). A set S is *mirror-symmetric* if it is invariant under the reflection in some line l. An isometry maps
l to the x-axis and the reflection to mu, and isometries preserve general position and convex position. So we always take
l to be the x-axis.

* N(n,a,b), for n >= 3 and a,b >= 2: the maximum size of an x-distinct set in general position with no n points in convex
  position, no a-cap and no b-cup. This is Baek's notation (Eur. J. Combin. 124 (2025) 104085, arXiv:2206.04260,
  Def. 1.3, which builds x-distinctness into "general position"). It is finite by the cups–caps theorem,
  N(n,a,b) <= C(a+b-4, a-2) (Erdős–Szekeres 1935).
* r_j = N(2j, j, 2j) and r'_j = N(2j-1, j, 2j-1), j >= 2. A 2j-cup is a convex 2j-gon, so r_j is also the largest x-distinct
  set in general position with no j-cap and no convex 2j-gon, and likewise for r'_j.
* N_mirror(k), k >= 3: the maximum size of a mirror-symmetric set in general position with no k points in convex position.
* E(n,a,b) = sum_{i=n-b}^{a-2} C(n-2, i). The *ETV conjecture* (Erdős–Tuza–Valtr 1996) says N(n,a,b) = E(n,a,b) for
  every triplet 2 <= a,b <= n <= a+b-2. Following Baek, P(n,a,b) denotes this statement for one triplet. P(n,n,n) is the
  Erdős–Szekeres conjecture N(n) = 2^(n-2).

Binomial identities (symmetry C(N,i) = C(N,N-i)):

    E(2j, j, 2j)     = sum_{i=0}^{j-2} C(2j-2,i) = (2^(2j-2) - C(2j-2,j-1))/2 ,
    E(2j-1, j, 2j-1) = sum_{i=0}^{j-2} C(2j-3,i) = 2^(2j-4).

Values for j = 2,...,7: E(2j,j,2j) = 1, 5, 22, 93, 386, 1586 and E(2j-1,j,2j-1) = 1, 4, 16, 64, 256, 1024.

## 2. Basic lemmas

**Lemma 2.1 (slopes).** Let x_a < x_b < x_c and let s_uv be the slope of uv. Then
orient(a,b,c) = (x_b - x_a)(x_c - x_b)(s_bc - s_ab), and s_ac is the average of s_ab and s_bc with positive weights
(x_b - x_a)/(x_c - x_a) and (x_c - x_b)/(x_c - x_a). Hence sign orient(a,b,c) = sign(s_bc - s_ab) = sign(s_ac - s_ab) =
sign(s_bc - s_ac). Also orient(a,b,c) > 0 iff b lies strictly below the segment ac.

*Proof.* Substitute y_b - y_a = s_ab (x_b - x_a) and y_c - y_a = s_ab (x_b - x_a) + s_bc (x_c - x_b). For the last claim,
y_b minus the height of the chord at x_b is (s_ab - s_ac)(x_b - x_a). ∎

*Consequences.* (a) A sequence is a cap iff its consecutive slopes strictly decrease, and a cup iff they strictly increase.
(b) If C is a cap and f is the piecewise-linear interpolation of its points, then f is concave with a strict slope decrease
at every interior abscissa. So for any three points p_i, p_j, p_k of C (i < j < k), p_j lies strictly above the chord
p_i p_k. Hence every 3-subset of a cap is a cap triple, every subsequence of a cap is a cap, and the interior points of a
cap lie strictly above the chord joining its end points. The same holds for cups, with "below".

**Lemma 2.2 (region lemma).** Let x_0 < x_1 < ... < x_m (m >= 1) and let f, g be continuous piecewise-linear functions on
I = [x_0, x_m] with breakpoints in {x_i}, f concave, g convex, g <= f. Put V = {(x_i, f(x_i)), (x_i, g(x_i)) : 0 <= i <= m}
and Q = {(x,y) : x in I, g(x) <= y <= f(x)}. Then Q = conv V. The point (x_i, f(x_i)) is an extreme point of Q if
(a) i = 0 or i = m, or (b) 0 < i < m and the slope of f strictly decreases at x_i. Likewise (x_i, g(x_i)) is extreme if
i = 0 or i = m, or if 0 < i < m and the slope of g strictly increases at x_i.

*Proof.* Q is the intersection of the strip I x R, the hypograph of the concave f and the epigraph of the convex g, so it is
convex. It is also compact, and V ⊂ Q. Conversely, for (x,y) in Q with x in [x_{i-1}, x_i], (x, f(x)) and (x, g(x)) are
convex combinations of points of V (f and g are affine there), and (x,y) lies between them. So Q = conv V.
(a) If (x_0, f(x_0)) = (u+w)/2 with u, w in Q, then x_u, x_w >= x_0 with mean x_0, so x_u = x_w = x_0. Then y_u, y_w <= f(x_0)
with mean f(x_0), so u = w. The same argument works at x_m and for g.
(b) Let v = (x_i, f(x_i)) = (u+w)/2 with u, w in Q. If x_u = x_w = x_i, then u = w = v as in (a). Otherwise, without loss of
generality, x_u < x_i < x_w. Let s+ < s- be the right and left slopes of f at x_i, pick s with s+ < s < s-, and put
h(x) = f(x_i) + s (x - x_i). By concavity, f(x) <= f(x_i) + s-(x - x_i) < h(x) for x < x_i, and
f(x) <= f(x_i) + s+(x - x_i) < h(x) for x > x_i. Hence f(x_i) = y_v = (y_u + y_w)/2 <= (f(x_u) + f(x_w))/2 <
(h(x_u) + h(x_w))/2 = h(x_i) = f(x_i), a contradiction. The case of g is symmetric. ∎

A point of a finite set P that is an extreme point of some convex set containing P is not in the convex hull of the other
points of P. So if every point of P is extreme in Q ⊇ conv P, then P is in convex position.

**Lemma 2.3 (convex position = cap + cup; standard, it underlies Erdős–Szekeres 1935).** Let P be x-distinct, in general
position, |P| >= 3, with leftmost point a and
rightmost point b. Then P is in convex position iff P = U ∪ L, where U is a cap from a to b and L is a cup from a to b. In
that case U = {a,b} ∪ {p : p strictly above line ab}, L = {a,b} ∪ {p : p strictly below line ab}, U ∩ L = {a,b} and
|P| = |U| + |L| - 2.

*Proof.* (<=) By Lemma 2.1(b), interior points of U lie strictly above line ab and interior points of L strictly below, so
U ∩ L = {a,b}. Let f and g be the interpolations of U and L. Then f is concave, g is convex and f >= chord >= g. Apply Lemma
2.2 on the union of their abscissae: a and b are extreme by (a), interior points of U by (b) (strict slope decrease), and
interior points of L by (b) for g. So P is in convex position.
(=>) No point of P lies on line ab (general position), so P = U ∪ L with U, L as displayed. Suppose u < v < w are
consecutive in U (by x) with orient(u,v,w) > 0, that is, v strictly below segment uw. Then v ≠ a, b, so v lies strictly
above segment ab, and x_a <= x_u < x_v < x_w <= x_b. The vertical line through v meets segment ab below v and segment uw
above v, so v ∈ conv{a,b,u,w} ⊂ conv(P \ {v}). This is a contradiction. So U is a cap, and symmetrically L is a cup. ∎

## 3. The mirror lemma (corrected and generalized `lem:mirror` of the note)

**Lemma 3.1.** Let C = (c_1, ..., c_m), m >= 1, be a cap (x_{c_1} < ... < x_{c_m}). Assume y_{c_i} > 0 for 1 < i < m and
y_{c_1}, y_{c_m} >= 0 (if m = 1, y_{c_1} > 0). Then V = C ∪ mu(C) is in convex position, and
|V| = 2m - #{endpoints of C on the x-axis}.

*Proof.* For m = 1, V is two points. Let m >= 2, let f be the interpolation of C on [x_{c_1}, x_{c_m}], and let g = -f. f is
concave with nonnegative end values, so f >= 0 >= g, and V = {(x_{c_i}, ±f(x_{c_i}))}. By Lemma 2.2 every point of V is an
extreme point of conv V. The endpoints are extreme by (a), the c_i with 1 < i < m by (b) (strict slope decrease of f), and
the mu(c_i) by (b) for g. The 2m points c_i, mu(c_i) are distinct except that c = mu(c) for an endpoint on the axis. ∎

The hypothesis y > 0 at interior points is implied by the others (an interior cap point lies strictly above the chord of
two points of height >= 0).

*Remark on the note's proof.* The note (`WRITEUP/note/symmetric_es7.tex`, `lem:mirror`) shows that the closed polygon
c_1 ... c_m mu(c_m) ... mu(c_1) turns to the same side at every vertex. That alone does not give convex position: the
closed polygon (-18,-62), (1,66), (-88,-82), (37,-76), (-7,49) turns left at every vertex and winds twice, and its vertex
(-18,-62) lies strictly inside the triangle (-88,-82), (37,-76), (1,66). One needs in addition that the polygon winds once,
for instance because it is simple. Here it is simple because its upper and lower chains are the graphs of f >= 0 and
-f <= 0 over one interval (x-monotonicity alone would not suffice). The region argument above avoids winding numbers. The
lemma itself is true.

## 4. Theorem A: the reduction

**Theorem A.** For every j >= 2: (i) N_mirror(2j) <= 2 r_j + 2; (ii) N_mirror(2j-1) <= 2 r'_j.

*Proof.* Let S be mirror-symmetric in the x-axis, in general position, with no k points in convex position. Put
R = S ∩ {y > 0} and A = S ∩ {y = 0}. Then S ∩ {y < 0} = mu(R) and |S| = 2|R| + |A|.

* (F1) |A| <= 2, since three axis points are collinear.
* (F2) R ∪ A is x-distinct. Two points p ≠ q of R with x_p = x_q would give three distinct points p, q, mu(p) on a vertical
  line. If p ∈ R and a ∈ A had x_p = x_a, then p, a, mu(p) would be collinear. Distinct axis points have distinct x.
* (F3) R ∪ A is in general position and has no k points in convex position (it is a subset of S).
* (F4) R has no j-cap. By Lemma 3.1 a j-cap C of R gives 2j >= k points C ∪ mu(C) of S in convex position.

(i) k = 2j. R is x-distinct, in general position, with no j-cap, no convex 2j-gon and hence no 2j-cup, so |R| <= r_j and
|S| <= 2 r_j + 2.

(ii) k = 2j - 1. If A = ∅, then |S| = 2|R| <= 2 r'_j. Otherwise pick a ∈ A and put X = R ∪ {a}. By (F2) and (F3), X is
x-distinct, in general position, with no (2j-1)-gon. We claim X has no j-cap. Let C be a j-cap of X. If a ∉ C, (F4) is
contradicted. The point a cannot be an interior point of C: its neighbours u, w in C lie in R, the chord uw has positive
height at x_a, a lies strictly below it, and orient(u,a,w) > 0 by Lemma 2.1. So a is the first or last point of C, and C
satisfies Lemma 3.1 with one endpoint on the axis. Then C ∪ mu(C) is a set of 2j - 1 = k points of S in convex position,
a contradiction. Hence |R| + 1 = |X| <= r'_j and |S| = 2|R| + |A| <= 2(r'_j - 1) + 2 = 2 r'_j. ∎

(In the even case an axis point cannot be used in the same way: a (j-1)-cap of R extended by one axis endpoint gives only
2j - 1 points.)

## 5. Theorem B: the far-flat construction

**Theorem B.** Let j >= 2 and let X be a finite x-distinct set in general position with no j-cap.
(i) If X has no 2j points in convex position, there is a mirror-symmetric set of 2|X| + 2 points in general position with
no 2j points in convex position.
(ii) If X has no 2j - 1 points in convex position, there is a mirror-symmetric set of 2|X| points in general position with
no 2j - 1 points in convex position.
Hence, with Theorem A: **N_mirror(2j) = 2 r_j + 2 and N_mirror(2j-1) = 2 r'_j.**

*Construction.* Translate X so that min x = min y = 0. Let W = max x, h = max y, and let g > 0 be the smallest gap between
consecutive x-coordinates (g = 1 if |X| = 1). In case (i) put D = W + 2 and A = {(W+1, 0), (W+2, 0)}. In case (ii) put
D = max(W, 1) and A = ∅. Choose an integer H with H·g > h·D, for example H = floor(hD/g) + 1. Let
R = X + (0, H) and S = R ∪ mu(R) ∪ A. Then S is mu-invariant, |S| = 2|X| + |A|, every point of R has
H <= y <= H + h, and for p ∈ R and z ∈ mu(R) ∪ A we have |x_z - x_p| <= D and y_z <= 0. A vertical translation preserves
orientations, so R has the same caps and convex subsets as X.

**Lemma 5.1 (cap lemma).** If P ⊂ S is in convex position and P ⊄ R, then P ∩ R is a cap. If P ⊄ mu(R), then
mu(P ∩ mu(R)) is a cap.

*Proof.* Let P' = P ∩ R with |P'| >= 3 (else trivial). P' is x-distinct, in general position and in convex position, so by
Lemma 2.3 P' = U ∪ L, with U a cap and L a cup from its leftmost point u to its rightmost point w. Suppose L has an interior
point q. Then q lies strictly below line uw and x_u + g <= x_q <= x_w - g. Pick z ∈ P \ R, so z ∈ mu(R) ∪ A. Then
* orient(u,w,q) < 0, since q is strictly below line uw;
* orient(w,z,q) = (x_z - x_w)(y_q - y_w) + (y_w - y_z)(x_q - x_w) <= D·h + H·(-g) < 0, because |x_z - x_w| <= D,
  |y_q - y_w| <= h, y_w - y_z >= H and x_q - x_w <= -g;
* orient(z,u,q) = orient(u,q,z) = (x_q - x_u)(y_z - y_u) - (y_q - y_u)(x_z - x_u) <= g·(-H) + h·D < 0.
By the identity orient(u,w,q) + orient(w,z,q) + orient(z,u,q) = orient(u,w,z), the barycentric coordinates of q in the
triangle uwz are orient(w,z,q)/orient(u,w,z), orient(z,u,q)/orient(u,w,z) and orient(u,w,q)/orient(u,w,z), all positive.
So q ∈ conv(P \ {q}), a contradiction. Hence L = {u,w} and P' = U is a cap. The second statement is the first one applied
to mu(P), which is in convex position, lies in S, and is not contained in R when P ⊄ mu(R). ∎

*General position of S.* Let p ≠ q be in R. Line pq has slope of absolute value at most h/g. At any abscissa x with
|x - x_p| <= D its height is >= H - hD/g > 0, so no point of mu(R) ∪ A lies on it. By symmetry no point of R ∪ A lies on a
line through two points of mu(R). For p ∈ R and q ∈ mu(R), segment pq crosses the axis at an abscissa in [0, W], and this
is the only axis point of line pq. The axis points have abscissae W+1 and W+2, so they are not on it. The line through two
axis points is the axis, which contains no other point of S. Triples inside R or inside mu(R) are not collinear because X
is in general position. Distinctness is clear (y > 0, y < 0, y = 0).

*Counting.* Let P ⊂ S be in convex position.
* If P ⊂ R or P ⊂ mu(R), then |P| <= 2j - 1 in case (i) and |P| <= 2j - 2 in case (ii), by the hypothesis on X.
* Otherwise P ⊄ R and P ⊄ mu(R). By Lemma 5.1, P ∩ R and mu(P ∩ mu(R)) are caps of R, so each has at most j - 1 points,
  and |P| <= 2j - 2 + |P ∩ A|. In case (ii), A = ∅, so |P| <= 2j - 2. In case (i), |P| <= 2j - 1 unless P ⊇ A = {a1, a2}.
  If P ⊇ A and P misses R or mu(R), then |P| <= (j-1) + 2 <= 2j - 1. If P ⊇ A and contains p ∈ R and q ∈ mu(R), then
  segment pq meets the axis at c = (x_c, 0) with x_c <= W < x_{a1} < x_{a2}, and c lies in the open segment pq. Then a1
  lies in the open segment c a2, hence in the interior of the triangle p q a2, which is nondegenerate by general position.
  So a1 ∈ conv(P \ {a1}), a contradiction.
So S has no 2j (case (i)) or 2j - 1 (case (ii)) points in convex position. Applying this to an extremal X (|X| = r_j,
resp. r'_j) and combining with Theorem A gives the equalities. ∎

**Lemma 5.2 (exact value).** For S as in the construction, maxconv(S) = max(maxconv(X), 2 cap(X) + [A ≠ ∅]).

*Proof.* "<=": Lemma 5.1 and the counting give |P| <= max(maxconv(X), 2c + min(|P ∩ A|, 1), c + |A|) with c = cap(X),
and c + 2 <= 2c + 1 since c >= 1. ">= 2c": Lemma 3.1 for a largest cap C of R. ">= 2c + 1" when A ≠ ∅: let C = c_1 ... c_m
be a largest cap of R and a1 = (W+1, 0). Then slope(c_m, a1) <= -H/(W+1) < -h/g <= slope(c_{m-1}, c_m), because
Hg > h(W+2). So C followed by a1 is a cap with one endpoint on the axis, and Lemma 3.1 gives 2m + 1 points. ∎

**Lemma 5.3 (slope form; used by `code/construct.py` and `code/lemma_check.py`).** Let X be a finite x-distinct set in
general position in [0,W] x [0,∞) with min x = 0, and let s be the largest absolute slope between two points of X. Let
H > s(W+2), R = X + (0,H), A ⊆ {(-1,0), (-2,0)} and S = R ∪ mu(R) ∪ A, and assume S is in general position (this holds for
all but finitely many H). Then maxconv(S) <= max(maxconv(X), 2 cap(X) + min(|A|,1), cap(X) + |A|).

*Proof.* (i) For p ∈ R and z ∈ mu(R) ∪ A the segment pz is vertical or has absolute slope > s: for z = mu(q), q ∈ R, the
height difference is >= 2H and the width is <= W, so the absolute slope is >= 2H/W > s; for z = (-c,0), c ∈ {1,2}, the slope
is y_p/(x_p + c) >= H/(W+2) > s.
(ii) Let P ⊆ S be in convex position with a point z ∈ mu(R) ∪ A. If P ∩ R is not a cap, Lemma 2.3 gives p, q, r ∈ P ∩ R
with x_p < x_q < x_r and q strictly below line pr. Line pr has absolute slope <= s, so at x_z ∈ [-2, W] its height is
>= H - s(W+2) > 0 >= y_z: z is strictly below line pr, like q. The points q and r lie in the cone
{p + (dx,dy) : dx > 0, |dy| <= s·dx}, which line zp meets only in p by (i), so q and r are on the same side of line zp.
Likewise p and q are on the same side of line zr. Hence q is strictly inside the triangle p z r, a contradiction. So
P ∩ R is a cap, and by symmetry mu(P ∩ mu(R)) is a cap if P has a point in R ∪ A.
(iii) For u ∈ R and l ∈ mu(R), the segment ul crosses the axis at a point c of its interior with x_c ∈ [0,W]; then (-1,0)
lies in the open segment from (-2,0) to c, so strictly inside the triangle (-2,0) u l. So P has at most one axis point if
it meets both R and mu(R).
(iv) Counting: P inside R or inside mu(R): <= maxconv(X); P inside A: <= |A|; P meeting R and A only (or mu(R) and A):
<= cap(X) + |A|; P meeting R and mu(R): <= 2 cap(X) + min(|A|,1).
General position for all but finitely many H: every orientation of a triple of S is affine in H. Triples inside R or inside
mu(R) have constant nonzero orientation. For p, q ∈ R the H-coefficient is -2(x_q - x_p) against a point of mu(R) and
-(x_q - x_p) against an axis point; for p ∈ R, l ∈ mu(R) and an axis point a it is -(x_p + x_l - 2x_a) < 0 (as x_a < 0);
two axis points and a point of R or mu(R) give ±(x_a2 - x_a1). None of these vanishes. ∎

*Remark (the form checked by `code/lemma_check.py`).* H > s(W+2) is used twice: for (i), and for "z strictly below line
pr" in (ii). Both follow from the slope condition (*): every segment from a point of R to a point of mu(R) ∪ A is
vertical or has absolute slope > s. Indeed, if x_z = x_p, line pr has height y_p > 0 >= y_z at x_z; otherwise (*) gives
y_p - y_z > s|x_p - x_z|, while the height of line pr changes by at most s|x_p - x_z| between x_p and x_z. Step (iii)
needs only that the axis points lie to the left of R. So the lemma holds under (*) for any set A of at most two axis
points to the left of R; the script checks (*) exactly, and every file in `sets/` also satisfies H > s(W+2).

With X from Lemma 6.5 and k = 2j, A = {(-1,0), (-2,0)}: maxconv(S) <= max(2j-1, 2(j-1)+1, (j-1)+2) = 2j-1. With k = 2j-1 and
A = ∅: maxconv(S) <= max(2j-2, 2(j-1), j-1) = 2j-2.

*Remarks.* (1) The placement of the axis points matters. With one axis point on each side of R, a (j-1)-cap of R, its
mirror image and both axis points can be in convex position (2j points); in a randomized exact test of a review this
happened in 360 of 400 placements. (2) The condition H·g > h·D is sufficient, not necessary: some known 46-point
extremal sets violate it. (3) A review tested Lemma 5.2 exactly on random and exhaustive grid inputs (README §9).

## 6. Theorem C: the Erdős–Szekeres/ETV block construction (lower bound for N(n,a,b))

This section is classical (Erdős–Szekeres 1935 and 1960/61; the lower bound of the ETV conjecture is the 1960/61
construction restricted to some blocks, Erdős–Tuza–Valtr 1996). It is included so that the lower bounds rest only on
written proofs given here.

**Lemma 6.1 (cups–caps sets).** For a, b >= 2 there is an x-distinct set G(a,b) in general position with C(a+b-4, a-2)
points, no a-cup and no b-cap.

*Proof.* Induction on a + b. If a = 2 or b = 2, take one point (C(b-2,0) = C(a-2,a-2) = 1; a single point has no 2-cup and
no 2-cap). Otherwise let L0 = G(a-1,b) and R0 = G(a,b-1), and let σ bound the absolute values of all slopes inside L0 and
inside R0. Put M = σ + 1 and G = εL0 ∪ ((1, M) + εR0). As ε -> 0 every cross slope tends to M, so for small ε: εL0 lies
left of the other part, and every cross slope exceeds every slope inside a part. These are finitely many strict
inequalities. Homotheties preserve orientations. A cap has strictly decreasing slopes, so its cross step, if any, comes
first: a cap is one point of εL0 followed by a cap of the right part (at most 1 + (b-2) points), a cap inside εL0 (at
most b - 1 points), or a cap inside the right part (at most b - 2 points). Symmetrically, a cup is a cup of εL0 (at most
a - 2 points) plus at most one more point, or lies inside the right part (at most a - 1). General position: two points in
one part and one in the other are not collinear, since the cross slope differs from the inner slope (Lemma 2.1). Size:
C(a+b-5,a-3) + C(a+b-5,a-2) = C(a+b-4,a-2). ∎

**Lemma 6.2 (block arrangement).** Let B_1, ..., B_m be finite x-distinct sets in general position. There are positively
homothetic copies B'_t = c_t + εB_t such that:
(i) B'_s lies entirely left of B'_t for s < t;
(ii) every slope between two points of one block exceeds every slope between points of two different blocks;
(iii) orient(p,q,r) < 0 for p ∈ B'_s, q ∈ B'_t, r ∈ B'_u with s < t < u.
For any such Y = ∪ B'_t:
(a) Y is x-distinct and in general position;
(b) every cap of Y is a cap of one block B'_s, followed by single points of later and later blocks;
(c) every cup of Y is a cup of one block, or a single point of some B'_s followed by a cup of one later block B'_t;
(d) if P ⊂ Y is in convex position, |P| >= 3, with leftmost point in B'_s and rightmost point in B'_t: if s = t then
    P ⊂ B'_s; if s < t then |P| <= κ_s + λ_t + (t - s - 1), where κ_s (λ_t) is the largest cap (cup) size in B_s (B_t).

*Proof.* Existence: let σ bound the absolute slopes inside the blocks, M = σ + 1 and c_t = (t, -M t^2). Then
slope(c_s, c_t) = -M(s+t) <= -3M < -σ - 1 and orient(c_s, c_t, c_u) = -M(t-s)(u-t)(u-s) < 0. Inner slopes do not depend
on ε. Cross slopes and cross orientations tend to those of the centres as ε -> 0. So for small ε, (i)–(iii) hold, since
they are finitely many strict inequalities.
(a) Three points of one block: general position of B_t. Two points p, p' of B'_s and q of another block: by (ii) the slope
of pp' differs from the slopes of pq and p'q, so the three points are not collinear (Lemma 2.1). Three blocks: (iii).
x-distinctness: (i) and the blocks.
(b) Slopes of a cap strictly decrease. After a cross step, an inner step would have a larger slope by (ii), so all later
steps are cross steps. Inner steps can only precede the first cross step, and then they lie in the first block.
(c) Slopes of a cup strictly increase. An inner step followed by a cross step is impossible by (ii). Two consecutive cross
steps are impossible by (iii) (orient < 0 means the slope decreases). So a cup has at most one cross step, and it is the
first step.
(d) If s = t, every point with abscissa between those of the leftmost and rightmost points lies in B'_s by (i). Let s < t,
and write P = U ∪ L as in Lemma 2.3, with U a cap and L a cup from the leftmost point a to the rightmost point b. By (b),
U consists of U ∩ B'_s (a cap of B'_s) followed by single points of distinct later blocks, the last of which is b; so
|U| <= |U ∩ B'_s| + (t - s - 1) + 1. By (c), L is a followed by a cup of B'_t ending at b; so |L| = 1 + |L ∩ B'_t|. Hence
|P| = |U| + |L| - 2 <= κ_s + (t - s - 1) + λ_t. ∎

**Theorem C (Erdős–Szekeres 1960/61; Erdős–Tuza–Valtr 1996).** For n >= 3 and 2 <= a, b <= n <= a + b - 2:
N(n,a,b) >= E(n,a,b).

*Proof.* For n - b <= i <= a - 2 let T_i = G(n-i, i+2) (Lemma 6.1): C(n-2,i) points, caps <= i+1, cups <= n-i-1. Arrange
T_{n-b}, ..., T_{a-2} from left to right by Lemma 6.2, indexing blocks by i.
* No convex n-gon: inside one block, |P| = |U| + |L| - 2 <= (i+1) + (n-i-1) - 2 = n - 2. Across blocks s < t,
  |P| <= (s+1) + (n-t-1) + (t-s-1) = n - 1.
* No a-cap: a cap is a cap of T_s (at most s+1 points) plus at most one point of each later block (at most a-2-s points),
  so it has at most a - 1 points.
* No b-cup: a cup inside T_t has at most n-t-1 <= b-1 points. A point plus a cup of a later T_t (so t >= n-b+1) has at most
  1 + (n-t-1) = n - t <= b - 1 points.
The size is E(n,a,b). ∎

**Corollary 6.3.** r_j >= (2^(2j-2) - C(2j-2,j-1))/2 and r'_j >= 2^(2j-4). The construction for r_j uses the blocks
T_i = G(2j-i, i+2), i = 0..j-2, of sizes C(2j-2,i). For r'_j it uses T_i = G(2j-1-i, i+2) of sizes C(2j-3,i).

The files in `sets/` realize these sets differently, as trees of the following composition.

**Lemma 6.4 (composition).** For finite x-distinct sets X, Y in general position write X ⊕ Y if every point of Y lies to
the right of every point of X and every slope between a point of X and a point of Y exceeds every slope inside X and every
slope inside Y. (After a shear (x, y) -> (x, y + Mx) with M large, which keeps orientations and the x-order, X lies to
the left of and deep below Y, as in the recursive step of the Erdős–Szekeres 1935 construction; after one such shear a
⊕-tree is a decomposable set in the sense of Baek–Balko.) Then X ∪ Y is x-distinct and in general position, and
cap(X ∪ Y) <= max(cap X, 1 + cap Y),
cup(X ∪ Y) <= max(cup X + 1, cup Y), maxconv(X ∪ Y) <= max(maxconv X, maxconv Y, cup X + cap Y).

*Proof.* For x1 < x2 in X and y ∈ Y, slope(x1,x2) < slope(x2,y): a cup triple (Lemma 2.1). For x ∈ X and y1 < y2 in Y,
slope(x,y1) > slope(y1,y2): a cap triple. A triple with two points in one part is not collinear (two different slopes
through a common point). A cap meeting both parts has at most one point in X (the last two points of X in it and the next
point would form a consecutive cup triple); a cup meeting both parts has at most one point in Y. This gives the cap and cup
bounds. If P is in convex position, meets both parts and |P| >= 3, Lemma 2.3 writes P = U ∪ L from its leftmost point
a ∈ X to its rightmost point b ∈ Y; then U ∩ X = {a} and L ∩ Y = {b}, so |P| <= (1 + cap Y) + (cup X + 1) - 2. ∎

**Lemma 6.5 (the ETV set as a ⊕-tree).** Let G(a,b) be one point if a = 2 or b = 2, and G(a-1,b) ⊕ G(a,b-1) otherwise.
For k >= 4 and j = ⌈k/2⌉ let T_s = G(k-s, s+2) and R = T_{j-2} ⊕ (T_{j-3} ⊕ (... ⊕ (T_1 ⊕ T_0))). Then R is x-distinct, in
general position, cap(R) <= j - 1, maxconv(R) <= k - 1 and |R| = sum_{s=0}^{j-2} C(k-2,s) (= E(2j,j,2j) for k = 2j and
2^(2j-4) = E(2j-1,j,2j-1) for k = 2j-1).

*Proof.* By Lemma 6.4 and induction, G(a,b) has cup <= max(a-2+1, a-1) = a-1, cap <= max(b-1, 1+b-2) = b-1 and
C(a+b-4,a-2) points. Put R_0 = T_0 (one point) and R_s = T_s ⊕ R_{s-1}. By induction cap(R_s) <= max(s+1, 1+s) = s+1,
cup(R_s) <= max(k-s, k-1) = k-1, and maxconv(R_s) <= max(maxconv T_s, maxconv R_{s-1}, (k-s-1) + s) = k-1, using
maxconv T_s <= (s+1) + (k-s-1) - 2 = k-2 (Lemma 2.3). ∎

## 7. Main consequences

**Theorem D.** For every j >= 2:

    N_mirror(2j)   = 2 N(2j, j, 2j) + 2    >= 2^(2j-2) - C(2j-2, j-1) + 2,
    N_mirror(2j-1) = 2 N(2j-1, j, 2j-1)    >= 2^(2j-3).

Equality on the right holds iff P(2j,j,2j), resp. P(2j-1,j,2j-1), holds. Both follow from the Erdős–Szekeres
conjecture for n = k (Prop. 7.1).

*Proof.* Theorems A, B and C, and Corollary 6.3 (the inequalities alone need only B and C). ∎

So the conjectured mirror value for even k is equivalent to the ETV conjecture on the triplets (2j, j, 2j). For odd k the
mirror maximum is at least 2^(k-2), the value the ES conjecture predicts for all sets, and equals it iff P(2j-1,j,2j-1)
holds. For even k the mirror maximum is smaller than 2^(k-2) by exactly C(k-2,k/2-1) - 2 iff P(k,k/2,k) holds. By
Baek's Theorem 1.5 (attributed there to ETV), P(2j,a,2j) for any a with j <= a <= 2j already implies P(2j,j,2j).

**Proposition 7.1 (ETV 1996; Baek's Theorem 1.5, special case).** If every set of 2^(n-2) + 1 points in general position
contains n points in convex position, then N(n,a,b) <= E(n,a,b) for every triplet (n,a,b).

*Proof.* Let X be x-distinct, in general position, with no n-gon, no a-cap and no b-cup. Take the blocks T_i = G(n-i,i+2)
for i in {0,...,n-2} \ {n-b,...,a-2}, and put X in place of the removed range. Arrange
T_0, ..., T_{n-b-1}, X, T_{a-1}, ..., T_{n-2} by Lemma 6.2 and call the result Y. Let P ⊂ Y be convex. Inside T_i,
|P| <= n-2; inside X, |P| <= n-1. Across blocks, Lemma 6.2(d) with κ(T_i) = i+1, λ(T_i) = n-i-1, κ(X) <= a-1 and
λ(X) <= b-1 gives:
* from T_s to T_t: at most (s+1) + (n-t-1) + (t-s-1) = n - 1 (if X lies between them, it counts as one block in place of
  a+b-n-1 >= 1 removed ones);
* from X to T_t (t >= a-1): at most (a-1) + (n-t-1) + (t-a+1) = n - 1;
* from T_s to X (s <= n-b-1): at most (s+1) + (b-1) + (n-b-1-s) = n - 1.
So Y has no convex n-gon, and |Y| = 2^(n-2) - E(n,a,b) + |X| <= 2^(n-2). ∎

**Corollary 7.2 (exact values for k <= 8).** N_mirror(k) = 2, 4, 8, 12, 32, 46 for k = 3, 4, 5, 6, 7, 8.

*Proof.* N(3,2,3) = N(4,2,4) = 1, since a 2-cap is any pair. N(n,3,n) = n - 1, so N(5,3,5) = 4 and N(6,3,6) = 5: an
x-distinct set with no 3-cap is a cup, an n-cup is a convex n-gon, and an (n-1)-cup attains the bound. N(7,4,7) =
C(6,2) + 1 = 16 and N(8,4,8) = C(7,2) + 1 = 22 by Baek's theorem (Theorem 1.6 in the numbering of arXiv:2206.04260v2):
"For any n ≥ 3, the statement P(n,4,n) holds. That is, C(n−1,2) + 2 points on a plane in general position determine
either a 4-cap or a n-gon", with general position including x-distinctness; the lower bounds are Theorem C. Then apply
Theorem D. ∎

Further confirmations of the two instances used: N(7,4,7) <= 16 by 17-point SAT certificates (`sat/`, README §4) and
N(8,4,8) <= 22 by 23-point SAT certificates made the same night (not in this directory); Balko–Valtr (ENDM 49, 2015)
reported both values by SAT computations over pseudolinear colourings.

## 8. Upper bounds for k >= 9

**Lemma 8.1 (Pascal step; the Erdős–Szekeres 1935 argument, with the n-gon condition carried along).** For a, b >= 3:
N(n,a,b) <= N(n,a-1,b) + N(n,a,b-1).

*Proof.* Let X be extremal and E = {p : p is the last point of an (a-1)-cap of X}. X \ E has no (a-1)-cap: the last point
of one would be in E. E has no (b-1)-cup. If c_1 ... c_{b-1} were one, c_1 would end an (a-1)-cap d_1 ... d_{a-2} c_1.
If (d_{a-2}, c_1, c_2) is a cap triple, d_1 ... d_{a-2} c_1 c_2 is an a-cap. Otherwise d_{a-2} c_1 ... c_{b-1} is a b-cup.
Both are excluded. Both parts inherit the other conditions. ∎

With N(n,a,b) <= C(a+b-4,a-2) and N(n,4,n) = C(n-1,2) + 1 = C(n,2) - (n-2) (Baek), induction on a gives
N(n,a,n) <= C(a+n-4, a-2) - (n-2) for a >= 4. Hence r_j <= C(3j-4, j-2) - (2j-2) and r'_j <= C(3j-5, j-2) - (2j-3). For
j = 5: r_5 <= 37 + 120 = 157 and r'_5 <= 29 + 84 = 113, so 188 <= N_mirror(10) <= 316 and 128 <= N_mirror(9) <= 226
(`tools/pascal_bounds.py`). Without Baek's theorem the cups–caps bounds give 240 and 332; the note's `prop:mirror`
bound 2C(3j-4,2j-2) + 2 is the latter. The Lean proof of r'_5 <= 113 (README §6) uses the mirror-image split: with
T = {first points of 4-caps}, S \ T has no 4-cap, so |S \ T| <= 29 by Baek at n = 9, and T has no 8-cup (an 8-cup ending
at the first point of a 4-cap extends to a 9-cup or to a 5-cap), so |T| <= C(9,3) = 84.

## 9. A second construction: symmetric blocks

This is the classical Erdős–Szekeres block set placed so that the reflection mu maps block i to block k-2-i; for even k
the self-paired middle block is replaced by two axis points. It is used for `sets/blocks_S_k13.txt`.

**Lemma 9.1 (block lemma).** Let k >= 3, n = k - 2, and let B_0, ..., B_n be pairwise disjoint finite sets whose union S is
in general position, such that each B_i is x-distinct, cap(B_i) <= i + 1, cup(B_i) <= k - 1 - i, and
* (A) for i < j: if p, q ∈ B_i, x_p < x_q and d ∈ B_j, then orient(p,q,d) < 0; if p, q ∈ B_j, x_p < x_q and u ∈ B_i, then
  orient(p,q,u) > 0 (each block lies below every line through two points of an earlier block, and above every line through
  two points of a later block);
* (C) for h < i < j, u ∈ B_h, m ∈ B_i, d ∈ B_j: orient(d,u,m) < 0.

Then S contains no k points in convex position.

*Proof.* Let P ⊆ S be in convex position, h = min{i : P ∩ B_i ≠ ∅}, j = max{i : P ∩ B_i ≠ ∅}. If h = j, Lemma 2.3 gives
|P| <= (h+1) + (k-1-h) - 2 = k - 2. Let h < j.
(i) P ∩ B_h is a cap, so it has at most h + 1 points. Otherwise Lemma 2.3 gives a, b, c ∈ P ∩ B_h with x_a < x_b < x_c and b
strictly below the chord ac: orient(a,c,b) < 0. Take d ∈ P ∩ B_j. By (A), orient(a,c,d) < 0, orient(c,d,b) = orient(b,c,d)
< 0 and orient(d,a,b) = orient(a,b,d) < 0. All three edge tests have the sign of orient(a,c,d), so b is interior to the
triangle acd, a contradiction.
(ii) P ∩ B_j is a cup, so it has at most k - 1 - j points: the mirror argument, with b above the chord and a point
u ∈ P ∩ B_h, all signs positive.
(iii) |P ∩ B_i| <= 1 for h < i < j. Let m, m' ∈ P ∩ B_i, x_m < x_m', u ∈ P ∩ B_h, d ∈ P ∩ B_j. By (C), orient(d,u,m') < 0
and orient(d,u,m) < 0. By (A), orient(u,m',m) = -orient(m,m',u) < 0 and orient(m',d,m) = orient(m,m',d) < 0. So m is
interior to the triangle d u m', a contradiction.
Hence |P| <= (h+1) + (j-h-1) + (k-1-j) = k - 1. ∎

**Lemma 9.2 (placement).** Let k >= 3, n = k - 2, and let T_0, ..., T_n be finite x-distinct sets in
[-W',W'] x [-H,H], W' >= 1, H >= 0, with all slopes inside each T_i at most σ in absolute value. Let c = 2W' + 3,
G >= c n^2 (H+1) + σ(c n^2 + 2W') + H + 1, t_i = 2i - n and B_i = T_i + (-c t_i^2, -G t_i). Then (A) and (C) hold, and no
triple of points meeting two or three different blocks is collinear.

*Proof.* Write X_i = -c t_i^2 ∈ [-c n^2, 0] and Y_i = -G t_i; for i < j, Y_i - Y_j = G(t_j - t_i) >= 2G.
(A) Let i < j, p, q ∈ B_i, d ∈ B_j. Line pq has absolute slope at most σ and |x_d - x_p| <= c n^2 + 2W', so at x = x_d it is
at height >= Y_i - H - σ(c n^2 + 2W'), while y_d <= Y_j + H. Since 2G > 2H + σ(c n^2 + 2W'), d is strictly below the line,
i.e. orient(p,q,d) < 0 for x_p < x_q. The second half is symmetric.
(C) Let h < i < j, u ∈ B_h, m ∈ B_i, d ∈ B_j, and write each point as block offset plus (α, β), |α| <= W', |β| <= H. Then
y_u > y_m > y_d, and orient(d,u,m) = (y_u - y_d)(x_L - x_m), where x_L = (1-λ) x_d + λ x_u is the abscissa of line du at
height y_m and λ = (y_m - y_d)/(y_u - y_d) ∈ (0,1). Put λ_0 = (t_j - t_i)/(t_j - t_h) and x_0 = (1-λ_0) X_j + λ_0 X_h. A
direct computation gives X_i - x_0 = c(t_i - t_h)(t_j - t_i) >= 4c. With A = G(t_j - t_i), B = G(t_j - t_h) >= 4G and
errors |e_1|, |e_2| <= 2H, |λ - λ_0| = |(A + e_1)/(B + e_2) - A/B| <= 4H/(B - 2H) <= 2H/G (as G >= H). Hence
x_L <= (1-λ) X_j + λ X_h + W' <= x_0 + c n^2 |λ - λ_0| + W' <= x_0 + 2 + W' (as G >= c n^2 H), while x_m >= X_i - W'. So
x_m - x_L >= 4c - 2W' - 2 > 0 and orient(d,u,m) < 0.
Non-collinearity: a triple with exactly two points in one block is non-degenerate by (A); a triple meeting three blocks
by (C). ∎

**Theorem 9.3.** For every k >= 3 there is a mirror-symmetric set of L(k) points in general position with no k points in
convex position, where L(k) = 2^(k-2) for odd k (no axis point) and L(k) = 2^(k-2) - C(k-2,k/2-1) + 2 for even k (two
axis points).

*Proof.* For 0 <= i < n/2 let T_i be an image of G(k-i, i+2) (Lemma 6.1) under an affine map of positive determinant that
keeps the x-order, placed in a box [-W',W'] x [-H,H] (such maps preserve caps, cups and general position). Put
T_{n-i} = mu T_i, and for even k put T_{n/2} = {(-1,0), (1,0)}. Choose W', H, σ as bounds for all T_i and c, G as in
Lemma 9.2. Since t_{n-i} = -t_i, B_{n-i} = mu B_i, so S = ∪ B_i is mu-symmetric, and the axis points are exactly those of
B_{n/2} (even k); for odd k every |Y_i| >= G > H. Block conditions: B_i (i < n/2) has no (i+2)-cap and no (k-i)-cup. mu
reverses orientations and keeps the x-order, so it exchanges caps and cups: B_{n-i} has no (i+2)-cup and no (k-i)-cap,
that is cap(B_{n-i}) <= (n-i) + 1 and cup(B_{n-i}) <= k - 1 - (n-i). For even k (k >= 4) the middle block has
cap = cup = 2 <= k/2. General position holds inside blocks (Lemma 6.1; mu is an isometry) and across blocks (Lemma 9.2).
Lemma 9.1 applies. The size is sum_i C(k-2,i) = 2^(k-2) for odd k, and 2^(k-2) - C(k-2,n/2) + 2 for even k. ∎

*Remarks.* (1) For odd k, Theorem 9.3 is an instance of Valtr's construction for an arbitrary skeleton, as described by
Baek and Balko (SoCG 2025, §4; they credit it to Valtr and state it without proof, citing Erdős–Szekeres 1960/61 and
Erdős–Tuza–Valtr 1996): take a mirror-symmetric skeleton and mirrored clusters. Reflection exchanges caps and cups,
which is the type change from cluster i to cluster k+2-i in their indexing, and no cluster is paired with itself because
k - 1 is even. Baek and Balko do not state the mirror consequence. (2) For even k = 2j, one axis point never creates a
k-gon from a (j-1)-cap of the upper half (2(j-1) + 1 < k), but two axis points at both ends of such a cap would (2j
points). In the construction both axis points lie to the right of all other blocks (X_i < X_{n/2} = 0 for i ≠ n/2), and
Lemma 9.1 covers every case.

## 10. What is open

Nothing mirror-specific. By Theorem D the upper bound of the conjectured even value for k = 2j is exactly the ETV statement
P(2j,j,2j): every x-distinct set in general position with (2^(2j-2) - C(2j-2,j-1))/2 + 1 points has a j-cap or a convex
2j-gon. It is known for j <= 4 (j = 4: Baek). It would follow from the ES conjecture for n = 2j (Prop. 7.1). For j >= 5
no source inspected (README §8) proves it; the first such cases are P(9,5,9) and P(10,5,10). For the even one, only
93 <= N(10,5,10) <= 157 is known here.
Likewise the odd statement N_mirror(2j-1) = 2^(2j-3) is exactly P(2j-1,j,2j-1), open from 64 <= N(9,5,9) <= 113 on.
Plain SAT at these sizes (65 and 94 points) is far beyond the 23-point instance of P(8,4,8), which already needed cube
splits in two reviews. Baek's method (slope labellings and laced cups) is developed for 4-cap-free configurations, and
his paper proves no case with a, b >= 5.
