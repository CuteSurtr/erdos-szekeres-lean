import ErdosSzekeres.Omission.CycleGeometry

namespace ErdosSzekeres.Omission

open ActualRanks BalancedCatalog Domains CycleSigns

/-- The cyclic order for row zero of Schroeder's balanced catalog, retained
exactly from ES8CycleData in the version-1 archive (CC BY 4.0). -/
def firstCycle : Fin 8 → Fin 252 := ![0, 4, 8, 15, 25, 37, 27, 18]

def firstSupport : Finset (Fin 252) := {0, 4, 8, 15, 18, 25, 27, 37}

theorem firstCycle_injective : Function.Injective firstCycle := by decide +kernel

theorem firstCycle_image : Finset.univ.image firstCycle = firstSupport := by decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 10000000 in
theorem firstCycle_checked : ∀ i j k : Fin 8, i < j → j < k →
    CheckTriple computedTable (firstCycle i) (firstCycle j) (firstCycle k) = true := by
  decide +kernel

namespace Configuration

theorem firstCycle_not_all_occupied {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    ¬ ∀ i : Fin 8, ∃ v : Fin n, c.balancedOwner noCap noCup v = firstCycle i := by
  classical
  intro full
  let f : Fin 8 → Fin n := fun i => Classical.choose (full i)
  have hf (i : Fin 8) : c.balancedOwner noCap noCup (f i) = firstCycle i :=
    Classical.choose_spec (full i)
  have hinj : Function.Injective f := by
    intro i j h
    apply firstCycle_injective
    rw [← hf i, ← hf j, h]
  have hp : Function.Injective c.point := fun i j h =>
    c.xOrder.injective (congrArg (· 0) h)
  apply noOctagon
  apply hasConvexNGon_of_positive_cycle (by omega) c.point hp ⟨f, hinj⟩
    (fun i => Finset.mem_image_of_mem c.point (Finset.mem_univ _))
  intro i j k hij hjk
  apply c.positive_of_checked_states noCap noCup (f i) (f j) (f k)
    (hinj.ne hij.ne) (hinj.ne hjk.ne) (hinj.ne (hij.trans hjk).ne)
  rw [hf i, hf j, hf k]
  exact firstCycle_checked i j k hij hjk

/-- The first literal omission row is geometrically necessary. This discharges
one actual row, rather than assuming its capacity as an extra hypothesis. -/
theorem first_row_hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point)) :
    1 ≤ (firstSupport \ c.occupied noCap noCup).card := by
  classical
  by_contra h
  have hz : (firstSupport \ c.occupied noCap noCup).card = 0 := by omega
  have hs : firstSupport ⊆ c.occupied noCap noCup :=
    Finset.sdiff_eq_empty_iff_subset.mp (Finset.card_eq_zero.mp hz)
  apply c.firstCycle_not_all_occupied noCap noCup noOctagon
  intro i
  have hm : firstCycle i ∈ firstSupport := by
    rw [← firstCycle_image]
    exact Finset.mem_image_of_mem firstCycle (Finset.mem_univ i)
  obtain ⟨v, _, hv⟩ := Finset.mem_image.mp (hs hm)
  exact ⟨v, hv⟩

end Configuration
end ErdosSzekeres.Omission
