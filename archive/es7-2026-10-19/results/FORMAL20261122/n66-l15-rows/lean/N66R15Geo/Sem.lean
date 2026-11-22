import N66R15Geo.Basic
import N66G15.Pos
import N66G15.Pair

/-!
# N66R15Geo.Sem: the intended assignment of the coupled owner CNF and the soundness of its families

For a `Model` `M` (n66enc: an x-ordered point set given by its triple colors, no 6-cap, no 6-cup, signotope
packets, no 5-cap + 5-cup on common ends) and owners `o : ℕ → ℕ` (positions `< n` ↦ distinct points), the
intended assignment `meaning M o`:
`bef i j` = `o i < o j`; `ge cup i j k` = `k ≤` the label coordinate of the x-sorted pair; `ori i j k` =
`ori3 M.cup (o i) (o j) (o k)`; `cvx i j k l` = `convexFrom` of the four orientations (its definition).

Every clause of the threshold, transitivity/growth, signotope and convex-definition families is true (S1-S5), and
every test clause is true when the test is *good* for the states `σ i` of the owners (T1-T3). The no-octagon
family (S6) is `N66R15Geo.Oct`.
-/

namespace N66R15Geo
open N66R15Enc N66G15 ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks

/-- Owners of the positions `0..n-1`: distinct points of `M`. -/
structure Owners (M : Model) (n : ℕ) (o : ℕ → ℕ) : Prop where
  lt : ∀ i, i < n → o i < M.n
  inj : ∀ i j, i < n → j < n → o i = o j → i = j

/-- The label coordinate (`cup = false`: cap, `true`: cup) of the x-sorted pair of points `x`, `y`. -/
noncomputable def lab (M : Model) (cup : Bool) (x y : ℕ) : ℕ :=
  if cup then (labels M.cup (min x y) (max x y)).2 else (labels M.cup (min x y) (max x y)).1

/-- **The intended assignment.** -/
noncomputable def meaning (M : Model) (o : ℕ → ℕ) : Atom → Bool
  | .bef i j => decide (o i < o j)
  | .ge cup i j k => decide (k ≤ lab M cup (o i) (o j))
  | .ori i j k => ori3 M.cup (o i) (o j) (o k)
  | .cvx i j k l => convexFrom (ori3 M.cup (o i) (o j) (o k)) (ori3 M.cup (o i) (o j) (o l))
      (ori3 M.cup (o i) (o k) (o l)) (ori3 M.cup (o j) (o k) (o l))

/-- A test is good for the states `σ` of the owners (N66 README §2.9; `transport5.good`). -/
def Good (σ : ℕ → Fin 70) : Test → Prop
  | .E u v => N66E15.can (σ u) (σ v) = false
  | .D u v a b => N66E15.domRef (N66E15.prof (σ u)) (N66E15.prof (σ v)) (a, b) = false
  | .P p q r => N66E15.tt (σ p) (σ q) (σ r) = true

section
variable {M : Model} {n : ℕ} {o : ℕ → ℕ}

theorem Owners.ne (ho : Owners M n o) {i j : ℕ} (hi : i < n) (hj : j < n) (hij : i ≠ j) : o i ≠ o j :=
  fun h => hij (ho.inj i j hi hj h)

theorem lab_comm (M : Model) (cup : Bool) (x y : ℕ) : lab M cup x y = lab M cup y x := by
  unfold lab; rw [min_comm, max_comm]

theorem lab_of_lt (M : Model) (cup : Bool) {x y : ℕ} (h : x < y) :
    lab M cup x y = if cup then (labels M.cup x y).2 else (labels M.cup x y).1 := by
  unfold lab; rw [min_eq_left (Nat.le_of_lt h), max_eq_right (Nat.le_of_lt h)]

theorem lab_bounds (M : Model) (cup : Bool) {x y : ℕ} (hxy : x ≠ y) (hx : x < M.n) (hy : y < M.n) :
    1 ≤ lab M cup x y ∧ lab M cup x y ≤ 4 := by
  rcases Nat.lt_or_gt_of_ne hxy with h | h
  · rw [lab_of_lt M cup h]
    have := label_bounds6 M h hy
    cases cup <;> simp <;> omega
  · rw [lab_comm, lab_of_lt M cup h]
    have := label_bounds6 M h hx
    cases cup <;> simp <;> omega

/-! ## The literals -/

theorem eval_befL (ho : Owners M n o) {u v : ℕ} (hu : u < n) (hv : v < n) (huv : u ≠ v) :
    (befL u v).eval (meaning M o) = decide (o u < o v) := by
  have hne := ho.ne hu hv huv
  unfold befL
  split
  · simp [L3.eval, meaning]
  · simp only [L3.eval, meaning]
    by_cases h : o u < o v
    · simp [h, Nat.lt_asymm h]
    · have : o v < o u := by omega
      simp [h, this]

theorem eval_geL (ho : Owners M n o) (cup : Bool) {u v : ℕ} (hu : u < n) (hv : v < n) (huv : u ≠ v) (k : ℕ) :
    (geL cup u v k).eval (meaning M o) = decide (k ≤ lab M cup (o u) (o v)) := by
  have hb := lab_bounds M cup (ho.ne hu hv huv) (ho.lt u hu) (ho.lt v hv)
  unfold geL
  split
  · simp only [L3.eval]; symm; simp; omega
  · split
    · simp only [L3.eval]; symm; simp; omega
    · simp only [L3.eval, meaning, beq_true]
      congr 2
      rcases Nat.lt_or_gt_of_ne huv with h | h
      · rw [min_eq_left (Nat.le_of_lt h), max_eq_right (Nat.le_of_lt h)]
      · rw [min_eq_right (Nat.le_of_lt h), max_eq_left (Nat.le_of_lt h), lab_comm]

theorem eval_oriL (ho : Owners M n o) {a b c : ℕ} (ha : a < n) (hb : b < n) (hc : c < n)
    (hab : a ≠ b) (hbc : b ≠ c) (hac : a ≠ c) :
    (oriL a b c).eval (meaning M o) = ori3 M.cup (o a) (o b) (o c) := by
  have n1 := ho.ne ha hb hab; have n2 := ho.ne hb hc hbc; have n3 := ho.ne ha hc hac
  unfold oriL sort3 inv3
  rcases Nat.lt_or_gt_of_ne hab with h1 | h1 <;> rcases Nat.lt_or_gt_of_ne hbc with h2 | h2 <;>
    rcases Nat.lt_or_gt_of_ne hac with h3 | h3
  · simp [L3.eval, meaning, Nat.le_of_lt h1, Nat.le_of_lt h2, Nat.lt_asymm h1, Nat.lt_asymm h2, Nat.lt_asymm h3]
  · omega
  · -- a < c < b
    simp [L3.eval, meaning, Nat.le_of_lt h1, Nat.not_le_of_lt h2, Nat.le_of_lt h3, Nat.lt_asymm h1,
      Nat.lt_asymm h3, h2]
    rw [ori3_swap23 M.cup n1 n2 n3]
  · -- c < a < b
    simp [L3.eval, meaning, Nat.le_of_lt h1, Nat.not_le_of_lt h2, Nat.not_le_of_lt h3, Nat.lt_asymm h1, h2, h3]
    exact (ori3_cyc M.cup n1 n2 n3)
  · -- b < a < c
    simp [L3.eval, meaning, Nat.not_le_of_lt h1, Nat.le_of_lt h3, h1, Nat.lt_asymm h2, Nat.lt_asymm h3]
    rw [ori3_swap12 M.cup n1 n2 n3]
  · -- b < c < a
    simp [L3.eval, meaning, Nat.not_le_of_lt h1, Nat.not_le_of_lt h3, Nat.le_of_lt h2, h1, h3, Nat.lt_asymm h2]
    have := ori3_cyc M.cup (u := o b) (v := o c) (w := o a) n2 (Ne.symm n3) (Ne.symm n1)
    rw [this]
  · omega
  · -- c < b < a
    simp [L3.eval, meaning, Nat.not_le_of_lt h1, Nat.not_le_of_lt h3, Nat.not_le_of_lt h2, h1, h2, h3]
    rw [ori3_swap12 M.cup (u := o b) (v := o c) (w := o a) n2 (Ne.symm n3) (Ne.symm n1),
      ori3_cyc M.cup (u := o b) (v := o c) (w := o a) n2 (Ne.symm n3) (Ne.symm n1)]

theorem sortAsc_four {a b c d : ℕ} (h1 : a < b) (h2 : b < c) (h3 : c < d) : sortAsc [a, b, c, d] = [a, b, c, d] := by
  simp [sortAsc, insAsc, Nat.le_of_lt h1, Nat.le_of_lt h2, Nat.le_of_lt h3]

theorem eval_cvxL {a b c d : ℕ} (h1 : a < b) (h2 : b < c) (h3 : c < d) :
    (cvxL a b c d).eval (meaning M o) = meaning M o (.cvx a b c d) := by
  unfold cvxL; rw [sortAsc_four h1 h2 h3]; simp [L3.eval]

theorem eval_flipIf (m : Atom → Bool) (b : Bool) (l : L3) : (flipIf b l).eval m = (l.eval m != b) := by
  unfold flipIf; cases b <;> simp [L3.eval_neg]

/-! ## S1: thresholds -/

theorem sat_thresh (ho : Owners M n o) : ∀ L ∈ threshCls n, ∃ l ∈ L, l.eval (meaning M o) = true := by
  intro L hL
  unfold threshCls at hL
  obtain ⟨p, hp, hL⟩ := List.mem_flatMap.1 hL
  obtain ⟨i, j, rfl, hij, hjn⟩ := combs2_shape hp
  simp only [List.mem_flatMap, List.mem_cons, List.mem_map, List.not_mem_nil, or_false] at hL
  obtain ⟨cup, -, k, hk, rfl⟩ := hL
  have hi : i < n := by omega
  by_cases h : k + 1 ≤ lab M cup (o i) (o j)
  · refine ⟨geL cup i j k, by simp, ?_⟩
    rw [eval_geL ho cup hi hjn (by omega)]; simp; omega
  · refine ⟨(geL cup i j (k + 1)).neg, by simp, ?_⟩
    rw [L3.eval_neg, eval_geL ho cup hi hjn (by omega)]; simpa using h

/-! ## S2, S3: transitivity and growth -/

theorem sat_triple (ho : Owners M n o) {a b c : ℕ} (ha : a < n) (hb : b < n) (hc : c < n)
    (hab : a ≠ b) (hbc : b ≠ c) (hac : a ≠ c) : ∀ L ∈ tripleCls a b c, ∃ l ∈ L, l.eval (meaning M o) = true := by
  have eab := eval_befL ho ha hb hab; have ebc := eval_befL ho hb hc hbc; have eac := eval_befL ho ha hc hac
  have n1 := ho.ne ha hb hab; have n2 := ho.ne hb hc hbc
  intro L hL
  unfold tripleCls at hL
  rcases List.mem_cons.1 hL with rfl | hL
  · by_cases x : o a < o b
    · by_cases y : o b < o c
      · exact ⟨befL a c, by simp, by rw [eac]; simp; omega⟩
      · exact ⟨(befL b c).neg, by simp, by rw [L3.eval_neg, ebc]; simpa using y⟩
    · exact ⟨(befL a b).neg, by simp, by rw [L3.eval_neg, eab]; simpa using x⟩
  · simp only [List.mem_flatMap, List.mem_cons, List.mem_map, List.not_mem_nil, or_false] at hL
    obtain ⟨cup, -, k, -, rfl⟩ := hL
    by_cases x : o a < o b
    · by_cases y : o b < o c
      · have hcn := ho.lt c hc
        have hinc := labels_increasing M.n M.cup (o a) (o b) (o c) x y hcn
        have eo : (oriL a b c).eval (meaning M o) = M.cup (o a) (o b) (o c) := by
          rw [eval_oriL ho ha hb hc hab hbc hac, ori3_lt M.cup x y]
        have l1 := lab_of_lt M cup x; have l2 := lab_of_lt M cup y
        have bd := lab_bounds M cup n2 (ho.lt b hb) hcn
        cases cup with
        | false =>
          cases hcol : M.cup (o a) (o b) (o c) with
          | true => exact ⟨oriL a b c, by simp, by simp [eo, hcol]⟩
          | false =>
            have g := hinc.1 hcol
            simp only [Bool.false_eq_true, if_false] at l1 l2
            by_cases hk : k ≤ lab M false (o a) (o b)
            · refine ⟨geL false b c (k + 1), by simp, ?_⟩
              rw [eval_geL ho false hb hc hbc]; simp; omega
            · refine ⟨(geL false a b k).neg, by simp, ?_⟩
              rw [L3.eval_neg, eval_geL ho false ha hb hab]; simpa using hk
        | true =>
          cases hcol : M.cup (o a) (o b) (o c) with
          | false => exact ⟨(oriL a b c).neg, by simp, by simp [L3.eval_neg, eo, hcol]⟩
          | true =>
            have g := hinc.2 hcol
            simp only [if_true] at l1 l2
            by_cases hk : k ≤ lab M true (o a) (o b)
            · refine ⟨geL true b c (k + 1), by simp, ?_⟩
              rw [eval_geL ho true hb hc hbc]; simp; omega
            · refine ⟨(geL true a b k).neg, by simp, ?_⟩
              rw [L3.eval_neg, eval_geL ho true ha hb hab]; simpa using hk
      · exact ⟨(befL b c).neg, by simp, by rw [L3.eval_neg, ebc]; simpa using y⟩
    · exact ⟨(befL a b).neg, by simp, by rw [L3.eval_neg, eab]; simpa using x⟩

theorem sat_trip (ho : Owners M n o) : ∀ L ∈ tripCls n, ∃ l ∈ L, l.eval (meaning M o) = true := by
  intro L hL
  unfold tripCls at hL
  simp only [List.mem_flatMap, List.mem_range] at hL
  obtain ⟨a, ha, b, hb, c, hc, hL⟩ := hL
  split at hL
  · simp at hL
  · rename_i h
    exact sat_triple ho ha hb hc (by tauto) (by tauto) (by tauto) L hL

/-! ## S4, S5: signotope packets and the convex definition -/

theorem bad4_invalid : ∀ bb ∈ bad4, ∀ p0 p1 p2 p3 : Bool, PacketValid p0 p1 p2 p3 →
    ¬ (p0 = bb.1 ∧ p1 = bb.2.1 ∧ p2 = bb.2.2.1 ∧ p3 = bb.2.2.2) := by decide

theorem sat_packet (ho : Owners M n o) {q0 q1 q2 q3 : ℕ} (h0 : q0 < n) (h1 : q1 < n) (h2 : q2 < n) (h3 : q3 < n)
    (d01 : q0 ≠ q1) (d02 : q0 ≠ q2) (d03 : q0 ≠ q3) (d12 : q1 ≠ q2) (d13 : q1 ≠ q3) (d23 : q2 ≠ q3) :
    ∀ L ∈ packetCls [q0, q1, q2, q3], ∃ l ∈ L, l.eval (meaning M o) = true := by
  intro L hL
  unfold packetCls at hL
  obtain ⟨bb, hbb, rfl⟩ := List.mem_map.1 hL
  by_cases x : o q0 < o q1
  · by_cases y : o q1 < o q2
    · by_cases z : o q2 < o q3
      · have hn3 := ho.lt q3 h3
        have pv := M.signotope (o q0) (o q1) (o q2) (o q3) x y z hn3
        have e0 : (oriL q0 q1 q2).eval (meaning M o) = M.cup (o q0) (o q1) (o q2) := by
          rw [eval_oriL ho h0 h1 h2 d01 d12 d02, ori3_lt M.cup x y]
        have e1 : (oriL q0 q1 q3).eval (meaning M o) = M.cup (o q0) (o q1) (o q3) := by
          rw [eval_oriL ho h0 h1 h3 d01 d13 d03, ori3_lt M.cup x (Nat.lt_trans y z)]
        have e2 : (oriL q0 q2 q3).eval (meaning M o) = M.cup (o q0) (o q2) (o q3) := by
          rw [eval_oriL ho h0 h2 h3 d02 d23 d03, ori3_lt M.cup (Nat.lt_trans x y) z]
        have e3 : (oriL q1 q2 q3).eval (meaning M o) = M.cup (o q1) (o q2) (o q3) := by
          rw [eval_oriL ho h1 h2 h3 d12 d23 d13, ori3_lt M.cup y z]
        have hne := bad4_invalid bb hbb _ _ _ _ pv
        by_cases c0 : M.cup (o q0) (o q1) (o q2) = bb.1
        · by_cases c1 : M.cup (o q0) (o q1) (o q3) = bb.2.1
          · by_cases c2 : M.cup (o q0) (o q2) (o q3) = bb.2.2.1
            · have c3 : M.cup (o q1) (o q2) (o q3) ≠ bb.2.2.2 := fun c3 => hne ⟨c0, c1, c2, c3⟩
              exact ⟨flipIf bb.2.2.2 (oriL q1 q2 q3), by simp, by rw [eval_flipIf, e3]; simpa using c3⟩
            · exact ⟨flipIf bb.2.2.1 (oriL q0 q2 q3), by simp, by rw [eval_flipIf, e2]; simpa using c2⟩
          · exact ⟨flipIf bb.2.1 (oriL q0 q1 q3), by simp, by rw [eval_flipIf, e1]; simpa using c1⟩
        · exact ⟨flipIf bb.1 (oriL q0 q1 q2), by simp, by rw [eval_flipIf, e0]; simpa using c0⟩
      · exact ⟨(befL q2 q3).neg, by simp, by rw [L3.eval_neg, eval_befL ho h2 h3 d23]; simpa using z⟩
    · exact ⟨(befL q1 q2).neg, by simp, by rw [L3.eval_neg, eval_befL ho h1 h2 d12]; simpa using y⟩
  · exact ⟨(befL q0 q1).neg, by simp, by rw [L3.eval_neg, eval_befL ho h0 h1 d01]; simpa using x⟩

theorem sat_cvxDef (ho : Owners M n o) {a b c d : ℕ} (h1 : a < b) (h2 : b < c) (h3 : c < d) (h4 : d < n) :
    ∀ L ∈ cvxDefCls a b c d, ∃ l ∈ L, l.eval (meaning M o) = true := by
  intro L hL
  unfold cvxDefCls at hL
  obtain ⟨m, -, rfl⟩ := List.mem_map.1 hL
  have e0 := eval_oriL ho (a := a) (b := b) (c := c) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
  have e1 := eval_oriL ho (a := a) (b := b) (c := d) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
  have e2 := eval_oriL ho (a := a) (b := c) (c := d) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
  have e3 := eval_oriL ho (a := b) (b := c) (c := d) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
  have ecv := eval_cvxL (M := M) (o := o) h1 h2 h3
  generalize bits4 m = bb
  by_cases c0 : ori3 M.cup (o a) (o b) (o c) = bb.1
  · by_cases c1 : ori3 M.cup (o a) (o b) (o d) = bb.2.1
    · by_cases c2 : ori3 M.cup (o a) (o c) (o d) = bb.2.2.1
      · by_cases c3 : ori3 M.cup (o b) (o c) (o d) = bb.2.2.2
        · have hv : (cvxL a b c d).eval (meaning M o) = convexFrom bb.1 bb.2.1 bb.2.2.1 bb.2.2.2 := by
            rw [ecv]; simp only [meaning]; rw [c0, c1, c2, c3]
          by_cases hcf : convexFrom bb.1 bb.2.1 bb.2.2.1 bb.2.2.2 = true
          · exact ⟨cvxL a b c d, by simp [hcf], by rw [hv]; exact hcf⟩
          · exact ⟨(cvxL a b c d).neg, by simp [hcf], by rw [L3.eval_neg, hv]; simpa using hcf⟩
        · exact ⟨flipIf bb.2.2.2 (oriL b c d), by simp, by rw [eval_flipIf, e3]; simpa using c3⟩
      · exact ⟨flipIf bb.2.2.1 (oriL a c d), by simp, by rw [eval_flipIf, e2]; simpa using c2⟩
    · exact ⟨flipIf bb.2.1 (oriL a b d), by simp, by rw [eval_flipIf, e1]; simpa using c1⟩
  · exact ⟨flipIf bb.1 (oriL a b c), by simp, by rw [eval_flipIf, e0]; simpa using c0⟩

theorem perm4_shape {ix : List ℕ} (h : ix ∈ perm4Idx) (a b c d : ℕ) :
    ∃ q0 q1 q2 q3, ix.map (fun x => [a, b, c, d].getD x 0) = [q0, q1, q2, q3] ∧
      ({q0, q1, q2, q3} : Finset ℕ) = {a, b, c, d} := by
  simp only [perm4Idx, List.mem_cons, List.not_mem_nil, or_false] at h
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl |
    rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    exact ⟨_, _, _, _, rfl, by first | rfl | (ext; simp only [Finset.mem_insert, Finset.mem_singleton]; tauto)⟩

theorem sat_quad (ho : Owners M n o) : ∀ L ∈ quadCls n, ∃ l ∈ L, l.eval (meaning M o) = true := by
  intro L hL
  unfold quadCls at hL
  obtain ⟨s, hs, hL⟩ := List.mem_flatMap.1 hL
  obtain ⟨a, b, c, d, rfl, h1, h2, h3, h4⟩ := combs4_shape hs
  simp only [List.mem_append, List.mem_flatMap] at hL
  rcases hL with ⟨ix, hix, hL⟩ | hL
  · obtain ⟨q0, q1, q2, q3, hq, hset⟩ := perm4_shape hix a b c d
    rw [hq] at hL
    have hm : ∀ x, x ∈ ({q0, q1, q2, q3} : Finset ℕ) ↔ x ∈ ({a, b, c, d} : Finset ℕ) := fun x => by rw [hset]
    have m0 := (hm q0).1 (by simp); have m1 := (hm q1).1 (by simp)
    have m2 := (hm q2).1 (by simp); have m3 := (hm q3).1 (by simp)
    have ma := (hm a).2 (by simp); have mb := (hm b).2 (by simp)
    have mc := (hm c).2 (by simp); have md := (hm d).2 (by simp)
    simp only [Finset.mem_insert, Finset.mem_singleton] at m0 m1 m2 m3 ma mb mc md
    exact sat_packet ho (by omega) (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
      (by omega) (by omega) (by omega) L hL
  · exact sat_cvxDef ho h1 h2 h3 h4 L hL

/-! ## T1-T3: tests -/

theorem canF_true_of (M : Model) {X Y : ℕ} (hXY : X < Y) (hY : Y < M.n) :
    N66E15.canF ⟨idxOf M.cup X, idxOf_lt M (lt_trans hXY hY)⟩ ⟨idxOf M.cup Y, idxOf_lt M hY⟩ = true := by
  unfold N66E15.canF
  exact List.any_eq_true.2 ⟨_, (label_dom M hXY hY).1, label_domRef M hXY hY⟩

theorem sat_test (ho : Owners M n o) (σ : ℕ → Fin 70) (hσ : ∀ i, i < n → idxOf M.cup (o i) = (σ i).val)
    {x : Test} (hx : testOk n x = true) (hg : Good σ x) : ∃ l ∈ testCl x, l.eval (meaning M o) = true := by
  cases x with
  | E u v =>
    simp only [testOk, Bool.and_eq_true, decide_eq_true_eq, bne_iff_ne, ne_eq] at hx
    obtain ⟨⟨hu, hv⟩, huv⟩ := hx
    refine ⟨(befL u v).neg, by simp [testCl], ?_⟩
    rw [L3.eval_neg, eval_befL ho hu hv huv]
    simp only [Bool.not_eq_true', decide_eq_false_iff_not, not_lt]
    by_contra hlt
    push_neg at hlt
    have hc := canF_true_of M hlt (ho.lt v hv)
    have e1 : (⟨idxOf M.cup (o u), idxOf_lt M (lt_trans hlt (ho.lt v hv))⟩ : Fin 70) = σ u := Fin.ext (hσ u hu)
    have e2 : (⟨idxOf M.cup (o v), idxOf_lt M (ho.lt v hv)⟩ : Fin 70) = σ v := Fin.ext (hσ v hv)
    rw [e1, e2, ← can_eq] at hc
    simp only [Good] at hg
    rw [hg] at hc; exact Bool.false_ne_true hc
  | D u v a b =>
    simp only [testOk, Bool.and_eq_true, decide_eq_true_eq, bne_iff_ne, ne_eq] at hx
    obtain ⟨⟨hu, hv⟩, huv⟩ := hx
    by_cases hlt : o u < o v
    · have hvn := ho.lt v hv
      have hd := label_domRef M hlt hvn
      have e1 : (⟨idxOf M.cup (o u), idxOf_lt M (lt_trans hlt hvn)⟩ : Fin 70) = σ u := Fin.ext (hσ u hu)
      have e2 : (⟨idxOf M.cup (o v), idxOf_lt M hvn⟩ : Fin 70) = σ v := Fin.ext (hσ v hv)
      rw [e1, e2] at hd
      simp only [Good] at hg
      have hne : labels M.cup (o u) (o v) ≠ (a, b) := fun h => by rw [h, hg] at hd; exact Bool.false_ne_true hd
      have hmin : min u v ≠ max u v := by omega
      have hmn : min u v < n := by omega
      have hmx : max u v < n := by omega
      have lab1 : lab M false (o (min u v)) (o (max u v)) = (labels M.cup (o u) (o v)).1 := by
        rcases Nat.lt_or_gt_of_ne huv with h | h
        · rw [min_eq_left (Nat.le_of_lt h), max_eq_right (Nat.le_of_lt h), lab_of_lt M false hlt]; rfl
        · rw [min_eq_right (Nat.le_of_lt h), max_eq_left (Nat.le_of_lt h), lab_comm, lab_of_lt M false hlt]; rfl
      have lab2 : lab M true (o (min u v)) (o (max u v)) = (labels M.cup (o u) (o v)).2 := by
        rcases Nat.lt_or_gt_of_ne huv with h | h
        · rw [min_eq_left (Nat.le_of_lt h), max_eq_right (Nat.le_of_lt h), lab_of_lt M true hlt]; rfl
        · rw [min_eq_right (Nat.le_of_lt h), max_eq_left (Nat.le_of_lt h), lab_comm, lab_of_lt M true hlt]; rfl
      have g1 := eval_geL ho false hmn hmx hmin
      have g2 := eval_geL ho true hmn hmx hmin
      by_cases ha : (labels M.cup (o u) (o v)).1 = a
      · have hb : (labels M.cup (o u) (o v)).2 ≠ b := fun hb => hne (Prod.ext ha hb)
        rcases Nat.lt_or_gt_of_ne hb with hb | hb
        · refine ⟨(geL true (min u v) (max u v) b).neg, by simp [testCl], ?_⟩
          rw [L3.eval_neg, g2, lab2]; simp; omega
        · refine ⟨geL true (min u v) (max u v) (b + 1), by simp [testCl], ?_⟩
          rw [g2, lab2]; simp; omega
      · rcases Nat.lt_or_gt_of_ne ha with ha | ha
        · refine ⟨(geL false (min u v) (max u v) a).neg, by simp [testCl], ?_⟩
          rw [L3.eval_neg, g1, lab1]; simp; omega
        · refine ⟨geL false (min u v) (max u v) (a + 1), by simp [testCl], ?_⟩
          rw [g1, lab1]; simp; omega
    · refine ⟨(befL u v).neg, by simp [testCl], ?_⟩
      rw [L3.eval_neg, eval_befL ho hu hv huv]; simpa using hlt
  | P p q r =>
    simp only [testOk, Bool.and_eq_true, decide_eq_true_eq, bne_iff_ne, ne_eq] at hx
    obtain ⟨⟨⟨⟨⟨hp, hq⟩, hr⟩, hpq⟩, hqr⟩, hpr⟩ := hx
    refine ⟨oriL p q r, by simp [testCl], ?_⟩
    rw [eval_oriL ho hp hq hr hpq hqr hpr]
    exact tt_sound M (ho.lt p hp) (ho.lt q hq) (ho.lt r hr) (hσ p hp) (hσ q hq) (hσ r hr) hg

end

end N66R15Geo
