# Exact consequence chain

**PROVED: universal T6 by the written finite/capacity chain; further
implications and their evidence dependencies are stated separately.**
All point sets are finite real sets in general position, with distinct
x coordinates and their induced order. Fix n>=5. No abstract SAT model
is treated as a real point set without a realization check.

## 1. Definitions and the established reduction

A terminal-safe weak Delta of U is a four-cap-free A meeting every whole
convex (n-1)-gon, such that every selected cap a<b<c has an ambient
four-cap u<v<b<c. A low split U=L disjoint-union R has both blocks
nonempty and x-separated, every LLR triple a cap and every LRR triple
a cup. U is admissible if it has no five-cap and no convex n-gon.

For L with no four-cap and no n-gon, T_n(L) is the disjunction:

1. A cup B meets every internal (n-1)-gon, and each selected vertex after
   its first ends an ambient three-cap in L.
2. L partitions into cups B,D with |D|<=n-2.

The frozen written classification, independently reviewed by the low-split
audit, proves that T_n(L) is equivalent to terminal selection for L joined
low to an (n-4)-cup. It also transfers T_n(L) to every right block with
maximum cup d<=n-4. All references to this reduction use actual geometry;
the CNF projection audit is a separate ingredient for finite results.

## 2. Lifting small full-set coverage to small left sets

Suppose terminal selection is known for every admissible full set with
at most M points. Then T_n(L) holds for every admissible left set with
|L|<=M-(n-4). For a nonempty L, place an (n-4)-cup sufficiently far to the
right and sufficiently low to obtain the low-split signs. The join has
no five-cap; a mixed polygon has at most 3+(n-4)=n-1 points. Internal
exclusions hold, so the full-set theorem applies. Its terminal selector
gives T_n(L) by the exact classification. Empty L is immediate.

This argument constructs a new ambient set and uses an existing theorem
at each permitted full cardinality. It never deletes ambient points from
a selector or infers smaller sizes from one larger-size certificate.

For n=6, M=11 gives all left sizes0 through9. Exact left10 and left11
results then give T6 through11. For n=7, M=13 gives left sizes0 through10;
exact left11 through15 give T7 through15. Each larger left size remains
its own obligation.

## 3. Capacity completes the left-size range

The existing Baek theorem, in the local vendor formulation, states

    |S| >= binomial(t+2,2)+2  =>  a four-cap or a (t+3)-gon.

At t=3 the threshold is12, giving capacity11 for no-four-cap/no-six-gon
sets. At t=4 the threshold is17, giving capacity16 for no-four-cap/
no-seven-gon sets. These are specializations of an existing theorem,
not numerical improvements. The list-configuration theorem must be
connected to an actual convex polygon; the Capacity drafts supply that
geometric bridge. The subsequent successful parent run checks both
capacity files and reports only the three standard axioms for all five
reported declarations, including the generic real-polygon bridge.

Thus:

* T6 through left11 plus checked capacity11 proves T6 for every admissible L.
* T7 through left15 plus checked capacity16 reduces universal T7 to exact
  left16. Its parent certificate is now accepted and the instance audit
  passes; the fresh independent proof-closure receipt remains pending.

The mathematical deductions are complete. The current evidence status of
each premise is listed separately in `DEPENDENCIES.md`. The complete T6
chain combines written geometry and audited finite certificates with
Lean-checked capacity; the whole chain is not a single Lean theorem.

## 4. Precisely which low joins are settled by universal T_n

Assume T_n(L) for every no-four-cap/no-n-gon L. In an admissible low split,
put d=maxcup(R). Standard split facts give

    d<=n-2,  maxcap(L)<=3,
    mixed polygons = an L cap joined to an R cup.

If d<=n-4, apply T_n(L) and its transfer to R. If d=n-3, no n-gon forces
L to be a cup: an L three-cap plus a maximum R cup would be an n-gon.
L has at most n-1 points. Take any l in L and the beta_R=(n-3) level.
This is terminal-safe. Internal R targets have a lower (n-3)-cup and
their right endpoints in that level; a mixed target uses an L pair and
a maximum R cup; any internal L target is all of L and contains l.

If d=n-2, L must be a singleton: an L pair plus a maximum R cup would
be an n-gon. A terminal selector of R extends by adjoining the singleton,
since every new selected triple is a cup and every new target contains
that singleton. **Universal T_n does not supply the required selector
of R in this branch.**

Consequently universal T_n implies:

* Every admissible low join with |L|>=2 has a terminal-safe weak Delta,
  without a bound on the total size or on |R|.
* A singleton-left low join is also settled if d<=n-3. The only conditional
  branch is |L|=1 and d=n-2, with its separate right-block premise.
* A cardinality-minimal terminal counterexample has no low cut. The two
  noncritical branches are directly positive; in the critical branch R
  is a proper admissible subset, so minimality supplies its selector.

The last conclusion is about a size-minimal counterexample, not about
every possible counterexample and not about all low joins.

## 5. Fixed-size cuts and weaker protection rules

For an m-point terminal-counterexample search, universal T_n justifies
excluding every low cut with at least two points on its left. To exclude
the singleton-left cut too, terminal selection at exactly size m-1 is
sufficient. The critical right block has precisely that size.

The same minimal-counterexample conclusion holds for each weaker rule
that accepts terminal certificates and survives adjoining a cup singleton:
the one-step cup rule, its transitive closure, the orientation-forced
rule, and exact uniform-envelope protection. The noncritical construction
is terminal-safe. In the critical branch, use minimality for that same
weaker rule, and extend its selector across the singleton. A terminal
smaller-size theorem suffices for all these weaker rules; an ordinary
weak-Delta theorem alone does not automatically supply their protection.

No new cut clauses or encoders are generated by this record.

## 6. n6 and n7 conclusions with their exact qualifications

Already, T6 through left11 proves terminal-safe selection for every
admissible n6 low join with 2<=|L|<=11, with arbitrary right-block size.
Checked capacity11 now bounds every left block by11, so this covers every
non-singleton-left low join and gives the general minimal-counterexample
exclusion without a remaining capacity premise.

The minimum-size n6 conclusion needs no capacity check: any12-point set
has |L|<=11 at every cut. Its noncritical low cuts are covered by the
bounded theorem, and a critical singleton-left cut has an11-point right
block, covered by the independently closed full terminal theorem. Thus
every12-point terminal counterexample already has no low cut. The audited
global terminal minimum is12, so this applies to every minimum example,
and agrees with the separate exact cut diagnostic of the known example.

For n7, bounded T7 through left15 already proves the analogous positive
statement whenever 2<=|L|<=15, with arbitrary right-block size. In
particular every non-singleton-left low cut of a full set of size at most16
is positive. Every14-point terminal counterexample has no low cut at all:
the critical singleton-left branch uses the established full13 theorem.
This is a conditional statement about a counterexample, not full14
existence. At full15 or16 the singleton-left branch still needs its
own full14 or15 premise.

The unrestricted n7 left theorem and its all-size minimal-counterexample
corollary await only the final independent left16 proof closure for the
review grade used here. Capacity16 is checked, the parent left16 proof
is accepted, and the full instance audit passes. The interrupted first
independent wrapper is not called a completed post-hash replay.

The separate [all-cap theorem](all_cap.md) gives additional unconditional
cut coverage: all n6 all-cap joins are positive, and bounded T7 through15
already settles every n7 all-cap join of full size at most16. The critical
singleton-left low-cut caveat does not apply to an all-cap singleton-left
cut; that case is directly positive by its high-split signs.

None of these statements refutes weak D(5,6), proves unrestricted terminal
selection, proves general uniform-envelope existence, or changes an ES
bound. The known terminal obstructions are compatible with these cut
reductions because a counterexample may be indecomposable or may arise
from the critical singleton extension of another counterexample.
