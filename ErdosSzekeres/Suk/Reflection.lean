import ErdosSzekeres.Suk.CupsCaps

namespace ErdosSzekeres

/-- Transport a convex polygon by an invertible linear change of coordinates. -/
theorem HasConvexNGon.linearEquiv {S : Finset Point} {n : ℕ}
    (h : HasConvexNGon n S) (e : Point ≃ₗ[ℝ] Point) :
    HasConvexNGon n (S.image e) := by
  classical
  obtain ⟨T, hTS, hTcard, hTconv⟩ := h
  refine ⟨T.image e, Finset.image_subset_image hTS, ?_, ?_⟩
  · simpa [Finset.card_image_of_injective T e.injective] using hTcard
  · rw [convexPosition_iff] at hTconv ⊢
    intro q hq hmem
    obtain ⟨p, hp, rfl⟩ := Finset.mem_image.mp hq
    apply hTconv p hp
    have hm : e.symm (e p) ∈
        e.symm.toLinearMap '' convexHull ℝ ((↑(T.image e) : Set Point) \ {e p}) :=
      Set.mem_image_of_mem e.symm hmem
    rw [e.symm.toLinearMap.image_convexHull] at hm
    change e.symm (e p) ∈ convexHull ℝ
      (e.symm '' ((↑(T.image e) : Set Point) \ {e p})) at hm
    have he : e.symm '' ((↑(T.image e) : Set Point) \ {e p}) =
        (T : Set Point) \ {p} := by
      rw [Set.image_diff e.symm.injective, Set.image_singleton,
        LinearEquiv.symm_apply_apply]
      congr 1
      simp [Finset.coe_image, ← Set.image_comp]
    simpa only [he, LinearEquiv.symm_apply_apply] using hm

namespace Suk

/-- Reflection in the horizontal axis keeps the x-order and exchanges cups/caps. -/
def reflectY : Point ≃ₗ[ℝ] Point where
  toFun p := ![p 0, -p 1]
  invFun p := ![p 0, -p 1]
  left_inv p := by ext i; fin_cases i <;> simp
  right_inv p := by ext i; fin_cases i <;> simp
  map_add' p q := by ext i; fin_cases i <;> simp [add_comm]
  map_smul' r p := by ext i; fin_cases i <;> simp

@[simp] theorem reflectY_x (p : Point) : reflectY p 0 = p 0 := rfl
@[simp] theorem reflectY_y (p : Point) : reflectY p 1 = -p 1 := rfl
@[simp] theorem reflectY_reflectY (p : Point) : reflectY (reflectY p) = p := by
  ext i; fin_cases i <;> simp

@[simp] theorem orient_reflectY (a b c : Point) :
    orient (reflectY a) (reflectY b) (reflectY c) = -orient a b c := by
  simp only [orient, reflectY_x, reflectY_y]
  ring

theorem generalPosition_reflectY {S : Finset Point} (h : GeneralPosition S) :
    GeneralPosition (S.image reflectY) := by
  classical
  rw [generalPosition_iff_orient_ne_zero] at h ⊢
  intro a ha b hb c hc hab hac hbc
  obtain ⟨a', ha', rfl⟩ := Finset.mem_image.mp ha
  obtain ⟨b', hb', rfl⟩ := Finset.mem_image.mp hb
  obtain ⟨c', hc', rfl⟩ := Finset.mem_image.mp hc
  simpa only [orient_reflectY, neg_ne_zero] using h a' ha' b' hb' c' hc'
    (fun he => hab (congrArg reflectY he)) (fun he => hac (congrArg reflectY he))
    (fun he => hbc (congrArg reflectY he))

theorem hasConvexNGon_of_reflectY {S : Finset Point} {n : ℕ}
    (h : HasConvexNGon n (S.image reflectY)) : HasConvexNGon n S := by
  classical
  simpa [Finset.image_image, Function.comp_def] using h.linearEquiv reflectY

end Suk
end ErdosSzekeres
