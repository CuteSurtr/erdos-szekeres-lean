# Independent combined cut audit — PASS

**COMPUTED:** all37 added clauses, every occurrence in the39-cut receipt,
and the unchanged exact base match independent reconstruction. **PROVED
(written):** under the explicit terminal existence dependencies below,
every real n7/m14 terminal counterexample has canonical values satisfying
this strengthened CNF. This is not unconditional equivalence of abstract
formulas. No accepted UNSAT proof for the combined formula is supplied here.

## Rows and retained base

Use positive t(a,b,c) for a cup, in increasing x order. At a cut k the two
nonempty blocks are L=[0,k) and R=[k,14). The three predicates require:

| Predicate | Two L, one R | One L, two R |
|---|---|---|
| high | cup | cap |
| low | cap | cup |
| all_cup | cup | cup |

For each predicate the added clause is the disjunction of the **negations**
of these required signs. It is false exactly when the cut predicate holds,
and true exactly when at least one mixed sign violates it. Pure triples
never occur. The independent builder counts vertices belonging to L;
the separate truth evaluator quantifies over LL times R and L times RR.
Neither imports or executes the producer.

At each cut the width is k(14-k)12/2. Each family totals2,730 literals.
The low cut1 equals all_cup cut1; high cut13 equals all_cup cut13. Those
are the only duplicate clauses. The retained order is high cuts1–13,
low cuts1–13, then all_cup cuts2–12:37 rows and8,034 literals. All39 receipt
entries, including both repeated row indices, agree independently.

The frozen [highsplit audit](../highsplit_audit/VERIFY_HIGHSPLIT.md) already
reconstructed the complete32,086-entry map and exact base. Here its map
hash is pinned and all364 orientation IDs are reconstructed independently.
All231,613 original clauses and4,104,153 body bytes remain unchanged.
The combined formula has32,086 variables,231,650 clauses and631,274
literals. The full reconstructed file has SHA-256
`01de4ba0c9831690f5e64a3592fd335ef701c100224060733e9734d55ac65554`.
The base SHA-256 is
`5dc0c1719cce7bda188abad8489534413ecbbcbe5f43e1b714244ec045a129c4`;
map SHA-256 is
`b81223d78761ab200ef5931cc33ab10821a3e3a2054c5e550d0d8da7cf0fa55e`.
There are no additional variables, units, fixed signs or symmetry premises.

## Common rank and polygon facts

All arguments below concern real x-ordered GP sets with no five-cap and
no convex seven-subset. Let beta(v) be the longest cup ending at v in a
block, and c its maximum. Its top level is terminal-safe within that block.
For c>=2 and a cap triple a<b<d in the level, take a maximum cup ending
...p,a. If p,a,b were a cup, that cup would extend to length c+1 at b.
Thus p,a,b is a cap; together with a,b,d it gives the ambient four-cap
p,a,b,d ending in the required pair b,d. A selected four-cap would extend
in the same fashion to a forbidden five-cap. For c=1 the block is a
singleton. This proof supplies ambient support; it makes no assertion of
selection in smaller ambient subsets.

Every convex polygon has an upper cap and lower cup with two shared end
vertices. A block with no five-cap and cup maximum c has polygon size at
most c+2. In particular an internal hexagon has lower cup length at least4.
If c<=4, its right endpoint lies in the top rank level whenever a hexagon
exists. Convexity may also be characterized by convexity of every four-
subset: a point inside the convex hull of others lies in a triangle of
three of them. These facts justify the mixed-polygon statements below.

## High cuts

The [independent high-split proof](../highsplit_audit/VERIFY_HIGHSPLIT.md)
already establishes the required real-counterexample implication. Its
noncritical branches need no smaller-size theorem. Only the final cut13
can require a selector on the left13-point block; that precise premise
is supplied by the independently [replayed exact13 certificate](../exact_audit/replay13/README.md)
and its semantic audit. No new high-cut premise is introduced here.

## Low cuts: complete14-point coverage

For a low cut, every mixed convex subset is an L cap joined to an R cup.
To verify the criterion, a three-point part has a convex four-set with a
point from the opposite block exactly when it is a cap on the left or a
cup on the right; two points from each side have the convex --++ pattern.
Apply the all-four-subset characterization. An L four-cap followed by any
R point would make a five-cap, so L has no four-cap. Write d=maxcup(R).
Appending any left point to an R six-cup would give a seven-gon, hence d<=5.

If d=5, two L points together with a maximum R cup would make a seven-gon.
Thus L is a singleton and R has13 points. A terminal selector in R plus
that singleton is valid: all new triples are cups, old supports remain,
and every new target contains the singleton. This branch uses exact13.

If d=4, an L cap triple would join a maximum R cup to make a seven-gon.
Thus L is a cup of size at most6. Select one L point and the top rank-four
level in R. An internal L hexagon uses all L and is hit; an internal R
hexagon meets its rank-four level. A mixed hexagon has two L points and
an R four-cup, whose final point is in that level. The union is terminal-
safe: the R level is safe, and with only one L point every mixed selected
triple is a cup. This branch needs no prior-size theorem.

If d<=3, L has at most13 points and satisfies the hypotheses of T7(L).
The independently [audited classification](../low_split_audit/VERIFY_LOW_SPLIT.md)
says T7(L) is equivalent to either of the following alternatives:

1. A cup B hits all internal L hexagons and every vertex of B after its
   first ends an ambient L three-cap.
2. L partitions into cups B,D with |D|<=5.

For alternative1 select B and the top cup-rank level of R. R has no
internal hexagon (polygon bound d+2<=5). A mixed hexagon must use an L
three-cap and a maximum R three-cup, so its final R point is selected.
For a selected mixed cap a<b<r, the later L vertex b ends an L three-cap
u<v<b; u,v,b,r is the required ambient four-cap. There is no selected
mixed four-cap because B is a cup. The local R level is already safe.
For alternative2 select B alone. The blue L cup D has no hexagon, and
no mixed hexagon can survive because it would need an L cap triple.
This proves transfer to arbitrary R with d<=3, not just to a three-cup.

The left-size premise has separate explicit coverage. For |L|<=10, form
a low join of L with a three-cup by a sufficiently large downward shift.
It has no five-cap, no seven-gon and at most13 points. Its terminal selector
implies T7(L) by the classification. Existence on that join uses separately
the [through11 boundary theorem](../../boundary/audit/VERIFY_BOUNDARY.md),
[size12 audit](../audit/VERIFY_EXTENSION.md), and
[exact13 replay](../exact_audit/replay13/README.md). For left11,12,13 use
their individual audited formulas and fresh accepted proofs in
[low_split_audit/replay](../low_split_audit/replay/README.md). Those fresh
proofs also extend T7 through left14, though left14 is not needed for a
14-point nonempty cut. No monotonicity in ambient size is assumed, and
left15/16 or an all-size low-cut theorem is not inferred.

## All mixed triples cups

A cap triple in either block together with any point in the other block
has its middle point inside the resulting triangle. Consequently a mixed
convex subset is exactly two cup parts, and their union is a cup. With
c_L,c_R the two local cup maxima, c_L+c_R<=6.

If both sides have at least two points, 2<=c_L,c_R<=4. Select the union of
their top rank levels. Each is safe by the rank proof; every mixed triple
is a cup, so combining them creates no cap or four-cap. Internal hexagons
meet their local top levels by the polygon bound. A mixed hexagon forces
c_L+c_R=6 and uses a maximum cup in each side, meeting both levels at their
endpoints. This gives a terminal selector without a prior-size premise.

If one side is a singleton and the other has cup maximum<=4, the same
rank-level construction works. The only remaining case has maximum5 in
the13-point block. Its terminal selector lifts after adding the singleton,
at either end, since all new triples are cups and new targets contain it.
This case again uses exact13. This independently confirms the terminal
scope of the parent's [cup-join note](../structure2/cup_join.md); it does
not audit that note's further protection notions or make a new size claim.

## Counterexample projection and controls

A real14-point failure has the canonical exact geometric/containment flags
of the audited base. Every cut predicate above would produce a terminal
selector, contradicting failure under the cited prior theorems. All37
added clauses therefore hold for that canonical assignment. The base size
bound |A|<=9 remains sound by thinning selected vertices with the ambient
set fixed. This is precisely the real-counterexample-to-CNF implication
needed for a later certificate. The clauses can remove abstract sign
models; they are not ordinary propositional consequences of the base.

Boolean checks cover39 canonical cut assignments,8,190 mixed sign flips,
6,006 pure sign flips and12,432 exhaustive assignment/cut pairs at m4/5.
For all39 predicates, separate controls reject a wrong literal sign and
an omitted literal. Thus row polarity and inclusion of every crossing
triple are tested as well as exact byte reconstruction.

Exact real controls reuse only our frozen independent integer determinant,
triangle-containment and endpoint-rank routines, never a producer or
parent checker. Parent fixtures supply only coordinates,n,cut; expected
selectors and ranks are ignored. Additional joins are constructed using
strict rational secant bounds. Every fixture is checked for GP/no5cap/no
n-gon; local ranks are also checked by enumerating cup subsets. There are
12 cases, eight of size14;1,158 selectors/lifts,92,592 mixed-subset tests
and396 actual cut-predicate comparisons pass. They include both critical
singleton ends, an interior14-point all-cup join, low right maxima1–5,
and the supplied two-four-cap control with nonvacuous ambient supports.
Two parent26-point fixtures are explicitly skipped and replaced by our
14-point singleton constructions. These are controls, not order-type
exhaustion or an independent universal finite theorem.

## Provenance and limits

Producer SHA-256:
`d8979afcc2b2793f810f314821b4bb2d369c471d0771962f195140b56bd02c24`.
The producer source and full receipt are copied as small evidence inputs;
all input hashes are stable before/after. All checks use one CPU, AS300MiB,
wall20/CPU19, affinity5,nice10. Rows took0.517s/20,900KiB; real controls
0.482s/22,700KiB. No compile, solver, cake, long unit or outward action
was run for this packet. Frozen dependencies remain unchanged.

At07:26KST the parent's matching allcuts14-a receipt still says SOLVING.
Only an accepted cake_lpr proof for the pinned combined CNF, together with
the dependencies here, could yield a finite14 terminal theorem. No weak
Delta, ES, or global-minimality conclusion is asserted.
