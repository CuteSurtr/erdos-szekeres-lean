import ES8Geo.Labelling

/-! # Layer data of an m-fold counterexample, for any m (no genericity): `LayerLab`

ENCBLEAN's `PolarLabelling` without `ψ_pos` and `ψ_inj` (which need `Even m`), and `layerLab_of_counterexample`,
ENCBLEAN's M5 (`labelling_of_counterexample`) with the steps that need `Even m` removed. Everything else is
ENCBLEAN's (`Lab.exists_layer_polar`, `dist2_le_of_later`, `toIcoMod`). -/

namespace EncB.Geo7
open ErdosSzekeres ErdosSzekeres.LayerLemma

/-- Layer `i < t` of `T` is the regular `m`-gon `P(i,k) = polar c (r i) (φ + ψ i + k·2π/m)` of hull vertices of
`peel T i`; `0 = ψ 0 ≤ ψ i < 2π/m`; radii positive and weakly decreasing. Phases of distinct layers may agree. -/
structure LayerLab (m t : ℕ) (T : Finset Point) (c : Point) where
  r : ℕ → ℝ
  ψ : ℕ → ℝ
  φ : ℝ
  r_pos  : ∀ i : ℕ, i < t → 0 < r i
  r_anti : ∀ i j : ℕ, i ≤ j → j < t → r j ≤ r i
  ψ_zero : ψ 0 = 0
  ψ_nonneg : ∀ i : ℕ, 0 ≤ ψ i
  ψ_lt   : ∀ i : ℕ, ψ i < 2 * Real.pi / m
  mem_layer : ∀ i k : ℕ, i < t →
    polar c (r i) (φ + ψ i + (k : ℝ) * (2 * Real.pi / m)) ∈ hullVerts (peel T i)

namespace LayerLab

variable {m t : ℕ} {T : Finset Point} {c : Point}

noncomputable def P (L : LayerLab m t T c) (a : EncB.Pt) : Point :=
  polar c (L.r a.1) (L.φ + L.ψ a.1 + (a.2 : ℝ) * (2 * Real.pi / m))

noncomputable def chi (L : LayerLab m t T c) (a b d : EncB.Pt) : Bool :=
  decide (0 < orient (L.P a) (L.P b) (L.P d))

end LayerLab

/-- **M5 for any m ≥ 2** (no genericity). -/
theorem layerLab_of_counterexample {m K t : ℕ} (hm : 2 ≤ m) (hK : K ≤ 2 * m)
    {T : Finset Point} {c : Point} (hc : c ∉ T)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T) (hno : ¬ HasConvexNGon K T)
    (hcard : T.card = m * t) : Nonempty (LayerLab m t T c) := by
  have hm0 : 0 < m := by omega
  have hu : 0 < 2 * Real.pi / m := by
    have : (0 : ℝ) < m := by exact_mod_cast hm0
    positivity
  choose R θ hRθ using EncB.Geo.Lab.exists_layer_polar (t := t) hm0 hK hc hinv hno hcard
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
  refine ⟨{
    r := R
    ψ := ψ
    φ := θ 0
    r_pos := fun i hi => (hRθ i hi).1
    r_anti := ?_
    ψ_zero := ?_
    ψ_nonneg := fun i => (hIco i).1
    ψ_lt := fun i => (hIco i).2
    mem_layer := ?_ }⟩
  · intro i j hij hj
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
  · intro i k hi
    have h := (hRθ i hi).2 ((k : ℤ) - J i)
    convert h using 2
    have h1 := hdecomp i
    push_cast
    linear_combination -h1

end EncB.Geo7

#print axioms EncB.Geo7.layerLab_of_counterexample
