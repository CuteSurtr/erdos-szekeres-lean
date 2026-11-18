# Independent cup/forced protection audit — confirmed

**PROVED:** the two protection predicates imply rightward line protection,
and the formulas have the claimed counterexample projection, conditional
on the already reviewed compact geometric base. **COMPUTED:** streamed
reconstruction matches every new clause and every map entry in the supplied
cup n7/m15 and forced n7/m13 instances; native regeneration and exact real
controls pass. **No finite-size theorem or new certificate is claimed.**

## Scope and source identity

Reviewed sources, retained under `data/source/selection/extension/`:

- `cup_terminal_general.cpp`:
  `c598be1509f99b7b1f8474b777483d18dac22f0ee26feb9bbf8e8b0184b445ef`.
- `forced_terminal_general.cpp`:
  `50b4f5437275bae7aec227cf5468a7ba3d38be461b291b9f605d2b544f29b015`.

The compact source has SHA-256
`1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553`,
identical to the snapshot in the [accepted generic audit](../audit/VERIFY_EXTENSION.md).
Its orientation, convexity, no-five-cap and no-n-gon arguments are inherited,
not re-audited in full. The new CNFs' entire geometry prefixes match the
corresponding existing generic CNFs byte-for-byte. The independent checker
reconstructs the geometric variable map and every subsequent new family.

[Parent projection notes](../PROTECTION_SOUNDNESS.md) agree with the
independent argument below. The [317-geometry predicate audit](../envelope/cup_dominance/comparison/prototype_check/README.md)
is additional inherited evidence for the forced predicate: its inspected
source hash equals the forced source reviewed here. Its 9,347,628 comparisons
are not represented as a rerun by this subtrack, and that predicate audit
alone was not a review of the generic containment/projection.

## Exact End4, support and Covered definitions

Positive sorted triple orientation denotes a cup. A four-cap flag is the
AND of all four negative triple signs; the cup variant also defines a
four-cup flag as the AND of all four positive signs. Each is a full Boolean
equivalence, including the reverse clause.

End4(b,c) is the OR of all four-cap flags on u<v<b<c. Its clauses are

    -End4 cap_1 ... cap_j 0
    -cap_i End4 0                         for every i.

For an empty family, the first row is the unit `-End4`; there is no free
truth value. In particular, End4 is false when fewer than two vertices
precede b. The source skips candidate supports with u<2 or v<3 only because
their End4 flag is identically false. This adds no hypothesis.

For the query pair (b,c), the identical support pair contributes End4(b,c)
directly. Every other support flag is an exact conjunction of End4(u,v)
and its stated orientation condition. Covered(b,c) is the exact OR of the
identical-pair term and all eligible support flags. Finally

    Bad(a,b,c) iff Cap(a,b,c) AND NOT Covered(b,c).

All directions are needed for the clean projection because Covered occurs
negatively. The independent rebuild checks every conjunction clause, every
reverse OR row, all empty End4 cases and the precise bad-triple definition.

Cup support cache reuse is sound: the key is literally the ordered pair
of Boolean inputs (End4 ID, cup-condition ID). Thus a reused flag denotes
exactly the same conjunction. The map uses the correct union mask and
support endpoint name at first allocation. The supplied cup instance has
3,380 distinct support flags and 442 cache reuses, all independently matched.
The forced source creates a separate support for each named comparison.
Shared-endpoint cases may repeat a condition literal; the repeated clauses
are harmless and were retained verbatim in the reconstruction.

## Independent geometric proof of both predicates

Let q=(b,c), p=(u,v), and d(X)=line_uv(X)-line_bc(X). Denominators are
positive because each pair is x-ordered. When the pairs coincide, d=0.
Otherwise the forced source requires v>=c and the applicable tests

    v>c: chi(b,c,v)>0,
    u>b: chi(b,u,v)>0,
    u<b: chi(u,b,c)<0.

At the rightmost endpoint x_v, the first test gives d(x_v)>0, or equality
when v=c. At the earlier left endpoint x_min(b,u), the other test gives
a strictly negative value, or equality when u=b. These claims follow by
substituting the point coordinates into the two secant lines. The direct
numeric controls use positive common denominators, independently of the
source's orientation expressions.

The two endpoint abscissae are distinct. At least one inequality is strict
for nonidentical pairs, so d has strictly positive slope and d(X)>0 for
X>x_v. An End4 support therefore dominates the query on the entire ray
X>max_x(U). No metric optimization or stronger geometric hypothesis enters.

The cup rule requires u>=b, v>=c and that the distinct endpoint union be
a cup. Its positive triple signs imply precisely the endpoint inequalities
just used (with shared-endpoint equalities). Thus the same conclusion
holds. A three-point union uses its existing orientation flag; a four-point
union uses the exact four-cup flag. This is the direct cup rule, not an
unrestricted recursive cup-path closure.

For comparison with the broader endpoint-sign predicate, a candidate
ambient four-cap support with v<c cannot satisfy that predicate under
no-five-cap: its value at the last endpoint x_c would be strictly above
y_c. Appending c to that four-cap would form a five-cap. Therefore the
source's v>=c restriction loses no endpoint-forced support in its stated
ambient domain. The no-five-cap assumption is used here; it is not a
claim about arbitrary point sets.

Neither predicate is necessary for uniform envelope domination. A line
can dominate only after an earlier crossing, or multiple ambient lines
can provide joint domination. The required two-support control below
explicitly preserves this distinction.

## Why the old four-cap obstruction is indispensable

Let D(S) mean that S contains a Bad triple **or an old four-cap**. The old
terminal-rank proof that absence of bad triples excludes four-caps cannot
be reused after broadening protection to other terminal lines.

The exact integer fixture is

    (0,0),(1,-1),(2,-3),(3,-6),
    (10,500),(11,600),(12,699),(13,797).

Both four-point blocks are caps; all 48 mixed triples are cups. The only
four-caps are masks 15 and 240. There is no five-cap and no convex five-set.
Every cap triple in A={0,1,2,3} is protected under both predicates by the
actual ambient four-cap {4,5,6,7}, using its terminal pair (6,7), yet A
itself is a four-cap. At n=7 the four-point complement cannot contain a
six-target. At n=5, A={0,1,2,3,4} similarly hits every four-target because
its complement has size three, while all its cap triples are protected.

The n7 size-four selection exceeds the retained k=3 range for this m=8
instance; it is a semantic warning, not a purported n7 A4 variable. The
n5 version has k=5 and directly exercises the emitted A4 and A5 rows.
Both native encoders were checked on this latter case.

At |S|=4 the source uses the one-way row

    -D(S) Bad(S-v1) Bad(S-v2) Bad(S-v3) Bad(S-v4) Cap4(S) 0.

The complete four-child list finds every bad triple, while Cap4(S) is the
indispensable four-point obstruction. For |S|>=5, it uses five deletion
children. A witness of size three or four misses at least one of five
chosen vertices, so canonical mixed containment satisfies the recurrence.
Four children would be insufficient for a four-point witness consisting
of exactly the four deleted vertices.

The control checks the actual emitted rows under canonical values. Deleting
the Cap4 term from the A4 row makes it false. For S={0,1,2,3,4}, deleting
the fifth child from the A5 row also makes it false: the first four children
remove a cap vertex, and only the fifth child retains the old four-cap.
Precise native row IDs and both failed mutations are retained in
[cup-blocks5.json](data/cup-blocks5.json) and
[forced-blocks5.json](data/forced-blocks5.json).

## Mixed one-way containment and whole projection

At size three, D aliases the exact Bad flag; below three it is constant
false. At size four use the row above. At larger sizes a true D node
descends to a true child. Cardinality decreases, ending at an exact Bad
triple or an exact Cap4 flag. Therefore every asserted D has a genuine
obstruction. Conversely canonical D(S), defined by actual mixed witness
containment, satisfies all rows by the four-/five-child cover argument.
These internal flags are deliberately one-way, not equivalences.

Target containment T has the already reviewed exact convex (n-1)-leaves
and one-way n-child recurrence. Descent and the same cover argument show
that asserted T has a genuine target and canonical exact T satisfies the
recurrence. Flags below target cardinality are constant false.

Put k=m-n+2. Every selection of size 0 through k has the positive failure
row D(A) OR T(U minus A). For any model, exact leaves and descent interpret
these rows as genuine failure of every retained selection. If a larger
protected weak Delta existed, any k-subset would remain four-cap-free and
have no Bad triple, since protection depends on the fixed ambient U.
Its complement has n-2 points and cannot contain a target. This would
contradict the retained failure row. No smaller selection is enlarged,
and sizes 0,1,2 are not omitted.

Conversely, any real counterexample to the specified sufficient selector
has a canonical assignment: its real orientations, exact geometric,
End4/support/Covered/Bad flags, and exact mixed D and target T. The inherited
base holds, every new definition/containment row holds, and every failure
row holds by nonexistence. Hence every real counterexample yields a model.
The same Boolean descent argument gives the corresponding projection over
the reviewed abstract signotope base. SAT alone does not provide real
coordinates or a real counterexample.

In particular, accepted UNSAT of a reviewed unrestricted instance would
imply existence at **that exact ambient size**. No monotonicity in ambient
size is proved: deleting points changes End4 and protection. The permitted
shrinking above changes only A inside a fixed U. An m13 or m15 result
cannot simply be rounded up to a through-m13 or through-m15 statement.

## Rightmost extension consequence

An accepted protected selector A is already four-cap-free and target-hitting.
For any rightmost insertion r preserving no-five-cap, a hypothetical new
four-cap abc r in A+r would give

    y_r < line_bc(x_r) <= line_uv(x_r)

for an actual ambient four-cap support ending u,v. That ambient four-cap
would extend by r to a five-cap, a contradiction. Old targets are hit by A
and new targets involving r are hit by r. Thus the same preselected A,
augmented by r, is a weak Delta for every such insertion. The enlarged set
need not remain n-gon-free. This implication requires retaining the old
four-cap condition, as the block control demonstrates.

## Two-support control: uniform does not mean protected

Use the h=5 eight-point fixture

    (0,0),(1,1),(2,0),(3,4),(4,-3),(5,10),(6,-2),(7,5)

and A={0,3,6}. Exact integer checks confirm GP, no five-cap, no seven-gon
and ordinary weak Delta. At X=7+t the query and ambient terminal lines are

    q36=-2t-4;
    L24=-3t/2-15/2, L56=-12t-14, L57=-5t/2+5.

Their rational identity (L24+L57)/2=q36+11/4 proves uniform protection by
the envelope. No single ambient line has both slope and value at t=0
at least those of q36, so none dominates the entire rightward ray.
Both independently evaluated predicates consequently have Covered(3,6)
false and Bad(0,3,6) true. Both native generic CNFs accept those canonical
values and treat this specific A as failing their stronger selector rule.
They do not claim that uniform-envelope selection fails on this set.

## Reconstruction and controls

The independent Python program imports no parent or previous checker.
It reconstructs IDs and maps using combinations and masks; streams every
new row in order; compares inherited geometry prefixes to old generic
CNFs; and checks complete headers, literal counts and EOF. Rebuilt CNFs
and maps match the originals byte-for-byte. Candidate support pairs are
reconstructed from the pair relation; forced literals are derived via
permutation signs from endpoint inequalities. For canonical controls,
support truth is instead computed from direct integer line values.

| Instance | Variables | Old geometry rows | New rows | Total rows |
|---|---:|---:|---:|---:|
| cup n7/m15 | 69,673 | 79,326 | 114,554 | 193,880 |
| forced n7/m13 | 18,563 | 32,461 | 35,618 | 68,079 |

Independent compilation of frozen source snapshots reproduces both main
CNFs and maps byte-for-byte. Fourteen further generated cases have complete
streamed map/new-row checks, including nine canonical real assignments
counting the primary forced13 control. All non-failure clauses hold.
False failure rows correctly identify genuine working selections in the
controls; they are not unexpected verification failures.

Exact AND/OR truth tables cover 1,020 assignments, including empty ORs.
Mixed-witness deletion covers pass 786 explicit cases. Eight boundary
formulas at m=n-1 or n contain the expected empty failure clauses; six
out-of-domain invocations reject their parameters without producing files.
No failed real control or incomplete audit run occurred. The shared
archived compact main emits a pre-existing return warning when included
under a renamed entry point; it is not called. Warnings and commands remain
in the compile logs; neither frozen parent source was modified.

## Status, resources and boundaries

The parent's forced13 180-second preflight remains **UNKNOWN**, with its
receipt preserved. The cup15 solver remains separate work. No cup/forced
LRAT was replayed. The user's later reservation separately authorized
the [exact terminal-safe m13 replay](../exact_audit/replay13/README.md),
which completed and released its allocation before this handoff. Its
certificate is not evidence of UNSAT for either protection formula.

Every invocation used one CPU, affinity 5, nice 10, AS300 MiB, CPU19 and
wall20 seconds. Compilation used AS500 MiB and CPU18/wall20. Primary row
checks took 0.38/0.19 seconds, peaking at 41,992/38,252 KiB RSS. Compilation
peaked at 159,980 KiB RSS, under the separate 500 MiB allowance. No long
subtrack unit, timeout, OOM, swap, installation, git operation, deletion,
external action or other-record edit occurred. The subset and exact audit
packets remain frozen; the separate m15 realization audit was not repeated.
