import Catalog
import ErdosSzekeres.Omission.CoverCuts
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace ResidualCoverCuts
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
-- Original catalog SHA-256: bccd12477064d8a490bbe863ae49dbc8d9dfececf7a65426ba36f7537c66293a
-- Each derived row is proved from original rows by a strict integer margin.
def support0 : Finset (Fin 154) := {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153}
theorem cut0 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    27 ≤ ∑ i ∈ support0, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 466, OmissionResidual.support 469, OmissionResidual.support 475, OmissionResidual.support 479, OmissionResidual.support 483, OmissionResidual.support 485, OmissionResidual.support 491, OmissionResidual.support 498, OmissionResidual.support 507, OmissionResidual.support 515, OmissionResidual.support 531, OmissionResidual.support 542, OmissionResidual.support 552, OmissionResidual.support 571, OmissionResidual.support 572, OmissionResidual.support 581, OmissionResidual.support 584, OmissionResidual.support 585, OmissionResidual.support 587, OmissionResidual.support 588, OmissionResidual.support 625, OmissionResidual.support 630, OmissionResidual.support 631, OmissionResidual.support 632, OmissionResidual.support 679, OmissionResidual.support 681, OmissionResidual.support 690, OmissionResidual.support 691, OmissionResidual.support 731, OmissionResidual.support 737, OmissionResidual.support 739, OmissionResidual.support 741, OmissionResidual.support 742, OmissionResidual.support 779, OmissionResidual.support 781, OmissionResidual.support 797, OmissionResidual.support 798, OmissionResidual.support 813, OmissionResidual.support 819, OmissionResidual.support 832, OmissionResidual.support 843, OmissionResidual.support 844, OmissionResidual.support 846, OmissionResidual.support 852, OmissionResidual.support 854, OmissionResidual.support 856, OmissionResidual.support 857, OmissionResidual.support 862, OmissionResidual.support 863, OmissionResidual.support 865, OmissionResidual.support 866, OmissionResidual.support 869, OmissionResidual.support 870, OmissionResidual.support 874, OmissionResidual.support 879, OmissionResidual.support 880, OmissionResidual.support 883, OmissionResidual.support 884, OmissionResidual.support 886, OmissionResidual.support 900, OmissionResidual.support 902, OmissionResidual.support 904, OmissionResidual.support 906, OmissionResidual.support 908, OmissionResidual.support 918, OmissionResidual.support 922, OmissionResidual.support 924, OmissionResidual.support 925, OmissionResidual.support 932, OmissionResidual.support 934, OmissionResidual.support 938, OmissionResidual.support 940, OmissionResidual.support 943, OmissionResidual.support 944, OmissionResidual.support 946, OmissionResidual.support 948, OmissionResidual.support 950, OmissionResidual.support 956, OmissionResidual.support 958, OmissionResidual.support 960, OmissionResidual.support 964, OmissionResidual.support 965, OmissionResidual.support 966, OmissionResidual.support 968, OmissionResidual.support 969, OmissionResidual.support 971, OmissionResidual.support 972, OmissionResidual.support 973, OmissionResidual.support 978, OmissionResidual.support 985, OmissionResidual.support 996, OmissionResidual.support 1005, OmissionResidual.support 1011, OmissionResidual.support 1012, OmissionResidual.support 1024, OmissionResidual.support 1025, OmissionResidual.support 1031, OmissionResidual.support 1049, OmissionResidual.support 1056, OmissionResidual.support 1061, OmissionResidual.support 1073, OmissionResidual.support 1076, OmissionResidual.support 1082, OmissionResidual.support 1100, OmissionResidual.support 1102, OmissionResidual.support 1104, OmissionResidual.support 1108, OmissionResidual.support 1111, OmissionResidual.support 1121, OmissionResidual.support 1123, OmissionResidual.support 1128, OmissionResidual.support 1139, OmissionResidual.support 1141, OmissionResidual.support 1143, OmissionResidual.support 1147, OmissionResidual.support 1153, OmissionResidual.support 1155, OmissionResidual.support 1160, OmissionResidual.support 1164, OmissionResidual.support 1165, OmissionResidual.support 1167, OmissionResidual.support 1171, OmissionResidual.support 1175, OmissionResidual.support 1179, OmissionResidual.support 1183, OmissionResidual.support 1186] ![OmissionResidual.demand 466, OmissionResidual.demand 469, OmissionResidual.demand 475, OmissionResidual.demand 479, OmissionResidual.demand 483, OmissionResidual.demand 485, OmissionResidual.demand 491, OmissionResidual.demand 498, OmissionResidual.demand 507, OmissionResidual.demand 515, OmissionResidual.demand 531, OmissionResidual.demand 542, OmissionResidual.demand 552, OmissionResidual.demand 571, OmissionResidual.demand 572, OmissionResidual.demand 581, OmissionResidual.demand 584, OmissionResidual.demand 585, OmissionResidual.demand 587, OmissionResidual.demand 588, OmissionResidual.demand 625, OmissionResidual.demand 630, OmissionResidual.demand 631, OmissionResidual.demand 632, OmissionResidual.demand 679, OmissionResidual.demand 681, OmissionResidual.demand 690, OmissionResidual.demand 691, OmissionResidual.demand 731, OmissionResidual.demand 737, OmissionResidual.demand 739, OmissionResidual.demand 741, OmissionResidual.demand 742, OmissionResidual.demand 779, OmissionResidual.demand 781, OmissionResidual.demand 797, OmissionResidual.demand 798, OmissionResidual.demand 813, OmissionResidual.demand 819, OmissionResidual.demand 832, OmissionResidual.demand 843, OmissionResidual.demand 844, OmissionResidual.demand 846, OmissionResidual.demand 852, OmissionResidual.demand 854, OmissionResidual.demand 856, OmissionResidual.demand 857, OmissionResidual.demand 862, OmissionResidual.demand 863, OmissionResidual.demand 865, OmissionResidual.demand 866, OmissionResidual.demand 869, OmissionResidual.demand 870, OmissionResidual.demand 874, OmissionResidual.demand 879, OmissionResidual.demand 880, OmissionResidual.demand 883, OmissionResidual.demand 884, OmissionResidual.demand 886, OmissionResidual.demand 900, OmissionResidual.demand 902, OmissionResidual.demand 904, OmissionResidual.demand 906, OmissionResidual.demand 908, OmissionResidual.demand 918, OmissionResidual.demand 922, OmissionResidual.demand 924, OmissionResidual.demand 925, OmissionResidual.demand 932, OmissionResidual.demand 934, OmissionResidual.demand 938, OmissionResidual.demand 940, OmissionResidual.demand 943, OmissionResidual.demand 944, OmissionResidual.demand 946, OmissionResidual.demand 948, OmissionResidual.demand 950, OmissionResidual.demand 956, OmissionResidual.demand 958, OmissionResidual.demand 960, OmissionResidual.demand 964, OmissionResidual.demand 965, OmissionResidual.demand 966, OmissionResidual.demand 968, OmissionResidual.demand 969, OmissionResidual.demand 971, OmissionResidual.demand 972, OmissionResidual.demand 973, OmissionResidual.demand 978, OmissionResidual.demand 985, OmissionResidual.demand 996, OmissionResidual.demand 1005, OmissionResidual.demand 1011, OmissionResidual.demand 1012, OmissionResidual.demand 1024, OmissionResidual.demand 1025, OmissionResidual.demand 1031, OmissionResidual.demand 1049, OmissionResidual.demand 1056, OmissionResidual.demand 1061, OmissionResidual.demand 1073, OmissionResidual.demand 1076, OmissionResidual.demand 1082, OmissionResidual.demand 1100, OmissionResidual.demand 1102, OmissionResidual.demand 1104, OmissionResidual.demand 1108, OmissionResidual.demand 1111, OmissionResidual.demand 1121, OmissionResidual.demand 1123, OmissionResidual.demand 1128, OmissionResidual.demand 1139, OmissionResidual.demand 1141, OmissionResidual.demand 1143, OmissionResidual.demand 1147, OmissionResidual.demand 1153, OmissionResidual.demand 1155, OmissionResidual.demand 1160, OmissionResidual.demand 1164, OmissionResidual.demand 1165, OmissionResidual.demand 1167, OmissionResidual.demand 1171, OmissionResidual.demand 1175, OmissionResidual.demand 1179, OmissionResidual.demand 1183, OmissionResidual.demand 1186] ![45, 64, 21, 62, 77, 15, 44, 36, 66, 46, 38, 58, 4, 5, 54, 20, 4, 28, 44, 36, 27, 22, 9, 53, 33, 51, 8, 14, 55, 10, 9, 11, 3, 18, 4, 20, 10, 19, 27, 9, 32, 34, 23, 28, 24, 1, 27, 2, 14, 1, 1, 21, 29, 31, 7, 34, 13, 37, 24, 16, 38, 31, 14, 32, 37, 3, 45, 29, 6, 25, 32, 25, 21, 56, 3, 22, 39, 10, 27, 18, 22, 9, 10, 28, 9, 44, 9, 118, 32, 29, 21, 5, 3, 19, 3, 2, 16, 15, 21, 5, 18, 4, 15, 5, 4, 20, 10, 4, 7, 2, 11, 38, 2, 16, 14, 5, 26, 11, 33, 23, 68, 69, 66, 53, 11, 55]
    support0 256 27 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 466) (Fin.cases (hrows 469) (Fin.cases (hrows 475) (Fin.cases (hrows 479) (Fin.cases (hrows 483) (Fin.cases (hrows 485) (Fin.cases (hrows 491) (Fin.cases (hrows 498) (Fin.cases (hrows 507) (Fin.cases (hrows 515) (Fin.cases (hrows 531) (Fin.cases (hrows 542) (Fin.cases (hrows 552) (Fin.cases (hrows 571) (Fin.cases (hrows 572) (Fin.cases (hrows 581) (Fin.cases (hrows 584) (Fin.cases (hrows 585) (Fin.cases (hrows 587) (Fin.cases (hrows 588) (Fin.cases (hrows 625) (Fin.cases (hrows 630) (Fin.cases (hrows 631) (Fin.cases (hrows 632) (Fin.cases (hrows 679) (Fin.cases (hrows 681) (Fin.cases (hrows 690) (Fin.cases (hrows 691) (Fin.cases (hrows 731) (Fin.cases (hrows 737) (Fin.cases (hrows 739) (Fin.cases (hrows 741) (Fin.cases (hrows 742) (Fin.cases (hrows 779) (Fin.cases (hrows 781) (Fin.cases (hrows 797) (Fin.cases (hrows 798) (Fin.cases (hrows 813) (Fin.cases (hrows 819) (Fin.cases (hrows 832) (Fin.cases (hrows 843) (Fin.cases (hrows 844) (Fin.cases (hrows 846) (Fin.cases (hrows 852) (Fin.cases (hrows 854) (Fin.cases (hrows 856) (Fin.cases (hrows 857) (Fin.cases (hrows 862) (Fin.cases (hrows 863) (Fin.cases (hrows 865) (Fin.cases (hrows 866) (Fin.cases (hrows 869) (Fin.cases (hrows 870) (Fin.cases (hrows 874) (Fin.cases (hrows 879) (Fin.cases (hrows 880) (Fin.cases (hrows 883) (Fin.cases (hrows 884) (Fin.cases (hrows 886) (Fin.cases (hrows 900) (Fin.cases (hrows 902) (Fin.cases (hrows 904) (Fin.cases (hrows 906) (Fin.cases (hrows 908) (Fin.cases (hrows 918) (Fin.cases (hrows 922) (Fin.cases (hrows 924) (Fin.cases (hrows 925) (Fin.cases (hrows 932) (Fin.cases (hrows 934) (Fin.cases (hrows 938) (Fin.cases (hrows 940) (Fin.cases (hrows 943) (Fin.cases (hrows 944) (Fin.cases (hrows 946) (Fin.cases (hrows 948) (Fin.cases (hrows 950) (Fin.cases (hrows 956) (Fin.cases (hrows 958) (Fin.cases (hrows 960) (Fin.cases (hrows 964) (Fin.cases (hrows 965) (Fin.cases (hrows 966) (Fin.cases (hrows 968) (Fin.cases (hrows 969) (Fin.cases (hrows 971) (Fin.cases (hrows 972) (Fin.cases (hrows 973) (Fin.cases (hrows 978) (Fin.cases (hrows 985) (Fin.cases (hrows 996) (Fin.cases (hrows 1005) (Fin.cases (hrows 1011) (Fin.cases (hrows 1012) (Fin.cases (hrows 1024) (Fin.cases (hrows 1025) (Fin.cases (hrows 1031) (Fin.cases (hrows 1049) (Fin.cases (hrows 1056) (Fin.cases (hrows 1061) (Fin.cases (hrows 1073) (Fin.cases (hrows 1076) (Fin.cases (hrows 1082) (Fin.cases (hrows 1100) (Fin.cases (hrows 1102) (Fin.cases (hrows 1104) (Fin.cases (hrows 1108) (Fin.cases (hrows 1111) (Fin.cases (hrows 1121) (Fin.cases (hrows 1123) (Fin.cases (hrows 1128) (Fin.cases (hrows 1139) (Fin.cases (hrows 1141) (Fin.cases (hrows 1143) (Fin.cases (hrows 1147) (Fin.cases (hrows 1153) (Fin.cases (hrows 1155) (Fin.cases (hrows 1160) (Fin.cases (hrows 1164) (Fin.cases (hrows 1165) (Fin.cases (hrows 1167) (Fin.cases (hrows 1171) (Fin.cases (hrows 1175) (Fin.cases (hrows 1179) (Fin.cases (hrows 1183) (Fin.cases (hrows 1186) (fun i => Fin.elim0 i)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#print axioms cut0
def support1 : Finset (Fin 154) := {48, 58, 61, 69, 71, 73, 76, 80, 81, 84, 88, 92, 98, 112, 120, 128}
theorem cut1 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 730, OmissionResidual.support 960, OmissionResidual.support 946] ![OmissionResidual.demand 730, OmissionResidual.demand 960, OmissionResidual.demand 946] ![1, 1, 1]
    support1 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 730) (Fin.cases (hrows 960) (Fin.cases (hrows 946) (fun i => Fin.elim0 i))))
def support2 : Finset (Fin 154) := {1, 2, 4, 7, 8, 14, 17, 18, 23, 25, 27, 33, 34, 39, 44, 53}
theorem cut2 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support2, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 847, OmissionResidual.support 846, OmissionResidual.support 4] ![OmissionResidual.demand 847, OmissionResidual.demand 846, OmissionResidual.demand 4] ![1, 1, 1]
    support2 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 847) (Fin.cases (hrows 846) (Fin.cases (hrows 4) (fun i => Fin.elim0 i))))
def support3 : Finset (Fin 154) := {0, 1, 2, 4, 7, 8, 14, 17, 18, 23, 25, 27, 33, 34, 39, 44, 53}
theorem cut3 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support3, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 847, OmissionResidual.support 846, OmissionResidual.support 0] ![OmissionResidual.demand 847, OmissionResidual.demand 846, OmissionResidual.demand 0] ![1, 1, 1]
    support3 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 847) (Fin.cases (hrows 846) (Fin.cases (hrows 0) (fun i => Fin.elim0 i))))
def support4 : Finset (Fin 154) := {0, 3, 4, 5, 8, 12, 14, 17, 18, 23, 25, 27, 33, 34, 39, 44, 53}
theorem cut4 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support4, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 853, OmissionResidual.support 849, OmissionResidual.support 0] ![OmissionResidual.demand 853, OmissionResidual.demand 849, OmissionResidual.demand 0] ![1, 1, 1]
    support4 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 853) (Fin.cases (hrows 849) (Fin.cases (hrows 0) (fun i => Fin.elim0 i))))
def support5 : Finset (Fin 154) := {1, 3, 4, 5, 8, 12, 14, 17, 18, 23, 25, 27, 33, 34, 39, 44, 53}
theorem cut5 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support5, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 853, OmissionResidual.support 849, OmissionResidual.support 4] ![OmissionResidual.demand 853, OmissionResidual.demand 849, OmissionResidual.demand 4] ![1, 1, 1]
    support5 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 853) (Fin.cases (hrows 849) (Fin.cases (hrows 4) (fun i => Fin.elim0 i))))
def support6 : Finset (Fin 154) := {0, 4, 8, 14, 17, 23, 25, 33, 43, 53, 65, 77, 89, 91, 101, 110}
theorem cut6 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support6, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 984, OmissionResidual.support 978, OmissionResidual.support 0] ![OmissionResidual.demand 984, OmissionResidual.demand 978, OmissionResidual.demand 0] ![1, 1, 1]
    support6 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 984) (Fin.cases (hrows 978) (Fin.cases (hrows 0) (fun i => Fin.elim0 i))))
def support7 : Finset (Fin 154) := {1, 4, 8, 14, 17, 23, 25, 33, 43, 53, 65, 77, 89, 91, 101, 110}
theorem cut7 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support7, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 984, OmissionResidual.support 978, OmissionResidual.support 4] ![OmissionResidual.demand 984, OmissionResidual.demand 978, OmissionResidual.demand 4] ![1, 1, 1]
    support7 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 984) (Fin.cases (hrows 978) (Fin.cases (hrows 4) (fun i => Fin.elim0 i))))
def support8 : Finset (Fin 154) := {0, 4, 6, 8, 10, 14, 17, 20, 23, 25, 27, 33, 37, 45, 50, 55, 65}
theorem cut8 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support8, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 865, OmissionResidual.support 857, OmissionResidual.support 0] ![OmissionResidual.demand 865, OmissionResidual.demand 857, OmissionResidual.demand 0] ![1, 1, 1]
    support8 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 865) (Fin.cases (hrows 857) (Fin.cases (hrows 0) (fun i => Fin.elim0 i))))
def support9 : Finset (Fin 154) := {1, 4, 6, 8, 10, 14, 17, 20, 23, 25, 27, 33, 37, 45, 50, 55, 65}
theorem cut9 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support9, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 865, OmissionResidual.support 857, OmissionResidual.support 4] ![OmissionResidual.demand 865, OmissionResidual.demand 857, OmissionResidual.demand 4] ![1, 1, 1]
    support9 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 865) (Fin.cases (hrows 857) (Fin.cases (hrows 4) (fun i => Fin.elim0 i))))
def support10 : Finset (Fin 154) := {0, 4, 5, 6, 8, 13, 14, 17, 21, 23, 25, 29, 33, 41, 45, 55}
theorem cut10 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support10, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 0, OmissionResidual.support 35, OmissionResidual.support 43] ![OmissionResidual.demand 0, OmissionResidual.demand 35, OmissionResidual.demand 43] ![1, 1, 1]
    support10 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 35) (Fin.cases (hrows 43) (fun i => Fin.elim0 i))))
def support11 : Finset (Fin 154) := {0, 3, 4, 8, 10, 13, 14, 17, 21, 23, 25, 29, 33, 41, 45, 55}
theorem cut11 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support11, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 0, OmissionResidual.support 70, OmissionResidual.support 20] ![OmissionResidual.demand 0, OmissionResidual.demand 70, OmissionResidual.demand 20] ![1, 1, 1]
    support11 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 70) (Fin.cases (hrows 20) (fun i => Fin.elim0 i))))
def support12 : Finset (Fin 154) := {1, 4, 5, 6, 8, 13, 14, 17, 21, 23, 25, 29, 33, 41, 45, 55}
theorem cut12 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support12, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 4, OmissionResidual.support 35, OmissionResidual.support 43] ![OmissionResidual.demand 4, OmissionResidual.demand 35, OmissionResidual.demand 43] ![1, 1, 1]
    support12 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 4) (Fin.cases (hrows 35) (Fin.cases (hrows 43) (fun i => Fin.elim0 i))))
def support13 : Finset (Fin 154) := {1, 3, 4, 8, 10, 13, 14, 17, 21, 23, 25, 29, 33, 41, 45, 55}
theorem cut13 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support13, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 4, OmissionResidual.support 70, OmissionResidual.support 20] ![OmissionResidual.demand 4, OmissionResidual.demand 70, OmissionResidual.demand 20] ![1, 1, 1]
    support13 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 4) (Fin.cases (hrows 70) (Fin.cases (hrows 20) (fun i => Fin.elim0 i))))
def support14 : Finset (Fin 154) := {1, 4, 5, 8, 13, 14, 17, 21, 23, 25, 31, 33, 34, 44}
theorem cut14 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support14, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 4, OmissionResidual.support 30, OmissionResidual.support 7] ![OmissionResidual.demand 4, OmissionResidual.demand 30, OmissionResidual.demand 7] ![1, 1, 1]
    support14 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 4) (Fin.cases (hrows 30) (Fin.cases (hrows 7) (fun i => Fin.elim0 i))))
def support15 : Finset (Fin 154) := {0, 2, 3, 4, 8, 13, 14, 17, 21, 23, 25, 31, 33, 34, 44}
theorem cut15 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support15, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 0, OmissionResidual.support 10, OmissionResidual.support 17] ![OmissionResidual.demand 0, OmissionResidual.demand 10, OmissionResidual.demand 17] ![1, 1, 1]
    support15 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 10) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support16 : Finset (Fin 154) := {0, 1, 4, 5, 8, 13, 14, 17, 21, 23, 25, 31, 33, 34, 44}
theorem cut16 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support16, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 0, OmissionResidual.support 30, OmissionResidual.support 7] ![OmissionResidual.demand 0, OmissionResidual.demand 30, OmissionResidual.demand 7] ![1, 1, 1]
    support16 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 30) (Fin.cases (hrows 7) (fun i => Fin.elim0 i))))
def support17 : Finset (Fin 154) := {1, 2, 3, 4, 8, 13, 14, 17, 21, 23, 25, 31, 33, 34, 44}
theorem cut17 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support17, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 4, OmissionResidual.support 10, OmissionResidual.support 17] ![OmissionResidual.demand 4, OmissionResidual.demand 10, OmissionResidual.demand 17] ![1, 1, 1]
    support17 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 4) (Fin.cases (hrows 10) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support18 : Finset (Fin 154) := {10, 14, 20, 21, 25, 29, 33, 36, 41, 45, 47, 55, 60, 66, 75}
theorem cut18 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support18, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 875, OmissionResidual.support 70, OmissionResidual.support 866] ![OmissionResidual.demand 875, OmissionResidual.demand 70, OmissionResidual.demand 866] ![1, 1, 1]
    support18 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 875) (Fin.cases (hrows 70) (Fin.cases (hrows 866) (fun i => Fin.elim0 i))))
def support19 : Finset (Fin 154) := {5, 8, 10, 13, 14, 20, 25, 29, 33, 36, 41, 45, 47, 55, 60, 66, 75}
theorem cut19 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support19, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 875, OmissionResidual.support 35, OmissionResidual.support 866] ![OmissionResidual.demand 875, OmissionResidual.demand 35, OmissionResidual.demand 866] ![1, 1, 1]
    support19 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 875) (Fin.cases (hrows 35) (Fin.cases (hrows 866) (fun i => Fin.elim0 i))))
def support20 : Finset (Fin 154) := {0, 4, 8, 11, 14, 16, 17, 23, 25, 30, 33, 39, 50, 56, 62, 67, 77}
theorem cut20 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support20, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 869, OmissionResidual.support 0, OmissionResidual.support 883] ![OmissionResidual.demand 869, OmissionResidual.demand 0, OmissionResidual.demand 883] ![1, 1, 1]
    support20 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 869) (Fin.cases (hrows 0) (Fin.cases (hrows 883) (fun i => Fin.elim0 i))))
def support21 : Finset (Fin 154) := {1, 4, 8, 11, 14, 16, 17, 23, 25, 30, 33, 39, 50, 56, 62, 67, 77}
theorem cut21 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support21, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 869, OmissionResidual.support 4, OmissionResidual.support 883] ![OmissionResidual.demand 869, OmissionResidual.demand 4, OmissionResidual.demand 883] ![1, 1, 1]
    support21 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 869) (Fin.cases (hrows 4) (Fin.cases (hrows 883) (fun i => Fin.elim0 i))))
def support22 : Finset (Fin 154) := {0, 4, 8, 11, 14, 16, 17, 23, 25, 30, 33, 39, 50, 62, 68, 79, 89}
theorem cut22 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support22, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 870, OmissionResidual.support 0, OmissionResidual.support 885] ![OmissionResidual.demand 870, OmissionResidual.demand 0, OmissionResidual.demand 885] ![1, 1, 1]
    support22 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 870) (Fin.cases (hrows 0) (Fin.cases (hrows 885) (fun i => Fin.elim0 i))))
def support23 : Finset (Fin 154) := {1, 4, 8, 11, 14, 16, 17, 23, 25, 30, 33, 39, 50, 62, 68, 79, 89}
theorem cut23 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support23, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 870, OmissionResidual.support 4, OmissionResidual.support 885] ![OmissionResidual.demand 870, OmissionResidual.demand 4, OmissionResidual.demand 885] ![1, 1, 1]
    support23 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 870) (Fin.cases (hrows 4) (Fin.cases (hrows 885) (fun i => Fin.elim0 i))))
def support24 : Finset (Fin 154) := {109, 116, 123, 127, 129, 133, 134, 138, 139, 142, 144, 146, 148, 150, 152}
theorem cut24 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support24, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1145, OmissionResidual.support 1147, OmissionResidual.support 1163] ![OmissionResidual.demand 1145, OmissionResidual.demand 1147, OmissionResidual.demand 1163] ![1, 1, 1]
    support24 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1145) (Fin.cases (hrows 1147) (Fin.cases (hrows 1163) (fun i => Fin.elim0 i))))
def support25 : Finset (Fin 154) := {68, 79, 89, 90, 99, 100, 107, 108, 109, 115, 116, 117, 122, 123, 124, 129, 130, 133, 134, 135, 138, 139, 140, 142, 143, 144, 146, 147, 148, 149, 150, 151, 152, 153}
theorem cut25 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    7 ≤ ∑ i ∈ support25, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1186, OmissionResidual.support 1164, OmissionResidual.support 1184] ![OmissionResidual.demand 1186, OmissionResidual.demand 1164, OmissionResidual.demand 1184] ![1, 1, 1]
    support25 2 7 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1186) (Fin.cases (hrows 1164) (Fin.cases (hrows 1184) (fun i => Fin.elim0 i))))
#print axioms cut25
def support26 : Finset (Fin 154) := {2, 4, 7, 13, 21, 25, 26, 31, 33, 34, 36, 44, 49, 54, 64}
theorem cut26 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support26, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 848, OmissionResidual.support 10, OmissionResidual.support 851] ![OmissionResidual.demand 848, OmissionResidual.demand 10, OmissionResidual.demand 851] ![1, 1, 1]
    support26 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 848) (Fin.cases (hrows 10) (Fin.cases (hrows 851) (fun i => Fin.elim0 i))))
def support27 : Finset (Fin 154) := {5, 8, 12, 13, 21, 25, 26, 31, 33, 34, 36, 44, 49, 54, 64}
theorem cut27 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support27, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 854, OmissionResidual.support 30, OmissionResidual.support 859] ![OmissionResidual.demand 854, OmissionResidual.demand 30, OmissionResidual.demand 859] ![1, 1, 1]
    support27 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 854) (Fin.cases (hrows 30) (Fin.cases (hrows 859) (fun i => Fin.elim0 i))))
def support28 : Finset (Fin 154) := {2, 4, 5, 7, 8, 13, 21, 25, 26, 31, 33, 34, 36, 44, 49, 54, 64}
theorem cut28 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support28, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 848, OmissionResidual.support 30, OmissionResidual.support 851] ![OmissionResidual.demand 848, OmissionResidual.demand 30, OmissionResidual.demand 851] ![1, 1, 1]
    support28 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 848) (Fin.cases (hrows 30) (Fin.cases (hrows 851) (fun i => Fin.elim0 i))))
def support29 : Finset (Fin 154) := {2, 4, 5, 8, 12, 13, 21, 25, 26, 31, 33, 34, 36, 44, 49, 54, 64}
theorem cut29 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support29, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 854, OmissionResidual.support 10, OmissionResidual.support 859] ![OmissionResidual.demand 854, OmissionResidual.demand 10, OmissionResidual.demand 859] ![1, 1, 1]
    support29 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 854) (Fin.cases (hrows 10) (Fin.cases (hrows 859) (fun i => Fin.elim0 i))))
def support30 : Finset (Fin 154) := {0, 2, 5, 7, 11, 12, 16, 18, 20, 23, 25, 27, 30, 34, 39, 44, 53}
theorem cut30 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support30, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 847, OmissionResidual.support 853, OmissionResidual.support 466] ![OmissionResidual.demand 847, OmissionResidual.demand 853, OmissionResidual.demand 466] ![1, 1, 1]
    support30 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 847) (Fin.cases (hrows 853) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support31 : Finset (Fin 154) := {1, 2, 5, 7, 11, 12, 16, 18, 20, 23, 25, 27, 30, 34, 39, 44, 53}
theorem cut31 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support31, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 847, OmissionResidual.support 853, OmissionResidual.support 468] ![OmissionResidual.demand 847, OmissionResidual.demand 853, OmissionResidual.demand 468] ![1, 1, 1]
    support31 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 847) (Fin.cases (hrows 853) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support32 : Finset (Fin 154) := {1, 3, 7, 11, 12, 16, 17, 18, 20, 23, 27, 30, 34, 39, 44, 53}
theorem cut32 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support32, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 846, OmissionResidual.support 849, OmissionResidual.support 468] ![OmissionResidual.demand 846, OmissionResidual.demand 849, OmissionResidual.demand 468] ![1, 1, 1]
    support32 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 846) (Fin.cases (hrows 849) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support33 : Finset (Fin 154) := {0, 1, 3, 7, 11, 12, 16, 17, 18, 20, 23, 27, 30, 34, 39, 44, 53}
theorem cut33 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support33, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 846, OmissionResidual.support 849, OmissionResidual.support 466] ![OmissionResidual.demand 846, OmissionResidual.demand 849, OmissionResidual.demand 466] ![1, 1, 1]
    support33 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 846) (Fin.cases (hrows 849) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support34 : Finset (Fin 154) := {0, 2, 5, 7, 11, 12, 16, 20, 23, 25, 26, 30, 34, 36, 49, 54, 64}
theorem cut34 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support34, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 848, OmissionResidual.support 854, OmissionResidual.support 466] ![OmissionResidual.demand 848, OmissionResidual.demand 854, OmissionResidual.demand 466] ![1, 1, 1]
    support34 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 848) (Fin.cases (hrows 854) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support35 : Finset (Fin 154) := {1, 2, 5, 7, 11, 12, 16, 20, 23, 25, 26, 30, 34, 36, 49, 54, 64}
theorem cut35 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support35, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 848, OmissionResidual.support 854, OmissionResidual.support 468] ![OmissionResidual.demand 848, OmissionResidual.demand 854, OmissionResidual.demand 468] ![1, 1, 1]
    support35 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 848) (Fin.cases (hrows 854) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support36 : Finset (Fin 154) := {0, 4, 7, 8, 11, 12, 16, 20, 23, 30, 33, 35, 44, 46, 54, 59, 74}
theorem cut36 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support36, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 852, OmissionResidual.support 860, OmissionResidual.support 466] ![OmissionResidual.demand 852, OmissionResidual.demand 860, OmissionResidual.demand 466] ![1, 1, 1]
    support36 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 852) (Fin.cases (hrows 860) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support37 : Finset (Fin 154) := {1, 4, 7, 8, 11, 12, 16, 20, 23, 30, 33, 35, 44, 46, 54, 59, 74}
theorem cut37 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support37, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 852, OmissionResidual.support 860, OmissionResidual.support 468] ![OmissionResidual.demand 852, OmissionResidual.demand 860, OmissionResidual.demand 468] ![1, 1, 1]
    support37 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 852) (Fin.cases (hrows 860) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support38 : Finset (Fin 154) := {48, 58, 61, 69, 71, 73, 76, 80, 81, 84, 88, 92, 98, 112, 120, 121, 128}
theorem cut38 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support38, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 959, OmissionResidual.support 731, OmissionResidual.support 946] ![OmissionResidual.demand 959, OmissionResidual.demand 731, OmissionResidual.demand 946] ![1, 1, 1]
    support38 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 959) (Fin.cases (hrows 731) (Fin.cases (hrows 946) (fun i => Fin.elim0 i))))
def support39 : Finset (Fin 154) := {48, 58, 61, 69, 71, 73, 76, 80, 81, 84, 88, 92, 98, 112, 120, 121}
theorem cut39 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support39, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 959, OmissionResidual.support 731, OmissionResidual.support 945] ![OmissionResidual.demand 959, OmissionResidual.demand 731, OmissionResidual.demand 945] ![1, 1, 1]
    support39 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 959) (Fin.cases (hrows 731) (Fin.cases (hrows 945) (fun i => Fin.elim0 i))))
def support40 : Finset (Fin 154) := {21, 27, 31, 38, 46, 47, 51, 52, 57, 63, 69, 73, 82, 93}
theorem cut40 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support40, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 585, OmissionResidual.support 583] ![OmissionResidual.demand 678, OmissionResidual.demand 585, OmissionResidual.demand 583] ![1, 1, 1]
    support40 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 585) (Fin.cases (hrows 583) (fun i => Fin.elim0 i))))
def support41 : Finset (Fin 154) := {79, 89, 101, 107, 115, 123, 130, 133, 138, 139, 142, 146, 147, 148, 150, 153}
theorem cut41 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support41, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1090, OmissionResidual.support 1164, OmissionResidual.support 1089] ![OmissionResidual.demand 1090, OmissionResidual.demand 1164, OmissionResidual.demand 1089] ![1, 1, 1]
    support41 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1090) (Fin.cases (hrows 1164) (Fin.cases (hrows 1089) (fun i => Fin.elim0 i))))
def support42 : Finset (Fin 154) := {109, 116, 123, 127, 129, 133, 134, 138, 139, 142, 144, 146, 148, 150, 152, 153}
theorem cut42 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support42, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1145, OmissionResidual.support 1147, OmissionResidual.support 1164] ![OmissionResidual.demand 1145, OmissionResidual.demand 1147, OmissionResidual.demand 1164] ![1, 1, 1]
    support42 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1145) (Fin.cases (hrows 1147) (Fin.cases (hrows 1164) (fun i => Fin.elim0 i))))
def support43 : Finset (Fin 154) := {109, 116, 123, 127, 129, 133, 134, 138, 139, 140, 142, 146, 148, 150, 151, 153}
theorem cut43 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support43, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1146, OmissionResidual.support 1144, OmissionResidual.support 1164] ![OmissionResidual.demand 1146, OmissionResidual.demand 1144, OmissionResidual.demand 1164] ![1, 1, 1]
    support43 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1146) (Fin.cases (hrows 1144) (Fin.cases (hrows 1164) (fun i => Fin.elim0 i))))
def support44 : Finset (Fin 154) := {100, 108, 115, 119, 122, 129, 133, 135, 138, 139, 142, 146, 148, 149, 150, 153}
theorem cut44 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support44, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1131, OmissionResidual.support 1164, OmissionResidual.support 1130] ![OmissionResidual.demand 1131, OmissionResidual.demand 1164, OmissionResidual.demand 1130] ![1, 1, 1]
    support44 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1131) (Fin.cases (hrows 1164) (Fin.cases (hrows 1130) (fun i => Fin.elim0 i))))
def support45 : Finset (Fin 154) := {100, 108, 115, 119, 122, 133, 134, 138, 139, 140, 142, 146, 148, 150, 151, 153}
theorem cut45 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support45, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1132, OmissionResidual.support 1133, OmissionResidual.support 1164] ![OmissionResidual.demand 1132, OmissionResidual.demand 1133, OmissionResidual.demand 1164] ![1, 1, 1]
    support45 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1132) (Fin.cases (hrows 1133) (Fin.cases (hrows 1164) (fun i => Fin.elim0 i))))
def support46 : Finset (Fin 154) := {90, 99, 107, 111, 115, 123, 130, 133, 138, 139, 142, 146, 147, 148, 150, 153}
theorem cut46 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support46, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1111, OmissionResidual.support 1164, OmissionResidual.support 1110] ![OmissionResidual.demand 1111, OmissionResidual.demand 1164, OmissionResidual.demand 1110] ![1, 1, 1]
    support46 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1111) (Fin.cases (hrows 1164) (Fin.cases (hrows 1110) (fun i => Fin.elim0 i))))
def support47 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 84, 93, 112}
theorem cut47 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support47, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 681, OmissionResidual.support 730] ![OmissionResidual.demand 678, OmissionResidual.demand 681, OmissionResidual.demand 730] ![1, 1, 1]
    support47 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 681) (Fin.cases (hrows 730) (fun i => Fin.elim0 i))))
def support48 : Finset (Fin 154) := {83, 93, 94, 97, 102, 103, 106, 108, 112, 116, 120, 124, 134, 135, 140}
theorem cut48 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support48, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 842, OmissionResidual.support 833, OmissionResidual.support 834] ![OmissionResidual.demand 842, OmissionResidual.demand 833, OmissionResidual.demand 834] ![1, 1, 1]
    support48 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 842) (Fin.cases (hrows 833) (Fin.cases (hrows 834) (fun i => Fin.elim0 i))))
def support49 : Finset (Fin 154) := {0, 4, 5, 7, 11, 12, 16, 20, 23, 24, 26, 30, 31, 36, 40, 49}
theorem cut49 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support49, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 478, OmissionResidual.support 483, OmissionResidual.support 466] ![OmissionResidual.demand 478, OmissionResidual.demand 483, OmissionResidual.demand 466] ![1, 1, 1]
    support49 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 478) (Fin.cases (hrows 483) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support50 : Finset (Fin 154) := {1, 4, 5, 7, 11, 12, 16, 20, 23, 24, 26, 30, 31, 36, 40, 49}
theorem cut50 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support50, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 478, OmissionResidual.support 483, OmissionResidual.support 468] ![OmissionResidual.demand 478, OmissionResidual.demand 483, OmissionResidual.demand 468] ![1, 1, 1]
    support50 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 478) (Fin.cases (hrows 483) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
#print axioms cut50
def support51 : Finset (Fin 154) := {0, 2, 7, 8, 11, 12, 16, 20, 23, 24, 26, 30, 31, 36, 40, 49}
theorem cut51 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support51, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 495, OmissionResidual.support 472, OmissionResidual.support 466] ![OmissionResidual.demand 495, OmissionResidual.demand 472, OmissionResidual.demand 466] ![1, 1, 1]
    support51 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 495) (Fin.cases (hrows 472) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support52 : Finset (Fin 154) := {1, 2, 7, 8, 11, 12, 16, 20, 23, 24, 26, 30, 31, 36, 40, 49}
theorem cut52 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support52, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 495, OmissionResidual.support 472, OmissionResidual.support 468] ![OmissionResidual.demand 495, OmissionResidual.demand 472, OmissionResidual.demand 468] ![1, 1, 1]
    support52 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 495) (Fin.cases (hrows 472) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support53 : Finset (Fin 154) := {29, 37, 38, 41, 47, 51, 52, 57, 58, 63, 69, 73, 84, 93, 94}
theorem cut53 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support53, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 631, OmissionResidual.support 630] ![OmissionResidual.demand 678, OmissionResidual.demand 631, OmissionResidual.demand 630] ![1, 1, 1]
    support53 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 631) (Fin.cases (hrows 630) (fun i => Fin.elim0 i))))
def support54 : Finset (Fin 154) := {68, 89, 91, 99, 108, 116, 124, 133, 138, 139, 142, 143, 146, 148, 150, 153}
theorem cut54 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support54, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1164, OmissionResidual.support 1061, OmissionResidual.support 1060] ![OmissionResidual.demand 1164, OmissionResidual.demand 1061, OmissionResidual.demand 1060] ![1, 1, 1]
    support54 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1164) (Fin.cases (hrows 1061) (Fin.cases (hrows 1060) (fun i => Fin.elim0 i))))
def support55 : Finset (Fin 154) := {5, 8, 12, 13, 25, 26, 29, 33, 41, 45, 47, 55, 60, 66, 75}
theorem cut55 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support55, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 35, OmissionResidual.support 861, OmissionResidual.support 856] ![OmissionResidual.demand 35, OmissionResidual.demand 861, OmissionResidual.demand 856] ![1, 1, 1]
    support55 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 35) (Fin.cases (hrows 861) (Fin.cases (hrows 856) (fun i => Fin.elim0 i))))
def support56 : Finset (Fin 154) := {5, 8, 10, 12, 14, 21, 25, 26, 29, 33, 41, 45, 47, 55, 60, 66, 75}
theorem cut56 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support56, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 70, OmissionResidual.support 861, OmissionResidual.support 856] ![OmissionResidual.demand 70, OmissionResidual.demand 861, OmissionResidual.demand 856] ![1, 1, 1]
    support56 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 70) (Fin.cases (hrows 861) (Fin.cases (hrows 856) (fun i => Fin.elim0 i))))
def support57 : Finset (Fin 154) := {8, 12, 14, 20, 23, 31, 33, 35, 40, 46, 55, 57, 59, 66, 70, 85}
theorem cut57 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support57, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 862, OmissionResidual.support 496, OmissionResidual.support 876] ![OmissionResidual.demand 862, OmissionResidual.demand 496, OmissionResidual.demand 876] ![1, 1, 1]
    support57 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 862) (Fin.cases (hrows 496) (Fin.cases (hrows 876) (fun i => Fin.elim0 i))))
def support58 : Finset (Fin 154) := {21, 27, 31, 38, 46, 47, 51, 52, 57, 63, 69, 73, 82, 84, 93, 103}
theorem cut58 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support58, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 680, OmissionResidual.support 585, OmissionResidual.support 583] ![OmissionResidual.demand 680, OmissionResidual.demand 585, OmissionResidual.demand 583] ![1, 1, 1]
    support58 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 680) (Fin.cases (hrows 585) (Fin.cases (hrows 583) (fun i => Fin.elim0 i))))
def support59 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 84, 102, 103, 112}
theorem cut59 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support59, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 680, OmissionResidual.support 730, OmissionResidual.support 679] ![OmissionResidual.demand 680, OmissionResidual.demand 730, OmissionResidual.demand 679] ![1, 1, 1]
    support59 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 680) (Fin.cases (hrows 730) (Fin.cases (hrows 679) (fun i => Fin.elim0 i))))
def support60 : Finset (Fin 154) := {90, 99, 107, 108, 111, 115, 122, 123, 126, 129, 130, 135, 139, 143, 147, 149}
theorem cut60 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support60, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1141, OmissionResidual.support 1111, OmissionResidual.support 1114] ![OmissionResidual.demand 1141, OmissionResidual.demand 1111, OmissionResidual.demand 1114] ![1, 1, 1]
    support60 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1141) (Fin.cases (hrows 1111) (Fin.cases (hrows 1114) (fun i => Fin.elim0 i))))
def support61 : Finset (Fin 154) := {39, 53, 59, 60, 70, 75, 77, 81, 82, 87, 93, 96, 97, 105}
theorem cut61 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support61, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 691, OmissionResidual.support 690, OmissionResidual.support 778] ![OmissionResidual.demand 691, OmissionResidual.demand 690, OmissionResidual.demand 778] ![1, 1, 1]
    support61 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 691) (Fin.cases (hrows 690) (Fin.cases (hrows 778) (fun i => Fin.elim0 i))))
def support62 : Finset (Fin 154) := {79, 89, 101, 107, 115, 123, 130, 133, 138, 139, 142, 146, 147, 148, 150, 152}
theorem cut62 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support62, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1090, OmissionResidual.support 1163, OmissionResidual.support 1089] ![OmissionResidual.demand 1090, OmissionResidual.demand 1163, OmissionResidual.demand 1089] ![1, 1, 1]
    support62 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1090) (Fin.cases (hrows 1163) (Fin.cases (hrows 1089) (fun i => Fin.elim0 i))))
def support63 : Finset (Fin 154) := {109, 116, 123, 127, 129, 133, 134, 138, 139, 140, 142, 146, 148, 150, 151, 152}
theorem cut63 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support63, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1146, OmissionResidual.support 1144, OmissionResidual.support 1163] ![OmissionResidual.demand 1146, OmissionResidual.demand 1144, OmissionResidual.demand 1163] ![1, 1, 1]
    support63 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1146) (Fin.cases (hrows 1144) (Fin.cases (hrows 1163) (fun i => Fin.elim0 i))))
def support64 : Finset (Fin 154) := {100, 108, 115, 119, 122, 133, 134, 138, 139, 140, 142, 146, 148, 150, 151, 152}
theorem cut64 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support64, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1132, OmissionResidual.support 1133, OmissionResidual.support 1163] ![OmissionResidual.demand 1132, OmissionResidual.demand 1133, OmissionResidual.demand 1163] ![1, 1, 1]
    support64 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1132) (Fin.cases (hrows 1133) (Fin.cases (hrows 1163) (fun i => Fin.elim0 i))))
def support65 : Finset (Fin 154) := {100, 108, 115, 119, 122, 129, 133, 135, 138, 139, 142, 146, 148, 149, 150, 152}
theorem cut65 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support65, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1131, OmissionResidual.support 1130, OmissionResidual.support 1163] ![OmissionResidual.demand 1131, OmissionResidual.demand 1130, OmissionResidual.demand 1163] ![1, 1, 1]
    support65 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1131) (Fin.cases (hrows 1130) (Fin.cases (hrows 1163) (fun i => Fin.elim0 i))))
def support66 : Finset (Fin 154) := {0, 4, 7, 8, 11, 12, 16, 20, 23, 26, 30, 33, 36, 44, 49, 54, 64}
theorem cut66 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support66, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 466, OmissionResidual.support 851, OmissionResidual.support 859] ![OmissionResidual.demand 466, OmissionResidual.demand 851, OmissionResidual.demand 859] ![1, 1, 1]
    support66 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 466) (Fin.cases (hrows 851) (Fin.cases (hrows 859) (fun i => Fin.elim0 i))))
def support67 : Finset (Fin 154) := {1, 4, 7, 8, 11, 12, 16, 20, 23, 26, 30, 33, 36, 44, 49, 54, 64}
theorem cut67 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support67, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 468, OmissionResidual.support 851, OmissionResidual.support 859] ![OmissionResidual.demand 468, OmissionResidual.demand 851, OmissionResidual.demand 859] ![1, 1, 1]
    support67 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 468) (Fin.cases (hrows 851) (Fin.cases (hrows 859) (fun i => Fin.elim0 i))))
def support68 : Finset (Fin 154) := {2, 4, 13, 21, 25, 31, 33, 34, 43, 44, 53, 54, 64, 66, 74, 75, 78, 85, 87, 90, 96, 99, 104, 107, 111, 113, 118, 121, 122, 125, 129, 135, 136, 141, 146, 149}
theorem cut68 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    7 ≤ ∑ i ∈ support68, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1173, OmissionResidual.support 1171, OmissionResidual.support 10] ![OmissionResidual.demand 1173, OmissionResidual.demand 1171, OmissionResidual.demand 10] ![1, 1, 1]
    support68 2 7 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1173) (Fin.cases (hrows 1171) (Fin.cases (hrows 10) (fun i => Fin.elim0 i))))
def support69 : Finset (Fin 154) := {5, 8, 13, 21, 25, 31, 33, 34, 43, 44, 53, 54, 64, 66, 74, 75, 78, 85, 87, 90, 96, 99, 104, 107, 111, 113, 118, 121, 122, 125, 129, 135, 136, 141, 146, 149}
theorem cut69 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    7 ≤ ∑ i ∈ support69, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1173, OmissionResidual.support 1171, OmissionResidual.support 30] ![OmissionResidual.demand 1173, OmissionResidual.demand 1171, OmissionResidual.demand 30] ![1, 1, 1]
    support69 2 7 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1173) (Fin.cases (hrows 1171) (Fin.cases (hrows 30) (fun i => Fin.elim0 i))))
def support70 : Finset (Fin 154) := {90, 99, 107, 111, 115, 123, 130, 133, 138, 139, 142, 146, 147, 148, 150, 152}
theorem cut70 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support70, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1111, OmissionResidual.support 1163, OmissionResidual.support 1110] ![OmissionResidual.demand 1111, OmissionResidual.demand 1163, OmissionResidual.demand 1110] ![1, 1, 1]
    support70 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1111) (Fin.cases (hrows 1163) (Fin.cases (hrows 1110) (fun i => Fin.elim0 i))))
def support71 : Finset (Fin 154) := {116, 123, 124, 129, 130, 132, 134, 135, 138, 140, 143, 144, 148, 152}
theorem cut71 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support71, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1153, OmissionResidual.support 1159, OmissionResidual.support 1150] ![OmissionResidual.demand 1153, OmissionResidual.demand 1159, OmissionResidual.demand 1150] ![1, 1, 1]
    support71 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1153) (Fin.cases (hrows 1159) (Fin.cases (hrows 1150) (fun i => Fin.elim0 i))))
def support72 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 92, 93, 97, 99, 102, 103, 113, 116, 123}
theorem cut72 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support72, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 816, OmissionResidual.support 784] ![OmissionResidual.demand 779, OmissionResidual.demand 816, OmissionResidual.demand 784] ![1, 1, 1]
    support72 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 816) (Fin.cases (hrows 784) (fun i => Fin.elim0 i))))
def support73 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 92, 93, 99, 103, 106, 112, 116, 121, 123}
theorem cut73 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support73, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 781, OmissionResidual.support 816, OmissionResidual.support 784] ![OmissionResidual.demand 781, OmissionResidual.demand 816, OmissionResidual.demand 784] ![1, 1, 1]
    support73 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 781) (Fin.cases (hrows 816) (Fin.cases (hrows 784) (fun i => Fin.elim0 i))))
def support74 : Finset (Fin 154) := {83, 93, 94, 97, 102, 103, 106, 108, 112, 116, 120, 124, 129, 140}
theorem cut74 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support74, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 842, OmissionResidual.support 832, OmissionResidual.support 835] ![OmissionResidual.demand 842, OmissionResidual.demand 832, OmissionResidual.demand 835] ![1, 1, 1]
    support74 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 842) (Fin.cases (hrows 832) (Fin.cases (hrows 835) (fun i => Fin.elim0 i))))
def support75 : Finset (Fin 154) := {8, 12, 20, 23, 31, 35, 40, 43, 46, 57, 59, 65, 70, 75, 85}
theorem cut75 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support75, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 496, OmissionResidual.support 527, OmissionResidual.support 576] ![OmissionResidual.demand 496, OmissionResidual.demand 527, OmissionResidual.demand 576] ![1, 1, 1]
    support75 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 496) (Fin.cases (hrows 527) (Fin.cases (hrows 576) (fun i => Fin.elim0 i))))
#print axioms cut75
def support76 : Finset (Fin 154) := {8, 12, 21, 23, 27, 31, 35, 40, 41, 46, 51, 57, 59, 70}
theorem cut76 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support76, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 496, OmissionResidual.support 498, OmissionResidual.support 579] ![OmissionResidual.demand 496, OmissionResidual.demand 498, OmissionResidual.demand 579] ![1, 1, 1]
    support76 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 496) (Fin.cases (hrows 498) (Fin.cases (hrows 579) (fun i => Fin.elim0 i))))
def support77 : Finset (Fin 154) := {29, 37, 38, 41, 47, 51, 52, 57, 58, 63, 69, 73, 84, 93, 94, 103}
theorem cut77 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support77, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 631, OmissionResidual.support 632] ![OmissionResidual.demand 678, OmissionResidual.demand 631, OmissionResidual.demand 632] ![1, 1, 1]
    support77 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 631) (Fin.cases (hrows 632) (fun i => Fin.elim0 i))))
def support78 : Finset (Fin 154) := {21, 27, 28, 31, 36, 40, 41, 46, 51, 52, 58, 61, 69, 71, 73, 81, 93}
theorem cut78 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support78, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 585, OmissionResidual.support 580, OmissionResidual.support 622] ![OmissionResidual.demand 585, OmissionResidual.demand 580, OmissionResidual.demand 622] ![1, 1, 1]
    support78 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 585) (Fin.cases (hrows 580) (Fin.cases (hrows 622) (fun i => Fin.elim0 i))))
def support79 : Finset (Fin 154) := {60, 70, 72, 75, 82, 87, 92, 97, 99, 102, 112, 113, 116, 129}
theorem cut79 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support79, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 817, OmissionResidual.support 785] ![OmissionResidual.demand 779, OmissionResidual.demand 817, OmissionResidual.demand 785] ![1, 1, 1]
    support79 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 817) (Fin.cases (hrows 785) (fun i => Fin.elim0 i))))
def support80 : Finset (Fin 154) := {21, 27, 28, 31, 36, 40, 46, 47, 52, 63, 69, 72, 73, 93}
theorem cut80 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support80, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 585, OmissionResidual.support 624, OmissionResidual.support 582] ![OmissionResidual.demand 585, OmissionResidual.demand 624, OmissionResidual.demand 582] ![1, 1, 1]
    support80 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 585) (Fin.cases (hrows 624) (Fin.cases (hrows 582) (fun i => Fin.elim0 i))))
def support81 : Finset (Fin 154) := {13, 18, 19, 26, 31, 35, 40, 41, 47, 51, 60, 61, 69, 81}
theorem cut81 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support81, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 571, OmissionResidual.support 528, OmissionResidual.support 531] ![OmissionResidual.demand 571, OmissionResidual.demand 528, OmissionResidual.demand 531] ![1, 1, 1]
    support81 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 571) (Fin.cases (hrows 528) (Fin.cases (hrows 531) (fun i => Fin.elim0 i))))
def support82 : Finset (Fin 154) := {68, 89, 91, 99, 108, 116, 124, 133, 138, 139, 142, 143, 146, 148, 150, 152}
theorem cut82 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support82, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1061, OmissionResidual.support 1163, OmissionResidual.support 1060] ![OmissionResidual.demand 1061, OmissionResidual.demand 1163, OmissionResidual.demand 1060] ![1, 1, 1]
    support82 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1061) (Fin.cases (hrows 1163) (Fin.cases (hrows 1060) (fun i => Fin.elim0 i))))
def support83 : Finset (Fin 154) := {29, 37, 41, 47, 52, 57, 58, 69, 75, 84, 87, 94, 103, 106, 114}
theorem cut83 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support83, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 631, OmissionResidual.support 632, OmissionResidual.support 728] ![OmissionResidual.demand 631, OmissionResidual.demand 632, OmissionResidual.demand 728] ![1, 1, 1]
    support83 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 631) (Fin.cases (hrows 632) (Fin.cases (hrows 728) (fun i => Fin.elim0 i))))
def support84 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 92, 99, 102, 103, 106, 112, 114, 116, 129}
theorem cut84 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support84, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 817, OmissionResidual.support 785] ![OmissionResidual.demand 780, OmissionResidual.demand 817, OmissionResidual.demand 785] ![1, 1, 1]
    support84 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 817) (Fin.cases (hrows 785) (fun i => Fin.elim0 i))))
def support85 : Finset (Fin 154) := {72, 82, 87, 93, 94, 99, 102, 103, 106, 112, 116, 120, 123, 124, 135, 140}
theorem cut85 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support85, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 842, OmissionResidual.support 816, OmissionResidual.support 819] ![OmissionResidual.demand 842, OmissionResidual.demand 816, OmissionResidual.demand 819] ![1, 1, 1]
    support85 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 842) (Fin.cases (hrows 816) (Fin.cases (hrows 819) (fun i => Fin.elim0 i))))
def support86 : Finset (Fin 154) := {84, 94, 98, 103, 109, 112, 117, 120, 124, 130, 135, 138, 140, 143, 144, 153}
theorem cut86 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support86, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 971, OmissionResidual.support 1160, OmissionResidual.support 972] ![OmissionResidual.demand 971, OmissionResidual.demand 1160, OmissionResidual.demand 972] ![1, 1, 1]
    support86 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 971) (Fin.cases (hrows 1160) (Fin.cases (hrows 972) (fun i => Fin.elim0 i))))
def support87 : Finset (Fin 154) := {109, 116, 123, 124, 127, 129, 130, 133, 134, 135, 138, 140, 143, 144, 148, 150, 153}
theorem cut87 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support87, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1144, OmissionResidual.support 1145, OmissionResidual.support 1160] ![OmissionResidual.demand 1144, OmissionResidual.demand 1145, OmissionResidual.demand 1160] ![1, 1, 1]
    support87 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1144) (Fin.cases (hrows 1145) (Fin.cases (hrows 1160) (fun i => Fin.elim0 i))))
def support88 : Finset (Fin 154) := {116, 123, 124, 129, 130, 132, 134, 135, 138, 140, 143, 144, 150, 151, 153}
theorem cut88 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support88, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1152, OmissionResidual.support 1160, OmissionResidual.support 1151] ![OmissionResidual.demand 1152, OmissionResidual.demand 1160, OmissionResidual.demand 1151] ![1, 1, 1]
    support88 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1152) (Fin.cases (hrows 1160) (Fin.cases (hrows 1151) (fun i => Fin.elim0 i))))
def support89 : Finset (Fin 154) := {116, 123, 124, 129, 130, 132, 134, 135, 138, 140, 143, 144, 148, 152, 153}
theorem cut89 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support89, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1153, OmissionResidual.support 1160, OmissionResidual.support 1150] ![OmissionResidual.demand 1153, OmissionResidual.demand 1160, OmissionResidual.demand 1150] ![1, 1, 1]
    support89 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1153) (Fin.cases (hrows 1160) (Fin.cases (hrows 1150) (fun i => Fin.elim0 i))))
def support90 : Finset (Fin 154) := {98, 106, 114, 121, 124, 127, 128, 130, 133, 135, 138, 140, 143, 144, 148, 150, 153}
theorem cut90 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support90, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1160, OmissionResidual.support 1122, OmissionResidual.support 1123] ![OmissionResidual.demand 1160, OmissionResidual.demand 1122, OmissionResidual.demand 1123] ![1, 1, 1]
    support90 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1160) (Fin.cases (hrows 1122) (Fin.cases (hrows 1123) (fun i => Fin.elim0 i))))
def support91 : Finset (Fin 154) := {20, 39, 43, 46, 53, 57, 59, 65, 70, 75, 77, 82, 85, 87, 96}
theorem cut91 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support91, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 576, OmissionResidual.support 577, OmissionResidual.support 690] ![OmissionResidual.demand 576, OmissionResidual.demand 577, OmissionResidual.demand 690] ![1, 1, 1]
    support91 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 576) (Fin.cases (hrows 577) (Fin.cases (hrows 690) (fun i => Fin.elim0 i))))
def support92 : Finset (Fin 154) := {1, 5, 7, 11, 12, 16, 18, 20, 23, 24, 27, 30, 31, 39}
theorem cut92 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support92, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 468, OmissionResidual.support 469, OmissionResidual.support 482] ![OmissionResidual.demand 468, OmissionResidual.demand 469, OmissionResidual.demand 482] ![1, 1, 1]
    support92 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 468) (Fin.cases (hrows 469) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support93 : Finset (Fin 154) := {0, 1, 5, 7, 11, 12, 16, 18, 20, 23, 24, 27, 30, 31, 39}
theorem cut93 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support93, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 466, OmissionResidual.support 469, OmissionResidual.support 482] ![OmissionResidual.demand 466, OmissionResidual.demand 469, OmissionResidual.demand 482] ![1, 1, 1]
    support93 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 466) (Fin.cases (hrows 469) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support94 : Finset (Fin 154) := {0, 2, 3, 7, 11, 12, 16, 18, 20, 23, 24, 27, 30, 31, 39}
theorem cut94 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support94, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 466, OmissionResidual.support 474, OmissionResidual.support 471] ![OmissionResidual.demand 466, OmissionResidual.demand 474, OmissionResidual.demand 471] ![1, 1, 1]
    support94 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 466) (Fin.cases (hrows 474) (Fin.cases (hrows 471) (fun i => Fin.elim0 i))))
def support95 : Finset (Fin 154) := {1, 2, 3, 7, 11, 12, 16, 18, 20, 23, 24, 27, 30, 31, 39}
theorem cut95 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support95, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 468, OmissionResidual.support 474, OmissionResidual.support 471] ![OmissionResidual.demand 468, OmissionResidual.demand 474, OmissionResidual.demand 471] ![1, 1, 1]
    support95 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 468) (Fin.cases (hrows 474) (Fin.cases (hrows 471) (fun i => Fin.elim0 i))))
def support96 : Finset (Fin 154) := {13, 18, 19, 26, 31, 35, 40, 41, 51, 57, 58, 61, 69, 70, 71, 81}
theorem cut96 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support96, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 530, OmissionResidual.support 529, OmissionResidual.support 571] ![OmissionResidual.demand 530, OmissionResidual.demand 529, OmissionResidual.demand 571] ![1, 1, 1]
    support96 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 530) (Fin.cases (hrows 529) (Fin.cases (hrows 571) (fun i => Fin.elim0 i))))
def support97 : Finset (Fin 154) := {84, 88, 94, 97, 103, 105, 112, 113, 119, 120, 121, 127, 128, 133, 134, 135, 145, 146, 150}
theorem cut97 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support97, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1103, OmissionResidual.support 1094, OmissionResidual.support 1102] ![OmissionResidual.demand 1103, OmissionResidual.demand 1094, OmissionResidual.demand 1102] ![1, 1, 1]
    support97 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1103) (Fin.cases (hrows 1094) (Fin.cases (hrows 1102) (fun i => Fin.elim0 i))))
def support98 : Finset (Fin 154) := {3, 8, 11, 12, 13, 18, 23, 24, 27, 31, 35, 39, 41, 51, 57, 70}
theorem cut98 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support98, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 529, OmissionResidual.support 498, OmissionResidual.support 474] ![OmissionResidual.demand 529, OmissionResidual.demand 498, OmissionResidual.demand 474] ![1, 1, 1]
    support98 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 529) (Fin.cases (hrows 498) (Fin.cases (hrows 474) (fun i => Fin.elim0 i))))
def support99 : Finset (Fin 154) := {78, 84, 87, 94, 96, 103, 111, 112, 113, 120, 121, 127, 129, 133, 135, 141, 146, 150}
theorem cut99 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support99, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1094, OmissionResidual.support 1082, OmissionResidual.support 1081] ![OmissionResidual.demand 1094, OmissionResidual.demand 1082, OmissionResidual.demand 1081] ![1, 1, 1]
    support99 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1094) (Fin.cases (hrows 1082) (Fin.cases (hrows 1081) (fun i => Fin.elim0 i))))
def support100 : Finset (Fin 154) := {39, 53, 59, 60, 70, 75, 77, 81, 82, 87, 92, 93, 96, 97, 102, 105, 113}
theorem cut100 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support100, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 691, OmissionResidual.support 690] ![OmissionResidual.demand 779, OmissionResidual.demand 691, OmissionResidual.demand 690] ![1, 1, 1]
    support100 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 691) (Fin.cases (hrows 690) (fun i => Fin.elim0 i))))
#print axioms cut100
def support101 : Finset (Fin 154) := {8, 12, 14, 20, 23, 26, 31, 33, 36, 40, 47, 49, 55, 60, 66, 75}
theorem cut101 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support101, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 875, OmissionResidual.support 495, OmissionResidual.support 861] ![OmissionResidual.demand 875, OmissionResidual.demand 495, OmissionResidual.demand 861] ![1, 1, 1]
    support101 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 875) (Fin.cases (hrows 495) (Fin.cases (hrows 861) (fun i => Fin.elim0 i))))
def support102 : Finset (Fin 154) := {5, 8, 12, 14, 16, 20, 24, 26, 33, 36, 40, 47, 49, 55, 60, 66, 75}
theorem cut102 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support102, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 875, OmissionResidual.support 483, OmissionResidual.support 861] ![OmissionResidual.demand 875, OmissionResidual.demand 483, OmissionResidual.demand 861] ![1, 1, 1]
    support102 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 875) (Fin.cases (hrows 483) (Fin.cases (hrows 861) (fun i => Fin.elim0 i))))
def support103 : Finset (Fin 154) := {5, 8, 10, 12, 20, 23, 25, 26, 31, 36, 40, 45, 47, 49, 60, 66, 75}
theorem cut103 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support103, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 495, OmissionResidual.support 866, OmissionResidual.support 856] ![OmissionResidual.demand 495, OmissionResidual.demand 866, OmissionResidual.demand 856] ![1, 1, 1]
    support103 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 495) (Fin.cases (hrows 866) (Fin.cases (hrows 856) (fun i => Fin.elim0 i))))
def support104 : Finset (Fin 154) := {5, 8, 12, 14, 16, 20, 23, 24, 26, 36, 40, 41, 47, 49, 51, 60}
theorem cut104 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support104, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 539, OmissionResidual.support 483, OmissionResidual.support 497] ![OmissionResidual.demand 539, OmissionResidual.demand 483, OmissionResidual.demand 497] ![1, 1, 1]
    support104 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 539) (Fin.cases (hrows 483) (Fin.cases (hrows 497) (fun i => Fin.elim0 i))))
def support105 : Finset (Fin 154) := {5, 10, 12, 16, 20, 24, 25, 26, 36, 40, 45, 47, 49, 60, 66, 75}
theorem cut105 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support105, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 866, OmissionResidual.support 483, OmissionResidual.support 856] ![OmissionResidual.demand 866, OmissionResidual.demand 483, OmissionResidual.demand 856] ![1, 1, 1]
    support105 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 866) (Fin.cases (hrows 483) (Fin.cases (hrows 856) (fun i => Fin.elim0 i))))
def support106 : Finset (Fin 154) := {83, 93, 94, 97, 102, 103, 106, 108, 112, 116, 120, 124, 134, 135, 144}
theorem cut106 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support106, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 833, OmissionResidual.support 834, OmissionResidual.support 843] ![OmissionResidual.demand 833, OmissionResidual.demand 834, OmissionResidual.demand 843] ![1, 1, 1]
    support106 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 833) (Fin.cases (hrows 834) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
def support107 : Finset (Fin 154) := {84, 88, 94, 97, 103, 105, 112, 113, 119, 120, 127, 128, 133, 134, 140, 145, 148, 150}
theorem cut107 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support107, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1103, OmissionResidual.support 1094, OmissionResidual.support 1104] ![OmissionResidual.demand 1103, OmissionResidual.demand 1094, OmissionResidual.demand 1104] ![1, 1, 1]
    support107 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1103) (Fin.cases (hrows 1094) (Fin.cases (hrows 1104) (fun i => Fin.elim0 i))))
def support108 : Finset (Fin 154) := {84, 88, 94, 97, 103, 105, 112, 113, 119, 120, 127, 128, 133, 134, 140, 145, 148}
theorem cut108 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support108, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1103, OmissionResidual.support 1104, OmissionResidual.support 1093] ![OmissionResidual.demand 1103, OmissionResidual.demand 1104, OmissionResidual.demand 1093] ![1, 1, 1]
    support108 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1103) (Fin.cases (hrows 1104) (Fin.cases (hrows 1093) (fun i => Fin.elim0 i))))
def support109 : Finset (Fin 154) := {5, 8, 12, 13, 16, 18, 23, 24, 27, 31, 35, 39, 41, 51, 57, 70}
theorem cut109 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support109, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 529, OmissionResidual.support 498, OmissionResidual.support 482] ![OmissionResidual.demand 529, OmissionResidual.demand 498, OmissionResidual.demand 482] ![1, 1, 1]
    support109 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 529) (Fin.cases (hrows 498) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support110 : Finset (Fin 154) := {90, 99, 107, 111, 122, 129, 133, 135, 138, 139, 142, 146, 148, 149, 150, 153}
theorem cut110 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support110, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1164, OmissionResidual.support 1114, OmissionResidual.support 1113] ![OmissionResidual.demand 1164, OmissionResidual.demand 1114, OmissionResidual.demand 1113] ![1, 1, 1]
    support110 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1164) (Fin.cases (hrows 1114) (Fin.cases (hrows 1113) (fun i => Fin.elim0 i))))
def support111 : Finset (Fin 154) := {72, 82, 87, 93, 94, 99, 102, 103, 106, 112, 116, 120, 124, 129, 130, 140}
theorem cut111 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support111, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 818, OmissionResidual.support 842, OmissionResidual.support 817] ![OmissionResidual.demand 818, OmissionResidual.demand 842, OmissionResidual.demand 817] ![1, 1, 1]
    support111 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 818) (Fin.cases (hrows 842) (Fin.cases (hrows 817) (fun i => Fin.elim0 i))))
def support112 : Finset (Fin 154) := {8, 12, 21, 23, 26, 27, 31, 36, 40, 41, 47, 49, 51, 60}
theorem cut112 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support112, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 495, OmissionResidual.support 578, OmissionResidual.support 497] ![OmissionResidual.demand 495, OmissionResidual.demand 578, OmissionResidual.demand 497] ![1, 1, 1]
    support112 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 495) (Fin.cases (hrows 578) (Fin.cases (hrows 497) (fun i => Fin.elim0 i))))
def support113 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 92, 93, 99, 102, 103, 106, 108, 114, 116, 122, 123}
theorem cut113 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support113, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 816, OmissionResidual.support 783] ![OmissionResidual.demand 780, OmissionResidual.demand 816, OmissionResidual.demand 783] ![1, 1, 1]
    support113 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 816) (Fin.cases (hrows 783) (fun i => Fin.elim0 i))))
def support114 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 92, 93, 99, 102, 103, 106, 108, 114, 122, 124, 130}
theorem cut114 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support114, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 818, OmissionResidual.support 783] ![OmissionResidual.demand 780, OmissionResidual.demand 818, OmissionResidual.demand 783] ![1, 1, 1]
    support114 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 818) (Fin.cases (hrows 783) (fun i => Fin.elim0 i))))
def support115 : Finset (Fin 154) := {21, 27, 28, 31, 36, 40, 41, 46, 58, 61, 63, 69, 71, 73, 81, 93}
theorem cut115 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support115, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 580, OmissionResidual.support 624, OmissionResidual.support 581] ![OmissionResidual.demand 580, OmissionResidual.demand 624, OmissionResidual.demand 581] ![1, 1, 1]
    support115 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 580) (Fin.cases (hrows 624) (Fin.cases (hrows 581) (fun i => Fin.elim0 i))))
def support116 : Finset (Fin 154) := {3, 5, 10, 11, 12, 18, 20, 24, 25, 27, 31, 37, 39, 45, 50, 55, 65}
theorem cut116 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support116, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 865, OmissionResidual.support 474, OmissionResidual.support 855] ![OmissionResidual.demand 865, OmissionResidual.demand 474, OmissionResidual.demand 855] ![1, 1, 1]
    support116 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 865) (Fin.cases (hrows 474) (Fin.cases (hrows 855) (fun i => Fin.elim0 i))))
def support117 : Finset (Fin 154) := {3, 6, 11, 12, 17, 18, 20, 24, 27, 31, 37, 39, 45, 50, 55, 65}
theorem cut117 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support117, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 857, OmissionResidual.support 474, OmissionResidual.support 850] ![OmissionResidual.demand 857, OmissionResidual.demand 474, OmissionResidual.demand 850] ![1, 1, 1]
    support117 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 857) (Fin.cases (hrows 474) (Fin.cases (hrows 850) (fun i => Fin.elim0 i))))
def support118 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 99, 102, 103, 106, 112, 114, 116, 123, 129}
theorem cut118 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support118, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 817, OmissionResidual.support 784] ![OmissionResidual.demand 780, OmissionResidual.demand 817, OmissionResidual.demand 784] ![1, 1, 1]
    support118 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 817) (Fin.cases (hrows 784) (fun i => Fin.elim0 i))))
def support119 : Finset (Fin 154) := {5, 10, 12, 16, 18, 20, 24, 25, 27, 31, 37, 39, 45, 50, 55, 65}
theorem cut119 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support119, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 865, OmissionResidual.support 482, OmissionResidual.support 855] ![OmissionResidual.demand 865, OmissionResidual.demand 482, OmissionResidual.demand 855] ![1, 1, 1]
    support119 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 865) (Fin.cases (hrows 482) (Fin.cases (hrows 855) (fun i => Fin.elim0 i))))
def support120 : Finset (Fin 154) := {3, 5, 6, 12, 16, 17, 18, 20, 24, 27, 31, 37, 39, 45, 50, 55, 65}
theorem cut120 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support120, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 857, OmissionResidual.support 482, OmissionResidual.support 850] ![OmissionResidual.demand 857, OmissionResidual.demand 482, OmissionResidual.demand 850] ![1, 1, 1]
    support120 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 857) (Fin.cases (hrows 482) (Fin.cases (hrows 850) (fun i => Fin.elim0 i))))
def support121 : Finset (Fin 154) := {71, 81, 83, 86, 92, 93, 97, 102, 106, 108, 112, 116, 120, 121, 134}
theorem cut121 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support121, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 815, OmissionResidual.support 833, OmissionResidual.support 812] ![OmissionResidual.demand 815, OmissionResidual.demand 833, OmissionResidual.demand 812] ![1, 1, 1]
    support121 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 815) (Fin.cases (hrows 833) (Fin.cases (hrows 812) (fun i => Fin.elim0 i))))
def support122 : Finset (Fin 154) := {41, 50, 55, 60, 70, 71, 75, 79, 81, 94, 99, 103, 109, 116, 123}
theorem cut122 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support122, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 941, OmissionResidual.support 942, OmissionResidual.support 784] ![OmissionResidual.demand 941, OmissionResidual.demand 942, OmissionResidual.demand 784] ![1, 1, 1]
    support122 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 941) (Fin.cases (hrows 942) (Fin.cases (hrows 784) (fun i => Fin.elim0 i))))
def support123 : Finset (Fin 154) := {28, 36, 40, 46, 48, 51, 58, 61, 63, 69, 73, 80, 81, 84, 102, 112}
theorem cut123 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support123, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 730, OmissionResidual.support 625, OmissionResidual.support 622] ![OmissionResidual.demand 730, OmissionResidual.demand 625, OmissionResidual.demand 622] ![1, 1, 1]
    support123 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 730) (Fin.cases (hrows 625) (Fin.cases (hrows 622) (fun i => Fin.elim0 i))))
def support124 : Finset (Fin 154) := {29, 37, 41, 47, 52, 57, 58, 69, 73, 75, 84, 87, 93, 94, 103, 106, 114}
theorem cut124 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support124, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 631, OmissionResidual.support 630, OmissionResidual.support 728] ![OmissionResidual.demand 631, OmissionResidual.demand 630, OmissionResidual.demand 728] ![1, 1, 1]
    support124 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 631) (Fin.cases (hrows 630) (Fin.cases (hrows 728) (fun i => Fin.elim0 i))))
def support125 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 84, 93, 112, 120}
theorem cut125 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support125, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 681, OmissionResidual.support 731] ![OmissionResidual.demand 678, OmissionResidual.demand 681, OmissionResidual.demand 731] ![1, 1, 1]
    support125 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 681) (Fin.cases (hrows 731) (fun i => Fin.elim0 i))))
#print axioms cut125
def support126 : Finset (Fin 154) := {0, 3, 4, 5, 8, 12, 14, 17, 18, 23, 25, 33, 37, 45, 50, 55, 65}
theorem cut126 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support126, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 0, OmissionResidual.support 855, OmissionResidual.support 850] ![OmissionResidual.demand 0, OmissionResidual.demand 855, OmissionResidual.demand 850] ![1, 1, 1]
    support126 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 855) (Fin.cases (hrows 850) (fun i => Fin.elim0 i))))
def support127 : Finset (Fin 154) := {1, 3, 4, 5, 8, 12, 14, 17, 18, 23, 25, 33, 37, 45, 50, 55, 65}
theorem cut127 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support127, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 4, OmissionResidual.support 855, OmissionResidual.support 850] ![OmissionResidual.demand 4, OmissionResidual.demand 855, OmissionResidual.demand 850] ![1, 1, 1]
    support127 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 4) (Fin.cases (hrows 855) (Fin.cases (hrows 850) (fun i => Fin.elim0 i))))
def support128 : Finset (Fin 154) := {84, 88, 94, 97, 103, 105, 112, 113, 119, 120, 121, 127, 129, 133, 135, 141, 146, 150}
theorem cut128 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support128, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1094, OmissionResidual.support 1102, OmissionResidual.support 1101] ![OmissionResidual.demand 1094, OmissionResidual.demand 1102, OmissionResidual.demand 1101] ![1, 1, 1]
    support128 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1094) (Fin.cases (hrows 1102) (Fin.cases (hrows 1101) (fun i => Fin.elim0 i))))
def support129 : Finset (Fin 154) := {84, 94, 98, 103, 109, 112, 117, 120, 124, 130, 135, 138, 140, 143, 144, 152}
theorem cut129 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support129, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 971, OmissionResidual.support 1159, OmissionResidual.support 972] ![OmissionResidual.demand 971, OmissionResidual.demand 1159, OmissionResidual.demand 972] ![1, 1, 1]
    support129 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 971) (Fin.cases (hrows 1159) (Fin.cases (hrows 972) (fun i => Fin.elim0 i))))
def support130 : Finset (Fin 154) := {116, 123, 124, 129, 130, 132, 134, 135, 138, 140, 143, 144, 150, 151, 152}
theorem cut130 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support130, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1152, OmissionResidual.support 1159, OmissionResidual.support 1151] ![OmissionResidual.demand 1152, OmissionResidual.demand 1159, OmissionResidual.demand 1151] ![1, 1, 1]
    support130 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1152) (Fin.cases (hrows 1159) (Fin.cases (hrows 1151) (fun i => Fin.elim0 i))))
def support131 : Finset (Fin 154) := {109, 116, 123, 124, 127, 129, 130, 134, 135, 138, 139, 140, 143, 144, 151, 152}
theorem cut131 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support131, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1146, OmissionResidual.support 1147, OmissionResidual.support 1159] ![OmissionResidual.demand 1146, OmissionResidual.demand 1147, OmissionResidual.demand 1159] ![1, 1, 1]
    support131 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1146) (Fin.cases (hrows 1147) (Fin.cases (hrows 1159) (fun i => Fin.elim0 i))))
def support132 : Finset (Fin 154) := {109, 116, 123, 124, 127, 129, 130, 133, 134, 135, 138, 140, 143, 144, 148, 150, 152}
theorem cut132 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support132, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1144, OmissionResidual.support 1145, OmissionResidual.support 1159] ![OmissionResidual.demand 1144, OmissionResidual.demand 1145, OmissionResidual.demand 1159] ![1, 1, 1]
    support132 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1144) (Fin.cases (hrows 1145) (Fin.cases (hrows 1159) (fun i => Fin.elim0 i))))
def support133 : Finset (Fin 154) := {98, 106, 114, 121, 124, 127, 128, 130, 133, 135, 138, 140, 143, 144, 148, 150, 152}
theorem cut133 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support133, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1122, OmissionResidual.support 1123, OmissionResidual.support 1159] ![OmissionResidual.demand 1122, OmissionResidual.demand 1123, OmissionResidual.demand 1159] ![1, 1, 1]
    support133 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1122) (Fin.cases (hrows 1123) (Fin.cases (hrows 1159) (fun i => Fin.elim0 i))))
def support134 : Finset (Fin 154) := {14, 20, 23, 28, 36, 38, 40, 41, 46, 47, 51, 57, 60, 63, 69, 73, 93}
theorem cut134 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support134, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 539, OmissionResidual.support 624] ![OmissionResidual.demand 678, OmissionResidual.demand 539, OmissionResidual.demand 624] ![1, 1, 1]
    support134 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 539) (Fin.cases (hrows 624) (fun i => Fin.elim0 i))))
def support135 : Finset (Fin 154) := {72, 82, 87, 96, 99, 102, 107, 112, 113, 116, 118, 121, 122, 129, 135, 138, 146}
theorem cut135 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support135, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 817, OmissionResidual.support 1100, OmissionResidual.support 1127] ![OmissionResidual.demand 817, OmissionResidual.demand 1100, OmissionResidual.demand 1127] ![1, 1, 1]
    support135 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 817) (Fin.cases (hrows 1100) (Fin.cases (hrows 1127) (fun i => Fin.elim0 i))))
def support136 : Finset (Fin 154) := {100, 108, 115, 116, 119, 122, 123, 129, 132, 134, 135, 139, 140, 143, 149, 151}
theorem cut136 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support136, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1152, OmissionResidual.support 1131, OmissionResidual.support 1133] ![OmissionResidual.demand 1152, OmissionResidual.demand 1131, OmissionResidual.demand 1133] ![1, 1, 1]
    support136 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1152) (Fin.cases (hrows 1131) (Fin.cases (hrows 1133) (fun i => Fin.elim0 i))))
def support137 : Finset (Fin 154) := {13, 18, 19, 26, 31, 35, 40, 41, 51, 57, 58, 61, 70, 71, 80, 92}
theorem cut137 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support137, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 530, OmissionResidual.support 529, OmissionResidual.support 572] ![OmissionResidual.demand 530, OmissionResidual.demand 529, OmissionResidual.demand 572] ![1, 1, 1]
    support137 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 530) (Fin.cases (hrows 529) (Fin.cases (hrows 572) (fun i => Fin.elim0 i))))
def support138 : Finset (Fin 154) := {21, 27, 31, 39, 41, 46, 51, 53, 57, 59, 70, 77, 82, 87, 96}
theorem cut138 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support138, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 579, OmissionResidual.support 620, OmissionResidual.support 690] ![OmissionResidual.demand 579, OmissionResidual.demand 620, OmissionResidual.demand 690] ![1, 1, 1]
    support138 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 579) (Fin.cases (hrows 620) (Fin.cases (hrows 690) (fun i => Fin.elim0 i))))
def support139 : Finset (Fin 154) := {2, 4, 13, 16, 21, 24, 25, 30, 31, 34, 39, 44, 49, 56, 60, 72, 78, 87}
theorem cut139 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support139, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 903, OmissionResidual.support 10, OmissionResidual.support 884] ![OmissionResidual.demand 903, OmissionResidual.demand 10, OmissionResidual.demand 884] ![1, 1, 1]
    support139 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 903) (Fin.cases (hrows 10) (Fin.cases (hrows 884) (fun i => Fin.elim0 i))))
def support140 : Finset (Fin 154) := {5, 8, 13, 16, 21, 24, 25, 30, 31, 34, 39, 44, 49, 56, 60, 72, 78, 87}
theorem cut140 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support140, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 903, OmissionResidual.support 30, OmissionResidual.support 884] ![OmissionResidual.demand 903, OmissionResidual.demand 30, OmissionResidual.demand 884] ![1, 1, 1]
    support140 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 903) (Fin.cases (hrows 30) (Fin.cases (hrows 884) (fun i => Fin.elim0 i))))
def support141 : Finset (Fin 154) := {99, 107, 108, 115, 118, 122, 123, 126, 129, 130, 135, 138, 143, 146, 147}
theorem cut141 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support141, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1126, OmissionResidual.support 1140, OmissionResidual.support 1127] ![OmissionResidual.demand 1126, OmissionResidual.demand 1140, OmissionResidual.demand 1127] ![1, 1, 1]
    support141 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1126) (Fin.cases (hrows 1140) (Fin.cases (hrows 1127) (fun i => Fin.elim0 i))))
def support142 : Finset (Fin 154) := {3, 8, 11, 12, 13, 18, 23, 24, 26, 27, 31, 39, 41, 47, 51, 60}
theorem cut142 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support142, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 528, OmissionResidual.support 497, OmissionResidual.support 474] ![OmissionResidual.demand 528, OmissionResidual.demand 497, OmissionResidual.demand 474] ![1, 1, 1]
    support142 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 528) (Fin.cases (hrows 497) (Fin.cases (hrows 474) (fun i => Fin.elim0 i))))
def support143 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 92, 93, 99, 103, 106, 112, 114, 116, 123, 129}
theorem cut143 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support143, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 816, OmissionResidual.support 785] ![OmissionResidual.demand 780, OmissionResidual.demand 816, OmissionResidual.demand 785] ![1, 1, 1]
    support143 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 816) (Fin.cases (hrows 785) (fun i => Fin.elim0 i))))
def support144 : Finset (Fin 154) := {20, 43, 46, 57, 60, 65, 70, 75, 77, 82, 85, 87, 92, 96, 97, 102, 113}
theorem cut144 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support144, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 576, OmissionResidual.support 577] ![OmissionResidual.demand 779, OmissionResidual.demand 576, OmissionResidual.demand 577] ![1, 1, 1]
    support144 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 576) (Fin.cases (hrows 577) (fun i => Fin.elim0 i))))
def support145 : Finset (Fin 154) := {20, 43, 46, 57, 60, 65, 70, 75, 77, 81, 82, 85, 87, 96, 103, 106, 114}
theorem cut145 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support145, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 576, OmissionResidual.support 577] ![OmissionResidual.demand 780, OmissionResidual.demand 576, OmissionResidual.demand 577] ![1, 1, 1]
    support145 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 576) (Fin.cases (hrows 577) (fun i => Fin.elim0 i))))
def support146 : Finset (Fin 154) := {20, 43, 46, 57, 60, 65, 70, 75, 77, 82, 85, 87, 92, 96, 106, 112, 121}
theorem cut146 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support146, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 781, OmissionResidual.support 576, OmissionResidual.support 577] ![OmissionResidual.demand 781, OmissionResidual.demand 576, OmissionResidual.demand 577] ![1, 1, 1]
    support146 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 781) (Fin.cases (hrows 576) (Fin.cases (hrows 577) (fun i => Fin.elim0 i))))
def support147 : Finset (Fin 154) := {109, 116, 123, 127, 129, 133, 134, 138, 139, 140, 142, 144, 146, 148, 150, 152}
theorem cut147 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support147, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1144, OmissionResidual.support 1147, OmissionResidual.support 1163] ![OmissionResidual.demand 1144, OmissionResidual.demand 1147, OmissionResidual.demand 1163] ![1, 1, 1]
    support147 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1144) (Fin.cases (hrows 1147) (Fin.cases (hrows 1163) (fun i => Fin.elim0 i))))
def support148 : Finset (Fin 154) := {90, 99, 107, 111, 122, 129, 133, 135, 138, 139, 142, 146, 148, 149, 150, 152}
theorem cut148 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support148, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1163, OmissionResidual.support 1114, OmissionResidual.support 1113] ![OmissionResidual.demand 1163, OmissionResidual.demand 1114, OmissionResidual.demand 1113] ![1, 1, 1]
    support148 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1163) (Fin.cases (hrows 1114) (Fin.cases (hrows 1113) (fun i => Fin.elim0 i))))
def support149 : Finset (Fin 154) := {60, 70, 72, 75, 82, 87, 92, 93, 97, 99, 102, 103, 108, 113, 122, 124, 130}
theorem cut149 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support149, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 818, OmissionResidual.support 783] ![OmissionResidual.demand 779, OmissionResidual.demand 818, OmissionResidual.demand 783] ![1, 1, 1]
    support149 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 818) (Fin.cases (hrows 783) (fun i => Fin.elim0 i))))
def support150 : Finset (Fin 154) := {60, 70, 72, 75, 82, 87, 92, 93, 99, 102, 103, 106, 108, 112, 121, 122, 124, 130}
theorem cut150 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support150, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 781, OmissionResidual.support 818, OmissionResidual.support 783] ![OmissionResidual.demand 781, OmissionResidual.demand 818, OmissionResidual.demand 783] ![1, 1, 1]
    support150 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 781) (Fin.cases (hrows 818) (Fin.cases (hrows 783) (fun i => Fin.elim0 i))))
#print axioms cut150
def support151 : Finset (Fin 154) := {49, 59, 64, 72, 82, 87, 92, 93, 97, 99, 102, 103, 108, 113, 116, 122, 123}
theorem cut151 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support151, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 737, OmissionResidual.support 816, OmissionResidual.support 739] ![OmissionResidual.demand 737, OmissionResidual.demand 816, OmissionResidual.demand 739] ![1, 1, 1]
    support151 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 737) (Fin.cases (hrows 816) (Fin.cases (hrows 739) (fun i => Fin.elim0 i))))
def support152 : Finset (Fin 154) := {49, 59, 64, 72, 82, 87, 92, 93, 97, 99, 102, 103, 108, 113, 122, 124, 130}
theorem cut152 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support152, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 737, OmissionResidual.support 818, OmissionResidual.support 739] ![OmissionResidual.demand 737, OmissionResidual.demand 818, OmissionResidual.demand 739] ![1, 1, 1]
    support152 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 737) (Fin.cases (hrows 818) (Fin.cases (hrows 739) (fun i => Fin.elim0 i))))
def support153 : Finset (Fin 154) := {60, 70, 72, 75, 82, 87, 92, 93, 97, 99, 102, 103, 108, 113, 116, 122, 123}
theorem cut153 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support153, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 816, OmissionResidual.support 783] ![OmissionResidual.demand 779, OmissionResidual.demand 816, OmissionResidual.demand 783] ![1, 1, 1]
    support153 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 816) (Fin.cases (hrows 783) (fun i => Fin.elim0 i))))
def support154 : Finset (Fin 154) := {60, 70, 72, 75, 82, 87, 92, 93, 99, 102, 103, 106, 108, 112, 116, 121, 122, 123}
theorem cut154 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support154, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 781, OmissionResidual.support 816, OmissionResidual.support 783] ![OmissionResidual.demand 781, OmissionResidual.demand 816, OmissionResidual.demand 783] ![1, 1, 1]
    support154 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 781) (Fin.cases (hrows 816) (Fin.cases (hrows 783) (fun i => Fin.elim0 i))))
def support155 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 84, 102, 103, 120}
theorem cut155 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support155, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 680, OmissionResidual.support 679, OmissionResidual.support 731] ![OmissionResidual.demand 680, OmissionResidual.demand 679, OmissionResidual.demand 731] ![1, 1, 1]
    support155 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 680) (Fin.cases (hrows 679) (Fin.cases (hrows 731) (fun i => Fin.elim0 i))))
def support156 : Finset (Fin 154) := {71, 81, 83, 86, 92, 93, 97, 102, 106, 108, 112, 116, 120, 128, 129, 134}
theorem cut156 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support156, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 815, OmissionResidual.support 832, OmissionResidual.support 813] ![OmissionResidual.demand 815, OmissionResidual.demand 832, OmissionResidual.demand 813] ![1, 1, 1]
    support156 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 815) (Fin.cases (hrows 832) (Fin.cases (hrows 813) (fun i => Fin.elim0 i))))
def support157 : Finset (Fin 154) := {71, 81, 83, 86, 92, 93, 97, 102, 106, 108, 112, 116, 120, 128, 129}
theorem cut157 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support157, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 814, OmissionResidual.support 832, OmissionResidual.support 813] ![OmissionResidual.demand 814, OmissionResidual.demand 832, OmissionResidual.demand 813] ![1, 1, 1]
    support157 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 814) (Fin.cases (hrows 832) (Fin.cases (hrows 813) (fun i => Fin.elim0 i))))
def support158 : Finset (Fin 154) := {5, 8, 12, 13, 16, 18, 23, 24, 26, 27, 31, 39, 41, 47, 51, 60}
theorem cut158 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support158, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 528, OmissionResidual.support 497, OmissionResidual.support 482] ![OmissionResidual.demand 528, OmissionResidual.demand 497, OmissionResidual.demand 482] ![1, 1, 1]
    support158 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 528) (Fin.cases (hrows 497) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support159 : Finset (Fin 154) := {60, 70, 72, 75, 82, 87, 92, 99, 102, 106, 108, 112, 121, 122, 124, 135}
theorem cut159 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support159, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 781, OmissionResidual.support 783, OmissionResidual.support 819] ![OmissionResidual.demand 781, OmissionResidual.demand 783, OmissionResidual.demand 819] ![1, 1, 1]
    support159 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 781) (Fin.cases (hrows 783) (Fin.cases (hrows 819) (fun i => Fin.elim0 i))))
def support160 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 92, 99, 102, 103, 106, 108, 112, 114, 122, 124, 135}
theorem cut160 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support160, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 783, OmissionResidual.support 819] ![OmissionResidual.demand 780, OmissionResidual.demand 783, OmissionResidual.demand 819] ![1, 1, 1]
    support160 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 783) (Fin.cases (hrows 819) (fun i => Fin.elim0 i))))
def support161 : Finset (Fin 154) := {28, 36, 40, 46, 48, 51, 58, 61, 63, 69, 73, 80, 84, 92, 93, 112}
theorem cut161 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support161, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 730, OmissionResidual.support 624, OmissionResidual.support 623] ![OmissionResidual.demand 730, OmissionResidual.demand 624, OmissionResidual.demand 623] ![1, 1, 1]
    support161 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 730) (Fin.cases (hrows 624) (Fin.cases (hrows 623) (fun i => Fin.elim0 i))))
def support162 : Finset (Fin 154) := {14, 20, 23, 30, 33, 41, 46, 51, 57, 59, 67, 70, 78, 82, 96}
theorem cut162 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support162, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 878, OmissionResidual.support 540, OmissionResidual.support 900] ![OmissionResidual.demand 878, OmissionResidual.demand 540, OmissionResidual.demand 900] ![1, 1, 1]
    support162 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 878) (Fin.cases (hrows 540) (Fin.cases (hrows 900) (fun i => Fin.elim0 i))))
def support163 : Finset (Fin 154) := {14, 20, 23, 28, 36, 38, 40, 41, 46, 47, 51, 57, 60, 63, 73, 80, 102}
theorem cut163 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support163, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 539, OmissionResidual.support 679, OmissionResidual.support 625] ![OmissionResidual.demand 539, OmissionResidual.demand 679, OmissionResidual.demand 625] ![1, 1, 1]
    support163 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 539) (Fin.cases (hrows 679) (Fin.cases (hrows 625) (fun i => Fin.elim0 i))))
def support164 : Finset (Fin 154) := {14, 20, 23, 28, 36, 38, 40, 41, 46, 47, 51, 57, 60, 63, 73, 80, 84, 102, 112}
theorem cut164 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support164, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 539, OmissionResidual.support 681, OmissionResidual.support 625] ![OmissionResidual.demand 539, OmissionResidual.demand 681, OmissionResidual.demand 625] ![1, 1, 1]
    support164 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 539) (Fin.cases (hrows 681) (Fin.cases (hrows 625) (fun i => Fin.elim0 i))))
def support165 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 92, 97, 99, 102, 103, 112, 113, 116, 123, 129}
theorem cut165 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support165, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 817, OmissionResidual.support 784] ![OmissionResidual.demand 779, OmissionResidual.demand 817, OmissionResidual.demand 784] ![1, 1, 1]
    support165 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 817) (Fin.cases (hrows 784) (fun i => Fin.elim0 i))))
def support166 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 92, 99, 102, 103, 106, 112, 116, 121, 123, 129}
theorem cut166 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support166, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 781, OmissionResidual.support 817, OmissionResidual.support 784] ![OmissionResidual.demand 781, OmissionResidual.demand 817, OmissionResidual.demand 784] ![1, 1, 1]
    support166 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 781) (Fin.cases (hrows 817) (Fin.cases (hrows 784) (fun i => Fin.elim0 i))))
def support167 : Finset (Fin 154) := {72, 82, 87, 93, 94, 99, 102, 103, 106, 112, 116, 120, 123, 124, 135, 144}
theorem cut167 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support167, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 816, OmissionResidual.support 819, OmissionResidual.support 843] ![OmissionResidual.demand 816, OmissionResidual.demand 819, OmissionResidual.demand 843] ![1, 1, 1]
    support167 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 816) (Fin.cases (hrows 819) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
def support168 : Finset (Fin 154) := {73, 83, 84, 88, 93, 94, 100, 102, 103, 109, 112, 117, 120, 134, 135, 140}
theorem cut168 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support168, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 969, OmissionResidual.support 968, OmissionResidual.support 458] ![OmissionResidual.demand 969, OmissionResidual.demand 968, OmissionResidual.demand 458] ![1, 1, 1]
    support168 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 969) (Fin.cases (hrows 968) (Fin.cases (hrows 458) (fun i => Fin.elim0 i))))
def support169 : Finset (Fin 154) := {2, 4, 13, 21, 25, 31, 34, 43, 44, 53, 64, 75, 87, 91, 99, 111, 118}
theorem cut169 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support169, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 995, OmissionResidual.support 10, OmissionResidual.support 985] ![OmissionResidual.demand 995, OmissionResidual.demand 10, OmissionResidual.demand 985] ![1, 1, 1]
    support169 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 995) (Fin.cases (hrows 10) (Fin.cases (hrows 985) (fun i => Fin.elim0 i))))
def support170 : Finset (Fin 154) := {5, 8, 13, 21, 25, 31, 34, 43, 44, 53, 64, 75, 87, 91, 99, 111, 118}
theorem cut170 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support170, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 995, OmissionResidual.support 30, OmissionResidual.support 985] ![OmissionResidual.demand 995, OmissionResidual.demand 30, OmissionResidual.demand 985] ![1, 1, 1]
    support170 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 995) (Fin.cases (hrows 30) (Fin.cases (hrows 985) (fun i => Fin.elim0 i))))
def support171 : Finset (Fin 154) := {0, 7, 11, 12, 16, 20, 23, 30, 35, 43, 46, 53, 59, 64, 74}
theorem cut171 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support171, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 466, OmissionResidual.support 494, OmissionResidual.support 526] ![OmissionResidual.demand 466, OmissionResidual.demand 494, OmissionResidual.demand 526] ![1, 1, 1]
    support171 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 466) (Fin.cases (hrows 494) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support172 : Finset (Fin 154) := {1, 7, 11, 12, 16, 20, 23, 30, 35, 43, 46, 53, 59, 64, 74}
theorem cut172 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support172, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 468, OmissionResidual.support 494, OmissionResidual.support 526] ![OmissionResidual.demand 468, OmissionResidual.demand 494, OmissionResidual.demand 526] ![1, 1, 1]
    support172 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 468) (Fin.cases (hrows 494) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support173 : Finset (Fin 154) := {109, 116, 123, 124, 127, 129, 130, 134, 135, 138, 139, 140, 143, 144, 151, 152, 153}
theorem cut173 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support173, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1146, OmissionResidual.support 1147, OmissionResidual.support 1160] ![OmissionResidual.demand 1146, OmissionResidual.demand 1147, OmissionResidual.demand 1160] ![1, 1, 1]
    support173 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1146) (Fin.cases (hrows 1147) (Fin.cases (hrows 1160) (fun i => Fin.elim0 i))))
def support174 : Finset (Fin 154) := {84, 88, 94, 97, 103, 105, 112, 113, 119, 120, 121, 127, 128, 133, 134, 135, 145, 146, 148}
theorem cut174 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support174, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1103, OmissionResidual.support 1102, OmissionResidual.support 1093] ![OmissionResidual.demand 1103, OmissionResidual.demand 1102, OmissionResidual.demand 1093] ![1, 1, 1]
    support174 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1103) (Fin.cases (hrows 1102) (Fin.cases (hrows 1093) (fun i => Fin.elim0 i))))
def support175 : Finset (Fin 154) := {60, 70, 72, 75, 82, 87, 92, 99, 102, 106, 108, 112, 116, 121, 122, 129}
theorem cut175 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support175, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 781, OmissionResidual.support 783, OmissionResidual.support 817] ![OmissionResidual.demand 781, OmissionResidual.demand 783, OmissionResidual.demand 817] ![1, 1, 1]
    support175 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 781) (Fin.cases (hrows 783) (Fin.cases (hrows 817) (fun i => Fin.elim0 i))))
#print axioms cut175
def support176 : Finset (Fin 154) := {41, 50, 55, 60, 70, 71, 75, 79, 81, 87, 94, 103, 106, 109, 114, 116, 123}
theorem cut176 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support176, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 941, OmissionResidual.support 780, OmissionResidual.support 942] ![OmissionResidual.demand 941, OmissionResidual.demand 780, OmissionResidual.demand 942] ![1, 1, 1]
    support176 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 941) (Fin.cases (hrows 780) (Fin.cases (hrows 942) (fun i => Fin.elim0 i))))
def support177 : Finset (Fin 154) := {78, 84, 87, 94, 96, 103, 111, 112, 113, 120, 121, 127, 129, 133, 135, 141, 146, 148}
theorem cut177 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support177, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1082, OmissionResidual.support 1093, OmissionResidual.support 1081] ![OmissionResidual.demand 1082, OmissionResidual.demand 1093, OmissionResidual.demand 1081] ![1, 1, 1]
    support177 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1082) (Fin.cases (hrows 1093) (Fin.cases (hrows 1081) (fun i => Fin.elim0 i))))
def support178 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 92, 99, 102, 103, 106, 108, 112, 114, 116, 122, 129}
theorem cut178 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support178, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 783, OmissionResidual.support 817] ![OmissionResidual.demand 780, OmissionResidual.demand 783, OmissionResidual.demand 817] ![1, 1, 1]
    support178 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 783) (Fin.cases (hrows 817) (fun i => Fin.elim0 i))))
def support179 : Finset (Fin 154) := {0, 4, 8, 11, 14, 16, 17, 23, 25, 30, 33, 39, 45, 50, 55, 65}
theorem cut179 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support179, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 0, OmissionResidual.support 520, OmissionResidual.support 557] ![OmissionResidual.demand 0, OmissionResidual.demand 520, OmissionResidual.demand 557] ![1, 1, 1]
    support179 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 520) (Fin.cases (hrows 557) (fun i => Fin.elim0 i))))
def support180 : Finset (Fin 154) := {1, 4, 8, 11, 14, 16, 17, 23, 25, 30, 33, 39, 45, 50, 55, 65}
theorem cut180 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support180, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 4, OmissionResidual.support 520, OmissionResidual.support 557] ![OmissionResidual.demand 4, OmissionResidual.demand 520, OmissionResidual.demand 557] ![1, 1, 1]
    support180 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 4) (Fin.cases (hrows 520) (Fin.cases (hrows 557) (fun i => Fin.elim0 i))))
def support181 : Finset (Fin 154) := {109, 116, 123, 127, 129, 133, 134, 138, 139, 140, 142, 144, 146, 148, 150, 152, 153}
theorem cut181 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support181, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1144, OmissionResidual.support 1147, OmissionResidual.support 1164] ![OmissionResidual.demand 1144, OmissionResidual.demand 1147, OmissionResidual.demand 1164] ![1, 1, 1]
    support181 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1144) (Fin.cases (hrows 1147) (Fin.cases (hrows 1164) (fun i => Fin.elim0 i))))
def support182 : Finset (Fin 154) := {100, 108, 115, 119, 122, 129, 133, 134, 135, 138, 139, 140, 142, 146, 148, 149, 150, 153}
theorem cut182 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support182, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1131, OmissionResidual.support 1132, OmissionResidual.support 1164] ![OmissionResidual.demand 1131, OmissionResidual.demand 1132, OmissionResidual.demand 1164] ![1, 1, 1]
    support182 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1131) (Fin.cases (hrows 1132) (Fin.cases (hrows 1164) (fun i => Fin.elim0 i))))
def support183 : Finset (Fin 154) := {72, 82, 87, 93, 94, 99, 102, 103, 106, 112, 116, 120, 124, 129, 130, 144}
theorem cut183 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support183, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 818, OmissionResidual.support 817, OmissionResidual.support 843] ![OmissionResidual.demand 818, OmissionResidual.demand 817, OmissionResidual.demand 843] ![1, 1, 1]
    support183 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 818) (Fin.cases (hrows 817) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
def support184 : Finset (Fin 154) := {10, 14, 16, 20, 25, 30, 33, 36, 39, 45, 47, 50, 55, 60, 65, 66, 75}
theorem cut184 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support184, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 875, OmissionResidual.support 866, OmissionResidual.support 557] ![OmissionResidual.demand 875, OmissionResidual.demand 866, OmissionResidual.demand 557] ![1, 1, 1]
    support184 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 875) (Fin.cases (hrows 866) (Fin.cases (hrows 557) (fun i => Fin.elim0 i))))
def support185 : Finset (Fin 154) := {13, 18, 26, 35, 44, 55, 58, 64, 69, 71, 75, 76, 81, 86, 95}
theorem cut185 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support185, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 874, OmissionResidual.support 873, OmissionResidual.support 616] ![OmissionResidual.demand 874, OmissionResidual.demand 873, OmissionResidual.demand 616] ![1, 1, 1]
    support185 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 874) (Fin.cases (hrows 873) (Fin.cases (hrows 616) (fun i => Fin.elim0 i))))
def support186 : Finset (Fin 154) := {14, 20, 23, 28, 36, 38, 40, 41, 46, 47, 51, 57, 60, 63, 69, 73, 84, 93, 103}
theorem cut186 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support186, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 680, OmissionResidual.support 539, OmissionResidual.support 624] ![OmissionResidual.demand 680, OmissionResidual.demand 539, OmissionResidual.demand 624] ![1, 1, 1]
    support186 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 680) (Fin.cases (hrows 539) (Fin.cases (hrows 624) (fun i => Fin.elim0 i))))
def support187 : Finset (Fin 154) := {41, 50, 55, 60, 67, 70, 71, 75, 81, 87, 94, 98, 103, 106, 114}
theorem cut187 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support187, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 937, OmissionResidual.support 938] ![OmissionResidual.demand 780, OmissionResidual.demand 937, OmissionResidual.demand 938] ![1, 1, 1]
    support187 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 937) (Fin.cases (hrows 938) (fun i => Fin.elim0 i))))
def support188 : Finset (Fin 154) := {90, 99, 107, 108, 111, 115, 122, 123, 126, 129, 130, 133, 135, 142, 143, 146, 149}
theorem cut188 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support188, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1141, OmissionResidual.support 1110, OmissionResidual.support 1113] ![OmissionResidual.demand 1141, OmissionResidual.demand 1110, OmissionResidual.demand 1113] ![1, 1, 1]
    support188 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1141) (Fin.cases (hrows 1110) (Fin.cases (hrows 1113) (fun i => Fin.elim0 i))))
def support189 : Finset (Fin 154) := {15, 21, 24, 27, 31, 34, 36, 39, 41, 47, 49, 51, 56, 60, 72, 78, 87}
theorem cut189 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support189, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 903, OmissionResidual.support 578, OmissionResidual.support 881] ![OmissionResidual.demand 903, OmissionResidual.demand 578, OmissionResidual.demand 881] ![1, 1, 1]
    support189 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 903) (Fin.cases (hrows 578) (Fin.cases (hrows 881) (fun i => Fin.elim0 i))))
def support190 : Finset (Fin 154) := {10, 14, 16, 20, 23, 25, 30, 36, 41, 47, 49, 51, 56, 60, 72, 78, 87}
theorem cut190 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support190, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 539, OmissionResidual.support 884, OmissionResidual.support 868] ![OmissionResidual.demand 539, OmissionResidual.demand 884, OmissionResidual.demand 868] ![1, 1, 1]
    support190 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 539) (Fin.cases (hrows 884) (Fin.cases (hrows 868) (fun i => Fin.elim0 i))))
def support191 : Finset (Fin 154) := {6, 11, 14, 20, 21, 23, 27, 31, 36, 37, 41, 42, 47, 51, 52, 60, 62}
theorem cut191 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support191, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 539, OmissionResidual.support 578, OmissionResidual.support 491] ![OmissionResidual.demand 539, OmissionResidual.demand 578, OmissionResidual.demand 491] ![1, 1, 1]
    support191 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 539) (Fin.cases (hrows 578) (Fin.cases (hrows 491) (fun i => Fin.elim0 i))))
def support192 : Finset (Fin 154) := {10, 16, 20, 21, 27, 31, 36, 37, 42, 47, 52, 62, 63, 72}
theorem cut192 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support192, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 515, OmissionResidual.support 514, OmissionResidual.support 582] ![OmissionResidual.demand 515, OmissionResidual.demand 514, OmissionResidual.demand 582] ![1, 1, 1]
    support192 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 515) (Fin.cases (hrows 514) (Fin.cases (hrows 582) (fun i => Fin.elim0 i))))
def support193 : Finset (Fin 154) := {6, 10, 11, 16, 20, 21, 27, 31, 36, 37, 42, 47, 52, 62, 63, 72}
theorem cut193 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support193, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 515, OmissionResidual.support 491, OmissionResidual.support 582] ![OmissionResidual.demand 515, OmissionResidual.demand 491, OmissionResidual.demand 582] ![1, 1, 1]
    support193 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 515) (Fin.cases (hrows 491) (Fin.cases (hrows 582) (fun i => Fin.elim0 i))))
def support194 : Finset (Fin 154) := {60, 70, 72, 75, 82, 87, 92, 93, 99, 103, 106, 112, 116, 121, 123, 129}
theorem cut194 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support194, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 781, OmissionResidual.support 816, OmissionResidual.support 785] ![OmissionResidual.demand 781, OmissionResidual.demand 816, OmissionResidual.demand 785] ![1, 1, 1]
    support194 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 781) (Fin.cases (hrows 816) (Fin.cases (hrows 785) (fun i => Fin.elim0 i))))
def support195 : Finset (Fin 154) := {60, 70, 72, 75, 82, 87, 92, 93, 97, 99, 102, 103, 112, 113, 116, 123, 129}
theorem cut195 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support195, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 816, OmissionResidual.support 785] ![OmissionResidual.demand 779, OmissionResidual.demand 816, OmissionResidual.demand 785] ![1, 1, 1]
    support195 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 816) (Fin.cases (hrows 785) (fun i => Fin.elim0 i))))
def support196 : Finset (Fin 154) := {21, 27, 28, 31, 36, 38, 40, 41, 46, 47, 51, 57, 60, 63, 69, 73, 93}
theorem cut196 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support196, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 624, OmissionResidual.support 578] ![OmissionResidual.demand 678, OmissionResidual.demand 624, OmissionResidual.demand 578] ![1, 1, 1]
    support196 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 624) (Fin.cases (hrows 578) (fun i => Fin.elim0 i))))
def support197 : Finset (Fin 154) := {47, 48, 57, 58, 61, 69, 73, 75, 80, 84, 87, 103, 106, 112, 114, 121}
theorem cut197 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support197, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 730, OmissionResidual.support 728, OmissionResidual.support 729] ![OmissionResidual.demand 730, OmissionResidual.demand 728, OmissionResidual.demand 729] ![1, 1, 1]
    support197 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 730) (Fin.cases (hrows 728) (Fin.cases (hrows 729) (fun i => Fin.elim0 i))))
def support198 : Finset (Fin 154) := {48, 58, 61, 69, 71, 73, 76, 80, 81, 84, 88, 92, 102, 112, 113}
theorem cut198 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support198, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 730, OmissionResidual.support 404, OmissionResidual.support 355] ![OmissionResidual.demand 730, OmissionResidual.demand 404, OmissionResidual.demand 355] ![1, 1, 1]
    support198 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 730) (Fin.cases (hrows 404) (Fin.cases (hrows 355) (fun i => Fin.elim0 i))))
def support199 : Finset (Fin 154) := {61, 71, 73, 76, 81, 83, 88, 92, 93, 100, 102, 109, 113, 120, 134}
theorem cut199 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support199, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 962, OmissionResidual.support 968, OmissionResidual.support 404] ![OmissionResidual.demand 962, OmissionResidual.demand 968, OmissionResidual.demand 404] ![1, 1, 1]
    support199 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 962) (Fin.cases (hrows 968) (Fin.cases (hrows 404) (fun i => Fin.elim0 i))))
def support200 : Finset (Fin 154) := {2, 4, 16, 19, 24, 25, 28, 30, 34, 39, 40, 49, 54, 56, 60, 72, 78, 87}
theorem cut200 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support200, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 903, OmissionResidual.support 12, OmissionResidual.support 884] ![OmissionResidual.demand 903, OmissionResidual.demand 12, OmissionResidual.demand 884] ![1, 1, 1]
    support200 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 903) (Fin.cases (hrows 12) (Fin.cases (hrows 884) (fun i => Fin.elim0 i))))
#print axioms cut200
def support201 : Finset (Fin 154) := {5, 8, 16, 19, 24, 25, 28, 30, 34, 39, 40, 49, 54, 56, 60, 72, 78, 87}
theorem cut201 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support201, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 903, OmissionResidual.support 32, OmissionResidual.support 884] ![OmissionResidual.demand 903, OmissionResidual.demand 32, OmissionResidual.demand 884] ![1, 1, 1]
    support201 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 903) (Fin.cases (hrows 32) (Fin.cases (hrows 884) (fun i => Fin.elim0 i))))
def support202 : Finset (Fin 154) := {19, 26, 35, 40, 48, 51, 58, 61, 69, 71, 76, 80, 81, 88, 92, 98, 112, 121}
theorem cut202 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support202, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 959, OmissionResidual.support 572, OmissionResidual.support 945] ![OmissionResidual.demand 959, OmissionResidual.demand 572, OmissionResidual.demand 945] ![1, 1, 1]
    support202 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 959) (Fin.cases (hrows 572) (Fin.cases (hrows 945) (fun i => Fin.elim0 i))))
def support203 : Finset (Fin 154) := {20, 43, 46, 50, 57, 65, 70, 75, 77, 81, 82, 85, 87, 96, 103, 106, 114}
theorem cut203 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support203, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 741, OmissionResidual.support 576, OmissionResidual.support 577] ![OmissionResidual.demand 741, OmissionResidual.demand 576, OmissionResidual.demand 577] ![1, 1, 1]
    support203 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 741) (Fin.cases (hrows 576) (Fin.cases (hrows 577) (fun i => Fin.elim0 i))))
def support204 : Finset (Fin 154) := {10, 14, 16, 20, 21, 23, 27, 31, 36, 37, 41, 42, 47, 51, 52, 60, 62}
theorem cut204 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support204, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 539, OmissionResidual.support 578, OmissionResidual.support 514] ![OmissionResidual.demand 539, OmissionResidual.demand 578, OmissionResidual.demand 514] ![1, 1, 1]
    support204 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 539) (Fin.cases (hrows 578) (Fin.cases (hrows 514) (fun i => Fin.elim0 i))))
def support205 : Finset (Fin 154) := {21, 27, 28, 31, 36, 40, 46, 52, 57, 58, 63, 69, 73, 82, 83, 93}
theorem cut205 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support205, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 624, OmissionResidual.support 583, OmissionResidual.support 584] ![OmissionResidual.demand 624, OmissionResidual.demand 583, OmissionResidual.demand 584] ![1, 1, 1]
    support205 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 624) (Fin.cases (hrows 583) (Fin.cases (hrows 584) (fun i => Fin.elim0 i))))
def support206 : Finset (Fin 154) := {15, 21, 24, 27, 28, 31, 36, 40, 42, 46, 47, 52, 63, 69, 72, 73, 93}
theorem cut206 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support206, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 585, OmissionResidual.support 624, OmissionResidual.support 551] ![OmissionResidual.demand 585, OmissionResidual.demand 624, OmissionResidual.demand 551] ![1, 1, 1]
    support206 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 585) (Fin.cases (hrows 624) (Fin.cases (hrows 551) (fun i => Fin.elim0 i))))
def support207 : Finset (Fin 154) := {3, 11, 12, 18, 24, 27, 31, 35, 39, 43, 53, 57, 65, 70, 75, 85}
theorem cut207 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support207, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 569, OmissionResidual.support 527, OmissionResidual.support 474] ![OmissionResidual.demand 569, OmissionResidual.demand 527, OmissionResidual.demand 474] ![1, 1, 1]
    support207 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 569) (Fin.cases (hrows 527) (Fin.cases (hrows 474) (fun i => Fin.elim0 i))))
def support208 : Finset (Fin 154) := {27, 46, 53, 57, 60, 65, 70, 75, 77, 82, 85, 87, 92, 96, 97, 102, 113}
theorem cut208 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support208, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 618, OmissionResidual.support 620] ![OmissionResidual.demand 779, OmissionResidual.demand 618, OmissionResidual.demand 620] ![1, 1, 1]
    support208 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 618) (Fin.cases (hrows 620) (fun i => Fin.elim0 i))))
def support209 : Finset (Fin 154) := {27, 46, 53, 57, 60, 65, 70, 75, 77, 81, 82, 85, 87, 96, 103, 106, 114}
theorem cut209 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support209, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 618, OmissionResidual.support 620] ![OmissionResidual.demand 780, OmissionResidual.demand 618, OmissionResidual.demand 620] ![1, 1, 1]
    support209 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 618) (Fin.cases (hrows 620) (fun i => Fin.elim0 i))))
def support210 : Finset (Fin 154) := {27, 46, 53, 57, 60, 65, 70, 75, 77, 82, 85, 87, 92, 96, 106, 112, 121}
theorem cut210 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support210, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 781, OmissionResidual.support 618, OmissionResidual.support 620] ![OmissionResidual.demand 781, OmissionResidual.demand 618, OmissionResidual.demand 620] ![1, 1, 1]
    support210 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 781) (Fin.cases (hrows 618) (Fin.cases (hrows 620) (fun i => Fin.elim0 i))))
def support211 : Finset (Fin 154) := {60, 70, 75, 85, 87, 92, 96, 97, 102, 104, 113, 118, 121, 129, 132, 141}
theorem cut211 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support211, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1070, OmissionResidual.support 779, OmissionResidual.support 1099] ![OmissionResidual.demand 1070, OmissionResidual.demand 779, OmissionResidual.demand 1099] ![1, 1, 1]
    support211 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1070) (Fin.cases (hrows 779) (Fin.cases (hrows 1099) (fun i => Fin.elim0 i))))
def support212 : Finset (Fin 154) := {99, 107, 108, 115, 118, 122, 123, 126, 129, 130, 135, 138, 142, 143, 149}
theorem cut212 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support212, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1141, OmissionResidual.support 1128, OmissionResidual.support 1125] ![OmissionResidual.demand 1141, OmissionResidual.demand 1128, OmissionResidual.demand 1125] ![1, 1, 1]
    support212 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1141) (Fin.cases (hrows 1128) (Fin.cases (hrows 1125) (fun i => Fin.elim0 i))))
def support213 : Finset (Fin 154) := {12, 27, 35, 43, 46, 53, 57, 59, 64, 65, 70, 74, 75, 85}
theorem cut213 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support213, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 527, OmissionResidual.support 618, OmissionResidual.support 526] ![OmissionResidual.demand 527, OmissionResidual.demand 618, OmissionResidual.demand 526] ![1, 1, 1]
    support213 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 527) (Fin.cases (hrows 618) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support214 : Finset (Fin 154) := {14, 20, 23, 30, 41, 43, 46, 51, 57, 59, 70, 77, 82, 87, 96}
theorem cut214 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support214, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 540, OmissionResidual.support 577, OmissionResidual.support 639] ![OmissionResidual.demand 540, OmissionResidual.demand 577, OmissionResidual.demand 639] ![1, 1, 1]
    support214 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 540) (Fin.cases (hrows 577) (Fin.cases (hrows 639) (fun i => Fin.elim0 i))))
def support215 : Finset (Fin 154) := {5, 12, 16, 18, 24, 27, 31, 35, 39, 43, 53, 57, 65, 70, 75, 85}
theorem cut215 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support215, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 569, OmissionResidual.support 527, OmissionResidual.support 482] ![OmissionResidual.demand 569, OmissionResidual.demand 527, OmissionResidual.demand 482] ![1, 1, 1]
    support215 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 569) (Fin.cases (hrows 527) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support216 : Finset (Fin 154) := {50, 62, 65, 70, 77, 81, 82, 89, 93, 97, 103, 105, 116, 123}
theorem cut216 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support216, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 797, OmissionResidual.support 740, OmissionResidual.support 743] ![OmissionResidual.demand 797, OmissionResidual.demand 740, OmissionResidual.demand 743] ![1, 1, 1]
    support216 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 797) (Fin.cases (hrows 740) (Fin.cases (hrows 743) (fun i => Fin.elim0 i))))
def support217 : Finset (Fin 154) := {19, 26, 35, 40, 48, 51, 58, 61, 69, 71, 76, 80, 81, 88, 92, 98, 120, 128}
theorem cut217 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support217, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 960, OmissionResidual.support 572, OmissionResidual.support 946] ![OmissionResidual.demand 960, OmissionResidual.demand 572, OmissionResidual.demand 946] ![1, 1, 1]
    support217 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 960) (Fin.cases (hrows 572) (Fin.cases (hrows 946) (fun i => Fin.elim0 i))))
def support218 : Finset (Fin 154) := {73, 83, 84, 88, 93, 94, 100, 102, 103, 109, 112, 117, 120, 129, 140}
theorem cut218 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support218, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 967, OmissionResidual.support 970, OmissionResidual.support 458] ![OmissionResidual.demand 967, OmissionResidual.demand 970, OmissionResidual.demand 458] ![1, 1, 1]
    support218 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 967) (Fin.cases (hrows 970) (Fin.cases (hrows 458) (fun i => Fin.elim0 i))))
def support219 : Finset (Fin 154) := {19, 26, 35, 48, 54, 58, 61, 66, 69, 73, 76, 80, 81, 84, 92, 95, 104, 112}
theorem cut219 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support219, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 888, OmissionResidual.support 730, OmissionResidual.support 887] ![OmissionResidual.demand 888, OmissionResidual.demand 730, OmissionResidual.demand 887] ![1, 1, 1]
    support219 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 888) (Fin.cases (hrows 730) (Fin.cases (hrows 887) (fun i => Fin.elim0 i))))
def support220 : Finset (Fin 154) := {21, 27, 28, 31, 36, 38, 40, 41, 46, 47, 51, 57, 60, 63, 73, 80, 84, 102, 112}
theorem cut220 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support220, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 681, OmissionResidual.support 625, OmissionResidual.support 578] ![OmissionResidual.demand 681, OmissionResidual.demand 625, OmissionResidual.demand 578] ![1, 1, 1]
    support220 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 681) (Fin.cases (hrows 625) (Fin.cases (hrows 578) (fun i => Fin.elim0 i))))
def support221 : Finset (Fin 154) := {21, 27, 28, 31, 36, 38, 40, 41, 46, 47, 51, 57, 60, 63, 73, 80, 102}
theorem cut221 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support221, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 679, OmissionResidual.support 625, OmissionResidual.support 578] ![OmissionResidual.demand 679, OmissionResidual.demand 625, OmissionResidual.demand 578] ![1, 1, 1]
    support221 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 679) (Fin.cases (hrows 625) (Fin.cases (hrows 578) (fun i => Fin.elim0 i))))
def support222 : Finset (Fin 154) := {21, 27, 28, 31, 36, 40, 41, 46, 47, 51, 60, 61, 69, 81}
theorem cut222 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support222, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 578, OmissionResidual.support 622, OmissionResidual.support 581] ![OmissionResidual.demand 578, OmissionResidual.demand 622, OmissionResidual.demand 581] ![1, 1, 1]
    support222 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 578) (Fin.cases (hrows 622) (Fin.cases (hrows 581) (fun i => Fin.elim0 i))))
def support223 : Finset (Fin 154) := {61, 71, 73, 76, 81, 83, 88, 92, 93, 100, 102, 109, 112, 113, 129}
theorem cut223 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support223, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 961, OmissionResidual.support 967, OmissionResidual.support 404] ![OmissionResidual.demand 961, OmissionResidual.demand 967, OmissionResidual.demand 404] ![1, 1, 1]
    support223 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 961) (Fin.cases (hrows 967) (Fin.cases (hrows 404) (fun i => Fin.elim0 i))))
def support224 : Finset (Fin 154) := {19, 26, 35, 38, 40, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 81, 84, 112}
theorem cut224 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support224, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 571, OmissionResidual.support 681, OmissionResidual.support 730] ![OmissionResidual.demand 571, OmissionResidual.demand 681, OmissionResidual.demand 730] ![1, 1, 1]
    support224 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 571) (Fin.cases (hrows 681) (Fin.cases (hrows 730) (fun i => Fin.elim0 i))))
def support225 : Finset (Fin 154) := {19, 26, 35, 38, 40, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 81, 84, 102, 112}
theorem cut225 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support225, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 571, OmissionResidual.support 730, OmissionResidual.support 679] ![OmissionResidual.demand 571, OmissionResidual.demand 730, OmissionResidual.demand 679] ![1, 1, 1]
    support225 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 571) (Fin.cases (hrows 730) (Fin.cases (hrows 679) (fun i => Fin.elim0 i))))
#print axioms cut225
def support226 : Finset (Fin 154) := {84, 88, 94, 97, 103, 105, 112, 113, 119, 120, 121, 127, 129, 133, 135, 141, 146, 148}
theorem cut226 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support226, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1102, OmissionResidual.support 1093, OmissionResidual.support 1101] ![OmissionResidual.demand 1102, OmissionResidual.demand 1093, OmissionResidual.demand 1101] ![1, 1, 1]
    support226 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1102) (Fin.cases (hrows 1093) (Fin.cases (hrows 1101) (fun i => Fin.elim0 i))))
def support227 : Finset (Fin 154) := {0, 7, 8, 11, 12, 14, 16, 20, 23, 30, 33, 35, 46, 55, 57, 66, 70, 85}
theorem cut227 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support227, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 862, OmissionResidual.support 876, OmissionResidual.support 466] ![OmissionResidual.demand 862, OmissionResidual.demand 876, OmissionResidual.demand 466] ![1, 1, 1]
    support227 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 862) (Fin.cases (hrows 876) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support228 : Finset (Fin 154) := {1, 7, 8, 11, 12, 14, 16, 20, 23, 30, 33, 35, 46, 55, 57, 66, 70, 85}
theorem cut228 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support228, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 862, OmissionResidual.support 876, OmissionResidual.support 468] ![OmissionResidual.demand 862, OmissionResidual.demand 876, OmissionResidual.demand 468] ![1, 1, 1]
    support228 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 862) (Fin.cases (hrows 876) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support229 : Finset (Fin 154) := {100, 108, 115, 119, 122, 129, 133, 134, 135, 138, 139, 140, 142, 146, 148, 150, 151, 153}
theorem cut229 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support229, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1133, OmissionResidual.support 1164, OmissionResidual.support 1130] ![OmissionResidual.demand 1133, OmissionResidual.demand 1164, OmissionResidual.demand 1130] ![1, 1, 1]
    support229 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1133) (Fin.cases (hrows 1164) (Fin.cases (hrows 1130) (fun i => Fin.elim0 i))))
def support230 : Finset (Fin 154) := {45, 55, 65, 66, 75, 76, 85, 86, 95, 98, 104, 106, 109, 114, 116, 121, 123, 124, 127, 128, 129, 130, 132, 134, 135, 137, 138, 140, 141, 143, 144, 145, 148, 150, 151, 152}
theorem cut230 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    7 ≤ ∑ i ∈ support230, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1179, OmissionResidual.support 1159, OmissionResidual.support 1178] ![OmissionResidual.demand 1179, OmissionResidual.demand 1159, OmissionResidual.demand 1178] ![1, 1, 1]
    support230 2 7 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1179) (Fin.cases (hrows 1159) (Fin.cases (hrows 1178) (fun i => Fin.elim0 i))))
def support231 : Finset (Fin 154) := {2, 4, 10, 13, 15, 20, 21, 25, 27, 31, 34, 36, 44, 45, 47, 60, 66, 75}
theorem cut231 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support231, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 879, OmissionResidual.support 866, OmissionResidual.support 10] ![OmissionResidual.demand 879, OmissionResidual.demand 866, OmissionResidual.demand 10] ![1, 1, 1]
    support231 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 879) (Fin.cases (hrows 866) (Fin.cases (hrows 10) (fun i => Fin.elim0 i))))
def support232 : Finset (Fin 154) := {5, 8, 10, 13, 15, 20, 21, 25, 27, 31, 34, 36, 44, 45, 47, 60, 66, 75}
theorem cut232 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support232, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 879, OmissionResidual.support 866, OmissionResidual.support 30] ![OmissionResidual.demand 879, OmissionResidual.demand 866, OmissionResidual.demand 30] ![1, 1, 1]
    support232 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 879) (Fin.cases (hrows 866) (Fin.cases (hrows 30) (fun i => Fin.elim0 i))))
def support233 : Finset (Fin 154) := {21, 27, 28, 31, 36, 40, 46, 52, 57, 58, 63, 73, 80, 82, 83, 102}
theorem cut233 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support233, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 625, OmissionResidual.support 583, OmissionResidual.support 584] ![OmissionResidual.demand 625, OmissionResidual.demand 583, OmissionResidual.demand 584] ![1, 1, 1]
    support233 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 625) (Fin.cases (hrows 583) (Fin.cases (hrows 584) (fun i => Fin.elim0 i))))
def support234 : Finset (Fin 154) := {0, 4, 7, 11, 12, 16, 20, 23, 30, 31, 35, 40, 43, 46, 53, 59, 64, 74}
theorem cut234 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support234, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 479, OmissionResidual.support 466, OmissionResidual.support 526] ![OmissionResidual.demand 479, OmissionResidual.demand 466, OmissionResidual.demand 526] ![1, 1, 1]
    support234 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 479) (Fin.cases (hrows 466) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support235 : Finset (Fin 154) := {1, 4, 7, 11, 12, 16, 20, 23, 30, 31, 35, 40, 43, 46, 53, 59, 64, 74}
theorem cut235 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support235, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 479, OmissionResidual.support 468, OmissionResidual.support 526] ![OmissionResidual.demand 479, OmissionResidual.demand 468, OmissionResidual.demand 526] ![1, 1, 1]
    support235 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 479) (Fin.cases (hrows 468) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support236 : Finset (Fin 154) := {0, 7, 8, 11, 12, 16, 20, 23, 30, 31, 35, 40, 43, 46, 53, 59, 64, 74}
theorem cut236 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support236, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 496, OmissionResidual.support 466, OmissionResidual.support 494] ![OmissionResidual.demand 496, OmissionResidual.demand 466, OmissionResidual.demand 494] ![1, 1, 1]
    support236 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 496) (Fin.cases (hrows 466) (Fin.cases (hrows 494) (fun i => Fin.elim0 i))))
def support237 : Finset (Fin 154) := {1, 7, 8, 11, 12, 16, 20, 23, 30, 31, 35, 40, 43, 46, 53, 59, 64, 74}
theorem cut237 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support237, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 496, OmissionResidual.support 468, OmissionResidual.support 494] ![OmissionResidual.demand 496, OmissionResidual.demand 468, OmissionResidual.demand 494] ![1, 1, 1]
    support237 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 496) (Fin.cases (hrows 468) (Fin.cases (hrows 494) (fun i => Fin.elim0 i))))
def support238 : Finset (Fin 154) := {6, 11, 14, 20, 21, 23, 27, 31, 37, 41, 42, 46, 51, 52, 57, 62, 70}
theorem cut238 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support238, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 540, OmissionResidual.support 491, OmissionResidual.support 579] ![OmissionResidual.demand 540, OmissionResidual.demand 491, OmissionResidual.demand 579] ![1, 1, 1]
    support238 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 540) (Fin.cases (hrows 491) (Fin.cases (hrows 579) (fun i => Fin.elim0 i))))
def support239 : Finset (Fin 154) := {6, 11, 20, 21, 27, 29, 31, 36, 37, 41, 42, 47, 51, 52, 58, 60, 62, 84, 94}
theorem cut239 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support239, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 631, OmissionResidual.support 578, OmissionResidual.support 491] ![OmissionResidual.demand 631, OmissionResidual.demand 578, OmissionResidual.demand 491] ![1, 1, 1]
    support239 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 631) (Fin.cases (hrows 578) (Fin.cases (hrows 491) (fun i => Fin.elim0 i))))
def support240 : Finset (Fin 154) := {41, 50, 55, 60, 70, 71, 75, 79, 81, 87, 92, 94, 97, 102, 103, 109, 113, 116, 123}
theorem cut240 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support240, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 941, OmissionResidual.support 779, OmissionResidual.support 942] ![OmissionResidual.demand 941, OmissionResidual.demand 779, OmissionResidual.demand 942] ![1, 1, 1]
    support240 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 941) (Fin.cases (hrows 779) (Fin.cases (hrows 942) (fun i => Fin.elim0 i))))
def support241 : Finset (Fin 154) := {41, 50, 55, 60, 70, 71, 75, 79, 81, 87, 92, 94, 103, 106, 109, 112, 116, 121, 123}
theorem cut241 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support241, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 941, OmissionResidual.support 781, OmissionResidual.support 942] ![OmissionResidual.demand 941, OmissionResidual.demand 781, OmissionResidual.demand 942] ![1, 1, 1]
    support241 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 941) (Fin.cases (hrows 781) (Fin.cases (hrows 942) (fun i => Fin.elim0 i))))
def support242 : Finset (Fin 154) := {41, 50, 55, 60, 70, 71, 75, 79, 81, 92, 94, 99, 102, 103, 108, 109, 116, 122, 123}
theorem cut242 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support242, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 941, OmissionResidual.support 783, OmissionResidual.support 942] ![OmissionResidual.demand 941, OmissionResidual.demand 783, OmissionResidual.demand 942] ![1, 1, 1]
    support242 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 941) (Fin.cases (hrows 783) (Fin.cases (hrows 942) (fun i => Fin.elim0 i))))
def support243 : Finset (Fin 154) := {2, 4, 19, 25, 28, 34, 40, 43, 53, 54, 64, 75, 87, 91, 99, 111, 118}
theorem cut243 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support243, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 995, OmissionResidual.support 12, OmissionResidual.support 985] ![OmissionResidual.demand 995, OmissionResidual.demand 12, OmissionResidual.demand 985] ![1, 1, 1]
    support243 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 995) (Fin.cases (hrows 12) (Fin.cases (hrows 985) (fun i => Fin.elim0 i))))
def support244 : Finset (Fin 154) := {5, 8, 19, 25, 28, 34, 40, 43, 53, 54, 64, 75, 87, 91, 99, 111, 118}
theorem cut244 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support244, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 995, OmissionResidual.support 32, OmissionResidual.support 985] ![OmissionResidual.demand 995, OmissionResidual.demand 32, OmissionResidual.demand 985] ![1, 1, 1]
    support244 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 995) (Fin.cases (hrows 32) (Fin.cases (hrows 985) (fun i => Fin.elim0 i))))
def support245 : Finset (Fin 154) := {5, 8, 10, 12, 16, 20, 23, 26, 31, 32, 36, 40, 47, 49, 51, 60}
theorem cut245 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support245, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 495, OmissionResidual.support 513, OmissionResidual.support 485] ![OmissionResidual.demand 495, OmissionResidual.demand 513, OmissionResidual.demand 485] ![1, 1, 1]
    support245 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 495) (Fin.cases (hrows 513) (Fin.cases (hrows 485) (fun i => Fin.elim0 i))))
def support246 : Finset (Fin 154) := {47, 57, 71, 75, 80, 81, 86, 87, 92, 97, 102, 106, 112, 113, 121}
theorem cut246 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support246, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 812, OmissionResidual.support 727, OmissionResidual.support 729] ![OmissionResidual.demand 812, OmissionResidual.demand 727, OmissionResidual.demand 729] ![1, 1, 1]
    support246 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 812) (Fin.cases (hrows 727) (Fin.cases (hrows 729) (fun i => Fin.elim0 i))))
def support247 : Finset (Fin 154) := {8, 12, 13, 18, 23, 26, 31, 35, 36, 40, 41, 49, 51, 57, 70}
theorem cut247 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support247, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 495, OmissionResidual.support 529, OmissionResidual.support 498] ![OmissionResidual.demand 495, OmissionResidual.demand 529, OmissionResidual.demand 498] ![1, 1, 1]
    support247 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 495) (Fin.cases (hrows 529) (Fin.cases (hrows 498) (fun i => Fin.elim0 i))))
def support248 : Finset (Fin 154) := {60, 70, 71, 75, 81, 86, 87, 92, 97, 102, 103, 106, 112, 113, 114, 121}
theorem cut248 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support248, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 780, OmissionResidual.support 812] ![OmissionResidual.demand 779, OmissionResidual.demand 780, OmissionResidual.demand 812] ![1, 1, 1]
    support248 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 780) (Fin.cases (hrows 812) (fun i => Fin.elim0 i))))
def support249 : Finset (Fin 154) := {0, 4, 8, 11, 14, 16, 17, 23, 25, 30, 33, 39, 50, 56, 62, 77}
theorem cut249 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support249, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 0, OmissionResidual.support 84, OmissionResidual.support 131] ![OmissionResidual.demand 0, OmissionResidual.demand 84, OmissionResidual.demand 131] ![1, 1, 1]
    support249 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 84) (Fin.cases (hrows 131) (fun i => Fin.elim0 i))))
def support250 : Finset (Fin 154) := {1, 4, 8, 11, 14, 16, 17, 23, 25, 30, 33, 39, 50, 56, 62, 77}
theorem cut250 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support250, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 4, OmissionResidual.support 84, OmissionResidual.support 131] ![OmissionResidual.demand 4, OmissionResidual.demand 84, OmissionResidual.demand 131] ![1, 1, 1]
    support250 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 4) (Fin.cases (hrows 84) (Fin.cases (hrows 131) (fun i => Fin.elim0 i))))
#print axioms cut250
def support251 : Finset (Fin 154) := {21, 27, 28, 31, 36, 40, 41, 46, 51, 57, 58, 61, 69, 70, 71, 81}
theorem cut251 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support251, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 580, OmissionResidual.support 579, OmissionResidual.support 622] ![OmissionResidual.demand 580, OmissionResidual.demand 579, OmissionResidual.demand 622] ![1, 1, 1]
    support251 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 580) (Fin.cases (hrows 579) (Fin.cases (hrows 622) (fun i => Fin.elim0 i))))
def support252 : Finset (Fin 154) := {78, 84, 87, 94, 96, 103, 105, 111, 112, 113, 114, 120, 121, 127, 129, 130, 133, 141, 142, 150}
theorem cut252 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support252, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1078, OmissionResidual.support 1094, OmissionResidual.support 1081] ![OmissionResidual.demand 1078, OmissionResidual.demand 1094, OmissionResidual.demand 1081] ![1, 1, 1]
    support252 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1078) (Fin.cases (hrows 1094) (Fin.cases (hrows 1081) (fun i => Fin.elim0 i))))
def support253 : Finset (Fin 154) := {10, 14, 16, 20, 21, 23, 27, 31, 37, 41, 42, 46, 51, 52, 57, 62, 70}
theorem cut253 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support253, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 540, OmissionResidual.support 514, OmissionResidual.support 579] ![OmissionResidual.demand 540, OmissionResidual.demand 514, OmissionResidual.demand 579] ![1, 1, 1]
    support253 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 540) (Fin.cases (hrows 514) (Fin.cases (hrows 579) (fun i => Fin.elim0 i))))
def support254 : Finset (Fin 154) := {8, 12, 14, 20, 33, 35, 43, 46, 53, 55, 57, 59, 64, 66, 70, 74, 85}
theorem cut254 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support254, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 862, OmissionResidual.support 876, OmissionResidual.support 526] ![OmissionResidual.demand 862, OmissionResidual.demand 876, OmissionResidual.demand 526] ![1, 1, 1]
    support254 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 862) (Fin.cases (hrows 876) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support255 : Finset (Fin 154) := {14, 20, 23, 39, 41, 43, 46, 51, 53, 57, 59, 70, 77, 82, 87, 96}
theorem cut255 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support255, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 540, OmissionResidual.support 577, OmissionResidual.support 690] ![OmissionResidual.demand 540, OmissionResidual.demand 577, OmissionResidual.demand 690] ![1, 1, 1]
    support255 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 540) (Fin.cases (hrows 577) (Fin.cases (hrows 690) (fun i => Fin.elim0 i))))
def support256 : Finset (Fin 154) := {88, 97, 105, 106, 113, 114, 119, 121, 128, 132, 133, 135, 138, 140, 146, 148}
theorem cut256 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support256, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1138, OmissionResidual.support 1102, OmissionResidual.support 1104] ![OmissionResidual.demand 1138, OmissionResidual.demand 1102, OmissionResidual.demand 1104] ![1, 1, 1]
    support256 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1138) (Fin.cases (hrows 1102) (Fin.cases (hrows 1104) (fun i => Fin.elim0 i))))
def support257 : Finset (Fin 154) := {10, 16, 20, 21, 27, 29, 31, 36, 37, 41, 42, 47, 51, 52, 58, 60, 62, 84, 94}
theorem cut257 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support257, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 631, OmissionResidual.support 578, OmissionResidual.support 514] ![OmissionResidual.demand 631, OmissionResidual.demand 578, OmissionResidual.demand 514] ![1, 1, 1]
    support257 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 631) (Fin.cases (hrows 578) (Fin.cases (hrows 514) (fun i => Fin.elim0 i))))
def support258 : Finset (Fin 154) := {108, 115, 116, 122, 123, 126, 129, 132, 134, 135, 138, 140, 143, 148, 149}
theorem cut258 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support258, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1141, OmissionResidual.support 1142, OmissionResidual.support 1150] ![OmissionResidual.demand 1141, OmissionResidual.demand 1142, OmissionResidual.demand 1150] ![1, 1, 1]
    support258 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1141) (Fin.cases (hrows 1142) (Fin.cases (hrows 1150) (fun i => Fin.elim0 i))))
def support259 : Finset (Fin 154) := {100, 108, 115, 119, 122, 129, 133, 134, 135, 138, 139, 140, 142, 146, 148, 149, 150, 152}
theorem cut259 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support259, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1131, OmissionResidual.support 1132, OmissionResidual.support 1163] ![OmissionResidual.demand 1131, OmissionResidual.demand 1132, OmissionResidual.demand 1163] ![1, 1, 1]
    support259 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1131) (Fin.cases (hrows 1132) (Fin.cases (hrows 1163) (fun i => Fin.elim0 i))))
def support260 : Finset (Fin 154) := {60, 70, 72, 75, 81, 82, 87, 93, 97, 99, 103, 105, 116, 123}
theorem cut260 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support260, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 816, OmissionResidual.support 778, OmissionResidual.support 784] ![OmissionResidual.demand 816, OmissionResidual.demand 778, OmissionResidual.demand 784] ![1, 1, 1]
    support260 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 816) (Fin.cases (hrows 778) (Fin.cases (hrows 784) (fun i => Fin.elim0 i))))
def support261 : Finset (Fin 154) := {19, 21, 26, 27, 31, 35, 40, 41, 46, 51, 57, 61, 69, 70, 81}
theorem cut261 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support261, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 571, OmissionResidual.support 579, OmissionResidual.support 581] ![OmissionResidual.demand 571, OmissionResidual.demand 579, OmissionResidual.demand 581] ![1, 1, 1]
    support261 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 571) (Fin.cases (hrows 579) (Fin.cases (hrows 581) (fun i => Fin.elim0 i))))
def support262 : Finset (Fin 154) := {60, 70, 75, 83, 92, 93, 97, 99, 102, 108, 112, 116, 122, 129}
theorem cut262 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support262, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 783, OmissionResidual.support 832, OmissionResidual.support 785] ![OmissionResidual.demand 783, OmissionResidual.demand 832, OmissionResidual.demand 785] ![1, 1, 1]
    support262 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 783) (Fin.cases (hrows 832) (Fin.cases (hrows 785) (fun i => Fin.elim0 i))))
def support263 : Finset (Fin 154) := {8, 12, 14, 20, 33, 35, 36, 43, 47, 55, 57, 60, 65, 66, 70, 75, 85}
theorem cut263 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support263, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 875, OmissionResidual.support 862, OmissionResidual.support 527] ![OmissionResidual.demand 875, OmissionResidual.demand 862, OmissionResidual.demand 527] ![1, 1, 1]
    support263 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 875) (Fin.cases (hrows 862) (Fin.cases (hrows 527) (fun i => Fin.elim0 i))))
def support264 : Finset (Fin 154) := {63, 72, 78, 82, 84, 90, 93, 94, 102, 103, 109, 112, 117, 120, 123, 135, 140}
theorem cut264 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support264, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 966, OmissionResidual.support 963, OmissionResidual.support 458] ![OmissionResidual.demand 966, OmissionResidual.demand 963, OmissionResidual.demand 458] ![1, 1, 1]
    support264 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 966) (Fin.cases (hrows 963) (Fin.cases (hrows 458) (fun i => Fin.elim0 i))))
def support265 : Finset (Fin 154) := {5, 8, 12, 16, 21, 23, 24, 26, 27, 31, 36, 40, 41, 47, 49, 51, 60}
theorem cut265 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support265, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 483, OmissionResidual.support 578, OmissionResidual.support 497] ![OmissionResidual.demand 483, OmissionResidual.demand 578, OmissionResidual.demand 497] ![1, 1, 1]
    support265 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 483) (Fin.cases (hrows 578) (Fin.cases (hrows 497) (fun i => Fin.elim0 i))))
def support266 : Finset (Fin 154) := {21, 27, 31, 36, 38, 46, 47, 51, 52, 57, 63, 69, 72, 73, 93}
theorem cut266 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support266, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 585, OmissionResidual.support 582] ![OmissionResidual.demand 678, OmissionResidual.demand 585, OmissionResidual.demand 582] ![1, 1, 1]
    support266 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 585) (Fin.cases (hrows 582) (fun i => Fin.elim0 i))))
def support267 : Finset (Fin 154) := {90, 99, 107, 108, 111, 115, 122, 123, 126, 129, 130, 133, 135, 138, 142, 146}
theorem cut267 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support267, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1110, OmissionResidual.support 1140, OmissionResidual.support 1113] ![OmissionResidual.demand 1110, OmissionResidual.demand 1140, OmissionResidual.demand 1113] ![1, 1, 1]
    support267 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1110) (Fin.cases (hrows 1140) (Fin.cases (hrows 1113) (fun i => Fin.elim0 i))))
def support268 : Finset (Fin 154) := {0, 7, 8, 11, 12, 14, 16, 20, 23, 26, 30, 33, 36, 47, 55, 60, 66, 75}
theorem cut268 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support268, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 875, OmissionResidual.support 466, OmissionResidual.support 861] ![OmissionResidual.demand 875, OmissionResidual.demand 466, OmissionResidual.demand 861] ![1, 1, 1]
    support268 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 875) (Fin.cases (hrows 466) (Fin.cases (hrows 861) (fun i => Fin.elim0 i))))
def support269 : Finset (Fin 154) := {1, 7, 8, 11, 12, 14, 16, 20, 23, 26, 30, 33, 36, 47, 55, 60, 66, 75}
theorem cut269 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support269, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 875, OmissionResidual.support 468, OmissionResidual.support 861] ![OmissionResidual.demand 875, OmissionResidual.demand 468, OmissionResidual.demand 861] ![1, 1, 1]
    support269 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 875) (Fin.cases (hrows 468) (Fin.cases (hrows 861) (fun i => Fin.elim0 i))))
def support270 : Finset (Fin 154) := {0, 5, 7, 10, 11, 12, 16, 20, 23, 25, 26, 30, 36, 45, 47, 60, 66, 75}
theorem cut270 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support270, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 866, OmissionResidual.support 466, OmissionResidual.support 856] ![OmissionResidual.demand 866, OmissionResidual.demand 466, OmissionResidual.demand 856] ![1, 1, 1]
    support270 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 866) (Fin.cases (hrows 466) (Fin.cases (hrows 856) (fun i => Fin.elim0 i))))
def support271 : Finset (Fin 154) := {1, 5, 7, 10, 11, 12, 16, 20, 23, 25, 26, 30, 36, 45, 47, 60, 66, 75}
theorem cut271 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support271, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 866, OmissionResidual.support 468, OmissionResidual.support 856] ![OmissionResidual.demand 866, OmissionResidual.demand 468, OmissionResidual.demand 856] ![1, 1, 1]
    support271 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 866) (Fin.cases (hrows 468) (Fin.cases (hrows 856) (fun i => Fin.elim0 i))))
def support272 : Finset (Fin 154) := {60, 70, 71, 75, 81, 86, 87, 92, 97, 102, 103, 106, 113, 114, 120, 128}
theorem cut272 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support272, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 779, OmissionResidual.support 780, OmissionResidual.support 813] ![OmissionResidual.demand 779, OmissionResidual.demand 780, OmissionResidual.demand 813] ![1, 1, 1]
    support272 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 779) (Fin.cases (hrows 780) (Fin.cases (hrows 813) (fun i => Fin.elim0 i))))
def support273 : Finset (Fin 154) := {1, 7, 9, 11, 15, 18, 24, 26, 27, 31, 34, 36, 39, 45, 47, 60, 66, 75}
theorem cut273 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support273, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 863, OmissionResidual.support 879, OmissionResidual.support 469] ![OmissionResidual.demand 863, OmissionResidual.demand 879, OmissionResidual.demand 469] ![1, 1, 1]
    support273 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 863) (Fin.cases (hrows 879) (Fin.cases (hrows 469) (fun i => Fin.elim0 i))))
def support274 : Finset (Fin 154) := {3, 9, 11, 12, 15, 18, 24, 26, 27, 31, 34, 36, 39, 45, 47, 60, 66, 75}
theorem cut274 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support274, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 863, OmissionResidual.support 879, OmissionResidual.support 474] ![OmissionResidual.demand 863, OmissionResidual.demand 879, OmissionResidual.demand 474] ![1, 1, 1]
    support274 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 863) (Fin.cases (hrows 879) (Fin.cases (hrows 474) (fun i => Fin.elim0 i))))
def support275 : Finset (Fin 154) := {1, 7, 9, 11, 15, 18, 24, 26, 27, 31, 34, 36, 39, 45, 58, 71, 76, 86}
theorem cut275 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support275, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 864, OmissionResidual.support 880, OmissionResidual.support 469] ![OmissionResidual.demand 864, OmissionResidual.demand 880, OmissionResidual.demand 469] ![1, 1, 1]
    support275 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 864) (Fin.cases (hrows 880) (Fin.cases (hrows 469) (fun i => Fin.elim0 i))))
#print axioms cut275
def support276 : Finset (Fin 154) := {3, 9, 11, 12, 15, 18, 24, 26, 27, 31, 34, 36, 39, 45, 58, 71, 76, 86}
theorem cut276 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support276, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 864, OmissionResidual.support 880, OmissionResidual.support 474] ![OmissionResidual.demand 864, OmissionResidual.demand 880, OmissionResidual.demand 474] ![1, 1, 1]
    support276 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 864) (Fin.cases (hrows 880) (Fin.cases (hrows 474) (fun i => Fin.elim0 i))))
def support277 : Finset (Fin 154) := {8, 12, 20, 23, 31, 35, 40, 41, 43, 46, 51, 57, 59, 65, 70, 75, 85}
theorem cut277 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support277, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 496, OmissionResidual.support 498, OmissionResidual.support 576] ![OmissionResidual.demand 496, OmissionResidual.demand 498, OmissionResidual.demand 576] ![1, 1, 1]
    support277 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 496) (Fin.cases (hrows 498) (Fin.cases (hrows 576) (fun i => Fin.elim0 i))))
def support278 : Finset (Fin 154) := {8, 12, 14, 20, 23, 31, 35, 40, 41, 43, 46, 51, 57, 59, 65, 70, 75, 85}
theorem cut278 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support278, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 496, OmissionResidual.support 540, OmissionResidual.support 527] ![OmissionResidual.demand 496, OmissionResidual.demand 540, OmissionResidual.demand 527] ![1, 1, 1]
    support278 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 496) (Fin.cases (hrows 540) (Fin.cases (hrows 527) (fun i => Fin.elim0 i))))
def support279 : Finset (Fin 154) := {71, 81, 86, 92, 94, 97, 103, 106, 108, 112, 116, 120, 121, 124, 134, 140}
theorem cut279 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support279, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 815, OmissionResidual.support 842, OmissionResidual.support 812] ![OmissionResidual.demand 815, OmissionResidual.demand 842, OmissionResidual.demand 812] ![1, 1, 1]
    support279 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 815) (Fin.cases (hrows 842) (Fin.cases (hrows 812) (fun i => Fin.elim0 i))))
def support280 : Finset (Fin 154) := {14, 20, 23, 30, 33, 43, 46, 57, 59, 65, 67, 70, 75, 78, 82, 85, 96}
theorem cut280 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support280, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 878, OmissionResidual.support 576, OmissionResidual.support 900] ![OmissionResidual.demand 878, OmissionResidual.demand 576, OmissionResidual.demand 900] ![1, 1, 1]
    support280 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 878) (Fin.cases (hrows 576) (Fin.cases (hrows 900) (fun i => Fin.elim0 i))))
def support281 : Finset (Fin 154) := {21, 27, 31, 36, 41, 46, 48, 52, 58, 61, 69, 71, 73, 80, 84, 93, 112}
theorem cut281 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support281, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 585, OmissionResidual.support 730, OmissionResidual.support 580] ![OmissionResidual.demand 585, OmissionResidual.demand 730, OmissionResidual.demand 580] ![1, 1, 1]
    support281 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 585) (Fin.cases (hrows 730) (Fin.cases (hrows 580) (fun i => Fin.elim0 i))))
def support282 : Finset (Fin 154) := {28, 36, 40, 46, 48, 51, 58, 61, 63, 69, 73, 80, 81, 84, 102, 120}
theorem cut282 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support282, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 625, OmissionResidual.support 731, OmissionResidual.support 622] ![OmissionResidual.demand 625, OmissionResidual.demand 731, OmissionResidual.demand 622] ![1, 1, 1]
    support282 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 625) (Fin.cases (hrows 731) (Fin.cases (hrows 622) (fun i => Fin.elim0 i))))
def support283 : Finset (Fin 154) := {21, 27, 28, 31, 36, 38, 40, 41, 46, 47, 51, 57, 60, 63, 69, 73, 84, 93, 103}
theorem cut283 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support283, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 680, OmissionResidual.support 624, OmissionResidual.support 578] ![OmissionResidual.demand 680, OmissionResidual.demand 624, OmissionResidual.demand 578] ![1, 1, 1]
    support283 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 680) (Fin.cases (hrows 624) (Fin.cases (hrows 578) (fun i => Fin.elim0 i))))
def support284 : Finset (Fin 154) := {21, 27, 31, 39, 41, 44, 46, 51, 57, 59, 67, 70, 78, 82, 96}
theorem cut284 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support284, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 579, OmissionResidual.support 894, OmissionResidual.support 916] ![OmissionResidual.demand 579, OmissionResidual.demand 894, OmissionResidual.demand 916] ![1, 1, 1]
    support284 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 579) (Fin.cases (hrows 894) (Fin.cases (hrows 916) (fun i => Fin.elim0 i))))
def support285 : Finset (Fin 154) := {100, 108, 115, 116, 119, 122, 123, 129, 132, 133, 134, 135, 140, 143, 146, 148, 151}
theorem cut285 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support285, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1152, OmissionResidual.support 1132, OmissionResidual.support 1130] ![OmissionResidual.demand 1152, OmissionResidual.demand 1132, OmissionResidual.demand 1130] ![1, 1, 1]
    support285 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1152) (Fin.cases (hrows 1132) (Fin.cases (hrows 1130) (fun i => Fin.elim0 i))))
def support286 : Finset (Fin 154) := {2, 7, 9, 15, 16, 18, 24, 26, 27, 31, 34, 36, 39, 45, 47, 60, 66, 75}
theorem cut286 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support286, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 863, OmissionResidual.support 879, OmissionResidual.support 471] ![OmissionResidual.demand 863, OmissionResidual.demand 879, OmissionResidual.demand 471] ![1, 1, 1]
    support286 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 863) (Fin.cases (hrows 879) (Fin.cases (hrows 471) (fun i => Fin.elim0 i))))
def support287 : Finset (Fin 154) := {5, 9, 12, 15, 16, 18, 24, 26, 27, 31, 34, 36, 39, 45, 47, 60, 66, 75}
theorem cut287 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support287, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 863, OmissionResidual.support 879, OmissionResidual.support 482] ![OmissionResidual.demand 863, OmissionResidual.demand 879, OmissionResidual.demand 482] ![1, 1, 1]
    support287 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 863) (Fin.cases (hrows 879) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support288 : Finset (Fin 154) := {2, 7, 9, 15, 16, 18, 24, 26, 27, 31, 34, 36, 39, 45, 58, 71, 76, 86}
theorem cut288 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support288, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 864, OmissionResidual.support 880, OmissionResidual.support 471] ![OmissionResidual.demand 864, OmissionResidual.demand 880, OmissionResidual.demand 471] ![1, 1, 1]
    support288 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 864) (Fin.cases (hrows 880) (Fin.cases (hrows 471) (fun i => Fin.elim0 i))))
def support289 : Finset (Fin 154) := {5, 9, 12, 15, 16, 18, 24, 26, 27, 31, 34, 36, 39, 45, 58, 71, 76, 86}
theorem cut289 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support289, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 864, OmissionResidual.support 880, OmissionResidual.support 482] ![OmissionResidual.demand 864, OmissionResidual.demand 880, OmissionResidual.demand 482] ![1, 1, 1]
    support289 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 864) (Fin.cases (hrows 880) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support290 : Finset (Fin 154) := {38, 47, 51, 57, 62, 63, 69, 73, 77, 82, 84, 89, 93, 103, 116, 123}
theorem cut290 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support290, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 680, OmissionResidual.support 797] ![OmissionResidual.demand 678, OmissionResidual.demand 680, OmissionResidual.demand 797] ![1, 1, 1]
    support290 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 680) (Fin.cases (hrows 797) (fun i => Fin.elim0 i))))
def support291 : Finset (Fin 154) := {38, 47, 51, 57, 62, 63, 69, 73, 77, 82, 84, 89, 93, 103, 124, 130}
theorem cut291 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support291, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 680, OmissionResidual.support 798] ![OmissionResidual.demand 678, OmissionResidual.demand 680, OmissionResidual.demand 798] ![1, 1, 1]
    support291 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 680) (Fin.cases (hrows 798) (fun i => Fin.elim0 i))))
def support292 : Finset (Fin 154) := {38, 47, 51, 57, 63, 69, 72, 73, 82, 84, 87, 93, 99, 103, 124, 130}
theorem cut292 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support292, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 680, OmissionResidual.support 818] ![OmissionResidual.demand 678, OmissionResidual.demand 680, OmissionResidual.demand 818] ![1, 1, 1]
    support292 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 680) (Fin.cases (hrows 818) (fun i => Fin.elim0 i))))
def support293 : Finset (Fin 154) := {38, 47, 51, 57, 63, 69, 72, 73, 82, 84, 87, 93, 99, 103, 116, 123}
theorem cut293 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support293, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 678, OmissionResidual.support 680, OmissionResidual.support 816] ![OmissionResidual.demand 678, OmissionResidual.demand 680, OmissionResidual.demand 816] ![1, 1, 1]
    support293 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 678) (Fin.cases (hrows 680) (Fin.cases (hrows 816) (fun i => Fin.elim0 i))))
def support294 : Finset (Fin 154) := {29, 37, 41, 52, 57, 62, 69, 73, 77, 82, 84, 89, 93, 103, 116, 123}
theorem cut294 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support294, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 630, OmissionResidual.support 632, OmissionResidual.support 797] ![OmissionResidual.demand 630, OmissionResidual.demand 632, OmissionResidual.demand 797] ![1, 1, 1]
    support294 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 630) (Fin.cases (hrows 632) (Fin.cases (hrows 797) (fun i => Fin.elim0 i))))
def support295 : Finset (Fin 154) := {29, 37, 41, 52, 57, 62, 69, 73, 77, 82, 84, 89, 93, 103, 124, 130}
theorem cut295 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support295, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 630, OmissionResidual.support 632, OmissionResidual.support 798] ![OmissionResidual.demand 630, OmissionResidual.demand 632, OmissionResidual.demand 798] ![1, 1, 1]
    support295 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 630) (Fin.cases (hrows 632) (Fin.cases (hrows 798) (fun i => Fin.elim0 i))))
def support296 : Finset (Fin 154) := {29, 37, 41, 52, 57, 69, 72, 73, 82, 84, 87, 93, 99, 103, 116, 123}
theorem cut296 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support296, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 630, OmissionResidual.support 632, OmissionResidual.support 816] ![OmissionResidual.demand 630, OmissionResidual.demand 632, OmissionResidual.demand 816] ![1, 1, 1]
    support296 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 630) (Fin.cases (hrows 632) (Fin.cases (hrows 816) (fun i => Fin.elim0 i))))
def support297 : Finset (Fin 154) := {29, 37, 41, 52, 57, 69, 72, 73, 82, 84, 87, 93, 99, 103, 124, 130}
theorem cut297 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support297, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 630, OmissionResidual.support 632, OmissionResidual.support 818] ![OmissionResidual.demand 630, OmissionResidual.demand 632, OmissionResidual.demand 818] ![1, 1, 1]
    support297 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 630) (Fin.cases (hrows 632) (Fin.cases (hrows 818) (fun i => Fin.elim0 i))))
def support298 : Finset (Fin 154) := {63, 72, 78, 82, 83, 90, 93, 97, 102, 103, 108, 112, 117, 124, 130, 135}
theorem cut298 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support298, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 965, OmissionResidual.support 834, OmissionResidual.support 966] ![OmissionResidual.demand 965, OmissionResidual.demand 834, OmissionResidual.demand 966] ![1, 1, 1]
    support298 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 965) (Fin.cases (hrows 834) (Fin.cases (hrows 966) (fun i => Fin.elim0 i))))
def support299 : Finset (Fin 154) := {72, 82, 83, 87, 93, 97, 99, 102, 103, 108, 112, 116, 123, 124, 135}
theorem cut299 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support299, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 816, OmissionResidual.support 834, OmissionResidual.support 819] ![OmissionResidual.demand 816, OmissionResidual.demand 834, OmissionResidual.demand 819] ![1, 1, 1]
    support299 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 816) (Fin.cases (hrows 834) (Fin.cases (hrows 819) (fun i => Fin.elim0 i))))
def support300 : Finset (Fin 154) := {73, 83, 84, 88, 93, 94, 100, 102, 103, 109, 112, 117, 120, 134, 135, 144}
theorem cut300 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support300, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 969, OmissionResidual.support 968, OmissionResidual.support 459] ![OmissionResidual.demand 969, OmissionResidual.demand 968, OmissionResidual.demand 459] ![1, 1, 1]
    support300 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 969) (Fin.cases (hrows 968) (Fin.cases (hrows 459) (fun i => Fin.elim0 i))))
#print axioms cut300
def support301 : Finset (Fin 154) := {97, 105, 106, 113, 114, 121, 126, 128, 129, 132, 138, 140, 141, 148}
theorem cut301 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support301, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1138, OmissionResidual.support 1121, OmissionResidual.support 1118] ![OmissionResidual.demand 1138, OmissionResidual.demand 1121, OmissionResidual.demand 1118] ![1, 1, 1]
    support301 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1138) (Fin.cases (hrows 1121) (Fin.cases (hrows 1118) (fun i => Fin.elim0 i))))
def support302 : Finset (Fin 154) := {38, 47, 51, 57, 60, 63, 66, 70, 78, 80, 84, 88, 92, 102, 112, 113}
theorem cut302 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support302, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 681, OmissionResidual.support 948, OmissionResidual.support 928] ![OmissionResidual.demand 681, OmissionResidual.demand 948, OmissionResidual.demand 928] ![1, 1, 1]
    support302 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 681) (Fin.cases (hrows 948) (Fin.cases (hrows 928) (fun i => Fin.elim0 i))))
def support303 : Finset (Fin 154) := {15, 24, 27, 32, 34, 36, 39, 47, 49, 51, 56, 60, 72, 78, 87}
theorem cut303 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support303, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 903, OmissionResidual.support 549, OmissionResidual.support 881] ![OmissionResidual.demand 903, OmissionResidual.demand 549, OmissionResidual.demand 881] ![1, 1, 1]
    support303 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 903) (Fin.cases (hrows 549) (Fin.cases (hrows 881) (fun i => Fin.elim0 i))))
def support304 : Finset (Fin 154) := {15, 24, 27, 32, 34, 36, 39, 49, 56, 58, 61, 71, 83, 88, 97}
theorem cut304 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support304, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 882, OmissionResidual.support 904, OmissionResidual.support 550] ![OmissionResidual.demand 882, OmissionResidual.demand 904, OmissionResidual.demand 550] ![1, 1, 1]
    support304 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 882) (Fin.cases (hrows 904) (Fin.cases (hrows 550) (fun i => Fin.elim0 i))))
def support305 : Finset (Fin 154) := {8, 12, 14, 20, 27, 33, 35, 36, 43, 46, 47, 53, 55, 57, 59, 60, 64, 65, 66, 70, 74, 75, 85}
theorem cut305 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support305, holes i := by
  apply rounded_cover_cut ![support213, support254, OmissionResidual.support 875] ![2, 3, OmissionResidual.demand 875] ![1, 1, 1]
    support305 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut213 holes hbool hrows) (Fin.cases (cut254 holes hbool hrows) (Fin.cases (hrows 875) (fun i => Fin.elim0 i))))
def support306 : Finset (Fin 154) := {15, 22, 24, 27, 32, 36, 37, 42, 47, 51, 58, 60, 73, 83}
theorem cut306 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support306, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 552, OmissionResidual.support 549, OmissionResidual.support 587] ![OmissionResidual.demand 552, OmissionResidual.demand 549, OmissionResidual.demand 587] ![1, 1, 1]
    support306 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 552) (Fin.cases (hrows 549) (Fin.cases (hrows 587) (fun i => Fin.elim0 i))))
def support307 : Finset (Fin 154) := {5, 8, 10, 12, 16, 20, 21, 23, 26, 27, 31, 32, 36, 37, 40, 41, 47, 49, 50, 51, 60}
theorem cut307 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support307, holes i := by
  apply rounded_cover_cut ![support112, support245, OmissionResidual.support 512] ![2, 2, OmissionResidual.demand 512] ![1, 1, 1]
    support307 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut112 holes hbool hrows) (Fin.cases (cut245 holes hbool hrows) (Fin.cases (hrows 512) (fun i => Fin.elim0 i))))
def support308 : Finset (Fin 154) := {10, 15, 16, 20, 24, 27, 32, 36, 37, 41, 42, 47, 50, 63, 72}
theorem cut308 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support308, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 551, OmissionResidual.support 515, OmissionResidual.support 512] ![OmissionResidual.demand 551, OmissionResidual.demand 515, OmissionResidual.demand 512] ![1, 1, 1]
    support308 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 551) (Fin.cases (hrows 515) (Fin.cases (hrows 512) (fun i => Fin.elim0 i))))
def support309 : Finset (Fin 154) := {10, 16, 20, 25, 30, 32, 36, 47, 49, 51, 56, 60, 72, 78, 87}
theorem cut309 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support309, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 513, OmissionResidual.support 868, OmissionResidual.support 884] ![OmissionResidual.demand 513, OmissionResidual.demand 868, OmissionResidual.demand 884] ![1, 1, 1]
    support309 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 513) (Fin.cases (hrows 868) (Fin.cases (hrows 884) (fun i => Fin.elim0 i))))
def support310 : Finset (Fin 154) := {43, 64, 65, 74, 85, 95, 96, 105, 107, 110, 115, 118, 125, 126, 131}
theorem cut310 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support310, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1042, OmissionResidual.support 1044, OmissionResidual.support 1006] ![OmissionResidual.demand 1042, OmissionResidual.demand 1044, OmissionResidual.demand 1006] ![1, 1, 1]
    support310 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1042) (Fin.cases (hrows 1044) (Fin.cases (hrows 1006) (fun i => Fin.elim0 i))))
def support311 : Finset (Fin 154) := {5, 12, 15, 16, 24, 26, 27, 32, 36, 40, 47, 49, 51, 60}
theorem cut311 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support311, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 549, OmissionResidual.support 483, OmissionResidual.support 485] ![OmissionResidual.demand 549, OmissionResidual.demand 483, OmissionResidual.demand 485] ![1, 1, 1]
    support311 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 549) (Fin.cases (hrows 483) (Fin.cases (hrows 485) (fun i => Fin.elim0 i))))
def support312 : Finset (Fin 154) := {28, 36, 40, 46, 49, 51, 54, 59, 61, 78, 80, 88, 92, 102, 113}
theorem cut312 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support312, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 932, OmissionResidual.support 623, OmissionResidual.support 910] ![OmissionResidual.demand 932, OmissionResidual.demand 623, OmissionResidual.demand 910] ![1, 1, 1]
    support312 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 932) (Fin.cases (hrows 623) (Fin.cases (hrows 910) (fun i => Fin.elim0 i))))
def support313 : Finset (Fin 154) := {48, 58, 61, 69, 71, 73, 76, 80, 81, 84, 88, 92, 98, 106, 112, 114, 120, 121, 128, 132, 138, 144, 150}
theorem cut313 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support313, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1139, support1, support39] ![OmissionResidual.demand 1139, 3, 3] ![1, 1, 1]
    support313 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1139) (Fin.cases (cut1 holes hbool hrows) (Fin.cases (cut39 holes hbool hrows) (fun i => Fin.elim0 i))))
def support314 : Finset (Fin 154) := {22, 32, 37, 42, 45, 47, 50, 56, 58, 60, 71, 83, 84, 88, 94, 97}
theorem cut314 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support314, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 923, OmissionResidual.support 588, OmissionResidual.support 897] ![OmissionResidual.demand 923, OmissionResidual.demand 588, OmissionResidual.demand 897] ![1, 1, 1]
    support314 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 923) (Fin.cases (hrows 588) (Fin.cases (hrows 897) (fun i => Fin.elim0 i))))
def support315 : Finset (Fin 154) := {75, 85, 86, 95, 104, 105, 115, 118, 121, 126, 129, 131, 132, 141}
theorem cut315 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support315, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1095, OmissionResidual.support 1067, OmissionResidual.support 1070] ![OmissionResidual.demand 1095, OmissionResidual.demand 1067, OmissionResidual.demand 1070] ![1, 1, 1]
    support315 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1095) (Fin.cases (hrows 1067) (Fin.cases (hrows 1070) (fun i => Fin.elim0 i))))
def support316 : Finset (Fin 154) := {48, 58, 61, 69, 71, 73, 76, 80, 81, 84, 88, 92, 98, 106, 112, 114, 120, 121, 128, 132, 138, 140, 148}
theorem cut316 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support316, holes i := by
  apply rounded_cover_cut ![support1, OmissionResidual.support 1138, support39] ![3, OmissionResidual.demand 1138, 3] ![1, 1, 1]
    support316 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1 holes hbool hrows) (Fin.cases (hrows 1138) (Fin.cases (cut39 holes hbool hrows) (fun i => Fin.elim0 i))))
def support317 : Finset (Fin 154) := {10, 16, 20, 21, 27, 31, 32, 36, 37, 41, 47, 50, 51, 60}
theorem cut317 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support317, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 513, OmissionResidual.support 578, OmissionResidual.support 512] ![OmissionResidual.demand 513, OmissionResidual.demand 578, OmissionResidual.demand 512] ![1, 1, 1]
    support317 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 513) (Fin.cases (hrows 578) (Fin.cases (hrows 512) (fun i => Fin.elim0 i))))
def support318 : Finset (Fin 154) := {5, 6, 8, 10, 11, 12, 16, 20, 21, 23, 26, 27, 31, 32, 36, 37, 40, 41, 47, 49, 50, 51, 60}
theorem cut318 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support318, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 490, support112, support245] ![OmissionResidual.demand 490, 2, 2] ![1, 1, 1]
    support318 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 490) (Fin.cases (cut112 holes hbool hrows) (Fin.cases (cut245 holes hbool hrows) (fun i => Fin.elim0 i))))
def support319 : Finset (Fin 154) := {72, 82, 87, 93, 96, 99, 103, 105, 107, 114, 115, 116, 118, 123, 130, 138, 142}
theorem cut319 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support319, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1098, OmissionResidual.support 816, OmissionResidual.support 1125] ![OmissionResidual.demand 1098, OmissionResidual.demand 816, OmissionResidual.demand 1125] ![1, 1, 1]
    support319 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1098) (Fin.cases (hrows 816) (Fin.cases (hrows 1125) (fun i => Fin.elim0 i))))
def support320 : Finset (Fin 154) := {6, 10, 11, 15, 16, 20, 24, 27, 32, 36, 37, 41, 42, 47, 50, 63, 72}
theorem cut320 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support320, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 551, OmissionResidual.support 515, OmissionResidual.support 490] ![OmissionResidual.demand 551, OmissionResidual.demand 515, OmissionResidual.demand 490] ![1, 1, 1]
    support320 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 551) (Fin.cases (hrows 515) (Fin.cases (hrows 490) (fun i => Fin.elim0 i))))
def support321 : Finset (Fin 154) := {71, 81, 83, 86, 87, 92, 93, 96, 97, 102, 106, 108, 112, 113, 116, 118, 120, 121, 128, 129, 132, 134, 141}
theorem cut321 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support321, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1099, support121, support156] ![OmissionResidual.demand 1099, 2, 2] ![1, 1, 1]
    support321 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1099) (Fin.cases (cut121 holes hbool hrows) (Fin.cases (cut156 holes hbool hrows) (fun i => Fin.elim0 i))))
def support322 : Finset (Fin 154) := {10, 15, 16, 20, 24, 27, 32, 36, 37, 42, 47, 51, 52, 60, 62}
theorem cut322 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support322, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 549, OmissionResidual.support 513, OmissionResidual.support 514] ![OmissionResidual.demand 549, OmissionResidual.demand 513, OmissionResidual.demand 514] ![1, 1, 1]
    support322 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 549) (Fin.cases (hrows 513) (Fin.cases (hrows 514) (fun i => Fin.elim0 i))))
def support323 : Finset (Fin 154) := {0, 3, 4, 5, 6, 8, 10, 11, 12, 14, 17, 18, 20, 23, 24, 25, 27, 31, 33, 37, 39, 45, 50, 55, 65}
theorem cut323 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support323, holes i := by
  apply rounded_cover_cut ![support116, support117, OmissionResidual.support 0] ![3, 3, OmissionResidual.demand 0] ![1, 1, 1]
    support323 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut116 holes hbool hrows) (Fin.cases (cut117 holes hbool hrows) (Fin.cases (hrows 0) (fun i => Fin.elim0 i))))
def support324 : Finset (Fin 154) := {1, 3, 4, 5, 6, 8, 10, 11, 12, 14, 17, 18, 20, 23, 24, 25, 27, 31, 33, 37, 39, 45, 50, 55, 65}
theorem cut324 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support324, holes i := by
  apply rounded_cover_cut ![support116, support117, OmissionResidual.support 4] ![3, 3, OmissionResidual.demand 4] ![1, 1, 1]
    support324 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut116 holes hbool hrows) (Fin.cases (cut117 holes hbool hrows) (Fin.cases (hrows 4) (fun i => Fin.elim0 i))))
def support325 : Finset (Fin 154) := {0, 1, 3, 4, 5, 6, 8, 10, 11, 12, 14, 17, 18, 20, 23, 24, 25, 27, 31, 33, 37, 39, 45, 50, 55, 65}
theorem cut325 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support325, holes i := by
  apply rounded_cover_cut ![support126, support9, OmissionResidual.support 474] ![3, 3, OmissionResidual.demand 474] ![1, 1, 1]
    support325 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut126 holes hbool hrows) (Fin.cases (cut9 holes hbool hrows) (Fin.cases (hrows 474) (fun i => Fin.elim0 i))))
#print axioms cut325
def support326 : Finset (Fin 154) := {5, 8, 10, 12, 14, 16, 20, 21, 24, 25, 26, 29, 33, 36, 40, 41, 45, 47, 49, 55, 60, 66, 75}
theorem cut326 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support326, holes i := by
  apply rounded_cover_cut ![support18, OmissionResidual.support 483, support56] ![3, OmissionResidual.demand 483, 3] ![1, 1, 1]
    support326 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut18 holes hbool hrows) (Fin.cases (hrows 483) (Fin.cases (cut56 holes hbool hrows) (fun i => Fin.elim0 i))))
def support327 : Finset (Fin 154) := {5, 8, 10, 12, 13, 14, 16, 20, 21, 24, 25, 26, 29, 33, 36, 40, 41, 45, 47, 49, 55, 60, 66, 75}
theorem cut327 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support327, holes i := by
  apply rounded_cover_cut ![support18, OmissionResidual.support 483, support55] ![3, OmissionResidual.demand 483, 3] ![1, 1, 1]
    support327 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut18 holes hbool hrows) (Fin.cases (hrows 483) (Fin.cases (cut55 holes hbool hrows) (fun i => Fin.elim0 i))))
def support328 : Finset (Fin 154) := {60, 70, 71, 72, 75, 81, 82, 86, 87, 92, 93, 97, 99, 103, 105, 106, 112, 116, 121, 123, 129}
theorem cut328 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support328, holes i := by
  apply rounded_cover_cut ![support194, OmissionResidual.support 812, support260] ![2, OmissionResidual.demand 812, 2] ![1, 1, 1]
    support328 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut194 holes hbool hrows) (Fin.cases (hrows 812) (Fin.cases (cut260 holes hbool hrows) (fun i => Fin.elim0 i))))
def support329 : Finset (Fin 154) := {53, 74, 75, 85, 95, 96, 105, 107, 110, 115, 118, 125, 126, 131}
theorem cut329 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support329, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1067, OmissionResidual.support 1022, OmissionResidual.support 1021] ![OmissionResidual.demand 1067, OmissionResidual.demand 1022, OmissionResidual.demand 1021] ![1, 1, 1]
    support329 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1067) (Fin.cases (hrows 1022) (Fin.cases (hrows 1021) (fun i => Fin.elim0 i))))
def support330 : Finset (Fin 154) := {6, 11, 17, 20, 27, 30, 32, 37, 39, 41, 50, 56, 62, 67, 77}
theorem cut330 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support330, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 869, OmissionResidual.support 490, OmissionResidual.support 858] ![OmissionResidual.demand 869, OmissionResidual.demand 490, OmissionResidual.demand 858] ![1, 1, 1]
    support330 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 869) (Fin.cases (hrows 490) (Fin.cases (hrows 858) (fun i => Fin.elim0 i))))
def support331 : Finset (Fin 154) := {1, 5, 7, 9, 11, 12, 15, 16, 18, 20, 23, 24, 26, 27, 30, 31, 34, 36, 39, 45, 58, 71, 76, 86}
theorem cut331 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support331, holes i := by
  apply rounded_cover_cut ![support275, support289, OmissionResidual.support 468] ![3, 3, OmissionResidual.demand 468] ![1, 1, 1]
    support331 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut275 holes hbool hrows) (Fin.cases (cut289 holes hbool hrows) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support332 : Finset (Fin 154) := {0, 1, 5, 7, 9, 11, 12, 15, 16, 18, 20, 23, 24, 26, 27, 30, 31, 34, 36, 39, 45, 58, 71, 76, 86}
theorem cut332 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support332, holes i := by
  apply rounded_cover_cut ![support275, support289, OmissionResidual.support 466] ![3, 3, OmissionResidual.demand 466] ![1, 1, 1]
    support332 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut275 holes hbool hrows) (Fin.cases (cut289 holes hbool hrows) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support333 : Finset (Fin 154) := {0, 2, 3, 7, 9, 11, 12, 15, 16, 18, 20, 23, 24, 26, 27, 30, 31, 34, 36, 39, 45, 58, 71, 76, 86}
theorem cut333 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support333, holes i := by
  apply rounded_cover_cut ![support276, support288, OmissionResidual.support 466] ![3, 3, OmissionResidual.demand 466] ![1, 1, 1]
    support333 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut276 holes hbool hrows) (Fin.cases (cut288 holes hbool hrows) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support334 : Finset (Fin 154) := {1, 2, 3, 7, 9, 11, 12, 15, 16, 18, 20, 23, 24, 26, 27, 30, 31, 34, 36, 39, 45, 58, 71, 76, 86}
theorem cut334 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support334, holes i := by
  apply rounded_cover_cut ![support276, support288, OmissionResidual.support 468] ![3, 3, OmissionResidual.demand 468] ![1, 1, 1]
    support334 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut276 holes hbool hrows) (Fin.cases (cut288 holes hbool hrows) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support335 : Finset (Fin 154) := {5, 12, 13, 16, 18, 26, 31, 32, 37, 41, 47, 50, 51, 60}
theorem cut335 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support335, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 484, OmissionResidual.support 528, OmissionResidual.support 485] ![OmissionResidual.demand 484, OmissionResidual.demand 528, OmissionResidual.demand 485] ![1, 1, 1]
    support335 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 484) (Fin.cases (hrows 528) (Fin.cases (hrows 485) (fun i => Fin.elim0 i))))
def support336 : Finset (Fin 154) := {97, 105, 113, 116, 121, 123, 126, 128, 129, 132, 134, 138, 140, 141, 148}
theorem cut336 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support336, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1121, OmissionResidual.support 1118, OmissionResidual.support 1150] ![OmissionResidual.demand 1121, OmissionResidual.demand 1118, OmissionResidual.demand 1150] ![1, 1, 1]
    support336 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1121) (Fin.cases (hrows 1118) (Fin.cases (hrows 1150) (fun i => Fin.elim0 i))))
def support337 : Finset (Fin 154) := {20, 43, 46, 57, 60, 65, 70, 71, 75, 77, 81, 82, 85, 86, 87, 92, 96, 97, 102, 103, 106, 112, 113, 114, 121}
theorem cut337 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support337, holes i := by
  apply rounded_cover_cut ![support145, OmissionResidual.support 812, support144] ![2, OmissionResidual.demand 812, 2] ![1, 1, 1]
    support337 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut145 holes hbool hrows) (Fin.cases (hrows 812) (Fin.cases (cut144 holes hbool hrows) (fun i => Fin.elim0 i))))
def support338 : Finset (Fin 154) := {2, 7, 9, 10, 16, 18, 20, 24, 26, 32, 36, 40, 47, 49, 51, 60}
theorem cut338 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support338, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 472, OmissionResidual.support 506, OmissionResidual.support 513] ![OmissionResidual.demand 472, OmissionResidual.demand 506, OmissionResidual.demand 513] ![1, 1, 1]
    support338 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 472) (Fin.cases (hrows 506) (Fin.cases (hrows 513) (fun i => Fin.elim0 i))))
def support339 : Finset (Fin 154) := {73, 83, 84, 88, 93, 94, 100, 102, 103, 109, 112, 117, 120, 124, 129, 130, 134, 135, 138, 140, 143, 144, 153}
theorem cut339 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support339, holes i := by
  apply rounded_cover_cut ![support218, OmissionResidual.support 1160, support300] ![3, OmissionResidual.demand 1160, 3] ![1, 1, 1]
    support339 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut218 holes hbool hrows) (Fin.cases (hrows 1160) (Fin.cases (cut300 holes hbool hrows) (fun i => Fin.elim0 i))))
def support340 : Finset (Fin 154) := {38, 47, 51, 57, 60, 63, 66, 69, 70, 78, 81, 84, 88, 93, 103, 105}
theorem cut340 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support340, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 680, OmissionResidual.support 927, OmissionResidual.support 947] ![OmissionResidual.demand 680, OmissionResidual.demand 927, OmissionResidual.demand 947] ![1, 1, 1]
    support340 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 680) (Fin.cases (hrows 927) (Fin.cases (hrows 947) (fun i => Fin.elim0 i))))
def support341 : Finset (Fin 154) := {64, 74, 86, 87, 95, 96, 104, 113, 118, 121, 122, 126, 129, 132, 136, 141}
theorem cut341 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support341, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1043, OmissionResidual.support 1095, OmissionResidual.support 1099] ![OmissionResidual.demand 1043, OmissionResidual.demand 1095, OmissionResidual.demand 1099] ![1, 1, 1]
    support341 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1043) (Fin.cases (hrows 1095) (Fin.cases (hrows 1099) (fun i => Fin.elim0 i))))
def support342 : Finset (Fin 154) := {87, 96, 97, 105, 113, 114, 118, 121, 126, 129, 130, 132, 138, 141, 142}
theorem cut342 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support342, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1098, OmissionResidual.support 1099, OmissionResidual.support 1118] ![OmissionResidual.demand 1098, OmissionResidual.demand 1099, OmissionResidual.demand 1118] ![1, 1, 1]
    support342 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1098) (Fin.cases (hrows 1099) (Fin.cases (hrows 1118) (fun i => Fin.elim0 i))))
def support343 : Finset (Fin 154) := {1, 5, 7, 9, 11, 12, 15, 16, 18, 20, 23, 24, 26, 27, 30, 31, 34, 36, 39, 45, 47, 60, 66, 75}
theorem cut343 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support343, holes i := by
  apply rounded_cover_cut ![support273, support287, OmissionResidual.support 468] ![3, 3, OmissionResidual.demand 468] ![1, 1, 1]
    support343 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut273 holes hbool hrows) (Fin.cases (cut287 holes hbool hrows) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support344 : Finset (Fin 154) := {0, 1, 5, 7, 9, 11, 12, 15, 16, 18, 20, 23, 24, 26, 27, 30, 31, 34, 36, 39, 45, 47, 60, 66, 75}
theorem cut344 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support344, holes i := by
  apply rounded_cover_cut ![support273, support287, OmissionResidual.support 466] ![3, 3, OmissionResidual.demand 466] ![1, 1, 1]
    support344 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut273 holes hbool hrows) (Fin.cases (cut287 holes hbool hrows) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support345 : Finset (Fin 154) := {0, 2, 3, 7, 9, 11, 12, 15, 16, 18, 20, 23, 24, 26, 27, 30, 31, 34, 36, 39, 45, 47, 60, 66, 75}
theorem cut345 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support345, holes i := by
  apply rounded_cover_cut ![support274, support286, OmissionResidual.support 466] ![3, 3, OmissionResidual.demand 466] ![1, 1, 1]
    support345 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut274 holes hbool hrows) (Fin.cases (cut286 holes hbool hrows) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support346 : Finset (Fin 154) := {1, 2, 3, 7, 9, 11, 12, 15, 16, 18, 20, 23, 24, 26, 27, 30, 31, 34, 36, 39, 45, 47, 60, 66, 75}
theorem cut346 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support346, holes i := by
  apply rounded_cover_cut ![support274, support286, OmissionResidual.support 468] ![3, 3, OmissionResidual.demand 468] ![1, 1, 1]
    support346 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut274 holes hbool hrows) (Fin.cases (cut286 holes hbool hrows) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support347 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 98, 106, 112, 114, 120, 121, 128, 132, 138, 144, 150}
theorem cut347 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support347, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1139, OmissionResidual.support 959, OmissionResidual.support 960] ![OmissionResidual.demand 1139, OmissionResidual.demand 959, OmissionResidual.demand 960] ![1, 1, 1]
    support347 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1139) (Fin.cases (hrows 959) (Fin.cases (hrows 960) (fun i => Fin.elim0 i))))
def support348 : Finset (Fin 154) := {4, 7, 19, 23, 26, 28, 31, 35, 36, 40, 46, 54, 59, 66, 76, 80, 92, 104}
theorem cut348 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support348, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 479, OmissionResidual.support 888, OmissionResidual.support 908] ![OmissionResidual.demand 479, OmissionResidual.demand 888, OmissionResidual.demand 908] ![1, 1, 1]
    support348 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 479) (Fin.cases (hrows 888) (Fin.cases (hrows 908) (fun i => Fin.elim0 i))))
def support349 : Finset (Fin 154) := {7, 19, 26, 28, 35, 36, 43, 46, 53, 54, 59, 64, 66, 74, 76, 80, 92, 104}
theorem cut349 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support349, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 494, OmissionResidual.support 888, OmissionResidual.support 908] ![OmissionResidual.demand 494, OmissionResidual.demand 888, OmissionResidual.demand 908] ![1, 1, 1]
    support349 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 494) (Fin.cases (hrows 888) (Fin.cases (hrows 908) (fun i => Fin.elim0 i))))
def support350 : Finset (Fin 154) := {2, 5, 7, 8, 12, 13, 16, 18, 23, 24, 26, 27, 31, 35, 36, 39, 40, 41, 49, 51, 57, 70}
theorem cut350 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support350, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 472, support247, support109] ![OmissionResidual.demand 472, 2, 2] ![1, 1, 1]
    support350 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 472) (Fin.cases (cut247 holes hbool hrows) (Fin.cases (cut109 holes hbool hrows) (fun i => Fin.elim0 i))))
#print axioms cut350
def support351 : Finset (Fin 154) := {20, 32, 43, 46, 50, 57, 60, 65, 70, 71, 75, 77, 81, 82, 85, 87, 91, 94, 96, 103, 106, 114, 127, 132}
theorem cut351 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support351, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 991, support203, support145] ![OmissionResidual.demand 991, 2, 2] ![1, 1, 1]
    support351 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 991) (Fin.cases (cut203 holes hbool hrows) (Fin.cases (cut145 holes hbool hrows) (fun i => Fin.elim0 i))))
def support352 : Finset (Fin 154) := {20, 43, 46, 57, 60, 65, 70, 71, 75, 77, 81, 82, 85, 86, 87, 92, 96, 97, 102, 103, 106, 113, 114, 120, 128}
theorem cut352 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support352, holes i := by
  apply rounded_cover_cut ![support145, support144, OmissionResidual.support 813] ![2, 2, OmissionResidual.demand 813] ![1, 1, 1]
    support352 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut145 holes hbool hrows) (Fin.cases (cut144 holes hbool hrows) (Fin.cases (hrows 813) (fun i => Fin.elim0 i))))
def support353 : Finset (Fin 154) := {87, 96, 108, 113, 115, 118, 121, 122, 126, 129, 132, 135, 138, 141, 146}
theorem cut353 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support353, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1099, OmissionResidual.support 1100, OmissionResidual.support 1140] ![OmissionResidual.demand 1099, OmissionResidual.demand 1100, OmissionResidual.demand 1140] ![1, 1, 1]
    support353 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1099) (Fin.cases (hrows 1100) (Fin.cases (hrows 1140) (fun i => Fin.elim0 i))))
def support354 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 98, 106, 112, 114, 120, 121, 128, 132, 138, 140, 148}
theorem cut354 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support354, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 959, OmissionResidual.support 1138, OmissionResidual.support 960] ![OmissionResidual.demand 959, OmissionResidual.demand 1138, OmissionResidual.demand 960] ![1, 1, 1]
    support354 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 959) (Fin.cases (hrows 1138) (Fin.cases (hrows 960) (fun i => Fin.elim0 i))))
def support355 : Finset (Fin 154) := {6, 11, 14, 15, 20, 23, 24, 27, 32, 36, 37, 41, 47, 50, 51, 60}
theorem cut355 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support355, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 549, OmissionResidual.support 490, OmissionResidual.support 539] ![OmissionResidual.demand 549, OmissionResidual.demand 490, OmissionResidual.demand 539] ![1, 1, 1]
    support355 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 549) (Fin.cases (hrows 490) (Fin.cases (hrows 539) (fun i => Fin.elim0 i))))
def support356 : Finset (Fin 154) := {53, 64, 65, 74, 85, 95, 96, 105, 107, 110, 115, 118, 125, 126, 131}
theorem cut356 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support356, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1042, OmissionResidual.support 1044, OmissionResidual.support 1021] ![OmissionResidual.demand 1042, OmissionResidual.demand 1044, OmissionResidual.demand 1021] ![1, 1, 1]
    support356 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1042) (Fin.cases (hrows 1044) (Fin.cases (hrows 1021) (fun i => Fin.elim0 i))))
def support357 : Finset (Fin 154) := {38, 47, 51, 57, 60, 63, 66, 69, 70, 78, 84, 88, 92, 93, 102, 103, 105, 113}
theorem cut357 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support357, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 680, OmissionResidual.support 948, OmissionResidual.support 927] ![OmissionResidual.demand 680, OmissionResidual.demand 948, OmissionResidual.demand 927] ![1, 1, 1]
    support357 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 680) (Fin.cases (hrows 948) (Fin.cases (hrows 927) (fun i => Fin.elim0 i))))
def support358 : Finset (Fin 154) := {52, 62, 67, 72, 79, 82, 83, 87, 93, 94, 99, 103, 117, 124, 130}
theorem cut358 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support358, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 958, OmissionResidual.support 818, OmissionResidual.support 957] ![OmissionResidual.demand 958, OmissionResidual.demand 818, OmissionResidual.demand 957] ![1, 1, 1]
    support358 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 958) (Fin.cases (hrows 818) (Fin.cases (hrows 957) (fun i => Fin.elim0 i))))
def support359 : Finset (Fin 154) := {39, 53, 59, 60, 70, 75, 81, 82, 89, 93, 99, 107, 108, 115}
theorem cut359 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support359, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 693, OmissionResidual.support 692, OmissionResidual.support 782] ![OmissionResidual.demand 693, OmissionResidual.demand 692, OmissionResidual.demand 782] ![1, 1, 1]
    support359 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 693) (Fin.cases (hrows 692) (Fin.cases (hrows 782) (fun i => Fin.elim0 i))))
def support360 : Finset (Fin 154) := {39, 50, 53, 59, 65, 70, 77, 81, 82, 87, 89, 93, 96, 108, 115}
theorem cut360 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support360, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 742, OmissionResidual.support 693, OmissionResidual.support 690] ![OmissionResidual.demand 742, OmissionResidual.demand 693, OmissionResidual.demand 690] ![1, 1, 1]
    support360 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 742) (Fin.cases (hrows 693) (Fin.cases (hrows 690) (fun i => Fin.elim0 i))))
def support361 : Finset (Fin 154) := {52, 62, 67, 72, 79, 82, 83, 87, 93, 94, 99, 103, 109, 116, 123}
theorem cut361 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support361, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 956, OmissionResidual.support 816, OmissionResidual.support 955] ![OmissionResidual.demand 956, OmissionResidual.demand 816, OmissionResidual.demand 955] ![1, 1, 1]
    support361 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 956) (Fin.cases (hrows 816) (Fin.cases (hrows 955) (fun i => Fin.elim0 i))))
def support362 : Finset (Fin 154) := {41, 50, 55, 60, 70, 71, 75, 79, 81, 83, 93, 99, 100, 108, 115}
theorem cut362 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support362, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 939, OmissionResidual.support 940, OmissionResidual.support 782] ![OmissionResidual.demand 939, OmissionResidual.demand 940, OmissionResidual.demand 782] ![1, 1, 1]
    support362 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 939) (Fin.cases (hrows 940) (Fin.cases (hrows 782) (fun i => Fin.elim0 i))))
def support363 : Finset (Fin 154) := {63, 72, 78, 82, 90, 93, 102, 103, 109, 112, 116, 123, 129, 132, 134, 143, 144, 152}
theorem cut363 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support363, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 963, OmissionResidual.support 964, OmissionResidual.support 1153] ![OmissionResidual.demand 963, OmissionResidual.demand 964, OmissionResidual.demand 1153] ![1, 1, 1]
    support363 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 963) (Fin.cases (hrows 964) (Fin.cases (hrows 1153) (fun i => Fin.elim0 i))))
def support364 : Finset (Fin 154) := {13, 18, 28, 31, 35, 36, 40, 41, 46, 51, 57, 61, 69, 70, 81}
theorem cut364 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support364, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 529, OmissionResidual.support 531, OmissionResidual.support 622] ![OmissionResidual.demand 529, OmissionResidual.demand 531, OmissionResidual.demand 622] ![1, 1, 1]
    support364 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 529) (Fin.cases (hrows 531) (Fin.cases (hrows 622) (fun i => Fin.elim0 i))))
def support365 : Finset (Fin 154) := {29, 37, 41, 50, 52, 55, 57, 67, 69, 70, 81, 84, 88, 93, 103, 105}
theorem cut365 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support365, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 632, OmissionResidual.support 912, OmissionResidual.support 936] ![OmissionResidual.demand 632, OmissionResidual.demand 912, OmissionResidual.demand 936] ![1, 1, 1]
    support365 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 632) (Fin.cases (hrows 912) (Fin.cases (hrows 936) (fun i => Fin.elim0 i))))
def support366 : Finset (Fin 154) := {19, 21, 26, 27, 28, 31, 35, 36, 38, 40, 46, 47, 51, 52, 57, 61, 63, 69, 72, 73, 80, 92, 93}
theorem cut366 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support366, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, support80, support266] ![OmissionResidual.demand 572, 2, 2] ![1, 1, 1]
    support366 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (cut80 holes hbool hrows) (Fin.cases (cut266 holes hbool hrows) (fun i => Fin.elim0 i))))
def support367 : Finset (Fin 154) := {63, 72, 78, 82, 90, 93, 102, 103, 112, 117, 124, 130, 135, 138, 140, 143, 144, 152}
theorem cut367 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support367, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 966, OmissionResidual.support 1159, OmissionResidual.support 965] ![OmissionResidual.demand 966, OmissionResidual.demand 1159, OmissionResidual.demand 965] ![1, 1, 1]
    support367 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 966) (Fin.cases (hrows 1159) (Fin.cases (hrows 965) (fun i => Fin.elim0 i))))
def support368 : Finset (Fin 154) := {63, 72, 78, 82, 90, 93, 102, 103, 112, 117, 124, 130, 135, 138, 140, 143, 144, 153}
theorem cut368 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support368, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 966, OmissionResidual.support 1160, OmissionResidual.support 965] ![OmissionResidual.demand 966, OmissionResidual.demand 1160, OmissionResidual.demand 965] ![1, 1, 1]
    support368 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 966) (Fin.cases (hrows 1160) (Fin.cases (hrows 965) (fun i => Fin.elim0 i))))
def support369 : Finset (Fin 154) := {60, 70, 71, 75, 81, 86, 87, 92, 93, 97, 105, 106, 112, 121}
theorem cut369 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support369, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 781, OmissionResidual.support 812, OmissionResidual.support 778] ![OmissionResidual.demand 781, OmissionResidual.demand 812, OmissionResidual.demand 778] ![1, 1, 1]
    support369 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 781) (Fin.cases (hrows 812) (Fin.cases (hrows 778) (fun i => Fin.elim0 i))))
def support370 : Finset (Fin 154) := {15, 19, 21, 24, 26, 27, 28, 31, 35, 36, 38, 40, 42, 46, 47, 51, 52, 57, 61, 63, 69, 72, 73, 80, 92, 93}
theorem cut370 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support370, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, support206, support266] ![OmissionResidual.demand 572, 2, 2] ![1, 1, 1]
    support370 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (cut206 holes hbool hrows) (Fin.cases (cut266 holes hbool hrows) (fun i => Fin.elim0 i))))
def support371 : Finset (Fin 154) := {21, 22, 27, 28, 31, 32, 36, 37, 40, 42, 46, 47, 52, 57, 58, 63, 69, 72, 73, 82, 83, 84, 93, 94}
theorem cut371 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support371, holes i := by
  apply rounded_cover_cut ![support80, support205, OmissionResidual.support 588] ![2, 2, OmissionResidual.demand 588] ![1, 1, 1]
    support371 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut80 holes hbool hrows) (Fin.cases (cut205 holes hbool hrows) (Fin.cases (hrows 588) (fun i => Fin.elim0 i))))
def support372 : Finset (Fin 154) := {28, 36, 40, 46, 48, 51, 58, 61, 63, 69, 73, 80, 84, 92, 93, 120}
theorem cut372 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support372, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 624, OmissionResidual.support 623, OmissionResidual.support 731] ![OmissionResidual.demand 624, OmissionResidual.demand 623, OmissionResidual.demand 731] ![1, 1, 1]
    support372 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 624) (Fin.cases (hrows 623) (Fin.cases (hrows 731) (fun i => Fin.elim0 i))))
def support373 : Finset (Fin 154) := {61, 71, 76, 81, 92, 100, 109, 112, 116, 120, 123, 129, 132, 134, 143, 144, 152}
theorem cut373 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support373, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 962, OmissionResidual.support 1153, OmissionResidual.support 961] ![OmissionResidual.demand 962, OmissionResidual.demand 1153, OmissionResidual.demand 961] ![1, 1, 1]
    support373 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 962) (Fin.cases (hrows 1153) (Fin.cases (hrows 961) (fun i => Fin.elim0 i))))
def support374 : Finset (Fin 154) := {73, 83, 88, 93, 100, 102, 109, 112, 116, 120, 123, 129, 132, 134, 143, 144, 152}
theorem cut374 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support374, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 968, OmissionResidual.support 1153, OmissionResidual.support 967] ![OmissionResidual.demand 968, OmissionResidual.demand 1153, OmissionResidual.demand 967] ![1, 1, 1]
    support374 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 968) (Fin.cases (hrows 1153) (Fin.cases (hrows 967) (fun i => Fin.elim0 i))))
def support375 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 61, 63, 69, 72, 73, 80, 82, 84, 87, 93, 99, 102, 103, 112, 124, 130}
theorem cut375 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support375, holes i := by
  apply rounded_cover_cut ![support47, OmissionResidual.support 818, support59] ![2, OmissionResidual.demand 818, 2] ![1, 1, 1]
    support375 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut47 holes hbool hrows) (Fin.cases (hrows 818) (Fin.cases (cut59 holes hbool hrows) (fun i => Fin.elim0 i))))
#print axioms cut375
def support376 : Finset (Fin 154) := {28, 36, 38, 40, 46, 47, 51, 57, 61, 63, 69, 73, 80, 92, 93}
theorem cut376 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support376, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 624, OmissionResidual.support 623, OmissionResidual.support 678] ![OmissionResidual.demand 624, OmissionResidual.demand 623, OmissionResidual.demand 678] ![1, 1, 1]
    support376 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 624) (Fin.cases (hrows 623) (Fin.cases (hrows 678) (fun i => Fin.elim0 i))))
def support377 : Finset (Fin 154) := {19, 21, 26, 27, 28, 31, 35, 36, 38, 40, 46, 47, 51, 52, 57, 61, 63, 69, 72, 73, 80, 82, 92, 93}
theorem cut377 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support377, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, support40, support80] ![OmissionResidual.demand 572, 2, 2] ![1, 1, 1]
    support377 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (cut40 holes hbool hrows) (Fin.cases (cut80 holes hbool hrows) (fun i => Fin.elim0 i))))
def support378 : Finset (Fin 154) := {22, 28, 32, 36, 37, 38, 40, 42, 46, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 84, 92, 93, 94, 120}
theorem cut378 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support378, holes i := by
  apply rounded_cover_cut ![support376, support372, OmissionResidual.support 588] ![2, 2, OmissionResidual.demand 588] ![1, 1, 1]
    support378 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut376 holes hbool hrows) (Fin.cases (cut372 holes hbool hrows) (Fin.cases (hrows 588) (fun i => Fin.elim0 i))))
def support379 : Finset (Fin 154) := {22, 28, 32, 36, 37, 38, 40, 42, 46, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 84, 92, 93, 94, 112}
theorem cut379 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support379, holes i := by
  apply rounded_cover_cut ![support376, OmissionResidual.support 588, support161] ![2, OmissionResidual.demand 588, 2] ![1, 1, 1]
    support379 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut376 holes hbool hrows) (Fin.cases (hrows 588) (Fin.cases (cut161 holes hbool hrows) (fun i => Fin.elim0 i))))
def support380 : Finset (Fin 154) := {28, 29, 36, 37, 38, 40, 41, 46, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 84, 92, 93, 94, 120}
theorem cut380 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support380, holes i := by
  apply rounded_cover_cut ![support376, support372, OmissionResidual.support 631] ![2, 2, OmissionResidual.demand 631] ![1, 1, 1]
    support380 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut376 holes hbool hrows) (Fin.cases (cut372 holes hbool hrows) (Fin.cases (hrows 631) (fun i => Fin.elim0 i))))
def support381 : Finset (Fin 154) := {28, 29, 36, 37, 38, 40, 41, 46, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 84, 92, 93, 94, 112}
theorem cut381 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support381, holes i := by
  apply rounded_cover_cut ![support376, support161, OmissionResidual.support 631] ![2, 2, OmissionResidual.demand 631] ![1, 1, 1]
    support381 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut376 holes hbool hrows) (Fin.cases (cut161 holes hbool hrows) (Fin.cases (hrows 631) (fun i => Fin.elim0 i))))
def support382 : Finset (Fin 154) := {22, 28, 32, 36, 37, 38, 40, 42, 46, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 81, 84, 92, 93, 94, 102, 120}
theorem cut382 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support382, holes i := by
  apply rounded_cover_cut ![support376, OmissionResidual.support 588, support282] ![2, OmissionResidual.demand 588, 2] ![1, 1, 1]
    support382 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut376 holes hbool hrows) (Fin.cases (hrows 588) (Fin.cases (cut282 holes hbool hrows) (fun i => Fin.elim0 i))))
def support383 : Finset (Fin 154) := {21, 27, 28, 31, 36, 38, 40, 41, 46, 47, 51, 52, 57, 58, 61, 63, 69, 71, 73, 80, 82, 92, 93}
theorem cut383 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support383, holes i := by
  apply rounded_cover_cut ![support376, support40, OmissionResidual.support 580] ![2, 2, OmissionResidual.demand 580] ![1, 1, 1]
    support383 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut376 holes hbool hrows) (Fin.cases (cut40 holes hbool hrows) (Fin.cases (hrows 580) (fun i => Fin.elim0 i))))
def support384 : Finset (Fin 154) := {15, 21, 24, 27, 28, 31, 32, 36, 38, 40, 46, 47, 51, 52, 57, 58, 61, 63, 69, 71, 73, 80, 82, 92, 93}
theorem cut384 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support384, holes i := by
  apply rounded_cover_cut ![support376, support40, OmissionResidual.support 550] ![2, 2, OmissionResidual.demand 550] ![1, 1, 1]
    support384 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut376 holes hbool hrows) (Fin.cases (cut40 holes hbool hrows) (Fin.cases (hrows 550) (fun i => Fin.elim0 i))))
def support385 : Finset (Fin 154) := {75, 85, 97, 104, 105, 113, 118, 121, 122, 126, 129, 132, 136, 141}
theorem cut385 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support385, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1070, OmissionResidual.support 1118, OmissionResidual.support 1069] ![OmissionResidual.demand 1070, OmissionResidual.demand 1118, OmissionResidual.demand 1069] ![1, 1, 1]
    support385 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1070) (Fin.cases (hrows 1118) (Fin.cases (hrows 1069) (fun i => Fin.elim0 i))))
def support386 : Finset (Fin 154) := {29, 37, 41, 50, 55, 57, 60, 65, 67, 69, 71, 77, 94, 98, 103, 106, 114}
theorem cut386 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support386, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 937, OmissionResidual.support 914, OmissionResidual.support 677] ![OmissionResidual.demand 937, OmissionResidual.demand 914, OmissionResidual.demand 677] ![1, 1, 1]
    support386 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 937) (Fin.cases (hrows 914) (Fin.cases (hrows 677) (fun i => Fin.elim0 i))))
def support387 : Finset (Fin 154) := {22, 28, 32, 36, 37, 38, 40, 42, 46, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 81, 84, 92, 93, 94, 102, 112}
theorem cut387 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support387, holes i := by
  apply rounded_cover_cut ![support376, OmissionResidual.support 588, support123] ![2, OmissionResidual.demand 588, 2] ![1, 1, 1]
    support387 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut376 holes hbool hrows) (Fin.cases (hrows 588) (Fin.cases (cut123 holes hbool hrows) (fun i => Fin.elim0 i))))
def support388 : Finset (Fin 154) := {28, 36, 40, 46, 48, 51, 58, 61, 63, 69, 73, 80, 84, 92, 93, 94, 103, 106, 112, 116, 120, 124, 140}
theorem cut388 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support388, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 842, support372, support161] ![OmissionResidual.demand 842, 2, 2] ![1, 1, 1]
    support388 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 842) (Fin.cases (cut372 holes hbool hrows) (Fin.cases (cut161 holes hbool hrows) (fun i => Fin.elim0 i))))
def support389 : Finset (Fin 154) := {28, 36, 40, 46, 48, 51, 58, 61, 63, 69, 73, 80, 84, 92, 93, 94, 103, 106, 112, 116, 120, 124, 144}
theorem cut389 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support389, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 843, support372, support161] ![OmissionResidual.demand 843, 2, 2] ![1, 1, 1]
    support389 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 843) (Fin.cases (cut372 holes hbool hrows) (Fin.cases (cut161 holes hbool hrows) (fun i => Fin.elim0 i))))
def support390 : Finset (Fin 154) := {6, 11, 14, 15, 20, 23, 24, 27, 36, 37, 42, 47, 52, 62, 63, 72}
theorem cut390 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support390, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 551, OmissionResidual.support 491, OmissionResidual.support 541] ![OmissionResidual.demand 551, OmissionResidual.demand 491, OmissionResidual.demand 541] ![1, 1, 1]
    support390 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 551) (Fin.cases (hrows 491) (Fin.cases (hrows 541) (fun i => Fin.elim0 i))))
def support391 : Finset (Fin 154) := {4, 6, 7, 10, 11, 14, 15, 16, 20, 21, 23, 24, 27, 31, 35, 36, 37, 40, 42, 46, 47, 52, 59, 62, 63, 72}
theorem cut391 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support391, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 479, support192, support390] ![OmissionResidual.demand 479, 2, 2] ![1, 1, 1]
    support391 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 479) (Fin.cases (cut192 holes hbool hrows) (Fin.cases (cut390 holes hbool hrows) (fun i => Fin.elim0 i))))
def support392 : Finset (Fin 154) := {26, 35, 53, 64, 65, 74, 75, 80, 85, 86, 92, 95, 96, 104, 105, 107, 110, 115, 118, 125, 126, 131}
theorem cut392 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support392, holes i := by
  apply rounded_cover_cut ![support329, support356, OmissionResidual.support 617] ![2, 2, OmissionResidual.demand 617] ![1, 1, 1]
    support392 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut329 holes hbool hrows) (Fin.cases (cut356 holes hbool hrows) (Fin.cases (hrows 617) (fun i => Fin.elim0 i))))
def support393 : Finset (Fin 154) := {4, 7, 13, 14, 18, 20, 23, 31, 35, 40, 41, 46, 51, 57, 59, 70}
theorem cut393 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support393, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 479, OmissionResidual.support 529, OmissionResidual.support 540] ![OmissionResidual.demand 479, OmissionResidual.demand 529, OmissionResidual.demand 540] ![1, 1, 1]
    support393 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 479) (Fin.cases (hrows 529) (Fin.cases (hrows 540) (fun i => Fin.elim0 i))))
def support394 : Finset (Fin 154) := {36, 46, 53, 64, 65, 74, 75, 80, 85, 86, 92, 95, 96, 104, 105, 107, 110, 115, 118, 125, 126, 131}
theorem cut394 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support394, holes i := by
  apply rounded_cover_cut ![support329, support356, OmissionResidual.support 673] ![2, 2, OmissionResidual.demand 673] ![1, 1, 1]
    support394 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut329 holes hbool hrows) (Fin.cases (cut356 holes hbool hrows) (Fin.cases (hrows 673) (fun i => Fin.elim0 i))))
def support395 : Finset (Fin 154) := {3, 5, 6, 10, 12, 15, 16, 17, 18, 20, 24, 27, 31, 36, 37, 39, 42, 45, 47, 50, 55, 63, 65, 72}
theorem cut395 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support395, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 850, OmissionResidual.support 515, OmissionResidual.support 551, support120] ![OmissionResidual.demand 850, OmissionResidual.demand 515, OmissionResidual.demand 551, 3] ![1, 1, 1, 1]
    support395 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 850) (Fin.cases (hrows 515) (Fin.cases (hrows 551) (Fin.cases (cut120 holes hbool hrows) (fun i => Fin.elim0 i)))))
def support396 : Finset (Fin 154) := {66, 75, 85, 86, 95, 104, 111, 114, 121, 123, 126, 127, 129, 132, 137, 141}
theorem cut396 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support396, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1047, OmissionResidual.support 1049, OmissionResidual.support 1095] ![OmissionResidual.demand 1047, OmissionResidual.demand 1049, OmissionResidual.demand 1095] ![1, 1, 1]
    support396 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1047) (Fin.cases (hrows 1049) (Fin.cases (hrows 1095) (fun i => Fin.elim0 i))))
def support397 : Finset (Fin 154) := {79, 89, 99, 101, 107, 108, 115, 116, 118, 123, 124, 130, 139, 143, 147}
theorem cut397 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support397, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1090, OmissionResidual.support 1126, OmissionResidual.support 1086] ![OmissionResidual.demand 1090, OmissionResidual.demand 1126, OmissionResidual.demand 1086] ![1, 1, 1]
    support397 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1090) (Fin.cases (hrows 1126) (Fin.cases (hrows 1086) (fun i => Fin.elim0 i))))
def support398 : Finset (Fin 154) := {30, 31, 39, 43, 44, 49, 59, 60, 70, 72, 79, 82, 89, 90, 99, 107}
theorem cut398 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support398, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 640, OmissionResidual.support 920, OmissionResidual.support 919] ![OmissionResidual.demand 640, OmissionResidual.demand 920, OmissionResidual.demand 919] ![1, 1, 1]
    support398 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 640) (Fin.cases (hrows 920) (Fin.cases (hrows 919) (fun i => Fin.elim0 i))))
def support399 : Finset (Fin 154) := {1, 7, 9, 11, 18, 21, 24, 26, 27, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut399 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support399, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 507, OmissionResidual.support 469, OmissionResidual.support 580] ![OmissionResidual.demand 507, OmissionResidual.demand 469, OmissionResidual.demand 580] ![1, 1, 1]
    support399 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 507) (Fin.cases (hrows 469) (Fin.cases (hrows 580) (fun i => Fin.elim0 i))))
def support400 : Finset (Fin 154) := {1, 7, 11, 13, 15, 18, 24, 26, 27, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut400 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support400, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 469, OmissionResidual.support 530, OmissionResidual.support 550] ![OmissionResidual.demand 469, OmissionResidual.demand 530, OmissionResidual.demand 550] ![1, 1, 1]
    support400 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 469) (Fin.cases (hrows 530) (Fin.cases (hrows 550) (fun i => Fin.elim0 i))))
#print axioms cut400
def support401 : Finset (Fin 154) := {71, 81, 86, 92, 94, 97, 103, 106, 108, 112, 116, 120, 121, 124, 134, 144}
theorem cut401 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support401, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 843, OmissionResidual.support 815, OmissionResidual.support 812] ![OmissionResidual.demand 843, OmissionResidual.demand 815, OmissionResidual.demand 812] ![1, 1, 1]
    support401 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 843) (Fin.cases (hrows 815) (Fin.cases (hrows 812) (fun i => Fin.elim0 i))))
def support : Fin 402 → Finset (Fin 154) := ![support0, support1, support2, support3, support4, support5, support6, support7, support8, support9, support10, support11, support12, support13, support14, support15, support16, support17, support18, support19, support20, support21, support22, support23, support24, support25, support26, support27, support28, support29, support30, support31, support32, support33, support34, support35, support36, support37, support38, support39, support40, support41, support42, support43, support44, support45, support46, support47, support48, support49, support50, support51, support52, support53, support54, support55, support56, support57, support58, support59, support60, support61, support62, support63, support64, support65, support66, support67, support68, support69, support70, support71, support72, support73, support74, support75, support76, support77, support78, support79, support80, support81, support82, support83, support84, support85, support86, support87, support88, support89, support90, support91, support92, support93, support94, support95, support96, support97, support98, support99, support100, support101, support102, support103, support104, support105, support106, support107, support108, support109, support110, support111, support112, support113, support114, support115, support116, support117, support118, support119, support120, support121, support122, support123, support124, support125, support126, support127, support128, support129, support130, support131, support132, support133, support134, support135, support136, support137, support138, support139, support140, support141, support142, support143, support144, support145, support146, support147, support148, support149, support150, support151, support152, support153, support154, support155, support156, support157, support158, support159, support160, support161, support162, support163, support164, support165, support166, support167, support168, support169, support170, support171, support172, support173, support174, support175, support176, support177, support178, support179, support180, support181, support182, support183, support184, support185, support186, support187, support188, support189, support190, support191, support192, support193, support194, support195, support196, support197, support198, support199, support200, support201, support202, support203, support204, support205, support206, support207, support208, support209, support210, support211, support212, support213, support214, support215, support216, support217, support218, support219, support220, support221, support222, support223, support224, support225, support226, support227, support228, support229, support230, support231, support232, support233, support234, support235, support236, support237, support238, support239, support240, support241, support242, support243, support244, support245, support246, support247, support248, support249, support250, support251, support252, support253, support254, support255, support256, support257, support258, support259, support260, support261, support262, support263, support264, support265, support266, support267, support268, support269, support270, support271, support272, support273, support274, support275, support276, support277, support278, support279, support280, support281, support282, support283, support284, support285, support286, support287, support288, support289, support290, support291, support292, support293, support294, support295, support296, support297, support298, support299, support300, support301, support302, support303, support304, support305, support306, support307, support308, support309, support310, support311, support312, support313, support314, support315, support316, support317, support318, support319, support320, support321, support322, support323, support324, support325, support326, support327, support328, support329, support330, support331, support332, support333, support334, support335, support336, support337, support338, support339, support340, support341, support342, support343, support344, support345, support346, support347, support348, support349, support350, support351, support352, support353, support354, support355, support356, support357, support358, support359, support360, support361, support362, support363, support364, support365, support366, support367, support368, support369, support370, support371, support372, support373, support374, support375, support376, support377, support378, support379, support380, support381, support382, support383, support384, support385, support386, support387, support388, support389, support390, support391, support392, support393, support394, support395, support396, support397, support398, support399, support400, support401]
def demand : Fin 402 → ℕ := ![27, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 7, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 3, 2, 3, 3, 3, 3, 3, 3, 7, 7, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 3, 3, 2, 2, 3, 2, 2, 2, 2, 2, 2, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 2, 2, 2, 2, 3, 3, 2, 3, 3, 2, 3, 2, 2, 2, 3, 3, 3, 3, 2, 3, 3, 3, 2, 2, 3, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 3, 3, 2, 3, 3, 2, 2, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 2, 2, 3, 3, 3, 3, 7, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 2, 3, 2, 2, 3, 2, 2, 2, 3, 3, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 2, 2, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 2, 3, 3, 3, 4, 2, 3, 2, 3, 2, 2, 3, 4, 3, 2, 4, 2, 3, 2, 2, 3, 2, 4, 4, 4, 4, 4, 3, 2, 3, 4, 4, 4, 4, 2, 2, 3, 2, 4, 3, 2, 2, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 4, 3, 3, 3, 2, 2, 2]
theorem all_rows (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    ∀ r, demand r ≤ ∑ i ∈ support r, holes i := by
  unfold support demand
  exact (Fin.cases (cut0 holes hbool hrows) (Fin.cases (cut1 holes hbool hrows) (Fin.cases (cut2 holes hbool hrows) (Fin.cases (cut3 holes hbool hrows) (Fin.cases (cut4 holes hbool hrows) (Fin.cases (cut5 holes hbool hrows) (Fin.cases (cut6 holes hbool hrows) (Fin.cases (cut7 holes hbool hrows) (Fin.cases (cut8 holes hbool hrows) (Fin.cases (cut9 holes hbool hrows) (Fin.cases (cut10 holes hbool hrows) (Fin.cases (cut11 holes hbool hrows) (Fin.cases (cut12 holes hbool hrows) (Fin.cases (cut13 holes hbool hrows) (Fin.cases (cut14 holes hbool hrows) (Fin.cases (cut15 holes hbool hrows) (Fin.cases (cut16 holes hbool hrows) (Fin.cases (cut17 holes hbool hrows) (Fin.cases (cut18 holes hbool hrows) (Fin.cases (cut19 holes hbool hrows) (Fin.cases (cut20 holes hbool hrows) (Fin.cases (cut21 holes hbool hrows) (Fin.cases (cut22 holes hbool hrows) (Fin.cases (cut23 holes hbool hrows) (Fin.cases (cut24 holes hbool hrows) (Fin.cases (cut25 holes hbool hrows) (Fin.cases (cut26 holes hbool hrows) (Fin.cases (cut27 holes hbool hrows) (Fin.cases (cut28 holes hbool hrows) (Fin.cases (cut29 holes hbool hrows) (Fin.cases (cut30 holes hbool hrows) (Fin.cases (cut31 holes hbool hrows) (Fin.cases (cut32 holes hbool hrows) (Fin.cases (cut33 holes hbool hrows) (Fin.cases (cut34 holes hbool hrows) (Fin.cases (cut35 holes hbool hrows) (Fin.cases (cut36 holes hbool hrows) (Fin.cases (cut37 holes hbool hrows) (Fin.cases (cut38 holes hbool hrows) (Fin.cases (cut39 holes hbool hrows) (Fin.cases (cut40 holes hbool hrows) (Fin.cases (cut41 holes hbool hrows) (Fin.cases (cut42 holes hbool hrows) (Fin.cases (cut43 holes hbool hrows) (Fin.cases (cut44 holes hbool hrows) (Fin.cases (cut45 holes hbool hrows) (Fin.cases (cut46 holes hbool hrows) (Fin.cases (cut47 holes hbool hrows) (Fin.cases (cut48 holes hbool hrows) (Fin.cases (cut49 holes hbool hrows) (Fin.cases (cut50 holes hbool hrows) (Fin.cases (cut51 holes hbool hrows) (Fin.cases (cut52 holes hbool hrows) (Fin.cases (cut53 holes hbool hrows) (Fin.cases (cut54 holes hbool hrows) (Fin.cases (cut55 holes hbool hrows) (Fin.cases (cut56 holes hbool hrows) (Fin.cases (cut57 holes hbool hrows) (Fin.cases (cut58 holes hbool hrows) (Fin.cases (cut59 holes hbool hrows) (Fin.cases (cut60 holes hbool hrows) (Fin.cases (cut61 holes hbool hrows) (Fin.cases (cut62 holes hbool hrows) (Fin.cases (cut63 holes hbool hrows) (Fin.cases (cut64 holes hbool hrows) (Fin.cases (cut65 holes hbool hrows) (Fin.cases (cut66 holes hbool hrows) (Fin.cases (cut67 holes hbool hrows) (Fin.cases (cut68 holes hbool hrows) (Fin.cases (cut69 holes hbool hrows) (Fin.cases (cut70 holes hbool hrows) (Fin.cases (cut71 holes hbool hrows) (Fin.cases (cut72 holes hbool hrows) (Fin.cases (cut73 holes hbool hrows) (Fin.cases (cut74 holes hbool hrows) (Fin.cases (cut75 holes hbool hrows) (Fin.cases (cut76 holes hbool hrows) (Fin.cases (cut77 holes hbool hrows) (Fin.cases (cut78 holes hbool hrows) (Fin.cases (cut79 holes hbool hrows) (Fin.cases (cut80 holes hbool hrows) (Fin.cases (cut81 holes hbool hrows) (Fin.cases (cut82 holes hbool hrows) (Fin.cases (cut83 holes hbool hrows) (Fin.cases (cut84 holes hbool hrows) (Fin.cases (cut85 holes hbool hrows) (Fin.cases (cut86 holes hbool hrows) (Fin.cases (cut87 holes hbool hrows) (Fin.cases (cut88 holes hbool hrows) (Fin.cases (cut89 holes hbool hrows) (Fin.cases (cut90 holes hbool hrows) (Fin.cases (cut91 holes hbool hrows) (Fin.cases (cut92 holes hbool hrows) (Fin.cases (cut93 holes hbool hrows) (Fin.cases (cut94 holes hbool hrows) (Fin.cases (cut95 holes hbool hrows) (Fin.cases (cut96 holes hbool hrows) (Fin.cases (cut97 holes hbool hrows) (Fin.cases (cut98 holes hbool hrows) (Fin.cases (cut99 holes hbool hrows) (Fin.cases (cut100 holes hbool hrows) (Fin.cases (cut101 holes hbool hrows) (Fin.cases (cut102 holes hbool hrows) (Fin.cases (cut103 holes hbool hrows) (Fin.cases (cut104 holes hbool hrows) (Fin.cases (cut105 holes hbool hrows) (Fin.cases (cut106 holes hbool hrows) (Fin.cases (cut107 holes hbool hrows) (Fin.cases (cut108 holes hbool hrows) (Fin.cases (cut109 holes hbool hrows) (Fin.cases (cut110 holes hbool hrows) (Fin.cases (cut111 holes hbool hrows) (Fin.cases (cut112 holes hbool hrows) (Fin.cases (cut113 holes hbool hrows) (Fin.cases (cut114 holes hbool hrows) (Fin.cases (cut115 holes hbool hrows) (Fin.cases (cut116 holes hbool hrows) (Fin.cases (cut117 holes hbool hrows) (Fin.cases (cut118 holes hbool hrows) (Fin.cases (cut119 holes hbool hrows) (Fin.cases (cut120 holes hbool hrows) (Fin.cases (cut121 holes hbool hrows) (Fin.cases (cut122 holes hbool hrows) (Fin.cases (cut123 holes hbool hrows) (Fin.cases (cut124 holes hbool hrows) (Fin.cases (cut125 holes hbool hrows) (Fin.cases (cut126 holes hbool hrows) (Fin.cases (cut127 holes hbool hrows) (Fin.cases (cut128 holes hbool hrows) (Fin.cases (cut129 holes hbool hrows) (Fin.cases (cut130 holes hbool hrows) (Fin.cases (cut131 holes hbool hrows) (Fin.cases (cut132 holes hbool hrows) (Fin.cases (cut133 holes hbool hrows) (Fin.cases (cut134 holes hbool hrows) (Fin.cases (cut135 holes hbool hrows) (Fin.cases (cut136 holes hbool hrows) (Fin.cases (cut137 holes hbool hrows) (Fin.cases (cut138 holes hbool hrows) (Fin.cases (cut139 holes hbool hrows) (Fin.cases (cut140 holes hbool hrows) (Fin.cases (cut141 holes hbool hrows) (Fin.cases (cut142 holes hbool hrows) (Fin.cases (cut143 holes hbool hrows) (Fin.cases (cut144 holes hbool hrows) (Fin.cases (cut145 holes hbool hrows) (Fin.cases (cut146 holes hbool hrows) (Fin.cases (cut147 holes hbool hrows) (Fin.cases (cut148 holes hbool hrows) (Fin.cases (cut149 holes hbool hrows) (Fin.cases (cut150 holes hbool hrows) (Fin.cases (cut151 holes hbool hrows) (Fin.cases (cut152 holes hbool hrows) (Fin.cases (cut153 holes hbool hrows) (Fin.cases (cut154 holes hbool hrows) (Fin.cases (cut155 holes hbool hrows) (Fin.cases (cut156 holes hbool hrows) (Fin.cases (cut157 holes hbool hrows) (Fin.cases (cut158 holes hbool hrows) (Fin.cases (cut159 holes hbool hrows) (Fin.cases (cut160 holes hbool hrows) (Fin.cases (cut161 holes hbool hrows) (Fin.cases (cut162 holes hbool hrows) (Fin.cases (cut163 holes hbool hrows) (Fin.cases (cut164 holes hbool hrows) (Fin.cases (cut165 holes hbool hrows) (Fin.cases (cut166 holes hbool hrows) (Fin.cases (cut167 holes hbool hrows) (Fin.cases (cut168 holes hbool hrows) (Fin.cases (cut169 holes hbool hrows) (Fin.cases (cut170 holes hbool hrows) (Fin.cases (cut171 holes hbool hrows) (Fin.cases (cut172 holes hbool hrows) (Fin.cases (cut173 holes hbool hrows) (Fin.cases (cut174 holes hbool hrows) (Fin.cases (cut175 holes hbool hrows) (Fin.cases (cut176 holes hbool hrows) (Fin.cases (cut177 holes hbool hrows) (Fin.cases (cut178 holes hbool hrows) (Fin.cases (cut179 holes hbool hrows) (Fin.cases (cut180 holes hbool hrows) (Fin.cases (cut181 holes hbool hrows) (Fin.cases (cut182 holes hbool hrows) (Fin.cases (cut183 holes hbool hrows) (Fin.cases (cut184 holes hbool hrows) (Fin.cases (cut185 holes hbool hrows) (Fin.cases (cut186 holes hbool hrows) (Fin.cases (cut187 holes hbool hrows) (Fin.cases (cut188 holes hbool hrows) (Fin.cases (cut189 holes hbool hrows) (Fin.cases (cut190 holes hbool hrows) (Fin.cases (cut191 holes hbool hrows) (Fin.cases (cut192 holes hbool hrows) (Fin.cases (cut193 holes hbool hrows) (Fin.cases (cut194 holes hbool hrows) (Fin.cases (cut195 holes hbool hrows) (Fin.cases (cut196 holes hbool hrows) (Fin.cases (cut197 holes hbool hrows) (Fin.cases (cut198 holes hbool hrows) (Fin.cases (cut199 holes hbool hrows) (Fin.cases (cut200 holes hbool hrows) (Fin.cases (cut201 holes hbool hrows) (Fin.cases (cut202 holes hbool hrows) (Fin.cases (cut203 holes hbool hrows) (Fin.cases (cut204 holes hbool hrows) (Fin.cases (cut205 holes hbool hrows) (Fin.cases (cut206 holes hbool hrows) (Fin.cases (cut207 holes hbool hrows) (Fin.cases (cut208 holes hbool hrows) (Fin.cases (cut209 holes hbool hrows) (Fin.cases (cut210 holes hbool hrows) (Fin.cases (cut211 holes hbool hrows) (Fin.cases (cut212 holes hbool hrows) (Fin.cases (cut213 holes hbool hrows) (Fin.cases (cut214 holes hbool hrows) (Fin.cases (cut215 holes hbool hrows) (Fin.cases (cut216 holes hbool hrows) (Fin.cases (cut217 holes hbool hrows) (Fin.cases (cut218 holes hbool hrows) (Fin.cases (cut219 holes hbool hrows) (Fin.cases (cut220 holes hbool hrows) (Fin.cases (cut221 holes hbool hrows) (Fin.cases (cut222 holes hbool hrows) (Fin.cases (cut223 holes hbool hrows) (Fin.cases (cut224 holes hbool hrows) (Fin.cases (cut225 holes hbool hrows) (Fin.cases (cut226 holes hbool hrows) (Fin.cases (cut227 holes hbool hrows) (Fin.cases (cut228 holes hbool hrows) (Fin.cases (cut229 holes hbool hrows) (Fin.cases (cut230 holes hbool hrows) (Fin.cases (cut231 holes hbool hrows) (Fin.cases (cut232 holes hbool hrows) (Fin.cases (cut233 holes hbool hrows) (Fin.cases (cut234 holes hbool hrows) (Fin.cases (cut235 holes hbool hrows) (Fin.cases (cut236 holes hbool hrows) (Fin.cases (cut237 holes hbool hrows) (Fin.cases (cut238 holes hbool hrows) (Fin.cases (cut239 holes hbool hrows) (Fin.cases (cut240 holes hbool hrows) (Fin.cases (cut241 holes hbool hrows) (Fin.cases (cut242 holes hbool hrows) (Fin.cases (cut243 holes hbool hrows) (Fin.cases (cut244 holes hbool hrows) (Fin.cases (cut245 holes hbool hrows) (Fin.cases (cut246 holes hbool hrows) (Fin.cases (cut247 holes hbool hrows) (Fin.cases (cut248 holes hbool hrows) (Fin.cases (cut249 holes hbool hrows) (Fin.cases (cut250 holes hbool hrows) (Fin.cases (cut251 holes hbool hrows) (Fin.cases (cut252 holes hbool hrows) (Fin.cases (cut253 holes hbool hrows) (Fin.cases (cut254 holes hbool hrows) (Fin.cases (cut255 holes hbool hrows) (Fin.cases (cut256 holes hbool hrows) (Fin.cases (cut257 holes hbool hrows) (Fin.cases (cut258 holes hbool hrows) (Fin.cases (cut259 holes hbool hrows) (Fin.cases (cut260 holes hbool hrows) (Fin.cases (cut261 holes hbool hrows) (Fin.cases (cut262 holes hbool hrows) (Fin.cases (cut263 holes hbool hrows) (Fin.cases (cut264 holes hbool hrows) (Fin.cases (cut265 holes hbool hrows) (Fin.cases (cut266 holes hbool hrows) (Fin.cases (cut267 holes hbool hrows) (Fin.cases (cut268 holes hbool hrows) (Fin.cases (cut269 holes hbool hrows) (Fin.cases (cut270 holes hbool hrows) (Fin.cases (cut271 holes hbool hrows) (Fin.cases (cut272 holes hbool hrows) (Fin.cases (cut273 holes hbool hrows) (Fin.cases (cut274 holes hbool hrows) (Fin.cases (cut275 holes hbool hrows) (Fin.cases (cut276 holes hbool hrows) (Fin.cases (cut277 holes hbool hrows) (Fin.cases (cut278 holes hbool hrows) (Fin.cases (cut279 holes hbool hrows) (Fin.cases (cut280 holes hbool hrows) (Fin.cases (cut281 holes hbool hrows) (Fin.cases (cut282 holes hbool hrows) (Fin.cases (cut283 holes hbool hrows) (Fin.cases (cut284 holes hbool hrows) (Fin.cases (cut285 holes hbool hrows) (Fin.cases (cut286 holes hbool hrows) (Fin.cases (cut287 holes hbool hrows) (Fin.cases (cut288 holes hbool hrows) (Fin.cases (cut289 holes hbool hrows) (Fin.cases (cut290 holes hbool hrows) (Fin.cases (cut291 holes hbool hrows) (Fin.cases (cut292 holes hbool hrows) (Fin.cases (cut293 holes hbool hrows) (Fin.cases (cut294 holes hbool hrows) (Fin.cases (cut295 holes hbool hrows) (Fin.cases (cut296 holes hbool hrows) (Fin.cases (cut297 holes hbool hrows) (Fin.cases (cut298 holes hbool hrows) (Fin.cases (cut299 holes hbool hrows) (Fin.cases (cut300 holes hbool hrows) (Fin.cases (cut301 holes hbool hrows) (Fin.cases (cut302 holes hbool hrows) (Fin.cases (cut303 holes hbool hrows) (Fin.cases (cut304 holes hbool hrows) (Fin.cases (cut305 holes hbool hrows) (Fin.cases (cut306 holes hbool hrows) (Fin.cases (cut307 holes hbool hrows) (Fin.cases (cut308 holes hbool hrows) (Fin.cases (cut309 holes hbool hrows) (Fin.cases (cut310 holes hbool hrows) (Fin.cases (cut311 holes hbool hrows) (Fin.cases (cut312 holes hbool hrows) (Fin.cases (cut313 holes hbool hrows) (Fin.cases (cut314 holes hbool hrows) (Fin.cases (cut315 holes hbool hrows) (Fin.cases (cut316 holes hbool hrows) (Fin.cases (cut317 holes hbool hrows) (Fin.cases (cut318 holes hbool hrows) (Fin.cases (cut319 holes hbool hrows) (Fin.cases (cut320 holes hbool hrows) (Fin.cases (cut321 holes hbool hrows) (Fin.cases (cut322 holes hbool hrows) (Fin.cases (cut323 holes hbool hrows) (Fin.cases (cut324 holes hbool hrows) (Fin.cases (cut325 holes hbool hrows) (Fin.cases (cut326 holes hbool hrows) (Fin.cases (cut327 holes hbool hrows) (Fin.cases (cut328 holes hbool hrows) (Fin.cases (cut329 holes hbool hrows) (Fin.cases (cut330 holes hbool hrows) (Fin.cases (cut331 holes hbool hrows) (Fin.cases (cut332 holes hbool hrows) (Fin.cases (cut333 holes hbool hrows) (Fin.cases (cut334 holes hbool hrows) (Fin.cases (cut335 holes hbool hrows) (Fin.cases (cut336 holes hbool hrows) (Fin.cases (cut337 holes hbool hrows) (Fin.cases (cut338 holes hbool hrows) (Fin.cases (cut339 holes hbool hrows) (Fin.cases (cut340 holes hbool hrows) (Fin.cases (cut341 holes hbool hrows) (Fin.cases (cut342 holes hbool hrows) (Fin.cases (cut343 holes hbool hrows) (Fin.cases (cut344 holes hbool hrows) (Fin.cases (cut345 holes hbool hrows) (Fin.cases (cut346 holes hbool hrows) (Fin.cases (cut347 holes hbool hrows) (Fin.cases (cut348 holes hbool hrows) (Fin.cases (cut349 holes hbool hrows) (Fin.cases (cut350 holes hbool hrows) (Fin.cases (cut351 holes hbool hrows) (Fin.cases (cut352 holes hbool hrows) (Fin.cases (cut353 holes hbool hrows) (Fin.cases (cut354 holes hbool hrows) (Fin.cases (cut355 holes hbool hrows) (Fin.cases (cut356 holes hbool hrows) (Fin.cases (cut357 holes hbool hrows) (Fin.cases (cut358 holes hbool hrows) (Fin.cases (cut359 holes hbool hrows) (Fin.cases (cut360 holes hbool hrows) (Fin.cases (cut361 holes hbool hrows) (Fin.cases (cut362 holes hbool hrows) (Fin.cases (cut363 holes hbool hrows) (Fin.cases (cut364 holes hbool hrows) (Fin.cases (cut365 holes hbool hrows) (Fin.cases (cut366 holes hbool hrows) (Fin.cases (cut367 holes hbool hrows) (Fin.cases (cut368 holes hbool hrows) (Fin.cases (cut369 holes hbool hrows) (Fin.cases (cut370 holes hbool hrows) (Fin.cases (cut371 holes hbool hrows) (Fin.cases (cut372 holes hbool hrows) (Fin.cases (cut373 holes hbool hrows) (Fin.cases (cut374 holes hbool hrows) (Fin.cases (cut375 holes hbool hrows) (Fin.cases (cut376 holes hbool hrows) (Fin.cases (cut377 holes hbool hrows) (Fin.cases (cut378 holes hbool hrows) (Fin.cases (cut379 holes hbool hrows) (Fin.cases (cut380 holes hbool hrows) (Fin.cases (cut381 holes hbool hrows) (Fin.cases (cut382 holes hbool hrows) (Fin.cases (cut383 holes hbool hrows) (Fin.cases (cut384 holes hbool hrows) (Fin.cases (cut385 holes hbool hrows) (Fin.cases (cut386 holes hbool hrows) (Fin.cases (cut387 holes hbool hrows) (Fin.cases (cut388 holes hbool hrows) (Fin.cases (cut389 holes hbool hrows) (Fin.cases (cut390 holes hbool hrows) (Fin.cases (cut391 holes hbool hrows) (Fin.cases (cut392 holes hbool hrows) (Fin.cases (cut393 holes hbool hrows) (Fin.cases (cut394 holes hbool hrows) (Fin.cases (cut395 holes hbool hrows) (Fin.cases (cut396 holes hbool hrows) (Fin.cases (cut397 holes hbool hrows) (Fin.cases (cut398 holes hbool hrows) (Fin.cases (cut399 holes hbool hrows) (Fin.cases (cut400 holes hbool hrows) (Fin.cases (cut401 holes hbool hrows) (fun i => Fin.elim0 i)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#print axioms all_rows
end ResidualCoverCuts
