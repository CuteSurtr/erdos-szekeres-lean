# Balanced omission geometry

This is the geometric connection for the 252-state balanced system, separate
from the still-unfinished full octagon bound. All points are in `Fin 2 → ℝ`.

**Completed, 9 October 2026:** `OmissionBalanced.real_configuration_bound`
proves `n ≤ 192` under the hypotheses below. All 2,685 geometric rows and the
final assembly passed Lean, with only `propext`, `Classical.choice` and
`Quot.sound` as transitive axioms. The full sources, check records and
reproduction instructions are in the
[balanced geometry artifact](../experiments/omission-balanced-geometry-2026-10-09/README.md).

## Exact hypotheses

`ErdosSzekeres.Omission.Configuration n` consists of `point : Fin n → Point`,
strictly increasing x-coordinates, and nonzero determinants for every increasing
triple. `Configuration.ofGeneralPosition` constructs this structure from the
repository's ordinary `GeneralPosition` predicate and the x-order hypothesis.
Strict x-order implies the points are distinct.

`c.HasCup k` means that some increasing selection of `k` indices has positive
orientation on **every** increasing triple. `c.HasCap k` uses negative
orientation. They are geometric predicates about the actual coordinates.
`HasConvexNGon 8 (Finset.univ.image c.point)` uses the repository's existing
convex-position definition, with no emptiness requirement.

The balanced subcase assumes no 7-cup, no 7-cap, and no convex octagon. These
are explicit extra restrictions: an arbitrary octagon-free point set need not
avoid 7-cups and 7-caps. Removing that distinction requires the residual and
partition arguments; it cannot be inferred from the balanced theorem alone.

## Checked proof components

Prepend `ErdosSzekeres.Omission.` to the names in this table.

| Step | Files and main declarations | What is proved |
| --- | --- | --- |
| Attained ranks | [ActualRanks.lean](../ErdosSzekeres/Omission/ActualRanks.lean): `ActualRanks.rank_attained`, `rank_growth` | Ranks come from actual ending paths and grow in the required coordinate. |
| Real paths → geometric cups/caps | [Realization.lean](../ErdosSzekeres/Omission/Realization.lean): `Configuration.endingPath_hasCup`, `endingPath_hasCap` | Consecutive path signs imply the all-triples geometric predicate, using the existing horizontal transitivity proofs. |
| State encoding and coverage | [BalancedStates.lean](../ErdosSzekeres/Omission/BalancedStates.lean), [Ferrers.lean](../ErdosSzekeres/Omission/Ferrers.lean), [BalancedCatalog.lean](../ErdosSzekeres/Omission/BalancedCatalog.lean): `ActualRanks.balancedState_injective`, `Ferrers.profile_count`, `BalancedCatalog.ownerIndex_profile` | Every actual point has one of the 252 Ferrers profiles, in the exact catalog order. |
| Injective assignment | [Realization.lean](../ErdosSzekeres/Omission/Realization.lean): `Configuration.balancedOwner_injective`, `balanced_universe_bound` | Distinct points receive distinct catalog indices; this already gives the classical bound 252 under no 7-cup/no 7-cap. |
| Pair-label domains | [Domains.lean](../ErdosSzekeres/Omission/Domains.lean): `Domains.actual_pair_fits`; [BoundingBoxes.lean](../ErdosSzekeres/Omission/BoundingBoxes.lean): `Domains.computedTable_valid` | Every actual pair label lies in the box computed from the directed difference of its two states. The box theorem is uniform; an external box table is unnecessary. |
| All six point orders | [CycleSigns.lean](../ErdosSzekeres/Omission/CycleSigns.lean): `CycleSigns.checked_triple_positive` | A validated cyclic triple has positive real orientation regardless of the chronological order of its owners. |
| Cycle → convex octagon | [CycleGeometry.lean](../ErdosSzekeres/Omission/CycleGeometry.lean): `Configuration.checked_cycle_capacity`, `list_cycle_hole_bound` | A checked cycle has at most seven occupied states in an octagon-free configuration. A row of size `k` therefore has at least `k-7` holes. |
| Small literal example | [FirstCycle.lean](../ErdosSzekeres/Omission/FirstCycle.lean): `Configuration.first_row_hole_bound` | The first eight-state row has at least one missing state, derived from the actual geometric hypotheses. |

The large, separate row check proves `CycleValid` for each of the source's
2,685 cycles of lengths 8–10. Each check also proves equality with that row's
literal support and demand in the previously checked arithmetic catalog.
Python emits Lean source; it does not supply a trusted geometric fact.

## Attribution and trust

The state/rank and sign strategy, several adapted proof modules, and the
catalog/cycle data come from Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891). Adapted code is MIT;
catalog and cycle data are CC BY 4.0. The exact module mapping, license notice,
and local changes are in [THIRD_PARTY.md](THIRD_PARTY.md). The real-coordinate
connections and computed-box proof were added here. No independent invention
or priority claim is made for the strategy.

The default library includes the components in the table. The generated large
certificates are separate artifacts with their own check records. Neither
the finished Suk theorem nor the finished HMPT theorem depends on this work.
The subsequent [projective reduction](OMISSION_PROJECTIVE.md) connects this
bound to arbitrary real point sets: every octagon-free set of at least 194
points has a root-deletion chart containing a 7-cup. It also completes the
conditional transfer from `AsymmetricBound 315` to ES(8) ≤ 317. That population
hypothesis, including the residual and partition arguments, remains unproved;
see the [remaining-work record](ES8_REMAINING.md).
