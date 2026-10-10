import Witness
import ErdosSzekeres.Omission.CoupledVariants
import ErdosSzekeres.Omission.CoupledSecondVariants
import ErdosSzekeres.Omission.CoupledThirdVariants
import ErdosSzekeres.Omission.CoupledFourthVariants
import ErdosSzekeres.Omission.CoupledFifthVariants
import ErdosSzekeres.Omission.CoupledNineVariant
import ErdosSzekeres.Omission.CoupledNineStructuralVariants

namespace OmissionResidual32Case4
open ErdosSzekeres.Omission
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

theorem all_first_variants : ∀ r : Fin 42,
    1 ≤ (CoupledVariants.support r ∩ missing).card := by decide +kernel

theorem all_second_variants : ∀ r : Fin 35,
    1 ≤ (CoupledSecondVariants.support r ∩ missing).card := by decide +kernel

theorem all_third_variants : ∀ r : Fin 3,
    1 ≤ (CoupledThirdVariants.support r ∩ missing).card := by decide +kernel

theorem all_fourth_variants : ∀ r : Fin 24,
    1 ≤ (CoupledFourthVariants.support r ∩ missing).card := by decide +kernel

theorem all_fifth_variants : ∀ r : Fin 28,
    1 ≤ (CoupledFifthVariants.support r ∩ missing).card := by decide +kernel

/-- The three later nine-state rows omitted from the frozen 2469-row catalog
also hold for this exact witness. Their hole counts are four, three and three. -/
theorem later_nine_rows :
    (CoupledNineVariant.support ∩ missing).card = 4 ∧
    (StructuralNine111.support ∩ missing).card = 3 ∧
    (StructuralNineShifted111.support ∩ missing).card = 3 := by decide +kernel

#print axioms all_first_variants
#print axioms all_second_variants
#print axioms all_third_variants
#print axioms all_fourth_variants
#print axioms all_fifth_variants
#print axioms later_nine_rows
end OmissionResidual32Case4
