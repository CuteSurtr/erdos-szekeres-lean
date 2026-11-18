# Independent general terminal-safe audit — confirmed within this scope

**PROVED:** the general projection argument below. **CERTIFIED:** independent
cake_lpr replays accept n7/m11, n7/m12 and n8/m13. **COMPUTED:** independently
reconstructed clauses/maps, exact coordinate controls, full subset scans,
and the small-cardinality filter/model checks all pass. No Lean proof,
general-size selection theorem, new ES bound or novelty claim is made.

Consequently every real five-cap-free, seven-gon-free old set of **12
points** has a terminal-safe weak Delta. Combined with the previously
proved/certified smaller-size result, the n=7 bound increases from 11 to
**12 old points**. The independent n8/m13 replay reconfirms the existing
13-point bound. These are terminal-safe existence statements with no
cup/complement boundary restriction. Later parent sweeps are outside this
completed audit until separately checked.

## Semantic definitions and ambient hypotheses

Let V be m points, strictly ordered by x, in general position, n>=5.
For an increasing triple abc, t(abc) is true exactly when its determinant
is positive (cup). A cap has all its triple signs negative. Q(S) denotes
that every four-subset of S is convex. For real points this is equivalent
to S being in convex position. The ambient hypotheses are no five-cap
and no convex n-gon. No cup maximum, complement, extremality, symmetry,
or minimal-counterexample hypothesis is needed.

A triple abc is bad exactly when it is a cap and no ambient four-cap
uvbc exists. Here u<v<b<c; u,v range over every pair preceding b, including
pairs using a. A selection A is terminal-safe when it has no four-cap and
each of its cap triples has such an ambient witness. It is a weak Delta
when it also meets every ambient convex (n-1)-subset.

## Why avoiding bad triples excludes four-caps

Suppose A contains the four-cap a<b<c<d. If abc were not bad, an ambient
four-cap u<v<b<c would exist. Appending d gives the five-cap u,v,b,c,d:
its consecutive slopes decrease, since u,v,b,c is a four-cap and b,c,d
is a cap. This contradicts the ambient hypothesis. Thus abc is bad.
The abstract signotope version uses the same negative consecutive triple
signs and the monochromatic-chain consequence of its one-change packets,
rather than slopes. Thus the reduction holds in the stated abstract model
as well as for real points.
Consequently in a five-cap-free ambient set, a selection is terminal-safe
if and only if it contains no bad triple. Without no-five-cap, the
implication need not hold; the hypothesis must not be omitted.

The same reasoning shows that adjoining a rightmost point r while
preserving no-five-cap cannot create a four-cap abc r in a terminal-safe
A+r: its witnessed terminal pair bc would yield a five-cap uvbc r.
Every old convex (n-1)-subset is already hit by A, and every new one using
r is hit by r. This extension consequence needs no no-n-gon condition
on the enlarged set. It does not assert that terminal safety is necessary
for every possible geometric extension.

## Exact auxiliary definitions

Four-cap flags must be fully equivalent to their negative triple signs
(or the negative consecutive signs, using the packet axioms). Each bad
flag must be fully equivalent to the negative sign of its triple AND
the negations of every ambient four-cap flag ending in its last pair.
One-way definitions do not suffice here, because negative uses could
otherwise conceal a witness or invent a bad triple.

Compact Q4 definitions are exact under the one-change packet axioms.
For |S|>=5, all four-subsets are convex exactly when each of the five
children deleting one of the five least vertices is convex: any fixed
four-subset misses one of those five vertices. Full equivalences at
sizes 5,...,n-1 and the negative disjunction of five children at size n
therefore express precisely the Q semantics and no-n-gon premise.
No-five-cap follows from the positive disjunction of its three consecutive
triple signs, since consecutive signs determine a monochromatic chain.

## One-way containment projection

Let D(S) mean contains a bad triple, with size-three leaves aliasing the
exact bad flags. For |S|>=4 use D(S) => OR D(S-v), where v ranges over
the four least vertices of S. A true node descends, decreasing cardinality,
to a genuine bad triple. Conversely any bad triple misses one of the four
chosen vertices. Thus exact containment values satisfy all these rows,
simultaneously for all S. Three children are insufficient: the witness
could be exactly the three chosen vertices.

Let T(S) mean contains a convex (n-1)-subset, with size-(n-1) leaves
aliasing Q. For larger S use T(S) => OR T(S-v) over the n least vertices.
The same descent and cover argument applies because a target has n-1
vertices. n-1 children are insufficient. Below the relevant witness sizes
the flags are constant false, not independent variables. Auxiliary flags
may be false despite witnesses in a one-way model; this causes no false
positive because every asserted flag still has a genuine witness, and
every actual counterexample has its canonical exact assignment.

## Selection range, including small universes

Put k=m-n+2. For k>=0, require D(A) OR T(V\\A) for every A with
0<=|A|<=k. All retained rows are failure statements. If a larger A worked,
choose any k-subset A' of A. Safety descends to A', and |V\\A'|=n-2,
so A' meets every target automatically. Therefore a working selection
exists if and only if one exists in the retained range. This proof shrinks
only; a small terminal-safe selection cannot in general be enlarged to
size three. In particular, sizes 0,1,2 must not be silently omitted.

If k<0, then m<n-2<n-1, so A=empty is safe and there are no targets.
Nonexistence is impossible and the encoder must emit an empty clause
(or an equivalent contradiction) if it supports that domain. The actual
source rejects m<n-1, so this negative-k case is outside its domain.
At k=0,1,2, a retained size-k row is
itself empty: its selection contains no triple and its complement has
n-2 points. This also forces the correct inconsistency for m<=n.

## Whole-formula projection and claim boundary

Take any model of the complete unconditioned formula. Exact flags recover
the stated ambient signotope geometry and bad triples; descent interprets
each true containment flag. Every retained selection fails for a genuine
reason, and the range argument excludes every omitted larger selection.
Conversely any ambient signotope with no terminal-safe weak Delta extends
to a model by exact Q, four-cap, bad-triple and containment assignments.
Thus the orientation projection is exactly terminal-safe nonexistence
within this abstract geometry, subject to the small-universe convention.
Every real counterexample supplies such signs. An UNSAT certificate can
therefore imply real selection existence after implementation review;
SAT alone does not prove real realizability. Fixed-sign certificates apply
only to those signs. The three unconditioned finite certificates audited
below have no fixed signs.

## Implementation and controls

The source domain is **5<=n<=8, n-1<=m<=20**. The inherited `Encoder`
constructor's ordinary weak-Delta range does not leak into this formula:
the source calls only `geometry()`, then uses separate D/T arrays and its
own loop over every mask of size 0 through m-n+2. It does not call the
ordinary compact `containment()` or `run()`. All new children are proper
one-vertex deletions. Numeric mask order allocates every child before its
parent, and leaves alias exact flags. Target nodes run through the full
universe, as required by the empty selection's complement. No old cup,
complement, symmetry or root-specific rows are present.

`check.py` imports only Python's standard library. It reconstructs every
variable ID and clause, including inherited geometry, while streaming the
actual map/CNF. Its geometry uses integer determinants, monotone hulls,
and full subset truth tables computed by upward closure of directly
enumerated witnesses. It never imports a parent or previous checker.
`extra_controls.py` imports only this audit's own `check.py` helpers.

- Every row and map entry matches for all three certified CNFs. Own
  compilation regenerates all three CNFs and maps byte-for-byte; hashes
  are in [regeneration.json](data/regeneration.json).
- All eight one-change four-sign packets pass exhaustive Q4-equivalence
  checks. Witness covers and deliberately too-short covers are checked.
- 272 general-position six-point permutations give 816 (m,n) controls,
  including 516 valid ambient cases. All 378,352 canonical clause tests
  and 48,384 terminal-safety equivalences pass. Invalid ambient cases
  fail only their actual no-five-cap/no-n-gon/failure rows, as intended.
- Twelve supported edge formulas at n=5,6,7,8 and m=n-1,n,n+1 match all
  reconstructed rows. Cases m=n-1,n contain the expected empty clauses.
  Six out-of-domain inputs are rejected with `bad_parameters`.
- Flipping each of 252 convex, 126 four-cap, and 84 bad-triple exact flags
  in a real nine-point control is rejected by its definition clauses.
  Setting 285 genuinely true internal containment flags false still
  satisfies all non-pool rows, confirming that these are deliberately
  one-way witnesses. All 1,024 leaf truth patterns of the bad-containment
  lattice on five points have the correct existential root projection.
- A six-point cap with its last four selected verifies why no-five-cap
  is necessary for bad-triple avoidance to imply four-cap avoidance.
  A three-cap verifies why growing a safe pair cannot be assumed safe.

Six frozen smaller valid real fixtures satisfy every geometry/definition/
containment row and violate precisely the failure rows belonging to
working selections in the retained range:

| Fixture | m | n | All terminal Deltas | False retained failure rows |
|---|---:|---:|---:|---:|
| original boundary n6 old set | 9 | 6 | 77 | 76 |
| refined boundary n6 old set | 9 | 6 | 54 | 53 |
| original boundary n7 old set | 11 | 7 | 499 | 464 |
| refined boundary n7 old set | 11 | 7 | 403 | 390 |
| original boundary n8 old set | 13 | 8 | 593 | 592 |
| refined boundary n8 old set | 13 | 8 | 593 | 592 |

The count differences are larger working selections omitted by the sound
shrinking reduction. They are not control failures. Each full subset scan
independently confirms the exact retained count.

## Real 18-point canonical SAT control

The frozen n7 fixture has minimum absolute determinant 227,322,879,
115 four-caps, 219 bad triples, 402 convex six-subsets, no five-cap and
no seven-gon. All **262,144** subsets were checked; none is terminal-safe
and target-hitting. The exact canonical assignment satisfies all
**1,047,884** clauses of the fixed-sign formula, with **522,956** variables
and 4,545,852 literals, including its 816 sign units. Every formula/map
entry also matches the independent reconstruction. This is an explicit
checked SAT assignment; no SAT search was needed.

The same exact orientation checks find 230 five-cups and **no six-cup**.
The maximum cap, cup and convex-subset sizes are (4,5,6). Thus forbidding
an (n-1)-cup does not restore terminal-safe existence for all sizes.
This is the already known real fixture, not a new minimality claim and
not a refutation of ordinary weak Delta or uniform-envelope selection.
See [the full control](data/real-terminal18.json) and
[cup/cap facts](data/terminal18_facts.json).

## Independent certificate replay

| n | m | Variables | Clauses | Replay seconds | Receipt |
|---|---:|---:|---:|---:|---|
| 7 | 11 | 3,730 | 18,944 | 0.232 | [replay](data/replay-n7m11.json) |
| 7 | 12 | 7,735 | 33,972 | 3.144 | [replay](data/replay-n7m12.json) |
| 8 | 13 | 14,535 | 65,392 | 2.891 | [replay](data/replay-n8m13.json) |

Each fresh log contains the **exact line** `s VERIFIED UNSAT`. Each CNF,
LRAT and cake_lpr binary was hashed before and after replay with identical
hashes. The parent's uncompressed and compressed proofs remain retained;
the largest replayed LRAT is 105,055,597 bytes. Exit zero alone was never
used as acceptance. The three CNF/LRAT pairs are:

| Case | CNF SHA-256 | LRAT SHA-256 |
|---|---|---|
| n7/m11 | `dc28e1f234449b95ac1ce181fc922503a61e35239ae56a9cf6fe42b18b8a777e` | `6ed485d0dfa3cceeca144b3a3bccd9470ce8c772f38c44a4e51d55be04e49a37` |
| n7/m12 | `cebe762c17735b3f811355987acc8912b57b880f341f3ff286097dd98e97d850` | `4f770646917f895d5a29934c380b191ee1aceb5bddf0d0f56ee67b23571a15b3` |
| n8/m13 | `9dc7bd3c109e066b5ef00dc9ff1c47f1446224741af38dd7d1f7376c7b7ca1f7` | `c6da911a5bd6554afd03fdde74e6de941b1352c82924d10336cb81e8910a5d20` |

A certificate at one m is not a monotonicity proof for smaller m: deleting
points can destroy terminal-pair witnesses. Coverage through 12 at n=7
uses the prior independently checked coverage through 11 plus m12 here.
The same A can be chosen before any rightmost insertion preserving
no-five-cap; A+r is a weak Delta by the argument above, even when the
extension has a seven-gon. The old set's no-seven-gon hypothesis remains.

## Small-cardinality filter

`small_delta.py` enumerates generic failure rows in increasing integer-mask
order, which is exactly the source's order. Its output retains a literal
subsequence, with **every other clause and every variable unchanged**.
The audit reconstructs the six outputs directly from the semantic clause
families, verifies the masks and point counts, and checks the DIMACS
headers. The retained row counts are 67,232,299,794,378,1093 for
(n,m,k)=(7,11,2),(7,11,3),(7,12,3),(7,12,4),(8,13,3),(8,13,4).

These values have k<=m-n+2. UNSAT of such a subformula would imply a
terminal-safe Delta of size at most k; SAT excludes only that range.
The checked n7/m11/k2 model assigns all 3,730 variables and satisfies all
17,525 clauses. Independent recovery from its orientation signs gives
46,96,62,9 terminal-safe Deltas of sizes 3,4,5,6 respectively, with
minimum size **three**. It is an abstract model; real realizability has
not been checked. The remaining five 15-second cases are **UNKNOWN**,
and imply no positive or negative cardinality theorem. See
[filter checks](data/filters.json) and [model check](data/small_sat.json).

## Resources, provenance and limits

All control jobs were sequential, one CPU, AS400 MiB, external 20 seconds;
compilation used AS500 MiB. The 18-point stream/assignment control used
29,092 KiB peak RSS. Replays used the parent's explicit one-CPU AS1100 MiB,
heap800/stack32 allocation, each externally limited to 20 seconds. The
largest observed cake RSS was 825,464 KiB. No long unit, solver search,
proof deletion, installation, git mutation, external action, old-record
edit or shared-manifest change was performed by this audit.

The unused renamed compact legacy main produces the retained benign
return-type compiler warning. An initial directory probe found the new
extension paths not yet created. There was no failed mathematical control,
AS failure, timeout, OOM, rejected replay or guard stop in this subtrack.
Expected invalid-domain and adversarial-control rejections are recorded
as controls. Parent UNKNOWN outcomes are preserved without promotion.

Frozen reviewed source files, fixture provenance, external hashes and
scoped SHA256SUMS accompany the report. No claim about later parent runs,
other extension tracks' mathematics, or any general all-size theorem is
included. No work remains running or queued in this audit allocation.
