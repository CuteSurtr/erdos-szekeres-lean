import D3Encoding.Instance
import ETVEncoding.Dimacs
import ErdosSzekeres.OrientationConvexity
import ErdosSzekeres.Suk.FourPoint
import Mathlib.Data.Real.Sqrt

/-!
# Labelled D3 configurations

A `LabelledD3 t` is the convention of `results/E`: points `P 0, …, P (3 t - 1)` (orbit `o`
is `P (3 o), P (3 o + 1), P (3 o + 2)`), the centre `P (3 t) = c`, the rotation `rotC c` by
120° about `c` acting as `rot`, the reflection `reflC c u` in the line through `c` with unit
direction `u` acting as `sigma`, all `3 t + 1` points (centre included) in general position,
and the labelling normal form (sector and angular order) as orientation facts.

`dimacsSatisfiable_of_labelled`: if the `3 t` points of such a configuration have no convex
`K`-gon (`K ≥ 5`), then the clauses of `d3cnf.py (3 t) K` are satisfiable.
-/

open ErdosSzekeres

namespace D3

/-! ### Signs -/

noncomputable def sgn (x : ℝ) : ℤ := if 0 < x then 1 else if x < 0 then -1 else 0

theorem sgn_neg (x : ℝ) : sgn (-x) = -sgn x := by
  unfold sgn
  rcases lt_trichotomy x 0 with h | rfl | h
  · simp [h, not_lt.2 h.le]
  · simp
  · simp [h, not_lt.2 h.le]

theorem sgn_pm {x : ℝ} (h : x ≠ 0) : sgn x = 1 ∨ sgn x = -1 := by
  unfold sgn
  rcases lt_or_gt_of_ne h with h | h
  · simp [h, not_lt.2 h.le]
  · simp [h]

theorem sgn_eq_one {x : ℝ} : sgn x = 1 ↔ 0 < x := by
  unfold sgn
  by_cases h1 : 0 < x
  · simp [h1]
  · by_cases h2 : x < 0 <;> simp [h1, h2]

theorem sgn_eq_neg_one {x : ℝ} : sgn x = -1 ↔ x < 0 := by
  unfold sgn
  by_cases h1 : 0 < x
  · simp [h1, not_lt.2 h1.le]
  · by_cases h2 : x < 0 <;> simp [h1, h2]

theorem sgn_mul_pos {x y : ℝ} (hx : x ≠ 0) (hy : y ≠ 0) : 0 < sgn x * sgn y ↔ 0 < x * y := by
  rcases lt_or_gt_of_ne hx with h1 | h1 <;> rcases lt_or_gt_of_ne hy with h2 | h2
  · simp [sgn, h1, h2, not_lt.2 h1.le, not_lt.2 h2.le, mul_pos_of_neg_of_neg h1 h2]
  · simp [sgn, h1, h2, not_lt.2 h1.le, (mul_neg_of_neg_of_pos h1 h2).le, not_lt.2]
  · simp [sgn, h1, h2, not_lt.2 h2.le, (mul_neg_of_pos_of_neg h1 h2).le, not_lt.2]
  · simp [sgn, h1, h2, mul_pos h1 h2]

theorem sgn_mul_neg {x y : ℝ} (hx : x ≠ 0) (hy : y ≠ 0) : sgn x * sgn y < 0 ↔ x * y < 0 := by
  rcases lt_or_gt_of_ne hx with h1 | h1 <;> rcases lt_or_gt_of_ne hy with h2 | h2
  · simp [sgn, h1, h2, not_lt.2 h1.le, not_lt.2 h2.le, (mul_pos_of_neg_of_neg h1 h2).le, not_lt.2]
  · simp [sgn, h1, h2, not_lt.2 h1.le, mul_neg_of_neg_of_pos h1 h2]
  · simp [sgn, h1, h2, not_lt.2 h2.le, mul_neg_of_pos_of_neg h1 h2]
  · simp [sgn, h1, h2, (mul_pos h1 h2).le, not_lt.2]

/-! ### The rotation and the reflection -/

/-- Rotation by 120° (counterclockwise) about `c`. -/
noncomputable def rotC (c p : Point) : Point :=
  ![c 0 + (-(1 / 2) * (p 0 - c 0) - (Real.sqrt 3 / 2) * (p 1 - c 1)),
    c 1 + ((Real.sqrt 3 / 2) * (p 0 - c 0) - (1 / 2) * (p 1 - c 1))]

/-- Reflection in the line through `c` with direction `u` (a unit vector). -/
noncomputable def reflC (c u p : Point) : Point :=
  ![c 0 + 2 * ((p 0 - c 0) * u 0 + (p 1 - c 1) * u 1) * u 0 - (p 0 - c 0),
    c 1 + 2 * ((p 0 - c 0) * u 0 + (p 1 - c 1) * u 1) * u 1 - (p 1 - c 1)]

theorem sqrt3_sq : Real.sqrt 3 * Real.sqrt 3 = 3 := Real.mul_self_sqrt (by norm_num)

theorem orient_rotC (c a b d : Point) :
    orient (rotC c a) (rotC c b) (rotC c d) = orient a b d := by
  simp only [orient, rotC, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
  linear_combination (1 / 4 : ℝ) * ((b 0 - a 0) * (d 1 - a 1) - (b 1 - a 1) * (d 0 - a 0)) *
    sqrt3_sq

theorem orient_reflC (c u a b d : Point) (hu : u 0 ^ 2 + u 1 ^ 2 = 1) :
    orient (reflC c u a) (reflC c u b) (reflC c u d) = -orient a b d := by
  simp only [orient, reflC, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
  linear_combination (-2 : ℝ) * ((b 0 - a 0) * (d 1 - a 1) - (b 1 - a 1) * (d 0 - a 0)) * hu

theorem orient_center_rot (c a : Point) :
    orient c a (rotC c a) = Real.sqrt 3 / 2 * ((a 0 - c 0) ^ 2 + (a 1 - c 1) ^ 2) := by
  simp only [orient, rotC, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
  ring

theorem orient_center_rot2 (c a : Point) :
    orient c a (rotC c (rotC c a)) = -(Real.sqrt 3 / 2 * ((a 0 - c 0) ^ 2 + (a 1 - c 1) ^ 2)) := by
  simp only [orient, rotC, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
  ring

/-! ### Labelled configurations -/

/-- A D3-symmetric configuration of `3 t` points with its centre, in the labelling of
`results/E` (see the module docstring). -/
structure LabelledD3 (t : ℕ) where
  P : ℕ → Point
  c : Point
  u : Point
  hc : P (3 * t) = c
  hu : u 0 ^ 2 + u 1 ^ 2 = 1
  rot_eq : ∀ i, i < 3 * t + 1 → P (rot (3 * t) 1 i) = rotC c (P i)
  refl_eq : ∀ i, i < 3 * t + 1 → P (sigma t (3 * t) i) = reflC c u (P i)
  gp : ∀ i j k, i < 3 * t + 1 → j < 3 * t + 1 → k < 3 * t + 1 → i ≠ j → i ≠ k → j ≠ k →
    orient (P i) (P j) (P k) ≠ 0
  sector : ∀ o, 1 ≤ o → o < t → 0 < orient c (P 0) (P (3 * o)) ∧ orient c (P 1) (P (3 * o)) < 0
  order : ∀ o o2, 1 ≤ o → o < o2 → o2 < t → 0 < orient c (P (3 * o)) (P (3 * o2))

namespace LabelledD3

variable {t : ℕ} (L : LabelledD3 t)

/-- The set of the `3 t` points (the centre is not a point of the set). -/
noncomputable def pts : Finset Point := (Finset.range (3 * t)).image L.P

noncomputable def chi : ℕ → ℕ → ℕ → ℤ := fun i j k => sgn (orient (L.P i) (L.P j) (L.P k))

theorem rot2 {i : ℕ} (hi : i < 3 * t + 1) : rot (3 * t) 2 i = rot (3 * t) 1 (rot (3 * t) 1 i) := by
  unfold rot; split_ifs <;> omega

theorem P_rot0 {i : ℕ} (hi : i < 3 * t + 1) : L.P (rot (3 * t) 0 i) = L.P i := by
  rw [rot_zero hi]

theorem P_rot2 {i : ℕ} (hi : i < 3 * t + 1) :
    L.P (rot (3 * t) 2 i) = rotC L.c (rotC L.c (L.P i)) := by
  rw [rot2 hi, L.rot_eq _ (rot_lt hi), L.rot_eq _ hi]

theorem orient_swap12 (a b d : Point) : orient b a d = -orient a b d := by
  unfold orient; ring

theorem chirotope : Chirotope t L.chi where
  swap12 a b c := by simp only [chi]; rw [orient_swap12, sgn_neg]
  swap23 a b c := by simp only [chi]; rw [orient_swap, sgn_neg]
  sign a b c ha hb hc hab hac hbc := sgn_pm (L.gp a b c ha hb hc hab hac hbc)
  equiv g hg a b c ha hb hc := by
    simp only [group, List.mem_cons, List.not_mem_nil, or_false] at hg
    simp only [chi]
    rcases hg with rfl | rfl | rfl | rfl | rfl | rfl
    · simp only [L.P_rot0 ha, L.P_rot0 hb, L.P_rot0 hc, one_mul]
    · simp only [L.rot_eq _ ha, L.rot_eq _ hb, L.rot_eq _ hc, orient_rotC, one_mul]
    · simp only [L.P_rot2 ha, L.P_rot2 hb, L.P_rot2 hc, orient_rotC, one_mul]
    · simp only [L.P_rot0 (sigma_lt ha), L.P_rot0 (sigma_lt hb), L.P_rot0 (sigma_lt hc),
        L.refl_eq _ ha, L.refl_eq _ hb, L.refl_eq _ hc, orient_reflC _ _ _ _ _ L.hu, sgn_neg]
      ring
    · simp only [L.rot_eq _ (sigma_lt ha), L.rot_eq _ (sigma_lt hb), L.rot_eq _ (sigma_lt hc),
        orient_rotC, L.refl_eq _ ha, L.refl_eq _ hb, L.refl_eq _ hc, orient_reflC _ _ _ _ _ L.hu,
        sgn_neg]
      ring
    · simp only [L.P_rot2 (sigma_lt ha), L.P_rot2 (sigma_lt hb), L.P_rot2 (sigma_lt hc),
        orient_rotC, L.refl_eq _ ha, L.refl_eq _ hb, L.refl_eq _ hc, orient_reflC _ _ _ _ _ L.hu,
        sgn_neg]
      ring

theorem orient_four (p q r x : Point) :
    orient p q r = orient x q r + orient p x r + orient p q x := by
  unfold orient; ring

theorem a4 : A4 (3 * t + 1) L.chi := by
  intro p q r x hp hq hr hx hpq hpr hpx hqr hqx hrx s hs h1 h2 h3
  simp only [chi] at *
  rw [orient_four (L.P p) (L.P q) (L.P r) (L.P x)]
  rcases hs with rfl | rfl
  · rw [sgn_eq_one] at *; linarith
  · rw [sgn_eq_neg_one] at *; linarith

theorem plucker (x y1 y2 y3 y4 : Point) :
    orient x y1 y2 * orient x y3 y4 - orient x y1 y3 * orient x y2 y4 +
      orient x y1 y4 * orient x y2 y3 = 0 := by
  unfold orient; ring

theorem gp3 : GP3 (3 * t + 1) L.chi := by
  intro x y1 y2 y3 y4 hx h1 h2 h3 h4 n1 n2 n3 n4 n12 n13 n14 n23 n24 n34
  have g := L.gp
  have d12 := g x y1 y2 hx h1 h2 n1 n2 n12
  have d34 := g x y3 y4 hx h3 h4 n3 n4 n34
  have d13 := g x y1 y3 hx h1 h3 n1 n3 n13
  have d24 := g x y2 y4 hx h2 h4 n2 n4 n24
  have d14 := g x y1 y4 hx h1 h4 n1 n4 n14
  have d23 := g x y2 y3 hx h2 h3 n2 n3 n23
  have pl := plucker (L.P x) (L.P y1) (L.P y2) (L.P y3) (L.P y4)
  simp only [chi]
  rw [sgn_mul_pos d12 d34, sgn_mul_pos d14 d23, sgn_mul_neg d12 d34, sgn_mul_neg d14 d23]
  have e1 : 0 < -(sgn (orient (L.P x) (L.P y1) (L.P y3)) * sgn (orient (L.P x) (L.P y2) (L.P y4)))
      ↔ orient (L.P x) (L.P y1) (L.P y3) * orient (L.P x) (L.P y2) (L.P y4) < 0 := by
    rw [neg_pos, sgn_mul_neg d13 d24]
  have e2 : -(sgn (orient (L.P x) (L.P y1) (L.P y3)) * sgn (orient (L.P x) (L.P y2) (L.P y4))) < 0
      ↔ 0 < orient (L.P x) (L.P y1) (L.P y3) * orient (L.P x) (L.P y2) (L.P y4) := by
    rw [neg_lt_zero, sgn_mul_pos d13 d24]
  rw [e1, e2]
  constructor
  · rintro ⟨a, b, c⟩; linarith
  · rintro ⟨a, b, c⟩; linarith

theorem rot_ne_center {i : ℕ} (hi : i < 3 * t) (k : ℕ) : rot (3 * t) k i ≠ 3 * t := by
  have := rot_lt' (k := k) hi; omega

theorem centerFacts : CenterFacts t L.chi := by
  intro a ha
  have hne1 : orient (L.P (3 * t)) (L.P a) (L.P (rot (3 * t) 1 a)) ≠ 0 :=
    L.gp _ _ _ (by omega) (by omega) (rot_lt (by omega)) (by omega)
      (Ne.symm (rot_ne_center ha 1)) (Ne.symm (rot_ne ha (by omega) (by omega)))
  have hne2 : orient (L.P (3 * t)) (L.P a) (L.P (rot (3 * t) 2 a)) ≠ 0 :=
    L.gp _ _ _ (by omega) (by omega) (rot_lt (by omega)) (by omega)
      (Ne.symm (rot_ne_center ha 2)) (Ne.symm (rot_ne ha (by omega) (by omega)))
  have s3 : 0 < Real.sqrt 3 / 2 := by positivity
  simp only [chi]
  rw [L.rot_eq _ (by omega), L.hc, orient_center_rot] at hne1 ⊢
  rw [L.P_rot2 (by omega), L.hc, orient_center_rot2] at hne2
  rw [L.P_rot2 (by omega), orient_center_rot2]
  constructor
  · rw [sgn_eq_one]
    rcases (mul_nonneg s3.le (by positivity :
      (0 : ℝ) ≤ (L.P a 0 - L.c 0) ^ 2 + (L.P a 1 - L.c 1) ^ 2)).lt_or_eq with h | h
    · exact h
    · exact absurd h.symm hne1
  · rw [sgn_eq_neg_one]
    rcases (mul_nonneg s3.le (by positivity :
      (0 : ℝ) ≤ (L.P a 0 - L.c 0) ^ 2 + (L.P a 1 - L.c 1) ^ 2)).lt_or_eq with h | h
    · linarith
    · exact absurd (by rw [← h]; ring) hne2

theorem sectorOrder : SectorOrder t L.chi := by
  refine ⟨fun o h1 h2 => ?_, fun o o2 h1 h2 h3 => ?_⟩
  · simp only [chi, L.hc]
    exact ⟨sgn_eq_one.2 (L.sector o h1 h2).1, sgn_eq_neg_one.2 (L.sector o h1 h2).2⟩
  · simp only [chi, L.hc]
    exact sgn_eq_one.2 (L.order o o2 h1 h2 h3)

theorem injOn : Set.InjOn L.P ↑(Finset.range (3 * t)) := by
  intro i hi j hj hij
  simp only [Finset.coe_range, Set.mem_Iio] at hi hj
  by_contra hne
  apply L.gp i j (3 * t) (by omega) (by omega) (by omega) hne (by omega) (by omega)
  rw [hij]; unfold orient; ring

/-- Sign-level: four points with no one inside the triangle of the other three are convex. -/
theorem quad_of_noIns {a b c d : ℕ} (ha : a < 3 * t + 1) (hb : b < 3 * t + 1)
    (hc : c < 3 * t + 1) (hd : d < 3 * t + 1) (hab : a < b) (hbc : b < c) (hcd : c < d)
    (F1 : ¬Ins L.chi d a b c) (F2 : ¬Ins L.chi c a b d) (F3 : ¬Ins L.chi b a c d)
    (F4 : ¬Ins L.chi a b c d) :
    QuadConvexSigns (decide (0 < orient (L.P a) (L.P b) (L.P c)))
      (decide (0 < orient (L.P a) (L.P b) (L.P d))) (decide (0 < orient (L.P a) (L.P c) (L.P d)))
      (decide (0 < orient (L.P b) (L.P c) (L.P d))) := by
  have hχ := L.chirotope
  have s12 := hχ.swap12
  have s23 := hχ.swap23
  have e1 := s12 a c d; have e2 := s12 a c b; have e3 := s23 a b c; have e4 := s12 a d b
  have e5 := s23 a b d; have e6 := s12 b d c; have e7 := s23 b c d; have e8 := s12 b d a
  have e9 := s23 b a d; have e10 := s12 a b d; have e11 := s12 c d a; have e12 := s23 c a d
  have e13 := s12 b c a; have e14 := s23 b a c; have e15 := s12 a b c; have e16 := s12 a d c
  have e17 := s23 a c d; have e18 := s23 c b d; have e19 := s12 b c d
  unfold Ins at F1 F2 F3 F4
  have w1 := hχ.sign a b c ha hb hc (by omega) (by omega) (by omega)
  have w2 := hχ.sign a b d ha hb hd (by omega) (by omega) (by omega)
  have w3 := hχ.sign a c d ha hc hd (by omega) (by omega) (by omega)
  have w4 := hχ.sign b c d hb hc hd (by omega) (by omega) (by omega)
  have q : ∀ i j k, i < 3 * t + 1 → j < 3 * t + 1 → k < 3 * t + 1 → i ≠ j → i ≠ k → j ≠ k →
      decide (0 < orient (L.P i) (L.P j) (L.P k)) = decide (L.chi i j k = 1) := by
    intro i j k _ _ _ _ _ _
    simp only [chi, sgn_eq_one]
  rw [q a b c ha hb hc (by omega) (by omega) (by omega), q a b d ha hb hd (by omega) (by omega)
    (by omega), q a c d ha hc hd (by omega) (by omega) (by omega),
    q b c d hb hc hd (by omega) (by omega) (by omega)]
  unfold QuadConvexSigns
  rcases w1 with h1 | h1 <;> rcases w2 with h2 | h2 <;> rcases w3 with h3 | h3 <;>
    rcases w4 with h4 | h4 <;> simp only [h1, h2, h3, h4] <;> simp <;> omega

/-- A convex `K`-set of the chirotope is a convex `K`-gon of the points. -/
theorem hasConvexNGon_of_convAll {X : List ℕ} (hX : X.Pairwise (· < ·)) (hK : 4 ≤ X.length)
    (hXP : ∀ x ∈ X, x < 3 * t) (h : ConvAll L.chi X) : HasConvexNGon X.length L.pts := by
  classical
  set G := X.toFinset with hG
  have hGN : ∀ i ∈ G, i < 3 * t := fun i hi => hXP i (List.mem_toFinset.1 hi)
  have hinj : Set.InjOn L.P ↑G := by
    intro i hi j hj hij
    exact L.injOn (by simpa using hGN i hi) (by simpa using hGN j hj) hij
  have hcard : G.card = X.length := List.toFinset_card_of_nodup (hX.imp fun h => Nat.ne_of_lt h)
  refine ⟨G.image L.P, ?_, ?_, ?_⟩
  · intro p hp
    simp only [Finset.mem_image] at hp
    obtain ⟨i, hi, rfl⟩ := hp
    exact Finset.mem_image_of_mem _ (Finset.mem_range.2 (hGN i hi))
  · rw [Finset.card_image_of_injOn hinj, hcard]
  · apply Suk.convexPosition_of_four_subsets (by rw [Finset.card_image_of_injOn hinj]; omega)
    intro T hT hT4
    obtain ⟨U, hUG, rfl⟩ := Finset.subset_image_iff.1 hT
    have hU4 : U.card = 4 := by
      rw [Finset.card_image_of_injOn (hinj.mono (by simpa using hUG))] at hT4
      exact hT4
    let e := U.orderEmbOfFin hU4
    have hem (i : Fin 4) : e i ∈ G := hUG (Finset.orderEmbOfFin_mem U hU4 i)
    have hT' : U.image L.P = {L.P (e 0), L.P (e 1), L.P (e 2), L.P (e 3)} := by
      rw [← Finset.image_orderEmbOfFin_univ U hU4, Finset.image_image]
      have hf : (Finset.univ : Finset (Fin 4)) = {0, 1, 2, 3} := by decide
      rw [hf]
      simp [e]
    rw [hT']
    have h01 : e 0 < e 1 := e.strictMono (by decide)
    have h12 : e 1 < e 2 := e.strictMono (by decide)
    have h23 : e 2 < e 3 := e.strictMono (by decide)
    have m : ∀ i : Fin 4, e i ∈ X := fun i => List.mem_toFinset.1 (hem i)
    have b : ∀ i : Fin 4, e i < 3 * t + 1 := fun i => by have := hGN _ (hem i); omega
    have gp := L.gp
    rw [convexPosition_four_iff_signs _ _ _ _
      (gp _ _ _ (b 0) (b 1) (b 2) (by omega) (by omega) (by omega))
      (gp _ _ _ (b 0) (b 1) (b 3) (by omega) (by omega) (by omega))
      (gp _ _ _ (b 0) (b 2) (b 3) (by omega) (by omega) (by omega))
      (gp _ _ _ (b 1) (b 2) (b 3) (by omega) (by omega) (by omega))]
    exact L.quad_of_noIns (b 0) (b 1) (b 2) (b 3) h01 h12 h23
      (h _ (m 3) _ (m 0) _ (m 1) _ (m 2) (by omega) (by omega) (by omega) h01 h12)
      (h _ (m 2) _ (m 0) _ (m 1) _ (m 3) (by omega) (by omega) (by omega) h01 (by omega))
      (h _ (m 1) _ (m 0) _ (m 2) _ (m 3) (by omega) (by omega) (by omega) (by omega) h23)
      (h _ (m 0) _ (m 1) _ (m 2) _ (m 3) (by omega) (by omega) (by omega) h12 h23)

end LabelledD3

/-- **Soundness of `d3cnf.py`, point-set level.** A labelled D3 configuration of `3 t`
points with no convex `K`-gon (`K ≥ 5`) satisfies the clauses of `d3cnf.py (3 t) K`. -/
theorem dimacsSatisfiable_of_labelled {t K : ℕ} (L : LabelledD3 t) (hG : GroupClosed t)
    (hK : 5 ≤ K) (hno : ¬HasConvexNGon K L.pts) :
    ETV.DimacsSatisfiable (d3Cnf (3 * t) K).2.2 := by
  have M : Model t K L.chi :=
    ⟨hK, hG, L.chirotope, fun X hX hlen hXP hc =>
      hno (hlen ▸ L.hasConvexNGon_of_convAll hX (by omega) hXP hc)⟩
  obtain ⟨ν, hν⟩ := d3Cnf_sat M L.a4 L.gp3 L.centerFacts L.sectorOrder
  refine ⟨ν, fun c hc => ?_⟩
  obtain ⟨l, hl, h⟩ := hν c hc
  exact ⟨l, hl, h⟩

/-- The 33-point instance: UNSAT of `d3cnf.py 33 7` excludes heptagon-free labelled D3
configurations. -/
theorem hasConvexNGon_of_unsat_d3 (h : ¬ETV.DimacsSatisfiable (d3Cnf 33 7).2.2)
    (L : LabelledD3 11) : HasConvexNGon 7 L.pts := by
  by_contra hno
  have hs := dimacsSatisfiable_of_labelled (K := 7) L groupClosed_11 (by norm_num) hno
  rw [show 3 * 11 = 33 from rfl] at hs
  exact h hs

end D3
