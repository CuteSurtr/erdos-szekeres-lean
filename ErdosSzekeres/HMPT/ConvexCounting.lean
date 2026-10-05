import ErdosSzekeres.HMPT.ProjectedCaps
import ErdosSzekeres.HMPT.FiniteBound

namespace ErdosSzekeres.HMPT

open Suk

noncomputable def rightRegion (P : Finset Point) (a : Point) : Finset Point := by
  classical
  exact P.filter (fun p => a 0 < p 0)

@[simp] theorem mem_rightRegion {P : Finset Point} {a p : Point} :
    p ∈ rightRegion P a ↔ p ∈ P ∧ a 0 < p 0 := by
  classical
  simp [rightRegion]

theorem rightRegion_subset (P : Finset Point) (a : Point) : rightRegion P a ⊆ P :=
  fun _ hp => (mem_rightRegion.mp hp).1

/-- A uniform convex family with the same leftmost vertex becomes a family
of horizontal caps. The map of families is injective and preserves the count. -/
theorem projected_cap_family {L : ℕ} (P : Finset Point) (a : Point)
    (F : Finset (Finset Point)) (hgp : GeneralPosition P)
    (hF : ∀ U ∈ F, U ⊆ P ∧ U.card = L + 1 ∧ ConvexPosition U)
    (ha : ∀ U ∈ F, a ∈ U)
    (hx : ∀ U ∈ F, ∀ p ∈ U, p ≠ a → a 0 < p 0) :
    ∃ G : Finset (Fin L → Point), G.card = F.card ∧
      (∀ q ∈ G, ∀ i, q i ∈ (rightRegion P a).image (projectFrom a)) ∧
      (∀ q ∈ G, StrictMono (fun i => q i 0)) ∧
      ∀ q ∈ G, ∀ i j k, i < j → j < k → orient (q i) (q j) (q k) < 0 := by
  classical
  have hchoose (U : F) : ∃ p : Fin L → Point,
      Finset.univ.image p = U.val.erase a ∧ Function.Injective p ∧
      StrictMono (fun i => projectFrom a (p i) 0) ∧
      ∀ i j k, i < j → j < k →
        orient (projectFrom a (p i)) (projectFrom a (p j)) (projectFrom a (p k)) < 0 := by
    have hcard : (U.val.erase a).card = L := by
      rw [Finset.card_erase_of_mem (ha U.val U.property), (hF U.val U.property).2.1]
      omega
    have h := exists_projected_cap (S := U.val.erase a) a
      (by rw [Finset.insert_erase (ha U.val U.property)]; exact hgp.mono (hF U.val U.property).1)
      (by rw [Finset.insert_erase (ha U.val U.property)]; exact (hF U.val U.property).2.2)
      (fun p hp => hx U.val U.property p (Finset.mem_erase.mp hp).2 (Finset.mem_erase.mp hp).1)
    rw [← hcard]
    exact h
  choose p himage hinj hmono hclockwise using hchoose
  have hmem (U : F) (i : Fin L) : p U i ∈ U.val ∧ p U i ≠ a := by
    have h : p U i ∈ U.val.erase a := himage U ▸ Finset.mem_image_of_mem (p U) (Finset.mem_univ i)
    exact ⟨(Finset.mem_erase.mp h).2, (Finset.mem_erase.mp h).1⟩
  let f : F → (Fin L → Point) := fun U i => projectFrom a (p U i)
  have hf : Function.Injective f := by
    intro U V he
    have hp : p U = p V := by
      funext i
      exact projectFrom_injOn a
        (hx U.val U.property _ (hmem U i).1 (hmem U i).2)
        (hx V.val V.property _ (hmem V i).1 (hmem V i).2) (congrFun he i)
    have herase : U.val.erase a = V.val.erase a := by rw [← himage U, ← himage V, hp]
    apply Subtype.ext
    calc
      U.val = insert a (U.val.erase a) := (Finset.insert_erase (ha U.val U.property)).symm
      _ = insert a (V.val.erase a) := congrArg (insert a) herase
      _ = V.val := Finset.insert_erase (ha V.val V.property)
  refine ⟨F.attach.image f, ?_, ?_, ?_, ?_⟩
  · rw [Finset.card_image_of_injective _ hf, Finset.card_attach]
  · intro q hq i
    obtain ⟨U, _, rfl⟩ := Finset.mem_image.mp hq
    exact Finset.mem_image_of_mem (projectFrom a) (mem_rightRegion.mpr
      ⟨(hF U.val U.property).1 (hmem U i).1,
        hx U.val U.property _ (hmem U i).1 (hmem U i).2⟩)
  · intro q hq
    obtain ⟨U, _, rfl⟩ := Finset.mem_image.mp hq
    exact hmono U
  · intro q hq
    obtain ⟨U, _, rfl⟩ := Finset.mem_image.mp hq
    exact hclockwise U

/-- The support-path product theorem now bounds genuine convex polygons
sharing a leftmost vertex, using projective normalization and its checked inverse. -/
theorem anchored_convex_family_bound {r n : ℕ} (P : Finset Point) (a : Point)
    (F : Finset (Finset Point)) (hn : 4 ≤ n) (hgp : GeneralPosition P)
    (hF : ∀ U ∈ F, U ⊆ P ∧ U.card = 2 * (r + 3) + 1 ∧ ConvexPosition U)
    (ha : ∀ U ∈ F, a ∈ U)
    (hx : ∀ U ∈ F, ∀ p ∈ U, p ≠ a → a 0 < p 0)
    (havoid : ¬ HasConvexNGon n P) : F.card ≤ productThreshold P.card r n := by
  classical
  obtain ⟨G, hcard, hpoints, hmono, hclockwise⟩ := projected_cap_family P a F hgp hF ha hx
  have hright : ∀ p ∈ rightRegion P a, a 0 < p 0 := fun _ hp => (mem_rightRegion.mp hp).2
  have hgen := hgp.mono (rightRegion_subset P a)
  have hbound := cap_family_bound ((rightRegion P a).image (projectFrom a)) G hn
    (generalPosition_projectFrom a hgen hright) hpoints hmono hclockwise
    (fun h => havoid ((hasConvexNGon_of_projectFrom a hn hgen hright h).mono (rightRegion_subset P a)))
  rw [hcard] at hbound
  have hsize : ((rightRegion P a).image (projectFrom a)).card ≤ P.card :=
    Finset.card_image_le.trans (Finset.card_le_card (rightRegion_subset P a))
  apply hbound.trans
  unfold productThreshold
  gcongr

/-- Count all convex subsets by their leftmost vertex. This establishes the
general convex-subset bridge needed for bootstrapping a known ES upper bound;
the stronger two-scale ratio estimate is separate. -/
theorem convex_family_bound {r n : ℕ} (P : Finset Point) (hn : 4 ≤ n)
    (hgp : GeneralPosition P)
    (hdist : ∀ p ∈ P, ∀ q ∈ P, p 0 = q 0 → p = q)
    (havoid : ¬ HasConvexNGon n P) :
    (convexSubsets P (2 * (r + 3) + 1)).card ≤ P.card * productThreshold P.card r n := by
  classical
  let F := convexSubsets P (2 * (r + 3) + 1)
  let R : Finset Point → Point → Prop := fun U a => a ∈ U ∧ ∀ p ∈ U, a 0 ≤ p 0
  have hlo : ∀ U ∈ F, 1 ≤ (P.bipartiteAbove R U).card := by
    intro U hU
    have hu := mem_convexSubsets.mp hU
    obtain ⟨a, ha, hmin⟩ := Finset.exists_min_image U (fun p => p 0)
      (Finset.card_pos.mp (by have := hu.2.1; omega))
    exact Nat.succ_le_iff.mpr (Finset.card_pos.mpr
      ⟨a, (Finset.mem_bipartiteAbove R).mpr ⟨hu.1 ha, ha, hmin⟩⟩)
  have hhi : ∀ a ∈ P, (F.bipartiteBelow R a).card ≤ productThreshold P.card r n := by
    intro a haP
    apply anchored_convex_family_bound P a (F.bipartiteBelow R a) hn hgp
    · intro U hU
      exact mem_convexSubsets.mp ((Finset.mem_bipartiteBelow R).mp hU).1
    · intro U hU
      exact ((Finset.mem_bipartiteBelow R).mp hU).2.1
    · intro U hU p hp hpa
      obtain ⟨hUF, ha, hmin⟩ := (Finset.mem_bipartiteBelow R).mp hU
      apply lt_of_le_of_ne (hmin p hp)
      intro he
      exact hpa (hdist p ((mem_convexSubsets.mp hUF).1 hp) a haP he.symm)
    · exact havoid
  simpa only [mul_one] using Finset.card_mul_le_card_mul R hlo hhi

end ErdosSzekeres.HMPT
