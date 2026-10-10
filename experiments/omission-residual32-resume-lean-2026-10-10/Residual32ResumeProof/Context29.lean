import Residual32ContextsProof.Catalog
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Resume.Context29
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open OmissionResidual32Contexts
-- The initial context is inherited from the frozen original tree.
def entries1 : List (Fin 2469 × ℕ) := [(7, 120), (199, 48), (229, 172), (250, 40), (275, 58), (313, 29), (466, 66), (475, 29), (484, 29), (572, 107), (610, 24), (640, 7), (730, 37), (777, 31), (781, 51), (798, 53), (834, 39), (850, 63), (873, 107), (876, 40), (878, 40), (903, 79), (904, 37), (905, 55), (912, 135), (920, 9), (926, 10), (941, 101), (944, 26), (945, 9), (946, 30), (948, 36), (950, 8), (954, 8), (963, 85), (967, 69), (968, 77), (971, 37), (972, 82), (973, 141), (978, 17), (995, 69), (996, 1), (1009, 11), (1016, 1), (1028, 17), (1031, 14), (1043, 5), (1061, 26), (1076, 36), (1081, 1), (1103, 18), (1108, 1), (1123, 18), (1140, 6), (1141, 15), (1143, 17), (1155, 32), (1167, 55), (1173, 32), (1175, 16), (1176, 12), (1177, 26), (1179, 46), (1182, 13), (1183, 10), (1186, 55), (1212, 1), (1223, 67), (1236, 11), (1254, 30), (1348, 43), (1349, 12), (1358, 54), (1443, 41), (1488, 8), (1497, 6), (1572, 3), (1580, 17), (1585, 10), (1685, 30), (1691, 11), (1710, 5), (1932, 11)]
def cs1 : List ℕ := [198, 150, 0, 92, 256, 40, 0, 256, 97, 0, 0, 257, 349, 255, 120, 41, 257, 255, 256, 107, 348, 161, 30, 257, 254, 0, 255, 0, 256, 165, 257, 255, 137, 255, 522, 256, 256, 256, 30, 254, 255, 257, 26, 149, 508, 256, 456, 0, 160, 251, 256, 384, 0, 255, 145, 627, 254, 255, 257, 256, 364, 256, 103, 176, 213, 256, 254, 265, 255, 457, 255, 255, 255, 272, 257, 256, 257, 184, 610, 255, 257, 0, 256, 253, 257, 256, 256, 255, 776, 249, 255, 254, 288, 678, 256, 175, 256, 255, 258, 255, 256, 255, 255, 257, 140, 551, 235, 187, 214, 629, 256, 255, 389, 255, 241, 210, 256, 256, 256, 255, 257, 257, 188, 257, 255, 245, 256, 256, 257, 256, 256, 256, 256, 256, 256, 256, 235, 256, 256, 255, 256, 244, 256, 256, 257, 247, 256, 253, 256, 256, 229, 256, 256, 239]
theorem loads1 : cs1.get =
    load (fun i : Fin entries1.length => support (entries1.get i).1)
      (fun i => (entries1.get i).2) := by
  apply load_eq_of_sparse_packed base cs1 support code
    entries1 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node1 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 78 (insert 112 (insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs1 support demand
    entries1 ((insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 78 (insert 112 (insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))))) : Finset (Fin 154)) 256 32 loads1
  decide +kernel
def entries2 : List (Fin 2469 × ℕ) := [(6, 2), (7, 142), (54, 22), (122, 49), (201, 41), (269, 36), (340, 28), (441, 1), (443, 34), (466, 91), (475, 41), (484, 41), (503, 2), (507, 10), (542, 2), (572, 72), (577, 23), (617, 20), (624, 46), (673, 21), (674, 44), (737, 3), (781, 53), (797, 28), (798, 68), (834, 31), (850, 29), (873, 104), (876, 59), (904, 19), (905, 151), (912, 123), (920, 51), (926, 32), (941, 91), (944, 1), (945, 3), (946, 43), (954, 27), (956, 28), (967, 89), (968, 82), (971, 49), (972, 77), (973, 137), (978, 24), (981, 34), (995, 44), (1009, 19), (1028, 5), (1031, 13), (1061, 17), (1100, 16), (1103, 32), (1108, 34), (1123, 13), (1139, 15), (1141, 12), (1143, 23), (1147, 8), (1149, 22), (1155, 46), (1167, 58), (1175, 12), (1176, 22), (1177, 24), (1179, 48), (1182, 17), (1186, 13), (1212, 14), (1223, 55), (1254, 10), (1316, 6), (1346, 17), (1348, 96), (1358, 60), (1401, 39), (1443, 29), (1488, 23), (1497, 3), (1685, 65), (1931, 10), (1952, 39)]
def cs2 : List ℕ := [206, 154, 0, 70, 246, 41, 0, 257, 99, 10, 0, 257, 402, 256, 110, 114, 257, 255, 257, 72, 351, 256, 65, 257, 255, 0, 257, 0, 256, 188, 257, 234, 160, 257, 523, 256, 256, 256, 65, 255, 255, 248, 29, 248, 500, 256, 494, 0, 256, 256, 256, 335, 58, 256, 77, 610, 256, 256, 256, 257, 407, 255, 125, 172, 256, 248, 257, 226, 256, 355, 256, 256, 203, 567, 256, 256, 256, 257, 17, 255, 255, 0, 256, 257, 256, 256, 256, 256, 721, 256, 256, 256, 309, 670, 256, 180, 175, 256, 256, 256, 256, 256, 257, 256, 147, 387, 220, 192, 185, 593, 256, 256, 483, 178, 216, 215, 256, 257, 256, 256, 257, 256, 137, 244, 230, 239, 256, 256, 256, 257, 256, 256, 257, 256, 256, 257, 217, 256, 257, 257, 256, 252, 226, 256, 257, 253, 257, 256, 256, 220, 244, 223, 243, 210]
theorem loads2 : cs2.get =
    load (fun i : Fin entries2.length => support (entries2.get i).1)
      (fun i => (entries2.get i).2) := by
  apply load_eq_of_sparse_packed base cs2 support code
    entries2 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node2 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 112 (insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs2 support demand
    entries2 ((insert 78 (insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 112 (insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)) 256 32 loads2
  decide +kernel
theorem node0 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 112 (insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 112 (insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154))
    78 node1 node2
theorem excludes_context :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 112 (insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact node0
#print axioms excludes_context
end OmissionResidual32Resume.Context29
