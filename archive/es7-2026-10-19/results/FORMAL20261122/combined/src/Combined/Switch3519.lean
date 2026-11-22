import Combined.ES304
import Combined.ES303
import Combined.ES302
import RS.Final3519

/-!
# combined: the s35_19 switch. NOT COMPILED YET.

Compile only after res-slices-fv has accepted `RS.s35_19` (its README §5.1 acceptance and §9 finish recipe), with the
recipe "s35_19 switch" in this directory's README (relink with tag 3519, compile, re-run the audit).
`RS.s35_19` is pre-registered (res-slices-fv §5.1) as
`theorem s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19`.
Each theorem below is the hypothesis form of this directory with `s35_19 := RS.s35_19`.
-/

namespace Combined

theorem residual_bound_118_s3519 (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118 :=
  residual_bound_118 n66 hP hQ hU hA RS.s35_19 s35_20

theorem es304_s3519 (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  es304 n66 hP hQ hU hA RS.s35_19 s35_20

theorem es303_s3519 (tree68 : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68) (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 303 8 :=
  es303 tree68 n66 hP hQ hU hA RS.s35_19 s35_20

theorem es302_s3519 (tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69) (n54 : OmissionZRow.N66Bound 54)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 302 8 :=
  es302 tree69 n54 hP hQ hU hA RS.s35_19 s35_20

end Combined

/-- info: 'Combined.residual_bound_118_s3519' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.residual_bound_118_s3519
/-- info: 'Combined.es304_s3519' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es304_s3519
/-- info: 'Combined.es303_s3519' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es303_s3519
/-- info: 'Combined.es302_s3519' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es302_s3519

set_option format.width 10000
#eval IO.println "=== CHECK"
#check Combined.residual_bound_118_s3519
#check Combined.es304_s3519
#check Combined.es303_s3519
#check Combined.es302_s3519
#eval IO.println "=== MODULES"
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"
#eval IO.println "=== END"
