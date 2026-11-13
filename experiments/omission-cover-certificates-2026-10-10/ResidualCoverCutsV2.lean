import Catalog
import ErdosSzekeres.Omission.CoverCuts
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace ResidualCoverCutsV2
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
def support402 : Finset (Fin 154) := {38, 47, 51, 57, 60, 63, 66, 70, 73, 78, 80, 92, 98, 102, 112, 121}
theorem cut402 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support402, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 930, OmissionResidual.support 950, OmissionResidual.support 679] ![OmissionResidual.demand 930, OmissionResidual.demand 950, OmissionResidual.demand 679] ![1, 1, 1]
    support402 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 930) (Fin.cases (hrows 950) (Fin.cases (hrows 679) (fun i => Fin.elim0 i))))
def support403 : Finset (Fin 154) := {15, 24, 27, 29, 36, 37, 41, 42, 47, 52, 58, 63, 72, 73, 83}
theorem cut403 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support403, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 629, OmissionResidual.support 552, OmissionResidual.support 551] ![OmissionResidual.demand 629, OmissionResidual.demand 552, OmissionResidual.demand 551] ![1, 1, 1]
    support403 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 629) (Fin.cases (hrows 552) (Fin.cases (hrows 551) (fun i => Fin.elim0 i))))
def support404 : Finset (Fin 154) := {97, 105, 113, 116, 123, 126, 128, 129, 132, 134, 138, 140, 145, 148}
theorem cut404 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support404, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1150, OmissionResidual.support 1120, OmissionResidual.support 1121] ![OmissionResidual.demand 1150, OmissionResidual.demand 1120, OmissionResidual.demand 1121] ![1, 1, 1]
    support404 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1150) (Fin.cases (hrows 1120) (Fin.cases (hrows 1121) (fun i => Fin.elim0 i))))
def support405 : Finset (Fin 154) := {5, 6, 8, 11, 12, 14, 15, 16, 20, 23, 24, 26, 27, 32, 36, 37, 40, 41, 42, 47, 49, 51, 52, 60, 62}
theorem cut405 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support405, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 491, support311, support104] ![OmissionResidual.demand 491, 2, 2] ![1, 1, 1]
    support405 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 491) (Fin.cases (cut311 holes hbool hrows) (Fin.cases (cut104 holes hbool hrows) (fun i => Fin.elim0 i))))
def support406 : Finset (Fin 154) := {5, 8, 9, 13, 19, 21, 25, 31, 34, 38, 44, 45, 51, 66}
theorem cut406 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support406, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 62, OmissionResidual.support 30, OmissionResidual.support 37] ![OmissionResidual.demand 62, OmissionResidual.demand 30, OmissionResidual.demand 37] ![1, 1, 1]
    support406 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 62) (Fin.cases (hrows 30) (Fin.cases (hrows 37) (fun i => Fin.elim0 i))))
def support407 : Finset (Fin 154) := {5, 8, 13, 15, 19, 21, 25, 28, 31, 34, 38, 44, 45, 51, 66}
theorem cut407 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support407, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 116, OmissionResidual.support 30, OmissionResidual.support 37] ![OmissionResidual.demand 116, OmissionResidual.demand 30, OmissionResidual.demand 37] ![1, 1, 1]
    support407 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 116) (Fin.cases (hrows 30) (Fin.cases (hrows 37) (fun i => Fin.elim0 i))))
def support408 : Finset (Fin 154) := {2, 4, 5, 8, 9, 13, 19, 21, 25, 31, 34, 38, 44, 45, 51, 66}
theorem cut408 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support408, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 62, OmissionResidual.support 10, OmissionResidual.support 37] ![OmissionResidual.demand 62, OmissionResidual.demand 10, OmissionResidual.demand 37] ![1, 1, 1]
    support408 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 62) (Fin.cases (hrows 10) (Fin.cases (hrows 37) (fun i => Fin.elim0 i))))
def support409 : Finset (Fin 154) := {2, 4, 10, 13, 14, 15, 21, 25, 28, 31, 34, 38, 44, 45, 51, 66}
theorem cut409 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support409, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 116, OmissionResidual.support 10, OmissionResidual.support 72] ![OmissionResidual.demand 116, OmissionResidual.demand 10, OmissionResidual.demand 72] ![1, 1, 1]
    support409 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 116) (Fin.cases (hrows 10) (Fin.cases (hrows 72) (fun i => Fin.elim0 i))))
def support410 : Finset (Fin 154) := {5, 8, 10, 13, 14, 15, 21, 25, 28, 31, 34, 38, 44, 45, 51, 66}
theorem cut410 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support410, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 116, OmissionResidual.support 30, OmissionResidual.support 72] ![OmissionResidual.demand 116, OmissionResidual.demand 30, OmissionResidual.demand 72] ![1, 1, 1]
    support410 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 116) (Fin.cases (hrows 30) (Fin.cases (hrows 72) (fun i => Fin.elim0 i))))
def support411 : Finset (Fin 154) := {2, 4, 9, 10, 13, 14, 19, 21, 25, 28, 31, 34, 38, 44, 45, 51, 66}
theorem cut411 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support411, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 62, OmissionResidual.support 10, OmissionResidual.support 72] ![OmissionResidual.demand 62, OmissionResidual.demand 10, OmissionResidual.demand 72] ![1, 1, 1]
    support411 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 62) (Fin.cases (hrows 10) (Fin.cases (hrows 72) (fun i => Fin.elim0 i))))
def support412 : Finset (Fin 154) := {5, 8, 9, 10, 13, 14, 19, 21, 25, 28, 31, 34, 38, 44, 45, 51, 66}
theorem cut412 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support412, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 62, OmissionResidual.support 30, OmissionResidual.support 72] ![OmissionResidual.demand 62, OmissionResidual.demand 30, OmissionResidual.demand 72] ![1, 1, 1]
    support412 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 62) (Fin.cases (hrows 30) (Fin.cases (hrows 72) (fun i => Fin.elim0 i))))
def support413 : Finset (Fin 154) := {2, 4, 5, 8, 13, 15, 19, 21, 25, 28, 31, 34, 38, 44, 45, 51, 66}
theorem cut413 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support413, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 116, OmissionResidual.support 10, OmissionResidual.support 37] ![OmissionResidual.demand 116, OmissionResidual.demand 10, OmissionResidual.demand 37] ![1, 1, 1]
    support413 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 116) (Fin.cases (hrows 10) (Fin.cases (hrows 37) (fun i => Fin.elim0 i))))
def support414 : Finset (Fin 154) := {5, 8, 10, 12, 16, 20, 21, 23, 26, 27, 31, 32, 36, 37, 40, 41, 42, 47, 49, 51, 52, 60, 62}
theorem cut414 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support414, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 514, support112, support245] ![OmissionResidual.demand 514, 2, 2] ![1, 1, 1]
    support414 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 514) (Fin.cases (cut112 holes hbool hrows) (Fin.cases (cut245 holes hbool hrows) (fun i => Fin.elim0 i))))
def support415 : Finset (Fin 154) := {5, 8, 10, 12, 14, 16, 20, 21, 23, 24, 26, 27, 31, 36, 37, 40, 41, 42, 47, 49, 51, 52, 60, 62}
theorem cut415 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support415, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 514, support112, support104] ![OmissionResidual.demand 514, 2, 2] ![1, 1, 1]
    support415 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 514) (Fin.cases (cut112 holes hbool hrows) (Fin.cases (cut104 holes hbool hrows) (fun i => Fin.elim0 i))))
def support416 : Finset (Fin 154) := {6, 11, 14, 20, 21, 23, 27, 31, 32, 37, 41, 46, 50, 52, 57, 63, 82}
theorem cut416 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support416, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 542, OmissionResidual.support 583, OmissionResidual.support 490] ![OmissionResidual.demand 542, OmissionResidual.demand 583, OmissionResidual.demand 490] ![1, 1, 1]
    support416 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 542) (Fin.cases (hrows 583) (Fin.cases (hrows 490) (fun i => Fin.elim0 i))))
def support417 : Finset (Fin 154) := {2, 7, 16, 19, 24, 26, 28, 35, 36, 40, 46, 49, 54, 66, 76, 80, 92, 104}
theorem cut417 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support417, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 888, OmissionResidual.support 472, OmissionResidual.support 908] ![OmissionResidual.demand 888, OmissionResidual.demand 472, OmissionResidual.demand 908] ![1, 1, 1]
    support417 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 888) (Fin.cases (hrows 472) (Fin.cases (hrows 908) (fun i => Fin.elim0 i))))
def support418 : Finset (Fin 154) := {48, 58, 61, 69, 73, 80, 84, 94, 103, 106, 112, 116, 120, 124, 144}
theorem cut418 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support418, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 843, OmissionResidual.support 731, OmissionResidual.support 730] ![OmissionResidual.demand 843, OmissionResidual.demand 731, OmissionResidual.demand 730] ![1, 1, 1]
    support418 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 843) (Fin.cases (hrows 731) (Fin.cases (hrows 730) (fun i => Fin.elim0 i))))
def support419 : Finset (Fin 154) := {21, 22, 27, 31, 32, 36, 37, 42, 47, 52, 58, 63, 72, 73, 83}
theorem cut419 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support419, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 587, OmissionResidual.support 584, OmissionResidual.support 582] ![OmissionResidual.demand 587, OmissionResidual.demand 584, OmissionResidual.demand 582] ![1, 1, 1]
    support419 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 587) (Fin.cases (hrows 584) (Fin.cases (hrows 582) (fun i => Fin.elim0 i))))
def support420 : Finset (Fin 154) := {21, 27, 29, 31, 37, 41, 46, 51, 52, 57, 69, 70, 73, 93}
theorem cut420 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support420, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 630, OmissionResidual.support 585, OmissionResidual.support 579] ![OmissionResidual.demand 630, OmissionResidual.demand 585, OmissionResidual.demand 579] ![1, 1, 1]
    support420 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 630) (Fin.cases (hrows 585) (Fin.cases (hrows 579) (fun i => Fin.elim0 i))))
def support421 : Finset (Fin 154) := {9, 18, 24, 26, 32, 38, 47, 51, 57, 60, 66, 70, 78, 80, 92, 98, 112, 121}
theorem cut421 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support421, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 930, OmissionResidual.support 950, OmissionResidual.support 506] ![OmissionResidual.demand 930, OmissionResidual.demand 950, OmissionResidual.demand 506] ![1, 1, 1]
    support421 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 930) (Fin.cases (hrows 950) (Fin.cases (hrows 506) (fun i => Fin.elim0 i))))
def support422 : Finset (Fin 154) := {38, 47, 57, 58, 66, 69, 78, 80, 86, 97, 98, 103, 106, 112, 114, 121}
theorem cut422 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support422, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 930, OmissionResidual.support 776, OmissionResidual.support 929] ![OmissionResidual.demand 930, OmissionResidual.demand 776, OmissionResidual.demand 929] ![1, 1, 1]
    support422 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 930) (Fin.cases (hrows 776) (Fin.cases (hrows 929) (fun i => Fin.elim0 i))))
def support423 : Finset (Fin 154) := {10, 14, 16, 20, 21, 23, 27, 31, 32, 37, 41, 46, 50, 52, 57, 63, 82}
theorem cut423 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support423, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 542, OmissionResidual.support 583, OmissionResidual.support 512] ![OmissionResidual.demand 542, OmissionResidual.demand 583, OmissionResidual.demand 512] ![1, 1, 1]
    support423 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 542) (Fin.cases (hrows 583) (Fin.cases (hrows 512) (fun i => Fin.elim0 i))))
def support424 : Finset (Fin 154) := {38, 47, 48, 57, 58, 66, 69, 78, 80, 88, 93, 98, 105, 112, 121}
theorem cut424 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support424, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 930, OmissionResidual.support 927, OmissionResidual.support 360] ![OmissionResidual.demand 930, OmissionResidual.demand 927, OmissionResidual.demand 360] ![1, 1, 1]
    support424 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 930) (Fin.cases (hrows 927) (Fin.cases (hrows 360) (fun i => Fin.elim0 i))))
def support425 : Finset (Fin 154) := {51, 60, 66, 70, 71, 78, 81, 86, 92, 97, 98, 103, 106, 112, 114, 121}
theorem cut425 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support425, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 950, OmissionResidual.support 812, OmissionResidual.support 949] ![OmissionResidual.demand 950, OmissionResidual.demand 812, OmissionResidual.demand 949] ![1, 1, 1]
    support425 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 950) (Fin.cases (hrows 812) (Fin.cases (hrows 949) (fun i => Fin.elim0 i))))
#print axioms cut425
def support426 : Finset (Fin 154) := {15, 21, 22, 24, 27, 31, 32, 36, 37, 42, 47, 52, 58, 63, 72, 73, 83}
theorem cut426 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support426, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 587, OmissionResidual.support 552, OmissionResidual.support 582] ![OmissionResidual.demand 587, OmissionResidual.demand 552, OmissionResidual.demand 582] ![1, 1, 1]
    support426 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 587) (Fin.cases (hrows 552) (Fin.cases (hrows 582) (fun i => Fin.elim0 i))))
def support427 : Finset (Fin 154) := {5, 6, 8, 11, 12, 14, 15, 16, 20, 23, 24, 26, 27, 32, 36, 37, 40, 41, 47, 49, 50, 51, 60}
theorem cut427 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support427, holes i := by
  apply rounded_cover_cut ![support311, OmissionResidual.support 490, support104] ![2, OmissionResidual.demand 490, 2] ![1, 1, 1]
    support427 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut311 holes hbool hrows) (Fin.cases (hrows 490) (Fin.cases (cut104 holes hbool hrows) (fun i => Fin.elim0 i))))
def support428 : Finset (Fin 154) := {10, 14, 16, 21, 23, 25, 29, 30, 33, 49, 52, 56, 60, 67, 72, 78, 87}
theorem cut428 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support428, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 884, OmissionResidual.support 75, OmissionResidual.support 899] ![OmissionResidual.demand 884, OmissionResidual.demand 75, OmissionResidual.demand 899] ![1, 1, 1]
    support428 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 884) (Fin.cases (hrows 75) (Fin.cases (hrows 899) (fun i => Fin.elim0 i))))
def support429 : Finset (Fin 154) := {73, 83, 88, 93, 100, 102, 112, 117, 120, 124, 130, 135, 138, 140, 143, 144, 153}
theorem cut429 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support429, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1160, OmissionResidual.support 970, OmissionResidual.support 969] ![OmissionResidual.demand 1160, OmissionResidual.demand 970, OmissionResidual.demand 969] ![1, 1, 1]
    support429 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1160) (Fin.cases (hrows 970) (Fin.cases (hrows 969) (fun i => Fin.elim0 i))))
def support430 : Finset (Fin 154) := {26, 35, 64, 74, 75, 80, 85, 86, 92, 95, 104, 105, 115, 118, 126, 131}
theorem cut430 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support430, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1042, OmissionResidual.support 617, OmissionResidual.support 1067] ![OmissionResidual.demand 1042, OmissionResidual.demand 617, OmissionResidual.demand 1067] ![1, 1, 1]
    support430 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1042) (Fin.cases (hrows 617) (Fin.cases (hrows 1067) (fun i => Fin.elim0 i))))
def support431 : Finset (Fin 154) := {9, 18, 24, 26, 32, 48, 58, 61, 69, 71, 76, 80, 81, 88, 92, 98, 112, 121}
theorem cut431 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support431, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 945, OmissionResidual.support 507, OmissionResidual.support 959] ![OmissionResidual.demand 945, OmissionResidual.demand 507, OmissionResidual.demand 959] ![1, 1, 1]
    support431 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 945) (Fin.cases (hrows 507) (Fin.cases (hrows 959) (fun i => Fin.elim0 i))))
def support432 : Finset (Fin 154) := {9, 18, 24, 26, 32, 48, 58, 61, 69, 71, 76, 80, 81, 88, 92, 98, 120, 128}
theorem cut432 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support432, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 507, OmissionResidual.support 946, OmissionResidual.support 960] ![OmissionResidual.demand 507, OmissionResidual.demand 946, OmissionResidual.demand 960] ![1, 1, 1]
    support432 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 507) (Fin.cases (hrows 946) (Fin.cases (hrows 960) (fun i => Fin.elim0 i))))
def support433 : Finset (Fin 154) := {13, 15, 18, 21, 22, 24, 27, 29, 31, 32, 35, 36, 37, 41, 42, 47, 52, 58, 61, 63, 69, 72, 73, 81, 83}
theorem cut433 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support433, holes i := by
  apply rounded_cover_cut ![support403, OmissionResidual.support 531, support419] ![2, OmissionResidual.demand 531, 2] ![1, 1, 1]
    support433 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut403 holes hbool hrows) (Fin.cases (hrows 531) (Fin.cases (cut419 holes hbool hrows) (fun i => Fin.elim0 i))))
def support434 : Finset (Fin 154) := {87, 89, 96, 105, 107, 110, 114, 115, 118, 123, 130, 132, 137, 138, 142}
theorem cut434 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support434, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1098, OmissionResidual.support 1097, OmissionResidual.support 1107] ![OmissionResidual.demand 1098, OmissionResidual.demand 1097, OmissionResidual.demand 1107] ![1, 1, 1]
    support434 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1098) (Fin.cases (hrows 1097) (Fin.cases (hrows 1107) (fun i => Fin.elim0 i))))
def support435 : Finset (Fin 154) := {21, 27, 31, 39, 41, 44, 46, 59, 61, 67, 69, 81, 88, 93, 105}
theorem cut435 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support435, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 896, OmissionResidual.support 918, OmissionResidual.support 581] ![OmissionResidual.demand 896, OmissionResidual.demand 918, OmissionResidual.demand 581] ![1, 1, 1]
    support435 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 896) (Fin.cases (hrows 918) (Fin.cases (hrows 581) (fun i => Fin.elim0 i))))
def support436 : Finset (Fin 154) := {31, 39, 44, 49, 59, 64, 67, 71, 81, 83, 87, 88, 93, 97, 105}
theorem cut436 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support436, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 918, OmissionResidual.support 736, OmissionResidual.support 917] ![OmissionResidual.demand 918, OmissionResidual.demand 736, OmissionResidual.demand 917] ![1, 1, 1]
    support436 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 918) (Fin.cases (hrows 736) (Fin.cases (hrows 917) (fun i => Fin.elim0 i))))
def support437 : Finset (Fin 154) := {2, 7, 16, 24, 26, 35, 36, 40, 46, 49, 53, 64, 65, 74, 75, 80, 85, 86, 92, 95, 96, 104, 105, 107, 110, 115, 118, 125, 126, 131}
theorem cut437 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support437, holes i := by
  apply rounded_cover_cut ![support392, OmissionResidual.support 472, support394] ![3, OmissionResidual.demand 472, 3] ![1, 1, 1]
    support437 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut392 holes hbool hrows) (Fin.cases (hrows 472) (Fin.cases (cut394 holes hbool hrows) (fun i => Fin.elim0 i))))
def support438 : Finset (Fin 154) := {29, 37, 41, 50, 52, 55, 57, 67, 69, 70, 73, 81, 93, 98, 103, 114}
theorem cut438 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support438, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 938, OmissionResidual.support 630, OmissionResidual.support 914] ![OmissionResidual.demand 938, OmissionResidual.demand 630, OmissionResidual.demand 914] ![1, 1, 1]
    support438 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 938) (Fin.cases (hrows 630) (Fin.cases (hrows 914) (fun i => Fin.elim0 i))))
def support439 : Finset (Fin 154) := {21, 22, 27, 29, 31, 32, 37, 38, 41, 42, 46, 47, 51, 52, 57, 58, 63, 69, 70, 73, 82, 84, 93, 94}
theorem cut439 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support439, holes i := by
  apply rounded_cover_cut ![support420, support40, OmissionResidual.support 588] ![2, 2, OmissionResidual.demand 588] ![1, 1, 1]
    support439 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut420 holes hbool hrows) (Fin.cases (cut40 holes hbool hrows) (Fin.cases (hrows 588) (fun i => Fin.elim0 i))))
def support440 : Finset (Fin 154) := {0, 2, 4, 5, 7, 8, 11, 12, 14, 16, 20, 21, 23, 24, 26, 27, 30, 31, 36, 40, 46, 49, 52, 57, 63, 82}
theorem cut440 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support440, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 542, OmissionResidual.support 583, support49, support51, OmissionResidual.support 483] ![OmissionResidual.demand 542, OmissionResidual.demand 583, 2, 2, OmissionResidual.demand 483] ![1, 1, 1, 1, 1]
    support440 3 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 542) (Fin.cases (hrows 583) (Fin.cases (cut49 holes hbool hrows) (Fin.cases (cut51 holes hbool hrows) (Fin.cases (hrows 483) (fun i => Fin.elim0 i))))))
def support441 : Finset (Fin 154) := {6, 11, 20, 27, 37, 42, 43, 46, 52, 53, 57, 62, 77, 82, 87, 96}
theorem cut441 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support441, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 491, OmissionResidual.support 577, OmissionResidual.support 620] ![OmissionResidual.demand 491, OmissionResidual.demand 577, OmissionResidual.demand 620] ![1, 1, 1]
    support441 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 491) (Fin.cases (hrows 577) (Fin.cases (hrows 620) (fun i => Fin.elim0 i))))
def support442 : Finset (Fin 154) := {10, 16, 20, 25, 27, 30, 32, 37, 39, 41, 50, 56, 62, 67, 77}
theorem cut442 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support442, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 883, OmissionResidual.support 867, OmissionResidual.support 512] ![OmissionResidual.demand 883, OmissionResidual.demand 867, OmissionResidual.demand 512] ![1, 1, 1]
    support442 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 883) (Fin.cases (hrows 867) (Fin.cases (hrows 512) (fun i => Fin.elim0 i))))
def support443 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 61, 62, 63, 69, 73, 77, 80, 82, 84, 89, 93, 102, 103, 112, 124, 130}
theorem cut443 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support443, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 798, support47, support59] ![OmissionResidual.demand 798, 2, 2] ![1, 1, 1]
    support443 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 798) (Fin.cases (cut47 holes hbool hrows) (Fin.cases (cut59 holes hbool hrows) (fun i => Fin.elim0 i))))
def support444 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 61, 62, 63, 69, 73, 77, 80, 82, 84, 89, 93, 102, 103, 112, 120, 124, 130}
theorem cut444 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support444, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 798, support47, support155] ![OmissionResidual.demand 798, 2, 2] ![1, 1, 1]
    support444 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 798) (Fin.cases (cut47 holes hbool hrows) (Fin.cases (cut155 holes hbool hrows) (fun i => Fin.elim0 i))))
def support445 : Finset (Fin 154) := {78, 84, 87, 94, 96, 103, 105, 111, 112, 114, 120, 123, 127, 130, 133, 137, 142, 148}
theorem cut445 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support445, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1077, OmissionResidual.support 1078, OmissionResidual.support 1093] ![OmissionResidual.demand 1077, OmissionResidual.demand 1078, OmissionResidual.demand 1093] ![1, 1, 1]
    support445 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1077) (Fin.cases (hrows 1078) (Fin.cases (hrows 1093) (fun i => Fin.elim0 i))))
def support446 : Finset (Fin 154) := {78, 84, 87, 94, 96, 103, 105, 111, 112, 114, 120, 123, 127, 130, 133, 137, 142, 150}
theorem cut446 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support446, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1077, OmissionResidual.support 1078, OmissionResidual.support 1094] ![OmissionResidual.demand 1077, OmissionResidual.demand 1078, OmissionResidual.demand 1094] ![1, 1, 1]
    support446 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1077) (Fin.cases (hrows 1078) (Fin.cases (hrows 1094) (fun i => Fin.elim0 i))))
def support447 : Finset (Fin 154) := {38, 47, 57, 66, 73, 78, 80, 83, 88, 93, 98, 102, 112, 113, 121}
theorem cut447 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support447, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 930, OmissionResidual.support 928, OmissionResidual.support 438] ![OmissionResidual.demand 930, OmissionResidual.demand 928, OmissionResidual.demand 438] ![1, 1, 1]
    support447 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 930) (Fin.cases (hrows 928) (Fin.cases (hrows 438) (fun i => Fin.elim0 i))))
def support448 : Finset (Fin 154) := {67, 77, 84, 94, 96, 101, 103, 105, 112, 114, 120, 123, 127, 130, 133, 137, 142, 148}
theorem cut448 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support448, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1055, OmissionResidual.support 1056, OmissionResidual.support 1093] ![OmissionResidual.demand 1055, OmissionResidual.demand 1056, OmissionResidual.demand 1093] ![1, 1, 1]
    support448 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1055) (Fin.cases (hrows 1056) (Fin.cases (hrows 1093) (fun i => Fin.elim0 i))))
def support449 : Finset (Fin 154) := {67, 77, 84, 94, 96, 101, 103, 105, 112, 114, 120, 123, 127, 130, 133, 137, 142, 150}
theorem cut449 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support449, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1055, OmissionResidual.support 1056, OmissionResidual.support 1094] ![OmissionResidual.demand 1055, OmissionResidual.demand 1056, OmissionResidual.demand 1094] ![1, 1, 1]
    support449 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1055) (Fin.cases (hrows 1056) (Fin.cases (hrows 1094) (fun i => Fin.elim0 i))))
def support450 : Finset (Fin 154) := {2, 4, 10, 13, 14, 15, 21, 25, 28, 31, 34, 38, 44, 56, 63, 78}
theorem cut450 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support450, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 120, OmissionResidual.support 10, OmissionResidual.support 77] ![OmissionResidual.demand 120, OmissionResidual.demand 10, OmissionResidual.demand 77] ![1, 1, 1]
    support450 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 120) (Fin.cases (hrows 10) (Fin.cases (hrows 77) (fun i => Fin.elim0 i))))
#print axioms cut450
def support451 : Finset (Fin 154) := {5, 8, 10, 13, 14, 15, 21, 25, 28, 31, 34, 38, 44, 56, 63, 78}
theorem cut451 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support451, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 120, OmissionResidual.support 30, OmissionResidual.support 77] ![OmissionResidual.demand 120, OmissionResidual.demand 30, OmissionResidual.demand 77] ![1, 1, 1]
    support451 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 120) (Fin.cases (hrows 30) (Fin.cases (hrows 77) (fun i => Fin.elim0 i))))
def support452 : Finset (Fin 154) := {10, 14, 20, 21, 25, 29, 33, 36, 47, 52, 56, 67, 72, 78, 87}
theorem cut452 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support452, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 75, OmissionResidual.support 868, OmissionResidual.support 877] ![OmissionResidual.demand 75, OmissionResidual.demand 868, OmissionResidual.demand 877] ![1, 1, 1]
    support452 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 75) (Fin.cases (hrows 868) (Fin.cases (hrows 877) (fun i => Fin.elim0 i))))
def support453 : Finset (Fin 154) := {26, 35, 48, 58, 61, 64, 69, 73, 75, 80, 81, 84, 86, 92, 95, 104, 120}
theorem cut453 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support453, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 617, OmissionResidual.support 731, OmissionResidual.support 616] ![OmissionResidual.demand 617, OmissionResidual.demand 731, OmissionResidual.demand 616] ![1, 1, 1]
    support453 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 617) (Fin.cases (hrows 731) (Fin.cases (hrows 616) (fun i => Fin.elim0 i))))
def support454 : Finset (Fin 154) := {36, 46, 60, 64, 70, 75, 80, 86, 87, 92, 97, 102, 104, 113}
theorem cut454 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support454, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 673, OmissionResidual.support 779, OmissionResidual.support 675] ![OmissionResidual.demand 673, OmissionResidual.demand 779, OmissionResidual.demand 675] ![1, 1, 1]
    support454 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 673) (Fin.cases (hrows 779) (Fin.cases (hrows 675) (fun i => Fin.elim0 i))))
def support455 : Finset (Fin 154) := {2, 7, 16, 24, 26, 35, 36, 40, 46, 49, 64, 75, 80, 86, 92, 104}
theorem cut455 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support455, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 617, OmissionResidual.support 472, OmissionResidual.support 673] ![OmissionResidual.demand 617, OmissionResidual.demand 472, OmissionResidual.demand 673] ![1, 1, 1]
    support455 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 617) (Fin.cases (hrows 472) (Fin.cases (hrows 673) (fun i => Fin.elim0 i))))
def support456 : Finset (Fin 154) := {26, 35, 48, 58, 61, 64, 69, 73, 75, 80, 81, 84, 86, 92, 95, 104, 112}
theorem cut456 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support456, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 617, OmissionResidual.support 730, OmissionResidual.support 616] ![OmissionResidual.demand 617, OmissionResidual.demand 730, OmissionResidual.demand 616] ![1, 1, 1]
    support456 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 617) (Fin.cases (hrows 730) (Fin.cases (hrows 616) (fun i => Fin.elim0 i))))
def support457 : Finset (Fin 154) := {4, 6, 7, 8, 11, 12, 13, 14, 18, 20, 21, 23, 27, 31, 35, 37, 40, 41, 42, 46, 51, 52, 57, 59, 62, 70}
theorem cut457 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support457, holes i := by
  apply rounded_cover_cut ![support76, OmissionResidual.support 491, support393] ![2, OmissionResidual.demand 491, 2] ![1, 1, 1]
    support457 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut76 holes hbool hrows) (Fin.cases (hrows 491) (Fin.cases (cut393 holes hbool hrows) (fun i => Fin.elim0 i))))
def support458 : Finset (Fin 154) := {28, 36, 40, 46, 49, 51, 59, 61, 64, 80, 87, 92, 97, 102, 113}
theorem cut458 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support458, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 737, OmissionResidual.support 623, OmissionResidual.support 675] ![OmissionResidual.demand 737, OmissionResidual.demand 623, OmissionResidual.demand 675] ![1, 1, 1]
    support458 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 737) (Fin.cases (hrows 623) (Fin.cases (hrows 675) (fun i => Fin.elim0 i))))
def support459 : Finset (Fin 154) := {19, 26, 35, 48, 54, 58, 61, 66, 69, 73, 76, 80, 81, 84, 92, 95, 104, 120}
theorem cut459 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support459, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 731, OmissionResidual.support 888, OmissionResidual.support 887] ![OmissionResidual.demand 731, OmissionResidual.demand 888, OmissionResidual.demand 887] ![1, 1, 1]
    support459 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 731) (Fin.cases (hrows 888) (Fin.cases (hrows 887) (fun i => Fin.elim0 i))))
def support460 : Finset (Fin 154) := {38, 47, 51, 57, 60, 63, 66, 70, 78, 80, 81, 84, 98, 103, 112, 114, 121}
theorem cut460 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support460, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 930, OmissionResidual.support 949, OmissionResidual.support 681] ![OmissionResidual.demand 930, OmissionResidual.demand 949, OmissionResidual.demand 681] ![1, 1, 1]
    support460 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 930) (Fin.cases (hrows 949) (Fin.cases (hrows 681) (fun i => Fin.elim0 i))))
def support461 : Finset (Fin 154) := {38, 47, 48, 57, 58, 61, 66, 69, 73, 78, 80, 84, 98, 103, 112, 114, 121}
theorem cut461 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support461, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 930, OmissionResidual.support 730, OmissionResidual.support 929] ![OmissionResidual.demand 930, OmissionResidual.demand 730, OmissionResidual.demand 929] ![1, 1, 1]
    support461 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 930) (Fin.cases (hrows 730) (Fin.cases (hrows 929) (fun i => Fin.elim0 i))))
def support462 : Finset (Fin 154) := {38, 47, 48, 57, 58, 61, 66, 69, 73, 78, 80, 84, 98, 103, 112, 114, 120, 121}
theorem cut462 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support462, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 930, OmissionResidual.support 731, OmissionResidual.support 929] ![OmissionResidual.demand 930, OmissionResidual.demand 731, OmissionResidual.demand 929] ![1, 1, 1]
    support462 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 930) (Fin.cases (hrows 731) (Fin.cases (hrows 929) (fun i => Fin.elim0 i))))
def support463 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 60, 61, 63, 66, 69, 70, 73, 78, 80, 84, 92, 98, 102, 103, 112, 114, 120, 121}
theorem cut463 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support463, holes i := by
  apply rounded_cover_cut ![support155, OmissionResidual.support 950, support461] ![2, OmissionResidual.demand 950, 3] ![1, 1, 1]
    support463 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut155 holes hbool hrows) (Fin.cases (hrows 950) (Fin.cases (cut461 holes hbool hrows) (fun i => Fin.elim0 i))))
def support464 : Finset (Fin 154) := {5, 9, 12, 16, 18, 24, 26, 27, 31, 32, 39, 47, 51, 60}
theorem cut464 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support464, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 506, OmissionResidual.support 482, OmissionResidual.support 485] ![OmissionResidual.demand 506, OmissionResidual.demand 482, OmissionResidual.demand 485] ![1, 1, 1]
    support464 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 506) (Fin.cases (hrows 482) (Fin.cases (hrows 485) (fun i => Fin.elim0 i))))
def support465 : Finset (Fin 154) := {62, 71, 77, 81, 82, 83, 86, 89, 92, 93, 94, 97, 102, 103, 106, 108, 112, 116, 120, 121, 124, 130, 134, 144}
theorem cut465 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support465, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 798, support121, support401] ![OmissionResidual.demand 798, 2, 2] ![1, 1, 1]
    support465 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 798) (Fin.cases (cut121 holes hbool hrows) (Fin.cases (cut401 holes hbool hrows) (fun i => Fin.elim0 i))))
def support466 : Finset (Fin 154) := {2, 4, 7, 9, 10, 15, 16, 18, 19, 20, 24, 25, 26, 27, 28, 32, 34, 36, 37, 40, 42, 47, 49, 51, 52, 54, 60, 62, 64}
theorem cut466 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support466, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 848, support322, OmissionResidual.support 514, OmissionResidual.support 506, OmissionResidual.support 12] ![OmissionResidual.demand 848, 2, OmissionResidual.demand 514, OmissionResidual.demand 506, OmissionResidual.demand 12] ![1, 1, 1, 1, 1]
    support466 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 848) (Fin.cases (cut322 holes hbool hrows) (Fin.cases (hrows 514) (Fin.cases (hrows 506) (Fin.cases (hrows 12) (fun i => Fin.elim0 i))))))
def support467 : Finset (Fin 154) := {8, 12, 21, 27, 33, 35, 44, 46, 55, 57, 59, 66, 70, 74, 85}
theorem cut467 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support467, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 862, OmissionResidual.support 890, OmissionResidual.support 51] ![OmissionResidual.demand 862, OmissionResidual.demand 890, OmissionResidual.demand 51] ![1, 1, 1]
    support467 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 862) (Fin.cases (hrows 890) (Fin.cases (hrows 51) (fun i => Fin.elim0 i))))
def support468 : Finset (Fin 154) := {43, 65, 74, 85, 87, 95, 96, 105, 107, 110, 114, 118, 123, 125, 132, 137}
theorem cut468 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support468, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1045, OmissionResidual.support 1006, OmissionResidual.support 1097] ![OmissionResidual.demand 1045, OmissionResidual.demand 1006, OmissionResidual.demand 1097] ![1, 1, 1]
    support468 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1045) (Fin.cases (hrows 1006) (Fin.cases (hrows 1097) (fun i => Fin.elim0 i))))
def support469 : Finset (Fin 154) := {51, 60, 66, 70, 73, 78, 81, 83, 88, 92, 93, 98, 102, 105, 112, 121}
theorem cut469 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support469, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 947, OmissionResidual.support 950, OmissionResidual.support 438] ![OmissionResidual.demand 947, OmissionResidual.demand 950, OmissionResidual.demand 438] ![1, 1, 1]
    support469 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 947) (Fin.cases (hrows 950) (Fin.cases (hrows 438) (fun i => Fin.elim0 i))))
def support470 : Finset (Fin 154) := {0, 1, 4, 7, 8, 11, 12, 14, 16, 17, 20, 23, 25, 30, 33, 35, 43, 46, 53, 59, 64, 74}
theorem cut470 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support470, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 844, support171, OmissionResidual.support 4] ![OmissionResidual.demand 844, 2, OmissionResidual.demand 4] ![1, 1, 1]
    support470 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 844) (Fin.cases (cut171 holes hbool hrows) (Fin.cases (hrows 4) (fun i => Fin.elim0 i))))
def support471 : Finset (Fin 154) := {51, 60, 66, 70, 73, 78, 81, 83, 88, 93, 98, 102, 103, 105, 114, 120, 128}
theorem cut471 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support471, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 949, OmissionResidual.support 947, OmissionResidual.support 439] ![OmissionResidual.demand 949, OmissionResidual.demand 947, OmissionResidual.demand 439] ![1, 1, 1]
    support471 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 949) (Fin.cases (hrows 947) (Fin.cases (hrows 439) (fun i => Fin.elim0 i))))
def support472 : Finset (Fin 154) := {26, 35, 48, 58, 61, 64, 69, 73, 75, 80, 81, 84, 86, 92, 94, 95, 103, 104, 106, 112, 116, 120, 124, 144}
theorem cut472 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support472, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 843, support453, support456] ![OmissionResidual.demand 843, 2, 2] ![1, 1, 1]
    support472 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 843) (Fin.cases (cut453 holes hbool hrows) (Fin.cases (cut456 holes hbool hrows) (fun i => Fin.elim0 i))))
def support473 : Finset (Fin 154) := {50, 65, 70, 77, 81, 85, 93, 95, 96, 97, 105, 110, 114, 123, 132, 137}
theorem cut473 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support473, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1045, OmissionResidual.support 1075, OmissionResidual.support 740] ![OmissionResidual.demand 1045, OmissionResidual.demand 1075, OmissionResidual.demand 740] ![1, 1, 1]
    support473 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1045) (Fin.cases (hrows 1075) (Fin.cases (hrows 740) (fun i => Fin.elim0 i))))
def support474 : Finset (Fin 154) := {2, 4, 10, 13, 14, 15, 21, 25, 28, 29, 31, 34, 38, 39, 44, 52, 56, 59, 63, 67, 70, 78, 82, 96}
theorem cut474 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support474, holes i := by
  apply rounded_cover_cut ![support450, OmissionResidual.support 75, OmissionResidual.support 916] ![2, OmissionResidual.demand 75, OmissionResidual.demand 916] ![1, 1, 1]
    support474 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut450 holes hbool hrows) (Fin.cases (hrows 75) (Fin.cases (hrows 916) (fun i => Fin.elim0 i))))
def support475 : Finset (Fin 154) := {5, 8, 10, 13, 14, 15, 21, 25, 28, 29, 31, 34, 38, 39, 44, 52, 56, 59, 63, 67, 70, 78, 82, 96}
theorem cut475 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support475, holes i := by
  apply rounded_cover_cut ![support451, OmissionResidual.support 75, OmissionResidual.support 916] ![2, OmissionResidual.demand 75, OmissionResidual.demand 916] ![1, 1, 1]
    support475 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut451 holes hbool hrows) (Fin.cases (hrows 75) (Fin.cases (hrows 916) (fun i => Fin.elim0 i))))
#print axioms cut475
def support476 : Finset (Fin 154) := {43, 74, 75, 77, 85, 95, 96, 105, 107, 110, 114, 118, 123, 125, 132, 137}
theorem cut476 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support476, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1006, OmissionResidual.support 1075, OmissionResidual.support 1068] ![OmissionResidual.demand 1006, OmissionResidual.demand 1075, OmissionResidual.demand 1068] ![1, 1, 1]
    support476 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1006) (Fin.cases (hrows 1075) (Fin.cases (hrows 1068) (fun i => Fin.elim0 i))))
def support477 : Finset (Fin 154) := {53, 65, 74, 85, 87, 95, 96, 105, 107, 110, 114, 118, 123, 125, 132, 137}
theorem cut477 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support477, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1045, OmissionResidual.support 1097, OmissionResidual.support 1021] ![OmissionResidual.demand 1045, OmissionResidual.demand 1097, OmissionResidual.demand 1021] ![1, 1, 1]
    support477 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1045) (Fin.cases (hrows 1097) (Fin.cases (hrows 1021) (fun i => Fin.elim0 i))))
def support478 : Finset (Fin 154) := {26, 35, 64, 69, 74, 75, 81, 85, 86, 95, 104, 113, 118, 122, 126, 136}
theorem cut478 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support478, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1043, OmissionResidual.support 616, OmissionResidual.support 1069] ![OmissionResidual.demand 1043, OmissionResidual.demand 616, OmissionResidual.demand 1069] ![1, 1, 1]
    support478 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1043) (Fin.cases (hrows 616) (Fin.cases (hrows 1069) (fun i => Fin.elim0 i))))
def support479 : Finset (Fin 154) := {83, 93, 94, 97, 99, 102, 103, 106, 107, 108, 112, 116, 118, 120, 122, 124, 129, 134, 135, 140, 143, 144, 149}
theorem cut479 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support479, holes i := by
  apply rounded_cover_cut ![support74, support106, OmissionResidual.support 1128] ![2, 2, OmissionResidual.demand 1128] ![1, 1, 1]
    support479 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut74 holes hbool hrows) (Fin.cases (cut106 holes hbool hrows) (Fin.cases (hrows 1128) (fun i => Fin.elim0 i))))
def support480 : Finset (Fin 154) := {83, 93, 94, 97, 99, 102, 103, 106, 107, 108, 112, 116, 118, 120, 122, 124, 129, 134, 135, 140, 143, 149}
theorem cut480 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support480, holes i := by
  apply rounded_cover_cut ![support74, OmissionResidual.support 1128, support48] ![2, OmissionResidual.demand 1128, 2] ![1, 1, 1]
    support480 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut74 holes hbool hrows) (Fin.cases (hrows 1128) (Fin.cases (cut48 holes hbool hrows) (fun i => Fin.elim0 i))))
def support481 : Finset (Fin 154) := {108, 115, 122, 124, 126, 129, 130, 134, 135, 138, 140, 143, 144, 146, 151, 152}
theorem cut481 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support481, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1159, OmissionResidual.support 1143, OmissionResidual.support 1140] ![OmissionResidual.demand 1159, OmissionResidual.demand 1143, OmissionResidual.demand 1140] ![1, 1, 1]
    support481 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1159) (Fin.cases (hrows 1143) (Fin.cases (hrows 1140) (fun i => Fin.elim0 i))))
def support482 : Finset (Fin 154) := {108, 115, 122, 124, 126, 129, 130, 134, 135, 138, 140, 143, 144, 146, 151, 153}
theorem cut482 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support482, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1160, OmissionResidual.support 1143, OmissionResidual.support 1140] ![OmissionResidual.demand 1160, OmissionResidual.demand 1143, OmissionResidual.demand 1140] ![1, 1, 1]
    support482 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1160) (Fin.cases (hrows 1143) (Fin.cases (hrows 1140) (fun i => Fin.elim0 i))))
def support483 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 61, 63, 69, 71, 73, 76, 80, 81, 84, 88, 92, 98, 102, 103, 112, 120, 124, 128, 130, 135, 138, 140, 143, 144, 152, 153}
theorem cut483 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support483, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 960, OmissionResidual.support 1159, OmissionResidual.support 1160, support1, OmissionResidual.support 679, OmissionResidual.support 680] ![OmissionResidual.demand 960, OmissionResidual.demand 1159, OmissionResidual.demand 1160, 3, OmissionResidual.demand 679, OmissionResidual.demand 680] ![1, 1, 1, 1, 1, 1]
    support483 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 960) (Fin.cases (hrows 1159) (Fin.cases (hrows 1160) (Fin.cases (cut1 holes hbool hrows) (Fin.cases (hrows 679) (Fin.cases (hrows 680) (fun i => Fin.elim0 i)))))))
def support484 : Finset (Fin 154) := {84, 88, 94, 97, 103, 105, 112, 113, 119, 120, 121, 124, 127, 128, 130, 133, 134, 135, 138, 140, 143, 144, 145, 146, 148, 152}
theorem cut484 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support484, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1159, support108, support174] ![OmissionResidual.demand 1159, 3, 3] ![1, 1, 1]
    support484 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1159) (Fin.cases (cut108 holes hbool hrows) (Fin.cases (cut174 holes hbool hrows) (fun i => Fin.elim0 i))))
def support485 : Finset (Fin 154) := {84, 88, 94, 97, 103, 105, 112, 113, 119, 120, 121, 124, 127, 128, 130, 133, 134, 135, 138, 140, 143, 144, 145, 146, 148, 153}
theorem cut485 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support485, holes i := by
  apply rounded_cover_cut ![support108, OmissionResidual.support 1160, support174] ![3, OmissionResidual.demand 1160, 3] ![1, 1, 1]
    support485 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut108 holes hbool hrows) (Fin.cases (hrows 1160) (Fin.cases (cut174 holes hbool hrows) (fun i => Fin.elim0 i))))
def support486 : Finset (Fin 154) := {1, 7, 11, 18, 21, 24, 27, 31, 39, 44, 46, 57, 59, 67, 70, 78, 82, 96}
theorem cut486 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support486, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 916, OmissionResidual.support 469, OmissionResidual.support 894] ![OmissionResidual.demand 916, OmissionResidual.demand 469, OmissionResidual.demand 894] ![1, 1, 1]
    support486 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 916) (Fin.cases (hrows 469) (Fin.cases (hrows 894) (fun i => Fin.elim0 i))))
def support487 : Finset (Fin 154) := {6, 14, 17, 21, 29, 42, 52, 56, 62, 67, 72, 83, 94, 98, 106}
theorem cut487 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support487, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 46, OmissionResidual.support 344, OmissionResidual.support 386] ![OmissionResidual.demand 46, OmissionResidual.demand 344, OmissionResidual.demand 386] ![1, 1, 1]
    support487 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 46) (Fin.cases (hrows 344) (Fin.cases (hrows 386) (fun i => Fin.elim0 i))))
def support488 : Finset (Fin 154) := {10, 14, 21, 25, 29, 42, 52, 56, 62, 67, 72, 83, 94, 98, 106}
theorem cut488 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support488, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 75, OmissionResidual.support 344, OmissionResidual.support 386] ![OmissionResidual.demand 75, OmissionResidual.demand 344, OmissionResidual.demand 386] ![1, 1, 1]
    support488 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 75) (Fin.cases (hrows 344) (Fin.cases (hrows 386) (fun i => Fin.elim0 i))))
def support489 : Finset (Fin 154) := {2, 5, 6, 7, 9, 10, 11, 12, 15, 16, 18, 20, 24, 26, 27, 32, 36, 37, 40, 42, 47, 49, 51, 52, 60, 62}
theorem cut489 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support489, holes i := by
  apply rounded_cover_cut ![support311, OmissionResidual.support 491, support338] ![2, OmissionResidual.demand 491, 2] ![1, 1, 1]
    support489 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut311 holes hbool hrows) (Fin.cases (hrows 491) (Fin.cases (cut338 holes hbool hrows) (fun i => Fin.elim0 i))))
def support490 : Finset (Fin 154) := {0, 4, 6, 8, 10, 14, 17, 20, 23, 25, 27, 33, 37, 56, 62, 67, 77}
theorem cut490 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support490, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 858, OmissionResidual.support 867, OmissionResidual.support 0] ![OmissionResidual.demand 858, OmissionResidual.demand 867, OmissionResidual.demand 0] ![1, 1, 1]
    support490 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 858) (Fin.cases (hrows 867) (Fin.cases (hrows 0) (fun i => Fin.elim0 i))))
def support491 : Finset (Fin 154) := {1, 4, 6, 8, 10, 14, 17, 20, 23, 25, 27, 33, 37, 56, 62, 67, 77}
theorem cut491 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support491, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 858, OmissionResidual.support 867, OmissionResidual.support 4] ![OmissionResidual.demand 858, OmissionResidual.demand 867, OmissionResidual.demand 4] ![1, 1, 1]
    support491 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 858) (Fin.cases (hrows 867) (Fin.cases (hrows 4) (fun i => Fin.elim0 i))))
def support492 : Finset (Fin 154) := {38, 47, 48, 57, 58, 61, 66, 69, 73, 78, 80, 83, 84, 88, 93, 98, 100, 102, 103, 105, 112, 114, 120, 121, 134}
theorem cut492 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support492, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 440, support461, support424] ![OmissionResidual.demand 440, 3, 3] ![1, 1, 1]
    support492 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 440) (Fin.cases (cut461 holes hbool hrows) (Fin.cases (cut424 holes hbool hrows) (fun i => Fin.elim0 i))))
def support493 : Finset (Fin 154) := {22, 29, 32, 37, 41, 42, 47, 48, 52, 57, 58, 61, 69, 73, 80, 83, 84, 103, 120}
theorem cut493 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support493, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 632, OmissionResidual.support 731, OmissionResidual.support 587] ![OmissionResidual.demand 632, OmissionResidual.demand 731, OmissionResidual.demand 587] ![1, 1, 1]
    support493 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 632) (Fin.cases (hrows 731) (Fin.cases (hrows 587) (fun i => Fin.elim0 i))))
def support494 : Finset (Fin 154) := {29, 37, 41, 47, 48, 52, 57, 58, 61, 69, 73, 80, 83, 84, 103, 120}
theorem cut494 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support494, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 632, OmissionResidual.support 731, OmissionResidual.support 629] ![OmissionResidual.demand 632, OmissionResidual.demand 731, OmissionResidual.demand 629] ![1, 1, 1]
    support494 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 632) (Fin.cases (hrows 731) (Fin.cases (hrows 629) (fun i => Fin.elim0 i))))
def support495 : Finset (Fin 154) := {22, 29, 32, 37, 41, 42, 47, 48, 52, 57, 58, 61, 69, 73, 80, 83, 84, 103, 112}
theorem cut495 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support495, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 632, OmissionResidual.support 730, OmissionResidual.support 587] ![OmissionResidual.demand 632, OmissionResidual.demand 730, OmissionResidual.demand 587] ![1, 1, 1]
    support495 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 632) (Fin.cases (hrows 730) (Fin.cases (hrows 587) (fun i => Fin.elim0 i))))
def support496 : Finset (Fin 154) := {29, 37, 41, 47, 48, 52, 57, 58, 61, 69, 73, 80, 83, 84, 103, 112}
theorem cut496 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support496, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 632, OmissionResidual.support 730, OmissionResidual.support 629] ![OmissionResidual.demand 632, OmissionResidual.demand 730, OmissionResidual.demand 629] ![1, 1, 1]
    support496 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 632) (Fin.cases (hrows 730) (Fin.cases (hrows 629) (fun i => Fin.elim0 i))))
def support497 : Finset (Fin 154) := {9, 13, 15, 19, 21, 22, 28, 29, 34, 38, 45, 48, 51, 56, 66, 73, 88}
theorem cut497 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support497, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 122, OmissionResidual.support 177, OmissionResidual.support 62] ![OmissionResidual.demand 122, OmissionResidual.demand 177, OmissionResidual.demand 62] ![1, 1, 1]
    support497 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 122) (Fin.cases (hrows 177) (Fin.cases (hrows 62) (fun i => Fin.elim0 i))))
def support498 : Finset (Fin 154) := {15, 21, 22, 28, 29, 34, 38, 45, 48, 51, 56, 66, 73, 88}
theorem cut498 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support498, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 122, OmissionResidual.support 177, OmissionResidual.support 116] ![OmissionResidual.demand 122, OmissionResidual.demand 177, OmissionResidual.demand 116] ![1, 1, 1]
    support498 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 122) (Fin.cases (hrows 177) (Fin.cases (hrows 116) (fun i => Fin.elim0 i))))
def support499 : Finset (Fin 154) := {38, 47, 57, 66, 69, 73, 78, 83, 88, 93, 98, 102, 103, 105, 114, 120, 128}
theorem cut499 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support499, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 927, OmissionResidual.support 929, OmissionResidual.support 439] ![OmissionResidual.demand 927, OmissionResidual.demand 929, OmissionResidual.demand 439] ![1, 1, 1]
    support499 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 927) (Fin.cases (hrows 929) (Fin.cases (hrows 439) (fun i => Fin.elim0 i))))
def support500 : Finset (Fin 154) := {38, 47, 57, 66, 69, 73, 78, 83, 88, 93, 98, 102, 103, 105, 112, 114, 121}
theorem cut500 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support500, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 927, OmissionResidual.support 929, OmissionResidual.support 438] ![OmissionResidual.demand 927, OmissionResidual.demand 929, OmissionResidual.demand 438] ![1, 1, 1]
    support500 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 927) (Fin.cases (hrows 929) (Fin.cases (hrows 438) (fun i => Fin.elim0 i))))
#print axioms cut500
def support501 : Finset (Fin 154) := {21, 27, 29, 31, 37, 41, 46, 52, 57, 61, 63, 69, 81, 82, 84, 103}
theorem cut501 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support501, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 632, OmissionResidual.support 583, OmissionResidual.support 581] ![OmissionResidual.demand 632, OmissionResidual.demand 583, OmissionResidual.demand 581] ![1, 1, 1]
    support501 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 632) (Fin.cases (hrows 583) (Fin.cases (hrows 581) (fun i => Fin.elim0 i))))
def support502 : Finset (Fin 154) := {51, 60, 66, 70, 81, 90, 92, 93, 100, 102, 108, 115, 122, 126, 134, 140, 143, 151}
theorem cut502 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support502, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 952, OmissionResidual.support 1143, OmissionResidual.support 951] ![OmissionResidual.demand 952, OmissionResidual.demand 1143, OmissionResidual.demand 951] ![1, 1, 1]
    support502 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 952) (Fin.cases (hrows 1143) (Fin.cases (hrows 951) (fun i => Fin.elim0 i))))
def support503 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 61, 62, 63, 69, 73, 77, 80, 82, 84, 89, 93, 102, 103, 112, 116, 123}
theorem cut503 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support503, holes i := by
  apply rounded_cover_cut ![support59, support47, OmissionResidual.support 797] ![2, 2, OmissionResidual.demand 797] ![1, 1, 1]
    support503 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut59 holes hbool hrows) (Fin.cases (cut47 holes hbool hrows) (Fin.cases (hrows 797) (fun i => Fin.elim0 i))))
def support504 : Finset (Fin 154) := {15, 21, 28, 32, 34, 41, 45, 48, 51, 56, 61, 73, 76, 88}
theorem cut504 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support504, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 118, OmissionResidual.support 122, OmissionResidual.support 269] ![OmissionResidual.demand 118, OmissionResidual.demand 122, OmissionResidual.demand 269] ![1, 1, 1]
    support504 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 118) (Fin.cases (hrows 122) (Fin.cases (hrows 269) (fun i => Fin.elim0 i))))
def support505 : Finset (Fin 154) := {9, 13, 15, 19, 21, 28, 32, 34, 41, 45, 48, 51, 56, 61, 73, 76, 88}
theorem cut505 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support505, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 64, OmissionResidual.support 122, OmissionResidual.support 269] ![OmissionResidual.demand 64, OmissionResidual.demand 122, OmissionResidual.demand 269] ![1, 1, 1]
    support505 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 64) (Fin.cases (hrows 122) (Fin.cases (hrows 269) (fun i => Fin.elim0 i))))
def support506 : Finset (Fin 154) := {19, 26, 29, 35, 37, 38, 40, 41, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 83, 84, 92, 93, 94, 103, 120}
theorem cut506 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support506, holes i := by
  apply rounded_cover_cut ![support494, OmissionResidual.support 572, support77] ![2, OmissionResidual.demand 572, 2] ![1, 1, 1]
    support506 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut494 holes hbool hrows) (Fin.cases (hrows 572) (Fin.cases (cut77 holes hbool hrows) (fun i => Fin.elim0 i))))
def support507 : Finset (Fin 154) := {19, 26, 29, 35, 37, 38, 40, 41, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 83, 84, 92, 93, 94, 103, 112}
theorem cut507 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support507, holes i := by
  apply rounded_cover_cut ![support496, OmissionResidual.support 572, support77] ![2, OmissionResidual.demand 572, 2] ![1, 1, 1]
    support507 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut496 holes hbool hrows) (Fin.cases (hrows 572) (Fin.cases (cut77 holes hbool hrows) (fun i => Fin.elim0 i))))
def support508 : Finset (Fin 154) := {19, 22, 26, 29, 32, 35, 37, 38, 40, 41, 42, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 83, 84, 92, 93, 94, 103, 120}
theorem cut508 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support508, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, support493, support77] ![OmissionResidual.demand 572, 2, 2] ![1, 1, 1]
    support508 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (cut493 holes hbool hrows) (Fin.cases (cut77 holes hbool hrows) (fun i => Fin.elim0 i))))
def support509 : Finset (Fin 154) := {19, 22, 26, 29, 32, 35, 37, 38, 40, 41, 42, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 83, 84, 92, 93, 94, 103, 112}
theorem cut509 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support509, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, support495, support77] ![OmissionResidual.demand 572, 2, 2] ![1, 1, 1]
    support509 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (cut495 holes hbool hrows) (Fin.cases (cut77 holes hbool hrows) (fun i => Fin.elim0 i))))
def support510 : Finset (Fin 154) := {42, 56, 62, 68, 72, 83, 91, 94, 117, 124, 130, 133, 135, 138, 139, 140, 144, 152}
theorem cut510 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support510, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1005, OmissionResidual.support 944, OmissionResidual.support 1154] ![OmissionResidual.demand 1005, OmissionResidual.demand 944, OmissionResidual.demand 1154] ![1, 1, 1]
    support510 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1005) (Fin.cases (hrows 944) (Fin.cases (hrows 1154) (fun i => Fin.elim0 i))))
def support511 : Finset (Fin 154) := {42, 56, 62, 68, 72, 83, 91, 94, 117, 124, 130, 133, 135, 138, 139, 140, 144, 153}
theorem cut511 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support511, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1005, OmissionResidual.support 944, OmissionResidual.support 1155] ![OmissionResidual.demand 1005, OmissionResidual.demand 944, OmissionResidual.demand 1155] ![1, 1, 1]
    support511 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1005) (Fin.cases (hrows 944) (Fin.cases (hrows 1155) (fun i => Fin.elim0 i))))
def support512 : Finset (Fin 154) := {9, 13, 19, 22, 24, 29, 31, 34, 38, 40, 45, 48, 56, 61, 73, 76, 88}
theorem cut512 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support512, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 64, OmissionResidual.support 177, OmissionResidual.support 201] ![OmissionResidual.demand 64, OmissionResidual.demand 177, OmissionResidual.demand 201] ![1, 1, 1]
    support512 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 64) (Fin.cases (hrows 177) (Fin.cases (hrows 201) (fun i => Fin.elim0 i))))
def support513 : Finset (Fin 154) := {61, 71, 73, 76, 81, 83, 88, 92, 93, 100, 102, 109, 112, 113, 116, 120, 123, 129, 132, 134, 143, 144, 152}
theorem cut513 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support513, holes i := by
  apply rounded_cover_cut ![support374, support373, OmissionResidual.support 404] ![3, 3, OmissionResidual.demand 404] ![1, 1, 1]
    support513 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut374 holes hbool hrows) (Fin.cases (cut373 holes hbool hrows) (Fin.cases (hrows 404) (fun i => Fin.elim0 i))))
def support514 : Finset (Fin 154) := {31, 39, 44, 49, 59, 64, 71, 79, 81, 83, 93, 99, 100, 108, 115}
theorem cut514 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support514, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 922, OmissionResidual.support 921, OmissionResidual.support 738] ![OmissionResidual.demand 922, OmissionResidual.demand 921, OmissionResidual.demand 738] ![1, 1, 1]
    support514 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 922) (Fin.cases (hrows 921) (Fin.cases (hrows 738) (fun i => Fin.elim0 i))))
def support515 : Finset (Fin 154) := {15, 21, 22, 24, 28, 29, 31, 34, 38, 40, 45, 48, 56, 61, 73, 76, 88}
theorem cut515 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support515, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 118, OmissionResidual.support 177, OmissionResidual.support 201] ![OmissionResidual.demand 118, OmissionResidual.demand 177, OmissionResidual.demand 201] ![1, 1, 1]
    support515 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 118) (Fin.cases (hrows 177) (Fin.cases (hrows 201) (fun i => Fin.elim0 i))))
def support516 : Finset (Fin 154) := {22, 29, 38, 45, 48, 56, 73, 83, 84, 88, 93, 98, 102, 120, 128}
theorem cut516 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support516, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 179, OmissionResidual.support 177, OmissionResidual.support 439] ![OmissionResidual.demand 179, OmissionResidual.demand 177, OmissionResidual.demand 439] ![1, 1, 1]
    support516 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 179) (Fin.cases (hrows 177) (Fin.cases (hrows 439) (fun i => Fin.elim0 i))))
def support517 : Finset (Fin 154) := {22, 29, 38, 45, 48, 56, 73, 83, 84, 88, 93, 98, 102, 112, 121}
theorem cut517 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support517, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 179, OmissionResidual.support 177, OmissionResidual.support 438] ![OmissionResidual.demand 179, OmissionResidual.demand 177, OmissionResidual.demand 438] ![1, 1, 1]
    support517 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 179) (Fin.cases (hrows 177) (Fin.cases (hrows 438) (fun i => Fin.elim0 i))))
def support518 : Finset (Fin 154) := {97, 105, 106, 113, 114, 121, 126, 128, 132, 134, 135, 138, 144, 145, 146, 150}
theorem cut518 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support518, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1120, OmissionResidual.support 1119, OmissionResidual.support 1139] ![OmissionResidual.demand 1120, OmissionResidual.demand 1119, OmissionResidual.demand 1139] ![1, 1, 1]
    support518 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1120) (Fin.cases (hrows 1119) (Fin.cases (hrows 1139) (fun i => Fin.elim0 i))))
def support519 : Finset (Fin 154) := {0, 4, 6, 8, 10, 11, 14, 16, 17, 20, 23, 25, 27, 30, 32, 33, 37, 39, 41, 50, 56, 62, 67, 77}
theorem cut519 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support519, holes i := by
  apply rounded_cover_cut ![support20, support490, OmissionResidual.support 512] ![3, 3, OmissionResidual.demand 512] ![1, 1, 1]
    support519 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut20 holes hbool hrows) (Fin.cases (cut490 holes hbool hrows) (Fin.cases (hrows 512) (fun i => Fin.elim0 i))))
def support520 : Finset (Fin 154) := {1, 4, 6, 8, 10, 11, 14, 16, 17, 20, 23, 25, 27, 30, 32, 33, 37, 39, 41, 50, 56, 62, 67, 77}
theorem cut520 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support520, holes i := by
  apply rounded_cover_cut ![support21, support491, OmissionResidual.support 512] ![3, 3, OmissionResidual.demand 512] ![1, 1, 1]
    support520 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut21 holes hbool hrows) (Fin.cases (cut491 holes hbool hrows) (Fin.cases (hrows 512) (fun i => Fin.elim0 i))))
def support521 : Finset (Fin 154) := {0, 1, 4, 6, 8, 10, 11, 14, 16, 17, 20, 23, 25, 27, 30, 32, 33, 37, 39, 41, 50, 56, 62, 67, 77}
theorem cut521 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support521, holes i := by
  apply rounded_cover_cut ![support20, support491, OmissionResidual.support 512] ![3, 3, OmissionResidual.demand 512] ![1, 1, 1]
    support521 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut20 holes hbool hrows) (Fin.cases (cut491 holes hbool hrows) (Fin.cases (hrows 512) (fun i => Fin.elim0 i))))
def support522 : Finset (Fin 154) := {6, 11, 14, 20, 21, 27, 33, 37, 42, 44, 46, 52, 57, 62, 67, 78, 82, 96}
theorem cut522 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support522, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 491, OmissionResidual.support 878, OmissionResidual.support 894] ![OmissionResidual.demand 491, OmissionResidual.demand 878, OmissionResidual.demand 894] ![1, 1, 1]
    support522 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 491) (Fin.cases (hrows 878) (Fin.cases (hrows 894) (fun i => Fin.elim0 i))))
def support523 : Finset (Fin 154) := {51, 60, 66, 70, 73, 78, 83, 88, 92, 93, 98, 102, 112, 113, 121}
theorem cut523 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support523, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 948, OmissionResidual.support 950, OmissionResidual.support 438] ![OmissionResidual.demand 948, OmissionResidual.demand 950, OmissionResidual.demand 438] ![1, 1, 1]
    support523 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 948) (Fin.cases (hrows 950) (Fin.cases (hrows 438) (fun i => Fin.elim0 i))))
def support524 : Finset (Fin 154) := {10, 14, 16, 20, 21, 27, 33, 37, 42, 44, 46, 52, 57, 62, 67, 78, 82, 96}
theorem cut524 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support524, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 878, OmissionResidual.support 514, OmissionResidual.support 894] ![OmissionResidual.demand 878, OmissionResidual.demand 514, OmissionResidual.demand 894] ![1, 1, 1]
    support524 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 878) (Fin.cases (hrows 514) (Fin.cases (hrows 894) (fun i => Fin.elim0 i))))
def support525 : Finset (Fin 154) := {29, 37, 38, 41, 47, 51, 52, 57, 58, 63, 69, 73, 83, 84, 103}
theorem cut525 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support525, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 632, OmissionResidual.support 629, OmissionResidual.support 680] ![OmissionResidual.demand 632, OmissionResidual.demand 629, OmissionResidual.demand 680] ![1, 1, 1]
    support525 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 632) (Fin.cases (hrows 629) (Fin.cases (hrows 680) (fun i => Fin.elim0 i))))
#print axioms cut525
def support526 : Finset (Fin 154) := {5, 9, 12, 15, 16, 18, 24, 26, 27, 34, 36, 40, 45, 49, 58, 71, 76, 86}
theorem cut526 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support526, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 483, OmissionResidual.support 864, OmissionResidual.support 880] ![OmissionResidual.demand 483, OmissionResidual.demand 864, OmissionResidual.demand 880] ![1, 1, 1]
    support526 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 483) (Fin.cases (hrows 864) (Fin.cases (hrows 880) (fun i => Fin.elim0 i))))
def support527 : Finset (Fin 154) := {2, 7, 9, 15, 16, 18, 24, 26, 27, 34, 36, 40, 45, 49, 58, 71, 76, 86}
theorem cut527 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support527, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 864, OmissionResidual.support 472, OmissionResidual.support 880] ![OmissionResidual.demand 864, OmissionResidual.demand 472, OmissionResidual.demand 880] ![1, 1, 1]
    support527 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 864) (Fin.cases (hrows 472) (Fin.cases (hrows 880) (fun i => Fin.elim0 i))))
def support528 : Finset (Fin 154) := {32, 42, 45, 50, 56, 60, 62, 68, 71, 72, 83, 94, 98, 100, 106, 108}
theorem cut528 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support528, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 344, OmissionResidual.support 924, OmissionResidual.support 925] ![OmissionResidual.demand 344, OmissionResidual.demand 924, OmissionResidual.demand 925] ![1, 1, 1]
    support528 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 344) (Fin.cases (hrows 924) (Fin.cases (hrows 925) (fun i => Fin.elim0 i))))
def support529 : Finset (Fin 154) := {22, 29, 32, 37, 38, 41, 42, 47, 51, 52, 57, 58, 63, 69, 73, 83, 84, 103}
theorem cut529 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support529, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 632, OmissionResidual.support 587, OmissionResidual.support 680] ![OmissionResidual.demand 632, OmissionResidual.demand 587, OmissionResidual.demand 680] ![1, 1, 1]
    support529 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 632) (Fin.cases (hrows 587) (Fin.cases (hrows 680) (fun i => Fin.elim0 i))))
def support530 : Finset (Fin 154) := {19, 26, 29, 35, 37, 38, 40, 41, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 83, 84, 92, 103, 120}
theorem cut530 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support530, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, support525, support494] ![OmissionResidual.demand 572, 2, 2] ![1, 1, 1]
    support530 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (cut525 holes hbool hrows) (Fin.cases (cut494 holes hbool hrows) (fun i => Fin.elim0 i))))
def support531 : Finset (Fin 154) := {19, 26, 29, 35, 37, 38, 40, 41, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 83, 84, 92, 103, 112}
theorem cut531 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support531, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, support525, support496] ![OmissionResidual.demand 572, 2, 2] ![1, 1, 1]
    support531 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (cut525 holes hbool hrows) (Fin.cases (cut496 holes hbool hrows) (fun i => Fin.elim0 i))))
def support532 : Finset (Fin 154) := {19, 22, 26, 29, 32, 35, 37, 38, 40, 41, 42, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 83, 84, 92, 103, 120}
theorem cut532 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support532, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, support525, support493] ![OmissionResidual.demand 572, 2, 2] ![1, 1, 1]
    support532 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (cut525 holes hbool hrows) (Fin.cases (cut493 holes hbool hrows) (fun i => Fin.elim0 i))))
def support533 : Finset (Fin 154) := {19, 22, 26, 29, 32, 35, 37, 38, 40, 41, 42, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 83, 84, 92, 103, 112}
theorem cut533 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support533, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, support525, support495] ![OmissionResidual.demand 572, 2, 2] ![1, 1, 1]
    support533 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (cut525 holes hbool hrows) (Fin.cases (cut495 holes hbool hrows) (fun i => Fin.elim0 i))))
def support534 : Finset (Fin 154) := {13, 15, 18, 21, 22, 24, 28, 29, 31, 32, 34, 35, 38, 40, 41, 45, 48, 51, 56, 57, 61, 70, 73, 76, 88}
theorem cut534 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support534, holes i := by
  apply rounded_cover_cut ![support504, support515, OmissionResidual.support 529] ![2, 2, OmissionResidual.demand 529] ![1, 1, 1]
    support534 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut504 holes hbool hrows) (Fin.cases (cut515 holes hbool hrows) (Fin.cases (hrows 529) (fun i => Fin.elim0 i))))
def support535 : Finset (Fin 154) := {9, 13, 15, 18, 19, 21, 22, 24, 28, 29, 31, 32, 34, 35, 38, 40, 41, 45, 48, 51, 56, 57, 61, 70, 73, 76, 88}
theorem cut535 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support535, holes i := by
  apply rounded_cover_cut ![support512, support504, OmissionResidual.support 529] ![2, 2, OmissionResidual.demand 529] ![1, 1, 1]
    support535 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut512 holes hbool hrows) (Fin.cases (cut504 holes hbool hrows) (Fin.cases (hrows 529) (fun i => Fin.elim0 i))))
def support536 : Finset (Fin 154) := {28, 29, 36, 37, 38, 40, 41, 46, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 83, 84, 92, 103, 120}
theorem cut536 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support536, holes i := by
  apply rounded_cover_cut ![support525, support494, OmissionResidual.support 623] ![2, 2, OmissionResidual.demand 623] ![1, 1, 1]
    support536 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut525 holes hbool hrows) (Fin.cases (cut494 holes hbool hrows) (Fin.cases (hrows 623) (fun i => Fin.elim0 i))))
def support537 : Finset (Fin 154) := {28, 29, 36, 37, 38, 40, 41, 46, 47, 48, 51, 52, 57, 58, 61, 63, 69, 73, 80, 83, 84, 92, 103, 112}
theorem cut537 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support537, holes i := by
  apply rounded_cover_cut ![support525, support496, OmissionResidual.support 623] ![2, 2, OmissionResidual.demand 623] ![1, 1, 1]
    support537 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut525 holes hbool hrows) (Fin.cases (cut496 holes hbool hrows) (Fin.cases (hrows 623) (fun i => Fin.elim0 i))))
def support538 : Finset (Fin 154) := {13, 18, 26, 31, 35, 41, 58, 61, 64, 69, 71, 75, 81, 86, 95}
theorem cut538 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support538, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 531, OmissionResidual.support 616, OmissionResidual.support 530] ![OmissionResidual.demand 531, OmissionResidual.demand 616, OmissionResidual.demand 530] ![1, 1, 1]
    support538 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 531) (Fin.cases (hrows 616) (Fin.cases (hrows 530) (fun i => Fin.elim0 i))))
def support539 : Finset (Fin 154) := {9, 13, 18, 19, 26, 31, 34, 35, 41, 45, 48, 58, 61, 64, 69, 71, 75, 76, 81, 86, 95}
theorem cut539 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support539, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 864, support538, OmissionResidual.support 64] ![OmissionResidual.demand 864, 2, OmissionResidual.demand 64] ![1, 1, 1]
    support539 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 864) (Fin.cases (cut538 holes hbool hrows) (Fin.cases (hrows 64) (fun i => Fin.elim0 i))))
def support540 : Finset (Fin 154) := {9, 13, 15, 18, 21, 26, 28, 31, 34, 35, 41, 45, 48, 58, 61, 64, 69, 71, 75, 76, 81, 86, 95}
theorem cut540 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support540, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 864, support538, OmissionResidual.support 118] ![OmissionResidual.demand 864, 2, OmissionResidual.demand 118] ![1, 1, 1]
    support540 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 864) (Fin.cases (cut538 holes hbool hrows) (Fin.cases (hrows 118) (fun i => Fin.elim0 i))))
def support541 : Finset (Fin 154) := {72, 82, 87, 89, 93, 94, 99, 102, 103, 106, 107, 110, 112, 115, 116, 120, 123, 124, 129, 130, 135, 143, 144, 147}
theorem cut541 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support541, holes i := by
  apply rounded_cover_cut ![support167, support183, OmissionResidual.support 1108] ![2, 2, OmissionResidual.demand 1108] ![1, 1, 1]
    support541 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut167 holes hbool hrows) (Fin.cases (cut183 holes hbool hrows) (Fin.cases (hrows 1108) (fun i => Fin.elim0 i))))
def support542 : Finset (Fin 154) := {16, 23, 25, 30, 31, 33, 41, 49, 52, 60, 68, 72, 79, 90, 99}
theorem cut542 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support542, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 886, OmissionResidual.support 135, OmissionResidual.support 901] ![OmissionResidual.demand 886, OmissionResidual.demand 135, OmissionResidual.demand 901] ![1, 1, 1]
    support542 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 886) (Fin.cases (hrows 135) (Fin.cases (hrows 901) (fun i => Fin.elim0 i))))
def support543 : Finset (Fin 154) := {15, 21, 28, 34, 38, 42, 56, 62, 63, 72, 78, 82, 83, 93, 94, 98, 103, 106, 114}
theorem cut543 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support543, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 120, OmissionResidual.support 420, OmissionResidual.support 344] ![OmissionResidual.demand 120, OmissionResidual.demand 420, OmissionResidual.demand 344] ![1, 1, 1]
    support543 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 120) (Fin.cases (hrows 420) (Fin.cases (hrows 344) (fun i => Fin.elim0 i))))
def support544 : Finset (Fin 154) := {49, 59, 64, 74, 75, 81, 85, 86, 87, 93, 95, 96, 97, 104, 105, 113, 118, 121, 122, 126, 129, 132, 136, 141}
theorem cut544 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support544, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, support385, support341] ![OmissionResidual.demand 736, 2, 2] ![1, 1, 1]
    support544 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (cut385 holes hbool hrows) (Fin.cases (cut341 holes hbool hrows) (fun i => Fin.elim0 i))))
def support545 : Finset (Fin 154) := {28, 36, 40, 46, 48, 51, 58, 61, 63, 69, 73, 80, 81, 84, 94, 102, 103, 106, 112, 116, 120, 124, 144}
theorem cut545 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support545, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 843, support123, support282] ![OmissionResidual.demand 843, 2, 2] ![1, 1, 1]
    support545 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 843) (Fin.cases (cut123 holes hbool hrows) (Fin.cases (cut282 holes hbool hrows) (fun i => Fin.elim0 i))))
def support546 : Finset (Fin 154) := {2, 7, 16, 24, 26, 35, 36, 40, 46, 49, 64, 69, 75, 81, 86, 95}
theorem cut546 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support546, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 472, OmissionResidual.support 616, OmissionResidual.support 672] ![OmissionResidual.demand 472, OmissionResidual.demand 616, OmissionResidual.demand 672] ![1, 1, 1]
    support546 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 472) (Fin.cases (hrows 616) (Fin.cases (hrows 672) (fun i => Fin.elim0 i))))
def support547 : Finset (Fin 154) := {5, 12, 16, 24, 26, 35, 36, 40, 46, 49, 64, 69, 75, 81, 86, 95}
theorem cut547 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support547, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 616, OmissionResidual.support 483, OmissionResidual.support 672] ![OmissionResidual.demand 616, OmissionResidual.demand 483, OmissionResidual.demand 672] ![1, 1, 1]
    support547 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 616) (Fin.cases (hrows 483) (Fin.cases (hrows 672) (fun i => Fin.elim0 i))))
def support548 : Finset (Fin 154) := {15, 21, 28, 34, 38, 40, 48, 49, 56, 59, 63, 73, 78, 88, 92, 102, 113}
theorem cut548 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support548, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 120, OmissionResidual.support 313, OmissionResidual.support 122] ![OmissionResidual.demand 120, OmissionResidual.demand 313, OmissionResidual.demand 122] ![1, 1, 1]
    support548 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 120) (Fin.cases (hrows 313) (Fin.cases (hrows 122) (fun i => Fin.elim0 i))))
def support549 : Finset (Fin 154) := {11, 16, 17, 23, 25, 30, 31, 33, 41, 49, 52, 60, 68, 72, 79, 90, 99}
theorem cut549 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support549, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 886, OmissionResidual.support 86, OmissionResidual.support 901] ![OmissionResidual.demand 886, OmissionResidual.demand 86, OmissionResidual.demand 901] ![1, 1, 1]
    support549 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 886) (Fin.cases (hrows 86) (Fin.cases (hrows 901) (fun i => Fin.elim0 i))))
def support550 : Finset (Fin 154) := {2, 4, 13, 21, 24, 25, 31, 34, 39, 44, 49, 68, 71, 79, 83, 100, 108}
theorem cut550 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support550, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 906, OmissionResidual.support 10, OmissionResidual.support 921] ![OmissionResidual.demand 906, OmissionResidual.demand 10, OmissionResidual.demand 921] ![1, 1, 1]
    support550 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 906) (Fin.cases (hrows 10) (Fin.cases (hrows 921) (fun i => Fin.elim0 i))))
#print axioms cut550
def support551 : Finset (Fin 154) := {2, 4, 13, 21, 24, 25, 31, 34, 39, 44, 49, 60, 68, 72, 79, 90, 99}
theorem cut551 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support551, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 905, OmissionResidual.support 10, OmissionResidual.support 919] ![OmissionResidual.demand 905, OmissionResidual.demand 10, OmissionResidual.demand 919] ![1, 1, 1]
    support551 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 905) (Fin.cases (hrows 10) (Fin.cases (hrows 919) (fun i => Fin.elim0 i))))
def support552 : Finset (Fin 154) := {28, 36, 40, 46, 48, 51, 58, 61, 63, 69, 73, 80, 81, 84, 94, 102, 103, 106, 112, 116, 120, 124, 140}
theorem cut552 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support552, holes i := by
  apply rounded_cover_cut ![support123, support282, OmissionResidual.support 842] ![2, 2, OmissionResidual.demand 842] ![1, 1, 1]
    support552 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut123 holes hbool hrows) (Fin.cases (cut282 holes hbool hrows) (Fin.cases (hrows 842) (fun i => Fin.elim0 i))))
def support553 : Finset (Fin 154) := {10, 13, 15, 16, 18, 20, 21, 24, 27, 31, 32, 35, 36, 37, 41, 42, 47, 50, 52, 61, 62, 63, 69, 72, 81}
theorem cut553 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support553, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 531, support192, support308] ![OmissionResidual.demand 531, 2, 2] ![1, 1, 1]
    support553 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 531) (Fin.cases (cut192 holes hbool hrows) (Fin.cases (cut308 holes hbool hrows) (fun i => Fin.elim0 i))))
def support554 : Finset (Fin 154) := {6, 10, 11, 13, 15, 16, 18, 20, 21, 24, 27, 31, 32, 35, 36, 37, 41, 42, 47, 50, 52, 61, 62, 63, 69, 72, 81}
theorem cut554 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support554, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 531, support192, support320] ![OmissionResidual.demand 531, 2, 2] ![1, 1, 1]
    support554 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 531) (Fin.cases (cut192 holes hbool hrows) (Fin.cases (cut320 holes hbool hrows) (fun i => Fin.elim0 i))))
def support555 : Finset (Fin 154) := {15, 21, 28, 34, 38, 40, 48, 49, 56, 59, 63, 73, 78, 81, 88, 93, 105}
theorem cut555 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support555, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 120, OmissionResidual.support 312, OmissionResidual.support 122] ![OmissionResidual.demand 120, OmissionResidual.demand 312, OmissionResidual.demand 122] ![1, 1, 1]
    support555 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 120) (Fin.cases (hrows 312) (Fin.cases (hrows 122) (fun i => Fin.elim0 i))))
def support556 : Finset (Fin 154) := {51, 60, 66, 70, 73, 78, 81, 83, 88, 93, 98, 102, 103, 105, 112, 114, 121}
theorem cut556 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support556, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 947, OmissionResidual.support 949, OmissionResidual.support 438] ![OmissionResidual.demand 947, OmissionResidual.demand 949, OmissionResidual.demand 438] ![1, 1, 1]
    support556 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 947) (Fin.cases (hrows 949) (Fin.cases (hrows 438) (fun i => Fin.elim0 i))))
def support557 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 61, 63, 69, 73, 80, 84, 93, 94, 102, 103, 106, 112, 116, 120, 124, 144}
theorem cut557 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support557, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 843, support155, support47] ![OmissionResidual.demand 843, 2, 2] ![1, 1, 1]
    support557 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 843) (Fin.cases (cut155 holes hbool hrows) (Fin.cases (cut47 holes hbool hrows) (fun i => Fin.elim0 i))))
def support558 : Finset (Fin 154) := {39, 49, 50, 53, 59, 64, 65, 70, 77, 81, 82, 87, 93, 96, 97, 105}
theorem cut558 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support558, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, OmissionResidual.support 690, OmissionResidual.support 740] ![OmissionResidual.demand 736, OmissionResidual.demand 690, OmissionResidual.demand 740] ![1, 1, 1]
    support558 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (hrows 690) (Fin.cases (hrows 740) (fun i => Fin.elim0 i))))
def support559 : Finset (Fin 154) := {63, 72, 73, 78, 82, 83, 88, 90, 93, 100, 102, 103, 112, 117, 123, 135}
theorem cut559 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support559, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 966, OmissionResidual.support 418, OmissionResidual.support 969] ![OmissionResidual.demand 966, OmissionResidual.demand 418, OmissionResidual.demand 969] ![1, 1, 1]
    support559 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 966) (Fin.cases (hrows 418) (Fin.cases (hrows 969) (fun i => Fin.elim0 i))))
def support560 : Finset (Fin 154) := {15, 21, 28, 34, 38, 42, 56, 62, 63, 72, 78, 82, 83, 94, 98, 102, 106, 112, 121}
theorem cut560 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support560, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 120, OmissionResidual.support 344, OmissionResidual.support 421] ![OmissionResidual.demand 120, OmissionResidual.demand 344, OmissionResidual.demand 421] ![1, 1, 1]
    support560 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 120) (Fin.cases (hrows 344) (Fin.cases (hrows 421) (fun i => Fin.elim0 i))))
def support561 : Finset (Fin 154) := {4, 5, 7, 8, 13, 21, 23, 25, 31, 33, 34, 35, 40, 44, 46, 59, 74}
theorem cut561 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support561, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 479, OmissionResidual.support 25, OmissionResidual.support 30] ![OmissionResidual.demand 479, OmissionResidual.demand 25, OmissionResidual.demand 30] ![1, 1, 1]
    support561 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 479) (Fin.cases (hrows 25) (Fin.cases (hrows 30) (fun i => Fin.elim0 i))))
def support562 : Finset (Fin 154) := {2, 4, 8, 12, 13, 21, 23, 25, 31, 33, 34, 35, 40, 44, 46, 59, 74}
theorem cut562 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support562, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 10, OmissionResidual.support 496, OmissionResidual.support 51] ![OmissionResidual.demand 10, OmissionResidual.demand 496, OmissionResidual.demand 51] ![1, 1, 1]
    support562 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 10) (Fin.cases (hrows 496) (Fin.cases (hrows 51) (fun i => Fin.elim0 i))))
def support563 : Finset (Fin 154) := {10, 14, 25, 28, 38, 42, 56, 62, 63, 72, 78, 82, 83, 93, 94, 98, 103, 106, 114}
theorem cut563 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support563, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 420, OmissionResidual.support 344, OmissionResidual.support 77] ![OmissionResidual.demand 420, OmissionResidual.demand 344, OmissionResidual.demand 77] ![1, 1, 1]
    support563 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 420) (Fin.cases (hrows 344) (Fin.cases (hrows 77) (fun i => Fin.elim0 i))))
def support564 : Finset (Fin 154) := {72, 82, 87, 96, 99, 102, 105, 112, 114, 116, 118, 123, 129, 132, 134, 137, 143, 144, 152}
theorem cut564 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support564, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1097, OmissionResidual.support 1153, OmissionResidual.support 817] ![OmissionResidual.demand 1097, OmissionResidual.demand 1153, OmissionResidual.demand 817] ![1, 1, 1]
    support564 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1097) (Fin.cases (hrows 1153) (Fin.cases (hrows 817) (fun i => Fin.elim0 i))))
def support565 : Finset (Fin 154) := {72, 82, 87, 96, 99, 102, 105, 112, 114, 116, 118, 123, 124, 129, 130, 132, 134, 135, 137, 138, 140, 143, 144, 148, 152}
theorem cut565 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support565, holes i := by
  apply rounded_cover_cut ![support71, support564, OmissionResidual.support 819] ![2, 2, OmissionResidual.demand 819] ![1, 1, 1]
    support565 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut71 holes hbool hrows) (Fin.cases (cut564 holes hbool hrows) (Fin.cases (hrows 819) (fun i => Fin.elim0 i))))
def support566 : Finset (Fin 154) := {72, 82, 87, 96, 99, 102, 105, 112, 114, 116, 118, 123, 124, 129, 130, 132, 134, 135, 137, 138, 140, 143, 144, 148, 152, 153}
theorem cut566 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support566, holes i := by
  apply rounded_cover_cut ![support89, support564, OmissionResidual.support 819] ![2, 2, OmissionResidual.demand 819] ![1, 1, 1]
    support566 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut89 holes hbool hrows) (Fin.cases (cut564 holes hbool hrows) (Fin.cases (hrows 819) (fun i => Fin.elim0 i))))
def support567 : Finset (Fin 154) := {72, 82, 87, 96, 99, 102, 105, 112, 114, 116, 118, 123, 124, 129, 130, 132, 134, 135, 137, 138, 140, 143, 144, 150, 151, 152}
theorem cut567 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support567, holes i := by
  apply rounded_cover_cut ![support130, support564, OmissionResidual.support 819] ![2, 2, OmissionResidual.demand 819] ![1, 1, 1]
    support567 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut130 holes hbool hrows) (Fin.cases (cut564 holes hbool hrows) (Fin.cases (hrows 819) (fun i => Fin.elim0 i))))
def support568 : Finset (Fin 154) := {72, 82, 87, 96, 99, 102, 105, 112, 114, 116, 118, 123, 124, 129, 130, 132, 134, 135, 137, 138, 140, 143, 144, 150, 151, 152, 153}
theorem cut568 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support568, holes i := by
  apply rounded_cover_cut ![support88, support564, OmissionResidual.support 819] ![2, 2, OmissionResidual.demand 819] ![1, 1, 1]
    support568 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut88 holes hbool hrows) (Fin.cases (cut564 holes hbool hrows) (Fin.cases (hrows 819) (fun i => Fin.elim0 i))))
def support569 : Finset (Fin 154) := {38, 47, 48, 57, 58, 61, 66, 69, 73, 78, 80, 84, 88, 93, 102, 105, 113, 120}
theorem cut569 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support569, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 731, OmissionResidual.support 928, OmissionResidual.support 927] ![OmissionResidual.demand 731, OmissionResidual.demand 928, OmissionResidual.demand 927] ![1, 1, 1]
    support569 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 731) (Fin.cases (hrows 928) (Fin.cases (hrows 927) (fun i => Fin.elim0 i))))
def support570 : Finset (Fin 154) := {38, 47, 48, 57, 58, 61, 66, 69, 73, 78, 80, 84, 88, 93, 102, 105, 112, 113}
theorem cut570 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support570, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 730, OmissionResidual.support 928, OmissionResidual.support 927] ![OmissionResidual.demand 730, OmissionResidual.demand 928, OmissionResidual.demand 927] ![1, 1, 1]
    support570 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 730) (Fin.cases (hrows 928) (Fin.cases (hrows 927) (fun i => Fin.elim0 i))))
def support571 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 60, 61, 63, 66, 69, 70, 73, 78, 80, 84, 88, 92, 93, 102, 105, 112, 113}
theorem cut571 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support571, holes i := by
  apply rounded_cover_cut ![support570, support47, OmissionResidual.support 948] ![3, 2, OmissionResidual.demand 948] ![1, 1, 1]
    support571 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut570 holes hbool hrows) (Fin.cases (cut47 holes hbool hrows) (Fin.cases (hrows 948) (fun i => Fin.elim0 i))))
def support572 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 60, 61, 63, 66, 69, 70, 73, 78, 80, 84, 88, 92, 93, 102, 105, 112, 113, 120}
theorem cut572 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support572, holes i := by
  apply rounded_cover_cut ![support569, support47, OmissionResidual.support 948] ![3, 2, OmissionResidual.demand 948] ![1, 1, 1]
    support572 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut569 holes hbool hrows) (Fin.cases (cut47 holes hbool hrows) (Fin.cases (hrows 948) (fun i => Fin.elim0 i))))
def support573 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 60, 61, 63, 66, 69, 70, 73, 78, 80, 81, 84, 88, 93, 102, 103, 105, 113, 120}
theorem cut573 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support573, holes i := by
  apply rounded_cover_cut ![support569, support155, OmissionResidual.support 947] ![3, 2, OmissionResidual.demand 947] ![1, 1, 1]
    support573 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut569 holes hbool hrows) (Fin.cases (cut155 holes hbool hrows) (Fin.cases (hrows 947) (fun i => Fin.elim0 i))))
def support574 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 60, 61, 63, 66, 69, 70, 73, 78, 80, 81, 84, 88, 93, 102, 103, 105, 112, 113}
theorem cut574 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support574, holes i := by
  apply rounded_cover_cut ![support570, support59, OmissionResidual.support 947] ![3, 2, OmissionResidual.demand 947] ![1, 1, 1]
    support574 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut570 holes hbool hrows) (Fin.cases (cut59 holes hbool hrows) (Fin.cases (hrows 947) (fun i => Fin.elim0 i))))
def support575 : Finset (Fin 154) := {38, 47, 48, 57, 58, 61, 66, 69, 73, 78, 80, 84, 88, 93, 94, 102, 103, 105, 106, 112, 113, 116, 120, 124, 144}
theorem cut575 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support575, holes i := by
  apply rounded_cover_cut ![support569, support570, OmissionResidual.support 843] ![3, 3, OmissionResidual.demand 843] ![1, 1, 1]
    support575 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut569 holes hbool hrows) (Fin.cases (cut570 holes hbool hrows) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
#print axioms cut575
def support576 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 60, 61, 63, 66, 69, 70, 73, 78, 80, 81, 84, 88, 93, 102, 103, 105, 112, 113, 120}
theorem cut576 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support576, holes i := by
  apply rounded_cover_cut ![support569, support59, OmissionResidual.support 947] ![3, 2, OmissionResidual.demand 947] ![1, 1, 1]
    support576 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut569 holes hbool hrows) (Fin.cases (cut59 holes hbool hrows) (Fin.cases (hrows 947) (fun i => Fin.elim0 i))))
def support577 : Finset (Fin 154) := {29, 37, 41, 52, 57, 63, 69, 72, 73, 78, 82, 84, 90, 93, 103, 123}
theorem cut577 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support577, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 630, OmissionResidual.support 418, OmissionResidual.support 632] ![OmissionResidual.demand 630, OmissionResidual.demand 418, OmissionResidual.demand 632] ![1, 1, 1]
    support577 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 630) (Fin.cases (hrows 418) (Fin.cases (hrows 632) (fun i => Fin.elim0 i))))
def support578 : Finset (Fin 154) := {3, 8, 9, 11, 12, 18, 23, 24, 26, 32, 37, 41, 47, 50, 51, 60}
theorem cut578 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support578, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 506, OmissionResidual.support 475, OmissionResidual.support 497] ![OmissionResidual.demand 506, OmissionResidual.demand 475, OmissionResidual.demand 497] ![1, 1, 1]
    support578 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 506) (Fin.cases (hrows 475) (Fin.cases (hrows 497) (fun i => Fin.elim0 i))))
def support579 : Finset (Fin 154) := {5, 8, 9, 12, 16, 18, 23, 24, 26, 32, 37, 41, 47, 50, 51, 60}
theorem cut579 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support579, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 506, OmissionResidual.support 484, OmissionResidual.support 497] ![OmissionResidual.demand 506, OmissionResidual.demand 484, OmissionResidual.demand 497] ![1, 1, 1]
    support579 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 506) (Fin.cases (hrows 484) (Fin.cases (hrows 497) (fun i => Fin.elim0 i))))
def support580 : Finset (Fin 154) := {0, 2, 3, 7, 12, 17, 18, 20, 25, 27, 30, 34, 39, 43, 44, 53}
theorem cut580 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support580, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 849, OmissionResidual.support 847, OmissionResidual.support 1] ![OmissionResidual.demand 849, OmissionResidual.demand 847, OmissionResidual.demand 1] ![1, 1, 1]
    support580 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 849) (Fin.cases (hrows 847) (Fin.cases (hrows 1) (fun i => Fin.elim0 i))))
def support581 : Finset (Fin 154) := {1, 2, 3, 7, 12, 17, 18, 20, 25, 27, 30, 34, 39, 43, 44, 53}
theorem cut581 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support581, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 849, OmissionResidual.support 847, OmissionResidual.support 5] ![OmissionResidual.demand 849, OmissionResidual.demand 847, OmissionResidual.demand 5] ![1, 1, 1]
    support581 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 849) (Fin.cases (hrows 847) (Fin.cases (hrows 5) (fun i => Fin.elim0 i))))
def support582 : Finset (Fin 154) := {1, 5, 7, 12, 17, 18, 20, 25, 27, 30, 34, 39, 43, 44, 53}
theorem cut582 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support582, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 846, OmissionResidual.support 853, OmissionResidual.support 5] ![OmissionResidual.demand 846, OmissionResidual.demand 853, OmissionResidual.demand 5] ![1, 1, 1]
    support582 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 846) (Fin.cases (hrows 853) (Fin.cases (hrows 5) (fun i => Fin.elim0 i))))
def support583 : Finset (Fin 154) := {0, 1, 5, 7, 12, 17, 18, 20, 25, 27, 30, 34, 39, 43, 44, 53}
theorem cut583 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support583, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 846, OmissionResidual.support 853, OmissionResidual.support 1] ![OmissionResidual.demand 846, OmissionResidual.demand 853, OmissionResidual.demand 1] ![1, 1, 1]
    support583 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 846) (Fin.cases (hrows 853) (Fin.cases (hrows 1) (fun i => Fin.elim0 i))))
def support584 : Finset (Fin 154) := {24, 31, 34, 40, 51, 61, 63, 68, 72, 73, 78, 82, 90, 100, 102, 122}
theorem cut584 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support584, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 205, OmissionResidual.support 800, OmissionResidual.support 203] ![OmissionResidual.demand 205, OmissionResidual.demand 800, OmissionResidual.demand 203] ![1, 1, 1]
    support584 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 205) (Fin.cases (hrows 800) (Fin.cases (hrows 203) (fun i => Fin.elim0 i))))
def support585 : Finset (Fin 154) := {6, 14, 17, 21, 29, 42, 52, 56, 62, 67, 68, 72, 79, 83, 94, 124}
theorem cut585 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support585, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 343, OmissionResidual.support 46, OmissionResidual.support 385] ![OmissionResidual.demand 343, OmissionResidual.demand 46, OmissionResidual.demand 385] ![1, 1, 1]
    support585 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 343) (Fin.cases (hrows 46) (Fin.cases (hrows 385) (fun i => Fin.elim0 i))))
def support586 : Finset (Fin 154) := {6, 14, 17, 21, 29, 42, 52, 56, 62, 67, 68, 72, 79, 83, 94, 117, 124}
theorem cut586 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support586, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 944, OmissionResidual.support 46, OmissionResidual.support 957] ![OmissionResidual.demand 944, OmissionResidual.demand 46, OmissionResidual.demand 957] ![1, 1, 1]
    support586 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 944) (Fin.cases (hrows 46) (Fin.cases (hrows 957) (fun i => Fin.elim0 i))))
def support587 : Finset (Fin 154) := {6, 14, 17, 21, 29, 42, 52, 56, 62, 67, 68, 72, 79, 83, 94, 116}
theorem cut587 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support587, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 341, OmissionResidual.support 46, OmissionResidual.support 383] ![OmissionResidual.demand 341, OmissionResidual.demand 46, OmissionResidual.demand 383] ![1, 1, 1]
    support587 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 341) (Fin.cases (hrows 46) (Fin.cases (hrows 383) (fun i => Fin.elim0 i))))
def support588 : Finset (Fin 154) := {6, 14, 17, 21, 29, 42, 52, 56, 62, 67, 68, 72, 79, 83, 94, 109, 116}
theorem cut588 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support588, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 943, OmissionResidual.support 46, OmissionResidual.support 955] ![OmissionResidual.demand 943, OmissionResidual.demand 46, OmissionResidual.demand 955] ![1, 1, 1]
    support588 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 943) (Fin.cases (hrows 46) (Fin.cases (hrows 955) (fun i => Fin.elim0 i))))
def support589 : Finset (Fin 154) := {7, 19, 26, 28, 35, 36, 40, 43, 46, 51, 53, 59, 61, 64, 74, 80, 92}
theorem cut589 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support589, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 494, OmissionResidual.support 572, OmissionResidual.support 623] ![OmissionResidual.demand 494, OmissionResidual.demand 572, OmissionResidual.demand 623] ![1, 1, 1]
    support589 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 494) (Fin.cases (hrows 572) (Fin.cases (hrows 623) (fun i => Fin.elim0 i))))
def support590 : Finset (Fin 154) := {4, 7, 23, 26, 31, 35, 36, 40, 46, 59, 64, 75, 80, 86, 92, 104}
theorem cut590 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support590, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 479, OmissionResidual.support 617, OmissionResidual.support 673] ![OmissionResidual.demand 479, OmissionResidual.demand 617, OmissionResidual.demand 673] ![1, 1, 1]
    support590 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 479) (Fin.cases (hrows 617) (Fin.cases (hrows 673) (fun i => Fin.elim0 i))))
def support591 : Finset (Fin 154) := {7, 13, 18, 21, 27, 35, 43, 44, 46, 53, 55, 59, 64, 69, 74, 76, 81, 95}
theorem cut591 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support591, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 494, OmissionResidual.support 874, OmissionResidual.support 892] ![OmissionResidual.demand 494, OmissionResidual.demand 874, OmissionResidual.demand 892] ![1, 1, 1]
    support591 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 494) (Fin.cases (hrows 874) (Fin.cases (hrows 892) (fun i => Fin.elim0 i))))
def support592 : Finset (Fin 154) := {4, 7, 13, 18, 21, 23, 27, 31, 35, 40, 44, 46, 55, 59, 69, 76, 81, 95}
theorem cut592 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support592, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 479, OmissionResidual.support 874, OmissionResidual.support 892] ![OmissionResidual.demand 479, OmissionResidual.demand 874, OmissionResidual.demand 892] ![1, 1, 1]
    support592 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 479) (Fin.cases (hrows 874) (Fin.cases (hrows 892) (fun i => Fin.elim0 i))))
def support593 : Finset (Fin 154) := {78, 87, 96, 97, 105, 111, 113, 114, 121, 126, 130, 133, 135, 138, 142, 146}
theorem cut593 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support593, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1078, OmissionResidual.support 1119, OmissionResidual.support 1082] ![OmissionResidual.demand 1078, OmissionResidual.demand 1119, OmissionResidual.demand 1082] ![1, 1, 1]
    support593 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1078) (Fin.cases (hrows 1119) (Fin.cases (hrows 1082) (fun i => Fin.elim0 i))))
def support594 : Finset (Fin 154) := {41, 50, 55, 60, 67, 70, 71, 75, 81, 83, 87, 88, 93, 97, 105}
theorem cut594 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support594, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 778, OmissionResidual.support 935, OmissionResidual.support 936] ![OmissionResidual.demand 778, OmissionResidual.demand 935, OmissionResidual.demand 936] ![1, 1, 1]
    support594 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 778) (Fin.cases (hrows 935) (Fin.cases (hrows 936) (fun i => Fin.elim0 i))))
def support595 : Finset (Fin 154) := {2, 3, 5, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 23, 24, 26, 32, 36, 37, 40, 41, 47, 49, 50, 51, 60}
theorem cut595 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support595, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 475, support338, support104] ![OmissionResidual.demand 475, 2, 2] ![1, 1, 1]
    support595 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 475) (Fin.cases (cut338 holes hbool hrows) (Fin.cases (cut104 holes hbool hrows) (fun i => Fin.elim0 i))))
def support596 : Finset (Fin 154) := {61, 71, 73, 76, 81, 83, 88, 92, 93, 100, 102, 120, 122, 128, 134}
theorem cut596 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support596, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 409, OmissionResidual.support 440, OmissionResidual.support 406] ![OmissionResidual.demand 409, OmissionResidual.demand 440, OmissionResidual.demand 406] ![1, 1, 1]
    support596 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 409) (Fin.cases (hrows 440) (Fin.cases (hrows 406) (fun i => Fin.elim0 i))))
def support597 : Finset (Fin 154) := {10, 14, 21, 25, 29, 42, 52, 56, 62, 67, 68, 72, 79, 83, 94, 124}
theorem cut597 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support597, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 343, OmissionResidual.support 385, OmissionResidual.support 75] ![OmissionResidual.demand 343, OmissionResidual.demand 385, OmissionResidual.demand 75] ![1, 1, 1]
    support597 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 343) (Fin.cases (hrows 385) (Fin.cases (hrows 75) (fun i => Fin.elim0 i))))
def support598 : Finset (Fin 154) := {10, 14, 21, 25, 29, 42, 52, 56, 62, 67, 68, 72, 79, 83, 94, 117, 124}
theorem cut598 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support598, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 944, OmissionResidual.support 957, OmissionResidual.support 75] ![OmissionResidual.demand 944, OmissionResidual.demand 957, OmissionResidual.demand 75] ![1, 1, 1]
    support598 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 944) (Fin.cases (hrows 957) (Fin.cases (hrows 75) (fun i => Fin.elim0 i))))
def support599 : Finset (Fin 154) := {10, 14, 21, 25, 29, 42, 52, 56, 62, 67, 68, 72, 79, 83, 94, 116}
theorem cut599 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support599, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 341, OmissionResidual.support 383, OmissionResidual.support 75] ![OmissionResidual.demand 341, OmissionResidual.demand 383, OmissionResidual.demand 75] ![1, 1, 1]
    support599 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 341) (Fin.cases (hrows 383) (Fin.cases (hrows 75) (fun i => Fin.elim0 i))))
def support600 : Finset (Fin 154) := {10, 14, 21, 25, 29, 42, 52, 56, 62, 67, 68, 72, 79, 83, 94, 109, 116}
theorem cut600 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support600, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 943, OmissionResidual.support 955, OmissionResidual.support 75] ![OmissionResidual.demand 943, OmissionResidual.demand 955, OmissionResidual.demand 75] ![1, 1, 1]
    support600 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 943) (Fin.cases (hrows 955) (Fin.cases (hrows 75) (fun i => Fin.elim0 i))))
#print axioms cut600
def support601 : Finset (Fin 154) := {0, 6, 7, 10, 12, 14, 17, 20, 21, 25, 29, 30, 42, 43, 52, 56, 62, 67, 72, 83, 94, 98, 106}
theorem cut601 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support601, holes i := by
  apply rounded_cover_cut ![support487, support488, OmissionResidual.support 1] ![2, 2, OmissionResidual.demand 1] ![1, 1, 1]
    support601 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut487 holes hbool hrows) (Fin.cases (cut488 holes hbool hrows) (Fin.cases (hrows 1) (fun i => Fin.elim0 i))))
def support602 : Finset (Fin 154) := {1, 6, 7, 10, 12, 14, 17, 20, 21, 25, 29, 30, 42, 43, 52, 56, 62, 67, 72, 83, 94, 98, 106}
theorem cut602 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support602, holes i := by
  apply rounded_cover_cut ![support487, support488, OmissionResidual.support 5] ![2, 2, OmissionResidual.demand 5] ![1, 1, 1]
    support602 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut487 holes hbool hrows) (Fin.cases (cut488 holes hbool hrows) (Fin.cases (hrows 5) (fun i => Fin.elim0 i))))
def support603 : Finset (Fin 154) := {9, 18, 24, 26, 32, 38, 47, 51, 57, 60, 66, 70, 78, 80, 88, 92, 102, 113}
theorem cut603 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support603, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 506, OmissionResidual.support 948, OmissionResidual.support 928] ![OmissionResidual.demand 506, OmissionResidual.demand 948, OmissionResidual.demand 928] ![1, 1, 1]
    support603 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 506) (Fin.cases (hrows 948) (Fin.cases (hrows 928) (fun i => Fin.elim0 i))))
def support604 : Finset (Fin 154) := {61, 71, 76, 81, 92, 100, 102, 108, 115, 120, 122, 126, 134, 140, 143, 151}
theorem cut604 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support604, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1143, OmissionResidual.support 411, OmissionResidual.support 409] ![OmissionResidual.demand 1143, OmissionResidual.demand 411, OmissionResidual.demand 409] ![1, 1, 1]
    support604 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1143) (Fin.cases (hrows 411) (Fin.cases (hrows 409) (fun i => Fin.elim0 i))))
def support605 : Finset (Fin 154) := {61, 63, 71, 72, 76, 78, 81, 82, 90, 92, 100, 102, 112, 122, 129}
theorem cut605 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support605, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 419, OmissionResidual.support 409, OmissionResidual.support 410] ![OmissionResidual.demand 419, OmissionResidual.demand 409, OmissionResidual.demand 410] ![1, 1, 1]
    support605 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 419) (Fin.cases (hrows 409) (Fin.cases (hrows 410) (fun i => Fin.elim0 i))))
def support606 : Finset (Fin 154) := {61, 63, 71, 72, 76, 78, 81, 82, 90, 92, 100, 102, 109, 112, 122, 129}
theorem cut606 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support606, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 964, OmissionResidual.support 409, OmissionResidual.support 961] ![OmissionResidual.demand 964, OmissionResidual.demand 409, OmissionResidual.demand 961] ![1, 1, 1]
    support606 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 964) (Fin.cases (hrows 409) (Fin.cases (hrows 961) (fun i => Fin.elim0 i))))
def support607 : Finset (Fin 154) := {8, 12, 14, 20, 23, 35, 41, 43, 46, 51, 53, 57, 59, 64, 70, 74}
theorem cut607 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support607, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 526, OmissionResidual.support 498, OmissionResidual.support 540] ![OmissionResidual.demand 526, OmissionResidual.demand 498, OmissionResidual.demand 540] ![1, 1, 1]
    support607 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 526) (Fin.cases (hrows 498) (Fin.cases (hrows 540) (fun i => Fin.elim0 i))))
def support608 : Finset (Fin 154) := {2, 4, 7, 16, 23, 24, 25, 26, 31, 36, 40, 41, 49, 52, 68, 79}
theorem cut608 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support608, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 478, OmissionResidual.support 472, OmissionResidual.support 135] ![OmissionResidual.demand 478, OmissionResidual.demand 472, OmissionResidual.demand 135] ![1, 1, 1]
    support608 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 478) (Fin.cases (hrows 472) (Fin.cases (hrows 135) (fun i => Fin.elim0 i))))
def support609 : Finset (Fin 154) := {7, 19, 26, 28, 29, 35, 36, 37, 38, 40, 41, 43, 46, 47, 48, 51, 52, 53, 57, 58, 59, 61, 63, 64, 69, 73, 74, 80, 83, 84, 92, 103, 120}
theorem cut609 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support609, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 494, support530, support536] ![OmissionResidual.demand 494, 3, 3] ![1, 1, 1]
    support609 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 494) (Fin.cases (cut530 holes hbool hrows) (Fin.cases (cut536 holes hbool hrows) (fun i => Fin.elim0 i))))
def support610 : Finset (Fin 154) := {7, 19, 22, 26, 28, 29, 32, 35, 36, 37, 38, 40, 41, 42, 43, 46, 47, 48, 51, 52, 53, 57, 58, 59, 61, 63, 64, 69, 73, 74, 80, 83, 84, 92, 103, 120}
theorem cut610 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support610, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 494, support532, support536] ![OmissionResidual.demand 494, 3, 3] ![1, 1, 1]
    support610 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 494) (Fin.cases (cut532 holes hbool hrows) (Fin.cases (cut536 holes hbool hrows) (fun i => Fin.elim0 i))))
def support611 : Finset (Fin 154) := {1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 21, 23, 24, 26, 27, 31, 32, 36, 37, 39, 40, 41, 47, 49, 50, 51, 60}
theorem cut611 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support611, holes i := by
  apply rounded_cover_cut ![support595, support307, OmissionResidual.support 469] ![3, 3, OmissionResidual.demand 469] ![1, 1, 1]
    support611 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut595 holes hbool hrows) (Fin.cases (cut307 holes hbool hrows) (Fin.cases (hrows 469) (fun i => Fin.elim0 i))))
def support612 : Finset (Fin 154) := {1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 21, 23, 24, 26, 27, 31, 32, 36, 37, 39, 40, 41, 42, 47, 49, 50, 51, 52, 60, 62}
theorem cut612 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support612, holes i := by
  apply rounded_cover_cut ![support414, support595, OmissionResidual.support 469] ![3, 3, OmissionResidual.demand 469] ![1, 1, 1]
    support612 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut414 holes hbool hrows) (Fin.cases (cut595 holes hbool hrows) (Fin.cases (hrows 469) (fun i => Fin.elim0 i))))
def support613 : Finset (Fin 154) := {8, 10, 12, 14, 16, 20, 21, 23, 27, 31, 35, 37, 40, 41, 42, 43, 46, 51, 52, 53, 57, 59, 62, 64, 70, 74}
theorem cut613 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support613, holes i := by
  apply rounded_cover_cut ![support76, support607, OmissionResidual.support 514] ![2, 2, OmissionResidual.demand 514] ![1, 1, 1]
    support613 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut76 holes hbool hrows) (Fin.cases (cut607 holes hbool hrows) (Fin.cases (hrows 514) (fun i => Fin.elim0 i))))
def support614 : Finset (Fin 154) := {6, 8, 11, 12, 14, 20, 21, 23, 27, 31, 35, 37, 40, 41, 42, 43, 46, 51, 52, 53, 57, 59, 62, 64, 70, 74}
theorem cut614 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support614, holes i := by
  apply rounded_cover_cut ![support76, support607, OmissionResidual.support 491] ![2, 2, OmissionResidual.demand 491] ![1, 1, 1]
    support614 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut76 holes hbool hrows) (Fin.cases (cut607 holes hbool hrows) (Fin.cases (hrows 491) (fun i => Fin.elim0 i))))
def support615 : Finset (Fin 154) := {8, 10, 12, 16, 20, 23, 27, 31, 35, 37, 40, 42, 43, 46, 52, 53, 57, 59, 62, 64, 65, 70, 74, 75, 85}
theorem cut615 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support615, holes i := by
  apply rounded_cover_cut ![support75, support213, OmissionResidual.support 514] ![2, 2, OmissionResidual.demand 514] ![1, 1, 1]
    support615 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut75 holes hbool hrows) (Fin.cases (cut213 holes hbool hrows) (Fin.cases (hrows 514) (fun i => Fin.elim0 i))))
def support616 : Finset (Fin 154) := {6, 8, 11, 12, 20, 23, 27, 31, 35, 37, 40, 42, 43, 46, 52, 53, 57, 59, 62, 64, 65, 70, 74, 75, 85}
theorem cut616 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support616, holes i := by
  apply rounded_cover_cut ![support75, support213, OmissionResidual.support 491] ![2, 2, OmissionResidual.demand 491] ![1, 1, 1]
    support616 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut75 holes hbool hrows) (Fin.cases (cut213 holes hbool hrows) (Fin.cases (hrows 491) (fun i => Fin.elim0 i))))
def support617 : Finset (Fin 154) := {21, 22, 27, 28, 31, 32, 36, 37, 38, 40, 42, 46, 47, 51, 52, 57, 58, 63, 69, 73, 82, 83, 84, 93, 94}
theorem cut617 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support617, holes i := by
  apply rounded_cover_cut ![support40, OmissionResidual.support 588, support205] ![2, OmissionResidual.demand 588, 2] ![1, 1, 1]
    support617 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut40 holes hbool hrows) (Fin.cases (hrows 588) (Fin.cases (cut205 holes hbool hrows) (fun i => Fin.elim0 i))))
def support618 : Finset (Fin 154) := {6, 10, 11, 14, 15, 20, 23, 24, 25, 27, 28, 36, 37, 38, 42, 47, 52, 56, 62, 63, 72, 78, 87}
theorem cut618 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support618, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 868, OmissionResidual.support 77, support390] ![OmissionResidual.demand 868, OmissionResidual.demand 77, 2] ![1, 1, 1]
    support618 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 868) (Fin.cases (hrows 77) (Fin.cases (cut390 holes hbool hrows) (fun i => Fin.elim0 i))))
def support619 : Finset (Fin 154) := {5, 6, 8, 10, 11, 12, 15, 16, 20, 23, 24, 26, 27, 31, 32, 36, 37, 40, 42, 47, 49, 51, 52, 60, 62}
theorem cut619 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support619, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 491, support311, support245] ![OmissionResidual.demand 491, 2, 2] ![1, 1, 1]
    support619 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 491) (Fin.cases (cut311 holes hbool hrows) (Fin.cases (cut245 holes hbool hrows) (fun i => Fin.elim0 i))))
def support620 : Finset (Fin 154) := {4, 5, 7, 8, 9, 12, 13, 16, 18, 23, 24, 26, 31, 32, 35, 37, 40, 41, 46, 47, 50, 51, 59, 60}
theorem cut620 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support620, holes i := by
  apply rounded_cover_cut ![support579, OmissionResidual.support 479, support335] ![2, OmissionResidual.demand 479, 2] ![1, 1, 1]
    support620 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut579 holes hbool hrows) (Fin.cases (hrows 479) (Fin.cases (cut335 holes hbool hrows) (fun i => Fin.elim0 i))))
def support621 : Finset (Fin 154) := {38, 47, 51, 57, 60, 61, 63, 66, 70, 71, 73, 76, 78, 80, 81, 84, 92, 98, 100, 102, 103, 112, 114, 121, 122}
theorem cut621 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support621, holes i := by
  apply rounded_cover_cut ![support402, OmissionResidual.support 409, support460] ![3, OmissionResidual.demand 409, 3] ![1, 1, 1]
    support621 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut402 holes hbool hrows) (Fin.cases (hrows 409) (Fin.cases (cut460 holes hbool hrows) (fun i => Fin.elim0 i))))
def support622 : Finset (Fin 154) := {49, 59, 61, 64, 71, 76, 81, 87, 92, 93, 97, 100, 102, 105, 113, 122}
theorem cut622 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support622, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 737, OmissionResidual.support 409, OmissionResidual.support 736] ![OmissionResidual.demand 737, OmissionResidual.demand 409, OmissionResidual.demand 736] ![1, 1, 1]
    support622 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 737) (Fin.cases (hrows 409) (Fin.cases (hrows 736) (fun i => Fin.elim0 i))))
def support623 : Finset (Fin 154) := {0, 6, 7, 10, 12, 14, 17, 20, 21, 25, 29, 30, 42, 43, 52, 56, 62, 67, 68, 72, 79, 83, 94, 116}
theorem cut623 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support623, holes i := by
  apply rounded_cover_cut ![support587, support599, OmissionResidual.support 1] ![2, 2, OmissionResidual.demand 1] ![1, 1, 1]
    support623 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut587 holes hbool hrows) (Fin.cases (cut599 holes hbool hrows) (Fin.cases (hrows 1) (fun i => Fin.elim0 i))))
def support624 : Finset (Fin 154) := {1, 6, 7, 10, 12, 14, 17, 20, 21, 25, 29, 30, 42, 43, 52, 56, 62, 67, 68, 72, 79, 83, 94, 116}
theorem cut624 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support624, holes i := by
  apply rounded_cover_cut ![support587, support599, OmissionResidual.support 5] ![2, 2, OmissionResidual.demand 5] ![1, 1, 1]
    support624 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut587 holes hbool hrows) (Fin.cases (cut599 holes hbool hrows) (Fin.cases (hrows 5) (fun i => Fin.elim0 i))))
def support625 : Finset (Fin 154) := {0, 6, 7, 10, 12, 14, 17, 20, 21, 25, 29, 30, 42, 43, 52, 56, 62, 67, 68, 72, 79, 83, 94, 109, 116}
theorem cut625 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support625, holes i := by
  apply rounded_cover_cut ![support588, support600, OmissionResidual.support 1] ![3, 3, OmissionResidual.demand 1] ![1, 1, 1]
    support625 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut588 holes hbool hrows) (Fin.cases (cut600 holes hbool hrows) (Fin.cases (hrows 1) (fun i => Fin.elim0 i))))
#print axioms cut625
def support626 : Finset (Fin 154) := {1, 6, 7, 10, 12, 14, 17, 20, 21, 25, 29, 30, 42, 43, 52, 56, 62, 67, 68, 72, 79, 83, 94, 109, 116}
theorem cut626 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support626, holes i := by
  apply rounded_cover_cut ![support588, support600, OmissionResidual.support 5] ![3, 3, OmissionResidual.demand 5] ![1, 1, 1]
    support626 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut588 holes hbool hrows) (Fin.cases (cut600 holes hbool hrows) (Fin.cases (hrows 5) (fun i => Fin.elim0 i))))
def support627 : Finset (Fin 154) := {0, 6, 7, 10, 12, 14, 17, 20, 21, 25, 29, 30, 42, 43, 52, 56, 62, 67, 68, 72, 79, 83, 94, 124}
theorem cut627 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support627, holes i := by
  apply rounded_cover_cut ![support585, support597, OmissionResidual.support 1] ![2, 2, OmissionResidual.demand 1] ![1, 1, 1]
    support627 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut585 holes hbool hrows) (Fin.cases (cut597 holes hbool hrows) (Fin.cases (hrows 1) (fun i => Fin.elim0 i))))
def support628 : Finset (Fin 154) := {1, 6, 7, 10, 12, 14, 17, 20, 21, 25, 29, 30, 42, 43, 52, 56, 62, 67, 68, 72, 79, 83, 94, 124}
theorem cut628 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support628, holes i := by
  apply rounded_cover_cut ![support585, support597, OmissionResidual.support 5] ![2, 2, OmissionResidual.demand 5] ![1, 1, 1]
    support628 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut585 holes hbool hrows) (Fin.cases (cut597 holes hbool hrows) (Fin.cases (hrows 5) (fun i => Fin.elim0 i))))
def support629 : Finset (Fin 154) := {0, 6, 7, 10, 12, 14, 17, 20, 21, 25, 29, 30, 42, 43, 52, 56, 62, 67, 68, 72, 79, 83, 94, 117, 124}
theorem cut629 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support629, holes i := by
  apply rounded_cover_cut ![support586, support598, OmissionResidual.support 1] ![3, 3, OmissionResidual.demand 1] ![1, 1, 1]
    support629 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut586 holes hbool hrows) (Fin.cases (cut598 holes hbool hrows) (Fin.cases (hrows 1) (fun i => Fin.elim0 i))))
def support630 : Finset (Fin 154) := {1, 6, 7, 10, 12, 14, 17, 20, 21, 25, 29, 30, 42, 43, 52, 56, 62, 67, 68, 72, 79, 83, 94, 117, 124}
theorem cut630 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support630, holes i := by
  apply rounded_cover_cut ![support586, support598, OmissionResidual.support 5] ![3, 3, OmissionResidual.demand 5] ![1, 1, 1]
    support630 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut586 holes hbool hrows) (Fin.cases (cut598 holes hbool hrows) (Fin.cases (hrows 5) (fun i => Fin.elim0 i))))
def support631 : Finset (Fin 154) := {29, 37, 38, 41, 47, 51, 52, 57, 58, 62, 63, 69, 73, 77, 82, 83, 84, 89, 93, 94, 103, 124, 130}
theorem cut631 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support631, holes i := by
  apply rounded_cover_cut ![support53, support525, OmissionResidual.support 798] ![2, 2, OmissionResidual.demand 798] ![1, 1, 1]
    support631 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut53 holes hbool hrows) (Fin.cases (cut525 holes hbool hrows) (Fin.cases (hrows 798) (fun i => Fin.elim0 i))))
def support632 : Finset (Fin 154) := {22, 29, 32, 37, 38, 41, 42, 47, 51, 52, 57, 58, 62, 63, 69, 73, 77, 82, 83, 84, 89, 93, 94, 103, 124, 130}
theorem cut632 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support632, holes i := by
  apply rounded_cover_cut ![support53, support529, OmissionResidual.support 798] ![2, 2, OmissionResidual.demand 798] ![1, 1, 1]
    support632 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut53 holes hbool hrows) (Fin.cases (cut529 holes hbool hrows) (Fin.cases (hrows 798) (fun i => Fin.elim0 i))))
def support633 : Finset (Fin 154) := {29, 37, 38, 41, 47, 51, 52, 57, 58, 62, 63, 69, 73, 77, 82, 83, 84, 89, 93, 94, 103, 116, 123}
theorem cut633 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support633, holes i := by
  apply rounded_cover_cut ![support53, support525, OmissionResidual.support 797] ![2, 2, OmissionResidual.demand 797] ![1, 1, 1]
    support633 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut53 holes hbool hrows) (Fin.cases (cut525 holes hbool hrows) (Fin.cases (hrows 797) (fun i => Fin.elim0 i))))
def support634 : Finset (Fin 154) := {22, 29, 32, 37, 38, 41, 42, 47, 51, 52, 57, 58, 62, 63, 69, 73, 77, 82, 83, 84, 89, 93, 94, 103, 116, 123}
theorem cut634 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support634, holes i := by
  apply rounded_cover_cut ![support53, support529, OmissionResidual.support 797] ![2, 2, OmissionResidual.demand 797] ![1, 1, 1]
    support634 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut53 holes hbool hrows) (Fin.cases (cut529 holes hbool hrows) (Fin.cases (hrows 797) (fun i => Fin.elim0 i))))
def support635 : Finset (Fin 154) := {3, 4, 7, 8, 13, 17, 21, 23, 31, 33, 34, 35, 40, 44, 46, 59, 74}
theorem cut635 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support635, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 17, OmissionResidual.support 479, OmissionResidual.support 25] ![OmissionResidual.demand 17, OmissionResidual.demand 479, OmissionResidual.demand 25] ![1, 1, 1]
    support635 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 17) (Fin.cases (hrows 479) (Fin.cases (hrows 25) (fun i => Fin.elim0 i))))
def support636 : Finset (Fin 154) := {22, 28, 29, 32, 36, 37, 38, 40, 41, 42, 46, 47, 48, 51, 52, 57, 58, 61, 62, 63, 69, 73, 77, 80, 82, 83, 84, 89, 92, 93, 94, 103, 120, 124, 130}
theorem cut636 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support636, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 798, support378, support536] ![OmissionResidual.demand 798, 3, 3] ![1, 1, 1]
    support636 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 798) (Fin.cases (cut378 holes hbool hrows) (Fin.cases (cut536 holes hbool hrows) (fun i => Fin.elim0 i))))
def support637 : Finset (Fin 154) := {28, 29, 36, 37, 38, 40, 41, 46, 47, 48, 51, 52, 57, 58, 61, 62, 63, 69, 73, 77, 80, 82, 83, 84, 89, 92, 93, 94, 103, 120, 124, 130}
theorem cut637 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support637, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 798, support380, support536] ![OmissionResidual.demand 798, 3, 3] ![1, 1, 1]
    support637 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 798) (Fin.cases (cut380 holes hbool hrows) (Fin.cases (cut536 holes hbool hrows) (fun i => Fin.elim0 i))))
def support638 : Finset (Fin 154) := {22, 28, 29, 32, 36, 37, 38, 40, 41, 42, 46, 47, 48, 51, 52, 57, 58, 61, 62, 63, 69, 73, 77, 80, 82, 83, 84, 89, 92, 93, 94, 103, 116, 120, 123}
theorem cut638 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support638, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 797, support378, support536] ![OmissionResidual.demand 797, 3, 3] ![1, 1, 1]
    support638 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 797) (Fin.cases (cut378 holes hbool hrows) (Fin.cases (cut536 holes hbool hrows) (fun i => Fin.elim0 i))))
def support639 : Finset (Fin 154) := {28, 29, 36, 37, 38, 40, 41, 46, 47, 48, 51, 52, 57, 58, 61, 62, 63, 69, 73, 77, 80, 82, 83, 84, 89, 92, 93, 94, 103, 116, 120, 123}
theorem cut639 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support639, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 797, support380, support536] ![OmissionResidual.demand 797, 3, 3] ![1, 1, 1]
    support639 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 797) (Fin.cases (cut380 holes hbool hrows) (Fin.cases (cut536 holes hbool hrows) (fun i => Fin.elim0 i))))
def support640 : Finset (Fin 154) := {3, 8, 9, 12, 13, 17, 18, 26, 29, 33, 34, 41, 45, 47, 55, 60, 66, 75}
theorem cut640 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support640, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 861, OmissionResidual.support 20, OmissionResidual.support 863] ![OmissionResidual.demand 861, OmissionResidual.demand 20, OmissionResidual.demand 863] ![1, 1, 1]
    support640 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 861) (Fin.cases (hrows 20) (Fin.cases (hrows 863) (fun i => Fin.elim0 i))))
def support641 : Finset (Fin 154) := {28, 36, 40, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 81, 84, 87, 92, 93, 94, 97, 102, 103, 105, 106, 112, 116, 120, 124, 140}
theorem cut641 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support641, holes i := by
  apply rounded_cover_cut ![support552, OmissionResidual.support 736, support388] ![3, OmissionResidual.demand 736, 3] ![1, 1, 1]
    support641 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut552 holes hbool hrows) (Fin.cases (hrows 736) (Fin.cases (cut388 holes hbool hrows) (fun i => Fin.elim0 i))))
def support642 : Finset (Fin 154) := {28, 36, 40, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 81, 84, 87, 92, 93, 94, 97, 102, 103, 105, 106, 112, 116, 120, 124, 144}
theorem cut642 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support642, holes i := by
  apply rounded_cover_cut ![support545, OmissionResidual.support 736, support389] ![3, OmissionResidual.demand 736, 3] ![1, 1, 1]
    support642 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut545 holes hbool hrows) (Fin.cases (hrows 736) (Fin.cases (cut389 holes hbool hrows) (fun i => Fin.elim0 i))))
def support643 : Finset (Fin 154) := {41, 50, 55, 60, 63, 67, 70, 71, 72, 75, 78, 81, 82, 83, 87, 88, 93, 94, 97, 98, 103, 105, 106, 114}
theorem cut643 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support643, holes i := by
  apply rounded_cover_cut ![support594, support187, OmissionResidual.support 420] ![3, 3, OmissionResidual.demand 420] ![1, 1, 1]
    support643 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut594 holes hbool hrows) (Fin.cases (cut187 holes hbool hrows) (Fin.cases (hrows 420) (fun i => Fin.elim0 i))))
def support644 : Finset (Fin 154) := {38, 47, 51, 57, 63, 72, 73, 78, 80, 82, 98, 102, 112, 121}
theorem cut644 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support644, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 421, OmissionResidual.support 679, OmissionResidual.support 301] ![OmissionResidual.demand 421, OmissionResidual.demand 679, OmissionResidual.demand 301] ![1, 1, 1]
    support644 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 421) (Fin.cases (hrows 679) (Fin.cases (hrows 301) (fun i => Fin.elim0 i))))
def support645 : Finset (Fin 154) := {5, 9, 12, 13, 16, 18, 19, 26, 31, 32, 34, 37, 38, 41, 45, 47, 50, 51, 60, 66, 75}
theorem cut645 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support645, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 62, support335, OmissionResidual.support 863] ![OmissionResidual.demand 62, 2, OmissionResidual.demand 863] ![1, 1, 1]
    support645 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 62) (Fin.cases (cut335 holes hbool hrows) (Fin.cases (hrows 863) (fun i => Fin.elim0 i))))
def support646 : Finset (Fin 154) := {41, 50, 55, 60, 67, 71, 73, 83, 88, 93, 94, 97, 98, 102, 106, 120, 128}
theorem cut646 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support646, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 937, OmissionResidual.support 935, OmissionResidual.support 439] ![OmissionResidual.demand 937, OmissionResidual.demand 935, OmissionResidual.demand 439] ![1, 1, 1]
    support646 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 937) (Fin.cases (hrows 935) (Fin.cases (hrows 439) (fun i => Fin.elim0 i))))
def support647 : Finset (Fin 154) := {6, 8, 9, 12, 14, 17, 18, 21, 26, 29, 33, 34, 41, 45, 47, 55, 60, 66, 75}
theorem cut647 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support647, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 861, OmissionResidual.support 863, OmissionResidual.support 43] ![OmissionResidual.demand 861, OmissionResidual.demand 863, OmissionResidual.demand 43] ![1, 1, 1]
    support647 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 861) (Fin.cases (hrows 863) (Fin.cases (hrows 43) (fun i => Fin.elim0 i))))
def support648 : Finset (Fin 154) := {28, 36, 40, 46, 48, 50, 51, 58, 61, 63, 65, 69, 70, 73, 77, 80, 81, 84, 92, 93, 94, 97, 102, 103, 105, 106, 112, 116, 120, 124, 140}
theorem cut648 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support648, holes i := by
  apply rounded_cover_cut ![support552, support388, OmissionResidual.support 740] ![3, 3, OmissionResidual.demand 740] ![1, 1, 1]
    support648 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut552 holes hbool hrows) (Fin.cases (cut388 holes hbool hrows) (Fin.cases (hrows 740) (fun i => Fin.elim0 i))))
def support649 : Finset (Fin 154) := {28, 36, 40, 46, 48, 50, 51, 58, 61, 63, 65, 69, 70, 73, 77, 80, 81, 84, 92, 93, 94, 97, 102, 103, 105, 106, 112, 116, 120, 124, 144}
theorem cut649 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support649, holes i := by
  apply rounded_cover_cut ![support545, support389, OmissionResidual.support 740] ![3, 3, OmissionResidual.demand 740] ![1, 1, 1]
    support649 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut545 holes hbool hrows) (Fin.cases (cut389 holes hbool hrows) (Fin.cases (hrows 740) (fun i => Fin.elim0 i))))
def support650 : Finset (Fin 154) := {28, 36, 40, 46, 48, 50, 51, 58, 61, 63, 65, 69, 70, 73, 77, 80, 81, 84, 92, 93, 97, 102, 105, 120}
theorem cut650 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support650, holes i := by
  apply rounded_cover_cut ![support282, support372, OmissionResidual.support 740] ![2, 2, OmissionResidual.demand 740] ![1, 1, 1]
    support650 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut282 holes hbool hrows) (Fin.cases (cut372 holes hbool hrows) (Fin.cases (hrows 740) (fun i => Fin.elim0 i))))
#print axioms cut650
def support651 : Finset (Fin 154) := {38, 47, 57, 66, 69, 73, 78, 80, 83, 88, 93, 98, 102, 105, 112, 121}
theorem cut651 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support651, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 927, OmissionResidual.support 930, OmissionResidual.support 438] ![OmissionResidual.demand 927, OmissionResidual.demand 930, OmissionResidual.demand 438] ![1, 1, 1]
    support651 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 927) (Fin.cases (hrows 930) (Fin.cases (hrows 438) (fun i => Fin.elim0 i))))
def support652 : Finset (Fin 154) := {21, 27, 31, 36, 38, 47, 48, 52, 57, 58, 66, 69, 73, 78, 80, 83, 88, 93, 98, 102, 105, 112, 121}
theorem cut652 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support652, holes i := by
  apply rounded_cover_cut ![support651, OmissionResidual.support 584, support424] ![3, OmissionResidual.demand 584, 3] ![1, 1, 1]
    support652 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut651 holes hbool hrows) (Fin.cases (hrows 584) (Fin.cases (cut424 holes hbool hrows) (fun i => Fin.elim0 i))))
def support653 : Finset (Fin 154) := {22, 32, 37, 38, 42, 47, 51, 57, 58, 63, 65, 69, 77, 84, 94, 103, 106, 114}
theorem cut653 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support653, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 588, OmissionResidual.support 677, OmissionResidual.support 680] ![OmissionResidual.demand 588, OmissionResidual.demand 677, OmissionResidual.demand 680] ![1, 1, 1]
    support653 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 588) (Fin.cases (hrows 677) (Fin.cases (hrows 680) (fun i => Fin.elim0 i))))
def support654 : Finset (Fin 154) := {0, 7, 11, 12, 14, 16, 20, 23, 30, 33, 46, 57, 59, 67, 70, 78, 82, 96}
theorem cut654 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support654, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 466, OmissionResidual.support 878, OmissionResidual.support 900] ![OmissionResidual.demand 466, OmissionResidual.demand 878, OmissionResidual.demand 900] ![1, 1, 1]
    support654 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 466) (Fin.cases (hrows 878) (Fin.cases (hrows 900) (fun i => Fin.elim0 i))))
def support655 : Finset (Fin 154) := {1, 7, 11, 12, 14, 16, 20, 23, 30, 33, 46, 57, 59, 67, 70, 78, 82, 96}
theorem cut655 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support655, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 468, OmissionResidual.support 878, OmissionResidual.support 900] ![OmissionResidual.demand 468, OmissionResidual.demand 878, OmissionResidual.demand 900] ![1, 1, 1]
    support655 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 468) (Fin.cases (hrows 878) (Fin.cases (hrows 900) (fun i => Fin.elim0 i))))
def support656 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 63, 69, 73, 76, 80, 84, 88, 102, 103, 113}
theorem cut656 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support656, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 355, OmissionResidual.support 679, OmissionResidual.support 680] ![OmissionResidual.demand 355, OmissionResidual.demand 679, OmissionResidual.demand 680] ![1, 1, 1]
    support656 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 355) (Fin.cases (hrows 679) (Fin.cases (hrows 680) (fun i => Fin.elim0 i))))
def support657 : Finset (Fin 154) := {51, 60, 61, 66, 70, 71, 76, 81, 88, 90, 92, 93, 100, 102, 113, 115, 122}
theorem cut657 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support657, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 404, OmissionResidual.support 952, OmissionResidual.support 951] ![OmissionResidual.demand 404, OmissionResidual.demand 952, OmissionResidual.demand 951] ![1, 1, 1]
    support657 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 404) (Fin.cases (hrows 952) (Fin.cases (hrows 951) (fun i => Fin.elim0 i))))
def support658 : Finset (Fin 154) := {87, 96, 105, 106, 113, 114, 118, 121, 123, 128, 132, 135, 137, 138, 144, 146, 150}
theorem cut658 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support658, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1139, OmissionResidual.support 1100, OmissionResidual.support 1097] ![OmissionResidual.demand 1139, OmissionResidual.demand 1100, OmissionResidual.demand 1097] ![1, 1, 1]
    support658 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1139) (Fin.cases (hrows 1100) (Fin.cases (hrows 1097) (fun i => Fin.elim0 i))))
def support659 : Finset (Fin 154) := {87, 96, 105, 106, 113, 114, 118, 121, 123, 128, 132, 135, 137, 138, 140, 146, 148}
theorem cut659 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support659, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1100, OmissionResidual.support 1097, OmissionResidual.support 1138] ![OmissionResidual.demand 1100, OmissionResidual.demand 1097, OmissionResidual.demand 1138] ![1, 1, 1]
    support659 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1100) (Fin.cases (hrows 1097) (Fin.cases (hrows 1138) (fun i => Fin.elim0 i))))
def support660 : Finset (Fin 154) := {49, 59, 61, 64, 71, 76, 81, 87, 88, 92, 93, 97, 102, 105, 113}
theorem cut660 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support660, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 404, OmissionResidual.support 737, OmissionResidual.support 736] ![OmissionResidual.demand 404, OmissionResidual.demand 737, OmissionResidual.demand 736] ![1, 1, 1]
    support660 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 404) (Fin.cases (hrows 737) (Fin.cases (hrows 736) (fun i => Fin.elim0 i))))
def support661 : Finset (Fin 154) := {87, 96, 105, 106, 113, 114, 118, 121, 128, 129, 130, 132, 138, 141, 142, 144, 150}
theorem cut661 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support661, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1139, OmissionResidual.support 1098, OmissionResidual.support 1099] ![OmissionResidual.demand 1139, OmissionResidual.demand 1098, OmissionResidual.demand 1099] ![1, 1, 1]
    support661 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1139) (Fin.cases (hrows 1098) (Fin.cases (hrows 1099) (fun i => Fin.elim0 i))))
def support662 : Finset (Fin 154) := {87, 96, 105, 106, 113, 114, 118, 121, 128, 129, 130, 132, 138, 140, 141, 142, 148}
theorem cut662 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support662, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1098, OmissionResidual.support 1138, OmissionResidual.support 1099] ![OmissionResidual.demand 1098, OmissionResidual.demand 1138, OmissionResidual.demand 1099] ![1, 1, 1]
    support662 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1098) (Fin.cases (hrows 1138) (Fin.cases (hrows 1099) (fun i => Fin.elim0 i))))
def support663 : Finset (Fin 154) := {50, 62, 65, 70, 77, 81, 82, 89, 93, 103, 106, 108, 114, 115, 116, 123}
theorem cut663 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support663, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 741, OmissionResidual.support 797, OmissionResidual.support 742] ![OmissionResidual.demand 741, OmissionResidual.demand 797, OmissionResidual.demand 742] ![1, 1, 1]
    support663 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 741) (Fin.cases (hrows 797) (Fin.cases (hrows 742) (fun i => Fin.elim0 i))))
def support664 : Finset (Fin 154) := {50, 62, 65, 70, 77, 81, 82, 89, 93, 103, 106, 108, 114, 115, 124, 130}
theorem cut664 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support664, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 741, OmissionResidual.support 798, OmissionResidual.support 742] ![OmissionResidual.demand 741, OmissionResidual.demand 798, OmissionResidual.demand 742] ![1, 1, 1]
    support664 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 741) (Fin.cases (hrows 798) (Fin.cases (hrows 742) (fun i => Fin.elim0 i))))
def support665 : Finset (Fin 154) := {73, 83, 88, 93, 94, 100, 102, 103, 106, 112, 116, 117, 120, 124, 135, 140}
theorem cut665 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support665, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 969, OmissionResidual.support 970, OmissionResidual.support 842] ![OmissionResidual.demand 969, OmissionResidual.demand 970, OmissionResidual.demand 842] ![1, 1, 1]
    support665 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 969) (Fin.cases (hrows 970) (Fin.cases (hrows 842) (fun i => Fin.elim0 i))))
def support666 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 63, 69, 73, 76, 80, 88, 93, 102, 113}
theorem cut666 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support666, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 355, OmissionResidual.support 679, OmissionResidual.support 678] ![OmissionResidual.demand 355, OmissionResidual.demand 679, OmissionResidual.demand 678] ![1, 1, 1]
    support666 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 355) (Fin.cases (hrows 679) (Fin.cases (hrows 678) (fun i => Fin.elim0 i))))
def support667 : Finset (Fin 154) := {48, 58, 61, 69, 73, 76, 80, 83, 84, 88, 93, 94, 97, 102, 103, 106, 108, 112, 113, 116, 120, 124, 134, 135, 144}
theorem cut667 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support667, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 355, support418, support106] ![OmissionResidual.demand 355, 2, 2] ![1, 1, 1]
    support667 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 355) (Fin.cases (cut418 holes hbool hrows) (Fin.cases (cut106 holes hbool hrows) (fun i => Fin.elim0 i))))
def support668 : Finset (Fin 154) := {48, 58, 69, 76, 80, 88, 94, 98, 103, 106, 112, 116, 120, 121, 124, 128, 140}
theorem cut668 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support668, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 945, OmissionResidual.support 946, OmissionResidual.support 842] ![OmissionResidual.demand 945, OmissionResidual.demand 946, OmissionResidual.demand 842] ![1, 1, 1]
    support668 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 945) (Fin.cases (hrows 946) (Fin.cases (hrows 842) (fun i => Fin.elim0 i))))
def support669 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 103, 106, 112, 116, 120, 121, 124, 128, 140}
theorem cut669 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support669, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 959, OmissionResidual.support 960, OmissionResidual.support 842] ![OmissionResidual.demand 959, OmissionResidual.demand 960, OmissionResidual.demand 842] ![1, 1, 1]
    support669 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 959) (Fin.cases (hrows 960) (Fin.cases (hrows 842) (fun i => Fin.elim0 i))))
def support670 : Finset (Fin 154) := {48, 58, 69, 76, 80, 88, 94, 98, 103, 106, 112, 116, 120, 121, 124, 128, 144}
theorem cut670 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support670, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 945, OmissionResidual.support 946, OmissionResidual.support 843] ![OmissionResidual.demand 945, OmissionResidual.demand 946, OmissionResidual.demand 843] ![1, 1, 1]
    support670 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 945) (Fin.cases (hrows 946) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
def support671 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 103, 106, 112, 116, 120, 121, 124, 128, 144}
theorem cut671 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support671, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 959, OmissionResidual.support 960, OmissionResidual.support 843] ![OmissionResidual.demand 959, OmissionResidual.demand 960, OmissionResidual.demand 843] ![1, 1, 1]
    support671 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 959) (Fin.cases (hrows 960) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
def support672 : Finset (Fin 154) := {0, 5, 6, 7, 11, 12, 16, 18, 20, 23, 27, 30, 32, 37, 41, 50}
theorem cut672 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support672, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 490, OmissionResidual.support 484, OmissionResidual.support 466] ![OmissionResidual.demand 490, OmissionResidual.demand 484, OmissionResidual.demand 466] ![1, 1, 1]
    support672 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 490) (Fin.cases (hrows 484) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support673 : Finset (Fin 154) := {1, 5, 6, 7, 11, 12, 16, 18, 20, 23, 27, 30, 32, 37, 41, 50}
theorem cut673 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support673, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 490, OmissionResidual.support 484, OmissionResidual.support 468] ![OmissionResidual.demand 490, OmissionResidual.demand 484, OmissionResidual.demand 468] ![1, 1, 1]
    support673 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 490) (Fin.cases (hrows 484) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support674 : Finset (Fin 154) := {0, 3, 7, 10, 11, 12, 16, 18, 20, 23, 27, 30, 32, 37, 41, 50}
theorem cut674 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support674, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 475, OmissionResidual.support 512, OmissionResidual.support 466] ![OmissionResidual.demand 475, OmissionResidual.demand 512, OmissionResidual.demand 466] ![1, 1, 1]
    support674 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 475) (Fin.cases (hrows 512) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support675 : Finset (Fin 154) := {1, 3, 7, 10, 11, 12, 16, 18, 20, 23, 27, 30, 32, 37, 41, 50}
theorem cut675 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support675, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 475, OmissionResidual.support 512, OmissionResidual.support 468] ![OmissionResidual.demand 475, OmissionResidual.demand 512, OmissionResidual.demand 468] ![1, 1, 1]
    support675 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 475) (Fin.cases (hrows 512) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
#print axioms cut675
def support676 : Finset (Fin 154) := {43, 74, 85, 87, 89, 96, 105, 107, 110, 114, 115, 118, 123, 125, 130, 138, 142}
theorem cut676 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support676, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1006, OmissionResidual.support 1098, OmissionResidual.support 1107] ![OmissionResidual.demand 1006, OmissionResidual.demand 1098, OmissionResidual.demand 1107] ![1, 1, 1]
    support676 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1006) (Fin.cases (hrows 1098) (Fin.cases (hrows 1107) (fun i => Fin.elim0 i))))
def support677 : Finset (Fin 154) := {6, 11, 14, 20, 23, 27, 29, 32, 37, 41, 46, 50, 52, 57, 63, 69, 82, 84, 103}
theorem cut677 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support677, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 490, OmissionResidual.support 542, OmissionResidual.support 632] ![OmissionResidual.demand 490, OmissionResidual.demand 542, OmissionResidual.demand 632] ![1, 1, 1]
    support677 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 490) (Fin.cases (hrows 542) (Fin.cases (hrows 632) (fun i => Fin.elim0 i))))
def support678 : Finset (Fin 154) := {15, 22, 27, 29, 34, 36, 38, 45, 48, 56, 58, 71, 73, 76, 83, 86, 88, 97}
theorem cut678 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support678, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 177, OmissionResidual.support 882, OmissionResidual.support 880] ![OmissionResidual.demand 177, OmissionResidual.demand 882, OmissionResidual.demand 880] ![1, 1, 1]
    support678 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 882) (Fin.cases (hrows 880) (fun i => Fin.elim0 i))))
def support679 : Finset (Fin 154) := {0, 3, 6, 7, 11, 12, 17, 18, 20, 25, 27, 30, 32, 37, 41, 43, 50}
theorem cut679 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support679, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 475, OmissionResidual.support 490, OmissionResidual.support 1] ![OmissionResidual.demand 475, OmissionResidual.demand 490, OmissionResidual.demand 1] ![1, 1, 1]
    support679 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 475) (Fin.cases (hrows 490) (Fin.cases (hrows 1) (fun i => Fin.elim0 i))))
def support680 : Finset (Fin 154) := {1, 3, 6, 7, 11, 12, 17, 18, 20, 25, 27, 30, 32, 37, 41, 43, 50}
theorem cut680 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support680, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 475, OmissionResidual.support 490, OmissionResidual.support 5] ![OmissionResidual.demand 475, OmissionResidual.demand 490, OmissionResidual.demand 5] ![1, 1, 1]
    support680 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 475) (Fin.cases (hrows 490) (Fin.cases (hrows 5) (fun i => Fin.elim0 i))))
def support681 : Finset (Fin 154) := {2, 4, 7, 23, 24, 25, 26, 31, 34, 36, 40, 49, 56, 61, 64, 73, 88}
theorem cut681 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support681, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 13, OmissionResidual.support 478, OmissionResidual.support 201] ![OmissionResidual.demand 13, OmissionResidual.demand 478, OmissionResidual.demand 201] ![1, 1, 1]
    support681 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 13) (Fin.cases (hrows 478) (Fin.cases (hrows 201) (fun i => Fin.elim0 i))))
def support682 : Finset (Fin 154) := {73, 83, 88, 93, 94, 100, 102, 103, 106, 112, 116, 117, 120, 124, 135, 140, 144}
theorem cut682 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support682, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 969, OmissionResidual.support 970, OmissionResidual.support 843] ![OmissionResidual.demand 969, OmissionResidual.demand 970, OmissionResidual.demand 843] ![1, 1, 1]
    support682 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 969) (Fin.cases (hrows 970) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
def support683 : Finset (Fin 154) := {43, 74, 85, 87, 89, 96, 107, 110, 113, 115, 118, 121, 123, 125, 130, 135, 138, 142, 146}
theorem cut683 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support683, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1006, OmissionResidual.support 1100, OmissionResidual.support 1107] ![OmissionResidual.demand 1006, OmissionResidual.demand 1100, OmissionResidual.demand 1107] ![1, 1, 1]
    support683 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1006) (Fin.cases (hrows 1100) (Fin.cases (hrows 1107) (fun i => Fin.elim0 i))))
def support684 : Finset (Fin 154) := {48, 58, 61, 69, 73, 76, 80, 83, 84, 88, 93, 94, 97, 102, 103, 106, 108, 112, 113, 116, 120, 124, 129, 140, 144}
theorem cut684 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support684, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 355, support74, support418] ![OmissionResidual.demand 355, 2, 2] ![1, 1, 1]
    support684 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 355) (Fin.cases (cut74 holes hbool hrows) (Fin.cases (cut418 holes hbool hrows) (fun i => Fin.elim0 i))))
def support685 : Finset (Fin 154) := {48, 58, 61, 69, 73, 76, 80, 83, 84, 88, 93, 94, 97, 102, 103, 106, 108, 112, 113, 116, 120, 124, 134, 135, 140, 144}
theorem cut685 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support685, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 355, support48, support418] ![OmissionResidual.demand 355, 2, 2] ![1, 1, 1]
    support685 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 355) (Fin.cases (cut48 holes hbool hrows) (Fin.cases (cut418 holes hbool hrows) (fun i => Fin.elim0 i))))
def support686 : Finset (Fin 154) := {2, 4, 7, 13, 21, 23, 25, 26, 31, 34, 36, 40, 44, 49, 64}
theorem cut686 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support686, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 13, OmissionResidual.support 478, OmissionResidual.support 10] ![OmissionResidual.demand 13, OmissionResidual.demand 478, OmissionResidual.demand 10] ![1, 1, 1]
    support686 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 13) (Fin.cases (hrows 478) (Fin.cases (hrows 10) (fun i => Fin.elim0 i))))
def support687 : Finset (Fin 154) := {1, 2, 4, 7, 13, 17, 21, 23, 25, 26, 31, 34, 36, 40, 44, 49, 64}
theorem cut687 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support687, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 13, OmissionResidual.support 478, OmissionResidual.support 7] ![OmissionResidual.demand 13, OmissionResidual.demand 478, OmissionResidual.demand 7] ![1, 1, 1]
    support687 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 13) (Fin.cases (hrows 478) (Fin.cases (hrows 7) (fun i => Fin.elim0 i))))
def support688 : Finset (Fin 154) := {2, 4, 5, 7, 8, 13, 21, 23, 25, 26, 31, 34, 36, 40, 44, 49, 64}
theorem cut688 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support688, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 13, OmissionResidual.support 478, OmissionResidual.support 30] ![OmissionResidual.demand 13, OmissionResidual.demand 478, OmissionResidual.demand 30] ![1, 1, 1]
    support688 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 13) (Fin.cases (hrows 478) (Fin.cases (hrows 30) (fun i => Fin.elim0 i))))
def support689 : Finset (Fin 154) := {2, 3, 4, 7, 8, 13, 17, 21, 23, 25, 26, 31, 34, 36, 40, 44, 49, 64}
theorem cut689 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support689, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 13, OmissionResidual.support 478, OmissionResidual.support 17] ![OmissionResidual.demand 13, OmissionResidual.demand 478, OmissionResidual.demand 17] ![1, 1, 1]
    support689 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 13) (Fin.cases (hrows 478) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support690 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 63, 69, 76, 80, 84, 88, 103, 112, 121}
theorem cut690 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support690, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 680, OmissionResidual.support 681, OmissionResidual.support 356] ![OmissionResidual.demand 680, OmissionResidual.demand 681, OmissionResidual.demand 356] ![1, 1, 1]
    support690 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 680) (Fin.cases (hrows 681) (Fin.cases (hrows 356) (fun i => Fin.elim0 i))))
def support691 : Finset (Fin 154) := {61, 71, 73, 76, 81, 83, 88, 92, 93, 94, 100, 102, 103, 106, 109, 112, 113, 116, 120, 124, 129, 134, 140}
theorem cut691 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support691, holes i := by
  apply rounded_cover_cut ![support199, support223, OmissionResidual.support 842] ![3, 3, OmissionResidual.demand 842] ![1, 1, 1]
    support691 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut199 holes hbool hrows) (Fin.cases (cut223 holes hbool hrows) (Fin.cases (hrows 842) (fun i => Fin.elim0 i))))
def support692 : Finset (Fin 154) := {61, 71, 73, 76, 81, 83, 88, 92, 93, 94, 100, 102, 103, 106, 109, 112, 113, 116, 120, 124, 129, 134, 144}
theorem cut692 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support692, holes i := by
  apply rounded_cover_cut ![support199, support223, OmissionResidual.support 843] ![3, 3, OmissionResidual.demand 843] ![1, 1, 1]
    support692 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut199 holes hbool hrows) (Fin.cases (cut223 holes hbool hrows) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
def support693 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 62, 63, 69, 73, 76, 77, 80, 82, 84, 88, 89, 93, 102, 103, 113, 124, 130}
theorem cut693 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support693, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 798, support656, support666] ![OmissionResidual.demand 798, 2, 2] ![1, 1, 1]
    support693 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 798) (Fin.cases (cut656 holes hbool hrows) (Fin.cases (cut666 holes hbool hrows) (fun i => Fin.elim0 i))))
def support694 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 62, 63, 69, 73, 76, 77, 80, 82, 84, 88, 89, 93, 102, 103, 113, 116, 123}
theorem cut694 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support694, holes i := by
  apply rounded_cover_cut ![support656, OmissionResidual.support 797, support666] ![2, OmissionResidual.demand 797, 2] ![1, 1, 1]
    support694 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut656 holes hbool hrows) (Fin.cases (hrows 797) (Fin.cases (cut666 holes hbool hrows) (fun i => Fin.elim0 i))))
def support695 : Finset (Fin 154) := {3, 8, 13, 17, 29, 32, 41, 45, 50, 55, 60, 68, 71, 79, 83, 100, 108}
theorem cut695 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support695, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 939, OmissionResidual.support 925, OmissionResidual.support 20] ![OmissionResidual.demand 939, OmissionResidual.demand 925, OmissionResidual.demand 20] ![1, 1, 1]
    support695 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 939) (Fin.cases (hrows 925) (Fin.cases (hrows 20) (fun i => Fin.elim0 i))))
def support696 : Finset (Fin 154) := {5, 8, 13, 25, 29, 32, 41, 45, 50, 55, 60, 68, 71, 79, 83, 100, 108}
theorem cut696 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support696, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 939, OmissionResidual.support 925, OmissionResidual.support 35] ![OmissionResidual.demand 939, OmissionResidual.demand 925, OmissionResidual.demand 35] ![1, 1, 1]
    support696 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 939) (Fin.cases (hrows 925) (Fin.cases (hrows 35) (fun i => Fin.elim0 i))))
def support697 : Finset (Fin 154) := {8, 12, 23, 26, 29, 37, 38, 41, 47, 51, 52, 57, 60, 62, 63, 69, 73, 77, 82, 84, 89, 93, 103, 124, 130}
theorem cut697 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support697, holes i := by
  apply rounded_cover_cut ![support295, OmissionResidual.support 497, support291] ![2, OmissionResidual.demand 497, 2] ![1, 1, 1]
    support697 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut295 holes hbool hrows) (Fin.cases (hrows 497) (Fin.cases (cut291 holes hbool hrows) (fun i => Fin.elim0 i))))
def support698 : Finset (Fin 154) := {8, 12, 23, 26, 29, 37, 38, 41, 47, 51, 52, 57, 60, 62, 63, 69, 73, 77, 82, 84, 89, 93, 103, 116, 123}
theorem cut698 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support698, holes i := by
  apply rounded_cover_cut ![support294, OmissionResidual.support 497, support290] ![2, OmissionResidual.demand 497, 2] ![1, 1, 1]
    support698 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut294 holes hbool hrows) (Fin.cases (hrows 497) (Fin.cases (cut290 holes hbool hrows) (fun i => Fin.elim0 i))))
def support699 : Finset (Fin 154) := {4, 7, 19, 21, 23, 26, 27, 31, 35, 40, 41, 46, 51, 59, 61, 69, 81}
theorem cut699 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support699, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 479, OmissionResidual.support 571, OmissionResidual.support 581] ![OmissionResidual.demand 479, OmissionResidual.demand 571, OmissionResidual.demand 581] ![1, 1, 1]
    support699 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 479) (Fin.cases (hrows 571) (Fin.cases (hrows 581) (fun i => Fin.elim0 i))))
def support700 : Finset (Fin 154) := {76, 86, 95, 104, 116, 119, 121, 123, 127, 128, 129, 132, 134, 141, 143, 144, 145, 152}
theorem cut700 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support700, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1073, OmissionResidual.support 1153, OmissionResidual.support 1072] ![OmissionResidual.demand 1073, OmissionResidual.demand 1153, OmissionResidual.demand 1072] ![1, 1, 1]
    support700 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1073) (Fin.cases (hrows 1153) (Fin.cases (hrows 1072) (fun i => Fin.elim0 i))))
#print axioms cut700
def support701 : Finset (Fin 154) := {8, 12, 19, 21, 23, 26, 27, 31, 35, 40, 41, 46, 51, 59, 61, 69, 81}
theorem cut701 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support701, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 571, OmissionResidual.support 496, OmissionResidual.support 581] ![OmissionResidual.demand 571, OmissionResidual.demand 496, OmissionResidual.demand 581] ![1, 1, 1]
    support701 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 571) (Fin.cases (hrows 496) (Fin.cases (hrows 581) (fun i => Fin.elim0 i))))
def support702 : Finset (Fin 154) := {60, 61, 70, 71, 75, 76, 81, 87, 88, 92, 103, 106, 112, 114, 121}
theorem cut702 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support702, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 780, OmissionResidual.support 405, OmissionResidual.support 781] ![OmissionResidual.demand 780, OmissionResidual.demand 405, OmissionResidual.demand 781] ![1, 1, 1]
    support702 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 780) (Fin.cases (hrows 405) (Fin.cases (hrows 781) (fun i => Fin.elim0 i))))
def support703 : Finset (Fin 154) := {5, 8, 9, 12, 13, 19, 22, 23, 24, 25, 26, 29, 31, 34, 36, 38, 40, 45, 48, 49, 56, 61, 64, 73, 76, 88}
theorem cut703 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support703, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 177, support512, OmissionResidual.support 33, OmissionResidual.support 495] ![OmissionResidual.demand 177, 2, OmissionResidual.demand 33, OmissionResidual.demand 495] ![1, 1, 1, 1]
    support703 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (cut512 holes hbool hrows) (Fin.cases (hrows 33) (Fin.cases (hrows 495) (fun i => Fin.elim0 i)))))
def support704 : Finset (Fin 154) := {40, 49, 59, 64, 74, 78, 88, 92, 99, 102, 104, 108, 113, 118, 122, 126, 136}
theorem cut704 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support704, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1043, OmissionResidual.support 739, OmissionResidual.support 313] ![OmissionResidual.demand 1043, OmissionResidual.demand 739, OmissionResidual.demand 313] ![1, 1, 1]
    support704 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1043) (Fin.cases (hrows 739) (Fin.cases (hrows 313) (fun i => Fin.elim0 i))))
def support705 : Finset (Fin 154) := {42, 56, 62, 68, 72, 82, 83, 87, 93, 94, 97, 99, 100, 102, 103, 106, 108, 112, 116, 120, 124, 129, 130, 140}
theorem cut705 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support705, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 717, support111, support74] ![OmissionResidual.demand 717, 2, 2] ![1, 1, 1]
    support705 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 717) (Fin.cases (cut111 holes hbool hrows) (Fin.cases (cut74 holes hbool hrows) (fun i => Fin.elim0 i))))
def support706 : Finset (Fin 154) := {42, 56, 62, 68, 72, 82, 83, 87, 93, 94, 97, 99, 100, 102, 103, 106, 108, 112, 116, 120, 124, 129, 130, 140, 144}
theorem cut706 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support706, holes i := by
  apply rounded_cover_cut ![support183, OmissionResidual.support 717, support74] ![2, OmissionResidual.demand 717, 2] ![1, 1, 1]
    support706 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut183 holes hbool hrows) (Fin.cases (hrows 717) (Fin.cases (cut74 holes hbool hrows) (fun i => Fin.elim0 i))))
def support707 : Finset (Fin 154) := {42, 56, 62, 68, 72, 82, 83, 87, 93, 94, 97, 99, 100, 102, 103, 106, 108, 112, 116, 120, 123, 124, 134, 135, 144}
theorem cut707 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support707, holes i := by
  apply rounded_cover_cut ![support167, OmissionResidual.support 717, support106] ![2, OmissionResidual.demand 717, 2] ![1, 1, 1]
    support707 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut167 holes hbool hrows) (Fin.cases (hrows 717) (Fin.cases (cut106 holes hbool hrows) (fun i => Fin.elim0 i))))
def support708 : Finset (Fin 154) := {42, 56, 62, 68, 72, 82, 83, 87, 93, 94, 97, 99, 100, 102, 103, 106, 108, 112, 116, 120, 123, 124, 134, 135, 140}
theorem cut708 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support708, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 717, support85, support48] ![OmissionResidual.demand 717, 2, 2] ![1, 1, 1]
    support708 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 717) (Fin.cases (cut85 holes hbool hrows) (Fin.cases (cut48 holes hbool hrows) (fun i => Fin.elim0 i))))
def support709 : Finset (Fin 154) := {42, 56, 62, 68, 72, 82, 83, 87, 93, 94, 97, 99, 100, 102, 103, 106, 108, 112, 116, 120, 123, 124, 134, 135, 140, 144}
theorem cut709 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support709, holes i := by
  apply rounded_cover_cut ![support167, OmissionResidual.support 717, support48] ![2, OmissionResidual.demand 717, 2] ![1, 1, 1]
    support709 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut167 holes hbool hrows) (Fin.cases (hrows 717) (Fin.cases (cut48 holes hbool hrows) (fun i => Fin.elim0 i))))
def support710 : Finset (Fin 154) := {8, 12, 26, 33, 35, 36, 44, 46, 59, 64, 74, 75, 80, 86, 92, 104}
theorem cut710 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support710, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 51, OmissionResidual.support 673, OmissionResidual.support 617] ![OmissionResidual.demand 51, OmissionResidual.demand 673, OmissionResidual.demand 617] ![1, 1, 1]
    support710 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 51) (Fin.cases (hrows 673) (Fin.cases (hrows 617) (fun i => Fin.elim0 i))))
def support711 : Finset (Fin 154) := {4, 7, 26, 33, 35, 36, 44, 46, 59, 64, 74, 75, 80, 86, 92, 104}
theorem cut711 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support711, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 673, OmissionResidual.support 25, OmissionResidual.support 617] ![OmissionResidual.demand 673, OmissionResidual.demand 25, OmissionResidual.demand 617] ![1, 1, 1]
    support711 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 673) (Fin.cases (hrows 25) (Fin.cases (hrows 617) (fun i => Fin.elim0 i))))
def support712 : Finset (Fin 154) := {8, 12, 19, 26, 28, 33, 35, 36, 40, 44, 46, 51, 59, 61, 74, 80, 92}
theorem cut712 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support712, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 51, OmissionResidual.support 623, OmissionResidual.support 572] ![OmissionResidual.demand 51, OmissionResidual.demand 623, OmissionResidual.demand 572] ![1, 1, 1]
    support712 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 51) (Fin.cases (hrows 623) (Fin.cases (hrows 572) (fun i => Fin.elim0 i))))
def support713 : Finset (Fin 154) := {4, 7, 19, 26, 28, 33, 35, 36, 40, 44, 46, 51, 59, 61, 74, 80, 92}
theorem cut713 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support713, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 25, OmissionResidual.support 623, OmissionResidual.support 572] ![OmissionResidual.demand 25, OmissionResidual.demand 623, OmissionResidual.demand 572] ![1, 1, 1]
    support713 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 25) (Fin.cases (hrows 623) (Fin.cases (hrows 572) (fun i => Fin.elim0 i))))
def support714 : Finset (Fin 154) := {8, 12, 13, 18, 27, 33, 35, 39, 44, 53, 55, 57, 66, 70, 85}
theorem cut714 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support714, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 862, OmissionResidual.support 49, OmissionResidual.support 872] ![OmissionResidual.demand 862, OmissionResidual.demand 49, OmissionResidual.demand 872] ![1, 1, 1]
    support714 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 862) (Fin.cases (hrows 49) (Fin.cases (hrows 872) (fun i => Fin.elim0 i))))
def support715 : Finset (Fin 154) := {108, 115, 122, 124, 126, 129, 130, 134, 135, 138, 140, 143, 144, 148, 149, 152}
theorem cut715 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support715, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1142, OmissionResidual.support 1159, OmissionResidual.support 1141] ![OmissionResidual.demand 1142, OmissionResidual.demand 1159, OmissionResidual.demand 1141] ![1, 1, 1]
    support715 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1142) (Fin.cases (hrows 1159) (Fin.cases (hrows 1141) (fun i => Fin.elim0 i))))
def support716 : Finset (Fin 154) := {108, 115, 122, 124, 126, 129, 130, 134, 135, 138, 140, 143, 144, 148, 149, 153}
theorem cut716 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support716, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1142, OmissionResidual.support 1160, OmissionResidual.support 1141] ![OmissionResidual.demand 1142, OmissionResidual.demand 1160, OmissionResidual.demand 1141] ![1, 1, 1]
    support716 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1142) (Fin.cases (hrows 1160) (Fin.cases (hrows 1141) (fun i => Fin.elim0 i))))
def support717 : Finset (Fin 154) := {42, 56, 62, 63, 68, 72, 77, 78, 82, 83, 89, 90, 93, 94, 103, 116, 123}
theorem cut717 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support717, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 418, OmissionResidual.support 341, OmissionResidual.support 797] ![OmissionResidual.demand 418, OmissionResidual.demand 341, OmissionResidual.demand 797] ![1, 1, 1]
    support717 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 418) (Fin.cases (hrows 341) (Fin.cases (hrows 797) (fun i => Fin.elim0 i))))
def support718 : Finset (Fin 154) := {42, 56, 62, 63, 68, 72, 77, 78, 82, 83, 89, 90, 93, 94, 103, 109, 116, 123}
theorem cut718 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support718, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 963, OmissionResidual.support 943, OmissionResidual.support 797] ![OmissionResidual.demand 963, OmissionResidual.demand 943, OmissionResidual.demand 797] ![1, 1, 1]
    support718 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 963) (Fin.cases (hrows 943) (Fin.cases (hrows 797) (fun i => Fin.elim0 i))))
def support719 : Finset (Fin 154) := {42, 56, 62, 63, 68, 72, 77, 78, 82, 83, 89, 90, 93, 94, 103, 117, 124, 130}
theorem cut719 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support719, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 965, OmissionResidual.support 944, OmissionResidual.support 798] ![OmissionResidual.demand 965, OmissionResidual.demand 944, OmissionResidual.demand 798] ![1, 1, 1]
    support719 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 965) (Fin.cases (hrows 944) (Fin.cases (hrows 798) (fun i => Fin.elim0 i))))
def support720 : Finset (Fin 154) := {8, 12, 13, 18, 26, 33, 35, 36, 44, 49, 55, 57, 64, 66, 70, 85}
theorem cut720 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support720, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 50, OmissionResidual.support 862, OmissionResidual.support 872] ![OmissionResidual.demand 50, OmissionResidual.demand 862, OmissionResidual.demand 872] ![1, 1, 1]
    support720 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 50) (Fin.cases (hrows 862) (Fin.cases (hrows 872) (fun i => Fin.elim0 i))))
def support721 : Finset (Fin 154) := {10, 14, 16, 20, 21, 27, 33, 36, 37, 42, 44, 47, 52, 62, 67, 72, 78, 87}
theorem cut721 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support721, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 877, OmissionResidual.support 514, OmissionResidual.support 893] ![OmissionResidual.demand 877, OmissionResidual.demand 514, OmissionResidual.demand 893] ![1, 1, 1]
    support721 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 877) (Fin.cases (hrows 514) (Fin.cases (hrows 893) (fun i => Fin.elim0 i))))
def support722 : Finset (Fin 154) := {8, 10, 12, 14, 16, 20, 21, 27, 33, 35, 37, 42, 43, 44, 46, 52, 53, 55, 57, 59, 62, 64, 66, 70, 74, 85}
theorem cut722 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support722, holes i := by
  apply rounded_cover_cut ![support254, support467, OmissionResidual.support 514] ![3, 3, OmissionResidual.demand 514] ![1, 1, 1]
    support722 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut254 holes hbool hrows) (Fin.cases (cut467 holes hbool hrows) (Fin.cases (hrows 514) (fun i => Fin.elim0 i))))
def support723 : Finset (Fin 154) := {10, 14, 16, 20, 21, 27, 33, 36, 37, 42, 44, 47, 52, 55, 60, 62, 66, 75}
theorem cut723 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support723, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 875, OmissionResidual.support 514, OmissionResidual.support 889] ![OmissionResidual.demand 875, OmissionResidual.demand 514, OmissionResidual.demand 889] ![1, 1, 1]
    support723 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 875) (Fin.cases (hrows 514) (Fin.cases (hrows 889) (fun i => Fin.elim0 i))))
def support724 : Finset (Fin 154) := {90, 99, 107, 108, 111, 115, 122, 123, 126, 129, 130, 135, 138, 139, 146, 147, 149}
theorem cut724 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support724, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1114, OmissionResidual.support 1111, OmissionResidual.support 1140] ![OmissionResidual.demand 1114, OmissionResidual.demand 1111, OmissionResidual.demand 1140] ![1, 1, 1]
    support724 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1114) (Fin.cases (hrows 1111) (Fin.cases (hrows 1140) (fun i => Fin.elim0 i))))
def support725 : Finset (Fin 154) := {83, 93, 94, 97, 99, 102, 103, 106, 107, 108, 112, 116, 118, 120, 122, 124, 129, 134, 135, 138, 140, 146}
theorem cut725 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support725, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1127, support74, support48] ![OmissionResidual.demand 1127, 2, 2] ![1, 1, 1]
    support725 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1127) (Fin.cases (cut74 holes hbool hrows) (Fin.cases (cut48 holes hbool hrows) (fun i => Fin.elim0 i))))
#print axioms cut725
def support726 : Finset (Fin 154) := {83, 93, 94, 97, 99, 102, 103, 106, 107, 108, 112, 116, 118, 120, 122, 124, 129, 134, 135, 138, 140, 144, 146}
theorem cut726 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support726, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1127, support74, support106] ![OmissionResidual.demand 1127, 2, 2] ![1, 1, 1]
    support726 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1127) (Fin.cases (cut74 holes hbool hrows) (Fin.cases (cut106 holes hbool hrows) (fun i => Fin.elim0 i))))
def support727 : Finset (Fin 154) := {42, 56, 62, 68, 72, 82, 83, 87, 93, 94, 97, 99, 100, 102, 103, 106, 108, 112, 116, 120, 123, 124, 129, 135, 140}
theorem cut727 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support727, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 717, support85, support74] ![OmissionResidual.demand 717, 2, 2] ![1, 1, 1]
    support727 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 717) (Fin.cases (cut85 holes hbool hrows) (Fin.cases (cut74 holes hbool hrows) (fun i => Fin.elim0 i))))
def support728 : Finset (Fin 154) := {42, 56, 62, 68, 72, 82, 83, 87, 93, 94, 97, 99, 100, 102, 103, 106, 108, 112, 116, 120, 123, 124, 129, 135, 140, 144}
theorem cut728 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support728, holes i := by
  apply rounded_cover_cut ![support167, OmissionResidual.support 717, support74] ![2, OmissionResidual.demand 717, 2] ![1, 1, 1]
    support728 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut167 holes hbool hrows) (Fin.cases (hrows 717) (Fin.cases (cut74 holes hbool hrows) (fun i => Fin.elim0 i))))
def support729 : Finset (Fin 154) := {42, 56, 62, 68, 72, 82, 83, 87, 93, 94, 97, 99, 100, 102, 103, 106, 108, 112, 116, 120, 124, 129, 130, 134, 135, 144}
theorem cut729 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support729, holes i := by
  apply rounded_cover_cut ![support183, OmissionResidual.support 717, support106] ![2, OmissionResidual.demand 717, 2] ![1, 1, 1]
    support729 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut183 holes hbool hrows) (Fin.cases (hrows 717) (Fin.cases (cut106 holes hbool hrows) (fun i => Fin.elim0 i))))
def support730 : Finset (Fin 154) := {6, 11, 14, 20, 21, 27, 33, 36, 37, 42, 44, 47, 52, 62, 67, 72, 78, 87}
theorem cut730 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support730, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 877, OmissionResidual.support 491, OmissionResidual.support 893] ![OmissionResidual.demand 877, OmissionResidual.demand 491, OmissionResidual.demand 893] ![1, 1, 1]
    support730 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 877) (Fin.cases (hrows 491) (Fin.cases (hrows 893) (fun i => Fin.elim0 i))))
def support731 : Finset (Fin 154) := {6, 8, 11, 12, 14, 20, 21, 27, 33, 35, 37, 42, 43, 44, 46, 52, 53, 55, 57, 59, 62, 64, 66, 70, 74, 85}
theorem cut731 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support731, holes i := by
  apply rounded_cover_cut ![support254, support467, OmissionResidual.support 491] ![3, 3, OmissionResidual.demand 491] ![1, 1, 1]
    support731 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut254 holes hbool hrows) (Fin.cases (cut467 holes hbool hrows) (Fin.cases (hrows 491) (fun i => Fin.elim0 i))))
def support732 : Finset (Fin 154) := {6, 11, 14, 20, 21, 27, 33, 36, 37, 42, 44, 47, 52, 55, 60, 62, 66, 75}
theorem cut732 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support732, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 875, OmissionResidual.support 491, OmissionResidual.support 889] ![OmissionResidual.demand 875, OmissionResidual.demand 491, OmissionResidual.demand 889] ![1, 1, 1]
    support732 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 875) (Fin.cases (hrows 491) (Fin.cases (hrows 889) (fun i => Fin.elim0 i))))
def support733 : Finset (Fin 154) := {38, 42, 47, 48, 51, 56, 57, 58, 61, 62, 63, 68, 69, 72, 73, 80, 82, 83, 84, 87, 93, 94, 99, 102, 103, 106, 112, 116, 120, 124, 130, 144}
theorem cut733 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support733, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 341, support557, support375] ![OmissionResidual.demand 341, 3, 3] ![1, 1, 1]
    support733 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 341) (Fin.cases (cut557 holes hbool hrows) (Fin.cases (cut375 holes hbool hrows) (fun i => Fin.elim0 i))))
def support734 : Finset (Fin 154) := {21, 27, 31, 36, 39, 41, 44, 49, 58, 61, 67, 71, 83, 88, 97}
theorem cut734 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support734, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 580, OmissionResidual.support 895, OmissionResidual.support 917] ![OmissionResidual.demand 580, OmissionResidual.demand 895, OmissionResidual.demand 917] ![1, 1, 1]
    support734 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 580) (Fin.cases (hrows 895) (Fin.cases (hrows 917) (fun i => Fin.elim0 i))))
def support735 : Finset (Fin 154) := {42, 56, 62, 68, 72, 82, 83, 87, 93, 94, 97, 99, 100, 102, 103, 106, 108, 112, 116, 120, 124, 129, 130, 134, 135, 140}
theorem cut735 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support735, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 717, support111, support48] ![OmissionResidual.demand 717, 2, 2] ![1, 1, 1]
    support735 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 717) (Fin.cases (cut111 holes hbool hrows) (Fin.cases (cut48 holes hbool hrows) (fun i => Fin.elim0 i))))
def support736 : Finset (Fin 154) := {42, 56, 62, 68, 72, 82, 83, 87, 93, 94, 97, 99, 100, 102, 103, 106, 108, 112, 116, 120, 124, 129, 130, 134, 135, 140, 144}
theorem cut736 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support736, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 717, support111, support106] ![OmissionResidual.demand 717, 2, 2] ![1, 1, 1]
    support736 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 717) (Fin.cases (cut111 holes hbool hrows) (Fin.cases (cut106 holes hbool hrows) (fun i => Fin.elim0 i))))
def support737 : Finset (Fin 154) := {42, 56, 62, 63, 68, 72, 77, 78, 82, 83, 89, 90, 93, 94, 103, 123, 124, 130}
theorem cut737 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support737, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 418, OmissionResidual.support 343, OmissionResidual.support 798] ![OmissionResidual.demand 418, OmissionResidual.demand 343, OmissionResidual.demand 798] ![1, 1, 1]
    support737 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 418) (Fin.cases (hrows 343) (Fin.cases (hrows 798) (fun i => Fin.elim0 i))))
def support738 : Finset (Fin 154) := {13, 18, 21, 27, 35, 36, 44, 53, 55, 58, 65, 69, 71, 76, 81, 86, 95}
theorem cut738 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support738, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 570, OmissionResidual.support 891, OmissionResidual.support 874] ![OmissionResidual.demand 570, OmissionResidual.demand 891, OmissionResidual.demand 874] ![1, 1, 1]
    support738 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 570) (Fin.cases (hrows 891) (Fin.cases (hrows 874) (fun i => Fin.elim0 i))))
def support739 : Finset (Fin 154) := {90, 99, 107, 108, 111, 115, 122, 123, 126, 129, 130, 134, 135, 138, 139, 140, 147, 148, 149}
theorem cut739 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support739, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1142, OmissionResidual.support 1114, OmissionResidual.support 1111] ![OmissionResidual.demand 1142, OmissionResidual.demand 1114, OmissionResidual.demand 1111] ![1, 1, 1]
    support739 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1142) (Fin.cases (hrows 1114) (Fin.cases (hrows 1111) (fun i => Fin.elim0 i))))
def support740 : Finset (Fin 154) := {63, 72, 73, 78, 82, 83, 88, 90, 93, 100, 102, 103, 117, 120, 122, 130, 140}
theorem cut740 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support740, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 965, OmissionResidual.support 970, OmissionResidual.support 800] ![OmissionResidual.demand 965, OmissionResidual.demand 970, OmissionResidual.demand 800] ![1, 1, 1]
    support740 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 965) (Fin.cases (hrows 970) (Fin.cases (hrows 800) (fun i => Fin.elim0 i))))
def support741 : Finset (Fin 154) := {63, 72, 73, 78, 82, 83, 88, 90, 93, 100, 102, 103, 109, 120, 122, 123, 134}
theorem cut741 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support741, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 963, OmissionResidual.support 968, OmissionResidual.support 800] ![OmissionResidual.demand 963, OmissionResidual.demand 968, OmissionResidual.demand 800] ![1, 1, 1]
    support741 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 963) (Fin.cases (hrows 968) (Fin.cases (hrows 800) (fun i => Fin.elim0 i))))
def support742 : Finset (Fin 154) := {63, 72, 73, 78, 82, 83, 88, 90, 93, 100, 102, 103, 120, 122, 123, 134}
theorem cut742 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support742, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 418, OmissionResidual.support 440, OmissionResidual.support 800] ![OmissionResidual.demand 418, OmissionResidual.demand 440, OmissionResidual.demand 800] ![1, 1, 1]
    support742 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 418) (Fin.cases (hrows 440) (Fin.cases (hrows 800) (fun i => Fin.elim0 i))))
def support743 : Finset (Fin 154) := {51, 60, 64, 66, 70, 74, 78, 88, 90, 92, 100, 102, 104, 113, 118, 122, 126, 136}
theorem cut743 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support743, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1043, OmissionResidual.support 952, OmissionResidual.support 948] ![OmissionResidual.demand 1043, OmissionResidual.demand 952, OmissionResidual.demand 948] ![1, 1, 1]
    support743 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1043) (Fin.cases (hrows 952) (Fin.cases (hrows 948) (fun i => Fin.elim0 i))))
def support744 : Finset (Fin 154) := {8, 12, 13, 14, 18, 20, 33, 35, 44, 46, 55, 57, 59, 66, 70, 74, 85}
theorem cut744 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support744, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 51, OmissionResidual.support 872, OmissionResidual.support 876] ![OmissionResidual.demand 51, OmissionResidual.demand 872, OmissionResidual.demand 876] ![1, 1, 1]
    support744 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 51) (Fin.cases (hrows 872) (Fin.cases (hrows 876) (fun i => Fin.elim0 i))))
def support745 : Finset (Fin 154) := {4, 7, 13, 14, 18, 20, 33, 35, 44, 46, 55, 57, 59, 66, 70, 74, 85}
theorem cut745 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support745, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 25, OmissionResidual.support 872, OmissionResidual.support 876] ![OmissionResidual.demand 25, OmissionResidual.demand 872, OmissionResidual.demand 876] ![1, 1, 1]
    support745 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 25) (Fin.cases (hrows 872) (Fin.cases (hrows 876) (fun i => Fin.elim0 i))))
def support746 : Finset (Fin 154) := {42, 56, 62, 63, 68, 72, 73, 78, 82, 83, 88, 90, 93, 100, 102, 103, 108, 117, 120, 130, 140}
theorem cut746 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support746, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 965, OmissionResidual.support 970, OmissionResidual.support 717] ![OmissionResidual.demand 965, OmissionResidual.demand 970, OmissionResidual.demand 717] ![1, 1, 1]
    support746 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 965) (Fin.cases (hrows 970) (Fin.cases (hrows 717) (fun i => Fin.elim0 i))))
def support747 : Finset (Fin 154) := {42, 56, 62, 63, 68, 72, 73, 78, 82, 83, 88, 90, 93, 100, 102, 103, 108, 109, 120, 123, 134}
theorem cut747 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support747, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 963, OmissionResidual.support 717, OmissionResidual.support 968] ![OmissionResidual.demand 963, OmissionResidual.demand 717, OmissionResidual.demand 968] ![1, 1, 1]
    support747 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 963) (Fin.cases (hrows 717) (Fin.cases (hrows 968) (fun i => Fin.elim0 i))))
def support748 : Finset (Fin 154) := {42, 56, 62, 63, 68, 72, 73, 78, 82, 83, 88, 90, 93, 100, 102, 103, 108, 120, 123, 134}
theorem cut748 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support748, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 418, OmissionResidual.support 717, OmissionResidual.support 440] ![OmissionResidual.demand 418, OmissionResidual.demand 717, OmissionResidual.demand 440] ![1, 1, 1]
    support748 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 418) (Fin.cases (hrows 717) (Fin.cases (hrows 440) (fun i => Fin.elim0 i))))
def support749 : Finset (Fin 154) := {7, 18, 35, 36, 43, 46, 53, 59, 64, 65, 69, 74, 75, 81, 86, 95}
theorem cut749 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support749, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 570, OmissionResidual.support 494, OmissionResidual.support 672] ![OmissionResidual.demand 570, OmissionResidual.demand 494, OmissionResidual.demand 672] ![1, 1, 1]
    support749 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 570) (Fin.cases (hrows 494) (Fin.cases (hrows 672) (fun i => Fin.elim0 i))))
def support750 : Finset (Fin 154) := {12, 18, 35, 36, 43, 46, 53, 59, 64, 65, 69, 74, 75, 81, 86, 95}
theorem cut750 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support750, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 570, OmissionResidual.support 526, OmissionResidual.support 672] ![OmissionResidual.demand 570, OmissionResidual.demand 526, OmissionResidual.demand 672] ![1, 1, 1]
    support750 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 570) (Fin.cases (hrows 526) (Fin.cases (hrows 672) (fun i => Fin.elim0 i))))
#print axioms cut750
def support751 : Finset (Fin 154) := {28, 36, 46, 64, 74, 75, 78, 80, 86, 88, 92, 102, 104, 113, 118, 122, 126, 136}
theorem cut751 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support751, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 673, OmissionResidual.support 1043, OmissionResidual.support 230] ![OmissionResidual.demand 673, OmissionResidual.demand 1043, OmissionResidual.demand 230] ![1, 1, 1]
    support751 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 673) (Fin.cases (hrows 1043) (Fin.cases (hrows 230) (fun i => Fin.elim0 i))))
def support752 : Finset (Fin 154) := {4, 7, 9, 15, 18, 24, 26, 27, 32, 33, 36, 39, 44, 53, 58, 61, 71}
theorem cut752 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support752, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 507, OmissionResidual.support 550, OmissionResidual.support 23] ![OmissionResidual.demand 507, OmissionResidual.demand 550, OmissionResidual.demand 23] ![1, 1, 1]
    support752 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 507) (Fin.cases (hrows 550) (Fin.cases (hrows 23) (fun i => Fin.elim0 i))))
def support753 : Finset (Fin 154) := {8, 9, 12, 15, 18, 24, 26, 27, 32, 33, 36, 39, 44, 53, 58, 61, 71}
theorem cut753 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support753, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 507, OmissionResidual.support 550, OmissionResidual.support 49] ![OmissionResidual.demand 507, OmissionResidual.demand 550, OmissionResidual.demand 49] ![1, 1, 1]
    support753 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 507) (Fin.cases (hrows 550) (Fin.cases (hrows 49) (fun i => Fin.elim0 i))))
def support754 : Finset (Fin 154) := {4, 7, 13, 18, 21, 26, 27, 31, 33, 36, 39, 41, 44, 53, 58, 61, 71}
theorem cut754 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support754, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 530, OmissionResidual.support 580, OmissionResidual.support 23] ![OmissionResidual.demand 530, OmissionResidual.demand 580, OmissionResidual.demand 23] ![1, 1, 1]
    support754 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 530) (Fin.cases (hrows 580) (Fin.cases (hrows 23) (fun i => Fin.elim0 i))))
def support755 : Finset (Fin 154) := {8, 12, 13, 18, 21, 26, 27, 31, 33, 36, 39, 41, 44, 53, 58, 61, 71}
theorem cut755 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support755, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 530, OmissionResidual.support 580, OmissionResidual.support 49] ![OmissionResidual.demand 530, OmissionResidual.demand 580, OmissionResidual.demand 49] ![1, 1, 1]
    support755 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 530) (Fin.cases (hrows 580) (Fin.cases (hrows 49) (fun i => Fin.elim0 i))))
def support756 : Finset (Fin 154) := {5, 8, 12, 13, 16, 18, 32, 33, 35, 37, 41, 44, 50, 55, 57, 66, 70, 85}
theorem cut756 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support756, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 484, OmissionResidual.support 862, OmissionResidual.support 872] ![OmissionResidual.demand 484, OmissionResidual.demand 862, OmissionResidual.demand 872] ![1, 1, 1]
    support756 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 484) (Fin.cases (hrows 862) (Fin.cases (hrows 872) (fun i => Fin.elim0 i))))
def support757 : Finset (Fin 154) := {99, 107, 115, 118, 122, 123, 124, 129, 130, 135, 138, 140, 143, 144, 146, 147, 152}
theorem cut757 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support757, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1127, OmissionResidual.support 1126, OmissionResidual.support 1159] ![OmissionResidual.demand 1127, OmissionResidual.demand 1126, OmissionResidual.demand 1159] ![1, 1, 1]
    support757 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1127) (Fin.cases (hrows 1126) (Fin.cases (hrows 1159) (fun i => Fin.elim0 i))))
def support758 : Finset (Fin 154) := {99, 107, 115, 118, 122, 123, 124, 129, 130, 135, 138, 140, 143, 144, 146, 147, 153}
theorem cut758 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support758, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1127, OmissionResidual.support 1126, OmissionResidual.support 1160] ![OmissionResidual.demand 1127, OmissionResidual.demand 1126, OmissionResidual.demand 1160] ![1, 1, 1]
    support758 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1127) (Fin.cases (hrows 1126) (Fin.cases (hrows 1160) (fun i => Fin.elim0 i))))
def support759 : Finset (Fin 154) := {3, 8, 11, 12, 13, 18, 32, 33, 35, 37, 41, 44, 50, 55, 57, 66, 70, 85}
theorem cut759 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support759, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 862, OmissionResidual.support 475, OmissionResidual.support 872] ![OmissionResidual.demand 862, OmissionResidual.demand 475, OmissionResidual.demand 872] ![1, 1, 1]
    support759 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 862) (Fin.cases (hrows 475) (Fin.cases (hrows 872) (fun i => Fin.elim0 i))))
def support760 : Finset (Fin 154) := {8, 12, 18, 33, 35, 36, 44, 46, 53, 59, 64, 65, 69, 74, 75, 81, 86, 95}
theorem cut760 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support760, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 51, OmissionResidual.support 570, OmissionResidual.support 672] ![OmissionResidual.demand 51, OmissionResidual.demand 570, OmissionResidual.demand 672] ![1, 1, 1]
    support760 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 51) (Fin.cases (hrows 570) (Fin.cases (hrows 672) (fun i => Fin.elim0 i))))
def support761 : Finset (Fin 154) := {4, 7, 18, 33, 35, 36, 44, 46, 53, 59, 64, 65, 69, 74, 75, 81, 86, 95}
theorem cut761 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support761, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 570, OmissionResidual.support 25, OmissionResidual.support 672] ![OmissionResidual.demand 570, OmissionResidual.demand 25, OmissionResidual.demand 672] ![1, 1, 1]
    support761 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 570) (Fin.cases (hrows 25) (Fin.cases (hrows 672) (fun i => Fin.elim0 i))))
def support762 : Finset (Fin 154) := {4, 7, 12, 26, 33, 35, 36, 43, 44, 46, 49, 53, 54, 59, 64, 74}
theorem cut762 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support762, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 851, OmissionResidual.support 852, OmissionResidual.support 526] ![OmissionResidual.demand 851, OmissionResidual.demand 852, OmissionResidual.demand 526] ![1, 1, 1]
    support762 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 851) (Fin.cases (hrows 852) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support763 : Finset (Fin 154) := {7, 8, 12, 26, 33, 35, 36, 43, 44, 46, 49, 53, 54, 59, 64, 74}
theorem cut763 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support763, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 859, OmissionResidual.support 860, OmissionResidual.support 494] ![OmissionResidual.demand 859, OmissionResidual.demand 860, OmissionResidual.demand 494] ![1, 1, 1]
    support763 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 859) (Fin.cases (hrows 860) (Fin.cases (hrows 494) (fun i => Fin.elim0 i))))
def support764 : Finset (Fin 154) := {4, 7, 8, 12, 26, 33, 35, 36, 43, 44, 46, 49, 53, 54, 59, 64, 74}
theorem cut764 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support764, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 851, OmissionResidual.support 860, OmissionResidual.support 494] ![OmissionResidual.demand 851, OmissionResidual.demand 860, OmissionResidual.demand 494] ![1, 1, 1]
    support764 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 851) (Fin.cases (hrows 860) (Fin.cases (hrows 494) (fun i => Fin.elim0 i))))
def support765 : Finset (Fin 154) := {4, 7, 12, 26, 33, 35, 36, 43, 44, 46, 49, 53, 59, 64, 74}
theorem cut765 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support765, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 24, OmissionResidual.support 25, OmissionResidual.support 526] ![OmissionResidual.demand 24, OmissionResidual.demand 25, OmissionResidual.demand 526] ![1, 1, 1]
    support765 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 24) (Fin.cases (hrows 25) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support766 : Finset (Fin 154) := {7, 8, 12, 26, 33, 35, 36, 43, 44, 46, 49, 53, 59, 64, 74}
theorem cut766 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support766, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 51, OmissionResidual.support 50, OmissionResidual.support 494] ![OmissionResidual.demand 51, OmissionResidual.demand 50, OmissionResidual.demand 494] ![1, 1, 1]
    support766 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 51) (Fin.cases (hrows 50) (Fin.cases (hrows 494) (fun i => Fin.elim0 i))))
def support767 : Finset (Fin 154) := {4, 7, 8, 12, 26, 33, 35, 36, 43, 44, 46, 49, 53, 59, 64, 74}
theorem cut767 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support767, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 51, OmissionResidual.support 24, OmissionResidual.support 526] ![OmissionResidual.demand 51, OmissionResidual.demand 24, OmissionResidual.demand 526] ![1, 1, 1]
    support767 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 51) (Fin.cases (hrows 24) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support768 : Finset (Fin 154) := {28, 36, 40, 46, 48, 58, 61, 63, 69, 73, 78, 80, 84, 88, 93, 102, 105, 120}
theorem cut768 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support768, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 625, OmissionResidual.support 229, OmissionResidual.support 731] ![OmissionResidual.demand 625, OmissionResidual.demand 229, OmissionResidual.demand 731] ![1, 1, 1]
    support768 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 625) (Fin.cases (hrows 229) (Fin.cases (hrows 731) (fun i => Fin.elim0 i))))
def support769 : Finset (Fin 154) := {8, 10, 12, 14, 16, 20, 21, 22, 27, 32, 33, 35, 36, 37, 42, 43, 44, 46, 47, 52, 53, 55, 57, 58, 59, 60, 62, 64, 65, 66, 70, 74, 75, 84, 85, 94}
theorem cut769 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support769, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 588, support722, support305] ![OmissionResidual.demand 588, 4, 4] ![1, 1, 1]
    support769 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 588) (Fin.cases (cut722 holes hbool hrows) (Fin.cases (cut305 holes hbool hrows) (fun i => Fin.elim0 i))))
def support770 : Finset (Fin 154) := {8, 10, 12, 13, 14, 16, 18, 20, 21, 27, 33, 35, 37, 42, 44, 46, 52, 55, 57, 59, 62, 66, 70, 74, 85}
theorem cut770 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support770, holes i := by
  apply rounded_cover_cut ![support744, support467, OmissionResidual.support 514] ![3, 3, OmissionResidual.demand 514] ![1, 1, 1]
    support770 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut744 holes hbool hrows) (Fin.cases (cut467 holes hbool hrows) (Fin.cases (hrows 514) (fun i => Fin.elim0 i))))
def support771 : Finset (Fin 154) := {5, 12, 13, 15, 16, 18, 24, 26, 27, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut771 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support771, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 530, OmissionResidual.support 550, OmissionResidual.support 482] ![OmissionResidual.demand 530, OmissionResidual.demand 550, OmissionResidual.demand 482] ![1, 1, 1]
    support771 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 530) (Fin.cases (hrows 550) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support772 : Finset (Fin 154) := {5, 9, 12, 16, 18, 21, 24, 26, 27, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut772 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support772, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 507, OmissionResidual.support 580, OmissionResidual.support 482] ![OmissionResidual.demand 507, OmissionResidual.demand 580, OmissionResidual.demand 482] ![1, 1, 1]
    support772 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 507) (Fin.cases (hrows 580) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support773 : Finset (Fin 154) := {2, 7, 13, 15, 16, 18, 24, 26, 27, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut773 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support773, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 530, OmissionResidual.support 550, OmissionResidual.support 471] ![OmissionResidual.demand 530, OmissionResidual.demand 550, OmissionResidual.demand 471] ![1, 1, 1]
    support773 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 530) (Fin.cases (hrows 550) (Fin.cases (hrows 471) (fun i => Fin.elim0 i))))
def support774 : Finset (Fin 154) := {2, 7, 9, 16, 18, 21, 24, 26, 27, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut774 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support774, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 507, OmissionResidual.support 580, OmissionResidual.support 471] ![OmissionResidual.demand 507, OmissionResidual.demand 580, OmissionResidual.demand 471] ![1, 1, 1]
    support774 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 507) (Fin.cases (hrows 580) (Fin.cases (hrows 471) (fun i => Fin.elim0 i))))
def support775 : Finset (Fin 154) := {7, 13, 18, 21, 27, 35, 36, 43, 44, 46, 53, 55, 58, 59, 64, 65, 69, 71, 74, 75, 76, 81, 86, 95}
theorem cut775 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support775, holes i := by
  apply rounded_cover_cut ![support749, OmissionResidual.support 891, support591] ![2, OmissionResidual.demand 891, 3] ![1, 1, 1]
    support775 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut749 holes hbool hrows) (Fin.cases (hrows 891) (Fin.cases (cut591 holes hbool hrows) (fun i => Fin.elim0 i))))
#print axioms cut775
def support776 : Finset (Fin 154) := {31, 39, 42, 44, 49, 56, 60, 62, 68, 71, 72, 79, 83, 90, 99, 100, 108}
theorem cut776 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support776, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 717, OmissionResidual.support 919, OmissionResidual.support 921] ![OmissionResidual.demand 717, OmissionResidual.demand 919, OmissionResidual.demand 921] ![1, 1, 1]
    support776 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 717) (Fin.cases (hrows 919) (Fin.cases (hrows 921) (fun i => Fin.elim0 i))))
def support777 : Finset (Fin 154) := {5, 8, 10, 12, 13, 16, 18, 20, 27, 32, 33, 35, 37, 39, 41, 44, 50, 53, 55, 57, 66, 70, 85}
theorem cut777 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support777, holes i := by
  apply rounded_cover_cut ![support756, support714, OmissionResidual.support 512] ![3, 3, OmissionResidual.demand 512] ![1, 1, 1]
    support777 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut756 holes hbool hrows) (Fin.cases (cut714 holes hbool hrows) (Fin.cases (hrows 512) (fun i => Fin.elim0 i))))
def support778 : Finset (Fin 154) := {10, 14, 15, 16, 20, 21, 24, 27, 31, 32, 33, 36, 37, 39, 42, 44, 47, 49, 51, 52, 60, 62, 67, 72, 78, 87}
theorem cut778 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support778, holes i := by
  apply rounded_cover_cut ![support322, support721, OmissionResidual.support 915] ![2, 3, OmissionResidual.demand 915] ![1, 1, 1]
    support778 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut322 holes hbool hrows) (Fin.cases (cut721 holes hbool hrows) (Fin.cases (hrows 915) (fun i => Fin.elim0 i))))
def support779 : Finset (Fin 154) := {63, 72, 73, 78, 82, 83, 88, 90, 93, 99, 100, 102, 103, 107, 112, 117, 118, 120, 122, 123, 129, 130, 135, 138, 140, 146}
theorem cut779 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support779, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1127, support559, support740] ![OmissionResidual.demand 1127, 3, 3] ![1, 1, 1]
    support779 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1127) (Fin.cases (cut559 holes hbool hrows) (Fin.cases (cut740 holes hbool hrows) (fun i => Fin.elim0 i))))
def support780 : Finset (Fin 154) := {63, 72, 73, 78, 82, 83, 88, 90, 93, 99, 100, 102, 103, 107, 112, 117, 118, 120, 122, 123, 129, 130, 135, 140, 143, 149}
theorem cut780 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support780, holes i := by
  apply rounded_cover_cut ![support559, OmissionResidual.support 1128, support740] ![3, OmissionResidual.demand 1128, 3] ![1, 1, 1]
    support780 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut559 holes hbool hrows) (Fin.cases (hrows 1128) (Fin.cases (cut740 holes hbool hrows) (fun i => Fin.elim0 i))))
def support781 : Finset (Fin 154) := {0, 7, 11, 12, 16, 18, 20, 23, 30, 35, 36, 43, 46, 53, 59, 64, 65, 69, 74, 75, 81, 86, 95}
theorem cut781 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support781, holes i := by
  apply rounded_cover_cut ![support750, support749, OmissionResidual.support 466] ![2, 2, OmissionResidual.demand 466] ![1, 1, 1]
    support781 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut750 holes hbool hrows) (Fin.cases (cut749 holes hbool hrows) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support782 : Finset (Fin 154) := {1, 7, 11, 12, 16, 18, 20, 23, 30, 35, 36, 43, 46, 53, 59, 64, 65, 69, 74, 75, 81, 86, 95}
theorem cut782 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support782, holes i := by
  apply rounded_cover_cut ![support750, support749, OmissionResidual.support 468] ![2, 2, OmissionResidual.demand 468] ![1, 1, 1]
    support782 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut750 holes hbool hrows) (Fin.cases (cut749 holes hbool hrows) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support783 : Finset (Fin 154) := {0, 4, 7, 8, 11, 12, 16, 20, 23, 26, 30, 33, 35, 36, 44, 46, 59, 64, 74, 75, 80, 86, 92, 104}
theorem cut783 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support783, holes i := by
  apply rounded_cover_cut ![support710, support711, OmissionResidual.support 466] ![2, 2, OmissionResidual.demand 466] ![1, 1, 1]
    support783 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut710 holes hbool hrows) (Fin.cases (cut711 holes hbool hrows) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support784 : Finset (Fin 154) := {1, 4, 7, 8, 11, 12, 16, 20, 23, 26, 30, 33, 35, 36, 44, 46, 59, 64, 74, 75, 80, 86, 92, 104}
theorem cut784 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support784, holes i := by
  apply rounded_cover_cut ![support710, support711, OmissionResidual.support 468] ![2, 2, OmissionResidual.demand 468] ![1, 1, 1]
    support784 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut710 holes hbool hrows) (Fin.cases (cut711 holes hbool hrows) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support785 : Finset (Fin 154) := {8, 10, 12, 14, 16, 20, 21, 27, 29, 33, 35, 36, 37, 41, 42, 43, 44, 46, 47, 52, 53, 55, 57, 58, 59, 60, 62, 64, 65, 66, 70, 74, 75, 84, 85, 94}
theorem cut785 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support785, holes i := by
  apply rounded_cover_cut ![support722, OmissionResidual.support 631, support305] ![4, OmissionResidual.demand 631, 4] ![1, 1, 1]
    support785 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (cut722 holes hbool hrows) (Fin.cases (hrows 631) (Fin.cases (cut305 holes hbool hrows) (fun i => Fin.elim0 i))))
def support786 : Finset (Fin 154) := {28, 36, 40, 46, 48, 51, 58, 60, 61, 63, 69, 70, 73, 78, 80, 81, 84, 88, 93, 102, 105, 120}
theorem cut786 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support786, holes i := by
  apply rounded_cover_cut ![support768, support282, OmissionResidual.support 375] ![2, 2, OmissionResidual.demand 375] ![1, 1, 1]
    support786 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut768 holes hbool hrows) (Fin.cases (cut282 holes hbool hrows) (Fin.cases (hrows 375) (fun i => Fin.elim0 i))))
def support787 : Finset (Fin 154) := {28, 36, 40, 46, 48, 51, 58, 60, 61, 63, 69, 70, 73, 78, 80, 81, 84, 88, 93, 102, 105, 112, 120}
theorem cut787 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support787, holes i := by
  apply rounded_cover_cut ![support768, support123, OmissionResidual.support 375] ![2, 2, OmissionResidual.demand 375] ![1, 1, 1]
    support787 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut768 holes hbool hrows) (Fin.cases (cut123 holes hbool hrows) (Fin.cases (hrows 375) (fun i => Fin.elim0 i))))
def support788 : Finset (Fin 154) := {1, 5, 7, 11, 12, 13, 15, 16, 18, 20, 23, 24, 26, 27, 30, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut788 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support788, holes i := by
  apply rounded_cover_cut ![support771, support400, OmissionResidual.support 468] ![2, 2, OmissionResidual.demand 468] ![1, 1, 1]
    support788 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut771 holes hbool hrows) (Fin.cases (cut400 holes hbool hrows) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support789 : Finset (Fin 154) := {1, 5, 7, 9, 11, 12, 16, 18, 20, 21, 23, 24, 26, 27, 30, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut789 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support789, holes i := by
  apply rounded_cover_cut ![support772, support399, OmissionResidual.support 468] ![2, 2, OmissionResidual.demand 468] ![1, 1, 1]
    support789 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut772 holes hbool hrows) (Fin.cases (cut399 holes hbool hrows) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support790 : Finset (Fin 154) := {0, 1, 5, 7, 11, 12, 13, 15, 16, 18, 20, 23, 24, 26, 27, 30, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut790 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support790, holes i := by
  apply rounded_cover_cut ![support771, support400, OmissionResidual.support 466] ![2, 2, OmissionResidual.demand 466] ![1, 1, 1]
    support790 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut771 holes hbool hrows) (Fin.cases (cut400 holes hbool hrows) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support791 : Finset (Fin 154) := {0, 1, 5, 7, 9, 11, 12, 16, 18, 20, 21, 23, 24, 26, 27, 30, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut791 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support791, holes i := by
  apply rounded_cover_cut ![support772, support399, OmissionResidual.support 466] ![2, 2, OmissionResidual.demand 466] ![1, 1, 1]
    support791 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut772 holes hbool hrows) (Fin.cases (cut399 holes hbool hrows) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support792 : Finset (Fin 154) := {1, 5, 7, 9, 11, 12, 13, 15, 16, 18, 20, 21, 23, 24, 26, 27, 30, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut792 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support792, holes i := by
  apply rounded_cover_cut ![support771, support399, OmissionResidual.support 468] ![2, 2, OmissionResidual.demand 468] ![1, 1, 1]
    support792 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut771 holes hbool hrows) (Fin.cases (cut399 holes hbool hrows) (Fin.cases (hrows 468) (fun i => Fin.elim0 i))))
def support793 : Finset (Fin 154) := {0, 1, 5, 7, 9, 11, 12, 13, 15, 16, 18, 20, 21, 23, 24, 26, 27, 30, 31, 32, 36, 39, 41, 58, 61, 71}
theorem cut793 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support793, holes i := by
  apply rounded_cover_cut ![support771, support399, OmissionResidual.support 466] ![2, 2, OmissionResidual.demand 466] ![1, 1, 1]
    support793 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut771 holes hbool hrows) (Fin.cases (cut399 holes hbool hrows) (Fin.cases (hrows 466) (fun i => Fin.elim0 i))))
def support794 : Finset (Fin 154) := {10, 14, 16, 20, 23, 30, 32, 33, 36, 47, 49, 51, 60, 67, 72, 78, 87}
theorem cut794 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support794, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 877, OmissionResidual.support 899, OmissionResidual.support 513] ![OmissionResidual.demand 877, OmissionResidual.demand 899, OmissionResidual.demand 513] ![1, 1, 1]
    support794 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 877) (Fin.cases (hrows 899) (Fin.cases (hrows 513) (fun i => Fin.elim0 i))))
def support795 : Finset (Fin 154) := {14, 20, 23, 30, 33, 36, 41, 47, 49, 51, 60, 67, 72, 78, 87}
theorem cut795 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support795, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 877, OmissionResidual.support 899, OmissionResidual.support 539] ![OmissionResidual.demand 877, OmissionResidual.demand 899, OmissionResidual.demand 539] ![1, 1, 1]
    support795 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 877) (Fin.cases (hrows 899) (Fin.cases (hrows 539) (fun i => Fin.elim0 i))))
def support796 : Finset (Fin 154) := {38, 47, 57, 61, 66, 71, 76, 80, 81, 92, 98, 104, 112, 121}
theorem cut796 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support796, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 407, OmissionResidual.support 289, OmissionResidual.support 297] ![OmissionResidual.demand 407, OmissionResidual.demand 289, OmissionResidual.demand 297] ![1, 1, 1]
    support796 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 407) (Fin.cases (hrows 289) (Fin.cases (hrows 297) (fun i => Fin.elim0 i))))
def support797 : Finset (Fin 154) := {6, 11, 14, 17, 21, 23, 27, 29, 31, 41, 46, 52, 56, 61, 67, 69, 81}
theorem cut797 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support797, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 46, OmissionResidual.support 581, OmissionResidual.support 83] ![OmissionResidual.demand 46, OmissionResidual.demand 581, OmissionResidual.demand 83] ![1, 1, 1]
    support797 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 46) (Fin.cases (hrows 581) (Fin.cases (hrows 83) (fun i => Fin.elim0 i))))
def support798 : Finset (Fin 154) := {10, 11, 14, 17, 21, 23, 25, 27, 29, 31, 41, 46, 52, 56, 61, 67, 69, 81}
theorem cut798 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support798, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 75, OmissionResidual.support 581, OmissionResidual.support 83] ![OmissionResidual.demand 75, OmissionResidual.demand 581, OmissionResidual.demand 83] ![1, 1, 1]
    support798 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 75) (Fin.cases (hrows 581) (Fin.cases (hrows 83) (fun i => Fin.elim0 i))))
def support799 : Finset (Fin 154) := {49, 59, 61, 64, 71, 76, 81, 87, 92, 93, 97, 100, 102, 105, 113, 120, 134}
theorem cut799 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support799, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, OmissionResidual.support 411, OmissionResidual.support 737] ![OmissionResidual.demand 736, OmissionResidual.demand 411, OmissionResidual.demand 737] ![1, 1, 1]
    support799 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (hrows 411) (Fin.cases (hrows 737) (fun i => Fin.elim0 i))))
def support800 : Finset (Fin 154) := {38, 47, 51, 57, 63, 72, 73, 80, 82, 84, 87, 99, 102, 112, 124, 135}
theorem cut800 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support800, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 679, OmissionResidual.support 681, OmissionResidual.support 819] ![OmissionResidual.demand 679, OmissionResidual.demand 681, OmissionResidual.demand 819] ![1, 1, 1]
    support800 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 679) (Fin.cases (hrows 681) (Fin.cases (hrows 819) (fun i => Fin.elim0 i))))
#print axioms cut800
def support801 : Finset (Fin 154) := {10, 14, 16, 21, 23, 25, 27, 29, 31, 41, 46, 52, 56, 61, 67, 69, 81}
theorem cut801 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support801, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 75, OmissionResidual.support 581, OmissionResidual.support 130] ![OmissionResidual.demand 75, OmissionResidual.demand 581, OmissionResidual.demand 130] ![1, 1, 1]
    support801 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 75) (Fin.cases (hrows 581) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))
def support802 : Finset (Fin 154) := {6, 14, 16, 17, 21, 23, 25, 27, 29, 31, 41, 46, 52, 56, 61, 67, 69, 81}
theorem cut802 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support802, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 46, OmissionResidual.support 581, OmissionResidual.support 130] ![OmissionResidual.demand 46, OmissionResidual.demand 581, OmissionResidual.demand 130] ![1, 1, 1]
    support802 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 46) (Fin.cases (hrows 581) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))
def support803 : Finset (Fin 154) := {49, 59, 61, 64, 71, 76, 81, 87, 92, 93, 97, 98, 102, 105, 112, 113, 121}
theorem cut803 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support803, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, OmissionResidual.support 737, OmissionResidual.support 407] ![OmissionResidual.demand 736, OmissionResidual.demand 737, OmissionResidual.demand 407] ![1, 1, 1]
    support803 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (hrows 737) (Fin.cases (hrows 407) (fun i => Fin.elim0 i))))
def support804 : Finset (Fin 154) := {94, 97, 103, 105, 106, 112, 113, 114, 116, 120, 121, 123, 124, 126, 128, 129, 132, 134, 138, 140, 141, 144, 148}
theorem cut804 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support804, holes i := by
  apply rounded_cover_cut ![support301, OmissionResidual.support 843, support336] ![2, OmissionResidual.demand 843, 2] ![1, 1, 1]
    support804 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut301 holes hbool hrows) (Fin.cases (hrows 843) (Fin.cases (cut336 holes hbool hrows) (fun i => Fin.elim0 i))))
def support805 : Finset (Fin 154) := {43, 74, 85, 87, 89, 96, 105, 107, 110, 114, 115, 118, 123, 125, 130, 132, 137, 143, 147}
theorem cut805 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support805, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1006, OmissionResidual.support 1108, OmissionResidual.support 1097] ![OmissionResidual.demand 1006, OmissionResidual.demand 1108, OmissionResidual.demand 1097] ![1, 1, 1]
    support805 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1006) (Fin.cases (hrows 1108) (Fin.cases (hrows 1097) (fun i => Fin.elim0 i))))
def support806 : Finset (Fin 154) := {64, 74, 87, 96, 97, 104, 105, 113, 114, 118, 121, 122, 126, 130, 135, 136, 138, 142, 146}
theorem cut806 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support806, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1043, OmissionResidual.support 1098, OmissionResidual.support 1119] ![OmissionResidual.demand 1043, OmissionResidual.demand 1098, OmissionResidual.demand 1119] ![1, 1, 1]
    support806 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1043) (Fin.cases (hrows 1098) (Fin.cases (hrows 1119) (fun i => Fin.elim0 i))))
def support807 : Finset (Fin 154) := {49, 59, 61, 64, 71, 76, 81, 87, 92, 93, 97, 98, 102, 105, 113, 120, 128}
theorem cut807 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support807, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, OmissionResidual.support 737, OmissionResidual.support 408] ![OmissionResidual.demand 736, OmissionResidual.demand 737, OmissionResidual.demand 408] ![1, 1, 1]
    support807 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (hrows 737) (Fin.cases (hrows 408) (fun i => Fin.elim0 i))))
def support808 : Finset (Fin 154) := {21, 27, 31, 38, 41, 46, 47, 51, 52, 57, 61, 63, 69, 81, 82, 84, 103}
theorem cut808 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support808, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 581, OmissionResidual.support 680, OmissionResidual.support 583] ![OmissionResidual.demand 581, OmissionResidual.demand 680, OmissionResidual.demand 583] ![1, 1, 1]
    support808 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 581) (Fin.cases (hrows 680) (Fin.cases (hrows 583) (fun i => Fin.elim0 i))))
def support809 : Finset (Fin 154) := {25, 42, 43, 56, 62, 64, 68, 72, 75, 82, 83, 87, 90, 94, 99, 102, 112, 124, 135}
theorem cut809 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support809, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 819, OmissionResidual.support 343, OmissionResidual.support 216] ![OmissionResidual.demand 819, OmissionResidual.demand 343, OmissionResidual.demand 216] ![1, 1, 1]
    support809 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 819) (Fin.cases (hrows 343) (Fin.cases (hrows 216) (fun i => Fin.elim0 i))))
def support810 : Finset (Fin 154) := {3, 9, 11, 12, 18, 24, 26, 29, 32, 37, 41, 47, 50, 52, 58, 61, 71, 84, 94}
theorem cut810 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support810, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 507, OmissionResidual.support 631, OmissionResidual.support 475] ![OmissionResidual.demand 507, OmissionResidual.demand 631, OmissionResidual.demand 475] ![1, 1, 1]
    support810 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 507) (Fin.cases (hrows 631) (Fin.cases (hrows 475) (fun i => Fin.elim0 i))))
def support811 : Finset (Fin 154) := {30, 43, 49, 50, 59, 64, 65, 70, 77, 81, 82, 87, 93, 96, 97, 105}
theorem cut811 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support811, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, OmissionResidual.support 639, OmissionResidual.support 740] ![OmissionResidual.demand 736, OmissionResidual.demand 639, OmissionResidual.demand 740] ![1, 1, 1]
    support811 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (hrows 639) (Fin.cases (hrows 740) (fun i => Fin.elim0 i))))
def support812 : Finset (Fin 154) := {21, 27, 31, 41, 46, 49, 52, 59, 61, 64, 69, 73, 81, 87, 93, 97, 105}
theorem cut812 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support812, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, OmissionResidual.support 581, OmissionResidual.support 585] ![OmissionResidual.demand 736, OmissionResidual.demand 581, OmissionResidual.demand 585] ![1, 1, 1]
    support812 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (hrows 581) (Fin.cases (hrows 585) (fun i => Fin.elim0 i))))
def support813 : Finset (Fin 154) := {38, 47, 51, 57, 63, 72, 73, 80, 82, 84, 87, 99, 102, 112, 116, 129}
theorem cut813 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support813, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 679, OmissionResidual.support 681, OmissionResidual.support 817] ![OmissionResidual.demand 679, OmissionResidual.demand 681, OmissionResidual.demand 817] ![1, 1, 1]
    support813 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 679) (Fin.cases (hrows 681) (Fin.cases (hrows 817) (fun i => Fin.elim0 i))))
def support814 : Finset (Fin 154) := {76, 86, 95, 104, 116, 119, 121, 123, 127, 128, 129, 132, 134, 140, 141, 143, 145, 151}
theorem cut814 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support814, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1073, OmissionResidual.support 1072, OmissionResidual.support 1152] ![OmissionResidual.demand 1073, OmissionResidual.demand 1072, OmissionResidual.demand 1152] ![1, 1, 1]
    support814 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1073) (Fin.cases (hrows 1072) (Fin.cases (hrows 1152) (fun i => Fin.elim0 i))))
def support815 : Finset (Fin 154) := {6, 9, 11, 18, 20, 24, 26, 27, 29, 32, 37, 41, 47, 50, 52, 58, 61, 71, 84, 94}
theorem cut815 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support815, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 490, OmissionResidual.support 507, OmissionResidual.support 631] ![OmissionResidual.demand 490, OmissionResidual.demand 507, OmissionResidual.demand 631] ![1, 1, 1]
    support815 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 490) (Fin.cases (hrows 507) (Fin.cases (hrows 631) (fun i => Fin.elim0 i))))
def support816 : Finset (Fin 154) := {8, 12, 19, 23, 26, 35, 38, 41, 47, 51, 57, 66, 70, 76, 80, 92, 104}
theorem cut816 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support816, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 153, OmissionResidual.support 498, OmissionResidual.support 289] ![OmissionResidual.demand 153, OmissionResidual.demand 498, OmissionResidual.demand 289] ![1, 1, 1]
    support816 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 153) (Fin.cases (hrows 498) (Fin.cases (hrows 289) (fun i => Fin.elim0 i))))
def support817 : Finset (Fin 154) := {0, 3, 6, 7, 9, 11, 12, 17, 18, 20, 24, 25, 26, 27, 29, 30, 32, 37, 41, 43, 47, 50, 52, 58, 61, 71, 84, 94}
theorem cut817 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support817, holes i := by
  apply rounded_cover_cut ![support810, support815, OmissionResidual.support 1] ![2, 2, OmissionResidual.demand 1] ![1, 1, 1]
    support817 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut810 holes hbool hrows) (Fin.cases (cut815 holes hbool hrows) (Fin.cases (hrows 1) (fun i => Fin.elim0 i))))
def support818 : Finset (Fin 154) := {1, 3, 6, 7, 9, 11, 12, 17, 18, 20, 24, 25, 26, 27, 29, 30, 32, 37, 41, 43, 47, 50, 52, 58, 61, 71, 84, 94}
theorem cut818 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support818, holes i := by
  apply rounded_cover_cut ![support810, support815, OmissionResidual.support 5] ![2, 2, OmissionResidual.demand 5] ![1, 1, 1]
    support818 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut810 holes hbool hrows) (Fin.cases (cut815 holes hbool hrows) (Fin.cases (hrows 5) (fun i => Fin.elim0 i))))
def support819 : Finset (Fin 154) := {21, 27, 31, 38, 41, 46, 47, 49, 51, 52, 57, 59, 61, 63, 64, 69, 73, 81, 82, 84, 87, 93, 97, 103, 105}
theorem cut819 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support819, holes i := by
  apply rounded_cover_cut ![support40, support808, OmissionResidual.support 736] ![2, 2, OmissionResidual.demand 736] ![1, 1, 1]
    support819 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut40 holes hbool hrows) (Fin.cases (cut808 holes hbool hrows) (Fin.cases (hrows 736) (fun i => Fin.elim0 i))))
def support820 : Finset (Fin 154) := {49, 59, 61, 64, 71, 76, 81, 87, 92, 93, 97, 100, 102, 105, 108, 113, 115, 120, 122, 126, 134, 140, 143, 151}
theorem cut820 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support820, holes i := by
  apply rounded_cover_cut ![support799, OmissionResidual.support 1143, support622] ![2, OmissionResidual.demand 1143, 2] ![1, 1, 1]
    support820 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut799 holes hbool hrows) (Fin.cases (hrows 1143) (Fin.cases (cut622 holes hbool hrows) (fun i => Fin.elim0 i))))
def support821 : Finset (Fin 154) := {3, 8, 9, 13, 17, 18, 26, 29, 34, 41, 44, 45, 55, 58, 71, 76, 86}
theorem cut821 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support821, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 864, OmissionResidual.support 873, OmissionResidual.support 20] ![OmissionResidual.demand 864, OmissionResidual.demand 873, OmissionResidual.demand 20] ![1, 1, 1]
    support821 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 864) (Fin.cases (hrows 873) (Fin.cases (hrows 20) (fun i => Fin.elim0 i))))
def support822 : Finset (Fin 154) := {5, 8, 9, 13, 18, 25, 26, 29, 34, 41, 44, 45, 55, 58, 71, 76, 86}
theorem cut822 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support822, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 864, OmissionResidual.support 873, OmissionResidual.support 35] ![OmissionResidual.demand 864, OmissionResidual.demand 873, OmissionResidual.demand 35] ![1, 1, 1]
    support822 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 864) (Fin.cases (hrows 873) (Fin.cases (hrows 35) (fun i => Fin.elim0 i))))
def support823 : Finset (Fin 154) := {49, 59, 61, 64, 71, 76, 81, 87, 92, 93, 94, 97, 98, 102, 103, 105, 106, 112, 113, 116, 120, 121, 124, 128, 140}
theorem cut823 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support823, holes i := by
  apply rounded_cover_cut ![support803, support807, OmissionResidual.support 842] ![2, 2, OmissionResidual.demand 842] ![1, 1, 1]
    support823 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut803 holes hbool hrows) (Fin.cases (cut807 holes hbool hrows) (Fin.cases (hrows 842) (fun i => Fin.elim0 i))))
def support824 : Finset (Fin 154) := {49, 59, 61, 64, 71, 76, 81, 87, 92, 93, 94, 97, 98, 102, 103, 105, 106, 112, 113, 116, 120, 121, 124, 128, 144}
theorem cut824 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support824, holes i := by
  apply rounded_cover_cut ![support803, support807, OmissionResidual.support 843] ![2, 2, OmissionResidual.demand 843] ![1, 1, 1]
    support824 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut803 holes hbool hrows) (Fin.cases (cut807 holes hbool hrows) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
def support825 : Finset (Fin 154) := {5, 8, 12, 15, 23, 24, 25, 26, 27, 32, 34, 36, 41, 47, 49, 51, 60, 64}
theorem cut825 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support825, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 549, OmissionResidual.support 497, OmissionResidual.support 33] ![OmissionResidual.demand 549, OmissionResidual.demand 497, OmissionResidual.demand 33] ![1, 1, 1]
    support825 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 549) (Fin.cases (hrows 497) (Fin.cases (hrows 33) (fun i => Fin.elim0 i))))
#print axioms cut825
def support826 : Finset (Fin 154) := {3, 8, 13, 17, 22, 29, 38, 41, 45, 48, 50, 55, 56, 70, 81, 84, 98, 103, 114}
theorem cut826 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support826, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 20, OmissionResidual.support 179, OmissionResidual.support 327] ![OmissionResidual.demand 20, OmissionResidual.demand 179, OmissionResidual.demand 327] ![1, 1, 1]
    support826 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 20) (Fin.cases (hrows 179) (Fin.cases (hrows 327) (fun i => Fin.elim0 i))))
def support827 : Finset (Fin 154) := {5, 8, 13, 22, 25, 29, 38, 41, 45, 48, 50, 55, 56, 70, 81, 84, 98, 103, 114}
theorem cut827 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support827, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 35, OmissionResidual.support 179, OmissionResidual.support 327] ![OmissionResidual.demand 35, OmissionResidual.demand 179, OmissionResidual.demand 327] ![1, 1, 1]
    support827 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 35) (Fin.cases (hrows 179) (Fin.cases (hrows 327) (fun i => Fin.elim0 i))))
def support828 : Finset (Fin 154) := {5, 12, 15, 16, 24, 25, 26, 27, 32, 34, 36, 47, 49, 51, 60, 64}
theorem cut828 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support828, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 549, OmissionResidual.support 485, OmissionResidual.support 33] ![OmissionResidual.demand 549, OmissionResidual.demand 485, OmissionResidual.demand 33] ![1, 1, 1]
    support828 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 549) (Fin.cases (hrows 485) (Fin.cases (hrows 33) (fun i => Fin.elim0 i))))
def support829 : Finset (Fin 154) := {3, 6, 8, 13, 14, 17, 21, 22, 29, 38, 41, 45, 48, 50, 52, 55, 56, 67, 70, 81, 84, 98, 103, 114}
theorem cut829 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support829, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 46, OmissionResidual.support 938, support826] ![OmissionResidual.demand 46, OmissionResidual.demand 938, 2] ![1, 1, 1]
    support829 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 46) (Fin.cases (hrows 938) (Fin.cases (cut826 holes hbool hrows) (fun i => Fin.elim0 i))))
def support830 : Finset (Fin 154) := {5, 8, 10, 13, 14, 21, 22, 25, 29, 38, 41, 45, 48, 50, 52, 55, 56, 67, 70, 81, 84, 98, 103, 114}
theorem cut830 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support830, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 75, OmissionResidual.support 938, support827] ![OmissionResidual.demand 75, OmissionResidual.demand 938, 2] ![1, 1, 1]
    support830 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 75) (Fin.cases (hrows 938) (Fin.cases (cut827 holes hbool hrows) (fun i => Fin.elim0 i))))
def support831 : Finset (Fin 154) := {5, 6, 8, 13, 14, 17, 21, 22, 25, 29, 38, 41, 45, 48, 50, 52, 55, 56, 67, 70, 81, 84, 98, 103, 114}
theorem cut831 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support831, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 46, OmissionResidual.support 938, support827] ![OmissionResidual.demand 46, OmissionResidual.demand 938, 2] ![1, 1, 1]
    support831 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 46) (Fin.cases (hrows 938) (Fin.cases (cut827 holes hbool hrows) (fun i => Fin.elim0 i))))
def support832 : Finset (Fin 154) := {3, 8, 10, 13, 14, 17, 21, 22, 25, 29, 38, 41, 45, 48, 50, 52, 55, 56, 67, 70, 81, 84, 98, 103, 114}
theorem cut832 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support832, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 75, OmissionResidual.support 938, support826] ![OmissionResidual.demand 75, OmissionResidual.demand 938, 2] ![1, 1, 1]
    support832 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 75) (Fin.cases (hrows 938) (Fin.cases (cut826 holes hbool hrows) (fun i => Fin.elim0 i))))
def support833 : Finset (Fin 154) := {94, 103, 106, 112, 114, 116, 120, 121, 124, 128, 130, 132, 135, 138, 140, 143, 144, 150, 153}
theorem cut833 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support833, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1160, OmissionResidual.support 842, OmissionResidual.support 1139] ![OmissionResidual.demand 1160, OmissionResidual.demand 842, OmissionResidual.demand 1139] ![1, 1, 1]
    support833 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1160) (Fin.cases (hrows 842) (Fin.cases (hrows 1139) (fun i => Fin.elim0 i))))
def support834 : Finset (Fin 154) := {94, 103, 106, 112, 114, 116, 120, 121, 124, 128, 130, 132, 135, 138, 140, 143, 144, 148, 153}
theorem cut834 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support834, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1160, OmissionResidual.support 843, OmissionResidual.support 1138] ![OmissionResidual.demand 1160, OmissionResidual.demand 843, OmissionResidual.demand 1138] ![1, 1, 1]
    support834 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1160) (Fin.cases (hrows 843) (Fin.cases (hrows 1138) (fun i => Fin.elim0 i))))
def support835 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 103, 106, 112, 114, 116, 120, 121, 124, 128, 130, 132, 135, 138, 140, 143, 144, 150, 153}
theorem cut835 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support835, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1160, support669, support347] ![OmissionResidual.demand 1160, 3, 3] ![1, 1, 1]
    support835 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1160) (Fin.cases (cut669 holes hbool hrows) (Fin.cases (cut347 holes hbool hrows) (fun i => Fin.elim0 i))))
def support836 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 103, 106, 112, 114, 116, 120, 121, 124, 128, 130, 132, 135, 138, 140, 143, 144, 148, 153}
theorem cut836 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support836, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1160, support671, support354] ![OmissionResidual.demand 1160, 3, 3] ![1, 1, 1]
    support836 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1160) (Fin.cases (cut671 holes hbool hrows) (Fin.cases (cut354 holes hbool hrows) (fun i => Fin.elim0 i))))
def support837 : Finset (Fin 154) := {94, 103, 106, 112, 114, 116, 120, 121, 124, 128, 130, 132, 135, 138, 140, 143, 144, 150, 152}
theorem cut837 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support837, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1159, OmissionResidual.support 842, OmissionResidual.support 1139] ![OmissionResidual.demand 1159, OmissionResidual.demand 842, OmissionResidual.demand 1139] ![1, 1, 1]
    support837 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1159) (Fin.cases (hrows 842) (Fin.cases (hrows 1139) (fun i => Fin.elim0 i))))
def support838 : Finset (Fin 154) := {94, 103, 106, 112, 114, 116, 120, 121, 124, 128, 130, 132, 135, 138, 140, 143, 144, 148, 152}
theorem cut838 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support838, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1159, OmissionResidual.support 843, OmissionResidual.support 1138] ![OmissionResidual.demand 1159, OmissionResidual.demand 843, OmissionResidual.demand 1138] ![1, 1, 1]
    support838 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1159) (Fin.cases (hrows 843) (Fin.cases (hrows 1138) (fun i => Fin.elim0 i))))
def support839 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 103, 106, 112, 114, 116, 120, 121, 124, 128, 130, 132, 135, 138, 140, 143, 144, 150, 152}
theorem cut839 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support839, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1159, support669, support347] ![OmissionResidual.demand 1159, 3, 3] ![1, 1, 1]
    support839 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1159) (Fin.cases (cut669 holes hbool hrows) (Fin.cases (cut347 holes hbool hrows) (fun i => Fin.elim0 i))))
def support840 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 103, 106, 112, 114, 116, 120, 121, 124, 128, 130, 132, 135, 138, 140, 143, 144, 148, 152}
theorem cut840 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support840, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1159, support671, support354] ![OmissionResidual.demand 1159, 3, 3] ![1, 1, 1]
    support840 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1159) (Fin.cases (cut671 holes hbool hrows) (Fin.cases (cut354 holes hbool hrows) (fun i => Fin.elim0 i))))
def support841 : Finset (Fin 154) := {25, 42, 43, 56, 62, 64, 68, 72, 75, 82, 83, 87, 90, 93, 94, 99, 103, 124, 130}
theorem cut841 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support841, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 818, OmissionResidual.support 343, OmissionResidual.support 216] ![OmissionResidual.demand 818, OmissionResidual.demand 343, OmissionResidual.demand 216] ![1, 1, 1]
    support841 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 818) (Fin.cases (hrows 343) (Fin.cases (hrows 216) (fun i => Fin.elim0 i))))
def support842 : Finset (Fin 154) := {0, 7, 11, 12, 16, 17, 20, 23, 30, 31, 33, 41, 43, 52, 68, 79}
theorem cut842 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support842, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 86, OmissionResidual.support 466, OmissionResidual.support 2] ![OmissionResidual.demand 86, OmissionResidual.demand 466, OmissionResidual.demand 2] ![1, 1, 1]
    support842 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 86) (Fin.cases (hrows 466) (Fin.cases (hrows 2) (fun i => Fin.elim0 i))))
def support843 : Finset (Fin 154) := {1, 7, 11, 12, 16, 17, 20, 23, 30, 31, 33, 41, 43, 52, 68, 79}
theorem cut843 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support843, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 86, OmissionResidual.support 468, OmissionResidual.support 6] ![OmissionResidual.demand 86, OmissionResidual.demand 468, OmissionResidual.demand 6] ![1, 1, 1]
    support843 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 86) (Fin.cases (hrows 468) (Fin.cases (hrows 6) (fun i => Fin.elim0 i))))
def support844 : Finset (Fin 154) := {0, 1, 7, 11, 12, 16, 17, 20, 23, 30, 31, 33, 41, 43, 52, 68, 79}
theorem cut844 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support844, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 86, OmissionResidual.support 466, OmissionResidual.support 6] ![OmissionResidual.demand 86, OmissionResidual.demand 466, OmissionResidual.demand 6] ![1, 1, 1]
    support844 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 86) (Fin.cases (hrows 466) (Fin.cases (hrows 6) (fun i => Fin.elim0 i))))
def support845 : Finset (Fin 154) := {21, 27, 40, 44, 46, 49, 53, 59, 65, 69, 78, 81, 86, 88, 93, 95, 105}
theorem cut845 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support845, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 312, OmissionResidual.support 619, OmissionResidual.support 168] ![OmissionResidual.demand 312, OmissionResidual.demand 619, OmissionResidual.demand 168] ![1, 1, 1]
    support845 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 312) (Fin.cases (hrows 619) (Fin.cases (hrows 168) (fun i => Fin.elim0 i))))
def support846 : Finset (Fin 154) := {7, 26, 27, 35, 43, 46, 53, 59, 64, 65, 69, 74, 75, 81, 86, 95}
theorem cut846 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support846, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 494, OmissionResidual.support 619, OmissionResidual.support 616] ![OmissionResidual.demand 494, OmissionResidual.demand 619, OmissionResidual.demand 616] ![1, 1, 1]
    support846 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 494) (Fin.cases (hrows 619) (Fin.cases (hrows 616) (fun i => Fin.elim0 i))))
def support847 : Finset (Fin 154) := {21, 27, 31, 40, 41, 44, 46, 49, 59, 61, 69, 78, 81, 88, 93, 105}
theorem cut847 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support847, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 312, OmissionResidual.support 581, OmissionResidual.support 168] ![OmissionResidual.demand 312, OmissionResidual.demand 581, OmissionResidual.demand 168] ![1, 1, 1]
    support847 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 312) (Fin.cases (hrows 581) (Fin.cases (hrows 168) (fun i => Fin.elim0 i))))
def support848 : Finset (Fin 154) := {7, 19, 21, 26, 27, 31, 35, 40, 41, 43, 46, 51, 53, 59, 61, 64, 69, 74, 81}
theorem cut848 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support848, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 494, OmissionResidual.support 581, OmissionResidual.support 571] ![OmissionResidual.demand 494, OmissionResidual.demand 581, OmissionResidual.demand 571] ![1, 1, 1]
    support848 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 494) (Fin.cases (hrows 581) (Fin.cases (hrows 571) (fun i => Fin.elim0 i))))
def support849 : Finset (Fin 154) := {7, 19, 26, 27, 35, 40, 43, 46, 51, 53, 59, 61, 64, 65, 69, 74, 81, 86, 95}
theorem cut849 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support849, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 494, OmissionResidual.support 619, OmissionResidual.support 571] ![OmissionResidual.demand 494, OmissionResidual.demand 619, OmissionResidual.demand 571] ![1, 1, 1]
    support849 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 494) (Fin.cases (hrows 619) (Fin.cases (hrows 571) (fun i => Fin.elim0 i))))
def support850 : Finset (Fin 154) := {7, 21, 26, 27, 31, 35, 41, 43, 46, 53, 59, 61, 64, 69, 74, 75, 81, 86, 95}
theorem cut850 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support850, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 494, OmissionResidual.support 581, OmissionResidual.support 616] ![OmissionResidual.demand 494, OmissionResidual.demand 581, OmissionResidual.demand 616] ![1, 1, 1]
    support850 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 494) (Fin.cases (hrows 581) (Fin.cases (hrows 616) (fun i => Fin.elim0 i))))
#print axioms cut850
def support851 : Finset (Fin 154) := {4, 7, 26, 27, 33, 35, 44, 46, 53, 59, 64, 65, 69, 74, 75, 81, 86, 95}
theorem cut851 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support851, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 619, OmissionResidual.support 25, OmissionResidual.support 616] ![OmissionResidual.demand 619, OmissionResidual.demand 25, OmissionResidual.demand 616] ![1, 1, 1]
    support851 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 619) (Fin.cases (hrows 25) (Fin.cases (hrows 616) (fun i => Fin.elim0 i))))
def support852 : Finset (Fin 154) := {0, 3, 6, 7, 9, 11, 12, 17, 18, 20, 24, 26, 27, 29, 30, 32, 33, 37, 41, 43, 47, 50, 52, 58, 61, 71, 84, 94}
theorem cut852 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support852, holes i := by
  apply rounded_cover_cut ![support810, OmissionResidual.support 2, support815] ![2, OmissionResidual.demand 2, 2] ![1, 1, 1]
    support852 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut810 holes hbool hrows) (Fin.cases (hrows 2) (Fin.cases (cut815 holes hbool hrows) (fun i => Fin.elim0 i))))
def support853 : Finset (Fin 154) := {1, 3, 6, 7, 9, 11, 12, 17, 18, 20, 24, 26, 27, 29, 30, 32, 33, 37, 41, 43, 47, 50, 52, 58, 61, 71, 84, 94}
theorem cut853 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support853, holes i := by
  apply rounded_cover_cut ![support810, OmissionResidual.support 6, support815] ![2, OmissionResidual.demand 6, 2] ![1, 1, 1]
    support853 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut810 holes hbool hrows) (Fin.cases (hrows 6) (Fin.cases (cut815 holes hbool hrows) (fun i => Fin.elim0 i))))
def support854 : Finset (Fin 154) := {32, 44, 45, 50, 53, 56, 60, 64, 68, 71, 79, 83, 86, 88, 97, 100, 108}
theorem cut854 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support854, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 923, OmissionResidual.support 351, OmissionResidual.support 925] ![OmissionResidual.demand 923, OmissionResidual.demand 351, OmissionResidual.demand 925] ![1, 1, 1]
    support854 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 923) (Fin.cases (hrows 351) (Fin.cases (hrows 925) (fun i => Fin.elim0 i))))
def support855 : Finset (Fin 154) := {12, 26, 27, 35, 43, 46, 53, 59, 64, 65, 69, 74, 75, 81, 86, 95}
theorem cut855 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support855, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 619, OmissionResidual.support 616, OmissionResidual.support 526] ![OmissionResidual.demand 619, OmissionResidual.demand 616, OmissionResidual.demand 526] ![1, 1, 1]
    support855 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 619) (Fin.cases (hrows 616) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support856 : Finset (Fin 154) := {4, 7, 19, 21, 26, 27, 31, 33, 35, 40, 41, 44, 46, 51, 59, 61, 69, 74, 81}
theorem cut856 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support856, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 581, OmissionResidual.support 25, OmissionResidual.support 571] ![OmissionResidual.demand 581, OmissionResidual.demand 25, OmissionResidual.demand 571] ![1, 1, 1]
    support856 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 581) (Fin.cases (hrows 25) (Fin.cases (hrows 571) (fun i => Fin.elim0 i))))
def support857 : Finset (Fin 154) := {4, 7, 19, 26, 27, 33, 35, 40, 44, 46, 51, 53, 59, 61, 65, 69, 74, 81, 86, 95}
theorem cut857 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support857, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 619, OmissionResidual.support 25, OmissionResidual.support 571] ![OmissionResidual.demand 619, OmissionResidual.demand 25, OmissionResidual.demand 571] ![1, 1, 1]
    support857 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 619) (Fin.cases (hrows 25) (Fin.cases (hrows 571) (fun i => Fin.elim0 i))))
def support858 : Finset (Fin 154) := {4, 7, 21, 26, 27, 31, 33, 35, 41, 44, 46, 59, 61, 64, 69, 74, 75, 81, 86, 95}
theorem cut858 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support858, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 581, OmissionResidual.support 25, OmissionResidual.support 616] ![OmissionResidual.demand 581, OmissionResidual.demand 25, OmissionResidual.demand 616] ![1, 1, 1]
    support858 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 581) (Fin.cases (hrows 25) (Fin.cases (hrows 616) (fun i => Fin.elim0 i))))
def support859 : Finset (Fin 154) := {4, 7, 13, 18, 19, 21, 23, 26, 27, 31, 35, 40, 41, 44, 46, 51, 55, 58, 59, 61, 69, 71, 76, 81, 86, 95}
theorem cut859 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support859, holes i := by
  apply rounded_cover_cut ![support699, OmissionResidual.support 873, support592] ![2, OmissionResidual.demand 873, 3] ![1, 1, 1]
    support859 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut699 holes hbool hrows) (Fin.cases (hrows 873) (Fin.cases (cut592 holes hbool hrows) (fun i => Fin.elim0 i))))
def support860 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 103, 106, 112, 114, 116, 120, 121, 123, 124, 128, 129, 132, 134, 138, 140, 144, 150}
theorem cut860 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support860, holes i := by
  apply rounded_cover_cut ![support347, support669, OmissionResidual.support 1151] ![3, 3, OmissionResidual.demand 1151] ![1, 1, 1]
    support860 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut347 holes hbool hrows) (Fin.cases (cut669 holes hbool hrows) (Fin.cases (hrows 1151) (fun i => Fin.elim0 i))))
def support861 : Finset (Fin 154) := {76, 86, 95, 104, 106, 114, 119, 121, 127, 128, 129, 132, 134, 138, 141, 144, 145, 150}
theorem cut861 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support861, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1073, OmissionResidual.support 1072, OmissionResidual.support 1139] ![OmissionResidual.demand 1073, OmissionResidual.demand 1072, OmissionResidual.demand 1139] ![1, 1, 1]
    support861 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1073) (Fin.cases (hrows 1072) (Fin.cases (hrows 1139) (fun i => Fin.elim0 i))))
def support862 : Finset (Fin 154) := {12, 19, 21, 26, 27, 31, 35, 40, 41, 43, 46, 51, 53, 59, 61, 64, 69, 74, 81}
theorem cut862 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support862, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 581, OmissionResidual.support 571, OmissionResidual.support 526] ![OmissionResidual.demand 581, OmissionResidual.demand 571, OmissionResidual.demand 526] ![1, 1, 1]
    support862 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 581) (Fin.cases (hrows 571) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support863 : Finset (Fin 154) := {12, 19, 26, 27, 35, 40, 43, 46, 51, 53, 59, 61, 64, 65, 69, 74, 81, 86, 95}
theorem cut863 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support863, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 619, OmissionResidual.support 571, OmissionResidual.support 526] ![OmissionResidual.demand 619, OmissionResidual.demand 571, OmissionResidual.demand 526] ![1, 1, 1]
    support863 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 619) (Fin.cases (hrows 571) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support864 : Finset (Fin 154) := {12, 21, 26, 27, 31, 35, 41, 43, 46, 53, 59, 61, 64, 69, 74, 75, 81, 86, 95}
theorem cut864 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support864, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 581, OmissionResidual.support 616, OmissionResidual.support 526] ![OmissionResidual.demand 581, OmissionResidual.demand 616, OmissionResidual.demand 526] ![1, 1, 1]
    support864 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 581) (Fin.cases (hrows 616) (Fin.cases (hrows 526) (fun i => Fin.elim0 i))))
def support865 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 103, 106, 112, 114, 116, 120, 121, 123, 124, 128, 129, 132, 134, 138, 140, 144, 148}
theorem cut865 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support865, holes i := by
  apply rounded_cover_cut ![support354, support671, OmissionResidual.support 1150] ![3, 3, OmissionResidual.demand 1150] ![1, 1, 1]
    support865 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut354 holes hbool hrows) (Fin.cases (cut671 holes hbool hrows) (Fin.cases (hrows 1150) (fun i => Fin.elim0 i))))
def support866 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 103, 106, 112, 114, 116, 120, 121, 123, 124, 128, 129, 132, 134, 138, 140, 144, 148, 150}
theorem cut866 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support866, holes i := by
  apply rounded_cover_cut ![support347, support671, OmissionResidual.support 1150] ![3, 3, OmissionResidual.demand 1150] ![1, 1, 1]
    support866 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut347 holes hbool hrows) (Fin.cases (cut671 holes hbool hrows) (Fin.cases (hrows 1150) (fun i => Fin.elim0 i))))
def support867 : Finset (Fin 154) := {8, 12, 26, 27, 33, 35, 44, 46, 53, 59, 64, 65, 69, 74, 75, 81, 86, 95}
theorem cut867 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support867, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 619, OmissionResidual.support 616, OmissionResidual.support 51] ![OmissionResidual.demand 619, OmissionResidual.demand 616, OmissionResidual.demand 51] ![1, 1, 1]
    support867 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 619) (Fin.cases (hrows 616) (Fin.cases (hrows 51) (fun i => Fin.elim0 i))))
def support868 : Finset (Fin 154) := {76, 86, 95, 104, 106, 114, 119, 121, 127, 128, 129, 132, 134, 138, 140, 141, 145, 148}
theorem cut868 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support868, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1073, OmissionResidual.support 1072, OmissionResidual.support 1138] ![OmissionResidual.demand 1073, OmissionResidual.demand 1072, OmissionResidual.demand 1138] ![1, 1, 1]
    support868 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1073) (Fin.cases (hrows 1072) (Fin.cases (hrows 1138) (fun i => Fin.elim0 i))))
def support869 : Finset (Fin 154) := {7, 13, 18, 21, 26, 27, 35, 43, 44, 46, 53, 55, 58, 59, 64, 65, 69, 71, 74, 75, 76, 81, 86, 95}
theorem cut869 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support869, holes i := by
  apply rounded_cover_cut ![support846, OmissionResidual.support 873, support591] ![2, OmissionResidual.demand 873, 3] ![1, 1, 1]
    support869 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut846 holes hbool hrows) (Fin.cases (hrows 873) (Fin.cases (cut591 holes hbool hrows) (fun i => Fin.elim0 i))))
def support870 : Finset (Fin 154) := {7, 13, 18, 19, 21, 26, 27, 35, 40, 43, 44, 46, 51, 53, 55, 58, 59, 61, 64, 65, 69, 71, 74, 76, 81, 86, 95}
theorem cut870 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support870, holes i := by
  apply rounded_cover_cut ![support849, OmissionResidual.support 873, support591] ![2, OmissionResidual.demand 873, 3] ![1, 1, 1]
    support870 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut849 holes hbool hrows) (Fin.cases (hrows 873) (Fin.cases (cut591 holes hbool hrows) (fun i => Fin.elim0 i))))
def support871 : Finset (Fin 154) := {7, 12, 13, 18, 21, 26, 27, 35, 43, 44, 46, 53, 55, 58, 59, 64, 65, 69, 71, 74, 75, 76, 81, 86, 95}
theorem cut871 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support871, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 873, support591, support855] ![OmissionResidual.demand 873, 3, 2] ![1, 1, 1]
    support871 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 873) (Fin.cases (cut591 holes hbool hrows) (Fin.cases (cut855 holes hbool hrows) (fun i => Fin.elim0 i))))
def support872 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 99, 103, 106, 107, 112, 114, 115, 116, 118, 120, 121, 123, 124, 128, 129, 130, 132, 134, 135, 138, 140, 143, 144, 147, 150, 153}
theorem cut872 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support872, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1126, support860, support835] ![OmissionResidual.demand 1126, 4, 4] ![1, 1, 1]
    support872 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1126) (Fin.cases (cut860 holes hbool hrows) (Fin.cases (cut835 holes hbool hrows) (fun i => Fin.elim0 i))))
def support873 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 99, 103, 106, 107, 112, 114, 115, 116, 118, 120, 121, 123, 124, 128, 129, 130, 132, 134, 135, 138, 140, 143, 144, 147, 150, 152}
theorem cut873 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support873, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1126, support860, support839] ![OmissionResidual.demand 1126, 4, 4] ![1, 1, 1]
    support873 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1126) (Fin.cases (cut860 holes hbool hrows) (Fin.cases (cut839 holes hbool hrows) (fun i => Fin.elim0 i))))
def support874 : Finset (Fin 154) := {33, 43, 53, 64, 74, 75, 85, 87, 96, 99, 101, 107, 110, 111, 118, 125}
theorem cut874 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support874, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1021, OmissionResidual.support 993, OmissionResidual.support 994] ![OmissionResidual.demand 1021, OmissionResidual.demand 993, OmissionResidual.demand 994] ![1, 1, 1]
    support874 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1021) (Fin.cases (hrows 993) (Fin.cases (hrows 994) (fun i => Fin.elim0 i))))
def support875 : Finset (Fin 154) := {8, 12, 13, 18, 26, 27, 33, 39, 44, 47, 53, 55, 60, 66, 75}
theorem cut875 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support875, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 861, OmissionResidual.support 49, OmissionResidual.support 871] ![OmissionResidual.demand 861, OmissionResidual.demand 49, OmissionResidual.demand 871] ![1, 1, 1]
    support875 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 861) (Fin.cases (hrows 49) (Fin.cases (hrows 871) (fun i => Fin.elim0 i))))
#print axioms cut875
def support876 : Finset (Fin 154) := {40, 49, 59, 64, 75, 78, 85, 88, 92, 99, 102, 104, 108, 113, 118, 122, 126, 136}
theorem cut876 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support876, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 313, OmissionResidual.support 739, OmissionResidual.support 1069] ![OmissionResidual.demand 313, OmissionResidual.demand 739, OmissionResidual.demand 1069] ![1, 1, 1]
    support876 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 313) (Fin.cases (hrows 739) (Fin.cases (hrows 1069) (fun i => Fin.elim0 i))))
def support877 : Finset (Fin 154) := {11, 17, 23, 24, 30, 33, 39, 49, 50, 56, 60, 62, 67, 72, 77, 78, 87}
theorem cut877 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support877, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 899, OmissionResidual.support 211, OmissionResidual.support 869] ![OmissionResidual.demand 899, OmissionResidual.demand 211, OmissionResidual.demand 869] ![1, 1, 1]
    support877 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 899) (Fin.cases (hrows 211) (Fin.cases (hrows 869) (fun i => Fin.elim0 i))))
def support878 : Finset (Fin 154) := {41, 50, 55, 63, 67, 70, 72, 78, 81, 82, 88, 93, 98, 103, 105, 114}
theorem cut878 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support878, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 420, OmissionResidual.support 936, OmissionResidual.support 938] ![OmissionResidual.demand 420, OmissionResidual.demand 936, OmissionResidual.demand 938] ![1, 1, 1]
    support878 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 420) (Fin.cases (hrows 936) (Fin.cases (hrows 938) (fun i => Fin.elim0 i))))
def support879 : Finset (Fin 154) := {2, 4, 6, 11, 13, 14, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut879 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support879, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 83, OmissionResidual.support 46, OmissionResidual.support 10] ![OmissionResidual.demand 83, OmissionResidual.demand 46, OmissionResidual.demand 10] ![1, 1, 1]
    support879 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 83) (Fin.cases (hrows 46) (Fin.cases (hrows 10) (fun i => Fin.elim0 i))))
def support880 : Finset (Fin 154) := {5, 6, 8, 11, 13, 14, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut880 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support880, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 83, OmissionResidual.support 46, OmissionResidual.support 30] ![OmissionResidual.demand 83, OmissionResidual.demand 46, OmissionResidual.demand 30] ![1, 1, 1]
    support880 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 83) (Fin.cases (hrows 46) (Fin.cases (hrows 30) (fun i => Fin.elim0 i))))
def support881 : Finset (Fin 154) := {1, 4, 10, 11, 13, 14, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut881 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support881, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 83, OmissionResidual.support 75, OmissionResidual.support 7] ![OmissionResidual.demand 83, OmissionResidual.demand 75, OmissionResidual.demand 7] ![1, 1, 1]
    support881 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 83) (Fin.cases (hrows 75) (Fin.cases (hrows 7) (fun i => Fin.elim0 i))))
def support882 : Finset (Fin 154) := {2, 4, 10, 11, 13, 14, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut882 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support882, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 83, OmissionResidual.support 75, OmissionResidual.support 10] ![OmissionResidual.demand 83, OmissionResidual.demand 75, OmissionResidual.demand 10] ![1, 1, 1]
    support882 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 83) (Fin.cases (hrows 75) (Fin.cases (hrows 10) (fun i => Fin.elim0 i))))
def support883 : Finset (Fin 154) := {3, 8, 10, 11, 13, 14, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut883 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support883, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 83, OmissionResidual.support 75, OmissionResidual.support 17] ![OmissionResidual.demand 83, OmissionResidual.demand 75, OmissionResidual.demand 17] ![1, 1, 1]
    support883 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 83) (Fin.cases (hrows 75) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support884 : Finset (Fin 154) := {5, 8, 10, 11, 13, 14, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut884 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support884, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 83, OmissionResidual.support 75, OmissionResidual.support 30] ![OmissionResidual.demand 83, OmissionResidual.demand 75, OmissionResidual.demand 30] ![1, 1, 1]
    support884 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 83) (Fin.cases (hrows 75) (Fin.cases (hrows 30) (fun i => Fin.elim0 i))))
def support885 : Finset (Fin 154) := {63, 72, 82, 84, 93, 94, 102, 103, 111, 112, 120, 127, 133, 137, 146, 148}
theorem cut885 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support885, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1041, OmissionResidual.support 1093, OmissionResidual.support 1038] ![OmissionResidual.demand 1041, OmissionResidual.demand 1093, OmissionResidual.demand 1038] ![1, 1, 1]
    support885 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1041) (Fin.cases (hrows 1093) (Fin.cases (hrows 1038) (fun i => Fin.elim0 i))))
def support886 : Finset (Fin 154) := {63, 72, 82, 84, 93, 94, 102, 103, 111, 112, 120, 127, 133, 137, 146, 150}
theorem cut886 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support886, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1041, OmissionResidual.support 1094, OmissionResidual.support 1038] ![OmissionResidual.demand 1041, OmissionResidual.demand 1094, OmissionResidual.demand 1038] ![1, 1, 1]
    support886 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1041) (Fin.cases (hrows 1094) (Fin.cases (hrows 1038) (fun i => Fin.elim0 i))))
def support887 : Finset (Fin 154) := {52, 62, 67, 72, 79, 82, 83, 93, 94, 103, 106, 112, 116, 117, 120, 124, 130, 144}
theorem cut887 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support887, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 958, OmissionResidual.support 843, OmissionResidual.support 957] ![OmissionResidual.demand 958, OmissionResidual.demand 843, OmissionResidual.demand 957] ![1, 1, 1]
    support887 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 958) (Fin.cases (hrows 843) (Fin.cases (hrows 957) (fun i => Fin.elim0 i))))
def support888 : Finset (Fin 154) := {1, 4, 6, 13, 14, 16, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut888 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support888, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 46, OmissionResidual.support 7, OmissionResidual.support 130] ![OmissionResidual.demand 46, OmissionResidual.demand 7, OmissionResidual.demand 130] ![1, 1, 1]
    support888 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 46) (Fin.cases (hrows 7) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))
def support889 : Finset (Fin 154) := {2, 4, 6, 13, 14, 16, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut889 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support889, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 46, OmissionResidual.support 10, OmissionResidual.support 130] ![OmissionResidual.demand 46, OmissionResidual.demand 10, OmissionResidual.demand 130] ![1, 1, 1]
    support889 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 46) (Fin.cases (hrows 10) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))
def support890 : Finset (Fin 154) := {3, 6, 8, 13, 14, 16, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut890 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support890, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 46, OmissionResidual.support 17, OmissionResidual.support 130] ![OmissionResidual.demand 46, OmissionResidual.demand 17, OmissionResidual.demand 130] ![1, 1, 1]
    support890 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 46) (Fin.cases (hrows 17) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))
def support891 : Finset (Fin 154) := {5, 6, 8, 13, 14, 16, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut891 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support891, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 46, OmissionResidual.support 30, OmissionResidual.support 130] ![OmissionResidual.demand 46, OmissionResidual.demand 30, OmissionResidual.demand 130] ![1, 1, 1]
    support891 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 46) (Fin.cases (hrows 30) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))
def support892 : Finset (Fin 154) := {1, 4, 10, 13, 14, 16, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut892 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support892, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 75, OmissionResidual.support 7, OmissionResidual.support 130] ![OmissionResidual.demand 75, OmissionResidual.demand 7, OmissionResidual.demand 130] ![1, 1, 1]
    support892 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 75) (Fin.cases (hrows 7) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))
def support893 : Finset (Fin 154) := {3, 8, 10, 13, 14, 16, 17, 21, 23, 25, 29, 31, 34, 41, 44, 52, 56, 67}
theorem cut893 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support893, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 75, OmissionResidual.support 17, OmissionResidual.support 130] ![OmissionResidual.demand 75, OmissionResidual.demand 17, OmissionResidual.demand 130] ![1, 1, 1]
    support893 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 75) (Fin.cases (hrows 17) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))
def support894 : Finset (Fin 154) := {21, 27, 29, 31, 37, 41, 46, 50, 51, 52, 57, 61, 63, 65, 69, 70, 73, 81, 82, 84, 89, 93, 103, 116, 123}
theorem cut894 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support894, holes i := by
  apply rounded_cover_cut ![support420, support501, OmissionResidual.support 743] ![2, 2, OmissionResidual.demand 743] ![1, 1, 1]
    support894 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut420 holes hbool hrows) (Fin.cases (cut501 holes hbool hrows) (Fin.cases (hrows 743) (fun i => Fin.elim0 i))))
def support895 : Finset (Fin 154) := {6, 11, 14, 20, 23, 27, 29, 32, 37, 41, 46, 50, 52, 57, 63, 69, 73, 82, 93}
theorem cut895 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support895, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 630, OmissionResidual.support 542, OmissionResidual.support 490] ![OmissionResidual.demand 630, OmissionResidual.demand 542, OmissionResidual.demand 490] ![1, 1, 1]
    support895 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 630) (Fin.cases (hrows 542) (Fin.cases (hrows 490) (fun i => Fin.elim0 i))))
def support896 : Finset (Fin 154) := {15, 24, 27, 28, 32, 36, 40, 46, 48, 58, 61, 63, 69, 71, 73, 80, 84, 93, 112}
theorem cut896 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support896, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 730, OmissionResidual.support 624, OmissionResidual.support 550] ![OmissionResidual.demand 730, OmissionResidual.demand 624, OmissionResidual.demand 550] ![1, 1, 1]
    support896 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 730) (Fin.cases (hrows 624) (Fin.cases (hrows 550) (fun i => Fin.elim0 i))))
def support897 : Finset (Fin 154) := {15, 24, 27, 28, 32, 36, 40, 46, 48, 58, 61, 63, 69, 71, 73, 80, 84, 93, 120}
theorem cut897 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support897, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 731, OmissionResidual.support 624, OmissionResidual.support 550] ![OmissionResidual.demand 731, OmissionResidual.demand 624, OmissionResidual.demand 550] ![1, 1, 1]
    support897 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 731) (Fin.cases (hrows 624) (Fin.cases (hrows 550) (fun i => Fin.elim0 i))))
def support898 : Finset (Fin 154) := {52, 62, 67, 72, 79, 82, 83, 93, 94, 103, 106, 112, 116, 117, 120, 124, 130, 140}
theorem cut898 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support898, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 958, OmissionResidual.support 842, OmissionResidual.support 957] ![OmissionResidual.demand 958, OmissionResidual.demand 842, OmissionResidual.demand 957] ![1, 1, 1]
    support898 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 958) (Fin.cases (hrows 842) (Fin.cases (hrows 957) (fun i => Fin.elim0 i))))
def support899 : Finset (Fin 154) := {50, 52, 62, 65, 67, 70, 72, 79, 81, 82, 83, 89, 93, 94, 103, 116, 123}
theorem cut899 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support899, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 383, OmissionResidual.support 743, OmissionResidual.support 384] ![OmissionResidual.demand 383, OmissionResidual.demand 743, OmissionResidual.demand 384] ![1, 1, 1]
    support899 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 383) (Fin.cases (hrows 743) (Fin.cases (hrows 384) (fun i => Fin.elim0 i))))
def support900 : Finset (Fin 154) := {50, 52, 62, 65, 67, 70, 72, 79, 81, 82, 83, 89, 93, 94, 103, 109, 116, 123}
theorem cut900 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support900, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 955, OmissionResidual.support 743, OmissionResidual.support 956] ![OmissionResidual.demand 955, OmissionResidual.demand 743, OmissionResidual.demand 956] ![1, 1, 1]
    support900 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 955) (Fin.cases (hrows 743) (Fin.cases (hrows 956) (fun i => Fin.elim0 i))))
#print axioms cut900
def support901 : Finset (Fin 154) := {15, 24, 27, 28, 32, 36, 40, 46, 48, 58, 61, 63, 69, 71, 73, 80, 84, 102, 112}
theorem cut901 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support901, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 730, OmissionResidual.support 625, OmissionResidual.support 550] ![OmissionResidual.demand 730, OmissionResidual.demand 625, OmissionResidual.demand 550] ![1, 1, 1]
    support901 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 730) (Fin.cases (hrows 625) (Fin.cases (hrows 550) (fun i => Fin.elim0 i))))
def support902 : Finset (Fin 154) := {15, 24, 27, 28, 32, 36, 40, 46, 48, 58, 61, 63, 69, 71, 73, 80, 84, 102, 120}
theorem cut902 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support902, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 625, OmissionResidual.support 731, OmissionResidual.support 550] ![OmissionResidual.demand 625, OmissionResidual.demand 731, OmissionResidual.demand 550] ![1, 1, 1]
    support902 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 625) (Fin.cases (hrows 731) (Fin.cases (hrows 550) (fun i => Fin.elim0 i))))
def support903 : Finset (Fin 154) := {4, 7, 21, 23, 26, 27, 28, 31, 36, 40, 46, 49, 52, 63, 69, 73, 93}
theorem cut903 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support903, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 624, OmissionResidual.support 585, OmissionResidual.support 478] ![OmissionResidual.demand 624, OmissionResidual.demand 585, OmissionResidual.demand 478] ![1, 1, 1]
    support903 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 624) (Fin.cases (hrows 585) (Fin.cases (hrows 478) (fun i => Fin.elim0 i))))
def support904 : Finset (Fin 154) := {8, 12, 21, 23, 26, 27, 28, 31, 36, 40, 46, 49, 52, 63, 69, 73, 93}
theorem cut904 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support904, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 624, OmissionResidual.support 585, OmissionResidual.support 495] ![OmissionResidual.demand 624, OmissionResidual.demand 585, OmissionResidual.demand 495] ![1, 1, 1]
    support904 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 624) (Fin.cases (hrows 585) (Fin.cases (hrows 495) (fun i => Fin.elim0 i))))
def support905 : Finset (Fin 154) := {9, 13, 15, 19, 24, 27, 28, 32, 34, 36, 40, 45, 46, 48, 58, 61, 63, 69, 71, 73, 76, 80, 84, 86, 102, 112}
theorem cut905 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support905, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 64, OmissionResidual.support 880, support901] ![OmissionResidual.demand 64, OmissionResidual.demand 880, 2] ![1, 1, 1]
    support905 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 64) (Fin.cases (hrows 880) (Fin.cases (cut901 holes hbool hrows) (fun i => Fin.elim0 i))))
def support906 : Finset (Fin 154) := {9, 13, 15, 19, 24, 27, 28, 32, 34, 36, 40, 45, 46, 48, 58, 61, 63, 69, 71, 73, 76, 80, 84, 86, 102, 120}
theorem cut906 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support906, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 64, OmissionResidual.support 880, support902] ![OmissionResidual.demand 64, OmissionResidual.demand 880, 2] ![1, 1, 1]
    support906 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 64) (Fin.cases (hrows 880) (Fin.cases (cut902 holes hbool hrows) (fun i => Fin.elim0 i))))
def support907 : Finset (Fin 154) := {9, 13, 15, 19, 24, 27, 28, 32, 34, 36, 40, 45, 46, 48, 58, 61, 63, 69, 71, 73, 76, 80, 84, 86, 93, 112}
theorem cut907 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support907, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 64, OmissionResidual.support 880, support896] ![OmissionResidual.demand 64, OmissionResidual.demand 880, 2] ![1, 1, 1]
    support907 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 64) (Fin.cases (hrows 880) (Fin.cases (cut896 holes hbool hrows) (fun i => Fin.elim0 i))))
def support908 : Finset (Fin 154) := {9, 13, 15, 19, 24, 27, 28, 32, 34, 36, 40, 45, 46, 48, 58, 61, 63, 69, 71, 73, 76, 80, 84, 86, 93, 120}
theorem cut908 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support908, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 64, OmissionResidual.support 880, support897] ![OmissionResidual.demand 64, OmissionResidual.demand 880, 2] ![1, 1, 1]
    support908 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 64) (Fin.cases (hrows 880) (Fin.cases (cut897 holes hbool hrows) (fun i => Fin.elim0 i))))
def support909 : Finset (Fin 154) := {28, 36, 40, 46, 49, 51, 59, 61, 63, 64, 69, 71, 73, 76, 80, 81, 87, 92, 93, 97, 98, 102, 105, 112, 113, 121}
theorem cut909 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support909, holes i := by
  apply rounded_cover_cut ![support458, support803, OmissionResidual.support 624] ![2, 2, OmissionResidual.demand 624] ![1, 1, 1]
    support909 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut458 holes hbool hrows) (Fin.cases (cut803 holes hbool hrows) (Fin.cases (hrows 624) (fun i => Fin.elim0 i))))
def support910 : Finset (Fin 154) := {28, 36, 40, 46, 49, 51, 59, 61, 63, 64, 69, 71, 73, 76, 80, 81, 87, 92, 93, 97, 98, 102, 105, 113, 120, 128}
theorem cut910 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support910, holes i := by
  apply rounded_cover_cut ![support458, support807, OmissionResidual.support 624] ![2, 2, OmissionResidual.demand 624] ![1, 1, 1]
    support910 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut458 holes hbool hrows) (Fin.cases (cut807 holes hbool hrows) (Fin.cases (hrows 624) (fun i => Fin.elim0 i))))
def support911 : Finset (Fin 154) := {28, 36, 40, 46, 49, 51, 59, 61, 63, 64, 69, 71, 73, 76, 80, 81, 87, 92, 93, 97, 100, 102, 105, 113, 122}
theorem cut911 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support911, holes i := by
  apply rounded_cover_cut ![support458, support622, OmissionResidual.support 624] ![2, 2, OmissionResidual.demand 624] ![1, 1, 1]
    support911 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut458 holes hbool hrows) (Fin.cases (cut622 holes hbool hrows) (Fin.cases (hrows 624) (fun i => Fin.elim0 i))))
def support912 : Finset (Fin 154) := {15, 24, 27, 36, 42, 46, 48, 58, 61, 64, 69, 73, 80, 83, 84, 87, 97, 102, 112, 113}
theorem cut912 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support912, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 552, OmissionResidual.support 730, OmissionResidual.support 675] ![OmissionResidual.demand 552, OmissionResidual.demand 730, OmissionResidual.demand 675] ![1, 1, 1]
    support912 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 552) (Fin.cases (hrows 730) (Fin.cases (hrows 675) (fun i => Fin.elim0 i))))
def support913 : Finset (Fin 154) := {15, 24, 27, 36, 42, 46, 48, 58, 61, 64, 69, 73, 80, 83, 84, 87, 97, 102, 113, 120}
theorem cut913 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support913, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 552, OmissionResidual.support 731, OmissionResidual.support 675] ![OmissionResidual.demand 552, OmissionResidual.demand 731, OmissionResidual.demand 675] ![1, 1, 1]
    support913 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 552) (Fin.cases (hrows 731) (Fin.cases (hrows 675) (fun i => Fin.elim0 i))))
def support914 : Finset (Fin 154) := {15, 24, 27, 36, 42, 46, 48, 58, 61, 64, 69, 73, 80, 83, 84, 87, 93, 97, 105, 112}
theorem cut914 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support914, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 552, OmissionResidual.support 730, OmissionResidual.support 674] ![OmissionResidual.demand 552, OmissionResidual.demand 730, OmissionResidual.demand 674] ![1, 1, 1]
    support914 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 552) (Fin.cases (hrows 730) (Fin.cases (hrows 674) (fun i => Fin.elim0 i))))
def support915 : Finset (Fin 154) := {15, 24, 27, 36, 42, 46, 48, 58, 61, 64, 69, 73, 80, 83, 84, 87, 93, 97, 105, 120}
theorem cut915 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support915, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 552, OmissionResidual.support 731, OmissionResidual.support 674] ![OmissionResidual.demand 552, OmissionResidual.demand 731, OmissionResidual.demand 674] ![1, 1, 1]
    support915 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 552) (Fin.cases (hrows 731) (Fin.cases (hrows 674) (fun i => Fin.elim0 i))))
def support916 : Finset (Fin 154) := {15, 24, 27, 28, 36, 40, 42, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 81, 83, 84, 87, 93, 97, 102, 105, 112}
theorem cut916 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support916, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, support914, support123] ![OmissionResidual.demand 736, 2, 2] ![1, 1, 1]
    support916 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (cut914 holes hbool hrows) (Fin.cases (cut123 holes hbool hrows) (fun i => Fin.elim0 i))))
def support917 : Finset (Fin 154) := {15, 24, 27, 28, 36, 40, 42, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 81, 83, 84, 87, 93, 97, 102, 105, 120}
theorem cut917 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support917, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, support915, support282] ![OmissionResidual.demand 736, 2, 2] ![1, 1, 1]
    support917 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (cut915 holes hbool hrows) (Fin.cases (cut282 holes hbool hrows) (fun i => Fin.elim0 i))))
def support918 : Finset (Fin 154) := {15, 24, 27, 28, 36, 40, 42, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 81, 83, 84, 87, 93, 97, 102, 105, 112, 113}
theorem cut918 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support918, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, support912, support123] ![OmissionResidual.demand 736, 2, 2] ![1, 1, 1]
    support918 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (cut912 holes hbool hrows) (Fin.cases (cut123 holes hbool hrows) (fun i => Fin.elim0 i))))
def support919 : Finset (Fin 154) := {15, 24, 27, 28, 36, 40, 42, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 81, 83, 84, 87, 93, 97, 102, 105, 113, 120}
theorem cut919 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support919, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, support913, support282] ![OmissionResidual.demand 736, 2, 2] ![1, 1, 1]
    support919 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (cut913 holes hbool hrows) (Fin.cases (cut282 holes hbool hrows) (fun i => Fin.elim0 i))))
def support920 : Finset (Fin 154) := {15, 24, 27, 28, 36, 40, 42, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 81, 83, 84, 87, 93, 97, 102, 105, 112, 120}
theorem cut920 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support920, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, support914, support282] ![OmissionResidual.demand 736, 2, 2] ![1, 1, 1]
    support920 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (cut914 holes hbool hrows) (Fin.cases (cut282 holes hbool hrows) (fun i => Fin.elim0 i))))
def support921 : Finset (Fin 154) := {15, 24, 27, 28, 36, 40, 42, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 81, 83, 84, 87, 93, 97, 102, 105, 112, 113, 120}
theorem cut921 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support921, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 736, support912, support282] ![OmissionResidual.demand 736, 2, 2] ![1, 1, 1]
    support921 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 736) (Fin.cases (cut912 holes hbool hrows) (Fin.cases (cut282 holes hbool hrows) (fun i => Fin.elim0 i))))
def support922 : Finset (Fin 154) := {2, 7, 16, 24, 25, 26, 31, 34, 36, 40, 49, 51, 63, 64, 68, 90}
theorem cut922 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support922, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 13, OmissionResidual.support 472, OmissionResidual.support 203] ![OmissionResidual.demand 13, OmissionResidual.demand 472, OmissionResidual.demand 203] ![1, 1, 1]
    support922 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 13) (Fin.cases (hrows 472) (Fin.cases (hrows 203) (fun i => Fin.elim0 i))))
def support923 : Finset (Fin 154) := {5, 12, 16, 24, 25, 26, 31, 34, 36, 40, 49, 51, 63, 64, 68, 90}
theorem cut923 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support923, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 33, OmissionResidual.support 483, OmissionResidual.support 203] ![OmissionResidual.demand 33, OmissionResidual.demand 483, OmissionResidual.demand 203] ![1, 1, 1]
    support923 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 33) (Fin.cases (hrows 483) (Fin.cases (hrows 203) (fun i => Fin.elim0 i))))
def support924 : Finset (Fin 154) := {15, 24, 27, 28, 36, 40, 42, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 83, 84, 87, 92, 93, 97, 102, 112, 113}
theorem cut924 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support924, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 737, support912, support161] ![OmissionResidual.demand 737, 2, 2] ![1, 1, 1]
    support924 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 737) (Fin.cases (cut912 holes hbool hrows) (Fin.cases (cut161 holes hbool hrows) (fun i => Fin.elim0 i))))
def support925 : Finset (Fin 154) := {15, 24, 27, 28, 36, 40, 42, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 83, 84, 87, 92, 93, 97, 102, 113, 120}
theorem cut925 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support925, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 737, support913, support372] ![OmissionResidual.demand 737, 2, 2] ![1, 1, 1]
    support925 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 737) (Fin.cases (cut913 holes hbool hrows) (Fin.cases (cut372 holes hbool hrows) (fun i => Fin.elim0 i))))
#print axioms cut925
def support926 : Finset (Fin 154) := {15, 24, 27, 28, 36, 40, 42, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 83, 84, 87, 92, 93, 97, 102, 105, 112, 113}
theorem cut926 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support926, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 737, support914, support161] ![OmissionResidual.demand 737, 2, 2] ![1, 1, 1]
    support926 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 737) (Fin.cases (cut914 holes hbool hrows) (Fin.cases (cut161 holes hbool hrows) (fun i => Fin.elim0 i))))
def support927 : Finset (Fin 154) := {15, 24, 27, 28, 36, 40, 42, 46, 48, 49, 51, 58, 59, 61, 63, 64, 69, 73, 80, 83, 84, 87, 92, 93, 97, 102, 105, 113, 120}
theorem cut927 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support927, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 737, support915, support372] ![OmissionResidual.demand 737, 2, 2] ![1, 1, 1]
    support927 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 737) (Fin.cases (cut915 holes hbool hrows) (Fin.cases (cut372 holes hbool hrows) (fun i => Fin.elim0 i))))
def support928 : Finset (Fin 154) := {24, 39, 49, 56, 60, 70, 72, 75, 78, 81, 82, 87, 93, 99, 103, 116, 123}
theorem cut928 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support928, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 211, OmissionResidual.support 784, OmissionResidual.support 816] ![OmissionResidual.demand 211, OmissionResidual.demand 784, OmissionResidual.demand 816] ![1, 1, 1]
    support928 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 211) (Fin.cases (hrows 784) (Fin.cases (hrows 816) (fun i => Fin.elim0 i))))
def support929 : Finset (Fin 154) := {31, 39, 44, 59, 63, 70, 72, 78, 79, 81, 82, 90, 93, 100, 107, 115}
theorem cut929 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support929, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 920, OmissionResidual.support 922, OmissionResidual.support 799] ![OmissionResidual.demand 920, OmissionResidual.demand 922, OmissionResidual.demand 799] ![1, 1, 1]
    support929 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 920) (Fin.cases (hrows 922) (Fin.cases (hrows 799) (fun i => Fin.elim0 i))))
def support930 : Finset (Fin 154) := {5, 12, 16, 26, 32, 38, 47, 51, 57, 60, 66, 69, 70, 78, 81, 88, 93, 105}
theorem cut930 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support930, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 947, OmissionResidual.support 485, OmissionResidual.support 927] ![OmissionResidual.demand 947, OmissionResidual.demand 485, OmissionResidual.demand 927] ![1, 1, 1]
    support930 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 947) (Fin.cases (hrows 485) (Fin.cases (hrows 927) (fun i => Fin.elim0 i))))
def support931 : Finset (Fin 154) := {24, 39, 49, 56, 60, 70, 72, 75, 78, 82, 87, 92, 99, 102, 112, 116, 129}
theorem cut931 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support931, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 211, OmissionResidual.support 817, OmissionResidual.support 785] ![OmissionResidual.demand 211, OmissionResidual.demand 817, OmissionResidual.demand 785] ![1, 1, 1]
    support931 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 211) (Fin.cases (hrows 817) (Fin.cases (hrows 785) (fun i => Fin.elim0 i))))
def support932 : Finset (Fin 154) := {24, 39, 49, 60, 63, 68, 70, 72, 75, 78, 81, 82, 90, 93, 99, 103, 116, 123}
theorem cut932 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support932, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 784, OmissionResidual.support 418, OmissionResidual.support 213] ![OmissionResidual.demand 784, OmissionResidual.demand 418, OmissionResidual.demand 213] ![1, 1, 1]
    support932 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 784) (Fin.cases (hrows 418) (Fin.cases (hrows 213) (fun i => Fin.elim0 i))))
def support933 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 99, 103, 106, 107, 112, 114, 116, 118, 120, 121, 122, 123, 124, 128, 129, 130, 132, 134, 135, 138, 140, 143, 144, 149, 150, 153}
theorem cut933 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support933, holes i := by
  apply rounded_cover_cut ![support860, OmissionResidual.support 1128, support835] ![4, OmissionResidual.demand 1128, 4] ![1, 1, 1]
    support933 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (cut860 holes hbool hrows) (Fin.cases (hrows 1128) (Fin.cases (cut835 holes hbool hrows) (fun i => Fin.elim0 i))))
def support934 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 99, 103, 106, 107, 112, 114, 116, 118, 120, 121, 122, 123, 124, 128, 129, 130, 132, 134, 135, 138, 140, 143, 144, 149, 150, 152}
theorem cut934 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support934, holes i := by
  apply rounded_cover_cut ![support860, OmissionResidual.support 1128, support839] ![4, OmissionResidual.demand 1128, 4] ![1, 1, 1]
    support934 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (cut860 holes hbool hrows) (Fin.cases (hrows 1128) (Fin.cases (cut839 holes hbool hrows) (fun i => Fin.elim0 i))))
def support935 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 99, 103, 106, 107, 112, 114, 116, 118, 120, 121, 122, 123, 124, 128, 129, 130, 132, 134, 135, 138, 140, 143, 144, 148, 149, 153}
theorem cut935 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support935, holes i := by
  apply rounded_cover_cut ![support865, OmissionResidual.support 1128, support836] ![4, OmissionResidual.demand 1128, 4] ![1, 1, 1]
    support935 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (cut865 holes hbool hrows) (Fin.cases (hrows 1128) (Fin.cases (cut836 holes hbool hrows) (fun i => Fin.elim0 i))))
def support936 : Finset (Fin 154) := {61, 71, 76, 81, 88, 92, 94, 98, 99, 103, 106, 107, 112, 114, 116, 118, 120, 121, 122, 123, 124, 128, 129, 130, 132, 134, 135, 138, 140, 143, 144, 148, 149, 152}
theorem cut936 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support936, holes i := by
  apply rounded_cover_cut ![support865, OmissionResidual.support 1128, support840] ![4, OmissionResidual.demand 1128, 4] ![1, 1, 1]
    support936 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (cut865 holes hbool hrows) (Fin.cases (hrows 1128) (Fin.cases (cut840 holes hbool hrows) (fun i => Fin.elim0 i))))
def support937 : Finset (Fin 154) := {24, 34, 39, 42, 49, 56, 60, 62, 68, 71, 72, 78, 83, 87, 100, 108}
theorem cut937 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support937, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 903, OmissionResidual.support 906, OmissionResidual.support 717] ![OmissionResidual.demand 903, OmissionResidual.demand 906, OmissionResidual.demand 717] ![1, 1, 1]
    support937 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 903) (Fin.cases (hrows 906) (Fin.cases (hrows 717) (fun i => Fin.elim0 i))))
def support938 : Finset (Fin 154) := {24, 39, 42, 49, 56, 60, 62, 68, 71, 72, 78, 83, 87, 100, 108}
theorem cut938 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support938, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 211, OmissionResidual.support 214, OmissionResidual.support 717] ![OmissionResidual.demand 211, OmissionResidual.demand 214, OmissionResidual.demand 717] ![1, 1, 1]
    support938 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 211) (Fin.cases (hrows 214) (Fin.cases (hrows 717) (fun i => Fin.elim0 i))))
def support939 : Finset (Fin 154) := {60, 70, 75, 81, 87, 92, 94, 99, 103, 106, 112, 116, 120, 121, 123, 124, 140}
theorem cut939 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support939, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 842, OmissionResidual.support 784, OmissionResidual.support 781] ![OmissionResidual.demand 842, OmissionResidual.demand 784, OmissionResidual.demand 781] ![1, 1, 1]
    support939 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 842) (Fin.cases (hrows 784) (Fin.cases (hrows 781) (fun i => Fin.elim0 i))))
def support940 : Finset (Fin 154) := {60, 70, 75, 81, 87, 92, 94, 99, 103, 106, 112, 116, 120, 121, 123, 124, 144}
theorem cut940 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support940, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 784, OmissionResidual.support 843, OmissionResidual.support 781] ![OmissionResidual.demand 784, OmissionResidual.demand 843, OmissionResidual.demand 781] ![1, 1, 1]
    support940 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 784) (Fin.cases (hrows 843) (Fin.cases (hrows 781) (fun i => Fin.elim0 i))))
def support941 : Finset (Fin 154) := {26, 35, 64, 69, 75, 81, 85, 86, 95, 104, 118, 121, 126, 129, 132, 141}
theorem cut941 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support941, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1070, OmissionResidual.support 616, OmissionResidual.support 1095] ![OmissionResidual.demand 1070, OmissionResidual.demand 616, OmissionResidual.demand 1095] ![1, 1, 1]
    support941 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1070) (Fin.cases (hrows 616) (Fin.cases (hrows 1095) (fun i => Fin.elim0 i))))
def support942 : Finset (Fin 154) := {5, 12, 16, 26, 32, 38, 47, 51, 57, 60, 66, 70, 78, 80, 88, 92, 102, 113}
theorem cut942 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support942, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 948, OmissionResidual.support 928, OmissionResidual.support 485] ![OmissionResidual.demand 948, OmissionResidual.demand 928, OmissionResidual.demand 485] ![1, 1, 1]
    support942 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 948) (Fin.cases (hrows 928) (Fin.cases (hrows 485) (fun i => Fin.elim0 i))))
def support943 : Finset (Fin 154) := {9, 13, 18, 19, 24, 26, 31, 32, 35, 40, 41, 48, 51, 57, 58, 61, 69, 70, 71, 76, 80, 81, 88, 92, 98, 112, 121}
theorem cut943 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support943, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 529, support202, support431] ![OmissionResidual.demand 529, 3, 3] ![1, 1, 1]
    support943 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 529) (Fin.cases (cut202 holes hbool hrows) (Fin.cases (cut431 holes hbool hrows) (fun i => Fin.elim0 i))))
def support944 : Finset (Fin 154) := {9, 13, 18, 19, 24, 26, 31, 32, 35, 40, 41, 48, 51, 57, 58, 61, 69, 70, 71, 76, 80, 81, 88, 92, 98, 120, 128}
theorem cut944 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support944, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 529, support217, support432] ![OmissionResidual.demand 529, 3, 3] ![1, 1, 1]
    support944 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 529) (Fin.cases (cut217 holes hbool hrows) (Fin.cases (cut432 holes hbool hrows) (fun i => Fin.elim0 i))))
def support945 : Finset (Fin 154) := {60, 70, 71, 75, 81, 86, 92, 99, 102, 103, 108, 116, 120, 122, 123, 134}
theorem cut945 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support945, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 784, OmissionResidual.support 815, OmissionResidual.support 783] ![OmissionResidual.demand 784, OmissionResidual.demand 815, OmissionResidual.demand 783] ![1, 1, 1]
    support945 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 784) (Fin.cases (hrows 815) (Fin.cases (hrows 783) (fun i => Fin.elim0 i))))
def support946 : Finset (Fin 154) := {5, 12, 16, 26, 32, 38, 47, 51, 57, 60, 66, 69, 70, 78, 81, 98, 103, 114}
theorem cut946 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support946, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 485, OmissionResidual.support 949, OmissionResidual.support 929] ![OmissionResidual.demand 485, OmissionResidual.demand 949, OmissionResidual.demand 929] ![1, 1, 1]
    support946 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 485) (Fin.cases (hrows 949) (Fin.cases (hrows 929) (fun i => Fin.elim0 i))))
def support947 : Finset (Fin 154) := {24, 39, 49, 56, 71, 77, 83, 87, 88, 91, 97, 108, 119, 126}
theorem cut947 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support947, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 212, OmissionResidual.support 982, OmissionResidual.support 1035] ![OmissionResidual.demand 212, OmissionResidual.demand 982, OmissionResidual.demand 1035] ![1, 1, 1]
    support947 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 212) (Fin.cases (hrows 982) (Fin.cases (hrows 1035) (fun i => Fin.elim0 i))))
def support948 : Finset (Fin 154) := {22, 29, 32, 37, 38, 41, 42, 45, 47, 48, 52, 56, 58, 73, 84, 88, 94}
theorem cut948 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support948, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 588, OmissionResidual.support 177, OmissionResidual.support 631] ![OmissionResidual.demand 588, OmissionResidual.demand 177, OmissionResidual.demand 631] ![1, 1, 1]
    support948 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 588) (Fin.cases (hrows 177) (Fin.cases (hrows 631) (fun i => Fin.elim0 i))))
def support949 : Finset (Fin 154) := {42, 56, 62, 63, 68, 72, 73, 78, 82, 83, 88, 93, 94, 98, 102, 112, 121, 124}
theorem cut949 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support949, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 343, OmissionResidual.support 421, OmissionResidual.support 438] ![OmissionResidual.demand 343, OmissionResidual.demand 421, OmissionResidual.demand 438] ![1, 1, 1]
    support949 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 343) (Fin.cases (hrows 421) (Fin.cases (hrows 438) (fun i => Fin.elim0 i))))
def support950 : Finset (Fin 154) := {42, 56, 62, 63, 68, 72, 73, 78, 82, 83, 88, 93, 94, 98, 102, 112, 116, 121}
theorem cut950 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support950, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 341, OmissionResidual.support 421, OmissionResidual.support 438] ![OmissionResidual.demand 341, OmissionResidual.demand 421, OmissionResidual.demand 438] ![1, 1, 1]
    support950 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 341) (Fin.cases (hrows 421) (Fin.cases (hrows 438) (fun i => Fin.elim0 i))))
#print axioms cut950
def support951 : Finset (Fin 154) := {99, 107, 115, 118, 122, 123, 124, 129, 130, 135, 138, 140, 142, 143, 144, 149, 152}
theorem cut951 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support951, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1125, OmissionResidual.support 1128, OmissionResidual.support 1159] ![OmissionResidual.demand 1125, OmissionResidual.demand 1128, OmissionResidual.demand 1159] ![1, 1, 1]
    support951 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1125) (Fin.cases (hrows 1128) (Fin.cases (hrows 1159) (fun i => Fin.elim0 i))))
def support952 : Finset (Fin 154) := {99, 107, 115, 118, 122, 123, 124, 129, 130, 135, 138, 140, 142, 143, 144, 149, 153}
theorem cut952 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support952, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1125, OmissionResidual.support 1128, OmissionResidual.support 1160] ![OmissionResidual.demand 1125, OmissionResidual.demand 1128, OmissionResidual.demand 1160] ![1, 1, 1]
    support952 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1125) (Fin.cases (hrows 1128) (Fin.cases (hrows 1160) (fun i => Fin.elim0 i))))
def support953 : Finset (Fin 154) := {42, 56, 62, 68, 71, 72, 81, 83, 86, 92, 93, 94, 97, 102, 103, 106, 108, 112, 116, 120, 121, 124, 134, 140}
theorem cut953 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support953, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 343, support279, support121] ![OmissionResidual.demand 343, 2, 2] ![1, 1, 1]
    support953 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 343) (Fin.cases (cut279 holes hbool hrows) (Fin.cases (cut121 holes hbool hrows) (fun i => Fin.elim0 i))))
def support954 : Finset (Fin 154) := {42, 56, 62, 68, 71, 72, 81, 83, 86, 92, 93, 94, 97, 102, 103, 106, 108, 112, 116, 120, 121, 124, 134, 144}
theorem cut954 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support954, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 343, support401, support121] ![OmissionResidual.demand 343, 2, 2] ![1, 1, 1]
    support954 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 343) (Fin.cases (cut401 holes hbool hrows) (Fin.cases (cut121 holes hbool hrows) (fun i => Fin.elim0 i))))
def support955 : Finset (Fin 154) := {29, 37, 38, 41, 42, 47, 51, 52, 56, 57, 58, 62, 63, 68, 69, 72, 73, 83, 84, 93, 94, 103, 124}
theorem cut955 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support955, holes i := by
  apply rounded_cover_cut ![support53, OmissionResidual.support 343, support525] ![2, OmissionResidual.demand 343, 2] ![1, 1, 1]
    support955 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut53 holes hbool hrows) (Fin.cases (hrows 343) (Fin.cases (cut525 holes hbool hrows) (fun i => Fin.elim0 i))))
def support956 : Finset (Fin 154) := {22, 29, 32, 37, 38, 41, 42, 47, 51, 52, 56, 57, 58, 62, 63, 68, 69, 72, 73, 83, 84, 93, 94, 103, 124}
theorem cut956 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support956, holes i := by
  apply rounded_cover_cut ![support53, OmissionResidual.support 343, support529] ![2, OmissionResidual.demand 343, 2] ![1, 1, 1]
    support956 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut53 holes hbool hrows) (Fin.cases (hrows 343) (Fin.cases (cut529 holes hbool hrows) (fun i => Fin.elim0 i))))
def support957 : Finset (Fin 154) := {29, 37, 41, 42, 47, 52, 56, 58, 62, 68, 72, 73, 83, 84, 94, 124}
theorem cut957 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support957, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 631, OmissionResidual.support 343, OmissionResidual.support 629] ![OmissionResidual.demand 631, OmissionResidual.demand 343, OmissionResidual.demand 629] ![1, 1, 1]
    support957 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 631) (Fin.cases (hrows 343) (Fin.cases (hrows 629) (fun i => Fin.elim0 i))))
def support958 : Finset (Fin 154) := {22, 29, 32, 37, 41, 42, 47, 52, 56, 58, 62, 68, 72, 73, 83, 84, 94, 124}
theorem cut958 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support958, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 588, OmissionResidual.support 343, OmissionResidual.support 629] ![OmissionResidual.demand 588, OmissionResidual.demand 343, OmissionResidual.demand 629] ![1, 1, 1]
    support958 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 588) (Fin.cases (hrows 343) (Fin.cases (hrows 629) (fun i => Fin.elim0 i))))
def support959 : Finset (Fin 154) := {29, 37, 38, 41, 42, 47, 51, 52, 56, 57, 58, 62, 63, 68, 69, 72, 73, 83, 84, 93, 94, 103, 116}
theorem cut959 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support959, holes i := by
  apply rounded_cover_cut ![support53, OmissionResidual.support 341, support525] ![2, OmissionResidual.demand 341, 2] ![1, 1, 1]
    support959 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut53 holes hbool hrows) (Fin.cases (hrows 341) (Fin.cases (cut525 holes hbool hrows) (fun i => Fin.elim0 i))))
def support960 : Finset (Fin 154) := {22, 29, 32, 37, 38, 41, 42, 47, 51, 52, 56, 57, 58, 62, 63, 68, 69, 72, 73, 83, 84, 93, 94, 103, 116}
theorem cut960 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support960, holes i := by
  apply rounded_cover_cut ![support53, OmissionResidual.support 341, support529] ![2, OmissionResidual.demand 341, 2] ![1, 1, 1]
    support960 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut53 holes hbool hrows) (Fin.cases (hrows 341) (Fin.cases (cut529 holes hbool hrows) (fun i => Fin.elim0 i))))
def support961 : Finset (Fin 154) := {29, 37, 41, 42, 47, 52, 56, 58, 62, 68, 72, 73, 83, 84, 94, 116}
theorem cut961 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support961, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 631, OmissionResidual.support 341, OmissionResidual.support 629] ![OmissionResidual.demand 631, OmissionResidual.demand 341, OmissionResidual.demand 629] ![1, 1, 1]
    support961 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 631) (Fin.cases (hrows 341) (Fin.cases (hrows 629) (fun i => Fin.elim0 i))))
def support962 : Finset (Fin 154) := {22, 29, 32, 37, 41, 42, 47, 52, 56, 58, 62, 68, 72, 73, 83, 84, 94, 116}
theorem cut962 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support962, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 588, OmissionResidual.support 341, OmissionResidual.support 629] ![OmissionResidual.demand 588, OmissionResidual.demand 341, OmissionResidual.demand 629] ![1, 1, 1]
    support962 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 588) (Fin.cases (hrows 341) (Fin.cases (hrows 629) (fun i => Fin.elim0 i))))
def support963 : Finset (Fin 154) := {1, 6, 7, 8, 12, 14, 17, 20, 21, 22, 24, 29, 30, 31, 32, 33, 35, 37, 39, 41, 42, 43, 44, 46, 47, 49, 52, 53, 56, 58, 59, 60, 64, 67, 72, 74, 78, 84, 87, 94}
theorem cut963 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support963, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 588, OmissionResidual.support 6, OmissionResidual.support 46, OmissionResidual.support 51, OmissionResidual.support 211, OmissionResidual.support 915, OmissionResidual.support 494, OmissionResidual.support 631] ![OmissionResidual.demand 588, OmissionResidual.demand 6, OmissionResidual.demand 46, OmissionResidual.demand 51, OmissionResidual.demand 211, OmissionResidual.demand 915, OmissionResidual.demand 494, OmissionResidual.demand 631] ![1, 1, 1, 1, 1, 1, 1, 1]
    support963 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 588) (Fin.cases (hrows 6) (Fin.cases (hrows 46) (Fin.cases (hrows 51) (Fin.cases (hrows 211) (Fin.cases (hrows 915) (Fin.cases (hrows 494) (Fin.cases (hrows 631) (fun i => Fin.elim0 i)))))))))
def support964 : Finset (Fin 154) := {13, 18, 26, 35, 44, 55, 58, 69, 71, 76, 81, 86, 95, 104, 126, 128, 132, 134, 145}
theorem cut964 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support964, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 874, OmissionResidual.support 1096, OmissionResidual.support 873] ![OmissionResidual.demand 874, OmissionResidual.demand 1096, OmissionResidual.demand 873] ![1, 1, 1]
    support964 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 874) (Fin.cases (hrows 1096) (Fin.cases (hrows 873) (fun i => Fin.elim0 i))))
def support965 : Finset (Fin 154) := {7, 35, 40, 43, 46, 49, 53, 59, 64, 74, 78, 88, 92, 102, 104, 113, 118, 122, 126, 136}
theorem cut965 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support965, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 313, OmissionResidual.support 494, OmissionResidual.support 1043] ![OmissionResidual.demand 313, OmissionResidual.demand 494, OmissionResidual.demand 1043] ![1, 1, 1]
    support965 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 313) (Fin.cases (hrows 494) (Fin.cases (hrows 1043) (fun i => Fin.elim0 i))))
def support966 : Finset (Fin 154) := {12, 35, 40, 43, 46, 49, 53, 59, 64, 74, 78, 88, 92, 102, 104, 113, 118, 122, 126, 136}
theorem cut966 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support966, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 313, OmissionResidual.support 526, OmissionResidual.support 1043] ![OmissionResidual.demand 313, OmissionResidual.demand 526, OmissionResidual.demand 1043] ![1, 1, 1]
    support966 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 313) (Fin.cases (hrows 526) (Fin.cases (hrows 1043) (fun i => Fin.elim0 i))))
def support967 : Finset (Fin 154) := {90, 99, 107, 111, 119, 122, 126, 129, 131, 133, 135, 136, 139, 141, 146, 149}
theorem cut967 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support967, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1157, OmissionResidual.support 1113, OmissionResidual.support 1114] ![OmissionResidual.demand 1157, OmissionResidual.demand 1113, OmissionResidual.demand 1114] ![1, 1, 1]
    support967 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1157) (Fin.cases (hrows 1113) (Fin.cases (hrows 1114) (fun i => Fin.elim0 i))))
def support968 : Finset (Fin 154) := {8, 12, 33, 35, 38, 41, 47, 50, 55, 57, 66, 69, 70, 78, 81, 85, 88, 93, 105}
theorem cut968 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support968, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 862, OmissionResidual.support 927, OmissionResidual.support 325] ![OmissionResidual.demand 862, OmissionResidual.demand 927, OmissionResidual.demand 325] ![1, 1, 1]
    support968 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 862) (Fin.cases (hrows 927) (Fin.cases (hrows 325) (fun i => Fin.elim0 i))))
def support969 : Finset (Fin 154) := {42, 56, 62, 68, 71, 72, 81, 83, 86, 92, 94, 100, 108, 116, 120, 134}
theorem cut969 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support969, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 815, OmissionResidual.support 341, OmissionResidual.support 717] ![OmissionResidual.demand 815, OmissionResidual.demand 341, OmissionResidual.demand 717] ![1, 1, 1]
    support969 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 815) (Fin.cases (hrows 341) (Fin.cases (hrows 717) (fun i => Fin.elim0 i))))
def support970 : Finset (Fin 154) := {8, 12, 23, 35, 37, 41, 50, 51, 57, 65, 69, 70, 77, 81, 103, 106, 114}
theorem cut970 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support970, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 741, OmissionResidual.support 498, OmissionResidual.support 677] ![OmissionResidual.demand 741, OmissionResidual.demand 498, OmissionResidual.demand 677] ![1, 1, 1]
    support970 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 741) (Fin.cases (hrows 498) (Fin.cases (hrows 677) (fun i => Fin.elim0 i))))
def support971 : Finset (Fin 154) := {8, 12, 23, 29, 35, 37, 41, 50, 51, 55, 57, 67, 69, 70, 81, 88, 93, 105}
theorem cut971 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support971, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 498, OmissionResidual.support 936, OmissionResidual.support 912] ![OmissionResidual.demand 498, OmissionResidual.demand 936, OmissionResidual.demand 912] ![1, 1, 1]
    support971 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 498) (Fin.cases (hrows 936) (Fin.cases (hrows 912) (fun i => Fin.elim0 i))))
def support972 : Finset (Fin 154) := {8, 12, 33, 35, 38, 41, 47, 50, 55, 57, 66, 69, 70, 78, 81, 85, 98, 103, 114}
theorem cut972 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support972, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 862, OmissionResidual.support 929, OmissionResidual.support 327] ![OmissionResidual.demand 862, OmissionResidual.demand 929, OmissionResidual.demand 327] ![1, 1, 1]
    support972 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 862) (Fin.cases (hrows 929) (Fin.cases (hrows 327) (fun i => Fin.elim0 i))))
def support973 : Finset (Fin 154) := {38, 47, 51, 57, 63, 69, 80, 84, 94, 103, 106, 112, 116, 120, 124, 144}
theorem cut973 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support973, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 843, OmissionResidual.support 680, OmissionResidual.support 681] ![OmissionResidual.demand 843, OmissionResidual.demand 680, OmissionResidual.demand 681] ![1, 1, 1]
    support973 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 843) (Fin.cases (hrows 680) (Fin.cases (hrows 681) (fun i => Fin.elim0 i))))
def support974 : Finset (Fin 154) := {38, 47, 51, 57, 63, 69, 80, 84, 94, 103, 106, 112, 116, 120, 124, 140}
theorem cut974 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support974, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 680, OmissionResidual.support 681, OmissionResidual.support 842] ![OmissionResidual.demand 680, OmissionResidual.demand 681, OmissionResidual.demand 842] ![1, 1, 1]
    support974 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 680) (Fin.cases (hrows 681) (Fin.cases (hrows 842) (fun i => Fin.elim0 i))))
def support975 : Finset (Fin 154) := {8, 12, 23, 35, 38, 41, 47, 51, 57, 60, 66, 70, 78, 80, 88, 92, 102, 113}
theorem cut975 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support975, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 948, OmissionResidual.support 498, OmissionResidual.support 928] ![OmissionResidual.demand 948, OmissionResidual.demand 498, OmissionResidual.demand 928] ![1, 1, 1]
    support975 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 948) (Fin.cases (hrows 498) (Fin.cases (hrows 928) (fun i => Fin.elim0 i))))
#print axioms cut975
def support976 : Finset (Fin 154) := {8, 12, 23, 35, 38, 41, 47, 51, 57, 60, 66, 69, 70, 78, 81, 88, 93, 105}
theorem cut976 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support976, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 947, OmissionResidual.support 498, OmissionResidual.support 927] ![OmissionResidual.demand 947, OmissionResidual.demand 498, OmissionResidual.demand 927] ![1, 1, 1]
    support976 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 947) (Fin.cases (hrows 498) (Fin.cases (hrows 927) (fun i => Fin.elim0 i))))
def support977 : Finset (Fin 154) := {24, 39, 42, 49, 56, 62, 68, 71, 72, 81, 83, 86, 92, 94, 100, 108, 116, 120, 134}
theorem cut977 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support977, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 815, OmissionResidual.support 341, OmissionResidual.support 214] ![OmissionResidual.demand 815, OmissionResidual.demand 341, OmissionResidual.demand 214] ![1, 1, 1]
    support977 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 815) (Fin.cases (hrows 341) (Fin.cases (hrows 214) (fun i => Fin.elim0 i))))
def support978 : Finset (Fin 154) := {8, 12, 23, 29, 35, 37, 41, 50, 51, 55, 57, 67, 69, 70, 81, 98, 103, 114}
theorem cut978 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support978, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 498, OmissionResidual.support 938, OmissionResidual.support 914] ![OmissionResidual.demand 498, OmissionResidual.demand 938, OmissionResidual.demand 914] ![1, 1, 1]
    support978 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 498) (Fin.cases (hrows 938) (Fin.cases (hrows 914) (fun i => Fin.elim0 i))))
def support979 : Finset (Fin 154) := {24, 34, 39, 49, 53, 56, 64, 71, 83, 86, 88, 91, 97, 108, 119, 126}
theorem cut979 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support979, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 904, OmissionResidual.support 996, OmissionResidual.support 982] ![OmissionResidual.demand 904, OmissionResidual.demand 996, OmissionResidual.demand 982] ![1, 1, 1]
    support979 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 904) (Fin.cases (hrows 996) (Fin.cases (hrows 982) (fun i => Fin.elim0 i))))
def support980 : Finset (Fin 154) := {24, 39, 49, 56, 71, 81, 83, 86, 88, 92, 93, 97, 102, 108, 116, 120, 134}
theorem cut980 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support980, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 212, OmissionResidual.support 815, OmissionResidual.support 833] ![OmissionResidual.demand 212, OmissionResidual.demand 815, OmissionResidual.demand 833] ![1, 1, 1]
    support980 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 212) (Fin.cases (hrows 815) (Fin.cases (hrows 833) (fun i => Fin.elim0 i))))
def support981 : Finset (Fin 154) := {31, 39, 41, 44, 50, 55, 59, 70, 78, 79, 81, 82, 93, 96, 100, 115}
theorem cut981 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support981, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 940, OmissionResidual.support 922, OmissionResidual.support 250] ![OmissionResidual.demand 940, OmissionResidual.demand 922, OmissionResidual.demand 250] ![1, 1, 1]
    support981 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 940) (Fin.cases (hrows 922) (Fin.cases (hrows 250) (fun i => Fin.elim0 i))))
def support982 : Finset (Fin 154) := {31, 39, 44, 51, 59, 60, 70, 79, 81, 82, 90, 93, 100, 107, 115}
theorem cut982 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support982, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 920, OmissionResidual.support 922, OmissionResidual.support 379] ![OmissionResidual.demand 920, OmissionResidual.demand 922, OmissionResidual.demand 379] ![1, 1, 1]
    support982 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 920) (Fin.cases (hrows 922) (Fin.cases (hrows 379) (fun i => Fin.elim0 i))))
def support983 : Finset (Fin 154) := {8, 12, 23, 35, 38, 41, 47, 51, 57, 60, 66, 69, 70, 78, 81, 98, 103, 114}
theorem cut983 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support983, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 498, OmissionResidual.support 949, OmissionResidual.support 929] ![OmissionResidual.demand 498, OmissionResidual.demand 949, OmissionResidual.demand 929] ![1, 1, 1]
    support983 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 498) (Fin.cases (hrows 949) (Fin.cases (hrows 929) (fun i => Fin.elim0 i))))
def support984 : Finset (Fin 154) := {61, 71, 76, 81, 86, 88, 92, 95, 98, 104, 119, 120, 127, 128, 134, 145}
theorem cut984 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support984, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1073, OmissionResidual.support 960, OmissionResidual.support 1037] ![OmissionResidual.demand 1073, OmissionResidual.demand 960, OmissionResidual.demand 1037] ![1, 1, 1]
    support984 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1073) (Fin.cases (hrows 960) (Fin.cases (hrows 1037) (fun i => Fin.elim0 i))))
def support985 : Finset (Fin 154) := {31, 39, 40, 41, 44, 49, 50, 55, 59, 70, 79, 81, 82, 90, 93, 100, 107, 115}
theorem cut985 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support985, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 920, OmissionResidual.support 940, OmissionResidual.support 314] ![OmissionResidual.demand 920, OmissionResidual.demand 940, OmissionResidual.demand 314] ![1, 1, 1]
    support985 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 920) (Fin.cases (hrows 940) (Fin.cases (hrows 314) (fun i => Fin.elim0 i))))
def support986 : Finset (Fin 154) := {31, 39, 41, 44, 50, 55, 59, 70, 79, 81, 82, 90, 93, 100, 107, 115}
theorem cut986 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support986, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 920, OmissionResidual.support 940, OmissionResidual.support 260] ![OmissionResidual.demand 920, OmissionResidual.demand 940, OmissionResidual.demand 260] ![1, 1, 1]
    support986 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 920) (Fin.cases (hrows 940) (Fin.cases (hrows 260) (fun i => Fin.elim0 i))))
def support987 : Finset (Fin 154) := {42, 56, 60, 62, 68, 70, 72, 75, 81, 82, 83, 87, 92, 93, 94, 99, 103, 106, 112, 116, 120, 121, 123, 124, 144}
theorem cut987 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support987, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 343, support940, support73] ![OmissionResidual.demand 343, 2, 2] ![1, 1, 1]
    support987 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 343) (Fin.cases (cut940 holes hbool hrows) (Fin.cases (cut73 holes hbool hrows) (fun i => Fin.elim0 i))))
def support988 : Finset (Fin 154) := {31, 39, 41, 44, 50, 53, 55, 59, 70, 79, 81, 82, 89, 93, 99, 100, 107, 115}
theorem cut988 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support988, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 940, OmissionResidual.support 922, OmissionResidual.support 692] ![OmissionResidual.demand 940, OmissionResidual.demand 922, OmissionResidual.demand 692] ![1, 1, 1]
    support988 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 940) (Fin.cases (hrows 922) (Fin.cases (hrows 692) (fun i => Fin.elim0 i))))
def support989 : Finset (Fin 154) := {42, 56, 60, 62, 68, 70, 72, 75, 81, 82, 83, 87, 92, 93, 94, 99, 103, 106, 112, 116, 120, 121, 123, 124, 140}
theorem cut989 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support989, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 343, support939, support73] ![OmissionResidual.demand 343, 2, 2] ![1, 1, 1]
    support989 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 343) (Fin.cases (cut939 holes hbool hrows) (Fin.cases (cut73 holes hbool hrows) (fun i => Fin.elim0 i))))
def support990 : Finset (Fin 154) := {31, 39, 44, 51, 59, 60, 67, 70, 78, 81, 82, 88, 93, 96, 105}
theorem cut990 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support990, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 918, OmissionResidual.support 916, OmissionResidual.support 375] ![OmissionResidual.demand 918, OmissionResidual.demand 916, OmissionResidual.demand 375] ![1, 1, 1]
    support990 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 918) (Fin.cases (hrows 916) (Fin.cases (hrows 375) (fun i => Fin.elim0 i))))
def support991 : Finset (Fin 154) := {12, 35, 38, 43, 47, 51, 57, 60, 65, 66, 69, 70, 75, 78, 81, 85, 88, 93, 105}
theorem cut991 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support991, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 947, OmissionResidual.support 927, OmissionResidual.support 527] ![OmissionResidual.demand 947, OmissionResidual.demand 927, OmissionResidual.demand 527] ![1, 1, 1]
    support991 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 947) (Fin.cases (hrows 927) (Fin.cases (hrows 527) (fun i => Fin.elim0 i))))
def support992 : Finset (Fin 154) := {12, 35, 38, 43, 47, 51, 57, 60, 65, 66, 70, 75, 78, 80, 85, 88, 92, 102, 113}
theorem cut992 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support992, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 948, OmissionResidual.support 928, OmissionResidual.support 527] ![OmissionResidual.demand 948, OmissionResidual.demand 928, OmissionResidual.demand 527] ![1, 1, 1]
    support992 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 948) (Fin.cases (hrows 928) (Fin.cases (hrows 527) (fun i => Fin.elim0 i))))
def support993 : Finset (Fin 154) := {8, 12, 23, 29, 35, 37, 41, 50, 51, 55, 57, 69, 70, 81, 88, 93, 105}
theorem cut993 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support993, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 498, OmissionResidual.support 325, OmissionResidual.support 238] ![OmissionResidual.demand 498, OmissionResidual.demand 325, OmissionResidual.demand 238] ![1, 1, 1]
    support993 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 498) (Fin.cases (hrows 325) (Fin.cases (hrows 238) (fun i => Fin.elim0 i))))
def support994 : Finset (Fin 154) := {31, 32, 39, 44, 49, 50, 56, 60, 67, 71, 72, 78, 83, 87, 88, 97}
theorem cut994 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support994, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 915, OmissionResidual.support 917, OmissionResidual.support 281] ![OmissionResidual.demand 915, OmissionResidual.demand 917, OmissionResidual.demand 281] ![1, 1, 1]
    support994 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 915) (Fin.cases (hrows 917) (Fin.cases (hrows 281) (fun i => Fin.elim0 i))))
def support995 : Finset (Fin 154) := {8, 12, 33, 35, 38, 41, 47, 50, 55, 57, 69, 70, 78, 81, 85, 88, 93, 105}
theorem cut995 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support995, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 56, OmissionResidual.support 325, OmissionResidual.support 298] ![OmissionResidual.demand 56, OmissionResidual.demand 325, OmissionResidual.demand 298] ![1, 1, 1]
    support995 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 56) (Fin.cases (hrows 325) (Fin.cases (hrows 298) (fun i => Fin.elim0 i))))
def support996 : Finset (Fin 154) := {31, 39, 40, 41, 44, 49, 50, 55, 59, 67, 70, 78, 81, 82, 88, 93, 96, 105}
theorem cut996 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support996, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 312, OmissionResidual.support 936, OmissionResidual.support 916] ![OmissionResidual.demand 312, OmissionResidual.demand 936, OmissionResidual.demand 916] ![1, 1, 1]
    support996 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 312) (Fin.cases (hrows 936) (Fin.cases (hrows 916) (fun i => Fin.elim0 i))))
def support997 : Finset (Fin 154) := {31, 39, 41, 44, 50, 55, 59, 67, 70, 78, 81, 82, 88, 93, 96, 105}
theorem cut997 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support997, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 936, OmissionResidual.support 916, OmissionResidual.support 256] ![OmissionResidual.demand 936, OmissionResidual.demand 916, OmissionResidual.demand 256] ![1, 1, 1]
    support997 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 936) (Fin.cases (hrows 916) (Fin.cases (hrows 256) (fun i => Fin.elim0 i))))
def support998 : Finset (Fin 154) := {42, 56, 60, 62, 68, 70, 72, 75, 81, 82, 83, 87, 92, 94, 99, 102, 103, 106, 112, 116, 120, 121, 123, 124, 129, 144}
theorem cut998 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support998, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 343, support940, support166] ![OmissionResidual.demand 343, 2, 2] ![1, 1, 1]
    support998 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 343) (Fin.cases (cut940 holes hbool hrows) (Fin.cases (cut166 holes hbool hrows) (fun i => Fin.elim0 i))))
def support999 : Finset (Fin 154) := {12, 29, 35, 37, 41, 43, 50, 55, 57, 65, 67, 69, 70, 75, 81, 85, 88, 93, 105}
theorem cut999 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support999, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 936, OmissionResidual.support 527, OmissionResidual.support 912] ![OmissionResidual.demand 936, OmissionResidual.demand 527, OmissionResidual.demand 912] ![1, 1, 1]
    support999 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 936) (Fin.cases (hrows 527) (Fin.cases (hrows 912) (fun i => Fin.elim0 i))))
def support1000 : Finset (Fin 154) := {8, 12, 23, 35, 41, 47, 51, 57, 60, 69, 70, 75, 81, 87, 103, 106, 114}
theorem cut1000 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1000, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 498, OmissionResidual.support 780, OmissionResidual.support 728] ![OmissionResidual.demand 498, OmissionResidual.demand 780, OmissionResidual.demand 728] ![1, 1, 1]
    support1000 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 498) (Fin.cases (hrows 780) (Fin.cases (hrows 728) (fun i => Fin.elim0 i))))
#print axioms cut1000
def support1001 : Finset (Fin 154) := {42, 56, 60, 62, 68, 70, 72, 75, 81, 82, 83, 87, 92, 94, 99, 102, 103, 106, 112, 116, 120, 121, 123, 124, 129, 140}
theorem cut1001 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1001, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 343, support939, support166] ![OmissionResidual.demand 343, 2, 2] ![1, 1, 1]
    support1001 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 343) (Fin.cases (cut939 holes hbool hrows) (Fin.cases (cut166 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1002 : Finset (Fin 154) := {39, 40, 49, 51, 53, 59, 60, 70, 78, 81, 82, 88, 89, 93, 99, 105, 107}
theorem cut1002 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1002, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 312, OmissionResidual.support 692, OmissionResidual.support 375] ![OmissionResidual.demand 312, OmissionResidual.demand 692, OmissionResidual.demand 375] ![1, 1, 1]
    support1002 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 312) (Fin.cases (hrows 692) (Fin.cases (hrows 375) (fun i => Fin.elim0 i))))
def support1003 : Finset (Fin 154) := {39, 40, 49, 51, 53, 59, 60, 70, 78, 82, 88, 89, 92, 99, 102, 107, 113}
theorem cut1003 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1003, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 313, OmissionResidual.support 692, OmissionResidual.support 376] ![OmissionResidual.demand 313, OmissionResidual.demand 692, OmissionResidual.demand 376] ![1, 1, 1]
    support1003 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 313) (Fin.cases (hrows 692) (Fin.cases (hrows 376) (fun i => Fin.elim0 i))))
def support1004 : Finset (Fin 154) := {42, 56, 62, 68, 71, 72, 81, 83, 86, 92, 94, 100, 108, 112, 116, 129}
theorem cut1004 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1004, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 341, OmissionResidual.support 717, OmissionResidual.support 814] ![OmissionResidual.demand 341, OmissionResidual.demand 717, OmissionResidual.demand 814] ![1, 1, 1]
    support1004 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 341) (Fin.cases (hrows 717) (Fin.cases (hrows 814) (fun i => Fin.elim0 i))))
def support1005 : Finset (Fin 154) := {24, 39, 49, 51, 56, 60, 63, 70, 72, 78, 82, 87, 90, 92, 100, 102, 122}
theorem cut1005 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1005, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 211, OmissionResidual.support 800, OmissionResidual.support 380] ![OmissionResidual.demand 211, OmissionResidual.demand 800, OmissionResidual.demand 380] ![1, 1, 1]
    support1005 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 211) (Fin.cases (hrows 800) (Fin.cases (hrows 380) (fun i => Fin.elim0 i))))
def support1006 : Finset (Fin 154) := {8, 12, 23, 35, 38, 41, 47, 51, 57, 60, 66, 70, 78, 80, 92, 98, 112, 121}
theorem cut1006 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1006, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 498, OmissionResidual.support 950, OmissionResidual.support 930] ![OmissionResidual.demand 498, OmissionResidual.demand 950, OmissionResidual.demand 930] ![1, 1, 1]
    support1006 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 498) (Fin.cases (hrows 950) (Fin.cases (hrows 930) (fun i => Fin.elim0 i))))
def support1007 : Finset (Fin 154) := {24, 34, 39, 49, 53, 64, 68, 71, 83, 86, 91, 97, 100, 108, 119, 126}
theorem cut1007 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1007, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 906, OmissionResidual.support 996, OmissionResidual.support 982] ![OmissionResidual.demand 906, OmissionResidual.demand 996, OmissionResidual.demand 982] ![1, 1, 1]
    support1007 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 906) (Fin.cases (hrows 996) (Fin.cases (hrows 982) (fun i => Fin.elim0 i))))
def support1008 : Finset (Fin 154) := {24, 34, 39, 49, 53, 56, 64, 68, 71, 83, 86, 88, 91, 97, 100, 108, 119, 126}
theorem cut1008 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1008, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 212, OmissionResidual.support 906, OmissionResidual.support 996] ![OmissionResidual.demand 212, OmissionResidual.demand 906, OmissionResidual.demand 996] ![1, 1, 1]
    support1008 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 212) (Fin.cases (hrows 906) (Fin.cases (hrows 996) (fun i => Fin.elim0 i))))
def support1009 : Finset (Fin 154) := {8, 12, 29, 33, 35, 37, 51, 55, 57, 60, 66, 69, 70, 78, 81, 85, 88, 93, 105}
theorem cut1009 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1009, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 947, OmissionResidual.support 862, OmissionResidual.support 238] ![OmissionResidual.demand 947, OmissionResidual.demand 862, OmissionResidual.demand 238] ![1, 1, 1]
    support1009 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 947) (Fin.cases (hrows 862) (Fin.cases (hrows 238) (fun i => Fin.elim0 i))))
def support1010 : Finset (Fin 154) := {8, 12, 33, 35, 37, 50, 55, 57, 65, 69, 70, 77, 81, 85, 103, 106, 114}
theorem cut1010 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1010, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 741, OmissionResidual.support 56, OmissionResidual.support 677] ![OmissionResidual.demand 741, OmissionResidual.demand 56, OmissionResidual.demand 677] ![1, 1, 1]
    support1010 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 741) (Fin.cases (hrows 56) (Fin.cases (hrows 677) (fun i => Fin.elim0 i))))
def support1011 : Finset (Fin 154) := {15, 27, 34, 36, 56, 58, 71, 76, 81, 83, 86, 92, 97, 106, 112, 121}
theorem cut1011 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1011, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 123, OmissionResidual.support 125, OmissionResidual.support 812] ![OmissionResidual.demand 123, OmissionResidual.demand 125, OmissionResidual.demand 812] ![1, 1, 1]
    support1011 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 123) (Fin.cases (hrows 125) (Fin.cases (hrows 812) (fun i => Fin.elim0 i))))
def support1012 : Finset (Fin 154) := {15, 27, 34, 36, 56, 58, 71, 76, 81, 83, 86, 92, 97, 106, 120, 128}
theorem cut1012 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1012, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 123, OmissionResidual.support 125, OmissionResidual.support 813] ![OmissionResidual.demand 123, OmissionResidual.demand 125, OmissionResidual.demand 813] ![1, 1, 1]
    support1012 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 123) (Fin.cases (hrows 125) (Fin.cases (hrows 813) (fun i => Fin.elim0 i))))
def support1013 : Finset (Fin 154) := {9, 15, 18, 26, 27, 34, 36, 56, 58, 71, 76, 81, 83, 86, 92, 97, 106, 112, 121}
theorem cut1013 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1013, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 123, OmissionResidual.support 68, OmissionResidual.support 812] ![OmissionResidual.demand 123, OmissionResidual.demand 68, OmissionResidual.demand 812] ![1, 1, 1]
    support1013 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 123) (Fin.cases (hrows 68) (Fin.cases (hrows 812) (fun i => Fin.elim0 i))))
def support1014 : Finset (Fin 154) := {9, 15, 18, 26, 27, 34, 36, 56, 58, 71, 76, 81, 83, 86, 92, 97, 106, 120, 128}
theorem cut1014 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1014, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 123, OmissionResidual.support 68, OmissionResidual.support 813] ![OmissionResidual.demand 123, OmissionResidual.demand 68, OmissionResidual.demand 813] ![1, 1, 1]
    support1014 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 123) (Fin.cases (hrows 68) (Fin.cases (hrows 813) (fun i => Fin.elim0 i))))
def support1015 : Finset (Fin 154) := {72, 82, 87, 93, 96, 99, 103, 105, 107, 114, 116, 118, 122, 123, 129, 130, 135, 138, 142, 146}
theorem cut1015 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1015, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 816, OmissionResidual.support 1098, OmissionResidual.support 1127] ![OmissionResidual.demand 816, OmissionResidual.demand 1098, OmissionResidual.demand 1127] ![1, 1, 1]
    support1015 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 816) (Fin.cases (hrows 1098) (Fin.cases (hrows 1127) (fun i => Fin.elim0 i))))
def support1016 : Finset (Fin 154) := {72, 82, 87, 93, 96, 99, 103, 105, 107, 114, 118, 122, 124, 129, 130, 135, 138, 142, 146}
theorem cut1016 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1016, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1098, OmissionResidual.support 818, OmissionResidual.support 1127] ![OmissionResidual.demand 1098, OmissionResidual.demand 818, OmissionResidual.demand 1127] ![1, 1, 1]
    support1016 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1098) (Fin.cases (hrows 818) (Fin.cases (hrows 1127) (fun i => Fin.elim0 i))))
def support1017 : Finset (Fin 154) := {27, 30, 43, 46, 53, 57, 59, 65, 70, 75, 77, 82, 85, 87, 96}
theorem cut1017 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1017, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 620, OmissionResidual.support 639, OmissionResidual.support 618] ![OmissionResidual.demand 620, OmissionResidual.demand 639, OmissionResidual.demand 618] ![1, 1, 1]
    support1017 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 620) (Fin.cases (hrows 639) (Fin.cases (hrows 618) (fun i => Fin.elim0 i))))
def support1018 : Finset (Fin 154) := {18, 27, 30, 35, 43, 46, 53, 57, 59, 65, 70, 75, 77, 82, 85, 87, 96}
theorem cut1018 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1018, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 620, OmissionResidual.support 639, OmissionResidual.support 569] ![OmissionResidual.demand 620, OmissionResidual.demand 639, OmissionResidual.demand 569] ![1, 1, 1]
    support1018 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 620) (Fin.cases (hrows 639) (Fin.cases (hrows 569) (fun i => Fin.elim0 i))))
def support1019 : Finset (Fin 154) := {28, 36, 40, 46, 51, 61, 63, 71, 73, 76, 80, 81, 92, 100, 102, 122}
theorem cut1019 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1019, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 623, OmissionResidual.support 625, OmissionResidual.support 409] ![OmissionResidual.demand 623, OmissionResidual.demand 625, OmissionResidual.demand 409] ![1, 1, 1]
    support1019 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 623) (Fin.cases (hrows 625) (Fin.cases (hrows 409) (fun i => Fin.elim0 i))))
def support1020 : Finset (Fin 154) := {19, 26, 28, 35, 36, 40, 46, 51, 61, 63, 71, 73, 76, 80, 81, 92, 100, 102, 122}
theorem cut1020 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1020, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, OmissionResidual.support 625, OmissionResidual.support 409] ![OmissionResidual.demand 572, OmissionResidual.demand 625, OmissionResidual.demand 409] ![1, 1, 1]
    support1020 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (hrows 625) (Fin.cases (hrows 409) (fun i => Fin.elim0 i))))
def support1021 : Finset (Fin 154) := {66, 75, 76, 85, 86, 95, 104, 111, 113, 114, 119, 122, 123, 127, 136, 137}
theorem cut1021 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1021, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1047, OmissionResidual.support 1048, OmissionResidual.support 1071] ![OmissionResidual.demand 1047, OmissionResidual.demand 1048, OmissionResidual.demand 1071] ![1, 1, 1]
    support1021 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1047) (Fin.cases (hrows 1048) (Fin.cases (hrows 1071) (fun i => Fin.elim0 i))))
def support1022 : Finset (Fin 154) := {21, 27, 31, 37, 46, 52, 57, 63, 65, 69, 73, 77, 82, 93, 97, 105}
theorem cut1022 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1022, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 583, OmissionResidual.support 585, OmissionResidual.support 676] ![OmissionResidual.demand 583, OmissionResidual.demand 585, OmissionResidual.demand 676] ![1, 1, 1]
    support1022 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 583) (Fin.cases (hrows 585) (Fin.cases (hrows 676) (fun i => Fin.elim0 i))))
def support1023 : Finset (Fin 154) := {42, 56, 62, 72, 77, 82, 83, 89, 93, 94, 98, 103, 106, 112, 116, 120, 123, 124, 144}
theorem cut1023 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1023, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 344, OmissionResidual.support 797, OmissionResidual.support 843] ![OmissionResidual.demand 344, OmissionResidual.demand 797, OmissionResidual.demand 843] ![1, 1, 1]
    support1023 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 344) (Fin.cases (hrows 797) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
def support1024 : Finset (Fin 154) := {42, 56, 62, 72, 77, 82, 83, 89, 93, 94, 98, 103, 106, 112, 116, 120, 124, 130, 144}
theorem cut1024 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1024, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 344, OmissionResidual.support 798, OmissionResidual.support 843] ![OmissionResidual.demand 344, OmissionResidual.demand 798, OmissionResidual.demand 843] ![1, 1, 1]
    support1024 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 344) (Fin.cases (hrows 798) (Fin.cases (hrows 843) (fun i => Fin.elim0 i))))
def support1025 : Finset (Fin 154) := {42, 56, 62, 72, 77, 82, 83, 89, 93, 94, 98, 103, 106, 112, 116, 120, 123, 124, 140}
theorem cut1025 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1025, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 344, OmissionResidual.support 797, OmissionResidual.support 842] ![OmissionResidual.demand 344, OmissionResidual.demand 797, OmissionResidual.demand 842] ![1, 1, 1]
    support1025 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 344) (Fin.cases (hrows 797) (Fin.cases (hrows 842) (fun i => Fin.elim0 i))))
#print axioms cut1025
def support1026 : Finset (Fin 154) := {42, 56, 62, 72, 77, 82, 83, 89, 93, 94, 98, 103, 106, 112, 116, 120, 124, 130, 140}
theorem cut1026 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1026, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 344, OmissionResidual.support 798, OmissionResidual.support 842] ![OmissionResidual.demand 344, OmissionResidual.demand 798, OmissionResidual.demand 842] ![1, 1, 1]
    support1026 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 344) (Fin.cases (hrows 798) (Fin.cases (hrows 842) (fun i => Fin.elim0 i))))
def support1027 : Finset (Fin 154) := {21, 27, 29, 31, 37, 46, 52, 55, 57, 63, 69, 73, 82, 93, 98, 103, 114}
theorem cut1027 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1027, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 583, OmissionResidual.support 585, OmissionResidual.support 240] ![OmissionResidual.demand 583, OmissionResidual.demand 585, OmissionResidual.demand 240] ![1, 1, 1]
    support1027 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 583) (Fin.cases (hrows 585) (Fin.cases (hrows 240) (fun i => Fin.elim0 i))))
def support1028 : Finset (Fin 154) := {14, 20, 23, 28, 29, 36, 37, 40, 41, 46, 52, 57, 63, 69, 73, 82, 93}
theorem cut1028 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1028, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 542, OmissionResidual.support 624, OmissionResidual.support 630] ![OmissionResidual.demand 542, OmissionResidual.demand 624, OmissionResidual.demand 630] ![1, 1, 1]
    support1028 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 542) (Fin.cases (hrows 624) (Fin.cases (hrows 630) (fun i => Fin.elim0 i))))
def support1029 : Finset (Fin 154) := {14, 20, 23, 28, 29, 36, 37, 40, 41, 46, 52, 57, 63, 69, 73, 82, 84, 93, 103}
theorem cut1029 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1029, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 542, OmissionResidual.support 624, OmissionResidual.support 632] ![OmissionResidual.demand 542, OmissionResidual.demand 624, OmissionResidual.demand 632] ![1, 1, 1]
    support1029 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 542) (Fin.cases (hrows 624) (Fin.cases (hrows 632) (fun i => Fin.elim0 i))))
def support1030 : Finset (Fin 154) := {21, 27, 28, 29, 31, 36, 37, 40, 41, 46, 52, 57, 63, 69, 73, 82, 93}
theorem cut1030 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1030, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 583, OmissionResidual.support 624, OmissionResidual.support 630] ![OmissionResidual.demand 583, OmissionResidual.demand 624, OmissionResidual.demand 630] ![1, 1, 1]
    support1030 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 583) (Fin.cases (hrows 624) (Fin.cases (hrows 630) (fun i => Fin.elim0 i))))
def support1031 : Finset (Fin 154) := {21, 27, 28, 29, 31, 36, 37, 40, 41, 46, 52, 57, 63, 69, 73, 82, 84, 93, 103}
theorem cut1031 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1031, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 583, OmissionResidual.support 624, OmissionResidual.support 632] ![OmissionResidual.demand 583, OmissionResidual.demand 624, OmissionResidual.demand 632] ![1, 1, 1]
    support1031 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 583) (Fin.cases (hrows 624) (Fin.cases (hrows 632) (fun i => Fin.elim0 i))))
def support1032 : Finset (Fin 154) := {27, 29, 37, 41, 46, 52, 53, 57, 69, 73, 77, 82, 87, 93, 96, 97, 105}
theorem cut1032 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1032, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 620, OmissionResidual.support 630, OmissionResidual.support 621] ![OmissionResidual.demand 620, OmissionResidual.demand 630, OmissionResidual.demand 621] ![1, 1, 1]
    support1032 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 620) (Fin.cases (hrows 630) (Fin.cases (hrows 621) (fun i => Fin.elim0 i))))
def support1033 : Finset (Fin 154) := {27, 29, 37, 41, 46, 52, 53, 57, 69, 77, 82, 84, 87, 93, 96, 97, 103, 105}
theorem cut1033 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1033, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 620, OmissionResidual.support 632, OmissionResidual.support 621] ![OmissionResidual.demand 620, OmissionResidual.demand 632, OmissionResidual.demand 621] ![1, 1, 1]
    support1033 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 620) (Fin.cases (hrows 632) (Fin.cases (hrows 621) (fun i => Fin.elim0 i))))
def support1034 : Finset (Fin 154) := {27, 29, 37, 41, 46, 52, 53, 57, 65, 69, 73, 77, 81, 82, 86, 87, 93, 95, 96}
theorem cut1034 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1034, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 620, OmissionResidual.support 630, OmissionResidual.support 619] ![OmissionResidual.demand 620, OmissionResidual.demand 630, OmissionResidual.demand 619] ![1, 1, 1]
    support1034 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 620) (Fin.cases (hrows 630) (Fin.cases (hrows 619) (fun i => Fin.elim0 i))))
def support1035 : Finset (Fin 154) := {27, 29, 37, 41, 46, 52, 53, 57, 65, 69, 77, 81, 82, 84, 86, 87, 95, 96, 103}
theorem cut1035 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1035, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 620, OmissionResidual.support 632, OmissionResidual.support 619] ![OmissionResidual.demand 620, OmissionResidual.demand 632, OmissionResidual.demand 619] ![1, 1, 1]
    support1035 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 620) (Fin.cases (hrows 632) (Fin.cases (hrows 619) (fun i => Fin.elim0 i))))
def support1036 : Finset (Fin 154) := {21, 27, 29, 31, 37, 41, 46, 50, 51, 52, 55, 57, 63, 69, 70, 73, 81, 82, 93, 98, 103, 114}
theorem cut1036 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1036, holes i := by
  apply rounded_cover_cut ![support420, support1027, OmissionResidual.support 327] ![2, 2, OmissionResidual.demand 327] ![1, 1, 1]
    support1036 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut420 holes hbool hrows) (Fin.cases (cut1027 holes hbool hrows) (Fin.cases (hrows 327) (fun i => Fin.elim0 i))))
def support1037 : Finset (Fin 154) := {19, 21, 26, 27, 28, 29, 31, 35, 36, 37, 40, 41, 46, 51, 52, 57, 61, 63, 69, 73, 80, 81, 82, 84, 92, 93, 103}
theorem cut1037 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1037, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 572, support1030, support501] ![OmissionResidual.demand 572, 2, 2] ![1, 1, 1]
    support1037 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 572) (Fin.cases (cut1030 holes hbool hrows) (Fin.cases (cut501 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1038 : Finset (Fin 154) := {77, 96, 105, 110, 114, 116, 123, 129, 130, 132, 134, 137, 138, 142, 144, 150}
theorem cut1038 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1038, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1076, OmissionResidual.support 1075, OmissionResidual.support 1151] ![OmissionResidual.demand 1076, OmissionResidual.demand 1075, OmissionResidual.demand 1151] ![1, 1, 1]
    support1038 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1076) (Fin.cases (hrows 1075) (Fin.cases (hrows 1151) (fun i => Fin.elim0 i))))
def support1039 : Finset (Fin 154) := {0, 1, 3, 5, 6, 7, 11, 12, 16, 17, 18, 19, 20, 23, 25, 26, 27, 28, 30, 32, 35, 36, 37, 41, 43, 46, 50, 53, 54, 59, 64, 66, 74, 76, 80, 92, 104}
theorem cut1039 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support1039, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 526, support349, support679, OmissionResidual.support 888, OmissionResidual.support 908, support673, OmissionResidual.support 490] ![OmissionResidual.demand 526, 3, 2, OmissionResidual.demand 888, OmissionResidual.demand 908, 2, OmissionResidual.demand 490] ![1, 1, 1, 1, 1, 1, 1]
    support1039 3 5 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 526) (Fin.cases (cut349 holes hbool hrows) (Fin.cases (cut679 holes hbool hrows) (Fin.cases (hrows 888) (Fin.cases (hrows 908) (Fin.cases (cut673 holes hbool hrows) (Fin.cases (hrows 490) (fun i => Fin.elim0 i))))))))
def support1040 : Finset (Fin 154) := {5, 6, 8, 10, 11, 12, 13, 14, 15, 16, 18, 20, 23, 24, 26, 27, 31, 32, 35, 36, 37, 40, 41, 42, 47, 49, 51, 52, 60, 61, 62, 69, 81}
theorem cut1040 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1040, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 531, support405, support619] ![OmissionResidual.demand 531, 3, 3] ![1, 1, 1]
    support1040 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 531) (Fin.cases (cut405 holes hbool hrows) (Fin.cases (cut619 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1041 : Finset (Fin 154) := {5, 12, 15, 25, 26, 27, 34, 36, 45, 47, 49, 60, 64, 66, 75}
theorem cut1041 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1041, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 856, OmissionResidual.support 879, OmissionResidual.support 33] ![OmissionResidual.demand 856, OmissionResidual.demand 879, OmissionResidual.demand 33] ![1, 1, 1]
    support1041 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 856) (Fin.cases (hrows 879) (Fin.cases (hrows 33) (fun i => Fin.elim0 i))))
def support1042 : Finset (Fin 154) := {3, 6, 8, 13, 14, 17, 21, 22, 29, 38, 41, 45, 48, 50, 52, 55, 56, 67, 70, 73, 81, 83, 84, 88, 93, 98, 102, 103, 105, 114, 120, 128}
theorem cut1042 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1042, holes i := by
  apply rounded_cover_cut ![support829, support516, OmissionResidual.support 936] ![3, 2, OmissionResidual.demand 936] ![1, 1, 1]
    support1042 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut829 holes hbool hrows) (Fin.cases (cut516 holes hbool hrows) (Fin.cases (hrows 936) (fun i => Fin.elim0 i))))
def support1043 : Finset (Fin 154) := {5, 8, 10, 13, 14, 21, 22, 25, 29, 38, 41, 45, 48, 50, 52, 55, 56, 67, 70, 73, 81, 83, 84, 88, 93, 98, 102, 103, 105, 114, 120, 128}
theorem cut1043 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1043, holes i := by
  apply rounded_cover_cut ![support830, support516, OmissionResidual.support 936] ![3, 2, OmissionResidual.demand 936] ![1, 1, 1]
    support1043 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut830 holes hbool hrows) (Fin.cases (cut516 holes hbool hrows) (Fin.cases (hrows 936) (fun i => Fin.elim0 i))))
def support1044 : Finset (Fin 154) := {2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 23, 24, 26, 27, 31, 32, 35, 36, 37, 40, 41, 42, 47, 49, 51, 52, 60, 61, 62, 69, 81}
theorem cut1044 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1044, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 531, support405, support489] ![OmissionResidual.demand 531, 3, 3] ![1, 1, 1]
    support1044 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 531) (Fin.cases (cut405 holes hbool hrows) (Fin.cases (cut489 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1045 : Finset (Fin 154) := {2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18, 20, 23, 24, 26, 27, 31, 32, 35, 36, 37, 40, 41, 42, 47, 49, 51, 52, 60, 61, 62, 69, 81}
theorem cut1045 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1045, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 531, support489, support619] ![OmissionResidual.demand 531, 3, 3] ![1, 1, 1]
    support1045 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 531) (Fin.cases (cut489 holes hbool hrows) (Fin.cases (cut619 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1046 : Finset (Fin 154) := {3, 6, 8, 13, 14, 17, 21, 22, 29, 38, 41, 45, 48, 50, 52, 55, 56, 67, 70, 73, 81, 83, 84, 88, 93, 98, 102, 103, 105, 112, 114, 121}
theorem cut1046 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1046, holes i := by
  apply rounded_cover_cut ![support829, OmissionResidual.support 936, support517] ![3, OmissionResidual.demand 936, 2] ![1, 1, 1]
    support1046 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut829 holes hbool hrows) (Fin.cases (hrows 936) (Fin.cases (cut517 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1047 : Finset (Fin 154) := {5, 8, 10, 13, 14, 21, 22, 25, 29, 38, 41, 45, 48, 50, 52, 55, 56, 67, 70, 73, 81, 83, 84, 88, 93, 98, 102, 103, 105, 112, 114, 121}
theorem cut1047 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1047, holes i := by
  apply rounded_cover_cut ![support830, OmissionResidual.support 936, support517] ![3, OmissionResidual.demand 936, 2] ![1, 1, 1]
    support1047 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut830 holes hbool hrows) (Fin.cases (hrows 936) (Fin.cases (cut517 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1048 : Finset (Fin 154) := {6, 10, 11, 15, 20, 25, 27, 34, 36, 37, 42, 47, 52, 56, 62, 72, 78, 87}
theorem cut1048 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1048, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 881, OmissionResidual.support 868, OmissionResidual.support 491] ![OmissionResidual.demand 881, OmissionResidual.demand 868, OmissionResidual.demand 491] ![1, 1, 1]
    support1048 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 881) (Fin.cases (hrows 868) (Fin.cases (hrows 491) (fun i => Fin.elim0 i))))
def support1049 : Finset (Fin 154) := {60, 70, 71, 72, 75, 81, 82, 86, 87, 92, 97, 99, 102, 103, 106, 112, 113, 114, 116, 120, 123, 128, 129}
theorem cut1049 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1049, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 813, support79, support118] ![OmissionResidual.demand 813, 2, 2] ![1, 1, 1]
    support1049 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 813) (Fin.cases (cut79 holes hbool hrows) (Fin.cases (cut118 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1050 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 60, 61, 63, 66, 69, 70, 73, 78, 80, 81, 84, 93, 98, 103, 112, 114, 121}
theorem cut1050 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1050, holes i := by
  apply rounded_cover_cut ![support47, OmissionResidual.support 949, support461] ![2, OmissionResidual.demand 949, 3] ![1, 1, 1]
    support1050 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut47 holes hbool hrows) (Fin.cases (hrows 949) (Fin.cases (cut461 holes hbool hrows) (fun i => Fin.elim0 i))))
#print axioms cut1050
def support1051 : Finset (Fin 154) := {38, 47, 48, 51, 57, 58, 60, 61, 63, 66, 69, 70, 71, 73, 78, 80, 81, 84, 86, 92, 93, 97, 98, 102, 103, 106, 112, 114, 120, 121, 128}
theorem cut1051 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support1051, holes i := by
  apply rounded_cover_cut ![support463, support1050, OmissionResidual.support 813] ![4, 4, OmissionResidual.demand 813] ![1, 1, 1]
    support1051 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (cut463 holes hbool hrows) (Fin.cases (cut1050 holes hbool hrows) (Fin.cases (hrows 813) (fun i => Fin.elim0 i))))
def support1052 : Finset (Fin 154) := {5, 8, 9, 10, 13, 14, 15, 18, 21, 25, 26, 28, 29, 34, 38, 41, 44, 45, 55, 56, 58, 63, 71, 76, 78, 86}
theorem cut1052 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1052, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 77, OmissionResidual.support 873, OmissionResidual.support 120, support822] ![OmissionResidual.demand 77, OmissionResidual.demand 873, OmissionResidual.demand 120, 3] ![1, 1, 1, 1]
    support1052 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 77) (Fin.cases (hrows 873) (Fin.cases (hrows 120) (Fin.cases (cut822 holes hbool hrows) (fun i => Fin.elim0 i)))))
def support1053 : Finset (Fin 154) := {63, 72, 82, 84, 93, 94, 102, 103, 111, 112, 120, 127, 133, 141, 142, 150}
theorem cut1053 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1053, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1039, OmissionResidual.support 1094, OmissionResidual.support 1040] ![OmissionResidual.demand 1039, OmissionResidual.demand 1094, OmissionResidual.demand 1040] ![1, 1, 1]
    support1053 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1039) (Fin.cases (hrows 1094) (Fin.cases (hrows 1040) (fun i => Fin.elim0 i))))
def support1054 : Finset (Fin 154) := {63, 72, 82, 84, 93, 94, 102, 103, 111, 112, 120, 127, 133, 141, 142, 148}
theorem cut1054 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1054, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 1039, OmissionResidual.support 1093, OmissionResidual.support 1040] ![OmissionResidual.demand 1039, OmissionResidual.demand 1093, OmissionResidual.demand 1040] ![1, 1, 1]
    support1054 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1039) (Fin.cases (hrows 1093) (Fin.cases (hrows 1040) (fun i => Fin.elim0 i))))
def support1055 : Finset (Fin 154) := {0, 2, 5, 7, 12, 16, 17, 20, 24, 26, 30, 33, 36, 40, 43, 49}
theorem cut1055 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1055, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 472, OmissionResidual.support 483, OmissionResidual.support 2] ![OmissionResidual.demand 472, OmissionResidual.demand 483, OmissionResidual.demand 2] ![1, 1, 1]
    support1055 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 472) (Fin.cases (hrows 483) (Fin.cases (hrows 2) (fun i => Fin.elim0 i))))
def support1056 : Finset (Fin 154) := {1, 2, 5, 7, 12, 16, 17, 20, 24, 26, 30, 33, 36, 40, 43, 49}
theorem cut1056 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1056, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 472, OmissionResidual.support 483, OmissionResidual.support 6] ![OmissionResidual.demand 472, OmissionResidual.demand 483, OmissionResidual.demand 6] ![1, 1, 1]
    support1056 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 472) (Fin.cases (hrows 483) (Fin.cases (hrows 6) (fun i => Fin.elim0 i))))
def support1057 : Finset (Fin 154) := {1, 3, 7, 11, 12, 17, 18, 20, 24, 27, 30, 31, 33, 39, 43}
theorem cut1057 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1057, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 6, OmissionResidual.support 469, OmissionResidual.support 474] ![OmissionResidual.demand 6, OmissionResidual.demand 469, OmissionResidual.demand 474] ![1, 1, 1]
    support1057 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 6) (Fin.cases (hrows 469) (Fin.cases (hrows 474) (fun i => Fin.elim0 i))))
def support1058 : Finset (Fin 154) := {0, 1, 3, 7, 11, 12, 17, 18, 20, 24, 27, 30, 31, 33, 39, 43}
theorem cut1058 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1058, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 2, OmissionResidual.support 469, OmissionResidual.support 474] ![OmissionResidual.demand 2, OmissionResidual.demand 469, OmissionResidual.demand 474] ![1, 1, 1]
    support1058 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (hrows 469) (Fin.cases (hrows 474) (fun i => Fin.elim0 i))))
def support1059 : Finset (Fin 154) := {5, 7, 12, 13, 16, 18, 21, 24, 26, 27, 35, 36, 40, 43, 44, 46, 49, 53, 55, 58, 59, 64, 65, 69, 71, 74, 75, 76, 81, 86, 95}
theorem cut1059 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    5 ≤ ∑ i ∈ support1059, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 483, support869, support775] ![OmissionResidual.demand 483, 4, 4] ![1, 1, 1]
    support1059 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 483) (Fin.cases (cut869 holes hbool hrows) (Fin.cases (cut775 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1060 : Finset (Fin 154) := {0, 2, 5, 7, 12, 16, 17, 18, 20, 24, 27, 30, 31, 33, 39, 43}
theorem cut1060 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1060, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 2, OmissionResidual.support 471, OmissionResidual.support 482] ![OmissionResidual.demand 2, OmissionResidual.demand 471, OmissionResidual.demand 482] ![1, 1, 1]
    support1060 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (hrows 471) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support1061 : Finset (Fin 154) := {1, 2, 5, 7, 12, 16, 17, 18, 20, 24, 27, 30, 31, 33, 39, 43}
theorem cut1061 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1061, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 6, OmissionResidual.support 471, OmissionResidual.support 482] ![OmissionResidual.demand 6, OmissionResidual.demand 471, OmissionResidual.demand 482] ![1, 1, 1]
    support1061 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 6) (Fin.cases (hrows 471) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support1062 : Finset (Fin 154) := {0, 4, 7, 8, 12, 17, 20, 23, 30, 31, 33, 35, 40, 43, 46, 59}
theorem cut1062 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1062, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 2, OmissionResidual.support 479, OmissionResidual.support 496] ![OmissionResidual.demand 2, OmissionResidual.demand 479, OmissionResidual.demand 496] ![1, 1, 1]
    support1062 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (hrows 479) (Fin.cases (hrows 496) (fun i => Fin.elim0 i))))
def support1063 : Finset (Fin 154) := {1, 4, 7, 8, 12, 17, 20, 23, 30, 31, 33, 35, 40, 43, 46, 59}
theorem cut1063 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1063, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 6, OmissionResidual.support 479, OmissionResidual.support 496] ![OmissionResidual.demand 6, OmissionResidual.demand 479, OmissionResidual.demand 496] ![1, 1, 1]
    support1063 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 6) (Fin.cases (hrows 479) (Fin.cases (hrows 496) (fun i => Fin.elim0 i))))
def support1064 : Finset (Fin 154) := {0, 2, 5, 7, 9, 12, 15, 16, 17, 18, 20, 24, 26, 27, 30, 33, 34, 36, 40, 43, 45, 49, 58, 71, 76, 86}
theorem cut1064 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1064, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 2, support526, support527] ![OmissionResidual.demand 2, 3, 3] ![1, 1, 1]
    support1064 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (cut526 holes hbool hrows) (Fin.cases (cut527 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1065 : Finset (Fin 154) := {1, 2, 5, 7, 9, 12, 15, 16, 17, 18, 20, 24, 26, 27, 30, 33, 34, 36, 40, 43, 45, 49, 58, 71, 76, 86}
theorem cut1065 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1065, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 6, support526, support527] ![OmissionResidual.demand 6, 3, 3] ![1, 1, 1]
    support1065 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 6) (Fin.cases (cut526 holes hbool hrows) (Fin.cases (cut527 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1066 : Finset (Fin 154) := {6, 8, 11, 12, 13, 14, 18, 20, 21, 27, 33, 35, 37, 42, 44, 46, 52, 55, 57, 59, 62, 66, 70, 74, 85}
theorem cut1066 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1066, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 491, support467, support744] ![OmissionResidual.demand 491, 3, 3] ![1, 1, 1]
    support1066 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 491) (Fin.cases (cut467 holes hbool hrows) (Fin.cases (cut744 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1067 : Finset (Fin 154) := {1, 5, 7, 11, 12, 16, 17, 18, 20, 24, 27, 30, 31, 33, 39, 43}
theorem cut1067 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1067, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 6, OmissionResidual.support 469, OmissionResidual.support 482] ![OmissionResidual.demand 6, OmissionResidual.demand 469, OmissionResidual.demand 482] ![1, 1, 1]
    support1067 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 6) (Fin.cases (hrows 469) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support1068 : Finset (Fin 154) := {0, 1, 5, 7, 11, 12, 16, 17, 18, 20, 24, 27, 30, 31, 33, 39, 43}
theorem cut1068 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1068, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 2, OmissionResidual.support 469, OmissionResidual.support 482] ![OmissionResidual.demand 2, OmissionResidual.demand 469, OmissionResidual.demand 482] ![1, 1, 1]
    support1068 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (hrows 469) (Fin.cases (hrows 482) (fun i => Fin.elim0 i))))
def support1069 : Finset (Fin 154) := {0, 2, 3, 7, 11, 12, 16, 17, 18, 20, 24, 27, 30, 31, 33, 39, 43}
theorem cut1069 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1069, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 2, OmissionResidual.support 474, OmissionResidual.support 471] ![OmissionResidual.demand 2, OmissionResidual.demand 474, OmissionResidual.demand 471] ![1, 1, 1]
    support1069 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (hrows 474) (Fin.cases (hrows 471) (fun i => Fin.elim0 i))))
def support1070 : Finset (Fin 154) := {1, 2, 3, 7, 11, 12, 16, 17, 18, 20, 24, 27, 30, 31, 33, 39, 43}
theorem cut1070 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1070, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 6, OmissionResidual.support 474, OmissionResidual.support 471] ![OmissionResidual.demand 6, OmissionResidual.demand 474, OmissionResidual.demand 471] ![1, 1, 1]
    support1070 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 6) (Fin.cases (hrows 474) (Fin.cases (hrows 471) (fun i => Fin.elim0 i))))
def support1071 : Finset (Fin 154) := {21, 22, 27, 29, 31, 32, 37, 38, 41, 42, 46, 47, 51, 52, 57, 58, 61, 63, 69, 73, 81, 82, 83, 84, 103}
theorem cut1071 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1071, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 587, support501, support808] ![OmissionResidual.demand 587, 2, 2] ![1, 1, 1]
    support1071 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 587) (Fin.cases (cut501 holes hbool hrows) (Fin.cases (cut808 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1072 : Finset (Fin 154) := {0, 2, 4, 5, 7, 11, 12, 16, 17, 20, 23, 24, 26, 30, 31, 33, 36, 40, 41, 43, 49, 52, 68, 79}
theorem cut1072 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1072, holes i := by
  apply rounded_cover_cut ![support1055, support49, OmissionResidual.support 86] ![2, 2, OmissionResidual.demand 86] ![1, 1, 1]
    support1072 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (cut49 holes hbool hrows) (Fin.cases (hrows 86) (fun i => Fin.elim0 i))))
def support1073 : Finset (Fin 154) := {0, 2, 5, 7, 8, 11, 12, 16, 17, 20, 23, 24, 26, 30, 31, 33, 36, 40, 41, 43, 49, 52, 68, 79}
theorem cut1073 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1073, holes i := by
  apply rounded_cover_cut ![support1055, support51, OmissionResidual.support 86] ![2, 2, OmissionResidual.demand 86] ![1, 1, 1]
    support1073 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (cut51 holes hbool hrows) (Fin.cases (hrows 86) (fun i => Fin.elim0 i))))
def support1074 : Finset (Fin 154) := {1, 2, 4, 5, 7, 11, 12, 16, 17, 20, 23, 24, 26, 30, 31, 33, 36, 40, 41, 43, 49, 52, 68, 79}
theorem cut1074 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1074, holes i := by
  apply rounded_cover_cut ![support1056, support50, OmissionResidual.support 86] ![2, 2, OmissionResidual.demand 86] ![1, 1, 1]
    support1074 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1056 holes hbool hrows) (Fin.cases (cut50 holes hbool hrows) (Fin.cases (hrows 86) (fun i => Fin.elim0 i))))
def support1075 : Finset (Fin 154) := {1, 2, 5, 7, 8, 11, 12, 16, 17, 20, 23, 24, 26, 30, 31, 33, 36, 40, 41, 43, 49, 52, 68, 79}
theorem cut1075 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1075, holes i := by
  apply rounded_cover_cut ![support1056, support52, OmissionResidual.support 86] ![2, 2, OmissionResidual.demand 86] ![1, 1, 1]
    support1075 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1056 holes hbool hrows) (Fin.cases (cut52 holes hbool hrows) (Fin.cases (hrows 86) (fun i => Fin.elim0 i))))
#print axioms cut1075
def support1076 : Finset (Fin 154) := {0, 1, 2, 4, 5, 7, 11, 12, 16, 17, 20, 23, 24, 26, 30, 31, 33, 36, 40, 41, 43, 49, 52, 68, 79}
theorem cut1076 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1076, holes i := by
  apply rounded_cover_cut ![support1055, support50, OmissionResidual.support 86] ![2, 2, OmissionResidual.demand 86] ![1, 1, 1]
    support1076 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (cut50 holes hbool hrows) (Fin.cases (hrows 86) (fun i => Fin.elim0 i))))
def support1077 : Finset (Fin 154) := {0, 1, 2, 5, 7, 8, 11, 12, 16, 17, 20, 23, 24, 26, 30, 31, 33, 36, 40, 41, 43, 49, 52, 68, 79}
theorem cut1077 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1077, holes i := by
  apply rounded_cover_cut ![support1055, support52, OmissionResidual.support 86] ![2, 2, OmissionResidual.demand 86] ![1, 1, 1]
    support1077 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (cut52 holes hbool hrows) (Fin.cases (hrows 86) (fun i => Fin.elim0 i))))
def support1078 : Finset (Fin 154) := {21, 22, 27, 29, 31, 32, 37, 38, 41, 42, 46, 47, 50, 51, 52, 57, 58, 61, 63, 65, 69, 70, 73, 77, 81, 82, 83, 84, 93, 94, 103, 106, 114}
theorem cut1078 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1078, holes i := by
  apply rounded_cover_cut ![support439, support1071, OmissionResidual.support 741] ![3, 3, OmissionResidual.demand 741] ![1, 1, 1]
    support1078 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut439 holes hbool hrows) (Fin.cases (cut1071 holes hbool hrows) (Fin.cases (hrows 741) (fun i => Fin.elim0 i))))
def support1079 : Finset (Fin 154) := {21, 22, 27, 29, 31, 32, 37, 38, 41, 42, 46, 47, 50, 51, 52, 57, 58, 61, 63, 65, 69, 70, 73, 77, 81, 82, 83, 84, 93, 94, 97, 103, 105}
theorem cut1079 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1079, holes i := by
  apply rounded_cover_cut ![support439, support1071, OmissionResidual.support 740] ![3, 3, OmissionResidual.demand 740] ![1, 1, 1]
    support1079 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut439 holes hbool hrows) (Fin.cases (cut1071 holes hbool hrows) (Fin.cases (hrows 740) (fun i => Fin.elim0 i))))
def support1080 : Finset (Fin 154) := {5, 9, 12, 16, 18, 24, 26, 27, 31, 32, 38, 39, 47, 51, 57, 60, 66, 70, 78, 80, 88, 92, 102, 113}
theorem cut1080 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1080, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 482, support942, support603] ![OmissionResidual.demand 482, 3, 3] ![1, 1, 1]
    support1080 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 482) (Fin.cases (cut942 holes hbool hrows) (Fin.cases (cut603 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1081 : Finset (Fin 154) := {0, 1, 2, 4, 5, 7, 11, 12, 13, 16, 17, 20, 21, 23, 24, 26, 30, 31, 33, 34, 36, 40, 43, 44, 49}
theorem cut1081 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1081, holes i := by
  apply rounded_cover_cut ![support1055, OmissionResidual.support 7, support49] ![2, OmissionResidual.demand 7, 2] ![1, 1, 1]
    support1081 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (hrows 7) (Fin.cases (cut49 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1082 : Finset (Fin 154) := {0, 2, 3, 5, 7, 8, 11, 12, 13, 16, 17, 20, 21, 23, 24, 26, 30, 31, 33, 34, 36, 40, 43, 44, 49}
theorem cut1082 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1082, holes i := by
  apply rounded_cover_cut ![support1055, OmissionResidual.support 17, support51] ![2, OmissionResidual.demand 17, 2] ![1, 1, 1]
    support1082 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (hrows 17) (Fin.cases (cut51 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1083 : Finset (Fin 154) := {1, 2, 3, 5, 7, 8, 11, 12, 13, 16, 17, 20, 21, 23, 24, 26, 30, 31, 33, 34, 36, 40, 43, 44, 49}
theorem cut1083 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1083, holes i := by
  apply rounded_cover_cut ![support1056, OmissionResidual.support 17, support52] ![2, OmissionResidual.demand 17, 2] ![1, 1, 1]
    support1083 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1056 holes hbool hrows) (Fin.cases (hrows 17) (Fin.cases (cut52 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1084 : Finset (Fin 154) := {0, 1, 2, 4, 5, 7, 8, 11, 12, 13, 16, 17, 20, 21, 23, 24, 26, 30, 31, 33, 34, 36, 40, 43, 44, 49}
theorem cut1084 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1084, holes i := by
  apply rounded_cover_cut ![support1055, OmissionResidual.support 7, support51] ![2, OmissionResidual.demand 7, 2] ![1, 1, 1]
    support1084 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (hrows 7) (Fin.cases (cut51 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1085 : Finset (Fin 154) := {0, 2, 3, 4, 5, 7, 8, 11, 12, 13, 16, 17, 20, 21, 23, 24, 26, 30, 31, 33, 34, 36, 40, 43, 44, 49}
theorem cut1085 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1085, holes i := by
  apply rounded_cover_cut ![support1055, OmissionResidual.support 17, support49] ![2, OmissionResidual.demand 17, 2] ![1, 1, 1]
    support1085 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (hrows 17) (Fin.cases (cut49 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1086 : Finset (Fin 154) := {0, 1, 2, 3, 5, 7, 8, 11, 12, 13, 16, 17, 20, 21, 23, 24, 26, 30, 31, 33, 34, 36, 40, 43, 44, 49}
theorem cut1086 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1086, holes i := by
  apply rounded_cover_cut ![support1055, OmissionResidual.support 17, support52] ![2, OmissionResidual.demand 17, 2] ![1, 1, 1]
    support1086 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (hrows 17) (Fin.cases (cut52 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1087 : Finset (Fin 154) := {1, 2, 3, 4, 5, 7, 8, 11, 12, 13, 16, 17, 20, 21, 23, 24, 26, 30, 31, 33, 34, 36, 40, 43, 44, 49}
theorem cut1087 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1087, holes i := by
  apply rounded_cover_cut ![support1056, OmissionResidual.support 17, support50] ![2, OmissionResidual.demand 17, 2] ![1, 1, 1]
    support1087 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1056 holes hbool hrows) (Fin.cases (hrows 17) (Fin.cases (cut50 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1088 : Finset (Fin 154) := {0, 1, 2, 3, 4, 5, 7, 8, 11, 12, 13, 16, 17, 20, 21, 23, 24, 26, 30, 31, 33, 34, 36, 40, 43, 44, 49}
theorem cut1088 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1088, holes i := by
  apply rounded_cover_cut ![support1055, OmissionResidual.support 17, support50] ![2, OmissionResidual.demand 17, 2] ![1, 1, 1]
    support1088 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (hrows 17) (Fin.cases (cut50 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1089 : Finset (Fin 154) := {10, 15, 16, 20, 21, 27, 28, 31, 34, 36, 37, 38, 42, 47, 52, 56, 62, 63, 72, 78, 87}
theorem cut1089 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1089, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 120, OmissionResidual.support 881, support192] ![OmissionResidual.demand 120, OmissionResidual.demand 881, 2] ![1, 1, 1]
    support1089 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 120) (Fin.cases (hrows 881) (Fin.cases (cut192 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1090 : Finset (Fin 154) := {3, 5, 9, 11, 12, 16, 18, 24, 26, 27, 31, 32, 38, 39, 47, 51, 57, 60, 66, 70, 78, 80, 88, 92, 102, 113}
theorem cut1090 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1090, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 474, support942, support603] ![OmissionResidual.demand 474, 3, 3] ![1, 1, 1]
    support1090 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 474) (Fin.cases (cut942 holes hbool hrows) (Fin.cases (cut603 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1091 : Finset (Fin 154) := {15, 21, 27, 28, 31, 34, 36, 38, 40, 46, 47, 52, 56, 63, 69, 72, 73, 78, 87, 93}
theorem cut1091 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1091, holes i := by
  apply rounded_cover_cut ![support80, OmissionResidual.support 120, OmissionResidual.support 881] ![2, OmissionResidual.demand 120, OmissionResidual.demand 881] ![1, 1, 1]
    support1091 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut80 holes hbool hrows) (Fin.cases (hrows 120) (Fin.cases (hrows 881) (fun i => Fin.elim0 i))))
def support1092 : Finset (Fin 154) := {2, 7, 16, 24, 26, 35, 36, 40, 46, 48, 49, 58, 61, 64, 69, 73, 75, 80, 81, 84, 86, 92, 95, 104, 120}
theorem cut1092 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1092, holes i := by
  apply rounded_cover_cut ![support455, OmissionResidual.support 731, support546] ![2, OmissionResidual.demand 731, 2] ![1, 1, 1]
    support1092 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut455 holes hbool hrows) (Fin.cases (hrows 731) (Fin.cases (cut546 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1093 : Finset (Fin 154) := {22, 29, 32, 37, 41, 42, 45, 47, 51, 52, 58, 61, 68, 73, 84, 94, 100}
theorem cut1093 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1093, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 273, OmissionResidual.support 588, OmissionResidual.support 631] ![OmissionResidual.demand 273, OmissionResidual.demand 588, OmissionResidual.demand 631] ![1, 1, 1]
    support1093 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 273) (Fin.cases (hrows 588) (Fin.cases (hrows 631) (fun i => Fin.elim0 i))))
def support1094 : Finset (Fin 154) := {63, 72, 73, 78, 82, 83, 88, 90, 93, 100, 102, 109, 112, 115, 129}
theorem cut1094 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1094, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 964, OmissionResidual.support 967, OmissionResidual.support 799] ![OmissionResidual.demand 964, OmissionResidual.demand 967, OmissionResidual.demand 799] ![1, 1, 1]
    support1094 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 964) (Fin.cases (hrows 967) (Fin.cases (hrows 799) (fun i => Fin.elim0 i))))
def support1095 : Finset (Fin 154) := {63, 72, 73, 78, 82, 83, 88, 90, 93, 100, 102, 112, 115, 117, 135}
theorem cut1095 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1095, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 966, OmissionResidual.support 969, OmissionResidual.support 799] ![OmissionResidual.demand 966, OmissionResidual.demand 969, OmissionResidual.demand 799] ![1, 1, 1]
    support1095 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 966) (Fin.cases (hrows 969) (Fin.cases (hrows 799) (fun i => Fin.elim0 i))))
def support1096 : Finset (Fin 154) := {52, 62, 67, 72, 79, 82, 83, 93, 94, 97, 102, 103, 108, 117, 120, 124, 130, 140}
theorem cut1096 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1096, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 958, OmissionResidual.support 957, OmissionResidual.support 835] ![OmissionResidual.demand 958, OmissionResidual.demand 957, OmissionResidual.demand 835] ![1, 1, 1]
    support1096 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 958) (Fin.cases (hrows 957) (Fin.cases (hrows 835) (fun i => Fin.elim0 i))))
def support1097 : Finset (Fin 154) := {1, 7, 9, 11, 18, 21, 24, 26, 27, 31, 32, 39, 41, 44, 46, 47, 51, 57, 59, 60, 67, 70, 78, 82, 96}
theorem cut1097 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1097, holes i := by
  apply rounded_cover_cut ![support486, support284, OmissionResidual.support 506] ![3, 3, OmissionResidual.demand 506] ![1, 1, 1]
    support1097 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut486 holes hbool hrows) (Fin.cases (cut284 holes hbool hrows) (Fin.cases (hrows 506) (fun i => Fin.elim0 i))))
def support1098 : Finset (Fin 154) := {73, 83, 84, 88, 93, 94, 100, 102, 103, 108, 109, 112, 115, 117, 120, 122, 126, 129, 134, 135, 140, 143, 149}
theorem cut1098 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1098, holes i := by
  apply rounded_cover_cut ![support218, OmissionResidual.support 1141, support168] ![3, OmissionResidual.demand 1141, 3] ![1, 1, 1]
    support1098 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut218 holes hbool hrows) (Fin.cases (hrows 1141) (Fin.cases (cut168 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1099 : Finset (Fin 154) := {1, 7, 11, 13, 18, 21, 24, 27, 31, 35, 39, 44, 46, 55, 69, 76, 81, 95}
theorem cut1099 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1099, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 874, OmissionResidual.support 469, OmissionResidual.support 892] ![OmissionResidual.demand 874, OmissionResidual.demand 469, OmissionResidual.demand 892] ![1, 1, 1]
    support1099 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 874) (Fin.cases (hrows 469) (Fin.cases (hrows 892) (fun i => Fin.elim0 i))))
def support1100 : Finset (Fin 154) := {1, 7, 11, 13, 18, 21, 24, 27, 31, 35, 39, 44, 46, 55, 57, 66, 70, 85}
theorem cut1100 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1100, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 469, OmissionResidual.support 872, OmissionResidual.support 890] ![OmissionResidual.demand 469, OmissionResidual.demand 872, OmissionResidual.demand 890] ![1, 1, 1]
    support1100 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 469) (Fin.cases (hrows 872) (Fin.cases (hrows 890) (fun i => Fin.elim0 i))))
#print axioms cut1100
def support1101 : Finset (Fin 154) := {52, 62, 67, 72, 79, 82, 83, 93, 94, 97, 102, 103, 108, 112, 117, 124, 130, 135}
theorem cut1101 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    3 ≤ ∑ i ∈ support1101, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 958, OmissionResidual.support 957, OmissionResidual.support 834] ![OmissionResidual.demand 958, OmissionResidual.demand 957, OmissionResidual.demand 834] ![1, 1, 1]
    support1101 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 958) (Fin.cases (hrows 957) (Fin.cases (hrows 834) (fun i => Fin.elim0 i))))
def support1102 : Finset (Fin 154) := {19, 26, 35, 48, 54, 58, 61, 66, 69, 73, 76, 80, 81, 84, 92, 94, 95, 103, 104, 106, 112, 116, 120, 124, 140}
theorem cut1102 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1102, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 842, support459, support219] ![OmissionResidual.demand 842, 3, 3] ![1, 1, 1]
    support1102 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 842) (Fin.cases (cut459 holes hbool hrows) (Fin.cases (cut219 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1103 : Finset (Fin 154) := {19, 26, 35, 48, 54, 58, 61, 66, 69, 73, 76, 80, 81, 84, 92, 94, 95, 103, 104, 106, 112, 116, 120, 124, 144}
theorem cut1103 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    4 ≤ ∑ i ∈ support1103, holes i := by
  apply rounded_cover_cut ![support459, OmissionResidual.support 843, support219] ![3, OmissionResidual.demand 843, 3] ![1, 1, 1]
    support1103 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut459 holes hbool hrows) (Fin.cases (hrows 843) (Fin.cases (cut219 holes hbool hrows) (fun i => Fin.elim0 i))))
def support1104 : Finset (Fin 154) := {22, 29, 32, 37, 41, 42, 47, 48, 52, 57, 58, 61, 69, 73, 80, 84, 93, 94, 120}
theorem cut1104 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1104, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 588, OmissionResidual.support 731, OmissionResidual.support 630] ![OmissionResidual.demand 588, OmissionResidual.demand 731, OmissionResidual.demand 630] ![1, 1, 1]
    support1104 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 588) (Fin.cases (hrows 731) (Fin.cases (hrows 630) (fun i => Fin.elim0 i))))
def support1105 : Finset (Fin 154) := {29, 37, 41, 47, 48, 52, 57, 58, 61, 69, 73, 80, 84, 93, 94, 120}
theorem cut1105 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1105, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 731, OmissionResidual.support 631, OmissionResidual.support 630] ![OmissionResidual.demand 731, OmissionResidual.demand 631, OmissionResidual.demand 630] ![1, 1, 1]
    support1105 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 731) (Fin.cases (hrows 631) (Fin.cases (hrows 630) (fun i => Fin.elim0 i))))
def support1106 : Finset (Fin 154) := {29, 37, 41, 47, 48, 52, 57, 58, 61, 69, 73, 80, 84, 93, 94, 112}
theorem cut1106 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1106, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 730, OmissionResidual.support 631, OmissionResidual.support 630] ![OmissionResidual.demand 730, OmissionResidual.demand 631, OmissionResidual.demand 630] ![1, 1, 1]
    support1106 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 730) (Fin.cases (hrows 631) (Fin.cases (hrows 630) (fun i => Fin.elim0 i))))
def support1107 : Finset (Fin 154) := {22, 29, 32, 37, 41, 42, 47, 48, 52, 57, 58, 61, 69, 73, 80, 84, 93, 94, 112}
theorem cut1107 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    2 ≤ ∑ i ∈ support1107, holes i := by
  apply rounded_cover_cut ![OmissionResidual.support 588, OmissionResidual.support 730, OmissionResidual.support 630] ![OmissionResidual.demand 588, OmissionResidual.demand 730, OmissionResidual.demand 630] ![1, 1, 1]
    support1107 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 588) (Fin.cases (hrows 730) (Fin.cases (hrows 630) (fun i => Fin.elim0 i))))
def support : Fin 1108 → Finset (Fin 154) := ![support0, support1, support2, support3, support4, support5, support6, support7, support8, support9, support10, support11, support12, support13, support14, support15, support16, support17, support18, support19, support20, support21, support22, support23, support24, support25, support26, support27, support28, support29, support30, support31, support32, support33, support34, support35, support36, support37, support38, support39, support40, support41, support42, support43, support44, support45, support46, support47, support48, support49, support50, support51, support52, support53, support54, support55, support56, support57, support58, support59, support60, support61, support62, support63, support64, support65, support66, support67, support68, support69, support70, support71, support72, support73, support74, support75, support76, support77, support78, support79, support80, support81, support82, support83, support84, support85, support86, support87, support88, support89, support90, support91, support92, support93, support94, support95, support96, support97, support98, support99, support100, support101, support102, support103, support104, support105, support106, support107, support108, support109, support110, support111, support112, support113, support114, support115, support116, support117, support118, support119, support120, support121, support122, support123, support124, support125, support126, support127, support128, support129, support130, support131, support132, support133, support134, support135, support136, support137, support138, support139, support140, support141, support142, support143, support144, support145, support146, support147, support148, support149, support150, support151, support152, support153, support154, support155, support156, support157, support158, support159, support160, support161, support162, support163, support164, support165, support166, support167, support168, support169, support170, support171, support172, support173, support174, support175, support176, support177, support178, support179, support180, support181, support182, support183, support184, support185, support186, support187, support188, support189, support190, support191, support192, support193, support194, support195, support196, support197, support198, support199, support200, support201, support202, support203, support204, support205, support206, support207, support208, support209, support210, support211, support212, support213, support214, support215, support216, support217, support218, support219, support220, support221, support222, support223, support224, support225, support226, support227, support228, support229, support230, support231, support232, support233, support234, support235, support236, support237, support238, support239, support240, support241, support242, support243, support244, support245, support246, support247, support248, support249, support250, support251, support252, support253, support254, support255, support256, support257, support258, support259, support260, support261, support262, support263, support264, support265, support266, support267, support268, support269, support270, support271, support272, support273, support274, support275, support276, support277, support278, support279, support280, support281, support282, support283, support284, support285, support286, support287, support288, support289, support290, support291, support292, support293, support294, support295, support296, support297, support298, support299, support300, support301, support302, support303, support304, support305, support306, support307, support308, support309, support310, support311, support312, support313, support314, support315, support316, support317, support318, support319, support320, support321, support322, support323, support324, support325, support326, support327, support328, support329, support330, support331, support332, support333, support334, support335, support336, support337, support338, support339, support340, support341, support342, support343, support344, support345, support346, support347, support348, support349, support350, support351, support352, support353, support354, support355, support356, support357, support358, support359, support360, support361, support362, support363, support364, support365, support366, support367, support368, support369, support370, support371, support372, support373, support374, support375, support376, support377, support378, support379, support380, support381, support382, support383, support384, support385, support386, support387, support388, support389, support390, support391, support392, support393, support394, support395, support396, support397, support398, support399, support400, support401, support402, support403, support404, support405, support406, support407, support408, support409, support410, support411, support412, support413, support414, support415, support416, support417, support418, support419, support420, support421, support422, support423, support424, support425, support426, support427, support428, support429, support430, support431, support432, support433, support434, support435, support436, support437, support438, support439, support440, support441, support442, support443, support444, support445, support446, support447, support448, support449, support450, support451, support452, support453, support454, support455, support456, support457, support458, support459, support460, support461, support462, support463, support464, support465, support466, support467, support468, support469, support470, support471, support472, support473, support474, support475, support476, support477, support478, support479, support480, support481, support482, support483, support484, support485, support486, support487, support488, support489, support490, support491, support492, support493, support494, support495, support496, support497, support498, support499, support500, support501, support502, support503, support504, support505, support506, support507, support508, support509, support510, support511, support512, support513, support514, support515, support516, support517, support518, support519, support520, support521, support522, support523, support524, support525, support526, support527, support528, support529, support530, support531, support532, support533, support534, support535, support536, support537, support538, support539, support540, support541, support542, support543, support544, support545, support546, support547, support548, support549, support550, support551, support552, support553, support554, support555, support556, support557, support558, support559, support560, support561, support562, support563, support564, support565, support566, support567, support568, support569, support570, support571, support572, support573, support574, support575, support576, support577, support578, support579, support580, support581, support582, support583, support584, support585, support586, support587, support588, support589, support590, support591, support592, support593, support594, support595, support596, support597, support598, support599, support600, support601, support602, support603, support604, support605, support606, support607, support608, support609, support610, support611, support612, support613, support614, support615, support616, support617, support618, support619, support620, support621, support622, support623, support624, support625, support626, support627, support628, support629, support630, support631, support632, support633, support634, support635, support636, support637, support638, support639, support640, support641, support642, support643, support644, support645, support646, support647, support648, support649, support650, support651, support652, support653, support654, support655, support656, support657, support658, support659, support660, support661, support662, support663, support664, support665, support666, support667, support668, support669, support670, support671, support672, support673, support674, support675, support676, support677, support678, support679, support680, support681, support682, support683, support684, support685, support686, support687, support688, support689, support690, support691, support692, support693, support694, support695, support696, support697, support698, support699, support700, support701, support702, support703, support704, support705, support706, support707, support708, support709, support710, support711, support712, support713, support714, support715, support716, support717, support718, support719, support720, support721, support722, support723, support724, support725, support726, support727, support728, support729, support730, support731, support732, support733, support734, support735, support736, support737, support738, support739, support740, support741, support742, support743, support744, support745, support746, support747, support748, support749, support750, support751, support752, support753, support754, support755, support756, support757, support758, support759, support760, support761, support762, support763, support764, support765, support766, support767, support768, support769, support770, support771, support772, support773, support774, support775, support776, support777, support778, support779, support780, support781, support782, support783, support784, support785, support786, support787, support788, support789, support790, support791, support792, support793, support794, support795, support796, support797, support798, support799, support800, support801, support802, support803, support804, support805, support806, support807, support808, support809, support810, support811, support812, support813, support814, support815, support816, support817, support818, support819, support820, support821, support822, support823, support824, support825, support826, support827, support828, support829, support830, support831, support832, support833, support834, support835, support836, support837, support838, support839, support840, support841, support842, support843, support844, support845, support846, support847, support848, support849, support850, support851, support852, support853, support854, support855, support856, support857, support858, support859, support860, support861, support862, support863, support864, support865, support866, support867, support868, support869, support870, support871, support872, support873, support874, support875, support876, support877, support878, support879, support880, support881, support882, support883, support884, support885, support886, support887, support888, support889, support890, support891, support892, support893, support894, support895, support896, support897, support898, support899, support900, support901, support902, support903, support904, support905, support906, support907, support908, support909, support910, support911, support912, support913, support914, support915, support916, support917, support918, support919, support920, support921, support922, support923, support924, support925, support926, support927, support928, support929, support930, support931, support932, support933, support934, support935, support936, support937, support938, support939, support940, support941, support942, support943, support944, support945, support946, support947, support948, support949, support950, support951, support952, support953, support954, support955, support956, support957, support958, support959, support960, support961, support962, support963, support964, support965, support966, support967, support968, support969, support970, support971, support972, support973, support974, support975, support976, support977, support978, support979, support980, support981, support982, support983, support984, support985, support986, support987, support988, support989, support990, support991, support992, support993, support994, support995, support996, support997, support998, support999, support1000, support1001, support1002, support1003, support1004, support1005, support1006, support1007, support1008, support1009, support1010, support1011, support1012, support1013, support1014, support1015, support1016, support1017, support1018, support1019, support1020, support1021, support1022, support1023, support1024, support1025, support1026, support1027, support1028, support1029, support1030, support1031, support1032, support1033, support1034, support1035, support1036, support1037, support1038, support1039, support1040, support1041, support1042, support1043, support1044, support1045, support1046, support1047, support1048, support1049, support1050, support1051, support1052, support1053, support1054, support1055, support1056, support1057, support1058, support1059, support1060, support1061, support1062, support1063, support1064, support1065, support1066, support1067, support1068, support1069, support1070, support1071, support1072, support1073, support1074, support1075, support1076, support1077, support1078, support1079, support1080, support1081, support1082, support1083, support1084, support1085, support1086, support1087, support1088, support1089, support1090, support1091, support1092, support1093, support1094, support1095, support1096, support1097, support1098, support1099, support1100, support1101, support1102, support1103, support1104, support1105, support1106, support1107]
def demand : Fin 1108 → ℕ := ![27, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 7, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 3, 2, 3, 3, 3, 3, 3, 3, 7, 7, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 3, 3, 2, 2, 3, 2, 2, 2, 2, 2, 2, 3, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 2, 2, 2, 2, 3, 3, 2, 3, 3, 2, 3, 2, 2, 2, 3, 3, 3, 3, 2, 3, 3, 3, 2, 2, 3, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 3, 3, 2, 3, 3, 2, 2, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 2, 2, 3, 3, 3, 3, 7, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 2, 3, 2, 2, 3, 2, 2, 2, 3, 3, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 2, 2, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 2, 3, 3, 3, 4, 2, 3, 2, 3, 2, 2, 3, 4, 3, 2, 4, 2, 3, 2, 2, 3, 2, 4, 4, 4, 4, 4, 3, 2, 3, 4, 4, 4, 4, 2, 2, 3, 2, 4, 3, 2, 2, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 3, 3, 2, 2, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 3, 4, 3, 3, 3, 2, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 3, 2, 2, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 4, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 2, 2, 2, 2, 3, 2, 3, 3, 3, 3, 4, 2, 3, 4, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 2, 2, 3, 3, 2, 2, 5, 4, 4, 3, 2, 2, 3, 3, 3, 4, 2, 2, 2, 2, 2, 2, 3, 3, 2, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 2, 4, 3, 2, 2, 2, 2, 4, 4, 4, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 2, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 2, 2, 2, 3, 3, 3, 3, 2, 2, 3, 2, 3, 2, 2, 3, 3, 3, 3, 3, 2, 2, 3, 2, 3, 3, 3, 3, 2, 2, 3, 2, 2, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 2, 3, 3, 4, 4, 3, 3, 4, 4, 3, 3, 3, 3, 2, 4, 4, 4, 4, 3, 4, 4, 4, 2, 3, 3, 3, 4, 4, 3, 3, 4, 2, 3, 3, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 3, 2, 3, 3, 2, 2, 2, 2, 2, 4, 4, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 3, 2, 3, 3, 3, 3, 3, 2, 2, 2, 2, 3, 2, 2, 2, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 3, 4, 3, 3, 3, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 2, 2, 3, 3, 3, 2, 2, 2, 2, 5, 4, 2, 2, 2, 2, 4, 3, 4, 4, 4, 4, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 4, 4, 2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 4, 4, 3, 2, 2, 2, 4, 4, 2, 3, 4, 4, 4, 5, 5, 3, 3, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 3, 2, 3, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 2, 3, 3, 2, 2, 5, 5, 5, 5, 3, 2, 2, 2, 2, 3, 4, 4, 2, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 5, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 3, 3, 2, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 3, 3, 3, 2, 3, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 5, 4, 3, 4, 4, 4, 4, 4, 4, 3, 3, 4, 5, 4, 2, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 4, 4, 4, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 3, 3, 2, 3, 3, 3, 4, 4, 3, 3, 3, 4, 4, 2, 2, 2, 2]
theorem all_rows (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 1187, OmissionResidual.demand r ≤
      ∑ i ∈ OmissionResidual.support r, holes i) :
    ∀ r, demand r ≤ ∑ i ∈ support r, holes i := by
  unfold support demand
  exact (Fin.cases (cut0 holes hbool hrows) (Fin.cases (cut1 holes hbool hrows) (Fin.cases (cut2 holes hbool hrows) (Fin.cases (cut3 holes hbool hrows) (Fin.cases (cut4 holes hbool hrows) (Fin.cases (cut5 holes hbool hrows) (Fin.cases (cut6 holes hbool hrows) (Fin.cases (cut7 holes hbool hrows) (Fin.cases (cut8 holes hbool hrows) (Fin.cases (cut9 holes hbool hrows) (Fin.cases (cut10 holes hbool hrows) (Fin.cases (cut11 holes hbool hrows) (Fin.cases (cut12 holes hbool hrows) (Fin.cases (cut13 holes hbool hrows) (Fin.cases (cut14 holes hbool hrows) (Fin.cases (cut15 holes hbool hrows) (Fin.cases (cut16 holes hbool hrows) (Fin.cases (cut17 holes hbool hrows) (Fin.cases (cut18 holes hbool hrows) (Fin.cases (cut19 holes hbool hrows) (Fin.cases (cut20 holes hbool hrows) (Fin.cases (cut21 holes hbool hrows) (Fin.cases (cut22 holes hbool hrows) (Fin.cases (cut23 holes hbool hrows) (Fin.cases (cut24 holes hbool hrows) (Fin.cases (cut25 holes hbool hrows) (Fin.cases (cut26 holes hbool hrows) (Fin.cases (cut27 holes hbool hrows) (Fin.cases (cut28 holes hbool hrows) (Fin.cases (cut29 holes hbool hrows) (Fin.cases (cut30 holes hbool hrows) (Fin.cases (cut31 holes hbool hrows) (Fin.cases (cut32 holes hbool hrows) (Fin.cases (cut33 holes hbool hrows) (Fin.cases (cut34 holes hbool hrows) (Fin.cases (cut35 holes hbool hrows) (Fin.cases (cut36 holes hbool hrows) (Fin.cases (cut37 holes hbool hrows) (Fin.cases (cut38 holes hbool hrows) (Fin.cases (cut39 holes hbool hrows) (Fin.cases (cut40 holes hbool hrows) (Fin.cases (cut41 holes hbool hrows) (Fin.cases (cut42 holes hbool hrows) (Fin.cases (cut43 holes hbool hrows) (Fin.cases (cut44 holes hbool hrows) (Fin.cases (cut45 holes hbool hrows) (Fin.cases (cut46 holes hbool hrows) (Fin.cases (cut47 holes hbool hrows) (Fin.cases (cut48 holes hbool hrows) (Fin.cases (cut49 holes hbool hrows) (Fin.cases (cut50 holes hbool hrows) (Fin.cases (cut51 holes hbool hrows) (Fin.cases (cut52 holes hbool hrows) (Fin.cases (cut53 holes hbool hrows) (Fin.cases (cut54 holes hbool hrows) (Fin.cases (cut55 holes hbool hrows) (Fin.cases (cut56 holes hbool hrows) (Fin.cases (cut57 holes hbool hrows) (Fin.cases (cut58 holes hbool hrows) (Fin.cases (cut59 holes hbool hrows) (Fin.cases (cut60 holes hbool hrows) (Fin.cases (cut61 holes hbool hrows) (Fin.cases (cut62 holes hbool hrows) (Fin.cases (cut63 holes hbool hrows) (Fin.cases (cut64 holes hbool hrows) (Fin.cases (cut65 holes hbool hrows) (Fin.cases (cut66 holes hbool hrows) (Fin.cases (cut67 holes hbool hrows) (Fin.cases (cut68 holes hbool hrows) (Fin.cases (cut69 holes hbool hrows) (Fin.cases (cut70 holes hbool hrows) (Fin.cases (cut71 holes hbool hrows) (Fin.cases (cut72 holes hbool hrows) (Fin.cases (cut73 holes hbool hrows) (Fin.cases (cut74 holes hbool hrows) (Fin.cases (cut75 holes hbool hrows) (Fin.cases (cut76 holes hbool hrows) (Fin.cases (cut77 holes hbool hrows) (Fin.cases (cut78 holes hbool hrows) (Fin.cases (cut79 holes hbool hrows) (Fin.cases (cut80 holes hbool hrows) (Fin.cases (cut81 holes hbool hrows) (Fin.cases (cut82 holes hbool hrows) (Fin.cases (cut83 holes hbool hrows) (Fin.cases (cut84 holes hbool hrows) (Fin.cases (cut85 holes hbool hrows) (Fin.cases (cut86 holes hbool hrows) (Fin.cases (cut87 holes hbool hrows) (Fin.cases (cut88 holes hbool hrows) (Fin.cases (cut89 holes hbool hrows) (Fin.cases (cut90 holes hbool hrows) (Fin.cases (cut91 holes hbool hrows) (Fin.cases (cut92 holes hbool hrows) (Fin.cases (cut93 holes hbool hrows) (Fin.cases (cut94 holes hbool hrows) (Fin.cases (cut95 holes hbool hrows) (Fin.cases (cut96 holes hbool hrows) (Fin.cases (cut97 holes hbool hrows) (Fin.cases (cut98 holes hbool hrows) (Fin.cases (cut99 holes hbool hrows) (Fin.cases (cut100 holes hbool hrows) (Fin.cases (cut101 holes hbool hrows) (Fin.cases (cut102 holes hbool hrows) (Fin.cases (cut103 holes hbool hrows) (Fin.cases (cut104 holes hbool hrows) (Fin.cases (cut105 holes hbool hrows) (Fin.cases (cut106 holes hbool hrows) (Fin.cases (cut107 holes hbool hrows) (Fin.cases (cut108 holes hbool hrows) (Fin.cases (cut109 holes hbool hrows) (Fin.cases (cut110 holes hbool hrows) (Fin.cases (cut111 holes hbool hrows) (Fin.cases (cut112 holes hbool hrows) (Fin.cases (cut113 holes hbool hrows) (Fin.cases (cut114 holes hbool hrows) (Fin.cases (cut115 holes hbool hrows) (Fin.cases (cut116 holes hbool hrows) (Fin.cases (cut117 holes hbool hrows) (Fin.cases (cut118 holes hbool hrows) (Fin.cases (cut119 holes hbool hrows) (Fin.cases (cut120 holes hbool hrows) (Fin.cases (cut121 holes hbool hrows) (Fin.cases (cut122 holes hbool hrows) (Fin.cases (cut123 holes hbool hrows) (Fin.cases (cut124 holes hbool hrows) (Fin.cases (cut125 holes hbool hrows) (Fin.cases (cut126 holes hbool hrows) (Fin.cases (cut127 holes hbool hrows) (Fin.cases (cut128 holes hbool hrows) (Fin.cases (cut129 holes hbool hrows) (Fin.cases (cut130 holes hbool hrows) (Fin.cases (cut131 holes hbool hrows) (Fin.cases (cut132 holes hbool hrows) (Fin.cases (cut133 holes hbool hrows) (Fin.cases (cut134 holes hbool hrows) (Fin.cases (cut135 holes hbool hrows) (Fin.cases (cut136 holes hbool hrows) (Fin.cases (cut137 holes hbool hrows) (Fin.cases (cut138 holes hbool hrows) (Fin.cases (cut139 holes hbool hrows) (Fin.cases (cut140 holes hbool hrows) (Fin.cases (cut141 holes hbool hrows) (Fin.cases (cut142 holes hbool hrows) (Fin.cases (cut143 holes hbool hrows) (Fin.cases (cut144 holes hbool hrows) (Fin.cases (cut145 holes hbool hrows) (Fin.cases (cut146 holes hbool hrows) (Fin.cases (cut147 holes hbool hrows) (Fin.cases (cut148 holes hbool hrows) (Fin.cases (cut149 holes hbool hrows) (Fin.cases (cut150 holes hbool hrows) (Fin.cases (cut151 holes hbool hrows) (Fin.cases (cut152 holes hbool hrows) (Fin.cases (cut153 holes hbool hrows) (Fin.cases (cut154 holes hbool hrows) (Fin.cases (cut155 holes hbool hrows) (Fin.cases (cut156 holes hbool hrows) (Fin.cases (cut157 holes hbool hrows) (Fin.cases (cut158 holes hbool hrows) (Fin.cases (cut159 holes hbool hrows) (Fin.cases (cut160 holes hbool hrows) (Fin.cases (cut161 holes hbool hrows) (Fin.cases (cut162 holes hbool hrows) (Fin.cases (cut163 holes hbool hrows) (Fin.cases (cut164 holes hbool hrows) (Fin.cases (cut165 holes hbool hrows) (Fin.cases (cut166 holes hbool hrows) (Fin.cases (cut167 holes hbool hrows) (Fin.cases (cut168 holes hbool hrows) (Fin.cases (cut169 holes hbool hrows) (Fin.cases (cut170 holes hbool hrows) (Fin.cases (cut171 holes hbool hrows) (Fin.cases (cut172 holes hbool hrows) (Fin.cases (cut173 holes hbool hrows) (Fin.cases (cut174 holes hbool hrows) (Fin.cases (cut175 holes hbool hrows) (Fin.cases (cut176 holes hbool hrows) (Fin.cases (cut177 holes hbool hrows) (Fin.cases (cut178 holes hbool hrows) (Fin.cases (cut179 holes hbool hrows) (Fin.cases (cut180 holes hbool hrows) (Fin.cases (cut181 holes hbool hrows) (Fin.cases (cut182 holes hbool hrows) (Fin.cases (cut183 holes hbool hrows) (Fin.cases (cut184 holes hbool hrows) (Fin.cases (cut185 holes hbool hrows) (Fin.cases (cut186 holes hbool hrows) (Fin.cases (cut187 holes hbool hrows) (Fin.cases (cut188 holes hbool hrows) (Fin.cases (cut189 holes hbool hrows) (Fin.cases (cut190 holes hbool hrows) (Fin.cases (cut191 holes hbool hrows) (Fin.cases (cut192 holes hbool hrows) (Fin.cases (cut193 holes hbool hrows) (Fin.cases (cut194 holes hbool hrows) (Fin.cases (cut195 holes hbool hrows) (Fin.cases (cut196 holes hbool hrows) (Fin.cases (cut197 holes hbool hrows) (Fin.cases (cut198 holes hbool hrows) (Fin.cases (cut199 holes hbool hrows) (Fin.cases (cut200 holes hbool hrows) (Fin.cases (cut201 holes hbool hrows) (Fin.cases (cut202 holes hbool hrows) (Fin.cases (cut203 holes hbool hrows) (Fin.cases (cut204 holes hbool hrows) (Fin.cases (cut205 holes hbool hrows) (Fin.cases (cut206 holes hbool hrows) (Fin.cases (cut207 holes hbool hrows) (Fin.cases (cut208 holes hbool hrows) (Fin.cases (cut209 holes hbool hrows) (Fin.cases (cut210 holes hbool hrows) (Fin.cases (cut211 holes hbool hrows) (Fin.cases (cut212 holes hbool hrows) (Fin.cases (cut213 holes hbool hrows) (Fin.cases (cut214 holes hbool hrows) (Fin.cases (cut215 holes hbool hrows) (Fin.cases (cut216 holes hbool hrows) (Fin.cases (cut217 holes hbool hrows) (Fin.cases (cut218 holes hbool hrows) (Fin.cases (cut219 holes hbool hrows) (Fin.cases (cut220 holes hbool hrows) (Fin.cases (cut221 holes hbool hrows) (Fin.cases (cut222 holes hbool hrows) (Fin.cases (cut223 holes hbool hrows) (Fin.cases (cut224 holes hbool hrows) (Fin.cases (cut225 holes hbool hrows) (Fin.cases (cut226 holes hbool hrows) (Fin.cases (cut227 holes hbool hrows) (Fin.cases (cut228 holes hbool hrows) (Fin.cases (cut229 holes hbool hrows) (Fin.cases (cut230 holes hbool hrows) (Fin.cases (cut231 holes hbool hrows) (Fin.cases (cut232 holes hbool hrows) (Fin.cases (cut233 holes hbool hrows) (Fin.cases (cut234 holes hbool hrows) (Fin.cases (cut235 holes hbool hrows) (Fin.cases (cut236 holes hbool hrows) (Fin.cases (cut237 holes hbool hrows) (Fin.cases (cut238 holes hbool hrows) (Fin.cases (cut239 holes hbool hrows) (Fin.cases (cut240 holes hbool hrows) (Fin.cases (cut241 holes hbool hrows) (Fin.cases (cut242 holes hbool hrows) (Fin.cases (cut243 holes hbool hrows) (Fin.cases (cut244 holes hbool hrows) (Fin.cases (cut245 holes hbool hrows) (Fin.cases (cut246 holes hbool hrows) (Fin.cases (cut247 holes hbool hrows) (Fin.cases (cut248 holes hbool hrows) (Fin.cases (cut249 holes hbool hrows) (Fin.cases (cut250 holes hbool hrows) (Fin.cases (cut251 holes hbool hrows) (Fin.cases (cut252 holes hbool hrows) (Fin.cases (cut253 holes hbool hrows) (Fin.cases (cut254 holes hbool hrows) (Fin.cases (cut255 holes hbool hrows) (Fin.cases (cut256 holes hbool hrows) (Fin.cases (cut257 holes hbool hrows) (Fin.cases (cut258 holes hbool hrows) (Fin.cases (cut259 holes hbool hrows) (Fin.cases (cut260 holes hbool hrows) (Fin.cases (cut261 holes hbool hrows) (Fin.cases (cut262 holes hbool hrows) (Fin.cases (cut263 holes hbool hrows) (Fin.cases (cut264 holes hbool hrows) (Fin.cases (cut265 holes hbool hrows) (Fin.cases (cut266 holes hbool hrows) (Fin.cases (cut267 holes hbool hrows) (Fin.cases (cut268 holes hbool hrows) (Fin.cases (cut269 holes hbool hrows) (Fin.cases (cut270 holes hbool hrows) (Fin.cases (cut271 holes hbool hrows) (Fin.cases (cut272 holes hbool hrows) (Fin.cases (cut273 holes hbool hrows) (Fin.cases (cut274 holes hbool hrows) (Fin.cases (cut275 holes hbool hrows) (Fin.cases (cut276 holes hbool hrows) (Fin.cases (cut277 holes hbool hrows) (Fin.cases (cut278 holes hbool hrows) (Fin.cases (cut279 holes hbool hrows) (Fin.cases (cut280 holes hbool hrows) (Fin.cases (cut281 holes hbool hrows) (Fin.cases (cut282 holes hbool hrows) (Fin.cases (cut283 holes hbool hrows) (Fin.cases (cut284 holes hbool hrows) (Fin.cases (cut285 holes hbool hrows) (Fin.cases (cut286 holes hbool hrows) (Fin.cases (cut287 holes hbool hrows) (Fin.cases (cut288 holes hbool hrows) (Fin.cases (cut289 holes hbool hrows) (Fin.cases (cut290 holes hbool hrows) (Fin.cases (cut291 holes hbool hrows) (Fin.cases (cut292 holes hbool hrows) (Fin.cases (cut293 holes hbool hrows) (Fin.cases (cut294 holes hbool hrows) (Fin.cases (cut295 holes hbool hrows) (Fin.cases (cut296 holes hbool hrows) (Fin.cases (cut297 holes hbool hrows) (Fin.cases (cut298 holes hbool hrows) (Fin.cases (cut299 holes hbool hrows) (Fin.cases (cut300 holes hbool hrows) (Fin.cases (cut301 holes hbool hrows) (Fin.cases (cut302 holes hbool hrows) (Fin.cases (cut303 holes hbool hrows) (Fin.cases (cut304 holes hbool hrows) (Fin.cases (cut305 holes hbool hrows) (Fin.cases (cut306 holes hbool hrows) (Fin.cases (cut307 holes hbool hrows) (Fin.cases (cut308 holes hbool hrows) (Fin.cases (cut309 holes hbool hrows) (Fin.cases (cut310 holes hbool hrows) (Fin.cases (cut311 holes hbool hrows) (Fin.cases (cut312 holes hbool hrows) (Fin.cases (cut313 holes hbool hrows) (Fin.cases (cut314 holes hbool hrows) (Fin.cases (cut315 holes hbool hrows) (Fin.cases (cut316 holes hbool hrows) (Fin.cases (cut317 holes hbool hrows) (Fin.cases (cut318 holes hbool hrows) (Fin.cases (cut319 holes hbool hrows) (Fin.cases (cut320 holes hbool hrows) (Fin.cases (cut321 holes hbool hrows) (Fin.cases (cut322 holes hbool hrows) (Fin.cases (cut323 holes hbool hrows) (Fin.cases (cut324 holes hbool hrows) (Fin.cases (cut325 holes hbool hrows) (Fin.cases (cut326 holes hbool hrows) (Fin.cases (cut327 holes hbool hrows) (Fin.cases (cut328 holes hbool hrows) (Fin.cases (cut329 holes hbool hrows) (Fin.cases (cut330 holes hbool hrows) (Fin.cases (cut331 holes hbool hrows) (Fin.cases (cut332 holes hbool hrows) (Fin.cases (cut333 holes hbool hrows) (Fin.cases (cut334 holes hbool hrows) (Fin.cases (cut335 holes hbool hrows) (Fin.cases (cut336 holes hbool hrows) (Fin.cases (cut337 holes hbool hrows) (Fin.cases (cut338 holes hbool hrows) (Fin.cases (cut339 holes hbool hrows) (Fin.cases (cut340 holes hbool hrows) (Fin.cases (cut341 holes hbool hrows) (Fin.cases (cut342 holes hbool hrows) (Fin.cases (cut343 holes hbool hrows) (Fin.cases (cut344 holes hbool hrows) (Fin.cases (cut345 holes hbool hrows) (Fin.cases (cut346 holes hbool hrows) (Fin.cases (cut347 holes hbool hrows) (Fin.cases (cut348 holes hbool hrows) (Fin.cases (cut349 holes hbool hrows) (Fin.cases (cut350 holes hbool hrows) (Fin.cases (cut351 holes hbool hrows) (Fin.cases (cut352 holes hbool hrows) (Fin.cases (cut353 holes hbool hrows) (Fin.cases (cut354 holes hbool hrows) (Fin.cases (cut355 holes hbool hrows) (Fin.cases (cut356 holes hbool hrows) (Fin.cases (cut357 holes hbool hrows) (Fin.cases (cut358 holes hbool hrows) (Fin.cases (cut359 holes hbool hrows) (Fin.cases (cut360 holes hbool hrows) (Fin.cases (cut361 holes hbool hrows) (Fin.cases (cut362 holes hbool hrows) (Fin.cases (cut363 holes hbool hrows) (Fin.cases (cut364 holes hbool hrows) (Fin.cases (cut365 holes hbool hrows) (Fin.cases (cut366 holes hbool hrows) (Fin.cases (cut367 holes hbool hrows) (Fin.cases (cut368 holes hbool hrows) (Fin.cases (cut369 holes hbool hrows) (Fin.cases (cut370 holes hbool hrows) (Fin.cases (cut371 holes hbool hrows) (Fin.cases (cut372 holes hbool hrows) (Fin.cases (cut373 holes hbool hrows) (Fin.cases (cut374 holes hbool hrows) (Fin.cases (cut375 holes hbool hrows) (Fin.cases (cut376 holes hbool hrows) (Fin.cases (cut377 holes hbool hrows) (Fin.cases (cut378 holes hbool hrows) (Fin.cases (cut379 holes hbool hrows) (Fin.cases (cut380 holes hbool hrows) (Fin.cases (cut381 holes hbool hrows) (Fin.cases (cut382 holes hbool hrows) (Fin.cases (cut383 holes hbool hrows) (Fin.cases (cut384 holes hbool hrows) (Fin.cases (cut385 holes hbool hrows) (Fin.cases (cut386 holes hbool hrows) (Fin.cases (cut387 holes hbool hrows) (Fin.cases (cut388 holes hbool hrows) (Fin.cases (cut389 holes hbool hrows) (Fin.cases (cut390 holes hbool hrows) (Fin.cases (cut391 holes hbool hrows) (Fin.cases (cut392 holes hbool hrows) (Fin.cases (cut393 holes hbool hrows) (Fin.cases (cut394 holes hbool hrows) (Fin.cases (cut395 holes hbool hrows) (Fin.cases (cut396 holes hbool hrows) (Fin.cases (cut397 holes hbool hrows) (Fin.cases (cut398 holes hbool hrows) (Fin.cases (cut399 holes hbool hrows) (Fin.cases (cut400 holes hbool hrows) (Fin.cases (cut401 holes hbool hrows) (Fin.cases (cut402 holes hbool hrows) (Fin.cases (cut403 holes hbool hrows) (Fin.cases (cut404 holes hbool hrows) (Fin.cases (cut405 holes hbool hrows) (Fin.cases (cut406 holes hbool hrows) (Fin.cases (cut407 holes hbool hrows) (Fin.cases (cut408 holes hbool hrows) (Fin.cases (cut409 holes hbool hrows) (Fin.cases (cut410 holes hbool hrows) (Fin.cases (cut411 holes hbool hrows) (Fin.cases (cut412 holes hbool hrows) (Fin.cases (cut413 holes hbool hrows) (Fin.cases (cut414 holes hbool hrows) (Fin.cases (cut415 holes hbool hrows) (Fin.cases (cut416 holes hbool hrows) (Fin.cases (cut417 holes hbool hrows) (Fin.cases (cut418 holes hbool hrows) (Fin.cases (cut419 holes hbool hrows) (Fin.cases (cut420 holes hbool hrows) (Fin.cases (cut421 holes hbool hrows) (Fin.cases (cut422 holes hbool hrows) (Fin.cases (cut423 holes hbool hrows) (Fin.cases (cut424 holes hbool hrows) (Fin.cases (cut425 holes hbool hrows) (Fin.cases (cut426 holes hbool hrows) (Fin.cases (cut427 holes hbool hrows) (Fin.cases (cut428 holes hbool hrows) (Fin.cases (cut429 holes hbool hrows) (Fin.cases (cut430 holes hbool hrows) (Fin.cases (cut431 holes hbool hrows) (Fin.cases (cut432 holes hbool hrows) (Fin.cases (cut433 holes hbool hrows) (Fin.cases (cut434 holes hbool hrows) (Fin.cases (cut435 holes hbool hrows) (Fin.cases (cut436 holes hbool hrows) (Fin.cases (cut437 holes hbool hrows) (Fin.cases (cut438 holes hbool hrows) (Fin.cases (cut439 holes hbool hrows) (Fin.cases (cut440 holes hbool hrows) (Fin.cases (cut441 holes hbool hrows) (Fin.cases (cut442 holes hbool hrows) (Fin.cases (cut443 holes hbool hrows) (Fin.cases (cut444 holes hbool hrows) (Fin.cases (cut445 holes hbool hrows) (Fin.cases (cut446 holes hbool hrows) (Fin.cases (cut447 holes hbool hrows) (Fin.cases (cut448 holes hbool hrows) (Fin.cases (cut449 holes hbool hrows) (Fin.cases (cut450 holes hbool hrows) (Fin.cases (cut451 holes hbool hrows) (Fin.cases (cut452 holes hbool hrows) (Fin.cases (cut453 holes hbool hrows) (Fin.cases (cut454 holes hbool hrows) (Fin.cases (cut455 holes hbool hrows) (Fin.cases (cut456 holes hbool hrows) (Fin.cases (cut457 holes hbool hrows) (Fin.cases (cut458 holes hbool hrows) (Fin.cases (cut459 holes hbool hrows) (Fin.cases (cut460 holes hbool hrows) (Fin.cases (cut461 holes hbool hrows) (Fin.cases (cut462 holes hbool hrows) (Fin.cases (cut463 holes hbool hrows) (Fin.cases (cut464 holes hbool hrows) (Fin.cases (cut465 holes hbool hrows) (Fin.cases (cut466 holes hbool hrows) (Fin.cases (cut467 holes hbool hrows) (Fin.cases (cut468 holes hbool hrows) (Fin.cases (cut469 holes hbool hrows) (Fin.cases (cut470 holes hbool hrows) (Fin.cases (cut471 holes hbool hrows) (Fin.cases (cut472 holes hbool hrows) (Fin.cases (cut473 holes hbool hrows) (Fin.cases (cut474 holes hbool hrows) (Fin.cases (cut475 holes hbool hrows) (Fin.cases (cut476 holes hbool hrows) (Fin.cases (cut477 holes hbool hrows) (Fin.cases (cut478 holes hbool hrows) (Fin.cases (cut479 holes hbool hrows) (Fin.cases (cut480 holes hbool hrows) (Fin.cases (cut481 holes hbool hrows) (Fin.cases (cut482 holes hbool hrows) (Fin.cases (cut483 holes hbool hrows) (Fin.cases (cut484 holes hbool hrows) (Fin.cases (cut485 holes hbool hrows) (Fin.cases (cut486 holes hbool hrows) (Fin.cases (cut487 holes hbool hrows) (Fin.cases (cut488 holes hbool hrows) (Fin.cases (cut489 holes hbool hrows) (Fin.cases (cut490 holes hbool hrows) (Fin.cases (cut491 holes hbool hrows) (Fin.cases (cut492 holes hbool hrows) (Fin.cases (cut493 holes hbool hrows) (Fin.cases (cut494 holes hbool hrows) (Fin.cases (cut495 holes hbool hrows) (Fin.cases (cut496 holes hbool hrows) (Fin.cases (cut497 holes hbool hrows) (Fin.cases (cut498 holes hbool hrows) (Fin.cases (cut499 holes hbool hrows) (Fin.cases (cut500 holes hbool hrows) (Fin.cases (cut501 holes hbool hrows) (Fin.cases (cut502 holes hbool hrows) (Fin.cases (cut503 holes hbool hrows) (Fin.cases (cut504 holes hbool hrows) (Fin.cases (cut505 holes hbool hrows) (Fin.cases (cut506 holes hbool hrows) (Fin.cases (cut507 holes hbool hrows) (Fin.cases (cut508 holes hbool hrows) (Fin.cases (cut509 holes hbool hrows) (Fin.cases (cut510 holes hbool hrows) (Fin.cases (cut511 holes hbool hrows) (Fin.cases (cut512 holes hbool hrows) (Fin.cases (cut513 holes hbool hrows) (Fin.cases (cut514 holes hbool hrows) (Fin.cases (cut515 holes hbool hrows) (Fin.cases (cut516 holes hbool hrows) (Fin.cases (cut517 holes hbool hrows) (Fin.cases (cut518 holes hbool hrows) (Fin.cases (cut519 holes hbool hrows) (Fin.cases (cut520 holes hbool hrows) (Fin.cases (cut521 holes hbool hrows) (Fin.cases (cut522 holes hbool hrows) (Fin.cases (cut523 holes hbool hrows) (Fin.cases (cut524 holes hbool hrows) (Fin.cases (cut525 holes hbool hrows) (Fin.cases (cut526 holes hbool hrows) (Fin.cases (cut527 holes hbool hrows) (Fin.cases (cut528 holes hbool hrows) (Fin.cases (cut529 holes hbool hrows) (Fin.cases (cut530 holes hbool hrows) (Fin.cases (cut531 holes hbool hrows) (Fin.cases (cut532 holes hbool hrows) (Fin.cases (cut533 holes hbool hrows) (Fin.cases (cut534 holes hbool hrows) (Fin.cases (cut535 holes hbool hrows) (Fin.cases (cut536 holes hbool hrows) (Fin.cases (cut537 holes hbool hrows) (Fin.cases (cut538 holes hbool hrows) (Fin.cases (cut539 holes hbool hrows) (Fin.cases (cut540 holes hbool hrows) (Fin.cases (cut541 holes hbool hrows) (Fin.cases (cut542 holes hbool hrows) (Fin.cases (cut543 holes hbool hrows) (Fin.cases (cut544 holes hbool hrows) (Fin.cases (cut545 holes hbool hrows) (Fin.cases (cut546 holes hbool hrows) (Fin.cases (cut547 holes hbool hrows) (Fin.cases (cut548 holes hbool hrows) (Fin.cases (cut549 holes hbool hrows) (Fin.cases (cut550 holes hbool hrows) (Fin.cases (cut551 holes hbool hrows) (Fin.cases (cut552 holes hbool hrows) (Fin.cases (cut553 holes hbool hrows) (Fin.cases (cut554 holes hbool hrows) (Fin.cases (cut555 holes hbool hrows) (Fin.cases (cut556 holes hbool hrows) (Fin.cases (cut557 holes hbool hrows) (Fin.cases (cut558 holes hbool hrows) (Fin.cases (cut559 holes hbool hrows) (Fin.cases (cut560 holes hbool hrows) (Fin.cases (cut561 holes hbool hrows) (Fin.cases (cut562 holes hbool hrows) (Fin.cases (cut563 holes hbool hrows) (Fin.cases (cut564 holes hbool hrows) (Fin.cases (cut565 holes hbool hrows) (Fin.cases (cut566 holes hbool hrows) (Fin.cases (cut567 holes hbool hrows) (Fin.cases (cut568 holes hbool hrows) (Fin.cases (cut569 holes hbool hrows) (Fin.cases (cut570 holes hbool hrows) (Fin.cases (cut571 holes hbool hrows) (Fin.cases (cut572 holes hbool hrows) (Fin.cases (cut573 holes hbool hrows) (Fin.cases (cut574 holes hbool hrows) (Fin.cases (cut575 holes hbool hrows) (Fin.cases (cut576 holes hbool hrows) (Fin.cases (cut577 holes hbool hrows) (Fin.cases (cut578 holes hbool hrows) (Fin.cases (cut579 holes hbool hrows) (Fin.cases (cut580 holes hbool hrows) (Fin.cases (cut581 holes hbool hrows) (Fin.cases (cut582 holes hbool hrows) (Fin.cases (cut583 holes hbool hrows) (Fin.cases (cut584 holes hbool hrows) (Fin.cases (cut585 holes hbool hrows) (Fin.cases (cut586 holes hbool hrows) (Fin.cases (cut587 holes hbool hrows) (Fin.cases (cut588 holes hbool hrows) (Fin.cases (cut589 holes hbool hrows) (Fin.cases (cut590 holes hbool hrows) (Fin.cases (cut591 holes hbool hrows) (Fin.cases (cut592 holes hbool hrows) (Fin.cases (cut593 holes hbool hrows) (Fin.cases (cut594 holes hbool hrows) (Fin.cases (cut595 holes hbool hrows) (Fin.cases (cut596 holes hbool hrows) (Fin.cases (cut597 holes hbool hrows) (Fin.cases (cut598 holes hbool hrows) (Fin.cases (cut599 holes hbool hrows) (Fin.cases (cut600 holes hbool hrows) (Fin.cases (cut601 holes hbool hrows) (Fin.cases (cut602 holes hbool hrows) (Fin.cases (cut603 holes hbool hrows) (Fin.cases (cut604 holes hbool hrows) (Fin.cases (cut605 holes hbool hrows) (Fin.cases (cut606 holes hbool hrows) (Fin.cases (cut607 holes hbool hrows) (Fin.cases (cut608 holes hbool hrows) (Fin.cases (cut609 holes hbool hrows) (Fin.cases (cut610 holes hbool hrows) (Fin.cases (cut611 holes hbool hrows) (Fin.cases (cut612 holes hbool hrows) (Fin.cases (cut613 holes hbool hrows) (Fin.cases (cut614 holes hbool hrows) (Fin.cases (cut615 holes hbool hrows) (Fin.cases (cut616 holes hbool hrows) (Fin.cases (cut617 holes hbool hrows) (Fin.cases (cut618 holes hbool hrows) (Fin.cases (cut619 holes hbool hrows) (Fin.cases (cut620 holes hbool hrows) (Fin.cases (cut621 holes hbool hrows) (Fin.cases (cut622 holes hbool hrows) (Fin.cases (cut623 holes hbool hrows) (Fin.cases (cut624 holes hbool hrows) (Fin.cases (cut625 holes hbool hrows) (Fin.cases (cut626 holes hbool hrows) (Fin.cases (cut627 holes hbool hrows) (Fin.cases (cut628 holes hbool hrows) (Fin.cases (cut629 holes hbool hrows) (Fin.cases (cut630 holes hbool hrows) (Fin.cases (cut631 holes hbool hrows) (Fin.cases (cut632 holes hbool hrows) (Fin.cases (cut633 holes hbool hrows) (Fin.cases (cut634 holes hbool hrows) (Fin.cases (cut635 holes hbool hrows) (Fin.cases (cut636 holes hbool hrows) (Fin.cases (cut637 holes hbool hrows) (Fin.cases (cut638 holes hbool hrows) (Fin.cases (cut639 holes hbool hrows) (Fin.cases (cut640 holes hbool hrows) (Fin.cases (cut641 holes hbool hrows) (Fin.cases (cut642 holes hbool hrows) (Fin.cases (cut643 holes hbool hrows) (Fin.cases (cut644 holes hbool hrows) (Fin.cases (cut645 holes hbool hrows) (Fin.cases (cut646 holes hbool hrows) (Fin.cases (cut647 holes hbool hrows) (Fin.cases (cut648 holes hbool hrows) (Fin.cases (cut649 holes hbool hrows) (Fin.cases (cut650 holes hbool hrows) (Fin.cases (cut651 holes hbool hrows) (Fin.cases (cut652 holes hbool hrows) (Fin.cases (cut653 holes hbool hrows) (Fin.cases (cut654 holes hbool hrows) (Fin.cases (cut655 holes hbool hrows) (Fin.cases (cut656 holes hbool hrows) (Fin.cases (cut657 holes hbool hrows) (Fin.cases (cut658 holes hbool hrows) (Fin.cases (cut659 holes hbool hrows) (Fin.cases (cut660 holes hbool hrows) (Fin.cases (cut661 holes hbool hrows) (Fin.cases (cut662 holes hbool hrows) (Fin.cases (cut663 holes hbool hrows) (Fin.cases (cut664 holes hbool hrows) (Fin.cases (cut665 holes hbool hrows) (Fin.cases (cut666 holes hbool hrows) (Fin.cases (cut667 holes hbool hrows) (Fin.cases (cut668 holes hbool hrows) (Fin.cases (cut669 holes hbool hrows) (Fin.cases (cut670 holes hbool hrows) (Fin.cases (cut671 holes hbool hrows) (Fin.cases (cut672 holes hbool hrows) (Fin.cases (cut673 holes hbool hrows) (Fin.cases (cut674 holes hbool hrows) (Fin.cases (cut675 holes hbool hrows) (Fin.cases (cut676 holes hbool hrows) (Fin.cases (cut677 holes hbool hrows) (Fin.cases (cut678 holes hbool hrows) (Fin.cases (cut679 holes hbool hrows) (Fin.cases (cut680 holes hbool hrows) (Fin.cases (cut681 holes hbool hrows) (Fin.cases (cut682 holes hbool hrows) (Fin.cases (cut683 holes hbool hrows) (Fin.cases (cut684 holes hbool hrows) (Fin.cases (cut685 holes hbool hrows) (Fin.cases (cut686 holes hbool hrows) (Fin.cases (cut687 holes hbool hrows) (Fin.cases (cut688 holes hbool hrows) (Fin.cases (cut689 holes hbool hrows) (Fin.cases (cut690 holes hbool hrows) (Fin.cases (cut691 holes hbool hrows) (Fin.cases (cut692 holes hbool hrows) (Fin.cases (cut693 holes hbool hrows) (Fin.cases (cut694 holes hbool hrows) (Fin.cases (cut695 holes hbool hrows) (Fin.cases (cut696 holes hbool hrows) (Fin.cases (cut697 holes hbool hrows) (Fin.cases (cut698 holes hbool hrows) (Fin.cases (cut699 holes hbool hrows) (Fin.cases (cut700 holes hbool hrows) (Fin.cases (cut701 holes hbool hrows) (Fin.cases (cut702 holes hbool hrows) (Fin.cases (cut703 holes hbool hrows) (Fin.cases (cut704 holes hbool hrows) (Fin.cases (cut705 holes hbool hrows) (Fin.cases (cut706 holes hbool hrows) (Fin.cases (cut707 holes hbool hrows) (Fin.cases (cut708 holes hbool hrows) (Fin.cases (cut709 holes hbool hrows) (Fin.cases (cut710 holes hbool hrows) (Fin.cases (cut711 holes hbool hrows) (Fin.cases (cut712 holes hbool hrows) (Fin.cases (cut713 holes hbool hrows) (Fin.cases (cut714 holes hbool hrows) (Fin.cases (cut715 holes hbool hrows) (Fin.cases (cut716 holes hbool hrows) (Fin.cases (cut717 holes hbool hrows) (Fin.cases (cut718 holes hbool hrows) (Fin.cases (cut719 holes hbool hrows) (Fin.cases (cut720 holes hbool hrows) (Fin.cases (cut721 holes hbool hrows) (Fin.cases (cut722 holes hbool hrows) (Fin.cases (cut723 holes hbool hrows) (Fin.cases (cut724 holes hbool hrows) (Fin.cases (cut725 holes hbool hrows) (Fin.cases (cut726 holes hbool hrows) (Fin.cases (cut727 holes hbool hrows) (Fin.cases (cut728 holes hbool hrows) (Fin.cases (cut729 holes hbool hrows) (Fin.cases (cut730 holes hbool hrows) (Fin.cases (cut731 holes hbool hrows) (Fin.cases (cut732 holes hbool hrows) (Fin.cases (cut733 holes hbool hrows) (Fin.cases (cut734 holes hbool hrows) (Fin.cases (cut735 holes hbool hrows) (Fin.cases (cut736 holes hbool hrows) (Fin.cases (cut737 holes hbool hrows) (Fin.cases (cut738 holes hbool hrows) (Fin.cases (cut739 holes hbool hrows) (Fin.cases (cut740 holes hbool hrows) (Fin.cases (cut741 holes hbool hrows) (Fin.cases (cut742 holes hbool hrows) (Fin.cases (cut743 holes hbool hrows) (Fin.cases (cut744 holes hbool hrows) (Fin.cases (cut745 holes hbool hrows) (Fin.cases (cut746 holes hbool hrows) (Fin.cases (cut747 holes hbool hrows) (Fin.cases (cut748 holes hbool hrows) (Fin.cases (cut749 holes hbool hrows) (Fin.cases (cut750 holes hbool hrows) (Fin.cases (cut751 holes hbool hrows) (Fin.cases (cut752 holes hbool hrows) (Fin.cases (cut753 holes hbool hrows) (Fin.cases (cut754 holes hbool hrows) (Fin.cases (cut755 holes hbool hrows) (Fin.cases (cut756 holes hbool hrows) (Fin.cases (cut757 holes hbool hrows) (Fin.cases (cut758 holes hbool hrows) (Fin.cases (cut759 holes hbool hrows) (Fin.cases (cut760 holes hbool hrows) (Fin.cases (cut761 holes hbool hrows) (Fin.cases (cut762 holes hbool hrows) (Fin.cases (cut763 holes hbool hrows) (Fin.cases (cut764 holes hbool hrows) (Fin.cases (cut765 holes hbool hrows) (Fin.cases (cut766 holes hbool hrows) (Fin.cases (cut767 holes hbool hrows) (Fin.cases (cut768 holes hbool hrows) (Fin.cases (cut769 holes hbool hrows) (Fin.cases (cut770 holes hbool hrows) (Fin.cases (cut771 holes hbool hrows) (Fin.cases (cut772 holes hbool hrows) (Fin.cases (cut773 holes hbool hrows) (Fin.cases (cut774 holes hbool hrows) (Fin.cases (cut775 holes hbool hrows) (Fin.cases (cut776 holes hbool hrows) (Fin.cases (cut777 holes hbool hrows) (Fin.cases (cut778 holes hbool hrows) (Fin.cases (cut779 holes hbool hrows) (Fin.cases (cut780 holes hbool hrows) (Fin.cases (cut781 holes hbool hrows) (Fin.cases (cut782 holes hbool hrows) (Fin.cases (cut783 holes hbool hrows) (Fin.cases (cut784 holes hbool hrows) (Fin.cases (cut785 holes hbool hrows) (Fin.cases (cut786 holes hbool hrows) (Fin.cases (cut787 holes hbool hrows) (Fin.cases (cut788 holes hbool hrows) (Fin.cases (cut789 holes hbool hrows) (Fin.cases (cut790 holes hbool hrows) (Fin.cases (cut791 holes hbool hrows) (Fin.cases (cut792 holes hbool hrows) (Fin.cases (cut793 holes hbool hrows) (Fin.cases (cut794 holes hbool hrows) (Fin.cases (cut795 holes hbool hrows) (Fin.cases (cut796 holes hbool hrows) (Fin.cases (cut797 holes hbool hrows) (Fin.cases (cut798 holes hbool hrows) (Fin.cases (cut799 holes hbool hrows) (Fin.cases (cut800 holes hbool hrows) (Fin.cases (cut801 holes hbool hrows) (Fin.cases (cut802 holes hbool hrows) (Fin.cases (cut803 holes hbool hrows) (Fin.cases (cut804 holes hbool hrows) (Fin.cases (cut805 holes hbool hrows) (Fin.cases (cut806 holes hbool hrows) (Fin.cases (cut807 holes hbool hrows) (Fin.cases (cut808 holes hbool hrows) (Fin.cases (cut809 holes hbool hrows) (Fin.cases (cut810 holes hbool hrows) (Fin.cases (cut811 holes hbool hrows) (Fin.cases (cut812 holes hbool hrows) (Fin.cases (cut813 holes hbool hrows) (Fin.cases (cut814 holes hbool hrows) (Fin.cases (cut815 holes hbool hrows) (Fin.cases (cut816 holes hbool hrows) (Fin.cases (cut817 holes hbool hrows) (Fin.cases (cut818 holes hbool hrows) (Fin.cases (cut819 holes hbool hrows) (Fin.cases (cut820 holes hbool hrows) (Fin.cases (cut821 holes hbool hrows) (Fin.cases (cut822 holes hbool hrows) (Fin.cases (cut823 holes hbool hrows) (Fin.cases (cut824 holes hbool hrows) (Fin.cases (cut825 holes hbool hrows) (Fin.cases (cut826 holes hbool hrows) (Fin.cases (cut827 holes hbool hrows) (Fin.cases (cut828 holes hbool hrows) (Fin.cases (cut829 holes hbool hrows) (Fin.cases (cut830 holes hbool hrows) (Fin.cases (cut831 holes hbool hrows) (Fin.cases (cut832 holes hbool hrows) (Fin.cases (cut833 holes hbool hrows) (Fin.cases (cut834 holes hbool hrows) (Fin.cases (cut835 holes hbool hrows) (Fin.cases (cut836 holes hbool hrows) (Fin.cases (cut837 holes hbool hrows) (Fin.cases (cut838 holes hbool hrows) (Fin.cases (cut839 holes hbool hrows) (Fin.cases (cut840 holes hbool hrows) (Fin.cases (cut841 holes hbool hrows) (Fin.cases (cut842 holes hbool hrows) (Fin.cases (cut843 holes hbool hrows) (Fin.cases (cut844 holes hbool hrows) (Fin.cases (cut845 holes hbool hrows) (Fin.cases (cut846 holes hbool hrows) (Fin.cases (cut847 holes hbool hrows) (Fin.cases (cut848 holes hbool hrows) (Fin.cases (cut849 holes hbool hrows) (Fin.cases (cut850 holes hbool hrows) (Fin.cases (cut851 holes hbool hrows) (Fin.cases (cut852 holes hbool hrows) (Fin.cases (cut853 holes hbool hrows) (Fin.cases (cut854 holes hbool hrows) (Fin.cases (cut855 holes hbool hrows) (Fin.cases (cut856 holes hbool hrows) (Fin.cases (cut857 holes hbool hrows) (Fin.cases (cut858 holes hbool hrows) (Fin.cases (cut859 holes hbool hrows) (Fin.cases (cut860 holes hbool hrows) (Fin.cases (cut861 holes hbool hrows) (Fin.cases (cut862 holes hbool hrows) (Fin.cases (cut863 holes hbool hrows) (Fin.cases (cut864 holes hbool hrows) (Fin.cases (cut865 holes hbool hrows) (Fin.cases (cut866 holes hbool hrows) (Fin.cases (cut867 holes hbool hrows) (Fin.cases (cut868 holes hbool hrows) (Fin.cases (cut869 holes hbool hrows) (Fin.cases (cut870 holes hbool hrows) (Fin.cases (cut871 holes hbool hrows) (Fin.cases (cut872 holes hbool hrows) (Fin.cases (cut873 holes hbool hrows) (Fin.cases (cut874 holes hbool hrows) (Fin.cases (cut875 holes hbool hrows) (Fin.cases (cut876 holes hbool hrows) (Fin.cases (cut877 holes hbool hrows) (Fin.cases (cut878 holes hbool hrows) (Fin.cases (cut879 holes hbool hrows) (Fin.cases (cut880 holes hbool hrows) (Fin.cases (cut881 holes hbool hrows) (Fin.cases (cut882 holes hbool hrows) (Fin.cases (cut883 holes hbool hrows) (Fin.cases (cut884 holes hbool hrows) (Fin.cases (cut885 holes hbool hrows) (Fin.cases (cut886 holes hbool hrows) (Fin.cases (cut887 holes hbool hrows) (Fin.cases (cut888 holes hbool hrows) (Fin.cases (cut889 holes hbool hrows) (Fin.cases (cut890 holes hbool hrows) (Fin.cases (cut891 holes hbool hrows) (Fin.cases (cut892 holes hbool hrows) (Fin.cases (cut893 holes hbool hrows) (Fin.cases (cut894 holes hbool hrows) (Fin.cases (cut895 holes hbool hrows) (Fin.cases (cut896 holes hbool hrows) (Fin.cases (cut897 holes hbool hrows) (Fin.cases (cut898 holes hbool hrows) (Fin.cases (cut899 holes hbool hrows) (Fin.cases (cut900 holes hbool hrows) (Fin.cases (cut901 holes hbool hrows) (Fin.cases (cut902 holes hbool hrows) (Fin.cases (cut903 holes hbool hrows) (Fin.cases (cut904 holes hbool hrows) (Fin.cases (cut905 holes hbool hrows) (Fin.cases (cut906 holes hbool hrows) (Fin.cases (cut907 holes hbool hrows) (Fin.cases (cut908 holes hbool hrows) (Fin.cases (cut909 holes hbool hrows) (Fin.cases (cut910 holes hbool hrows) (Fin.cases (cut911 holes hbool hrows) (Fin.cases (cut912 holes hbool hrows) (Fin.cases (cut913 holes hbool hrows) (Fin.cases (cut914 holes hbool hrows) (Fin.cases (cut915 holes hbool hrows) (Fin.cases (cut916 holes hbool hrows) (Fin.cases (cut917 holes hbool hrows) (Fin.cases (cut918 holes hbool hrows) (Fin.cases (cut919 holes hbool hrows) (Fin.cases (cut920 holes hbool hrows) (Fin.cases (cut921 holes hbool hrows) (Fin.cases (cut922 holes hbool hrows) (Fin.cases (cut923 holes hbool hrows) (Fin.cases (cut924 holes hbool hrows) (Fin.cases (cut925 holes hbool hrows) (Fin.cases (cut926 holes hbool hrows) (Fin.cases (cut927 holes hbool hrows) (Fin.cases (cut928 holes hbool hrows) (Fin.cases (cut929 holes hbool hrows) (Fin.cases (cut930 holes hbool hrows) (Fin.cases (cut931 holes hbool hrows) (Fin.cases (cut932 holes hbool hrows) (Fin.cases (cut933 holes hbool hrows) (Fin.cases (cut934 holes hbool hrows) (Fin.cases (cut935 holes hbool hrows) (Fin.cases (cut936 holes hbool hrows) (Fin.cases (cut937 holes hbool hrows) (Fin.cases (cut938 holes hbool hrows) (Fin.cases (cut939 holes hbool hrows) (Fin.cases (cut940 holes hbool hrows) (Fin.cases (cut941 holes hbool hrows) (Fin.cases (cut942 holes hbool hrows) (Fin.cases (cut943 holes hbool hrows) (Fin.cases (cut944 holes hbool hrows) (Fin.cases (cut945 holes hbool hrows) (Fin.cases (cut946 holes hbool hrows) (Fin.cases (cut947 holes hbool hrows) (Fin.cases (cut948 holes hbool hrows) (Fin.cases (cut949 holes hbool hrows) (Fin.cases (cut950 holes hbool hrows) (Fin.cases (cut951 holes hbool hrows) (Fin.cases (cut952 holes hbool hrows) (Fin.cases (cut953 holes hbool hrows) (Fin.cases (cut954 holes hbool hrows) (Fin.cases (cut955 holes hbool hrows) (Fin.cases (cut956 holes hbool hrows) (Fin.cases (cut957 holes hbool hrows) (Fin.cases (cut958 holes hbool hrows) (Fin.cases (cut959 holes hbool hrows) (Fin.cases (cut960 holes hbool hrows) (Fin.cases (cut961 holes hbool hrows) (Fin.cases (cut962 holes hbool hrows) (Fin.cases (cut963 holes hbool hrows) (Fin.cases (cut964 holes hbool hrows) (Fin.cases (cut965 holes hbool hrows) (Fin.cases (cut966 holes hbool hrows) (Fin.cases (cut967 holes hbool hrows) (Fin.cases (cut968 holes hbool hrows) (Fin.cases (cut969 holes hbool hrows) (Fin.cases (cut970 holes hbool hrows) (Fin.cases (cut971 holes hbool hrows) (Fin.cases (cut972 holes hbool hrows) (Fin.cases (cut973 holes hbool hrows) (Fin.cases (cut974 holes hbool hrows) (Fin.cases (cut975 holes hbool hrows) (Fin.cases (cut976 holes hbool hrows) (Fin.cases (cut977 holes hbool hrows) (Fin.cases (cut978 holes hbool hrows) (Fin.cases (cut979 holes hbool hrows) (Fin.cases (cut980 holes hbool hrows) (Fin.cases (cut981 holes hbool hrows) (Fin.cases (cut982 holes hbool hrows) (Fin.cases (cut983 holes hbool hrows) (Fin.cases (cut984 holes hbool hrows) (Fin.cases (cut985 holes hbool hrows) (Fin.cases (cut986 holes hbool hrows) (Fin.cases (cut987 holes hbool hrows) (Fin.cases (cut988 holes hbool hrows) (Fin.cases (cut989 holes hbool hrows) (Fin.cases (cut990 holes hbool hrows) (Fin.cases (cut991 holes hbool hrows) (Fin.cases (cut992 holes hbool hrows) (Fin.cases (cut993 holes hbool hrows) (Fin.cases (cut994 holes hbool hrows) (Fin.cases (cut995 holes hbool hrows) (Fin.cases (cut996 holes hbool hrows) (Fin.cases (cut997 holes hbool hrows) (Fin.cases (cut998 holes hbool hrows) (Fin.cases (cut999 holes hbool hrows) (Fin.cases (cut1000 holes hbool hrows) (Fin.cases (cut1001 holes hbool hrows) (Fin.cases (cut1002 holes hbool hrows) (Fin.cases (cut1003 holes hbool hrows) (Fin.cases (cut1004 holes hbool hrows) (Fin.cases (cut1005 holes hbool hrows) (Fin.cases (cut1006 holes hbool hrows) (Fin.cases (cut1007 holes hbool hrows) (Fin.cases (cut1008 holes hbool hrows) (Fin.cases (cut1009 holes hbool hrows) (Fin.cases (cut1010 holes hbool hrows) (Fin.cases (cut1011 holes hbool hrows) (Fin.cases (cut1012 holes hbool hrows) (Fin.cases (cut1013 holes hbool hrows) (Fin.cases (cut1014 holes hbool hrows) (Fin.cases (cut1015 holes hbool hrows) (Fin.cases (cut1016 holes hbool hrows) (Fin.cases (cut1017 holes hbool hrows) (Fin.cases (cut1018 holes hbool hrows) (Fin.cases (cut1019 holes hbool hrows) (Fin.cases (cut1020 holes hbool hrows) (Fin.cases (cut1021 holes hbool hrows) (Fin.cases (cut1022 holes hbool hrows) (Fin.cases (cut1023 holes hbool hrows) (Fin.cases (cut1024 holes hbool hrows) (Fin.cases (cut1025 holes hbool hrows) (Fin.cases (cut1026 holes hbool hrows) (Fin.cases (cut1027 holes hbool hrows) (Fin.cases (cut1028 holes hbool hrows) (Fin.cases (cut1029 holes hbool hrows) (Fin.cases (cut1030 holes hbool hrows) (Fin.cases (cut1031 holes hbool hrows) (Fin.cases (cut1032 holes hbool hrows) (Fin.cases (cut1033 holes hbool hrows) (Fin.cases (cut1034 holes hbool hrows) (Fin.cases (cut1035 holes hbool hrows) (Fin.cases (cut1036 holes hbool hrows) (Fin.cases (cut1037 holes hbool hrows) (Fin.cases (cut1038 holes hbool hrows) (Fin.cases (cut1039 holes hbool hrows) (Fin.cases (cut1040 holes hbool hrows) (Fin.cases (cut1041 holes hbool hrows) (Fin.cases (cut1042 holes hbool hrows) (Fin.cases (cut1043 holes hbool hrows) (Fin.cases (cut1044 holes hbool hrows) (Fin.cases (cut1045 holes hbool hrows) (Fin.cases (cut1046 holes hbool hrows) (Fin.cases (cut1047 holes hbool hrows) (Fin.cases (cut1048 holes hbool hrows) (Fin.cases (cut1049 holes hbool hrows) (Fin.cases (cut1050 holes hbool hrows) (Fin.cases (cut1051 holes hbool hrows) (Fin.cases (cut1052 holes hbool hrows) (Fin.cases (cut1053 holes hbool hrows) (Fin.cases (cut1054 holes hbool hrows) (Fin.cases (cut1055 holes hbool hrows) (Fin.cases (cut1056 holes hbool hrows) (Fin.cases (cut1057 holes hbool hrows) (Fin.cases (cut1058 holes hbool hrows) (Fin.cases (cut1059 holes hbool hrows) (Fin.cases (cut1060 holes hbool hrows) (Fin.cases (cut1061 holes hbool hrows) (Fin.cases (cut1062 holes hbool hrows) (Fin.cases (cut1063 holes hbool hrows) (Fin.cases (cut1064 holes hbool hrows) (Fin.cases (cut1065 holes hbool hrows) (Fin.cases (cut1066 holes hbool hrows) (Fin.cases (cut1067 holes hbool hrows) (Fin.cases (cut1068 holes hbool hrows) (Fin.cases (cut1069 holes hbool hrows) (Fin.cases (cut1070 holes hbool hrows) (Fin.cases (cut1071 holes hbool hrows) (Fin.cases (cut1072 holes hbool hrows) (Fin.cases (cut1073 holes hbool hrows) (Fin.cases (cut1074 holes hbool hrows) (Fin.cases (cut1075 holes hbool hrows) (Fin.cases (cut1076 holes hbool hrows) (Fin.cases (cut1077 holes hbool hrows) (Fin.cases (cut1078 holes hbool hrows) (Fin.cases (cut1079 holes hbool hrows) (Fin.cases (cut1080 holes hbool hrows) (Fin.cases (cut1081 holes hbool hrows) (Fin.cases (cut1082 holes hbool hrows) (Fin.cases (cut1083 holes hbool hrows) (Fin.cases (cut1084 holes hbool hrows) (Fin.cases (cut1085 holes hbool hrows) (Fin.cases (cut1086 holes hbool hrows) (Fin.cases (cut1087 holes hbool hrows) (Fin.cases (cut1088 holes hbool hrows) (Fin.cases (cut1089 holes hbool hrows) (Fin.cases (cut1090 holes hbool hrows) (Fin.cases (cut1091 holes hbool hrows) (Fin.cases (cut1092 holes hbool hrows) (Fin.cases (cut1093 holes hbool hrows) (Fin.cases (cut1094 holes hbool hrows) (Fin.cases (cut1095 holes hbool hrows) (Fin.cases (cut1096 holes hbool hrows) (Fin.cases (cut1097 holes hbool hrows) (Fin.cases (cut1098 holes hbool hrows) (Fin.cases (cut1099 holes hbool hrows) (Fin.cases (cut1100 holes hbool hrows) (Fin.cases (cut1101 holes hbool hrows) (Fin.cases (cut1102 holes hbool hrows) (Fin.cases (cut1103 holes hbool hrows) (Fin.cases (cut1104 holes hbool hrows) (Fin.cases (cut1105 holes hbool hrows) (Fin.cases (cut1106 holes hbool hrows) (Fin.cases (cut1107 holes hbool hrows) (fun i => Fin.elim0 i)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#print axioms all_rows
end ResidualCoverCutsV2
