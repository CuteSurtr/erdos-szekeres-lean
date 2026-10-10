import Residual32ContextsProof.Catalog
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Resume.Context24
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open OmissionResidual32Contexts
-- The initial context is inherited from the frozen original tree.
def entries37 : List (Fin 2469 × ℕ) := [(229, 1)]
def cs37 : List ℕ := [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
theorem loads37 : cs37.get =
    load (fun i : Fin entries37.length => support (entries37.get i).1)
      (fun i => (entries37.get i).2) := by
  apply load_eq_of_sparse_packed base cs37 support code
    entries37 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node37 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 28 (insert 78 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs37 support demand
    entries37 ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)) ((insert 28 (insert 78 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))))) : Finset (Fin 154)) 0 32 loads37
  decide +kernel
def entries38 : List (Fin 2469 × ℕ) := [(62, 1), (177, 6), (199, 1), (275, 10), (312, 7), (325, 7), (420, 1), (468, 19), (570, 1), (571, 11), (577, 2), (673, 15), (674, 4), (693, 2), (730, 10), (798, 7), (819, 1), (850, 9), (852, 5), (873, 7), (874, 14), (876, 7), (903, 2), (904, 6), (906, 4), (912, 23), (918, 18), (940, 1), (941, 14), (943, 3), (944, 5), (946, 6), (947, 17), (963, 13), (964, 7), (966, 1), (967, 1), (968, 14), (971, 3), (972, 8), (973, 16), (978, 3), (995, 4), (996, 3), (1009, 2), (1012, 2), (1022, 2), (1030, 1), (1043, 1), (1044, 1), (1061, 3), (1069, 3), (1081, 5), (1103, 2), (1123, 3), (1128, 3), (1133, 3), (1138, 2), (1139, 1), (1141, 1), (1143, 2), (1154, 2), (1162, 1), (1167, 9), (1173, 5), (1177, 2), (1179, 1), (1181, 2), (1183, 7), (1186, 7), (1237, 3), (1443, 5), (1500, 1), (2270, 10)]
def cs38 : List ℕ := [0, 32, 10, 19, 8, 13, 0, 37, 10, 1, 0, 32, 41, 32, 7, 0, 32, 31, 31, 12, 41, 10, 6, 32, 26, 0, 31, 0, 0, 29, 32, 32, 10, 31, 36, 31, 32, 32, 7, 32, 32, 32, 8, 24, 70, 31, 33, 0, 23, 32, 31, 40, 0, 31, 10, 95, 32, 32, 24, 32, 33, 32, 15, 23, 32, 29, 33, 59, 32, 70, 32, 32, 33, 32, 24, 32, 31, 30, 68, 31, 32, 79, 32, 33, 32, 31, 31, 32, 124, 31, 33, 31, 16, 115, 33, 31, 32, 31, 32, 23, 32, 31, 24, 32, 27, 107, 24, 26, 27, 83, 31, 32, 32, 32, 32, 31, 32, 33, 32, 32, 32, 32, 27, 32, 32, 32, 31, 32, 32, 32, 32, 31, 31, 33, 33, 32, 27, 29, 32, 32, 33, 30, 32, 32, 32, 24, 33, 32, 32, 32, 32, 30, 29, 30]
theorem loads38 : cs38.get =
    load (fun i : Fin entries38.length => support (entries38.get i).1)
      (fun i => (entries38.get i).2) := by
  apply load_eq_of_sparse_packed base cs38 support code
    entries38 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node38 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 28 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 78 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs38 support demand
    entries38 ((insert 28 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 78 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)) 32 32 loads38
  decide +kernel
theorem node27 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 78 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)) ((insert 78 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154))
    28 node37 node38
def entries35 : List (Fin 2469 × ℕ) := [(17, 56), (43, 54), (62, 37), (96, 18), (116, 5), (122, 39), (325, 156), (361, 5), (427, 47), (468, 203), (577, 8), (622, 64), (624, 11), (673, 59), (780, 42), (783, 2), (798, 69), (850, 56), (852, 42), (874, 60), (876, 57), (904, 71), (905, 38), (912, 191), (918, 73), (919, 13), (920, 60), (940, 20), (942, 23), (943, 87), (944, 28), (947, 67), (952, 7), (968, 69), (971, 80), (972, 42), (973, 139), (978, 12), (994, 1), (995, 60), (1009, 55), (1012, 18), (1061, 13), (1069, 20), (1075, 24), (1076, 33), (1099, 9), (1100, 5), (1101, 13), (1102, 13), (1104, 1), (1123, 37), (1141, 28), (1147, 19), (1155, 9), (1167, 48), (1176, 20), (1177, 48), (1179, 6), (1181, 16), (1183, 6), (1185, 22), (1186, 68), (1211, 7), (1237, 26), (1346, 41), (1372, 56), (1443, 21), (1469, 90), (1556, 46), (1559, 38), (1619, 64), (1685, 9), (1845, 23), (1954, 81), (2008, 2), (2169, 1), (2270, 27)]
def cs35 : List ℕ := [0, 256, 27, 141, 149, 53, 54, 379, 166, 103, 0, 256, 393, 256, 111, 53, 256, 255, 256, 37, 321, 190, 9, 256, 226, 0, 256, 0, 256, 256, 256, 256, 64, 256, 344, 257, 396, 247, 51, 256, 256, 255, 115, 177, 592, 255, 450, 0, 245, 256, 255, 318, 0, 256, 42, 815, 256, 256, 255, 257, 257, 256, 184, 186, 256, 208, 256, 334, 256, 597, 522, 239, 254, 256, 227, 418, 256, 216, 89, 255, 256, 780, 226, 255, 250, 255, 255, 256, 882, 232, 256, 242, 257, 741, 237, 256, 228, 255, 256, 257, 255, 255, 256, 256, 153, 799, 256, 255, 242, 486, 256, 255, 256, 195, 256, 255, 256, 255, 256, 255, 388, 256, 256, 256, 256, 243, 255, 255, 227, 255, 255, 255, 256, 255, 255, 256, 227, 256, 256, 255, 255, 203, 255, 248, 255, 209, 256, 255, 244, 255, 256, 255, 255, 244]
theorem loads35 : cs35.get =
    load (fun i : Fin entries35.length => support (entries35.get i).1)
      (fun i => (entries35.get i).2) := by
  apply load_eq_of_sparse_packed base cs35 support code
    entries35 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node35 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 70 (insert 120 (insert 75 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs35 support demand
    entries35 ((insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 70 (insert 120 (insert 75 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))))) : Finset (Fin 154)) 256 32 loads35
  decide +kernel
def entries36 : List (Fin 2469 × ℕ) := [(17, 105), (340, 4), (361, 42), (427, 67), (468, 228), (545, 75), (571, 34), (577, 77), (622, 95), (672, 19), (673, 87), (674, 13), (798, 64), (819, 30), (850, 77), (852, 38), (873, 62), (874, 86), (904, 57), (905, 76), (912, 179), (918, 123), (923, 32), (939, 10), (941, 63), (942, 47), (943, 59), (944, 6), (963, 17), (966, 1), (968, 91), (971, 53), (972, 71), (973, 138), (978, 27), (995, 32), (1009, 44), (1012, 9), (1022, 4), (1033, 5), (1034, 8), (1049, 35), (1061, 22), (1069, 26), (1076, 6), (1102, 10), (1103, 19), (1123, 26), (1139, 4), (1141, 22), (1155, 11), (1162, 15), (1167, 48), (1173, 7), (1176, 19), (1177, 48), (1179, 10), (1183, 22), (1184, 18), (1186, 70), (1237, 28), (1316, 3), (1372, 3), (1443, 23), (1469, 67), (1559, 32), (1619, 28), (1621, 6), (1655, 20), (1685, 62), (1845, 20), (1849, 7), (1954, 95)]
def cs36 : List ℕ := [0, 256, 0, 182, 161, 28, 0, 389, 200, 28, 0, 256, 428, 256, 75, 62, 256, 257, 256, 34, 408, 167, 62, 256, 189, 0, 250, 0, 256, 241, 256, 256, 60, 256, 339, 256, 511, 256, 62, 256, 256, 120, 69, 267, 611, 257, 523, 0, 231, 256, 229, 290, 4, 257, 45, 727, 255, 256, 234, 256, 256, 256, 129, 188, 256, 258, 256, 372, 255, 598, 47, 255, 256, 256, 256, 370, 256, 257, 47, 256, 256, 502, 256, 255, 230, 257, 257, 247, 755, 255, 256, 241, 147, 519, 255, 257, 257, 256, 255, 255, 256, 257, 256, 255, 232, 567, 134, 213, 209, 573, 249, 256, 225, 201, 192, 235, 256, 255, 256, 257, 387, 183, 210, 256, 254, 257, 257, 257, 249, 255, 255, 257, 257, 256, 256, 256, 238, 257, 255, 256, 255, 231, 245, 255, 255, 230, 257, 256, 256, 256, 253, 256, 254, 241]
theorem loads36 : cs36.get =
    load (fun i : Fin entries36.length => support (entries36.get i).1)
      (fun i => (entries36.get i).2) := by
  apply load_eq_of_sparse_packed base cs36 support code
    entries36 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node36 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 70 (insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 120 (insert 75 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs36 support demand
    entries36 ((insert 70 (insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 120 (insert 75 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))))) : Finset (Fin 154)) 256 32 loads36
  decide +kernel
theorem node33 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 120 (insert 75 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 120 (insert 75 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))))) : Finset (Fin 154))
    70 node35 node36
def entries34 : List (Fin 2469 × ℕ) := [(17, 66), (43, 9), (62, 16), (95, 23), (116, 24), (325, 82), (461, 9), (464, 22), (468, 206), (507, 49), (545, 29), (571, 20), (577, 55), (622, 41), (624, 41), (673, 106), (674, 21), (780, 5), (783, 19), (798, 81), (850, 40), (852, 64), (873, 2), (874, 101), (904, 61), (905, 55), (912, 201), (918, 95), (919, 19), (920, 2), (941, 34), (942, 54), (943, 78), (944, 44), (963, 26), (967, 50), (969, 14), (971, 1), (972, 44), (973, 125), (978, 49), (995, 54), (1004, 6), (1005, 3), (1006, 39), (1009, 39), (1012, 10), (1048, 5), (1049, 4), (1069, 15), (1100, 9), (1103, 36), (1114, 30), (1120, 8), (1123, 21), (1139, 6), (1142, 15), (1155, 24), (1167, 44), (1176, 24), (1177, 33), (1179, 54), (1183, 27), (1185, 2), (1186, 56), (1212, 20), (1237, 1), (1310, 40), (1348, 65), (1374, 46), (1443, 33), (1540, 15), (1618, 41), (1641, 3), (1685, 46), (1689, 21), (1954, 71), (2169, 25), (2270, 48)]
def cs34 : List ℕ := [0, 255, 48, 154, 136, 49, 9, 390, 185, 106, 0, 255, 366, 256, 38, 70, 255, 256, 256, 36, 339, 193, 46, 255, 255, 0, 255, 0, 257, 256, 255, 256, 90, 256, 370, 256, 466, 241, 86, 257, 256, 225, 131, 306, 599, 256, 507, 0, 192, 255, 256, 298, 0, 257, 64, 776, 256, 256, 220, 257, 256, 256, 212, 172, 255, 254, 256, 413, 255, 571, 257, 256, 231, 256, 257, 407, 255, 256, 53, 256, 255, 571, 189, 256, 150, 257, 255, 235, 752, 252, 256, 247, 255, 722, 256, 256, 228, 255, 256, 255, 254, 257, 147, 257, 244, 613, 224, 257, 205, 450, 257, 257, 255, 217, 258, 255, 254, 254, 257, 256, 45, 256, 255, 256, 254, 247, 256, 256, 249, 255, 254, 226, 257, 255, 254, 254, 202, 223, 255, 255, 254, 222, 218, 222, 254, 256, 255, 245, 255, 255, 255, 255, 255, 254]
theorem loads34 : cs34.get =
    load (fun i : Fin entries34.length => support (entries34.get i).1)
      (fun i => (entries34.get i).2) := by
  apply load_eq_of_sparse_packed base cs34 support code
    entries34 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node34 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 120 (insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 75 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs34 support demand
    entries34 ((insert 120 (insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 75 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)) 256 32 loads34
  decide +kernel
theorem node29 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 75 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 75 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154))
    120 node33 node34
def entries31 : List (Fin 2469 × ℕ) := [(17, 378), (43, 210), (62, 136), (122, 45), (325, 515), (401, 49), (465, 234), (468, 1000), (571, 98), (577, 9), (622, 287), (674, 285), (739, 33), (798, 382), (813, 6), (815, 127), (819, 195), (850, 130), (859, 101), (864, 384), (874, 486), (876, 254), (904, 214), (905, 164), (912, 737), (918, 469), (919, 71), (920, 7), (924, 80), (940, 33), (941, 9), (942, 234), (943, 466), (944, 34), (947, 364), (952, 42), (967, 164), (968, 123), (971, 237), (972, 148), (973, 577), (978, 54), (996, 4), (1006, 22), (1009, 173), (1015, 49), (1044, 71), (1061, 41), (1075, 6), (1076, 42), (1099, 149), (1100, 59), (1101, 9), (1103, 166), (1104, 71), (1113, 14), (1114, 187), (1123, 186), (1167, 228), (1174, 41), (1175, 83), (1179, 6), (1181, 56), (1182, 53), (1184, 100), (1186, 195), (1348, 256), (1469, 249), (1488, 13), (1528, 36), (1540, 30), (1559, 111), (1685, 53), (1689, 145), (1845, 22), (1846, 104), (1954, 417), (2169, 75)]
def cs31 : List ℕ := [0, 1000, 0, 508, 417, 0, 210, 1417, 896, 520, 0, 1000, 1648, 1000, 464, 98, 1000, 1000, 1000, 234, 1263, 686, 53, 1000, 378, 0, 1000, 0, 1001, 1000, 1000, 1000, 80, 1000, 1502, 1001, 1706, 867, 189, 1000, 1001, 1001, 500, 730, 2529, 999, 1868, 0, 714, 1000, 1001, 1865, 0, 1000, 225, 2891, 1001, 1000, 1000, 1001, 999, 1001, 882, 616, 1000, 538, 1000, 1543, 1000, 2509, 1718, 820, 930, 1001, 1000, 6, 1000, 830, 473, 1001, 616, 3088, 668, 1001, 1001, 803, 687, 998, 3163, 1000, 1000, 676, 769, 3659, 974, 1000, 989, 1001, 1000, 1000, 1001, 1032, 1000, 1001, 166, 3335, 760, 1001, 799, 2021, 1000, 1000, 1000, 892, 999, 1001, 1000, 1001, 999, 1000, 1001, 998, 906, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 999, 1001, 1001, 1000, 786, 999, 1000, 1000, 1001, 917, 1000, 958, 1000, 888, 1000, 1000, 1001, 1000, 1000, 1000, 987, 772]
theorem loads31 : cs31.get =
    load (fun i : Fin entries31.length => support (entries31.get i).1)
      (fun i => (entries31.get i).2) := by
  apply load_eq_of_sparse_packed base cs31 support code
    entries31 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node31 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 75 (insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 70 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs31 support demand
    entries31 ((insert 75 (insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 70 (insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)) 1000 32 loads31
  decide +kernel
def entries32 : List (Fin 2469 × ℕ) := [(7, 25), (17, 56), (54, 12), (62, 51), (355, 3), (465, 5), (468, 214), (475, 12), (484, 12), (542, 12), (570, 11), (571, 55), (577, 43), (622, 55), (674, 77), (738, 1), (758, 6), (776, 34), (797, 24), (798, 83), (812, 19), (819, 21), (844, 12), (850, 72), (859, 6), (873, 27), (874, 81), (876, 52), (891, 23), (903, 17), (904, 9), (905, 84), (912, 148), (918, 146), (923, 7), (939, 88), (941, 53), (943, 56), (944, 40), (945, 23), (963, 37), (967, 19), (968, 36), (971, 50), (972, 57), (973, 141), (978, 26), (1006, 3), (1009, 32), (1031, 8), (1043, 3), (1044, 6), (1048, 21), (1061, 8), (1100, 8), (1103, 40), (1104, 4), (1113, 34), (1114, 28), (1123, 19), (1128, 12), (1132, 17), (1138, 11), (1139, 2), (1141, 9), (1143, 19), (1147, 8), (1155, 5), (1167, 48), (1175, 29), (1179, 41), (1183, 32), (1186, 67), (1238, 13), (1348, 33), (1443, 4), (1469, 83), (1497, 32), (1540, 18), (1619, 29), (1685, 85), (1846, 18), (1848, 22), (1954, 109), (2270, 17)]
def cs32 : List ℕ := [25, 256, 30, 157, 134, 29, 0, 365, 213, 80, 0, 256, 479, 257, 64, 85, 256, 256, 256, 106, 363, 206, 85, 256, 169, 12, 256, 23, 256, 233, 256, 257, 60, 256, 373, 256, 416, 256, 136, 256, 256, 165, 96, 290, 599, 256, 464, 0, 256, 256, 256, 368, 12, 255, 35, 653, 246, 255, 255, 256, 255, 255, 203, 165, 257, 256, 256, 374, 255, 632, 52, 255, 255, 256, 256, 62, 256, 256, 86, 256, 205, 486, 220, 255, 223, 243, 184, 256, 614, 256, 256, 175, 81, 604, 256, 256, 256, 255, 256, 255, 256, 255, 162, 257, 94, 606, 207, 256, 256, 435, 256, 256, 256, 202, 210, 246, 257, 256, 257, 256, 255, 256, 257, 257, 256, 256, 257, 257, 256, 258, 257, 256, 257, 256, 257, 256, 194, 256, 256, 257, 256, 222, 243, 256, 258, 251, 255, 256, 256, 257, 257, 256, 257, 245]
theorem loads32 : cs32.get =
    load (fun i : Fin entries32.length => support (entries32.get i).1)
      (fun i => (entries32.get i).2) := by
  apply load_eq_of_sparse_packed base cs32 support code
    entries32 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node32 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 70 (insert 75 (insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs32 support demand
    entries32 ((insert 70 (insert 75 (insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)) ((insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)) 256 32 loads32
  decide +kernel
theorem node30 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 75 (insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 75 (insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154))
    70 node31 node32
theorem node28 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 78 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154))
    75 node29 node30
theorem node13 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)) ((insert 7 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154))
    78 node27 node28
def entries25 : List (Fin 2469 × ℕ) := [(7, 3), (17, 73), (43, 16), (62, 25), (229, 49), (275, 1), (325, 133), (415, 9), (483, 96), (527, 4), (531, 34), (542, 59), (622, 33), (673, 66), (674, 10), (780, 41), (781, 41), (782, 2), (798, 53), (813, 6), (850, 51), (859, 44), (860, 98), (874, 54), (901, 7), (902, 11), (904, 67), (905, 43), (912, 193), (918, 113), (920, 32), (940, 24), (942, 48), (943, 96), (944, 11), (946, 12), (947, 88), (964, 70), (968, 82), (971, 54), (972, 55), (973, 122), (978, 17), (995, 56), (1006, 1), (1009, 63), (1012, 35), (1069, 38), (1075, 50), (1076, 11), (1100, 21), (1101, 32), (1103, 20), (1123, 26), (1139, 15), (1141, 24), (1155, 30), (1167, 55), (1173, 14), (1176, 17), (1177, 55), (1179, 9), (1181, 12), (1182, 3), (1183, 20), (1186, 60), (1212, 19), (1248, 1), (1269, 26), (1273, 5), (1277, 1), (1346, 29), (1372, 66), (1443, 10), (1469, 75), (1556, 3), (1559, 52), (1619, 51), (1685, 47), (1845, 3), (2410, 40)]
def cs25 : List ℕ := [40, 3, 0, 124, 43, 96, 16, 0, 255, 76, 0, 40, 333, 255, 115, 47, 136, 255, 256, 25, 99, 139, 47, 117, 257, 0, 257, 0, 256, 256, 58, 255, 52, 255, 328, 256, 425, 244, 72, 256, 256, 256, 107, 117, 615, 256, 442, 0, 237, 257, 256, 321, 59, 206, 156, 721, 256, 256, 256, 255, 255, 255, 160, 256, 256, 243, 255, 396, 256, 629, 457, 202, 256, 256, 231, 477, 264, 222, 256, 256, 256, 781, 255, 256, 242, 256, 257, 254, 1013, 230, 256, 256, 257, 803, 221, 256, 254, 256, 257, 256, 257, 257, 256, 256, 199, 878, 254, 255, 232, 511, 256, 255, 257, 245, 256, 256, 257, 257, 255, 256, 401, 256, 256, 256, 257, 255, 256, 257, 252, 257, 257, 249, 256, 257, 257, 256, 246, 251, 256, 257, 257, 206, 256, 257, 258, 218, 255, 256, 256, 256, 256, 256, 251, 257]
theorem loads25 : cs25.get =
    load (fun i : Fin entries25.length => support (entries25.get i).1)
      (fun i => (entries25.get i).2) := by
  apply load_eq_of_sparse_packed base cs25 support code
    entries25 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node25 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 70 (insert 120 (insert 75 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs25 support demand
    entries25 ((insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 70 (insert 120 (insert 75 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))))) : Finset (Fin 154)) 256 32 loads25
  decide +kernel
def entries26 : List (Fin 2469 × ℕ) := [(7, 46), (17, 95), (62, 10), (116, 28), (229, 56), (275, 39), (483, 98), (484, 101), (507, 32), (542, 95), (545, 19), (571, 31), (577, 22), (622, 52), (673, 93), (693, 15), (731, 25), (776, 3), (798, 47), (819, 7), (834, 6), (850, 15), (859, 23), (860, 125), (873, 6), (874, 46), (901, 10), (903, 32), (904, 36), (905, 57), (912, 139), (918, 116), (923, 24), (939, 14), (941, 88), (942, 13), (943, 38), (944, 27), (945, 26), (946, 33), (963, 65), (964, 20), (967, 31), (968, 79), (969, 2), (971, 43), (972, 61), (973, 125), (978, 34), (995, 48), (1009, 28), (1012, 5), (1028, 5), (1034, 14), (1049, 14), (1061, 30), (1069, 20), (1075, 18), (1076, 15), (1078, 3), (1101, 15), (1102, 5), (1103, 22), (1123, 27), (1139, 12), (1141, 28), (1155, 17), (1162, 18), (1167, 65), (1173, 38), (1177, 66), (1179, 25), (1183, 42), (1186, 65), (1372, 55), (1443, 23), (1456, 11), (1540, 18), (1559, 76), (1618, 1), (1685, 44), (1845, 5), (1848, 2), (2410, 2)]
def cs26 : List ℕ := [2, 57, 0, 110, 48, 199, 0, 11, 256, 43, 0, 13, 375, 258, 127, 72, 212, 257, 256, 41, 149, 213, 44, 118, 256, 0, 257, 0, 256, 183, 23, 257, 197, 255, 434, 257, 428, 255, 82, 256, 257, 255, 65, 123, 643, 256, 519, 11, 205, 256, 255, 280, 95, 228, 186, 567, 257, 256, 257, 256, 255, 256, 112, 256, 257, 215, 255, 362, 256, 543, 13, 256, 256, 257, 256, 399, 258, 257, 256, 255, 257, 329, 256, 257, 244, 256, 258, 231, 760, 256, 255, 256, 170, 632, 257, 257, 256, 256, 258, 255, 257, 257, 145, 229, 256, 592, 163, 196, 242, 567, 257, 256, 200, 256, 237, 257, 256, 257, 256, 256, 317, 256, 235, 256, 255, 256, 257, 256, 257, 256, 256, 256, 256, 256, 257, 256, 249, 256, 256, 255, 256, 255, 252, 248, 256, 256, 256, 255, 256, 256, 256, 256, 233, 249]
theorem loads26 : cs26.get =
    load (fun i : Fin entries26.length => support (entries26.get i).1)
      (fun i => (entries26.get i).2) := by
  apply load_eq_of_sparse_packed base cs26 support code
    entries26 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node26 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 70 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 120 (insert 75 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs26 support demand
    entries26 ((insert 70 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 120 (insert 75 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)) 256 32 loads26
  decide +kernel
theorem node23 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 120 (insert 75 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 120 (insert 75 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154))
    70 node25 node26
def entries24 : List (Fin 2469 × ℕ) := [(17, 73), (62, 20), (229, 80), (275, 6), (325, 89), (350, 9), (464, 14), (465, 9), (483, 112), (484, 4), (507, 27), (531, 36), (542, 71), (571, 39), (624, 1), (673, 108), (674, 67), (783, 3), (798, 61), (850, 18), (859, 15), (860, 73), (873, 19), (874, 108), (901, 56), (904, 11), (905, 15), (906, 46), (912, 185), (918, 147), (924, 13), (941, 41), (942, 24), (943, 75), (944, 43), (947, 48), (956, 21), (963, 67), (967, 70), (969, 10), (972, 26), (973, 125), (978, 53), (995, 47), (1006, 21), (1009, 43), (1012, 31), (1048, 1), (1069, 12), (1076, 8), (1091, 2), (1103, 49), (1114, 21), (1123, 11), (1139, 20), (1142, 8), (1143, 19), (1155, 38), (1162, 1), (1167, 35), (1173, 18), (1176, 18), (1177, 42), (1179, 39), (1182, 21), (1183, 22), (1186, 53), (1212, 17), (1310, 3), (1348, 101), (1374, 55), (1443, 21), (1516, 14), (1540, 14), (1546, 25), (1547, 12), (1572, 5), (1618, 44), (1685, 71), (2421, 77)]
def cs24 : List ℕ := [0, 77, 0, 91, 77, 116, 0, 0, 238, 91, 0, 77, 299, 256, 148, 71, 193, 256, 256, 59, 148, 144, 71, 204, 255, 0, 256, 0, 256, 256, 133, 256, 94, 256, 301, 256, 487, 207, 91, 256, 256, 255, 118, 186, 540, 258, 504, 0, 219, 255, 256, 288, 92, 256, 106, 673, 256, 256, 194, 257, 256, 256, 200, 243, 255, 248, 257, 486, 255, 664, 256, 256, 256, 256, 213, 418, 270, 212, 256, 256, 256, 630, 257, 255, 138, 257, 257, 256, 928, 256, 256, 256, 256, 984, 255, 256, 217, 256, 256, 255, 256, 256, 86, 256, 243, 851, 256, 256, 257, 464, 256, 255, 256, 223, 255, 257, 256, 255, 256, 256, 26, 256, 231, 256, 255, 256, 257, 256, 248, 255, 255, 234, 256, 255, 227, 255, 221, 200, 256, 255, 255, 220, 228, 214, 256, 256, 256, 230, 256, 252, 256, 256, 256, 255]
theorem loads24 : cs24.get =
    load (fun i : Fin entries24.length => support (entries24.get i).1)
      (fun i => (entries24.get i).2) := by
  apply load_eq_of_sparse_packed base cs24 support code
    entries24 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node24 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 120 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 75 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs24 support demand
    entries24 ((insert 120 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 75 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)) 256 32 loads24
  decide +kernel
theorem node15 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 75 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 75 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154))
    120 node23 node24
def entries21 : List (Fin 2469 × ℕ) := [(229, 1)]
def cs21 : List ℕ := [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
theorem loads21 : cs21.get =
    load (fun i : Fin entries21.length => support (entries21.get i).1)
      (fun i => (entries21.get i).2) := by
  apply load_eq_of_sparse_packed base cs21 support code
    entries21 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node21 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 28 (insert 78 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs21 support demand
    entries21 ((insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 28 (insert 78 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)) 0 32 loads21
  decide +kernel
def entries22 : List (Fin 2469 × ℕ) := [(62, 11), (177, 4), (190, 1), (199, 5), (275, 7), (312, 1), (325, 11), (361, 1), (483, 19), (531, 3), (542, 5), (570, 4), (571, 7), (674, 9), (693, 1), (730, 10), (741, 1), (798, 7), (850, 6), (860, 6), (873, 6), (874, 12), (876, 1), (903, 2), (904, 1), (906, 3), (912, 26), (918, 18), (926, 1), (941, 10), (943, 4), (944, 6), (945, 1), (946, 3), (947, 18), (963, 13), (964, 6), (965, 1), (968, 13), (971, 4), (972, 6), (973, 16), (978, 4), (994, 1), (995, 2), (996, 5), (1006, 3), (1012, 2), (1030, 2), (1043, 4), (1061, 3), (1081, 5), (1082, 2), (1103, 2), (1114, 3), (1123, 3), (1127, 1), (1128, 3), (1139, 2), (1143, 2), (1154, 3), (1167, 9), (1173, 3), (1175, 5), (1181, 4), (1183, 5), (1186, 7), (1443, 3), (1500, 2), (1503, 3), (1701, 5), (2421, 13)]
def cs22 : List ℕ := [0, 13, 0, 6, 13, 19, 0, 0, 19, 11, 0, 13, 44, 32, 19, 0, 32, 32, 31, 18, 19, 0, 4, 19, 30, 0, 32, 0, 0, 30, 14, 31, 8, 31, 37, 32, 28, 32, 15, 31, 32, 31, 10, 30, 64, 31, 21, 0, 24, 31, 30, 48, 5, 33, 14, 83, 31, 32, 26, 31, 31, 32, 18, 30, 33, 28, 33, 62, 31, 81, 31, 31, 32, 32, 31, 7, 32, 30, 65, 32, 20, 86, 32, 32, 32, 19, 22, 32, 121, 32, 33, 32, 5, 123, 31, 32, 32, 34, 32, 27, 33, 32, 19, 32, 12, 113, 25, 30, 31, 75, 32, 32, 32, 33, 32, 31, 31, 32, 32, 33, 32, 33, 28, 33, 31, 32, 32, 32, 33, 32, 32, 32, 32, 32, 33, 30, 28, 29, 32, 32, 32, 28, 30, 31, 32, 27, 30, 32, 32, 32, 32, 30, 30, 28]
theorem loads22 : cs22.get =
    load (fun i : Fin entries22.length => support (entries22.get i).1)
      (fun i => (entries22.get i).2) := by
  apply load_eq_of_sparse_packed base cs22 support code
    entries22 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node22 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 28 (insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 78 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs22 support demand
    entries22 ((insert 28 (insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)) ((insert 78 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)) 32 32 loads22
  decide +kernel
theorem node17 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 78 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 78 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154))
    28 node21 node22
def entries19 : List (Fin 2469 × ℕ) := [(7, 34), (43, 4), (62, 20), (65, 36), (177, 8), (325, 60), (364, 19), (464, 7), (483, 15), (526, 8), (542, 32), (570, 4), (571, 5), (622, 37), (639, 17), (674, 32), (798, 21), (814, 9), (815, 5), (819, 14), (859, 23), (860, 10), (873, 6), (874, 40), (901, 22), (904, 24), (905, 11), (912, 50), (918, 54), (942, 19), (943, 33), (944, 15), (947, 17), (953, 13), (968, 28), (971, 14), (972, 29), (973, 55), (977, 6), (978, 17), (1006, 3), (1009, 26), (1015, 1), (1043, 8), (1061, 11), (1076, 9), (1101, 2), (1103, 8), (1113, 11), (1114, 1), (1123, 23), (1141, 3), (1155, 4), (1167, 16), (1174, 12), (1175, 16), (1179, 12), (1185, 2), (1186, 29), (1310, 24), (1443, 5), (1540, 5), (1559, 19), (1618, 10), (1619, 5), (1685, 20), (1846, 10), (1848, 1), (1849, 12), (1851, 4), (2169, 12), (2180, 17), (2421, 28)]
def cs19 : List ℕ := [0, 62, 0, 0, 62, 15, 4, 0, 78, 71, 0, 28, 101, 100, 64, 20, 49, 99, 101, 25, 60, 58, 28, 99, 65, 0, 100, 0, 100, 99, 73, 100, 15, 99, 173, 84, 150, 67, 48, 101, 100, 100, 48, 89, 249, 100, 162, 0, 86, 101, 100, 204, 32, 99, 61, 224, 100, 99, 100, 101, 101, 100, 73, 75, 99, 53, 101, 120, 101, 243, 179, 95, 101, 99, 99, 12, 101, 84, 17, 100, 58, 335, 100, 100, 86, 57, 100, 91, 355, 100, 101, 89, 68, 314, 91, 100, 99, 99, 100, 101, 99, 114, 86, 100, 48, 321, 74, 100, 96, 186, 100, 100, 100, 98, 99, 99, 101, 100, 100, 99, 100, 99, 87, 101, 100, 100, 99, 100, 99, 99, 98, 99, 100, 100, 100, 96, 92, 93, 99, 100, 99, 99, 95, 98, 100, 91, 100, 100, 100, 100, 93, 100, 96, 90]
theorem loads19 : cs19.get =
    load (fun i : Fin entries19.length => support (entries19.get i).1)
      (fun i => (entries19.get i).2) := by
  apply load_eq_of_sparse_packed base cs19 support code
    entries19 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node19 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 70 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs19 support demand
    entries19 ((insert 78 (insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)) ((insert 70 (insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)) 100 32 loads19
  decide +kernel
def entries20 : List (Fin 2469 × ℕ) := [(7, 36), (62, 33), (355, 4), (475, 49), (483, 16), (507, 13), (526, 34), (542, 49), (570, 4), (571, 32), (622, 27), (674, 17), (739, 1), (777, 16), (797, 1), (798, 36), (815, 5), (819, 7), (859, 33), (860, 2), (873, 3), (874, 28), (891, 16), (901, 8), (904, 10), (905, 27), (912, 51), (918, 64), (923, 8), (939, 22), (941, 20), (943, 21), (944, 11), (945, 20), (946, 1), (953, 8), (963, 6), (968, 26), (969, 2), (971, 24), (972, 24), (973, 51), (977, 7), (978, 6), (1009, 26), (1030, 2), (1044, 18), (1061, 6), (1076, 3), (1100, 4), (1101, 15), (1103, 8), (1104, 10), (1113, 10), (1123, 15), (1141, 8), (1155, 2), (1167, 15), (1175, 15), (1179, 11), (1183, 2), (1185, 1), (1186, 32), (1212, 2), (1297, 6), (1310, 20), (1528, 1), (1540, 7), (1559, 4), (1618, 2), (1655, 8), (1685, 48), (1845, 4), (1846, 12), (1848, 7), (2421, 43)]
def cs20 : List ℕ := [0, 79, 0, 49, 79, 16, 0, 0, 78, 48, 0, 92, 177, 100, 92, 48, 66, 100, 99, 65, 92, 100, 48, 100, 68, 0, 99, 16, 99, 99, 58, 100, 72, 101, 169, 100, 133, 100, 81, 101, 99, 91, 32, 106, 238, 100, 153, 0, 99, 102, 99, 172, 49, 100, 50, 168, 100, 100, 99, 101, 100, 98, 69, 79, 101, 64, 100, 132, 100, 226, 8, 99, 87, 100, 101, 11, 100, 63, 8, 100, 67, 190, 99, 100, 72, 80, 71, 69, 286, 99, 100, 70, 12, 207, 100, 102, 89, 101, 99, 100, 100, 100, 60, 99, 27, 251, 67, 100, 99, 175, 101, 100, 99, 89, 77, 100, 99, 100, 101, 101, 100, 100, 83, 100, 99, 100, 100, 100, 101, 100, 100, 101, 101, 99, 100, 99, 67, 101, 99, 99, 100, 92, 87, 99, 100, 85, 99, 100, 99, 99, 99, 100, 96, 96]
theorem loads20 : cs20.get =
    load (fun i : Fin entries20.length => support (entries20.get i).1)
      (fun i => (entries20.get i).2) := by
  apply load_eq_of_sparse_packed base cs20 support code
    entries20 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node20 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 70 (insert 78 (insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs20 support demand
    entries20 ((insert 70 (insert 78 (insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))))) : Finset (Fin 154)) ((insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)) 100 32 loads20
  decide +kernel
theorem node18 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 78 (insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)) ((insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154))
    70 node19 node20
theorem node16 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 75 (insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154))
    78 node17 node18
theorem node14 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 7 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154))
    75 node15 node16
theorem node1 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)) ((insert 36 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154))
    7 node13 node14
def entries3 : List (Fin 2469 × ℕ) := [(7, 97), (116, 28), (120, 70), (275, 69), (312, 129), (325, 104), (361, 12), (420, 14), (466, 256), (531, 5), (571, 88), (610, 2), (617, 70), (730, 9), (731, 64), (798, 33), (819, 1), (850, 69), (864, 28), (873, 61), (874, 84), (876, 26), (878, 43), (903, 50), (904, 26), (906, 44), (912, 187), (918, 127), (921, 7), (926, 3), (941, 78), (943, 14), (944, 13), (945, 32), (947, 126), (963, 102), (964, 48), (967, 48), (968, 88), (969, 3), (971, 30), (972, 63), (973, 104), (992, 15), (994, 37), (995, 75), (996, 9), (1012, 22), (1030, 10), (1043, 11), (1044, 36), (1061, 46), (1101, 5), (1103, 50), (1123, 33), (1139, 13), (1141, 25), (1142, 14), (1155, 9), (1162, 31), (1166, 15), (1167, 75), (1173, 40), (1174, 2), (1175, 25), (1177, 3), (1179, 11), (1183, 62), (1186, 66), (1310, 21), (1372, 9), (1443, 48), (1545, 11), (1548, 2), (1572, 11), (1685, 23)]
def cs3 : List ℕ := [256, 97, 0, 69, 97, 0, 0, 256, 0, 28, 0, 256, 325, 256, 69, 121, 256, 256, 256, 88, 325, 218, 23, 256, 122, 0, 256, 0, 142, 210, 256, 236, 72, 211, 519, 256, 21, 256, 121, 256, 238, 256, 27, 142, 542, 256, 90, 0, 161, 256, 256, 355, 13, 256, 67, 732, 258, 256, 236, 256, 257, 256, 75, 255, 256, 256, 257, 522, 257, 511, 256, 256, 255, 256, 190, 256, 255, 200, 684, 256, 208, 693, 254, 256, 256, 249, 255, 256, 1100, 252, 256, 256, 70, 974, 214, 255, 257, 256, 257, 256, 286, 256, 209, 255, 173, 1000, 204, 218, 256, 622, 245, 256, 255, 257, 256, 256, 257, 257, 256, 256, 257, 257, 197, 256, 256, 256, 255, 256, 257, 256, 256, 255, 255, 256, 257, 256, 196, 221, 256, 256, 257, 204, 241, 256, 257, 224, 256, 245, 256, 237, 254, 198, 212, 241]
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
      (∀ i ∈ ((insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 78 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs3 support demand
    entries3 ((insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 78 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)) 256 32 loads3
  decide +kernel
def entries11 : List (Fin 2469 × ℕ) := [(7, 116), (20, 2), (116, 24), (122, 41), (275, 32), (325, 187), (400, 14), (427, 35), (466, 256), (526, 4), (531, 9), (571, 56), (617, 9), (693, 15), (731, 29), (777, 6), (780, 34), (782, 1), (798, 56), (850, 44), (860, 72), (874, 12), (876, 59), (904, 33), (905, 32), (912, 197), (918, 53), (919, 10), (920, 61), (942, 25), (943, 96), (944, 29), (954, 14), (968, 98), (971, 45), (972, 78), (973, 116), (978, 15), (994, 46), (995, 90), (1012, 29), (1043, 46), (1075, 39), (1076, 7), (1101, 41), (1103, 3), (1122, 17), (1139, 26), (1141, 3), (1155, 34), (1167, 79), (1173, 4), (1174, 5), (1176, 42), (1177, 14), (1186, 51), (1211, 38), (1212, 10), (1248, 44), (1269, 6), (1273, 7), (1346, 51), (1372, 92), (1417, 12), (1443, 35), (1451, 2), (1459, 8), (1469, 31), (1556, 24), (1619, 98), (1685, 57), (1689, 30), (2169, 6)]
def cs11 : List ℕ := [256, 116, 0, 46, 116, 0, 0, 256, 74, 98, 0, 256, 376, 231, 59, 122, 256, 256, 255, 56, 315, 238, 57, 256, 163, 0, 255, 0, 153, 256, 256, 255, 130, 256, 402, 254, 31, 241, 81, 254, 87, 255, 125, 144, 510, 256, 166, 0, 256, 75, 256, 250, 0, 256, 81, 779, 256, 256, 256, 255, 254, 255, 181, 68, 250, 249, 256, 329, 256, 530, 544, 255, 255, 256, 256, 468, 275, 240, 6, 256, 173, 725, 255, 256, 224, 256, 255, 255, 904, 232, 255, 256, 234, 713, 257, 256, 219, 255, 257, 255, 256, 256, 255, 255, 132, 770, 256, 257, 228, 557, 256, 256, 256, 198, 257, 256, 256, 256, 256, 256, 402, 257, 256, 256, 256, 245, 256, 256, 219, 255, 256, 256, 257, 256, 256, 256, 227, 246, 257, 255, 257, 220, 256, 235, 256, 145, 256, 256, 248, 231, 208, 233, 233, 218]
theorem loads11 : cs11.get =
    load (fun i : Fin entries11.length => support (entries11.get i).1)
      (fun i => (entries11.get i).2) := by
  apply load_eq_of_sparse_packed base cs11 support code
    entries11 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node11 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 75 (insert 120 (insert 70 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs11 support demand
    entries11 ((insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 75 (insert 120 (insert 70 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))))) : Finset (Fin 154)) 256 32 loads11
  decide +kernel
def entries12 : List (Fin 2469 × ℕ) := [(7, 53), (96, 13), (116, 3), (275, 8), (325, 80), (361, 20), (401, 4), (466, 100), (571, 52), (690, 13), (731, 11), (736, 30), (739, 18), (777, 1), (798, 36), (813, 9), (815, 28), (819, 15), (850, 8), (860, 4), (864, 37), (873, 3), (874, 30), (876, 44), (903, 6), (904, 16), (905, 19), (912, 56), (918, 13), (919, 11), (920, 3), (942, 11), (943, 36), (944, 11), (954, 22), (968, 36), (970, 1), (971, 30), (972, 23), (973, 48), (978, 9), (994, 23), (995, 8), (1015, 8), (1016, 9), (1040, 2), (1043, 22), (1044, 1), (1061, 3), (1075, 13), (1099, 4), (1100, 8), (1101, 11), (1104, 8), (1114, 4), (1122, 20), (1139, 22), (1141, 4), (1143, 3), (1147, 2), (1155, 12), (1167, 29), (1174, 22), (1186, 23), (1211, 9), (1443, 3), (1469, 21), (1528, 1), (1619, 8), (1685, 31), (1845, 10), (2169, 18)]
def cs12 : List ℕ := [100, 53, 0, 8, 53, 0, 0, 100, 4, 45, 0, 100, 112, 99, 44, 34, 100, 99, 99, 52, 144, 87, 31, 100, 49, 0, 100, 0, 55, 87, 100, 98, 16, 100, 195, 99, 21, 64, 34, 99, 73, 99, 47, 61, 199, 87, 69, 0, 91, 100, 99, 172, 0, 81, 26, 278, 100, 100, 101, 99, 93, 100, 83, 23, 101, 51, 100, 98, 100, 212, 208, 101, 100, 100, 101, 8, 100, 100, 6, 99, 61, 313, 87, 100, 93, 101, 101, 95, 305, 100, 100, 68, 102, 270, 100, 100, 101, 100, 101, 101, 100, 109, 101, 100, 45, 276, 65, 100, 101, 204, 100, 102, 101, 89, 101, 100, 101, 100, 101, 100, 188, 101, 97, 101, 100, 100, 101, 101, 101, 102, 100, 100, 101, 100, 101, 101, 101, 100, 100, 101, 100, 97, 86, 81, 101, 48, 100, 100, 88, 101, 89, 74, 82, 83]
theorem loads12 : cs12.get =
    load (fun i : Fin entries12.length => support (entries12.get i).1)
      (fun i => (entries12.get i).2) := by
  apply load_eq_of_sparse_packed base cs12 support code
    entries12 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node12 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 75 (insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 120 (insert 70 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs12 support demand
    entries12 ((insert 75 (insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)) ((insert 120 (insert 70 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)) 100 32 loads12
  decide +kernel
theorem node9 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 120 (insert 70 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 120 (insert 70 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154))
    75 node11 node12
def entries10 : List (Fin 2469 × ℕ) := [(7, 425), (95, 11), (96, 201), (116, 110), (122, 345), (179, 117), (275, 75), (325, 734), (355, 4), (364, 197), (461, 2), (465, 155), (466, 1000), (507, 166), (570, 22), (572, 412), (739, 118), (780, 153), (783, 4), (797, 7), (798, 369), (850, 189), (860, 257), (873, 140), (876, 311), (904, 72), (905, 186), (912, 689), (919, 88), (920, 188), (921, 29), (941, 77), (943, 248), (944, 139), (945, 108), (952, 63), (956, 91), (963, 111), (967, 277), (971, 181), (972, 55), (973, 489), (978, 79), (994, 240), (995, 252), (996, 23), (1006, 46), (1012, 104), (1061, 53), (1075, 87), (1091, 32), (1100, 194), (1103, 102), (1104, 59), (1123, 93), (1139, 33), (1141, 129), (1142, 49), (1148, 19), (1155, 139), (1167, 192), (1174, 83), (1175, 182), (1179, 212), (1186, 140), (1212, 159), (1248, 167), (1310, 299), (1372, 108), (1443, 61), (1618, 48), (1623, 234), (1685, 79), (1689, 30), (1705, 14), (2008, 115), (2169, 35)]
def cs10 : List ℕ := [1000, 425, 0, 304, 425, 0, 0, 1000, 372, 329, 0, 1000, 1446, 1000, 311, 534, 1000, 1000, 1000, 412, 1311, 959, 196, 1000, 472, 0, 1000, 0, 833, 1000, 1000, 999, 289, 1000, 1872, 1000, 299, 878, 306, 999, 711, 1001, 387, 557, 2288, 1001, 867, 0, 1000, 727, 1000, 1300, 91, 1000, 522, 2979, 1000, 1000, 999, 999, 1000, 1000, 854, 410, 1000, 798, 1002, 1206, 1000, 1479, 1882, 1000, 772, 1000, 1000, 1000, 1000, 901, 111, 999, 871, 2031, 968, 999, 759, 1001, 1000, 1000, 3276, 999, 1000, 1000, 872, 2744, 732, 1000, 926, 999, 1001, 1000, 1000, 1000, 992, 999, 477, 2606, 825, 1000, 999, 1815, 893, 1000, 1000, 898, 1000, 999, 1000, 1000, 1000, 999, 236, 1001, 957, 999, 999, 986, 999, 1000, 913, 1000, 999, 965, 1000, 1000, 890, 951, 754, 999, 999, 999, 1000, 784, 859, 1000, 1000, 999, 1000, 999, 999, 1000, 1000, 1000, 1000, 927]
theorem loads10 : cs10.get =
    load (fun i : Fin entries10.length => support (entries10.get i).1)
      (fun i => (entries10.get i).2) := by
  apply load_eq_of_sparse_packed base cs10 support code
    entries10 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node10 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 120 (insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 70 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs10 support demand
    entries10 ((insert 120 (insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)) ((insert 70 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)) 1000 32 loads10
  decide +kernel
theorem node5 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 70 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 70 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154))
    120 node9 node10
def entries7 : List (Fin 2469 × ℕ) := [(43, 3), (62, 39), (96, 19), (116, 41), (122, 28), (203, 9), (275, 32), (355, 10), (360, 13), (466, 91), (475, 3), (484, 3), (531, 3), (571, 15), (572, 36), (577, 39), (617, 10), (736, 3), (738, 3), (739, 3), (798, 20), (850, 32), (901, 3), (903, 10), (905, 1), (912, 61), (918, 79), (919, 9), (923, 30), (924, 4), (941, 27), (943, 3), (944, 17), (945, 3), (946, 14), (963, 30), (964, 12), (967, 14), (968, 36), (971, 29), (972, 10), (973, 39), (992, 5), (994, 20), (995, 30), (1006, 2), (1012, 17), (1043, 6), (1061, 14), (1069, 19), (1101, 4), (1103, 19), (1114, 8), (1123, 12), (1138, 3), (1139, 19), (1141, 11), (1155, 14), (1167, 36), (1173, 3), (1174, 14), (1175, 11), (1179, 9), (1186, 4), (1212, 21), (1223, 6), (1273, 5), (1310, 9), (1372, 11), (1443, 14), (1685, 7), (1829, 5), (2008, 28)]
def cs7 : List ℕ := [97, 0, 0, 63, 6, 3, 3, 97, 34, 67, 0, 100, 135, 100, 3, 76, 100, 99, 99, 90, 136, 79, 7, 100, 20, 0, 100, 0, 90, 99, 100, 100, 72, 70, 221, 100, 14, 99, 87, 99, 74, 99, 20, 102, 216, 242, 59, 0, 89, 37, 99, 193, 0, 99, 34, 226, 99, 100, 93, 99, 84, 100, 40, 65, 99, 99, 99, 176, 101, 163, 0, 100, 85, 99, 98, 99, 100, 100, 55, 100, 100, 147, 101, 100, 90, 89, 100, 90, 357, 100, 100, 100, 54, 251, 100, 100, 100, 100, 99, 99, 100, 100, 89, 99, 72, 246, 83, 94, 81, 232, 82, 100, 100, 100, 93, 100, 100, 100, 99, 101, 99, 94, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 101, 100, 100, 94, 92, 84, 101, 100, 101, 69, 96, 94, 99, 78, 91, 100, 88, 100, 100, 75, 73, 83]
theorem loads7 : cs7.get =
    load (fun i : Fin entries7.length => support (entries7.get i).1)
      (fun i => (entries7.get i).2) := by
  apply load_eq_of_sparse_packed base cs7 support code
    entries7 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node7 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 70 (insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 45 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs7 support demand
    entries7 ((insert 70 (insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)) ((insert 45 (insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅))))))))))))))) : Finset (Fin 154)) 100 32 loads7
  decide +kernel
def entries8 : List (Fin 2469 × ℕ) := [(7, 136), (54, 73), (96, 45), (122, 73), (203, 1), (417, 11), (466, 174), (475, 20), (484, 20), (503, 48), (531, 4), (542, 18), (571, 58), (572, 65), (577, 86), (592, 2), (737, 61), (738, 8), (739, 12), (758, 2), (776, 46), (777, 8), (798, 68), (819, 11), (844, 18), (873, 46), (874, 9), (876, 10), (904, 50), (905, 92), (912, 142), (918, 114), (939, 45), (941, 65), (942, 16), (943, 42), (944, 45), (946, 51), (963, 50), (964, 16), (967, 17), (968, 58), (971, 38), (972, 52), (973, 127), (978, 37), (995, 28), (996, 9), (1006, 16), (1009, 11), (1028, 17), (1043, 6), (1048, 34), (1049, 27), (1061, 11), (1100, 28), (1103, 2), (1123, 21), (1138, 8), (1139, 5), (1141, 35), (1143, 4), (1155, 43), (1162, 6), (1167, 64), (1173, 29), (1175, 56), (1179, 56), (1186, 28), (1212, 36), (1223, 40), (1232, 4), (1273, 14), (1348, 61), (1359, 21), (1372, 14), (1443, 24), (1497, 8), (1528, 3), (1540, 7), (1619, 24), (1621, 2), (1685, 47)]
def cs8 : List ℕ := [232, 157, 0, 20, 176, 20, 0, 253, 161, 24, 0, 255, 414, 254, 28, 120, 255, 255, 255, 123, 367, 256, 47, 255, 167, 18, 255, 0, 181, 189, 255, 255, 64, 255, 521, 256, 61, 255, 47, 256, 185, 170, 87, 250, 564, 103, 236, 0, 256, 225, 239, 234, 18, 255, 125, 652, 257, 256, 250, 256, 254, 223, 155, 146, 255, 255, 255, 320, 255, 462, 26, 255, 256, 256, 254, 255, 256, 255, 95, 254, 255, 305, 249, 257, 165, 255, 255, 255, 658, 246, 254, 212, 234, 518, 256, 255, 254, 256, 256, 255, 255, 256, 175, 240, 211, 412, 185, 194, 255, 501, 254, 256, 255, 250, 180, 252, 255, 256, 254, 256, 256, 254, 254, 254, 256, 255, 255, 256, 255, 254, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 233, 255, 255, 247, 255, 255, 255, 255, 255, 255, 253, 252]
theorem loads8 : cs8.get =
    load (fun i : Fin entries8.length => support (entries8.get i).1)
      (fun i => (entries8.get i).2) := by
  apply load_eq_of_sparse_packed base cs8 support code
    entries8 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node8 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 45 (insert 70 (insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs8 support demand
    entries8 ((insert 45 (insert 70 (insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))))) : Finset (Fin 154)) ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154)) 256 32 loads8
  decide +kernel
theorem node6 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 70 (insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 70 (insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))))) : Finset (Fin 154)) ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154))
    45 node7 node8
theorem node4 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 78 (insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154))
    70 node5 node6
theorem node2 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 36 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅)))))) : Finset (Fin 154)) ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154))
    78 node3 node4
theorem node0 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)) ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154))
    36 node1 node2
theorem excludes_context :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 105 (insert 93 (insert 88 (insert 81 (insert 69 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact node0
#print axioms excludes_context
end OmissionResidual32Resume.Context24
