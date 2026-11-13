import Residual32ContextsProof.Catalog
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Resume.Context485517
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open OmissionResidual32Contexts
-- The initial context is inherited from the frozen original tree.
def entries23 : List (Fin 2469 × ℕ) := [(0, 84), (4, 7), (77, 92), (91, 18), (132, 34), (302, 91), (304, 31), (472, 39), (483, 11), (498, 73), (518, 58), (550, 17), (552, 166), (571, 10), (617, 59), (731, 73), (740, 93), (741, 14), (779, 90), (781, 81), (782, 34), (783, 82), (798, 1), (851, 46), (868, 26), (870, 84), (872, 5), (874, 56), (941, 50), (943, 25), (944, 64), (949, 98), (950, 25), (961, 26), (962, 131), (963, 76), (964, 53), (971, 53), (973, 149), (1009, 57), (1010, 28), (1011, 42), (1012, 40), (1025, 23), (1030, 14), (1044, 9), (1070, 24), (1076, 64), (1082, 1), (1089, 8), (1108, 32), (1123, 12), (1154, 25), (1155, 18), (1171, 27), (1178, 43), (1183, 14), (1184, 18), (1186, 64), (1199, 73), (1217, 152), (1253, 20), (1277, 11), (1309, 14), (1516, 2), (1546, 16), (1556, 18), (1617, 13), (1665, 42), (2169, 17)]
def cs23 : List ℕ := [256, 80, 191, 0, 230, 236, 73, 257, 257, 0, 176, 256, 256, 152, 256, 183, 256, 248, 231, 10, 256, 73, 0, 443, 233, 553, 258, 335, 92, 73, 256, 17, 17, 257, 152, 258, 401, 0, 92, 269, 216, 210, 255, 27, 399, 256, 0, 26, 73, 256, 255, 257, 0, 255, 256, 255, 255, 78, 256, 155, 583, 257, 174, 255, 248, 255, 256, 14, 255, 181, 751, 256, 244, 239, 192, 685, 256, 186, 568, 255, 145, 569, 254, 255, 126, 236, 257, 257, 14, 223, 255, 231, 556, 255, 206, 207, 256, 257, 256, 255, 256, 256, 256, 256, 231, 255, 233, 241, 256, 553, 256, 257, 256, 228, 256, 255, 254, 256, 257, 256, 257, 256, 256, 255, 215, 235, 257, 255, 80, 255, 255, 215, 256, 256, 256, 178, 241, 192, 256, 256, 246, 243, 253, 256, 162, 192, 209, 245, 235, 240, 204, 256, 256, 256]
theorem loads23 : cs23.get =
    load (fun i : Fin entries23.length => support (entries23.get i).1)
      (fun i => (entries23.get i).2) := by
  apply load_eq_of_sparse_packed base cs23 support code
    entries23 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node23 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 92 (insert 75 (insert 25 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs23 support demand
    entries23 ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)) ((insert 92 (insert 75 (insert 25 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))))) : Finset (Fin 154)) 256 32 loads23
  decide +kernel
def entries24 : List (Fin 2469 × ℕ) := [(0, 90), (4, 52), (77, 113), (91, 33), (132, 20), (302, 69), (446, 33), (450, 53), (472, 42), (483, 12), (498, 78), (518, 40), (550, 106), (552, 80), (571, 86), (731, 37), (740, 28), (741, 32), (777, 33), (778, 102), (819, 16), (835, 8), (851, 48), (868, 26), (870, 74), (874, 92), (884, 16), (925, 23), (926, 28), (943, 54), (944, 22), (949, 59), (953, 13), (962, 27), (964, 93), (966, 30), (971, 54), (972, 64), (973, 149), (984, 16), (1009, 18), (1011, 57), (1012, 29), (1021, 8), (1025, 6), (1030, 13), (1043, 27), (1045, 1), (1073, 4), (1075, 14), (1076, 50), (1082, 20), (1089, 35), (1090, 20), (1108, 7), (1132, 3), (1137, 5), (1154, 24), (1155, 2), (1160, 26), (1171, 30), (1172, 13), (1173, 21), (1177, 23), (1178, 28), (1179, 27), (1183, 5), (1186, 56), (1217, 131), (1253, 35), (1277, 19), (1309, 34), (1546, 49), (1549, 37), (1846, 8)]
def cs24 : List ℕ := [256, 52, 173, 0, 225, 143, 0, 256, 255, 0, 179, 240, 256, 125, 255, 186, 256, 216, 256, 86, 232, 0, 0, 406, 240, 534, 256, 317, 113, 0, 256, 0, 157, 255, 165, 256, 422, 0, 113, 254, 229, 149, 156, 46, 391, 255, 0, 26, 37, 255, 256, 256, 0, 256, 255, 254, 256, 78, 256, 118, 401, 256, 150, 256, 213, 254, 254, 5, 257, 248, 501, 255, 257, 150, 123, 490, 254, 145, 515, 256, 70, 559, 257, 257, 155, 182, 254, 257, 28, 257, 256, 251, 27, 257, 256, 254, 256, 256, 256, 256, 255, 256, 180, 256, 219, 256, 181, 257, 256, 564, 250, 257, 257, 140, 256, 256, 256, 257, 256, 255, 256, 158, 166, 256, 178, 244, 256, 256, 200, 255, 257, 203, 256, 257, 254, 257, 256, 245, 257, 256, 256, 255, 257, 257, 223, 231, 233, 250, 235, 256, 200, 256, 256, 257]
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
      (∀ i ∈ ((insert 92 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 75 (insert 25 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs24 support demand
    entries24 ((insert 92 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 75 (insert 25 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))))) : Finset (Fin 154)) 256 32 loads24
  decide +kernel
theorem node21 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 75 (insert 25 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)) ((insert 75 (insert 25 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))))) : Finset (Fin 154))
    92 node23 node24
def entries22 : List (Fin 2469 × ℕ) := [(20, 43), (37, 33), (77, 467), (302, 67), (304, 192), (472, 27), (483, 33), (498, 103), (550, 66), (552, 873), (571, 316), (690, 29), (692, 111), (731, 60), (739, 113), (740, 459), (798, 25), (813, 246), (819, 124), (835, 67), (851, 179), (853, 70), (868, 207), (870, 130), (872, 262), (874, 162), (884, 76), (887, 157), (922, 224), (926, 391), (934, 24), (944, 36), (949, 420), (950, 128), (962, 297), (963, 115), (964, 373), (966, 45), (972, 330), (973, 535), (1009, 271), (1025, 80), (1033, 93), (1043, 268), (1044, 126), (1045, 112), (1072, 124), (1073, 248), (1075, 61), (1076, 125), (1082, 171), (1086, 30), (1089, 94), (1090, 11), (1108, 26), (1137, 16), (1138, 46), (1175, 13), (1182, 100), (1183, 22), (1185, 78), (1186, 365), (1197, 207), (1200, 327), (1217, 212), (1220, 293), (1253, 288), (1482, 66), (1528, 59), (1545, 24), (1584, 44), (1846, 95), (1851, 19)]
def cs22 : List ℕ := [1000, 620, 239, 663, 1001, 555, 207, 999, 1001, 0, 1001, 923, 999, 1001, 1001, 939, 929, 1000, 999, 506, 1000, 534, 0, 1430, 999, 1599, 1000, 1514, 467, 643, 999, 224, 457, 1001, 588, 1000, 1673, 66, 500, 1069, 659, 746, 909, 0, 1974, 1001, 0, 207, 60, 999, 999, 1000, 90, 999, 1000, 1001, 1001, 431, 999, 760, 1015, 739, 300, 1000, 1000, 716, 1000, 146, 1000, 761, 1598, 1000, 1000, 999, 691, 0, 1001, 999, 2383, 1000, 60, 2300, 998, 1000, 456, 771, 690, 1000, 135, 999, 1000, 628, 1000, 999, 781, 1001, 1000, 1000, 1000, 889, 1001, 1001, 938, 999, 792, 1001, 621, 1000, 729, 1949, 1001, 1057, 1000, 1000, 1000, 1000, 1001, 1000, 1001, 1000, 1000, 745, 1000, 1001, 1000, 822, 1001, 1000, 770, 999, 999, 690, 1001, 1000, 1001, 1000, 955, 819, 1001, 1001, 786, 718, 970, 1000, 895, 796, 1001, 997, 889, 900, 735, 913, 1000, 1000]
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
      (∀ i ∈ ((insert 75 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 25 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs22 support demand
    entries22 ((insert 75 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 25 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)) 1000 32 loads22
  decide +kernel
theorem node17 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 25 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)) ((insert 25 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154))
    75 node21 node22
def entries19 : List (Fin 2469 × ℕ) := [(43, 11), (302, 2), (446, 1), (450, 4), (498, 38), (552, 51), (570, 4), (571, 4), (730, 14), (731, 33), (740, 18), (776, 1), (778, 11), (779, 3), (780, 8), (783, 32), (784, 2), (798, 2), (851, 38), (870, 27), (872, 18), (874, 27), (903, 2), (922, 17), (924, 25), (943, 18), (944, 30), (949, 32), (953, 17), (962, 48), (964, 46), (966, 5), (972, 17), (973, 57), (1009, 11), (1010, 12), (1011, 20), (1012, 23), (1021, 4), (1025, 5), (1043, 2), (1048, 7), (1069, 20), (1076, 10), (1082, 15), (1089, 3), (1090, 4), (1100, 9), (1108, 3), (1128, 2), (1155, 17), (1167, 13), (1173, 6), (1178, 5), (1182, 2), (1183, 4), (1184, 3), (1186, 23), (1220, 4), (1248, 23), (1253, 49), (1309, 10), (1417, 16), (1435, 11), (1517, 20), (1537, 9), (1546, 22), (1556, 6)]
def cs19 : List ℕ := [53, 4, 9, 4, 87, 9, 31, 100, 96, 0, 0, 100, 100, 54, 11, 51, 62, 75, 62, 4, 73, 11, 0, 100, 62, 0, 100, 84, 0, 11, 100, 26, 45, 100, 12, 100, 147, 20, 0, 124, 15, 88, 99, 13, 195, 100, 0, 0, 47, 100, 100, 100, 0, 99, 100, 100, 101, 65, 99, 64, 204, 99, 97, 51, 100, 99, 101, 39, 101, 83, 262, 100, 101, 99, 53, 225, 100, 92, 114, 100, 48, 260, 100, 100, 64, 100, 90, 100, 6, 100, 100, 100, 100, 100, 100, 81, 99, 99, 101, 100, 96, 100, 98, 99, 65, 99, 101, 94, 100, 208, 87, 101, 100, 84, 101, 100, 100, 101, 100, 101, 99, 75, 100, 99, 97, 91, 99, 101, 31, 101, 100, 82, 101, 101, 100, 102, 97, 91, 101, 101, 70, 84, 92, 101, 82, 78, 96, 100, 87, 88, 82, 101, 101, 101]
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
      (∀ i ∈ ((insert 25 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 75 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs19 support demand
    entries19 ((insert 25 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 75 (insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)) 100 32 loads19
  decide +kernel
def entries20 : List (Fin 2469 × ℕ) := [(43, 22), (189, 4), (275, 1), (304, 9), (340, 7), (362, 19), (498, 9), (550, 7), (552, 67), (571, 25), (660, 9), (692, 8), (731, 26), (740, 29), (742, 1), (798, 6), (812, 17), (813, 1), (851, 22), (859, 9), (870, 13), (872, 30), (874, 32), (902, 5), (903, 5), (922, 13), (924, 20), (926, 14), (931, 11), (943, 23), (949, 32), (950, 14), (953, 1), (962, 41), (963, 7), (964, 37), (972, 24), (973, 54), (1009, 24), (1010, 5), (1011, 13), (1021, 6), (1033, 16), (1034, 10), (1043, 20), (1044, 9), (1045, 15), (1072, 9), (1073, 13), (1076, 5), (1081, 7), (1082, 14), (1086, 6), (1128, 5), (1155, 5), (1167, 11), (1175, 5), (1182, 5), (1183, 6), (1184, 6), (1186, 35), (1220, 33), (1253, 45), (1451, 8), (1545, 10), (1547, 3), (1846, 15), (1851, 11), (1901, 5)]
def cs20 : List ℕ := [78, 33, 0, 33, 67, 0, 22, 100, 68, 0, 0, 91, 101, 67, 22, 74, 78, 79, 100, 25, 78, 22, 0, 96, 79, 0, 101, 112, 0, 22, 100, 13, 51, 101, 43, 101, 150, 0, 0, 80, 45, 32, 97, 11, 234, 79, 0, 0, 26, 101, 100, 101, 17, 100, 101, 100, 101, 44, 100, 53, 114, 100, 63, 59, 101, 92, 101, 32, 99, 83, 171, 100, 99, 100, 71, 13, 100, 102, 187, 99, 26, 217, 99, 100, 66, 100, 58, 100, 27, 100, 99, 93, 101, 99, 99, 99, 100, 102, 101, 70, 100, 100, 73, 99, 47, 101, 101, 100, 80, 204, 100, 99, 100, 100, 100, 99, 100, 99, 100, 99, 100, 87, 71, 98, 100, 95, 101, 99, 45, 99, 100, 84, 100, 100, 100, 99, 79, 95, 101, 100, 85, 70, 87, 100, 81, 72, 100, 100, 91, 94, 71, 94, 100, 100]
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
      (∀ i ∈ ((insert 75 (insert 25 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs20 support demand
    entries20 ((insert 75 (insert 25 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)) 100 32 loads20
  decide +kernel
theorem node18 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 25 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 25 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154))
    75 node19 node20
theorem node1 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)) ((insert 109 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154))
    25 node17 node18
def entries15 : List (Fin 2469 × ℕ) := [(20, 13), (37, 1), (77, 129), (132, 42), (273, 16), (302, 60), (411, 50), (483, 19), (498, 32), (550, 31), (552, 173), (572, 108), (738, 25), (740, 129), (741, 18), (779, 60), (783, 46), (813, 153), (847, 18), (849, 13), (851, 46), (868, 35), (870, 60), (874, 116), (925, 22), (933, 8), (934, 12), (944, 47), (949, 130), (950, 101), (957, 15), (965, 29), (966, 56), (973, 154), (1009, 47), (1011, 22), (1043, 38), (1044, 17), (1045, 44), (1061, 2), (1073, 57), (1076, 18), (1081, 19), (1082, 11), (1089, 26), (1090, 26), (1108, 3), (1122, 25), (1154, 1), (1159, 23), (1173, 25), (1174, 5), (1175, 17), (1184, 8), (1185, 31), (1186, 70), (1197, 127), (1217, 46), (1218, 62), (1248, 21), (1253, 83), (1266, 42), (1346, 4), (1398, 36), (1403, 27), (1466, 1), (1496, 4), (1584, 3), (1605, 52), (1705, 3), (2169, 17), (2225, 19)]
def cs15 : List ℕ := [256, 62, 126, 26, 256, 255, 127, 255, 256, 0, 168, 251, 255, 256, 256, 204, 256, 213, 255, 109, 230, 127, 0, 392, 223, 464, 256, 343, 129, 140, 255, 17, 73, 256, 186, 256, 391, 0, 130, 237, 249, 188, 220, 0, 495, 201, 0, 39, 52, 257, 256, 451, 15, 254, 256, 256, 257, 32, 256, 143, 483, 257, 149, 256, 239, 257, 257, 15, 256, 168, 723, 257, 232, 241, 132, 256, 245, 232, 641, 256, 160, 695, 256, 257, 52, 169, 255, 257, 22, 256, 256, 178, 613, 256, 115, 256, 256, 516, 256, 256, 256, 256, 256, 257, 178, 256, 256, 256, 256, 109, 255, 256, 256, 256, 257, 256, 255, 257, 256, 255, 256, 230, 256, 257, 257, 226, 256, 255, 255, 255, 257, 193, 256, 256, 256, 237, 239, 217, 256, 256, 176, 239, 256, 255, 207, 231, 237, 256, 235, 254, 215, 241, 256, 255]
theorem loads15 : cs15.get =
    load (fun i : Fin entries15.length => support (entries15.get i).1)
      (fun i => (entries15.get i).2) := by
  apply load_eq_of_sparse_packed base cs15 support code
    entries15 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node15 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 97 (insert 92 (insert 25 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs15 support demand
    entries15 ((insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 97 (insert 92 (insert 25 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))))) : Finset (Fin 154)) 256 32 loads15
  decide +kernel
def entries16 : List (Fin 2469 × ℕ) := [(4, 21), (77, 40), (91, 1), (304, 28), (411, 9), (448, 9), (472, 5), (483, 5), (498, 15), (552, 40), (572, 41), (617, 3), (690, 23), (731, 45), (741, 23), (781, 21), (783, 31), (785, 12), (797, 2), (798, 4), (815, 17), (851, 15), (870, 20), (874, 41), (891, 12), (924, 32), (925, 25), (931, 19), (944, 27), (947, 27), (949, 43), (950, 19), (960, 1), (965, 2), (966, 29), (973, 59), (1009, 10), (1010, 3), (1012, 3), (1030, 6), (1043, 24), (1044, 11), (1072, 5), (1073, 26), (1075, 12), (1081, 6), (1082, 15), (1089, 13), (1090, 1), (1154, 4), (1159, 7), (1160, 5), (1173, 11), (1179, 1), (1186, 27), (1197, 39), (1212, 1), (1217, 35), (1218, 19), (1228, 8), (1253, 25), (1271, 3), (1317, 1), (1478, 7), (1528, 6), (1619, 4), (2126, 16), (2169, 30), (2225, 18)]
def cs16 : List ℕ := [99, 40, 59, 0, 100, 98, 39, 99, 100, 4, 40, 99, 99, 81, 100, 40, 89, 80, 100, 41, 79, 51, 0, 154, 54, 154, 99, 106, 40, 39, 99, 30, 61, 100, 65, 100, 103, 0, 47, 127, 98, 54, 67, 0, 202, 100, 0, 7, 49, 98, 100, 182, 0, 101, 99, 99, 99, 22, 101, 100, 259, 100, 60, 78, 85, 44, 101, 0, 100, 97, 263, 100, 61, 101, 54, 101, 99, 89, 239, 100, 93, 233, 100, 101, 52, 39, 73, 101, 51, 83, 100, 62, 205, 100, 75, 99, 101, 0, 100, 101, 101, 100, 100, 100, 76, 96, 99, 101, 101, 29, 100, 101, 100, 90, 100, 100, 101, 99, 100, 99, 101, 100, 100, 100, 99, 80, 100, 100, 32, 91, 98, 79, 100, 100, 100, 100, 100, 90, 99, 100, 70, 88, 99, 100, 64, 86, 94, 96, 68, 98, 88, 88, 100, 100]
theorem loads16 : cs16.get =
    load (fun i : Fin entries16.length => support (entries16.get i).1)
      (fun i => (entries16.get i).2) := by
  apply load_eq_of_sparse_packed base cs16 support code
    entries16 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node16 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 97 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 92 (insert 25 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs16 support demand
    entries16 ((insert 97 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 92 (insert 25 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))))) : Finset (Fin 154)) 100 32 loads16
  decide +kernel
theorem node13 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 92 (insert 25 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 92 (insert 25 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))))) : Finset (Fin 154))
    97 node15 node16
def entries14 : List (Fin 2469 × ℕ) := [(0, 486), (72, 42), (77, 296), (91, 103), (132, 142), (273, 69), (302, 293), (397, 71), (448, 117), (472, 97), (483, 97), (498, 303), (550, 264), (552, 220), (571, 364), (731, 177), (740, 129), (778, 346), (835, 32), (842, 125), (851, 303), (868, 120), (870, 336), (874, 333), (884, 64), (891, 213), (924, 242), (925, 211), (933, 7), (944, 117), (949, 561), (957, 21), (966, 468), (973, 546), (1005, 71), (1009, 149), (1011, 22), (1012, 30), (1034, 19), (1043, 161), (1044, 35), (1045, 130), (1073, 245), (1076, 50), (1081, 76), (1082, 42), (1089, 210), (1108, 91), (1121, 42), (1133, 81), (1154, 10), (1160, 26), (1173, 187), (1177, 106), (1179, 103), (1186, 190), (1197, 175), (1212, 77), (1217, 303), (1218, 258), (1219, 3), (1228, 26), (1248, 100), (1253, 36), (1261, 141), (1370, 46), (1488, 52), (1502, 36), (1549, 70), (1584, 70), (1605, 126), (1660, 11), (1831, 94), (2225, 92)]
def cs14 : List ℕ := [1000, 261, 658, 3, 1000, 833, 175, 1000, 1000, 0, 458, 936, 1000, 611, 999, 484, 1000, 1000, 1000, 364, 720, 388, 0, 1706, 678, 1886, 1000, 1261, 338, 175, 1000, 0, 786, 1000, 751, 1000, 1453, 0, 432, 1000, 1000, 617, 408, 0, 1888, 1000, 0, 214, 303, 1000, 999, 1575, 21, 1000, 1000, 1000, 1000, 397, 1000, 400, 1594, 1000, 545, 1000, 861, 566, 999, 21, 1000, 1000, 1813, 1000, 1001, 803, 568, 1000, 1000, 401, 2343, 1000, 397, 1921, 1001, 1000, 303, 757, 755, 1000, 106, 1000, 1000, 688, 0, 999, 889, 999, 1000, 1000, 1000, 640, 999, 1001, 898, 999, 909, 999, 884, 1000, 1000, 370, 955, 1000, 1000, 737, 999, 999, 1000, 1000, 1000, 1000, 764, 590, 873, 1000, 1000, 882, 1000, 1000, 548, 1000, 888, 723, 1000, 1001, 894, 1000, 1000, 882, 1001, 1000, 999, 1000, 1001, 1000, 670, 1000, 878, 1000, 849, 1000, 844, 1000, 926, 865]
theorem loads14 : cs14.get =
    load (fun i : Fin entries14.length => support (entries14.get i).1)
      (fun i => (entries14.get i).2) := by
  apply load_eq_of_sparse_packed base cs14 support code
    entries14 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node14 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 92 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 25 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs14 support demand
    entries14 ((insert 92 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 25 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)) 1000 32 loads14
  decide +kernel
theorem node9 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 25 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 25 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154))
    92 node13 node14
def entries11 : List (Fin 2469 × ℕ) := [(43, 19), (273, 20), (411, 37), (498, 100), (550, 4), (552, 135), (571, 35), (731, 100), (740, 11), (741, 9), (782, 10), (783, 58), (784, 49), (785, 35), (815, 5), (842, 6), (851, 133), (859, 33), (870, 106), (874, 120), (891, 16), (922, 13), (924, 99), (925, 5), (944, 88), (949, 143), (952, 27), (964, 26), (966, 92), (973, 142), (1009, 38), (1011, 34), (1012, 28), (1031, 14), (1034, 7), (1045, 3), (1069, 41), (1070, 38), (1073, 30), (1076, 32), (1081, 27), (1082, 15), (1089, 11), (1108, 38), (1133, 7), (1154, 51), (1167, 35), (1173, 34), (1175, 1), (1177, 37), (1186, 25), (1220, 68), (1228, 15), (1241, 12), (1248, 70), (1251, 4), (1253, 54), (1261, 23), (1266, 3), (1275, 25), (1417, 14), (1490, 35), (1517, 27), (1546, 9), (1556, 65), (1652, 5), (2132, 20), (2169, 51), (2225, 5)]
def cs11 : List ℕ := [122, 68, 0, 68, 187, 0, 46, 255, 187, 0, 0, 255, 255, 120, 19, 174, 122, 255, 188, 35, 149, 35, 0, 222, 174, 0, 255, 285, 0, 19, 255, 64, 190, 255, 138, 255, 410, 27, 0, 379, 35, 166, 223, 35, 596, 256, 0, 35, 100, 255, 257, 411, 0, 255, 255, 255, 256, 100, 255, 143, 679, 196, 226, 118, 255, 185, 255, 62, 256, 255, 660, 256, 244, 255, 108, 545, 255, 201, 372, 256, 100, 652, 256, 256, 100, 254, 255, 256, 38, 256, 255, 223, 255, 257, 221, 254, 256, 256, 256, 255, 227, 255, 254, 255, 195, 256, 256, 256, 255, 65, 255, 256, 255, 158, 255, 256, 255, 256, 255, 255, 196, 198, 254, 254, 256, 249, 255, 255, 82, 255, 256, 215, 255, 257, 215, 256, 255, 213, 256, 256, 193, 255, 256, 256, 125, 224, 222, 255, 225, 201, 217, 255, 236, 219]
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
      (∀ i ∈ ((insert 25 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 75 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs11 support demand
    entries11 ((insert 25 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 75 (insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)) 256 32 loads11
  decide +kernel
def entries12 : List (Fin 2469 × ℕ) := [(43, 32), (273, 28), (304, 8), (362, 7), (409, 2), (498, 36), (550, 5), (552, 36), (571, 29), (660, 6), (690, 23), (693, 5), (731, 34), (740, 15), (741, 6), (742, 2), (815, 24), (851, 41), (859, 5), (870, 23), (874, 35), (891, 23), (902, 18), (922, 7), (924, 34), (944, 32), (947, 2), (949, 33), (950, 33), (951, 11), (952, 15), (965, 13), (966, 27), (973, 59), (1009, 6), (1033, 2), (1034, 4), (1043, 8), (1045, 14), (1072, 7), (1073, 13), (1075, 3), (1076, 11), (1081, 20), (1082, 15), (1089, 11), (1090, 13), (1128, 10), (1154, 11), (1167, 11), (1175, 22), (1186, 16), (1220, 34), (1253, 24), (1261, 8), (1344, 8), (1403, 14), (1488, 5), (1490, 22), (1652, 5), (1666, 11), (1732, 2), (1845, 6), (1849, 3), (1991, 7), (2139, 3), (2225, 2)]
def cs12 : List ℕ := [58, 34, 0, 34, 65, 0, 32, 99, 65, 0, 0, 81, 99, 35, 32, 63, 58, 100, 69, 29, 58, 55, 0, 112, 63, 0, 99, 120, 2, 32, 99, 7, 95, 99, 78, 100, 158, 0, 0, 114, 39, 96, 68, 11, 208, 100, 2, 22, 36, 100, 100, 218, 0, 101, 100, 101, 100, 36, 100, 61, 163, 100, 74, 42, 100, 62, 101, 11, 99, 100, 215, 101, 100, 100, 47, 0, 102, 96, 186, 99, 36, 200, 100, 100, 36, 31, 102, 101, 24, 100, 100, 65, 102, 101, 99, 102, 100, 101, 100, 40, 101, 100, 93, 99, 50, 101, 101, 99, 101, 16, 100, 100, 101, 101, 101, 101, 99, 99, 100, 101, 99, 101, 87, 100, 99, 76, 101, 101, 64, 100, 99, 92, 101, 100, 100, 99, 89, 95, 100, 99, 86, 101, 100, 99, 63, 94, 80, 99, 96, 99, 67, 97, 86, 78]
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
      (∀ i ∈ ((insert 75 (insert 25 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs12 support demand
    entries12 ((insert 75 (insert 25 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))))) : Finset (Fin 154)) ((insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)) 100 32 loads12
  decide +kernel
theorem node10 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 25 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 25 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154))
    75 node11 node12
theorem node3 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 51 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154))
    25 node9 node10
def entries7 : List (Fin 2469 × ℕ) := [(77, 116), (421, 9), (456, 7), (472, 89), (518, 24), (550, 38), (552, 122), (616, 35), (617, 38), (689, 66), (731, 96), (741, 32), (778, 78), (779, 8), (780, 29), (784, 37), (785, 34), (798, 55), (843, 4), (859, 7), (870, 89), (872, 14), (874, 125), (888, 44), (922, 38), (924, 67), (925, 41), (933, 1), (934, 27), (944, 74), (960, 11), (966, 117), (973, 153), (1009, 53), (1011, 27), (1044, 16), (1069, 15), (1070, 39), (1073, 12), (1076, 50), (1082, 6), (1086, 4), (1089, 6), (1090, 34), (1108, 11), (1122, 9), (1123, 62), (1128, 5), (1132, 13), (1133, 1), (1137, 6), (1173, 44), (1177, 44), (1179, 19), (1186, 52), (1191, 82), (1197, 7), (1199, 28), (1220, 35), (1248, 42), (1251, 6), (1253, 133), (1266, 13), (1273, 6), (1276, 24), (1403, 5), (1459, 34), (1549, 19), (1660, 4), (1902, 2), (2116, 14), (2132, 47), (2225, 16)]
def cs7 : List ℕ := [257, 63, 89, 117, 250, 117, 35, 257, 257, 0, 140, 257, 257, 174, 233, 160, 257, 241, 256, 44, 192, 35, 0, 285, 249, 257, 346, 277, 116, 35, 257, 52, 146, 257, 161, 256, 413, 0, 182, 300, 117, 54, 196, 0, 545, 257, 0, 0, 96, 257, 257, 0, 0, 256, 256, 256, 257, 80, 256, 122, 473, 145, 223, 256, 257, 147, 255, 0, 256, 256, 410, 257, 227, 218, 97, 626, 255, 204, 372, 256, 244, 551, 255, 256, 109, 248, 256, 254, 55, 256, 255, 180, 256, 256, 158, 255, 215, 255, 256, 255, 256, 256, 255, 256, 255, 255, 256, 219, 256, 77, 256, 256, 256, 164, 255, 257, 255, 256, 256, 256, 205, 254, 256, 255, 221, 256, 257, 255, 191, 248, 256, 219, 255, 255, 236, 256, 256, 198, 257, 256, 164, 255, 237, 257, 185, 228, 209, 256, 251, 256, 256, 256, 256, 235]
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
      (∀ i ∈ ((insert 51 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 75 (insert 26 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs7 support demand
    entries7 ((insert 51 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 75 (insert 26 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))))) : Finset (Fin 154)) 256 32 loads7
  decide +kernel
def entries8 : List (Fin 2469 × ℕ) := [(77, 37), (179, 4), (421, 20), (468, 10), (472, 26), (552, 49), (689, 3), (691, 22), (731, 51), (737, 12), (741, 5), (813, 13), (815, 4), (816, 1), (817, 5), (819, 11), (859, 16), (868, 16), (870, 26), (872, 33), (874, 30), (888, 37), (922, 18), (924, 34), (925, 25), (934, 10), (944, 3), (949, 18), (965, 24), (966, 19), (973, 54), (1009, 20), (1010, 18), (1021, 3), (1043, 22), (1044, 8), (1045, 3), (1073, 28), (1075, 26), (1076, 5), (1081, 18), (1082, 8), (1090, 8), (1182, 6), (1184, 1), (1185, 8), (1186, 16), (1191, 10), (1197, 26), (1199, 12), (1212, 22), (1220, 28), (1253, 37), (1261, 6), (1308, 1), (1403, 11), (1466, 1), (1528, 13), (1545, 1), (1612, 9), (1652, 8), (1666, 8), (1858, 5), (1991, 3)]
def cs8 : List ℕ := [101, 50, 26, 38, 85, 48, 38, 101, 101, 0, 53, 101, 101, 101, 85, 49, 101, 102, 101, 37, 91, 38, 4, 123, 75, 101, 116, 87, 37, 42, 101, 18, 59, 101, 38, 100, 144, 0, 44, 104, 36, 38, 52, 0, 210, 101, 0, 16, 55, 101, 101, 27, 1, 101, 100, 101, 100, 36, 100, 62, 86, 56, 49, 100, 100, 27, 100, 7, 101, 81, 76, 100, 100, 100, 76, 0, 100, 83, 178, 100, 91, 145, 100, 101, 55, 67, 77, 91, 11, 100, 100, 54, 100, 100, 69, 100, 99, 100, 99, 73, 100, 100, 100, 100, 100, 99, 99, 86, 100, 47, 99, 100, 99, 82, 75, 99, 100, 100, 100, 100, 100, 95, 100, 99, 99, 77, 100, 100, 55, 100, 99, 80, 99, 99, 100, 99, 89, 83, 99, 100, 71, 88, 96, 100, 77, 82, 99, 100, 94, 100, 91, 92, 99, 100]
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
      (∀ i ∈ ((insert 75 (insert 51 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 26 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs8 support demand
    entries8 ((insert 75 (insert 51 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))))) : Finset (Fin 154)) ((insert 26 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)) 100 32 loads8
  decide +kernel
theorem node5 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 51 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 26 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 51 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 26 (insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅)))))))))) : Finset (Fin 154))
    75 node7 node8
def entries6 : List (Fin 2469 × ℕ) := [(4, 79), (77, 47), (179, 97), (211, 29), (302, 58), (304, 2), (411, 10), (466, 73), (468, 93), (550, 30), (552, 67), (689, 94), (731, 153), (739, 21), (740, 26), (741, 110), (798, 28), (815, 6), (852, 4), (872, 46), (874, 97), (922, 15), (925, 45), (931, 57), (934, 44), (944, 83), (949, 6), (957, 6), (960, 26), (965, 12), (966, 78), (973, 133), (1009, 51), (1011, 20), (1012, 14), (1043, 38), (1044, 19), (1045, 3), (1061, 19), (1073, 77), (1075, 14), (1082, 16), (1089, 39), (1090, 32), (1123, 12), (1143, 2), (1154, 5), (1173, 56), (1175, 26), (1179, 1), (1186, 16), (1189, 31), (1191, 5), (1197, 55), (1209, 38), (1212, 51), (1220, 43), (1224, 10), (1266, 42), (1276, 16), (1398, 15), (1403, 32), (1417, 19), (1459, 54), (1466, 2), (1488, 4), (1528, 3), (1543, 11), (1545, 6), (1556, 34), (1605, 6), (1701, 45), (1882, 4), (1901, 33), (2225, 32)]
def cs6 : List ℕ := [214, 256, 31, 52, 222, 60, 55, 254, 255, 0, 47, 257, 257, 235, 255, 97, 257, 255, 255, 0, 219, 55, 97, 427, 126, 255, 0, 209, 47, 156, 257, 60, 79, 255, 161, 190, 97, 0, 238, 239, 161, 59, 150, 0, 462, 255, 14, 0, 256, 256, 255, 6, 12, 256, 257, 255, 256, 173, 256, 256, 229, 225, 193, 137, 200, 255, 255, 12, 256, 256, 456, 256, 256, 226, 199, 255, 256, 242, 455, 252, 253, 520, 256, 256, 256, 254, 256, 255, 109, 255, 257, 186, 256, 255, 103, 256, 256, 255, 255, 256, 256, 255, 256, 256, 235, 255, 256, 256, 257, 87, 212, 256, 256, 256, 255, 256, 256, 257, 256, 256, 257, 256, 257, 255, 257, 251, 256, 256, 219, 255, 256, 189, 254, 256, 258, 257, 256, 202, 255, 256, 141, 231, 255, 256, 158, 256, 256, 232, 249, 256, 248, 247, 241, 216]
theorem loads6 : cs6.get =
    load (fun i : Fin entries6.length => support (entries6.get i).1)
      (fun i => (entries6.get i).2) := by
  apply load_eq_of_sparse_packed base cs6 support code
    entries6 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node6 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 26 (insert 51 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs6 support demand
    entries6 ((insert 26 (insert 51 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))))) : Finset (Fin 154)) ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)) 256 32 loads6
  decide +kernel
theorem node4 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 51 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 51 (insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))))) : Finset (Fin 154)) ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154))
    26 node5 node6
theorem node2 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 109 (insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅))))))))) : Finset (Fin 154)) ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154))
    51 node3 node4
theorem node0 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)) ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154))
    109 node1 node2
theorem excludes_context :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 88 (insert 67 (insert 47 (insert 46 (insert 43 (insert 37 (insert 34 (insert 31 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 81 (insert 78 (insert 70 (insert 60 (insert 44 (insert 39 (insert 36 (insert 27 (insert 23 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact node0
#print axioms excludes_context
end OmissionResidual32Resume.Context485517
