import LemmaZ
import BalancedBudgetsZ
import FixedStatesZ
import LemmaZStar
import BalancedBudgetsZZs
import BalancedBudgetsZZsN
import Composition305
import Composition304
import Composition303
import Composition306

/-!
comp-audit statement-fidelity review (slot lrev, 22 Nov 2026). One compile, read-only use of the worker's
`comp-audit/out/olean`. Sections: A axioms, B full statements, C definitions as loaded, D Lean-checked links between
evidence forms and hypotheses, E module list, F row dumps (for an outside comparison with the checkers' inputs).
-/

open scoped BigOperators

-- A. axioms of the 31 audited theorems
#print axioms OmissionBalancedZ.composition_304_z
#print axioms OmissionBalancedZ.composition_305_z
#print axioms OmissionBalancedZF.composition_304_zf
#print axioms OmissionBalancedZF.composition_303_zf
#print axioms OmissionBalancedZZsF.composition_303_zzsf
#print axioms OmissionBalancedZZsF.composition_302_zzsf
#print axioms OmissionBalancedZZsF.composition_301_zzsf
#print axioms OmissionBalancedZZsF.composition_300_zzsf
#print axioms OmissionBalancedZZsN.composition_302_n54
#print axioms OmissionBalancedZZsN.composition_301_n53
#print axioms composition_304
#print axioms composition_303
#print axioms composition_305
#print axioms composition_306
#print axioms OmissionZRow.z_row
#print axioms OmissionZStarRow.zs_row
#print axioms OmissionBalancedZZsN.z_row_of
#print axioms OmissionBalancedZZsN.zs_row_of
#print axioms OmissionBalancedZ.balanced_bound_of_hole_budget_z
#print axioms OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf
#print axioms OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn
#print axioms OmissionZRow.Z_eq
#print axioms OmissionZStarRow.Zs_eq
#print axioms OmissionBalancedZ.feasible_holes_z
#print axioms OmissionBalancedZF.feasible_holes_zf
#print axioms OmissionBalancedZF.balanced_bound_of_hole_budget_zf
#print axioms OmissionBalancedZZsN.zzsn_55_iff
#print axioms avoiding_302
#print axioms avoiding_303
#print axioms avoiding_304
#print axioms avoiding_305
-- A2. lemmas the review's argument also uses
#print axioms OmissionBalancedZF.zero_mem_occupied
#print axioms OmissionBalancedZF.one_mem_occupied
#print axioms OmissionBalancedZZsF.feasible_holes_zzsf
#print axioms OmissionBalancedZZsN.feasible_holes_zzsn
#print axioms OmissionZRow.Z_card
#print axioms OmissionZStarRow.Zs_card
#print axioms OmissionBalanced.all_geometric_rows
#print axioms BalancedCoverCutsV2.all_rows
#print axioms ErdosSzekeres.Omission.Partition.forces_of_population_bounds
#print axioms ErdosSzekeres.Omission.Partition.avoiding_card_le_of_population_bounds

-- B. full statements, every binder shown
#check @OmissionBalancedZ.composition_304_z
#check @OmissionBalancedZ.composition_305_z
#check @OmissionBalancedZF.composition_304_zf
#check @OmissionBalancedZF.composition_303_zf
#check @OmissionBalancedZZsF.composition_303_zzsf
#check @OmissionBalancedZZsF.composition_302_zzsf
#check @OmissionBalancedZZsF.composition_301_zzsf
#check @OmissionBalancedZZsF.composition_300_zzsf
#check @OmissionBalancedZZsN.composition_302_n54
#check @OmissionBalancedZZsN.composition_301_n53
#check @composition_304
#check @composition_303
#check @composition_305
#check @composition_306
#check @OmissionZRow.z_row
#check @OmissionZStarRow.zs_row
#check @OmissionBalancedZZsN.z_row_of
#check @OmissionBalancedZZsN.zs_row_of
#check @OmissionBalancedZ.balanced_bound_of_hole_budget_z
#check @OmissionBalancedZZsF.balanced_bound_of_hole_budget_zzsf
#check @OmissionBalancedZZsN.balanced_bound_of_hole_budget_zzsn
#check @OmissionZRow.Z_eq
#check @OmissionZStarRow.Zs_eq
#check @OmissionBalancedZ.feasible_holes_z
#check @OmissionBalancedZF.feasible_holes_zf
#check @OmissionBalancedZF.balanced_bound_of_hole_budget_zf
#check @OmissionBalancedZZsN.zzsn_55_iff
#check @avoiding_302
#check @avoiding_303
#check @avoiding_304
#check @avoiding_305

-- C. definitions as loaded
#print ErdosSzekeres.Point
#print ErdosSzekeres.GeneralPosition
#print ErdosSzekeres.ConvexPosition
#print ErdosSzekeres.HasConvexNGon
#print ErdosSzekeres.ForcesConvexNGon
#print ErdosSzekeres.orient
#print ErdosSzekeres.Omission.Configuration
#print ErdosSzekeres.Omission.Configuration.HasCap
#print ErdosSzekeres.Omission.Configuration.HasCup
#print ErdosSzekeres.Omission.Configuration.cup
#print ErdosSzekeres.Omission.Configuration.occupied
#print ErdosSzekeres.Omission.Configuration.balancedOwner
#print ErdosSzekeres.Omission.Subsets.JunctionOn
#print ErdosSzekeres.Omission.Subsets.NoJunctionOn
#print ErdosSzekeres.Omission.Partition.BalancedBound
#print ErdosSzekeres.Omission.Partition.ResidualBound
#print OmissionZRow.N66Bound
#print OmissionZRow.zProfile
#print OmissionZRow.Z
#print OmissionZStarRow.zsProfile
#print OmissionZStarRow.Zs
#print OmissionBalancedZ.ExcludesHoleBudgetZ
#print OmissionBalancedZF.ExcludesHoleBudgetZF
#print OmissionBalancedZZsF.ExcludesHoleBudgetZZsF
#print OmissionBalancedZZsN.ExcludesHoleBudgetZZsN
#print OmissionBalanced.row
#print OmissionBalanced.support
#print OmissionBalanced.demand

-- C2. the written readings, checked definitionally
example : ErdosSzekeres.ForcesConvexNGon 304 8 ↔
    ∀ s : Finset (Fin 2 → ℝ), ErdosSzekeres.GeneralPosition s → 304 ≤ s.card →
      ∃ t : Finset (Fin 2 → ℝ), t ⊆ s ∧ t.card = 8 ∧
        ConvexIndependent ℝ (fun p : (t : Set (Fin 2 → ℝ)) => (p : Fin 2 → ℝ)) := Iff.rfl

example (s : Finset (Fin 2 → ℝ)) : ErdosSzekeres.GeneralPosition s ↔
    ∀ a ∈ s, ∀ b ∈ s, ∀ c ∈ s, a ≠ b → a ≠ c → b ≠ c →
      ¬ Collinear ℝ ({a, b, c} : Set (Fin 2 → ℝ)) := Iff.rfl

example : OmissionBalancedZ.ExcludesHoleBudgetZ 67 ↔
    ¬ ∃ h : Fin 252 → ℕ, (∀ i, h i ≤ 1) ∧
      (∀ r : Fin 2685, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, h i) ∧
      (∀ r : Fin 446, BalancedCoverCutsV2.demand r ≤ ∑ i ∈ BalancedCoverCutsV2.support r, h i) ∧
      15 ≤ ∑ i ∈ OmissionZRow.Z, h i ∧ (∑ i, h i) ≤ 67 := Iff.rfl

-- D. links between what the evidence certifies and the Lean hypotheses
namespace CompAuditReview

/-- What a zero-side-only tree (every path starts with state 0 occupied; lemma path 0:1) on the catalog rows,
the Z-row and the Z*-row at demand `r` and budget `b` certifies: state 0 is fixed occupied, state 1 is free. -/
def ZeroSideZZs (r b : ℕ) : Prop :=
  ¬ ∃ holes : Fin 252 → ℕ, holes 0 = 0 ∧ (∀ i, holes i ≤ 1) ∧
    (∀ q, OmissionBalanced.demand q ≤ ∑ i ∈ OmissionBalanced.support q, holes i) ∧
    (∀ q, BalancedCoverCutsV2.demand q ≤ ∑ i ∈ BalancedCoverCutsV2.support q, holes i) ∧
    r ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ r ≤ ∑ i ∈ OmissionZStarRow.Zs, holes i ∧
    (∑ i, holes i) ≤ b

theorem zzsf_of_zeroSide (b : ℕ) (h : ZeroSideZZs 15 b) :
    OmissionBalancedZZsF.ExcludesHoleBudgetZZsF b := by
  rintro ⟨x, h0, -, rest⟩
  exact h ⟨x, h0, rest⟩

theorem zzsn_of_zeroSide (r b : ℕ) (h : ZeroSideZZs r b) :
    OmissionBalancedZZsN.ExcludesHoleBudgetZZsN r b := by
  rintro ⟨x, h0, -, rest⟩
  exact h ⟨x, h0, rest⟩

theorem zf_of_z (b : ℕ) (h : OmissionBalancedZ.ExcludesHoleBudgetZ b) :
    OmissionBalancedZF.ExcludesHoleBudgetZF b := by
  rintro ⟨x, -, -, rest⟩
  exact h ⟨x, rest⟩

theorem balanced_mono {a b : ℕ} (hab : a ≤ b) (h : ErdosSzekeres.Omission.Partition.BalancedBound a) :
    ErdosSzekeres.Omission.Partition.BalancedBound b := by
  intro n c h1 h2 h3
  exact le_trans (h n c h1 h2 h3) hab

/-- 306 from the inputs that do exist (the budget-66 tree of ES305), not from the stopped budget-65 campaign. -/
theorem forces_306_of_305_inputs (trees : OmissionBalancedZ.ExcludesHoleBudgetZ 66)
    (n66 : OmissionZRow.N66Bound 55) (hR : ErdosSzekeres.Omission.Partition.ResidualBound 118) :
    ErdosSzekeres.ForcesConvexNGon 306 8 :=
  composition_306 (balanced_mono (by norm_num)
    (OmissionBalancedZ.balanced_bound_of_hole_budget_z n66 trees)) hR

end CompAuditReview

#print axioms CompAuditReview.zzsf_of_zeroSide
#print axioms CompAuditReview.zzsn_of_zeroSide
#print axioms CompAuditReview.zf_of_z
#print axioms CompAuditReview.balanced_mono
#print axioms CompAuditReview.forces_306_of_305_inputs

-- E. the environment's module list (for the outside closure check)
open Lean in
#eval show CoreM Unit from do
  for m in (← getEnv).header.moduleNames do
    IO.println s!"module {m}"

-- F. row dumps from the loaded definitions (decidable membership over the 252 states, ascending)
#eval show IO Unit from do
  for r in List.finRange 2685 do
    let s := (List.finRange 252).filter (fun i => decide (i ∈ OmissionBalanced.support r))
    IO.println s!"ROW {r.val} {OmissionBalanced.demand r} {s.map Fin.val}"

#eval show IO Unit from do
  for r in List.finRange 446 do
    let s := (List.finRange 252).filter (fun i => decide (i ∈ BalancedCoverCutsV2.support r))
    IO.println s!"CUT {r.val} {BalancedCoverCutsV2.demand r} {s.map Fin.val}"

#eval show IO Unit from do
  IO.println s!"ZIDX {OmissionZRow.zIndices}"
  IO.println s!"ZSIDX {OmissionZStarRow.zsIndices}"
  IO.println s!"ZSET {((List.finRange 252).filter (fun i => decide (i ∈ OmissionZRow.Z))).map Fin.val}"
  IO.println s!"ZSSET {((List.finRange 252).filter (fun i => decide (i ∈ OmissionZStarRow.Zs))).map Fin.val}"
  for k in List.range 252 do
    IO.println s!"CAT {k} {ErdosSzekeres.Omission.BalancedCatalog.catalog.getD k []}"

#eval IO.println "REVIEW-END"
