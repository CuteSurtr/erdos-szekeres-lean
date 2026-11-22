import Combined.Residual
import BalancedBudgetsZZsN

/-!
# combined (22 Nov 2026, part 1): ES(8) ≤ 302 with every Lean-checked piece plugged in

`OmissionBalancedZZsN.composition_302_n54` (ES303N20261120/BalancedBudgetsZZsN.lean, comp-audit olean) with
`Combined.residual_bound_118`, whose `N66Bound 55` comes from `N66Bound 54` (`n66Bound_mono`).
-/

namespace Combined

/-- `N66Bound` is monotone in the bound. -/
theorem n66Bound_mono {a b : ℕ} (hab : a ≤ b) (h : OmissionZRow.N66Bound a) : OmissionZRow.N66Bound b := by
  intro n c noCap noCup noOct
  exact Nat.le_trans (h n c noCap noCup noOct) hab

/-- **ES(8) ≤ 302**, Lean-checked modulo the budget-69 tree statement `ExcludesHoleBudgetZZsN 16 69`,
`N66Bound 54`, the row-text verdicts of the four blocks and the slices s35_19, s35_20. -/
theorem es302 (tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69) (n54 : OmissionZRow.N66Bound 54)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 302 8 :=
  OmissionBalancedZZsN.composition_302_n54 tree69 n54
    (residual_bound_118 (n66Bound_mono (by norm_num) n54) hP hQ hU hA s35_19 s35_20)

end Combined

/-- info: 'Combined.n66Bound_mono' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.n66Bound_mono
/-- info: 'Combined.es302' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es302

set_option format.width 10000
#eval IO.println "=== CHECK"
#check Combined.n66Bound_mono
#check Combined.es302
#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"
