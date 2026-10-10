import Residual32ResumeProof.Context492357
import Residual32ResumeProof.Context29
import Residual32ResumeProof.Context485519
import Residual32ResumeProof.Context492355
import Residual32ResumeProof.Context485517
import Residual32ResumeProof.Context24
import ContextGeometry
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Resume
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open ErdosSzekeres ErdosSzekeres.Omission OmissionResidual32Transfer
theorem geometric_context492357 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ ((insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)), i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ ((insert 78 (insert 65 (insert 50 (insert 49 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  exact context_impossible_of_exclusion ((insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)) ((insert 78 (insert 65 (insert 50 (insert 49 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154))
    Context492357.excludes_context c noCap noOctagon noJunction hn hm ho
#print axioms geometric_context492357
theorem geometric_context29 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ ((insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ ((insert 112 (insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  exact context_impossible_of_exclusion ((insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 112 (insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154))
    Context29.excludes_context c noCap noOctagon noJunction hn hm ho
#print axioms geometric_context29
theorem geometric_context485519 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ ((insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  exact context_impossible_of_exclusion ((insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154))
    Context485519.excludes_context c noCap noOctagon noJunction hn hm ho
#print axioms geometric_context485519
theorem geometric_context492355 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)), i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  exact context_impossible_of_exclusion ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)) ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154))
    Context492355.excludes_context c noCap noOctagon noJunction hn hm ho
#print axioms geometric_context492355
theorem geometric_context485517 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)), i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  exact context_impossible_of_exclusion ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)) ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154))
    Context485517.excludes_context c noCap noOctagon noJunction hn hm ho
#print axioms geometric_context485517
theorem geometric_context24 {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)
    (hm : ∀ i ∈ ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)), i ∉ c.residualOccupied noCap noOctagon noJunction)
    (ho : ∀ i ∈ ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154)), i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by
  exact context_impossible_of_exclusion ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)) ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154))
    Context24.excludes_context c noCap noOctagon noJunction hn hm ho
#print axioms geometric_context24
end OmissionResidual32Resume
