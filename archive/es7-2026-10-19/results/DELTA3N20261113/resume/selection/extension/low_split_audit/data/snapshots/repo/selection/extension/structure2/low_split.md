# Low-split follow-up: the remaining branch is explicit

**PROVED partial reduction; the general hard case remains unresolved.**
This is separate from the frozen high-split packet. No unconditional
low-cut SAT clauses are justified here.

Fix n>=5. Suppose U=L disjoint-union R is a nonempty x-separated split
with every LLR triple a cap and every LRR triple a cup. Assume no five-cap
and no n-gon. Put d=maxcup(R). The mirrored chain/polygon statements give

    1<=d<=n-2,   maxcap(L)<=3,
    mixed convex subsets = a cap in L plus a cup in R.

The parent's two easy cases are sound. If d=n-2, L is a singleton;
adjoining it preserves any protected Delta of R, because all new selected
triples are cups. If d=n-3, L is a cup of size at most n-1. The set
{v in R: beta_R(v)=n-3} plus any one L point is terminal-safe and hits
all targets. The rank-level and target arguments are the same as in
case (ii) of the high-split proof with the indicated sides changed.

## Proved part of the hard case

Suppose d<=n-4 and **maxcup(L)<=n-2**. Let

    B={v in L: beta_L(v)=n-2},
    C={v in R: beta_R(v)=d},       A=B union C.

There is no internal R target: its polygon bound is d+2<=n-2.
An internal L target has lower cup length at least n-2, since L has no
four-cap. Its right endpoint therefore has beta_L=n-2 and belongs to B.
A mixed target can occur only when d=n-4, and then it consists of an L
three-cap and a maximum R cup. The latter's last point belongs to C.

B is a cup: a cap triple within one beta_L level would extend left to
a four-cap in L, impossible. C is terminal-safe within R by the ordinary
single-rank lemma. A selected mixed cap triple has two first vertices in
B and its last vertex in R. The first two vertices have equal global
cup-ending rank n-2, so the same rank lemma gives an ambient four-cap
on its terminal pair. Mixed LRR triples are cups. There is no selected
four-cap: one wholly in a block is already excluded; a mixed four-cap
would require three L vertices forming a cap, impossible in B.

This proves terminal-safe selection for the hard case under the displayed
additional cup bound, without assuming L is decomposable. In particular
it covers the original n7, maximum-cup-five subclass whenever a low-split
cut exists. The only remaining hard branch has maxcup(L)=n-1.

### The parent's smaller endpoint choice

The terminal polygon lemma in `../../../../a4/theory.md`, Section 1.2, applies
directly to L with k=n-1: it needs no external root and no n-gon assumption.
Let E be the right endpoints of all internal L targets. The absent
(n-1)-cup forces each such polygon to have an upper three-cap and lower
(n-2)-cup. Hence every e in E ends an L three-cap. If e1<e2<e3 formed a
cap, the no-four-cap extension fact would append e2 to an (n-2)-cup ending
at e1, making a forbidden (n-1)-cup. Thus E is a cup; the same prior lemma
also gives |E|<=n-3.

One may use E in place of B above. If d=n-4, keep C as displayed; every
selected LLR cap a,b,r is protected by an L three-cap ending at b followed
by r. If d<=n-5, there are no mixed targets, so take C empty. For n=5,
the hard case has d=1 and R is a singleton; its rank-one level is harmless.
The parent's endpoint argument therefore passes without an extra root.

## Exact obstruction to the naive symmetry

Choosing all of L is a hitting set in the hard case because R has no
internal targets, but it need not be terminal-safe. L has no four-cap,
so a cap triple lying wholly in L has no ambient four-cap ending at its
last pair: a later R point cannot be a preceding cap witness. This is
why the high-split choice of the whole far block cannot be mirrored.

Write alpha_L(v) for the longest cap ending at v in L. For a selected
mixed cap a<b<r with a,b in L and r in R, its pair (b,r) is an ambient
End4 pair if and only if alpha_L(b)=3. Indeed a mixed four-cap consists
of three L cap vertices followed by one R point. This gives a precise
sufficient subproblem for the remaining branch: find a cup B in L that
hits every internal target and has alpha_L(b)=3 at every selected vertex
after the first. Then B together with C above is terminal-safe.

For the particularly adversarial choice R=a d-cup with d=n-4, every mixed
target uses all of R. Terminal selection therefore has two possibilities:

1. Select an R point. The L part must be a cup transversal of the internal
   targets with the alpha condition just stated.
2. Select no R point. The L part must be a cup meeting all internal
   targets and every three-cap in L.

This is an exact structured terminal problem for that choice of R,
not a restatement of arbitrary uniform-envelope selection. Failure would
refute a terminal low-cut reduction, not weak Delta or uniform existence.

## Exact elimination of the right block, every n>=5

**PROVED equivalence, without asserting the predicate always holds.**
For fixed L with no four-cap and no n-gon, define T_n(L) to mean at least
one of the following:

* A cup B meets every internal (n-1)-gon of L, and every selected point
  after its first ends a three-cap in L.
* L partitions into cups B and D, with |D|<=n-2.

Then these three statements are equivalent:

1. T_n(L).
2. A low-split join of L to an (n-4)-cup has a terminal-safe weak Delta.
3. Every low-split join of L to a nonempty five-cap-free R with
   maxcup(R)<=n-4 has a terminal-safe weak Delta.

All such joins automatically satisfy the geometric hypotheses: maximum
cap at most four; internal L polygons have size below n; internal R
polygons have size at most maxcup(R)+2<=n-2; and mixed polygons have size
at most 3+maxcup(R)<=n-1.

For 1 -> 3 in the first alternative, take

    A=B union {v in R: beta_R(v)=maxcup(R)}.

The R level is terminal-safe. Every selected LLR cap has a second L
vertex b ending a three-cap in L; appending its selected R point gives
the required ambient four-cap. LRR triples are cups, and B itself is a
cup. These facts also exclude all selected four-caps. Internal L targets
meet B. Mixed targets can occur only at maxcup(R)=n-4 and then use a
maximum R cup, whose endpoint meets the R rank level. There are no
internal R targets. This construction works even when there are no
mixed targets; selecting the R level is optional in that subcase.

In the second alternative, A=B alone suffices. Its complement in L is
a cup of size at most n-2, so has no internal target and no three-cap.
Any mixed target would need a three-cap in that L complement; smaller
d gives no mixed target at all. Again there are no internal R targets.
The selected B has no cap triples, hence is terminal-safe.

The implication 3 -> 2 is immediate. For 2 -> 1, any terminal selector
has a cup B as its L part. If it selects an R point, each pair of selected
L points must have its second endpoint ending an L three-cap, exactly as
proved above. Its B meets all internal targets, giving the first
alternative. If it selects no R point, every L three-cap gives a mixed
target by joining all of the canonical (n-4)-cup R. Therefore L minus B
is a cup; internal target coverage further forces its size at most n-2.
This gives the second alternative. QED.

This equivalence is geometric, and does not assume that L is recursively
decomposable. It transfers a proved/checked left-block predicate to all
right-block shapes; it does not turn finite positive probes into a proof
that every L satisfies T_n.

## Exact n7 classification reviewed for the parent's specialized CNF

Let L have no four-cap and no seven-gon, and low-join it to a three-cup R.
The full U is automatically (5,7)-valid: its cap maximum is at most four,
and a mixed polygon has at most 3+3=6 vertices. Every terminal selector
has a cup B=A intersection L, because no ambient four-cap can end in a
pair wholly in L. The two alternatives above become:

* **Parent Option 1 (R selected):** B is a cup, hits every internal
  hexagon, and every selected b after its first point satisfies
  End3_L(b). Any nonempty R selection hits every mixed hexagon. Conversely
  any such B works with just one R point. These conditions also exclude
  old four-caps: there is no three-cap in B, while an LRR triple is a cup.
* **Parent Option 2 (R unselected):** both B and L minus B are cups, and
  |L minus B|<=5. The complement must be a cup to hit every L three-cap
  times all of R; once it is a cup, it avoids internal hexagons exactly
  when its size is at most five. Since L has no seven-gon, |B|<=6.
  Thus this alternative is impossible for |L|>=12; at |L|=11 its sizes
  must be exactly 6+5.

The grid/fixed-fixture code calls Parent Option 1 `kindII` and Parent
Option 2 `kindI`, following the earlier paragraph's order. This naming
difference does not change either condition.

For m_L>=5, Parent Option 1 need only enumerate
|B|<=min(6,m_L-5). Its cup and End3-after-first conditions are hereditary
under taking subsets. If a successful B leaves fewer than five points in
its complement, thin B until the complement has exactly five points;
coverage is then automatic. The independent bound six follows because
B is a cup in a seven-gon-free L. B empty and singleton must remain
eligible. End3_L(b) must be defined exactly as the OR of all negative
triples ending at b when its negation is used in a failure clause.

No independent encoder was built by this track. The parent reported
accepted LRATs for left sizes eleven and twelve on 14 November, with the
new encoder's semantic audit pending. Those reports are not integrated
as finite theorems in this proof record.

**Transfer to arbitrary R (conditional).** If the two-option classification
has a positive answer for every admissible L, it resolves every n7
low-split hard case d<=3, regardless of the size/shape of R. For d=3,
Parent Option 1 combines its B with the beta_R=3 level; Parent Option 2
needs no R points because the L complement is a cup. For d<=2 there are
no mixed targets, so either cup B alone suffices. The case d=4 is already
proved above; d=5 remains the singleton-left reduction to R. This transfer
does not remove that critical-case induction premise.

## Bounded adversarial plan

Use a complete small n5 integer grid for L with no four-cap, no five-gon
and maximum cup four. Test the two structured cup-transversal options
above exactly, and retain explicit failures of tempting single-level or
two-level shortcuts. Add only a few prescribed n7 left blocks; no pool
sweep, coordinate hillclimb, generic terminal CNF or long job is intended.
No theorem will be inferred from a positive grid.

Cup-ending vertex ranks need not increase along an arbitrary cup. Any
argument that treats them as strictly increasing without an additional
reason is invalid; no such assumption is used in the proved partial case.

The first bounded n5 grid is complete: 109 remaining-branch left blocks
among 19,608 configurations. Each has a type-II cup; three have no type-I
cup. Twenty-two blocks are missed by both individual top rank levels,
and sixty-two have a cap in their union. Exact examples and all counts
are retained in `data/low_left_n5_grid.json`; this does not prove the
general cup-transversal subproblem.

A concise failed rank shortcut uses

    L=((0,0),(1,0),(2,-3),(3,-3),(4,1),(5,2)),  n=5.

Its cup ranks are (1,2,2,3,4,4). Level three {3} misses the four-cup
{0,1,4,5}; level four {4,5} misses the quadrilateral {0,1,2,3}; their
union contains the cap {3,4,5}. Nevertheless B={0,2} is a successful
Parent Option 1 cup, since 2 ends the cap 012. Thus neither the failure
of the two rank choices nor their union refutes the structured lemma.

All 22 old real a4 controls (counting reflections separately) and the
four predesignated 16-point n7 left blocks have Parent Option 1 cups.
All four n7 blocks have no Parent Option 2 cup in the exact enumeration;
the first two also fail both rank-five and rank-six selections. These
are bounded finite computations, not a universal existence proof.

`data/low_split_controls.json` then checks eleven full low-split sets:
small endpoint examples at n5,6,7,8; three larger n7 endpoint examples;
and the four long-cup n7 examples joined to a three-cup. All pass exact
premise, target-coverage, four-cap-avoidance and terminal-certificate checks.
The largest has 25 points and 46 selected cap triples, 36 of them mixed.
The hard long-cup controls each have 19 points and ten selected mixed
cap triples. No universal n5 conclusion is inferred from these checks;
the parent's separate n5 certificates require their own semantic audit.

Finally, `tools/verify_low_classification.py` imports no finder, generator,
prior checker or encoder. It constructs canonical low joins, checks all
caps and polygons with integer determinants and monotone hulls, and
compares every full-set selection against the two-option classification.
The n5/n6/n7 controls compare 128 / 8,192 / 524,288 assignments and find
36 / 60 / 616 terminal-safe selections respectively, exactly matching

    (2^(n-4)-1) * number_of_Option1_cups + number_of_Option2_cups.

The 19-point n7 control has 543 four-caps, 253 unprotected cap triples and
481 hexagons. Its 88 Option 1 cups and zero Option 2 cups account for all
616 terminal selections. These arithmetic replays verify the geometric
classification on fixed real inputs, not the parent's new CNF code.
Output: `data/low_classification_replay.json`, PASS.
