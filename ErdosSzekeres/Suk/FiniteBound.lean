import ErdosSzekeres.Suk.FiniteDensityBound
import ErdosSzekeres.Suk.CoordinateNormalization

namespace ErdosSzekeres.Suk

/-- An unconditional finite Erdős–Szekeres bound from explicit integer
inequalities. The geometric positive-fraction extraction, coordinate changes,
and chain/antichain cases are all internal to the proof. -/
theorem finite_density_bound {N m k n K r t b : ℕ}
    (hkm : k + 2 ≤ m) (hn : 4 ≤ n) (hK : 3 ≤ K) (hb : 3 ≤ b)
    (hchainreach : n ≤ r * K) (hantireach : n ≤ t * b) (hregions : t * (r + 1) ≤ k)
    (hs : 4 ^ (2 * (m + 3)) ≤ N)
    (hsize : 2 * extractionThreshold N m k
        (2 ^ (n + K - 4) * (n + b - 4).choose (n - 2)) *
          (4 ^ (2 * (m + 3))).choose (2 * (m + 3)) < N.choose (2 * (m + 3))) :
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
    apply horizontal_finite_density_bound (fun p : T => p.val) hx Finset.univ
      hkm hn hK hb hchainreach hantireach hregions
    · simpa only [himage] using hgpT
    · simpa only [hucard] using hs
    · simpa only [hucard] using hsize
  have hback := hpoly.linearEquiv e.symm
  simpa [T, Finset.image_image, Function.comp_def] using hback

end ErdosSzekeres.Suk
