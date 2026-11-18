# Independent review of the extension embedding family

**Written all-gap embedding equivalence confirmed; controls COMPUTED.**
No gap was found in the new selector/orientation clause family. The
independently rebuilt complete cup n7/add1 formula matches the parent's
certificate input exactly. Its cake acceptance log and retained proof
hashes were checked; cake was **not independently replayed** here.

Reviewed source: `../lift/extension_cnf.cpp`, SHA-256
`eac5c72391a0090468e28022f424f4aa43c6efa8aea1767207d3e0985d5dec5a`.
Included universal encoder:
`b953e14fc7d0840712bbf63f502e00c7342cbd1cdb9ef3ed548759e8ae8aa12c`.
The review concerns this embedding family and the requested weak-n8 lemma.
The optional unit simplifier, other lift lemmas, and the new five-point
transversal probe are outside this audit.

## Complete coverage of increasing copies

Let the old labels be 0,...,r-1 and the total size be m=r+k. In any
increasing embedding with positions p_i, define d_i=p_i-i. There are i
earlier old points and only k extra points, so 0<=d_i<=k. Strictly
increasing positions imply d_i<=d_(i+1). Conversely, any such nondecreasing
sequence gives positions p_i=i+d_i in [0,m), with p_(i+1)>p_i. It determines
one increasing r-subset, and every increasing r-subset arises this way.
This includes initial, terminal, repeated-gap, and separated insertions:
there is no requirement d_0=0 or d_(r-1)=k.

The selector row for old point i has one positive clause and all pairwise
negative clauses, hence exactly one true E(i,d). For adjacent rows, the
clauses forbid precisely a decrease in the chosen offset. Transitivity
then ensures monotonicity for any triple of old labels, not only adjacent
labels. The selected positions are therefore an injective increasing copy.

For old i<j<l, the loops include every a<=b<=c in [0,k]. On the selected
offsets, exactly the matching three-selector implication is active and
forces t(i+a,j+b,l+c) to equal the old sign. These three positions are
strictly increasing. Every other implication for that old triple has a
false selector in its antecedent. Thus the clauses force all and only the
old orientation requirements at the selected copy.

Conversely, for any extension containing an increasing old copy, set its
corresponding E(i,p_i-i) true and all other selectors false. All row/order
clauses hold, and the active orientation clauses hold by the copy's signs.
This is an explicit canonical assignment for **every** insertion pattern,
not merely a proof that some preferred gap works.

Selectors are allocated after the inherited universal variables and cannot
collide with them. The full source emits the existing geometric/Delta
formula unchanged, then appends the embedding clauses. Its default options
are lattice, no symmetry and no cube. The reviewed delivered formula has
no fixed positions or full-sign pins. Optional fixed positions or pins
would narrow the claim and must be retained in its statement. Likewise,
embedding-only and base-only outputs omit the full counterexample demand.

Combining the inherited canonical assignment with these selectors includes
every genuine real extension with the fixed old coordinates. It also
includes other realizations with the same old signs. A SAT assignment alone
need not be realizable; an all-gap UNSAT conclusion concerns this fixed old
order type and the stated total size/mode, not arbitrary old configurations.

## Independent controls and exact delivered formula

[`audit_embedding.py`](audit_embedding.py) compiled both sources independently
into the assigned audit scratch directory. It then inspected the actual
emitted clauses, without importing the author's checker.

- For an actual mixed-sign four-point set and k=0,...,5, all **252** increasing
  insertion patterns were tested. Each received explicit general-position
  integer coordinates preserving the old points and its canonical selector
  assignment; all embedding clauses held.
- All **2,275** four-row offset vectors for those k values were enumerated.
  The emitted row/order clauses accept exactly the nondecreasing vectors.
- For the actual 15-point integer fixture and k=1, all **16** insertion
  gaps were realized with an extra integer point and checked clause by clause.
- In every tested embedding, flipping each mapped old triple in turn makes
  the formula fail. This is **8,288** rejected single-triple flips, confirming
  that no old orientation requirement was omitted.

These coordinate controls test the embedding layer. The arbitrary added
control points are not asserted to satisfy all ambient Delta premises.
Completeness of the full formula follows from the separate inherited
canonical-assignment argument, not from pretending such controls are
counterexamples.

The standalone old cup n7/m16 formula has **452,135** clauses. Every one
matches the corresponding prefix of the rebuilt extension formula. The
remaining **1,864** clauses match the independently tested embedding-only
formula after the correct selector-ID shift: 30 one-hot clauses, 14 order
clauses and 1,820 old-orientation implications.

The full result has **142,767 variables and 453,999 clauses**, with SHA-256
`9138cb5807ca6d208e2cb3f1519b0060026d495e295e9388c1f45bc35284d233`.
It is byte-identical to
`/home/jay/research/data/delta3-codex-20261113/resume/lift/cup-n7-add1-all-gaps/case.cnf`.
This binds the all-gap source review to the actual certificate input.

The parent's [certificate record](results/lift-parent-result.json) and
[cake log](results/lift-parent-cake.log) were retained in audit scope. The
log contains the exact line `s VERIFIED UNSAT`; its hash matches the record.
The retained LRAT hashes to
`41978f2d53df04787a34aba49a119675079d95b63bb5f5350cef7541289467f1`,
and its zstd file hashes to
`032c50005028d0da32cb69148451fbe532296dd3e0b22b8518dd0f2abdb59371`.
Both current files matched. This audit did not launch a solver or cake,
and does not describe that log/hash check as an independent proof replay.

The certified finite statement, using that parent evidence and the reviewed
model, is: no (5,7)-valid 16-point abstract cup-side counterexample contains
an increasing copy of the fixed old 15-point signotope, across all 16
insertion gaps. It consequently excludes real one-point cup-side lifts of
that source. It does not exclude two or more insertions or settle weak Delta.

## Requested weak-n8 lemma

**The written lemma is valid.** Assume S has no convex hexagon, A is disjoint
from S with |A|<=5, and Q=S union A has no five-cap. No octagon-free premise
is required for this conclusion.

Every convex heptagon H in Q contains at least two points of A: otherwise
at least six vertices of H lie in S, and convexity is hereditary, producing
a forbidden hexagon in S. It therefore suffices to choose a four-cap-free
R contained in A that omits at most one point of A.

For |A|<=3 take R=A. For |A|=4 choose any three points. For |A|=5 there is
a four-subset which is not a four-cap. If all five four-subsets were caps,
every triple of A would be contained in a cap and have negative orientation,
making A a five-cap, contrary to the premise. Choose such a noncap four-set
as R. In each case R has no four-cap, and every heptagon's at least two
added vertices cannot both lie in the at-most-one omitted point. Thus R
meets every heptagon and is a working weak Delta.

This proof also works with the abstract hereditary four-subset convexity
definition. The source15 fixture's no-hexagon premise was independently
checked in the pool geometry audit. The lemma rules out weak-n8 failure
for its extensions by up to five points satisfying no-five-cap; it does
not establish a cup-side statement or apply to arbitrary sources containing
hexagons.

## Files, resources and readiness

[embedding_audit.json](results/embedding_audit.json) records all control
counts and hashes. The entire independent compile/control/regeneration/hash
invocation took **5.023 seconds**, under AS400 MiB, one CPU, an 18-second
CPU limit and an external 20-second SIGKILL deadline. No long job or unit
was started, and no parent file or proof was modified. Scratch files remain
under `.../resume/audit/embedding/`.

Reproduce using the research venv Python with `-B audit_embedding.py`, under
`timeout -s KILL 20s`. Required source/model review is complete. The parent
certificate's independent cake replay remains explicitly unperformed.
