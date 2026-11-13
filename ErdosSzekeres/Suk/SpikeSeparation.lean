import ErdosSzekeres.Suk.SupportSequence

namespace ErdosSzekeres.Suk

/-- Extend the preceding support line to an earlier clockwise anchor. -/
theorem CapFrame.extend_left (F : CapFrame) {x p : Point}
    (hxab : orient x F.a F.b < 0) (hxbc : orient x F.b F.c < 0)
    (hp : p ∈ F.spike) : orient x F.b p < 0 := by
  have he : orient F.a F.b F.c * orient x F.b p =
      orient x F.b F.c * orient F.a F.b p - orient x F.a F.b * orient F.b F.c p := by
    simp only [orient]
    ring
  have h₀ := mul_pos_of_neg_of_neg hxbc hp.1
  have h₁ := mul_neg_of_neg_of_pos hxab hp.2.1
  by_contra! hn
  have h₂ := mul_nonpos_of_nonpos_of_nonneg F.abc.le hn
  linarith

/-- Extend the following support line to a later clockwise anchor. -/
theorem CapFrame.extend_right (F : CapFrame) {x p : Point}
    (hbcx : orient F.b F.c x < 0) (hcdx : orient F.c F.d x < 0)
    (hp : p ∈ F.spike) : orient F.c x p < 0 := by
  have he : orient F.b F.c F.d * orient F.c x p =
      orient F.b F.c x * orient F.c F.d p - orient F.b F.c p * orient F.c F.d x := by
    simp only [orient]
    ring
  have h₀ := mul_pos_of_neg_of_neg hbcx hp.2.2
  have h₁ := mul_neg_of_pos_of_neg hp.2.1 hcdx
  by_contra! hn
  have h₂ := mul_nonpos_of_nonpos_of_nonneg F.bcd.le hn
  linarith

theorem CapFrame.before_pair (F : CapFrame) {p : Point}
    (hbc : orient F.b F.c p < 0) (hbd : 0 < orient F.b F.d p) :
    orient F.a F.b p < 0 := by
  have he : orient F.a F.b F.c * orient F.b F.d p =
      orient F.a F.b F.d * orient F.b F.c p - orient F.a F.b p * orient F.b F.c F.d := by
    simp only [orient]
    ring
  have h₀ := mul_neg_of_neg_of_pos F.abc hbd
  have h₁ := mul_pos_of_neg_of_neg F.abd hbc
  by_contra! hn
  have h₂ := mul_nonpos_of_nonneg_of_nonpos hn F.bcd.le
  linarith

theorem CapFrame.after_pair (F : CapFrame) {p : Point}
    (hbc : orient F.b F.c p < 0) (hac : 0 < orient F.a F.c p) :
    orient F.c F.d p < 0 := by
  have he : orient F.a F.b F.c * orient F.c F.d p =
      orient F.a F.c F.d * orient F.b F.c p - orient F.a F.c p * orient F.b F.c F.d := by
    simp only [orient]
    ring
  have h₀ := mul_pos_of_neg_of_neg F.acd hbc
  have h₁ := mul_neg_of_pos_of_neg hac F.bcd
  by_contra! hn
  have h₂ := mul_nonpos_of_nonpos_of_nonneg F.abc.le hn
  linarith

/-- Any increasing quadruple from the support sequence forms a local frame. -/
def ClockwiseAnchors.frameOfIndices {m : ℕ} (A : ClockwiseAnchors m)
    (i j k l : Fin m) (hij : i < j) (hjk : j < k) (hkl : k < l) : CapFrame where
  a := A.point i
  b := A.point j
  c := A.point k
  d := A.point l
  abc := A.clockwise i j k hij hjk
  abd := A.clockwise i j l hij (hjk.trans hkl)
  acd := A.clockwise i k l (hij.trans hjk) hkl
  bcd := A.clockwise j k l hjk hkl

theorem ClockwiseAnchors.spike_left_boundary {r : ℕ} (A : ClockwiseAnchors (r + 3))
    (i : Fin r) {p : Point} (hp : p ∈ (A.frame i).spike)
    (x : Fin (r + 3)) (hx : x.val < i.val + 1) :
    orient (A.point x) (A.frame i).b p < 0 := by
  by_cases he : x.val = i.val
  · have hx' : x = ⟨i.val, by omega⟩ := Fin.ext he
    rw [hx']
    exact hp.1
  · apply (A.frame i).extend_left (p := p) _ _ hp
    · exact A.clockwise _ _ _ (by change x.val < i.val; omega)
        (by change i.val < i.val + 1; omega)
    · exact A.clockwise _ _ _ (by change x.val < i.val + 1; omega)
        (by change i.val + 1 < i.val + 2; omega)

theorem ClockwiseAnchors.spike_right_boundary {r : ℕ} (A : ClockwiseAnchors (r + 3))
    (i : Fin r) {p : Point} (hp : p ∈ (A.frame i).spike)
    (x : Fin (r + 3)) (hx : i.val + 2 < x.val) :
    orient (A.frame i).c (A.point x) p < 0 := by
  by_cases he : x.val = i.val + 3
  · have hx' : x = ⟨i.val + 3, by omega⟩ := Fin.ext he
    rw [hx']
    exact hp.2.2
  · apply (A.frame i).extend_right (p := p) _ _ hp
    · exact A.clockwise _ _ _ (by change i.val + 1 < i.val + 2; omega)
        (by change i.val + 2 < x.val; omega)
    · exact A.clockwise _ _ _ (by change i.val + 2 < i.val + 3; omega)
        (by change i.val + 3 < x.val; omega)

/-- A point in a later spike is below every pair-line of preceding anchors. -/
theorem ClockwiseAnchors.spike_after_pair {r : ℕ} (A : ClockwiseAnchors (r + 3))
    (i : Fin r) {p : Point} (hp : p ∈ (A.frame i).spike)
    (x y : Fin (r + 3)) (hxy : x < y) (hy : y.val ≤ i.val + 1) :
    orient (A.point x) (A.point y) p < 0 := by
  by_cases he : y.val = i.val + 1
  · have hy' : y = ⟨i.val + 1, by omega⟩ := Fin.ext he
    rw [hy']
    exact A.spike_left_boundary i hp x (by change x.val < y.val at hxy; omega)
  · let b : Fin (r + 3) := ⟨i.val + 1, by omega⟩
    let c : Fin (r + 3) := ⟨i.val + 2, by omega⟩
    let d : Fin (r + 3) := ⟨i.val + 3, by omega⟩
    have hyb : y < b := by change y.val < i.val + 1; omega
    have hbc : b < c := by change i.val + 1 < i.val + 2; omega
    have hcd : c < d := by change i.val + 2 < i.val + 3; omega
    let G := A.frameOfIndices y b c d hyb hbc hcd
    have hgp : p ∈ G.spike :=
      ⟨A.spike_left_boundary i hp y hyb, hp.2.1, hp.2.2⟩
    exact (A.frameOfIndices x y b c hxy hyb hbc).before_pair
      hgp.1 (G.spike_orientations hgp).1

/-- A point in an earlier spike is below every pair-line of following anchors. -/
theorem ClockwiseAnchors.spike_before_pair {r : ℕ} (A : ClockwiseAnchors (r + 3))
    (i : Fin r) {p : Point} (hp : p ∈ (A.frame i).spike)
    (x y : Fin (r + 3)) (hxy : x < y) (hx : i.val + 2 ≤ x.val) :
    orient (A.point x) (A.point y) p < 0 := by
  by_cases he : x.val = i.val + 2
  · have hx' : x = ⟨i.val + 2, by omega⟩ := Fin.ext he
    rw [hx']
    exact A.spike_right_boundary i hp y (by change x.val < y.val at hxy; omega)
  · let a : Fin (r + 3) := ⟨i.val, by omega⟩
    let b : Fin (r + 3) := ⟨i.val + 1, by omega⟩
    let c : Fin (r + 3) := ⟨i.val + 2, by omega⟩
    have hab : a < b := by change i.val < i.val + 1; omega
    have hbc : b < c := by change i.val + 1 < i.val + 2; omega
    have hcx : c < x := by change i.val + 2 < x.val; omega
    let G := A.frameOfIndices a b c x hab hbc hcx
    have hgp : p ∈ G.spike :=
      ⟨hp.1, hp.2.1, A.spike_right_boundary i hp x hcx⟩
    exact (A.frameOfIndices b c x y hbc hcx hxy).after_pair
      hgp.2.2 (G.spike_orientations hgp).2.2

/-- A point inside these four supporting halfplanes lies strictly between
the two rays from a spike point to its outer-base endpoints. -/
theorem CapFrame.base_cone_of_pair_lines (F : CapFrame) {p q : Point}
    (hp : p ∈ F.spike)
    (hq : orient F.a F.b q < 0 ∧ orient F.a F.c q < 0 ∧
      orient F.b F.d q < 0 ∧ orient F.c F.d q < 0) :
    0 < orient p F.a q ∧ orient p F.d q < 0 := by
  have hp' := F.spike_orientations hp
  constructor
  · have he : orient F.a F.b F.c * orient p F.a q =
        -orient F.a F.b p * orient F.a F.c q +
          orient F.a F.b q * orient F.a F.c p := by
      simp only [orient]
      ring
    have h₀ := mul_neg_of_pos_of_neg (neg_pos.mpr hp.1) hq.2.1
    have h₁ := mul_neg_of_neg_of_pos hq.1 hp'.1
    by_contra! hn
    have h₂ := mul_nonneg_of_nonpos_of_nonpos F.abc.le hn
    linarith
  · have he : orient F.b F.c F.d * orient p F.d q =
        -orient F.b F.d p * orient F.c F.d q +
          orient F.b F.d q * orient F.c F.d p := by
      simp only [orient]
      ring
    have h₀ := mul_pos_of_neg_of_neg (neg_neg_of_pos hp'.2.2) hq.2.2.2
    have h₁ := mul_pos_of_neg_of_neg hq.2.2.1 hp.2.2
    by_contra! hn
    have h₂ := mul_nonpos_of_nonpos_of_nonneg F.bcd.le hn
    linarith

theorem ClockwiseAnchors.nonadjacent_spike_pair_lines {r : ℕ}
    (A : ClockwiseAnchors (r + 3)) (i j : Fin r)
    (hsep : i.val + 1 < j.val ∨ j.val + 1 < i.val)
    {p : Point} (hp : p ∈ (A.frame j).spike) :
    orient (A.frame i).a (A.frame i).b p < 0 ∧
      orient (A.frame i).a (A.frame i).c p < 0 ∧
      orient (A.frame i).b (A.frame i).d p < 0 ∧
      orient (A.frame i).c (A.frame i).d p < 0 := by
  rcases hsep with hsep | hsep
  · refine ⟨?_, ?_, ?_, ?_⟩
    all_goals
      apply A.spike_after_pair j hp <;> simp only [Fin.lt_def] <;> omega
  · refine ⟨?_, ?_, ?_, ?_⟩
    all_goals
      apply A.spike_before_pair j hp <;> simp only [Fin.lt_def] <;> omega

/-- The antichain separation step from Suk's Case 1. Every point of a
nonadjacent support spike lies on the same strict side of an incomparable
pair-line as the first outer-base endpoint. All region signs are derived
from the single clockwise support sequence. -/
theorem ClockwiseAnchors.incomparable_pair_nonadjacent_same_side {r : ℕ}
    (A : ClockwiseAnchors (r + 3)) (i j : Fin r)
    (hsep : i.val + 1 < j.val ∨ j.val + 1 < i.val)
    (p q : (A.frame i).spike) (z : (A.frame j).spike)
    (hpq : ¬ (A.frame i).toOuter p ≤ (A.frame i).toOuter q)
    (hqp : ¬ (A.frame i).toOuter q ≤ (A.frame i).toOuter p) :
    0 < orient p.val q.val (A.frame i).a * orient p.val q.val z.val := by
  let F := A.frame i
  have hbase := (F.toOuter p).incomparable_same_side (F.toOuter q) hpq hqp
  change 0 < orient p.val q.val F.a * orient p.val q.val F.d at hbase
  have hcone := F.base_cone_of_pair_lines p.property
    (A.nonadjacent_spike_pair_lines i j hsep z.property)
  have hD : 0 < orient p.val F.a F.d := by
    simpa only [orient_cycle p.val F.a F.d] using
      (F.spike_orientations p.property).2.1
  have he : orient p.val F.a F.d *
        (orient p.val q.val F.a * orient p.val q.val z.val) =
      orient p.val F.a z.val * (orient p.val q.val F.a * orient p.val q.val F.d) -
        orient p.val F.d z.val * (orient p.val q.val F.a) ^ 2 := by
    simp only [orient]
    ring
  have h₀ := mul_pos hcone.1 hbase
  have h₁ := mul_nonpos_of_nonpos_of_nonneg hcone.2.le (sq_nonneg (orient p.val q.val F.a))
  by_contra! hn
  have h₂ := mul_nonpos_of_nonneg_of_nonpos hD.le hn
  linarith only [he, h₀, h₁, h₂]

/-- In particular, no line through an incomparable pair meets another
nonadjacent spike. -/
theorem ClockwiseAnchors.incomparable_pair_nonadjacent_not_collinear {r : ℕ}
    (A : ClockwiseAnchors (r + 3)) (i j : Fin r)
    (hsep : i.val + 1 < j.val ∨ j.val + 1 < i.val)
    (p q : (A.frame i).spike) (z : (A.frame j).spike)
    (hpq : ¬ (A.frame i).toOuter p ≤ (A.frame i).toOuter q)
    (hqp : ¬ (A.frame i).toOuter q ≤ (A.frame i).toOuter p) :
    ¬ Collinear ℝ ({p.val, q.val, z.val} : Set Point) := by
  rw [← orient_eq_zero_iff_collinear]
  exact right_ne_zero_of_mul (ne_of_gt
    (A.incomparable_pair_nonadjacent_same_side i j hsep p q z hpq hqp))

theorem ClockwiseAnchors.nonadjacent_spikes_disjoint {r : ℕ}
    (A : ClockwiseAnchors (r + 3)) (i j : Fin r)
    (hsep : i.val + 1 < j.val ∨ j.val + 1 < i.val) :
    Disjoint (A.frame i).spike (A.frame j).spike := by
  apply Set.disjoint_left.mpr
  intro p hi hj
  have hpos := hi.2.1
  have hneg : orient (A.frame i).b (A.frame i).c p < 0 := by
    rcases hsep with hsep | hsep
    · apply A.spike_after_pair j hj <;> simp only [Fin.lt_def] <;> omega
    · apply A.spike_before_pair j hj <;> simp only [Fin.lt_def] <;> omega
  linarith only [hpos, hneg]

end ErdosSzekeres.Suk
