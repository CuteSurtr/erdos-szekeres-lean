import ES8Geo.Interface

/-!
# ENCBLEAN M6, unit G9rules: the key bridge (G8), the arc bridge (G9) and the angular rules

For a polar labelling `L : PolarLabelling m t T c` (`m` even, `u = 2π/m`) this file proves the two
angular-rule fields of the intended model (`DESIGN.md` §2.4, §3.4 rows G8, G9, `ruleA`, `ruleB`):

* `EncB.Geo.labelling_ruleA`: `AltCCW m L.psiLt a b d → L.chi a b d = true`;
* `EncB.Geo.labelling_ruleB`:
  `BlockCCW m L.psiLt a b d → b.1 ≤ a.1 → b.1 ≤ d.1 → L.chi a b d = true`.

Only `hm : 3 ≤ m` (for `0 < m`), `heven : Even m` and `L` are used: no general position and no
convexity hypothesis. The rules use only the fields `r_pos`, `r_anti`, `ψ_zero`, `ψ_pos`, `ψ_lt`
of `L` (`ψ_inj` enters only `rdir_eq_iff`; `mem_layer` is not used).

**Objects and directions.** The object `(a, true)` is the point `L.P a`, of true direction
`φ + ψ a.1 + a.2·u`; `(a, false)` is its antipode `2c - L.P a`, of true direction that plus `π`
(`odir`, `P_eq_odir`, `antipode_eq_odir`). Its *reduced relative direction* is
`rdir L o = cell m o · u + ψ o.1.1 ∈ [0, 2π)` (`rdir_nonneg`, `rdir_lt`), and
`odir L o ≡ φ + rdir L o (mod 2π)` (`odir_eq`; for the antipode this is `KeyOrder.antipode_even`,
which needs `m` even).

* **G8** (`objLt_iff`, `rdir_eq_iff`): on objects of valid layers, `EncB.objLt m L.psiLt o o'` iff
  `rdir L o < rdir L o'` (`KeyOrder.cell_lt_iff`), and equal reduced directions are equal keys
  (`KeyOrder.cell_eq_iff` plus `ψ_inj`).
* **G9** (`ccwIn_iff_inArc_of_lt`/`_of_gt`, `ccwIn_iff_inArc`, `ccwIn_objLt_iff_inArc`,
  `ccwIn_objLt_iff_inArc_odir`): for `X, Y, Z ∈ [0, 2π)`, `ccwIn (· < ·) X Z Y` (the linear order
  read cyclically) iff `PhaseClassification.inArc X (arcGap X Y) Z`; hence `ccwIn (objLt ..) x z y`
  iff the true direction of `z` lies in the open ccw arc that starts at the true direction of `x`
  and has the length of the arc from `x` to `y`.
* **G9 for a ccw triple** (`lift3`, `arcFrame`): if `(a,true) → (b,true) → (d,true)` is ccw for
  `objLt`, then `P a, P b, P d` have true directions `α < β < δ < α + 2π` (lifts of
  `φ + rdir`; `polar_add_int_two_pi` absorbs the lifts), and each `EncB.ArcHasAntipode` test is
  the `PhaseClassification.arcHasAntipode` test of the corresponding arc. Distinct keys exclude the
  gap `α + 2π - δ = π`: it would give `(d, true)` and `(a, false)` the same reduced direction.
* **Rules.** Rule A is `PhaseClassification.orient_pos_of_alternating`, rule B is
  `PhaseClassification.orient_pos_of_runMidB` with the radii `r a.1 ≤ r b.1 ≥ r d.1` from `r_anti`.
  Instead of the cyclic relabelling via `orient_cycle` suggested in `DESIGN.md` §3.4, the three
  cyclic cases are absorbed by lifting `B`, `D` by `2π` (`lift3`), so `chi a b d` is used as is.

Helpers live in `EncB.Geo.Arc`; the two main theorems are in `EncB.Geo`. Every proof is complete
and checked by the kernel; the `#print axioms` lines at the end list only the standard axioms.
-/

open ErdosSzekeres ErdosSzekeres.LayerLemma

namespace EncB.Geo.Arc

open Real

variable {m t : ℕ} {T : Finset Point} {c : Point}

/-! ## Reduced and true directions of objects -/

/-- Reduced relative direction of an object: `cell · (2π/m) + ψ (layer)`, in `[0, 2π)`. -/
noncomputable def rdir (L : PolarLabelling m t T c) (o : EncB.Pt × Bool) : ℝ :=
  (EncB.cell m o : ℝ) * (2 * π / m) + L.ψ o.1.1

/-- True direction of an object: `φ + ψᵢ + k·(2π/m)` for the point of label `(i, k)`, plus `π` for
its antipode. -/
noncomputable def odir (L : PolarLabelling m t T c) (o : EncB.Pt × Bool) : ℝ :=
  L.φ + L.ψ o.1.1 + (o.1.2 : ℝ) * (2 * π / m) + (if o.2 then 0 else π)

theorem psi_nonneg (L : PolarLabelling m t T c) {i : ℕ} (hi : i < t) : 0 ≤ L.ψ i := by
  rcases Nat.eq_zero_or_pos i with rfl | h
  · rw [L.ψ_zero]
  · exact (L.ψ_pos i h hi).le

theorem psi_lt (L : PolarLabelling m t T c) {i : ℕ} (hi : i < t) : L.ψ i < 2 * π / m :=
  L.ψ_lt i hi

theorem u_pos (hm : 0 < m) : 0 < 2 * π / (m : ℝ) := by
  have : (0 : ℝ) < m := by exact_mod_cast hm
  positivity

theorem cell_lt (hm : 0 < m) {o : EncB.Pt × Bool} (ho : o.1.2 < m) : EncB.cell m o < m := by
  unfold EncB.cell
  split
  · exact ho
  · exact Nat.mod_lt _ hm

theorem rdir_nonneg (hm : 0 < m) (L : PolarLabelling m t T c) {o : EncB.Pt × Bool}
    (ho : o.1.1 < t) : 0 ≤ rdir L o := by
  unfold rdir
  have := psi_nonneg L ho
  have := u_pos hm
  positivity

theorem rdir_lt (hm : 0 < m) (L : PolarLabelling m t T c) {o : EncB.Pt × Bool}
    (ho : EncB.PtOk m t o.1) : rdir L o < 2 * π := by
  unfold rdir
  have hc : EncB.cell m o + 1 ≤ m := cell_lt hm ho.2
  have hc' : (EncB.cell m o : ℝ) + 1 ≤ m := by exact_mod_cast hc
  have hu := u_pos hm
  have hψ := psi_lt L ho.1
  have hmR : (0 : ℝ) < m := by exact_mod_cast hm
  have key : (m : ℝ) * (2 * π / m) = 2 * π := by field_simp
  nlinarith

/-- The antipode object's reduced direction is the point's plus `π`, modulo `2π`
(`KeyOrder.antipode_even`; `m` even). -/
theorem rdir_false (hm : 0 < m) (heven : Even m) (L : PolarLabelling m t T c) {a : EncB.Pt}
    (ha : a.1 < t) : ∃ e : ℤ, rdir L (a, false) = rdir L (a, true) + π + 2 * π * e := by
  have h := KeyOrder.antipode_even hm heven (a.2 : ℤ) (psi_nonneg L ha) (psi_lt L ha)
  have hcast : (((a.2 + m / 2) % m : ℕ) : ℝ) =
      ((((a.2 : ℤ) + ((m / 2 : ℕ) : ℤ)) % (m : ℤ) : ℤ) : ℝ) := by
    rw [← Int.cast_natCast]
    norm_cast
  refine ⟨-toIcoDiv Real.two_pi_pos 0 ((a.2 : ℤ) * (2 * π / m) + L.ψ a.1 + π), ?_⟩
  have hs := self_sub_toIcoMod Real.two_pi_pos 0 ((a.2 : ℤ) * (2 * π / m) + L.ψ a.1 + π)
  rw [h, zsmul_eq_mul] at hs
  simp only [rdir, EncB.cell, Bool.false_eq_true, ↓reduceIte, hcast]
  push_cast at hs ⊢
  linarith

/-- True direction = `φ` + reduced direction, modulo `2π`. -/
theorem odir_eq (hm : 0 < m) (heven : Even m) (L : PolarLabelling m t T c) {o : EncB.Pt × Bool}
    (ho : o.1.1 < t) : ∃ n : ℤ, odir L o = L.φ + rdir L o + 2 * π * n := by
  obtain ⟨a, b⟩ := o
  cases b
  · obtain ⟨e, he⟩ := rdir_false hm heven L (a := a) ho
    refine ⟨-e, ?_⟩
    rw [he]
    simp only [odir, rdir, EncB.cell, Bool.false_eq_true, ↓reduceIte]
    push_cast
    ring
  · refine ⟨0, ?_⟩
    simp only [odir, rdir, EncB.cell, ↓reduceIte]
    push_cast
    ring

/-- The point of an object `(a, true)` has direction `odir L (a, true)`. -/
theorem P_eq_odir (L : PolarLabelling m t T c) (a : EncB.Pt) :
    L.P a = polar c (L.r a.1) (odir L (a, true)) := by
  simp only [PolarLabelling.P, odir, ↓reduceIte, add_zero]

/-- `polar c r (θ + π)` is the reflection of `polar c r θ` in `c`. -/
theorem polar_add_pi (c : Point) (r θ : ℝ) : polar c r (θ + π) = (2 : ℝ) • c - polar c r θ := by
  funext i
  fin_cases i <;> simp [polar, Real.cos_add_pi, Real.sin_add_pi] <;> ring

/-- The object `(a, false)` is the antipode `2c - P a` of the point of `a`. -/
theorem antipode_eq_odir (L : PolarLabelling m t T c) (a : EncB.Pt) :
    polar c (L.r a.1) (odir L (a, false)) = (2 : ℝ) • c - L.P a := by
  simp only [odir, Bool.false_eq_true, ↓reduceIte, PolarLabelling.P, polar_add_pi]

/-- The label map at any lift `φ + rdir + 2πn` of the direction, with `PhaseClassification.polar`
(equal to `LayerLemma.polar` by `Capstone.polar_eq`). -/
theorem P_eq_polar (L : PolarLabelling m t T c) (a : EncB.Pt) {θ : ℝ} (n : ℤ)
    (hθ : θ = L.φ + rdir L (a, true) + 2 * π * n) :
    L.P a = PhaseClassification.polar c (L.r a.1) θ := by
  rw [hθ, show L.φ + rdir L (a, true) + 2 * π * n =
      (L.φ + L.ψ a.1 + (a.2 : ℝ) * (2 * π / m)) + (n : ℝ) * (2 * π) by
    simp only [rdir, EncB.cell, ↓reduceIte]; ring, PhaseClassification.polar_add_int_two_pi]
  exact ErdosSzekeres.Capstone.polar_eq _ _ _

/-! ## G8: the key bridge -/

/-- **G8.** On objects of valid layers, `objLt` is the real order of the reduced directions
(`KeyOrder.cell_lt_iff`, with `psiLt` read as `ψ i < ψ j`). -/
theorem objLt_iff (hm : 0 < m) (L : PolarLabelling m t T c) {o o' : EncB.Pt × Bool}
    (ho : o.1.1 < t) (ho' : o'.1.1 < t) :
    EncB.objLt m L.psiLt o o' ↔ rdir L o < rdir L o' := by
  have h := KeyOrder.cell_lt_iff (u_pos hm) (EncB.cell m o : ℤ) (EncB.cell m o' : ℤ)
    (psi_nonneg L ho) (psi_lt L ho) (psi_nonneg L ho') (psi_lt L ho')
  simp only [Int.cast_natCast, Nat.cast_lt, Nat.cast_inj] at h
  unfold rdir
  rw [h]
  simp [EncB.objLt, PolarLabelling.psiLt]

/-- **G8, equality.** Two objects of valid layers have the same reduced direction iff they have
the same cell and the same layer (`KeyOrder.cell_eq_iff` and `ψ_inj`). -/
theorem rdir_eq_iff (hm : 0 < m) (L : PolarLabelling m t T c) {o o' : EncB.Pt × Bool}
    (ho : o.1.1 < t) (ho' : o'.1.1 < t) :
    rdir L o = rdir L o' ↔ EncB.cell m o = EncB.cell m o' ∧ o.1.1 = o'.1.1 := by
  have h := KeyOrder.cell_eq_iff (u_pos hm) (EncB.cell m o : ℤ) (EncB.cell m o' : ℤ)
    (psi_nonneg L ho) (psi_lt L ho) (psi_nonneg L ho') (psi_lt L ho')
  simp only [Int.cast_natCast, Nat.cast_inj] at h
  unfold rdir
  rw [h]
  constructor
  · rintro ⟨h1, h2⟩
    exact ⟨h1, L.ψ_inj _ _ ho ho' h2⟩
  · rintro ⟨h1, h2⟩
    exact ⟨h1, by rw [h2]⟩

/-! ## G9: arcs of the cyclically read linear order on `[0, 2π)` are circular arcs -/

/-- `inArc` depends only on `θ - s` modulo `2π` and on the gap. -/
theorem inArc_congr {s g θ s' g' θ' : ℝ} (n : ℤ) (hg : g' = g)
    (h : θ' - s' = θ - s + 2 * π * n) :
    PhaseClassification.inArc s' g' θ' ↔ PhaseClassification.inArc s g θ := by
  subst hg
  constructor
  · rintro ⟨k, h1, h2⟩
    exact ⟨k + n, by push_cast; linarith, by push_cast; linarith⟩
  · rintro ⟨k, h1, h2⟩
    exact ⟨k - n, by push_cast; linarith, by push_cast; linarith⟩

/-- An integer `k` with `-2π < 2πk < 2π` is `0`. -/
theorem int_eq_zero_of {k : ℤ} (h1 : -(2 * π) < 2 * π * k) (h2 : 2 * π * k < 2 * π) : k = 0 := by
  have hp : 0 < 2 * π := by positivity
  have a : (k : ℝ) < 1 := by nlinarith
  have b : (-1 : ℝ) < k := by nlinarith
  have a' : k < 1 := by exact_mod_cast a
  have b' : -1 < k := by exact_mod_cast b
  omega

/-- An integer `k` with `-2π < 2πk < 4π` is `0` or `1`. -/
theorem int_eq_zero_or_one_of {k : ℤ} (h1 : -(2 * π) < 2 * π * k) (h2 : 2 * π * k < 4 * π) :
    k = 0 ∨ k = 1 := by
  have hp : 0 < 2 * π := by positivity
  have a : (k : ℝ) < 2 := by nlinarith
  have b : (-1 : ℝ) < k := by nlinarith
  have a' : k < 2 := by exact_mod_cast a
  have b' : -1 < k := by exact_mod_cast b
  omega

/-- Two reduced directions that differ by a multiple of `2π` are equal. -/
theorem eq_of_two_pi_mul {X Y : ℝ} (hX0 : 0 ≤ X) (hX : X < 2 * π) (hY0 : 0 ≤ Y) (hY : Y < 2 * π)
    (n : ℤ) (h : X = Y + 2 * π * n) : X = Y := by
  obtain rfl : n = 0 := int_eq_zero_of (by linarith) (by linarith)
  simpa using h

/-- **G9 core, `X < Y`.** For directions in `[0, 2π)`, `Z` is strictly inside the ccw arc from `X`
to `Y` of the cyclically read linear order iff it lies in the open circular arc `(X, Y)`. -/
theorem ccwIn_iff_inArc_of_lt {X Y Z : ℝ} (hX : 0 ≤ X) (hY : Y < 2 * π) (hZ0 : 0 ≤ Z)
    (hZ : Z < 2 * π) (hXY : X < Y) :
    EncB.ccwIn (fun x y : ℝ => x < y) X Z Y ↔ PhaseClassification.inArc X (Y - X) Z := by
  simp only [EncB.ccwIn]
  constructor
  · rintro (⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩)
    · exact ⟨0, by push_cast; linarith, by push_cast; linarith⟩
    · linarith
    · linarith
  · rintro ⟨k, h1, h2⟩
    obtain rfl : k = 0 := int_eq_zero_of (by linarith) (by linarith)
    push_cast at h1 h2
    exact Or.inl ⟨by linarith, by linarith⟩

/-- **G9 core, `Y < X`** (the arc wraps past `2π`): the open circular arc `(X, Y + 2π)`. -/
theorem ccwIn_iff_inArc_of_gt {X Y Z : ℝ} (hX : X < 2 * π) (hY : 0 ≤ Y) (hZ0 : 0 ≤ Z)
    (hZ : Z < 2 * π) (hYX : Y < X) :
    EncB.ccwIn (fun x y : ℝ => x < y) X Z Y ↔ PhaseClassification.inArc X (Y + 2 * π - X) Z := by
  simp only [EncB.ccwIn]
  constructor
  · rintro (⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩)
    · linarith
    · exact ⟨0, by push_cast; linarith, by push_cast; linarith⟩
    · exact ⟨1, by push_cast; linarith, by push_cast; linarith⟩
  · rintro ⟨k, h1, h2⟩
    rcases int_eq_zero_or_one_of (k := k) (by linarith) (by linarith) with rfl | rfl
    · push_cast at h1 h2
      exact Or.inr (Or.inl ⟨hYX, by linarith⟩)
    · push_cast at h1 h2
      exact Or.inr (Or.inr ⟨by linarith, hYX⟩)

/-- Length of the ccw arc from `X` to `Y` for `X, Y ∈ [0, 2π)` (`0` when `X = Y`). -/
noncomputable def arcGap (X Y : ℝ) : ℝ := if X ≤ Y then Y - X else Y + 2 * π - X

/-- **G9 (reals).** For `X, Y, Z ∈ [0, 2π)`: `ccwIn (· < ·) X Z Y` iff `Z` lies, modulo `2π`, in
the open ccw arc `(X, X + arcGap X Y)`. -/
theorem ccwIn_iff_inArc {X Y Z : ℝ} (hX0 : 0 ≤ X) (hX : X < 2 * π) (hY0 : 0 ≤ Y) (hY : Y < 2 * π)
    (hZ0 : 0 ≤ Z) (hZ : Z < 2 * π) :
    EncB.ccwIn (fun x y : ℝ => x < y) X Z Y ↔ PhaseClassification.inArc X (arcGap X Y) Z := by
  unfold arcGap
  rcases lt_trichotomy X Y with h | rfl | h
  · rw [if_pos h.le]
    exact ccwIn_iff_inArc_of_lt hX0 hY hZ0 hZ h
  · rw [if_pos le_rfl, sub_self]
    simp only [EncB.ccwIn]
    constructor
    · rintro (⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩) <;> linarith
    · rintro ⟨k, h1, h2⟩
      linarith
  · rw [if_neg (not_le.2 h)]
    exact ccwIn_iff_inArc_of_gt hX hY0 hZ0 hZ h

/-- `ccwIn` transported along a map that matches the two orders on the three pairs it reads. -/
theorem ccwIn_map {α β : Type} {lt : α → α → Prop} {lt' : β → β → Prop} (f : α → β) {x z y : α}
    (hxz : lt x z ↔ lt' (f x) (f z)) (hzy : lt z y ↔ lt' (f z) (f y))
    (hyx : lt y x ↔ lt' (f y) (f x)) :
    EncB.ccwIn lt x z y ↔ EncB.ccwIn lt' (f x) (f z) (f y) := by
  simp only [EncB.ccwIn, hxz, hzy, hyx]

/-- `ccwIn` for `objLt` is `ccwIn` for the real order of the reduced directions (by G8). -/
theorem ccwIn_objLt_iff (hm : 0 < m) (L : PolarLabelling m t T c) {x z y : EncB.Pt × Bool}
    (hx : x.1.1 < t) (hz : z.1.1 < t) (hy : y.1.1 < t) :
    EncB.ccwIn (EncB.objLt m L.psiLt) x z y ↔
      EncB.ccwIn (fun p q : ℝ => p < q) (rdir L x) (rdir L z) (rdir L y) :=
  ccwIn_map (rdir L) (objLt_iff hm L hx hz) (objLt_iff hm L hz hy) (objLt_iff hm L hy hx)

/-- **G9 (objects, reduced directions).** For objects of valid labels, `z` is inside the ccw arc
from `x` to `y` for `objLt` iff `rdir z` lies in the open arc `(rdir x, rdir x + arcGap)`. -/
theorem ccwIn_objLt_iff_inArc (hm : 0 < m) (L : PolarLabelling m t T c)
    {x z y : EncB.Pt × Bool} (hx : EncB.PtOk m t x.1) (hz : EncB.PtOk m t z.1)
    (hy : EncB.PtOk m t y.1) :
    EncB.ccwIn (EncB.objLt m L.psiLt) x z y ↔
      PhaseClassification.inArc (rdir L x) (arcGap (rdir L x) (rdir L y)) (rdir L z) := by
  rw [ccwIn_objLt_iff hm L hx.1 hz.1 hy.1]
  exact ccwIn_iff_inArc (rdir_nonneg hm L hx.1) (rdir_lt hm L hx) (rdir_nonneg hm L hy.1)
    (rdir_lt hm L hy) (rdir_nonneg hm L hz.1) (rdir_lt hm L hz)

/-- **G9 (objects, true directions).** For objects of valid labels, `z` is inside the ccw arc from
`x` to `y` for `objLt` iff the true direction of `z` (point or antipode, `P_eq_odir`,
`antipode_eq_odir`) lies in the open ccw arc that starts at the true direction of `x` and is as
long as the arc from `x` to `y`. -/
theorem ccwIn_objLt_iff_inArc_odir (hm : 0 < m) (heven : Even m) (L : PolarLabelling m t T c)
    {x z y : EncB.Pt × Bool} (hx : EncB.PtOk m t x.1) (hz : EncB.PtOk m t z.1)
    (hy : EncB.PtOk m t y.1) :
    EncB.ccwIn (EncB.objLt m L.psiLt) x z y ↔
      PhaseClassification.inArc (odir L x) (arcGap (rdir L x) (rdir L y)) (odir L z) := by
  rw [ccwIn_objLt_iff_inArc hm L hx hz hy]
  obtain ⟨nx, hnx⟩ := odir_eq hm heven L hx.1
  obtain ⟨nz, hnz⟩ := odir_eq hm heven L hz.1
  exact (inArc_congr (nz - nx) rfl (by rw [hnx, hnz]; push_cast; ring)).symm

/-! ## G9 for a ccw triple, and the frame of the two rules -/

/-- **G9 for a ccw triple.** If `A → B → D` is counterclockwise in the cyclically read linear
order on `[0, 2π)`, there are lifts `β ≡ B`, `δ ≡ D` (mod `2π`) with `A < β < δ < A + 2π` such
that, for every `Z ∈ [0, 2π)`, `ccwIn` on each of the three arcs is membership in the open arcs
`(A, β)`, `(β, δ)`, `(δ, A + 2π)`. -/
theorem lift3 {A B D : ℝ} (hA0 : 0 ≤ A) (hA : A < 2 * π) (hB0 : 0 ≤ B) (hB : B < 2 * π)
    (hD0 : 0 ≤ D) (hD : D < 2 * π) (h : EncB.ccwIn (fun x y : ℝ => x < y) A B D) :
    ∃ β δ : ℝ, (∃ nb : ℤ, β = B + 2 * π * nb) ∧ (∃ nd : ℤ, δ = D + 2 * π * nd) ∧
      A < β ∧ β < δ ∧ δ < A + 2 * π ∧
      (∀ Z, 0 ≤ Z → Z < 2 * π →
        (EncB.ccwIn (fun x y : ℝ => x < y) A Z B ↔ PhaseClassification.inArc A (β - A) Z)) ∧
      (∀ Z, 0 ≤ Z → Z < 2 * π →
        (EncB.ccwIn (fun x y : ℝ => x < y) B Z D ↔ PhaseClassification.inArc β (δ - β) Z)) ∧
      (∀ Z, 0 ≤ Z → Z < 2 * π →
        (EncB.ccwIn (fun x y : ℝ => x < y) D Z A ↔
          PhaseClassification.inArc δ (A + 2 * π - δ) Z)) := by
  have hpi := Real.pi_pos
  rcases h with ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · -- `A < B < D`: no lift
    refine ⟨B, D, ⟨0, by simp⟩, ⟨0, by simp⟩, h1, h2, by linarith, fun Z hZ0 hZ => ?_,
      fun Z hZ0 hZ => ?_, fun Z hZ0 hZ => ?_⟩
    · exact ccwIn_iff_inArc_of_lt hA0 hB hZ0 hZ h1
    · exact ccwIn_iff_inArc_of_lt hB0 hD hZ0 hZ h2
    · exact ccwIn_iff_inArc_of_gt hD hA0 hZ0 hZ (by linarith)
  · -- `D < A < B`: lift `D` by `2π`
    refine ⟨B, D + 2 * π, ⟨0, by simp⟩, ⟨1, by simp⟩, h2, by linarith, by linarith,
      fun Z hZ0 hZ => ?_, fun Z hZ0 hZ => ?_, fun Z hZ0 hZ => ?_⟩
    · exact ccwIn_iff_inArc_of_lt hA0 hB hZ0 hZ h2
    · exact ccwIn_iff_inArc_of_gt hB hD0 hZ0 hZ (by linarith)
    · rw [ccwIn_iff_inArc_of_lt hD0 hA hZ0 hZ h1]
      exact (inArc_congr (-1) (by ring) (by push_cast; ring)).symm
  · -- `B < D < A`: lift `B` and `D` by `2π`
    refine ⟨B + 2 * π, D + 2 * π, ⟨1, by simp⟩, ⟨1, by simp⟩, by linarith, by linarith,
      by linarith, fun Z hZ0 hZ => ?_, fun Z hZ0 hZ => ?_, fun Z hZ0 hZ => ?_⟩
    · exact ccwIn_iff_inArc_of_gt hA hB0 hZ0 hZ (h1.trans h2)
    · rw [ccwIn_iff_inArc_of_lt hB0 hD hZ0 hZ h1]
      exact (inArc_congr (-1) (by ring) (by push_cast; ring)).symm
    · rw [ccwIn_iff_inArc_of_lt hD0 hA hZ0 hZ h2]
      exact (inArc_congr (-1) (by ring) (by push_cast; ring)).symm

/-- The three antipode tests of an arc, moved from reduced directions (`Af ≡ A + π`, …) to the
true directions `α ≡ φ + A`, … (all congruences mod `2π`). -/
theorem arcHasAntipode_iff_of (φ : ℝ) {A B D Af Bf Df α β δ X s g g' : ℝ}
    (na nb nd ea eb ed : ℤ)
    (hα : α = φ + A + 2 * π * na) (hβ : β = φ + B + 2 * π * nb) (hδ : δ = φ + D + 2 * π * nd)
    (hAf : Af = A + π + 2 * π * ea) (hBf : Bf = B + π + 2 * π * eb)
    (hDf : Df = D + π + 2 * π * ed) (hs : s = φ + X) (hg : g' = g) :
    (PhaseClassification.inArc X g Af ∨ PhaseClassification.inArc X g Bf ∨
        PhaseClassification.inArc X g Df) ↔
      PhaseClassification.arcHasAntipode α β δ s g' := by
  unfold PhaseClassification.arcHasAntipode
  exact or_congr (inArc_congr (na - ea) hg (by rw [hα, hs, hAf]; push_cast; ring)).symm
    (or_congr (inArc_congr (nb - eb) hg (by rw [hβ, hs, hBf]; push_cast; ring)).symm
      (inArc_congr (nd - ed) hg (by rw [hδ, hs, hDf]; push_cast; ring)).symm)

/-- `ArcHasAntipode` in terms of reduced directions (by G8). -/
theorem arcHasAntipode_rdir (hm : 0 < m) (L : PolarLabelling m t T c) {a b d x y : EncB.Pt}
    (ha : a.1 < t) (hb : b.1 < t) (hd : d.1 < t) (hx : x.1 < t) (hy : y.1 < t) :
    EncB.ArcHasAntipode m L.psiLt a b d x y ↔
      (EncB.ccwIn (fun p q : ℝ => p < q) (rdir L (x, true)) (rdir L (a, false))
          (rdir L (y, true)) ∨
        EncB.ccwIn (fun p q : ℝ => p < q) (rdir L (x, true)) (rdir L (b, false))
          (rdir L (y, true)) ∨
        EncB.ccwIn (fun p q : ℝ => p < q) (rdir L (x, true)) (rdir L (d, false))
          (rdir L (y, true))) := by
  unfold EncB.ArcHasAntipode
  simp only [List.mem_cons, List.not_mem_nil, or_false, exists_eq_or_imp, exists_eq_left]
  rw [ccwIn_objLt_iff hm L hx ha hy, ccwIn_objLt_iff hm L hx hb hy, ccwIn_objLt_iff hm L hx hd hy]

/-- **The frame of a ccw triple of valid labels.** True directions `α < β < δ < α + 2π` of
`P a, P b, P d` in which the three `EncB.ArcHasAntipode` tests are the
`PhaseClassification.arcHasAntipode` tests of the arcs `(α, β)`, `(β, δ)`, `(δ, α + 2π)`, and in
which distinct keys exclude the gap `α + 2π - δ = π`. -/
theorem arcFrame (hm : 0 < m) (heven : Even m) (L : PolarLabelling m t T c) {a b d : EncB.Pt}
    (ha : EncB.PtOk m t a) (hb : EncB.PtOk m t b) (hd : EncB.PtOk m t d)
    (hccw : EncB.ccwIn (EncB.objLt m L.psiLt) (a, true) (b, true) (d, true)) :
    ∃ α β δ : ℝ, α < β ∧ β < δ ∧ δ < α + 2 * π ∧
      L.P a = PhaseClassification.polar c (L.r a.1) α ∧
      L.P b = PhaseClassification.polar c (L.r b.1) β ∧
      L.P d = PhaseClassification.polar c (L.r d.1) δ ∧
      (EncB.ArcHasAntipode m L.psiLt a b d a b ↔
        PhaseClassification.arcHasAntipode α β δ α (β - α)) ∧
      (EncB.ArcHasAntipode m L.psiLt a b d b d ↔
        PhaseClassification.arcHasAntipode α β δ β (δ - β)) ∧
      (EncB.ArcHasAntipode m L.psiLt a b d d a ↔
        PhaseClassification.arcHasAntipode α β δ δ (α + 2 * π - δ)) ∧
      (EncB.KeysDistinct m L.psiLt a b d → α + 2 * π - δ ≠ π) := by
  -- reduced directions of the six objects, all in `[0, 2π)`
  have hA0 := rdir_nonneg hm L (o := (a, true)) ha.1
  have hB0 := rdir_nonneg hm L (o := (b, true)) hb.1
  have hD0 := rdir_nonneg hm L (o := (d, true)) hd.1
  have hA := rdir_lt hm L (o := (a, true)) ha
  have hB := rdir_lt hm L (o := (b, true)) hb
  have hD := rdir_lt hm L (o := (d, true)) hd
  have hAf0 := rdir_nonneg hm L (o := (a, false)) ha.1
  have hBf0 := rdir_nonneg hm L (o := (b, false)) hb.1
  have hDf0 := rdir_nonneg hm L (o := (d, false)) hd.1
  have hAf := rdir_lt hm L (o := (a, false)) ha
  have hBf := rdir_lt hm L (o := (b, false)) hb
  have hDf := rdir_lt hm L (o := (d, false)) hd
  obtain ⟨ea, hea⟩ := rdir_false hm heven L ha.1
  obtain ⟨eb, heb⟩ := rdir_false hm heven L hb.1
  obtain ⟨ed, hed⟩ := rdir_false hm heven L hd.1
  rw [ccwIn_objLt_iff hm L ha.1 hb.1 hd.1] at hccw
  obtain ⟨β, δ, ⟨nb, hβ⟩, ⟨nd, hδ⟩, h1, h2, h3, arcAB, arcBD, arcDA⟩ :=
    lift3 hA0 hA hB0 hB hD0 hD hccw
  refine ⟨L.φ + rdir L (a, true), L.φ + β, L.φ + δ, by linarith, by linarith, by linarith,
    P_eq_polar L a 0 (by simp), P_eq_polar L b nb (by rw [hβ]; ring),
    P_eq_polar L d nd (by rw [hδ]; ring), ?_, ?_, ?_, ?_⟩
  · rw [arcHasAntipode_rdir hm L ha.1 hb.1 hd.1 ha.1 hb.1, arcAB _ hAf0 hAf, arcAB _ hBf0 hBf,
      arcAB _ hDf0 hDf]
    exact arcHasAntipode_iff_of L.φ 0 nb nd ea eb ed (by simp) (by rw [hβ]; ring)
      (by rw [hδ]; ring) hea heb hed rfl (by ring)
  · rw [arcHasAntipode_rdir hm L ha.1 hb.1 hd.1 hb.1 hd.1, arcBD _ hAf0 hAf, arcBD _ hBf0 hBf,
      arcBD _ hDf0 hDf]
    exact arcHasAntipode_iff_of L.φ 0 nb nd ea eb ed (by simp) (by rw [hβ]; ring)
      (by rw [hδ]; ring) hea heb hed rfl (by ring)
  · rw [arcHasAntipode_rdir hm L ha.1 hb.1 hd.1 hd.1 ha.1, arcDA _ hAf0 hAf, arcDA _ hBf0 hBf,
      arcDA _ hDf0 hDf]
    exact arcHasAntipode_iff_of L.φ 0 nb nd ea eb ed (by simp) (by rw [hβ]; ring)
      (by rw [hδ]; ring) hea heb hed rfl (by ring)
  · intro hkeys hgap
    -- the gap `π` would give `(d, true)` and `(a, false)` the same reduced direction
    have heq : rdir L (d, true) = rdir L (a, false) :=
      eq_of_two_pi_mul hD0 hD hAf0 hAf (-nd - ea) (by rw [hea]; push_cast; linarith)
    have hk := hkeys (d, true) (by simp [EncB.objs6]) (a, false) (by simp [EncB.objs6])
      (by simp)
    rw [objLt_iff hm L hd.1 ha.1, objLt_iff hm L ha.1 hd.1] at hk
    rcases hk with hk | hk <;> linarith

end EncB.Geo.Arc

namespace EncB.Geo

/-- **Rule A** (the `ruleA` field of the intended model): a ccw triple whose six-object pattern
alternates (`AltCCW`) turns left. -/
theorem labelling_ruleA {m t : ℕ} (hm : 3 ≤ m) (heven : Even m) {T : Finset Point} {c : Point}
    (L : PolarLabelling m t T c) :
    ∀ a b d, EncB.PtOk m t a → EncB.PtOk m t b → EncB.PtOk m t d → EncB.Distinct3 a b d →
      EncB.AltCCW m L.psiLt a b d → L.chi a b d = true := by
  intro a b d ha hb hd _ hA
  obtain ⟨_, hccw, h1, h2, h3⟩ := hA
  obtain ⟨α, β, δ, hab, hbd, hda, hPa, hPb, hPd, e1, e2, e3, _⟩ :=
    Arc.arcFrame (by omega) heven L ha hb hd hccw
  have hpos := PhaseClassification.orient_pos_of_alternating (c := c)
    (L.r_pos a.1 ha.1) (L.r_pos b.1 hb.1) (L.r_pos d.1 hd.1) hab hbd hda
    ⟨e1.1 h1, e2.1 h2, e3.1 h3⟩
  rw [← hPa, ← hPb, ← hPd] at hpos
  simp [PolarLabelling.chi, hpos]

/-- **Rule B** (the `ruleB` field of the intended model): a ccw triple whose arcs `(a, b)` and
`(b, d)` hold no antipode (`BlockCCW`), with the middle label `b` on the outermost of the three
layers, turns left. -/
theorem labelling_ruleB {m t : ℕ} (hm : 3 ≤ m) (heven : Even m) {T : Finset Point} {c : Point}
    (L : PolarLabelling m t T c) :
    ∀ a b d, EncB.PtOk m t a → EncB.PtOk m t b → EncB.PtOk m t d → EncB.Distinct3 a b d →
      EncB.BlockCCW m L.psiLt a b d → b.1 ≤ a.1 → b.1 ≤ d.1 → L.chi a b d = true := by
  intro a b d ha hb hd _ hB hba hbd'
  obtain ⟨hkeys, hccw, h1, h2⟩ := hB
  obtain ⟨α, β, δ, hab, hbd, hda, hPa, hPb, hPd, e1, e2, _, hg3⟩ :=
    Arc.arcFrame (by omega) heven L ha hb hd hccw
  have hpos := PhaseClassification.orient_pos_of_runMidB (c := c)
    (L.r_pos a.1 ha.1) (L.r_pos d.1 hd.1) hab hbd hda (hg3 hkeys)
    ⟨fun h => h1 (e1.2 h), fun h => h2 (e2.2 h)⟩
    (L.r_anti b.1 a.1 hba ha.1) (L.r_anti b.1 d.1 hbd' hd.1)
  rw [← hPa, ← hPb, ← hPd] at hpos
  simp [PolarLabelling.chi, hpos]

end EncB.Geo

#print axioms EncB.Geo.labelling_ruleA
#print axioms EncB.Geo.labelling_ruleB
#print axioms EncB.Geo.Arc.objLt_iff
#print axioms EncB.Geo.Arc.rdir_eq_iff
#print axioms EncB.Geo.Arc.ccwIn_iff_inArc
#print axioms EncB.Geo.Arc.ccwIn_objLt_iff_inArc
#print axioms EncB.Geo.Arc.ccwIn_objLt_iff_inArc_odir
#print axioms EncB.Geo.Arc.arcFrame
