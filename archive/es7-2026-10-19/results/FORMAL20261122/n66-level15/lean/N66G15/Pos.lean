import N66G15.Final3

/-!
# N66G15.Pos: soundness of the positive clauses (4.3, the six-order test on plain domains) for every `Model`

If `tt a b c` holds, then for the x-order `(p, q, r)` of the owners the three plain domains contain the pair labels
(state separation, `ActualRanks.actual_incoming_admissible`), so the test's bound `max D(q→r) ≤ min D(p→q)` in the
coordinate of the order's parity holds for the labels, and label growth (`labels_increasing`) then fixes the color
of the x-ordered triple; the parity bookkeeping of `ori3` turns it into `ori3 x y z = true`.
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks ErdosSzekeres.Omission.StateInterface
  N66E15

/-! ## The tables, without evaluating them -/

theorem tt_eq (a b c : Fin 70) : tt a b c = ttF a b c := by
  have ha := a.isLt; have hb := b.isLt; have hc := c.isLt
  unfold tt ttArr
  rw [Array.getD_eq_getD_getElem?, Array.getElem?_ofFn, dif_pos (by omega), Option.getD_some]
  congr 1 <;> apply Fin.ext <;> simp only [] <;> omega

theorem prof_idxOf (M : Model) {v : ℕ} (hv : v < M.n) :
    prof ⟨idxOf M.cup v, idxOf_lt M hv⟩ = profOf M.cup v := by
  unfold prof stateArr
  rw [Array.getD_eq_getD_getElem?, List.getElem?_toArray,
    List.getElem?_eq_getElem (by rw [stateList_length]; exact idxOf_lt M hv), Option.getD_some]
  exact profOf_of_idxOf M hv

/-! ## Labels lie in the plain domains -/

theorem col_profOf (cup : ℕ → ℕ → ℕ → Bool) (v x : ℕ) (h1 : 1 ≤ x) (h4 : x ≤ 4) :
    (profOf cup v).col x = column cup v (x - 1) := by
  unfold Prof.col profOf
  rcases (show x = 1 ∨ x = 2 ∨ x = 3 ∨ x = 4 by omega) with rfl | rfl | rfl | rfl <;> simp

theorem label_cells (M : Model) {u v : ℕ} (huv : u < v) (hv : v < M.n) :
    cellIn (profOf M.cup v) (labels M.cup u v).1 (labels M.cup u v).2 = true ∧
      cellIn (profOf M.cup u) (labels M.cup u v).1 (labels M.cup u v).2 = false := by
  have bd := label_bounds6 M huv hv
  have adm := actual_incoming_admissible M.n M.cup u v huv hv
  have e : (labels M.cup u v) = ((labels M.cup u v).1 - 1 + 1, (labels M.cup u v).2) := by
    ext <;> simp; omega
  have hV := (incoming_iff_column M.cup v ((labels M.cup u v).1 - 1) (labels M.cup u v).2 (by omega)).1
    (by rw [← e]; exact adm.1)
  have hU : ¬ (labels M.cup u v).2 ≤ column M.cup u ((labels M.cup u v).1 - 1) := fun h =>
    adm.2 (by rw [e]; exact (incoming_iff_column M.cup u _ _ (by omega)).2 h)
  refine ⟨?_, ?_⟩
  · simp only [cellIn, decide_eq_true_eq]
    rw [col_profOf M.cup v _ (by omega) (by omega)]
    omega
  · simp only [cellIn, decide_eq_false_iff_not]
    rw [col_profOf M.cup u _ (by omega) (by omega)]
    omega

theorem mem_grid' {x y : ℕ} (h1 : 1 ≤ x) (h2 : x ≤ 4) (h3 : 1 ≤ y) (h4 : y ≤ 4) : (x, y) ∈ grid := by
  unfold grid
  simp only [List.mem_flatMap, List.mem_map, List.mem_range, Prod.mk.injEq]
  exact ⟨x - 1, by omega, y - 1, by omega, by omega, by omega⟩

theorem label_dom (M : Model) {u v : ℕ} (huv : u < v) (hv : v < M.n) :
    (labels M.cup u v) ∈ grid ∧ domPlain (prof ⟨idxOf M.cup u, idxOf_lt M (lt_trans huv hv)⟩)
      (prof ⟨idxOf M.cup v, idxOf_lt M hv⟩) (labels M.cup u v) = true := by
  have bd := label_bounds6 M huv hv
  have hc := label_cells M huv hv
  refine ⟨mem_grid' bd.1 bd.2.1 bd.2.2.1 bd.2.2.2, ?_⟩
  rw [prof_idxOf M (lt_trans huv hv), prof_idxOf M hv]
  simp only [domPlain, hc.1, hc.2, Bool.not_false, Bool.and_self]

/-! ## Min and max over a domain -/

theorem foldl_min_le : ∀ (l : List ℕ) (x : ℕ), l.foldl min x ≤ x ∧ ∀ a ∈ l, l.foldl min x ≤ a
  | [], x => ⟨Nat.le_refl x, fun _ h => absurd h List.not_mem_nil⟩
  | b :: l, x => by
    obtain ⟨h1, h2⟩ := foldl_min_le l (min x b)
    simp only [List.foldl_cons]
    refine ⟨Nat.le_trans h1 (Nat.min_le_left x b), fun a ha => ?_⟩
    rcases List.mem_cons.1 ha with rfl | ha
    · exact Nat.le_trans h1 (Nat.min_le_right x a)
    · exact h2 a ha

theorem mn_le (coord : Bool) (u v : Fin 70) {z : ℕ × ℕ} (hz : z ∈ grid) (hd : domPlain (prof u) (prof v) z = true) :
    mnPlain coord u v ≤ coordOf coord z := by
  have hmem : coordOf coord z ∈ (grid.filter (domPlain (prof u) (prof v))).map (coordOf coord) :=
    List.mem_map_of_mem (List.mem_filter.2 ⟨hz, hd⟩)
  unfold mnPlain
  split
  · rename_i h; rw [h] at hmem; simp at hmem
  · rename_i x xs h
    rw [h] at hmem
    obtain ⟨h1, h2⟩ := foldl_min_le xs x
    rcases List.mem_cons.1 hmem with e | e
    · rw [e]; exact h1
    · exact h2 _ e

theorem le_mx (coord : Bool) (u v : Fin 70) {z : ℕ × ℕ} (hz : z ∈ grid) (hd : domPlain (prof u) (prof v) z = true) :
    coordOf coord z ≤ mxPlain coord u v := by
  have hmem : coordOf coord z ∈ (grid.filter (domPlain (prof u) (prof v))).map (coordOf coord) :=
    List.mem_map_of_mem (List.mem_filter.2 ⟨hz, hd⟩)
  unfold mxPlain
  split
  · rename_i h; rw [h] at hmem; simp at hmem
  · rename_i x xs h
    rw [h] at hmem
    obtain ⟨h1, h2⟩ := EncB.le_foldl_max xs x
    rcases List.mem_cons.1 hmem with e | e
    · rw [e]; exact h1
    · exact h2 _ e

theorem nePlain_of (u v : Fin 70) {z : ℕ × ℕ} (hz : z ∈ grid) (hd : domPlain (prof u) (prof v) z = true) :
    nePlain u v = true := List.any_eq_true.2 ⟨z, hz, hd⟩

/-! ## One x-ordered triple -/

/-- **The forced color.** If the test's condition for the order `(p, q, r)` holds and the owners `P < Q < R` have
these states, the triple is a cup for the cap coordinate (`coord = false`) and a cap for the cup coordinate. -/
theorem forced_color (M : Model) {p q r : Fin 70} {P Q R : ℕ} (hPQ : P < Q) (hQR : Q < R) (hR : R < M.n)
    (hp : idxOf M.cup P = p.val) (hq : idxOf M.cup Q = q.val) (hr : idxOf M.cup R = r.val) (coord : Bool)
    (hcond : (!(nePlain p q && nePlain q r && nePlain p r) || decide (mxPlain coord q r ≤ mnPlain coord p q)) = true) :
    M.cup P Q R = !coord := by
  have ep : p = ⟨idxOf M.cup P, idxOf_lt M (lt_trans hPQ (lt_trans hQR hR))⟩ := Fin.ext hp.symm
  have eq' : q = ⟨idxOf M.cup Q, idxOf_lt M (lt_trans hQR hR)⟩ := Fin.ext hq.symm
  have er : r = ⟨idxOf M.cup R, idxOf_lt M hR⟩ := Fin.ext hr.symm
  subst ep; subst eq'; subst er
  have dPQ := label_dom M hPQ (lt_trans hQR hR)
  have dQR := label_dom M hQR hR
  have dPR := label_dom M (lt_trans hPQ hQR) hR
  rw [nePlain_of _ _ dPQ.1 dPQ.2, nePlain_of _ _ dQR.1 dQR.2, nePlain_of _ _ dPR.1 dPR.2] at hcond
  simp only [Bool.and_self, Bool.not_true, Bool.false_or, decide_eq_true_eq] at hcond
  have h1 := le_mx coord _ _ dQR.1 dQR.2
  have h2 := mn_le coord _ _ dPQ.1 dPQ.2
  have hinc := (labels_increasing M.n M.cup) P Q R hPQ hQR hR
  cases coord with
  | false =>
    simp only [coordOf, Bool.false_eq_true, if_false] at h1 h2
    cases hc : M.cup P Q R with
    | false => have := hinc.1 hc; omega
    | true => rfl
  | true =>
    simp only [coordOf, if_true] at h1 h2
    cases hc : M.cup P Q R with
    | false => rfl
    | true => have := hinc.2 hc; omega

/-- **The six-order test is sound:** `tt a b c` makes the owners of `a, b, c` positively oriented in that order. -/
theorem tt_sound (M : Model) {a b c : Fin 70} {x y z : ℕ} (hx : x < M.n) (hy : y < M.n) (hz : z < M.n)
    (ha : idxOf M.cup x = a.val) (hb : idxOf M.cup y = b.val) (hc : idxOf M.cup z = c.val)
    (htt : tt a b c = true) : ori3 M.cup x y z = true := by
  rw [tt_eq] at htt
  unfold ttF at htt
  simp only [Bool.and_eq_true, decide_eq_true_eq] at htt
  obtain ⟨⟨hab, hbc, hac⟩, hall⟩ := htt
  have nxy := owner_ne M hab ha hb
  have nyz := owner_ne M hbc hb hc
  have nxz := owner_ne M hac ha hc
  have hcase : ∀ o ∈ sixOrders a b c,
      (!(nePlain o.1 o.2.1 && nePlain o.2.1 o.2.2.1 && nePlain o.1 o.2.2.1) ||
        decide (mxPlain o.2.2.2 o.2.1 o.2.2.1 ≤ mnPlain o.2.2.2 o.1 o.2.1)) = true :=
    fun o ho => List.all_eq_true.1 hall o ho
  rcases Nat.lt_or_gt_of_ne nxy with h1 | h1 <;> rcases Nat.lt_or_gt_of_ne nyz with h2 | h2 <;>
    rcases Nat.lt_or_gt_of_ne nxz with h3 | h3
  · have := forced_color M h1 h2 hz ha hb hc false (hcase (a, b, c, false) (by simp [sixOrders]))
    simp [ori3, h1, h2, this]
  · omega
  · have := forced_color M h3 (show z < y by omega) hy ha hc hb true (hcase (a, c, b, true) (by simp [sixOrders]))
    simp [ori3, h1, show ¬ y < z by omega, h3, this]
  · have := forced_color M (show z < x by omega) h1 hy hc ha hb false
      (hcase (c, a, b, false) (by simp [sixOrders]))
    simp [ori3, h1, show ¬ y < z by omega, show ¬ x < z by omega, this]
  · have := forced_color M (show y < x by omega) h3 hz hb ha hc true (hcase (b, a, c, true) (by simp [sixOrders]))
    simp [ori3, show ¬ x < y by omega, h3, this]
  · have := forced_color M h2 (show z < x by omega) hx hb hc ha false
      (hcase (b, c, a, false) (by simp [sixOrders]))
    simp [ori3, show ¬ x < y by omega, show ¬ x < z by omega, h2, this]
  · omega
  · have := forced_color M (show z < y by omega) (show y < x by omega) hx hc hb ha true
      (hcase (c, b, a, true) (by simp [sixOrders]))
    simp [ori3, show ¬ x < y by omega, show ¬ x < z by omega, show ¬ y < z by omega, this]

/-- **4.3.** -/
theorem holds_pos (M : Model) : M.Holds (posClauses ()) := by
  classical
  intro cl hcl
  unfold posClauses at hcl
  obtain ⟨t, ht, hcl⟩ := List.mem_filterMap.1 hcl
  have hd : t.1 ≠ t.2.1 ∧ t.2.1 ≠ t.2.2 ∧ t.1 ≠ t.2.2 := by
    unfold comb3 at ht
    simp only [List.mem_flatMap, List.mem_filterMap] at ht
    obtain ⟨i, -, j, -, k, -, hk⟩ := ht
    split at hk
    · rename_i hijk
      simp only [Option.some.injEq] at hk
      subst hk
      exact ⟨Fin.ne_of_lt hijk.1, Fin.ne_of_lt hijk.2, Fin.ne_of_lt (lt_trans hijk.1 hijk.2)⟩
    · simp at hk
  obtain ⟨hij, hjk, hik⟩ := hd
  dsimp only at hcl
  split at hcl
  · rename_i htt
    simp only [Option.some.injEq] at hcl
    subst hcl
    apply holds_of_owners3 (a := t.1) (b := t.2.1) (c := t.2.2) (by simp)
    intro x y z hx hy hz ha hb hc
    refine ⟨(true, Atom.orient t.1 t.2.1 t.2.2), by simp, ?_⟩
    simp only [Agree, meaning_orient, decide_eq_true_eq]
    exact (ori_iff M hx hy hz ha hb hc).2 (tt_sound M hx hy hz ha hb hc htt)
  · split at hcl
    · rename_i _ htt
      simp only [Option.some.injEq] at hcl
      subst hcl
      apply holds_of_owners3 (a := t.1) (b := t.2.2) (c := t.2.1) (by simp)
      intro x z y hx hz hy ha hc hb
      refine ⟨(false, Atom.orient t.1 t.2.1 t.2.2), by simp, ?_⟩
      simp only [Agree, meaning_orient, decide_eq_false_iff_not]
      rw [ori_iff M hx hy hz ha hb hc]
      have h := tt_sound M hx hz hy ha hc hb htt
      rw [ori3_swap23 M.cup (owner_ne M hij ha hb) (owner_ne M hjk hb hc) (owner_ne M hik ha hc)] at h
      simpa using h
    · simp at hcl

end N66G15

#print axioms N66G15.holds_pos
