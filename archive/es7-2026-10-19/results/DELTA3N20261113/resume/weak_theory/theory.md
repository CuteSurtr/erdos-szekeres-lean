# Weak Delta: extreme-point thresholds and a monotone repair obstruction

**PROVED (written argument):** the extension criterion and terminal-edge
criterion below, plus the sharp repair bound and its propagation. Exact
coordinate controls are in findings.json and independent_check.json.
Neither weak D(5,7) nor weak D(5,8) is proved. No novelty claim is made.

## 1. Definitions

All sets are real, finite, in general position, with distinct x-coordinates.
Write p<q for x(p)<x(q), and let ell_pq(X) be the height at abscissa X of the
line through p,q. A j-cap has strictly decreasing consecutive slopes.
Put k=n-1, where the applications have n=7 or 8. A weak Delta in U is a
four-cap-free A subset U meeting every convex k-gon in U. It may itself
contain convex k-gons; it need not meet a polygon's lower chain.

Let r=(X,Y) be to the right of every point of U. For j>=3 define

    F_j(U;X) = max {ell_bc(X): some j-cap in U has last two vertices b,c}.

The maximum of an empty family is minus infinity. The two thresholds relevant
here are F_3(A;X) and F_4(U;X).

## 2. Exact thresholds (PROVED)

**Lemma 1.** If U has no (j+1)-cap, then U union {r} has no (j+1)-cap iff
Y>F_j(U;X). In particular, if U has no five-cap and A subset U has no four-cap,

    U+r has no five-cap iff Y>F_4(U;X),
    A+r has no four-cap iff Y>F_3(A;X).

**Proof.** Every new cap must end at the rightmost point r. A j-cap ending
...b,c extends by r iff slope(b,c)>slope(c,r), equivalently Y<ell_bc(X).
Strictly decreasing consecutive slopes are sufficient for a cap. Conversely,
deleting r from a new (j+1)-cap gives precisely such a j-cap. General position
excludes equality with every eligible line, so the stated inequalities are
equivalent. The empty-family convention covers the absence of j-caps. QED.

**Theorem 2 (dominated-threshold extension).** Suppose U has no five-cap,
A is a weak Delta in U, and r is rightmost with U+r still five-cap-free.
If

    F_3(A;X) <= F_4(U;X),

then A union {r} is a weak Delta in U union {r}. The weaker, exact condition
Y>F_3(A;X) also suffices for this particular r.

**Proof.** Lemma 1 gives Y>F_4(U;X)>=F_3(A;X), hence A+r is four-cap-free.
Every old target k-gon is hit by A; every new one contains r. QED.

No no-(k+1)-gon hypothesis was used. Hence this applies in particular to
valid (5,n) instances and does not require an induction in n or cup-side hits.
For a fixed X, the threshold comparison guarantees extension for *every*
five-cap-free placement of r on that vertical line.

**Corollary 3 (ambient terminal-edge certificate).** It suffices that, for
every three-cap a,b,c in A, its last pair b,c is the last pair of some four-cap
u,v,b,c in U. Then A+r is a weak Delta for every rightmost r preserving
five-cap-freeness.

**Proof.** Every line in the defining maximum for F_3(A;X) then occurs in the
maximum for F_4(U;X), at every X. Apply Theorem 2. Equivalently, a proposed
blocking cap a,b,c,r would imply the five-cap u,v,b,c,r. QED.

If h_U(b,c) is the maximum cap length ending in the ordered pair b,c, a
blocking triple a,b,c necessarily has h_U(b,c)=3: it is at least three,
at most four, and the value four is excluded by the preceding argument.
Thus only terminal pairs of ambient rank exactly three need be tested.
This is a geometric restriction on the exact cap blockers, not a claim that
all such triples actually block r. Their line-height inequality remains
necessary.

## 3. Exact deletion-only extension (PROVED)

Let A be a weak Delta in U=S minus {r}. Define

    B_r(A) = {{a,b,c} subset A: a,b,c,r is a four-cap},
    T_A = {H intersect A: H is a convex k-gon in U}.

**Lemma 4.** For R subset A, (A minus R) union {r} is a weak Delta in S iff

1. R meets every triple of B_r(A), and
2. no member of T_A is contained in R.

**Proof.** An old four-cap cannot appear after deleting points of A. Every
new four-cap contains r and is removed exactly when R hits its other three
points. Old polygons keep a hit exactly when their old support is not entirely
deleted; all polygons containing r acquire a hit. QED.

**Useful sufficient consequence.** If the blocker family has a transversal
of size t and every old k-gon has at least t+1 points in A, deleting such a
transversal and adding r works. The terminal-edge restriction above can reduce
the blocker family before its transversal is sought. This consequence is
combinatorial, unlike the line-height and terminal-edge assertions.

**Private-hit obstruction.** Suppose {a,b,c} is a blocker and each q in
{a,b,c} has an old polygon H_q with H_q intersect A={q}. No deletion-only
extension with r red exists: breaking the cap deletes at least one q and
loses H_q. If A also misses a k-gon containing r, leaving r blue cannot work,
even after arbitrary deletions from A.

More generally, if A is inclusion-minimal as a weak Delta in U, every
nonempty deletion loses an old polygon. Such an A admits this monotone
extension iff it is already a weak Delta in S or A+r is four-cap-free.

## 4. Sharp smallest-size monotone obstructions

**Proposition 5 (PROVED).** If |S|<=n+1 and A is a weak Delta in S minus {r},
then either A is already a weak Delta in S or A union {r} is one. The point r
need not be extreme, and no five-cap or n-gon restriction is needed here.

**Proof.** If A misses a target polygon H, H has n-1 points, contains r, and
is disjoint from A. Consequently |A|<=|S|-(n-1)<=2. Then A+r has at most three
points and hence no four-cap. It hits the old polygons by hypothesis and all
new polygons at r. QED.

The threshold is sharp for *arbitrary-old-Delta monotone extension*, even
among valid (5,n) real sets and even with r rightmost. The following exact
fixtures have n+2 points. In each, A has three vertices, T=A+r is a four-cap,
and B=S minus T has n-2 vertices. Every B+t, t in T, is a convex (n-1)-gon.
Thus A is a weak Delta in S-r simply because its complement there has only
n-2 points. Each B+q, q in A, is a private polygon, and B+r is the missed
new polygon. The private-hit obstruction proves that *no* subset of A,
with either color assigned to r, is a full weak Delta.

These coordinate predicates are **COMPUTED**, not SAT-certified. The logical
obstruction given those predicates is the written proof above. A completely
different full Delta exists: the singleton {0} works in both fixtures.

### n=7: nine points

```
0=(19177,-21808)   1=(25783,9497)    2=(37372,-22731)
3=(44405,-21278)   4=(51652,6136)    5=(52152,-51)
6=(52672,32131)    7=(63579,63430)   8=(67591,-9280)
```

Here r=8, A={4,6,7}, and B={0,1,2,3,5}. The retained source indices are
{0,2,5,6,7,8,9,10,11} in DELTA2's `restr_ends_weak_a5_n7_m12_real.json`.

### n=8: ten points

```
0=(8030,-15070)     1=(11105,45305)    2=(35376,-23390)
3=(125287,-34578)   4=(143356,-22746)  5=(148656,23516)
6=(149156,-12964)   7=(150244,48374)   8=(151892,58675)
9=(157253,-2952)
```

Here r=9, A={6,7,8}, and B={0,1,2,3,4,5}. The retained source indices are
{0,1,3,6,7,8,9,10,11,12} in DELTA2's `restr_ends_weak_a5_n8_m13_real.json`.

The lower bound in Proposition 5 makes these globally smallest by total
number of points for this precise extension obstruction at their respective
parameters. This says nothing about the minimum size of a Delta counterexample.
No search over all order types is needed for that size-minimality conclusion.

**Proposition 6 (exact form at the threshold, PROVED).** At |S|=n+2, a weak
Delta A of S-r admits no full weak Delta of the form C or C+r, C subset A,
iff |A|=3, T=A+r is a four-cap, and every B+t, t in T, is a convex (n-1)-gon,
where B=S minus T. This does not require r to be extreme.

**Proof of necessity.** Since A fails with r blue, it misses a target polygon
H containing r; hence |A|<=3. Since A+r also fails and all its polygon hits
are automatic, it contains a four-cap, so |A|>=3. Thus |A|=3, T is that cap,
and H=B+r by cardinality. For q in A, the set (A minus {q})+r has only three
points and is cap-free. Its failure must be an old polygon missing it. The
only available n-1 vertices are B+q, so B+q is a polygon. Sufficiency is the
private-hit argument of Section 3. QED.

## 5. Propagating this obstruction to larger n (PROVED)

Suppose a valid (5,n) obstruction has the form in Section 4, and its leftmost
point b belongs to B. Insert a point l just to the left and above b so that:

1. replacing b by l in any old triple preserves its orientation;
2. (l,b,q) is a cup for every other old point q.

Such a placement exists. Choose a negative slope M smaller than all slopes bq
and set
l=(x(b)-epsilon, y(b)-M epsilon). The second condition holds by the choice of
M; all finitely many strict old triple signs are preserved for small enough
positive epsilon. Choose epsilon avoiding all finitely many collinearities.

The enlarged set is (5,n+1)-valid. A five-cap using l but not b would project
to an old five-cap; one using both has the cup turn l,b,q and is impossible.
Any convex (n+1)-gon would, on deleting l if present, contain an old convex
n-gon. Put B'=B+l and leave T and r unchanged.

Each B'+t is convex: in the old polygon B+t, replace the first vertex b of
the upper chain by l and prepend l to its lower chain. The upper chain signs
are preserved by condition 1, and the new lower turn l,b,q is a cup by
condition 2. Both chains now have the same endpoints l and the old rightmost
vertex and retain all old vertices. Their union is convex and has n points.

Therefore the same private-hit proof gives a monotone obstruction on n+3
points at parameter n+1. Iterating the nine-point base establishes sharp
obstructions for every n>=7. The two explicit target fixtures above do not
depend on running or numerically approximating this construction.

This is a lift of a *repair-rule obstruction*, not a lift of a counterexample
to weak Delta or to the cup-side conjecture.

## 6. Failed construction and exact remaining gap

An attempted simpler construction placed a common cup before four cap vertices.
The concrete last blue point (-1,-20) and proposed cap
(0,0),(1,10),(2,18),(3,24) form a five-cap. It was rejected before use. This
failed control is retained in the data; it supplies no valid Delta instance.

The exact unproved step for a deletion proof of D(5,n) is to select a favorable
old Delta, or to allow additions/recolorings of old blue points with preserved
coverage. Theorem 2 and Corollary 3 give sufficient tests for a favorable choice;
they do not assert that every valid deletion has one. The n-gon-free hypothesis
has not yet been used to force such a choice. The parent is independently
investigating maximal red sets; none of its results is assumed here.
