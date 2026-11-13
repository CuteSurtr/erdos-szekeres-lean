import ErdosSzekeres.HMPT.Maxima
import ErdosSzekeres.Suk.AntichainExtraction
import ErdosSzekeres.Suk.AntichainCaps

namespace ErdosSzekeres.HMPT

open Suk
open scoped BigOperators

/-- The local supporting edges that allow a cap to join caps in nonadjacent spikes. -/
def InnerCap (F : CapFrame) (s : Finset Point) : Prop :=
  ∀ p ∈ s, ∃ q ∈ s, p ≠ q ∧ ∀ z ∈ s, z ≠ p → z ≠ q →
    0 < orient p q F.a * orient p q z

theorem InnerCap.convexPosition {F : CapFrame} {s : Finset Point}
    (h : InnerCap F s) : ConvexPosition s := by
  apply convexPosition_of_pair_supports
  intro p hp
  obtain ⟨q, _, hpq, hs⟩ := h p hp
  refine ⟨q, orient p q F.a, hpq, ?_⟩
  intro z hz hzp
  by_cases hzq : z = q
  · exact Or.inl hzq
  · exact Or.inr (hs z hz hzp hzq)

/-- An attained maximum of supported caps in a fixed geometric antichain. -/
structure AntichainCapacity (F : CapFrame) (T : Finset Point) where
  cap : Finset Point
  subset : cap ⊆ T
  supports : InnerCap F cap
  maximal : ∀ U ⊆ T, InnerCap F U → U.card ≤ cap.card

theorem exists_antichainCapacity (F : CapFrame) (T : Finset Point) :
    Nonempty (AntichainCapacity F T) := by
  obtain ⟨S, hS, hs, hm⟩ := exists_max_card_subset T (InnerCap F) (by simp [InnerCap])
  exact ⟨⟨S, hS, hs, hm⟩⟩

/-- A maximal supported cap controls the entire antichain by cups-caps.
Padding its size to two makes the statement valid even for sets of size at most one. -/
theorem AntichainCapacity.card_le_binomial {F : CapFrame} {T : Finset Point}
    (B : AntichainCapacity F T) (hx : F.Horizontal) {n : ℕ} (hn : 3 ≤ n)
    (hgp : GeneralPosition T) (hspike : ∀ p ∈ T, p ∈ F.spike)
    (hanti : SpikeAntichain F T) (havoid : ¬ HasConvexNGon n T) :
    T.card ≤ (n + max 2 B.cap.card - 3).choose (n - 2) := by
  by_contra! hsize
  rcases F.antichain_cup_cap hx hn (b := max 2 B.cap.card + 1) (by omega)
      hgp hspike hanti (by convert hsize using 1) with hgon | ⟨U, hU, hcard, hs⟩
  · exact havoid hgon
  · have := B.maximal U hU hs
    omega

theorem AntichainCapacity.card_lt {F : CapFrame} {T : Finset Point}
    (B : AntichainCapacity F T) {n : ℕ} (havoid : ¬ HasConvexNGon n T) :
    B.cap.card < n := by
  by_contra! hsize
  exact havoid ((B.supports.convexPosition.hasConvexNGon hsize).mono B.subset)

/-- The budget of attained inner caps over any nonadjacent set of spikes. -/
theorem separated_cap_budget {r n : ℕ} {P : Finset Point}
    (A : ClockwiseAnchors (r + 3)) (T : Fin r → Finset Point)
    (B : (i : Fin r) → AntichainCapacity (A.frame i) (T i))
    (I : Finset (Fin r))
    (hsep : ∀ i ∈ I, ∀ j ∈ I, i ≠ j → i.val + 1 < j.val ∨ j.val + 1 < i.val)
    (hspike : ∀ i, ∀ p ∈ T i, p ∈ (A.frame i).spike)
    (hanti : ∀ i, SpikeAntichain (A.frame i) (T i))
    (hpoints : ∀ i, T i ⊆ P) (havoid : ¬ HasConvexNGon n P) :
    (∑ i ∈ I, (B i).cap.card) < n := by
  by_contra! hsize
  exact havoid (A.hasConvexNGon_union_antichain_caps_of_supports I (fun i => (B i).cap)
    hsep (fun i _ p hp => hspike i p ((B i).subset hp))
    (fun i _ => (hanti i).mono (B i).subset) (fun i _ => (B i).supports)
    (fun i _ => (B i).subset.trans (hpoints i)) hsize)

/-- Applying nonadjacent gluing to the even and odd spikes gives the full
horizontal cap budget without any nonempty-region assumption. -/
theorem parity_cap_budget {r n : ℕ} {P : Finset Point}
    (A : ClockwiseAnchors (r + 3)) (T : Fin r → Finset Point)
    (B : (i : Fin r) → AntichainCapacity (A.frame i) (T i))
    (hspike : ∀ i, ∀ p ∈ T i, p ∈ (A.frame i).spike)
    (hanti : ∀ i, SpikeAntichain (A.frame i) (T i))
    (hpoints : ∀ i, T i ⊆ P) (havoid : ¬ HasConvexNGon n P) :
    (∑ i, (B i).cap.card) ≤ 2 * (n - 1) := by
  classical
  have hbudget (b : ℕ) :
      (∑ i ∈ Finset.univ.filter (fun i : Fin r => i.val % 2 = b), (B i).cap.card) ≤ n - 1 := by
    have hlt := separated_cap_budget A T B
      (Finset.univ.filter (fun i : Fin r => i.val % 2 = b)) (by
        intro i hi j hj hij
        have hi' := (Finset.mem_filter.mp hi).2
        have hj' := (Finset.mem_filter.mp hj).2
        have hne : i.val ≠ j.val := fun he => hij (Fin.ext he)
        omega) hspike hanti hpoints havoid
    omega
  have heq : (∑ i, (B i).cap.card) =
      (∑ i ∈ Finset.univ.filter (fun i : Fin r => i.val % 2 = 0), (B i).cap.card) +
      (∑ i ∈ Finset.univ.filter (fun i : Fin r => i.val % 2 = 1), (B i).cap.card) := by
    simp only [Finset.sum_filter]
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    have hi : i.val % 2 = 0 ∨ i.val % 2 = 1 := by omega
    rcases hi with hi | hi <;> simp [hi]
  rw [heq]
  have h0 := hbudget 0
  have h1 := hbudget 1
  omega

end ErdosSzekeres.HMPT
