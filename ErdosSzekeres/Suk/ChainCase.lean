import ErdosSzekeres.Suk.CapGrowth
import ErdosSzekeres.Suk.SpikeChain

namespace ErdosSzekeres.Suk

/-- Cardinality-aware gluing with an explicit neighboring-frame witness. -/
theorem glue_neighboring_chain_caps {F G : CapFrame}
    (C : SpikeChain F) (D : SpikeChain G)
    (hneighbor : ∃ A : AdjacentCapFrames, A.left = F ∧ A.right = G)
    {P : Finset Point} (hgp : GeneralPosition P) (hanchor : F.c ∈ P)
    (hC : C.points ⊆ P) (hD : D.points ⊆ P)
    {a b n : ℕ} (hn : 4 ≤ n) (hsize : n ≤ a + b)
    (hc : C.LeftCap a) (hd : D.RightCap b) : HasConvexNGon n P := by
  obtain ⟨A, rfl, rfl⟩ := hneighbor
  exact A.glue_chain_caps C D hgp hanchor hC hD hn hsize hc hd

/-- Suk's chain-case induction for actual geometric support spikes.
Every spike contains a chain of more than 2^(n+K-4) points, and r*K reaches n.
No extraction or gluing hypothesis is assumed: both come from the geometric
chain theorems. The only relations between frames are witnessed adjacency. -/
theorem chain_case_of_frames {n K r : ℕ} {P : Finset Point}
    (F : Fin r → CapFrame) (C : (i : Fin r) → SpikeChain (F i))
    (hn : 4 ≤ n) (hK : 3 ≤ K) (hreach : n ≤ r * K)
    (hgp : GeneralPosition P)
    (hanchors : ∀ i, (F i).b ∈ P ∧ (F i).c ∈ P)
    (hpoints : ∀ i, (C i).points ⊆ P)
    (hsize : ∀ i, 2 ^ (n + K - 4) < (C i).length)
    (hneighbors : ∀ (i : ℕ) (hi : i + 1 < r),
      ∃ A : AdjacentCapFrames,
        A.left = F ⟨i, by omega⟩ ∧ A.right = F ⟨i + 1, hi⟩) :
    HasConvexNGon n P := by
  let L : ℕ → ℕ → Prop := fun i m => ∃ hi : i < r, (C ⟨i, hi⟩).LeftCap m
  let R : ℕ → ℕ → Prop := fun i m => ∃ hi : i < r, (C ⟨i, hi⟩).RightCap m
  apply iterated_cap_growth L R (HasConvexNGon n P) n K r (by omega) hK hreach
  · intro i _ m hnm hi
    obtain ⟨hi, hc⟩ := hi
    exact ((C ⟨i, hi⟩).leftCap_hasConvexNGon hc hnm).mono (hpoints _)
  · intro i _ m hnm hi
    obtain ⟨hi, hc⟩ := hi
    exact ((C ⟨i, hi⟩).rightCap_hasConvexNGon hc hnm).mono (hpoints _)
  · intro i hi a b hab hc hd
    obtain ⟨hic, hc⟩ := hc
    obtain ⟨hid, hd⟩ := hd
    exact glue_neighboring_chain_caps (C ⟨i, hic⟩) (C ⟨i + 1, hid⟩)
      (hneighbors i hi) hgp (hanchors _).2 (hpoints _) (hpoints _) hn hab hc hd
  · intro i hi a b ha hb hab
    have hgen : GeneralPosition (insert (F ⟨i, hi⟩).b
        (insert (F ⟨i, hi⟩).c (C ⟨i, hi⟩).points)) := by
      apply hgp.mono
      exact Finset.insert_subset_iff.mpr ⟨(hanchors _).1,
        Finset.insert_subset_iff.mpr ⟨(hanchors _).2, hpoints _⟩⟩
    rcases (C ⟨i, hi⟩).split_caps hgen (hsize _) ha hb hab with hc | hc
    · exact Or.inl ⟨hi, hc⟩
    · exact Or.inr ⟨hi, hc⟩

end ErdosSzekeres.Suk
