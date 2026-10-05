import ErdosSzekeres.HMPT.ConvexFan
import ErdosSzekeres.HMPT.ConvexCounting

namespace ErdosSzekeres.HMPT

open Suk
open scoped BigOperators

/-- A fixed smaller fan determines the projection anchor and the full
alternating anchor sequence. The only additional free endpoint choices are
the three already present in the support-path counting theorem. -/
theorem convexFan_fiber_bound {r n : ℕ} (P : Finset Point)
    (F : Finset (ConvexFan (2 * (r + 3)))) (D : ConvexFan (r + 3))
    (hn : 4 ≤ n) (hgp : GeneralPosition P) (hD : D.vertices ⊆ P)
    (hpoints : ∀ C ∈ F, C.vertices ⊆ P) (heven : ∀ C ∈ F, C.even = D)
    (havoid : ¬ HasConvexNGon n P) :
    F.card ≤ P.card ^ 3 * supportProductBound r n := by
  classical
  let T := (rightRegion P D.anchor).image (projectFrom D.anchor)
  let G := F.image ConvexFan.projected
  have hanchor (C) (hC : C ∈ F) : C.anchor = D.anchor := congrArg ConvexFan.anchor (heven C hC)
  have hinj : Set.InjOn (@ConvexFan.projected (2 * (r + 3))) (F : Set _) := by
    intro C hC E hE h
    exact ConvexFan.eq_of_anchor_projected_eq ((hanchor C hC).trans (hanchor E hE).symm) h
  have hcard : G.card = F.card := Finset.card_image_of_injOn hinj
  have hGT : ∀ q ∈ G, ∀ i, q i ∈ T := by
    intro q hq i
    obtain ⟨C, hC, rfl⟩ := Finset.mem_image.mp hq
    change projectFrom C.anchor (C.point i) ∈ T
    rw [hanchor C hC]
    exact Finset.mem_image_of_mem (projectFrom D.anchor) (mem_rightRegion.mpr
      ⟨hpoints C hC (C.point_mem i), hanchor C hC ▸ C.right i⟩)
  have hanchors : ∀ q ∈ G, evenVertices q = D.projectedAnchors.point := by
    intro q hq
    obtain ⟨C, hC, rfl⟩ := Finset.mem_image.mp hq
    change C.even.projected = D.projected
    rw [heven C hC]
  have hclockwise : ∀ q ∈ G, ∀ i j k, i < j → j < k → orient (q i) (q j) (q k) < 0 := by
    intro q hq
    obtain ⟨C, _, rfl⟩ := Finset.mem_image.mp hq
    exact C.clockwise
  have hright : ∀ p ∈ rightRegion P D.anchor, D.anchor 0 < p 0 :=
    fun _ hp => (mem_rightRegion.mp hp).2
  have hgen := hgp.mono (rightRegion_subset P D.anchor)
  have hgenT : GeneralPosition T := generalPosition_projectFrom D.anchor hgen hright
  have havoidT : ¬ HasConvexNGon n T := fun h =>
    havoid ((hasConvexNGon_of_projectFrom D.anchor hn hgen hright h).mono
      (rightRegion_subset P D.anchor))
  have hDT : ∀ i, D.projectedAnchors.point i ∈ T := by
    intro i
    exact Finset.mem_image_of_mem (projectFrom D.anchor)
      (mem_rightRegion.mpr ⟨hD (D.point_mem i), D.right i⟩)
  have hfiber := support_fiber_card_le T D.projectedAnchors G hGT hanchors hclockwise
  have hprod := support_product_bound D.projectedAnchors D.mono
    (fun i => (D.projectedAnchors.frame i).region T) hn hgenT hDT
    (fun i => (D.projectedAnchors.frame i).region_subset T)
    (fun i p hp => ((D.projectedAnchors.frame i).mem_region T p).mp hp |>.2) havoidT
  have hsize : T.card ≤ P.card :=
    Finset.card_image_le.trans (Finset.card_le_card (rightRegion_subset P D.anchor))
  calc
    F.card = G.card := hcard.symm
    _ ≤ T.card ^ 3 * ∏ i : Fin r, ((D.projectedAnchors.frame i).region T).card := hfiber
    _ ≤ T.card ^ 3 * supportProductBound r n := Nat.mul_le_mul_left _ hprod
    _ ≤ P.card ^ 3 * supportProductBound r n := Nat.mul_le_mul_right _ (Nat.pow_le_pow_left hsize _)

/-- Count a family by its actual smaller convex fans, not all point tuples. -/
theorem convexFan_family_bound {r n : ℕ} (P : Finset Point)
    (F : Finset (ConvexFan (2 * (r + 3)))) (hn : 4 ≤ n) (hgp : GeneralPosition P)
    (hpoints : ∀ C ∈ F, C.vertices ⊆ P) (havoid : ¬ HasConvexNGon n P) :
    F.card ≤ (convexSubsets P (r + 4)).card * (P.card ^ 3 * supportProductBound r n) := by
  classical
  let E := F.image ConvexFan.even
  have hEpoints : ∀ D ∈ E, D.vertices ⊆ P := by
    intro D hD
    obtain ⟨C, hC, rfl⟩ := Finset.mem_image.mp hD
    exact C.even_vertices_subset.trans (hpoints C hC)
  have hEcard : E.card ≤ (convexSubsets P (r + 4)).card := by
    rw [← Finset.card_image_of_injective E (ConvexFan.vertices_injective (r + 3))]
    apply Finset.card_le_card
    intro U hU
    obtain ⟨D, hD, rfl⟩ := Finset.mem_image.mp hU
    exact mem_convexSubsets.mpr ⟨hEpoints D hD, by simpa using D.card_vertices, D.convex⟩
  have hlo : ∀ C ∈ F, 1 ≤ (E.bipartiteAbove (fun C D => C.even = D) C).card := by
    intro C hC
    exact Nat.succ_le_iff.mpr (Finset.card_pos.mpr ⟨C.even,
      (Finset.mem_bipartiteAbove _).mpr ⟨Finset.mem_image_of_mem _ hC, rfl⟩⟩)
  have hhi : ∀ D ∈ E, (F.bipartiteBelow (fun C D => C.even = D) D).card ≤
      P.card ^ 3 * supportProductBound r n := by
    intro D hD
    apply convexFan_fiber_bound P _ D hn hgp (hEpoints D hD)
      (fun C hC => hpoints C ((Finset.mem_bipartiteBelow _).mp hC).1)
      (fun C hC => ((Finset.mem_bipartiteBelow _).mp hC).2) havoid
  have h := Finset.card_mul_le_card_mul
    (fun (C : ConvexFan (2 * (r + 3))) D => C.even = D) hlo hhi
  simp only [mul_one] at h
  exact h.trans (Nat.mul_le_mul_right _ hEcard)

/-- The geometric convex-subset ratio estimate. The three powers of |P|
are explicit endpoint losses of the support path; the anchor choices are
counted by genuine smaller convex subsets with no assumed incidence bound. -/
theorem convex_family_ratio_bound {r n : ℕ} (P : Finset Point) (hn : 4 ≤ n)
    (hgp : GeneralPosition P)
    (hdist : ∀ p ∈ P, ∀ q ∈ P, p 0 = q 0 → p = q)
    (havoid : ¬ HasConvexNGon n P) :
    (convexSubsets P (2 * (r + 3) + 1)).card ≤
      (convexSubsets P (r + 4)).card * (P.card ^ 3 * supportProductBound r n) := by
  obtain ⟨F, hcard, hpoints⟩ := exists_convexFan_family P (2 * (r + 3)) hgp hdist
  rw [← hcard]
  exact convexFan_family_bound P F hn hgp hpoints havoid

end ErdosSzekeres.HMPT
