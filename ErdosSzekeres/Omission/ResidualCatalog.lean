/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8ResidualCatalog.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: local namespaces, actual real-point geometry, Lean 4.24 and kernel checks.
-/
import ErdosSzekeres.Omission.ResidualCatalogData

namespace ErdosSzekeres.Omission.ResidualCatalog
open StateInterface ResidualRanks ResidualStates

local instance : BEq (List Nat) := instBEqOfDecidableEq

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem catalog_length : catalog.length=154 := by decide +kernel

theorem profiles_covered : profiles.all (fun xs=>catalog.contains (xs++[0]))=true := by decide +kernel

theorem catalog_covers (f : ResidualStates.State) : stateList f++[0]∈catalog := by
  have h := List.all_eq_true.mp profiles_covered (stateList f) (stateList_mem f)
  simpa using h

noncomputable def ownerIndex (n cup)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup) (v : Fin n) : Fin 154 :=
  ⟨catalog.idxOf (stateList (state n cup caps cups junction v)++[0]),by
    have h := List.idxOf_lt_length_iff.mpr (catalog_covers (state n cup caps cups junction v))
    rwa [catalog_length] at h⟩

theorem ownerIndex_profile (n cup)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup) (v : Fin n) :
    catalog[(ownerIndex n cup caps cups junction v).val]'(by rw [catalog_length]; exact (ownerIndex n cup caps cups junction v).isLt)
      = stateList (state n cup caps cups junction v)++[0] := by
  have member := catalog_covers (state n cup caps cups junction v)
  simpa only [ownerIndex] using
    (List.getElem_idxOf (a := stateList (state n cup caps cups junction v)++[0])
      (l := catalog) (List.idxOf_lt_length_iff.mpr member))

theorem ownerIndex_injective (n cup)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup) :
    Function.Injective (ownerIndex n cup caps cups junction) := by
  intro u v eq
  apply state_injective n cup caps cups junction
  apply stateList_injective
  have h : stateList (state n cup caps cups junction u)++[0]=stateList (state n cup caps cups junction v)++[0] := by
    rw [←ownerIndex_profile n cup caps cups junction u,←ownerIndex_profile n cup caps cups junction v]
    simp only [eq]
  exact List.append_cancel_right h

end ErdosSzekeres.Omission.ResidualCatalog
