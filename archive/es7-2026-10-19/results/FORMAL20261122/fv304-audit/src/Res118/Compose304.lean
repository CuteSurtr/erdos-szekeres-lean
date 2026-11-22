/-
res118-lean (22 November 2026): ES(8) ≤ 304 from the balanced budget-67 tree, N66 ≤ 55, the six residual slice
trees and the four blocks of unit rows, in Lean. `OmissionBalancedZ.composition_304_z` (ES305N20261119/
BalancedBudgetsZ.lean, compiled here from a byte-identical copy, sha256 3e0651a0…) with `ResidualBound 118`
supplied by `Res118.residual_bound_118_of_slices`.
-/
import BalancedBudgetsZ
import Res118.Final

open ErdosSzekeres

namespace Res118

/-- **ES(8) ≤ 304, Lean-checked modulo**: the budget-67 balanced tree (`ExcludesHoleBudgetZ 67`), N66 ≤ 55, the
validity of the four unit-row blocks and the six residual slice exclusions. -/
theorem forces_304_of_slices
    (trees : OmissionBalancedZ.ExcludesHoleBudgetZ 67)
    (n66 : OmissionZRow.N66Bound 55)
    (vP : BlockValid rowsP) (vQ : BlockValid rowsQ) (vU : BlockValid rowsU) (vA : BlockValid rowsA)
    (s33_18 : ResSliceExcludes [] 33 18)
    (s34_18 : ResSliceExcludes (rowsP ++ rowsQ) 34 18)
    (s34_19 : ResSliceExcludes rowsP 34 19)
    (s35_18 : ResSliceExcludes (rowsP ++ rowsQ) 35 18)
    (s35_19 : ResSliceExcludes (rowsP ++ rowsQ ++ rowsU) 35 19)
    (s35_20 : ResSliceExcludes (rowsP ++ rowsQ ++ rowsA) 35 20) :
    ForcesConvexNGon 304 8 :=
  OmissionBalancedZ.composition_304_z trees n66
    (residual_bound_118_of_slices n66 vP vQ vU vA s33_18 s34_18 s34_19 s35_18 s35_19 s35_20)

end Res118

#print axioms Res118.forces_304_of_slices
