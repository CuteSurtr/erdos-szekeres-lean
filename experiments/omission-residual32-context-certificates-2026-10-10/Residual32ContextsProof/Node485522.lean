import Residual32ContextsProof.Catalog
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Contexts
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
-- Conditional arithmetic exclusion; geometric row validity is explicit.
def entries485522 : List (Fin 2469 × ℕ) := [(0, 29), (72, 38), (91, 5), (275, 6), (302, 9), (304, 19), (347, 23), (392, 9), (409, 1), (472, 4), (483, 1), (498, 25), (550, 31), (552, 64), (571, 30), (616, 3), (737, 8), (739, 8), (740, 27), (741, 5), (812, 4), (813, 24), (819, 17), (851, 23), (870, 5), (872, 4), (874, 25), (887, 1), (940, 22), (942, 6), (962, 31), (963, 16), (964, 22), (966, 9), (971, 18), (972, 26), (973, 54), (1004, 1), (1009, 17), (1010, 14), (1011, 18), (1061, 12), (1069, 5), (1076, 16), (1082, 8), (1099, 1), (1100, 4), (1108, 5), (1122, 9), (1123, 12), (1137, 6), (1138, 3), (1171, 2), (1172, 2), (1173, 16), (1177, 13), (1178, 5), (1179, 18), (1183, 10), (1185, 5), (1186, 27), (1200, 1), (1209, 22), (1217, 8), (1219, 43), (1253, 23), (1273, 1), (1372, 5), (1433, 3), (1482, 19), (1545, 3), (1572, 3), (1660, 8), (1665, 6), (1851, 5), (2457, 7)]
def cs485522 : List ℕ := [82, 44, 12, 44, 98, 9, 0, 101, 100, 0, 39, 101, 100, 40, 90, 95, 101, 100, 90, 31, 74, 1, 0, 151, 100, 100, 101, 146, 38, 20, 101, 0, 37, 100, 69, 99, 151, 19, 38, 78, 63, 79, 88, 2, 185, 99, 0, 3, 0, 100, 100, 99, 31, 100, 100, 99, 10, 51, 100, 44, 0, 99, 87, 47, 101, 99, 99, 13, 100, 89, 111, 99, 100, 83, 57, 99, 99, 97, 113, 99, 3, 206, 100, 100, 70, 99, 99, 74, 23, 100, 99, 85, 98, 100, 81, 100, 100, 118, 99, 99, 99, 91, 87, 99, 68, 100, 98, 81, 88, 213, 96, 99, 100, 98, 100, 100, 99, 99, 100, 99, 100, 98, 86, 99, 99, 97, 99, 99, 94, 99, 100, 89, 100, 98, 99, 99, 99, 100, 100, 99, 91, 99, 100, 99, 99, 90, 99, 94, 99, 99, 99, 99, 99, 97]
theorem loads485522 : cs485522.get =
    load (fun i : Fin entries485522.length => support (entries485522.get i).1)
      (fun i => (entries485522.get i).2) := by
  apply load_eq_of_sparse_packed base cs485522 support code
    entries485522 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node485522 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 88 (insert 67 (insert 60 (insert 56 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 97 (insert 81 (insert 78 (insert 70 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs485522 support demand
    entries485522 ((insert 88 (insert 67 (insert 60 (insert 56 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 109 (insert 97 (insert 81 (insert 78 (insert 70 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)) 100 32 loads485522
  decide +kernel
#print axioms node485522
end OmissionResidual32Contexts
