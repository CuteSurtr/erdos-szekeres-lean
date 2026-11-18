# Scope and exact algorithms

This is a fixed-coordinate finite search, labeled COMPUTED. It does not
establish a universal uniform-envelope theorem. The exposure equivalence
and one/two-line domination certificates are proved in
`../../boundary/envelope/theory.md`, Sections 1–3. No approximate
optimization or SAT verdict alone is treated as a geometric conclusion.

## Coordinates, chains, and polygons

The input has increasing integer x-coordinates, at most 60 points, and
coordinate absolute values at most 10^15. Each orientation is computed
with signed 128-bit integer multiplication. Coordinate differences have
absolute value at most 2*10^15, so the determinant absolute value is at
most 8*10^30, well within 2^127. Zero determinants reject the input.
The actual pools have at most 42 points and coordinate bound 1.8*10^11;
variations scale by 1024, staying within the same safe input limit.

In x-order, a chain is a cup/cap exactly when its consecutive slopes
increase/decrease strictly. Consecutive orientation tests therefore
enumerate every such chain, without needing all its triple tests.
For each fixed first vertex a, the dynamic program stores the longest
cup/cap ending in a pair (b,c). Only reachable nonzero states extend.
The base chains are (a,c) of length two. Every chain decomposes into a
predecessor chain and its final edge, so these maxima are exact.

Every convex polygon has a unique leftmost/rightmost pair a,b and splits
into a cup and cap between them. Their internal points lie strictly on
opposite sides of the line ab, so they are disjoint. Conversely, the union
of any such cup and cap is convex. Its size is the sum of chain sizes
minus two. Taking the two longest chains with common endpoints gives the
maximum convex polygon size. Thus maxcap<5 and maxgon<n exactly validate
the requested premises.

After validity is established, all cap chains have size at most four.
Enumerate all cap and cup chains, then join those with the same endpoints
and sizes c,u satisfying c+u-2=n-1. The mask set removes any duplicates.
The preceding decomposition proves this enumerates exactly all target
polygons. Every four-cap and cap triple is also explicitly enumerated.
Resource limits may interrupt enumeration; such a result is a failure or
UNKNOWN, never an accepted model.

## Exposure and the membership formula

A terminal line is represented by integers (dy,z,dx), with dx>0, meaning
its slope is dy/dx and its height at M=max_x(U) is z/dx. For a candidate q
and ambient line ell, subtract their slope/height numerators using a
common positive denominator. The exact inequality q(t)>ell(t) is
`ds*t+dz>0`. Positive ds imposes a strict lower bound -dz/ds; negative ds
imposes a strict upper bound; equal slopes either forbid exposure or add
no bound. Intersect with t>0 using integer cross-products. Empty exposure
is additionally witnessed by a single dominating ambient line or the
exact rational two-line convex combination from the prior theory.
Nonempty exposure gets an exact interior test t, explicitly checked
against every ambient line.

The CNF has one variable per point, true iff it belongs to A:

- every target polygon contributes its all-positive membership clause;
- every old four-cap contributes its all-negative membership clause;
- every exposed cap triple contributes its all-negative membership clause.

The first two families are exactly old weak Delta; the third is precisely
uniform envelope safety, by the prior theorem. No four-cap row is omitted.
Every SAT assignment is checked against every clause. A second Python
implementation then rechecks all premises, no four-cap in A, no target
polygon in its complement, and a rational domination certificate for
every cap triple of A. It imports no finder geometry. This within-track
check is distinct from the parent's independent audit.

The optional `terminalsafe.cnf` replaces the exposure triples by every
cap triple whose last pair is not the last pair of an ambient four-cap.
Under the validated no-five-cap premise these are exactly rank-three
terminal pairs. It retains the other two clause families. This track
emits that formula for the parent but does not solve or minimize it.

## Coordinate variations and limits of coverage

Each variation changes one y-coordinate. Each determinant involving that
vertex is affine in the displacement. Take the smallest positive root
in the proposed direction among determinants that could change sign,
move 7/8 of the way toward it, and round toward zero after scaling all
coordinates by 1024. The move cannot reach a zero determinant. The code
also compares every triple sign before and after the move. With no finite
root it uses a bounded fraction of the vertical span. x-order is preserved.

Thus each accepted variation preserves the original order type and the
geometric premises, but may change terminal-line exposure. Every variation
still receives a fresh geometry check, complete coordinate CNF, SAT model
check and direct geometric replay. This finite sample does not exhaust
coordinate realizations or establish uniform safety from orientation data.

## Controls and evidence

The control suite checks exact maximum cup/cap/polygon sizes against
exhaustive subsets and hulls, and checks every target/cap row on 55 small
coordinate cases (41 valid, 14 deliberately or naturally invalid).
All candidate terminal pairs in valid controls agree with a separate
Fraction-based test at all line intersections and the final slope.
Algebra cases exercise the necessary two-line branch, open endpoints,
equal slopes, empty ambient family, and an interior exposure interval.
The old-four-cap example checks that exposure safety cannot replace the
four-cap clauses. These controls do not prove the implementation correct.

An UNSAT verdict is only COMPUTED and must trigger a frozen input packet,
an immediate parent notification, independent clause audit and retained
cake_lpr-checked LRAT before any CERTIFIED claim. UNKNOWN and check errors
are preserved. No negative result is reinterpreted as a theorem.
