import BalancedBudgets
import Residual32Bridge2650.Rows
import E311.Final

/-!
NOT COMPILED (6 November 2026). The last step of the compact ES(8) ≤ 311 recheck, stated
exactly. `E311.Final` is written and compiled by `drive_es311.py` after every chunk and both
Roots; it proves `E311.balanced_excludes_63` and `E311.residual_excludes_32`, the bodies of
`OmissionBalanced.ExcludesHoleBudget 63` and `OmissionResidual32Bridge2650.Excludes2650Zero 32`.
This file feeds them to the same geometric bounds that `Final311/Final.lean` uses. Its imports
need the geometric chain of the 311 record (the balanced row geometry behind `BalancedBudgets`,
and `Residual32Bridge2650.Rows` with the rank-core modules, some of which peaked at 12–20 GB
when they were last compiled), so it cannot run under this machine's 12 GB per-process cap.

Open, as of the 6 November review: compile this file in ONE consistent build. Lean does not check an
imported .olean against the .olean files it was compiled against, and the bridges
(`CompactChecker.Bridge311Bal`, `CompactChecker.Bridge311Res`, imported through `E311.Final`) were
compiled against copies of `BalancedProof.Catalog`, `BalancedCoverCutsV2` and
`Residual32Bridge2650.Catalog` built separately in `build/ext/`, while `BalancedBudgets` and
`Residual32Bridge2650.Rows` would load the geometric chain's copies. Required:
  1. one toolchain (Lean 4.24.0, Mathlib v4.24.0) and one build directory in which every module of
     the import closure, the three catalogs included, is compiled once from its pinned source;
  2. the bridges, `E311.Final` and this file compiled against that directory, with `build/ext/` NOT on
     LEAN_PATH (no module provided by two LEAN_PATH roots; `drive_es311.py` refuses such a path) --
     or, if the chain's three catalog .olean files have the sha256 of the `build/ext/` ones (rebuilds
     here were byte-identical for 7 of 7 modules that fit the hard cap), the existing bridge .oleans;
  3. a per-process memory cap above 12 GB (`RankCoreFour` 19.7 GB; `BalancedCoverCutsV2` was
     OOM-killed under a hard 12 GB cap with 12.4 GB of anonymous memory);
  4. record `#print axioms forces_convex_octagon_311`; optionally replay the final environment with an
     independent checker (lean4checker).
-/

open ErdosSzekeres

namespace ErdosSzekeres.Omission.Compact311

theorem balanced_population_188 : Partition.BalancedBound 188 :=
  OmissionBalanced.balanced_bound_of_hole_budget (budget := 63) E311.balanced_excludes_63

theorem residual_population_121 : Partition.ResidualBound 121 :=
  OmissionResidual32Bridge2650.residual_bound_121_of_excludes E311.residual_excludes_32

theorem forces_convex_octagon_311 : ForcesConvexNGon 311 8 :=
  Partition.forces_of_population_bounds (by omega) balanced_population_188 residual_population_121

#print axioms forces_convex_octagon_311

end ErdosSzekeres.Omission.Compact311
