import LeanLB.G.Bridge

/-!
# Certified integer approximations of points with coordinates in `ℤ[t]`

A point is given exactly by `(X, Y)`, `X, Y ∈ ℤ³`, standing for `(u, v) = (X(t), Y(t))` with
`X(t) = X₀ + X₁t + X₂t²` (`evT`), and in the plane for `(u/2, s·v)` (`embT t s`). The checker works on
integer approximations `(Ũ, Ṽ)` of `(sc·u, sc·v)` (translated to natural numbers), each within `1`
(`apxOK`, certified from rational bounds `lo/D < t < (lo + 1)/D`). If all approximations are
at most `Mx`, an approximate orientation larger than `E = 8·Mx + 8` certifies a positive orientation
(`opA_sound`), and the order `abA` is certified with the margin `2 + 2c` (`abA_sound`).
-/

namespace LeanLB.G

open ErdosSzekeres

/-- `r₀ + r₁t + r₂t²`. -/
noncomputable def evT (t : ℝ) (r : ℤ × ℤ × ℤ) : ℝ := (r.1 : ℝ) + (r.2.1 : ℝ) * t + (r.2.2 : ℝ) * t ^ 2

/-- Lower bound for `D²·(r₀ + r₁t + r₂t²)` when `lo/D < t < (lo + 1)/D`, `0 < lo`. -/
def lowB (lo D : ℤ) (r : ℤ × ℤ × ℤ) : ℤ :=
  D * D * r.1 + min (r.2.1 * lo * D) (r.2.1 * (lo + 1) * D) +
    min (r.2.2 * lo * lo) (r.2.2 * (lo + 1) * (lo + 1))

/-- Upper bound for `D²·(r₀ + r₁t + r₂t²)`. -/
def uppB (lo D : ℤ) (r : ℤ × ℤ × ℤ) : ℤ :=
  D * D * r.1 + max (r.2.1 * lo * D) (r.2.1 * (lo + 1) * D) +
    max (r.2.2 * lo * lo) (r.2.2 * (lo + 1) * (lo + 1))

theorem bounds_evT {t : ℝ} {lo D : ℤ} (hD : 0 < D) (hlo : 0 < lo)
    (h1 : (lo : ℝ) / D < t) (h2 : t < ((lo + 1 : ℤ) : ℝ) / D) (r : ℤ × ℤ × ℤ) :
    (lowB lo D r : ℝ) ≤ (D : ℝ) ^ 2 * evT t r ∧ (D : ℝ) ^ 2 * evT t r ≤ (uppB lo D r : ℝ) := by
  have hD' : (0 : ℝ) < D := by exact_mod_cast hD
  have hl0 : (0 : ℝ) < lo := by exact_mod_cast hlo
  set T := t * D with hT
  have hT1 : (lo : ℝ) < T := by rw [div_lt_iff₀ hD'] at h1; linarith
  have hT2 : T < ((lo + 1 : ℤ) : ℝ) := by rw [lt_div_iff₀ hD'] at h2; linarith
  push_cast at hT2
  have key : (D : ℝ) ^ 2 * evT t r = (D : ℝ) * D * r.1 + r.2.1 * T * D + r.2.2 * T ^ 2 := by
    unfold evT; rw [hT]; ring
  have hsq1 : (lo : ℝ) * lo ≤ T ^ 2 := by nlinarith
  have hsq2 : T ^ 2 ≤ ((lo : ℝ) + 1) * ((lo : ℝ) + 1) := by nlinarith
  rw [key]
  unfold lowB uppB
  push_cast
  constructor
  · have e1 : min ((r.2.1 : ℝ) * lo * D) (r.2.1 * (lo + 1) * D) ≤ r.2.1 * T * D := by
      rcases le_or_gt 0 (r.2.1 : ℝ) with hr | hr
      · have := mul_nonneg (mul_nonneg hr (sub_nonneg.mpr hT1.le)) hD'.le
        exact le_trans (min_le_left _ _) (by linarith)
      · have := mul_nonneg (mul_nonneg (neg_nonneg.mpr hr.le) (sub_nonneg.mpr hT2.le)) hD'.le
        exact le_trans (min_le_right _ _) (by linarith)
    have e2 : min ((r.2.2 : ℝ) * lo * lo) (r.2.2 * (lo + 1) * (lo + 1)) ≤ r.2.2 * T ^ 2 := by
      rcases le_or_gt 0 (r.2.2 : ℝ) with hr | hr
      · have := mul_nonneg hr (sub_nonneg.mpr hsq1)
        exact le_trans (min_le_left _ _) (by linarith)
      · have := mul_nonneg (neg_nonneg.mpr hr.le) (sub_nonneg.mpr hsq2)
        exact le_trans (min_le_right _ _) (by linarith)
    linarith
  · have e1 : (r.2.1 : ℝ) * T * D ≤ max ((r.2.1 : ℝ) * lo * D) (r.2.1 * (lo + 1) * D) := by
      rcases le_or_gt 0 (r.2.1 : ℝ) with hr | hr
      · have := mul_nonneg (mul_nonneg hr (sub_nonneg.mpr hT2.le)) hD'.le
        exact le_trans (by linarith) (le_max_right _ _)
      · have := mul_nonneg (mul_nonneg (neg_nonneg.mpr hr.le) (sub_nonneg.mpr hT1.le)) hD'.le
        exact le_trans (by linarith) (le_max_left _ _)
    have e2 : (r.2.2 : ℝ) * T ^ 2 ≤ max ((r.2.2 : ℝ) * lo * lo) (r.2.2 * (lo + 1) * (lo + 1)) := by
      rcases le_or_gt 0 (r.2.2 : ℝ) with hr | hr
      · have := mul_nonneg hr (sub_nonneg.mpr hsq2)
        exact le_trans (by linarith) (le_max_right _ _)
      · have := mul_nonneg (neg_nonneg.mpr hr.le) (sub_nonneg.mpr hsq1)
        exact le_trans (by linarith) (le_max_left _ _)
    linarith

/-- `n` approximates `sc·(r₀ + r₁t + r₂t²)` within `1`, certified from `lowB` and `uppB`. -/
def apxOK (lo D sc : ℤ) (r : ℤ × ℤ × ℤ) (n : ℤ) : Bool :=
  decide ((n - 1) * (D * D) ≤ sc * lowB lo D r) && decide (sc * uppB lo D r ≤ (n + 1) * (D * D))

theorem apxOK_sound {t : ℝ} {lo D sc : ℤ} (hD : 0 < D) (hlo : 0 < lo) (hsc : 0 < sc)
    (h1 : (lo : ℝ) / D < t) (h2 : t < ((lo + 1 : ℤ) : ℝ) / D) {r : ℤ × ℤ × ℤ} {n : ℤ}
    (h : apxOK lo D sc r n = true) : |(n : ℝ) - sc * evT t r| ≤ 1 := by
  unfold apxOK at h
  rw [Bool.and_eq_true, decide_eq_true_eq, decide_eq_true_eq] at h
  obtain ⟨hl, hu⟩ := h
  obtain ⟨bl, bu⟩ := bounds_evT hD hlo h1 h2 r
  have hD0 : (0 : ℝ) < D := by exact_mod_cast hD
  have hD' : (0 : ℝ) < (D : ℝ) ^ 2 := by positivity
  have hsc' : (0 : ℝ) < sc := by exact_mod_cast hsc
  have hl' : ((n : ℝ) - 1) * ((D : ℝ) * D) ≤ sc * lowB lo D r := by exact_mod_cast hl
  have hu' : (sc : ℝ) * uppB lo D r ≤ ((n : ℝ) + 1) * ((D : ℝ) * D) := by exact_mod_cast hu
  have a1 : ((n : ℝ) - 1) * (D : ℝ) ^ 2 ≤ sc * evT t r * (D : ℝ) ^ 2 := by
    have := mul_le_mul_of_nonneg_left bl hsc'.le
    nlinarith
  have a2 : sc * evT t r * (D : ℝ) ^ 2 ≤ ((n : ℝ) + 1) * (D : ℝ) ^ 2 := by
    have := mul_le_mul_of_nonneg_left bu hsc'.le
    nlinarith
  have b1 := le_of_mul_le_mul_right a1 hD'
  have b2 := le_of_mul_le_mul_right a2 hD'
  rw [abs_le]
  constructor <;> linarith

/-! ## Points and the tests -/

/-- Exact points `(X, Y)`. -/
abbrev Q := (ℤ × ℤ × ℤ) × (ℤ × ℤ × ℤ)

/-- The plane point `(X(t)/2, s·Y(t))`. -/
noncomputable def embT (t s : ℝ) (q : Q) : Point := ![evT t q.1 / 2, s * evT t q.2]

/-- The certificate of one checker point: both approximations within `1`, both at most `Mx`. -/
def certOK (lo D sc s0 s1 : ℤ) (Mx : ℕ) (p : Q × NP) : Bool :=
  apxOK lo D sc p.1.1 ((p.2.1 : ℤ) - s0) && apxOK lo D sc p.1.2 ((p.2.2 : ℤ) - s1) &&
    Nat.ble p.2.1 Mx && Nat.ble p.2.2 Mx

/-- Approximate orientation larger than `E`. -/
def opA (E : ℕ) (a b c : Q × NP) : Bool :=
  Nat.blt (a.2.2 * b.2.1 + b.2.2 * c.2.1 + c.2.2 * a.2.1 + E)
    (a.2.1 * b.2.2 + b.2.1 * c.2.2 + c.2.1 * a.2.2)

/-- The order by `v + c·u`, with margin `m`. -/
def abA (c m : ℕ) (p q : Q × NP) : Bool :=
  Nat.blt (p.2.2 + c * p.2.1 + m) (q.2.2 + c * q.2.1)

theorem opA_cyc (E : ℕ) (a b c : Q × NP) : opA E b c a = opA E a b c := by
  unfold opA
  congr 1 <;> ring

theorem prod_err {x x' y y' M : ℝ} (hx : |x'| ≤ M) (hy : |y'| ≤ M) (ex : |x' - x| ≤ 2)
    (ey : |y' - y| ≤ 2) : |x' * y' - x * y| ≤ 4 * M + 4 := by
  have e : x' * y' - x * y = x' * (y' - y) + y * (x' - x) := by ring
  have hy2 : |y| ≤ M + 2 := by
    have := abs_sub_abs_le_abs_sub y' y
    have := abs_sub_comm y' y
    linarith [abs_sub_abs_le_abs_sub y y']
  rw [e]
  calc |x' * (y' - y) + y * (x' - x)| ≤ |x' * (y' - y)| + |y * (x' - x)| := abs_add_le _ _
    _ = |x'| * |y' - y| + |y| * |x' - x| := by rw [abs_mul, abs_mul]
    _ ≤ M * 2 + (M + 2) * 2 := by
        gcongr
        · exact le_trans (abs_nonneg _) hx
        · linarith [abs_nonneg x', hx]
    _ = 4 * M + 4 := by ring

section
variable {t s : ℝ} {lo D sc s0 s1 : ℤ} {Mx : ℕ}

/-- What a certificate gives, in real numbers. -/
theorem certOK_sound (hD : 0 < D) (hlo : 0 < lo) (hsc : 0 < sc)
    (h1 : (lo : ℝ) / D < t) (h2 : t < ((lo + 1 : ℤ) : ℝ) / D) {p : Q × NP}
    (h : certOK lo D sc s0 s1 Mx p = true) :
    |((p.2.1 : ℝ) - s0) - sc * evT t p.1.1| ≤ 1 ∧ |((p.2.2 : ℝ) - s1) - sc * evT t p.1.2| ≤ 1 ∧
      (p.2.1 : ℝ) ≤ Mx ∧ (p.2.2 : ℝ) ≤ Mx := by
  unfold certOK at h
  simp only [Bool.and_eq_true, Nat.ble_eq] at h
  obtain ⟨⟨⟨ha, hb⟩, hc⟩, hd⟩ := h
  have e1 := apxOK_sound hD hlo hsc h1 h2 ha
  have e2 := apxOK_sound hD hlo hsc h1 h2 hb
  push_cast at e1 e2
  exact ⟨e1, e2, by exact_mod_cast hc, by exact_mod_cast hd⟩

theorem opA_sound (hD : 0 < D) (hlo : 0 < lo) (hsc : 0 < sc) (hs : 0 < s)
    (h1 : (lo : ℝ) / D < t) (h2 : t < ((lo + 1 : ℤ) : ℝ) / D) {a b c : Q × NP}
    (ha : certOK lo D sc s0 s1 Mx a = true) (hb : certOK lo D sc s0 s1 Mx b = true)
    (hc : certOK lo D sc s0 s1 Mx c = true) (h : opA (8 * Mx + 8) a b c = true) :
    0 < orient (embT t s a.1) (embT t s b.1) (embT t s c.1) := by
  obtain ⟨au, av, au', av'⟩ := certOK_sound hD hlo hsc h1 h2 ha
  obtain ⟨bu, bv, bu', bv'⟩ := certOK_sound hD hlo hsc h1 h2 hb
  obtain ⟨cu, cv, cu', cv'⟩ := certOK_sound hD hlo hsc h1 h2 hc
  unfold opA at h
  rw [Nat.blt_eq] at h
  have hO : (8 * (Mx : ℝ) + 8) <
      ((b.2.1 : ℝ) - a.2.1) * ((c.2.2 : ℝ) - a.2.2) - ((b.2.2 : ℝ) - a.2.2) * ((c.2.1 : ℝ) - a.2.1) := by
    have : ((a.2.2 * b.2.1 + b.2.2 * c.2.1 + c.2.2 * a.2.1 + (8 * Mx + 8) : ℕ) : ℝ) <
        ((a.2.1 * b.2.2 + b.2.1 * c.2.2 + c.2.1 * a.2.2 : ℕ) : ℝ) := by exact_mod_cast h
    push_cast at this
    linarith
  set ua := evT t a.1.1; set va := evT t a.1.2
  set ub := evT t b.1.1; set vb := evT t b.1.2
  set uc := evT t c.1.1; set vc := evT t c.1.2
  have hsc' : (0 : ℝ) < sc := by exact_mod_cast hsc
  have hn : ∀ x y : ℕ, (x : ℝ) ≤ Mx → (y : ℝ) ≤ Mx → |(x : ℝ) - y| ≤ Mx := by
    intro x y hx hy
    rw [abs_le]; constructor <;> linarith [(Nat.cast_nonneg x : (0 : ℝ) ≤ x),
      (Nat.cast_nonneg y : (0 : ℝ) ≤ y)]
  have hd : ∀ (x y : ℕ) (σ : ℤ) (w z : ℝ), |((x : ℝ) - σ) - sc * w| ≤ 1 →
      |((y : ℝ) - σ) - sc * z| ≤ 1 → |((x : ℝ) - y) - sc * (w - z)| ≤ 2 := by
    intro x y σ w z hx hy
    have : ((x : ℝ) - y) - sc * (w - z) = (((x : ℝ) - σ) - sc * w) - (((y : ℝ) - σ) - sc * z) := by
      ring
    rw [this]
    exact le_trans (abs_sub _ _) (by linarith)
  have p1 := prod_err (hn _ _ bu' au') (hn _ _ cv' av') (hd _ _ _ _ _ bu au) (hd _ _ _ _ _ cv av)
  have p2 := prod_err (hn _ _ bv' av') (hn _ _ cu' au') (hd _ _ _ _ _ bv av) (hd _ _ _ _ _ cu au)
  have hpos : 0 < (sc : ℝ) * (ub - ua) * (sc * (vc - va)) - sc * (vb - va) * (sc * (uc - ua)) := by
    rw [abs_le] at p1 p2
    linarith [p1.1, p1.2, p2.1, p2.2]
  have hO' : 0 < (ub - ua) * (vc - va) - (vb - va) * (uc - ua) := by
    have e : (sc : ℝ) * (ub - ua) * (sc * (vc - va)) - sc * (vb - va) * (sc * (uc - ua)) =
        (sc : ℝ) ^ 2 * ((ub - ua) * (vc - va) - (vb - va) * (uc - ua)) := by ring
    rw [e] at hpos
    exact pos_of_mul_pos_right hpos (by positivity)
  have e : orient (embT t s a.1) (embT t s b.1) (embT t s c.1) =
      s / 2 * ((ub - ua) * (vc - va) - (vb - va) * (uc - ua)) := by
    simp only [orient, embT, Matrix.cons_val_zero, Matrix.cons_val_one]
    ring
  rw [e]
  exact mul_pos (by linarith) hO'

theorem abA_sound (hD : 0 < D) (hlo : 0 < lo) (hsc : 0 < sc)
    (h1 : (lo : ℝ) / D < t) (h2 : t < ((lo + 1 : ℤ) : ℝ) / D) (c : ℕ) {p q : Q × NP}
    (hp : certOK lo D sc s0 s1 Mx p = true) (hq : certOK lo D sc s0 s1 Mx q = true)
    (h : abA c (2 + 2 * c) p q = true) :
    evT t p.1.2 + c * evT t p.1.1 < evT t q.1.2 + c * evT t q.1.1 := by
  obtain ⟨pu, pv, -, -⟩ := certOK_sound hD hlo hsc h1 h2 hp
  obtain ⟨qu, qv, -, -⟩ := certOK_sound hD hlo hsc h1 h2 hq
  unfold abA at h
  rw [Nat.blt_eq] at h
  have h' : ((p.2.2 + c * p.2.1 + (2 + 2 * c) : ℕ) : ℝ) < ((q.2.2 + c * q.2.1 : ℕ) : ℝ) := by
    exact_mod_cast h
  push_cast at h'
  have hsc' : (0 : ℝ) < sc := by exact_mod_cast hsc
  have hc0 : (0 : ℝ) ≤ c := Nat.cast_nonneg c
  rw [abs_le] at pu pv qu qv
  have key : (sc : ℝ) * ((evT t p.1.2 + c * evT t p.1.1)) < sc * (evT t q.1.2 + c * evT t q.1.1) := by
    nlinarith [pu.1, pu.2, pv.1, pv.2, qu.1, qu.2, qv.1, qv.2]
  exact lt_of_mul_lt_mul_left key hsc'.le

end

end LeanLB.G
