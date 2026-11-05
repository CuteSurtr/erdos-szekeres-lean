import CompactChecker.Bridge311Bal
import CompactChecker.Bridge311Res
import ErdosSzekeres.Omission.PopulationBounds

/-!
# The bridges conclude exactly the definitions that the ES(8) ≤ 311 assembly consumes

`OmissionBalanced.ExcludesHoleBudget` (BalancedBudgets.lean) and
`OmissionResidual32Bridge2650.Excludes2650Zero` (Residual32Bridge2650/Rows.lean) live in
modules that import the geometric row proofs, which are not built on this machine. Below are
verbatim copies of the two definitions, under primed names, in the same namespaces and with
the same `open` lines as their source files, so that their bodies elaborate exactly as there.
The two theorems check that the bridges' conclusions are these propositions.
-/

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission

namespace OmissionBalanced

/-- Verbatim copy of `ExcludesHoleBudget` (BalancedBudgets.lean, lines 9–11). -/
def ExcludesHoleBudget' (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
    (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget

end OmissionBalanced

namespace OmissionResidual32Bridge2650

/-- Verbatim copy of `Excludes2650Zero` (Residual32Bridge2650/Rows.lean, lines 98–100). -/
def Excludes2650Zero' (budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧ holes 0 = 0 ∧
    (∀ r, demand2650 r ≤ ∑ i ∈ support2650 r, holes i) ∧ (∑ i, holes i) ≤ budget

end OmissionResidual32Bridge2650

namespace CompactChecker.Bridge311Defs

theorem balanced_bridge_is_ExcludesHoleBudget {budget : ℕ}
    (h : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcat62 3131 252 budget (pmask (zerosF 252) []) holes) :
    OmissionBalanced.ExcludesHoleBudget' budget :=
  Bridge311Bal.balanced_of_root h

theorem residual_bridge_is_Excludes2650Zero {budget : ℕ}
    (h : ¬ ∃ holes : Fin 154 → ℕ,
      FFeas fcat2650 2650 154 budget (pmask (zerosF 154) [(0, 2)]) holes) :
    OmissionResidual32Bridge2650.Excludes2650Zero' budget :=
  Bridge311Res.residual_of_root h

/-- The checks are syntactic up to unfolding the primed definitions. -/
example : OmissionBalanced.ExcludesHoleBudget' 63 =
    ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
      (∑ i, holes i) ≤ 63 := rfl

#print axioms balanced_bridge_is_ExcludesHoleBudget
#print axioms residual_bridge_is_Excludes2650Zero

end CompactChecker.Bridge311Defs
