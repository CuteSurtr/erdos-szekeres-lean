import ErdosSzekeres.Suk.MonochromaticCounting

namespace ErdosSzekeres.Suk

theorem horizontal_positive_transitive {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hx : StrictMono (fun i => p i 0)) :
    TripleTransitive (fun i j k => 0 < orient (p i) (p j) (p k)) := by
  intro i j k l hij hjk hkl hijk hjkl
  exact ⟨orientationDet_pos_pqs_of_pqr_qrs (pointEquiv (p i)) (pointEquiv (p j))
      (pointEquiv (p k)) (pointEquiv (p l)) (hx hij) (hx hjk) (hx hkl) hijk hjkl,
    orientationDet_pos_prs_of_pqr_qrs (pointEquiv (p i)) (pointEquiv (p j))
      (pointEquiv (p k)) (pointEquiv (p l)) (hx hij) (hx hjk) (hx hkl) hijk hjkl⟩

theorem horizontal_nonpositive_transitive {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hx : StrictMono (fun i => p i 0)) :
    TripleTransitive (fun i j k => ¬ 0 < orient (p i) (p j) (p k)) := by
  intro i j k l hij hjk hkl hijk hjkl
  have hx₀ := hx hij
  have hx₁ := hx hjk
  have hx₂ := hx hkl
  have h₀ : orient (p i) (p j) (p k) ≤ 0 := not_lt.mp hijk
  have h₁ : orient (p j) (p k) (p l) ≤ 0 := not_lt.mp hjkl
  have e₀ : (p k 0 - p j 0) * orient (p i) (p j) (p l) =
      (p l 0 - p j 0) * orient (p i) (p j) (p k) +
        (p j 0 - p i 0) * orient (p j) (p k) (p l) := by simp only [orient]; ring
  have e₁ : (p k 0 - p j 0) * orient (p i) (p k) (p l) =
      (p k 0 - p i 0) * orient (p j) (p k) (p l) +
        (p l 0 - p k 0) * orient (p i) (p j) (p k) := by simp only [orient]; ring
  constructor <;> apply not_lt.mpr <;> nlinarith only [e₀, e₁, h₀, h₁, hx₀, hx₁, hx₂]

/-- An unconditional density bound for genuine cups and caps of an
x-ordered real point set in general position. -/
theorem horizontal_cups_caps_density {ι : Type*} [LinearOrder ι]
    (p : ι → Point) (hx : StrictMono (fun i => p i 0)) (s : Finset ι)
    (hgp : GeneralPosition (s.image p)) (k : ℕ) (hk : 3 ≤ k) (hs : 4 ^ k ≤ s.card) :
    s.card.choose k ≤
      ((cliqueSubsets (fun i j l => 0 < orient (p i) (p j) (p l)) s k).card +
        (cliqueSubsets (fun i j l => orient (p i) (p j) (p l) < 0) s k).card) *
          (4 ^ k).choose k := by
  classical
  have hinj : Function.Injective p := fun i j he => hx.injective (congrArg (fun q : Point => q 0) he)
  have heq : cliqueSubsets (fun i j l => ¬ 0 < orient (p i) (p j) (p l)) s k =
      cliqueSubsets (fun i j l => orient (p i) (p j) (p l) < 0) s k := by
    ext u
    simp only [mem_cliqueSubsets]
    constructor
    · rintro ⟨hus, hcard, hc⟩
      refine ⟨hus, hcard, ?_⟩
      intro i hi j hj l hl hij hjl
      have hn := (generalPosition_iff_orient_ne_zero _).mp hgp _
        (Finset.mem_image_of_mem p (hus hi)) _ (Finset.mem_image_of_mem p (hus hj)) _
        (Finset.mem_image_of_mem p (hus hl)) (hinj.ne hij.ne)
        (hinj.ne (hij.trans hjl).ne) (hinj.ne hjl.ne)
      exact lt_of_le_of_ne (not_lt.mp (hc i hi j hj l hl hij hjl)) hn
    · rintro ⟨hus, hcard, hc⟩
      exact ⟨hus, hcard, fun i hi j hj l hl hij hjl =>
        not_lt.mpr (hc i hi j hj l hl hij hjl).le⟩
  simpa only [heq] using monochromatic_subsets_density
    (fun i j l => 0 < orient (p i) (p j) (p l))
    (horizontal_positive_transitive p hx) (horizontal_nonpositive_transitive p hx) s k hk hs

end ErdosSzekeres.Suk
