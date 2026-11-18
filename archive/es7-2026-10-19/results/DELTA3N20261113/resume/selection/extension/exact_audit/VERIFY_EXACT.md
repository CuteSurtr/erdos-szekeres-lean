# Independent exact-containment audit — confirmed

**PROVED:** the reverse augmentation preserves the orientation projection
of the previously reviewed generic terminal-safe formula. In particular,
every real counterexample has canonical exact flags satisfying all added
clauses. **COMPUTED:** every map entry and added row of the supplied n7/m13
instance matches independent reconstruction, and all original CNF body
bytes are retained unchanged. **No new UNSAT certificate is claimed.**

## Scope and inherited base

Reviewed source: `../augment_exact.py`, SHA-256
`6ba217c01a3341b0f2d501c97688643b0a247ba40b22256324f7fa6762d08a24`.
Reviewed inputs are the pinned `terminal7-a/m13/input.cnf` and `.map`;
reviewed output is `n7m13-exact.cnf`.

The geometric base and its real-counterexample interpretation are inherited
from [the completed generic audit](../audit/VERIFY_EXTENSION.md), especially
Exact auxiliary definitions, One-way containment projection and Whole-formula
projection. This task does not redo that full base audit. It reconstructs
the complete variable map and the containment/failure interface needed by
the new argument, and verifies preservation of all other base bytes.
Neither the parent augmenter nor any previous checker is imported or run.

The augmenter assumes a compatible, already reviewed CNF and map. It is
not itself a standalone validator of the base. This independent audit
establishes the required compatibility for the pinned n7/m13 instance.

## Canonical exact containment

Fix the base orientation variables and the exact geometric auxiliary flags.
For a point set V, call a triple a<b<c bad when it is a cap and no ambient
four-cap u<v<b<c exists. Let B be that family of triples and H the family
of convex (n-1)-subsets. These leaves are already exact in the reviewed base.
Define

    D(S) = true iff some b in B is contained in S,
    T(S) = true iff some h in H is contained in S.

At witness cardinality, D aliases the exact bad-triple flag and T aliases
the exact convexity flag. Below witness cardinality the flag is constant
false. The map creates no additional independent leaf variables.

For a family of witnesses of cardinality k, let C(S) be the k+1 children
obtained by deleting each of the k+1 least vertices of S. Then

    Contains(S) iff OR { Contains(U) : U in C(S) }.

The right-to-left implication needs only U subset S. For the converse,
any k-element witness misses at least one of the k+1 distinct deleted
vertices, so it survives in the corresponding child. This argument is
pure set containment and introduces no geometric, symmetry, cup-rank,
coordinate, or minimal-counterexample premise.

The reviewed base contains the forward clause

    -parent child_1 ... child_(k+1) 0

for each internal containment parent. The augmentation adds precisely

    -child_i parent 0

for each specified child. Thus the augmented flags satisfy full OR
equivalence. Child cardinality strictly decreases, so induction from the
exact leaves gives unique exact containment values. Here k=3 for D and
k=n-1=6 for T, hence four and seven children respectively.

## Preservation of the whole projection

Take any model of the original formula. Descent through its one-way
clauses proves that any true original internal containment flag has a
genuine true leaf witness below it. Therefore replacing all internal
flags by canonical exact values can only change false flags to true.

Every original containment clause is satisfied by the canonical values
by the cover argument above. Every selection-failure clause contains only
positive D(A) and/or T(V minus A), so an originally true failure clause
remains true. All other old clauses refer only to unchanged variables.
The added reverse clauses hold because a witness contained in a child
is contained in its parent. Consequently the canonical replacement is a
model of the augmented formula with exactly the same orientations and
geometric leaves. Conversely an augmented model is an original model
because every original clause is retained.

Thus the two formulas have the same projection onto orientations and
exact geometric flags. They need not have the same assignments to the
internal containment flags: the old formula allows some witnessed flags
to remain false. The augmentation deliberately removes those auxiliary
assignments; the canonical replacement preserves satisfiability for each
fixed original geometry.

In particular, any real five-cap-free, seven-gon-free terminal-safe
nonexistence example satisfies the reviewed base under its canonical
assignment, and that same exact assignment satisfies the augmentation.
UNSAT of the augmented formula would therefore imply the corresponding
real existence result, once its LRAT has been accepted independently.
No such new UNSAT conclusion is asserted by this formula audit alone.

## Complete n7/m13 map and clause check

The independent checker builds all IDs in the reviewed allocation order
using combinations and integer-mask order, without trusting map counts.
All **15,822** map entries, including their IDs, kinds and masks, agree.
The reconstructed map is also byte-for-byte identical.

| Kind | Count | Cardinalities |
|---|---:|---|
| orientation | 286 | 3 |
| convex | 3,718 | 4,5,6 |
| terminal_fourcap | 715 | 4 |
| terminal_bad_triple | 286 | 3 |
| bad_contains | 6,721 | 4 through 8 |
| target_contains | 4,096 | 7 through 13 |

There are four reverse rows per bad parent and seven per target parent:
**26,884 + 28,672 = 55,556**, with no duplicates and no new variables.
Every child ID is smaller than its parent, denotes a proper single-vertex
deletion, and aliases the correct exact leaf at the boundary.

The checker reconstructs and matches all **10,817** old forward containment
rows and all **7,099** retained positive selection-failure rows. It verifies
that internal containment IDs have no uses outside those interfaces, and
that there are no fixed-sign clauses. This explicitly validates the
monotonicity premise in the whole-projection argument without rebuilding
the geometric base clauses.

The original header declares 59,815 clauses and the actual parsed count
agrees. Its 1,167,995-byte body, including comments, whitespace, ordering
and all clause literals, is unchanged. Only the DIMACS header is replaced,
followed by the new phase comment and the 55,556 reverse clauses. The
augmented header and actual count both give **115,371** clauses.
The entire independently rebuilt augmented CNF has the same SHA-256:

`3ec4b75d9076b6f257fed83f3cbb17b8372a43f53f1c0fc8d30730e4c5d35b87`.

Every possible witness in every internal parent was checked against its
deletion cover: **182,182 bad-family** and **217,932 target-family** cases.
Omitting one child from the required width is refuted by the explicit
witness consisting of exactly the remaining deleted vertices. Those
negative controls are retained in `data/controls.json`.

## Exact coordinate and Boolean controls

Two real 13-point fixtures use the first and last 13 points of the frozen
23-point integer input. A new independent integer implementation computes
orientation, caps, bad triples, triangle-based convexity and canonical
containment flags. No previous geometry checker is imported.

| Fixture | Four-caps | Bad triples | Hexagons | False failure rows |
|---|---:|---:|---:|---:|
| first13 | 1 | 123 | 69 | 87 |
| last13 | 56 | 60 | 139 | 345 |

Both have integer general position, no five-cap and no seven-gon. All
**55,556 new rows** and all non-failure base rows hold for each canonical
assignment. These fixtures have valid selections, so their full
nonexistence formulas appropriately fail at the displayed positive
selection-failure rows. They are positive geometric controls for the
augmentation, not asserted SAT counterexamples.

Setting all internal flags false preserves the local old containment
clauses but violates 1,713 and 1,573 reverse clauses respectively. This
checks the distinction between unchanged orientation projection and
unchanged auxiliary assignments. The control claims only local containment
satisfaction, not satisfaction of each fixture's full failure formula.

The abstract bad-containment lattice on five points was checked for all
1,024 leaf patterns and all 64 internal assignments: **65,536 cases**.
There are 54,450 old local models and exactly 1,024 exact models, one per
leaf pattern. Every old true flag remains true after canonical repair.
The target lattice uses the actual n7 witness size six on eight vertices:
89 deterministic leaf patterns, all 512 internal assignments each,
**45,568 cases**, with 30,534 old local models and exactly 89 exact models.
The same repair property holds. These finite checks support the general
inductive argument, rather than replacing it.

Missing and duplicate rows, wrong polarity, reversed implication, wrong
parent and a corrupted map mask are rejected. Precise mutations and
messages are retained. No unexpected failure, timeout, memory stop or
UNKNOWN control occurred.

## Operational outcome and pending certificate

Structure check: **0.42 seconds, 80,664 KiB peak RSS**. Controls:
**0.38 seconds, 80,140 KiB peak RSS**. Each invocation was bounded by
AS300 MiB, CPU19 seconds, wall20 seconds, affinity CPU 5 and nice 10.
They ran sequentially; no compiler or long-running job was needed.
Sources and CNF/map inputs were hashed before/after with stable results.

The parent's `nov13c-vfy-delta6-finite13` job uses this augmented CNF and
writes into `finite13-b/`. At handoff no accepted certificate was available.
No independent cake replay was attempted under the short AS300 allocation.
A retained proof, concrete replay-memory reservation and deadline are
required for the next replay step; acceptance must be the exact
`s VERIFIED UNSAT` line, never exit zero alone. Preserve the proof.

The generic-base dependency, certificate-pending status and separation
from the m15 coordinate audit are intentional boundaries of this task.
The prior fixed-23 subset audit remains frozen and unchanged.
