# ES(8) ≤ 317: remaining work

**Status, 2026-10-09: ES(8) ≤ 317 is not proved; the balanced geometric subcase is complete.**
The finished Suk and HMPT real-point theorems do not depend on this project.
The actual-point state encoding and geometric cycle soundness are now proved;
see [the balanced geometry record](OMISSION_GEOMETRY.md).

Two complete exact integer certificates exclude the stronger budgets in the
literal balanced and residual omission systems, giving occupancy bounds 192
and 123. Two independent programs replayed them. Lean now checks the complete
balanced tree, all 2,685 balanced row encodings and their geometric necessity,
and the actual-point balanced bound 192. The residual tree remains incomplete.
See the [balanced geometric proof artifact](../experiments/omission-balanced-geometry-2026-10-09/README.md).

| Remaining component | What would be required | Present uncertainty |
| --- | --- | --- |
| Complete arithmetic certificates | Finish the 145,474-leaf residual tree, compose every branch, and audit its final root. The 9,862-leaf balanced tree and its finite occupancy corollary are done. | The balanced 898-part build succeeded. The first 330 residual parts (13,827 leaves) are checked. The other 3,081 parts and root remain. The most recent 20-part block took about 15 minutes on this Mac; a simple extrapolation suggests roughly 39 hours for the remaining parts, but part sizes vary and that is not a benchmark or completion promise. |
| Real points → states | **Done for the balanced subcase:** attained ranks, Ferrers profiles, catalog coverage, exact indexing, and the injective actual-point owner map are proved in `ErdosSzekeres/Omission/`. | The residual state restrictions and their relation to a partition of an arbitrary point set remain separate obligations. |
| Geometric necessity of every row | **Done for all 2,685 balanced rows**, including support and demand alignment with the arithmetic catalog. Still needed: residual restricted-domain cycle constraints and all 23 block constraints using the relevant Baek-style geometric bound. | The residual geometric proof and its enumerations have not been ported under this project's trust rules. Balanced row checks do not discharge residual rows. |
| Partition and projective transfer | Prove the minimum-slope balanced/residual decomposition and its avoidance hypotheses. Normalize and order the root-deleted chart; prove that a chart 7-cap plus the deleted root gives an octagon. Apply the two population bounds, pull the polygon back, and account for the root. | Generic positive-chart injectivity, general-position preservation and polygon pullback already exist in `HMPT/Projective.lean`, using the same projective formula as the source. Their composition with this partition and its cup/cap conventions has not been proved. |

If all those steps hold, the proposed arithmetic is: the two chart parts have
at most `192 + 123 = 315` points; reinserting one projective root gives at most
316 points in an octagon-avoiding set; hence 317 points force an octagon. The
extra two units are **one root and one strict forcing threshold**, not two
geometric endpoints. This would be a finite octagon result, not a reduction of
HMPT's asymptotic coefficient. No priority or currently-best-bound claim is made.

More specifically, `HMPT.projectFrom` sends a point right of the root to its
ray slope and negative reciprocal horizontal distance. Its determinant formula
is already proved, as are `generalPosition_projectFrom` and
`hasConvexNGon_of_projectFrom`. The latter already pulls an eight-point convex
polygon from a positive-denominator chart back to the original real set.
`Suk.exists_horizontal_image` supplies an existing coordinate normalization.
These are reusable checked tools, not a completed ES(8) transfer.

The missing root-specific argument must show that a **7-cap in the chart**
produces an actual convex octagon with the retained root, with the correct
orientation reversal and radial ordering. Separately, the minimum-slope
partition must produce a balanced part to which the new theorem applies and
a residual part satisfying the residual no-junction/rank restrictions. That
includes a three-chain exclusion and the 23 block capacities, which use a
Baek-style 22-point bound. No amount of arithmetic-certificate checking alone
establishes these implications.

The comparison source is Michael Schroeder's
[version-1 archive, 19 September 2026](https://doi.org/10.5281/zenodo.22842891).
The current balanced adaptation includes `ES8ActualRanks`, `ES8BalancedStates`,
`ES8BalancedCatalog`, and the state/sign prerequisites; see the exact attribution
in [THIRD_PARTY.md](THIRD_PARTY.md). The residual geometry, block argument,
partition and projective transfer are not ported. Relevant remaining source
modules include `ES8ResidualCycleGeometry`, `ES8BlockGeometry`,
`ES8PartitionComplete`, `ES8ProjectiveTransfer` and `ES8Final`.

**Rough size:** the previous read-only import scan of the archive's `formal/sources`
finds 44 local modules (4,018 physical lines) reachable from `ES8Final`, before
external `ES8.*`, `ErdosTuzaValtr.*` and Mathlib imports. This is a size indicator,
not a count of all required work: generated tables can occupy very few long
lines, and API or trust changes can expand a port substantially. The archive
contains 208 Lean files overall and targets Lean 4.32.0-rc1; this project pins
4.24.0.

The balanced work added about 1,100 maintained Lean lines, plus generated row
proofs. It removes a concrete portion of the earlier estimate, but does not
measure the hard residual/block and projective obligations. A low-confidence
remaining planning range is still **several thousand to low tens of thousands
of handwritten Lean lines across dozens of modules, plus generated certificate
data**. For one experienced Lean/geometric-combinatorics contributor, think
**weeks to a few months**, conditional on the source reduction being valid and
portable. This is a low-confidence engineering estimate, not a completion date.
A flaw in a necessary row or transfer argument could require new mathematics
and make that range inapplicable. The residual and partition-specific geometry
is the largest unresolved proof obligation; some general projective machinery
is already available. Finishing arithmetic alone would not finish the result.
