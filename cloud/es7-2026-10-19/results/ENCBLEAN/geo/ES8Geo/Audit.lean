import ES8Geo.Main

/-! # M8 audit: axioms and statements of the geometric half, pinned by `#guard_msgs`

`lake build` fails if any of these outputs changes. Part of `scripts/audit_geo.sh` (check 7 re-elaborates
this file). Every declaration here that mentions the (6,8,11) instance is a term (no tactic block). -/

/-! ## The texts hypothesis is equivalent to `CubesUnsat64`

The hypothesis of `sixfold_es8_of_texts` (and of `EncB.no_model_6811_of_texts`) is not vacuous: since
every text parses (`EncB.parseDimacs_cube64_get`), it says exactly `CubesUnsat64`. The proof is a term
(no `cases`/`injection`, which would try to reduce `encB 6 8 11`). -/

namespace EncB.Geo

/-- **The texts hypothesis ↔ `CubesUnsat64`.** -/
theorem texts_iff_cubesUnsat64 :
    (∀ (i : Nat) (hi : i < EncB.cubes64.length) (nv : Nat) (G : List (List Int)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 6 8 11) (EncB.cubes64.get ⟨i, hi⟩)) = some (nv, G) →
        ¬EncB.DimacsSatisfiable G) ↔ EncB.CubesUnsat64 :=
  ⟨EncB.cubesUnsat64_of_texts_get, fun h i hi _nv G hp =>
    have hG : G = EncB.cubeCnf (EncB.encB 6 8 11) (EncB.cubes64.get ⟨i, hi⟩) :=
      congrArg Prod.snd (Option.some.inj (hp.symm.trans (EncB.parseDimacs_cube64_get i hi)))
    fun hs => h _ (List.get_mem EncB.cubes64 ⟨i, hi⟩) (hG ▸ hs)⟩

end EncB.Geo

/-! ## Axioms -/

/-- info: 'EncB.Geo.sixfold_es8' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.sixfold_es8

/-- info: 'EncB.Geo.sixfold_es8_of_texts' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.sixfold_es8_of_texts

/-- info: 'EncB.Geo.sixfold66_of_unsat' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.sixfold66_of_unsat

/-- info: 'EncB.Geo.sixfold66_of_cubes64' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.sixfold66_of_cubes64

/-- info: 'EncB.Geo.sixfold66_of_no_model' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.sixfold66_of_no_model

/-- info: 'EncB.Geo.modelOfLabelling' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.modelOfLabelling

/-- info: 'EncB.Geo.labelling_of_counterexample' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.labelling_of_counterexample

/-- info: 'EncB.Geo.modelOfLabelling_chi' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.modelOfLabelling_chi

/-- info: 'EncB.Geo.modelOfLabelling_psiLt' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.modelOfLabelling_psiLt

/-- info: 'EncB.Geo.sixfold_es8_order6' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.sixfold_es8_order6

/-- info: 'EncB.Geo.sixfold_es8_order6_of_texts' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.sixfold_es8_order6_of_texts

/-- info: 'EncB.Geo.rotAbout_neg_sixth' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.rotAbout_neg_sixth

/-- info: 'EncB.Geo.invariant_sixth_of_five' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.invariant_sixth_of_five

/-- info: 'EncB.Geo.texts_iff_cubesUnsat64' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in #print axioms EncB.Geo.texts_iff_cubesUnsat64

/-! ## Statements -/

/--
info: EncB.Geo.sixfold_es8 : EncB.CubesUnsat64 →
  ∀ (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point),
    ErdosSzekeres.GeneralPosition S →
      ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 6)) S →
        61 ≤ S.card → ErdosSzekeres.HasConvexNGon 8 S
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.sixfold_es8

/--
info: EncB.Geo.sixfold_es8_of_texts : (∀ (i : ℕ) (hi : i < EncB.cubes64.length) (nv : ℕ) (G : List (List ℤ)),
    EncB.parseDimacs (EncB.cnfText (EncB.encode 6 8 11) (EncB.cubes64.get ⟨i, hi⟩)) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G) →
  ∀ (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point),
    ErdosSzekeres.GeneralPosition S →
      ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 6)) S →
        61 ≤ S.card → ErdosSzekeres.HasConvexNGon 8 S
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.sixfold_es8_of_texts

/--
info: EncB.Geo.sixfold66_of_unsat : ¬EncB.DimacsSatisfiable (EncB.encB 6 8 11) → ErdosSzekeres.LayerLemma.Sixfold66
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.sixfold66_of_unsat

/-- info: EncB.Geo.sixfold66_of_cubes64 : EncB.CubesUnsat64 → ErdosSzekeres.LayerLemma.Sixfold66 -/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.sixfold66_of_cubes64

/-- The hypothesis of `sixfold_es8_of_texts` is literally that of `EncB.no_model_6811_of_texts`. -/
example (h : ∀ (i : Nat) (hi : i < EncB.cubes64.length) (nv : Nat) (G : List (List Int)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 6 8 11) (EncB.cubes64.get ⟨i, hi⟩)) = some (nv, G) →
        ¬EncB.DimacsSatisfiable G) : EncB.Model 6 8 11 → False :=
  EncB.no_model_6811_of_texts h

/-- `sixfold_es8` concludes the statement of `sixfold_octagon` from `CubesUnsat64`. -/
example (h : EncB.CubesUnsat64) :
    ∀ (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point),
      ErdosSzekeres.GeneralPosition S →
      ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 6)) S →
      61 ≤ S.card → ErdosSzekeres.HasConvexNGon 8 S :=
  EncB.Geo.sixfold_es8 h


/--
info: EncB.Geo.texts_iff_cubesUnsat64 : (∀ (i : ℕ) (hi : i < EncB.cubes64.length) (nv : ℕ) (G : List (List ℤ)),
    EncB.parseDimacs (EncB.cnfText (EncB.encode 6 8 11) (EncB.cubes64.get ⟨i, hi⟩)) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G) ↔
  EncB.CubesUnsat64
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.texts_iff_cubesUnsat64

/--
info: EncB.Geo.sixfold66_of_no_model : (∀ (a : EncB.Model 6 8 11), False) → ErdosSzekeres.LayerLemma.Sixfold66
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.sixfold66_of_no_model

/--
info: EncB.Geo.sixfold_es8_order6 : EncB.CubesUnsat64 →
  ∀ (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point),
    ErdosSzekeres.GeneralPosition S →
      ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 6)) S ∨
          ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi * 5 / 6)) S →
        61 ≤ S.card → ErdosSzekeres.HasConvexNGon 8 S
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.sixfold_es8_order6

/--
info: EncB.Geo.sixfold_es8_order6_of_texts : (∀ (i : ℕ) (hi : i < EncB.cubes64.length) (nv : ℕ) (G : List (List ℤ)),
    EncB.parseDimacs (EncB.cnfText (EncB.encode 6 8 11) (EncB.cubes64.get ⟨i, hi⟩)) = some (nv, G) →
      ¬EncB.DimacsSatisfiable G) →
  ∀ (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point),
    ErdosSzekeres.GeneralPosition S →
      ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 6)) S ∨
          ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi * 5 / 6)) S →
        61 ≤ S.card → ErdosSzekeres.HasConvexNGon 8 S
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.sixfold_es8_order6_of_texts

/--
info: EncB.Geo.rotAbout_neg_sixth : ∀ (c : ErdosSzekeres.Point),
  ErdosSzekeres.LayerLemma.rotAbout c (-(2 * Real.pi / 6)) = ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi * 5 / 6)
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.rotAbout_neg_sixth

/--
info: @EncB.Geo.modelOfLabelling : {m K t : ℕ} →
  3 ≤ m →
    Even m →
      4 ≤ K →
        K ≤ 2 * m →
          {T : Finset ErdosSzekeres.Point} →
            {c : ErdosSzekeres.Point} →
              ErdosSzekeres.GeneralPosition T →
                c ∉ T →
                  ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / ↑m)) T →
                    ¬ErdosSzekeres.HasConvexNGon K T → EncB.Geo.PolarLabelling m t T c → EncB.Model m K t
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.modelOfLabelling

/--
info: @EncB.Geo.modelOfLabelling_chi : ∀ {m K t : ℕ} (hm : 3 ≤ m) (heven : Even m) (hK4 : 4 ≤ K) (hK : K ≤ 2 * m)
  {T : Finset ErdosSzekeres.Point} {c : ErdosSzekeres.Point} (hgp : ErdosSzekeres.GeneralPosition T) (hc : c ∉ T)
  (hinv : ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / ↑m)) T)
  (hno : ¬ErdosSzekeres.HasConvexNGon K T) (L : EncB.Geo.PolarLabelling m t T c),
  (EncB.Geo.modelOfLabelling hm heven hK4 hK hgp hc hinv hno L).chi = L.chi
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.modelOfLabelling_chi

/--
info: @EncB.Geo.modelOfLabelling_psiLt : ∀ {m K t : ℕ} (hm : 3 ≤ m) (heven : Even m) (hK4 : 4 ≤ K) (hK : K ≤ 2 * m)
  {T : Finset ErdosSzekeres.Point} {c : ErdosSzekeres.Point} (hgp : ErdosSzekeres.GeneralPosition T) (hc : c ∉ T)
  (hinv : ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / ↑m)) T)
  (hno : ¬ErdosSzekeres.HasConvexNGon K T) (L : EncB.Geo.PolarLabelling m t T c),
  (EncB.Geo.modelOfLabelling hm heven hK4 hK hgp hc hinv hno L).psiLt = L.psiLt
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.modelOfLabelling_psiLt

/--
info: @EncB.Geo.labelling_of_counterexample : ∀ {m K t : ℕ},
  2 ≤ m →
    Even m →
      K ≤ 2 * m →
        ∀ {T : Finset ErdosSzekeres.Point} {c : ErdosSzekeres.Point},
          ErdosSzekeres.GeneralPosition T →
            c ∉ T →
              ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / ↑m)) T →
                ¬ErdosSzekeres.HasConvexNGon K T → T.card = m * t → Nonempty (EncB.Geo.PolarLabelling m t T c)
-/
#guard_msgs (whitespace := lax) in #check @EncB.Geo.labelling_of_counterexample
