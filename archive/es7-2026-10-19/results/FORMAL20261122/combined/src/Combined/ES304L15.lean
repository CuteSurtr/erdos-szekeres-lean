import Combined.ES304
import N66R15Geo.Final

/-!
# combined part 2 (22-23 Nov 2026): ES(8) ≤ 304 with N66 from level 15

`N66R15.n66_bound_55` (n66-l15-rows; reviewed in its `review/VERIFY_n66-l15-rows.md`) fills the `N66Bound 55` slot
of part 1's `Combined.es304` (FV304's `E304Z.Final.forces_304_of_n66_res`: the budget-67 tree is the Lean theorem
`E304Z.Final.excludes_67`).

Remaining hypotheses, and nothing else: the cake_lpr verdict props `N66R15Enc.CubesUnsat105R` (105 level-15 cube
verdicts), `N66R15Geo.RowCertsUnsat` (629 row-certificate verdicts: 628 full CNFs plus the trimmed sub-CNF of
template 208) and `RowGeo.RowsTextUnsat rowsP/Q/U/A` (2,025 row-text verdicts), all under trust items E1-E6; and the
slices s35_19 and s35_20 (not yet Lean-checked).
-/

namespace Combined

/-- **ES(8) ≤ 304**, Lean-checked modulo the N66 level-15 verdicts, the row-text verdicts of the four blocks and the
slices s35_19, s35_20. -/
theorem es304_l15 (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  es304 (N66R15.n66_bound_55 cubes certs) hP hQ hU hA s35_19 s35_20

end Combined

/-- info: 'Combined.es304_l15' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es304_l15

set_option format.width 10000
#eval IO.println "=== CHECK"
#check Combined.es304_l15
#check E304Z.Final.excludes_67

-- Mechanical statement check (fails the compile otherwise): hypothesis count, and no binder mentions `N66Bound`.
open Lean Meta in
#eval show MetaM Unit from do
  for (n, k) in [(``Combined.es304_l15, 8)] do
    let ci ← getConstInfo n
    forallTelescope ci.type fun xs body => do
      unless xs.size == k do throwError "{n}: {xs.size} hypotheses, expected {k}"
      for x in xs do
        if (← inferType x).getUsedConstants.contains ``OmissionZRow.N66Bound then
          throwError "{n}: a hypothesis mentions OmissionZRow.N66Bound"
      IO.println s!"STMT {n}: {xs.size} hypotheses, none mentions N66Bound; conclusion {← ppExpr body}"

#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"
