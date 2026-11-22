import Combined.ES304
import Combined.ES303
import Combined.ES302

/-!
# Independent review of `combined` part 1 (slot rv5, 22 Nov 2026). THE ONE compile; no olean output.

S1 axioms of the worker theorems (from the worker's oleans); S2 the reviewer's own statements, re-elaborated here
from the pieces by a different route (blocks via `blockValid_*`/`rowsUnsat_of_texts` into
`Res118.residual_bound_118_of_slices`; 304 via `composition_304_z` + `excludes_67`); S3 type equality worker vs
reviewer; S4 kinds and declaring modules; S5 stored statements; S6 definitions and unfolded restatements (`Iff.rfl`);
S7 axioms of the reviewer's theorems and the pieces; S8 module list with Lean's own olean resolution; S9 the four
row lists from the olean; S10 one interpreter `rowText` (last: the only step with a crash risk).
-/

open Lean Meta Elab Command

set_option maxHeartbeats 0
set_option format.width 100000

#eval IO.println "=== S1 AXIOMS (worker theorems)"
#print axioms Combined.residual_bound_118
#print axioms Combined.es304
#print axioms Combined.es303
#print axioms Combined.es302
#print axioms Combined.n66Bound_mono

namespace RV5

theorem rb118 (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118 :=
  Res118.residual_bound_118_of_slices n66
    (RowGeo.blockValid_P (RowGeo.rowsUnsat_of_texts hP))
    (RowGeo.blockValid_Q (RowGeo.rowsUnsat_of_texts hQ))
    (RowGeo.blockValid_U (RowGeo.rowsUnsat_of_texts hU))
    (RowGeo.blockValid_A (RowGeo.rowsUnsat_of_texts hA))
    RS.s33_18 RS.s34_18 RS.s34_19 RS.s35_18 t19 t20

theorem es304 (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 304 8 :=
  OmissionBalancedZ.composition_304_z E304Z.Final.excludes_67 n66 (rb118 n66 hP hQ hU hA t19 t20)

theorem es303 (tree : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68) (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 303 8 :=
  OmissionBalancedZZsF.composition_303_zzsf tree n66 (rb118 n66 hP hQ hU hA t19 t20)

theorem n66mono {a b : ℕ} (hab : a ≤ b) (h : OmissionZRow.N66Bound a) : OmissionZRow.N66Bound b := by
  intro n c h1 h2 h3
  exact Nat.le_trans (h n c h1 h2 h3) hab

theorem es302 (tree : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69) (n54 : OmissionZRow.N66Bound 54)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (t19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (t20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.ForcesConvexNGon 302 8 :=
  OmissionBalancedZZsN.composition_302_n54 tree n54
    (rb118 (n66mono (by decide) n54) hP hQ hU hA t19 t20)

/-- Non-vacuity aid: the row hypothesis says exactly "the Lean CNF of every row is unsatisfiable". -/
theorem text_iff (rows : List (List ℕ)) : RowGeo.RowsTextUnsat rows ↔ RowGeo.RowsUnsat rows := by
  constructor
  · intro h
    exact RowGeo.rowsUnsat_of_texts h
  · intro h s hs nv F hp
    rw [RowGeo.parseDimacsBytes_rowText] at hp
    first
      | (cases hp; exact h s hs)
      | (simp only [Option.some.injEq, Prod.mk.injEq] at hp; obtain ⟨-, rfl⟩ := hp; exact h s hs)

end RV5

#eval show MetaM Unit from do
  IO.println "=== S3 TYPE EQUALITY (worker constant vs reviewer re-elaboration)"
  let pairs : List (Name × Name) := [(`Combined.residual_bound_118, `RV5.rb118), (`Combined.es304, `RV5.es304),
    (`Combined.es303, `RV5.es303), (`Combined.es302, `RV5.es302), (`Combined.n66Bound_mono, `RV5.n66mono)]
  for (a, b) in pairs do
    let ta := (← getConstInfo a).type
    let tb := (← getConstInfo b).type
    let de ← isDefEq ta tb
    let concl ← forallTelescope ta fun xs body => do
      return s!"nhyp={xs.size} head={body.getAppFn.constName?} concl={← ppExpr body}"
    IO.println s!"TYPEEQ {a} {b} alpha={ta == tb} defeq={de} {concl}"

#eval show CoreM Unit from do
  IO.println "=== S4 DECLARATIONS (kind, declaring module)"
  let env ← getEnv
  let names : List Name := [`ErdosSzekeres.ForcesConvexNGon, `ErdosSzekeres.HasConvexNGon,
    `ErdosSzekeres.GeneralPosition, `ErdosSzekeres.ConvexPosition, `ErdosSzekeres.Point,
    `ErdosSzekeres.Omission.Configuration, `ErdosSzekeres.Omission.Partition.ResidualBound,
    `ErdosSzekeres.Omission.Partition.forces_of_population_bounds, `OmissionZRow.N66Bound,
    `RowGeo.RowsTextUnsat, `RowGeo.RowsUnsat, `RowEnc.rowText, `RowEnc.rowCnf, `RowEnc.rowNv,
    `EncB.parseDimacsBytes, `EncB.DimacsSatisfiable, `EncB.DimacsSat, `EncB.render,
    `Res118.ResSliceExcludes, `Res118.BlockValid, `Res118.ValidUnitRow, `Res118.rowsP, `Res118.rowsQ,
    `Res118.rowsU, `Res118.rowsA, `OmissionBalancedZ.ExcludesHoleBudgetZ, `OmissionBalancedZZsF.ExcludesHoleBudgetZZsF,
    `OmissionBalancedZZsN.ExcludesHoleBudgetZZsN, `RS.s33_18, `RS.s34_18, `RS.s34_19, `RS.s35_18, `RS.s35_19,
    `RS.s35_20, `E304Z.Final.excludes_67, `E304Z.Final.forces_304_of_n66_res, `OmissionBalancedZ.composition_304_z,
    `OmissionBalancedZZsF.composition_303_zzsf, `OmissionBalancedZZsN.composition_302_n54,
    `RowGeo.residual_bound_118_of_texts, `RowGeo.blockValid_P, `RowGeo.blockValid_Q, `RowGeo.blockValid_U,
    `RowGeo.blockValid_A, `RowGeo.rowsUnsat_of_texts, `RowGeo.parseDimacsBytes_rowText,
    `Res118.residual_bound_118_of_slices, `Combined.residual_bound_118, `Combined.es304, `Combined.es303,
    `Combined.es302, `Combined.n66Bound_mono, `Combined.residual_bound_118_s3519, `Combined.es304_s3519,
    `RV5.rb118, `RV5.es304]
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

#eval IO.println "=== S5 STORED STATEMENTS"
set_option pp.fullNames true in
#check Combined.residual_bound_118
set_option pp.fullNames true in
#check Combined.es304
set_option pp.fullNames true in
#check Combined.es303
set_option pp.fullNames true in
#check Combined.es302
set_option pp.fullNames true in
#check Combined.n66Bound_mono
set_option pp.fullNames true in
#check Res118.residual_bound_118_of_slices
set_option pp.fullNames true in
#check RowGeo.residual_bound_118_of_texts
set_option pp.fullNames true in
#check RS.s33_18
set_option pp.fullNames true in
#check RS.s34_18
set_option pp.fullNames true in
#check RS.s34_19
set_option pp.fullNames true in
#check RS.s35_18
set_option pp.fullNames true in
#check E304Z.Final.excludes_67
set_option pp.fullNames true in
#check E304Z.Final.forces_304_of_n66_res
set_option pp.fullNames true in
#check OmissionBalancedZ.composition_304_z
set_option pp.fullNames true in
#check OmissionBalancedZZsF.composition_303_zzsf
set_option pp.fullNames true in
#check OmissionBalancedZZsN.composition_302_n54
set_option pp.fullNames true in
#check RowGeo.parseDimacsBytes_rowText

#eval IO.println "=== S6 DEFINITIONS"
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
#print RowGeo.RowsTextUnsat
set_option pp.fullNames true in
#print RowGeo.RowsUnsat
set_option pp.fullNames true in
#print EncB.DimacsSatisfiable
set_option pp.fullNames true in
#print EncB.DimacsSat
set_option pp.fullNames true in
#print Res118.ResSliceExcludes
set_option pp.fullNames true in
#print Res118.BlockValid
set_option pp.fullNames true in
#print Res118.ValidUnitRow
set_option pp.fullNames true in
#print OmissionBalancedZZsF.ExcludesHoleBudgetZZsF
set_option pp.fullNames true in
#print OmissionBalancedZZsN.ExcludesHoleBudgetZZsN
set_option pp.fullNames true in
#print RowEnc.rowText

-- unfolded restatements in the reviewer's words (each must elaborate with no error)
example (N n : ℕ) : ErdosSzekeres.ForcesConvexNGon N n ↔
    ∀ s : Finset (Fin 2 → ℝ), ErdosSzekeres.GeneralPosition s → N ≤ s.card →
      ∃ t : Finset (Fin 2 → ℝ), t ⊆ s ∧ t.card = n ∧
        ConvexIndependent ℝ (fun p : (t : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) := Iff.rfl

example (s : Finset (Fin 2 → ℝ)) : ErdosSzekeres.GeneralPosition s ↔
    ∀ a ∈ s, ∀ b ∈ s, ∀ c ∈ s, a ≠ b → a ≠ c → b ≠ c → ¬ Collinear ℝ ({a, b, c} : Set (Fin 2 → ℝ)) := Iff.rfl

example (B : ℕ) : OmissionZRow.N66Bound B ↔ ∀ n : ℕ, ∀ c : ErdosSzekeres.Omission.Configuration n,
    ¬ c.HasCap 6 → ¬ c.HasCup 6 → ¬ ErdosSzekeres.HasConvexNGon 8 (Finset.univ.image c.point) → n ≤ B := Iff.rfl

example (B : ℕ) : ErdosSzekeres.Omission.Partition.ResidualBound B ↔
    ∀ n : ℕ, ∀ c : ErdosSzekeres.Omission.Configuration n, ¬ c.HasCap 6 →
      ¬ ErdosSzekeres.HasConvexNGon 8 (Finset.univ.image c.point) →
      ErdosSzekeres.Omission.Subsets.NoJunctionOn c.cup (Finset.range n) → n ≤ B := Iff.rfl

example (rows : List (List ℕ)) : RowGeo.RowsTextUnsat rows ↔
    ∀ s ∈ rows, ∀ nv F, EncB.parseDimacsBytes (RowEnc.rowText s).toUTF8.data.toList = some (nv, F) →
      ¬ ∃ ν : ℕ → Bool, ∀ c ∈ F, ∃ l ∈ c, (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false) := Iff.rfl

example : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN (70 - 55) 68 ↔
    OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68 := Iff.rfl

#eval IO.println "=== S7 AXIOMS (reviewer theorems and the pieces)"
#print axioms RV5.rb118
#print axioms RV5.es304
#print axioms RV5.es303
#print axioms RV5.es302
#print axioms RV5.n66mono
#print axioms RV5.text_iff
#print axioms RS.s33_18
#print axioms RS.s34_18
#print axioms RS.s34_19
#print axioms RS.s35_18
#print axioms RowGeo.residual_bound_118_of_texts
#print axioms OmissionBalancedZZsF.composition_303_zzsf
#print axioms OmissionBalancedZZsN.composition_302_n54

#eval show CoreM Unit from do
  IO.println "=== S8 MODULES (Lean's own resolution via findOLean)"
  let env ← getEnv
  IO.println s!"NMODULES {env.header.moduleNames.size}"
  for m in env.header.moduleNames do
    let p ← findOLean m
    IO.println s!"MOD {m} {p}"

#eval show IO Unit from do
  IO.println "=== S9 ROWS (interpreter, Res118.Rows olean)"
  for (nm, rows) in [("P", Res118.rowsP), ("Q", Res118.rowsQ), ("U", Res118.rowsU), ("A", Res118.rowsA)] do
    IO.println s!"ROWLEN {nm} {rows.length}"
    let mut i := 0
    for s in rows do
      IO.println s!"ROW {nm} {i} {",".intercalate (s.map toString)}"
      i := i + 1

#eval show IO Unit from do
  IO.println "=== S10 INTERPRETER rowText U 0"
  match Res118.rowsU[0]? with
  | some s =>
    let t := RowEnc.rowText s
    IO.FS.writeFile "/home/jay/research/data/formalize-20261122/combined/review/data/interp_rowText_U_0.cnf" t
    IO.println s!"INTERP U 0 support={s} bytes={t.utf8ByteSize}"
  | none => IO.println "INTERP U 0 missing"

#eval IO.println "=== END"
