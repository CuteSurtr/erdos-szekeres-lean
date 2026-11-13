import ErdosSzekeres.Suk.SpikeGeometry

namespace ErdosSzekeres.Suk

/-- Local data for two neighboring support spikes. All fields are orientation
conditions on the original five anchors. -/
structure AdjacentCapFrames where
  left : CapFrame
  e : Point
  bce : orient left.b left.c e < 0
  bde : orient left.b left.d e < 0
  cde : orient left.c left.d e < 0

def AdjacentCapFrames.right (F : AdjacentCapFrames) : CapFrame :=
  ⟨F.left.b, F.left.c, F.left.d, F.e, F.left.bcd, F.bce, F.bde, F.cde⟩

/-- Every point of the neighboring spike lies strictly to the left of both
rays from a point of the first spike toward its outer base endpoints. -/
theorem AdjacentCapFrames.cross_orientation (F : AdjacentCapFrames) {p q : Point}
    (hp : p ∈ F.left.spike) (hq : q ∈ F.right.spike) :
    0 < orient p F.left.a q ∧ 0 < orient p F.left.d q := by
  have hp' := F.left.spike_orientations hp
  have hq' := F.right.spike_orientations hq
  change orient F.left.b F.left.c q < 0 ∧ 0 < orient F.left.c F.left.d q ∧
    orient F.left.d F.e q < 0 at hq
  change 0 < orient F.left.b F.left.d q ∧ 0 < orient F.left.b F.e q ∧
    0 < orient F.left.c F.e q at hq'
  have e₀ : orient F.left.a F.left.b F.left.c * orient F.left.b F.left.d q =
      orient F.left.a F.left.b F.left.d * orient F.left.b F.left.c q -
        orient F.left.a F.left.b q * orient F.left.b F.left.c F.left.d := by
    simp only [orient]
    ring
  have e₁ : orient F.left.b F.left.c F.left.d * orient F.left.a F.left.c q =
      -orient F.left.a F.left.b F.left.c * orient F.left.c F.left.d q +
        orient F.left.b F.left.c q * orient F.left.a F.left.c F.left.d := by
    simp only [orient]
    ring
  have habq : orient F.left.a F.left.b q < 0 := by
    have h₀ := mul_neg_of_neg_of_pos F.left.abc hq'.1
    have h₁ := mul_pos_of_neg_of_neg F.left.abd hq.1
    by_contra! hn
    have h₂ := mul_nonpos_of_nonneg_of_nonpos hn F.left.bcd.le
    linarith
  have hacq : orient F.left.a F.left.c q < 0 := by
    have h₀ := mul_pos (neg_pos.mpr F.left.abc) hq.2.1
    have h₁ := mul_pos_of_neg_of_neg hq.1 F.left.acd
    by_contra! hn
    have h₂ := mul_nonpos_of_nonpos_of_nonneg F.left.bcd.le hn
    linarith
  constructor
  · have he : orient F.left.a F.left.b F.left.c * orient p F.left.a q =
        -orient F.left.a F.left.b p * orient F.left.a F.left.c q +
          orient F.left.a F.left.b q * orient F.left.a F.left.c p := by
      simp only [orient]
      ring
    have h₀ := mul_neg_of_pos_of_neg (neg_pos.mpr hp.1) hacq
    have h₁ := mul_neg_of_neg_of_pos habq hp'.1
    by_contra! hn
    have h₂ := mul_nonneg_of_nonpos_of_nonpos F.left.abc.le hn
    linarith
  · have he : orient F.left.b F.left.c F.left.d * orient p F.left.d q =
        -orient F.left.b F.left.d p * orient F.left.c F.left.d q +
          orient F.left.b F.left.d q * orient F.left.c F.left.d p := by
      simp only [orient]
      ring
    have h₀ := mul_neg_of_neg_of_pos (neg_neg_of_pos hp'.2.2) hq.2.1
    have h₁ := mul_neg_of_pos_of_neg hq'.1 hp.2.2
    by_contra! hn
    have h₂ := mul_nonneg_of_nonpos_of_nonpos F.left.bcd.le hn
    linarith

/-- A line along a chain in the first spike leaves the entire neighboring
spike on one weak side. General position will exclude equality. -/
theorem AdjacentCapFrames.ordered_pair_right (F : AdjacentCapFrames)
    (p q : F.left.spike) (r : F.right.spike) (hpq : F.left.toOuter p ≤ F.left.toOuter q) :
    0 ≤ orient p.val q.val r.val := by
  have hcross := F.cross_orientation p.property r.property
  have hmem := (AboveBase.le_iff _ _).mp hpq
  have hh : q.val ∈ {x : Point | 0 ≤ orient r.val p.val x} := by
    apply convexHull_min (s := ({F.left.a, F.left.d, p.val} : Set Point)) ?_
      (convex_orient_nonnegative r.val p.val) hmem
    intro x hx
    change 0 ≤ orient r.val p.val x
    rcases hx with rfl | rfl | rfl
    · simpa only [orient_cycle r.val p.val F.left.a] using hcross.1.le
    · simpa only [orient_cycle r.val p.val F.left.d] using hcross.2.le
    · simp [orient, mul_comm]
  change 0 ≤ orient r.val p.val q.val at hh
  simpa only [orient_cycle r.val p.val q.val] using hh

/-- The symmetric cross-spike inequalities, proved directly from the five
anchors rather than assuming a reflected coordinate system. -/
theorem AdjacentCapFrames.cross_orientation_left (F : AdjacentCapFrames) {p q : Point}
    (hp : p ∈ F.left.spike) (hq : q ∈ F.right.spike) :
    orient q F.left.b p < 0 ∧ orient q F.e p < 0 := by
  have hp' := F.left.spike_orientations hp
  have hq' := F.right.spike_orientations hq
  change orient F.left.b F.left.c q < 0 ∧ 0 < orient F.left.c F.left.d q ∧
    orient F.left.d F.e q < 0 at hq
  change 0 < orient F.left.b F.left.d q ∧ 0 < orient F.left.b F.e q ∧
    0 < orient F.left.c F.e q at hq'
  have e₀ : orient F.left.b F.left.c F.left.d * orient F.left.c F.e p =
      orient F.left.b F.left.c F.e * orient F.left.c F.left.d p -
        orient F.left.b F.left.c p * orient F.left.c F.left.d F.e := by
    simp only [orient]
    ring
  have e₁ : orient F.left.b F.left.c F.left.d * orient F.left.d F.e p =
      orient F.left.b F.left.d F.e * orient F.left.c F.left.d p -
        orient F.left.b F.left.d p * orient F.left.c F.left.d F.e := by
    simp only [orient]
    ring
  have hcep : orient F.left.c F.e p < 0 := by
    have h₀ := mul_pos_of_neg_of_neg F.bce hp.2.2
    have h₁ := mul_neg_of_pos_of_neg hp.2.1 F.cde
    by_contra! hn
    have h₂ := mul_nonpos_of_nonpos_of_nonneg F.left.bcd.le hn
    linarith
  have hdep : orient F.left.d F.e p < 0 := by
    have h₀ := mul_pos_of_neg_of_neg F.bde hp.2.2
    have h₁ := mul_neg_of_pos_of_neg hp'.2.2 F.cde
    by_contra! hn
    have h₂ := mul_nonpos_of_nonpos_of_nonneg F.left.bcd.le hn
    linarith
  constructor
  · have he : orient F.left.b F.left.c F.left.d * orient q F.left.b p =
        orient F.left.b F.left.c p * orient F.left.b F.left.d q -
          orient F.left.b F.left.d p * orient F.left.b F.left.c q := by
      simp only [orient]
      ring
    have h₀ := mul_pos hp.2.1 hq'.1
    have h₁ := mul_neg_of_pos_of_neg hp'.2.2 hq.1
    by_contra! hn
    have h₂ := mul_nonpos_of_nonpos_of_nonneg F.left.bcd.le hn
    linarith
  · have he : orient F.left.c F.left.d F.e * orient q F.e p =
        -orient F.left.c F.e q * orient F.left.d F.e p +
          orient F.left.c F.e p * orient F.left.d F.e q := by
      simp only [orient]
      ring
    have h₀ := mul_pos_of_neg_of_neg (neg_neg_of_pos hq'.2.2) hdep
    have h₁ := mul_pos_of_neg_of_neg hcep hq.2.2
    by_contra! hn
    have h₂ := mul_nonpos_of_nonpos_of_nonneg F.cde.le hn
    linarith

theorem AdjacentCapFrames.ordered_pair_left (F : AdjacentCapFrames)
    (p q : F.right.spike) (r : F.left.spike) (hpq : F.right.toOuter p ≤ F.right.toOuter q) :
    orient p.val q.val r.val ≤ 0 := by
  have hcross := F.cross_orientation_left r.property p.property
  have hmem := (AboveBase.le_iff _ _).mp hpq
  have hh : q.val ∈ {x : Point | 0 ≤ orient p.val r.val x} := by
    apply convexHull_min (s := ({F.left.b, F.e, p.val} : Set Point)) ?_
      (convex_orient_nonnegative p.val r.val) hmem
    intro x hx
    change 0 ≤ orient p.val r.val x
    rcases hx with rfl | rfl | rfl
    · rw [orient_swap p.val F.left.b r.val]
      exact neg_nonneg.mpr hcross.1.le
    · rw [orient_swap p.val F.e r.val]
      exact neg_nonneg.mpr hcross.2.le
    · simp [orient]
  change 0 ≤ orient p.val r.val q.val at hh
  rw [orient_swap p.val q.val r.val] at hh
  exact neg_nonneg.mp hh

end ErdosSzekeres.Suk
