# Completed minimum-slope partition

**Completed, 9 October 2026:** the minimum-slope split, junction removal,
three-chain exclusion and reindexing into actual induced configurations are
proved. Together with the balanced bound and projective transfer, this leaves
the residual population theorem as the explicit hypothesis for ES(8) ≤ 317.
That residual theorem is still unproved.

The main result is `ErdosSzekeres.Omission.Partition.exists_partition` in
[Partition.lean](../ErdosSzekeres/Omission/Partition.lean). For an ordered real
configuration with at least two points, no 7-cap and no convex octagon, it
constructs disjoint index sets `H` and `R` covering every point, with
`n = H.card + R.card`, and proves:

- The induced configuration on `H` has no 7-cap, no 7-cup and no convex octagon.
- The induced configuration on `R` has no 6-cap, no convex octagon and no
  junction formed by an incoming 6-cup and outgoing 5-cap at the same point.

The hypotheses refer to actual real points. Subsets are enumerated in their
original x-order, with the exact image set proved. Both junction witnesses are
transported through the same enumeration. No assertion equates ranks computed
inside a subset with ranks from its ambient configuration.

## Proof map

Prepend `ErdosSzekeres.Omission.` to every declaration below.

| Component | File | Main declarations and role |
| --- | --- | --- |
| Geometric chain closure | [PlanarChains.lean](../ErdosSzekeres/Omission/PlanarChains.lean) | `PlanarChains.chain3_all`, `positive_four`, `negative_four`: consecutive signs imply all ordered triple signs using real-plane transitivity. |
| Lists and actual cups/caps | [ListGeometry.lean](../ErdosSzekeres/Omission/ListGeometry.lean) | `ListGeometry.hasCup_of_list`, `hasCap_of_list`, `listCup_of_hasCup`, `listCap_of_hasCap`: transport in both directions; `hasNCup_octagon` gives an actual octagon. |
| Minimum-slope neighbours | [MinimumSlope.lean](../ErdosSzekeres/Omission/MinimumSlope.lean) | `MinimumSlope.exists_min_neighbors`, `cap_to_right`, `cup_from_left`: attained minima and strict signs; no global distinct-slope assumption. |
| Induced configurations | [Subsets.lean](../ErdosSzekeres/Omission/Subsets.lean) | `Subsets.restrict_image`, `restrict_no_cup`, `restrict_no_cap`, `restrict_no_octagon`, `no_junction_restrict`: preserve the actual selected points and witness restrictions. |
| Cup plus an upper point | [CupExtension.lean](../ErdosSzekeres/Omission/CupExtension.lean) | `CupExtension.cup_above_chord`: a point above the endpoint chord, within its horizontal span, forms a polygon with the cup; `cup7_cap3` specializes to an octagon. |
| Initial split and junctions | [SlopePartition.lean](../ErdosSzekeres/Omission/SlopePartition.lean) | `SlopePartition.upper_no_six_cap`, `lower_no_seven_cup`, `residual_no_junction`, `residual_no_six_cap`, `parts_cover`. |
| Three-chain contradiction | [ThreeChain.lean](../ErdosSzekeres/Omission/ThreeChain.lean) | `ThreeChain.three_chain`: the required incoming/outgoing chains force a forbidden 7-cap or an actual octagon. Shared interior points are permitted. |
| Complete partition | [Partition.lean](../ErdosSzekeres/Omission/Partition.lean) | `Partition.balanced_no_seven_cup`, `parts_disjoint`, `exists_partition`, `asymmetric_of_population_bounds`: prove the split and compose population bounds. |

The endpoint bookkeeping is explicit. A seven-cup in the balanced union
cannot start in the lower part or end at a junction. Its first point must
therefore be a junction and its last point in the lower part. The outgoing
cap's second point lies in the upper part, so it differs from that last point;
this supplies the exception required by the three-chain lemma.

## Exact remaining proposition

`Partition.ResidualBound 123` expands to:

```lean
∀ n : ℕ, ∀ c : Configuration n,
  ¬ c.HasCap 6 →
  ¬ HasConvexNGon 8 (Finset.univ.image c.point) →
  Subsets.NoJunctionOn c.cup (Finset.range n) → n ≤ 123
```

`NoJunctionOn` forbids two concrete chains entirely inside that configuration:
a six-point cup ending at a vertex and a five-point cap starting there.
General position and strict x-order are part of `Configuration`; real-plane
transitivity makes these consecutive-sign chains genuine cups and caps.

The [standalone composition](../experiments/omission-partition-2026-10-09/BalancedPartition.lean)
uses the previously checked large balanced certificate and proves:

- `OmissionBalanced.balanced_bound_192` with no added population assumption.
- `OmissionBalanced.asymmetric_315_of_residual_123`.
- `OmissionBalanced.forces_317_of_residual_123`.
- `OmissionBalanced.large_avoiding_set_has_residual`: any octagon-free
  general-position set of at least 317 points has an actual root-deletion chart
  and an induced residual subset of at least 124 points satisfying the three
  restrictions above. The chart maps and residual index set are retained.

The middle two statements are **conditional on the unproved residual bound**.
The last is a necessary condition on a putative counterexample, not its
exclusion. The residual arithmetic certificate remains partial. The residual state/domain
geometry, all 1,164 residual cycle rows and all 23 block capacities are now
proved in [the residual geometric transfer](OMISSION_RESIDUAL.md). That proof
reduces the remaining population bound to the explicit arithmetic proposition
`OmissionResidual.ExcludesThirtyHoles`. The current README and batch records
give the arithmetic progress; no complete residual root is claimed.

## Provenance and verification

The partition strategy and adapted proofs come from Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891), under MIT. The
[third-party record](THIRD_PARTY.md) maps every adapted module and retains the
copyright notice. The all-triples/list bridge and direct one-point cup extension
connect that argument to this project's polygon definition. No claim of an
independently discovered partition or improved global bound is made.

All eight modules build with warnings treated as errors and their 73 public
theorems are included in the main axiom audit. The large-certificate composition
is checked separately; [its record](../experiments/omission-partition-2026-10-09/README.md)
distinguishes this check from rebuilding the certificate trees.
