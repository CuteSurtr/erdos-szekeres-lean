import CycleIndependence
import BlockIndependence

namespace AdditionalResidualStrictness
open ErdosSzekeres.Omission.AdditionalResidualRows
set_option maxHeartbeats 100000000
set_option maxRecDepth 100000

def witness (i : Fin 21) : Finset (Fin 154) :=
  if h : i.val < 20 then (cycle ⟨i.val, h⟩).toFinset else blockWitness

theorem original_rows_allow_witness (i : Fin 21) (r : Fin 1187) :
    OmissionResidual.demand r ≤ (OmissionResidual.support r \ witness i).card := by
  by_cases h : i.val < 20
  · simpa only [witness, h, dif_pos] using original_rows_allow_each_cycle ⟨i.val, h⟩ r
  · simpa only [witness, h, dif_neg] using original_rows_allow_block r

theorem other_new_rows_allow_witness : ∀ i j : Fin 21, i ≠ j →
    demand j ≤ (support j \ witness i).card := by
  decide +kernel

theorem own_row_fails : ∀ i : Fin 21,
    ¬ demand i ≤ (support i \ witness i).card := by
  decide +kernel

/-- Every added inequality excludes an abstract assignment satisfying all old
rows and every other new row. This does not assert geometric realizability of
any of these assignments or improve the total population bound. -/
theorem independent_each_additional_row (i : Fin 21) :
    ∃ occupied : Finset (Fin 154),
      (∀ r : Fin 1187, OmissionResidual.demand r ≤
        (OmissionResidual.support r \ occupied).card) ∧
      (∀ j : Fin 21, i ≠ j → demand j ≤ (support j \ occupied).card) ∧
      ¬ demand i ≤ (support i \ occupied).card := by
  exact ⟨witness i, original_rows_allow_witness i,
    other_new_rows_allow_witness i, own_row_fails i⟩

#print axioms original_rows_allow_witness
#print axioms other_new_rows_allow_witness
#print axioms own_row_fails
#print axioms independent_each_additional_row
end AdditionalResidualStrictness
