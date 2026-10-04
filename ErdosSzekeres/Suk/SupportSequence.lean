import ErdosSzekeres.Suk.ChainCase

namespace ErdosSzekeres.Suk

/-- A finite clockwise support sequence. The orientation condition holds for
every increasing triple, as for an ordered cap of a convex support polygon. -/
structure ClockwiseAnchors (m : ℕ) where
  point : Fin m → Point
  clockwise : ∀ i j k, i < j → j < k → orient (point i) (point j) (point k) < 0

/-- The four consecutive anchors around the ith support spike. -/
def ClockwiseAnchors.frame {r : ℕ} (A : ClockwiseAnchors (r + 3)) (i : Fin r) :
    CapFrame where
  a := A.point ⟨i.val, by omega⟩
  b := A.point ⟨i.val + 1, by omega⟩
  c := A.point ⟨i.val + 2, by omega⟩
  d := A.point ⟨i.val + 3, by omega⟩
  abc := A.clockwise _ _ _ (by change i.val < i.val + 1; omega)
    (by change i.val + 1 < i.val + 2; omega)
  abd := A.clockwise _ _ _ (by change i.val < i.val + 1; omega)
    (by change i.val + 1 < i.val + 3; omega)
  acd := A.clockwise _ _ _ (by change i.val < i.val + 2; omega)
    (by change i.val + 2 < i.val + 3; omega)
  bcd := A.clockwise _ _ _ (by change i.val + 1 < i.val + 2; omega)
    (by change i.val + 2 < i.val + 3; omega)

/-- Consecutive windows in one support sequence satisfy the geometric
adjacency conditions used by the gluing theorem. -/
theorem ClockwiseAnchors.adjacent_frames {r : ℕ} (A : ClockwiseAnchors (r + 3))
    (i : ℕ) (hi : i + 1 < r) : ∃ F : AdjacentCapFrames,
      F.left = A.frame ⟨i, by omega⟩ ∧ F.right = A.frame ⟨i + 1, hi⟩ := by
  let F : AdjacentCapFrames := {
    left := A.frame ⟨i, by omega⟩
    e := A.point ⟨i + 4, by omega⟩
    bce := A.clockwise _ _ _ (by change i + 1 < i + 2; omega)
      (by change i + 2 < i + 4; omega)
    bde := A.clockwise _ _ _ (by change i + 1 < i + 3; omega)
      (by change i + 3 < i + 4; omega)
    cde := A.clockwise _ _ _ (by change i + 2 < i + 3; omega)
      (by change i + 3 < i + 4; omega) }
  refine ⟨F, rfl, ?_⟩
  apply CapFrame.ext <;> rfl

/-- The geometric chain case on a finite clockwise sequence of support anchors.
The sequence itself supplies all neighboring-frame hypotheses. -/
theorem ClockwiseAnchors.chain_case {n K r : ℕ} {P : Finset Point}
    (A : ClockwiseAnchors (r + 3)) (C : (i : Fin r) → SpikeChain (A.frame i))
    (hn : 4 ≤ n) (hK : 3 ≤ K) (hreach : n ≤ r * K)
    (hgp : GeneralPosition P) (hanchors : ∀ i, A.point i ∈ P)
    (hpoints : ∀ i, (C i).points ⊆ P)
    (hsize : ∀ i, 2 ^ (n + K - 4) < (C i).length) : HasConvexNGon n P := by
  apply chain_case_of_frames A.frame C hn hK hreach hgp _ hpoints hsize
    A.adjacent_frames
  intro i
  exact ⟨hanchors _, hanchors _⟩

/-- The same chain case stated for finite subsets in the triangle order,
without requiring a chosen ordering or assumed adjacency witnesses. -/
theorem ClockwiseAnchors.chain_case_finsets {n K r : ℕ} {P : Finset Point}
    (A : ClockwiseAnchors (r + 3))
    (s : (i : Fin r) → Finset (AboveBase (A.frame i).outerBase))
    (hn : 4 ≤ n) (hK : 3 ≤ K) (hreach : n ≤ r * K)
    (hgp : GeneralPosition P) (hanchors : ∀ i, A.point i ∈ P)
    (hspike : ∀ i, ∀ p ∈ s i, p.val ∈ (A.frame i).spike)
    (hchain : ∀ i, DilworthTheorem.IsChain (s i : Set (AboveBase (A.frame i).outerBase)))
    (hpoints : ∀ i, (s i).image AboveBase.val ⊆ P)
    (hsize : ∀ i, 2 ^ (n + K - 4) < (s i).card) : HasConvexNGon n P := by
  choose C hlength hsame using fun i =>
    SpikeChain.exists_of_finset (A.frame i) (s i) (hspike i) (hchain i)
  apply A.chain_case C hn hK hreach hgp hanchors
  · intro i
    simpa only [hsame i] using hpoints i
  · intro i
    simpa only [hlength i] using hsize i

end ErdosSzekeres.Suk
