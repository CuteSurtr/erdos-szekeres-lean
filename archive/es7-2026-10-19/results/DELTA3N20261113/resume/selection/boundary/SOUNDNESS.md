# Boundary formulas: written soundness

**PROVED reductions; solver outcomes require their own checks.** All sets
are finite, in general position, with distinct x-coordinates. A weak Delta
has no four-cap and hits every whole convex (n-1)-gon. Terminal-safe means
that every three-cap in it ends in a pair of ambient cap rank four.

## Complement obstruction

At |U|=2n-3, the previous cup-rank proof supplies a terminal-safe Delta if
U has no (n-2)-cup. An (n-1)-cup also works, since its complement has n-2
points. Otherwise the maximum cup length is n-2. Every such cup is safe;
it works unless its entire (n-1)-point complement is convex. Thus failure
of terminal-safe selection implies the complementary-cup obstruction in
`complement.cpp`. The converse does not hold: the real fixtures refute it.

Each new cup flag is equivalent to the conjunction of every triple sign
being positive. The existential positive row requires such a cup. Negative
all-triple rows prohibit longer cups, and the implication from each cup
flag to the complement's exact convexity flag is literal. No orientation
pinning or symmetry is imposed. The old mode has |U|=2n-3; root mode adds
one last label, imposes no-five-cap/no-n-gon on the whole set, but applies
the cup/complement conditions only to the old labels.

## Full-set long cups

If a set S contains a cup C of size |S|-n+1, and this number is positive,
then every prescribed r belongs to a weak Delta. If r is outside C, use
C+r; if r is in C, add any one point outside C instead. The resulting set
has |S|-n+2 points, contains r, and has no four-cap: any four of its points
include three from a cup. Its complement has n-2 points and so contains no
target. In our n>=6 boundary domain an outside point always exists.

Consequently a rooted failure at |S|=2n-2 cannot have an (n-1)-cup anywhere
in S. `refine.py` appends all negative all-triple rows for root-containing
(n-1)-subsets; the old ones already occur in the base. This is a necessary
restriction, not a sufficient characterization of rooted failure.

## Exact terminal-safe failure

`terminal_boundary.py` uses the old complementary-cup obstruction and adds
these families:

1. Each four-set cap flag is equivalent to all four triple signs being
   negative.
2. For every a<b<c, a bad-triple flag is equivalent to the triple being a
   cap and *none* of the four-caps u<v<b<c existing. These are exactly the
   cap triples whose last pair has cap rank three in a five-cap-free set.
3. For each A with 0<=|A|<=|U|-n+2, a failure row requires a bad triple
   inside A or a convex (n-1)-subset inside U-A.

Under no-five-cap, absence of bad triples also excludes four-caps. If
a<b<c<d were a four-cap in A, its prefix a,b,c must be bad: a four-cap
ending b,c would extend through d to a forbidden five-cap. Thus family 3
expresses failure of terminal-safe selection on its complete size range.
Exact equivalences admit the canonical assignment and prohibit invented
cap/bad witnesses. Larger terminal-safe solutions can be shrunk to
|U|-n+2, preserving safety and leaving only n-2 complement points. Smaller
solutions are explicitly tested: growing a safe two-set to three is not
presumed possible.

Therefore UNSAT of the full terminal formula, if independently validated
and certified, would show terminal-safe selection for every (5,n)-valid
U of size 2n-3. The earlier written theorem covers all smaller sizes. Such
selection permits every rightmost extension preserving five-cap-freeness,
even if that extension introduces an n-gon. This interpretation remains
conditional until the result-level checks are complete. SAT only gives an
abstract signotope candidate until exact realization and semantic checks.
