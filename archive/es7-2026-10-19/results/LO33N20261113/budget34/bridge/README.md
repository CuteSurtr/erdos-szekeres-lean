# PROVED conditional bridge; slice 19 EXACT TREE; ES(8) <= 308 remains open

14 November 2026. Bounded mathematical sidecar, finalized before 10:40 KST.
The dependency receipts and source-audit cutoff time are in
[source-audit.json](data/source-audit.json). **Not fully Lean-checked;
unrefereed.** No Lean build, solver, tree replay, certificate check, web
request or git operation was performed here. Writes are confined to this
directory. Parent developments after the recorded cutoff require a new status.

## 1. Statement

**PROVED conditional deduction.** Under the established geometric inputs
below, exclusions of the two budget-34 slices
`(h(F)>=19,h(Lo)>=15)` and `(h(F)>=20,h(Lo)>=14)` imply **ES(8)<=308**.
Slice 19 now has a completed independent **EXACT TREE** replay. Consequently
**N66<=55 implies ES(8)<=308**, using the inherited N5<=65 result and its
evidence limitation in section 4. Neither N66<=55 nor ES(8)<=308 is claimed.

The initial slice-20 row system has a valid abstract witness. The parent's
seven additional cuts and 3,471-row version are separate, ongoing work.

## 2. Model, hypotheses and soundness

Let S be a finite set of real planar points in general position (no three
collinear), with no convex octagon. The existing projective chart and
minimum-slope partition give H,R with `|S|<=1+|H|+|R|`. In the chart's
fixed x-direction, both are configurations with distinct x-coordinates:

- H has no 7-cap, no 7-cup and no convex octagon.
- R has no 6-cap, no convex octagon and no junction consisting of an
  ambient 6-cup ending at the start of an ambient 5-cap.

The Lean composition handles the chart and the small cases. No rotation
preserving a directional cap/cup prohibition is being assumed. Empty R
satisfies every population bound used below. For nonempty R, its injective
owner map has image O in the 154-state catalog C, with state 0 in O. Define
`h_i=0` for occupied states and `h_i=1` otherwise, and `h(A)=sum_(i in A) h_i`.
Then `h_0=0`, `|R|+h(C)=154`, and all 2,650 Lean covering inequalities
`h(S_r)>=d_r` hold. These are statements about the same ambient R and its
state indexing, not states recomputed separately on its subsets.

Define `F={f1>=5}`, `Lo={f1<=4}`. They partition C with sizes 84 and 70.
The first height is the longest ambient cup ending at the owner minus one.
Thus F owners are the endpoints of ambient 6-cups. A 5-cap on F owners
would start at such an endpoint, violating no-junction. A 6-cup on Lo
owners would end in F, a contradiction. Both subsets inherit octagon
avoidance and general position, and Lo inherits no 6-cap. Therefore

    h(F) >= 84-N5,       h(Lo) >= 70-N66.                 (A)

Here N5 bounds all octagon-free, 5-cap-free configurations in their given
x-direction; N66 bounds all octagon-free configurations with neither a
6-cap nor a 6-cup. The established bounds 65 and 56 give F19 and Lo14.
This is the written [Lemma A](../../../THEORY310N20261113/README.md),
independently checked against the Lean definitions in
[VERIFY_LO, section 2.6](../../VERIFY_LO.md).

Let Q be the pinned 812 coupled covering inequalities. Their use additionally
requires: every support CNF is a sound relaxation of the owners of every
actual residual configuration, and its hash-matched LRAT is accepted by
cake_lpr with the exact line `s VERIFIED UNSAT`. This combines the written
encoder audit with the completed independent pool replay; an UNSAT solver
status alone is insufficient. No equality-case, symmetry or extra geometric
assumption may be introduced silently in a new cut.

## 3. Proofs: baseline, bridge and remaining equality case

**Baseline 309 (PROVED, inherited computer-assisted chain).** The Lean
budget-32 exclusion gives `h(C)>=33`. Nine base rows, indexed

    973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315,

each have demand 6 and support of size 28 in F; they cover each F state
three times. Summing gives `3h(F)>=54`, hence `h(F)>=18`. By (A) and
N66<=56, `h(Lo)>=14`. If `h(C)<=33`, it equals 33 and `h(F)` is 18 or 19.
The independently replayed budget-33 Lean-only trees exclude respectively
`(F18,Lo15)` and `(F19,Lo14)`. Their only pending branch is state 0 missing,
impossible for actual nonempty R. Hence `h(C)>=34`, `|R|<=120` and
`|S|<=1+187+120=308`; therefore ES(8)<=309. This preferred chain uses
neither N5 nor the residual coupled rows. See
[ES309's two-slice chain](../../../ES309N20261113/README.md).

**Bridge to 308 (PROVED conditional).** Assume no Boolean vector exists
at budget 34 for either of the following systems: all 2,650 base rows, Q,
`h_0=0`, and the two displayed capacity rows.

| Budget-34 slice | h(F) | h(Lo) | F owners | Lo owners |
|---|---:|---:|---:|---:|
| 19 | 19 | 15 | 65 | 55 |
| 20 | 20 | 14 | 64 | 56 |

For an actual R with `h(C)<=34`, the baseline forces equality; (A) restricts
`19<=h(F)<=20`. The matching slice excludes its hole vector. Thus
`h(C)>=35`, `|R|<=154-35=119`, and `|S|<=1+187+119=307`.
The forcing threshold is **187+119+2=308**, by
`Partition.forces_of_population_bounds` with its positivity premise
`1<=187+119`. The two capacity demands sum to 34, so the rows plus budget
already enforce the equalities in the table. These are conditional slice
rows, not separate unconditional capacities F<=64 or Lo<=55.

**One completed slice (PROVED conditional corollary).** With N5<=65 and a
future proof of N66<=55, (A) gives F19 and Lo15. Any vector with at most 34
holes is in slice 19, now excluded by its EXACT TREE. Hence residual
population<=119 and ES(8)<=308. This deduction needs no budget-33 tree.
N66<=56 supplies only Lo14 and cannot replace the antecedent 55 here.

**Remaining equality case (PROVED necessary condition).** Using the current
bounds and the completed slice 19, any actual R with 120 owners must have
**64 F owners and 56 Lo owners**. A hypothetical 308-point octagon-free S
must saturate every population inequality:

    |H|=187,  |R|=120,  |R intersect F|=64,  |R intersect Lo|=56.

Indeed `308<=1+|H|+|R|<=1+187+120=308`. Here the last two intersections
mean owner preimages of the state families. Thus the Lo subset attains
the current N66 upper bound. The two residual-only instances omit the
requirement that R coexist with a saturated balanced part in one partition.
These necessary conditions alone do not exclude the case.

## 4. Existing records and exact proof status

| Input | Evidence used; boundary |
|---|---|
| Balanced 187 and population composition | **PROVED, existing Lean components.** `Compact310.balanced_population_187` in `Final310Compact.lean`; `Partition.forces_of_population_bounds` in `PopulationBounds.lean`. The 10 November real assembly receipt says verified, with only `propext, Classical.choice, Quot.sound`. |
| Residual catalog, owners, rows and budget 32 | **PROVED, existing Lean components.** `Residual32Bridge2650/Rows.lean`: `all_rows_2650`, `holes_sum_add_population`; `zero_mem_residualOccupied`; `E310.residual_excludes_32 : Excludes2650Zero 32`. Catalog/JSON correspondence was independently checked in VERIFY_LO. |
| N5<=65 | **PROVED written with recorded CERTIFIED components**, [ETV5 and VERIFY_N5](../../../ETV5N20261113/VERIFY_N5.md). Independent arithmetic encoder, 32/32 accepted cubes; all row justifications checked. Only 2/299 template and 1/428 core proofs were freshly re-certified in that audit; the rest inherit recorded verdicts. **Both original and independent arithmetic LRATs were deleted**, per those records. This memo inherits the audited result, not a fresh retained-proof replay. |
| N66<=56 | **PROVED written with CERTIFIED components**, [followup56](../../../VERIFY309N20261113/followup56/VERIFY_N66_56.md). All 319,611 trimmed clauses recognized, 6,775 used rows justified, 624 supporting CNFs covered by 620 prior checks and four fresh certificates; retained main LRAT independently accepted. Mirror symmetry is justified by reflecting the real configuration if needed. Not Lean-checked. |
| Baseline slices 18,19, budget 33 | **EXACT TREE**, independently replayed in [VERIFY_LO](../../VERIFY_LO.md): 3,815 and 186,077 nodes, minimum margin 1, only state-0-missing pending. Only base rows and respective slice capacities. |
| Frozen Q, 812 rows | **CERTIFIED**, [pool summary](../audit/pool_summary.json), completed 10:12:14 KST: 812 independent encoder reconstructions, 812 retained LRAT hash matches and fresh exact stdout acceptances. Written geometric soundness inherited from [VERIFY309, link (c)](../../../VERIFY309N20261113/README.md). |
| Slice 19, budget 34 | **EXACT TREE**, [independent summary](../audit/s19-summary.json), completed 10:16:01 KST: 3,643/3,643 contexts, 1,658,483 nodes, 829,242 leaves, minimum margin 1; sole pending state-0-missing branch; 447 coupled rows used. No replay repeated here. |
| Initial slice 20, budget 34 | **COMPUTED finder witness**, independently checked by the SAT track against every row and all 283,115 combined-CNF clauses: 34 holes, F20/Lo14. The explicit integer witness refutes exclusion for that frozen abstract system; it supplies no real configuration or ES lower bound. The receipt under `sat/parent-witness-1/` is hashed in source-audit.json. |
| Parent's slice-20 version 2 | Parent reports seven fresh CNF/LRAT cuts killing the first witness and 3,471 total rows prepared. New cut soundness/provenance and full strengthened exclusion remain parent/audit obligations; not checked here. Killing one witness does not close a slice. |

The 309 chain, the above geometric capacity transfer, slice gluing, new
corollary, CNF soundness/certification and Python tree replay are outside
the current Lean theorem. No `Excludes2650Zero 34` over the base rows alone
is established. A future formal export must include the extra valid rows
and capacity hypotheses, or prove the actual residual bound directly.

## 5. Elementary slice restrictions and adversarial review

**PROVED redundant restrictions from already proved inequalities.** Let
B_j be the nine Baek supports listed above and `e_j=h(B_j)-6>=0`. Their
incidence identity gives `sum_j e_j=3h(F)-54`. Therefore:

| Slice | Total block slack | Every block's hole count | Tight blocks guaranteed |
|---|---:|---:|---:|
| 19 | 3 | 6 through 9 | at least 6 |
| 20 | 6 | 6 through 12 | at least 3 |

The upper bounds follow because no nonnegative summand exceeds the total;
at most that many integer slacks are positive. In particular row 973 is
exactly `{f1=6}`, so its 28 states have 19..22 owners in slice 19 and
16..22 in slice 20. Equivalently `h(F\B_j)>=48-2t` at slice t: demand 10
for t=19, demand 8 for t=20. These complement rows are not explicitly in
the frozen inputs, but are already implied, even over the real LP
relaxation, by the nine rows and `h(F)<=t`. The tight-block count uses
integrality. They may guide branching; they provide **no additional
mathematical exclusion** for a valid witness of the existing rows.

The [supplied initial slice-20 witness](data/s20-v1-witness.json) has nine block hole counts
`(6,6,7,6,6,6,6,6,11)` in the listed order. Its slack is `1+5=6`; it
satisfies these restrictions. This identity does not rule out that witness
or prove 35 total holes.

Critical boundaries checked:

- With its rows, weights and node fixed, a budget-33 weighted leaf has
  margin `m_34=m_33-C` at budget 34, where C is its leaf capacity.
  Positive old margins need not remain positive;
  old slices 19/20 also have different Lo demands. They cannot be relabelled.
- An EXACT TREE needs all master contexts, correct paths and input hashes,
  positive exact leaf margins at **34**, and no unresolved branch other
  than state 0 missing. A finder verdict or partial replay is insufficient.
- Slice 19 may keep its original row pool when slice 20 gains sound rows:
  actual residual vectors satisfy both systems. Row ordering must remain
  matched to each tree's weights; closure does not require identical pools.
- The slice-20 witness concerns the initial 3,464-row system. It cannot
  refute a strengthened system containing a cut it violates. Conversely,
  refuting that witness alone proves neither full UNSAT nor ES(8)<=308.
- No ETV conjectural value, unproved N66<=55, stronger balanced bound,
  solver status, or sample of real sets is used as a theorem here.

## 6. Method, controls, files and hashes

Read the house rules and newest status, inspected the cited proof records
and Lean source signatures, and derived the counting arguments above.
Only small standard-library Python reads were used, each under AS150MiB
and one-CPU affinity; no external proof check was duplicated.

[check_sources.py](tools/check_sources.py) records the pinned source counts,
nine-row incidence and explicit cut absence, selected inherited receipts,
and hashes in [source-audit.json](data/source-audit.json). These are exact
finite source identities, not a solver or certificate-verifier result.
The [parent input manifest](../data/input-manifest.json) pins both initial
instances. SHA256SUMS pins this memo and its supporting files. The live
`WITNESS.json` changed during this sidecar; the context-94 witness was
recovered from `WITNESS.refuted-1.json`, matched to the independent source
receipt, and preserved byte-for-byte here. No large
proof or tree is copied, read in full, modified or deleted by this sidecar.

## 7. What remains and resume

The only missing finite exclusion in the current 65/56 route is slice 20
with a sufficiently strong, sound row system. Consume the parent's final
cut provenance and [audit receipts](../audit/VERIFY_BUDGET34.md); if that
slice closes, apply section 3. If it does not, retain the completed
conditional 55 corollary and the remaining equality case. No further
sidecar compute is needed; N5's historical proof-retention limitation must
remain visible in any resulting statement.
