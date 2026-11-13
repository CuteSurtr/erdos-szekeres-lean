import ErdosSzekeres.HMPT.RegionProduct
import ErdosSzekeres.Suk.FiniteBound

namespace ErdosSzekeres.HMPT

open Suk
open scoped BigOperators

/-- The number of possible anchor lists and endpoint choices times the
geometric product bound. All losses in this finite path version are explicit. -/
def productThreshold (N r n : ℕ) : ℕ :=
  N ^ (r + 3) * (N ^ 3 * supportProductBound r n)

/-- Under n-gon avoidance, the geometric product estimate bounds an entire
family of horizontal caps, via its alternating-anchor fibers. -/
theorem cap_family_bound {r n : ℕ} (S : Finset Point)
    (F : Finset (Fin (2 * (r + 3)) → Point)) (hn : 4 ≤ n)
    (hgp : GeneralPosition S) (hpoints : ∀ p ∈ F, ∀ i, p i ∈ S)
    (hmono : ∀ p ∈ F, StrictMono (fun i => p i 0))
    (hclockwise : ∀ p ∈ F, ∀ i j l, i < j → j < l → orient (p i) (p j) (p l) < 0)
    (havoid : ¬ HasConvexNGon n S) : F.card ≤ productThreshold S.card r n := by
  classical
  by_contra! hsize
  obtain ⟨a, _, hlarge⟩ := exists_large_alternating_fiber S F hpoints hsize
  let G := F.filter (fun p => evenVertices p = a)
  obtain ⟨p, hp⟩ := Finset.card_pos.mp (show 0 < G.card from (Nat.zero_le _).trans_lt hlarge)
  have hpF := (Finset.mem_filter.mp hp).1
  let C : ClockwiseAnchors (2 * (r + 3)) := ⟨p, hclockwise p hpF⟩
  let A := C.even
  have hbound := support_fiber_card_le S A G
    (fun q hq => hpoints q (Finset.mem_filter.mp hq).1)
    (fun q hq => (Finset.mem_filter.mp hq).2.trans (Finset.mem_filter.mp hp).2.symm)
    (fun q hq => hclockwise q (Finset.mem_filter.mp hq).1)
  have hxA : StrictMono (fun i => A.point i 0) := by
    intro i j hij
    apply hmono p hpF
    change 2 * i.val < 2 * j.val
    omega
  have hprod := support_product_bound A hxA (fun i => (A.frame i).region S) hn hgp
    (fun _ => hpoints p hpF _) (fun i => (A.frame i).region_subset S)
    (fun i q hq => ((A.frame i).mem_region S q).mp hq |>.2) havoid
  exact (not_lt_of_ge (hbound.trans (Nat.mul_le_mul_left _ hprod))) hlarge

theorem hasConvexNGon_of_many_caps {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hx : StrictMono (fun i => p i 0)) (s : Finset ι)
    {r n : ℕ} (hn : 4 ≤ n) (hgp : GeneralPosition (s.image p))
    (hsize : productThreshold s.card r n <
      (cliqueSubsets (fun i j l => orient (p i) (p j) (p l) < 0) s (2 * (r + 3))).card) :
    HasConvexNGon n (s.image p) := by
  classical
  by_contra havoid
  obtain ⟨F, hcard, hpoints, hmono, hclockwise⟩ :=
    ordered_clique_family p hx (fun a b c => orient a b c < 0) s (2 * (r + 3))
  have hinj : Function.Injective p := fun i j he =>
    hx.injective (congrArg (fun q : Point => q 0) he)
  have h := cap_family_bound (s.image p) F hn hgp hpoints hmono hclockwise havoid
  rw [Finset.card_image_of_injective s hinj, hcard] at h
  exact (not_lt_of_ge h) hsize

/-- The product argument for an arbitrary horizontally ordered point set.
Density and reflection provide the cap family, so no extraction hypothesis remains. -/
theorem horizontal_finite_product_bound {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hx : StrictMono (fun i => p i 0)) (s : Finset ι)
    {r n : ℕ} (hn : 4 ≤ n) (hgp : GeneralPosition (s.image p))
    (hs : 4 ^ (2 * (r + 3)) ≤ s.card)
    (hsize : 2 * productThreshold s.card r n *
      (4 ^ (2 * (r + 3))).choose (2 * (r + 3)) < s.card.choose (2 * (r + 3))) :
    HasConvexNGon n (s.image p) := by
  classical
  let D := productThreshold s.card r n
  let L := 2 * (r + 3)
  have hdensity := horizontal_cups_caps_density p hx s hgp L (by dsimp [L]; omega) hs
  have hlarge : D < (cliqueSubsets (fun i j l => orient (p i) (p j) (p l) < 0) s L).card ∨
      D < (cliqueSubsets (fun i j l => 0 < orient (p i) (p j) (p l)) s L).card := by
    by_contra! h
    have hc := Nat.mul_le_mul_right ((4 ^ L).choose L) (show
      (cliqueSubsets (fun i j l => 0 < orient (p i) (p j) (p l)) s L).card +
        (cliqueSubsets (fun i j l => orient (p i) (p j) (p l) < 0) s L).card ≤ 2 * D
      from by omega)
    exact (not_lt_of_ge (hdensity.trans hc)) hsize
  rcases hlarge with hc | hc
  · exact hasConvexNGon_of_many_caps p hx s hn hgp hc
  · have hr : HasConvexNGon n (s.image (fun i => reflectY (p i))) := by
      apply hasConvexNGon_of_many_caps (fun i => reflectY (p i))
        (by simpa only [reflectY_x] using hx) s hn
      · simpa only [Finset.image_image, Function.comp_def] using generalPosition_reflectY hgp
      · simpa only [orient_reflectY, neg_lt_zero] using hc
    apply hasConvexNGon_of_reflectY
    simpa only [Finset.image_image, Function.comp_def] using hr

/-- An unconditional real-plane bound from the product method. Its hypotheses
are finite integer inequalities only. The published asymptotic coefficient is
a separate target, requiring sharper density and optimization estimates. -/
theorem finite_product_bound {N r n : ℕ} (hn : 4 ≤ n)
    (hs : 4 ^ (2 * (r + 3)) ≤ N)
    (hsize : 2 * productThreshold N r n *
      (4 ^ (2 * (r + 3))).choose (2 * (r + 3)) < N.choose (2 * (r + 3))) :
    ForcesConvexNGon N n := by
  classical
  apply (forcesConvexNGon_iff_exact N n).mpr
  intro S hgp hcard
  obtain ⟨e, hgpT, hxT⟩ := exists_horizontal_image S hgp
  let T := S.image e
  have hTcard : T.card = N := by
    simpa only [T, Finset.card_image_of_injective S e.injective] using hcard
  have hxinj : Function.Injective (fun p : T => p.val 0) := by
    intro p q he
    exact Subtype.ext (hxT p.val p.property q.val q.property he)
  let order : LinearOrder T := LinearOrder.lift' (fun p : T => p.val 0) hxinj
  letI := order
  have hx : @StrictMono T ℝ order.toPreorder _ (fun p : T => p.val 0) := fun _ _ h => h
  have himage : (Finset.univ : Finset T).image Subtype.val = T := by
    ext p
    simp
  have hucard : (Finset.univ : Finset T).card = N := by simpa using hTcard
  have hpoly : HasConvexNGon n T := by
    rw [← himage]
    apply horizontal_finite_product_bound (fun p : T => p.val) hx Finset.univ hn
    · simpa only [himage] using hgpT
    · simpa only [hucard] using hs
    · simpa only [hucard] using hsize
  have hback := hpoly.linearEquiv e.symm
  simpa [T, Finset.image_image, Function.comp_def] using hback

end ErdosSzekeres.HMPT
