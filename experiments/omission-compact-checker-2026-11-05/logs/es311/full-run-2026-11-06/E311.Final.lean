import E311B.Root
import E311R.Root
import CompactChecker.Bridge311Bal
import CompactChecker.Bridge311Res

/-!
ES(8) ≤ 311, compact recheck: the two arithmetic facts that `Final311/Final.lean` consumes.

* `balanced_excludes_63` is the body of `OmissionBalanced.ExcludesHoleBudget 63`
  (BalancedBudgets.lean), which Final311 obtains as
  `OmissionBalancedCover63.exclusion_transfer OmissionBalancedCover63.excludes_budget`.
* `residual_excludes_32` is the body of `OmissionResidual32Bridge2650.Excludes2650Zero 32`
  (Residual32Bridge2650/Rows.lean), which Final311 uses as `residual_excludes_2650_zero`.
-/

open scoped BigOperators

namespace E311

theorem balanced_excludes_63 :
    ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
      (∑ i, holes i) ≤ 63 :=
  CompactChecker.Bridge311Bal.balanced_of_root E311B.root

theorem residual_excludes_32 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧ holes 0 = 0 ∧
      (∀ r, OmissionResidual32Bridge2650.demand2650 r ≤
        ∑ i ∈ OmissionResidual32Bridge2650.support2650 r, holes i) ∧
      (∑ i, holes i) ≤ 32 :=
  CompactChecker.Bridge311Res.residual_of_root E311R.root

#print axioms balanced_excludes_63
#print axioms residual_excludes_32

end E311
