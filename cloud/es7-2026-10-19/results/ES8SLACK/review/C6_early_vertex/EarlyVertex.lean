import ErdosSzekeres.Omission.CycleGeometry
import ErdosSzekeres.Omission.ResidualCycleGeometry

/-!
Independent kernel check of claim C6 (early-vertex occupancy), stated against the repository's own
owner maps `BalancedCatalog.ownerIndex` / `ResidualCatalog.ownerIndex` and occupied sets
`Configuration.occupied` / `Configuration.residualOccupied` (the sets used by `feasible_holes` and by
`residual_bound_of_excludes2650`).
-/

open ErdosSzekeres ErdosSzekeres.Omission

namespace C6Check

-- same instance as in BalancedCatalog / ResidualCatalog (used inside `ownerIndex`)
local instance : BEq (List Nat) := instBEqOfDecidableEq

section ranks
open ActualRanks

theorem ending_from_zero {cup : Nat → Nat → Nat → Bool} {color : Bool} {v l : Nat}
    (p : EndingPath cup color 0 v l) : l = 2 := by
  cases p with
  | pair _ => rfl
  | @step t u v l path huv same =>
    have := (length_bounds path).2.2
    omega

theorem rank_zero_left (cup : Nat → Nat → Nat → Bool) (color : Bool) (v : Nat) (hv : 0 < v) :
    rank cup color 0 v = 2 :=
  ending_from_zero (rank_attained cup color 0 v hv)

theorem ending_one_two {cup : Nat → Nat → Nat → Bool} {color : Bool} {l : Nat}
    (p : EndingPath cup color 1 2 l) : l = 2 ∨ (l = 3 ∧ cup 0 1 2 = color) := by
  cases p with
  | pair _ => exact Or.inl rfl
  | @step t u v l path huv same =>
    have hb := (length_bounds path).2.2
    have ht : t = 0 := by omega
    subst ht
    have := ending_from_zero path
    exact Or.inr ⟨by omega, same⟩

theorem rank_one_two (cup : Nat → Nat → Nat → Bool) (color : Bool) :
    rank cup color 1 2 = if cup 0 1 2 = color then 3 else 2 := by
  rcases ending_one_two (rank_attained cup color 1 2 (by omega)) with h | ⟨h, hc⟩
  · split_ifs with hc
    · have p3 : EndingPath cup color 1 2 3 :=
        EndingPath.step (EndingPath.pair (by omega : (0:Nat) < 1)) (by omega) hc
      have := rank_ge p3
      omega
    · exact h
  · rw [if_pos hc]; exact h

theorem labels_zero_left (cup : Nat → Nat → Nat → Bool) (v : Nat) (hv : 0 < v) :
    labels cup 0 v = (1, 1) := by
  simp [labels, rank_zero_left cup _ v hv]

theorem labels_one_two (cup : Nat → Nat → Nat → Bool) :
    labels cup 1 2 = if cup 0 1 2 = false then (2, 1) else (1, 2) := by
  unfold labels
  rw [rank_one_two cup false, rank_one_two cup true]
  cases cup 0 1 2 <;> simp

theorem column_vertex0 (cup : Nat → Nat → Nat → Bool) (i : Nat) : column cup 0 i = 0 := by
  simp [column]

theorem column_vertex1 (cup : Nat → Nat → Nat → Bool) (i : Nat) :
    column cup 1 i = if i = 0 then 1 else 0 := by
  unfold column
  rw [Finset.range_one, Finset.sup_singleton, labels_zero_left cup 1 (by omega)]
  by_cases hi : i = 0
  · subst hi; simp
  · rw [if_neg hi, if_neg (by simp; omega)]

theorem column_vertex2 (cup : Nat → Nat → Nat → Bool) (i : Nat) :
    column cup 2 i =
      max (if i + 1 ≤ (labels cup 1 2).1 then (labels cup 1 2).2 else 0)
        (if i + 1 ≤ 1 then 1 else 0) := by
  unfold column
  rw [Finset.range_add_one, Finset.range_one, Finset.sup_insert, Finset.sup_singleton,
    labels_zero_left cup 2 (by omega)]

end ranks

section balanced
open ActualRanks

theorem stateList_vertex0 (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (h : 0 < n) :
    Ferrers.stateList (balancedState n cup caps cups ⟨0, h⟩) = [0, 0, 0, 0, 0] := by
  simp [Ferrers.stateList, balancedState, List.ofFn_succ, column_vertex0]

theorem stateList_vertex1 (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (h : 1 < n) :
    Ferrers.stateList (balancedState n cup caps cups ⟨1, h⟩) = [1, 0, 0, 0, 0] := by
  simp [Ferrers.stateList, balancedState, List.ofFn_succ, column_vertex1]

theorem stateList_vertex2 (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (h : 2 < n) :
    Ferrers.stateList (balancedState n cup caps cups ⟨2, h⟩) =
      (if cup 0 1 2 = false then [1, 1, 0, 0, 0] else [2, 0, 0, 0, 0]) := by
  cases hc : cup 0 1 2 <;>
    simp [Ferrers.stateList, balancedState, List.ofFn_succ, column_vertex2, labels_one_two, hc]

theorem owner0 (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (h : 0 < n) :
    BalancedCatalog.ownerIndex n cup caps cups ⟨0, h⟩ = 0 := by
  apply Fin.ext
  change BalancedCatalog.catalog.idxOf (Ferrers.stateList (balancedState n cup caps cups ⟨0, h⟩)) = 0
  rw [stateList_vertex0]
  decide +kernel

theorem owner1 (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (h : 1 < n) :
    BalancedCatalog.ownerIndex n cup caps cups ⟨1, h⟩ = 1 := by
  apply Fin.ext
  change BalancedCatalog.catalog.idxOf (Ferrers.stateList (balancedState n cup caps cups ⟨1, h⟩)) = 1
  rw [stateList_vertex1]
  decide +kernel

theorem owner2 (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (h : 2 < n) :
    BalancedCatalog.ownerIndex n cup caps cups ⟨2, h⟩ = (if cup 0 1 2 = false then 2 else 3) := by
  apply Fin.ext
  change BalancedCatalog.catalog.idxOf (Ferrers.stateList (balancedState n cup caps cups ⟨2, h⟩)) = _
  rw [stateList_vertex2]
  cases cup 0 1 2
  · decide +kernel
  · decide +kernel

/-- C6, balanced part, at the level of the occupied set used by `OmissionBalanced.feasible_holes`. -/
theorem balanced_early_occupancy {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7) (h : 2 < n) :
    (0 : Fin 252) ∈ c.occupied noCap noCup ∧ (1 : Fin 252) ∈ c.occupied noCap noCup ∧
      ((2 : Fin 252) ∈ c.occupied noCap noCup ∨ (3 : Fin 252) ∈ c.occupied noCap noCup) := by
  have m : ∀ v : Fin n, c.balancedOwner noCap noCup v ∈ c.occupied noCap noCup :=
    fun v => Finset.mem_image.mpr ⟨v, Finset.mem_univ _, rfl⟩
  refine ⟨?_, ?_, ?_⟩
  · have e := owner0 n c.cup (c.avoids_of_noCap noCap) (c.avoids_of_noCup noCup) (by omega)
    have := m ⟨0, by omega⟩
    rwa [Configuration.balancedOwner, e] at this
  · have e := owner1 n c.cup (c.avoids_of_noCap noCap) (c.avoids_of_noCup noCup) (by omega)
    have := m ⟨1, by omega⟩
    rwa [Configuration.balancedOwner, e] at this
  · have e := owner2 n c.cup (c.avoids_of_noCap noCap) (c.avoids_of_noCup noCup) h
    have := m ⟨2, h⟩
    rw [Configuration.balancedOwner, e] at this
    split_ifs at this
    · exact Or.inl this
    · exact Or.inr this

/-- The same statement for the literal hole vector of `feasible_holes`:
`h_0 = 0`, `h_1 = 0`, `h_2 + h_3 ≤ 1`. -/
theorem balanced_early_holes {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7) (h : 2 < n) :
    let holes : Fin 252 → ℕ := fun i => if i ∈ c.occupied noCap noCup then 0 else 1
    holes 0 = 0 ∧ holes 1 = 0 ∧ holes 2 + holes 3 ≤ 1 := by
  intro holes
  obtain ⟨h0, h1, h23⟩ := balanced_early_occupancy c noCap noCup h
  refine ⟨by simp [holes, h0], by simp [holes, h1], ?_⟩
  rcases h23 with h2 | h3
  · simp only [holes, if_pos h2]; split_ifs <;> omega
  · simp only [holes, if_pos h3]; split_ifs <;> omega

end balanced

section residual
open ActualRanks

theorem res_column_vertex1 (n : Nat) (cup : Nat → Nat → Nat → Bool) (i : Nat) :
    ResidualStates.column n cup 1 i =
      if i + 1 ≤ 6 - ResidualRanks.rank n cup false 0 1 then 1 else 0 := by
  unfold ResidualStates.column
  rw [Finset.range_one, Finset.sup_singleton]
  simp only [ResidualRanks.labels, rank_zero_left cup true 1 (by omega)]

theorem res_rank01_bounds (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n)) (h : 1 < n) :
    2 ≤ ResidualRanks.rank n cup false 0 1 ∧ ResidualRanks.rank n cup false 0 1 < 6 :=
  ⟨(ResidualRanks.path_bounds (ResidualRanks.rank_attained n cup false 0 1 (by omega) h)).1,
   ResidualRanks.rank_lt_no_cap n cup 0 1 caps (by omega) h⟩

theorem res_owner1 (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : ResidualRanks.NoJunction n cup) (h : 1 < n) :
    (ResidualCatalog.ownerIndex n cup caps cups junction ⟨1, h⟩).val = 1 ∨
    (ResidualCatalog.ownerIndex n cup caps cups junction ⟨1, h⟩).val = 2 ∨
    (ResidualCatalog.ownerIndex n cup caps cups junction ⟨1, h⟩).val = 4 ∨
    (ResidualCatalog.ownerIndex n cup caps cups junction ⟨1, h⟩).val = 7 := by
  have hb := res_rank01_bounds n cup caps h
  have hs : ResidualStates.stateList (ResidualStates.state n cup caps cups junction ⟨1, h⟩) ++ [0] =
      List.ofFn (fun i : Fin 4 =>
        if i.val + 1 ≤ 6 - ResidualRanks.rank n cup false 0 1 then 1 else 0) ++ [0] := by
    simp only [ResidualStates.stateList, ResidualStates.state, res_column_vertex1]
  change ResidualCatalog.catalog.idxOf
      (ResidualStates.stateList (ResidualStates.state n cup caps cups junction ⟨1, h⟩) ++ [0]) = 1 ∨
    ResidualCatalog.catalog.idxOf
      (ResidualStates.stateList (ResidualStates.state n cup caps cups junction ⟨1, h⟩) ++ [0]) = 2 ∨
    ResidualCatalog.catalog.idxOf
      (ResidualStates.stateList (ResidualStates.state n cup caps cups junction ⟨1, h⟩) ++ [0]) = 4 ∨
    ResidualCatalog.catalog.idxOf
      (ResidualStates.stateList (ResidualStates.state n cup caps cups junction ⟨1, h⟩) ++ [0]) = 7
  rw [hs]
  generalize ResidualRanks.rank n cup false 0 1 = F at hb ⊢
  obtain ⟨lo, hi⟩ := hb
  have hF : F = 2 ∨ F = 3 ∨ F = 4 ∨ F = 5 := by omega
  rcases hF with rfl | rfl | rfl | rfl
  · right; right; right; decide +kernel
  · right; right; left; decide +kernel
  · right; left; decide +kernel
  · left; decide +kernel

/-- C6, residual part, at the level of `Configuration.residualOccupied` (the occupied set used by
`residual_bound_of_excludes2650`). -/
theorem residual_early_occupancy {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (h : 1 < n) :
    (1 : Fin 154) ∈ c.residualOccupied noCap noOctagon noJunction ∨
    (2 : Fin 154) ∈ c.residualOccupied noCap noOctagon noJunction ∨
    (4 : Fin 154) ∈ c.residualOccupied noCap noOctagon noJunction ∨
    (7 : Fin 154) ∈ c.residualOccupied noCap noOctagon noJunction := by
  have m : c.residualOwner noCap noOctagon noJunction ⟨1, h⟩ ∈
      c.residualOccupied noCap noOctagon noJunction :=
    Finset.mem_image.mpr ⟨⟨1, h⟩, Finset.mem_univ _, rfl⟩
  have e := res_owner1 n c.cup (fun hh => noCap (ListGeometry.hasCap_of_list c hh))
    (c.residual_avoids_cup noOctagon) (ResidualRanks.noJunction_of_lists n c.cup noJunction) h
  unfold Configuration.residualOwner at m
  generalize ResidualCatalog.ownerIndex n c.cup (fun hh => noCap (ListGeometry.hasCap_of_list c hh))
    (c.residual_avoids_cup noOctagon) (ResidualRanks.noJunction_of_lists n c.cup noJunction) ⟨1, h⟩ = k
    at m e
  rcases e with e | e | e | e
  · left; have : k = 1 := Fin.ext e
    exact this ▸ m
  · right; left; have : k = 2 := Fin.ext e
    exact this ▸ m
  · right; right; left; have : k = 4 := Fin.ext e
    exact this ▸ m
  · right; right; right; have : k = 7 := Fin.ext e
    exact this ▸ m

end residual

#print axioms balanced_early_occupancy
#print axioms balanced_early_holes
#print axioms residual_early_occupancy

end C6Check
