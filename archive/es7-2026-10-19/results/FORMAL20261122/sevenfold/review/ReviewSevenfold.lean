import Geo7.Main7
import Lean

/-!
# Reviewer slot lrv2: statement fidelity of item sevenfold-encoder (ONE compile)

Read from the worker's olean store (`/home/jay/research/data/formalize-20261122/sevenfold/olean`, Mathlib
`f897ebcf` from ENCBLEAN geo's packages). Nothing here proves anything new: every theorem below is closed by
`Iff.rfl`, `rfl` or by naming one of the worker's theorems. Statements that mention `7 8 10` are copied verbatim, so
the unifier never has a reason to unfold `encode 7 8 10`. Each command is independent: an error in one is reported
as a failed check, not retried.
-/

/-! ## A. Axioms of the reviewed theorems -/

#print axioms EncB.Geo7.sevenfold_es8_of_text
#print axioms EncB.Geo7.sevenfold_es8_order7_of_text
#print axioms EncB.Geo7.sevenfold70_of_unsat
#print axioms EncB.Geo7.geo7Bridge
#print axioms EncB.Geo7.modelO_of_counterexample
#print axioms EncB.Geo7.exists_perturbation
#print axioms EncB.encB_satisfiable_odd
#print axioms EncB.no_modelO_7810_of_text
#print axioms EncB.text7810_iff
#print axioms EncB.Geo7.sevenfold_es8
#print axioms EncB.encB_satisfiable_7810
#print axioms ErdosSzekeres.LayerLemma.sevenfold_octagon
#print axioms EncB.parseDimacs_base7810
#print axioms EncB.encB7810_unsat_of_text
#print axioms EncB.no_modelO_7810_of_bytes
#print axioms EncB.Geo7.sevenfold70_of_no_modelO
#print axioms EncB.Geo7.layerLab_of_counterexample
#print axioms EncB.Geo7.invariant_seventh_of_order7

/-! ## B. Statements as stored in the oleans -/

#check @EncB.Geo7.sevenfold_es8_of_text
#check @EncB.Geo7.sevenfold_es8_order7_of_text
#check @EncB.Geo7.sevenfold70_of_unsat
#check @EncB.Geo7.geo7Bridge
#check @EncB.Geo7.modelO_of_counterexample
#check @EncB.Geo7.exists_perturbation
#check @EncB.encB_satisfiable_odd
#check @EncB.no_modelO_7810_of_text
#check @EncB.text7810_iff
#check @EncB.Geo7.sevenfold_es8
#check @ErdosSzekeres.LayerLemma.sevenfold_octagon
#check @EncB.Geo7.invariant_seventh_of_order7

set_option pp.all true in
#check @EncB.Geo7.sevenfold_es8_of_text

/-! ## C. Every definition the final statement unfolds to -/

#print ErdosSzekeres.Point
#print ErdosSzekeres.GeneralPosition
#print ErdosSzekeres.ConvexPosition
#print ErdosSzekeres.HasConvexNGon
#print ErdosSzekeres.LayerLemma.Invariant
#print ErdosSzekeres.LayerLemma.rotAbout
#print ErdosSzekeres.LayerLemma.Sevenfold70
#print EncB.Geo7.Geo7Bridge
#print EncB.DimacsSat
#print EncB.DimacsSatisfiable
#print EncB.cnfText
#print EncB.renderCube
#print EncB.encode
#print EncB.encB
#print EncB.numVars
#print EncB.cubeCnf
#print EncB.parseDimacs
#print EncB.ModelO
#print ConvexIndependent
#print Collinear

/-! ## D. One definitional check per definition (generic arguments; nothing mentions `7 8 10`) -/

section Unfold
open ErdosSzekeres ErdosSzekeres.LayerLemma

theorem review_def_gp (s : Finset Point) : GeneralPosition s ↔
    ∀ a ∈ s, ∀ b ∈ s, ∀ d ∈ s, a ≠ b → a ≠ d → b ≠ d →
      ¬ Collinear ℝ ({a, b, d} : Set (Fin 2 → ℝ)) := Iff.rfl

theorem review_def_convpos (s : Finset Point) : ConvexPosition s ↔
    ConvexIndependent ℝ (fun p : (s : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) := Iff.rfl

theorem review_def_ngon (n : ℕ) (s : Finset Point) : HasConvexNGon n s ↔
    ∃ u : Finset (Fin 2 → ℝ), u ⊆ s ∧ u.card = n ∧
      ConvexIndependent ℝ (fun p : (u : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) := Iff.rfl

theorem review_def_inv (f : Point → Point) (S : Finset Point) : Invariant f S ↔ ∀ p ∈ S, f p ∈ S := Iff.rfl

theorem review_def_rot (c p : Point) (θ : ℝ) : rotAbout c θ p =
    ![c 0 + Real.cos θ * (p 0 - c 0) - Real.sin θ * (p 1 - c 1),
      c 1 + Real.sin θ * (p 0 - c 0) + Real.cos θ * (p 1 - c 1)] := rfl

theorem review_def_s70 : Sevenfold70 ↔ ∀ (T : Finset Point) (c : Point), GeneralPosition T → c ∉ T →
    Invariant (rotAbout c (2 * Real.pi / 7)) T → T.card = 70 → HasConvexNGon 8 T := Iff.rfl

theorem review_def_sat (F : List (List ℤ)) : EncB.DimacsSatisfiable F ↔
    ∃ ν : ℕ → Bool, ∀ C ∈ F, ∃ l ∈ C, (0 < l ∧ ν l.natAbs = true) ∨ (l < 0 ∧ ν l.natAbs = false) := Iff.rfl

theorem review_def_text (m K t : ℕ) (cube : List ℤ) : EncB.cnfText (EncB.encode m K t) cube =
    EncB.renderCube (EncB.numVars m K t) (EncB.encB m K t) (EncB.bodyR (EncB.encB m K t)) cube := rfl

theorem review_def_cube (F : List (List ℤ)) (cube : List ℤ) :
    EncB.cubeCnf F cube = F ++ cube.map fun z => [z] := rfl

end Unfold

/-! ## E. The reviewer's own unfolded statements, closed by naming the worker's theorems -/

/-- D2 with every geometric notion unfolded by hand (coordinates, `Collinear`, `ConvexIndependent`), from the
verbatim CNF hypothesis of `sevenfold_es8`. -/
theorem review_D2
    (hcert : ¬ EncB.DimacsSatisfiable (EncB.encB 7 8 10))
    (S : Finset (Fin 2 → ℝ)) (c : Fin 2 → ℝ)
    (hgp : ∀ a ∈ S, ∀ b ∈ S, ∀ d ∈ S, a ≠ b → a ≠ d → b ≠ d →
      ¬ Collinear ℝ ({a, b, d} : Set (Fin 2 → ℝ)))
    (hsym : ∀ p ∈ S,
      (![c 0 + Real.cos (2 * Real.pi / 7) * (p 0 - c 0) - Real.sin (2 * Real.pi / 7) * (p 1 - c 1),
         c 1 + Real.sin (2 * Real.pi / 7) * (p 0 - c 0) + Real.cos (2 * Real.pi / 7) * (p 1 - c 1)]
        : Fin 2 → ℝ) ∈ S)
    (hcard : 65 ≤ S.card) :
    ∃ U : Finset (Fin 2 → ℝ), U ⊆ S ∧ U.card = 8 ∧
      ConvexIndependent ℝ (fun p : (U : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  EncB.Geo7.sevenfold_es8 hcert S c hgp hsym hcard

/-- The same from the verbatim text hypothesis of `sevenfold_es8_of_text`. -/
theorem review_D2_text
    (h : ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 7 8 10) []) = some (nv, G) → ¬ EncB.DimacsSatisfiable G)
    (S : Finset (Fin 2 → ℝ)) (c : Fin 2 → ℝ)
    (hgp : ∀ a ∈ S, ∀ b ∈ S, ∀ d ∈ S, a ≠ b → a ≠ d → b ≠ d →
      ¬ Collinear ℝ ({a, b, d} : Set (Fin 2 → ℝ)))
    (hsym : ∀ p ∈ S,
      (![c 0 + Real.cos (2 * Real.pi / 7) * (p 0 - c 0) - Real.sin (2 * Real.pi / 7) * (p 1 - c 1),
         c 1 + Real.sin (2 * Real.pi / 7) * (p 0 - c 0) + Real.cos (2 * Real.pi / 7) * (p 1 - c 1)]
        : Fin 2 → ℝ) ∈ S)
    (hcard : 65 ≤ S.card) :
    ∃ U : Finset (Fin 2 → ℝ), U ⊆ S ∧ U.card = 8 ∧
      ConvexIndependent ℝ (fun p : (U : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  EncB.Geo7.sevenfold_es8_of_text h S c hgp hsym hcard

/-- Any rotation of order 7 (angle `2πj/7`, `1 ≤ j ≤ 6`), unfolded by hand. -/
theorem review_D2_order7
    (h : ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 7 8 10) []) = some (nv, G) → ¬ EncB.DimacsSatisfiable G)
    (S : Finset (Fin 2 → ℝ)) (c : Fin 2 → ℝ)
    (hgp : ∀ a ∈ S, ∀ b ∈ S, ∀ d ∈ S, a ≠ b → a ≠ d → b ≠ d →
      ¬ Collinear ℝ ({a, b, d} : Set (Fin 2 → ℝ)))
    (j : ℕ) (hj : 1 ≤ j ∧ j ≤ 6)
    (hsym : ∀ p ∈ S,
      (![c 0 + Real.cos (2 * Real.pi * j / 7) * (p 0 - c 0) - Real.sin (2 * Real.pi * j / 7) * (p 1 - c 1),
         c 1 + Real.sin (2 * Real.pi * j / 7) * (p 0 - c 0) + Real.cos (2 * Real.pi * j / 7) * (p 1 - c 1)]
        : Fin 2 → ℝ) ∈ S)
    (hcard : 65 ≤ S.card) :
    ∃ U : Finset (Fin 2 → ℝ), U ⊆ S ∧ U.card = 8 ∧
      ConvexIndependent ℝ (fun p : (U : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  EncB.Geo7.sevenfold_es8_order7_of_text h S c hgp j hj hsym hcard

/-- Narrower variants (only the rotation unfolded / only the conclusion unfolded), to localise a failure. -/
theorem review_D2_rot_only
    (hcert : ¬ EncB.DimacsSatisfiable (EncB.encB 7 8 10))
    (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point) (hgp : ErdosSzekeres.GeneralPosition S)
    (hsym : ∀ p ∈ S,
      (![c 0 + Real.cos (2 * Real.pi / 7) * (p 0 - c 0) - Real.sin (2 * Real.pi / 7) * (p 1 - c 1),
         c 1 + Real.sin (2 * Real.pi / 7) * (p 0 - c 0) + Real.cos (2 * Real.pi / 7) * (p 1 - c 1)]
        : Fin 2 → ℝ) ∈ S)
    (hcard : 65 ≤ S.card) : ErdosSzekeres.HasConvexNGon 8 S :=
  EncB.Geo7.sevenfold_es8 hcert S c hgp hsym hcard

theorem review_D2_concl_only
    (hcert : ¬ EncB.DimacsSatisfiable (EncB.encB 7 8 10))
    (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point)
    (hgp : ∀ a ∈ S, ∀ b ∈ S, ∀ d ∈ S, a ≠ b → a ≠ d → b ≠ d →
      ¬ Collinear ℝ ({a, b, d} : Set (Fin 2 → ℝ)))
    (hinv : ErdosSzekeres.LayerLemma.Invariant
      (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 7)) S)
    (hcard : 65 ≤ S.card) :
    ∃ U : Finset (Fin 2 → ℝ), U ⊆ S ∧ U.card = 8 ∧
      ConvexIndependent ℝ (fun p : (U : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) :=
  EncB.Geo7.sevenfold_es8 hcert S c hgp hinv hcard

/-- The text hypothesis is the plain unsatisfiability of `encB 7 8 10` (verbatim copy of `text7810_iff`). -/
theorem review_h_iff :
    (∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 7 8 10) []) = some (nv, G) → ¬ EncB.DimacsSatisfiable G) ↔
    ¬ EncB.DimacsSatisfiable (EncB.encB 7 8 10) :=
  EncB.text7810_iff

#print axioms review_D2
#print axioms review_D2_text
#print axioms review_D2_order7
#print axioms review_D2_rot_only
#print axioms review_D2_concl_only
#print axioms review_h_iff
#print axioms review_def_rot

/-! ## F. Axiom scan over every constant of the 13 own modules and of the 32 vendored modules (last) -/

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let groups : List (String × Array Name) := [
    ("own (13)", #[`EncBO.ModelO, `EncBO.SoundO, `EncBO.RulesO, `EncBO.AngO, `EncBO.SatisfiableO,
      `EncBO.Compose7, `Geo7.PolarData, `Geo7.ArcData, `Geo7.LayerLab, `Geo7.LayerBasic, `Geo7.Perturb,
      `Geo7.ModelOfLab, `Geo7.Main7]),
    ("vendored (32)", #[`EncB.Gen, `EncB.Dimacs, `EncB.Coded, `EncB.Cover, `EncB.Model, `EncB.ModelLemmas,
      `EncB.SortLemmas, `EncB.SoundOlit, `EncB.SoundOrbit, `EncB.SoundChain, `EncB.SoundAng, `EncB.SoundRules,
      `EncB.SoundWord, `EncB.Satisfiable, `EncB.Render, `EncB.Compose, `ErdosSzekeres.Definitions,
      `ErdosSzekeres.Orientation, `ErdosSzekeres.Basic, `ErdosSzekeres.OrientationGeometry,
      `ErdosSzekeres.Suk.TriangleOrder, `ErdosSzekeres.Suk.BaseChart, `ErdosSzekeres.Suk.BaseOrder,
      `ErdosSzekeres.Suk.FourPoint, `ErdosSzekeres.Suk.SupportingLines, `ErdosSzekeres.Suk.OrientationClique,
      `ES8Geo.KeyOrder, `ES8Geo.Capstone2, `ES8Geo.OrbitConsistency, `ES8Geo.Orbit, `ES8Geo.Interface,
      `ES8Geo.Labelling])]
  for (label, mods) in groups do
    let mut names : Array Name := #[]
    let mut axiomDecls : Array Name := #[]
    let mut missing : Array Name := #[]
    for m in mods do
      match env.getModuleIdx? m with
      | none => missing := missing.push m
      | some idx =>
        match env.header.moduleData[idx.toNat]? with
        | none => missing := missing.push m
        | some md =>
          for ci in md.constants do
            names := names.push ci.name
            if ci matches .axiomInfo _ then axiomDecls := axiomDecls.push ci.name
    let (_, st) := ((names.forM CollectAxioms.collect).run env).run {}
    logInfo m!"axiom scan {label}: {names.size} constants in {mods.size - missing.size} modules (missing: {missing.toList}); union of axioms used: {(st.axioms.qsort Name.lt).toList}; axiom declarations: {axiomDecls.toList}"
