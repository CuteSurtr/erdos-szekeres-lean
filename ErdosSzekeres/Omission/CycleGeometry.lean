import ErdosSzekeres.Omission.CycleSigns
import ErdosSzekeres.Omission.Realization
import ErdosSzekeres.ConvexCycleCuts
import Mathlib.Data.Finset.Sort

namespace ErdosSzekeres.Omission

open ActualRanks BalancedCatalog Domains CycleSigns

namespace Configuration

noncomputable def occupied {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7) : Finset (Fin 252) :=
  Finset.univ.image (c.balancedOwner noCap noCup)

theorem occupied_card {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7) :
    (c.occupied noCap noCup).card = n := by
  simp [occupied, Finset.card_image_of_injective _ (c.balancedOwner_injective noCap noCup)]

/-- A checked triple of state indices forces positive orientation of its actual
owners, regardless of their chronological order. -/
theorem positive_of_checked_states {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (u v w : Fin n) (huv : u ≠ v) (hvw : v ≠ w) (huw : u ≠ w)
    (checked : CheckTriple computedTable (c.balancedOwner noCap noCup u)
      (c.balancedOwner noCap noCup v) (c.balancedOwner noCap noCup w) = true) :
    0 < orient (c.point u) (c.point v) (c.point w) := by
  apply checked_triple_positive n computedTable
    (fun i => (c.balancedOwner noCap noCup i).val) c.cup (labels c.cup) c.point
    (labels_increasing n c.cup) ?_ ?_ c.generalPosition u v w huv hvw huw checked
  · intro a b hab
    exact actual_pair_fits n c.cup (c.avoids_of_noCap noCap) (c.avoids_of_noCup noCup)
      a b hab _ (computedTable_valid _ _)
  · intro a b d _ _
    exact c.cup_true_iff a b d

/-- Every occupied subsequence of a checked cycle is convex. In an octagon-free
configuration it therefore contains at most seven actual owners. -/
theorem checked_cycle_capacity {n k : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (e : Fin k → Fin 252) (he : Function.Injective e)
    (checked : ∀ i j l : Fin k, i < j → j < l →
      CheckTriple computedTable (e i) (e j) (e l) = true) :
    ((Finset.univ.image e) ∩ c.occupied noCap noCup).card ≤ 7 := by
  classical
  let selected := Finset.univ.filter (fun i : Fin k => e i ∈ c.occupied noCap noCup)
  have image_eq : selected.image e = (Finset.univ.image e) ∩ c.occupied noCap noCup := by
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
  have full (i : Fin 8) : ∃ v : Fin n, c.balancedOwner noCap noCup v = e (t i) := by
    have hm := selected.orderEmbOfFin_mem rfl (⟨i.val, by omega⟩ : Fin selected.card)
    have ho : e (t i) ∈ c.occupied noCap noCup := (Finset.mem_filter.mp hm).2
    obtain ⟨v, _, hv⟩ := Finset.mem_image.mp ho
    exact ⟨v, hv⟩
  let f : Fin 8 → Fin n := fun i => Classical.choose (full i)
  have hf (i : Fin 8) : c.balancedOwner noCap noCup (f i) = e (t i) :=
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
  apply c.positive_of_checked_states noCap noCup (f i) (f j) (f l)
    (hinj.ne hij.ne) (hinj.ne hjl.ne) (hinj.ne (hij.trans hjl).ne)
  rw [hf i, hf j, hf l]
  exact checked (t i) (t j) (t l) (ht hij) (ht hjl)

theorem checked_cycle_hole_bound {n k : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (e : Fin k → Fin 252) (he : Function.Injective e)
    (checked : ∀ i j l : Fin k, i < j → j < l →
      CheckTriple computedTable (e i) (e j) (e l) = true) :
    k - 7 ≤ ((Finset.univ.image e) \ c.occupied noCap noCup).card := by
  have cap := c.checked_cycle_capacity noCap noCup noOctagon e he checked
  have count := Finset.card_sdiff_add_card_inter (Finset.univ.image e) (c.occupied noCap noCup)
  have size : (Finset.univ.image e).card = k := by
    simp [Finset.card_image_of_injective _ he]
  omega

end Configuration

/-- The finite condition checked for each literal row. -/
def CycleValid (ids : List (Fin 252)) : Prop :=
  Function.Injective ids.get ∧ ∀ i j k : Fin ids.length, i < j → j < k →
    CheckTriple computedTable (ids.get i) (ids.get j) (ids.get k) = true

instance (ids : List (Fin 252)) : Decidable (CycleValid ids) := by
  unfold CycleValid
  infer_instance

theorem Configuration.list_cycle_hole_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (ids : List (Fin 252)) (checked : CycleValid ids) :
    ids.length - 7 ≤ (ids.toFinset \ c.occupied noCap noCup).card := by
  have hi : Finset.univ.image ids.get = ids.toFinset := by
    ext x
    simp [List.mem_iff_get]
  simpa only [hi] using c.checked_cycle_hole_bound noCap noCup noOctagon
    ids.get checked.1 checked.2

end ErdosSzekeres.Omission
