/-
Adapted from Jineon Baek's erdos-tuza-valtr proof code, distributed in
Michael Schroeder's version-1 archive, DOI 10.5281/zenodo.22842891.
Licensed under Apache-2.0; see docs/APACHE-2.0.txt and docs/THIRD_PARTY.md.
Changes: local imports and compatibility with Lean/Mathlib v4.24.0.
-/
-- Mirror configuration
import ErdosSzekeres.Vendor.ETV.Lib.List.Lemmas
set_option linter.unusedVariables false
set_option linter.unusedSimpArgs false
set_option linter.unnecessarySeqFocus false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
variable {α : Type*}
open OrderDual
section Mirror

variable [LinearOrder α]

open OrderDual

@[simp]
theorem List.Mirror_nil : ([] : List α).Mirror = [] :=
  rfl

@[simp]
theorem List.Mirror_singleton {a : α} : [a].Mirror = [toDual a] :=
  rfl

@[simp]
theorem List.Mirror_cons {a : α} {l : List α} : (a :: l).Mirror = l.Mirror ++ [toDual a] := by
  simp [List.Mirror]

@[simp]
theorem List.Mirror_append {l1 l2 : List α} : (l1 ++ l2).Mirror = l2.Mirror ++ l1.Mirror := by
  simp [List.Mirror]

@[simp]
theorem List.ofMirror_nil : ([] : List αᵒᵈ).ofMirror = [] :=
  rfl

@[simp]
theorem List.ofMirrorMirror {l : List αᵒᵈ} : l.ofMirror.Mirror = l :=
  by simp [List.ofMirror, List.Mirror, Function.comp_def]

@[simp]
theorem Finset.ofMirrorMirror {S : Finset αᵒᵈ} : S.ofMirror.Mirror = S :=
  by
  ext x
  simp only [Finset.ofMirror, Finset.Mirror, Finset.mem_image]
  constructor
  · rintro ⟨a, ⟨b, hb, rfl⟩, rfl⟩
    exact hb
  · intro hx
    exact ⟨ofDual x, ⟨x, hx, rfl⟩, rfl⟩

@[simp]
theorem List.Mirror_length {l : List α} : l.Mirror.length = l.length := by rw [List.Mirror]; simp

theorem List.chain'_mirror {l : List α} : List.IsChain (· < ·) l.Mirror ↔ List.IsChain (· < ·) l := by
  change (l.map toDual).reverse.IsChain (· < ·) ↔ l.IsChain (· < ·)
  rw [List.isChain_reverse, List.isChain_map]
  rfl

theorem List.Mirror_getLast? {l : List α} : l.Mirror.getLast? = Option.map toDual l.head? := by
  rw [List.Mirror] <;> cases l <;> simp <;> tauto

theorem List.Mirror_head? {l : List α} : l.Mirror.head? = Option.map toDual l.getLast? :=
  by
  rw [List.Mirror, List.reverse_head?]
  -- quick-and-dirty proof
  induction' l with a l ih;
  simp
  simp; cases' l with b l; simp
  simp; simp at ih; exact ih

theorem List.ofMirror_getLast? {l : List αᵒᵈ} : l.ofMirror.getLast? = Option.map ofDual l.head? :=
  by rw [List.ofMirror] <;> cases l <;> simp <;> tauto

theorem List.ofMirror_head? {l : List αᵒᵈ} : l.ofMirror.head? = Option.map ofDual l.getLast? :=
  by
  rw [List.ofMirror, List.reverse_head?]
  -- quick-and-dirty proof
  induction' l with a l ih;
  simp
  simp; cases' l with b l; simp
  simp; simp at ih; exact ih

theorem List.Mirror_mem_getLast? {a : α} {l : List α} :
    toDual a ∈ l.Mirror.getLast? ↔ a ∈ l.head? := by rw [List.Mirror] <;> cases l <;> simp

theorem List.Mirror_mem_head? {a : α} {l : List α} : toDual a ∈ l.Mirror.head? ↔ a ∈ l.getLast? :=
  by
  rw [List.Mirror, List.reverse_head?]
  -- quick-and-dirty proof
  induction' l with a l ih;
  simp
  simp; cases' l with b l; simp
  simp; simp at ih; exact ih

@[simp]
theorem List.Mirror_in {l : List α} {S : Finset α} : l.Mirror.In S.Mirror ↔ l.In S :=
  by
  rw [List.Mirror]; simp; constructor
  · simp [List.In, Finset.Mirror, HasSubset.Subset]
  · simp [List.In, Finset.Mirror]

@[simp]
theorem Finset.memMirror {a : α} {S : Finset α} : toDual a ∈ S.Mirror ↔ a ∈ S := by
  simp [Finset.Mirror]

@[simp]
theorem Finset.Mirror_card {S : Finset α} : S.Mirror.card = S.card :=
  by
  rw [Finset.Mirror]
  apply S.card_image_of_injective
  intro a b; simp

end Mirror
