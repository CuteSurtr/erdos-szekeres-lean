"""gen_bind.py (b69-prep): writes lean/BindN54.lean from zrow/zrow.json and zrow/zstar.json (the literal lists come from
the JSON files, not from the Lean sources). An #eval of all 3,131 Lean rows was tried and dropped: it did not
finish in 10 min; which loop was slow was not determined (bisect.log has only partial timings). Run: python3 -I -B lean/gen_bind.py"""
import json
ZR = '/home/jay/research/data/bal186-20261119/zrow/'
z = json.load(open(ZR + 'zrow.json'))[0]['support']; zs = json.load(open(ZR + 'zstar.json'))['zstar']
assert len(z) == len(zs) == 70
L = ', '.join
src = f"""import BalancedBudgetsZZsN
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
        (16 ≤ ∑ i ∈ _root_.OmissionZRow.Z, holes i) ∧ (16 ≤ ∑ i ∈ _root_.OmissionZStarRow.Zs, holes i) ∧
        (∑ i, holes i) ≤ 69 := Iff.rfl

/-- Lean's Z is exactly the support in zrow.json. -/
theorem b69prep_Z : ∀ i : Fin 252, i ∈ _root_.OmissionZRow.Z ↔ i.val ∈ ([{L(map(str, z))}] : List ℕ) :=
  _root_.OmissionZRow.Z_eq

/-- Lean's Z* is exactly the support in zstar.json. -/
theorem b69prep_Zs : ∀ i : Fin 252, i ∈ _root_.OmissionZStarRow.Zs ↔ i.val ∈ ([{L(map(str, zs))}] : List ℕ) :=
  _root_.OmissionZStarRow.Zs_eq

#check @OmissionBalancedZZsN.composition_302_n54
#print axioms b69prep_instance
#print axioms b69prep_Z
#print axioms b69prep_Zs
#print axioms OmissionBalancedZZsN.composition_302_n54

"""
open('/home/jay/research/data/bal186-20261119/b69prep/lean/BindN54.lean', 'w').write(src)
