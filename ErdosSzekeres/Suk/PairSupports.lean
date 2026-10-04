import ErdosSzekeres.Suk.SupportingLines

namespace ErdosSzekeres.Suk

/-- An open halfplane together with one point on its boundary is convex.
The scale permits either orientation of the supporting line. -/
theorem convex_insert_scaled_orient_positive (p q : Point) (c : ℝ) :
    Convex ℝ (insert q {r : Point | 0 < c * orient p q r}) := by
  have hq : orient p q q = 0 := by simp only [orient]; ring
  have he (a b : Point) (u v : ℝ) (huv : u + v = 1) :
      c * orient p q (u • a + v • b) =
        u * (c * orient p q a) + v * (c * orient p q b) := by
    rw [orient_affine_combination _ _ _ _ _ _ huv]
    ring
  intro a ha b hb u v hu hv huv
  rcases ha with ha | ha <;> rcases hb with hb | hb
  · subst a
    subst b
    left
    rw [← add_smul, huv, one_smul]
  · subst a
    by_cases hv0 : v = 0
    · left
      have hu1 : u = 1 := by linarith
      simp [hv0, hu1]
    · right
      change 0 < c * orient p q (u • q + v • b)
      rw [he _ _ _ _ huv, hq, mul_zero, mul_zero, zero_add]
      exact mul_pos (lt_of_le_of_ne hv (Ne.symm hv0)) hb
  · subst b
    by_cases hu0 : u = 0
    · left
      have hv1 : v = 1 := by linarith
      simp [hu0, hv1]
    · right
      change 0 < c * orient p q (u • a + v • q)
      rw [he _ _ _ _ huv, hq, mul_zero, mul_zero, add_zero]
      exact mul_pos (lt_of_le_of_ne hu (Ne.symm hu0)) ha
  · right
    change 0 < c * orient p q (u • a + v • b)
    rw [he _ _ _ _ huv]
    by_cases hu0 : u = 0
    · have hv1 : v = 1 := by linarith
      simpa [hu0, hv1] using hb
    · exact add_pos_of_pos_of_nonneg
        (mul_pos (lt_of_le_of_ne hu (Ne.symm hu0)) ha) (mul_nonneg hv hb.le)

/-- A supporting line may pass through one other selected vertex. Strict
separation of all the remaining vertices still proves convex independence. -/
theorem convexPosition_of_pair_supports (s : Finset Point)
    (hs : ∀ p ∈ s, ∃ (q : Point) (c : ℝ), p ≠ q ∧
      ∀ r ∈ s, r ≠ p → r = q ∨ 0 < c * orient p q r) : ConvexPosition s := by
  rw [convexPosition_iff]
  intro p hp hmem
  obtain ⟨q, c, hpq, hside⟩ := hs p hp
  have hsub : ((s : Set Point) \ {p}) ⊆ insert q {r : Point | 0 < c * orient p q r} := by
    intro r hr
    exact hside r hr.1 (by simpa using hr.2)
  have h := convexHull_min hsub (convex_insert_scaled_orient_positive p q c) hmem
  rcases h with h | h
  · exact hpq h
  · simp [orient] at h

end ErdosSzekeres.Suk
