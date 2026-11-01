# SYM2: an explicit centrally symmetric set of 32 points with no convex 7-gon (and 2^(k-2) points for every odd k)

## Result

`sym7_32points.txt` lists 32 points with integer coordinates (absolute values at most 1,250,000). The set

- is centrally symmetric: it equals its image under (x, y) -> (-x, -y), and the origin is not one of the points;
- is in general position: no three points are collinear;
- has no 7 points in convex position.

So it is a 2-fold rotationally symmetric extremal set for the Erdős–Szekeres problem with k = 7 (2^(k-2) = 32 points).

Context. Subercaseaux, Mackey, Qian and Heule, "Automated Symmetric Constructions in Discrete Geometry" (arXiv
2506.00224, 2025), Section 6.2: on 32 points only s-fold rotational symmetry with s in {1, 2, 4} is possible for a
7-gon-free set, and no realizable 4-fold one exists. Their conclusion lists the realization of a 2-fold symmetric 32-point
construction without a convex 7-gon as future work, says they suspect symmetric constructions exist for all k >= 7, and
calls the known extremal construction asymmetric. The set here is such a 2-fold realization, and the
construction below gives one for every odd k. With their 4-fold result, 2 is the largest order of rotational symmetry
of a 32-point set without a convex 7-gon.

**Attribution.** The existence of such sets for every odd k follows from published work.
- Baek and Balko (*The Erdős–Szekeres Conjecture Revisited*, SoCG 2025, Definition 13, Lemma 14 and §6.1) describe a
  construction due to Valtr. It blows up an arbitrary base of k - 1 points in general position into 2^(k-2) points
  without a convex k-gon, using clusters with cup and cap parameters x_i = i - 1 and y_i = k - i - 1.
- For odd k, take a centrally symmetric base and pair each cluster with its negative. The half-turn exchanges cups and
  caps and the two parameters, so the union is centrally symmetric.
- After a quarter-turn, the cubic construction below is a special case: base points on the curve y = x³ and
  Erdős–Szekeres cup-cap sets as clusters.

So this directory does not give a new general construction method. Its contribution is the explicit symmetric
specialization, a short direct proof via the cubic, and exact integer coordinates. These answer the concrete
realization task named in arXiv 2506.00224. Whether the symmetric corollary was stated explicitly anywhere before has not
been established.

The 32-point set is not known to be the largest centrally symmetric set without a convex 7-gon. Excluding 34 points is
open; see `results/WRITEUP/SYMMETRIC.md`, §4.

## Verification

- `python3 verify.py sym7_32points.txt 7`: exact integer arithmetic. Checks distinctness, central symmetry, no collinear
  triple, and the size of the largest subset in convex position (6), by the dynamic program in `convex.py`
  (anchored at the lowest vertex, O(n^4)). `test_convex.py` compares it with brute force on 300 random sets: 0 mismatches.
- `brute.c` (independent of the dynamic program; reads the orientation signs that `verify.py` writes): every one of the
  C(32, 7) = 3,365,856 seven-point subsets is tested, using that a subset in general position is in convex position iff
  no point lies in a triangle of three others. Result: 0 in convex position. For comparison, 27,055 of the 906,192
  six-point subsets are in convex position.
- `sym9_128points.txt`: the same construction for k = 9: 128 points, centrally symmetric, no three collinear, largest
  convex subset 8 (`python3 verify.py sym9_128points.txt 9`, dynamic program only).
- `build.py` regenerates both sets (`sym(7, X=50, Y=10000, K=3)` and `sym(9, X=10**15, Y=10**15, K=10**9)`).

## Construction and proof (every odd k)

Notation. Points are sorted by x. An a-cup is a sequence of a points with increasing slopes between consecutive points,
an a-cap one with decreasing slopes. A set in convex position is the union of its lower chain (a cup) and its upper
chain (a cap), which share the leftmost and the rightmost point. The half-turn h(p) = -p maps cups to caps and caps to
cups (it reverses the x-order and keeps slopes). For a, b >= 2, G(a, b) is the Erdős–Szekeres set of C(a+b-4, a-2)
points in general position with no a-cup and no b-cap (`build.py: g`).

Construction. Let k be odd, n = k - 2, and x_i = 2i - n for i = 0..n (odd integers, x_{n-i} = -x_i). For i < n/2 let C_i
be a copy of G(i+2, k-i), shrunk and flattened by an affine map (x, y) -> (εx, ε²y), placed at the point (x_i, x_i³) of
the curve y = x³. For i > n/2 let C_i = h(C_{n-i}). Let S be the union of the C_i. Since y = x³ is symmetric under h,
S = h(S), and |S| = sum_i C(n, i) = 2^n = 2^(k-2). Every C_i has no (i+2)-cup and no (k-i)-cap: for i > n/2,
C_{n-i} has no (k-i)-cup and no (i+2)-cap, and h swaps the two.

Theorem. For ε small enough, S is in general position and has no k points in convex position.

Proof. Three different clusters have collinear centres only if x_a + x_b + x_c = 0, which is impossible for three odd
numbers. Together with the flatness of the clusters, this gives general position for small ε. The coordinates in the files
are checked exactly.

Slopes. A segment inside a cluster has slope of absolute value below some η (small with ε). A segment from C_a to
C_b with a < b has slope within η of s(a, b) = x_a² + x_a x_b + x_b², which is at least 1. For a < b < c,
s(b, c) - s(a, b) = (x_c - x_a)(x_a + x_b + x_c), whose absolute value is at least 4. So consecutive jumps between
clusters compare like the signs of x_a + x_b + x_c.

Let P in S be in convex position, with its leftmost point p in C_l and its rightmost point q in C_r.
If l = r, then P lies in one cluster C_l, and |P| <= (l + 1) + (k - l - 1) - 2 = k - 2.
Let l < r, U the lower chain and A the upper chain of P.

- U has increasing slopes. After its first jump between clusters, it cannot use a segment inside a cluster. So U is a
  cup in C_l (at most l + 1 points), then single points in clusters l < c_1 < ... < c_t < r, then q. With c_0 = l
  and c_{t+1} = r, increasing slopes mean x_{c_{j-1}} + x_{c_j} + x_{c_{j+1}} > 0 for every j. These sums increase with
  j, so the condition is the same as x_l + x_{c_1} + x_{c_2} > 0 (if t >= 1).
- A has decreasing slopes. A segment inside a cluster cannot come before a jump, and A must reach q in C_r. So A is p,
  then single points in clusters l < d_1 < ... < d_s < r, then a cap in C_r (at most k - r - 1 points, ending at q).
  With d_0 = l and d_{s+1} = r, decreasing slopes mean x_{d_{j-1}} + x_{d_j} + x_{d_{j+1}} < 0 for every j, which is
  the same as x_{d_{s-1}} + x_{d_s} + x_r < 0 (if s >= 1).
- Lemma: if t, s >= 1, then d_s < c_1. Otherwise c_1 <= d_s. Since l <= d_{s-1}, c_2 <= r and x is increasing,
  0 < x_l + x_{c_1} + x_{c_2} <= x_{d_{s-1}} + x_{d_s} + x_r < 0, a contradiction. So the clusters used by U and by A
  between l and r are different, and t + s <= r - l - 1.
- Count. |P| = |U| + |A| - 2 <= (l + 1 + t + 1) + (1 + s + k - r - 1) - 2 = (k - 1) + (t + s) - (r - l - 1) <= k - 1. ∎

On the classical convex curve, the half-turn would send the curve to a concave one. The odd cubic is concave on one
side and convex on the other, and the Lemma shows that this costs nothing: the upper chain can only use clusters
to the left of all the clusters the lower chain uses.

## Even k

Centrally symmetric 2^(k-2)-point sets without a convex k-gon do not exist for k = 4: four centrally symmetric points
form a parallelogram. For k = 6 they exist, because the paper above has 4-fold symmetric 16-point examples. For even
k >= 8 the question stays open here. The construction above needs a middle cluster at the centre, which is collinear
with every symmetric pair of cluster centres. `build.py: sym_even` fails for k = 4, 6 and 8 (largest convex subset k).
