-- combined part 3 (pre-registered 25 Nov 2026 ~16:40 KST, before E302ZZ.Final and RS.Final3520 exist; PART3.md):
-- the budget-69 tree (FV302, `E302ZZ.Final.excludes_69`) and the slice s35_20 (res-slices-fv, `RS.s35_20`)
-- discharged in Lean. NOT COMPILED YET: compile only after both are accepted (PART3.md §1).
import Combined.Switch3519L15
import E302ZZ.Final
import RS.Final3520

open ErdosSzekeres ErdosSzekeres.Omission

namespace Combined

/-- ES(8) ≤ 302, Lean-checked modulo exactly the cake_lpr verdict propositions H-N66C (105 level-15 cube leaves),
H-N66R (629 row certificates) and H-ROWS (2,025 row verdicts); trust items E1-E6 as in REMAINS.md. -/
theorem es302_verdicts (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA) :
    ErdosSzekeres.ForcesConvexNGon 302 8 :=
  es302_l15_s3519 E302ZZ.Final.excludes_69 cubes certs hP hQ hU hA RS.s35_20

/-- ES(8) ≤ 304 with s35_20 discharged (the same verdict hypotheses; the 304 tree is FV304's). -/
theorem es304_verdicts (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  es304_l15_s3519 cubes certs hP hQ hU hA RS.s35_20

/-- `ResidualBound 118` with s35_20 discharged (the same verdict hypotheses). -/
theorem residual_bound_118_verdicts (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118 :=
  residual_bound_118_l15_s3519 cubes certs hP hQ hU hA RS.s35_20

end Combined

/-! Statement checks (FV302 acceptance item 1 and review finding of 25 Nov): each discharged theorem and the new
end theorem have exactly the pre-registered types; the elaborator rejects the module otherwise. -/
example : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69 := E302ZZ.Final.excludes_69
example : OmissionZRow.N66Bound 54 → Partition.ResidualBound 118 → ForcesConvexNGon 302 8 :=
  E302ZZ.Final.forces_302_of_n54_res
example : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20 := RS.s35_20
example : N66R15Enc.CubesUnsat105R → N66R15Geo.RowCertsUnsat → RowGeo.RowsTextUnsat Res118.rowsP →
    RowGeo.RowsTextUnsat Res118.rowsQ → RowGeo.RowsTextUnsat Res118.rowsU → RowGeo.RowsTextUnsat Res118.rowsA →
    ForcesConvexNGon 302 8 := Combined.es302_verdicts

/-- info: 'Combined.es302_verdicts' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es302_verdicts
/-- info: 'Combined.es304_verdicts' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es304_verdicts
/-- info: 'Combined.residual_bound_118_verdicts' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.residual_bound_118_verdicts

set_option format.width 10000
#eval IO.println "=== CHECK"
#check Combined.es302_verdicts
#check Combined.es304_verdicts
#check Combined.residual_bound_118_verdicts
