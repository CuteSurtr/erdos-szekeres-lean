import Geo7.Perturb
import Geo7.ArcData
import EncBO.Compose7

/-!
# M6 for odd m: the intended `ModelO` of a counterexample (assembly of G-A … G-D)

* `chi` is the orientation table of the counterexample's own labels (`LayerLab.chi`); its fields `chi_rot`,
  `chi_cycle`, `chi_swap`, `nest`, `noChain` are `LayerBasic`'s copies of ENCBLEAN's ModelBasic.
* A perturbation `η > 0` (`exists_perturbation`, with `v = π/m`) gives the phases `θ'ᵢ = ψᵢ + iη ∈ [0, 2π/m)`,
  the bits `hbᵢ = [θ'ᵢ < π/m]` and the phases modulo `π/m`, `ψ'ᵢ = θ'ᵢ − hbitᵢ·π/m ∈ [0, π/m)`.
* `(r, ψ', φ)` is a `PolarData (2m) t c` (`polarDataP`): the half-sector grid of `2m` directions per layer, on which
  the label `liftO hb (i,k) = (i, 2k + hbitᵢ)` is the perturbed point `L.Pη η (i,k)` (`P_liftO`).
* Rules A/B: ArcBridge's copy `polar_ruleA/B` at `2m` gives the sign of the perturbed triple, and (C1) moves it to
  the counterexample's own triple.
Nothing here needs `m` odd; the odd encoder (M3) does.
-/

namespace EncB.Geo7
open ErdosSzekeres ErdosSzekeres.LayerLemma

variable {m t : ℕ} {T : Finset Point} {c : Point}

/-- Perturbed phase. -/
noncomputable def thP (L : LayerLab m t T c) (η : ℝ) (i : ℕ) : ℝ := L.ψ i + (i : ℝ) * η

/-- The half-sector bit `[θ'ᵢ < π/m]`. -/
noncomputable def hbP (L : LayerLab m t T c) (η : ℝ) (i : ℕ) : Bool := decide (thP L η i < Real.pi / m)

/-- The phase modulo `π/m`. -/
noncomputable def psiP (L : LayerLab m t T c) (η : ℝ) (i : ℕ) : ℝ :=
  if hbP L η i then thP L η i else thP L η i - Real.pi / m

/-- The integer half-sector index of the bit. -/
def hz (b : Bool) : ℤ := if b then 0 else 1

theorem thP_eq (L : LayerLab m t T c) (η : ℝ) (i : ℕ) :
    thP L η i = psiP L η i + (hz (hbP L η i) : ℝ) * (Real.pi / m) := by
  unfold psiP hz
  split <;> push_cast <;> ring

theorem two_pi_div_two_mul (m : ℕ) : 2 * Real.pi / ((2 * m : ℕ) : ℝ) = Real.pi / m := by
  push_cast
  rcases Nat.eq_zero_or_pos m with rfl | hm
  · simp
  · have : (m : ℝ) ≠ 0 := by exact_mod_cast hm.ne'
    field_simp

/-- Conditions (C2), (C3) and `η > 0` on a perturbation. -/
structure GoodEta (L : LayerLab m t T c) (η : ℝ) : Prop where
  pos : 0 < η
  generic : ∀ i j, i < t → j < t → i ≠ j → ∀ k : ℤ,
    (L.ψ i + (i : ℝ) * η) - (L.ψ j + (j : ℝ) * η) ≠ k * (Real.pi / m)
  lt_u : ∀ i, i < t → L.ψ i + (i : ℝ) * η < 2 * Real.pi / m

theorem thP_nonneg (L : LayerLab m t T c) {η : ℝ} (hη : 0 < η) (i : ℕ) : 0 ≤ thP L η i := by
  unfold thP
  have := L.ψ_nonneg i
  positivity

theorem psiP_nonneg (L : LayerLab m t T c) {η : ℝ} (hη : 0 < η) (i : ℕ) : 0 ≤ psiP L η i := by
  unfold psiP hbP
  split
  · exact thP_nonneg L hη i
  · next h =>
    simp only [decide_eq_true_eq, not_lt] at h
    linarith

theorem hbP_zero (L : LayerLab m t T c) (η : ℝ) (hm : 0 < m) : hbP L η 0 = true := by
  have hpos : 0 < Real.pi / m := div_pos Real.pi_pos (by exact_mod_cast hm)
  simp only [hbP, thP, L.ψ_zero, Nat.cast_zero, zero_mul, add_zero, decide_eq_true_eq]
  exact hpos

theorem psiP_zero (L : LayerLab m t T c) (η : ℝ) (hm : 0 < m) : psiP L η 0 = 0 := by
  simp only [psiP, hbP_zero L η hm, if_true, thP, L.ψ_zero, Nat.cast_zero, zero_mul, add_zero]

/-- Equal phases modulo `π/m` force equal layers (from (C2)). -/
theorem psiP_inj (L : LayerLab m t T c) {η : ℝ} (hg : GoodEta L η) {i j : ℕ} (hi : i < t) (hj : j < t)
    (h : psiP L η i = psiP L η j) : i = j := by
  by_contra hij
  apply hg.generic i j hi hj hij (hz (hbP L η i) - hz (hbP L η j))
  have e1 := thP_eq L η i
  have e2 := thP_eq L η j
  simp only [thP] at e1 e2
  push_cast
  rw [e1, e2, h]
  ring

/-- **The half-sector polar data** of a good perturbation. -/
noncomputable def polarDataP (L : LayerLab m t T c) {η : ℝ} (hg : GoodEta L η) (hm : 0 < m) :
    PolarData (2 * m) t c where
  r := L.r
  ψ := psiP L η
  φ := L.φ
  r_pos := L.r_pos
  r_anti := L.r_anti
  ψ_zero := psiP_zero L η hm
  ψ_pos := by
    intro i hi0 hi
    rcases (psiP_nonneg L hg.pos i).lt_or_eq with h | h
    · exact h
    · exfalso
      have h0t : 0 < t := lt_of_le_of_lt (Nat.zero_le i) hi
      have := psiP_inj L hg hi h0t (by rw [← h, psiP_zero L η hm])
      omega
  ψ_lt := by
    intro i hi
    rw [two_pi_div_two_mul]
    have hlt := hg.lt_u i hi
    unfold psiP hbP
    split
    · next h => simpa using h
    · have hm' : (m : ℝ) ≠ 0 := by exact_mod_cast hm.ne'
      have : 2 * Real.pi / m = Real.pi / m + Real.pi / m := by field_simp; ring
      simp only [thP] at hlt ⊢
      linarith
  ψ_inj := fun i j hi hj h => psiP_inj L hg hi hj h

/-- On the half-sector grid, the lifted label is the perturbed point. -/
theorem P_liftO (L : LayerLab m t T c) {η : ℝ} (hg : GoodEta L η) (hm : 0 < m) (a : EncB.Pt) :
    (polarDataP L hg hm).P (EncB.liftO (hbP L η) a) = L.Pη η a := by
  simp only [PolarData.P, polarDataP, LayerLab.Pη, EncB.liftO, EncB.hbit]
  congr 1
  rw [two_pi_div_two_mul]
  have hm' : (m : ℝ) ≠ 0 := by exact_mod_cast hm.ne'
  unfold psiP
  split
  · simp only [thP]
    push_cast
    field_simp
    ring
  · simp only [thP]
    push_cast
    field_simp
    ring

/-- `ModelO`'s rules A/B for the counterexample's `chi`, from ArcBridge's copy at `2m` and (C1). -/
theorem chi_of_perturbed (L : LayerLab m t T c) {η : ℝ} (hg : GoodEta L η) (hm : 0 < m)
    (hsign : ∀ a b d, EncB.PtOk m t a → EncB.PtOk m t b → EncB.PtOk m t d → EncB.Distinct3 a b d →
      (0 < orient (L.Pη η a) (L.Pη η b) (L.Pη η d) ↔ 0 < orient (L.P a) (L.P b) (L.P d)))
    {a b d : EncB.Pt} (ha : EncB.PtOk m t a) (hb : EncB.PtOk m t b) (hd : EncB.PtOk m t d)
    (hdist : EncB.Distinct3 a b d)
    (h : (polarDataP L hg hm).chi (EncB.liftO (hbP L η) a) (EncB.liftO (hbP L η) b)
      (EncB.liftO (hbP L η) d) = true) : L.chi a b d = true := by
  simp only [PolarData.chi, P_liftO, decide_eq_true_eq] at h
  simp only [LayerLab.chi, decide_eq_true_eq]
  exact (hsign a b d ha hb hd hdist).1 h

theorem ptOk_liftO {hb : ℕ → Bool} {a : EncB.Pt} (ha : EncB.PtOk m t a) :
    EncB.PtOk (2 * m) t (EncB.liftO hb a) :=
  ⟨ha.1, EncB.liftO_snd_lt ha.2⟩

/-- **M6 for any m ≥ 3** (used at odd m): a counterexample yields a `ModelO m K t`. -/
theorem modelO_of_counterexample {m K t : ℕ} (hm : 3 ≤ m) (hK4 : 4 ≤ K) (hK : K ≤ 2 * m)
    {T : Finset Point} {c : Point} (hgp : GeneralPosition T) (hc : c ∉ T)
    (hinv : Invariant (rotAbout c (2 * Real.pi / m)) T) (hno : ¬ HasConvexNGon K T)
    (hcard : T.card = m * t) : Nonempty (EncB.ModelO m K t) := by
  have hm0 : 0 < m := by omega
  obtain ⟨L⟩ := layerLab_of_counterexample (by omega) hK hc hinv hno hcard
  have hv : 0 < Real.pi / m := div_pos Real.pi_pos (by exact_mod_cast hm0)
  obtain ⟨η, hη, hsign, hgen, hlt⟩ := exists_perturbation L hv
    (fun a b d ha hb hd hdist => lab_orient_ne_zero hm hgp hc L a b d ha hb hd hdist)
  have hg : GoodEta L η := ⟨hη, hgen, hlt⟩
  let D := polarDataP L hg hm0
  have hm2 : 3 ≤ 2 * m := by omega
  have he2 : Even (2 * m) := even_two_mul m
  exact ⟨{
    chi := L.chi
    psiLt := D.psiLt
    hb := hbP L η
    psiLt_irrefl := fun i => by simp [PolarData.psiLt]
    psiLt_trans := fun i j k h1 h2 => by
      simp only [PolarData.psiLt, decide_eq_true_eq] at h1 h2 ⊢
      exact h1.trans h2
    psiLt_total := fun i j hi hj hij => by
      simp only [PolarData.psiLt, decide_eq_true_eq]
      exact lt_or_gt_of_ne fun e => hij (D.ψ_inj i j hi hj e)
    psiLt_zero := fun i hi hit => by
      simp only [PolarData.psiLt, decide_eq_true_eq, D.ψ_zero]
      exact D.ψ_pos i hi hit
    hb_zero := hbP_zero L η hm0
    chi_rot := lab_chi_rot hm L
    chi_cycle := lab_chi_cycle L
    chi_swap := lab_chi_swap hm hgp hc L
    ruleA := fun a b d ha hb hd hdist hA =>
      chi_of_perturbed L hg hm0 hsign ha hb hd hdist
        (polar_ruleA hm2 he2 D _ _ _ (ptOk_liftO ha) (ptOk_liftO hb) (ptOk_liftO hd)
          (EncB.RulesO.distinct3_lift hdist) hA)
    ruleB := fun a b d ha hb hd hdist hB hba hbd =>
      chi_of_perturbed L hg hm0 hsign ha hb hd hdist
        (polar_ruleB hm2 he2 D _ _ _ (ptOk_liftO ha) (ptOk_liftO hb) (ptOk_liftO hd)
          (EncB.RulesO.distinct3_lift hdist) hB hba hbd)
    nest := lab_nest hm hK hgp hc hinv hno L
    noChain := lab_noChain hm hK4 hK hgp hc hinv hno L }⟩

end EncB.Geo7

#print axioms EncB.Geo7.modelO_of_counterexample
