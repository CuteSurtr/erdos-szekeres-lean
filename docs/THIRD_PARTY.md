# Third-party Lean source provenance

The project's default license and all exceptions are specified in
[LICENSING.md](LICENSING.md). Existing upstream terms below are retained;
the root Apache-2.0 license does not relicense these contributions.

The following files in `ErdosSzekeres/Vendor/` are adapted from
[sneed-and-feed/lean-theorems-1](https://github.com/sneed-and-feed/lean-theorems-1),
revision `4fce2c92ad4321064a06afdc86d0272bc625ce14`, under CC0-1.0. The full license
is included as `docs/CC0-1.0.txt`. Original module names under `Formalization/`:

- `DilworthTheorem.lean`
- `ErdosSzekeresConvex/Orientation.lean`
- `ErdosSzekeresConvex/Sorting.lean`
- `ErdosSzekeresConvex/CupCap.lean`
- `ErdosSzekeresConvex/ConvexPolygon.lean`

These checked prerequisites are used in Suk's argument; they do not constitute
a formalization of Suk's theorem. The upstream version targets a later Mathlib. Local changes
redirect imports and adapt APIs to the pinned Mathlib v4.24.0. Their inclusion
must be accompanied by successful local compilation, axiom audits and bridges
between their geometric definitions and this project's definitions.

Other inspection clones under `.cache/` are not vendored dependencies. In
particular, no EmptyHexagonLean source or placeholder axiom has been imported.

## Combinatorial cups-caps prerequisite

`ErdosSzekeres/Vendor/ETV/` adapts the list, configuration and cups-caps
modules from [Jineon Baek's erdos-tuza-valtr](https://github.com/jcpaik/erdos-tuza-valtr),
revision `a5ad53efefb36f8654b9227ce4dba2bf04a7ec3f`, under Apache-2.0.
The full license is in `docs/APACHE-2.0.txt`.

Changes redirect imports, replace deprecated chain names, repair proof scripts
for Lean/Mathlib v4.24.0, remove unneeded mirror lemmas and imports, and suppress
style lint warnings in the adapted files. Kernel checking is unchanged. The
upstream cap-cup theorem gives consecutive-triple paths for arbitrary colorings.
`Suk/TransitiveColoring.lean` supplies a separate proved path-to-clique bridge
under transitivity, then derives the clique upper bound needed in Suk's proof.
The original cups-caps prerequisite did not import the ETV extremal theorem.
The later residual block port below adds the relevant Baek theorem, with a
separate proved transfer from its list predicate to real convex polygons.

## Finite octagon search inputs

The omission-row experiments use Michael Schroeder's version-1 archive,
[*Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*,
19 September 2026](https://doi.org/10.5281/zenodo.22842891).
Its data and prose are distributed under CC BY 4.0, its original code under
MIT, and its Baek port under Apache-2.0. The complete archive remains an ignored
local inspection dependency. The balanced geometry adaptations listed below
are now maintained in this repository.

The archive's README describes its DOI as reserved for an unpublished Zenodo
draft. This attribution identifies the supplied, pinned archive and does not
assert that the identifier resolves publicly. The original data/prose license
notice is retained in [SCHROEDER-CC-BY-4.0.md](SCHROEDER-CC-BY-4.0.md).

The source catalogue hashes are recorded in the experiment manifests. Our
prefix enumeration and stronger-budget tree searches use those catalogues
and, for tree refinement, extend the published branch trees with newly found
integer certificates. This is an adaptation of the data, not an endorsement
by the author. The arithmetic checker and `OmissionCertificates.lean` were
implemented independently. Their mathematical weighted-capacity argument is
the one used by the source's omission certificates. See `OMISSION.md` for the
precise boundary between reproduced data and newly proved lemmas. The
completed geometric transfer is documented in `OMISSION_RESIDUAL.md`.

The generated `experiments/omission-chunked-2026-10-05/Catalog.lean` preserves
that archive's balanced row indices, supports and demands and adds packed
integer encodings. `Leaf.lean` uses one newly strengthened certificate leaf.
The adapted catalog data remains under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/);
the directory README provides source credit, change descriptions and reproduction
commands. These generated Lean proof inputs are committed; compiled `.olean`
files and the upstream inspection checkout are not. No source Lean module from
the archive has been imported into the finished Suk or HMPT dependency graph.

`experiments/omission-balanced-lean-2026-10-09/row-source.json.gz` preserves the
upstream balanced JSON byte for byte. Its `sources.tar.gz` contains newly
generated Lean arithmetic proofs and the same adapted catalog data under
CC BY 4.0. The directory README credits the author and explains the changes.
The source bundle contains no compiled objects; all build products remain
ignored. `scripts/omission_lean_export.py` and `check_omission_lean.py` implement
the local arithmetic export and checking workflow. Those arithmetic proof
generators do not import upstream Lean code.

## Balanced omission geometry — 9 October 2026

The following modules in `ErdosSzekeres/Omission/` adapt proof code from the
same version-1 archive. The complete MIT license, including Michael Schroeder's
2026 copyright notice, is in [SCHROEDER-MIT.txt](SCHROEDER-MIT.txt).

| Local module | Archive module under `formal/sources/` |
| --- | --- |
| `StateInterface.lean` | `ES8/Admissible.lean` |
| `ActualRanks.lean` | `ES8ActualRanks.lean` |
| `BalancedStates.lean` | `ES8BalancedStates.lean` |
| `Ferrers.lean` | `ES8Ferrers.lean` |
| `BalancedCatalog.lean` | `ES8BalancedCatalog.lean` |
| `Domains.lean` | `ES8Domains.lean` |
| `CycleSigns.lean` | `ES8CycleSigns.lean` |

Changes redirect namespaces and imports, adapt proofs to Lean/Mathlib 4.24,
use this project's real-plane type and determinant, and use kernel reduction
for the finite checks. `BalancedCatalogData.lean` preserves the source's exact
252-profile order as a literal list; the catalog data is under CC BY 4.0.
`scripts/omission_geometry_export.py` extracts the ordered cycle data from
`ES8CycleData.lean`, preserving all 2,685 orders. The emitted cycle lists remain
CC BY 4.0 adaptations, with their source hashes in the export manifest.

`Realization.lean` connects attained paths to this project's all-triples cups,
caps and general-position predicate. `BoundingBoxes.lean` proves correctness
of boxes computed from each finite state difference, without importing the
source's 63,504-entry box table. `CycleGeometry.lean` connects checked triples
to the existing `HasConvexNGon` definition and proves the missing-state bound.
These connections and the generated row-to-arithmetic composition were added
here, using the archive's balanced-state/cycle strategy. They are not claimed
as an independently discovered geometric method. The first-cycle example
preserves cycle zero from the source data.

The new modules are included in the default library and audit; the large
generated row and arithmetic certificates are checked separately. Neither
`Suk.theorem2016` nor `HMPT.theorem2020` depends on these adaptations. No
endorsement by the original author is implied.

## Projective/root transfer — 9 October 2026

`ErdosSzekeres/Omission/ProjectiveTransfer.lean` adapts the root/chart argument
from the same version-1 archive's `ES8ProjectiveTransfer.lean` and `ES8Final.lean`,
under MIT, copyright (c) 2026 Michael Schroeder. The complete notice is retained
in [SCHROEDER-MIT.txt](SCHROEDER-MIT.txt) and attribution appears in the source.

This version uses the existing `HMPT.projectFrom` lemmas, Suk's coordinate
normalization and this project's finite-set polygon predicate. It generalizes
the root-cap lemma to every cap size at least three, exposes the actual maps in
`IsRootDeletionChart`, and leaves the asymmetric population bound as an explicit
theorem parameter. The standalone `BalancedProjective.lean` adds the cardinality
composition with the completed balanced bound. The [proof map](OMISSION_PROJECTIVE.md)
distinguishes these checked statements from the still-unproved global bound.

## Minimum-slope partition — 9 October 2026

Eight further modules under `ErdosSzekeres/Omission/` adapt the same archive's
MIT proof code, copyright (c) 2026 Michael Schroeder. Every source header credits
the archive; the complete notice remains in [SCHROEDER-MIT.txt](SCHROEDER-MIT.txt).

| Local module | Source module / adaptation |
| --- | --- |
| `PlanarChains.lean` | `ES8PlanarChains.lean`: real-plane four-point identities and bounded chain closure. |
| `ListGeometry.lean` | List/sign portion of `ES8BaekGeometry.lean`; adds both directions of the bridge to this project's all-triples cup/cap predicates. It does not import the source's Baek capacity theorem. |
| `MinimumSlope.lean` | `ES8MinimumSlope.lean`: attained minima and strict geometric consequences. |
| `Subsets.lean` | Reindexing and junction portion of `ES8Subset.lean`; replaces source-specific population imports with local image, avoidance and junction transport. |
| `CupExtension.lean` | Chord identity and arc strategy from `ES8BoundaryGeometry.lean`; proves a direct all-triples one-point extension using this project's convex-position theorem, without porting the full boundary module. |
| `SlopePartition.lean` | `ES8SlopePartition.lean`: initial split, junction removal and residual restrictions. The source's final population-bound call is replaced by an explicit local composition. |
| `ThreeChain.lean` | `ES8ThreeChain.lean`: adapts the case argument to actual `HasConvexNGon`, using the new direct cup/three-cap lemma. |
| `Partition.lean` | `ES8PartitionComplete.lean`: complete seven-cup exclusion; adds disjointness, exact subset cardinality, an actual-configuration partition theorem and conditional population composition. |

All coordinates, namespaces and imports are adapted to the local Lean/Mathlib
4.24 library. The residual population estimate is an explicit parameter, not
an axiom. The standalone `BalancedPartition.lean` supplies the already checked
balanced bound and adds the necessary 124-point residual condition for a
putative 317-point counterexample. The source method is credited; these ports
are not claimed as independently discovered geometric arguments.

## Residual geometry and Baek block bound — 9 October 2026

The following further modules under `ErdosSzekeres/Omission/` adapt the same
version-1 archive's MIT code, copyright (c) 2026 Michael Schroeder. Source
headers and [SCHROEDER-MIT.txt](SCHROEDER-MIT.txt) preserve the notice.

| Local module | Source / adaptation |
| --- | --- |
| `ResidualRanks.lean` | `ES8ResidualRanks.lean`; adds the bridge from the proved actual no-junction condition to rank witnesses. |
| `ResidualStates.lean` | `ES8ResidualStates.lean`; kernel enumeration of the 154 restricted profiles. |
| `ResidualCatalog.lean` | `ES8ResidualCatalog.lean`; exact local owner indexing. |
| `ResidualDomains.lean` | `ES8ResidualDomains.lean`; actual directed label differences. |
| `BlockCompression.lean` | `ES8BlockCompression.lean`; finite pairs/growth checks and the two-valued rank argument, omitting the source-specific mask checker. |
| `BlockGeometry.lean` | `ES8BlockGeometry.lean`; actual capacity and a new finite-set row interface. |
| `BoundaryGeometry.lean` | `ES8BoundaryGeometry.lean` plus supporting affine-function lemmas from `ES8Geometry.lean`; uses `Fin 2 → ℝ` and proves a general finite polygon conclusion. |
| `Baek.lean` | `ES8Baek.lean`; specialization of the separately ported Apache-2.0 theorem. |
| `BaekGeometry.lean` | Remaining boundary-to-polygon portion of `ES8BaekGeometry.lean`, reusing the already maintained list/sign bridge. |

`ResidualCatalogData.lean` preserves the exact source profile order, including
its trailing zero. Catalog, cycle and block data are CC BY 4.0. The new residual
exporters retain the source's 1,164 cycle orders and 23 compression records and
replace evaluation-based validations with kernel checks. The artifact retains
source hashes, notices, a byte-preserved residual JSON and generated proof sources.
`ResidualRealization.lean`, `ResidualBoxes.lean` and `ResidualCycleGeometry.lean`
adapt the local balanced connections to the restricted residual ranks; these
use the credited source method, not a claimed independent geometric discovery.

The following new modules under `ErdosSzekeres/Vendor/ETV/` port Jineon Baek's
proof as distributed in the archive, under Apache-2.0:
`Lib/List/Mirror`, `Config/Mirror`, `Config/Default`, the five `Etv/*` modules,
`Main/Defs`, `Main/InductionStep`, `Main/Main`, and the five `Main/Lemmas/*`
modules. Existing vendored files are preserved. Changes redirect imports,
restore mirror lemmas in a separate module, and adapt sorted-list APIs to
Lean/Mathlib 4.24. Full license: [APACHE-2.0.txt](APACHE-2.0.txt).
The general Baek theorem, its 23-point specialization and the real geometric
interpretation all build and pass the axiom audit. None enters the dependency
closure of the finished Suk or HMPT main theorem.

## Additional residual rows — 10 October 2026

`Omission/AdditionalResidualRows.lean` and
`experiments/omission-additional-rows-2026-10-10*` retain the same source state
numbering and use the credited cycle/compression methods. The 20 cycle rows
and one block row were discovered locally outside the pinned original row
list and rechecked by the Lean kernel. Their derived state-index data retains
CC BY 4.0 attribution to Schroeder's version-1 catalog. The new independence
proofs use the exact catalog already preserved in the residual geometry
artifact. No upstream search code is added with these files, and no priority
or endorsement claim is made. The artifact README gives reproduction and
distinguishes abstract witnesses from realizable configurations.

## Compressed complete certificates — 10 October 2026

`experiments/omission-cover-certificates-2026-10-10/` retains the pinned original
row data inside two augmented JSON catalogs and generated Lean source-only
archives. These adapted data remain CC BY 4.0 with the author and DOI recorded
in the artifact README and manifest. The new rounded cuts, stronger-budget
trees, proof generators and exact checking records document the local changes.
`experiments/omission-global-assembly-2026-10-10/` preserves the renamed balanced
geometric sources under the original adaptation's MIT attribution and the
original fallback residual tree as attributed CC BY 4.0 data. No compiled
objects or upstream inspection checkout are committed. The complete 317-point
proof uses these finite inputs and the separately attributed geometric ports;
it does not change the dependency provenance of Suk or HMPT.

## Coupled residual obstructions — 10 October 2026

The `Omission/Coupled*` modules and their experiment bundles retain
Schroeder's state numbering and the preceding attributed geometric interfaces.
Derived state data retain CC BY 4.0 attribution to the pinned version-1 archive.
The local shared order/rank/orientation encodings, finite refutations,
actual-owner necessity proofs and template extensions are project additions;
they are not statements attributed to Suk or HMPT, and no literature priority
or endorsement claim is made.

Five kernel-checked thirteen-state cores are preserved in the
[first](../experiments/omission-coupled-core-2026-10-10/README.md),
[second](../experiments/omission-coupled-next-2026-10-10/README.md),
[third](../experiments/omission-coupled-demand-two-2026-10-10/README.md),
[fourth](../experiments/omission-coupled-fourth-2026-10-10/README.md) and
[fifth](../experiments/omission-coupled-fifth-2026-10-10/README.md) bundles.
Their source snapshots, literal CNF/LRAT certificates, independently replayed
deletion models and axiom audits document the local changes. The first two
cores yield families of 42 and 35 supports, whose union has 57 distinct rows.
The separate [union bundle](../experiments/omission-coupled-union-2026-10-10/README.md)
contains the checked nine-independent/48-redundant classification against its
frozen earlier row system. Its Boolean witnesses do not assert realizability.

The third and fourth bundles also preserve three selected third-core variants
and 24 fourth-core variants, including the fourth core itself. The third bundle
contains the fourteen-state demand-two theorem, assembled from its new core,
two credited original cycle rows and an earlier template row. These additions
reuse the attributed residual-state method and this project's proved geometric
bridges. They neither replace the earlier provenance nor establish a new
asymptotic coefficient; the [paper map](PAPER_MAP.md#supplementary-project-results-coupled-residual-obstructions)
lists their precise theorem names and scope.

[CoupledLrat.lean](../ErdosSzekeres/Omission/CoupledLrat.lean) invokes Mathlib's
Apache-2.0 `Mathlib.Tactic.Sat.FromLRAT` proof-term generator; it does not vendor
that implementation or introduce a native-evaluation axiom. CaDiCaL and Z3 were
used only for untrusted discovery and are not committed here. The literal
derivations are independently replayed and checked by Lean's kernel. Compiled
objects and inspection caches remain ignored.

The fifth bundle additionally preserves 28 checked template variants. The
[eleven-state](../experiments/omission-coupled-eleven-2026-10-10/README.md) and
[nine-state](../experiments/omission-coupled-nine-2026-10-10/README.md) bundles
use the same attributed catalog and semantic interfaces, with separately
checked literal refutations and complete deletion witnesses. Their discovery
model witnesses are abstract Boolean assignments, not realized point sets.

The [finite HMPT refinement](../experiments/hmpt-binomial-refinement-2026-10-10/README.md)
retains a binomial subset count in the existing two-scale argument. It relies
on the already attributed HMPT geometry and Mathlib counting facts; it does not
import a new third-party implementation or assert literature priority.

The [endpoint budget analysis](../experiments/hmpt-endpoint-barrier-2026-10-10/README.md)
uses the same HMPT coefficient and this repository's explicit entropy budget.
It introduces no external code and does not attribute an impossibility claim
to the published paper.

The [uniform factorial saving](../experiments/hmpt-factorial-saving-2026-10-10/README.md)
and [visible-edge insertion lemma](../experiments/visible-edge-insertion-2026-10-10/README.md)
are new project proofs using existing attributed prerequisites and Mathlib.
The [second nine-state support](../experiments/omission-coupled-nine-variant-2026-10-10/README.md)
reuses the original nine-state refutation with newly checked state-dependent
premises. Its literal state data retain the same catalog attribution and data
license. These additions introduce no new third-party code or priority claim.

The [residual32 witness continuation](../experiments/omission-residual32-case4-2026-10-10/README.md),
[sixth core](../experiments/omission-residual32-witness-coupled-2026-10-10/README.md),
[generic sixth template](../experiments/omission-residual32-sixth-variants-2026-10-10/README.md),
and [128 new Fourth-template rows](../experiments/omission-residual32-fourth-global-variants-2026-10-10/README.md)
retain this same catalog and geometric-interface attribution. Their search
scripts adapt earlier local coupled models and exporters, with source hashes
recorded in each bundle. The new literal CNF/LRAT derivation, Lean necessity
proofs and finite witnesses are project additions. The independent RUP checker
adapts `scripts/check_omission_coupled_core.py`; no external solver source or
binary is committed. The case-2/case-7 partial trees and failed repair searches
are research diagnostics, not new bounds attributed to any paper.
