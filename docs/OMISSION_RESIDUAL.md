# Completed residual population bound and geometric transfer

**The residual population bound 123 and the global real-point bound
`ES(8) ≤ 316` are now checked.** The closed statements
`ErdosSzekeres.Omission.residual_population_123` and
`ErdosSzekeres.Omission.forces_convex_octagon_316` live in
[`FinalCover316.lean`](../experiments/omission-global-assembly-2026-10-10/FinalCover316.lean).
The [complete final record](../experiments/omission-global-assembly-2026-10-10/global-cover-316-check.json)
binds all arithmetic, geometry, and catalog bridges; its
[axiom output](../experiments/omission-global-assembly-2026-10-10/global-cover-316-axioms.txt)
reports only `propext`, `Classical.choice`, and `Quot.sound`. See
[OMISSION_ASSEMBLY.md](OMISSION_ASSEMBLY.md) for the complete reproduction.

For an actual `Configuration n` of real points in strict x-order and general
position, assume no 6-cap, no convex octagon, and no incoming 6-cup/outgoing
5-cap junction. The maintained library now proves its injective assignment to
the exact 154 residual states. The separately checked artifact proves that its
occupied states satisfy every one of the 1,187 literal omission rows.

The completed arithmetic route derives 402 additional inequalities from the
original 1,187 rows, then excludes every Boolean hole vector of total at most
30 with a 4,686-leaf certificate. All 149 proof parts and its root passed Lean.
The hole identity `sum holes + n = 154` therefore gives `n ≤ 123`. Together
with balanced population 191, the geometric partition gives threshold 316.
The older 145,474-leaf direct tree remains partial and is not used by this proof.

All names below are under `ErdosSzekeres.Omission`, except the standalone rows.

| Step | File | Principal checked declarations |
| --- | --- | --- |
| Attained future-cap ranks and actual past-cup ranks | `ResidualRanks.lean` | `rank_attained`, `rank_growth`, `label_bounds`, `labels_increasing` |
| Actual junction exclusion removes the exceptional label | `ResidualRanks.lean` | `noJunction_of_lists`, `forbidden_label` |
| Restricted Ferrers profiles and injective states | `ResidualStates.lean` | `state_injective`, `profile_count`, `residual_universe_bound` |
| Exact source catalog order | `ResidualCatalog.lean`, `ResidualCatalogData.lean` | `ownerIndex_profile`, `ownerIndex_injective`; four heights with the source's trailing zero |
| Actual points, exact owner count | `ResidualRealization.lean`, `ResidualCycleGeometry.lean` | `Configuration.residualOwner_injective`, `Configuration.residual_universe_bound`, `Configuration.residual_occupied_card` |
| Directed state differences and computed boxes | `ResidualDomains.lean`, `ResidualBoxes.lean` | `owner_contains`, `actual_pair_fits`, `computedTable_valid` |
| Positive geometric cycles | `ResidualCycleGeometry.lean` | `Configuration.residual_positive_of_checked_states`, `residual_checked_cycle_capacity`, `residual_list_cycle_hole_bound` |
| Compression to two cap-rank values | `BlockCompression.lean`, `BlockGeometry.lean` | `no_four_cap_of_rank2`, `actual_compressed_growth` |
| Baek's combinatorial prerequisite | `Baek.lean`, `Vendor/ETV/Main/Main.lean` | `Baek.four_cap_or_eight_gon`, `Baek.capacity22`; the upstream general `main` theorem is also kernel checked |
| Real convex boundary, with shared endpoints counted exactly | `BoundaryGeometry.lean`, `BaekGeometry.lean` | `boundary_convex_position`, `Boundary.card`, `boundary_polygon`, `hasNGon_octagon`, `geometric_capacity22` |
| Actual block capacity and omission inequality | `BlockGeometry.lean` | `block_capacity_ranks`, `block_hole_bound` |
| All literal row implications | Standalone `ResidualGeometry.lean` and `ResidualAllGeometry.lean`, archived in the artifact | `OmissionResidual.all_nonblock_rows`, `OmissionResidual.all_geometric_rows` |
| Exact arithmetic handoff | Standalone `ResidualReduction.lean` | `OmissionResidual.feasible_holes`, `residual_bound_of_arithmetic`, `forces_317_of_arithmetic` |
| Derived arithmetic rows | Standalone `ResidualCoverCuts.lean` | `ResidualCoverCuts.all_rows`: all 402 rounded-cover consequences of the original rows |
| Complete arithmetic exclusion | Generated `ResidualCoverProof.Root` and its 149 parts | `OmissionResidualCover.excludes_budget`: no feasible vector with at most 30 holes in the 1,589-row system |
| Exact catalog identification | Standalone `ResidualCoverBridge.lean` | `OmissionResidualCover.base_catalog_matches`, `cut_catalog_matches`, `all_cover_rows`, `exclusion_transfer` |
| Closed actual bound and global result | Standalone `FinalCover316.lean` | `ErdosSzekeres.Omission.residual_population_123`, `forces_convex_octagon_316`, `convex_octagon_of_card_ge_316` |

The original `forces_317_of_arithmetic` theorem is a conditional interface:
the balanced bound and `ExcludesThirtyHoles` imply `ForcesConvexNGon 317 8`.
The arithmetic premise is a proposition definition, not an axiom. Its exact
hole exclusion is now supplied through the checked compressed root and catalog
transfer. `OmissionResidual.residual_bound_of_hole_budget`, in
`ResidualBudgets.lean`, supplies the parameterized population interface used by
the final assembly. `feasible_holes` is unconditional under the stated residual
geometric restrictions and concludes `sum holes + n = 154` for a Boolean
vector satisfying every original literal row. The global theorem derives the
residual restrictions from its partition; it assumes only general position
and the cardinality threshold on the original real point set.

The generated cycle checker handles rows below 1165 except row 973. The 23
block checks handle row 973 and rows 1165–1186. Coverage is proved inside Lean;
row 973 is not accidentally counted as a cycle. Every generated module checks
its literal support and demand against the same arithmetic catalog.

The [artifact](../experiments/omission-residual-geometry-2026-10-09/README.md)
contains 39 successful cycle-module checks, 24 successful block/composition
checks, three further reduction theorems, their axiom outputs and hashes.
Corrupted cyclic order and collapsed block thresholds are both rejected by
Lean in negative controls. That 9 October artifact's 444-root maintained-library
audit is historical; current library validation is in [VALIDATION.md](VALIDATION.md).
The [10 October cover artifact](../experiments/omission-cover-certificates-2026-10-10/README.md)
and [global assembly artifact](../experiments/omission-global-assembly-2026-10-10/README.md)
preserve the new complete arithmetic and final theorem records separately.
The default library build is not counted as a replay of the generated trees.

Further arithmetic budgets and stronger numerical thresholds remain separate
candidates until their own complete roots and global statements pass. The
original geometric transfer is already complete; these candidates do not
leave an unproved geometric assumption inside the checked 316 result.

The ranks, restricted-state method, block compression and supporting-line
strategy follow Michael Schroeder's version-1 archive,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
Baek's proof code is Apache-2.0, Schroeder's original proof code is MIT, and
literal catalog/cycle/block data are CC BY 4.0. Local changes use this project's
real-plane and convex-position definitions and replace evaluation shortcuts
with kernel proofs. See [THIRD_PARTY.md](THIRD_PARTY.md); no independent discovery
or priority claim is made for these geometric arguments.
