/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8ResidualDomains.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: local namespaces, actual real-point geometry, Lean 4.24 and kernel checks.
-/
import ErdosSzekeres.Omission.ResidualCatalog
import ErdosSzekeres.Omission.Domains

namespace ErdosSzekeres.Omission.ResidualDomains
open StateInterface Domains ResidualRanks ResidualCatalog ResidualStates

def grid : List Label := (List.range 4).flatMap (fun x => (List.range 6).map (fun y => (x+1,y+1)))

def valid (a b : List Nat) (box : Box) : Bool :=
  grid.all (fun z => decide (Contains b z ∧ ¬ Contains a z → Fits box z))

theorem mem_grid (z : Label) (h : 1 ≤ z.1 ∧ z.1 ≤ 4 ∧ 1 ≤ z.2 ∧ z.2 ≤ 6) : z ∈ grid := by
  apply List.mem_flatMap.mpr
  refine ⟨z.1-1,List.mem_range.mpr (by omega),?_⟩
  apply List.mem_map.mpr
  exact ⟨z.2-1,List.mem_range.mpr (by omega),by ext <;> simp <;> omega⟩

theorem valid_sound (a b : List Nat) (box : Box) (ok : valid a b box=true)
    (z : Label) (bounds : 1 ≤ z.1 ∧ z.1 ≤ 4 ∧ 1 ≤ z.2 ∧ z.2 ≤ 6)
    (difference : Contains b z ∧ ¬ Contains a z) : Fits box z := by
  have h := List.all_eq_true.mp ok z (mem_grid z bounds)
  exact of_decide_eq_true h difference

def shape (id : Nat) : List Nat := catalog.getD id []

theorem owner_shape (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup) (v : Fin n) :
    shape (ownerIndex n cup caps cups junction v).val = stateList (state n cup caps cups junction v)++[0] := by
  unfold shape
  rw [List.getD_eq_getElem catalog [] (by rw [catalog_length]; exact (ownerIndex n cup caps cups junction v).isLt)]
  exact ownerIndex_profile n cup caps cups junction v

theorem owner_contains (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup) (v : Fin n)
    (z : Label) (bounds : 1 ≤ z.1 ∧ z.1 ≤ 4 ∧ 1 ≤ z.2 ∧ z.2 ≤ 6) :
    Contains (shape (ownerIndex n cup caps cups junction v).val) z ↔ Incoming (labels n cup) v z := by
  rw [owner_shape]
  unfold Contains stateList
  have hi : z.1-1 < 4 := by omega
  rw [List.getD_eq_getElem _ 0 (by simp; omega)]
  rw [List.getElem_append_left (by simpa using hi)]
  simp only [List.getElem_ofFn,state]
  have cell : z.1-1+1=z.1 := by omega
  simpa only [cell] using (incoming_iff_column n cup v (z.1-1) z.2 (by omega)).symm

theorem actual_pair_fits (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup)
    (u v : Fin n) (uv : u < v) (box : Box)
    (ok : valid (shape (ownerIndex n cup caps cups junction u).val)
      (shape (ownerIndex n cup caps cups junction v).val) box=true) : Fits box (labels n cup u v) := by
  have bd := label_bounds n cup caps cups u v uv v.isLt
  have ad := incoming_admissible n cup (labels n cup) (labels_increasing n cup caps) u v uv v.isLt
  apply valid_sound _ _ _ ok _ bd
  rw [owner_contains n cup caps cups junction v _ bd,owner_contains n cup caps cups junction u _ bd]
  exact ad

end ErdosSzekeres.Omission.ResidualDomains
