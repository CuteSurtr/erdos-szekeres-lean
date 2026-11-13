import Residual32ContextsProof.Catalog
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Resume.Context492357
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
open OmissionResidual32Contexts
-- The initial context is inherited from the frozen original tree.
def entries1 : List (Fin 2469 × ℕ) := [(7, 111), (64, 128), (77, 29), (84, 63), (120, 128), (179, 94), (352, 9), (359, 69), (421, 444), (472, 518), (498, 19), (540, 56), (569, 66), (622, 27), (632, 247), (692, 9), (731, 181), (737, 23), (741, 473), (743, 57), (777, 86), (813, 45), (817, 26), (848, 51), (850, 204), (852, 37), (855, 291), (864, 270), (865, 90), (868, 190), (870, 273), (878, 71), (902, 34), (904, 63), (906, 342), (920, 60), (921, 102), (934, 104), (944, 75), (957, 137), (966, 128), (972, 88), (973, 471), (997, 195), (1009, 38), (1010, 141), (1011, 32), (1012, 134), (1044, 108), (1045, 47), (1061, 81), (1073, 143), (1076, 128), (1077, 29), (1081, 18), (1090, 104), (1114, 4), (1121, 82), (1133, 128), (1147, 79), (1154, 43), (1155, 300), (1169, 52), (1172, 144), (1173, 296), (1175, 51), (1177, 35), (1179, 126), (1186, 43), (1188, 178), (1198, 34), (1201, 58), (1208, 88), (1212, 186), (1222, 84), (1223, 233), (1314, 169), (1349, 225), (1572, 89), (1591, 133), (1593, 399), (1605, 135), (1637, 270), (1645, 274), (2279, 77)]
def cs1 : List ℕ := [267, 510, 1000, 407, 1000, 1001, 0, 1000, 1000, 797, 613, 741, 1000, 1000, 1000, 398, 1000, 1000, 1000, 527, 949, 1000, 94, 1000, 1000, 1805, 1000, 90, 728, 375, 1000, 1000, 0, 1001, 2590, 432, 1221, 1001, 920, 1000, 1000, 581, 75, 52, 2001, 2006, 1000, 190, 862, 1638, 1708, 1000, 384, 1001, 1000, 1001, 1000, 684, 996, 999, 0, 1000, 636, 999, 1000, 2079, 1000, 573, 1000, 1000, 999, 1000, 1000, 571, 1001, 999, 1000, 999, 1972, 1000, 1000, 857, 997, 719, 1000, 1001, 999, 1000, 327, 1000, 999, 913, 701, 0, 435, 933, 1001, 913, 999, 789, 1000, 1001, 999, 1000, 817, 1001, 999, 970, 1000, 522, 1001, 1000, 999, 1001, 999, 1001, 1000, 1000, 1000, 1001, 859, 973, 936, 1000, 1000, 1001, 1001, 1000, 948, 1000, 1000, 1002, 1000, 1000, 924, 1000, 942, 869, 1000, 1439, 1001, 1000, 981, 781, 1000, 959, 953, 1000, 958, 1000, 783, 914, 948, 1000]
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
      (∀ i ∈ ((insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 139 (insert 78 (insert 65 (insert 50 (insert 49 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs1 support demand
    entries1 ((insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)) ((insert 139 (insert 78 (insert 65 (insert 50 (insert 49 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅)))))))))) : Finset (Fin 154)) 1000 32 loads1
  decide +kernel
def entries2 : List (Fin 2469 × ℕ) := [(7, 93), (20, 5), (64, 134), (77, 94), (120, 139), (179, 76), (202, 14), (352, 73), (359, 124), (421, 166), (472, 433), (498, 37), (622, 81), (625, 91), (632, 205), (730, 31), (731, 259), (737, 42), (741, 391), (743, 157), (817, 171), (848, 114), (850, 325), (852, 116), (855, 208), (864, 261), (865, 56), (868, 14), (870, 192), (880, 15), (885, 128), (902, 94), (906, 425), (920, 61), (921, 78), (934, 88), (944, 166), (957, 235), (966, 248), (973, 435), (997, 261), (1009, 118), (1010, 90), (1011, 93), (1012, 122), (1031, 47), (1044, 137), (1073, 136), (1076, 11), (1078, 4), (1081, 24), (1089, 48), (1108, 124), (1122, 54), (1123, 182), (1126, 45), (1132, 55), (1153, 139), (1172, 147), (1173, 272), (1175, 39), (1177, 152), (1183, 133), (1185, 90), (1188, 138), (1201, 78), (1208, 102), (1222, 80), (1223, 145), (1273, 128), (1275, 129), (1314, 205), (1349, 260), (1466, 68), (1572, 101), (1591, 42), (1593, 429), (1605, 50), (1637, 261), (1645, 194), (2225, 32), (2279, 113)]
def cs2 : List ℕ := [145, 558, 1001, 535, 1000, 1000, 0, 1001, 1001, 824, 425, 519, 1000, 1000, 1000, 415, 1001, 1000, 999, 563, 555, 1000, 76, 1001, 985, 1769, 1001, 71, 860, 286, 1001, 1000, 0, 1000, 2762, 411, 1135, 999, 999, 1000, 1000, 507, 166, 0, 2000, 2081, 1000, 14, 925, 1581, 1764, 1001, 440, 1000, 1001, 998, 999, 502, 991, 1000, 0, 1000, 823, 999, 1001, 2154, 1000, 730, 1001, 1001, 1000, 999, 1000, 682, 1000, 1000, 999, 930, 1762, 999, 1000, 948, 1000, 918, 1000, 974, 999, 1001, 462, 1000, 1000, 911, 643, 0, 647, 934, 1001, 878, 1001, 725, 1000, 999, 1000, 999, 813, 961, 1000, 999, 1000, 218, 1000, 1000, 1000, 999, 1001, 1000, 1000, 1000, 1000, 1000, 880, 1000, 797, 1000, 999, 972, 999, 1000, 1000, 1000, 891, 1000, 1000, 1001, 882, 1000, 999, 661, 1000, 435, 890, 832, 900, 1000, 883, 804, 930, 751, 1000, 707, 1001, 755, 574, 915]
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
      (∀ i ∈ ((insert 139 (insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 78 (insert 65 (insert 50 (insert 49 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs2 support demand
    entries2 ((insert 139 (insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅))))))))) : Finset (Fin 154)) ((insert 78 (insert 65 (insert 50 (insert 49 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)) 1000 32 loads2
  decide +kernel
theorem node0 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 78 (insert 65 (insert 50 (insert 49 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact split_excludes support demand 32 ((insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)) ((insert 78 (insert 65 (insert 50 (insert 49 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154))
    139 node1 node2
theorem excludes_context :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 109 (insert 93 (insert 88 (insert 67 (insert 60 (insert 47 (insert 43 (insert 27 ∅)))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 78 (insert 65 (insert 50 (insert 49 (insert 45 (insert 44 (insert 36 (insert 34 (insert 25 ∅))))))))) : Finset (Fin 154)), holes i = 0) := by
  exact node0
#print axioms excludes_context
end OmissionResidual32Resume.Context492357
