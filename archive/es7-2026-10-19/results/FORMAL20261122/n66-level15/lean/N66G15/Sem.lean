import N66G15.Families

/-!
# N66G15.Sem: what the order, orientation and threshold literals mean for the owners

For states with owners (points `x, y, z` of the model with those states), the generator's literals agree with the
intended assignment exactly when:
* `befLit a b` ↔ `x < y` (`agree_befLit`);
* `oriLit a b c` ↔ `ori3 cup x y z = true` (`agree_oriLit`; `ori3` is antisymmetric, `ori3_swap12/23/cyc`);
* `geAtom cup a b k` (2 ≤ k ≤ 4) ↔ `k ≤` the label coordinate of the pair (`agree_geAtom`).
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks N66E15

/-- A literal agrees with the intended assignment. -/
def Agree (M : Model) (l : SLit) : Prop := M.meaning l.2 = l.1

theorem agree_neg (M : Model) (l : SLit) : Agree M l.neg ↔ ¬ Agree M l := by
  obtain ⟨b, a⟩ := l
  unfold Agree SLit.neg
  cases b <;> cases M.meaning a <;> simp

theorem agree_guard (M : Model) (s : Fin 70) : Agree M (guard s) ↔ ¬ M.occ s := by
  simp [Agree, N66E15.guard, meaning_sel]

/-- The owner of an occupied state. -/
theorem occ_iff (M : Model) (s : Fin 70) : M.occ s ↔ ∃ x < M.n, idxOf M.cup x = s.val := Iff.rfl

theorem owner_unique (M : Model) {x x' : ℕ} {s : Fin 70} (hx : x < M.n) (hx' : x' < M.n)
    (h : idxOf M.cup x = s.val) (h' : idxOf M.cup x' = s.val) : x = x' :=
  idxOf_injective M hx hx' (h.trans h'.symm)

theorem owner_ne (M : Model) {x y : ℕ} {a b : Fin 70} (hab : a ≠ b)
    (hx : idxOf M.cup x = a.val) (hy : idxOf M.cup y = b.val) : x ≠ y := by
  rintro rfl
  exact hab (Fin.ext (hx.symm.trans hy))

open Classical in
theorem meaning_before (M : Model) (i j : Fin 70) : M.meaning (.before i j) = decide (M.Bef i j) := rfl

theorem bef_iff (M : Model) {i j : Fin 70} {x y : ℕ} (hx : x < M.n) (hy : y < M.n)
    (hi : idxOf M.cup x = i.val) (hj : idxOf M.cup y = j.val) : M.Bef i j ↔ x < y := by
  constructor
  · rintro ⟨u, v, huv, hv, hu, hv'⟩
    rw [owner_unique M (lt_trans huv hv) hx hu hi, owner_unique M hv hy hv' hj] at huv
    exact huv
  · intro h
    exact ⟨x, y, h, hy, hi, hj⟩

/-- **The order literal.** -/
theorem agree_befLit (M : Model) {a b : Fin 70} {x y : ℕ} (hab : a ≠ b) (hx : x < M.n) (hy : y < M.n)
    (ha : idxOf M.cup x = a.val) (hb : idxOf M.cup y = b.val) : Agree M (befLit a b) ↔ x < y := by
  have hne := owner_ne M hab ha hb
  unfold befLit Agree
  split
  · simp only [meaning_before, decide_eq_true_eq]
    exact bef_iff M hx hy ha hb
  · simp only [meaning_before, decide_eq_false_iff_not]
    rw [bef_iff M hy hx hb ha]
    omega

/-! ## The orientation of three owners -/

theorem ori3_lt (cup : ℕ → ℕ → ℕ → Bool) {u v w : ℕ} (h1 : u < v) (h2 : v < w) : ori3 cup u v w = cup u v w := by
  simp [ori3, h1, h2]

theorem ori3_swap23 (cup : ℕ → ℕ → ℕ → Bool) {u v w : ℕ} (h1 : u ≠ v) (h2 : v ≠ w) (h3 : u ≠ w) :
    ori3 cup u w v = !ori3 cup u v w := by
  rcases Nat.lt_or_gt_of_ne h1 with a1 | a1 <;> rcases Nat.lt_or_gt_of_ne h2 with a2 | a2 <;>
    rcases Nat.lt_or_gt_of_ne h3 with a3 | a3 <;>
    simp [ori3, a1, a2, a3, Nat.lt_asymm a1, Nat.lt_asymm a2, Nat.lt_asymm a3] <;> omega

theorem ori3_swap12 (cup : ℕ → ℕ → ℕ → Bool) {u v w : ℕ} (h1 : u ≠ v) (h2 : v ≠ w) (h3 : u ≠ w) :
    ori3 cup v u w = !ori3 cup u v w := by
  rcases Nat.lt_or_gt_of_ne h1 with a1 | a1 <;> rcases Nat.lt_or_gt_of_ne h2 with a2 | a2 <;>
    rcases Nat.lt_or_gt_of_ne h3 with a3 | a3 <;>
    simp [ori3, a1, a2, a3, Nat.lt_asymm a1, Nat.lt_asymm a2, Nat.lt_asymm a3] <;> omega

theorem ori3_cyc (cup : ℕ → ℕ → ℕ → Bool) {u v w : ℕ} (h1 : u ≠ v) (h2 : v ≠ w) (h3 : u ≠ w) :
    ori3 cup w u v = ori3 cup u v w := by
  rcases Nat.lt_or_gt_of_ne h1 with a1 | a1 <;> rcases Nat.lt_or_gt_of_ne h2 with a2 | a2 <;>
    rcases Nat.lt_or_gt_of_ne h3 with a3 | a3 <;>
    simp [ori3, a1, a2, a3, Nat.lt_asymm a1, Nat.lt_asymm a2, Nat.lt_asymm a3] <;> omega

open Classical in
theorem meaning_orient (M : Model) (i j k : Fin 70) : M.meaning (.orient i j k) = decide (M.Ori i j k) := rfl

theorem ori_iff (M : Model) {i j k : Fin 70} {x y z : ℕ} (hx : x < M.n) (hy : y < M.n) (hz : z < M.n)
    (hi : idxOf M.cup x = i.val) (hj : idxOf M.cup y = j.val) (hk : idxOf M.cup z = k.val) :
    M.Ori i j k ↔ ori3 M.cup x y z = true := by
  constructor
  · rintro ⟨u, v, w, hu, hv, hw, hu', hv', hw', h⟩
    rw [owner_unique M hu hx hu' hi, owner_unique M hv hy hv' hj, owner_unique M hw hz hw' hk] at h
    exact h
  · intro h
    exact ⟨x, y, z, hx, hy, hz, hi, hj, hk, h⟩

/-- **The orientation literal.** -/
theorem agree_oriLit (M : Model) {a b c : Fin 70} {x y z : ℕ} (hab : a ≠ b) (hbc : b ≠ c) (hac : a ≠ c)
    (hx : x < M.n) (hy : y < M.n) (hz : z < M.n)
    (ha : idxOf M.cup x = a.val) (hb : idxOf M.cup y = b.val) (hc : idxOf M.cup z = c.val) :
    Agree M (oriLit a b c) ↔ ori3 M.cup x y z = true := by
  have nxy := owner_ne M hab ha hb
  have nyz := owner_ne M hbc hb hc
  have nxz := owner_ne M hac ha hc
  unfold oriLit Agree
  split
  · split
    · simp only [meaning_orient, decide_eq_true_eq]
      exact ori_iff M hx hy hz ha hb hc
    · split
      · simp only [meaning_orient, decide_eq_false_iff_not]
        rw [ori_iff M hx hz hy ha hc hb, ori3_swap23 M.cup nxy nyz nxz]
        simp
      · simp only [meaning_orient, decide_eq_true_eq]
        rw [ori_iff M hz hx hy hc ha hb, ori3_cyc M.cup nxy nyz nxz]
  · split
    · simp only [meaning_orient, decide_eq_false_iff_not]
      rw [ori_iff M hy hx hz hb ha hc, ori3_swap12 M.cup nxy nyz nxz]
      simp
    · split
      · simp only [meaning_orient, decide_eq_true_eq]
        rw [ori_iff M hy hz hx hb hc ha]
        rw [(ori3_cyc M.cup nyz (Ne.symm nxz) (Ne.symm nxy)).symm]
      · simp only [meaning_orient, decide_eq_false_iff_not]
        rw [ori_iff M hz hy hx hc hb ha]
        rw [ori3_swap12 M.cup nyz (Ne.symm nxz) (Ne.symm nxy),
          (ori3_cyc M.cup nyz (Ne.symm nxz) (Ne.symm nxy)).symm]
        simp

/-! ## The threshold literal -/

theorem labGe_iff (M : Model) {cup : Bool} {i j : Fin 70} {x y : ℕ} (hxy : x < y) (hy : y < M.n)
    (hi : idxOf M.cup x = i.val) (hj : idxOf M.cup y = j.val) (k : ℕ) :
    M.LabGe cup i j k ↔ k ≤ (if cup then (labels M.cup x y).2 else (labels M.cup x y).1) := by
  have hx : x < M.n := lt_trans hxy hy
  constructor
  · rintro ⟨u, v, huv, hv, hidx, hk⟩
    have hu : u < M.n := lt_trans huv hv
    rcases hidx with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · rw [owner_unique M hu hx h1 hi, owner_unique M hv hy h2 hj] at hk
      exact hk
    · have e1 := owner_unique M hu hy h1 hj
      have e2 := owner_unique M hv hx h2 hi
      omega
  · intro h
    exact ⟨x, y, hxy, hy, Or.inl ⟨hi, hj⟩, h⟩

theorem labGe_comm (M : Model) {cup : Bool} {i j : Fin 70} {k : ℕ} : M.LabGe cup i j k ↔ M.LabGe cup j i k := by
  constructor <;> rintro ⟨u, v, huv, hv, hidx, hk⟩ <;> exact ⟨u, v, huv, hv, hidx.symm, hk⟩

/-- **The threshold literal** for an x-ordered pair of owners. -/
theorem agree_geAtom (M : Model) (cup : Bool) {a b : Fin 70} {x y : ℕ} (hxy : x < y) (hy : y < M.n)
    (ha : idxOf M.cup x = a.val) (hb : idxOf M.cup y = b.val) {k : ℕ} (hk : k < 5) :
    M.meaning (geAtom cup a b k) = true ↔ k ≤ (if cup then (labels M.cup x y).2 else (labels M.cup x y).1) := by
  classical
  rw [meaning_geAtom M cup a b hk, decide_eq_true_eq]
  split
  · exact labGe_iff M hxy hy ha hb k
  · rw [labGe_comm]; exact labGe_iff M hxy hy ha hb k

end N66G15

#print axioms N66G15.agree_befLit
#print axioms N66G15.agree_oriLit
#print axioms N66G15.agree_geAtom
