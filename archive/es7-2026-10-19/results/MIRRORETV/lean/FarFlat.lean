import Mathlib

/-!
# Quantitative core of the far-flat cap lemma (mirrorM/theory, THEORY.md Lemma 5.1 and
"General position of S")

Points of `R` have heights in `[H, H+h]`; a point `z` of `mu R ∪ A` has height `≤ 0` and horizontal
distance `≤ D` from points of `R`; distinct abscissae of `R` differ by at least `g > 0`; and `H*g > h*D`.
-/

/-- twice the signed area of the triangle (a, b, c) -/
def orient (ax ay bx by' cx cy : ℝ) : ℝ := (bx - ax) * (cy - ay) - (by' - ay) * (cx - ax)

/-- Lemma 5.1, second bullet: `orient(w, z, q) < 0`. -/
theorem orient_wzq_neg (xw yw xq yq xz yz H h g D : ℝ)
    (hg : 0 < g) (hD : 0 ≤ D) (key : h * D < H * g)
    (hyw : H ≤ yw) (hyw' : yw ≤ H + h) (hyq : H ≤ yq) (hyq' : yq ≤ H + h)
    (hyz : yz ≤ 0) (hxzw : |xz - xw| ≤ D) (hxqw : xq - xw ≤ -g) :
    orient xw yw xz yz xq yq < 0 := by
  unfold orient
  have e1 : |yq - yw| ≤ h := by rw [abs_le]; constructor <;> linarith
  have h1 : (xz - xw) * (yq - yw) ≤ D * h := by
    calc (xz - xw) * (yq - yw) ≤ |(xz - xw) * (yq - yw)| := le_abs_self _
      _ = |xz - xw| * |yq - yw| := abs_mul _ _
      _ ≤ D * h := mul_le_mul hxzw e1 (abs_nonneg _) hD
  have a1 : H ≤ yw - yz := by linarith
  have a3 : (yw - yz) * (xq - xw) ≤ H * (xq - xw) := by nlinarith
  have a4 : H * (xq - xw) ≤ H * (-g) := by
    have hH : 0 ≤ H := by nlinarith [abs_nonneg (xz - xw)]
    nlinarith
  nlinarith

/-- Lemma 5.1, third bullet: `orient(u, q, z) < 0` (equal to `orient(z, u, q)`). -/
theorem orient_uqz_neg (xu yu xq yq xz yz H h g D : ℝ)
    (hg : 0 < g) (hD : 0 ≤ D) (key : h * D < H * g)
    (hyu : H ≤ yu) (hyu' : yu ≤ H + h) (hyq : H ≤ yq) (hyq' : yq ≤ H + h)
    (hyz : yz ≤ 0) (hxzu : |xz - xu| ≤ D) (hxqu : g ≤ xq - xu) :
    orient xu yu xq yq xz yz < 0 := by
  unfold orient
  have e1 : |yq - yu| ≤ h := by rw [abs_le]; constructor <;> linarith
  have h1 : -((yq - yu) * (xz - xu)) ≤ h * D := by
    calc -((yq - yu) * (xz - xu)) ≤ |(yq - yu) * (xz - xu)| := neg_le_abs _
      _ = |yq - yu| * |xz - xu| := abs_mul _ _
      _ ≤ h * D := mul_le_mul e1 hxzu (abs_nonneg _) (le_trans (abs_nonneg _) e1)
  have hH : 0 ≤ H := by
    have : 0 ≤ h * D := mul_nonneg (le_trans (abs_nonneg _) e1) hD
    nlinarith
  have a1 : yz - yu ≤ -H := by linarith
  have a3 : (xq - xu) * (yz - yu) ≤ g * (yz - yu) :=
    mul_le_mul_of_nonpos_right hxqu (by linarith)
  have a4 : g * (yz - yu) ≤ g * (-H) := by nlinarith
  nlinarith

/-- cyclic invariance used in Lemma 5.1: `orient(z,u,q) = orient(u,q,z)`. -/
theorem orient_cyclic (ax ay bx by' cx cy : ℝ) :
    orient cx cy ax ay bx by' = orient ax ay bx by' cx cy := by
  unfold orient; ring

/-- the area identity giving barycentric coordinates. -/
theorem orient_sum (ux uy wx wy zx zy qx qy : ℝ) :
    orient ux uy wx wy qx qy + orient wx wy zx zy qx qy + orient zx zy ux uy qx qy
      = orient ux uy wx wy zx zy := by
  unfold orient; ring

/-- barycentric representation: if the three sub-orientations are negative, `q` is a strict convex
combination of `u, w, z` (so `q` lies in the convex hull of the other points). -/
theorem inside_triangle (ux uy wx wy zx zy qx qy : ℝ)
    (h1 : orient ux uy wx wy qx qy < 0) (h2 : orient wx wy zx zy qx qy < 0)
    (h3 : orient zx zy ux uy qx qy < 0) :
    ∃ lu lw lz : ℝ, 0 < lu ∧ 0 < lw ∧ 0 < lz ∧ lu + lw + lz = 1 ∧
      lu * ux + lw * wx + lz * zx = qx ∧ lu * uy + lw * wy + lz * zy = qy := by
  have hsum := orient_sum ux uy wx wy zx zy qx qy
  have hT : orient ux uy wx wy zx zy < 0 := by linarith
  have hT0 : orient ux uy wx wy zx zy ≠ 0 := ne_of_lt hT
  refine ⟨orient wx wy zx zy qx qy / orient ux uy wx wy zx zy,
          orient zx zy ux uy qx qy / orient ux uy wx wy zx zy,
          orient ux uy wx wy qx qy / orient ux uy wx wy zx zy,
          div_pos_of_neg_of_neg h2 hT, div_pos_of_neg_of_neg h3 hT, div_pos_of_neg_of_neg h1 hT, ?_, ?_, ?_⟩
  · rw [← add_div, ← add_div, div_eq_one_iff_eq hT0]; linarith
  · rw [div_mul_eq_mul_div, div_mul_eq_mul_div, div_mul_eq_mul_div, ← add_div, ← add_div,
      div_eq_iff hT0]
    unfold orient; ring
  · rw [div_mul_eq_mul_div, div_mul_eq_mul_div, div_mul_eq_mul_div, ← add_div, ← add_div,
      div_eq_iff hT0]
    unfold orient; ring

/-- General position of `S`: a line through two points of `R` (abscissae `≥ g` apart) misses every
point of height `≤ 0` within horizontal distance `D`. -/
theorem line_misses (xp yp xq yq xr yr H h g D : ℝ)
    (hg : 0 < g) (hD : 0 ≤ D) (key : h * D < H * g)
    (hyp : H ≤ yp) (hyp' : yp ≤ H + h) (hyq : H ≤ yq) (hyq' : yq ≤ H + h)
    (hyr : yr ≤ 0) (hxr : |xr - xp| ≤ D) (hgap : g ≤ |xq - xp|) :
    orient xp yp xq yq xr yr ≠ 0 := by
  rcases le_abs'.mp hgap with hneg | hpos
  · -- case xq - xp ≤ -g : the orientation is positive
    apply ne_of_gt
    unfold orient
    have e1 : |yq - yp| ≤ h := by rw [abs_le]; constructor <;> linarith
    have h1 : (yq - yp) * (xr - xp) ≤ h * D := by
      calc (yq - yp) * (xr - xp) ≤ |(yq - yp) * (xr - xp)| := le_abs_self _
        _ = |yq - yp| * |xr - xp| := abs_mul _ _
        _ ≤ h * D := mul_le_mul e1 hxr (abs_nonneg _) (le_trans (abs_nonneg _) e1)
    have a1 : yr - yp ≤ -H := by linarith
    have hH : 0 ≤ H := by
      have : 0 ≤ h * D := mul_nonneg (le_trans (abs_nonneg _) e1) hD
      nlinarith
    have a3 : g * H ≤ (xq - xp) * (yr - yp) := by nlinarith
    nlinarith
  · exact ne_of_lt (orient_uqz_neg xp yp xq yq xr yr H h g D hg hD key hyp hyp' hyq hyq' hyr hxr hpos)

#print axioms orient_wzq_neg
#print axioms orient_uqz_neg
#print axioms orient_sum
#print axioms inside_triangle
#print axioms line_misses
