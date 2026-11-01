import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Prod
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Algebra.GroupWithZero.Basic
import Mathlib.Algebra.Ring.Parity
import Mathlib.Tactic.Ring

/-!
# Claim P-compat: `2^(m-1)` points and `m`-fold rotational symmetry

Independent check written for primefold / verify_literature_P-compat (2026-11-02).

Model of the plane: a commutative group with zero `K` (in the application `K = ℂ`), centre `0`, and the rotation by
`2π/m` acting as `z ↦ ζ * z`, where `ζ ^ m = 1` and `ζ ^ j ≠ 1` for `0 < j < m`. For `ζ = exp (2πi/m)` these two facts
are Mathlib's `Complex.isPrimitiveRoot_exp` (not imported here to stay under the memory cap). A rotation about another
centre `c` reduces to this case by translating by `-c`.

Contents
* `dvd_card`, `card_mod`: the orbit lemma (a finite rotation-invariant set has size `≡ [0 ∈ S] (mod m)`).
* `exists_card0`, `exists_card1`, `exists_iff`: the converse, given `t` orbits with distinct radii.
* `compat_even`, `compat_odd`, `classification`: the arithmetic of `2^(m-1) mod m ∈ {0, 1}`.
* `ex341`: the example m = 341. (The pseudoprime list below 3000 is checked in Python, compat_check.py.)
Not formalized: Fermat's little theorem (all odd primes are compatible; textbook). It is confirmed numerically for
every odd prime below 200000 in ../compat_check.py, which also checks the pseudoprime list below 3000.
-/

namespace PCompat

open Finset

section Orbit

variable {K : Type*} [CommGroupWithZero K] [DecidableEq K] {m : ℕ} {ζ : K}

omit [DecidableEq K] in
lemma ne_zero_of_order (hm : 0 < m) (hζm : ζ ^ m = 1) : ζ ≠ 0 := by
  rintro rfl
  rw [zero_pow hm.ne'] at hζm
  exact zero_ne_one hζm

omit [DecidableEq K] in
/-- Powers of `ζ` below its order are pairwise distinct. -/
lemma pow_inj_of_order (hm : 0 < m) (hζm : ζ ^ m = 1) (hprim : ∀ j, 0 < j → j < m → ζ ^ j ≠ 1)
    {i j : ℕ} (hi : i < m) (hj : j < m) (h : ζ ^ i = ζ ^ j) : i = j := by
  have hζ0 := ne_zero_of_order hm hζm
  rcases Nat.lt_trichotomy i j with hij | hij | hij
  · exfalso
    apply hprim (j - i) (by omega) (by omega)
    apply mul_left_cancel₀ (pow_ne_zero i hζ0)
    rw [← pow_add, Nat.add_sub_of_le hij.le, mul_one, h]
  · exact hij
  · exfalso
    apply hprim (i - j) (by omega) (by omega)
    apply mul_left_cancel₀ (pow_ne_zero j hζ0)
    rw [← pow_add, Nat.add_sub_of_le hij.le, mul_one, h]

omit [DecidableEq K] in
lemma pow_mul_mem {T : Finset K} (hinv : ∀ z ∈ T, ζ * z ∈ T) {z : K} (hz : z ∈ T) :
    ∀ j : ℕ, ζ ^ j * z ∈ T
  | 0 => by simpa using hz
  | j + 1 => by
      have h := hinv _ (pow_mul_mem hinv hz j)
      rwa [show ζ * (ζ ^ j * z) = ζ ^ (j + 1) * z by rw [pow_succ', mul_assoc]] at h

/-- **Orbit lemma.** A finite set that avoids the centre and is closed under the rotation has size divisible by
`m`: it is a disjoint union of orbits `{ζ ^ j * z : j < m}`, each of size exactly `m`. -/
theorem dvd_card (hm : 0 < m) (hζm : ζ ^ m = 1) (hprim : ∀ j, 0 < j → j < m → ζ ^ j ≠ 1) :
    ∀ T : Finset K, (0 : K) ∉ T → (∀ z ∈ T, ζ * z ∈ T) → m ∣ T.card := by
  have hζ0 := ne_zero_of_order hm hζm
  intro T
  induction T using Finset.strongInduction
  next T ih =>
  intro h0 hinv
  rcases T.eq_empty_or_nonempty with hT | ⟨z, hz⟩
  · simp [hT]
  have hz0 : z ≠ 0 := fun h => h0 (h ▸ hz)
  set O : Finset K := (range m).image (fun j => ζ ^ j * z) with hOdef
  have hOT : O ⊆ T := by
    intro w hw
    obtain ⟨j, -, rfl⟩ := mem_image.mp hw
    exact pow_mul_mem hinv hz j
  have hOcard : O.card = m := by
    rw [hOdef, card_image_of_injOn, card_range]
    intro i hi j hj hij
    simp only [coe_range, Set.mem_Iio] at hi hj
    exact pow_inj_of_order hm hζm hprim hi hj (mul_right_cancel₀ hz0 hij)
  have hzO : z ∈ O := mem_image.mpr ⟨0, mem_range.mpr hm, by simp⟩
  have hsub : T \ O ⊂ T := ⟨sdiff_subset, fun h => (mem_sdiff.mp (h hz)).2 hzO⟩
  have hrest : m ∣ (T \ O).card := by
    refine ih _ hsub (fun h => h0 (mem_sdiff.mp h).1) ?_
    intro w hw
    rw [mem_sdiff] at hw ⊢
    refine ⟨hinv w hw.1, fun hwO => hw.2 ?_⟩
    obtain ⟨j, hj, hjeq⟩ := mem_image.mp hwO
    rw [mem_range] at hj
    change ζ ^ j * z = ζ * w at hjeq
    rcases j with _ | j
    · refine mem_image.mpr ⟨m - 1, mem_range.mpr (by omega), ?_⟩
      change ζ ^ (m - 1) * z = w
      rw [pow_zero, one_mul] at hjeq
      rw [hjeq, ← mul_assoc, ← pow_succ, Nat.sub_add_cancel (by omega : 1 ≤ m), hζm, one_mul]
    · refine mem_image.mpr ⟨j, mem_range.mpr (by omega), ?_⟩
      change ζ ^ j * z = w
      apply mul_left_cancel₀ hζ0
      rw [← hjeq, pow_succ', mul_assoc]
  have hcard : T.card = (T \ O).card + m := by
    rw [← hOcard, card_sdiff_add_card_eq_card hOT]
  rw [hcard]
  exact Nat.dvd_add hrest (Nat.dvd_refl m)

/-- Corollary: `|S| ≡ 1 (mod m)` if the centre is in `S`, and `|S| ≡ 0 (mod m)` otherwise. -/
theorem card_mod (hm : 0 < m) (hζm : ζ ^ m = 1) (hprim : ∀ j, 0 < j → j < m → ζ ^ j ≠ 1)
    (S : Finset K) (hinv : ∀ z ∈ S, ζ * z ∈ S) :
    S.card % m = (if (0 : K) ∈ S then 1 else 0) % m := by
  have hζ0 := ne_zero_of_order hm hζm
  have hT : m ∣ (S.erase 0).card := by
    refine dvd_card hm hζm hprim _ (notMem_erase 0 S) ?_
    intro z hz
    rw [mem_erase] at hz ⊢
    exact ⟨mul_ne_zero hζ0 hz.1, hinv z hz.2⟩
  obtain ⟨t, ht⟩ := hT
  by_cases h0 : (0 : K) ∈ S
  · rw [if_pos h0, ← card_erase_add_one h0, ht, Nat.mul_add_mod]
  · rw [if_neg h0, ← erase_eq_of_notMem h0, ht, Nat.mul_mod_right, Nat.zero_mod]

variable (r : ℕ → K)

/-- Converse, without the centre: `t` orbits of pairwise distinct radii give `m * t` points. -/
theorem exists_card0 (hm : 0 < m) (hζm : ζ ^ m = 1) (hprim : ∀ j, 0 < j → j < m → ζ ^ j ≠ 1)
    (hr0 : ∀ i, r i ≠ 0) (hdisj : ∀ i i' j j', j < m → j' < m → ζ ^ j * r i = ζ ^ j' * r i' → i = i')
    (t : ℕ) : ∃ S : Finset K, (∀ z ∈ S, ζ * z ∈ S) ∧ (0 : K) ∉ S ∧ S.card = m * t := by
  have hζ0 := ne_zero_of_order hm hζm
  refine ⟨(range m ×ˢ range t).image (fun p => ζ ^ p.1 * r p.2), ?_, ?_, ?_⟩
  · intro z hz
    obtain ⟨⟨j, i⟩, hp, rfl⟩ := mem_image.mp hz
    rw [mem_product, mem_range, mem_range] at hp
    by_cases hj : j + 1 < m
    · refine mem_image.mpr ⟨(j + 1, i), ?_, ?_⟩
      · rw [mem_product, mem_range, mem_range]; exact ⟨hj, hp.2⟩
      · change ζ ^ (j + 1) * r i = ζ * (ζ ^ j * r i)
        rw [pow_succ', mul_assoc]
    · have hjm : j + 1 = m := by omega
      refine mem_image.mpr ⟨(0, i), ?_, ?_⟩
      · rw [mem_product, mem_range, mem_range]; exact ⟨hm, hp.2⟩
      · change ζ ^ 0 * r i = ζ * (ζ ^ j * r i)
        rw [pow_zero, one_mul, ← mul_assoc, ← pow_succ', hjm, hζm, one_mul]
  · intro h
    obtain ⟨⟨j, i⟩, -, hji⟩ := mem_image.mp h
    exact mul_ne_zero (pow_ne_zero j hζ0) (hr0 i) hji
  · rw [card_image_of_injOn, card_product, card_range, card_range]
    rintro ⟨j, i⟩ hp ⟨j', i'⟩ hp' h
    simp only [coe_product, coe_range, Set.mem_prod, Set.mem_Iio] at hp hp'
    change ζ ^ j * r i = ζ ^ j' * r i' at h
    have hii : i = i' := hdisj i i' j j' hp.1 hp'.1 h
    subst hii
    have hjj : ζ ^ j = ζ ^ j' := mul_right_cancel₀ (hr0 i) h
    rw [pow_inj_of_order hm hζm hprim hp.1 hp'.1 hjj]

/-- Converse, with the centre: `m * t + 1` points. -/
theorem exists_card1 (hm : 0 < m) (hζm : ζ ^ m = 1) (hprim : ∀ j, 0 < j → j < m → ζ ^ j ≠ 1)
    (hr0 : ∀ i, r i ≠ 0) (hdisj : ∀ i i' j j', j < m → j' < m → ζ ^ j * r i = ζ ^ j' * r i' → i = i')
    (t : ℕ) : ∃ S : Finset K, (∀ z ∈ S, ζ * z ∈ S) ∧ S.card = m * t + 1 := by
  obtain ⟨S, hS, h0, hc⟩ := exists_card0 r hm hζm hprim hr0 hdisj t
  refine ⟨insert 0 S, ?_, ?_⟩
  · intro z hz
    rw [mem_insert] at hz ⊢
    rcases hz with rfl | hz
    · exact Or.inl (mul_zero ζ)
    · exact Or.inr (hS z hz)
  · rw [card_insert_of_notMem h0, hc]

/-- **Size compatibility, both directions.** A finite rotation-invariant set of `N` points exists iff
`N mod m ∈ {0, 1 mod m}`. -/
theorem exists_iff (hm : 0 < m) (hζm : ζ ^ m = 1) (hprim : ∀ j, 0 < j → j < m → ζ ^ j ≠ 1)
    (hr0 : ∀ i, r i ≠ 0) (hdisj : ∀ i i' j j', j < m → j' < m → ζ ^ j * r i = ζ ^ j' * r i' → i = i')
    (N : ℕ) : (∃ S : Finset K, (∀ z ∈ S, ζ * z ∈ S) ∧ S.card = N) ↔ (N % m = 0 ∨ N % m = 1 % m) := by
  constructor
  · rintro ⟨S, hinv, rfl⟩
    have h := card_mod hm hζm hprim S hinv
    by_cases h0 : (0 : K) ∈ S
    · rw [if_pos h0] at h
      exact Or.inr h
    · rw [if_neg h0, Nat.zero_mod] at h
      exact Or.inl h
  · intro h
    have hdm := Nat.div_add_mod N m
    by_cases hN : N % m = 0
    · obtain ⟨S, hS, -, hc⟩ := exists_card0 r hm hζm hprim hr0 hdisj (N / m)
      exact ⟨S, hS, by omega⟩
    · have h1 : N % m = 1 % m := h.resolve_left hN
      have hm1 : 1 < m := by
        by_contra hle
        have hm1' : m = 1 := by omega
        subst hm1'
        exact hN (Nat.mod_one N)
      rw [Nat.mod_eq_of_lt hm1] at h1
      obtain ⟨S, hS, hc⟩ := exists_card1 r hm hζm hprim hr0 hdisj (N / m)
      exact ⟨S, hS, by omega⟩

end Orbit

/-! ## Arithmetic of `N = 2^(m-1)` -/

/-- `N` points are size-compatible with `m`-fold rotational symmetry. -/
def Compat (m N : ℕ) : Prop := N % m = 0 ∨ N % m = 1 % m

/-- Even `m`: compatible iff `m` is a power of two (`m = 2, 4, 8, …`, i.e. `k = 3, 5, 9, 17, …`). -/
theorem compat_even {m : ℕ} (h2 : 2 ≤ m) (he : Even m) :
    Compat m (2 ^ (m - 1)) ↔ ∃ a, 1 ≤ a ∧ m = 2 ^ a := by
  have h1m : 1 % m = 1 := Nat.mod_eq_of_lt (by omega)
  unfold Compat
  rw [h1m]
  constructor
  · rintro (h | h)
    · obtain ⟨a, -, ha⟩ := (Nat.dvd_prime_pow Nat.prime_two).mp (Nat.dvd_of_mod_eq_zero h)
      refine ⟨a, ?_, ha⟩
      rcases Nat.eq_zero_or_pos a with rfl | hpos
      · rw [pow_zero] at ha; omega
      · exact hpos
    · exfalso
      obtain ⟨r, hr⟩ := he
      have h2m : 2 ∣ m := ⟨r, by omega⟩
      have hA : 2 ^ (m - 1) % 2 = 1 := by
        rw [← Nat.mod_mod_of_dvd _ h2m, h]
      have hB : 2 ^ (m - 1) % 2 = 0 := Nat.mod_eq_zero_of_dvd (dvd_pow_self 2 (by omega))
      omega
  · rintro ⟨a, ha, rfl⟩
    left
    apply Nat.mod_eq_zero_of_dvd
    apply Nat.pow_dvd_pow 2
    have : a < 2 ^ a := Nat.lt_two_pow_self
    omega

/-- Odd `m ≥ 3`: residue `0` is impossible, so compatible iff `2^(m-1) ≡ 1 (mod m)`. -/
theorem compat_odd {m : ℕ} (h3 : 3 ≤ m) (ho : Odd m) :
    Compat m (2 ^ (m - 1)) ↔ 2 ^ (m - 1) % m = 1 := by
  have h1m : 1 % m = 1 := Nat.mod_eq_of_lt (by omega)
  unfold Compat
  rw [h1m]
  constructor
  · rintro (h | h)
    · exfalso
      obtain ⟨a, -, ha⟩ := (Nat.dvd_prime_pow Nat.prime_two).mp (Nat.dvd_of_mod_eq_zero h)
      obtain ⟨r, hr⟩ := ho
      rcases a with _ | a
      · rw [pow_zero] at ha; omega
      · rw [pow_succ] at ha; omega
    · exact h
  · exact Or.inr

/-- The complete classification for every `m ≥ 1`: `m = 1`, or `m` a power of two `≥ 2`, or `m` odd `≥ 3` with
`2^(m-1) ≡ 1 (mod m)` (odd primes, by Fermat, and base-2 Fermat pseudoprimes, by definition). -/
theorem classification (m : ℕ) (hm : 1 ≤ m) :
    Compat m (2 ^ (m - 1)) ↔
      m = 1 ∨ (∃ a, 1 ≤ a ∧ m = 2 ^ a) ∨ (Odd m ∧ 3 ≤ m ∧ 2 ^ (m - 1) % m = 1) := by
  rcases Nat.even_or_odd m with he | ho
  · have h2 : 2 ≤ m := by obtain ⟨r, hr⟩ := he; omega
    rw [compat_even h2 he]
    constructor
    · intro h; exact Or.inr (Or.inl h)
    · rintro (h | h | ⟨hodd, -, -⟩)
      · omega
      · exact h
      · exact absurd he (Nat.not_even_iff_odd.mpr hodd)
  · rcases (show m = 1 ∨ 3 ≤ m by obtain ⟨r, hr⟩ := ho; omega) with rfl | h3
    · exact ⟨fun _ => Or.inl rfl, fun _ => Or.inl (by decide)⟩
    · rw [compat_odd h3 ho]
      constructor
      · intro h; exact Or.inr (Or.inr ⟨ho, h3, h⟩)
      · rintro (h | ⟨a, ha, rfl⟩ | ⟨-, -, h⟩)
        · omega
        · exact absurd (Nat.even_pow.mpr ⟨even_two, by omega⟩) (Nat.not_even_iff_odd.mpr ho)
        · exact h

set_option exponentiation.threshold 400 in
/-- The example `m = 341 = 11 * 31` (`k = 342`). -/
theorem ex341 : Compat 341 (2 ^ (341 - 1)) ∧ 341 = 11 * 31 ∧ ¬ Nat.Prime 341 ∧
    2 ^ 10 % 11 = 1 ∧ 2 ^ 10 % 31 = 1 ∧ 2 ^ 10 % 341 = 1 := by
  refine ⟨Or.inr (by decide), by decide, ?_, by decide, by decide, by decide⟩
  rw [show (341 : ℕ) = 11 * 31 by decide]
  exact Nat.not_prime_mul (by decide) (by decide)

end PCompat

#print axioms PCompat.dvd_card
#print axioms PCompat.card_mod
#print axioms PCompat.exists_iff
#print axioms PCompat.compat_even
#print axioms PCompat.compat_odd
#print axioms PCompat.classification
#print axioms PCompat.ex341
