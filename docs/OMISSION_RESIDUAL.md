# Completed residual geometric transfer

For an actual `Configuration n` of real points in strict x-order and general
position, assume no 6-cap, no convex octagon, and no incoming 6-cup/outgoing
5-cap junction. The maintained library now proves its injective assignment to
the exact 154 residual states. The separately checked artifact proves that its
occupied states satisfy every one of the 1,187 literal omission rows.

This finishes the residual geometric transfer in the current reduction. It
does **not** prove that at most 123 states can be occupied. The complete stronger
integer certificate has been replayed outside Lean; its large Lean tree remains
partially checked. [Remaining work](ES8_REMAINING.md) gives the precise boundary.

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

The last theorem is conditional: the completed balanced bound and an actual
proof of `ExcludesThirtyHoles` imply `ForcesConvexNGon 317 8`. The arithmetic
premise is a proposition definition, not an axiom. `feasible_holes` is
unconditional under the stated residual geometric restrictions and concludes
`sum holes + n = 154` for a Boolean vector satisfying every literal row.

The generated cycle checker handles rows below 1165 except row 973. The 23
block checks handle row 973 and rows 1165–1186. Coverage is proved inside Lean;
row 973 is not accidentally counted as a cycle. Every generated module checks
its literal support and demand against the same arithmetic catalog.

The [artifact](../experiments/omission-residual-geometry-2026-10-09/README.md)
contains 39 successful cycle-module checks, 24 successful block/composition
checks, three further reduction theorems, their axiom outputs and hashes.
Corrupted cyclic order and collapsed block thresholds are both rejected by
Lean in negative controls. The default library's 444-root audit is recorded
separately; it does not pretend to compile the large generated certificates.

The ranks, restricted-state method, block compression and supporting-line
strategy follow Michael Schroeder's version-1 archive,
[DOI 10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891).
Baek's proof code is Apache-2.0, Schroeder's original proof code is MIT, and
literal catalog/cycle/block data are CC BY 4.0. Local changes use this project's
real-plane and convex-position definitions and replace evaluation shortcuts
with kernel proofs. See [THIRD_PARTY.md](THIRD_PARTY.md); no independent discovery
or priority claim is made for these geometric arguments.
