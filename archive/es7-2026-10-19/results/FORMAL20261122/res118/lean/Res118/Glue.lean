/-
res118-lean (22 November 2026): the gluing behind `ResidualBound 118`, in Lean, modulo explicit hypotheses.

Written chain: ES307N20261118 §3; ROADMAP20261115/ROUTE307_1116 §1.1–1.3; the 308 bridge
(LO33N20261113/budget34/bridge/README.md §2–3); VERIFY_LO §2.4–2.7.

Proved here (on top of the Lean rows of chain311 and Res118.LemmaA):
* `three_hF`, `hF18`: the nine base rows 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315 of `all_rows_2650`
  (zero-based, demand 6 each) cover every F-state exactly three times and nothing else, so 3·h(F) ≥ 54 (L4).
* `hLo`: h(Lo) ≥ 70 − B from `OmissionZRow.N66Bound B` (Lemma A, L5 + L13).
* `slice_false`: an actual nonempty residual configuration whose hole vector has h(F) ≥ T, h(Lo) ≥ B − T and at
  most B holes contradicts a slice exclusion, given the validity of the slice's extra rows.
* `residual_bound_118_of_blocks`: with h(F) ≥ 18 and h(Lo) ≥ 15, every split with h(C) = |H| ≤ 35 is one of
  (18,15), (18,16), (19,15), (18,17), (19,16), (20,15); the six slice exclusions give h(C) ≥ 36, and
  |R| + h(C) = 154 (`holes_sum_add_population`) gives |R| ≤ 118.

Hypotheses (definitions only; nothing here asserts them):
* `ResSliceExcludes rows B T`: the system of a slice tree: Boolean hole vector on the 154 states, state 0
  occupied, the 2,650 rows `support2650`/`demand2650`, the capacity rows (F, T) and (Lo, B − T), the unit rows
  `rows` (demand 1, support `lsupp s`), at most B holes. This is the shape of `Excludes2650Zero` plus the slice's
  extra rows in the order of its row file (rows 2650, 2651 = capacity rows; 2652.. = `rows`).
* `BlockValid rows`: every unit row of `rows` holds for every actual nonempty residual configuration.
-/
import Residual32Bridge2650.Rows
import ZeroState
import Res118.LemmaA

open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission
open OmissionResidual32Bridge2650 OmissionResidual32Transfer

namespace Res118

/-- The support of a literal row as a set of residual states (`CompactChecker.fsupp` of a catalog row). -/
def lsupp (s : List ℕ) : Finset (Fin 154) := Finset.univ.filter (fun i : Fin 154 => i.val ∈ s)

/-- A unit row (demand 1) with support `s` is valid: every actual nonempty residual configuration (as in
`Partition.ResidualBound`) leaves at least one state of `s` unoccupied. -/
def ValidUnitRow (s : List ℕ) : Prop :=
  ∀ n : ℕ, ∀ c : Configuration n, ∀ (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)), 0 < n →
      1 ≤ ∑ i ∈ lsupp s, holesOf (c.residualOccupied noCap noOctagon noJunction) i

/-- Every row of a block of unit rows is valid. -/
def BlockValid (rows : List (List ℕ)) : Prop := ∀ s ∈ rows, ValidUnitRow s

theorem BlockValid.nil : BlockValid [] := fun _ h => nomatch h

theorem BlockValid.append {a b : List (List ℕ)} (ha : BlockValid a) (hb : BlockValid b) :
    BlockValid (a ++ b) := by
  intro s hs
  rcases List.mem_append.mp hs with h | h
  · exact ha s h
  · exact hb s h

/-- The arithmetic statement a residual slice tree proves: no Boolean hole vector with state 0 occupied satisfies
the 2,650 base rows, the capacity rows (F, T) and (Lo, B − T) and the unit rows `rows`, with at most B holes. -/
def ResSliceExcludes (rows : List (List ℕ)) (B T : ℕ) : Prop :=
  ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧ holes 0 = 0 ∧
    (∀ r, demand2650 r ≤ ∑ i ∈ support2650 r, holes i) ∧
    T ≤ ∑ i ∈ F, holes i ∧ B - T ≤ ∑ i ∈ Lo, holes i ∧
    (∀ s ∈ rows, 1 ≤ ∑ i ∈ lsupp s, holes i) ∧ (∑ i, holes i) ≤ B

/-! ## h(F) ≥ 18 from nine base rows (L4) -/

/-- The nine base rows of L4 (zero-based indices into `all_rows_2650`). -/
abbrev r973 : Fin 2650 := ⟨973, by decide⟩
abbrev r1165 : Fin 2650 := ⟨1165, by decide⟩
abbrev r1167 : Fin 2650 := ⟨1167, by decide⟩
abbrev r1171 : Fin 2650 := ⟨1171, by decide⟩
abbrev r1175 : Fin 2650 := ⟨1175, by decide⟩
abbrev r1179 : Fin 2650 := ⟨1179, by decide⟩
abbrev r1183 : Fin 2650 := ⟨1183, by decide⟩
abbrev r1186 : Fin 2650 := ⟨1186, by decide⟩
abbrev r2315 : Fin 2650 := ⟨2315, by decide⟩

set_option maxRecDepth 100000 in
theorem nine_demands : demand2650 r973 = 6 ∧ demand2650 r1165 = 6 ∧ demand2650 r1167 = 6 ∧
    demand2650 r1171 = 6 ∧ demand2650 r1175 = 6 ∧ demand2650 r1179 = 6 ∧ demand2650 r1183 = 6 ∧
    demand2650 r1186 = 6 ∧ demand2650 r2315 = 6 := by
  decide +kernel

set_option maxRecDepth 100000 in
/-- Every F-state lies in exactly three of the nine supports, every Lo-state in none. -/
theorem nine_mult : ∀ i : Fin 154,
    (if i ∈ support2650 r973 then 1 else 0) + (if i ∈ support2650 r1165 then 1 else 0) +
      (if i ∈ support2650 r1167 then 1 else 0) + (if i ∈ support2650 r1171 then 1 else 0) +
      (if i ∈ support2650 r1175 then 1 else 0) + (if i ∈ support2650 r1179 then 1 else 0) +
      (if i ∈ support2650 r1183 then 1 else 0) + (if i ∈ support2650 r1186 then 1 else 0) +
      (if i ∈ support2650 r2315 then 1 else 0) = if i ∈ F then 3 else 0 := by
  decide +kernel

theorem sum_eq_ind (S : Finset (Fin 154)) (h : Fin 154 → ℕ) :
    ∑ i ∈ S, h i = ∑ i, (if i ∈ S then 1 else 0) * h i := by
  simp only [ite_mul, one_mul, zero_mul]
  rw [Finset.sum_ite_mem, Finset.univ_inter]

theorem three_hF (h : Fin 154 → ℕ) :
    ∑ i ∈ support2650 r973, h i + ∑ i ∈ support2650 r1165, h i + ∑ i ∈ support2650 r1167, h i +
      ∑ i ∈ support2650 r1171, h i + ∑ i ∈ support2650 r1175, h i + ∑ i ∈ support2650 r1179, h i +
      ∑ i ∈ support2650 r1183, h i + ∑ i ∈ support2650 r1186, h i + ∑ i ∈ support2650 r2315, h i =
      3 * ∑ i ∈ F, h i := by
  simp only [sum_eq_ind _ h, Finset.mul_sum, ← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl (fun i _ => ?_)
  simp only [← add_mul]
  rw [nine_mult i]
  split_ifs <;> simp

/-- **L4**: h(F) ≥ 18 for the hole vector of every actual residual configuration. -/
theorem hF18 {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    18 ≤ ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i := by
  have rows := all_rows_2650 c noCap noOctagon noJunction
  have h1 := rows r973
  have h2 := rows r1165
  have h3 := rows r1167
  have h4 := rows r1171
  have h5 := rows r1175
  have h6 := rows r1179
  have h7 := rows r1183
  have h8 := rows r1186
  have h9 := rows r2315
  obtain ⟨d1, d2, d3, d4, d5, d6, d7, d8, d9⟩ := nine_demands
  have h := three_hF (holesOf (c.residualOccupied noCap noOctagon noJunction))
  omega

/-! ## h(Lo) ≥ 70 − N66 (Lemma A, L5) -/

theorem hLo {B n : ℕ} (n66 : OmissionZRow.N66Bound B) (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    70 - B ≤ ∑ i ∈ Lo, holesOf (c.residualOccupied noCap noOctagon noJunction) i := by
  rw [holesOf_sum]
  exact lo_row n66 c noCap noOctagon noJunction

/-! ## Gluing -/

/-- One slice applied to an actual nonempty residual configuration. -/
theorem slice_false {rows : List (List ℕ)} {B T : ℕ} (hs : ResSliceExcludes rows B T)
    (hv : BlockValid rows) {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 0 < n)
    (hT : T ≤ ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i)
    (hL : B - T ≤ ∑ i ∈ Lo, holesOf (c.residualOccupied noCap noOctagon noJunction) i)
    (hB : ∑ i, holesOf (c.residualOccupied noCap noOctagon noJunction) i ≤ B) : False := by
  have hzero := OmissionResidualZeroState.zero_mem_residualOccupied c noCap noOctagon noJunction hn
  exact hs ⟨holesOf (c.residualOccupied noCap noOctagon noJunction), holesOf_boolean _,
    by simp only [holesOf, if_pos hzero], all_rows_2650 c noCap noOctagon noJunction, hT, hL,
    fun s hs' => hv s hs' n c noCap noOctagon noJunction hn, hB⟩

/-- **ResidualBound 118** from N66 ≤ 55, six slice exclusions and the validity of four blocks of unit rows. The
slice row lists are the ones of the slice trees: `[]` (budget 33), `P` (s19), `P ++ Q` (s18-v13, b35s18-v13),
`P ++ Q ++ U` (b35s19-v16), `P ++ Q ++ A` (b35s20-v169). -/
theorem residual_bound_118_of_blocks {P Q U A : List (List ℕ)}
    (n66 : OmissionZRow.N66Bound 55)
    (vP : BlockValid P) (vQ : BlockValid Q) (vU : BlockValid U) (vA : BlockValid A)
    (s33_18 : ResSliceExcludes [] 33 18)
    (s34_18 : ResSliceExcludes (P ++ Q) 34 18)
    (s34_19 : ResSliceExcludes P 34 19)
    (s35_18 : ResSliceExcludes (P ++ Q) 35 18)
    (s35_19 : ResSliceExcludes (P ++ Q ++ U) 35 19)
    (s35_20 : ResSliceExcludes (P ++ Q ++ A) 35 20) :
    Partition.ResidualBound 118 := by
  intro n c noCap noOctagon noJunction
  by_contra hn
  have hsum := holes_sum_add_population c noCap noOctagon noJunction
  have hF := hF18 c noCap noOctagon noJunction
  have hL := hLo n66 c noCap noOctagon noJunction
  have hp := sum_Lo_add_sum_F (holesOf (c.residualOccupied noCap noOctagon noJunction))
  have hpos : 0 < n := by omega
  have vPQ := vP.append vQ
  have vPQU := vPQ.append vU
  have vPQA := vPQ.append vA
  -- h(F) ≥ 18, h(Lo) ≥ 15, h(F) + h(Lo) = h(C) ≤ 35: six cases.
  by_cases e33 : ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i +
      ∑ i ∈ Lo, holesOf (c.residualOccupied noCap noOctagon noJunction) i = 33
  · exact slice_false s33_18 BlockValid.nil c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
  by_cases e34 : ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i +
      ∑ i ∈ Lo, holesOf (c.residualOccupied noCap noOctagon noJunction) i = 34
  · by_cases f18 : ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i = 18
    · exact slice_false s34_18 vPQ c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
    · exact slice_false s34_19 vP c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
  by_cases f18 : ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i = 18
  · exact slice_false s35_18 vPQ c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
  by_cases f19 : ∑ i ∈ F, holesOf (c.residualOccupied noCap noOctagon noJunction) i = 19
  · exact slice_false s35_19 vPQU c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)
  · exact slice_false s35_20 vPQA c noCap noOctagon noJunction hpos (by omega) (by omega) (by omega)

end Res118

#print axioms Res118.nine_demands
#print axioms Res118.nine_mult
#print axioms Res118.three_hF
#print axioms Res118.hF18
#print axioms Res118.hLo
#print axioms Res118.slice_false
#print axioms Res118.residual_bound_118_of_blocks
