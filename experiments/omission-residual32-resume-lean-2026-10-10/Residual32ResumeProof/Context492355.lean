import Residual32ContextsProof.Catalog
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Resume.Context492355
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open OmissionResidual32Contexts
-- The initial context is inherited from the frozen original tree.
def entries17 : List (Fin 2469 × ℕ) := [(13, 434), (30, 154), (64, 840), (77, 2765), (84, 1489), (118, 1247), (120, 945), (132, 228), (179, 3659), (271, 1882), (350, 420), (454, 689), (466, 1543), (472, 1162), (498, 752), (622, 473), (623, 1305), (624, 29), (630, 5244), (730, 1976), (740, 2873), (741, 1574), (845, 282), (850, 1058), (852, 2202), (855, 3698), (862, 277), (864, 3414), (868, 3635), (870, 1606), (872, 255), (878, 2149), (880, 1236), (885, 2627), (906, 1545), (920, 1637), (922, 554), (924, 816), (934, 2965), (940, 1026), (944, 2183), (965, 1160), (966, 68), (970, 473), (973, 4728), (997, 1728), (1010, 1701), (1011, 1175), (1020, 425), (1031, 1025), (1044, 612), (1045, 574), (1061, 303), (1073, 200), (1081, 199), (1096, 2248), (1111, 604), (1123, 2374), (1133, 1066), (1153, 330), (1154, 800), (1158, 432), (1172, 1674), (1173, 3599), (1175, 400), (1177, 296), (1178, 569), (1179, 701), (1186, 599), (1203, 514), (1204, 4510), (1210, 62), (1212, 1075), (1219, 479), (1221, 1908), (1224, 5), (1249, 394), (1258, 12), (1261, 1648), (1308, 1666), (1344, 227), (1364, 205), (1403, 1607), (1555, 2954), (1559, 1851), (1591, 108), (1593, 2631), (1605, 427), (1642, 1987), (2009, 1096), (2225, 730)]
def cs17 : List ℕ := [3965, 5852, 10001, 6047, 7293, 10001, 0, 10002, 10001, 7981, 6400, 7092, 10002, 10000, 10000, 3428, 10001, 10000, 10000, 3471, 10001, 10001, 3659, 10001, 4694, 24544, 10001, 1715, 8615, 9999, 10001, 10000, 2698, 10001, 28354, 5478, 14020, 10000, 10000, 9999, 10000, 10000, 2183, 282, 21831, 24318, 10001, 3635, 10000, 10001, 18436, 9122, 5669, 10001, 12753, 10001, 17602, 8677, 10000, 7363, 816, 10001, 9999, 10000, 10002, 17490, 10002, 2149, 10000, 10000, 10001, 10000, 10000, 10000, 10001, 10001, 9999, 10001, 20270, 10000, 7546, 10000, 10000, 7742, 10000, 10002, 15215, 10001, 1169, 10001, 17444, 7934, 10001, 21737, 5279, 10000, 9665, 10000, 10001, 7854, 9999, 10001, 10001, 10000, 10000, 10001, 10002, 10002, 10000, 2944, 8372, 11009, 9171, 5496, 9221, 10001, 10002, 10001, 10001, 9998, 6497, 10002, 10000, 10002, 10001, 10001, 9999, 10001, 7123, 10002, 10002, 9843, 10000, 10001, 10000, 10001, 9455, 10001, 10001, 10001, 10000, 10001, 9026, 10001, 10002, 9682, 10001, 9074, 8219, 10001, 10002, 9165, 8639, 9356]
theorem loads17 : cs17.get =
    load (fun i : Fin entries17.length => support (entries17.get i).1)
      (fun i => (entries17.get i).2) := by
  apply load_eq_of_sparse_packed base cs17 support code
    entries17 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node17 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 86 (insert 90 (insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs17 support demand
    entries17 ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)) ((insert 86 (insert 90 (insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))))) : Finset (Fin 154)) 10000 32 loads17
  decide +kernel
def entries18 : List (Fin 2469 × ℕ) := [(13, 172), (64, 98), (77, 296), (84, 251), (118, 191), (120, 77), (132, 81), (179, 288), (286, 16), (411, 12), (431, 68), (466, 44), (472, 206), (498, 143), (569, 32), (623, 276), (630, 327), (632, 132), (667, 18), (675, 9), (730, 76), (740, 208), (741, 134), (833, 199), (850, 268), (852, 291), (855, 258), (864, 273), (868, 374), (870, 36), (874, 102), (878, 259), (885, 330), (906, 64), (920, 265), (922, 3), (924, 284), (934, 141), (940, 143), (944, 240), (965, 309), (966, 76), (973, 479), (997, 248), (1010, 183), (1031, 90), (1033, 13), (1044, 16), (1045, 202), (1061, 72), (1065, 109), (1066, 15), (1111, 43), (1123, 242), (1133, 63), (1154, 92), (1158, 80), (1172, 171), (1173, 350), (1177, 71), (1186, 67), (1201, 53), (1204, 340), (1210, 53), (1212, 104), (1221, 282), (1224, 5), (1226, 186), (1258, 32), (1261, 105), (1286, 67), (1293, 101), (1348, 110), (1403, 76), (1482, 15), (1488, 60), (1559, 35), (1576, 16), (1591, 114), (1593, 340), (1616, 110), (1991, 45), (2009, 67), (2225, 56), (2458, 136)]
def cs18 : List ℕ := [326, 451, 1000, 608, 742, 1000, 0, 1000, 1001, 778, 670, 671, 1000, 1000, 1001, 268, 1001, 1001, 1000, 438, 964, 1001, 288, 1001, 270, 2646, 1000, 0, 1001, 829, 1001, 1001, 302, 1001, 2742, 573, 1480, 1000, 1001, 1002, 1001, 827, 240, 0, 2170, 2156, 1001, 374, 1000, 1001, 2059, 1001, 474, 1000, 1376, 999, 1904, 908, 763, 841, 284, 1000, 1001, 1000, 1000, 1603, 1000, 259, 1000, 999, 1001, 904, 999, 999, 1000, 708, 1000, 1001, 2060, 1001, 708, 1000, 1000, 961, 925, 1000, 411, 1000, 367, 1001, 1746, 812, 912, 2017, 858, 835, 903, 1001, 1000, 823, 1000, 1000, 1001, 1000, 489, 1000, 1000, 1000, 1000, 171, 1001, 1110, 892, 784, 1000, 1000, 1000, 998, 1000, 1000, 1000, 950, 1000, 1000, 999, 1000, 1001, 1000, 532, 1000, 999, 1000, 1001, 999, 1000, 999, 980, 998, 1000, 1000, 999, 1001, 810, 1000, 865, 853, 1000, 864, 1000, 1000, 948, 1000, 774, 760]
theorem loads18 : cs18.get =
    load (fun i : Fin entries18.length => support (entries18.get i).1)
      (fun i => (entries18.get i).2) := by
  apply load_eq_of_sparse_packed base cs18 support code
    entries18 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node18 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 86 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 90 (insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs18 support demand
    entries18 ((insert 86 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)) ((insert 90 (insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))))) : Finset (Fin 154)) 1000 32 loads18
  decide +kernel
theorem node13 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 90 (insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)) ((insert 90 (insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))))) : Finset (Fin 154))
    86 node17 node18
def entries15 : List (Fin 2469 × ℕ) := [(37, 48), (64, 406), (70, 67), (77, 275), (84, 66), (120, 339), (132, 10), (153, 14), (179, 52), (199, 143), (228, 119), (271, 37), (359, 5), (447, 160), (457, 41), (472, 450), (483, 8), (498, 131), (569, 199), (623, 35), (625, 15), (630, 143), (632, 315), (675, 83), (692, 91), (739, 241), (740, 183), (741, 179), (743, 20), (816, 83), (832, 26), (833, 105), (850, 150), (852, 219), (855, 392), (864, 259), (868, 469), (870, 320), (878, 118), (880, 199), (885, 63), (888, 28), (906, 59), (922, 209), (924, 177), (944, 363), (945, 16), (965, 1), (970, 160), (973, 555), (978, 18), (1009, 163), (1010, 60), (1011, 85), (1031, 44), (1044, 19), (1045, 34), (1076, 170), (1090, 125), (1108, 85), (1119, 57), (1123, 176), (1128, 72), (1133, 29), (1153, 21), (1154, 116), (1155, 102), (1169, 34), (1172, 57), (1173, 191), (1175, 187), (1177, 68), (1178, 24), (1179, 167), (1186, 57), (1204, 308), (1210, 138), (1221, 230), (1224, 89), (1226, 305), (1232, 17), (1258, 85), (1348, 104), (1349, 94), (1364, 34), (1370, 83), (1403, 50), (1559, 73), (1576, 39), (1593, 286), (1642, 12), (1667, 126), (1991, 30), (2168, 54), (2225, 85)]
def cs15 : List ℕ := [230, 535, 1000, 458, 754, 964, 0, 1000, 1000, 951, 811, 843, 1000, 1000, 1000, 538, 1000, 1000, 1000, 782, 1000, 1000, 52, 1000, 672, 2320, 1001, 199, 999, 577, 1000, 1000, 214, 1000, 2664, 692, 1836, 1000, 1000, 1000, 889, 841, 363, 52, 1857, 2417, 1000, 469, 1000, 1000, 1792, 1000, 458, 1000, 1001, 1000, 1931, 1000, 1000, 997, 177, 999, 1000, 999, 1001, 1666, 1002, 246, 1000, 1000, 1001, 999, 999, 999, 1000, 803, 1797, 785, 1785, 1000, 848, 1000, 574, 999, 1000, 1000, 1001, 1000, 736, 1001, 306, 658, 970, 1599, 893, 694, 1000, 1000, 1000, 1001, 1000, 999, 999, 1001, 810, 1000, 1001, 1001, 1000, 248, 1000, 1000, 964, 650, 1000, 1001, 1001, 1000, 1001, 1001, 1001, 1000, 988, 1001, 1001, 1000, 1001, 1000, 657, 1001, 1000, 980, 1001, 1000, 1001, 1000, 1001, 1000, 999, 1001, 1001, 1001, 918, 1001, 1002, 1001, 854, 913, 1000, 1001, 1000, 937, 1001, 731]
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
      (∀ i ∈ ((insert 90 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 76 (insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs15 support demand
    entries15 ((insert 90 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)) ((insert 76 (insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))))) : Finset (Fin 154)) 1000 32 loads15
  decide +kernel
def entries16 : List (Fin 2469 × ℕ) := [(10, 51), (62, 211), (77, 4099), (84, 1167), (120, 2760), (132, 171), (179, 106), (271, 1332), (420, 405), (421, 431), (472, 5184), (483, 328), (507, 704), (569, 309), (572, 1176), (623, 1454), (630, 2200), (632, 2465), (673, 2036), (692, 468), (730, 1524), (731, 2124), (739, 727), (740, 3289), (743, 87), (815, 700), (816, 138), (817, 83), (842, 906), (845, 21), (850, 1097), (852, 479), (855, 4238), (864, 1103), (868, 4128), (870, 3349), (872, 2550), (878, 388), (906, 2255), (922, 2760), (924, 4059), (940, 582), (944, 3923), (970, 2465), (973, 4795), (996, 527), (997, 882), (1010, 716), (1011, 2471), (1012, 767), (1031, 745), (1044, 824), (1045, 367), (1076, 68), (1081, 789), (1090, 2073), (1096, 594), (1108, 318), (1123, 2905), (1133, 386), (1153, 336), (1154, 1958), (1169, 789), (1173, 4416), (1175, 789), (1186, 446), (1203, 1106), (1204, 3260), (1221, 1505), (1224, 2811), (1251, 317), (1258, 1183), (1269, 26), (1273, 762), (1308, 1014), (1322, 446), (1349, 1147), (1403, 1561), (1555, 446), (1559, 1680), (1593, 2823), (1667, 343), (1836, 7), (2225, 1958)]
def cs16 : List ℕ := [2611, 7198, 10000, 4357, 7707, 10000, 0, 10000, 10000, 4841, 8227, 8832, 10000, 10001, 10000, 2760, 9999, 10000, 10001, 4210, 10000, 10000, 106, 10000, 8471, 22191, 10000, 0, 10000, 4771, 10000, 10000, 6095, 10001, 21688, 7325, 16322, 10000, 9999, 9999, 10000, 7726, 3923, 810, 22550, 18207, 10002, 4128, 5441, 9999, 19436, 10001, 4665, 8896, 10000, 10001, 21745, 9059, 7142, 8392, 4059, 10001, 10000, 9999, 10000, 17433, 10000, 2324, 9999, 10000, 10000, 9835, 10000, 10000, 10000, 9999, 1892, 9721, 19180, 9999, 10001, 10000, 5513, 10000, 10000, 10000, 10001, 10000, 3254, 9999, 5308, 9468, 8794, 16890, 10000, 4824, 10001, 10001, 10000, 7093, 10000, 10000, 5962, 7120, 7835, 10001, 10001, 9299, 10001, 1208, 10001, 10000, 5962, 6440, 7237, 10000, 10001, 10000, 10000, 10001, 10001, 10001, 7870, 10001, 10000, 10000, 10000, 10001, 4288, 10000, 10001, 7913, 10000, 10001, 8066, 10000, 10000, 8654, 10001, 10001, 10001, 10000, 7953, 8655, 10001, 6178, 10000, 8421, 7110, 10000, 10001, 6733, 9061, 6449]
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
      (∀ i ∈ ((insert 76 (insert 90 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs16 support demand
    entries16 ((insert 76 (insert 90 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)) ((insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)) 10000 32 loads16
  decide +kernel
theorem node14 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 90 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 90 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)) ((insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154))
    76 node15 node16
theorem node1 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)) ((insert 56 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154))
    90 node13 node14
def entries11 : List (Fin 2469 × ℕ) := [(64, 150), (72, 24), (118, 150), (359, 91), (420, 6), (421, 85), (456, 65), (472, 465), (540, 12), (569, 160), (625, 97), (630, 301), (632, 6), (737, 327), (740, 240), (741, 68), (742, 32), (798, 99), (835, 74), (844, 79), (848, 68), (850, 223), (855, 309), (864, 307), (865, 160), (870, 242), (876, 40), (878, 53), (885, 146), (906, 474), (922, 137), (940, 183), (965, 273), (966, 213), (972, 125), (973, 512), (997, 69), (1004, 1), (1005, 69), (1009, 4), (1010, 310), (1011, 29), (1012, 240), (1045, 118), (1061, 80), (1069, 15), (1075, 180), (1078, 19), (1082, 7), (1090, 105), (1096, 340), (1099, 15), (1120, 62), (1123, 205), (1133, 107), (1153, 196), (1154, 80), (1155, 58), (1172, 27), (1173, 431), (1177, 41), (1178, 42), (1186, 7), (1188, 3), (1201, 215), (1204, 241), (1212, 49), (1221, 148), (1224, 229), (1236, 12), (1258, 139), (1261, 105), (1317, 15), (1348, 63), (1349, 144), (1499, 99), (1503, 215), (1545, 129), (1559, 195), (1576, 69), (1593, 316), (1598, 79), (1605, 56), (1660, 121)]
def cs11 : List ℕ := [239, 685, 1001, 464, 776, 1000, 0, 1001, 1001, 852, 263, 631, 1000, 1001, 808, 150, 1000, 1000, 999, 545, 877, 1001, 0, 1001, 951, 1785, 1000, 160, 776, 307, 1000, 1000, 0, 1001, 2675, 389, 1216, 999, 419, 999, 1000, 646, 70, 79, 1989, 2070, 1001, 0, 992, 1593, 1724, 1001, 436, 1001, 1002, 998, 0, 716, 999, 936, 0, 1000, 686, 1001, 1001, 1852, 1000, 326, 998, 999, 1000, 999, 776, 999, 1001, 985, 999, 777, 1357, 998, 888, 999, 1002, 852, 797, 999, 999, 955, 358, 829, 1000, 1000, 971, 2027, 619, 999, 1001, 999, 837, 723, 998, 1000, 1000, 1001, 869, 1000, 1000, 623, 998, 223, 1000, 1000, 999, 997, 1001, 998, 998, 999, 1000, 999, 998, 1000, 650, 999, 960, 974, 999, 1000, 999, 999, 1000, 890, 2196, 999, 998, 999, 999, 1000, 999, 998, 997, 1000, 607, 998, 999, 997, 999, 700, 998, 999, 781, 773, 998, 626]
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
      (∀ i ∈ ((insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 49 (insert 132 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs11 support demand
    entries11 ((insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)) ((insert 49 (insert 132 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))))) : Finset (Fin 154)) 1000 32 loads11
  decide +kernel
def entries12 : List (Fin 2469 × ℕ) := [(0, 28), (12, 43), (32, 7), (35, 46), (64, 48), (70, 60), (72, 37), (118, 35), (359, 20), (421, 36), (456, 11), (466, 76), (479, 19), (572, 99), (624, 27), (630, 120), (632, 15), (667, 104), (675, 56), (689, 7), (690, 2), (692, 32), (740, 27), (741, 31), (806, 7), (835, 34), (844, 33), (852, 51), (855, 116), (857, 5), (864, 140), (870, 87), (876, 29), (885, 29), (916, 1), (922, 75), (957, 22), (965, 72), (966, 52), (970, 35), (972, 50), (973, 131), (1002, 16), (1005, 35), (1010, 67), (1012, 54), (1045, 38), (1061, 36), (1075, 22), (1078, 12), (1089, 1), (1090, 41), (1096, 62), (1120, 63), (1123, 71), (1133, 42), (1139, 5), (1153, 16), (1154, 6), (1173, 125), (1204, 102), (1221, 17), (1224, 13), (1258, 73), (1261, 11), (1298, 31), (1348, 11), (1503, 13), (1547, 29), (1559, 16), (1576, 35), (1593, 59), (1660, 65)]
def cs12 : List ℕ := [154, 115, 162, 102, 256, 245, 5, 209, 255, 247, 97, 193, 255, 255, 256, 35, 135, 255, 256, 256, 173, 256, 0, 255, 0, 577, 256, 5, 211, 241, 255, 256, 104, 256, 576, 182, 162, 256, 103, 255, 257, 257, 35, 33, 493, 704, 257, 0, 178, 17, 509, 257, 157, 255, 256, 256, 0, 171, 235, 222, 0, 257, 173, 256, 198, 365, 257, 23, 256, 257, 232, 257, 255, 257, 256, 179, 256, 176, 312, 255, 257, 256, 255, 248, 151, 257, 256, 255, 48, 255, 256, 256, 174, 604, 202, 232, 256, 256, 208, 224, 256, 256, 255, 256, 187, 256, 251, 199, 256, 50, 256, 268, 257, 244, 257, 255, 256, 255, 256, 256, 256, 257, 167, 256, 255, 256, 256, 256, 234, 256, 236, 214, 542, 256, 256, 256, 256, 256, 257, 256, 256, 256, 144, 256, 256, 256, 256, 172, 217, 256, 207, 173, 226, 131]
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
      (∀ i ∈ ((insert 49 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 132 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs12 support demand
    entries12 ((insert 49 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)) ((insert 132 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)) 256 32 loads12
  decide +kernel
theorem node3 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 132 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)) ((insert 132 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154))
    49 node11 node12
def entries9 : List (Fin 2469 × ℕ) := [(7, 19), (12, 19), (64, 42), (70, 6), (72, 29), (118, 35), (421, 15), (457, 28), (468, 38), (472, 49), (625, 20), (630, 68), (632, 43), (689, 26), (690, 41), (731, 27), (737, 19), (740, 112), (741, 42), (743, 13), (817, 26), (844, 14), (848, 60), (850, 29), (852, 36), (855, 116), (864, 111), (870, 36), (878, 25), (885, 72), (906, 28), (921, 25), (922, 13), (940, 48), (957, 66), (965, 26), (966, 78), (970, 24), (971, 30), (973, 107), (995, 19), (1009, 60), (1010, 54), (1011, 52), (1043, 2), (1044, 12), (1069, 58), (1076, 61), (1086, 9), (1121, 2), (1122, 33), (1123, 59), (1133, 19), (1137, 19), (1158, 12), (1159, 25), (1172, 4), (1173, 66), (1175, 12), (1178, 23), (1179, 33), (1186, 34), (1203, 30), (1204, 91), (1210, 37), (1212, 49), (1221, 36), (1224, 23), (1249, 7), (1273, 5), (1316, 1), (1343, 24), (1545, 46), (1559, 95), (1576, 23), (1593, 74), (1645, 35), (1701, 3)]
def cs9 : List ℕ := [80, 238, 255, 120, 255, 256, 0, 256, 255, 227, 35, 170, 256, 256, 218, 35, 255, 256, 256, 135, 136, 255, 0, 255, 77, 584, 256, 0, 256, 117, 256, 255, 0, 256, 646, 59, 318, 256, 129, 255, 241, 165, 0, 14, 510, 550, 257, 0, 222, 255, 505, 256, 223, 256, 256, 255, 0, 162, 256, 170, 0, 257, 257, 257, 256, 432, 255, 137, 256, 256, 256, 191, 257, 257, 257, 255, 256, 256, 240, 445, 226, 255, 257, 216, 252, 256, 255, 256, 36, 257, 257, 178, 196, 482, 199, 138, 257, 256, 253, 256, 255, 256, 241, 257, 194, 257, 237, 220, 255, 175, 199, 256, 256, 194, 255, 255, 234, 387, 256, 256, 257, 255, 240, 163, 258, 256, 257, 255, 186, 255, 258, 220, 163, 255, 194, 258, 257, 186, 257, 256, 257, 229, 247, 230, 257, 187, 229, 220, 245, 256, 255, 256, 256, 195]
theorem loads9 : cs9.get =
    load (fun i : Fin entries9.length => support (entries9.get i).1)
      (fun i => (entries9.get i).2) := by
  apply load_eq_of_sparse_packed base cs9 support code
    entries9 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node9 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 117 (insert 79 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs9 support demand
    entries9 ((insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)) ((insert 117 (insert 79 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))))) : Finset (Fin 154)) 256 32 loads9
  decide +kernel
def entries10 : List (Fin 2469 × ℕ) := [(7, 4), (64, 19), (72, 14), (118, 19), (350, 24), (420, 33), (421, 11), (468, 14), (472, 6), (498, 3), (623, 4), (625, 12), (630, 33), (632, 12), (689, 1), (740, 51), (817, 9), (833, 13), (844, 12), (848, 12), (852, 18), (855, 55), (862, 3), (864, 45), (870, 18), (885, 19), (906, 25), (920, 9), (921, 7), (934, 10), (940, 35), (964, 5), (973, 47), (995, 1), (996, 4), (997, 14), (1010, 11), (1011, 24), (1031, 4), (1044, 15), (1061, 2), (1069, 8), (1076, 14), (1078, 6), (1082, 2), (1090, 9), (1122, 24), (1123, 15), (1133, 12), (1137, 9), (1159, 23), (1172, 1), (1173, 43), (1175, 2), (1186, 10), (1188, 12), (1203, 4), (1204, 38), (1210, 23), (1221, 13), (1224, 1), (1249, 5), (1261, 1), (1272, 13), (1343, 1), (1348, 5), (1360, 6), (1370, 22), (1417, 3), (1559, 17), (1576, 18), (1593, 28), (1598, 7), (1605, 2), (1642, 20), (1645, 4), (1795, 3)]
def cs10 : List ℕ := [29, 84, 99, 38, 98, 100, 0, 99, 100, 99, 21, 69, 101, 100, 86, 19, 99, 99, 100, 54, 40, 100, 0, 99, 54, 228, 99, 0, 100, 45, 100, 100, 0, 99, 279, 45, 114, 100, 50, 101, 99, 86, 0, 12, 197, 214, 99, 0, 92, 100, 201, 100, 48, 100, 100, 100, 0, 52, 99, 42, 0, 100, 60, 101, 100, 166, 100, 0, 100, 99, 101, 90, 93, 99, 100, 100, 100, 79, 102, 162, 95, 99, 102, 47, 66, 101, 99, 101, 14, 100, 102, 92, 91, 242, 56, 36, 90, 100, 99, 101, 101, 99, 101, 101, 76, 100, 99, 101, 101, 24, 99, 100, 100, 59, 100, 100, 100, 10, 100, 100, 99, 99, 85, 51, 100, 100, 100, 99, 57, 100, 99, 85, 50, 99, 47, 100, 100, 64, 98, 100, 94, 93, 82, 91, 99, 52, 97, 81, 81, 100, 70, 80, 94, 63]
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
      (∀ i ∈ ((insert 117 (insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 79 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs10 support demand
    entries10 ((insert 117 (insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))))) : Finset (Fin 154)) ((insert 79 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)) 100 32 loads10
  decide +kernel
theorem node5 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 79 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)) ((insert 79 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154))
    117 node9 node10
def entries7 : List (Fin 2469 × ℕ) := [(10, 1), (64, 20), (118, 22), (348, 59), (421, 24), (448, 33), (466, 54), (468, 9), (472, 48), (540, 23), (542, 18), (572, 17), (617, 8), (623, 21), (630, 89), (632, 31), (689, 4), (731, 9), (740, 120), (741, 61), (743, 29), (797, 11), (798, 14), (813, 17), (817, 57), (852, 42), (855, 89), (864, 122), (865, 47), (870, 9), (874, 2), (885, 19), (906, 102), (916, 10), (934, 19), (960, 15), (965, 12), (966, 72), (973, 91), (975, 38), (997, 31), (1005, 6), (1009, 12), (1010, 35), (1011, 34), (1031, 30), (1043, 26), (1069, 4), (1081, 18), (1107, 5), (1108, 72), (1121, 37), (1122, 19), (1123, 44), (1133, 17), (1137, 18), (1155, 28), (1158, 20), (1159, 11), (1172, 42), (1173, 93), (1177, 22), (1179, 54), (1186, 14), (1201, 54), (1204, 137), (1210, 23), (1217, 9), (1219, 34), (1221, 61), (1251, 37), (1269, 30), (1273, 14), (1316, 19), (1349, 1), (1370, 20), (1555, 5), (1559, 83), (1576, 41), (1593, 42), (1645, 26), (2168, 12)]
def cs7 : List ℕ := [124, 257, 256, 171, 257, 255, 0, 257, 256, 184, 47, 237, 256, 256, 256, 22, 257, 257, 256, 79, 256, 256, 0, 423, 150, 482, 256, 90, 193, 120, 257, 256, 0, 257, 770, 69, 280, 256, 46, 256, 255, 156, 65, 0, 525, 452, 255, 0, 175, 256, 447, 254, 138, 256, 257, 256, 0, 166, 255, 110, 0, 254, 179, 255, 256, 517, 257, 11, 256, 255, 256, 256, 255, 255, 250, 257, 257, 237, 293, 77, 209, 256, 256, 200, 197, 257, 257, 256, 37, 257, 257, 230, 247, 440, 159, 185, 188, 256, 193, 256, 256, 255, 256, 257, 207, 256, 256, 238, 256, 101, 255, 256, 256, 226, 250, 256, 256, 256, 256, 256, 251, 256, 232, 257, 255, 256, 234, 256, 208, 256, 256, 228, 145, 255, 144, 256, 256, 235, 255, 255, 256, 256, 223, 256, 250, 187, 251, 237, 256, 198, 256, 201, 256, 152]
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
      (∀ i ∈ ((insert 79 (insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 23 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs7 support demand
    entries7 ((insert 79 (insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))))) : Finset (Fin 154)) ((insert 23 (insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)) 256 32 loads7
  decide +kernel
def entries8 : List (Fin 2469 × ℕ) := [(10, 13), (17, 3), (35, 1), (43, 1), (64, 2), (118, 2), (348, 7), (420, 2), (421, 4), (448, 2), (472, 4), (557, 5), (569, 1), (572, 5), (617, 2), (630, 15), (632, 2), (731, 2), (737, 1), (740, 18), (741, 5), (743, 6), (813, 1), (817, 3), (845, 17), (848, 4), (852, 6), (855, 15), (857, 1), (864, 16), (870, 4), (878, 6), (906, 14), (916, 2), (922, 1), (934, 3), (960, 1), (965, 1), (966, 9), (971, 1), (973, 13), (975, 6), (997, 5), (1005, 1), (1009, 2), (1010, 4), (1011, 2), (1031, 1), (1069, 2), (1107, 3), (1108, 5), (1121, 2), (1122, 5), (1123, 4), (1133, 4), (1155, 2), (1158, 3), (1172, 6), (1173, 11), (1175, 2), (1179, 8), (1186, 3), (1201, 2), (1251, 3), (1269, 4), (1273, 6), (1316, 1), (1370, 5), (1559, 10), (1575, 1), (1576, 2), (1600, 7), (1637, 3), (1645, 6)]
def cs8 : List ℕ := [0, 19, 31, 3, 31, 25, 2, 31, 13, 18, 3, 10, 32, 31, 12, 12, 9, 28, 32, 14, 24, 31, 0, 2, 18, 67, 31, 1, 31, 19, 32, 31, 0, 31, 90, 14, 27, 33, 10, 32, 31, 19, 8, 17, 62, 60, 31, 0, 19, 32, 60, 31, 17, 31, 32, 32, 3, 24, 31, 19, 0, 31, 18, 32, 32, 67, 32, 8, 32, 32, 32, 32, 32, 32, 31, 32, 31, 28, 44, 8, 28, 32, 32, 24, 25, 31, 31, 32, 3, 30, 33, 31, 32, 57, 24, 21, 27, 32, 32, 32, 32, 31, 33, 32, 25, 32, 31, 30, 32, 19, 32, 32, 32, 24, 31, 31, 32, 32, 32, 31, 32, 32, 28, 32, 31, 32, 24, 31, 23, 30, 32, 28, 21, 32, 20, 32, 31, 28, 33, 32, 32, 32, 29, 32, 31, 26, 31, 27, 32, 27, 32, 28, 32, 24]
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
      (∀ i ∈ ((insert 23 (insert 79 (insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs8 support demand
    entries8 ((insert 23 (insert 79 (insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))))) : Finset (Fin 154)) ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)) 32 32 loads8
  decide +kernel
theorem node6 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 79 (insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 79 (insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))))) : Finset (Fin 154)) ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154))
    23 node7 node8
theorem node4 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 132 (insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)) ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154))
    79 node5 node6
theorem node2 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 56 (insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)) ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154))
    132 node3 node4
theorem node0 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)) ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154))
    56 node1 node2
theorem excludes_context :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 93 (insert 78 (insert 65 (insert 50 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact node0
#print axioms excludes_context
end OmissionResidual32Resume.Context492355
