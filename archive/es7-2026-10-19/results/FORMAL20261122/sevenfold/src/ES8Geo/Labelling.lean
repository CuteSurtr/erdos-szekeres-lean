import ES8Geo.Interface

/-! # M5: a polar labelling of a counterexample (DESIGN.md §3.3, F1-F8)

From a `ρ`-invariant set `T` in general position (`ρ = rotAbout c (2π/m)`, `m` even, `c ∉ T`,
no convex `K`-gon, `K ≤ 2m`) with `|T| = m·t` we build a `PolarLabelling m t T c`.

* F1: `peel T n` is nonempty for `n < t` (`card_peel`).
* F2-F4: a hull vertex `xₙ = polar c Rₙ θₙ` of `peel T n` (`hullVerts_nonempty`, `exists_angle`,
  `sqrt_dist2_pos`); its rotations `polar c Rₙ (θₙ + k·u)` (`u = 2π/m`) are hull vertices too
  (`iterate_mem_hullVerts_peel`, `rotAbout_iterate`, `rotAbout_polar`), also for `k : ℤ`
  (`polar_add_int`).
* F5: `ψₙ := toIcoMod u 0 (θₙ - θ₀)` and `φ := θ₀`.
* F6: `mem_layer`; F7: `ψ` distinct and positive off layer 0 (`phase_ne_of_distinct_layers`);
  F8: `r_anti` (`dist2_le_of_later`, `dist2_polar`).
-/

namespace EncB.Geo
open ErdosSzekeres ErdosSzekeres.LayerLemma

namespace Lab

/-- Rotations by natural multiples of `u = 2π/m` extend to integer multiples. -/
theorem mem_int {m : ℕ} (hm : 0 < m) {H : Finset Point} {c : Point} {R θ : ℝ}
    (h : ∀ k : ℕ, polar c R (θ + (k : ℝ) * (2 * Real.pi / m)) ∈ H) (z : ℤ) :
    polar c R (θ + (z : ℝ) * (2 * Real.pi / m)) ∈ H := by
  have hmz : (0 : ℤ) < m := by exact_mod_cast hm
  have hmR : (m : ℝ) ≠ 0 := by exact_mod_cast hm.ne'
  have hnn : 0 ≤ z % (m : ℤ) := Int.emod_nonneg z hmz.ne'
  have hk := h (z % (m : ℤ)).toNat
  have hcast : (((z % (m : ℤ)).toNat : ℕ) : ℝ) = ((z % (m : ℤ) : ℤ) : ℝ) := by
    exact_mod_cast Int.toNat_of_nonneg hnn
  rw [hcast, ← polar_add_int c R _ (z / (m : ℤ))] at hk
  have hz : (z : ℝ) = ((z % (m : ℤ) : ℤ) : ℝ) + (m : ℝ) * ((z / (m : ℤ) : ℤ) : ℝ) := by
    exact_mod_cast (Int.emod_add_mul_ediv z (m : ℤ)).symm
  convert hk using 2
  rw [hz]
  field_simp
  ring

/-- F2-F4 (and the integer extension): every layer `n < t` contains, as hull vertices of
`peel T n`, a full regular `m`-gon `polar c R (θ + z·2π/m)` with `R > 0`. -/
theorem exists_layer_polar {m K t : ℕ} (hm : 0 < m) (hK : K ≤ 2 * m)
    {T : Finset Point} {c : Point} (hc : c ∉ T)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T) (hno : ¬ HasConvexNGon K T)
    (hcard : T.card = m * t) (n : ℕ) :
    ∃ R θ : ℝ, n < t → 0 < R ∧
      ∀ z : ℤ, polar c R (θ + (z : ℝ) * (2 * Real.pi / m)) ∈ hullVerts (peel T n) := by
  by_cases hn : n < t
  swap
  · exact ⟨0, 0, fun h => absurd h hn⟩
  -- F1
  have ht : m * (t - 1) < T.card := by
    rw [hcard]
    exact Nat.mul_lt_mul_of_pos_left (by omega) hm
  have hcp := card_peel hm hK hc hinv hno ht n hn.le
  have hne : (peel T n).Nonempty := by
    rw [← Finset.card_pos]
    have h1 : m * n < m * t := Nat.mul_lt_mul_of_pos_left hn hm
    omega
  -- F2, F3
  obtain ⟨x, hx⟩ := hullVerts_nonempty hne
  have hxc : x ≠ c := Capstone.ne_of_mem hc (peel_subset T n (hullVerts_subset _ hx))
  obtain ⟨θ, hθ⟩ := Capstone.exists_angle c x hxc
  refine ⟨Real.sqrt (dist2 c x), θ, fun _ => ⟨Capstone.sqrt_dist2_pos hxc, ?_⟩⟩
  -- F4
  apply mem_int hm
  intro k
  have hk := iterate_mem_hullVerts_peel hm hK hc hinv hno hx k
  rw [rotAbout_iterate, hθ, rotAbout_polar] at hk
  exact hk

end Lab

/-- **M5.** A counterexample with `m·t` points has a polar labelling of its `t` layers. -/
theorem labelling_of_counterexample {m K t : ℕ} (hm : 2 ≤ m) (heven : Even m) (hK : K ≤ 2 * m)
    {T : Finset Point} {c : Point} (hgp : GeneralPosition T) (hc : c ∉ T)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T) (hno : ¬ HasConvexNGon K T)
    (hcard : T.card = m * t) : Nonempty (PolarLabelling m t T c) := by
  have hm0 : 0 < m := by omega
  have hu : 0 < 2 * Real.pi / m := by
    have : (0 : ℝ) < m := by exact_mod_cast hm0
    positivity
  choose R θ hRθ using Lab.exists_layer_polar (t := t) hm0 hK hc hinv hno hcard
  -- F5
  set u : ℝ := 2 * Real.pi / m with hudef
  let ψ : ℕ → ℝ := fun i => toIcoMod hu 0 (θ i - θ 0)
  let J : ℕ → ℤ := fun i => toIcoDiv hu 0 (θ i - θ 0)
  have hdecomp : ∀ i, θ i - θ 0 = ψ i + (J i : ℝ) * u := by
    intro i
    have h := self_sub_toIcoMod hu 0 (θ i - θ 0)
    rw [zsmul_eq_mul] at h
    simp only [ψ, J]
    linarith
  have hIco : ∀ i, 0 ≤ ψ i ∧ ψ i < u := by
    intro i
    have h := toIcoMod_mem_Ico hu 0 (θ i - θ 0)
    rw [zero_add] at h
    exact h
  have hmem : ∀ i, i < t → polar c (R i) (θ i) ∈ hullVerts (peel T i) := by
    intro i hi
    have h := (hRθ i hi).2 0
    simpa using h
  -- F7: phases of distinct layers differ by no integer multiple of `u`
  have hphase : ∀ i j, i < t → j < t → i ≠ j → ∀ k : ℤ, θ j - θ i ≠ k * u :=
    fun i j hi hj hij =>
      phase_ne_of_distinct_layers hm heven hK hc hinv hgp hno hij (hRθ i hi).1 (hRθ j hj).1
        (hmem i hi) (hmem j hj)
  have hψinj : ∀ i j, i < t → j < t → ψ i = ψ j → i = j := by
    intro i j hi hj hψ
    by_contra hij
    apply hphase i j hi hj hij (J j - J i)
    have h1 := hdecomp i
    have h2 := hdecomp j
    push_cast
    linear_combination h2 - h1 - hψ
  refine ⟨{
    r := R
    ψ := ψ
    φ := θ 0
    r_pos := fun i hi => (hRθ i hi).1
    r_anti := ?_
    ψ_zero := ?_
    ψ_pos := ?_
    ψ_lt := fun i _ => (hIco i).2
    ψ_inj := hψinj
    mem_layer := ?_ }⟩
  · -- F8
    intro i j hij hj
    have hi : i < t := lt_of_le_of_lt hij hj
    have h := dist2_le_of_later hm0 hK hc hinv hno hij (hmem i hi)
      (hullVerts_subset _ (hmem j hj))
    rw [dist2_polar, dist2_polar] at h
    have hRi := (hRθ i hi).1
    have hRj := (hRθ j hj).1
    nlinarith
  · show toIcoMod hu 0 (θ 0 - θ 0) = 0
    rw [sub_self]
    exact toIcoMod_eq_self hu |>.2 ⟨le_refl 0, by rw [zero_add]; exact hu⟩
  · intro i hi0 hi
    have h0t : 0 < t := lt_of_le_of_lt (Nat.zero_le i) hi
    rcases (hIco i).1.lt_or_eq with h | h
    · exact h
    · exfalso
      have hne : (0 : ℕ) ≠ i := by omega
      have hψ0 : ψ 0 = 0 := by
        show toIcoMod hu 0 (θ 0 - θ 0) = 0
        rw [sub_self]
        exact toIcoMod_eq_self hu |>.2 ⟨le_refl 0, by rw [zero_add]; exact hu⟩
      exact hne (hψinj 0 i h0t hi (by rw [hψ0, h]))
  · -- F6
    intro i k hi
    have h := (hRθ i hi).2 ((k : ℤ) - J i)
    convert h using 2
    have h1 := hdecomp i
    push_cast
    linear_combination -h1

end EncB.Geo

#print axioms EncB.Geo.labelling_of_counterexample
