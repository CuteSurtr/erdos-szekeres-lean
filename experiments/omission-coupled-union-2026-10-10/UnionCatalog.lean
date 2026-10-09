import ErdosSzekeres.Omission.CoupledVariants
import ErdosSzekeres.Omission.CoupledSecondVariants

/-! A deduplicated union of the two checked template families. These are
necessary geometric inequalities; distinctness does not imply independence. -/
namespace ErdosSzekeres.Omission.CoupledUnion
set_option maxHeartbeats 100000000
set_option maxRecDepth 100000

def origin : Fin 57 → Sum (Fin 42) (Fin 35) := ![Sum.inl 0, Sum.inl 1, Sum.inl 2, Sum.inl 3, Sum.inl 4, Sum.inl 5, Sum.inl 6, Sum.inl 7, Sum.inl 8, Sum.inl 9, Sum.inl 10, Sum.inl 11, Sum.inl 12, Sum.inl 13, Sum.inl 14, Sum.inl 15, Sum.inl 16, Sum.inl 17, Sum.inl 18, Sum.inl 19, Sum.inl 20, Sum.inl 21, Sum.inl 22, Sum.inl 23, Sum.inl 24, Sum.inl 25, Sum.inl 26, Sum.inl 27, Sum.inl 28, Sum.inl 29, Sum.inl 30, Sum.inl 31, Sum.inl 32, Sum.inl 33, Sum.inl 34, Sum.inl 35, Sum.inl 36, Sum.inl 37, Sum.inl 38, Sum.inl 39, Sum.inl 40, Sum.inl 41, Sum.inr 2, Sum.inr 4, Sum.inr 7, Sum.inr 8, Sum.inr 10, Sum.inr 11, Sum.inr 13, Sum.inr 17, Sum.inr 19, Sum.inr 22, Sum.inr 23, Sum.inr 25, Sum.inr 26, Sum.inr 28, Sum.inr 33]

def support (i : Fin 57) : Finset (Fin 154) :=
  match origin i with
  | .inl r => CoupledVariants.support r
  | .inr r => CoupledSecondVariants.support r

def literalSupport : Fin 57 → Finset (Fin 154) := ![{11, 17, 30, 39, 43, 50, 53, 56, 62, 65, 68, 77, 79}, {11, 17, 30, 39, 43, 50, 53, 56, 62, 65, 68, 77, 89}, {11, 17, 30, 39, 43, 50, 53, 56, 62, 65, 77, 91, 101}, {11, 17, 30, 39, 43, 50, 53, 56, 62, 65, 77, 91, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 67, 77, 79, 89}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 67, 77, 101, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 68, 77, 91, 101}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 68, 77, 91, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 68, 89, 91, 101}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 68, 89, 91, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 77, 79, 101, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 79, 89, 101, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 68, 77, 89, 91, 101}, {11, 17, 30, 39, 43, 50, 53, 62, 68, 77, 89, 91, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 77, 79, 89, 101, 110}, {11, 17, 30, 39, 43, 50, 62, 65, 68, 77, 89, 91, 101}, {11, 17, 30, 39, 43, 50, 62, 65, 68, 77, 89, 91, 110}, {11, 17, 30, 39, 43, 50, 62, 65, 77, 79, 89, 101, 110}, {16, 25, 30, 39, 43, 50, 53, 56, 62, 65, 68, 77, 79}, {16, 25, 30, 39, 43, 50, 53, 56, 62, 65, 68, 77, 89}, {16, 25, 30, 39, 43, 50, 53, 56, 62, 65, 77, 91, 101}, {16, 25, 30, 39, 43, 50, 53, 56, 62, 65, 77, 91, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 67, 77, 79, 89}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 67, 77, 101, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 68, 77, 91, 101}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 68, 77, 91, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 68, 89, 91, 101}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 68, 89, 91, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 77, 79, 101, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 79, 89, 101, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 68, 77, 89, 91, 101}, {16, 25, 30, 39, 43, 50, 53, 62, 68, 77, 89, 91, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 77, 79, 89, 101, 110}, {16, 25, 30, 39, 43, 50, 62, 65, 68, 77, 89, 91, 101}, {16, 25, 30, 39, 43, 50, 62, 65, 68, 77, 89, 91, 110}, {16, 25, 30, 39, 43, 50, 62, 65, 77, 79, 89, 101, 110}, {23, 30, 33, 39, 43, 50, 53, 62, 65, 67, 77, 79, 89}, {23, 30, 33, 39, 43, 50, 53, 62, 65, 67, 77, 101, 110}, {23, 30, 33, 39, 43, 50, 53, 62, 65, 77, 79, 101, 110}, {23, 30, 33, 39, 43, 50, 53, 62, 65, 79, 89, 101, 110}, {23, 30, 33, 39, 43, 50, 53, 62, 77, 79, 89, 101, 110}, {23, 30, 33, 39, 43, 50, 62, 65, 77, 79, 89, 101, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 67, 68, 77, 89}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 67, 77, 91, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 68, 77, 79, 89}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 77, 79, 91, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 77, 89, 91, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 77, 89, 101, 110}, {11, 17, 30, 39, 43, 50, 53, 62, 65, 79, 89, 91, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 67, 68, 77, 89}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 67, 77, 91, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 68, 77, 79, 89}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 77, 79, 91, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 77, 89, 91, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 77, 89, 101, 110}, {16, 25, 30, 39, 43, 50, 53, 62, 65, 79, 89, 91, 110}, {23, 30, 33, 39, 43, 50, 53, 62, 65, 77, 89, 101, 110}]

def secondIndex : Fin 35 → Fin 57 := ![1, 3, 42, 4, 43, 5, 7, 44, 45, 10, 46, 47, 9, 48, 11, 19, 21, 49, 22, 50, 23, 25, 51, 52, 28, 53, 54, 27, 55, 29, 36, 37, 38, 56, 39]

def independentIndex : Fin 9 → Fin 57 := ![6, 7, 10, 24, 25, 28, 38, 45, 52]

def redundantIndex : Fin 48 → Fin 57 := ![0, 1, 2, 3, 4, 5, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 26, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56]

def redundancyRow : Fin 48 → Fin 1187 := ![84, 84, 84, 84, 85, 85, 87, 87, 88, 87, 87, 88, 87, 87, 88, 131, 131, 131, 131, 134, 134, 136, 136, 140, 136, 136, 140, 136, 136, 140, 185, 185, 190, 190, 190, 85, 85, 87, 978, 978, 88, 134, 134, 136, 984, 984, 140, 992]

theorem matches_literal : ∀ i : Fin 57, support i = literalSupport i := by
  decide +kernel

theorem first_covered : ∀ i : Fin 42,
    support ⟨i.val, Nat.lt_trans i.isLt (by decide)⟩ = CoupledVariants.support i := by
  decide +kernel

theorem second_covered : ∀ i : Fin 35,
    support (secondIndex i) = CoupledSecondVariants.support i := by decide +kernel

theorem distinct_support : Function.Injective support := by decide +kernel

theorem card_thirteen : ∀ i : Fin 57, (support i).card = 13 := by decide +kernel

theorem classification : ∀ i : Fin 57,
    (∃ k : Fin 9, independentIndex k = i) ∨
    (∃ k : Fin 48, redundantIndex k = i) := by decide +kernel

theorem independent_indices_injective : Function.Injective independentIndex := by decide +kernel

theorem redundant_indices_injective : Function.Injective redundantIndex := by decide +kernel

theorem classes_disjoint : ∀ i : Fin 9, ∀ j : Fin 48,
    independentIndex i ≠ redundantIndex j := by decide +kernel

theorem all_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (i : Fin 57) :
    1 ≤ (support i \ c.residualOccupied noCap noOctagon noJunction).card := by
  unfold support
  cases origin i with
  | inl r => exact CoupledVariants.all_rows c noCap noOctagon noJunction r
  | inr r => exact CoupledSecondVariants.all_rows c noCap noOctagon noJunction r

#print axioms matches_literal
#print axioms first_covered
#print axioms second_covered
#print axioms distinct_support
#print axioms card_thirteen
#print axioms classification
#print axioms independent_indices_injective
#print axioms redundant_indices_injective
#print axioms classes_disjoint
#print axioms all_rows
end ErdosSzekeres.Omission.CoupledUnion
