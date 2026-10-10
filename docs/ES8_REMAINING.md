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
| 313 through the residual side | Finish the 32-hole exclusion, check its complete arithmetic proof in Lean, then compose it with the now-proved full geometric transfer. | The resumed tree has eight pending leaves within three of the original 24 contexts. Eleven original contexts have Lean proofs; ten more have complete integer-replayed subtrees. One side of the state-43 split is closed arithmetically. The partial tree has 391,293 leaves, about eight times the completed residual31 proof. Similar packing could require thousands of generated Lean parts; compression could change that size substantially. Unexplored subtrees prevent a reliable completion-time estimate. |
| Further improvements | Find stronger necessary constraints or a stronger counting argument, and prove the complete resulting reduction. | The newer coupled and structural geometric rows are individually proved. They do not themselves establish a stronger population bound, and no reliable estimate for another global improvement is available. |

The enlarged residual model has 2,469 rows, including twelve arithmetic
consequences. Its [full literal geometric binding](../experiments/omission-residual32-transfer-2026-10-10/README.md)
is now proved in Lean. `OmissionResidual32Transfer.all_rows` establishes every
indexed row for the same actual residual assignment, and `feasible_holes`
proves the population equation `sum holes + n = 154`. The conditional theorem
`residual_bound_of_hole_budget` isolates the arithmetic exclusion still needed;
it does not supply that exclusion. The existing chart and partition can then
be reused. Whether this finite Boolean model excludes 32 holes remains unresolved.

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
bounds, and they do not establish tightness of the newest model.

The source method and comparison remain Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891). No currently-best-bound
or priority claim is made. These finite improvements do not change HMPT's
asymptotic coefficient.
