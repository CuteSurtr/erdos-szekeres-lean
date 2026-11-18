import F16Products

namespace Delta3.Forced16Algebra

open Lean.Grind Std

variable {K : Type u} [CommRing K]

def determinant (u v : K × K) : K := u.1 * v.2 - u.2 * v.1

def orient (a b c : K × K) : K :=
  determinant (b.1 - a.1, b.2 - a.2) (c.1 - a.1, c.2 - a.2)

/-- The two-dimensional Pluecker relation, proved by ring algebra. -/
theorem determinant_gp (u v w z : K × K) :
    determinant u v * determinant w z - determinant u w * determinant v z +
      determinant u z * determinant v w = 0 := by
  simp only [determinant]
  grind only

/-- The common-point Grassmann–Pluecker identity for actual coordinate determinants. -/
theorem orient_gp (a b c d e : K × K) :
    orient a b c * orient a d e - orient a b d * orient a c e +
      orient a b e * orient a c d = 0 :=
  determinant_gp (b.1 - a.1, b.2 - a.2) (c.1 - a.1, c.2 - a.2)
    (d.1 - a.1, d.2 - a.2) (e.1 - a.1, e.2 - a.2)

variable [LT K]

/-- Absolute value defined directly from the order, to avoid heavy real imports. -/
noncomputable def magnitude (a : K) : K := by
  classical
  exact if a < 0 then -a else a

theorem magnitude_of_neg {a : K} (h : a < 0) : magnitude a = -a := by
  simp only [magnitude, if_pos h]

theorem magnitude_zero : magnitude (0 : K) = 0 := by
  classical
  unfold magnitude
  split <;> simp only [AddCommGroup.neg_zero]

variable [LE K] [LawfulOrderLT K] [IsLinearOrder K]

theorem magnitude_of_pos {a : K} (h : 0 < a) : magnitude a = a := by
  simp only [magnitude, if_neg (Preorder.not_gt_of_lt h)]

variable [OrderedRing K]

theorem magnitude_pos {a : K} (h : a ≠ 0) : 0 < magnitude a := by
  rcases LinearOrder.trichotomy 0 a with hp | he | hn
  · rw [magnitude_of_pos hp]
    exact hp
  · exact False.elim (h he.symm)
  · rw [magnitude_of_neg hn]
    exact OrderedAdd.neg_pos_iff.mpr hn

/-- In a zero sum of three nonzero terms, a term with the unique sign has
magnitude equal to the sum of the other two positive magnitudes. -/
theorem unique_sign_magnitude (a b c : K) (hsum : a + b + c = 0)
    (hsign : (0 < a ∧ b < 0 ∧ c < 0) ∨ (a < 0 ∧ 0 < b ∧ 0 < c)) :
    magnitude a = magnitude b + magnitude c ∧
      0 < magnitude b ∧ 0 < magnitude c ∧ magnitude b < magnitude a := by
  have heq : magnitude a = magnitude b + magnitude c := by
    rcases hsign with ⟨ha, hb, hc⟩ | ⟨ha, hb, hc⟩
    · rw [magnitude_of_pos ha, magnitude_of_neg hb, magnitude_of_neg hc]
      grind only
    · rw [magnitude_of_neg ha, magnitude_of_pos hb, magnitude_of_pos hc]
      grind only
  have hb : 0 < magnitude b := by
    rcases hsign with ⟨_, hb, _⟩ | ⟨_, hb, _⟩
    · exact magnitude_pos (Preorder.ne_of_lt hb)
    · exact magnitude_pos (Preorder.ne_of_gt hb)
  have hc : 0 < magnitude c := by
    rcases hsign with ⟨_, _, hc⟩ | ⟨_, _, hc⟩
    · exact magnitude_pos (Preorder.ne_of_lt hc)
    · exact magnitude_pos (Preorder.ne_of_gt hc)
  have hlt := OrderedAdd.add_lt_right (magnitude b) hc
  rw [Semiring.add_zero, ← heq] at hlt
  exact ⟨heq, hb, hc, hlt⟩

#print axioms determinant_gp
#print axioms orient_gp
#print axioms magnitude_of_neg
#print axioms magnitude_zero
#print axioms magnitude_of_pos
#print axioms magnitude_pos
#print axioms unique_sign_magnitude

end Delta3.Forced16Algebra
