# ES(8) ≤ 317: remaining work

**Status, 2026-10-09: ES(8) ≤ 317 is not proved. The balanced geometric subcase,
minimum-slope partition and projective/root transfer are complete.**
The finished Suk and HMPT real-point theorems do not depend on this project.
The actual-point state encoding and geometric cycle soundness are now proved;
see [the balanced geometry record](OMISSION_GEOMETRY.md) and
[the projective proof map](OMISSION_PROJECTIVE.md). The
[completed partition](OMISSION_PARTITION.md) now reduces the target to
`Partition.ResidualBound 123` alone.

Two complete exact integer certificates exclude the stronger budgets in the
literal balanced and residual omission systems, giving occupancy bounds 192
and 123. Two independent programs replayed them. Lean now checks the complete
balanced tree, all 2,685 balanced row encodings and their geometric necessity,
and the actual-point balanced bound 192. The residual tree remains incomplete.
See the [balanced geometric proof artifact](../experiments/omission-balanced-geometry-2026-10-09/README.md).

| Remaining component | What would be required | Present uncertainty |
| --- | --- | --- |
| Complete arithmetic certificates | Finish the 145,474-leaf residual tree, compose every branch, and audit its final root. The 9,862-leaf balanced tree and its finite occupancy corollary are done. | The balanced 898-part build succeeded. The first 330 residual parts (13,827 leaves) are checked. The other 3,081 parts and root remain. The most recent 20-part block took about 15 minutes on this Mac; a simple extrapolation suggests roughly 39 hours for the remaining parts, but part sizes vary and that is not a benchmark or completion promise. |
| Real points → states | **Done for the balanced subcase:** attained ranks, Ferrers profiles, catalog coverage, exact indexing, and the injective actual-point owner map are proved in `ErdosSzekeres/Omission/`. | The partition now supplies actual residual points and the required no-6-cap/no-junction restrictions. Their encoding by the residual two-sided ranks, restricted states and literal catalog remains to be proved. |
| Geometric necessity of every row | **Done for all 2,685 balanced rows**, including support and demand alignment with the arithmetic catalog. Still needed: residual restricted-domain cycle constraints and all 23 block constraints using the relevant Baek-style geometric bound. | The residual geometric proof and its enumerations have not been ported under this project's trust rules. Balanced row checks do not discharge residual rows. |
| Partition | **Done:** minimum-slope neighbours, junction removal, three-chain exclusion, disjoint cover, exact cardinality and all avoidance conditions on the induced configurations. | `Partition.exists_partition` has no unproved splitting hypothesis. `asymmetric_of_population_bounds` composes 192 and 123; only the residual population bound remains unproved after importing the finished balanced certificate. |
| Projective/root transfer | **Done:** normalize an arbitrary real set, delete a leftmost root, order the chart, preserve cardinality and octagon avoidance, and exclude chart 7-caps using the root. | `forces_317_of_asymmetric_315` proves the complete conditional transfer. It still needs an actual proof of `AsymmetricBound 315`. |

If all those steps hold, the proposed arithmetic is: the two chart parts have
at most `192 + 123 = 315` points; reinserting one projective root gives at most
316 points in an octagon-avoiding set; hence 317 points force an octagon. The
extra two units are **one root and one strict forcing threshold**, not two
geometric endpoints. This would be a finite octagon result, not a reduction of
HMPT's asymptotic coefficient. No priority or currently-best-bound claim is made.

The completed `root_cap_polygon` proves that a **7-cap in the chart** produces
an actual convex octagon with the retained root, including orientation reversal
and radial ordering. It is uniform for cap sizes at least three.
`exists_cap_free_chart` combines this with the existing HMPT projective lemmas
and Suk coordinate normalization, retaining explicit witnesses for the maps.
The original point set needs only general position, not distinct x-coordinates.

The precise remaining target is now `Partition.ResidualBound 123`: every
ordered real configuration with no 6-cap, no convex octagon and no junction
consisting of an incoming 6-cup and outgoing 5-cap has at most 123 points.
The completed partition handles configurations containing 7-cups and proves
all of these residual restrictions. The separately checked
`OmissionBalanced.forces_317_of_residual_123` composes it with the 192-point
bound and the projective transfer.

The remaining geometry must encode these actual residual configurations in the
154-state catalog, derive each restricted-domain cycle row, and prove the 23
block capacities using a Baek-style 22-point bound. The three-chain exclusion
needed by the partition is finished. Arithmetic-certificate checking alone
cannot establish the residual row and block implications. A putative
317-point counterexample is now proved to yield at least 124 residual chart
points satisfying the exact required restrictions, but those points have not
yet been excluded.

The comparison source is Michael Schroeder's
[version-1 archive, 19 September 2026](https://doi.org/10.5281/zenodo.22842891).
The current balanced adaptation includes `ES8ActualRanks`, `ES8BalancedStates`,
`ES8BalancedCatalog`, and the state/sign prerequisites; see the exact attribution
in [THIRD_PARTY.md](THIRD_PARTY.md). The projective/root argument from
`ES8ProjectiveTransfer` and `ES8Final` has now been adapted using this project's
existing geometry, as have `ES8MinimumSlope`, `ES8SlopePartition`, `ES8ThreeChain`
and `ES8PartitionComplete`. The residual geometry and block argument remain;
relevant source modules include `ES8ResidualRanks`, `ES8ResidualStates`,
`ES8ResidualCycleGeometry` and `ES8BlockGeometry`.

**Rough size:** the previous read-only import scan of the archive's `formal/sources`
finds 44 local modules (4,018 physical lines) reachable from `ES8Final`, before
external `ES8.*`, `ErdosTuzaValtr.*` and Mathlib imports. This is a size indicator,
not a count of all required work: generated tables can occupy very few long
lines, and API or trust changes can expand a port substantially. The archive
contains 208 Lean files overall and targets Lean 4.32.0-rc1; this project pins
4.24.0.

The balanced work added about 1,100 maintained Lean lines, plus generated row
proofs. The completed projective transfer adds 203 maintained Lean lines; the
partition and its supporting geometry add another 1,169 across eight modules.
These remove concrete portions of the earlier estimate, but do not measure the
hard residual/block obligations. A low-confidence
remaining planning range is still **several thousand to low tens of thousands
of handwritten Lean lines across dozens of modules, plus generated certificate
data**. For one experienced Lean/geometric-combinatorics contributor, think
**weeks to a few months**, conditional on the source reduction being valid and
portable. This is a low-confidence engineering estimate, not a completion date.
A flaw in a necessary residual row or block argument could require new mathematics
and make that range inapplicable. The residual and block geometry is the largest
unresolved proof obligation. The partition and projective/root transfer are
finished; completing arithmetic alone would still not finish the result.
