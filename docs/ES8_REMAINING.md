# Finite octagon status and remaining work

**10 October 2026: ES(8) ≤ 314 is proved. No geometric transfer or arithmetic
obligation remains for that theorem.** This also settles every former project
target from 317 down to 315. Their earlier proof records remain preserved.

The closed results are `ErdosSzekeres.Omission.forces_convex_octagon_314` and
`convex_octagon_of_card_ge_314`, in
[FinalCover314B61FusedR31Fused.lean](../experiments/omission-global-assembly-2026-10-10/FinalCover314B61FusedR31Fused.lean).
The [complete check record](../experiments/omission-global-assembly-2026-10-10/global-cover-314-check.json)
binds 3,929 unchanged inputs and contains successful final axiom reports.
It uses only `propext`, `Classical.choice` and `Quot.sound`. Its scope is
arbitrary finite real planar point sets in general position, with no
emptiness requirement for the polygon.

## What closed the geometric transfer

The projective chart removes one point and excludes 7-caps. The minimum-slope
partition gives balanced and residual induced configurations with all needed
avoidance and junction conditions. Actual attained ranks inject those points
into the 252- and 154-state catalogs. All 2,685 balanced and 1,187 residual
constraints are proved for those assignments, including the Baek block bound
and its supporting-line transfer to convex real polygons.

The checked arithmetic exclusions rule out at most 61 balanced holes and at
most 31 residual holes, giving populations at most 190 and 122. Thus an
avoiding original set has at most `190 + 122 + 1 = 313` points. The next integer
314 is the forcing threshold. No abstract-model realizability assumption is
used in that implication. The balanced and residual arithmetic certificates
contain 22,318 and 50,945 leaves, respectively; their 446 and 1,108 rounding
cuts and exact catalog identifications are also checked in Lean.

## Stronger research targets, not completed bounds

| Target | Required work | Unknowns and rough size |
| --- | --- | --- |
| 313 through the balanced side | Exclude at most 62 balanced holes, export and check a complete arithmetic proof, then reuse the proved geometric interface. | The bounded witness search was inconclusive. No exclusion or 62-hole witness was found. The geometric transfer for the present catalog is already available, but there is no reliable search or proof-size estimate. |
| 313 through the residual side | Exclude at most 32 holes using stronger geometry, check the complete arithmetic certificate and its literal row binding, then compose the result with the partition. | The old 2,469-row catalog admits a Lean-checked 32-hole witness, so its full exclusion is impossible. A new core, 128 Fourth-template rows, 48 relaxed Sixth-template rows, and four further coupled rows are geometrically proved. The resulting 2,650-row system excludes that witness, but bounded searches remain inconclusive. A prior partial tree already had 391,293 leaves; a successful new proof could differ radically in size. There is no reliable completion-time or proof-size estimate. |
| Further improvements | Find stronger necessary constraints or a stronger counting argument, and prove the complete resulting reduction. | The newer coupled and structural geometric rows are individually proved. They do not themselves establish a stronger population bound, and no reliable estimate for another global improvement is available. |

The enlarged residual model has 2,469 rows, including twelve arithmetic
consequences. Its [full literal geometric binding](../experiments/omission-residual32-transfer-2026-10-10/README.md)
is now proved in Lean. `OmissionResidual32Transfer.all_rows` establishes every
indexed row for the same actual residual assignment, and `feasible_holes`
proves the population equation `sum holes + n = 154`. The conditional theorem
`residual_bound_of_hole_budget` isolates the arithmetic exclusion still needed;
it does not supply that exclusion. The existing chart and partition can then
be reused. The old model is now proved to admit 32 holes; that conditional
interface cannot be discharged from these rows alone.

The [case-4 witness](../experiments/omission-residual32-case4-2026-10-10/README.md)
is checked in Lean and satisfies every old row, the branch context, and
occupation of state zero. Cases 2 and 7 remain incomplete. Their partial
certificates cannot change the feasibility of case 4. The
[new coupled obstruction](../experiments/omission-residual32-witness-coupled-2026-10-10/README.md)
proves that this witness is not geometrically realizable and supplies a valid
new row. The [128-row Fourth-template family](../experiments/omission-residual32-fourth-global-variants-2026-10-10/README.md)
is also Lean-checked. A [relaxed Sixth template](../experiments/omission-residual32-sixth-relaxed-2026-10-10/README.md)
adds 48 further Lean-checked inequalities. Four further [coupled certificates](../experiments/omission-residual32-rank-certificates-2026-10-10/README.md)
bring the current total to 2,650 rows. The strengthened model
has no complete exclusion or feasible 32-hole witness at this checkpoint;
one saved 32-hole candidate still violates only row 973, while the other saved
basins now fail additional new rows. The geometric necessity of
these additional rows is finished. Whether the combined inequalities force
at least 33 holes is unknown.
The separately proved [attained-rank restriction](../experiments/omission-residual-rank-attainment-2026-10-10/README.md)
bounds an edge's cup label by its source height plus one. It removes 13,832
candidate edge labels, but produces no new incompatible pair or bounding-box
forced triple sign in the finite assessment. Two of the new certificates use
16 and 3 instances of its coupled clause. However, the new
[normalization theorem](../experiments/omission-residual-rank-normalization-2026-10-10/README.md)
proves that this bound does not change satisfiability of the abstract coupled
model: clipping cup labels preserves all its constraints on the same occupied
states. Thus it can help individual proof certificates but cannot alone
exclude more abstract supports. The theorem does not cover additional
equations expressing exact attained ranks or establish realizability.

The four new rows successively strengthen the previous conjunction, as
checked by exact 33-hole countermodels. They also exclude the entire saved
306-vertex single-swap component of 33-hole assignments. This is a finite
local-search result, not an enumeration of all 33-hole assignments or a
global 32-hole exclusion. The [2,650-row search record](../experiments/omission-residual32-rank-global-2026-10-10/README.md)
separates these checks from the bounded solver runs.
See [MATH.md](MATH.md) for the exact population calculation and certificate logic.

The [new residual checkpoint](../experiments/omission-residual32-resume-2026-10-10/README.md)
preserves the resumed tree's identity and sixteen closed conditional subtrees;
the earlier frozen tree remains unchanged. The [five-cut Lean bundle](../experiments/omission-residual32-context-certificates-2026-10-10/README.md)
and transfer bundle distinguish checked theorems from integer search evidence.
The [six resumed Lean subtrees](../experiments/omission-residual32-resume-lean-2026-10-10/README.md)
discharge 44 splits and 50 weighted leaves and supply actual geometric corollaries.
The [balanced search diagnostic](../experiments/omission-balanced62-research-2026-10-10/README.md)
and [SAT continuation](../experiments/omission-balanced62-sat-2026-10-10/README.md)
are inconclusive. The separately proved occupancy of state zero is an additional
actual-rank restriction; fixing it closed no extra original context in the
numerical probe. No stronger bound follows from these partial results.

A Lean-checked 32-hole abstract witness satisfies all 1,187 original residual
rows and all 45 earlier additions. Later searches found further witnesses for
some intermediate models. These expose limitations of those specific Boolean
models; they do not provide real residual configurations or Erdős–Szekeres lower
bounds, and they do not establish tightness of the newest strengthened model.

The source method and comparison remain Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891). No currently-best-bound
or priority claim is made. These finite improvements do not change HMPT's
asymptotic coefficient.
