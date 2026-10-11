import ErdosSzekeres.LowerBound.Defs
import Mathlib.Order.Filter.Finite

/-! Translating a block far to the right and far up or down realizes the
stacking signs. Translation preserves all the bounded quantities. -/

namespace ErdosSzekeres.LowerBound

/-- Translate a finite point set by `v`. -/
noncomputable def translate (v : Point) (s : Finset Point) : Finset Point :=
  s.image (· + v)

variable {σ : ℝ} {m : ℕ} {v : Point} {s : Finset Point}

theorem card_translate : (translate v s).card = s.card :=
  Finset.card_image_of_injective s (add_left_injective v)

theorem generalPosition_translate (h : GeneralPosition s) : GeneralPosition (translate v s) := by
  rw [generalPosition_iff_orient_ne_zero] at h ⊢
  simp only [translate, Finset.forall_mem_image, ne_eq, add_left_inj, orient_translate]
  exact h

theorem distinctX_translate (h : DistinctX s) : DistinctX (translate v s) := by
  rintro _ hp _ hq hpq
  simp only [translate, Finset.coe_image, Set.mem_image, Finset.mem_coe] at hp hq
  obtain ⟨a, ha, rfl⟩ := hp
  obtain ⟨b, hb, rfl⟩ := hq
  simp only [Pi.add_apply, add_left_inj] at hpq
  rw [h ha hb hpq]

theorem chainBound_translate (h : ChainBound σ m s) : ChainBound σ m (translate v s) := by
  intro t ht hc
  obtain ⟨u, hu, rfl⟩ := Finset.subset_image_iff.1 ht
  rw [Finset.card_image_of_injective _ (add_left_injective v)]
  refine h u hu fun a ha b hb c hc' hab hbc => ?_
  simpa [orient_translate] using
    hc _ (Finset.mem_image_of_mem _ ha) _ (Finset.mem_image_of_mem _ hb)
      _ (Finset.mem_image_of_mem _ hc') (by simpa using hab) (by simpa using hbc)

open scoped Pointwise in
private theorem convexPosition_of_translate {u : Finset Point}
    (h : ConvexPosition (translate v u)) : ConvexPosition u := by
  have hT : ((translate v u : Finset Point) : Set Point) = v +ᵥ (u : Set Point) := by
    rw [translate, Finset.coe_image, ← Set.image_vadd]
    simp_rw [vadd_eq_add, add_comm v]
  rw [convexPosition_iff, hT] at h
  rw [convexPosition_iff]
  intro p hp hmem
  refine h (v +ᵥ p) (Set.vadd_mem_vadd_set hp) ?_
  rw [← Set.vadd_set_singleton, ← Set.vadd_set_sdiff, convexHull_vadd]
  exact Set.vadd_mem_vadd_set hmem

theorem convexBound_translate (h : ConvexBound m s) : ConvexBound m (translate v s) := by
  intro t ht hc
  obtain ⟨u, hu, rfl⟩ := Finset.subset_image_iff.1 ht
  rw [Finset.card_image_of_injective _ (add_left_injective v)]
  exact h u hu (convexPosition_of_translate hc)

/-- A linear function of positive slope is eventually positive. -/
private theorem eventually_pos_mul_add {c : ℝ} (hc : 0 < c) (d : ℝ) :
    ∀ᶠ M in Filter.atTop, 0 < c * M + d :=
  (Filter.eventually_gt_atTop (-d / c)).mono fun M hM => by
    rw [div_lt_iff₀ hc] at hM
    linarith

/-- Every second block can be translated so that it is stacked on the first. -/
theorem exists_stacked (σ : ℝ) (hσ : σ ≠ 0) (A B : Finset Point) :
    ∃ v : Point, Stacked σ A (translate v B) := by
  have hσ2 : 0 < σ ^ 2 := by positivity
  obtain ⟨t, ht⟩ : ∃ t : ℝ, ∀ a ∈ A, ∀ b ∈ B, a 0 < b 0 + t :=
    ((Filter.eventually_all_finset A).2 fun a _ => (Filter.eventually_all_finset B).2 fun b _ =>
      (Filter.eventually_gt_atTop (a 0 - b 0)).mono fun _ h => by linarith).exists
  have hL : ∀ᶠ M in Filter.atTop, ∀ a ∈ A, ∀ a' ∈ A, ∀ b ∈ B, a 0 < a' 0 →
      0 < σ * orient a a' (b + ![t, σ * M]) := by
    refine (Filter.eventually_all_finset A).2 fun a _ => (Filter.eventually_all_finset A).2
      fun a' _ => (Filter.eventually_all_finset B).2 fun b _ =>
        Filter.eventually_imp_distrib_left.2 fun h => ?_
    refine (eventually_pos_mul_add (mul_pos hσ2 (sub_pos.2 h))
      (σ * orient a a' (b + ![t, 0]))).mono fun M hM => ?_
    convert hM using 1
    simp [orient]
    ring
  have hR : ∀ᶠ M in Filter.atTop, ∀ a ∈ A, ∀ b ∈ B, ∀ b' ∈ B, b 0 < b' 0 →
      σ * orient a (b + ![t, σ * M]) (b' + ![t, σ * M]) < 0 := by
    refine (Filter.eventually_all_finset A).2 fun a _ => (Filter.eventually_all_finset B).2
      fun b _ => (Filter.eventually_all_finset B).2 fun b' _ =>
        Filter.eventually_imp_distrib_left.2 fun h => ?_
    refine (eventually_pos_mul_add (mul_pos hσ2 (sub_pos.2 h))
      (-(σ * orient a (b + ![t, 0]) (b' + ![t, 0])))).mono fun M hM => ?_
    rw [← neg_pos]
    convert hM using 1
    simp [orient]
    ring
  obtain ⟨M, hL, hR⟩ := (hL.and hR).exists
  refine ⟨![t, σ * M], ⟨?_, ?_, ?_⟩⟩ <;> simp only [translate, Finset.forall_mem_image]
  · intro a ha b hb
    simpa using ht a ha b hb
  · exact hL
  · intro a ha b hb b' hb' h
    exact hR a ha b hb b' hb' (by simpa using h)

end ErdosSzekeres.LowerBound
