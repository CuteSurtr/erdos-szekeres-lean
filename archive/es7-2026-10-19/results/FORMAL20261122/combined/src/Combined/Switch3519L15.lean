import Combined.N66L15
import Combined.ES304L15
import RS.Final3519

/-!
# combined part 2: the s35_19 switch for the level-15 forms. NOT COMPILED YET.

Compile only after res-slices-fv has accepted `RS.s35_19` (its README §5.1 acceptance and §9 finish recipe), with the
recipe "s35_19 switch (part 2 forms)" in this directory's README. `RS.s35_19` is pre-registered (res-slices-fv
§5.1) as `theorem s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19`.
Each theorem below is the part-2 form of this directory with `s35_19 := RS.s35_19`.
-/

namespace Combined

theorem residual_bound_118_l15_s3519 (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118 :=
  residual_bound_118_l15 cubes certs hP hQ hU hA RS.s35_19 s35_20

theorem es304_l15_s3519 (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  es304_l15 cubes certs hP hQ hU hA RS.s35_19 s35_20

theorem es303_l15_s3519 (tree68 : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68)
    (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 303 8 :=
  es303_l15 tree68 cubes certs hP hQ hU hA RS.s35_19 s35_20

theorem es302_l15_s3519 (tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69)
    (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 302 8 :=
  es302_l15 tree69 cubes certs hP hQ hU hA RS.s35_19 s35_20

end Combined

/-- info: 'Combined.residual_bound_118_l15_s3519' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.residual_bound_118_l15_s3519
/-- info: 'Combined.es304_l15_s3519' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es304_l15_s3519
/-- info: 'Combined.es303_l15_s3519' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es303_l15_s3519
/-- info: 'Combined.es302_l15_s3519' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms Combined.es302_l15_s3519

set_option format.width 10000
#eval IO.println "=== CHECK"
#check Combined.residual_bound_118_l15_s3519
#check Combined.es304_l15_s3519
#check Combined.es303_l15_s3519
#check Combined.es302_l15_s3519

-- Mechanical statement check (fails the compile otherwise): hypothesis count, and no binder mentions `N66Bound`.
open Lean Meta in
#eval show MetaM Unit from do
  for (n, k) in [(``Combined.residual_bound_118_l15_s3519, 7), (``Combined.es304_l15_s3519, 7),
                 (``Combined.es303_l15_s3519, 8), (``Combined.es302_l15_s3519, 8)] do
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
