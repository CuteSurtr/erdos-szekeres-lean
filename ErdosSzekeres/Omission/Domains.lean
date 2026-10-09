/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, formal/sources/ES8Domains.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Catalog data: CC BY 4.0; see docs/THIRD_PARTY.md.
Changes: local namespaces/imports, Lean/Mathlib 4.24 compatibility, kernel-only checks.
-/
import ErdosSzekeres.Omission.BalancedCatalog
import Mathlib.Data.List.GetD

namespace ErdosSzekeres.Omission.Domains
open ErdosSzekeres.Omission.StateInterface ErdosSzekeres.Omission.ActualRanks ErdosSzekeres.Omission.BalancedCatalog

structure Box where
  present : Bool
  xmin : Nat
  xmax : Nat
  ymin : Nat
  ymax : Nat
  deriving Repr,DecidableEq

def Fits (b : Box) (z : Label) : Prop :=
  b.present=true ∧ b.xmin ≤ z.1 ∧ z.1 ≤ b.xmax ∧ b.ymin ≤ z.2 ∧ z.2 ≤ b.ymax
instance (b : Box) (z : Label) : Decidable (Fits b z) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _))

def grid : List Label := (List.range 5).flatMap (fun x => (List.range 5).map (fun y => (x+1,y+1)))

def Contains (s : List Nat) (z : Label) : Prop := z.2 ≤ s.getD (z.1-1) 0
instance (s : List Nat) (z : Label) : Decidable (Contains s z) := inferInstanceAs (Decidable (_ ≤ _))

def valid (a b : List Nat) (box : Box) : Bool :=
  grid.all (fun z => decide (Contains b z ∧ ¬ Contains a z → Fits box z))

theorem mem_grid (z : Label) (h : 1 ≤ z.1 ∧ z.1 ≤ 5 ∧ 1 ≤ z.2 ∧ z.2 ≤ 5) : z ∈ grid := by
  apply List.mem_flatMap.mpr
  refine ⟨z.1-1,List.mem_range.mpr (by omega),?_⟩
  apply List.mem_map.mpr
  exact ⟨z.2-1,List.mem_range.mpr (by omega),by ext <;> simp <;> omega⟩

theorem valid_sound (a b : List Nat) (box : Box) (ok : valid a b box=true)
    (z : Label) (bounds : 1 ≤ z.1 ∧ z.1 ≤ 5 ∧ 1 ≤ z.2 ∧ z.2 ≤ 5)
    (difference : Contains b z ∧ ¬ Contains a z) : Fits box z := by
  have h := List.all_eq_true.mp ok z (mem_grid z bounds)
  exact of_decide_eq_true h difference

def shape (id : Nat) : List Nat := catalog.getD id []

theorem owner_shape (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (v : Fin n) :
    shape (ownerIndex n cup caps cups v).val = ErdosSzekeres.Omission.Ferrers.stateList (balancedState n cup caps cups v) := by
  unfold shape
  rw [List.getD_eq_getElem catalog []
    (by rw [catalog_length]; exact (ownerIndex n cup caps cups v).isLt)]
  exact ownerIndex_profile n cup caps cups v

theorem owner_contains (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7) (v : Fin n)
    (z : Label) (bounds : 1 ≤ z.1 ∧ z.1 ≤ 5 ∧ 1 ≤ z.2 ∧ z.2 ≤ 5) :
    Contains (shape (ownerIndex n cup caps cups v).val) z ↔ Incoming (labels cup) v z := by
  rw [owner_shape]
  unfold Contains ErdosSzekeres.Omission.Ferrers.stateList
  have hi : z.1-1 < 5 := by omega
  rw [List.getD_eq_getElem _ 0 (by simpa using hi)]
  simp only [List.getElem_ofFn,balancedState]
  have cell : z.1-1+1=z.1 := by omega
  simpa only [cell] using (incoming_iff_column cup v (z.1-1) z.2 (by omega)).symm

theorem actual_pair_fits (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7)
    (u v : Fin n) (uv : u < v) (box : Box)
    (ok : valid (shape (ownerIndex n cup caps cups u).val)
      (shape (ownerIndex n cup caps cups v).val) box=true) : Fits box (labels cup u v) := by
  have bd := balanced_label_bounds n cup caps cups u v uv v.isLt
  have ad := actual_incoming_admissible n cup u v uv v.isLt
  apply valid_sound _ _ _ ok _ bd
  rw [owner_contains n cup caps cups v _ bd,owner_contains n cup caps cups u _ bd]
  exact ad

end ErdosSzekeres.Omission.Domains
