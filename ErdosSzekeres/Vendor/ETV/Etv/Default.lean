/-
Adapted from Jineon Baek's erdos-tuza-valtr proof code, distributed in
Michael Schroeder's version-1 archive, DOI 10.5281/zenodo.22842891.
Licensed under Apache-2.0; see docs/APACHE-2.0.txt and docs/THIRD_PARTY.md.
Changes: local imports and compatibility with Lean/Mathlib v4.24.0.
-/
import ErdosSzekeres.Vendor.ETV.Etv.Defs
import ErdosSzekeres.Vendor.ETV.Etv.Label
import ErdosSzekeres.Vendor.ETV.Etv.Mirror
import ErdosSzekeres.Vendor.ETV.Etv.AlphaBeta

set_option linter.unusedVariables false
set_option linter.unusedSimpArgs false
set_option linter.unnecessarySeqFocus false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
