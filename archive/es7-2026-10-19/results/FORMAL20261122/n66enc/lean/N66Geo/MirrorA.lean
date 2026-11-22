import N66Geo.Final5

/-!
# N66Geo.MirrorA: negating the triple colors swaps the labels and transposes the states (combinatorial half of G4)

If `cup' i j k = !cup i j k` on every increasing triple below `n`, then paths swap colors, so ranks and labels swap
coordinates (`labels_swap`), the incoming state of every point is transposed, and its column heights are the
conjugate partition (`column_swap`): `column cup' v i = #{a < 4 : i + 1 ≤ column cup v a}` when labels are ≤ 4.
-/

namespace N66Geo
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks N66Enc

variable {n : ℕ} {cup cup' : ℕ → ℕ → ℕ → Bool}

theorem endingPath_swap (hneg : ∀ i j k, i < j → j < k → k < n → cup' i j k = !cup i j k) :
    ∀ {color : Bool} {u v l : ℕ}, v < n → (EndingPath cup' color u v l ↔ EndingPath cup (!color) u v l) := by
  intro color u v l hv
  constructor
  · intro h
    induction h with
    | pair huv => exact .pair huv
    | @step t u v l path huv same ih =>
      have htu := (length_bounds path).2.2
      exact .step (ih (lt_trans huv hv)) huv (by rw [← same, hneg t u v htu huv hv]; simp)
  · intro h
    induction h with
    | pair huv => exact .pair huv
    | @step t u v l path huv same ih =>
      have htu := (length_bounds path).2.2
      exact .step (ih (lt_trans huv hv)) huv (by rw [hneg t u v htu huv hv, same]; simp)

theorem rank_swap (hneg : ∀ i j k, i < j → j < k → k < n → cup' i j k = !cup i j k) {color : Bool} {u v : ℕ}
    (hv : v < n) : rank cup' color u v = rank cup (!color) u v := by
  classical
  have hl : lengths cup' color u v = lengths cup (!color) u v := by
    unfold lengths
    apply Finset.filter_congr
    intro l _
    exact endingPath_swap hneg hv
  unfold rank
  split
  · rename_i huv
    simp only [hl]
  · rfl

theorem labels_swap (hneg : ∀ i j k, i < j → j < k → k < n → cup' i j k = !cup i j k) {u v : ℕ} (hv : v < n) :
    labels cup' u v = ((labels cup u v).2, (labels cup u v).1) := by
  unfold labels
  rw [rank_swap hneg hv, rank_swap hneg hv]
  rfl

/-- `column cup v a ≥ i + 1` iff some earlier point gives a label with cap coordinate ≥ a+1 and cup ≥ i+1. -/
theorem column_ge_iff (cup : ℕ → ℕ → ℕ → Bool) (v a i : ℕ) :
    i + 1 ≤ column cup v a ↔ ∃ u < v, a + 1 ≤ (labels cup u v).1 ∧ i + 1 ≤ (labels cup u v).2 := by
  classical
  unfold column
  rw [Finset.le_sup_iff (show (⊥ : ℕ) < i + 1 from Nat.succ_pos i)]
  constructor
  · rintro ⟨u, hu, h⟩
    split at h
    · exact ⟨u, Finset.mem_range.1 hu, by assumption, h⟩
    · omega
  · rintro ⟨u, hu, h1, h2⟩
    exact ⟨u, Finset.mem_range.2 hu, by rw [if_pos h1]; exact h2⟩

/-- **Conjugate columns.** With labels bounded by 4 in both coordinates, the swapped column heights are the
conjugate partition of the original ones. -/
theorem column_swap (hneg : ∀ i j k, i < j → j < k → k < n → cup' i j k = !cup i j k) {v : ℕ} (hv : v < n)
    (hb : ∀ u < v, (labels cup u v).1 ≤ 4) (i : ℕ) :
    column cup' v i = ((List.range 4).filter (fun a => decide (i + 1 ≤ column cup v a))).length := by
  classical
  set G := column cup' v i with hG
  -- G is the largest cap coordinate among labels with cup coordinate ≥ i+1
  have hGle : G ≤ 4 := by
    rw [hG]; unfold column
    apply Finset.sup_le
    intro u hu
    rw [labels_swap hneg hv]
    have := hb u (Finset.mem_range.1 hu)
    split <;> omega
  have key : ∀ a, (i + 1 ≤ column cup v a ↔ a < G) := by
    intro a
    rw [column_ge_iff]
    constructor
    · rintro ⟨u, hu, h1, h2⟩
      have : (labels cup u v).1 ≤ G := by
        rw [hG]; unfold column
        have := Finset.le_sup (f := fun u => if i + 1 ≤ (labels cup' u v).1 then (labels cup' u v).2 else 0)
          (Finset.mem_range.2 hu)
        dsimp only at this
        rw [labels_swap hneg hv] at this
        simp only [if_pos h2] at this
        exact this
      omega
    · intro haG
      have hpos : 0 < G := by omega
      obtain ⟨u, hu, hmax⟩ := Finset.exists_mem_eq_sup (Finset.range v)
        (Finset.nonempty_range_iff.2 (by
          intro h0; subst h0; rw [hG] at hpos; simp [column] at hpos))
        (fun u => if i + 1 ≤ (labels cup' u v).1 then (labels cup' u v).2 else 0)
      have hGu : G = (if i + 1 ≤ (labels cup' u v).1 then (labels cup' u v).2 else 0) := by
        rw [hG]; exact hmax
      rw [labels_swap hneg hv] at hGu
      simp only at hGu
      split at hGu
      · exact ⟨u, Finset.mem_range.1 hu, by omega, by assumption⟩
      · omega
  have hfilter : (List.range 4).filter (fun a => decide (i + 1 ≤ column cup v a)) = List.range G := by
    have : (List.range 4).filter (fun a => decide (i + 1 ≤ column cup v a)) =
        (List.range 4).filter (fun a => decide (a < G)) := by
      apply List.filter_congr
      intro a _
      simp only [decide_eq_decide]
      exact key a
    rw [this]
    rcases (show G = 0 ∨ G = 1 ∨ G = 2 ∨ G = 3 ∨ G = 4 by omega) with h | h | h | h | h <;>
      rw [h] <;> decide
  rw [hfilter, List.length_range]

end N66Geo

#print axioms N66Geo.labels_swap
#print axioms N66Geo.column_swap
