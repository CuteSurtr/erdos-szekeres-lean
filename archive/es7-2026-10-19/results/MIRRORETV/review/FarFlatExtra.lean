import Mathlib

/-!
# Extra checks for THEORY.md Theorem B (B_farflat_exact verification), written independently.

Covers the two geometric steps of Theorem B that `theory/lean/FarFlat.lean` does not state:
* `gp_cross_axis`: a point `p` above the axis, a point `q` below it (both with abscissa in `[0, W]`) and an
  axis point `(xa, 0)` with `xa > W` are not collinear (general position of `S`, mixed triples).
* `a1_inside`: with `a1 = (W+1, 0)`, `a2 = (W+2, 0)`, the point `a1` is a strict convex combination of
  `p`, `q`, `a2` (the counting step "a1 lies inside triangle p q a2").
and composes the quantitative bounds of Lemma 5.1 into one statement:
* `lemma51_core`: if `u, q, w` are lifted points with `x_u + g ≤ x_q ≤ x_w - g`, `q` strictly below line `uw`,
  and `z` has height `≤ 0` and horizontal distance `≤ D` from `u` and `w`, and `H g > h D`, then `q` is a
  strict convex combination of `u, w, z`.
-/

namespace FFX

/-- twice the signed area of the triangle (a, b, c) -/
def orient (ax ay bx by' cx cy : ℝ) : ℝ := (bx - ax) * (cy - ay) - (by' - ay) * (cx - ax)

theorem orient_sum (ux uy wx wy zx zy qx qy : ℝ) :
    orient ux uy wx wy qx qy + orient wx wy zx zy qx qy + orient zx zy ux uy qx qy
      = orient ux uy wx wy zx zy := by
  unfold orient; ring

/-- barycentric representation from three sub-orientations of one strict sign (here: negative). -/
theorem bary_of_neg (ux uy wx wy zx zy qx qy : ℝ)
    (h1 : orient ux uy wx wy qx qy < 0) (h2 : orient wx wy zx zy qx qy < 0)
    (h3 : orient zx zy ux uy qx qy < 0) :
    ∃ lu lw lz : ℝ, 0 < lu ∧ 0 < lw ∧ 0 < lz ∧ lu + lw + lz = 1 ∧
      lu * ux + lw * wx + lz * zx = qx ∧ lu * uy + lw * wy + lz * zy = qy := by
  have hsum := orient_sum ux uy wx wy zx zy qx qy
  set T := orient ux uy wx wy zx zy with hTdef
  have hT : T < 0 := by linarith
  have hT0 : T ≠ 0 := ne_of_lt hT
  refine ⟨orient wx wy zx zy qx qy / T, orient zx zy ux uy qx qy / T, orient ux uy wx wy qx qy / T,
    div_pos_of_neg_of_neg h2 hT, div_pos_of_neg_of_neg h3 hT, div_pos_of_neg_of_neg h1 hT, ?_, ?_, ?_⟩
  · field_simp; linarith
  · field_simp; rw [hTdef]; unfold orient; ring
  · field_simp; rw [hTdef]; unfold orient; ring

/-- same, positive orientation (counterclockwise triangle). -/
theorem bary_of_pos (ux uy wx wy zx zy qx qy : ℝ)
    (h1 : 0 < orient ux uy wx wy qx qy) (h2 : 0 < orient wx wy zx zy qx qy)
    (h3 : 0 < orient zx zy ux uy qx qy) :
    ∃ lu lw lz : ℝ, 0 < lu ∧ 0 < lw ∧ 0 < lz ∧ lu + lw + lz = 1 ∧
      lu * ux + lw * wx + lz * zx = qx ∧ lu * uy + lw * wy + lz * zy = qy := by
  have hsum := orient_sum ux uy wx wy zx zy qx qy
  set T := orient ux uy wx wy zx zy with hTdef
  have hT : 0 < T := by linarith
  have hT0 : T ≠ 0 := ne_of_gt hT
  refine ⟨orient wx wy zx zy qx qy / T, orient zx zy ux uy qx qy / T, orient ux uy wx wy qx qy / T,
    div_pos h2 hT, div_pos h3 hT, div_pos h1 hT, ?_, ?_, ?_⟩
  · field_simp; linarith
  · field_simp; rw [hTdef]; unfold orient; ring
  · field_simp; rw [hTdef]; unfold orient; ring

/-- General position of `S` for mixed triples (one point of `R`, one of `mu R`, one axis point right of `R`). -/
theorem gp_cross_axis (W xp yp xq yq xa : ℝ) (hxp0 : 0 ≤ xp) (hxpW : xp ≤ W) (hxq0 : 0 ≤ xq) (hxqW : xq ≤ W)
    (hyp : 0 < yp) (hyq : yq < 0) (hxa : W < xa) :
    orient xp yp xq yq xa 0 ≠ 0 := by
  have key : orient xp yp xq yq xa 0 = yp * (xa - xq) + (-yq) * (xa - xp) := by unfold orient; ring
  have h1 : 0 < yp * (xa - xq) := mul_pos hyp (by linarith)
  have h2 : 0 < (-yq) * (xa - xp) := mul_pos (by linarith) (by linarith)
  rw [key]; exact ne_of_gt (by linarith)

/-- Counting step of Theorem B(i): `a1 = (W+1,0)` lies strictly inside the triangle `p q a2`. -/
theorem a1_inside (W xp yp xq yq : ℝ) (hxp0 : 0 ≤ xp) (hxpW : xp ≤ W) (hxq0 : 0 ≤ xq) (hxqW : xq ≤ W)
    (hyp : 0 < yp) (hyq : yq < 0) :
    ∃ lp lq la : ℝ, 0 < lp ∧ 0 < lq ∧ 0 < la ∧ lp + lq + la = 1 ∧
      lp * xp + lq * xq + la * (W + 2) = W + 1 ∧ lp * yp + lq * yq + la * 0 = 0 := by
  -- the three sub-orientations of a1 w.r.t. the triangle (p, q, a2) are all positive
  have o1 : 0 < orient xp yp xq yq (W + 1) 0 := by
    have key : orient xp yp xq yq (W + 1) 0 = yp * (W + 1 - xq) + (-yq) * (W + 1 - xp) := by
      unfold orient; ring
    rw [key]
    have := mul_pos hyp (show (0:ℝ) < W + 1 - xq by linarith)
    have := mul_pos (show (0:ℝ) < -yq by linarith) (show (0:ℝ) < W + 1 - xp by linarith)
    linarith
  have o2 : 0 < orient xq yq (W + 2) 0 (W + 1) 0 := by
    have key : orient xq yq (W + 2) 0 (W + 1) 0 = -yq := by unfold orient; ring
    rw [key]; linarith
  have o3 : 0 < orient (W + 2) 0 xp yp (W + 1) 0 := by
    have key : orient (W + 2) 0 xp yp (W + 1) 0 = yp := by unfold orient; ring
    rw [key]; exact hyp
  exact bary_of_pos xp yp xq yq (W + 2) 0 (W + 1) 0 o1 o2 o3

/-- Lemma 5.1 core, composed: `q` (an interior lower-chain point of `P ∩ R`) is a strict convex combination of
`u`, `w` (extreme points of `P ∩ R`) and any `z ∈ P \ R`. -/
theorem lemma51_core (xu yu xw yw xq yq xz yz H h g D : ℝ)
    (hg : 0 < g) (hD : 0 ≤ D) (key : h * D < H * g)
    (hyu : H ≤ yu) (hyu' : yu ≤ H + h) (hyw : H ≤ yw) (hyw' : yw ≤ H + h)
    (hyq : H ≤ yq) (hyq' : yq ≤ H + h) (hyz : yz ≤ 0)
    (hxzu : |xz - xu| ≤ D) (hxzw : |xz - xw| ≤ D)
    (hxqu : g ≤ xq - xu) (hxqw : xq - xw ≤ -g)
    (below : orient xu yu xw yw xq yq < 0) :
    ∃ lu lw lz : ℝ, 0 < lu ∧ 0 < lw ∧ 0 < lz ∧ lu + lw + lz = 1 ∧
      lu * xu + lw * xw + lz * xz = xq ∧ lu * yu + lw * yw + lz * yz = yq := by
  have e_qw : |yq - yw| ≤ h := by rw [abs_le]; constructor <;> linarith
  have e_qu : |yq - yu| ≤ h := by rw [abs_le]; constructor <;> linarith
  have hh : 0 ≤ h := le_trans (abs_nonneg _) e_qw
  have hH : 0 < H := by
    have : 0 ≤ h * D := mul_nonneg hh hD
    by_contra hc; push_neg at hc
    have : H * g ≤ 0 := mul_nonpos_of_nonpos_of_nonneg hc hg.le
    linarith
  -- orient(w, z, q) < 0
  have o2 : orient xw yw xz yz xq yq < 0 := by
    have expand : orient xw yw xz yz xq yq = (xz - xw) * (yq - yw) + (yw - yz) * (xq - xw) := by
      unfold orient; ring
    have b1 : (xz - xw) * (yq - yw) ≤ D * h := by
      calc (xz - xw) * (yq - yw) ≤ |(xz - xw) * (yq - yw)| := le_abs_self _
        _ = |xz - xw| * |yq - yw| := abs_mul _ _
        _ ≤ D * h := mul_le_mul hxzw e_qw (abs_nonneg _) hD
    have b2 : (yw - yz) * (xq - xw) ≤ H * (-g) := by
      have hA : H ≤ yw - yz := by linarith
      have hB : xq - xw ≤ -g := hxqw
      have hneg : xq - xw < 0 := by linarith
      calc (yw - yz) * (xq - xw) ≤ H * (xq - xw) := by nlinarith
        _ ≤ H * (-g) := by nlinarith
    rw [expand]; nlinarith
  -- orient(z, u, q) = orient(u, q, z) < 0
  have o3 : orient xz yz xu yu xq yq < 0 := by
    have expand : orient xz yz xu yu xq yq = (xq - xu) * (yz - yu) - (yq - yu) * (xz - xu) := by
      unfold orient; ring
    have b1 : -((yq - yu) * (xz - xu)) ≤ h * D := by
      calc -((yq - yu) * (xz - xu)) ≤ |(yq - yu) * (xz - xu)| := neg_le_abs _
        _ = |yq - yu| * |xz - xu| := abs_mul _ _
        _ ≤ h * D := mul_le_mul e_qu hxzu (abs_nonneg _) hh
    have b2 : (xq - xu) * (yz - yu) ≤ g * (-H) := by
      have hA : yz - yu ≤ -H := by linarith
      calc (xq - xu) * (yz - yu) ≤ g * (yz - yu) := mul_le_mul_of_nonpos_right hxqu (by linarith)
        _ ≤ g * (-H) := by nlinarith
    rw [expand]; nlinarith
  exact bary_of_neg xu yu xw yw xz yz xq yq below o2 o3

end FFX

#print axioms FFX.gp_cross_axis
#print axioms FFX.a1_inside
#print axioms FFX.lemma51_core
#print axioms FFX.bary_of_neg
#print axioms FFX.bary_of_pos
