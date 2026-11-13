import Residual32ContextsProof.Catalog
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace OmissionResidual32Contexts
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
-- Conditional arithmetic exclusion; geometric row validity is explicit.
def entries30 : List (Fin 2469 × ℕ) := [(7, 504), (122, 207), (238, 540), (275, 293), (326, 95), (465, 136), (466, 451), (475, 86), (484, 86), (507, 43), (572, 288), (577, 156), (617, 158), (624, 306), (674, 98), (737, 3), (739, 67), (798, 202), (850, 289), (873, 289), (876, 42), (903, 171), (904, 209), (905, 243), (920, 236), (926, 8), (941, 355), (944, 223), (945, 42), (946, 137), (948, 374), (963, 265), (967, 68), (968, 307), (970, 181), (973, 542), (978, 54), (992, 73), (994, 39), (995, 328), (1004, 11), (1009, 91), (1010, 27), (1012, 3), (1028, 17), (1030, 4), (1061, 62), (1075, 6), (1076, 111), (1101, 14), (1102, 69), (1108, 21), (1123, 28), (1128, 44), (1131, 36), (1133, 5), (1139, 6), (1140, 29), (1141, 110), (1146, 33), (1154, 1), (1155, 99), (1167, 154), (1174, 100), (1175, 25), (1177, 108), (1178, 64), (1179, 235), (1183, 190), (1186, 170), (1223, 294), (1254, 169), (1318, 53), (1442, 55), (1443, 71), (1516, 41), (1559, 376), (1572, 46), (1580, 31), (1585, 86), (1931, 174), (1932, 3), (1950, 52)]
def cs30 : List ℕ := [745, 673, 0, 375, 1001, 86, 0, 1000, 689, 43, 0, 1000, 1601, 1001, 305, 207, 1000, 1001, 1001, 288, 1375, 711, 0, 1000, 666, 0, 999, 0, 889, 540, 1000, 857, 516, 1000, 1787, 1000, 1001, 1001, 0, 1000, 1001, 1001, 234, 669, 2204, 1000, 1587, 0, 762, 1000, 919, 1417, 0, 1000, 640, 2369, 1000, 1001, 887, 1001, 1332, 1000, 436, 947, 1000, 1001, 1000, 344, 999, 1499, 1001, 999, 999, 1445, 1000, 1000, 1000, 1001, 1000, 1001, 1001, 0, 1000, 999, 669, 1001, 999, 1001, 2642, 822, 1000, 1000, 1266, 2343, 692, 758, 843, 933, 927, 1000, 1000, 1001, 1000, 467, 736, 1604, 845, 882, 712, 1987, 1002, 1000, 110, 1000, 1001, 830, 1000, 1000, 1001, 1001, 1001, 1001, 740, 1001, 1000, 867, 1001, 1000, 1000, 1002, 1001, 1001, 1001, 1000, 1000, 972, 821, 1001, 1002, 1001, 1000, 1001, 997, 1002, 918, 974, 1001, 887, 1000, 1002, 1001, 1000, 1001, 1001]
theorem loads30 : cs30.get =
    load (fun i : Fin entries30.length => support (entries30.get i).1)
      (fun i => (entries30.get i).2) := by
  apply load_eq_of_sparse_packed base cs30 support code
    entries30 code_correct
  · decide +kernel
  · decide +kernel
  · decide +kernel
  · decide +kernel
theorem node30 :
    ¬ ∃ holes : Fin 154 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧
      (∑ i, holes i) ≤ 32 ∧
      (∀ i ∈ ((insert 112 (insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)), holes i = 1) ∧
      (∀ i ∈ ((insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)), holes i = 0) := by
  apply sparse_list_conditioned_excludes cs30 support demand
    entries30 ((insert 112 (insert 81 (insert 67 (insert 54 (insert 47 (insert 27 (insert 25 ∅))))))) : Finset (Fin 154)) ((insert 109 (insert 105 (insert 93 (insert 92 (insert 88 (insert 73 (insert 69 (insert 60 (insert 55 (insert 51 (insert 46 (insert 44 (insert 43 (insert 34 (insert 20 (insert 12 ∅)))))))))))))))) : Finset (Fin 154)) 1000 32 loads30
  decide +kernel
#print axioms node30
end OmissionResidual32Contexts
