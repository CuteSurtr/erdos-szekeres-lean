import ETVEncoding.Main
import ETVEncoding.Targets

/-!
# Removing the distinct-x hypothesis

The shear `(x, y) ↦ (x + ε y, y)` is a linear bijection of determinant 1, so it preserves
`orient` exactly and maps convex position to convex position. For all but finitely many `ε`
it makes the x-coordinates of a finite set distinct. This proves `DistinctXReduction`, and
with it the unconditional consequence of an UNSAT verdict for `gen_etv.py N K K K`.
-/

namespace ETV

open ErdosSzekeres

/-- The shear `(x, y) ↦ (x + ε y, y)`. -/
def shear (ε : ℝ) : Point →ₗ[ℝ] Point where
  toFun p := ![p 0 + ε * p 1, p 1]
  map_add' p q := by
    ext i
    fin_cases i
    all_goals simp
    all_goals ring
  map_smul' c p := by
    ext i
    fin_cases i
    all_goals simp
    all_goals ring

@[simp] theorem shear_apply_zero (ε : ℝ) (p : Point) : shear ε p 0 = p 0 + ε * p 1 := rfl

@[simp] theorem shear_apply_one (ε : ℝ) (p : Point) : shear ε p 1 = p 1 := rfl

theorem shear_neg_shear (ε : ℝ) (p : Point) : shear (-ε) (shear ε p) = p := by
  ext i
  fin_cases i <;> simp

theorem shear_shear_neg (ε : ℝ) (p : Point) : shear ε (shear (-ε) p) = p := by
  ext i
  fin_cases i <;> simp

theorem shear_injective (ε : ℝ) : Function.Injective (shear ε) := fun p q h => by
  rw [← shear_neg_shear ε p, h, shear_neg_shear]

theorem orient_shear (ε : ℝ) (a b c : Point) :
    orient (shear ε a) (shear ε b) (shear ε c) = orient a b c := by
  simp only [orient, shear_apply_zero, shear_apply_one]
  ring

theorem generalPosition_shear {S : Finset Point} (ε : ℝ) (h : GeneralPosition S) :
    GeneralPosition (S.image (shear ε)) := by
  classical
  rw [generalPosition_iff_orient_ne_zero] at h ⊢
  intro a ha b hb c hc hab hac hbc
  obtain ⟨a', ha', rfl⟩ := Finset.mem_image.1 ha
  obtain ⟨b', hb', rfl⟩ := Finset.mem_image.1 hb
  obtain ⟨c', hc', rfl⟩ := Finset.mem_image.1 hc
  rw [orient_shear]
  exact h a' ha' b' hb' c' hc' (fun e => hab (e ▸ rfl)) (fun e => hac (e ▸ rfl))
    (fun e => hbc (e ▸ rfl))

/-- Convex position pulls back along an injective linear map. -/
theorem convexPosition_of_image_linear {T : Finset Point} (f : Point →ₗ[ℝ] Point)
    (hf : Function.Injective f) (h : ConvexPosition (T.image f)) : ConvexPosition T := by
  classical
  rw [convexPosition_iff] at h ⊢
  intro p hp hhull
  apply h (f p) (by rw [Finset.coe_image]; exact Set.mem_image_of_mem f hp)
  have := Set.mem_image_of_mem f hhull
  rw [LinearMap.image_convexHull] at this
  rwa [Finset.coe_image, ← Set.image_singleton, ← Set.image_diff hf]

/-- Some shear makes all x-coordinates distinct. -/
theorem exists_shear_distinctX (S : Finset Point) :
    ∃ ε : ℝ, LowerBound.DistinctX (S.image (shear ε)) := by
  classical
  let bad : Finset ℝ := (S ×ˢ S).image (fun pq => (pq.2 0 - pq.1 0) / (pq.1 1 - pq.2 1))
  haveI : Infinite ℝ := Infinite.of_injective (Nat.cast : ℕ → ℝ) Nat.cast_injective
  obtain ⟨ε, hε⟩ := Infinite.exists_notMem_finset bad
  refine ⟨ε, ?_⟩
  intro a ha b hb hab
  simp only [Finset.coe_image, Set.mem_image, Finset.mem_coe] at ha hb
  obtain ⟨p, hp, rfl⟩ := ha
  obtain ⟨q, hq, rfl⟩ := hb
  have hab' : p 0 + ε * p 1 = q 0 + ε * q 1 := hab
  by_cases h1 : p 1 = q 1
  · have h0 : p 0 = q 0 := by
      rw [h1] at hab'
      linarith
    have : p = q := by
      ext i
      fin_cases i
      · exact h0
      · exact h1
    rw [this]
  · exfalso
    apply hε
    rw [Finset.mem_image]
    refine ⟨(p, q), Finset.mem_product.2 ⟨hp, hq⟩, ?_⟩
    simp only
    rw [div_eq_iff (sub_ne_zero.2 h1)]
    linarith

/-- **`DistinctXReduction` holds.** -/
theorem distinctXReduction : DistinctXReduction := by
  classical
  intro N K h S hgp hN
  obtain ⟨T, hTS, hT⟩ := Finset.exists_subset_card_eq hN
  obtain ⟨ε, hε⟩ := exists_shear_distinctX T
  have hcard : (T.image (shear ε)).card = N := by
    rw [Finset.card_image_of_injective _ (shear_injective ε), hT]
  obtain ⟨U', hU', hU'card, hU'conv⟩ :=
    h (T.image (shear ε)) (generalPosition_shear ε (hgp.mono hTS)) hε hcard
  refine ⟨U'.image (shear (-ε)), ?_, ?_, ?_⟩
  · intro q hq
    obtain ⟨p', hp', rfl⟩ := Finset.mem_image.1 hq
    obtain ⟨t, ht, rfl⟩ := Finset.mem_image.1 (hU' hp')
    rw [shear_neg_shear]
    exact hTS ht
  · rw [Finset.card_image_of_injective _ (shear_injective (-ε)), hU'card]
  · apply convexPosition_of_image_linear (shear ε) (shear_injective ε)
    have : (U'.image (shear (-ε))).image (shear ε) = U' := by
      rw [Finset.image_image]
      conv_rhs => rw [← Finset.image_id (s := U')]
      apply Finset.image_congr
      intro p _
      exact shear_shear_neg ε p
    rw [this]
    exact hU'conv

/-- **What an UNSAT certificate for `gen_etv.py N K K K` proves** (`K ≥ 4`): every `N` points
in general position contain a convex `K`-gon. No distinct-x hypothesis. -/
theorem forcesConvexNGon_of_unsat {N K : ℕ} (hunsat : ¬DimacsSatisfiable (dimacs N K K K))
    (hK : 4 ≤ K) : ForcesConvexNGon N K :=
  distinctXReduction N K (fun S hgp hS hN => hasConvexNGon_of_unsat hunsat hK S hgp hS hN)

/-- In particular, UNSAT of `gen_etv.py 33 7 7 7` would prove the heptagon case of the
Erdős–Szekeres conjecture (`HeptagonConjecture` is `ForcesConvexNGon 33 7`). -/
theorem heptagonConjecture_of_unsat (h : ¬DimacsSatisfiable (dimacs 33 7 7 7)) :
    HeptagonConjecture :=
  forcesConvexNGon_of_unsat h (by norm_num)

end ETV
