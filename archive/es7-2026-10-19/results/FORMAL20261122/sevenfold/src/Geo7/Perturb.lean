import Geo7.LayerBasic

/-!
# G-C: a small rotation of the layers keeps every orientation sign and makes the phases generic

For layer data `L` (`LayerLab`, any `m`) and `η : ℝ`, the perturbed label map rotates layer `i` by `i·η`:
`Pη η (i,k) = polar c (r i) ((φ + ψ i + k·2π/m) + i·η)`. We prove that some `η > 0` satisfies

* (C1) every valid triple of distinct labels keeps the sign of `orient` (`eventually_sign`; continuity through
  `orient_polar`, finitely many triples, `orient ≠ 0` at `η = 0` given as a hypothesis);
* (C2) for `i ≠ j < t`, `(ψ i + iη) − (ψ j + jη)` is no integer multiple of `v > 0` (`eventually_generic`;
  for each pair only two multiples can be hit for `0 < η < v/|i−j|`, each at one value of `η`);
* (C3) `ψ i + iη < 2π/m` for `i < t`.

This replaces P1's Lemma generic(b) (k8_soundness_p1.tex): the orientation signs of the original set are kept and
only the *phase order* is read off the perturbed one, so the layer structure of a perturbed set is never needed.
-/

namespace EncB.Geo7
open ErdosSzekeres ErdosSzekeres.LayerLemma Filter Topology

variable {m t : ℕ} {T : Finset Point} {c : Point}

/-- The perturbed label map: layer `a.1` rotated by `a.1 · η`. -/
noncomputable def LayerLab.Pη (L : LayerLab m t T c) (η : ℝ) (a : EncB.Pt) : Point :=
  polar c (L.r a.1) ((L.φ + L.ψ a.1 + (a.2 : ℝ) * (2 * Real.pi / m)) + (a.1 : ℝ) * η)

theorem LayerLab.Pη_zero (L : LayerLab m t T c) (a : EncB.Pt) : L.Pη 0 a = L.P a := by
  simp only [LayerLab.Pη, LayerLab.P, mul_zero, add_zero]

/-- Continuity of the orientation of three rotating polar points. -/
theorem continuous_orient_polar (c : Point) (r1 r2 r3 a1 a2 a3 b1 b2 b3 : ℝ) :
    Continuous fun η : ℝ =>
      orient (polar c r1 (a1 + b1 * η)) (polar c r2 (a2 + b2 * η)) (polar c r3 (a3 + b3 * η)) := by
  simp only [orient_polar]
  fun_prop

/-- The sign of `orient` at `η` near `0` is its sign at `0`, when that is nonzero. -/
theorem eventually_sign_one (L : LayerLab m t T c) (a b d : EncB.Pt)
    (h : orient (L.P a) (L.P b) (L.P d) ≠ 0) :
    ∀ᶠ η in 𝓝 (0 : ℝ), (0 < orient (L.Pη η a) (L.Pη η b) (L.Pη η d) ↔ 0 < orient (L.P a) (L.P b) (L.P d)) := by
  have hc := (continuous_orient_polar c (L.r a.1) (L.r b.1) (L.r d.1)
    (L.φ + L.ψ a.1 + (a.2 : ℝ) * (2 * Real.pi / m)) (L.φ + L.ψ b.1 + (b.2 : ℝ) * (2 * Real.pi / m))
    (L.φ + L.ψ d.1 + (d.2 : ℝ) * (2 * Real.pi / m)) (a.1 : ℝ) (b.1 : ℝ) (d.1 : ℝ)).continuousAt (x := 0)
  have h0 : orient (L.Pη 0 a) (L.Pη 0 b) (L.Pη 0 d) = orient (L.P a) (L.P b) (L.P d) := by
    rw [L.Pη_zero, L.Pη_zero, L.Pη_zero]
  rcases lt_or_gt_of_ne h with hneg | hpos
  · have hev := hc.eventually_lt continuousAt_const (show _ < (0 : ℝ) from by
      simp only [LayerLab.Pη] at h0 ⊢; rw [h0]; exact hneg)
    filter_upwards [hev] with η hη
    simp only [LayerLab.Pη] at hη ⊢
    exact ⟨fun h1 => absurd (lt_trans h1 hη) (lt_irrefl _), fun h1 => absurd (lt_trans h1 hneg) (lt_irrefl _)⟩
  · have hev := continuousAt_const.eventually_lt hc (show (0 : ℝ) < _ from by
      simp only [LayerLab.Pη] at h0 ⊢; rw [h0]; exact hpos)
    filter_upwards [hev] with η hη
    simp only [LayerLab.Pη] at hη ⊢
    exact ⟨fun _ => hpos, fun _ => hη⟩

/-- The valid labels as a finset. -/
def labs (m t : ℕ) : Finset EncB.Pt := Finset.range t ×ˢ Finset.range m

theorem mem_labs {m t : ℕ} {a : EncB.Pt} : a ∈ labs m t ↔ EncB.PtOk m t a := by
  simp [labs, EncB.PtOk, Finset.mem_product]

/-- **(C1)** All valid triples of distinct labels keep their orientation sign near `η = 0`. -/
theorem eventually_sign (L : LayerLab m t T c)
    (h : ∀ a b d, EncB.PtOk m t a → EncB.PtOk m t b → EncB.PtOk m t d → EncB.Distinct3 a b d →
      orient (L.P a) (L.P b) (L.P d) ≠ 0) :
    ∀ᶠ η in 𝓝 (0 : ℝ), ∀ a b d, EncB.PtOk m t a → EncB.PtOk m t b → EncB.PtOk m t d → EncB.Distinct3 a b d →
      (0 < orient (L.Pη η a) (L.Pη η b) (L.Pη η d) ↔ 0 < orient (L.P a) (L.P b) (L.P d)) := by
  have hall : ∀ᶠ η in 𝓝 (0 : ℝ), ∀ a ∈ labs m t, ∀ b ∈ labs m t, ∀ d ∈ labs m t, EncB.Distinct3 a b d →
      (0 < orient (L.Pη η a) (L.Pη η b) (L.Pη η d) ↔ 0 < orient (L.P a) (L.P b) (L.P d)) := by
    rw [eventually_all_finset]
    intro a ha
    rw [eventually_all_finset]
    intro b hb
    rw [eventually_all_finset]
    intro d hd
    by_cases hdist : EncB.Distinct3 a b d
    · filter_upwards [eventually_sign_one L a b d
        (h a b d (mem_labs.1 ha) (mem_labs.1 hb) (mem_labs.1 hd) hdist)] with η hη
      exact fun _ => hη
    · exact Eventually.of_forall fun _ h' => absurd h' hdist
  filter_upwards [hall] with η hη
  intro a b d ha hb hd hdist
  exact hη a (mem_labs.2 ha) b (mem_labs.2 hb) d (mem_labs.2 hd) hdist

/-- Every point `≠ b` near `0` from the right. -/
theorem eventually_ne_Ioi (b : ℝ) : ∀ᶠ η in 𝓝[>] (0 : ℝ), η ≠ b := by
  rcases le_or_gt b 0 with hb | hb
  · exact eventually_nhdsWithin_of_forall fun η (hη : 0 < η) => ne_of_gt (lt_of_le_of_lt hb hη)
  · exact ((eventually_lt_nhds hb).filter_mono nhdsWithin_le_nhds).mono fun η h => ne_of_lt h

/-- **The key step of (C2)**: `D + s·η` avoids `vℤ` for all small `η > 0`, if `s ≠ 0`. -/
theorem eventually_not_mul {D s v : ℝ} (hv : 0 < v) (hs : s ≠ 0) :
    ∀ᶠ η in 𝓝[>] (0 : ℝ), ∀ k : ℤ, D + s * η ≠ k * v := by
  set n : ℤ := ⌊D / v⌋ with hn
  have hsa : 0 < |s| := abs_pos.2 hs
  have h3 : ∀ᶠ η in 𝓝[>] (0 : ℝ), η < v / |s| :=
    (eventually_lt_nhds (div_pos hv hsa)).filter_mono nhdsWithin_le_nhds
  have h4 : ∀ᶠ η in 𝓝[>] (0 : ℝ), 0 < η := eventually_nhdsWithin_of_forall fun η hη => hη
  filter_upwards [eventually_ne_Ioi (((n : ℝ) * v - D) / s), eventually_ne_Ioi ((((n + 1 : ℤ) : ℝ) * v - D) / s),
    h3, h4] with η e1 e2 e3 e4
  intro k hk
  -- `k` is within distance `< 1` of `D / v`
  have hdiff : (k : ℝ) - D / v = s * η / v := by
    field_simp
    linarith
  have hsmall : |s * η / v| < 1 := by
    rw [abs_div, abs_mul, abs_of_pos e4, abs_of_pos hv, div_lt_one hv]
    calc |s| * η < |s| * (v / |s|) := mul_lt_mul_of_pos_left e3 hsa
      _ = v := by field_simp
  rw [← hdiff] at hsmall
  have hb := abs_lt.1 hsmall
  have hn1 : (n : ℝ) ≤ D / v := Int.floor_le _
  have hn2 : D / v < n + 1 := Int.lt_floor_add_one _
  have hk1 : (k : ℝ) < n + 2 := by linarith
  have hk2 : (n : ℝ) - 1 < k := by linarith
  have hk1' : k < n + 2 := by exact_mod_cast hk1
  have hk2' : n - 1 < k := by exact_mod_cast hk2
  have hη : η = ((k : ℝ) * v - D) / s := by
    field_simp
    linarith
  rcases (show k = n ∨ k = n + 1 by omega) with rfl | rfl
  · exact e1 hη
  · exact e2 hη

/-- **(C2)** For distinct layers the perturbed phases differ by no multiple of `v`. -/
theorem eventually_generic (L : LayerLab m t T c) {v : ℝ} (hv : 0 < v) :
    ∀ᶠ η in 𝓝[>] (0 : ℝ), ∀ i j, i < t → j < t → i ≠ j →
      ∀ k : ℤ, (L.ψ i + (i : ℝ) * η) - (L.ψ j + (j : ℝ) * η) ≠ k * v := by
  have hall : ∀ᶠ η in 𝓝[>] (0 : ℝ), ∀ i ∈ Finset.range t, ∀ j ∈ Finset.range t, i ≠ j →
      ∀ k : ℤ, (L.ψ i + (i : ℝ) * η) - (L.ψ j + (j : ℝ) * η) ≠ k * v := by
    rw [eventually_all_finset]
    intro i _
    rw [eventually_all_finset]
    intro j _
    by_cases hij : i = j
    · exact Eventually.of_forall fun _ h' => absurd hij h'
    · have hs : ((i : ℝ) - j) ≠ 0 := sub_ne_zero.2 (by exact_mod_cast hij)
      filter_upwards [eventually_not_mul (D := L.ψ i - L.ψ j) hv hs] with η hη
      intro _ k hk
      exact hη k (by rw [← hk]; ring)
  filter_upwards [hall] with η hη
  intro i j hi hj hij
  exact hη i (Finset.mem_range.2 hi) j (Finset.mem_range.2 hj) hij

/-- **(C3)** The perturbed phases stay below `2π/m`. -/
theorem eventually_lt_u (L : LayerLab m t T c) :
    ∀ᶠ η in 𝓝 (0 : ℝ), ∀ i, i < t → L.ψ i + (i : ℝ) * η < 2 * Real.pi / m := by
  have hall : ∀ᶠ η in 𝓝 (0 : ℝ), ∀ i ∈ Finset.range t, L.ψ i + (i : ℝ) * η < 2 * Real.pi / m := by
    rw [eventually_all_finset]
    intro i _
    have hc : Continuous fun η : ℝ => L.ψ i + (i : ℝ) * η := by fun_prop
    exact hc.continuousAt.eventually_lt continuousAt_const (by simpa using L.ψ_lt i)
  filter_upwards [hall] with η hη
  exact fun i hi => hη i (Finset.mem_range.2 hi)

/-- **G-C.** Some `η > 0` satisfies (C1), (C2) (with `v`) and (C3). -/
theorem exists_perturbation (L : LayerLab m t T c) {v : ℝ} (hv : 0 < v)
    (h : ∀ a b d, EncB.PtOk m t a → EncB.PtOk m t b → EncB.PtOk m t d → EncB.Distinct3 a b d →
      orient (L.P a) (L.P b) (L.P d) ≠ 0) :
    ∃ η : ℝ, 0 < η ∧
      (∀ a b d, EncB.PtOk m t a → EncB.PtOk m t b → EncB.PtOk m t d → EncB.Distinct3 a b d →
        (0 < orient (L.Pη η a) (L.Pη η b) (L.Pη η d) ↔ 0 < orient (L.P a) (L.P b) (L.P d))) ∧
      (∀ i j, i < t → j < t → i ≠ j → ∀ k : ℤ, (L.ψ i + (i : ℝ) * η) - (L.ψ j + (j : ℝ) * η) ≠ k * v) ∧
      (∀ i, i < t → L.ψ i + (i : ℝ) * η < 2 * Real.pi / m) := by
  have hpos : ∀ᶠ η in 𝓝[>] (0 : ℝ), 0 < η := eventually_nhdsWithin_of_forall fun η hη => hη
  obtain ⟨η, h1, h2, h3, h4⟩ := (hpos.and ((eventually_sign L h).filter_mono nhdsWithin_le_nhds |>.and
    ((eventually_generic L hv).and ((eventually_lt_u L).filter_mono nhdsWithin_le_nhds)))).exists
  exact ⟨η, h1, h2, h3, h4⟩

end EncB.Geo7

#print axioms EncB.Geo7.exists_perturbation
