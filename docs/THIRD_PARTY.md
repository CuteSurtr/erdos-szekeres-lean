# Third-party Lean source provenance

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
No ETV extremal theorem or enumeration certificate is imported.

## Finite octagon search inputs

The omission-row experiments use Michael Schroeder's version-1 archive,
[*Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*,
19 September 2026](https://doi.org/10.5281/zenodo.22842891).
Its data and prose are distributed under CC BY 4.0, its original code under
MIT, and its Baek port under Apache-2.0. The complete archive remains an ignored
local inspection dependency. The balanced geometry adaptations listed below
are now maintained in this repository.

The source catalogue hashes are recorded in the experiment manifests. Our
prefix enumeration and stronger-budget tree searches use those catalogues
and, for tree refinement, extend the published branch trees with newly found
integer certificates. This is an adaptation of the data, not an endorsement
by the author. The arithmetic checker and `OmissionCertificates.lean` were
implemented independently. Their mathematical weighted-capacity argument is
the one used by the source's omission certificates. See `OMISSION.md` for the
precise boundary between reproduced data, newly proved lemmas, and unproved
geometric transfer.

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
