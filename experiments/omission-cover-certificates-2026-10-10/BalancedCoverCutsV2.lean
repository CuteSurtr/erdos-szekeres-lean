import BalancedProof.Catalog
import ErdosSzekeres.Omission.CoverCuts
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace BalancedCoverCutsV2
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000
-- Original catalog SHA-256: 23363c9e341a7edf4de28b6bf21970983cc6d4cafa6f2bdef54ce3d25b1c5a94
-- Each derived row is proved from original rows by a strict integer margin.
def support0 : Finset (Fin 252) := {136, 154, 174, 178, 188, 189, 194, 203, 208, 209, 216, 218, 220, 228}
theorem cut0 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support0, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 150, OmissionBalanced.support 112, OmissionBalanced.support 111] ![OmissionBalanced.demand 150, OmissionBalanced.demand 112, OmissionBalanced.demand 111] ![1, 1, 1]
    support0 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 150) (Fin.cases (hrows 112) (Fin.cases (hrows 111) (fun i => Fin.elim0 i))))
#print axioms cut0
def support1 : Finset (Fin 252) := {136, 154, 174, 178, 189, 194, 202, 208, 209, 215, 220, 225, 227, 235}
theorem cut1 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support1, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 114, OmissionBalanced.support 154, OmissionBalanced.support 113] ![OmissionBalanced.demand 114, OmissionBalanced.demand 154, OmissionBalanced.demand 113] ![1, 1, 1]
    support1 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 114) (Fin.cases (hrows 154) (Fin.cases (hrows 113) (fun i => Fin.elim0 i))))
def support2 : Finset (Fin 252) := {14, 20, 21, 29, 35, 40, 47, 48, 57, 62, 77, 78, 90, 112}
theorem cut2 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support2, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 42, OmissionBalanced.support 45, OmissionBalanced.support 60] ![OmissionBalanced.demand 42, OmissionBalanced.demand 45, OmissionBalanced.demand 60] ![1, 1, 1]
    support2 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 42) (Fin.cases (hrows 45) (Fin.cases (hrows 60) (fun i => Fin.elim0 i))))
def support3 : Finset (Fin 252) := {23, 31, 32, 35, 42, 47, 48, 55, 57, 62, 77, 78, 90, 112}
theorem cut3 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support3, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 68, OmissionBalanced.support 1278, OmissionBalanced.support 74] ![OmissionBalanced.demand 68, OmissionBalanced.demand 1278, OmissionBalanced.demand 74] ![1, 1, 1]
    support3 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 68) (Fin.cases (hrows 1278) (Fin.cases (hrows 74) (fun i => Fin.elim0 i))))
def support4 : Finset (Fin 252) := {8, 13, 23, 25, 31, 35, 40, 47, 48, 55, 62, 72, 75, 93}
theorem cut4 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support4, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 67, OmissionBalanced.support 27, OmissionBalanced.support 26] ![OmissionBalanced.demand 67, OmissionBalanced.demand 27, OmissionBalanced.demand 26] ![1, 1, 1]
    support4 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 67) (Fin.cases (hrows 27) (Fin.cases (hrows 26) (fun i => Fin.elim0 i))))
def support5 : Finset (Fin 252) := {16, 24, 26, 31, 36, 42, 43, 49, 57, 62, 73, 77, 97, 115}
theorem cut5 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support5, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 59, OmissionBalanced.support 56, OmissionBalanced.support 72] ![OmissionBalanced.demand 59, OmissionBalanced.demand 56, OmissionBalanced.demand 72] ![1, 1, 1]
    support5 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 59) (Fin.cases (hrows 56) (Fin.cases (hrows 72) (fun i => Fin.elim0 i))))
def support6 : Finset (Fin 252) := {23, 31, 33, 35, 42, 43, 48, 57, 62, 63, 73, 77, 97, 115}
theorem cut6 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support6, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 66, OmissionBalanced.support 1278, OmissionBalanced.support 78] ![OmissionBalanced.demand 66, OmissionBalanced.demand 1278, OmissionBalanced.demand 78] ![1, 1, 1]
    support6 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 66) (Fin.cases (hrows 1278) (Fin.cases (hrows 78) (fun i => Fin.elim0 i))))
def support7 : Finset (Fin 252) := {139, 161, 173, 174, 189, 194, 196, 203, 204, 209, 216, 219, 220, 228}
theorem cut7 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support7, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 150, OmissionBalanced.support 119, OmissionBalanced.support 117] ![OmissionBalanced.demand 150, OmissionBalanced.demand 119, OmissionBalanced.demand 117] ![1, 1, 1]
    support7 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 150) (Fin.cases (hrows 119) (Fin.cases (hrows 117) (fun i => Fin.elim0 i))))
def support8 : Finset (Fin 252) := {139, 161, 173, 174, 189, 194, 203, 204, 211, 216, 222, 230, 231, 237}
theorem cut8 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support8, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 120, OmissionBalanced.support 152, OmissionBalanced.support 118] ![OmissionBalanced.demand 120, OmissionBalanced.demand 152, OmissionBalanced.demand 118] ![1, 1, 1]
    support8 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 120) (Fin.cases (hrows 152) (Fin.cases (hrows 118) (fun i => Fin.elim0 i))))
def support9 : Finset (Fin 252) := {5, 13, 16, 17, 26, 29, 31, 36, 42, 47, 57, 60, 62, 77}
theorem cut9 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support9, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 56, OmissionBalanced.support 20, OmissionBalanced.support 19] ![OmissionBalanced.demand 56, OmissionBalanced.demand 20, OmissionBalanced.demand 19] ![1, 1, 1]
    support9 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 56) (Fin.cases (hrows 20) (Fin.cases (hrows 19) (fun i => Fin.elim0 i))))
def support10 : Finset (Fin 252) := {8, 13, 23, 25, 29, 31, 35, 42, 47, 48, 57, 60, 62, 77}
theorem cut10 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support10, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 25, OmissionBalanced.support 1278, OmissionBalanced.support 24] ![OmissionBalanced.demand 25, OmissionBalanced.demand 1278, OmissionBalanced.demand 24] ![1, 1, 1]
    support10 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 25) (Fin.cases (hrows 1278) (Fin.cases (hrows 24) (fun i => Fin.elim0 i))))
def support11 : Finset (Fin 252) := {1, 5, 7, 11, 13, 17, 20, 22, 25, 26, 31, 34, 35, 46}
theorem cut11 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support11, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 4, OmissionBalanced.support 3, OmissionBalanced.support 17] ![OmissionBalanced.demand 4, OmissionBalanced.demand 3, OmissionBalanced.demand 17] ![1, 1, 1]
    support11 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 4) (Fin.cases (hrows 3) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support12 : Finset (Fin 252) := {5, 9, 13, 17, 20, 26, 29, 31, 35, 36, 46, 57, 62, 77}
theorem cut12 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support12, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 34, OmissionBalanced.support 20, OmissionBalanced.support 17] ![OmissionBalanced.demand 34, OmissionBalanced.demand 20, OmissionBalanced.demand 17] ![1, 1, 1]
    support12 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 34) (Fin.cases (hrows 20) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support13 : Finset (Fin 252) := {0, 1, 5, 7, 11, 13, 17, 20, 22, 25, 26, 31, 34, 35, 46}
theorem cut13 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support13, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 4, OmissionBalanced.support 2, OmissionBalanced.support 17] ![OmissionBalanced.demand 4, OmissionBalanced.demand 2, OmissionBalanced.demand 17] ![1, 1, 1]
    support13 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 4) (Fin.cases (hrows 2) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support14 : Finset (Fin 252) := {0, 2, 3, 7, 11, 13, 17, 20, 22, 25, 26, 31, 34, 35, 46}
theorem cut14 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support14, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 6, OmissionBalanced.support 2, OmissionBalanced.support 10] ![OmissionBalanced.demand 6, OmissionBalanced.demand 2, OmissionBalanced.demand 10] ![1, 1, 1]
    support14 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 6) (Fin.cases (hrows 2) (Fin.cases (hrows 10) (fun i => Fin.elim0 i))))
def support15 : Finset (Fin 252) := {1, 2, 3, 7, 11, 13, 17, 20, 22, 25, 26, 31, 34, 35, 46}
theorem cut15 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support15, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 6, OmissionBalanced.support 3, OmissionBalanced.support 10] ![OmissionBalanced.demand 6, OmissionBalanced.demand 3, OmissionBalanced.demand 10] ![1, 1, 1]
    support15 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 6) (Fin.cases (hrows 3) (Fin.cases (hrows 10) (fun i => Fin.elim0 i))))
def support16 : Finset (Fin 252) := {205, 216, 217, 220, 225, 226, 229, 231, 234, 238, 240, 244, 246, 250}
theorem cut16 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support16, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 179, OmissionBalanced.support 176, OmissionBalanced.support 180] ![OmissionBalanced.demand 179, OmissionBalanced.demand 176, OmissionBalanced.demand 180] ![1, 1, 1]
    support16 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 179) (Fin.cases (hrows 176) (Fin.cases (hrows 180) (fun i => Fin.elim0 i))))
def support17 : Finset (Fin 252) := {205, 216, 217, 220, 225, 226, 229, 231, 234, 238, 240, 244, 246, 250, 251}
theorem cut17 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support17, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 179, OmissionBalanced.support 176, OmissionBalanced.support 181] ![OmissionBalanced.demand 179, OmissionBalanced.demand 176, OmissionBalanced.demand 181] ![1, 1, 1]
    support17 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 179) (Fin.cases (hrows 176) (Fin.cases (hrows 181) (fun i => Fin.elim0 i))))
def support18 : Finset (Fin 252) := {205, 216, 217, 220, 225, 226, 229, 231, 234, 238, 240, 244, 248, 249, 250}
theorem cut18 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support18, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 177, OmissionBalanced.support 180, OmissionBalanced.support 178] ![OmissionBalanced.demand 177, OmissionBalanced.demand 180, OmissionBalanced.demand 178] ![1, 1, 1]
    support18 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 180) (Fin.cases (hrows 178) (fun i => Fin.elim0 i))))
def support19 : Finset (Fin 252) := {205, 216, 217, 220, 225, 226, 229, 231, 234, 238, 240, 244, 248, 249, 251}
theorem cut19 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support19, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 177, OmissionBalanced.support 181, OmissionBalanced.support 178] ![OmissionBalanced.demand 177, OmissionBalanced.demand 181, OmissionBalanced.demand 178] ![1, 1, 1]
    support19 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 181) (Fin.cases (hrows 178) (fun i => Fin.elim0 i))))
def support20 : Finset (Fin 252) := {174, 189, 194, 205, 215, 216, 220, 222, 225, 231, 234, 238, 242, 246}
theorem cut20 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support20, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 176, OmissionBalanced.support 157, OmissionBalanced.support 156] ![OmissionBalanced.demand 176, OmissionBalanced.demand 157, OmissionBalanced.demand 156] ![1, 1, 1]
    support20 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 176) (Fin.cases (hrows 157) (Fin.cases (hrows 156) (fun i => Fin.elim0 i))))
def support21 : Finset (Fin 252) := {174, 189, 191, 194, 203, 204, 209, 216, 220, 222, 226, 228, 238, 243}
theorem cut21 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support21, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 150, OmissionBalanced.support 153, OmissionBalanced.support 169] ![OmissionBalanced.demand 150, OmissionBalanced.demand 153, OmissionBalanced.demand 169] ![1, 1, 1]
    support21 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 150) (Fin.cases (hrows 153) (Fin.cases (hrows 169) (fun i => Fin.elim0 i))))
def support22 : Finset (Fin 252) := {174, 189, 191, 194, 204, 209, 215, 220, 222, 225, 234, 235, 238, 246}
theorem cut22 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support22, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 171, OmissionBalanced.support 154, OmissionBalanced.support 157] ![OmissionBalanced.demand 171, OmissionBalanced.demand 154, OmissionBalanced.demand 157] ![1, 1, 1]
    support22 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 171) (Fin.cases (hrows 154) (Fin.cases (hrows 157) (fun i => Fin.elim0 i))))
def support23 : Finset (Fin 252) := {5, 13, 14, 17, 20, 29, 35, 36, 43, 48, 57, 61, 62, 77}
theorem cut23 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support23, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 42, OmissionBalanced.support 20, OmissionBalanced.support 18] ![OmissionBalanced.demand 42, OmissionBalanced.demand 20, OmissionBalanced.demand 18] ![1, 1, 1]
    support23 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 42) (Fin.cases (hrows 20) (Fin.cases (hrows 18) (fun i => Fin.elim0 i))))
def support24 : Finset (Fin 252) := {10, 17, 22, 23, 31, 35, 36, 42, 43, 48, 57, 61, 62, 77}
theorem cut24 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support24, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1278, OmissionBalanced.support 38, OmissionBalanced.support 40] ![OmissionBalanced.demand 1278, OmissionBalanced.demand 38, OmissionBalanced.demand 40] ![1, 1, 1]
    support24 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1278) (Fin.cases (hrows 38) (Fin.cases (hrows 40) (fun i => Fin.elim0 i))))
def support25 : Finset (Fin 252) := {174, 189, 190, 194, 203, 208, 209, 215, 216, 220, 228, 229, 234, 241}
theorem cut25 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support25, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 150, OmissionBalanced.support 165, OmissionBalanced.support 155] ![OmissionBalanced.demand 150, OmissionBalanced.demand 165, OmissionBalanced.demand 155] ![1, 1, 1]
    support25 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 150) (Fin.cases (hrows 165) (Fin.cases (hrows 155) (fun i => Fin.elim0 i))))
#print axioms cut25
def support26 : Finset (Fin 252) := {174, 189, 190, 194, 203, 208, 215, 216, 222, 231, 234, 237, 238, 246}
theorem cut26 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support26, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 167, OmissionBalanced.support 152, OmissionBalanced.support 157] ![OmissionBalanced.demand 167, OmissionBalanced.demand 152, OmissionBalanced.demand 157] ![1, 1, 1]
    support26 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 167) (Fin.cases (hrows 152) (Fin.cases (hrows 157) (fun i => Fin.elim0 i))))
def support27 : Finset (Fin 252) := {81, 118, 135, 143, 154, 161, 171, 173, 178, 179, 189, 193, 194, 207}
theorem cut27 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support27, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 102, OmissionBalanced.support 93, OmissionBalanced.support 92] ![OmissionBalanced.demand 102, OmissionBalanced.demand 93, OmissionBalanced.demand 92] ![1, 1, 1]
    support27 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 102) (Fin.cases (hrows 93) (Fin.cases (hrows 92) (fun i => Fin.elim0 i))))
def support28 : Finset (Fin 252) := {44, 57, 58, 62, 72, 73, 78, 80, 90, 97, 108, 116, 133, 170}
theorem cut28 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support28, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 87, OmissionBalanced.support 82, OmissionBalanced.support 85] ![OmissionBalanced.demand 87, OmissionBalanced.demand 82, OmissionBalanced.demand 85] ![1, 1, 1]
    support28 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 87) (Fin.cases (hrows 82) (Fin.cases (hrows 85) (fun i => Fin.elim0 i))))
def support29 : Finset (Fin 252) := {155, 171, 172, 188, 194, 202, 208, 209, 216, 220, 228, 229, 234, 241}
theorem cut29 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support29, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 127, OmissionBalanced.support 130, OmissionBalanced.support 148] ![OmissionBalanced.demand 127, OmissionBalanced.demand 130, OmissionBalanced.demand 148] ![1, 1, 1]
    support29 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 127) (Fin.cases (hrows 130) (Fin.cases (hrows 148) (fun i => Fin.elim0 i))))
def support30 : Finset (Fin 252) := {158, 176, 179, 189, 196, 203, 204, 211, 216, 220, 226, 228, 238, 243}
theorem cut30 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support30, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 138, OmissionBalanced.support 135, OmissionBalanced.support 158] ![OmissionBalanced.demand 138, OmissionBalanced.demand 135, OmissionBalanced.demand 158] ![1, 1, 1]
    support30 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 138) (Fin.cases (hrows 135) (Fin.cases (hrows 158) (fun i => Fin.elim0 i))))
def support31 : Finset (Fin 252) := {10, 17, 22, 23, 31, 35, 42, 43, 49, 57, 63, 79, 80, 96}
theorem cut31 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support31, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 65, OmissionBalanced.support 41, OmissionBalanced.support 39] ![OmissionBalanced.demand 65, OmissionBalanced.demand 41, OmissionBalanced.demand 39] ![1, 1, 1]
    support31 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 65) (Fin.cases (hrows 41) (Fin.cases (hrows 39) (fun i => Fin.elim0 i))))
def support32 : Finset (Fin 252) := {23, 31, 33, 35, 43, 48, 55, 62, 63, 72, 90, 93, 97, 133}
theorem cut32 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support32, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 67, OmissionBalanced.support 80, OmissionBalanced.support 70] ![OmissionBalanced.demand 67, OmissionBalanced.demand 80, OmissionBalanced.demand 70] ![1, 1, 1]
    support32 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 67) (Fin.cases (hrows 80) (Fin.cases (hrows 70) (fun i => Fin.elim0 i))))
def support33 : Finset (Fin 252) := {118, 154, 158, 161, 179, 188, 189, 196, 203, 208, 216, 218, 220, 228}
theorem cut33 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support33, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 135, OmissionBalanced.support 104, OmissionBalanced.support 105] ![OmissionBalanced.demand 135, OmissionBalanced.demand 104, OmissionBalanced.demand 105] ![1, 1, 1]
    support33 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 135) (Fin.cases (hrows 104) (Fin.cases (hrows 105) (fun i => Fin.elim0 i))))
def support34 : Finset (Fin 252) := {118, 154, 155, 161, 171, 188, 194, 196, 204, 209, 216, 219, 220, 228}
theorem cut34 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support34, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 127, OmissionBalanced.support 103, OmissionBalanced.support 105] ![OmissionBalanced.demand 127, OmissionBalanced.demand 103, OmissionBalanced.demand 105] ![1, 1, 1]
    support34 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 127) (Fin.cases (hrows 103) (Fin.cases (hrows 105) (fun i => Fin.elim0 i))))
def support35 : Finset (Fin 252) := {23, 31, 32, 35, 42, 47, 55, 57, 63, 80, 90, 96, 97, 133}
theorem cut35 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support35, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 65, OmissionBalanced.support 76, OmissionBalanced.support 70] ![OmissionBalanced.demand 65, OmissionBalanced.demand 76, OmissionBalanced.demand 70] ![1, 1, 1]
    support35 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 65) (Fin.cases (hrows 76) (Fin.cases (hrows 70) (fun i => Fin.elim0 i))))
def support36 : Finset (Fin 252) := {23, 31, 35, 44, 55, 57, 62, 63, 72, 80, 90, 97, 114, 133}
theorem cut36 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support36, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 82, OmissionBalanced.support 69, OmissionBalanced.support 70] ![OmissionBalanced.demand 82, OmissionBalanced.demand 69, OmissionBalanced.demand 70] ![1, 1, 1]
    support36 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 82) (Fin.cases (hrows 69) (Fin.cases (hrows 70) (fun i => Fin.elim0 i))))
def support37 : Finset (Fin 252) := {118, 137, 154, 161, 171, 179, 188, 189, 194, 196, 207, 216, 220, 228}
theorem cut37 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support37, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 102, OmissionBalanced.support 115, OmissionBalanced.support 105] ![OmissionBalanced.demand 102, OmissionBalanced.demand 115, OmissionBalanced.demand 105] ![1, 1, 1]
    support37 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 102) (Fin.cases (hrows 115) (Fin.cases (hrows 105) (fun i => Fin.elim0 i))))
def support38 : Finset (Fin 252) := {120, 137, 155, 163, 171, 172, 181, 188, 194, 209, 217, 221, 226, 229, 236}
theorem cut38 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support38, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 893, OmissionBalanced.support 128, OmissionBalanced.support 895] ![OmissionBalanced.demand 893, OmissionBalanced.demand 128, OmissionBalanced.demand 895] ![1, 1, 1]
    support38 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 893) (Fin.cases (hrows 128) (Fin.cases (hrows 895) (fun i => Fin.elim0 i))))
def support39 : Finset (Fin 252) := {120, 137, 155, 163, 171, 172, 181, 188, 194, 205, 209, 210, 216, 220, 228}
theorem cut39 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support39, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 127, OmissionBalanced.support 892, OmissionBalanced.support 894] ![OmissionBalanced.demand 127, OmissionBalanced.demand 892, OmissionBalanced.demand 894] ![1, 1, 1]
    support39 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 127) (Fin.cases (hrows 892) (Fin.cases (hrows 894) (fun i => Fin.elim0 i))))
def support40 : Finset (Fin 252) := {32, 42, 47, 55, 60, 62, 66, 75, 78, 90, 104, 112, 123, 133, 159}
theorem cut40 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support40, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 74, OmissionBalanced.support 529, OmissionBalanced.support 418] ![OmissionBalanced.demand 74, OmissionBalanced.demand 529, OmissionBalanced.demand 418] ![1, 1, 1]
    support40 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 74) (Fin.cases (hrows 529) (Fin.cases (hrows 418) (fun i => Fin.elim0 i))))
def support41 : Finset (Fin 252) := {15, 22, 25, 34, 37, 48, 55, 62, 72, 75, 85, 93, 104, 114, 140}
theorem cut41 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support41, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 51, OmissionBalanced.support 373, OmissionBalanced.support 289] ![OmissionBalanced.demand 51, OmissionBalanced.demand 373, OmissionBalanced.demand 289] ![1, 1, 1]
    support41 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 51) (Fin.cases (hrows 373) (Fin.cases (hrows 289) (fun i => Fin.elim0 i))))
def support42 : Finset (Fin 252) := {32, 42, 47, 55, 60, 62, 66, 75, 78, 104, 108, 123, 130, 151, 175}
theorem cut42 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support42, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 75, OmissionBalanced.support 530, OmissionBalanced.support 419] ![OmissionBalanced.demand 75, OmissionBalanced.demand 530, OmissionBalanced.demand 419] ![1, 1, 1]
    support42 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 75) (Fin.cases (hrows 530) (Fin.cases (hrows 419) (fun i => Fin.elim0 i))))
def support43 : Finset (Fin 252) := {76, 100, 121, 128, 143, 147, 173, 176, 185, 189, 191, 196, 204, 209, 219}
theorem cut43 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support43, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 106, OmissionBalanced.support 701, OmissionBalanced.support 703] ![OmissionBalanced.demand 106, OmissionBalanced.demand 701, OmissionBalanced.demand 703] ![1, 1, 1]
    support43 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 106) (Fin.cases (hrows 701) (Fin.cases (hrows 703) (fun i => Fin.elim0 i))))
def support44 : Finset (Fin 252) := {92, 118, 128, 139, 147, 161, 173, 176, 185, 189, 191, 196, 204, 209, 219}
theorem cut44 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support44, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 777, OmissionBalanced.support 117, OmissionBalanced.support 781] ![OmissionBalanced.demand 777, OmissionBalanced.demand 117, OmissionBalanced.demand 781] ![1, 1, 1]
    support44 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 777) (Fin.cases (hrows 117) (Fin.cases (hrows 781) (fun i => Fin.elim0 i))))
def support45 : Finset (Fin 252) := {23, 31, 35, 46, 48, 51, 55, 62, 72, 75, 85, 93, 104, 114, 140}
theorem cut45 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support45, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 67, OmissionBalanced.support 447, OmissionBalanced.support 349] ![OmissionBalanced.demand 67, OmissionBalanced.demand 447, OmissionBalanced.demand 349] ![1, 1, 1]
    support45 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 67) (Fin.cases (hrows 447) (Fin.cases (hrows 349) (fun i => Fin.elim0 i))))
def support46 : Finset (Fin 252) := {15, 22, 25, 30, 34, 42, 57, 63, 70, 79, 80, 88, 96, 114, 131}
theorem cut46 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support46, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 337, OmissionBalanced.support 50, OmissionBalanced.support 293] ![OmissionBalanced.demand 337, OmissionBalanced.demand 50, OmissionBalanced.demand 293] ![1, 1, 1]
    support46 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 337) (Fin.cases (hrows 50) (Fin.cases (hrows 293) (fun i => Fin.elim0 i))))
def support47 : Finset (Fin 252) := {33, 43, 48, 56, 57, 61, 63, 73, 79, 88, 107, 116, 134, 153, 169}
theorem cut47 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support47, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 79, OmissionBalanced.support 497, OmissionBalanced.support 435] ![OmissionBalanced.demand 79, OmissionBalanced.demand 497, OmissionBalanced.demand 435] ![1, 1, 1]
    support47 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 79) (Fin.cases (hrows 497) (Fin.cases (hrows 435) (fun i => Fin.elim0 i))))
def support48 : Finset (Fin 252) := {23, 31, 35, 41, 42, 46, 57, 63, 70, 79, 80, 88, 96, 114, 131}
theorem cut48 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support48, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 404, OmissionBalanced.support 65, OmissionBalanced.support 356] ![OmissionBalanced.demand 404, OmissionBalanced.demand 65, OmissionBalanced.demand 356] ![1, 1, 1]
    support48 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 404) (Fin.cases (hrows 65) (Fin.cases (hrows 356) (fun i => Fin.elim0 i))))
def support49 : Finset (Fin 252) := {23, 31, 35, 41, 42, 46, 63, 70, 73, 79, 97, 107, 115, 133, 150}
theorem cut49 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support49, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 66, OmissionBalanced.support 405, OmissionBalanced.support 357] ![OmissionBalanced.demand 66, OmissionBalanced.demand 405, OmissionBalanced.demand 357] ![1, 1, 1]
    support49 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 66) (Fin.cases (hrows 405) (Fin.cases (hrows 357) (fun i => Fin.elim0 i))))
def support50 : Finset (Fin 252) := {82, 98, 117, 135, 144, 163, 172, 178, 188, 190, 194, 195, 203, 208, 218}
theorem cut50 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support50, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 100, OmissionBalanced.support 742, OmissionBalanced.support 744] ![OmissionBalanced.demand 100, OmissionBalanced.demand 742, OmissionBalanced.demand 744] ![1, 1, 1]
    support50 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 100) (Fin.cases (hrows 742) (Fin.cases (hrows 744) (fun i => Fin.elim0 i))))
#print axioms cut50
def support51 : Finset (Fin 252) := {92, 118, 128, 139, 161, 166, 173, 176, 196, 200, 203, 205, 216, 220, 228}
theorem cut51 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support51, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 119, OmissionBalanced.support 779, OmissionBalanced.support 783] ![OmissionBalanced.demand 119, OmissionBalanced.demand 779, OmissionBalanced.demand 783] ![1, 1, 1]
    support51 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 119) (Fin.cases (hrows 779) (Fin.cases (hrows 783) (fun i => Fin.elim0 i))))
def support52 : Finset (Fin 252) := {23, 31, 35, 46, 48, 51, 55, 75, 78, 85, 90, 112, 123, 133, 159}
theorem cut52 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support52, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 68, OmissionBalanced.support 448, OmissionBalanced.support 350] ![OmissionBalanced.demand 68, OmissionBalanced.demand 448, OmissionBalanced.demand 350] ![1, 1, 1]
    support52 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 68) (Fin.cases (hrows 448) (Fin.cases (hrows 350) (fun i => Fin.elim0 i))))
def support53 : Finset (Fin 252) := {101, 118, 136, 144, 154, 163, 172, 178, 188, 190, 194, 195, 203, 208, 218}
theorem cut53 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support53, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 824, OmissionBalanced.support 111, OmissionBalanced.support 827] ![OmissionBalanced.demand 824, OmissionBalanced.demand 111, OmissionBalanced.demand 827] ![1, 1, 1]
    support53 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 824) (Fin.cases (hrows 111) (Fin.cases (hrows 827) (fun i => Fin.elim0 i))))
def support54 : Finset (Fin 252) := {101, 118, 136, 144, 154, 172, 178, 181, 188, 205, 209, 210, 216, 220, 228}
theorem cut54 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support54, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 112, OmissionBalanced.support 825, OmissionBalanced.support 829] ![OmissionBalanced.demand 112, OmissionBalanced.demand 825, OmissionBalanced.demand 829] ![1, 1, 1]
    support54 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 112) (Fin.cases (hrows 825) (Fin.cases (hrows 829) (fun i => Fin.elim0 i))))
def support55 : Finset (Fin 252) := {111, 137, 147, 158, 166, 176, 179, 189, 196, 203, 214, 217, 226, 229, 236}
theorem cut55 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support55, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 136, OmissionBalanced.support 856, OmissionBalanced.support 858] ![OmissionBalanced.demand 136, OmissionBalanced.demand 856, OmissionBalanced.demand 858] ![1, 1, 1]
    support55 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 136) (Fin.cases (hrows 856) (Fin.cases (hrows 858) (fun i => Fin.elim0 i))))
def support56 : Finset (Fin 252) := {33, 43, 48, 56, 57, 61, 63, 73, 79, 88, 97, 107, 115, 133, 150}
theorem cut56 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support56, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 496, OmissionBalanced.support 78, OmissionBalanced.support 434] ![OmissionBalanced.demand 496, OmissionBalanced.demand 78, OmissionBalanced.demand 434] ![1, 1, 1]
    support56 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 496) (Fin.cases (hrows 78) (Fin.cases (hrows 434) (fun i => Fin.elim0 i))))
def support57 : Finset (Fin 252) := {111, 137, 147, 158, 166, 176, 179, 189, 196, 200, 203, 205, 216, 220, 228}
theorem cut57 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support57, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 135, OmissionBalanced.support 855, OmissionBalanced.support 857] ![OmissionBalanced.demand 135, OmissionBalanced.demand 855, OmissionBalanced.demand 857] ![1, 1, 1]
    support57 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 135) (Fin.cases (hrows 855) (Fin.cases (hrows 857) (fun i => Fin.elim0 i))))
def support58 : Finset (Fin 252) := {64, 81, 118, 135, 143, 154, 161, 171, 173, 178, 179, 189, 193, 194, 207}
theorem cut58 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support58, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 90, OmissionBalanced.support 102, OmissionBalanced.support 93] ![OmissionBalanced.demand 90, OmissionBalanced.demand 102, OmissionBalanced.demand 93] ![1, 1, 1]
    support58 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 90) (Fin.cases (hrows 102) (Fin.cases (hrows 93) (fun i => Fin.elim0 i))))
def support59 : Finset (Fin 252) := {44, 57, 58, 62, 72, 73, 78, 80, 90, 97, 108, 116, 133, 170, 187}
theorem cut59 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support59, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 88, OmissionBalanced.support 82, OmissionBalanced.support 85] ![OmissionBalanced.demand 88, OmissionBalanced.demand 82, OmissionBalanced.demand 85] ![1, 1, 1]
    support59 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 88) (Fin.cases (hrows 82) (Fin.cases (hrows 85) (fun i => Fin.elim0 i))))
def support60 : Finset (Fin 252) := {64, 98, 100, 135, 143, 154, 161, 171, 173, 178, 179, 189, 193, 194, 207}
theorem cut60 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support60, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 90, OmissionBalanced.support 97, OmissionBalanced.support 94] ![OmissionBalanced.demand 90, OmissionBalanced.demand 97, OmissionBalanced.demand 94] ![1, 1, 1]
    support60 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 90) (Fin.cases (hrows 97) (Fin.cases (hrows 94) (fun i => Fin.elim0 i))))
def support61 : Finset (Fin 252) := {81, 98, 100, 135, 143, 154, 161, 171, 173, 178, 179, 189, 193, 194, 207}
theorem cut61 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support61, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 92, OmissionBalanced.support 97, OmissionBalanced.support 94] ![OmissionBalanced.demand 92, OmissionBalanced.demand 97, OmissionBalanced.demand 94] ![1, 1, 1]
    support61 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 92) (Fin.cases (hrows 97) (Fin.cases (hrows 94) (fun i => Fin.elim0 i))))
def support62 : Finset (Fin 252) := {44, 57, 58, 62, 72, 73, 78, 80, 90, 97, 108, 116, 151, 153, 187}
theorem cut62 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support62, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 88, OmissionBalanced.support 83, OmissionBalanced.support 84] ![OmissionBalanced.demand 88, OmissionBalanced.demand 83, OmissionBalanced.demand 84] ![1, 1, 1]
    support62 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 88) (Fin.cases (hrows 83) (Fin.cases (hrows 84) (fun i => Fin.elim0 i))))
def support63 : Finset (Fin 252) := {44, 57, 58, 62, 72, 73, 78, 80, 90, 97, 108, 116, 151, 153, 170}
theorem cut63 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support63, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 87, OmissionBalanced.support 83, OmissionBalanced.support 84] ![OmissionBalanced.demand 87, OmissionBalanced.demand 83, OmissionBalanced.demand 84] ![1, 1, 1]
    support63 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 87) (Fin.cases (hrows 83) (Fin.cases (hrows 84) (fun i => Fin.elim0 i))))
def support64 : Finset (Fin 252) := {44, 57, 71, 72, 77, 84, 88, 90, 96, 104, 107, 115, 123, 133, 150, 159, 174}
theorem cut64 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support64, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 512, OmissionBalanced.support 504, OmissionBalanced.support 582] ![OmissionBalanced.demand 512, OmissionBalanced.demand 504, OmissionBalanced.demand 582] ![1, 1, 1]
    support64 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 512) (Fin.cases (hrows 504) (Fin.cases (hrows 582) (fun i => Fin.elim0 i))))
def support65 : Finset (Fin 252) := {44, 57, 62, 71, 72, 77, 80, 88, 90, 96, 97, 115, 127, 133, 151, 168}
theorem cut65 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support65, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 584, OmissionBalanced.support 509, OmissionBalanced.support 82] ![OmissionBalanced.demand 584, OmissionBalanced.demand 509, OmissionBalanced.demand 82] ![1, 1, 1]
    support65 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 584) (Fin.cases (hrows 509) (Fin.cases (hrows 82) (fun i => Fin.elim0 i))))
def support66 : Finset (Fin 252) := {33, 43, 44, 48, 57, 62, 63, 72, 73, 80, 90, 97, 116, 133, 134}
theorem cut66 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support66, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 79, OmissionBalanced.support 82, OmissionBalanced.support 80] ![OmissionBalanced.demand 79, OmissionBalanced.demand 82, OmissionBalanced.demand 80] ![1, 1, 1]
    support66 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 79) (Fin.cases (hrows 82) (Fin.cases (hrows 80) (fun i => Fin.elim0 i))))
def support67 : Finset (Fin 252) := {34, 45, 50, 64, 109, 117, 124, 128, 136, 143, 144, 149, 157, 161, 162, 178, 193}
theorem cut67 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support67, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 517, OmissionBalanced.support 558, OmissionBalanced.support 444] ![OmissionBalanced.demand 517, OmissionBalanced.demand 558, OmissionBalanced.demand 444] ![1, 1, 1]
    support67 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 517) (Fin.cases (hrows 558) (Fin.cases (hrows 444) (fun i => Fin.elim0 i))))
def support68 : Finset (Fin 252) := {64, 65, 81, 117, 124, 135, 136, 143, 144, 154, 157, 161, 162, 173, 178, 193}
theorem cut68 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support68, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 655, OmissionBalanced.support 90, OmissionBalanced.support 657] ![OmissionBalanced.demand 655, OmissionBalanced.demand 90, OmissionBalanced.demand 657] ![1, 1, 1]
    support68 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 655) (Fin.cases (hrows 90) (Fin.cases (hrows 657) (fun i => Fin.elim0 i))))
def support69 : Finset (Fin 252) := {46, 59, 65, 81, 109, 117, 124, 128, 136, 143, 144, 149, 157, 161, 162, 178, 193}
theorem cut69 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support69, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 655, OmissionBalanced.support 527, OmissionBalanced.support 607] ![OmissionBalanced.demand 655, OmissionBalanced.demand 527, OmissionBalanced.demand 607] ![1, 1, 1]
    support69 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 655) (Fin.cases (hrows 527) (Fin.cases (hrows 607) (fun i => Fin.elim0 i))))
def support70 : Finset (Fin 252) := {50, 64, 81, 117, 124, 135, 136, 143, 144, 154, 157, 161, 162, 173, 178, 193}
theorem cut70 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support70, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 558, OmissionBalanced.support 92, OmissionBalanced.support 559] ![OmissionBalanced.demand 558, OmissionBalanced.demand 92, OmissionBalanced.demand 559] ![1, 1, 1]
    support70 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 558) (Fin.cases (hrows 92) (Fin.cases (hrows 559) (fun i => Fin.elim0 i))))
def support71 : Finset (Fin 252) := {117, 118, 135, 154, 161, 171, 178, 179, 188, 189, 194, 203, 207, 208, 218}
theorem cut71 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support71, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 102, OmissionBalanced.support 100, OmissionBalanced.support 104] ![OmissionBalanced.demand 102, OmissionBalanced.demand 100, OmissionBalanced.demand 104] ![1, 1, 1]
    support71 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 102) (Fin.cases (hrows 100) (Fin.cases (hrows 104) (fun i => Fin.elim0 i))))
def support72 : Finset (Fin 252) := {46, 59, 65, 81, 109, 117, 124, 143, 147, 155, 163, 167, 174, 179, 180, 194, 207}
theorem cut72 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support72, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 528, OmissionBalanced.support 608, OmissionBalanced.support 656] ![OmissionBalanced.demand 528, OmissionBalanced.demand 608, OmissionBalanced.demand 656] ![1, 1, 1]
    support72 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 528) (Fin.cases (hrows 608) (Fin.cases (hrows 656) (fun i => Fin.elim0 i))))
def support73 : Finset (Fin 252) := {81, 82, 98, 117, 135, 143, 144, 155, 163, 171, 174, 179, 180, 189, 194, 207}
theorem cut73 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support73, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 743, OmissionBalanced.support 93, OmissionBalanced.support 741] ![OmissionBalanced.demand 743, OmissionBalanced.demand 93, OmissionBalanced.demand 741] ![1, 1, 1]
    support73 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 743) (Fin.cases (hrows 93) (Fin.cases (hrows 741) (fun i => Fin.elim0 i))))
def support74 : Finset (Fin 252) := {83, 100, 118, 124, 136, 154, 155, 161, 163, 171, 174, 179, 180, 189, 194, 207}
theorem cut74 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support74, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 747, OmissionBalanced.support 102, OmissionBalanced.support 745] ![OmissionBalanced.demand 747, OmissionBalanced.demand 102, OmissionBalanced.demand 745] ![1, 1, 1]
    support74 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 747) (Fin.cases (hrows 102) (Fin.cases (hrows 745) (fun i => Fin.elim0 i))))
def support75 : Finset (Fin 252) := {77, 92, 101, 118, 128, 136, 144, 147, 155, 161, 163, 167, 174, 179, 180, 194, 207}
theorem cut75 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support75, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 715, OmissionBalanced.support 822, OmissionBalanced.support 780] ![OmissionBalanced.demand 715, OmissionBalanced.demand 822, OmissionBalanced.demand 780] ![1, 1, 1]
    support75 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 715) (Fin.cases (hrows 822) (Fin.cases (hrows 780) (fun i => Fin.elim0 i))))
#print axioms cut75
def support76 : Finset (Fin 252) := {77, 92, 101, 118, 128, 139, 144, 147, 154, 158, 163, 167, 171, 174, 180, 189, 207}
theorem cut76 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support76, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 715, OmissionBalanced.support 826, OmissionBalanced.support 776] ![OmissionBalanced.demand 715, OmissionBalanced.demand 826, OmissionBalanced.demand 776] ![1, 1, 1]
    support76 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 715) (Fin.cases (hrows 826) (Fin.cases (hrows 776) (fun i => Fin.elim0 i))))
def support77 : Finset (Fin 252) := {74, 98, 109, 118, 139, 147, 154, 158, 161, 167, 171, 174, 179, 189, 194, 207}
theorem cut77 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support77, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 691, OmissionBalanced.support 693, OmissionBalanced.support 102] ![OmissionBalanced.demand 691, OmissionBalanced.demand 693, OmissionBalanced.demand 102] ![1, 1, 1]
    support77 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 691) (Fin.cases (hrows 693) (Fin.cases (hrows 102) (fun i => Fin.elim0 i))))
def support78 : Finset (Fin 252) := {118, 121, 143, 154, 161, 171, 173, 179, 189, 194, 196, 204, 207, 209, 219}
theorem cut78 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support78, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 106, OmissionBalanced.support 102, OmissionBalanced.support 103] ![OmissionBalanced.demand 106, OmissionBalanced.demand 102, OmissionBalanced.demand 103] ![1, 1, 1]
    support78 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 106) (Fin.cases (hrows 102) (Fin.cases (hrows 103) (fun i => Fin.elim0 i))))
def support79 : Finset (Fin 252) := {58, 73, 78, 90, 94, 97, 102, 108, 112, 116, 123, 130, 142, 170, 187, 192}
theorem cut79 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support79, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 597, OmissionBalanced.support 88, OmissionBalanced.support 719] ![OmissionBalanced.demand 597, OmissionBalanced.demand 88, OmissionBalanced.demand 719] ![1, 1, 1]
    support79 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 597) (Fin.cases (hrows 88) (Fin.cases (hrows 719) (fun i => Fin.elim0 i))))
def support80 : Finset (Fin 252) := {58, 78, 89, 94, 97, 102, 107, 112, 116, 123, 127, 130, 142, 187, 201, 206, 217}
theorem cut80 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support80, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 600, OmissionBalanced.support 720, OmissionBalanced.support 602] ![OmissionBalanced.demand 600, OmissionBalanced.demand 720, OmissionBalanced.demand 602] ![1, 1, 1]
    support80 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 600) (Fin.cases (hrows 720) (Fin.cases (hrows 602) (fun i => Fin.elim0 i))))
def support81 : Finset (Fin 252) := {58, 78, 89, 94, 97, 102, 107, 112, 116, 123, 127, 130, 142, 170, 186, 192, 205}
theorem cut81 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support81, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 601, OmissionBalanced.support 599, OmissionBalanced.support 719] ![OmissionBalanced.demand 601, OmissionBalanced.demand 599, OmissionBalanced.demand 719] ![1, 1, 1]
    support81 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 601) (Fin.cases (hrows 599) (Fin.cases (hrows 719) (fun i => Fin.elim0 i))))
def support82 : Finset (Fin 252) := {58, 73, 78, 90, 94, 97, 102, 108, 112, 116, 123, 130, 142, 170, 187, 206}
theorem cut82 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support82, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 598, OmissionBalanced.support 720, OmissionBalanced.support 87] ![OmissionBalanced.demand 598, OmissionBalanced.demand 720, OmissionBalanced.demand 87] ![1, 1, 1]
    support82 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 598) (Fin.cases (hrows 720) (Fin.cases (hrows 87) (fun i => Fin.elim0 i))))
def support83 : Finset (Fin 252) := {58, 73, 78, 89, 90, 94, 97, 107, 108, 115, 116, 127, 134, 170, 186, 187}
theorem cut83 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support83, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 599, OmissionBalanced.support 88, OmissionBalanced.support 683] ![OmissionBalanced.demand 599, OmissionBalanced.demand 88, OmissionBalanced.demand 683] ![1, 1, 1]
    support83 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 599) (Fin.cases (hrows 88) (Fin.cases (hrows 683) (fun i => Fin.elim0 i))))
def support84 : Finset (Fin 252) := {58, 73, 89, 90, 94, 102, 107, 108, 115, 123, 127, 134, 142, 187, 201, 206, 217}
theorem cut84 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support84, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 598, OmissionBalanced.support 684, OmissionBalanced.support 602] ![OmissionBalanced.demand 598, OmissionBalanced.demand 684, OmissionBalanced.demand 602] ![1, 1, 1]
    support84 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 598) (Fin.cases (hrows 684) (Fin.cases (hrows 602) (fun i => Fin.elim0 i))))
def support85 : Finset (Fin 252) := {58, 73, 89, 90, 94, 102, 107, 108, 115, 123, 127, 134, 142, 170, 186, 192, 205}
theorem cut85 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support85, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 601, OmissionBalanced.support 597, OmissionBalanced.support 683] ![OmissionBalanced.demand 601, OmissionBalanced.demand 597, OmissionBalanced.demand 683] ![1, 1, 1]
    support85 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 601) (Fin.cases (hrows 597) (Fin.cases (hrows 683) (fun i => Fin.elim0 i))))
def support86 : Finset (Fin 252) := {58, 73, 78, 89, 90, 94, 97, 107, 108, 115, 116, 127, 134, 170, 187, 201}
theorem cut86 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support86, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 600, OmissionBalanced.support 684, OmissionBalanced.support 87] ![OmissionBalanced.demand 600, OmissionBalanced.demand 684, OmissionBalanced.demand 87] ![1, 1, 1]
    support86 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 600) (Fin.cases (hrows 684) (Fin.cases (hrows 87) (fun i => Fin.elim0 i))))
def support87 : Finset (Fin 252) := {44, 57, 71, 72, 77, 84, 88, 96, 104, 108, 127, 134, 142, 170, 186, 192, 205}
theorem cut87 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support87, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 515, OmissionBalanced.support 507, OmissionBalanced.support 585] ![OmissionBalanced.demand 515, OmissionBalanced.demand 507, OmissionBalanced.demand 585] ![1, 1, 1]
    support87 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 515) (Fin.cases (hrows 507) (Fin.cases (hrows 585) (fun i => Fin.elim0 i))))
def support88 : Finset (Fin 252) := {44, 57, 62, 71, 72, 77, 80, 88, 96, 107, 108, 116, 134, 153, 169, 170}
theorem cut88 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support88, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 510, OmissionBalanced.support 85, OmissionBalanced.support 583] ![OmissionBalanced.demand 510, OmissionBalanced.demand 85, OmissionBalanced.demand 583] ![1, 1, 1]
    support88 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 510) (Fin.cases (hrows 85) (Fin.cases (hrows 583) (fun i => Fin.elim0 i))))
def support89 : Finset (Fin 252) := {61, 76, 83, 100, 124, 128, 136, 143, 147, 155, 163, 167, 174, 179, 180, 194, 207}
theorem cut89 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support89, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 628, OmissionBalanced.support 702, OmissionBalanced.support 745] ![OmissionBalanced.demand 628, OmissionBalanced.demand 702, OmissionBalanced.demand 745] ![1, 1, 1]
    support89 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 628) (Fin.cases (hrows 702) (Fin.cases (hrows 745) (fun i => Fin.elim0 i))))
def support90 : Finset (Fin 252) := {100, 101, 118, 136, 143, 144, 154, 155, 163, 171, 174, 179, 180, 189, 194, 207}
theorem cut90 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support90, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 826, OmissionBalanced.support 822, OmissionBalanced.support 97] ![OmissionBalanced.demand 826, OmissionBalanced.demand 822, OmissionBalanced.demand 97] ![1, 1, 1]
    support90 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 826) (Fin.cases (hrows 822) (Fin.cases (hrows 97) (fun i => Fin.elim0 i))))
def support91 : Finset (Fin 252) := {44, 62, 71, 77, 80, 84, 88, 93, 97, 104, 107, 112, 123, 133, 150, 159, 174}
theorem cut91 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support91, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 512, OmissionBalanced.support 630, OmissionBalanced.support 508] ![OmissionBalanced.demand 512, OmissionBalanced.demand 630, OmissionBalanced.demand 508] ![1, 1, 1]
    support91 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 512) (Fin.cases (hrows 630) (Fin.cases (hrows 508) (fun i => Fin.elim0 i))))
def support92 : Finset (Fin 252) := {32, 42, 44, 47, 55, 57, 62, 72, 78, 80, 90, 97, 108, 130, 133}
theorem cut92 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support92, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 75, OmissionBalanced.support 82, OmissionBalanced.support 76] ![OmissionBalanced.demand 75, OmissionBalanced.demand 82, OmissionBalanced.demand 76] ![1, 1, 1]
    support92 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 75) (Fin.cases (hrows 82) (Fin.cases (hrows 76) (fun i => Fin.elim0 i))))
def support93 : Finset (Fin 252) := {44, 57, 62, 72, 77, 80, 84, 90, 93, 97, 104, 112, 133, 142, 153, 177}
theorem cut93 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support93, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 505, OmissionBalanced.support 631, OmissionBalanced.support 82] ![OmissionBalanced.demand 505, OmissionBalanced.demand 631, OmissionBalanced.demand 82] ![1, 1, 1]
    support93 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 505) (Fin.cases (hrows 631) (Fin.cases (hrows 82) (fun i => Fin.elim0 i))))
def support94 : Finset (Fin 252) := {44, 57, 71, 72, 77, 84, 88, 96, 104, 108, 115, 123, 127, 151, 168, 175, 190}
theorem cut94 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support94, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 514, OmissionBalanced.support 584, OmissionBalanced.support 506] ![OmissionBalanced.demand 514, OmissionBalanced.demand 584, OmissionBalanced.demand 506] ![1, 1, 1]
    support94 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 514) (Fin.cases (hrows 584) (Fin.cases (hrows 506) (fun i => Fin.elim0 i))))
def support95 : Finset (Fin 252) := {34, 45, 50, 64, 109, 121, 124, 128, 135, 139, 144, 149, 154, 157, 162, 173, 193}
theorem cut95 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support95, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 516, OmissionBalanced.support 444, OmissionBalanced.support 559] ![OmissionBalanced.demand 516, OmissionBalanced.demand 444, OmissionBalanced.demand 559] ![1, 1, 1]
    support95 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 516) (Fin.cases (hrows 444) (Fin.cases (hrows 559) (fun i => Fin.elim0 i))))
def support96 : Finset (Fin 252) := {59, 64, 81, 109, 121, 128, 135, 139, 143, 149, 154, 157, 161, 173, 178, 193}
theorem cut96 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support96, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 90, OmissionBalanced.support 605, OmissionBalanced.support 607] ![OmissionBalanced.demand 90, OmissionBalanced.demand 605, OmissionBalanced.demand 607] ![1, 1, 1]
    support96 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 90) (Fin.cases (hrows 605) (Fin.cases (hrows 607) (fun i => Fin.elim0 i))))
def support97 : Finset (Fin 252) := {45, 64, 81, 109, 121, 128, 135, 139, 143, 149, 154, 157, 161, 173, 178, 193}
theorem cut97 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support97, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 516, OmissionBalanced.support 517, OmissionBalanced.support 92] ![OmissionBalanced.demand 516, OmissionBalanced.demand 517, OmissionBalanced.demand 92] ![1, 1, 1]
    support97 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 516) (Fin.cases (hrows 517) (Fin.cases (hrows 92) (fun i => Fin.elim0 i))))
def support98 : Finset (Fin 252) := {46, 59, 65, 81, 109, 121, 124, 128, 135, 139, 144, 149, 154, 157, 162, 173, 193}
theorem cut98 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support98, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 527, OmissionBalanced.support 605, OmissionBalanced.support 657] ![OmissionBalanced.demand 527, OmissionBalanced.demand 605, OmissionBalanced.demand 657] ![1, 1, 1]
    support98 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 527) (Fin.cases (hrows 605) (Fin.cases (hrows 657) (fun i => Fin.elim0 i))))
def support99 : Finset (Fin 252) := {4, 7, 8, 13, 23, 25, 31, 35, 40, 47, 48, 55, 62, 72, 75, 93}
theorem cut99 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support99, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 67, OmissionBalanced.support 27, OmissionBalanced.support 13] ![OmissionBalanced.demand 67, OmissionBalanced.demand 27, OmissionBalanced.demand 13] ![1, 1, 1]
    support99 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 67) (Fin.cases (hrows 27) (Fin.cases (hrows 13) (fun i => Fin.elim0 i))))
def support100 : Finset (Fin 252) := {4, 7, 14, 15, 20, 22, 25, 35, 40, 47, 48, 55, 62, 72, 75, 93}
theorem cut100 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support100, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 44, OmissionBalanced.support 51, OmissionBalanced.support 13] ![OmissionBalanced.demand 44, OmissionBalanced.demand 51, OmissionBalanced.demand 13] ![1, 1, 1]
    support100 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 44) (Fin.cases (hrows 51) (Fin.cases (hrows 13) (fun i => Fin.elim0 i))))
#print axioms cut100
def support101 : Finset (Fin 252) := {8, 13, 14, 15, 20, 22, 25, 35, 40, 47, 48, 55, 62, 72, 75, 93}
theorem cut101 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support101, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 44, OmissionBalanced.support 51, OmissionBalanced.support 26] ![OmissionBalanced.demand 44, OmissionBalanced.demand 51, OmissionBalanced.demand 26] ![1, 1, 1]
    support101 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 44) (Fin.cases (hrows 51) (Fin.cases (hrows 26) (fun i => Fin.elim0 i))))
def support102 : Finset (Fin 252) := {60, 74, 82, 98, 109, 117, 144, 147, 155, 161, 163, 167, 174, 179, 180, 194, 207}
theorem cut102 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support102, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 618, OmissionBalanced.support 693, OmissionBalanced.support 741] ![OmissionBalanced.demand 618, OmissionBalanced.demand 693, OmissionBalanced.demand 741] ![1, 1, 1]
    support102 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 618) (Fin.cases (hrows 693) (Fin.cases (hrows 741) (fun i => Fin.elim0 i))))
def support103 : Finset (Fin 252) := {65, 81, 98, 117, 124, 135, 155, 161, 163, 171, 174, 179, 180, 189, 194, 207}
theorem cut103 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support103, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 658, OmissionBalanced.support 656, OmissionBalanced.support 94] ![OmissionBalanced.demand 658, OmissionBalanced.demand 656, OmissionBalanced.demand 94] ![1, 1, 1]
    support103 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 658) (Fin.cases (hrows 656) (Fin.cases (hrows 94) (fun i => Fin.elim0 i))))
def support104 : Finset (Fin 252) := {60, 74, 82, 98, 109, 135, 139, 144, 147, 158, 163, 167, 171, 174, 180, 189, 207}
theorem cut104 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support104, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 691, OmissionBalanced.support 618, OmissionBalanced.support 743] ![OmissionBalanced.demand 691, OmissionBalanced.demand 618, OmissionBalanced.demand 743] ![1, 1, 1]
    support104 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 691) (Fin.cases (hrows 618) (Fin.cases (hrows 743) (fun i => Fin.elim0 i))))
def support105 : Finset (Fin 252) := {44, 57, 62, 71, 72, 77, 80, 88, 90, 96, 116, 127, 134, 153, 170, 186}
theorem cut105 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support105, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 511, OmissionBalanced.support 83, OmissionBalanced.support 585] ![OmissionBalanced.demand 511, OmissionBalanced.demand 83, OmissionBalanced.demand 585] ![1, 1, 1]
    support105 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 511) (Fin.cases (hrows 83) (Fin.cases (hrows 585) (fun i => Fin.elim0 i))))
def support106 : Finset (Fin 252) := {44, 57, 71, 72, 77, 84, 88, 90, 96, 104, 107, 134, 142, 153, 169, 177, 191}
theorem cut106 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support106, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 505, OmissionBalanced.support 513, OmissionBalanced.support 583] ![OmissionBalanced.demand 505, OmissionBalanced.demand 513, OmissionBalanced.demand 583] ![1, 1, 1]
    support106 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 505) (Fin.cases (hrows 513) (Fin.cases (hrows 583) (fun i => Fin.elim0 i))))
def support107 : Finset (Fin 252) := {192, 205, 210, 216, 217, 223, 225, 226, 229, 234, 238, 239, 240, 244, 249, 250}
theorem cut107 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support107, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 180, OmissionBalanced.support 1022, OmissionBalanced.support 1023] ![OmissionBalanced.demand 180, OmissionBalanced.demand 1022, OmissionBalanced.demand 1023] ![1, 1, 1]
    support107 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 180) (Fin.cases (hrows 1022) (Fin.cases (hrows 1023) (fun i => Fin.elim0 i))))
def support108 : Finset (Fin 252) := {192, 205, 210, 216, 217, 223, 225, 226, 229, 234, 238, 239, 240, 244, 249, 250, 251}
theorem cut108 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support108, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 181, OmissionBalanced.support 1022, OmissionBalanced.support 1023] ![OmissionBalanced.demand 181, OmissionBalanced.demand 1022, OmissionBalanced.demand 1023] ![1, 1, 1]
    support108 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 181) (Fin.cases (hrows 1022) (Fin.cases (hrows 1023) (fun i => Fin.elim0 i))))
def support109 : Finset (Fin 252) := {156, 172, 188, 195, 202, 210, 217, 221, 226, 229, 234, 238, 240, 241, 244, 245, 250}
theorem cut109 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support109, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 180, OmissionBalanced.support 980, OmissionBalanced.support 981] ![OmissionBalanced.demand 180, OmissionBalanced.demand 980, OmissionBalanced.demand 981] ![1, 1, 1]
    support109 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 180) (Fin.cases (hrows 980) (Fin.cases (hrows 981) (fun i => Fin.elim0 i))))
def support110 : Finset (Fin 252) := {156, 172, 188, 195, 202, 210, 217, 221, 226, 229, 234, 238, 240, 241, 244, 245, 251}
theorem cut110 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support110, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 181, OmissionBalanced.support 980, OmissionBalanced.support 981] ![OmissionBalanced.demand 181, OmissionBalanced.demand 980, OmissionBalanced.demand 981] ![1, 1, 1]
    support110 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 181) (Fin.cases (hrows 980) (Fin.cases (hrows 981) (fun i => Fin.elim0 i))))
def support111 : Finset (Fin 252) := {192, 205, 210, 216, 217, 223, 225, 226, 229, 232, 234, 238, 240, 244, 246, 248, 250}
theorem cut111 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support111, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 180, OmissionBalanced.support 1020, OmissionBalanced.support 1021] ![OmissionBalanced.demand 180, OmissionBalanced.demand 1020, OmissionBalanced.demand 1021] ![1, 1, 1]
    support111 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 180) (Fin.cases (hrows 1020) (Fin.cases (hrows 1021) (fun i => Fin.elim0 i))))
def support112 : Finset (Fin 252) := {192, 205, 210, 216, 217, 223, 225, 226, 229, 232, 234, 238, 240, 244, 246, 248, 251}
theorem cut112 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support112, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 181, OmissionBalanced.support 1020, OmissionBalanced.support 1021] ![OmissionBalanced.demand 181, OmissionBalanced.demand 1020, OmissionBalanced.demand 1021] ![1, 1, 1]
    support112 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 181) (Fin.cases (hrows 1020) (Fin.cases (hrows 1021) (fun i => Fin.elim0 i))))
def support113 : Finset (Fin 252) := {174, 189, 194, 205, 209, 215, 216, 220, 225, 229, 231, 234, 235, 241, 244, 249}
theorem cut113 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support113, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 177, OmissionBalanced.support 154, OmissionBalanced.support 155] ![OmissionBalanced.demand 177, OmissionBalanced.demand 154, OmissionBalanced.demand 155] ![1, 1, 1]
    support113 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 154) (Fin.cases (hrows 155) (fun i => Fin.elim0 i))))
def support114 : Finset (Fin 252) := {174, 189, 194, 205, 215, 216, 220, 222, 225, 231, 234, 238, 242, 244, 246, 249}
theorem cut114 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support114, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 177, OmissionBalanced.support 157, OmissionBalanced.support 156] ![OmissionBalanced.demand 177, OmissionBalanced.demand 157, OmissionBalanced.demand 156] ![1, 1, 1]
    support114 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 157) (Fin.cases (hrows 156) (fun i => Fin.elim0 i))))
def support115 : Finset (Fin 252) := {174, 189, 194, 205, 209, 215, 216, 220, 225, 229, 231, 234, 235, 238, 241, 246}
theorem cut115 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support115, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 176, OmissionBalanced.support 154, OmissionBalanced.support 155] ![OmissionBalanced.demand 176, OmissionBalanced.demand 154, OmissionBalanced.demand 155] ![1, 1, 1]
    support115 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 176) (Fin.cases (hrows 154) (Fin.cases (hrows 155) (fun i => Fin.elim0 i))))
def support116 : Finset (Fin 252) := {174, 189, 194, 205, 209, 215, 216, 220, 222, 225, 231, 234, 235, 238, 246}
theorem cut116 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support116, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 176, OmissionBalanced.support 154, OmissionBalanced.support 157] ![OmissionBalanced.demand 176, OmissionBalanced.demand 154, OmissionBalanced.demand 157] ![1, 1, 1]
    support116 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 176) (Fin.cases (hrows 154) (Fin.cases (hrows 157) (fun i => Fin.elim0 i))))
def support117 : Finset (Fin 252) := {174, 189, 191, 194, 203, 204, 209, 216, 220, 222, 226, 228, 238, 243, 244, 247}
theorem cut117 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support117, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 150, OmissionBalanced.support 170, OmissionBalanced.support 153] ![OmissionBalanced.demand 150, OmissionBalanced.demand 170, OmissionBalanced.demand 153] ![1, 1, 1]
    support117 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 150) (Fin.cases (hrows 170) (Fin.cases (hrows 153) (fun i => Fin.elim0 i))))
def support118 : Finset (Fin 252) := {174, 189, 191, 194, 203, 204, 209, 216, 222, 226, 229, 231, 236, 237, 244, 247}
theorem cut118 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support118, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 170, OmissionBalanced.support 151, OmissionBalanced.support 152] ![OmissionBalanced.demand 170, OmissionBalanced.demand 151, OmissionBalanced.demand 152] ![1, 1, 1]
    support118 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 170) (Fin.cases (hrows 151) (Fin.cases (hrows 152) (fun i => Fin.elim0 i))))
def support119 : Finset (Fin 252) := {174, 189, 191, 194, 203, 204, 209, 216, 222, 226, 229, 231, 236, 237, 238, 243}
theorem cut119 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support119, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 151, OmissionBalanced.support 169, OmissionBalanced.support 152] ![OmissionBalanced.demand 151, OmissionBalanced.demand 169, OmissionBalanced.demand 152] ![1, 1, 1]
    support119 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 151) (Fin.cases (hrows 169) (Fin.cases (hrows 152) (fun i => Fin.elim0 i))))
def support120 : Finset (Fin 252) := {174, 189, 191, 194, 204, 209, 215, 220, 222, 225, 234, 235, 238, 244, 246, 249}
theorem cut120 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support120, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 172, OmissionBalanced.support 154, OmissionBalanced.support 157] ![OmissionBalanced.demand 172, OmissionBalanced.demand 154, OmissionBalanced.demand 157] ![1, 1, 1]
    support120 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 172) (Fin.cases (hrows 154) (Fin.cases (hrows 157) (fun i => Fin.elim0 i))))
def support121 : Finset (Fin 252) := {174, 189, 191, 194, 204, 209, 215, 222, 225, 229, 231, 234, 241, 242, 244, 249}
theorem cut121 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support121, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 172, OmissionBalanced.support 155, OmissionBalanced.support 156] ![OmissionBalanced.demand 172, OmissionBalanced.demand 155, OmissionBalanced.demand 156] ![1, 1, 1]
    support121 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 172) (Fin.cases (hrows 155) (Fin.cases (hrows 156) (fun i => Fin.elim0 i))))
def support122 : Finset (Fin 252) := {174, 189, 191, 194, 204, 209, 215, 222, 225, 229, 231, 234, 238, 241, 242, 246}
theorem cut122 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support122, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 171, OmissionBalanced.support 155, OmissionBalanced.support 156] ![OmissionBalanced.demand 171, OmissionBalanced.demand 155, OmissionBalanced.demand 156] ![1, 1, 1]
    support122 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 171) (Fin.cases (hrows 155) (Fin.cases (hrows 156) (fun i => Fin.elim0 i))))
def support123 : Finset (Fin 252) := {21, 23, 29, 31, 35, 40, 47, 48, 55, 62, 72, 78, 90, 93, 112}
theorem cut123 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support123, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 68, OmissionBalanced.support 60, OmissionBalanced.support 67] ![OmissionBalanced.demand 68, OmissionBalanced.demand 60, OmissionBalanced.demand 67] ![1, 1, 1]
    support123 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 68) (Fin.cases (hrows 60) (Fin.cases (hrows 67) (fun i => Fin.elim0 i))))
def support124 : Finset (Fin 252) := {14, 20, 32, 35, 40, 42, 47, 48, 55, 62, 72, 78, 90, 93, 112}
theorem cut124 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support124, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 45, OmissionBalanced.support 74, OmissionBalanced.support 44] ![OmissionBalanced.demand 45, OmissionBalanced.demand 74, OmissionBalanced.demand 44] ![1, 1, 1]
    support124 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 45) (Fin.cases (hrows 74) (Fin.cases (hrows 44) (fun i => Fin.elim0 i))))
def support125 : Finset (Fin 252) := {2, 5, 7, 8, 17, 19, 20, 25, 26, 31, 35, 39, 46, 47, 54, 60, 74}
theorem cut125 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support125, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 214, OmissionBalanced.support 235, OmissionBalanced.support 6] ![OmissionBalanced.demand 214, OmissionBalanced.demand 235, OmissionBalanced.demand 6] ![1, 1, 1]
    support125 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 214) (Fin.cases (hrows 235) (Fin.cases (hrows 6) (fun i => Fin.elim0 i))))
#print axioms cut125
def support126 : Finset (Fin 252) := {2, 4, 7, 12, 17, 20, 25, 26, 31, 35, 39, 46, 47, 54, 60, 74}
theorem cut126 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support126, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 194, OmissionBalanced.support 205, OmissionBalanced.support 6] ![OmissionBalanced.demand 194, OmissionBalanced.demand 205, OmissionBalanced.demand 6] ![1, 1, 1]
    support126 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 194) (Fin.cases (hrows 205) (Fin.cases (hrows 6) (fun i => Fin.elim0 i))))
def support127 : Finset (Fin 252) := {5, 8, 13, 17, 19, 20, 25, 26, 31, 35, 39, 46, 47, 54, 60, 74}
theorem cut127 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support127, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 214, OmissionBalanced.support 235, OmissionBalanced.support 17] ![OmissionBalanced.demand 214, OmissionBalanced.demand 235, OmissionBalanced.demand 17] ![1, 1, 1]
    support127 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 214) (Fin.cases (hrows 235) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support128 : Finset (Fin 252) := {2, 4, 5, 12, 13, 17, 20, 25, 26, 31, 35, 39, 46, 47, 54, 60, 74}
theorem cut128 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support128, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 194, OmissionBalanced.support 205, OmissionBalanced.support 17] ![OmissionBalanced.demand 194, OmissionBalanced.demand 205, OmissionBalanced.demand 17] ![1, 1, 1]
    support128 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 194) (Fin.cases (hrows 205) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support129 : Finset (Fin 252) := {0, 3, 7, 10, 11, 13, 17, 20, 22, 25, 31, 34, 36, 43, 48, 61}
theorem cut129 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support129, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 11, OmissionBalanced.support 2, OmissionBalanced.support 38] ![OmissionBalanced.demand 11, OmissionBalanced.demand 2, OmissionBalanced.demand 38] ![1, 1, 1]
    support129 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 11) (Fin.cases (hrows 2) (Fin.cases (hrows 38) (fun i => Fin.elim0 i))))
def support130 : Finset (Fin 252) := {1, 3, 7, 10, 11, 13, 17, 20, 22, 25, 31, 34, 36, 43, 48, 61}
theorem cut130 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support130, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 11, OmissionBalanced.support 3, OmissionBalanced.support 38] ![OmissionBalanced.demand 11, OmissionBalanced.demand 3, OmissionBalanced.demand 38] ![1, 1, 1]
    support130 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 11) (Fin.cases (hrows 3) (Fin.cases (hrows 38) (fun i => Fin.elim0 i))))
def support131 : Finset (Fin 252) := {0, 5, 6, 7, 11, 13, 17, 20, 22, 25, 31, 34, 36, 43, 48, 61}
theorem cut131 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support131, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 2, OmissionBalanced.support 18, OmissionBalanced.support 21] ![OmissionBalanced.demand 2, OmissionBalanced.demand 18, OmissionBalanced.demand 21] ![1, 1, 1]
    support131 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (hrows 18) (Fin.cases (hrows 21) (fun i => Fin.elim0 i))))
def support132 : Finset (Fin 252) := {1, 5, 6, 7, 11, 13, 17, 20, 22, 25, 31, 34, 36, 43, 48, 61}
theorem cut132 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support132, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 3, OmissionBalanced.support 18, OmissionBalanced.support 21] ![OmissionBalanced.demand 3, OmissionBalanced.demand 18, OmissionBalanced.demand 21] ![1, 1, 1]
    support132 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 3) (Fin.cases (hrows 18) (Fin.cases (hrows 21) (fun i => Fin.elim0 i))))
def support133 : Finset (Fin 252) := {2, 4, 5, 7, 13, 17, 20, 25, 26, 29, 31, 35, 42, 46, 47, 60}
theorem cut133 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support133, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 6, OmissionBalanced.support 12, OmissionBalanced.support 19] ![OmissionBalanced.demand 6, OmissionBalanced.demand 12, OmissionBalanced.demand 19] ![1, 1, 1]
    support133 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 6) (Fin.cases (hrows 12) (Fin.cases (hrows 19) (fun i => Fin.elim0 i))))
def support134 : Finset (Fin 252) := {2, 7, 8, 13, 17, 20, 25, 26, 29, 31, 35, 42, 46, 47, 60}
theorem cut134 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support134, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 7, OmissionBalanced.support 6, OmissionBalanced.support 24] ![OmissionBalanced.demand 7, OmissionBalanced.demand 6, OmissionBalanced.demand 24] ![1, 1, 1]
    support134 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 7) (Fin.cases (hrows 6) (Fin.cases (hrows 24) (fun i => Fin.elim0 i))))
def support135 : Finset (Fin 252) := {2, 5, 7, 8, 13, 17, 20, 25, 26, 29, 31, 35, 42, 46, 47, 60}
theorem cut135 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support135, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 7, OmissionBalanced.support 17, OmissionBalanced.support 24] ![OmissionBalanced.demand 7, OmissionBalanced.demand 17, OmissionBalanced.demand 24] ![1, 1, 1]
    support135 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 7) (Fin.cases (hrows 17) (Fin.cases (hrows 24) (fun i => Fin.elim0 i))))
def support136 : Finset (Fin 252) := {4, 5, 7, 13, 17, 20, 25, 26, 29, 31, 35, 42, 46, 47, 60}
theorem cut136 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support136, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 12, OmissionBalanced.support 19, OmissionBalanced.support 17] ![OmissionBalanced.demand 12, OmissionBalanced.demand 19, OmissionBalanced.demand 17] ![1, 1, 1]
    support136 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 12) (Fin.cases (hrows 19) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support137 : Finset (Fin 252) := {190, 203, 208, 215, 217, 220, 226, 229, 231, 234, 238, 240, 244, 245, 246, 250}
theorem cut137 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support137, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 167, OmissionBalanced.support 166, OmissionBalanced.support 180] ![OmissionBalanced.demand 167, OmissionBalanced.demand 166, OmissionBalanced.demand 180] ![1, 1, 1]
    support137 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 167) (Fin.cases (hrows 166) (Fin.cases (hrows 180) (fun i => Fin.elim0 i))))
def support138 : Finset (Fin 252) := {190, 203, 208, 215, 217, 220, 226, 229, 231, 234, 238, 240, 244, 245, 246, 251}
theorem cut138 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support138, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 167, OmissionBalanced.support 166, OmissionBalanced.support 181] ![OmissionBalanced.demand 167, OmissionBalanced.demand 166, OmissionBalanced.demand 181] ![1, 1, 1]
    support138 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 167) (Fin.cases (hrows 166) (Fin.cases (hrows 181) (fun i => Fin.elim0 i))))
def support139 : Finset (Fin 252) := {190, 203, 208, 215, 217, 220, 226, 229, 231, 234, 238, 240, 241, 244, 248, 250}
theorem cut139 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support139, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 180, OmissionBalanced.support 165, OmissionBalanced.support 168] ![OmissionBalanced.demand 180, OmissionBalanced.demand 165, OmissionBalanced.demand 168] ![1, 1, 1]
    support139 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 180) (Fin.cases (hrows 165) (Fin.cases (hrows 168) (fun i => Fin.elim0 i))))
def support140 : Finset (Fin 252) := {190, 203, 208, 215, 217, 220, 226, 229, 231, 234, 238, 240, 241, 244, 248, 251}
theorem cut140 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support140, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 181, OmissionBalanced.support 165, OmissionBalanced.support 168] ![OmissionBalanced.demand 181, OmissionBalanced.demand 165, OmissionBalanced.demand 168] ![1, 1, 1]
    support140 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 181) (Fin.cases (hrows 165) (Fin.cases (hrows 168) (fun i => Fin.elim0 i))))
def support141 : Finset (Fin 252) := {177, 191, 197, 204, 205, 212, 216, 220, 225, 226, 231, 234, 239, 244, 247, 249}
theorem cut141 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support141, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 177, OmissionBalanced.support 1011, OmissionBalanced.support 1013] ![OmissionBalanced.demand 177, OmissionBalanced.demand 1011, OmissionBalanced.demand 1013] ![1, 1, 1]
    support141 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 1011) (Fin.cases (hrows 1013) (fun i => Fin.elim0 i))))
def support142 : Finset (Fin 252) := {177, 191, 197, 204, 205, 212, 216, 220, 225, 226, 231, 232, 234, 243, 244, 246, 249}
theorem cut142 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support142, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 177, OmissionBalanced.support 1010, OmissionBalanced.support 1012] ![OmissionBalanced.demand 177, OmissionBalanced.demand 1010, OmissionBalanced.demand 1012] ![1, 1, 1]
    support142 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 1010) (Fin.cases (hrows 1012) (fun i => Fin.elim0 i))))
def support143 : Finset (Fin 252) := {191, 204, 205, 209, 216, 220, 222, 225, 226, 231, 234, 238, 244, 246, 247}
theorem cut143 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support143, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 176, OmissionBalanced.support 170, OmissionBalanced.support 171] ![OmissionBalanced.demand 176, OmissionBalanced.demand 170, OmissionBalanced.demand 171] ![1, 1, 1]
    support143 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 176) (Fin.cases (hrows 170) (Fin.cases (hrows 171) (fun i => Fin.elim0 i))))
def support144 : Finset (Fin 252) := {191, 204, 205, 209, 216, 220, 222, 225, 226, 231, 234, 238, 244, 246, 247, 249}
theorem cut144 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support144, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 177, OmissionBalanced.support 170, OmissionBalanced.support 171] ![OmissionBalanced.demand 177, OmissionBalanced.demand 170, OmissionBalanced.demand 171] ![1, 1, 1]
    support144 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 170) (Fin.cases (hrows 171) (fun i => Fin.elim0 i))))
def support145 : Finset (Fin 252) := {177, 191, 197, 204, 205, 212, 216, 220, 225, 226, 231, 232, 234, 238, 243, 246}
theorem cut145 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support145, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 176, OmissionBalanced.support 1010, OmissionBalanced.support 1012] ![OmissionBalanced.demand 176, OmissionBalanced.demand 1010, OmissionBalanced.demand 1012] ![1, 1, 1]
    support145 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 176) (Fin.cases (hrows 1010) (Fin.cases (hrows 1012) (fun i => Fin.elim0 i))))
def support146 : Finset (Fin 252) := {191, 204, 205, 209, 216, 220, 222, 225, 226, 231, 234, 238, 243, 244, 246, 249}
theorem cut146 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support146, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 177, OmissionBalanced.support 169, OmissionBalanced.support 171] ![OmissionBalanced.demand 177, OmissionBalanced.demand 169, OmissionBalanced.demand 171] ![1, 1, 1]
    support146 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 169) (Fin.cases (hrows 171) (fun i => Fin.elim0 i))))
def support147 : Finset (Fin 252) := {177, 191, 197, 204, 205, 212, 216, 220, 225, 226, 231, 234, 238, 239, 246, 247, 249}
theorem cut147 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support147, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 176, OmissionBalanced.support 1011, OmissionBalanced.support 1013] ![OmissionBalanced.demand 176, OmissionBalanced.demand 1011, OmissionBalanced.demand 1013] ![1, 1, 1]
    support147 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 176) (Fin.cases (hrows 1011) (Fin.cases (hrows 1013) (fun i => Fin.elim0 i))))
def support148 : Finset (Fin 252) := {191, 204, 205, 209, 216, 220, 222, 225, 226, 231, 234, 238, 243, 244, 249}
theorem cut148 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support148, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 177, OmissionBalanced.support 172, OmissionBalanced.support 169] ![OmissionBalanced.demand 177, OmissionBalanced.demand 172, OmissionBalanced.demand 169] ![1, 1, 1]
    support148 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 172) (Fin.cases (hrows 169) (fun i => Fin.elim0 i))))
def support149 : Finset (Fin 252) := {5, 13, 16, 17, 20, 26, 29, 31, 35, 36, 42, 46, 57, 62, 77}
theorem cut149 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support149, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 56, OmissionBalanced.support 20, OmissionBalanced.support 17] ![OmissionBalanced.demand 56, OmissionBalanced.demand 20, OmissionBalanced.demand 17] ![1, 1, 1]
    support149 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 56) (Fin.cases (hrows 20) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support150 : Finset (Fin 252) := {8, 13, 15, 22, 25, 35, 37, 40, 47, 55, 67, 72, 75, 84, 93, 119}
theorem cut150 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support150, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 234, OmissionBalanced.support 288, OmissionBalanced.support 26] ![OmissionBalanced.demand 234, OmissionBalanced.demand 288, OmissionBalanced.demand 26] ![1, 1, 1]
    support150 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 234) (Fin.cases (hrows 288) (Fin.cases (hrows 26) (fun i => Fin.elim0 i))))
#print axioms cut150
def support151 : Finset (Fin 252) := {77, 92, 101, 118, 128, 139, 144, 147, 154, 171, 176, 181, 185, 191, 197, 204, 219}
theorem cut151 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support151, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 716, OmissionBalanced.support 828, OmissionBalanced.support 777] ![OmissionBalanced.demand 716, OmissionBalanced.demand 828, OmissionBalanced.demand 777] ![1, 1, 1]
    support151 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 716) (Fin.cases (hrows 828) (Fin.cases (hrows 777) (fun i => Fin.elim0 i))))
def support152 : Finset (Fin 252) := {2, 5, 7, 13, 16, 17, 26, 29, 31, 36, 42, 47, 57, 60, 62, 77}
theorem cut152 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support152, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 7, OmissionBalanced.support 56, OmissionBalanced.support 20] ![OmissionBalanced.demand 7, OmissionBalanced.demand 56, OmissionBalanced.demand 20] ![1, 1, 1]
    support152 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 7) (Fin.cases (hrows 56) (Fin.cases (hrows 20) (fun i => Fin.elim0 i))))
def support153 : Finset (Fin 252) := {4, 7, 8, 13, 23, 25, 29, 31, 35, 42, 47, 48, 57, 60, 62, 77}
theorem cut153 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support153, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 25, OmissionBalanced.support 12, OmissionBalanced.support 1278] ![OmissionBalanced.demand 25, OmissionBalanced.demand 12, OmissionBalanced.demand 1278] ![1, 1, 1]
    support153 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 25) (Fin.cases (hrows 12) (Fin.cases (hrows 1278) (fun i => Fin.elim0 i))))
def support154 : Finset (Fin 252) := {2, 7, 9, 10, 17, 20, 22, 26, 29, 36, 42, 47, 57, 60, 62, 77}
theorem cut154 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support154, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 7, OmissionBalanced.support 34, OmissionBalanced.support 40] ![OmissionBalanced.demand 7, OmissionBalanced.demand 34, OmissionBalanced.demand 40] ![1, 1, 1]
    support154 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 7) (Fin.cases (hrows 34) (Fin.cases (hrows 40) (fun i => Fin.elim0 i))))
def support155 : Finset (Fin 252) := {4, 7, 14, 15, 20, 22, 25, 29, 35, 42, 47, 48, 57, 60, 62, 77}
theorem cut155 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support155, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 42, OmissionBalanced.support 12, OmissionBalanced.support 49] ![OmissionBalanced.demand 42, OmissionBalanced.demand 12, OmissionBalanced.demand 49] ![1, 1, 1]
    support155 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 42) (Fin.cases (hrows 12) (Fin.cases (hrows 49) (fun i => Fin.elim0 i))))
def support156 : Finset (Fin 252) := {5, 9, 10, 13, 17, 20, 22, 26, 29, 36, 42, 47, 57, 60, 62, 77}
theorem cut156 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support156, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 34, OmissionBalanced.support 19, OmissionBalanced.support 40] ![OmissionBalanced.demand 34, OmissionBalanced.demand 19, OmissionBalanced.demand 40] ![1, 1, 1]
    support156 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 34) (Fin.cases (hrows 19) (Fin.cases (hrows 40) (fun i => Fin.elim0 i))))
def support157 : Finset (Fin 252) := {8, 13, 14, 15, 20, 22, 25, 29, 35, 42, 47, 48, 57, 60, 62, 77}
theorem cut157 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support157, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 42, OmissionBalanced.support 24, OmissionBalanced.support 49] ![OmissionBalanced.demand 42, OmissionBalanced.demand 24, OmissionBalanced.demand 49] ![1, 1, 1]
    support157 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 42) (Fin.cases (hrows 24) (Fin.cases (hrows 49) (fun i => Fin.elim0 i))))
def support158 : Finset (Fin 252) := {0, 3, 5, 7, 11, 13, 17, 19, 22, 25, 26, 28, 34, 35, 41, 46, 59}
theorem cut158 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support158, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 197, OmissionBalanced.support 213, OmissionBalanced.support 2] ![OmissionBalanced.demand 197, OmissionBalanced.demand 213, OmissionBalanced.demand 2] ![1, 1, 1]
    support158 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 197) (Fin.cases (hrows 213) (Fin.cases (hrows 2) (fun i => Fin.elim0 i))))
def support159 : Finset (Fin 252) := {1, 3, 5, 7, 11, 13, 17, 19, 22, 25, 26, 28, 34, 35, 41, 46, 59}
theorem cut159 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support159, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 197, OmissionBalanced.support 213, OmissionBalanced.support 3] ![OmissionBalanced.demand 197, OmissionBalanced.demand 213, OmissionBalanced.demand 3] ![1, 1, 1]
    support159 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 197) (Fin.cases (hrows 213) (Fin.cases (hrows 3) (fun i => Fin.elim0 i))))
def support160 : Finset (Fin 252) := {2, 5, 7, 9, 13, 17, 20, 26, 29, 31, 35, 36, 46, 57, 62, 77}
theorem cut160 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support160, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 34, OmissionBalanced.support 6, OmissionBalanced.support 20] ![OmissionBalanced.demand 34, OmissionBalanced.demand 6, OmissionBalanced.demand 20] ![1, 1, 1]
    support160 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 34) (Fin.cases (hrows 6) (Fin.cases (hrows 20) (fun i => Fin.elim0 i))))
def support161 : Finset (Fin 252) := {1, 2, 7, 11, 12, 13, 17, 22, 25, 26, 28, 34, 35, 41, 46, 59}
theorem cut161 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support161, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 188, OmissionBalanced.support 3, OmissionBalanced.support 193] ![OmissionBalanced.demand 188, OmissionBalanced.demand 3, OmissionBalanced.demand 193] ![1, 1, 1]
    support161 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 188) (Fin.cases (hrows 3) (Fin.cases (hrows 193) (fun i => Fin.elim0 i))))
def support162 : Finset (Fin 252) := {0, 1, 2, 7, 11, 12, 13, 17, 22, 25, 26, 28, 34, 35, 41, 46, 59}
theorem cut162 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support162, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 188, OmissionBalanced.support 2, OmissionBalanced.support 193] ![OmissionBalanced.demand 188, OmissionBalanced.demand 2, OmissionBalanced.demand 193] ![1, 1, 1]
    support162 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 188) (Fin.cases (hrows 2) (Fin.cases (hrows 193) (fun i => Fin.elim0 i))))
def support163 : Finset (Fin 252) := {0, 6, 7, 10, 11, 13, 17, 22, 25, 30, 34, 41, 49, 56, 63, 79, 95}
theorem cut163 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support163, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 2, OmissionBalanced.support 222, OmissionBalanced.support 251] ![OmissionBalanced.demand 2, OmissionBalanced.demand 222, OmissionBalanced.demand 251] ![1, 1, 1]
    support163 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (hrows 222) (Fin.cases (hrows 251) (fun i => Fin.elim0 i))))
def support164 : Finset (Fin 252) := {1, 6, 7, 10, 11, 13, 17, 22, 25, 30, 34, 41, 49, 56, 63, 79, 95}
theorem cut164 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support164, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 3, OmissionBalanced.support 222, OmissionBalanced.support 251] ![OmissionBalanced.demand 3, OmissionBalanced.demand 222, OmissionBalanced.demand 251] ![1, 1, 1]
    support164 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 3) (Fin.cases (hrows 222) (Fin.cases (hrows 251) (fun i => Fin.elim0 i))))
def support165 : Finset (Fin 252) := {2, 7, 10, 16, 17, 20, 22, 26, 31, 35, 36, 42, 46, 57, 62, 77}
theorem cut165 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support165, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 56, OmissionBalanced.support 6, OmissionBalanced.support 40] ![OmissionBalanced.demand 56, OmissionBalanced.demand 6, OmissionBalanced.demand 40] ![1, 1, 1]
    support165 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 56) (Fin.cases (hrows 6) (Fin.cases (hrows 40) (fun i => Fin.elim0 i))))
def support166 : Finset (Fin 252) := {5, 10, 13, 16, 17, 20, 22, 26, 31, 35, 36, 42, 46, 57, 62, 77}
theorem cut166 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support166, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 56, OmissionBalanced.support 17, OmissionBalanced.support 40] ![OmissionBalanced.demand 56, OmissionBalanced.demand 17, OmissionBalanced.demand 40] ![1, 1, 1]
    support166 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 56) (Fin.cases (hrows 17) (Fin.cases (hrows 40) (fun i => Fin.elim0 i))))
def support167 : Finset (Fin 252) := {44, 62, 71, 77, 80, 84, 88, 93, 104, 107, 112, 116, 142, 153, 169, 177, 191}
theorem cut167 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support167, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 510, OmissionBalanced.support 631, OmissionBalanced.support 513] ![OmissionBalanced.demand 510, OmissionBalanced.demand 631, OmissionBalanced.demand 513] ![1, 1, 1]
    support167 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 510) (Fin.cases (hrows 631) (Fin.cases (hrows 513) (fun i => Fin.elim0 i))))
def support168 : Finset (Fin 252) := {5, 8, 10, 13, 17, 22, 25, 29, 31, 36, 43, 48, 57, 61, 62, 77}
theorem cut168 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support168, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 25, OmissionBalanced.support 20, OmissionBalanced.support 38] ![OmissionBalanced.demand 25, OmissionBalanced.demand 20, OmissionBalanced.demand 38] ![1, 1, 1]
    support168 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 25) (Fin.cases (hrows 20) (Fin.cases (hrows 38) (fun i => Fin.elim0 i))))
def support169 : Finset (Fin 252) := {5, 10, 13, 15, 17, 20, 22, 25, 36, 42, 43, 48, 57, 61, 62, 77}
theorem cut169 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support169, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 18, OmissionBalanced.support 49, OmissionBalanced.support 40] ![OmissionBalanced.demand 18, OmissionBalanced.demand 49, OmissionBalanced.demand 40] ![1, 1, 1]
    support169 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 18) (Fin.cases (hrows 49) (Fin.cases (hrows 40) (fun i => Fin.elim0 i))))
def support170 : Finset (Fin 252) := {174, 189, 190, 194, 203, 208, 209, 215, 226, 229, 231, 234, 236, 238, 241, 246}
theorem cut170 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support170, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 167, OmissionBalanced.support 151, OmissionBalanced.support 155] ![OmissionBalanced.demand 167, OmissionBalanced.demand 151, OmissionBalanced.demand 155] ![1, 1, 1]
    support170 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 167) (Fin.cases (hrows 151) (Fin.cases (hrows 155) (fun i => Fin.elim0 i))))
def support171 : Finset (Fin 252) := {174, 189, 190, 194, 203, 208, 215, 220, 222, 226, 229, 234, 238, 241, 243, 246}
theorem cut171 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support171, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 165, OmissionBalanced.support 153, OmissionBalanced.support 157] ![OmissionBalanced.demand 165, OmissionBalanced.demand 153, OmissionBalanced.demand 157] ![1, 1, 1]
    support171 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 165) (Fin.cases (hrows 153) (Fin.cases (hrows 157) (fun i => Fin.elim0 i))))
def support172 : Finset (Fin 252) := {138, 155, 171, 172, 180, 188, 197, 202, 208, 220, 221, 226, 229, 234, 236, 241}
theorem cut172 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support172, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 941, OmissionBalanced.support 943, OmissionBalanced.support 148] ![OmissionBalanced.demand 941, OmissionBalanced.demand 943, OmissionBalanced.demand 148] ![1, 1, 1]
    support172 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 941) (Fin.cases (hrows 943) (Fin.cases (hrows 148) (fun i => Fin.elim0 i))))
def support173 : Finset (Fin 252) := {44, 57, 62, 72, 77, 80, 84, 90, 93, 104, 112, 116, 123, 133, 153, 159}
theorem cut173 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support173, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 504, OmissionBalanced.support 630, OmissionBalanced.support 83] ![OmissionBalanced.demand 504, OmissionBalanced.demand 630, OmissionBalanced.demand 83] ![1, 1, 1]
    support173 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 504) (Fin.cases (hrows 630) (Fin.cases (hrows 83) (fun i => Fin.elim0 i))))
def support174 : Finset (Fin 252) := {44, 57, 62, 71, 72, 77, 80, 88, 96, 97, 107, 108, 115, 133, 150, 151}
theorem cut174 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support174, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 582, OmissionBalanced.support 508, OmissionBalanced.support 84] ![OmissionBalanced.demand 582, OmissionBalanced.demand 508, OmissionBalanced.demand 84] ![1, 1, 1]
    support174 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 582) (Fin.cases (hrows 508) (Fin.cases (hrows 84) (fun i => Fin.elim0 i))))
def support175 : Finset (Fin 252) := {100, 139, 143, 154, 161, 171, 173, 179, 189, 194, 196, 204, 207, 209, 219}
theorem cut175 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support175, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 97, OmissionBalanced.support 117, OmissionBalanced.support 98] ![OmissionBalanced.demand 97, OmissionBalanced.demand 117, OmissionBalanced.demand 98] ![1, 1, 1]
    support175 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 97) (Fin.cases (hrows 117) (Fin.cases (hrows 98) (fun i => Fin.elim0 i))))
#print axioms cut175
def support176 : Finset (Fin 252) := {8, 13, 14, 20, 25, 29, 35, 40, 42, 47, 48, 60, 62, 72, 93}
theorem cut176 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support176, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 24, OmissionBalanced.support 44, OmissionBalanced.support 27] ![OmissionBalanced.demand 24, OmissionBalanced.demand 44, OmissionBalanced.demand 27] ![1, 1, 1]
    support176 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 24) (Fin.cases (hrows 44) (Fin.cases (hrows 27) (fun i => Fin.elim0 i))))
def support177 : Finset (Fin 252) := {155, 171, 194, 202, 205, 209, 216, 220, 225, 229, 231, 234, 235, 241, 244, 249}
theorem cut177 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support177, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 177, OmissionBalanced.support 129, OmissionBalanced.support 130] ![OmissionBalanced.demand 177, OmissionBalanced.demand 129, OmissionBalanced.demand 130] ![1, 1, 1]
    support177 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 177) (Fin.cases (hrows 129) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))
def support178 : Finset (Fin 252) := {155, 171, 194, 202, 205, 209, 216, 220, 225, 229, 231, 234, 235, 238, 241, 246}
theorem cut178 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support178, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 176, OmissionBalanced.support 129, OmissionBalanced.support 130] ![OmissionBalanced.demand 176, OmissionBalanced.demand 129, OmissionBalanced.demand 130] ![1, 1, 1]
    support178 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 176) (Fin.cases (hrows 129) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))
def support179 : Finset (Fin 252) := {92, 98, 118, 128, 135, 139, 147, 158, 161, 167, 171, 174, 179, 189, 194, 207}
theorem cut179 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support179, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 776, OmissionBalanced.support 780, OmissionBalanced.support 94] ![OmissionBalanced.demand 776, OmissionBalanced.demand 780, OmissionBalanced.demand 94] ![1, 1, 1]
    support179 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 776) (Fin.cases (hrows 780) (Fin.cases (hrows 94) (fun i => Fin.elim0 i))))
def support180 : Finset (Fin 252) := {33, 43, 56, 61, 67, 72, 79, 85, 88, 90, 107, 115, 123, 133, 150, 159, 174}
theorem cut180 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support180, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 438, OmissionBalanced.support 430, OmissionBalanced.support 496] ![OmissionBalanced.demand 438, OmissionBalanced.demand 430, OmissionBalanced.demand 496] ![1, 1, 1]
    support180 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 438) (Fin.cases (hrows 430) (Fin.cases (hrows 496) (fun i => Fin.elim0 i))))
def support181 : Finset (Fin 252) := {136, 154, 155, 171, 178, 188, 194, 202, 203, 208, 209, 218, 220, 225, 235}
theorem cut181 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support181, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 114, OmissionBalanced.support 129, OmissionBalanced.support 111] ![OmissionBalanced.demand 114, OmissionBalanced.demand 129, OmissionBalanced.demand 111] ![1, 1, 1]
    support181 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 114) (Fin.cases (hrows 129) (Fin.cases (hrows 111) (fun i => Fin.elim0 i))))
def support182 : Finset (Fin 252) := {136, 154, 155, 171, 178, 188, 194, 202, 208, 209, 215, 216, 220, 227, 228}
theorem cut182 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support182, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 112, OmissionBalanced.support 127, OmissionBalanced.support 113] ![OmissionBalanced.demand 112, OmissionBalanced.demand 127, OmissionBalanced.demand 113] ![1, 1, 1]
    support182 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 112) (Fin.cases (hrows 127) (Fin.cases (hrows 113) (fun i => Fin.elim0 i))))
def support183 : Finset (Fin 252) := {5, 8, 13, 17, 19, 20, 25, 36, 39, 43, 48, 61, 62, 71, 77, 92}
theorem cut183 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support183, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 18, OmissionBalanced.support 237, OmissionBalanced.support 216] ![OmissionBalanced.demand 18, OmissionBalanced.demand 237, OmissionBalanced.demand 216] ![1, 1, 1]
    support183 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 18) (Fin.cases (hrows 237) (Fin.cases (hrows 216) (fun i => Fin.elim0 i))))
def support184 : Finset (Fin 252) := {5, 8, 10, 17, 19, 22, 25, 31, 36, 39, 43, 48, 61, 62, 71, 77, 92}
theorem cut184 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support184, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 38, OmissionBalanced.support 237, OmissionBalanced.support 216] ![OmissionBalanced.demand 38, OmissionBalanced.demand 237, OmissionBalanced.demand 216] ![1, 1, 1]
    support184 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 38) (Fin.cases (hrows 237) (Fin.cases (hrows 216) (fun i => Fin.elim0 i))))
def support185 : Finset (Fin 252) := {32, 47, 54, 60, 66, 70, 75, 80, 97, 104, 107, 112, 123, 133, 150, 159, 174}
theorem cut185 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support185, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 426, OmissionBalanced.support 529, OmissionBalanced.support 422] ![OmissionBalanced.demand 426, OmissionBalanced.demand 529, OmissionBalanced.demand 422] ![1, 1, 1]
    support185 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 426) (Fin.cases (hrows 529) (Fin.cases (hrows 422) (fun i => Fin.elim0 i))))
def support186 : Finset (Fin 252) := {5, 13, 14, 17, 20, 26, 29, 31, 35, 36, 46, 48, 57, 62, 77}
theorem cut186 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support186, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 42, OmissionBalanced.support 20, OmissionBalanced.support 17] ![OmissionBalanced.demand 42, OmissionBalanced.demand 20, OmissionBalanced.demand 17] ![1, 1, 1]
    support186 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 42) (Fin.cases (hrows 20) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support187 : Finset (Fin 252) := {174, 189, 194, 203, 205, 215, 216, 220, 222, 225, 231, 234, 237, 238, 246}
theorem cut187 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support187, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 176, OmissionBalanced.support 152, OmissionBalanced.support 157] ![OmissionBalanced.demand 176, OmissionBalanced.demand 152, OmissionBalanced.demand 157] ![1, 1, 1]
    support187 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 176) (Fin.cases (hrows 152) (Fin.cases (hrows 157) (fun i => Fin.elim0 i))))
def support188 : Finset (Fin 252) := {3, 5, 9, 11, 13, 17, 20, 26, 29, 31, 35, 36, 46, 57, 62, 77}
theorem cut188 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support188, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 34, OmissionBalanced.support 20, OmissionBalanced.support 10] ![OmissionBalanced.demand 34, OmissionBalanced.demand 20, OmissionBalanced.demand 10] ![1, 1, 1]
    support188 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 34) (Fin.cases (hrows 20) (Fin.cases (hrows 10) (fun i => Fin.elim0 i))))
def support189 : Finset (Fin 252) := {3, 8, 11, 13, 14, 20, 25, 26, 29, 31, 35, 46, 48, 57, 62, 77}
theorem cut189 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support189, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 42, OmissionBalanced.support 25, OmissionBalanced.support 10] ![OmissionBalanced.demand 42, OmissionBalanced.demand 25, OmissionBalanced.demand 10] ![1, 1, 1]
    support189 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 42) (Fin.cases (hrows 25) (Fin.cases (hrows 10) (fun i => Fin.elim0 i))))
def support190 : Finset (Fin 252) := {0, 2, 5, 7, 11, 13, 17, 20, 22, 25, 27, 31, 34, 38, 46, 51, 65}
theorem cut190 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support190, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 191, OmissionBalanced.support 2, OmissionBalanced.support 209] ![OmissionBalanced.demand 191, OmissionBalanced.demand 2, OmissionBalanced.demand 209] ![1, 1, 1]
    support190 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 191) (Fin.cases (hrows 2) (Fin.cases (hrows 209) (fun i => Fin.elim0 i))))
def support191 : Finset (Fin 252) := {1, 2, 5, 7, 11, 13, 17, 20, 22, 25, 27, 31, 34, 38, 46, 51, 65}
theorem cut191 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support191, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 191, OmissionBalanced.support 3, OmissionBalanced.support 209] ![OmissionBalanced.demand 191, OmissionBalanced.demand 3, OmissionBalanced.demand 209] ![1, 1, 1]
    support191 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 191) (Fin.cases (hrows 3) (Fin.cases (hrows 209) (fun i => Fin.elim0 i))))
def support192 : Finset (Fin 252) := {0, 4, 7, 8, 11, 13, 17, 22, 25, 34, 37, 40, 51, 55, 66, 75, 99}
theorem cut192 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support192, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 204, OmissionBalanced.support 2, OmissionBalanced.support 233] ![OmissionBalanced.demand 204, OmissionBalanced.demand 2, OmissionBalanced.demand 233] ![1, 1, 1]
    support192 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 204) (Fin.cases (hrows 2) (Fin.cases (hrows 233) (fun i => Fin.elim0 i))))
def support193 : Finset (Fin 252) := {1, 4, 7, 8, 11, 13, 17, 22, 25, 34, 37, 40, 51, 55, 66, 75, 99}
theorem cut193 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support193, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 204, OmissionBalanced.support 3, OmissionBalanced.support 233] ![OmissionBalanced.demand 204, OmissionBalanced.demand 3, OmissionBalanced.demand 233] ![1, 1, 1]
    support193 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 204) (Fin.cases (hrows 3) (Fin.cases (hrows 233) (fun i => Fin.elim0 i))))
def support194 : Finset (Fin 252) := {1, 3, 7, 11, 13, 17, 18, 20, 22, 25, 31, 34, 38, 46, 51, 65}
theorem cut194 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support194, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 3, OmissionBalanced.support 186, OmissionBalanced.support 199] ![OmissionBalanced.demand 3, OmissionBalanced.demand 186, OmissionBalanced.demand 199] ![1, 1, 1]
    support194 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 3) (Fin.cases (hrows 186) (Fin.cases (hrows 199) (fun i => Fin.elim0 i))))
def support195 : Finset (Fin 252) := {0, 1, 3, 7, 11, 13, 17, 18, 20, 22, 25, 31, 34, 38, 46, 51, 65}
theorem cut195 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support195, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 2, OmissionBalanced.support 186, OmissionBalanced.support 199] ![OmissionBalanced.demand 2, OmissionBalanced.demand 186, OmissionBalanced.demand 199] ![1, 1, 1]
    support195 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (hrows 186) (Fin.cases (hrows 199) (fun i => Fin.elim0 i))))
def support196 : Finset (Fin 252) := {5, 8, 13, 14, 17, 20, 25, 26, 29, 31, 35, 46, 48, 57, 62, 77}
theorem cut196 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support196, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 42, OmissionBalanced.support 25, OmissionBalanced.support 17] ![OmissionBalanced.demand 42, OmissionBalanced.demand 25, OmissionBalanced.demand 17] ![1, 1, 1]
    support196 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 42) (Fin.cases (hrows 25) (Fin.cases (hrows 17) (fun i => Fin.elim0 i))))
def support197 : Finset (Fin 252) := {0, 6, 7, 10, 11, 13, 17, 22, 25, 30, 34, 36, 41, 48, 56, 61, 76}
theorem cut197 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support197, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 2, OmissionBalanced.support 221, OmissionBalanced.support 249] ![OmissionBalanced.demand 2, OmissionBalanced.demand 221, OmissionBalanced.demand 249] ![1, 1, 1]
    support197 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (hrows 221) (Fin.cases (hrows 249) (fun i => Fin.elim0 i))))
def support198 : Finset (Fin 252) := {1, 6, 7, 10, 11, 13, 17, 22, 25, 30, 34, 36, 41, 48, 56, 61, 76}
theorem cut198 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support198, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 3, OmissionBalanced.support 221, OmissionBalanced.support 249] ![OmissionBalanced.demand 3, OmissionBalanced.demand 221, OmissionBalanced.demand 249] ![1, 1, 1]
    support198 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 3) (Fin.cases (hrows 221) (Fin.cases (hrows 249) (fun i => Fin.elim0 i))))
def support199 : Finset (Fin 252) := {0, 3, 5, 7, 11, 13, 17, 19, 22, 25, 28, 34, 36, 48, 56, 61, 76}
theorem cut199 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support199, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 2, OmissionBalanced.support 198, OmissionBalanced.support 215] ![OmissionBalanced.demand 2, OmissionBalanced.demand 198, OmissionBalanced.demand 215] ![1, 1, 1]
    support199 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 2) (Fin.cases (hrows 198) (Fin.cases (hrows 215) (fun i => Fin.elim0 i))))
def support200 : Finset (Fin 252) := {152, 176, 185, 196, 200, 211, 214, 217, 226, 229, 234, 238, 240, 243, 244, 247, 251}
theorem cut200 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support200, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 974, OmissionBalanced.support 973, OmissionBalanced.support 181] ![OmissionBalanced.demand 974, OmissionBalanced.demand 973, OmissionBalanced.demand 181] ![1, 1, 1]
    support200 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 974) (Fin.cases (hrows 973) (Fin.cases (hrows 181) (fun i => Fin.elim0 i))))
#print axioms cut200
def support201 : Finset (Fin 252) := {169, 185, 191, 209, 213, 217, 222, 224, 226, 229, 234, 238, 240, 244, 246, 249, 251}
theorem cut201 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support201, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1001, OmissionBalanced.support 1000, OmissionBalanced.support 181] ![OmissionBalanced.demand 1001, OmissionBalanced.demand 1000, OmissionBalanced.demand 181] ![1, 1, 1]
    support201 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1001) (Fin.cases (hrows 1000) (Fin.cases (hrows 181) (fun i => Fin.elim0 i))))
def support202 : Finset (Fin 252) := {152, 176, 185, 196, 200, 211, 214, 217, 226, 229, 234, 238, 240, 243, 244, 247, 250}
theorem cut202 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support202, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 974, OmissionBalanced.support 973, OmissionBalanced.support 180] ![OmissionBalanced.demand 974, OmissionBalanced.demand 973, OmissionBalanced.demand 180] ![1, 1, 1]
    support202 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 974) (Fin.cases (hrows 973) (Fin.cases (hrows 180) (fun i => Fin.elim0 i))))
def support203 : Finset (Fin 252) := {169, 185, 191, 209, 213, 217, 222, 224, 226, 229, 234, 238, 240, 244, 246, 249, 250}
theorem cut203 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support203, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1001, OmissionBalanced.support 1000, OmissionBalanced.support 180] ![OmissionBalanced.demand 1001, OmissionBalanced.demand 1000, OmissionBalanced.demand 180] ![1, 1, 1]
    support203 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1001) (Fin.cases (hrows 1000) (Fin.cases (hrows 180) (fun i => Fin.elim0 i))))
def support204 : Finset (Fin 252) := {169, 185, 191, 200, 209, 214, 217, 222, 226, 229, 234, 238, 240, 243, 244, 247, 251}
theorem cut204 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support204, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 999, OmissionBalanced.support 181, OmissionBalanced.support 998] ![OmissionBalanced.demand 999, OmissionBalanced.demand 181, OmissionBalanced.demand 998] ![1, 1, 1]
    support204 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 999) (Fin.cases (hrows 181) (Fin.cases (hrows 998) (fun i => Fin.elim0 i))))
def support205 : Finset (Fin 252) := {169, 185, 191, 200, 209, 214, 217, 222, 226, 229, 234, 238, 240, 243, 244, 247, 250}
theorem cut205 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support205, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 999, OmissionBalanced.support 180, OmissionBalanced.support 998] ![OmissionBalanced.demand 999, OmissionBalanced.demand 180, OmissionBalanced.demand 998] ![1, 1, 1]
    support205 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 999) (Fin.cases (hrows 180) (Fin.cases (hrows 998) (fun i => Fin.elim0 i))))
def support206 : Finset (Fin 252) := {75, 91, 99, 109, 117, 135, 157, 162, 174, 180, 183, 190, 195, 199, 202, 215, 227}
theorem cut206 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support206, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 773, OmissionBalanced.support 699, OmissionBalanced.support 821] ![OmissionBalanced.demand 773, OmissionBalanced.demand 699, OmissionBalanced.demand 821] ![1, 1, 1]
    support206 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 773) (Fin.cases (hrows 699) (Fin.cases (hrows 821) (fun i => Fin.elim0 i))))
def support207 : Finset (Fin 252) := {79, 95, 103, 121, 124, 143, 149, 157, 167, 174, 185, 191, 198, 211, 212, 222, 230}
theorem cut207 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support207, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 801, OmissionBalanced.support 833, OmissionBalanced.support 731] ![OmissionBalanced.demand 801, OmissionBalanced.demand 833, OmissionBalanced.demand 731] ![1, 1, 1]
    support207 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 801) (Fin.cases (hrows 833) (Fin.cases (hrows 731) (fun i => Fin.elim0 i))))
def support208 : Finset (Fin 252) := {32, 42, 54, 55, 60, 66, 70, 96, 104, 108, 115, 123, 127, 151, 168, 175, 190}
theorem cut208 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support208, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 419, OmissionBalanced.support 484, OmissionBalanced.support 427] ![OmissionBalanced.demand 419, OmissionBalanced.demand 484, OmissionBalanced.demand 427] ![1, 1, 1]
    support208 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 419) (Fin.cases (hrows 484) (Fin.cases (hrows 427) (fun i => Fin.elim0 i))))
def support209 : Finset (Fin 252) := {60, 74, 82, 98, 109, 135, 139, 144, 158, 163, 166, 184, 188, 190, 195, 203, 218}
theorem cut209 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support209, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 692, OmissionBalanced.support 744, OmissionBalanced.support 619] ![OmissionBalanced.demand 692, OmissionBalanced.demand 744, OmissionBalanced.demand 619] ![1, 1, 1]
    support209 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 692) (Fin.cases (hrows 744) (Fin.cases (hrows 619) (fun i => Fin.elim0 i))))
def support210 : Finset (Fin 252) := {24, 36, 49, 52, 56, 61, 68, 71, 77, 89, 94, 116, 134, 142, 152, 160, 176}
theorem cut210 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support210, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 459, OmissionBalanced.support 370, OmissionBalanced.support 366] ![OmissionBalanced.demand 459, OmissionBalanced.demand 370, OmissionBalanced.demand 366] ![1, 1, 1]
    support210 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 459) (Fin.cases (hrows 370) (Fin.cases (hrows 366) (fun i => Fin.elim0 i))))
def support211 : Finset (Fin 252) := {21, 29, 39, 40, 53, 60, 66, 77, 84, 94, 102, 108, 127, 130, 148, 156, 172}
theorem cut211 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support211, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 334, OmissionBalanced.support 330, OmissionBalanced.support 392] ![OmissionBalanced.demand 334, OmissionBalanced.demand 330, OmissionBalanced.demand 392] ![1, 1, 1]
    support211 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 334) (Fin.cases (hrows 330) (Fin.cases (hrows 392) (fun i => Fin.elim0 i))))
def support212 : Finset (Fin 252) := {61, 76, 83, 100, 124, 128, 136, 143, 147, 155, 181, 185, 191, 196, 197, 209, 219}
theorem cut212 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support212, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 746, OmissionBalanced.support 703, OmissionBalanced.support 629] ![OmissionBalanced.demand 746, OmissionBalanced.demand 703, OmissionBalanced.demand 629] ![1, 1, 1]
    support212 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 746) (Fin.cases (hrows 703) (Fin.cases (hrows 629) (fun i => Fin.elim0 i))))
def support213 : Finset (Fin 252) := {79, 95, 103, 121, 124, 143, 149, 157, 167, 174, 181, 185, 191, 196, 197, 209, 219}
theorem cut213 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support213, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 800, OmissionBalanced.support 730, OmissionBalanced.support 832] ![OmissionBalanced.demand 800, OmissionBalanced.demand 730, OmissionBalanced.demand 832] ![1, 1, 1]
    support213 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 800) (Fin.cases (hrows 730) (Fin.cases (hrows 832) (fun i => Fin.elim0 i))))
def support214 : Finset (Fin 252) := {33, 48, 56, 61, 63, 67, 85, 88, 93, 107, 112, 116, 142, 153, 169, 177, 191}
theorem cut214 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support214, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 542, OmissionBalanced.support 435, OmissionBalanced.support 439] ![OmissionBalanced.demand 542, OmissionBalanced.demand 435, OmissionBalanced.demand 439] ![1, 1, 1]
    support214 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 542) (Fin.cases (hrows 435) (Fin.cases (hrows 439) (fun i => Fin.elim0 i))))
def support215 : Finset (Fin 252) := {132, 158, 167, 179, 184, 196, 211, 214, 217, 226, 229, 234, 236, 238, 240, 243, 244, 251}
theorem cut215 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support215, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 926, OmissionBalanced.support 928, OmissionBalanced.support 181] ![OmissionBalanced.demand 926, OmissionBalanced.demand 928, OmissionBalanced.demand 181] ![1, 1, 1]
    support215 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 926) (Fin.cases (hrows 928) (Fin.cases (hrows 181) (fun i => Fin.elim0 i))))
def support216 : Finset (Fin 252) := {132, 158, 167, 179, 184, 196, 211, 214, 217, 226, 229, 234, 236, 238, 240, 243, 244, 250}
theorem cut216 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support216, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 926, OmissionBalanced.support 928, OmissionBalanced.support 180] ![OmissionBalanced.demand 926, OmissionBalanced.demand 928, OmissionBalanced.demand 180] ![1, 1, 1]
    support216 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 926) (Fin.cases (hrows 928) (Fin.cases (hrows 180) (fun i => Fin.elim0 i))))
def support217 : Finset (Fin 252) := {33, 48, 56, 61, 63, 67, 71, 77, 85, 89, 94, 116, 134, 142, 152, 160, 176}
theorem cut217 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support217, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 433, OmissionBalanced.support 437, OmissionBalanced.support 538] ![OmissionBalanced.demand 433, OmissionBalanced.demand 437, OmissionBalanced.demand 538] ![1, 1, 1]
    support217 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 433) (Fin.cases (hrows 437) (Fin.cases (hrows 538) (fun i => Fin.elim0 i))))
def support218 : Finset (Fin 252) := {6, 11, 18, 30, 34, 41, 46, 49, 56, 61, 63, 68, 79, 85, 95, 103, 121}
theorem cut218 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support218, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 226, OmissionBalanced.support 222, OmissionBalanced.support 261] ![OmissionBalanced.demand 226, OmissionBalanced.demand 222, OmissionBalanced.demand 261] ![1, 1, 1]
    support218 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 226) (Fin.cases (hrows 222) (Fin.cases (hrows 261) (fun i => Fin.elim0 i))))
def support219 : Finset (Fin 252) := {21, 29, 39, 40, 53, 60, 66, 77, 84, 90, 94, 102, 107, 112, 129, 138, 155}
theorem cut219 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support219, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 333, OmissionBalanced.support 391, OmissionBalanced.support 329] ![OmissionBalanced.demand 333, OmissionBalanced.demand 391, OmissionBalanced.demand 329] ![1, 1, 1]
    support219 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 333) (Fin.cases (hrows 391) (Fin.cases (hrows 329) (fun i => Fin.elim0 i))))
def support220 : Finset (Fin 252) := {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251}
theorem cut220 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    55 ≤ ∑ i ∈ support220, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 35, OmissionBalanced.support 134, OmissionBalanced.support 184, OmissionBalanced.support 189, OmissionBalanced.support 190, OmissionBalanced.support 208, OmissionBalanced.support 220, OmissionBalanced.support 229, OmissionBalanced.support 230, OmissionBalanced.support 234, OmissionBalanced.support 242, OmissionBalanced.support 247, OmissionBalanced.support 248, OmissionBalanced.support 257, OmissionBalanced.support 260, OmissionBalanced.support 263, OmissionBalanced.support 264, OmissionBalanced.support 265, OmissionBalanced.support 273, OmissionBalanced.support 281, OmissionBalanced.support 284, OmissionBalanced.support 285, OmissionBalanced.support 305, OmissionBalanced.support 307, OmissionBalanced.support 308, OmissionBalanced.support 309, OmissionBalanced.support 317, OmissionBalanced.support 318, OmissionBalanced.support 319, OmissionBalanced.support 326, OmissionBalanced.support 327, OmissionBalanced.support 328, OmissionBalanced.support 330, OmissionBalanced.support 333, OmissionBalanced.support 358, OmissionBalanced.support 366, OmissionBalanced.support 369, OmissionBalanced.support 376, OmissionBalanced.support 378, OmissionBalanced.support 385, OmissionBalanced.support 386, OmissionBalanced.support 387, OmissionBalanced.support 397, OmissionBalanced.support 398, OmissionBalanced.support 400, OmissionBalanced.support 412, OmissionBalanced.support 423, OmissionBalanced.support 431, OmissionBalanced.support 462, OmissionBalanced.support 464, OmissionBalanced.support 465, OmissionBalanced.support 466, OmissionBalanced.support 467, OmissionBalanced.support 472, OmissionBalanced.support 474, OmissionBalanced.support 475, OmissionBalanced.support 478, OmissionBalanced.support 486, OmissionBalanced.support 498, OmissionBalanced.support 503, OmissionBalanced.support 515, OmissionBalanced.support 521, OmissionBalanced.support 522, OmissionBalanced.support 527, OmissionBalanced.support 528, OmissionBalanced.support 536, OmissionBalanced.support 543, OmissionBalanced.support 554, OmissionBalanced.support 555, OmissionBalanced.support 556, OmissionBalanced.support 559, OmissionBalanced.support 561, OmissionBalanced.support 567, OmissionBalanced.support 568, OmissionBalanced.support 573, OmissionBalanced.support 576, OmissionBalanced.support 579, OmissionBalanced.support 580, OmissionBalanced.support 586, OmissionBalanced.support 588, OmissionBalanced.support 598, OmissionBalanced.support 601, OmissionBalanced.support 612, OmissionBalanced.support 623, OmissionBalanced.support 636, OmissionBalanced.support 646, OmissionBalanced.support 648, OmissionBalanced.support 650, OmissionBalanced.support 653, OmissionBalanced.support 659, OmissionBalanced.support 661, OmissionBalanced.support 662, OmissionBalanced.support 666, OmissionBalanced.support 668, OmissionBalanced.support 671, OmissionBalanced.support 672, OmissionBalanced.support 673, OmissionBalanced.support 675, OmissionBalanced.support 677, OmissionBalanced.support 681, OmissionBalanced.support 682, OmissionBalanced.support 686, OmissionBalanced.support 694, OmissionBalanced.support 704, OmissionBalanced.support 707, OmissionBalanced.support 722, OmissionBalanced.support 726, OmissionBalanced.support 733, OmissionBalanced.support 735, OmissionBalanced.support 738, OmissionBalanced.support 740, OmissionBalanced.support 748, OmissionBalanced.support 751, OmissionBalanced.support 754, OmissionBalanced.support 767, OmissionBalanced.support 769, OmissionBalanced.support 770, OmissionBalanced.support 787, OmissionBalanced.support 790, OmissionBalanced.support 791, OmissionBalanced.support 792, OmissionBalanced.support 801, OmissionBalanced.support 805, OmissionBalanced.support 808, OmissionBalanced.support 810, OmissionBalanced.support 812, OmissionBalanced.support 817, OmissionBalanced.support 818, OmissionBalanced.support 819, OmissionBalanced.support 821, OmissionBalanced.support 844, OmissionBalanced.support 846, OmissionBalanced.support 854, OmissionBalanced.support 865, OmissionBalanced.support 872, OmissionBalanced.support 873, OmissionBalanced.support 874, OmissionBalanced.support 882, OmissionBalanced.support 885, OmissionBalanced.support 887, OmissionBalanced.support 902, OmissionBalanced.support 918, OmissionBalanced.support 920, OmissionBalanced.support 930, OmissionBalanced.support 931, OmissionBalanced.support 933, OmissionBalanced.support 935, OmissionBalanced.support 937, OmissionBalanced.support 943, OmissionBalanced.support 976, OmissionBalanced.support 1002, OmissionBalanced.support 1004, OmissionBalanced.support 1005, OmissionBalanced.support 1018, support1, support2, support4, support5, support8, support9, support13, support19, support22, support23, support26, support27, support28, support29, support30, support31, support38, support41, support42, support43, support46, support47, support49, support50, support51, support52, support54, support55, support67, support68, support79, support80, support84, support95, support109, support164, support193, support197, support199, support200, support201, support205, support206, support207, support208, support209, support210, support211, support212, support214] ![OmissionBalanced.demand 35, OmissionBalanced.demand 134, OmissionBalanced.demand 184, OmissionBalanced.demand 189, OmissionBalanced.demand 190, OmissionBalanced.demand 208, OmissionBalanced.demand 220, OmissionBalanced.demand 229, OmissionBalanced.demand 230, OmissionBalanced.demand 234, OmissionBalanced.demand 242, OmissionBalanced.demand 247, OmissionBalanced.demand 248, OmissionBalanced.demand 257, OmissionBalanced.demand 260, OmissionBalanced.demand 263, OmissionBalanced.demand 264, OmissionBalanced.demand 265, OmissionBalanced.demand 273, OmissionBalanced.demand 281, OmissionBalanced.demand 284, OmissionBalanced.demand 285, OmissionBalanced.demand 305, OmissionBalanced.demand 307, OmissionBalanced.demand 308, OmissionBalanced.demand 309, OmissionBalanced.demand 317, OmissionBalanced.demand 318, OmissionBalanced.demand 319, OmissionBalanced.demand 326, OmissionBalanced.demand 327, OmissionBalanced.demand 328, OmissionBalanced.demand 330, OmissionBalanced.demand 333, OmissionBalanced.demand 358, OmissionBalanced.demand 366, OmissionBalanced.demand 369, OmissionBalanced.demand 376, OmissionBalanced.demand 378, OmissionBalanced.demand 385, OmissionBalanced.demand 386, OmissionBalanced.demand 387, OmissionBalanced.demand 397, OmissionBalanced.demand 398, OmissionBalanced.demand 400, OmissionBalanced.demand 412, OmissionBalanced.demand 423, OmissionBalanced.demand 431, OmissionBalanced.demand 462, OmissionBalanced.demand 464, OmissionBalanced.demand 465, OmissionBalanced.demand 466, OmissionBalanced.demand 467, OmissionBalanced.demand 472, OmissionBalanced.demand 474, OmissionBalanced.demand 475, OmissionBalanced.demand 478, OmissionBalanced.demand 486, OmissionBalanced.demand 498, OmissionBalanced.demand 503, OmissionBalanced.demand 515, OmissionBalanced.demand 521, OmissionBalanced.demand 522, OmissionBalanced.demand 527, OmissionBalanced.demand 528, OmissionBalanced.demand 536, OmissionBalanced.demand 543, OmissionBalanced.demand 554, OmissionBalanced.demand 555, OmissionBalanced.demand 556, OmissionBalanced.demand 559, OmissionBalanced.demand 561, OmissionBalanced.demand 567, OmissionBalanced.demand 568, OmissionBalanced.demand 573, OmissionBalanced.demand 576, OmissionBalanced.demand 579, OmissionBalanced.demand 580, OmissionBalanced.demand 586, OmissionBalanced.demand 588, OmissionBalanced.demand 598, OmissionBalanced.demand 601, OmissionBalanced.demand 612, OmissionBalanced.demand 623, OmissionBalanced.demand 636, OmissionBalanced.demand 646, OmissionBalanced.demand 648, OmissionBalanced.demand 650, OmissionBalanced.demand 653, OmissionBalanced.demand 659, OmissionBalanced.demand 661, OmissionBalanced.demand 662, OmissionBalanced.demand 666, OmissionBalanced.demand 668, OmissionBalanced.demand 671, OmissionBalanced.demand 672, OmissionBalanced.demand 673, OmissionBalanced.demand 675, OmissionBalanced.demand 677, OmissionBalanced.demand 681, OmissionBalanced.demand 682, OmissionBalanced.demand 686, OmissionBalanced.demand 694, OmissionBalanced.demand 704, OmissionBalanced.demand 707, OmissionBalanced.demand 722, OmissionBalanced.demand 726, OmissionBalanced.demand 733, OmissionBalanced.demand 735, OmissionBalanced.demand 738, OmissionBalanced.demand 740, OmissionBalanced.demand 748, OmissionBalanced.demand 751, OmissionBalanced.demand 754, OmissionBalanced.demand 767, OmissionBalanced.demand 769, OmissionBalanced.demand 770, OmissionBalanced.demand 787, OmissionBalanced.demand 790, OmissionBalanced.demand 791, OmissionBalanced.demand 792, OmissionBalanced.demand 801, OmissionBalanced.demand 805, OmissionBalanced.demand 808, OmissionBalanced.demand 810, OmissionBalanced.demand 812, OmissionBalanced.demand 817, OmissionBalanced.demand 818, OmissionBalanced.demand 819, OmissionBalanced.demand 821, OmissionBalanced.demand 844, OmissionBalanced.demand 846, OmissionBalanced.demand 854, OmissionBalanced.demand 865, OmissionBalanced.demand 872, OmissionBalanced.demand 873, OmissionBalanced.demand 874, OmissionBalanced.demand 882, OmissionBalanced.demand 885, OmissionBalanced.demand 887, OmissionBalanced.demand 902, OmissionBalanced.demand 918, OmissionBalanced.demand 920, OmissionBalanced.demand 930, OmissionBalanced.demand 931, OmissionBalanced.demand 933, OmissionBalanced.demand 935, OmissionBalanced.demand 937, OmissionBalanced.demand 943, OmissionBalanced.demand 976, OmissionBalanced.demand 1002, OmissionBalanced.demand 1004, OmissionBalanced.demand 1005, OmissionBalanced.demand 1018, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4] ![233, 233, 584, 12, 167, 18, 81, 104, 114, 8, 101, 238, 226, 2, 122, 133, 85, 1, 83, 20, 76, 104, 26, 29, 53, 93, 82, 19, 114, 32, 112, 1, 78, 33, 138, 98, 38, 6, 3, 124, 44, 117, 182, 60, 28, 18, 288, 298, 28, 128, 62, 2, 14, 69, 106, 53, 216, 163, 1, 159, 24, 277, 58, 88, 24, 147, 158, 73, 93, 100, 8, 227, 106, 18, 106, 94, 60, 8, 2, 8, 8, 88, 213, 206, 23, 93, 6, 89, 62, 23, 18, 6, 73, 69, 2, 1, 163, 18, 216, 182, 1, 28, 288, 92, 58, 14, 3, 18, 227, 156, 16, 298, 158, 93, 18, 112, 83, 32, 33, 104, 277, 98, 28, 38, 93, 2, 6, 124, 82, 78, 115, 114, 20, 176, 28, 37, 326, 176, 135, 85, 26, 104, 18, 15, 122, 101, 81, 133, 8, 2, 114, 4, 49, 596, 226, 226, 86, 201, 201, 21, 376, 376, 20, 20, 21, 134, 134, 86, 95, 95, 57, 57, 231, 226, 66, 226, 100, 231, 100, 77, 77, 66, 56, 6, 6, 56, 38, 38, 195, 172, 195, 14, 25, 172, 25, 14, 180, 168, 95, 95, 168, 180, 91, 91]
    support220 1000 55 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 35) (Fin.cases (hrows 134) (Fin.cases (hrows 184) (Fin.cases (hrows 189) (Fin.cases (hrows 190) (Fin.cases (hrows 208) (Fin.cases (hrows 220) (Fin.cases (hrows 229) (Fin.cases (hrows 230) (Fin.cases (hrows 234) (Fin.cases (hrows 242) (Fin.cases (hrows 247) (Fin.cases (hrows 248) (Fin.cases (hrows 257) (Fin.cases (hrows 260) (Fin.cases (hrows 263) (Fin.cases (hrows 264) (Fin.cases (hrows 265) (Fin.cases (hrows 273) (Fin.cases (hrows 281) (Fin.cases (hrows 284) (Fin.cases (hrows 285) (Fin.cases (hrows 305) (Fin.cases (hrows 307) (Fin.cases (hrows 308) (Fin.cases (hrows 309) (Fin.cases (hrows 317) (Fin.cases (hrows 318) (Fin.cases (hrows 319) (Fin.cases (hrows 326) (Fin.cases (hrows 327) (Fin.cases (hrows 328) (Fin.cases (hrows 330) (Fin.cases (hrows 333) (Fin.cases (hrows 358) (Fin.cases (hrows 366) (Fin.cases (hrows 369) (Fin.cases (hrows 376) (Fin.cases (hrows 378) (Fin.cases (hrows 385) (Fin.cases (hrows 386) (Fin.cases (hrows 387) (Fin.cases (hrows 397) (Fin.cases (hrows 398) (Fin.cases (hrows 400) (Fin.cases (hrows 412) (Fin.cases (hrows 423) (Fin.cases (hrows 431) (Fin.cases (hrows 462) (Fin.cases (hrows 464) (Fin.cases (hrows 465) (Fin.cases (hrows 466) (Fin.cases (hrows 467) (Fin.cases (hrows 472) (Fin.cases (hrows 474) (Fin.cases (hrows 475) (Fin.cases (hrows 478) (Fin.cases (hrows 486) (Fin.cases (hrows 498) (Fin.cases (hrows 503) (Fin.cases (hrows 515) (Fin.cases (hrows 521) (Fin.cases (hrows 522) (Fin.cases (hrows 527) (Fin.cases (hrows 528) (Fin.cases (hrows 536) (Fin.cases (hrows 543) (Fin.cases (hrows 554) (Fin.cases (hrows 555) (Fin.cases (hrows 556) (Fin.cases (hrows 559) (Fin.cases (hrows 561) (Fin.cases (hrows 567) (Fin.cases (hrows 568) (Fin.cases (hrows 573) (Fin.cases (hrows 576) (Fin.cases (hrows 579) (Fin.cases (hrows 580) (Fin.cases (hrows 586) (Fin.cases (hrows 588) (Fin.cases (hrows 598) (Fin.cases (hrows 601) (Fin.cases (hrows 612) (Fin.cases (hrows 623) (Fin.cases (hrows 636) (Fin.cases (hrows 646) (Fin.cases (hrows 648) (Fin.cases (hrows 650) (Fin.cases (hrows 653) (Fin.cases (hrows 659) (Fin.cases (hrows 661) (Fin.cases (hrows 662) (Fin.cases (hrows 666) (Fin.cases (hrows 668) (Fin.cases (hrows 671) (Fin.cases (hrows 672) (Fin.cases (hrows 673) (Fin.cases (hrows 675) (Fin.cases (hrows 677) (Fin.cases (hrows 681) (Fin.cases (hrows 682) (Fin.cases (hrows 686) (Fin.cases (hrows 694) (Fin.cases (hrows 704) (Fin.cases (hrows 707) (Fin.cases (hrows 722) (Fin.cases (hrows 726) (Fin.cases (hrows 733) (Fin.cases (hrows 735) (Fin.cases (hrows 738) (Fin.cases (hrows 740) (Fin.cases (hrows 748) (Fin.cases (hrows 751) (Fin.cases (hrows 754) (Fin.cases (hrows 767) (Fin.cases (hrows 769) (Fin.cases (hrows 770) (Fin.cases (hrows 787) (Fin.cases (hrows 790) (Fin.cases (hrows 791) (Fin.cases (hrows 792) (Fin.cases (hrows 801) (Fin.cases (hrows 805) (Fin.cases (hrows 808) (Fin.cases (hrows 810) (Fin.cases (hrows 812) (Fin.cases (hrows 817) (Fin.cases (hrows 818) (Fin.cases (hrows 819) (Fin.cases (hrows 821) (Fin.cases (hrows 844) (Fin.cases (hrows 846) (Fin.cases (hrows 854) (Fin.cases (hrows 865) (Fin.cases (hrows 872) (Fin.cases (hrows 873) (Fin.cases (hrows 874) (Fin.cases (hrows 882) (Fin.cases (hrows 885) (Fin.cases (hrows 887) (Fin.cases (hrows 902) (Fin.cases (hrows 918) (Fin.cases (hrows 920) (Fin.cases (hrows 930) (Fin.cases (hrows 931) (Fin.cases (hrows 933) (Fin.cases (hrows 935) (Fin.cases (hrows 937) (Fin.cases (hrows 943) (Fin.cases (hrows 976) (Fin.cases (hrows 1002) (Fin.cases (hrows 1004) (Fin.cases (hrows 1005) (Fin.cases (hrows 1018) (Fin.cases (cut1 holes hbool hrows) (Fin.cases (cut2 holes hbool hrows) (Fin.cases (cut4 holes hbool hrows) (Fin.cases (cut5 holes hbool hrows) (Fin.cases (cut8 holes hbool hrows) (Fin.cases (cut9 holes hbool hrows) (Fin.cases (cut13 holes hbool hrows) (Fin.cases (cut19 holes hbool hrows) (Fin.cases (cut22 holes hbool hrows) (Fin.cases (cut23 holes hbool hrows) (Fin.cases (cut26 holes hbool hrows) (Fin.cases (cut27 holes hbool hrows) (Fin.cases (cut28 holes hbool hrows) (Fin.cases (cut29 holes hbool hrows) (Fin.cases (cut30 holes hbool hrows) (Fin.cases (cut31 holes hbool hrows) (Fin.cases (cut38 holes hbool hrows) (Fin.cases (cut41 holes hbool hrows) (Fin.cases (cut42 holes hbool hrows) (Fin.cases (cut43 holes hbool hrows) (Fin.cases (cut46 holes hbool hrows) (Fin.cases (cut47 holes hbool hrows) (Fin.cases (cut49 holes hbool hrows) (Fin.cases (cut50 holes hbool hrows) (Fin.cases (cut51 holes hbool hrows) (Fin.cases (cut52 holes hbool hrows) (Fin.cases (cut54 holes hbool hrows) (Fin.cases (cut55 holes hbool hrows) (Fin.cases (cut67 holes hbool hrows) (Fin.cases (cut68 holes hbool hrows) (Fin.cases (cut79 holes hbool hrows) (Fin.cases (cut80 holes hbool hrows) (Fin.cases (cut84 holes hbool hrows) (Fin.cases (cut95 holes hbool hrows) (Fin.cases (cut109 holes hbool hrows) (Fin.cases (cut164 holes hbool hrows) (Fin.cases (cut193 holes hbool hrows) (Fin.cases (cut197 holes hbool hrows) (Fin.cases (cut199 holes hbool hrows) (Fin.cases (cut200 holes hbool hrows) (Fin.cases (cut201 holes hbool hrows) (Fin.cases (cut205 holes hbool hrows) (Fin.cases (cut206 holes hbool hrows) (Fin.cases (cut207 holes hbool hrows) (Fin.cases (cut208 holes hbool hrows) (Fin.cases (cut209 holes hbool hrows) (Fin.cases (cut210 holes hbool hrows) (Fin.cases (cut211 holes hbool hrows) (Fin.cases (cut212 holes hbool hrows) (Fin.cases (cut214 holes hbool hrows) (fun i => Fin.elim0 i)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
def support221 : Finset (Fin 252) := {0, 3, 4, 5, 8, 15, 18, 19, 25, 27, 28, 37, 52, 56, 67, 76, 83, 100}
theorem cut221 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support221, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 218, OmissionBalanced.support 202] ![OmissionBalanced.demand 0, OmissionBalanced.demand 218, OmissionBalanced.demand 202] ![1, 1, 1]
    support221 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 218) (Fin.cases (hrows 202) (fun i => Fin.elim0 i))))
def support222 : Finset (Fin 252) := {1, 3, 4, 5, 8, 15, 18, 19, 25, 27, 28, 37, 52, 56, 67, 76, 83, 100}
theorem cut222 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support222, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 218, OmissionBalanced.support 1029, OmissionBalanced.support 202] ![OmissionBalanced.demand 218, OmissionBalanced.demand 1029, OmissionBalanced.demand 202] ![1, 1, 1]
    support222 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 218) (Fin.cases (hrows 1029) (Fin.cases (hrows 202) (fun i => Fin.elim0 i))))
def support223 : Finset (Fin 252) := {1, 2, 4, 8, 12, 15, 18, 25, 27, 28, 37, 38, 41, 51, 59, 65, 81}
theorem cut223 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support223, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 195, OmissionBalanced.support 190] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 195, OmissionBalanced.demand 190] ![1, 1, 1]
    support223 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 195) (Fin.cases (hrows 190) (fun i => Fin.elim0 i))))
def support224 : Finset (Fin 252) := {0, 1, 2, 4, 8, 12, 15, 18, 25, 27, 28, 37, 38, 41, 51, 59, 65, 81}
theorem cut224 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support224, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 195, OmissionBalanced.support 190] ![OmissionBalanced.demand 0, OmissionBalanced.demand 195, OmissionBalanced.demand 190] ![1, 1, 1]
    support224 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 195) (Fin.cases (hrows 190) (fun i => Fin.elim0 i))))
def support225 : Finset (Fin 252) := {0, 3, 4, 5, 8, 15, 18, 19, 25, 27, 28, 37, 38, 41, 51, 59, 65, 81}
theorem cut225 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support225, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 217, OmissionBalanced.support 201] ![OmissionBalanced.demand 0, OmissionBalanced.demand 217, OmissionBalanced.demand 201] ![1, 1, 1]
    support225 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 217) (Fin.cases (hrows 201) (fun i => Fin.elim0 i))))
#print axioms cut225
def support226 : Finset (Fin 252) := {1, 3, 4, 5, 8, 15, 18, 19, 25, 27, 28, 37, 38, 41, 51, 59, 65, 81}
theorem cut226 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support226, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 217, OmissionBalanced.support 201] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 217, OmissionBalanced.demand 201] ![1, 1, 1]
    support226 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 217) (Fin.cases (hrows 201) (fun i => Fin.elim0 i))))
def support227 : Finset (Fin 252) := {0, 4, 6, 8, 10, 15, 18, 25, 27, 30, 37, 41, 52, 56, 67, 76, 83, 100}
theorem cut227 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support227, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 257, OmissionBalanced.support 225] ![OmissionBalanced.demand 0, OmissionBalanced.demand 257, OmissionBalanced.demand 225] ![1, 1, 1]
    support227 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 257) (Fin.cases (hrows 225) (fun i => Fin.elim0 i))))
def support228 : Finset (Fin 252) := {1, 4, 6, 8, 10, 15, 18, 25, 27, 30, 37, 41, 52, 56, 67, 76, 83, 100}
theorem cut228 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support228, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 257, OmissionBalanced.support 225] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 257, OmissionBalanced.demand 225] ![1, 1, 1]
    support228 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 257) (Fin.cases (hrows 225) (fun i => Fin.elim0 i))))
def support229 : Finset (Fin 252) := {1, 2, 4, 7, 8, 15, 18, 20, 25, 27, 31, 37, 38, 46, 51, 65}
theorem cut229 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support229, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 191, OmissionBalanced.support 186] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 191, OmissionBalanced.demand 186] ![1, 1, 1]
    support229 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 191) (Fin.cases (hrows 186) (fun i => Fin.elim0 i))))
def support230 : Finset (Fin 252) := {0, 1, 2, 4, 7, 8, 15, 18, 20, 25, 27, 31, 37, 38, 46, 51, 65}
theorem cut230 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support230, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 191, OmissionBalanced.support 186] ![OmissionBalanced.demand 0, OmissionBalanced.demand 191, OmissionBalanced.demand 186] ![1, 1, 1]
    support230 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 191) (Fin.cases (hrows 186) (fun i => Fin.elim0 i))))
def support231 : Finset (Fin 252) := {0, 4, 8, 15, 18, 25, 27, 37, 64, 81, 86, 100, 105, 121, 124, 143}
theorem cut231 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support231, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 387, OmissionBalanced.support 318] ![OmissionBalanced.demand 0, OmissionBalanced.demand 387, OmissionBalanced.demand 318] ![1, 1, 1]
    support231 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 387) (Fin.cases (hrows 318) (fun i => Fin.elim0 i))))
def support232 : Finset (Fin 252) := {1, 4, 8, 15, 18, 25, 27, 37, 64, 81, 86, 100, 105, 121, 124, 143}
theorem cut232 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support232, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 387, OmissionBalanced.support 318] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 387, OmissionBalanced.demand 318] ![1, 1, 1]
    support232 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 387) (Fin.cases (hrows 318) (fun i => Fin.elim0 i))))
def support233 : Finset (Fin 252) := {0, 4, 8, 11, 15, 17, 18, 25, 27, 34, 37, 46, 61, 79, 86, 105, 124}
theorem cut233 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support233, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 262, OmissionBalanced.support 0, OmissionBalanced.support 311] ![OmissionBalanced.demand 262, OmissionBalanced.demand 0, OmissionBalanced.demand 311] ![1, 1, 1]
    support233 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 262) (Fin.cases (hrows 0) (Fin.cases (hrows 311) (fun i => Fin.elim0 i))))
def support234 : Finset (Fin 252) := {1, 4, 8, 11, 15, 17, 18, 25, 27, 34, 37, 46, 61, 79, 86, 105, 124}
theorem cut234 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support234, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 262, OmissionBalanced.support 1029, OmissionBalanced.support 311] ![OmissionBalanced.demand 262, OmissionBalanced.demand 1029, OmissionBalanced.demand 311] ![1, 1, 1]
    support234 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 262) (Fin.cases (hrows 1029) (Fin.cases (hrows 311) (fun i => Fin.elim0 i))))
def support235 : Finset (Fin 252) := {0, 4, 8, 11, 15, 17, 18, 25, 27, 37, 45, 59, 68, 76, 85, 95, 103, 121}
theorem cut235 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support235, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 263, OmissionBalanced.support 314] ![OmissionBalanced.demand 0, OmissionBalanced.demand 263, OmissionBalanced.demand 314] ![1, 1, 1]
    support235 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 263) (Fin.cases (hrows 314) (fun i => Fin.elim0 i))))
def support236 : Finset (Fin 252) := {1, 4, 8, 11, 15, 17, 18, 25, 27, 37, 45, 59, 68, 76, 85, 95, 103, 121}
theorem cut236 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support236, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 263, OmissionBalanced.support 314] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 263, OmissionBalanced.demand 314] ![1, 1, 1]
    support236 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 263) (Fin.cases (hrows 314) (fun i => Fin.elim0 i))))
def support237 : Finset (Fin 252) := {0, 3, 4, 8, 10, 14, 15, 18, 23, 25, 27, 33, 37, 48, 52, 67}
theorem cut237 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support237, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 1113, OmissionBalanced.support 1045] ![OmissionBalanced.demand 0, OmissionBalanced.demand 1113, OmissionBalanced.demand 1045] ![1, 1, 1]
    support237 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 1113) (Fin.cases (hrows 1045) (fun i => Fin.elim0 i))))
def support238 : Finset (Fin 252) := {1, 3, 4, 8, 10, 14, 15, 18, 23, 25, 27, 33, 37, 48, 52, 67}
theorem cut238 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support238, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 1113, OmissionBalanced.support 1045] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 1113, OmissionBalanced.demand 1045] ![1, 1, 1]
    support238 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 1113) (Fin.cases (hrows 1045) (fun i => Fin.elim0 i))))
def support239 : Finset (Fin 252) := {0, 4, 8, 11, 15, 17, 18, 25, 27, 34, 37, 46, 61, 68, 79, 85, 103}
theorem cut239 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support239, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 261, OmissionBalanced.support 310] ![OmissionBalanced.demand 0, OmissionBalanced.demand 261, OmissionBalanced.demand 310] ![1, 1, 1]
    support239 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 261) (Fin.cases (hrows 310) (fun i => Fin.elim0 i))))
def support240 : Finset (Fin 252) := {1, 4, 8, 11, 15, 17, 18, 25, 27, 34, 37, 46, 61, 68, 79, 85, 103}
theorem cut240 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support240, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 261, OmissionBalanced.support 310] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 261, OmissionBalanced.demand 310] ![1, 1, 1]
    support240 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 261) (Fin.cases (hrows 310) (fun i => Fin.elim0 i))))
def support241 : Finset (Fin 252) := {5, 8, 10, 15, 19, 23, 27, 33, 37, 39, 48, 52, 67, 71, 84, 92, 101, 118}
theorem cut241 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support241, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 220, OmissionBalanced.support 240, OmissionBalanced.support 1113] ![OmissionBalanced.demand 220, OmissionBalanced.demand 240, OmissionBalanced.demand 1113] ![1, 1, 1]
    support241 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 220) (Fin.cases (hrows 240) (Fin.cases (hrows 1113) (fun i => Fin.elim0 i))))
def support242 : Finset (Fin 252) := {5, 8, 14, 19, 27, 33, 37, 39, 48, 52, 67, 71, 84, 92, 101, 118}
theorem cut242 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support242, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 220, OmissionBalanced.support 240, OmissionBalanced.support 15] ![OmissionBalanced.demand 220, OmissionBalanced.demand 240, OmissionBalanced.demand 15] ![1, 1, 1]
    support242 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 220) (Fin.cases (hrows 240) (Fin.cases (hrows 15) (fun i => Fin.elim0 i))))
def support243 : Finset (Fin 252) := {4, 7, 12, 25, 29, 34, 35, 42, 46, 47, 53, 60, 70, 75, 91}
theorem cut243 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support243, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 12, OmissionBalanced.support 227, OmissionBalanced.support 206] ![OmissionBalanced.demand 12, OmissionBalanced.demand 227, OmissionBalanced.demand 206] ![1, 1, 1]
    support243 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 12) (Fin.cases (hrows 227) (Fin.cases (hrows 206) (fun i => Fin.elim0 i))))
def support244 : Finset (Fin 252) := {0, 3, 4, 5, 8, 13, 15, 18, 20, 25, 27, 37, 43, 52, 61, 67, 83}
theorem cut244 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support244, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 210, OmissionBalanced.support 200] ![OmissionBalanced.demand 0, OmissionBalanced.demand 210, OmissionBalanced.demand 200] ![1, 1, 1]
    support244 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 210) (Fin.cases (hrows 200) (fun i => Fin.elim0 i))))
def support245 : Finset (Fin 252) := {1, 3, 4, 5, 8, 13, 15, 18, 20, 25, 27, 37, 43, 52, 61, 67, 83}
theorem cut245 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support245, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 210, OmissionBalanced.support 200] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 210, OmissionBalanced.demand 200] ![1, 1, 1]
    support245 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 210) (Fin.cases (hrows 200) (fun i => Fin.elim0 i))))
def support246 : Finset (Fin 252) := {0, 4, 5, 6, 8, 14, 15, 18, 23, 25, 27, 33, 37, 48, 52, 67}
theorem cut246 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support246, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 15, OmissionBalanced.support 1073] ![OmissionBalanced.demand 0, OmissionBalanced.demand 15, OmissionBalanced.demand 1073] ![1, 1, 1]
    support246 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 15) (Fin.cases (hrows 1073) (fun i => Fin.elim0 i))))
def support247 : Finset (Fin 252) := {1, 4, 5, 6, 8, 14, 15, 18, 23, 25, 27, 33, 37, 48, 52, 67}
theorem cut247 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support247, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 15, OmissionBalanced.support 1073] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 15, OmissionBalanced.demand 1073] ![1, 1, 1]
    support247 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 15) (Fin.cases (hrows 1073) (fun i => Fin.elim0 i))))
def support248 : Finset (Fin 252) := {1, 4, 5, 8, 14, 15, 18, 23, 25, 27, 35, 37, 38, 51}
theorem cut248 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support248, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 1060, OmissionBalanced.support 1030] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 1060, OmissionBalanced.demand 1030] ![1, 1, 1]
    support248 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 1060) (Fin.cases (hrows 1030) (fun i => Fin.elim0 i))))
def support249 : Finset (Fin 252) := {0, 1, 4, 5, 8, 14, 15, 18, 23, 25, 27, 35, 37, 38, 51}
theorem cut249 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support249, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 1060, OmissionBalanced.support 1030] ![OmissionBalanced.demand 0, OmissionBalanced.demand 1060, OmissionBalanced.demand 1030] ![1, 1, 1]
    support249 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 1060) (Fin.cases (hrows 1030) (fun i => Fin.elim0 i))))
def support250 : Finset (Fin 252) := {0, 2, 3, 4, 8, 14, 15, 18, 23, 25, 27, 35, 37, 38, 51}
theorem cut250 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support250, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 1035, OmissionBalanced.support 1044] ![OmissionBalanced.demand 0, OmissionBalanced.demand 1035, OmissionBalanced.demand 1044] ![1, 1, 1]
    support250 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 1035) (Fin.cases (hrows 1044) (fun i => Fin.elim0 i))))
#print axioms cut250
def support251 : Finset (Fin 252) := {1, 2, 3, 4, 8, 14, 15, 18, 23, 25, 27, 35, 37, 38, 51}
theorem cut251 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support251, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 1035, OmissionBalanced.support 1044] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 1035, OmissionBalanced.demand 1044] ![1, 1, 1]
    support251 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 1035) (Fin.cases (hrows 1044) (fun i => Fin.elim0 i))))
def support252 : Finset (Fin 252) := {108, 127, 130, 146, 151, 165, 170, 187, 214, 224, 226, 233, 236, 243, 247, 250}
theorem cut252 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support252, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 844, OmissionBalanced.support 843, OmissionBalanced.support 2681] ![OmissionBalanced.demand 844, OmissionBalanced.demand 843, OmissionBalanced.demand 2681] ![1, 1, 1]
    support252 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 844) (Fin.cases (hrows 843) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support253 : Finset (Fin 252) := {108, 127, 130, 146, 151, 165, 170, 187, 214, 224, 226, 233, 236, 243, 247, 251}
theorem cut253 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support253, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 844, OmissionBalanced.support 843, OmissionBalanced.support 2682] ![OmissionBalanced.demand 844, OmissionBalanced.demand 843, OmissionBalanced.demand 2682] ![1, 1, 1]
    support253 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 844) (Fin.cases (hrows 843) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support254 : Finset (Fin 252) := {170, 186, 192, 200, 210, 213, 214, 223, 224, 226, 232, 233, 236, 243, 246, 247, 248, 250}
theorem cut254 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support254, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1004, OmissionBalanced.support 1002, OmissionBalanced.support 2681] ![OmissionBalanced.demand 1004, OmissionBalanced.demand 1002, OmissionBalanced.demand 2681] ![1, 1, 1]
    support254 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1004) (Fin.cases (hrows 1002) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support255 : Finset (Fin 252) := {170, 186, 192, 200, 210, 213, 214, 223, 224, 226, 232, 233, 236, 243, 246, 247, 248, 251}
theorem cut255 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support255, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1004, OmissionBalanced.support 1002, OmissionBalanced.support 2682] ![OmissionBalanced.demand 1004, OmissionBalanced.demand 1002, OmissionBalanced.demand 2682] ![1, 1, 1]
    support255 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1004) (Fin.cases (hrows 1002) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support256 : Finset (Fin 252) := {170, 186, 192, 200, 210, 213, 214, 223, 224, 226, 233, 236, 239, 243, 247, 249, 250}
theorem cut256 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support256, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1005, OmissionBalanced.support 1003, OmissionBalanced.support 2681] ![OmissionBalanced.demand 1005, OmissionBalanced.demand 1003, OmissionBalanced.demand 2681] ![1, 1, 1]
    support256 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1005) (Fin.cases (hrows 1003) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support257 : Finset (Fin 252) := {170, 186, 192, 200, 210, 213, 214, 223, 224, 226, 233, 236, 239, 243, 247, 249, 250, 251}
theorem cut257 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support257, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1005, OmissionBalanced.support 1003, OmissionBalanced.support 2682] ![OmissionBalanced.demand 1005, OmissionBalanced.demand 1003, OmissionBalanced.demand 2682] ![1, 1, 1]
    support257 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1005) (Fin.cases (hrows 1003) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support258 : Finset (Fin 252) := {186, 200, 205, 213, 214, 220, 224, 226, 231, 233, 236, 243, 244, 247, 249, 250}
theorem cut258 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support258, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1017, OmissionBalanced.support 1015, OmissionBalanced.support 2681] ![OmissionBalanced.demand 1017, OmissionBalanced.demand 1015, OmissionBalanced.demand 2681] ![1, 1, 1]
    support258 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1017) (Fin.cases (hrows 1015) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support259 : Finset (Fin 252) := {186, 200, 205, 213, 214, 220, 224, 226, 231, 233, 236, 238, 243, 246, 247, 248, 250}
theorem cut259 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support259, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1016, OmissionBalanced.support 1014, OmissionBalanced.support 2681] ![OmissionBalanced.demand 1016, OmissionBalanced.demand 1014, OmissionBalanced.demand 2681] ![1, 1, 1]
    support259 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1016) (Fin.cases (hrows 1014) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support260 : Finset (Fin 252) := {186, 200, 205, 213, 214, 220, 224, 226, 231, 233, 236, 238, 243, 246, 247, 248, 251}
theorem cut260 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support260, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1016, OmissionBalanced.support 1014, OmissionBalanced.support 2682] ![OmissionBalanced.demand 1016, OmissionBalanced.demand 1014, OmissionBalanced.demand 2682] ![1, 1, 1]
    support260 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1016) (Fin.cases (hrows 1014) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support261 : Finset (Fin 252) := {186, 200, 205, 213, 214, 220, 224, 226, 231, 233, 236, 243, 244, 247, 249, 250, 251}
theorem cut261 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support261, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1017, OmissionBalanced.support 1015, OmissionBalanced.support 2682] ![OmissionBalanced.demand 1017, OmissionBalanced.demand 1015, OmissionBalanced.demand 2682] ![1, 1, 1]
    support261 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1017) (Fin.cases (hrows 1015) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support262 : Finset (Fin 252) := {130, 148, 156, 166, 183, 195, 210, 214, 221, 224, 226, 233, 236, 241, 243, 245, 247, 250}
theorem cut262 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support262, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 920, OmissionBalanced.support 919, OmissionBalanced.support 2681] ![OmissionBalanced.demand 920, OmissionBalanced.demand 919, OmissionBalanced.demand 2681] ![1, 1, 1]
    support262 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 920) (Fin.cases (hrows 919) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support263 : Finset (Fin 252) := {130, 148, 156, 166, 183, 195, 210, 214, 221, 224, 226, 233, 236, 241, 243, 245, 247, 251}
theorem cut263 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support263, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 920, OmissionBalanced.support 919, OmissionBalanced.support 2682] ![OmissionBalanced.demand 920, OmissionBalanced.demand 919, OmissionBalanced.demand 2682] ![1, 1, 1]
    support263 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 920) (Fin.cases (hrows 919) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support264 : Finset (Fin 252) := {0, 4, 8, 11, 15, 17, 18, 25, 27, 37, 45, 59, 76, 86, 95, 105, 124, 143}
theorem cut264 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support264, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 264, OmissionBalanced.support 315] ![OmissionBalanced.demand 0, OmissionBalanced.demand 264, OmissionBalanced.demand 315] ![1, 1, 1]
    support264 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 264) (Fin.cases (hrows 315) (fun i => Fin.elim0 i))))
def support265 : Finset (Fin 252) := {1, 4, 8, 11, 15, 17, 18, 25, 27, 37, 45, 59, 76, 86, 95, 105, 124, 143}
theorem cut265 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support265, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 264, OmissionBalanced.support 315] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 264, OmissionBalanced.demand 315] ![1, 1, 1]
    support265 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 264) (Fin.cases (hrows 315) (fun i => Fin.elim0 i))))
def support266 : Finset (Fin 252) := {10, 15, 23, 27, 30, 33, 37, 48, 52, 54, 67, 71, 84, 92, 101, 118}
theorem cut266 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support266, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 259, OmissionBalanced.support 1113, OmissionBalanced.support 294] ![OmissionBalanced.demand 259, OmissionBalanced.demand 1113, OmissionBalanced.demand 294] ![1, 1, 1]
    support266 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 259) (Fin.cases (hrows 1113) (Fin.cases (hrows 294) (fun i => Fin.elim0 i))))
def support267 : Finset (Fin 252) := {33, 43, 56, 61, 67, 72, 79, 85, 88, 90, 107, 134, 142, 153, 169, 177, 191}
theorem cut267 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support267, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 431, OmissionBalanced.support 497, OmissionBalanced.support 439] ![OmissionBalanced.demand 431, OmissionBalanced.demand 497, OmissionBalanced.demand 439] ![1, 1, 1]
    support267 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 431) (Fin.cases (hrows 497) (Fin.cases (hrows 439) (fun i => Fin.elim0 i))))
def support268 : Finset (Fin 252) := {94, 111, 120, 137, 147, 158, 163, 166, 171, 176, 181, 188, 214, 217, 221, 226, 236}
theorem cut268 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support268, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 895, OmissionBalanced.support 799, OmissionBalanced.support 856] ![OmissionBalanced.demand 895, OmissionBalanced.demand 799, OmissionBalanced.demand 856] ![1, 1, 1]
    support268 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 895) (Fin.cases (hrows 799) (Fin.cases (hrows 856) (fun i => Fin.elim0 i))))
def support269 : Finset (Fin 252) := {5, 8, 9, 14, 21, 23, 27, 35, 38, 44, 51, 52, 62, 84}
theorem cut269 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support269, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 16, OmissionBalanced.support 30, OmissionBalanced.support 1060] ![OmissionBalanced.demand 16, OmissionBalanced.demand 30, OmissionBalanced.demand 1060] ![1, 1, 1]
    support269 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 16) (Fin.cases (hrows 30) (Fin.cases (hrows 1060) (fun i => Fin.elim0 i))))
def support270 : Finset (Fin 252) := {5, 8, 14, 16, 21, 23, 27, 32, 35, 38, 44, 51, 52, 62, 84}
theorem cut270 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support270, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 16, OmissionBalanced.support 1189, OmissionBalanced.support 1060] ![OmissionBalanced.demand 16, OmissionBalanced.demand 1189, OmissionBalanced.demand 1060] ![1, 1, 1]
    support270 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 16) (Fin.cases (hrows 1189) (Fin.cases (hrows 1060) (fun i => Fin.elim0 i))))
def support271 : Finset (Fin 252) := {5, 8, 10, 14, 15, 16, 23, 27, 32, 35, 38, 44, 51, 52, 62, 84}
theorem cut271 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support271, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1114, OmissionBalanced.support 1189, OmissionBalanced.support 1060] ![OmissionBalanced.demand 1114, OmissionBalanced.demand 1189, OmissionBalanced.demand 1060] ![1, 1, 1]
    support271 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1114) (Fin.cases (hrows 1189) (Fin.cases (hrows 1060) (fun i => Fin.elim0 i))))
def support272 : Finset (Fin 252) := {5, 8, 9, 10, 14, 15, 21, 23, 27, 32, 35, 38, 44, 51, 52, 62, 84}
theorem cut272 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support272, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1114, OmissionBalanced.support 30, OmissionBalanced.support 1060] ![OmissionBalanced.demand 1114, OmissionBalanced.demand 30, OmissionBalanced.demand 1060] ![1, 1, 1]
    support272 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1114) (Fin.cases (hrows 30) (Fin.cases (hrows 1060) (fun i => Fin.elim0 i))))
def support273 : Finset (Fin 252) := {2, 4, 10, 14, 15, 16, 23, 27, 32, 35, 38, 44, 51, 52, 62, 84}
theorem cut273 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support273, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1114, OmissionBalanced.support 1189, OmissionBalanced.support 1035] ![OmissionBalanced.demand 1114, OmissionBalanced.demand 1189, OmissionBalanced.demand 1035] ![1, 1, 1]
    support273 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1114) (Fin.cases (hrows 1189) (Fin.cases (hrows 1035) (fun i => Fin.elim0 i))))
def support274 : Finset (Fin 252) := {2, 4, 9, 10, 14, 15, 21, 23, 27, 32, 35, 38, 44, 51, 52, 62, 84}
theorem cut274 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support274, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1114, OmissionBalanced.support 30, OmissionBalanced.support 1035] ![OmissionBalanced.demand 1114, OmissionBalanced.demand 30, OmissionBalanced.demand 1035] ![1, 1, 1]
    support274 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1114) (Fin.cases (hrows 30) (Fin.cases (hrows 1035) (fun i => Fin.elim0 i))))
def support275 : Finset (Fin 252) := {5, 8, 10, 14, 15, 27, 30, 33, 37, 48, 52, 54, 67, 71, 84, 92, 101, 118}
theorem cut275 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support275, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 259, OmissionBalanced.support 15, OmissionBalanced.support 294] ![OmissionBalanced.demand 259, OmissionBalanced.demand 15, OmissionBalanced.demand 294] ![1, 1, 1]
    support275 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 259) (Fin.cases (hrows 15) (Fin.cases (hrows 294) (fun i => Fin.elim0 i))))
#print axioms cut275
def support276 : Finset (Fin 252) := {160, 176, 181, 191, 198, 204, 205, 209, 216, 217, 222, 226, 232, 238, 243}
theorem cut276 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support276, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 990, OmissionBalanced.support 992, OmissionBalanced.support 169] ![OmissionBalanced.demand 990, OmissionBalanced.demand 992, OmissionBalanced.demand 169] ![1, 1, 1]
    support276 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 990) (Fin.cases (hrows 992) (Fin.cases (hrows 169) (fun i => Fin.elim0 i))))
def support277 : Finset (Fin 252) := {160, 176, 181, 191, 198, 204, 205, 209, 216, 217, 222, 226, 239, 244, 247}
theorem cut277 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support277, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 991, OmissionBalanced.support 993, OmissionBalanced.support 170] ![OmissionBalanced.demand 991, OmissionBalanced.demand 993, OmissionBalanced.demand 170] ![1, 1, 1]
    support277 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 991) (Fin.cases (hrows 993) (Fin.cases (hrows 170) (fun i => Fin.elim0 i))))
def support278 : Finset (Fin 252) := {2, 4, 5, 8, 9, 14, 21, 23, 27, 35, 38, 44, 51, 52, 62, 84}
theorem cut278 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support278, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 16, OmissionBalanced.support 30, OmissionBalanced.support 1035] ![OmissionBalanced.demand 16, OmissionBalanced.demand 30, OmissionBalanced.demand 1035] ![1, 1, 1]
    support278 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 16) (Fin.cases (hrows 30) (Fin.cases (hrows 1035) (fun i => Fin.elim0 i))))
def support279 : Finset (Fin 252) := {2, 4, 5, 8, 14, 16, 21, 23, 27, 32, 35, 38, 44, 51, 52, 62, 84}
theorem cut279 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support279, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 16, OmissionBalanced.support 1189, OmissionBalanced.support 1035] ![OmissionBalanced.demand 16, OmissionBalanced.demand 1189, OmissionBalanced.demand 1035] ![1, 1, 1]
    support279 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 16) (Fin.cases (hrows 1189) (Fin.cases (hrows 1035) (fun i => Fin.elim0 i))))
def support280 : Finset (Fin 252) := {0, 4, 6, 8, 10, 15, 18, 22, 25, 27, 31, 37, 43, 52, 61, 67, 83}
theorem cut280 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support280, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 253, OmissionBalanced.support 223] ![OmissionBalanced.demand 0, OmissionBalanced.demand 253, OmissionBalanced.demand 223] ![1, 1, 1]
    support280 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 253) (Fin.cases (hrows 223) (fun i => Fin.elim0 i))))
def support281 : Finset (Fin 252) := {1, 4, 6, 8, 10, 15, 18, 22, 25, 27, 31, 37, 43, 52, 61, 67, 83}
theorem cut281 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support281, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 253, OmissionBalanced.support 223] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 253, OmissionBalanced.demand 223] ![1, 1, 1]
    support281 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 253) (Fin.cases (hrows 223) (fun i => Fin.elim0 i))))
def support282 : Finset (Fin 252) := {122, 139, 144, 157, 173, 178, 190, 198, 203, 205, 216, 222, 223, 231, 237}
theorem cut282 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support282, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 132, OmissionBalanced.support 902, OmissionBalanced.support 898] ![OmissionBalanced.demand 132, OmissionBalanced.demand 902, OmissionBalanced.demand 898] ![1, 1, 1]
    support282 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 132) (Fin.cases (hrows 902) (Fin.cases (hrows 898) (fun i => Fin.elim0 i))))
def support283 : Finset (Fin 252) := {0, 4, 6, 8, 10, 15, 18, 25, 27, 30, 37, 41, 56, 68, 85, 95, 103, 121}
theorem cut283 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support283, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 258, OmissionBalanced.support 226] ![OmissionBalanced.demand 0, OmissionBalanced.demand 258, OmissionBalanced.demand 226] ![1, 1, 1]
    support283 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 258) (Fin.cases (hrows 226) (fun i => Fin.elim0 i))))
def support284 : Finset (Fin 252) := {1, 4, 6, 8, 10, 15, 18, 25, 27, 30, 37, 41, 56, 68, 85, 95, 103, 121}
theorem cut284 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support284, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 258, OmissionBalanced.support 226] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 258, OmissionBalanced.demand 226] ![1, 1, 1]
    support284 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 258) (Fin.cases (hrows 226) (fun i => Fin.elim0 i))))
def support285 : Finset (Fin 252) := {133, 150, 159, 167, 180, 184, 199, 203, 212, 214, 218, 224, 232, 237, 243, 246}
theorem cut285 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support285, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 935, OmissionBalanced.support 931, OmissionBalanced.support 2651] ![OmissionBalanced.demand 935, OmissionBalanced.demand 931, OmissionBalanced.demand 2651] ![1, 1, 1]
    support285 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 935) (Fin.cases (hrows 931) (Fin.cases (hrows 2651) (fun i => Fin.elim0 i))))
def support286 : Finset (Fin 252) := {5, 10, 16, 19, 27, 30, 32, 39, 42, 52, 54, 71, 84, 92, 101, 118}
theorem cut286 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support286, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 220, OmissionBalanced.support 259, OmissionBalanced.support 1063] ![OmissionBalanced.demand 220, OmissionBalanced.demand 259, OmissionBalanced.demand 1063] ![1, 1, 1]
    support286 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 220) (Fin.cases (hrows 259) (Fin.cases (hrows 1063) (fun i => Fin.elim0 i))))
def support287 : Finset (Fin 252) := {5, 8, 10, 15, 19, 23, 27, 30, 32, 39, 42, 52, 54, 71, 84, 92, 101, 118}
theorem cut287 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support287, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 220, OmissionBalanced.support 259, OmissionBalanced.support 1090] ![OmissionBalanced.demand 220, OmissionBalanced.demand 259, OmissionBalanced.demand 1090] ![1, 1, 1]
    support287 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 220) (Fin.cases (hrows 259) (Fin.cases (hrows 1090) (fun i => Fin.elim0 i))))
def support288 : Finset (Fin 252) := {130, 148, 156, 166, 172, 183, 188, 190, 195, 202, 205, 210, 217, 221, 233, 240, 245}
theorem cut288 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support288, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 981, OmissionBalanced.support 920, OmissionBalanced.support 958] ![OmissionBalanced.demand 981, OmissionBalanced.demand 920, OmissionBalanced.demand 958] ![1, 1, 1]
    support288 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 981) (Fin.cases (hrows 920) (Fin.cases (hrows 958) (fun i => Fin.elim0 i))))
def support289 : Finset (Fin 252) := {110, 128, 136, 157, 173, 178, 183, 191, 205, 209, 213, 215, 220, 225, 235}
theorem cut289 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support289, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 854, OmissionBalanced.support 133, OmissionBalanced.support 850] ![OmissionBalanced.demand 854, OmissionBalanced.demand 133, OmissionBalanced.demand 850] ![1, 1, 1]
    support289 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 854) (Fin.cases (hrows 133) (Fin.cases (hrows 850) (fun i => Fin.elim0 i))))
def support290 : Finset (Fin 252) := {5, 8, 14, 23, 27, 35, 38, 51, 64, 81, 86, 98, 118, 125, 139, 144, 161}
theorem cut290 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support290, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 388, OmissionBalanced.support 468, OmissionBalanced.support 1060] ![OmissionBalanced.demand 388, OmissionBalanced.demand 468, OmissionBalanced.demand 1060] ![1, 1, 1]
    support290 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 388) (Fin.cases (hrows 468) (Fin.cases (hrows 1060) (fun i => Fin.elim0 i))))
def support291 : Finset (Fin 252) := {2, 4, 14, 23, 27, 35, 38, 51, 64, 81, 86, 98, 118, 125, 139, 144, 161}
theorem cut291 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support291, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 388, OmissionBalanced.support 468, OmissionBalanced.support 1035] ![OmissionBalanced.demand 388, OmissionBalanced.demand 468, OmissionBalanced.demand 1035] ![1, 1, 1]
    support291 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 388) (Fin.cases (hrows 468) (Fin.cases (hrows 1035) (fun i => Fin.elim0 i))))
def support292 : Finset (Fin 252) := {46, 59, 65, 81, 109, 121, 124, 135, 147, 158, 163, 167, 171, 174, 180, 189, 207}
theorem cut292 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support292, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 528, OmissionBalanced.support 658, OmissionBalanced.support 606] ![OmissionBalanced.demand 528, OmissionBalanced.demand 658, OmissionBalanced.demand 606] ![1, 1, 1]
    support292 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 528) (Fin.cases (hrows 658) (Fin.cases (hrows 606) (fun i => Fin.elim0 i))))
def support293 : Finset (Fin 252) := {151, 168, 175, 184, 195, 199, 210, 214, 221, 224, 226, 233, 236, 241, 243, 245, 247, 250}
theorem cut293 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support293, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 970, OmissionBalanced.support 969, OmissionBalanced.support 2681] ![OmissionBalanced.demand 970, OmissionBalanced.demand 969, OmissionBalanced.demand 2681] ![1, 1, 1]
    support293 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 970) (Fin.cases (hrows 969) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support294 : Finset (Fin 252) := {151, 168, 175, 184, 195, 199, 210, 214, 221, 224, 226, 233, 236, 241, 243, 245, 247, 251}
theorem cut294 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support294, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 970, OmissionBalanced.support 969, OmissionBalanced.support 2682] ![OmissionBalanced.demand 970, OmissionBalanced.demand 969, OmissionBalanced.demand 2682] ![1, 1, 1]
    support294 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 970) (Fin.cases (hrows 969) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support295 : Finset (Fin 252) := {133, 150, 159, 167, 180, 197, 199, 209, 212, 219, 221, 224, 232, 235, 241, 246}
theorem cut295 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support295, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 935, OmissionBalanced.support 933, OmissionBalanced.support 2668] ![OmissionBalanced.demand 935, OmissionBalanced.demand 933, OmissionBalanced.demand 2668] ![1, 1, 1]
    support295 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 935) (Fin.cases (hrows 933) (Fin.cases (hrows 2668) (fun i => Fin.elim0 i))))
def support296 : Finset (Fin 252) := {134, 152, 160, 176, 181, 185, 191, 196, 198, 200, 205, 211, 214, 217, 232, 238, 243}
theorem cut296 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support296, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 990, OmissionBalanced.support 973, OmissionBalanced.support 938] ![OmissionBalanced.demand 990, OmissionBalanced.demand 973, OmissionBalanced.demand 938] ![1, 1, 1]
    support296 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 990) (Fin.cases (hrows 973) (Fin.cases (hrows 938) (fun i => Fin.elim0 i))))
def support297 : Finset (Fin 252) := {134, 152, 160, 176, 181, 185, 191, 196, 198, 200, 205, 211, 214, 217, 239, 244, 247}
theorem cut297 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support297, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 991, OmissionBalanced.support 974, OmissionBalanced.support 939] ![OmissionBalanced.demand 991, OmissionBalanced.demand 974, OmissionBalanced.demand 939] ![1, 1, 1]
    support297 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 991) (Fin.cases (hrows 974) (Fin.cases (hrows 939) (fun i => Fin.elim0 i))))
def support298 : Finset (Fin 252) := {8, 15, 19, 23, 30, 32, 37, 39, 42, 54, 67, 71, 84, 92, 101, 118}
theorem cut298 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support298, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 240, OmissionBalanced.support 294, OmissionBalanced.support 1090] ![OmissionBalanced.demand 240, OmissionBalanced.demand 294, OmissionBalanced.demand 1090] ![1, 1, 1]
    support298 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 240) (Fin.cases (hrows 294) (Fin.cases (hrows 1090) (fun i => Fin.elim0 i))))
def support299 : Finset (Fin 252) := {112, 129, 138, 147, 155, 171, 174, 180, 183, 191, 197, 202, 205, 210, 213, 225, 235}
theorem cut299 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support299, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 942, OmissionBalanced.support 865, OmissionBalanced.support 913] ![OmissionBalanced.demand 942, OmissionBalanced.demand 865, OmissionBalanced.demand 913] ![1, 1, 1]
    support299 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 942) (Fin.cases (hrows 865) (Fin.cases (hrows 913) (fun i => Fin.elim0 i))))
def support300 : Finset (Fin 252) := {9, 14, 21, 38, 44, 52, 62, 81, 84, 86, 98, 100, 118, 137, 145, 158, 163, 179}
theorem cut300 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support300, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 564, OmissionBalanced.support 469, OmissionBalanced.support 30] ![OmissionBalanced.demand 564, OmissionBalanced.demand 469, OmissionBalanced.demand 30] ![1, 1, 1]
    support300 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 564) (Fin.cases (hrows 469) (Fin.cases (hrows 30) (fun i => Fin.elim0 i))))
#print axioms cut300
def support301 : Finset (Fin 252) := {16, 23, 32, 38, 44, 52, 62, 81, 84, 86, 98, 100, 118, 137, 145, 158, 163, 179}
theorem cut301 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support301, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 564, OmissionBalanced.support 469, OmissionBalanced.support 1189] ![OmissionBalanced.demand 564, OmissionBalanced.demand 469, OmissionBalanced.demand 1189] ![1, 1, 1]
    support301 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 564) (Fin.cases (hrows 469) (Fin.cases (hrows 1189) (fun i => Fin.elim0 i))))
def support302 : Finset (Fin 252) := {6, 11, 15, 22, 23, 25, 31, 35, 36, 43, 48, 55, 61, 63, 72, 80, 114}
theorem cut302 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support302, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 52, OmissionBalanced.support 69, OmissionBalanced.support 21] ![OmissionBalanced.demand 52, OmissionBalanced.demand 69, OmissionBalanced.demand 21] ![1, 1, 1]
    support302 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 52) (Fin.cases (hrows 69) (Fin.cases (hrows 21) (fun i => Fin.elim0 i))))
def support303 : Finset (Fin 252) := {5, 8, 10, 14, 15, 16, 23, 27, 32, 35, 38, 44, 51, 68, 80, 104}
theorem cut303 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support303, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 37, OmissionBalanced.support 1060, OmissionBalanced.support 53] ![OmissionBalanced.demand 37, OmissionBalanced.demand 1060, OmissionBalanced.demand 53] ![1, 1, 1]
    support303 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 37) (Fin.cases (hrows 1060) (Fin.cases (hrows 53) (fun i => Fin.elim0 i))))
def support304 : Finset (Fin 252) := {2, 4, 10, 14, 15, 16, 23, 27, 32, 35, 38, 44, 51, 68, 80, 104}
theorem cut304 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support304, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 37, OmissionBalanced.support 1035, OmissionBalanced.support 53] ![OmissionBalanced.demand 37, OmissionBalanced.demand 1035, OmissionBalanced.demand 53] ![1, 1, 1]
    support304 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 37) (Fin.cases (hrows 1035) (Fin.cases (hrows 53) (fun i => Fin.elim0 i))))
def support305 : Finset (Fin 252) := {8, 15, 19, 23, 30, 32, 37, 53, 55, 67, 70, 84, 88, 110, 119, 136}
theorem cut305 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support305, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 242, OmissionBalanced.support 296, OmissionBalanced.support 28] ![OmissionBalanced.demand 242, OmissionBalanced.demand 296, OmissionBalanced.demand 28] ![1, 1, 1]
    support305 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 242) (Fin.cases (hrows 296) (Fin.cases (hrows 28) (fun i => Fin.elim0 i))))
def support306 : Finset (Fin 252) := {8, 15, 19, 23, 25, 30, 32, 48, 53, 55, 62, 70, 88, 93, 110}
theorem cut306 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support306, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 238, OmissionBalanced.support 291, OmissionBalanced.support 28] ![OmissionBalanced.demand 238, OmissionBalanced.demand 291, OmissionBalanced.demand 28] ![1, 1, 1]
    support306 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 238) (Fin.cases (hrows 291) (Fin.cases (hrows 28) (fun i => Fin.elim0 i))))
def support307 : Finset (Fin 252) := {5, 8, 10, 15, 16, 19, 30, 32, 37, 39, 42, 54, 67, 71, 84, 92, 101, 118}
theorem cut307 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support307, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 240, OmissionBalanced.support 294, OmissionBalanced.support 1063] ![OmissionBalanced.demand 240, OmissionBalanced.demand 294, OmissionBalanced.demand 1063] ![1, 1, 1]
    support307 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 240) (Fin.cases (hrows 294) (Fin.cases (hrows 1063) (fun i => Fin.elim0 i))))
def support308 : Finset (Fin 252) := {159, 174, 180, 189, 197, 203, 209, 212, 219, 221, 226, 232, 235, 236, 241, 243, 246}
theorem cut308 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support308, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 987, OmissionBalanced.support 983, OmissionBalanced.support 2668] ![OmissionBalanced.demand 987, OmissionBalanced.demand 983, OmissionBalanced.demand 2668] ![1, 1, 1]
    support308 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 987) (Fin.cases (hrows 983) (Fin.cases (hrows 2668) (fun i => Fin.elim0 i))))
def support309 : Finset (Fin 252) := {133, 150, 159, 167, 180, 184, 199, 203, 212, 214, 218, 224, 228, 232, 236, 241, 243, 246}
theorem cut309 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support309, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 935, OmissionBalanced.support 931, OmissionBalanced.support 161] ![OmissionBalanced.demand 935, OmissionBalanced.demand 931, OmissionBalanced.demand 161] ![1, 1, 1]
    support309 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 935) (Fin.cases (hrows 931) (Fin.cases (hrows 161) (fun i => Fin.elim0 i))))
def support310 : Finset (Fin 252) := {10, 17, 22, 27, 34, 36, 42, 57, 60, 62, 68, 77, 96, 104, 122}
theorem cut310 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support310, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 312, OmissionBalanced.support 40, OmissionBalanced.support 256] ![OmissionBalanced.demand 312, OmissionBalanced.demand 40, OmissionBalanced.demand 256] ![1, 1, 1]
    support310 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 312) (Fin.cases (hrows 40) (Fin.cases (hrows 256) (fun i => Fin.elim0 i))))
def support311 : Finset (Fin 252) := {0, 3, 4, 5, 8, 13, 15, 18, 20, 25, 27, 31, 37, 38, 46, 51, 65}
theorem cut311 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support311, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 209, OmissionBalanced.support 199] ![OmissionBalanced.demand 0, OmissionBalanced.demand 209, OmissionBalanced.demand 199] ![1, 1, 1]
    support311 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 209) (Fin.cases (hrows 199) (fun i => Fin.elim0 i))))
def support312 : Finset (Fin 252) := {1, 3, 4, 5, 8, 13, 15, 18, 20, 25, 27, 31, 37, 38, 46, 51, 65}
theorem cut312 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support312, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 209, OmissionBalanced.support 199] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 209, OmissionBalanced.demand 199] ![1, 1, 1]
    support312 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 209) (Fin.cases (hrows 199) (fun i => Fin.elim0 i))))
def support313 : Finset (Fin 252) := {133, 150, 159, 167, 180, 184, 197, 209, 212, 214, 219, 221, 232, 235, 236, 241, 243, 246}
theorem cut313 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support313, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 931, OmissionBalanced.support 929, OmissionBalanced.support 2668] ![OmissionBalanced.demand 931, OmissionBalanced.demand 929, OmissionBalanced.demand 2668] ![1, 1, 1]
    support313 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 931) (Fin.cases (hrows 929) (Fin.cases (hrows 2668) (fun i => Fin.elim0 i))))
def support314 : Finset (Fin 252) := {10, 15, 17, 22, 23, 25, 31, 35, 36, 43, 48, 55, 61, 63, 72, 80, 114}
theorem cut314 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support314, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 52, OmissionBalanced.support 69, OmissionBalanced.support 38] ![OmissionBalanced.demand 52, OmissionBalanced.demand 69, OmissionBalanced.demand 38] ![1, 1, 1]
    support314 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 52) (Fin.cases (hrows 69) (Fin.cases (hrows 38) (fun i => Fin.elim0 i))))
def support315 : Finset (Fin 252) := {16, 26, 31, 36, 38, 42, 46, 60, 68, 73, 78, 94, 115, 123, 141}
theorem cut315 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support315, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 305, OmissionBalanced.support 57, OmissionBalanced.support 380] ![OmissionBalanced.demand 305, OmissionBalanced.demand 57, OmissionBalanced.demand 380] ![1, 1, 1]
    support315 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 305) (Fin.cases (hrows 57) (Fin.cases (hrows 380) (fun i => Fin.elim0 i))))
def support316 : Finset (Fin 252) := {112, 129, 138, 147, 155, 166, 171, 174, 180, 188, 191, 197, 214, 217, 221, 226, 236}
theorem cut316 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support316, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 941, OmissionBalanced.support 910, OmissionBalanced.support 864] ![OmissionBalanced.demand 941, OmissionBalanced.demand 910, OmissionBalanced.demand 864] ![1, 1, 1]
    support316 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 941) (Fin.cases (hrows 910) (Fin.cases (hrows 864) (fun i => Fin.elim0 i))))
def support317 : Finset (Fin 252) := {112, 129, 138, 147, 155, 171, 174, 180, 183, 191, 197, 202, 217, 221, 224, 234, 241}
theorem cut317 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support317, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 943, OmissionBalanced.support 914, OmissionBalanced.support 866] ![OmissionBalanced.demand 943, OmissionBalanced.demand 914, OmissionBalanced.demand 866] ![1, 1, 1]
    support317 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 943) (Fin.cases (hrows 914) (Fin.cases (hrows 866) (fun i => Fin.elim0 i))))
def support318 : Finset (Fin 252) := {10, 15, 23, 27, 30, 33, 37, 54, 63, 68, 71, 85, 104, 113, 122, 139}
theorem cut318 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support318, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 260, OmissionBalanced.support 295, OmissionBalanced.support 36] ![OmissionBalanced.demand 260, OmissionBalanced.demand 295, OmissionBalanced.demand 36] ![1, 1, 1]
    support318 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 260) (Fin.cases (hrows 295) (Fin.cases (hrows 36) (fun i => Fin.elim0 i))))
def support319 : Finset (Fin 252) := {168, 184, 190, 199, 208, 214, 224, 226, 231, 233, 236, 238, 243, 246, 247, 248, 250}
theorem cut319 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support319, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 997, OmissionBalanced.support 996, OmissionBalanced.support 2681] ![OmissionBalanced.demand 997, OmissionBalanced.demand 996, OmissionBalanced.demand 2681] ![1, 1, 1]
    support319 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 997) (Fin.cases (hrows 996) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support320 : Finset (Fin 252) := {168, 184, 190, 199, 208, 214, 224, 226, 231, 233, 236, 238, 243, 246, 247, 248, 251}
theorem cut320 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support320, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 997, OmissionBalanced.support 996, OmissionBalanced.support 2682] ![OmissionBalanced.demand 997, OmissionBalanced.demand 996, OmissionBalanced.demand 2682] ![1, 1, 1]
    support320 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 997) (Fin.cases (hrows 996) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support321 : Finset (Fin 252) := {16, 23, 24, 32, 33, 38, 44, 52, 58, 62, 68, 84, 97, 123}
theorem cut321 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support321, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1189, OmissionBalanced.support 71, OmissionBalanced.support 55] ![OmissionBalanced.demand 1189, OmissionBalanced.demand 71, OmissionBalanced.demand 55] ![1, 1, 1]
    support321 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1189) (Fin.cases (hrows 71) (Fin.cases (hrows 55) (fun i => Fin.elim0 i))))
def support322 : Finset (Fin 252) := {9, 14, 16, 21, 23, 24, 32, 33, 38, 44, 52, 58, 62, 68, 84, 97, 123}
theorem cut322 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support322, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 30, OmissionBalanced.support 71, OmissionBalanced.support 55] ![OmissionBalanced.demand 30, OmissionBalanced.demand 71, OmissionBalanced.demand 55] ![1, 1, 1]
    support322 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 30) (Fin.cases (hrows 71) (Fin.cases (hrows 55) (fun i => Fin.elim0 i))))
def support323 : Finset (Fin 252) := {130, 148, 156, 166, 172, 183, 188, 190, 195, 202, 205, 210, 217, 221, 224, 234, 241}
theorem cut323 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support323, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 919, OmissionBalanced.support 980, OmissionBalanced.support 957] ![OmissionBalanced.demand 919, OmissionBalanced.demand 980, OmissionBalanced.demand 957] ![1, 1, 1]
    support323 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 919) (Fin.cases (hrows 980) (Fin.cases (hrows 957) (fun i => Fin.elim0 i))))
def support324 : Finset (Fin 252) := {186, 200, 205, 213, 217, 220, 226, 229, 231, 233, 234, 238, 240, 244, 248, 250}
theorem cut324 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support324, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1016, OmissionBalanced.support 1017, OmissionBalanced.support 180] ![OmissionBalanced.demand 1016, OmissionBalanced.demand 1017, OmissionBalanced.demand 180] ![1, 1, 1]
    support324 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1016) (Fin.cases (hrows 1017) (Fin.cases (hrows 180) (fun i => Fin.elim0 i))))
def support325 : Finset (Fin 252) := {186, 200, 205, 213, 217, 220, 226, 229, 231, 233, 234, 238, 240, 244, 248, 250, 251}
theorem cut325 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support325, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1016, OmissionBalanced.support 1017, OmissionBalanced.support 181] ![OmissionBalanced.demand 1016, OmissionBalanced.demand 1017, OmissionBalanced.demand 181] ![1, 1, 1]
    support325 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1016) (Fin.cases (hrows 1017) (Fin.cases (hrows 181) (fun i => Fin.elim0 i))))
#print axioms cut325
def support326 : Finset (Fin 252) := {186, 200, 205, 213, 217, 220, 224, 226, 229, 231, 234, 238, 240, 244, 246, 249, 250}
theorem cut326 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support326, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1014, OmissionBalanced.support 1015, OmissionBalanced.support 180] ![OmissionBalanced.demand 1014, OmissionBalanced.demand 1015, OmissionBalanced.demand 180] ![1, 1, 1]
    support326 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1014) (Fin.cases (hrows 1015) (Fin.cases (hrows 180) (fun i => Fin.elim0 i))))
def support327 : Finset (Fin 252) := {186, 200, 205, 213, 217, 220, 224, 226, 229, 231, 234, 238, 240, 244, 246, 249, 251}
theorem cut327 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support327, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1014, OmissionBalanced.support 1015, OmissionBalanced.support 181] ![OmissionBalanced.demand 1014, OmissionBalanced.demand 1015, OmissionBalanced.demand 181] ![1, 1, 1]
    support327 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1014) (Fin.cases (hrows 1015) (Fin.cases (hrows 181) (fun i => Fin.elim0 i))))
def support328 : Finset (Fin 252) := {112, 129, 138, 147, 166, 180, 183, 188, 197, 214, 218, 221, 224, 228, 236, 241}
theorem cut328 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support328, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 866, OmissionBalanced.support 864, OmissionBalanced.support 143] ![OmissionBalanced.demand 866, OmissionBalanced.demand 864, OmissionBalanced.demand 143] ![1, 1, 1]
    support328 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 866) (Fin.cases (hrows 864) (Fin.cases (hrows 143) (fun i => Fin.elim0 i))))
def support329 : Finset (Fin 252) := {3, 5, 10, 11, 13, 15, 17, 20, 22, 23, 25, 26, 31, 35, 36, 42, 43, 46, 48, 57, 61, 62, 77}
theorem cut329 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support329, holes i := by
  apply rounded_cover_cut ![support24, support169, OmissionBalanced.support 10] ![2, 2, OmissionBalanced.demand 10] ![1, 1, 1]
    support329 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut24 holes hbool hrows) (Fin.cases (cut169 holes hbool hrows) (Fin.cases (hrows 10) (fun i => Fin.elim0 i))))
def support330 : Finset (Fin 252) := {133, 150, 159, 167, 180, 197, 199, 209, 212, 219, 221, 224, 228, 232, 236, 241, 243, 246}
theorem cut330 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support330, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 935, OmissionBalanced.support 933, OmissionBalanced.support 2667] ![OmissionBalanced.demand 935, OmissionBalanced.demand 933, OmissionBalanced.demand 2667] ![1, 1, 1]
    support330 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 935) (Fin.cases (hrows 933) (Fin.cases (hrows 2667) (fun i => Fin.elim0 i))))
def support331 : Finset (Fin 252) := {4, 7, 12, 34, 37, 40, 46, 51, 53, 55, 60, 66, 70, 75, 91, 99, 117}
theorem cut331 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support331, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 227, OmissionBalanced.support 208, OmissionBalanced.support 204] ![OmissionBalanced.demand 227, OmissionBalanced.demand 208, OmissionBalanced.demand 204] ![1, 1, 1]
    support331 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 227) (Fin.cases (hrows 208) (Fin.cases (hrows 204) (fun i => Fin.elim0 i))))
def support332 : Finset (Fin 252) := {151, 168, 175, 184, 195, 199, 214, 223, 224, 226, 232, 233, 236, 243, 246, 247, 248, 250}
theorem cut332 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support332, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 972, OmissionBalanced.support 971, OmissionBalanced.support 2681] ![OmissionBalanced.demand 972, OmissionBalanced.demand 971, OmissionBalanced.demand 2681] ![1, 1, 1]
    support332 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 972) (Fin.cases (hrows 971) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support333 : Finset (Fin 252) := {151, 168, 175, 184, 195, 199, 214, 223, 224, 226, 232, 233, 236, 243, 246, 247, 248, 251}
theorem cut333 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support333, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 972, OmissionBalanced.support 971, OmissionBalanced.support 2682] ![OmissionBalanced.demand 972, OmissionBalanced.demand 971, OmissionBalanced.demand 2682] ![1, 1, 1]
    support333 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 972) (Fin.cases (hrows 971) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support334 : Finset (Fin 252) := {94, 111, 120, 137, 147, 158, 163, 166, 171, 176, 181, 188, 200, 205, 210, 216, 228}
theorem cut334 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support334, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 798, OmissionBalanced.support 894, OmissionBalanced.support 855] ![OmissionBalanced.demand 798, OmissionBalanced.demand 894, OmissionBalanced.demand 855] ![1, 1, 1]
    support334 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 798) (Fin.cases (hrows 894) (Fin.cases (hrows 855) (fun i => Fin.elim0 i))))
def support335 : Finset (Fin 252) := {6, 11, 18, 22, 31, 34, 36, 43, 46, 48, 61, 68, 79, 85, 103}
theorem cut335 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support335, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 261, OmissionBalanced.support 21, OmissionBalanced.support 224] ![OmissionBalanced.demand 261, OmissionBalanced.demand 21, OmissionBalanced.demand 224] ![1, 1, 1]
    support335 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 261) (Fin.cases (hrows 21) (Fin.cases (hrows 224) (fun i => Fin.elim0 i))))
def support336 : Finset (Fin 252) := {10, 17, 22, 27, 31, 34, 36, 43, 46, 48, 61, 68, 79, 85, 103}
theorem cut336 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support336, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 310, OmissionBalanced.support 38, OmissionBalanced.support 254] ![OmissionBalanced.demand 310, OmissionBalanced.demand 38, OmissionBalanced.demand 254] ![1, 1, 1]
    support336 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 310) (Fin.cases (hrows 38) (Fin.cases (hrows 254) (fun i => Fin.elim0 i))))
def support337 : Finset (Fin 252) := {148, 166, 172, 183, 190, 203, 205, 208, 215, 217, 220, 229, 233, 240, 245}
theorem cut337 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support337, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 958, OmissionBalanced.support 960, OmissionBalanced.support 166] ![OmissionBalanced.demand 958, OmissionBalanced.demand 960, OmissionBalanced.demand 166] ![1, 1, 1]
    support337 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 958) (Fin.cases (hrows 960) (Fin.cases (hrows 166) (fun i => Fin.elim0 i))))
def support338 : Finset (Fin 252) := {159, 174, 180, 189, 197, 209, 212, 215, 219, 221, 232, 234, 235, 241, 246}
theorem cut338 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support338, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 989, OmissionBalanced.support 2668, OmissionBalanced.support 985] ![OmissionBalanced.demand 989, OmissionBalanced.demand 2668, OmissionBalanced.demand 985] ![1, 1, 1]
    support338 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 989) (Fin.cases (hrows 2668) (Fin.cases (hrows 985) (fun i => Fin.elim0 i))))
def support339 : Finset (Fin 252) := {33, 43, 48, 56, 61, 67, 79, 85, 88, 93, 107, 112, 134, 142, 153, 169, 177, 191}
theorem cut339 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support339, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 497, OmissionBalanced.support 439, OmissionBalanced.support 542] ![OmissionBalanced.demand 497, OmissionBalanced.demand 439, OmissionBalanced.demand 542] ![1, 1, 1]
    support339 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 497) (Fin.cases (hrows 439) (Fin.cases (hrows 542) (fun i => Fin.elim0 i))))
def support340 : Finset (Fin 252) := {0, 4, 6, 8, 10, 15, 18, 22, 25, 27, 31, 37, 43, 68, 79, 85, 103}
theorem cut340 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support340, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 0, OmissionBalanced.support 254, OmissionBalanced.support 224] ![OmissionBalanced.demand 0, OmissionBalanced.demand 254, OmissionBalanced.demand 224] ![1, 1, 1]
    support340 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 0) (Fin.cases (hrows 254) (Fin.cases (hrows 224) (fun i => Fin.elim0 i))))
def support341 : Finset (Fin 252) := {1, 4, 6, 8, 10, 15, 18, 22, 25, 27, 31, 37, 43, 68, 79, 85, 103}
theorem cut341 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support341, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1029, OmissionBalanced.support 254, OmissionBalanced.support 224] ![OmissionBalanced.demand 1029, OmissionBalanced.demand 254, OmissionBalanced.demand 224] ![1, 1, 1]
    support341 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1029) (Fin.cases (hrows 254) (Fin.cases (hrows 224) (fun i => Fin.elim0 i))))
def support342 : Finset (Fin 252) := {122, 139, 144, 157, 173, 178, 181, 190, 203, 205, 209, 210, 216, 220, 228}
theorem cut342 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support342, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 900, OmissionBalanced.support 131, OmissionBalanced.support 2439] ![OmissionBalanced.demand 900, OmissionBalanced.demand 131, OmissionBalanced.demand 2439] ![1, 1, 1]
    support342 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 900) (Fin.cases (hrows 131) (Fin.cases (hrows 2439) (fun i => Fin.elim0 i))))
def support343 : Finset (Fin 252) := {159, 174, 180, 189, 197, 203, 209, 212, 219, 221, 226, 228, 232, 236, 243}
theorem cut343 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support343, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 987, OmissionBalanced.support 983, OmissionBalanced.support 2667] ![OmissionBalanced.demand 987, OmissionBalanced.demand 983, OmissionBalanced.demand 2667] ![1, 1, 1]
    support343 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 987) (Fin.cases (hrows 983) (Fin.cases (hrows 2667) (fun i => Fin.elim0 i))))
def support344 : Finset (Fin 252) := {141, 158, 163, 181, 189, 196, 198, 203, 219, 221, 226, 228, 232, 236, 243}
theorem cut344 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support344, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 954, OmissionBalanced.support 952, OmissionBalanced.support 2650] ![OmissionBalanced.demand 954, OmissionBalanced.demand 952, OmissionBalanced.demand 2650] ![1, 1, 1]
    support344 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 954) (Fin.cases (hrows 952) (Fin.cases (hrows 2650) (fun i => Fin.elim0 i))))
def support345 : Finset (Fin 252) := {150, 167, 174, 184, 194, 199, 203, 214, 218, 222, 224, 237, 238, 243, 246}
theorem cut345 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support345, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 968, OmissionBalanced.support 964, OmissionBalanced.support 2651] ![OmissionBalanced.demand 968, OmissionBalanced.demand 964, OmissionBalanced.demand 2651] ![1, 1, 1]
    support345 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 968) (Fin.cases (hrows 964) (Fin.cases (hrows 2651) (fun i => Fin.elim0 i))))
def support346 : Finset (Fin 252) := {32, 42, 47, 55, 58, 62, 73, 78, 80, 90, 97, 108, 112, 116, 151, 187}
theorem cut346 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support346, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 77, OmissionBalanced.support 88, OmissionBalanced.support 74] ![OmissionBalanced.demand 77, OmissionBalanced.demand 88, OmissionBalanced.demand 74] ![1, 1, 1]
    support346 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 77) (Fin.cases (hrows 88) (Fin.cases (hrows 74) (fun i => Fin.elim0 i))))
def support347 : Finset (Fin 252) := {5, 8, 10, 15, 17, 19, 23, 30, 32, 36, 39, 42, 54, 62, 71, 77, 92}
theorem cut347 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support347, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 216, OmissionBalanced.support 1090, OmissionBalanced.support 250] ![OmissionBalanced.demand 216, OmissionBalanced.demand 1090, OmissionBalanced.demand 250] ![1, 1, 1]
    support347 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 216) (Fin.cases (hrows 1090) (Fin.cases (hrows 250) (fun i => Fin.elim0 i))))
def support348 : Finset (Fin 252) := {5, 10, 16, 17, 19, 30, 32, 36, 39, 42, 54, 62, 71, 77, 92}
theorem cut348 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support348, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 216, OmissionBalanced.support 1063, OmissionBalanced.support 250] ![OmissionBalanced.demand 216, OmissionBalanced.demand 1063, OmissionBalanced.demand 250] ![1, 1, 1]
    support348 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 216) (Fin.cases (hrows 1063) (Fin.cases (hrows 250) (fun i => Fin.elim0 i))))
def support349 : Finset (Fin 252) := {8, 13, 19, 25, 29, 34, 35, 42, 46, 47, 53, 60, 70, 75, 91}
theorem cut349 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support349, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 236, OmissionBalanced.support 24, OmissionBalanced.support 266] ![OmissionBalanced.demand 236, OmissionBalanced.demand 24, OmissionBalanced.demand 266] ![1, 1, 1]
    support349 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 236) (Fin.cases (hrows 24) (Fin.cases (hrows 266) (fun i => Fin.elim0 i))))
def support350 : Finset (Fin 252) := {133, 150, 159, 167, 180, 184, 197, 209, 212, 214, 219, 221, 228, 232, 236, 243}
theorem cut350 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support350, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 931, OmissionBalanced.support 929, OmissionBalanced.support 2667] ![OmissionBalanced.demand 931, OmissionBalanced.demand 929, OmissionBalanced.demand 2667] ![1, 1, 1]
    support350 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 931) (Fin.cases (hrows 929) (Fin.cases (hrows 2667) (fun i => Fin.elim0 i))))
#print axioms cut350
def support351 : Finset (Fin 252) := {159, 174, 180, 189, 190, 203, 208, 212, 215, 226, 231, 232, 234, 238, 243, 246}
theorem cut351 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support351, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 987, OmissionBalanced.support 167, OmissionBalanced.support 989] ![OmissionBalanced.demand 987, OmissionBalanced.demand 167, OmissionBalanced.demand 989] ![1, 1, 1]
    support351 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 987) (Fin.cases (hrows 167) (Fin.cases (hrows 989) (fun i => Fin.elim0 i))))
def support352 : Finset (Fin 252) := {2, 4, 7, 12, 17, 25, 26, 29, 34, 35, 42, 46, 47, 53, 60, 70, 75, 91}
theorem cut352 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support352, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 7, OmissionBalanced.support 227, OmissionBalanced.support 206] ![OmissionBalanced.demand 7, OmissionBalanced.demand 227, OmissionBalanced.demand 206] ![1, 1, 1]
    support352 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 7) (Fin.cases (hrows 227) (Fin.cases (hrows 206) (fun i => Fin.elim0 i))))
def support353 : Finset (Fin 252) := {129, 147, 155, 166, 183, 188, 194, 209, 214, 218, 224, 228, 229, 236, 241}
theorem cut353 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support353, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 916, OmissionBalanced.support 143, OmissionBalanced.support 912] ![OmissionBalanced.demand 916, OmissionBalanced.demand 143, OmissionBalanced.demand 912] ![1, 1, 1]
    support353 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 916) (Fin.cases (hrows 143) (Fin.cases (hrows 912) (fun i => Fin.elim0 i))))
def support354 : Finset (Fin 252) := {4, 7, 14, 20, 21, 25, 29, 35, 40, 42, 47, 48, 60, 62, 78, 90, 112}
theorem cut354 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support354, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 45, OmissionBalanced.support 12, OmissionBalanced.support 60] ![OmissionBalanced.demand 45, OmissionBalanced.demand 12, OmissionBalanced.demand 60] ![1, 1, 1]
    support354 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 45) (Fin.cases (hrows 12) (Fin.cases (hrows 60) (fun i => Fin.elim0 i))))
def support355 : Finset (Fin 252) := {8, 15, 19, 23, 25, 32, 35, 41, 48, 53, 55, 62, 70, 88, 93, 110}
theorem cut355 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support355, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 238, OmissionBalanced.support 352, OmissionBalanced.support 28] ![OmissionBalanced.demand 238, OmissionBalanced.demand 352, OmissionBalanced.demand 28] ![1, 1, 1]
    support355 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 238) (Fin.cases (hrows 352) (Fin.cases (hrows 28) (fun i => Fin.elim0 i))))
def support356 : Finset (Fin 252) := {112, 129, 138, 147, 159, 166, 177, 183, 188, 206, 214, 218, 224, 226, 228, 234, 236, 241}
theorem cut356 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support356, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 860, OmissionBalanced.support 862, OmissionBalanced.support 143] ![OmissionBalanced.demand 860, OmissionBalanced.demand 862, OmissionBalanced.demand 143] ![1, 1, 1]
    support356 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 860) (Fin.cases (hrows 862) (Fin.cases (hrows 143) (fun i => Fin.elim0 i))))
def support357 : Finset (Fin 252) := {133, 150, 159, 167, 180, 184, 197, 199, 203, 214, 218, 221, 224, 236, 237, 241, 243, 246}
theorem cut357 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support357, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 933, OmissionBalanced.support 929, OmissionBalanced.support 2651] ![OmissionBalanced.demand 933, OmissionBalanced.demand 929, OmissionBalanced.demand 2651] ![1, 1, 1]
    support357 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 933) (Fin.cases (hrows 929) (Fin.cases (hrows 2651) (fun i => Fin.elim0 i))))
def support358 : Finset (Fin 252) := {16, 26, 31, 36, 38, 42, 46, 57, 60, 62, 68, 77, 96, 104, 122}
theorem cut358 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support358, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 379, OmissionBalanced.support 56, OmissionBalanced.support 304] ![OmissionBalanced.demand 379, OmissionBalanced.demand 56, OmissionBalanced.demand 304] ![1, 1, 1]
    support358 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 379) (Fin.cases (hrows 56) (Fin.cases (hrows 304) (fun i => Fin.elim0 i))))
def support359 : Finset (Fin 252) := {32, 42, 47, 55, 58, 62, 73, 78, 80, 90, 97, 108, 112, 116, 151, 170}
theorem cut359 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support359, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 77, OmissionBalanced.support 87, OmissionBalanced.support 74] ![OmissionBalanced.demand 77, OmissionBalanced.demand 87, OmissionBalanced.demand 74] ![1, 1, 1]
    support359 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 77) (Fin.cases (hrows 87) (Fin.cases (hrows 74) (fun i => Fin.elim0 i))))
def support360 : Finset (Fin 252) := {76, 81, 100, 121, 128, 135, 143, 147, 158, 167, 171, 174, 179, 189, 194, 207}
theorem cut360 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support360, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 700, OmissionBalanced.support 702, OmissionBalanced.support 93] ![OmissionBalanced.demand 700, OmissionBalanced.demand 702, OmissionBalanced.demand 93] ![1, 1, 1]
    support360 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 700) (Fin.cases (hrows 702) (Fin.cases (hrows 93) (fun i => Fin.elim0 i))))
def support361 : Finset (Fin 252) := {108, 127, 146, 156, 165, 175, 192, 206, 214, 224, 226, 233, 234, 236, 240, 243, 247, 250}
theorem cut361 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support361, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 846, OmissionBalanced.support 845, OmissionBalanced.support 2681] ![OmissionBalanced.demand 846, OmissionBalanced.demand 845, OmissionBalanced.demand 2681] ![1, 1, 1]
    support361 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 846) (Fin.cases (hrows 845) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support362 : Finset (Fin 252) := {108, 127, 146, 156, 165, 175, 192, 206, 214, 224, 226, 233, 234, 236, 240, 243, 247, 251}
theorem cut362 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support362, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 846, OmissionBalanced.support 845, OmissionBalanced.support 2682] ![OmissionBalanced.demand 846, OmissionBalanced.demand 845, OmissionBalanced.demand 2682] ![1, 1, 1]
    support362 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 846) (Fin.cases (hrows 845) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support363 : Finset (Fin 252) := {110, 128, 136, 157, 166, 173, 178, 191, 200, 203, 205, 209, 216, 220, 228}
theorem cut363 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support363, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 852, OmissionBalanced.support 131, OmissionBalanced.support 848] ![OmissionBalanced.demand 852, OmissionBalanced.demand 131, OmissionBalanced.demand 848] ![1, 1, 1]
    support363 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 852) (Fin.cases (hrows 131) (Fin.cases (hrows 848) (fun i => Fin.elim0 i))))
def support364 : Finset (Fin 252) := {115, 132, 141, 163, 167, 181, 184, 196, 198, 214, 219, 221, 228, 232, 236, 243}
theorem cut364 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support364, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 883, OmissionBalanced.support 881, OmissionBalanced.support 2650] ![OmissionBalanced.demand 883, OmissionBalanced.demand 881, OmissionBalanced.demand 2650] ![1, 1, 1]
    support364 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 883) (Fin.cases (hrows 881) (Fin.cases (hrows 2650) (fun i => Fin.elim0 i))))
def support365 : Finset (Fin 252) := {127, 146, 165, 172, 190, 205, 214, 217, 224, 226, 233, 234, 236, 240, 243, 247, 250}
theorem cut365 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support365, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 908, OmissionBalanced.support 907, OmissionBalanced.support 2681] ![OmissionBalanced.demand 908, OmissionBalanced.demand 907, OmissionBalanced.demand 2681] ![1, 1, 1]
    support365 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 908) (Fin.cases (hrows 907) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support366 : Finset (Fin 252) := {127, 146, 165, 172, 190, 205, 214, 217, 224, 226, 233, 234, 236, 240, 243, 247, 251}
theorem cut366 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support366, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 908, OmissionBalanced.support 907, OmissionBalanced.support 2682] ![OmissionBalanced.demand 908, OmissionBalanced.demand 907, OmissionBalanced.demand 2682] ![1, 1, 1]
    support366 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 908) (Fin.cases (hrows 907) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support367 : Finset (Fin 252) := {1, 7, 11, 14, 20, 23, 26, 31, 35, 40, 46, 51, 55, 67, 90, 102, 112, 138}
theorem cut367 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support367, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 277, OmissionBalanced.support 4, OmissionBalanced.support 348] ![OmissionBalanced.demand 277, OmissionBalanced.demand 4, OmissionBalanced.demand 348] ![1, 1, 1]
    support367 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 277) (Fin.cases (hrows 4) (Fin.cases (hrows 348) (fun i => Fin.elim0 i))))
def support368 : Finset (Fin 252) := {10, 15, 22, 23, 27, 33, 37, 42, 48, 52, 57, 67, 77, 84, 101}
theorem cut368 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support368, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1113, OmissionBalanced.support 255, OmissionBalanced.support 286] ![OmissionBalanced.demand 1113, OmissionBalanced.demand 255, OmissionBalanced.demand 286] ![1, 1, 1]
    support368 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1113) (Fin.cases (hrows 255) (Fin.cases (hrows 286) (fun i => Fin.elim0 i))))
def support369 : Finset (Fin 252) := {153, 169, 177, 185, 197, 200, 212, 213, 214, 216, 224, 228, 232, 237, 243, 246}
theorem cut369 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support369, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 977, OmissionBalanced.support 975, OmissionBalanced.support 2669] ![OmissionBalanced.demand 977, OmissionBalanced.demand 975, OmissionBalanced.demand 2669] ![1, 1, 1]
    support369 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 977) (Fin.cases (hrows 975) (Fin.cases (hrows 2669) (fun i => Fin.elim0 i))))
def support370 : Finset (Fin 252) := {153, 169, 177, 185, 197, 200, 212, 213, 214, 216, 224, 228, 232, 237, 243, 246, 247, 249}
theorem cut370 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support370, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 977, OmissionBalanced.support 975, OmissionBalanced.support 2670] ![OmissionBalanced.demand 977, OmissionBalanced.demand 975, OmissionBalanced.demand 2670] ![1, 1, 1]
    support370 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 977) (Fin.cases (hrows 975) (Fin.cases (hrows 2670) (fun i => Fin.elim0 i))))
def support371 : Finset (Fin 252) := {153, 169, 177, 185, 197, 200, 212, 213, 214, 216, 224, 228, 237, 239, 247, 249}
theorem cut371 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support371, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 978, OmissionBalanced.support 976, OmissionBalanced.support 2670] ![OmissionBalanced.demand 978, OmissionBalanced.demand 976, OmissionBalanced.demand 2670] ![1, 1, 1]
    support371 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 978) (Fin.cases (hrows 976) (Fin.cases (hrows 2670) (fun i => Fin.elim0 i))))
def support372 : Finset (Fin 252) := {153, 169, 177, 185, 197, 200, 212, 213, 214, 216, 224, 228, 237, 239, 243, 246, 247, 249}
theorem cut372 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support372, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 978, OmissionBalanced.support 976, OmissionBalanced.support 2669] ![OmissionBalanced.demand 978, OmissionBalanced.demand 976, OmissionBalanced.demand 2669] ![1, 1, 1]
    support372 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 978) (Fin.cases (hrows 976) (Fin.cases (hrows 2669) (fun i => Fin.elim0 i))))
def support373 : Finset (Fin 252) := {169, 185, 191, 200, 209, 213, 214, 216, 217, 222, 224, 226, 228, 229, 234, 237, 238, 240, 243, 244, 246, 247, 249, 251}
theorem cut373 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support373, holes i := by
  apply rounded_cover_cut ![support201, support204, OmissionBalanced.support 2669] ![3, 3, OmissionBalanced.demand 2669] ![1, 1, 1]
    support373 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut201 holes hbool hrows) (Fin.cases (cut204 holes hbool hrows) (Fin.cases (hrows 2669) (fun i => Fin.elim0 i))))
def support374 : Finset (Fin 252) := {169, 185, 191, 200, 209, 213, 214, 216, 217, 222, 224, 226, 228, 229, 234, 237, 238, 240, 243, 244, 246, 247, 249, 250}
theorem cut374 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support374, holes i := by
  apply rounded_cover_cut ![support203, support205, OmissionBalanced.support 2669] ![3, 3, OmissionBalanced.demand 2669] ![1, 1, 1]
    support374 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut203 holes hbool hrows) (Fin.cases (cut205 holes hbool hrows) (Fin.cases (hrows 2669) (fun i => Fin.elim0 i))))
def support375 : Finset (Fin 252) := {169, 185, 191, 200, 209, 213, 214, 216, 217, 222, 224, 226, 228, 229, 234, 237, 238, 240, 243, 244, 246, 247, 249, 250, 251}
theorem cut375 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support375, holes i := by
  apply rounded_cover_cut ![support201, support205, OmissionBalanced.support 2669] ![3, 3, OmissionBalanced.demand 2669] ![1, 1, 1]
    support375 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut201 holes hbool hrows) (Fin.cases (cut205 holes hbool hrows) (Fin.cases (hrows 2669) (fun i => Fin.elim0 i))))
#print axioms cut375
def support376 : Finset (Fin 252) := {10, 15, 17, 23, 25, 27, 33, 34, 37, 60, 63, 68, 77, 85, 96, 104, 122}
theorem cut376 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support376, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 312, OmissionBalanced.support 371, OmissionBalanced.support 36] ![OmissionBalanced.demand 312, OmissionBalanced.demand 371, OmissionBalanced.demand 36] ![1, 1, 1]
    support376 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 312) (Fin.cases (hrows 371) (Fin.cases (hrows 36) (fun i => Fin.elim0 i))))
def support377 : Finset (Fin 252) := {10, 15, 17, 23, 25, 27, 33, 37, 45, 63, 68, 74, 85, 92, 104, 113, 122, 139}
theorem cut377 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support377, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 316, OmissionBalanced.support 375, OmissionBalanced.support 36] ![OmissionBalanced.demand 316, OmissionBalanced.demand 375, OmissionBalanced.demand 36] ![1, 1, 1]
    support377 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 316) (Fin.cases (hrows 375) (Fin.cases (hrows 36) (fun i => Fin.elim0 i))))
def support378 : Finset (Fin 252) := {5, 8, 14, 19, 23, 27, 35, 37, 38, 39, 51, 54, 66, 74, 82, 98}
theorem cut378 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support378, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1060, OmissionBalanced.support 219, OmissionBalanced.support 239] ![OmissionBalanced.demand 1060, OmissionBalanced.demand 219, OmissionBalanced.demand 239] ![1, 1, 1]
    support378 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1060) (Fin.cases (hrows 219) (Fin.cases (hrows 239) (fun i => Fin.elim0 i))))
def support379 : Finset (Fin 252) := {2, 4, 12, 14, 23, 27, 35, 37, 38, 39, 51, 54, 66, 74, 82, 98}
theorem cut379 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support379, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1035, OmissionBalanced.support 196, OmissionBalanced.support 207] ![OmissionBalanced.demand 1035, OmissionBalanced.demand 196, OmissionBalanced.demand 207] ![1, 1, 1]
    support379 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1035) (Fin.cases (hrows 196) (Fin.cases (hrows 207) (fun i => Fin.elim0 i))))
def support380 : Finset (Fin 252) := {6, 10, 11, 17, 22, 27, 31, 34, 36, 43, 46, 48, 61, 68, 79, 85, 103}
theorem cut380 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support380, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 310, OmissionBalanced.support 21, OmissionBalanced.support 254] ![OmissionBalanced.demand 310, OmissionBalanced.demand 21, OmissionBalanced.demand 254] ![1, 1, 1]
    support380 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 310) (Fin.cases (hrows 21) (Fin.cases (hrows 254) (fun i => Fin.elim0 i))))
def support381 : Finset (Fin 252) := {2, 4, 7, 14, 23, 27, 29, 35, 37, 38, 42, 51, 60, 66, 82}
theorem cut381 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support381, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1035, OmissionBalanced.support 192, OmissionBalanced.support 203] ![OmissionBalanced.demand 1035, OmissionBalanced.demand 192, OmissionBalanced.demand 203] ![1, 1, 1]
    support381 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1035) (Fin.cases (hrows 192) (Fin.cases (hrows 203) (fun i => Fin.elim0 i))))
def support382 : Finset (Fin 252) := {158, 179, 189, 191, 203, 204, 209, 211, 216, 222, 226, 231, 237, 238, 243}
theorem cut382 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support382, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 169, OmissionBalanced.support 138, OmissionBalanced.support 137] ![OmissionBalanced.demand 169, OmissionBalanced.demand 138, OmissionBalanced.demand 137] ![1, 1, 1]
    support382 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 169) (Fin.cases (hrows 138) (Fin.cases (hrows 137) (fun i => Fin.elim0 i))))
def support383 : Finset (Fin 252) := {4, 7, 14, 20, 25, 32, 35, 40, 42, 47, 48, 55, 62, 75, 78, 90, 112}
theorem cut383 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support383, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 45, OmissionBalanced.support 13, OmissionBalanced.support 74] ![OmissionBalanced.demand 45, OmissionBalanced.demand 13, OmissionBalanced.demand 74] ![1, 1, 1]
    support383 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 45) (Fin.cases (hrows 13) (Fin.cases (hrows 74) (fun i => Fin.elim0 i))))
def support384 : Finset (Fin 252) := {99, 117, 135, 162, 180, 188, 190, 195, 202, 203, 208, 215, 218, 227, 231, 238, 240, 248}
theorem cut384 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support384, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 168, OmissionBalanced.support 821, OmissionBalanced.support 820] ![OmissionBalanced.demand 168, OmissionBalanced.demand 821, OmissionBalanced.demand 820] ![1, 1, 1]
    support384 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 168) (Fin.cases (hrows 821) (Fin.cases (hrows 820) (fun i => Fin.elim0 i))))
def support385 : Finset (Fin 252) := {186, 200, 205, 213, 214, 220, 224, 226, 231, 233, 236, 238, 243, 244, 246, 247, 250}
theorem cut385 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support385, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1017, OmissionBalanced.support 1014, OmissionBalanced.support 2681] ![OmissionBalanced.demand 1017, OmissionBalanced.demand 1014, OmissionBalanced.demand 2681] ![1, 1, 1]
    support385 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1017) (Fin.cases (hrows 1014) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support386 : Finset (Fin 252) := {186, 200, 205, 213, 214, 220, 224, 226, 231, 233, 236, 238, 243, 244, 247, 248, 249, 250}
theorem cut386 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support386, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1016, OmissionBalanced.support 1015, OmissionBalanced.support 2681] ![OmissionBalanced.demand 1016, OmissionBalanced.demand 1015, OmissionBalanced.demand 2681] ![1, 1, 1]
    support386 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1016) (Fin.cases (hrows 1015) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support387 : Finset (Fin 252) := {186, 200, 205, 213, 214, 220, 224, 226, 231, 233, 236, 238, 243, 244, 247, 248, 249, 251}
theorem cut387 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support387, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1016, OmissionBalanced.support 1015, OmissionBalanced.support 2682] ![OmissionBalanced.demand 1016, OmissionBalanced.demand 1015, OmissionBalanced.demand 2682] ![1, 1, 1]
    support387 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1016) (Fin.cases (hrows 1015) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support388 : Finset (Fin 252) := {186, 200, 205, 213, 214, 220, 224, 226, 231, 233, 236, 238, 243, 244, 246, 247, 250, 251}
theorem cut388 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support388, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1017, OmissionBalanced.support 1014, OmissionBalanced.support 2682] ![OmissionBalanced.demand 1017, OmissionBalanced.demand 1014, OmissionBalanced.demand 2682] ![1, 1, 1]
    support388 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1017) (Fin.cases (hrows 1014) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support389 : Finset (Fin 252) := {130, 148, 156, 166, 175, 183, 192, 206, 214, 224, 226, 233, 234, 236, 240, 243, 247, 250}
theorem cut389 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support389, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 918, OmissionBalanced.support 917, OmissionBalanced.support 2681] ![OmissionBalanced.demand 918, OmissionBalanced.demand 917, OmissionBalanced.demand 2681] ![1, 1, 1]
    support389 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 918) (Fin.cases (hrows 917) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support390 : Finset (Fin 252) := {130, 148, 156, 166, 175, 183, 192, 206, 214, 224, 226, 233, 234, 236, 240, 243, 247, 251}
theorem cut390 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support390, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 918, OmissionBalanced.support 917, OmissionBalanced.support 2682] ![OmissionBalanced.demand 918, OmissionBalanced.demand 917, OmissionBalanced.demand 2682] ![1, 1, 1]
    support390 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 918) (Fin.cases (hrows 917) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
def support391 : Finset (Fin 252) := {2, 7, 17, 26, 29, 32, 42, 47, 54, 60, 70, 80, 96, 97, 115, 127, 151, 168}
theorem cut391 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support391, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 7, OmissionBalanced.support 484, OmissionBalanced.support 423] ![OmissionBalanced.demand 7, OmissionBalanced.demand 484, OmissionBalanced.demand 423] ![1, 1, 1]
    support391 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 7) (Fin.cases (hrows 484) (Fin.cases (hrows 423) (fun i => Fin.elim0 i))))
def support392 : Finset (Fin 252) := {4, 7, 25, 29, 32, 35, 42, 47, 54, 60, 70, 80, 96, 97, 115, 127, 151, 168}
theorem cut392 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support392, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 12, OmissionBalanced.support 484, OmissionBalanced.support 423] ![OmissionBalanced.demand 12, OmissionBalanced.demand 484, OmissionBalanced.demand 423] ![1, 1, 1]
    support392 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 12) (Fin.cases (hrows 484) (Fin.cases (hrows 423) (fun i => Fin.elim0 i))))
def support393 : Finset (Fin 252) := {100, 101, 118, 136, 143, 144, 154, 155, 171, 181, 191, 196, 197, 204, 209, 219}
theorem cut393 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support393, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 823, OmissionBalanced.support 828, OmissionBalanced.support 98] ![OmissionBalanced.demand 823, OmissionBalanced.demand 828, OmissionBalanced.demand 98] ![1, 1, 1]
    support393 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 823) (Fin.cases (hrows 828) (Fin.cases (hrows 98) (fun i => Fin.elim0 i))))
def support394 : Finset (Fin 252) := {23, 31, 35, 42, 46, 48, 51, 60, 73, 78, 85, 94, 115, 123, 141}
theorem cut394 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support394, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 346, OmissionBalanced.support 1470, OmissionBalanced.support 64] ![OmissionBalanced.demand 346, OmissionBalanced.demand 1470, OmissionBalanced.demand 64] ![1, 1, 1]
    support394 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 346) (Fin.cases (hrows 1470) (Fin.cases (hrows 64) (fun i => Fin.elim0 i))))
def support395 : Finset (Fin 252) := {1, 7, 9, 11, 16, 20, 26, 29, 31, 35, 38, 42, 46, 52, 73, 94, 102, 120}
theorem cut395 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support395, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 244, OmissionBalanced.support 303, OmissionBalanced.support 4] ![OmissionBalanced.demand 244, OmissionBalanced.demand 303, OmissionBalanced.demand 4] ![1, 1, 1]
    support395 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 244) (Fin.cases (hrows 303) (Fin.cases (hrows 4) (fun i => Fin.elim0 i))))
def support396 : Finset (Fin 252) := {1, 7, 11, 14, 20, 23, 26, 29, 31, 35, 42, 46, 51, 67, 73, 94, 102, 120}
theorem cut396 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support396, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 275, OmissionBalanced.support 345, OmissionBalanced.support 4] ![OmissionBalanced.demand 275, OmissionBalanced.demand 345, OmissionBalanced.demand 4] ![1, 1, 1]
    support396 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 275) (Fin.cases (hrows 345) (Fin.cases (hrows 4) (fun i => Fin.elim0 i))))
def support397 : Finset (Fin 252) := {5, 8, 10, 14, 15, 22, 27, 33, 37, 42, 48, 52, 57, 67, 77, 84, 101}
theorem cut397 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support397, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 15, OmissionBalanced.support 255, OmissionBalanced.support 286] ![OmissionBalanced.demand 15, OmissionBalanced.demand 255, OmissionBalanced.demand 286] ![1, 1, 1]
    support397 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 15) (Fin.cases (hrows 255) (Fin.cases (hrows 286) (fun i => Fin.elim0 i))))
def support398 : Finset (Fin 252) := {159, 174, 180, 189, 197, 209, 212, 215, 219, 221, 228, 232, 234, 236, 241, 243, 246}
theorem cut398 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support398, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 989, OmissionBalanced.support 985, OmissionBalanced.support 2667] ![OmissionBalanced.demand 989, OmissionBalanced.demand 985, OmissionBalanced.demand 2667] ![1, 1, 1]
    support398 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 989) (Fin.cases (hrows 985) (Fin.cases (hrows 2667) (fun i => Fin.elim0 i))))
def support399 : Finset (Fin 252) := {148, 166, 172, 183, 190, 205, 214, 217, 224, 226, 233, 234, 236, 240, 243, 247, 250}
theorem cut399 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support399, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 958, OmissionBalanced.support 957, OmissionBalanced.support 2681] ![OmissionBalanced.demand 958, OmissionBalanced.demand 957, OmissionBalanced.demand 2681] ![1, 1, 1]
    support399 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 958) (Fin.cases (hrows 957) (Fin.cases (hrows 2681) (fun i => Fin.elim0 i))))
def support400 : Finset (Fin 252) := {148, 166, 172, 183, 190, 205, 214, 217, 224, 226, 233, 234, 236, 240, 243, 247, 251}
theorem cut400 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support400, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 958, OmissionBalanced.support 957, OmissionBalanced.support 2682] ![OmissionBalanced.demand 958, OmissionBalanced.demand 957, OmissionBalanced.demand 2682] ![1, 1, 1]
    support400 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 958) (Fin.cases (hrows 957) (Fin.cases (hrows 2682) (fun i => Fin.elim0 i))))
#print axioms cut400
def support401 : Finset (Fin 252) := {2, 4, 5, 8, 12, 14, 23, 27, 35, 37, 38, 39, 51, 54, 66, 74, 82, 98}
theorem cut401 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support401, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1060, OmissionBalanced.support 196, OmissionBalanced.support 207] ![OmissionBalanced.demand 1060, OmissionBalanced.demand 196, OmissionBalanced.demand 207] ![1, 1, 1]
    support401 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1060) (Fin.cases (hrows 196) (Fin.cases (hrows 207) (fun i => Fin.elim0 i))))
def support402 : Finset (Fin 252) := {2, 4, 5, 8, 14, 19, 23, 27, 35, 37, 38, 39, 51, 54, 66, 74, 82, 98}
theorem cut402 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support402, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1035, OmissionBalanced.support 219, OmissionBalanced.support 239] ![OmissionBalanced.demand 1035, OmissionBalanced.demand 219, OmissionBalanced.demand 239] ![1, 1, 1]
    support402 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1035) (Fin.cases (hrows 219) (Fin.cases (hrows 239) (fun i => Fin.elim0 i))))
def support403 : Finset (Fin 252) := {5, 8, 10, 13, 17, 22, 23, 25, 29, 31, 35, 36, 42, 43, 47, 48, 57, 60, 61, 62, 77}
theorem cut403 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support403, holes i := by
  apply rounded_cover_cut ![support24, OmissionBalanced.support 24, support168] ![2, OmissionBalanced.demand 24, 2] ![1, 1, 1]
    support403 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut24 holes hbool hrows) (Fin.cases (hrows 24) (Fin.cases (cut168 holes hbool hrows) (fun i => Fin.elim0 i))))
def support404 : Finset (Fin 252) := {6, 10, 11, 17, 18, 22, 31, 34, 36, 43, 46, 48, 61, 68, 79, 85, 103}
theorem cut404 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support404, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 261, OmissionBalanced.support 38, OmissionBalanced.support 224] ![OmissionBalanced.demand 261, OmissionBalanced.demand 38, OmissionBalanced.demand 224] ![1, 1, 1]
    support404 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 261) (Fin.cases (hrows 38) (Fin.cases (hrows 224) (fun i => Fin.elim0 i))))
def support405 : Finset (Fin 252) := {2, 7, 17, 21, 26, 29, 32, 40, 42, 47, 55, 60, 66, 84, 102, 108, 130, 156}
theorem cut405 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support405, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 417, OmissionBalanced.support 7, OmissionBalanced.support 330] ![OmissionBalanced.demand 417, OmissionBalanced.demand 7, OmissionBalanced.demand 330] ![1, 1, 1]
    support405 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 417) (Fin.cases (hrows 7) (Fin.cases (hrows 330) (fun i => Fin.elim0 i))))
def support406 : Finset (Fin 252) := {16, 26, 38, 41, 46, 49, 54, 60, 68, 71, 77, 80, 96, 104, 113, 122, 139}
theorem cut406 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support406, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 300, OmissionBalanced.support 308, OmissionBalanced.support 379] ![OmissionBalanced.demand 300, OmissionBalanced.demand 308, OmissionBalanced.demand 379] ![1, 1, 1]
    support406 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 300) (Fin.cases (hrows 308) (Fin.cases (hrows 379) (fun i => Fin.elim0 i))))
def support407 : Finset (Fin 252) := {1, 7, 11, 14, 20, 23, 26, 31, 35, 40, 46, 51, 55, 67, 72, 84, 93, 119}
theorem cut407 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support407, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 276, OmissionBalanced.support 4, OmissionBalanced.support 347] ![OmissionBalanced.demand 276, OmissionBalanced.demand 4, OmissionBalanced.demand 347] ![1, 1, 1]
    support407 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 276) (Fin.cases (hrows 4) (Fin.cases (hrows 347) (fun i => Fin.elim0 i))))
def support408 : Finset (Fin 252) := {32, 42, 47, 54, 55, 60, 70, 80, 96, 97, 107, 108, 115, 133, 150, 151}
theorem cut408 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support408, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 77, OmissionBalanced.support 422, OmissionBalanced.support 483] ![OmissionBalanced.demand 77, OmissionBalanced.demand 422, OmissionBalanced.demand 483] ![1, 1, 1]
    support408 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 77) (Fin.cases (hrows 422) (Fin.cases (hrows 483) (fun i => Fin.elim0 i))))
def support409 : Finset (Fin 252) := {10, 17, 27, 30, 34, 49, 54, 60, 68, 71, 77, 80, 96, 104, 113, 122, 139}
theorem cut409 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support409, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 260, OmissionBalanced.support 252, OmissionBalanced.support 312] ![OmissionBalanced.demand 260, OmissionBalanced.demand 252, OmissionBalanced.demand 312] ![1, 1, 1]
    support409 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 260) (Fin.cases (hrows 252) (Fin.cases (hrows 312) (fun i => Fin.elim0 i))))
def support410 : Finset (Fin 252) := {2, 7, 17, 21, 26, 29, 32, 40, 42, 47, 55, 60, 66, 84, 90, 102, 112, 138}
theorem cut410 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support410, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 7, OmissionBalanced.support 416, OmissionBalanced.support 329] ![OmissionBalanced.demand 7, OmissionBalanced.demand 416, OmissionBalanced.demand 329] ![1, 1, 1]
    support410 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 7) (Fin.cases (hrows 416) (Fin.cases (hrows 329) (fun i => Fin.elim0 i))))
def support411 : Finset (Fin 252) := {14, 20, 33, 35, 40, 43, 48, 56, 61, 67, 72, 78, 79, 85, 88, 90, 93, 107, 112, 134, 142, 153, 169, 177, 191}
theorem cut411 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    5 ≤ ∑ i ∈ support411, holes i := by
  apply rounded_cover_cut ![support267, OmissionBalanced.support 45, support339] ![4, OmissionBalanced.demand 45, 4] ![1, 1, 1]
    support411 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (cut267 holes hbool hrows) (Fin.cases (hrows 45) (Fin.cases (cut339 holes hbool hrows) (fun i => Fin.elim0 i))))
def support412 : Finset (Fin 252) := {174, 189, 190, 194, 203, 208, 215, 222, 225, 226, 231, 238, 240, 242, 243, 248}
theorem cut412 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support412, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 168, OmissionBalanced.support 156, OmissionBalanced.support 153] ![OmissionBalanced.demand 168, OmissionBalanced.demand 156, OmissionBalanced.demand 153] ![1, 1, 1]
    support412 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 168) (Fin.cases (hrows 156) (Fin.cases (hrows 153) (fun i => Fin.elim0 i))))
def support413 : Finset (Fin 252) := {155, 171, 172, 188, 194, 202, 208, 209, 220, 225, 226, 229, 235, 236, 240, 245}
theorem cut413 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support413, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 128, OmissionBalanced.support 129, OmissionBalanced.support 149] ![OmissionBalanced.demand 128, OmissionBalanced.demand 129, OmissionBalanced.demand 149] ![1, 1, 1]
    support413 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 128) (Fin.cases (hrows 129) (Fin.cases (hrows 149) (fun i => Fin.elim0 i))))
def support414 : Finset (Fin 252) := {116, 134, 142, 153, 164, 170, 182, 187, 221, 229, 232, 236, 239, 241, 245, 250}
theorem cut414 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support414, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 884, OmissionBalanced.support 885, OmissionBalanced.support 2683] ![OmissionBalanced.demand 884, OmissionBalanced.demand 885, OmissionBalanced.demand 2683] ![1, 1, 1]
    support414 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 884) (Fin.cases (hrows 885) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support415 : Finset (Fin 252) := {170, 186, 192, 200, 210, 213, 221, 223, 229, 232, 233, 236, 239, 241, 245, 248, 250}
theorem cut415 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support415, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1005, OmissionBalanced.support 1004, OmissionBalanced.support 2683] ![OmissionBalanced.demand 1005, OmissionBalanced.demand 1004, OmissionBalanced.demand 2683] ![1, 1, 1]
    support415 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1005) (Fin.cases (hrows 1004) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support416 : Finset (Fin 252) := {170, 186, 192, 200, 210, 213, 221, 223, 229, 232, 233, 236, 239, 241, 245, 248, 250, 251}
theorem cut416 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support416, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1005, OmissionBalanced.support 1004, OmissionBalanced.support 2684] ![OmissionBalanced.demand 1005, OmissionBalanced.demand 1004, OmissionBalanced.demand 2684] ![1, 1, 1]
    support416 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1005) (Fin.cases (hrows 1004) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support417 : Finset (Fin 252) := {116, 134, 142, 153, 164, 170, 182, 187, 221, 229, 232, 236, 239, 241, 245, 251}
theorem cut417 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support417, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 884, OmissionBalanced.support 885, OmissionBalanced.support 2684] ![OmissionBalanced.demand 884, OmissionBalanced.demand 885, OmissionBalanced.demand 2684] ![1, 1, 1]
    support417 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 884) (Fin.cases (hrows 885) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support418 : Finset (Fin 252) := {153, 169, 177, 185, 197, 212, 213, 221, 224, 229, 232, 236, 239, 241, 245, 246, 249, 250}
theorem cut418 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support418, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 977, OmissionBalanced.support 978, OmissionBalanced.support 2683] ![OmissionBalanced.demand 977, OmissionBalanced.demand 978, OmissionBalanced.demand 2683] ![1, 1, 1]
    support418 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 977) (Fin.cases (hrows 978) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support419 : Finset (Fin 252) := {153, 169, 177, 185, 197, 212, 213, 221, 224, 229, 232, 236, 239, 241, 245, 246, 249, 251}
theorem cut419 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support419, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 977, OmissionBalanced.support 978, OmissionBalanced.support 2684] ![OmissionBalanced.demand 977, OmissionBalanced.demand 978, OmissionBalanced.demand 2684] ![1, 1, 1]
    support419 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 977) (Fin.cases (hrows 978) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support420 : Finset (Fin 252) := {170, 186, 192, 200, 210, 213, 221, 223, 224, 229, 232, 236, 239, 241, 245, 246, 249, 250}
theorem cut420 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support420, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1002, OmissionBalanced.support 1003, OmissionBalanced.support 2683] ![OmissionBalanced.demand 1002, OmissionBalanced.demand 1003, OmissionBalanced.demand 2683] ![1, 1, 1]
    support420 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1002) (Fin.cases (hrows 1003) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support421 : Finset (Fin 252) := {170, 186, 192, 200, 210, 213, 221, 223, 224, 229, 232, 236, 239, 241, 245, 246, 249, 251}
theorem cut421 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support421, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1002, OmissionBalanced.support 1003, OmissionBalanced.support 2684] ![OmissionBalanced.demand 1002, OmissionBalanced.demand 1003, OmissionBalanced.demand 2684] ![1, 1, 1]
    support421 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1002) (Fin.cases (hrows 1003) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support422 : Finset (Fin 252) := {153, 169, 177, 185, 197, 200, 212, 214, 221, 229, 232, 236, 239, 241, 243, 245, 247, 250}
theorem cut422 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support422, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 976, OmissionBalanced.support 975, OmissionBalanced.support 2683] ![OmissionBalanced.demand 976, OmissionBalanced.demand 975, OmissionBalanced.demand 2683] ![1, 1, 1]
    support422 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 976) (Fin.cases (hrows 975) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support423 : Finset (Fin 252) := {153, 169, 177, 185, 197, 200, 212, 214, 221, 229, 232, 236, 239, 241, 243, 245, 247, 251}
theorem cut423 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support423, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 976, OmissionBalanced.support 975, OmissionBalanced.support 2684] ![OmissionBalanced.demand 976, OmissionBalanced.demand 975, OmissionBalanced.demand 2684] ![1, 1, 1]
    support423 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 976) (Fin.cases (hrows 975) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support424 : Finset (Fin 252) := {177, 191, 197, 204, 212, 221, 225, 229, 232, 234, 236, 239, 241, 245, 246, 249, 250}
theorem cut424 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support424, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1012, OmissionBalanced.support 1013, OmissionBalanced.support 2683] ![OmissionBalanced.demand 1012, OmissionBalanced.demand 1013, OmissionBalanced.demand 2683] ![1, 1, 1]
    support424 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1012) (Fin.cases (hrows 1013) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support425 : Finset (Fin 252) := {177, 191, 197, 204, 212, 221, 225, 229, 232, 234, 236, 239, 241, 245, 246, 249, 251}
theorem cut425 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support425, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1012, OmissionBalanced.support 1013, OmissionBalanced.support 2684] ![OmissionBalanced.demand 1012, OmissionBalanced.demand 1013, OmissionBalanced.demand 2684] ![1, 1, 1]
    support425 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1012) (Fin.cases (hrows 1013) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
#print axioms cut425
def support426 : Finset (Fin 252) := {153, 169, 177, 185, 197, 200, 212, 213, 214, 216, 221, 224, 228, 229, 232, 236, 237, 239, 241, 243, 245, 246, 247, 249, 250}
theorem cut426 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    5 ≤ ∑ i ∈ support426, holes i := by
  apply rounded_cover_cut ![support371, support369, OmissionBalanced.support 2683] ![4, 4, OmissionBalanced.demand 2683] ![1, 1, 1]
    support426 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (cut371 holes hbool hrows) (Fin.cases (cut369 holes hbool hrows) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support427 : Finset (Fin 252) := {153, 169, 177, 185, 197, 200, 212, 213, 214, 216, 221, 224, 228, 229, 232, 236, 237, 239, 241, 243, 245, 246, 247, 249, 251}
theorem cut427 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    5 ≤ ∑ i ∈ support427, holes i := by
  apply rounded_cover_cut ![support371, support369, OmissionBalanced.support 2684] ![4, 4, OmissionBalanced.demand 2684] ![1, 1, 1]
    support427 2 5 (by decide +kernel) holes hbool
  exact (Fin.cases (cut371 holes hbool hrows) (Fin.cases (cut369 holes hbool hrows) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support428 : Finset (Fin 252) := {134, 152, 160, 181, 185, 198, 200, 214, 221, 229, 232, 236, 239, 241, 243, 245, 247, 250}
theorem cut428 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support428, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 939, OmissionBalanced.support 938, OmissionBalanced.support 2683] ![OmissionBalanced.demand 939, OmissionBalanced.demand 938, OmissionBalanced.demand 2683] ![1, 1, 1]
    support428 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 939) (Fin.cases (hrows 938) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support429 : Finset (Fin 252) := {134, 152, 160, 181, 185, 198, 200, 214, 221, 229, 232, 236, 239, 241, 243, 245, 247, 251}
theorem cut429 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support429, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 939, OmissionBalanced.support 938, OmissionBalanced.support 2684] ![OmissionBalanced.demand 939, OmissionBalanced.demand 938, OmissionBalanced.demand 2684] ![1, 1, 1]
    support429 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 939) (Fin.cases (hrows 938) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support430 : Finset (Fin 252) := {177, 191, 197, 204, 205, 212, 216, 220, 221, 225, 226, 229, 231, 232, 234, 236, 239, 241, 243, 244, 245, 246, 247, 249, 250}
theorem cut430 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support430, holes i := by
  apply rounded_cover_cut ![support141, support142, OmissionBalanced.support 2683] ![3, 3, OmissionBalanced.demand 2683] ![1, 1, 1]
    support430 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut141 holes hbool hrows) (Fin.cases (cut142 holes hbool hrows) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support431 : Finset (Fin 252) := {177, 191, 197, 204, 205, 212, 216, 220, 221, 225, 226, 229, 231, 232, 234, 236, 239, 241, 243, 244, 245, 246, 247, 249, 251}
theorem cut431 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support431, holes i := by
  apply rounded_cover_cut ![support141, support142, OmissionBalanced.support 2684] ![3, 3, OmissionBalanced.demand 2684] ![1, 1, 1]
    support431 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut141 holes hbool hrows) (Fin.cases (cut142 holes hbool hrows) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support432 : Finset (Fin 252) := {177, 191, 197, 204, 205, 212, 216, 220, 221, 225, 226, 229, 231, 232, 234, 236, 238, 239, 241, 243, 245, 246, 247, 249, 250}
theorem cut432 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support432, holes i := by
  apply rounded_cover_cut ![support147, support145, OmissionBalanced.support 2683] ![3, 3, OmissionBalanced.demand 2683] ![1, 1, 1]
    support432 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut147 holes hbool hrows) (Fin.cases (cut145 holes hbool hrows) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support433 : Finset (Fin 252) := {177, 191, 197, 204, 205, 212, 216, 220, 221, 225, 226, 229, 231, 232, 234, 236, 238, 239, 241, 243, 245, 246, 247, 249, 251}
theorem cut433 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support433, holes i := by
  apply rounded_cover_cut ![support147, support145, OmissionBalanced.support 2684] ![3, 3, OmissionBalanced.demand 2684] ![1, 1, 1]
    support433 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (cut147 holes hbool hrows) (Fin.cases (cut145 holes hbool hrows) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support434 : Finset (Fin 252) := {177, 191, 197, 204, 212, 216, 221, 226, 229, 232, 236, 239, 241, 243, 245, 247, 250}
theorem cut434 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support434, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1011, OmissionBalanced.support 1010, OmissionBalanced.support 2683] ![OmissionBalanced.demand 1011, OmissionBalanced.demand 1010, OmissionBalanced.demand 2683] ![1, 1, 1]
    support434 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1011) (Fin.cases (hrows 1010) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support435 : Finset (Fin 252) := {177, 191, 197, 204, 212, 216, 221, 226, 229, 232, 236, 239, 241, 243, 245, 247, 251}
theorem cut435 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support435, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1011, OmissionBalanced.support 1010, OmissionBalanced.support 2684] ![OmissionBalanced.demand 1011, OmissionBalanced.demand 1010, OmissionBalanced.demand 2684] ![1, 1, 1]
    support435 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1011) (Fin.cases (hrows 1010) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support436 : Finset (Fin 252) := {160, 176, 181, 198, 204, 216, 221, 226, 229, 232, 236, 239, 241, 243, 245, 247, 250}
theorem cut436 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support436, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 993, OmissionBalanced.support 992, OmissionBalanced.support 2683] ![OmissionBalanced.demand 993, OmissionBalanced.demand 992, OmissionBalanced.demand 2683] ![1, 1, 1]
    support436 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 993) (Fin.cases (hrows 992) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support437 : Finset (Fin 252) := {160, 176, 181, 198, 204, 216, 221, 226, 229, 232, 236, 239, 241, 243, 245, 247, 251}
theorem cut437 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support437, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 993, OmissionBalanced.support 992, OmissionBalanced.support 2684] ![OmissionBalanced.demand 993, OmissionBalanced.demand 992, OmissionBalanced.demand 2684] ![1, 1, 1]
    support437 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 993) (Fin.cases (hrows 992) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support438 : Finset (Fin 252) := {174, 189, 190, 191, 194, 203, 204, 208, 209, 215, 216, 222, 226, 229, 231, 234, 236, 237, 238, 241, 244, 246, 247}
theorem cut438 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support438, holes i := by
  apply rounded_cover_cut ![support26, support170, OmissionBalanced.support 170] ![2, 2, OmissionBalanced.demand 170] ![1, 1, 1]
    support438 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (cut26 holes hbool hrows) (Fin.cases (cut170 holes hbool hrows) (Fin.cases (hrows 170) (fun i => Fin.elim0 i))))
def support439 : Finset (Fin 252) := {158, 176, 179, 189, 196, 203, 204, 211, 216, 226, 229, 231, 236, 237, 244, 247}
theorem cut439 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support439, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 159, OmissionBalanced.support 136, OmissionBalanced.support 137] ![OmissionBalanced.demand 159, OmissionBalanced.demand 136, OmissionBalanced.demand 137] ![1, 1, 1]
    support439 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 159) (Fin.cases (hrows 136) (Fin.cases (hrows 137) (fun i => Fin.elim0 i))))
def support440 : Finset (Fin 252) := {158, 176, 179, 189, 196, 203, 204, 211, 216, 226, 229, 231, 236, 237, 238, 243}
theorem cut440 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    2 ≤ ∑ i ∈ support440, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 158, OmissionBalanced.support 136, OmissionBalanced.support 137] ![OmissionBalanced.demand 158, OmissionBalanced.demand 136, OmissionBalanced.demand 137] ![1, 1, 1]
    support440 2 2 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 158) (Fin.cases (hrows 136) (Fin.cases (hrows 137) (fun i => Fin.elim0 i))))
def support441 : Finset (Fin 252) := {192, 205, 210, 216, 221, 223, 225, 229, 232, 236, 239, 240, 241, 245, 248, 250}
theorem cut441 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support441, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1023, OmissionBalanced.support 1021, OmissionBalanced.support 2683] ![OmissionBalanced.demand 1023, OmissionBalanced.demand 1021, OmissionBalanced.demand 2683] ![1, 1, 1]
    support441 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1023) (Fin.cases (hrows 1021) (Fin.cases (hrows 2683) (fun i => Fin.elim0 i))))
def support442 : Finset (Fin 252) := {192, 205, 210, 216, 221, 223, 225, 229, 232, 236, 239, 240, 241, 245, 248, 250, 251}
theorem cut442 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support442, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 1023, OmissionBalanced.support 1021, OmissionBalanced.support 2684] ![OmissionBalanced.demand 1023, OmissionBalanced.demand 1021, OmissionBalanced.demand 2684] ![1, 1, 1]
    support442 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 1023) (Fin.cases (hrows 1021) (Fin.cases (hrows 2684) (fun i => Fin.elim0 i))))
def support443 : Finset (Fin 252) := {32, 42, 47, 54, 55, 60, 70, 80, 90, 96, 97, 115, 127, 133, 151, 168}
theorem cut443 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    3 ≤ ∑ i ∈ support443, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 423, OmissionBalanced.support 484, OmissionBalanced.support 76] ![OmissionBalanced.demand 423, OmissionBalanced.demand 484, OmissionBalanced.demand 76] ![1, 1, 1]
    support443 2 3 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 423) (Fin.cases (hrows 484) (Fin.cases (hrows 76) (fun i => Fin.elim0 i))))
def support444 : Finset (Fin 252) := {32, 42, 54, 55, 60, 66, 70, 90, 96, 104, 107, 115, 123, 133, 150, 159, 174}
theorem cut444 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    4 ≤ ∑ i ∈ support444, holes i := by
  apply rounded_cover_cut ![OmissionBalanced.support 426, OmissionBalanced.support 483, OmissionBalanced.support 418] ![OmissionBalanced.demand 426, OmissionBalanced.demand 483, OmissionBalanced.demand 418] ![1, 1, 1]
    support444 2 4 (by decide +kernel) holes hbool
  exact (Fin.cases (hrows 426) (Fin.cases (hrows 483) (Fin.cases (hrows 418) (fun i => Fin.elim0 i))))
def support445 : Finset (Fin 252) := {0, 1, 3, 7, 11, 13, 17, 18, 20, 22, 25, 31, 34, 38, 46, 51, 65, 99, 117, 135, 155, 162, 171, 180, 188, 190, 194, 195, 202, 203, 208, 209, 215, 218, 226, 227, 229, 231, 234, 236, 238, 241, 246}
theorem cut445 (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    7 ≤ ∑ i ∈ support445, holes i := by
  apply rounded_cover_cut ![support194, support195, OmissionBalanced.support 128, OmissionBalanced.support 821, OmissionBalanced.support 820, OmissionBalanced.support 167, OmissionBalanced.support 130] ![3, 3, OmissionBalanced.demand 128, OmissionBalanced.demand 821, OmissionBalanced.demand 820, OmissionBalanced.demand 167, OmissionBalanced.demand 130] ![1, 1, 1, 1, 1, 1, 1]
    support445 2 7 (by decide +kernel) holes hbool
  exact (Fin.cases (cut194 holes hbool hrows) (Fin.cases (cut195 holes hbool hrows) (Fin.cases (hrows 128) (Fin.cases (hrows 821) (Fin.cases (hrows 820) (Fin.cases (hrows 167) (Fin.cases (hrows 130) (fun i => Fin.elim0 i))))))))
def support : Fin 446 → Finset (Fin 252) := ![support0, support1, support2, support3, support4, support5, support6, support7, support8, support9, support10, support11, support12, support13, support14, support15, support16, support17, support18, support19, support20, support21, support22, support23, support24, support25, support26, support27, support28, support29, support30, support31, support32, support33, support34, support35, support36, support37, support38, support39, support40, support41, support42, support43, support44, support45, support46, support47, support48, support49, support50, support51, support52, support53, support54, support55, support56, support57, support58, support59, support60, support61, support62, support63, support64, support65, support66, support67, support68, support69, support70, support71, support72, support73, support74, support75, support76, support77, support78, support79, support80, support81, support82, support83, support84, support85, support86, support87, support88, support89, support90, support91, support92, support93, support94, support95, support96, support97, support98, support99, support100, support101, support102, support103, support104, support105, support106, support107, support108, support109, support110, support111, support112, support113, support114, support115, support116, support117, support118, support119, support120, support121, support122, support123, support124, support125, support126, support127, support128, support129, support130, support131, support132, support133, support134, support135, support136, support137, support138, support139, support140, support141, support142, support143, support144, support145, support146, support147, support148, support149, support150, support151, support152, support153, support154, support155, support156, support157, support158, support159, support160, support161, support162, support163, support164, support165, support166, support167, support168, support169, support170, support171, support172, support173, support174, support175, support176, support177, support178, support179, support180, support181, support182, support183, support184, support185, support186, support187, support188, support189, support190, support191, support192, support193, support194, support195, support196, support197, support198, support199, support200, support201, support202, support203, support204, support205, support206, support207, support208, support209, support210, support211, support212, support213, support214, support215, support216, support217, support218, support219, support220, support221, support222, support223, support224, support225, support226, support227, support228, support229, support230, support231, support232, support233, support234, support235, support236, support237, support238, support239, support240, support241, support242, support243, support244, support245, support246, support247, support248, support249, support250, support251, support252, support253, support254, support255, support256, support257, support258, support259, support260, support261, support262, support263, support264, support265, support266, support267, support268, support269, support270, support271, support272, support273, support274, support275, support276, support277, support278, support279, support280, support281, support282, support283, support284, support285, support286, support287, support288, support289, support290, support291, support292, support293, support294, support295, support296, support297, support298, support299, support300, support301, support302, support303, support304, support305, support306, support307, support308, support309, support310, support311, support312, support313, support314, support315, support316, support317, support318, support319, support320, support321, support322, support323, support324, support325, support326, support327, support328, support329, support330, support331, support332, support333, support334, support335, support336, support337, support338, support339, support340, support341, support342, support343, support344, support345, support346, support347, support348, support349, support350, support351, support352, support353, support354, support355, support356, support357, support358, support359, support360, support361, support362, support363, support364, support365, support366, support367, support368, support369, support370, support371, support372, support373, support374, support375, support376, support377, support378, support379, support380, support381, support382, support383, support384, support385, support386, support387, support388, support389, support390, support391, support392, support393, support394, support395, support396, support397, support398, support399, support400, support401, support402, support403, support404, support405, support406, support407, support408, support409, support410, support411, support412, support413, support414, support415, support416, support417, support418, support419, support420, support421, support422, support423, support424, support425, support426, support427, support428, support429, support430, support431, support432, support433, support434, support435, support436, support437, support438, support439, support440, support441, support442, support443, support444, support445]
def demand : Fin 446 → ℕ := ![2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 4, 3, 2, 4, 3, 4, 3, 2, 4, 3, 3, 4, 4, 3, 2, 3, 4, 4, 3, 3, 4, 4, 3, 4, 3, 4, 3, 4, 2, 3, 4, 4, 3, 3, 4, 2, 2, 2, 4, 3, 4, 3, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 3, 2, 3, 2, 2, 3, 4, 2, 2, 2, 2, 2, 2, 3, 3, 2, 3, 3, 3, 3, 2, 2, 4, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 3, 4, 2, 2, 3, 3, 4, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4, 55, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 4, 4, 2, 2, 3, 3, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 4, 3, 3, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 2, 2, 2, 4, 3, 4, 3, 4, 3, 3, 3, 4, 2, 3, 4, 4, 4, 3, 3, 2, 2, 4, 3, 3, 3, 3, 4, 3, 4, 4, 4, 4, 4, 3, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 4, 3, 3, 3, 2, 3, 4, 4, 3, 2, 3, 4, 4, 3, 4, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 3, 3, 2, 2, 3, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 3, 3, 3, 4, 3, 3, 4, 3, 5, 2, 2, 3, 4, 4, 3, 4, 4, 4, 4, 4, 4, 3, 3, 5, 5, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 4, 7]
theorem all_rows (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    ∀ r, demand r ≤ ∑ i ∈ support r, holes i := by
  unfold support demand
  exact (Fin.cases (cut0 holes hbool hrows) (Fin.cases (cut1 holes hbool hrows) (Fin.cases (cut2 holes hbool hrows) (Fin.cases (cut3 holes hbool hrows) (Fin.cases (cut4 holes hbool hrows) (Fin.cases (cut5 holes hbool hrows) (Fin.cases (cut6 holes hbool hrows) (Fin.cases (cut7 holes hbool hrows) (Fin.cases (cut8 holes hbool hrows) (Fin.cases (cut9 holes hbool hrows) (Fin.cases (cut10 holes hbool hrows) (Fin.cases (cut11 holes hbool hrows) (Fin.cases (cut12 holes hbool hrows) (Fin.cases (cut13 holes hbool hrows) (Fin.cases (cut14 holes hbool hrows) (Fin.cases (cut15 holes hbool hrows) (Fin.cases (cut16 holes hbool hrows) (Fin.cases (cut17 holes hbool hrows) (Fin.cases (cut18 holes hbool hrows) (Fin.cases (cut19 holes hbool hrows) (Fin.cases (cut20 holes hbool hrows) (Fin.cases (cut21 holes hbool hrows) (Fin.cases (cut22 holes hbool hrows) (Fin.cases (cut23 holes hbool hrows) (Fin.cases (cut24 holes hbool hrows) (Fin.cases (cut25 holes hbool hrows) (Fin.cases (cut26 holes hbool hrows) (Fin.cases (cut27 holes hbool hrows) (Fin.cases (cut28 holes hbool hrows) (Fin.cases (cut29 holes hbool hrows) (Fin.cases (cut30 holes hbool hrows) (Fin.cases (cut31 holes hbool hrows) (Fin.cases (cut32 holes hbool hrows) (Fin.cases (cut33 holes hbool hrows) (Fin.cases (cut34 holes hbool hrows) (Fin.cases (cut35 holes hbool hrows) (Fin.cases (cut36 holes hbool hrows) (Fin.cases (cut37 holes hbool hrows) (Fin.cases (cut38 holes hbool hrows) (Fin.cases (cut39 holes hbool hrows) (Fin.cases (cut40 holes hbool hrows) (Fin.cases (cut41 holes hbool hrows) (Fin.cases (cut42 holes hbool hrows) (Fin.cases (cut43 holes hbool hrows) (Fin.cases (cut44 holes hbool hrows) (Fin.cases (cut45 holes hbool hrows) (Fin.cases (cut46 holes hbool hrows) (Fin.cases (cut47 holes hbool hrows) (Fin.cases (cut48 holes hbool hrows) (Fin.cases (cut49 holes hbool hrows) (Fin.cases (cut50 holes hbool hrows) (Fin.cases (cut51 holes hbool hrows) (Fin.cases (cut52 holes hbool hrows) (Fin.cases (cut53 holes hbool hrows) (Fin.cases (cut54 holes hbool hrows) (Fin.cases (cut55 holes hbool hrows) (Fin.cases (cut56 holes hbool hrows) (Fin.cases (cut57 holes hbool hrows) (Fin.cases (cut58 holes hbool hrows) (Fin.cases (cut59 holes hbool hrows) (Fin.cases (cut60 holes hbool hrows) (Fin.cases (cut61 holes hbool hrows) (Fin.cases (cut62 holes hbool hrows) (Fin.cases (cut63 holes hbool hrows) (Fin.cases (cut64 holes hbool hrows) (Fin.cases (cut65 holes hbool hrows) (Fin.cases (cut66 holes hbool hrows) (Fin.cases (cut67 holes hbool hrows) (Fin.cases (cut68 holes hbool hrows) (Fin.cases (cut69 holes hbool hrows) (Fin.cases (cut70 holes hbool hrows) (Fin.cases (cut71 holes hbool hrows) (Fin.cases (cut72 holes hbool hrows) (Fin.cases (cut73 holes hbool hrows) (Fin.cases (cut74 holes hbool hrows) (Fin.cases (cut75 holes hbool hrows) (Fin.cases (cut76 holes hbool hrows) (Fin.cases (cut77 holes hbool hrows) (Fin.cases (cut78 holes hbool hrows) (Fin.cases (cut79 holes hbool hrows) (Fin.cases (cut80 holes hbool hrows) (Fin.cases (cut81 holes hbool hrows) (Fin.cases (cut82 holes hbool hrows) (Fin.cases (cut83 holes hbool hrows) (Fin.cases (cut84 holes hbool hrows) (Fin.cases (cut85 holes hbool hrows) (Fin.cases (cut86 holes hbool hrows) (Fin.cases (cut87 holes hbool hrows) (Fin.cases (cut88 holes hbool hrows) (Fin.cases (cut89 holes hbool hrows) (Fin.cases (cut90 holes hbool hrows) (Fin.cases (cut91 holes hbool hrows) (Fin.cases (cut92 holes hbool hrows) (Fin.cases (cut93 holes hbool hrows) (Fin.cases (cut94 holes hbool hrows) (Fin.cases (cut95 holes hbool hrows) (Fin.cases (cut96 holes hbool hrows) (Fin.cases (cut97 holes hbool hrows) (Fin.cases (cut98 holes hbool hrows) (Fin.cases (cut99 holes hbool hrows) (Fin.cases (cut100 holes hbool hrows) (Fin.cases (cut101 holes hbool hrows) (Fin.cases (cut102 holes hbool hrows) (Fin.cases (cut103 holes hbool hrows) (Fin.cases (cut104 holes hbool hrows) (Fin.cases (cut105 holes hbool hrows) (Fin.cases (cut106 holes hbool hrows) (Fin.cases (cut107 holes hbool hrows) (Fin.cases (cut108 holes hbool hrows) (Fin.cases (cut109 holes hbool hrows) (Fin.cases (cut110 holes hbool hrows) (Fin.cases (cut111 holes hbool hrows) (Fin.cases (cut112 holes hbool hrows) (Fin.cases (cut113 holes hbool hrows) (Fin.cases (cut114 holes hbool hrows) (Fin.cases (cut115 holes hbool hrows) (Fin.cases (cut116 holes hbool hrows) (Fin.cases (cut117 holes hbool hrows) (Fin.cases (cut118 holes hbool hrows) (Fin.cases (cut119 holes hbool hrows) (Fin.cases (cut120 holes hbool hrows) (Fin.cases (cut121 holes hbool hrows) (Fin.cases (cut122 holes hbool hrows) (Fin.cases (cut123 holes hbool hrows) (Fin.cases (cut124 holes hbool hrows) (Fin.cases (cut125 holes hbool hrows) (Fin.cases (cut126 holes hbool hrows) (Fin.cases (cut127 holes hbool hrows) (Fin.cases (cut128 holes hbool hrows) (Fin.cases (cut129 holes hbool hrows) (Fin.cases (cut130 holes hbool hrows) (Fin.cases (cut131 holes hbool hrows) (Fin.cases (cut132 holes hbool hrows) (Fin.cases (cut133 holes hbool hrows) (Fin.cases (cut134 holes hbool hrows) (Fin.cases (cut135 holes hbool hrows) (Fin.cases (cut136 holes hbool hrows) (Fin.cases (cut137 holes hbool hrows) (Fin.cases (cut138 holes hbool hrows) (Fin.cases (cut139 holes hbool hrows) (Fin.cases (cut140 holes hbool hrows) (Fin.cases (cut141 holes hbool hrows) (Fin.cases (cut142 holes hbool hrows) (Fin.cases (cut143 holes hbool hrows) (Fin.cases (cut144 holes hbool hrows) (Fin.cases (cut145 holes hbool hrows) (Fin.cases (cut146 holes hbool hrows) (Fin.cases (cut147 holes hbool hrows) (Fin.cases (cut148 holes hbool hrows) (Fin.cases (cut149 holes hbool hrows) (Fin.cases (cut150 holes hbool hrows) (Fin.cases (cut151 holes hbool hrows) (Fin.cases (cut152 holes hbool hrows) (Fin.cases (cut153 holes hbool hrows) (Fin.cases (cut154 holes hbool hrows) (Fin.cases (cut155 holes hbool hrows) (Fin.cases (cut156 holes hbool hrows) (Fin.cases (cut157 holes hbool hrows) (Fin.cases (cut158 holes hbool hrows) (Fin.cases (cut159 holes hbool hrows) (Fin.cases (cut160 holes hbool hrows) (Fin.cases (cut161 holes hbool hrows) (Fin.cases (cut162 holes hbool hrows) (Fin.cases (cut163 holes hbool hrows) (Fin.cases (cut164 holes hbool hrows) (Fin.cases (cut165 holes hbool hrows) (Fin.cases (cut166 holes hbool hrows) (Fin.cases (cut167 holes hbool hrows) (Fin.cases (cut168 holes hbool hrows) (Fin.cases (cut169 holes hbool hrows) (Fin.cases (cut170 holes hbool hrows) (Fin.cases (cut171 holes hbool hrows) (Fin.cases (cut172 holes hbool hrows) (Fin.cases (cut173 holes hbool hrows) (Fin.cases (cut174 holes hbool hrows) (Fin.cases (cut175 holes hbool hrows) (Fin.cases (cut176 holes hbool hrows) (Fin.cases (cut177 holes hbool hrows) (Fin.cases (cut178 holes hbool hrows) (Fin.cases (cut179 holes hbool hrows) (Fin.cases (cut180 holes hbool hrows) (Fin.cases (cut181 holes hbool hrows) (Fin.cases (cut182 holes hbool hrows) (Fin.cases (cut183 holes hbool hrows) (Fin.cases (cut184 holes hbool hrows) (Fin.cases (cut185 holes hbool hrows) (Fin.cases (cut186 holes hbool hrows) (Fin.cases (cut187 holes hbool hrows) (Fin.cases (cut188 holes hbool hrows) (Fin.cases (cut189 holes hbool hrows) (Fin.cases (cut190 holes hbool hrows) (Fin.cases (cut191 holes hbool hrows) (Fin.cases (cut192 holes hbool hrows) (Fin.cases (cut193 holes hbool hrows) (Fin.cases (cut194 holes hbool hrows) (Fin.cases (cut195 holes hbool hrows) (Fin.cases (cut196 holes hbool hrows) (Fin.cases (cut197 holes hbool hrows) (Fin.cases (cut198 holes hbool hrows) (Fin.cases (cut199 holes hbool hrows) (Fin.cases (cut200 holes hbool hrows) (Fin.cases (cut201 holes hbool hrows) (Fin.cases (cut202 holes hbool hrows) (Fin.cases (cut203 holes hbool hrows) (Fin.cases (cut204 holes hbool hrows) (Fin.cases (cut205 holes hbool hrows) (Fin.cases (cut206 holes hbool hrows) (Fin.cases (cut207 holes hbool hrows) (Fin.cases (cut208 holes hbool hrows) (Fin.cases (cut209 holes hbool hrows) (Fin.cases (cut210 holes hbool hrows) (Fin.cases (cut211 holes hbool hrows) (Fin.cases (cut212 holes hbool hrows) (Fin.cases (cut213 holes hbool hrows) (Fin.cases (cut214 holes hbool hrows) (Fin.cases (cut215 holes hbool hrows) (Fin.cases (cut216 holes hbool hrows) (Fin.cases (cut217 holes hbool hrows) (Fin.cases (cut218 holes hbool hrows) (Fin.cases (cut219 holes hbool hrows) (Fin.cases (cut220 holes hbool hrows) (Fin.cases (cut221 holes hbool hrows) (Fin.cases (cut222 holes hbool hrows) (Fin.cases (cut223 holes hbool hrows) (Fin.cases (cut224 holes hbool hrows) (Fin.cases (cut225 holes hbool hrows) (Fin.cases (cut226 holes hbool hrows) (Fin.cases (cut227 holes hbool hrows) (Fin.cases (cut228 holes hbool hrows) (Fin.cases (cut229 holes hbool hrows) (Fin.cases (cut230 holes hbool hrows) (Fin.cases (cut231 holes hbool hrows) (Fin.cases (cut232 holes hbool hrows) (Fin.cases (cut233 holes hbool hrows) (Fin.cases (cut234 holes hbool hrows) (Fin.cases (cut235 holes hbool hrows) (Fin.cases (cut236 holes hbool hrows) (Fin.cases (cut237 holes hbool hrows) (Fin.cases (cut238 holes hbool hrows) (Fin.cases (cut239 holes hbool hrows) (Fin.cases (cut240 holes hbool hrows) (Fin.cases (cut241 holes hbool hrows) (Fin.cases (cut242 holes hbool hrows) (Fin.cases (cut243 holes hbool hrows) (Fin.cases (cut244 holes hbool hrows) (Fin.cases (cut245 holes hbool hrows) (Fin.cases (cut246 holes hbool hrows) (Fin.cases (cut247 holes hbool hrows) (Fin.cases (cut248 holes hbool hrows) (Fin.cases (cut249 holes hbool hrows) (Fin.cases (cut250 holes hbool hrows) (Fin.cases (cut251 holes hbool hrows) (Fin.cases (cut252 holes hbool hrows) (Fin.cases (cut253 holes hbool hrows) (Fin.cases (cut254 holes hbool hrows) (Fin.cases (cut255 holes hbool hrows) (Fin.cases (cut256 holes hbool hrows) (Fin.cases (cut257 holes hbool hrows) (Fin.cases (cut258 holes hbool hrows) (Fin.cases (cut259 holes hbool hrows) (Fin.cases (cut260 holes hbool hrows) (Fin.cases (cut261 holes hbool hrows) (Fin.cases (cut262 holes hbool hrows) (Fin.cases (cut263 holes hbool hrows) (Fin.cases (cut264 holes hbool hrows) (Fin.cases (cut265 holes hbool hrows) (Fin.cases (cut266 holes hbool hrows) (Fin.cases (cut267 holes hbool hrows) (Fin.cases (cut268 holes hbool hrows) (Fin.cases (cut269 holes hbool hrows) (Fin.cases (cut270 holes hbool hrows) (Fin.cases (cut271 holes hbool hrows) (Fin.cases (cut272 holes hbool hrows) (Fin.cases (cut273 holes hbool hrows) (Fin.cases (cut274 holes hbool hrows) (Fin.cases (cut275 holes hbool hrows) (Fin.cases (cut276 holes hbool hrows) (Fin.cases (cut277 holes hbool hrows) (Fin.cases (cut278 holes hbool hrows) (Fin.cases (cut279 holes hbool hrows) (Fin.cases (cut280 holes hbool hrows) (Fin.cases (cut281 holes hbool hrows) (Fin.cases (cut282 holes hbool hrows) (Fin.cases (cut283 holes hbool hrows) (Fin.cases (cut284 holes hbool hrows) (Fin.cases (cut285 holes hbool hrows) (Fin.cases (cut286 holes hbool hrows) (Fin.cases (cut287 holes hbool hrows) (Fin.cases (cut288 holes hbool hrows) (Fin.cases (cut289 holes hbool hrows) (Fin.cases (cut290 holes hbool hrows) (Fin.cases (cut291 holes hbool hrows) (Fin.cases (cut292 holes hbool hrows) (Fin.cases (cut293 holes hbool hrows) (Fin.cases (cut294 holes hbool hrows) (Fin.cases (cut295 holes hbool hrows) (Fin.cases (cut296 holes hbool hrows) (Fin.cases (cut297 holes hbool hrows) (Fin.cases (cut298 holes hbool hrows) (Fin.cases (cut299 holes hbool hrows) (Fin.cases (cut300 holes hbool hrows) (Fin.cases (cut301 holes hbool hrows) (Fin.cases (cut302 holes hbool hrows) (Fin.cases (cut303 holes hbool hrows) (Fin.cases (cut304 holes hbool hrows) (Fin.cases (cut305 holes hbool hrows) (Fin.cases (cut306 holes hbool hrows) (Fin.cases (cut307 holes hbool hrows) (Fin.cases (cut308 holes hbool hrows) (Fin.cases (cut309 holes hbool hrows) (Fin.cases (cut310 holes hbool hrows) (Fin.cases (cut311 holes hbool hrows) (Fin.cases (cut312 holes hbool hrows) (Fin.cases (cut313 holes hbool hrows) (Fin.cases (cut314 holes hbool hrows) (Fin.cases (cut315 holes hbool hrows) (Fin.cases (cut316 holes hbool hrows) (Fin.cases (cut317 holes hbool hrows) (Fin.cases (cut318 holes hbool hrows) (Fin.cases (cut319 holes hbool hrows) (Fin.cases (cut320 holes hbool hrows) (Fin.cases (cut321 holes hbool hrows) (Fin.cases (cut322 holes hbool hrows) (Fin.cases (cut323 holes hbool hrows) (Fin.cases (cut324 holes hbool hrows) (Fin.cases (cut325 holes hbool hrows) (Fin.cases (cut326 holes hbool hrows) (Fin.cases (cut327 holes hbool hrows) (Fin.cases (cut328 holes hbool hrows) (Fin.cases (cut329 holes hbool hrows) (Fin.cases (cut330 holes hbool hrows) (Fin.cases (cut331 holes hbool hrows) (Fin.cases (cut332 holes hbool hrows) (Fin.cases (cut333 holes hbool hrows) (Fin.cases (cut334 holes hbool hrows) (Fin.cases (cut335 holes hbool hrows) (Fin.cases (cut336 holes hbool hrows) (Fin.cases (cut337 holes hbool hrows) (Fin.cases (cut338 holes hbool hrows) (Fin.cases (cut339 holes hbool hrows) (Fin.cases (cut340 holes hbool hrows) (Fin.cases (cut341 holes hbool hrows) (Fin.cases (cut342 holes hbool hrows) (Fin.cases (cut343 holes hbool hrows) (Fin.cases (cut344 holes hbool hrows) (Fin.cases (cut345 holes hbool hrows) (Fin.cases (cut346 holes hbool hrows) (Fin.cases (cut347 holes hbool hrows) (Fin.cases (cut348 holes hbool hrows) (Fin.cases (cut349 holes hbool hrows) (Fin.cases (cut350 holes hbool hrows) (Fin.cases (cut351 holes hbool hrows) (Fin.cases (cut352 holes hbool hrows) (Fin.cases (cut353 holes hbool hrows) (Fin.cases (cut354 holes hbool hrows) (Fin.cases (cut355 holes hbool hrows) (Fin.cases (cut356 holes hbool hrows) (Fin.cases (cut357 holes hbool hrows) (Fin.cases (cut358 holes hbool hrows) (Fin.cases (cut359 holes hbool hrows) (Fin.cases (cut360 holes hbool hrows) (Fin.cases (cut361 holes hbool hrows) (Fin.cases (cut362 holes hbool hrows) (Fin.cases (cut363 holes hbool hrows) (Fin.cases (cut364 holes hbool hrows) (Fin.cases (cut365 holes hbool hrows) (Fin.cases (cut366 holes hbool hrows) (Fin.cases (cut367 holes hbool hrows) (Fin.cases (cut368 holes hbool hrows) (Fin.cases (cut369 holes hbool hrows) (Fin.cases (cut370 holes hbool hrows) (Fin.cases (cut371 holes hbool hrows) (Fin.cases (cut372 holes hbool hrows) (Fin.cases (cut373 holes hbool hrows) (Fin.cases (cut374 holes hbool hrows) (Fin.cases (cut375 holes hbool hrows) (Fin.cases (cut376 holes hbool hrows) (Fin.cases (cut377 holes hbool hrows) (Fin.cases (cut378 holes hbool hrows) (Fin.cases (cut379 holes hbool hrows) (Fin.cases (cut380 holes hbool hrows) (Fin.cases (cut381 holes hbool hrows) (Fin.cases (cut382 holes hbool hrows) (Fin.cases (cut383 holes hbool hrows) (Fin.cases (cut384 holes hbool hrows) (Fin.cases (cut385 holes hbool hrows) (Fin.cases (cut386 holes hbool hrows) (Fin.cases (cut387 holes hbool hrows) (Fin.cases (cut388 holes hbool hrows) (Fin.cases (cut389 holes hbool hrows) (Fin.cases (cut390 holes hbool hrows) (Fin.cases (cut391 holes hbool hrows) (Fin.cases (cut392 holes hbool hrows) (Fin.cases (cut393 holes hbool hrows) (Fin.cases (cut394 holes hbool hrows) (Fin.cases (cut395 holes hbool hrows) (Fin.cases (cut396 holes hbool hrows) (Fin.cases (cut397 holes hbool hrows) (Fin.cases (cut398 holes hbool hrows) (Fin.cases (cut399 holes hbool hrows) (Fin.cases (cut400 holes hbool hrows) (Fin.cases (cut401 holes hbool hrows) (Fin.cases (cut402 holes hbool hrows) (Fin.cases (cut403 holes hbool hrows) (Fin.cases (cut404 holes hbool hrows) (Fin.cases (cut405 holes hbool hrows) (Fin.cases (cut406 holes hbool hrows) (Fin.cases (cut407 holes hbool hrows) (Fin.cases (cut408 holes hbool hrows) (Fin.cases (cut409 holes hbool hrows) (Fin.cases (cut410 holes hbool hrows) (Fin.cases (cut411 holes hbool hrows) (Fin.cases (cut412 holes hbool hrows) (Fin.cases (cut413 holes hbool hrows) (Fin.cases (cut414 holes hbool hrows) (Fin.cases (cut415 holes hbool hrows) (Fin.cases (cut416 holes hbool hrows) (Fin.cases (cut417 holes hbool hrows) (Fin.cases (cut418 holes hbool hrows) (Fin.cases (cut419 holes hbool hrows) (Fin.cases (cut420 holes hbool hrows) (Fin.cases (cut421 holes hbool hrows) (Fin.cases (cut422 holes hbool hrows) (Fin.cases (cut423 holes hbool hrows) (Fin.cases (cut424 holes hbool hrows) (Fin.cases (cut425 holes hbool hrows) (Fin.cases (cut426 holes hbool hrows) (Fin.cases (cut427 holes hbool hrows) (Fin.cases (cut428 holes hbool hrows) (Fin.cases (cut429 holes hbool hrows) (Fin.cases (cut430 holes hbool hrows) (Fin.cases (cut431 holes hbool hrows) (Fin.cases (cut432 holes hbool hrows) (Fin.cases (cut433 holes hbool hrows) (Fin.cases (cut434 holes hbool hrows) (Fin.cases (cut435 holes hbool hrows) (Fin.cases (cut436 holes hbool hrows) (Fin.cases (cut437 holes hbool hrows) (Fin.cases (cut438 holes hbool hrows) (Fin.cases (cut439 holes hbool hrows) (Fin.cases (cut440 holes hbool hrows) (Fin.cases (cut441 holes hbool hrows) (Fin.cases (cut442 holes hbool hrows) (Fin.cases (cut443 holes hbool hrows) (Fin.cases (cut444 holes hbool hrows) (Fin.cases (cut445 holes hbool hrows) (fun i => Fin.elim0 i)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#print axioms all_rows
end BalancedCoverCutsV2
