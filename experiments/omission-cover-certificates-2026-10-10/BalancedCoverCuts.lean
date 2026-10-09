import BalancedProof.Catalog
import ErdosSzekeres.Omission.CoverCuts
open scoped BigOperators
open ErdosSzekeres.OmissionCertificates
namespace BalancedCoverCuts
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
def support : Fin 220 → Finset (Fin 252) := ![support0, support1, support2, support3, support4, support5, support6, support7, support8, support9, support10, support11, support12, support13, support14, support15, support16, support17, support18, support19, support20, support21, support22, support23, support24, support25, support26, support27, support28, support29, support30, support31, support32, support33, support34, support35, support36, support37, support38, support39, support40, support41, support42, support43, support44, support45, support46, support47, support48, support49, support50, support51, support52, support53, support54, support55, support56, support57, support58, support59, support60, support61, support62, support63, support64, support65, support66, support67, support68, support69, support70, support71, support72, support73, support74, support75, support76, support77, support78, support79, support80, support81, support82, support83, support84, support85, support86, support87, support88, support89, support90, support91, support92, support93, support94, support95, support96, support97, support98, support99, support100, support101, support102, support103, support104, support105, support106, support107, support108, support109, support110, support111, support112, support113, support114, support115, support116, support117, support118, support119, support120, support121, support122, support123, support124, support125, support126, support127, support128, support129, support130, support131, support132, support133, support134, support135, support136, support137, support138, support139, support140, support141, support142, support143, support144, support145, support146, support147, support148, support149, support150, support151, support152, support153, support154, support155, support156, support157, support158, support159, support160, support161, support162, support163, support164, support165, support166, support167, support168, support169, support170, support171, support172, support173, support174, support175, support176, support177, support178, support179, support180, support181, support182, support183, support184, support185, support186, support187, support188, support189, support190, support191, support192, support193, support194, support195, support196, support197, support198, support199, support200, support201, support202, support203, support204, support205, support206, support207, support208, support209, support210, support211, support212, support213, support214, support215, support216, support217, support218, support219]
def demand : Fin 220 → ℕ := ![2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 4, 3, 2, 4, 3, 4, 3, 2, 4, 3, 3, 4, 4, 3, 2, 3, 4, 4, 3, 3, 4, 4, 3, 4, 3, 4, 3, 4, 2, 3, 4, 4, 3, 3, 4, 2, 2, 2, 4, 3, 4, 3, 4, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 3, 2, 3, 2, 2, 3, 4, 2, 2, 2, 2, 2, 2, 3, 3, 2, 3, 3, 3, 3, 2, 2, 4, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 3, 4, 2, 2, 3, 3, 4, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 4, 4, 4]
theorem all_rows (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i) :
    ∀ r, demand r ≤ ∑ i ∈ support r, holes i := by
  unfold support demand
  exact (Fin.cases (cut0 holes hbool hrows) (Fin.cases (cut1 holes hbool hrows) (Fin.cases (cut2 holes hbool hrows) (Fin.cases (cut3 holes hbool hrows) (Fin.cases (cut4 holes hbool hrows) (Fin.cases (cut5 holes hbool hrows) (Fin.cases (cut6 holes hbool hrows) (Fin.cases (cut7 holes hbool hrows) (Fin.cases (cut8 holes hbool hrows) (Fin.cases (cut9 holes hbool hrows) (Fin.cases (cut10 holes hbool hrows) (Fin.cases (cut11 holes hbool hrows) (Fin.cases (cut12 holes hbool hrows) (Fin.cases (cut13 holes hbool hrows) (Fin.cases (cut14 holes hbool hrows) (Fin.cases (cut15 holes hbool hrows) (Fin.cases (cut16 holes hbool hrows) (Fin.cases (cut17 holes hbool hrows) (Fin.cases (cut18 holes hbool hrows) (Fin.cases (cut19 holes hbool hrows) (Fin.cases (cut20 holes hbool hrows) (Fin.cases (cut21 holes hbool hrows) (Fin.cases (cut22 holes hbool hrows) (Fin.cases (cut23 holes hbool hrows) (Fin.cases (cut24 holes hbool hrows) (Fin.cases (cut25 holes hbool hrows) (Fin.cases (cut26 holes hbool hrows) (Fin.cases (cut27 holes hbool hrows) (Fin.cases (cut28 holes hbool hrows) (Fin.cases (cut29 holes hbool hrows) (Fin.cases (cut30 holes hbool hrows) (Fin.cases (cut31 holes hbool hrows) (Fin.cases (cut32 holes hbool hrows) (Fin.cases (cut33 holes hbool hrows) (Fin.cases (cut34 holes hbool hrows) (Fin.cases (cut35 holes hbool hrows) (Fin.cases (cut36 holes hbool hrows) (Fin.cases (cut37 holes hbool hrows) (Fin.cases (cut38 holes hbool hrows) (Fin.cases (cut39 holes hbool hrows) (Fin.cases (cut40 holes hbool hrows) (Fin.cases (cut41 holes hbool hrows) (Fin.cases (cut42 holes hbool hrows) (Fin.cases (cut43 holes hbool hrows) (Fin.cases (cut44 holes hbool hrows) (Fin.cases (cut45 holes hbool hrows) (Fin.cases (cut46 holes hbool hrows) (Fin.cases (cut47 holes hbool hrows) (Fin.cases (cut48 holes hbool hrows) (Fin.cases (cut49 holes hbool hrows) (Fin.cases (cut50 holes hbool hrows) (Fin.cases (cut51 holes hbool hrows) (Fin.cases (cut52 holes hbool hrows) (Fin.cases (cut53 holes hbool hrows) (Fin.cases (cut54 holes hbool hrows) (Fin.cases (cut55 holes hbool hrows) (Fin.cases (cut56 holes hbool hrows) (Fin.cases (cut57 holes hbool hrows) (Fin.cases (cut58 holes hbool hrows) (Fin.cases (cut59 holes hbool hrows) (Fin.cases (cut60 holes hbool hrows) (Fin.cases (cut61 holes hbool hrows) (Fin.cases (cut62 holes hbool hrows) (Fin.cases (cut63 holes hbool hrows) (Fin.cases (cut64 holes hbool hrows) (Fin.cases (cut65 holes hbool hrows) (Fin.cases (cut66 holes hbool hrows) (Fin.cases (cut67 holes hbool hrows) (Fin.cases (cut68 holes hbool hrows) (Fin.cases (cut69 holes hbool hrows) (Fin.cases (cut70 holes hbool hrows) (Fin.cases (cut71 holes hbool hrows) (Fin.cases (cut72 holes hbool hrows) (Fin.cases (cut73 holes hbool hrows) (Fin.cases (cut74 holes hbool hrows) (Fin.cases (cut75 holes hbool hrows) (Fin.cases (cut76 holes hbool hrows) (Fin.cases (cut77 holes hbool hrows) (Fin.cases (cut78 holes hbool hrows) (Fin.cases (cut79 holes hbool hrows) (Fin.cases (cut80 holes hbool hrows) (Fin.cases (cut81 holes hbool hrows) (Fin.cases (cut82 holes hbool hrows) (Fin.cases (cut83 holes hbool hrows) (Fin.cases (cut84 holes hbool hrows) (Fin.cases (cut85 holes hbool hrows) (Fin.cases (cut86 holes hbool hrows) (Fin.cases (cut87 holes hbool hrows) (Fin.cases (cut88 holes hbool hrows) (Fin.cases (cut89 holes hbool hrows) (Fin.cases (cut90 holes hbool hrows) (Fin.cases (cut91 holes hbool hrows) (Fin.cases (cut92 holes hbool hrows) (Fin.cases (cut93 holes hbool hrows) (Fin.cases (cut94 holes hbool hrows) (Fin.cases (cut95 holes hbool hrows) (Fin.cases (cut96 holes hbool hrows) (Fin.cases (cut97 holes hbool hrows) (Fin.cases (cut98 holes hbool hrows) (Fin.cases (cut99 holes hbool hrows) (Fin.cases (cut100 holes hbool hrows) (Fin.cases (cut101 holes hbool hrows) (Fin.cases (cut102 holes hbool hrows) (Fin.cases (cut103 holes hbool hrows) (Fin.cases (cut104 holes hbool hrows) (Fin.cases (cut105 holes hbool hrows) (Fin.cases (cut106 holes hbool hrows) (Fin.cases (cut107 holes hbool hrows) (Fin.cases (cut108 holes hbool hrows) (Fin.cases (cut109 holes hbool hrows) (Fin.cases (cut110 holes hbool hrows) (Fin.cases (cut111 holes hbool hrows) (Fin.cases (cut112 holes hbool hrows) (Fin.cases (cut113 holes hbool hrows) (Fin.cases (cut114 holes hbool hrows) (Fin.cases (cut115 holes hbool hrows) (Fin.cases (cut116 holes hbool hrows) (Fin.cases (cut117 holes hbool hrows) (Fin.cases (cut118 holes hbool hrows) (Fin.cases (cut119 holes hbool hrows) (Fin.cases (cut120 holes hbool hrows) (Fin.cases (cut121 holes hbool hrows) (Fin.cases (cut122 holes hbool hrows) (Fin.cases (cut123 holes hbool hrows) (Fin.cases (cut124 holes hbool hrows) (Fin.cases (cut125 holes hbool hrows) (Fin.cases (cut126 holes hbool hrows) (Fin.cases (cut127 holes hbool hrows) (Fin.cases (cut128 holes hbool hrows) (Fin.cases (cut129 holes hbool hrows) (Fin.cases (cut130 holes hbool hrows) (Fin.cases (cut131 holes hbool hrows) (Fin.cases (cut132 holes hbool hrows) (Fin.cases (cut133 holes hbool hrows) (Fin.cases (cut134 holes hbool hrows) (Fin.cases (cut135 holes hbool hrows) (Fin.cases (cut136 holes hbool hrows) (Fin.cases (cut137 holes hbool hrows) (Fin.cases (cut138 holes hbool hrows) (Fin.cases (cut139 holes hbool hrows) (Fin.cases (cut140 holes hbool hrows) (Fin.cases (cut141 holes hbool hrows) (Fin.cases (cut142 holes hbool hrows) (Fin.cases (cut143 holes hbool hrows) (Fin.cases (cut144 holes hbool hrows) (Fin.cases (cut145 holes hbool hrows) (Fin.cases (cut146 holes hbool hrows) (Fin.cases (cut147 holes hbool hrows) (Fin.cases (cut148 holes hbool hrows) (Fin.cases (cut149 holes hbool hrows) (Fin.cases (cut150 holes hbool hrows) (Fin.cases (cut151 holes hbool hrows) (Fin.cases (cut152 holes hbool hrows) (Fin.cases (cut153 holes hbool hrows) (Fin.cases (cut154 holes hbool hrows) (Fin.cases (cut155 holes hbool hrows) (Fin.cases (cut156 holes hbool hrows) (Fin.cases (cut157 holes hbool hrows) (Fin.cases (cut158 holes hbool hrows) (Fin.cases (cut159 holes hbool hrows) (Fin.cases (cut160 holes hbool hrows) (Fin.cases (cut161 holes hbool hrows) (Fin.cases (cut162 holes hbool hrows) (Fin.cases (cut163 holes hbool hrows) (Fin.cases (cut164 holes hbool hrows) (Fin.cases (cut165 holes hbool hrows) (Fin.cases (cut166 holes hbool hrows) (Fin.cases (cut167 holes hbool hrows) (Fin.cases (cut168 holes hbool hrows) (Fin.cases (cut169 holes hbool hrows) (Fin.cases (cut170 holes hbool hrows) (Fin.cases (cut171 holes hbool hrows) (Fin.cases (cut172 holes hbool hrows) (Fin.cases (cut173 holes hbool hrows) (Fin.cases (cut174 holes hbool hrows) (Fin.cases (cut175 holes hbool hrows) (Fin.cases (cut176 holes hbool hrows) (Fin.cases (cut177 holes hbool hrows) (Fin.cases (cut178 holes hbool hrows) (Fin.cases (cut179 holes hbool hrows) (Fin.cases (cut180 holes hbool hrows) (Fin.cases (cut181 holes hbool hrows) (Fin.cases (cut182 holes hbool hrows) (Fin.cases (cut183 holes hbool hrows) (Fin.cases (cut184 holes hbool hrows) (Fin.cases (cut185 holes hbool hrows) (Fin.cases (cut186 holes hbool hrows) (Fin.cases (cut187 holes hbool hrows) (Fin.cases (cut188 holes hbool hrows) (Fin.cases (cut189 holes hbool hrows) (Fin.cases (cut190 holes hbool hrows) (Fin.cases (cut191 holes hbool hrows) (Fin.cases (cut192 holes hbool hrows) (Fin.cases (cut193 holes hbool hrows) (Fin.cases (cut194 holes hbool hrows) (Fin.cases (cut195 holes hbool hrows) (Fin.cases (cut196 holes hbool hrows) (Fin.cases (cut197 holes hbool hrows) (Fin.cases (cut198 holes hbool hrows) (Fin.cases (cut199 holes hbool hrows) (Fin.cases (cut200 holes hbool hrows) (Fin.cases (cut201 holes hbool hrows) (Fin.cases (cut202 holes hbool hrows) (Fin.cases (cut203 holes hbool hrows) (Fin.cases (cut204 holes hbool hrows) (Fin.cases (cut205 holes hbool hrows) (Fin.cases (cut206 holes hbool hrows) (Fin.cases (cut207 holes hbool hrows) (Fin.cases (cut208 holes hbool hrows) (Fin.cases (cut209 holes hbool hrows) (Fin.cases (cut210 holes hbool hrows) (Fin.cases (cut211 holes hbool hrows) (Fin.cases (cut212 holes hbool hrows) (Fin.cases (cut213 holes hbool hrows) (Fin.cases (cut214 holes hbool hrows) (Fin.cases (cut215 holes hbool hrows) (Fin.cases (cut216 holes hbool hrows) (Fin.cases (cut217 holes hbool hrows) (Fin.cases (cut218 holes hbool hrows) (Fin.cases (cut219 holes hbool hrows) (fun i => Fin.elim0 i)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
#print axioms all_rows
end BalancedCoverCuts
