import ErdosSzekeres.Suk.SpikeSeparation

namespace ErdosSzekeres.Suk

def CapFrame.Horizontal (F : CapFrame) : Prop :=
  F.a 0 < F.b 0 ∧ F.b 0 < F.c 0 ∧ F.c 0 < F.d 0

/-- For a horizontal cap, its support spike is strictly between the two
middle anchors in x-coordinate. -/
theorem CapFrame.spike_x_bounds (F : CapFrame) (hx : F.Horizontal)
    {p : Point} (hp : p ∈ F.spike) : F.b 0 < p 0 ∧ p 0 < F.c 0 := by
  constructor
  · have he : (F.c 0 - F.b 0) * orient F.a F.b p -
        (F.b 0 - F.a 0) * orient F.b F.c p =
        orient F.a F.b F.c * (p 0 - F.b 0) := by
      simp only [orient]
      ring
    have h₀ := mul_neg_of_pos_of_neg (sub_pos.mpr hx.2.1) hp.1
    have h₁ := mul_pos (sub_pos.mpr hx.1) hp.2.1
    by_contra! hn
    have h₂ := mul_nonneg_of_nonpos_of_nonpos F.abc.le (sub_nonpos.mpr hn)
    linarith only [he, h₀, h₁, h₂]
  · have he : (F.d 0 - F.c 0) * orient F.b F.c p -
        (F.c 0 - F.b 0) * orient F.c F.d p =
        orient F.b F.c F.d * (p 0 - F.c 0) := by
      simp only [orient]
      ring
    have h₀ := mul_pos (sub_pos.mpr hx.2.2) hp.2.1
    have h₁ := mul_neg_of_pos_of_neg (sub_pos.mpr hx.2.1) hp.2.2
    by_contra! hn
    have h₂ := mul_nonpos_of_nonpos_of_nonneg F.bcd.le (sub_nonneg.mpr hn)
    linarith only [he, h₀, h₁, h₂]

/-- If a pair-line leaves both base endpoints on one side, its orientation
against the left anchor has the opposite sign to its horizontal direction. -/
theorem CapFrame.anchor_pair_sign (F : CapFrame) (hx : F.Horizontal)
    {p q : Point} (hp : p ∈ F.spike)
    (hbase : 0 < orient p q F.a * orient p q F.d) :
    0 < (q 0 - p 0) * (-orient p q F.a) := by
  have hpx := F.spike_x_bounds hx hp
  have hpa : F.a 0 < p 0 := hx.1.trans hpx.1
  have hpd : p 0 < F.d 0 := hpx.2.trans hx.2.2
  have hD := (F.spike_orientations hp).2.1
  have he : orient F.a F.d p * ((q 0 - p 0) * (-orient p q F.a)) =
      (F.d 0 - p 0) * (orient p q F.a) ^ 2 +
        (p 0 - F.a 0) * (orient p q F.a * orient p q F.d) := by
    simp only [orient]
    ring
  have h₀ := mul_nonneg (sub_pos.mpr hpd).le (sq_nonneg (orient p q F.a))
  have h₁ := mul_pos (sub_pos.mpr hpa) hbase
  by_contra! hn
  have h₂ := mul_nonpos_of_nonneg_of_nonpos hD.le hn
  linarith only [he, h₀, h₁, h₂]

theorem CapFrame.incomparable_distinct_x (F : CapFrame) (hx : F.Horizontal)
    (p q : F.spike) (hpq : ¬ F.toOuter p ≤ F.toOuter q)
    (hqp : ¬ F.toOuter q ≤ F.toOuter p) : p.val 0 ≠ q.val 0 := by
  have h := F.anchor_pair_sign (p := p.val) (q := q.val) hx p.property
    ((F.toOuter p).incomparable_same_side (F.toOuter q) hpq hqp)
  intro he
  simp [he] at h

theorem CapFrame.incomparable_anchor_negative (F : CapFrame) (hx : F.Horizontal)
    (p q : F.spike) (hpq : ¬ F.toOuter p ≤ F.toOuter q)
    (hqp : ¬ F.toOuter q ≤ F.toOuter p) (hxq : p.val 0 < q.val 0) :
    orient p.val q.val F.a < 0 := by
  have h := F.anchor_pair_sign (p := p.val) (q := q.val) hx p.property
    ((F.toOuter p).incomparable_same_side (F.toOuter q) hpq hqp)
  exact neg_pos.mp (pos_of_mul_pos_right h (sub_pos.mpr hxq).le)

theorem ClockwiseAnchors.frame_horizontal {r : ℕ} (A : ClockwiseAnchors (r + 3))
    (hx : StrictMono (fun i => A.point i 0)) (i : Fin r) : (A.frame i).Horizontal := by
  refine ⟨hx ?_, hx ?_, hx ?_⟩ <;> change _ < _
  all_goals simp only [Fin.lt_def]; omega

end ErdosSzekeres.Suk
