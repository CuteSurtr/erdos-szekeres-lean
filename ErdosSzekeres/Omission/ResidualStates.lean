/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8ResidualStates.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: local namespaces, actual real-point geometry, Lean 4.24 and kernel checks.
-/
import ErdosSzekeres.Omission.ResidualRanks
import ErdosSzekeres.Omission.Ferrers

namespace ErdosSzekeres.Omission.ResidualStates
open StateInterface ResidualRanks

noncomputable def column (n : Nat) (cup : Nat→Nat→Nat→Bool) (v i : Nat) : Nat :=
  (Finset.range v).sup (fun u => if i+1≤(labels n cup u v).1 then (labels n cup u v).2 else 0)

theorem column_antitone (n cup v) : Antitone (column n cup v) := by
  intro i j ij
  unfold column
  apply Finset.sup_le
  intro u hu
  by_cases big : j+1≤(labels n cup u v).1
  · have small : i+1≤(labels n cup u v).1 := by omega
    rw [if_pos big]
    exact Finset.le_sup_of_le hu (by rw [if_pos small])
  · rw [if_neg big]; exact Nat.zero_le _

theorem column_le_six (n cup)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (v i) (hv : v<n) : column n cup v i≤6 := by
  unfold column
  apply Finset.sup_le
  intro u hu
  have bounds := label_bounds n cup caps cups u v (Finset.mem_range.mp hu) hv
  split_ifs <;> omega

theorem incoming_iff_column (n cup v i b) (hb : 0<b) :
    Incoming (labels n cup) v (i+1,b) ↔ b≤column n cup v i := by
  classical
  unfold Incoming column
  constructor
  · rintro ⟨u,hu,hcap,hcup⟩
    exact Finset.le_sup_of_le (Finset.mem_range.mpr hu) (by simpa [hcap] using hcup)
  · intro h
    obtain ⟨u,hu,high⟩ := (Finset.le_sup_iff hb).mp h
    by_cases hc : i+1≤(labels n cup u v).1
    · exact ⟨u,Finset.mem_range.mp hu,hc,by simpa [hc] using high⟩
    · simp only [if_neg hc] at high; omega

/-- A maximal (1,6) cell must be attained by an actual incoming pair. Its
exclusion removes precisely the 56 profiles with first height 6 and second <6. -/
theorem top_cell_constraint (n cup)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup)
    (v) (hv : v<n) : column n cup v 0<6 ∨ column n cup v 1=6 := by
  have zero := column_le_six n cup caps cups v 0 hv
  have one := column_le_six n cup caps cups v 1 hv
  by_contra neg
  have six : 6≤column n cup v 0 := by omega
  obtain ⟨u,hu,ha,hb⟩ := (incoming_iff_column n cup v 0 6 (by omega)).mpr six
  have bounds := label_bounds n cup caps cups u v hu hv
  have h2 : (labels n cup u v).2=6 := by omega
  by_cases h1 : (labels n cup u v).1=1
  · exact forbidden_label n cup caps junction u v hu hv (Prod.ext h1 h2)
  · have atTwo : Incoming (labels n cup) v (2,6) := ⟨u,hu,by omega,by omega⟩
    have high := (incoming_iff_column n cup v 1 6 (by omega)).mp atTwo
    omega

abbrev State := { f : Fin 4→Fin 7 // Antitone f ∧ ((f 0).val<6 ∨ (f 1).val=6) }

noncomputable def state (n cup)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup) (v : Fin n) : State :=
  ⟨fun i=>⟨column n cup v i,by have := column_le_six n cup caps cups v i v.isLt; omega⟩,
    ⟨fun i j h=>column_antitone n cup v h,top_cell_constraint n cup caps cups junction v v.isLt⟩⟩

theorem state_injective (n cup)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup) :
    Function.Injective (state n cup caps cups junction) := by
  have separate (u v : Fin n) (huv : u<v) : state n cup caps cups junction u≠state n cup caps cups junction v := by
    intro equal
    have adm := incoming_admissible n cup (labels n cup) (labels_increasing n cup caps) u v huv v.isLt
    have bd := label_bounds n cup caps cups u v huv v.isLt
    let d := labels n cup u v
    let i : Fin 4 := ⟨d.1-1,by dsimp [d]; omega⟩
    have cell : i.val+1=d.1 := by dsimp [i,d]; omega
    have colEqual : column n cup u i=column n cup v i :=
      congrArg Fin.val (congrFun (congrArg Subtype.val equal) i)
    have atV : d.2≤column n cup v i := by
      apply (incoming_iff_column n cup v i d.2 (by dsimp [d]; omega)).mp
      simpa only [cell] using adm.1
    have atU : Incoming (labels n cup) u (i.val+1,d.2) :=
      (incoming_iff_column n cup u i d.2 (by dsimp [d]; omega)).mpr (colEqual ▸ atV)
    exact adm.2 (by simpa only [cell] using atU)
  intro u v equal
  by_contra ne
  rcases lt_or_gt_of_ne ne with h | h
  · exact separate u v h equal
  · exact separate v u h equal.symm

noncomputable def stateList (f : State) : List Nat := List.ofFn (fun i=>(f.val i).val)

def allowed (xs : List Nat) : Bool := decide (xs.getD 0 0<6 ∨ xs.getD 1 0=6)
def profiles : List (List Nat) := (Ferrers.profiles 4 6).filter allowed

theorem stateList_mem (f : State) : stateList f∈profiles := by
  apply List.mem_filter.mpr
  constructor
  · apply Ferrers.profiles_cover
    · exact List.length_ofFn
    · apply List.pairwise_ofFn.mpr
      intro i j hij; exact f.property.1 (le_of_lt hij)
    · intro a ha; obtain ⟨i,rfl⟩ := List.mem_ofFn.mp ha; have := (f.val i).isLt; omega
  · simpa [allowed,stateList] using f.property.2

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem profile_count : profiles.length=154 := by decide +kernel

theorem stateList_injective : Function.Injective stateList := by
  intro f g eq
  have he := List.ofFn_inj.mp eq
  apply Subtype.ext
  funext i; apply Fin.ext; exact congrFun he i

theorem residual_universe_bound (n cup)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup) : n≤154 := by
  classical
  let f : Fin n→{xs : List Nat // xs∈profiles.toFinset} :=
    fun v=>⟨stateList (state n cup caps cups junction v),List.mem_toFinset.mpr (stateList_mem _)⟩
  have inj : Function.Injective f := by
    intro u v he
    exact state_injective n cup caps cups junction
      (stateList_injective (congrArg Subtype.val he))
  have count := Fintype.card_le_of_injective f inj
  rw [Fintype.card_fin,Fintype.card_coe] at count
  exact count.trans ((List.toFinset_card_le profiles).trans_eq profile_count)

/-- The 154-state cover applies to the geometric residual hypotheses, with
actual starting/ending witnesses and a genuine convex-octagon prohibition. -/
theorem geometric_universe_bound {n} (c : Configuration n)
    (caps : ¬(ActualRanks.colorConfig c.cup true).HasNCap 6 (Finset.range n))
    (octagons : ¬HasConvexNGon 8 (Finset.univ.image c.point))
    (junction : NoJunction n c.cup) : n≤154 := by
  apply residual_universe_bound n c.cup caps _ junction
  apply ActualRanks.avoids_of_no_cup
  exact fun h=>octagons (ListGeometry.hasNCup_octagon c h)

end ErdosSzekeres.Omission.ResidualStates
