import ErdosSzekeres.Definitions
import ErdosSzekeres.Orientation
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Algebra.Order.ToIntervalMod
import Mathlib.Analysis.SpecialFunctions.Complex.Arg

/-!
# Phase patterns of three directions and the two angular rules

Three directions `α < β < δ < α + 2π` (counter-clockwise order, normalized to one turn starting at
`α`) and their antipodes `α + π, β + π, δ + π` give six points on the circle.  The ccw gaps are
`g₁ = β - α`, `g₂ = δ - β`, `g₃ = α + 2π - δ`.

* `inArc s g θ`: the direction `θ` lies, modulo `2π`, in the open ccw arc `(s, s + g)`.
* `Alternating α β δ`: each of the three open arcs between ccw-consecutive points contains an
  antipode (pattern `PAPAPA`).
* `RunAt …`: two consecutive arcs contain no antipode (a cyclic run `PPP`).

Main results:
* `alternating_iff_gaps_lt_pi`: alternation ⇔ all three gaps `< π` (no genericity needed);
  `alternating_exactly_one`: then each arc holds exactly one antipode (the opposite one).
* `runMidB_iff`: a `PPP` run with middle point `β` ⇔ `g₁ + g₂ < π` (open half-plane), given
  `g₃ ≠ π`.
* `gap_classification`, `phase_trichotomy`: under genericity (no gap equal to `π`), the pattern is
  alternating or has a `PPP` run with middle `α`, `β` or `δ`; alternation excludes every run.
* `centre_inside_of_alternating`, `halfplane_of_runMidB`: the geometric meaning of the patterns.
* `orient_pos_of_alternating` (rule A), `orient_pos_of_runMid{A,B,D}` (rule B) and
  `orient_pos_of_phase`: in ccw order, with the rule-B radius condition for the run's middle
  point, `orient a b d > 0`.
* `exists_polar`, `polar_toIcoMod`, `orient_sign_of_phase`: arbitrary points `≠ c` and arbitrary
  real directions, reduced into `[α, α + 2π)`; the sign is `+` for ccw order `a, b, d` and `-` for
  ccw order `a, d, b`.
* `word_dichotomy`: the discrete case split on cyclic words of length 6 (by `decide`).
-/

namespace PhaseClassification

open ErdosSzekeres Real

/-- The point at distance `r` from `c` in direction `θ` (copied from `LayerLemma.lean`). -/
noncomputable def polar (c : Point) (r θ : ℝ) : Point := ![c 0 + r * Real.cos θ, c 1 + r * Real.sin θ]

/-- Polar orientation formula (copied from `LayerLemma.lean`). -/
theorem orient_polar (c : Point) (ra rb rd α β δ : ℝ) :
    orient (polar c ra α) (polar c rb β) (polar c rd δ) =
      ra * rb * Real.sin (β - α) + rb * rd * Real.sin (δ - β) + rd * ra * Real.sin (α - δ) := by
  simp only [orient, polar, Matrix.cons_val_zero, Matrix.cons_val_one, Real.sin_sub]
  ring

/-- Angular rule A (copied from `LayerLemma.lean`). -/
theorem orient_polar_centre_inside {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hb : 0 < rb)
    (hd : 0 < rd) (h1 : 0 < β - α) (h1' : β - α < Real.pi) (h2 : 0 < δ - β) (h2' : δ - β < Real.pi)
    (h3 : 0 < α - δ + 2 * Real.pi) (h3' : α - δ + 2 * Real.pi < Real.pi) :
    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by
  rw [orient_polar]
  have s1 := Real.sin_pos_of_pos_of_lt_pi h1 h1'
  have s2 := Real.sin_pos_of_pos_of_lt_pi h2 h2'
  have s3 : 0 < Real.sin (α - δ) := by
    have := Real.sin_pos_of_pos_of_lt_pi h3 h3'
    rwa [Real.sin_add_two_pi] at this
  positivity

/-- `sin x + sin y > sin (x + y)` for `x, y ∈ (0, π)` (copied from `LayerLemma.lean`). -/
theorem sin_add_lt {x y : ℝ} (hx : 0 < x) (hx' : x < Real.pi) (hy : 0 < y) (hy' : y < Real.pi) :
    Real.sin (x + y) < Real.sin x + Real.sin y := by
  rw [Real.sin_add]
  have sx := Real.sin_pos_of_pos_of_lt_pi hx hx'
  have sy := Real.sin_pos_of_pos_of_lt_pi hy hy'
  have cx : Real.cos x < 1 := by
    refine lt_of_le_of_ne (Real.cos_le_one x) fun h => ?_
    have := (Real.cos_eq_one_iff_of_lt_of_lt (by linarith) (by linarith)).1 h
    linarith
  have cy : Real.cos y < 1 := by
    refine lt_of_le_of_ne (Real.cos_le_one y) fun h => ?_
    have := (Real.cos_eq_one_iff_of_lt_of_lt (by linarith) (by linarith)).1 h
    linarith
  nlinarith [mul_pos sx (sub_pos.2 cy), mul_pos sy (sub_pos.2 cx)]

/-- Angular rule B (copied from `LayerLemma.lean`). -/
theorem orient_polar_halfplane {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hd : 0 < rd)
    (hba : ra ≤ rb) (hbd : rd ≤ rb) (h1 : 0 < β - α) (h2 : 0 < δ - β) (h12 : δ - α < Real.pi) :
    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by
  rw [orient_polar]
  set x := β - α
  set y := δ - β
  have hxy : α - δ = -(x + y) := by simp only [x, y]; ring
  rw [hxy, Real.sin_neg]
  have hx' : x < Real.pi := by simp only [x, y] at h12 h2 ⊢; linarith
  have hy' : y < Real.pi := by simp only [x, y] at h12 h1 ⊢; linarith
  have sx := Real.sin_pos_of_pos_of_lt_pi h1 hx'
  have sy := Real.sin_pos_of_pos_of_lt_pi h2 hy'
  have key := sin_add_lt h1 hx' h2 hy'
  have e1 : ra * rd * Real.sin x ≤ ra * rb * Real.sin x := by
    have := mul_le_mul_of_nonneg_left hbd (mul_nonneg ha.le sx.le)
    nlinarith
  have e2 : ra * rd * Real.sin y ≤ rb * rd * Real.sin y := by
    have := mul_le_mul_of_nonneg_left hba (mul_nonneg hd.le sy.le)
    nlinarith
  have e3 : 0 < ra * rd * (Real.sin x + Real.sin y - Real.sin (x + y)) := by
    have := sub_pos.2 key
    positivity
  nlinarith

/-! ## Periodicity -/

theorem polar_add_int_two_pi (c : Point) (r θ : ℝ) (k : ℤ) :
    polar c r (θ + k * (2 * π)) = polar c r θ := by
  simp only [polar]
  rw [Real.cos_add_int_mul_two_pi, Real.sin_add_int_mul_two_pi]

theorem polar_add_two_pi (c : Point) (r θ : ℝ) : polar c r (θ + 2 * π) = polar c r θ := by
  simpa using polar_add_int_two_pi c r θ 1

/-! ## Arcs and phase patterns -/

/-- `θ` lies, modulo `2π`, in the open ccw arc `(s, s + g)`. -/
def inArc (s g θ : ℝ) : Prop := ∃ k : ℤ, s < θ + 2 * π * k ∧ θ + 2 * π * k < s + g

/-- Some antipode `α + π`, `β + π`, `δ + π` lies in the open arc `(s, s + g)`. -/
def arcHasAntipode (α β δ s g : ℝ) : Prop :=
  inArc s g (α + π) ∨ inArc s g (β + π) ∨ inArc s g (δ + π)

/-- **Pattern `PAPAPA`.**  Each of the three open arcs between ccw-consecutive points
`α → β → δ → α + 2π` contains an antipode.  Each then contains exactly one, namely the
antipode of the opposite point (`alternating_exactly_one`). -/
def Alternating (α β δ : ℝ) : Prop :=
  arcHasAntipode α β δ α (β - α) ∧ arcHasAntipode α β δ β (δ - β) ∧
    arcHasAntipode α β δ δ (α + 2 * π - δ)

/-- **A cyclic run `PPP` with middle point `β`**: the arcs `(α, β)` and `(β, δ)` contain no
antipode. -/
def RunMidB (α β δ : ℝ) : Prop :=
  ¬ arcHasAntipode α β δ α (β - α) ∧ ¬ arcHasAntipode α β δ β (δ - β)

/-- Run `PPP` with middle point `δ`: arcs `(β, δ)` and `(δ, α + 2π)` empty. -/
def RunMidD (α β δ : ℝ) : Prop :=
  ¬ arcHasAntipode α β δ β (δ - β) ∧ ¬ arcHasAntipode α β δ δ (α + 2 * π - δ)

/-- Run `PPP` with middle point `α`: arcs `(δ, α + 2π)` and `(α, β)` empty. -/
def RunMidA (α β δ : ℝ) : Prop :=
  ¬ arcHasAntipode α β δ δ (α + 2 * π - δ) ∧ ¬ arcHasAntipode α β δ α (β - α)

theorem inArc_of (s g θ : ℝ) (k : ℤ) (h1 : s < θ + 2 * π * k) (h2 : θ + 2 * π * k < s + g) :
    inArc s g θ := ⟨k, h1, h2⟩

/-- If some lift of `θ` lies in `[s + g, s + 2π]`, then `θ` is not in the open arc `(s, s + g)`. -/
theorem not_inArc {s g θ : ℝ} (m : ℤ) (h1 : s + g ≤ θ + 2 * π * m) (h2 : θ + 2 * π * m ≤ s + 2 * π) :
    ¬ inArc s g θ := by
  rintro ⟨k, hk1, hk2⟩
  have hpi := Real.pi_pos
  rcases le_or_gt 0 (k - m) with h | h
  · have h' : (0 : ℝ) ≤ (k : ℝ) - m := by exact_mod_cast h
    nlinarith [mul_nonneg hpi.le h']
  · have h'' : k - m ≤ -1 := by omega
    have h' : (k : ℝ) - m ≤ -1 := by exact_mod_cast h''
    nlinarith [mul_le_mul_of_nonneg_left h' hpi.le]

/-! ## (b) Alternation ⇔ all gaps `< π` -/

/-- Arc `(α, β)` is empty when `g₁ + g₂ ≤ π`. -/
theorem arc1_empty {α β δ : ℝ} (hab : α < β) (hbd : β < δ) (h : δ - α ≤ π) :
    ¬ arcHasAntipode α β δ α (β - α) := by
  rintro (h' | h' | h')
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'

/-- Arc `(β, δ)` is empty when `g₁ + g₂ ≤ π`. -/
theorem arc2_empty {α β δ : ℝ} (hab : α < β) (hbd : β < δ) (h : δ - α ≤ π) :
    ¬ arcHasAntipode α β δ β (δ - β) := by
  rintro (h' | h' | h')
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'

/-- Arc `(β, δ)` is empty when `g₂ + g₃ ≤ π`. -/
theorem arc2_empty' {α β δ : ℝ} (hbd : β < δ) (hda : δ < α + 2 * π) (h : α + 2 * π - β ≤ π) :
    ¬ arcHasAntipode α β δ β (δ - β) := by
  rintro (h' | h' | h')
  · exact not_inArc 1 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'

/-- Arc `(δ, α + 2π)` is empty when `g₂ + g₃ ≤ π`. -/
theorem arc3_empty {α β δ : ℝ} (hbd : β < δ) (hda : δ < α + 2 * π) (h : α + 2 * π - β ≤ π) :
    ¬ arcHasAntipode α β δ δ (α + 2 * π - δ) := by
  rintro (h' | h' | h')
  · exact not_inArc 1 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'

/-- Arc `(δ, α + 2π)` is empty when `g₃ + g₁ ≤ π`. -/
theorem arc3_empty' {α β δ : ℝ} (hab : α < β) (hda : δ < α + 2 * π) (h : β + 2 * π - δ ≤ π) :
    ¬ arcHasAntipode α β δ δ (α + 2 * π - δ) := by
  rintro (h' | h' | h')
  · exact not_inArc 1 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 1 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'

/-- Arc `(α, β)` is empty when `g₃ + g₁ ≤ π`. -/
theorem arc1_empty' {α β δ : ℝ} (hab : α < β) (hda : δ < α + 2 * π) (h : β + 2 * π - δ ≤ π) :
    ¬ arcHasAntipode α β δ α (β - α) := by
  rintro (h' | h' | h')
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc 0 (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'
  · exact not_inArc (-1) (by push_cast; linarith) (by push_cast; linarith [Real.pi_pos]) h'

/-- **(b)** For directions in ccw order `α < β < δ < α + 2π`, the six points alternate
(`PAPAPA`) iff all three ccw gaps are `< π`. -/
theorem alternating_iff_gaps_lt_pi {α β δ : ℝ} (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π) :
    Alternating α β δ ↔ (β - α < π ∧ δ - β < π ∧ α + 2 * π - δ < π) := by
  constructor
  · rintro ⟨h1, h2, h3⟩
    refine ⟨?_, ?_, ?_⟩
    · by_contra hc
      exact arc2_empty' hbd hda (by linarith) h2
    · by_contra hc
      exact arc3_empty' hab hda (by linarith) h3
    · by_contra hc
      exact arc1_empty hab hbd (by linarith) h1
  · rintro ⟨g1, g2, g3⟩
    refine ⟨Or.inr (Or.inr (inArc_of _ _ _ (-1) (by push_cast; linarith) (by push_cast; linarith))),
      Or.inl (inArc_of _ _ _ 0 (by push_cast; linarith) (by push_cast; linarith)),
      Or.inr (Or.inl (inArc_of _ _ _ 0 (by push_cast; linarith) (by push_cast; linarith)))⟩

/-! ## Runs `PPP` ⇔ open half-plane -/

/-- If `g₁ + g₂ > π`, one of the arcs `(α, β)`, `(β, δ)` contains an antipode. -/
theorem arc12_nonempty {α β δ : ℝ} (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π)
    (h : π < δ - α) : arcHasAntipode α β δ α (β - α) ∨ arcHasAntipode α β δ β (δ - β) := by
  rcases lt_or_ge π (δ - β) with h2 | h2
  · -- `β + π ∈ (β, δ)`
    exact Or.inr (Or.inr (Or.inl (inArc_of _ _ _ 0 (by push_cast; linarith [Real.pi_pos])
      (by push_cast; linarith))))
  · rcases lt_or_ge (β - α) π with h1 | h1
    · rcases eq_or_lt_of_le h2 with h2 | h2
      · -- `δ - β = π`, so `α + π ∈ (β, δ)`
        exact Or.inr (Or.inl (inArc_of _ _ _ 0 (by push_cast; linarith) (by push_cast; linarith)))
      · -- `δ - π ∈ (α, β)`
        exact Or.inl (Or.inr (Or.inr (inArc_of _ _ _ (-1) (by push_cast; linarith)
          (by push_cast; linarith))))
    · rcases eq_or_lt_of_le h1 with h1 | h1
      · -- `β - α = π`, so `δ - π ∈ (α, β)` (as `δ - β < π`)
        exact Or.inl (Or.inr (Or.inr (inArc_of _ _ _ (-1) (by push_cast; linarith)
          (by push_cast; linarith))))
      · -- `α + π ∈ (α, β)`
        exact Or.inl (Or.inl (inArc_of _ _ _ 0 (by push_cast; linarith [Real.pi_pos])
          (by push_cast; linarith)))

/-- **Run `PPP` with middle `β` ⇔ open half-plane** `g₁ + g₂ < π` (given `g₃ ≠ π`). -/
theorem runMidB_iff {α β δ : ℝ} (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π)
    (hg3 : α + 2 * π - δ ≠ π) : RunMidB α β δ ↔ δ - α < π := by
  constructor
  · rintro ⟨h1, h2⟩
    by_contra hc
    have hc' : π < δ - α := lt_of_le_of_ne (not_lt.1 hc) (fun h => hg3 (by linarith))
    rcases arc12_nonempty hab hbd hda hc' with h | h
    · exact h1 h
    · exact h2 h
  · intro h
    exact ⟨arc1_empty hab hbd h.le, arc2_empty hab hbd h.le⟩

/-! ## (a) The classification -/

/-- **(a) Trichotomy of gaps.**  For directions in ccw order, with no gap equal to `π` (the six
points are distinct), either all gaps are `< π` (rule A), or two consecutive gaps sum to `< π`
(open half-plane; rule B), for exactly one of the three cyclic labellings. -/
theorem gap_classification {α β δ : ℝ} (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π)
    (hg1 : β - α ≠ π) (hg2 : δ - β ≠ π) (hg3 : α + 2 * π - δ ≠ π) :
    (β - α < π ∧ δ - β < π ∧ α + 2 * π - δ < π) ∨ δ - α < π ∨ α + 2 * π - β < π ∨
      β + 2 * π - δ < π := by
  rcases lt_or_gt_of_ne hg1 with h1 | h1 <;> rcases lt_or_gt_of_ne hg2 with h2 | h2 <;>
    rcases lt_or_gt_of_ne hg3 with h3 | h3
  · exact Or.inl ⟨h1, h2, h3⟩
  · exact Or.inr (Or.inl (by linarith))
  · exact Or.inr (Or.inr (Or.inr (by linarith)))
  · linarith
  · exact Or.inr (Or.inr (Or.inl (by linarith)))
  · linarith
  · linarith
  · linarith

/-- **Phase trichotomy.**  Under genericity, the pattern is alternating or has a `PPP` run with
middle point `α`, `β` or `δ`; and alternation excludes every run. -/
theorem phase_trichotomy {α β δ : ℝ} (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π)
    (hg1 : β - α ≠ π) (hg2 : δ - β ≠ π) (hg3 : α + 2 * π - δ ≠ π) :
    (Alternating α β δ ∨ RunMidA α β δ ∨ RunMidB α β δ ∨ RunMidD α β δ) ∧
      (Alternating α β δ → ¬ RunMidA α β δ ∧ ¬ RunMidB α β δ ∧ ¬ RunMidD α β δ) := by
  refine ⟨?_, ?_⟩
  · rcases gap_classification hab hbd hda hg1 hg2 hg3 with h | h | h | h
    · exact Or.inl ((alternating_iff_gaps_lt_pi hab hbd hda).2 h)
    · exact Or.inr (Or.inr (Or.inl ⟨arc1_empty hab hbd h.le, arc2_empty hab hbd h.le⟩))
    · exact Or.inr (Or.inr (Or.inr ⟨arc2_empty' hbd hda h.le, arc3_empty hbd hda h.le⟩))
    · exact Or.inr (Or.inl ⟨arc3_empty' hab hda h.le, arc1_empty' hab hda h.le⟩)
  · rintro ⟨h1, h2, h3⟩
    exact ⟨fun h => h.1 h3, fun h => h.1 h1, fun h => h.1 h2⟩

/-! ## Connection to the angular rules -/

/-- **Rule A from the pattern.**  Alternation gives a positive ccw triple. -/
theorem orient_pos_of_alternating {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hb : 0 < rb)
    (hd : 0 < rd) (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π)
    (halt : Alternating α β δ) :
    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by
  obtain ⟨g1, g2, g3⟩ := (alternating_iff_gaps_lt_pi hab hbd hda).1 halt
  exact orient_polar_centre_inside ha hb hd (by linarith) g1 (by linarith) g2 (by linarith)
    (by linarith)

/-- **Rule B from a run with middle `β`.** -/
theorem orient_pos_of_runMidB {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hd : 0 < rd)
    (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π) (hg3 : α + 2 * π - δ ≠ π)
    (hrun : RunMidB α β δ) (hba : ra ≤ rb) (hbd' : rd ≤ rb) :
    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by
  have h := (runMidB_iff hab hbd hda hg3).1 hrun
  exact orient_polar_halfplane ha hd hba hbd' (by linarith) (by linarith) h

/-- **Rule B from a run with middle `δ`** (the triple `β, δ, α + 2π`, then cyclic invariance). -/
theorem orient_pos_of_runMidD {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hb : 0 < rb)
    (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π) (hg1 : β - α ≠ π)
    (hrun : RunMidD α β δ) (hdb : rb ≤ rd) (hda' : ra ≤ rd) :
    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by
  -- relabel: `β < δ < α + 2π < β + 2π`, which is again in ccw order
  have hrun' : RunMidB β δ (α + 2 * π) := by
    obtain ⟨h1, h2⟩ := hrun
    refine ⟨?_, ?_⟩
    · rintro (h | h | h)
      · exact h1 (Or.inr (Or.inl h))
      · exact h1 (Or.inr (Or.inr h))
      · obtain ⟨k, hk1, hk2⟩ := h
        exact h1 (Or.inl ⟨k + 1, by push_cast; linarith, by push_cast; linarith⟩)
    · rintro (h | h | h)
      · exact h2 (Or.inr (Or.inl (by simpa using h)))
      · exact h2 (Or.inr (Or.inr (by simpa using h)))
      · obtain ⟨k, hk1, hk2⟩ := h
        exact h2 (Or.inl ⟨k + 1, by push_cast; linarith, by push_cast; linarith⟩)
  have hpos := orient_pos_of_runMidB (c := c) hb ha hbd hda (by linarith)
    (by intro h; exact hg1 (by linarith)) hrun' hdb hda'
  rw [polar_add_two_pi] at hpos
  rwa [orient_cycle] at hpos

/-- **Rule B from a run with middle `α`** (the triple `δ, α + 2π, β + 2π`). -/
theorem orient_pos_of_runMidA {c : Point} {ra rb rd α β δ : ℝ} (hb : 0 < rb) (hd : 0 < rd)
    (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π) (hg2 : δ - β ≠ π)
    (hrun : RunMidA α β δ) (hba : rb ≤ ra) (hda' : rd ≤ ra) :
    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by
  have hrun' : RunMidB δ (α + 2 * π) (β + 2 * π) := by
    obtain ⟨h1, h2⟩ := hrun
    refine ⟨?_, ?_⟩
    · rintro (h | h | h)
      · obtain ⟨k, hk1, hk2⟩ := h
        exact h1 (Or.inr (Or.inr ⟨k, by linarith, by linarith⟩))
      · obtain ⟨k, hk1, hk2⟩ := h
        exact h1 (Or.inl ⟨k + 1, by push_cast; linarith, by push_cast; linarith⟩)
      · obtain ⟨k, hk1, hk2⟩ := h
        exact h1 (Or.inr (Or.inl ⟨k + 1, by push_cast; linarith, by push_cast; linarith⟩))
    · rintro (h | h | h)
      · obtain ⟨k, hk1, hk2⟩ := h
        exact h2 (Or.inr (Or.inr ⟨k - 1, by push_cast; linarith, by push_cast; linarith⟩))
      · obtain ⟨k, hk1, hk2⟩ := h
        exact h2 (Or.inl ⟨k, by linarith, by linarith⟩)
      · obtain ⟨k, hk1, hk2⟩ := h
        exact h2 (Or.inr (Or.inl ⟨k, by linarith, by linarith⟩))
  have hpos := orient_pos_of_runMidB (c := c) hd hb hda (by linarith) (by linarith)
    (by intro h; exact hg2 (by linarith)) hrun' hda' hba
  rw [polar_add_two_pi, polar_add_two_pi] at hpos
  rwa [← orient_cycle] at hpos

/-- **Main theorem (sorted form).**  For three points `a, b, d` at positive radii in ccw direction
order `α < β < δ < α + 2π`, with the six phase points distinct (no gap equal to `π`), suppose
that whenever the pattern has a `PPP` run, its middle point has the largest radius (the radius
order of layers).  Then `orient a b d > 0`. -/
theorem orient_pos_of_phase {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hb : 0 < rb)
    (hd : 0 < rd) (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π)
    (hg1 : β - α ≠ π) (hg2 : δ - β ≠ π) (hg3 : α + 2 * π - δ ≠ π)
    (hA : RunMidA α β δ → rb ≤ ra ∧ rd ≤ ra) (hB : RunMidB α β δ → ra ≤ rb ∧ rd ≤ rb)
    (hD : RunMidD α β δ → rb ≤ rd ∧ ra ≤ rd) :
    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by
  rcases (phase_trichotomy hab hbd hda hg1 hg2 hg3).1 with h | h | h | h
  · exact orient_pos_of_alternating ha hb hd hab hbd hda h
  · exact orient_pos_of_runMidA hb hd hab hbd hda hg2 h (hA h).1 (hA h).2
  · exact orient_pos_of_runMidB ha hd hab hbd hda hg3 h (hB h).1 (hB h).2
  · exact orient_pos_of_runMidD ha hb hab hbd hda hg1 h (hD h).1 (hD h).2

/-- In the alternating pattern, each arc contains exactly one antipode: the antipode of the
point opposite to it. -/
theorem alternating_exactly_one {α β δ : ℝ} (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π)
    (halt : Alternating α β δ) :
    (inArc α (β - α) (δ + π) ∧ ¬ inArc α (β - α) (α + π) ∧ ¬ inArc α (β - α) (β + π)) ∧
    (inArc β (δ - β) (α + π) ∧ ¬ inArc β (δ - β) (β + π) ∧ ¬ inArc β (δ - β) (δ + π)) ∧
    (inArc δ (α + 2 * π - δ) (β + π) ∧ ¬ inArc δ (α + 2 * π - δ) (α + π) ∧
      ¬ inArc δ (α + 2 * π - δ) (δ + π)) := by
  obtain ⟨g1, g2, g3⟩ := (alternating_iff_gaps_lt_pi hab hbd hda).1 halt
  have hpi := Real.pi_pos
  refine ⟨⟨inArc_of _ _ _ (-1) (by push_cast; linarith) (by push_cast; linarith),
      not_inArc 0 (by push_cast; linarith) (by push_cast; linarith),
      not_inArc 0 (by push_cast; linarith) (by push_cast; linarith)⟩,
    ⟨inArc_of _ _ _ 0 (by push_cast; linarith) (by push_cast; linarith),
      not_inArc 0 (by push_cast; linarith) (by push_cast; linarith),
      not_inArc 0 (by push_cast; linarith) (by push_cast; linarith)⟩,
    ⟨inArc_of _ _ _ 0 (by push_cast; linarith) (by push_cast; linarith),
      not_inArc 1 (by push_cast; linarith) (by push_cast; linarith),
      not_inArc 0 (by push_cast; linarith) (by push_cast; linarith)⟩⟩

/-! ## Geometric meaning of the two patterns -/

/-- Orientation of an edge against the centre. -/
theorem orient_polar_centre (c : Point) (ra rb α β : ℝ) :
    orient (polar c ra α) (polar c rb β) c = ra * rb * Real.sin (β - α) := by
  simp only [orient, polar, Matrix.cons_val_zero, Matrix.cons_val_one, Real.sin_sub]
  ring

/-- **Alternation ⇒ the centre is strictly inside the triangle**: `c` is strictly left of the
three ccw edges `a → b`, `b → d`, `d → a`. -/
theorem centre_inside_of_alternating {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hb : 0 < rb)
    (hd : 0 < rd) (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π)
    (halt : Alternating α β δ) :
    0 < orient (polar c ra α) (polar c rb β) c ∧ 0 < orient (polar c rb β) (polar c rd δ) c ∧
      0 < orient (polar c rd δ) (polar c ra α) c := by
  obtain ⟨g1, g2, g3⟩ := (alternating_iff_gaps_lt_pi hab hbd hda).1 halt
  simp only [orient_polar_centre]
  have s1 := Real.sin_pos_of_pos_of_lt_pi (sub_pos.2 hab) g1
  have s2 := Real.sin_pos_of_pos_of_lt_pi (sub_pos.2 hbd) g2
  have s3 : 0 < Real.sin (α - δ) := by
    have := Real.sin_pos_of_pos_of_lt_pi (x := α + 2 * π - δ) (by linarith) g3
    rwa [show α + 2 * π - δ = (α - δ) + 2 * π by ring, Real.sin_add_two_pi] at this
  exact ⟨by positivity, by positivity, by positivity⟩

/-- **A run `PPP` with middle `β` ⇒ the three points lie in an open half-plane through the
centre**: with `φ = (α + δ)/2`, the linear form `(p - c) · (cos φ, sin φ)` is positive at all
three points. -/
theorem halfplane_of_runMidB {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hb : 0 < rb)
    (hd : 0 < rd) (hab : α < β) (hbd : β < δ) (hda : δ < α + 2 * π) (hg3 : α + 2 * π - δ ≠ π)
    (hrun : RunMidB α β δ) :
    ∃ φ : ℝ, ∀ p ∈ ({polar c ra α, polar c rb β, polar c rd δ} : Set Point),
      0 < (p 0 - c 0) * Real.cos φ + (p 1 - c 1) * Real.sin φ := by
  have h := (runMidB_iff hab hbd hda hg3).1 hrun
  refine ⟨(α + δ) / 2, ?_⟩
  have key : ∀ r θ : ℝ, 0 < r → α ≤ θ → θ ≤ δ →
      0 < (polar c r θ 0 - c 0) * Real.cos ((α + δ) / 2) +
        (polar c r θ 1 - c 1) * Real.sin ((α + δ) / 2) := by
    intro r θ hr h1 h2
    have e : (polar c r θ 0 - c 0) * Real.cos ((α + δ) / 2) +
        (polar c r θ 1 - c 1) * Real.sin ((α + δ) / 2) = r * Real.cos (θ - (α + δ) / 2) := by
      simp only [polar, Matrix.cons_val_zero, Matrix.cons_val_one, Real.cos_sub]
      ring
    rw [e]
    have hc : 0 < Real.cos (θ - (α + δ) / 2) :=
      Real.cos_pos_of_mem_Ioo ⟨by linarith, by linarith⟩
    positivity
  intro p hp
  rcases hp with rfl | rfl | rfl
  · exact key ra α ha le_rfl (by linarith)
  · exact key rb β hb hab.le hbd.le
  · exact key rd δ hd (by linarith) le_rfl

/-! ## Every point other than the centre has a polar form -/

/-- Every point `p ≠ c` is `polar c r θ` with `r > 0` (take `r = |p - c|`, `θ = arg (p - c)`). -/
theorem exists_polar (c p : Point) (hp : p ≠ c) : ∃ r θ : ℝ, 0 < r ∧ p = polar c r θ := by
  set z : ℂ := ⟨p 0 - c 0, p 1 - c 1⟩
  have hz : z ≠ 0 := by
    intro h
    apply hp
    have h0 : p 0 - c 0 = 0 := congrArg Complex.re h
    have h1 : p 1 - c 1 = 0 := congrArg Complex.im h
    funext i
    fin_cases i
    · simpa using sub_eq_zero.1 h0
    · simpa using sub_eq_zero.1 h1
  refine ⟨‖z‖, Complex.arg z, norm_pos_iff.2 hz, ?_⟩
  have e0 := Complex.norm_mul_cos_arg z
  have e1 := Complex.norm_mul_sin_arg z
  funext i
  fin_cases i
  · simp only [polar, Fin.zero_eta, Matrix.cons_val_zero]
    rw [e0]
    simp [z]
  · simp only [polar, Fin.mk_one, Matrix.cons_val_one]
    rw [e1]
    simp [z]

/-! ## Arbitrary real directions -/

/-- Reducing a direction modulo `2π` into `[α, α + 2π)` does not move the point. -/
theorem polar_toIcoMod (c : Point) (r α θ : ℝ) :
    polar c r (toIcoMod Real.two_pi_pos α θ) = polar c r θ := by
  have h := toIcoMod_add_toIcoDiv_zsmul Real.two_pi_pos α θ
  conv_rhs => rw [← h]
  rw [zsmul_eq_mul, polar_add_int_two_pi]

/-- **Main theorem (general directions).**  For arbitrary real directions `α, β, δ`, let
`β' = β mod 2π` and `δ' = δ mod 2π`, reduced into `[α, α + 2π)`.  If `β' < δ'` (ccw order
`a, b, d`) the phase classification of `(α, β', δ')` with the rule-B radius condition gives
`orient a b d > 0`; if `δ' < β'` (ccw order `a, d, b`) the classification of `(α, δ', β')`
gives `orient a b d < 0`. -/
theorem orient_sign_of_phase {c : Point} {ra rb rd α β δ : ℝ} (ha : 0 < ra) (hb : 0 < rb)
    (hd : 0 < rd) (hβα : toIcoMod Real.two_pi_pos α β ≠ α)
    (hδα : toIcoMod Real.two_pi_pos α δ ≠ α) :
    (toIcoMod Real.two_pi_pos α β < toIcoMod Real.two_pi_pos α δ →
      toIcoMod Real.two_pi_pos α β - α ≠ π →
      toIcoMod Real.two_pi_pos α δ - toIcoMod Real.two_pi_pos α β ≠ π →
      α + 2 * π - toIcoMod Real.two_pi_pos α δ ≠ π →
      (RunMidA α (toIcoMod Real.two_pi_pos α β) (toIcoMod Real.two_pi_pos α δ) →
        rb ≤ ra ∧ rd ≤ ra) →
      (RunMidB α (toIcoMod Real.two_pi_pos α β) (toIcoMod Real.two_pi_pos α δ) →
        ra ≤ rb ∧ rd ≤ rb) →
      (RunMidD α (toIcoMod Real.two_pi_pos α β) (toIcoMod Real.two_pi_pos α δ) →
        rb ≤ rd ∧ ra ≤ rd) →
      0 < orient (polar c ra α) (polar c rb β) (polar c rd δ)) ∧
    (toIcoMod Real.two_pi_pos α δ < toIcoMod Real.two_pi_pos α β →
      toIcoMod Real.two_pi_pos α δ - α ≠ π →
      toIcoMod Real.two_pi_pos α β - toIcoMod Real.two_pi_pos α δ ≠ π →
      α + 2 * π - toIcoMod Real.two_pi_pos α β ≠ π →
      (RunMidA α (toIcoMod Real.two_pi_pos α δ) (toIcoMod Real.two_pi_pos α β) →
        rd ≤ ra ∧ rb ≤ ra) →
      (RunMidB α (toIcoMod Real.two_pi_pos α δ) (toIcoMod Real.two_pi_pos α β) →
        ra ≤ rd ∧ rb ≤ rd) →
      (RunMidD α (toIcoMod Real.two_pi_pos α δ) (toIcoMod Real.two_pi_pos α β) →
        rd ≤ rb ∧ ra ≤ rb) →
      orient (polar c ra α) (polar c rb β) (polar c rd δ) < 0) := by
  have hB := toIcoMod_mem_Ico Real.two_pi_pos α β
  have hD := toIcoMod_mem_Ico Real.two_pi_pos α δ
  have hB0 : α < toIcoMod Real.two_pi_pos α β := lt_of_le_of_ne hB.1 (Ne.symm hβα)
  have hD0 : α < toIcoMod Real.two_pi_pos α δ := lt_of_le_of_ne hD.1 (Ne.symm hδα)
  rw [← polar_toIcoMod c rb α β, ← polar_toIcoMod c rd α δ]
  refine ⟨fun hlt g1 g2 g3 hA hBr hDr => ?_, fun hlt g1 g2 g3 hA hBr hDr => ?_⟩
  · exact orient_pos_of_phase ha hb hd hB0 hlt hD.2 g1 g2 g3 hA hBr hDr
  · have := orient_pos_of_phase (c := c) ha hd hb hD0 hlt hB.2 g1 g2 g3 hA hBr hDr
    rw [orient_swap] at this
    linarith

/-! ## The discrete pattern (as a cyclic word of length 6) -/

/-- **Discrete dichotomy.**  A cyclic word `s : Fin 6 → Bool` (`true` = point `P`, `false` =
antipode `A`) in which position `i + 3` is the antipode of position `i` (`s (i+3) = !s i`) is
either alternating (`PAPAPA`/`APAPAP`) or contains a cyclic run `PPP`, and not both.  This is the
case split of the encoders (`kinds in ('PAPAPA', 'APAPAP')`, else `find('PPP')` in the doubled
word); checked by `decide` over all 64 words. -/
theorem word_dichotomy :
    ∀ s : Fin 6 → Bool, (∀ i : Fin 6, s (i + 3) = !s i) →
      ((∀ i : Fin 6, s (i + 1) = !s i) ∨ ∃ i : Fin 6, s i ∧ s (i + 1) ∧ s (i + 2)) ∧
      ¬ ((∀ i : Fin 6, s (i + 1) = !s i) ∧ ∃ i : Fin 6, s i ∧ s (i + 1) ∧ s (i + 2)) := by
  decide

end PhaseClassification
