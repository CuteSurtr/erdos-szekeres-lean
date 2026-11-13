import ErdosSzekeres.LowerBound.Defs

/-! Orientation tests for membership in a triangle. -/

namespace ErdosSzekeres.LowerBound

/-- If `d` lies strictly on the same side of each edge of the triangle `abc`
as the opposite vertex, then `d` lies in the triangle. The common sign is `s`. -/
theorem mem_convexHull_of_orient (s : ℝ) (a b c d : Point)
    (habc : 0 < s * orient a b c) (habd : 0 < s * orient a b d)
    (hbcd : 0 < s * orient b c d) (hcad : 0 < s * orient c a d) :
    d ∈ convexHull ℝ ({a, b, c} : Set Point) := by
  have hs : s ≠ 0 := by rintro rfl; simp at habc
  have hD : orient a b c ≠ 0 := by rintro h; simp [h] at habc
  have hw : ∀ x, 0 < s * x → 0 ≤ x / orient a b c := fun x hx => by
    rw [← mul_div_mul_left x _ hs]; exact (div_pos hx habc).le
  have key := (convex_convexHull ℝ ({a, b, c} : Set Point)).sum_mem (t := Finset.univ)
    (w := ![orient b c d / orient a b c, orient c a d / orient a b c,
      orient a b d / orient a b c]) (z := ![a, b, c]) ?_ ?_ ?_
  · convert key using 1
    ext i
    simp only [Fin.sum_univ_three, Finset.sum_apply, Pi.smul_apply, smul_eq_mul,
      Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two, Matrix.head_cons,
      Matrix.tail_cons]
    field_simp
    fin_cases i <;> simp [orient] <;> ring
  · intro i _
    fin_cases i <;> simp [hw _ hbcd, hw _ hcad, hw _ habd]
  · simp only [Fin.sum_univ_three, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
      Matrix.head_cons, Matrix.tail_cons]
    field_simp
    simp only [orient]
    ring
  · intro i _
    fin_cases i <;> exact subset_convexHull ℝ _ (by simp)

/-- A vertex of a convex polygon is not in the triangle spanned by three other vertices. -/
theorem _root_.ErdosSzekeres.ConvexPosition.not_mem_convexHull_triple {t : Finset Point}
    (ht : ConvexPosition t) {a b c d : Point} (ha : a ∈ t) (hb : b ∈ t) (hc : c ∈ t)
    (hd : d ∈ t) (hda : d ≠ a) (hdb : d ≠ b) (hdc : d ≠ c) :
    d ∉ convexHull ℝ ({a, b, c} : Set Point) := fun h =>
  (convexPosition_iff t).1 ht d hd <| convexHull_mono (by
    rintro x (rfl | rfl | rfl) <;> simp_all [eq_comm]) h

end ErdosSzekeres.LowerBound
