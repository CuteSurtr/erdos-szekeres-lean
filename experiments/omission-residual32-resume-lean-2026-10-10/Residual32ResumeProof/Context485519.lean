import Residual32ContextsProof.Catalog
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Resume.Context485519
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open OmissionResidual32Contexts
-- The initial context is inherited from the frozen original tree.
def entries1 : List (Fin 2469 × ℕ) := [(4, 13), (43, 8), (77, 55), (179, 26), (472, 14), (483, 5), (498, 34), (550, 26), (552, 56), (690, 6), (692, 16), (730, 17), (731, 1), (739, 27), (740, 26), (742, 6), (798, 1), (812, 17), (851, 24), (868, 8), (870, 23), (872, 39), (887, 27), (891, 1), (902, 9), (922, 15), (931, 1), (942, 18), (943, 41), (944, 3), (962, 56), (963, 14), (964, 22), (965, 1), (972, 32), (973, 53), (975, 1), (1010, 27), (1011, 20), (1012, 12), (1019, 2), (1033, 4), (1034, 8), (1069, 24), (1075, 11), (1077, 1), (1078, 7), (1081, 14), (1082, 7), (1090, 2), (1128, 2), (1137, 15), (1139, 2), (1154, 1), (1159, 10), (1172, 1), (1173, 17), (1178, 15), (1182, 4), (1183, 19), (1186, 28), (1200, 18), (1207, 1), (1209, 4), (1220, 32), (1254, 30), (1316, 4), (1451, 8), (1484, 3), (1516, 1), (1528, 1), (1660, 2), (1851, 19)]
def cs1 : List ℕ := [37, 93, 14, 50, 90, 5, 8, 100, 100, 0, 81, 91, 101, 57, 99, 82, 86, 99, 71, 27, 70, 27, 26, 141, 101, 99, 100, 115, 55, 55, 100, 15, 26, 99, 50, 100, 164, 3, 81, 98, 20, 81, 100, 0, 186, 99, 0, 8, 44, 101, 100, 34, 5, 100, 100, 99, 169, 76, 101, 74, 0, 100, 95, 100, 100, 100, 99, 24, 99, 48, 175, 100, 100, 77, 47, 90, 99, 101, 179, 99, 18, 187, 101, 100, 91, 99, 66, 100, 24, 99, 100, 98, 100, 98, 88, 74, 91, 100, 100, 94, 99, 100, 57, 102, 57, 100, 100, 76, 100, 238, 83, 100, 100, 86, 81, 99, 100, 100, 99, 100, 101, 96, 99, 100, 100, 87, 99, 101, 40, 99, 100, 97, 100, 99, 99, 100, 95, 100, 100, 99, 89, 100, 99, 97, 100, 68, 100, 99, 91, 100, 78, 96, 100, 100]
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
      (∀ i ∈ ((insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs1 support demand
    entries1 ((insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 109 (insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)) 100 32 loads1
  decide +kernel
def entries3 : List (Fin 2469 × ℕ) := [(4, 43), (37, 12), (77, 50), (132, 35), (179, 36), (409, 7), (448, 12), (472, 5), (483, 10), (498, 34), (550, 40), (552, 14), (571, 7), (617, 11), (689, 3), (690, 1), (692, 4), (730, 8), (731, 21), (738, 4), (740, 8), (741, 27), (751, 12), (815, 2), (851, 46), (859, 4), (868, 50), (869, 6), (870, 43), (872, 16), (874, 32), (920, 12), (922, 1), (933, 10), (934, 19), (940, 3), (944, 34), (965, 3), (966, 6), (973, 55), (1009, 10), (1010, 6), (1011, 9), (1012, 2), (1020, 1), (1031, 6), (1043, 5), (1070, 4), (1073, 7), (1075, 13), (1076, 17), (1082, 6), (1089, 5), (1090, 10), (1096, 2), (1123, 6), (1126, 2), (1132, 1), (1137, 7), (1155, 5), (1172, 3), (1173, 18), (1177, 22), (1178, 1), (1179, 13), (1183, 12), (1186, 22), (1188, 17), (1192, 2), (1199, 6), (1218, 50), (1258, 10), (1261, 1), (1286, 10), (1308, 12), (1344, 16), (1354, 1), (1403, 12), (1516, 7), (1555, 6), (1652, 3), (1666, 5), (1701, 3), (2457, 1)]
def cs3 : List ℕ := [0, 101, 55, 2, 97, 80, 6, 101, 101, 0, 100, 99, 100, 54, 101, 54, 100, 100, 100, 19, 100, 6, 36, 170, 69, 248, 83, 106, 50, 42, 99, 16, 40, 101, 73, 100, 169, 0, 101, 122, 86, 43, 48, 0, 203, 101, 0, 50, 82, 101, 99, 100, 1, 101, 100, 99, 223, 53, 100, 54, 0, 100, 99, 100, 94, 100, 100, 18, 99, 85, 129, 100, 100, 72, 49, 90, 99, 100, 214, 99, 60, 164, 49, 100, 92, 100, 100, 101, 51, 99, 99, 66, 99, 101, 54, 99, 98, 100, 100, 63, 100, 100, 88, 69, 83, 101, 99, 99, 100, 36, 100, 102, 100, 73, 99, 100, 100, 100, 100, 100, 100, 100, 99, 99, 99, 100, 100, 100, 96, 100, 99, 100, 101, 101, 100, 101, 100, 99, 101, 99, 97, 101, 101, 100, 83, 100, 101, 99, 101, 100, 96, 100, 100, 100]
theorem loads3 : cs3.get =
    load (fun i : Fin entries3.length => support (entries3.get i).1)
      (fun i => (entries3.get i).2) := by
  apply load_eq_of_sparse_packed base cs3 support code
    entries3 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node3 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 25 (insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs3 support demand
    entries3 ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 25 (insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)) 100 32 loads3
  decide +kernel
def entries4 : List (Fin 2469 × ℕ) := [(179, 645), (273, 112), (409, 127), (472, 147), (498, 144), (550, 138), (552, 491), (571, 210), (692, 62), (731, 206), (737, 16), (739, 89), (740, 47), (741, 324), (742, 36), (812, 42), (813, 99), (814, 142), (815, 184), (851, 348), (859, 144), (870, 344), (872, 82), (874, 357), (891, 73), (902, 150), (922, 162), (930, 226), (934, 27), (940, 48), (944, 418), (962, 114), (965, 189), (966, 235), (973, 583), (1009, 76), (1010, 49), (1011, 9), (1033, 30), (1034, 88), (1045, 150), (1061, 41), (1073, 96), (1075, 76), (1076, 124), (1081, 195), (1082, 131), (1089, 13), (1090, 213), (1096, 40), (1108, 1), (1123, 39), (1128, 165), (1133, 29), (1137, 65), (1172, 69), (1173, 183), (1177, 233), (1182, 89), (1186, 69), (1219, 354), (1253, 151), (1261, 13), (1276, 56), (1310, 23), (1317, 8), (1344, 40), (1354, 51), (1370, 91), (1403, 200), (1469, 71), (1633, 56), (1652, 22), (1705, 13), (1901, 207), (1991, 38), (2141, 15), (2458, 78), (2468, 5)]
def cs4 : List ℕ := [151, 354, 147, 354, 499, 0, 0, 1000, 646, 0, 0, 849, 1000, 646, 0, 629, 652, 698, 1000, 210, 505, 73, 645, 799, 776, 0, 1000, 1263, 94, 645, 999, 162, 250, 1000, 606, 1000, 1586, 0, 871, 1129, 556, 304, 924, 0, 2255, 999, 94, 226, 945, 1000, 999, 560, 0, 1000, 1000, 1000, 1285, 659, 1002, 584, 0, 1001, 999, 518, 1000, 999, 1000, 89, 999, 867, 1300, 1001, 999, 903, 377, 494, 1000, 1000, 1373, 999, 526, 2346, 1000, 999, 1001, 1000, 1000, 999, 322, 1001, 1000, 751, 1000, 992, 704, 999, 999, 999, 999, 820, 999, 999, 898, 999, 557, 999, 999, 1001, 1000, 183, 999, 1293, 999, 903, 978, 1000, 1000, 1000, 1000, 999, 1000, 998, 1000, 1000, 999, 976, 999, 999, 692, 1000, 1000, 999, 999, 999, 1000, 1000, 999, 999, 999, 1000, 613, 999, 999, 1001, 491, 970, 999, 1000, 999, 1000, 788, 1000, 805, 708]
theorem loads4 : cs4.get =
    load (fun i : Fin entries4.length => support (entries4.get i).1)
      (fun i => (entries4.get i).2) := by
  apply load_eq_of_sparse_packed base cs4 support code
    entries4 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node4 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 25 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs4 support demand
    entries4 ((insert 25 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))))) : Finset (Fin 154)) ((insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)) 1000 32 loads4
  decide +kernel
theorem node2 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154))
    25 node3 node4
theorem node0 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154))
    109 node1 node2
theorem excludes_context :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 88 (insert 67 (insert 60 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 56 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact node0
#print axioms excludes_context
end OmissionResidual32Resume.Context485519
