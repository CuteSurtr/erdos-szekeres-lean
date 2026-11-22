import Combined.N66L15
import Combined.ES304L15

/-!
# Independent review of `combined` part 2 (slot rv5, 23 Nov 2026). THE ONE compile; no olean output.

B1 axioms of the three cheap worker theorems (es304_l15 in B12); B2 the reviewer's own re-elaboration by another route
(N66 through `N66R15Geo.n66_bound_54_of_rows` + `rowsValid_R15`, not `N66R15.n66_bound_54/55`; ResidualBound 118 through
the four blocks and the RS slices into `Res118.residual_bound_118_of_slices`, not `Combined.residual_bound_118`; 304
through `composition_304_z` + `excludes_67`; 303/302 through `composition_303_zzsf` / `composition_302_n54`, not the
part-1 `Combined.*`); B3 type equality worker vs own; B4 binder audit; B5 kinds and declaring modules; B6 stored
statements and values; B7 definitions and hand-unfolded explicit statements (accepted by defeq); B8 verdict-shaped
composite (text forms of the two N66 props); B10 module list with Lean's own olean resolution;
B11 axioms of the reviewer's theorems and pieces; B12 the two E304Z walks; B9 interpreter dumps of `R1_15` and
`leaves105` at the very end (the only step with a crash risk).
-/

set_option maxHeartbeats 0
set_option format.width 100000

#eval IO.println "=== B1 AXIOMS (worker part-2 theorems, from the worker's oleans; es304_l15 in B12)"
#print axioms Combined.residual_bound_118_l15
#print axioms Combined.es303_l15
#print axioms Combined.es302_l15

namespace RV5P2

/-- N66Bound 54 by the generic theorem at `R1_15` (not `N66R15.n66_bound_54`). -/
theorem n54 (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat) : OmissionZRow.N66Bound 54 :=
  N66R15Geo.n66_bound_54_of_rows (R := N66R15Enc.R1_15) cubes (N66R15Geo.rowsValid_R15 certs)

/-- N66Bound 55 from 54 by `Nat.le_trans` (not `N66R15.n66_bound_55`). -/
theorem n55 (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat) : OmissionZRow.N66Bound 55 :=
  fun n c h1 h2 h3 => Nat.le_trans (n54 cubes certs n c h1 h2 h3) (by decide)

theorem rb118 (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118 :=
  Res118.residual_bound_118_of_slices (n55 cubes certs)
    (RowGeo.blockValid_P (RowGeo.rowsUnsat_of_texts hP))
    (RowGeo.blockValid_Q (RowGeo.rowsUnsat_of_texts hQ))
    (RowGeo.blockValid_U (RowGeo.rowsUnsat_of_texts hU))
    (RowGeo.blockValid_A (RowGeo.rowsUnsat_of_texts hA))
    RS.s33_18 RS.s34_18 RS.s34_19 RS.s35_18 t19 t20

theorem es304 (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  OmissionBalancedZ.composition_304_z E304Z.Final.excludes_67 (n55 cubes certs)
    (rb118 cubes certs hP hQ hU hA t19 t20)

theorem es303 (tree68 : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68)
    (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 303 8 :=
  OmissionBalancedZZsF.composition_303_zzsf tree68 (n55 cubes certs) (rb118 cubes certs hP hQ hU hA t19 t20)

theorem es302 (tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69)
    (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 302 8 :=
  OmissionBalancedZZsN.composition_302_n54 tree69 (n54 cubes certs) (rb118 cubes certs hP hQ hU hA t19 t20)

end RV5P2

open Lean Meta in
#eval show MetaM Unit from do
  IO.println "=== B3 TYPE EQUALITY (worker constant vs reviewer re-elaboration)"
  let pairs : List (Name × Name) := [(`Combined.residual_bound_118_l15, `RV5P2.rb118),
    (`Combined.es304_l15, `RV5P2.es304), (`Combined.es303_l15, `RV5P2.es303), (`Combined.es302_l15, `RV5P2.es302),
    (`N66R15.n66_bound_54, `RV5P2.n54), (`N66R15.n66_bound_55, `RV5P2.n55)]
  for (a, b) in pairs do
    try
      let ta := (← getConstInfo a).type
      let tb := (← getConstInfo b).type
      let de ← isDefEq ta tb
      IO.println s!"TYPEEQ {a} {b} alpha={ta == tb} defeq={de}"
    catch e =>
      IO.println s!"TYPEEQ {a} {b} ERROR {← e.toMessageData.toString}"

open Lean Meta in
#eval show MetaM Unit from do
  IO.println "=== B4 BINDERS (worker part-2 theorems)"
  let bad : List Name := [`OmissionZRow.N66Bound, `ErdosSzekeres.Omission.Partition.ResidualBound,
    `Res118.BlockValid, `RowGeo.RowsUnsat, `N66G15.RowsValid, `N66G15.RowValid, `OmissionBalancedZ.ExcludesHoleBudgetZ,
    `ErdosSzekeres.ForcesConvexNGon, `N66E15.CubesUnsat105, `N66E15.R0_15, `N66Enc.R0, `RowGeo.R0Parse]
  for n in [`Combined.residual_bound_118_l15, `Combined.es304_l15, `Combined.es303_l15, `Combined.es302_l15] do
    let ci ← getConstInfo n
    let kind := match ci with
      | .thmInfo _ => "theorem" | .axiomInfo _ => "AXIOM" | .defnInfo _ => "def" | .opaqueInfo _ => "opaque"
      | _ => "other"
    forallTelescope ci.type fun xs body => do
      IO.println s!"BINDERS {n} kind={kind} levelParams={ci.levelParams.length} count={xs.size} concl={← ppExpr body} conclHasFVar={body.hasFVar}"
      for x in xs do
        let d ← x.fvarId!.getDecl
        let bi := match d.binderInfo with
          | .default => "default" | .implicit => "implicit" | .strictImplicit => "strictImplicit"
          | .instImplicit => "instImplicit"
        let used := d.type.getUsedConstants
        let hit := bad.filter used.contains
        IO.println s!"  BINDER {n} {d.userName} info={bi} head={d.type.getAppFn.constName?} intermediate={hit} dep={d.type.hasFVar} type={← ppExpr d.type}"

open Lean in
#eval show CoreM Unit from do
  IO.println "=== B5 DECLARATIONS (kind, declaring module)"
  let env ← getEnv
  let names : List Name := [`ErdosSzekeres.ForcesConvexNGon, `ErdosSzekeres.HasConvexNGon,
    `ErdosSzekeres.GeneralPosition, `ErdosSzekeres.ConvexPosition, `ErdosSzekeres.Point,
    `ErdosSzekeres.Omission.Partition.ResidualBound, `OmissionZRow.N66Bound,
    `N66R15Enc.CubesUnsat105R, `N66R15Geo.RowCertsUnsat, `N66E15.leaves105, `N66E15.tree15, `N66E15.fullCnf,
    `N66E15.nvHeader, `N66R15Enc.R1_15, `N66R15Enc.R1nat15, `N66R15Enc.rowsAll, `N66R15Enc.templates,
    `N66R15Enc.cores, `N66R15Enc.certCnf, `N66R15Enc.certText, `N66R15Enc.subCnfChecked, `N66R15Enc.printClauses,
    `EncB.DimacsSatisfiable, `EncB.DimacsSat, `EncB.parseDimacs, `EncB.parseDimacsBytes, `EncB.render,
    `RowGeo.RowsTextUnsat, `RowEnc.rowText, `Res118.ResSliceExcludes, `Res118.rowsP, `Res118.rowsQ, `Res118.rowsU,
    `Res118.rowsA, `OmissionBalancedZZsF.ExcludesHoleBudgetZZsF, `OmissionBalancedZZsN.ExcludesHoleBudgetZZsN,
    `N66R15.n66_bound_54, `N66R15.n66_bound_55, `N66R15Geo.n66_bound_54_of_rows, `N66R15Geo.rowsValid_R15,
    `N66R15.cubesUnsat105R_of_texts, `N66R15.rowCertsUnsat_of_texts, `Combined.residual_bound_118, `Combined.es304,
    `Combined.es303, `Combined.es302, `Combined.n66Bound_mono, `Combined.residual_bound_118_l15, `Combined.es304_l15,
    `Combined.es303_l15, `Combined.es302_l15, `RS.s33_18, `RS.s34_18, `RS.s34_19, `RS.s35_18, `RS.s35_19, `RS.s35_20,
    `Combined.residual_bound_118_l15_s3519, `Combined.es304_l15_s3519, `Combined.residual_bound_118_s3519,
    `E304Z.Final.excludes_67, `OmissionBalancedZ.composition_304_z, `OmissionBalancedZZsF.composition_303_zzsf,
    `OmissionBalancedZZsN.composition_302_n54, `Res118.residual_bound_118_of_slices, `RowGeo.blockValid_P,
    `RowGeo.rowsUnsat_of_texts, `RowGeo.R0Parse, `N66Enc.R0, `RV5P2.es304]
  for n in names do
    let kind := match env.find? n with
      | some (ConstantInfo.thmInfo _) => "theorem"
      | some (ConstantInfo.defnInfo _) => "def"
      | some (ConstantInfo.axiomInfo _) => "AXIOM"
      | some (ConstantInfo.opaqueInfo _) => "opaque"
      | some (ConstantInfo.inductInfo _) => "inductive"
      | some (ConstantInfo.ctorInfo _) => "ctor"
      | some (ConstantInfo.recInfo _) => "rec"
      | some (ConstantInfo.quotInfo _) => "quot"
      | none => "MISSING"
    let mod := match env.getModuleIdxFor? n with
      | some i => ((env.header.moduleNames[i]?).map toString).getD "?"
      | none => "(this file)"
    IO.println s!"DECL {n} {kind} {mod}"

#eval IO.println "=== B6 STORED STATEMENTS AND VALUES"
set_option pp.fullNames true in
#print Combined.residual_bound_118_l15
set_option pp.fullNames true in
#print Combined.es304_l15
set_option pp.fullNames true in
#print Combined.es303_l15
set_option pp.fullNames true in
#print Combined.es302_l15
set_option pp.fullNames true in
#check @N66R15.n66_bound_54
set_option pp.fullNames true in
#check @N66R15.n66_bound_55
set_option pp.fullNames true in
#check @N66R15Geo.n66_bound_54_of_rows
set_option pp.fullNames true in
#check @N66R15Geo.rowsValid_R15
set_option pp.fullNames true in
#check @Combined.residual_bound_118
set_option pp.fullNames true in
#check @Combined.es304
set_option pp.fullNames true in
#check @Combined.es303
set_option pp.fullNames true in
#check @Combined.es302
set_option pp.fullNames true in
#check @Res118.residual_bound_118_of_slices
set_option pp.fullNames true in
#check @OmissionBalancedZ.composition_304_z
set_option pp.fullNames true in
#check @OmissionBalancedZZsF.composition_303_zzsf
set_option pp.fullNames true in
#check @OmissionBalancedZZsN.composition_302_n54
set_option pp.fullNames true in
#check @E304Z.Final.excludes_67

#eval IO.println "=== B7 DEFINITIONS"
set_option pp.fullNames true in
#print ErdosSzekeres.ForcesConvexNGon
set_option pp.fullNames true in
#print ErdosSzekeres.HasConvexNGon
set_option pp.fullNames true in
#print ErdosSzekeres.GeneralPosition
set_option pp.fullNames true in
#print ErdosSzekeres.ConvexPosition
set_option pp.fullNames true in
#print ErdosSzekeres.Omission.Partition.ResidualBound
set_option pp.fullNames true in
#print OmissionZRow.N66Bound
set_option pp.fullNames true in
#print N66R15Enc.CubesUnsat105R
set_option pp.fullNames true in
#print N66R15Geo.RowCertsUnsat
set_option pp.fullNames true in
#print N66E15.leaves105
set_option pp.fullNames true in
#print N66E15.fullCnf
set_option pp.fullNames true in
#print N66R15Enc.R1_15
set_option pp.fullNames true in
#print N66R15Enc.R1nat15
set_option pp.fullNames true in
#print N66R15Enc.certCnf
set_option pp.fullNames true in
#print RowGeo.RowsTextUnsat
set_option pp.fullNames true in
#print EncB.DimacsSatisfiable
set_option pp.fullNames true in
#print EncB.DimacsSat
set_option pp.fullNames true in
#print Res118.ResSliceExcludes
set_option pp.fullNames true in
#print OmissionBalancedZZsF.ExcludesHoleBudgetZZsF
set_option pp.fullNames true in
#print OmissionBalancedZZsN.ExcludesHoleBudgetZZsN

namespace RV5P2

/-- The reviewer's plain DIMACS unsatisfiability: no assignment satisfies every clause (literal l > 0 true iff
ν |l| = true, literal l < 0 true iff ν |l| = false). -/
def rvUnsat (F : List (List Int)) : Prop :=
  ¬ ∃ ν : ℕ → Bool, ∀ cl ∈ F, ∃ l ∈ cl, (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false)

/-- The reviewer's plain statement "every N points in the plane, no three on a line, contain the vertices of a
convex n-gon". -/
def rvForces (N n : ℕ) : Prop :=
  ∀ s : Finset (Fin 2 → ℝ),
    (∀ a ∈ s, ∀ b ∈ s, ∀ c ∈ s, a ≠ b → a ≠ c → b ≠ c → ¬ Collinear ℝ ({a, b, c} : Set (Fin 2 → ℝ))) →
    N ≤ s.card →
    ∃ t : Finset (Fin 2 → ℝ), t ⊆ s ∧ t.card = n ∧
      ConvexIndependent ℝ (fun p : (t : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ))

/-- Every row text, parsed strictly from its UTF-8 bytes, is unsatisfiable. -/
def rvTextsUnsat (rows : List (List ℕ)) : Prop :=
  ∀ s ∈ rows, ∀ nv F, EncB.parseDimacsBytes (RowEnc.rowText s).toUTF8.data.toList = some (nv, F) → rvUnsat F

theorem forces_iff (N n : ℕ) : rvForces N n ↔ ErdosSzekeres.ForcesConvexNGon N n := Iff.rfl

theorem es304_explicit
    (cubes : ∀ c ∈ N66E15.leaves105, rvUnsat (N66E15.fullCnf N66R15Enc.R1_15 c))
    (certs : (∀ t ∈ N66R15Enc.templates, rvUnsat (N66R15Enc.certCnf t)) ∧
      (∀ k ∈ N66R15Enc.cores, rvUnsat (N66R15Enc.certCnf k)))
    (hP : rvTextsUnsat Res118.rowsP) (hQ : rvTextsUnsat Res118.rowsQ)
    (hU : rvTextsUnsat Res118.rowsU) (hA : rvTextsUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    rvForces 304 8 :=
  Combined.es304_l15 cubes certs hP hQ hU hA t19 t20

theorem es303_explicit (tree68 : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68)
    (cubes : ∀ c ∈ N66E15.leaves105, rvUnsat (N66E15.fullCnf N66R15Enc.R1_15 c))
    (certs : (∀ t ∈ N66R15Enc.templates, rvUnsat (N66R15Enc.certCnf t)) ∧
      (∀ k ∈ N66R15Enc.cores, rvUnsat (N66R15Enc.certCnf k)))
    (hP : rvTextsUnsat Res118.rowsP) (hQ : rvTextsUnsat Res118.rowsQ)
    (hU : rvTextsUnsat Res118.rowsU) (hA : rvTextsUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    rvForces 303 8 :=
  Combined.es303_l15 tree68 cubes certs hP hQ hU hA t19 t20

theorem es302_explicit (tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69)
    (cubes : ∀ c ∈ N66E15.leaves105, rvUnsat (N66E15.fullCnf N66R15Enc.R1_15 c))
    (certs : (∀ t ∈ N66R15Enc.templates, rvUnsat (N66R15Enc.certCnf t)) ∧
      (∀ k ∈ N66R15Enc.cores, rvUnsat (N66R15Enc.certCnf k)))
    (hP : rvTextsUnsat Res118.rowsP) (hQ : rvTextsUnsat Res118.rowsQ)
    (hU : rvTextsUnsat Res118.rowsU) (hA : rvTextsUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    rvForces 302 8 :=
  Combined.es302_l15 tree69 cubes certs hP hQ hU hA t19 t20

theorem rb118_explicit
    (cubes : ∀ c ∈ N66E15.leaves105, rvUnsat (N66E15.fullCnf N66R15Enc.R1_15 c))
    (certs : (∀ t ∈ N66R15Enc.templates, rvUnsat (N66R15Enc.certCnf t)) ∧
      (∀ k ∈ N66R15Enc.cores, rvUnsat (N66R15Enc.certCnf k)))
    (hP : rvTextsUnsat Res118.rowsP) (hQ : rvTextsUnsat Res118.rowsQ)
    (hU : rvTextsUnsat Res118.rowsU) (hA : rvTextsUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118 :=
  Combined.residual_bound_118_l15 cubes certs hP hQ hU hA t19 t20

/-- ES(8) ≤ 304 with the two N66 props replaced by the verdict shapes E1-E3 deliver (printed trims per leaf;
printed certificate texts; T208 through a printed sub-list), through the reviewed bridges. -/
theorem es304_texts
    (hcub : ∀ c ∈ N66E15.leaves105, ∃ (ds : List N66R15Enc.Desc) (L : List (List Int)),
      N66R15Enc.printClauses c ds = some L ∧ N66R15Enc.litsBounded N66E15.nvHeader L = true ∧
      ∀ nv F, EncB.parseDimacs (EncB.render N66E15.nvHeader L) = some (nv, F) → ¬ EncB.DimacsSatisfiable F)
    (hT : ∀ t ∈ N66R15Enc.templates, t = N66R15Enc.tmpl208 ∨
      ∀ nv F, EncB.parseDimacs (N66R15Enc.certText t) = some (nv, F) → ¬ EncB.DimacsSatisfiable F)
    (h208 : ∃ (idx : List ℕ) (F : List (List Int)), N66R15Enc.subCnfChecked N66R15Enc.tmpl208 idx = some F ∧
      ∀ nv G, EncB.parseDimacs (EncB.render (N66R15Enc.nvOf N66R15Enc.tmpl208.n) F) = some (nv, G) →
        ¬ EncB.DimacsSatisfiable G)
    (hC : ∀ k ∈ N66R15Enc.cores, ∀ nv F, EncB.parseDimacs (N66R15Enc.certText k) = some (nv, F) →
      ¬ EncB.DimacsSatisfiable F)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  Combined.es304_l15 (N66R15.cubesUnsat105R_of_texts hcub) (N66R15.rowCertsUnsat_of_texts hT h208 hC)
    hP hQ hU hA t19 t20

end RV5P2

#eval IO.println "=== B8 EXPLICIT AND TEXT FORMS ELABORATED (axioms of the non-304 explicit forms in B11; es304_explicit/_texts not walked: their terms are Combined.es304_l15 applied, plus the two bridges printed in B11)"
set_option pp.fullNames true in
#check @RV5P2.es304_explicit
set_option pp.fullNames true in
#check @RV5P2.es304_texts

open Lean in
#eval show CoreM Unit from do
  IO.println "=== B10 MODULES (Lean's own resolution via findOLean)"
  let env ← getEnv
  IO.println s!"NMODULES {env.header.moduleNames.size}"
  for m in env.header.moduleNames do
    let p ← findOLean m
    IO.println s!"MOD {m} {p}"

#eval IO.println "=== B11 AXIOMS (reviewer theorems and pieces, no E304Z walk)"
#print axioms RV5P2.n54
#print axioms RV5P2.n55
#print axioms RV5P2.rb118
#print axioms RV5P2.es303
#print axioms RV5P2.es302
#print axioms RV5P2.rb118_explicit
#print axioms RV5P2.es303_explicit
#print axioms RV5P2.es302_explicit
#print axioms RV5P2.forces_iff
#print axioms N66R15.n66_bound_54
#print axioms N66R15.n66_bound_55
#print axioms N66R15Geo.n66_bound_54_of_rows
#print axioms N66R15Geo.rowsValid_R15
#print axioms N66R15.cubesUnsat105R_of_texts
#print axioms N66R15.rowCertsUnsat_of_texts
#print axioms Combined.residual_bound_118
#print axioms Combined.es303
#print axioms Combined.es302

#eval IO.println "=== B12 AXIOMS (E304Z walks)"
#print axioms Combined.es304_l15
#print axioms RV5P2.es304

#eval show IO Unit from do
  IO.println "=== B9 INTERPRETER (olean data on this LEAN_PATH)"
  IO.FS.writeFile "/home/jay/research/data/formalize-20261122/combined/review/part2/data/rv5p2_R1_15.txt"
    (String.join (N66R15Enc.R1_15.map fun T => " ".intercalate (T.map fun s => toString s.val) ++ "\n"))
  IO.FS.writeFile "/home/jay/research/data/formalize-20261122/combined/review/part2/data/rv5p2_leaves105.txt"
    (String.join (N66E15.leaves105.map fun c =>
      " ".intercalate (c.map fun z => s!"{z.1.val}:{if z.2 then 1 else 0}") ++ "\n"))
  IO.println s!"LEN rowsAll={N66R15Enc.rowsAll.length} R1_15={N66R15Enc.R1_15.length} leaves105={N66E15.leaves105.length} templates={N66R15Enc.templates.length} cores={N66R15Enc.cores.length} nvHeader={N66E15.nvHeader}"
  IO.println s!"LEN rowsP={Res118.rowsP.length} rowsQ={Res118.rowsQ.length} rowsU={Res118.rowsU.length} rowsA={Res118.rowsA.length}"

#eval IO.println "=== END"
