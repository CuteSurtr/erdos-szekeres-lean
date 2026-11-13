import ErdosSzekeres.Omission.CoupledSemantics

/-
Clipping cup coordinates in the abstract coupled labeling model.
This does not assert that the clipped coordinates are attained geometric ranks.
The imported catalog and residual infrastructure retain their source attribution.
-/

namespace ErdosSzekeres.Omission.RankNormalization

open ResidualDomains

/-- Data unaffected by clipping, including any separately encoded convexity data. -/
structure Frame (k : Nat) where
  position : Fin k → Nat
  cap : Fin k → Fin k → Nat
  positive : Fin k → Fin k → Fin k → Bool
  convex : Fin k → Fin k → Fin k → Fin k → Bool

abbrev Cups (k : Nat) := Fin k → Fin k → Nat

def height {k : Nat} (profiles : Fin k → List Nat) (i : Fin k) : Nat :=
  (profiles i).getD 0 0

/-- Only the four possible cap coordinates need this Ferrers maximum property. -/
def HeightDominates {k : Nat} (profiles : Fin k → List Nat) : Prop :=
  ∀ i a, 1 ≤ a → a ≤ 4 → (profiles i).getD (a - 1) 0 ≤ height profiles i

def Allowed {k : Nat} (profiles : Fin k → List Nat) (i j : Fin k)
    (a b : Nat) : Prop :=
  Domains.Contains (profiles j) (a, b) ∧
  ¬ Domains.Contains (profiles i) (a, b) ∧ (a, b) ≠ (1, 6)

/-- The complete label-dependent part of the coupled model. Additional packet,
fixed-sign, convexity and octagon constraints are arbitrary predicates on Frame. -/
structure Valid {k : Nat} (profiles : Fin k → List Nat) (F : Frame k)
    (q : Cups k) : Prop where
  injective : Function.Injective F.position
  cap_symm : ∀ i j, F.cap i j = F.cap j i
  cup_symm : ∀ i j, q i j = q j i
  cap_bounds : ∀ i j, i ≠ j → 1 ≤ F.cap i j ∧ F.cap i j ≤ 4
  cup_bounds : ∀ i j, i ≠ j → 1 ≤ q i j ∧ q i j ≤ 6
  domain : ∀ i j, F.position i < F.position j →
    Allowed profiles i j (F.cap i j) (q i j)
  cup_growth : ∀ i j l, F.position i < F.position j →
    F.position j < F.position l → F.positive i j l = true → q i j < q j l
  cap_growth : ∀ i j l, F.position i < F.position j →
    F.position j < F.position l → F.positive i j l = false → F.cap i j < F.cap j l

def SourceBound {k : Nat} (profiles : Fin k → List Nat) (F : Frame k)
    (q : Cups k) : Prop :=
  ∀ i j, F.position i < F.position j → q i j ≤ height profiles i + 1

/-- Earlier-owner clipping; diagonal entries (and ties) are unchanged. -/
def clip {k : Nat} (profiles : Fin k → List Nat) (F : Frame k) (q : Cups k) :
    Cups k := fun i j =>
  if F.position i < F.position j then min (q i j) (height profiles i + 1)
  else if F.position j < F.position i then min (q i j) (height profiles j + 1)
  else q i j

theorem clip_ordered {k : Nat} (profiles : Fin k → List Nat) (F : Frame k)
    (q : Cups k) {i j : Fin k} (hij : F.position i < F.position j) :
    clip profiles F q i j = min (q i j) (height profiles i + 1) := by
  simp [clip, hij]

theorem clip_symm {k : Nat} (profiles : Fin k → List Nat) (F : Frame k)
    (q : Cups k) (hs : ∀ i j, q i j = q j i) (i j : Fin k) :
    clip profiles F q i j = clip profiles F q j i := by
  unfold clip
  by_cases h : F.position i < F.position j
  · have hn : ¬ F.position j < F.position i := by omega
    simp [h, hn, hs i j]
  · by_cases h' : F.position j < F.position i
    · simp [h, h', hs i j]
    · simp [h, h', hs i j]

/-- Clipping preserves target membership, source exclusion, and the forbidden cell. -/
theorem allowed_clip {k : Nat} (profiles : Fin k → List Nat)
    (hd : HeightDominates profiles) (i j : Fin k) (a b : Nat)
    (ha : 1 ≤ a) (ha4 : a ≤ 4) (hb6 : b ≤ 6)
    (h : Allowed profiles i j a b) :
    Allowed profiles i j a (min b (height profiles i + 1)) := by
  obtain ⟨ht, hs, hf⟩ := h
  have hmax := hd i a ha ha4
  unfold Allowed
  unfold Domains.Contains at ht hs ⊢
  dsimp only at ht hs
  refine ⟨?_, ?_, ?_⟩
  · dsimp only
    omega
  · dsimp only
    omega
  · intro heq
    have ha1 : a = 1 := congrArg Prod.fst heq
    have hmin : min b (height profiles i + 1) = 6 := congrArg Prod.snd heq
    have hb : b = 6 := by omega
    exact hf (by simp [ha1, hb])

theorem clipped_growth (b c middle source : Nat) (hbc : b < c)
    (hm : b ≤ middle) :
    min b (source + 1) < min c (middle + 1) := by
  omega

theorem clip_valid {k : Nat} (profiles : Fin k → List Nat)
    (hd : HeightDominates profiles) (F : Frame k) (q : Cups k)
    (h : Valid profiles F q) : Valid profiles F (clip profiles F q) := by
  refine ⟨h.injective, h.cap_symm, clip_symm profiles F q h.cup_symm, h.cap_bounds,
    ?_, ?_, ?_, h.cap_growth⟩
  · intro i j hne
    have hb := h.cup_bounds i j hne
    unfold clip
    split_ifs <;> omega
  · intro i j hij
    have hne : i ≠ j := by intro heq; subst j; omega
    have ha := h.cap_bounds i j hne
    rw [clip_ordered profiles F q hij]
    exact allowed_clip profiles hd i j _ _ ha.1 ha.2
      (h.cup_bounds i j hne).2 (h.domain i j hij)
  · intro i j l hij hjl hp
    rw [clip_ordered profiles F q hij, clip_ordered profiles F q hjl]
    have hne : i ≠ j := by intro heq; subst j; omega
    have ha := h.cap_bounds i j hne
    have ht := (h.domain i j hij).1
    have hmax := hd j (F.cap i j) ha.1 ha.2
    have hm : q i j ≤ height profiles j := by
      unfold Domains.Contains at ht
      exact le_trans ht hmax
    exact clipped_growth _ _ _ _ (h.cup_growth i j l hij hjl hp) hm

theorem clip_sourceBound {k : Nat} (profiles : Fin k → List Nat)
    (F : Frame k) (q : Cups k) : SourceBound profiles F (clip profiles F q) := by
  intro i j hij
  rw [clip_ordered profiles F q hij]
  exact min_le_right _ _

/-- Every old abstract model has a clipped model on exactly the same frame. -/
theorem exists_iff_sourceBound {k : Nat} (profiles : Fin k → List Nat)
    (hd : HeightDominates profiles) (F : Frame k) :
    (∃ q, Valid profiles F q) ↔
      ∃ q, Valid profiles F q ∧ SourceBound profiles F q := by
  constructor
  · rintro ⟨q, hq⟩
    exact ⟨clip profiles F q, clip_valid profiles hd F q hq,
      clip_sourceBound profiles F q⟩
  · rintro ⟨q, hq, _⟩
    exact ⟨q, hq⟩

/-- Any additional conditions depending only on unchanged data are preserved. -/
theorem exists_frame_iff_sourceBound {k : Nat} (profiles : Fin k → List Nat)
    (hd : HeightDominates profiles) (P : Frame k → Prop) :
    (∃ F q, P F ∧ Valid profiles F q) ↔
      ∃ F q, P F ∧ Valid profiles F q ∧ SourceBound profiles F q := by
  constructor
  · rintro ⟨F, q, hP, hq⟩
    exact ⟨F, clip profiles F q, hP, clip_valid profiles hd F q hq,
      clip_sourceBound profiles F q⟩
  · rintro ⟨F, q, hP, hq, _⟩
    exact ⟨F, q, hP, hq⟩

end ErdosSzekeres.Omission.RankNormalization

#print axioms ErdosSzekeres.Omission.RankNormalization.clip_ordered
#print axioms ErdosSzekeres.Omission.RankNormalization.clip_symm
#print axioms ErdosSzekeres.Omission.RankNormalization.allowed_clip
#print axioms ErdosSzekeres.Omission.RankNormalization.clipped_growth
#print axioms ErdosSzekeres.Omission.RankNormalization.clip_valid
#print axioms ErdosSzekeres.Omission.RankNormalization.clip_sourceBound
#print axioms ErdosSzekeres.Omission.RankNormalization.exists_iff_sourceBound
#print axioms ErdosSzekeres.Omission.RankNormalization.exists_frame_iff_sourceBound
