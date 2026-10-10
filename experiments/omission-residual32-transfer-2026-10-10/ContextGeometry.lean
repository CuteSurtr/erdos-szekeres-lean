import Transfer
import Residual32ContextsProof.Audit
open scoped BigOperators
open ErdosSzekeres ErdosSzekeres.Omission
namespace OmissionResidual32Transfer
set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

theorem hole_budget_of_population {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n) :
    (∑ i, holesOf (c.residualOccupied noCap noOctagon noJunction) i) ≤ 32 := by
  let occupied := c.residualOccupied noCap noOctagon noJunction
  have hc := Finset.card_add_card_compl occupied
  have ho : occupied.card = n := c.residual_occupied_card noCap noOctagon noJunction
  have hh : (∑ i : Fin 154, holesOf occupied i) = occupiedᶜ.card := by
    simpa only [Finset.compl_eq_univ_sdiff] using holesOf_sum occupied Finset.univ
  change (∑ i : Fin 154, holesOf occupied i) ≤ 32
  rw [hh]
  simp only [Fintype.card_fin] at hc
  omega

/-- Transfer any literal contextual arithmetic exclusion to actual geometry.
The occupied/missing context is evaluated on the very same hole vector. -/
theorem context_impossible_of_exclusion (missing occupied : Finset (Fin 154))
    (verified : ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, OmissionResidual32Contexts.demand r ≤
        ∑ i ∈ OmissionResidual32Contexts.support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ missing, holes i = 1) ∧ (∀ i ∈ occupied, holes i = 0))
    {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ missing, i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ occupied, i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  apply verified
  refine ⟨holesOf (c.residualOccupied noCap noOctagon noJunction), holesOf_boolean _,
    all_rows c noCap noOctagon noJunction, hole_budget_of_population c noCap noOctagon noJunction hn,
    ?_, ?_⟩
  · intro i hi
    simp only [holesOf, if_neg (hm i hi)]
  · intro i hi
    simp only [holesOf, if_pos (ho i hi)]

def missing492360 : Finset (Fin 154) := {27, 43, 47, 49, 60, 67, 87, 88, 93, 109}
def occupied492360 : Finset (Fin 154) := {25, 34, 36, 44, 45, 50, 65, 78}
theorem geometric_node492360 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ missing492360, i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ occupied492360, i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  apply context_impossible_of_exclusion missing492360 occupied492360 _ c noCap noOctagon noJunction hn hm ho
  have hmEq : missing492360 = (insert 109 (insert 93 (insert 88 (insert 87 (insert 67 (insert 60 (insert 49 (insert 47 (insert 43 (insert 27 ∅)))))))))) := by decide +kernel
  have hoEq : occupied492360 = (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))) := by decide +kernel
  rw [hmEq, hoEq]
  exact OmissionResidual32Contexts.node492360
#print axioms geometric_node492360

def missing492359 : Finset (Fin 154) := {27, 43, 47, 49, 60, 67, 88, 93, 109}
def occupied492359 : Finset (Fin 154) := {25, 34, 36, 44, 45, 50, 65, 78, 87}
theorem geometric_node492359 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ missing492359, i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ occupied492359, i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  apply context_impossible_of_exclusion missing492359 occupied492359 _ c noCap noOctagon noJunction hn hm ho
  have hmEq : missing492359 = (insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 49 (insert 47 (insert 43 (insert 27 ∅))))))))) := by decide +kernel
  have hoEq : occupied492359 = (insert 87 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) := by decide +kernel
  rw [hmEq, hoEq]
  exact OmissionResidual32Contexts.node492359
#print axioms geometric_node492359

def missing485523 : Finset (Fin 154) := {31, 34, 37, 43, 46, 47, 56, 60, 67, 88, 109}
def occupied485523 : Finset (Fin 154) := {23, 27, 36, 39, 44, 70, 78, 81, 97}
theorem geometric_node485523 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ missing485523, i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ occupied485523, i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  apply context_impossible_of_exclusion missing485523 occupied485523 _ c noCap noOctagon noJunction hn hm ho
  have hmEq : missing485523 = (insert 109 (insert 88 (insert 67 (insert 60 (insert 56 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))))) := by decide +kernel
  have hoEq : occupied485523 = (insert 97 (insert 81 (insert 78 (insert 70 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) := by decide +kernel
  rw [hmEq, hoEq]
  exact OmissionResidual32Contexts.node485523
#print axioms geometric_node485523

def missing485522 : Finset (Fin 154) := {31, 34, 37, 43, 46, 47, 56, 60, 67, 88}
def occupied485522 : Finset (Fin 154) := {23, 27, 36, 39, 44, 70, 78, 81, 97, 109}
theorem geometric_node485522 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ missing485522, i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ occupied485522, i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  apply context_impossible_of_exclusion missing485522 occupied485522 _ c noCap noOctagon noJunction hn hm ho
  have hmEq : missing485522 = (insert 88 (insert 67 (insert 60 (insert 56 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) := by decide +kernel
  have hoEq : occupied485522 = (insert 109 (insert 97 (insert 81 (insert 78 (insert 70 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) := by decide +kernel
  rw [hmEq, hoEq]
  exact OmissionResidual32Contexts.node485522
#print axioms geometric_node485522

def missing30 : Finset (Fin 154) := {25, 27, 47, 54, 67, 81, 112}
def occupied30 : Finset (Fin 154) := {12, 20, 34, 43, 44, 46, 51, 55, 60, 69, 73, 88, 92, 93, 105, 109}
theorem geometric_node30 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ missing30, i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ occupied30, i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  apply context_impossible_of_exclusion missing30 occupied30 _ c noCap noOctagon noJunction hn hm ho
  have hmEq : missing30 = (insert 112 (insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) := by decide +kernel
  have hoEq : occupied30 = (insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) := by decide +kernel
  rw [hmEq, hoEq]
  exact OmissionResidual32Contexts.node30
#print axioms geometric_node30

#print axioms context_impossible_of_exclusion


/-- The two checked children exclude their shared parent, regardless of state 87. -/
theorem geometric_parent492360 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ missing492359, i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ occupied492360, i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  have missing_eq : missing492360 = insert 87 missing492359 := by decide +kernel
  have occupied_eq : occupied492359 = insert 87 occupied492360 := by decide +kernel
  by_cases hb : (87 : Fin 154) ∈ c.residualOccupied noCap noOctagon noJunction
  · apply geometric_node492359 c noCap noOctagon noJunction hn hm
    intro i hi
    rw [occupied_eq, Finset.mem_insert] at hi
    rcases hi with rfl | hi
    · exact hb
    · exact ho i hi
  · apply geometric_node492360 c noCap noOctagon noJunction hn _ ho
    intro i hi
    rw [missing_eq, Finset.mem_insert] at hi
    rcases hi with rfl | hi
    · exact hb
    · exact hm i hi
#print axioms geometric_parent492360

/-- The two checked children exclude their shared parent, regardless of state 109. -/
theorem geometric_parent485523 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ missing485522, i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ occupied485523, i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  have missing_eq : missing485523 = insert 109 missing485522 := by decide +kernel
  have occupied_eq : occupied485522 = insert 109 occupied485523 := by decide +kernel
  by_cases hb : (109 : Fin 154) ∈ c.residualOccupied noCap noOctagon noJunction
  · apply geometric_node485522 c noCap noOctagon noJunction hn hm
    intro i hi
    rw [occupied_eq, Finset.mem_insert] at hi
    rcases hi with rfl | hi
    · exact hb
    · exact ho i hi
  · apply geometric_node485523 c noCap noOctagon noJunction hn _ ho
    intro i hi
    rw [missing_eq, Finset.mem_insert] at hi
    rcases hi with rfl | hi
    · exact hb
    · exact hm i hi
#print axioms geometric_parent485523
end OmissionResidual32Transfer
