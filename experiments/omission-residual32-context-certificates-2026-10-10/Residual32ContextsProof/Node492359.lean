import Residual32ContextsProof.Catalog
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Contexts
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
-- Conditional arithmetic exclusion; geometric row validity is explicit.
def entries492359 : List (Fin 2469 × ℕ) := [(10, 2), (12, 10), (43, 3), (77, 32), (118, 11), (394, 12), (411, 9), (421, 21), (456, 1), (457, 12), (466, 32), (498, 2), (540, 13), (569, 2), (571, 21), (572, 22), (625, 27), (632, 43), (675, 14), (690, 29), (692, 1), (741, 21), (743, 6), (813, 7), (817, 18), (844, 9), (850, 25), (852, 38), (855, 31), (864, 28), (868, 26), (885, 43), (920, 13), (925, 26), (944, 9), (966, 15), (973, 49), (976, 13), (984, 7), (1010, 9), (1011, 10), (1012, 5), (1031, 11), (1033, 8), (1034, 8), (1044, 7), (1045, 10), (1081, 3), (1086, 9), (1108, 11), (1120, 3), (1123, 18), (1132, 2), (1133, 16), (1137, 3), (1153, 1), (1155, 3), (1172, 17), (1173, 31), (1175, 4), (1177, 11), (1179, 6), (1183, 17), (1184, 3), (1186, 20), (1188, 16), (1201, 34), (1202, 16), (1258, 2), (1316, 8), (1349, 3), (1469, 5), (1572, 3), (1591, 13), (1593, 35), (1640, 6), (1659, 9), (1900, 1), (2008, 13)]
def cs492359 : List ℕ := [57, 34, 28, 54, 101, 100, 3, 80, 100, 76, 58, 32, 99, 100, 101, 11, 88, 100, 99, 89, 83, 101, 0, 100, 0, 245, 100, 0, 86, 59, 100, 100, 26, 101, 201, 101, 73, 99, 67, 99, 86, 77, 9, 16, 213, 204, 101, 26, 47, 0, 165, 102, 55, 100, 100, 100, 100, 63, 77, 85, 26, 100, 77, 100, 81, 152, 100, 20, 101, 100, 90, 99, 101, 63, 100, 100, 98, 90, 165, 100, 100, 100, 100, 47, 100, 98, 99, 171, 48, 100, 99, 100, 70, 0, 51, 90, 100, 98, 99, 99, 91, 101, 100, 100, 70, 84, 99, 96, 101, 37, 100, 100, 100, 99, 100, 100, 100, 100, 100, 101, 73, 99, 90, 100, 100, 100, 100, 100, 95, 100, 81, 100, 100, 100, 90, 99, 98, 96, 100, 100, 100, 92, 89, 100, 99, 86, 100, 100, 101, 100, 93, 100, 89, 89]
theorem loads492359 : cs492359.get =
    load (fun i : Fin entries492359.length => support (entries492359.get i).1)
      (fun i => (entries492359.get i).2) := by
  apply load_eq_of_sparse_packed base cs492359 support code
    entries492359 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node492359 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 49 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 87 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs492359 support demand
    entries492359 ((insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 49 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)) ((insert 87 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)) 100 32 loads492359
  decide +kernel
#print axioms node492359
end OmissionResidual32Contexts
