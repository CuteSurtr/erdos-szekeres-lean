import AE33Geo.Radius1

/-! # Statement-fidelity review of ae33-lean (reviewer slot lrv3, 22 Nov 2026)

Reviewer's own file. No `open`, full names printed, no auto-bound implicits. Compiled against oleans rebuilt by the
reviewer from a snapshot of the worker's sources (`review/olean`), not against the worker's `build/olean`.
Section 4 restates the theorems in the reviewer's own words with the definitions unfolded; each restatement is a
separate declaration, so a typo there costs only that item. -/

set_option autoImplicit false
set_option pp.fullNames true

/-! ## 1. Axioms (first, so they print even if a later item fails) -/

#print axioms AE33Geo.ae33_pair
#print axioms AE33Geo.ae33_radius1
#print axioms AE33Geo.ae33_radius0
#print axioms AE33Geo.cnf_sat
#print axioms AE33.texts_iff_cnfs
#print axioms AE33Geo.clauseOf_sound
#print axioms AE33.parse_cnfText
#print axioms AE33Geo.pair_of_unsat
#print axioms AE33Geo.pairs_cover
#print axioms AE33Geo.pairOfIdx_of_mem
#print axioms AE33Geo.mem_of_any

/-! ## 2. Full statements -/

#check @AE33Geo.ae33_pair
#check @AE33Geo.ae33_radius1
#check @AE33Geo.ae33_radius0
#check @AE33Geo.cnf_sat
#check @AE33Geo.clauseOf_sound
#check @AE33.texts_iff_cnfs
#check @AE33.parse_cnfText
#check @AE33Geo.pair_of_unsat
#check @AE33Geo.pairs_cover

/-! ## 3. Definitions that occur in the statements -/

#print AE33.TextsUnsat203
#print AE33.CnfsUnsat203
#print AE33.cnfText
#print AE33.cnf
#print AE33.clauseB
#print AE33.numVars
#print AE33.numVarsN
#print AE33.n2
#print AE33.baseOf
#print AE33.pairOfIdx
#print AE33.base
#print AE33.keepIdx
#print AE33.hept
#print AE33.iorient
#print AE33.Pt
#print AE33Geo.Realizes
#print AE33Geo.RealizesMirror
#print AE33Geo.ConvexNGonThrough
#print AE33Geo.OTEmb
#print AE33Geo.OTEmbMirror
#print AE33Geo.Ctx
#print AE33Geo.Realizes31
#print AE33Geo.PosChain
#print ErdosSzekeres.Point
#print ErdosSzekeres.orient
#print ErdosSzekeres.GeneralPosition
#print ErdosSzekeres.ConvexPosition
#print ErdosSzekeres.HasConvexNGon
#print EncB.DimacsSatisfiable
#print EncB.DimacsSat
#print EncB.parseDimacs
#print EncB.render

/-! ## 4. Reviewer's restatements -/

/-- RS1. REC §1 Theorem with every definition unfolded (pair index form). Pure definitional unfolding. -/
theorem review_rs1_pair_unfolded :
    AE33.TextsUnsat203 → ∀ (i : Fin 203) (P : Fin 31 → ErdosSzekeres.Point),
      ((∀ a b c : Fin 31, (0 < ErdosSzekeres.orient (P a) (P b) (P c) ↔
          0 < AE33.iorient ((AE33.baseOf i).getD a (0, 0)) ((AE33.baseOf i).getD b (0, 0))
            ((AE33.baseOf i).getD c (0, 0)))) ∨
       (∀ a b c : Fin 31, (0 < ErdosSzekeres.orient (P a) (P b) (P c) ↔
          AE33.iorient ((AE33.baseOf i).getD a (0, 0)) ((AE33.baseOf i).getD b (0, 0))
            ((AE33.baseOf i).getD c (0, 0)) < 0))) →
      ∀ p q : ErdosSzekeres.Point,
        ErdosSzekeres.GeneralPosition (insert p (insert q (Finset.univ.image P))) →
        (insert p (insert q (Finset.univ.image P))).card = 33 →
        (∃ t : Finset ErdosSzekeres.Point, t ⊆ insert p (insert q (Finset.univ.image P)) ∧ t.card = 7 ∧
            ErdosSzekeres.ConvexPosition t ∧ p ∈ t) ∨
        (∃ t : Finset ErdosSzekeres.Point, t ⊆ insert p (insert q (Finset.univ.image P)) ∧ t.card = 7 ∧
            ErdosSzekeres.ConvexPosition t ∧ q ∈ t) :=
  fun h i P hP p q hgp hcard => AE33Geo.ae33_pair h i P hP p q hgp hcard

/-- RS2. REC §1 Corollary with every definition unfolded. Pure definitional unfolding. -/
theorem review_rs2_radius1_unfolded :
    AE33.TextsUnsat203 → ∀ (S : Finset ErdosSzekeres.Point), ErdosSzekeres.GeneralPosition S → S.card = 33 →
      ∀ (u v : ℕ), u < 33 → v < 33 → u ≠ v → ∀ (φ : ℕ → ErdosSzekeres.Point),
        (∀ w : ℕ, w < 33 → w ≠ u → w ≠ v → φ w ∈ S) →
        (∀ a b : ℕ, a < 33 → b < 33 → a ≠ u → a ≠ v → b ≠ u → b ≠ v → φ a = φ b → a = b) →
        ((∀ a b c : ℕ, a < 33 → b < 33 → c < 33 → a ≠ u → a ≠ v → b ≠ u → b ≠ v → c ≠ u → c ≠ v →
            (0 < ErdosSzekeres.orient (φ a) (φ b) (φ c) ↔
              0 < AE33.iorient (AE33.ae33.getD a (0, 0)) (AE33.ae33.getD b (0, 0)) (AE33.ae33.getD c (0, 0)))) ∨
         (∀ a b c : ℕ, a < 33 → b < 33 → c < 33 → a ≠ u → a ≠ v → b ≠ u → b ≠ v → c ≠ u → c ≠ v →
            (0 < ErdosSzekeres.orient (φ a) (φ b) (φ c) ↔
              AE33.iorient (AE33.ae33.getD a (0, 0)) (AE33.ae33.getD b (0, 0)) (AE33.ae33.getD c (0, 0)) < 0))) →
        ∃ t : Finset ErdosSzekeres.Point, t ⊆ S ∧ t.card = 7 ∧ ErdosSzekeres.ConvexPosition t :=
  fun h S hgp hcard u v hu hv huv φ hS hinj hφ =>
    AE33Geo.ae33_radius1 h S hgp hcard u v hu hv huv φ hS hinj hφ

/-- RS3. Radius 0 with the natural hypothesis (each label once ≠ w), from `ae33_radius0`. -/
theorem review_rs3_radius0_natural :
    AE33.TextsUnsat203 → ∀ (S : Finset ErdosSzekeres.Point), ErdosSzekeres.GeneralPosition S → S.card = 33 →
      ∀ (w : ℕ), w < 33 → ∀ (φ : ℕ → ErdosSzekeres.Point),
        (∀ x : ℕ, x < 33 → x ≠ w → φ x ∈ S) →
        (∀ a b : ℕ, a < 33 → b < 33 → a ≠ w → b ≠ w → φ a = φ b → a = b) →
        ((∀ a b c : ℕ, a < 33 → b < 33 → c < 33 → a ≠ w → b ≠ w → c ≠ w →
            (0 < ErdosSzekeres.orient (φ a) (φ b) (φ c) ↔
              0 < AE33.iorient (AE33.ae33.getD a (0, 0)) (AE33.ae33.getD b (0, 0)) (AE33.ae33.getD c (0, 0)))) ∨
         (∀ a b c : ℕ, a < 33 → b < 33 → c < 33 → a ≠ w → b ≠ w → c ≠ w →
            (0 < ErdosSzekeres.orient (φ a) (φ b) (φ c) ↔
              AE33.iorient (AE33.ae33.getD a (0, 0)) (AE33.ae33.getD b (0, 0)) (AE33.ae33.getD c (0, 0)) < 0))) →
        ∃ t : Finset ErdosSzekeres.Point, t ⊆ S ∧ t.card = 7 ∧ ErdosSzekeres.ConvexPosition t :=
  fun h S hgp hcard w hw φ hS hinj hφ => AE33Geo.ae33_radius0 h S hgp hcard w hw φ hS hinj
    (hφ.elim (fun H => Or.inl fun a b c ha hb hc h1 _ h3 _ h5 _ => H a b c ha hb hc h1 h3 h5)
      (fun H => Or.inr fun a b c ha hb hc h1 _ h3 _ h5 _ => H a b c ha hb hc h1 h3 h5))

/-- RS4. REC §1 Theorem for an explicit pair u < v < 33 that meets H (instead of an index into `pairs203`). -/
theorem review_rs4_pair_explicit (h : AE33.TextsUnsat203) (u v : ℕ) (huv : u < v) (hv : v < 33)
    (hH : u ∈ AE33.hept ∨ v ∈ AE33.hept) (P : Fin 31 → ErdosSzekeres.Point)
    (hP : AE33Geo.Realizes (AE33.base u v) P ∨ AE33Geo.RealizesMirror (AE33.base u v) P)
    (p q : ErdosSzekeres.Point)
    (hgp : ErdosSzekeres.GeneralPosition (insert p (insert q (Finset.univ.image P))))
    (hcard : (insert p (insert q (Finset.univ.image P))).card = 33) :
    AE33Geo.ConvexNGonThrough 7 (insert p (insert q (Finset.univ.image P))) p ∨
      AE33Geo.ConvexNGonThrough 7 (insert p (insert q (Finset.univ.image P))) q := by
  rcases AE33Geo.pairs_cover v hv u huv with hany | ⟨hu', hv'⟩
  · obtain ⟨i, hi, hpair⟩ := AE33Geo.pairOfIdx_of_mem (AE33Geo.mem_of_any hany)
    have hb : AE33.baseOf i = AE33.base u v := by simp only [AE33.baseOf, hpair]
    have hreal : AE33Geo.Realizes (AE33.baseOf i) P ∨ AE33Geo.RealizesMirror (AE33.baseOf i) P := by
      rw [hb]; exact hP
    exact AE33Geo.ae33_pair h ⟨i, hi⟩ P hreal p q hgp hcard
  · exact (hH.elim hu' hv').elim

/-- The map of RS5: label `w` of AE33 − {u, v} goes to `σ w`. -/
noncomputable def reviewPhi (u v : ℕ) (T : Finset ErdosSzekeres.Point)
    (σ : {w : ℕ // w < 33 ∧ w ≠ u ∧ w ≠ v} ≃ T) (w : ℕ) : ErdosSzekeres.Point :=
  if hw : w < 33 ∧ w ≠ u ∧ w ≠ v then (σ ⟨w, hw⟩ : ErdosSzekeres.Point) else 0

theorem reviewPhi_eq {u v : ℕ} {T : Finset ErdosSzekeres.Point}
    (σ : {w : ℕ // w < 33 ∧ w ≠ u ∧ w ≠ v} ≃ T) {w : ℕ} (hw : w < 33 ∧ w ≠ u ∧ w ≠ v) :
    reviewPhi u v T σ w = (σ ⟨w, hw⟩ : ErdosSzekeres.Point) := by
  unfold reviewPhi
  rw [dif_pos hw]

/-- RS5. REC §1 Corollary in set form: S (33 points, general position) contains a subset T and a bijection σ from
the labels of AE33 − {u, v} onto T that preserves (or reverses) every orientation sign. Then S has a convex 7-gon. -/
theorem review_rs5_radius1_subset (h : AE33.TextsUnsat203) (S : Finset ErdosSzekeres.Point)
    (hgp : ErdosSzekeres.GeneralPosition S) (hcard : S.card = 33)
    (u v : ℕ) (hu : u < 33) (hv : v < 33) (huv : u ≠ v)
    (T : Finset ErdosSzekeres.Point) (hT : T ⊆ S)
    (σ : {w : ℕ // w < 33 ∧ w ≠ u ∧ w ≠ v} ≃ T)
    (hsign : (∀ a b c : {w : ℕ // w < 33 ∧ w ≠ u ∧ w ≠ v},
        (0 < ErdosSzekeres.orient (σ a : ErdosSzekeres.Point) (σ b : ErdosSzekeres.Point)
            (σ c : ErdosSzekeres.Point) ↔
          0 < AE33.iorient (AE33.ae33.getD a.1 (0, 0)) (AE33.ae33.getD b.1 (0, 0)) (AE33.ae33.getD c.1 (0, 0)))) ∨
      (∀ a b c : {w : ℕ // w < 33 ∧ w ≠ u ∧ w ≠ v},
        (0 < ErdosSzekeres.orient (σ a : ErdosSzekeres.Point) (σ b : ErdosSzekeres.Point)
            (σ c : ErdosSzekeres.Point) ↔
          AE33.iorient (AE33.ae33.getD a.1 (0, 0)) (AE33.ae33.getD b.1 (0, 0)) (AE33.ae33.getD c.1 (0, 0)) < 0))) :
    ErdosSzekeres.HasConvexNGon 7 S := by
  refine AE33Geo.ae33_radius1 h S hgp hcard u v hu hv huv (reviewPhi u v T σ) ?_ ?_ ?_
  · intro w hw h1 h2
    rw [reviewPhi_eq σ ⟨hw, h1, h2⟩]
    exact hT (σ ⟨w, ⟨hw, h1, h2⟩⟩).2
  · intro a b ha hb h1 h2 h3 h4 hab
    rw [reviewPhi_eq σ ⟨ha, h1, h2⟩, reviewPhi_eq σ ⟨hb, h3, h4⟩] at hab
    exact congrArg Subtype.val (σ.injective (Subtype.ext hab))
  · rcases hsign with hs | hs
    · left
      intro a b c ha hb hc h1 h2 h3 h4 h5 h6
      rw [reviewPhi_eq σ ⟨ha, h1, h2⟩, reviewPhi_eq σ ⟨hb, h3, h4⟩, reviewPhi_eq σ ⟨hc, h5, h6⟩]
      exact hs ⟨a, ⟨ha, h1, h2⟩⟩ ⟨b, ⟨hb, h3, h4⟩⟩ ⟨c, ⟨hc, h5, h6⟩⟩
    · right
      intro a b c ha hb hc h1 h2 h3 h4 h5 h6
      rw [reviewPhi_eq σ ⟨ha, h1, h2⟩, reviewPhi_eq σ ⟨hb, h3, h4⟩, reviewPhi_eq σ ⟨hc, h5, h6⟩]
      exact hs ⟨a, ⟨ha, h1, h2⟩⟩ ⟨b, ⟨hb, h3, h4⟩⟩ ⟨c, ⟨hc, h5, h6⟩⟩

#print axioms review_rs1_pair_unfolded
#print axioms review_rs2_radius1_unfolded
#print axioms review_rs3_radius0_natural
#print axioms review_rs4_pair_explicit
#print axioms review_rs5_radius1_subset
