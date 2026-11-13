import ES8Geo.Interface

/-! # M6 (basic fields): the label map of a polar labelling and the easy fields of `EncB.Model`

For a polar labelling `L : PolarLabelling m t T c` of a counterexample we prove (DESIGN.md §3.4):

* G1 `labelling_P_rot`: `P (rot a) = ρ (P a)` (the wrap `k = m-1 ↦ 0` adds `2π`, `polar_add_int`);
* `labelling_P_mem`: `P a` is a hull vertex of `peel T a.1`;
* G2 `labelling_P_injOn`: `P` is injective on valid labels (distinct layers: `not_mem_hullVerts_peel_of_ne`;
  same layer: `P(i,k) = ρ^[k] P(i,0)` and `minimalPeriod_rotAbout`);
* G3 `labelling_orient_ne_zero`: distinct valid labels give a non-degenerate triangle;
* the `Model` fields `psiLt_irrefl/trans/total/zero`, `chi_rot`, `chi_cycle`, `chi_swap`, `nest`, `noChain`,
  each stated with exactly the shape of the field of `EncB.Model m K t` with `chi := L.chi`,
  `psiLt := L.psiLt`.

Each theorem takes only the standing hypotheses it needs, in the standing order. Helpers live in
`EncB.Geo.Basic`.
-/

namespace EncB.Geo
open ErdosSzekeres ErdosSzekeres.LayerLemma

namespace Basic

variable {m t : ℕ} {T : Finset Point} {c : Point}

theorem P_def (L : PolarLabelling m t T c) (i k : ℕ) :
    L.P (i, k) = polar c (L.r i) (L.φ + L.ψ i + (k : ℝ) * (2 * Real.pi / m)) := rfl

/-- `P(i,k) = ρ^[k] P(i,0)`. -/
theorem P_eq_iterate (L : PolarLabelling m t T c) (i k : ℕ) :
    L.P (i, k) = (rotAbout c (2 * Real.pi / m))^[k] (L.P (i, 0)) := by
  rw [rotAbout_iterate, P_def, P_def, rotAbout_polar]
  congr 1
  push_cast
  ring

/-- A label point is a point of `T`. -/
theorem P_mem_T (L : PolarLabelling m t T c) (a : EncB.Pt) (ha : EncB.PtOk m t a) : L.P a ∈ T :=
  peel_subset T a.1 (hullVerts_subset _ (L.mem_layer a.1 a.2 ha.1))

/-- A label point lies in every earlier peel. -/
theorem P_mem_peel (L : PolarLabelling m t T c) (a : EncB.Pt) (ha : EncB.PtOk m t a) {i : ℕ}
    (hi : i ≤ a.1) : L.P a ∈ peel T i :=
  peel_antitone T hi (hullVerts_subset _ (L.mem_layer a.1 a.2 ha.1))

theorem decide_pos_neg {x : ℝ} (hx : x ≠ 0) : decide (0 < -x) = !decide (0 < x) := by
  rcases lt_or_gt_of_ne hx with h | h
  · simp [h, not_lt.2 h.le]
  · simp [h, not_lt.2 (neg_nonpos.2 h.le)]

end Basic

open Basic

/-- **G1.** The label map commutes with the rotation: `P (rot a) = ρ (P a)`. -/
theorem labelling_P_rot {m t : ℕ} (hm : 3 ≤ m) {T : Finset Point} {c : Point}
    (L : PolarLabelling m t T c) (a : EncB.Pt) (ha : a.2 < m) :
    L.P (EncB.rot m a) = rotAbout c (2 * Real.pi / m) (L.P a) := by
  obtain ⟨i, k⟩ := a
  have hmR : (m : ℝ) ≠ 0 := Nat.cast_ne_zero.2 (by omega)
  show L.P (i, (k + 1) % m) = _
  rw [P_def, P_def, rotAbout_polar]
  rcases Nat.lt_or_ge (k + 1) m with h | h
  · rw [Nat.mod_eq_of_lt h]
    congr 1
    push_cast
    ring
  · have hk : k + 1 = m := by simp at ha; omega
    rw [hk, Nat.mod_self]
    have hkR : (k : ℝ) + 1 = m := by exact_mod_cast hk
    have hθ : L.φ + L.ψ i + (k : ℝ) * (2 * Real.pi / m) + 2 * Real.pi / m =
        (L.φ + L.ψ i + ((0 : ℕ) : ℝ) * (2 * Real.pi / m)) + ((1 : ℤ) : ℝ) * (2 * Real.pi) := by
      have : (k : ℝ) * (2 * Real.pi / m) + 2 * Real.pi / m = 2 * Real.pi := by
        rw [← add_one_mul, hkR]
        field_simp
      push_cast
      linarith
    rw [hθ, polar_add_int]

/-- The label point `P a` of a valid label is a hull vertex of `peel T a.1`. -/
theorem labelling_P_mem {m t : ℕ} {T : Finset Point} {c : Point} (L : PolarLabelling m t T c)
    (a : EncB.Pt) (ha : EncB.PtOk m t a) : L.P a ∈ hullVerts (peel T a.1) :=
  L.mem_layer a.1 a.2 ha.1

/-- **G2.** The label map is injective on valid labels. -/
theorem labelling_P_injOn {m t : ℕ} (hm : 3 ≤ m) {T : Finset Point} {c : Point} (hc : c ∉ T)
    (L : PolarLabelling m t T c) (a b : EncB.Pt) (ha : EncB.PtOk m t a) (hb : EncB.PtOk m t b)
    (h : L.P a = L.P b) : a = b := by
  obtain ⟨i, k⟩ := a
  obtain ⟨j, l⟩ := b
  have hi : i = j := by
    by_contra hij
    have h1 := labelling_P_mem L (i, k) ha
    have h2 := labelling_P_mem L (j, l) hb
    rw [h] at h1
    exact not_mem_hullVerts_peel_of_ne T hij h1 h2
  subst hi
  have hx : L.P (i, 0) ≠ c := by
    intro hxc
    exact hc (hxc ▸ P_mem_T L (i, 0) ⟨ha.1, by simp; omega⟩)
  have hper := minimalPeriod_rotAbout (m := m) (by omega) hx
  rw [P_eq_iterate L i k, P_eq_iterate L i l] at h
  have hk : k < Function.minimalPeriod (rotAbout c (2 * Real.pi / m)) (L.P (i, 0)) := by
    rw [hper]; exact ha.2
  have hl : l < Function.minimalPeriod (rotAbout c (2 * Real.pi / m)) (L.P (i, 0)) := by
    rw [hper]; exact hb.2
  have hkl : k = l := (Function.iterate_eq_iterate_iff_of_lt_minimalPeriod hk hl).1 h
  rw [hkl]

/-- **G3.** Three distinct valid labels give a non-degenerate triangle. -/
theorem labelling_orient_ne_zero {m t : ℕ} (hm : 3 ≤ m) {T : Finset Point} {c : Point}
    (hgp : GeneralPosition T) (hc : c ∉ T) (L : PolarLabelling m t T c) (a b d : EncB.Pt)
    (ha : EncB.PtOk m t a) (hb : EncB.PtOk m t b) (hd : EncB.PtOk m t d)
    (hdist : EncB.Distinct3 a b d) : orient (L.P a) (L.P b) (L.P d) ≠ 0 := by
  obtain ⟨hab, had, hbd⟩ := hdist
  exact (generalPosition_iff_orient_ne_zero T).1 hgp _ (P_mem_T L a ha) _ (P_mem_T L b hb) _
    (P_mem_T L d hd) (fun e => hab (labelling_P_injOn hm hc L a b ha hb e))
    (fun e => had (labelling_P_injOn hm hc L a d ha hd e))
    (fun e => hbd (labelling_P_injOn hm hc L b d hb hd e))

/-! ## The `psiLt` fields -/

theorem labelling_psiLt_irrefl {m t : ℕ} {T : Finset Point} {c : Point}
    (L : PolarLabelling m t T c) : ∀ i, L.psiLt i i = false := by
  intro i
  simp [PolarLabelling.psiLt]

theorem labelling_psiLt_trans {m t : ℕ} {T : Finset Point} {c : Point}
    (L : PolarLabelling m t T c) :
    ∀ i j k, L.psiLt i j = true → L.psiLt j k = true → L.psiLt i k = true := by
  intro i j k h1 h2
  simp only [PolarLabelling.psiLt, decide_eq_true_eq] at h1 h2 ⊢
  exact h1.trans h2

theorem labelling_psiLt_total {m t : ℕ} {T : Finset Point} {c : Point}
    (L : PolarLabelling m t T c) :
    ∀ i j, i < t → j < t → i ≠ j → L.psiLt i j = true ∨ L.psiLt j i = true := by
  intro i j hi hj hij
  simp only [PolarLabelling.psiLt, decide_eq_true_eq]
  exact lt_or_gt_of_ne (fun e => hij (L.ψ_inj i j hi hj e))

theorem labelling_psiLt_zero {m t : ℕ} {T : Finset Point} {c : Point}
    (L : PolarLabelling m t T c) : ∀ i, 0 < i → i < t → L.psiLt 0 i = true := by
  intro i hi hit
  simp only [PolarLabelling.psiLt, decide_eq_true_eq, L.ψ_zero]
  exact L.ψ_pos i hi hit

/-! ## The `chi` fields -/

theorem labelling_chi_rot {m t : ℕ} (hm : 3 ≤ m) {T : Finset Point} {c : Point}
    (L : PolarLabelling m t T c) :
    ∀ a b d, EncB.PtOk m t a → EncB.PtOk m t b → EncB.PtOk m t d →
      L.chi (EncB.rot m a) (EncB.rot m b) (EncB.rot m d) = L.chi a b d := by
  intro a b d ha hb hd
  simp only [PolarLabelling.chi]
  rw [labelling_P_rot hm L a ha.2, labelling_P_rot hm L b hb.2, labelling_P_rot hm L d hd.2,
    orient_rotAbout_inv]

theorem labelling_chi_cycle {m t : ℕ} {T : Finset Point} {c : Point}
    (L : PolarLabelling m t T c) :
    ∀ a b d, EncB.PtOk m t a → EncB.PtOk m t b → EncB.PtOk m t d → EncB.Distinct3 a b d →
      L.chi b d a = L.chi a b d := by
  intro a b d _ _ _ _
  simp only [PolarLabelling.chi, orient_cycle]

theorem labelling_chi_swap {m t : ℕ} (hm : 3 ≤ m) {T : Finset Point} {c : Point}
    (hgp : GeneralPosition T) (hc : c ∉ T) (L : PolarLabelling m t T c) :
    ∀ a b d, EncB.PtOk m t a → EncB.PtOk m t b → EncB.PtOk m t d → EncB.Distinct3 a b d →
      L.chi a d b = !L.chi a b d := by
  intro a b d ha hb hd hdist
  rw [PolarLabelling.chi, PolarLabelling.chi, orient_swap]
  exact decide_pos_neg (labelling_orient_ne_zero hm hgp hc L a b d ha hb hd hdist)

/-! ## Nesting and chains -/

theorem labelling_nest {m K t : ℕ} (hm : 3 ≤ m) (hK : K ≤ 2 * m) {T : Finset Point} {c : Point}
    (hgp : GeneralPosition T) (hc : c ∉ T) (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T)
    (hno : ¬ HasConvexNGon K T) (L : PolarLabelling m t T c) :
    ∀ i j k, i < j → j < t → k < m → L.chi (i, 0) (i, 1) (j, k) = true := by
  intro i j k hij hjt hk
  have hrot : EncB.rot m (i, 0) = (i, 1) := by
    simp only [EncB.rot, Nat.zero_add, Prod.mk.injEq, true_and]
    exact Nat.mod_eq_of_lt (by omega)
  have h1 : L.P (i, 1) = rotAbout c (2 * Real.pi / m) (L.P (i, 0)) := by
    rw [← hrot]; exact labelling_P_rot hm L (i, 0) (by simp; omega)
  have hx : L.P (i, 0) ∈ hullVerts (peel T i) :=
    labelling_P_mem L (i, 0) ⟨by omega, by simp; omega⟩
  have hy : L.P (j, k) ∈ peel T j :=
    P_mem_peel L (j, k) ⟨hjt, hk⟩ le_rfl
  simp only [PolarLabelling.chi, decide_eq_true_eq]
  rw [h1]
  exact strict_nesting (by omega) hK hc hinv hno hgp hij hx hy

theorem labelling_noChain {m K t : ℕ} (hm : 3 ≤ m) (hK4 : 4 ≤ K) (hK : K ≤ 2 * m)
    {T : Finset Point} {c : Point} (hgp : GeneralPosition T) (hc : c ∉ T)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T) (hno : ¬ HasConvexNGon K T)
    (L : PolarLabelling m t T c) :
    ∀ i, i < t → ∀ q : Nat → EncB.Pt,
      (∀ s, s < K - 1 → EncB.InQ m t i (q s)) →
      (∀ s, s + 1 < K - 1 → L.chi (i, 0) (q s) (q (s + 1)) = true) →
      (∀ s, s + 2 < K - 1 → L.chi (q s) (q (s + 1)) (q (s + 2)) = true) → False := by
  intro i hi q hq hfan hturn
  have hp0 : EncB.PtOk m t (i, 0) := ⟨hi, by simp; omega⟩
  have hqok : ∀ s, s < K - 1 → EncB.PtOk m t (q s) := fun s hs =>
    ⟨(hq s hs).2.1, (hq s hs).2.2.1⟩
  refine chain_clauses_sound hm hK4 hK hc hinv hno hgp (labelling_P_mem L (i, 0) hp0)
    (q := fun s => L.P (q s)) (fun s hs => P_mem_peel L (q s) (hqok s hs) (hq s hs).1)
    (fun s hs e => (hq s hs).2.2.2 (labelling_P_injOn hm hc L _ _ (hqok s hs) hp0 e)) ?_ ?_
  · intro s hs
    have := hfan s hs
    simpa only [PolarLabelling.chi, decide_eq_true_eq] using this
  · intro s hs
    have := hturn s hs
    simpa only [PolarLabelling.chi, decide_eq_true_eq] using this

end EncB.Geo

#print axioms EncB.Geo.labelling_P_rot
#print axioms EncB.Geo.labelling_P_mem
#print axioms EncB.Geo.labelling_P_injOn
#print axioms EncB.Geo.labelling_orient_ne_zero
#print axioms EncB.Geo.labelling_psiLt_irrefl
#print axioms EncB.Geo.labelling_psiLt_trans
#print axioms EncB.Geo.labelling_psiLt_total
#print axioms EncB.Geo.labelling_psiLt_zero
#print axioms EncB.Geo.labelling_chi_rot
#print axioms EncB.Geo.labelling_chi_cycle
#print axioms EncB.Geo.labelling_chi_swap
#print axioms EncB.Geo.labelling_nest
#print axioms EncB.Geo.labelling_noChain
