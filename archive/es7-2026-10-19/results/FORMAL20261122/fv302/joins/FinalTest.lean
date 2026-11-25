import CompactChecker.BridgeZZs16
import BalancedBudgetsZZsN
open CompactChecker ErdosSzekeres ErdosSzekeres.Omission
namespace E302ZZ.FinalTest
/-- FV302 pilot: the Root statement (zero branch of state 0) gives ES(8) <= 302 from N66 <= 54 and the residual
bound 118, through BridgeZZs16 and composition_302_n54 (the Final module will use E302ZZ.root for hroot). -/
theorem forces_302_of_root
    (hroot : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(0, 2)]) holes)
    (n66 : OmissionZRow.N66Bound 54) (hR : Partition.ResidualBound 118) : ForcesConvexNGon 302 8 :=
  OmissionBalancedZZsN.composition_302_n54 (BridgeZZs16.zzsn16_of_root hroot) n66 hR
#print axioms forces_302_of_root
end E302ZZ.FinalTest
