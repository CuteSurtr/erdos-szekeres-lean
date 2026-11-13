import ErdosSzekeres.Suk.Quadrilateral

namespace ErdosSzekeres

/-- The three equivalent ways to split four orientation signs into two pairs. -/
def QuadConvexSigns (x y z w : Bool) : Prop :=
  (x = y ∧ z = w) ∨ (x ≠ z ∧ y ≠ w) ∨ (y = z ∧ x = w)

instance (x y z w : Bool) : Decidable (QuadConvexSigns x y z w) := by
  unfold QuadConvexSigns
  infer_instance

theorem quadConvexSigns_iff_count (x y z w : Bool) :
    QuadConvexSigns x y z w ↔ [!w, z, !y, x].count true = 2 := by
  cases x <;> cases y <;> cases z <;> cases w <;> decide

private theorem pos_product_iff_sign_eq (x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0) :
    0 < x * y ↔ decide (0 < x) = decide (0 < y) := by
  rcases lt_or_gt_of_ne hx with hx | hx <;>
    rcases lt_or_gt_of_ne hy with hy | hy <;>
    simp [mul_pos_iff, hx, hy, not_lt.mpr hx.le, not_lt.mpr hy.le]

private theorem neg_product_iff_sign_ne (x y : ℝ) (hx : x ≠ 0) (hy : y ≠ 0) :
    x * y < 0 ↔ decide (0 < x) ≠ decide (0 < y) := by
  rcases lt_or_gt_of_ne hx with hx | hx <;>
    rcases lt_or_gt_of_ne hy with hy | hy <;>
    simp [mul_neg_iff, hx, hy, not_lt.mpr hx.le, not_lt.mpr hy.le]

/-- Exact Boolean convex-quadrilateral semantics for four real points.
No coordinate ordering is assumed. -/
theorem convexPosition_four_iff_signs (a b c d : Point)
    (h₀ : orient a b c ≠ 0) (h₁ : orient a b d ≠ 0)
    (h₂ : orient a c d ≠ 0) (h₃ : orient b c d ≠ 0) :
    ConvexPosition ({a, b, c, d} : Finset Point) ↔
      QuadConvexSigns (decide (0 < orient a b c)) (decide (0 < orient a b d))
        (decide (0 < orient a c d)) (decide (0 < orient b c d)) := by
  rw [Suk.convexPosition_four_iff_pair_separation a b c d h₀ h₁ h₂ h₃]
  unfold QuadConvexSigns
  rw [pos_product_iff_sign_eq _ _ h₀ h₁, pos_product_iff_sign_eq _ _ h₂ h₃,
    neg_product_iff_sign_ne _ _ h₀ h₂, neg_product_iff_sign_ne _ _ h₁ h₃,
    pos_product_iff_sign_eq _ _ h₁ h₂, pos_product_iff_sign_eq _ _ h₀ h₃]

theorem convexPosition_four_iff_sign_count (a b c d : Point)
    (h₀ : orient a b c ≠ 0) (h₁ : orient a b d ≠ 0)
    (h₂ : orient a c d ≠ 0) (h₃ : orient b c d ≠ 0) :
    ConvexPosition ({a, b, c, d} : Finset Point) ↔
      [!(decide (0 < orient b c d)), decide (0 < orient a c d),
        !(decide (0 < orient a b d)), decide (0 < orient a b c)].count true = 2 := by
  rw [convexPosition_four_iff_signs a b c d h₀ h₁ h₂ h₃, quadConvexSigns_iff_count]

end ErdosSzekeres
