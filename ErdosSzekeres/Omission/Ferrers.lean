/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, formal/sources/ES8Ferrers.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Catalog data: CC BY 4.0; see docs/THIRD_PARTY.md.
Changes: local namespaces/imports, Lean/Mathlib 4.24 compatibility, kernel-only checks.
-/
import ErdosSzekeres.Omission.BalancedStates
import Mathlib.Data.List.OfFn
import Std.Tactic

namespace ErdosSzekeres.Omission.Ferrers

/-- All decreasing height lists of prescribed length, generated without first
enumerating every function from Fin 5 to Fin 6. -/
def profiles : Nat → Nat → List (List Nat)
  | 0,_ => [[]]
  | n+1,h => (List.range (h+1)).flatMap (fun a => (profiles n a).map (a :: ·))

theorem profiles_cover (n h : Nat) (xs : List Nat) (len : xs.length=n)
    (sorted : xs.Pairwise (fun a b => b ≤ a)) (bounded : ∀ a ∈ xs, a ≤ h) :
    xs ∈ profiles n h := by
  induction n generalizing h xs with
  | zero =>
    have : xs=[] := List.length_eq_zero_iff.mp len
    subst xs
    simp [profiles]
  | succ n ih =>
    cases xs with
    | nil => simp at len
    | cons a xs =>
      have length : xs.length=n := by simpa using len
      have order := List.pairwise_cons.mp sorted
      have tail := ih a xs length order.2 order.1
      have head : a < h+1 := by have := bounded a (by simp); omega
      apply List.mem_flatMap.mpr
      refine ⟨a,List.mem_range.mpr head,?_⟩
      exact List.mem_map.mpr ⟨xs,tail,rfl⟩

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem profile_count : (profiles 5 5).length=252 := by decide +kernel

noncomputable def stateList (f : ErdosSzekeres.Omission.ActualRanks.FerrersState) : List Nat :=
  List.ofFn (fun i => (f.val i).val)

theorem stateList_mem (f : ErdosSzekeres.Omission.ActualRanks.FerrersState) : stateList f ∈ profiles 5 5 := by
  apply profiles_cover
  · exact List.length_ofFn
  · apply List.pairwise_ofFn.mpr
    intro i j hij
    exact f.property (le_of_lt hij)
  · intro a ha
    obtain ⟨i,rfl⟩ := List.mem_ofFn.mp ha
    have := (f.val i).isLt
    omega

theorem stateList_injective : Function.Injective stateList := by
  intro f g equal
  have pointwise := List.ofFn_inj.mp equal
  apply Subtype.ext
  funext i
  apply Fin.ext
  exact congrFun pointwise i

/-- An actual balanced configuration injects into the completely covered
252-entry profile list, without imposing chronology on incomparable states. -/
theorem actual_states_inject (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : ErdosSzekeres.Omission.ActualRanks.Avoids n cup false 7) (cups : ErdosSzekeres.Omission.ActualRanks.Avoids n cup true 7) :
    Function.Injective (fun v : Fin n => stateList (ErdosSzekeres.Omission.ActualRanks.balancedState n cup caps cups v)) :=
  stateList_injective.comp (ErdosSzekeres.Omission.ActualRanks.balancedState_injective n cup caps cups)

/-- The formal cups-caps universe bound, before octagon-specific row cuts. -/
theorem balanced_universe_bound (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : ErdosSzekeres.Omission.ActualRanks.Avoids n cup false 7) (cups : ErdosSzekeres.Omission.ActualRanks.Avoids n cup true 7) :
    n ≤ 252 := by
  classical
  let f : Fin n → {xs : List Nat // xs ∈ (profiles 5 5).toFinset} :=
    fun v => ⟨stateList (ErdosSzekeres.Omission.ActualRanks.balancedState n cup caps cups v),
      List.mem_toFinset.mpr (stateList_mem _)⟩
  have inj : Function.Injective f := by
    intro u v equal
    exact actual_states_inject n cup caps cups (congrArg Subtype.val equal)
  have count := Fintype.card_le_of_injective f inj
  rw [Fintype.card_fin,Fintype.card_coe] at count
  have size : (profiles 5 5).toFinset.card ≤ 252 := by
    calc
      _ ≤ (profiles 5 5).length := List.toFinset_card_le _
      _ = 252 := profile_count
  exact count.trans size


#print axioms profile_count
#print axioms actual_states_inject
end ErdosSzekeres.Omission.Ferrers
