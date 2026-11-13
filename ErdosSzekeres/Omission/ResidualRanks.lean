/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8ResidualRanks.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: local namespaces, actual real-point geometry, Lean 4.24 and kernel checks.
-/
import ErdosSzekeres.Omission.ListGeometry
import ErdosSzekeres.Omission.Subsets

namespace ErdosSzekeres.Omission.ResidualRanks
open StateInterface ActualRanks

/-- Actual paths starting at the exact ordered pair, entirely within the same
ambient finite configuration. The upper bound on the final vertex is explicit. -/
inductive StartingPath (n : Nat) (cup : Nat→Nat→Nat→Bool) (color : Bool) : Nat→Nat→Nat→Prop
  | pair {u v} : u<v → v<n → StartingPath n cup color u v 2
  | step {u v w len} : StartingPath n cup color v w len → u<v → cup u v w=color →
      StartingPath n cup color u v (len+1)

theorem path_bounds {n cup color u v len} (p : StartingPath n cup color u v len) :
    2≤len ∧ len+u≤n ∧ u<v ∧ v<n := by
  induction p with
  | pair huv hvn => omega
  | step path huv same ih => omega

theorem list_witness {n cup color u v len} (p : StartingPath n cup color u v len) :
    ∃ xs, (u::v::xs).length=len ∧ (colorConfig cup color).Cup (u::v::xs) ∧
      (u::v::xs).In (Finset.range n) := by
  induction p with
  | @pair u v huv hvn =>
    refine ⟨[],rfl,?_,?_⟩
    · exact ⟨by simpa using huv,by simp [List.Chain3']⟩
    · intro a ha; simp only [List.mem_cons,List.not_mem_nil,or_false] at ha
      exact Finset.mem_range.mpr (by rcases ha with rfl | rfl <;> omega)
  | @step u v w len path huv same ih =>
    obtain ⟨xs,hxs,chain,inside⟩ := ih
    refine ⟨w::xs,by simpa using congrArg (fun x : Nat=>x+1) hxs,?_,?_⟩
    · exact ⟨List.isChain_cons_cons.mpr ⟨huv,chain.1⟩,
        List.chain3'_cons.mpr ⟨same,chain.2⟩⟩
    · intro a ha
      rcases List.mem_cons.mp ha with rfl | ha
      · exact Finset.mem_range.mpr (by have := path_bounds path; omega)
      · exact inside a ha

/-- Prefix shortening preserves the starting pair; no witness is borrowed from
a different ambient set. -/
theorem truncate {n cup color u v len} (p : StartingPath n cup color u v len)
    (m : Nat) (lo : 2≤m) (hi : m≤len) : StartingPath n cup color u v m := by
  induction p generalizing m with
  | pair huv hvn =>
    have he : m=2 := by omega
    subst m
    exact .pair huv hvn
  | @step u v w len path huv same ih =>
    by_cases h : m=2
    · subst m; exact .pair huv (by have := path_bounds path; omega)
    · have small := ih (m-1) (by omega) (by omega)
      have he : m-1+1=m := by omega
      simpa only [he] using StartingPath.step small huv same

noncomputable def lengths (n : Nat) (cup : Nat→Nat→Nat→Bool) (color : Bool) (u v : Nat) : Finset Nat := by
  classical
  exact (Finset.range (n+1)).filter (StartingPath n cup color u v)

theorem mem_lengths {n cup color u v len} :
    len∈lengths n cup color u v ↔ StartingPath n cup color u v len := by
  classical
  simp only [lengths,Finset.mem_filter,Finset.mem_range]
  exact ⟨And.right,fun p=>⟨by have := path_bounds p; omega,p⟩⟩

theorem lengths_nonempty (n cup color u v) (huv : u<v) (hvn : v<n) :
    (lengths n cup color u v).Nonempty := ⟨2,mem_lengths.mpr (.pair huv hvn)⟩

noncomputable def rank (n : Nat) (cup : Nat→Nat→Nat→Bool) (color : Bool) (u v : Nat) : Nat :=
  if h : u<v ∧ v<n then (lengths n cup color u v).max' (lengths_nonempty n cup color u v h.1 h.2) else 0

theorem rank_attained (n cup color u v) (huv : u<v) (hvn : v<n) :
    StartingPath n cup color u v (rank n cup color u v) := by
  classical
  unfold rank; rw [dif_pos ⟨huv,hvn⟩]
  exact mem_lengths.mp (Finset.max'_mem _ _)

theorem rank_ge {n cup color u v len} (p : StartingPath n cup color u v len) : len≤rank n cup color u v := by
  classical
  have bounds := path_bounds p
  unfold rank; rw [dif_pos ⟨bounds.2.2.1,bounds.2.2.2⟩]
  exact Finset.le_max' _ _ (mem_lengths.mpr p)

theorem rank_growth (n cup color u v w) (huv : u<v) (hvw : v<w) (hwn : w<n) (same : cup u v w=color) :
    rank n cup color v w < rank n cup color u v := by
  have := rank_ge (StartingPath.step (rank_attained n cup color v w hvw hwn) huv same)
  omega

theorem rank_lt_no_cap (n cup u v) (noCap : ¬(colorConfig cup true).HasNCap 6 (Finset.range n))
    (huv : u<v) (hvn : v<n) : rank n cup false u v<6 := by
  by_contra high
  have p := truncate (rank_attained n cup false u v huv hvn) 6 (by omega) (by omega)
  obtain ⟨xs,len,chain,inside⟩ := list_witness p
  exact noCap ⟨u::v::xs,⟨(false_cup_iff_cap cup _).mp chain,len⟩,inside⟩

/-- Two-sided ranks: reversed future-cap length and actual past-cup length. -/
noncomputable def labels (n : Nat) (cup : Nat→Nat→Nat→Bool) (u v : Nat) : Label :=
  (6-rank n cup false u v, ActualRanks.rank cup true u v-1)

theorem label_bounds (n cup)
    (noCap : ¬(colorConfig cup true).HasNCap 6 (Finset.range n)) (noCup : Avoids n cup true 8)
    (u v) (huv : u<v) (hvn : v<n) :
    1≤(labels n cup u v).1 ∧ (labels n cup u v).1≤4 ∧
    1≤(labels n cup u v).2 ∧ (labels n cup u v).2≤6 := by
  have a := rank_lt_no_cap n cup u v noCap huv hvn
  have b := (path_bounds (rank_attained n cup false u v huv hvn)).1
  have c := rank_lt_of_avoids n cup true 8 (by omega) noCup u v huv hvn
  have d := (ActualRanks.length_bounds (ActualRanks.rank_attained cup true u v huv)).1
  simp only [labels]; omega

theorem labels_increasing (n cup)
    (noCap : ¬(colorConfig cup true).HasNCap 6 (Finset.range n)) :
    IncreasingLabels n cup (labels n cup) := by
  intro u v w huv hvw hwn
  constructor
  · intro same
    have growth := rank_growth n cup false u v w huv hvw hwn same
    have top := rank_lt_no_cap n cup u v noCap huv (by omega)
    simp only [labels]; omega
  · intro same
    have growth := ActualRanks.rank_growth cup true u v w huv hvw same
    have low := (ActualRanks.length_bounds (ActualRanks.rank_attained cup true u v huv)).1
    simp only [labels]; omega

/-- Both witnesses share their actual junction vertex inside this ambient set. -/
def NoJunction (n : Nat) (cup : Nat→Nat→Nat→Bool) : Prop :=
  ∀ t u v, u<n → ¬(EndingPath cup true t u 6 ∧ StartingPath n cup false u v 5)

theorem ending_seven_prefix {cup u v} (p : EndingPath cup true u v 7) :
    ∃ t, EndingPath cup true t u 6 := by
  cases p with
  | step path _ _ => exact ⟨_,path⟩

/-- The critical label is impossible because its two attained ranks provide
the forbidden six-cup/five-cap junction, after dropping the cup's last point. -/
theorem forbidden_label (n cup)
    (noCap : ¬(colorConfig cup true).HasNCap 6 (Finset.range n))
    (noJunction : NoJunction n cup) (u v) (huv : u<v) (hvn : v<n) :
    labels n cup u v≠(1,6) := by
  intro eq
  have a := congrArg Prod.fst eq
  have b := congrArg Prod.snd eq
  have bounded := rank_lt_no_cap n cup u v noCap huv hvn
  have c : rank n cup false u v=5 := by simp only [labels] at a; omega
  have q : ActualRanks.rank cup true u v=7 := by simp only [labels] at b; omega
  have cap := rank_attained n cup false u v huv hvn
  have cup := ActualRanks.rank_attained cup true u v huv
  rw [c] at cap
  rw [q] at cup
  obtain ⟨t,path⟩ := ending_seven_prefix cup
  exact noJunction t u v (by omega) ⟨path,cap⟩

/-- The partition's concrete no-junction predicate excludes the two attained
paths at the same actual vertex. No rank bound is assumed in this bridge. -/
theorem noJunction_of_lists (n : ℕ) (cup : ℕ → ℕ → ℕ → Bool)
    (avoid : Subsets.NoJunctionOn cup (Finset.range n)) : NoJunction n cup := by
  intro t u v hu pair
  obtain ⟨ending, starting⟩ := pair
  obtain ⟨xs, xl, xc, bounded⟩ := ActualRanks.list_witness ending
  obtain ⟨ys, yl, yc, yi⟩ := list_witness starting
  apply avoid u
  refine ⟨xs, ys, t, v, xl, yl, xc, yc, ?_, yi⟩
  intro a ha
  exact Finset.mem_range.mpr (lt_of_le_of_lt (bounded a ha) hu)

end ErdosSzekeres.Omission.ResidualRanks
