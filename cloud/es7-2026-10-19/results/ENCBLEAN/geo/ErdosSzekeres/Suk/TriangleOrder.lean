import ErdosSzekeres.OrientationGeometry
import Mathlib.Analysis.Convex.Combination
import Mathlib.Order.Basic

namespace ErdosSzekeres.Suk

@[ext] structure UpperPoint where
  val : Point
  property : 0 < val 1

/-- Coordinates adapted to the segment from (0,0) to (1,0). -/
noncomputable def triangleCoordinates (p : UpperPoint) : ℝ × ℝ :=
  (p.val 0 / p.val 1, (1 - p.val 0) / p.val 1)

theorem triangleCoordinates_injective : Function.Injective triangleCoordinates := by
  intro p q h
  have h₀ := congrArg Prod.fst h
  have h₁ := congrArg Prod.snd h
  dsimp [triangleCoordinates] at h₀ h₁
  have hp := ne_of_gt p.property
  have hq := ne_of_gt q.property
  have h₀' := (div_eq_div_iff hp hq).mp h₀
  have h₁' := (div_eq_div_iff hp hq).mp h₁
  have hy : p.val 1 = q.val 1 := by nlinarith
  have hx : p.val 0 = q.val 0 := by
    rw [hy] at h₀'
    exact mul_right_cancel₀ hq h₀'
  apply UpperPoint.ext
  ext i
  fin_cases i <;> assumption

instance : PartialOrder UpperPoint :=
  PartialOrder.lift triangleCoordinates triangleCoordinates_injective

theorem triangle_mem_of_weights (a b c p : Point) (u v w : ℝ)
    (hu : 0 ≤ u) (hv : 0 ≤ v) (hw : 0 ≤ w) (hs : u + v + w = 1)
    (hp : p = u • a + v • b + w • c) :
    p ∈ convexHull ℝ ({a, b, c} : Set Point) := by
  have h := (convex_convexHull ℝ ({a, b, c} : Set Point)).sum_mem
    (t := Finset.univ) (w := ![u, v, w]) (z := ![a, b, c])
    (by intro i _; fin_cases i <;> assumption)
    (by simpa [Fin.sum_univ_three] using hs)
    (by intro i _; apply subset_convexHull; fin_cases i <;> simp)
  simpa [Fin.sum_univ_three, hp] using h

/-- The lifted order has precisely the triangle-containment meaning used in
Suk's partial-order construction, for a normalized horizontal base segment. -/
theorem triangleOrder_iff (p q : UpperPoint) :
    p ≤ q ↔ q.val ∈ convexHull ℝ ({![0, 0], ![1, 0], p.val} : Set Point) := by
  change (p.val 0 / p.val 1 ≤ q.val 0 / q.val 1 ∧
    (1 - p.val 0) / p.val 1 ≤ (1 - q.val 0) / q.val 1) ↔ _
  rw [div_le_div_iff₀ p.property q.property, div_le_div_iff₀ p.property q.property]
  constructor
  · rintro ⟨h₀, h₁⟩
    let w := q.val 1 / p.val 1
    have hw : 0 ≤ w := (div_pos q.property p.property).le
    have he : w * p.val 1 = q.val 1 := div_mul_cancel₀ _ (ne_of_gt p.property)
    have he' := congrArg (fun t : ℝ => t * p.val 0) he
    have hv : 0 ≤ q.val 0 - w * p.val 0 := by
      apply nonneg_of_mul_nonneg_right (a := p.val 1) ?_ p.property
      nlinarith
    have hu : 0 ≤ 1 - q.val 0 - w * (1 - p.val 0) := by
      apply nonneg_of_mul_nonneg_right (a := p.val 1) ?_ p.property
      nlinarith
    apply triangle_mem_of_weights ![0, 0] ![1, 0] p.val q.val
      (1 - q.val 0 - w * (1 - p.val 0)) (q.val 0 - w * p.val 0) w hu hv hw
    · ring
    · ext i
      fin_cases i <;> simp [Pi.smul_apply, smul_eq_mul, Pi.add_apply]
      exact he.symm
  · intro hq
    have hconv₀ : Convex ℝ {x : Point | p.val 0 * x 1 ≤ x 0 * p.val 1} := by
      intro x hx y hy a b ha hb hab
      simp only [Set.mem_setOf_eq, Pi.add_apply, Pi.smul_apply, smul_eq_mul] at *
      nlinarith [mul_nonneg ha (sub_nonneg.mpr hx), mul_nonneg hb (sub_nonneg.mpr hy)]
    have hconv₁ : Convex ℝ {x : Point | (1 - p.val 0) * x 1 ≤ (1 - x 0) * p.val 1} := by
      intro x hx y hy a b ha hb hab
      simp only [Set.mem_setOf_eq, Pi.add_apply, Pi.smul_apply, smul_eq_mul] at *
      have hab' := congrArg (fun t : ℝ => t * p.val 1) hab
      nlinarith [mul_nonneg ha (sub_nonneg.mpr hx), mul_nonneg hb (sub_nonneg.mpr hy)]
    have hs₀ : ({![0, 0], ![1, 0], p.val} : Set Point) ⊆
        {x : Point | p.val 0 * x 1 ≤ x 0 * p.val 1} := by
      intro x hx
      rcases hx with rfl | rfl | rfl <;> simp [le_of_lt p.property]
    have hs₁ : ({![0, 0], ![1, 0], p.val} : Set Point) ⊆
        {x : Point | (1 - p.val 0) * x 1 ≤ (1 - x 0) * p.val 1} := by
      intro x hx
      rcases hx with rfl | rfl | rfl <;> simp [le_of_lt p.property]
    exact ⟨convexHull_min hs₀ hconv₀ hq, convexHull_min hs₁ hconv₁ hq⟩

theorem triangleOrder_cross_products (p q : UpperPoint) :
    p ≤ q ↔ p.val 0 * q.val 1 ≤ q.val 0 * p.val 1 ∧
      (1 - p.val 0) * q.val 1 ≤ (1 - q.val 0) * p.val 1 := by
  change (_ / _ ≤ _ / _ ∧ _ / _ ≤ _ / _) ↔ _
  rw [div_le_div_iff₀ p.property q.property, div_le_div_iff₀ p.property q.property]

/-- Incomparable points put both endpoints of the base strictly on the same
side of their line. This is the separation used in Suk's antichain case. -/
theorem incomparable_base_same_side (p q : UpperPoint)
    (hpq : ¬ p ≤ q) (hqp : ¬ q ≤ p) :
    0 < orient p.val q.val ![0, 0] * orient p.val q.val ![1, 0] := by
  rw [triangleOrder_cross_products] at hpq hqp
  simp only [orient, Matrix.cons_val_zero, Matrix.cons_val_one]
  by_cases h : p.val 0 * q.val 1 ≤ q.val 0 * p.val 1
  · have h' : (1 - q.val 0) * p.val 1 < (1 - p.val 0) * q.val 1 :=
      lt_of_not_ge (fun h' => hpq ⟨h, h'⟩)
    have h'' : p.val 0 * q.val 1 < q.val 0 * p.val 1 := by
      by_contra! hn
      apply hqp
      exact ⟨hn, h'.le⟩
    apply mul_pos_of_neg_of_neg <;> nlinarith
  · have h' : q.val 0 * p.val 1 < p.val 0 * q.val 1 := lt_of_not_ge h
    have h'' : (1 - p.val 0) * q.val 1 < (1 - q.val 0) * p.val 1 :=
      lt_of_not_ge (fun h'' => hqp ⟨h'.le, h''⟩)
    apply mul_pos <;> nlinarith

/-- No point of the base segment is collinear with an incomparable pair. -/
theorem incomparable_base_not_collinear (p q : UpperPoint)
    (hpq : ¬ p ≤ q) (hqp : ¬ q ≤ p) (t : ℝ) (ht₀ : 0 ≤ t) (ht₁ : t ≤ 1) :
    orient p.val q.val ![t, 0] ≠ 0 := by
  have hprod := incomparable_base_same_side p q hpq hqp
  have heq : orient p.val q.val ![t, 0] =
      (1 - t) * orient p.val q.val ![0, 0] + t * orient p.val q.val ![1, 0] := by
    simp only [orient, Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  rw [heq]
  by_cases ht : t = 0
  · subst t
    simpa using (left_ne_zero_of_mul (ne_of_gt hprod))
  have ht : 0 < t := lt_of_le_of_ne ht₀ (Ne.symm ht)
  rcases (mul_pos_iff.mp hprod) with ⟨ha, hb⟩ | ⟨ha, hb⟩
  · exact ne_of_gt (add_pos_of_nonneg_of_pos
      (mul_nonneg (sub_nonneg.mpr ht₁) ha.le) (mul_pos ht hb))
  · exact ne_of_lt (add_neg_of_nonpos_of_neg
      (mul_nonpos_of_nonneg_of_nonpos (sub_nonneg.mpr ht₁) ha.le)
      (mul_neg_of_pos_of_neg ht hb))

/-- Moving forward in the triangle order moves strictly toward the base. -/
theorem triangleOrder_height_strict (p q : UpperPoint) (hpq : p < q) :
    q.val 1 < p.val 1 := by
  obtain ⟨h₀, h₁⟩ := (triangleOrder_cross_products p q).mp hpq.le
  have hle : q.val 1 ≤ p.val 1 := by linarith
  by_contra! hge
  have hy : p.val 1 = q.val 1 := le_antisymm hge hle
  have hx : p.val 0 = q.val 0 := by
    rw [hy] at h₀ h₁
    have hmul : p.val 0 * q.val 1 = q.val 0 * q.val 1 := by linarith
    exact mul_right_cancel₀ (ne_of_gt q.property) hmul
  apply hpq.ne
  apply UpperPoint.ext
  ext i
  fin_cases i <;> assumption

/-- The line through a strictly ordered pair meets the normalized base. -/
theorem triangleOrder_line_meets_base (p q : UpperPoint) (hpq : p < q) :
    ∃ t : ℝ, 0 ≤ t ∧ t ≤ 1 ∧ orient p.val q.val ![t, 0] = 0 := by
  obtain ⟨h₀, h₁⟩ := (triangleOrder_cross_products p q).mp hpq.le
  have hden : 0 < p.val 1 - q.val 1 := sub_pos.mpr (triangleOrder_height_strict p q hpq)
  let t := (p.val 1 * q.val 0 - q.val 1 * p.val 0) / (p.val 1 - q.val 1)
  have ht₀ : 0 ≤ t := div_nonneg (by nlinarith) hden.le
  have ht₁ : t ≤ 1 := (div_le_one hden).mpr (by nlinarith)
  refine ⟨t, ht₀, ht₁, ?_⟩
  have ht : t * (p.val 1 - q.val 1) = p.val 1 * q.val 0 - q.val 1 * p.val 0 :=
    div_mul_cancel₀ _ (ne_of_gt hden)
  simp only [orient, Matrix.cons_val_zero, Matrix.cons_val_one]
  nlinarith

end ErdosSzekeres.Suk
