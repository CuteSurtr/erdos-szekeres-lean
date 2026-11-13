import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Algebra.Order.ToIntervalMod

/-!
# Key order for the layered encoder

A direction is written `θ = J * u + ψ` with an integer cell index `J`, a cell width `u > 0`
and a phase `ψ ∈ [0, u)`.

* (a) `cell_lt_iff`: the real order of `θ` is the lexicographic order of `(J, ψ)`.
* (b) `cell_lt_iff_rank`: if `rank` is strictly monotone on the set of phases, the real
  order of `θ` is the lexicographic order of the integer key `(J, rank ψ)`.
* (c) `reduce_mod_two_pi`, `antipode_odd`, `antipode_even`: reduction mod `2π` into `[0, 2π)`
  sends `J * u + ψ` to `(J % N) * u + ψ` when `N * u = 2π`; the antipode `θ + π` gets key
  `((J + m) % (2m), rank)` for units `π/m`, and `((J + m/2) % m, rank)` for units `2π/m`, `m` even.
-/

namespace KeyOrder

open Real

/-- (a) Order of `J * u + ψ` is the lexicographic order of `(J, ψ)`. -/
theorem cell_lt_iff {u : ℝ} (hu : 0 < u) (J₁ J₂ : ℤ) {ψ₁ ψ₂ : ℝ}
    (h₁0 : 0 ≤ ψ₁) (h₁u : ψ₁ < u) (h₂0 : 0 ≤ ψ₂) (h₂u : ψ₂ < u) :
    (J₁ : ℝ) * u + ψ₁ < (J₂ : ℝ) * u + ψ₂ ↔ J₁ < J₂ ∨ (J₁ = J₂ ∧ ψ₁ < ψ₂) := by
  constructor
  · intro h
    rcases lt_trichotomy J₁ J₂ with hlt | heq | hgt
    · exact Or.inl hlt
    · subst heq
      exact Or.inr ⟨rfl, by linarith⟩
    · exfalso
      have h' : J₂ + 1 ≤ J₁ := hgt
      have h'' : (J₂ : ℝ) + 1 ≤ J₁ := by exact_mod_cast h'
      have := mul_le_mul_of_nonneg_right h'' hu.le
      linarith
  · rintro (hlt | ⟨rfl, hψ⟩)
    · have h' : J₁ + 1 ≤ J₂ := hlt
      have h'' : (J₁ : ℝ) + 1 ≤ J₂ := by exact_mod_cast h'
      have := mul_le_mul_of_nonneg_right h'' hu.le
      linarith
    · linarith

/-- (a') Equality of directions is equality of `(J, ψ)`. -/
theorem cell_eq_iff {u : ℝ} (hu : 0 < u) (J₁ J₂ : ℤ) {ψ₁ ψ₂ : ℝ}
    (h₁0 : 0 ≤ ψ₁) (h₁u : ψ₁ < u) (h₂0 : 0 ≤ ψ₂) (h₂u : ψ₂ < u) :
    (J₁ : ℝ) * u + ψ₁ = (J₂ : ℝ) * u + ψ₂ ↔ J₁ = J₂ ∧ ψ₁ = ψ₂ := by
  constructor
  · intro h
    have n1 := (cell_lt_iff hu J₁ J₂ h₁0 h₁u h₂0 h₂u).not.mp (lt_irrefl _ |> fun hh => by
      intro hlt; rw [h] at hlt; exact hh hlt)
    have n2 := (cell_lt_iff hu J₂ J₁ h₂0 h₂u h₁0 h₁u).not.mp (lt_irrefl _ |> fun hh => by
      intro hlt; rw [h] at hlt; exact hh hlt)
    push_neg at n1 n2
    have hJ : J₁ = J₂ := le_antisymm n2.1 n1.1
    exact ⟨hJ, le_antisymm (n2.2 hJ.symm) (n1.2 hJ)⟩
  · rintro ⟨rfl, rfl⟩
    rfl

/-- (b) With `rank` strictly monotone on the set `S` of phases, the order of the directions
is the lexicographic order of the integer keys `(J, rank ψ)`. -/
theorem cell_lt_iff_rank {u : ℝ} (hu : 0 < u) {S : Set ℝ} (rank : ℝ → ℕ)
    (hrank : StrictMonoOn rank S) (J₁ J₂ : ℤ) {ψ₁ ψ₂ : ℝ} (hS₁ : ψ₁ ∈ S) (hS₂ : ψ₂ ∈ S)
    (h₁0 : 0 ≤ ψ₁) (h₁u : ψ₁ < u) (h₂0 : 0 ≤ ψ₂) (h₂u : ψ₂ < u) :
    (J₁ : ℝ) * u + ψ₁ < (J₂ : ℝ) * u + ψ₂ ↔
      toLex (J₁, rank ψ₁) < toLex (J₂, rank ψ₂) := by
  rw [cell_lt_iff hu J₁ J₂ h₁0 h₁u h₂0 h₂u, Prod.Lex.lt_iff]
  simp only [ofLex_toLex, hrank.lt_iff_lt hS₁ hS₂]

/-- (b') Same with a finite set of phases given as a `Finset`. -/
theorem cell_lt_iff_rank_finset {u : ℝ} (hu : 0 < u) (S : Finset ℝ) (rank : ℝ → ℕ)
    (hrank : StrictMonoOn rank (S : Set ℝ)) (J₁ J₂ : ℤ) {ψ₁ ψ₂ : ℝ} (hS₁ : ψ₁ ∈ S)
    (hS₂ : ψ₂ ∈ S) (h₁0 : 0 ≤ ψ₁) (h₁u : ψ₁ < u) (h₂0 : 0 ≤ ψ₂) (h₂u : ψ₂ < u) :
    (J₁ : ℝ) * u + ψ₁ < (J₂ : ℝ) * u + ψ₂ ↔
      toLex (J₁, rank ψ₁) < toLex (J₂, rank ψ₂) :=
  cell_lt_iff_rank hu rank hrank J₁ J₂ (Finset.mem_coe.mpr hS₁) (Finset.mem_coe.mpr hS₂)
    h₁0 h₁u h₂0 h₂u

/-- (c0) Reduction mod `2π` into `[0, 2π)`: when `N * u = 2π`, the direction `J * u + ψ`
reduces to `(J % N) * u + ψ`. -/
theorem reduce_mod_two_pi {N : ℤ} (hN : 0 < N) {u : ℝ} (hu : 0 < u)
    (hNu : (N : ℝ) * u = 2 * π) (J : ℤ) {ψ : ℝ} (h0 : 0 ≤ ψ) (h1 : ψ < u) :
    toIcoMod Real.two_pi_pos 0 ((J : ℝ) * u + ψ) = ((J % N : ℤ) : ℝ) * u + ψ := by
  rw [toIcoMod_eq_iff]
  refine ⟨⟨?_, ?_⟩, J / N, ?_⟩
  · have h : (0 : ℝ) ≤ ((J % N : ℤ) : ℝ) := by exact_mod_cast Int.emod_nonneg J hN.ne'
    have := mul_nonneg h hu.le
    linarith
  · have h : J % N + 1 ≤ N := Int.emod_lt_of_pos J hN
    have h' : ((J % N : ℤ) : ℝ) + 1 ≤ N := by exact_mod_cast h
    have := mul_le_mul_of_nonneg_right h' hu.le
    linarith
  · rw [zsmul_eq_mul, ← hNu]
    have h : ((J % N : ℤ) : ℝ) + (N : ℝ) * ((J / N : ℤ) : ℝ) = J := by
      exact_mod_cast Int.emod_add_mul_ediv J N
    linear_combination (-u) * h

/-- (c1) Antipode for units `π/m` (cells mod `2m`; used for odd `m`, oddness not needed):
`θ + π` reduced mod `2π` has cell `(J + m) % (2m)` and the same phase. -/
theorem antipode_odd {m : ℕ} (hm : 0 < m) (J : ℤ) {ψ : ℝ} (h0 : 0 ≤ ψ) (h1 : ψ < π / m) :
    toIcoMod Real.two_pi_pos 0 ((J : ℝ) * (π / m) + ψ + π) =
      (((J + m) % (2 * m) : ℤ) : ℝ) * (π / m) + ψ := by
  have hm' : (m : ℝ) ≠ 0 := by exact_mod_cast hm.ne'
  have hθ : (J : ℝ) * (π / m) + ψ + π = ((J + m : ℤ) : ℝ) * (π / m) + ψ := by
    push_cast
    field_simp
    ring
  rw [hθ]
  refine reduce_mod_two_pi (N := 2 * m) (by positivity) (by positivity) ?_ _ h0 h1
  push_cast
  field_simp

/-- (c2) Antipode for units `2π/m` with `m` even (cells mod `m`): `θ + π` reduced mod `2π`
has cell `(J + m/2) % m` and the same phase. -/
theorem antipode_even {m : ℕ} (hm : 0 < m) (he : Even m) (J : ℤ) {ψ : ℝ} (h0 : 0 ≤ ψ)
    (h1 : ψ < 2 * π / m) :
    toIcoMod Real.two_pi_pos 0 ((J : ℝ) * (2 * π / m) + ψ + π) =
      (((J + (m / 2 : ℕ)) % m : ℤ) : ℝ) * (2 * π / m) + ψ := by
  obtain ⟨k, rfl⟩ := he
  have hk : (k + k) / 2 = k := by omega
  rw [hk] at *
  have hm' : ((k + k : ℕ) : ℝ) ≠ 0 := by exact_mod_cast hm.ne'
  have hk' : (k : ℝ) ≠ 0 := by
    have : k ≠ 0 := by omega
    exact_mod_cast this
  have hθ : (J : ℝ) * (2 * π / (k + k : ℕ)) + ψ + π =
      ((J + k : ℤ) : ℝ) * (2 * π / (k + k : ℕ)) + ψ := by
    push_cast
    field_simp
    ring
  rw [hθ]
  refine reduce_mod_two_pi (N := ((k + k : ℕ) : ℤ)) (by exact_mod_cast hm) (by positivity)
    ?_ _ h0 h1
  push_cast
  field_simp

/-- (d) Combined: after reduction mod `2π` (cells mod `N`, `N * u = 2π`), the order of the
reduced directions is the lexicographic order of the keys `(J % N, rank ψ)`. -/
theorem reduced_lt_iff_key {N : ℤ} (hN : 0 < N) {u : ℝ} (hu : 0 < u)
    (hNu : (N : ℝ) * u = 2 * π) {S : Set ℝ} (rank : ℝ → ℕ) (hrank : StrictMonoOn rank S)
    (J₁ J₂ : ℤ) {ψ₁ ψ₂ : ℝ} (hS₁ : ψ₁ ∈ S) (hS₂ : ψ₂ ∈ S)
    (h₁0 : 0 ≤ ψ₁) (h₁u : ψ₁ < u) (h₂0 : 0 ≤ ψ₂) (h₂u : ψ₂ < u) :
    toIcoMod Real.two_pi_pos 0 ((J₁ : ℝ) * u + ψ₁) <
        toIcoMod Real.two_pi_pos 0 ((J₂ : ℝ) * u + ψ₂) ↔
      toLex (J₁ % N, rank ψ₁) < toLex (J₂ % N, rank ψ₂) := by
  rw [reduce_mod_two_pi hN hu hNu J₁ h₁0 h₁u, reduce_mod_two_pi hN hu hNu J₂ h₂0 h₂u]
  exact cell_lt_iff_rank hu rank hrank _ _ hS₁ hS₂ h₁0 h₁u h₂0 h₂u

end KeyOrder

#print axioms KeyOrder.cell_lt_iff
#print axioms KeyOrder.cell_eq_iff
#print axioms KeyOrder.cell_lt_iff_rank
#print axioms KeyOrder.cell_lt_iff_rank_finset
#print axioms KeyOrder.reduce_mod_two_pi
#print axioms KeyOrder.antipode_odd
#print axioms KeyOrder.antipode_even
#print axioms KeyOrder.reduced_lt_iff_key
