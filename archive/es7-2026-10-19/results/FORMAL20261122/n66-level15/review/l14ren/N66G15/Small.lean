import N66G15.Owners

/-!
# N66G15.Small: three fields of `Gaps` (4.11 `fixed`, L6 `lexChoice`, L7 `holes`)

* `holds_fixed`: the first point owns state 0 (empty diagram), the second state 1 (the single cell (1,1)).
* `lexChoice`: for every occupancy, it or its τ-image satisfies LEX (the 27 pairs are τ-pairs, kernel check).
* `holes_le`: with `n ≥ 56` points at most 14 of the states 2..69 are unoccupied (owners are injective).
-/

namespace N66G15
open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.Omission.ActualRanks N66E15

/-! ## 4.11: the fixed states -/

theorem column_zero (cup : ℕ → ℕ → ℕ → Bool) (i : ℕ) : column cup 0 i = 0 := by
  simp [column]

theorem rank_zero_one (cup : ℕ → ℕ → ℕ → Bool) (color : Bool) : rank cup color 0 1 = 2 := by
  have h := length_bounds (rank_attained cup color 0 1 (by decide))
  omega

theorem column_one (cup : ℕ → ℕ → ℕ → Bool) (i : ℕ) : column cup 1 i = if i = 0 then 1 else 0 := by
  unfold column
  rw [Finset.range_one, Finset.sup_singleton]
  simp only [labels, rank_zero_one]
  split_ifs <;> omega

theorem idxOf_zero (cup : ℕ → ℕ → ℕ → Bool) : idxOf cup 0 = 0 := by
  simp only [idxOf, profOf, column_zero]
  decide +kernel

theorem idxOf_one (cup : ℕ → ℕ → ℕ → Bool) : idxOf cup 1 = 1 := by
  simp only [idxOf, profOf, column_one]
  decide +kernel

/-- **4.11.** -/
theorem holds_fixed (M : Model) (hn : 2 ≤ M.n) : M.Holds fixedUnits := by
  intro cl hcl
  simp only [fixedUnits, List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hcl
  rcases hcl with rfl | rfl
  · refine ⟨(true, Atom.sel 0), List.mem_singleton_self _, ?_⟩
    simp only [meaning_sel, decide_eq_true_eq]
    exact ⟨0, by omega, idxOf_zero M.cup⟩
  · refine ⟨(true, Atom.sel 1), List.mem_singleton_self _, ?_⟩
    simp only [meaning_sel, decide_eq_true_eq]
    exact ⟨1, by omega, idxOf_one M.cup⟩

/-! ## L6: LEX for an occupancy or its τ-image -/

theorem sbPairs_tau_check :
    sbPairs.all (fun p => decide (tau p.1 = p.2) && decide (tau p.2 = p.1)) = true := by decide +kernel

theorem tau_pair {p : Fin 70 × Fin 70} (hp : p ∈ sbPairs) : tau p.1 = p.2 ∧ tau p.2 = p.1 := by
  have h := List.all_eq_true.1 sbPairs_tau_check p hp
  simp only [Bool.and_eq_true, decide_eq_true_eq] at h
  exact h

theorem mem_of_getElem_mem {j : ℕ} {p : Fin 70 × Fin 70} (hp : p ∈ sbPairs[j]?) : p ∈ sbPairs :=
  List.mem_of_getElem? hp

/-- **L6.** -/
theorem lexChoice (x : Fin 70 → Prop) : LexOcc x ∨ LexOcc (fun s => x (tau s)) := by
  classical
  by_cases hall : ∀ j : ℕ, ∀ p : Fin 70 × Fin 70, p ∈ sbPairs[j]? → (x p.1 ↔ x p.2)
  · left
    intro j p hp _ h1
    exact (hall j p hp).1 h1
  · have hex : ∃ j : ℕ, ∃ p : Fin 70 × Fin 70, p ∈ sbPairs[j]? ∧ ¬ (x p.1 ↔ x p.2) := by
      by_contra hno
      apply hall
      intro j p hp
      by_contra hne
      exact hno ⟨j, p, hp, hne⟩
    obtain ⟨p0, hp0, hd0⟩ := Nat.find_spec hex
    have hmin : ∀ t < Nat.find hex, ∀ q : Fin 70 × Fin 70, q ∈ sbPairs[t]? → (x q.1 ↔ x q.2) := by
      intro t ht q hq
      by_contra h
      exact Nat.find_min hex ht ⟨q, hq, h⟩
    have huniq : ∀ {q : Fin 70 × Fin 70}, q ∈ sbPairs[Nat.find hex]? → q = p0 := fun hq =>
      Option.some.inj (hq.symm.trans hp0)
    by_cases hs : x p0.1
    · right
      have ht : ¬ x p0.2 := fun h => hd0 ⟨fun _ => h, fun _ => hs⟩
      intro j p hp hagree h1
      obtain ⟨hp1, hp2⟩ := tau_pair (mem_of_getElem_mem hp)
      simp only [hp1, hp2] at h1 ⊢
      rcases lt_trichotomy j (Nat.find hex) with hj | hj | hj
      · exact (hmin j hj p hp).2 h1
      · subst hj
        rw [huniq hp] at h1
        exact absurd h1 ht
      · have hq := hagree (Nat.find hex) hj p0 hp0
        obtain ⟨hq1, hq2⟩ := tau_pair (mem_of_getElem_mem hp0)
        simp only [hq1, hq2] at hq
        exact absurd hq.symm hd0
    · left
      intro j p hp hagree h1
      rcases lt_trichotomy j (Nat.find hex) with hj | hj | hj
      · exact (hmin j hj p hp).1 h1
      · subst hj
        rw [huniq hp] at h1
        exact absurd h1 hs
      · exact absurd (hagree (Nat.find hex) hj p0 hp0) hd0

/-! ## L7: at most 14 holes -/

/-- **L7.** -/
theorem holes_le (M : Model) (hn : 56 ≤ M.n) : M.holes ≤ 14 := by
  classical
  let q : ℕ → Prop := fun i => ¬ M.occ ⟨(i + 2) % 70, Nat.mod_lt _ (by decide)⟩
  let H : Finset ℕ := (((List.range 68).filter (fun i => decide (q i))).map (· + 2)).toFinset
  let O : Finset ℕ := ((List.range M.n).map (idxOf M.cup)).toFinset
  have hHcard : H.card = M.holes := by
    have hnd : (((List.range 68).filter (fun i => decide (q i))).map (· + 2)).Nodup :=
      ((List.nodup_range).filter _).map (fun a b h => by simpa using h)
    rw [List.toFinset_card_of_nodup hnd, List.length_map]
    rfl
  have hOcard : O.card = M.n := by
    have hnd : ((List.range M.n).map (idxOf M.cup)).Nodup := by
      apply List.Nodup.map_on _ List.nodup_range
      intro u hu v hv h
      exact idxOf_injective M (List.mem_range.1 hu) (List.mem_range.1 hv) h
    rw [List.toFinset_card_of_nodup hnd, List.length_map, List.length_range]
  have hdisj : Disjoint H O := by
    rw [Finset.disjoint_left]
    intro x hxH hxO
    simp only [H, List.mem_toFinset, List.mem_map, List.mem_filter, List.mem_range, decide_eq_true_eq] at hxH
    simp only [O, List.mem_toFinset, List.mem_map, List.mem_range] at hxO
    obtain ⟨i, ⟨hi, hq⟩, rfl⟩ := hxH
    obtain ⟨v, hv, hve⟩ := hxO
    apply hq
    refine ⟨v, hv, ?_⟩
    rw [hve]
    simp only [Nat.mod_eq_of_lt (show i + 2 < 70 by omega)]
  have hsub : H ∪ O ⊆ Finset.range 70 := by
    intro x hx
    rw [Finset.mem_union] at hx
    rw [Finset.mem_range]
    rcases hx with hx | hx
    · simp only [H, List.mem_toFinset, List.mem_map, List.mem_filter, List.mem_range] at hx
      obtain ⟨i, ⟨hi, _⟩, rfl⟩ := hx
      omega
    · simp only [O, List.mem_toFinset, List.mem_map, List.mem_range] at hx
      obtain ⟨v, hv, rfl⟩ := hx
      exact idxOf_lt M hv
  have := Finset.card_le_card hsub
  rw [Finset.card_union_of_disjoint hdisj, Finset.card_range, hHcard, hOcard] at this
  omega

end N66G15

#print axioms N66G15.holds_fixed
#print axioms N66G15.lexChoice
#print axioms N66G15.holes_le
