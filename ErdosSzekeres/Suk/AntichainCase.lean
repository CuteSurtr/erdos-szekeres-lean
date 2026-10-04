import ErdosSzekeres.Suk.AntichainExtraction
import ErdosSzekeres.Suk.AntichainCaps

namespace ErdosSzekeres.Suk

open scoped BigOperators

/-- The finite geometric antichain case from Suk's proof. Each nonadjacent
part is an actual antichain in its outer-base triangle order. Cups-caps
extraction and all local and global support conditions are proved internally. -/
theorem ClockwiseAnchors.antichain_case {r n b : ℕ} {P : Finset Point}
    (A : ClockwiseAnchors (r + 3)) (hx : StrictMono (fun i => A.point i 0))
    (I : Finset (Fin r)) (Q : Fin r → Finset Point)
    (hn : 3 ≤ n) (hb : 3 ≤ b) (hreach : n ≤ I.card * b) (hgp : GeneralPosition P)
    (hsep : ∀ i ∈ I, ∀ j ∈ I, i ≠ j → i.val + 1 < j.val ∨ j.val + 1 < i.val)
    (hspike : ∀ i ∈ I, ∀ p ∈ Q i, p ∈ (A.frame i).spike)
    (hanti : ∀ i ∈ I, ∀ p ∈ Q i, ∀ q ∈ Q i, p ≠ q →
      q ∉ convexHull ℝ ({(A.frame i).a, (A.frame i).d, p} : Set Point))
    (hpoints : ∀ i ∈ I, Q i ⊆ P)
    (hsize : ∀ i ∈ I, (n + b - 4).choose (n - 2) < (Q i).card) :
    HasConvexNGon n P := by
  classical
  by_contra hnot
  have hcaps : ∀ i : Fin r, ∃ S : Finset Point, i ∈ I →
      S ⊆ Q i ∧ S.card = b ∧
        ∀ p ∈ S, ∃ q ∈ S, p ≠ q ∧ ∀ z ∈ S, z ≠ p → z ≠ q →
          0 < orient p q (A.frame i).a * orient p q z := by
    intro i
    by_cases hi : i ∈ I
    · rcases (A.frame i).antichain_cup_cap (A.frame_horizontal hx i) hn hb
          (hgp.mono (hpoints i hi)) (hspike i hi) (hanti i hi) (hsize i hi) with h | h
      · exact (hnot (h.mono (hpoints i hi))).elim
      · obtain ⟨S, hsub, hcard, hs⟩ := h
        exact ⟨S, fun _ => ⟨hsub, hcard, hs⟩⟩
    · exact ⟨∅, fun h => (hi h).elim⟩
  choose S hS using hcaps
  apply hnot
  apply A.hasConvexNGon_union_antichain_caps_of_supports I S hsep
  · intro i hi p hp
    exact hspike i hi p ((hS i hi).1 hp)
  · intro i hi p hp q hq hpq
    exact hanti i hi p ((hS i hi).1 hp) q ((hS i hi).1 hq) hpq
  · intro i hi
    exact (hS i hi).2.2
  · intro i hi
    exact (hS i hi).1.trans (hpoints i hi)
  · calc
      n ≤ I.card * b := hreach
      _ = ∑ _i ∈ I, b := by simp
      _ = ∑ i ∈ I, (S i).card :=
        Finset.sum_congr rfl (fun i hi => (hS i hi).2.1.symm)

end ErdosSzekeres.Suk
