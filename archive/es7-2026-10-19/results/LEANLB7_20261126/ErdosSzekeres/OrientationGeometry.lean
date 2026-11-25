import ErdosSzekeres.Definitions
import ErdosSzekeres.Orientation
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

namespace ErdosSzekeres

private theorem exists_smul_of_det_zero (u v : Point) (hu : u ≠ 0)
    (h : u 0 * v 1 - u 1 * v 0 = 0) : ∃ r : ℝ, v = r • u := by
  by_cases hx : u 0 = 0
  · have hy : u 1 ≠ 0 := by
      intro hy
      apply hu
      ext i
      fin_cases i <;> simp [hx, hy]
    refine ⟨v 1 / u 1, ?_⟩
    ext i
    fin_cases i
    · change v 0 = v 1 / u 1 * u 0
      rw [hx, mul_zero]
      rw [hx, zero_mul, zero_sub, neg_eq_zero] at h
      have := mul_eq_zero.mp h
      exact this.resolve_left hy
    · simp [div_mul_cancel₀ _ hy]
  · refine ⟨v 0 / u 0, ?_⟩
    ext i
    fin_cases i
    · simp [div_mul_cancel₀ _ hx]
    · change v 1 = v 0 / u 0 * u 1
      field_simp
      nlinarith

/-- The determinant test agrees with Mathlib's affine definition, including
degenerate triples. This is the first geometric bridge for exact certificates. -/
theorem orient_eq_zero_iff_collinear (a b c : Point) :
    orient a b c = 0 ↔ Collinear ℝ ({a, b, c} : Set Point) := by
  rw [collinear_iff_of_mem (k := ℝ) (p₀ := a) (by simp : a ∈ ({a, b, c} : Set Point))]
  constructor
  · intro h
    by_cases hab : b = a
    · subst b
      refine ⟨c - a, ?_⟩
      intro p hp
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hp
      rcases hp with rfl | rfl | rfl
      · exact ⟨0, by simp⟩
      · exact ⟨0, by simp⟩
      · exact ⟨1, by simp⟩
    · have hu : b - a ≠ 0 := sub_ne_zero.mpr hab
      obtain ⟨r, hr⟩ := exists_smul_of_det_zero (b - a) (c - a) hu h
      refine ⟨b - a, ?_⟩
      intro p hp
      simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hp
      rcases hp with rfl | rfl | rfl
      · exact ⟨0, by simp⟩
      · exact ⟨1, by simp⟩
      · exact ⟨r, by simpa [vadd_eq_add, sub_eq_iff_eq_add] using hr⟩
  · rintro ⟨v, hv⟩
    obtain ⟨r, hr⟩ := hv b (by simp)
    obtain ⟨s, hs⟩ := hv c (by simp)
    rw [hr, hs]
    simp only [orient, vadd_eq_add, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    ring

theorem generalPosition_iff_orient_ne_zero (s : Finset Point) :
    GeneralPosition s ↔ ∀ a ∈ s, ∀ b ∈ s, ∀ c ∈ s,
      a ≠ b → a ≠ c → b ≠ c → orient a b c ≠ 0 := by
  simp only [GeneralPosition, ne_eq, orient_eq_zero_iff_collinear]

/-- A decidable rational predicate whose transfer theorem has no numerical
tolerances or floating-point assumptions. -/
abbrev RationalGeneralPosition (s : Finset (Fin 2 → ℚ)) : Prop :=
  ∀ a ∈ s, ∀ b ∈ s, ∀ c ∈ s,
    a ≠ b → a ≠ c → b ≠ c → orient a b c ≠ 0

theorem generalPosition_of_rational (s : Finset (Fin 2 → ℚ))
    (h : RationalGeneralPosition s) : GeneralPosition (s.image rationalToReal) := by
  classical
  rw [generalPosition_iff_orient_ne_zero]
  intro a ha b hb c hc hab hac hbc
  obtain ⟨a', ha', rfl⟩ := Finset.mem_image.mp ha
  obtain ⟨b', hb', rfl⟩ := Finset.mem_image.mp hb
  obtain ⟨c', hc', rfl⟩ := Finset.mem_image.mp hc
  apply (orient_rationalToReal_ne_zero a' b' c').mpr
  exact h a' ha' b' hb' c' hc'
    (fun e => hab (congrArg rationalToReal e))
    (fun e => hac (congrArg rationalToReal e))
    (fun e => hbc (congrArg rationalToReal e))

end ErdosSzekeres
