# ES(8) ≤ 317: remaining work

**Status, 2026-10-09: not proved. Certificate work has resumed.**
The finished Suk and HMPT real-point theorems do not depend on this project.
The geometric work estimated below has not been started as part of this resume.

Two complete exact integer certificates exclude the stronger budgets in the
literal balanced and residual omission systems, giving occupancy bounds 192
and 123. Two independent programs replayed them. Lean now checks the complete
balanced tree, all 2,685 balanced row encodings, and the explicit occupancy
bound 192. The residual tree remains incomplete. See the
[balanced proof artifact](../experiments/omission-balanced-lean-2026-10-09/README.md).

| Remaining component | What would be required | Present uncertainty |
| --- | --- | --- |
| Complete arithmetic certificates | Finish the 145,474-leaf residual tree, compose every branch, and audit its final root. The 9,862-leaf balanced tree and its finite occupancy corollary are done. | The balanced 898-part build succeeded. The residual 3,411-part build stopped partway; failed blocks pass with sequential checking, but total remaining runtime is not yet measured. |
| Real points → states | Define attained ending-path ranks and Ferrers profiles for arbitrary normalized real configurations; prove the catalog covers them and that the owner map is injective. | This exact state encoding has not been connected to this repository's geometry. Source ordering, boundary cases and index conventions require proof. |
| Geometric necessity of every row | Prove that each balanced cycle constraint follows from octagon avoidance. On the residual side, also prove the restricted-domain cycle constraints and the 23 block constraints using the relevant Baek-style geometric bound. | Arithmetic UNSAT alone does not establish any of these implications. The source proof and its finite enumerations have not been ported or independently checked under this project's trust rules. |
| Partition and projective transfer | Prove the balanced/residual decomposition, the normalization hypotheses, general-position preservation, convex-polygon pullback and reinsertion of the distinguished root. Then connect the result to `ForcesConvexNGon 317 8`. | Existing HMPT projective lemmas may help, but their applicability to this particular decomposition has not been established. Exact bookkeeping matters. |

If all those steps hold, the proposed arithmetic is: the two chart parts have
at most `192 + 123 = 315` points; reinserting one projective root gives at most
316 points in an octagon-avoiding set; hence 317 points force an octagon. The
extra two units are **one root and one strict forcing threshold**, not two
geometric endpoints. This would be a finite octagon result, not a reduction of
HMPT's asymptotic coefficient. No priority or currently-best-bound claim is made.

The comparison source is Michael Schroeder's
[version-1 archive, 19 September 2026](https://doi.org/10.5281/zenodo.22842891).
Relevant source modules include `ES8ActualRanks`, `ES8BalancedStates`,
`ES8BalancedCatalog`, `ES8CycleValidation`, `ES8BalancedGeometry`,
`ES8ResidualCycleGeometry`, `ES8BlockGeometry`, `ES8PartitionComplete`,
`ES8ProjectiveTransfer` and `ES8Final`. None has been imported as a proof here.

**Rough size:** a read-only import scan of the archive's `formal/sources`
finds 44 local modules (4,018 physical lines) reachable from `ES8Final`, before
external `ES8.*`, `ErdosTuzaValtr.*` and Mathlib imports. This is a size indicator,
not a count of all required work: generated tables can occupy very few long
lines, and API or trust changes can expand a port substantially. The archive
contains 208 Lean files overall and targets Lean 4.32.0-rc1; this project pins
4.24.0.

A reasonable planning range is **several thousand to low tens of thousands of
handwritten Lean lines across dozens of modules, plus generated certificate
data**. For one experienced Lean/geometric-combinatorics contributor, think
**weeks to a few months**, conditional on the source reduction being valid and
portable. This is a low-confidence engineering estimate, not a completion date.
A flaw in a necessary row or transfer argument could require new mathematics
and make that range inapplicable. The geometric transfer is the largest
unresolved proof obligation; finishing arithmetic alone would not finish the
result.
