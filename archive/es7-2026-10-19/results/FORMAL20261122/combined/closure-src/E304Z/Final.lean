import E304Z.Root
import CompactChecker.BridgeZ
import BalancedBudgetsZ
open CompactChecker ErdosSzekeres ErdosSzekeres.Omission
namespace E304Z.Final
/-- FV304: the budget-67 Z-row tree, checked in Lean by the compact checker (8,192 contexts joined by the Root). -/
theorem excludes_67 : OmissionBalancedZ.ExcludesHoleBudgetZ 67 := BridgeZ.balanced_z_of_root E304Z.root
/-- ES(8) <= 304 from N66 <= 55 and the residual bound 118 alone (the tree hypothesis is discharged in Lean). -/
theorem forces_304_of_n66_res (n66 : OmissionZRow.N66Bound 55) (hR : Partition.ResidualBound 118) :
    ForcesConvexNGon 304 8 :=
  OmissionBalancedZ.composition_304_z excludes_67 n66 hR
#print axioms excludes_67
#print axioms forces_304_of_n66_res
end E304Z.Final
