import E302ZZ.Root
import CompactChecker.BridgeZZs16
import BalancedBudgetsZZsN
open CompactChecker ErdosSzekeres ErdosSzekeres.Omission
namespace E302ZZ.Final
/-- FV302: the budget-69 tree with the Z-row and Z*-row at 16, checked in Lean by the compact checker
(32,618 contexts joined by the Root at the zero branch of state 0). -/
theorem excludes_69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69 := BridgeZZs16.zzsn16_of_root E302ZZ.root
/-- ES(8) <= 302 from N66 <= 54 and the residual bound 118 alone (the tree hypothesis is discharged in Lean). -/
theorem forces_302_of_n54_res (n66 : OmissionZRow.N66Bound 54) (hR : Partition.ResidualBound 118) :
    ForcesConvexNGon 302 8 :=
  OmissionBalancedZZsN.composition_302_n54 excludes_69 n66 hR
#print axioms excludes_69
#print axioms forces_302_of_n54_res
end E302ZZ.Final
