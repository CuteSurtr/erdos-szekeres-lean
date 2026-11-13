/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, formal/sources/ES8BalancedCatalog.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Catalog data: CC BY 4.0; see docs/THIRD_PARTY.md.
Changes: local namespaces/imports, Lean/Mathlib 4.24 compatibility, kernel-only checks.
-/
import ErdosSzekeres.Omission.BalancedCatalogData

namespace ErdosSzekeres.Omission.BalancedCatalog
open ErdosSzekeres.Omission.Ferrers ErdosSzekeres.Omission.ActualRanks

-- Mathlib 4.24's getElem_idxOf uses equality induced by DecidableEq.
local instance : BEq (List Nat) := instBEqOfDecidableEq

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem catalog_length : catalog.length=252 := by decide +kernel

theorem profiles_covered : (profiles 5 5).all (fun xs => catalog.contains xs)=true := by decide +kernel

theorem catalog_covers (xs : List Nat) (member : xs ∈ profiles 5 5) : xs ∈ catalog := by
  have h := List.all_eq_true.mp profiles_covered xs member
  simpa using h

noncomputable def ownerIndex (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (v : Fin n) : Fin 252 :=
  ⟨catalog.idxOf (stateList (balancedState n cup caps cups v)),by
    have member := catalog_covers _ (stateList_mem (balancedState n cup caps cups v))
    have h := List.idxOf_lt_length_iff.mpr member
    rwa [catalog_length] at h⟩

/-- This is the exact source-index interpretation, not a replacement enumeration. -/
theorem ownerIndex_profile (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (v : Fin n) :
    catalog[(ownerIndex n cup caps cups v).val]'(by rw [catalog_length]; exact (ownerIndex n cup caps cups v).isLt)
      = stateList (balancedState n cup caps cups v) := by
  have member := catalog_covers _ (stateList_mem (balancedState n cup caps cups v))
  simpa only [ownerIndex] using
    (List.getElem_idxOf (a := stateList (balancedState n cup caps cups v))
      (l := catalog) (List.idxOf_lt_length_iff.mpr member))

theorem ownerIndex_injective (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) :
    Function.Injective (ownerIndex n cup caps cups) := by
  intro u v equal
  apply actual_states_inject n cup caps cups
  dsimp only
  rw [← ownerIndex_profile n cup caps cups u,← ownerIndex_profile n cup caps cups v]
  simp only [equal]

#print axioms ownerIndex_injective
end ErdosSzekeres.Omission.BalancedCatalog
