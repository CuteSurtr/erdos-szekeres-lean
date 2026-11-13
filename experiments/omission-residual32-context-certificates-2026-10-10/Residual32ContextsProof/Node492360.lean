import Residual32ContextsProof.Catalog
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Contexts
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
-- Conditional arithmetic exclusion; geometric row validity is explicit.
def entries492360 : List (Fin 2469 × ℕ) := [(12, 26), (64, 2), (72, 3), (77, 15), (118, 11), (179, 3), (250, 1), (352, 2), (394, 11), (409, 4), (421, 14), (466, 10), (498, 8), (540, 17), (571, 3), (572, 23), (625, 24), (632, 48), (692, 1), (741, 17), (743, 18), (842, 3), (850, 48), (852, 29), (855, 3), (857, 1), (864, 11), (878, 25), (883, 27), (885, 32), (920, 17), (924, 20), (925, 23), (944, 22), (966, 34), (973, 53), (997, 11), (1004, 1), (1009, 16), (1010, 6), (1044, 3), (1049, 7), (1076, 17), (1086, 1), (1121, 3), (1122, 1), (1123, 23), (1128, 4), (1131, 5), (1132, 13), (1133, 3), (1155, 9), (1159, 7), (1160, 1), (1169, 7), (1172, 11), (1173, 14), (1175, 10), (1177, 10), (1179, 14), (1186, 24), (1188, 17), (1201, 25), (1202, 9), (1217, 21), (1222, 10), (1277, 2), (1466, 6), (1560, 3), (1572, 12), (1584, 6), (1591, 8), (1593, 41), (1637, 6), (1640, 23), (1659, 9), (1747, 7), (1900, 5), (2008, 16), (2225, 9)]
def cs492360 : List ℕ := [40, 35, 72, 73, 100, 100, 1, 75, 99, 70, 24, 41, 100, 99, 100, 24, 100, 99, 99, 100, 84, 99, 3, 100, 0, 225, 100, 22, 97, 67, 100, 99, 43, 100, 231, 100, 39, 100, 75, 99, 81, 89, 30, 7, 236, 206, 100, 0, 65, 10, 189, 100, 59, 99, 100, 99, 100, 98, 76, 53, 43, 100, 100, 100, 77, 132, 100, 59, 101, 100, 79, 100, 89, 73, 100, 100, 98, 88, 127, 100, 101, 100, 99, 64, 100, 94, 99, 25, 37, 100, 100, 65, 90, 0, 79, 95, 100, 49, 101, 61, 97, 100, 83, 101, 99, 98, 102, 100, 101, 41, 100, 101, 93, 57, 101, 100, 101, 100, 100, 100, 61, 100, 99, 100, 101, 101, 99, 101, 88, 100, 93, 100, 100, 101, 100, 100, 99, 94, 100, 101, 100, 100, 97, 101, 101, 95, 67, 101, 100, 100, 101, 100, 101, 89]
theorem loads492360 : cs492360.get =
    load (fun i : Fin entries492360.length => support (entries492360.get i).1)
      (fun i => (entries492360.get i).2) := by
  apply load_eq_of_sparse_packed base cs492360 support code
    entries492360 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node492360 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 93 (insert 88 (insert 87 (insert 67 (insert 60 (insert 49 (insert 47 (insert 43 (insert 27 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs492360 support demand
    entries492360 ((insert 109 (insert 93 (insert 88 (insert 87 (insert 67 (insert 60 (insert 49 (insert 47 (insert 43 (insert 27 ∅)))))))))) : Finset (Fin 154)) ((insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))) : Finset (Fin 154)) 100 32 loads492360
  decide +kernel
#print axioms node492360
end OmissionResidual32Contexts
