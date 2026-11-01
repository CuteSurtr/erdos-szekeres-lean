import Mathlib.NumberTheory.FermatPsp
import Mathlib.RingTheory.RootsOfUnity.Complex
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Tactic.Ring

/-!
Independent Lean check of claim L0 (primefold/theory PROOFS.md, Lemma 0).

The plane is modelled by `ℂ`; the rotation by `2π/m` about the centre `O = 0` is multiplication by a
primitive `m`-th root of unity `ζ` (for instance `exp (2πi/m)`, see `L0_rot`).  No general-position
hypothesis is assumed anywhere: for even `m` the centre is excluded by parity alone.
"Base-2 Fermat pseudoprime" is Mathlib's `Nat.FermatPsp m 2` (`m ∣ 2^(m-1) - 1`, `m` composite, `1 < m`).
-/

namespace L0Check

open Finset

/-- Arithmetic core: `m * t + e = 2^(m-1)` with `e ≤ 1`, `m ≥ 2` forces either
(`m` odd, `e = 1`, `m` prime or a base-2 Fermat pseudoprime) or (`e = 0`, `m` a power of two). -/
theorem arith (m t e : ℕ) (hm : 2 ≤ m) (he : e ≤ 1) (h : m * t + e = 2 ^ (m - 1)) :
    (Odd m ∧ e = 1 ∧ (m.Prime ∨ Nat.FermatPsp m 2)) ∨ (e = 0 ∧ ∃ j, m = 2 ^ j) := by
  rcases Nat.even_or_odd m with hev | hodd
  · right
    have h2 : Even (2 ^ (m - 1)) := (Nat.even_pow' (by omega)).2 even_two
    have hmt : Even (m * t) := hev.mul_right t
    have he0 : e = 0 := by
      rcases Nat.even_or_odd e with hee | heo
      · obtain ⟨r, hr⟩ := hee
        omega
      · exfalso
        have hodd' : Odd (m * t + e) := hmt.add_odd heo
        rw [h] at hodd'
        exact (Nat.not_even_iff_odd.2 hodd') h2
    refine ⟨he0, ?_⟩
    have hdvd : m ∣ 2 ^ (m - 1) := ⟨t, by rw [← h, he0, add_zero]⟩
    obtain ⟨i, -, hi⟩ := (Nat.dvd_prime_pow Nat.prime_two).1 hdvd
    exact ⟨i, hi⟩
  · left
    have he1 : e = 1 := by
      by_contra hne
      have he0 : e = 0 := by omega
      have hdvd : m ∣ 2 ^ (m - 1) := ⟨t, by rw [← h, he0, add_zero]⟩
      obtain ⟨i, -, hi⟩ := (Nat.dvd_prime_pow Nat.prime_two).1 hdvd
      cases i with
      | zero => simp at hi; omega
      | succ i =>
        rw [hi, pow_succ] at hodd
        exact (Nat.not_even_iff_odd.2 hodd) (even_two.mul_left _)
    refine ⟨hodd, he1, ?_⟩
    by_cases hp : m.Prime
    · exact Or.inl hp
    · right
      refine ⟨?_, hp, by omega⟩
      show m ∣ 2 ^ (m - 1) - 1
      exact ⟨t, by rw [← h, he1, Nat.add_sub_cancel]⟩

/-- Orbit counting: a finite set of non-zero complex numbers that is invariant under multiplication by a
primitive `m`-th root of unity has cardinality divisible by `m` (every orbit has exactly `m` points). -/
theorem orbit_dvd (m : ℕ) (hm : 0 < m) (ζ : ℂ) (hζ : IsPrimitiveRoot ζ m) :
    ∀ T : Finset ℂ, (0 : ℂ) ∉ T → (∀ z ∈ T, ζ * z ∈ T) → m ∣ T.card := by
  intro T
  induction T using Finset.strongInduction with
  | H T ih =>
    intro h0 hT
    rcases T.eq_empty_or_nonempty with hE | ⟨z, hz⟩
    · simp [hE]
    have hz0 : z ≠ 0 := fun h => h0 (h ▸ hz)
    have hζ0 : ζ ≠ 0 := hζ.ne_zero (by omega)
    have hpow : ∀ k : ℕ, ζ ^ k * z ∈ T := by
      intro k
      induction k with
      | zero => simpa using hz
      | succ k ihk =>
        have h1 := hT _ ihk
        have h2 : ζ ^ (k + 1) * z = ζ * (ζ ^ k * z) := by ring
        rw [h2]
        exact h1
    set O : Finset ℂ := (Finset.range m).image (fun k => ζ ^ k * z) with hO
    have hOT : O ⊆ T := by
      intro w hw
      rw [hO, Finset.mem_image] at hw
      obtain ⟨k, -, rfl⟩ := hw
      exact hpow k
    have hOcard : O.card = m := by
      rw [hO, Finset.card_image_of_injOn, Finset.card_range]
      intro i hi j hj hij
      simp only [Finset.coe_range, Set.mem_Iio] at hi hj
      have hij' : ζ ^ i = ζ ^ j := mul_right_cancel₀ hz0 hij
      exact hζ.pow_inj hi hj hij'
    have hinv : ∀ w ∈ T \ O, ζ * w ∈ T \ O := by
      intro w hw
      rw [Finset.mem_sdiff] at hw ⊢
      refine ⟨hT w hw.1, ?_⟩
      intro hmem
      apply hw.2
      rw [hO, Finset.mem_image] at hmem ⊢
      obtain ⟨k, hk, hkw⟩ := hmem
      rw [Finset.mem_range] at hk
      rcases k with _ | k
      · refine ⟨m - 1, Finset.mem_range.2 (by omega), ?_⟩
        simp only [pow_zero, one_mul] at hkw
        rw [hkw, ← mul_assoc, ← pow_succ, Nat.sub_add_cancel (by omega : 1 ≤ m), hζ.pow_eq_one,
          one_mul]
      · refine ⟨k, Finset.mem_range.2 (by omega), ?_⟩
        have h3 : ζ ^ (k + 1) * z = ζ * (ζ ^ k * z) := by ring
        rw [h3] at hkw
        exact mul_left_cancel₀ hζ0 hkw
    have hOne : O.Nonempty := ⟨z, by
      rw [hO, Finset.mem_image]
      exact ⟨0, Finset.mem_range.2 hm, by simp⟩⟩
    have hsub : T \ O ⊂ T := Finset.sdiff_ssubset hOT hOne
    have hcard : (T \ O).card + m = T.card := by
      rw [← hOcard, Finset.card_sdiff_add_card_eq_card hOT]
    have h0' : (0 : ℂ) ∉ T \ O := fun h => h0 (Finset.mem_sdiff.1 h).1
    obtain ⟨c, hc⟩ := ih (T \ O) hsub h0' hinv
    exact ⟨c + 1, by rw [← hcard, hc]; ring⟩

/-- Claim L0: an `m`-fold rotationally symmetric finite set (`m ≥ 2`, centre `0`) with exactly `2^(m-1)`
points forces either (`m` odd, centre in the set, `m` prime or base-2 Fermat pseudoprime) or (centre not
in the set, `m` a power of two). No general position assumed. -/
theorem L0 (m : ℕ) (hm : 2 ≤ m) (ζ : ℂ) (hζ : IsPrimitiveRoot ζ m) (S : Finset ℂ)
    (hS : ∀ z ∈ S, ζ * z ∈ S) (hcard : S.card = 2 ^ (m - 1)) :
    (Odd m ∧ (0 : ℂ) ∈ S ∧ (m.Prime ∨ Nat.FermatPsp m 2)) ∨ ((0 : ℂ) ∉ S ∧ ∃ j, m = 2 ^ j) := by
  have hζ0 : ζ ≠ 0 := hζ.ne_zero (by omega)
  have hinv : ∀ z ∈ S.erase 0, ζ * z ∈ S.erase 0 := by
    intro z hz
    rw [Finset.mem_erase] at hz ⊢
    exact ⟨mul_ne_zero hζ0 hz.1, hS z hz.2⟩
  obtain ⟨t, ht⟩ := orbit_dvd m (by omega) ζ hζ (S.erase 0) (Finset.notMem_erase 0 S) hinv
  by_cases h0 : (0 : ℂ) ∈ S
  · have hc := Finset.card_erase_add_one h0
    have h1 : m * t + 1 = 2 ^ (m - 1) := by rw [← ht, hc, hcard]
    rcases arith m t 1 hm le_rfl h1 with ⟨hodd, -, hp⟩ | ⟨h10, -⟩
    · exact Or.inl ⟨hodd, h0, hp⟩
    · exact absurd h10 one_ne_zero
  · have hc : S.erase 0 = S := Finset.erase_eq_of_notMem h0
    have h1 : m * t + 0 = 2 ^ (m - 1) := by rw [add_zero, ← ht, hc, hcard]
    rcases arith m t 0 hm (Nat.zero_le _) h1 with ⟨-, h01, -⟩ | ⟨-, hj⟩
    · exact absurd h01 zero_ne_one
    · exact Or.inr ⟨h0, hj⟩

/-- The same statement for the rotation by `2π/m` about `0`, i.e. multiplication by `exp (2πi/m)`. -/
theorem L0_rot (m : ℕ) (hm : 2 ≤ m) (S : Finset ℂ)
    (hS : ∀ z ∈ S, Complex.exp (2 * Real.pi * Complex.I / m) * z ∈ S)
    (hcard : S.card = 2 ^ (m - 1)) :
    (Odd m ∧ (0 : ℂ) ∈ S ∧ (m.Prime ∨ Nat.FermatPsp m 2)) ∨ ((0 : ℂ) ∉ S ∧ ∃ j, m = 2 ^ j) :=
  L0 m hm _ (Complex.isPrimitiveRoot_exp m (by omega)) S hS hcard

end L0Check

#print axioms L0Check.L0_rot
