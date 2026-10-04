import ErdosSzekeres.Suk.TriangleMembership

namespace ErdosSzekeres.Suk

/-- Four consecutive vertices of a clockwise convex polygon. No choice of
horizontal axis is needed for the local support-spike geometry. -/
structure CapFrame where
  a : Point
  b : Point
  c : Point
  d : Point
  abc : orient a b c < 0
  abd : orient a b d < 0
  acd : orient a c d < 0
  bcd : orient b c d < 0

@[ext] theorem CapFrame.ext {F G : CapFrame}
    (ha : F.a = G.a) (hb : F.b = G.b) (hc : F.c = G.c) (hd : F.d = G.d) : F = G := by
  cases F
  cases G
  cases ha
  cases hb
  cases hc
  cases hd
  rfl

/-- Outside the middle edge, inside the two neighboring supporting lines. -/
def CapFrame.spike (F : CapFrame) : Set Point :=
  {p | orient F.a F.b p < 0 ∧ 0 < orient F.b F.c p ∧ orient F.c F.d p < 0}

/-- The three remaining signs for inserting p between b and c in the polygon.
These follow from determinant identities; they are not extra spike axioms. -/
theorem CapFrame.spike_orientations (F : CapFrame) {p : Point} (hp : p ∈ F.spike) :
    0 < orient F.a F.c p ∧ 0 < orient F.a F.d p ∧ 0 < orient F.b F.d p := by
  obtain ⟨habp, hbcp, hcdp⟩ := hp
  have e₀ : orient F.a F.b F.c * orient F.b F.d p =
      orient F.a F.b F.d * orient F.b F.c p - orient F.a F.b p * orient F.b F.c F.d := by
    simp only [orient]
    ring
  have e₁ : orient F.b F.c F.d * orient F.a F.c p =
      -orient F.a F.b F.c * orient F.c F.d p + orient F.b F.c p * orient F.a F.c F.d := by
    simp only [orient]
    ring
  have e₂ : orient F.a F.b F.c * orient F.a F.d p =
      orient F.a F.b F.d * orient F.a F.c p - orient F.a F.b p * orient F.a F.c F.d := by
    simp only [orient]
    ring
  have hbd : 0 < orient F.b F.d p := by
    have h₀ := mul_neg_of_neg_of_pos F.abd hbcp
    have h₁ := mul_pos_of_neg_of_neg habp F.bcd
    by_contra! hn
    have h₂ := mul_nonneg_of_nonpos_of_nonpos F.abc.le hn
    linarith
  have hac : 0 < orient F.a F.c p := by
    have h₀ := mul_neg_of_pos_of_neg (neg_pos.mpr F.abc) hcdp
    have h₁ := mul_neg_of_pos_of_neg hbcp F.acd
    by_contra! hn
    have h₂ := mul_nonneg_of_nonpos_of_nonpos F.bcd.le hn
    linarith
  have had : 0 < orient F.a F.d p := by
    have h₀ := mul_neg_of_neg_of_pos F.abd hac
    have h₁ := mul_pos_of_neg_of_neg habp F.acd
    by_contra! hn
    have h₂ := mul_nonneg_of_nonpos_of_nonpos F.abc.le hn
    linarith
  exact ⟨hac, had, hbd⟩

def CapFrame.outerBase (F : CapFrame) : BaseSegment :=
  ⟨F.a, F.d, by intro h; have hn := F.abd; rw [h] at hn; simp [orient] at hn⟩

def CapFrame.edgeBase (F : CapFrame) : BaseSegment :=
  ⟨F.b, F.c, by
    intro h
    have hn := F.abc
    rw [h] at hn
    have he : orient F.a F.c F.c = 0 := by simp only [orient]; ring
    linarith⟩

def CapFrame.toOuter (F : CapFrame) (p : F.spike) : AboveBase F.outerBase :=
  ⟨p.val, (F.spike_orientations p.property).2.1⟩

def CapFrame.toEdge (F : CapFrame) (p : F.spike) : AboveBase F.edgeBase :=
  ⟨p.val, p.property.2.1⟩

/-- Inside a spike, the triangle on the outer base narrows to the triangle
on the middle edge. This links Suk's order to his edge-anchor caps. -/
theorem CapFrame.outer_triangle_imp_edge_triangle (F : CapFrame) {p q : Point}
    (hp : p ∈ F.spike) (hq : q ∈ F.spike)
    (hqp : q ∈ convexHull ℝ ({F.a, F.d, p} : Set Point)) :
    q ∈ convexHull ℝ ({F.b, F.c, p} : Set Point) := by
  have hp' := F.spike_orientations hp
  rw [mem_triangle_iff_of_orient_pos F.b F.c p q hp.2.1]
  refine ⟨hq.2.1.le, ?_, ?_⟩
  · apply convexHull_min (t := {r : Point | 0 ≤ orient F.c p r}) ?_
      (convex_orient_nonnegative F.c p) hqp
    intro r hr
    change 0 ≤ orient F.c p r
    rcases hr with rfl | rfl | rfl
    · simpa only [orient_cycle F.a F.c p] using hp'.1.le
    · rw [orient_swap F.c F.d p]
      exact neg_nonneg.mpr hp.2.2.le
    · simp [orient, mul_comm]
  · apply convexHull_min (t := {r : Point | 0 ≤ orient p F.b r}) ?_
      (convex_orient_nonnegative p F.b) hqp
    intro r hr
    change 0 ≤ orient p F.b r
    rcases hr with rfl | rfl | rfl
    · have he : orient p F.b F.a = -orient F.a F.b p := by simp only [orient]; ring
      rw [he]
      exact neg_nonneg.mpr hp.1.le
    · simpa only [orient_cycle p F.b F.d] using hp'.2.2.le
    · simp [orient, mul_comm]

theorem CapFrame.toEdge_le_of_toOuter_le (F : CapFrame) (p q : F.spike)
    (h : F.toOuter p ≤ F.toOuter q) : F.toEdge p ≤ F.toEdge q := by
  rw [AboveBase.le_iff] at h ⊢
  exact F.outer_triangle_imp_edge_triangle p.property q.property h

theorem CapFrame.toEdge_lt_of_toOuter_lt (F : CapFrame) (p q : F.spike)
    (h : F.toOuter p < F.toOuter q) : F.toEdge p < F.toEdge q := by
  refine lt_of_le_of_ne (F.toEdge_le_of_toOuter_le p q h.le) ?_
  intro he
  apply h.ne
  apply AboveBase.ext
  exact congrArg (fun z : AboveBase F.edgeBase => z.val) he

end ErdosSzekeres.Suk
