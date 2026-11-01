# Centrally symmetric sets of 2^(k−2) points without a convex k-gon, k even

Written 1 November 2026 (UTC); the six fixes asked for by the review (`review/README.md`) are applied.

**Theorem.** For every even k ≥ 6 there is a set S of 2^(k−2) points in the plane, in general position, with S = −S
and 0 ∉ S, that contains no k points in convex position.

**Status.** Written proof, refereed by an independent review (`review/README.md`), which found it correct and complete.
Not machine-checked.

**Credit.** The theorem is implied by known results, although no source inspected states it (`README.md`, "Credit and
status" and §6): k = 6 by the fourfold symmetric 16-point sets of Subercaseaux, Mackey, Qian and Heule
(arXiv:2506.00224v1, App. C) and of Mackey's thesis (CMU-CS-25-108), and every even k ≥ 8 by Baek and Balko's blow-up
lemma (SoCG 2025, Lemma 14) applied to such a 16-point set with a half-turn-symmetric labelling that is not a threshold.
The ingredients G(a, b) are the Erdős–Szekeres sets, and Lemma 3 adapts the Valtr / Erdős–Szekeres blow-up argument
(Remarks on Lemma 3). The proof below is an independent, self-contained proof. It does not use Lemma 14, whose proof is
omitted in the SoCG version.

The statement is false for k = 4: four centrally symmetric points in general position form a parallelogram. The proof
uses k ≥ 6 in exactly one place (Step 4 of Lemma 3), where a configuration of 4 points cannot be excluded.

## 0. Conventions

General position: no three points collinear. cross(u, v) = u_x v_y − u_y v_x and orient(a, b, c) = cross(b − a, c − a).

For a set with distinct x-coordinates, a *chain* is a sequence of its points with increasing x. A chain p_1, …, p_s is
an *s-cup* if orient(p_{i−1}, p_i, p_{i+1}) > 0 for all 1 < i < s (slopes strictly increase), and an *s-cap* if all
these are < 0 (slopes strictly decrease). Chains of at most 2 points are both. A contiguous piece of a cup (cap) is a
cup (cap).

**Fact 0.1** (standard). Let P be in general position with distinct x-coordinates, |P| ≥ 3, in convex position, and
let a, b be its leftmost and rightmost points. The points of P on or below the line ab, in x-order, form a cup L from a
to b. The points on or above form a cap U from a to b. L ∩ U = {a, b}, so |P| = |L| + |U| − 2.

**Fact 0.2.** The half-turn h(p) = −p preserves orientation (orient(−a, −b, −c) = orient(a, b, c)) and reverses the
x-order. The image of a chain p_1, …, p_s is the chain −p_s, …, −p_1, whose turns are
orient(−p_{i+1}, −p_i, −p_{i−1}) = −orient(p_{i−1}, p_i, p_{i+1}). Hence h maps cups to caps and caps to cups. A map
(x, y) ↦ (αx + t_1, βy + t_2) with α, β > 0 preserves the x-order and orientation signs, hence cups, caps and general
position.

## 1. Two ingredients

**Lemma 1 (Erdős–Szekeres).** For integers a, b ≥ 2 there is a set G(a, b) of C(a+b−4, a−2) points in general
position, with distinct x-coordinates, with no a-cup and no b-cap.

*Proof.* Induction on a + b. If a = 2 or b = 2 take one point. Otherwise let L = G(a−1, b) and R = G(a, b−1), and
translate R strictly to the right of L and then far up. Then every slope between L and R exceeds every slope inside L
or inside R. General position: a line through two points of one part has a smaller slope than any segment joining the
parts. A cup meeting both parts has its L-points first. It has only one point in R, because after the jump slope any
slope inside R is smaller. Its L-part is a cup in L, so it has at most (a−2) + 1 = a − 1 points. A cup inside one part
has at most a − 1 points. A cap meeting both parts has only one point in L, because a slope inside L followed by the
larger jump slope is impossible in a cap. So it has at most 1 + (b−2) = b − 1 points. Size:
C(a+b−5, a−3) + C(a+b−5, a−2) = C(a+b−4, a−2). ∎

**Lemma 2 (symmetric middle set).** For m ≥ 2 there is a set M_0 with the following properties:
- M_0 = −M_0, 0 ∉ M_0, |M_0| = C(2m−2, m−1);
- general position and distinct x-coordinates;
- no (m+1)-cup and no (m+1)-cap;
- all slopes in (−1/2, 1/2);
- every point (u, v) satisfies |v| < |u|/2.

*Proof.* Let X = G(m, m+1), which has no m-cup, no (m+1)-cap and C(2m−3, m−2) points. For t > 0 let
X_t = {(−4 + t g_x, −1 + t² g_y) : g ∈ X} and M_0 = X_t ∪ (−X_t). As t → 0:
- slopes inside X_t and inside −X_t equal t·(slopes of X), so they tend to 0;
- slopes between the parts tend to slope((−4, −1), (4, 1)) = 1/4;
- the points tend to ±(4, 1).

Fix t small enough that the inside slopes lie in (−1/8, 1/8) and the between slopes in (1/8, 3/8). Also require
X_t ⊂ {x < 0} and |v| < |u|/2 for all points. Then:
- *Symmetry and size.* M_0 = −M_0, 0 ∉ M_0, and
  |M_0| = 2·C(2m−3, m−2) = C(2m−3, m−2) + C(2m−3, m−1) = C(2m−2, m−1).
- *Distinct x and general position.* Distinct x holds because X has distinct x and the two parts are separated.
  General position follows from Fact 0.2 inside each part, and from the slope gap for a triple with two points in one
  part.
- *No (m+1)-cup.* X_t lies to the left of −X_t. A cup meeting both parts has at most m − 1 points in X_t and, because
  of the slope gap, at most 1 point in −X_t, so at most m in total. A cup inside X_t has at most m − 1 points. A cup
  inside −X_t has at most m points: X_t has no (m+1)-cap, and Fact 0.2 turns caps of X_t into cups of −X_t.
- *No (m+1)-cap.* h(M_0) = M_0 and h exchanges cups and caps. ∎

M_0 is an instance of the recursion step of Lemma 1 for G(m+1, m+1), with the right part chosen as the negative of the
left part.

## 2. The blow-up lemma

Fix an even k ≥ 6, and let n = k − 2 and m = k/2. The *base abscissae* x_0 < … < x_n are

  x_j = 2j − n + 1 (j < n/2),   x_{n/2} = 0,   x_j = 2j − n − 1 (j > n/2),

that is {x_j} = {−(n−1), …, −3, −1, 0, 1, 3, …, n−1}, with x_{n−j} = −x_j.

**Fact 2.1.** For pairwise distinct a, b, c: x_a + x_b + x_c = 0 iff {a, b, c} = {j, n/2, n−j} for some j ≠ n/2.
(A sum of three odd numbers is odd. If one of the three is 0, the other two must be opposite.)

**Lemma 3 (blow-up lemma).** Let S be a finite set in general position, partitioned into clusters B_0, …, B_n, such
that
- (H0) all points of S have distinct x-coordinates;
- (H1) for i < j, every point of B_i is to the left of every point of B_j;
- (H2) every slope between points of different clusters exceeds every slope between two points of one cluster;
- (H3) if a < b < c, x_a + x_b + x_c ≠ 0, and p ∈ B_a, q ∈ B_b, r ∈ B_c, then
  sign orient(p, q, r) = sign(x_a + x_b + x_c);
- (H4) if j < n/2, p ∈ B_j, q ∈ B_{n/2}, r ∈ B_{n−j} and x(p) + x(r) ≠ 0, then
  sign orient(p, q, r) = −sign(x(p) + x(r));
- (H5) B_j has no (j+2)-cup and no (k−j)-cap (0 ≤ j ≤ n).

Then S contains no k points in convex position.

*Proof.* Let P ⊆ S be in convex position with |P| ≥ 3. Let B_l and B_r contain its leftmost point u_0 and its
rightmost point w.

*Case l = r.* By (H1), P ⊆ B_l. By Fact 0.1 and (H5), |P| ≤ (l+1) + (k−l−1) − 2 = k − 2.

*Case l < r.* Let L (cup) and U (cap) be as in Fact 0.1.

**Step 1 (shape of the chains).** Suppose L has two points in a cluster B_c with c ≠ l. By (H1) the points of L in B_c
are consecutive in L; take the first two, y and y'. Then y ≠ u_0, and the predecessor of y lies in a cluster to the
left. By (H2) the slope into y exceeds slope(y, y'), which is impossible in a cup. So L has at most one point in each
cluster ≠ B_l; in particular L ∩ B_r = {w}. The points of L in B_l form an initial segment L_0, which is a cup in B_l,
so |L_0| ≤ l + 1 by (H5).

The same argument applies to U, using the last two points of U in a cluster B_c, c ≠ r, and the successor of the
second one. So U has at most one point in each cluster ≠ B_r, and U ∩ B_l = {u_0}. The points of U in B_r form a final
segment U_0, which is a cap, so |U_0| ≤ k − r − 1.

Write the other points of L as p_{c_1}, …, p_{c_t} (p_{c_i} ∈ B_{c_i}, l < c_1 < … < c_t < r) and those of U as
p'_{d_1}, …, p'_{d_s} (l < d_1 < … < d_s < r). Then L = L_0, p_{c_1}, …, p_{c_t}, w and
U = u_0, p'_{d_1}, …, p'_{d_s}, U_0, so

  |P| = |L| + |U| − 2 = |L_0| + |U_0| + t + s ≤ k − (r − l) + t + s.   (*)

**Step 2 (two sign conditions).** Put c_{t+1} := r and d_0 := l.

If t ≥ 1, the turn of L at p_{c_1} is (e, p_{c_1}, p_{c_2}), where e is the last point of L_0 and p_{c_2} := w if
t = 1. The three points lie in clusters l < c_1 < c_2 and the turn is positive. By (H3) (a zero sum gives the
inequality trivially),

  Σ_L := x_l + x_{c_1} + x_{c_2} ≥ 0.

If s ≥ 1, the turn of U at p'_{d_s} is (p'_{d_{s−1}}, p'_{d_s}, f), where f is the first point of U_0 and
p'_{d_0} := u_0. This turn is negative, so by (H3)

  Σ_U := x_{d_{s−1}} + x_{d_s} + x_r ≤ 0.

**Step 3 (disjointness except in one configuration).** Suppose t = 0, or s = 0, or t, s ≥ 1 with c_1 > d_s. Then the
clusters c_i and d_i are pairwise distinct and lie strictly between l and r. So t + s ≤ r − l − 1, and (*) gives
|P| ≤ k − 1.

Otherwise t, s ≥ 1 and c_1 ≤ d_s. Since l ≤ d_{s−1}, c_1 ≤ d_s, c_2 ≤ r, and the x_j increase, we get
0 ≤ Σ_L ≤ Σ_U ≤ 0. Every comparison is then an equality:
- d_{s−1} = l, so s = 1;
- c_1 = d_1;
- c_2 = r, so t = 1;
- x_l + x_{c_1} + x_r = 0, so by Fact 2.1 c_1 = n/2 and r = n − l, with l < n/2.

**Step 4 (the exceptional configuration).** Now L = L_0, q, w and U = u_0, q', U_0, with q, q' ∈ B_{n/2},
e, u_0 ∈ B_l and f, w ∈ B_{n−l}. The two turns give

  orient(e, q, w) > 0,   orient(u_0, q', f) < 0.

Since u_0 is leftmost and w rightmost in P, x(u_0) ≤ x(e) and x(f) ≤ x(w). Hence

  σ_U := x(u_0) + x(f) ≤ x(e) + x(w) =: σ_L.

By (H4), σ_L ≠ 0 forces σ_L < 0, and σ_U ≠ 0 forces σ_U > 0. The four cases:
- σ_L ≠ 0 ≠ σ_U: σ_U > 0 > σ_L ≥ σ_U, impossible.
- σ_L = 0 ≠ σ_U: σ_U > 0 = σ_L ≥ σ_U, impossible.
- σ_L ≠ 0 = σ_U: σ_L < 0 = σ_U ≤ σ_L, impossible.
- σ_L = σ_U = 0: then x(u_0) = x(e) and x(f) = x(w), so e = u_0 and f = w by (H0). Thus L_0 = {u_0}, U_0 = {w} and
  P = {u_0, q, q', w}. Here q ≠ q', because q lies on L, q' lies on U, and L ∩ U = {u_0, w}. So |P| = 4 < k.

In every case |P| ≤ k − 1. ∎

**Remarks on Lemma 3.**
- Lemma 3 uses no symmetry. Without the middle cluster, i.e. with a base in general position, it reduces to the
  Valtr / Erdős–Szekeres argument; Steps 3–4 deal with the forced collinear base triples (x_j, 0, −x_j).
- Baek and Balko's Lemma 14 needs a base in general position, so it does not apply to this base.
- For l < n/2 − 1, Step 4 is not needed: there r − l = n − 2l ≥ 4, and (*) with t = s = 1 gives |P| ≤ k − 2. Only
  l = n/2 − 1 needs (H4).

## 3. The construction and the theorem

For j < n/2 let G_j = G(j+2, k−j) (Lemma 1), and let M_0 be as in Lemma 2 with m = k/2. Put q_j = (x_j, x_j³), so
q_{n−j} = −q_j. For 0 < ε < 1 define

  B_j = {q_j + (ε g_x, ε² g_y) : g ∈ G_j} (j < n/2),   B_{n−j} = −B_j (j < n/2),   B_{n/2} = ε² M_0,

and S_ε = ∪_j B_j. Each outer cluster has size of order ε; the middle cluster has the much smaller size of order ε².

**Theorem.** For every even k ≥ 6 and all sufficiently small ε > 0, S_ε is a set of 2^(k−2) points in general position
with S_ε = −S_ε and 0 ∉ S_ε, and it contains no k points in convex position.

*Proof.* We check symmetry, size, general position and (H0)–(H5); Lemma 3 then gives the claim. Each condition below is
a finite list of strict inequalities about finitely many points, whose coordinates are polynomials in ε. For most of
them the inequality holds in the limit ε → 0, and hence for all small ε. For (H4), and for the general-position check
of the triples (p, q, −p) with q in the middle cluster, the orientation itself tends to 0; there the sign is read from
its leading term after division by ε, respectively ε², as done below. Points of B_j are within Cε of q_j, and points of
B_{n/2} within Cε² of 0; C depends only on the G_j and M_0.

*Symmetry, size.* B_{n−j} = −B_j by definition, and B_{n/2} = −B_{n/2} because M_0 = −M_0. Also 0 ∉ M_0 and q_j ≠ 0
for j ≠ n/2. The clusters are disjoint by (H1), and
|S_ε| = Σ_{j<n/2} 2·C(k−2, j) + C(k−2, n/2) = Σ_{j=0}^{n} C(k−2, j) = 2^(k−2).

*(H0), (H1).* Base abscissae differ by at least 1. Inside a cluster the x-coordinates are distinct because the G_j and
M_0 have distinct x-coordinates.

*(H2).* Slopes inside B_j (j ≠ n/2) equal ε·(slopes of G_j), which tend to 0. Slopes inside B_{n/2} are the slopes of
M_0, which lie in (−1/2, 1/2). A slope between B_a and B_b (a < b) tends to
(x_b³ − x_a³)/(x_b − x_a) = x_a² + x_a x_b + x_b² = ½((x_a + x_b)² + x_a² + x_b²) ≥ 1.

*(H3).* For the cubic, orient(q_a, q_b, q_c) = (x_b − x_a)(x_c − x_a)(x_c − x_b)(x_a + x_b + x_c), which has the sign
of x_a + x_b + x_c when a < b < c. When this is nonzero, continuity gives the same sign for small ε.

*(H4).* Let j < n/2, p = q_j + e and r = −(q_j + e'), where e = (ε g_x, ε² g_y) and e' = (ε g'_x, ε² g'_y) with
g, g' ∈ G_j. Let q = ε² μ with μ ∈ M_0. The identity

  orient(p, q, r) = cross(p − r, q) − cross(p, r)

gives two terms:
- cross(p − r, q) = O(ε²);
- −cross(p, r) = cross(q_j + e, q_j + e') = cross(q_j, e' − e) + cross(e, e') = x_j³ ε (g_x − g'_x) + O(ε²).

Since x(p) + x(r) = ε(g_x − g'_x),

  orient(p, q, r) = x_j³ (x(p) + x(r)) + O(ε²).

For j = 0, G_0 has one point, so x(p) + x(r) = 0 always and (H4) is vacuous. For j ≥ 1, if x(p) + x(r) ≠ 0 then
|x(p) + x(r)| ≥ ε δ_j, where δ_j > 0 is the least x-gap in G_j. Since x_j³ ≤ −1, the sign is −sign(x(p) + x(r)) for
small ε.

This is where the middle cluster must be small. The argument needs its size to be small compared with ε δ_j, the least
x-gap inside the outer clusters; the scale ε² is sufficient, not necessary (in exact computations of the review, a
middle cluster at scale ε^(3/2) also works for k = 6 at ε = 2^−10, 2^−16, 2^−24 and for k = 8 at 2^−16 and 2^−24, but
not for k = 8 at 2^−10). At a scale comparable with the outer clusters, cross(p − r, q) ≈ 2 cross(q_j, q) dominates,
and both signs occur because M_0 = −M_0; see Remark 3.

*(H5).* B_j (j < n/2) is an image of G_j under a map as in Fact 0.2, so it has no (j+2)-cup and no (k−j)-cap.
B_{n−j} = −B_j has no (k−j)-cup and no (j+2)-cap. With j' = n − j these bounds read j' + 2 and k − j', as required.
B_{n/2} has no (m+1)-cup or cap, and m + 1 = n/2 + 2 = k − n/2.

*General position.* Three points in one cluster are not collinear, since every cluster is an affine image of some G_j
or of M_0. Two points in one cluster and one in another are not collinear by (H2). For three clusters a < b < c with
x_a + x_b + x_c ≠ 0, use (H3). Otherwise, by Fact 2.1 the triple is (B_j, B_{n/2}, B_{n−j}) with j < n/2. If
x(p) + x(r) ≠ 0, use (H4). If x(p) + x(r) = 0 then g = g' (the x-coordinates of G_j are distinct), so r = −p and
orient(p, q, −p) = 2 cross(p, q) = 2ε² cross(p, μ). As ε → 0, cross(p, μ) → cross(q_j, μ) = x_j(μ_y − x_j² μ_x). This
limit is nonzero: x_j ≠ 0, and Lemma 2 gives |μ_y| < |μ_x|/2, which forces μ_x ≠ 0 and hence |μ_y| < x_j²|μ_x|. So
orient(p, q, −p) ≠ 0 for small ε. ∎

**Remarks.**
1. For even n, the base x_i = 2i − n, which is used for odd k in the proposition labelled `prop:B` in
   `WRITEUP/note/symmetric_es7.tex` (the construction of `SYM2`), has unforced zero-sum triples when k ≥ 8 (for example
   −6 + 2 + 4 = 0 for k = 8), so it is degenerate there. For k = 6 (n = 4) only the forced triples occur. We use odd
   abscissae plus 0 instead, which leaves only the forced triples (x, 0, −x) for every even k.
2. A "split middle", with k clusters on a centrally symmetric base without centre, does not work by itself. The four
   central base points form a parallelogram, and the count produces a k-gon. This was confirmed exactly for k = 6 and 8
   (`logs/negative_controls.log`; `review/logs/extensions.log`).
3. A middle cluster at a scale δ with ε ≪ δ ≪ 1 fails (argument sketched here, not written in full). In Step 4 the sign
   of orient(e, q, w) is then that of 2 cross(q_l, q), i.e. it depends on which side of the line through 0 and q_l the
   point q lies. Since M_0 = −M_0, both sides occur. So a full (k/2−1)-cup of B_{n/2−1}, a point q of the middle
   cluster on one side, q' = −q on the other side, and a full (k/2−1)-cap of B_{n/2+1} are in convex position: k
   points. The review confirmed this exactly for k = 6 and 8 with δ = ε^(1/2) and ε^(1/4) (`review/logs/remark3.log`).

## 4. Integer instances

`construct.py K FILE` builds integer sets for k = 6, 8 and 10 from the same ingredients (the same base abscissae, the
sets G_j and M_0), but with a different scaling from Section 3. The outer clusters are copies of G_j stretched
horizontally by an integer factor c (their vertical extent is not reduced) and placed at Λ·(x_j, x_j³); the middle
cluster M_0 keeps its own integer coordinates. Here c ≥ max(16·slope_max, 8R_M, 8H_max) + 1 and
Λ ≥ max(4096R_c, 16R_c²/c), rounded up to a power of 10. Here slope_max and H_max are the largest absolute slope and
the largest height of the G_j, and R_c and R_M are the largest values of |x| + |y| on the centred, stretched G_j and on
M_0.

These sets are therefore not members of the family S_ε. They are covered by Lemma 3 directly: (H0)–(H5) and general
position are verified for them exactly, and their largest convex subsets are also computed directly (`README.md` §4).
