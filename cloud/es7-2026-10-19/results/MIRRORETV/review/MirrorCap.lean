import Mathlib

/-!
# Mirror cap lemma: independent formal check (THEORY.md Lemma 3.1, note_patch.tex `lem:mirror`)

A cap `c_0, …, c_{m-1}` (strictly increasing abscissae `x`, and `orient (c_i, c_{i+1}, c_{i+2}) < 0`, i.e. every
interior point strictly above the chord of its neighbours), with interior heights `> 0` and end heights `≥ 0`
(and `y 0 > 0` if `m = 1`), together with its mirror image in the x-axis, is in convex position: no point of
`V = {c_i} ∪ {μ c_i}` lies in the convex hull of the other points of `V`.

Proof method (different from THEORY.md's region argument): every point of `V` is exposed by an explicit linear
functional; an open half-plane is convex, so the convex hull of the other points misses the point.
We also prove the coincidence pattern behind the count `|V| = 2m - #(endpoints on the axis)`.
-/

namespace MirrorCap

/-- twice the signed area of the triangle `p q r` -/
def orient (p q r : ℝ × ℝ) : ℝ := (q.1 - p.1) * (r.2 - p.2) - (q.2 - p.2) * (r.1 - p.1)

/-- slope of the edge from `c_i` to `c_{i+1}` -/
noncomputable def sl (x y : ℕ → ℝ) (i : ℕ) : ℝ := (y (i + 1) - y i) / (x (i + 1) - x i)

/-- the point set `{c_i : i < m} ∪ {μ c_i : i < m}` with `c_i = (x i, y i)`, `μ (a, b) = (a, -b)` -/
def V (x y : ℕ → ℝ) (m : ℕ) : Set (ℝ × ℝ) :=
  {p | ∃ i < m, p = (x i, y i)} ∪ {p | ∃ i < m, p = (x i, -y i)}

section
variable {x y : ℕ → ℝ} {m : ℕ}

lemma edge_eq {i : ℕ} (h : x i < x (i + 1)) :
    y (i + 1) = y i + sl x y i * (x (i + 1) - x i) := by
  unfold sl
  have hne : x (i + 1) - x i ≠ 0 := by linarith
  rw [div_mul_cancel₀ _ hne]
  ring

lemma orient_eq_slopes (xa ya xb yb xc yc : ℝ) (h1 : xa < xb) (h2 : xb < xc) :
    orient (xa, ya) (xb, yb) (xc, yc)
      = (xb - xa) * (xc - xb) * ((yc - yb) / (xc - xb) - (yb - ya) / (xb - xa)) := by
  unfold orient
  have ha : xb - xa ≠ 0 := by linarith
  have hb : xc - xb ≠ 0 := by linarith
  field_simp
  ring

/-- the cap condition `orient < 0` means that consecutive slopes strictly decrease -/
lemma slope_dec_of_orient (hx : ∀ i, i + 1 < m → x i < x (i + 1))
    (hcap : ∀ i, i + 2 < m → orient (x i, y i) (x (i + 1), y (i + 1)) (x (i + 2), y (i + 2)) < 0) :
    ∀ i, i + 2 < m → sl x y (i + 1) < sl x y i := by
  intro i hi
  have h1 : x i < x (i + 1) := hx i (by omega)
  have h2 : x (i + 1) < x (i + 2) := hx (i + 1) (by omega)
  have ho := hcap i hi
  rw [orient_eq_slopes _ _ _ _ _ _ h1 h2] at ho
  have hpos : 0 < (x (i + 1) - x i) * (x (i + 2) - x (i + 1)) := by
    apply mul_pos <;> linarith
  have key : (y (i + 2) - y (i + 1)) / (x (i + 2) - x (i + 1)) < (y (i + 1) - y i) / (x (i + 1) - x i) := by
    by_contra hcon
    push_neg at hcon
    have : 0 ≤ (x (i + 1) - x i) * (x (i + 2) - x (i + 1)) *
        ((y (i + 2) - y (i + 1)) / (x (i + 2) - x (i + 1)) - (y (i + 1) - y i) / (x (i + 1) - x i)) :=
      mul_nonneg hpos.le (by linarith)
    linarith
  show (y (i + 1 + 1) - y (i + 1)) / (x (i + 1 + 1) - x (i + 1)) < (y (i + 1) - y i) / (x (i + 1) - x i)
  exact key

lemma sl_anti (hdec : ∀ i, i + 2 < m → sl x y (i + 1) < sl x y i) :
    ∀ j k, j < k → k + 1 < m → sl x y k < sl x y j := by
  intro j k hjk hk
  induction k with
  | zero => omega
  | succ k ih =>
    rcases Nat.lt_succ_iff_lt_or_eq.mp hjk with h | h
    · exact lt_trans (hdec k (by omega)) (ih h (by omega))
    · rw [← h]; exact hdec j (by omega)

lemma x_mono (hx : ∀ i, i + 1 < m → x i < x (i + 1)) :
    ∀ j k, j < k → k < m → x j < x k := by
  intro j k hjk hk
  induction k with
  | zero => omega
  | succ k ih =>
    rcases Nat.lt_succ_iff_lt_or_eq.mp hjk with h | h
    · exact lt_trans (ih h (by omega)) (hx k (by omega))
    · rw [← h]; exact hx j (by omega)

/-- points to the right of `c_j` lie on or below the line through `c_j` with the slope of the edge leaving `c_j` -/
lemma chord_right (hx : ∀ i, i + 1 < m → x i < x (i + 1))
    (hdec : ∀ i, i + 2 < m → sl x y (i + 1) < sl x y i) (j : ℕ) :
    ∀ k, j < k → k < m → y k ≤ y j + sl x y j * (x k - x j) := by
  intro k hjk hk
  induction k with
  | zero => omega
  | succ k ih =>
    rcases Nat.lt_succ_iff_lt_or_eq.mp hjk with h | h
    · have e := edge_eq (y := y) (hx k (by omega))
      have ihk := ih h (by omega)
      have hs : sl x y k < sl x y j := sl_anti hdec j k h (by omega)
      have hxk : x k < x (k + 1) := hx k (by omega)
      have hm : sl x y k * (x (k + 1) - x k) ≤ sl x y j * (x (k + 1) - x k) :=
        mul_le_mul_of_nonneg_right hs.le (by linarith)
      rw [e]
      linarith
    · rw [← h]
      exact (edge_eq (y := y) (hx j (by omega))).le

/-- points to the left of `c_{i+1}` lie on or below the line through `c_{i+1}` with the slope of the edge
entering `c_{i+1}` -/
lemma chord_left (hx : ∀ i, i + 1 < m → x i < x (i + 1))
    (hdec : ∀ i, i + 2 < m → sl x y (i + 1) < sl x y i) (i : ℕ) (hi : i + 1 < m) :
    ∀ n k, k + n = i → y k ≤ y (i + 1) + sl x y i * (x k - x (i + 1)) := by
  intro n
  induction n with
  | zero =>
    intro k hk
    have hk' : k = i := by omega
    rw [hk']
    have e := edge_eq (y := y) (hx i hi)
    linarith
  | succ n ih =>
    intro k hk
    have ih1 := ih (k + 1) (by omega)
    have e := edge_eq (y := y) (hx k (by omega))
    have hs : sl x y i < sl x y k := sl_anti hdec k i (by omega) hi
    have hxk : x k < x (k + 1) := hx k (by omega)
    have hm : sl x y i * (x (k + 1) - x k) ≤ sl x y k * (x (k + 1) - x k) :=
      mul_le_mul_of_nonneg_right hs.le (by linarith)
    linarith

lemma y_nonneg (hint : ∀ i, 0 < i → i + 1 < m → 0 < y i) (h0 : 0 ≤ y 0) (hlast : 0 ≤ y (m - 1)) :
    ∀ k, k < m → 0 ≤ y k := by
  intro k hk
  rcases Nat.eq_zero_or_pos k with h | h
  · rw [h]; exact h0
  · by_cases hk' : k + 1 < m
    · exact (hint k h hk').le
    · have : k = m - 1 := by omega
      rw [this]; exact hlast

/-- every point `c_i` of the cap is exposed by a linear functional `w ↦ a * w.1 + b * w.2` -/
theorem exposed_c (hx : ∀ i, i + 1 < m → x i < x (i + 1))
    (hdec : ∀ i, i + 2 < m → sl x y (i + 1) < sl x y i)
    (hint : ∀ i, 0 < i → i + 1 < m → 0 < y i) (h0 : 0 ≤ y 0) (hlast : 0 ≤ y (m - 1))
    (hone : m = 1 → 0 < y 0) (i : ℕ) (hi : i < m) :
    ∃ a b : ℝ, ∀ w ∈ V x y m, w ≠ (x i, y i) → a * w.1 + b * w.2 < a * x i + b * y i := by
  have ynn := y_nonneg hint h0 hlast
  rcases Nat.eq_zero_or_pos i with hzero | hpos
  · -- i = 0
    subst hzero
    by_cases hm1 : m = 1
    · -- a single point above the axis
      have hy0 := hone hm1
      refine ⟨0, 1, ?_⟩
      intro w hw hne
      rcases hw with ⟨k, hk, rfl⟩ | ⟨k, hk, rfl⟩
      · exact absurd (by rw [show k = 0 by omega]) hne
      · have hk0 : k = 0 := by omega
        rw [hk0]
        show 0 * x 0 + 1 * -y 0 < 0 * x 0 + 1 * y 0
        linarith
    · -- left endpoint of a cap with at least two points
      set t := max (sl x y 0) 0 + 1 with ht
      have ht1 : sl x y 0 < t := by
        have := le_max_left (sl x y 0) 0; linarith
      have ht0 : 0 < t := by
        have := le_max_right (sl x y 0) 0; linarith
      refine ⟨-t, 1, ?_⟩
      intro w hw hne
      rcases hw with ⟨k, hk, rfl⟩ | ⟨k, hk, rfl⟩
      · have hk0 : k ≠ 0 := by
          intro h; apply hne; rw [h]
        have hpk : 0 < k := Nat.pos_of_ne_zero hk0
        have hc := chord_right hx hdec 0 k hpk hk
        have hxk : x 0 < x k := x_mono hx 0 k hpk hk
        have hmul : sl x y 0 * (x k - x 0) < t * (x k - x 0) :=
          mul_lt_mul_of_pos_right ht1 (by linarith)
        show -t * x k + 1 * y k < -t * x 0 + 1 * y 0
        linarith
      · by_cases hk0 : k = 0
        · rw [hk0] at hne ⊢
          have hy0 : y 0 ≠ 0 := by
            intro h; apply hne; rw [h, neg_zero]
          have hy0' : 0 < y 0 := lt_of_le_of_ne h0 (Ne.symm hy0)
          show -t * x 0 + 1 * -y 0 < -t * x 0 + 1 * y 0
          linarith
        · have hpk : 0 < k := Nat.pos_of_ne_zero hk0
          have hxk : x 0 < x k := x_mono hx 0 k hpk hk
          have hyk := ynn k hk
          have hmul : 0 < t * (x k - x 0) := mul_pos ht0 (by linarith)
          show -t * x k + 1 * -y k < -t * x 0 + 1 * y 0
          linarith
  · obtain ⟨p, rfl⟩ : ∃ p, i = p + 1 := ⟨i - 1, by omega⟩
    by_cases hin : p + 1 + 1 < m
    · -- interior point: slope strictly between the two edge slopes
      have hsd : sl x y (p + 1) < sl x y p := hdec p (by omega)
      set t := (sl x y p + sl x y (p + 1)) / 2 with ht
      have ht1 : sl x y (p + 1) < t := by rw [ht]; linarith
      have ht2 : t < sl x y p := by rw [ht]; linarith
      have hyi : 0 < y (p + 1) := hint (p + 1) hpos hin
      have keyc : ∀ k, k < m → k ≠ p + 1 → y k - t * x k < y (p + 1) - t * x (p + 1) := by
        intro k hk hne
        rcases Nat.lt_or_gt_of_ne hne with hlt | hgt
        · have hc := chord_left hx hdec p (by omega) (p - k) k (by omega)
          have hxk : x k < x (p + 1) := x_mono hx k (p + 1) hlt (by omega)
          have hmul : sl x y p * (x k - x (p + 1)) < t * (x k - x (p + 1)) :=
            mul_lt_mul_of_neg_right ht2 (by linarith)
          linarith
        · have hc := chord_right hx hdec (p + 1) k hgt hk
          have hxk : x (p + 1) < x k := x_mono hx (p + 1) k hgt hk
          have hmul : sl x y (p + 1) * (x k - x (p + 1)) < t * (x k - x (p + 1)) :=
            mul_lt_mul_of_pos_right ht1 (by linarith)
          linarith
      refine ⟨-t, 1, ?_⟩
      intro w hw hne
      rcases hw with ⟨k, hk, rfl⟩ | ⟨k, hk, rfl⟩
      · have hkne : k ≠ p + 1 := by
          intro h; apply hne; rw [h]
        have := keyc k hk hkne
        show -t * x k + 1 * y k < -t * x (p + 1) + 1 * y (p + 1)
        linarith
      · show -t * x k + 1 * -y k < -t * x (p + 1) + 1 * y (p + 1)
        by_cases hkk : k = p + 1
        · rw [hkk]; linarith
        · have h1 := keyc k hk hkk
          have h2 := ynn k hk
          linarith
    · -- right endpoint: i = p + 1 = m - 1, m ≥ 2
      have hmp : m = p + 2 := by omega
      set t := min (sl x y p) 0 - 1 with ht
      have ht2 : t < sl x y p := by
        have := min_le_left (sl x y p) 0; linarith
      have ht0 : t < 0 := by
        have := min_le_right (sl x y p) 0; linarith
      have hlast' : 0 ≤ y (p + 1) := by
        have : p + 1 = m - 1 := by omega
        rw [this]; exact hlast
      refine ⟨-t, 1, ?_⟩
      intro w hw hne
      rcases hw with ⟨k, hk, rfl⟩ | ⟨k, hk, rfl⟩
      · have hkne : k ≠ p + 1 := by
          intro h; apply hne; rw [h]
        have hlt : k < p + 1 := by omega
        have hc := chord_left hx hdec p (by omega) (p - k) k (by omega)
        have hxk : x k < x (p + 1) := x_mono hx k (p + 1) hlt (by omega)
        have hmul : sl x y p * (x k - x (p + 1)) < t * (x k - x (p + 1)) :=
          mul_lt_mul_of_neg_right ht2 (by linarith)
        show -t * x k + 1 * y k < -t * x (p + 1) + 1 * y (p + 1)
        linarith
      · show -t * x k + 1 * -y k < -t * x (p + 1) + 1 * y (p + 1)
        by_cases hkk : k = p + 1
        · rw [hkk] at hne ⊢
          have hy : y (p + 1) ≠ 0 := by
            intro h; apply hne; rw [h, neg_zero]
          have hy' : 0 < y (p + 1) := lt_of_le_of_ne hlast' (Ne.symm hy)
          linarith
        · have hlt : k < p + 1 := by omega
          have hxk : x k < x (p + 1) := x_mono hx k (p + 1) hlt (by omega)
          have hyk := ynn k hk
          have hmul : 0 < t * (x k - x (p + 1)) := mul_pos_of_neg_of_neg ht0 (by linarith)
          linarith

/-- every mirrored point `μ c_i` is exposed as well (apply the functional of `c_i` after reflecting) -/
theorem exposed_mu (hx : ∀ i, i + 1 < m → x i < x (i + 1))
    (hdec : ∀ i, i + 2 < m → sl x y (i + 1) < sl x y i)
    (hint : ∀ i, 0 < i → i + 1 < m → 0 < y i) (h0 : 0 ≤ y 0) (hlast : 0 ≤ y (m - 1))
    (hone : m = 1 → 0 < y 0) (i : ℕ) (hi : i < m) :
    ∃ a b : ℝ, ∀ w ∈ V x y m, w ≠ (x i, -y i) → a * w.1 + b * w.2 < a * x i + b * (-y i) := by
  obtain ⟨a, b, h⟩ := exposed_c hx hdec hint h0 hlast hone i hi
  refine ⟨a, -b, ?_⟩
  intro w hw hne
  have hw' : (w.1, -w.2) ∈ V x y m := by
    rcases hw with ⟨k, hk, rfl⟩ | ⟨k, hk, rfl⟩
    · right; exact ⟨k, hk, rfl⟩
    · left; exact ⟨k, hk, by simp⟩
  have hne' : (w.1, -w.2) ≠ (x i, y i) := by
    intro heq
    apply hne
    have h1 : w.1 = x i := congrArg Prod.fst heq
    have h2 : -w.2 = y i := congrArg Prod.snd heq
    refine Prod.ext h1 ?_
    show w.2 = -y i
    linarith
  have hh := h _ hw' hne'
  have e1 : a * (w.1, -w.2).1 + b * (w.1, -w.2).2 = a * w.1 + -b * w.2 := by
    show a * w.1 + b * -w.2 = a * w.1 + -b * w.2
    ring
  rw [e1] at hh
  linarith

/-- **Mirror cap lemma.** No point of `V` lies in the convex hull of the other points of `V`. -/
theorem convex_position (hx : ∀ i, i + 1 < m → x i < x (i + 1))
    (hcap : ∀ i, i + 2 < m → orient (x i, y i) (x (i + 1), y (i + 1)) (x (i + 2), y (i + 2)) < 0)
    (hint : ∀ i, 0 < i → i + 1 < m → 0 < y i) (h0 : 0 ≤ y 0) (hlast : 0 ≤ y (m - 1))
    (hone : m = 1 → 0 < y 0) :
    ∀ v ∈ V x y m, v ∉ convexHull ℝ (V x y m \ {v}) := by
  have hdec := slope_dec_of_orient hx hcap
  intro v hv hmem
  have hexp : ∃ a b : ℝ, ∀ w ∈ V x y m, w ≠ v → a * w.1 + b * w.2 < a * v.1 + b * v.2 := by
    rcases hv with ⟨i, hi, rfl⟩ | ⟨i, hi, rfl⟩
    · exact exposed_c hx hdec hint h0 hlast hone i hi
    · exact exposed_mu hx hdec hint h0 hlast hone i hi
  obtain ⟨a, b, hab⟩ := hexp
  have hlin : IsLinearMap ℝ (fun w : ℝ × ℝ => a * w.1 + b * w.2) := by
    refine ⟨fun u w => ?_, fun c u => ?_⟩
    · simp only [Prod.fst_add, Prod.snd_add]; ring
    · simp only [Prod.smul_fst, Prod.smul_snd, smul_eq_mul]; ring
  have hconv := convex_halfSpace_lt hlin (a * v.1 + b * v.2)
  have hsub : V x y m \ {v} ⊆ {w | a * w.1 + b * w.2 < a * v.1 + b * v.2} := by
    intro w hw
    exact hab w hw.1 hw.2
  have hin : a * v.1 + b * v.2 < a * v.1 + b * v.2 := convexHull_min hsub hconv hmem
  exact lt_irrefl _ hin

/-- The same conclusion in Mathlib's vocabulary: `V` is a convex independent set. -/
theorem convexIndependent (hx : ∀ i, i + 1 < m → x i < x (i + 1))
    (hcap : ∀ i, i + 2 < m → orient (x i, y i) (x (i + 1), y (i + 1)) (x (i + 2), y (i + 2)) < 0)
    (hint : ∀ i, 0 < i → i + 1 < m → 0 < y i) (h0 : 0 ≤ y 0) (hlast : 0 ≤ y (m - 1))
    (hone : m = 1 → 0 < y 0) :
    ConvexIndependent ℝ (Subtype.val : V x y m → ℝ × ℝ) :=
  convexIndependent_set_iff_notMem_convexHull_diff.mpr
    (convex_position hx hcap hint h0 hlast hone)

/-- Coincidences among the `2m` listed points (this gives `|V| = 2m - #(endpoints on the axis)`):
the `c_i` are pairwise distinct, the `μ c_i` are pairwise distinct, and `c_i = μ c_k` forces `i = k`,
`y i = 0` and `i` an endpoint. -/
theorem coincidences (hx : ∀ i, i + 1 < m → x i < x (i + 1))
    (hint : ∀ i, 0 < i → i + 1 < m → 0 < y i) {i k : ℕ} (hi : i < m) (hk : k < m) :
    ((x i, y i) = (x k, y k) → i = k) ∧ ((x i, -y i) = (x k, -y k) → i = k) ∧
    ((x i, y i) = (x k, -y k) → i = k ∧ y i = 0 ∧ (i = 0 ∨ i = m - 1)) := by
  have xinj : x i = x k → i = k := by
    intro h
    rcases Nat.lt_trichotomy i k with hlt | heq | hgt
    · exact absurd h (ne_of_lt (x_mono hx i k hlt hk))
    · exact heq
    · exact absurd h (ne_of_gt (x_mono hx k i hgt hi))
  refine ⟨fun h => xinj (congrArg Prod.fst h), fun h => xinj (congrArg Prod.fst h), fun h => ?_⟩
  have hik := xinj (congrArg Prod.fst h)
  have h2 : y i = -y k := congrArg Prod.snd h
  rw [← hik] at h2
  have hy : y i = 0 := by linarith
  refine ⟨hik, hy, ?_⟩
  by_contra hcon
  push_neg at hcon
  have := hint i (Nat.pos_of_ne_zero hcon.1) (by omega)
  linarith

end

end MirrorCap

#print axioms MirrorCap.convex_position
#print axioms MirrorCap.convexIndependent
#print axioms MirrorCap.coincidences
