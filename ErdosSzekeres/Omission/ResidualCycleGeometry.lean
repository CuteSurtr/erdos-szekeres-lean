import ErdosSzekeres.Omission.CycleSigns
import ErdosSzekeres.Omission.ResidualRealization
import ErdosSzekeres.Omission.ResidualBoxes
import ErdosSzekeres.ConvexCycleCuts
import Mathlib.Data.Finset.Sort

namespace ErdosSzekeres.Omission

open ResidualRanks ResidualCatalog ResidualDomains CycleSigns Subsets

namespace Configuration

noncomputable def residualOccupied {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) : Finset (Fin 154) :=
  Finset.univ.image (c.residualOwner noCap noOctagon noJunction)

theorem residual_occupied_card {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n)) :
    (c.residualOccupied noCap noOctagon noJunction).card = n := by
  simp [residualOccupied, Finset.card_image_of_injective _ (c.residualOwner_injective noCap noOctagon noJunction)]

/-- A checked triple of state indices forces positive orientation of its actual
owners, regardless of their chronological order. -/
theorem residual_positive_of_checked_states {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n))
    (u v w : Fin n) (huv : u ≠ v) (hvw : v ≠ w) (huw : u ≠ w)
    (checked : CheckTriple computedTable (c.residualOwner noCap noOctagon noJunction u)
      (c.residualOwner noCap noOctagon noJunction v) (c.residualOwner noCap noOctagon noJunction w) = true) :
    0 < orient (c.point u) (c.point v) (c.point w) := by
  apply checked_triple_positive n computedTable
    (fun i => (c.residualOwner noCap noOctagon noJunction i).val) c.cup (labels n c.cup) c.point
    (labels_increasing n c.cup (fun h => noCap (ListGeometry.hasCap_of_list c h))) ?_ ?_ c.generalPosition u v w huv hvw huw checked
  · intro a b hab
    exact actual_pair_fits n c.cup (fun h => noCap (ListGeometry.hasCap_of_list c h))
      (c.residual_avoids_cup noOctagon) (noJunction_of_lists n c.cup noJunction)
      a b hab _ (computedTable_valid _ _)
  · intro a b d _ _
    exact c.cup_true_iff a b d

/-- Every occupied subsequence of a checked cycle is convex. In an octagon-free
configuration it therefore contains at most seven actual owners. -/
theorem residual_checked_cycle_capacity {n k : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n))
    (e : Fin k → Fin 154) (he : Function.Injective e)
    (checked : ∀ i j l : Fin k, i < j → j < l →
      CheckTriple computedTable (e i) (e j) (e l) = true) :
    ((Finset.univ.image e) ∩ c.residualOccupied noCap noOctagon noJunction).card ≤ 7 := by
  classical
  let selected := Finset.univ.filter (fun i : Fin k => e i ∈ c.residualOccupied noCap noOctagon noJunction)
  have image_eq : selected.image e = (Finset.univ.image e) ∩ c.residualOccupied noCap noOctagon noJunction := by
    ext z
    simp only [selected, Finset.mem_image, Finset.mem_filter, Finset.mem_univ,
      true_and, Finset.mem_inter]
    constructor
    · rintro ⟨i, hi, rfl⟩
      exact ⟨⟨i, rfl⟩, hi⟩
    · rintro ⟨⟨i, rfl⟩, hi⟩
      exact ⟨i, hi, rfl⟩
  rw [← image_eq, Finset.card_image_of_injective _ he]
  by_contra h
  have h8 : 8 ≤ selected.card := by omega
  let t : Fin 8 → Fin k := fun i => selected.orderEmbOfFin rfl ⟨i.val, by omega⟩
  have ht : StrictMono t := by
    intro i j hij
    exact (selected.orderEmbOfFin rfl).strictMono hij
  have full (i : Fin 8) : ∃ v : Fin n, c.residualOwner noCap noOctagon noJunction v = e (t i) := by
    have hm := selected.orderEmbOfFin_mem rfl (⟨i.val, by omega⟩ : Fin selected.card)
    have ho : e (t i) ∈ c.residualOccupied noCap noOctagon noJunction := (Finset.mem_filter.mp hm).2
    obtain ⟨v, _, hv⟩ := Finset.mem_image.mp ho
    exact ⟨v, hv⟩
  let f : Fin 8 → Fin n := fun i => Classical.choose (full i)
  have hf (i : Fin 8) : c.residualOwner noCap noOctagon noJunction (f i) = e (t i) :=
    Classical.choose_spec (full i)
  have hinj : Function.Injective f := by
    intro i j h
    apply ht.injective
    apply he
    rw [← hf i, ← hf j, h]
  have hp : Function.Injective c.point := fun i j h =>
    c.xOrder.injective (congrArg (· 0) h)
  apply noOctagon
  apply hasConvexNGon_of_positive_cycle (by omega) c.point hp ⟨f, hinj⟩
    (fun _ => Finset.mem_image_of_mem c.point (Finset.mem_univ _))
  intro i j l hij hjl
  apply c.residual_positive_of_checked_states noCap noOctagon noJunction (f i) (f j) (f l)
    (hinj.ne hij.ne) (hinj.ne hjl.ne) (hinj.ne (hij.trans hjl).ne)
  rw [hf i, hf j, hf l]
  exact checked (t i) (t j) (t l) (ht hij) (ht hjl)

theorem residual_checked_cycle_hole_bound {n k : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n))
    (e : Fin k → Fin 154) (he : Function.Injective e)
    (checked : ∀ i j l : Fin k, i < j → j < l →
      CheckTriple computedTable (e i) (e j) (e l) = true) :
    k - 7 ≤ ((Finset.univ.image e) \ c.residualOccupied noCap noOctagon noJunction).card := by
  have cap := c.residual_checked_cycle_capacity noCap noOctagon noJunction e he checked
  have count := Finset.card_sdiff_add_card_inter (Finset.univ.image e) (c.residualOccupied noCap noOctagon noJunction)
  have size : (Finset.univ.image e).card = k := by
    simp [Finset.card_image_of_injective _ he]
  omega

end Configuration

/-- The finite condition checked for each literal row. -/
def ResidualCycleValid (ids : List (Fin 154)) : Prop :=
  Function.Injective ids.get ∧ ∀ i j k : Fin ids.length, i < j → j < k →
    CheckTriple computedTable (ids.get i) (ids.get j) (ids.get k) = true

instance (ids : List (Fin 154)) : Decidable (ResidualCycleValid ids) := by
  unfold ResidualCycleValid
  infer_instance

theorem Configuration.residual_list_cycle_hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : NoJunctionOn c.cup (Finset.range n))
    (ids : List (Fin 154)) (checked : ResidualCycleValid ids) :
    ids.length - 7 ≤ (ids.toFinset \ c.residualOccupied noCap noOctagon noJunction).card := by
  have hi : Finset.univ.image ids.get = ids.toFinset := by
    ext x
    simp [List.mem_iff_get]
  simpa only [hi] using c.residual_checked_cycle_hole_bound noCap noOctagon noJunction
    ids.get checked.1 checked.2

end ErdosSzekeres.Omission
