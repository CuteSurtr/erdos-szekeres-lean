import MirrorEncoding.Cover

/-!
# The leaf CNFs as `verify/v3/v3_check.py` writes them

`v3_check.py` (commit 92746ac, formerly bdf319c) writes, for a case cube `c` and a leaf `l`:
the header, `F`'s clauses unchanged, then one unit clause per literal of
`sorted(c, key=abs)`, then one unit clause per literal of
`sorted((x for x in l if x not in set(c)), key=abs)`. `v3LeafCnf F c l` is that clause list.
Python's `sorted` is stable, and so is `List.mergeSort` with `≤` on `natAbs`.

`v3LeafCnf F c l` and `cubeCnf (cubeCnf F c) l` have the same clauses, in another order and
multiplicity, so one is satisfiable iff the other is (`v3LeafCnf_iff`). A leaf containing the
negation of a case-cube literal gives a CNF with units `[x]` and `[-x]`, which is
unsatisfiable without any solver fact (`not_dimacsSatisfiable_of_neg_mem`).
-/

namespace V2L2

open ETV Mir

/-- Python's `sorted(xs, key=abs)` (stable). -/
def sortAbs (xs : List Int) : List Int := xs.mergeSort fun a b => decide (a.natAbs ≤ b.natAbs)

/-- The unit literals that `v3_check.py` appends: the case cube sorted by absolute value, then
the leaf literals not in the case cube, sorted by absolute value. -/
def v3Units (c l : List Int) : List Int := sortAbs c ++ sortAbs (l.filter fun x => decide (x ∉ c))

/-- The clause list of the file that `v3_check.py` gives cake_lpr for case cube `c`, leaf `l`. -/
def v3LeafCnf (F : List (List Int)) (c l : List Int) : List (List Int) :=
  F ++ (v3Units c l).map fun z => [z]

/-- Satisfiability is monotone in the set of clauses. -/
theorem dimacsSatisfiable_of_subset {A B : List (List ℤ)} (h : ∀ d ∈ B, d ∈ A) :
    DimacsSatisfiable A → DimacsSatisfiable B := fun ⟨ν, hν⟩ => ⟨ν, fun d hd => hν d (h d hd)⟩

/-- `DimacsSatisfiable` depends only on the set of clauses. -/
theorem dimacsSatisfiable_congr {A B : List (List ℤ)} (hAB : ∀ d ∈ A, d ∈ B)
    (hBA : ∀ d ∈ B, d ∈ A) : DimacsSatisfiable A ↔ DimacsSatisfiable B :=
  ⟨dimacsSatisfiable_of_subset hBA, dimacsSatisfiable_of_subset hAB⟩

theorem mem_v3LeafCnf_iff {F : List (List ℤ)} {c l d : List ℤ} :
    d ∈ v3LeafCnf F c l ↔ d ∈ cubeCnf (cubeCnf F c) l := by
  simp only [v3LeafCnf, cubeCnf, v3Units, sortAbs, List.mem_append, List.mem_map,
    List.mem_mergeSort, List.mem_filter, decide_eq_true_eq]
  constructor
  · rintro (h | ⟨z, (hz | ⟨hz, -⟩), rfl⟩)
    · exact Or.inl (Or.inl h)
    · exact Or.inl (Or.inr ⟨z, hz, rfl⟩)
    · exact Or.inr ⟨z, hz, rfl⟩
  · rintro ((h | ⟨z, hz, rfl⟩) | ⟨z, hz, rfl⟩)
    · exact Or.inl h
    · exact Or.inr ⟨z, Or.inl hz, rfl⟩
    · by_cases hc : z ∈ c
      · exact Or.inr ⟨z, Or.inl hc, rfl⟩
      · exact Or.inr ⟨z, Or.inr ⟨hz, hc⟩, rfl⟩

/-- The checked file and the Lean term of V2-L are equisatisfiable. -/
theorem v3LeafCnf_iff (F : List (List ℤ)) (c l : List ℤ) :
    DimacsSatisfiable (v3LeafCnf F c l) ↔ DimacsSatisfiable (cubeCnf (cubeCnf F c) l) :=
  dimacsSatisfiable_congr (fun _ h => mem_v3LeafCnf_iff.1 h) (fun _ h => mem_v3LeafCnf_iff.2 h)

/-- A CNF with the unit clauses `[z]` and `[-z]`, `z ≠ 0`, has no model. -/
theorem not_dimacsSatisfiable_of_units {F : List (List ℤ)} {z : ℤ} (hz : z ≠ 0)
    (h1 : [z] ∈ F) (h2 : [-z] ∈ F) : ¬DimacsSatisfiable F := by
  rintro ⟨ν, hν⟩
  obtain ⟨a, ha, h⟩ := hν _ h1
  obtain ⟨b, hb, h'⟩ := hν _ h2
  simp only [List.mem_singleton] at ha hb
  subst ha; subst hb
  rw [Int.natAbs_neg] at h'
  rcases h with ⟨h, e⟩ | ⟨h, e⟩ <;> rcases h' with ⟨h', e'⟩ | ⟨h', e'⟩ <;>
    first | omega | (rw [e] at e'; exact absurd e' (by decide))

/-- A leaf containing the negation of a (nonzero) case-cube literal needs no solver fact. -/
theorem not_dimacsSatisfiable_of_neg_mem {F : List (List ℤ)} {c l : List ℤ} {x : ℤ}
    (hx : x ∈ l) (hnx : -x ∈ c) (h0 : -x ≠ 0) :
    ¬DimacsSatisfiable (cubeCnf (cubeCnf F c) l) := by
  refine not_dimacsSatisfiable_of_units (z := x) (by omega) ?_ ?_ <;>
    simp only [cubeCnf, List.mem_append, List.mem_map, List.cons.injEq, and_true]
  · exact Or.inr ⟨x, hx, rfl⟩
  · exact Or.inl (Or.inr ⟨-x, hnx, rfl⟩)

end V2L2
