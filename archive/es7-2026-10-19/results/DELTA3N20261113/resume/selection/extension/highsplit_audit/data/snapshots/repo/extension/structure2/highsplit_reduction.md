# High-split reduction without a cup-length hypothesis

**PROVED (written, parent-derived statement; adversarial proof review by
this track).** Fix n>=5. A high-split cut with at least two points on its
right admits a terminal-safe weak Delta in every real five-cap-free,
n-gon-free set. A high-split singleton on the right preserves existence
from the left set. Consequently a size-minimal counterexample to terminal,
cup, closure, orientation-forced or uniform-envelope selection has no
high-split cut. Every recursively high-split-decomposable set satisfying
the two geometric exclusions admits a terminal-safe weak Delta.

There is **no global cup-length hypothesis**. This strengthens the earlier
`separated_general.md`; that rank-level theorem and its original controls
remain intact. No novelty or finite-size SAT conclusion is claimed here.

## Definitions and split facts

Let U=L disjoint-union R be a finite real set in general position with
distinct x coordinates. Both blocks are nonempty, every L point is to the
left of every R point, every LLR triple is a cup, and every LRR triple is
a cap. Call these sign conditions S. Assume no five-cap and no convex
n-gon. A weak Delta has no four-cap and hits every whole convex (n-1)-gon.
It is terminal-safe if each of its cap triples ends in the last pair of
an ambient four-cap.

Write c=maxcup(L). The split facts proved in `separated_theorem.md` give:

* A cup in L followed by one point of R is a cup. Thus c+1<=n-1,
  because every n-cup is an n-gon, and **1<=c<=n-2**.
* One L point followed by a cap in R is a cap. Thus **maxcap(R)<=3**.
* A mixed convex subset consists exactly of a cup in L and a cap in R.
  Its maximum possible size is c+maxcap(R).
* Every polygon in L has at most c+2 points: its upper cap has at most
  four and its lower cup at most c, with the two extreme endpoints shared.

In particular all chain bounds concern actual real geometry. No
realizability or completeness assertion about a SAT sign relaxation is
implicit in the argument.

## The three cases

### (i) c<=n-4: choose A=R

There is no target wholly in L, since c+2<=n-2. Hence every target meets R.
There is no four-cap in R. For each cap triple a<b<d in R, any l in L
makes l,a,b,d an ambient four-cap: all three mixed triples are LRR caps,
and a,b,d is a cap. Thus R itself is a terminal-safe weak Delta.

### (ii) c=n-3: choose a rank level in L and one R point

A three-cap in R, together with a maximum cup in L, would give an n-gon.
Thus R has no three-cap and is itself a cup. The n-gon exclusion implies
|R|<=n-1. Let beta_L(v) be the longest cup ending at v within L, put

    B={v in L: beta_L(v)=n-3},     A=B union {r},

where **r is any point of R**.

An internal L target has lower cup length at least n-3, because its upper
cap has length at most four. Its right endpoint therefore has beta_L=n-3
and lies in B. A mixed target must use n-3 cup vertices in L and two cap
vertices in R: these are the respective maxima and they sum to n-1.
The last selected L vertex lies in B. An internal R target can exist only
when |R|=n-1, in which case it is all of R and contains the chosen r.

For completeness, the rank-level safety argument is internal to L. If
a<b<d in B form a cap, take a longest cup ending ...p,a. Its penultimate
p exists because n-3>=2. If p,a,b were a cup, appending b to that longest
cup would make beta_L(b)>=n-2, contrary to b in B. Hence p,a,b is a cap;
with a,b,d cap, decreasing consecutive slopes make p,a,b,d a four-cap
in L ending in b,d. If B contained a four-cap a,b,d,e, applying this
argument to a,b,d and appending e would give a five-cap in L. Thus B is
four-cap-free and all its cap triples have terminal certificates in L.

The new selected point r creates no selected cap triple: every triple
with r has two points in L and is an LLR cup. It therefore creates no
four-cap either, and all old terminal certificates remain ambient in U.
This proves that A is terminal-safe.

### (iii) c=n-2: R is a singleton and existence reduces to L

If R had two points, they would be a two-cap; together with a maximum
cup in L they would form an n-gon. Thus R={r}.

If B is a terminal-safe weak Delta of L, let A=B union {r}. Every target
in L meets B, and every other target contains r. All triples containing r
are LLR cups, so there is no new cap triple or four-cap in A. The old
terminal certificates remain in U. Thus A is terminal-safe.

The same implication holds for the one-step cup, two-triangle closure,
orientation-forced and exact uniform-envelope rules: existing supporting
four-caps and their orientation/line certificates remain available, and
there are no new selected cap triples. For the exact envelope rule, the
rightward domain for U is a subset of the old rightward domain for L,
which preserves each old all-X inequality. This direction is sufficient;
no converse for the envelope rule is assumed.

## Induction and minimal counterexamples

Define a recursively high-split-decomposable set to be a singleton, or a
set with such a cut whose two nonempty blocks are recursively high-split-
decomposable. The empty set may also be admitted as a trivial base case.
Induct on its cardinality, fixing n throughout. A singleton has a
terminal-safe weak Delta (for example the empty selection). Cases (i)
and (ii) need no inductive assumption. In case (iii), L is a proper
recursively decomposable subset, and the no-five-cap/no-n-gon assumptions
are inherited by L. Apply induction to L and then add r. This proves the
recursive corollary with no missing cup-length assumption.

More generally, for any of the protection rules just listed, a
cardinality-minimal real counterexample cannot admit a high-split cut.
Cases (i) and (ii) directly give a terminal-safe selection, which passes
each of these weaker protection rules. Case (iii) gives a smaller
counterexample in L by contraposition of the extension implication.

The distinction is essential: an arbitrary set with a high-split cut is
not asserted to be terminal-safe. In the singleton-right case the needed
selection of L is a hypothesis or an inductive conclusion, not a new
unconditional theorem about L.

## Exact form of the SAT strengthening

Number m vertices from 0 through m-1, and let t_abc mean that a<b<c is a
cup. At cut k, L={0,...,k-1}, R={k,...,m-1}. Negating S_k is the one clause

    OR_{a<b<k<=c} (NOT t_abc)  OR  OR_{a<k<=b<c} t_abc.       (C_k)

These cuts have different dependencies:

* **1<=k<=m-2:** |R|>=2 rules out case (iii), so (C_k) is valid for every
  real counterexample to any listed protection rule, unconditionally.
* **k=m-1:** (C_k) is valid for all size-m real counterexamples once the
  same selection property has been established for all admissible real
  sets of exactly size m-1. Only this preceding size is needed here,
  because case (iii) has |L|=m-1.

Thus an audited size-12 result can justify all cut clauses in a size-13
search; an audited size-13 result can then justify them at size 14. This
record does not audit those finite results or their encoders. A proof
for an augmented CNF still needs the usual soundness audit and accepted
cake_lpr certificate before yielding a finite geometric conclusion.
Clauses may exclude non-real abstract sign assignments that were not
known to be impossible in the base relaxation; this is harmless for a
real-geometry implication, but no unconditional propositional equivalence
to the original CNF is claimed.

The encoder's bound |A|<=m-n+2 causes no additional obstruction when
m>=n-1. Any protected weak Delta can be thinned to that bound: if its
complement has fewer than n-2 points, move arbitrary selected vertices
to the complement until it has n-2 points. Such a complement cannot
contain an (n-1)-gon, and taking subsets preserves four-cap avoidance and
each listed protection rule, with the ambient U unchanged. If the
complement already has at least n-2 points the bound already holds.

## n=5 and scope of controls

At n=5, c is 1, 2 or 3. Case (i) is exactly c=1; L is a singleton.
Case (ii) uses the beta_L=2 level, whose longest cups have a penultimate
vertex as required. Case (iii) is c=3 and forces R singleton. None of
these cases assumes that U has no four-cup. Four-cups in R in cases (i)
and (ii), and a four-cup crossing the singleton in case (iii), are allowed.

`data/highsplit_cases.json` records eighteen named controls. Five each
at n=5,6,8 exercise all three branches, internal targets in both blocks,
R cups of length n-1, and the critical case with both empty and nonempty
left selections. Two n=7 controls have 26 points and maximum cup six;
their prescribed selectors have 46 cap triples with exact terminal
certificates. In case (ii) every choice of r in the named R is checked.
All named controls pass. The three small nonvacuous critical controls
check every terminal-safe left selector, not just one chosen example.

`data/highsplit_n5_grid.json` records a completed bounded n=5 grid:
19,608 configurations were considered, with 90 valid splits: five in
case (i), sixty in case (ii), and twenty-five in case (iii). The last
twenty-five have four-cups, so they exercise hypotheses omitted by the
earlier cup-bounded theorem. All 344 eligible left-selection lifts in
these critical cases pass. This is a fixed integer grid, not exhaustion
over real order types.

The eighteenth named control is deliberately **not** an unconditional
positive selection claim. Append a high rightmost singleton to the
certified terminal18 obstruction from `../../terminal/README.md`.
The resulting 19-point set has maxima (cap,cup,gon)=(4,6,6), satisfies S
at its last cut, and has exactly the old ambient four-caps. It still has
no terminal-safe Delta: restricting any supposed terminal-safe selection
to the old eighteen points would hit every old target, retain cap
avoidance, and retain exactly the same available terminal certificates.
This contradicts the already audited terminal18 result. Thus the
preceding-size premise for the last-cut clause is mathematically
essential. No new SAT result or global minimum-size claim is involved.

The parent reviewed the written reduction, including the exact-m-1
dependency and the thinning argument. The proof and its exact controls
are frozen under `HIGHSPLIT_SHA256SUMS`; later optional structural work
belongs in separate files. The old n=7 proof and fixtures remain intact
as an instance with a stronger cup bound.
