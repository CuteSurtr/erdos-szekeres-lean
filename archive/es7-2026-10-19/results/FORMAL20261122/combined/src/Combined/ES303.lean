import Combined.Residual
import BalancedBudgetsZZs

/-!
# combined (22 Nov 2026, part 1): ES(8) ≤ 303 with every Lean-checked piece plugged in

`OmissionBalancedZZsF.composition_303_zzsf` (ES303N20261120/BalancedBudgetsZZs.lean, comp-audit olean) with
`Combined.residual_bound_118`. The budget-67 tree (FV304) is not used: 303 needs the budget-68 tree instead.
-/

namespace Combined

/-- **ES(8) ≤ 303**, Lean-checked modulo the budget-68 tree statement `ExcludesHoleBudgetZZsF 68`, `N66Bound 55`,
the row-text verdicts of the four blocks and the slices s35_19, s35_20. -/
theorem es303 (tree68 : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68) (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 303 8 :=
  OmissionBalancedZZsF.composition_303_zzsf tree68 n66 (residual_bound_118 n66 hP hQ hU hA s35_19 s35_20)

end Combined

/-- info: 'Combined.es303' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es303

set_option format.width 10000
#eval IO.println "=== CHECK"
#check Combined.es303
#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"
