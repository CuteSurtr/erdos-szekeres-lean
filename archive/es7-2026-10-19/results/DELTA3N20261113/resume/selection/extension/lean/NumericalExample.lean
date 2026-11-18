import FieldAdapter

/-! Pure affine-line example, independent of any geometric realization. -/

namespace Delta3.WeightedEnvelope.Example

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

local instance : Lean.Grind.Field K := grindField K

def q : Line K := ⟨-2, -4⟩
def L24 : Line K := ⟨-3 / 2, -15 / 2⟩
def L56 : Line K := ⟨-12, -14⟩
def L57 (h : K) : Line K := ⟨(h - 10) / 2, h⟩
def F (h t : K) : K := max (L24.eval t) (max (L56.eval t) ((L57 h).eval t))

theorem half_sum (t : K) : (L24.eval t + (L57 5).eval t) / 2 = q.eval t + 11 / 4 := by
  grind [L24, L57, q, Line.eval]

theorem mean_le_max (a b : K) : (a + b) / 2 ≤ max a b :=
  (div_le_iff₀ (show (0 : K) < 2 from zero_lt_two)).2
    ((add_le_add (le_max_left a b) (le_max_right a b)).trans_eq (mul_two (max a b)).symm)

/-- The exact positive margin holds on the whole parameter line, hence on the requested ray. -/
theorem safe_at_five (t : K) : q.eval t + 11 / 4 ≤ F 5 t :=
  calc
    q.eval t + 11 / 4 = (L24.eval t + (L57 5).eval t) / 2 := (half_sum t).symm
    _ ≤ max (L24.eval t) ((L57 5).eval t) := mean_le_max _ _
    _ ≤ F 5 t := max_le (le_max_left _ _) ((le_max_right _ _).trans (le_max_right _ _))

/-- Each of the three ambient lines fails at an explicit positive parameter. -/
theorem no_single_support_at_five :
    (∃ t : K, 0 < t ∧ L24.eval t < q.eval t) ∧
    (∃ t : K, 0 < t ∧ L56.eval t < q.eval t) ∧
    (∃ t : K, 0 < t ∧ (L57 5).eval t < q.eval t) := by
  refine ⟨⟨1, ?_, ?_⟩, ⟨1, ?_, ?_⟩, ⟨20, ?_, ?_⟩⟩
  all_goals grind [L24, L56, L57, q, Line.eval]

theorem difference24 (t : K) : q.eval t - L24.eval t = (7 - t) / 2 := by
  grind [q, L24, Line.eval]

theorem below24_iff (t : K) : L24.eval t < q.eval t ↔ t < 7 := by
  rw [← sub_pos, difference24, lt_div_iff₀ (show (0 : K) < 2 from zero_lt_two),
    zero_mul, sub_pos]

theorem difference57_at_three (t : K) : q.eval t - (L57 3).eval t = (3 * t - 14) / 2 := by
  grind [q, L57, Line.eval]

theorem below57_at_three_iff (t : K) : (L57 3).eval t < q.eval t ↔ 14 / 3 < t := by
  rw [← sub_pos, difference57_at_three,
    lt_div_iff₀ (show (0 : K) < 2 from zero_lt_two), zero_mul, sub_pos,
    div_lt_iff₀ (show (0 : K) < 3 by grind), mul_comm t 3]

theorem below56_iff (t : K) : L56.eval t < q.eval t ↔ -1 < t := by
  change -12 * t + -14 < -2 * t + -4 ↔ -1 < t
  grind

/-- The strict exposure interval is exact, including exclusion of both endpoints. -/
theorem exposure_at_three_iff (t : K) : F 3 t < q.eval t ↔ 14 / 3 < t ∧ t < 7 := by
  rw [F, max_lt_iff, max_lt_iff, below24_iff, below56_iff, below57_at_three_iff]
  grind

theorem exposure_at_six :
    F (K := K) 3 6 = -33 / 2 ∧ (q (K := K)).eval 6 = -16 ∧
      F (K := K) 3 6 < q.eval 6 := by
  dsimp [F, L24, L56, L57, q, Line.eval]
  grind

#print axioms half_sum
#print axioms mean_le_max
#print axioms safe_at_five
#print axioms no_single_support_at_five
#print axioms difference24
#print axioms below24_iff
#print axioms difference57_at_three
#print axioms below57_at_three_iff
#print axioms below56_iff
#print axioms exposure_at_three_iff
#print axioms exposure_at_six

end Delta3.WeightedEnvelope.Example
