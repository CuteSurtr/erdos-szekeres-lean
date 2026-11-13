import ErdosSzekeres.Suk.DenseCapExtraction
import ErdosSzekeres.Suk.OrderedCounting
import ErdosSzekeres.Suk.Reflection

namespace ErdosSzekeres.Suk

/-- The exact finite family threshold used in the alternating-anchor proof. -/
def extractionThreshold (N m k B : ℕ) : ℕ :=
  N ^ (m + 3) * (N ^ 3 * (B ^ (m - k - 2) * N ^ (k + 2)))

/-- Dense horizontal caps feed directly into the checked finite geometric engine. -/
theorem hasConvexNGon_of_many_caps {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hx : StrictMono (fun i => p i 0)) (s : Finset ι)
    {m k n K r t b : ℕ} (hkm : k + 2 ≤ m)
    (hn : 4 ≤ n) (hK : 3 ≤ K) (hb : 3 ≤ b)
    (hchainreach : n ≤ r * K) (hantireach : n ≤ t * b) (hregions : t * (r + 1) ≤ k)
    (hgp : GeneralPosition (s.image p))
    (hsize : extractionThreshold s.card m k
        (2 ^ (n + K - 4) * (n + b - 4).choose (n - 2)) <
      (cliqueSubsets (fun i j l => orient (p i) (p j) (p l) < 0) s (2 * (m + 3))).card) :
    HasConvexNGon n (s.image p) := by
  classical
  obtain ⟨F, hcard, hpoints, hmono, hclockwise⟩ :=
    ordered_clique_family p hx (fun a b c => orient a b c < 0) s (2 * (m + 3))
  have hinj : Function.Injective p := fun i j he =>
    hx.injective (congrArg (fun q : Point => q 0) he)
  obtain ⟨A, Q, hxA, hA, hQ, hspike, hlarge⟩ :=
    rich_support_of_dense_caps (s.image p) F hkm hpoints hmono hclockwise
      (by simpa only [Finset.card_image_of_injective s hinj, hcard, extractionThreshold]
        using hsize)
  exact A.finite_support_bound hxA Q hn hK hb hchainreach hantireach hregions
    hgp hA hQ hspike hlarge

/-- A finite numerical sufficient condition, with no support configuration or
cap-family assumptions. Reflection handles whichever color is denser. -/
theorem horizontal_finite_density_bound {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hx : StrictMono (fun i => p i 0)) (s : Finset ι)
    {m k n K r t b : ℕ} (hkm : k + 2 ≤ m)
    (hn : 4 ≤ n) (hK : 3 ≤ K) (hb : 3 ≤ b)
    (hchainreach : n ≤ r * K) (hantireach : n ≤ t * b) (hregions : t * (r + 1) ≤ k)
    (hgp : GeneralPosition (s.image p)) (hs : 4 ^ (2 * (m + 3)) ≤ s.card)
    (hsize : 2 * extractionThreshold s.card m k
        (2 ^ (n + K - 4) * (n + b - 4).choose (n - 2)) *
          (4 ^ (2 * (m + 3))).choose (2 * (m + 3)) < s.card.choose (2 * (m + 3))) :
    HasConvexNGon n (s.image p) := by
  classical
  let D := extractionThreshold s.card m k
    (2 ^ (n + K - 4) * (n + b - 4).choose (n - 2))
  let L := 2 * (m + 3)
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
  · exact hasConvexNGon_of_many_caps p hx s hkm hn hK hb hchainreach hantireach hregions hgp hc
  · have hr : HasConvexNGon n (s.image (fun i => reflectY (p i))) := by
      apply hasConvexNGon_of_many_caps (fun i => reflectY (p i))
        (by simpa only [reflectY_x] using hx) s hkm hn hK hb hchainreach hantireach hregions
      · simpa only [Finset.image_image, Function.comp_def] using generalPosition_reflectY hgp
      · simpa only [orient_reflectY, neg_lt_zero] using hc
    apply hasConvexNGon_of_reflectY
    simpa only [Finset.image_image, Function.comp_def] using hr

end ErdosSzekeres.Suk
