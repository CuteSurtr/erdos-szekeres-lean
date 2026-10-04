import ErdosSzekeres.Suk.HorizontalCounting
import Mathlib.Data.Finset.Sort

namespace ErdosSzekeres.Suk

/-- Enumerating a uniform family in increasing order preserves its cardinality.
This bridges the subset density count to the point sequences used by extraction. -/
theorem ordered_clique_family {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hx : StrictMono (fun i => p i 0))
    (R : Point → Point → Point → Prop) (s : Finset ι) (L : ℕ) :
    ∃ F : Finset (Fin L → Point),
      F.card = (cliqueSubsets (fun i j k => R (p i) (p j) (p k)) s L).card ∧
      (∀ q ∈ F, ∀ i, q i ∈ s.image p) ∧
      (∀ q ∈ F, StrictMono (fun i => q i 0)) ∧
      ∀ q ∈ F, ∀ i j k, i < j → j < k → R (q i) (q j) (q k) := by
  classical
  let U := cliqueSubsets (fun i j k => R (p i) (p j) (p k)) s L
  have hcard (u : U) : u.val.card = L := (mem_cliqueSubsets.mp u.property).2.1
  let f : U → (Fin L → Point) := fun u i => p (u.val.orderEmbOfFin (hcard u) i)
  have hinj : Function.Injective p := fun i j he =>
    hx.injective (congrArg (fun q : Point => q 0) he)
  have hf : Function.Injective f := by
    intro u v he
    have he' : (u.val.orderEmbOfFin (hcard u) : Fin L → ι) =
        v.val.orderEmbOfFin (hcard v) := by
      funext i
      exact hinj (congrFun he i)
    apply Subtype.ext
    rw [← Finset.image_orderEmbOfFin_univ u.val (hcard u),
      ← Finset.image_orderEmbOfFin_univ v.val (hcard v), he']
  refine ⟨U.attach.image f, ?_, ?_, ?_, ?_⟩
  · rw [Finset.card_image_of_injective _ hf, Finset.card_attach]
  · intro q hq i
    obtain ⟨u, _, rfl⟩ := Finset.mem_image.mp hq
    exact Finset.mem_image_of_mem p ((mem_cliqueSubsets.mp u.property).1
      (Finset.orderEmbOfFin_mem _ (hcard u) i))
  · intro q hq
    obtain ⟨u, _, rfl⟩ := Finset.mem_image.mp hq
    exact hx.comp (u.val.orderEmbOfFin (hcard u)).strictMono
  · intro q hq i j k hij hjk
    obtain ⟨u, _, rfl⟩ := Finset.mem_image.mp hq
    exact (mem_cliqueSubsets.mp u.property).2.2 _
      (Finset.orderEmbOfFin_mem _ (hcard u) i) _
      (Finset.orderEmbOfFin_mem _ (hcard u) j) _
      (Finset.orderEmbOfFin_mem _ (hcard u) k)
      ((u.val.orderEmbOfFin (hcard u)).strictMono hij)
      ((u.val.orderEmbOfFin (hcard u)).strictMono hjk)

end ErdosSzekeres.Suk
