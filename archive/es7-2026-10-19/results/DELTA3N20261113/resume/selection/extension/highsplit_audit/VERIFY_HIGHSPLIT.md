# Independent m14 exact and conditional-cut audit — confirmed

**PROVED (written):** exact reverse containment preserves the old orientation
projection. The high-split reduction is sound for real point sets; at size14,
cuts1–12 need no smaller-size selection result and cut13 needs terminal-safe
existence at exactly size13. **COMPUTED:** every map entry and added clause
matches independent streaming reconstruction; exact integer controls pass.
This record supplies no m14 UNSAT certificate or unconditional equivalence
between the cut-strengthened formula and the original formula.

## Reviewed instance and inherited base

The pinned instance has n=7,m=14. The generic geometric encoder is inherited
from [the accepted base audit](../audit/VERIFY_EXTENSION.md); this does not
repeat that full audit. The reviewed producers are `../augment_exact.py`
and `../augment_indecomposable.py`. Neither producer nor any earlier checker
is imported or executed by the independent programs in `tools/`.

The complete map has 32,086 entries: 364 orientations; 6,006 convexity flags
of sizes4–6; 1,001 terminal four-cap flags; 364 terminal bad-triple flags;
14,443 internal bad-triple containment flags of sizes4–9; and 9,908 internal
target-containment flags of sizes7–14. Every ID, kind, mask and map byte was
reconstructed. The old formula has 104,485 clauses, including 24,351 forward
containment clauses and 14,913 positive selection-failure clauses. There are
no fixed-sign rows. Internal containment flags occur only in their own
forward clauses and the positive failure interface.

## Exact augmentation and projection

Let D(S) mean that S contains an exact bad cap triple and T(S) that S contains
an exact convex six-subset. For witnesses of size k, use the k+1 children
formed by deleting each of the k+1 least vertices. Any k-witness omits at
least one of those deleted vertices, so it lies in a child. Conversely a
witness in a child is in its parent. Thus canonical containment is exactly
the OR of these children, a set-theoretic fact without a geometric premise.

The old clauses are `-parent child_1 ... child_(k+1)`. The new clauses are
exactly `-child_i parent`, four per D parent and seven per T parent. All
57,772 D reverses and 69,356 T reverses were rebuilt in order. Every child
has smaller cardinality and an earlier ID; all 6,643 possible relative
witness positions at the relevant cardinalities survive in a child.

For any old model, a true one-way containment flag descends to a true exact
leaf. Replacing internal flags by canonical containment can therefore only
turn false flags true. Positive failure clauses remain satisfied; forward
and reverse clauses hold; other variables and clauses are unchanged. Any
augmented model conversely satisfies the retained old formula. This proves
equality of orientation projections, not that every old auxiliary assignment
already satisfies the added rows. For a real counterexample, the exact
geometric leaves and canonical flags supply this model.

The terminal condition rules out selected four-caps under the inherited
no-five-cap premise: in a selected cap a<b<c<d, protection of a,b,c supplies
u<v<b<c, and u,v,b,c,d would be a five-cap. The size bound |A|<=m-n+2=9
loses no selector: if the blue complement has fewer than n-2 vertices,
thin A until it has n-2. The complement still cannot contain a target;
cap avoidance and terminal certificates survive taking subsets of A with
the ambient set fixed. No ambient-size monotonicity is used.

All 2,241,860 old body bytes are unchanged. Independent reconstruction gives
the exact input SHA-256
`5dc0c1719cce7bda188abad8489534413ecbbcbe5f43e1b714244ec045a129c4`,
with 231,613 clauses.

## Meaning and reconstruction of the cut clauses

At cut k let L={0,...,k-1}, R={k,...,13}. A high split S_k requires every
LLR triple to be a cup and every LRR triple to be a cap. With positive t
meaning cup, the independent row is

    C_k = OR( -t_abc : two vertices in L )
          OR( +t_abc : one vertex in L ).

Pure triples are absent. C_k is **false exactly when S_k holds**, or true
iff a required mixed sign is violated. The independent code counts left
vertices rather than using the producer's endpoint inequalities. Every
mixed triple occurs once, with the specified sign. The 13 lengths are
78,144,198,240,270,288,294,288,270,240,198,144,78, totaling2,730 literals.
There are no new variables.

Both conditional files retain the exact body unchanged and append only
these13 rows and their comment. Both and our reconstruction have SHA-256
`ba43ca6ecbaeb6bc05854271a27f1204e3a690240a5c525bf1b2a9223dbd1819`
and231,626 clauses. Controls checked13 canonical splits, all2,730 single
mixed sign changes, all2,002 pure changes, and all4,144 assignment/cut pairs
at m=4,5. Wrong-sign and omitted-literal counterexamples are retained for
every cut; duplicate literals are rejected by exact row comparison.

## Independent proof of the real-geometric reduction

Assume real x-ordered GP U=L disjoint-union R satisfies S, has no five-cap
and no convex n-gon, n>=5. Set c=maxcup(L). A cup in L followed by any r in
R is a cup, so1<=c<=n-2. Any l in L followed by a cap in R is a cap, so R
has no four-cap. A mixed subset is convex exactly when its L part is a cup
and its R part a cap. This can be checked through four-subsets: three L
plus one R are convex exactly when the L triple is a cup; one L plus three
R exactly when the R triple is a cap; two of each have convex sign pattern
++--. A nonconvex finite GP set has a point inside a triangle of other
points, so convexity of all four-subsets is sufficient. Finally a polygon
wholly in L has at most c+2 vertices: its upper cap has at most four, its
lower cup at most c, and their two endpoints are shared.

* If c<=n-4, choose A=R. No target lies wholly in L since c+2<=n-2.
  R has no four-cap; every cap triple in R is protected by prepending any
  l in L. Thus A hits all targets and is terminal-safe.
* If c=n-3, R cannot have a cap triple: with a longest L cup that would
  form an n-gon. R is a cup of size at most n-1. Let beta(v) be longest
  L cup ending at v, B={v:beta(v)=c}, and choose A=B+{r} for any r in R.
  An internal L target has a lower chain of size at least n-3, so its
  right endpoint lies in B. A mixed target has n-3 L cup vertices and
  two R cap vertices, so its last L vertex lies in B. An internal R
  target must be all of R and contains r. For a cap a<b<d in B, take a
  longest cup ending ...p,a. The penultimate p exists since c>=2. A cup
  p,a,b would extend it beyond rank c at b, hence p,a,b is a cap.
  Decreasing consecutive slopes give four-cap p,a,b,d. A four-cap in B
  would extend this to a forbidden five-cap. Adding r creates only LLR
  cup triples. Thus A is terminal-safe.
* If c=n-2, R is a singleton: two R vertices plus a longest L cup would
  form an n-gon. Given a terminal-safe selector B in L, B+R hits all
  targets; new triples are cups and old ambient certificates remain.
  This branch requires existence in L; it does not establish that premise.

Therefore a real m14 counterexample cannot have a high split at cuts1–12,
where |R|>=2. It cannot have one at cut13 if terminal-safe existence is known
at **exactly size13**. The prior all-smaller-sizes formulation is sufficient
but stronger than needed. The independently [replayed exact m13 proof](../exact_audit/replay13/README.md)
and its encoder audit supply this premise. No general monotonicity in
ambient cardinality is asserted.

The clauses may remove nonreal sign assignments from the relaxation. The
real-counterexample implication is what is proved. An accepted proof for
this conditional CNF plus these dependencies would exclude real m14
counterexamples; the CNF alone does not discharge the lemma or size13 premise.

## Independent real controls and negative premise control

Controls use unbounded Python integers, strict triangle containment for
four-subsets, all-four-subset convexity and endpoint DP for cup ranks.
No floating arithmetic or hull implementation is used. Fifteen coordinate
fixtures at n=5,6,8 and m<=14 use only P,n,cut from the parent data; supplied
ranks/selectors are ignored. Every right choice in branch ii and every
terminal-safe left selector in the small branch-iii cases was checked:
222 selectors/lifts and21,599 mixed-subset checks. Three large parent
fixtures are not counted as replayed.

An independent m14 critical control takes old18 vertices0..12 and appends
(3817,61604281), strictly above every old secant at that x. Its left maxcup
is5; the full set is GP, no-five-cap, no-seven-gon, with58 four-caps,
97 bad cap triples and54 hexagons. The lifted selector is{0,2,3,13}.
Canonical values satisfy all216,700 non-failure rows, including every
reverse. As a positive instance it correctly violates580 counterexample
failure rows. All13 actual cut rows agree with the direct split predicate;
exactly the final cut is high-split and excluded.

For the essential negative control, append (758071,206805657) above every
secant of the old18 obstruction. This real19 set is GP, no-five-cap,
no-seven-gon, high-split at its final cut, and has exactly the old115
four-caps. All402 old targets remain among its632 targets. Any alleged
terminal-safe selector would restrict to one on old18: old targets remain
hit and all available terminal certificates are still old. This contradicts
the previously checked [terminal18 obstruction](../../terminal/README.md)
and the independent [mapped18 enumeration](../subset_audit/VERIFY_SUBSETS.md).
Thus omitting the preceding-size premise is false in general. This uses
the explicitly cited old obstruction, not a fresh color search or proof
replay, and asserts no global minimum.

## Provenance, strict limits and retained failure

Exact producer SHA-256:
`6ba217c01a3341b0f2d501c97688643b0a247ba40b22256324f7fa6762d08a24`.
Current conditional producer SHA-256:
`13cb24b60f086c06fd25f44982b26d3a6729a40a766474ec29fb60c123eda66b`.
The latter matches v2. The earlier receipt names
`2f54ecbb15b7b30ebae0859b0eab97789edc680c9071e7c70599b5cbf85bfe1e`
and says every size below14. Its producer bytes were not independently
recovered, so no source diff is asserted. Both produced files were compared
byte-for-byte and rebuilt; both receipts and current sources are retained.

Every job used one CPU, AS300 MiB, CPU19s, wall20s, affinity5, nice10.
Successful rows:0.54s/31,660KiB peak RSS. Controls:0.13s,0.29s,0.15s,
at most25,152KiB. Hashes were stable before/after. No solver, proof replay,
long unit, git, install, deletion or external action was used.

The first checker attempt rejected padded whitespace in the base DIMACS
header after0.07s, before checking clauses. Its source, logs, hashes and
partial scratch output remain. The corrected version parses header tokens
and still compares every body byte literally; the second attempt passes.
No evidence input was modified to obtain the pass.

At handoff the parent conditional run indecomp14-a was SOLVING. No
conclusive m14 solver outcome or additional cake allocation is claimed.
