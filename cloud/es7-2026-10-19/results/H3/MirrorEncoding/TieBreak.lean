import MirrorEncoding.Interior
import Mathlib.Order.Interval.Set.Infinite

/-!
# Breaking x-ties in sub-case (ii) with a projective map

`pmap ε : (x, y) ↦ (x, y) / (1 + ε y)` commutes with `reflX`, and for `1 + ε y > 0` on the
three points it multiplies `orient` by a positive factor:
`orient (pmap a) (pmap b) (pmap c) * (w a * w b * w c) = orient a b c`. For all but finitely
many small `ε > 0` the image of a `MirrorSet` has distinct x-coordinates (`exists_eps`).
Pulling the x-sorted enumeration of the image back along `pinv ε` gives an enumeration of
`S` that satisfies the hypotheses of `interior_signotope_of_enum`. This proves
`InteriorTieBreak`.
-/

namespace Mir

open ETV ErdosSzekeres

/-- The weight `1 + ε y`. -/
noncomputable def wt (ε : ℝ) (q : Point) : ℝ := 1 + ε * q 1

/-- The projective map `(x, y) ↦ (x, y) / (1 + ε y)`. -/
noncomputable def pmap (ε : ℝ) (q : Point) : Point := ![q 0 / wt ε q, q 1 / wt ε q]

/-- Its inverse `(u, v) ↦ (u, v) / (1 - ε v)`. -/
noncomputable def pinv (ε : ℝ) (u : Point) : Point :=
  ![u 0 / (1 - ε * u 1), u 1 / (1 - ε * u 1)]

@[simp] theorem pmap_zero (ε : ℝ) (q : Point) : pmap ε q 0 = q 0 / wt ε q := rfl
@[simp] theorem pmap_one (ε : ℝ) (q : Point) : pmap ε q 1 = q 1 / wt ε q := rfl

theorem one_sub_pmap {ε : ℝ} {q : Point} (hw : 0 < wt ε q) :
    1 - ε * pmap ε q 1 = 1 / wt ε q := by
  have hw' : wt ε q ≠ 0 := hw.ne'
  rw [pmap_one]
  field_simp
  simp only [wt]
  ring

theorem pinv_pmap {ε : ℝ} {q : Point} (hw : 0 < wt ε q) : pinv ε (pmap ε q) = q := by
  have hw' : wt ε q ≠ 0 := hw.ne'
  simp only [pinv]
  rw [one_sub_pmap hw]
  ext i
  fin_cases i
  · simp only [Fin.zero_eta, Fin.isValue, Matrix.cons_val_zero, pmap_zero]
    field_simp
  · simp only [Fin.mk_one, Fin.isValue, Matrix.cons_val_one, Matrix.cons_val_zero, pmap_one]
    field_simp

theorem wt_reflX (ε : ℝ) (q : Point) : wt ε (reflX q) = wt ε q := by
  simp [wt]

theorem pmap_reflX (ε : ℝ) (q : Point) : pmap ε (reflX q) = reflX (pmap ε q) := by
  ext i
  fin_cases i
  · simp only [Fin.zero_eta, Fin.isValue, pmap_zero, reflX_zero, wt_reflX]
    ring
  · simp [wt_reflX]

theorem pinv_reflX (ε : ℝ) (u : Point) : pinv ε (reflX u) = reflX (pinv ε u) := by
  ext i
  fin_cases i
  · simp only [pinv, Fin.zero_eta, Fin.isValue, Matrix.cons_val_zero, reflX_zero, reflX_one]
    ring
  · simp [pinv]

theorem orient_pmap (ε : ℝ) (a b c : Point) (ha : wt ε a ≠ 0) (hb : wt ε b ≠ 0)
    (hc : wt ε c ≠ 0) :
    orient (pmap ε a) (pmap ε b) (pmap ε c) * (wt ε a * wt ε b * wt ε c) = orient a b c := by
  simp only [orient, pmap_zero, pmap_one]
  field_simp
  simp only [wt]
  ring

/-- A good `ε`: all weights positive and the projected x-coordinates distinct. -/
theorem exists_eps {S : Finset Point} {c : Point} (hM : MirrorSet S c) :
    ∃ ε : ℝ, 0 < ε ∧ (∀ q ∈ S, 0 < wt ε q) ∧ Set.InjOn (fun q => pmap ε q 0) ↑S := by
  classical
  let M : ℝ := S.sum fun q => |q 1|
  have hM0 : 0 ≤ M := Finset.sum_nonneg fun q _ => abs_nonneg _
  let bad : Finset ℝ := (S ×ˢ S).image
    (fun pq => (pq.2 0 - pq.1 0) / (pq.1 0 * pq.2 1 - pq.2 0 * pq.1 1))
  have hpos : (0 : ℝ) < 1 / (M + 1) := by positivity
  obtain ⟨ε, ⟨hε0, hε1⟩, hεb⟩ := (Set.Ioo_infinite hpos).exists_notMem_finset bad
  have hεM : ε * (M + 1) < 1 := (lt_div_iff₀ (by linarith)).1 hε1
  have hw : ∀ q ∈ S, 0 < wt ε q := by
    intro q hq
    have h1 : |q 1| ≤ M := Finset.single_le_sum (f := fun q => |q 1|)
      (fun q _ => abs_nonneg _) hq
    have h2 : -|q 1| ≤ q 1 := neg_abs_le _
    simp only [wt]
    nlinarith
  refine ⟨ε, hε0, hw, ?_⟩
  intro p hp q hq hpq
  simp only [pmap_zero] at hpq
  have hwp := (hw p hp).ne'
  have hwq := (hw q hq).ne'
  rw [div_eq_div_iff hwp hwq] at hpq
  simp only [wt] at hpq
  -- `hpq : p 0 * (1 + ε * q 1) = q 0 * (1 + ε * p 1)`
  by_cases hD : p 0 * q 1 - q 0 * p 1 = 0
  · have h0 : p 0 = q 0 := by nlinarith
    have hfac : p 0 * (q 1 - p 1) = 0 := by rw [← h0] at hD; linarith
    rcases mul_eq_zero.1 hfac with hp0 | h1
    · have hpc : p = c := by
        by_contra hne
        exact hM.off p (by simpa using hp) hne hp0
      have hqc : q = c := by
        by_contra hne
        exact hM.off q (by simpa using hq) hne (h0 ▸ hp0)
      rw [hpc, hqc]
    · ext i
      fin_cases i
      · exact h0
      · simp only [Fin.mk_one, Fin.isValue]
        linarith
  · exfalso
    apply hεb
    rw [Finset.mem_image]
    refine ⟨(p, q), Finset.mem_product.2 ⟨by simpa using hp, by simpa using hq⟩, ?_⟩
    simp only
    rw [div_eq_iff hD]
    linarith

/-- **`InteriorTieBreak` holds.** -/
theorem interiorTieBreak (S : Finset Point) (c : Point) (K : ℕ) (hK : 4 ≤ K)
    (hgp : GeneralPosition S) (hM : MirrorSet S c)
    (hin : c ∈ convexHull ℝ (↑(S.erase c) : Set Point)) (hno : ¬HasConvexNGon K S) :
    ∃ σ : Sig, IsSignotope S.card σ ∧ ¬HasGon σ S.card K ∧ MirSym S.card false σ ∧
      AxisInterior S.card σ := by
  classical
  obtain ⟨ε, _, hw, hinj⟩ := exists_eps hM
  let S' := S.image (pmap ε)
  have hφ : Set.InjOn (pmap ε) ↑S := fun p hp q hq h =>
    hinj hp hq (by simp only; rw [h])
  have hX' : LowerBound.DistinctX S' := by
    intro u hu v hv huv
    simp only [S', Finset.coe_image, Set.mem_image, Finset.mem_coe] at hu hv
    obtain ⟨p, hp, rfl⟩ := hu
    obtain ⟨q, hq, rfl⟩ := hv
    rw [hinj hp hq huv]
  have hM' : MirrorSet S' (pmap ε c) := by
    refine ⟨Finset.mem_image_of_mem _ hM.mem, by simp [hM.axis], ?_, ?_⟩
    · intro u hu
      obtain ⟨q, hq, rfl⟩ := Finset.mem_image.1 hu
      rw [← pmap_reflX]
      exact Finset.mem_image_of_mem _ (hM.symm q hq)
    · intro u hu hne
      obtain ⟨q, hq, rfl⟩ := Finset.mem_image.1 hu
      have hqc : q ≠ c := fun e => hne (by rw [e])
      simp only [pmap_zero]
      exact div_ne_zero (hM.off q hq hqc) (hw q hq).ne'
  obtain ⟨P', hx', hP', hpair', hc', hleft'⟩ := exists_mirror_xsorted hM' hX'
  have hcard : S'.card = S.card := Finset.card_image_of_injOn hφ
  rw [hcard] at hx' hP' hpair' hc' hleft'
  set N := S.card with hN
  -- every `P' i` is the image of a point of `S`
  have hpre : ∀ i, i < N → ∃ q ∈ S, pmap ε q = P' i := by
    intro i hi
    have : P' i ∈ S' := by rw [← hP']; exact mem_ptSet hi
    simpa [S'] using this
  let P : ℕ → Point := fun i => pinv ε (P' i)
  have hPS : ∀ i, i < N → P i ∈ S ∧ pmap ε (P i) = P' i := by
    intro i hi
    obtain ⟨q, hq, e⟩ := hpre i hi
    have : P i = q := by simp only [P, ← e, pinv_pmap (hw q hq)]
    rw [this]
    exact ⟨hq, e⟩
  have hsigeq : ∀ i j k, i < N → j < N → k < N → sigOf P i j k = sigOf P' i j k := by
    intro i j k hi hj hk
    obtain ⟨hiS, ei⟩ := hPS i hi
    obtain ⟨hjS, ej⟩ := hPS j hj
    obtain ⟨hkS, ek⟩ := hPS k hk
    have hprod : 0 < wt ε (P i) * wt ε (P j) * wt ε (P k) :=
      mul_pos (mul_pos (hw _ hiS) (hw _ hjS)) (hw _ hkS)
    have e := orient_pmap ε (P i) (P j) (P k) (hw _ hiS).ne' (hw _ hjS).ne' (hw _ hkS).ne'
    rw [ei, ej, ek] at e
    simp only [sigOf]
    rw [← e]
    simp only [decide_eq_decide]
    exact mul_pos_iff_of_pos_right hprod
  have hsig : IsSignotope N (sigOf P) := by
    intro i j k l hij hjk hkl hl
    rw [hsigeq i j k (by omega) (by omega) (by omega), hsigeq i j l (by omega) (by omega) hl,
      hsigeq i k l (by omega) (by omega) hl, hsigeq j k l (by omega) (by omega) hl]
    exact isSignotope_sigOf hx' i j k l hij hjk hkl hl
  have hinjP : Set.InjOn P ↑(Finset.range N) := by
    intro i hi j hj e
    simp only [Finset.coe_range, Set.mem_Iio] at hi hj
    apply hx'.injOn (by simpa using hi) (by simpa using hj)
    rw [← (hPS i hi).2, ← (hPS j hj).2]
    exact congrArg (pmap ε) e
  have hP : ptSet P N = S := by
    ext q
    simp only [ptSet, Finset.mem_image, Finset.mem_range]
    constructor
    · rintro ⟨i, hi, rfl⟩
      exact (hPS i hi).1
    · intro hq
      have : pmap ε q ∈ ptSet P' N := by rw [hP']; exact Finset.mem_image_of_mem _ hq
      simp only [ptSet, Finset.mem_image, Finset.mem_range] at this
      obtain ⟨i, hi, e⟩ := this
      exact ⟨i, hi, by simp only [P, e, pinv_pmap (hw q hq)]⟩
  have hpair : ∀ i, i < N → P (N - 1 - i) = reflX (P i) := by
    intro i hi
    simp only [P, hpair' i hi, pinv_reflX]
  have hc : P (axisPt N) = c := by
    simp only [P, hc', pinv_pmap (hw c hM.mem)]
  have hleft : ∀ i, i < axisPt N → P i 0 < 0 := by
    intro i hi
    have hiN : i < N := by
      have := Finset.card_pos.2 ⟨c, hM.mem⟩
      simp only [axisPt] at hi
      omega
    obtain ⟨hiS, ei⟩ := hPS i hiN
    have h1 : 0 < 1 - ε * P' i 1 := by
      rw [← ei, one_sub_pmap (hw _ hiS)]
      exact one_div_pos.2 (hw _ hiS)
    simp only [P, pinv, Matrix.cons_val_zero]
    exact div_neg_of_neg_of_pos (hleft' i hi) h1
  exact interior_signotope_of_enum hK hgp hM hin hno P hsig hinjP hP hpair hc hleft

end Mir
