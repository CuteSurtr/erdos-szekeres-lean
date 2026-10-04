import ErdosSzekeres.Suk.AntichainCase
import ErdosSzekeres.Suk.SpikeDichotomy
import ErdosSzekeres.Suk.RegionSelection

namespace ErdosSzekeres.Suk

/-- The finite geometric engine of Suk's proof. A horizontal clockwise
support sequence and sufficiently populated spikes force an n-gon. The
chain/antichain dichotomy, selection, extraction, and gluing are all proved.
Positive-fraction extraction and asymptotic parameter estimates are separate. -/
theorem ClockwiseAnchors.finite_support_bound {k n K r t b : ℕ} {P : Finset Point}
    (A : ClockwiseAnchors (k + 3)) (hx : StrictMono (fun i => A.point i 0))
    (Q : Fin k → Finset Point)
    (hn : 4 ≤ n) (hK : 3 ≤ K) (hb : 3 ≤ b)
    (hchainreach : n ≤ r * K) (hantireach : n ≤ t * b) (hregions : t * (r + 1) ≤ k)
    (hgp : GeneralPosition P) (hanchors : ∀ i, A.point i ∈ P)
    (hpoints : ∀ i, Q i ⊆ P) (hspike : ∀ i, ∀ p ∈ Q i, p ∈ (A.frame i).spike)
    (hsize : ∀ i, 2 ^ (n + K - 4) * (n + b - 4).choose (n - 2) < (Q i).card) :
    HasConvexNGon n P := by
  classical
  let good : ℕ → Prop := fun i => ∃ hi : i < k, ∃ C : SpikeChain (A.frame ⟨i, hi⟩),
    2 ^ (n + K - 4) < C.length ∧ C.points ⊆ Q ⟨i, hi⟩
  rcases consecutive_or_separated good k r t hregions with ⟨start, hstart, hgood⟩ |
      ⟨f, hf, hsep⟩
  · let index : Fin r → Fin k := fun i => ⟨start + i.val, by omega⟩
    have hcs (i : Fin r) : ∃ C : SpikeChain (A.frame (index i)),
        2 ^ (n + K - 4) < C.length ∧ C.points ⊆ Q (index i) := by
      obtain ⟨hi, C, hlen, hsub⟩ := hgood i.val i.isLt
      exact ⟨C, hlen, hsub⟩
    choose C hlen hsub using hcs
    apply chain_case_of_frames (fun i => A.frame (index i)) C hn hK hchainreach hgp
    · intro i
      exact ⟨hanchors _, hanchors _⟩
    · intro i
      exact (hsub i).trans (hpoints (index i))
    · exact hlen
    · intro i hi
      exact A.adjacent_frames (start + i) (by omega)
  · let index : Fin t → Fin k := fun i => ⟨f i, (hf i).1⟩
    have hmono : StrictMono index := by
      intro i j hij
      have h := hsep i j hij
      change f i < f j
      omega
    let I : Finset (Fin k) := Finset.univ.image index
    have hI : I.card = t := by simp [I, Finset.card_image_of_injective _ hmono.injective]
    have hIsep : ∀ i ∈ I, ∀ j ∈ I, i ≠ j → i.val + 1 < j.val ∨ j.val + 1 < i.val := by
      intro i hi j hj hij
      obtain ⟨a, _, rfl⟩ := Finset.mem_image.mp hi
      obtain ⟨b, _, rfl⟩ := Finset.mem_image.mp hj
      have hab : a ≠ b := fun he => hij (congrArg index he)
      rcases lt_or_gt_of_ne hab with hab | hab
      · exact Or.inl (hsep a b hab)
      · exact Or.inr (hsep b a hab)
    have hanti : ∀ i : Fin k, ∃ S : Finset Point, i ∈ I →
        S ⊆ Q i ∧ (n + b - 4).choose (n - 2) < S.card ∧
          ∀ p ∈ S, ∀ q ∈ S, p ≠ q →
            q ∉ convexHull ℝ ({(A.frame i).a, (A.frame i).d, p} : Set Point) := by
      intro i
      by_cases hi : i ∈ I
      · obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hi
        rcases (A.frame (index j)).spike_chain_or_antichain (Q (index j)) (hspike _)
            (2 ^ (n + K - 4)) ((n + b - 4).choose (n - 2)) (hsize _) with
            ⟨C, hlen, hsub⟩ | ⟨S, hsub, hcard, hanti⟩
        · exact ((hf j).2 ⟨(hf j).1, C, hlen, hsub⟩).elim
        · exact ⟨S, fun _ => ⟨hsub, hcard, hanti⟩⟩
      · exact ⟨∅, fun h => (hi h).elim⟩
    choose S hS using hanti
    apply A.antichain_case hx I S (by omega) hb (by simpa only [hI] using hantireach)
      hgp hIsep
    · intro i hi p hp
      exact hspike i p ((hS i hi).1 hp)
    · intro i hi
      exact (hS i hi).2.2
    · intro i hi
      exact (hS i hi).1.trans (hpoints i)
    · intro i hi
      exact (hS i hi).2.1

end ErdosSzekeres.Suk
