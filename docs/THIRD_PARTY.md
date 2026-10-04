# Third-party Lean source provenance

Files in `ErdosSzekeres/Vendor/` are adapted from
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
Baek's Apache-2.0-licensed `jcpaik/erdos-tuza-valtr` is also being inspected as a
source for the transitive-coloring cups-caps theorem, which is stronger than a
theorem restricted to realized point sets.
