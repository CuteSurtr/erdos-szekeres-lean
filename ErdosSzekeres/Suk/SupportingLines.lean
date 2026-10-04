import ErdosSzekeres.Suk.BaseOrder
import ErdosSzekeres.Basic

namespace ErdosSzekeres.Suk

theorem orient_affine_combination (p q a b : Point) (u v : ℝ) (huv : u + v = 1) :
    orient p q (u • a + v • b) = u * orient p q a + v * orient p q b := by
  simp only [orient, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  linear_combination (p 1 * q 0 - p 0 * q 1) * huv

theorem convex_orient_positive (p q : Point) : Convex ℝ {r : Point | 0 < orient p q r} := by
  intro a ha b hb u v hu hv huv
  change 0 < orient p q (u • a + v • b)
  rw [orient_affine_combination _ _ _ _ _ _ huv]
  by_cases h : u = 0
  · have hv1 : v = 1 := by linarith
    simpa [h, hv1] using hb
  · exact add_pos_of_pos_of_nonneg (mul_pos (lt_of_le_of_ne hu (Ne.symm h)) ha)
      (mul_nonneg hv hb.le)

theorem convex_orient_nonnegative (p q : Point) : Convex ℝ {r : Point | 0 ≤ orient p q r} := by
  intro a ha b hb u v hu hv huv
  change 0 ≤ orient p q (u • a + v • b)
  rw [orient_affine_combination _ _ _ _ _ _ huv]
  exact add_nonneg (mul_nonneg hu ha) (mul_nonneg hv hb)

/-- A strict supporting line at every selected point proves convex independence. -/
theorem convexPosition_of_strict_supports (s : Finset Point)
    (hs : ∀ p ∈ s, ∃ q : Point, ∀ r ∈ s, r ≠ p → 0 < orient p q r) :
    ConvexPosition s := by
  rw [convexPosition_iff]
  intro p hp hmem
  obtain ⟨q, hq⟩ := hs p hp
  have hsub : ((s : Set Point) \ {p}) ⊆ {r : Point | 0 < orient p q r} := by
    intro r hr
    exact hq r hr.1 (by simpa using hr.2)
  have h := convexHull_min hsub (convex_orient_positive p q) hmem
  simp [orient] at h

theorem orient_support_sum (a p b r : Point) :
    orient p (p + b - a) r = orient a p r + orient p b r := by
  simp only [orient, Pi.add_apply, Pi.sub_apply]
  ring

/-- The counterclockwise four-point orientation pattern forces a convex
quadrilateral. This is useful for Suk's four-point gluing argument. -/
theorem convexPosition_four_of_positive (a b c d : Point)
    (habc : 0 < orient a b c) (habd : 0 < orient a b d)
    (hacd : 0 < orient a c d) (hbcd : 0 < orient b c d) :
    ConvexPosition ({a, b, c, d} : Finset Point) := by
  classical
  apply convexPosition_of_strict_supports
  intro p hp
  simp only [Finset.mem_insert, Finset.mem_singleton] at hp
  rcases hp with hp | hp | hp | hp <;> subst p
  · refine ⟨a + b - d, ?_⟩
    intro r hr hrp
    rw [orient_support_sum]
    simp only [Finset.mem_insert, Finset.mem_singleton] at hr
    rcases hr with rfl | rfl | rfl | rfl
    · exact (hrp rfl).elim
    all_goals simp only [orient] at *; nlinarith
  · refine ⟨b + c - a, ?_⟩
    intro r hr hrp
    rw [orient_support_sum]
    simp only [Finset.mem_insert, Finset.mem_singleton] at hr
    rcases hr with rfl | rfl | rfl | rfl
    · simp only [orient] at *; nlinarith
    · exact (hrp rfl).elim
    all_goals simp only [orient] at *; nlinarith
  · refine ⟨c + d - b, ?_⟩
    intro r hr hrp
    rw [orient_support_sum]
    simp only [Finset.mem_insert, Finset.mem_singleton] at hr
    rcases hr with rfl | rfl | rfl | rfl
    · simp only [orient] at *; nlinarith
    · simp only [orient] at *; nlinarith
    · exact (hrp rfl).elim
    · simp only [orient] at *; nlinarith
  · refine ⟨d + a - c, ?_⟩
    intro r hr hrp
    rw [orient_support_sum]
    simp only [Finset.mem_insert, Finset.mem_singleton] at hr
    rcases hr with rfl | rfl | rfl | rfl
    · simp only [orient] at *; nlinarith
    · simp only [orient] at *; nlinarith
    · simp only [orient] at *; nlinarith
    · exact (hrp rfl).elim

end ErdosSzekeres.Suk
