import BalancedBudgetsZZsN
open scoped BigOperators
set_option maxRecDepth 10000

/-! b69-prep (22 Nov 2026): the Lean side of the rows binding of the budget-69 tree. -/

/-- The instance used by `composition_302_n54` unfolds to: the 2,685 OmissionBalanced rows, the 446 cover cuts, the
Z-row and the Z*-row both at demand 16, at most 69 holes, holes 0 = holes 1 = 0 (all names `_root_`-qualified). -/
theorem b69prep_instance :
    OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69 ↔
      ¬ ∃ holes : Fin 252 → ℕ, holes 0 = 0 ∧ holes 1 = 0 ∧ (∀ i, holes i ≤ 1) ∧
        (∀ q : Fin 2685, _root_.OmissionBalanced.demand q ≤ ∑ i ∈ _root_.OmissionBalanced.support q, holes i) ∧
        (∀ q : Fin 446, _root_.BalancedCoverCutsV2.demand q ≤ ∑ i ∈ _root_.BalancedCoverCutsV2.support q, holes i) ∧
        (15 ≤ ∑ i ∈ _root_.OmissionZRow.Z, holes i) ∧ (16 ≤ ∑ i ∈ _root_.OmissionZStarRow.Zs, holes i) ∧
        (∑ i, holes i) ≤ 69 := Iff.rfl

/-- Lean's Z is exactly the support in zrow.json. -/
theorem b69prep_Z : ∀ i : Fin 252, i ∈ _root_.OmissionZRow.Z ↔ i.val ∈ ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 29, 31, 32, 33, 34, 35, 36, 40, 42, 43, 44, 46, 47, 48, 49, 55, 57, 58, 60, 61, 62, 63, 72, 73, 75, 77, 78, 79, 80, 90, 93, 94, 96, 97, 108, 112, 114, 115, 116, 130, 133, 134, 151, 153, 170, 187] : List ℕ) :=
  _root_.OmissionZRow.Z_eq

/-- Lean's Z* is exactly the support in zstar.json. -/
theorem b69prep_Zs : ∀ i : Fin 252, i ∈ _root_.OmissionZStarRow.Zs ↔ i.val ∈ ([64, 81, 98, 100, 117, 118, 121, 135, 136, 137, 139, 143, 154, 155, 157, 158, 161, 171, 172, 173, 174, 176, 178, 179, 188, 189, 190, 191, 193, 194, 196, 202, 203, 204, 205, 207, 208, 209, 211, 215, 216, 217, 218, 219, 220, 222, 225, 226, 227, 228, 229, 230, 231, 234, 235, 236, 237, 238, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251] : List ℕ) :=
  _root_.OmissionZStarRow.Zs_eq

#check @OmissionBalancedZZsN.composition_302_n54
#print axioms b69prep_instance
#print axioms b69prep_Z
#print axioms b69prep_Zs
#print axioms OmissionBalancedZZsN.composition_302_n54

