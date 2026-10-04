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
