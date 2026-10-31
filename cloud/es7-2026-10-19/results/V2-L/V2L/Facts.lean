import V2L.Data

/-!
# The split tables, and structural facts about the data

`upTable` pairs each upper chain `U` with its cube `UP(U)`; `caseTable` pairs each case
`(U, L)` with `cube(U, L)`. `casesOf U` is the list of case cubes with upper chain `U`, in
file order: exactly the blocking cubes of `cover.py`'s obligation `up:U`
(`[H.cube(U2, L) for U2, L in H.cases() if U2 == U]`).

The facts below are checked by the kernel (`decide +kernel`, no `native_decide`). Only the
nonzero-literal facts are used by the main theorem; the others record that the data is the
split described in `results/Mii-S/soundness.md`.
-/

namespace V2L

/-- Each upper chain `U` with its cube `UP(U)`. -/
def upTable : List (List Nat × List Int) := upSets.zip upCubes

/-- Each case `(U, L)` with its cube `cube(U, L)`. -/
def caseTable : List ((List Nat × List Nat) × List Int) := caseSpecs.zip caseCubes

/-- The case cubes with upper chain `U`, in `cases.icnf` order. -/
def casesOf (U : List Nat) : List (List Int) :=
  (caseTable.filter fun p => p.1.1 == U).map Prod.snd

/-- The pair labels `2..16`. -/
def labels : List Nat := List.range' 2 15

/-- `cover.py`'s `UPS`: `()`, then the singletons, then the pairs `a < b`. -/
def upSetsSpec : List (List Nat) :=
  [[]] ++ labels.map (fun a => [a]) ++
    labels.flatMap fun a => (List.range' (a + 1) (16 - a)).map fun b => [a, b]

/-- `hullsplit.py`'s `cases()`. -/
def caseSpecsSpec : List (List Nat × List Nat) :=
  labels.flatMap (fun a => [([a], []), ([], [a])]) ++
  labels.flatMap (fun a => (List.range' (a + 1) (16 - a)).flatMap fun b =>
    [([a, b], []), ([], [a, b])]) ++
  labels.flatMap fun a => (labels.filter (· ≠ a)).map fun b => ([a], [b])

theorem upSets_eq : upSets = upSetsSpec := by decide +kernel

theorem caseSpecs_eq : caseSpecs = caseSpecsSpec := by decide +kernel

theorem upSets_length : upSets.length = 121 := by decide +kernel

theorem upCubes_length : upCubes.length = 121 := by decide +kernel

theorem caseSpecs_length : caseSpecs.length = 450 := by decide +kernel

theorem caseCubes_length : caseCubes.length = 450 := by decide +kernel

theorem upSets_nodup : upSets.Nodup := by decide +kernel

/-- Every case's upper chain is one of the 121. -/
theorem caseSpecs_upper_mem : ∀ p ∈ caseSpecs, p.1 ∈ upSets := by decide +kernel

/-- The lists `casesOf U` partition the 450 cases. -/
theorem casesOf_length_sum : (upSets.map fun U => (casesOf U).length).sum = 450 := by
  decide +kernel

set_option maxRecDepth 10000 in
theorem upCubes_nonzero : ∀ c ∈ upCubes, ∀ z ∈ c, z ≠ 0 := by decide +kernel

set_option maxRecDepth 10000 in
theorem caseCubes_nonzero : ∀ c ∈ caseCubes, ∀ z ∈ c, z ≠ 0 := by decide +kernel

theorem upTable_snd : upTable.map Prod.snd = upCubes :=
  List.map_snd_zip (by rw [upSets_length, upCubes_length]; exact Nat.le_refl _)

theorem caseTable_snd : caseTable.map Prod.snd = caseCubes :=
  List.map_snd_zip (by rw [caseSpecs_length, caseCubes_length]; exact Nat.le_refl _)

theorem mem_caseCubes_of_casesOf {U : List Nat} {c : List Int} (h : c ∈ casesOf U) :
    ∃ s, (s, c) ∈ caseTable := by
  obtain ⟨⟨s, c'⟩, hp, rfl⟩ := List.mem_map.1 h
  exact ⟨s, (List.mem_filter.1 hp).1⟩

theorem casesOf_nonzero (U : List Nat) : ∀ c ∈ casesOf U, ∀ z ∈ c, z ≠ 0 := by
  intro c hc
  obtain ⟨s, hs⟩ := mem_caseCubes_of_casesOf hc
  exact caseCubes_nonzero c (caseTable_snd ▸ List.mem_map.2 ⟨(s, c), hs, rfl⟩)

theorem upTable_nonzero : ∀ p ∈ upTable, ∀ z ∈ p.2, z ≠ 0 := fun p hp =>
  upCubes_nonzero p.2 (upTable_snd ▸ List.mem_map.2 ⟨p, hp, rfl⟩)

end V2L
