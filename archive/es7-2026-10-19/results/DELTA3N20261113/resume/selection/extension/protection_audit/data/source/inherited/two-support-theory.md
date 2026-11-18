# Two supports are necessary in real five-cap-free geometry

**PROVED (written).** The example below refutes the one-support strengthening
of the prior envelope lemma. It also shows that exposure depends on more
than triple orientations. These are statements about one line and a
specified weak Delta; they assert no failure of a Delta selection problem
and no universal selection existence theorem.
No Lean formalization, external independent verification, or novelty claim
is made. Exact computational checks are recorded separately.

## 1. Definitions and statement

Points are indexed from zero in increasing x order. A cap has strictly
decreasing successive edge slopes. For M=max_x(U) and t>0, a pair bc has
terminal line ell_bc(M+t)=s_bc*t+z_bc. Let F be the maximum of the terminal
lines of all four-caps in U. A cap-triple terminal line q is safe when
q(t)<=F(t) for every t>0, and exposed otherwise.

For two affine lines, one dominates the other on all t>0 exactly when its
slope and value at t=0 are both at least as large. The prior two-support
lemma in [the envelope proof](../../boundary/envelope/theory.md) allows a
convex combination of two ambient lines as a certificate of safety.

**Proposition.** There is an eight-point real five-cap-free set in general
position, with distinct integer x coordinates, and a cap-triple terminal
line that is safe but has no one-line ambient certificate. Moving just one
point while preserving all triple orientations makes that same terminal
line exposed. The x coordinates and the target triple remain fixed.

## 2. The geometric family

For 3<=h<=5, use

| Index | Point |
|---|---|
| 0 | (0,0) |
| 1 | (1,1) |
| 2 | (2,0) |
| 3 | (3,4) |
| 4 | (4,-3) |
| 5 | (5,10) |
| 6 | (6,-2) |
| 7 | (7,h) |

Every member is in general position, all have the same triple orientations,
and their complete list of four-caps is

    (0,1,2,4), (2,3,5,6), (2,3,5,7).                         (1)

Here is a full finite determinant certificate. For row (a,b), the middle
column lists D(a,b,c) for c=b+1,...,6 in order; an empty dash means there is
no such c. The last two columns give D(a,b,7) at the indicated h.
D(a,b,c) is the signed determinant of p_b-p_a and p_c-p_a; a negative
value denotes a cap triple. The table accounts for all 56 triples.

| (a,b) | c=b+1,...,6 | h=3 | h=5 |
|---|---|---:|---:|
| (0,1) | -2, 1, -7, 5, -8 | -4 | -2 |
| (0,2) | 8, -6, 20, -4 | 6 | 10 |
| (0,3) | -25, 10, -30 | -19 | -13 |
| (0,4) | 55, 10 | 33 | 41 |
| (0,5) | -70 | -55 | -45 |
| (0,6) | — | 32 | 44 |
| (1,2) | 5, -1, 13, 2 | 8 | 10 |
| (1,3) | -17, 6, -21 | -14 | -10 |
| (1,4) | 43, 11 | 30 | 36 |
| (1,5) | -57 | -46 | -38 |
| (1,6) | — | 28 | 38 |
| (2,3) | -11, -2, -18 | -17 | -15 |
| (2,4) | 29, 8 | 21 | 25 |
| (2,5) | -46 | -41 | -35 |
| (2,6) | — | 22 | 30 |
| (3,4) | 20, 15 | 27 | 29 |
| (3,5) | -30 | -26 | -22 |
| (3,6) | — | 21 | 27 |
| (4,5) | -25 | -33 | -31 |
| (4,6) | — | 9 | 13 |
| (5,6) | — | 17 | 19 |

All entries are nonzero. The determinants involving point 7 are affine in
h and have the same strict sign at both endpoints, so no orientation
changes for any 3<=h<=5. Scanning for decreasing successive slopes gives
exactly (1); equivalently each four-cap has all four triple determinants
negative. The target triple (0,3,6) is a cap because D(0,3,6)=-30.

There is no five-cap. Any five-cap would extend one of the three four-caps
in (1) on the right. For 0124 the possible new endpoints 5,6,7 give last
turns D(2,4,5)=29, D(2,4,6)=8, D(2,4,7)=2h+15, all positive. For 2356 the
only possible endpoint 7 gives D(5,6,7)=h+14>0. The four-cap 2357 has no
point to its right. Thus none can extend.

## 3. Two ambient lines are necessary

Take h=5. At X=7+t the line q of terminal pair 36 and all three ambient
lines are

    q(t)   = -2t - 4,
    L24(t) = -3t/2 - 15/2,
    L56(t) = -12t - 14,
    L57(t) = -5t/2 + 5.

The rational weights 1/2,1/2 give

    (L24(t)+L57(t))/2 = -2t-5/4 = q(t)+11/4.

This weighted mean never exceeds max(L24,L57), so q is below F for every
t>0, with a positive exact margin. Each individual ambient line fails:

* L24(0)=-15/2<-4=q(0), so it fails on an initial positive interval;
  explicitly L24(1)=-9<q(1)=-6.
* L57 has slope -5/2<-2, so it eventually falls below q;
  explicitly L57(20)=-45<q(20)=-44.
* L56 has smaller slope and smaller initial height than q;
  explicitly L56(1)=-26<q(1)=-6.

This covers the complete ambient family, proving the claimed necessity of
two supporting lines. It does not assert minimality of eight points.

## 4. Exposure changes inside one order type

Keep points 0,...,6 unchanged and set h=3. The target q and the first two
ambient lines are unchanged, while L57(t)=-7t/2+3. Therefore

    q-L24 = (7-t)/2,
    q-L56 = 10t+10,
    q-L57 = 3t/2-7.

All three inequalities q>Li hold exactly when

    14/3 < t < 7.                                          (2)

Thus q is exposed. At t=6, q=-16, whereas L24=-33/2, L56=-86 and L57=-18,
so F=-33/2<q. If an insertion witness is desired, r=(13,-65/4) lies strictly
between F and q. It is in general position with U, preserves absence of
five-caps, and creates the four-cap (0,3,6,r). The first two assertions
follow respectively by direct determinants and the ambient threshold:
every possible new five-cap must extend an old four-cap, but r lies above
all their terminal lines. This witnesses only the individual triple's
exposure, without imposing or making a claim about an n-gon restriction.

The same computation describes the full family. For 3<=h<=5,

    L57(t) = ((h-10)/2)*t+h.

Its slope is below -2 and its height at zero is above -4. L24 has slope
above -2 and height below -4; L56 is below q throughout t>0. The exposure
conditions reduce to

    2(h+4)/(6-h) < t < 7.

Consequently q is safe exactly when h>=34/9. At the transition h=34/9
the interval is empty: touching the envelope is safe, not exposure.
For h>=34/9 the weights

    lambda=1/(7-h) on L57,  1-lambda on L24

match the slope of q and give height surplus

    lambda*L57(0)+(1-lambda)*L24(0)-q(0)
      = (9h-34)/(2(7-h)) >= 0.

No single ambient line dominates q anywhere in this parameter family.
The order of the four slopes and the order of their values at t=0 remain
unchanged throughout, even as exposure changes. The determinant table
already proved that all primal triple orientations stay fixed too.

## 5. A specified weak Delta, and the valid (5,7) insertion

Let A={0,3,6}. On either eight-point set, A has no four-cap simply because
it has three points. Its complement has only five points, so A
automatically meets every convex six-gon. Thus A is a weak Delta.
Exact exhaustive hull checks give maximum cap, cup and convex polygon
sizes (4,4,6) for both old sets: they are valid (5,7) sets, not merely
five-cap-free examples. The complement of A has maximum convex polygon
size four. These are separate COMPUTED exact geometry checks; the parent
also independently reported the same maxima using endpoint-chain DP,
without importing this track's code.

For h=5, the envelope proof above implies that **this same A**, enlarged by
any rightmost insertion r preserving five-cap-freeness, remains a weak
Delta. There is only one triple to check in A, namely 036. A+r contains
no four-cap because its terminal line is below the ambient envelope.
It meets every old six-gon via A and every new six-gon via r. In particular
this holds if insertions must also preserve absence of seven-gons.

For h=3 and r=(13,-65/4), the full nine-point set still has maximum cap,
cup and convex polygon sizes (4,4,6), so this is a valid (5,7) extension.
A+r contains the four-cap (0,3,6,r), and therefore is not a weak Delta.
The conditional property “this A plus every valid rightmost r is a weak
Delta” has changed although all old triple orientations are identical.

**This is not a monotone-extension failure.** Keeping A unchanged and
placing r in its complement still gives a weak Delta of the nine-point
set. Its complement has maximum convex polygon size four. The exhaustive
check finds no new convex six-gon containing r; in particular A misses no
new target. A+r also meets all targets; its failure is solely its four-cap.
The parent independently reported the same cap/cup/polygon and complement
maxima. This statement concerns the displayed insertion, not all possible
insertions with r kept outside A.

## 6. Consequences for exact encoding, and limits

The same labeled orientation assignment describes h=3 and h=5, but the
truth of exposure for cap triple 036 differs. Hence no Boolean predicate
of those triple orientations alone can exactly recover exposure for every
fixed realization. This remains true on the fixed x grid 0,...,7.

An exact coordinate-based selection encoder can compute the required
intervals or use the two-support certificates. An abstract encoding needs
additional soundly constrained data about terminal lines and their
intersections, or a proved relaxation with the desired implication. Merely
guessing exposure flags is not justified by this example. Replacing safe
triples by triples with one supporting ambient line is strictly stronger
and can discard genuinely safe triples.

The h=3 member also gives a geometric counterexample to testing only the
height at t=0 and the final slope: q(0)=-4<F(0)=3 and slope(q)=-2 is below
the largest ambient slope -3/2, yet (2) is nonempty. An interior envelope
test or equivalent intersection comparison is necessary.

Nothing here shows that the stronger one-support selection rule has no
Delta solution on this set. The result refutes orientation-only
classification of exposure, or of uniform extension-safety for a specified
weak Delta. It does not refute orientation invariance of existence of some
whole uniform Delta, which has a different quantifier. General uniform
selection, weak Delta, and numerical ES bounds are unaffected.
