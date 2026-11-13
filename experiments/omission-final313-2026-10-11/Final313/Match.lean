import Residual2650ZeroProof.Catalog
import Residual32Bridge2650.Catalog

/-!
Row-by-row identity of the exported certificate catalog (`OmissionResidual2650Zero`)
and the bridge catalog (`OmissionResidual32Bridge2650`). Both are generated from the
same 2,650-row source with different packing bases; supports and demands are compared
literally by the kernel in 128-row chunks.
-/

namespace OmissionResidual2650ZeroMatch
open OmissionResidual32Bridge2650

set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

abbrev SameRow (r : ℕ) (h : r < 2650) : Prop :=
  OmissionResidual2650Zero.support ⟨r, h⟩ = support2650 ⟨r, h⟩ ∧
  OmissionResidual2650Zero.demand ⟨r, h⟩ = demand2650 ⟨r, h⟩

theorem SameRow.congr {a b : ℕ} (e : a = b) {ha : a < 2650} {hb : b < 2650}
    (h : SameRow a ha) : SameRow b hb := by
  subst e
  exact h

theorem chunk0 : ∀ j (hj : j < 128), SameRow (0 + j) (by omega) := by
  decide +kernel

theorem chunk1 : ∀ j (hj : j < 128), SameRow (128 + j) (by omega) := by
  decide +kernel

theorem chunk2 : ∀ j (hj : j < 128), SameRow (256 + j) (by omega) := by
  decide +kernel

theorem chunk3 : ∀ j (hj : j < 128), SameRow (384 + j) (by omega) := by
  decide +kernel

theorem chunk4 : ∀ j (hj : j < 128), SameRow (512 + j) (by omega) := by
  decide +kernel

theorem chunk5 : ∀ j (hj : j < 128), SameRow (640 + j) (by omega) := by
  decide +kernel

theorem chunk6 : ∀ j (hj : j < 128), SameRow (768 + j) (by omega) := by
  decide +kernel

theorem chunk7 : ∀ j (hj : j < 128), SameRow (896 + j) (by omega) := by
  decide +kernel

theorem chunk8 : ∀ j (hj : j < 128), SameRow (1024 + j) (by omega) := by
  decide +kernel

theorem chunk9 : ∀ j (hj : j < 128), SameRow (1152 + j) (by omega) := by
  decide +kernel

theorem chunk10 : ∀ j (hj : j < 128), SameRow (1280 + j) (by omega) := by
  decide +kernel

theorem chunk11 : ∀ j (hj : j < 128), SameRow (1408 + j) (by omega) := by
  decide +kernel

theorem chunk12 : ∀ j (hj : j < 128), SameRow (1536 + j) (by omega) := by
  decide +kernel

theorem chunk13 : ∀ j (hj : j < 128), SameRow (1664 + j) (by omega) := by
  decide +kernel

theorem chunk14 : ∀ j (hj : j < 128), SameRow (1792 + j) (by omega) := by
  decide +kernel

theorem chunk15 : ∀ j (hj : j < 128), SameRow (1920 + j) (by omega) := by
  decide +kernel

theorem chunk16 : ∀ j (hj : j < 128), SameRow (2048 + j) (by omega) := by
  decide +kernel

theorem chunk17 : ∀ j (hj : j < 128), SameRow (2176 + j) (by omega) := by
  decide +kernel

theorem chunk18 : ∀ j (hj : j < 128), SameRow (2304 + j) (by omega) := by
  decide +kernel

theorem chunk19 : ∀ j (hj : j < 128), SameRow (2432 + j) (by omega) := by
  decide +kernel

theorem chunk20 : ∀ j (hj : j < 90), SameRow (2560 + j) (by omega) := by
  decide +kernel

theorem same_row : ∀ r : Fin 2650, SameRow r.val r.isLt := by
  intro ⟨r, hr⟩
  show SameRow r hr
  obtain ⟨k, hk, j, hj, rfl⟩ : ∃ k < 21, ∃ j < 128, r = 128 * k + j :=
    ⟨r / 128, by omega, r % 128, Nat.mod_lt _ (by omega), by omega⟩
  interval_cases k
  · exact SameRow.congr (by omega) (chunk0 j (by omega))
  · exact SameRow.congr (by omega) (chunk1 j (by omega))
  · exact SameRow.congr (by omega) (chunk2 j (by omega))
  · exact SameRow.congr (by omega) (chunk3 j (by omega))
  · exact SameRow.congr (by omega) (chunk4 j (by omega))
  · exact SameRow.congr (by omega) (chunk5 j (by omega))
  · exact SameRow.congr (by omega) (chunk6 j (by omega))
  · exact SameRow.congr (by omega) (chunk7 j (by omega))
  · exact SameRow.congr (by omega) (chunk8 j (by omega))
  · exact SameRow.congr (by omega) (chunk9 j (by omega))
  · exact SameRow.congr (by omega) (chunk10 j (by omega))
  · exact SameRow.congr (by omega) (chunk11 j (by omega))
  · exact SameRow.congr (by omega) (chunk12 j (by omega))
  · exact SameRow.congr (by omega) (chunk13 j (by omega))
  · exact SameRow.congr (by omega) (chunk14 j (by omega))
  · exact SameRow.congr (by omega) (chunk15 j (by omega))
  · exact SameRow.congr (by omega) (chunk16 j (by omega))
  · exact SameRow.congr (by omega) (chunk17 j (by omega))
  · exact SameRow.congr (by omega) (chunk18 j (by omega))
  · exact SameRow.congr (by omega) (chunk19 j (by omega))
  · exact SameRow.congr (by omega) (chunk20 j (by omega))

theorem support_eq : ∀ r, OmissionResidual2650Zero.support r = support2650 r :=
  fun r => (same_row r).1

theorem demand_eq : ∀ r, OmissionResidual2650Zero.demand r = demand2650 r :=
  fun r => (same_row r).2

#print axioms support_eq
#print axioms demand_eq

end OmissionResidual2650ZeroMatch
