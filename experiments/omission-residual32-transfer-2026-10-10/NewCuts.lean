import Residual32ContextsProof.Catalog
import ErdosSzekeres.Omission.CoverCuts
open scoped BigOperators
open ErdosSzekeres
namespace OmissionResidual32Transfer
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

open ErdosSzekeres.OmissionCertificates
theorem cut0 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2457 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2457, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 1075, OmissionResidual32Contexts.support 1076, OmissionResidual32Contexts.support 1125] ![OmissionResidual32Contexts.demand 1075, OmissionResidual32Contexts.demand 1076, OmissionResidual32Contexts.demand 1125] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2457) 2 (OmissionResidual32Contexts.demand 2457) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨1075, by omega⟩) (Fin.cases (hrows ⟨1076, by omega⟩) (Fin.cases (hrows ⟨1125, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut0
theorem cut1 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2458 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2458, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 934, OmissionResidual32Contexts.support 1143, OmissionResidual32Contexts.support 933] ![OmissionResidual32Contexts.demand 934, OmissionResidual32Contexts.demand 1143, OmissionResidual32Contexts.demand 933] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2458) 2 (OmissionResidual32Contexts.demand 2458) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨934, by omega⟩) (Fin.cases (hrows ⟨1143, by omega⟩) (Fin.cases (hrows ⟨933, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut1
theorem cut2 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2459 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2459, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 1098, OmissionResidual32Contexts.support 1159, OmissionResidual32Contexts.support 819] ![OmissionResidual32Contexts.demand 1098, OmissionResidual32Contexts.demand 1159, OmissionResidual32Contexts.demand 819] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2459) 2 (OmissionResidual32Contexts.demand 2459) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨1098, by omega⟩) (Fin.cases (hrows ⟨1159, by omega⟩) (Fin.cases (hrows ⟨819, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut2
theorem cut3 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2460 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2460, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 1098, OmissionResidual32Contexts.support 1160, OmissionResidual32Contexts.support 819] ![OmissionResidual32Contexts.demand 1098, OmissionResidual32Contexts.demand 1160, OmissionResidual32Contexts.demand 819] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2460) 2 (OmissionResidual32Contexts.demand 2460) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨1098, by omega⟩) (Fin.cases (hrows ⟨1160, by omega⟩) (Fin.cases (hrows ⟨819, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut3
theorem cut4 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2461 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2461, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 924, OmissionResidual32Contexts.support 587, OmissionResidual32Contexts.support 898] ![OmissionResidual32Contexts.demand 924, OmissionResidual32Contexts.demand 587, OmissionResidual32Contexts.demand 898] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2461) 2 (OmissionResidual32Contexts.demand 2461) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨924, by omega⟩) (Fin.cases (hrows ⟨587, by omega⟩) (Fin.cases (hrows ⟨898, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut4
theorem cut5 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2462 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2462, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 2457, OmissionResidual32Contexts.support 817, OmissionResidual32Contexts.support 1621] ![OmissionResidual32Contexts.demand 2457, OmissionResidual32Contexts.demand 817, OmissionResidual32Contexts.demand 1621] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2462) 2 (OmissionResidual32Contexts.demand 2462) (by decide +kernel) holes hbool
  exact (Fin.cases (cut0 holes hbool hrows) (Fin.cases (hrows ⟨817, by omega⟩) (Fin.cases (hrows ⟨1621, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut5
theorem cut6 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2463 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2463, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 12, OmissionResidual32Contexts.support 72, OmissionResidual32Contexts.support 62] ![OmissionResidual32Contexts.demand 12, OmissionResidual32Contexts.demand 72, OmissionResidual32Contexts.demand 62] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2463) 2 (OmissionResidual32Contexts.demand 2463) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨12, by omega⟩) (Fin.cases (hrows ⟨72, by omega⟩) (Fin.cases (hrows ⟨62, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut6
theorem cut7 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2464 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2464, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 32, OmissionResidual32Contexts.support 37, OmissionResidual32Contexts.support 116] ![OmissionResidual32Contexts.demand 32, OmissionResidual32Contexts.demand 37, OmissionResidual32Contexts.demand 116] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2464) 2 (OmissionResidual32Contexts.demand 2464) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨32, by omega⟩) (Fin.cases (hrows ⟨37, by omega⟩) (Fin.cases (hrows ⟨116, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut7
theorem cut8 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2465 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2465, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 12, OmissionResidual32Contexts.support 37, OmissionResidual32Contexts.support 116] ![OmissionResidual32Contexts.demand 12, OmissionResidual32Contexts.demand 37, OmissionResidual32Contexts.demand 116] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2465) 2 (OmissionResidual32Contexts.demand 2465) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨12, by omega⟩) (Fin.cases (hrows ⟨37, by omega⟩) (Fin.cases (hrows ⟨116, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut8
theorem cut9 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2466 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2466, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 32, OmissionResidual32Contexts.support 72, OmissionResidual32Contexts.support 62] ![OmissionResidual32Contexts.demand 32, OmissionResidual32Contexts.demand 72, OmissionResidual32Contexts.demand 62] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2466) 2 (OmissionResidual32Contexts.demand 2466) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨32, by omega⟩) (Fin.cases (hrows ⟨72, by omega⟩) (Fin.cases (hrows ⟨62, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut9
theorem cut10 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2467 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2467, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 1551, OmissionResidual32Contexts.support 552, OmissionResidual32Contexts.support 1448] ![OmissionResidual32Contexts.demand 1551, OmissionResidual32Contexts.demand 552, OmissionResidual32Contexts.demand 1448] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2467) 2 (OmissionResidual32Contexts.demand 2467) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨1551, by omega⟩) (Fin.cases (hrows ⟨552, by omega⟩) (Fin.cases (hrows ⟨1448, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut10
theorem cut11 (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    OmissionResidual32Contexts.demand 2468 ≤ ∑ i ∈ OmissionResidual32Contexts.support 2468, holes i := by
  apply rounded_cover_cut ![OmissionResidual32Contexts.support 812, OmissionResidual32Contexts.support 1096, OmissionResidual32Contexts.support 1120] ![OmissionResidual32Contexts.demand 812, OmissionResidual32Contexts.demand 1096, OmissionResidual32Contexts.demand 1120] ![1, 1, 1]
    (OmissionResidual32Contexts.support 2468) 2 (OmissionResidual32Contexts.demand 2468) (by decide +kernel) holes hbool
  exact (Fin.cases (hrows ⟨812, by omega⟩) (Fin.cases (hrows ⟨1096, by omega⟩) (Fin.cases (hrows ⟨1120, by omega⟩) (fun i => Fin.elim0 i))))
#print axioms cut11
theorem new_cut_rows (holes : Fin 154 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2457, OmissionResidual32Contexts.demand ⟨r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨r.val, by omega⟩, holes i) :
    ∀ r : Fin 12, OmissionResidual32Contexts.demand ⟨2457 + r.val, by omega⟩ ≤
      ∑ i ∈ OmissionResidual32Contexts.support ⟨2457 + r.val, by omega⟩, holes i := by
  exact (Fin.cases (cut0 holes hbool hrows) (Fin.cases (cut1 holes hbool hrows) (Fin.cases (cut2 holes hbool hrows) (Fin.cases (cut3 holes hbool hrows) (Fin.cases (cut4 holes hbool hrows) (Fin.cases (cut5 holes hbool hrows) (Fin.cases (cut6 holes hbool hrows) (Fin.cases (cut7 holes hbool hrows) (Fin.cases (cut8 holes hbool hrows) (Fin.cases (cut9 holes hbool hrows) (Fin.cases (cut10 holes hbool hrows) (Fin.cases (cut11 holes hbool hrows) (fun i => Fin.elim0 i)))))))))))))
#print axioms new_cut_rows
end OmissionResidual32Transfer
